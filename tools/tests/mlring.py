# Beyond, the mining laser's ring turns with its rock (9 Nov 2026: "the ring seems to go wherever it wishes"): the ring is a
# great circle in the rock's own frame (its tumble and squashed shape); aiming the nose at a point of the ring as drawn puts the
# beam on the ring, before and after the rock has turned, and the rock's pose runs on the galaxy clock (host and guests agree)
import asyncio,json
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[];bad=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    def check(name,ok,info=''):
      print(('ok   ' if ok else 'FAIL ')+name,info)
      if not ok:bad.append(name)
    r=json.loads(await ev("""(()=>{running=false;const P=S.player,p=W.player;P.docked=null;const a=S.sectors[W.sid].ast.filter(x=>ringOK(x)).sort((x,y)=>d3(x,p)-d3(y,p))[0];
      // a point of the ring as drawn (the same frame the HUD draws it in), the ship placed 250 m out from it, nose on it
      const aim=th=>{const F=mlFrame(a),n=F.n,ax=Math.abs(n.x)<.9?{x:1,y:0,z:0}:{x:0,y:1,z:0};let u={x:n.y*ax.z-n.z*ax.y,y:n.z*ax.x-n.x*ax.z,z:n.x*ax.y-n.y*ax.x};const ul=Math.hypot(u.x,u.y,u.z);u={x:u.x/ul,y:u.y/ul,z:u.z/ul};
        const v={x:n.y*u.z-n.z*u.y,y:n.z*u.x-n.x*u.z,z:n.x*u.y-n.y*u.x},w=mlFromS(F,(u.x*Math.cos(th)+v.x*Math.sin(th))*F.R,(u.y*Math.cos(th)+v.y*Math.sin(th))*F.R,(u.z*Math.cos(th)+v.z*Math.sin(th))*F.R);
        const P0={x:a.x+w.x,y:a.y+w.y,z:a.z+w.z},l=Math.hypot(w.x,w.y,w.z),out={x:w.x/l,y:w.y/l,z:w.z/l};p.x=P0.x+out.x*250;p.y=P0.y+out.y*250;p.z=P0.z+out.z*250;
        // nose toward the ring point
        const dx=P0.x-p.x,dy=P0.y-p.y,dz=P0.z-p.z,dl=Math.hypot(dx,dy,dz),fz={x:dx/dl,y:dy/dl,z:dz/dl},c=fz.z,ax2={x:-fz.y,y:fz.x,z:0},s2=Math.hypot(ax2.x,ax2.y);
        if(s2<1e-9){p.q=c>0?{x:0,y:0,z:0,w:1}:{x:0,y:1,z:0,w:0}}else{const ang=Math.acos(Math.max(-1,Math.min(1,c))),k=Math.sin(ang/2)/s2;p.q={x:ax2.x*k,y:ax2.y*k,z:0,w:Math.cos(ang/2)}}
        const B=mlBeam(p,a);return{on:!!(B&&B.on&&!B.assist),hit:B?Math.hypot(B.x-P0.x,B.y-P0.y,B.z-P0.z):-1,P0}};
      const r1=[0,1.3,2.6,4,5.2].map(aim);const old=r1[0].P0;S.T+=40;const r2=[0,1.3,2.6,4,5.2].map(aim);
      // the old spot after the rock has turned: no longer the ring
      const q0=astPose(a,0,{x:0,y:0,z:0,w:1});S.T+=0;const t1=JSON.stringify(q0),t2=JSON.stringify(astPose(a,123456,{x:0,y:0,z:0,w:1}));
      return JSON.stringify({before:r1.map(x=>x.on),after:r2.map(x=>x.on),hit:r1.concat(r2).map(x=>Math.round(x.hit)),moved:Math.round(Math.hypot(r2[0].P0.x-old.x,r2[0].P0.y-old.y,r2[0].P0.z-old.z)),clock:t1===t2})})()"""))
    check('aimed at the ring as drawn, the beam lands on it (all round the ring)',all(r['before']) and max(r['hit'])<=3,r)
    check('the rock turns and the ring turns with it: aimed at the ring as drawn now, still on it',all(r['after']) and r['moved']>0,r)
    check('the rock\'s pose follows the galaxy clock (the same for host and guests)',r['clock'],r)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
