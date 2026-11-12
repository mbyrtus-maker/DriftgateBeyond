# Driftgate Beyond: the Compact's ships (12 Nov 2026), for review. The user, 11 Nov 2026: "Sand colored same as the powers":
# freeport security and traffic, independent pilots and anything else on the neutral side fly the three powers' hull designs
# in the Compact's sand colour (src/js/16zzzzf_gfx.js). One of each class in each power's design, drawn in the built game
# through the same shipMesh call the game makes for a Compact ship ('cz:<line>:neutral'), engines lit.
# Usage: flock /tmp/dgbeyond-browser.lock python3 tools/previews/compact_sheet.py OUT.png
import asyncio,json,os,sys,tempfile,math
from playwright.async_api import async_playwright
from PIL import Image,ImageDraw,ImageFont
HERE=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,HERE)
from audit_game import JS_SETUP,GAME
OUT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.join(HERE,'beyond_compact.png'))
CLS=['interceptor','striker','heavy','scout','scout2','bomber','gunboat','skiff','prospector','dredger','courier','freighter','bulker','constructor','drone']
LINES=['halcyon','varkesh','ostrova'];CW,CH=330,230
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=await b.new_page(viewport={'width':CW,'height':CH},device_scale_factor=2);errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=120000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(3500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await pg.add_style_tag(content='body *{visibility:hidden !important} #gl{visibility:visible !important}')
    await ev(JS_SETUP)
    names=json.loads(await ev("JSON.stringify(Object.fromEntries(%s.map(c=>[c,[CLASSES[c]?CLASSES[c].name:c,%s.map(l=>czModel(l,c))]])))"%(json.dumps(CLS),json.dumps(LINES))))
    kit=json.loads(await ev("JSON.stringify(%s.filter(c=>{const m=shipMesh('neutral',c);return !(m&&m.hull&&m.hull.mdl&&m.hull.mdl.startsWith('dz_'))}))"%json.dumps(CLS)))
    tmp=tempfile.mkdtemp(prefix='compact_');shots={}
    for c in CLS:
      for j,l in enumerate(LINES):
        await ev(f"(()=>{{const A=__A,m=shipMesh('cz:{l}:neutral','{c}');A.items=[{{m:m.hull,p:[0,0,0],s:1}}];A.eng=m.eng.map(e=>e.slice());A.shots=[];A.beams=[];A.turs=[];A.spr=[];A.gt=null;A.bub=null;A.col=hexRGB(sideCol('neutral'));A.fl=.9;A.thr=1;const C=A.cam;C.yaw=.62+Math.PI*0;C.pit=.28;C.top=0;C.d=4.3;C.fov=26;return 1}})()")
        await pg.wait_for_timeout(140);f=os.path.join(tmp,f'{c}_{j}.png');await pg.locator('#gl').screenshot(path=f);shots[(c,j)]=f
      print(c,flush=True)
    await b.close()
  fb=lambda s:ImageFont.truetype('DejaVuSans-Bold.ttf',s);fr=lambda s:ImageFont.truetype('DejaVuSans.ttf',s)
  LW=170;W=LW+CW*len(LINES);H=64+CH*len(CLS)+24;sh=Image.new('RGB',(W,H),(9,12,18));g=ImageDraw.Draw(sh)
  g.text((10,8),"Driftgate Beyond · the Compact's ships: the powers' designs in sand",font=fb(17),fill=(230,232,236))
  g.text((10,32),'Freeport security and traffic, independent pilots, anything neutral · the design is the one its home freeport\'s yard sells',font=fr(11),fill=(140,150,165))
  for j,l in enumerate(LINES):g.text((LW+CW*j+8,48),l.capitalize()+' design',font=fb(12),fill=(232,200,120))
  for r,c in enumerate(CLS):
    y0=64+CH*r;g.text((8,y0+10),names[c][0],font=fb(13),fill=(220,224,232));g.text((8,y0+30),c,font=fr(11),fill=(130,138,150))
    for j in range(len(LINES)):
      sh.paste(Image.open(shots[(c,j)]).convert('RGB').resize((CW,CH),Image.LANCZOS),(LW+CW*j,y0));g.text((LW+CW*j+8,y0+CH-18),str(names[c][1][j]),font=fr(10),fill=(120,128,140))
    g.line([(0,y0),(W,y0)],fill=(30,36,48))
  g.text((10,H-18),'Classes that still draw a model outside the powers\' designs on the neutral side: %s · page errors: %s'%(kit or 'none',errs[:2] or 'none'),font=fr(11),fill=(120,128,140))
  sh.save(OUT);print('wrote',OUT,sh.size,'kit left:',kit,'errors:',errs[:3])
asyncio.run(main())
