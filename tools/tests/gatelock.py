# Beyond 6c (6 Nov 2026): gate lock kits. Scrapheart makes a kit from the Unbound's stores and sells it for 2,500 cr, one per
# pilot per hour; it counts as pirate gear; set within 300 m of a gate (not a freeport's or the Wrack's) it arms in 20 s with
# a quarter of its health, then seals the gate both ways for 5 minutes; it shows on both sides of the gate as one hull and
# breaking it from the far side opens the gate (the power pays the breaker); burnt out, its materials fall as debris; a convoy
# reaching it waits; off-screen traffic routes round it; the Unbound lock a gate for a convoy their raiders wait for; the
# powers post a job to break it; the HUD chip; the ledger stays exact throughout
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
    print('the haven makes a kit',await ev("""(()=>{devLedger(()=>{inv.add(S.econ.stock.pirate,'plate',10);inv.add(S.econ.stock.pirate,'wire',10)});const st=mkStock(S.stations.wr),n0=st.glock||0;S.glMakeT=0;glTick();const n1=st.glock||0;glTick();return JSON.stringify({before:n0,after:n1,again:st.glock||0,next:Math.round(S.glMakeT-S.T)})})()"""))
    print('ledger',await ev(LED))
    print('bought at Scrapheart',await ev("""(()=>{const P=S.player;undock();exitSector();P.sector='wr';P.docked=null;enterSector('wr');P.docked='station';transfer('halcyon','player',6000);const c0=P.credits;dockAction('buy','glock:1');const m=dockErr,paid=c0-P.credits;dockAction('buy','glock:1');return JSON.stringify({m,paid,kits:P.cargo.glock||0,again:dockErr,gear:gearOn(P)})})()"""))
    print('ledger',await ev(LED))
    print('not on the Wrack',await ev("glWhyNot('wr',NEIGH.wr[0])"))
    # a Halcyon frontier gate
    print('at a gate',await ev("""(()=>{const P=S.player;P.docked=null;const ids=SECTOR_DEFS.map(d=>d.id),ok=(id,n)=>!glWhyNot(id,n),sid=ids.find(id=>sectorOwner(id)==='halcyon'&&!DEF[id].home&&NEIGH[id].some(n=>ok(id,n)))||ids.find(id=>sectorOwner(id)==='halcyon'&&NEIGH[id].some(n=>ok(id,n)))||ids.find(id=>NEIGH[id].some(n=>ok(id,n)));const to=NEIGH[sid].find(n=>ok(sid,n));
      exitSector();P.sector=sid;enterSector(sid);const g=GATES[sid].find(x=>x.to===to),p=W.player;p.x=g.x*.94;p.y=g.y*.94;p.z=g.z*.94;p.vx=p.vy=p.vz=0;window._A=sid;window._B=to;return JSON.stringify({sid,to,dist:Math.round(d3(p,g)),chip:convoyChip()})})()"""))
    print('set it',await ev("""(()=>{const P=S.player;dockAction('glock',window._B);const L=glOf(window._A,window._B);const e=W.ents.find(x=>x.alive&&x.glId===(L&&L.id));return JSON.stringify({m:dockErr,stage:L&&L.stage,hp:L&&L.hp,ent:!!e,hull:e&&Math.round(e.hull),down:!!S.gateDown[gateKey(window._A,window._B)],kits:P.cargo.glock||0})})()"""))
    print('ledger',await ev(LED))
    print('armed',await ev("""(()=>{const L=glOf(window._A,window._B);L.t0=S.T-GL.arm-1;glTick();worldUpdate(1/60);const e=W.ents.find(x=>x.alive&&x.glId===L.id);return JSON.stringify({stage:L.stage,hp:L.hp,hull:e&&Math.round(e.hull),down:Math.round(S.gateDown[L.key]-S.T),txt:ogTxt(window._A,window._B)})})()"""))
    print('a convoy waits at it',await ev("""(()=>{const g=W.ents.find(x=>x.type==='gate'&&x.to===window._B);const e=makeNPC('trader','halcyon','freighter',1,{},'trader:-9:halcyon');e.ai.dest=g;return gateLocked(e)})()"""))
    print('off-screen traffic routes round it',await ev("""(()=>{glRouting=true;try{const s=!!ogSealed(window._A,window._B),r=ogRoute(window._A,window._B);return JSON.stringify({sealed:s,route:r&&r.length})}finally{glRouting=false}})()"""))
    print('break-it job',await ev("""(()=>{const P=S.player,hs=Object.keys(S.stations).find(s=>S.stations[s].owner==='halcyon'&&S.stations[s].kind==='core');exitSector();P.sector=hs;enterSector(hs);P.docked='station';const c=dockCtx();const L=jobsList(c,P,[P.cargo]);P.docked=null;const j=L.find(x=>String(x.id).startsWith('gl:'));return j?j.title+' · '+j.pay:'none'})()"""))
    print('hit from the far side',await ev("""(()=>{const P=S.player,L=glOf(window._A,window._B);exitSector();P.sector=window._B;enterSector(window._B);worldUpdate(1/60);const e=W.ents.find(x=>x.alive&&x.glId===L.id);e.hull=900;worldUpdate(1/60);return JSON.stringify({ent:!!e,lockHp:Math.round(L.hp)})})()"""))
    print('broken',await ev("""(()=>{const P=S.player,L=glOf(window._A,window._B),e=W.ents.find(x=>x.alive&&x.glId===L.id),c0=P.credits;e.hull=1;killShip(e,'player',{src:W.player});return JSON.stringify({gone:!glOf(window._A,window._B),down:!!S.gateDown[gateKey(window._A,window._B)],paid:P.credits-c0})})()"""))
    print('ledger',await ev(LED))
    print('burns out',await ev("""(()=>{let L=null;devLedger(()=>{});L=glPlace(window._A,window._B,'pirate');L.load={};devLedger(()=>{L.load={plate:1,wire:1}});L.t0=S.T-GL.arm-1;glTick();L.until=S.T-1;glTick();return JSON.stringify({gone:!glOf(window._A,window._B),down:!!S.gateDown[gateKey(window._A,window._B)]})})()"""))
    print('ledger',await ev(LED))
    print('the Unbound lock a convoy gate',await ev("""(()=>{const st=mkStock(S.stations.wr);if(!(st.glock>0)){devLedger(()=>{inv.add(st,'glock',1)})}const k0=st.glock;const t={id:-5,path:[window._A,window._B],leg:0,sector:window._A};const r=Math.random;Math.random=()=>0;let L=null;try{L=glUnbLock(t)}finally{Math.random=r}return JSON.stringify({lock:!!L,by:L&&L.by,stage:L&&L.stage,kitsUsed:k0-(st.glock||0)})})()"""))
    print('ledger',await ev(LED))
    await pg.wait_for_timeout(8000)
    print('after flight',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
