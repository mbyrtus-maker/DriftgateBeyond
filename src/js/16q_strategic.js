//@src 16q_strategic.js
// ============================================================ the strategic map: a sector view with orders (Beyond stage 12)
// Clicking a system on the galaxy map (M) now opens a live top-down view of it beside the usual detail: its gates, station,
// outpost, rocks (Riftstone in pink), your Lairs and depots, and the ships there (live when the system is loaded, otherwise
// the capitals and convoys your intel knows of), with a count of threats. Below it, your forces there and their orders:
// your capital ships (stay here, or come here from elsewhere) and the AI crews at your depot (mine, haul, guard, idle).
function sxThreat(e){const P=S.player;return e&&(e.side==='brood'||e.side==='pirate'||FAC_IDS.includes(e.side)&&pilotHostile(P,e.side))}
function sxDraw(cv,sid){const c=cv.getContext('2d'),W0=cv.width,H0=cv.height,s=S.sectors[sid],w=WORLDS[sid];c.fillStyle='#05080f';c.fillRect(0,0,W0,H0);
  let R=2600;for(const g of GATES[sid]||[])R=Math.max(R,hyp(g.x,g.z)+400);const k=(W0/2-10)/R,X=x=>W0/2+x*k,Y=z=>H0/2+z*k;
  c.strokeStyle='rgba(54,67,95,.5)';for(const r of[.25,.5,.75,1]){c.beginPath();c.arc(W0/2,H0/2,(W0/2-10)*r,0,TAU);c.stroke()}
  for(const a of s.ast){c.fillStyle=a.rift?'#ff4fc8':'rgba(170,165,150,.55)';const r=Math.max(1,astR(a)*k*1.2);c.fillRect(X(a.x)-r/2,Y(a.z)-r/2,r,r)}
  for(const g of GATES[sid]||[]){c.strokeStyle='#6fb7ff';c.strokeRect(X(g.x)-4,Y(g.z)-4,8,8);c.fillStyle='#6fb7ff';c.font='9px sans-serif';c.fillText(DEF[g.to]?DEF[g.to].name.split(' ')[0]:'',X(g.x)+6,Y(g.z)+3)}
  const R0=S.stations[sid];if(R0){c.fillStyle=sideCol(R0.owner==='player'?'player':R0.owner);c.beginPath();c.arc(X(R0.x),Y(R0.z),7,0,TAU);c.fill()}
  for(const L of S.lairs||[])if(L.sid===sid&&L.hull>0&&(L.pid===(curPid()||'me'))){c.strokeStyle='#f0b24a';c.beginPath();c.arc(X(L.x),Y(L.z),5,0,TAU);c.stroke()}
  let threats=0,ships=0;const dot=(x,z,col,big)=>{c.fillStyle=col;c.beginPath();c.arc(X(x),Y(z),big?4:2,0,TAU);c.fill()};
  if(w){for(const e of w.ents){if(e.type!=='ship'||!e.alive||e.role==='limpet')continue;ships++;if(sxThreat(e))threats++;dot(e.x,e.z,e.isPlayer||e.rp?'#ffffff':sideCol(e.side),e.role==='frigate')}}
  else{for(const t of S.frigates||[])if(t.sector===sid&&(fMine(t)||covered(sid))){ships++;if(sxThreat(t))threats++;const o=rdir(.2);dot(o.x*900,o.z*900,fMine(t)?'#f0b24a':sideCol(t.side),true)}
    for(const t of S.traders||[])if(t.sector===sid&&covered(sid)){ships++;const o=rdir(.2);dot(o.x*1400,o.z*1400,sideCol(t.side))}}
  c.fillStyle='#cfd6e4';c.font='10px sans-serif';c.fillText(`${w?'live':'from intel'} · ${ships} ship${ships===1?'':'s'} · ${threats} threat${threats===1?'':'s'}`,8,H0-8);return{ships,threats}}
function sxHtml(sid){const P=S.player,mine=(S.frigates||[]).filter(t=>fMine(t)),here=mine.filter(t=>t.sector===sid),D=myDepots(P).filter(R=>R.sid===sid);
  let h=`<div><div class="h3">Sector view</div><canvas id="sxCv" width="300" height="300" style="width:100%;max-width:300px;aspect-ratio:1;display:block;border:1px solid var(--line)"></canvas>`;
  if(mine.length||D.length){h+=`<div class="h3" style="margin-top:8px">Your forces · orders</div>`;
    for(const t of mine)h+=`<div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin:3px 0"><b>${esc(t.name)}</b><span class="note" style="margin:0">${esc(DEF[t.sector].name)}${t.dest&&t.dest!==t.sector?` → ${esc(DEF[t.dest].name)}`:''}</span>${t.sector===sid?`<button class="btn sm" type="button" data-sx="hold" data-arg="${t.id}">Guard here</button>`:`<button class="btn sm" type="button" data-sx="come" data-arg="${t.id}">Come here</button>`}</div>`;
    for(const R of D)for(const c of R.crew||[])h+=`<div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin:3px 0"><b>${esc(c.name)}</b><span class="note" style="margin:0">${esc(CLASSES[c.cls].name)}${c.laid?' · laid up':''}</span>${['mine','haul','guard','idle'].map(j=>`<button class="btn sm" type="button" data-sx="crew" data-arg="${R.sid}:${c.id}:${j}" aria-pressed="${c.job===j}">${j}</button>`).join('')}</div>`}
  return h+`</div>`}
{const o=renderMapSide;renderMapSide=function(){o.apply(this,arguments);try{if(S.unb||S.training)return;const el=$('mapSide');el.insertAdjacentHTML('afterbegin',sxHtml(mapSel));const cv=$('sxCv');if(cv)sxDraw(cv,mapSel)}catch(err){console.error(err)}}}
function sxOrder(act,arg){const P=S.player;if(act==='come'||act==='hold'){const t=(S.frigates||[]).find(x=>String(x.id)===String(arg)&&fMine(x));if(!t)return'';t.dest=act==='come'?mapSel:t.sector;t.jumpTo=null;const m=act==='come'?`${t.name} ordered to ${DEF[mapSel].name}.`:`${t.name} holds ${DEF[t.sector].name}.`;feed(m,'info');return m}
  if(act==='crew'){if(NET.cl){netSend({t:'act',act:'crewjob',arg});return'Working…'}dockAction('crewjob',arg);return dockErr}return''}
{const el=$('mapSide');if(el)el.addEventListener('click',e=>{const b=e.target.closest('[data-sx]');if(!b)return;sxOrder(b.dataset.sx,b.dataset.arg);try{renderMapSide();drawMap()}catch(err){}})}
