//@src 16zzs_crewruns.js
// ============================================================ Beyond: your crews do real work (live space stage 1b, 6 Nov 2026)
// Your depot's crews (16o_depots.js, 16w_crews.js) flew for show while the minute tick did their work. Now:
//   - a mining crew's ship drills real rocks while the depot's system is open, filling its hold at its hull's rate (skiff 3,
//     prospector 5, dredger 7 t a minute) and unloading at the depot; out of sight the minute tick mines as before;
//   - a hauling crew loads what the depot sells and flies it to the nearest market that deals with you, sells it there and
//     flies home empty: a tracked ship on the lanes (S.crRuns) that shows in any live system on its way and can be shot down
//     (the crew is lost, its hold salvage). It used to be sold at that market from the depot directly.
// Guards and idle crews are as they were.
const CRR={hop:45};
function crRuns(){return S.crRuns=S.crRuns||[]}
function crRunOf(id){return crRuns().find(r=>String(r.id)===String(id))||null}
function crCrew(r){const R=S.stations[r.depot];return R&&(R.crew||[]).find(c=>c.id===r.crew)||null}
// a hauling run: load at the depot what it's set to sell, to the nearest market that deals with you
function crewHaulStart(R,c,O){const fs=depTraders(O);let best=null,bh=99;for(const id in S.stations){const D=S.stations[id];if(!D||!fs.includes(D.owner))continue;const h=HOP[R.sid]&&HOP[R.sid][id];if(h!=null&&h<bh){bh=h;best=D}}if(!best)return null;
  let cap=DEP.haul[c.cls];const load={};for(const q in R.sell||{}){if(cap<=0)break;const m=Math.min(Math.floor(cap/mass(q)),(R.stock[q]||0)-(R.sell[q]||0));if(m<=0)continue;load[q]=inv.take(R.stock,q,m);cap-=m*mass(q)}
  if(!Object.keys(load).length)return null;const r={id:S.nextId++,crew:c.id,depot:R.sid,pid:R.pid||'me',cls:c.cls,name:c.name,mk:best.sid,path:trPath(R.sid,best.sid)||[R.sid],leg:0,sector:R.sid,next:S.T+CRR.hop*.5,load,state:'go',T0:S.T};
  crRuns().push(r);c.run=r.id;if(WORLDS[r.sector])inW(WORLDS[r.sector],()=>crSpawn(r,false));return r}
function crSell(r){const D=S.stations[r.mk],R=S.stations[r.depot],O=lairOwner({pid:r.pid})||S.player;if(!D||!R)return;const mk=mkStock(D),f=D.owner;
  for(const q of Object.keys(r.load)){const have=r.load[q]||0;const pr=Math.max(1,Math.floor(price(mk,q)*.95)),n=Math.min(have,Math.floor((S.econ.treasury[f]||0)/pr));if(n<=0)continue;inv.take(r.load,q,n);inv.add(mk,q,n);const got=payTo(O,f,n*pr);eco(R,'hauling',got,`${r.name} sold ${n} ${ITEMS[q].name} at ${D.name}`)}}
function crArrive(r){const R=S.stations[r.depot],c=crCrew(r);
  if(r.state==='go'){crSell(r);r.state='back';r.path=trPath(r.mk,r.depot)||[r.mk];r.leg=0;r.sector=r.path[0];r.next=S.T+CRR.hop*.5;if(WORLDS[r.sector])inW(WORLDS[r.sector],()=>crSpawn(r,false));return}
  if(R&&R.owner==='player')inv.addAll(R.stock,r.load);else toDebris(S.sectors[r.sector],r.load);r.load={};if(c)c.run=null;crRuns().splice(crRuns().indexOf(r),1)}
function crRunsTick(){if(NET.cl||!S)return;for(const r of crRuns().slice()){if(r.live)continue;const c=crCrew(r);if(!c){toDebris(S.sectors[r.sector],r.load);r.load={};crRuns().splice(crRuns().indexOf(r),1);continue}
  if(S.T<r.next)continue;if(r.leg>=r.path.length-1){crArrive(r);continue}r.leg++;r.sector=r.path[r.leg];r.next=S.T+CRR.hop;if(WORLDS[r.sector])inW(WORLDS[r.sector],()=>crSpawn(r,true))}}
{const o=strategicTick;strategicTick=function(){const x=o.apply(this,arguments);try{crRunsTick()}catch(e){console.error(e)}return x}}
{const o=ledger;ledger=function(){const r=o.apply(this,arguments);try{const L=r.L['Your ship, hold, vault'];for(const x of S.crRuns||[]){const v=invVec(x.load||{});for(const e of RAWS){L[e]+=v[e];r.tot[e]+=v[e]}}}catch(e){}return r}}
// live: the hauling crew's ship on its way
function crSpawn(r,arrive){if(r.live||!W)return;const P=lairOwner({pid:r.pid||'me'})||S.player,e=makeNPC('crew',P.faction||'halcyon',r.cls,1,{},`crr:${r.id}`);e.side='player';e.crRun=r.id;e.pname=r.name;e.cargo=r.load;r.load={};r.live=true;
  const gs=GATES[W.sid]||[],prev=r.path[r.leg-1],gin=gs.find(g=>g.to===prev),SE=W.stationEnt;
  if(arrive&&gin){e.x=gin.x*.93;e.y=gin.y*.93;e.z=gin.z*.93;fxWarp(e,PLAYER_COL)}else if(SE&&r.leg===0){const o=rdir(1);e.x=SE.x+o.x*200;e.y=SE.y+o.y*80;e.z=SE.z+o.z*200}else{const g=pick(gs);if(g){e.x=g.x*.9;e.y=g.y*.9;e.z=g.z*.9}}
  faceInstant(e,-e.x,-e.y,-e.z);W.ents.push(e);return e}
{const o=npcThink;npcThink=function(e,dt){if(e.crRun&&!NET.cl){const r=crRunOf(e.crRun);if(!r){e.crRun=null;e.role='leave';return}e.ai.t-=dt;e.life+=dt;e.mining=null;
  if(r.leg<r.path.length-1){const g=W.ents.find(x=>x.type==='gate'&&x.to===r.path[r.leg+1]);if(g){npcGateJump(e,g,dt,.8);return}}
  const SE=W.stationEnt;if(SE){const d=steer(e,SE.x,SE.y,SE.z,dt,true,.8);faceTo(e,SE,dt);if(d<(SE.r||150)+60){r.arrived=true;despawn(e)}return}r.arrived=true;despawn(e);return}
  return o.apply(this,arguments)}}
// a crew's own run comes before crewThink (its ship carries crRun, not crewId); a crew away on a run isn't at the depot
{const o=crewSpawn;crewSpawn=function(R,id,c){if(c&&c.run)return null;return o.apply(this,arguments)}}
{const o=returnHome;returnHome=function(e){if(e&&e.crRun){const r=crRunOf(e.crRun);if(r){inv.addAll(r.load,e.cargo);inv.addAll(r.load,e.load);e.cargo={};e.load={};r.live=false;
  if(r.arrived){r.arrived=false;r.leg=r.path.length-1;crArrive(r)}else if(r.leg<r.path.length-1&&e.gj){r.leg++;r.sector=r.path[r.leg];r.next=S.T+CRR.hop;if(WORLDS[r.sector])inW(WORLDS[r.sector],()=>crSpawn(r,true))}}}return o.apply(this,arguments)}}
{const o=killShip;killShip=function(e,src,at){const r=e&&e.crRun?crRunOf(e.crRun):null;const x=o.apply(this,arguments);
  if(r&&e&&!e.alive){const R=S.stations[r.depot],c=crCrew(r);if(R&&c){R.crew=R.crew.filter(y=>y!==c);keyFeed(r.pid,`✕ ${c.name}'s ${CLASSES[c.cls].name} was shot down in ${DEF[W.sid].name} on a hauling run: the crew is lost.`,'bad')}const i=crRuns().indexOf(r);if(i>=0)crRuns().splice(i,1)}return x}}
{const o=holderIn;holderIn=function(st,path){if(typeof path==='string'&&path.startsWith('crr:')){const r=(st.crRuns||[]).find(x=>String(x.id)===path.split(':')[1]);return r?(r.load=r.load||{}):(st.player.vault=st.player.vault||{})}return o.apply(this,arguments)}}
{const o=openWorld;openWorld=function(sid){const w=o.apply(this,arguments);try{if(!NET.cl&&S)inW(w,()=>{for(const r of crRuns())if(r.sector===sid){r.live=false;crSpawn(r,false)}})}catch(e){console.error(e)}return w}}
{const o=shipLabel;shipLabel=function(e){if(e&&e.crRun)return`${e.pname} · your hauler on a run (${CLASSES[e.cls].name})`;return o.apply(this,arguments)}}
// mining live: the crew's ship drills a real rock at its hull's rate and unloads at the depot
{const o=crewThink;crewThink=function(e,dt){if(e.job==='mine'&&DEP.mine[e.cls]){const R=S.stations[e.crewR];if(R&&!(W.t-e.lastHit<CRW.flee)){const b=crewBase(R),ai=e.ai;e.thrusting=false;e.boosting=false;e.mining=null;ai.t-=dt;e.life+=dt;
    if(invMass(e.cargo)>=Math.min(e.st.cargo||40,DEP.mine[e.cls]*4)){const d=steer(e,b.x,b.y,b.z,dt,true);faceTo(e,b,dt);if(d<170){inv.addAll(R.stock,e.cargo);e.cargo={}}return}
    let a=ai.ast;if(!a||oreTotal(a)<=0||!S.sectors[W.sid].ast.includes(a))a=ai.ast=crewRock(e,b);if(!a){e.job='idle';return}
    const r=astR(a)+CRW.mineGap,q=ai.mo||(ai.mo=rdir(.5)),tx=a.x+q.x*r,ty=a.y+q.y*r,tz=a.z+q.z*r,d=hyp(tx-e.x,ty-e.y,tz-e.z);
    if(d>40){steer(e,tx,ty,tz,dt,true);faceTo(e,d>400?{x:tx,y:ty,z:tz}:a,dt);return}brake(e,dt);faceTo(e,a,dt);e.mining=a;
    e.mineAcc=(e.mineAcc||0)+DEP.mine[e.cls]/60*dt;const s=S.sectors[W.sid];while(e.mineAcc>=1){e.mineAcc-=1;const k=mainOre(a);if(!k)break;a.ore[k]--;if(!a.ore[k])delete a.ore[k];inv.add(e.cargo,k,1);if(oreTotal(a)<=0){removeAst(s,a);ai.ast=null;break}}return}}
  return o.apply(this,arguments)}}
// a crew ship leaving the world takes its hold home to the depot (the system closing, or a job change)
{const o=returnHome;returnHome=function(e){if(e&&e.crewId&&invMass(e.cargo)>0){const R=S.stations[e.crewR];if(R)inv.addAll(R.stock,e.cargo);else toDebris(S.sectors[W.sid],e.cargo);e.cargo={}}return o.apply(this,arguments)}}
