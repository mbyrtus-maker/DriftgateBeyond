# Beyond: the Drone controller and drones as ammunition (3 Nov 2026). A new Light Miner has a controller fitted in its own
# utility slot; without one its drones stay in the bay; a fighter can't fit one; drones lost are refilled at Rearm when you
# dock (built by the station from its stores, paid to its treasury); a maker's controller makes tougher or harder-hitting
# drones; an older miner's fit gets the slot and a controller; the ledger stays exact throughout
import asyncio,json,os
from playwright.async_api import async_playwright
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'")
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await ev("(()=>{const r=document.querySelector('#roles [data-role=\"mining\"]');if(r)r.click();return 1})()")
    await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    print('new miner',await ev("(()=>{const P=S.player,F=fitOf(P);return JSON.stringify({cls:P.cls,u:F.u,bay:P.bay,ctl:drnCtl(P),cap:drnCap(P)})})()"))
    await ev("(()=>{undock();return 1})()");await pg.wait_for_timeout(1500)
    print('launched',await ev("(()=>{const L=W.player.drones||[];return JSON.stringify({n:L.filter(d=>d.alive).length,hull:L[0]&&Math.round(L[0].st.hull)})})()"))
    # lose both drones, dock, auto rearm refills them
    print('lost and docked',await ev("""(()=>{const P=S.player;for(const d of W.player.drones||[]){d.shield=0;damageShip(d,9999,'brood',null,'kinetic')}W.player.drones=(W.player.drones||[]).filter(d=>d.alive);P.docked='station';const c0=P.credits,R=S.stations[P.sector],t0=S.econ.treasury.neutral;openDock('ship');
      return JSON.stringify({bay:P.bay.drone,paid:c0-P.credits,toTreasury:S.econ.treasury.neutral-t0,msg:dockErr.slice(0,160)})})()"""))
    print('ledger',await ev(LED))
    # no controller, no drones
    print('controller out',await ev("(()=>{const P=S.player,F=fitOf(P),i=F.u.indexOf('dronec');dockAction('fit','u:'+i+':');return JSON.stringify({u:F.u,cap:drnCap(P),q:rearmQuote(P).drn,msg:dockErr.slice(0,80)})})()"))
    await ev("(()=>{undock();return 1})()");await pg.wait_for_timeout(1200)
    print('launched without',await ev("(W.player.drones||[]).filter(d=>d.alive).length"))
    # a fighter can't take one; a maker's controller (Corvane: +20% drone hull) at grade 2
    print('fighter refused',await ev("(()=>{const P=S.player,c=P.cls;P.docked='station';P.cls='interceptor';const m=fitDo(dockCtx(),P,'u:0:pt_dronec');P.cls=c;fitOf(P);return m})()"))
    print('maker controller',await ev("""(()=>{const P=S.player,F=fitOf(P),i=F.u.indexOf('')>=0?F.u.indexOf(''):1;const id=MK_ITEMS.dronec.find(x=>ITEMS[x].maker==='tcy');devLedger(()=>{inv.add(P.cargo,id,1)});const m=fitDo(dockCtx(),P,'u:'+i+':'+id);devLedger(()=>{F.ug[i]=2});
      return JSON.stringify({id,name:ITEMS[id].name,tr:ITEMS[id].tr,m:m.slice(0,60),ctl:drnCtl(P)})})()"""))
    await ev("(()=>{undock();return 1})()");await pg.wait_for_timeout(1200)
    print('tougher drones',await ev("(()=>{const L=(W.player.drones||[]).filter(d=>d.alive);return JSON.stringify({n:L.length,hull:L[0]&&Math.round(L[0].st.hull),base:Math.round(shipStats(S.player.faction,'drone',S.player.tiers.weapon).hull)})})()"))
    # a fit from before the change: no slot, no controller
    print('older fit',await ev("(()=>{const P=S.player;P.docked='station';devLedger(()=>{P.fit={cls:'skiff',d:null,w:['mlaser','charge'],u:['land'],g:[1,1],ug:[1],wi:[null,null],ui:[null]}});const F=fitOf(P);return JSON.stringify({u:F.u,cap:drnCap(P)})})()"))
    print('sold where',await ev("(()=>{const out={};for(const sid in S.stations){const R=S.stations[sid];let st;try{st=mkStock(R)}catch(e){continue}if(!st)continue;const n=Object.keys(st).filter(k=>ITEMS[k]&&ITEMS[k].part==='dronec').length;if(n)out[sid]=n}return JSON.stringify(out)})()"))
    print('ledger',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
