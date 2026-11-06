# usage: python3 tools/corpsim/run_v17.py  -> 200 galaxies of 16 h per setting (N=, W=); writes res_v17.json
# v17: buyers weigh price against quality by how much money they have, and a launch keeps the old grade on the market
# (as clearance stock or as the maker's budget line). Who buys what, what it does to R&D, failures and who leads.
import sys,os,json,statistics as st
from collections import defaultdict,Counter
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from sim17 import sim,D,P as SP
from multiprocessing import Pool
N=int(os.environ.get('N',200))
def one_g(a):
  seed,p=a;p=dict(p);p['log']=True;r=sim(seed,p)
  o=dict(fail=len(r['failures']),launches=len(r['launches']),grade3=any(x[3]>=3 for x in r['launches']),grade4=any(x[3]>=4 for x in r['launches']),
         tweaks=r['tweaks'],std=r['faction_std'],sales=r['sales'],ore=r['ore_units'],buy=r.get('buy_cls',{}),old=len(r.get('old_lines',[])))
  o['rev']=sum(r['rev'].values());o['profit']=sum(net-c*ck for t,m,net,ck,c,k in r['log'])
  # who leads a kind for a 2-hour spell, and with which grade against its best rival
  L=sorted(r['launches'])
  def grade(m,k,t):
    g=1
    for tt,mm,kk,gg,_ in L:
      if tt>t:break
      if mm==m and kk==k:g=gg
    return g
  blocks=defaultdict(Counter)
  for t,m,net,ck,c,k in r['log']:
    if t>=240:blocks[(k,(t-240)//120)][m]+=1
  lead=Counter()
  for (k,b),c in blocks.items():
    n=sum(c.values())
    if n<8 or len(c)<2:continue
    m,top=c.most_common(1)[0]
    if top/n<.6:lead['even']+=1;continue
    t=240+b*120+60;gl=grade(m,k,t);go=max(grade(mm,k,t) for mm in c if mm!=m)
    lead['lower' if gl<go else 'same' if gl==go else 'higher']+=1
  o['lead']=lead
  return o
def one(v):
  name,p=v
  with Pool(int(os.environ.get('W',2))) as pool:R=pool.map(one_g,[(s,p) for s in range(N)])
  o={k:st.mean(r[k] for r in R) for k in ('fail','launches','tweaks','std','sales','ore','rev','profit','old')}
  o['grade3']=sum(r['grade3'] for r in R)/N;o['grade4']=sum(r['grade4'] for r in R)/N;o['nofail']=sum(1 for r in R if r['fail']==0)/N
  lead=Counter()
  for r in R:lead.update(r['lead'])
  n=sum(lead.values());o['lead']={k:v/n for k,v in lead.items()}
  b=defaultdict(Counter)
  for r in R:
    for c,d in r['buy'].items():b[c].update(d)
  o['buy']={c:{k:v/sum(d.values()) for k,v in d.items()} for c,d in b.items()};o['buy_n']={c:sum(d.values())/N for c,d in b.items()}
  return name,o
V=[('v17 (budget line)',{}),('v16 rules',{'price_sens':False,'old':'off'}),('price-minded buyers only',{'old':'off'}),('price-minded buyers + clearance',{'old':'clear'}),('budget line, no price-minded buyers',{'price_sens':False})]
if __name__=='__main__':
  res={}
  for v in V:
    n,o=one(v);res[n]=o;print(n,json.dumps({k:(round(x,3) if isinstance(x,float) else ({a:round(b,3) if isinstance(b,float) else b for a,b in x.items()} if isinstance(x,dict) and k!='buy' else x)) for k,x in o.items() if k!='buy'}),flush=True)
    for c,d in o['buy'].items():print('   ',c,{k:round(x,3) for k,x in sorted(d.items())})
  json.dump(res,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'res_v17.json'),'w'),indent=1)
