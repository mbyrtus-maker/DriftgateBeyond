//@src 16zzq_raiders.js
// ============================================================ Beyond: raiders are tracked (live space stage 3, 6 Nov 2026)
// No chance-spawned raider or Unbound wings any more. Every hostile wing out on the lanes is a tracked raid party (S.raids,
// 16_expansion.js): a raid on a convoy or depot, as before, or now a prowl: a party sent to a hunting ground with no target,
// waiting there a few minutes for whatever comes through (the Unbound out of the Wrack into the deep, the void, the hubs and
// the contested systems; a power's raiders into an enemy's border systems; the Brood around its own territory), then home.
// A prowl springs on any hostile convoy that comes through. Off-screen, raiders meeting a hostile garrison fight it by the
// odds (the garrison cuts their chances and loses ships when it loses). And a power's offensive or build party, done, flies
// home along the lanes as a tracked party instead of landing back in its warehouse.
const PRW={rate:{fac:.012,brood:.008,pirate:.02},max:{fac:3,brood:2,pirate:5},cut:.85,winLf:.4,loseLf:.1,skirmish:.5};
RAID.max={...RAID.max,...PRW.max};
{const o=popWants;popWants=function(){return o.apply(this,arguments).filter(w=>w[0]!=='raider'&&w[0]!=='pirate')}}
// hunting grounds: where each side's raiders go looking
function prwGrounds(side,src){const out=[];for(const d of SECTOR_DEFS){const id=d.id,h=HOP[src.sid][id];if(h===undefined||h<1||h>src.reach+1)continue;
  if(side==='pirate'){if(!PIR_OK0.has(id)&&!(src.cap&&PIR_OK.has(id)))continue;const w={deep:3,void:2,hub:2,contested:2,frontier:1}[d.kind]||0;if(w)out.push([id,w])}
  else if(side==='brood'){if(d.kind==='hive'||!broodNear(id)||territory('brood').has(id))continue;out.push([id,1])}
  else{const ow=sectorOwner(id);if(!ow||ow===side||!hostile(side,ow)||d.kind==='core')continue;out.push([id,d.kind==='frontier'||d.kind==='contested'?2:1])}}
  return out}
function prwSend(side){const kind=side==='pirate'?'pirate':side==='brood'?'brood':'fac',mine=(S.raids||[]).filter(r=>r.side===side&&!r.ret&&!r.strike);if(mine.length>=PRW.max[kind])return null;
  const srcL=raidSources(side).filter(s=>!mine.some(r=>r.src===s.sid&&S.T-r.T0<RAID.cool));if(!srcL.length)return null;const src=pick(srcL),G=prwGrounds(side,src);if(!G.length)return null;
  const c=wpickArr(G);const kit=raidShips(side,src.srcs);if(!kit)return null;const r=raidSend(side,{src,tgt:null,dep:null,c},kit);if(r){r.prowl=true;if(r.path.length===1&&r.state!=='wait'){r.state='wait';r.until=S.T+RAID.wait}}return r}
{const o=raidDispatch;raidDispatch=function(){const x=o.apply(this,arguments);try{if(S.T>=300)for(const side of[...FAC_IDS,'brood','pirate']){const kind=side==='pirate'?'pirate':side==='brood'?'brood':'fac';if(Math.random()<PRW.rate[kind])prwSend(side)}}catch(e){console.error(e)}return x}}
// a prowl stays out until its wait is up; it has no target to lose
{const o=raidStillOn;raidStillOn=function(r){if(r&&r.prowl&&!r.tgt&&!r.dep)return r.state!=='wait'||S.T<(r.until||0);return o.apply(this,arguments)}}
// a prowl waiting in a system springs on a hostile convoy that comes through (off-screen)
function prwCatch(){for(const r of S.raids||[]){if(!r.prowl||r.live||r.state!=='wait'||r.tgt||WORLDS[r.sector])continue;
  const t=(S.traders||[]).find(x=>x.sector===r.sector&&!x.live&&hostile(r.side,x.side)&&x.side!=='pirate'&&!(x.escWait>S.T)&&invValue(x.load||{})>=40);if(!t)continue;
  r.tgt=t.id;if(raidFight(r)){const i=S.traders.indexOf(t);if(i>=0)S.traders.splice(i,1)}}}
{const o=raidsTick;raidsTick=function(){const x=o.apply(this,arguments);try{if(!NET.cl&&S&&!S.training){prwCatch();prwSkirmishes()}}catch(e){console.error(e)}return x}}
// live: a prowl holds by one of the system's gates (the Unbound among the rocks when there are any), fighting what comes
{const o=raidGoal;raidGoal=function(r){if(r&&r.prowl&&!r.tgt&&!r.dep&&r.state!=='home'&&r.dest===W.sid){if(S.T>(r.until||0))return{gate:null};const gs=W.ents.filter(x=>x.type==='gate');if(!r.hold||!gs.some(g=>g.to===r.hold))r.hold=(pick(gs)||{}).to;const g=gs.find(x=>x.to===r.hold);return g?{hold:g,R:700}:{gate:null}}return o.apply(this,arguments)}}
{const o=raidSpawn;raidSpawn=function(r,arrive){const x=o.apply(this,arguments);try{if(r&&r.prowl&&r.side==='pirate'&&r.live&&!arrive&&DEF[W.sid].kind!=='den'){const g=Object.values(W.groups).find(g=>g.raid===r.id);if(g&&Math.random()<PIR_LURK)lurkPlan(g,true)}}catch(e){}return x}}
// ---- raiders against a garrison, off-screen
function prwGar(sid,side){const L=[];for(const k in S.gar||{}){const ro=S.gar[k];if(ro.sid!==sid||!hostile(side,ro.f))continue;if(ro.m.some(m=>!m.live))L.push(k)}return L}
function prwGarN(sid,side){let n=0;for(const k of prwGar(sid,side))n+=S.gar[k].m.filter(m=>!m.live).length;return n}
{const o=raidOdds;raidOdds=function(r,sid){const p=o.apply(this,arguments);try{const n=prwGarN(sid,r.side);if(n)return clamp(p*Math.pow(PRW.cut,n),.05,.95)}catch(e){}return p}}
function prwGarLoss(sid,side,lf){const s=S.sectors[sid];for(const k of prwGar(sid,side)){const force={},ships=grForce(k,force);grSettle(k,ships,force,lf,s)}}
// a raid's fight at a convoy or depot: the garrison there loses ships when the raiders win, a few when they don't
{const o=raidFight;raidFight=function(r){const sid=r&&r.sector,side=r&&r.side,n=sid?prwGarN(sid,side):0,had=S.raids.includes(r);const won=o.apply(this,arguments);
  try{if(n&&!WORLDS[sid])prwGarLoss(sid,side,won?PRW.winLf:(had&&!S.raids.includes(r)?PRW.loseLf:0))}catch(e){console.error(e)}return won}}
// a prowl waiting where a hostile garrison is: they fight it out
function prwSkirmishes(){for(const r of (S.raids||[]).slice()){if(!r.prowl||r.live||r.state!=='wait'||r.skT>S.T||WORLDS[r.sector])continue;const n=prwGarN(r.sector,r.side);if(!n)continue;r.skT=S.T+60;
  const win=Math.random()<raidOdds(r,r.sector,PRW.skirmish);
  if(win){prwGarLoss(r.sector,r.side,PRW.winLf);raidAttrition(r,r.sector);if(covered(r.sector)&&prwGar(r.sector,r.side).some(k=>friendSide(S.gar[k].f)))feed(`⚠ ${raidWho(r.side)} raiders mauled the patrol in ${DEF[r.sector].name}.`,'bad')}
  else{prwGarLoss(r.sector,r.side,PRW.loseLf);raidWipe(r,r.sector,prwGar(r.sector,r.side).some(k=>friendSide(S.gar[k].f))?`✔ The patrol in ${DEF[r.sector].name} broke up ${art(raidWho(r.side)).toLowerCase()} ${raidWho(r.side)} raiding party.`:null)}}}
// ---- a force done with its work flies home: a tracked party along the lanes, unloading into its warehouse there
function prwHome(side,sid,force){const home=homeOf(side);if(!force||!Object.keys(force).length)return null;
  if(!sid||sid===home||!(FAC_IDS.includes(side)||side==='brood'||side==='pirate')||!trPath(sid,home)){inv.addAll(S.econ.stock[side]||S.econ.stock.pirate,force);return null}
  const tier=side==='pirate'?pirateTier():factionTier(side)||1,ships=[],left={...force};for(let i=0;i<6;i++){let c=pickFighter('patrol'),ld=loadout(side==='pirate'?'pirate':'patrol',tier,c);if(!haveIn(ld,[left])){c='interceptor';ld=loadout(side==='pirate'?'pirate':'patrol',1,c)}if(!haveIn(ld,[left])&&ships.length)break;takeFrom(ld,[left]);ships.push({cls:c,tier,ld})}
  const r={id:S.nextId++,side,src:home,cap:null,tgt:null,dep:null,dest:home,sector:sid,path:trPath(sid,home),leg:0,next:S.T+RAID.hop,state:'home',ships,kit:{...force},loot:{},back:[],T0:S.T,ret:true};
  for(const k in force)delete force[k];(S.raids=S.raids||[]).push(r);if(WORLDS[sid])inW(WORLDS[sid],()=>raidSpawn(r,false));return r}
// ---- stage 3b: an offensive flies to its target. Formed at its side's home, the strike group travels the lanes hop by hop as
// a tracked party (a raid token with .strike), showing in any live system on its way; at the target it becomes the offensive
// again: it jumps in and fights live, or the battle is resolved out of sight as before.
function prwStrikeStart(ev){const from=homeOf(ev.att);if(!from||from===ev.sector){ev.trDone=1;return}const path=trPath(from,ev.sector);if(!path||path.length<2){ev.trDone=1;return}
  const ships=[];(ev.cls||[]).forEach(c=>ships.push({cls:c,tier:ev.tier,ld:loadout(ev.att==='pirate'?'pirate':'patrol',ev.tier,c)}));if(!ships.length){ev.trDone=1;return}
  const r={id:S.nextId++,side:ev.att,src:from,cap:null,tgt:null,dep:null,dest:ev.sector,sector:from,path,leg:0,next:S.T+RAID.hop,state:'out',ships,kit:{},loot:{},back:[],T0:S.T,strike:ev.id};
  inv.addAll(r.kit,ev.force);for(const k in ev.force)delete ev.force[k];ev.tr=r.id;ev.eta=1e12;(S.raids=S.raids||[]).push(r);if(WORLDS[r.sector])inW(WORLDS[r.sector],()=>raidSpawn(r,false))}
function prwStrikeHand(r){const ev=S.events.find(e=>e.id===r.strike);const i=S.raids.indexOf(r);if(i>=0)S.raids.splice(i,1);
  if(!ev||ev.stage==='done'){prwHome(r.side,r.sector,r.kit);r.kit={};return null}
  inv.addAll(ev.force,r.kit);r.kit={};ev.cls=r.ships.map(s=>s.cls);ev.n=r.ships.length;ev.tr=null;ev.trDone=1;ev.eta=S.T;
  if(ev.n<2){ev.stage='done';prwHome(ev.att,r.sector,ev.force);ev.force={};return null}return ev}
{const o=updateEvents;updateEvents=function(){try{if(!NET.cl)for(const ev of S.events||[])if(ev.type==='offensive'&&ev.stage==='inbound'&&!ev.tr&&!ev.trDone)prwStrikeStart(ev)}catch(e){console.error(e)}return o.apply(this,arguments)}}
{const o=raidStillOn;raidStillOn=function(r){if(r&&r.strike)return true;return o.apply(this,arguments)}}
{const o=raidArrive;raidArrive=function(r){if(r&&r.strike){prwStrikeHand(r);return}return o.apply(this,arguments)}}
// arriving in an open target system: the group jumps in as the offensive
{const o=raidSpawn;raidSpawn=function(r,arrive){if(r&&r.strike&&W&&W.sid===r.dest){const ev=prwStrikeHand(r);if(ev)engageOffensive(ev);return}return o.apply(this,arguments)}}
// a strike group wiped out on the way: the offensive is over
{const o=raidWipe;raidWipe=function(r,sid,msg){if(r&&r.strike){const ev=S.events.find(e=>e.id===r.strike);if(ev&&ev.stage!=='done'){ev.stage='done';ev.force={}}}return o.apply(this,arguments)}}
// a strike group cut down on the way turns for home: the offensive is called off and the survivors are a plain party home
{const o=raidHome;raidHome=function(r){if(r&&r.strike){const ev=S.events.find(e=>e.id===r.strike);if(ev&&ev.stage!=='done'){ev.stage='done';ev.force={}}r.strike=null;r.ret=true}return o.apply(this,arguments)}}
// ---- Varkesh's tougher hulls count in these fights too (6 Nov 2026): a raid on a convoy, a depot or a garrison is a battle
// nobody watches, so each side's toughK (FACTIONS[f].tough: Varkesh 1.12) shifts the odds as it does in offensives and sieges
function prwTough(p,att,def){const ka=toughK(att),kd=def?toughK(def):1;if(ka===kd)return p;const o=p/(1-p)*ka/kd;return clamp(o/(1+o),.05,.95)}
{const o=raidOdds;raidOdds=function(r,sid,base,owner){const p=o.apply(this,arguments);try{let def=owner;if(!def){const g=prwGar(sid,r.side);if(g.length)def=S.gar[g[0]].f;else{const R=S.stations[sid];if(R&&r.dep===sid)def=R.owner}}return prwTough(p,r.side,def)}catch(e){return p}}}
{const o=prwGarLoss;prwGarLoss=function(sid,side,lf){const s=S.sectors[sid];for(const k of prwGar(sid,side)){const force={},ships=grForce(k,force);grSettle(k,ships,force,lf/toughK(S.gar[k].f),s)}}}
