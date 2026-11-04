# Beyond: freeports never fall (3 Nov 2026). The Brood razing a freeport knocks it out instead: still there, dark for five
# minutes (no market, no jobs, no docking), then lit again at half hull; a freeport an older galaxy lost is rebuilt; ledger exact
import asyncio,json,os
from playwright.async_api import async_playwright
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1200,'height':800});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    print('defences',await ev("(()=>{const P=S.player;undock();exitSector();P.sector='cw';P.docked=null;enterSector('cw');const R=S.stations.cw,E=W.stationEnt;mdlStationTurrets(E);return JSON.stringify({sMax:R.sMax,hMax:R.hMax,turrets:E.turrets.length,placed:E.turrets.filter(t=>t.p&&(t.p[0]||t.p[1]||t.p[2])).length,range:E.range})})()"))
    print('distress',await ev("(()=>{S.distress=[];FEED.length=0;razeStation('cw','brood');const d=(S.distress||[]).find(x=>x.sid==='cw');S.fpDark={};return JSON.stringify({call:!!d,fac:d&&d.fac,heard:FEED.some(f=>/Distress call from Coldwater/.test(f.msg))})})()"))
    print('razed',await ev("(()=>{const P=S.player;undock();exitSector();P.sector='cw';P.docked=null;enterSector('cw');razeStation('cw','brood');const R=S.stations.cw;return JSON.stringify({still:!!R,dark:fpDark('cw'),canDock:canDock(W.stationEnt),ent:!!W.stationEnt})})()"))
    print('docked view',await ev("(()=>{const P=S.player;P.docked='station';const c=dockCtx();P.docked=null;return JSON.stringify({market:!!c.market,jobs:!!c.contracts,sub:c.sub})})()"))
    print('relit',await ev("(()=>{S.T+=301;strategicTick();const R=S.stations.cw;return JSON.stringify({dark:fpDark('cw'),hull:Math.round(R.hull/R.hMax*100)+'%',canDock:canDock(W.stationEnt)})})()"))
    print('lost one rebuilt',await ev("(()=>{devLedger(()=>{delete S.stations.ew});strategicTick();return JSON.stringify({back:!!S.stations.ew,name:S.stations.ew&&S.stations.ew.name})})()"))
    print('ledger',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
