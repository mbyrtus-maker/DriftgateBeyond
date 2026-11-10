//@src 16zt_fees.js
// ============================================================ your base's fees (Beyond, agreed 3 Nov 2026)
// At a Depot or Station you own you set three fees, each between a minimum and a maximum (reworked 9 Nov 2026, the user: "should
// be a per transaction fee, services fee (credits not percentage) and docking fee (default 0)"; it used to be a sell price %,
// a buy offer % and a services %):
//   Transaction fee (0–20%, default 5%): a cut of every trade at your market. Traders buying from you pay it on top of the price;
//     traders selling to you have it taken off what you pay them. Each visit's lot shrinks 30% per 10 points above the default
//     (grows below it, up to 1.4 times).
//   Services fee (0–500 cr, default 100 cr): what a visiting pilot pays for repairs and rearming. Visiting pilots (Compact
//     contractors and the pilots of the powers that deal with you) stop about six an hour at the default (a Station half as
//     many again); 8% fewer per 10 cr above the default (a fifth at 500 cr), 8% more below it (1.4 times at 0).
//   Docking fee (0–100 cr, default 0): paid by every trader and visiting pilot who docks; traders come 7% less often per 10 cr
//     (100 cr: under a third as often), and takers for the jobs you post there wait longer (twice as long at 100 cr).
// They change traffic only, never standing. Only credits move (treasuries to you), so the ledger stays exact. Fees saved under
// the old scheme are converted once (the transaction fee at its default, the services % times 100 cr). Shown in Holdings
// (Fees), Economy, the map panel and the company profile (the defaults for new bases).
const FEE={tx:{min:0,max:.2,step:.01,def:.05,name:'Transaction fee'},svc:{min:0,max:500,step:10,def:100,name:'Services fee'},dock:{min:0,max:100,step:5,def:0,name:'Docking fee'},
  k:3,svcK:.8,visit:.1,skip:.35};
const FEE_KEYS=['tx','svc','dock'];
// fees saved under the old scheme (sell %, buy %, services %): converted once
function feeMig(f){if(!f||typeof f!=='object')return f;if('sell'in f||'buy'in f||(typeof f.svc==='number'&&f.svc>0&&f.svc<=2)){if(typeof f.svc==='number'&&f.svc>0&&f.svc<=2)f.svc=Math.round(f.svc*10)*10;delete f.sell;delete f.buy}return f}
function feeOf(R){const f=feeMig(R&&R.fees)||{};const o={};for(const k of FEE_KEYS)o[k]=typeof f[k]==='number'?f[k]:FEE[k].def;return o}
function feeTd(F){return Math.max(0,1-F.dock/140)}
function feeTs(F){return clamp(1-FEE.k*(F.tx-FEE.tx.def),.2,1.4)}
function feeTb(F){return feeTs(F)}
function feeTv(F){return clamp(1-FEE.svcK*(F.svc-FEE.svc.def)/100,.2,1.4)}
function feeReps(R){return typeof hasB==='function'&&hasB(R,'market')?2:1}
function feeVisitP(R,F){return FEE.visit*(R.pst?1.5:1)*feeTv(F)*feeTd(F)}
function feeFmt(k,v){return k==='tx'?`${Math.round(v*100)}%`:`${fmt(v)} cr`}
// ---- traders, with your prices and docking fee
depTradeTick=function(){for(const R of Object.values(S.stations||{})){if(!R||R.owner!=='player'||R.kind!=='depot'||!R.sell)continue;const O=lairOwner({pid:R.pid||'me'})||S.player,fs=depTraders(O),reps=feeReps(R),F=feeOf(R),
    lot=DEP.lot*(typeof hasB==='function'&&hasB(R,'storage')?2:1),mg=(R.mg||1)*(reps>1?1.1:1);if(!fs.length)continue;
  for(let rep=0;rep<reps;rep++){if(Math.random()>(1-FEE.skip)*feeTd(F))continue;const f=pick(fs),st=R.stock,fst=S.econ.stock[f]=S.econ.stock[f]||{};
    if(F.dock>0){const got=payTo(O,f,Math.min(F.dock,S.econ.treasury[f]||0));if(got)eco(R,'docking',got,`${FACTIONS[f].short} trader docked`)}
    const ls=Math.max(1,Math.round(lot*feeTs(F))),lb=Math.max(1,Math.round(lot*feeTb(F)));
    for(const k in R.sell){const n=Math.min(ls,(st[k]||0)-(R.sell[k]||0));if(n<=0)continue;const pr=Math.max(1,Math.round(price(st,k)*mg*(1+F.tx)));const pay=Math.min(n*pr,S.econ.treasury[f]||0);const m=Math.floor(pay/pr);if(m<=0)continue;inv.take(st,k,m);inv.add(fst,k,m);const got=payTo(O,f,m*pr);eco(R,'market',got,`${FACTIONS[f].short} traders bought ${m} ${ITEMS[k].name}`)}
    for(const k in R.buy){const n=Math.min(lb,(R.buy[k]||0)-(st[k]||0),fst[k]||0);if(n<=0)continue;const pr=Math.max(1,Math.round(price(fst,k)*(1-F.tx)));const m=Math.min(n,Math.floor(O.credits/pr));if(m<=0)continue;inv.take(fst,k,m);inv.add(st,k,m);payFrom(O,f,m*pr);eco(R,'market',-m*pr,`bought ${m} ${ITEMS[k].name} from ${FACTIONS[f].short} traders`)}}
  // visiting pilots: repairs and rearming
  if(Math.random()<feeVisitP(R,F)){const by=Math.random()<.5||!fs.length?'neutral':pick(fs),want=Math.round(F.svc)+F.dock,got=payTo(O,by,Math.min(want,S.econ.treasury[by]||0));
    if(got)eco(R,'services',got,`${by==='neutral'?'a Compact contractor':`${/^[AEIOU]/.test(FACTIONS[by].short)?'an':'a'} ${FACTIONS[by].short} pilot`} repaired and rearmed`)}}};
// ---- posted jobs: the docking fee makes takers slower to come
{const o=pjPost;pjPost=function(P,arg){const n0=pjList().length,r=o.apply(this,arguments);try{if(pjList().length>n0){const j=pjList()[pjList().length-1],F=feeOf(S.stations[j.sid]);if(F.dock>0)j.claimAt=j.posted+(j.claimAt-j.posted)*(1+F.dock/100)}}catch(e){}return r}}
// ---- setting them
function feeSet(P,arg){const[sid,k,d]=String(arg).split(':'),R=S.stations[sid];if(!R||R.owner!=='player'||(R.pid||'me')!==pkeyOf(P))return'Not your base.';
  if(k==='reset'){R.fees={};return`✓ ${R.name}'s fees are back at the galaxy defaults.`}const D=FEE[k];if(!D||!D.step||!FEE_KEYS.includes(k))return'';const F=feeOf(R);
  const v=Math.round(clamp(F[k]+(+d||0)*D.step,D.min,D.max)/D.step)*D.step;R.fees=R.fees||{};R.fees[k]=k==='tx'?Math.round(v*100)/100:Math.round(v);return`✓ ${R.name}: ${D.name.toLowerCase()} ${feeFmt(k,R.fees[k])}.`}
{const o=dockAction;dockAction=function(act,arg){if(act==='feeset'){dockErr=feeSet(S.player,arg);return}return o.apply(this,arguments)}}
{const o=coClick;coClick=function(act,arg){if(act==='feeset'){if(NET.cl){netSend({t:'act',act,arg});coErr='Working…';renderCompany();return}dockAction(act,arg);coErr=dockErr;renderCompany();return}return o.apply(this,arguments)}}
// ---- shown: Holdings detail (Fees), the map panel
function feeHtml(R){const F=feeOf(R),reps=feeReps(R),tv=Math.round(60*reps*(1-FEE.skip)*feeTd(F)),tv0=Math.round(60*reps*(1-FEE.skip)),pv=Math.round(60*feeVisitP(R,F)),pv0=Math.round(60*feeVisitP(R,feeOf(null)));
  const row=k=>{const D=FEE[k],v=F[k];return`<div class="coln"><span style="flex:1">${D.name} <span class="mass">${feeFmt(k,D.min)}–${feeFmt(k,D.max)} · default ${feeFmt(k,D.def)}</span></span><span class="cotri"><button type="button" data-co="feeset" data-arg="${R.sid}:${k}:-1" ${v<=D.min+1e-9?'disabled':''} aria-label="Lower">−</button><button type="button" class="on" style="min-width:64px;justify-content:center;cursor:default" tabindex="-1">${feeFmt(k,v)}</button><button type="button" data-co="feeset" data-arg="${R.sid}:${k}:1" ${v>=D.max-1e-9?'disabled':''} aria-label="Raise">+</button></span></div>`};
  const lotS=feeTs(F),lotB=feeTb(F),dflt=FEE_KEYS.every(k=>Math.abs(F[k]-FEE[k].def)<1e-9);
  return`<div class="lab" style="margin-top:14px">Fees</div>${FEE_KEYS.map(row).join('')}
    <div class="note" style="margin:8px 0 0">Traders: about ${tv} visits an hour${tv!==tv0?` (${tv0} at the defaults)`:''}, buying ${lotS<.99||lotS>1.01?`${lotS>1?'bigger':'smaller'} lots (×${lotS.toFixed(2)})`:'normal lots'} and selling you ${lotB<.99||lotB>1.01?`${lotB>1?'bigger':'smaller'} lots (×${lotB.toFixed(2)})`:'normal lots'}. Visiting pilots: about ${pv} an hour${pv!==pv0?` (${pv0} at the defaults)`:''}.</div>
    ${dflt?'':`<div class="act" style="justify-content:flex-start;margin-top:6px"><button class="btn sm" type="button" data-co="feeset" data-arg="${R.sid}:reset">Back to the defaults</button></div>`}`}
{const o=coDetail;coDetail=function(P,b){let h=o.apply(this,arguments);try{if(b&&b.R)h=h.replace(/<div class="act" style="margin-top:16px"><button class="btn sm" type="button" data-co="tab" data-arg="economy">/,m=>feeHtml(b.R)+m)}catch(e){console.error(e)}return h}}
function feeLine(R){const F=feeOf(R);return`Fees: transaction ${feeFmt('tx',F.tx)} · services ${feeFmt('svc',F.svc)} · docking ${feeFmt('dock',F.dock)}`}
{const o=mpHtml;mpHtml=function(sid){let h=o.apply(this,arguments);try{const R=S.stations[sid];if(R&&R.owner==='player'&&R.fees)h=h.replace('<div class="mpslot-course"></div>',`<div class="note" style="margin:-4px 0 10px">${esc(feeLine(R))}</div><div class="mpslot-course"></div>`)}catch(e){}return h}}
