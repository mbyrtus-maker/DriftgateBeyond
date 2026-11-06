# usage: python3 tools/corpsim/run_v16.py  -> 200 galaxies of 16 h per setting (N=, W= to change); writes res_v16.json
# v16: makers answer a rival that outsells them with a tweak (then R&D). How often they tweak and why, how much R&D it
# starts, failures, and whether any maker stays on top of a kind of part for long.
import sys,os,json,statistics as st
from collections import defaultdict,Counter
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from sim16 import sim,D
from multiprocessing import Pool
N=int(os.environ.get('N',200))
def one_g(a):
  seed,p=a;p=dict(p);p['log']=True;r=sim(seed,p)
  o=dict(fail=len(r['failures']),launches=len(r['launches']),first=min((x[0] for x in r['launches']),default=None))
  o['tw']=Counter(x[3] for x in r.get('tweak_log',[]));o['proj']=Counter(x[4] if len(x)>4 else 'disliked' for x in r['projects'])
  o['ceo']=len(r['ceo_changes']);o['grade3']=any(x[3]>=3 for x in r['launches'])
  # leaders: per kind and 2-hour block from 4 h, the top maker's share of corporate sales of that kind
  blocks=defaultdict(Counter)
  for t,m,net,ck,c,k in r['log']:
    if t>=240:blocks[(k,(t-240)//120)][m]+=1
  lead=[];runs=defaultdict(list)
  for (k,b),c in sorted(blocks.items()):
    n=sum(c.values())
    if n<8 or len(c)<1:continue
    m,top=c.most_common(1)[0];lead.append(top/n);runs[k].append(m if top/n>=.6 else None)
  o['lead']=lead
  # the longest run of 2-hour blocks one maker held 60% or more of a kind
  longest=[]
  for k,seq in runs.items():
    best=cur=0;prev=None
    for m in seq:
      cur=cur+1 if (m is not None and m==prev) else (1 if m is not None else 0);prev=m;best=max(best,cur)
    longest.append(best)
  o['longest']=longest
  o['rev']=r['rev'];o['failby']=[x[1] for x in r['failures']]
  return o
def one(v):
  name,p=v
  with Pool(int(os.environ.get('W',2))) as pool:R=pool.map(one_g,[(s,p) for s in range(N)])
  o={'fail':st.mean(r['fail'] for r in R),'nofail':sum(1 for r in R if r['fail']==0)/N,'launches':st.mean(r['launches'] for r in R),
     'first_h':st.median(r['first'] for r in R if r['first'] is not None)/60,'ceo':st.mean(r['ceo'] for r in R),'grade3':sum(r['grade3'] for r in R)/N}
  o['tweaks']={k:sum(r['tw'][k] for r in R)/N for k in ('disliked','outsold','both')};o['tweaks_all']=sum(o['tweaks'].values())
  o['projects']={k:sum(r['proj'][k] for r in R)/N for k in ('disliked','outsold','both')}
  L=[x for r in R for x in r['lead']];o['lead_mean']=st.mean(L);o['lead_60']=sum(1 for x in L if x>=.6)/len(L);o['lead_80']=sum(1 for x in L if x>=.8)/len(L)
  lg=[x for r in R for x in r['longest']];o['long_run_blocks']=st.mean(lg);o['kinds_held_6h']=sum(1 for x in lg if x>=3)/len(lg)
  fb=Counter(m for r in R for m in r['failby']);o['failby']={D['makers'][m]['name']:v for m,v in fb.most_common()}
  tops=Counter(max(r['rev'],key=r['rev'].get) for r in R);o['top']={D['makers'][m]['name']:v for m,v in tops.most_common()}
  return name,o
V=[('v16',{}),('v15 rules (no answer to a rival)',{'outsold':False}),('being outsold also leads to R&D',{'out_rd':True}),('v16 at 1.5 times',{'out_ratio':1.5}),('v16 every 15 min',{'out_cool':15})]
if __name__=='__main__':
  res={}
  for v in V:
    n,o=one(v);res[n]=o;print(n,{k:(round(x,3) if isinstance(x,float) else x) for k,x in o.items() if k not in('failby','top')},flush=True)
  json.dump(res,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'res_v16.json'),'w'),indent=1)
