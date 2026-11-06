# usage: python3 tools/corpsim/run_v18.py -> 200 galaxies of 16 h per setting (N=, W=); writes res_v18.json
# v18: "go broke or go home": no reserve, storage charged by the station on every unit (shut lines too), stale goods marked
# down below the profit floor, shut lines sell out their stock, a launch retires the old grade. Failures, by maker and by
# cause, against v17, and each rule on its own.
import sys,os,json,statistics as stt
from collections import Counter
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import sim17,sim18
from multiprocessing import Pool
N=int(os.environ.get('N',200));H=int(os.environ.get('H',16))
def one(a):
  v,seed,p=a;r=(sim17 if v==17 else sim18).sim(seed,dict(p,hours=H))
  T=r['T'];return dict(fail=len(r['failures']),who=[f[1] for f in r['failures']],ceo=[f[3] for f in r['failures']],at=[f[0] for f in r['failures']],launches=len(r['launches']),
    g3=any(x[3]>=3 for x in r['launches']),sales=r['sales'],std=r['faction_std'],tweaks=r['tweaks'],storage=r.get('storage',0),md=r.get('markdowns',0),shut=r.get('shut',0),
    minm=r['min_margin'],poor=sum(1 for m,t in T.items() if t<1500),rich=sum(1 for m,t in T.items() if t>6000),ceos=len(r['ceo_changes']))
SET=[('v17 (budget line, 3 h reserve, no storage)',17,{}),
     ('v18: all the new rules (storage 3%/h)',18,{}),
     ('v18 at storage 2%/h',18,dict(store_h=.02)),
     ('v18 at storage 5%/h',18,dict(store_h=.05)),
     ('v18 without markdowns',18,dict(md_min=1.0)),
     ('only: no reserve',17,dict(reserve=0,rd_reserve=0)),
     ('only: old grade retired',17,dict(old='retire')),
     ('only: storage 3%/h + markdowns + shut lines sell out',18,dict(reserve=3,rd_reserve=3,old='budget')),
     ('v18 with no CEO reserves at all',18,dict(ceo_reserve=False))]
if __name__=='__main__':
  out={}
  with Pool(int(os.environ.get('W',2))) as pool:
    for name,v,p in SET:
      R=pool.map(one,[(v,i,p) for i in range(N)])
      f=[x['fail'] for x in R];who=Counter(w for x in R for w in x['who']);ceo=Counter(w for x in R for w in x['ceo'])
      at=[t for x in R for t in x['at']]
      o=dict(fail=round(stt.mean(f),2),none=round(sum(1 for x in f if x==0)/N*100),launches=round(stt.mean(x['launches'] for x in R),1),g3=round(sum(x['g3'] for x in R)/N*100),
             sales=round(stt.mean(x['sales'] for x in R)),std=round(stt.mean(x['std'] for x in R)),tweaks=round(stt.mean(x['tweaks'] for x in R)),storage=round(stt.mean(x['storage'] for x in R)),
             md=round(stt.mean(x['md'] for x in R)),shut=round(stt.mean(x['shut'] for x in R),1),poor=round(stt.mean(x['poor'] for x in R),2),rich=round(stt.mean(x['rich'] for x in R),2),
             first_fail_h=round(stt.median(at)/60,1) if at else None,who=dict(who.most_common()),ceo=dict(ceo.most_common()),ceos=round(stt.mean(x['ceos'] for x in R),1))
      out[name]=o;print(name,json.dumps({k:v for k,v in o.items() if k not in('who','ceo')}),'\n   failed:',dict(who.most_common(6)),'CEO:',dict(ceo.most_common(4)),flush=True)
  json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'res_v18.json'),'w'),indent=1)
