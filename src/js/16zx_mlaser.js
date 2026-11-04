//@src 16zx_mlaser.js
// ============================================================ the mining laser, felt (Beyond, 3 Nov 2026)
// The laser cut too slowly to notice (a tonne every six seconds on a Light Miner) and said nothing while it worked. Now it
// cuts about twice as fast, the beam's spot on the ring carries a ring that fills as the next tonne comes free, with the ore's
// name, each tonne that lands in the hold is called out, and the key hint reads "hold: cut the ring" with the laser picked.
// Held right on the ring yourself, the laser cuts twice as fast ("ON THE RING · ×2"); swung there by the beam, at the base rate.
// The beam also finds the ring for you: when it strikes the rock off the ring and the nearest point of the ring is within 45
// degrees of your nose (and in range, on your side of the rock or just over its rim), it swings onto the ring and cuts there. Aiming at the rock is enough; you no longer
// have to hold the nose on the thin band.
LOAD.ml.rate={skiff:.35,prospector:.5,dredger:.65};
// held right on the ring yourself (not swung there by the beam), the laser cuts twice as fast
const ML={ringK:2};let mlK=1;
{const o=mlRate;mlRate=function(P){return o.apply(this,arguments)*mlK}}
{const o=mlCut;mlCut=function(e,P,a,dt,sec,show){let B=null;try{B=mlBeam(e,a)}catch(err){}mlK=B&&B.on&&!B.assist?ML.ringK:1;try{return o.apply(this,arguments)}finally{mlK=1}}}LOAD.ml.assist=Math.cos(45*Math.PI/180);
{const o=mlBeam;mlBeam=function(e,a){const B=o.apply(this,arguments);try{if(B&&B.on)return B;const n=ringN(a),R=astR(a);qRot(e.q,0,0,1,_f);
  // candidates on the ring: the point nearest the ship, and the point nearest where the beam strikes; the first within the cone wins
  const r=e.st.radius,sx=e.x+_f.x*r,sy=e.y+_f.y*r,sz=e.z+_f.z*r,C=[[sx-a.x,sy-a.y,sz-a.z]];if(B)C.unshift([B.x-a.x,B.y-a.y,B.z-a.z]);
  for(let[px,py,pz]of C){const dn=px*n.x+py*n.y+pz*n.z;px-=dn*n.x;py-=dn*n.y;pz-=dn*n.z;const l=Math.hypot(px,py,pz);if(l<1e-6)continue;
    const qx=a.x+px/l*R,qy=a.y+py/l*R,qz=a.z+pz/l*R,dx=qx-sx,dy=qy-sy,dz=qz-sz,d=Math.hypot(dx,dy,dz);if(d>LOAD.ml.range||(dx*_f.x+dy*_f.y+dz*_f.z)/d<LOAD.ml.assist)continue;
    if(((qx-a.x)*(sx-a.x)+(qy-a.y)*(sy-a.y)+(qz-a.z)*(sz-a.z))<-.3*R*Math.hypot(sx-a.x,sy-a.y,sz-a.z))continue;
    return{x:qx,y:qy,z:qz,d,on:true,off:0,assist:true}}return B}catch(err){return B}}}
{const o=mlCut;mlCut=function(e,P,a,dt,sec,show){const k0=e.isPlayer?invMass(P.cargo):0,r=o.apply(this,arguments);
  try{if(e.isPlayer&&r==='cut'&&invMass(P.cargo)>k0){const k=mainOre(a)||'';W.mlGot=(W.mlGot||0)+1;if(W.t-(W.mlSaid||-9)>1.2){W.mlSaid=W.t;flash(`+${W.mlGot} t ${k&&ITEMS[k]?ITEMS[k].name:'ore'} · hold ${invMass(P.cargo)} / ${e.st.cargo} t`);W.mlGot=0}}}catch(err){}return r}}
{const o=blDraw;blDraw=function(c){o.apply(this,arguments);try{if(!loadOn())return;const p=W.player,P=S.player;if(!p||mtoolOf(P)!=='mlaser'||!p.mlRock||!p.blHeld)return;const a=p.mlRock,B=mlBeam(p,a);if(!B||!B.on)return;
  const L=proj(B.x,B.y,B.z);if(L.behind)return;const f=(p.mlAcc||0)%1,k=mainOre(a);c.save();c.lineWidth=3;c.strokeStyle='rgba(122,217,167,.25)';c.beginPath();c.arc(L.x,L.y,13,0,TAU);c.stroke();
  c.strokeStyle='#7ad9a7';c.beginPath();c.arc(L.x,L.y,13,-Math.PI/2,-Math.PI/2+TAU*f);c.stroke();c.font='700 11px "Saira Semi Condensed",sans-serif';c.textAlign='left';c.lineWidth=3;c.strokeStyle='rgba(4,8,16,.85)';
  const lab=`${B.assist?'CUTTING':'ON THE RING · ×'+ML.ringK} ${k&&ITEMS[k]?ITEMS[k].name.toUpperCase():'ORE'} · ${oreTotal(a)} t LEFT`;c.strokeText(lab,L.x+20,L.y+4);c.fillStyle='#7ad9a7';c.fillText(lab,L.x+20,L.y+4);c.restore()}catch(e){}}}
{const o=keysNow;keysNow=function(){const k=o.apply(this,arguments);try{if(mtoolOf(S.player)==='mlaser')for(const x of k)if(x[1]==='charge')x[1]='hold: cut the ring'}catch(e){}return k}}
// the rock's target panel tells you how to work it with the tool you have picked
{const o=hudUpdate;hudUpdate=function(){const r=o.apply(this,arguments);try{if(W&&W.tgt&&W.tgt.kind==='ast'&&loadOn()&&mtoolOf(S.player)==='mlaser'){for(const d of $('hTgt').querySelectorAll('.ts'))if(/^Fire charges/.test(d.textContent)){const a=W.tgt.ref;
  d.textContent=ringOK(a)?`Mining laser: hold ${kb('mine')} with the rock ahead (within ${LOAD.ml.range} m). The beam finds its ring and cuts ore into your hold, slow and safe. ${kb('mtool')} switches to charges.`:`Its ring is broken (a blast cracked it): the laser can't cut it. Switch to charges (${kb('mtool')}) or find another rock.`}}}catch(e){}return r}}
// ---- a new mining hull comes with its tools (user, 3 Nov 2026): taking a mining hull at a shipyard used to carry your old
// weapons across into its slots (a Light Fighter's guns in a Light Miner), so it arrived without a mining laser. Now any
// standard mining tool the hull is designed for (the mining laser and charge launcher) that isn't fitted is fitted for you:
// your own from the hold or vault first (any maker's), otherwise the shipyard builds a standard one from the station's own
// stores (goods only move, so the ledger stays exact). The part it displaces goes to your vault as before.
function mlTools(c,P){if(!P||S.unb||!loadOn()||!blHull(P.cls))return'';const F=fitOf(P),D=slotsOf(P.cls,designOf(P.faction,P.cls)?P.faction:null),st=c.storage||P.vault,R=S.stations[P.sector];
  let mk=null;try{mk=R?(R.owner==='player'?R.stock:mkStock(R)):null}catch(e){}const out=[];
  D.w.forEach((k,i)=>{if(k!=='mlaser'&&k!=='charge')return;if(F.w.includes(k))return;
    let id=partItems(k).find(x=>countIn(x,[P.cargo,st])>0);
    if(!id&&mk&&haveIn(PART_RC[k],[mk])){takeFrom(PART_RC[k],[mk]);inv.add(P.cargo,PART[k],1);id=PART[k]}
    if(!id)return;const was=F.w[i];const m=fitDo(c,P,`w:${i}:${id}`);if(F.w[i]===k)out.push(`${ITEMS[id].name}${was&&was!==k?` (your ${(WPN[was]||{}).name||was} went to your ${c.storage&&c.storage!==P.vault?(c.storageName||'store'):'vault'})`:''}`);else if(m)out.push(m)});
  if(!out.length)return'';try{refreshPlayerStats()}catch(e){}if(F.w.includes('mlaser'))P.mtool='mlaser';return` Fitted for mining: ${out.join(', ')}.`}
// and its drone bay comes full: drones from your hold or vault first, otherwise the shipyard builds them from the station's
// stores (freeports sell none, so a Light Miner taken there used to launch with an empty bay)
function hullDrones(c,P){const cap=(CLASSES[P.cls]&&CLASSES[P.cls].drones)||0;P.bay=P.bay||{};let need=cap-(P.bay.drone||0);if(need<=0)return'';const st=c.storage||P.vault,R=S.stations[P.sector];
  let mk=null;try{mk=R?(R.owner==='player'?R.stock:mkStock(R)):null}catch(e){}let n=0;
  for(const h of[P.cargo,st]){if(need<=0)break;const k=inv.take(h,'drone',need);n+=k;need-=k}
  const rc=ITEMS.drone.recipe;while(need>0&&mk&&haveIn(rc,[mk])){takeFrom(rc,[mk]);n++;need--}
  if(!n)return'';inv.add(P.bay,'drone',n);return` Drone bay ${P.bay.drone}/${cap}.`}
// empty slots on a new hull take your own parts of the hull's standard kinds back from the hold or vault (switching a Light
// Miner back to a Light Fighter used to leave it with no guns, the guns sitting in the vault)
function hullRefit(c,P){if(!P||S.unb||!loadOn())return'';const F=fitOf(P),D=slotsOf(P.cls,designOf(P.faction,P.cls)?P.faction:null),st=c.storage||P.vault,out=[];
  for(const g of['w','u'])(D[g]||[]).forEach((k,i)=>{const A=g==='w'?F.w:F.u;if(!k||A[i])return;const id=partItems(k).find(x=>countIn(x,[P.cargo,st])>0);if(!id)return;fitDo(c,P,`${g}:${i}:${id}`);if(A[i]===k)out.push(ITEMS[id].name)});
  if(!out.length)return'';try{refreshPlayerStats()}catch(e){}return` Refitted from your vault: ${out.join(', ')}.`}
{const o=dockAction;dockAction=function(act,arg){const r=o.apply(this,arguments);if(act==='hull'&&String(dockErr||'').startsWith('✓')){try{const t=mlTools(dockCtx(),S.player)+hullRefit(dockCtx(),S.player)+hullDrones(dockCtx(),S.player);if(t){dockErr=dockErr.replace(/ ?Drone bay \d+\/\d+ \(the station is out of drones[^)]*\)\.?/,'')+t}}catch(e){console.error(e)}}return r}}
// ---- easier to use (user, 3 Nov 2026: "no sound and does not target properly"): holding F with the laser and no rock
// targeted targets the rock ahead for you (the nearest whose surface is in range and within 35 degrees of your nose); the
// beam's hum and crackle play while it cuts (07_audio keys on p.mlSnd, stamped each frame the beam is on a rock).
function mlAutoTgt(p){const sec=S.sectors[W.sid];if(!sec)return null;qRot(p.q,0,0,1,_f);let best=null,bs=1e9;
  for(const a of sec.ast){if(!ringOK(a))continue;const dx=a.x-p.x,dy=a.y-p.y,dz=a.z-p.z,d=Math.hypot(dx,dy,dz)||1,R=astR(a);if(d-R>LOAD.ml.range)continue;const c=(dx*_f.x+dy*_f.y+dz*_f.z)/d;if(c<Math.cos(35*Math.PI/180)&&d>R)continue;const sc=d*(2-c);if(sc<bs){bs=sc;best=a}}
  return best}
{const o=blPilotUpdate;blPilotUpdate=function(p,P,st,sec,dt){try{if(loadOn()&&blHull(P.cls)&&mtoolOf(P)==='mlaser'&&(keys.KeyF||mouse.r||touch.mine)&&!(W.tgt&&W.tgt.kind==='ast'&&validTgt(W.tgt))&&!blCloudNear(p,sec)){const a=mlAutoTgt(p);if(a){W.tgt={kind:'ast',ref:a};flash('Mining laser: targeted the rock ahead.')}}}catch(e){}
  const r=o.apply(this,arguments);try{if(p.mlRock&&p.blHeld&&p.mlSay0!=='aim')p.mlSnd=W.t}catch(e){}return r}}
{const o=mlSay;mlSay=function(e,P,r){if(e)e.mlSay0=r;return o.apply(this,arguments)}}
