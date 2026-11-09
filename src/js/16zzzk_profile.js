//@src 16zzzk_profile.js
// ============================================================ Beyond: your company profile (user, 8 Nov 2026)
// "When a player is going to buy a depot or station kit they have to first fill out their faction screen. Name of faction.
// Choose a logo. Choose a depot / station design from a list of six possible pre-created designs. Asteroid bases are one of
// the choices. Deposit $100k into their faction's treasury to buy initial stock, pay for jobs etc. Set fee rates. Choose a
// color hue." Answers: the profile comes "before you can build a depot or station in any way"; the treasury pays for all
// base business; the designs are looks only; it is the company's profile (declaring stays separate); a hue slider.
//   Company → Profile: name, logo (twelve marks of the players' own), base design (six, looks only), colour (a hue slider, kept
//   25° from the powers', the Brood's, the Unbound's and the Compact's hues), default fees for new bases (with Apply to all),
//   and the treasury: opened with a 100,000 cr deposit, then Deposit / Withdraw by hand.
//   Gate: building a Depot or Station any way (from frames, a kit, a Lair, a Depot) and buying a Depot or Station Kit need a
//   saved profile with its treasury open.
//   Treasury: the wallet co_<pilot>. While the base business runs (your markets' trades and fees, crews' hire and wages, crew
//   runs, posted jobs and their runs, capital ships built), each profiled pilot's credits are swapped with their treasury, so
//   everything that business pays or earns comes out of, or goes into, the treasury (the ledger is unchanged: both are
//   counted credits).
// The name and colour live in the brand record (S.brands), as before; the rest in P.co.
const COP={deposit:100000,gap:25,sat:.72,lit:.58,logos:12};
const CO_DESIGN_FALLBACK=['Company standard','Wheel','Spire','Cluster','Disc','Asteroid'];
function coReady(P){return!!(P&&P.co&&P.co.ok)}
function coWal(P){return P&&P.co&&P.co.w}
// a profile made by coDefault (a Legend start, the dev tools, tests) has no treasury yet: its business runs on the pilot's own
// credits until the treasury is opened from the Profile tab
function coFunded(P){return!!(P&&P.co&&P.co.ok&&P.co.fund)}
function coNeedTxt(){return'Set up your company first: Company → Profile (name, logo, base design, colour, fees and a 100,000 cr treasury).'}
function coDesigns(){try{if(typeof BM_DESIGNS!=='undefined'&&BM_DESIGNS.length)return BM_DESIGNS.map(d=>d.name)}catch(e){}return CO_DESIGN_FALLBACK}
function coLogoCount(){try{if(typeof CO_LOGO!=='undefined'&&CO_LOGO.length)return CO_LOGO.length}catch(e){}return COP.logos}
function coLogoHtml(i,size,col){try{if(typeof coLogoSvg==='function')return coLogoSvg(i,size,col)}catch(e){}return`<span style="display:inline-flex;width:${size}px;height:${size}px;border:1px solid ${col};border-radius:50%;align-items:center;justify-content:center;font-size:${Math.round(size*.45)}px;color:${col}">${i+1}</span>`}
// ---- colour: hue helpers and the hues kept clear
function hslHex(h,s,l){const f=n=>{const k=(n+h/30)%12,a=s*Math.min(l,1-l),c=l-a*Math.max(-1,Math.min(k-3,9-k,1));return Math.round(c*255).toString(16).padStart(2,'0')};return'#'+f(0)+f(8)+f(4)}
function hexHue(hex){const[r,g,b]=hexRGB(hex),mx=Math.max(r,g,b),mn=Math.min(r,g,b),d=mx-mn;if(d<1e-6)return null;let h=mx===r?((g-b)/d)%6:mx===g?(b-r)/d+2:(r-g)/d+4;h*=60;return h<0?h+360:h}
function coTaken(){const L=[];const add=(n,c)=>{const h=c&&hexHue(c);if(h!=null)L.push({n,h})};for(const f of FAC_IDS)add(FACTIONS[f].short,FACTIONS[f].col);
  for(const[s,n]of[['brood','the Brood'],['pirate','the Unbound'],['neutral','the Compact']])try{add(n,sideCol(s))}catch(e){}return L}
function coHueClash(h){for(const x of coTaken()){const d=Math.abs(((h-x.h)%360+540)%360-180);if(d<COP.gap)return x.n}return null}
function coHueCol(h){return hslHex(((+h%360)+360)%360,COP.sat,COP.lit)}
// ---- the profile itself (a dock action: a guest's runs on the host)
function coDefault(P){if(!P||P.co)return P&&P.co;const k=pkeyOf(P);P.co={ok:1,w:'co_'+k,logo:0,design:1,fees:{},T:S.T};try{const N=brSlot(P,true);if(N!=null&&!S.brands[N].col){let h=40;while(coHueClash(h)&&h<400)h+=17;S.brands[N].col=coHueCol(h%360)}}catch(e){}return P.co}
function coSave(P,arg){const q={};for(const kv of String(arg||'').split(';')){const i=kv.indexOf('=');if(i>0)q[kv.slice(0,i)]=decodeURIComponent(kv.slice(i+1))}
  const name=String(q.name||'').trim().slice(0,32),logo=Math.floor(+q.logo),design=Math.floor(+q.design),hue=Math.round(+q.hue);
  if(name.length<2)return'Give your company a name.';if(!(logo>=0&&logo<coLogoCount()))return'Pick a logo.';if(!(design>=1&&design<=6))return'Pick a base design.';if(!(hue>=0&&hue<360))return'Pick a colour.';
  const clash=coHueClash(hue);const N=brSlot(P,true);if(N==null)return'No company slot free in this galaxy.';const B=S.brands[N],col=coHueCol(hue);
  if(P.decl&&B.col&&B.col!==col)return'Your colour is fixed now that you have declared a faction.';if(clash&&B.col!==col)return`That colour is too close to ${clash}'s. Pick another hue.`;
  const fees={};for(const k of['sell','buy','svc','dock']){const D=FEE[k];if(q[k]==null||q[k]==='')continue;const v=clamp(+q[k],D.min,D.max);if(isFinite(v))fees[k]=k==='dock'?Math.round(v):Math.round(v*100)/100}
  let first=false;if(!coFunded(P)){if(P.credits<COP.deposit)return`Opening your company's treasury takes a ${fmt(COP.deposit)} cr deposit. You have ${fmt(P.credits)} cr.`;first=true}
  const k=pkeyOf(P);P.co=Object.assign(P.co||{},{ok:1,fund:1,w:(P.co&&P.co.w)||'co_'+k,logo,design,fees,T:(P.co&&P.co.T)||S.T});if(first)transfer('player',P.co.w,COP.deposit);
  if(!P.decl)B.name=name;B.col=col;for(const R of myDepots(P))R.design=design;try{for(const key of Object.keys(MESH))if(key.startsWith('bm'))delete MESH[key]}catch(e){}
  return first?`✓ ${name} is set up. Its treasury opens with ${fmt(COP.deposit)} cr: your bases' business runs through it now.`:`✓ ${name}'s profile is saved.`}
function coTreas(P,arg){if(!coFunded(P))return coNeedTxt();const[d,n0]=String(arg).split(':'),w=P.co.w;const n=n0==='all'?(d==='in'?P.credits:S.econ.treasury[w]||0):Math.floor(+n0);if(!(n>0))return'Nothing to move.';
  const got=d==='in'?transfer('player',w,n):transfer(w,'player',n);return got?`✓ ${d==='in'?'Deposited':'Withdrew'} ${fmt(got)} cr. The treasury holds ${fmt(S.econ.treasury[w]||0)} cr.`:d==='in'?'Not enough credits.':'The treasury is empty.'}
function coFeesAll(P){if(!coReady(P))return coNeedTxt();const L=myDepots(P);for(const R of L)R.fees={...(P.co.fees||{})};return`✓ Your default fees now apply at ${L.length} base${L.length===1?'':'s'}.`}
{const o=dockAction;dockAction=function(act,arg){if(act==='coprof'){dockErr=coSave(S.player,arg);return}if(act==='cotr'){dockErr=coTreas(S.player,arg);return}if(act==='cofeeall'){dockErr=coFeesAll(S.player);return}return o.apply(this,arguments)}}
for(const a of['coprof','cotr','cofeeall'])CO_REMOTE.add(a);
// new bases take the profile's design and fees; a base made some other way (a Legend start, the dev tools) brings a profile
{const o=depMake;depMake=function(P){const R=o.apply(this,arguments);try{if(P&&!P.co)coDefault(P);if(P&&P.co){R.design=P.co.design||1;if(P.co.fees&&Object.keys(P.co.fees).length)R.fees={...P.co.fees}}}catch(e){console.error(e)}return R}}
if(typeof bmDesignOf==='function'){const o=bmDesignOf;bmDesignOf=function(R){if(R&&R.design)return R.design;return o.apply(this,arguments)}}
// ---- the gate: no Depot or Station any way without a profile
{const o=depFresh;depFresh=function(P){if(!coReady(P))return coNeedTxt();return o.apply(this,arguments)}}
{const o=depFromLair;depFromLair=function(P){if(!coReady(P))return coNeedTxt();return o.apply(this,arguments)}}
{const o=staUp;staUp=function(P){if(!coReady(P))return coNeedTxt();return o.apply(this,arguments)}}
{const o=startPlayerBuild;startPlayerBuild=function(){if(S&&S.player&&!NET.cl&&!coReady(S.player)){flash(coNeedTxt(),true);return}return o.apply(this,arguments)}}
{const o=dockAction;dockAction=function(act,arg){if(act==='buy'&&!NET.cl){const k=String(arg).split(':')[0];if((k==='kit_depot'||k==='kit_station')&&!coReady(S.player)){coTab='profile';dockErr=`A ${ITEMS[k].name} is sold to companies only. ${coNeedTxt()}`;return}}return o.apply(this,arguments)}}
// ---- the treasury runs the base business: swap each profiled pilot's credits with their treasury while it runs
let CO_SW=0;
function coRun(fn){if(CO_SW||!S)return fn();const L=[];for(const P of allPilots()){if(!coFunded(P))continue;L.push([P,P.credits]);P.credits=S.econ.treasury[P.co.w]||0}CO_SW=1;
  try{return fn()}finally{CO_SW=0;for(const[P,c]of L){S.econ.treasury[P.co.w]=P.credits;P.credits=c}}}
{const o=depTradeTick;depTradeTick=function(){const a=arguments,t=this;return coRun(()=>o.apply(t,a))}}
{const o=crewHire;crewHire=function(){const a=arguments,t=this;return coRun(()=>o.apply(t,a))}}
{const o=crewTick;crewTick=function(){const a=arguments,t=this;return coRun(()=>o.apply(t,a))}}
{const o=pjPost;pjPost=function(){const a=arguments,t=this;return coRun(()=>o.apply(t,a))}}
{const o=pjTick;pjTick=function(){const a=arguments,t=this;return coRun(()=>o.apply(t,a))}}
{const o=pjFinish;pjFinish=function(){const a=arguments,t=this;return coRun(()=>o.apply(t,a))}}
{const o=pjDo;pjDo=function(){const a=arguments,t=this;return coRun(()=>o.apply(t,a))}}
{const o=pjCancel;pjCancel=function(){const a=arguments,t=this;return coRun(()=>o.apply(t,a))}}
{const o=pjRunEnd;pjRunEnd=function(){const a=arguments,t=this;return coRun(()=>o.apply(t,a))}}
{const o=pjRunStart;pjRunStart=function(){const a=arguments,t=this;return coRun(()=>o.apply(t,a))}}
{const o=pjArrive;pjArrive=function(){const a=arguments,t=this;return coRun(()=>o.apply(t,a))}}
{const o=crewHaulStart;crewHaulStart=function(){const a=arguments,t=this;return coRun(()=>o.apply(t,a))}}
{const o=crSell;crSell=function(){const a=arguments,t=this;return coRun(()=>o.apply(t,a))}}
{const o=crArrive;crArrive=function(){const a=arguments,t=this;return coRun(()=>o.apply(t,a))}}
{const o=crRunsTick;crRunsTick=function(){const a=arguments,t=this;return coRun(()=>o.apply(t,a))}}
{const o=capBuild;capBuild=function(){const a=arguments,t=this;return coRun(()=>o.apply(t,a))}}
// ---- the Profile tab
let coForm=null;
function coFormOf(P){if(coForm)return coForm;const N=brSlot(P),B=N!=null&&S.brands?S.brands[N]:null,col=B&&B.col;let hue=col?Math.round(hexHue(col)||40):40;if(!col)while(coHueClash(hue)&&hue<400)hue+=17;
  const f={...feeOfDef(),...((P.co&&P.co.fees)||{})};return coForm={name:(B&&B.name)||`${P.name||'Pilot'}'s Works`,logo:P.co?P.co.logo:0,design:P.co?P.co.design:1,hue:hue%360,fees:f}}
function feeOfDef(){const o={};for(const k of['sell','buy','svc','dock'])o[k]=FEE[k].def;return o}
function coArg(F){return[`name=${encodeURIComponent(F.name)}`,`logo=${F.logo}`,`design=${F.design}`,`hue=${F.hue}`,...['sell','buy','svc','dock'].map(k=>`${k}=${F.fees[k]}`)].join(';')}
function coProfHtml(P){const F=coFormOf(P),col=coHueCol(F.hue),clash=coHueClash(F.hue),ready=coFunded(P),w=ready?P.co.w:null,D=coDesigns();
  let h=`<p class="note" style="margin:0 0 12px">${ready?'Your company. Change anything here and Save; the deposit is paid once.':`Before you build a Depot or a Station, or buy their kits, set up your company. Saving opens its treasury with a ${fmt(COP.deposit)} cr deposit from your credits; your bases' business runs through it from then on.`}</p>`;
  h+=`<div class="lab">Name</div><input id="coNm" type="text" maxlength="32" value="${esc(F.name)}" ${P.decl?'disabled':''} style="width:min(360px,100%);margin:4px 0 12px" aria-label="Company name">`;
  h+=`<div class="lab">Logo</div><div style="display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 12px">${Array.from({length:coLogoCount()},(_,i)=>`<button class="btn sm" type="button" data-co="cof" data-arg="logo:${i}" aria-pressed="${F.logo===i}" style="padding:4px;border-color:${F.logo===i?col:'var(--line)'}">${coLogoHtml(i,30,F.logo===i?col:'#9aa4b8')}</button>`).join('')}</div>`;
  h+=`<div class="lab">Base design <span class="note" style="margin:0">(looks only)</span></div><div style="display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 12px">${D.map((n,i)=>`<button class="btn sm" type="button" data-co="cof" data-arg="design:${i+1}" aria-pressed="${F.design===i+1}" style="border-color:${F.design===i+1?col:'var(--line)'}">${esc(n)}</button>`).join('')}</div>`;
  h+=`<div class="lab">Colour</div><div style="display:flex;gap:10px;align-items:center;margin:6px 0 4px"><span style="display:inline-block;width:28px;height:28px;border-radius:6px;background:${col}"></span><input id="coHue" type="range" min="0" max="359" value="${F.hue}" ${P.decl?'disabled':''} aria-label="Company colour hue" style="width:min(300px,60vw);accent-color:${col}"></div>`;
  h+=`<div class="note" style="margin:0 0 12px;${clash?'color:var(--amber)':''}">${clash?`Too close to ${esc(clash)}'s colour: move the slider.`:P.decl?'Fixed now that you have declared a faction.':'Kept clear of the powers\', the Brood\'s, the Unbound\'s and the Compact\'s colours.'}</div>`;
  h+=`<div class="lab">Fees at new bases</div><div style="margin:6px 0 4px">${['sell','buy','svc','dock'].map(k=>{const Dd=FEE[k];return`<div style="display:flex;gap:8px;align-items:center;margin:3px 0"><span style="width:130px">${esc(Dd.name)}</span><button class="btn sm" type="button" data-co="cof" data-arg="fee:${k}:-1">−</button><b class="mono" style="min-width:56px;text-align:center">${esc(feeFmt(k,F.fees[k]))}</b><button class="btn sm" type="button" data-co="cof" data-arg="fee:${k}:1">+</button></div>`}).join('')}</div>`;
  if(ready)h+=`<button class="btn sm" type="button" data-co="cofeeall" style="margin:2px 0 12px">Apply to all my bases</button>`;
  h+=`<div class="act" style="margin:10px 0 16px"><button class="btn pri" type="button" data-co="cosave" ${clash&&!P.decl?'disabled':''}>${ready?'Save':`Save and open the treasury · ${fmt(COP.deposit)} cr`}</button></div>`;
  if(ready){const t=S.econ.treasury[w]||0;h+=`<div class="h3">Treasury · <span class="mono">${fmt(t)} cr</span></div><p class="note" style="margin:0 0 6px">Wages, posted jobs, your markets' buys and capital ships come out of it; fees and your markets' sales go into it.</p>
    <div class="act">${[10000,50000].map(n=>`<button class="btn sm" type="button" data-co="cotr" data-arg="in:${n}" ${P.credits<n?'disabled':''}>Deposit ${fmt(n)}</button>`).join('')}${[10000,50000].map(n=>`<button class="btn sm" type="button" data-co="cotr" data-arg="out:${n}" ${t<n?'disabled':''}>Withdraw ${fmt(n)}</button>`).join('')}<button class="btn sm" type="button" data-co="cotr" data-arg="out:all" ${t<1?'disabled':''}>Withdraw all</button></div>`}
  return h}
{const o=coTabs;coTabs=function(){const L=o.apply(this,arguments);return S&&S.unb?L:[['profile','Profile'],...L]}}
{const o=renderCompany;renderCompany=function(){const r=o.apply(this,arguments);try{if(coTab==='profile'&&S&&!S.unb){$('coBody').innerHTML=coProfHtml(S.player);const P=S.player;
    const nm=$('coNm');if(nm)nm.addEventListener('input',e=>{coFormOf(P).name=e.target.value});const hu=$('coHue');if(hu){hu.addEventListener('change',e=>{coFormOf(P).hue=+e.target.value;renderCompany()});hu.addEventListener('input',e=>{const sw=hu.previousElementSibling;if(sw)sw.style.background=coHueCol(+e.target.value)})}}
  if(S&&S.player&&coFunded(S.player)){const t=S.econ.treasury[S.player.co.w]||0,sub=$('coSub');if(sub&&!/treasury/.test(sub.textContent))sub.textContent+=` · treasury ${fmt(t)} cr`}}catch(e){console.error(e)}return r}}
{const o=coClick;coClick=function(act,arg){const P=S.player;
  if(act==='cof'){const F=coFormOf(P),[k,v,d]=String(arg).split(':');if(k==='logo')F.logo=+v;else if(k==='design')F.design=+v;else if(k==='fee'){const D=FEE[v];F.fees[v]=Math.round(clamp(F.fees[v]+(+d)*D.step,D.min,D.max)/D.step)*D.step;if(v!=='dock')F.fees[v]=Math.round(F.fees[v]*100)/100}renderCompany();return}
  if(act==='cosave'||act==='cotr'||act==='cofeeall'){const a=act==='cosave'?'coprof':act,g=act==='cosave'?coArg(coFormOf(P)):arg;if(NET.cl){netSend({t:'act',act:a,arg:g});coErr='Working…';renderCompany();return}dockAction(a,g);coErr=dockErr;if(a==='coprof'&&dockErr.startsWith('✓'))coForm=null;renderCompany();return}
  return o.apply(this,arguments)}}
