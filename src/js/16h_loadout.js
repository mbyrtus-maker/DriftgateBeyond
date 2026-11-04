//@src 16h_loadout.js
// ============================================================ weapon and utility slots (Beyond stage 3)
// A pilot's ship is a hull with slots: weapon slots (machine gun, laser, missile launcher, torpedo launcher on bombers; mining
// laser and charge launcher on mining hulls only) and utility slots (landing kit, cargo module, scanner). Each weapon is limited
// differently: the machine gun by ammunition, the laser by reactor energy, launchers by payload. Payload (rounds, missiles,
// torpedoes, charges) is never reloaded in flight: docking rearms it, paid to the station owner's treasury.
//   P.fit  {cls, w: [weapon per slot or ''], g: [its grade], u: [utility per slot or ''], ug: [its grade]}
//   A pilot starts with the hull's default fit; after that parts are real items (stage 4): built from components, bought, moved
//   between hold, vault and slots, and upgraded through grades 1-5 in place. Moving to another hull moves the fitted parts across.
//   P.ammo  machine-gun rounds aboard;  P.mtool  the mining tool F uses ('charge' or 'mlaser')
// Training and the Unbound mode keep Driftgate 1's weapons (every gun and laser, launchers reloading in flight, landing for all).
const WPN={gun:{name:'Machine gun',desc:'Kinetic: lead your shots; strong against hull. Uses ammunition.'},
  laser:{name:'Laser',desc:'Hits instantly; strong against shields. Drains the reactor fast.'},
  missile:{name:'Missile launcher',desc:'Seeking missiles from a magazine, rearmed at a dock. Each hits twice as hard as before.'},
  torpedo:{name:'Torpedo launcher',desc:'The siege weapon: bombers only. Rearmed at a dock.'},
  mlaser:{name:'Mining laser',desc:'Mining hulls only. Hold the beam on a rock\'s ring to cut ore steadily. Draws on the reactor.'},
  charge:{name:'Charge launcher',desc:'Mining hulls only. Blast charges at fault points for a big, fast yield. Charges are payload.'}};
const UTIL={land:{name:'Landing kit',desc:'Land on a rock (E): systems down, off enemy sensors beyond close range.'},
  cargo:{name:'Cargo module',desc:'+20% hold.'},
  scanner:{name:'Scanner',desc:'Rock scans reach every rock within 1.5 km and last longer.'}};
// slot counts and the fit a new hull comes with (the design's starting proposal; they will vary by power's design in stage 6)
const HULL_SLOTS={interceptor:{w:['gun','laser','missile'],u:['land']},striker:{w:['gun','laser','missile','gun'],u:['land']},
  heavy:{w:['gun','gun','laser','missile','missile'],u:['land','scanner']},bomber:{w:['torpedo','gun','laser'],u:['land']},gunboat:{w:['torpedo','gun','gun','laser'],u:['land','cargo']},
  skiff:{w:['charge','gun'],u:['land']},prospector:{w:['charge','mlaser','gun'],u:['land']},dredger:{w:['charge','mlaser','gun'],u:['land','cargo']},
  courier:{w:['gun'],u:['cargo','land']},freighter:{w:['gun','laser'],u:['cargo','land']},bulker:{w:['gun','laser'],u:['cargo','cargo']},
  scout:{w:['laser','missile'],u:['land','scanner']},scout2:{w:['gun','laser','missile'],u:['land','scanner']},constructor:{w:['gun'],u:['cargo']},
  wraith:{w:['gun','gun','laser','laser'],u:['land']},raider:{w:['gun','laser','missile'],u:['land']},corsair:{w:['gun','laser','missile','gun'],u:['land']},
  plunderer:{w:['gun','gun','laser','missile','missile'],u:['land','cargo']},uskiff:{w:['laser','missile'],u:['land','scanner']}};
// ammo: rounds per machine gun; prices per round, missile, torpedo and charge; mslK: a pilot's missile damage multiplier;
// dupK: damage added by each extra gun or laser of the same kind; gunE: share of a gun shot's energy refunded (ammunition is its limit)
const LOAD={ammo:600,ammoCr:.15,mslCr:25,torpCr:90,chgCr:6,mslK:2,dupK:.2,gunE:.7,cargoK:.2,scanR:1500,scanT:40,
  ml:{range:380,band:.15,e:8,rate:{skiff:.17,prospector:.25,dredger:.33}}};
function loadOn(){return!!S&&!S.training&&!S.unb}
function slotsOf(cls,fac){const b=HULL_SLOTS[cls]||{w:['gun','laser'],u:['land']},d=fac&&typeof designOf==='function'?designOf(fac,cls):null;return d&&(d.w||d.u)?{w:d.w||b.w,u:d.u||b.u}:b}
function isTorpHull(cls){return!!(CLASSES[cls]||{}).torp}
// which weapons a slot of this hull takes: mining tools on mining hulls only, torpedoes on bombers only (their launcher is the
// first slot and stays a torpedo launcher), missiles on every other hull
function wpnOK(cls,k,i){if(!WPN[k])return false;if(isTorpHull(cls)){if(i===0)return k==='torpedo';return k==='gun'||k==='laser'}
  if(k==='torpedo')return false;if(k==='mlaser'||k==='charge')return!!blHull(cls);return true}
const FIT_T=new WeakMap();
// ---- parts as items (stage 4): each part is built from components; an upgrade to the next grade feeds in the grade's components
const PART={gun:'pt_gun',laser:'pt_laser',missile:'pt_msl',torpedo:'pt_torp',mlaser:'pt_mlaser',charge:'pt_charge',land:'pt_land',cargo:'pt_cargo',scanner:'pt_scan'};
const PART_RC={gun:{plate:2,wire:1},laser:{wire:2,coil:1},missile:{plate:2,wire:2},torpedo:{plate:3,coil:1},mlaser:{plate:1,wire:1,coil:1},charge:{plate:1,wire:2},land:{plate:2},cargo:{plate:4},scanner:{wire:1,coil:1}};
const PART_COL={gun:'#e8b070',laser:'#a5deff',missile:'#ff8f6b',torpedo:'#ffcf5a',mlaser:'#7ad9a7',charge:'#f0b24a',land:'#bba98d',cargo:'#d6ccb4',scanner:'#c99cff'};
for(const k in PART){ITEMS[PART[k]]={name:(WPN[k]||UTIL[k]).name,recipe:PART_RC[k],col:PART_COL[k],part:k};ITEM_ORDER.push(PART[k]);CRAFTABLE.push(PART[k])}
// what each grade above 1 adds: damage for guns and lasers, rounds, a missile or charge per launcher, mining-laser rate,
// cargo-module hold and scanner reach. Landing kits have one grade.
const PG={dmg:.1,ammo:.25,ml:.15,cargo:.05,scan:.2};
function partUpg(t){const r={...UPG[t]};if(t>=3)r.matrix=1;return r}
function partToStore(st,k,g,it){inv.add(st,it||PART[k],1);for(let t=2;t<=(g||1);t++)inv.addAll(st,partUpg(t))}
function fitItems(F){const o={};if(!F||!Array.isArray(F.w))return o;const add=(k,g,it)=>{if(!k||!(PART[k]||(it&&ITEMS[it])))return;inv.add(o,it||PART[k],1);for(let t=2;t<=(g||1);t++)inv.addAll(o,partUpg(t))};
  F.w.forEach((k,i)=>add(k,F.g&&F.g[i],F.wi&&F.wi[i]));(F.u||[]).forEach((k,i)=>add(k,F.ug&&F.ug[i],F.ui&&F.ui[i]));return o}
// the fit a pilot is created with; afterwards parts only move, so the ledger stays exact
function fitNew(cls,fac){const D=slotsOf(cls,fac);return{cls,d:fac||null,w:D.w.slice(),u:D.u.slice(),g:D.w.map(()=>1),ug:D.u.map(()=>1),wi:D.w.map(()=>null),ui:D.u.map(()=>null)}}
function fitOf(P){if(!P)return{w:[],u:[],g:[],ug:[]};if(!P.fit||!Array.isArray(P.fit.w))P.fit={cls:P.cls,w:[],u:[],g:[],ug:[]};const F=P.fit;if(!Array.isArray(F.u))F.u=[];if(!F.g)F.g=F.w.map(()=>1);if(!F.ug)F.ug=F.u.map(()=>1);
  if(F.cls!==P.cls||(F.d||null)!==(designOf(P.faction,P.cls)?P.faction:null))fitMigrate(P,F);if(P.tune&&typeof P.tune==='object')FIT_T.set(P.tune,F);return F}
// a new hull: the fitted parts move across into slots that take them, in order; what doesn't fit goes to the vault
function fitMigrate(P,F){const D=slotsOf(P.cls,P.faction),st=P.vault||(P.vault={}),N={cls:P.cls,d:designOf(P.faction,P.cls)?P.faction:null,w:D.w.map(()=>''),u:D.u.map(()=>''),g:D.w.map(()=>1),ug:D.u.map(()=>1),wi:D.w.map(()=>null),ui:D.u.map(()=>null)};const wi=F.wi||[],ui=F.ui||[];
  F.w.forEach((k,j)=>{if(!k)return;const i=N.w.findIndex((s,x)=>!s&&wpnOK(P.cls,k,x));if(i>=0){N.w[i]=k;N.g[i]=F.g[j]||1;N.wi[i]=wi[j]||null}else partToStore(st,k,F.g[j]||1,wi[j])});
  F.u.forEach((k,j)=>{if(!k)return;const i=N.u.indexOf('');if(i>=0){N.u[i]=k;N.ug[i]=F.ug[j]||1;N.ui[i]=ui[j]||null}else partToStore(st,k,F.ug[j]||1,ui[j])});Object.assign(F,N)}
function fitG(P,k){const F=fitOf(P);let g=0;F.w.forEach((x,i)=>{if(x===k)g=Math.max(g,F.g[i]||1)});return g}
function fitGs(P,k){const F=fitOf(P);let s=0;F.w.forEach((x,i)=>{if(x===k)s+=(F.g[i]||1)-1});return s}
function fitUG(P,k){const F=fitOf(P);let g=0;F.u.forEach((x,i)=>{if(x===k)g=Math.max(g,F.ug[i]||1)});return g}
function fitN(P,k){if(!loadOn())return k==='gun'||k==='laser'?1:0;return fitOf(P).w.filter(x=>x===k).length}
function fitHas(P,k){if(!loadOn())return k==='land';return fitOf(P).u.includes(k)}
function ammoCap(P){return Math.round((fitN(P,'gun')+PG.ammo*fitGs(P,'gun'))*LOAD.ammo)}
function mtools(P){const w=fitOf(P).w;return['charge','mlaser'].filter(k=>w.includes(k))}
function mtoolOf(P){const t=mtools(P);if(!t.includes(P.mtool))P.mtool=t[0]||null;return P.mtool}
function pilotOfEnt(e){if(!e)return null;if(e.isPlayer)return S.player;if(e.rp)return(S.pilots||{})[e.rp]||null;return null}
function ldSay(e,t,bad){if(!e)return;const k='_ldm'+t.length;if(W.t-(e[k]||-9)<2.5)return;e[k]=W.t;if(e.isPlayer)flash(t,!!bad);else if(e.rp&&NET.host)netMsg(e.rp,'flash',t,!!bad)}
// ---- launcher and magazine sizes follow the fit
{const o=pRack;pRack=function(P){if(!loadOn()||!P)return o.apply(this,arguments);const k=isTorpHull(P.cls)?'torpedo':'missile',n=fitN(P,k);return n?o.apply(this,arguments)*n+fitGs(P,k):0}}
{const o=blCap;blCap=function(P){if(!loadOn()||!P)return o.apply(this,arguments);const n=fitN(P,'charge');return n?Math.round(o.apply(this,arguments)*(1+.5*(n-1)))+fitGs(P,'charge'):0}}
// payload is never reloaded in flight: the rack, the charge magazine and the rounds only refill by rearming at a dock.
// Swarm pods are part of the hull and still reload on their own.
{const o=magTick;magTick=function(P,dt){if(!loadOn()||!P||!P.tiers)return o.apply(this,arguments);fitOf(P);mtoolOf(P);
  const cap=pRack(P),sc=swarmCap(P);if(!P.magV){P.rack=cap;P.swarm=sc;P.mslT=0;P.swT=0;P.magV=1}if(P.rack>cap)P.rack=cap;P.mslT=0;
  const bc=blCap(P);if(P.blN==null)P.blN=bc;if(P.blN>bc)P.blN=bc;P.blT=0;
  const ac=ammoCap(P);if(P.ammo==null)P.ammo=ac;if(P.ammo>ac)P.ammo=ac;
  if(P.wpn==='laser'&&!fitN(P,'laser')&&fitN(P,'gun'))P.wpn='kinetic';else if(P.wpn!=='laser'&&!fitN(P,'gun')&&fitN(P,'laser'))P.wpn='laser';
  if(sc&&(P.swarm||0)<sc){if(!(P.swT>0))P.swT=reloadT(P,'swarm');P.swT-=dt;if(P.swT<=0){P.swarm=sc;P.swT=0}}else P.swT=0}}
// ---- the machine gun spends a round a shot (and little energy); extra guns or lasers of a kind add damage
{const o=fire;fire=function(e){const P=loadOn()&&pilotOfEnt(e);if(!P)return o.apply(this,arguments);if(e.jamMode&&fitN(P,'jammer'))return o.apply(this,arguments);const n=fitN(P,'gun');
  if(!n){ldSay(e,`No machine gun fitted.${fitN(P,'laser')?' Lasers: '+kb('las')+'.':''}`,true);return}
  if(!(P.ammo>0)){ldSay(e,`Out of ammunition: dock to rearm.${fitN(P,'laser')?' Switch to lasers ('+kb('las')+').':''}`,true);return}
  const lf=e.lastFire,d=e.st.dmg;e.st.dmg=d*(1+LOAD.dupK*(n-1))*(1+PG.dmg*(fitG(P,'gun')-1));try{o.apply(this,arguments)}finally{e.st.dmg=d}
  if(e.lastFire!==lf){P.ammo=Math.max(0,P.ammo-1);e.energy=Math.min(e.st.eCap,e.energy+e.st.shotCost*LOAD.gunE)}}}
{const o=fireLaser;fireLaser=function(e){const P=loadOn()&&pilotOfEnt(e);if(!P)return o.apply(this,arguments);const n=fitN(P,'laser');
  if(!n){ldSay(e,'No laser fitted.',true);return}const d=e.st.dmg;e.st.dmg=d*(1+LOAD.dupK*(n-1))*(1+PG.dmg*(fitG(P,'laser')-1));try{return o.apply(this,arguments)}finally{e.st.dmg=d}}}
{const o=setWeapon;setWeapon=function(w){if(!loadOn()||!S||!running)return o.apply(this,arguments);const P=S.player,k=w==='laser'?'laser':'gun';
  if(!fitN(P,k)){flash(k==='laser'?'No laser fitted.':'No machine gun fitted.',true);return}if(P.wpn===w)return;P.wpn=w;
  flash(w==='laser'?'Laser: instant hit, heavy reactor draw. Strong against shields.':`Machine gun: lead the target. ${P.ammo} rounds aboard. Strong against hull.`)}}
// ---- missiles and torpedoes: payload rearmed at a dock; a pilot's missiles hit twice as hard
{const o=fireMissile;fireMissile=function(){if(!loadOn()||!W||!running||S.player.docked||W.dead)return o.apply(this,arguments);const P=S.player,t=isTorpHull(P.cls);
  if(!pRack(P)){flash(`No ${t?'torpedo':'missile'} launcher fitted.`,true);return}if(P.rack<=0){flash(`Out of ${t?'torpedoes':'missiles'}: dock to rearm.`,true);return}return o.apply(this,arguments)}}
{const o=launchMissile;launchMissile=function(e,tgt,tier,kind){const n=W.missiles.length;const r=o.apply(this,arguments);
  if(loadOn()&&(kind||'missile')==='missile'&&(e.isPlayer||e.rp)){const m=W.missiles[W.missiles.length-1];if(W.missiles.length>n&&m&&m.src===e)m.dmg*=LOAD.mslK}return r}}
// ---- charges: only with a charge launcher fitted, and none reloaded in flight
{const o=blFire;blFire=function(e,P){if(!loadOn())return o.apply(this,arguments);if(!fitN(P,'charge')){blSay(P,'No charge launcher fitted.',true);return}
  if(!(P.blN>0)&&!((e.blCd||0)>W.t)){blSay(P,'No charges left: dock to rearm.',true);return}return o.apply(this,arguments)}}
// ---- the landing kit: without one, E never offers to land on a rock
{const o=landCandidate;landCandidate=function(){if(loadOn()&&!fitHas(S.player,'land'))return null;return o.apply(this,arguments)}}
// ---- cargo modules and scanners
{const o=shipStats;shipStats=function(fac,cls,T,U){const B=o.apply(this,arguments);const F=U&&typeof U==='object'&&FIT_T.get(U);
  if(F&&F.cls===cls&&loadOn()&&B.cargo){let k=0;F.u.forEach((x,i)=>{if(x==='cargo')k+=LOAD.cargoK+PG.cargo*((F.ug[i]||1)-1)});if(k)B.cargo=Math.round(B.cargo*(1+k))}return B}}
{const o=vF;vF=function(P,key){const v=o.apply(this,arguments);if((key==='blScanR'||key==='blScan')&&loadOn()&&P&&P.fit&&fitHas(P,'scanner'))return Math.max(v||0,key==='blScanR'?LOAD.scanR*(1+PG.scan*(fitUG(P,'scanner')-1)):LOAD.scanT);return v}}
// ============================================================ the mining laser and rock rings
// Every rock has a ring: a seam around it (a great circle fixed by its seed). Hold the beam on the ring and ore is cut steadily
// into the hold; off the ring the beam only sparks. A blast breaks a rock's ring for good, so each rock is worked one way:
// slow and safe with the laser, or fast and risky with charges. Ore moves from the rock to the hold: nothing is made or lost.
function ringN(a){if(a._rn&&a._rnk===a.id)return a._rn;const r=blRng(((a.seed||a.id||1)*31+7)>>>0),z=r()*2-1,t=r()*TAU,q=Math.sqrt(1-z*z);a._rn={x:q*Math.cos(t),y:q*Math.sin(t),z};a._rnk=a.id;return a._rn}
function ringOK(a){return!!a&&!a.wpt&&!a.comet&&!a.noRing&&oreTotal(a)>0}
// where the beam meets the rock, and whether that point is on the ring
function mlBeam(e,a){qRot(e.q,0,0,1,_f);const R=astR(a),r=e.st.radius,ox=e.x+_f.x*r-a.x,oy=e.y+_f.y*r-a.y,oz=e.z+_f.z*r-a.z,b=ox*_f.x+oy*_f.y+oz*_f.z,c=ox*ox+oy*oy+oz*oz-R*R,D=b*b-c;
  if(D<0)return null;const t=-b-Math.sqrt(D);if(t<0||t>LOAD.ml.range)return null;const hx=ox+_f.x*t,hy=oy+_f.y*t,hz=oz+_f.z*t,n=ringN(a),s=(hx*n.x+hy*n.y+hz*n.z)/R;
  return{x:a.x+hx,y:a.y+hy,z:a.z+hz,d:t,on:Math.abs(s)<LOAD.ml.band,off:Math.abs(s)}}
function mlRate(P){return(LOAD.ml.rate[P.cls]||.2)*(1+.2*(blTier(P)-1))*(1+PG.ml*(Math.max(1,fitG(P,'mlaser'))-1))}
// one frame of cutting (host and single player; a guest's client calls it with show only, for the beam)
function mlCut(e,P,a,dt,sec,show){const need=LOAD.ml.e*dt;if(e.energy<need)return'energy';e.energy-=need;const B=mlBeam(e,a);if(!B)return'aim';
  if(!MUTE)W.beams.push({src:e,x:B.x,y:B.y,z:B.z,ttl:.06,col:B.on?'#7ad9a7':'#f0b24a'});if(!B.on){if(!MUTE&&Math.random()<dt*6)fxSpark(B,'#f0b24a',1);return'ring'}
  if(!MUTE&&Math.random()<dt*10)fxSpark(B,'#ffe0b0',1);if(show)return'cut';
  e.mlAcc=(e.mlAcc||0)+mlRate(P)*dt;while(e.mlAcc>=1){const k=mainOre(a);if(!k)break;if(mass(k)>e.st.cargo-invMass(P.cargo))return'full';e.mlAcc-=1;inv.take(a.ore,k,1);inv.add(P.cargo,k,1);a.lased=1}
  if(oreTotal(a)<=0){removeAst(sec,a);return'done'}return'cut'}
function mlSay(e,P,r){const T={energy:'Mining laser: not enough reactor energy.',aim:`Mining laser: point at the rock, within ${LOAD.ml.range} m.`,ring:'Mining laser: hold the beam on the ring (the green band).',full:'Hold is full. Dock to unload.',done:'The rock is cut through: nothing left in it.'};if(T[r])ldSay(e,T[r],r!=='ring'&&r!=='aim')}
// F with the mining laser picked: scoop chunks and clouds as before, otherwise cut the targeted rock along its ring
{const o=blPilotUpdate;blPilotUpdate=function(p,P,st,sec,dt){if(!loadOn()||!blHull(P.cls)||mtoolOf(P)!=='mlaser')return o.apply(this,arguments);
  const hold=!!(keys.KeyF||mouse.r||touch.mine);p.blHeld=hold;p.mining=null;p.mlRock=null;p.mlA=0;
  {const ch=!NET.cl&&chunkAt(p,sec);if(ch){p.mining=ch;p.mining0=ch;blCollect(p,P,ch,dt,sec)}}
  const cl=hold?blCloudNear(p,sec):null;if(cl){p.mining=cl;if(!NET.cl&&cl!==p.mining0)blCollect(p,P,cl,dt,sec);p.mining0=null;return}p.mining0=null;if(!hold)return;
  const a=W.tgt&&W.tgt.kind==='ast'&&validTgt(W.tgt)?W.tgt.ref:null;if(!a){ldSay(p,'Mining laser: target a rock (R), then hold F with its ring under your nose.');return}
  if(!ringOK(a)){ldSay(p,'This rock\'s ring is broken: a blast cracked it. Switch to charges ('+kb('mtool')+') or find another rock.',true);return}
  p.mlRock=a;p.mlA=a.id;mlSay(p,P,mlCut(p,P,a,dt,sec,NET.cl))}}
// a guest's mining laser: the host cuts for it from the rock id in its input
{const o=netWorld;netWorld=function(dt){o.apply(this,arguments);if(!loadOn())return;const now=performance.now(),sec=S.sectors[W.sid];
  for(const e of W.ents){if(!e.rp||!e.alive)continue;const u=MP.inp[e.rp],P=S.pilots[e.rp];if(!u||!P||!u.ml||now-u.at>600||!fitN(P,'mlaser'))continue;const a=sec.ast.find(x=>x.id===u.ml);if(!ringOK(a))continue;e.mlRock=a;mlSay(e,P,mlCut(e,P,a,dt,sec))}}}
// a blast breaks the ring of every rock it cracks
{const o=blDetonate;blDetonate=function(P,e){const s=S.sectors[W.sid],k=blKey(P),ids=new Set((s.charges||[]).filter(c=>c.o===k&&!c.wp).map(c=>c.a));const r=o.apply(this,arguments);for(const a of s.ast)if(ids.has(a.id))a.noRing=1;return r}}
function mtoolToggle(){const P=S.player,t=mtools(P);if(!loadOn()||!t.length){flash('No mining tools fitted.',true);return}if(t.length<2){flash(`${WPN[t[0]].name} is your only mining tool.`);return}
  P.mtool=P.mtool==='mlaser'?'charge':'mlaser';flash(P.mtool==='mlaser'?'Mining laser: target a rock, hold F on its ring. Slow, steady and safe.':`Charge launcher: F fires a charge at a fault point, ${kb('det')} detonates. ${P.blN||0} charges aboard.`)}
// the ring on the targeted rock (when scanned or close), green where the beam would cut
{const o=blDraw;blDraw=function(c){o.apply(this,arguments);if(!loadOn())return;const p=W.player,P=S.player;if(!p||!fitN(P,'mlaser'))return;
  const a=W.tgt&&W.tgt.kind==='ast'&&validTgt(W.tgt)?W.tgt.ref:null;if(!a||!ringOK(a))return;const dist=d3(a,p);if(!((a.scanT||0)>W.t||dist<BL.eyeR+astR(a)+300))return;
  const n=ringN(a),R=astR(a)*1.01,ax=Math.abs(n.x)<.9?{x:1,y:0,z:0}:{x:0,y:1,z:0};let u={x:n.y*ax.z-n.z*ax.y,y:n.z*ax.x-n.x*ax.z,z:n.x*ax.y-n.y*ax.x};const ul=hyp(u.x,u.y,u.z);u={x:u.x/ul,y:u.y/ul,z:u.z/ul};
  const v={x:n.y*u.z-n.z*u.y,y:n.z*u.x-n.x*u.z,z:n.x*u.y-n.y*u.x},B=mlBeam(p,a),on=mtoolOf(P)==='mlaser'&&B&&B.on;c.save();c.lineWidth=on?2.5:1.6;
  let prev=null;for(let i=0;i<=64;i++){const th=i/64*TAU,cs=Math.cos(th),sn=Math.sin(th),wx=u.x*cs+v.x*sn,wy=u.y*cs+v.y*sn,wz=u.z*cs+v.z*sn,front=(wx*(p.x-a.x)+wy*(p.y-a.y)+wz*(p.z-a.z))>0,L=proj(a.x+wx*R,a.y+wy*R,a.z+wz*R);
    if(prev&&!L.behind&&!prev.L.behind){c.strokeStyle=front?(on?'#7ad9a7':'rgba(122,217,167,.8)'):'rgba(122,217,167,.22)';c.beginPath();c.moveTo(prev.L.x,prev.L.y);c.lineTo(L.x,L.y);c.stroke()}prev={L}}
  if(B&&mtoolOf(P)==='mlaser'){const L=proj(B.x,B.y,B.z);if(!L.behind){c.strokeStyle=B.on?'#7ad9a7':'#f0b24a';c.beginPath();c.arc(L.x,L.y,6,0,TAU);c.stroke()}}c.restore()}}
// ============================================================ rearming at a dock
// rounds, missiles or torpedoes, and charges, paid to the station owner's treasury (free at your own depot or outpost)
function rearmQuote(P){const t=isTorpHull(P.cls),q={ammo:Math.max(0,ammoCap(P)-(P.ammo||0)),rack:Math.max(0,pRack(P)-(P.rack||0)),chg:Math.max(0,blCap(P)-(P.blN||0))};
  q.cr={ammo:Math.ceil(q.ammo*LOAD.ammoCr),rack:q.rack*(t?LOAD.torpCr:LOAD.mslCr),chg:q.chg*LOAD.chgCr};q.tot=q.cr.ammo+q.cr.rack+q.cr.chg;q.n=q.ammo+q.rack+q.chg;return q}
function rearmDo(c,P){const q=rearmQuote(P);if(!q.n)return'Nothing to rearm.';c={...c,wallet:c.wallet||'neutral'};const free=false,t=isTorpHull(P.cls),got=[];let paid=0;
  const buy=(n,each,fn,lab)=>{if(!n)return;let k=free?n:Math.min(n,Math.floor((P.credits-paid)/each));if(k<=0)return;const cr=free?0:Math.ceil(k*each);paid+=cr;fn(k);got.push(`${fmt(k)} ${lab}`)};
  buy(q.rack,t?LOAD.torpCr:LOAD.mslCr,k=>P.rack=(P.rack||0)+k,t?'torpedoes':'missiles');buy(q.chg,LOAD.chgCr,k=>P.blN=(P.blN||0)+k,'charges');buy(q.ammo,LOAD.ammoCr,k=>P.ammo=(P.ammo||0)+k,'rounds');
  if(paid)transfer('player',c.wallet,paid);if(!got.length)return'Not enough credits to rearm.';return`✓ Rearmed: ${got.join(', ')}${paid?` for ${fmt(paid)} cr to the ${sideName(c.wallet)} treasury`:''}.`}
// fit a part into a slot (from your hold or storage, or bought here when the market has one), or take it out ('' kind): the part
// that comes out goes to storage, with the components of its upgrades
function fitDo(c,P,arg){let[g,i0,k]=String(arg).split(':');const i=+i0,F=fitOf(P),ws=g==='w',arr=ws?F.w:F.u,gr=ws?F.g:F.ug;if(g!=='w'&&g!=='u')return'';let pick=null;if(k&&ITEMS[k]&&ITEMS[k].part){pick=k;k=ITEMS[k].part}
  const ids=ws?(F.wi||(F.wi=F.w.map(()=>null))):(F.ui||(F.ui=F.u.map(()=>null)));
  if(!(i>=0&&i<arr.length))return'No such slot.';if(k&&(ws?!wpnOK(P.cls,k,i):!UTIL[k]))return'That part doesn\'t fit that slot.';const it=k&&(pick||PART[k]);if((k||'')===(arr[i]||'')&&(ids[i]||PART[k]||null)===(it||null))return'';
  const st=c.storage||P.vault,srcs=[P.cargo,st];
  if(k&&countIn(it,srcs)<1){if(c.market&&(c.market[it]||0)>0){dockErr='';dockActionBase('buy',it+':1');if(countIn(it,srcs)<1)return dockErr&&!String(dockErr).startsWith('✓')?dockErr:'Could not buy one.'}
    else return`No ${ITEMS[it].name} on hand: build one (Fabricate) or buy one where it's sold.`}
  const out=arr[i],outIt=out&&(ids[i]||PART[out]);if(out)partToStore(st,out,gr[i],ids[i]);arr[i]='';gr[i]=1;ids[i]=null;if(k){takeFrom({[it]:1},srcs);arr[i]=k;gr[i]=1;ids[i]=it===PART[k]?null:it}
  if(P.tune&&typeof P.tune==='object')FIT_T.set(P.tune,F);if(W&&W.player)refreshPlayerStats();mtoolOf(P);if(P.ammo>ammoCap(P))P.ammo=ammoCap(P);if(P.rack>pRack(P))P.rack=pRack(P);if(P.blN>blCap(P))P.blN=blCap(P);
  return k?`✓ ${ITEMS[it].name} fitted${out?`; the ${ITEMS[outIt].name} went to your ${String(c.storageName||'vault').toLowerCase()}`:''}.`:`✓ ${ITEMS[outIt].name} taken out and put in your ${String(c.storageName||'vault').toLowerCase()}.`}
// upgrade a fitted part to its next grade: the grade's components from hold or storage, and a workshop fee at a power's or freeport dock
function pupQuote(c,P,arg){const[g,i0]=String(arg).split(':'),i=+i0,F=fitOf(P),k=(g==='w'?F.w:F.u)[i],t=((g==='w'?F.g:F.ug)[i]||1)+1;if(!k||k==='land'||t>MK_TOP)return null;const r=partUpg(t);return{k,t,r,fee:c.fee?Math.ceil(invValue(r)*.08):0}}
function pupDo(c,P,arg){const q=pupQuote(c,P,arg);if(!q)return'That part can\'t be upgraded further.';const srcs=[P.cargo,c.storage||P.vault];if(!haveIn(q.r,srcs))return'Not enough components for that grade.';if(P.credits<q.fee)return'Not enough credits for the workshop fee.';
  takeFrom(q.r,srcs);if(q.fee)transfer('player',c.wallet,q.fee);const[g,i0]=String(arg).split(':'),F=fitOf(P);(g==='w'?F.g:F.ug)[+i0]=q.t;if(W&&W.player)refreshPlayerStats();return`✓ ${ITEMS[PART[q.k]].name} upgraded to grade ${q.t}.`}
let dockActionBase=null;
{const o=dockAction;dockActionBase=o;dockAction=function(act,arg){if(loadOn()&&(act==='rearm'||act==='fit'||act==='pup')){const c=dockCtx(),P=S.player;dockErr=act==='rearm'?rearmDo(c,P):act==='fit'?fitDo(c,P,arg):pupDo(c,P,arg);return}return o.apply(this,arguments)}}
// docking rearms whatever the credits cover
{const o=openDock;openDock=function(){const r=o.apply(this,arguments);try{if(loadOn()&&S.player.docked&&S.player.docked!=='bridge'&&S.player.docked!=='turret'&&rearmQuote(S.player).n){dockClick('rearm');if(!NET.cl&&dockErr&&dockErr.startsWith('✓'))feed(dockErr.slice(2),'info')}}catch(err){}return r}}
// the Loadout section of the Ship tab: each slot's part and grade, its next upgrade, and the parts that could go in it
function loadoutHtml(c,P){if(!loadOn())return'';const F=fitOf(P),q=rearmQuote(P),t=isTorpHull(P.cls),srcs=[P.cargo,c.storage||P.vault];
  let h=`<div class="h3" style="margin-top:22px">Loadout · ${F.w.length} weapon slot${F.w.length>1?'s':''}, ${F.u.length} utility</div><p class="note" style="margin-top:0">Each slot takes one part. Parts are built from components (Fabricate) or bought where they're sold, and upgraded in place through grades 1 to 5 with each grade's components; grades 3 to 5 also need a Calibration Matrix. A part you take out goes to your ${esc(String(c.storageName||'vault').toLowerCase())} with its upgrade components. The machine gun is limited by its rounds, the laser by your reactor, launchers by their payload, which is rearmed when you dock and never in flight.</p>`;
  const row=(g,i,cur,gr,opts,lab)=>{const arg=`${g}:${i}`,uq=cur?pupQuote(c,P,arg):null,cid=cur?((g==='w'?F.wi:F.ui)||[])[i]||PART[cur]:null,nm=cur?ITEMS[cid].name:'';
    let r=`<div style="border-top:1px solid var(--line);padding:6px 0"><div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap"><span class="note" style="width:70px;margin:0">${lab} ${i+1}</span>${cur?`<b>${esc(nm)}</b><span class="req ok">grade ${gr}</span>`:'<span class="note" style="margin:0">empty</span>'}`;
    if(uq){const ok=haveIn(uq.r,srcs)&&P.credits>=uq.fee;r+=`<button class="btn sm" type="button" data-act="pup" data-arg="${arg}" ${ok?'':'disabled'}>To grade ${uq.t}${uq.fee?` · ${fmt(uq.fee)} cr`:''}</button>${Object.keys(uq.r).map(x=>chip(x,uq.r[x],countIn(x,srcs))).join('')}`}
    if(cur)r+=`<button class="btn sm" type="button" data-act="fit" data-arg="${arg}:">Take out</button>`;r+=`</div><div style="display:flex;gap:6px;flex-wrap:wrap;margin:4px 0 0 78px">`;
    for(const k of opts)for(const it of partItems(k)){if(it===cid)continue;const have=countIn(it,srcs),mk=c.market&&(c.market[it]||0)>0?mBuy(c,it):0;if(it!==PART[k]&&!have&&!mk)continue;
      r+=`<button class="btn sm" type="button" data-act="fit" data-arg="${arg}:${it}" title="${esc((WPN[k]||UTIL[k]).desc+(ITEMS[it].trTxt?' '+ITEMS[it].trTxt:''))}" ${have||mk&&P.credits>=mk?'':'disabled'}>${esc(ITEMS[it].name)} · ${have?`${have} on hand`:mk?`buy ${fmt(mk)} cr`:'none here'}</button>`}
    return r+'</div></div>'};
  F.w.forEach((w,i)=>{h+=row('w',i,w,F.g[i]||1,Object.keys(WPN).filter(k=>wpnOK(P.cls,k,i)),'Weapon')});
  F.u.forEach((u,i)=>{h+=row('u',i,u,F.ug[i]||1,Object.keys(UTIL),'Utility')});
  const rows=[ammoCap(P)?`Rounds ${fmt(P.ammo||0)} / ${fmt(ammoCap(P))}`:'',pRack(P)?`${t?'Torpedoes':'Missiles'} ${P.rack||0} / ${pRack(P)}`:'',blCap(P)?`Charges ${P.blN||0} / ${blCap(P)}`:''].filter(Boolean);
  h+=`<div style="display:flex;gap:10px;align-items:center;margin-top:10px;flex-wrap:wrap"><button class="btn" type="button" data-act="rearm" ${q.n&&(!c.wallet||P.credits>0)?'':'disabled'}>Rearm${q.n?` · ${fmt(q.tot)} cr`:''}</button><span class="note">${rows.join(' · ')||'No payload weapons fitted.'}</span></div>`;return h}
{const o=insHtml;insHtml=function(c,P){return loadoutHtml(c,P)+o.apply(this,arguments)}}
// HUD: the gun readout shows the rounds left, or the mining tool on a mining hull
{const o=hudUpdate;hudUpdate=function(){const r=o.apply(this,arguments);try{if(loadOn()&&W&&W.player&&!S.player.docked){const P=S.player,el=$('hWpn');
  const g=P.wpn==='laser'?(fitN(P,'laser')?'LASER':'—'):(fitN(P,'gun')?`GUN ${P.ammo||0}`:'—'),m=blHull(P.cls)&&mtoolOf(P)?` · ${P.mtool==='mlaser'?'M-LASER':'CHARGES '+(P.blN||0)}`:'';el.textContent=g+m;if(P.wpn!=='laser'&&fitN(P,'gun')&&(P.ammo||0)<60)el.style.color='var(--danger)'}}catch(err){}return r}}
// a guest keeps its own pick of mining tool; the host's record wins for everything else
OWN.push('mtool');

// ---- stage 4 bookkeeping: fitted parts are counted in the ledger with the pilot's ship; a new pilot's default fit and the
// stations' first stock of parts are made with the galaxy (before its baseline is taken), so nothing appears later from nothing
{const o=ledger;ledger=function(){const r=o.apply(this,arguments);const Y=r.L['Your ship, hold, vault'];for(const P of allPilots()){if(!P||!P.fit)continue;const v=invVec(fitItems(P.fit));for(const e of RAWS){Y[e]+=v[e];r.tot[e]+=v[e]}}return r}}
// freeports stock every part, the powers' core stations their combat and utility parts (makers take over in stage 7)
function partsSeed(){for(const id in S.stations||{}){const R=S.stations[id];if(!R)continue;const st=mkStock(R);if(R.owner==='neutral'){for(const k in PART)inv.add(st,PART[k],3)}
  else if(FAC_IDS.includes(R.owner)&&R.kind==='core'){for(const k of['gun','laser','missile','torpedo','land','cargo','scanner'])inv.add(st,PART[k],2)}}}
{const o=newGame;newGame=function(){const r=o.apply(this,arguments);if(S&&S.player){if(!S.player.fit)S.player.fit=fitNew(S.player.cls,designOf(S.player.faction,S.player.cls)?S.player.faction:null);partsSeed();const l=ledger();S.ledger0={tot:l.tot,credits:l.credits}}return r}}
{const o=newPilot;newPilot=function(pid){const r=o.apply(this,arguments);const P=S.pilots&&S.pilots[pid];if(P&&!P.fit)devLedger(()=>{P.fit=fitNew(P.cls,designOf(P.faction,P.cls)?P.faction:null)});return r}}
