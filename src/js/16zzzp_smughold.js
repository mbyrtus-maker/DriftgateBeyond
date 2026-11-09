//@src 16zzzp_smughold.js
// ============================================================ Beyond: the Smuggler's hold, Unbound gear at Scrapheart (user, 9 Nov 2026)
// "Is there a cargo hold part that makes your cargo size smaller but harder to scan?" — "Add it at Scrapheart."
//   A cargo hold system (the Loadout's cargo system, in place of the standard or a maker's hold): −20% hold, and a customs scan
//   that finds contraband in your hold comes out clear half the time (on top of a hidden cargo container's own chance).
//   Made at Scrapheart from the Unbound's stores (a standard hold's makings) every SMH.make seconds while fewer than SMH.shelf are on its
//   market; SMH.price cr (SMH.sell back). Installed, it is recorded as the cargo system 'smug' (P.sysm.cargo), like a maker's.
// The ledger stays exact: it is built from the Unbound's stores and moves like any part.
// its recipe is the standard cargo hold's (the ledger counts a fitted system by its slot and grade)
const SMH={recipe:{...SLOT.cargo.base},make:900,shelf:2,price:3500,sell:1750,cargo:-.2,clear:.5};
ITEMS.sy_smug_cargo={name:"Smuggler's hold",recipe:{...SMH.recipe},sys:'cargo',grade:1,col:'#b98fd8',tr:{cargo:SMH.cargo},trTxt:`Unbound make: a cargo hold · ${Math.round(SMH.cargo*100)}% hold · a customs scan that finds contraband comes out clear ${Math.round(SMH.clear*100)}% of the time.`};
ITEM_ORDER.push('sy_smug_cargo');
SYS_TR.smug={cargo:{cargo:SMH.cargo}};
function smhOn(P){return!!(P&&P.sysm&&P.sysm.cargo==='smug')}
// installed through the Loadout: the system slot remembers it (and gives it back when swapped out)
{const o=rdSysFit;rdSysFit=function(arg){const[sl,id]=String(arg).split(':');const r=o.apply(this,arguments);try{if(id==='sy_smug_cargo'&&String(r).startsWith('✓')){const P=S.player;(P.sysm=P.sysm||{}).cargo='smug';if(W&&W.player)refreshPlayerStats()}}catch(e){console.error(e)}return r}}
// customs: half the time the hold keeps its secret
{const o=scanResolve;scanResolve=function(P,f,key){if(smhOn(P)&&contraFor(P,f).length&&Math.random()<SMH.clear){scanSay(key,`✓ ${FACTIONS[f].short} customs: scan clear (your smuggler's hold kept its secret).`);return}return o.apply(this,arguments)}}
// made at Scrapheart
function smhTick(){if(NET.cl||!S||S.training)return;const R=S.stations&&S.stations.wr;if(!R||R.owner!=='pirate'||(typeof havenDown==='function'&&havenDown())||S.T<(S.smhT||0))return;S.smhT=S.T+SMH.make;
  const st=mkStock(R),src=S.econ.stock.pirate;if((st.sy_smug_cargo||0)<SMH.shelf&&src&&haveIn(SMH.recipe,[src])){takeFrom(SMH.recipe,[src]);inv.add(st,'sy_smug_cargo',1)}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{smhTick()}catch(e){console.error(e)}return r}}
{const o=mBuy;mBuy=function(c,id){if(id==='sy_smug_cargo')return SMH.price;return o.apply(this,arguments)}}
{const o=mSell;mSell=function(c,id){if(id==='sy_smug_cargo')return SMH.sell;return o.apply(this,arguments)}}
