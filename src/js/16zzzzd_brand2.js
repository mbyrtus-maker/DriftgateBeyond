//@src 16zzzzd_brand2.js
// ============================================================ Beyond: the Brand screen, every buildable part (user, 9 Nov 2026)
// "For 'My brand' you're going to have to move that into a separate screen and list all the parts that can be built. Might
// do a similar screen to the market where you select the type of parts and then a menu from there." Asked which parts: all
// of them, systems included. See BEYOND_DESIGN.md "The Brand screen".
//   Company → Brand: the Market's part filters (Drive … Utility), the parts of the picked filter, the picked part's traits.
//   New brand kinds: the drone controller; the name-only parts (landing kit, beacon rig, launch rack, cargo scanner, hidden
//   hold); the eight systems (sys_<slot>). Branded parts and systems come in grades with the makers' recipes. Items carry
//   brand:N, never maker. An installed brand system is P.sysm[slot]='bp<N>'; sysTr reads its traits from the brand.
//   Built at your own base: Station → Fab → Your brand (top grade from the base: Depot G2, G3 at level 3; Station G4, G5 at
//   three buildings).
for(const[k,v]of Object.entries({thrust:'thrust',maxSpd:'top speed',turn:'turning',eCap:'reactor capacity',eRegen:'reactor recharge',sCap:'shield strength',hull:'hull',shotCost:'shot energy',lockT:'lock time',reload:'reload time',drill:'blast power'}))if(!TR_TXT[k])TR_TXT[k]=v;
const BR_PLAIN=['land','bdev','lrack','cscan','hide'];
const BR_SYSN={engine:'drive',power:'reactor',shield:'shield emitter',weapon:'fire control',armor:'armour',drill:'blast rig',cargo:'cargo hold',payload:'payload bay'};
BR.step.dronec={dh:[.06,1,1],dd:[.06,1,1],speed:[.01,1,1]};
for(const k of BR_PLAIN)if(PART[k])BR.step[k]={};
Object.assign(BR.step,{sys_engine:{thrust:[.03,1,1],maxSpd:[.02,1,1],turn:[.03,1,1]},sys_power:{eCap:[.03,1,1],eRegen:[.03,1,1]},
  sys_shield:{sCap:[.03,1,1],eRegen:[.02,1,1],maxSpd:[.01,1,1]},sys_weapon:{dmg:[.02,1,1],lockT:[.04,-1,1],shotCost:[.03,-1,1]},
  sys_armor:{hull:[.03,1,1],maxSpd:[.01,1,1],turn:[.02,1,1]},sys_cargo:{cargo:[.03,1,1],maxSpd:[.01,1,1],thrust:[.02,1,1]},
  sys_drill:{drill:[.04,1,1],eRegen:[.02,1,1],maxSpd:[.01,1,1]},sys_payload:{reload:[.03,-1,1],cargo:[.02,1,1],thrust:[.02,1,1]}});
const BR_NEWPART=['dronec',...BR_PLAIN].filter(k=>PART[k]&&!BR_KINDS.includes(k));
for(const k of[...BR_NEWPART,...Object.keys(SLOT).map(s=>'sys_'+s)])if(!BR_KINDS.includes(k))BR_KINDS.push(k);
function brIsSys(k){return String(k).startsWith('sys_')}
function brKindName(k){if(brIsSys(k)){const n=BR_SYSN[k.slice(4)]||k.slice(4);return n[0].toUpperCase()+n.slice(1)}const D=WPN[k]||UTIL[k];return D?D.name:k}
function brStd(k){return brIsSys(k)?rdGid('sy_'+k.slice(4),1):PART[k]}
// the kinds graded the way the makers grade them
const BR_GK=new Set(Object.values(ITEMS).filter(I=>I&&I.maker&&I.grade>1&&I.part).map(I=>I.part));
// ---- items: the new part kinds at grade 1, every graded part kind at grades 2-5, the systems at grades 1-5
for(let N=0;N<BR.slots;N++){
  for(const k of BR_NEWPART){const id=`bp${N}_${k}`,base=brKindName(k);
    ITEMS[id]={recipe:{...PART_RC[k]},col:PART_COL[k],part:k,brand:N,get name(){return`${brName(N)} ${base.replace(/^./,x=>x.toLowerCase())}`},get tr(){return brTr(N,k)},get trTxt(){const t=trText(brTr(N,k));return t?`${brName(N)} (your brand): ${t}.`:`${brName(N)}: carries your name.`}};
    ITEM_ORDER.push(id);(MK_ITEMS[k]=MK_ITEMS[k]||[]).push(id)}
  for(const k of BR_KINDS){if(brIsSys(k)||!BR_GK.has(k))continue;const id=`bp${N}_${k}`;if(!ITEMS[id])continue;
    for(let g=2;g<=5;g++){const gid=rdGid(id,g),rc={...ITEMS[id].recipe};for(let t=2;t<=g;t++)for(const x in partUpg(t))rc[x]=(rc[x]||0)+partUpg(t)[x];
      ITEMS[gid]={recipe:rc,col:ITEMS[id].col,part:k,brand:N,grade:g,base:id,get name(){return`${ITEMS[id].name} G${g}`},get tr(){return brTr(N,k)},get trTxt(){return ITEMS[id].trTxt}};ITEM_ORDER.push(gid);(MK_ITEMS[k]=MK_ITEMS[k]||[]).push(gid)}}
  for(const sl in SLOT){const id=`sy_bp${N}_${sl}`,k='sys_'+sl;
    for(let g=1;g<=5;g++){const gid=rdGid(id,g);ITEMS[gid]={recipe:compInv(sl,g),col:'#9fb3d8',sys:sl,grade:g,base:id,brand:N,get name(){return`${brName(N)} ${BR_SYSN[sl]}${g>1?' G'+g:''}`},get tr(){return brTr(N,k)},
      get trTxt(){const t=trText(brTr(N,k));return`${brName(N)} (your brand): ${BR_SYSN[sl]}, grade ${g}${t?' · '+t:''}.`}};ITEM_ORDER.push(gid)}}}
// a brand system's traits, like a maker's
{const o=sysTr;sysTr=function(m,sl){const x=/^bp(\d+)$/.exec(m||'');if(x)return brTr(+x[1],'sys_'+sl);return o.apply(this,arguments)}}
// installing one records the brand
{const o=rdSysFit;rdSysFit=function(arg){const[sl,id]=String(arg).split(':'),I=ITEMS[id];const r=o.apply(this,arguments);try{if(I&&I.brand!=null&&I.sys===sl&&String(r).startsWith('✓')){const P=S.player;(P.sysm=P.sysm||{})[sl]='bp'+I.brand;if(W&&W.player)refreshPlayerStats()}}catch(e){console.error(e)}return r}}
// the brand's points check names every kind (the systems included)
brSave=function(P,arg){if(!myDepots(P).length)return'Your brand begins with your first Depot.';const N=brSlot(P,true);if(N==null)return'No brand slot free in this galaxy.';const B=brOf(N);
  const[nmE,spec]=String(arg).split('|'),name=decodeURIComponent(nmE||'').replace(/[<>]/g,'').trim().slice(0,24)||B.name,pts={};
  for(const part of String(spec||'').split(';')){if(!part)continue;const[k,rest]=part.split(':');if(!BR.step[k])continue;for(const kv of String(rest||'').split(',')){const[t,v]=kv.split('=');const n=Math.round(+v||0);if(!BR.step[k][t]||!n)continue;(pts[k]=pts[k]||{})[t]=clamp(n,-BR.range,BR.range)}}
  for(const k in pts){if(brCost({[k]:pts[k]})>brBudget(N))return`${brKindName(k)}: the strengths cost more points than the weaknesses pay back.`}
  const same=JSON.stringify(pts)===JSON.stringify(B.pts||{});if(!same&&B.set){if(P.credits<BR.respec)return`Reshaping your brand costs ${fmt(BR.respec)} cr.`;payFrom(P,'neutral',BR.respec)}
  B.name=name;if(!same){B.pts=pts;B.set=(B.set||0)+1}return`✓ ${name}${same?' renamed':`${/s$/i.test(name)?"'":"'s"} brand ${B.set>1?'reshaped':'set'}`}.`};
// ---- building at your own base
function brGradeCap(R){return!R?0:R.pst?(staLvl(R)>=3?5:4):(depLvl(R)>=3?3:2)}
function brMyBase(P){const R=P&&P.docked==='station'&&S.stations[P.sector];return R&&R.owner==='player'&&(R.pid||'me')===pkeyOf(P)?R:null}
function brItemAt(N,k,g){const id=brIsSys(k)?`sy_bp${N}_${k.slice(4)}`:`bp${N}_${k}`,gid=rdGid(id,g),I=ITEMS[gid];return I&&Object.keys(I.recipe).length?gid:null}
function brMake(P,k,n){const I=ITEMS[k],R=brMyBase(P);if(!I||I.brand==null)return'No such part.';if(!R)return'Your brand is built at your own Depot or Station.';
  const N=brSlot(P);if(N==null||I.brand!==N)return'That is another company\'s brand.';const g=I.grade||1,cap=brGradeCap(R);if(g>cap)return`${R.name}'s workshop builds up to grade ${cap}.`;
  const r=I.recipe,srcs=[P.cargo,R.stock];if(!Object.keys(r).length)return'Nothing to build.';let made=0;const lim=n==='max'?999:Math.max(1,Math.round(+n||1));
  while(made<lim&&haveIn(r,srcs)){takeFrom(r,srcs);inv.add(R.stock,k,1);made++}return made?`✓ Built ${made} ${I.name} into ${R.name}'s store.`:`Not enough materials for the ${I.name}.`}
{const o=dockAction;dockAction=function(act,arg){if(act==='make'&&!S.unb){const[k,n]=String(arg).split(':'),I=ITEMS[k];if(I&&I.brand!=null){dockErr=brMake(S.player,k,n);return}}return o.apply(this,arguments)}}
let brFabG=1;
function brFabOn(c,P){return!!(c&&c.baseOwner&&!S.unb&&brMyBase(P)&&brSlot(P)!=null)}
function brFabHtml(c,P){const R=brMyBase(P),N=brSlot(P);if(!R||N==null)return'';const cap=brGradeCap(R);brFabG=clamp(brFabG,1,cap);const srcs=[P.cargo,R.stock];
  let h=`<p class="note" style="margin:0 0 10px">Your brand's parts and systems, built to the shape you set on Company → Brand. ${esc(R.name)}'s workshop builds up to grade ${cap}${R.pst?(cap<5?' (grade 5 with three buildings)':''):` (${cap<3?'grade 3 at Depot level 3; ':''}a Station builds grade 4 and 5)`}. Fitting a grade still follows your Contractor Rating.</p>`;
  h+=`<div class="obox-row obox-sys" style="margin-bottom:10px">${[1,2,3,4,5].map(g=>`<button class="obox${brFabG===g?' on':''}" type="button" data-act="brfabg" data-arg="${g}" ${g>cap?'disabled':''} aria-pressed="${brFabG===g}">Grade ${g}</button>`).join('')}</div>`;
  h+=`<div class="tblw"><table class="t"><thead><tr><th>Part</th><th>Recipe</th><th class="r">Have</th><th></th></tr></thead><tbody>`;let any=0;
  for(const grp of MK_PARTS)for(const k of brKindsIn(grp)){const id=brItemAt(N,k,brFabG);if(!id)continue;any++;const r=ITEMS[id].recipe,can=haveIn(r,srcs);
    h+=`<tr><td class="iname">${sw(id)}${esc(ITEMS[id].name)}<span class="mass">${MK_GN[grp]} · ${mass(id)} t</span></td><td>${Object.keys(r).map(i=>chip(i,r[i],countIn(i,srcs))).join('')}</td><td class="r num">${countIn(id,srcs)}</td>
      <td><div class="act"><button class="btn sm" data-act="make" data-arg="${id}:1" ${can?'':'disabled'}>Make 1</button><button class="btn sm" data-act="make" data-arg="${id}:max" ${can?'':'disabled'}>Make max</button></div></td></tr>`}
  h+=`</tbody></table></div>`;if(!any)h+=`<div class="empty">Nothing of your brand comes in grade ${brFabG}.</div>`;return h}
{const o=dockClick;dockClick=function(act,arg){if(act==='brfabg'){brFabG=+arg||1;renderDock();return}return o.apply(this,arguments)}}
// ---- the Brand screen
function brKindsIn(grp){return BR_KINDS.filter(k=>{const s=brStd(k);return s&&ITEMS[s]&&mkGroup(s)===grp})}
let brCat='p_wpn',brPick=null;
function brStepLab(k,t,v){const St=BR.step[k][t],eff=v*St[0]*St[1];return t==='mag'?`${eff>0?'+':''}${eff} ${TR_TXT[t]}`:`${eff>0?'+':eff<0?'−':'±'}${Math.round(Math.abs(eff)*1000)/10}% ${TR_TXT[t]||t}`}
function brShapeTxt(k,g){const St=BR.step[k];if(!Object.keys(St).length)return'name only';const L=Object.keys(g||{}).filter(t=>g[t]&&St[t]).map(t=>brStepLab(k,t,g[t]));return L.length?L.join(', '):'standard'}
function brScreenHtml(P){let h='';if(!myDepots(P).length)return`<p class="note">Your brand begins with your first Depot: parts and systems built at its workshop carry your company's name and the traits you shape here.</p>`;
  const N=brSlot(P,true),B=N!=null?brOf(N):null,D=brDraftGet(),bud=N!=null?brBudget(N):0;if(!B)return`<p class="note">No brand slot free in this galaxy.</p>`;
  h+=`<div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:6px"><span class="lab" style="margin:0">Company name</span><input id="brName" maxlength="24" value="${esc(B.name||`${P.name||'Pilot'}'s Works`)}" style="background:var(--bg2,#111);color:inherit;border:1px solid var(--line);padding:4px 8px;font:inherit"><span class="note" style="margin:0;flex:1;min-width:260px">Built at your Depot's or Station's workshop (Station → Fab → Your brand), your parts and systems carry this name and the traits you shape here. Each strength costs a point, each weakness pays one back: every part nets to zero${bud?` (your brand has ${bud} extra)`:''}. The first shape is free; reshaping costs ${fmt(BR.respec)} cr and reshapes every part of your brand, fitted or stored.</span></div>`;
  const cnt=g=>brKindsIn(g).length,shaped=g=>brKindsIn(g).filter(k=>Object.values(D.pts[k]||{}).some(v=>v)).length;
  if(!MK_PARTS.includes(brCat)||!cnt(brCat))brCat=MK_PARTS.find(cnt)||'p_wpn';const L=brKindsIn(brCat);if(!L.includes(brPick))brPick=L[0]||null;
  h+=`<div class="obox-row" style="margin:12px 0">${MK_PARTS.map(g=>`<button class="obox${brCat===g?' on':''}" type="button" data-co="brcat" data-arg="${g}" ${cnt(g)?'':'disabled'} aria-pressed="${brCat===g}">${MK_GN[g]} <span>${shaped(g)} / ${cnt(g)}</span></button>`).join('')}</div>`;
  h+=`<div class="cowrap"><div class="colist">`;
  for(const k of L){const on=k===brPick,c=brCost({[k]:D.pts[k]||{}}),st=brShapeTxt(k,D.pts[k]),bad=c>bud;
    h+=`<button class="corow${on?' on':''}" type="button" data-co="brpick" data-arg="${k}">${gIcon(brStd(k),20)}<span><b>${esc(brKindName(k))}</b><br><span class="note" style="margin:0;color:${bad?'var(--danger)':st==='standard'||st==='name only'?'var(--dim)':'var(--ok,#7ad9a7)'}">${esc(st)}${brIsSys(k)?' · system':''}</span></span></button>`}
  h+=`</div><div class="codet">`;
  if(brPick){const k=brPick,St=BR.step[k],g=D.pts[k]||{},c=brCost({[k]:g}),eg=brItemAt(N,k,1)||brItemAt(N,k,2),gs=[1,2,3,4,5].filter(x=>brItemAt(N,k,x));
    h+=`<div class="lab">${esc(MK_GN[brCat])}${brIsSys(k)?' · system':''}</div><div class="ldname">${gIcon(brStd(k),26)}<b>${esc(eg?ITEMS[eg].name.replace(/ G\d$/,''):brKindName(k))}</b></div>`;
    if(!Object.keys(St).length)h+=`<p class="note">No trait to shape: built at your workshop it carries your company's name.</p>`;
    else{h+=`<div style="display:grid;grid-template-columns:auto 1fr auto;gap:6px 10px;align-items:center;margin:8px 0">`;
      for(const t of Object.keys(St)){const v=g[t]||0;h+=`<button class="btn sm" type="button" data-co="brstep" data-arg="${k}:${t}:-1" ${v<=-BR.range?'disabled':''} aria-label="Less ${esc(TR_TXT[t]||t)}">−</button><span style="text-align:center;color:${v>0?'var(--ok,#7ad9a7)':v<0?'var(--danger)':'var(--dim)'}">${esc(brStepLab(k,t,v))}</span><button class="btn sm" type="button" data-co="brstep" data-arg="${k}:${t}:1" ${v>=BR.range?'disabled':''} aria-label="More ${esc(TR_TXT[t]||t)}">+</button>`}
      h+=`</div><div class="kv"><span>Points</span><b style="color:${c>bud?'var(--danger)':c<0?'var(--dim)':'inherit'}">${c>0?'+':''}${c}${c>bud?' · needs weaknesses to pay for it':c<0?' · weaknesses unspent':' · balanced'}</b></div>`}
    h+=`<div class="kv"><span>Grades</span><b>${gs.length?gs.map(x=>'G'+x).join(' · '):'—'}</b></div>`;
    if(eg){const r=ITEMS[eg].recipe;h+=`<div class="kv"><span>Recipe (G${ITEMS[eg].grade||1})</span><b style="font-weight:400">${Object.keys(r).map(i=>`${r[i]} ${esc(ITEMS[i]?ITEMS[i].name:i)}`).join(' · ')}</b></div>`}
    h+=`<p class="note" style="margin:8px 0 0">${brIsSys(k)?'Install it on Ship → Upgrades, like a maker\'s system.':'Fit it on Ship → Loadout, like any part.'} A Depot's workshop builds up to grade 2 (3 at level 3), a Station's up to 4 (5 with three buildings).</p>`}
  h+=`</div></div>`;
  const bad=BR_KINDS.some(k=>brCost({[k]:D.pts[k]||{}})>bud),same=JSON.stringify(D.pts)===JSON.stringify(B.pts||{});
  h+=`<div class="act" style="margin-top:12px"><button class="btn pri" type="button" data-co="brsave" ${bad?'disabled':''}>${same?'Save name':B.set?`Reshape · ${fmt(BR.respec)} cr`:'Set the brand'}</button><button class="btn" type="button" data-co="brreset" ${same?'disabled':''}>Undo changes</button>${bad?`<span class="note" style="color:var(--danger);margin:0">Some strengths aren't paid for by weaknesses.</span>`:''}</div>`;
  return h}
// Holdings no longer carries the brand
brHtml=function(){return''};
{const o=coTabs;coTabs=function(){const L=o.apply(this,arguments);if(S&&S.unb)return L;const i=L.findIndex(x=>x[0]==='holdings');L.splice(i<0?L.length:i+1,0,['brand','Brand']);return L}}
{const o=coClick;coClick=function(act,arg){if(act==='brcat'){brCat=arg;brPick=null;renderCompany();return}if(act==='brpick'){brPick=arg;renderCompany();return}return o.apply(this,arguments)}}
{const o=renderCompany;renderCompany=function(){const a=document.activeElement,keep=a&&a.id==='brName'?{v:a.value,s:a.selectionStart,e:a.selectionEnd}:null;const r=o.apply(this,arguments);
  try{if(coTab==='brand'&&S&&!S.unb&&S.player&&!$('company').hidden){$('coBody').innerHTML=brScreenHtml(S.player);if(keep){const b=$('brName');if(b){b.value=keep.v;b.focus();try{b.setSelectionRange(keep.s,keep.e)}catch(e){}}}}}catch(e){console.error(e)}return r}}
