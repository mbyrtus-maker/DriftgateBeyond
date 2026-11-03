# Beyond stage 12b: the new galaxy and Scrapheart. 46 systems, planar gate links, every freeport with two gates that both lead
# into deep space; Scrapheart docks a peaceful contractor (market, rumours) and its guns and the Wrack's Unbound hold fire
# until you attack them; a rumour run paid by the Unbound (ledger exact); Unbound holds are bigger
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
    print('galaxy',await ev("""(()=>{const cross=(a,b,c,d)=>{const o=(p,q,r)=>(q.x-p.x)*(r.y-p.y)-(q.y-p.y)*(r.x-p.x);return o(a,b,c)*o(a,b,d)<0&&o(c,d,a)*o(c,d,b)<0};let x=0;for(let i=0;i<LINKS.length;i++)for(let j=i+1;j<LINKS.length;j++){const[a,b2]=LINKS[i],[c,d]=LINKS[j];if(new Set([a,b2,c,d]).size===4&&cross(DEF[a],DEF[b2],DEF[c],DEF[d]))x++}
      const fp=FREEPORTS.map(f=>f.sid+':'+NEIGH[f.sid].map(n=>DEF[n].kind).join('/'));return JSON.stringify({systems:SECTOR_DEFS.length,links:LINKS.length,crossings:x,freeports:fp,bloom:DEF.bl.kind,wrack:NEIGH.wr.map(n=>DEF[n].kind)})})()"""))
    print('unbound holds',await ev("JSON.stringify(['raider','corsair','plunderer','uskiff'].map(k=>k+':'+CLASSES[k].cargo))"))
    print('dock at scrapheart',await ev("""(()=>{const P=S.player;exitSector();P.sector='wr';P.docked=null;enterSector('wr');const E=W.stationEnt;return JSON.stringify({station:E&&E.fac,canDock:!!E&&canDock(E),guns:E?stHostile(E,W.player):null,unbound:hostile('pirate','player')})})()"""))
    print('ctx',await ev("""(()=>{const P=S.player;P.docked='station';const c=dockCtx();for(let i=0;i<40;i++)fixerTick();dockTab='jobs';renderDock();const L=JOBS_LAST.filter(j=>String(j.id).startsWith('bmr:'));return JSON.stringify({sub:c.sub,market:!!c.market,wallet:c.wallet,rumours:L.map(j=>j.title+' · '+j.pay).slice(0,3)})})()"""))
    print('run',await ev("""(()=>{const P=S.player;P.cls='bulker';fitOf(P);refreshPlayerStats();P.rp=5000;devLedger(()=>{P.cargo={}});P.run=null;const x=(S.bm||[]).find(y=>y.from==='wr'&&!y.taken);if(!x)return 'no rumour';dockAction('bmtake',x.id);const m=dockErr,R=P.run;if(!R)return m;const c0=P.credits,t0=S.econ.treasury.pirate;exitSector();P.sector=R.to;enterSector(R.to);P.docked='station';openDock();return JSON.stringify({take:m,paid:P.credits-c0,fromUnbound:t0-S.econ.treasury.pirate,run:P.run})})()"""))
    print('ledger',await ev(LED))
    print('peace breaks',await ev("""(()=>{const P=S.player;exitSector();P.sector='wr';P.docked=null;enterSector('wr');const a=hostile('pirate','player');standHit(P,'pirate',10,'ship');const b=hostile('pirate','player');return JSON.stringify({before:a,after:b,canDock:canDock(W.stationEnt)})})()"""))
    await pg.wait_for_timeout(20000)
    print('after flight',await ev("JSON.stringify({T:Math.round(S.T)})"),await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
