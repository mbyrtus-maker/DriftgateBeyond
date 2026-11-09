# Beyond live space stage 1b (6 Nov 2026): your crews do real work. A mining crew drills a real rock live and unloads at the
# depot; a hauling crew flies its load to a market on the lanes (out of sight), sells it, comes home; a hauling crew shot down
# on its run is lost with its hold as salvage; the ledger stays exact throughout
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
    print('depot and crews',await ev("""(()=>{const P=S.player;undock();P.rp=5000;const sid=SECTOR_DEFS.map(d=>d.id).find(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id]&&S.sectors[id].ast.some(a=>!a.rift&&oreTotal(a)>40));exitSector();P.sector=sid;P.docked=null;enterSector(sid);P.cls='bulker';fitOf(P);refreshPlayerStats();devLedger(()=>{P.cargo={frame:2}});
      depFresh(P);transfer('halcyon','player',30000);const R=S.stations[sid];devOf(R).hangar=2;window._SID=sid;const p=W.player;p.x=4000;p.y=2000;p.z=4000;const a=crewHire(R,P,'prospector'),b=crewHire(R,P,'freighter');devLedger(()=>{inv.add(R.stock,'plate',40);inv.add(R.stock,'fe',60)});R.sell={fe:0};return JSON.stringify({sid,a,b,crews:R.crew.map(c=>c.cls+':'+c.job)})})()"""))
    await pg.wait_for_timeout(2500)
    print('ledger',await ev(LED))
    await pg.wait_for_timeout(30000)
    print('crew miner drilling',await ev("(()=>{const e=W.ents.find(x=>x.crewId&&x.job==='mine');return JSON.stringify({cargo:e?invMass(e.cargo):-1,mining:!!(e&&e.mining)})})()"))
    print('ledger',await ev(LED))
    print('unloads',await ev("(()=>{const e=W.ents.find(x=>x.crewId&&x.job==='mine');const R=S.stations[window._SID];inv.add(e.cargo,'fe',0);e.cargo.fe=(e.cargo.fe||0);window._st0=invMass(R.stock);const need=DEP.mine[e.cls]*4-invMass(e.cargo);const a=S.sectors[W.sid].ast.find(x=>(x.ore.fe||0)>need+2);if(a&&need>0){inv.take(a.ore,'fe',need);inv.add(e.cargo,'fe',need)}e.x=W.stationEnt.x+120;e.y=W.stationEnt.y;e.z=W.stationEnt.z;return 'ok'})()"))
    await pg.wait_for_timeout(3000)
    print('into the store',await ev("(()=>Math.round(invMass(S.stations[window._SID].stock)-window._st0))()"))
    print('ledger',await ev(LED))
    print('a hauling run out of sight',await ev("""(()=>{const P=S.player,R=S.stations[window._SID],c=R.crew.find(x=>x.job==='haul');exitSector();const c0=P.credits;c.hT=200;crewTick();const r=crRunOf(c.run);if(!r)return 'no run';const out=JSON.stringify({load:r.load,to:r.mk,hops:r.path.length-1});
      for(let i=0;i<200&&c.run;i++){S.T+=10;crRunsTick()}enterSector(window._SID);return out+' '+JSON.stringify({home:!c.run,earned:P.credits-c0,fe:R.stock.fe})})()"""))
    print('ledger',await ev(LED))
    print('shot down on a run',await ev("""(()=>{const R=S.stations[window._SID],c=R.crew.find(x=>x.job==='haul');devLedger(()=>{inv.add(R.stock,'fe',30)});c.hT=200;crewTick();const r=crRunOf(c.run);if(!r)return 'no run';const e=W.ents.find(x=>x.crRun===r.id);if(!e)return 'not live';const n0=R.crew.length;killShip(e,'pirate',{});return JSON.stringify({crews:n0+'->'+R.crew.length,run:!!crRunOf(r.id),crates:S.sectors[W.sid].crates.length})})()"""))
    print('ledger',await ev(LED))
    await pg.wait_for_timeout(3000)
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
