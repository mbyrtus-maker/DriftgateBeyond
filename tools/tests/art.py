# Beyond, 5 Nov 2026: the rest of the approved art in the game. Every power's constructor draws as its approved model (the
# class name "constructor" used to find Object's own constructor and fall back to Driftgate 1's); every class the Unbound fly
# draws as one of their six designs; the shared assault ship flies from a capital to the base it assaults when that happens in
# an open system (survivors fly back, the shot-down ones blow up on the way in). No errors.
import asyncio,json,os
from playwright.async_api import async_playwright
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
FAILS=[]
def check(n,ok,info=''):
  print(('ok   ' if ok else 'FAIL ')+n+(' · '+str(info) if info!='' else ''),flush=True)
  if not ok:FAILS.append(n)
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1200,'height':760});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(4000)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    used=json.loads(await ev("""(()=>{let last=null;const o=mdlMesh;mdlMesh=function(n){last=n;return o.apply(this,arguments)};const out={};
      const one=(f,c)=>{for(const k in MESH)delete MESH[k];last=null;try{shipMesh(f,c)}catch(e){last='ERR '+e.message}return last};
      for(const f of FAC_IDS)out[f+':constructor']=one(f,'constructor');
      for(const c of ['raider','corsair','plunderer','uskiff','interceptor','striker','heavy','bomber','gunboat','scout','scout2','courier','freighter','bulker','skiff','prospector','dredger','constructor'])out['pirate:'+c]=one('pirate',c);
      mdlMesh=o;return JSON.stringify(out)})()"""))
    check('every power\'s constructor draws as its approved model',[used[f+':constructor'] for f in ('halcyon','varkesh','ostrova')]==['dz_architect','dz_foundry','dz_loom'],{k:v for k,v in used.items() if 'constructor' in k})
    six={'dz_raider','dz_skiff','dz_corsair','dz_plunderer','dz_wrecker'}
    bad={k:v for k,v in used.items() if k.startswith('pirate:') and v not in six}
    check('every Unbound class draws as one of their designs',not bad,bad)
    check('the Unbound bomber is their Wrecker',used['pirate:bomber']=='dz_wrecker')
    # the assault ship: three fly in from a capital's side, one is shot down on the way, two fly back
    r=json.loads(await ev("""(()=>{undock();const E=W.stationEnt,p=W.player;p.x=E.x+900;p.y=E.y+250;p.z=E.z+900;p.vx=p.vy=p.vz=0;faceInstant(p,E.x-p.x,E.y-p.y,E.z-p.z);
      const t={side:'varkesh',sector:W.sid};let calls=0;const o=drawMesh;window.__asd=0;
      asFly(t,W.sid,true);asFly(t,W.sid,false);asFly(t,W.sid,true);for(const s of W.asl){s.a={x:p.x+(E.x-p.x)*.25,y:p.y+60,z:p.z+(E.z-p.z)*.25};s.dur=5}
      return JSON.stringify({n:W.asl.length,die:W.asl.filter(s=>s.die).length,mdl:mdlHas('dz_assault')})})()"""))
    check('assault ships take off for the base',r['n']==3 and r['die']==1 and r['mdl'],r)
    # (game time, not page time: the page may run slow)
    t0=await ev("W.t")
    async def until(dt):
      for i in range(120):
        if await ev("W.t")>=t0+dt:return
        await pg.wait_for_timeout(250)
    await until(6.5);mid=await ev("(W.asl||[]).length")
    await until(17);end=await ev("(W.asl||[]).length")
    check('one is shot down on the way in, the others land and fly home',mid==2 and end==0,'%s in flight halfway, %s at the end'%(mid,end))
    # a capital's real assault in the open system sends them
    r=json.loads(await ev("""(()=>{W.asl=[];const R=W.stationEnt.rec,t={side:'halcyon',sector:W.sid,aload:2,load:{},name:'Test'};aSend(t,W.sid,0);aSend(t,W.sid,1);return JSON.stringify({n:W.asl.length,aload:t.aload})})()"""))
    check('a capital\'s landing (aSend) flies them in the open system',r['n']==2,r)
    check('no errors',not errs,errs[:4])
    await b.close()
  print('FAILED: '+', '.join(FAILS) if FAILS else 'ALL OK')
asyncio.run(main())
