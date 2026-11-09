# Driftgate Beyond: the makers' R&D stations as the game draws them (9 Nov 2026), for review. One maker per home style
# (Teal & Corvane, Marchgun, Spirewright, Coldwater Prospecting), with no labs, two and four at mixed grades, and four labs
# offline (its control centre knocked out: the lights dim); and, for scale, a station beside its power's depot and a fighter.
# Rendered in the built game (index.html) through rdsMesh and the 'rds' entity draw hook, in Chromium at deviceScaleFactor 2.
# Usage: flock /tmp/dgbeyond-browser.lock python3 tools/previews/rds_game_sheet.py OUT.png
import asyncio,json,os,sys,tempfile
from playwright.async_api import async_playwright
from PIL import Image,ImageDraw,ImageFont
HERE=os.path.dirname(os.path.abspath(__file__))
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(HERE,'..','..','index.html')))
OUT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.join(HERE,'beyond_rds_game.png'))
ROWS=[('tcy','Halcyon','Teal & Corvane Yards'),('mg','Varkesh','Marchgun Ordnance'),('sw','Ostrova','Spirewright'),('cp','Freeports','Coldwater Prospecting')]
COLS=[('No labs','a new maker: four empty sockets',[0,0,0,0],False),('Two labs','grades 2 and 4',[2,4,0,0],False),
      ('Four labs','grades 5, 3, 4 and 2',[5,3,4,2],False),('Four labs, offline','control centre knocked out: lights dim',[5,3,4,2],True)]
CW,CH=380,320   # one cell in CSS pixels (x2 in the picture)
DIST=175        # the camera's distance in metres (the same for every cell, so sizes compare)
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=await b.new_page(viewport={'width':CW,'height':CH},device_scale_factor=2);errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=90000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(4000)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    # only the flight view: the HUD and its overlay canvas hidden
    await pg.add_style_tag(content='body *{visibility:hidden !important} #gl{visibility:visible !important}')
    # a quiet spot far out from the station; the camera held on the station, the player hidden (cockpit view)
    r=await ev("""(()=>{if(S.player.docked)undock();const p=W.player,s=SCN.sun;window.__P={x:p.x+7000,y:p.y+2600,z:p.z+7000};
      const E={type:'rds',x:__P.x,y:__P.y,z:__P.z,q:q0(),m:'tcy',labs:[0,0,0,0],offline:false};W.ents.push(E);window.__E=E;
      let a=Math.atan2(s.x,s.z)+.5;const el=.38,d=%d;window.__C={x:Math.sin(a)*Math.cos(el)*d,y:Math.sin(el)*d,z:Math.cos(a)*Math.cos(el)*d};
      qAxis(0,1,0,a-.6,E.q);cam.mode='cockpit';
      updateCamera=function(){const E=window.__T||__E,C=__C,p=W.player;p.x=__P.x;p.y=__P.y-400;p.z=__P.z-900;p.vx=p.vy=p.vz=0;if(p.hull!==undefined&&p.st)p.hull=Math.max(p.hull,1);cam.x=E.x+C.x;cam.y=E.y+C.y;cam.z=E.z+C.z;qLook(-C.x,-C.y,-C.z,0,1,0,cam.q);cam.fov=30};
      return JSON.stringify({sun:[s.x,s.y,s.z],pts:rdsPoints('tcy')})})()"""%DIST)
    print(r,flush=True)
    tmp=tempfile.mkdtemp(prefix='rds_sheet_');shots={}
    for m,_,_ in ROWS:
      for j,(_,_,labs,off) in enumerate(COLS):
        await ev(f"(()=>{{__E.m='{m}';__E.labs={json.dumps(labs)};__E.offline={'true' if off else 'false'};return 1}})()")
        await pg.wait_for_timeout(700);f=os.path.join(tmp,f'{m}_{j}.png');await pg.locator('#gl').screenshot(path=f);shots[(m,j)]=f
    # for scale: a Halcyon station with four labs beside a Halcyon depot (105 m half-size) and an interceptor
    await pg.set_viewport_size({'width':CW*2,'height':CH})
    await ev("""(()=>{__E.m='tcy';__E.labs=[5,3,4,2];__E.offline=false;const C=__C,l=Math.hypot(C.x,C.z);window.__C={x:C.x/l*Math.hypot(C.x,C.y,C.z)*1.9,y:C.y*1.9,z:C.z/l*Math.hypot(C.x,C.y,C.z)*1.9};
      const sx=-C.z/l,sz=C.x/l;window.__D={x:__E.x+sx*190,y:__E.y,z:__E.z+sz*190};window.__F={x:__E.x-sx*95,y:__E.y-10,z:__E.z-sz*95};
      const o=drawWorks;drawWorks=function(t){const r=o.apply(this,arguments);const m=stMesh('by_dp_halcyon','halcyon',105);mModel(MM,__D.x,__D.y,__D.z,__E.q,1,1,1);drawMesh(m.core,MM);
        const f=shipMesh('halcyon','interceptor'),k=CLASSES.interceptor.radius*1.25;mModel(MM,__F.x,__F.y,__F.z,__E.q,k,k,k);drawMesh(f.hull,MM);if(f.rim)drawMesh(f.rim,MM);return r};
      window.__T={x:__E.x+sx*55,y:__E.y,z:__E.z+sz*55};return 1})()""")
    await pg.wait_for_timeout(900);fscale=os.path.join(tmp,'scale.png');await pg.locator('#gl').screenshot(path=fscale)
    info=json.loads(await ev("JSON.stringify(Object.fromEntries(['tcy','mg','sw','cp'].map(m=>[m,{style:RDS_STYLE(m),r:Math.round(rdsPoints(m).r)}])))"))
    await b.close()
  # the sheet
  S=2;LW=200;HD=96;W=LW*S+CW*S*len(COLS);H=HD*S+CH*S*len(ROWS)+CH*S+60*S
  fb=lambda s:ImageFont.truetype('DejaVuSans-Bold.ttf',s*S);fr=lambda s:ImageFont.truetype('DejaVuSans.ttf',s*S)
  sh=Image.new('RGB',(W,H),(9,12,18));g=ImageDraw.Draw(sh)
  g.text((20*S,16*S),"Driftgate Beyond · The makers' R&D stations in the game",font=fb(22),fill=(230,232,236))
  g.text((20*S,46*S),"As the game draws them (rdsMesh; model pack rds_*, rdl_*_g2-5, rdp_*) · the maker's accent and mark · no shields · each cell the same camera distance (%d m)"%DIST,font=fr(12),fill=(140,150,165))
  for j,(t,sub,_,_) in enumerate(COLS):g.text((LW*S+CW*S*j+12*S,HD*S-34*S),t,font=fb(14),fill=(170,178,190));g.text((LW*S+CW*S*j+12*S,HD*S-14*S),sub,font=fr(11),fill=(120,128,140))
  ACC={'tcy':'#3fb8e6','mg':'#ffa040','sw':'#9b7bff','cp':'#e0b552'}
  for i,(m,home,name) in enumerate(ROWS):
    y0=HD*S+CH*S*i;F=tuple(int(ACC[m][k:k+2],16) for k in (1,3,5))
    g.rectangle([12*S,y0+10*S,15*S,y0+CH*S-10*S],fill=F);g.text((24*S,y0+14*S),home,font=fb(20),fill=F);g.text((24*S,y0+44*S),name,font=fr(12),fill=(200,204,212))
    g.text((24*S,y0+64*S),'rds_'+info[m]['style'],font=fr(11),fill=(120,128,140));g.text((24*S,y0+82*S),'radius %d m with four labs'%info[m]['r'],font=fr(11),fill=(120,128,140))
    for j in range(len(COLS)):sh.paste(Image.open(shots[(m,j)]).convert('RGB'),(LW*S+CW*S*j,y0))
  y0=HD*S+CH*S*len(ROWS)+20*S;g.text((24*S,y0+14*S),'For scale',font=fb(20),fill=(200,204,212))
  g.text((24*S,y0+44*S),'Teal & Corvane, four labs,\nbeside a Halcyon depot\nand a Halcyon interceptor',font=fr(12),fill=(160,168,180))
  sh.paste(Image.open(fscale).convert('RGB'),(LW*S,y0))
  g.text((20*S,H-28*S),'Errors in the page: %s'%(errs[:2] if errs else 'none'),font=fr(11),fill=(110,118,130))
  sh.save(OUT);print('wrote',OUT,sh.size,'errors:',errs[:4])
asyncio.run(main())
