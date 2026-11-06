# usage: python3 tools/corpsim/whale2_v15.py MAKER KIND RATE  (e.g. mg gun 120)
# What a pilot's bulk buying of one maker's line (hour 4 to hour 8) does to the other makers of that kind of part and to
# its buyers, against the same 100 galaxies without them (sim15's P['whale'] at rate 0).
import sys,os,statistics as st
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from sim15 import sim,D
from run_v15 import at
from multiprocessing import Pool
M,K=sys.argv[1],sys.argv[2];RATE=float(sys.argv[3]);T0,T1=240,480
def one(a):
  seed,rate=a
  r=sim(seed,{'log':True,'whale':dict(m=M,kind=K,t0=T0,t1=T1,rate=rate)})
  lg=r['log'];makers=[m for m in D['makers'] if any(x[1]==m and x[5]==K for x in lg)]
  o={'std':r['whale_snap'][T1]-r['whale_snap'][T0],'pm':r.get('whale_pm',{}),'whale':r.get('whale',{}).get('units',0),'mk':{}}
  for m in makers:
    mk=r['mkt'][m];a0=at(mk,T0);ok=lambda x:x and x[1]>0 and len(x)>10 and x[10]==a0[10]
    a1=at(mk,T1);a3=at(mk,959)
    o['mk'][m]=dict(sold=sum(1 for t,mm,net,ck,c,k in lg if T0<=t<T1 and mm==m and k==K),
      sold_after=sum(1 for t,mm,net,ck,c,k in lg if T1<=t<T1+240 and mm==m and k==K),
      tweaks=sum(1 for t,mm,k in r.get('tweak_log',[]) if mm==m and k==K and T0<=t<T1+120),
      proj=sum(1 for t,mm,k,g in r['projects'] if mm==m and k==K and T0<=t<T1+240),
      px=(a1[1]/a0[1]-1) if ok(a1) and a0[1]>0 else -1,px16=(a3[1]/a0[1]-1) if ok(a3) and a0[1]>0 else -1,
      E=(a1[4] if ok(a1) else 0)-a0[4],failed=any(x[1]==m and x[0]>=T0 for x in r['failures']))
  return o
N=100
with Pool(2) as pool:
  A=pool.map(one,[(s,0) for s in range(N)]);B=pool.map(one,[(s,RATE) for s in range(N)])
names={m:D['makers'][m]['name'] for m in D['makers']}
ms=sorted({m for o in A+B for m in o['mk']},key=lambda m:m!=M)
print(f'pilot buys {st.mean(o["whale"] for o in B):.0f} of {names[M]}\'s {K} lines')
print('buyers who took the faction standard part instead, hours 4-8:',round(st.mean(o['std'] for o in A),1),'->',round(st.mean(o['std'] for o in B),1))
for m in ms:
  def f(L,k):
    v=[o['mk'][m][k] for o in L if m in o['mk']];return st.mean(v) if v else 0
  pmA=st.mean(o['pm'].get(m,1) for o in A);pmB=st.mean(o['pm'].get(m,1) for o in B)
  print(f"{names[m]:24s} sold h4-8 {f(A,'sold'):5.1f}->{f(B,'sold'):5.1f} | h8-12 {f(A,'sold_after'):5.1f}->{f(B,'sold_after'):5.1f} | price x{pmA:.2f}->x{pmB:.2f} | tweaks {f(A,'tweaks'):.2f}->{f(B,'tweaks'):.2f} | R&D {f(A,'proj'):.2f}->{f(B,'proj'):.2f} | earn/h {f(A,'E'):+.0f}->{f(B,'E'):+.0f} | shares h4-8 {f(A,'px'):+.0%}->{f(B,'px'):+.0%} h4-16 {f(A,'px16'):+.0%}->{f(B,'px16'):+.0%} | failed {sum(o['mk'][m]['failed'] for o in A if m in o['mk'])}->{sum(o['mk'][m]['failed'] for o in B if m in o['mk'])}")
