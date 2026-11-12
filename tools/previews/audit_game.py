# Driftgate Beyond: graphics audit sheets (11 Nov 2026). Every model in the pack as the game draws it, from four angles,
# with what the game attaches to it: engine glows and thrust streaks on its engine points, a shot leaving each of the points
# its guns fire from, the mining beams, a gunboat's or bomber's live turret, a capital's point-defence and main-gun points,
# and a station's or base's live turrets on their seats. Rendered in the built game (index.html) in Chromium, through the
# game's own mdlMesh/engFix/engGlow/bolt/drawTurret, so what the sheet shows is what the game's renderer does.
# Usage: flock /tmp/dgbeyond-browser.lock python3 tools/previews/audit_game.py OUTDIR [TAG] [model ...]
#   OUTDIR/audit_<TAG>_NN.png, seven models a sheet. DG_GAME picks the page (default: the repo's index.html).
#   CELL=WxH, PER=rows a sheet, ZOOM=closer by that factor. VIEWSET=turret: side and three-quarter views; TURRET=yaw,pitch poses the live turret.
#   CODE=1 adds the sheet of parts drawn in code (turrets, gate, beacon, crate, rocks, the Bloom Heart, shots, missiles).
import asyncio,json,os,sys,tempfile,math
from playwright.async_api import async_playwright
from PIL import Image,ImageDraw,ImageFont
HERE=os.path.dirname(os.path.abspath(__file__))
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(HERE,'..','..','index.html')))
OUTD=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else '.');TAG=sys.argv[2] if len(sys.argv)>2 else 'now';ONLY=sys.argv[3:]
CW,CH=[int(v) for v in os.environ.get('CELL','300x225').split('x')];PER=int(os.environ.get('PER','7'));ZOOM=float(os.environ.get('ZOOM','1'))   # CELL=520x390 PER=3 ZOOM=1.5 for a closer look
VIEWS=[('chase (behind, above)',math.pi+.42,.3,0),('front 3/4',.62,.26,0),('side',math.pi/2,.02,0),('top',0,1.5,1)]
if os.environ.get('VIEWSET')=='turret':VIEWS=[('side',math.pi/2,.02,0),('rear three-quarters',math.pi+.7,.32,0),('front three-quarters',.75,.3,0),('from astern, level',math.pi,.06,0)]
JS_SETUP=r"""(()=>{
 const A=window.__A={items:[],eng:[],shots:[],beams:[],turs:[],spr:[],gt:null,cam:{yaw:0,pit:0,d:6,fov:26,top:0,t:[0,0,0]},fl:1.25,thr:1,col:[1,1,1],scol:[1,1,1]};
 const sl=Math.hypot(-.42,.7,.58);
 draw3D=function(){
  G.viewport(0,0,glc.width,glc.height);G.clearColor(.035,.045,.065,1);G.clear(G.COLOR_BUFFER_BIT|G.DEPTH_BUFFER_BIT);
  const C=A.cam,x=Math.sin(C.yaw)*Math.cos(C.pit)*C.d,y=Math.sin(C.pit)*C.d,z=Math.cos(C.yaw)*Math.cos(C.pit)*C.d;
  cam.x=C.t[0]+x;cam.y=C.t[1]+y;cam.z=C.t[2]+z;if(C.top)qLook(-x,-y,-z,0,0,1,cam.q);else qLook(-x,-y,-z,0,1,0,cam.q);cam.fov=C.fov;computeMatrices();
  SCN.sun={x:-.42/sl,y:.7/sl,z:.58/sl};SCN.sunCol=[1,.95,.86];SCN.amb=[.2,.22,.29];
  G.disable(G.BLEND);G.enable(G.DEPTH_TEST);G.depthMask(true);G.depthFunc(G.LEQUAL);useMesh();
  for(const it of A.items){mModel(MM,it.p[0],it.p[1],it.p[2],it.q||Q_ID,it.s,it.s,it.s);drawMesh(it.m,MM)}
  for(const t of A.turs)drawTurret(t.tm,t.p[0],t.p[1],t.p[2],t.n[0],t.n[1],t.n[2],t.aim,t.s,ONE3);
  if(A.gt){if(A.gt.m.base){mModel(MM,A.gt.p[0],A.gt.p[1],A.gt.p[2],A.gt.qb||A.gt.q,1,1,1);drawMesh(A.gt.m.base,MM,ONE3,ZERO3)}mModel(MM,A.gt.p[0],A.gt.p[1],A.gt.p[2],A.gt.q,1,1,1);drawMesh(A.gt.m.hull,MM,ONE3,ZERO3);drawMesh(A.gt.m.rim,MM)}
  G.enable(G.BLEND);G.blendFunc(G.ONE,G.ONE);G.depthMask(false);useMesh();
  if(A.bub){mModel(MM,0,0,0,Q_ID,A.bub[0],A.bub[1],A.bub[2]);drawMesh(GEN.shield,MM,A.bub[3],ZERO3,A.bub[4])}
  _f.x=0;_f.y=0;_f.z=-1;
  for(const e of A.eng){engGlow(e[0],e[1],e[2],e[3],A.fl,A.col);if(A.thr){const L=e[3]*9;streak(e[0],e[1],e[2],e[0],e[1],e[2]-L,e[3]*.8,A.col,.32)}}
  for(const b of A.shots){if(A.strk)streak(b[0],b[1],b[2],b[3],b[4],b[5],3,[.85,.85,.9],.9);else bolt(b[0],b[1],b[2],b[3],b[4],b[5],b[6],b[7]||A.scol,1)}
  for(const b of A.beams){capsule(b[0],b[1],b[2],b[3],b[4],b[5],b[6]*7,b[7],.3);capsule(b[0],b[1],b[2],b[3],b[4],b[5],b[6]*3,b[7],.6);capsule(b[0],b[1],b[2],b[3],b[4],b[5],b[6]*1.1,[1,1,1],.85)}
  for(const s of A.spr)sprite(s[0],s[1],s[2],s[3],s[4],s[5]);
  flushBB();G.depthMask(true);G.disable(G.BLEND)};
 // which power flies each model, and as what class
 const who={};const put=(m,fac,cls)=>{if(m&&!who[m])who[m]={fac,cls}};
 for(const f in DESIGN)for(const c in DESIGN[f])put(DESIGN[f][c].m,f,c);
 for(const f in WORK_MDL)for(const c in WORK_MDL[f])put(WORK_MDL[f][c],f,c);
 for(const f of['halcyon','varkesh','ostrova','pirate'])for(const c of Object.keys(FAC_MDL[f]))put(FAC_MDL[f][c],f,c);
 for(const c in BRAND_MDL)put(BRAND_MDL[c],{gannet:'halcyon',bombard:'varkesh',vesper:'ostrova',wraith:'wraith'}[c],c);
 for(const f in DST.mdl)put(DST.mdl[f],f,f==='pirate'?'carrier':'frigate');
 for(const c in BROOD_MDL)put(BROOD_MDL[c],'brood',c);put('b_gullet','brood','frigate');
 for(const c of['interceptor','striker','heavy','bomber','scout','scout2','picket','gunboat','skiff','prospector','dredger','courier','freighter','bulker','constructor','carrier','escort'])put(c,'neutral',c);
 window.__who=who;
 window.__set=function(name){const M=MDL.i[name],w=who[name]||{},A=window.__A;let fac=w.fac||'neutral';A.items=[];A.eng=[];A.shots=[];A.beams=[];A.turs=[];A.spr=[];A.gt=null;A.bub=null;
  const info={name,kind:M.k,n:M.n,fac,cls:w.cls||'',K:1};
  if(M.k==='ship'){const cls=w.cls,C=CLASSES[cls]||{},r=C.radius||14,sc=r*1.25;info.r=r;const pfac=fac==='wraith'?'wraith':fac;
   A.items.push({m:mdlMesh(name,pfac,1),p:[0,0,0],s:1});A.eng=engFix(name).map(e=>e.slice());info.eng=A.eng;
   const fc=fac==='neutral'||fac==='wraith'?[.9,.9,.8]:hexRGB(sideCol(fac==='pirate'?'pirate':fac));A.col=fc;A.scol=fc;A.fl=1.25;A.thr=1;
   const cap=!!(M.tp&&M.tp.length)||cls==='carrier'||cls==='escort'||cls==='frigate';
   if(cap){for(const p of M.tp||[]){A.spr.push([p[0],p[1],p[2],.035,[1,1,.6],.9])}
     if(cls==='frigate'||(fac==='pirate'&&cls==='carrier'))A.shots.push([0,.08,.76,0,.08,.76+70/sc,8/sc,null]);info.tp=(M.tp||[]).length}
   else if(fac!=='brood'||true){const L=16/sc,w=2.6*.95/sc;if(cls==='bombard'){A.shots.push([0,0,.96+.45,0,0,.96+.45+L*1.6,w*1.6,null]);A.spr.push([0,0,.96,.035,[1,1,1],1])}else if(M.g&&M.g.length){for(const p of M.g)A.shots.push([p[0],p[1],p[2]+.12,p[0],p[1],p[2]+.12+L*.6,w*.6,null]);info.g=M.g.length}else for(const sx of[-1,1]){A.shots.push([sx*.336,0,.8+.45,sx*.336,0,.8+.45+L,w,null]);A.spr.push([sx*.336,0,.8,.035,[1,1,1],1])}}
   if(C.lasers){const nl=C.lasers,ml=M.ml;for(let li=0;li<nl;li++){const o=(li-(nl-1)/2)*.55,h=ml&&ml.length?ml[Math.min(ml.length-1,nl<=1?(ml.length>>1):Math.round(li*(ml.length-1)/(nl-1)))]:[o,0,1];A.beams.push([h[0],h[1],h[2],o*.3,-.25,3.2,1/sc,[.95,.6,.3]])}info.ml=(ml||[]).length}
   if(hasTur(cls)){const tm=gturretMesh(pfac),m=M.ts&&typeof GT!=='undefined'?[M.ts[1]+GT.piv,M.ts[2]]:(TUR_MOUNT[cls]||[.3,-.38]),q=q0(),q1=q0(),q2=q0(),yaw=window.__tyaw===undefined?Math.PI:window.__tyaw,pit=window.__tpit===undefined?.1:window.__tpit;qMul(Q_ID,qAxis(0,1,0,yaw,q1),q2);const qb={x:q2.x,y:q2.y,z:q2.z,w:q2.w};qMul(q2,qAxis(1,0,0,-pit,q1),q);A.gt={m:tm,p:[0,m[0],m[1]],q,qb};info.seat=M.ts?1:0}
   return info}
  // structures: in their own units x the size the game draws them at
  let K=1,tur=[];const by=name.startsWith('by_');
  if(/^by_(d\d_)?depot\d$/.test(name)||/^by_(d\d_)?core$/.test(name)){K=/core$/.test(name)?BM.K.station:BM.K.depot;fac='player';const g=new GB();bmPart(g,name,fac,0,K,0,0,0);A.items.push({m:g.upload(),p:[0,0,0],s:1});
    const c=M.c||[0,0,0],h=M.h||1;(M.tp||[]).forEach((p,i)=>{const n=M.tn[i];tur.push({p:[(p[0]*h+c[0])*K+n[0]*BM.tuLift,(p[1]*h+c[1])*K+n[1]*BM.tuLift,(p[2]*h+c[2])*K+n[2]*BM.tuLift],n:n.slice(),s:BM.tuS})});info.K=K;info.R=h*K;info.c=c.map(v=>v*K)}
  else if(/^by_(st|dp)_|^by_freeport|^by_haven/.test(name)){fac=/halcyon|varkesh|ostrova/.exec(name);fac=fac?fac[0]:name==='by_haven'?'pirate':'neutral';const kind=/^by_st/.test(name)?'core':/^by_dp/.test(name)?'depot':name==='by_haven'?'haven':'free',size=ST_MDL.size[kind];
    const m=stMesh(name,fac,size);A.items.push({m:m.core,p:[0,0,0],s:1});const n=kind==='depot'?4:6;for(const p of stSurf(name,size,n)){const l=Math.hypot(...p)||1;tur.push({p:p.slice(),n:p.map(v=>v/l),s:1.15})}info.R=size;info.K=size/(M.h||1)}
  else if(by||name.startsWith('rd')){K=name.startsWith('by_lair')?BM.K.lair:by?BM.K.station*BM.bS:RDS.K;fac=name.startsWith('rd')?(/halcyon|varkesh|ostrova/.exec(name)||['neutral'])[0]:name==='by_rift'?'neutral':'player';
    if(name==='by_rift'){const g=new GB();mdlTris(name,'neutral',1,g,RIFT_PAL);A.items.push({m:g.upload(),p:[0,0,0],s:60});info.R=60}
    else{const g=new GB();bmPart(g,name,fac,0,K,-(M.c||[0,0,0])[0]*K,-(M.c||[0,0,0])[1]*K,-(M.c||[0,0,0])[2]*K);A.items.push({m:g.upload(),p:[0,0,0],s:1});info.R=(M.h||1)*K;info.K=K;
}}
  else{const s=M.s||100;A.items.push({m:mdlMesh(name,'neutral',s),p:[0,0,0],s:1});info.R=s;for(const p of M.tp||[])tur.push({p:[p[0]*s,p[1]*s+3,p[2]*s],n:[0,1,0],s:name==='rockbase'?1.15:1.6})}
  info.fac=fac;const TM=turretMesh(fac==='player'?'player':fac);for(const t of tur){const l=Math.hypot(t.n[0],0,t.n[2])||0;const aim=l>.3?{x:t.n[0]/l,y:.15,z:t.n[2]/l}:{x:.7,y:t.n[1]>0?.2:-.2,z:.7};const al=Math.hypot(aim.x,aim.y,aim.z);aim.x/=al;aim.y/=al;aim.z/=al;A.turs.push({tm:TM,p:t.p,n:t.n,aim,s:t.s})}
  info.tur=tur.length;A.thr=0;return info};
 return Object.keys(MDL.i).length})()"""
JS_CODE=r"""(()=>{const A=window.__A,clr=()=>{A.items=[];A.eng=[];A.shots=[];A.beams=[];A.turs=[];A.spr=[];A.gt=null;A.bub=null;A.thr=0;A.strk=0};
 const ship=(n,f)=>{A.items.push({m:mdlMesh(n,f,1),p:[0,0,0],s:1});A.col=hexRGB(sideCol(f));A.scol=A.col;return engFix(n).map(e=>e.slice())};
 window.__code={
  'station turret (turretMesh), Halcyon':()=>{clr();A.turs.push({tm:turretMesh('halcyon'),p:[0,0,0],n:[0,1,0],aim:{x:0,y:.2,z:.98},s:1});return 48},
  'station turret, Varkesh, aimed up and aside':()=>{clr();A.turs.push({tm:turretMesh('varkesh'),p:[0,0,0],n:[0,1,0],aim:{x:.6,y:.6,z:.53},s:1});return 48},
  'station turret firing (shot style turret)':()=>{clr();A.turs.push({tm:turretMesh('ostrova'),p:[0,0,0],n:[0,1,0],aim:{x:0,y:0,z:1},s:1});A.scol=hexRGB(sideCol('ostrova'));A.shots.push([0,0,55,0,0,55+26,3.4,null]);return 60},
  'ship turret (gturretMesh) on a gunboat hull':()=>{clr();ship('dz_warhound','varkesh');const q=q0(),q1=q0(),q2=q0();qMul(Q_ID,qAxis(0,1,0,2.4,q1),q2);qMul(q2,qAxis(1,0,0,-.3,q1),q);A.gt={m:gturretMesh('varkesh'),p:[0,.28,-.38],q};return 1},
  'ship turret alone':()=>{clr();A.gt={m:gturretMesh('halcyon'),p:[0,0,0],q:Q_ID};return .45},
  'engine: idle':()=>{clr();A.eng=ship('dz_kite','halcyon');A.fl=.5;return 1},
  'engine: thrust':()=>{clr();A.eng=ship('dz_kite','halcyon');A.fl=1.25;A.thr=1;return 1},
  'engine: boost (streak 16x)':()=>{clr();A.eng=ship('dz_talon','varkesh');A.fl=1.9;A.thr=1;return 1},
  'kinetic shots: pulse, slug, lance, scrap, spore':()=>{clr();ship('dz_swift','halcyon');const sc=12.5;let i=0;for(const k of['pulse','slug','lance','scrap','spore']){const st=SHOT_STY[k],x=(i-2)*.5;A.shots.push([x,0,1.2,x,0,1.2+st[0]/sc,st[1]*.95/sc,[[.31,.85,.82],[1,.48,.24],[.72,.58,1],[.85,.8,.6],[.6,.89,.35]][i]]);i++}return 1.4},
  'laser beam from the nose':()=>{clr();ship('dz_mote','ostrova');A.beams.push([0,0,1,.4,.2,5,1/12.5,hexRGB(sideCol('ostrova'))]);A.spr.push([0,0,1,7/12.5,hexRGB(sideCol('ostrova')),.85]);return 1.3},
  'mining beams (Heavy Miner, 3 lasers)':()=>{clr();ship('dz_heron','halcyon');for(const o of[-.55,0,.55])A.beams.push([o,0,1,o*.2,-.3,4,1/28,[.95,.6,.3]]);return 1.3},
  'missile, swarm and torpedo in flight':()=>{clr();let i=0;for(const kind of['missile','swarm','torpedo']){const k=(MK[kind]||MK.missile).k,x=(i-1)*30,c=[1,.7,.3];A.spr.push([x,0,-14*k,11*k,c,1],[x,0,-14*k,4*k,[1,1,1],1]);A.shots.push([x,0,-14*k,x,0,0,0,null]);if(k>1)A.spr.push([x,0,0,26,[1,.75,.3],.5]);if(typeof mslMesh==='function')A.items.push({m:mslMesh(kind),p:[x,0,-5.5*k],s:11*k});i++}A.strk=1;return 30},
  'ship shield: hit flash':()=>{clr();ship('dz_osprey','halcyon');A.bub=[1.5,1.05,1.65,[.45,.75,1],.13];return 1.7},
  'jump gate':()=>{clr();A.items.push({m:GEN.gate,p:[0,0,0],s:1});return 130},
  'sector beacon':()=>{clr();A.items.push({m:GEN.bcn,p:[0,0,0],s:1.25},{m:GEN.bcnL,p:[0,0,0],s:1.25},{m:GEN.bcnRing,p:[0,25,0],s:1.25});return 70},
  'crate and wreck point':()=>{clr();A.items.push({m:GEN.crate,p:[0,0,0],s:16},{m:GEN.crateL,p:[0,0,0],s:16});return 22},
  'asteroids (ferrite, aurorite, comet)':()=>{clr();A.items.push({m:astMesh(1,'fe'),p:[-2.4,0,0],s:1},{m:astMesh(3,'au'),p:[0,0,0],s:1},{m:astMesh(5,'comet'),p:[2.4,0,0],s:1});return 3},
  'Riftstone rock':()=>{clr();A.items.push({m:riftMesh(),p:[0,0,0],s:1});return 1.2},
  'the Bloom Heart (broodMesh)':()=>{clr();const m=broodMesh();A.items.push({m:m.core,p:[0,0,0],s:1},{m:m.spin,p:[0,0,0],s:1});return 150},
  'Driftgate 1 station (fallback, code)':()=>{clr();const m=stationMesh('halcyon','core');A.items.push({m:m.core,p:[0,0,0],s:1});return 170}};
 return Object.keys(window.__code)})()"""
async def main():
  os.makedirs(OUTD,exist_ok=True)
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=await b.new_page(viewport={'width':CW,'height':CH},device_scale_factor=2);errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=120000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(3500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await pg.add_style_tag(content='body *{visibility:hidden !important} #gl{visibility:visible !important}')
    n=await ev(JS_SETUP);print('models in pack:',n,flush=True)
    if os.environ.get('TURRET'):
      ty,tp=os.environ['TURRET'].split(',');await ev(f'(()=>{{window.__tyaw={ty};window.__tpit={tp};return 1}})()')
    names=json.loads(await ev("JSON.stringify(Object.keys(MDL.i))"))
    if ONLY:names=[x for x in names if x in ONLY]
    if ONLY==['-']:names=[]
    tmp=tempfile.mkdtemp(prefix='audit_');rows=[]
    for name in names:
      try:info=json.loads(await ev(f"JSON.stringify(__set('{name}'))"))
      except Exception as e:print('FAILED',name,str(e)[:200],flush=True);continue
      R=info.get('R',1.0);shots=[]
      for k,(lab,yaw,pit,top) in enumerate(VIEWS):
        d=R*(5.6 if info['kind']!='ship' else 4.9)/ZOOM
        await ev(f"(()=>{{const C=__A.cam;C.yaw={yaw};C.pit={pit};C.top={top};C.d={d};C.fov=26;return 1}})()");await pg.wait_for_timeout(140)
        f=os.path.join(tmp,f'{name}_{k}.png');await pg.locator('#gl').screenshot(path=f);shots.append(f)
      rows.append((info,shots));print(name,info.get('fac'),info.get('cls'),flush=True)
    code=[]
    if os.environ.get('CODE'):
      for lab in json.loads(await ev("JSON.stringify("+JS_CODE+")")):
        R=float(await ev(f"__code[{json.dumps(lab)}]()"));shots=[]
        for k,(vl,yaw,pit,top) in enumerate(VIEWS):
          await ev(f"(()=>{{const C=__A.cam;C.yaw={yaw};C.pit={pit};C.top={top};C.d={R*5.2};C.fov=26;return 1}})()");await pg.wait_for_timeout(140)
          f=os.path.join(tmp,f'code_{len(code)}_{k}.png');await pg.locator('#gl').screenshot(path=f);shots.append(f)
        code.append(({'name':lab,'kind':'drawn in code','n':0,'fac':'','cls':''},shots));print('code:',lab,flush=True)
    await b.close()
  fb=lambda s:ImageFont.truetype('DejaVuSans-Bold.ttf',s);fr=lambda s:ImageFont.truetype('DejaVuSans.ttf',s)
  for si in range(0,len(rows),PER):
    part=rows[si:si+PER];LW=150;W=LW+CW*len(VIEWS);H=34+CH*len(part)
    sh=Image.new('RGB',(W,H),(9,12,18));g=ImageDraw.Draw(sh)
    g.text((8,8),f'Driftgate Beyond graphics audit · {TAG} · sheet {si//PER+1}',font=fb(14),fill=(230,232,236))
    for k,(lab,_,_,_) in enumerate(VIEWS):g.text((LW+CW*k+6,12),lab,font=fr(11),fill=(130,140,155))
    for r,(info,shots) in enumerate(part):
      y0=34+CH*r;g.text((6,y0+8),info['name'],font=fb(13),fill=(220,224,232))
      g.text((6,y0+28),f"{info.get('fac','')} {info.get('cls','')}",font=fr(11),fill=(150,158,170));g.text((6,y0+44),f"{info['kind']} · {info['n']} tris",font=fr(11),fill=(120,128,140))
      ex=[]
      if info.get('eng') is not None:ex.append(f"{len(info['eng'])} engine pts")
      if info.get('tp'):ex.append(f"{info['tp']} pd mounts")
      if info.get('tur'):ex.append(f"{info['tur']} live turrets")
      if info.get('g'):ex.append(f"{info['g']} gun muzzles")
      if info.get('ml'):ex.append(f"{info['ml']} mining heads")
      if 'seat' in info:ex.append('turret on its seat' if info['seat'] else 'turret: old fixed mount')
      for i,t in enumerate(ex):g.text((6,y0+60+i*15),t,font=fr(11),fill=(120,128,140))
      for k,f in enumerate(shots):sh.paste(Image.open(f).convert('RGB').resize((CW,CH),Image.LANCZOS),(LW+CW*k,y0))
      g.line([(0,y0),(W,y0)],fill=(30,36,48))
    out=os.path.join(OUTD,f'audit_{TAG}_{si//PER+1:02d}.png');sh.save(out);print('wrote',out,flush=True)
  for si in range(0,len(code),PER):
    part=code[si:si+PER];LW=150;W=LW+CW*len(VIEWS);H=34+CH*len(part)
    sh=Image.new('RGB',(W,H),(9,12,18));g=ImageDraw.Draw(sh)
    g.text((8,8),f'Driftgate Beyond graphics audit · {TAG} · parts drawn in code {si//PER+1}',font=fb(14),fill=(230,232,236))
    for r,(info,shots) in enumerate(part):
      y0=34+CH*r;words=info['name'].split(' ');lines=[''];
      for w in words:
        if len(lines[-1])+len(w)>20:lines.append('')
        lines[-1]=(lines[-1]+' '+w).strip()
      for i,t in enumerate(lines):g.text((6,y0+8+i*15),t,font=fb(11),fill=(220,224,232))
      for k,f in enumerate(shots):sh.paste(Image.open(f).convert('RGB').resize((CW,CH),Image.LANCZOS),(LW+CW*k,y0))
      g.line([(0,y0),(W,y0)],fill=(30,36,48))
    out=os.path.join(OUTD,f'audit_{TAG}_code_{si//PER+1:02d}.png');sh.save(out);print('wrote',out,flush=True)
  print('page errors:',errs[:6])
if __name__=='__main__':asyncio.run(main())
