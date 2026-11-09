# Beyond stage 10: Depots. A Lair upgraded to a Depot in place (store from the stash, ledger exact); your market sells and buys
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
    print('market',await ev("""(()=>{const P=S.player,R=S.stations[P.sector];devLedger(()=>{inv.add(R.stock,'ir',60);inv.add(R.stock,'plate',20)});dockAction('mkset',`${R.sid}:ir:sell:10`);dockAction('mkset',`${R.sid}:cu:buy:30`);const c0=P.credits,s0=R.stock.ir;
      for(let i=0;i<12;i++)depTradeTick();return JSON.stringify({sold:s0-(R.stock.ir||0),bought:R.stock.cu||0,credits:P.credits-c0,eco:(R.eco||[]).slice(-3).map(e=>e.w)})})()"""))
    print('ledger',await ev(LED))
    print('hire',await ev("""(()=>{const P=S.player,R=S.stations[P.sector];devLedger(()=>{P.credits+=40000});const m1=crewHire(R,P,'prospector');const m2=crewHire(R,P,'freighter');return JSON.stringify({m1,m2,crew:R.crew.map(c=>c.name+':'+c.cls+':'+c.job),cap:crewCap(R)})})()"""))
    print('add a hangar',await ev("""(()=>{const R=S.stations[S.player.sector];devOf(R).hangar=1;const m=crewHire(R,S.player,'freighter');return JSON.stringify({m,crew:R.crew.map(c=>c.cls+':'+c.job)})})()"""))
    print('crews work',await ev("""(()=>{const P=S.player,R=S.stations[P.sector];const st0=invMass(R.stock),c0=P.credits;for(let i=0;i<10;i++)crewTick();return JSON.stringify({storeGain:invMass(R.stock)-st0,credits:P.credits-c0,eco:Object.entries(ecoSum(R,S.T-3600,S.T+1)).map(([k,n])=>k+' '+n)})})()"""))
    print('ledger',await ev(LED))
    print('laid up',await ev("""(()=>{const P=S.player,R=S.stations[P.sector];devLedger(()=>{R.stock.plate=0});for(let i=0;i<70;i++)crewTick();return JSON.stringify(R.crew.map(c=>c.name+(c.laid?' laid up':' working')))})()"""))
    print('unpaid',await ev("""(()=>{const P=S.player,R=S.stations[P.sector];devLedger(()=>{P.credits=0});for(let i=0;i<3;i++)crewTick();return JSON.stringify({crew:R.crew.length})})()"""))
    print('ledger',await ev(LED))
    print('tabs',await ev("""(()=>{$('company').hidden=false;const o={};for(const t of['holdings','economy','crews']){coTab=t;renderCompany();o[t]=$('coBody').innerText.slice(0,140).replace(/\\n/g,' | ')}return JSON.stringify(o)})()"""))
    await ev("(()=>{$('company').hidden=true;undock();return 1})()");await pg.wait_for_timeout(20000)
    print('after flight',await ev("JSON.stringify({T:Math.round(S.T)})"),await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
