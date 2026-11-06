# usage: python3 tools/corpsim/run_v13.py  -> 200 galaxies of 16 h per setting; writes res_v13.json beside this file
# The stock market: what moves share prices, how news lands, and how simple trading strategies fare.
import json,statistics as st,sys,os,math
from collections import Counter,defaultdict
from multiprocessing import Pool
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from sim13 import sim,D
N=int(os.environ.get('N',200))
def pct(v,q):v=sorted(v);return v[min(len(v)-1,int(q*len(v)))] if v else 0
def at(mk,t):
  v=None
  for x in mk:
    if x[0]<=t:v=x
    else:break
  return v
def one(a):
  name,p=a;R=[sim(s,p) for s in range(N)];ms=list(D['makers'])
  o=dict(name=name)
  o['fail']=st.mean(len(r['failures']) for r in R);o['nofail']=sum(1 for r in R if not r['failures'])/N
  o['failby']=Counter(D['makers'][x[1]]['name'] for r in R for x in r['failures']).most_common()
  o['launches']=st.mean(len(r['launches']) for r in R);o['first_launch_h']=st.median([r['launches'][0][0]/60 for r in R if r['launches']] or [0])
  o['ceo_changes']=st.mean(len(r['ceo_changes']) for r in R);o['ceo_why']=Counter(c[4] for r in R for c in r['ceo_changes'])
  o['issues']=st.mean(len(r['issues']) for r in R);o['issued_shares']=st.mean(sum(x[2] for x in r['issues']) for r in R)
  o['top']=Counter(D['makers'][max(ms,key=lambda m:r['rev'][m])]['name'] for r in R).most_common()
  rets=[];dev=[];comp=defaultdict(list);endP=[];endE=[];endB=[]
  for r in R:
    for m in ms:
      mk=r['mkt'][m];h=[x for x in mk if x[0]%60==0 and x[1]>0]
      for a1,b1 in zip(h,h[1:]):
        rets.append(math.log(b1[1]/a1[1]))
        P0=a1[1];ea=a1[2]-a1[3]-a1[6]-a1[7];eb=b1[2]-b1[3]-b1[6]-b1[7]
        comp['book'].append(abs(b1[3]-a1[3])/P0);comp['earnings'].append(abs(eb-ea)/P0);comp['pipeline'].append(abs(b1[6]-a1[6])/P0);comp['dividends'].append(abs(b1[7]-a1[7])/P0)
      dev+=[abs(x[1]-x[2])/x[2] for x in mk if x[2]>0 and x[0]>60]
      e=at(mk,16*60-1)
      if e and e[1]>0:endP.append(e[1]);endE.append(e[4]);endB.append(e[3])
  o['vol_h']=st.pstdev(rets);o['dev']=st.mean(dev);o['moves']={k:st.mean(v) for k,v in comp.items()}
  def corr(x,y):
    mx,my=st.mean(x),st.mean(y);sx,sy=st.pstdev(x),st.pstdev(y);return sum((a-mx)*(b-my) for a,b in zip(x,y))/len(x)/sx/sy
  o['corr_P_E']=corr(endP,endE);o['corr_P_book']=corr(endP,endB)
  # what the value is made of, at 8 h and 16 h (median share of value)
  mix={}
  for T in (8,16):
    parts=defaultdict(list)
    for r in R:
      for m in ms:
        x=at(r['mkt'][m],T*60-1)
        if not x or x[2]<=0:continue
        earn=x[2]-x[3]-x[6]-x[7];parts['book'].append(x[3]/x[2]);parts['earnings and growth'].append(earn/x[2]);parts['pipeline'].append(x[6]/x[2]);parts['dividends'].append(x[7]/x[2])
    mix[T]={k:st.mean(v) for k,v in parts.items()}
  o['mix']=mix
  # how news lands: price change from just before to 30 and 120 minutes after
  ev=defaultdict(lambda:([],[]))
  for r in R:
    for t,m,k in r['news']:
      a0=at(r['mkt'][m],t-1);a1=at(r['mkt'][m],t+30);a2=at(r['mkt'][m],t+120)
      if a0 and a1 and a2 and a0[1]>0 and a1[1]>0 and a2[1]>0:ev[k][0].append(a1[1]/a0[1]-1);ev[k][1].append(a2[1]/a0[1]-1)
  # the usual drift over 30 and 120 minutes at any moment, to tell news from the general rise
  b30=[];b120=[]
  for r in R:
    for m in ms:
      mk=r['mkt'][m];byt={x[0]:x[1] for x in mk}
      for x in mk:
        if x[0]>=60 and x[0]%15==0 and x[1]>0 and byt.get(x[0]+30,0)>0 and byt.get(x[0]+120,0)>0:b30.append(byt[x[0]+30]/x[1]-1);b120.append(byt[x[0]+120]/x[1]-1)
  o['drift']=(st.mean(b30),st.mean(b120))
  o['news']={k:(st.mean(v[0]),st.mean(v[1]),len(v[0])/N,st.mean(v[0])-o['drift'][0],st.mean(v[1])-o['drift'][1]) for k,v in ev.items()}
  # simple trading strategies (price only; a failure loses the stake)
  strat=defaultdict(list)
  for r in R:
    for m in ms:
      mk=r['mkt'][m];h=[x for x in mk if x[0]%5==0]
      s0=at(mk,60);s1=at(mk,16*60-1)
      if s0 and s0[1]>0:strat['buy at 1 h, hold to 16 h'].append((s1[1] if s1 else 0)/s0[1]-1)
      # buy when the price is 20% under value, sell when it reaches value (or after 3 h)
      i=12
      while i<len(h)-1:
        x=h[i]
        if x[1]>0 and x[2]>0 and x[1]<.8*x[2]:
          j=i+1
          while j<len(h) and h[j][0]<x[0]+180 and not (h[j][1]>=h[j][2] or h[j][1]==0):j+=1
          j=min(j,len(h)-1);strat['buy 20% under value, sell at value'].append(h[j][1]/x[1]-1);i=j+1
        else:i+=1
    for t,m,k in r['news']:
      if k=='launch':
        a0=at(r['mkt'][m],t);a2=at(r['mkt'][m],t+120)
        if a0 and a2 and a0[1]>0:strat['buy on a launch, sell 2 h later'].append(a2[1]/a0[1]-1)
      if k=='ceo':
        a0=at(r['mkt'][m],t);a2=at(r['mkt'][m],t+120)
        if a0 and a2 and a0[1]>0:strat['buy on a new CEO, sell 2 h later'].append(a2[1]/a0[1]-1)
  o['strat']={k:(st.mean(v),st.median(v),sum(1 for x in v if x>0)/len(v),len(v)/N) for k,v in strat.items()}
  return name,o
V=[('v13',{}),('v13 first try (slow earnings, no listing)',{'debias':False,'listing':-1}),('v13 with share issues for R&D',{'issue':True}),('v13 without news shocks',{'news':{'launch':0,'project':0,'sabotaged':0,'spied':0,'tweak':0,'ceo':0}}),('v13 book value only (v12 style)',{'kappa':1.0,'mu':0,'sigma':0,'mkt_H':0,'pipe_k':0,'div_H':0,'news':{'launch':0,'project':0,'sabotaged':0,'spied':0,'tweak':0,'ceo':0}})]
if __name__=='__main__':
  res={}
  with Pool(int(os.environ.get('W',2))) as p:
    for n,o in p.imap(one,V):res[n]=o;print(n,'done',flush=True)
  json.dump(res,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'res_v13.json'),'w'),default=str)
