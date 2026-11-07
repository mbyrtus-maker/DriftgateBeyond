# Beyond training, section 2 (Contracts and standing): the section starts a contractor at the freeport with a freeport
# request set up to the next freeport; every step completes from the game's own actions: the Allegiance tab (opened with the key its prompt names) and the Jobs tab,
# selecting and dropping a job, selecting the request, buying the goods, the trip, docking and delivering; paid by the
# Compact, standing up, ledger exact
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
    print('picker',await ev("JSON.stringify([...document.querySelectorAll('#trPick [data-trk]')].map(b=>b.dataset.trk+(b.disabled?'(soon)':'')))"))
    await pg.evaluate("document.querySelector('#trPick [data-trk=b2]').click()");await pg.wait_for_timeout(1500)
    print('start',await ev("JSON.stringify({by:S.training.by,docked:S.player.docked,sector:S.player.sector,steps:TRAIN[S.training.i].steps.length,k:bt2K()&&{item:bt2K().item,n:bt2K().n,to:bt2K().st,reward:bt2K().reward},dest:S.training.v.dest,hops:HOP[S.player.sector][S.training.v.dest],cr:S.player.credits})"))
    step=lambda: ev("trCur()?S.training.j:99")
    async def wait_step(n,act,limit=40):
      for i in range(limit):
        await ev(act);await pg.wait_for_timeout(250)
        if await step()>n:return True
      return False
    ack="(()=>{S.training.ack=1;return 1})()"
    acts=["(()=>{$('dock').hidden=false;dockTab='allegiance';renderDock();return 1})()",ack,ack,
      "(()=>{dockTab='jobs';renderDock();return 1})()",ack,
      "(()=>{renderDock();if(!JTRACK){const j=JOBS_LAST.find(x=>x.btn&&x.btn[0]==='jtrack');if(j)dockClick('jtrack',j.id)}else dockClick('jdrop','t:'+JTRACK.id);return 1})()",
      "(()=>{dockTab='jobs';renderDock();dockClick('jtrack','r:'+S.training.v.kid);return 1})()",
      "(()=>{dockClick('hbuy',String(S.training.v.kid));return 1})()",
      "(()=>{const P=S.player,d=S.training.v.dest;if(P.sector!==d){if(P.docked)undock();exitSector();P.sector=d;P.docked=null;enterSector(d)}return 1})()",
      "(()=>{const SE=W.stationEnt,p=W.player;apOn=false;p.x=SE.x+200;p.y=SE.y;p.z=SE.z;p.vx=p.vy=p.vz=0;p.boot=0;if(!W.docking&&!S.player.docked)actPress();return 1})()",
      "(()=>{if(S.player.docked){$('dock').hidden=false;dockTab='jobs';renderDock();window._c0=window._c0||S.player.credits;dockClick('deliver',String(S.training.v.kid))}return 1})()",
      ack,ack]
    # step 1 with the real key: the dock open on Overview, press the digit the prompt names, as a pilot would
    await ev("(()=>{$('dock').hidden=false;dockTab='home';renderDock();return 1})()")
    kk=await ev(r"(()=>{const m=String(trCur().s.x()).match(/<kbd>(\d)<\/kbd>/);return m?m[1]:''})()")
    await pg.evaluate("c=>{dispatchEvent(new KeyboardEvent('keydown',{code:c,bubbles:true}));dispatchEvent(new KeyboardEvent('keyup',{code:c,bubbles:true}))}",'Digit'+kk)
    await pg.wait_for_timeout(1000)
    tab=await ev("dockTab");print('allegiance key',kk,'opens',tab,'step',await ev("S.training.j"))
    if tab!='allegiance':print('STUCK the prompt names key',kk,'for Allegiance, which opens',tab)
    for n,a in enumerate(acts):
      ok=await wait_step(n,a,120 if n==9 else 40)
      print(n+1,'ok' if ok else 'STUCK',await ev("(()=>{const c=trCur();return c?String(typeof c.s.x==='function'?c.s.x():c.s.x).replace(/<[^>]+>/g,'').slice(0,90):'done'})()"),await ev("dockErr||''"))
      if not ok:break
    print('end',await ev("JSON.stringify({done:S.training.done.length,sector:S.player.sector,cr:S.player.credits,paid:S.player.credits-(window._c0||0),stand:+standOf('neutral').toFixed(2),job:!!JTRACK})"),await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
