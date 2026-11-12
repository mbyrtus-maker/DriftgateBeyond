//@src 16zzzzf_gfx.js
// ============================================================ the graphics pass (Beyond, 11 Nov 2026)
// The user's ask: thrusters and guns with shape; parts oriented right and mounted right. This file is the game's side of it;
// the models' side is in tools/ (brood.Mesh.vent, beyond_hulls.barrel, beyond_recon.seat, the pack's new points).
//   - Engine flares sit on the nozzles. A model whose builder recorded its nozzles carries them as its engine points (the
//     pack's 'ex'), one flare each; engFix no longer guesses for those.
//   - Shots leave from the guns. Each model carries its gun muzzles ('g'). A shot is still simulated from the point it always
//     was (so aim, hits and balance are untouched); only its drawing starts at the muzzle and eases onto the true path in
//     0.15 s, and its tail grows out of the muzzle instead of starting behind it. A short flash marks the muzzle.
//   - Mining beams leave from the hull's mining heads ('ml'), drawing only.
//   - The live turret on Bomber and Heavy Bomber hulls stands on the model's own seat ('ts'): its base ring on the hull, its
//     guns pitching on trunnions above it. It was drawn at one fixed point for every hull (floating over some, sunk into
//     others, a second turret on top of one already modelled), and the whole thing, base and all, pitched with the guns.
//     The mount point gameplay reads (where its shots start and the gunner sits) moves with it: see turMount below.
//   - Missiles and torpedoes have a body.
// ---- the model a mesh was built from, so a ship's entity can reach its model's points
{const o=mdlMesh;mdlMesh=function(name,fac,s){const m=o.apply(this,arguments);if(m)m.mdl=name;return m}}
function entMdl(e){try{const m=shipMesh(e.side==='pirate'?'pirate':e.fac,e.role==='limpet'?'limpet':e.cls),n=m&&m.hull&&m.hull.mdl;return n&&MDL.i?MDL.i[n]||null:null}catch(err){return null}}
{const o=engFix;engFix=function(name){const M=MDL.i&&MDL.i[name];if(M&&M.ex)return M.e;return o.apply(this,arguments)}}
// ---- shots drawn from the muzzle
const GFX={ease:.15,flash:.07},_gfv={x:0,y:0,z:0};
function gfxShot(e,b){try{const M=entMdl(e),g=M&&M.g;if(!g||!g.length)return b;const sc=e.st.radius*1.25;e._gi=((e._gi||0)+1)%g.length;const p=g[e._gi];qRot(e.q,p[0]*sc,p[1]*sc,p[2]*sc,_gfv);
  b.ox=e.x+_gfv.x-b.x;b.oy=e.y+_gfv.y-b.y;b.oz=e.z+_gfv.z-b.z;b.ot=W.t;e._mf=W.t}catch(err){}return b}
// a turret's shot: from the tip of the barrel that fired (the turret's guns are shorter than the old box barrels)
function gfxTurShot(e,T,b){try{const sc=e.st.radius*1.25,q=turretQ(e,T,_gq3);qRot(q,(T.barrel>0?1:-1)*GT.bx*sc,0,GT.tip*sc,_gfv);const M=turretMount(e);b.ox=M.x+_gfv.x-b.x;b.oy=M.y+_gfv.y-b.y;b.oz=M.z+_gfv.z-b.z;b.ot=W.t}catch(err){}return b}
// where a shot is drawn: its head, and how long a tail it has grown
const _gsp={x:0,y:0,z:0,L:0};
function gfxShotPos(b,sp,L){let k=0,gl=L;if(b.ot!==undefined){const a=W.t-b.ot;k=a<GFX.ease?1-a/GFX.ease:0;k*=k;gl=Math.min(L,Math.max(1,sp*a))}_gsp.x=b.x+(k?b.ox*k:0);_gsp.y=b.y+(k?b.oy*k:0);_gsp.z=b.z+(k?b.oz*k:0);_gsp.L=gl;return _gsp}
// a ship's mining heads in the world: head i of n beams, or null when its model has none
function gfxMineHead(e,li,nl,out){const M=entMdl(e),ml=M&&M.ml;if(!ml||!ml.length)return null;const n=ml.length,i=nl<=1?(n>>1):Math.round(li*(n-1)/(nl-1)),p=ml[Math.min(n-1,i)],sc=e.st.radius*1.25;qRot(e.q,p[0]*sc,p[1]*sc,p[2]*sc,out);out.x+=e.x;out.y+=e.y;out.z+=e.z;return out}
// the muzzle flash of a ship that has just fired (drawn with the engine flares)
function gfxFlash(e,sc,c){if(e._mf===undefined)return;const a=W.t-e._mf;if(a<0||a>GFX.flash)return;const M=entMdl(e),g=M&&M.g;if(!g||!g.length)return;const p=g[(e._gi||0)%g.length],k=1-a/GFX.flash;qRot(e.q,p[0]*sc,p[1]*sc,p[2]*sc,_gfv);
  sprite(e.x+_gfv.x,e.y+_gfv.y,e.z+_gfv.z,sc*.16*(1.2-k*.4),c,.8*k);sprite(e.x+_gfv.x,e.y+_gfv.y,e.z+_gfv.z,sc*.07,[1,1,1],.9*k)}
// ---- the live turret: its seat on each hull
// GT: the turret in units of the hull's draw scale: the base ring's radius, the height of the trunnions above the seat, the
// guns' offset either side and their tips ahead of the trunnions
const GT={r:.075,piv:.052,bx:.016,tip:.3};
// (y, z) of the turret's pivot on the hull: the model's seat plus the pivot's height; hulls without a seat keep the old mount
{const o=turMount;turMount=function(e){const M=entMdl(e),s=M&&M.ts;if(s)return[s[1]+GT.piv,s[2]];return o.apply(this,arguments)}}
// the mesh: a base that only turns (turntable, yoke) and a head that pitches on it (trunnion block, twin guns), cached by
// palette; the Brood's is grown (a mound of flesh, two bone spitters)
gturretMesh=function(fac){const key='gt2'+fac;if(MESH[key])return MESH[key];const P=mdlPal(fac),LI=P.c[0],MI=P.c[1],DK=P.c[2],AC=P.c[3],GL=P.c[4],GW=P.c[5],b=new GB(),h=new GB(),L=new GB(),qz=qAxis(1,0,0,Math.PI/2,q0()),qx=qAxis(0,0,1,-Math.PI/2,q0()),r=GT.r,pv=GT.piv;
  L.seg([0,0,0],[0,0,0],[0,0,0]);
  if(fac==='brood'){
    // base: a puckered mound (drawn about the pivot, so its foot is pv below); head: a knuckle and two curved spitters
    b.set(0,-pv+.012,0).cyl(r*1.05,r*.8,.024,9,AC);b.set(0,-pv+.036,0).cyl(r*.8,r*.5,.026,9,scaleC(AC,.85));b.set(0,-pv+.03,0).torus(r*.9,.006,9,3,LI);
    h.set(0,0,0).sphere(.03,5,8,MI);for(const s of[-1,1]){h.set(GT.bx*s,.002,.1,qz).cyl(.012,.008,.16,5,LI);h.set(GT.bx*s,.006,.235,qz).cyl(.008,.0035,.13,5,LI);h.set(.024*s,.014,.012).sphere(.014,4,6,GW,.9)}
    return MESH[key]={base:b.upload(),hull:h.upload(),rim:L.upload(true)}}
  // base: a turntable ring with an accent band, a low faceted drum and two yoke cheeks up to the trunnions
  b.set(0,-pv+.008,0).cyl(r,r*.96,.016,10,DK);b.set(0,-pv+.019,0).cyl(r*.97,r*.97,.006,10,AC,.35,false);b.set(0,-pv+.03,0).cyl(r*.9,r*.66,.022,10,MI);
  for(const s of[-1,1]){b.set(s*.036,-pv*.42,0).box(.012,pv*1.05,.04,LI);b.set(s*.044,0,0,qx).cyl(.012,.012,.006,6,DK)}
  // head: a chamfered trunnion block with a glacis, a lit sight, twin guns (sleeve, barrel, muzzle collar)
  tuPrism(h,[[-.034,tuOct(.029,.019,.007,.004)],[-.02,tuOct(.03,.024,.009,.004)],[.022,tuOct(.03,.024,.009,.004)],[.046,tuOct(.022,.013,.006,0)]],LI);
  h.set(0,.029,-.006).box(.03,.004,.03,GL,.2);h.set(.012,.012,.0465).box(.012,.006,.003,GW,.9);h.set(0,.004,-.0345).box(.036,.016,.003,DK);
  for(const s of[-1,1]){const x=GT.bx*s;h.set(x,0,.07,qz).cyl(.0105,.0095,.07,6,MI);h.set(x,0,.18,qz).cyl(.0062,.0056,.2,6,DK,0,false);h.set(x,0,.092,qz).cyl(.0074,.0074,.008,6,AC,.35,false);h.set(x,0,GT.tip-.012,qz).cyl(.0092,.0086,.024,6,MI)}
  return MESH[key]={base:b.upload(),hull:h.upload(),rim:L.upload(true)}};
// drawn at the pivot: the base turned about the hull's up by the turret's yaw only, the head by yaw and pitch
const _gtq=q0(),_gtq2=q0();
function gfxDrawTurret(e,fac,sc){const T=e.tur||{yaw:Math.PI,pitch:.1},m=turMount(e);qRot(e.q,0,m[0]*sc,m[1]*sc,_u);const x=e.x+_u.x,y=e.y+_u.y,z=e.z+_u.z,tm=gturretMesh(fac);
  if(tm.base){qMul(e.q,qAxis(0,1,0,T.yaw,_gtq2),_gtq);mModel(MM,x,y,z,_gtq,sc,sc,sc);drawMesh(tm.base,MM,ONE3,ZERO3)}
  turretQ(e,T,_gq3);mModel(MM,x,y,z,_gq3,sc,sc,sc);drawMesh(tm.hull,MM,ONE3,ZERO3);drawMesh(tm.rim,MM)}
// ---- missiles and torpedoes with a body (they were a streak and two sprites): a finned body along its flight, in the pass
// the works draw in; the streak and the motor's glow stay as they were, behind it
function mslMesh(kind){const key='msl'+kind;if(MESH[key])return MESH[key];const g=new GB(),qz=qAxis(1,0,0,Math.PI/2,q0()),tp=kind==='torpedo',B=tp?[.42,.44,.48]:[.62,.64,.68],D=[.2,.21,.24],A=tp?[1,.62,.25]:kind==='swarm'?[1,.5,.72]:[.9,.3,.25];
  // model units: 1 = the missile's length, nose at +z; a nose cone, a banded body, a motor nozzle, four fins
  g.set(0,0,.36,qz).cyl(tp?.075:.055,.012,.28,8,A);g.set(0,0,-.02,qz).cyl(tp?.075:.055,tp?.075:.055,.48,8,B);g.set(0,0,.2,qz).cyl(tp?.078:.058,tp?.078:.058,.03,8,D,0,false);
  g.set(0,0,-.31,qz).cyl(tp?.05:.036,tp?.07:.052,.1,8,D);g.set(0,0,-.385,qz).cyl(tp?.04:.03,tp?.052:.04,.05,8,D,0,false);g.set(0,0,-.36,qz).cyl(tp?.034:.024,tp?.034:.024,.004,8,[1,.85,.6],1);
  for(let i=0;i<4;i++){const a=i/4*TAU+(tp?0:Math.PI/4),c=Math.cos(a),s=Math.sin(a),r0=tp?.07:.05,r1=tp?.17:.14;g.set(0,0,0);
    const p=(r,zz)=>[c*r,s*r,zz],w=.006,n=[-s*w,c*w,0],P=(q,k)=>[q[0]+n[0]*k,q[1]+n[1]*k,q[2]];const A1=p(r0,-.12),A2=p(r1,-.3),A3=p(r1,-.36),A4=p(r0,-.34),ce=[c*(r0+r1)/2,s*(r0+r1)/2,-.28];
    g.quad(P(A1,1),P(A2,1),P(A3,1),P(A4,1),D,0,ce);g.quad(P(A1,-1),P(A4,-1),P(A3,-1),P(A2,-1),D,0,ce);g.quad(P(A1,1),P(A1,-1),P(A2,-1),P(A2,1),A,0,ce);g.quad(P(A2,1),P(A2,-1),P(A3,-1),P(A3,1),D,0,ce)}
  return MESH[key]=g.upload()}
const _mq=q0();
{const o=drawWorks;drawWorks=function(t){const r=o.apply(this,arguments);try{if(W&&W.missiles&&W.missiles.length)for(const m of W.missiles){const sp=hyp(m.vx,m.vy,m.vz);if(sp<1)continue;const k=(MK[m.kind]||MK.missile).k,L=11*k;if(!inView(m.x,m.y,m.z,L))continue;
  const up=Math.abs(m.vy)/sp>.95?1:0;qLook(m.vx,m.vy,m.vz,up,up?0:1,0,_mq);const ux=m.vx/sp,uy=m.vy/sp,uz=m.vz/sp;
  // the body's nose at the missile's point, its tail back along the flight (the streak's first two thirds)
  mModel(MM,m.x-ux*L*.5,m.y-uy*L*.5,m.z-uz*L*.5,_mq,L,L,L);drawMesh(mslMesh(m.kind==='torpedo'?'torpedo':m.kind==='swarm'?'swarm':'missile'),MM)}}catch(err){if(!gfxErr++)console.error(err)}return r}}
let gfxErr=0;
