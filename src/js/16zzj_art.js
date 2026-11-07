//@src 16zzj_art.js
// ============================================================ the rest of the approved art (Beyond, 5 Nov 2026)
// The user's ask: push all approved art. What still drew as Driftgate 1's, and is now the approved Beyond look:
//  - Constructors (Architect, Foundry, Loom). They were mapped since 2 Nov but never drew: the class is called "constructor",
//    and looking that name up in a plain object finds every object's own constructor function, so the old model won.
//  - The Unbound fly only their six designs (decided 2 Nov): every class they fly now draws as one of the Raider, Skiff,
//    Corsair, Plunderer, Wrecker (their Wrecker, the bomber, flies at last) or Ravager.
//  - The shared assault ship (approved 2 Nov; Driftgate 1 never drew one): when a capital lands marines on a base in a system
//    someone is watching, its assault ships fly from the capital to the base, set down, and the survivors fly back; the ones
//    the abstract roll shot down blow up on the run in. A picture of what the rules already decided: nothing here changes them.
//    Guests in that system see the same flights (the host sends them).
const hasOwnK=(o,k)=>!!o&&Object.prototype.hasOwnProperty.call(o,k);
fmdl=function(fac,cls){if(hasOwnK(BRAND_MDL,cls))return BRAND_MDL[cls];const m=hasOwnK(FAC_MDL[fac],cls)?FAC_MDL[fac][cls]:null;return m&&mdlHas(m)?m:null};
Object.assign(FAC_MDL.pirate,{bomber:'dz_wrecker',gunboat:'dz_wrecker',constructor:'dz_wrecker',scout2:'dz_skiff',courier:'dz_skiff',skiff:'dz_skiff',prospector:'dz_skiff',dredger:'dz_plunderer',freighter:'dz_plunderer',bulker:'dz_plunderer',
  drone:'dz_raider',frigate:'dz_ravager'});
// (7 Nov 2026) and their Junk Drone (a Raider, small) and their Destroyer (the Ravager, their capital hull): both drew as
// Driftgate 1's hulls
// ---- assault ships in flight
const ASF={r:17,spd:170,hold:4,stag:.7,max:12};
function asMesh(fac){const f=fmFac(fac),k='asl'+f;return MESH[k]||(MESH[k]=mdlMesh('dz_assault',FACTIONS[f]||f==='pirate'?f:'neutral',1))}
function asFly(t,sid,ok){const w=WORLDS[sid];if(!w||!mdlHas('dz_assault'))return;inW(w,()=>{const tg=W.stationEnt&&W.stationEnt.rec&&W.stationEnt.rec.sid===sid?W.stationEnt:W.outpostEnt;if(!tg)return;
  W.asl=W.asl||[];if(W.asl.length>=ASF.max)return;const E=W.ents.find(x=>x.alive&&x.tok===t);let a;
  if(E)a={x:E.x,y:E.y,z:E.z};else{const gt=W.ents.find(x=>x.type==='gate'&&x.to===t.sector)||W.ents.find(x=>x.type==='gate');const d=rdir();a=gt?{x:gt.x,y:gt.y,z:gt.z}:{x:tg.x+d.x*5000,y:tg.y+d.y*800,z:tg.z+d.z*5000}}
  const d=rdir(),R=((tg.st&&tg.st.radius)||tg.r||150)*.95,b={x:tg.x+d.x*R,y:tg.y+Math.abs(d.y)*R*.4,z:tg.z+d.z*R},dur=clamp(hyp(b.x-a.x,b.y-a.y,b.z-a.z)/ASF.spd,5,30);
  const n=W.asl.filter(x=>x.t0>W.t-1).length,S1={a,b,t0:W.t+n*ASF.stag,dur,die:!ok,dieAt:rnd(.45,.85),fac:t.side,q:q0()};W.asl.push(S1);
  // guests in that system see them too
  if(NET.host)for(const c of readyCl()){const P=S.pilots[c.pid];if(P&&P.sector===sid)send(c.L,{t:'asl',sid,a,b,d:S1.t0-W.t,dur,die:S1.die,dieAt:S1.dieAt,fac:t.side})}})}
{const o=clientRecv;clientRecv=function(m){if(m&&m.t==='asl'){try{if(W&&W.sid===m.sid){W.asl=W.asl||[];if(W.asl.length<ASF.max)W.asl.push({a:m.a,b:m.b,t0:W.t+(m.d||0),dur:m.dur,die:m.die,dieAt:m.dieAt,fac:m.fac,q:q0()})}}catch(e){}return}return o.apply(this,arguments)}}
{const o=aSend;aSend=function(t,sid){const r=o.apply(this,arguments);try{asFly(t,sid,!!r)}catch(e){console.error(e)}return r}}
function asPos(s,t,out){const k=t-s.t0;let u,from=s.a,to=s.b,dir=1;if(k<s.dur){u=k/s.dur}else if(k<s.dur+ASF.hold){u=1}else{u=(k-s.dur-ASF.hold)/s.dur;from=s.b;to=s.a;dir=-1}
  const e=u*u*(3-2*u);out.x=from.x+(to.x-from.x)*e;out.y=from.y+(to.y-from.y)*e+Math.sin(Math.PI*u)*120*dir;out.z=from.z+(to.z-from.z)*e;out.vx=to.x-from.x;out.vy=to.y-from.y;out.vz=to.z-from.z;return out}
const _asp={};
{const o=drawWorks;drawWorks=function(t){const r=o.apply(this,arguments);try{if(!W||!W.asl||!W.asl.length)return r;const now=W.t;
  W.asl=W.asl.filter(s=>{const k=now-s.t0;if(k<0)return true;if(s.die&&k>=s.dur*s.dieAt){asPos(s,s.t0+s.dur*s.dieAt,_asp);if(W===LW)fxBoom(_asp,40,sideCol(s.fac));return false}return k<s.dur*2+ASF.hold});
  for(const s of W.asl){if(now<s.t0)continue;asPos(s,now,_asp);if(!inView(_asp.x,_asp.y,_asp.z,ASF.r*2))continue;if(hyp(_asp.vx,_asp.vy,_asp.vz)>1)qLook(_asp.vx,_asp.vy,_asp.vz,0,1,0,s.q);
    mModel(MM,_asp.x,_asp.y,_asp.z,s.q,ASF.r,ASF.r,ASF.r);drawMesh(asMesh(s.fac),MM)}}catch(e){console.error(e)}return r}}
