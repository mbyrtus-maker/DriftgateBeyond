//@src 16zzy_bloom.js
// ============================================================ Beyond: the Bloom grows from raw ore (user, 6 Nov 2026)
// The user: "All Brood ships are just made with ore. All Brood upgrades are made with just ore, they do not need parts or kits
// or anything. Rework the build priority order to make sure it has enough defence, then do upgrades to the nodes, then do
// capital ships." (Earlier: "The Brood nodes upgrade with weapons, hull and shields, and make capitals.")
//   - Ore, not parts. Whatever the Brood builds (a fighter, a miner, a Seeder's frames, Overgrowth, a node module, a capital)
//     costs the mass of ore its kit would be made of (Alloy Plate is 3 t, a Siege Torpedo 13 t, and so on), in whatever ore
//     it has. When a Brood store is asked for a kit it hasn't got, it grows the missing parts there and then from its ore,
//     most plentiful ore first. The ore changes kind but not mass: the ledger books the change as "Bloom transmutation"
//     (S.bxm), so it stays exact.
//   - The order it spends in: 1. defence (its garrisons at the hive and every node made up to strength, its miners, the
//     Overgrowth it grows against carriers, ships sent to answer an attack); 2. node upgrades; 3. capital ships; 4. everything
//     else (swarms, surges, Seeders for new nodes, ordinary Overgrowth, capital wings). Each takes only the ore left over
//     after what the steps before it still need (bloomHold: the garrisons' missing ships, then the next node module, then
//     the next capital).
//   - Bloom Nodes grow: every 60 to 100 seconds a module on one node, weapons (the defence platform) or hull and shields
//     (the hull and shield works), up to level 3 each (depot level 3). No crew. Nodes facing an enemy grow first, hull first.
//     Paid from the node's own store first, then the hive.
//   - Capitals: the Leviathan (one at a time, from minute BAL.brLevT) and Prowlers (up to 2), grown at the Bloom Node nearest
//     the enemy, of ore.
const BLOOM={every:[60,100],max:{def:3,armor:3},front:3};
let BRP='swarm';   // the spending step of the Brood build in progress: def, up, cap or swarm
function bloomNodes(){return Object.values(S.stations).filter(R=>R&&R.owner==='brood'&&R.kind==='depot')}
function bloomFront(R){return NEIGH[R.sid].some(n=>{const o=sideNorm(sectorOwner(n));return o&&o!=='brood'&&o!=='neutral'&&hostile('brood',o)})||(S.frigates||[]).some(t=>t.hull>0&&t.side!=='brood'&&hostile('brood',t.side)&&(t.sector===R.sid||NEIGH[R.sid].includes(t.sector)))}
function bloomMass(kit){let m=0;const v=invVec(kit);for(const e of RAWS)m+=v[e];return Math.ceil(m)}
function oreMass(st){let m=0;for(const e of RAWS)m+=st&&st[e]||0;return m}
// ---- what each step still needs (in tonnes of ore)
function bloomNeedDef(){let n=0;const km=bloomMass(loadout('patrol',factionTier('brood')||1,'striker'));for(const k in S.gar||{}){const ro=S.gar[k];if(ro.f!=='brood')continue;const st=grSite(k);if(!st)continue;n+=Math.max(0,grTarget(st)-ro.m.length)*km}return n}
function bloomNextUp(){let best=null;for(const R of bloomNodes()){const d=devOf(R),fr=bloomFront(R);for(const k of['armor','def']){if((d[k]||0)>=BLOOM.max[k]||!devNext(R,k))continue;const m=bloomMass(devNext(R,k)),w=(fr?0:1e6)+m;if(!best||w<best.w)best={R,k,m,w}}}return best}
function bloomNextCap(){const f='brood';if(S.T<BAL.brLevT||!bloomNodes().length)return null;const busy=t=>S.events.some(e=>e.type===t&&e.att===f&&e.stage!=='done');
  if(!busy('frigbuild')&&facCar(f).length<1)return{type:'frigbuild',m:bloomMass(withSeal(CARRIER_COST,f,CAP_SEAL.carrier))};
  if(!busy('escbuild')&&facEsc(f).length<(ESC_CAP[f]||0))return{type:'escbuild',m:bloomMass(escCost(f))};return null}
// ore the hive holds back from a step for the steps before it
function bloomHold(step){if(step==='def')return 0;let h=bloomNeedDef();if(step==='up')return h;const u=bloomNextUp();h+=u?u.m:0;if(step==='cap')return h;const c=bloomNextCap();return h+(c?c.m:0)}
// ---- ore into parts: grow `want` (item→count) in store `into`, from the ore in `pools` (hive spare after the hold first
// spent from the other pools); books the change of kind in S.bxm
function bloomGrow(into,want,pools,hold){const M=bloomMass(want);if(M<=0)return true;const hv=S.econ.stock.brood;
  const L=[];for(const p of pools){if(!p)continue;const lim=p===hv?Math.max(0,oreMass(p)-hold):oreMass(p);if(lim<=0)continue;L.push([p,lim])}
  let have=0;for(const[,l]of L)have+=l;if(have<M)return false;
  const took={};let left=M;for(const[p,lim]of L){let room=lim;const es=RAWS.filter(e=>(p[e]||0)>0).sort((a,b)=>(p[b]||0)-(p[a]||0));for(const e of es){if(left<=0||room<=0)break;const q=Math.min(p[e],left,room);inv.take(p,e,q);took[e]=(took[e]||0)+q;left-=q;room-=q}if(left<=0)break}
  const made=invVec(want);S.bxm=S.bxm||{};for(const e of RAWS){const d=(took[e]||0)-(made[e]||0);if(d)S.bxm[e]=(S.bxm[e]||0)+d}
  for(const k in want)inv.add(into,k,want[k]);return true}
let BSC={t:-1,set:null};
function isBroodStore(s){if(!s||!S||!S.econ)return false;if(s===S.econ.stock.brood||s===S.econ.fleet.brood||(S.surge&&s===S.surge.store))return true;if(BSC.t!==S.T||BSC.S!==S){BSC={t:S.T,S,set:new Set(bloomNodes().map(R=>dStore(R)))}}return BSC.set.has(s)}
// any kit asked of a Brood store is grown from ore when the parts aren't there (within the current step's share)
{const o=haveIn;haveIn=function(req,srcs){const r=o.apply(this,arguments);if(r||!S||!srcs||NET.cl)return r;
  try{const bs=srcs.filter(isBroodStore);if(!bs.length)return r;const want={};for(const k in req){let h=0;for(const s of srcs)h+=s&&s[k]||0;if(h<req[k])want[k]=req[k]-h}
    const hv=S.econ.stock.brood,pools=[...bs.filter(s=>s!==hv),hv];if(!bloomGrow(bs[0],want,pools,bloomHold(BRP)))return false}catch(e){console.error(e);return r}
  return o.apply(this,arguments)}}
{const o=ledger;ledger=function(){const r=o.apply(this,arguments);try{const L=r.L['Faction & Unbound stores'];for(const e of RAWS){const d=(S.bxm&&S.bxm[e])||0;L[e]+=d;r.tot[e]+=d}}catch(e){}return r}}
// the step each kind of build belongs to
function bloomStep(step,fn){return function(){const p=BRP;BRP=step;try{return fn.apply(this,arguments)}finally{BRP=p}}}
grKit=bloomStep('def',grKit);mrKit=bloomStep('def',mrKit);dispatchResponse=bloomStep('def',dispatchResponse);ogGuardTick=bloomStep('def',ogGuardTick);
// ---- a Bloom Node needs no crew
{const o=devCap;devCap=function(R){if(R&&R.owner==='brood'&&R.kind==='depot')return 99;return o.apply(this,arguments)}}
// pay a growth's mass from the node's own store, then the hive (within the step's share)
function bloomPay(R,M,step){const want={};let left=M;const ds=R?dStore(R):null,took={};
  if(ds)for(const e of RAWS.filter(e=>(ds[e]||0)>0).sort((a,b)=>ds[b]-ds[a])){if(left<=0)break;const q=Math.min(ds[e],left);left-=q;took[e]=q}
  const hv=S.econ.stock.brood,room=Math.max(0,oreMass(hv)-bloomHold(step));if(left>room)return null;
  for(const e in took)inv.take(ds,e,took[e]);for(const e of RAWS.filter(e=>(hv[e]||0)>0).sort((a,b)=>hv[b]-hv[a])){if(left<=0)break;const q=Math.min(hv[e],left);inv.take(hv,e,q);took[e]=(took[e]||0)+q;left-=q}return took}
function bloomGrowTick(){if(NET.cl||!S||S.training)return;const A=S.ai.brood=S.ai.brood||{};if(A.grow===undefined)A.grow=S.T+rnd(...BLOOM.every);if(S.T<A.grow)return;A.grow=S.T+rnd(...BLOOM.every);
  const u=bloomNextUp();if(!u)return;const{R,k}=u,cost=bloomPay(R,u.m,'up');if(!cost)return;
  inv.addAll(R.fort,cost);devOf(R)[k]++;if(R.wk&&R.wk[k]!==undefined)R.wk[k]+=WK_HP[k];applyDev(R);
  if(covered(R.sid)||W&&W.sid===R.sid)feed(`⚠ ${R.name} in ${DEF[R.sid].name} has grown ${k==='def'?'more spore batteries':'a thicker carapace'} (level ${depotLevel(R)}).`,'warn')}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{bloomGrowTick()}catch(e){console.error(e)}return r}}
CAP_BROOD_OWN=true;
// capitals, once defence and the next node upgrade are covered
function bloomCapTick(){if(NET.cl||!S||S.training)return;const T=S.T,f='brood',A=S.ai.brood=S.ai.brood||{};if(T<(A.capT||0))return;A.capT=T+rnd(40,70);
  const c=bloomNextCap();if(!c)return;const L=bloomNodes();
  const fr=L.filter(bloomFront),P=(fr.length?fr:L).slice().sort((a,b)=>invMass(dStore(b))-invMass(dStore(a)));for(const R of P){const kit=bloomPay(R,c.m,'cap');if(!kit)continue;
    S.events.push({id:S.nextId++,type:c.type,t0:T,yard:f,att:f,sector:R.sid,force:kit,until:T+(c.type==='escbuild'?ESCORT_TIME:FRIGATE_TIME),stage:'building',bloom:1});
    if(covered(R.sid))feed(`⚠ ${R.name} in ${DEF[R.sid].name} is swelling: the Brood is growing a ${c.type==='escbuild'?'Prowler':'Leviathan'} there.`,'warn');return}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{bloomCapTick()}catch(e){console.error(e)}return r}}
