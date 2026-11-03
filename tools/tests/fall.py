# Beyond: when your base falls. A power that breaks your Station captures it (75-90% hull, its buildings and store, holding
# the system for the power; your crews leave) or destroys it; you take a captured base back by breaking its hull; a Lair worn
# down by a power is impounded (its stash into the power's stores) or destroyed; the ledger stays exact throughout
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
    print('station',await ev("""(()=>{const P=S.player;undock();P.rp=5000;const sid=SECTOR_DEFS.map(d=>d.id).find(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id]);exitSector();P.sector=sid;P.docked=null;enterSector(sid);P.cls='bulker';fitOf(P);refreshPlayerStats();devLedger(()=>{P.cargo={frame:2}});
      depFresh(P);const R=S.stations[sid];devLedger(()=>{inv.add(R.stock,'keel',1);inv.add(R.stock,'frame',3);inv.add(R.stock,'seal',1);inv.add(R.stock,'plate',60);inv.add(R.stock,'coil',8);inv.add(R.stock,'fe',200)});staUp(P,R);staBuild(P,R,'hangar');R.crew=[{id:S.nextId++,name:'Test',cls:'skiff',job:'idle',laid:false,hired:S.T}];window._SID=sid;
      return JSON.stringify({sid,pst:!!R.pst,owner:sectorOwner(sid),bld:R.bld,store:invMass(R.stock)})})()"""))
    print('ledger',await ev(LED))
    print('captured',await ev("""(()=>{const sid=window._SID,R=S.stations[sid];FALL.cap.station=9;relInit();for(const f of FAC_IDS)S.leaders[f].traits=[];const t0=invMass(R.stock);razeStation(sid,'varkesh');const R2=S.stations[sid];
      return JSON.stringify({there:!!R2,owner:R2&&R2.owner,sector:sectorOwner(sid),hull:R2&&Math.round(R2.hull/R2.hMax*100)+'%',bld:R2&&R2.bld,store:[t0,R2&&invMass(dStore(R2))],crews:R2&&R2.crew.length,was:!!(R2&&R2.was),ent:W.stationEnt&&W.stationEnt.fac})})()"""))
    print('ledger',await ev(LED))
    print('taken back',await ev("""(()=>{const sid=window._SID;razeStation(sid,'player');const R=S.stations[sid];return JSON.stringify({owner:R.owner,mine:myDepots(S.player).includes(R),sector:sectorOwner(sid),store:invMass(R.stock),hull:Math.round(R.hull/R.hMax*100)+'%',bld:R.bld})})()"""))
    print('ledger',await ev(LED))
    print('destroyed',await ev("""(()=>{const sid=window._SID;FALL.cap.station=-9;captureDepot(sid,'halcyon');return JSON.stringify({there:!!S.stations[sid]})})()"""))
    print('ledger',await ev(LED))
    print('lair impounded',await ev("""(()=>{const P=S.player,sid=window._SID;P.cls='freighter';fitOf(P);refreshPlayerStats();const a=S.sectors[sid].ast.filter(r=>oreTotal(r)>=60&&!r.rift)[0];if(!a)return 'no rock';const e=W.player;e.x=a.x+astR(a)+200;e.y=a.y;e.z=a.z;
      devLedger(()=>{P.cargo={frame:1,plate:6}});const m=lairBuildB();const L=lairsOf(P)[0];if(!L)return m;L.build=0;devLedger(()=>{inv.add(L.stash,'ir',40)});FALL.lair=9;L.seen.varkesh=1;P.stand.varkesh=-70;const n=makeNPC('patrol','varkesh','striker',1,{},null);n.x=L.x+600;n.y=L.y;n.z=L.z;W.ents.push(n);L.hull=5;
      const v0=S.econ.stock.varkesh.ir||0;for(let i=0;i<200&&lairsOf(P).length;i++)lairWorldB(1);return JSON.stringify({gone:!lairsOf(P).length,toVarkesh:(S.econ.stock.varkesh.ir||0)-v0})})()"""))
    print('ledger',await ev(LED))
    await pg.wait_for_timeout(10000)
    print('after flight',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
