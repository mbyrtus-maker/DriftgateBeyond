# Beyond 12c: the Dread Pirate. Rolled with two pirate traits, shown on the Allegiance tab, flies (spawned with an escort in a
# live system, or aboard the Ravager), killed by a pilot: every power pays the bounty and a Paranoid captain takes the hat with a
# bounty on that pilot; its events (raiding season, tribute, hoard sale, open house, lie low) run with the ledger exact;
# the hunt job at a power's station and the rumour of its whereabouts at the Rusty Tankard
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
    print('dread',await ev("JSON.stringify({name:S.dread.name,traits:S.dread.traits,prof:LEADP.pirate,ship:S.dread.ship.sid})"))
    print('allegiance',await ev("(()=>{const h=allegianceHtml(S.player);return h.includes('The Unbound')&&h.includes(S.dread.name)})()"))
    print('spawn',await ev("""(()=>{const P=S.player,D=S.dread;S.frigates=S.frigates.filter(t=>t.side!=='pirate');exitSector();P.sector='wr';P.docked=null;D.ship.sid='wr';D.ship.live=0;D.ship.move=S.T+999;enterSector('wr');strategicTick();const e=dpEnt();return JSON.stringify({ent:!!e,pname:e&&e.pname,cls:e&&e.cls,hull:e&&Math.round(e.hull),escort:W.ents.filter(x=>x.alive&&x.side==='pirate'&&x.tier===4).length})})()"""))
    print('killed by you',await ev("""(()=>{const P=S.player,D=S.dread,e=dpEnt(),c0=P.credits,n0=D.name;e.hull=1;e.shield=0;killShip(e,'player',{src:W.player});const N=S.dread;return JSON.stringify({paid:P.credits-c0,old:n0,new:N.name,n:N.n,traits:N.traits,why:N.why,bountyOnYou:N.bounty[pkeyOf(P)]||0,flying:N.ship.alive})})()"""))
    print('ledger',await ev(LED))
    print('back',await ev("""(()=>{const D=S.dread;S.T=D.ship.back+1;strategicTick();return JSON.stringify({alive:D.ship.alive,sid:D.ship.sid})})()"""))
    print('ravager carries it',await ev("""(()=>{const D=S.dread;const t=makeCarrier('pirate','wr',{});D.ship.alive=true;strategicTick();const a={rav:D.ship.rav===t.id,sid:D.ship.sid===t.sector};const n0=D.name;devLedger(()=>{S.frigates=S.frigates.filter(x=>x!==t)});strategicTick();a.sunk=S.dread.name!==n0;a.why=S.dread.why;return JSON.stringify(a)})()"""))
    print('ledger',await ev(LED))
    print('events',await ev("""(()=>{const D=S.dread,out={};for(const f of FAC_IDS)transfer('player',f,0);devLedger(()=>{inv.add(S.econ.stock.pirate,'plate',800)});S.econ.treasury.pirate=Math.max(S.econ.treasury.pirate,0);
      for(let i=0;i<60;i++){D.cool=0;dpAct();}return JSON.stringify({season:!!D.season,sale:!!D.sale,house:!!D.house,low:!!D.low})})()"""))
    print('ledger',await ev(LED))
    print('hoard sale price',await ev("""(()=>{const D=S.dread,R=S.stations.wr;D.sale=0;const a=stPrice(R,'plate');D.sale=S.T+100;const b=stPrice(R,'plate');return (b/a).toFixed(2)})()"""))
    print('hunt job',await ev("""(()=>{const P=S.player,D=S.dread;D.ship.alive=true;const hs=Object.keys(S.stations).find(s=>S.stations[s].owner==='halcyon'&&S.stations[s].kind==='core');exitSector();P.sector=hs;enterSector(hs);P.docked='station';const c=dockCtx();const L=jobsList(c,P,[P.cargo]);P.docked=null;const j=L.find(x=>String(x.id).startsWith('dp:'));return j?j.title+' · '+j.sub+' · '+j.pay:'none'})()"""))
    print('rumour',await ev("""(()=>{const P=S.player;exitSector();P.sector='wr';enterSector('wr');P.docked='station';const c=dockCtx();P.credits=Math.max(P.credits,0);devLedger(()=>{});transfer('halcyon','player',400);const c0=P.credits;dockAction('dpword','');P.docked=null;return dockErr+' · paid '+(c0-P.credits)})()"""))
    print('ledger',await ev(LED))
    await pg.wait_for_timeout(15000)
    print('after flight',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
