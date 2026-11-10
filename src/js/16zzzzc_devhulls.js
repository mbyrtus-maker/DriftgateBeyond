//@src 16zzzzc_devhulls.js
// ============================================================ Beyond: fly any faction's hulls from the dev menu (user, 9 Nov 2026)
// "On the cheat menu you should be able to select a faction and then a hull, so you can fly all the ships in the game as a
// developer." The dev menu's ship row now has a faction picker (Halcyon, Varkesh, Ostrova, the Unbound) and the hull list
// for it: every hull a yard builds plus the Wraith in that power's design, and the power's own signature hull (the Gannet,
// the Bombard, the Vesper); for the Unbound their Raider, Corsair, Plunderer and Skiff and the Wraith. Flying one sets your
// ship's faction (its look, its design's stats, its hull names) to the one picked. A dev tool: no cost, the old hull's
// parts and cargo that won't fit go to the vault as before (devHull).
const DEV_SIG={halcyon:'gannet',varkesh:'bombard',ostrova:'vesper'},DEV_UNB=['raider','corsair','plunderer','uskiff','wraith'];
function devHullsOf(f){if(f==='pirate')return DEV_UNB.filter(k=>CLASSES[k]);const L=Object.keys(HULL_COST).filter(k=>CLASSES[k]);if(DEV_SIG[f]&&CLASSES[DEV_SIG[f]])L.push(DEV_SIG[f]);return L}
function devHullName(f,k){const F=FAC(f)||{};return(F.hulls||{})[k]||CLASSES[k].name}
devShips=function(){const fs=$('devFac'),sel=$('devShip');if(!sel||!S)return;const P=S.player,cur=P.cls;
  if(fs){const v=fs.value||(FACTIONS[P.faction]||P.faction==='pirate'?P.faction:'halcyon');fs.innerHTML=[...FAC_IDS,'pirate'].map(f=>`<option value="${f}"${f===v?' selected':''}>${esc(f==='pirate'?'The Unbound':FACTIONS[f].short)}</option>`).join('');if(!fs._wired){fs._wired=1;fs.addEventListener('change',()=>devShips())}}
  const f=fs?fs.value:'halcyon';sel.innerHTML=devHullsOf(f).sort((a,b)=>CLASSES[a].name.localeCompare(CLASSES[b].name)).map(k=>`<option value="${k}"${k===cur&&f===P.faction?' selected':''}>${esc(devHullName(f,k))} · ${esc(CLASSES[k].name)}${k===cur&&f===P.faction?' (current)':''}</option>`).join('')};
function devHullAs(f,cls){const P=S.player;if(!CLASSES[cls])return'Unknown hull.';if(!(FACTIONS[f]||f==='pirate'))f=P.faction;const same=P.cls===cls&&P.faction===f;if(same)return'You already fly that ship.';
  const tmp=!(cls in HULL_COST);if(tmp)HULL_COST[cls]={};let r='';const was=P.faction;try{P.faction=f;if(P.cls===cls){refreshPlayerStats&&W&&W.player&&refreshPlayerStats();r=`You now fly a ${devHullName(f,cls)} (${CLASSES[cls].name}).`}else r=devHull(cls)}finally{if(tmp)delete HULL_COST[cls]}
  try{if(W&&W.player&&P===S.player){W.player.fac=P.faction;W.player.cls=P.cls;refreshPlayerStats();W.player.hull=W.player.st.hull;W.player.shield=W.player.st.sCap}}catch(e){}
  return String(r).replace(/You now fly a .*? \(/,`You now fly a ${devHullName(f,cls)}${f!==was?` in ${f==='pirate'?'the Unbound\'s':FAC(f).short+'\'s'} design`:''} (`)}
