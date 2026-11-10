//@src 16zzzi_escort.js
// ============================================================ Beyond: formation flying, and miners hiring guards (user, 8 Nov 2026)
// "When targeting the ship you're escorting there should be an autopilot that puts you in formation with that craft so that
// you both jump simultaneously and move across a sector together. Only breaking when there's enemy fighters or another
// mission you'd rather take." And: "All miner pilots should be able to hire a guard/escort especially if they are going into
// deep space or unfriendly space", paid in time while it mines (a miner may not jump).
//   Formation: the host marks, for each pilot, the ship it is escorting or guarding in that pilot's system (P.fmE, its entity
//     id; it reaches a guest in the pilot record). Target that ship and press J (autopilot): you hold a slot off its side and
//     match its speed. When it jumps (it reaches its gate, or vanishes there) and you are within 1.6 km, you jump with it, and
//     on arrival you fall back in on it. Steering or thrust breaks off; so do hostile fighters within 2.5 km of you or it
//     (they are targeted for you). Press J on it again to fall back in.
//   The escorted freighter jumps when it reaches its gate if its escort is within 1.6 km (no wait for the galaxy's clock), so
//     the two arrive together.
//   Guard jobs: an independent miner setting off to mine in, or through, deep space, Brood or pirate borders, or a power's
//     space where it isn't welcome, hires a guard if it can afford one (at least 400 cr above its reserve). The job (Jobs,
//     within 3 jumps) pays 150 cr for each jump it makes with you in the system it leaves or enters and 50 cr for each minute
//     you are within 2.5 km while it mines, paid as you go from its purse, up to the sum it set aside (the trip's estimate).
//     With a pilot within 3 jumps it waits at its freeport 90 s for a taker, and up to 4 minutes for a guard who signed on.
//     The job ends when it docks again (or is shot down).
const IGD={jump:150,min:50,wait:90,waitG:240,minCap:400,near:3,reach:2500};
const FMN={side:150,up:35,back:110,far:900,jump:1600,gate:700,hostR:2500,after:25000};
const FM_V={f:{x:0,y:0,z:0},r:{x:0,y:0,z:0},u:{x:0,y:0,z:0}};
let IG_GO=false,FM_AFTER=0,FM_HT=0;
function igOn(){return!!(S&&!S.training&&!S.unb&&S.ind)}
function sameK(a,b){return a===b||(isMe(a)&&isMe(b))}
// ---- guard jobs: when a miner hires
function igWhy(I,to){const p=indPath(I,I.sector,to);let deep=0,bad=0,unf=0;
  for(const s of p){if(DEF[s]&&DEF[s].kind==='deep')deep=1;if(indDanger(s)>0)bad=1;const o=sectorOwner(s);if(o==='pirate'||o==='brood'||(FAC_IDS.includes(o)&&(I.stand[o]||0)<=STAND.dock))unf=1}
  return bad?'past the Brood or a pirate den':unf?'through unfriendly space':deep?'into deep space':''}
function igMins(I){return Math.ceil(indCargo(I)*IND.fill/(IND.mineT[I.cls]||3))}
function igCap(I,to){const h=indHops(I.sector,to),est=2*Math.max(1,h)*IGD.jump+igMins(I)*IGD.min;return Math.max(0,Math.min(est,Math.floor(indPurse(I)-IND.reserve)))}
function igNear(sid){return allPilots().some(P=>P&&P.sector&&HOP[P.sector]&&HOP[P.sector][sid]!=null&&HOP[P.sector][sid]<=IGD.near)}
{const o=indGo;indGo=function(I,k,to,extra){
  if(!IG_GO&&k==='mine'&&I&&I.role==='miner'&&igOn()&&!NET.cl&&!I.hire){const why=igWhy(I,to),cap=why?igCap(I,to):0;
    if(why&&cap>=IGD.minCap){const wait=igNear(I.sector);I.hire={to,x:extra||{},why,cap,T:S.T,st:wait?'wait':'out'};
      for(const P of allPilots()){const h=HOP[P.sector]&&HOP[P.sector][I.sector];if(h!=null&&h<=IGD.near)keyFeed(pkeyOf(P),`📋 ${I.name}, an independent miner in ${DEF[I.sector].name}, is hiring a guard for a trip ${why} (Jobs).`,'info')}
      if(wait){I.st='dock';return}}}
  return o.apply(this,arguments)}}
// a miner waiting for its guard makes no other plans
{const o=indPlan;indPlan=function(I){if(I&&I.hire&&I.hire.st==='wait')return;return o.apply(this,arguments)}}
function igDepart(I){const H=I.hire;H.st='out';IG_GO=true;try{indGo(I,'mine',H.to,H.x)}finally{IG_GO=false}}
function igEnd(I,why){const G=I.guard;if(G){if(why)keyFeed(G.k,why,'bad');else keyFeed(G.k,`✔ Guard job done: ${I.name} is docked at ${DEF[I.sector].name}. You were paid ${fmt(G.paid)} cr in all.`,'good')}I.guard=null;I.hire=null}
function igStep(I){const H=I.hire;if(!H)return;const G=I.guard;
  if(I.st==='down'){igEnd(I,`✖ ${I.name}, the miner you were guarding, was shot down.${G&&G.paid?` You were paid ${fmt(G.paid)} cr.`:''}`);return}
  if(H.st==='wait'){if(I.st!=='dock'){igEnd(I,`${I.name} changed its plans: the guard job is off.`);return}
    if((G&&pSect(G.k)===I.sector)||S.T-H.T>=(G?IGD.waitG:IGD.wait))igDepart(I)}}
{const o=indTick;indTick=function(){const r=o.apply(this,arguments);try{if(igOn()&&!NET.cl)for(const I of indAll())igStep(I)}catch(e){console.error(e)}return r}}
// home again (or delivered its ore): the trip, and the job, are over
{const o=indArrive;indArrive=function(I){const H=I&&I.hire,k=I&&I.run&&I.run.k;const r=o.apply(this,arguments);try{if(H&&H.st==='out'&&k&&k!=='mine')igEnd(I)}catch(e){console.error(e)}return r}}
function igPay(I,n,what){const G=I.guard,H=I.hire;if(!G||!H)return;const amt=Math.min(n,H.cap-G.paid,Math.floor(indPurse(I)-IND.reserve/2));
  if(amt<=0){if(!G.capped){G.capped=1;keyFeed(G.k,`${I.name} has paid all it set aside for a guard (${fmt(G.paid)} cr).`,'warn')}return}
  const got=payKey(G.k,indW(I),amt);G.paid+=got;if(got>0)keyFeed(G.k,`🛡 +${fmt(got)} cr from ${I.name} (${what}).`,'good')}
function igTake(P,id){const I=indById(id);if(!I||!I.hire||I.st==='down')return'That miner no longer needs a guard.';if(I.guard)return`${I.name} already has a guard.`;
  const k=pkeyOf(P);fmClear(k);I.guard={k,name:P.name||'a pilot',paid:0,acc:0,ls:I.sector,T0:S.T};if(I.sector!==P.sector)P.route=I.sector;
  return`✓ You're guarding ${I.name}: ${IGD.jump} cr for each jump with it and ${IGD.min} cr a minute while it mines, up to ${fmt(I.hire.cap)} cr.${I.hire.st==='wait'?` It waits for you at ${DEF[I.sector].name}.`:''} Target it and press ${kb('autopilot')} to fly in formation.`}
function fmClear(k){for(const t of S.traders||[])if(t.esc&&sameK(t.esc.k,k))t.esc=null;for(const I of indAll())if(I.guard&&sameK(I.guard.k,k))I.guard=null}
// signing on to escort a convoy or a maker's flight ends a guard job
{const o=cvSign;cvSign=function(t,k){try{for(const I of indAll())if(I.guard&&sameK(I.guard.k,k))I.guard=null}catch(e){}return o.apply(this,arguments)}}
{const o=dockAction;dockAction=function(act,arg){if(act==='igtake'){if(NET.cl)return o.apply(this,arguments);dockErr=igTake(S.player,arg);return}return o.apply(this,arguments)}}
// the Jobs board: guard jobs for miners within 3 jumps
{const o=jobsList;jobsList=function(c,P,srcs){const out=o.apply(this,arguments);try{if(!igOn()||!c||c.kind!=='station')return out;const me=pkeyOf(P),hop=sid=>HOP[P.sector]&&HOP[P.sector][sid]!=null?HOP[P.sector][sid]:0,far=n=>n?`${n} jump${n>1?'s':''}`:'here';
  for(const I of indAll()){const H=I.hire;if(!H||I.st==='down')continue;const G=I.guard,mine=G&&sameK(G.k,me);if(G&&!mine)continue;const j=hop(I.sector);if(j>IGD.near)continue;
    const where=H.st==='wait'?`waiting at ${esc(DEF[I.sector].name)}`:I.st==='work'?`mining in ${esc(DEF[I.sector].name)}`:`now in ${esc(DEF[I.sector].name)}`,left=Math.max(0,H.cap-(G?G.paid:0));
    out.push({id:'igd:'+I.id,by:'ind_'+I.id,sid:I.sector,ty:'fight',title:`Guard: ${esc(I.name)}'s ${esc(CLASSES[I.cls].name)}, mining ${esc(DEF[H.to].name)}`,
      sub:mine?`your job · paid ${fmt(G.paid)} of up to ${fmt(H.cap)} cr · ${where}`:`going ${esc(H.why)} · ${where} · up to ${fmt(H.cap)} cr`,hops:j,where:far(j),payN:left,pay:`${IGD.jump} cr a jump · ${IGD.min} cr a min`,
      btn:mine?(I.sector!==P.sector?['croute',I.sector,'Set course']:null):['igtake',I.id,'Take the job'],
      detail:()=>`<p class="note" style="margin:0">${esc(I.name)}, an independent miner, is going ${esc(H.why)} to mine ${esc(DEF[H.to].name)} and is hiring a guard. Fly with it: ${IGD.jump} cr for each jump it makes with you in the system it leaves or enters, and ${IGD.min} cr for each minute you stay within ${(IGD.reach/1000).toFixed(1)} km while it mines, paid as you go from its own purse, up to ${fmt(H.cap)} cr. Target it and press ${kb('autopilot')} to fly in formation: you jump when it jumps.${H.st==='wait'?` It waits at ${esc(DEF[I.sector].name)} a few minutes for its guard.`:''}</p>`})}}catch(e){console.error(e)}return out}}
{const o=jbIssuer;jbIssuer=function(j){if(j&&typeof j.by==='string'&&j.by.startsWith('ind_')){const I=indById(j.by.slice(4));return I?`[I] ${I.name}`:"[I] an independent"}return o.apply(this,arguments)}}
{const o=sideCol;sideCol=function(s){if(typeof s==='string'&&s.startsWith('ind_'))return'#c9b98f';return o.apply(this,arguments)}}
// ---- the host, every frame: which ship each pilot is escorting (P.fmE), guard pay, and freighters that jump with their escort
function fmEntOf(k,sid){const w=WORLDS[sid];if(!w)return null;
  for(const t of S.traders||[])if(t.esc&&sameK(t.esc.k,k)&&t.sector===sid){const h=`trader:${t.id}:${t.side}`;return w.ents.find(x=>x.alive&&x.home===h)||null}
  for(const I of indAll())if(I.guard&&sameK(I.guard.k,k)&&I.sector===sid)return w.ents.find(x=>x.alive&&x.indId===I.id)||null;return null}
function fmHost(dt){if(NET.cl||!S||!S.player)return;FM_HT-=dt;const slow=FM_HT<=0;if(slow)FM_HT=.25;
  if(slow)for(const P of allPilots()){if(!P)continue;const e=P.docked?null:fmEntOf(pkeyOf(P),P.sector),id=e?e.id:null;if(P.fmE!==id)P.fmE=id}
  if(!igOn())return;
  for(const I of indAll()){const G=I.guard;if(!G||!I.hire)continue;
    if(G.ls!==I.sector){const ps=pSect(G.k);if(G.ls&&(ps===G.ls||ps===I.sector))igPay(I,IGD.jump,'a jump guarded');G.ls=I.sector}
    if(I.st==='work'&&I.live){const w=WORLDS[I.sector],GP=xPilotOfKey(G.k),me=w&&GP&&!GP.docked&&pilotEntIn(w,G.k),e=me&&w.ents.find(x=>x.alive&&x.indId===I.id);
      if(e&&d3(me,e)<IGD.reach){G.acc=(G.acc||0)+dt;if(G.acc>=60){G.acc-=60;igPay(I,IGD.min,'a minute guarding')}}}}}
{const o=step;step=function(dt){const r=o.apply(this,arguments);try{fmHost(dt)}catch(e){console.error(e)}return r}}
function trHopNow(t,e){returnHome(e);despawn(e);t.live=false;if(t.leg>=t.path.length-1)return;const prev=t.sector;t.leg++;t.sector=t.path[t.leg];t.next=S.T+TRADER_HOP;
  if(t.kind==='haul'){cvStep(t,prev);if(raidMeet(t,prev)){const i=S.traders.indexOf(t);if(i>=0)S.traders.splice(i,1);return}}
  if(WORLDS[t.sector])inW(WORLDS[t.sector],()=>spawnTrader(t,true))}
{const o=traderThink;traderThink=function(e,dt){const was=!!(e.ai&&e.ai.arrived);const r=o.apply(this,arguments);
  try{if(!was&&!NET.cl&&e.ai.arrived&&e.ai.dest&&e.ai.dest.type==='gate'){const t=e.tradeT;if(t&&t.esc&&(S.traders||[]).includes(t)){const pe=pilotEntIn(W,t.esc.k);if(pe&&d3(pe,e)<FMN.jump)trHopNow(t,e)}}}catch(err){console.error(err)}return r}}
// ---- the pilot's side (host and guest alike): formation flight
function fmEnt(){const id=S.player&&S.player.fmE;if(id==null||!W)return null;return W.ents.find(e=>e.alive&&e.type==='ship'&&String(e.id)===String(id))||null}
function fmName(E){let n='';try{n=E.pname||shipLabel(E)}catch(e){}return n||'your charge'}
function fmStart(E,quiet){W.fmn={ref:E,lx:E.x,ly:E.y,lz:E.z,name:fmName(E)};W.tgt={kind:'ship',ref:E};W.apSet=W.tgt;apOn=true;
  if(!quiet)flash(`Formation on ${W.fmn.name}: you'll jump when it jumps. Steer or thrust to break off.`)}
function fmMan(){return keys.KeyW||keys.KeyS||keys.KeyA||keys.KeyD||keys.ArrowLeft||keys.ArrowRight||keys.ArrowUp||keys.ArrowDown||touch.on||(mouse.in&&mouse.aim&&!mouse.free&&hyp(mouse.x-VW/2,mouse.y-VH/2)>Math.min(VW,VH)*.42*.25)}
function fmHostile(p,R){let b=null,bd=1e9;for(const o of W.ents){if(o.type!=='ship'||!o.alive||o.isPlayer||o===R||o.masked)continue;if(o.role==='miner'||o.role==='hauler'||o.role==='trader'||o.role==='builder')continue;if(!hostile('player',o.side))continue;
    const d=Math.min(d3(o,p),d3(o,R));if(d<FMN.hostR&&d<bd){bd=d;b=o}}return b}
function fmGate(F){let b=null,bd=FMN.gate;for(const g of GATES[W.sid]||[]){const d=hyp(g.x-F.lx,g.y-F.ly,g.z-F.lz);if(d<bd){bd=d;b=g}}return b}
function fmGone(p,F){W.fmn=null;apOn=false;const g=fmGate(F),d=hyp(F.lx-p.x,F.ly-p.y,F.lz-p.z);
  if(g&&d<FMN.jump&&!gateLocked(p)&&!S.gateDown[gateKey(W.sid,g.to)]){W.gc=null;W.gate=null;W.jump={to:g.to,t:0,g};p.inJump=true;W.tgt=null;SFX.jump();FM_AFTER=performance.now()+FMN.after;flash(`Jumping with ${F.name} to ${DEF[g.to].name}.`);return}
  flash(g?`${F.name} jumped out: you were too far behind to follow.`:`${F.name} has docked or gone. Formation off.`)}
function fmFly(p,dt){const F=W.fmn,R=F.ref;
  if(!R.alive||!W.ents.includes(R)||(R.ai&&R.ai.arrived&&R.ai.dest&&R.ai.dest.type==='gate')){fmGone(p,F);return false}
  F.lx=R.x;F.ly=R.y;F.lz=R.z;
  const H=fmHostile(p,R);if(H){W.fmn=null;apOn=false;W.tgt={kind:'ship',ref:H};flash(`Hostiles near ${F.name}: formation broken, ${fmName(H)} targeted. Target your charge and press ${kb('autopilot')} to fall back in.`,true);return false}
  qRot(R.q,0,0,1,FM_V.f);qRot(R.q,1,0,0,FM_V.r);qRot(R.q,0,1,0,FM_V.u);const f=FM_V.f,r=FM_V.r,u=FM_V.u;
  const sx=R.x+r.x*FMN.side+u.x*FMN.up-f.x*FMN.back,sy=R.y+r.y*FMN.side+u.y*FMN.up-f.y*FMN.back,sz=R.z+r.z*FMN.side+u.z*FMN.up-f.z*FMN.back,ex=sx-p.x,ey=sy-p.y,ez=sz-p.z,d=hyp(ex,ey,ez);
  if(d>FMN.far){const err=faceDir(p,ex,ey,ez,dt);if(err<.6)steer(p,sx,sy,sz,dt,false,1);else brake(p,dt*.4);p.thrusting=err<.6;return true}
  const cm=Math.min(d*.9,140)/(d||1);let vx=(R.vx||0)+ex*cm,vy=(R.vy||0)+ey*cm,vz=(R.vz||0)+ez*cm;const vm=hyp(vx,vy,vz),cap=p.st.maxSpd*1.15;if(vm>cap){vx*=cap/vm;vy*=cap/vm;vz*=cap/vm}
  const dvx=vx-p.vx,dvy=vy-p.vy,dvz=vz-p.vz,dv=hyp(dvx,dvy,dvz)||1,acc=Math.min(p.st.thrust*1.2,dv/dt);p.vx+=dvx/dv*acc*dt;p.vy+=dvy/dv*acc*dt;p.vz+=dvz/dv*acc*dt;p.thrusting=dv>25;
  if(d<300)faceDir(p,f.x,f.y,f.z,dt);else faceDir(p,ex,ey,ez,dt);return true}
{const o=autopilot;autopilot=function(p,dt){if(W&&W.fmn)return fmFly(p,dt);return o.apply(this,arguments)}}
{const o=toggleAutopilot;toggleAutopilot=function(){if(!apOn&&W&&!S.player.docked&&!W.dead&&W.tgt&&W.tgt.kind==='ship'&&!(W.player&&W.player.landed)){const E=fmEnt();if(E&&W.tgt.ref===E){fmStart(E);return}}
  if(apOn&&W)W.fmn=null;return o.apply(this,arguments)}}
// after a jump together: fall back in on it when it appears (unless you take the stick first)
{const o=playerUpdate;playerUpdate=function(dt){const r=o.apply(this,arguments);try{if(W&&W.fmn&&!apOn)W.fmn=null;
  if(FM_AFTER){if(performance.now()>FM_AFTER||fmMan()||S.player.docked)FM_AFTER=0;else if(!apOn&&W&&!W.jump&&!W.dead){const E=fmEnt();if(E){FM_AFTER=0;fmStart(E,true);flash(`Back in formation on ${W.fmn.name}.`)}}}}catch(e){console.error(e)}return r}}
// ---- your charge targeted for you (user, 9 Nov 2026: "when taking guard missions [or escort] it would be helpful to target
// the ship being guarded when you're in the same sector"). In the same system as the ship you guard or escort, it becomes your
// target as you arrive (or undock, or take the job there), with a note on the formation key; and whenever you have no target
// at all (a hostile you were fighting is dead), it is targeted again. A target you pick yourself is left alone.
{const o=hudUpdate;hudUpdate=function(){const r=o.apply(this,arguments);try{if(!W||!W.player||S.player.docked){if(W)W.fmAuto=null;return r}if(W.dead||W.fmn)return r;const E=fmEnt();if(!E)return r;
  if(W.fmAuto!==E.id){W.fmAuto=E.id;if(!W.tgt||!W.tgt.ref||!(W.tgt.kind==='ship'&&W.tgt.ref.alive&&hostile('player',W.tgt.ref.side))){W.tgt={kind:'ship',ref:E};flash(`${fmName(E)} targeted: the ship you're ${E.indId!=null?'guarding':'escorting'}. Press ${kb('autopilot')} to fly in formation.`)}}
  else if(!W.tgt||(W.tgt.ref&&W.tgt.ref.alive===false))W.tgt={kind:'ship',ref:E}}catch(e){}return r}}
