//@src 16zzm_gatelock.js
// ============================================================ gate lock kits (Beyond 6c, decided by the user 6 Nov 2026)
// Pirate gear from the Wrack. Scrapheart Haven makes a kit every 10 minutes from the Unbound's stores (one Alloy Plate and
// one Conduit each, so the ledger stays exact) while it has the materials and fewer than four on its shelf, and sells them
// for 2,500 cr, one per pilot per hour. Owning one is no crime; carrying one is contraband, like the rest of the gear.
// Fly within 300 m of a gate with a kit in your hold and press F: the lock clamps the gate and arms in 20 s (it can be shot
// off meanwhile, at a quarter of its health), with a warning to every ship on both sides. Armed, the gate is sealed both
// ways for 5 minutes, then the lock burns out. It has 2,000 health, no shield and no regrowth, every weapon does full
// damage, and it can be shot from either side of the gate. Burnt out or destroyed, its materials fall as debris there.
// Not on a freeport's gates or the Wrack's, one per gate, and never on a power's home system's last open gate. Capital
// ships still jump on their own drives. A convoy that reaches a locked gate is stuck there until the lock goes; off-screen
// traffic routes round a locked gate when there is a way round. The Unbound set locks on the convoys their raiders lie in
// wait for (more under a Cunning or Greedy Dread Pirate, less under a Paranoid one), using the haven's own kits. Locking a
// power's gate where its ships or its beacon see you costs standing with it and raises its heat on you; a lock that traps
// one of its convoys counts as raiding it. The powers post a job to break a lock on their gates, paid to whoever kills it.
const GL={hp:2000,arm:20,hold:300,price:2500,sell:1250,make:600,shelf:4,gap:3600,setR:300,seeR:4000,stand:8,heat:30,trap:5,breakPay:800,unbBase:.45};
ITEMS.glock={name:'Gate lock kit',recipe:{plate:1,wire:1},col:'#d8cd98',gear:1};ITEM_ORDER.push('glock');
CLASSES.glock={name:'Gate lock',hull:GL.hp,shield:0,speed:.01,turn:.01,weapon:0,cargo:0,drill:0,radius:110,rack:0,boost:1,agile:.1,acc:.01,desc:'An Unbound clamp sealing a jump gate.'};
if(PIRATE.hulls)PIRATE.hulls.glock='Gate lock';
function glOf(a,b){const k=gateKey(a,b);return(S.glocks||[]).find(L=>L.key===k)||null}
function glName(L){return`the gate between ${DEF[L.a].name} and ${DEF[L.b].name}`}
function glLeft(L){return Math.max(0,L.stage==='arm'?L.t0+GL.arm-S.T:L.until-S.T)}
// where a lock may go
function glWhyNot(a,b){if(!a||!b||!(NEIGH[a]||[]).includes(b))return'There is no gate there.';const k=gateKey(a,b);
  if(a==='wr'||b==='wr')return'The Wrack\'s gates can\'t be locked.';
  if(isFreeF(S.stations[a])||isFreeF(S.stations[b])||DEF[a].kind==='free'||DEF[b].kind==='free')return'A freeport\'s gates can\'t be locked.';
  if(glOf(a,b))return'This gate already has a lock on it.';if(ogAt(a,b)||S.gateDown[k])return'This gate is already sealed.';
  for(const x of[a,b])if(DEF[x].home&&ogOpenGates(x,k)<1)return`That would cut ${DEF[x].name} off: a home system always keeps one gate open.`;return''}
// a lock clamps a gate (by a pilot's key, or 'pirate' for the Unbound); the kit's materials ride in the lock
function glPlace(a,b,by){const why=glWhyNot(a,b);if(why)return why;const L={id:S.nextId++,key:gateKey(a,b),a,b,by,t0:S.T,stage:'arm',until:S.T+GL.arm+GL.hold,hp:GL.hp*.25,load:{...ITEMS.glock.recipe},trap:{}};
  (S.glocks=S.glocks||[]).push(L);ogSay(L,`⚠ Something is clamping ${glName(L)}: a gate lock, arming in ${GL.arm} s. Shoot it off the gate.`,'warn');return L}
function glEnd(L,sid){S.glocks=(S.glocks||[]).filter(x=>x!==L);if(L.down!=null&&S.gateDown[L.key]===L.down)delete S.gateDown[L.key];const s=S.sectors[sid||L.a];if(s)toDebris(s,L.load);L.load={};
  for(const w of Object.values(WORLDS))for(const e of w.ents)if(e.glId===L.id&&e.alive){e.alive=false;const i=w.ents.indexOf(e);if(i>=0)w.ents.splice(i,1)}}
function glTick(){if(NET.cl||!S)return;S.glocks=S.glocks||[];const T=S.T;
  for(const L of S.glocks.slice()){if(L.stage==='arm'&&T>=L.t0+GL.arm){L.stage='set';L.hp=Math.min(GL.hp,L.hp+GL.hp*.75);S.gateDown[L.key]=L.down=L.until;for(const w of Object.values(WORLDS))for(const e of w.ents)if(e.glId===L.id&&e.alive)e.hull=L.hp;ogSay(L,`⚠ ${glName(L)[0].toUpperCase()+glName(L).slice(1)} is locked for ${GL.hold/60} minutes.`,'bad');continue}
    if(T>=L.until){ogSay(L,`The gate lock on ${glName(L)} has burnt out: the gate is open.`,'info');glEnd(L)}}
  // the haven makes a kit every 10 minutes
  const R=S.stations&&S.stations.wr;if(R&&R.owner==='pirate'&&!havenDown()&&T>=(S.glMakeT||0)){S.glMakeT=T+GL.make;const st=mkStock(R),src=S.econ.stock.pirate;if((st.glock||0)<GL.shelf&&src&&haveIn(ITEMS.glock.recipe,[src])){takeFrom(ITEMS.glock.recipe,[src]);inv.add(st,'glock',1)}}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{glTick()}catch(err){frameErr('gate locks',err)}return r}}
{const o=ledger;ledger=function(){const r=o.apply(this,arguments);try{const L=r.L['Faction & Unbound stores'];for(const x of S.glocks||[]){const v=invVec(x.load||{});for(const e of RAWS){L[e]+=v[e];r.tot[e]+=v[e]}}}catch(e){}return r}}
// ---- in the world: one lock seen from both sides of its gate, one hull
function glEnt(L){const to=W.sid===L.a?L.b:L.a,g=(GATES[W.sid]||[]).find(x=>x.to===to);if(!g)return null;const e=makeNPC('glock','pirate','glock',1,{},'stock:pirate');e.glId=L.id;e.x=g.x*.985;e.y=g.y*.985;e.z=g.z*.985;e.vx=e.vy=e.vz=0;
  qLook(-g.x,-g.y,-g.z,0,1,0,e.q);e.st={...e.st,hull:GL.hp,sCap:0};e.hull=L.hp;e.shield=0;e.noRegen=1e12;e.pname='Gate lock';W.ents.push(e);return e}
function glWorld(){if(NET.cl||!W)return;for(const L of S.glocks||[]){if(L.a!==W.sid&&L.b!==W.sid)continue;let e=W.ents.find(x=>x.alive&&x.glId===L.id);if(!e)e=glEnt(L);if(!e)continue;if(L.hp<e.hull-1)e.hull=L.hp;e.vx=e.vy=e.vz=0;e.shield=0;
    const max=L.stage==='arm'?GL.hp*.25:GL.hp;if(e.hull>max)e.hull=max;L.hp=e.hull}}
{const o=worldUpdate;worldUpdate=function(dt){const r=o.apply(this,arguments);try{glWorld()}catch(err){frameErr('gate locks',err)}return r}}
{const o=npcThink;npcThink=function(e,dt){if(e.role==='glock'){e.vx=e.vy=e.vz=0;e.thrusting=false;e.boosting=false;return}return o.apply(this,arguments)}}
{const o=killShip;killShip=function(e,src,at){if(e&&e.role==='glock'&&e.alive){const L=(S.glocks||[]).find(x=>x.id===e.glId);e.load={};e.cargo={};if(L){const kp=at&&at.src&&at.src.rp,killer=kp||(src==='player'?'me':null);ogSay(L,`✔ The gate lock on ${glName(L)} is destroyed: the gate is open.`,'good');
      if(killer){const f=[sectorOwner(L.a),sectorOwner(L.b)].find(x=>FAC_IDS.includes(x));if(f)runAs(isMe(killer)?null:killer,()=>{const got=transfer(f,'player',GL.breakPay);if(got)feed(`✔ ${FACTIONS[f].short} pays +${fmt(got)} cr for breaking the gate lock.`,'good')})}
      glEnd(L,W.sid)}}return o.apply(this,arguments)}}
// the gate's own text
{const o=ogTxt;ogTxt=function(sid,to){const L=glOf(sid,to);if(L&&L.stage!=='arm')return`This gate is locked by an Unbound gate lock (${Math.round(L.hp)} of ${GL.hp} hull, ${fmtT(glLeft(L))} left). Shoot it off the gate to open it.`;return o.apply(this,arguments)}}
// ---- a convoy that reaches a locked gate waits there; off-screen traffic goes round it
{const o=gateLocked;gateLocked=function(e){const r=o.apply(this,arguments);if(r)return r;try{const D=e&&e.ai&&e.ai.dest;if(e&&e.role==='trader'&&D&&D.type==='gate'&&W){const L=glOf(W.sid,D.to);if(L&&L.stage!=='arm'){glTrap(L,e);return true}}}catch(err){}return false}}
function glTrap(L,e){if(L.trap[e.id])return;L.trap[e.id]=1;if(!L.by||L.by==='pirate'||!FAC_IDS.includes(e.side))return;const P=xPilotOfKey(L.by);if(P&&!P.sworn)standAdd(e.side,-GL.trap,'your gate lock trapped its convoy',P)}
let glRouting=false;
{const o=tradersTick;tradersTick=function(){glRouting=true;try{return o.apply(this,arguments)}finally{glRouting=false}}}
{const o=ogSealed;ogSealed=function(a,b){const r=o.apply(this,arguments);if(r||!glRouting)return r;const L=glOf(a,b);return L&&L.stage!=='arm'?L:null}}
{const o=ogRoute;ogRoute=function(a,b){if(!glRouting)return o.apply(this,arguments);const prev={[a]:null},q=[a];while(q.length){const c=q.shift();if(c===b)break;for(const n of NEIGH[c]||[]){if(n in prev||ogSealed(c,n))continue;prev[n]=c;q.push(n)}}if(!(b in prev))return null;const p=[];for(let c=b;c!=null;c=prev[c])p.unshift(c);return p}}
// ---- the Unbound lock the gate a convoy they're waiting for will leave by
function glUnbChance(){let p=GL.unbBase;if(dpHas('Cunning')||dpHas('Greedy'))p*=1.6;if(dpHas('Paranoid'))p*=.5;return Math.min(.9,p)}
function glUnbTake(){const R=S.stations&&S.stations.wr;if(!R||havenDown())return false;const st=mkStock(R);if(!(st.glock>0))return false;inv.take(st,'glock',1);return true}
function glUnbLock(t){const nx=t.path&&t.path[t.leg+1];if(!nx||glOf(t.sector,nx)||glWhyNot(t.sector,nx)||Math.random()>glUnbChance())return null;if(!glUnbTake())return null;const L=glPlace(t.sector,nx,'pirate');if(typeof L==='string'){inv.add(mkStock(S.stations.wr),'glock',1);return null}L.stage='set';L.hp=GL.hp;S.gateDown[L.key]=L.down=L.until=S.T+GL.hold;return L}
{const o=raidOdds;raidOdds=function(r,sid,base,owner){const p=o.apply(this,arguments);return r&&r.lockK?Math.min(.95,p*r.lockK):p}}
{const o=raidFight;raidFight=function(r){try{if(r&&r.side==='pirate'&&!r.dep&&!r.lockK){const t=(S.traders||[]).find(x=>x.id===r.tgt);if(t&&glUnbLock(t))r.lockK=1.25}}catch(err){}return o.apply(this,arguments)}}
{const o=spawnTrader;spawnTrader=function(t,arrive){const e=o.apply(this,arguments);try{if(arrive&&!NET.cl&&t.kind==='haul'&&(S.raids||[]).some(r=>r.side==='pirate'&&r.tgt===t.id&&r.sector===t.sector)){const L=glUnbLock(t);if(L){L.stage='arm';L.t0=S.T;L.until=S.T+GL.arm+GL.hold;L.hp=GL.hp*.25;delete S.gateDown[L.key];L.down=null}}}catch(err){}return e}}
// ---- a pilot sets one: F within 300 m of a gate with a kit in the hold
function glGateNear(e){if(!W||!e)return null;let best=null,bd=GL.setR+(e.st?e.st.radius:0);for(const g of GATES[W.sid]||[]){const d=d3(e,g);if(d<bd){bd=d;best=g}}return best}
function glSet(P,e,to){if(!P||!e)return'No ship.';if(!(P.cargo.glock>0))return'You have no gate lock kit aboard.';const g=glGateNear(e);if(!g||(to&&g.to!==to))return`Fly within ${GL.setR} m of a gate to set the lock.`;
  const L=glPlace(W.sid,g.to,pkeyOf(P));if(typeof L==='string')return L;inv.take(P.cargo,'glock',1);
  // seen by a power whose gate it is: standing and heat
  for(const sid of[L.a,L.b]){const f=sectorOwner(sid);if(!FAC_IDS.includes(f))continue;const B=S.beacons&&S.beacons[W.sid],seen=(B&&B.owner===f)||W.ents.some(x=>x.alive&&x.type==='ship'&&x.side===f&&!x.isPlayer&&d3(x,e)<GL.seeR);
    if(seen){if(!P.sworn)standAdd(f,-GL.stand,'you locked its gate',P);smHeat(P,f,GL.heat,'locking its gate')}}
  return`☠ Gate lock set on the gate to ${DEF[g.to].name}: it arms in ${GL.arm} s and holds ${GL.hold/60} minutes.`}
{const o=dockAction;dockAction=function(act,arg){if(act==='glock'){const P=S.player,pid=curPid(),e=NET.on&&MP.rp&&pid&&MP.rp[pid]?MP.rp[pid]:W&&W.player,w=e&&worldOf(e);dockErr=w?inW(w,()=>glSet(P,e,String(arg||'')))||'':glSet(P,e,String(arg||''));return}
  if(act==='buy'&&String(arg).split(':')[0]==='glock'){const P=S.player;if(S.T-(P.glockT||-1e9)<GL.gap){dockErr=`The haven sells you one gate lock kit an hour: next in ${fmtT(GL.gap-(S.T-P.glockT))}.`;return}const n0=P.cargo.glock||0,s0=countIn('glock',[P.cargo,P.vault||{}]);const r=o.call(this,act,'glock:1');if(countIn('glock',[P.cargo,P.vault||{}])>s0)P.glockT=S.T;return r}
  return o.apply(this,arguments)}}
if(typeof CO_REMOTE!=='undefined'){CO_REMOTE.add('glock');CO_REMOTE.add('cocol')}
function glPress(){const P=S.player,e=W&&W.player;if(!e||P.docked||W.dead)return false;if(!(P.cargo.glock>0))return false;const g=glGateNear(e);if(!g)return false;
  if(NET.cl){netSend({t:'act',act:'glock',arg:g.to});flash('Setting the gate lock…');return true}dockAction('glock',g.to);flash(dockErr,!/^☠/.test(dockErr));return true}
{const o=blPilotUpdate;blPilotUpdate=function(p,P,st,sec,dt){const hold=!!(keys.KeyF||mouse.r||touch.mine);if(P&&P.cargo&&P.cargo.glock>0&&glGateNear(p)){const press=hold&&!p.glHeld;p.glHeld=hold;if(press)glPress();return}p.glHeld=hold;return o.apply(this,arguments)}}
{const o=convoyChip;convoyChip=function(){const c=o.apply(this,arguments);if(c)return c;try{const P=S.player,e=W&&W.player;if(e&&!P.docked&&P.cargo.glock>0){const g=glGateNear(e);if(g){const why=glWhyNot(W.sid,g.to);return why?[`☠ Gate lock: ${why}`,'warn']:[`☠ F: set a gate lock on the gate to ${DEF[g.to].name}`,'warn']}}
    if(e){for(const L of S.glocks||[])if(L.a===W.sid||L.b===W.sid)return[`☠ Gate lock on the gate to ${DEF[L.a===W.sid?L.b:L.a].name}: ${L.stage==='arm'?'arming':'locked'}, ${fmtT(glLeft(L))}`,'bad']}}catch(err){}return null}}
// contraband: a kit counts as pirate gear for customs
{const o=gearOn;gearOn=function(P){return o.apply(this,arguments)+(P&&P.cargo&&loadOn()?(P.cargo.glock||0):0)}}
// the haven's price; elsewhere a kit fetches half
{const o=mBuy;mBuy=function(c,id){if(id==='glock')return GL.price;return o.apply(this,arguments)}}
{const o=mSell;mSell=function(c,id){if(id==='glock')return GL.sell;return o.apply(this,arguments)}}
// the powers post a job to break a lock on their gates
{const o=jobsList;jobsList=function(c,P,srcs){const out=o.apply(this,arguments);try{if(!c||c.kind!=='station'||!FAC_IDS.includes(c.owner))return out;for(const L of S.glocks||[]){const mine=[L.a,L.b].some(s=>sectorOwner(s)===c.owner);if(!mine)continue;const j=HOP[P.sector][L.a]||0;
      out.push({id:'gl:'+L.id,by:c.owner,sid:L.a,ty:'fight',title:`Break the gate lock on ${esc(glName(L))}`,sub:`${L.stage==='arm'?'arming':'locked'} · ${fmtT(glLeft(L))} left`,hops:j,where:`${j} jump${j===1?'':'s'}`,payN:GL.breakPay,pay:`${fmt(GL.breakPay)} cr`,btn:L.a!==P.sector?['croute',L.a,'Set course']:null,
        detail:()=>`<p class="note" style="margin:0">An Unbound gate lock has sealed the gate. ${FACTIONS[c.owner].short} pays ${fmt(GL.breakPay)} cr to whoever destroys it (2,000 hull, any weapon, from either side of the gate).</p>`})}}catch(err){console.error(err)}return out}}
// its look: a ring of clamps round the gate's mouth in Unbound sand, with red warning lights
{const o=shipMesh;shipMesh=function(fac,cls){if(cls!=='glock')return o.apply(this,arguments);if(MESH.glock)return MESH.glock;
  const F=hexRGB(PIRATE.col),D=[.22,.2,.16],Rd=[1,.25,.2],g=new GB(),L=new GB();g.set(0,0,0).torus(.62,.07,24,6,D,0);
  for(let i=0;i<6;i++){const a=i/6*TAU;g.set(Math.cos(a)*.62,Math.sin(a)*.62,0,qLook(Math.cos(a),Math.sin(a),0,0,0,1,q0())).box(.16,.16,.3,F,0);g.set(Math.cos(a)*.5,Math.sin(a)*.5,.12).sphere(.05,4,6,Rd,1)}
  L.seg([0,0,0],[0,0,0],[0,0,0]);return MESH.glock={hull:g.upload(),rim:L.upload(true),eng:[]}}}
// a lock is not a ship: no kill bounty for it (the power whose gate it is pays the breaker)
{const o=payKill;payKill=function(e){if(e&&e.role==='glock')return;return o.apply(this,arguments)}}
