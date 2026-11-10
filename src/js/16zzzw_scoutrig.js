//@src 16zzzw_scoutrig.js
// ============================================================ Beyond: every scout comes with a beacon rig (user, 9 Nov 2026)
// "Scout should come with a beacon rig and it should not be used up when claiming a beacon." (The rig is never used up: see
// 16zi_small.js.) A pilot docked at a station in a scout hull (Scout, Pathfinder, the Unbound's skiff) with no beacon rig
// fitted gets one fitted, once for each hull it takes up: from its own vault if it keeps one there, else from the station's
// shelf with the hull (every station keeps standard parts, the beacon rig among them). Taken out by hand afterwards, it
// stays out until the pilot changes hull. The ledger stays exact: the rig moves from a store into the fit.
function scRigSlot(P){const F=fitOf(P),D=slotsOf(P.cls,P.faction);let i=D.u.findIndex((k,j)=>k==='bdev'&&!F.u[j]);if(i<0)i=F.u.findIndex(k=>!k);return i}
function scRigGive(P){if(!isScoutCls(P.cls)||P.docked!=='station'||smxN(P,'bdev')>0){if(isScoutCls(P.cls)&&smxN(P,'bdev')>0)P.rigFor=P.cls;return}if(P.rigFor===P.cls)return;
  const i=scRigSlot(P);if(i<0){P.rigFor=P.cls;return}const R=S.stations[P.sector];let st=null;try{st=R&&mkStock(R)}catch(e){}if(!st&&R&&R.owner==='pirate')st=S.econ.stock.pirate;
  const src=[P.vault,st].find(x=>x&&(x.pt_bdev||0)>0);if(!src)return;inv.take(src,'pt_bdev',1);const F=fitOf(P);F.u[i]='bdev';F.ug[i]=1;if(F.ui)F.ui[i]=null;P.rigFor=P.cls;
  keyFeed(pkeyOf(P),`Beacon rig fitted to your ${CLASSES[P.cls].name}${src===P.vault?' from your vault':', with the hull'}: it flips beacons for the power you do intel work for, and is never used up.`,'good')}
{const o=smxRigTick;smxRigTick=function(){const r=o.apply(this,arguments);try{if(loadOn()&&!S.unb)for(const P of allPilots())if(P)scRigGive(P)}catch(e){console.error(e)}return r}}
// straight away when the hull is taken (not only on the next tick)
{const o=dockAction;dockAction=function(act,arg){const r=o.apply(this,arguments);try{if((act==='hull'||act==='hullsw')&&loadOn())scRigGive(S.player)}catch(e){console.error(e)}return r}}
// ---- (user, 9 Nov 2026: "my hauler launched without drones, that shouldn't happen") every miner and hauler comes with a
// Drone controller the same way (a new hull carried across only the parts the old one had, so a hauler bought from a fighter
// had an empty controller slot and no drones), and drones are topped up before you launch: the bay refills at the automatic
// rearm when you dock, which ran before a hull bought or a controller fitted at the same dock.
function scKitGive(P,k){if(!P||P.docked!=='station'||!loadOn())return false;const ok=k==='dronec'?drnHull(P.cls):isScoutCls(P.cls);if(!ok)return false;P.kitFor=P.kitFor||{};const key=P.cls+':'+k,F=fitOf(P);
  if((F.u||[]).includes(k)){P.kitFor[key]=1;return false}if(P.kitFor[key])return false;const D=slotsOf(P.cls,P.faction);let i=D.u.findIndex((x,j)=>x===k&&!F.u[j]);if(i<0)i=F.u.findIndex(x=>!x);if(i<0){P.kitFor[key]=1;return false}
  const R=S.stations[P.sector];let st=null;try{st=R&&mkStock(R)}catch(e){}if(!st&&R&&R.owner==='pirate')st=S.econ.stock.pirate;const it=PART[k],src=[P.vault,st].find(x=>x&&(x[it]||0)>0);if(!src)return false;
  inv.take(src,it,1);F.u[i]=k;F.ug[i]=1;if(F.ui)F.ui[i]=null;P.kitFor[key]=1;keyFeed(pkeyOf(P),`${UTIL[k].name} fitted to your ${CLASSES[P.cls].name}${src===P.vault?' from your vault':', with the hull'}.`,'good');return true}
function scDrones(P){try{if(P&&P.docked==='station'&&loadOn()&&drnNeed(P)>0){const k=pkeyOf(P);runAs(isMe(k)?null:k,()=>{const D=drnRefill(dockCtx(),S.player);if(D.n)keyFeed(k,`Drone bay topped up: ${D.n} drone${D.n>1?'s':''}${D.paid?` (${fmt(D.paid)} cr)`:''}.`,'good');else if(D.short)keyFeed(k,`Drone bay short ${D.short}: the station can't build them (or you can't pay).`,'warn')})}}catch(e){console.error(e)}}
{const o=smxRigTick;smxRigTick=function(){const r=o.apply(this,arguments);try{if(loadOn()&&!S.unb)for(const P of allPilots())if(P&&scKitGive(P,'dronec'))scDrones(P)}catch(e){console.error(e)}return r}}
{const o=dockAction;dockAction=function(act,arg){const r=o.apply(this,arguments);try{if((act==='hull'||act==='hullsw')&&loadOn()){scKitGive(S.player,'dronec');scDrones(S.player)}}catch(e){console.error(e)}return r}}
// launching: a drone bay that isn't full is topped up first (host and single player; a guest's launch runs here on the host)
{const o=undock;undock=function(){try{const P=S.player;if(P&&P.docked==='station'&&loadOn()&&drnNeed(P)>0)scDrones(P)}catch(e){console.error(e)}return o.apply(this,arguments)}}
{const o=hUndock;hUndock=function(pid){try{const P=S.pilots&&S.pilots[pid];if(P&&P.docked==='station'&&loadOn()&&drnNeed(P)>0)scDrones(P)}catch(e){console.error(e)}return o.apply(this,arguments)}}
