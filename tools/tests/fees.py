# Beyond: your base's fees. Defaults; the steppers clamp at their limits; steep prices sell smaller lots and cheap ones bigger;
# the docking fee is paid by traders and thins their visits; visiting pilots pay services; posted jobs wait longer behind a
# docking fee; the Holdings panel shows the Fees; the ledger stays exact
import asyncio,json,os
from playwright.async_api import async_playwright
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    await pg.wait_for_function('window.__dg&&__dg.ev("!!(S&&S.player)")',timeout=30000);await pg.evaluate("__dg.ev('coDefault(S.player)')")  # a company profile (8 Nov 2026: no Depot without one)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    print('setup',await ev("""(()=>{const P=S.player;undock();transfer('halcyon','player',20000);const sid=SECTOR_DEFS.map(d=>d.id).filter(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id])[0];
      exitSector();P.sector=sid;P.docked=null;enterSector(sid);devLedger(()=>{P.cargo={frame:2}});depFresh(P);const R=S.stations[sid];devLedger(()=>{inv.add(R.stock,'plate',4000)});R.sell={plate:0};window._S=sid;return JSON.stringify(feeOf(R))})()"""))
    print('clamp',await ev("(()=>{for(let i=0;i<20;i++)feeSet(S.player,_S+':sell:1');for(let i=0;i<40;i++)feeSet(S.player,_S+':dock:1');return JSON.stringify(feeOf(S.stations[_S]))})()"))
    # sell volume: an hour of trade at 130% vs 80%
    run="""(sell,dock)=>{const R=S.stations[_S];R.fees={sell,dock};R.eco=[];const p0=R.stock.plate;for(let i=0;i<60;i++)depTradeTick();const by=k=>R.eco.filter(e=>e.k===k).reduce((a,e)=>a+e.n,0);return{sold:p0-R.stock.plate,market:by('market'),docking:by('docking'),services:by('services'),visits:R.eco.filter(e=>e.k==='docking').length}}"""
    print('steep 130%',await ev(f"(()=>{{const f={run};return JSON.stringify(f(1.3,0))}})()"))
    print('cheap 80%',await ev(f"(()=>{{const f={run};return JSON.stringify(f(.8,0))}})()"))
    print('default',await ev(f"(()=>{{const f={run};return JSON.stringify(f(1,0))}})()"))
    print('dock 100',await ev(f"(()=>{{const f={run};return JSON.stringify(f(1,100))}})()"))
    print('dock 25',await ev(f"(()=>{{const f={run};return JSON.stringify(f(1,25))}})()"))
    print('posted wait',await ev("(()=>{const R=S.stations[_S];R.fees={dock:100};const P=S.player;pjPost(P,_S+':guard:x:0:medium');const j=pjList()[pjList().length-1];R.fees={};pjPost(P,_S+':guard:x:0:medium');const k=pjList()[pjList().length-1];return JSON.stringify({w100:Math.round(j.claimAt-j.posted),w0:Math.round(k.claimAt-k.posted)})})()"))
    print('panel',await ev("(()=>{const R=S.stations[_S];R.fees={sell:1.1,dock:50};$('company').hidden=false;coTab='holdings';coSel='D:'+_S;renderCompany();const d=$('coBody').querySelector('.codet').innerText;const i=d.indexOf('FEES');document.querySelector('#company [data-co=feeset][data-arg$=\":svc:1\"]').click();return d.slice(i,i+420).replace(/\\n/g,' | ')+' || '+JSON.stringify(feeOf(R))+' '+$('coErr').textContent})()"))
    await pg.screenshot(path='/tmp/claude-0/-home-claude/82d47366-d8e2-5d87-95a4-e70ca203b8c5/scratchpad/shots/fees.png')
    print('reset',await ev("(()=>{document.querySelector('#company [data-co=feeset][data-arg$=\":reset\"]').click();return JSON.stringify(feeOf(S.stations[_S]))})()"))
    print('ledger',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
