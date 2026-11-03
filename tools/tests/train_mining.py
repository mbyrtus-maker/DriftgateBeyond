# Beyond training, section 4 (Mining): a Medium Miner; every step completes from the game's own actions and controls:
# targeting a rock, the mining laser on its ring (F held), switching to charges, a charge fired, detonated and its chunks
# scooped, docking, own ore delivered to a request, the rest sold; ledger exact
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
    LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
    await pg.evaluate("document.querySelector('#trPick [data-trk=b4]').click()");await pg.wait_for_timeout(1500)
    print('start',await ev("JSON.stringify({cls:S.player.cls,tools:mtools(S.player),mtool:S.player.mtool,blN:S.player.blN,steps:TRAIN[S.training.i].steps.length})"))
    step=lambda: ev("trCur()?S.training.j:99")
    async def wait_step(n,act,limit=40):
      for i in range(limit):
        await ev(act);await pg.wait_for_timeout(250)
        if await step()>n:return True
      return False
    ack="(()=>{S.training.ack=1;return 1})()"
    # pick a big rock well away from the station and gates, and keep it
    pickrock="""(()=>{const s=S.sectors[W.sid],SE=W.stationEnt;let a=s.ast.find(x=>x.id===window._rk);if(!a||oreTotal(a)<20||!ringOK(a)){a=s.ast.filter(x=>!x.comet&&!x.rift&&ringOK(x)&&oreTotal(x)>=40&&(!SE||d3(x,SE)>1500)&&GATES[W.sid].every(g=>d3(x,g)>1500)).sort((x,y)=>oreTotal(y)-oreTotal(x))[0];window._rk=a&&a.id}return a})()"""
    laser="""(()=>{const a=%s;const p=W.player,n=ringN(a);let d={x:-n.z,y:0,z:n.x};if(Math.hypot(d.x,d.z)<.1)d={x:1,y:0,z:0};const l=Math.hypot(d.x,d.y,d.z);d.x/=l;d.y/=l;d.z/=l;const R=astR(a)+60;
      p.x=a.x+d.x*R;p.y=a.y+d.y*R;p.z=a.z+d.z*R;p.vx=p.vy=p.vz=0;faceInstant(p,-d.x,-d.y,-d.z);W.tgt={kind:'ast',ref:a};keys.KeyF=true;p.energy=p.st.eCap;return 1})()"""%pickrock
    fire="""(()=>{keys.KeyF=false;const a=%s,p=W.player,P=S.player;if(bt4Charges())return 1;const pts=blPts(a),q=pts[0];const dx=q.x-a.x,dy=q.y-a.y,dz=q.z-a.z,l=Math.hypot(dx,dy,dz);p.x=a.x+dx/l*(l+150);p.y=a.y+dy/l*(l+150);p.z=a.z+dz/l*(l+150);p.vx=p.vy=p.vz=0;faceInstant(p,-dx,-dy,-dz);W.tgt={kind:'ast',ref:a};p.blCd=0;blFire(p,P);return 1})()"""%pickrock
    det="""(()=>{const a=%s,p=W.player;const dx=p.x-a.x,dy=p.y-a.y,dz=p.z-a.z,l=Math.hypot(dx,dy,dz)||1,R=astR(a)+260;p.x=a.x+dx/l*R;p.y=a.y+dy/l*R;p.z=a.z+dz/l*R;blDetonate(S.player,p);return 1})()"""%pickrock
    scoop="""(()=>{const s=S.sectors[W.sid],p=W.player,c=(s.clouds||[]).filter(x=>oreTotal(x)>0).sort((x,y)=>d3(x,p)-d3(y,p))[0];if(c){p.x=c.x;p.y=c.y;p.z=c.z;p.vx=c.vx||0;p.vy=c.vy||0;p.vz=c.vz||0;keys.KeyF=true}return 1})()"""
    acts=["(()=>{undock();return 1})()","(()=>{targetNearest('ast');return 1})()",ack,laser,
      "(()=>{keys.KeyF=false;S.player.mtool='charge';return 1})()",fire,det,scoop,
      "(()=>{keys.KeyF=false;return 1})()".replace("return 1","S.training.ack=1;return 1"),
      "(()=>{if(W.docking||S.player.docked)return 1;const SE=W.stationEnt,p=W.player;apOn=false;p.x=SE.x+200;p.y=SE.y;p.z=SE.z;p.vx=p.vy=p.vz=0;p.boot=0;actPress();return 1})()",
      "(()=>{if(S.player.docked){$('dock').hidden=false;dockTab='jobs';renderDock();dockClick('deliver',String(S.training.v.kid))}return 1})()",
      "(()=>{const k=bt4Ore();if(k){dockAction('sell',k+':all');renderDock()}return 1})()",ack]
    for n,a in enumerate(acts):
      ok=await wait_step(n,a,120 if n in(3,7,9) else 40)
      print(n+1,'ok' if ok else 'STUCK',await ev("(()=>{const c=trCur();return c?String(typeof c.s.x==='function'?c.s.x():c.s.x).replace(/<[^>]+>/g,'').slice(0,80):'done'})()"),await ev("JSON.stringify({ore:trOre(),ch:bt4Charges(),err:dockErr||''})"))
      if not ok:break
    print('end',await ev("JSON.stringify({done:S.training.done.length,cargo:S.player.cargo,cr:S.player.credits})"),await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
