//@src 16x_bases.js
// ============================================================ your bases drawn in the company style (Beyond, after stage 14)
// The approved models from tools/previews/beyond_stations.py, in the model pack as by_*: a Lair (level 1 or 2) set into its
// rock, a Depot by level (1 storage; 2 production and hangar; 3 turrets, armour and the life-support ring), and a Station: the
// core with five hardpoints, each built-on hardpoint carrying its building (shipyard, external storage, defence platform,
// hangar, forge, market wing) in the order you built them. The pack keeps each model's centre and half-extent (c, h) so the
// buildings go back on the core at the right size; each base is assembled once into one mesh and cached by its shape.
const BM={K:{lair:38,depot:48,station:32},hpR:4.6,hpY:-.9,bS:.8,bld:{yard:'by_yard',storage:'by_storage',defence:'by_defence',hangar:'by_hangar',forge:'by_forge',market:'by_market'}};
const BM_HP=[0,1,2,3,4].map(k=>Math.PI/2+k*2*Math.PI/5);
// (8 Nov 2026) six base designs, picked on your company profile (looks only: stats, turrets and buildings are the same). Each
// has a Depot at levels 1-3 and a Station core with the same five hardpoints, so the buildings attach unchanged. Designs 2-6
// are tools/previews/beyond_base_designs.py, in the pack as by_d<N>_depot1-3 and by_d<N>_core with their turret seats as tp.
const BM_DESIGNS=[{id:1,name:'Company standard',note:'a drum hub with a docking arm; the Station a tall spine and habitat ring',depot:n=>'by_depot'+n,core:'by_core'},
  {id:2,name:'Wheel',note:'a standing habitat wheel on an axle',depot:n=>'by_d2_depot'+n,core:'by_d2_core'},
  {id:3,name:'Spire',note:'a tall stepped tower with balconies and a needle',depot:n=>'by_d3_depot'+n,core:'by_d3_core'},
  {id:4,name:'Truss cluster',note:'modules bolted into open cube frames',depot:n=>'by_d4_depot'+n,core:'by_d4_core'},
  {id:5,name:'Disc',note:'a flat lens with a lit rim and docking slots',depot:n=>'by_d5_depot'+n,core:'by_d5_core'},
  {id:6,name:'Asteroid',note:'built into a large rock: hab domes, docking arms, lights',depot:n=>'by_d6_depot'+n,core:'by_d6_core'}];
// the design a base is drawn in (the main session wraps this to read the owner's company profile)
function bmDesignOf(R){return R&&R.design||1}
// the design record for a base, falling back to the standard set when its models aren't in the pack
function bmDesign(R){const D=BM_DESIGNS.find(x=>x.id===bmDesignOf(R));return D&&mdlHas(D.core)&&mdlHas(D.depot(1))?D:BM_DESIGNS[0]}
function bmModel(R){const D=bmDesign(R);return R.pst?D.core:D.depot(Math.min(3,depLvl(R)))}
function bmShape(R){return bmDesign(R).id+(R.pst?'s'+(R.bld||[]).length:'d'+depLvl(R))}
// copy a packed model into a mesh builder in its original model space, turned about +y, scaled and moved
function bmPart(g,name,fac,yaw,s,ox,oy,oz){const M=MDL.i[name];if(!M)return;const n=M.n,P=new Int16Array(MDL.b,M.o,n*9),R=new Uint8Array(MDL.b,M.o+n*18,n),SH=new Uint8Array(MDL.b,M.o+n*19,n),Q=mdlPal(fac),h=(M.h||1)/32767,c=M.c||[0,0,0],cs=Math.cos(yaw),sn=Math.sin(yaw),v=new Float32Array(9);
  for(let t=0;t<n;t++){const o=t*9;for(let j=0;j<3;j++){const x=P[o+j*3]*h+c[0],y=P[o+j*3+1]*h+c[1],z=P[o+j*3+2]*h+c[2];v[j*3]=(cs*x+sn*z)*s+ox;v[j*3+1]=y*s+oy;v[j*3+2]=(-sn*x+cs*z)*s+oz}
    const ux=v[3]-v[0],uy=v[4]-v[1],uz=v[5]-v[2],wx=v[6]-v[0],wy=v[7]-v[1],wz=v[8]-v[2];let nx=uy*wz-uz*wy,ny=uz*wx-ux*wz,nz=ux*wy-uy*wx;const l=Math.hypot(nx,ny,nz)||1;nx/=l;ny/=l;nz/=l;
    const r=R[t],col=Q.c[r],sh=SH[t]/100,em=Q.e[r];for(let j=0;j<3;j++)g.d.push(v[j*3],v[j*3+1],v[j*3+2],nx,ny,nz,col[0]*sh,col[1]*sh,col[2]*sh,em)}}
function bmSpin(){if(MESH.bmSpin)return MESH.bmSpin;const e=new GB();e.seg([0,0,0],[0,0,0],[0,0,0]);return MESH.bmSpin=e.upload(true)}
function bmReady(){return MDL.ready&&mdlHas('by_core')}
// the mesh for a player depot or Station record
function bmBase(R,fac){const st=!!R.pst,lv=st?(R.bld||[]).join(','):String(depLvl(R)),D=bmDesign(R),key='bm'+D.id+(st?'s':'d')+lv+fac;if(MESH[key])return MESH[key];const g=new GB();
  if(st){const K=BM.K.station;bmPart(g,D.core,fac,0,K,0,0,0);(R.bld||[]).slice(0,5).forEach((b,i)=>{const a=BM_HP[i];if(BM.bld[b])bmPart(g,BM.bld[b],fac,Math.PI/2-a,BM.bS*K,Math.cos(a)*BM.hpR*K,BM.hpY*K,Math.sin(a)*BM.hpR*K)})}
  else bmPart(g,D.depot(Math.min(3,depLvl(R))),fac,0,BM.K.depot,0,0,0);
  return MESH[key]={core:g.upload(),spin:bmSpin()}}
function bmLair(lvl,fac){const key='bml'+lvl+fac;if(MESH[key])return MESH[key];const g=new GB();bmPart(g,'by_lair'+(lvl>=2?2:1),fac,0,BM.K.lair,0,0,0);return MESH[key]=g.upload()}
function bmOwned(R){return!!R&&R.owner==='player'&&R.kind==='depot'}
{const o=stationMesh;stationMesh=function(fac,kind){const SE=W&&W.stationEnt,R=SE&&SE.rec;if(fac==='player'&&kind==='depot'&&bmOwned(R)&&bmReady())return bmBase(R,fac);return o.apply(this,arguments)}}
// turrets sit on the model: a Depot's on its dome rim, keel and docking arm; a Station's round its habitat ring and crown.
// The other designs carry their seats in the pack (tp, in the model's packed frame: unpacked with its centre and half-extent).
function bmTurrets(R){const D=bmDesign(R);if(D.id!==1){const M=MDL.i[bmModel(R)],K=R.pst?BM.K.station:BM.K.depot;if(M&&M.tp&&M.tp.length){const c=M.c||[0,0,0],h=M.h||1;return M.tp.map(p=>[(p[0]*h+c[0])*K,(p[1]*h+c[1])*K,(p[2]*h+c[2])*K])}}
  if(R.pst){const K=BM.K.station,out=[];for(let i=0;i<6;i++){const a=i/6*TAU+.3;out.push([Math.cos(a)*3.1*K,.45*K,Math.sin(a)*3.1*K])}out.push([0,2.75*K,0],[0,-3.3*K,0]);return out}
  const K=BM.K.depot;return[...[Math.PI/4,-Math.PI/4,Math.PI*.6].map(a=>[Math.cos(a)*.45*K,1.2*K,Math.sin(a)*.45*K]),[0,-1.65*K,0],[1.4*K,.4*K,0],[-.2*K,.25*K,-1.35*K]]}
{const o=mdlStationTurrets;mdlStationTurrets=function(SE){const R=SE&&SE.rec;if(!SE._mt&&bmOwned(R)&&bmReady()){SE._mt=1;devEnt(SE);const T=bmTurrets(R);SE.turrets.filter(t=>!t.mod).forEach((tu,i)=>{tu.p=T[i%T.length].slice()});SE._bmShape=bmShape(R);return}return o.apply(this,arguments)}}
// a base that changes shape (a new level or building, or a new design) re-seats its turrets
{const o=worldUpdate;worldUpdate=function(dt){const r=o.apply(this,arguments);try{const SE=W&&W.stationEnt,R=SE&&SE.rec;if(SE&&SE._bmShape&&bmOwned(R)){const sh=bmShape(R);if(sh!==SE._bmShape)SE._mt=0}}catch(err){}return r}}
// Lairs: the rock with the hangar cut into it, and its beacon above
{const o=lairDrawB;lairDrawB=function(){if(!bmReady())return o.apply(this,arguments);const k=curPid()||'me';for(const L of(S.lairs||[])){if(L.sid!==W.sid||L.hull<=0||L.pid!==k||!inView(L.x,L.y,L.z,140))continue;
  qAxis(.2,1,.1,.6,_xq);qNorm(_xq);mModel(MM,L.x,L.y,L.z,_xq,1,1,1);drawMesh(bmLair(L.lvl||1,'player'),MM);sprite(L.x,L.y+100,L.z,10+3*Math.sin(W.t*3),L.build>S.T?[.9,.6,.3]:[.85,.8,.55],.6)}}}
