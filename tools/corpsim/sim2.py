# Corporations model v2 (user, 5 Nov 2026): every upgradable system is a part; every maker part trades a strength for a
# weakness that makes sense for that kind of part (standard parts stay at zero); parts sell at a profit after the station's cut
# and fees; supply and demand move the price of parts people want; a part people don't like gets up to 3 tweaks, then is
# replaced by a new product and its unsold stock is broken back into raw ore. One step = 1 minute.
import json,math,random,zlib
H=__file__.rsplit('/',1)[0]
D=json.load(open(H+'/data.json'));D2=json.load(open(H+'/data2.json'))
HOME_SID={'halcyon':'hp','varkesh':'vb','ostrova':'os','mw':'mw','cw':'cw','ew':'ew'}
FREEPORTS=['mw','cw','ew'];POWERS=['halcyon','varkesh','ostrova']
# ---- what each kind of part can be good at, and what it costs (key, sign): +1 = the stat goes up (a cost stat such as power
# draw), -1 = a good stat goes down
KINDS={
 'engine':{'name':'Drive','good':['speed','turn'],'weak':[('e',1),('hp',-1)]},
 'power':{'name':'Reactor','good':['en','enr'],'weak':[('speed',-1),('sig',1)]},
 'shield':{'name':'Shield emitter','good':['sh','shr'],'weak':[('shr',-1),('e',1)]},
 'armor':{'name':'Armor','good':['hp'],'weak':[('speed',-1),('turn',-1)]},
 'weapon':{'name':'Fire control','good':['dmg','track'],'weak':[('e',1),('sig',1)]},
 'drill':{'name':'Blast rig','good':['ml'],'weak':[('e',1),('speed',-1)]},
 'hold':{'name':'Cargo hold','good':['cargo'],'weak':[('speed',-1),('turn',-1)]},
 'gun':{'name':'Machine gun','good':['dmg','ammo'],'weak':[('ammo',-1),('e',1),('dmg',-1)]},
 'laser':{'name':'Laser','good':['dmg','range'],'weak':[('e',1),('dmg',-1)]},
 'missile':{'name':'Missile launcher','good':['dmg','mag'],'weak':[('lock',1),('mag',-1)]},
 'torpedo':{'name':'Torpedo launcher','good':['dmg','mag'],'weak':[('lock',1),('mag',-1)]},
 'mlaser':{'name':'Mining laser','good':['ml'],'weak':[('e',1),('range',-1)]},
 'charge':{'name':'Charge launcher','good':['ml','mag'],'weak':[('mag',-1),('ml',-1),('e',1)]},
 'scanner':{'name':'Scanner','good':['scan'],'weak':[('e',1),('sig',1)]},
 'dronec':{'name':'Drone controller','good':['dh','dd'],'weak':[('dh',-1),('dd',-1),('e',1)]},
 'cargo':{'name':'Cargo module','good':['cargo'],'weak':[('speed',-1),('turn',-1)]},
 'land':{'name':'Landing kit','good':['stealth'],'weak':[('boot',1)]},
 'bdev':{'name':'Beacon rig','good':['mag'],'weak':[('speed',-1),('sig',1)]},
 'lrack':{'name':'Limpet rack','good':['mag'],'weak':[('speed',-1),('sig',1)]},
 'hide':{'name':'Hidden container','good':['stealth'],'weak':[('cargo',-1)]},
 'jammer':{'name':'Jammer','good':['jam'],'weak':[('e',1),('sig',1)]},
 'hook':{'name':'Cargo hook','good':['tow'],'weak':[('e',1),('sig',1)]},
 'cscan':{'name':'Cargo scanner','good':['scan'],'weak':[('e',1),('sig',1)]}}
SYSTEMS=['engine','power','shield','weapon','armor','drill','hold']
COST_KEYS={'e','lock','sig','boot'}
# what a +100% on each stat is worth to a buyer of each role (mag: per unit)
ROLE_W={'fighter':{'dmg':1,'sh':.8,'shr':.5,'hp':.8,'en':.5,'enr':.4,'speed':.5,'turn':.5,'track':.5,'range':.3,'ammo':.4,'mag':.08,'e':-.6,'lock':-.4,'sig':-.2,'boot':-.1,'stealth':.2,'jam':.2,'scan':.1},
 'hauler':{'cargo':1,'speed':.8,'turn':.2,'sh':.6,'shr':.3,'hp':.6,'en':.2,'enr':.2,'dh':.6,'dd':.4,'stealth':.4,'dmg':.15,'e':-.1,'sig':-.4,'boot':-.1,'tow':.3,'ammo':.1,'range':.1},
 'miner':{'ml':1,'cargo':.6,'dh':.5,'dd':.35,'sh':.4,'shr':.2,'hp':.4,'en':.4,'enr':.4,'mag':.06,'scan':.2,'range':.3,'speed':.2,'turn':.1,'e':-.5,'sig':-.2,'boot':-.1,'dmg':.1},
 'scout':{'scan':1,'speed':.8,'stealth':.6,'turn':.4,'sh':.4,'en':.3,'mag':.05,'dmg':.2,'jam':.3,'e':-.2,'sig':-.6,'boot':-.2,'hp':.2,'range':.2}}
ROLE_CLS={'fighter':['interceptor','striker','heavy','bomber','gunboat'],'hauler':['courier','freighter','bulker'],'miner':['skiff','prospector','dredger'],'scout':['scout','scout2']}
MINING={'skiff','prospector','dredger'}
def role_slots(role):
  out=[]
  for c in ROLE_CLS[role]:
    s=D['slots'].get(c)
    if s:out+=s['w']+s['u']+['engine','power','shield','weapon','armor','hold']+(['drill'] if c in MINING else [])
  return out
RSLOTS={r:role_slots(r) for r in ROLE_W}
KIND_ROLES={k:{r:RSLOTS[r].count(k)/len(RSLOTS[r]) for r in ROLE_W if k in RSLOTS[r]} for k in KINDS}
# ---- the trade-off rule: points (mag 1 = 10 points); a part's weakness is at least half its strength; no stat past +25% (mag +2)
PT=lambda k,v:abs(v)*(10 if k=='mag' else 100)
def strength(tr):return sum(PT(k,v) for k,v in tr.items() if (k not in COST_KEYS and v>0) or (k in COST_KEYS and v<0))
def weakness(tr):return sum(PT(k,v) for k,v in tr.items() if (k not in COST_KEYS and v<0) or (k in COST_KEYS and v>0))
def to_val(k,pts):return pts/(10 if k=='mag' else 100)
def rnd2(v,k):return round(v) if k=='mag' else round(v,3)
def fix_tradeoff(kind,tr,rng=None):
  """make a set of traits obey the rule: weakness >= half the strength, on a sensible weakness for the kind"""
  tr={k:v for k,v in tr.items() if v}
  s,w=strength(tr),weakness(tr)
  if w>=s/2-1e-9:return tr
  need=s/2-w+.1
  cur=[k for k,v in tr.items() if (k not in COST_KEYS and v<0) or (k in COST_KEYS and v>0)]
  opts=[(k,sg) for k,sg in KINDS[kind]['weak'] if not (k in tr and ((tr[k]>0)!=(sg>0)))]
  k,sg=(next(((k,sg) for k,sg in opts if k in cur),None) or (opts[0] if not rng else rng.choice(opts)))
  if k=='mag':need=max(10,math.ceil(need/10)*10)
  tr[k]=rnd2(tr.get(k,0)+sg*to_val(k,need),k);return tr
def value(tr,role):
  W=ROLE_W[role];return sum(W.get(k,0)*v for k,v in tr.items())
def appeal(kind,tr):
  R=KIND_ROLES[kind];t=sum(R.values()) or 1
  return sum(w*value(tr,r) for r,w in R.items())/t
def new_traits(kind,rng):
  """a new product: one strength (two now and then), 6 to 14 points, paid for with a weakness of at least half"""
  K=KINDS[kind];g=list(K['good']);rng.shuffle(g);n=2 if len(g)>1 and rng.random()<.3 else 1;tot=rng.uniform(6,14);tr={}
  for i,k in enumerate(g[:n]):
    pts=tot/n
    if k=='mag':pts=10
    tr[k]=rnd2(to_val(k,pts),k)
  opts=[(k,sg) for k,sg in K['weak'] if k not in tr];k,sg=rng.choice(opts)
  w=strength(tr)*rng.uniform(.5,.75)+.1;w=max(10,math.ceil(w/10)*10) if k=='mag' else w
  tr[k]=rnd2(sg*to_val(k,w),k);return fix_tradeoff(kind,tr)
# ---- the makers' system lines (a trait line each; standard lines from one maker per system)
SYS_LINES={'ewd':['engine','power'],'qs':['armor','hold'],'hf':['armor','drill'],'tcy':['hold','engine'],'bl':['shield','weapon'],'ad':['power','shield'],
           'mg':['weapon','armor'],'sw':['power'],'cp':['drill'],'cr':['shield','engine'],'mwa':['weapon']}
SYS_STD={'ewd':['engine'],'ad':['power','shield'],'mg':['weapon'],'qs':['armor','hold'],'hf':['drill']}
SYSK={'engine':'engine','power':'power','shield':'shield','weapon':'weapon','armor':'armor','drill':'drill','hold':'cargo'}
def catalogue():
  items={}
  for id,it in D['items'].items():
    if not it['maker'] or it['part']=='claim':continue
    tr=dict(it['tr']);items[id]=dict(name=it['name'],part=it['part'],maker=it['maker'],tr0=tr,tr=fix_tradeoff(it['part'],tr) if tr else {},base=it['base'],comp=it['comp'],ore=D2['items'][id]['oreVal'],oret=sum(D2['items'][id]['ore'].values()))
  for m,ks in list(SYS_LINES.items())+[('std:'+m,ks) for m,ks in SYS_STD.items()]:
    std=m.startswith('std:');m=m.replace('std:','')
    for k in ks:
      g=D2['sys'][SYSK[k]]['g']['2'];id=('msq_' if std else 'ms_')+m+'_'+k
      tr={} if std else new_traits(k,random.Random(zlib.crc32(id.encode())))
      items[id]=dict(name=D['makers'][m]['name'].split()[0]+(' standard ' if std else ' ')+KINDS[k]['name'].lower(),part=k,maker=m,tr0={},tr=tr,base=round(g['cv']*1.11),comp=g['cv'],ore=g['oreVal'],oret=sum(g['ore'].values()))
  return items
CAT=catalogue()
P=dict(start=3000,upk=80,upk_line=20,dues=.15,markup=1.5,min_margin=.15,review=20,div=.4,shares=100,home_share=60,
       refit_per_h=12,refit_parts=1.5,contractor_per_h=20,merchant_per_h=16,player_per_h=2,
       beta=8.0,loyal=.06,works_every=1.5,cap=4,struggle_h=2,replace=(30,60),reserve=3,retire=120,
       tweak_pts=(2,4),cap_bonus=.25,cap_mag=2,max_tweaks=3,dislike=.5,dislike_min=1.5,window=120,settle=60,launch=300,
       up=1.06,down=.97,pm_max=1.6,craze_sellouts=3,craze_len=40,craze_k=1.5,spike_every=45,spike_len=30,spike_k=2.0,
       refits=True,hours=16,systems=True,want=1.0,down_floor='profit',hot=1.5)
class Line:
  def __init__(s,id,it):
    s.id=id;s.kind=it['part'];s.tr=dict(it['tr']);s.trs=[dict(it['tr'])];s.base=it['base'];s.comp=it['comp'];s.ore=it['ore'];s.oret=it['oret'];s.name=it['name']
    s.std=not it['tr'];s.pm=1.0;s.stock=2;s.sold=[];s.ev=[];s.tweaks=0;s.last_tw=-999;s.sellouts=[];s.craze=0;s.active=True;s.gen=1;s.minst=2;s.sellout_rev=False;s.margins=[]
  def price(s):return s.base*P['markup']*s.pm
  def floor(s):return (1+P['min_margin'])*s.comp/((1-P['dues'])*s.base*P['markup'])
class Maker:
  def __init__(s,m,rng,new=False):
    s.m=m;s.name=D['makers'][m]['name'];s.home=D['makers'][m]['home'];s.sid=HOME_SID[s.home];s.T=P['start'];s.alive=True;s.struggling=False
    s.lines=[Line(id,it) for id,it in CAT.items() if it['maker']==m and (P['systems'] or it['part'] not in SYSTEMS)]
    if new:
      for L in s.lines:
        if not L.std:L.tr=new_traits(L.kind,rng);L.trs=[dict(L.tr)]
    s.share_px=[];s.div_paid=0;s.hist=[];s.born=0;s.rev=0;s.rev_sys=0
  def upkeep_h(s):return P['upk']+P['upk_line']*sum(1 for L in s.lines if L.active)
def sim(seed,params=None):
  global P
  P0=P;P=dict(P0,**(params or {}));rng=random.Random(seed)
  try:
    makers={m:Maker(m,rng) for m in D['makers']}
    station={k:0.0 for k in ['halcyon','varkesh','ostrova','neutral']}
    owner_of=lambda sid:{'hp':'halcyon','vb':'varkesh','os':'ostrova'}.get(sid,'neutral')
    st=dict(failures=[],replacements=[],tweaks=0,tk={},crazes=0,spikes=0,div=0,ore_t=0.0,ore_cr=0.0,ore_units=0,launch=0,sales=0,sales_sys=0,sales_std=0,min_margin=9,price_up=0,price_down=0)
    spike=[];boost_t=[]
    def buy(role,where,kind=None,mult=1.0):
      k=kind or rng.choice(RSLOTS[role])
      if k=='drill' and role!='miner':return
      if not P['systems'] and k in SYSTEMS:return
      cands=[(mk,L) for mk in makers.values() if mk.alive and (where is None or mk.sid in where) for L in mk.lines if L.kind==k and L.stock>0 and L.active]
      if not cands:return
      xs=[]
      for mk,L in cands:
        x=(1+value(L.tr,role))/L.pm+(P['loyal'] if where and mk.sid==where[0] else 0)
        if L.craze>0:x*=P['craze_k']
        xs.append(P['beta']*x)
      mx=max(xs);sc=[math.exp(v-mx) for v in xs];t=sum(sc);r=rng.random()*t;i=0
      while r>sc[i]:r-=sc[i];i+=1
      n=len(cands)
      for j,(mk2,L2) in enumerate(cands):L2.ev.append((now,1/n,j==i))
      mk,L=cands[i];pr=L.price()*mult;L.stock-=1;L.sold.append(now);net=pr*(1-P['dues']);mk.T+=net;mk.rev+=net;station[owner_of(mk.sid)]+=pr*P['dues']
      m=net/L.comp-1;L.margins.append(m);st['min_margin']=min(st['min_margin'],m);st['sales']+=1
      if L.kind in SYSTEMS:st['sales_sys']+=1;mk.rev_sys+=net
      if L.std:st['sales_std']+=1
      if L.stock==0:L.sellouts.append(now);L.sellout_rev=True
      L.minst=min(L.minst,L.stock)
    def poisson(rate):
      n=0;l=math.exp(-rate);p=rng.random()
      while p>l:n+=1;p*=rng.random()
      return n
    def disliked(L):
      E=[e for e in L.ev if e[0]>now-P['window']]
      exp=sum(e[1] for e in E);got=sum(1 for e in E if e[2])
      return exp>=P['dislike_min'] and got<P['dislike']*exp
    def share(L):
      E=[e for e in L.ev if e[0]>now-P['window']];exp=sum(e[1] for e in E);got=sum(1 for e in E if e[2]);return got,exp
    def wanted(L):
      got,exp=share(L);return any(t>now-60 for t in L.sold) and got>=P['want']*exp
    def tweak(L):
      opts=[];a0=appeal(L.kind,L.tr);K=KINDS[L.kind]
      cur_w=[k for k,v in L.tr.items() if (k not in COST_KEYS and v<0) or (k in COST_KEYS and v>0)]
      for g in K['good']:
        if g in L.tr and L.tr[g]<0:continue
        d=10 if g=='mag' else rng.uniform(*P['tweak_pts'])
        t=dict(L.tr);capv=P['cap_mag'] if g=='mag' else P['cap_bonus'];nv=min(capv,t.get(g,0)+to_val(g,d))
        if nv<=t.get(g,0)+1e-9:continue
        t[g]=rnd2(nv,g)
        for wk,sg in K['weak']:
          if wk==g:continue
          # put the extra weakness on this cost stat
          need=strength(t)/2-weakness(t)+.1
          t3=dict(t)
          if need>0:
            add=max(10,math.ceil(need/10)*10) if wk=='mag' else need
            if wk in t3 and ((t3[wk]>0)!=(sg>0)):continue
            t3[wk]=rnd2(t3.get(wk,0)+sg*to_val(wk,add),wk)
          opts.append((appeal(L.kind,t3),('boost',t3)))
      # move the whole weakness onto another cost stat
      if cur_w:
        wp=weakness(L.tr)
        for wk,sg in K['weak']:
          if wk in cur_w or (wk in L.tr and ((L.tr[wk]>0)!=(sg>0))):continue
          t={k:v for k,v in L.tr.items() if k not in cur_w};add=max(10,math.ceil(wp/10)*10) if wk=='mag' else wp
          t[wk]=rnd2(sg*to_val(wk,add),wk);opts.append((appeal(L.kind,t),('move',t)))
      if not opts:return None
      opts.sort(key=lambda x:-x[0]);kind,t=opts[0][1];L.tr=t;L.trs.append(dict(t));return kind
    for now in range(int(P['hours']*60)):
      # works build stock, keeping a reserve
      if now%max(1,int(P['works_every']))==0:
        for mk in makers.values():
          if not mk.alive:continue
          ls=[L for L in mk.lines if L.active and L.stock<P['cap']]
          if not ls:continue
          L=min(ls,key=lambda L:L.stock)
          if mk.T-L.comp<P['reserve']*mk.upkeep_h():continue
          mk.T-=L.comp;station[owner_of(mk.sid)]+=L.comp;L.stock+=1
      for mk in makers.values():
        if mk.alive:mk.T-=mk.upkeep_h()/60
      if P['refits']:
        for f in POWERS:
          for _ in range(poisson(P['refit_per_h']*P['refit_parts']/60)):buy('fighter',[HOME_SID[f]]+FREEPORTS)
      for _ in range(poisson(P['contractor_per_h']/60)):
        role=rng.choices(['fighter','hauler','miner','scout'],[.4,.3,.25,.05])[0];buy(role,rng.choice([[s] for s in FREEPORTS+['hp','vb','os']]))
      for _ in range(poisson(P['merchant_per_h']/60)):
        role=rng.choices(['fighter','hauler','miner','scout'],[.45,.3,.2,.05])[0];buy(role,None)
      for _ in range(poisson(P['player_per_h']/60)):buy(rng.choice(['fighter','hauler','miner']),None)
      # demand spikes: a kind of part badly wanted somewhere for a while
      if rng.random()<1/P['spike_every']:
        k=rng.choice(list(KINDS));spike.append((k,now+P['spike_len']));st['spikes']+=1
        for mk in makers.values():
          for L in mk.lines:
            if L.kind==k and not L.active and mk.alive:L.active=True
      spike=[s for s in spike if s[1]>now]
      for k,_ in spike:
        for _ in range(poisson(10/60/max(1,len(spike)))):buy(rng.choice([r for r in KIND_ROLES[k]] or ['fighter']),None,kind=k,mult=P['spike_k'])
      for mk in makers.values():
        for L in mk.lines:
          if L.craze>0:L.craze-=1
          elif len([t for t in L.sellouts if t>now-60])>=P['craze_sellouts']:L.craze=P['craze_len'];st['crazes']+=1;L.sellouts=[]
      # the review: prices, tweaks, replacements, idle lines, dividends
      if now%P['review']==0 and now>0:
        for mk in makers.values():
          if not mk.alive:continue
          prof=mk.T-(mk.hist[-1] if mk.hist else P['start']);mk.hist.append(mk.T)
          for L in mk.lines:
            L.ev=[e for e in L.ev if e[0]>now-P['window']]
            if not L.active:continue
            got,exp=share(L)
            if any(t>now-60 for t in L.sold) and not disliked(L):
              # supply and demand, for parts people want: bought more than its share (or sold out) -> dearer; less than its
              # share with full shelves -> cheaper, never below a profit after the station's cut and fees
              fl=L.floor() if P['down_floor']=='profit' else 1.0
              if L.sellout_rev or (exp>=1 and got>=P['hot']*exp):L.pm=min(P['pm_max'],L.pm*P['up']);st['price_up']+=1
              elif got<exp and L.minst>=P['cap']-1 and L.pm>fl+1e-9:L.pm=max(fl,L.pm*P['down']);st['price_down']+=1
            elif not L.std and disliked(L) and now-L.last_tw>=P['settle']:
              if L.tweaks<P['max_tweaks']:
                k=tweak(L)
                if k:L.tweaks+=1;L.last_tw=now;st['tweaks']+=1;st['tk'][k]=st['tk'].get(k,0)+1;L.ev=[]
              else:
                # a new product: the old one's stock is broken back into raw ore (sold to the station)
                st['ore_units']+=L.stock;st['ore_t']+=L.stock*L.oret;st['ore_cr']+=L.stock*L.ore;mk.T+=L.stock*L.ore
                st['replacements'].append((now,mk.m,L.id,L.kind,L.gen,dict(L.tr)))
                L.stock=0;L.tr=new_traits(L.kind,rng);L.trs.append(dict(L.tr));L.tweaks=0;L.gen+=1;L.last_tw=now;L.ev=[];L.pm=1.0;L.sold=[]
                mk.T-=P['launch'];st['launch']+=P['launch']
            L.sellout_rev=False;L.minst=L.stock
            if P['retire'] and L.active and now>P['retire'] and not [t for t in L.sold if t>now-P['retire']] and L.stock>=P['cap']:L.active=False
          mk.struggling=mk.T<P['struggle_h']*mk.upkeep_h()
          if prof>0 and not mk.struggling:
            d=prof*P['div'];mk.T-=d;mk.div_paid+=d;st['div']+=d
          mk.share_px.append((now,max(1,mk.T/P['shares'])))
      for m,mk in list(makers.items()):
        if mk.alive and mk.T<=0:
          mk.alive=False;st['failures'].append((now,m,mk.name));mk.rebirth=now+rng.randint(*P['replace'])
        if not mk.alive and now>=getattr(mk,'rebirth',1e9):
          nm=Maker(m,rng,new=True);nm.born=now;makers[m]=nm
      if now%60==0:
        tl=[L for mk in makers.values() for L in mk.lines if not L.std]
        boost_t.append((now,max(max([PT(k,v) for k,v in L.tr.items() if k!='mag' and ((k not in COST_KEYS and v>0) or (k in COST_KEYS and v<0))]+[0]) for L in tl),
                        sum(strength(L.tr)-weakness(L.tr) for L in tl)/len(tl)))
    lines=[(mk.m,L.id,L.kind,L.std,L.tweaks,L.gen,L.tr,round(L.pm,3),len(L.sold),L.trs,L.active) for mk in makers.values() for L in mk.lines]
    return dict(st,T={m:round(mk.T) for m,mk in makers.items()},struggling={m:mk.struggling for m,mk in makers.items()},
                divm={m:round(mk.div_paid) for m,mk in makers.items()},rev={m:round(mk.rev) for m,mk in makers.items()},rev_sys={m:round(mk.rev_sys) for m,mk in makers.items()},
                px={m:mk.share_px for m,mk in makers.items()},lines=lines,boost_t=boost_t)
  finally:
    P=P0
if __name__=='__main__':
  import time;t=time.time();r=sim(1)
  print(round(time.time()-t,1),'s',{k:r[k] for k in ('failures','tweaks','tk','crazes','spikes','ore_t','ore_cr','ore_units','sales','sales_sys','sales_std','min_margin','price_up','price_down')},len(r['replacements']))
  print(r['T'])
