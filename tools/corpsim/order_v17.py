# usage: python3 tools/corpsim/order_v17.py MAKER KIND UNITS [SHARE]  (e.g. mg gun 60)
# A faction's bulk order with one maker at hour 4 (sim17's P['orders']): how long it takes to fill, and what it does to the
# maker's own buyers, its rivals and the faction standard parts, against the same 100 galaxies without the order.
import sys,os,statistics as st
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from sim17 import sim,D
from multiprocessing import Pool
M,K,U=sys.argv[1],sys.argv[2],int(sys.argv[3]);SH=float(sys.argv[4]) if len(sys.argv)>4 else .5;T0=240
def one(a):
  seed,on=a;p={'log':True,'order_share':SH}
  if on:p['orders']=[dict(m=M,kind=K,units=U,t0=T0)]
  r=sim(seed,p);o=r['orders_out'][0] if on else None
  t1=(o['t_done'] if o and o['t_done'] else T0+240) if on else None
  return dict(o=o,log=[(t,m,k) for t,m,net,ck,c,k in r['log'] if T0<=t<T0+360],fail=any(x[1]==M for x in r['failures']),std=r['faction_std'])
N=100
with Pool(2) as pool:A=pool.map(one,[(s,False) for s in range(N)]);B=pool.map(one,[(s,True) for s in range(N)])
done=[x['o']['t_done']-T0 for x in B if x['o'] and x['o']['t_done']]
print(f"order of {U} {K} from {D['makers'][M]['name']} at hour 4, works share {SH}: filled in {len(done)}/{N}, median {st.median(done):.0f} min (10%-90%: {sorted(done)[len(done)//10]:.0f}-{sorted(done)[len(done)*9//10]:.0f})")
W=int(st.median(done))
def cnt(L,f):return st.mean(sum(1 for t,m,k in x['log'] if t<T0+W and f(m,k)) for x in L)
print(f"while it fills ({W} min): maker's other sales of {K} {cnt(A,lambda m,k:m==M and k==K):.1f} -> {cnt(B,lambda m,k:m==M and k==K):.1f}; its other lines {cnt(A,lambda m,k:m==M and k!=K):.1f} -> {cnt(B,lambda m,k:m==M and k!=K):.1f}; rivals' {K} {cnt(A,lambda m,k:m!=M and k==K):.1f} -> {cnt(B,lambda m,k:m!=M and k==K):.1f}")
print('maker failures',sum(x['fail'] for x in A),'->',sum(x['fail'] for x in B))
