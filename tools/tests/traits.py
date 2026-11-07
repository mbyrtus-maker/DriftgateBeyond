# Beyond: traits on every AI entity. The powers' leaders (14 traits) and the Dread Pirate (8) set how each side's AI pilots
# fly (LEADP, through findHostile and npcThink) and how their leaders choose events, successors, audiences and stand-ins.
# This test sweeps every trait on every side and checks:
#   names    every trait named in a table or a hasT/rgHas/dpHas/includes call exists (catches typos that silently do nothing)
#   profile  each single trait gives the profile the design says; any two blend (ranges multiply, Vengeful never breaks off,
#            the rest take the larger break-off, flags OR); no profile field is set but never read
#   rolls    starting rolls: two different valid traits, no shared pair; neutral mode gives none and a plain profile
#   events   evWeight is finite, and 0 exactly when a trait forbids the event
#   live     in a live system, for each power and the Unbound: reach scales with the trait, Ruthless picks the miner,
#            Zealous the Brood, Honourable leaves a jammed-dark ship; break-off by hull for every combat role; which AI
#            roles the traits actually reach
#   succession  a killed leader's successor is Vengeful with a grudge, an ousted one shares none of the old traits, the
#            Dread Pirate's successor; profiles follow at once
#   save     a galaxy saved and continued in a fresh tab keeps its pilots' trait profiles
#   hour     an hour of strategy with rolled leaders: every leader keeps two valid traits and LEADP never goes stale
# Lines start PASS, FAIL or GAP. FAIL is a bug and goes in the errors list. GAP is designed behaviour not built yet (the
# design table in BEYOND_DESIGN.md 11c/12c says pilots do it, nothing in the code does): printed, not an error.
import asyncio,json,os,re,itertools
from playwright.async_api import async_playwright
HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.join(HERE,'..','..')
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(ROOT,'index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-3)b.push('cr:'+(l.credits-S.ledger0.credits).toFixed(2));return b.length?'LEAK '+b.join(' '):'exact'})()"""

# what each single trait does to a side's pilots, as built (16g_leaders.js leaderProfiles, 16zc_dread.js dpProfile)
BASE={'range':1,'breakoff':0,'honour':False,'ruthless':False,'zeal':False}
POWER={'Ambitious':{'range':1.3},'Opportunist':{'range':1.15},'Cautious':{'range':.85,'breakoff':.3},'Patient':{'range':.9},
  'Isolationist':{'range':.9},'Mercantile':{'breakoff':.2},'Vengeful':{'breakoff':0},'Honourable':{'honour':True},
  'Ruthless':{'ruthless':True},'Zealous':{'zeal':True},'Scheming':{},'Wary':{},'Loyal':{},'Industrious':{}}
PIRATE={'Bloodthirsty':{'range':1.3},'Showman':{'range':1.15},'Cunning':{'range':.9},'Paranoid':{'range':.8,'breakoff':.25},
  'Superstitious':{'breakoff':.3},'Greedy':{'honour':True,'ruthless':True},'Gallant':{'honour':True},'Kingmaker':{}}
# the design's pilot behaviour for traits whose profile is plain (BEYOND_DESIGN.md 11c / 12c tables)
DESIGN_GAP={'Scheming':'hit and run, pick off isolated ships, ambush at gates','Wary':'keep their distance from allied ships; patrols scan more',
  'Loyal':'answer allies\' distress calls; guard allied convoys','Industrious':'guard miners and constructors first',
  'Mercantile':'guard convoys and traders before miners and outposts (only the break-off is built)',
  'Patient':'hold positions, wait for reinforcements, attack late and in force (only the shorter reach is built)',
  'Kingmaker':'raid whichever power leads the galaxy (events only; pilots fly plain)',
  'Opportunist':'strike whoever is weakest, join fights as a third party (only the longer reach is built)',
  'Bloodthirsty':'finish jammed ships, hit escorts and patrols (only the longer chase is built; a hurt Bloodthirsty ship breaks off when its other trait says so, user 7 Nov 2026)'}
# ---- pilot traits (agreed 7 Nov 2026, BEYOND_DESIGN.md "Pilot traits"): one trait per AI ship, under its leader's style.
# Starting pools by role, and the trait a pilot who comes back (aces, independents) learns from how it died. The Brood have none.
PILOT_START={'universal':['Steady','Skittish','Unpredictable','Loyal','Greedy'],
  'fighter':['Hotshot','Sniper','Opportunist','Duelist','Guardian','Lone Wolf','Rock Hopper'],
  'scout':['Ghost','Thrill Seeker','Bait','Shadow','Tripwire'],
  'bomber':['Big Game Hunter','Patient','Kamikaze-ish','Precision','Hit and Run'],
  'miner':['Prospector','Homebody','Hoarder','Efficient','Rock Diver'],
  'hauler':['Speed Demon','Safe Routes','Convoy Lover','Overloader','Smuggler'],
  'capital':['Admiral','Brawler Captain','Bastion','Carrier Minded','Glory Seeker','Cautious Commander']}
PILOT_DEATH={'universal':{'an ace or named pilot (combat)':'Vengeful','an ace or named pilot (non-combat)':'Haunted','unknown':'Shaken'},
  'fighter':{'an enemy fighter':'Cautious','a missile or torpedo':'Missile-Wary','capital point defence':'Flak-Shy','outnumbered':'Pack Fighter'},
  'scout':{'ambushed':'Jumpy','its Shadow target':'Long Leash','deep in hostile space':'Edge Walker'},
  'bomber':{'point defence on a run':'Long Launch','intercepted before the run':'Escort Only','escaping after the run':'Quick Exit','the target\'s explosion':'Blast-Aware'},
  'miner':{'pirates or raiders':'Watchful','a full hold':'Light Load','far from base':'Homebody'},
  'hauler':{'ambushed on a route':'Route Changer','hostile space':'Safe Routes','travelling alone':'Convoy Only'},
  'capital':{'bombers or torpedoes':'Screen First','an enemy capital':'Outranged','swarmed by fighters':'Point Defense Doctrine','advancing alone':'Fleet Anchor'}}
PILOT_RARE=['Skittish','Duelist','Lone Wolf','Kamikaze-ish','Glory Seeker']
# names a pilot trait shares with a leader trait: a pilot's trait must never be read as its leader's (or the other way)
def pilot_names():return sorted({t for l in PILOT_START.values() for t in l}|{t for d in PILOT_DEATH.values() for t in d.values()})
PILOT_LEADER_CLASH=sorted(set(pilot_names())&(set(POWER)|set(PIRATE)))

def blend(spec,traits):
  p=dict(BASE)
  for t in traits:
    d=spec[t];p['range']*=d.get('range',1)
    for k in('honour','ruthless','zeal'):p[k]=p[k] or d.get(k,False)
  if 'Vengeful' in traits:p['breakoff']=0
  else:p['breakoff']=max([0]+[spec[t].get('breakoff',0) for t in traits])
  return p
def same(a,b):return all((abs(a[k]-b[k])<1e-9 if isinstance(b[k],float) or isinstance(b[k],int) and not isinstance(b[k],bool) else a[k]==b[k]) for k in BASE)

R={'pass':0,'fail':[],'gap':[]}
def ok(cond,name,detail=''):
  if cond:R['pass']+=1;print('PASS',name)
  else:R['fail'].append(name+(': '+detail if detail else ''));print('FAIL',name,detail)
def gap(name,detail):R['gap'].append(name);print('GAP ',name,'-',detail)

def static_checks():
  src={};d=os.path.join(ROOT,'src','js')
  for f in sorted(os.listdir(d)):
    if f.endswith('.js'):src[f]=open(os.path.join(d,f),encoding='utf8').read()
  alls='\n'.join(src.values())
  T=re.search(r"const TRAITS=\[([^\]]*)\]",alls).group(1);T=re.findall(r"'(\w+)'",T)
  D=re.search(r"const DP_TRAITS=\[([^\]]*)\]",alls).group(1);D=re.findall(r"'(\w+)'",D)
  bad=[]
  for f,s in src.items():
    pat=r"(hasT\([^,()]+,|rgHas\([^,()]+,|traits\.includes\(|\bt\()\s*'([A-Za-z]+)'" if f in('16g_leaders.js','16zc_dread.js') else r"(hasT\([^,()]+,|rgHas\([^,()]+,|traits\.includes\()\s*'([A-Za-z]+)'"
    for m in re.finditer(pat,s):
      if m.group(2) not in T+D:bad.append(f'{f}: {m.group(0)}')
      if m.group(1).startswith(('hasT','rgHas')) and m.group(2) not in T:bad.append(f'{f}: {m.group(0)} (not a power trait)')
    for m in re.finditer(r"dpHas\('([A-Za-z]+)'\)",s):
      if m.group(1) not in D:bad.append(f'{f}: dpHas({m.group(1)}) (not a pirate trait)')
    for m in re.finditer(r"\bsuccession\([^,()]+,'(\w+)'",s):
      if not re.search(r"\b"+m.group(1)+r":\[",src['16g_leaders.js']):bad.append(f'{f}: succession cause {m.group(1)} has no SUCC row')
  ok(not bad,'names: every trait named in a call exists',' | '.join(bad[:6]))
  # profile fields that are set but never read anywhere a profile is used
  users=[s for f,s in src.items() if 'leadP(' in s or 'LEADP' in s]
  for k in('range','breakoff','honour','ruthless','zeal'):
    reads=sum(len(re.findall(r"\bp\."+k+r"\b(?!\s*(?:\*|\|\||&&)?=(?!=))",s)) for s in users)
    ok(reads>0,f'profile field {k} is read somewhere','set by leaderProfiles/dpProfile, never read: the trait that sets it does nothing through it')
  # traits that reach the AI's flying: which think loops use the trait-aware target finder
  for fn in('frigateThink','scoutThink','traderThink','crewThink','defThink','droneThink'):
    m=re.search(r"function "+fn+r"\(e,dt\)\{",alls)
    if not m:continue
    body=alls[m.end():m.end()+6000];body=body[:body.find('\nfunction ')] if '\nfunction ' in body else body
    if 'findHostile' not in body and 'leadP' not in body:print('INFO',fn,'never reads a trait (targets without findHostile/leadP)')
  # pilot traits: every agreed name must be in the code once the build lands (a missing or misspelt one is a trait nobody rolls)
  # built yet? common words (Steady, Ghost, Smuggler, Homebody) already appear elsewhere, so look for the distinctive names
  names=pilot_names();found=[t for t in('Missile-Wary','Flak-Shy','Rock Hopper','Pack Fighter','Point Defense Doctrine','Kamikaze-ish','Big Game Hunter') if re.search(r"['\"]"+re.escape(t)+r"['\"]",alls)]
  if not found:gap('pilot traits','not built yet (no pilot-only trait name in src/js): only the leader layer is tested; extend the pilot section when it lands')
  else:
    miss=[t for t in names if not re.search(r"['\"]"+re.escape(t)+r"['\"]",alls)]
    ok(not miss,f'pilot traits: all {len(names)} agreed names are in the code',' '.join(miss[:12]))
    print('INFO pilot trait names shared with leader traits (keep them apart):',', '.join(PILOT_LEADER_CLASH))
  # a founder's traits (design 11c: pick two when you declare)
  if 'traits' not in src.get('16s_declare.js',''):gap('declared faction traits','a founder picks two traits on declaring and its AI pilots fly by them (not built: only the sleep-mode stand-in has traits)')
  return T,D

async def main():
  T,D=static_checks()
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await ev("(()=>{relInit();dpInit();leaderProfiles();return 1})()")
    async def j(c):
      r=await ev(c)
      try:return json.loads(r)
      except Exception:raise RuntimeError(f'probe returned {r!r}')
    print('start',await ev("JSON.stringify({leaders:FAC_IDS.map(f=>leaderOf(f).traits),dread:S.dread&&S.dread.traits,sides:Object.keys(LEADP)})"))
    pt=await j("JSON.stringify({T:TRAITS,D:DP_TRAITS})")
    ok(sorted(pt['T'])==sorted(POWER),'the power traits match the design list',str(set(pt['T'])^set(POWER)))
    ok(sorted(pt['D'])==sorted(PIRATE),'the pirate traits match the design list',str(set(pt['D'])^set(PIRATE)))

    # ---- names in every table
    n=await j("""(()=>{const bad=[];const chk=(w,l,v)=>{for(const t of l||[])if(!v.includes(t))bad.push(w+':'+t)};
      for(const k in EV_LEAN)chk('EV_LEAN.'+k,EV_LEAN[k],TRAITS);for(const k in EV_NEVER)chk('EV_NEVER.'+k,EV_NEVER[k],TRAITS);
      for(const k in SUCC)chk('SUCC.'+k,SUCC[k],TRAITS);chk('FALL.keepT',FALL.keepT,TRAITS);chk('FALL.razeT',FALL.razeT,TRAITS);
      for(const k in AUD_REQ){chk('AUD_REQ.'+k+'.lean',AUD_REQ[k].lean,TRAITS);chk('AUD_REQ.'+k+'.never',AUD_REQ[k].never,TRAITS)}
      for(const f of FAC_IDS)chk('LEAD0.'+f,LEAD0[f].traits,TRAITS);for(const k in DP_SUCC)chk('DP_SUCC.'+k,DP_SUCC[k],DP_TRAITS);
      for(const k of Object.keys(RG_TXT))if(!TRAITS.includes(k))bad.push('RG_TXT:'+k);
      const where={};for(const t of TRAITS){where[t]=[];if(Object.values(EV_LEAN).some(l=>l.includes(t))||Object.values(EV_NEVER).some(l=>l.includes(t)))where[t].push('events');
        if(Object.values(SUCC).some(l=>l.includes(t)))where[t].push('successions');if(Object.values(AUD_REQ).some(r=>(r.lean||[]).includes(t)||(r.never||[]).includes(t)))where[t].push('audiences');
        if(FALL.keepT.includes(t)||FALL.razeT.includes(t))where[t].push('captures')}
      return JSON.stringify({bad,noTxt:TRAITS.filter(t=>!RG_TXT[t]),where})})()""")
    ok(not n['bad'],'names: every trait in the tables exists',' '.join(n['bad'][:8]))
    ok(not n['noTxt'],'every trait has stand-in text for the Allegiance picker',' '.join(n['noTxt']))
    print('INFO where each power trait counts:',' · '.join(f"{t}: {','.join(w) or '-'}" for t,w in n['where'].items()))

    # ---- profiles: single traits, then every pair, on every power and the Unbound
    await ev("""window.__tr={setT(side,tr){if(side==='pirate')S.dread.traits=tr.slice();else S.leaders[side].traits=tr.slice();leaderProfiles();return JSON.stringify(LEADP[side]||null)}};1""")
    keep=await ev("JSON.stringify({L:FAC_IDS.map(f=>leaderOf(f).traits),D:S.dread.traits})")
    for side,spec in [(f,POWER) for f in ('halcyon','varkesh','ostrova')]+[('pirate',PIRATE)]:
      wrong=[]
      for t in spec:
        got=await j(f"__tr.setT('{side}',['{t}'])")
        if not got or not same(got,blend(spec,[t])):wrong.append(f'{t}: {got}')
      ok(not wrong,f'profile: each single trait on {side}',' | '.join(wrong[:4]))
      wrong=[]
      for a,c in itertools.combinations(spec,2):
        got=await j(f"__tr.setT('{side}',['{a}','{c}'])")
        if not got or not same(got,blend(spec,[a,c])):wrong.append(f'{a}+{c}: {got}')
      ok(not wrong,f'profile: every pair blends on {side} ({len(list(itertools.combinations(spec,2)))} pairs)',' | '.join(wrong[:4]))
      got=await j(f"__tr.setT('{side}',[])");ok(got and same(got,BASE),f'profile: no traits flies plain on {side}',str(got))
    for t,why in DESIGN_GAP.items():
      if t in POWER and not POWER[t] or t in PIRATE and not PIRATE[t] or t in('Mercantile','Patient','Opportunist','Bloodthirsty'):gap(f'pilots: {t}',why)
    # put the galaxy's rolled leaders back (the sweep above left them with none)
    await ev(f"(()=>{{const k={keep};FAC_IDS.forEach((f,i)=>leaderOf(f).traits=k.L[i]);S.dread.traits=k.D;leaderProfiles();return 1}})()")
    sides=await j("(()=>{leaderProfiles();return JSON.stringify(Object.keys(LEADP))})()")
    ok(set(sides)>={'halcyon','varkesh','ostrova','pirate'},'every power and the Unbound have a profile',str(sides))

    # ---- rolls and neutral mode
    r=await j("""(()=>{const bad=[];for(let i=0;i<300;i++){const R=leadRoll(),pairs=new Set();for(const f of FAC_IDS){const t=R[f];if(t.length!==2||t[0]===t[1]||!t.every(x=>TRAITS.includes(x)))bad.push(f+':'+t);pairs.add([...t].sort().join('|'))}if(pairs.size!==3)bad.push('shared pair '+JSON.stringify(R))}
      for(let i=0;i<300;i++){const t=dpRoll();if(t.length!==2||t[0]===t[1]||!t.every(x=>DP_TRAITS.includes(x)))bad.push('dp:'+t)}
      const L=S.leaders,m=LEADT.mode;let neu;try{LEADT.mode='neutral';S.leaders=null;leadersInit();neu={tr:FAC_IDS.map(f=>leaderOf(f).traits.length),p:FAC_IDS.map(f=>LEADP[f])}}finally{LEADT.mode=m;S.leaders=L;leaderProfiles()}
      return JSON.stringify({bad:bad.slice(0,5),neu})})()""")
    ok(not r['bad'],'rolls: 300 starting rolls and 300 pirate rolls valid',str(r['bad']))
    ok(all(x==0 for x in r['neu']['tr']) and all(same(x,BASE) for x in r['neu']['p']),'rolls: neutral mode (war checks) gives no traits and plain pilots',str(r['neu']))

    # ---- event weights
    e=await j("""(()=>{const bad=[],K=[...new Set(Object.keys(EV_LEAN).concat(Object.keys(EV_NEVER)))],L=leaderOf('halcyon'),t0=L.traits;
      try{for(const t of TRAITS){L.traits=[t];for(const k of K){const w=evWeight('halcyon',k),never=(EV_NEVER[k]||[]).includes(t);if(!isFinite(w)||w<0||(w===0)!==never)bad.push(t+'/'+k+'='+w)}}}finally{L.traits=t0}
      return JSON.stringify(bad)})()""")
    ok(not e,'events: every trait weighs every event, 0 only when forbidden',' '.join(e[:6]))

    # ---- live: targeting and break-off for every side
    s=await j("""(()=>{if(S.player.docked)undock();for(let i=0;i<FAC_IDS.length;i++)for(let k=i+1;k<FAC_IDS.length;k++){const a=FAC_IDS[i],c=FAC_IDS[k];S.rel[a][c]=S.rel[c][a]=-90;const P=pairOf(a,c);P.war=1;P.warT=S.T;P.ally=0}
      Object.assign(window.__tr,{clear(){W.ents=W.ents.filter(x=>!x.__tr)},sp(role,side,cls,x){const e=makeNPC(role,side,cls,1,{},W.sid);e.__tr=1;e.pt=null;e.ptk=null;e.ptWant=undefined;e.x=90000+x;e.y=7000;e.z=-90000;W.ents.push(e);return e}});
      return JSON.stringify({live:!!W,hv:hostile('halcyon','varkesh'),ph:hostile('pirate','halcyon'),hb:hostile('halcyon','brood'),pb:hostile('pirate','brood')})})()""")
    ok(s['live'] and s['hv'] and s['ph'] and s['hb'],'live: a system with the powers at war, the Unbound and the Brood hostile',str(s))
    foe={'halcyon':'varkesh','varkesh':'ostrova','ostrova':'halcyon','pirate':'halcyon'}
    for side,spec in [(f,POWER) for f in ('halcyon','varkesh','ostrova')]+[('pirate',PIRATE)]:
      g=foe[side];out=await j(f"""(()=>{{const res={{}},sp=__tr.sp,side='{side}',g='{g}';
        const reach=(tr)=>{{__tr.setT(side,tr);const r=LEADP[side].range,o={{}};for(const[k,f]of[['in',.95],['out',1.05]]){{__tr.clear();const A=sp('patrol',side,'interceptor',0),B=sp('patrol',g,'interceptor',1000*r*f);o[k]=findHostile(A,1000)===B}}return o}};
        for(const t of {json.dumps(list(spec))})res['reach '+t]=reach([t]);
        __tr.setT(side,[]);__tr.clear();{{const A=sp('patrol',side,'interceptor',0),F=sp('patrol',g,'interceptor',200),M=sp('miner',g,'prospector',700);res.plainPicks=findHostile(A,1000)===F?'fighter':'other'}}
        for(const t of {json.dumps([t for t in spec if spec[t].get('ruthless')])}){{__tr.setT(side,[t]);__tr.clear();const A=sp('patrol',side,'interceptor',0),F=sp('patrol',g,'interceptor',200),M=sp('miner',g,'prospector',700);res['ruthless '+t]=findHostile(A,1000)===M}}
        for(const t of {json.dumps([t for t in spec if spec[t].get('zeal')])}){{__tr.setT(side,[t]);__tr.clear();const A=sp('patrol',side,'interceptor',0),F=sp('patrol',g,'interceptor',200),Bz=sp('patrol','brood','mite',700);res['zeal '+t]=findHostile(A,1000)===Bz}}
        for(const t of {json.dumps([t for t in spec if spec[t].get('honour')])}.concat([''])){{__tr.setT(side,t?[t]:[]);__tr.clear();const A=sp('patrol',side,'interceptor',0),F=sp('patrol',g,'interceptor',300);F.jamOff=W.t+60;res['jammed '+(t||'plain')]=findHostile(A,1000)===F}}
        __tr.clear();return JSON.stringify(res)}})()""")
      bad=[k for k,v in out.items() if k.startswith('reach') and not (v['in'] and not v['out'])]
      ok(not bad,f'live {side}: reach scales with each trait',' '.join(f"{k}={out[k]}" for k in bad[:4]))
      for k,v in out.items():
        if k.startswith(('ruthless','zeal')):ok(v,f'live {side}: {k} goes for its target first (miner / Brood over a nearer fighter)')
        if k.startswith('jammed'):ok(v==(k=='jammed plain'),f'live {side}: {k} '+('fires on a jammed-dark ship' if k=='jammed plain' else 'leaves a jammed-dark ship alone'),str(v))
      ok(out['plainPicks']=='fighter',f'live {side}: plain pilots take the nearest',out['plainPicks'])
    # break-off by hull, every combat role, for each side's break-off traits
    roles=['patrol','escort','raider','strike','pirate','screen']
    for side,spec in [('halcyon',POWER),('pirate',PIRATE)]:
      bo=[t for t in spec if spec[t].get('breakoff')]
      out=await j(f"""(()=>{{const res={{}},sp=__tr.sp,side='{side}',g='{'varkesh' if side!='pirate' else 'halcyon'}';
        for(const t of {json.dumps(bo)}.concat(['Vengeful+'+{json.dumps(bo[0])}]))for(const role of {json.dumps(roles)}){{const tr=t.startsWith('Vengeful+')?(side==='pirate'?null:['Vengeful',t.slice(9)]):[t];if(!tr)continue;
          __tr.setT(side,tr);const b=LEADP[side].breakoff,o={{}};for(const[k,h]of[['hurt',Math.max(.05,b-.08)],['whole',Math.min(.95,b+.1)]]){{__tr.clear();const A=sp(role,side,'interceptor',0),B=sp('patrol',g,'interceptor',300);A.ai.tgt=B;A.order=null;A.hull=A.st.hull*(b?h:.1);try{{npcThink(A,.016)}}catch(e){{o.err=String(e).slice(0,80)}}o[k]=A.role==='leave'}}res[t+'/'+role]=o}}
        __tr.clear();__tr.setT(side,[]);return JSON.stringify(res)}})()""")
      for k,v in out.items():
        t,role=k.split('/')
        if v.get('err'):ok(False,f'live {side}: npcThink for a {role}',v['err']);continue
        if t.startswith('Vengeful'):ok(not v['hurt'],f'live {side}: Vengeful {role} stays at low hull even with {t[9:]}');continue
        want=role in('patrol','escort','raider')
        if want:ok(v['hurt'] and not v['whole'],f'live {side}: {t} {role} breaks off when hurt, not before',str(v))
        elif not v['hurt']:gap(f'break-off: {side} {role}s',f'{t} pilots in the {role} role never break off (npcThink wrapper only covers patrol, escort, raider)')
    # the user, 7 Nov 2026: break-off wins over Bloodthirsty (a Bloodthirsty pirate that is also Superstitious or Paranoid breaks off)
    bt=await j("""(()=>{const sp=__tr.sp,o={};for(const t2 of ['Superstitious','Paranoid']){__tr.setT('pirate',['Bloodthirsty',t2]);__tr.clear();const A=sp('raider','pirate','interceptor',0),B=sp('patrol','halcyon','interceptor',300);A.ai.tgt=B;A.order=null;A.hull=A.st.hull*.1;try{npcThink(A,.016)}catch(e){}o[t2]=A.role==='leave'}
      __tr.clear();__tr.setT('pirate',[]);return JSON.stringify(o)})()""")
    ok(all(bt.values()),'live pirate: a hurt Bloodthirsty raider breaks off when its other trait says so (break-off wins)',str(bt))
    # which roles' target choice a trait reaches (Ruthless: the miner over a nearer fighter)
    out=await j("""(()=>{const res={},sp=__tr.sp;__tr.setT('halcyon',['Ruthless']);for(const role of ['patrol','escort','raider','strike','pirate','screen']){__tr.clear();const A=sp(role,'halcyon','interceptor',0),F=sp('patrol','varkesh','interceptor',200),M=sp('miner','varkesh','prospector',700);A.ai.t=0;A.ai.tgt=null;A.order=null;try{npcThink(A,.016)}catch(e){}res[role]=A.ai.tgt===M?'miner':A.ai.tgt===F?'fighter':'none'}
      __tr.clear();__tr.setT('halcyon',[]);return JSON.stringify(res)})()""")
    print('INFO Ruthless target choice by role (miner = the trait reaches it):',out)
    for role,v in out.items():
      if v!='miner':gap(f'targeting: {role}s',f'a Ruthless {role} took the {v}, not the miner: the trait doesn\'t reach this role\'s targeting')

    # put the rolled leaders back again (the live probes left each side with none)
    await ev(f"(()=>{{const k={keep};FAC_IDS.forEach((f,i)=>leaderOf(f).traits=k.L[i]);S.dread.traits=k.D;leaderProfiles();return 1}})()")
    # ---- successions
    sc=await j("""(()=>{const res={};const prof=f=>JSON.stringify(LEADP[f]);
      leaderOf('halcyon').traits=['Mercantile','Cautious'];leaderProfiles();succession('halcyon','killed','varkesh');{const N=leaderOf('halcyon');const p0=prof('halcyon');leaderProfiles();res.killed={tr:N.traits,grudge:N.grudge.varkesh||0,fresh:p0===prof('halcyon'),bo:LEADP.halcyon.breakoff}}
      leaderOf('varkesh').traits=['Cautious','Patient'];leaderProfiles();succession('varkesh','ousted');{const N=leaderOf('varkesh');const p0=prof('varkesh');leaderProfiles();res.ousted={tr:N.traits,fresh:p0===prof('varkesh')}}
      S.dread.traits=['Greedy','Gallant'];leaderProfiles();dpSucceed('killedPow','ostrova');{const N=S.dread;const p0=prof('pirate');leaderProfiles();res.dread={tr:N.traits,grudge:N.grudge.ostrova||0,fresh:p0===prof('pirate')}}
      return JSON.stringify(res)})()""")
    k=sc['killed'];ok(len(set(k['tr']))==2 and 'Vengeful' in k['tr'] and k['grudge']>0 and k['fresh'] and k['bo']==0,'succession: a killed leader\'s successor is Vengeful, holds a grudge, pilots follow at once',str(k))
    k=sc['ousted'];ok(len(set(k['tr']))==2 and not set(k['tr'])&{'Cautious','Patient'} and set(k['tr'])<=set(POWER) and k['fresh'],'succession: an ousted Cautious, Patient leader\'s successor shares neither trait',str(k))
    k=sc['dread'];ok(len(set(k['tr']))==2 and set(k['tr'])<=set(PIRATE) and k['fresh'],'succession: the Dread Pirate\'s successor has two pirate traits, pilots follow at once',str(k))
    print('ledger',await ev(LED))

    # ---- save and continue in a fresh tab
    sv=await j("""(()=>{S.leaders.halcyon.traits=['Ambitious','Ruthless'];S.leaders.varkesh.traits=['Cautious','Honourable'];S.dread.traits=['Paranoid','Bloodthirsty'];leaderProfiles();
      const before={h:LEADP.halcyon,v:LEADP.varkesh,p:LEADP.pirate},snap=JSON.parse(JSON.stringify(serialize()));LEADP={};let err=null;try{startWith(snap)}catch(e){err=String(e).slice(0,120)}
      return JSON.stringify({err,before,after:{h:LEADP.halcyon||null,v:LEADP.varkesh||null,p:LEADP.pirate||null},tr:S.leaders.halcyon.traits})})()""")
    ok(not sv['err'],'save: a saved galaxy continues',str(sv['err']))
    ok(sv['after']['h']==sv['before']['h'] and sv['after']['v']==sv['before']['v'],'save: the powers\' pilots keep their leaders\' traits after Continue',f"after={sv['after']['h']},{sv['after']['v']} (leadersInit returns early on a saved galaxy, so nothing rebuilds LEADP)")
    ok(sv['after']['p']==sv['before']['p'],'save: the Unbound keep the Dread Pirate\'s traits after Continue',f"after={sv['after']['p']}")
    # Continue after a save made in flight moves the ledger by itself (+15 Vantium a time, 7 Nov 2026: the economy bot's), so
    # the hour below is measured from the continued galaxy
    print('ledger after Continue (not a trait matter)',await ev(LED));await ev("(()=>{S.ledger0=ledger();return 1})()")

    # ---- an hour of strategy with rolled leaders
    hr=await j("""(()=>{const bad=new Set();let stale=0,succ=0,n0=FAC_IDS.map(f=>leaderOf(f).name+leaderOf(f).n).join();running=false;exitSector();W=null;const t0=S.T;
      while(S.T<t0+3600){S.T+=10;strategicTick();updateEvents();
        for(const f of FAC_IDS){const L=leaderOf(f);if(!L||L.traits.length!==2||L.traits[0]===L.traits[1]||!L.traits.every(t=>TRAITS.includes(t)))bad.add(f+':['+(L&&L.traits)+'] '+(L&&L.name)+' #'+(L&&L.n)+' since '+(L&&Math.round(L.since-t0))+'s, last: '+String(((S.chron||[]).slice(-1)[0]||{}).t||(S.chron||[]).slice(-1)[0]||'').slice(0,90))}
        if(S.dread&&S.dread.traits.length&&(S.dread.traits.length!==2||!S.dread.traits.every(t=>DP_TRAITS.includes(t))))bad.add('dread:'+S.dread.traits);
        if(Math.random()<.02){const f=pick(FAC_IDS);succession(f,pick(Object.keys(SUCC)),pick(FAC_IDS.filter(g=>g!==f)));succ++}
        // measure without repairing: rebuild, compare, then put the old profiles back so staleness persists and is counted
        const a=JSON.stringify(LEADP);leaderProfiles();if(a!==JSON.stringify(LEADP)){stale++;LEADP=JSON.parse(a)}}
      return JSON.stringify({bad:[...bad].slice(0,5),stale,succ})})()""")
    ok(not hr['bad'],f"hour: every leader keeps two valid traits ({hr['succ']} forced successions)",str(hr['bad']))
    ok(hr['stale']==0,'hour: pilot profiles never go stale',f"{hr['stale']} ticks where LEADP didn't match the leaders")
    print('ledger',await ev(LED))

    print(f"traits: {R['pass']} passed, {len(R['fail'])} failed, {len(R['gap'])} gaps")
    print('errors',(errs+R['fail'])[:12]);await b.close()
asyncio.run(main())
