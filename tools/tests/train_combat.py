# Beyond training, section 3 (Combat): the section starts a contractor in a Light Fighter at the freeport; every step
# completes from the game's own actions: targeting and cycling practice drones, the laser, a kill, a missile, flares, the
# rest of the drones, scooping a salvage crate, two live Unbound raiders, a distress call; ledger exact
import asyncio,json,sys
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
SHOT=sys.argv[1] if len(sys.argv)>1 else None
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await pg.evaluate("document.getElementById('mpName').value='Tester'")
    await pg.evaluate("document.getElementById('bTrain').click()");await pg.wait_for_timeout(300)
    LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
    LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
    print('picker',await ev("JSON.stringify([...document.querySelectorAll('#trPick [data-trk]')].map(b=>b.dataset.trk+(b.disabled?'(soon)':'')))"))
    await pg.evaluate("document.querySelector('#trPick [data-trk=b3]').click()");await pg.wait_for_timeout(1500)
    print('start',await ev("JSON.stringify({by:S.training.by,docked:S.player.docked,cls:S.player.cls,steps:TRAIN[S.training.i].steps.length,rack:S.player.rack})"))
    step=lambda: ev("trCur()?S.training.j:99")
    async def wait_step(n,act,limit=40):
      for i in range(limit):
        await ev(act);await pg.wait_for_timeout(250)
        if await step()>n:return True
      return False
    ack="(()=>{S.training.ack=1;return 1})()"
    kill="(()=>{const d=trDroneEnts()[0];if(d)damageShip(d,99999,'player',{x:d.x,y:d.y,z:d.z,src:W.player},'laser');return 1})()"
    acts=["(()=>{undock();return 1})()",
      "(()=>{targetNearest('hostile');return 1})()",
      "(()=>{const d=trDroneEnts().find(x=>x!==S.training.v.t1);if(d)W.tgt={kind:'ship',ref:d};return 1})()",
      "(()=>{S.player.wpn='laser';return 1})()",kill,ack,
      "(()=>{const d=trDroneEnts()[0];if(d&&!W.missiles.some(m=>m.src===W.player))launchMissile(W.player,d,1,'missile');return 1})()",
      "(()=>{W.player.energy=W.player.st.eCap;playerFlares();return 1})()",
      "(()=>{for(const d of trDroneEnts())damageShip(d,99999,'player',{x:d.x,y:d.y,z:d.z,src:W.player},'laser');return 1})()",
      "(()=>{const c=S.sectors[W.sid].crates.find(x=>x.id===S.training.v.crate),p=W.player;if(c){p.x=c.x;p.y=c.y;p.z=c.z;p.vx=p.vy=p.vz=0}return 1})()",
      "(()=>{window._hp=W.player.hull;for(const e of bt3WingLive())damageShip(e,99999,'player',{x:e.x,y:e.y,z:e.z,src:W.player},'laser');return 1})()",
      "(()=>{pilotDistress();return 1})()",ack,ack]
    for n,a in enumerate(acts):
      ok=await wait_step(n,a,60)
      print(n+1,'ok' if ok else 'STUCK',await ev("(()=>{const c=trCur();return c?String(typeof c.s.x==='function'?c.s.x():c.s.x).replace(/<[^>]+>/g,'').slice(0,80):'done'})()"))
      if not ok:break
    print('end',await ev("JSON.stringify({done:S.training.done.length,cargo:S.player.cargo,drones:trDroneEnts().length,wing:bt3WingLive().length,distT:Math.round((S.player.distT||0)-S.T)})"),await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
