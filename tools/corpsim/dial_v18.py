# v18 with a small cash cushion: how many failures each setting gives (the user's "go broke or go home" dial)
import os,json
from run_v18 import one,N
from multiprocessing import Pool
import statistics as stt
from collections import Counter
SET=[('v18, R&D needs 1 h of costs spare, stock none',dict(rd_reserve=1)),('v18, 0.5 h reserve',dict(reserve=.5,rd_reserve=.5)),('v18, 1 h reserve',dict(reserve=1,rd_reserve=1)),('v18, 2 h reserve',dict(reserve=2,rd_reserve=2)),('v18 over 32 h',dict(_h=32))]
if __name__=='__main__':
  with Pool(2) as pool:
    for name,p in SET:
      R=pool.map(one,[(18,i,p) for i in range(N)])
      f=[x['fail'] for x in R];who=Counter(w for x in R for w in x['who'])
      print(name,dict(fail=round(stt.mean(f),2),none=round(sum(1 for x in f if x==0)/N*100),g3=round(sum(x['g3'] for x in R)/N*100),launches=round(stt.mean(x['launches'] for x in R),1),first=round(stt.median([t for x in R for t in x['at']])/60,1) if any(x['at'] for x in R) else None),dict(who.most_common(5)),flush=True)
