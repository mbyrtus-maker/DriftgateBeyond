# Beyond stage 13: declaring a faction. 20 systems for 10 minutes wins, no deadline; declaring needs a Station; a declared
# faction counts its Stations and draws the truce when it leads; proposals (alliance, tribute) answered; losing the last
# Station ends it; the Brood's strength follows the systems it holds
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
    print('rules',await ev("JSON.stringify({need:VIC_NEED,minutes:WIN_TIME/60,deadline:TIE_T>1e9,holdable:SECTOR_DEFS.filter(d=>!FREEPORTS.some(f=>f.sid===d.id)&&d.id!=='wr').length,clock:document.getElementById('hClock').hidden})"))
    print('without a station',await ev("(()=>{dockAction('declare');return dockErr})()"))
    print('station',await ev("""(()=>{const P=S.player;undock();P.rp=5000;const sid=SECTOR_DEFS.map(d=>d.id).find(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id]);exitSector();P.sector=sid;P.docked=null;enterSector(sid);P.cls='bulker';fitOf(P);refreshPlayerStats();devLedger(()=>{P.cargo={frame:2}});depFresh(P);const R=S.stations[sid];
      devLedger(()=>{inv.add(R.stock,'keel',1);inv.add(R.stock,'frame',2);inv.add(R.stock,'seal',1)});staUp(P,R);window._R=R;return JSON.stringify({sid,owner:sectorOwner(sid),counts:controlCounts().player||0})})()"""))
    print('declare',await ev("(()=>{dockAction('declare');return JSON.stringify({msg:dockErr,decl:S.player.decl,counts:controlCounts().player||0})})()"))
    print('truce on the leader',await ev("""(()=>{const keep=sectorOwner;let fake=0;sectorOwner=function(id){if(fake<VIC_NEED&&!DEF[id].home&&!FREEPORTS.some(f=>f.sid===id)&&id!=='wr'&&id!=='bl'){return 'player'}return keep.apply(this,arguments)};const n=controlCounts();S.coal=null;coalTick();const C=S.coal;sectorOwner=keep;const h=hostile('varkesh','player');S.coal=null;return JSON.stringify({playerSystems:n.player,coal:C&&{lead:C.lead,mem:C.mem},hostile:h})})()"""))
    print('proposals',await ev("""(()=>{const P=S.player;P.stand.halcyon=50;P.stand.varkesh=-40;S.propT={};declTick();const L=(P.props||[]).map(x=>x.f+':'+x.k);const a=P.props.find(x=>x.k==='ally'),d=P.props.find(x=>x.k==='demand');const r1=a?propAnswer(P,a.id,true):'';const r2=d?propAnswer(P,d.id,false):'';return JSON.stringify({props:L,ally:r1,demand:r2,allied:P.allied,hostileVarkesh:hostile('varkesh','player')})})()"""))
    print('ledger',await ev(LED))
    print('tab',await ev("(()=>{$('company').hidden=false;coTab='allegiance';renderCompany();return $('coBody').innerText.slice(0,260).replace(/\\n/g,' | ')})()"))
    print('loses its station',await ev("""(()=>{const P=S.player,R=_R;devLedger(()=>{delete S.stations[R.sid]});declTick();return JSON.stringify({decl:P.decl})})()"""))
    print('brood ramp',await ev("JSON.stringify([1,3,5,8,12,15].map(n=>n+':'+broodK(n).toFixed(2)))"))
    print('brood now',await ev("(()=>{broodRamp();return JSON.stringify({n:controlCounts().brood||0,k:S.broodK,brOff:+BAL.brOff.toFixed(3),hives:BAL.brLevT<1e9})})()"))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
