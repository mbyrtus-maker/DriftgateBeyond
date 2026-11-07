//@src 16zzy_bloom.js
// ============================================================ Beyond: the Bloom grows from raw ore (user, 6 Nov 2026)
// "The Brood don't need parts or components: they convert raw ore into depot upgrades and capital ships. The Brood nodes
// upgrade with weapons, hull and shields, and make capitals."
//   - Bloom Nodes grow: every minute or two the Brood grows a module on one of its nodes, weapons (the defence platform) or
//     hull and shields (the hull and shield works), up to level 3 each, so a node climbs to depot level 3. It needs no crew
//     (no life support) and no parts: it costs the mass of ore those modules are made of (Alloy Plate is 3 t, and so on), in
//     any ore it has to spare, from the node's own store first, then the hive's (the hive keeps BLOOM.keep back for its swarms). Nodes facing an
//     enemy (a hostile system or capital ship next door) grow first.
//   - Capitals from ore: a Leviathan or a Prowler costs the mass of ore its kit is made of, in any ore, not the kit, and it is grown at the
//     Bloom Node nearest the enemy (the hive if the Brood has none).
// The ledger stays exact: ore goes into the node's fortification or the capital's hold, and falls as debris when they die.
const BLOOM={every:[60,100],keep:{fe:150,cu:150},max:{def:3,armor:3},front:3};
function bloomNodes(){return Object.values(S.stations).filter(R=>R&&R.owner==='brood'&&R.kind==='depot')}
function bloomFront(R){return NEIGH[R.sid].some(n=>{const o=sideNorm(sectorOwner(n));return o&&o!=='brood'&&o!=='neutral'&&hostile('brood',o)})||(S.frigates||[]).some(t=>t.hull>0&&t.side!=='brood'&&hostile('brood',t.side)&&(t.sector===R.sid||NEIGH[R.sid].includes(t.sector)))}
// the Bloom eats rock, not recipes: a growth costs the mass of ore its kit would be made of, in whatever ore the Brood has to
// spare, the node's own store first, then the hive's (which keeps BLOOM.keep back for its swarms), the most plentiful first,
// and last the hive's spare Alloy Plate and Conduit, digested back (BLOOM.keepKit kept)
BLOOM.keep={fe:150,cu:150,ir:100,xc:50};BLOOM.keepKit={plate:60,wire:40};
function bloomMass(kit){let m=0;const v=invVec(kit);for(const e of RAWS)m+=v[e];return Math.ceil(m)}
function bloomPools(R){const L=[],hv=S.econ.stock.brood||{};if(R){const ds=dStore(R);for(const e of RAWS)if((ds[e]||0)>0)L.push([ds,e,ds[e]])}
  const hr=RAWS.map(e=>[hv,e,Math.max(0,(hv[e]||0)-(BLOOM.keep[e]||0))]).filter(x=>x[2]>0).sort((a,b)=>b[2]-a[2]);L.push(...hr);
  for(const k in BLOOM.keepKit){const n=Math.max(0,(hv[k]||0)-BLOOM.keepKit[k]);if(n>0)L.push([hv,k,n])}return L}
function bloomPay(R,M){const L=bloomPools(R);let have=0;for(const[,k,n]of L)have+=n*(RAWS.includes(k)?1:bloomMass({[k]:1}));if(have<M)return null;
  const got={};let left=M;for(const[st,k,n]of L){if(left<=0)break;const per=RAWS.includes(k)?1:bloomMass({[k]:1}),q=Math.min(n,Math.ceil(left/per));inv.take(st,k,q);inv.add(got,k,q);left-=q*per}return got}
// a Bloom Node needs no crew
{const o=devCap;devCap=function(R){if(R&&R.owner==='brood'&&R.kind==='depot')return 99;return o.apply(this,arguments)}}
function bloomGrowTick(){if(NET.cl||!S||S.training)return;const A=S.ai.brood=S.ai.brood||{};if(A.grow===undefined)A.grow=S.T+rnd(...BLOOM.every);if(S.T<A.grow)return;A.grow=S.T+rnd(...BLOOM.every);
  const opts=[];for(const R of bloomNodes()){const d=devOf(R),fr=bloomFront(R)?BLOOM.front:1;for(const k in BLOOM.max)if((d[k]||0)<BLOOM.max[k]&&devNext(R,k))opts.push([[R,k],fr*(k==='armor'?1.1:1)])}
  if(!opts.length)return;const[R,k]=wpickArr(opts),cost=bloomPay(R,bloomMass(devNext(R,k)));if(!cost)return;
  inv.addAll(R.fort,cost);devOf(R)[k]++;if(R.wk&&R.wk[k]!==undefined)R.wk[k]+=WK_HP[k];applyDev(R);
  if(covered(R.sid)||W&&W.sid===R.sid)feed(`⚠ ${R.name} in ${DEF[R.sid].name} has grown ${k==='def'?'more spore batteries':'a thicker carapace'} (level ${depotLevel(R)}).`,'warn')}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{bloomGrowTick()}catch(e){console.error(e)}return r}}
CAP_BROOD_OWN=true;
// the Brood grows its capitals itself (node's store, then the hive's spare, digesting plate and conduit as needed): a Leviathan
// while it has none (from minute BAL.brLevT), Prowlers up to its cap
function bloomCapTick(){if(NET.cl||!S||S.training)return;const T=S.T,f='brood';if(T<BAL.brLevT)return;const A=S.ai.brood=S.ai.brood||{};if(T<(A.capT||0))return;A.capT=T+rnd(40,70);
  const busy=t=>S.events.some(e=>e.type===t&&e.att===f&&e.stage!=='done');const L=bloomNodes();if(!L.length)return;
  let type=null,M=0;if(!busy('frigbuild')&&facCar(f).length<1){type='frigbuild';M=bloomMass(withSeal(CARRIER_COST,f,CAP_SEAL.carrier))}else if(!busy('escbuild')&&facEsc(f).length<(ESC_CAP[f]||0)){type='escbuild';M=bloomMass(escCost(f))}if(!type)return;
  const fr=L.filter(bloomFront),P=(fr.length?fr:L).slice().sort((a,b)=>invMass(dStore(b))-invMass(dStore(a)));for(const R of P){const kit=bloomPay(R,M);if(!kit)continue;
    S.events.push({id:S.nextId++,type,t0:T,yard:f,att:f,sector:R.sid,force:kit,until:T+(type==='escbuild'?ESCORT_TIME:FRIGATE_TIME),stage:'building',bloom:1});
    if(covered(R.sid))feed(`⚠ ${R.name} in ${DEF[R.sid].name} is swelling: the Brood is growing a ${type==='escbuild'?'Prowler':'Leviathan'} there.`,'warn');return}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{bloomCapTick()}catch(e){console.error(e)}return r}}
