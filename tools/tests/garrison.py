# Beyond live space stage 2 (6 Nov 2026): garrisons. Every station, depot, outpost and the hive a power or the Brood holds
# keeps a garrison of fighters with their kits aboard; live they fly as the system's patrol wing (no chance patrols); a ship
# that breaks off flies home and docks and relaunches with the others; one killed leaves the garrison until the stores build
# another; off-screen the garrison defends its site and loses ships in the fight; a site that changes hands loses its
# garrison; the ledger stays exact throughout
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
    print('garrisons',await ev("JSON.stringify(Object.fromEntries(Object.entries(S.gar).map(([k,r])=>[k,r.f+' '+r.m.map(m=>m.c[0]+m.t).join('')])))"))
    print('ledger',await ev(LED))
    print('to hp',await ev("""(()=>{const P=S.player;undock();exitSector();P.sector='hp';P.docked=null;enterSector('hp');const pw=popWants().filter(w=>w[0]==='patrol').length;
      const g=W.ents.filter(e=>e.grKey);return JSON.stringify({chancePatrols:pw,flying:g.map(e=>e.cls+':'+e.role),wing:g.length&&g.every(e=>e.grp===g[0].grp),line:grLine('S.hp')})})()"""))
    print('ledger',await ev(LED))
    print('one killed',await ev("(()=>{const e=W.ents.find(x=>x.grKey==='S.hp');killShip(e,'pirate',{});return grLine('S.hp')})()"))
    print('ledger',await ev(LED))
    print('one breaks off and docks',await ev("""(()=>{const e=W.ents.find(x=>x.grKey==='S.hp'&&x.alive);const D=W.stationEnt;e.role='flee';e.x=D.x+150;e.y=D.y;e.z=D.z;window._E=e;return 'ok'})()"""))
    await pg.wait_for_timeout(3000)
    print('docked',await ev("(()=>{const e=window._E,m=grEntry('S.hp',e.grId);return JSON.stringify({gone:!W.ents.includes(e),live:m&&m.live,kit:m&&m.load})})()"))
    print('ledger',await ev(LED))
    print('relaunch',await ev("(()=>{const ro=S.gar['S.hp'];for(const m of ro.m)m.next=S.T-1;populate(false);return JSON.stringify({out:W.ents.filter(e=>e.grKey==='S.hp'&&e.alive).length,roster:ro.m.length})})()"))
    print('leave',await ev("(()=>{const P=S.player;exitSector();P.sector='mw';enterSector('mw');return JSON.stringify({live:S.gar['S.hp'].m.filter(m=>m.live).length})})()"))
    print('ledger',await ev(LED))
    print('rebuilt',await ev("""(()=>{devLedger(()=>{inv.add(S.econ.fleet.halcyon,'plate',12);inv.add(S.econ.fleet.halcyon,'wire',8)});const ro=S.gar['S.hp'];ro.t=S.T-1;grTick();return grLine('S.hp')})()"""))
    print('ledger',await ev(LED))
    # off-screen: the depot hr is besieged and its garrison fights
    print('siege',await ev("""(()=>{const ro=S.gar['S.hr'],n0=ro.m.length;const force={};devLedger(()=>{});const f=S.econ.stock.varkesh;for(let i=0;i<4;i++){const ld=loadout('patrol',1,'striker');if(takeFrom(ld,[f]))inv.addAll(force,ld)}inv.add(force,'torpedo',inv.take(f,'torpedo',8));
      const ev={id:S.nextId++,type:'offensive',att:'varkesh',st:'hr',sector:'hr',force,cls:'raider',stage:'engaged'};S.events.push(ev);const r=Math.random;let k=0;Math.random=()=>{k++;return .99};try{resolveAbstract(ev)}finally{Math.random=r}
      return JSON.stringify({before:n0,after:ro.m.length,line:grLine('S.hr'),owner:S.stations.hr.owner})})()"""))
    print('ledger',await ev(LED))
    print('a lost fight',await ev("""(()=>{const s=S.sectors.hr,d0=s.debris.fe+s.debris.cu+s.debris.ir,force={};const ships=grForce('S.hr',force);const n=grSettle('S.hr',ships.slice(0,2).concat([]),force,1,s);grSettle('S.hr',ships.slice(2),force,0,s);return JSON.stringify({fought:ships.length,lost:n,left:S.gar['S.hr'].m.length,debris:Math.round(s.debris.fe+s.debris.cu+s.debris.ir-d0),forceLeft:invMass(force),line:grLine('S.hr')})})()"""))
    print('ledger',await ev(LED))
    print('site lost',await ev("(()=>{const o=S.outposts.kestrel;const was=o.owner;o.owner='halcyon';grTick();const n=S.gar['O.kestrel']?S.gar['O.kestrel'].m.length:0;o.owner='varkesh';grTick();const v=S.gar['O.kestrel']&&S.gar['O.kestrel'].f;o.owner=was;grTick();return JSON.stringify({built:n,taken:v,after:!!S.gar['O.kestrel']})})()"))
    print('ledger',await ev(LED))
    print('hive wings',await ev("(()=>{const P=S.player;exitSector();P.sector='bl';enterSector('bl');const gs=new Set(W.ents.filter(e=>e.grKey==='S.bl').map(e=>e.grp.id));return JSON.stringify({ships:W.ents.filter(e=>e.grKey==='S.bl').length,wings:gs.size})})()"))
    print('map',await ev("mapSectorNow('hp').replace(/<[^>]+>/g,' ').replace(/\\s+/g,' ').trim().slice(-70)"))
    print('ledger',await ev(LED))
    for i in range(3):await ev("(()=>{for(let i=0;i<30;i++){S.T+=10;strategicTick();updateEvents()}})()")
    print('an hour on',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
