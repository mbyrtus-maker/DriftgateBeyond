//@src 16w_crews.js
// ============================================================ AI crews as ships you can see (Beyond, after stage 14)
// Your depot's crews still do their work abstractly, every minute (16o_depots.js), so nothing here moves goods. While a
// depot's system is loaded, each working crew also flies there as a ship on your side: miners hover at the system's rocks
// with their beams on, haulers shuttle between the depot and a gate, guards circle the depot and fight what comes near it,
// idle crews wait beside it. Laid-up crews stay in the hangar. A crew ship destroyed is a crew lost: the pilot and the
// hull are gone from the hangar. Crew ships carry nothing, so a loss drops nothing and the ledger is untouched.
// In multiplayer only the host's own crews fly for now (a guest's crews keep working abstractly).
const CRW={sync:1,guardR:380,guardReach:2600,idleR:240,mineGap:70,flee:4};
function crewMine(P){return(R)=>R&&R.owner==='player'&&R.kind==='depot'&&(R.pid||'me')===pkeyOf(P)}
function crewEnts(){return W?W.ents.filter(e=>e.crewId&&e.alive):[]}
function crewBase(R){return{x:R.x||0,y:R.y||0,z:R.z||0,vx:0,vy:0,vz:0}}
function crewSpawn(R,id,c){const P=S.player,e=makeNPC('crew',P.faction||'halcyon',c.cls,1,{},null);e.side='player';e.crewId=c.id;e.crewR=id;e.job=c.job;e.pname=c.name;
  const b=crewBase(R),o=rdir(1);e.x=b.x+o.x*170;e.y=b.y+o.y*170;e.z=b.z+o.z*170;faceInstant(e,o.x,o.y,o.z);e.slot=(R.crew||[]).indexOf(c);W.ents.push(e);return e}
function crewSync(){if(!W||!S||S.unb||S.training||NET.cl)return;const mine=crewMine(S.player),live=crewEnts();
  for(const e of live){const R=S.stations[e.crewR],c=R&&(R.crew||[]).find(x=>x.id===e.crewId);if(!c||c.laid||R.sid!==W.sid||c.job!==e.job){fxWarp(e,PLAYER_COL);despawn(e)}}
  for(const id in S.stations){const R=S.stations[id];if(!mine(R)||R.sid!==W.sid)continue;for(const c of R.crew||[]){if(c.laid||W.ents.some(e=>e.crewId===c.id&&e.alive))continue;crewSpawn(R,id,c)}}}
function crewRock(e,b){const s=S.sectors[W.sid];let best=null,bd=1e12;for(const a of s.ast){if(a.comet||a.rift||oreTotal(a)<=0)continue;const d=d3(a,b);if(d<bd){bd=d;best=a}}return best}
function crewThink(e,dt){const R=S.stations[e.crewR];if(!R){despawn(e);return}const b=crewBase(R),ai=e.ai;e.mining=null;e.thrusting=false;e.boosting=false;ai.t-=dt;e.life+=dt;
  const hurt=W.t-e.lastHit<CRW.flee;
  if(e.job==='guard'){if(ai.t<=0||!(ai.tgt&&ai.tgt.alive&&W.ents.includes(ai.tgt))){ai.t=.6;const t=findHostile(e,2000);ai.tgt=t&&d3(t,b)<CRW.guardReach?t:null}
    if(ai.tgt){fight(e,ai.tgt,dt);return}
    const a=W.t*.07+(e.slot||0)*2.1;holdSlot(e,b,b.x+Math.cos(a)*CRW.guardR,b.y+Math.sin(a*.7)*90,b.z+Math.sin(a)*CRW.guardR,dt,.8);faceDir(e,-Math.sin(a),0,Math.cos(a),dt);return}
  if(hurt){e.boosting=true;steer(e,b.x,b.y,b.z,dt,true,1.3);faceTo(e,b,dt);return}
  if(e.job==='mine'){let a=ai.ast;if(!a||oreTotal(a)<=0||!S.sectors[W.sid].ast.includes(a))a=ai.ast=crewRock(e,b);if(!a){e.job='idle';return}
    const r=astR(a)+CRW.mineGap,o=ai.mo||(ai.mo=rdir(.5)),tx=a.x+o.x*r,ty=a.y+o.y*r,tz=a.z+o.z*r,d=hyp(tx-e.x,ty-e.y,tz-e.z);
    if(d>40){steer(e,tx,ty,tz,dt,true);faceTo(e,d>400?{x:tx,y:ty,z:tz}:a,dt)}else{brake(e,dt);faceTo(e,a,dt);e.mining=a}return}
  if(e.job==='haul'){const gs=GATES[W.sid]||[];if(!ai.leg){const g=gs.length?gs.reduce((m,x)=>d3(x,b)<d3(m,b)?x:m,gs[0]):null;ai.gate=g?{x:g.x*.9,y:g.y*.9,z:g.z*.9}:{x:b.x+1800,y:b.y,z:b.z};ai.dock={x:b.x+rnd(-200,200),y:b.y+rnd(-60,60),z:b.z+rnd(-200,200)};ai.leg='out'}
    const T=ai.leg==='out'?ai.gate:ai.dock,d=steer(e,T.x,T.y,T.z,dt,true);faceTo(e,T,dt);if(d<90)ai.leg=ai.leg==='out'?'in':'out';return}
  const a=(e.slot||0)*1.7;holdSlot(e,b,b.x+Math.cos(a)*CRW.idleR,b.y+40,b.z+Math.sin(a)*CRW.idleR,dt,.6);faceTo(e,b,dt)}
{const o=npcThink;npcThink=function(e,dt){if(e.crewId){if(!NET.cl)crewThink(e,dt);return}return o.apply(this,arguments)}}
// a crew ship lost is a crew lost
{const o=killShip;killShip=function(e,src,at){const was=e&&e.crewId&&e.alive?e:null;const r=o.apply(this,arguments);if(was&&!was.alive){const R=S.stations[was.crewR],c=R&&(R.crew||[]).find(x=>x.id===was.crewId);
  if(c){R.crew=R.crew.filter(x=>x!==c);keyFeed(R.pid||'me',`✕ ${c.name}'s ${CLASSES[c.cls].name} was destroyed near ${R.name}: the crew is lost.`,'bad')}}return r}}
// crew ships don't take room from the system's traffic
{const o=popCap;popCap=function(){return o.apply(this,arguments)+(W?W.ents.filter(e=>e.crewId&&e.alive).length:0)}}
{const o=shipLabel;shipLabel=function(e){if(e&&e.crewId)return`${e.pname} · your ${{mine:'miner',haul:'hauler',guard:'guard',idle:'crew'}[e.job]||'crew'} (${CLASSES[e.cls].name})`;return o.apply(this,arguments)}}
{const o=worldUpdate;worldUpdate=function(dt){const r=o.apply(this,arguments);try{if(W&&!NET.cl){W.crwT=(W.crwT||0)-dt;if(W.crwT<=0){W.crwT=CRW.sync;crewSync()}}}catch(err){console.error(err)}return r}}
