# usage: python3 tools/corpsim/run_v14.py  -> 200 galaxies of 16 h per setting (N=, W= to change); writes res_v14.json beside this file
# v14: the market with success-based dividends, the powers' politics (war moves weapon makers) and analysts' ratings.
import json,statistics as st,sys,os,math
from collections import Counter,defaultdict
from multiprocessing import Pool
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from sim14 import sim,D,P as SP
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

  # late volatility (after 4 h), total return with dividends
  late=[]
  for r in R:
    for m in ms:
      h=[x for x in r['mkt'][m] if x[0]%60==0 and x[1]>0 and x[0]>=240]
      late+=[math.log(b1[1]/a1[1]) for a1,b1 in zip(h,h[1:]) if len(a1)>10 and len(b1)>10 and a1[10]==b1[10]]
  o['vol_late']=st.pstdev(late)
  tot=[];divs=[];yields=[]
  for r in R:
    for m in ms:
      mk=r['mkt'][m];s0=at(mk,60);s1=at(mk,16*60-1)
      if not(s0 and s0[1]>0 and len(s0)>10):continue
      g0=s0[10];d0=s0[9];rows=[x for x in mk if x[0]>=60 and len(x)>10 and x[10]==g0]
      dget=(rows[-1][9] if rows else d0)-d0;alive=s1 and len(s1)>10 and s1[10]==g0 and s1[1]>0
      tot.append(((s1[1] if alive else 0)+dget)/s0[1]-1);divs.append(dget/s0[1])
  o['hold_total']=(st.mean(tot),st.median(tot),sum(1 for x in tot if x>0)/len(tot));o['hold_div']=st.mean(divs)
  # dividend payout by success
  dk=defaultdict(list)
  for r in R:
    ranks={}
    for t,m,k in r['div_k']:dk['all'].append(k)
    final=sorted(ms,key=lambda m:-r['rev'][m])
    for t,m,k in r['div_k']:
      if t>=480:dk['top 3 sellers' if m in final[:3] else 'bottom 3 sellers' if m in final[-3:] else 'middle'].append(k)
  o['payout']={k:st.mean(v) for k,v in dk.items()};o['div_total']=st.mean(r['div'] for r in R)
  # politics
  if R[0].get('politics') is not None:
    o['wars']=st.mean(sum(1 for x in r['politics'] if x[2]=='war') for r in R);o['tensions']=st.mean(sum(1 for x in r['politics'] if x[2]=='tension') for r in R)
    o['war_share']={f:st.mean(r['war_min'].get(f,0) for r in R)/960 for f in ('halcyon','varkesh','ostrova')}
    EXP={'bl':1,'mwa':1,'wf':.75,'mg':.67,'cr':.5,'qs':.5,'ad':.33,'hf':.33,'sw':.33,'ewd':0,'tcy':0,'cp':0}
    pe=defaultdict(lambda:([],[]))
    for r in R:
      for t,m,k in r['news']:
        if not k.startswith('pol_'):continue
        grp=('war makers' if EXP[m]>=.67 else 'mixed' if EXP[m]>0 else 'civilian')
        a0=at(r['mkt'][m],t-1);a1=at(r['mkt'][m],t+30);a2=at(r['mkt'][m],t+120)
        if a0 and a1 and a2 and a0[1]>0 and a1[1]>0 and a2[1]>0:pe[(k[4:],grp)][0].append(a1[1]/a0[1]-1);pe[(k[4:],grp)][1].append(a2[1]/a0[1]-1)
    o['pol_news']={f'{k[0]} / {k[1]}':(st.mean(v[0])-o['drift'][0],st.mean(v[1])-o['drift'][1],len(v[0])/N) for k,v in pe.items()}
    # earnings of war makers vs civilian makers, by how many pairs are at war
    ew=defaultdict(list)
    for r in R:
      pol=sorted(r['politics']);
      def nwar(t):
        rel={}
        for tt,p,v in pol:
          if tt>t:break
          rel[p]=v
        return sum(1 for v in rel.values() if v=='war')
      for m in ms:
        for x in r['mkt'][m]:
          if x[0]>=240 and x[0]%30==0 and x[1]>0:ew[('war makers' if EXP[m]>=.67 else 'civilian' if EXP[m]==0 else 'mixed',min(2,nwar(x[0])))].append(x[4])
    o['earn_by_war']={f'{k[0]} / {k[1]} wars':st.mean(v) for k,v in sorted(ew.items())}
  # analysts' ratings
  if R[0].get('ratings'):
    o['rating_mix']={k:v/sum(1 for r in R for x in r['ratings']) for k,v in Counter(x[2] for r in R for x in r['ratings']).items()}
    rs=defaultdict(list)
    for r in R:
      for t,m,rt,gen in r['ratings']:
        a0=at(r['mkt'][m],t);a2=at(r['mkt'][m],t+120)
        if a0 and a2 and a0[1]>0 and len(a0)>10 and len(a2)>10 and a2[10]==a0[10] and t+120<960:rs[rt].append(a2[1]/a0[1]-1)
        elif a0 and a0[1]>0 and t+120<960:rs[rt].append(-1)
    o['rating_next2h']={k:(st.mean(v)-o['drift'][1],sum(1 for x in v if x>0)/len(v),len(v)/N) for k,v in sorted(rs.items())}
    # follow the rating: buy on strong buy, sell when it drops to hold or worse (or after 4 h)
    tr=[]
    for r in R:
      by=defaultdict(list)
      for t,m,rt,gen in r['ratings']:by[m].append((t,rt,gen))
      for m,L in by.items():
        i=0
        while i<len(L):
          t,rt,gen=L[i]
          if rt==2:
            j=i+1
            while j<len(L) and L[j][1]>0 and L[j][0]<t+240 and L[j][2]==gen:j+=1
            t1=L[j][0] if j<len(L) else 959;a0=at(r['mkt'][m],t);a1=at(r['mkt'][m],t1)
            ok=a1 and len(a1)>10 and a1[10]==gen and a1[1]>0
            tr.append(((a1[1]/a0[1]-1) if ok else -1,(t1-t)));i=j+1
          else:i+=1
    o['follow_rating']=(st.mean(x[0] for x in tr),sum(1 for x in tr if x[0]>0)/len(tr),len(tr)/N,st.mean(x[1] for x in tr)/60) if tr else None
  return name,o
V=[('v14',{}),('v14 without politics',{'politics':False}),('v14 with a flat 40% payout',{'div_lo':.4,'div_hi':.4}),('v13 settings',{'politics':False,'div_lo':.4,'div_hi':.4,'g_a':1.0})]
if __name__=='__main__':
  res={}
  with Pool(int(os.environ.get('W',2))) as p:
    for n,o in p.imap(one,V):res[n]=o;print(n,'done',flush=True)
  json.dump(res,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'res_v14.json'),'w'),default=str)
