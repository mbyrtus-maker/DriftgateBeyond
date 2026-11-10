//@src 16x2_basemods.js
// ============================================================ your bases: docking ports and development modules on the model
// (10 Nov 2026) A player Depot or Station docks at its own model's collars, and its development modules (the works: storage
// vaults, production works, habitat, shield works, fighter hangar, defence platform) stand on it. Before, a player base
// borrowed the Driftgate 1 depot's ports (rings hanging about 124 m out, inside the bigger Station cores) and its modules
// stood in a row 400 m away. The pack keeps each base model's collar faces ('pt') and a berth per module kind ('wb': the hull
// point a truss strut starts from and the module stack's centre), found clear of the live turrets, the ports' approach lanes,
// every hardpoint's building and each other (tools/previews/beyond_base_designs.py).
// Modules on a player base are drawn at BM.wkS of their free-standing size (their hit spheres too); a kind's units stack on
// its berth. A Station's shipyard works sit in its Shipyard building (the building is the slipway; no second yard is drawn).
// The defence platform carries its turrets on its deck and keel, standing along the deck's normal like the base's own.
BM.wkS=.5;BM.wkStep=2.15;BM.yardS=.65
function bmBaseSE(){const SE=W&&W.stationEnt,R=SE&&SE.rec;return SE&&bmOwned(R)&&bmReady()?SE:null}
function bmLocal(R,p){const M=MDL.i[bmModel(R)],K=R.pst?BM.K.station:BM.K.depot,c=M.c||[0,0,0],h=M.h||1;return[(p[0]*h+c[0])*K,(p[1]*h+c[1])*K,(p[2]*h+c[2])*K]}
// a kind's berth on the base: {H: the strut's hull point, C: the stack's centre} in station-local metres
function bmBerth(R,k){const M=MDL.i[bmModel(R)],B=M&&M.wb&&M.wb[k];return B?{H:bmLocal(R,B[0]),C:bmLocal(R,B[1])}:null}
// docking: the model's own collars
{const o=portName;portName=function(E){if(E&&E.type==='station'&&bmOwned(E.rec)&&bmReady())return bmModel(E.rec);return o.apply(this,arguments)}}
{const o=mdlPorts;mdlPorts=function(name){const M=MDL.ready&&MDL.i[name];if(M&&/^by_(d\d_)?(depot\d|core)$/.test(name)){if(name in PORTS)return PORTS[name];
  const K=/core$/.test(name)?BM.K.station:BM.K.depot,c=M.c||[0,0,0],h=M.h||1;return PORTS[name]=M.pt&&M.pt.length?M.pt.map(p=>[(p[0]*h+c[0])*K,(p[1]*h+c[1])*K,(p[2]*h+c[2])*K]):null}return o.apply(this,arguments)}}
// the works' layout on a player base
{const o=wkLayout;wkLayout=function(kind,k,lvl,slot){const SE=bmBaseSE();if(SE&&kind===SE.kind){const R=SE.rec,sig='bm'+bmShape(R);
    if(k==='yard'&&R.pst){const i=(R.bld||[]).indexOf('yard'),Y=Object.values(S.yards||{}).find(y=>y.pst===R.sid);if(i>=0&&i<5&&Y){const a=BM_HP[i],K=BM.K.station,d=[Math.cos(a),0,Math.sin(a)],r=(BM.hpR+2.9*BM.bS)*K;
      return{yaw:Math.PI/2-a,parts:[[d[0]*(r-WK_SLIP[2]),BM.hpY*K-WK_SLIP[1],d[2]*(r-WK_SLIP[2])]],sc:BM.yardS,hide:true,sig}}}
    const B=k!=='yard'&&k!=='yardb'&&bmBerth(R,k);if(B){const u=WKU[k]*BM.wkS,n=k==='def'?1:Math.max(1,lvl||1),a=Math.atan2(B.C[2]-B.H[2],B.C[0]-B.H[0]),parts=[];
      for(let i=0;i<n;i++){const dy=(i-(n-1)/2)*BM.wkStep*u;parts.push([B.C[0],B.C[1]+dy,B.C[2]])}
      return{yaw:-a,parts,sc:BM.wkS,hub:B.H,sig}}}
  return o.apply(this,arguments)}}
// the defence platform's turrets on a player base: half on its deck, half under its keel, round its middle
{const o=devEnt;devEnt=function(SE){const r=o.apply(this,arguments);try{const R=SE&&SE.rec;if(SE&&W&&SE===W.stationEnt&&bmOwned(R)&&bmReady()){const d=devOf(R),T=SE.turrets.filter(t=>t.mod);
    if(d.def&&T.length){const L=wkLayout(SE.kind,'def',d.def),c=L.parts[0],u=WKU.def*(L.sc||1),n=T.length;T.forEach((tu,i)=>{const up=i%2?-1:1,a=i/n*TAU+.4+L.yaw;
      tu.p=[c[0]+Math.cos(a)*u*.55,c[1]+up*(u*.08+BM.tuLift),c[2]+Math.sin(a)*u*.55];tu.n=[0,up,0]})}SE._subL=null}}catch(err){}return r}}
// the struts: a square truss from the hull to each module stack, and a spine up a stack of more than one unit
function bmStrutMesh(){if(MESH.bmStrut)return MESH.bmStrut;const g=new GB(),D=[.2,.21,.24],A=[.72,.55,.25];
  for(const sx of[-.5,.5])for(const sy of[-.5,.5])g.set(sx,sy,.5).box(.16,.16,1,D);
  for(let k=0;k<=8;k++){const z=k/8;g.set(0,.5,z).box(1,.1,.012,D);g.set(0,-.5,z).box(1,.1,.012,D);g.set(.5,0,z).box(.1,1,.012,D);g.set(-.5,0,z).box(.1,1,.012,D)}
  g.set(0,.56,.04).box(.7,.04,.03,A,.4);g.set(0,.56,.96).box(.7,.04,.03,A,.4);return MESH.bmStrut=g.upload()}
const _bsa={x:0,y:0,z:0},_bsb={x:0,y:0,z:0},_bsq=q0();
function bmStrut(SE,a,b,w){qRot(SE.q,a[0],a[1],a[2],_bsa);qRot(SE.q,b[0],b[1],b[2],_bsb);const fx=_bsb.x-_bsa.x,fy=_bsb.y-_bsa.y,fz=_bsb.z-_bsa.z,L=Math.hypot(fx,fy,fz);if(L<1)return;
  qRot(SE.q,0,1,0,_u);if(Math.abs((fx*_u.x+fy*_u.y+fz*_u.z)/L)>.95)qRot(SE.q,1,0,0,_u);qLook(fx,fy,fz,_u.x,_u.y,_u.z,_bsq);
  mModel(MM,SE.x+_bsa.x,SE.y+_bsa.y,SE.z+_bsa.z,_bsq,w,w,L);drawMesh(bmStrutMesh(),MM)}
function bmStruts(){const SE=bmBaseSE();if(!SE||!inView(SE.x,SE.y,SE.z,900))return;for(const w of W.works||[]){if(!w.hub||!w.parts||!w.parts.length||w.sid!==W.sid)continue;
  const L=wkLayout(SE.kind,w.k,w.lvl,w.slot);if(!L.hub)continue;const P=L.parts,u=WKU[w.k]*(L.sc||1),n=P.length,c=[0,0,0];for(const p of P){c[0]+=p[0]/n;c[1]+=p[1]/n;c[2]+=p[2]/n}
  const dx=c[0]-L.hub[0],dz=c[2]-L.hub[2],l=Math.hypot(dx,dz)||1,e=[c[0]-dx/l*u*.55,L.hub[1],c[2]-dz/l*u*.55];
  bmStrut(SE,L.hub,e,Math.max(7,u*.28));if(n>1)bmStrut(SE,[e[0],P[0][1],e[2]],[e[0],P[n-1][1],e[2]],Math.max(6,u*.24))}}
{const o=drawWorks;drawWorks=function(t){const r=o.apply(this,arguments);try{bmStruts()}catch(err){}return r}}
