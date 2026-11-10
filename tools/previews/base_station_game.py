# Driftgate Beyond: each base design's Depot 3 beside its bare Station and its Station with five buildings, as the game draws
# them and at the same in-game scale (one camera distance for every cell), for review (10 Nov 2026).
# Usage: flock /tmp/dgbeyond-browser.lock python3 tools/previews/base_station_game.py OUT.png [TITLE]
import asyncio,json,os,sys,tempfile
from playwright.async_api import async_playwright
from PIL import Image,ImageDraw,ImageFont
HERE=os.path.dirname(os.path.abspath(__file__))
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(HERE,'..','..','index.html')))
OUT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.join(HERE,'beyond_base_stations.png'))
TITLE=sys.argv[2] if len(sys.argv)>2 else 'each level with its development modules, at one scale'
DESIGNS=[(1,'Company standard'),(2,'Wheel'),(3,'Spire'),(4,'Truss cluster'),(5,'Disc'),(6,'Asteroid')]
# development modules: Depot 1 a storage vault and a defence platform; Depot 2 adds production and a hangar; Depot 3 and the
# Stations every kind (habitat 2, storage 2, production, defence, shield works, hangar: six used)
D1="d.life=0;d.store=1;d.def=1;";D2="d.life=1;d.store=1;d.prod=1;d.hangar=1;";D3="d.life=2;d.store=2;d.prod=1;d.def=1;d.armor=1;d.hangar=1;"
CFG=[('Depot 1',"R.pst=0;R.bld=[];"+D1),('Depot 2',"R.pst=0;R.bld=[];"+D2),('Depot 3',"R.pst=0;R.bld=[];"+D3),('Station, no buildings',"R.pst=1;R.bld=[];"+D3),
     ('Station, five buildings',"R.pst=1;R.bld=['yard','storage','defence','hangar','market'];S.yards[yardKeyOf(R)]={sector:R.sid,fort:{},pst:R.sid};"+D3)]
ANG=[('three-quarter',.75,.42),('side',2.2,.08)]
DIST=float(os.environ.get('DIST','1100'))
CW,CH,DS=300,260,2
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
      const R=depMake(P,sid,{x:0,y:0,z:0},{},{});depEnt(R);window.__R=R;cam.mode='cockpit';window.__C={a:0,e:0,d:400};
      for(const e of W.ents)if(e!==W.player&&e.type==='ship'){e.alive=false}
      updateCamera=function(){const E=W.stationEnt,C=__C,p=W.player;p.x=E.x+4000;p.y=E.y-3000;p.z=E.z+4000;p.vx=p.vy=p.vz=0;
        const x=Math.cos(C.a)*Math.cos(C.e)*C.d,y=Math.sin(C.e)*C.d,z=Math.sin(C.a)*Math.cos(C.e)*C.d;cam.x=E.x+x;cam.y=E.y+y;cam.z=E.z+z;qLook(-x,-y,-z,0,1,0,cam.q);cam.fov=34;
        E.shield=0;E.lastHit=-99;const l=Math.hypot(x,y,z);for(const t of E.turrets)t.aim={x:x/l,y:y/l,z:z/l}};return 1})()""")
    tmp=tempfile.mkdtemp(prefix='bstation_');shots={};info={}
    for n,_ in DESIGNS:
      for j,(lab,js) in enumerate(CFG):
        info[(n,j)]=json.loads(await ev(f"""(()=>{{const R=__R;R.design={n};const d=devOf(R);d.store=0;d.prod=0;d.def=0;d.armor=0;d.hangar=0;d.life=0;for(const k in S.yards||{{}})if(S.yards[k].pst===R.sid)delete S.yards[k];{js}const SE=W.stationEnt;SE._mt=0;SE._subL=null;mdlStationTurrets(SE);
          const M=MDL.i[bmModel(R)],K=R.pst?BM.K.station:BM.K.depot;return JSON.stringify({{model:bmModel(R),r:Math.round((M.h||1)*K),lv:depLvl(R),wk:wkDescs(R.sid).map(w=>w.k+w.lvl).join(' ')}})}})()"""))
        for k,(an,a,e) in enumerate(ANG):
          await ev(f"(()=>{{__C.a={a};__C.e={e};__C.d={DIST};return 1}})()");await pg.wait_for_timeout(350)
          f=os.path.join(tmp,f'{n}_{j}_{k}.png');await pg.locator('#gl').screenshot(path=f);shots[(n,j,k)]=f
      print('design',n,flush=True)
    await b.close()
  S=DS;LW=175;HD=74;NC=len(CFG)*len(ANG);W=(LW+CW*NC)*S;H=(HD+CH*len(DESIGNS)+26)*S
  fb=lambda s:ImageFont.truetype('DejaVuSans-Bold.ttf',s*S);fr=lambda s:ImageFont.truetype('DejaVuSans.ttf',s*S)
  sh=Image.new('RGB',(W,H),(9,12,18));g=ImageDraw.Draw(sh)
  g.text((14*S,10*S),'Driftgate Beyond · Player bases: '+TITLE,font=fb(20),fill=(230,232,236))
  g.text((14*S,36*S),f'As the game draws them, every cell from {DIST:.0f} m (the same in-game scale); live turrets on their plinths',font=fr(11),fill=(140,150,165))
  for j,(lab,_) in enumerate(CFG):
    x0=(LW+CW*len(ANG)*j)*S;g.text((x0+8*S,52*S),lab,font=fb(13),fill=(190,198,210))
  for i,(n,name) in enumerate(DESIGNS):
    y0=(HD+CH*i)*S;g.text((12*S,y0+12*S),f'{n}. {name}',font=fb(14),fill=(200,206,216))
    for j in range(len(CFG)):
      I=info[(n,j)];g.text((12*S,y0+(34+j*42)*S),I['model'],font=fr(9),fill=(130,138,150));g.text((12*S,y0+(45+j*42)*S),f'  half-size {I["r"]} m',font=fr(9),fill=(130,138,150));g.text((12*S,y0+(56+j*42)*S),'  '+I['wk'],font=fr(8),fill=(110,118,130))
      for k in range(len(ANG)):sh.paste(Image.open(shots[(n,j,k)]).convert('RGB'),((LW+CW*(len(ANG)*j+k))*S,y0))
    g.line([(0,y0),(W,y0)],fill=(30,36,48))
  for j in range(1,len(CFG)):x=(LW+CW*len(ANG)*j)*S;g.line([(x,(HD-24)*S),(x,H-26*S)],fill=(60,66,80),width=2*S)
  g.text((14*S,H-20*S),'Errors in the page: %s'%(errs[:2] if errs else 'none'),font=fr(10),fill=(110,118,130))
  sh.save(OUT);print('wrote',OUT,sh.size,'errors:',errs[:4])
asyncio.run(main())
