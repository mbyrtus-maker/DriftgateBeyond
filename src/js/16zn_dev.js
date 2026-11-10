//@src 16zn_dev.js
// ============================================================ the developer panel for Beyond (Ctrl+Alt+D, 3 Nov 2026)
// You aren't sworn to a faction, so the panel stops assuming one: every power (and the Unbound and the Brood) can be the
// enemy, friendly wings and capitals fly as yours (contractor capitals), and "Vault" reads Hangar. A Beyond section adds:
// standing (+25 / −25 with a chosen power or the Compact), Contractor Rating +1, heat cleared or raised, the kits for a Lair,
// a Depot and a Station into your hold, an AI crew at your depot, Rift Shards and contraband, the Dread Pirate spawned here,
// Scrapheart knocked out, and ten minutes of the galaxy run forward. Each one that makes goods moves the ledger baseline
// (devLedger), as the old tools do. Guests' requests run on the host.
const DVX={kits:{lair:{frame:1,plate:6},depot:{frame:2},station:{keel:1,frame:2,seal:1},bld:{frame:1,plate:20,coil:4}}};
(function(){const D=document.getElementById('dev');if(!D)return;
  const res=D.querySelector('[data-dev="res"]');if(res)res.textContent=S&&S.player&&S.player.docked?'Storage here: +10 of each resource':'Hangar: +10 of each resource';
  const gb=D.querySelector('[data-dev="gunboat"]');
  const sec=document.createElement('div');sec.innerHTML=`<div class="dv-sec">Beyond</div>
    <div class="dv-s"><label class="dv-l" for="devPow">Power</label><select id="devPow" aria-label="Power"></select><button type="button" class="btn" data-dev="bx:st+">Standing +25</button><button type="button" class="btn" data-dev="bx:st-">−25</button></div>
    <div class="dv-s wr"><button type="button" class="btn" data-dev="bx:rp">Rating +1</button><button type="button" class="btn" data-dev="bx:cool">Clear heat</button><button type="button" class="btn" data-dev="bx:hot">Heat +40</button></div>
    <div class="dv-s wr"><button type="button" class="btn" data-dev="bx:klair">Lair kit</button><button type="button" class="btn" data-dev="bx:kdepot">Depot kit</button><button type="button" class="btn" data-dev="bx:kst">Station kit</button><button type="button" class="btn" data-dev="bx:kbld">Building kit</button></div>
    <div class="dv-s wr"><button type="button" class="btn" data-dev="bx:crew">AI crew at your depot</button><button type="button" class="btn" data-dev="bx:rift">Rift Shards + contraband</button></div>
    <div class="dv-s wr"><button type="button" class="btn" data-dev="bx:dread">Dread Pirate here</button><button type="button" class="btn" data-dev="bx:haven">Knock out Scrapheart</button><button type="button" class="btn" data-dev="bx:time">+10 min of galaxy</button></div>`;
  const msg=D.querySelector('#devMsg');while(sec.firstChild)D.insertBefore(sec.firstChild,msg)})();
function devPowUI(){const s=$('devPow');if(!s||s.children.length)return;s.innerHTML=[...FAC_IDS.map(f=>[f,FACTIONS[f].short]),['neutral','Freeport Compact']].map(([k,n])=>`<option value="${k}">${esc(n)}</option>`).join('')}
// every power can be the enemy now
devEnemyUI=function(){const sel=$('devSide');if(!sel||!S)return;const cur=sel.value;sel.innerHTML=[...FAC_IDS.map(f=>[f,FACTIONS[f].name]),['pirate','The Unbound (pirates)'],['brood','The Brood']].map(([k,n])=>`<option value="${k}"${k===cur?' selected':''}>${esc(n)}</option>`).join('');
  const T=$('devTypes');if(T&&!T.children.length)T.innerHTML=DEV_TYPES.map(([k,n],i)=>`<label><input type="checkbox" value="${k}"${i<2?' checked':''}>${esc(n)}</label>`).join('')};
{const o=devToggle;devToggle=function(){const r=o.apply(this,arguments);try{devPowUI()}catch(e){}return r}}
// the friendly heavy bomber flies as yours, not a power's
{const o=devGunboat;devGunboat=function(){if(S.unb||S.player.sworn)return o.apply(this,arguments);const P=S.player,f0=P.faction;let r;const fT=factionTier;factionTier=function(){return Math.max(1,fT(f0))};try{P.faction='player';r=o.apply(this,arguments)}finally{P.faction=f0;factionTier=fT}
  try{for(const e of W.ents)if(e.role==='patrol'&&e.side==='player'&&e.cls==='gunboat'&&!e.fac)e.fac=f0}catch(e){}return r}}
function devBx(k,P,arg){P=P||S.player;const kit=K=>{const to=P.docked?(P.vault=P.vault||{}):P.cargo;devLedger(()=>inv.addAll(to,K));return`Added ${Object.keys(K).map(i=>`${K[i]} ${ITEMS[i].name}`).join(', ')} to your ${P.docked?'hangar':'hold'}.`};
  if(k==='st+'||k==='st-'){const f=arg||'halcyon';standAdd(f,k==='st+'?25:-25,'developer',P);return`Standing with ${f==='neutral'?'the Compact':FACTIONS[f].short} ${k==='st+'?'+25':'−25'}.`}
  if(k==='rp'){const r=ratingOf(P),need=RATING.need[Math.min(10,r+1)];P.rp=Math.max(P.rp||0,need||P.rp);return`Contractor Rating ${ratingOf(P)}.`}
  if(k==='cool'){P.heat={};P.ranF={};return'Heat cleared with every power.'}
  if(k==='hot'){for(const f of FAC_IDS)smHeat(P,f,40,'developer');return'Heat +40 with every power.'}
  if(k==='klair')return kit(DVX.kits.lair);if(k==='kdepot')return kit(DVX.kits.depot);if(k==='kst')return kit(DVX.kits.station);if(k==='kbld')return kit(DVX.kits.bld);
  if(k==='crew'){const R=myDepots(P)[0];if(!R)return'You have no depot.';R.crew=R.crew||[];if(R.crew.length>=crewCap(R))return'That depot\'s hangar is full.';R.crew.push({id:S.nextId++,name:pick(['Okafor','Lune','Grey','Mbeki','Ishida','Roan','Vey']),cls:'prospector',job:'mine',laid:false,hired:S.T});return`A crew joins ${R.name}.`}
  if(k==='rift'){const to=P.docked?(P.vault=P.vault||{}):P.cargo;devLedger(()=>{inv.add(to,'riftshard',3);inv.add(to,'relic',2);inv.add(to,'rift',4)});return`3 Rift Shards, 2 Ghost relics and 4 Riftstone in your ${P.docked?'hangar':'hold'}.`}
  if(k==='dread'){if(typeof dpOf!=='function'||!dpOf())return'No Dread Pirate in this galaxy.';if(!W||!W.player)return'Not in a system.';const D=dpOf();D.ship.alive=true;D.ship.rav=null;D.ship.sid=W.sid;D.ship.live=0;D.ship.move=S.T+999;dpSpawn(W);return`${dpName(D)} is here.`}
  if(k==='haven'){if(typeof havenKnock!=='function')return'';if(havenDown())return'Scrapheart is already dark.';havenKnock(null,null);return'Scrapheart Haven knocked out.'}
  if(k==='time'){for(let i=0;i<60;i++){S.T+=10;strategicTick();updateEvents()}return'Ten minutes of the galaxy ran forward.'}
  return''}
{const o=devDo;devDo=function(k){if(String(k).startsWith('bx:')){if(!running||!S)return;const kk=k.slice(3),arg=($('devPow')||{}).value;let msg;
    if(NET.cl){netSend({t:'devbx',k:kk,arg});msg='Asked the host…'}else msg=devBx(kk,S.player,arg);$('devMsg').textContent=msg||'';SFX.clunk();if(S.player.docked&&typeof renderDock==='function')renderDock();if(!NET.cl)save();return}
  return o.apply(this,arguments)}}
{const o=hostRecv;hostRecv=function(L,m){if(m&&m.t==='devbx'){const c=MP.cl[L.peer],P=c&&c.ready&&S.pilots[c.pid];if(!P)return;if($('dev').hidden){netMsg(c.pid,'flash','Developer tools are off: the host has to open the developer panel (Ctrl+Alt+D) first.');return}
    const r=runAs(c.pid,()=>devBx(String(m.k||''),P,String(m.arg||'')));sendPR(c,false,true);send(L,syncMsg(c));netMsg(c.pid,'flash',r||'');return}return o.apply(this,arguments)}}
{const o=devRes;devRes=function(){const r=o.apply(this,arguments);return S&&!S.unb&&typeof r==='string'?r.replace('the vault','your hangar'):r}}
