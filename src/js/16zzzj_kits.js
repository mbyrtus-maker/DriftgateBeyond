//@src 16zzzj_kits.js
// ============================================================ Beyond: Lair, Depot and Station kits (user, 8 Nov 2026)
// The user: the bases' recipes "should still be needed to create the kits, but they should be purchaseable on the market and
// be able to be slotted into Cargo slots. They should require a certain tonnage cargo space (large)"; "Constructor is not a
// player ship. So they should all only fit in the heavy hauler; it's end game stuff"; carried in the hold; any ship that can
// carry one deploys it; "They are freely stocked at all stations."
//   Items: Lair Kit (1 Depot Frame, 6 Alloy Plate), Depot Kit (2 Depot Frames), Station Kit (1 Capital Keel, 2 Depot
//     Frames, 1 Compact Seal): 150, 180 and 220 t in the hold, and only a Heavy Hauler's hold takes one (bought by another
//     hull, it goes to your hangar). Fabricated at a dock from the recipe like any component.
//   Stocked: every power's and freeport's market has one of each while a pilot is docked there, assembled from that market's
//     own store (from the recipe's components, or what they are made of); when no pilot is docked, unsold kits are broken
//     back into exactly what they were made from. The ledger stays exact.
//   Deploying: a kit in the hold (or the base's store, for an upgrade) stands in for the loose materials: Build a Lair, Build a
//     Depot here (any hull, no Constructor), Upgrade a Lair to a Depot, Upgrade a Depot to a Station. It is unpacked into its
//     components at that moment and used as they would be.
ITEMS.kit_lair={name:'Lair Kit',recipe:{frame:1,plate:6},col:'#c9a86a',kit:1};
ITEMS.kit_depot={name:'Depot Kit',recipe:{frame:2},col:'#a8c0e0',kit:1};
ITEMS.kit_station={name:'Station Kit',recipe:{keel:1,frame:2,seal:1},col:'#e0c070',kit:1};
const KIT_IDS=['kit_lair','kit_depot','kit_station'],KIT_T={kit_lair:150,kit_depot:180,kit_station:220},KIT_HULL='bulker';
for(const k of KIT_IDS){ITEM_ORDER.push(k);CRAFTABLE.push(k)}
{const o=mass;mass=function(id){return KIT_T[id]||o.apply(this,arguments)}}
{const o=stockTarget;stockTarget=function(id){return KIT_T[id]?1:o.apply(this,arguments)}}
function isKit(k){return!!KIT_T[k]}
// a cost met by loose materials, or by the kit that stands in for them
function kitOr(cost,srcs,kid){return haveIn(cost,srcs)||countIn(kid,srcs)>0}
// unpack one kit (from the first source holding one) into its components, in that same source
function kitUnpack(kid,srcs){for(const s of srcs)if(s&&(s[kid]||0)>0){inv.take(s,kid,1);inv.addAll(s,ITEMS[kid].recipe);return true}return false}
// ---- the market: one of each kit on the shelf while a pilot is docked
function kitKey(R){const s=storeOf(R);return S.econ.stock[R.owner]&&s===S.econ.stock[R.owner]?'w:'+R.owner:'s:'+R.sid}
function kitMkOf(key){if(key.startsWith('w:'))return S.econ.stock[key.slice(2)]||null;const R=S.stations[key.slice(2)];return R?storeOf(R):null}
// what one kit takes from a store: the recipe's components where it has them, else what they are made of (down to ore)
function kitPlan(mk,k){const left={...mk},took={};
  const need=(id,n)=>{const h=Math.min(left[id]||0,n);if(h>0){left[id]-=h;took[id]=(took[id]||0)+h;n-=h}if(n<=0)return true;if(RAWS.includes(id)||!ITEMS[id]||!ITEMS[id].recipe)return false;const r=ITEMS[id].recipe;for(const x in r)if(!need(x,r[x]*n))return false;return true};
  const r=ITEMS[k].recipe;for(const x in r)if(!need(x,r[x]))return null;return took}
function kitTick(){if(NET.cl||!S||!S.econ||S.training||S.unb)return;S.kitShelf=S.kitShelf||{};const want={},L=mkStations();
  for(const P of allPilots()){if(!P||P.docked!=='station')continue;const R=S.stations[P.sector];if(R&&L.includes(R))want[kitKey(R)]=R}
  for(const key in want){const mk=kitMkOf(key);if(!mk)continue;const rec=S.kitShelf[key]=S.kitShelf[key]||[];
    for(const k of KIT_IDS){const have=mk[k]||0;let mine=rec.filter(x=>x.k===k);while(mine.length>have){rec.splice(rec.indexOf(mine[0]),1);mine=mine.slice(1)}
      if(have<1){const took=kitPlan(mk,k);if(took){takeFrom(took,[mk]);inv.add(mk,k,1);rec.push({k,took})}}}}
  for(const key of Object.keys(S.kitShelf)){if(want[key])continue;const mk=kitMkOf(key);
    if(mk)for(const x of S.kitShelf[key])if((mk[x.k]||0)>0){inv.take(mk,x.k,1);inv.addAll(mk,x.took)}
    delete S.kitShelf[key]}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{kitTick()}catch(e){console.error(e)}return r}}
// docking puts them on the shelf at once (the host; a guest's arrive with the next tick)
{const o=finishDock;finishDock=function(){const r=o.apply(this,arguments);try{kitTick()}catch(e){console.error(e)}return r}}
// ---- only a Heavy Hauler's hold takes a kit
let KIT_NOHOLD=false;
{const o=holdFree;holdFree=function(){return KIT_NOHOLD?0:o.apply(this,arguments)}}
{const o=dockAction;dockAction=function(act,arg){const k=typeof arg==='string'?arg.split(':')[0]:'';
  if(isKit(k)&&!NET.cl&&S.player.cls!==KIT_HULL){
    if(act==='buy'){KIT_NOHOLD=true;try{o.apply(this,arguments)}finally{KIT_NOHOLD=false}if(dockErr&&dockErr.startsWith('✓'))dockErr+=` A ${ITEMS[k].name} rides only in a Heavy Hauler's hold.`;return}
    if(act==='mv'&&arg.split(':')[1]!=='in'){dockErr=`A ${ITEMS[k].name} (${mass(k)} t) rides only in a Heavy Hauler's hold.`;return}}
  return o.apply(this,arguments)}}
// ---- deploying: the kit stands in for the loose materials
{const o=lairSpot;lairSpot=function(P){const r=o.apply(this,arguments);if(P&&r&&r.a&&r.why&&r.why.startsWith('You need')&&(P.cargo.kit_lair||0)>0)return{a:r.a};return r}}
{const o=lairMake;lairMake=function(P){if(P&&!haveIn(LAIR_B.cost,[P.cargo])&&!P.lairKit)kitUnpack('kit_lair',[P.cargo]);return o.apply(this,arguments)}}
{const o=depFresh;depFresh=function(P){if(P&&W&&W.player&&depCan(W.sid)&&!haveIn(DEP.cost,[P.cargo]))kitUnpack('kit_depot',[P.cargo]);return o.apply(this,arguments)}}
{const o=depFromLair;depFromLair=function(P,L){if(P&&L&&depCan(L.sid)&&!haveIn(DEP.cost,[P.cargo,L.stash]))kitUnpack('kit_depot',[P.cargo,L.stash]);return o.apply(this,arguments)}}
{const o=staUp;staUp=function(P,R){if(P&&R&&R.owner==='player'&&!R.pst&&(R.pid||'me')===pkeyOf(P)&&!haveIn(STA.cost,[P.cargo,R.stock]))kitUnpack('kit_station',[P.cargo,R.stock]);return o.apply(this,arguments)}}
