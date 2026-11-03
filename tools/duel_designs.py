# design duels (Beyond stage 6): python3 tools/duel_designs.py PAGE N interceptor,striker,heavy [grade]; prints the first power's win share per pair
import asyncio,json,sys,os,time
from playwright.async_api import async_playwright
G='file://'+os.path.abspath(sys.argv[1]);N=int(sys.argv[2]);CLS=sys.argv[3].split(',');T=int(sys.argv[4]) if len(sys.argv)>4 else 1
SETUP=r"""(()=>{running=false;exitSector();relInit();for(const a of FAC_IDS)for(const b of FAC_IDS)if(a<b){S.rel[a][b]=S.rel[b][a]=-80;Object.assign(pairOf(a,b),{war:true,warT:S.T})}
 const sid=SECTOR_DEFS.map(d=>d.id).find(id=>!S.stations[id]&&!(S.outposts&&S.outposts[id]));
 const kit=(cls,t)=>{const C=CLASSES[cls],o={},r=rackCapC(cls,t);if(C.torp)o.torpedo=r;else if(r>0)o.missile=r;if(C.swarm)o.swarm=C.swarm;return o};
 const mk=(side,cls,t)=>{const e=makeNPC('patrol',side,cls,t,kit(cls,t),null);e.aimT=1;e.flares=1;e.hull=e.st.hull;e.shield=e.st.sCap;e.energy=e.st.eCap;e.wpn='kinetic';return e};
 window.DD=function(fa,fb,cls,t,maxT){W=openWorld(sid);W.player=null;W.ents=W.ents.filter(e=>!e.npc&&e.type!=='ship');W.popT=1e9;
  const A=mk(fa,cls,t),B=mk(fb,cls,t);A.x=-700;B.x=700;A.y=B.y=0;A.z=B.z=9000;W.ents.push(A,B);const dt=1/30;let tt=0;
  while(tt<maxT&&A.alive&&B.alive&&A.hull>0&&B.hull>0){W.popT=1e9;W.ents=W.ents.filter(e=>e===A||e===B||!e.npc||e.side===fa||e.side===fb);worldUpdate(dt);tt+=dt}
  const fr=e=>(e.alive&&e.hull>0)?(Math.max(0,e.hull)/e.st.hull+Math.max(0,e.shield)/Math.max(1,e.st.sCap))/2:0;const r=[fr(A),fr(B)];delete WORLDS[sid];return r};return sid})()"""
async def main():
  async with async_playwright() as p:
    br=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await br.new_page();errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto(G+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await ev(SETUP)
    for cls in CLS:
      for a,b in [('halcyon','varkesh'),('halcyon','ostrova'),('varkesh','ostrova')]:
        w=l=0;t0=time.time()
        for k in range(N):
          x,y=(a,b) if k%2==0 else (b,a)
          r=json.loads(await ev(f"JSON.stringify(DD('{x}','{y}','{cls}',{T},150))"))
          ra,rb=(r[0],r[1]) if x==a else (r[1],r[0])
          if ra>rb:w+=1
          elif rb>ra:l+=1
        print(cls,a,'vs',b,f'{w}-{l}',f'{w/max(1,w+l):.0%}',f'{time.time()-t0:.0f}s',flush=True)
    print('errors',errs[:3]);await br.close()
asyncio.run(main())
