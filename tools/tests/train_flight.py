# Beyond training, section 1 (Flight and your first job): the picker lists the sections; the section starts a contractor at
# the freeport with Beyond's ship systems on; every step completes from the real controls and game state, through docking,
# selecting a job and a jump; no simulation errors
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
    print('picker',await ev("JSON.stringify([...document.querySelectorAll('#trPick [data-trk]')].map(b=>b.dataset.trk+(b.disabled?'(soon)':'')))"))
    await pg.evaluate("document.querySelector('#trPick [data-trk=b1]').click()");await pg.wait_for_timeout(1500)
    print('start',await ev("JSON.stringify({by:S.training.by,sworn:S.player.sworn,docked:S.player.docked,sector:S.player.sector,loadOn:loadOn(),fit:fitOf(S.player).u,steps:TRAIN[S.training.i].steps.length})"))
    step=lambda: ev("trCur()?S.training.j:99")
    async def wait_step(n,act,limit=40):
      for i in range(limit):
        await ev(act);await pg.wait_for_timeout(250)
        if await step()>n:return True
      return False
    # each step: do what it asks (directly through the game's own state and controls), then check it advanced
    acts=["(()=>{undock();return 1})()",
      "(()=>{const p=W.player;qRot(p.q,0,0,1,_f);p.vx=_f.x*170;p.vy=_f.y*170;p.vz=_f.z*170;return 1})()",
      "(()=>{const p=W.player;p.vx=p.vy=p.vz=0;return 1})()",
      "(()=>{keys[KEY_DEF.rollL]=true;return 1})()",
      "(()=>{keys[KEY_DEF.rollL]=false;keys.ShiftLeft=true;const p=W.player;qRot(p.q,0,0,1,_f);p.vx=_f.x*230;p.vy=_f.y*230;p.vz=_f.z*230;return 1})()",
      "(()=>{keys.ShiftLeft=false;S.player.fa=false;return 1})()",
      "(()=>{S.player.fa=true;return 1})()",
      "(()=>{S.player.level=false;return 1})()",
      "(()=>{S.player.level=true;return 1})()",
      "(()=>{cam.mode='cockpit';return 1})()",
      "(()=>{cam.mode='chase';return 1})()",
      "(()=>{targetNearest('ast');return 1})()",
      "(()=>{const p=W.player,a=W.tgt.ref;p.vx=p.vy=p.vz=0;const d=d3(p,a)||1,R=astR(a)+p.st.radius+10;p.x=a.x+(p.x-a.x)/d*R;p.y=a.y+(p.y-a.y)/d*R;p.z=a.z+(p.z-a.z)/d*R;actPress();return 1})()",
      "(()=>{actPress();return 1})()",
      "(()=>{const SE=W.stationEnt;W.tgt={kind:'station',ref:SE};apOn=true;return 1})()",
      "(()=>{const SE=W.stationEnt,p=W.player;apOn=false;p.x=SE.x+200;p.y=SE.y;p.z=SE.z;p.vx=p.vy=p.vz=0;p.boot=0;if(!W.docking)actPress();return 1})()",
      "(()=>{if(S.player.docked){$('dock').hidden=false;dockTab='jobs';renderDock()}return 1})()",
      "(()=>{renderDock();const j=JOBS_LAST.find(x=>x.btn&&x.btn[0]==='jtrack');if(j)dockClick('jtrack',j.id);return 1})()",
      "(()=>{S.training.ack=1;return 1})()",
      "(()=>{const P=S.player;if(P.docked)undock();const g=GATES[W.sid].find(x=>x.to===P.route)||GATES[W.sid][0];const p=W.player;if(!S.training.v.placed&&!S.player.docked){S.training.v.placed=1;const dx=p.x-g.x,dz=p.z-g.z,l=Math.hypot(dx,dz)||1;p.x=g.x+dx/l*500;p.y=g.y;p.z=g.z+dz/l*500;p.vx=p.vy=p.vz=0;faceInstant(p,g.x-p.x,g.y-p.y,g.z-p.z)}if(!W.jump&&!S.player.docked)apOn=true;return 1})()",
      "(()=>{S.training.ack=1;return 1})()"]
    for n,a in enumerate(acts):
      ok=await wait_step(n,a,400 if n==19 else 120 if n==15 else 40)
      print(n+1,'ok' if ok else 'STUCK',await ev("(()=>{const c=trCur();return c?String(typeof c.s.x==='function'?c.s.x():c.s.x).replace(/<[^>]+>/g,'').slice(0,70):'done'})()"))
      if not ok:break
    if SHOT:await pg.screenshot(path=SHOT)
    print('end',await ev("JSON.stringify({done:S.training.done.length,sector:S.player.sector,home:S.training.v.home,j:S.training.j,jump:!!W.jump,docked:S.player.docked,wsid:W.sid,running})"))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
