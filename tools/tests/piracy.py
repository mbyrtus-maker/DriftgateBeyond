# Beyond: pirate gear for contractors. Jammer and cargo hook parts sold at Scrapheart; jam mode fires jam rounds that jam an
# unshielded ship dark; the hook moves its hold into yours, tagged stolen (ledger exact); customs heat for gear aboard
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
    print('scrapheart stock',await ev("JSON.stringify({jammer:mkStock(S.stations.wr).pt_jammer||0,hook:mkStock(S.stations.wr).pt_hook||0,crafted:CRAFTABLE.includes('pt_jammer')})"))
    print('fit',await ev("""(()=>{const P=S.player,FC={storage:P.vault,storageName:'Vault'};devLedger(()=>{inv.add(P.vault,'pt_jammer',1);inv.add(P.vault,'pt_hook',1)});const a=fitDo(FC,P,'w:1:pt_jammer'),b2=fitDo(FC,P,'u:0:pt_hook');return JSON.stringify({a,b:b2,fit:fitOf(P).w.concat(fitOf(P).u)})})()"""))
    print('jam and hook',await ev("""(()=>{undock();const P=S.player,p=W.player;relInit();const e=makeNPC('hauler','varkesh','courier',1,{},null);e.dummy=true;qRot(p.q,0,0,1,_f);e.x=p.x+_f.x*120;e.y=p.y+_f.y*120;e.z=p.z+_f.z*120;e.vx=e.vy=e.vz=0;e.shield=0;W.ents.push(e);devLedger(()=>{e.cargo={ir:12,plate:4}});W.tgt={kind:'ship',ref:e};let shots=0;
      jamToggle();for(let i=0;i<400&&!jamDark(e);i++){p.cool=0;p.energy=p.st.eCap;p.boot=0;p.vx=p.vy=p.vz=0;e.vx=e.vy=e.vz=0;e.x=p.x+_f.x*120;e.y=p.y+_f.y*120;e.z=p.z+_f.z*120;faceInstant(p,e.x-p.x,e.y-p.y,e.z-p.z);const n0=W.shots.length;fire(p);shots+=W.shots.length-n0;shotsUpdate(.05);e.shield=0}const dark=jamDark(e);
      devLedger(()=>{P.cargo={}});keys.KeyE=true;for(let i=0;i<40;i++)pgHookTick(.25);keys.KeyE=false;return JSON.stringify({dark,shots,jam:Math.round(e.jam||0),cap:Math.round(jamCap(e)),alive:e.alive,hull:Math.round(e.hull),took:P.cargo,tags:P.stol,heat:Math.round(heatOf('varkesh')),stand:+standOf('varkesh').toFixed(1)})})()"""))
    print('ledger',await ev(LED))
    print('customs',await ev("""(()=>{const P=S.player;P.heat={};P.caught=null;devLedger(()=>{P.cargo={}});scanResolve(P,'halcyon','me');const a=Math.round(heatOf('halcyon'));scanResolve(P,'varkesh','me');return JSON.stringify({halcyon:a,varkesh:Math.round(heatOf('varkesh'))})})()"""))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
