# usage: python3 tools/corpsim/run_v19.py -> 200 galaxies of 16 h per setting (N=, W=); writes res_v20.json
# v20: running costs scaled to each line's market
import sys,os,json,statistics as stt
from collections import Counter
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import sim20
from multiprocessing import Pool
N=int(os.environ.get('N',200))
def one(a):
  seed,p=a;p=dict(p);h=p.pop('_h',16);r=sim20.sim(seed,dict(p,hours=h))
  return dict(fail=len(r['failures']),who=[f[1] for f in r['failures']],diag=r.get('diag',[]),launches=len(r['launches']),g3=any(x[3]>=3 for x in r['launches']),
              sales=r['sales'],std=r['faction_std'],shut=r.get('shut',0),md=r.get('markdowns',0))
SET=[('v19 flat 240 + 50, 32 h',dict(_h=32)),
     ('scaled: 60 + 0.5 of fair margin, 32 h',dict(upk_f=.5,upk_base=60,_h=32)),
     ('scaled: 60 + 0.7 of fair margin, 32 h',dict(upk_f=.7,upk_base=60,_h=32)),
     ('scaled: 120 + 0.5 of fair margin, 32 h',dict(upk_f=.5,upk_base=120,_h=32)),
     ('scaled: 60 + 0.85 of fair margin, 32 h',dict(upk_f=.85,upk_base=60,_h=32)),
     ('scaled: 60 + 0.5, 16 h',dict(upk_f=.5,upk_base=60))]
if __name__=='__main__':
  out={}
  with Pool(int(os.environ.get('W',2))) as pool:
    for name,p in SET:
      R=pool.map(one,[(i,p) for i in range(N)])
      f=[x['fail'] for x in R];D=[d for x in R for d in x['diag']];C=Counter(d['cause'] for d in D)
      o=dict(fail=round(stt.mean(f),2),none=round(sum(1 for x in f if x==0)/N*100),launches=round(stt.mean(x['launches'] for x in R),1),g3=round(sum(x['g3'] for x in R)/N*100),
             sales=round(stt.mean(x['sales'] for x in R)),std=round(stt.mean(x['std'] for x in R)),shut=round(stt.mean(x['shut'] for x in R),1),
             causes={k:round(v/max(1,len(D))*100) for k,v in C.most_common()},share=round(stt.median([d['share'] for d in D]),2) if D else None,
             age_h=round(stt.median([d['age'] for d in D])/60,1) if D else None,stock=round(stt.median([d['stock'] for d in D])) if D else None,
             who=dict(Counter(w for x in R for w in x['who']).most_common(6)),ceo=dict(Counter(d['ceo'] for d in D).most_common(4)))
      out[name]=o;print(name,json.dumps(o),flush=True)
  json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'res_v20.json'),'w'),indent=1)
