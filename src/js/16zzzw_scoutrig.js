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
