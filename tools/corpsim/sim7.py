# Corporations model v7 (user, 5 Nov 2026, evening): corporate R&D. On top of v6:
#  - every product launches at grade 1 with small traits;
#  - a line that keeps losing gets up to 2 small tweaks; if it still loses, its maker funds an R&D project for the next grade
#    (funding, design time, a materials run, trials), then launches the upgraded line and retires the old one at once
#    (its unsold stock goes back to raw ore in the station that holds it);
#  - grades raise a part's main stat by about 1.5 times today's steps; buyers fit up to the grade they can (the powers' AI up
#    to grade 3);
#  - rival makers spy on and sabotage each other's projects (a grey area: no crime); every stage and attack is a mission;
#  - no random galaxy events.
# v6 was (user, 5 Nov 2026, evening): v5, but standard parts are no longer the corporations': each faction's
# stations stock them (the old way), always on the shelf at list price, and makers sell only their trait lines.
# v5 was (user, 5 Nov 2026, evening): v4, but
#  - every maker sells at every station (powers' homes and freeports alike);
#  - no random line-ups: each maker makes the same products in every galaxy, with the same starting traits (the game's lines
#    with the trade-off fixes, and v2's system lines). CEOs and events are still random, and a product that fails its three
#    tweaks is still replaced by a new one with new traits.
# v4 was (user, 5 Nov 2026, evening): v3, and
#  - every corporation also sells at the three freeports;
#  - every station keeps standard parts (the old way) for respawns and for buyers who find no maker's part of the kind;
#  - random galaxy events (a power's famine, feast or plague; a war scare; an ore boom; a component shortage) move demand,
#    component costs and what buyers pay, so the CEOs and supply and demand don't have the market to themselves.
# v3 was (user, 5 Nov 2026, evening), on top of v2's rules:
#  - no upgrades at all: every system, weapon and utility is a part at one level; products differ only in their trade-offs;
#  - the Unbound's gear (jammer, cargo hook, hidden container, cargo scanner) stays outside the corporations (old system);
#  - a replaced product's unsold stock is broken into raw ore that goes into the station holding that stock (the maker is not paid);
#  - no fixed story: each galaxy deals every maker a random line-up of products (leaning to what its name suggests) and rolls
#    their traits afresh;
#  - each maker has a CEO with a trait, kept until a product line fails (replaced after 3 tweaks) or the share price falls far
#    enough below its peak under that CEO; then the board brings in a new CEO with a new trait.
# One step = 1 minute.
import json,math,random
from sim2 import (D,D2,KINDS,SYSTEMS,COST_KEYS,ROLE_W,RSLOTS,KIND_ROLES,HOME_SID,FREEPORTS,POWERS,PT,strength,weakness,to_val,rnd2,
                  fix_tradeoff,value,appeal,new_traits)
UNBOUND={'jammer','hook','hide','cscan'}
CORP_KINDS=[k for k in KINDS if k not in UNBOUND]
SYSD={'engine':'engine','power':'power','shield':'shield','weapon':'weapon','armor':'armor','drill':'drill','hold':'cargo'}
# component cost and ore value of each kind of part. No upgrades and no grades (user, 5 Nov 2026): a part is a part, and
# products differ only in their trade-offs. A system part costs what today's Mk2 system does (so systems and weapons are of
# a size); a weapon or utility costs its standard recipe.
# v7: grades 2 to 5 add the game's part-upgrade components (plate and wire, then coil and matrix, lattice, cores)
ADD={1:0,2:88,3:524,4:1208,5:2298}
COMP={};ORE={}
for k in CORP_KINDS:
  if k in SYSD:
    g=D2['sys'][SYSD[k]]['g']['2'];c,o=g['cv'],g['oreVal']
  else:
    it=next(i for i,x in D['items'].items() if x['part']==k);c,o=D['items'][it]['comp'],D2['items'][it]['oreVal']
  COMP[k]={t:c+ADD[t] for t in range(1,6)};ORE[k]={t:round(o+.8*ADD[t]) for t in range(1,6)}
# what a grade adds to a part's main stat: about 1.5 times today's steps (user, 5 Nov 2026)
GSTEP={'gun':.15,'laser':.15,'missile':.15,'torpedo':.15,'mlaser':.225,'charge':.225,'scanner':.3,'dronec':.15,'cargo':.075,'land':.15,'bdev':1,'lrack':1}
SYS_CUM=[0,0,.27,.54,.72,.9]
def gbonus(k,g):return SYS_CUM[g] if k in SYSTEMS else GSTEP.get(k,.15)*(g-1)
def gval(k,g,role):return ROLE_W[role].get(KINDS[k]['good'][0],0)*gbonus(k,g)
LIST_K=1.11
GRADES=[1,2,3,4,5]
# what makers are known for: a maker is three times as likely to be dealt these kinds
AFF={'ewd':['engine','power'],'qs':['armor','hold','cargo'],'hf':['armor','drill','charge'],'tcy':['hold','cargo','dronec'],'bl':['laser','shield'],'ad':['laser','power','scanner'],
     'mg':['gun','missile','weapon'],'sw':['scanner','mlaser','power'],'cp':['mlaser','charge','drill','scanner','dronec'],'cr':['shield','engine','gun','laser'],
     'mwa':['gun','laser','missile','torpedo'],'wf':['missile','torpedo','charge']}
# CEO traits: what each does in the model
# galaxy events: what each does while it lasts (a power's events hit that power; the others hit the whole galaxy)
EVENTS={
 'famine':dict(w=2,power=True,txt="the power's refits halve, components at its home cost 25% more, buyers there pay 10% less"),
 'feast':dict(w=2,power=True,txt="the power's refits rise by half, contractors flock to its home, buyers there pay 10% more"),
 'plague':dict(w=2,power=True,txt="the power's refits fall 40%, half the contractors stay away from its home, works there run at half speed"),
 'war scare':dict(w=1,power=False,txt="every power refits 50% more, and contractors want fighter parts more often"),
 'ore boom':dict(w=1,power=False,txt="components cost 15% less everywhere"),
 'shortage':dict(w=1,power=False,txt="components cost 30% more everywhere")}
CEOS={
 'Innovator':'new products and tweaks roll a third bigger (same trade-off rule)',
 'Penny-pincher':'running costs -25%, keeps a 5-hour reserve',
 'Premium':'list prices +15%, new products 2 points stronger',
 'Discounter':'list prices -10%, demand rises capped at 1.3x',
 'Expansionist':'opens a new product line when its money passes twice the start (up to 3)',
 'Generous':'pays 60% of profit in dividends (others 40%)',
 'Cautious':'keeps a 6-hour reserve, pays 25% in dividends',
 'Restless':'judges parts over 1 hour and tweaks every 30 minutes'}
P=dict(start=3000,upk=120,upk_line=25,dues=.15,markup=1.5,min_margin=.15,review=20,div=.4,shares=100,
       refit_per_h=12,refit_parts=1.5,contractor_per_h=20,merchant_per_h=16,player_per_h=2,
       beta=8.0,loyal=.06,works_every=1.5,cap={1:4,2:4,3:4,4:4,5:4},grade_w=[1.0],gb_ai=[.45,.35,.2,0,0],gb_other=[.3,.3,.2,.13,.07],small=6,rd_cost={2:1500,3:4000,4:9000,5:18000},rd_design={2:30,3:60,4:90,5:120},rd_mat=(20,60),rd_trial=(15,30),sab_h=.12,spy_h=.10,sab_ok=.6,rd_reserve=3,struggle_h=2,replace=(30,60),reserve=3,retire=120,
       tweak_pts=(2,4),cap_bonus=.25,cap_mag=2,max_tweaks=2,dislike=.5,dislike_min=1.5,window=120,settle=60,launch=300,
       up=1.06,down=.97,pm_max=1.6,hot=1.5,craze_sellouts=3,craze_len=40,craze_k=1.5,spike_every=45,spike_len=30,spike_k=2.0,
       refits=True,hours=16,all_freeports=True,all_ports=True,station_std=True,events=False,event_every=90,event_len=(60,120),trait_lines=(2,3),std_lines=(1,2),ceo=True,ceo_drop=.6,ceo_cool=120,ceo_on_replace=True,random_lineup=False,faction_std=True)
def lineup(rng):
  """deal the galaxy's products: for each kind, 2 to 3 makers with a trait line and 1 to 2 with a standard line"""
  ms=list(D['makers']);deal={m:[] for m in ms}
  for k in CORP_KINDS:
    for std,(lo,hi) in ((False,P['trait_lines']),(True,P['std_lines'])):
      n=rng.randint(lo,hi);pool=[m for m in ms if (k,std) not in deal[m] and (k,not std) not in deal[m]]
      for _ in range(n):
        if not pool:break
        w=[(3 if k in AFF[m] else 1)/(1+len(deal[m])*.35) for m in pool];m=rng.choices(pool,w)[0];pool.remove(m);deal[m].append((k,std))
  return deal
def fixed_lineup():
  """the fixed line-up: the game's maker lines (Unbound gear left out) and v2's system lines, with their fixed traits"""
  from sim2 import CAT
  deal={m:[] for m in D['makers']}
  for id,it in CAT.items():
    if it['part'] in UNBOUND:continue
    if P['faction_std'] and not it['tr']:continue
    tr=dict(it['tr'])
    if tr and P.get('small') and strength(tr)>P['small'] and not any(k=='mag' for k in tr):
      f=P['small']/strength(tr);tr=fix_tradeoff(it['part'],{k:rnd2(v*f,k) for k,v in tr.items()})
    deal[it['maker']].append((it['part'],not it['tr'],tr,it['name']))
  return deal
class Line:
  def __init__(s,kind,std,tr):
    s.kind=kind;s.std=std;s.tr=dict(tr);s.trs=[dict(tr)];s.pm=1.0;s.g=1;s.stock={g:(2 if g==1 else 0) for g in GRADES};s.sold=[];s.ev=[];s.tweaks=0;s.last_tw=-999
    s.sellouts=[];s.craze=0;s.active=True;s.gen=1;s.minst=0;s.sellout_rev=False;s.sold_g={g:0 for g in GRADES};s.ckavg=1.0
  def comp(s,g):return COMP[s.kind][g]
  def lst(s,g,mk):return COMP[s.kind][g]*LIST_K*P['markup']*mk.listk()
  def price(s,g,mk):return s.lst(g,mk)*max(s.pm,s.floor(mk))
  def floor(s,mk):return (1+P['min_margin'])*s.ckavg/((1-P['dues'])*LIST_K*P['markup']*mk.listk())
  def units(s):return sum(s.stock.values())
  def full(s):return s.stock[s.g]>=P['cap'][s.g]
class Maker:
  def __init__(s,m,rng,lines):
    s.m=m;s.name=D['makers'][m]['name'];s.home=D['makers'][m]['home'];s.sid=HOME_SID[s.home];s.T=P['start'];s.alive=True;s.struggling=False;s.rng=rng
    s.ceo=rng.choice(list(CEOS)) if P['ceo'] else None;s.ceo_since=0;s.ceo_peak=None;s.ceos=[(0,s.ceo,None)];s.extra=0;s.proj=None;s.intel=set()
    s.lines=[Line(x[0],x[1],{} if x[1] else (dict(x[2]) if len(x)>2 else s.roll(x[0]))) for x in lines]
    s.share_px=[];s.div_paid=0;s.hist=[];s.born=0;s.rev=0;s.rev_sys=0;s.ck=1.0
  def roll(s,k):
    tr=new_traits(k,s.rng)
    if s.ceo in('Innovator','Premium'):
      f=4/3 if s.ceo=='Innovator' else 1;add=2 if s.ceo=='Premium' else 0
      g=[x for x in tr if x in KINDS[k]['good'] and tr[x]>0 and not (x in COST_KEYS)]
      for x in g:
        if x=='mag':continue
        tr[x]=rnd2(min(P['cap_bonus'],tr[x]*f+to_val(x,add/len(g))),x)
      tr=fix_tradeoff(k,tr)
    return tr
  def listk(s):return {'Premium':1.15,'Discounter':.9}.get(s.ceo,1.0)
  def upkeep_h(s):return (P['upk']+P['upk_line']*sum(1 for L in s.lines if L.active))*(.75 if s.ceo=='Penny-pincher' else 1)
  def reserve(s):return {'Penny-pincher':5,'Cautious':6}.get(s.ceo,P['reserve'])
  def divk(s):return {'Generous':.6,'Cautious':.25}.get(s.ceo,P['div'])
  def window(s):return 60 if s.ceo=='Restless' else P['window']
  def settle(s):return 30 if s.ceo=='Restless' else P['settle']
  def stockval(s):return sum(L.comp(g)*n for L in s.lines for g,n in L.stock.items())
  def px(s):return max(1,(s.T+s.stockval())/P['shares'])
def sim(seed,params=None):
  global P
  P0=P;P=dict(P0,**(params or {}));rng=random.Random(seed)
  try:
    deal=lineup(rng) if P['random_lineup'] else fixed_lineup()
    makers={m:Maker(m,rng,deal[m]) for m in D['makers']}
    st=dict(failures=[],replacements=[],tweaks=0,crazes=0,spikes=0,div=0,ore_cr=0.0,ore_units=0,ore_at={},launch=0,sales=0,sales_sys=0,sales_std=0,
            station_std=0,faction_std=0,projects=[],launches=[],sab=0,sab_hit=0,spy=0,missions={},gtime=[],std_kind={},events=[],rev_g={g:0.0 for g in GRADES},sales_g={g:0 for g in GRADES},min_margin=9,ceo_changes=[],opened=0,lost=0)
    spike=[];EV=[]
    def ev_on(k,tgt=None):return any(e['k']==k and (tgt is None or e['tgt']==tgt) for e in EV)
    def refit_k(f):
      k=1.0
      if ev_on('famine',f):k*=.5
      if ev_on('feast',f):k*=1.5
      if ev_on('plague',f):k*=.6
      if ev_on('war scare'):k*=1.5
      return k
    OWN={HOME_SID[f]:f for f in POWERS}
    def cost_k(sid):
      k=1.0
      if sid in OWN and ev_on('famine',OWN[sid]):k*=1.25
      if ev_on('ore boom'):k*=.85
      if ev_on('shortage'):k*=1.3
      return k
    def pay_k(where):
      if not where or where[0] not in OWN:return 1.0
      f=OWN[where[0]];return (1.1 if ev_on('feast',f) else 1.0)*(.9 if ev_on('famine',f) else 1.0)
    def slow(sid):return sid in OWN and ev_on('plague',OWN[sid])
    def buy(role,where,kind=None,mult=1.0,ai=False):
      k=kind or rng.choice(RSLOTS[role])
      if k not in COMP or (k=='drill' and role!='miner'):return
      gb=rng.choices(GRADES,P['gb_ai'] if ai else P['gb_other'])[0]
      cands=[(mk,L) for mk in makers.values() if mk.alive and (where is None or P['all_ports'] or mk.sid in where or (P['all_freeports'] and any(x in FREEPORTS for x in where))) for L in mk.lines if L.kind==k and L.active and L.g<=gb and L.stock[L.g]>0]
      if not cands and P['faction_std']:st['faction_std']+=1;return
      if not cands:
        # the station's own standard parts (the old way), or nothing
        if P['station_std']:st['station_std']+=1
        else:st['lost']+=1
        return
      xs=[]
      for mk,L in cands:
        x=(1+value(L.tr,role)+gval(L.kind,L.g,role))/(L.pm*mk.listk())+(P['loyal'] if where and mk.sid==where[0] else 0)
        if L.craze>0:x*=P['craze_k']
        xs.append(P['beta']*x)
      # the faction's standard part is always there to choose instead, at list price
      if P['faction_std']:xs.append(P['beta']*1.0)
      mx=max(xs);sc=[math.exp(v-mx) for v in xs];t=sum(sc);r=rng.random()*t;i=0
      while r>sc[i]:r-=sc[i];i+=1
      n=len(xs)
      for j,(mk2,L2) in enumerate(cands):L2.ev.append((now,1/n,j==i))
      if i>=len(cands):st['faction_std']+=1;st['std_kind'][k]=st['std_kind'].get(k,0)+1;return
      mk,L=cands[i];g=L.g;pr=max(L.price(g,mk)*pay_k(where),L.lst(g,mk)*L.floor(mk))*mult;L.stock[g]-=1;L.sold.append(now);L.sold_g[g]+=1;net=pr*(1-P['dues']);mk.T+=net;mk.rev+=net
      if P.get('log'):st.setdefault('log',[]).append((now,mk.m,net,mk.ck,L.comp(g)))
      m=net/(L.comp(g)*L.ckavg)-1;st['min_margin']=min(st['min_margin'],m);st['sales']+=1;st['rev_g'][g]+=net;st['sales_g'][g]+=1
      if L.kind in SYSTEMS:st['sales_sys']+=1;mk.rev_sys+=net
      if L.std:st['sales_std']+=1
      if L.stock[g]==0:L.sellouts.append(now);L.sellout_rev=True
    def poisson(rate):
      n=0;l=math.exp(-rate);p=rng.random()
      while p>l:n+=1;p*=rng.random()
      return n
    def share(L,mk):
      E=[e for e in L.ev if e[0]>now-mk.window()];return sum(1 for e in E if e[2]),sum(e[1] for e in E)
    def disliked(L,mk):
      got,exp=share(L,mk);return exp>=P['dislike_min'] and got<P['dislike']*exp
    def tweak(L,mk):
      opts=[];K=KINDS[L.kind];lo,hi=P['tweak_pts']
      if mk.ceo=='Innovator':lo,hi=lo*4/3,hi*4/3
      cur_w=[k for k,v in L.tr.items() if (k not in COST_KEYS and v<0) or (k in COST_KEYS and v>0)]
      for g in K['good']:
        if g in L.tr and L.tr[g]<0:continue
        d=10 if g=='mag' else rng.uniform(lo,hi)
        t=dict(L.tr);capv=P['cap_mag'] if g=='mag' else P['cap_bonus'];nv=min(capv,t.get(g,0)+to_val(g,d))
        if nv<=t.get(g,0)+1e-9:continue
        t[g]=rnd2(nv,g)
        for wk,sg in K['weak']:
          if wk==g:continue
          need=strength(t)/2-weakness(t)+.1;t3=dict(t)
          if need>0:
            add=max(10,math.ceil(need/10)*10) if wk=='mag' else need
            if wk in t3 and ((t3[wk]>0)!=(sg>0)):continue
            t3[wk]=rnd2(t3.get(wk,0)+sg*to_val(wk,add),wk)
          opts.append((appeal(L.kind,t3),t3))
      if cur_w:
        wp=weakness(L.tr)
        for wk,sg in K['weak']:
          if wk in cur_w or (wk in L.tr and ((L.tr[wk]>0)!=(sg>0))):continue
          t={k:v for k,v in L.tr.items() if k not in cur_w};add=max(10,math.ceil(wp/10)*10) if wk=='mag' else wp
          t[wk]=rnd2(sg*to_val(wk,add),wk);opts.append((appeal(L.kind,t),t))
      if not opts:return False
      opts.sort(key=lambda x:-x[0]);L.tr=opts[0][1];L.trs.append(dict(L.tr));return True
    def new_ceo(mk,why):
      old=mk.ceo;mk.ceo=rng.choice([c for c in CEOS if c!=old]);[setattr(L,'pm',max(L.pm,L.floor(mk))) for L in mk.lines];mk.ceo_since=now;mk.ceo_peak=None;mk.ceos.append((now,mk.ceo,why));st['ceo_changes'].append((now,mk.m,old,mk.ceo,why))
    for now in range(int(P['hours']*60)):
      # galaxy events
      EV=[e for e in EV if e['t1']>now]
      if P['events'] and rng.random()<1/P['event_every']:
        k=rng.choices(list(EVENTS),[v['w'] for v in EVENTS.values()])[0];tgt=rng.choice(POWERS) if EVENTS[k]['power'] else None
        if not ev_on(k,tgt):e=dict(k=k,tgt=tgt,t0=now,t1=now+rng.randint(*P['event_len']));EV.append(e);st['events'].append(e)
      for mk in makers.values():mk.ck=cost_k(mk.sid)
      # works: build the emptiest shelf it can afford, keeping its reserve
      if now%max(1,int(P['works_every']))==0:
        for mk in makers.values():
          if not mk.alive or (slow(mk.sid) and now%(2*max(1,int(P['works_every'])))):continue
          opts=sorted(((L.stock[g]/P['cap'][g],g,id(L),L) for L in mk.lines if L.active for g in GRADES if g==L.g and L.stock[g]<P['cap'][g]),key=lambda x:(x[0],x[1]))
          for _,g,_,L in opts:
            c=L.comp(g)*mk.ck
            if mk.T-c>=mk.reserve()*mk.upkeep_h():u=L.units();L.ckavg=(L.ckavg*u+mk.ck)/(u+1);mk.T-=c;L.stock[g]+=1;break
      for mk in makers.values():
        if mk.alive:mk.T-=mk.upkeep_h()/60
      # R&D projects: stages, and rivals' espionage and sabotage
      def mis(k):st['missions'][k]=st['missions'].get(k,0)+1
      for mk in makers.values():
        pj=mk.proj
        if not mk.alive or not pj:continue
        rivals=[r for r in makers.values() if r is not mk and r.alive and any(L.kind==pj['L'].kind for L in r.lines)]
        for r in rivals:
          if rng.random()<P['sab_h']/60:
            st['sab']+=1;mis('sabotage');mis('security')
            if rng.random()<P['sab_ok']*(.5 if mk.ceo=='Cautious' else 1):
              st['sab_hit']+=1
              if pj['stage']=='design':pj['t']+=20
              elif pj['stage']=='materials':pj['t']=now+rng.randint(*P['rd_mat']);mk.T-=.1*pj['cost']
              else:pj['t']=now+rng.randint(*P['rd_trial'])
          if rng.random()<P['spy_h']/60:
            st['spy']+=1;mis('espionage')
            rp=r.proj
            if rp and rp['L'].kind==pj['L'].kind:rp['t']-=max(0,(rp['t']-now)*.25)
            else:r.intel.add(pj['L'].kind)
        if now>=pj['t']:
          if pj['stage']=='design':pj['stage']='materials';pj['t']=now+rng.randint(*P['rd_mat']);mis('materials run');mis('rare ore')
          elif pj['stage']=='materials':pj['stage']='trials';pj['t']=now+rng.randint(*P['rd_trial']);mis('prototype escort');mis('test flight')
          else:
            # launch: the old line is retired at once; its stock goes back to raw ore in the station that holds it
            L=pj['L'];u=L.units();v=sum(ORE[L.kind][g]*n for g,n in L.stock.items());st['ore_units']+=u;st['ore_cr']+=v;st['ore_at'][mk.sid]=st['ore_at'].get(mk.sid,0)+v
            L.g=pj['g'];L.stock={g:0 for g in GRADES};L.tr=mk.roll(L.kind);L.trs.append(dict(L.tr));L.tweaks=0;L.gen+=1;L.last_tw=now;L.ev=[];L.pm=1.0;L.sold=[];L.active=True;L.ckavg=1.0
            st['launches'].append((now,mk.m,L.kind,L.g,now-pj['t0']));mk.proj=None;mis('launch delivery')
      if now%60==0:
        gs=[L.g for mk in makers.values() for L in mk.lines]
        st['gtime'].append((now,max(gs),sum(gs)/len(gs),sum(1 for x in gs if x>=2)/len(gs)))
      if P['refits']:
        for f in POWERS:
          for _ in range(poisson(P['refit_per_h']*P['refit_parts']*refit_k(f)/60)):buy('fighter',[HOME_SID[f]]+FREEPORTS,ai=True)
      for _ in range(poisson(P['contractor_per_h']/60)):
        role=rng.choices(['fighter','hauler','miner','scout'],[.6 if ev_on('war scare') else .4,.3,.25,.05])[0]
        sites=FREEPORTS+['hp','vb','os'];w=[(2 if s in OWN and ev_on('feast',OWN[s]) else 1)*(.5 if s in OWN and ev_on('plague',OWN[s]) else 1) for s in sites]
        buy(role,[rng.choices(sites,w)[0]])
      for _ in range(poisson(P['merchant_per_h']/60)):
        role=rng.choices(['fighter','hauler','miner','scout'],[.45,.3,.2,.05])[0];buy(role,None)
      for _ in range(poisson(P['player_per_h']/60)):buy(rng.choice(['fighter','hauler','miner']),None)
      if rng.random()<1/P['spike_every']:
        k=rng.choice(CORP_KINDS);spike.append((k,now+P['spike_len']));st['spikes']+=1
        for mk in makers.values():
          for L in mk.lines:
            if L.kind==k and not L.active and mk.alive:L.active=True
      spike=[s for s in spike if s[1]>now]
      for k,_ in spike:
        for _ in range(poisson(10/60/max(1,len(spike)))):buy(rng.choice(list(KIND_ROLES[k]) or ['fighter']),None,kind=k,mult=P['spike_k'])
      for mk in makers.values():
        for L in mk.lines:
          if L.craze>0:L.craze-=1
          elif len([t for t in L.sellouts if t>now-60])>=P['craze_sellouts']:L.craze=P['craze_len'];st['crazes']+=1;L.sellouts=[]
      if now%P['review']==0 and now>0:
        for mk in makers.values():
          if not mk.alive:continue
          prof=mk.T-(mk.hist[-1] if mk.hist else P['start']);mk.hist.append(mk.T);replaced=False
          for L in mk.lines:
            L.ev=[e for e in L.ev if e[0]>now-max(P['window'],60)]
            if not L.active:continue
            got,exp=share(L,mk)
            if any(t>now-60 for t in L.sold) and not disliked(L,mk):
              fl=L.floor(mk);cap=1.3 if mk.ceo=='Discounter' else P['pm_max']
              if L.sellout_rev or (exp>=1 and got>=P['hot']*exp):L.pm=min(cap,L.pm*P['up'])
              elif got<exp and L.full() and L.pm>fl+1e-9:L.pm=max(fl,L.pm*P['down'])
            elif not L.std and disliked(L,mk) and now-L.last_tw>=mk.settle():
              if L.tweaks<P['max_tweaks']:
                if tweak(L,mk):L.tweaks+=1;L.last_tw=now;st['tweaks']+=1;L.ev=[]
              elif mk.proj is None and L.g<5 and mk.T-P['rd_cost'][L.g+1]>=max(mk.reserve(),P['rd_reserve'])*mk.upkeep_h():
                # R&D: fund a project for the next grade of this kind
                ng=L.g+1;c=P['rd_cost'][ng];mk.T-=c;d=P['rd_design'][ng]*(.7 if L.kind in mk.intel else 1);mk.intel.discard(L.kind)
                mk.proj=dict(L=L,g=ng,stage='design',t=now+d,t0=now,cost=c);st['projects'].append((now,mk.m,L.kind,ng));replaced=True
            L.sellout_rev=False
            if P['retire'] and L.active and now>P['retire'] and not [t for t in L.sold if t>now-P['retire']] and L.full():L.active=False
          # an Expansionist opens a new line when rich
          if mk.ceo=='Expansionist' and mk.T>2*P['start'] and mk.extra<3:
            have={(L.kind,L.std) for L in mk.lines};ks=[k for k in CORP_KINDS if (k,False) not in have and (k,True) not in have]
            if ks:k=rng.choice(ks);mk.lines.append(Line(k,False,mk.roll(k)));mk.extra+=1;mk.T-=P['launch'];st['opened']+=1
          mk.struggling=mk.T<P['struggle_h']*mk.upkeep_h()
          if prof>0 and not mk.struggling:
            d=prof*mk.divk();mk.T-=d;mk.div_paid+=d;st['div']+=d
          px=mk.px();mk.share_px.append((now,px,mk.div_paid/P['shares']))
          # the board: a product line failed, or the shares fell far below their peak under this CEO
          if P['ceo']:
            mk.ceo_peak=max(mk.ceo_peak or px,px)
            if now-mk.ceo_since>=P['ceo_cool']:
              if replaced and P['ceo_on_replace']:new_ceo(mk,'line')
              elif px<P['ceo_drop']*mk.ceo_peak:new_ceo(mk,'shares')
      for m,mk in list(makers.items()):
        if mk.alive and mk.T<=0:
          mk.alive=False;mk.failed_at=now;st['failures'].append((now,m,mk.name,mk.ceo));mk.rebirth=now+rng.randint(*P['replace'])
        if not mk.alive and now>=getattr(mk,'rebirth',1e9):
          nm=Maker(m,rng,[(L.kind,L.std) for L in mk.lines]);mk.proj=None;nm.born=now;makers[m]=nm
          # the company's history carries on: its shares were worth nothing while it was gone
          nm.share_px=mk.share_px+[(mk.failed_at,0,mk.div_paid/P['shares'])];nm.ceos=mk.ceos+[(now,nm.ceo,'new company')];nm.div_paid=0
    lines=[(mk.m,L.kind,L.std,L.tweaks,L.gen,L.tr,round(L.pm,3),len(L.sold),L.trs,L.g) for mk in makers.values() for L in mk.lines]
    return dict(st,T={m:round(mk.T) for m,mk in makers.items()},struggling={m:mk.struggling for m,mk in makers.items()},
                divm={m:round(mk.div_paid) for m,mk in makers.items()},rev={m:round(mk.rev) for m,mk in makers.items()},rev_sys={m:round(mk.rev_sys) for m,mk in makers.items()},
                px={m:mk.share_px for m,mk in makers.items()},ceos={m:mk.ceos for m,mk in makers.items()},deal={m:deal[m] for m in deal},lines=lines)
  finally:
    P=P0
if __name__=='__main__':
  import time;t=time.time();r=sim(1)
  print(round(time.time()-t,1),'s',{k:r[k] for k in ('failures','tweaks','crazes','spikes','ore_cr','ore_units','sales','sales_sys','sales_std','min_margin','opened','lost','sales_g')},len(r['replacements']),len(r['ceo_changes']))
  print(r['T']);print({m:[c[1] for c in v] for m,v in r['ceos'].items()})
  print({k:v for k,v in COMP.items()})
