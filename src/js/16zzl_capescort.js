//@src 16zzl_capescort.js
// ============================================================ capital escorts ride the jump; the carrier's defence set (user, 6 Nov 2026)
// A capital ship's own fighter escort docks on it once its jump drive passes 75% of the spin-up, and jumps with it:
//  - fighters given a Guard or Escort order on a capital (from its bridge) fly to a berth on its hull and hold there, guns
//    cold; if the spin-up is broken they undock and fight again. When it jumps they go with it (their load rides in the
//    capital's hold, so the ledger stays exact) and undock beside it in the next system, their order still running;
//  - a carrier's own craft (its wings, except any out on a strike next door, and its defence set) fly home and land.
// Freighters and other ships a capital is escorting are not its escort: they stay behind.
// Every power's and pilot's carrier also carries a defence set: five fighters (one heavy, two medium, two light) and a
// scout, built from the same deck kits as its wings (plate and coil, aboard, so the ledger stays exact). They only escort
// the carrier and take no other orders. They wait docked until a threat is realised (a hostile ship within 4.5 km, fire on
// the carrier, or a missile or torpedo coming at it), launch, fight within 1.5 km of it, and land again once it has been
// clear for 20 seconds. The scout has two jobs of its own in the carrier's system: it flips the beacon (or re-secures its
// side's fading one) when it isn't locked, and it plants its limpet on an enemy capital attacking the carrier, then rearms
// aboard. Lost craft are replaced like the wings': from the faction's stores when the carrier refits, or by its fabricator.
// The Brood's Hive Ships and the Unbound's Ravager have no defence set.
const CAPJ={dock:.75,threatR:4500,defR:1500,clear:20,launchGap:.35,set:['heavy','striker','striker','interceptor','interceptor','scout'],hullGap:60};
function capSpin(M){const t=M&&M.tok;return!!(t&&t.spin&&t.spin.p>=CAPJ.dock)}
function capIs(T){return!!(T&&T.role==='frigate'&&T.tok&&T.alive)}
// ---- escorts ordered onto a capital: a berth on its hull while the drive spins past 75%
function capBerth(T,n){const R=T.st.radius,k=[[.55,.32,.1],[-.55,.32,.1],[.4,.38,-.45],[-.4,.38,-.45]][n%4];qRot(T.q,k[0]*R,k[1]*R,k[2]*R,_u);return{x:T.x+_u.x,y:T.y+_u.y,z:T.z+_u.z}}
{const o=orderThink;orderThink=function(e,dt){const O=e.order,T=O&&O.tgt;
  if(!NET.cl&&O&&(O.kind==='guard'||O.kind==='escort')&&capIs(T)&&W.ents.includes(T)&&W.t<=O.until){
    if(capSpin(T)){const B=capBerth(T,O.slot||0);
      if(e.hullRide===T||d3(e,B)<CAPJ.hullGap){e.hullRide=T;e.x=B.x;e.y=B.y;e.z=B.z;e.vx=T.vx;e.vy=T.vy;e.vz=T.vz;qCopy(e.q,T.q);e.thrusting=e.boosting=false;e.ai.tgt=null;return true}
      e.hullRide=null;holdSlot(e,T,B.x,B.y,B.z,dt,2.2);faceTo(e,B,dt);e.ai.tgt=null;return true}
    if(e.hullRide)e.hullRide=null}
  return o.apply(this,arguments)}}
// the jump: escorts on the hull go with it; their load rides in the capital's hold
{const o=despawnFrigate;despawnFrigate=function(e){try{const t=e&&e.tok;if(t&&!NET.cl){
      for(const r of W.ents.slice()){if(r.hullRide!==e||!r.alive||!r.order)continue;const O=r.order;
        (t.riders=t.riders||[]).push({cls:r.cls,side:r.side,fac:r.fac,tier:r.tier||1,home:r.home,role:r.role,kind:O.kind,left:Math.max(0,O.until-W.t),pid:O.pid||null,slot:O.slot||0,by:O.by,ld:{...r.load},cg:{...(r.cargo||{})},hull:r.hull,shield:r.shield});
        inv.addAll(t.load,r.load);inv.addAll(t.load,r.cargo||{});r.load={};r.cargo={};r.alive=false;const i=W.ents.indexOf(r);if(i>=0)W.ents.splice(i,1);if(W.tgt&&W.tgt.ref===r)W.tgt=null}
      if(isCar(t)&&capDefOK(t)){t.def=capDefNow(e);for(const p of(e.dfl||[]))if(p.alive&&W.ents.includes(p))despawn(p);e.dfl=[];e.dbay=[]}}}catch(err){frameErr('capital escorts',err)}
  return o.apply(this,arguments)}}
{const o=spawnFrigate;spawnFrigate=function(t,arrive){const e=o.apply(this,arguments);try{if(e&&!NET.cl){
      if(t.riders&&t.riders.length){const L=t.riders;t.riders=[];for(const R of L){const ld={},cg={};for(const k in R.ld){const m=Math.min(R.ld[k],e.load[k]||0);if(m>0)ld[k]=inv.take(e.load,k,m)}for(const k in R.cg){const m=Math.min(R.cg[k],e.load[k]||0);if(m>0)cg[k]=inv.take(e.load,k,m)}
          const r=makeNPC(R.role||'patrol',R.side,R.cls,R.tier,ld,R.home);r.fac=R.fac||r.fac;r.cargo=cg;if(R.hull)r.hull=Math.min(r.st.hull,R.hull);if(R.shield!=null)r.shield=Math.min(r.st.sCap,R.shield);
          const B=capBerth(e,R.slot);r.x=B.x;r.y=B.y;r.z=B.z;qCopy(r.q,e.q);r.order={kind:R.kind,tgt:e,until:W.t+Math.max(30,R.left),slot:R.slot,by:R.by,pid:R.pid};W.ents.push(r)}}
      if(isCar(t)&&capDefOK(t)){e.dbay=(t.def||[]).slice();t.def=[];e.dfl=[];e.defT=-1e9}}}catch(err){frameErr('capital escorts',err)}return e}}
// ---- the carrier's own craft land before it jumps
{const o=droneThink;droneThink=function(e,dt){const M=e.mom;
  if(e.def){defThink(e,dt);return}
  if(!NET.cl&&e.role==='flight'&&M&&M.alive&&W.ents.includes(M)&&capSpin(M)&&e.mis!=='sortie'){const d=d3(e,M);if(d<M.st.radius+110){carStow(M,e);return}steer(e,M.x,M.y,M.z,dt,true);faceTo(e,M,dt);e.thrusting=true;return}
  return o.apply(this,arguments)}}
// ---- the defence set
function capDefOK(t){return!!t&&isCar(t)&&t.side!=='brood'&&t.side!=='pirate'}
function capDefSide(t){if(t.side==='player'||t.owner){const P=t.owner&&S.pilots&&S.pilots[t.owner]||S.player;return intelFor(P)}return FAC_IDS.includes(t.side)?t.side:null}
function capDefBy(t){return t.owner||(t.side==='player'?'me':null)}
// what a carrier has of its set: aboard plus flying (live), or listed on the token
function capDefNow(e){return(e.dbay||[]).concat((e.dfl||[]).filter(p=>p.alive&&W.ents.includes(p)).map(p=>p.cls))}
function capDefHave(t){if(t.live){const e=carEnt(t);if(e)return capDefNow(e)}return t.def||[]}
function capDefMissing(t){const have=capDefHave(t).slice(),out=[];for(const c of CAPJ.set){const i=have.indexOf(c);if(i>=0)have.splice(i,1);else out.push(c)}return out}
function capDefKit(c){return carKit(c)}
// filled from the faction's (or pilot's) stores when the carrier refits, like its wings
function capDefFill(t,srcs){if(!capDefOK(t))return;for(const c of capDefMissing(t)){const kit=capDefKit(c);if(!takeFrom(kit,srcs))break;if(t.live&&carEnt(t)){const e=carEnt(t);inv.addAll(e.load,kit);(e.dbay=e.dbay||[]).push(c)}else{inv.addAll(t.load,kit);(t.def=t.def||[]).push(c)}}}
{const o=capRefill;capRefill=function(t){const r=o.apply(this,arguments);try{if(capDefOK(t)){const f=t.side==='player'?sideNorm('player'):t.side,own=carOwned(t),st=own&&S.pilots&&S.pilots[t.owner]?S.pilots[t.owner].vault:S.econ.stock[f];if(st)capDefFill(t,own?[st]:[S.econ.fleet[f],st].filter(Boolean))}}catch(err){console.error(err)}return r}}
// a carrier delivered fully loaded (the developer spawn) comes with its set too
{const o=carFullLoad;carFullLoad=function(t){const r=o.apply(this,arguments);try{if(capDefOK(t)){t.def=[];for(const c of CAPJ.set){t.def.push(c);inv.addAll(t.load,capDefKit(c))}}}catch(err){console.error(err)}return r}}
// the fabricator replaces a lost defence craft before anything else
{const o=carTick;carTick=function(){try{if(!NET.cl)for(const t of S.frigates){if(!capDefOK(t)||carOwned(t)||t.hull<=0)continue;t.store=t.store||{};
      if(t.fab&&t.fab.def&&S.T>=t.fab.until){const fb=t.fab;t.fab=null;const e=t.live&&carEnt(t);if(e){inv.addAll(e.load,fb.kit);(e.dbay=e.dbay||[]).push(fb.cls)}else{inv.addAll(t.load,fb.kit);(t.def=t.def||[]).push(fb.cls)}}
      if(!t.fab){const miss=capDefMissing(t);if(miss.length){const c=miss[0],kit=capDefKit(c);if(haveIn(kit,[t.store])){takeFrom(kit,[t.store]);t.fab={cls:c,kit,until:S.T+BAL.carFab,def:1}}}}}}catch(err){console.error(err)}
  return o.apply(this,arguments)}}
// what the carrier asks its faction for includes the set's kits
{const o=carWant;carWant=function(t){const w=o.apply(this,arguments);try{if(capDefOK(t))for(const c of capDefMissing(t)){const k=capDefKit(c);for(const x in k)w[x]=(w[x]||0)+k[x]}}catch(err){}return w}}
// a threat to the carrier: a hostile ship within 4.5 km, fire on it, a missile or torpedo coming at it
function capThreat(M){if(W.t-(M.lastHit||-1e9)<3&&M.lastHitBy&&hostile(M.side,M.lastHitBy))return true;
  for(const m of W.missiles)if(m.tgt===M&&hostile(M.side,m.side))return true;
  for(const o of W.ents){if(o.type!=='ship'||!o.alive||o===M||o.role==='limpet'||o.role==='drone'||!hostE(M.side,o))continue;if(o.isPlayer&&(S.player.docked||W.dead))continue;if(mHid(o,M))continue;if(d3(o,M)<CAPJ.threatR)return true}return false}
// an enemy capital attacking the carrier, with no limpet of ours on it yet
function capAttacker(M,f){for(const o of W.ents){if(o.role!=='frigate'||!o.alive||o===M||!hostE(M.side,o))continue;const R=o.tok;if(R&&R.pings&&R.pings[f]&&R.pings[f].until>S.T)continue;
    if(d3(o,M)<6000&&((W.t-(M.lastHit||-1e9)<10&&M.lastHitBy===o.side)||o.lanceT===M||d3(o,M)<3200))return o}return null}
function capBeaconJob(M,f){const B=S.beacons&&S.beacons[W.sid];if(!B||!f)return null;if(B.owner===f&&bcnState(B)==='locked')return null;return bcnCan(B,f)?B:null}
function defLaunch(M,cls){const ld=capDefKit(cls),got={};for(const k in ld){const m=Math.min(ld[k],M.load[k]||0);if(m>0)got[k]=inv.take(M.load,k,m)}
  const p=makeNPC('flight',M.side,cls,factionTier(M.fac),got,M.home);p.fac=M.fac;p.mom=M;p.def=1;p.wg='D';p.limpet=isScoutCls(cls)?1:0;p.ai.orb=Math.random()*TAU;p.x=M.x;p.y=M.y-M.st.radius*.3;p.z=M.z;qCopy(p.q,M.q);(M.dfl=M.dfl||[]).push(p);W.ents.push(p);return p}
function defStow(M,p){inv.addAll(M.load,p.load||{});p.load={};const i=W.ents.indexOf(p);if(i>=0)W.ents.splice(i,1);p.alive=false;M.dfl=(M.dfl||[]).filter(x=>x!==p);(M.dbay=M.dbay||[]).push(p.cls);if(W.tgt&&W.tgt.ref===p)W.tgt=null}
function defHome(e,M,dt){const d=d3(e,M);if(d<M.st.radius+110){defStow(M,e);return}steer(e,M.x,M.y,M.z,dt,true);faceTo(e,M,dt);e.thrusting=true}
function defThink(e,dt){const M=e.mom;if(NET.cl)return;if(!M||!M.alive||!W.ents.includes(M)){e.def=0;e.role='leave';e.mom=null;return}
  if(capSpin(M)){defHome(e,M,dt);return}
  const t=M.tok,f=t&&capDefSide(t),ai=e.ai;
  if(isScoutCls(e.cls)){
    if(e.limpet){const E=f&&capAttacker(M,f);if(E){const d=d3(e,E);if(d<lpRad(E)+140){if(limpetPlant(E,f,capDefBy(t),e))e.limpet=0}else{steer(e,E.x,E.y,E.z,dt,false,1.1);faceTo(e,E,dt);e.thrusting=true;e.boosting=d>1500}return}}
    const B=capBeaconJob(M,f);if(B){e.bcnJob=1;const d=d3(e,B);if(d>BCN_R*.5){steer(e,B.x,B.y,B.z,dt,true);faceTo(e,B,dt);e.thrusting=true}else{e.vx*=.9;e.vy*=.9;e.vz*=.9;e.thrusting=false}return}
    e.bcnJob=0;defHome(e,M,dt);return}
  // fighters: the threat nearest the carrier, within 1.5 km of it
  if(ai.t<=0||!(ai.tgt&&ai.tgt.alive&&W.ents.includes(ai.tgt))||d3(ai.tgt,M)>CAPJ.defR*1.3){ai.t=.4+rnd(.3);ai.tgt=threatTo(M,e,CAPJ.defR)}
  if(ai.tgt){fight(e,ai.tgt,dt);return}
  if(W.t-(M.defT||-1e9)>CAPJ.clear){defHome(e,M,dt);return}
  ai.orb=(ai.orb||0)+dt*.35;const R=M.st.radius+220,a=ai.orb;holdSlot(e,M,M.x+Math.cos(a)*R,M.y+Math.sin(a*1.3)*30,M.z+Math.sin(a)*R,dt,2);const rv=hyp(e.vx,e.vy,e.vz);if(rv>15)faceDir(e,e.vx,e.vy,e.vz,dt)}
// the carrier decides: launch on a threat, the scout for its jobs, nothing while the drive is past 75%
{const o=frigateThink;frigateThink=function(e,dt){const r=o.apply(this,arguments);try{const t=e.tok;if(!NET.cl&&e.alive&&t&&capDefOK(t)&&W.ents.includes(e)&&!capSpin(e)){
      e.dbay=e.dbay||[];e.dfl=e.dfl||[];const f=capDefSide(t);
      if(capThreat(e))e.defT=W.t;const hot=W.t-(e.defT||-1e9)<1;
      if(W.t>=(e.defLT||0)&&e.dbay.length){let i=-1;
        if(hot)i=e.dbay.findIndex(c=>!isScoutCls(c));
        if(i<0){const si=e.dbay.findIndex(c=>isScoutCls(c));if(si>=0&&f&&(capBeaconJob(e,f)||capAttacker(e,f)))i=si}
        if(i>=0){const c=e.dbay.splice(i,1)[0];defLaunch(e,c);e.defLT=W.t+CAPJ.launchGap}}}}catch(err){frameErr('defence set',err)}return r}}
// the scout counts as a beacon flipper for its side
{const o=bcnFlipper;bcnFlipper=function(e){if(e&&e.def&&e.bcnJob&&e.alive&&isScoutCls(e.cls)&&e.mom&&e.mom.tok){const f=capDefSide(e.mom.tok);if(f)return{side:f,by:capDefBy(e.mom.tok)}}return o.apply(this,arguments)}}
// the Hangar console: a line for the defence set
function capDefLine(e){const fly=(e.dfl||[]).filter(p=>p.alive&&W.ents.includes(p)),miss=capDefMissing(e.tok);return`<p class="note" style="margin:8px 0 0">Defence set: ${(e.dbay||[]).length} aboard, ${fly.length} flying${miss.length?`, ${miss.length} to replace`:''}. They escort this carrier only, launch when a threat comes within 4.5 km (or it's hit), and land once it has been clear for ${CAPJ.clear} s. The scout flips this system's beacon when it isn't locked, and limpets an enemy capital that attacks.</p>`}
{const o=hangarHtml;hangarHtml=function(F,t,C,B){let h=o.apply(this,arguments);try{if(t&&capDefOK(t))h+=capDefLine(F)}catch(err){}return h}}
