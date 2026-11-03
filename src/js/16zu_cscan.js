//@src 16zu_cscan.js
// ============================================================ the cargo scanner (Beyond, agreed 3 Nov 2026)
// A utility part (built into every Unbound hull at grade 1). Target a ship within range (1,200 m + 150 m a grade) and hold
// it there: at once a rough reading (the kinds of goods, about how many tonnes, about what they're worth); after the scan
// (4 s, half a second less a grade, at least 2 s) the exact manifest. Hidden cargo containers keep their share out. The
// scanned ship notices: pilots are warned; AI freighters, traders and miners notice half the time and run for the gate;
// finishing a scan of a power's ship in that power's own space adds a little heat with it. Readings stay with each ship
// while it's in the system. Local pilot only (guests in multiplayer don't hold other ships' cargo yet).
const CSC={r:1200,rG:150,t:4,tG:.5,tMin:2,notice:.5,heat:6};
UTIL.cscan={name:'Cargo scanner',desc:'Target a ship in range (1.2 km, +150 m a grade) and hold it: a rough reading at once, the exact manifest after the scan (4 s, faster at better grades). Built into every Unbound hull.'};
PART.cscan='pt_cscan';PART_RC.cscan={wire:1,coil:1};PART_COL.cscan='#f5e663';ITEMS.pt_cscan={name:UTIL.cscan.name,recipe:PART_RC.cscan,col:PART_COL.cscan,part:'cscan'};ITEM_ORDER.push('pt_cscan');CRAFTABLE.push('pt_cscan');
{const o=partsSeed;partsSeed=function(){o.apply(this,arguments);try{const R=S.stations&&S.stations[WRACK.sid];if(R)inv.add(mkStock(R),'pt_cscan',3)}catch(e){}}}
function cscG(P){if(!P)return 0;const g=loadOn()?fitUG(P,'cscan'):0;return Math.max(g,UNB_HULLS.includes(P.cls)?1:0)}
function cscR(g){return CSC.r+CSC.rG*(g-1)}
function cscT(g){return Math.max(CSC.tMin,CSC.t-CSC.tG*(g-1))}
// what a ship carries, as a scan sees it (a pilot's hidden container keeps its share, the contraband first)
function cscLoad(T){let C={};if(T.isPlayer)C=S.player.cargo;else if(T.rp&&S.pilots&&S.pilots[T.rp])C=S.pilots[T.rp].cargo;else C=hookSrc(T)||{};C={...C};
  const P=T.isPlayer?S.player:T.rp&&S.pilots?S.pilots[T.rp]:null;let cap=P&&typeof hideCap==='function'?hideCap(P):0;
  if(cap>0){const ks=Object.keys(C).sort((a,b)=>(giKind(b)==='con')-(giKind(a)==='con'));for(const k of ks){if(cap<=0)break;const n=Math.min(C[k],Math.floor(cap/mass(k)));if(n>0){C[k]-=n;cap-=n*mass(k)}}}
  for(const k in C)if(!(C[k]>0)||!ITEMS[k])delete C[k];return C}
const CSC_GN={ore:'ore',comp:'components',wpn:'weapons',util:'utility parts',msl:'payload',chg:'payload',rnd:'payload',con:'contraband'};
function cscRough(C){const m=invMass(C),v=invValue(C),kinds=[...new Set(Object.keys(C).map(k=>CSC_GN[giKind(k)]||'goods'))];if(!m)return'empty hold';
  return`${kinds.join(', ')} · ${m<10?'under 10':'about '+fmt(Math.round(m/10)*10)} t · about ${fmt(Math.max(100,Math.round(v/250)*250))} cr`}
function cscExact(C){const ks=Object.keys(C).sort((a,b)=>C[b]*mass(b)-C[a]*mass(a));if(!ks.length)return'Empty hold.';
  return ks.map(k=>`<span style="display:inline-flex;gap:4px;align-items:center;margin-right:8px">${gIcon(k,12)}${esc(ITEMS[k].name)} <b>${C[k]}</b></span>`).join('')+`<div class="ts" style="margin-top:2px">${fmt(invMass(C))} t · worth about ${fmt(Math.round(invValue(C)))} cr</div>`}
// the scan, run each HUD update for the local pilot
function cscTick(){if(!W||!W.player||S.training||NET.cl)return null;const P=S.player,g=cscG(P);if(!g||P.docked){W.csc=null;return null}
  const T=W.tgt&&W.tgt.kind==='ship'?W.tgt.ref:null;if(!T||!T.alive||T.isPlayer||T.role==='limpet'){return null}
  const R=T._csc||(T._csc={p:0,done:false,seen:false});const inR=d3(T,W.player)<=cscR(g)+(T.st&&T.st.radius||0);
  const now=W.t,dt=Math.min(.5,Math.max(0,now-(R.last||now)));R.last=now;
  if(inR&&!R.done){if(!R.seen){R.seen=true;cscNotice(T,P)}R.p+=dt/cscT(g);if(R.p>=1){R.p=1;R.done=true;cscDone(T,P)}}
  return{T,R,g,inR}}
function cscNotice(T,P){if(T.rp){try{netMsg(T.rp,'flash',`${P.name||'A pilot'} is scanning your cargo.`)}catch(e){}return}
  if(['hauler','trader','miner'].includes(T.role)&&!T.npcFled&&Math.random()<CSC.notice){T.npcFled=1;T.role='flee';if(T.ai)T.ai.tgt=null;feed(`${hullName(T.side,T.cls)} noticed your scan and is running for the gate.`,'warn')}}
function cscDone(T,P){if(FAC_IDS.includes(T.side)&&sectorOwner(W.sid)===T.side&&typeof smHeat==='function')smHeat(P,T.side,CSC.heat,'scanning its ships')}
{const o=hudUpdate;hudUpdate=function(){const r=o.apply(this,arguments);try{const s=cscTick();if(s){const tp=$('hTgt').querySelector('.tp');if(tp){const C=cscLoad(s.T),R=s.R;
      tp.insertAdjacentHTML('beforeend',`<div class="ts" style="margin-top:6px;color:#f5e663">Cargo scan${R.done?'':` · ${s.inR?Math.round(R.p*100)+'%':`out of range (${fmt(cscR(s.g))} m)`}`}</div><div class="ts">${R.done?cscExact(C):R.seen?esc(cscRough(C)):'Close in to scan its hold.'}</div>`)}}}catch(e){}return r}}
