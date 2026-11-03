//@src 16u_piracy.js
// ============================================================ pirate gear for contractors (Beyond, after stage 14)
// The Unbound's tools, fitted to your own ship: a jammer in a weapon slot (key 4 toggles jam mode: your guns fire jam rounds
// and your missiles fly as shock harpoons; jammers never kill and do nothing to a shielded ship) and a cargo hook in a utility
// slot (hold E beside a ship jammed dark, within 150 m or 400 m on a harpoon tether, to hook its hold: 8 t a second, most
// valuable first). What you hook is tagged stolen from its owner, and taking it raises that power's heat. Owning the gear is
// no crime, but carrying it is: a customs scan that finds pirate gear on your ship (fitted or in the hold) raises that power's
// heat, more if you've jammed one of its ships in the last hour. Sold at Scrapheart Haven; never built at a workshop.
const PG2={heatLight:15,heatHeavy:30,jamMem:3600,hookHeat:.6};
WPN.jammer={name:'Jammer',desc:'Pirate gear. In jam mode (key 4) your guns fire jam rounds and missiles fly as shock harpoons. Never kills; useless against shields. Contraband to carry.'};
UTIL.hook={name:'Cargo hook',desc:'Pirate gear. Hold E beside a ship jammed dark to hook its hold. What you take is stolen. Contraband to carry.'};
PART.jammer='pt_jammer';PART.hook='pt_hook';PART_RC.jammer={wire:2,coil:1};PART_RC.hook={plate:2,wire:1};PART_COL.jammer='#b7c6ff';PART_COL.hook='#d8cd98';
for(const k of['jammer','hook']){ITEMS[PART[k]]={name:(WPN[k]||UTIL[k]).name,recipe:PART_RC[k],col:PART_COL[k],part:k,gear:1};ITEM_ORDER.push(PART[k])}
{const o=wpnOK;wpnOK=function(cls,k,i){if(k==='jammer')return!blHull(cls)&&!(isTorpHull(cls)&&i===0)&&!!CLASSES[cls];return o.apply(this,arguments)}}
// Scrapheart stocks the gear
{const o=partsSeed;partsSeed=function(){o.apply(this,arguments);const R=S.stations&&S.stations.wr;if(R&&R.owner==='pirate'){const st=mkStock(R);inv.add(st,'pt_jammer',3);inv.add(st,'pt_hook',3)}}}
function gearOn(P){if(!P||!loadOn())return 0;const F=fitOf(P);return F.w.filter(k=>k==='jammer').length+F.u.filter(k=>k==='hook').length+(P.cargo.pt_jammer||0)+(P.cargo.pt_hook||0)}
// ---- the cargo hook (local pilot; a guest's hook waits for the multiplayer pass)
function pgHookTarget(){const p=W&&W.player,P=S.player;if(!p||S.unb||!loadOn()||!fitHas(P,'hook')||P.docked)return null;const T=W.tgt&&W.tgt.kind==='ship'&&W.tgt.ref;if(!T||!T.alive||!jamDark(T)||T.role==='frigate')return null;
  const reach=T.teth&&T.teth.until>W.t&&T.teth.by===p?400:JAM.hookR;return d3(T,p)<reach+T.st.radius?T:null}
function pgHookTick(dt){const p=W.player,P=S.player,T=keys.KeyE?pgHookTarget():null;if(!T){p._hk=0;return}const cg=T.cargo;if(!cg||!Object.keys(cg).some(k=>cg[k]>0)){if(W.t-(W._hkMsg||0)>2){W._hkMsg=W.t;flash('Its hold is empty.')}return}
  p._hk=(p._hk||0)+JAM.hookRate*dt;let moved=0;while(p._hk>=1){const ks=Object.keys(cg).filter(k=>cg[k]>0&&mass(k)>0).sort((a,b)=>baseValue(b)/mass(b)-baseValue(a)/mass(a)),k=ks[0];if(!k)break;const m=mass(k);if(invMass(P.cargo)+m>p.st.cargo){if(W.t-(W._hkMsg||0)>2){W._hkMsg=W.t;flash('Hold full.')}break}if(p._hk<m)break;
    p._hk-=m;inv.take(cg,k,1);inv.add(P.cargo,k,1);if(FAC_IDS.includes(T.side)){stolAdd(P,k,T.side,1);smHeat(P,T.side,PG2.hookHeat*m,'hooking its cargo');standHit(P,T.side,m*2,'convoy')}moved+=m}
  if(moved&&W.t-(W._hkMsg||0)>1.5){W._hkMsg=W.t;flash(`☠ Hooking ${shipLabel(T)}'s hold: ${invMass(P.cargo)}/${p.st.cargo} t.`)}}
{const o=actPress;actPress=function(){if(!NET.cl&&pgHookTarget())return;return o.apply(this,arguments)}}
{const o=worldUpdate;worldUpdate=function(dt){const r=o.apply(this,arguments);try{if(W&&W===LW&&W.player&&!NET.cl&&!S.unb)pgHookTick(dt)}catch(err){console.error(err)}return r}}
// jamming a power's ship is remembered (for customs) and costs standing like any attack
{const o=jamHit;jamHit=function(e,b){const src=b&&b.src,P=src&&pilotOfEnt(src);if(P&&!S.unb&&FAC_IDS.includes(e.side)){P.jamT=P.jamT||{};P.jamT[e.side]=S.T}return o.apply(this,arguments)}}
// customs: pirate gear aboard raises the scanning power's heat (fitted gear can't be hidden; gear in the hold can)
{const o=scanResolve;scanResolve=function(P,f,key){const g=gearOn(P);o.apply(this,arguments);if(!g)return;const hot=P.jamT&&S.T-(P.jamT[f]||-1e9)<PG2.jamMem,inHold=(P.cargo.pt_jammer||0)+(P.cargo.pt_hook||0),fitted=g-inHold;
  if(!fitted&&inHold&&hideCap(P)>=inHold*mass('pt_hook'))return;smHeat(P,f,hot?PG2.heatHeavy:PG2.heatLight,'pirate gear found aboard');scanSay(key,`⚠ ${FACTIONS[f].short} customs logged pirate gear on your ship${hot?', and they know you jammed one of theirs':''}.`,true)}}
// the HUD gun readout says when jam mode is on
{const o=hudUpdate;hudUpdate=function(){const r=o.apply(this,arguments);try{if(loadOn()&&W&&W.player&&W.player.jamMode&&!S.unb){const el=$('hWpn');el.textContent='JAM';el.style.color='#b7c6ff'}}catch(err){}return r}}
