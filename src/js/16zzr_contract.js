//@src 16zzr_contract.js
// ============================================================ Beyond: AI contractors fly the jobs (live space stage 5, 6 Nov 2026)
// A job posted for other pilots (16zf_posted.js) that an AI pilot takes is no longer a timer: the taker is a tracked ship
// (S.pjRuns) that flies the lanes hop by hop, shows in a live system and can be shot down.
//   Supply  the taker buys the goods at the nearest market that has them (your credits, as before), carries them along the
//           lanes and puts them into your depot's store.
//   Haul    the taker loads the goods at your depot, carries them to the nearest market that deals with you and sells them
//           there (the proceeds are yours).
//   Mine    the taker flies to your depot's system and mines its rocks: out of sight at a miner's rate, live drilling a real
//           rock and unloading at your depot, until the tonnes are cut.
//   Guard   the taker flies in and stands guard over the depot for 20 minutes (its guns +50% only while it's there).
// Its fee is paid when the job is done. A taker shot down fails the job: no fee, and what it carried is salvage.
const PJR={hop:45,mine:.35,cls:{supply:'freighter',haul:'freighter',mine:'prospector',guard:'striker'}};
function pjRuns(){return S.pjRuns=S.pjRuns||[]}
function pjRunOf(id){return pjRuns().find(r=>String(r.id)===String(id))||null}
function pjJob(r){return pjList().find(j=>j.id===r.job)}
function pjRunEnd(r,ok,why){const j=pjJob(r),R=j&&S.stations[j.sid],P=j&&xPilotOfKey(j.pid);const i=pjRuns().indexOf(r);if(i>=0)pjRuns().splice(i,1);if(!j||j.state==='done')return;
  if(ok&&P&&R){const fee=payFrom(P,j.by,Math.min(Math.round(j.bid*(r.feeK!=null?r.feeK:1)),P.credits));eco(R,'jobs',-fee,`${j.who}'s fee`);j.paid=fee;j.msg=`done by ${j.who}:${why?' '+why+',':''} paid ${fmt(fee)} cr`;keyFeed(j.pid,`📋 ${pjTitle(j)}: ${j.msg}.`,'good')}
  else{j.msg=`failed: ${why||'the contractor was lost'}`;if(j.pid)keyFeed(j.pid,`📋 ${pjTitle(j)}: ${j.msg}.`,'bad')}j.state='done'}
// a taker signs on: where it starts, what it carries
function pjRunStart(j){const R=S.stations[j.sid],P=xPilotOfKey(j.pid);if(!R||!P)return;const side=j.by;let from=R.sid,to=R.sid,load={},D=null;
  if(j.kind==='supply'){const s=pjSrc(R,j.item,'supply',P);if(!s){pjRunEnd({job:j.id},false,'no market has it');return}D=s.D;const mk=mkStock(D),pr=Math.ceil(stPrice(D,j.item));const n=Math.min(j.n,mk[j.item]||0,Math.floor(P.credits/pr));
    if(n<=0){pjRunEnd({job:j.id},false,'nothing bought');return}inv.take(mk,j.item,n);load[j.item]=n;{const paid=payFrom(P,D.owner,n*pr);if(ITEMS[j.item].maker&&typeof ceSale==='function')ceSale(ITEMS[j.item].maker,j.item,n,paid,D.owner==='neutral'?'neutral':D.owner,D.sid)}eco(R,'jobs',-n*pr,`${n} ${ITEMS[j.item].name} bought at ${D.name}`);from=D.sid}
  else if(j.kind==='haul'){const s=pjSrc(R,j.item,'haul',P);if(!s){pjRunEnd({job:j.id},false,'no market will take it');return}D=s.D;const n=Math.min(j.n,R.stock[j.item]||0);if(n<=0){pjRunEnd({job:j.id},false,'nothing in the store to haul');return}
    inv.take(R.stock,j.item,n);load[j.item]=n;to=D.sid}
  else{const s=pjSrc(R,'fe','haul',P)||pjSrc(R,'fe','supply',P);if(s)from=s.D.sid}
  const r={id:S.nextId++,job:j.id,kind:j.kind,side,cls:PJR.cls[j.kind],from,to,dst:D?D.sid:R.sid,depot:R.sid,path:trPath(from,to)||[from],leg:0,sector:from,next:S.T+PJR.hop*.5,load,state:'go',cut:0,T0:S.T};
  pjRuns().push(r);j.run=r.id;j.due=1e12;if(WORLDS[r.sector])inW(WORLDS[r.sector],()=>pjSpawn(r,false))}
// arriving: what each kind does at the end of its route
function pjArrive(r){const j=pjJob(r),R=j&&S.stations[j.sid],P=j&&xPilotOfKey(j.pid);if(!j||!R||R.owner!=='player'||!P){if(Object.keys(r.load).length)toDebris(S.sectors[r.sector],r.load);r.load={};pjRunEnd(r,false,'the depot is gone');return}
  if(r.kind==='supply'){const n=r.load[j.item]||0;inv.addAll(R.stock,r.load);r.load={};pjRunEnd(r,true,`${n} of ${j.n} brought in`);return}
  if(r.kind==='haul'){
    // back at the depot with what the market couldn't pay for
    if(r.back){inv.addAll(R.stock,r.load);r.load={};pjRunEnd(r,true,r.why);return}
    const D=S.stations[r.dst];const n=r.load[j.item]||0;if(!D){toDebris(S.sectors[r.sector],r.load);r.load={};pjRunEnd(r,false,'the market is gone');return}
    // the buyer takes only what it can pay for; the fee is scaled to what sold, and the rest rides home to the depot's store
    const f=D.owner,pr=Math.max(1,Math.floor(stPrice(D,j.item)*.95)),k=Math.min(n,Math.floor((S.econ.treasury[f]||0)/pr));if(k>0){inv.take(r.load,j.item,k);inv.add(mkStock(D),j.item,k)}
    const got=k?payTo(P,f,k*pr):0;if(k)eco(R,'jobs',got,`${k} ${ITEMS[j.item].name} sold at ${D.name}`);r.feeK=n?k/n:0;const why=`${k} sold for ${fmt(got)} cr`;
    if(Object.keys(r.load).some(x=>r.load[x]>0)){r.back=1;r.why=`${why}, ${n-k} brought back`;r.from=D.sid;r.to=R.sid;r.dst=R.sid;r.path=trPath(D.sid,R.sid)||[D.sid];r.leg=0;r.sector=D.sid;r.next=S.T+PJR.hop*.5;return}
    pjRunEnd(r,true,why);return}
  r.state='work';r.until=S.T+(r.kind==='guard'?PJB.guardT:1e12)}
// the clock: hops along the lanes out of sight, mining and guarding at the depot
function pjRunsTick(){if(NET.cl||!S)return;for(const r of pjRuns().slice()){if(r.live)continue;const j=pjJob(r);
  // the job ended under it (the depot lost, the job cancelled): what it carries is dumped where it is
  if(!j||j.state==='done'){if(Object.keys(r.load||{}).length&&S.sectors[r.sector])toDebris(S.sectors[r.sector],r.load);r.load={};pjRuns().splice(pjRuns().indexOf(r),1);continue}
  if(r.state==='work'){const R=S.stations[r.depot];if(!R||R.owner!=='player'){pjRunEnd(r,false,'the depot is gone');continue}
    if(r.kind==='guard'){if(S.T>=r.until)pjRunEnd(r,true,'20 minutes on guard');continue}
    if(r.kind==='mine'&&!WORLDS[r.depot]){const got=extract(S.sectors[r.depot],sRound(PJR.mine*10));const m=invMass(got);inv.addAll(R.stock,got);r.cut+=m;if(r.cut>=j.n||!m)pjRunEnd(r,true,`${Math.round(r.cut)} t cut`)}continue}
  if(S.T<r.next)continue;if(r.leg>=r.path.length-1){pjArrive(r);continue}
  r.leg++;r.sector=r.path[r.leg];r.next=S.T+PJR.hop;if(WORLDS[r.sector])inW(WORLDS[r.sector],()=>pjSpawn(r,true))}}
{const o=pjTick;pjTick=function(){const x=o.apply(this,arguments);try{for(const j of pjList())if(j.state==='taken'&&!j.run)pjRunStart(j);pjRunsTick()}catch(e){console.error(e)}return x}}
// a depot is only guarded while its guard is there
{const o=depGunK;depGunK=function(SE,t){const R=SE&&SE.rec;if(R&&R.owner==='player'){const g=pjList().find(j=>j.sid===R.sid&&j.kind==='guard'&&j.state==='taken');if(g){const r=pjRunOf(g.run);if(!r||r.state!=='work'){const st=g.state;g.state='x';try{return o.apply(this,arguments)}finally{g.state=st}}}}return o.apply(this,arguments)}}
// ---- live: the taker's ship
function pjSpawn(r,arrive){if(r.live||!W)return;const role=r.kind==='guard'?'patrol':r.kind==='mine'&&r.state==='work'?'miner':'hauler';
  const e=makeNPC(role,r.side,r.cls,1,{},`pj:${r.id}`);e.cargo=r.load;r.load={};e.pjRun=r.id;r.live=true;const gs=GATES[W.sid]||[],prev=r.path[r.leg-1],nxt=r.path[r.leg+1],gin=gs.find(g=>g.to===prev),SE=W.stationEnt;
  const at=gin||pick(gs);if(arrive&&gin){e.x=gin.x*.93;e.y=gin.y*.93;e.z=gin.z*.93;fxWarp(e,sideCol(r.side))}else if(r.state==='work'&&SE){const o=rdir(1);e.x=SE.x+o.x*400;e.y=SE.y+o.y*200;e.z=SE.z+o.z*400}else if(at){e.x=at.x*.9;e.y=at.y*.9;e.z=at.z*.9}
  faceInstant(e,-e.x,-e.y,-e.z);e.pjName=r.kind;W.ents.push(e);return e}
function pjLeave(e,r){const j=pjJob(r);return j&&r.state!=='work'&&r.leg<r.path.length-1?(W.ents.find(x=>x.type==='gate'&&x.to===r.path[r.leg+1])||null):null}
{const o=npcThink;npcThink=function(e,dt){if(e.pjRun&&!NET.cl){const r=pjRunOf(e.pjRun);if(!r){e.role='leave';e.pjRun=null;return o.apply(this,arguments)}
  const SE=W.stationEnt,j=pjJob(r);e.ai.t-=dt;e.life+=dt;
  // en route: the gate to the next hop, or the station at the end
  if(r.state!=='work'){const g=pjLeave(e,r);if(g){npcGateJump(e,g,dt,.8);return}const D=SE;if(D){const d=steer(e,D.x,D.y,D.z,dt,true,.8);faceTo(e,D,dt);if(d<(D.r||150)+60){r.arrived=true;despawn(e)}return}e.role='leave';return o.apply(this,arguments)}
  if(r.kind==='guard'){if(S.T>=r.until){r.done=true;e.role='leave';e.pjRun=null;pjRunEnd(r,true,'20 minutes on guard');return o.apply(this,arguments)}e.role='patrol';return o.apply(this,arguments)}
  // mining live: drill a real rock, unload into the depot's store when full or when the tonnes are cut
  const R=S.stations[r.depot],s=S.sectors[W.sid],need=j?j.n-r.cut:0,full=invMass(e.cargo)>=Math.min(e.st.cargo,need);
  if(full||need<=0){if(SE&&R){const d=steer(e,SE.x,SE.y,SE.z,dt,true);faceTo(e,SE,dt);if(d<160){const m=invMass(e.cargo);inv.addAll(R.stock,e.cargo);e.cargo={};r.cut+=m;if(r.cut>=j.n){r.done=true;e.role='leave';e.pjRun=null;pjRunEnd(r,true,`${Math.round(r.cut)} t cut`)}}}return}
  let a=e.ai.ast;if(!a||!s.ast.includes(a)){a=s.ast.filter(x=>!x.comet&&oreTotal(x)>0).sort((p,q)=>d3(p,e)-d3(q,e))[0];e.ai.ast=a}if(!a){pjRunEnd(r,true,`${Math.round(r.cut)} t cut (the rocks ran out)`);e.role='leave';e.pjRun=null;return}
  const d=d3(a,e),rr=astR(a);if(d>rr+150){steer(e,a.x,a.y,a.z,dt,true);faceTo(e,a,dt);return}brake(e,dt);if(faceTo(e,a,dt)<.3){e.mining=a;e.mineAcc+=PJR.mine*dt;while(e.mineAcc>=1){e.mineAcc-=1;const k=mainOre(a);if(!k)break;a.ore[k]--;if(!a.ore[k])delete a.ore[k];inv.add(e.cargo,k,1);if(oreTotal(a)<=0){removeAst(s,a);e.ai.ast=null;break}}}return}
  return o.apply(this,arguments)}}
// the ship leaves the world: its hold goes back aboard the run; through a gate it's on its next hop, at the station it has arrived
{const o=returnHome;returnHome=function(e){if(e&&e.pjRun){const r=pjRunOf(e.pjRun);if(r){inv.addAll(r.load,e.cargo);inv.addAll(r.load,e.load);e.cargo={};e.load={};r.live=false;
  if(r.arrived){r.arrived=false;r.leg=r.path.length-1;r.next=S.T;pjArrive(r);if(r.state==='work'&&pjRuns().includes(r)&&W&&W.sid===r.depot){r.respawn=true}}else if(r.state!=='work'&&r.leg<r.path.length-1&&e.gj){r.leg++;r.sector=r.path[r.leg];r.next=S.T+PJR.hop;if(WORLDS[r.sector])inW(WORLDS[r.sector],()=>pjSpawn(r,true))}}}return o.apply(this,arguments)}}
{const o=killShip;killShip=function(e){if(e&&e.pjRun){const r=pjRunOf(e.pjRun);e.pjRun=null;if(r){r.live=false;const j=pjJob(r);pjRunEnd(r,false,`the ${j?j.who.replace(/^an? /,''):'contractor'}'s ship was shot down in ${DEF[W.sid].name}`)}}return o.apply(this,arguments)}}
{const o=holderIn;holderIn=function(st,path){if(typeof path==='string'&&path.startsWith('pj:')){const r=(st.pjRuns||[]).find(x=>String(x.id)===path.split(':')[1]);return r?(r.load=r.load||{}):st.econ.stock.neutral||st.econ.stock.pirate}return o.apply(this,arguments)}}
{const o=ledger;ledger=function(){const r=o.apply(this,arguments);try{const L=r.L['Fleets in muster'];for(const x of S.pjRuns||[]){const v=invVec(x.load||{});for(const e of RAWS){L[e]+=v[e];r.tot[e]+=v[e]}}}catch(e){}return r}}
// a system that opens with a taker in it: the ship is there
{const o=openWorld;openWorld=function(sid){const w=o.apply(this,arguments);try{if(!NET.cl&&S)inW(w,()=>{for(const r of pjRuns())if(r.sector===sid||(r.state==='work'&&r.depot===sid)){r.live=false;pjSpawn(r,false)}})}catch(e){console.error(e)}return w}}
// the run's line on the job (Post jobs tab)
function pjRunLine(j){const r=pjRunOf(j.run);if(!r)return'';return r.state==='work'?(r.kind==='guard'?`on guard, ${fmtT(Math.max(0,r.until-S.T))} left`:`mining: ${Math.round(r.cut)} of ${j.n} t`):`in ${DEF[r.sector].name}${r.leg<r.path.length-1?`, ${r.path.length-1-r.leg} jump${r.path.length-1-r.leg>1?'s':''} out`:''}`}
{const o=populate;populate=function(initial){try{if(W&&!NET.cl)for(const r of pjRuns())if(r.respawn&&!r.live&&r.depot===W.sid){r.respawn=false;pjSpawn(r,false)}}catch(e){console.error(e)}return o.apply(this,arguments)}}
// a contractor's label: whose pilot, and on what job
{const o=shipLabel;shipLabel=function(e){if(e&&e.pjName){const k=PJB.kinds[e.pjName]||'';return`${e.side==='neutral'?'Compact':FAC(e.side)?FAC(e.side).short:sideName(e.side)} contractor${k?' · '+k:''}`}return o.apply(this,arguments)}}
