# Beyond live space stage 1 (6 Nov 2026): station miners. Every power's station, depot and the Brood's hive keeps a roster
# of miners with their kits aboard; off-screen a site mines at its roster's share of the old rate; live the roster flies
# (placed at the rocks on arrival), mines at the same average rate, unloads into the station and relaunches; a miner killed
# leaves the roster and the site's mining falls until its stores build another; no miner is spawned by chance; the ledger
# stays exact throughout
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
    print('rosters',await ev("JSON.stringify(Object.fromEntries(Object.entries(S.mrs).map(([k,r])=>[k,r.f+' '+r.m.length+'/'+mrTarget(mrSite(k))])))"))
    print('ledger',await ev(LED))
    print('no chance miners',await ev("(()=>{const ids=['hp','vb','os','hr','bl'];let n=0;for(const sid of ids){W.sid=W.sid;}return JSON.stringify(popWantsAt('hp'))})()".replace("popWantsAt('hp')","(()=>{const P=S.player;undock();exitSector();P.sector='hp';P.docked=null;enterSector('hp');return popWants().filter(w=>w[0]==='miner').length})()")))
    print('live at hp',await ev("JSON.stringify(W.ents.filter(e=>e.role==='miner').map(e=>({c:e.cls,k:e.mrKey,ast:!!e.ai.ast})))"))
    print('ledger',await ev(LED))
    # off-screen work follows the roster: hr (a depot) with its roster then with one miner gone
    print('off-screen share',await ev("""(()=>{const ro=S.mrs['S.hr'],w1=mrWork('S.hr');const m=ro.m[0];const w2=(()=>{ro.m.shift();const w=mrWork('S.hr');ro.m.unshift(m);return w})();return JSON.stringify({full:+w1.toFixed(2),less:+w2.toFixed(2)})})()"""))
    print('kill one live',await ev("(()=>{const e=W.ents.find(x=>x.role==='miner'&&x.mrKey==='S.hp');const n0=S.mrs['S.hp'].m.length,w0=mrWork('S.hp');killShip(e,'pirate',{});return JSON.stringify({n0,n1:S.mrs['S.hp'].m.length,w0:+w0.toFixed(2),w1:+mrWork('S.hp').toFixed(2),line:mrLine('S.hp')})})()"))
    print('ledger',await ev(LED))
    print('unloads and docks',await ev("""(()=>{const e=W.ents.find(x=>x.role==='miner'&&x.mrKey==='S.hp'&&x.alive);const D=W.stationEnt;devLedger(()=>{});const st=storeOf(D.rec),fe0=st.fe||0;
      const m=mrEntry(e.mrKey,e.mrId);let moved=0;devLedger(()=>{const a=S.sectors.hp.ast.find(x=>(x.ore.fe||0)>=5);if(a){inv.take(a.ore,'fe',5);inv.add(e.cargo,'fe',5);moved=5}});e.ai.state='return';e.x=D.x+60;e.y=D.y;e.z=D.z;window._M=m;return JSON.stringify({moved,id:e.mrId})})()"""))
    await pg.wait_for_timeout(2500)
    print('docked',await ev("(()=>{const m=window._M;return JSON.stringify({live:m.live,kit:m.load,back:Math.round(m.next-S.T)})})()"))
    print('ledger',await ev(LED))
    print('relaunches',await ev("(()=>{const m=window._M;m.next=S.T-1;populate(false);return JSON.stringify({live:m.live,out:W.ents.filter(e=>e.role==='miner'&&e.mrKey==='S.hp').length})})()"))
    print('rebuilds from stores',await ev("""(()=>{let r=null;devLedger(()=>{inv.add(S.econ.stock.halcyon,'plate',10);inv.add(S.econ.stock.halcyon,'wire',10)});const ro=S.mrs['S.hp'];ro.t=S.T-1;mrTick();return JSON.stringify({n:ro.m.length,line:mrLine('S.hp')})})()"""))
    print('ledger',await ev(LED))
    print('leave: kits aboard',await ev("(()=>{const P=S.player;exitSector();P.sector='mw';enterSector('mw');return JSON.stringify({live:S.mrs['S.hp'].m.filter(m=>m.live).length,kits:S.mrs['S.hp'].m.every(m=>(m.load.plate||0)>0)})})()"))
    print('ledger',await ev(LED))
    print('site lost: kits to debris',await ev("""(()=>{const R=S.stations.hr,o=R.owner;const d0=JSON.stringify(S.sectors.hr.debris);R.owner='varkesh';mrTick();const gone=!S.mrs['S.hr']||S.mrs['S.hr'].f==='varkesh';const n=S.mrs['S.hr']?S.mrs['S.hr'].m.length:0;R.owner=o;return JSON.stringify({gone,newRoster:n})})()"""))
    print('ledger',await ev(LED))
    print('save/load',await ev("(()=>{save();const j=JSON.parse(localStorage.getItem(SAVE_KEY));return JSON.stringify({sites:Object.keys(j.mrs||{}).length,live:Object.values(j.mrs||{}).reduce((a,r)=>a+r.m.filter(m=>m.live).length,0)})})()"))
    print('map line',await ev("mapSectorNow('vb').replace(/<[^>]+>/g,' ').replace(/\\s+/g,' ').trim().slice(-60)"))
    for i in range(3):
      await ev("(()=>{for(let i=0;i<30;i++){S.T+=10;strategicTick();updateEvents()}})()")
    print('an hour on',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
