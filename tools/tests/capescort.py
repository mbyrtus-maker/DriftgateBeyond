# Beyond (6 Nov 2026): capital escorts ride the jump, and the carrier's defence set. A carrier comes with five fighters and
# a scout docked; they stay aboard with no threat, launch when a raider comes within 4.5 km, fight, and land 20 s after it's
# clear; the scout flips an unlocked beacon and limpets an attacking enemy capital; past 75% of the spin-up everything lands
# and jumps with the carrier; a fighter guarding an escort capital docks on its hull past 75%, rides the jump in the
# capital's hold and undocks beside it with its order still running; the ledger stays exact throughout
import asyncio,json
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    # a quiet Halcyon system of the open ring, the player docked out of the way
    print('setup',await ev("""(()=>{const P=S.player;const ids=SECTOR_DEFS.map(d=>d.id),sid=ids.find(id=>sectorOwner(id)==='halcyon'&&!DEF[id].home&&S.beacons&&S.beacons[id])||ids.find(id=>sectorOwner(id)==='halcyon'&&!DEF[id].home)||ids.find(id=>sectorOwner(id)==='halcyon');exitSector();P.sector=sid;P.docked=null;enterSector(sid);
      for(const e of W.ents.slice())if(e.type==='ship'&&!e.isPlayer&&e.alive&&hostile('halcyon',e.side))despawn(e);W.player.x=6000;W.player.y=3000;W.player.z=6000;window._SID=sid;
      let t=null;devLedger(()=>{t=makeCarrier('halcyon',sid,{},null,true)});t.dummy=true;window._T=t;strategicTick();const e=carEnt(t);
      return JSON.stringify({sid,def:capDefHave(t),live:!!e,bay:e&&e.dbay.length,flying:e&&e.dfl.length})})()"""))
    print('ledger',await ev(LED))
    await pg.wait_for_timeout(4000)
    print('no threat: all aboard',await ev("(()=>{const e=carEnt(window._T);return JSON.stringify({bay:e.dbay.length,flying:e.dfl.filter(p=>p.alive).length})})()"))
    print('raider at 3 km',await ev("""(()=>{const M=carEnt(window._T);const r=makeNPC('raider','pirate','raider',1,{},'stock:pirate');r.x=M.x+3000;r.y=M.y;r.z=M.z;W.ents.push(r);window._R=r;return capThreat(M)})()"""))
    await pg.wait_for_timeout(5000)
    print('launched',await ev("(()=>{const e=carEnt(window._T);const f=e.dfl.filter(p=>p.alive&&W.ents.includes(p));return JSON.stringify({flying:f.map(p=>p.cls),bay:e.dbay})})()"))
    print('ledger',await ev(LED))
    print('raider gone',await ev("(()=>{const r=window._R;if(r.alive)despawn(r);for(const e of W.ents.slice())if(e.type==='ship'&&!e.isPlayer&&e.alive&&hostile('halcyon',e.side))despawn(e);return 'ok'})()"))
    await pg.wait_for_timeout(45000)
    print('landed after 20 s clear',await ev("(()=>{const e=carEnt(window._T);return JSON.stringify({flying:e.dfl.filter(p=>p.alive&&W.ents.includes(p)).length,bay:e.dbay.length})})()"))
    print('ledger',await ev(LED))
    print('beacon open to the scout',await ev("""(()=>{const B=S.beacons[window._SID];if(!B)return 'no beacon here';B.owner='varkesh';B.by=null;B.T=S.T-1000;B.sec=S.T-1000;const M=carEnt(window._T),f=capDefSide(window._T);return JSON.stringify({state:bcnState(B),job:!!capBeaconJob(M,f)})})()"""))
    await pg.wait_for_timeout(45000)
    print('scout flipped it',await ev("(()=>{const B=S.beacons[window._SID],e=carEnt(window._T);return JSON.stringify({owner:B.owner,state:bcnState(B),scoutOut:e.dfl.filter(p=>p.alive&&W.ents.includes(p)).map(p=>p.cls)})})()"))
    await pg.wait_for_timeout(20000)
    print('scout home',await ev("(()=>{const e=carEnt(window._T);return JSON.stringify({bay:e.dbay,flying:e.dfl.filter(p=>p.alive&&W.ents.includes(p)).length})})()"))
    print('enemy capital attacks',await ev("""(()=>{const M=carEnt(window._T);let r=null;devLedger(()=>{r=makeCarrier('pirate',window._SID,{})});strategicTick();const E=carEnt(r);E.x=M.x+2500;E.y=M.y;E.z=M.z;M.lastHit=W.t;M.lastHitBy='pirate';window._E=r;return JSON.stringify({live:!!E,att:!!capAttacker(M,'halcyon')})})()"""))
    await pg.wait_for_timeout(25000)
    print('limpet on it',await ev("(()=>{const R=window._E;return JSON.stringify({ping:!!(R.pings&&R.pings.halcyon&&R.pings.halcyon.until>S.T)})})()"))
    print('ledger',await ev(LED))
    print('enemy gone',await ev("(()=>{const R=window._E,E=carEnt(R);if(E)despawnFrigate(E);devLedger(()=>{S.frigates=S.frigates.filter(x=>x!==R)});for(const e of W.ents.slice())if(e.type==='ship'&&!e.isPlayer&&e.alive&&hostile('halcyon',e.side))despawn(e);return 'ok'})()"))
    # the jump: a raider keeps them flying, then the drive spins up
    print('jump ordered',await ev("""(()=>{const t=window._T,M=carEnt(t);const r=makeNPC('raider','pirate','raider',1,{},'stock:pirate');r.x=M.x+3500;r.y=M.y;r.z=M.z;r.hull=1e6;r.st={...r.st,hull:1e6};r.ai.passive=1;W.ents.push(r);window._R=r;
      const to=NEIGH[window._SID].find(n=>!DEF[n].home);t.dummy=false;t.jumpTo=to;window._TO=to;return to})()"""))
    await pg.wait_for_timeout(3000)
    print('spinning',await ev("(()=>{const t=window._T,e=carEnt(t);return JSON.stringify({p:t.spin&&+t.spin.p.toFixed(2),flying:e?e.dfl.filter(p=>p.alive&&W.ents.includes(p)).length:-1})})()"))
    print('past 75%',await ev("(()=>{const t=window._T;if(t.spin)t.spin.p=.8;return 'ok'})()"))
    await pg.wait_for_timeout(8000)
    print('all landed',await ev("(()=>{const t=window._T,e=carEnt(t);return JSON.stringify({sector:t.sector,live:!!e,flying:e?e.dfl.filter(p=>p.alive&&W.ents.includes(p)).length:'gone',wings:e?(e.flights||[]).filter(p=>p.alive&&W.ents.includes(p)&&p.mis!=='sortie').length:'gone'})})()"))
    await pg.wait_for_timeout(15000)
    print('jumped with the set',await ev("(()=>{const t=window._T;return JSON.stringify({sector:t.sector,to:window._TO,def:capDefHave(t).length,wing:(t.wing||[]).length})})()"))
    print('ledger',await ev(LED))
    # a fighter guarding an escort capital docks on its hull past 75% and rides the jump
    print('escort capital guarded',await ev("""(()=>{if(window._R&&window._R.alive)despawn(window._R);let c=null;devLedger(()=>{c=makeEscort('halcyon',window._SID,{})});c.dummy=true;strategicTick();const C=carEnt(c);window._C=c;
      let g=null;devLedger(()=>{g=makeNPC('patrol','halcyon','striker',1,{missile:2},'stock:halcyon');g.x=0;g.y=0;g.z=0;W.ents.push(g)});g.x=C.x+400;g.y=C.y;g.z=C.z;g.order={kind:'guard',tgt:C,until:W.t+600,slot:0,by:true,pid:null};window._G=g;
      c.spin={to:NEIGH[window._SID].find(n=>!DEF[n].home),p:.8};return JSON.stringify({cap:!!C,guard:true})})()"""))
    await pg.wait_for_timeout(6000)
    print('on the hull',await ev("(()=>{const g=window._G,C=carEnt(window._C);return JSON.stringify({ride:g.hullRide===C,dist:Math.round(d3(g,C)),rel:Math.round(hyp(g.vx-C.vx,g.vy-C.vy,g.vz-C.vz))})})()"))
    print('spin broken: undocks',await ev("(()=>{const c=window._C;const s=c.spin;c.spin=null;window._S=s;return 'ok'})()"))
    await pg.wait_for_timeout(1500)
    print('free',await ev("(()=>JSON.stringify({ride:!!window._G.hullRide}))()"))
    print('spins again and jumps',await ev("(()=>{const c=window._C;c.spin={to:window._S.to,p:.8};return 'ok'})()"))
    await pg.wait_for_timeout(5000)
    print('docked again',await ev("(()=>!!window._G.hullRide)()"))
    print('the jump',await ev("""(()=>{const c=window._C,C=carEnt(c);despawnFrigate(C);c.sector=c.spin.to;c.spin=null;return JSON.stringify({riders:(c.riders||[]).map(r=>r.cls+':'+r.kind),load:c.load.missile||0,gone:!W.ents.includes(window._G)})})()"""))
    print('ledger',await ev(LED))
    print('arrives beside it',await ev("""(()=>{const c=window._C;c.sector=window._SID;const C=spawnFrigate(c,true);const g=W.ents.find(e=>e.alive&&e.order&&e.order.tgt===C);return JSON.stringify({rider:!!g,cls:g&&g.cls,missiles:g&&g.load.missile||0,dist:g&&Math.round(d3(g,C)),left:g&&Math.round(g.order.until-W.t)})})()"""))
    print('ledger',await ev(LED))
    print('hangar line',await ev("(()=>{const t=window._T;return capDefLine({tok:t,dbay:capDefHave(t),dfl:[]}).replace(/<[^>]+>/g,'').slice(0,90)})()"))
    await pg.wait_for_timeout(8000)
    print('after flight',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
