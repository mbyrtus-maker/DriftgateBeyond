# Driftgate Beyond: a player company's logo on its bases, as the game draws them (10 Nov 2026), for review. Two companies
# (different marks and colours, set on the profile and brand as a player would) on four of the six designs, Depot 3 and the
# bare Station: the whole base from flying distance, then each logo board close up (the camera along the board's normal).
# Usage: flock /tmp/dgbeyond-browser.lock python3 tools/previews/base_logos_game.py OUT.png
import asyncio,json,os,sys,tempfile
from playwright.async_api import async_playwright
from PIL import Image,ImageDraw,ImageFont
HERE=os.path.dirname(os.path.abspath(__file__))
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(HERE,'..','..','index.html')))
OUT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.join(HERE,'beyond_base_logos.png'))
CO=[(3,'#4f7cff','Cobalt, mark 3'),(7,'#f0b24a','Gold, mark 7')]
ROWS=[(1,'Company standard'),(2,'Wheel'),(5,'Disc'),(6,'Asteroid')]
KINDS=[('Depot 3',0),('Station',1)]
CW,CH,DS=300,240,2
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=await b.new_page(viewport={'width':CW,'height':CH},device_scale_factor=DS);errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=90000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(3500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await pg.add_style_tag(content='body *{visibility:hidden !important} #gl{visibility:visible !important}')
    await ev("""(()=>{const P=S.player;if(P.docked)undock();const sid=Object.keys(DEF).find(s=>depCan(s)&&DEF[s].kind!=='hive'&&DEF[s].kind!=='den');exitSector();W=null;P.sector=sid;enterSector(sid);
      const R=depMake(P,sid,{x:0,y:0,z:0},{},{});depEnt(R);window.__R=R;cam.mode='cockpit';window.__C={x:500,y:250,z:400,t:null};
      for(const e of W.ents)if(e!==W.player&&e.type==='ship'){e.alive=false}
      wkDescs=function(){return[]};
      updateCamera=function(){const E=W.stationEnt,C=__C,p=W.player;p.x=E.x+4000;p.y=E.y-3000;p.z=E.z+4000;p.vx=p.vy=p.vz=0;const T=C.t||{x:E.x,y:E.y,z:E.z};
        cam.x=T.x+C.x;cam.y=T.y+C.y;cam.z=T.z+C.z;const up=Math.abs(C.y)>.95*Math.hypot(C.x,C.y,C.z)?[1,0,0]:[0,1,0];qLook(-C.x,-C.y,-C.z,up[0],up[1],up[2],cam.q);cam.fov=34;E.shield=0;E.lastHit=-99};return 1})()""")
    tmp=tempfile.mkdtemp(prefix='blogos_');shots={};info={}
    for ci,(lg,col,_) in enumerate(CO):
      await ev(f"""(()=>{{const P=S.player;P.co=P.co||{{}};P.co.logo={lg};const N=brSlot(P,true);S.brands[N].col='{col}';return 1}})()""")
      for n,_ in ROWS:
        for ki,(kl,st) in enumerate(KINDS):
          r=json.loads(await ev(f"""(()=>{{const R=__R;R.design={n};R.pst={st};R.bld=[];const d=devOf(R);d.store={0 if st else 6};const SE=W.stationEnt;SE._mt=0;mdlStationTurrets(SE);
            const M=MDL.i[bmModel(R)],K=R.pst?BM.K.station:BM.K.depot,c=M.c||[0,0,0],h=M.h||1;return JSON.stringify({{model:bmModel(R),lg:(M.lg||[]).map(L=>({{p:L[0].map((v,i)=>(v*h+c[i])*K),n:L[1],s:L[2]*h*K}})),logo:bmLogoOf(R),col:coCol(R.pid||'me')}})}})()"""))
          info[(ci,n,ki)]=r;D=820 if st else 560
          await ev(f"(()=>{{__C.x={D*.62};__C.y={D*.42};__C.z={D*.66};__C.t=null;return 1}})()");await pg.wait_for_timeout(400)
          f=os.path.join(tmp,f'{ci}_{n}_{ki}_w.png');await pg.locator('#gl').screenshot(path=f);shots[(ci,n,ki,0)]=f
          for bi in range(2):
            if bi<len(r['lg']):
              L=r['lg'][bi];dd=L['s']*7.5
              await ev(f"""(()=>{{const E=W.stationEnt,p={json.dumps(L['p'])},n={json.dumps(L['n'])};qRot(E.q,p[0],p[1],p[2],_u);__C.t={{x:E.x+_u.x,y:E.y+_u.y,z:E.z+_u.z}};qRot(E.q,n[0],n[1],n[2],_u);
                const t=[_u.x,_u.y,_u.z],k={dd};__C.x=t[0]*k+(Math.abs(t[1])>.9?k*.15:0);__C.y=t[1]*k+k*.12;__C.z=t[2]*k;return 1}})()""");await pg.wait_for_timeout(400)
              f=os.path.join(tmp,f'{ci}_{n}_{ki}_{bi}.png');await pg.locator('#gl').screenshot(path=f);shots[(ci,n,ki,bi+1)]=f
      print('company',ci,flush=True)
    await b.close()
  S=DS;LW=150;HD=96;NC=len(CO)*len(KINDS)*3;W=(LW+CW*NC)*S;H=(HD+CH*len(ROWS)+24)*S
  fb=lambda s:ImageFont.truetype('DejaVuSans-Bold.ttf',s*S);fr=lambda s:ImageFont.truetype('DejaVuSans.ttf',s*S)
  sh=Image.new('RGB',(W,H),(9,12,18));g=ImageDraw.Draw(sh)
  g.text((14*S,10*S),'Driftgate Beyond · Player bases: the company logo on its Depots and Stations',font=fb(20),fill=(230,232,236))
  g.text((14*S,36*S),'Two companies (the profile\'s mark and the brand colour), each base whole from flying distance, then each logo board close up. As the game draws them.',font=fr(11),fill=(140,150,165))
  for ci,(lg,col,lab) in enumerate(CO):
    for ki,(kl,_) in enumerate(KINDS):
      x0=(LW+CW*3*(ci*2+ki))*S;g.text((x0+8*S,56*S),f'{lab} · {kl}',font=fb(13),fill=tuple(int(col[k:k+2],16) for k in (1,3,5)))
      for j,t in enumerate(('whole base','board 1','board 2')):g.text((x0+(CW*j+8)*S,76*S),t,font=fr(10),fill=(120,128,140))
  for i,(n,name) in enumerate(ROWS):
    y0=(HD+CH*i)*S;g.text((12*S,y0+12*S),f'{n}. {name}',font=fb(14),fill=(200,206,216))
    for ci in range(len(CO)):
      for ki in range(len(KINDS)):
        I=info[(ci,n,ki)];g.text((12*S,y0+(36+(ci*2+ki)*16)*S),f"{I['model']}: {len(I['lg'])} boards",font=fr(9),fill=(130,138,150))
        for j in range(3):
          f=shots.get((ci,n,ki,j))
          if f:sh.paste(Image.open(f).convert('RGB'),((LW+CW*(3*(ci*2+ki)+j))*S,y0))
    g.line([(0,y0),(W,y0)],fill=(30,36,48))
  for k in range(1,len(CO)*len(KINDS)):x=(LW+CW*3*k)*S;g.line([(x,(HD-44)*S),(x,H-24*S)],fill=(60,66,80),width=2*S)
  g.text((14*S,H-18*S),'Errors in the page: %s'%(errs[:2] if errs else 'none'),font=fr(10),fill=(110,118,130))
  sh.save(OUT);print('wrote',OUT,sh.size,'errors:',errs[:4])
asyncio.run(main())
