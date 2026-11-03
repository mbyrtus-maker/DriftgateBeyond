//@src 16zg_brand.js
// ============================================================ your own brand, from Depot level (Beyond section 3, 3 Nov 2026)
// You name your company when you have a Depot, and shape its trait with points: for each kind of part, each strength you
// buy costs points and each weakness you take pays them back, netting to zero, so a brand is a shape, not a free gain.
// Parts built at your Depot's or Station's workshop carry the company's name and that trait, and sell on your market like
// any maker's (a Lair's workshop still builds standard parts). The first shape is free; reshaping costs 1,500 cr (to the
// Compact) and reshapes every part of your brand, fitted or stored.
// Items: four fixed brand slots (one per pilot of a galaxy), bp<N>_<kind>, with the standard part's recipe, so the ledger
// is untouched; the name and the trait are read live from S.brands[N].
const BR={slots:4,range:3,respec:1500,
  step:{gun:{dmg:[.04,1,1],ammo:[.08,1,1],speed:[.01,1,1]},laser:{dmg:[.04,1,1],e:[.05,-1,1],speed:[.01,1,1]},missile:{mag:[1,1,2],lock:[.05,-1,1]},torpedo:{mag:[1,1,2],lock:[.05,-1,1]},
    charge:{mag:[1,1,2],speed:[.01,1,1]},mlaser:{ml:[.05,1,1],e:[.05,-1,1]},cargo:{cargo:[.03,1,1],speed:[.01,1,1]},scanner:{scan:[.1,1,1],speed:[.01,1,1]}}};
const BR_KINDS=Object.keys(BR.step);
function brOf(N){return S&&S.brands&&S.brands[N]||null}
function brTr(N,k){const B=brOf(N),g=B&&B.pts&&B.pts[k],St=BR.step[k],out={};if(!g||!St)return out;for(const t in g){const s=St[t];if(!s||!g[t])continue;out[t]=Math.round(g[t]*s[0]*s[1]*1000)/1000}return out}
function brName(N){const B=brOf(N);return B&&B.name||'Company'}
for(let N=0;N<BR.slots;N++)for(const k of BR_KINDS){const id=`bp${N}_${k}`,base=(WPN[k]||UTIL[k]).name;
  ITEMS[id]={recipe:{...PART_RC[k]},col:PART_COL[k],part:k,brand:N,get name(){return`${brName(N)} ${base.replace(/^./,x=>x.toLowerCase())}`},get tr(){return brTr(N,k)},get trTxt(){const t=trText(brTr(N,k));return t?`${brName(N)} (your brand): ${t}.`:`${brName(N)}: standard.`}};
  ITEM_ORDER.push(id);(MK_ITEMS[k]=MK_ITEMS[k]||[]).push(id)}
// a pilot's brand slot (given with the first depot)
function brSlot(P,make){const k=pkeyOf(P);S.brandOf=S.brandOf||{};if(S.brandOf[k]!=null)return S.brandOf[k];if(!make)return null;const used=new Set(Object.values(S.brandOf));for(let N=0;N<BR.slots;N++)if(!used.has(N)){S.brandOf[k]=N;S.brands=S.brands||{};S.brands[N]={name:`${P.name||'Pilot'}'s Works`,pts:{},set:0};return N}return null}
function brCost(pts){let c=0;for(const k in pts)for(const t in pts[k]){const s=BR.step[k]&&BR.step[k][t];if(s)c+=pts[k][t]*s[2]}return c}
function brBudget(N){const B=brOf(N);return(B&&B.bonus)||0}
// shaping: arg is "name|kind:trait=steps,trait=steps;kind:…" (the name URI-encoded)
function brSave(P,arg){if(!myDepots(P).length)return'Your brand begins with your first Depot.';const N=brSlot(P,true);if(N==null)return'No brand slot free in this galaxy.';const B=brOf(N);
  const[nmE,spec]=String(arg).split('|'),name=decodeURIComponent(nmE||'').replace(/[<>]/g,'').trim().slice(0,24)||B.name,pts={};
  for(const part of String(spec||'').split(';')){if(!part)continue;const[k,rest]=part.split(':');if(!BR.step[k])continue;for(const kv of String(rest||'').split(',')){const[t,v]=kv.split('=');const n=Math.round(+v||0);if(!BR.step[k][t]||!n)continue;(pts[k]=pts[k]||{})[t]=clamp(n,-BR.range,BR.range)}}
  for(const k in pts){if(brCost({[k]:pts[k]})>brBudget(N))return`${(WPN[k]||UTIL[k]).name}: the strengths cost more points than the weaknesses pay back.`}
  const same=JSON.stringify(pts)===JSON.stringify(B.pts||{});if(!same&&B.set){if(P.credits<BR.respec)return`Reshaping your brand costs ${fmt(BR.respec)} cr.`;payFrom(P,'neutral',BR.respec)}
  B.name=name;if(!same){B.pts=pts;B.set=(B.set||0)+1}return`✓ ${name}${same?' renamed':`${/s$/i.test(name)?"'":"'s"} brand ${B.set>1?'reshaped':'set'}`}.`}
// built at your own Depot's or Station's workshop: your brand
{const o=dockAction;dockAction=function(act,arg){if(act==='brsave'){dockErr=brSave(S.player,arg);return}
  if(act==='make'&&!S.unb){const P=S.player,R=P.docked==='station'&&S.stations[P.sector],k=String(arg).split(':')[0],I=ITEMS[k];
    if(R&&R.owner==='player'&&(R.pid||'me')===pkeyOf(P)&&I&&I.part&&k===PART[I.part]&&BR.step[I.part]){const N=brSlot(P,true),st=R.stock,n0=st[k]||0;const r=o.apply(this,arguments);const made=(st[k]||0)-n0;
      if(N!=null&&made>0){inv.take(st,k,made);inv.add(st,`bp${N}_${I.part}`,made);dockErr=`✓ Built ${made} ${ITEMS[`bp${N}_${I.part}`].name}.`}return r}}
  return o.apply(this,arguments)}}
{const o=coClick;coClick=function(act,arg){if(act==='brstep'){const[k,t,d]=String(arg).split(':');brDraftGet();const g=(brDraft.pts[k]=brDraft.pts[k]||{});g[t]=clamp((g[t]||0)+(+d),-BR.range,BR.range);renderCompany();return}
  if(act==='brsave'){const nm=(document.getElementById('brName')||{}).value||'';brDraftGet();const spec=Object.keys(brDraft.pts).map(k=>`${k}:${Object.keys(brDraft.pts[k]).filter(t=>brDraft.pts[k][t]).map(t=>`${t}=${brDraft.pts[k][t]}`).join(',')}`).join(';');const a=`${encodeURIComponent(nm)}|${spec}`;
    if(NET.cl){netSend({t:'act',act,arg:a});coErr='Working…';renderCompany();return}dockAction(act,a);coErr=dockErr;brDraft=null;renderCompany();return}
  if(act==='brreset'){brDraft=null;renderCompany();return}return o.apply(this,arguments)}}
let brDraft=null;
function brDraftGet(){if(!brDraft){const N=brSlot(S.player),B=N!=null&&brOf(N);brDraft={pts:JSON.parse(JSON.stringify((B&&B.pts)||{}))}}return brDraft}
// ---- the Holdings tab: your brand
{const o=holdingsHtml;holdingsHtml=function(P){let h=o.apply(this,arguments);try{h+=brHtml(P)}catch(err){console.error(err)}return h}}
function brHtml(P){let h=`<div class="h3" style="margin-top:16px">Your brand</div>`;if(!myDepots(P).length)return h+`<p class="note" style="margin:0">Your brand begins with your first Depot: parts built at its workshop carry your company's name and trait.</p>`;
  const N=brSlot(P),B=N!=null?brOf(N):null,D=brDraftGet(),bud=N!=null?brBudget(N):0;
  h+=`<p class="note" style="margin:0 0 8px">Parts built at your Depot's or Station's workshop carry your company's name and its trait, and sell on your market like any maker's. For each kind of part, every strength costs points and every weakness pays them back: the points must net to zero${bud?` (your brand has ${bud} extra)`:''}. The first shape is free; reshaping costs ${fmt(BR.respec)} cr and reshapes every part of your brand.</p>`;
  h+=`<div style="display:flex;gap:8px;align-items:center;margin-bottom:8px"><span class="note" style="margin:0">Company name</span><input id="brName" maxlength="24" value="${esc((B&&B.name)||`${P.name||'Pilot'}'s Works`)}" style="background:var(--bg2,#111);color:inherit;border:1px solid var(--line);padding:4px 8px;font:inherit"></div>`;
  h+=`<div class="tblw"><table class="t"><thead><tr><th>Part</th><th>Trait</th><th class="r">Points</th></tr></thead><tbody>`;
  for(const k of BR_KINDS){const g=D.pts[k]||{},c=brCost({[k]:g}),St=BR.step[k];
    h+=`<tr><td class="iname">${esc((WPN[k]||UTIL[k]).name)}</td><td style="white-space:normal">${Object.keys(St).map(t=>{const v=g[t]||0,eff=v*St[t][0]*St[t][1];const lab=t==='mag'?`${eff>0?'+':''}${eff} ${TR_TXT[t]}`:`${eff>0?'+':eff<0?'−':'±'}${Math.round(Math.abs(eff)*100)}% ${TR_TXT[t]}`;
      return`<span style="display:inline-flex;gap:3px;align-items:center;margin-right:10px"><button class="btn sm" type="button" data-co="brstep" data-arg="${k}:${t}:-1" ${v<=-BR.range?'disabled':''}>−</button><span style="min-width:120px;text-align:center;color:${v>0?'var(--ok,#7ad9a7)':v<0?'var(--danger)':'var(--dim)'}">${lab}</span><button class="btn sm" type="button" data-co="brstep" data-arg="${k}:${t}:1" ${v>=BR.range?'disabled':''}>+</button></span>`}).join('')}</td>
      <td class="r num" style="color:${c>bud?'var(--danger)':'inherit'}">${c>0?'+':''}${c}</td></tr>`}
  const bad=BR_KINDS.some(k=>brCost({[k]:D.pts[k]||{}})>bud),same=JSON.stringify(D.pts)===JSON.stringify((B&&B.pts)||{});
  h+=`</tbody></table></div><div class="act" style="margin-top:8px"><button class="btn pri" type="button" data-co="brsave" ${bad?'disabled':''}>${same?'Save name':B&&B.set?`Reshape · ${fmt(BR.respec)} cr`:'Set the brand'}</button><button class="btn" type="button" data-co="brreset">Undo changes</button>${bad?`<span class="note" style="color:var(--danger);margin:0">Some strengths aren't paid for by weaknesses.</span>`:''}</div>`;
  return h}
// the Company screen redraws every second: keep what's being typed in the name box
{const o=renderCompany;renderCompany=function(){const a=document.activeElement,keep=a&&a.id==='brName'?{v:a.value,s:a.selectionStart,e:a.selectionEnd}:null;const r=o.apply(this,arguments);
  if(keep){const b=document.getElementById('brName');if(b){b.value=keep.v;b.focus();try{b.setSelectionRange(keep.s,keep.e)}catch(e){}}}return r}}
