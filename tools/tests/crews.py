# Beyond: AI crews as ships you can see. A depot with a miner, a hauler and a guard: each flies in the depot's system (miner
# beam on a rock, guard circling, hauler moving), a job change swaps the ship, a laid-up crew stays home, a crew ship destroyed
# loses the crew, the ledger stays exact. (Built from depots.py's setup.)
# Old header: A Lair upgraded to a Depot in place (store from the stash, ledger exact); your market sells and buys
# through visiting traders (credits and goods only move); AI crews hired, mining this system's rocks, hauling to a market,
# paid wages, laid up without running costs, leaving unpaid; the Economy and Post jobs tabs
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
    await pg.wait_for_function('window.__dg&&__dg.ev("!!(S&&S.player)")',timeout=30000);await pg.evaluate("__dg.ev('coDefault(S.player)')")  # a company profile (8 Nov 2026: no Depot without one)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    print('lair',await ev("""(()=>{const P=S.player;undock();P.rp=5000;const sid=SECTOR_DEFS.map(d=>d.id).find(id=>!S.stations[id]&&canBuildIn(id,'player')&&S.sectors[id].ast.filter(a=>oreTotal(a)>=60&&!a.rift).length>=3);exitSector();P.sector=sid;P.docked=null;enterSector(sid);
      const a=S.sectors[sid].ast.filter(r=>oreTotal(r)>=60&&!r.rift)[0],e=W.player;e.x=a.x+astR(a)+200;e.y=a.y;e.z=a.z;P.cls='bulker';fitOf(P);refreshPlayerStats();devLedger(()=>{P.cargo={frame:3,plate:6,fe:20}});lairBuildB();const L=lairsOf(P)[0];S.T=L.build+1;lairWorldB(.1);lairDock(L);dockAction('mv','fe:in:all');return JSON.stringify({sid,lair:!!L,stash:L.stash})})()"""))
    print('upgrade',await ev("""(()=>{dockAction('depotup');const P=S.player,R=S.stations[P.sector];return JSON.stringify({msg:dockErr,owner:R&&R.owner,kind:R&&R.kind,store:R&&R.stock,docked:P.docked,lairs:lairsOf(P).length,ctx:dockCtx().sub})})()"""))
    print('ledger',await ev(LED))
    print('hire',await ev("""(()=>{const P=S.player,R=S.stations[P.sector];devLedger(()=>{P.credits+=60000;inv.add(R.stock,'plate',20)});devOf(R).hangar=3;const m=['prospector','freighter','interceptor'].map(k=>crewHire(R,P,k));R.crew[2].job='guard';return JSON.stringify({m,crew:R.crew.map(c=>c.cls+':'+c.job)})})()"""))
    await ev("(()=>{undock();return 1})()");await pg.wait_for_timeout(15000)
    print('flying',await ev("""(()=>{const R=S.stations[S.player.sector];const E=W.ents.filter(e=>e.crewId&&e.alive);return JSON.stringify(E.map(e=>({job:e.job,label:shipLabel(e),side:e.side,mining:!!e.mining,toBase:Math.round(d3(e,R)),spd:Math.round(hyp(e.vx,e.vy,e.vz))})))})()"""))
    print('ledger',await ev(LED))
    print('job change',await ev("""(()=>{const R=S.stations[S.player.sector];R.crew[1].job='idle';return 1})()"""));await pg.wait_for_timeout(3000)
    print('after change',await ev("""JSON.stringify(W.ents.filter(e=>e.crewId&&e.alive).map(e=>e.job))"""))
    print('laid up',await ev("""(()=>{const R=S.stations[S.player.sector];R.crew[1].laid=true;return 1})()"""));await pg.wait_for_timeout(3000)
    print('after laid',await ev("""JSON.stringify(W.ents.filter(e=>e.crewId&&e.alive).map(e=>e.job))"""))
    print('loss',await ev("""(()=>{const R=S.stations[S.player.sector];const e=W.ents.find(x=>x.crewId&&x.job==='mine');killShip(e,'brood');return JSON.stringify({crew:R.crew.map(c=>c.cls+':'+c.job),ents:W.ents.filter(e=>e.crewId&&e.alive).length,feed:FEED.slice(-3).map(f=>f.msg||f.t||f).join(' / ').slice(0,200)})})()"""))
    await pg.wait_for_timeout(3000)
    print('no respawn',await ev("""JSON.stringify(W.ents.filter(e=>e.crewId&&e.alive).map(e=>e.job))"""))
    print('ledger',await ev(LED))
    print('elsewhere',await ev("""(()=>{const P=S.player,home=P.sector;exitSector();P.sector=NEIGH[home][0];enterSector(P.sector);return 1})()"""));await pg.wait_for_timeout(3000)
    print('none elsewhere',await ev("""W.ents.filter(e=>e.crewId).length"""),await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
