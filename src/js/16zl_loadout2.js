//@src 16zl_loadout2.js
// ============================================================ the Loadout screen (Beyond screens pass, 3 Nov 2026)
// Ship → Loadout (was Systems): a top-down schematic of your ship with every weapon and utility slot labelled around it
// (its part, icon and grade pips) and a strip of its systems below. Click a slot or a system; the panel on the right shows it:
//   - a part: its trait (maker's, your brand's, a Rift Shard's), its grade, the next upgrade with what you have of each
//     component (red when short) and the fee, Upgrade or Upgrade with a Rift Shard, Take out (to your hangar or store), and
//     Fit instead: every part that fits that slot, with where it is (hold, hangar) or its price here;
//   - a system: its grade, what it gives, the next grade's components (with what you're missing), the fee, To Grade N,
//     Aurora tuning and its variant, exactly as the old Systems tab offered them.
// Below the systems: ammunition, missiles and charges, and Rearm. The ship's stats stay in the header line.
// The old Loadout block in the Shipyard tab goes (it lives here now).
let ldSel='parts';
const LD_EFF={gun:'+10% damage a grade',laser:'+10% damage a grade',missile:'one more missile a grade',torpedo:'one more torpedo a grade',charge:'one more charge a grade',mlaser:'+15% cutting rate a grade',cargo:'+5% hold a grade',scanner:'+20% reach a grade',dronec:'+25% drone hull and +15% drone damage a grade',land:'one grade only',hide:'+4 t hidden a grade',bdev:'never used up (grades add nothing)',lrack:'one more limpet a grade'};
function ldShape(cls){if(blHull(cls))return'M0,-120 L40,-96 L52,40 L36,110 L-36,110 L-52,40 L-40,-96 Z M-52,-10 L-96,0 L-96,50 L-52,52 Z M52,-10 L96,0 L96,50 L52,52 Z';
  if(isHaulCls(cls))return'M0,-130 L36,-104 L40,110 L-40,110 L-36,-104 Z M-40,-60 L-92,-56 L-92,70 L-40,74 Z M40,-60 L92,-56 L92,70 L40,74 Z';
  return'M0,-150 L18,-80 L26,-20 L110,20 L150,34 L150,56 L110,58 L34,66 L28,110 L50,136 L0,128 L-50,136 L-28,110 L-34,66 L-110,58 L-150,56 L-150,34 L-110,20 L-26,-20 L-18,-80 Z'}
function ldPips(n,big){let s='';for(let i=1;i<=5;i++)s+=`<i style="display:inline-block;width:${big?14:9}px;height:${big?5:3}px;margin-right:2px;background:${i<=n?'var(--amber,#f0b24a)':'#232d45'}"></i>`;return s}
function ldSlotHtml(c,P,g,i){const F=fitOf(P),kind=(g==='w'?F.w:F.u)[i],gr=((g==='w'?F.g:F.ug)[i])||1,srcs=[P.cargo,c.storage||P.vault];
  let h=`<div class="lab">${g==='w'?'Weapon':'Utility'} ${i+1}</div>`;
  if(kind){const id=((g==='w'?F.wi:F.ui)||[])[i]||PART[kind],I=ITEMS[id],rt=F.rt&&F.rt[g+i];
    h+=`<div class="ldname">${gIcon(id,24)}<b>${esc(I.name)}</b></div><div class="note" style="margin:4px 0">${I.maker&&typeof mkLogoSvg==='function'?mkLogoSvg(I.maker,16,true)+' ':''}${esc(I.trTxt||'Standard part.')}${rt?` <span style="color:#ff7ad8">Rift: ${esc(trText(rt.tr))}</span>`:''}</div>
      <div style="margin:6px 0 12px">${ldPips(gr,1)} <span class="note">grade ${gr} · ${esc((WPN[kind]||UTIL[kind]||{}).desc||'')}</span></div>`;
    const q=pupQuote(c,P,`${g}:${i}`);if(q){const ok=haveIn(q.r,srcs)&&P.credits>=q.fee,short=Object.keys(q.r).filter(k=>countIn(k,srcs)<q.r[k]);
      h+=`<div class="ldbox"><div class="lab">To grade ${q.t}</div><div class="note" style="margin:2px 0 6px">${esc(LD_EFF[kind]||'')}</div><div>${Object.keys(q.r).map(k=>chip(k,q.r[k],countIn(k,srcs))).join('')}</div>
        <div class="note" style="margin:6px 0;color:${short.length?'var(--danger)':'var(--ok,#7ad9a7)'}">${short.length?'Missing: '+short.map(k=>`${q.r[k]-countIn(k,srcs)} ${esc(ITEMS[k].name)}`).join(', '):'You have everything it needs.'}${q.fee?` · fee ${fmt(q.fee)} cr`:''}</div>
        <div class="act"><button class="btn pri" data-act="pup" data-arg="${g}:${i}" ${ok?'':'disabled'}>Upgrade${q.fee?' · '+fmt(q.fee)+' cr':''}</button>${countIn('riftshard',srcs)?`<button class="btn" data-act="pupr" data-arg="${g}:${i}" ${ok?'':'disabled'} style="color:#ff7ad8;border-color:#ff7ad8">With a Rift Shard</button>`:''}${short.length&&c.market?`<button class="btn" data-act="tab" data-arg="market">Buy what's missing ›</button>`:''}</div></div>`}
    h+=`<div class="act" style="margin:10px 0"><button class="btn" data-act="fit" data-arg="${g}:${i}:">Take out → ${esc(String(c.storageName||'Vault').toLowerCase()==='vault'?'hangar':String(c.storageName).toLowerCase())}</button></div>`}
  else h+=`<div class="ldname"><b style="color:var(--dim)">Empty slot</b></div>`;
  const kinds=g==='w'?Object.keys(WPN).filter(k=>wpnOK(P.cls,k,i)):Object.keys(UTIL).filter(k=>!['bdev','lrack'].includes(k)||isScoutCls(P.cls));
  const cur=kind?(((g==='w'?F.wi:F.ui)||[])[i]||PART[kind]):null;let rows='';
  // (user, 3 Nov 2026) only the parts you have, in your hold or hangar: buying is the Market's job
  for(const k of kinds)for(const it of partItems(k)){if(it===cur)continue;const have=countIn(it,srcs);if(!have)continue;
    rows+=`<div class="ldopt">${gIcon(it,15)}<span style="flex:1;min-width:0"><span>${esc(ITEMS[it].name)}</span><br><span class="mass" style="margin:0">${esc(ITEMS[it].trTxt||'standard')} · ${have} on hand</span></span><button class="btn sm" data-act="fit" data-arg="${g}:${i}:${it}">Fit</button></div>`}
  if(rows)h+=`<div class="lab" style="margin-top:12px">Fit instead · from your hold and hangar</div>${rows}`;else h+=`<div class="note" style="margin-top:12px">No other parts for this slot in your hold or hangar.${c.market?' Buy parts on the Market, then fit them here.':''}</div>`;return h}
// (user, 8 Nov 2026) the systems have their own places on the ship, like the weapon and utility slots: fire control, the
// shield emitter, the reactor and armour down the left, the payload bay, cargo hold, blast rig (mining hulls) and drive down
// the right, each on a leader line to where it sits in the hull; the strip of systems under the ship is gone
// (user, 8 Nov 2026) armour, the cargo hold and the payload bay sit at the side with no leader line: they're the whole hull
const LD_SYS_FREE=new Set(['armor','cargo','payload']);
const LD_SYS_AT={weapon:[0,-112],shield:[-8,-62],power:[0,6],armor:[-14,74],payload:[10,-34],cargo:[14,42],drill:[12,82],engine:[0,104]};
function ldSysName(P,sl){const m=(P.sysm||{})[sl],t=P.tiers[sl]||1,I=m&&typeof rdGid==='function'?ITEMS[rdGid(`sy_${m}_${sl}`,t)]:null;return I?I.name:'Standard'}
function ldLeft(c,P){const F=fitOf(P),W0=572,cw=134,rh=54,st=W.player&&W.player.st;
  const nW=F.w.length,nU=F.u.length,ny=Math.max(1,Math.ceil(nW/2));
  const L=['weapon','shield','power','armor'],R=['payload','cargo',...(blHull(P.cls)?['drill']:[]),'engine'],y0=8+ny*rh+10,uy=y0+Math.max(L.length,R.length)*rh+6,H0=uy+52,cx=W0/2,cy=Math.round((8+uy)/2)+6,k=.95;
  const slots=[];
  F.w.forEach((w,i)=>{const side=i%2?1:-1,row=Math.floor(i/2);slots.push({g:'w',i,x:side<0?4:W0-cw-4,y:8+row*rh,ax:cx+side*(40+row*18),ay:cy-60+row*40,side})});
  F.u.forEach((u,i)=>{slots.push({g:'u',i,x:W0/2-(cw+8)*nU/2+i*(cw+8)+4,y:uy,ax:cx+(i-(nU-1)/2)*24,ay:cy+90,side:0})});
  L.forEach((sl,i)=>slots.push({g:'s',sl,x:4,y:y0+i*rh,ax:cx+LD_SYS_AT[sl][0]*k,ay:cy+LD_SYS_AT[sl][1]*k,side:-1}));
  R.forEach((sl,i)=>slots.push({g:'s',sl,x:W0-cw-4,y:y0+i*rh,ax:cx+LD_SYS_AT[sl][0]*k,ay:cy+LD_SYS_AT[sl][1]*k,side:1}));
  let svg=`<svg width="${W0}" height="${H0}" viewBox="0 0 ${W0} ${H0}" aria-hidden="true" style="position:absolute;inset:0"><path d="${ldShape(P.cls)}" transform="translate(${cx} ${cy}) scale(${k})" fill="#0f1729" stroke="${sideCol(P.faction)||'#4fd8d0'}" stroke-width="1.6"/>`;
  let btns='';for(const s of slots){const sys=s.g==='s',key=sys?'sys:'+s.sl:`${s.g}:${s.i}`,on=ldSel===key,ex=s.side<0?s.x+cw:s.side>0?s.x:s.x+cw/2,ey=s.side?s.y+24:s.y;
    if(!(sys&&LD_SYS_FREE.has(s.sl)))svg+=`<line x1="${s.ax}" y1="${s.ay}" x2="${ex}" y2="${ey}" stroke="${on?'#f0b24a':sys?'#26344a':'#2b3a52'}"${sys?' stroke-dasharray="3 3"':''}/><circle cx="${s.ax}" cy="${s.ay}" r="${sys?3:3.5}" fill="${on?'#f0b24a':sys?'#26344a':'#2b3a52'}"/>`;
    const pos=`left:${s.x}px;top:${s.y}px;width:${cw}px${s.side>0?';text-align:right;align-items:flex-end':''}`;
    if(sys){const t=P.tiers[s.sl]||1,lab=typeof RD_SYSN!=='undefined'&&RD_SYSN[s.sl]?RD_SYSN[s.sl][0].toUpperCase()+RD_SYSN[s.sl].slice(1):SLOT[s.sl].name,m=(P.sysm||{})[s.sl];
      btns+=`<button class="ldslot ldsysp${on?' on':''}" type="button" data-act="ldsel" data-arg="${key}" style="${pos}" title="${esc(lab)}: ${esc(ldSysName(P,s.sl))}"><span class="lab" style="font-size:10px">${esc(lab)}</span><span class="ldsn">${m&&typeof mkLogoSvg==='function'?mkLogoSvg(m,12,true)+' ':''}${esc(ldSysName(P,s.sl))}</span><span>${ldPips(t)}${(P.tune||{})[s.sl]?' '+'✦'.repeat(P.tune[s.sl]):''}</span></button>`;continue}
    const kind=(s.g==='w'?F.w:F.u)[s.i],gr=((s.g==='w'?F.g:F.ug)[s.i])||1,id=kind?(((s.g==='w'?F.wi:F.ui)||[])[s.i]||PART[kind]):null;
    btns+=`<button class="ldslot${on?' on':''}" type="button" data-act="ldsel" data-arg="${key}" style="${pos}"><span class="lab" style="font-size:10px">${s.g==='w'?'Weapon':'Utility'} ${s.i+1}</span><span class="ldsn">${id?gIcon(id,13)+esc(ITEMS[id].name):'<span style="color:var(--dim)">empty</span>'}</span><span>${id?ldPips(gr):''}</span></button>`}
  svg+=`</svg>`;
  const q=rearmQuote(P),t=isTorpHull(P.cls),rows=[ammoCap(P)?`Rounds ${fmt(P.ammo||0)} / ${fmt(ammoCap(P))}`:'',pRack(P)?`${t?'Torpedoes':'Missiles'} ${P.rack||0} / ${pRack(P)}`:'',blCap(P)?`Charges ${P.blN||0} / ${blCap(P)}`:'',typeof drnCap==='function'&&drnCap(P)?`Drones ${(P.bay&&P.bay.drone)||0} / ${drnCap(P)}`:''].filter(Boolean);
  return`<div class="ldhead"><b>${esc((FAC(P.faction)||{hulls:{}}).hulls[P.cls]||CLASSES[P.cls].name)}</b> <span class="note" style="margin:0">${esc(CLASSES[P.cls].name)} · ${F.w.length} weapon, ${F.u.length} utility${st?` · ${Math.round(st.maxSpd)} m/s · ${Math.round(st.sCap)} shield · ${Math.round(st.hull)} hull · ${st.cargo} t`:''}</span></div>
    <div class="ldmap"><div style="position:relative;width:${W0}px;height:${H0}px">${svg}${btns}</div></div>
    <div class="act" style="margin-top:8px;align-items:center;border-top:1px solid var(--line);padding-top:8px"><button class="btn" data-act="rearm" ${q.n&&(!c.wallet||P.credits>0)?'':'disabled'}>Rearm${q.n?` · ${fmt(q.tot)} cr`:''}</button><span class="note" style="margin:0 0 0 8px">${rows.join(' · ')||'No payload weapons fitted.'}</span></div>`}
{const o=loadoutHtml;loadoutHtml=function(c,P){return S&&!S.unb&&!S.training?'':o.apply(this,arguments)}}
{const o=dockClick;dockClick=function(act,arg){if(act==='ldsel'){ldSel=arg;renderDock();return}return o.apply(this,arguments)}}
{const o=renderDock;renderDock=function(){const r=o.apply(this,arguments);try{
  const T=$('dTabs');if(T&&!S.unb)for(const b of T.querySelectorAll('button[data-arg="upg"]:not(.mtab)'))if(b.firstChild&&b.firstChild.nodeType===3)b.firstChild.nodeValue='Loadout';
  if(dockTab!=='upg'||S.unb||S.training||!loadOn())return r;const c=dockCtx(),P=S.player,B=$('dBody');if(!c||!B)return r;
  const slotEls=[...B.querySelectorAll('.slots > *')],intro=B.querySelector('.grid2 .note');
  const F=fitOf(P);if(ldSel.startsWith('w:')&&!(+ldSel.slice(2)<F.w.length))ldSel='parts';if(ldSel.startsWith('u:')&&!(+ldSel.slice(2)<F.u.length))ldSel='parts';
  let right='';if(ldSel==='parts')right=ldPartsHtml(c,P);else if(ldSel.startsWith('sys:')){const id=ldSel.slice(4),sl=SLOT[id];right=`<div class="lab">System</div><div class="ldname"><b>${esc(sl?sl.name:id)}</b></div><div class="note" style="margin:4px 0 10px">Built into the hull and upgraded in place: it never comes out, and it carries over with the ship in your hangar.</div><div id="ldSysHost"></div>`}
  else{const[g,i]=ldSel.split(':');right=ldSlotHtml(c,P,g,+i)}
  if(ldSel!=='parts')right=`<button class="mkf" type="button" data-act="ldsel" data-arg="parts" style="margin:0 0 10px">‹ Your parts</button>`+right;
  const host=document.createElement('div');host.className='ldwrap';host.innerHTML=`<div class="ldl">${ldLeft(c,P)}</div><div class="ldr">${right}</div>`;
  if(ldSel.startsWith('sys:')){const idx=SLOTS.findIndex(s=>s.id===ldSel.slice(4)),el=slotEls[idx];const H=host.querySelector('#ldSysHost');if(el&&H){H.appendChild(el);el.classList.add('ldsysdetail')}if(intro&&H){const n=document.createElement('div');n.className='note';n.style.marginTop='14px';n.innerHTML=intro.innerHTML;H.appendChild(n)}}
  B.innerHTML='';B.appendChild(host)}catch(err){console.error(err)}return r}}
// ---- the Loadout's first view (user, 3 Nov 2026): the parts in your hold and hangar that this ship can take, each with Fit
// into the best slot for it (an empty one first, then one holding the same kind, then the first that takes it); pick a slot
// on the ship for its grades and the rest, or a system's + for its grades
function ldTarget(P,it){const k=ITEMS[it]&&ITEMS[it].part;if(!k)return null;const F=fitOf(P),ws=!!WPN[k],A=ws?F.w:F.u;
  const ok=i=>ws?wpnOK(P.cls,k,i):!(k==='dronec'&&!drnHull(P.cls))&&!(k==='claim'&&!beaconCls(P.cls))&&!(['bdev','lrack'].includes(k)&&!isScoutCls(P.cls))&&!!UTIL[k];
  let i=A.findIndex((x,j)=>!x&&ok(j));if(i<0)i=A.findIndex((x,j)=>x===k&&ok(j));if(i<0)i=A.findIndex((x,j)=>ok(j));return i<0?null:{g:ws?'w':'u',i,was:A[i]}}
function ldPartsHtml(c,P){const srcs=[P.cargo,c.storage||P.vault],L=ITEM_ORDER.filter(it=>ITEMS[it]&&ITEMS[it].part&&countIn(it,srcs)>0);
  let h=`<div class="lab">Your parts</div><div class="ldname"><b>Fit from your hold and hangar</b></div><div class="note" style="margin:4px 0 12px">Parts you have that this ship can take. Pick a slot on the ship to see its part, grades and other choices, or a system to see what's installed and what can replace it.</div>`;
  let rows='',no=0;for(const it of L){const T=ldTarget(P,it);if(!T){no++;continue}const was=T.was?ITEMS[(((T.g==='w'?fitOf(P).wi:fitOf(P).ui)||[])[T.i])||PART[T.was]]:null;
    rows+=`<div class="ldopt">${gIcon(it,15)}<span style="flex:1;min-width:0"><span>${esc(ITEMS[it].name)}</span><br><span class="mass" style="margin:0">${esc(ITEMS[it].trTxt||'standard')} · ${countIn(it,srcs)} on hand · ${T.g==='w'?'Weapon':'Utility'} ${T.i+1}${was?` (replaces ${esc(was.name)})`:' (empty)'}</span></span><button class="btn sm" data-act="fit" data-arg="${T.g}:${T.i}:${it}">Fit</button></div>`}
  h+=rows||`<div class="empty">No parts for this ship in your hold or hangar.${c.market?' Buy parts on the Market (Trade), then fit them here.':''}</div>`;
  if(no)h+=`<div class="note" style="margin-top:10px">${no} other part${no>1?'s':''} you have won't fit this ship.</div>`;return h}
