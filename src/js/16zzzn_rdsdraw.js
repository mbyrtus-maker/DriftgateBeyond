//@src 16zzzn_rdsdraw.js
// ============================================================ the makers' R&D stations drawn (Beyond, built 9 Nov 2026)
// Each maker's own small station in its home system (BEYOND_DESIGN.md "A maker's R&D station"; the approved preview of 6 Nov
// 2026, tools/previews/beyond_corp.py; no shields since 9 Nov 2026). Its parts are in the model pack (tools/rdstation.py):
// a tower per home style (rds_halcyon, rds_varkesh, rds_ostrova, rds_free) with the CEO's launch bay at its foot, two turret
// seats and blank logo boards; a lab per style and grade (rdl_<style>_g2..g5) for each socket in use; a marker for an empty
// socket (rdp_<style>). rdsMesh puts them together once per maker and lab set, in the maker's accent (MK_ACC) over its home's
// hull colour, and draws the maker's mark (MK_LOGO, its current one if it was reborn) lit on the boards. An offline station
// (its control centre knocked out) draws with its lights dimmed. Entities of type 'rds' in W.ents (x, y, z, q, m, labs,
// offline) are drawn in the world pass; the gameplay (placement, sub-systems, offline and escrow) lives elsewhere.
// Scale: RDS.K metres per tower unit, so a station with four labs is about 50 m in radius (half a power depot's 105).
const RDS={K:13};
function RDS_STYLE(m){const h=MAKERS[m]&&MAKERS[m].home;return h==='halcyon'||h==='varkesh'||h==='ostrova'?h:'free'}
function rdsReady(){return MDL.ready&&mdlHas('rds_halcyon')}
// a turn as a row-major 3x3: local +z turned up by pitch, then about +y by yaw (from +z toward +x), as the pack records it
function rdsRot(yaw,pitch){const cy=Math.cos(yaw),sy=Math.sin(yaw),cp=Math.cos(pitch),sp=Math.sin(pitch);return[cy,-sy*sp,sy*cp,0,cp,sp,-sy,-cy*sp,cy*cp]}
// the maker's palette: its accent over its home's hull colour; offline, the accent, lights and windows go dim
function rdsPal(m,off){const acc=mkAcc(m),F=hexRGB(acc),st=RDS_STYLE(m),P=mdlPal('co:'+acc),c=P.c.slice(),e=P.e.slice();c[0]=mixC(MDL_HULL[st==='free'?'neutral':st]||[.57,.58,.6],F,.1);
  if(off){c[3]=scaleC(c[3],.5);c[5]=scaleC(F,.25);c[6]=scaleC(c[6],.3);e[4]*=.3;e[5]=.1;e[6]=.05}return{c,e}}
// copy a packed part into the builder: its model space (unpacked with its centre and half-extent), turned by R, scaled, moved
function rdsPart(g,name,pal,R,s,o){const M=MDL.i[name];if(!M)return;const n=M.n,P=new Int16Array(MDL.b,M.o,n*9),RL=new Uint8Array(MDL.b,M.o+n*18,n),SH=new Uint8Array(MDL.b,M.o+n*19,n),h=(M.h||1)/32767,c=M.c||[0,0,0],v=new Float32Array(9);
  for(let t=0;t<n;t++){const q=t*9;for(let j=0;j<3;j++){const x=P[q+j*3]*h+c[0],y=P[q+j*3+1]*h+c[1],z=P[q+j*3+2]*h+c[2];v[j*3]=(R[0]*x+R[1]*y+R[2]*z)*s+o[0];v[j*3+1]=(R[3]*x+R[4]*y+R[5]*z)*s+o[1];v[j*3+2]=(R[6]*x+R[7]*y+R[8]*z)*s+o[2]}
    const ux=v[3]-v[0],uy=v[4]-v[1],uz=v[5]-v[2],wx=v[6]-v[0],wy=v[7]-v[1],wz=v[8]-v[2];let nx=uy*wz-uz*wy,ny=uz*wx-ux*wz,nz=ux*wy-uy*wx;const l=Math.hypot(nx,ny,nz)||1;nx/=l;ny/=l;nz/=l;
    const r=RL[t],col=pal.c[r],sh=SH[t]/100,em=pal.e[r];for(let j=0;j<3;j++)g.d.push(v[j*3],v[j*3+1],v[j*3+2],nx,ny,nz,col[0]*sh,col[1]*sh,col[2]*sh,em)}}
// a mark's glyph as convex polygons, y up (MK_LOGO's SVG paths are y down), cached
const RDS_GLYPH={};
function rdsGlyph(key){if(RDS_GLYPH[key])return RDS_GLYPH[key];const L=MK_LOGO[key],out=[];
  if(L)for(const sp of L.d.split('Z')){const pts=sp.replace(/M/g,' ').trim().split(/\s+/).filter(Boolean).map(t=>t.split(',').map(Number));if(pts.length>=3&&pts.every(p=>p.length===2&&isFinite(p[0])&&isFinite(p[1])))out.push(pts.map(p=>[p[0],-p[1]]))}
  return RDS_GLYPH[key]=out}
// the station's mesh for maker m with labs = up to four grades by socket (0 = empty; a lab draws at grade 2 to 5), cached
function rdsMesh(m,labs,off){if(!rdsReady()||!MAKERS[m])return null;const st=RDS_STYLE(m),T=MDL.i['rds_'+st];if(!T||!T.sk)return null;
  const lg=mkLogoOf(m),L=[0,1,2,3].map(i=>{const v=+((labs&&labs[i])||0);return v>0?Math.max(2,Math.min(5,Math.round(v))):0}),key='rds'+m+lg+mkAcc(m)+L.join('')+(off?'o':'');if(MESH[key])return MESH[key];
  const K=RDS.K,ct=T.c,ht=T.h,pal=rdsPal(m,off),g=new GB();
  // the tower, centred on its own middle
  rdsPart(g,'rds_'+st,pal,[1,0,0,0,1,0,0,0,1],K,[-ct[0]*K,-ct[1]*K,-ct[2]*K]);
  // a lab in each socket in use, the empty-socket marker where the style shows one
  T.sk.forEach((sk,i)=>{const p=T.sub.sock[i],o=[p[0]*ht*K,p[1]*ht*K,p[2]*ht*K],gr=L[i],nm=gr?`rdl_${st}_g${gr}`:(sk[3]?'rdp_'+st:null);if(nm&&mdlHas(nm))rdsPart(g,nm,pal,rdsRot(sk[0],sk[1]),sk[2]*K,o)});
  // the maker's mark, lit in its accent on each board
  const G=rdsGlyph(lg),col=pal.c[5],em=pal.e[5];
  T.lg.forEach((b,i)=>{const R=rdsRot(b[0],b[1]),c=T.sub.logo[i],k=b[2]/2*.78,z=.034,nx=R[2],ny=R[5],nz=R[8];
    const at=(x,y)=>[(R[0]*x*k+R[1]*y*k+R[2]*z+c[0]*ht)*K,(R[3]*x*k+R[4]*y*k+R[5]*z+c[1]*ht)*K,(R[6]*x*k+R[7]*y*k+R[8]*z+c[2]*ht)*K];
    for(const poly of G){const A=at(poly[0][0],poly[0][1]);for(let j=1;j<poly.length-1;j++){const B=at(poly[j][0],poly[j][1]),C=at(poly[j+1][0],poly[j+1][1]);for(const V of[A,B,C])g.d.push(V[0],V[1],V[2],nx,ny,nz,col[0],col[1],col[2],em)}}});
  return MESH[key]=g.upload()}
// the station's points in metres, in its own frame (turn by the entity's q and add its position for the world): each socket
// (where its lab joins, the outward yaw and pitch, the lab's centre c: a sub-system), the control centre cc, the CEO's launch
// bay and the way it faces, the two turret seats, the logo boards, and the radius of the whole station with four labs
const RDS_PTS={};
function rdsPoints(m){const st=RDS_STYLE(m);if(RDS_PTS[st])return RDS_PTS[st];const T=MDL.ready&&MDL.i['rds_'+st];if(!T||!T.sk)return null;const k=T.h*RDS.K,P=p=>[p[0]*k,p[1]*k,p[2]*k];
  return RDS_PTS[st]={sockets:T.sub.sock.map((p,i)=>({p:P(p),yaw:T.sk[i][0],pitch:T.sk[i][1],c:P(T.sub.lab[i])})),cc:P(T.sub.cc[0]),bay:P(T.sub.bay[0]),bayDir:T.bd.slice(),tp:T.tp.map(P),logo:T.sub.logo.map(P),r:T.rr*RDS.K}}
// a point of the station (from rdsPoints) in the world
function rdsAt(e,p,out){out=out||{x:0,y:0,z:0};qRot(e.q||Q_ID,p[0],p[1],p[2],out);out.x+=e.x;out.y+=e.y;out.z+=e.z;return out}
// drawn in the world pass with the works: dimmed when offline, a flash when hit
let rdsErr=0;
function rdsDraw(){if(!W||!W.ents||!rdsReady())return;for(const e of W.ents){if(e.type!=='rds'||!MAKERS[e.m])continue;const P=rdsPoints(e.m);if(!P||!inView(e.x,e.y,e.z,P.r*1.2))continue;const m=rdsMesh(e.m,e.labs,!!e.offline);if(!m)continue;
  mModel(MM,e.x,e.y,e.z,e.q||Q_ID,1,1,1);const hurt=e.lastHit!==undefined&&W.t-e.lastHit<.1;drawMesh(m,MM,e.offline?[.78,.76,.8]:ONE3,hurt?[.3,.22,.14]:ZERO3)}}
{const o=drawWorks;drawWorks=function(t){const r=o.apply(this,arguments);try{rdsDraw()}catch(err){if(!rdsErr++)console.error(err)}return r}}
