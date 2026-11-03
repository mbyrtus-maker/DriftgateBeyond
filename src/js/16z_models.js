//@src 16z_models.js
// ============================================================ every approved Beyond design in the game (2 Nov 2026)
// The rest of the approved models, packed as dz_* (ships) and by_* (structures) by tools/build_models.py: each power's scouts,
// bombers, constructors, drones, escorts and carriers; the house-brand hulls and the Wraith; the Unbound hulls; the powers'
// stations and depots, the freeport, Scrapheart Haven and the Riftstone rock. Models only: classes keep their stats.
// Escorts and carriers bring their own turret mounts, sub-target points and (carriers) deck spots from the models.
const FAC_MDL={halcyon:{scout:'dz_lark',scout2:'dz_skylark',bomber:'dz_condor',gunboat:'dz_harrier',constructor:'dz_architect',drone:'dz_aegis',escort:'dz_shrike',carrier:'dz_sovereign'},
  varkesh:{scout:'dz_jackal',scout2:'dz_wolfhound',bomber:'dz_maul',gunboat:'dz_warhound',constructor:'dz_foundry',drone:'dz_ward',escort:'dz_vanguard',carrier:'dz_bastille'},
  ostrova:{scout:'dz_seer',scout2:'dz_oracle',bomber:'dz_obelisk',gunboat:'dz_sentinel',constructor:'dz_loom',drone:'dz_halo',escort:'dz_lantern',carrier:'dz_cathedral'},
  pirate:{raider:'dz_raider',corsair:'dz_corsair',plunderer:'dz_plunderer',uskiff:'dz_skiff',interceptor:'dz_raider',striker:'dz_corsair',heavy:'dz_plunderer',scout:'dz_skiff'}};
const BRAND_MDL={gannet:'dz_gannet',bombard:'dz_bombard',vesper:'dz_vesper',wraith:'dz_wraith'};
// a faction's escort and carrier are also called by those names in its hull list; its destroyer by its approved name
for(const f of FAC_IDS){const H=FACTIONS[f].hulls;if(DST&&DST.dname[f])H.frigate=DST.dname[f]}
function fmdl(fac,cls){if(BRAND_MDL[cls])return BRAND_MDL[cls];const m=FAC_MDL[fac]&&FAC_MDL[fac][cls];return m&&mdlHas(m)?m:null}
// the player's own ships take their design line's look (P.faction); a 'player' side resolves the same way
function fmFac(fac){return fac==='player'&&S&&S.player?S.player.faction:fac}
{const o=shipMesh;shipMesh=function(fac,cls){const F=fmFac(fac),m=fmdl(F,cls);if(m&&mdlHas(m)){const key='fz'+F+cls;if(MESH[key])return MESH[key];const L=new GB();L.seg([0,0,0],[0,0,0],[0,0,0]);
  return MESH[key]={hull:mdlMesh(m,F==='wraith'?'wraith':F,1),rim:L.upload(true),eng:engFix(m).map(e=>e.slice()),mdl:true}}return o.apply(this,arguments)}}
// escorts and carriers: turrets on the model's mounts, sub-targets on its parts, berths and deck spots from its geometry
function capM(E){if(!E||E.side==='brood'||E.side==='pirate')return null;const t=E.tok;if(!t||!(isEsc(t)||isCar(t)))return null;const m=fmdl(fmFac(E.fac),E.cls);return m&&MDL.ready&&MDL.i[m]?m:null}
{const o=mdlFrigTurrets;mdlFrigTurrets=function(e){const m=e&&!e._mt&&e.turrets&&capM(e);if(m){const M=MDL.i[m];if(M.tp&&M.tp.length){e._mt=1;const k=1.25/1.1;e.turrets.forEach((tu,i)=>{const p=M.tp[i%M.tp.length];tu.p=[p[0]*k,p[1]*k,p[2]*k]});return}}return o.apply(this,arguments)}}
{const o=subLocal;subLocal=function(E){const m=E&&E.type==='ship'&&capM(E);if(!m)return o.apply(this,arguments);if(E._subL&&E._subL.ok===MDL.ready)return E._subL.a;const P=Object.create(E);P.cls=m;delete P._subL;const a=o.call(this,P);E._subL={ok:MDL.ready,a};return a}}
{const o=capMdlKey;capMdlKey=function(F){const m=capM(F)||(F&&isDst(F.tok)&&F.side!=='brood'&&dstMdl(fmFac(F.fac),'frigate'));return m&&MDL.ready&&MDL.i[m]?m:o.apply(this,arguments)}}
// a carrier takes ships down onto its own deck spots
function capDeck(F){const m=capM(F);const M=m&&isCar(F.tok)&&MDL.i[m];return M&&M.pt&&M.pt.length>=4?M.pt:null}
{const o=carBay;carBay=function(F){return!!capDeck(F)||o.apply(this,arguments)}}
{const o=berthPose;berthPose=function(F,i,cls,out){const pt=capDeck(F);if(!pt)return o.apply(this,arguments);const k=F.st.radius*1.25,sc=(CLASSES[cls]||CLASSES.interceptor).radius*1.25,b=pt[i&3];
  qRot(F.q,b[0]*k,b[1]*k+sc*.32,b[2]*k,_bv1);out.x=F.x+_bv1.x;out.y=F.y+_bv1.y;out.z=F.z+_bv1.z;qCopy(out.q,F.q);qRot(F.q,0,1,0,_bv1);out.nx=_bv1.x;out.ny=_bv1.y;out.nz=_bv1.z;out.bay=0;return out}}
// ---- the powers' stations and depots, the freeport, Scrapheart Haven
const ST_MDL={size:{core:170,free:210,haven:240,depot:105,fdepot:80}};
// the three freeports share one design, each with its own touches (3 Nov 2026): Coldwater Drift and Ember Wake have their own models
const FP_MDL={cw:'by_freeport_cw',ew:'by_freeport_ew'};
function stMdlName(fac,kind,sid){if(kind==='haven')return'by_haven';if(kind==='free')return FP_MDL[sid]&&MDL.i&&MDL.i[FP_MDL[sid]]?FP_MDL[sid]:'by_freeport';if(FAC_IDS.includes(fac)){if(kind==='core')return'by_st_'+fac;if(kind==='depot'||kind==='fdepot')return'by_dp_'+fac}return null}
function stMesh(name,fac,size){const key='stz'+name+fac+size;if(MESH[key])return MESH[key];const M=MDL.i[name],s=size/(M.h||1),c=M.c||[0,0,0],g=new GB();bmPart(g,name,fac,0,s,-c[0]*s,-c[1]*s,-c[2]*s);return MESH[key]={core:g.upload(),spin:bmSpin(),s}}
{const o=stationMesh;stationMesh=function(fac,kind){const SE=W&&W.stationEnt,R=SE&&SE.rec,k=R&&R.fwd?'fdepot':kind,nm=MDL.ready&&stMdlName(fac,kind,R&&R.sid);if(nm&&MDL.i[nm])return stMesh(nm,fac==='pirate'?'pirate':fac,ST_MDL.size[k]||150);return o.apply(this,arguments)}}
// turrets set onto the model's own surface: for each, the outermost hull point in its direction (found once per model)
function stSurf(name,size,n){const key=name+':'+size+':'+n;stSurf.c=stSurf.c||{};if(stSurf.c[key])return stSurf.c[key];const M=MDL.i[name],P=new Int16Array(MDL.b,M.o,M.n*9),h=(M.h||1)/32767,s=size/(M.h||1),out=[];
  for(let i=0;i<n;i++){const a=i/n*TAU+.4,dx=Math.cos(a),dy=i%2?.55:-.25,dz=Math.sin(a),l=Math.hypot(dx,dy,dz);let best=null,bd=-1e9;
    for(let t=0;t<M.n;t++){const o=t*9;const x=(P[o]+P[o+3]+P[o+6])/3*h,y=(P[o+1]+P[o+4]+P[o+7])/3*h,z=(P[o+2]+P[o+5]+P[o+8])/3*h;const d=(x*dx+y*dy+z*dz)/l;if(d>bd){bd=d;best=[x,y,z]}}
    out.push(best.map(v=>v*s))}return stSurf.c[key]=out}
{const o=mdlStationTurrets;mdlStationTurrets=function(SE){const R=SE&&SE.rec,nm=SE&&!SE._mt&&MDL.ready&&!bmOwned(R)&&stMdlName(SE.fac,SE.kind,R&&R.sid);if(nm&&MDL.i[nm]){SE._mt=1;devEnt(SE);const k=R&&R.fwd?'fdepot':SE.kind,T=stSurf(nm,ST_MDL.size[k]||150,Math.max(1,SE.turrets.filter(t=>!t.mod).length));
  SE.turrets.filter(t=>!t.mod).forEach((tu,i)=>{tu.p=T[i%T.length].slice()});return}return o.apply(this,arguments)}}
// ---- the Riftstone rock: dark, jagged, split by glowing pink rifts
const RIFT_PAL=(()=>{const F=hexRGB('#ff4fc8');return{c:[[.3,.28,.3],[.2,.19,.21],[.09,.08,.1],F,[.16,.1,.16],F,mixC(F,[1,1,1],.55),[.24,.22,.25],[.13,.12,.14]],e:[0,0,0,.3,.2,.95,.8,0,0]}})();
function riftMesh(){if(MESH.riftz)return MESH.riftz;if(!mdlHas('by_rift'))return null;const M=MDL.i.by_rift,g=new GB();mdlTris('by_rift','neutral',1,g,RIFT_PAL);return MESH.riftz=g.upload()}
{const o=portName;portName=function(E){if(E&&E.type==='station'&&MDL.ready&&!bmOwned(E.rec)){const nm=stMdlName(E.fac,E.kind,E.rec&&E.rec.sid);if(nm&&MDL.i[nm]&&!(E.rec&&E.rec.fwd))return nm}return o.apply(this,arguments)}}
