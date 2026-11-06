//@src 16zd_fall.js
// ============================================================ when your base falls: the power captures it or destroys it (Beyond, 3 Nov 2026)
// The design (section 9, decided 2 Nov): the AI that takes one of your Lairs, Depots or Stations decides whether to capture it,
// gaining it at least 75% intact with its buildings and stores, or destroy it, so everything there is lost. A captured base
// can be taken back; a destroyed one is gone.
// - Depots and Stations: whichever way the power broke it (assault ships, a siege, or guns alone) its leader chooses. Stations
//   are worth keeping more than depots; Ruthless leaders destroy; Ambitious, Mercantile, Industrious and Opportunist ones keep;
//   a base far from the power's own space is harder to hold, so more often destroyed. Captured: it flies the power's flag at
//   75-90% hull with its buildings, its store (all but up to a quarter, lost in the fighting as debris) and its modules, and
//   holds the system for that power; your crews leave, your market orders lapse, your vault there stays yours. Destroyed:
//   Driftgate 1's raze (everything spills or drifts).
// - Taking it back: break a captured base's hull yourself and its old hands open the doors: it's yours again, its store with it,
//   at a third of its hull.
// - Lairs: a power that wears one down impounds it (the stash, less up to a quarter, into its stores; the Lair is shut) or
//   destroys it (the stash drifts as salvage). An impounded Lair isn't a base the power can use, so it can't be taken back.
// Ledger: goods only move (store to store, or into debris).
const FALL={keep:[.75,.9],lose:.25,back:.33,cap:{station:.85,depot:.55},far:.3,keepT:['Ambitious','Mercantile','Industrious','Opportunist'],razeT:['Ruthless'],lair:.5};
function fallTr(f,x){const L=leaderOf(f);return!!(L&&L.traits.includes(x))}
function fallChoice(R,side,lair){if(!FAC_IDS.includes(side))return'raze';if(FALL.razeT.some(t=>fallTr(side,t)))return'raze';
  let p=lair?FALL.lair:R.pst?FALL.cap.station:FALL.cap.depot;if(FALL.keepT.some(t=>fallTr(side,t)))p+=.2;if(fallTr(side,'Vengeful'))p-=.15;
  const sid=lair?R.sid:R.sid,T=territory(side);if(!lair&&!(T.has(sid)||NEIGH[sid].some(s=>T.has(s))))p-=FALL.far;return Math.random()<p?'capture':'raze'}
function fallKind(R){return R.pst?'Station':'Depot'}
// the station entity in a live system is swapped for one in its new colours (as Driftgate 1's capture does)
function fallSwap(sid,R,side){const w=WORLDS[sid];if(!w)return;inW(w,()=>{const E=W.stationEnt;if(E&&E.rec===R){if(W===LW&&S.player.docked==='station')undock();if(NET.host)netKickDocked(sid,'station',side);fxBoom(E,200,sideCol(side));const i=W.ents.indexOf(E);if(i>=0)W.ents.splice(i,1);W.stationEnt=null;const N=addStationEnt(R);N.shield=0;N.offline=W.t+20;if(W.tgt&&W.tgt.ref===E)W.tgt={kind:'station',ref:N}}})}
function fallCapture(R,side){const sid=R.sid,s=S.sectors[sid],pid=R.pid||'me',kind=fallKind(R),lost={};
  for(const k in R.stock){const m=Math.floor((R.stock[k]||0)*rnd(0,FALL.lose));if(m>0)lost[k]=inv.take(R.stock,k,m)}toDebris(s,lost);
  R.was={pid,name:R.name,pst:!!R.pst,T:S.T};const nCrew=(R.crew||[]).length;R.crew=[];R.sell={};R.buy={};delete R.pid;
  R.owner=side;R.name=`${FACTIONS[side].short} ${R.pst?'station':'depot'} (taken) · ${DEF[sid].name}`;inv.addAll(dStore(R),R.stock);R.stock={};
  R.hull=Math.round(R.hMax*rnd(FALL.keep[0],FALL.keep[1]));R.shield=0;if(S.distress)S.distress=S.distress.filter(d=>d.sid!==sid);
  keyFeed(pid,`✕ ${FACTIONS[side].short} has captured your ${kind} in ${DEF[sid].name}, with its buildings and ${fmt(invMass(dStore(R)))} t of its store.${nCrew?` Your ${nCrew} crew${nCrew>1?'s':''} left.`:''} Break its hull yourself to take it back.`,'bad');
  if(covered(sid)&&!isMe(pid))feed(`${FACTIONS[side].short} captured a contractor's ${kind.toLowerCase()} in ${DEF[sid].name}.`,'news');
  chron&&chron(`${FACTIONS[side].short} captured a contractor's ${kind.toLowerCase()} in ${DEF[sid].name}.`,'',[side]);fallSwap(sid,R,side)}
function fallRetake(R,P){const sid=R.sid,W0=R.was;R.owner='player';if(W0.pid&&W0.pid!=='me')R.pid=W0.pid;else delete R.pid;R.name=W0.name;inv.addAll(R.stock,dStore(R));R.store={};
  R.hull=Math.round(R.hMax*FALL.back);R.shield=0;R.crew=[];delete R.was;keyFeed(W0.pid||'me',`✓ Your ${fallKind(R)} in ${DEF[sid].name} is yours again: its old hands opened the doors. ${fmt(invMass(R.stock))} t in its store.`,'good');
  chron&&chron(`A contractor took back their ${fallKind(R).toLowerCase()} in ${DEF[sid].name}.`);fallSwap(sid,R,'player')}
// a power breaks your base: its leader chooses
{const o=captureDepot;captureDepot=function(sid,side){const R=S.stations[sid];if(R&&R.was&&FAC_IDS.includes(R.owner)&&side==='player'&&!S.unb)return fallRetake(R);if(R&&R.owner==='player'&&!S.unb){const sd=sideNorm(side);if(FAC_IDS.includes(sd)){if(fallChoice(R,sd)==='raze'){R._fallR=1;return razeStation(sid,sd)}return fallCapture(R,sd)}}return o.apply(this,arguments)}}
{const o=razeStation;razeStation=function(sid,by){const R=S.stations[sid];if(R&&!S.unb){
    if(R.owner==='player'&&R.kind==='depot'&&!R._fallR){const sd=sideNorm(by);if(FAC_IDS.includes(sd)&&fallChoice(R,sd)==='capture')return fallCapture(R,sd)}
    if(R.was&&FAC_IDS.includes(R.owner)&&by==='player')return fallRetake(R)}
  return o.apply(this,arguments)}}
// your Lair, worn down by a power that found it: impounded or destroyed (replaces stage 9's lairWorldB)
lairWorldB=function(dt){const Ls=(S.lairs||[]).filter(L=>L.sid===W.sid&&L.hull>0);if(!Ls.length)return;
  for(const L of Ls){const O=lairOwner(L);if(!O)continue;if(L.build&&S.T>=L.build){L.build=0;keyFeed(L.pid,`⛏ Your Lair in ${DEF[L.sid].name} is ready: dock with E nearby.`,'good')}let by=null;
    for(const e of W.ents){if(e.type!=='ship'||!e.alive||!FAC_IDS.includes(e.side)||!e.npc)continue;if(!pilotHostile(O,e.side))continue;
      if(e.role==='scout'&&!L.seen[e.side]&&d3(e,L)<LAIR_B.seeR){L.seen[e.side]=1;keyFeed(L.pid,`⚠ A ${FACTIONS[e.side].short} scout has found your Lair in ${DEF[W.sid].name}. Their ships will attack it on sight.`,'bad')}
      if(L.seen[e.side]&&d3(e,L)<2500){L.hull-=6*dt;by=e.side}}
    if(L.hull<=0){const s=S.sectors[W.sid],imp=by&&fallChoice(L,by,true)==='capture';let msg;
      if(imp){const lost={};for(const k in L.stash){const m=Math.floor((L.stash[k]||0)*rnd(0,FALL.lose));if(m>0)lost[k]=inv.take(L.stash,k,m)}toDebris(s,lost);const t=invMass(L.stash);{const sh={...L.stash};for(const k in sh)inv.take(L.stash,k,sh[k]);frShip(by,W.sid,sh,'plunder','plunder')}
        msg=`✕ ${FACTIONS[by].short} has impounded your Lair in ${DEF[W.sid].name}: ${fmt(t)} t of its stash went into their stores.`}
      else{if(Object.keys(L.stash).length)s.crates.push({id:S.nextId++,x:L.x,y:L.y,z:L.z,inv:L.stash,until:S.T+600});msg=`✕ Your Lair in ${DEF[W.sid].name} was destroyed. Its stash is drifting as salvage.`}
      toDebris(s,L.fort||{});L.stash={};L.fort={};L.lt=[];S.lairs=S.lairs.filter(x=>x!==L);if(!MUTE)fxBoom(L,260,'#ffcf5a');keyFeed(L.pid,msg,'bad');lairEvict(L)}}}
// the captured base shows whose it was
{const o=dockCtx;dockCtx=function(){const c=o.apply(this,arguments);try{const R=S.player&&S.stations[S.player.sector];if(c&&c.kind==='station'&&R&&R.was&&FAC_IDS.includes(R.owner))c.sub+=` · captured from a contractor`}catch(e){}return c}}
