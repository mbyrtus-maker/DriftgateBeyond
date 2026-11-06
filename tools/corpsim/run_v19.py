# usage: python3 tools/corpsim/run_v19.py -> 200 galaxies of 16 h per setting (N=, W=); writes res_v19.json
# v19: prudent makers under v18's no-net rules; failures and why each one happened
import sys,os,json,statistics as stt
from collections import Counter
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import sim19
from multiprocessing import Pool
N=int(os.environ.get('N',200))
def one(a):
  seed,p=a;p=dict(p);h=p.pop('_h',16);r=sim19.sim(seed,dict(p,hours=h))
  return dict(fail=len(r['failures']),who=[f[1] for f in r['failures']],diag=r.get('diag',[]),launches=len(r['launches']),g3=any(x[3]>=3 for x in r['launches']),
              sales=r['sales'],std=r['faction_std'],shut=r.get('shut',0),md=r.get('markdowns',0))
SET=[('prudent makers, running costs 240 + 50 a line',{}),('running costs 300 + 60',dict(upk=300,upk_line=60)),('running costs 360 + 70',dict(upk=360,upk_line=70)),
     ('running costs 420 + 80',dict(upk=420,upk_line=80)),('240 + 50, over 32 h',dict(_h=32)),('360 + 70, over 32 h',dict(upk=360,upk_line=70,_h=32))]
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
  json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'res_v19.json'),'w'),indent=1)
