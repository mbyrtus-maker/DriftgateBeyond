//@src 16zzzs_allegiance.js
// ============================================================ Beyond: the dock's Allegiance tab, reorganised (user, 9 Nov 2026)
// "Move all of the 'you' items to the top, reorganise the Powers, Leaders and Standing to be side by side in two columns,
// rework the bonuses to be more concise."
//   You (top): an audience or letters of marque where this dock offers them, your Contractor Rating, your standing with
//   each power and the freeports with each power's heat beside it, the Dread Pirate's bounty on you, your faction, your regent.
//   Then two columns: left, the powers (each with its leader and its bonuses in three short lines) and the Unbound;
//   right, the standing between the powers and the chronicle.
// This replaces the whole allegianceHtml chain (rating, heat, declare, the Unbound, audience, marque and regent wrappers);
// each piece is drawn here instead.
const AL_PERK={halcyon:[['Ships','Shields +12% · Hull −12%'],['Perk','Trade Charter: buys freeport ore when short'],['Career','Hauling +20% (Freeport jobs) · Gannet']],
  varkesh:[['Ships','Speed −10%'],['Perk','Dominion hulls: Hull +25%, self-repairing armour'],['Career','Mining +20% (Aurorite jobs) · Bombard']],
  ostrova:[['Ships','Reactor +12% · Shields −12%'],['Perk','Archive fleet: third escort, cheaper carriers'],['Career','Scout pay +40% · drive peek · Vesper']]};
function alPerkHtml(f){const L=AL_PERK[f];if(!L)return`<div class="note" style="margin:4px 0 0">${String(FAC(f).traitText||'').split('<br>').map(esc).join('<br>')}</div>`;
  return`<div style="display:grid;grid-template-columns:58px 1fr;gap:2px 10px;margin-top:6px;font-size:13px">${L.map(([k,v])=>`<span class="lab" style="margin:0;line-height:1.7">${k}</span><span style="color:var(--ivory,#ece4cf)">${esc(v)}</span>`).join('')}</div>`}
function alH3(t,top){return`<div class="h3" style="margin-top:${top==null?18:top}px">${t}</div>`}
allegianceHtml=function(P){P=P||S.player;relInit();let h='';
  // ---- you
  try{const c=P.docked?dockCtx():null;if(c){h+=audHtml(c,P);if(c.rum)h+=marqHtml(P)}}catch(e){console.error(e)}
  if(!P.sworn&&!S.unb)h+=ratingHtml(P);
  const heat=!P.sworn;
  h+=alH3('Your standing',4)+`<div class="tblw"><table class="t"><tbody>${STAND_POW.map(f=>{const v=standOf(f,P),pct=Math.round((v+100)/2),hw=heat&&FAC_IDS.includes(f)?heatWord(heatOf(f,P)):null;
    return`<tr><td style="width:110px"><b style="color:${sideCol(f)}">${esc(sideName(f))}</b></td><td><div style="height:6px;background:rgba(255,255,255,.08);position:relative;max-width:300px"><i style="position:absolute;left:0;top:0;bottom:0;width:${pct}%;background:${standCol(v)}"></i><i style="position:absolute;left:50%;top:-2px;bottom:-2px;width:1px;background:rgba(236,228,207,.4)"></i></div></td><td style="width:100px;color:${standCol(v)}">${standName(v)}</td><td style="width:110px" class="r">${hw?`<span class="note" style="margin:0">heat</span> <b style="color:${hw[1]}">${hw[0]}</b>`:''}</td></tr>`}).join('')}</tbody></table></div>`;
  h+=`<p class="note" style="margin:6px 0 0">${P.sworn?`You fly for ${esc(FAC(P.sworn).name)}. `:''}Heat is how hard a power's patrols are looking for you; it cools on its own. The Brood and the Unbound are always hostile.</p>`;
  try{const D=dpOf(),b=D&&D.bounty&&D.bounty[pkeyOf(P)];if(b)h+=`<p class="note" style="color:var(--danger);margin:6px 0 0">☠ ${esc(dpName(D))} has a ${fmt(b)} cr bounty on you: Unbound ships go for you first.</p>`}catch(e){}
  if(!P.sworn&&!S.unb){const n=controlCounts().player||0;h+=alH3('Your faction');
    if(P.decl){h+=`<div class="kv"><span>${esc(P.decl.name)}</span><b class="amber">${n} of ${VIC_NEED} systems</b></div><p class="note" style="margin:2px 0 8px">Hold ${VIC_NEED} systems for ${Math.round(WIN_TIME/60)} minutes to win the galaxy. Lose your last Station and the faction falls back into a company.${P.allied&&Object.keys(P.allied).length?` Allied with ${Object.keys(P.allied).map(f=>esc(FACTIONS[f].short)).join(', ')}.`:''}</p>`;
      for(const x of P.props||[])h+=`<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:4px 0"><span>${x.k==='ally'?`✉ ${esc(lName(x.f))} proposes an alliance`:`✉ ${esc(lName(x.f))} demands ${fmt(x.amt)} cr tribute`} · ${fmtT(Math.max(0,x.until-S.T))}</span><button class="btn sm" type="button" data-co="prop" data-arg="${x.id}:y">${x.k==='ally'?'Accept':'Pay'}</button><button class="btn sm" type="button" data-co="prop" data-arg="${x.id}:n">${x.k==='ally'?'Decline':'Refuse'}</button></div>`}
    else h+=`<div style="display:flex;gap:14px;align-items:center;flex-wrap:wrap"><span class="note" style="margin:0;flex:1;min-width:240px">Own a Station to declare your own faction: ${VIC_NEED} systems held for ${Math.round(WIN_TIME/60)} minutes wins the galaxy.</span><button class="btn${declOK(P)?' pri':''}" type="button" data-co="declare" ${declOK(P)?'':'disabled'}>Declare your faction</button></div>`}
  try{if(rgOn(P))h+=rgHtml(P)}catch(e){console.error(e)}
  // ---- the powers and their leaders | the standing between them and the chronicle
  let L=alH3('The powers and their leaders',0);
  for(const f of FAC_IDS){const ld=leaderOf(f);
    L+=`<div style="padding:10px 0;border-top:1px solid var(--line,#1d2740)"><div style="display:flex;gap:8px;align-items:baseline;flex-wrap:wrap"><b style="color:${sideCol(f)};font-size:15px">${esc(FAC(f).name)}</b><span style="flex:1"></span><span class="note" style="margin:0">${ld.ship&&!ld.ship.alive?'not flying':ld.ship?`in ${esc(DEF[ld.ship.sid].name)}`:''}</span></div>
      <div style="margin-top:2px">${esc(ld.title)} ${esc(ld.name)}${ld.n>1?` <span class="mass">${ordinal(ld.n)} of the line</span>`:''} <span class="note" style="margin:0">· ${ld.traits.map(esc).join(' · ')}</span></div>${alPerkHtml(f)}</div>`}
  try{const D=dpOf();if(D)L+=`<div style="padding:10px 0;border-top:1px solid var(--line,#1d2740)"><div style="display:flex;gap:8px;align-items:baseline;flex-wrap:wrap"><b style="color:${sideCol('pirate')};font-size:15px">The Unbound</b><span style="flex:1"></span><span class="note" style="margin:0">${D.ship.alive?(D.ship.rav?'aboard the Ravager':'flying'):'not flying'}</span></div><div style="margin-top:2px">${esc(dpName(D))}${D.n>1?` <span class="mass">${ordinal(D.n)} to wear the hat</span>`:''} <span class="note" style="margin:0">· ${D.traits.map(esc).join(' · ')}</span></div></div>`}catch(e){}
  let R=alH3('Between the powers',0)+`<div class="tblw"><table class="t"><thead><tr><th></th>${FAC_IDS.map(f=>`<th style="color:${sideCol(f)}">${esc(FAC(f).short)}</th>`).join('')}</tr></thead><tbody>${FAC_IDS.map(a=>`<tr><td style="color:${sideCol(a)}"><b>${esc(FAC(a).short)}</b></td>${FAC_IDS.map(b=>{if(a===b)return'<td style="color:var(--faint)">·</td>';const bd=relBandOf(a,b),P2=pairOf(a,b),tags=[P2.pact?'pact':'',P2.emb?'embargo':''].filter(Boolean).join(', ');return`<td><b style="color:${REL_BANDS[bd][1]}">${REL_BANDS[bd][0]}</b>${tags?`<span class="mass"> ${tags}</span>`:''}</td>`}).join('')}</tr>`).join('')}</tbody></table></div>`;
  const C=(S.chron||[]).slice(-14).reverse();R+=alH3('Chronicle')+(C.length?`<div class="log">${C.map(x=>`<div><b>${fmtT(x.T)}</b>${esc(x.msg)}</div>`).join('')}</div>`:'<div class="empty">Nothing yet: the powers are watching each other.</div>');
  h+=`<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px 32px;margin-top:24px;align-items:start"><div style="min-width:0">${L}</div><div style="min-width:0">${R}</div></div>`;
  return h};
