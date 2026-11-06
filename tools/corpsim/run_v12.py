# usage: python3 tools/corpsim/run_v12.py  -> 200 galaxies of 16 h per setting; writes res_v12.json beside this file
import json,statistics as st,sys,os
from collections import Counter,defaultdict
from multiprocessing import Pool
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from sim12 import P as sim_P,sim,D,CEOS,GRADES
N=200
def pct(v,q):v=sorted(v);return v[min(len(v)-1,int(q*len(v)))] if v else 0
def one(a):
  name,p=a;R=[sim(s,p) for s in range(N)];ms=list(D['makers'])
  o=dict(name=name)
  f=[len(r['failures']) for r in R];o['fail']=st.mean(f);o['nofail']=sum(1 for x in f if x==0)/N
  o['failby']=Counter(D['makers'][x[1]]['name'] for r in R for x in r['failures']).most_common()
  o['projects']=st.mean(len(r['projects']) for r in R);o['launches']=st.mean(len(r['launches']) for r in R)
  o['launch_g']={g:sum(1 for r in R for x in r['launches'] if x[3]==g)/N for g in (2,3,4,5)}
  o['first_launch_h']=st.median([r['launches'][0][0]/60 for r in R if r['launches']] or [0])
  o['proj_time']={g:st.median([x[4]/60 for r in R for x in r['launches'] if x[3]==g] or [0]) for g in (2,3,4,5)}
  o['launch_kind']=Counter(x[2] for r in R for x in r['launches']).most_common()
  o['launch_maker']={D['makers'][m]['name']:sum(1 for r in R for x in r['launches'] if x[1]==m)/N for m in ms}
  o['max_grade']=Counter(max(x[9] for x in r['lines']) for r in R)
  o['sales_g']={g:st.mean(r['sales_g'][g]/max(1,r['sales']) for r in R) for g in GRADES}
  o['faction_std']=st.mean(r['faction_std']/(r['faction_std']+r['sales']) for r in R)
  o['sab']=st.mean(r['sab'] for r in R);o['sab_hit']=st.mean(r['sab_hit'] for r in R);o['spy']=st.mean(r['spy'] for r in R)
  mk=set(k for r in R for k in r['missions']);o['missions']={k:st.mean(r['missions'].get(k,0) for r in R) for k in sorted(mk)};o['missions_total']=sum(o['missions'].values())
  o['ceo_changes']=st.mean(len(r['ceo_changes']) for r in R)
  o['ore_cr']=st.mean(r['ore_cr'] for r in R);o['div']=st.mean(r['div'] for r in R);o['min_margin']=min(r['min_margin'] for r in R)
  o['gtime']=[(R[0]['gtime'][i][0]//60,st.mean(r['gtime'][i][2] for r in R),st.mean(r['gtime'][i][3] for r in R)) for i in range(len(R[0]['gtime']))]
  o['top']=Counter(D['makers'][max(ms,key=lambda m:r['rev'][m])]['name'] for r in R).most_common()
  o['first_launch_p']=(pct([x['launches'][0][0]/60 for x in R if x['launches']],.1),pct([x['launches'][0][0]/60 for x in R if x['launches']],.9))
  if p.get('rd_cost',{}).get(2,0)>1e8:
    R2=[sim(s,dict(p,log=True)) for s in range(100)]
    o['earn']={D['makers'][m]['name']:(st.mean(sum(net-c*ck for t,mm,net,ck,c in r['log'] if mm==m) for r in R2)/16,(sim_P['upk']+sim_P['upk_line']*len(R2[0]['deal'][m]))*1.0) for m in ms}
  ks=Counter();[ks.update(x['kind_sales']) for x in R];tot=sum(ks.values()) or 1
  o['kinds']={k:v/tot for k,v in ks.most_common()};o['mining']=sum(ks[k] for k in ('mlaser','charge','drill'))/tot
  o['sales_n']=st.mean(x['sales'] for x in R)
  o['spy_hit']=st.mean(r['spy_hit'] for r in R)
  pb={}
  for pw in ('halcyon','varkesh','ostrova'):
    tot=Counter()
    for r in R:tot.update(r['pw_buys'].get(pw,{}))
    n=sum(tot.values()) or 1;pb[pw]=[(D['makers'][m]['name'],round(c/n,3)) for m,c in tot.most_common(4)]
  o['pw_buys']=pb
  o['per_maker']={D['makers'][m]['name']:dict(lines=len(R[0]['deal'][m]),rev_h=st.mean(r['rev'][m] for r in R)/16,px=st.median([r['px'][m][-1][1] for r in R if r['px'][m]]),
     px10=pct([r['px'][m][-1][1] for r in R if r['px'][m]],.1),px90=pct([r['px'][m][-1][1] for r in R if r['px'][m]],.9),fail=sum(1 for r in R for x in r['failures'] if x[1]==m),
     launches=sum(1 for r in R for x in r['launches'] if x[1]==m)/N) for m in ms}
  return name,o
V=[('v12',{}),('v12 without R&D',{'rd_cost':{2:1e9,3:1e9,4:1e9,5:1e9}}),('v11 running costs, for comparison',{'upk':120,'upk_line':25,'rd_reserve':6}),('v12 over 32 h',{'hours':32})]
if __name__=='__main__':
  res={}
  with Pool(2) as p:
    for n,o in p.imap(one,V):res[n]=o;print(n,'done',flush=True)
  json.dump(res,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'res_v12.json'),'w'),default=str)
