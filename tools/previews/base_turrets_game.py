# Driftgate Beyond: a player company's bases with their live turrets, as the game draws them (10 Nov 2026), for review.
# Every design (1-6) at Depot 1, 2, 3 and as a Station with no buildings and with five, each from three angles (above, level,
# below), the live turrets drawn by draw3D where bmTurrets seats them. Rendered in the built game (index.html) in Chromium.
# Usage: flock /tmp/dgbeyond-browser.lock python3 tools/previews/base_turrets_game.py OUT.png [TITLE]
import asyncio,json,os,sys,tempfile,math
from playwright.async_api import async_playwright
from PIL import Image,ImageDraw,ImageFont
HERE=os.path.dirname(os.path.abspath(__file__))
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(HERE,'..','..','index.html')))
OUT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.join(HERE,'beyond_base_turrets.png'))
TITLE=sys.argv[2] if len(sys.argv)>2 else 'live turrets on every design'
DESIGNS=[(1,'Company standard'),(2,'Wheel'),(3,'Spire'),(4,'Truss cluster'),(5,'Disc'),(6,'Asteroid')]
CFG=[('Depot 1',"R.pst=0;R.bld=[];d.store=0;",300),('Depot 2',"R.pst=0;R.bld=[];d.store=3;",300),('Depot 3',"R.pst=0;R.bld=[];d.store=6;",300),
     ('Station, bare',"R.pst=1;R.bld=[];d.store=6;",540),('Station, 5 buildings',"R.pst=1;R.bld=['yard','storage','defence','hangar','market'];d.store=6;",600)]
ANG=[('above',.7,.55),('level',2.6,.06),('below',4.4,-.6)]
CW,CH=250,210;DS=2
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=await b.new_page(viewport={'width':CW,'height':CH},device_scale_factor=2);errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=90000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(3500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await pg.add_style_tag(content='body *{visibility:hidden !important} #gl{visibility:visible !important}')
    r=await ev("""(()=>{const P=S.player;if(P.docked)undock();const sid=Object.keys(DEF).find(s=>depCan(s)&&DEF[s].kind!=='hive'&&DEF[s].kind!=='den');exitSector();W=null;P.sector=sid;enterSector(sid);
      const R=depMake(P,sid,{x:0,y:0,z:0},{},{});depEnt(R);window.__R=R;const SE=W.stationEnt;cam.mode='cockpit';window.__C={a:0,e:0,d:400};
      for(const e of W.ents)if(e!==W.player&&e.type==='ship'){e.alive=false}
      wkDescs=function(){return[]};
      updateCamera=function(){const E=W.stationEnt,C=__C,p=W.player;p.x=E.x+3000;p.y=E.y-2000;p.z=E.z+3000;p.vx=p.vy=p.vz=0;
        const x=Math.cos(C.a)*Math.cos(C.e)*C.d,y=Math.sin(C.e)*C.d,z=Math.sin(C.a)*Math.cos(C.e)*C.d;cam.x=E.x+x;cam.y=E.y+y;cam.z=E.z+z;qLook(-x,-y,-z,0,1,0,cam.q);cam.fov=34;
        E.shield=0;E.lastHit=-99;for(const t of E.turrets){t.aim={x:x,y:y,z:z};const l=Math.hypot(x,y,z);t.aim.x/=l;t.aim.y/=l;t.aim.z/=l}};
      return JSON.stringify({sid,ok:!!SE})})()""")
    print(r,flush=True)
    tmp=tempfile.mkdtemp(prefix='bturrets_');shots={};info={}
    for n,_ in DESIGNS:
      for j,(lab,js,dist) in enumerate(CFG):
        info[(n,j)]=json.loads(await ev(f"""(()=>{{const R=__R;R.design={n};const d=devOf(R);d.prod=0;d.def=0;d.armor=0;d.hangar=0;d.life=0;{js}const SE=W.stationEnt;SE._mt=0;SE._subL=null;mdlStationTurrets(SE);
          return JSON.stringify({{model:bmModel(R),n:SE.turrets.length,p:SE.turrets.map(t=>t.p.map(Math.round))}})}})()"""))
        for k,(an,a,e) in enumerate(ANG):
          await ev(f"(()=>{{__C.a={a};__C.e={e};__C.d={dist};return 1}})()");await pg.wait_for_timeout(350)
          f=os.path.join(tmp,f'{n}_{j}_{k}.png');await pg.locator('#gl').screenshot(path=f);shots[(n,j,k)]=f
      print('design',n,flush=True)
    await b.close()
  S=DS;LW=170;HD=70;W=(LW+CW*len(CFG)*len(ANG))*S;H=(HD+CH*len(DESIGNS)+30)*S
  fb=lambda s:ImageFont.truetype('DejaVuSans-Bold.ttf',s*S);fr=lambda s:ImageFont.truetype('DejaVuSans.ttf',s*S)
  sh=Image.new('RGB',(W,H),(9,12,18));g=ImageDraw.Draw(sh)
  g.text((14*S,10*S),'Driftgate Beyond · Player bases: '+TITLE,font=fb(20),fill=(230,232,236))
  for j,(lab,_,dist) in enumerate(CFG):
    x0=(LW+CW*len(ANG)*j)*S;g.text((x0+8*S,40*S),f'{lab}  (camera {dist} m)',font=fb(13),fill=(190,198,210))
    for k,(an,_,_) in enumerate(ANG):g.text((x0+(CW*k+8)*S,56*S),an,font=fr(10),fill=(120,128,140))
  for i,(n,name) in enumerate(DESIGNS):
    y0=(HD+CH*i)*S;g.text((12*S,y0+12*S),f'{n}. {name}',font=fb(14),fill=(200,206,216))
    for j in range(len(CFG)):
      I=info[(n,j)];g.text((12*S,y0+(34+j*30)*S),f'{CFG[j][0]}: {I["model"]}',font=fr(9),fill=(120,128,140));g.text((12*S,y0+(46+j*30)*S),f'  {I["n"]} live turrets',font=fr(9),fill=(120,128,140))
      for k in range(len(ANG)):sh.paste(Image.open(shots[(n,j,k)]).convert('RGB'),((LW+CW*(len(ANG)*j+k))*S,y0))
    g.line([(0,y0),(W,y0)],fill=(30,36,48))
  for j in range(1,len(CFG)):x=(LW+CW*len(ANG)*j)*S;g.line([(x,(HD-20)*S),(x,H-30*S)],fill=(60,66,80),width=2*S)
  g.text((14*S,H-22*S),'Errors in the page: %s'%(errs[:2] if errs else 'none'),font=fr(11),fill=(110,118,130))
  sh.save(OUT);print('wrote',OUT,sh.size,'errors:',errs[:4])
asyncio.run(main())
