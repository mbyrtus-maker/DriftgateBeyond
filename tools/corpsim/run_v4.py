# usage: python3 tools/corpsim/run_v4.py  -> 200 galaxies of 16 h per setting; writes res_v4.json beside this file
import json,statistics as st,sys,os
from collections import Counter,defaultdict
from multiprocessing import Pool
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from sim4 import sim,CEOS,EVENTS,FREEPORTS,D,SYSTEMS,COST_KEYS,PT,strength,weakness
N=200
def pct(v,q):v=sorted(v);return v[min(len(v)-1,int(q*len(v)))]
def one(a):
  name,p=a;R=[sim(s,p) for s in range(N)]
  o=dict(name=name);ms=list(D['makers'])
  f=[len(r['failures']) for r in R];o['fail']=st.mean(f);o['nofail']=sum(1 for x in f if x==0)/N
  o['failby']=Counter(D['makers'][x[1]]['name'] for r in R for x in r['failures']).most_common()
  o['fail_ceo']=Counter(x[3] for r in R for x in r['failures']).most_common()
  o['rep']=st.mean(len(r['replacements']) for r in R);o['rep_kind']=Counter(x[2] for r in R for x in r['replacements']).most_common()
  o['tweaks']=st.mean(r['tweaks'] for r in R);o['ore_cr']=st.mean(r['ore_cr'] for r in R);o['ore_units']=st.mean(r['ore_units'] for r in R)
  o['min_margin']=min(r['min_margin'] for r in R);o['div']=st.mean(r['div'] for r in R);o['struggling']=st.mean(sum(r['struggling'].values()) for r in R)
  o['sys_share']=st.mean(r['sales_sys']/r['sales'] for r in R);o['std_share']=st.mean(r['sales_std']/r['sales'] for r in R);o['lost']=st.mean(r['lost']/(r['lost']+r['sales']) for r in R)
  o['opened']=st.mean(r['opened'] for r in R);o['crazes']=st.mean(r['crazes'] for r in R)
  sold=[x for r in R for x in r['lines'] if x[7]>0];pm=[x[6] for x in sold]
  o['pm']=dict(med=st.median(pm),p10=pct(pm,.1),p90=pct(pm,.9),over12=sum(1 for x in pm if x>1.2)/len(pm),under09=sum(1 for x in pm if x<.9)/len(pm))
  tl=[x for r in R for x in r['lines'] if not x[2]]
  gs=lambda tr:max([PT(k,v) for k,v in tr.items() if k!='mag' and ((k not in COST_KEYS and v>0) or (k in COST_KEYS and v<0))]+[0])
  o['boost']=dict(over20=sum(1 for x in tl if gs(x[5])>=20)/len(tl),mean=st.mean(gs(x[5]) for x in tl),net_mean=st.mean(strength(x[5])-weakness(x[5]) for x in tl),net_max=max(strength(x[5])-weakness(x[5]) for x in tl),
     rule_ok=all(weakness(t)>=strength(t)/2-1e-6 for x in tl for t in x[8] if t))
  # CEOs
  o['ceo_changes']=st.mean(len(r['ceo_changes']) for r in R);o['ceo_why']=Counter(x[4] for r in R for x in r['ceo_changes'])
  ten=defaultdict(list)
  for r in R:
    for m in ms:
      cs=r['ceos'][m];px=r['px'][m]
      for i,(t0,c,why) in enumerate(cs):
        t1=cs[i+1][0] if i+1<len(cs) else 16*60;end=cs[i+1][2] if i+1<len(cs) else 'end'
        a=[(p,d) for t,p,d in px if t0<=t<=t1]
        if len(a)>=2 and t1>t0:ten[c].append((((a[-1][0]+a[-1][1]-a[0][1])/a[0][0]-1)/((t1-t0)/60),(t1-t0)/60,end))
  o['ceo']={c:dict(n=len(v),growth_h=st.mean(x[0] for x in v),growth_med=st.median(x[0] for x in v),tenure_h=st.mean(x[1] for x in v),ousted=sum(1 for x in v if x[2] in('line','shares'))/len(v)) for c,v in ten.items()}
  # variety: who sells most, galaxy to galaxy
  top=Counter(max(ms,key=lambda m:r['rev'][m]) for r in R);o['top']={D['makers'][m]['name']:n for m,n in top.most_common()}
  o['rev_range']={D['makers'][m]['name']:(pct([r['rev'][m]/16 for r in R],.1),st.median([r['rev'][m]/16 for r in R]),pct([r['rev'][m]/16 for r in R],.9)) for m in ms}
  o['ten_end']={c:Counter(x[2] for x in v) for c,v in ten.items()}
  o['station_std']=st.mean(r['station_std']/(r['station_std']+r['sales']) for r in R)
  o['events']=st.mean(len(r['events']) for r in R);o['ev_kind']={k:sum(1 for r in R for e in r['events'] if e['k']==k)/N for k in EVENTS}
  fp=lambda m:D['makers'][m]['home'] in('mw','cw','ew')
  o['fail_fp']=sum(1 for r in R for x in r['failures'] if fp(x[1]));o['fail_n']=sum(len(r['failures']) for r in R)
  o['px_end']={w:(pct([r['px'][m][-1][1] for r in R for m in ms if fp(m)==(w=='freeport') and r['px'][m]],.1),st.median([r['px'][m][-1][1] for r in R for m in ms if fp(m)==(w=='freeport') and r['px'][m]]),pct([r['px'][m][-1][1] for r in R for m in ms if fp(m)==(w=='freeport') and r['px'][m]],.9)) for w in ('freeport','power')}
  # CEO changes while an event touched the galaxy, per hour, against the rest
  inn=out=0;tin=tout=0
  for r in R:
    on=[0]*(16*60)
    for e in r['events']:
      for t in range(e['t0'],min(e['t1'],16*60)):on[t]=1
    tin+=sum(on)/60;tout+=(16*60-sum(on))/60
    for c in r['ceo_changes']:
      if on[min(c[0],16*60-1)]:inn+=1
      else:out+=1
  o['ceo_rate_event']=inn/max(1,tin);o['ceo_rate_calm']=out/max(1,tout)
  o['lines_per_maker']=st.mean(len(r['deal'][m]) for r in R for m in ms)
  return name,o
V=[('v4',{}),('v4 without events',{'events':False}),('v4, makers sell only at home',{'all_freeports':False}),('v4 without CEOs',{'ceo':False})]
if __name__=='__main__':
  res={}
  with Pool(2) as p:
    for n,o in p.imap(one,V):res[n]=o;print(n,json.dumps({k:(round(v,3) if isinstance(v,float) else v) for k,v in o.items() if k not in('rev_range',)},default=str),'\n',flush=True)
  json.dump(res,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'res_v4.json'),'w'),default=str)
