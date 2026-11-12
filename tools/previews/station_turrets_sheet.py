# Driftgate Beyond: the live turrets on the powers' stations and depots, the freeports and Scrapheart Haven (12 Nov 2026), for
# review. Drawn in the built game with the game's own calls: the station's mesh (stMesh) and its turrets where the game stands
# them (mdlStationTurrets on a stand-in station, then drawTurret), the whole station first, then each turret close up from the
# side (along the hull) and from three-quarters above. The measured check is tools/stseats.py.
# Usage: flock /tmp/dgbeyond-browser.lock python3 tools/previews/station_turrets_sheet.py OUTDIR [MODEL ...]   (one PNG per model)
import asyncio,json,os,sys,tempfile
from playwright.async_api import async_playwright
from PIL import Image,ImageDraw,ImageFont
HERE=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,HERE)
from audit_game import JS_SETUP,GAME
OUT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else HERE);os.makedirs(OUT,exist_ok=True)
ALL=[('by_st_halcyon','halcyon','core',None,0),('by_st_varkesh','varkesh','core',None,0),('by_st_ostrova','ostrova','core',None,0),
     ('by_dp_halcyon','halcyon','depot',None,0),('by_dp_varkesh','varkesh','depot',None,0),('by_dp_ostrova','ostrova','depot',None,0),
     ('by_dp_halcyon','halcyon','depot',None,1),('by_dp_varkesh','varkesh','depot',None,1),('by_dp_ostrova','ostrova','depot',None,1),
     ('by_freeport','neutral','free','mw',0),('by_freeport_cw','neutral','free','cw',0),('by_freeport_ew','neutral','free','ew',0),('by_haven','pirate','haven','wr',0),('wk_def','varkesh','def',None,0)]
want=sys.argv[2:];CW,CH=300,240
JS=r"""(nm,fac,kind,sid,fwd)=>{const A=__A,n=fwd?STN.fdepot.tur:(STN[kind]||STN.core).tur,SE={type:'station',fac,kind,rec:{sid,fwd:!!fwd,owner:fac,kind},turrets:[]};
 for(let i=0;i<n;i++)SE.turrets.push({p:[0,0,0],aim:{x:0,y:0,z:1},cool:0});
 let size,m;
 if(kind==='def'){
  // the defence platform under a station with Defence works at level 3: the game's own devEnt places its six turrets
  const R={sid:'x',owner:fac,kind:'core',dev:{def:3}},E={type:'station',fac,kind:'core',rec:R,turrets:[],sMax:1,shield:1};R.sMax=1;
  const dO=devOf;devOf=function(r){return r===R?R.dev:dO.apply(this,arguments)};try{devEnt(E)}finally{devOf=dO}
  const c=wkLayout('core','def',3).parts[0];SE.turrets=E.turrets.map(t=>({p:[t.p[0]-c[0],t.p[1]-c[1],t.p[2]-c[2]],n:t.n,aim:t.aim}));size=WKU.def;m={core:wkMesh('wk_def',fac),spin:null}}
 else{const dv=devEnt;devEnt=function(){};try{mdlStationTurrets(SE)}finally{devEnt=dv}
  size=ST_MDL.size[fwd?'fdepot':kind]||150;m=stMesh(nm,fac,size)}
 A.items=[{m:m.core,p:[0,0,0],s:1}];if(m.spin)A.items.push({m:m.spin,p:[0,0,0],s:1});A.eng=[];A.shots=[];A.beams=[];A.spr=[];A.gt=null;A.bub=null;A.thr=0;
 const TM=turretMesh(fac),ts=SE._ts||1.15;A.turs=SE.turrets.map(t=>{const p=t.p,l=Math.hypot(p[0],p[1],p[2])||1,n=t.n||[p[0]/l,p[1]/l,p[2]/l];
   // aimed out along the hull, a little up from its seat
   let ax=p[0]/l-n[0]*(p[0]*n[0]+p[1]*n[1]+p[2]*n[2])/l,ay=p[1]/l-n[1]*(p[0]*n[0]+p[1]*n[1]+p[2]*n[2])/l,az=p[2]/l-n[2]*(p[0]*n[0]+p[1]*n[1]+p[2]*n[2])/l;let al=Math.hypot(ax,ay,az);
   if(al<.2){ax=Math.abs(n[1])>.9?1:0;ay=Math.abs(n[1])>.9?0:1;az=0;const d=ax*n[0]+ay*n[1]+az*n[2];ax-=n[0]*d;ay-=n[1]*d;az-=n[2]*d;al=Math.hypot(ax,ay,az)}
   ax=ax/al+n[0]*.25;ay=ay/al+n[1]*.25;az=az/al+n[2]*.25;al=Math.hypot(ax,ay,az);return{tm:TM,p:p,n:n,aim:{x:ax/al,y:ay/al,z:az/al},s:ts}});
 return JSON.stringify({size,ts,seated:!!SE._ts||kind==='def',t:A.turs.map(t=>({p:t.p,n:t.n}))})}"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=await b.new_page(viewport={'width':CW,'height':CH},device_scale_factor=2);errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=120000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(3500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await pg.add_style_tag(content='body *{visibility:hidden !important} #gl{visibility:visible !important}')
    await ev(JS_SETUP);tmp=tempfile.mkdtemp(prefix='stt_')
    fb=lambda s:ImageFont.truetype('DejaVuSans-Bold.ttf',s);fr=lambda s:ImageFont.truetype('DejaVuSans.ttf',s)
    for nm,fac,kind,sid,fwd in ALL:
      tag=nm+('_fwd' if fwd else '')
      if want and tag not in want and nm not in want:continue
      info=json.loads(await ev("(%s)(%s,%s,%s,%s,%d)"%(JS,json.dumps(nm),json.dumps(fac),json.dumps(kind),json.dumps(sid),fwd)));size=info['size'];T=info['t'];cells=[]
      async def shot(t,yaw,pit,d,label):
        await ev(f"(()=>{{const C=__A.cam;C.t=[{t[0]},{t[1]},{t[2]}];C.yaw={yaw};C.pit={pit};C.top=0;C.d={d};C.fov=26;return 1}})()");await pg.wait_for_timeout(160)
        f=os.path.join(tmp,f'{tag}_{len(cells)}.png');await pg.locator('#gl').screenshot(path=f);cells.append((f,label))
      await shot([0,0,0],.7,.32,size*5.4,'the whole station');await shot([0,0,0],3.6,-.3,size*5.4,'from the other side, below')
      import math
      for i,t in enumerate(T):
        p,n=t['p'],t['n']
        # the side view looks along the hull (square to the seat's normal); the other from three-quarters above the seat
        u=[1.0,0,0] if abs(n[1])>.9 else [n[2],0,-n[0]];ul=math.hypot(*u) or 1;u=[v/ul for v in u]
        for kind_,dv in (('side',[u[0]+n[0]*.08,u[1]+n[1]*.08,u[2]+n[2]*.08]),('three-quarters',[u[0]*.6+n[0]*.62+(n[1]*u[2]-n[2]*u[1])*.5,u[1]*.6+n[1]*.62+(n[2]*u[0]-n[0]*u[2])*.5,u[2]*.6+n[2]*.62+(n[0]*u[1]-n[1]*u[0])*.5])):
          l=math.hypot(*dv);dv=[v/l for v in dv];yaw=math.atan2(dv[0],dv[2]);pit=math.asin(max(-1,min(1,dv[1])))
          await shot(p,yaw,pit,150*info['ts']/1.15,f'turret {i+1} · {kind_}')
      per=4 if len(cells)<=6 else 7 if len(cells)==14 else 5;rows=(len(cells)+per-1)//per
      sh=Image.new('RGB',(CW*per,34+(CH+2)*rows),(9,12,18));g=ImageDraw.Draw(sh)
      g.text((8,8),'%s%s · live turrets on their seats · %d turrets, drawn at %.2f · %s'%(nm,' as a forward depot' if fwd else '',len(T),info['ts'],'seats from the pack' if info['seated'] else 'the old rule (no seats in the pack)'),font=fb(14),fill=(230,232,236))
      for k,(f,label) in enumerate(cells):
        x,y=(k%per)*CW,34+(k//per)*(CH+2);sh.paste(Image.open(f).convert('RGB').resize((CW,CH),Image.LANCZOS),(x,y));g.text((x+6,y+4),label,font=fr(11),fill=(150,160,175))
      o=os.path.join(OUT,'stturrets_%s.png'%tag);sh.save(o);print('wrote',o,sh.size,flush=True)
    print('page errors',errs[:3]);await b.close()
if __name__=='__main__':asyncio.run(main())
