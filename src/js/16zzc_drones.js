//@src 16zzc_drones.js
// ============================================================ the Drone controller; guard drones as ammunition (Beyond, 3 Nov 2026)
// The user's asks and choices:
//  - A utility part, the Drone controller (pt_dronec), gives a pilot's ship its guard drones: without one fitted the drones
//    stay in the bay. It fits the hulls with a drone bay only (the miners and haulers); the hull sets how many drones it
//    carries, and each grade above 1 makes the drones tougher (+25% hull) and harder-hitting (+15% damage). Every miner and
//    hauler has a slot for it (one more utility slot) and comes with one fitted. Two makers build their own: Coldwater
//    Prospecting (+15% drone damage) and Teal & Corvane Yards (+20% drone hull); a plain one is built in a workshop.
//  - Guard drones are ammunition: lost drones are gone, and the bay is refilled at Rearm (automatically when you dock) like
//    missiles and charges: your own Guard Drones from the hold or vault first, then drones the station builds from its own
//    stores, paid in credits at the drone's value to the station's treasury (free at your own base). Drones in a hold stay
//    ordinary goods; the station's materials become the drones, so the ledger stays exact.
//  - Pilots from before this change: a miner or hauler without the new slot gets it, and (once) a standard controller
//    fitted in it, so their drones keep flying.
const DRN={hullG:.25,dmgG:.15};
function drnHull(cls){return((CLASSES[cls]&&CLASSES[cls].drones)||0)>0}
for(const k in HULL_SLOTS)if(drnHull(k)&&!HULL_SLOTS[k].u.includes('dronec'))HULL_SLOTS[k].u.push('dronec');
function drnCtl(P){if(!P||!loadOn())return{on:true,g:1,dh:0,dd:0};const F=fitOf(P);let best=null;
  (F.u||[]).forEach((k,i)=>{if(k!=='dronec')return;const g=(F.ug&&F.ug[i])||1,it=F.ui&&F.ui[i],tr=(it&&ITEMS[it]&&ITEMS[it].tr)||{};if(!best||g>best.g)best={on:true,g,dh:tr.dh||0,dd:tr.dd||0}});
  return best||{on:false,g:0,dh:0,dd:0}}
function drnCap(P){return drnCtl(P).on?((CLASSES[P.cls]&&CLASSES[P.cls].drones)||0):0}
function drnPrice(){return Math.max(1,Math.round(baseValue('drone')))}
// fitting: drone-bay hulls only
{const o=fitDo;fitDo=function(c,P,arg){const[g,i0,k]=String(arg).split(':'),I=k&&ITEMS[k];if(g==='u'&&(k==='dronec'||(I&&I.part==='dronec'))&&!drnHull(P.cls))return'A Drone controller fits miners and haulers only (ships with a drone bay).';return o.apply(this,arguments)}}
// new fits are marked; an older miner's or hauler's fit gets the slot and, once, a standard controller
{const o=fitNew;fitNew=function(){const F=o.apply(this,arguments);F.dcg=1;return F}}
{const o=fitOf;fitOf=function(P){const F=o.apply(this,arguments);try{if(P&&P.cls&&drnHull(P.cls)&&Array.isArray(F.u)){const D=slotsOf(P.cls,designOf(P.faction,P.cls)?P.faction:null);
    while(F.u.length<D.u.length){F.u.push('');(F.ug=F.ug||[]).push(1);(F.ui=F.ui||[]).push(null)}
    if(!F.dcg&&!NET.cl&&S&&S.ledger0){F.dcg=1;if(!F.u.includes('dronec')){const i=F.u.lastIndexOf('');if(i>=0)devLedger(()=>{F.u[i]='dronec';F.ug[i]=1;F.ui[i]=null})}}}}catch(e){}return F}}
// launching: no controller, no drones; a controller's grade and maker make them tougher
function drnBuff(P,L){const C=drnCtl(P);if(!C.on)return;const kh=(1+DRN.hullG*(C.g-1))*(1+C.dh),kd=(1+DRN.dmgG*(C.g-1))*(1+C.dd);if(kh===1&&kd===1)return;
  for(const d of L||[]){if(!d||d._dbuf)continue;d._dbuf=1;d.st={...d.st,hull:d.st.hull*kh,dmg:d.st.dmg*kd};d.hull=d.st.hull}}
{const o=launchPlayerDrones;launchPlayerDrones=function(){const P=S&&S.player;if(P&&loadOn()&&!drnCtl(P).on)return;const r=o.apply(this,arguments);try{drnBuff(P,W&&W.player&&W.player.drones)}catch(e){}return r}}
{const o=spawnRP;spawnRP=function(pid){const P=S.pilots&&S.pilots[pid];let kept=0;if(P&&loadOn()&&!drnCtl(P).on){P.bay=P.bay||{};kept=P.bay.drone||0;P.bay.drone=0}
  let r;try{r=o.apply(this,arguments)}finally{if(kept&&P)P.bay.drone=(P.bay.drone||0)+kept}
  try{const e=MP.rp[pid];if(e&&P){const L=[];for(const w of Object.values(WORLDS))for(const d of w.ents)if(d.role==='drone'&&d.mom===e)L.push(d);drnBuff(P,L)}}catch(e){}return r}}
// ---- Rearm: the drone bay refills like the magazines
function drnNeed(P){P.bay=P.bay||{};return Math.max(0,drnCap(P)-(P.bay.drone||0))}
let drnInQ=true;
{const o=rearmQuote;rearmQuote=function(P){const q=o.apply(this,arguments);try{if(drnInQ&&loadOn()){const n=drnNeed(P);q.drn=n;q.cr.drn=n*drnPrice();q.tot+=q.cr.drn;q.n+=n}}catch(e){}return q}}
function drnRefill(c,P){const need=drnNeed(P);if(!need)return{n:0,paid:0,short:0};const st=(c&&c.storage)||P.vault;let own=0;
  for(const h of[P.cargo,st]){if(own>=need)break;own+=inv.take(h,'drone',need-own)}
  const R=S.stations[P.sector],mine=R&&R.owner==='player';let mk=null;try{mk=R&&P.docked==='station'?(mine?R.stock:mkStock(R)):null}catch(e){}
  const pr=mine?0:drnPrice(),rc=ITEMS.drone.recipe;let b=0,paid=0;
  while(own+b<need&&mk&&haveIn(rc,[mk])&&P.credits-paid>=pr){takeFrom(rc,[mk]);b++;paid+=pr}
  if(paid)transfer('player',(c&&c.wallet)||(R&&R.owner)||'neutral',paid);if(own+b)inv.add(P.bay,'drone',own+b);return{n:own+b,own,paid,short:need-own-b}}
{const o=rearmDo;rearmDo=function(c,P){let D={n:0,paid:0,short:0};try{if(loadOn())D=drnRefill(c,P)}catch(e){console.error(e)}
  drnInQ=false;let m;try{m=o.apply(this,arguments)}finally{drnInQ=true}
  if(!D.n&&!D.short)return m;const cap=drnCap(P),dm=D.n?`${D.n} guard drone${D.n>1?'s':''}${D.paid?` (${fmt(D.paid)} cr)`:''} · bay ${P.bay.drone||0}/${cap}`:'',sm=D.short?` The station couldn't supply ${D.short} more drone${D.short>1?'s':''}.`:'';
  if(/^Nothing to rearm|^Not enough credits/.test(m))return D.n?`✓ Rearmed: ${dm}.${sm}`:(m+sm);return m.replace(/\.$/,'')+(dm?` · ${dm}`:'')+'.'+sm}}
// the Ship tab's drone bay note
{const o=renderDock;renderDock=function(){const r=o.apply(this,arguments);try{if(loadOn()&&S.player&&drnHull(S.player.cls)){const el=$('dBody');if(el)for(const h of el.querySelectorAll('.h3'))if(/^Drone bay/.test(h.textContent)){const n=h.nextElementSibling;if(n&&n.classList.contains('note')){const C=drnCtl(S.player);
  n.textContent=C.on?`Guard drones launch with you and defend your ship (Drone controller, grade ${C.g}). They're ammunition: lost drones are gone, and the bay refills at Rearm when you dock, from your own drones first, then built by the station for ${fmt(drnPrice())} cr each.`:'No Drone controller fitted: your drones stay in the bay. Fit one in a utility slot on the Loadout.'}}}}catch(e){}return r}}
