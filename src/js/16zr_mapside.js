//@src 16zr_mapside.js
// ============================================================ the map's side panel, minimal (Beyond screens pass, 3 Nov 2026)
// For the picked system, on top: its name (live or from intel), who holds it, its station and your base there; Set course /
// Clear course; a threat line when a strike is coming at it, with Guards intercept (that base's crews guard it, or a Guard
// job is posted); then Your forces: your crews based here and every capital of yours, each with a tick box and its status.
// Pick any of them and give the orders that fit: crews Mine, Haul, Guard, Idle; capitals Come here, Guard here, Patrol here,
// Escort me. The sector picture stays (hidden while the map itself is zoomed into the system). Everything the panel showed
// before (galaxy control, operations, your capital fleet, vaults, recent news, pilots online, New pilot) is under "More ▾".
let mpPick=new Set(),mpMore=false,mpMsg='';
function mpForces(sid){const P=S.player,me=pkeyOf(P),L=[];
  for(const R of myDepots(P).filter(R=>R.sid===sid))for(const c of R.crew||[]){const w=c.laid&&c.job!=='run'?['var(--danger)','laid up']:[c.job==='idle'?'var(--dim)':'#7ad9a7',JB_WORD[c.job]||c.job];L.push({key:`c:${R.sid}:${c.id}`,crew:1,R,c,name:c.name,cls:`${CLASSES[c.cls].name} · crew`,st:w,job:c.job})}
  for(const t of(S.frigates||[]).filter(fMine)){const j=HOP[t.sector]&&HOP[t.sector][sid],st=t.patrol?['#f0b24a',`patrolling ${DEF[t.patrol.base].name}`]:t.escort?['#f0b24a',t.escort.pid===me?'escorting you':'escorting']:t.sector===sid?['#7ad9a7','here']:t.dest===sid?['#f0b24a','on its way']:['var(--dim)',`${j} jump${j===1?'':'s'} away`];
    L.push({key:'t:'+t.id,cap:1,t,name:t.name,cls:`${isCar(t)?'Carrier':isDst(t)?'Destroyer':'Escort'} · capital${t.sector!==sid?' · in '+DEF[t.sector].name:''}`,st,ord:t.patrol&&t.patrol.base===sid?'patrol':t.escort&&t.escort.pid===me?'escort':t.sector===sid&&(!t.dest||t.dest===sid)?'hold':t.dest===sid?'come':null})}
  return L}
function mpHtml(sid){const P=S.player,d=DEF[sid],own=sectorOwner(sid),R=S.stations[sid],mineR=myDepots(P).find(x=>x.sid===sid),live=!!(W&&W.sid===sid)||!!WORLDS[sid];
  let h=`<div class="mpmin"><div style="display:flex;gap:10px;align-items:baseline;flex-wrap:wrap"><b class="mptitle" style="color:${sideCol(own)}">${esc(d.name)}</b><span style="display:inline-flex;gap:6px;align-items:center;font-size:12px;color:${live?'#7ad9a7':'var(--dim)'}"><span class="cdot" style="background:${live?'#7ad9a7':'#5a647c'}"></span>${live?'live':'from intel'}</span><span style="flex:1"></span><button class="cov" type="button" data-sx="zoom" data-arg="${mapZoom?'':sid}">${mapZoom?'◀ Galaxy':'Zoom in ▸'}</button></div>`;
  h+=`<div class="note" style="margin:4px 0 10px">Held by <b style="color:${sideCol(own)}">${own?esc(sideName(own)):'nobody'}</b>${R?` · ${esc(R.name)}`:''}${mineR?` · your ${mineR.pst?'Station, level '+staLvl(mineR):'Depot, level '+depLvl(mineR)}`:''}${sid===P.sector?' · you are here':` · ${HOP[P.sector][sid]} jump${HOP[P.sector][sid]===1?'':'s'}`}</div>`;
  h+=`<div class="mpslot-course"></div>`;
  const ev=(S.events||[]).find(e=>e.type==='offensive'&&e.sector===sid&&e.stage!=='done'&&(evKnown(e)||(mineR&&e.st===mineR.sid)||friendSide(evOwner(e))));
  if(ev){const tgt=mineR&&ev.st===mineR.sid;h+=`<div class="coalert" style="border-left-color:var(--danger);flex-wrap:wrap"><span class="cdot" style="background:var(--danger)"></span><span style="flex:1;min-width:160px">${ev.att==='brood'?'A Brood':`A ${esc(sideName(ev.att))}`} strike${tgt?' on your '+(mineR.pst?'Station':'Depot'):''} · ${ev.stage==='engaged'?'fighting now':`about ${fmtT(Math.max(0,(ev.eta||S.T)-S.T))}`}</span>${tgt?`<button class="btn sm" type="button" data-mp="guard" data-arg="${mineR.sid}">Guards intercept</button>`:''}</div>`}
  const F=mpForces(sid);for(const k of[...mpPick])if(!F.some(f=>f.key===k))mpPick.delete(k);
  if(F.length){h+=`<div class="lab" style="margin:6px 0 2px">Your forces</div>`;
    for(const f of F){const on=mpPick.has(f.key);h+=`<button class="mpforce${on?' on':''}" type="button" data-mp="pick" data-arg="${f.key}" aria-pressed="${on}"><span class="mpchk"></span><span style="min-width:0;flex:1"><b>${esc(f.name)}</b><span class="note cosub" style="margin:0">${esc(f.cls)}</span></span><span style="display:inline-flex;gap:6px;align-items:center;font-size:12px;color:${f.st[0]};white-space:nowrap"><span class="cdot" style="background:${f.st[0]}"></span>${esc(f.st[1])}</span></button>`}
    const pk=F.filter(f=>mpPick.has(f.key)),cr=pk.filter(f=>f.crew),cp=pk.filter(f=>f.cap),one=L=>L.length===1?L[0]:null;
    if(!pk.length)h+=`<div class="note" style="margin:8px 0 0">Tick your forces to give them orders.</div>`;
    if(cr.length){const j=one(cr)&&one(cr).job;h+=`<div class="lab" style="margin:10px 0 4px">${cr.length===1?esc(cr[0].name):cr.length+' crews'}</div><div class="coopts" style="margin:0">${[['mine','Mine here'],['haul','Haul home'],['guard','Guard the depot'],['idle','Idle']].map(([k,n])=>`<button class="${j===k?'on':''}" type="button" data-mp="crew" data-arg="${k}">${n}</button>`).join('')}</div>`}
    if(cp.length){const o=one(cp)&&one(cp).ord;h+=`<div class="lab" style="margin:10px 0 4px">${cp.length===1?esc(cp[0].name):cp.length+' capitals'}</div><div class="coopts" style="margin:0">${[['come','Come here'],['hold','Guard here'],['patrol','Patrol around here'],['escort','Escort me']].map(([k,n])=>`<button class="${o===k?'on':''}" type="button" data-mp="cap" data-arg="${k}">${n}</button>`).join('')}</div>`}}
  else h+=`<div class="note" style="margin:6px 0 0">None of your forces are here.${(S.frigates||[]).some(fMine)?'':' Crews work from your depots; capitals come from your Station\'s shipyard.'}</div>`;
  if(mpMsg)h+=`<div class="note" style="margin:8px 0 0;color:#7ad9a7">${esc(mpMsg)}</div>`;
  return h+`<div class="mpslot-sx"></div><button class="cov" type="button" data-mp="more" style="margin-top:12px">${mpMore?'Less ▴':'More ▾'}</button></div>`}
{const o=renderMapSide;renderMapSide=function(){const r=o.apply(this,arguments);try{if(!S||S.unb||S.training||!mapSel)return r;const el=$('mapSide');if(!el)return r;
  const old=document.createElement('div');old.className='mpold';while(el.firstChild)old.appendChild(el.firstChild);el.innerHTML=mpHtml(mapSel);
  // the course buttons and the sector picture keep their handlers: move them up
  const cs=el.querySelector('.mpslot-course'),bc=old.querySelector('#bCourse'),bx=old.querySelector('#bClear');if(bc||bx){const box=(bc||bx).parentElement;cs.appendChild(box);const n=box.nextElementSibling;if(n&&n.classList.contains('note')&&/^Course to/.test(n.textContent))cs.appendChild(n)}
  const cv=old.querySelector('#sxCv');if(cv&&!mapZoom){el.querySelector('.mpslot-sx').appendChild(cv);cv.style.marginTop='12px'}
  old.hidden=!mpMore;el.appendChild(old)}catch(e){console.error(e)}return r}}
function mpOrder(act,arg){const P=S.player,F=mpForces(mapSel),pk=F.filter(f=>mpPick.has(f.key));
  if(act==='pick'){mpPick.has(arg)?mpPick.delete(arg):mpPick.add(arg);mpMsg='';return}
  if(act==='more'){mpMore=!mpMore;return}
  if(act==='guard'){if(NET.cl){netSend({t:'act',act:'hgguard',arg});mpMsg='Working…';return}dockAction('hgguard',arg);mpMsg=dockErr;return}
  if(act==='crew'){const L=pk.filter(f=>f.crew);for(const f of L){const a=`${f.R.sid}:${f.c.id}:${arg}`;if(NET.cl)netSend({t:'act',act:'crewjob',arg:a});else dockAction('crewjob',a)}mpMsg=L.length?`✓ ${L.map(f=>f.name).join(', ')}: ${({mine:'mining',haul:'hauling',guard:'guarding',idle:'idle'})[arg]}.`:'';return}
  if(act==='cap'){const L=pk.filter(f=>f.cap);for(const f of L){const id=String(f.t.id);if(arg==='come'||arg==='hold'){sxOrder(arg,id);if(NET.cl)netSend({t:'fdest',id:f.t.id,dest:arg==='come'?mapSel:f.t.sector})}else sxOrder(arg,id)}mpMsg=L.length?`✓ ${L.map(f=>f.name).join(', ')}: ${({come:'coming here',hold:'guarding where it is',patrol:'patrolling around '+DEF[mapSel].name,escort:'escorting you'})[arg]}.`:'';return}}
{const el=$('mapSide');if(el)el.addEventListener('click',e=>{const b=e.target.closest('[data-mp]');if(!b)return;mpOrder(b.dataset.mp,b.dataset.arg);try{renderMapSide();drawMap()}catch(err){}})}
// a new system picked: a fresh selection
{const o=toggleMap;toggleMap=function(){mpPick.clear();mpMsg='';return o.apply(this,arguments)}}
