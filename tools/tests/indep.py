# Beyond (7 Nov 2026): independent pilots and pilot traits. Twelve independents at the three freeports with stakes from the
# Compact, traits rolled, parts off the shelf; an hour out of sight (trading, mining, board jobs); a posted job taken by an
# independent and paid into its purse; one flying live and arriving; one shot down live (no standing lost, kit and hold as
# salvage), back after 5 minutes with a death trait; every AI ship rolls a trait; an ace learns from its death; trait
# behaviour (Opportunist targets, Light Load miners, Tripwire scouts); the ledger exact throughout
import asyncio,json,os
from playwright.async_api import async_playwright
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[];fails=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    def chk(name,ok,info=''):
      print(('ok   ' if ok else 'FAIL ')+name,info)
      if not ok:fails.append(name)
    r=json.loads(await ev("(()=>{strategicTick();const L=indAll();return JSON.stringify({n:L.length,ports:[...new Set(L.map(I=>I.port))].length,traits:L.every(I=>I.pt&&PT_FX[I.pt]),purse:L.every(I=>indPurse(I)>0),kit:L.filter(I=>Object.keys(I.kit).length).length})})()"))
    chk('twelve independents at three freeports',r['n']==12 and r['ports']==3,r)
    chk('each with a trait and a purse',r['traits'] and r['purse'],r)
    chk('most fitted parts off the shelf',r['kit']>=6,r)
    chk('ledger after arrival',(await ev(LED))=='exact')
    # an hour out of sight
    r=json.loads(await ev("(()=>{for(let i=0;i<360;i++){S.T+=10;strategicTick();updateEvents()}const L=indAll();return JSON.stringify({jobs:L.reduce((a,I)=>a+I.jobs,0),earned:L.reduce((a,I)=>a+I.earned,0),busy:L.filter(I=>I.st!=='dock').length})})()"))
    chk('an hour of work: trades, ore and deliveries',r['jobs']>=10 and r['earned']>3000,r)
    chk('ledger after an hour',(await ev(LED))=='exact',await ev(LED))
    # a posted job goes to an independent
    print('depot',await ev("""(()=>{const P=S.player;undock();P.rp=5000;const sid=SECTOR_DEFS.map(d=>d.id).find(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id]&&S.sectors[id].ast.some(a=>!a.rift&&oreTotal(a)>40));exitSector();P.sector=sid;P.docked=null;enterSector(sid);P.cls='bulker';fitOf(P);refreshPlayerStats();devLedger(()=>{P.cargo={frame:2}});
      depFresh(P);transfer('halcyon','player',20000);window._SID=sid;const p=W.player;p.x=4000;p.y=2000;p.z=4000;for(const I of indAll())if(I.role==='hauler'&&I.st!=='down'){I.st='dock';I.run=null;I.live=false;I.sector=I.port}return sid})()"""))
    r=json.loads(await ev("""(()=>{const P=S.player,sid=window._SID;pjPost(P,`${sid}:supply:plate:6:fast`);const j=S.pj[S.pj.length-1];j.claimAt=S.T;pjTick();const rr=pjRunOf(j.run);const I=rr&&indById(rr.ind);window._J=j;window._I=I&&I.id;window._P0=I?indPurse(I):0;return JSON.stringify({who:j.who,run:!!rr,ind:!!I,st:I&&I.st,cls:rr&&rr.cls})})()"""))
    chk('a posted job is taken by an independent',r['ind'] and 'independent' in (r['who'] or ''),r)
    # fly elsewhere so the run goes out of sight
    await ev("""(()=>{const P=S.player,sid=window._SID,far=SECTOR_DEFS.map(d=>d.id).filter(id=>id!==sid&&(HOP[sid][id]||0)>=4)[0];exitSector();P.sector=far;P.docked=null;enterSector(far);if(WORLDS[sid])closeWorld(WORLDS[sid]);return far})()""")
    r=json.loads(await ev("""(()=>{const j=window._J;for(let i=0;i<160&&j.state!=='done';i++){S.T+=10;strategicTick()}const I=indById(window._I);return JSON.stringify({state:j.state,msg:j.msg,paid:j.paid,purse:I?indPurse(I)-window._P0:null,st:I&&I.st})})()"""))
    chk('the job is flown and the fee goes into its purse',r['state']=='done' and (r['paid'] or 0)>0 and (r['purse'] or 0)>=r['paid']*0.5,r)
    chk('ledger after the posted job',(await ev(LED))=='exact',await ev(LED))
    # one flying live: an independent's trade run passing through this system
    await ev("""(()=>{const P=S.player,sid=window._SID;exitSector();P.sector=sid;P.docked=null;enterSector(sid);const p=W.player;p.x=4000;p.y=2000;p.z=4000;return 1})()""")
    r=json.loads(await ev("""(()=>{const sid=window._SID,I=indAll().find(x=>x.role==='hauler'&&x.st==='dock')||indAll().find(x=>x.st!=='down'&&x.st!=='pj'&&!x.live);if(!I)return '{}';const nb=NEIGH[sid][0];I.sector=nb;I.run={k:'home',to:sid,path:[nb,sid],leg:0,next:S.T,T0:S.T};I.st='go';devLedger(()=>{I.hold={fe:5}});window._L=I.id;
      I.run.leg=1;I.sector=sid;const e=indSpawn(I,true);return JSON.stringify({live:!!e,label:e&&e.pname,cargo:e&&e.cargo,pt:e&&e.pt})})()"""))
    chk('an independent flies live with its name and trait',r.get('live') and 'Independent' in (r.get('label') or ''),r)
    r=json.loads(await ev("""(()=>{const I=indById(window._L),e=W.ents.find(x=>x.indId===I.id&&x.alive);const P=S.player,s0=JSON.stringify(P.stand);const c0=Object.keys(S.sectors[W.sid].crates).length;
      damageShip(e,5,'player',{src:W.player,x:e.x,y:e.y,z:e.z},'kinetic');const k0=JSON.stringify(I.kit);killShip(e,'player',{src:W.player,kind:'missile'});return JSON.stringify({st:I.st,cause:I.cause,stand:JSON.stringify(P.stand)===s0,kit:Object.keys(I.kit).length,back:I.back-S.T,killer:I.killer})})()"""))
    chk('shot down live: down, kit lost, no standing lost',r['st']=='down' and r['kit']==0 and r['stand'],r)
    chk('killed by you counts as a named pilot',r['cause']=='named',r)
    chk('ledger after the loss (hold and kit as salvage)',(await ev(LED))=='exact',await ev(LED))
    r=json.loads(await ev("""(()=>{const I=indById(window._L);for(let i=0;i<40;i++){S.T+=10;strategicTick()}return JSON.stringify(I?{st:I.st,pt:I.pt,nem:I.nem,cls:I.cls,sector:I.sector,port:I.port}:{gone:1})})()"""))
    chk('back at its freeport after 5 minutes with a death trait (Haunted: you killed it)',r.get('gone') or (r['st']!='down' and r['pt']=='Haunted' and r['nem']=='me'),r)
    chk('ledger after its return',(await ev(LED))=='exact',await ev(LED))
    # death traits by cause
    r=json.loads(await ev("JSON.stringify({f1:ptDeath('fighter','missile'),f2:ptDeath('fighter','pd'),f3:ptDeath('fighter','outnumbered'),m:ptDeath('miner','full'),h:ptDeath('hauler','alone'),b:ptDeath('bomber','escape'),c:ptDeath('capital','bomber'),s:ptDeath('scout','shadow'),u:ptDeath('miner','?'),v:ptDeath('fighter','named',{killer:'ace:3'})})"))
    chk('death traits by cause',r=={'f1':'Missile-Wary','f2':'Flak-Shy','f3':'Pack Fighter','m':'Light Load','h':'Convoy Only','b':'Quick Exit','c':'Screen First','s':'Long Leash','u':'Shaken','v':'Vengeful'},r)
    # every AI ship rolls a trait
    r=json.loads(await ev("""(()=>{const c={};let n=0,st=0;for(let i=0;i<400;i++){const e=makeNPC(pick(['patrol','raider','miner','hauler','scout']),'halcyon',pick(['striker','skiff','courier','scout','bomber']),1,{},null);n++;if(e.pt==='Steady')st++;c[e.pt]=(c[e.pt]||0)+1}const b=makeNPC('raider','brood','mite',1,{},null);return JSON.stringify({steady:st/n,kinds:Object.keys(c).length,brood:b.pt||null})})()"""))
    chk('every AI ship rolls a trait, Steady the common roll, the Brood none',0.15<r['steady']<0.35 and r['kinds']>=20 and r['brood'] is None,r)
    # an ace learns from its death
    r=json.loads(await ev("""(()=>{aceInit();const A=S.aces.find(a=>a.side==='varkesh'&&!a.ret);if(!A)return '{}';A.pt='Hotshot';A.d=0;const e={aceId:A.id,side:A.side,type:'ship',st:{hull:100},cargo:{},x:0,y:0,z:0,alive:true,dmg:{}};A.ptCause=ptCause(e,'halcyon',{kind:'missile',src:{type:'ship',role:'patrol',x:0,y:0,z:0}},'fighter');aceDown(A);return JSON.stringify({pt:A.pt,neu:A.ptNew})})()"""))
    chk('an ace downed by a missile comes back Missile-Wary',r.get('pt')=='Missile-Wary',r)
    # traits in live behaviour
    r=json.loads(await ev("""(()=>{const p=W.player;const e=makeNPC('patrol','pirate','striker',1,{},null);e.pt='Opportunist';e.ptk=null;e.x=p.x;e.y=p.y;e.z=p.z+200;W.ents.push(e);
      const a=makeNPC('miner','halcyon','skiff',1,{},null);a.x=e.x+300;a.y=e.y;a.z=e.z;W.ents.push(a);const h=makeNPC('miner','halcyon','skiff',1,{},null);h.x=e.x+600;h.y=e.y;h.z=e.z;h.hull=h.st.hull*.2;W.ents.push(h);
      const t=findHostile(e,1500);const ok=t===h;despawn(e);despawn(a);despawn(h);return JSON.stringify({hurtFirst:ok})})()"""))
    chk('an Opportunist goes for the damaged ship first',r['hurtFirst'],r)
    r=json.loads(await ev("""(()=>{const s=S.sectors[W.sid];const a=s.ast.find(x=>!x.comet&&oreTotal(x)>30);if(!a)return JSON.stringify({skip:1});const e=makeNPC('miner',S.player.sworn||'halcyon','skiff',1,{},null);e.pt='Light Load';e.ptk=null;e.x=a.x+40;e.y=a.y;e.z=a.z;W.ents.push(e);devLedger(()=>{e.cargo={fe:Math.ceil(e.st.cargo*.55)}});
      npcThink(e,.05);const st=e.ai.state;devLedger(()=>{e.cargo={}});despawn(e);return JSON.stringify({state:st})})()"""))
    chk('a Light Load miner turns home at half a hold',r.get('skip') or r['state']=='return',r)
    r=json.loads(await ev("""(()=>{const e=makeNPC('scout','ostrova','scout',1,{},null);e.pt='Tripwire';e.ptk=null;e.x=0;e.y=0;e.z=0;W.ents.push(e);const sb=scoutBeaconGoal;scoutBeaconGoal=()=>null;const pn=ptP(e);let ok=false;try{for(let i=0;i<200;i++)scoutThink(e,.05);ok=!!e.ai.ptGate}finally{scoutBeaconGoal=sb}despawn(e);return JSON.stringify({gate:ok})})()"""))
    chk('a Tripwire scout picks a gate to watch',r['gate'],r)
    await pg.wait_for_timeout(15000)
    chk('ledger at the end',(await ev(LED))=='exact',await ev(LED))
    print('fails',fails)
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
