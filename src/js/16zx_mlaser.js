//@src 16zx_mlaser.js
// ============================================================ the mining laser, felt (Beyond, 3 Nov 2026)
// The laser cut too slowly to notice (a tonne every six seconds on a Light Miner) and said nothing while it worked. Now it
// cuts about twice as fast, the beam's spot on the ring carries a ring that fills as the next tonne comes free, with the ore's
// name, each tonne that lands in the hold is called out, and the key hint reads "hold: cut the ring" with the laser picked.
// The beam also finds the ring for you: when it strikes the rock off the ring and the nearest point of the ring is within 25
// degrees of your nose (and in range), it swings onto the ring and cuts there. Aiming at the rock is enough; you no longer
// have to hold the nose on the thin band.
LOAD.ml.rate={skiff:.35,prospector:.5,dredger:.65};LOAD.ml.assist=Math.cos(25*Math.PI/180);
{const o=mlBeam;mlBeam=function(e,a){const B=o.apply(this,arguments);try{if(B&&B.on)return B;const n=ringN(a),R=astR(a);qRot(e.q,0,0,1,_f);
  // candidates on the ring: the point nearest the ship, and the point nearest where the beam strikes; the first within the cone wins
  const r=e.st.radius,sx=e.x+_f.x*r,sy=e.y+_f.y*r,sz=e.z+_f.z*r,C=[[sx-a.x,sy-a.y,sz-a.z]];if(B)C.unshift([B.x-a.x,B.y-a.y,B.z-a.z]);
  for(let[px,py,pz]of C){const dn=px*n.x+py*n.y+pz*n.z;px-=dn*n.x;py-=dn*n.y;pz-=dn*n.z;const l=Math.hypot(px,py,pz);if(l<1e-6)continue;
    const qx=a.x+px/l*R,qy=a.y+py/l*R,qz=a.z+pz/l*R,dx=qx-sx,dy=qy-sy,dz=qz-sz,d=Math.hypot(dx,dy,dz);if(d>LOAD.ml.range||(dx*_f.x+dy*_f.y+dz*_f.z)/d<LOAD.ml.assist)continue;
    if(((qx-a.x)*(sx-a.x)+(qy-a.y)*(sy-a.y)+(qz-a.z)*(sz-a.z))<0)continue;
    return{x:qx,y:qy,z:qz,d,on:true,off:0,assist:true}}return B}catch(err){return B}}}
{const o=mlCut;mlCut=function(e,P,a,dt,sec,show){const k0=e.isPlayer?invMass(P.cargo):0,r=o.apply(this,arguments);
  try{if(e.isPlayer&&r==='cut'&&invMass(P.cargo)>k0){const k=mainOre(a)||'';W.mlGot=(W.mlGot||0)+1;if(W.t-(W.mlSaid||-9)>1.2){W.mlSaid=W.t;flash(`+${W.mlGot} t ${k&&ITEMS[k]?ITEMS[k].name:'ore'} · hold ${invMass(P.cargo)} / ${e.st.cargo} t`);W.mlGot=0}}}catch(err){}return r}}
{const o=blDraw;blDraw=function(c){o.apply(this,arguments);try{if(!loadOn())return;const p=W.player,P=S.player;if(!p||mtoolOf(P)!=='mlaser'||!p.mining||p.mining.ore===undefined)return;const a=p.mining,B=mlBeam(p,a);if(!B||!B.on)return;
  const L=proj(B.x,B.y,B.z);if(L.behind)return;const f=(p.mlAcc||0)%1,k=mainOre(a);c.save();c.lineWidth=3;c.strokeStyle='rgba(122,217,167,.25)';c.beginPath();c.arc(L.x,L.y,13,0,TAU);c.stroke();
  c.strokeStyle='#7ad9a7';c.beginPath();c.arc(L.x,L.y,13,-Math.PI/2,-Math.PI/2+TAU*f);c.stroke();c.font='700 11px "Saira Semi Condensed",sans-serif';c.textAlign='left';c.lineWidth=3;c.strokeStyle='rgba(4,8,16,.85)';
  const lab=`CUTTING ${k&&ITEMS[k]?ITEMS[k].name.toUpperCase():'ORE'} · ${oreTotal(a)} t LEFT`;c.strokeText(lab,L.x+20,L.y+4);c.fillStyle='#7ad9a7';c.fillText(lab,L.x+20,L.y+4);c.restore()}catch(e){}}}
{const o=keysNow;keysNow=function(){const k=o.apply(this,arguments);try{if(mtoolOf(S.player)==='mlaser')for(const x of k)if(x[1]==='charge')x[1]='hold: cut the ring'}catch(e){}return k}}
// the rock's target panel tells you how to work it with the tool you have picked
{const o=hudUpdate;hudUpdate=function(){const r=o.apply(this,arguments);try{if(W&&W.tgt&&W.tgt.kind==='ast'&&loadOn()&&mtoolOf(S.player)==='mlaser'){for(const d of $('hTgt').querySelectorAll('.ts'))if(/^Fire charges/.test(d.textContent)){const a=W.tgt.ref;
  d.textContent=ringOK(a)?`Mining laser: hold ${kb('mine')} with the rock ahead (within ${LOAD.ml.range} m). The beam finds its ring and cuts ore into your hold, slow and safe. ${kb('mtool')} switches to charges.`:`Its ring is broken (a blast cracked it): the laser can't cut it. Switch to charges (${kb('mtool')}) or find another rock.`}}}catch(e){}return r}}
