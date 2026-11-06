import json,statistics as st,sys
from collections import Counter,defaultdict
from multiprocessing import Pool
from sim2 import sim,CAT,KINDS,strength,weakness,COST_KEYS,PT,SYSTEMS
N=200
def one(a):
  name,p=a;R=[sim(s,p) for s in range(N)]
  out=dict(name=name)
  f=[len(r['failures']) for r in R];out['fail']=st.mean(f);out['nofail']=sum(1 for x in f if x==0)/N
  out['failby']=Counter(nm for r in R for t,m,nm in r['failures']).most_common()
  out['tweaks']=st.mean(r['tweaks'] for r in R);out['tk']={k:sum(r['tk'].get(k,0) for r in R)/N for k in ('boost','move')}
  out['rep']=st.mean(len(r['replacements']) for r in R);out['rep_kind']=Counter(x[3] for r in R for x in r['replacements']).most_common()
  out['rep_line']=Counter(x[2] for r in R for x in r['replacements']).most_common(12)
  out['rep_first_h']=st.median([r['replacements'][0][0]/60 for r in R if r['replacements']] or [0])
  out['ore_t']=st.mean(r['ore_t'] for r in R);out['ore_cr']=st.mean(r['ore_cr'] for r in R);out['ore_units']=st.mean(r['ore_units'] for r in R)
  out['min_margin']=min(r['min_margin'] for r in R)
  out['sales']=st.mean(r['sales'] for r in R);out['sys_share']=st.mean(r['sales_sys']/r['sales'] for r in R);out['std_share']=st.mean(r['sales_std']/r['sales'] for r in R)
  out['div']=st.mean(r['div'] for r in R);out['crazes']=st.mean(r['crazes'] for r in R);out['spikes']=st.mean(r['spikes'] for r in R)
  out['struggling']=st.mean(sum(r['struggling'].values()) for r in R)
  sold=[x for r in R for x in r['lines'] if x[8]>0]
  pms=[x[7] for x in sold];out['pm']=dict(med=st.median(pms),p10=sorted(pms)[len(pms)//10],p90=sorted(pms)[9*len(pms)//10],max=max(pms),over12=sum(1 for x in pms if x>1.2)/len(pms),under09=sum(1 for x in pms if x<.9)/len(pms))
  # price by kind (median end price multiplier of lines that sold)
  bk=defaultdict(list)
  for x in sold:bk[x[2]].append(x[7])
  out['pm_kind']={k:round(st.median(v),2) for k,v in bk.items()}
  # boosts and the trade-off rule on every trait line at the end
  tl=[x for r in R for x in r['lines'] if not x[3]]
  gs=lambda tr:max([PT(k,v) for k,v in tr.items() if k!='mag' and ((k not in COST_KEYS and v>0) or (k in COST_KEYS and v<0))]+[0])
  out['boost']=dict(max=max(gs(x[6]) for x in tl),mean=st.mean(gs(x[6]) for x in tl),over20=sum(1 for x in tl if gs(x[6])>=20)/len(tl),
     net_max=max(strength(x[6])-weakness(x[6]) for x in tl),net_mean=st.mean(strength(x[6])-weakness(x[6]) for x in tl),
     rule_ok=all(weakness(tr)>=strength(tr)/2-1e-6 for x in tl for tr in x[9] if tr),std_zero=all(not x[6] for r in R for x in r['lines'] if x[3]))
  top=sorted(((gs(x[6]),x[1],x[6]) for x in tl),key=lambda z:-z[0])[:10];out['top']=top
  out['T']={m:st.median(r['T'][m] for r in R) for m in R[0]['T']};out['divm']={m:st.median(r['divm'][m] for r in R) for m in R[0]['T']}
  out['rev']={m:st.mean(r['rev'][m] for r in R)/16 for m in R[0]['T']};out['rev_sys']={m:st.mean(r['rev_sys'][m] for r in R)/16 for m in R[0]['T']}
  out['px']={m:st.median(r['px'][m][-1][1] for r in R if r['px'][m]) for m in R[0]['T']}
  out['boost_t']=[(R[0]['boost_t'][i][0]//60,st.mean(r['boost_t'][i][1] for r in R),max(r['boost_t'][i][1] for r in R),st.mean(r['boost_t'][i][2] for r in R)) for i in range(len(R[0]['boost_t']))]
  # one galaxy's story of a replaced product
  for r in R:
    if r['replacements']:out['story']=r['replacements'][:3];break
  return name,out
V=[('v2',{}),('v2 no system parts',{'systems':False}),('v2 price floor at list',{'down_floor':'base'}),('v2 running cost 60 + 15',{'upk':60,'upk_line':15})]
if __name__=='__main__':
  res={}
  with Pool(2) as p:
    for n,o in p.imap(one,V):
      res[n]=o;print(n,json.dumps({k:(round(v,3) if isinstance(v,float) else v) for k,v in o.items() if k in('fail','nofail','failby','tweaks','tk','rep','rep_kind','rep_first_h','ore_t','ore_cr','min_margin','sys_share','std_share','pm','boost','div','crazes','struggling')}),flush=True)
  json.dump(res,open(__file__.rsplit('/',1)[0]+'/res_v2.json','w'),default=str)
