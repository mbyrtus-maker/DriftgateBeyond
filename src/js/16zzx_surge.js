//@src 16zzx_surge.js
// ============================================================ Beyond: Brood surges (6 Nov 2026; the user's proposal of 5 Nov, built)
// The more the powers fight, the more the Brood surges: the salvage their wars leave behind fills a galaxy-wide surge meter;
// full, the Brood throws one big, telegraphed wave at one system on the edge of its space, and the meter empties.
//   - The meter: every ship destroyed and every load blown into debris adds its worth (a capital a lot, a fighter a little),
//     double next to Brood space; the Brood's own losses and anything inside Brood space don't count. It drains a tenth an hour.
//   - The bar: SURGE.bar credits' worth of salvage, less the more systems the Brood holds (a spreading Brood surges more
//     often); a surge that is beaten off raises the next bar by a quarter. At most one surge at a time, 30 minutes apart.
//   - The target: a system next to Brood space that isn't the Brood's, with a station or outpost to take, where the most
//     salvage was made lately (the Brood goes where the dead are), else the richest.
//   - Two minutes' warning (galaxy-wide news), then the wave: a Brood offensive SURGE.k times the size of an ordinary one (up
//     to SURGE.max ships), from the Brood's stores, coming through the gates from Brood space.
// The Bloom eats the salvage it counts: debris in and next to Brood space feeds a surge mass the wave is grown from.
// The galaxy map shows the gauge ("The Bloom stirs").
let STRAT_SURGE_SKIP=false;
const SURGE={feed:.03,cap:{fe:500,cu:300,ir:200,xc:40},bar:60000,shrink:.2,drain:.1,near:2,gap:1800,warn:120,k:2.2,max:30,min:8,hold:1.25};
function surgeOf(){const g=S.surge=S.surge||{m:0,bar:SURGE.bar,k:1,last:-1e9,at:{}};g.store=g.store||{};return g}
function surgeBar(){const g=surgeOf(),n=controlCounts().brood||0;return g.bar*g.k/(1+SURGE.shrink*n)}
function surgeNear(sid){if(!sid||broodHeld(sid))return 0;return NEIGH[sid].some(n=>broodHeld(n))?SURGE.near:1}
function surgeFeed(sid,v){if(!S||!(v>0))return;const w=surgeNear(sid);if(!w)return;const g=surgeOf();g.m+=v*w;g.at[sid]=(g.at[sid]||0)+v*w}
// fed by what's blown apart: debris (off-screen battles, wrecked holds and kits) and ships killed live
{const o=toDebris;toDebris=function(s,inv0){try{if(S&&S.sectors&&!STRAT_SURGE_SKIP){const sid=Object.keys(S.sectors).find(k=>S.sectors[k]===s);if(sid)surgeFeed(sid,invValue(inv0||{}))}}catch(e){}return o.apply(this,arguments)}}
{const o=killShip;killShip=function(e){try{if(e&&e.alive&&e.side!=='brood'&&e.role!=='limpet'&&W)surgeFeed(W.sid,invValue(e.load||{})+invValue(e.cargo||{})+(e.role==='frigate'?3000:150))}catch(err){}return o.apply(this,arguments)}}
// the Bloom feeds on the dead: it draws the war's debris out of its own systems and the systems next to them into its
// surge mass (S.surge.store, up to what one big surge takes: SURGE.cap), and grows the surge from it; nothing is created, the debris is real (blown out of ships and holds)
function surgeZone(){const t=territory('brood'),z=new Set(t);for(const id of t)for(const n of NEIGH[id])if(!(DEF[n].home&&DEF[n].kind==='core'))z.add(n);return z}
function surgeHarvest(){const g=surgeOf();for(const id of surgeZone()){const d=S.sectors[id]&&S.sectors[id].debris;if(!d)continue;for(const e in SURGE.cap){const m=Math.min(d[e]||0,Math.ceil((d[e]||0)*SURGE.feed),SURGE.cap[e]-(g.store[e]||0));if(m>0){d[e]-=m;inv.add(g.store,e,m)}}}}
// make n of an item in a store from what the store holds, its parts first
function surgeCraft(st,item,n){const r=ITEMS[item]&&ITEMS[item].recipe;if(!r)return;let k=0;while((st[item]||0)<n&&k<200){k++;for(const x in r)if((st[x]||0)<r[x])surgeCraft(st,x,r[x]);if(!haveIn(r,[st]))return;takeFrom(r,[st]);inv.add(st,item,1)}}
function surgeFit(ld,srcs,st){if(haveIn(ld,srcs))return true;for(const x in ld){let have=0;for(const s of srcs)have+=s[x]||0;if(have<ld[x])surgeCraft(st,x,(st[x]||0)+ld[x]-have)}return haveIn(ld,srcs)}
{const o=ledger;ledger=function(){const r=o.apply(this,arguments);try{const L=r.L['Faction & Unbound stores'],v=invVec((S.surge&&S.surge.store)||{});for(const e of RAWS){L[e]+=v[e];r.tot[e]+=v[e]}}catch(e){}return r}}
// the target: on the edge of Brood space, held by someone else, with something to take
function surgeTarget(){const g=surgeOf(),c=[];for(const d of SECTOR_DEFS){const sid=d.id;if(broodHeld(sid)||!NEIGH[sid].some(n=>broodHeld(n)))continue;
    const R=S.stations[sid],oid=OUT_BY_SECTOR[sid],o=oid&&S.outposts[oid];let tgt=null;
    if(R&&R.kind!=='hive'&&R.owner!=='brood'&&fightsAt('brood',R.owner))tgt={st:sid};else if(o&&o.owner!=='brood'&&o.owner!=='pirate')tgt={out:oid};if(!tgt)continue;
    if(S.events.some(e=>e.type==='offensive'&&e.stage!=='done'&&e.att==='brood'&&(tgt.st?e.st===sid:e.target===tgt.out)))continue;
    const sal=g.at[sid]||0,rich=R?invValue(storeOf(R)||{})*.05:(o?invValue(o.stock||{})*.05:0);c.push([{sid,tgt},1+sal+rich])}
  if(!c.length)return null;c.sort((a,b)=>b[1]-a[1]);return c[0][0]}
function surgeLaunch(){const g=surgeOf(),T=surgeTarget();if(!T)return false;const f='brood',tier=factionTier(f),role='patrol',srcs=[g.store,S.econ.fleet[f],S.econ.stock[f]].filter(Boolean);
  const isSt=!!T.tgt.st,Rr=isSt?S.stations[T.tgt.st]:null,o=isSt?null:S.outposts[T.tgt.out],lvl=isSt?(Rr.kind==='core'?4:2):o.level;
  const base=clamp(3+lvl+1+BAL.brN,4,BRSW.max),n=clamp(Math.round(base*SURGE.k),SURGE.min,SURGE.max),nb=isSt?Math.max(4,Math.floor(n/2)):Math.max(2,Math.floor(n/3));
  const force={},cls=[];let got=0;for(let i=0;i<n;i++){const want=i<nb?bmbPick(f,i,role,tier,srcs):pickFighter(role);let cl=want,ld=loadout(role,tier,cl);if(!surgeFit(ld,srcs,g.store)){cl='striker';ld=loadout(role,tier,cl);surgeFit(ld,srcs,g.store)}if(takeFrom(ld,srcs)){inv.addAll(force,ld);cls.push(cl);got++}else break}
  if(got<SURGE.min){inv.addAll(g.store,force);return false}
  const ev={id:S.nextId++,type:'offensive',att:f,target:isSt?null:T.tgt.out,st:isSt?T.tgt.st:undefined,stName:isSt?Rr.name:o.name,sector:T.sid,eta:S.T+SURGE.warn,force,n:got,tier,cls,stage:'inbound',surge:1,trDone:1};
  S.events.push(ev);g.m=0;g.at={};g.last=S.T;g.live=ev.id;g.tev={st:ev.st,target:ev.target};
  allFeed(`☣ Brood surge: the Bloom is spilling toward ${DEF[T.sid].name}${isSt?` (${Rr.name})`:''}. ${got} Brood ships, 2 minutes.`,'bad');try{announce(ev)}catch(e){}return true}
function surgeTick(){if(NET.cl||!S||S.training)return;const g=surgeOf();surgeHarvest();g.m=Math.max(0,g.m*(1-SURGE.drain*10/3600));for(const k in g.at){g.at[k]*=1-1.5*10/3600;if(g.at[k]<1)delete g.at[k]}
  if(g.live){const ev=S.events.find(e=>e.id===g.live);if(!ev||ev.stage==='done'){const held=!surgeFell(g.tev||ev||{});g.live=null;if(held){g.k*=SURGE.hold;allFeed(`✔ The Brood surge was beaten off. The Bloom draws back.`,'good')}else{g.k=1;allFeed(`☣ The Brood surge broke through.`,'bad')}}return}
  if(S.T-g.last<SURGE.gap||S.T<600)return;const bar=surgeBar();if(!g.half&&g.m>=bar*.5){g.half=1;allFeed('The Bloom stirs: the war\'s dead are feeding it.','news')}
  if(g.m>=bar&&S.T>=(g.retry||0)){if(surgeLaunch())g.half=0;else g.retry=S.T+120}}
function surgeFell(ev){if(!ev.st&&!ev.target)return false;if(ev.st){const R=S.stations[ev.st];return!R||R.owner==='brood'}const o=S.outposts[ev.target];return!!o&&o.owner==='brood'}
{const o=strategicTick;strategicTick=function(){const x=o.apply(this,arguments);try{surgeTick()}catch(e){console.error(e)}return x}}
// the gauge on the galaxy map
{const o=mapSectorNow;mapSectorNow=function(sid){let h=o.apply(this,arguments);try{if(DEF[sid].kind==='hive'||broodHeld(sid)){const g=surgeOf(),p=Math.min(100,Math.round(g.m/surgeBar()*100));h+=`<span>The Bloom stirs</span><b style="color:${FACTIONS.brood.col}">${g.live?'surging now':p+'% to the next surge'}</b>`}}catch(e){}return h}}
