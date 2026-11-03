# Beyond stage 11: Stations. A Depot doesn't hold the system, a Station does; upgrading takes a keel, frames and a seal
# (ledger exact); buildings one per level with their effects (hangar, defence, forge, yard); an Escort laid down at level 3
# and launched from your slip
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
    print('depot',await ev("""(()=>{const P=S.player;undock();P.rp=5000;const sid=SECTOR_DEFS.map(d=>d.id).find(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id]);exitSector();P.sector=sid;P.docked=null;enterSector(sid);P.cls='bulker';fitOf(P);refreshPlayerStats();devLedger(()=>{P.cargo={frame:2}});
      const m=depFresh(P);return JSON.stringify({sid,msg:m,owner:sectorOwner(sid),station:!!W.stationEnt})})()"""))
    print('ledger',await ev(LED))
    print('station',await ev("""(()=>{const P=S.player,R=S.stations[P.sector];const a=staUp(P,R);devLedger(()=>{inv.add(R.stock,'keel',1);inv.add(R.stock,'frame',2);inv.add(R.stock,'seal',1)});const m=staUp(P,R);return JSON.stringify({without:a,msg:m,owner:sectorOwner(P.sector),hMax:R.hMax,lvl:staLvl(R)})})()"""))
    print('ledger',await ev(LED))
    print('buildings',await ev("""(()=>{const P=S.player,R=S.stations[P.sector];devLedger(()=>{inv.add(R.stock,'frame',5);inv.add(R.stock,'plate',100);inv.add(R.stock,'coil',20)});const cap0=crewCap(R),h0=R.hMax;const out=[];for(const k of['hangar','defence','yard','forge'])out.push(staBuild(P,R,k));
      P.docked='station';const c=dockCtx();return JSON.stringify({out,lvl:staLvl(R),crew:[cap0,crewCap(R)],hull:[h0,R.hMax],fab:c.fab,forge:c.forge,hulls:c.hulls,sub:c.sub,yard:S.yards[yardKeyOf(R)]})})()"""))
    print('ledger',await ev(LED))
    print('escort',await ev("""(()=>{const P=S.player,R=S.stations[P.sector];devLedger(()=>{inv.addAll(R.stock,escCost('player'))});const m=capBuild(P,R,'esc');const ev=S.events.find(e=>e.type==='escbuild'&&e.att===yardKeyOf(R));const n0=S.frigates.filter(fMine).length;S.T=ev.until+1;capitalTick();
      const mine=S.frigates.filter(fMine);return JSON.stringify({msg:m,launched:mine.length-n0,ship:mine.map(t=>t.name+' '+t.cls+' '+t.side+' @'+t.sector),carrier:capBuild(P,R,'car')})})()"""))
    print('ledger',await ev(LED))
    print('holdings',await ev("(()=>{$('company').hidden=false;coTab='holdings';renderCompany();return $('coBody').innerText.slice(0,300).replace(/\\n/g,' | ')})()"))
    await ev("(()=>{$('company').hidden=true;if(S.player.docked)undock();return 1})()");await pg.wait_for_timeout(20000)
    print('after flight',await ev("JSON.stringify({T:Math.round(S.T)})"),await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
