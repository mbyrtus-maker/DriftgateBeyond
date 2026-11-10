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
// ---- (user, 9 Nov 2026) "add to the developer menu a 'jump to system' choice so I can instantly teleport anywhere on the map":
// pick any system and jump there at once (undocking first), arriving near its station if it has one, else at a gate. A guest
// teleports on its own screen and tells the host where it now is.
function devSysList(){const sel=$('devSys');if(!sel||!S)return;const cur=sel.value||S.player.sector;sel.innerHTML=SECTOR_DEFS.slice().sort((a,b)=>a.name.localeCompare(b.name)).map(d=>{const R=S.stations[d.id],o=R?` · ${R.owner==='player'?'yours':R.owner==='neutral'?'freeport':R.owner==='pirate'?'Unbound':(FAC(R.owner)||{}).short||R.owner}`:'';return`<option value="${d.id}"${d.id===cur?' selected':''}>${esc(d.name)}${o}${d.id===S.player.sector?' (here)':''}</option>`}).join('')}
{const o=devShips;devShips=function(){const r=o.apply(this,arguments);try{devSysList()}catch(e){}return r}}
function devTeleport(to){const P=S.player;if(!DEF[to])return'Unknown system.';if(to===P.sector&&!P.docked)return'You are already there.';
  if(P.docked){try{$('dock').hidden=true;$('company').hidden=true}catch(e){}P.docked=null}if(W&&W.bridge)return'Leave the bridge first.';
  exitSector();P.sector=to;const g=(GATES[to]||[])[0]||{x:3000,y:0,z:0},l=hyp(g.x,g.y,g.z)||1;P.x=g.x-g.x/l*300;P.y=g.y-g.y/l*300;P.z=g.z-g.z/l*300;P.vx=P.vy=P.vz=0;enterSector(to);
  {const E=W.stationEnt,p=W.player;if(E&&p){const r=(E.r||130)+380;p.x=E.x+r*.7;p.y=E.y+60;p.z=E.z+r*.7;p.vx=p.vy=p.vz=0;faceInstant(p,E.x-p.x,E.y-p.y,E.z-p.z)}}if(NET.cl){const q=W.player;netSend({t:'dev',k:'tp',to,x:q.x,y:q.y,z:q.z})}try{save()}catch(e){}return`Jumped to ${DEF[to].name}.`}
{const o=devDo;devDo=function(k){if(k==='tp'){const sel=$('devSys');const m=devTeleport(sel?sel.value:'');try{flash(m)}catch(e){}devSysList();return}return o.apply(this,arguments)}}
// the host moves a guest that teleported
{const o=hostRecv;hostRecv=function(L,m){try{if(m&&m.t==='dev'&&m.k==='tp'){const c=MP.cl[L.peer],pid=c&&c.pid,P=pid&&S.pilots[pid];if(P&&DEF[m.to]){despawnRP(pid);P.docked=null;P.sector=String(m.to);P.x=+m.x||0;P.y=+m.y||0;P.z=+m.z||0;delete MP.inp[pid];if(!WORLDS[P.sector])openWorld(P.sector);spawnRP(pid);netRoster()}return}}catch(e){console.error(e)}return o.apply(this,arguments)}}
