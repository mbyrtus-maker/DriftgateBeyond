# v19 (6 Nov 2026, the user: "corporations shouldn't be stupid with cash flow; they should fail when their products don't
# keep up with upgrades, their tweaks don't win back sales, or their goods aren't cheap or available"): v18's rules (storage,
# markdowns, shut lines selling out, the old grade retired, no budget line) with a prudent maker: it builds to its sales
# (a line's shelf target is 1 + what it sold in the last hour, up to the cap), keeps an hour of running costs back from
# building, and funds R&D only with 3 hours of costs to spare. Every failure is diagnosed: was the maker still selling its
# fair share (a cash-flow failure, which shouldn't happen), out-graded, out-tweaked, too dear, or out of stock?
# v18 (6 Nov 2026, the user's rules after v17: "go broke or go home"): no reserve kept back (only a Penny-pincher's or a
# Cautious CEO's own caution); the station charges each maker storage on every unit on its shelves (store_h of the unit's
# component cost an hour), shut lines included; a station marks down goods that aren't moving below the maker's profit
# floor (md_step each review after stale minutes without a sale, down to md_min of the normal price, easing back as they
# sell); a shut line stops building and stops paying its line cost but keeps its stock on sale (marked down, paying
# storage) until it sells out; a launch retires the old grade at once (stock to ore, as v16): another maker's grade 1 may
# pick up the low end. Running costs and R&D are paid to the host station (no change to the makers' side of the model).
# Corporations model v17 (user, 6 Nov 2026): v16 with
#  - buyers who weigh price against quality, by how much money they have. Each buyer is cash-strapped, steady or flush;
#    a part's appeal is its quality (1 + its stats' worth + its grade's worth) divided by its price relative to the kind's
#    grade 1 list price raised to the buyer's price sensitivity (strapped 1.0, steady 0.5, flush 0.15). Contractors are
#    40% strapped, 40% steady, 20% flush; the powers' refits half steady, half flush; other pilots 35/40/25. Before, price
#    only mattered between parts of the same grade, so a better grade always won when a buyer could afford it;
#  - a launch no longer clears the old grade off the market (old='clear' or 'budget'):
#    'clear'  - the old grade's stock stays on the shelves on clearance at 30% off list (about what it cost to build, so no
#               profit), and is not rebuilt; stock unsold for 2 hours is broken into ore as before;
#    'budget' - the old grade stays as the maker's cheaper line at 15% off list (still 15% over cost), built and sold like
#               any line (and paying its running cost), with no tweaks or R&D of its own; at the next launch the old budget
#               line goes on clearance and the grade just replaced becomes the budget line.
# v16 was (user, 6 Nov 2026): v15 with
#  - pilots don't trade shares (designed, not built): makers' money, shares and dividends run in the background, and what
#    the makers do (R&D projects, materials runs, trials, spying, sabotage) is what pilots see, as missions;
#  - a maker answers a rival that is outselling it: when the best-selling rival maker of a kind of part has sold at least
#    twice as many in the maker's review window (45 min) as the maker's own line, and at least 3 more, the maker tweaks that
#    line, as often as every 30 minutes. Being outsold never starts an R&D project by itself (that doubled failures, to 0.73
#    a galaxy, by sending makers into R&D early); R&D still follows 2 tweaks of a line buyers pass by;
#  - a tweak is instant and changes every unit of that line already on the shelves.
# v15 was (user, 5 Nov 2026, late): v14 with
#  - CEOs replaced by the board after the share price has fallen several periods in a row (by default 2 hours running,
#    each hour's price under the hour before's; 3 hours gave about 4 changes a galaxy, 2 about 10), not when a product line is replaced; a new CEO has 2 hours' grace;
#  - shares that pay a pilot back with interest within about 2 hours (user: 'reliably ahead at 2 h', about +10% and ahead
#    about 85% of the time). run_v15.py measures a pilot's 2-hour round trip with a broker's fee each way and the price moved
#    by their own buying and selling. To get there:
#    - R&D money counts as an asset at cost while the project runs (worth 1.0, 1.2, 1.4 times its cost through design,
#      materials and trials), so starting a project no longer knocks the price down;
#    - the launch premium is used up as the new line's earnings come through (and fades only slowly otherwise), instead of
#      fading on a clock while earnings lag behind;
#    - investors are calmer still (mood and noise a third of v14's), earnings are smoothed over longer, and sales growth
#      counts for less (0.2).
# v14 was (user, 5 Nov 2026, late): v13's market, with
#  - R&D paid for out of the maker's own money (no share issues);
#  - dividends that grow with success: a maker pays out 40% of its profit when it earns the galaxy's average, more when it
#    earns more (up to 80%), less when it earns less (down to 10%); Generous CEOs pay half as much again, Cautious ones 40% less;
#  - the powers' politics: each pair of powers drifts between peace, tension and war (standing in for the game's own wars).
#    A power at war refits its warships twice as often (1.3 times under tension), buys weapons, armour and shields half as
#    often again, and its miners and haulers refit 20% less; contractors take fighter work more often while any war is on.
#    Investors move at once: weapon makers rise on tension and war and fall on peace, in proportion to how much of what they
#    make is war gear (guns, lasers, launchers, fire control, armour, shields);
#  - analysts: every hour each maker gets a rough rating (strong buy, buy, hold, sell, strong sell) from the analysts' own
#    estimate of its value, which is off by about 18% and changes its mind slowly; players see the rating, not the value;
#  - sales growth smoothed before investors use it, and calmer investors (mood moves a third as fast, lasts longer) - prices
#    were too jumpy;
#  - until a maker's smoothed earnings have built up, investors assume it earns a typical 200 cr an hour (not its first
#    few minutes' sales scaled up).
# v13 was (user, 5 Nov 2026, late): v12 with the products evened out (every maker's expected earnings after
# running costs within about 190 to 250 cr an hour), and share prices set by a market (see the stock market section below).
# Stock market (v13): each maker's shares trade at a market price that chases what investors think the company is worth:
#   value per share = (money + stock at cost)/shares                                 book value
#                   + earnings per hour (smoothed over hours) x 8 h x (1 + half the sales growth)/shares
#                   + an R&D project in progress: its cost x 1.5 x how far along/shares  the pipeline
#                     (at launch it becomes a launch premium that fades by half in about 2 hours)
#                   + dividends per hour (smoothed) x 4 h/shares                      income investors like
# Investors' mood (the market's and each company's) drifts and reverts, so a price can stay under or over value for hours.
# Every 5 minutes the price moves 8% of the way to value times mood, keeps 15% of its last move (momentum), and takes a little
# noise; news moves it at once (a launch +8%, a project started -2%, sabotage suffered -4%, a spy's success +2%, a tweak
# -0.5%, a new CEO -3%). A company that fails is worth nothing. Optionally a maker short of R&D money issues new shares
# (up to 30% more, at 95% of the price) instead of waiting.
# v12 was (user, 5 Nov 2026, evening): v11 with running costs doubled for the bigger market (240 cr an hour plus
# 50 per active line), and R&D funded with 3 hours of running costs kept back (6 before), for about one failure in a galaxy and
# the first R&D launch at about 3 hours.
# v11 was (user, 5 Nov 2026, evening): v10, and the powers refit their whole fleets, not just warships:
#  - mining fleets (Varkesh, the ore-hungry garrison state, twice as much as the others; it favours mining lasers, charge
#    launchers and blast rigs and values mining yield), so mining gear is popular;
#  - haulers (Halcyon's merchant houses most; they favour cargo holds and modules and value hold and speed);
#  - scouts (Ostrova's archive fleet most; it favours scanners);
#  - miners buy their mining gear (mining lasers, charge launchers, blast rigs) three times as often as other parts' share.
# v10 was (user, 5 Nov 2026, evening): v9 with the goods divided more evenly, so every maker has at least
# one solid line (a part every hull fits: a system part, a gun or a laser). 39 trait lines as before, 2 to 4 per maker.
# Lines a maker already had keep their traits; new ones get small traits rolled once and fixed.
# v9 was (user, 5 Nov 2026, evening): v8 tuned so the first R&D launch comes at about 3 hours:
#  - products judged over 45 minutes of sales, on less evidence, and tweaked every 15 minutes;
#  - project stages shorter (design G2 15 min ... G5 60; materials 10 to 20; trials 5 to 15);
#  - a project is funded with 6 hours of running costs to spare (8 before).
# v8 was (user, 5 Nov 2026, evening): v7 with a shorter timeline and the powers' tastes:
#  - products are judged over 1 hour and tweaked every 30 minutes; R&D costs half (G2 750 cr ... G5 9,000), and a project is
#    funded only with 8 hours of running costs to spare;
#  - each power's refits favour the equipment and traits of its doctrine (Halcyon shields, Varkesh armour and guns, Ostrova
#    reactors and rapid fire): it buys more of those kinds of part and values those stats more;
#  - spying speeds up the spy's own R&D (its current project, or a head start on its next); sabotage only slows the target's.
# v7 was (user, 5 Nov 2026, evening): corporate R&D. On top of v6:
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
def gval(k,g,role,pw=None):return ROLE_W[role].get(KINDS[k]['good'][0],0)*taste(pw,KINDS[k]['good'][0])*gbonus(k,g)
# the powers' tastes, from their doctrines (01_core WING_DOC): kinds of part their refits buy more of, and stats they value more
TASTE={'halcyon':dict(kinds={'shield':2.0,'laser':1.5,'engine':1.3,'hold':1.5,'cargo':1.5},stats={'sh':1.6,'shr':1.6,'speed':1.2,'hp':.8,'cargo':1.3}),
       'varkesh':dict(kinds={'armor':2.0,'gun':1.5,'weapon':1.5,'torpedo':1.3,'mlaser':1.5,'charge':1.5,'drill':1.5},stats={'hp':1.6,'dmg':1.4,'speed':.7,'ml':1.4}),
       'ostrova':dict(kinds={'power':2.0,'weapon':1.5,'scanner':1.8},stats={'en':1.6,'enr':1.6,'track':1.4,'e':.6,'shr':.8})}
# miners wear out and upgrade their mining gear most: they buy mining lasers, charge launchers and blast rigs more often (v11)
MINE_K={'mlaser','charge','drill'}
def taste(pw,k):return TASTE[pw]['stats'].get(k,1.0) if pw and P['tastes'] else 1.0
def appeal8(kind,tr):
  # makers judge a tweak by all their buyers: the roles that fit the part, and the powers' refits with their tastes
  base=appeal(kind,tr)
  if not P['tastes'] or 'fighter' not in KIND_ROLES[kind]:return base
  pw=sum(TASTE[f]['kinds'].get(kind,1.0)*pvalue(tr,'fighter',f) for f in TASTE)/sum(TASTE[f]['kinds'].get(kind,1.0) for f in TASTE)
  return .5*base+.5*pw
def pvalue(tr,role,pw):return sum(ROLE_W[role].get(k,0)*taste(pw,k)*v for k,v in tr.items())
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
P=dict(start=3000,upk=240,upk_line=50,dues=.15,markup=1.5,min_margin=.15,review=20,div=.4,shares=100,
       refit_per_h=12,refit_parts=1.5,contractor_per_h=20,merchant_per_h=16,player_per_h=2,
       beta=8.0,loyal=.06,works_every=1.5,cap={1:4,2:4,3:4,4:4,5:4},grade_w=[1.0],gb_ai=[.45,.35,.2,0,0],gb_other=[.3,.3,.2,.13,.07],small=6,rd_cost={2:750,3:2000,4:4500,5:9000},rd_design={2:15,3:30,4:45,5:60},rd_mat=(10,20),rd_trial=(5,15),sab_h=.12,spy_h=.10,sab_ok=.6,rd_reserve=3,tastes=True,struggle_h=2,replace=(30,60),reserve=1,retire=120,pace=60,diag=180,
       tweak_pts=(2,4),cap_bonus=.25,cap_mag=2,max_tweaks=2,dislike=.5,dislike_min=1.0,window=45,settle=15,launch=300,
       up=1.06,down=.97,pm_max=1.6,hot=1.5,craze_sellouts=3,craze_len=40,craze_k=1.5,spike_every=45,spike_len=30,spike_k=2.0,
       refits=True,hours=16,all_freeports=True,all_ports=True,station_std=True,events=False,event_every=90,event_len=(60,120),trait_lines=(2,3),std_lines=(1,2),ceo=True,ceo_drop=.6,ceo_cool=120,ceo_on_replace=True,random_lineup=False,faction_std=True,lineup10=True,lineup13=True,mkt_H=8,pipe_k=1.5,div_H=4,fresh_k=.5,fresh_decay=.998,mood_keep=.995,mood_sd=.004,market_sd=.002,kappa=.08,mu=.05,sigma=.002,e_a=.006,g_w=.2,d_a=.02,issue=False,issue_max=.3,news={'launch':.08,'project':-.02,'sabotaged':-.04,'spied':.02,'tweak':-.005,'ceo':-.03},miner_refit={'halcyon':6,'varkesh':12,'ostrova':6},hauler_refit={'halcyon':10,'varkesh':4,'ostrova':5},scout_refit={'halcyon':2,'varkesh':2,'ostrova':5},mine_k=3.0,debias='prior',listing=60,div_lo=.1,div_hi=.8,g_a=.03,politics=True,pol_rates=dict(tension=1/8,war=1/1.5,calm=1/2,peace=1/2.5),war_fit=2.0,tension_fit=1.3,war_kinds=1.5,war_civil=.8,war_news={'tension':.03,'war':.06,'peace':-.05,'civil_war':-.02,'civil_peace':.01},rating=True,an_sd=.18,an_keep=.85,e_prior=200,ceo_mode='streak',ceo_period=60,ceo_streak=2,pipe_stage={'design':.67,'materials':.8,'trials':.93},fresh_mode='earn',outsold=True,out_ratio=2.0,out_min=3,out_dislike=True,out_rd=False,out_cool=30,price_sens=True,sens={'strapped':1.0,'steady':.5,'flush':.15},wealth={'contractor':(.4,.4,.2),'power':(0,.5,.5),'other':(.35,.4,.25)},old='retire',clear_pm=.7,store_h=.03,stale=60,md_step=.9,md_min=.5,md_back=1.04,shut_sell=True,budget_pm=.85,orders=None,order_share=.5,order_premium=.2,order_deposit=.6)
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
LINEUP10={'ewd':['engine','power','cargo'],'tcy':['engine','armor','cargo','dronec'],'cr':['engine','shield'],'sw':['power','weapon','mlaser'],
  'ad':['power','shield','scanner'],'bl':['shield','laser','scanner'],'mg':['weapon','gun','missile'],'mwa':['gun','laser','torpedo'],
  'wf':['gun','weapon','missile','torpedo'],'qs':['armor','hold','cargo'],'hf':['armor','hold','charge','drill'],'cp':['hold','mlaser','drill','dronec']}
SOLID={'engine','power','shield','weapon','armor','hold','gun','laser'}
LINEUP13={'ewd': ['engine', 'power', 'cargo'], 'tcy': ['engine', 'hold', 'cargo', 'dronec'], 'cr': ['engine', 'shield'], 'sw': ['power', 'weapon', 'scanner'], 'ad': ['power', 'shield', 'scanner'], 'bl': ['shield', 'laser', 'torpedo'], 'mg': ['weapon', 'gun', 'mlaser'], 'mwa': ['armor', 'laser', 'torpedo', 'missile'], 'wf': ['gun', 'weapon', 'charge', 'missile'], 'qs': ['armor', 'hold', 'cargo', 'gun'], 'hf': ['armor', 'dronec', 'drill'], 'cp': ['hold', 'mlaser', 'drill']}
def lineup10():
  from sim2 import CAT
  import zlib
  deal={m:[] for m in D['makers']}
  for m,ks in (LINEUP13 if P.get('lineup13') else LINEUP10).items():
    for k in ks:
      old=[it for it in CAT.values() if it['maker']==m and it['part']==k and it['tr']]
      tr=dict(old[0]['tr']) if old else new_traits(k,random.Random(zlib.crc32(('v10'+m+k).encode())))
      if P.get('small') and strength(tr)>P['small'] and not any(x=='mag' for x in tr):
        f=P['small']/strength(tr);tr=fix_tradeoff(k,{x:rnd2(v*f,x) for x,v in tr.items()})
      deal[m].append((k,False,tr,D['makers'][m]['name']+' '+KINDS[k]['name'].lower()))
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
    s.sellouts=[];s.craze=0;s.active=True;s.gen=1;s.minst=0;s.sellout_rev=False;s.sold_g={g:0 for g in GRADES};s.ckavg=1.0;s.clear=False;s.budget=False;s.md=1.0;s.shut=False
  def comp(s,g):return COMP[s.kind][g]
  def lst(s,g,mk):return COMP[s.kind][g]*LIST_K*P['markup']*mk.listk()
  def price(s,g,mk):return s.lst(g,mk)*(s.pm if s.clear else max(s.pm,s.floor(mk)))*s.md
  def floor(s,mk):return (1+P['min_margin'])*s.ckavg/((1-P['dues'])*LIST_K*P['markup']*mk.listk())
  def units(s):return sum(s.stock.values())
  def full(s):return s.stock[s.g]>=P['cap'][s.g]
class Maker:
  def __init__(s,m,rng,lines):
    s.m=m;s.name=D['makers'][m]['name'];s.home=D['makers'][m]['home'];s.sid=HOME_SID[s.home];s.T=P['start'];s.alive=True;s.struggling=False;s.rng=rng
    s.ceo=rng.choice(list(CEOS)) if P['ceo'] else None;s.ceo_since=0;s.ceo_peak=None;s.ceos=[(0,s.ceo,None)];s.extra=0;s.proj=None;s.intel=set()
    s.lines=[Line(x[0],x[1],{} if x[1] else (dict(x[2]) if len(x)>2 else s.roll(x[0]))) for x in lines]
    s.share_px=[];s.div_paid=0;s.evlog=[];s.oos=[];s.asked=[];s.hist=[];s.born=0;s.rev=0;s.rev_sys=0;s.ck=1.0
    s.shares=P['shares'];s.mp=P['start']/P['shares'];s.mp_prev=s.mp;s.E=0.0;s.op=0.0;s.sales_t=[];s.div_ema=0.0;s.div_recent=0.0;s.mkt=[];s.V=s.mp;s.issued=0;s.mood=0.0;s.fresh=0.0;s.nobs=0;s.lsum=0.0;s.ev_last=0.0;s.ev_ref=None;s.Eu=0.0;s.gs=0.0;s.an=0.0;s.dps=0.0;s.gen=0;s.rating=None
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
  def upkeep_h(s):return (P['upk']+P['upk_line']*sum(1 for L in s.lines if L.active and not L.clear and not L.shut))*(.75 if s.ceo=='Penny-pincher' else 1)
  def reserve(s):return ({'Penny-pincher':5,'Cautious':6} if P.get('ceo_reserve',True) else {}).get(s.ceo,P['reserve'])
  def divk(s,avgE=None):
    if avgE is None or avgE<=0:k=P['div']
    else:k=max(P['div_lo'],min(P['div_hi'],P['div']*max(0,s.Eu)/avgE))
    return min(.9,k*{'Generous':1.5,'Cautious':.6}.get(s.ceo,1.0))
  def window(s):return 60 if s.ceo=='Restless' else P['window']
  def settle(s):return 30 if s.ceo=='Restless' else P['settle']
  def stockval(s):return sum(L.comp(g)*n for L in s.lines for g,n in L.stock.items())
  def px(s):return max(1,(s.T+s.stockval())/s.shares)
def sim(seed,params=None):
  global P
  P0=P;P=dict(P0,**(params or {}));rng=random.Random(seed)
  try:
    deal=lineup(rng) if P['random_lineup'] else (lineup10() if P['lineup10'] else fixed_lineup())
    makers={m:Maker(m,rng,deal[m]) for m in D['makers']}
    st=dict(failures=[],replacements=[],tweaks=0,crazes=0,spikes=0,div=0,ore_cr=0.0,ore_units=0,ore_at={},launch=0,sales=0,sales_sys=0,sales_std=0,
            station_std=0,faction_std=0,projects=[],launches=[],news=[],issues=[],pw_buys={},div_k=[],politics=[],ratings=[],war_min={},kind_sales={},sab=0,sab_hit=0,spy=0,spy_hit=0,missions={},gtime=[],std_kind={},events=[],rev_g={g:0.0 for g in GRADES},sales_g={g:0 for g in GRADES},min_margin=9,ceo_changes=[],opened=0,lost=0)
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
    def buy(role,where,kind=None,mult=1.0,ai=False,pw=None):
      if kind:k=kind
      elif pw and P['tastes']:sl=RSLOTS[role];wa=role=='fighter' and at_war(pw);k=rng.choices(sl,[TASTE[pw]['kinds'].get(x,1.0)*(P['mine_k'] if role=='miner' and x in MINE_K else 1)*(P['war_kinds'] if wa and x in WAR_KINDS else 1) for x in sl])[0]
      elif role=='miner':sl=RSLOTS[role];k=rng.choices(sl,[P['mine_k'] if x in MINE_K else 1 for x in sl])[0]
      else:k=rng.choice(RSLOTS[role])
      if k not in COMP or (k=='drill' and role!='miner'):return
      gb=rng.choices(GRADES,P['gb_ai'] if ai else P['gb_other'])[0]
      cands=[(mk,L) for mk in makers.values() if mk.alive and (where is None or P['all_ports'] or mk.sid in where or (P['all_freeports'] and any(x in FREEPORTS for x in where))) for L in mk.lines if L.kind==k and L.active and L.g<=gb and L.stock[L.g]>0]
      if not cands and P['faction_std']:st['faction_std']+=1;return
      if not cands:
        # the station's own standard parts (the old way), or nothing
        if P['station_std']:st['station_std']+=1
        else:st['lost']+=1
        return
      xs=[];ref=COMP[k][1]*LIST_K*P['markup']
      if P['price_sens']:
        wl=P['wealth']['power' if pw else 'contractor' if ai else 'other'];wc=rng.choices(('strapped','steady','flush'),wl)[0];al=P['sens'][wc]
      for mk,L in cands:
        if P['price_sens']:x=(1+pvalue(L.tr,role,pw)+gval(L.kind,L.g,role,pw))/((L.price(L.g,mk)/ref)**al)+(P['loyal'] if where and mk.sid==where[0] else 0)
        else:x=(1+pvalue(L.tr,role,pw)+gval(L.kind,L.g,role,pw))/(L.pm*mk.listk())+(P['loyal'] if where and mk.sid==where[0] else 0)
        if L.craze>0:x*=P['craze_k']
        xs.append(P['beta']*x)
      # the faction's standard part is always there to choose instead, at list price
      if P['faction_std']:xs.append(P['beta']*1.0)
      mx=max(xs);sc=[math.exp(v-mx) for v in xs];t=sum(sc);r=rng.random()*t;i=0
      while r>sc[i]:r-=sc[i];i+=1
      n=len(xs)
      for j,(mk2,L2) in enumerate(cands):L2.ev.append((now,1/n,j==i));mk2.evlog.append((now,1/n,j==i))
      for mk2 in makers.values():
        if mk2.alive and any(L2.kind==k and L2.active and not L2.std and L2.stock[L2.g]==0 for L2 in mk2.lines):mk2.oos.append(now)
        if mk2.alive and any(L2.kind==k and L2.active and not L2.std for L2 in mk2.lines):mk2.asked.append(now)
      if i>=len(cands) and P['price_sens']:st.setdefault('buy_cls',{}).setdefault(wc,{});st['buy_cls'][wc]['standard']=st['buy_cls'][wc].get('standard',0)+1
      if i>=len(cands):st['faction_std']+=1;st['std_kind'][k]=st['std_kind'].get(k,0)+1;return
      mk,L=cands[i];g=L.g
      if P['price_sens']:st.setdefault('buy_cls',{}).setdefault(wc,{});k2=('clear' if L.clear else 'budget' if L.budget else 'grade 1' if L.g==1 else 'new grade');st['buy_cls'][wc][k2]=st['buy_cls'][wc].get(k2,0)+1
      if pw:st['pw_buys'].setdefault(pw,{});st['pw_buys'][pw][mk.m]=st['pw_buys'][pw].get(mk.m,0)+1
      pr=(L.price(g,mk)*pay_k(where) if L.clear else max(L.price(g,mk)*pay_k(where),L.lst(g,mk)*L.floor(mk)*L.md))*mult;L.md=min(1.0,L.md*P['md_back']);L.stock[g]-=1;L.sold.append(now);L.sold_g[g]+=1;net=pr*(1-P['dues']);mk.T+=net;mk.rev+=net
      if P.get('log'):st.setdefault('log',[]).append((now,mk.m,net,mk.ck,L.comp(g),L.kind))
      mk.op+=net-L.comp(g)*L.ckavg;mk.sales_t.append(now)
      m=net/(L.comp(g)*L.ckavg)-1;st['min_margin']=min(st['min_margin'],m);st['sales']+=1;st['rev_g'][g]+=net;st['sales_g'][g]+=1
      st['kind_sales'][L.kind]=st['kind_sales'].get(L.kind,0)+1
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
    def outsold(L,mk):
      # the best-selling rival maker's line of this kind has sold at least out_ratio times as many, and out_min more, in
      # the maker's review window
      if not P['outsold']:return False
      w=now-mk.window();own=sum(1 for t in L.sold if t>w)
      best=max((sum(1 for t in L2.sold if t>w) for m2 in makers.values() if m2.alive and m2 is not mk for L2 in m2.lines if L2.kind==L.kind and L2.active and not L2.std),default=0)
      return best>=P['out_ratio']*own and best>=own+P['out_min']
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
          opts.append((appeal8(L.kind,t3),t3))
      if cur_w:
        wp=weakness(L.tr)
        for wk,sg in K['weak']:
          if wk in cur_w or (wk in L.tr and ((L.tr[wk]>0)!=(sg>0))):continue
          t={k:v for k,v in L.tr.items() if k not in cur_w};add=max(10,math.ceil(wp/10)*10) if wk=='mag' else wp
          t[wk]=rnd2(sg*to_val(wk,add),wk);opts.append((appeal8(L.kind,t),t))
      if not opts:return False
      opts.sort(key=lambda x:-x[0]);L.tr=opts[0][1];L.trs.append(dict(L.tr));return True
    def news(mk,k):
      if mk.alive:mk.mp*=1+P['news'][k];st['news'].append((now,mk.m,k))
    # the powers' politics (v14): each pair drifts between peace, tension and war
    PAIRS=[(a,b) for i,a in enumerate(POWERS) for b in POWERS[i+1:]];REL={p:'peace' for p in PAIRS}
    WAR_KINDS={'gun','laser','missile','torpedo','weapon','armor','shield'}
    def at_war(f):return P['politics'] and any(v=='war' and f in p for p,v in REL.items())
    def tense(f):return P['politics'] and any(v=='tension' and f in p for p,v in REL.items())
    def exposure(mk):
      ls=[L for L in mk.lines if L.active and not L.std];return sum(1 for L in ls if L.kind in WAR_KINDS)/len(ls) if ls else 0
    def pol_news(k):
      for mk in makers.values():
        if not mk.alive:continue
        e=exposure(mk);civ={'war':'civil_war','peace':'civil_peace'}.get(k)
        f=P['war_news'][k]*e+(P['war_news'][civ]*(1-e) if civ else 0);mk.mp*=1+f;st['news'].append((now,mk.m,'pol_'+k))
    def new_ceo(mk,why):
      old=mk.ceo;mk.ceo=rng.choice([c for c in CEOS if c!=old]);[setattr(L,'pm',max(L.pm,L.floor(mk))) for L in mk.lines if not L.clear];mk.ceo_since=now;mk.ceo_peak=None;mk.ceos.append((now,mk.ceo,why));st['ceo_changes'].append((now,mk.m,old,mk.ceo,why));news(mk,'ceo')
    def diagnose(mk):
      w=now-P['diag'];E=[e for e in mk.evlog if e[0]>w];got=sum(1 for e in E if e[2]);exp=sum(e[1] for e in E)
      ls=[L for L in mk.lines if L.active and not L.std and not L.clear]
      kinds={L.kind for L in ls}
      og=sum(1 for k in kinds if max((L2.g for m2 in makers.values() if m2.alive and m2 is not mk for L2 in m2.lines if L2.kind==k and L2.active),default=0)>max(L.g for L in ls if L.kind==k))
      tw=sum(1 for L in ls if L.tweaks>=P['max_tweaks'])
      dear=[];
      for L in ls:
        r=[L2.price(L2.g,m2) for m2 in makers.values() if m2.alive and m2 is not mk for L2 in m2.lines if L2.kind==L.kind and L2.active and L2.g==L.g]
        if r:dear.append(L.price(L.g,mk)/(sum(r)/len(r)))
      ask=sum(1 for t in mk.asked if t>w);oos=sum(1 for t in mk.oos if t>w)
      d=dict(share=round(got/exp,2) if exp else 0,outgraded=og,kinds=len(kinds),tweaked_out=tw,lines=len(ls),dear=round(sum(dear)/len(dear),2) if dear else 1.0,oos=round(oos/ask,2) if ask else 0,
             stock=round(sum(L.comp(g)*n for L in mk.lines for g,n in L.stock.items())),rd=bool(mk.proj),ceo=mk.ceo,age=now-mk.born)
      if d['share']>=.9:c='cash flow (selling its share)'
      elif d['oos']>=.3:c='out of stock'
      elif og and og>=len(kinds)/2:c='out-graded'
      elif d['dear']>=1.1:c='too dear'
      elif tw:c='tweaks did not win buyers back'
      else:c='losing on stats (before its tweaks ran out)'
      d['cause']=c;st.setdefault('diag',[]).append(d)
    for now in range(int(P['hours']*60)):
      # galaxy events
      EV=[e for e in EV if e['t1']>now]
      if P['events'] and rng.random()<1/P['event_every']:
        k=rng.choices(list(EVENTS),[v['w'] for v in EVENTS.values()])[0];tgt=rng.choice(POWERS) if EVENTS[k]['power'] else None
        if not ev_on(k,tgt):e=dict(k=k,tgt=tgt,t0=now,t1=now+rng.randint(*P['event_len']));EV.append(e);st['events'].append(e)
      for mk in makers.values():mk.ck=cost_k(mk.sid)
      # a wealthy pilot buying one line in bulk (experiment; off unless P['whale'] is set): from t0 to t1 they buy every
      # unit on the shelf, up to `rate` an hour, at the shelf price; it counts as a sale like any other
      W=P.get('whale')
      if W and W['t0']<=now<W['t1']:
        mk=makers[W['m']];Lw=next((L for L in mk.lines if L.kind==W['kind'] and L.active),None) if mk.alive else None
        ws=st.setdefault('whale',dict(units=0,spend=0.0,list=0.0))
        if Lw and Lw.stock[Lw.g]>0 and rng.random()<W['rate']/60:
          g=Lw.g;pr=Lw.price(g,mk);Lw.stock[g]-=1;Lw.sold.append(now);Lw.sold_g[g]+=1;net=pr*(1-P['dues']);mk.T+=net;mk.rev+=net
          mk.op+=net-Lw.comp(g)*Lw.ckavg;mk.sales_t.append(now);Lw.ev.append((now,1.0,True))
          ws['units']+=1;ws['spend']+=pr;ws['list']+=Lw.lst(g,mk)
          if Lw.stock[g]==0:Lw.sellouts.append(now);Lw.sellout_rev=True
      if W and now in (W['t0'],W['t1']):st.setdefault('whale_snap',{})[now]=st['std_kind'].get(W['kind'],0)
      if W and now==W['t1']:st['whale_pm']={m2.m:round(L.pm,3) for m2 in makers.values() if m2.alive for L in m2.lines if L.kind==W['kind'] and L.active}
      # bulk orders (v17 experiment, off unless P['orders'] is set): a faction places an order for `units` of a maker's line
      # at time t0, paying list + order_premium, half up front; the maker gives the order up to order_share of its works
      # ticks until it is filled. Finished units are set aside for the buyer (not sold on the shelf; no craze, no rival
      # tweaks), paid in full on completion. Missions are counted from the order (see BEYOND_DESIGN.md).
      OR=st.setdefault('_orders',[dict(o,done=0,paid=0.0,t_done=None,started=False) for o in (P['orders'] or [])])
      for o in OR:
        if now>=o['t0'] and not o['started']:
          mk=makers[o['m']];Lo=next((L for L in mk.lines if L.kind==o['kind'] and L.active and not L.clear and not L.budget),None)
          if Lo:o['started']=True;o['L']=Lo;o['price']=Lo.lst(Lo.g,mk)*(1+P['order_premium']);dep=o['price']*o['units']*P['order_deposit'];o['escrow']=dep*(1-P['dues']);o['paid']+=dep
      busy=set()
      if now%max(1,int(P['works_every']))==0:
        for o in OR:
          if o['started'] and o['t_done'] is None and makers[o['m']].alive and rng.random()<P['order_share']:
            mk=makers[o['m']];L=o['L'];c=L.comp(L.g)*mk.ck
            # the deposit is held for the order and pays for its components first; then the maker's own money, keeping
            # its reserve
            if o['escrow']>=c:o['escrow']-=c;o['done']+=1;busy.add(mk.m)
            elif mk.T-(c-o['escrow'])>=mk.reserve()*mk.upkeep_h():mk.T-=c-o['escrow'];o['escrow']=0.0;o['done']+=1;busy.add(mk.m)
            if o['done']>=o['units'] and o['t_done'] is None:
              # paid in full; a one-off for investors (cash, not the earnings they multiply)
              o['t_done']=now;rest=o['price']*o['units']-o['paid'];mk.T+=rest*(1-P['dues'])+o['escrow'];o['escrow']=0.0;o['paid']+=rest
      # works: build the emptiest shelf it can afford, keeping its reserve
      if now%max(1,int(P['works_every']))==0:
        for mk in makers.values():
          if not mk.alive or mk.m in busy or (slow(mk.sid) and now%(2*max(1,int(P['works_every'])))):continue
          opts=sorted(((L.stock[g]/P['cap'][g],g,id(L),L) for L in mk.lines if L.active and not L.clear and not L.shut for g in GRADES if g==L.g and L.stock[g]<min(P['cap'][g],1+sum(1 for t in L.sold[-12:] if t>now-P['pace']))),key=lambda x:(x[0],x[1]))
          for _,g,_,L in opts:
            c=L.comp(g)*mk.ck
            if mk.T-c>=mk.reserve()*mk.upkeep_h():u=L.units();L.ckavg=(L.ckavg*u+mk.ck)/(u+1);mk.T-=c;L.stock[g]+=1;break
      for mk in makers.values():
        if mk.alive:mk.T-=mk.upkeep_h()/60;mk.op-=mk.upkeep_h()/60
        if mk.alive and P['store_h']:
          sc=sum(L.comp(g)*n for L in mk.lines if L.active for g,n in L.stock.items())*P['store_h']/60;mk.T-=sc;mk.op-=sc;st['storage']=st.get('storage',0)+sc
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
              st['sab_hit']+=1;news(mk,'sabotaged')
              if pj['stage']=='design':pj['t']+=20
              elif pj['stage']=='materials':pj['t']=now+rng.randint(*P['rd_mat'])
              else:pj['t']=now+rng.randint(*P['rd_trial'])
          if rng.random()<P['spy_h']/60:
            st['spy']+=1;mis('espionage')
            # spying speeds up the spy's own R&D: its current project, or a head start on its next one
            rp=r.proj;st['spy_hit']+=1;news(r,'spied')
            if rp:rp['t']-=max(0,(rp['t']-now)*.25)
            else:r.intel.add('any')
        if now>=pj['t']:
          if pj['stage']=='design':pj['stage']='materials';pj['t']=now+rng.randint(*P['rd_mat']);mis('materials run');mis('rare ore')
          elif pj['stage']=='materials':pj['stage']='trials';pj['t']=now+rng.randint(*P['rd_trial']);mis('prototype escort');mis('test flight')
          else:
            # launch: the old line is retired at once; its stock goes back to raw ore in the station that holds it
            L=pj['L']
            if P['old'] in ('clear','budget'):
              # the old grade stays on the market (v17): as a budget line, or its stock on clearance
              for Lo in [x for x in mk.lines if x.kind==L.kind and x.budget and x.active]:
                Lo.budget=False;Lo.clear=True;Lo.pm=P['clear_pm'];Lo.t_clear=now
                if Lo.units()==0:Lo.active=False
              Ln=Line(L.kind,False,L.tr);Ln.g=L.g;Ln.stock=dict(L.stock);Ln.ckavg=L.ckavg;Ln.trs=list(L.trs);Ln.t_clear=now
              if P['old']=='budget':Ln.budget=True;Ln.pm=P['budget_pm']
              else:Ln.clear=True;Ln.pm=P['clear_pm']
              if Ln.units()>0 or Ln.budget:mk.lines.append(Ln)
              st.setdefault('old_lines',[]).append((now,mk.m,L.kind,L.g,Ln.units()))
            else:
              u=L.units();v=sum(ORE[L.kind][g]*n for g,n in L.stock.items());st['ore_units']+=u;st['ore_cr']+=v;st['ore_at'][mk.sid]=st['ore_at'].get(mk.sid,0)+v
            L.g=pj['g'];L.stock={g:0 for g in GRADES};L.tr=mk.roll(L.kind);L.trs.append(dict(L.tr));L.tweaks=0;L.gen+=1;L.last_tw=now;L.ev=[];L.pm=1.0;L.sold=[];L.active=True;L.ckavg=1.0
            st['launches'].append((now,mk.m,L.kind,L.g,now-pj['t0']));mk.fresh+=P['pipe_k']*pj['cost']*P['pipe_stage']['trials']+P['fresh_k']*pj['cost'];mk.ev_ref=getattr(mk,'ev_last',0.0);mk.proj=None;mis('launch delivery');news(mk,'launch')
      if P['politics'] and now%5==0 and now>0:
        R_=P['pol_rates']
        for p in PAIRS:
          v=REL[p];u=rng.random();nv=v
          if v=='peace' and u<R_['tension']/12:nv='tension'
          elif v=='tension':nv='war' if u<R_['war']/12 else ('peace' if u<(R_['war']+R_['calm'])/12 else v)
          elif v=='war' and u<R_['peace']/12:nv='peace'
          if nv!=v:
            REL[p]=nv;st['politics'].append((now,p,nv))
            if nv=='tension':pol_news('tension')
            elif nv=='war':pol_news('war')
            elif v=='war':pol_news('peace')
        for f in POWERS:
          if at_war(f):st['war_min'][f]=st['war_min'].get(f,0)+5
      if now%5==0:
        # investors' mood: the whole market's, and each company's, drift slowly and revert
        mkt_mood=st.setdefault('_mood',0.0)*P['mood_keep']+P['market_sd']*rng.gauss(0,1);st['_mood']=mkt_mood
        for mk in makers.values():
          if not mk.alive:continue
          mk.mood=mk.mood*P['mood_keep']+P['mood_sd']*rng.gauss(0,1);mk.fresh*=P['fresh_decay']
          if P['fresh_mode']=='earn' and mk.fresh>0 and getattr(mk,'ev_ref',None) is not None and mk.ev_last>mk.ev_ref:mk.fresh=max(0.0,mk.fresh-(mk.ev_last-mk.ev_ref));mk.ev_ref=mk.ev_last
          mk.E=(1-P['e_a'])*mk.E+P['e_a']*(mk.op*12);mk.op=0;mk.div_ema=(1-P['d_a'])*mk.div_ema+P['d_a']*(mk.div_recent*12);mk.div_recent=0
          mk.nobs+=1;Eu=(mk.E+P['e_prior']*(1-P['e_a'])**mk.nobs if P['debias']=='prior' else mk.E/(1-(1-P['e_a'])**mk.nobs)) if P['debias'] else mk.E;Du=(mk.div_ema if P['debias']=='prior' else mk.div_ema/(1-(1-P['d_a'])**mk.nobs)) if P['debias'] else mk.div_ema
          mk.sales_t=[t for t in mk.sales_t if t>now-240];s1=sum(1 for t in mk.sales_t if t>now-120);s0=len(mk.sales_t)-s1
          graw=P['g_w']*max(-.5,min(.5,s1/s0-1)) if s0>0 and now>=240 else 0
          mk.gs=(1-P['g_a'])*mk.gs+P['g_a']*graw;g=mk.gs;mk.Eu=Eu
          book=(mk.T+mk.stockval())/mk.shares
          ev=Eu*P['mkt_H']*(1+g) if Eu>0 else Eu*P['mkt_H']*.5
          mk.ev_last=ev
          pj=mk.proj;pipe=P['pipe_k']*pj['cost']*P['pipe_stage'][pj['stage']] if pj else 0
          mk.V=max(.5,book+(ev+pipe+mk.fresh+Du*P['div_H'])/mk.shares)
          tgt=mk.V*math.exp(mk.mood+mkt_mood)
          # before the market opens (the first hour) the listing price is the average value so far
          if now<=P['listing'] and mk.nobs==now//5+1:mk.lsum+=tgt;mk.mp=mk.mp_prev=mk.lsum/mk.nobs
          else:
            nmp=mk.mp+P['kappa']*(tgt-mk.mp)+P['mu']*(mk.mp-mk.mp_prev)+P['sigma']*mk.mp*rng.gauss(0,1)
            mk.mp_prev=mk.mp;mk.mp=max(.5,nmp)
          mk.mkt.append((now,round(mk.mp,2),round(mk.V,2),round(book,2),round(Eu),round(g,2),round((pipe+mk.fresh)/mk.shares,2),round(Du*P['div_H']/mk.shares,2),round(mk.mood+mkt_mood,3),round(mk.dps,3),mk.gen))
      if P['rating'] and now%60==0 and now>=P['listing']:
        for mk in makers.values():
          if not mk.alive:continue
          mk.an=mk.an*P['an_keep']+P['an_sd']*math.sqrt(1-P['an_keep']**2)*rng.gauss(0,1)
          r_=mk.V*math.exp(mk.an)/mk.mp;rt=2 if r_>=1.25 else 1 if r_>=1.08 else 0 if r_>.93 else -1 if r_>.8 else -2
          mk.rating=rt;st['ratings'].append((now,mk.m,rt,mk.gen))
      if now%60==0:
        gs=[L.g for mk in makers.values() for L in mk.lines]
        st['gtime'].append((now,max(gs),sum(gs)/len(gs),sum(1 for x in gs if x>=2)/len(gs)))
      if P['refits']:
        for f in POWERS:
          wk=P['war_fit'] if at_war(f) else (P['tension_fit'] if tense(f) else 1.0);ck=P['war_civil'] if at_war(f) else 1.0
          for _ in range(poisson(P['refit_per_h']*P['refit_parts']*refit_k(f)*wk/60)):buy('fighter',[HOME_SID[f]]+FREEPORTS,ai=True,pw=f)
          # the powers' mining fleets refit too (v11)
          for _ in range(poisson(P['miner_refit'].get(f,0)*P['refit_parts']*refit_k(f)*ck/60)):buy('miner',[HOME_SID[f]]+FREEPORTS,ai=True,pw=f)
          for _ in range(poisson(P['hauler_refit'].get(f,0)*P['refit_parts']*refit_k(f)*ck/60)):buy('hauler',[HOME_SID[f]]+FREEPORTS,ai=True,pw=f)
          for _ in range(poisson(P['scout_refit'].get(f,0)*P['refit_parts']*refit_k(f)/60)):buy('scout',[HOME_SID[f]]+FREEPORTS,ai=True,pw=f)
      for _ in range(poisson(P['contractor_per_h']/60)):
        role=rng.choices(['fighter','hauler','miner','scout'],[.6 if ev_on('war scare') or any(v=='war' for v in REL.values()) else .4,.3,.25,.05])[0]
        sites=FREEPORTS+['hp','vb','os'];w=[(2 if s in OWN and ev_on('feast',OWN[s]) else 1)*(.5 if s in OWN and ev_on('plague',OWN[s]) else 1) for s in sites]
        buy(role,[rng.choices(sites,w)[0]])
      for _ in range(poisson(P['merchant_per_h']/60)):
        role=rng.choices(['fighter','hauler','miner','scout'],[.45,.3,.2,.05])[0];buy(role,None)
      for _ in range(poisson(P['player_per_h']/60)):buy(rng.choice(['fighter','hauler','miner']),None)
      if rng.random()<1/P['spike_every']:
        k=rng.choice(CORP_KINDS);spike.append((k,now+P['spike_len']));st['spikes']+=1
        for mk in makers.values():
          for L in mk.lines:
            if L.kind==k and (not L.active or L.shut) and not L.clear and mk.alive:L.active=True;L.shut=False
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
            if L.clear:
              if L.units()==0:L.active=False
              elif now-max([getattr(L,'t_clear',0)]+L.sold)>=P['retire']:
                u=L.units();v=sum(ORE[L.kind][g]*n for g,n in L.stock.items());st['ore_units']+=u;st['ore_cr']+=v;st['ore_at'][mk.sid]=st['ore_at'].get(mk.sid,0)+v;L.stock={g:0 for g in GRADES};L.active=False
              continue
            if L.units()>0 and now-max([getattr(L,'t_md',0)]+L.sold)>=P['stale']:L.md=max(P['md_min'],L.md*P['md_step']);L.t_md=now-P['stale']+P['review'];st['markdowns']=st.get('markdowns',0)+1
            if L.shut:
              if L.units()==0:L.active=False;L.shut=False
              continue
            got,exp=share(L,mk)
            dl=disliked(L,mk) if P['out_dislike'] else False;os_=(not L.std) and outsold(L,mk)
            if any(t>now-60 for t in L.sold) and not dl and not os_:
              fl=L.floor(mk);cap=1.3 if mk.ceo=='Discounter' else P['pm_max']
              if L.sellout_rev or (exp>=1 and got>=P['hot']*exp):L.pm=min(cap,L.pm*P['up'])
              elif got<exp and L.full() and L.pm>fl+1e-9:L.pm=max(fl,L.pm*P['down'])
            elif L.budget:pass
            elif not L.std and os_ and not dl and not P['out_rd']:
              # answering a rival: a tweak, as often as every out_cool minutes, never by itself an R&D project
              if now-L.last_tw>=P['out_cool'] and tweak(L,mk):L.last_tw=now;st['tweaks']+=1;L.ev=[];news(mk,'tweak');st.setdefault('tweak_log',[]).append((now,mk.m,L.kind,'outsold'))
            elif not L.std and (dl or os_) and now-L.last_tw>=mk.settle():
              if L.tweaks<P['max_tweaks']:
                if tweak(L,mk):L.tweaks+=1;L.last_tw=now;st['tweaks']+=1;L.ev=[];news(mk,'tweak');st.setdefault('tweak_log',[]).append((now,mk.m,L.kind,'outsold' if os_ and not dl else 'disliked' if dl and not os_ else 'both'))
              elif P['issue'] and mk.proj is None and L.g<5 and mk.issued<P['issue_max']*P['shares'] and mk.mp>3 and mk.T-P['rd_cost'][L.g+1]<max(mk.reserve(),P['rd_reserve'])*mk.upkeep_h():
                # not enough money: issue new shares to fund the project (diluting the old ones)
                need=P['rd_cost'][L.g+1]+max(mk.reserve(),P['rd_reserve'])*mk.upkeep_h()-mk.T;n=min(math.ceil(need/(.95*mk.mp)),int(P['issue_max']*P['shares']-mk.issued))
                if n>0:mk.T+=n*.95*mk.mp;mk.shares+=n;mk.issued+=n;st['issues'].append((now,mk.m,n,round(mk.mp,1)))
              elif mk.proj is None and L.g<5 and mk.T-P['rd_cost'][L.g+1]>=max(mk.reserve(),P['rd_reserve'])*mk.upkeep_h():
                # R&D: fund a project for the next grade of this kind
                ng=L.g+1;c=P['rd_cost'][ng];mk.T-=c;d=P['rd_design'][ng]*(.7 if 'any' in mk.intel else 1);mk.intel.discard('any')
                mk.proj=dict(L=L,g=ng,stage='design',t=now+d,t0=now,cost=c);st['projects'].append((now,mk.m,L.kind,ng,'outsold' if os_ and not dl else 'disliked' if dl and not os_ else 'both'));replaced=True;news(mk,'project')
            L.sellout_rev=False
            if P['retire'] and L.active and now>P['retire'] and not [t for t in L.sold if t>now-P['retire']] and L.full():
              if P['shut_sell']:L.shut=True;st['shut']=st.get('shut',0)+1
              else:L.active=False
          # an Expansionist opens a new line when rich
          if mk.ceo=='Expansionist' and mk.T>2*P['start'] and mk.extra<3:
            have={(L.kind,L.std) for L in mk.lines};ks=[k for k in CORP_KINDS if (k,False) not in have and (k,True) not in have]
            if ks:k=rng.choice(ks);mk.lines.append(Line(k,False,mk.roll(k)));mk.extra+=1;mk.T-=P['launch'];st['opened']+=1
          mk.struggling=mk.T<P['struggle_h']*mk.upkeep_h()
          if prof>0 and not mk.struggling:
            avgE=sum(max(0,x.Eu) for x in makers.values() if x.alive)/max(1,sum(1 for x in makers.values() if x.alive))
            d=prof*mk.divk(avgE);mk.T-=d;mk.div_paid+=d;st['div']+=d;mk.div_recent+=d;mk.dps+=d/mk.shares;st['div_k'].append((now,mk.m,round(mk.divk(avgE),3)))
          px=mk.mp;mk.share_px.append((now,px,mk.div_paid/mk.shares))
          # the board: a product line failed, or the shares fell far below their peak under this CEO
          if P['ceo'] and P['ceo_mode']=='streak':
            # the board: the share price has fallen several periods in a row (v15)
            if now%P['ceo_period']==0:
              last=getattr(mk,'ceo_last',None);mk.ceo_last=px
              mk.fall=(getattr(mk,'fall',0)+1) if last is not None and px<last else 0
              if mk.fall>=P['ceo_streak'] and now-mk.ceo_since>=P['ceo_cool']:new_ceo(mk,'shares');mk.fall=0
          elif P['ceo']:
            mk.ceo_peak=max(mk.ceo_peak or px,px)
            if now-mk.ceo_since>=P['ceo_cool']:
              if replaced and P['ceo_on_replace']:new_ceo(mk,'line')
              elif px<P['ceo_drop']*mk.ceo_peak:new_ceo(mk,'shares')
      for m,mk in list(makers.items()):
        if mk.alive and mk.T<=0:
          diagnose(mk);mk.alive=False;mk.failed_at=now;mk.mp=0;mk.mkt.append((now,0,0,0,0,0,0,0));st['failures'].append((now,m,mk.name,mk.ceo));mk.rebirth=now+rng.randint(*P['replace'])
        if not mk.alive and now>=getattr(mk,'rebirth',1e9):
          nm=Maker(m,rng,[(L.kind,L.std) for L in mk.lines if not L.clear and not L.budget]);mk.proj=None;nm.born=now;nm.gen=mk.gen+1;makers[m]=nm
          # the company's history carries on: its shares were worth nothing while it was gone
          nm.share_px=mk.share_px+[(mk.failed_at,0,mk.div_paid/mk.shares)];nm.mkt=mk.mkt+[(now,round(nm.mp,2),round(nm.mp,2),round(nm.mp,2),0,0,0,0)];nm.ceos=mk.ceos+[(now,nm.ceo,'new company')];nm.div_paid=0
    lines=[(mk.m,L.kind,L.std,L.tweaks,L.gen,L.tr,round(L.pm,3),len(L.sold),L.trs,L.g) for mk in makers.values() for L in mk.lines]
    st['orders_out']=[dict(m=o['m'],kind=o['kind'],units=o['units'],t0=o['t0'],done=o['done'],t_done=o['t_done']) for o in st.get('_orders',[])]
    return dict(st,T={m:round(mk.T) for m,mk in makers.items()},struggling={m:mk.struggling for m,mk in makers.items()},
                divm={m:round(mk.div_paid) for m,mk in makers.items()},rev={m:round(mk.rev) for m,mk in makers.items()},rev_sys={m:round(mk.rev_sys) for m,mk in makers.items()},
                px={m:mk.share_px for m,mk in makers.items()},ceos={m:mk.ceos for m,mk in makers.items()},mkt={m:mk.mkt for m,mk in makers.items()},shares={m:mk.shares for m,mk in makers.items()},deal={m:deal[m] for m in deal},lines=lines)
  finally:
    P=P0
if __name__=='__main__':
  import time;t=time.time();r=sim(1)
  print(round(time.time()-t,1),'s',{k:r[k] for k in ('failures','tweaks','crazes','spikes','ore_cr','ore_units','sales','sales_sys','sales_std','min_margin','opened','lost','sales_g')},len(r['replacements']),len(r['ceo_changes']))
  print(r['T']);print({m:[c[1] for c in v] for m,v in r['ceos'].items()})
  print({k:v for k,v in COMP.items()})
