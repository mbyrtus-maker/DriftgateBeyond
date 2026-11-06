# usage: python3 tools/corpsim/whale_v15.py MAKER KIND RATE  (e.g. mg gun 120)
# A wealthy pilot buys one maker's line in bulk from hour 4 to hour 8 (sim15's P['whale']), against the same 100 galaxies without them.
import sys,statistics as st,json
sys.path.insert(0,'/home/claude/driftgatebeyond/tools/corpsim')
from sim15 import sim,D
from run_v15 import at
from multiprocessing import Pool
M,K=sys.argv[1],sys.argv[2];RATE=float(sys.argv[3]);T0,T1=240,480
def one(a):
  seed,whale=a
  p={'log':True}
  if whale:p['whale']=dict(m=M,kind=K,t0=T0,t1=T1,rate=RATE)
  r=sim(seed,p);o={}
  lg=r['log']
  o['own_other']=sum(1 for t,m,net,ck,c,k in lg if T0<=t<T1 and m==M and k==K)
  o['rivals']=sum(1 for t,m,net,ck,c,k in lg if T0<=t<T1 and m!=M and k==K)
  o['maker_rest']=sum(1 for t,m,net,ck,c,k in lg if T0<=t<T1 and m==M and k!=K)
  ws=r.get('whale',dict(units=0,spend=0,list=0));o['w_units']=ws['units'];o['w_spend']=ws['spend'];o['w_list']=ws['list']
  sn=r.get('whale_snap',{});o['std']=(sn.get(T1,0)-sn.get(T0,0)) if whale else None
  mk=r['mkt'][M];a0=at(mk,T0);a1=at(mk,T1);a2=at(mk,T1+120);a3=at(mk,959)
  ok=lambda x:x and x[1]>0 and len(x)>10 and x[10]==a0[10]
  o['px']=[a0[1],a1[1] if ok(a1) else 0,a2[1] if ok(a2) else 0,a3[1] if ok(a3) else 0]
  o['E']=[a0[4],a1[4] if ok(a1) else 0]
  o['failed']=any(x[1]==M for x in r['failures'])
  rivals=[m for m in D['makers'] if m!=M]
  o['riv_proj']=sum(1 for t,m,k in r['news'] if k=='project' and m!=M and T0<=t<T1+120)
  o['riv_tw']=sum(1 for t,m,k in r['news'] if k=='tweak' and m!=M and T0<=t<T1+120)
  o['rev']=sum(net for t,m,net,ck,c,k in lg if T0<=t<T1 and m==M)
  o['ceo']=sum(1 for c in r['ceo_changes'] if c[1]==M)
  return o
N=100
with Pool(2) as pool:
  A=pool.map(one,[(s,False) for s in range(N)]);B=pool.map(one,[(s,True) for s in range(N)])
def m(L,k):return st.mean(x[k] for x in L)
print('whale units',m(B,'w_units'),'spend',round(m(B,'w_spend')),'paid vs list',round(sum(x['w_spend'] for x in B)/max(1,sum(x['w_list'] for x in B)),3))
for k in ('own_other','rivals','maker_rest','riv_proj','riv_tw','rev','ceo'):print(k,round(m(A,k),1),round(m(B,k),1))
for lab,L in (('base',A),('whale',B)):
  ch=[x['px'][1]/x['px'][0]-1 for x in L if x['px'][0]>0];ch2=[x['px'][2]/x['px'][1]-1 for x in L if x['px'][1]>0];ch3=[x['px'][3]/x['px'][0]-1 for x in L if x['px'][0]>0]
  print(lab,'price 4h->8h',round(st.mean(ch),3),'8h->10h',round(st.mean(ch2),3),'4h->16h',round(st.mean(ch3),3),'E',round(m(L,'E')[0] if False else st.mean(x['E'][0] for x in L)),round(st.mean(x['E'][1] for x in L)),'fail',sum(x['failed'] for x in L))
print('std fallback for kind during window (whale)',m(B,'std'))
# pump and dump: 40 shares bought at 4h, sold at 8h
pd=[40*(x['px'][1]-x['px'][0]) for x in B];base=[40*(x['px'][1]-x['px'][0]) for x in A]
print('40 shares 4h->8h gain whale',round(st.mean(pd)),'base',round(st.mean(base)),'extra',round(st.mean(pd)-st.mean(base)),'vs product spend',round(m(B,'w_spend')))
