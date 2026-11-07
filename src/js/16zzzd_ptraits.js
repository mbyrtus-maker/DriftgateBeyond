//@src 16zzzd_ptraits.js
// ============================================================ Beyond: pilot traits (agreed with the user 7 Nov 2026)
// Every AI pilot carries one trait that guides how it flies and fights while alive (BEYOND_DESIGN.md, "Pilot traits"). It sits
// under the leader's style (16g_leaders.js: a power's pilots fly like its leader) and leans a pilot one way inside it.
//   Rolled: when a ship launches (makeNPC), from its role's pool (fighter, scout, bomber, miner, hauler, capital) most of the
//           time and the universal pool otherwise, Steady the common roll and the extreme traits rare. The Brood have none.
//   Kept:   pilots with a record keep theirs across live and out of sight: aces (A.pt), independents (I.pt), your crews
//           (c.pt), the powers' convoys and scouts (t.pt) and capital ships (t.pt, the captain's).
//   Learned: a pilot who dies and comes back (an ace, an independent) takes a new trait from how it died (ptCause, ptDeath),
//           which replaces the old one. Losses stay final for everyone else (the user, 7 Nov 2026).
// The behaviour is live-space AI: reach, break-off, preferred range, whom to shoot first, formation, flares, rock choice,
// when to run, how a scout watches, how a bomber commits, how a captain positions its ship. Out of sight, traits steer the
// independents' own choices (routes, where to mine, what to trade, how long to wait for company; 16zzzc_indep.js).
const PT_POOL={
  universal:{Skittish:.7,Unpredictable:1,Loyal:1.6,Greedy:1},
  fighter:{Hotshot:2,Sniper:2,Opportunist:2,Duelist:.6,Guardian:2,'Lone Wolf':.6,'Rock Hopper':1.4},
  scout:{Ghost:2,'Thrill Seeker':1.2,Bait:1.2,Shadow:1.2,Tripwire:2},
  bomber:{'Big Game Hunter':1.4,Patient:2,'Kamikaze-ish':.6,Precision:2,'Hit and Run':2},
  miner:{Prospector:2,Homebody:2,Hoarder:1.2,Efficient:2.5,'Rock Diver':.8},
  hauler:{'Speed Demon':1.2,'Safe Routes':2,'Convoy Lover':1.5,Overloader:1.5,Smuggler:.8},
  capital:{Admiral:2,'Brawler Captain':1.5,Bastion:2,'Carrier Minded':1.5,'Glory Seeker':.6,'Cautious Commander':1.5}};
const PT_ROLL={steady:.25,role:.6};
// died to → the new trait, by role (and 'named': killed by an ace or a named pilot, yours included)
const PT_DEATH={fighter:{dogfight:'Cautious',missile:'Missile-Wary',pd:'Flak-Shy',outnumbered:'Pack Fighter'},
  scout:{ambush:'Jumpy',shadow:'Long Leash',deep:'Edge Walker'},
  bomber:{pd:'Long Launch',intercepted:'Escort Only',escape:'Quick Exit',blast:'Blast-Aware'},
  miner:{raided:'Watchful',full:'Light Load',far:'Homebody'},
  hauler:{ambush:'Route Changer',hostile:'Safe Routes',alone:'Convoy Only'},
  capital:{bomber:'Screen First',capital:'Outranged',swarmed:'Point Defense Doctrine',alone:'Fleet Anchor'}};
const PT_COMBAT=new Set(['fighter','bomber','capital']);
// what each trait does to a live ship
const PT_FX={Steady:{},Skittish:{flee:1500,brk:.6},Unpredictable:{erratic:1},Loyal:{loyal:1},Greedy:{pref:'civ',rng:1.1},
  Hotshot:{rng:1.3,brk:0,stay:1,want:260},Sniper:{rng:1.2,want:800},Opportunist:{pref:'hurt'},Duelist:{duel:1,stay:1},Guardian:{pref:'guard'},'Lone Wolf':{solo:1,rng:1.4},'Rock Hopper':{rocks:1},
  Ghost:{flee:2200,noFire:1},'Thrill Seeker':{flee:700,roam:4200},Bait:{bait:1},Shadow:{shadow:2200},Tripwire:{gate:1},
  'Big Game Hunter':{pref:'cap'},Patient:{wait:20},'Kamikaze-ish':{stay:1,brk:0},Precision:{prec:1},'Hit and Run':{hitrun:1},
  Prospector:{rock:'far'},Homebody:{rock:'home'},Hoarder:{hoard:1},Efficient:{rock:'near'},'Rock Diver':{rock:'rare'},
  'Speed Demon':{boost:1},'Safe Routes':{},'Convoy Lover':{},Overloader:{slow:.9},Smuggler:{dodge:1},
  Admiral:{cap:'fleet'},'Brawler Captain':{cap:'brawl'},Bastion:{cap:'hold'},'Carrier Minded':{cap:'back'},'Glory Seeker':{cap:'glory'},'Cautious Commander':{cap:'save'},
  Vengeful:{venge:1,stay:1},Haunted:{haunt:2600},Shaken:{brk:.35,rng:.9},
  Cautious:{brk:.4,want:650,rng:.9},'Missile-Wary':{flares:1},'Flak-Shy':{nocap:1},'Pack Fighter':{pack:1},
  Jumpy:{flee:2600},'Long Leash':{shadow:4000,flee:1800},'Edge Walker':{flee:2000},
  'Long Launch':{tStand:2100},'Escort Only':{escortOnly:1},'Quick Exit':{hitrun:1,boostOut:1},'Blast-Aware':{blastAware:1},
  Watchful:{flee:2500},'Light Load':{half:1},'Route Changer':{},'Convoy Only':{},
  'Screen First':{cap:'screen'},Outranged:{cap:'back'},'Point Defense Doctrine':{cap:'screen'},'Fleet Anchor':{cap:'fleet'}};
function ptName(t){return t||''}
function ptHas(x,t){return!!x&&x.pt===t}
function ptP(e){if(!e||!e.pt)return null;if(e.ptk!==e.pt){e.ptk=e.pt;e.ptp=PT_FX[e.pt]||{}}return e.ptp}
function ptRoll(role){if(!PT_POOL[role])return null;const r=Math.random();if(r<PT_ROLL.steady)return'Steady';return wpick(r<PT_ROLL.steady+PT_ROLL.role?PT_POOL[role]:PT_POOL.universal)}
function ptDeath(role,cause,who){if(cause==='named'){if(who&&who.killer)who.nem=who.killer;return PT_COMBAT.has(role)?'Vengeful':'Haunted'}const M=PT_DEATH[role]||{};return M[cause]||'Shaken'}
function ptRoleOf(e){if(!e||e.side==='brood'||e.type!=='ship')return null;const r=e.role,c=e.cls;if(r==='frigate')return'capital';if(r==='drone'||r==='limpet'||r==='og'||r==='builder'||c==='drone')return null;
  if(r==='crew')return e.job==='mine'?'miner':e.job==='haul'?'hauler':'fighter';if(r==='scout'||c==='scout'||c==='scout2')return'scout';if(isBmb(c))return'bomber';
  if(r==='miner'||blHull(c))return'miner';if(r==='hauler'||r==='trader'||isHaulCls(c))return'hauler';return'fighter'}
// ---- how it died
function ptKillerTag(k){if(!k)return null;if(k.isPlayer)return'me';if(k.rp)return'rp:'+k.rp;if(k.aceId)return'ace:'+k.aceId;if(k.indId)return'ind:'+k.indId;return null}
function ptCause(e,src,at,role){role=role||ptRoleOf(e);const k=at&&at.src&&at.src.type==='ship'?at.src:null,kind=at&&at.kind;
  if(ptKillerTag(k))return'named';
  const hostN=R=>W.ents.filter(x=>x.type==='ship'&&x.alive&&x!==e&&hostE(e.side,x)&&d3(x,e)<R).length;
  if(role==='fighter'){if(kind==='missile'||kind==='torpedo'||kind==='swarm')return'missile';if(k&&k.role==='frigate'||(at&&at.tur))return'pd';if(hostN(2500)>=3)return'outnumbered';return k?'dogfight':'unknown'}
  if(role==='bomber'){if(k&&k.role==='frigate'||(at&&at.tur)||(!k&&W.stationEnt&&d3(W.stationEnt,e)<2600))return'pd';if(kind==='blast')return'blast';if(e.ptLaunch&&W.t-e.ptLaunch<30)return'escape';return k?'intercepted':'unknown'}
  if(role==='scout'){if(e.ai&&e.ai.shadow&&k===e.ai.shadow)return'shadow';const o=sectorOwner(W.sid);if(broodHeld(W.sid)||(o&&o!==e.side&&hostile(e.side,o)))return'deep';return'ambush'}
  if(role==='miner'){if(invMass(e.cargo||{})>=e.st.cargo*.85)return'full';return'raided'}
  if(role==='hauler'){const o=sectorOwner(W.sid);if(broodHeld(W.sid)||(o&&hostile(e.side,o)))return'hostile';return W.ents.some(x=>x!==e&&x.alive&&x.type==='ship'&&x.side===e.side&&d3(x,e)<2500)?'ambush':'alone'}
  if(role==='capital'){if(kind==='torpedo'||(k&&isBmb(k.cls)))return'bomber';if(k&&k.role==='frigate')return'capital';if(W.ents.filter(x=>x.type==='ship'&&x.alive&&hostE(e.side,x)&&x.role!=='frigate'&&d3(x,e)<3000).length>=4)return'swarmed';
    if(!W.ents.some(x=>x!==e&&x.alive&&x.role==='frigate'&&x.side===e.side&&d3(x,e)<5000))return'alone';return'unknown'}
  return'unknown'}
// ---- whom a Vengeful pilot hunts, whom a Haunted one runs from
function ptNemesis(x){const n=x&&x.nem;if(!n||!W)return null;if(n==='me')return W.player&&!W.dead&&!S.player.docked?W.player:null;
  const[a,b]=String(n).split(':');return W.ents.find(o=>o.type==='ship'&&o.alive&&(a==='rp'?o.rp===b:a==='ace'?String(o.aceId)===b:a==='ind'?String(o.indId)===b:false))||null}
function ptRec(e){if(!e)return null;if(e.indId&&typeof indById==='function')return indById(e.indId);if(e.aceId&&typeof aceById==='function')return aceById(e.aceId);return null}
// ---- the independents' out-of-sight dials
function ptHopK(I){return ptHas(I,'Speed Demon')?.85:ptHas(I,'Overloader')?1.1:1}
function ptRiskK(I){return ptHas(I,'Watchful')||ptHas(I,'Skittish')?.6:ptHas(I,'Greedy')||ptHas(I,'Hoarder')?1.25:ptHas(I,'Shaken')?.8:1}
// a ship that runs when hostiles come close (Skittish, Ghost, Jumpy, Watchful...), or when its nemesis shows (Haunted)
function ptNear(e,R,pred){for(const o of W.ents)if(o.type==='ship'&&o.alive&&o!==e&&hostE(e.side,o)&&!(o.isPlayer&&(S.player.docked||W.dead))&&!mHid(o,e)&&d3(o,e)<R&&(!pred||pred(o)))return true;return false}
function ptFlee(e){const P=ptP(e);if(!P)return false;if(P.haunt){const N=ptNemesis(ptRec(e)||e);if(N&&d3(N,e)<P.haunt)return true}return!!P.flee&&ptNear(e,P.flee)}
// which rock a miner picks
function ptRock(e,L,SE){const P=ptP(e);if(!P||!P.rock||!L.length)return null;const base=SE||{x:0,y:0,z:0};
  if(P.rock==='near')return L.slice().sort((a,b)=>d3(a,e)-d3(b,e))[0];if(P.rock==='home')return L.slice().sort((a,b)=>d3(a,base)-d3(b,base))[0];
  if(P.rock==='far')return L.slice().sort((a,b)=>d3(b,base)-d3(a,base))[Math.floor(Math.random()*Math.min(3,L.length))];
  if(P.rock==='rare'){const rv=a=>(a.ore.au||0)*70+(a.ore.xc||0)*40+(a.ore.nu||0)*30+(a.ore.ir||0)*16;return L.slice().sort((a,b)=>rv(b)-rv(a))[0]}return null}
function ptFriendNear(e,R,pred){return W.ents.some(x=>x!==e&&x.type==='ship'&&x.alive&&(x.side===e.side||(x.isPlayer&&friendSide(e.side)))&&d3(x,e)<R&&(!pred||pred(x)))}
const PT_CBT=new Set(['patrol','raider','pirate','strike','escort','screen','crew','flight']);
// ---- rolling: every ship as it launches; records keep theirs
function ptApply(e){const P=ptP(e);if(!e||!e.st)return e;if(e.ptSpd==null)e.ptSpd=e.st.maxSpd;const k=(P&&P.slow)||1;if(e.st.maxSpd!==e.ptSpd*k)e.st=Object.assign({},e.st,{maxSpd:e.ptSpd*k});
  if(P&&P.flares)e.flares=true;e.ptWant=P&&P.want||undefined;return e}
{const o=makeNPC;makeNPC=function(){const e=o.apply(this,arguments);try{if(e&&!e.pt){const r=ptRoleOf(e);if(r){e.pt=ptRoll(r);ptApply(e)}}}catch(err){}return e}}
function ptTok(e,t,role){if(!e||!t)return e;if(t.pt===undefined)t.pt=e.side==='brood'?null:ptRoll(role);e.pt=t.pt;e.ptk=null;return ptApply(e)}
{const o=spawnFrigate;spawnFrigate=function(t){const e=o.apply(this,arguments);try{if(e)ptTok(e,t,'capital')}catch(err){}return e}}
{const o=spawnTrader;spawnTrader=function(t){const e=o.apply(this,arguments);try{if(e)ptTok(e,t,'hauler')}catch(err){}return e}}
{const o=spawnScout;spawnScout=function(t){const e=o.apply(this,arguments);try{if(e)ptTok(e,t,'scout')}catch(err){}return e}}
{const o=crewSpawn;crewSpawn=function(R,id,c){const e=o.apply(this,arguments);try{if(e&&c){if(c.pt===undefined)c.pt=ptRoll(ptRoleOf(e)||'fighter');e.pt=c.pt;e.ptk=null;ptApply(e)}}catch(err){}return e}}
{const o=crSpawn;crSpawn=function(r){const e=o.apply(this,arguments);try{const c=e&&r&&typeof crCrew==='function'?crCrew(r):null;if(e&&c){if(c.pt===undefined)c.pt=ptRoll('hauler');e.pt=c.pt;e.ptk=null;ptApply(e)}}catch(err){}return e}}
{const o=aceWing;aceWing=function(A){const g=o.apply(this,arguments);try{const e=g&&g.members[0];if(e&&A&&!String(A.id).startsWith('L')){if(A.pt===undefined)A.pt=ptRoll('fighter');e.pt=A.pt;e.ptk=null;ptApply(e);
    if(A.ptNew){A.ptNew=0;if(!NET.cl)allFeed(`★ ${aceLabel(A)} is back in the fight, ${A.pt} now.`,'info')}}}catch(err){}return g}}
// an ace shot down learns from it when it comes back
{const o=aceKilled;aceKilled=function(e,src,at){try{const A=aceById(e.aceId);if(A){A.ptCause=ptCause(e,src,at,'fighter');A.killer=ptKillerTag(at&&at.src&&at.src.type==='ship'?at.src:null)}}catch(err){}return o.apply(this,arguments)}}
{const o=aceDown;aceDown=function(A){const r=o.apply(this,arguments);try{if(A&&!A.ret){const was=A.pt;A.pt=ptDeath('fighter',A.ptCause||'unknown',A);A.ptCause=null;if(A.pt!==was)A.ptNew=1}}catch(err){}return r}}
// independents keep their trait on their ship (16zzzc_indep.js sets e.pt; this applies its numbers)
{const o=indFly;indFly=function(e){const r=o.apply(this,arguments);try{ptApply(e)}catch(err){}return r}}
// ---- whom to shoot: reach and first choice
{const o=findHostile;findHostile=function(e,range){const P=ptP(e);if(!P)return o.apply(this,arguments);const R=range*(P.rng||1);const ai=e.ai||{};
  if(P.duel&&ai.duel&&ai.duel.alive&&W.ents.includes(ai.duel)&&!mHid(ai.duel,e)&&d3(ai.duel,e)<R*2)return ai.duel;
  if(P.venge){const N=ptNemesis(ptRec(e)||e);if(N&&hostE(e.side,N)&&d3(N,e)<R*1.6)return N}
  let t=o.call(this,e,R);const hit=W.t-(e.lastHit||-99)<2.5;
  const scan=f=>{let best=null,bd=1e12;for(const x of W.ents){if(x.type!=='ship'||!x.alive||x===e||!hostE(e.side,x)||mHid(x,e)||(x.isPlayer&&(S.player.docked||W.dead)))continue;const d=d3(x,e);if(d>R*1.15)continue;const v=f(x,d);if(v!=null&&v<bd){bd=v;best=x}}return best};
  if(P.pref==='hurt'){const b=scan((x,d)=>(x.hull/(x.st.hull||1))*1000+d*.2);if(b)t=b}
  else if(P.pref==='civ'){const b=scan((x,d)=>x.role==='miner'||x.role==='hauler'||x.role==='trader'?d:null);if(b)t=b}
  else if(P.pref==='cap'){const b=scan((x,d)=>x.role==='frigate'?d:null);t=b||(hit?t:null)}
  else if(P.pref==='guard'){const charges=W.ents.filter(x=>x.type==='ship'&&x.alive&&x.side===e.side&&(x.role==='miner'||x.role==='hauler'||x.role==='trader'||x.role==='frigate'));if(charges.length){const b=scan((x,d)=>{let m=1e12;for(const c of charges)m=Math.min(m,d3(c,x));return m<1500?m:null});if(b)t=b}}
  if(P.loyal&&!hit){let att=null;for(const f of W.ents)if(f!==e&&f.type==='ship'&&f.alive&&f.side===e.side&&f.lastHitBy&&W.t-(f.lastHit||-99)<3&&d3(f,e)<2200){att=scan((x,d)=>x.side===f.lastHitBy&&d3(x,f)<1600?d:null);if(att)break}if(att)t=att}
  if(P.nocap&&t&&t.role==='frigate'){t=scan((x,d)=>x.role==='frigate'?null:d)}
  if(P.pack&&t&&!hit&&!ptFriendNear(e,1500,x=>PT_CBT.has(x.role)||x.isPlayer))t=null;
  if(P.duel&&t)ai.duel=t;return t}}
// ---- flying: break-off, running, formation, idle wandering, bombers' commitment
{const o=npcThink;npcThink=function(e,dt){const P=e.npc&&!NET.cl&&ptP(e);if(!P)return o.apply(this,arguments);const ai=e.ai,cbt=PT_CBT.has(e.role);
  try{
    if((e.role==='patrol'||e.role==='escort'||e.role==='raider'||e.role==='pirate')&&!e.indId&&!e.leaderOf&&!e.order&&!e.aceId){
      if(P.brk&&e.hull<e.st.hull*P.brk&&ai.tgt&&!P.stay){e.role='leave';ai.tgt=null}
      if(P.haunt&&ptFlee(e)){e.role='flee';ai.tgt=null}}
    if(P.solo&&e.grp&&!ai.ptSolo&&(e.role==='patrol'||e.role==='raider'||e.role==='pirate')&&grpLead(e.grp)!==e){ai.ptSolo=1;const g=e.grp;g.members=g.members.filter(m=>m!==e);e.grp=null}
    if(P.erratic&&W.t>(ai.ptErr||0)){ai.ptErr=W.t+rnd(18,40);e.ptWant=pick([260,400,600,800]);if(Math.random()<.4)ai.tgt=null;ai.wp=null}
    if(P.rocks&&cbt&&!ai.tgt&&(!ai.wp||d3(ai.wp,e)<140)&&!e.grp){const s=S.sectors[W.sid],L=s&&s.ast.filter(a=>!a.comet);if(L&&L.length){const a=pick(L),q=rdir(1),r=astR(a)+160;ai.wp={x:a.x+q.x*r,y:a.y+q.y*r,z:a.z+q.z*r}}}
    if(e.role==='miner'&&e.side!=='brood'&&!e.pjRun&&!e.indId){const s=S.sectors[W.sid],SE=W.stationEnt;
      if(P.rock&&!ai.ast&&!ai.state){const L=s.ast.filter(x=>!x.comet&&oreTotal(x)>0);const a=ptRock(e,L,SE&&SE.fac===e.side?SE:null);if(a)ai.ast=a}
      if(P.half&&invMass(e.cargo)>=e.st.cargo*.5)ai.state='return';if(P.flee&&ptFlee(e))ai.state='return'}
    if(isBmb(e.cls)&&(P.hitrun||P.blastAware)&&e.ptLaunch&&(e.role==='strike'||e.role==='raider')){
      if(P.hitrun&&!(e.load.torpedo>0)&&!(ai.siege)){e.role='leave';ai.tgt=null}
      else if(P.blastAware&&W.t-e.ptLaunch<4&&ai.tgt){const t=ai.tgt,dx=e.x-t.x,dy=e.y-t.y,dz=e.z-t.z,l=hyp(dx,dy,dz)||1;e.boosting=true;steer(e,e.x+dx/l*800,e.y+dy/l*800,e.z+dz/l*800,dt,false,1.2);faceDir(e,dx,dy,dz,dt);ai.t-=dt;e.life+=dt;return}}
  }catch(err){console.error(err)}
  const r=o.apply(this,arguments);
  try{if(e.role==='miner'&&P.hoard&&ai.state==='return'&&invMass(e.cargo)<e.st.cargo&&e.hull>e.st.hull*.4&&W.t-e.lastHit>=4)ai.state=null;
    if(P.boostOut&&e.role==='leave')e.boosting=true;
    if((e.role==='hauler'||e.role==='trader')&&!e.indId&&(P.boost||(P.dodge&&ptNear(e,2000,x=>FAC_IDS.includes(x.side)))||ptFlee(e)))e.boosting=true}catch(err){}
  return r}}
// a scout's trait: how close it lets hostiles come, whom it tails, where it watches
{const o=scoutThink;scoutThink=function(e,dt){const P=ptP(e);if(!P||NET.cl)return o.apply(this,arguments);const ai=e.ai;
  let th=null,bd=1e12;for(const x of W.ents){if(x.type!=='ship'||!x.alive||!hostE(e.side,x)||(x.isPlayer&&(S.player.docked||W.dead))||mHid(x,e))continue;const d=d3(x,e);if(d<bd){bd=d;th=x}}
  const away=(R,boost)=>{e.boosting=boost;const ax=e.x-th.x,ay=e.y-th.y,az=e.z-th.z,l=hyp(ax,ay,az)||1;let tx=e.x+ax/l*900,ty=e.y+ay/l*250,tz=e.z+az/l*900;const r=hyp(tx,ty,tz);if(r>3400){tx*=3400/r;ty*=3400/r;tz*=3400/r}steer(e,tx,ty,tz,dt,false,1);faceDir(e,e.vx,e.vy,e.vz,dt)};
  if(P.shadow){let X=ai.shadow;if(!(X&&X.alive&&W.ents.includes(X))){X=null;let b=1e12;for(const x of W.ents){if(x.type!=='ship'||!x.alive||!hostE(e.side,x)||mHid(x,e))continue;if(!(x.role==='frigate'||x.aceId||x.pname||x.isPlayer||x.rp))continue;const d=d3(x,e);if(d<b&&d<9000){b=d;X=x}}ai.shadow=X}
    if(X){const d=d3(X,e),want=P.shadow;if(th&&th!==X&&bd<900){away(900,true);return}const dx=e.x-X.x,dy=e.y-X.y,dz=e.z-X.z,l=hyp(dx,dy,dz)||1;e.boosting=d>want*1.6;steer(e,X.x+dx/l*want,X.y+dy/l*want*.4,X.z+dz/l*want,dt,d<want*1.15,1);faceTo(e,X,dt);return}}
  if(P.bait&&th&&bd<2600){if(bd>1100&&!ai.baited){steer(e,th.x,th.y,th.z,dt,false,.9);faceTo(e,th,dt);return}ai.baited=1;let F=null,fd=1e12;for(const x of W.ents)if(x!==e&&x.type==='ship'&&x.alive&&x.side===e.side&&PT_CBT.has(x.role)){const d=d3(x,e);if(d<fd){fd=d;F=x}}
    if(F){e.boosting=true;steer(e,F.x,F.y,F.z,dt,false,1.2);faceDir(e,e.vx,e.vy,e.vz,dt);return}}
  const R0=P.flee||1400;
  if(th&&bd<R0){if(bd<1400&&R0<=1400&&!P.noFire)return o.apply(this,arguments);away(R0,bd<R0*.7);return}
  if((P.gate||P.roam)&&typeof scoutBeaconGoal==='function'&&scoutBeaconGoal(e))return o.apply(this,arguments);
  if(P.gate){const gs=GATES[W.sid]||[];if(gs.length){if(!ai.ptGate||!gs.includes(ai.ptGate))ai.ptGate=pick(gs);const g=ai.ptGate,p={x:g.x*.82,y:g.y*.82+120,z:g.z*.82},d=d3(p,e);e.boosting=false;if(d>220){steer(e,p.x,p.y,p.z,dt,true,.8);faceDir(e,p.x-e.x,p.y-e.y,p.z-e.z,dt)}else{brake(e,dt);faceTo(e,g,dt)}return}}
  if(P.roam){if(!ai.wp||d3(ai.wp,e)<220){const q=rdir(.6),r=rnd(1800,P.roam)*SPACE;ai.wp={x:q.x*r,y:q.y*r,z:q.z*r}}
    if(th&&bd<1400){e.boosting=false;steer(e,ai.wp.x,ai.wp.y,ai.wp.z,dt,false,.8);faceDir(e,e.vx,e.vy,e.vz,dt);return}}
  return o.apply(this,arguments)}}
// bombers: how far out they launch (Long Launch), whether they wait for an opening or an escort (Patient, Escort Only),
// whether they go for subsystems (Precision)
{const o=bomberRun;bomberRun=function(e,OE,dt){const P=ptP(e);if(!P||NET.cl)return o.apply(this,arguments);const ai=e.ai;
  if(P.tStand&&!ai.stand){const r=rdir(.8),R=Math.min(TORP_RANGE*.9,P.tStand);ai.stand={x:OE.x+r.x*R,y:OE.y+r.y*R,z:OE.z+r.z*R}}
  const cover=()=>ptFriendNear(e,1800,x=>PT_CBT.has(x.role)&&!isBmb(x.cls));
  if((P.escortOnly&&!cover())||(P.wait&&W.t<(ai.ptWaitT||(ai.ptWaitT=W.t+P.wait))&&!cover()&&!((OE.shield||0)<=0&&OE.type==='ship'))){if(!ai.stand){const r=rdir(.8);ai.stand={x:OE.x+r.x*2400,y:OE.y+r.y*2400,z:OE.z+r.z*2400}}
    const hold={x:OE.x+(ai.stand.x-OE.x)*1.6,y:OE.y+(ai.stand.y-OE.y)*1.6,z:OE.z+(ai.stand.z-OE.z)*1.6};steer(e,hold.x,hold.y,hold.z,dt,true,.8);faceTo(e,OE,dt);return}
  return o.apply(this,arguments)}}
{const o=wkPickFor;wkPickFor=function(e,hasStation,chance){const P=ptP(e);if(P&&P.prec)chance=Math.max(chance||0,.9);return o.call(this,e,hasStation,chance)}}
{const o=launchMissile;launchMissile=function(e,tgt,tier,kind){if(e&&e.npc&&kind==='torpedo')e.ptLaunch=W.t;return o.apply(this,arguments)}}
// capital captains: where an AI captain puts its ship in a live fight
{const o=frigateThink;frigateThink=function(e,dt){const r=o.apply(this,arguments);try{const t=e.tok,P=ptP(e);if(!P||!P.cap||!t||NET.cl||t.dummy||fOwn(t)||t.spin||e.charging||!S.frigates.includes(t)||!e.alive)return r;
    let foe=null,fd=1e12;for(const x of W.ents)if(x!==e&&x.alive&&x.role==='frigate'&&hostE(e.side,x)){const d=d3(x,e)*(P.cap==='glory'?(x.cls==='carrier'?.5:x.cls==='frigate'?.7:1):1);if(d<fd){fd=d;foe=x}}
    const go=(x,y,z,k)=>{steer(e,x,y,z,dt,true,k||.7);e.thrusting=true};
    if((P.cap==='brawl'||P.cap==='glory')&&foe&&d3(foe,e)<7000&&d3(foe,e)>1300){const d=d3(foe,e),dx=e.x-foe.x,dy=e.y-foe.y,dz=e.z-foe.z;go(foe.x+dx/d*1200,foe.y+dy/d*1200,foe.z+dz/d*1200,.8)}
    else if(P.cap==='back'&&foe&&d3(foe,e)<3200){const d=d3(foe,e),dx=e.x-foe.x,dy=e.y-foe.y,dz=e.z-foe.z;go(e.x+dx/d*900,e.y+dy/d*900,e.z+dz/d*900,.7)}
    else if(P.cap==='save'&&e.hull<e.st.hull*.45){const th=foe||W.ents.find(x=>x.type==='ship'&&x.alive&&hostE(e.side,x)&&d3(x,e)<4000);if(th){const d=d3(th,e)||1,dx=e.x-th.x,dy=e.y-th.y,dz=e.z-th.z;go(e.x+dx/d*1200,e.y+dy/d*1200,e.z+dz/d*1200,1);e.boosting=true}}
    else if(P.cap==='hold'){const SE=W.stationEnt;if(SE&&SE.fac===e.side&&d3(SE,e)>1400&&d3(SE,e)<6000)go(SE.x+(e.x-SE.x)*.3,SE.y+(e.y-SE.y)*.3,SE.z+(e.z-SE.z)*.3,.6)}
    else if(P.cap==='fleet'){const F=W.ents.filter(x=>x!==e&&x.alive&&x.role==='frigate'&&x.side===e.side&&d3(x,e)<6000);if(F.length){const c={x:0,y:0,z:0};for(const x of F){c.x+=x.x/F.length;c.y+=x.y/F.length;c.z+=x.z/F.length}if(d3(c,e)>1500)go(c.x,c.y,c.z,.6)}}
    else if(P.cap==='screen'){let b=null,bd=TORP_RANGE;for(const x of W.ents)if(x.type==='ship'&&x.alive&&hostE(e.side,x)&&(isBmb(x.cls)||x.role!=='frigate')&&!mHid(x,e)){const d=d3(x,e)*(isBmb(x.cls)?.5:1);if(d<bd){bd=d;b=x}}if(b&&!(e.lanceT&&e.lanceT.role==='frigate'))e.lanceT=b}
  }catch(err){console.error(err)}return r}}
