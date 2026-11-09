//@src 16zzz_corp.js
// ============================================================ Beyond: the corporate economy, stage 1 (7 Nov 2026)
// The makers get money of their own, buyers besides you, and lives: they earn, pay their way, tweak their products from
// their sales, answer to their boards, pay dividends, and fail and are replaced. Built from "Corporations with money" and
// "Corporate economy: last pass" in BEYOND_DESIGN.md (simulations v17 to v20). Grades through R&D, the R&D stations,
// meetings, bulk orders and corporate missions are the next stages.
//   - Money: each maker has a treasury (S.econ.treasury['corp_'+m], so the ledger counts it), capitalised at the start by its
//     home (its power, or the Compact for a freeport maker) with CE.start (8,000 cr since 8 Nov 2026, was 4,000: the game's makers carry more lines than
//     the simulations' 3,000 was set for). Credits only ever move between wallets.
//   - Income: every sale of its parts on any market, less the station's 15% dues (the station's owner keeps those).
//     A maker lists its parts at 1.5 times their component cost (the simulations' list price; Premium +15%, Discounter
//     -10%) or the market's price if higher, and never below 15% over cost after dues (the profit floor).
//   - Costs: its works pay the host station's owner for the components they take (at that market's price); running costs
//     each hour to the host's owner: 60 cr plus, for each line, half that line's fair margin (the margin every maker line of
//     its kind earned in the last hour, over the kind's lines), at least 10 cr a line (simulation v20). A line that hasn't
//     sold in 2 hours is shut: it pays nothing and isn't built, but its stock stays on sale. Penny-pincher x0.75.
//   - Prudent works (simulation v19): a line is built up to 1 more than it sold in the last hour (at most 4 on the shelf), and
//     only with an hour of running costs kept back (a Penny-pincher keeps 5, a Cautious CEO 6).
//   - Buyers besides you: the powers refit their fleets. Every 5 minutes each power buys parts for its fleet (12 an hour at
//     peace, 16 under tension, 24 at war) at its own stations and the freeports, choosing by its tastes, the parts' traits and
//     price; they go into its fleet's fitted parts (counted in the ledger), which wear out half an hour and fall as debris in
//     its space (the war spends them).
//   - Tweaks: every 15 minutes (Restless: every 10) a maker reviews its trait lines over the last 45 minutes. A line bought
//     less than half its fair share, or outsold two to one (and by 3) by a rival's line of its kind, gets a tweak: its
//     strength up 2 to 4 points (a launcher +1), its weakness grown to at least half the strength, at most +25% (launchers +2),
//     3 tweaks a line, 30 minutes apart. A tweak changes every unit of the line, fitted ones too.
//   - CEOs (Penny-pincher, Premium, Innovator, Expansionist, Cautious, Generous, Discounter, Restless): Premium prices +15%,
//     Discounter -10%, Innovator tweaks a third bigger, Generous pays half as much again in dividends, Cautious 0.6 times.
//     The board replaces a CEO whose share price has fallen two hours running (2 hours' grace for a new one).
//   - Shares: worth (treasury + stock on the shelves at cost + 8 hours of smoothed profit) / 100 shares, valued hourly.
//     Dividends: 40% of an hour's profit when in profit and not struggling, 60% to its home, 40% to the Compact.
//   - Struggling below 2 hours of running costs (News); failing when it can't pay them: its works close, its stock stays on
//     sale. 30 to 60 minutes later a new company opens at the same home, capitalised by the home, making the same kinds of
//     part under a new name, with a new CEO and small fresh traits.
const CE={floor0:.6,floorH:3,markup:1.5,shut:7200,start:8000,dues:.15,floor:1.15,base:60,lineF:.5,lineMin:10,shelf:1,cap:4,struggleH:2,reborn:[1800,3600],review:900,window:2700,twCool:1800,twMax:3,twStep:[.02,.04],trCap:.25,magCap:2,
  refit:{peace:12,tension:16,war:24,every:300,keep:3000,away:.35},wear:.5,div:.4,divHome:.6,grace:7200,
  ceos:['Penny-pincher','Premium','Innovator','Expansionist','Cautious','Generous','Discounter','Restless']};
const CE_KSTAT={gun:['dmg','ammo'],laser:['dmg','e'],missile:['mag','lock'],torpedo:['mag','lock'],charge:['mag'],mlaser:['ml','e'],cargo:['cargo'],scanner:['scan'],dronec:['dh','dd']};
const CE_BAD={e:1,lock:1};   // stats where a rise is a weakness
const CE_TASTE={halcyon:{laser:1.5,cargo:1.5,scanner:1.2,dronec:1.2},varkesh:{gun:1.5,torpedo:1.3,mlaser:1.5,charge:1.5,missile:1.2},ostrova:{scanner:1.8,laser:1.3,missile:1.2}};
const CE_NAMES=[['Lumen','Vesper','Halyard','Cinder','Tallow','Aster','Granite','Corvid','Quill','Ferrous','Saltmarsh','Paleward','Sable','Kestrel','Orrery','Lattice'],['Works','Industries','Fabrication','Yards','Arms','Systems','Engineering','Manufactory']];
// the game's own line-up, kept so a new galaxy starts from it
const CE_DEF={mk:{},it:{}};for(const m in MAKERS)CE_DEF.mk[m]={name:MAKERS[m].name,short:MAKERS[m].short,parts:JSON.parse(JSON.stringify(MAKERS[m].parts))};
for(const m in MK_LINE)for(const id of MK_LINE[m])CE_DEF.it[id]={name:ITEMS[id].name,tr:{...(ITEMS[id].tr||{})}};
function ceW(m){return'corp_'+m}
function ceKind(id){const I=ITEMS[id];return!I?'?':I.part||(I.sys?'sys_'+I.sys:'?')}
function ceT(m){return(S.econ.treasury[ceW(m)])||0}
function ceOf(m){return S.corp&&S.corp[m]}
function ceHomeWallet(m){const h=MAKERS[m].home;return FAC_IDS.includes(h)?h:'neutral'}
function ceHostWallet(m){const R=mkAtHome(m);if(!R)return ceHomeWallet(m);return R.owner==='neutral'?'neutral':R.owner}
function ceAlive(m){const c=ceOf(m);return!!c&&!c.dead}
function ceTrLines(m){return(MK_LINE[m]||[]).filter(id=>id.startsWith('mp_'))}
function ceGood(tr){let g=0;for(const k in tr){const v=k==='mag'?tr[k]*.1:tr[k];g+=CE_BAD[k]?-v:v}return g}
function ceNews(m,msg,big){try{if(newsOK()){newsAdd({f:ceHomeWallet(m),who:MAKERS[m].name,msg:MAKERS[m].short+(/^'s /.test(msg)?'':' ')+msg},big);return}}catch(e){}allFeed(`${MAKERS[m].name}: ${msg}`,'news')}
// ---- names and traits: applied from S.corp (a loaded galaxy) or reset to the game's own (a new one)
// ---- logos (7 Nov 2026): each maker shows its mark (MK_LOGO, 16zzz_logos.js) in its accent (MK_ACC). A reborn maker keeps the
// accent (it still belongs to its home) and takes a spare mark no other maker shows, preferring one never used in the galaxy
// (S.corpLogos keeps the spares used). A galaxy saved before logos gets each maker's own mark.
function mkLogoOf(m){const c=S&&S.corp&&S.corp[m];return c&&c.logo&&MK_LOGO[c.logo]?c.logo:m}
function mkAcc(m){return MK_ACC[m]||'#e8c878'}
// a logo as inline SVG, px square: the glyph alone, or (board) on a dark board with an accent rim like the R&D station's
function logoSvg(key,col,px,board){const L=MK_LOGO[key];if(!L)return'';const t=board?`<rect x="-1.08" y="-1.08" width="2.16" height="2.16" rx=".12" fill="#0e121e" stroke="${col}" stroke-width=".14"/><path d="${L.d}" fill="${col}" transform="scale(.74)"/>`:`<path d="${L.d}" fill="${col}"/>`;
  return`<svg class="mklogo" width="${px}" height="${px}" viewBox="-1.16 -1.16 2.32 2.32" role="img" aria-label="${esc(L.n)}" style="vertical-align:middle;flex:none"><title>${esc(L.n)}</title>${t}</svg>`}
function mkLogoSvg(m,px,board){return logoSvg(mkLogoOf(m),mkAcc(m),px,board)}
function ceNewLogo(m){const used=new Set(Object.keys(S.corp||{}).filter(x=>x!==m).map(mkLogoOf)),ever=new Set(S.corpLogos||[]);
  const free=MK_SPARE.filter(k=>!used.has(k)),fresh=free.filter(k=>!ever.has(k)),k=pick(fresh.length?fresh:free.length?free:MK_SPARE);S.corpLogos=[...ever,k];return k}
function ceApply(){if(S&&S.corp&&!NET.cl)for(const m in S.corp)if(S.corp[m]&&!S.corp[m].logo)S.corp[m].logo=m;
  for(const m in MAKERS){const d=CE_DEF.mk[m],c=ceOf(m);MAKERS[m].name=c&&c.name||d.name;MAKERS[m].short=c&&c.short||d.short;
    for(const k in d.parts){const id=`mp_${m}_${k}`;MAKERS[m].parts[k]=c&&c.tr&&c.tr[id]?{...c.tr[id]}:{...d.parts[k]}}
    for(const id of MK_LINE[m]||[]){const I=ITEMS[id],D=CE_DEF.it[id];if(!I||!D)continue;const tr=c&&c.tr&&c.tr[id]?c.tr[id]:D.tr;I.tr={...tr};
      I.name=c&&c.short&&c.short!==d.short?D.name.replace(d.short,c.short):D.name;I.trTxt=id.startsWith('mq_')?`${MAKERS[m].name}: standard.`:(trText(I.tr)?`${MAKERS[m].name}: ${trText(I.tr)}.`:`${MAKERS[m].name}: standard.`);
      const tw=c&&c.ln&&c.ln[id]&&c.ln[id].tw;if(tw)I.trTxt+=` Revised ${tw===1?'once':tw===2?'twice':tw+' times'}.`}}}
function ceInit(){if(S.corp||NET.cl||S.training)return;S.corp={};for(const m in MAKERS){const home=ceHomeWallet(m);S.corp[m]={logo:m,ceo:pick(CE.ceos),ceoT:0,ln:{},tr:{},sales:[],hist:[],E:0,px:0,pxH:[],div:0,gen:1,inc:0,cost:0};
    transfer(home,ceW(m),CE.start);S.corp[m].store={...CE_STOCK};if(S.ledger0){const v=invVec(CE_STOCK);for(const e of RAWS)S.ledger0.tot[e]+=v[e]}}ceApply()}
// (user, 8 Nov 2026) "Double the makers' starting treasury. Give the makers some components to start with." A maker starts with 8,000 cr and
// its own store of components (made with the galaxy), which its works use before buying off the market; its supply runs land there too
const CE_STOCK={plate:60,wire:40,coil:20};
function ceStore(m){const c=ceOf(m);if(!c)return{};return c.store=c.store||{}}
{const o=ledger;ledger=function(){const r=o.apply(this,arguments);try{const L=r.L.Stations;for(const m in S.corp||{}){const st=S.corp[m].store;if(!st)continue;const v=invVec(st);for(const e of RAWS){L[e]+=v[e];r.tot[e]+=v[e]}}}catch(e){}return r}}
{const o=newGame;newGame=function(){const r=o.apply(this,arguments);try{if(S){S.corp=null;ceApply();if(!S.training)ceInit()}}catch(e){console.error(e)}return r}}
{const o=startWith;startWith=function(st){const r=o.apply(this,arguments);try{if(S){ceApply();if(!S.corp&&!S.training)ceInit()}}catch(e){console.error(e)}return r}}
// ---- prices: the profit floor and the CEO's pricing
function ceComp(sid,id){const R=S.stations[sid],rc=ITEMS[id]&&ITEMS[id].recipe;if(!rc)return 0;let c=0;for(const k in rc)c+=(R?stPrice(R,k):baseValue(k))*rc[k];return c}
{const o=stPrice;stPrice=function(R,id){const v=o.apply(this,arguments);try{const I=ITEMS[id],m=I&&I.maker;if(!m||!S||!S.corp||!R)return v;const c=ceOf(m),k=c&&c.ceo==='Premium'?1.15:c&&c.ceo==='Discounter'?.9:1;
  const cc=ceComp(R.sid,id);return Math.max(v*k,cc*CE.markup*k,cc*CE.floor/(1-CE.dues))}catch(e){return v}}}
// ---- a sale: the maker's share to its treasury, the station's dues stay with its owner
function ceSale(m,id,n,paid,wallet,sid){if(!S.corp||!(paid>0))return;const c=ceOf(m);if(!c)return;if(c.dead){return}const net=Math.floor(paid*(1-CE.dues));const got=transfer(wallet,ceW(m),net);
  const home=mkHomeSid(m),mar=got-ceComp(home,id)*n;c.sales.push([S.T,ITEMS[id].base||id,n,mar,sid]);c.inc+=got;c.mar=(c.mar||0)+mar}
{const o=dockAction;dockAction=function(act,arg){if(act!=='buy'||!S||!S.corp||NET.cl)return o.apply(this,arguments);const k=String(arg).split(':')[0],I=ITEMS[k];if(!I||!I.maker)return o.apply(this,arguments);
  const c=dockCtx();if(!c||!c.market||c.wallet==='player'||c.owner==='player')return o.apply(this,arguments);const P=S.player,c0=P.credits,n0=c.market[k]||0,wl=c.wallet;const r=o.apply(this,arguments);
  try{const spent=c0-P.credits,n=n0-(c.market[k]||0);if(spent>0&&n>0)ceSale(I.maker,k,n,spent,wl,P.sector)}catch(e){console.error(e)}return r}}
// ---- the works: prudent, and paying for their components
function ceSold(m,id,span){const c=ceOf(m);let n=0;for(const x of c.sales)if(x[1]===id&&x[0]>S.T-span)n+=x[2];return n}
function ceReserve(m){const c=ceOf(m);return(c.ceo==='Penny-pincher'?5:c.ceo==='Cautious'?6:1)*ceUpkeep(m)}
makersTick=function(){if(NET.cl||!S||S.training||S.unb)return;S.mkT=S.mkT||0;if(S.T<S.mkT)return;S.mkT=S.T+MK_WORKS.every;
  if(!S.corpConv){try{corpConvert()}catch(e){}S.corpConv=1}
  for(const m in MAKERS){const R=mkAtHome(m);if(!R)continue;if(S.corp&&!ceAlive(m))continue;const st=mkStock(R);
    const want=id=>!S.corp?MK_WORKS.cap:Math.min(CE.cap,CE.shelf+ceSold(m,id,3600));
    const ids=MK_LINE[m].filter(id=>(st[id]||0)<want(id)&&!(S.corp&&S.T>CE.shut&&!ceSold(m,id,CE.shut)&&(st[id]||0)>0)).sort((a,b)=>(st[a]||0)/want(a)-(st[b]||0)/want(b));
    for(const id of ids){const rc=ITEMS[id].recipe;if(!haveIn(rc,[st]))continue;if(S.corp){const cost=Math.ceil(ceComp(R.sid,id));if(ceT(m)-cost<ceReserve(m))continue;transfer(ceW(m),R.owner==='neutral'?'neutral':R.owner,cost);ceOf(m).cost+=cost}
      takeFrom(rc,[st]);inv.add(st,id,1);break}}};
// ---- running costs: 60 cr an hour plus half each line's fair margin (at least 10)
function ceFair(){const T=S.T,mar={},nl={};for(const m in MAKERS){const c=ceOf(m);if(!c||c.dead)continue;for(const x of c.sales)if(x[0]>T-3600){const k=ceKind(x[1]);mar[k]=(mar[k]||0)+x[3]}for(const id of MK_LINE[m]){const k=ceKind(id);nl[k]=(nl[k]||0)+1}}
  const f={};for(const k in nl)f[k]=Math.max(0,mar[k]||0)/nl[k];return f}
let CE_FAIR={t:-1,f:{}};
function ceUpkeep(m){if(CE_FAIR.t!==S.T){CE_FAIR={t:S.T,f:ceFair()}}const c=ceOf(m);let u=CE.base;for(const id of MK_LINE[m]||[]){if(c&&S.T>CE.shut&&!ceSold(m,id,CE.shut))continue;u+=Math.max(CE.lineMin,CE.lineF*(CE_FAIR.f[ceKind(id)]||0))}return u*(c&&c.ceo==='Penny-pincher'?.75:1)}
function ceMinute(){const T=S.T;for(const m in MAKERS){const c=ceOf(m);if(!c)continue;
    if(c.dead){if(T>=c.reborn)ceReborn(m);continue}
    c.sales=c.sales.filter(x=>x[0]>T-Math.max(CE.window,CE.shut,3600));
    const due=ceUpkeep(m)/60,paid=transfer(ceW(m),ceHostWallet(m),Math.max(1,Math.round(due)));c.cost+=paid;c.up=(c.up||0)+paid;
    if(paid<Math.round(due)||ceT(m)<=0){ceFail(m);continue}
    const str=ceT(m)<CE.struggleH*ceUpkeep(m);if(str&&!c.str){c.str=1;ceNews(m,`is in trouble: under ${CE.struggleH} hours of running costs left (${fmt(ceT(m))} cr).`)}else if(!str&&c.str&&ceT(m)>CE.struggleH*1.5*ceUpkeep(m))c.str=0}}
function ceFail(m,why){const c=ceOf(m);if(c.rd){if(c.rd.proto)inv.addAll(ceStore(m),c.rd.proto);c.rd=null}c.dead=1;c.str=0;c.floorH=0;c.vals=0;c.px0=0;c.reborn=S.T+rnd(...CE.reborn);const left=ceT(m);if(left>0)transfer(ceW(m),ceHostWallet(m),left);
  ceNews(m,why==='floor'?`has been liquidated after ${CE.floorH} hours with its shares on the floor. Its works are closed and what it made stays on sale; a new company will take them over.`:`has failed. Its works are closed; what it made stays on sale, and its shares are worthless.`,true)}
function ceReborn(m){const c=ceOf(m),home=ceHomeWallet(m);if((S.econ.treasury[home]||0)<CE.start){c.reborn=S.T+300;return}const old=MAKERS[m].name;
  let nm,sh,i=0;do{sh=pick(CE_NAMES[0]);nm=`${sh} ${pick(CE_NAMES[1])}`;i++}while(i<20&&Object.values(MAKERS).some(x=>x.short===sh));
  c.name=nm;c.short=sh;c.dead=0;c.gen=(c.gen||1)+1;c.logo=ceNewLogo(m);c.ceo=pick(CE.ceos);c.ceoT=S.T;c.ln={};c.tr={};c.sales=[];c.E=0;c.iv=0;c.mar=0;c.up=0;c.px0=0;c.floorH=0;c.pxH=[];c.inc=0;c.cost=0;
  for(const id of ceTrLines(m)){const ks=CE_KSTAT[ITEMS[id].part];if(!ks)continue;const s=ks[0],tr={};tr[s]=s==='mag'?1:(CE_BAD[s]?-1:1)*Math.round(rnd(.04,.08)*100)/100;ceBalance(tr,ITEMS[id].part);c.tr[id]=tr}
  transfer(home,ceW(m),CE.start);ceApply();ceNews(m,`opens at ${DEF[mkHomeSid(m)].name} in the works ${old} left, under CEO trait ${c.ceo}. Its new mark: ${MK_LOGO[c.logo].n}.`,true)}
// ---- tweaks
function ceBalance(tr,kind){const ks=CE_KSTAT[kind]||[];let good=0,bad=0;for(const k in tr){const v=(k==='mag'?tr[k]*.1:tr[k])*(CE_BAD[k]?-1:1);if(v>0)good+=v;else bad-=v}
  const need=good*.5-bad;if(need<=.001)return tr;const w=ks.find(k=>k!=='mag'&&!((tr[k]||0)*(CE_BAD[k]?-1:1)>0))||'speed';const sg=CE_BAD[w]?1:-1;tr[w]=Math.round(((tr[w]||0)+sg*need)*100)/100;return tr}
function ceTweak(m,id,why){const c=ceOf(m),I=ITEMS[id],ks=CE_KSTAT[I.part];if(!ks)return false;const tr={...(c.tr[id]||I.tr||{})};
  const gv=k=>(k==='mag'?(tr[k]||0)*.1:(tr[k]||0))*(CE_BAD[k]?-1:1);let s=ks.slice().sort((a,b)=>gv(b)-gv(a))[0];if(gv(s)<0)s=ks.find(k=>gv(k)>=0)||ks[0];
  const sg=CE_BAD[s]?-1:1,step=s==='mag'?1:Math.round(rnd(...CE.twStep)*(c.ceo==='Innovator'?4/3:1)*100)/100,cap=s==='mag'?CE.magCap:CE.trCap;
  const cur=(tr[s]||0)*sg;if(cur>=cap)return false;tr[s]=sg*Math.min(cap,Math.round((cur+step)*100)/100);ceBalance(tr,I.part);
  c.tr[id]=tr;const L=c.ln[id]=c.ln[id]||{tw:0,last:-1e9};L.tw++;L.last=S.T;ceApply();
  ceNews(m,`has revised its ${I.name.replace(MAKERS[m].short+' ','')} (${why}): now ${trText(tr)}.`);return true}
function ceReview(){const T=S.T,sold={},byKind={};for(const m in MAKERS){const c=ceOf(m);if(!c||c.dead)continue;for(const id of MK_LINE[m]){sold[id]=ceSold(m,id,CE.window);const k=ceKind(id);(byKind[k]=byKind[k]||[]).push([m,id])}}
  for(const m in MAKERS){const c=ceOf(m);if(!c||c.dead)continue;const every=c.ceo==='Restless'?600:CE.review;if(T<(c.revT||0))continue;c.revT=T+every;
    for(const id of ceTrLines(m)){const k=ITEMS[id].part;if(!CE_KSTAT[k])continue;const L=c.ln[id]||{tw:0,last:-1e9};if(L.tw>=CE.twMax||T-L.last<(c.ceo==='Restless'?CE.twCool/2:CE.twCool))continue;
      const peers=byKind[k]||[],tot=peers.reduce((a,[,x])=>a+sold[x],0),fair=tot/Math.max(1,peers.length),mine=sold[id];
      const rival=peers.filter(([mm])=>mm!==m).sort((a,b)=>sold[b[1]]-sold[a[1]])[0];
      if(rival&&sold[rival[1]]>=2*mine&&sold[rival[1]]>=mine+3)ceTweak(m,id,`outsold by ${MAKERS[rival[0]].short}`);
      else if(fair>=1&&mine<fair*.5)ceTweak(m,id,'buyers passing it by')}}}
// ---- the hour: profit, shares, dividends, the board
// (user, 8 Nov 2026: "fix investment vs product launch") the share price rides on the operating profit (the margin on what
// sold, less running costs), not on cash flow: components bought for stock, R&D and freight are investments. Stock counts at
// cost and the R&D a maker has put in counts while its project runs, then fades 20% an hour after it ends.
// The market leader's premium: each kind of part a maker outsold every rival in over the last hour (2 or more sold) adds 15%
// to its price, up to 45%; a launch that takes the lead lifts the price, losing it drops it. While a maker leads a kind, the
// R&D it put in fades 5% an hour instead of 20% (investors keep valuing a product that leads).
function ceLeads(){const u={};for(const m in MAKERS){const c=ceOf(m);if(!c||c.dead)continue;for(const x of c.sales){if(x[0]<=S.T-3600)continue;const k=ceKind(x[1]);(u[k]=u[k]||{})[m]=(u[k][m]||0)+x[2]}}
  const n={};for(const k in u){let b=null,bv=0,sec=0;for(const m in u[k]){const v=u[k][m];if(v>bv){sec=bv;bv=v;b=m}else if(v>sec)sec=v}if(b&&bv>=2&&bv>sec)n[b]=(n[b]||0)+1}return n}
function ceHour(){const LEAD=ceLeads();for(const m in MAKERS){const c=ceOf(m);if(!c||c.dead)continue;c.lead=LEAD[m]||0;const cf=c.inc-c.cost,p=(c.mar||0)-(c.up||0);c.inc=0;c.cost=0;c.mar=0;c.up=0;c.E=c.E?c.E*.6+p*.4:p;if(!c.rd)c.iv=Math.round((c.iv||0)*(c.lead?.95:.8));c.hist.push([S.T,p,ceT(m)]);if(c.hist.length>48)c.hist.shift();
    let sv=0;for(const sid in S.stations){const R=S.stations[sid];if(!R)continue;let st;try{st=mkStock(R)}catch(e){continue}for(const id of MK_LINE[m])for(let g=1;g<=5;g++){const gid=g>1?`${id}_g${g}`:id;if(st[gid])sv+=st[gid]*ceComp(mkHomeSid(m),gid)}}
    const px=Math.max(1,(ceT(m)+sv+(c.iv||0)+8*c.E)/100*(1+Math.min(.45,.15*c.lead)));c.px=px;c.pxH.push(Math.round(px*10)/10);if(c.pxH.length>48)c.pxH.shift();
    if(p>0&&!c.str){const k=c.ceo==='Generous'?1.5:c.ceo==='Cautious'?.6:1,d=Math.floor(p*CE.div*k);if(d>0){const a=transfer(ceW(m),ceHomeWallet(m),Math.floor(d*CE.divHome)),b=transfer(ceW(m),'neutral',d-Math.floor(d*CE.divHome));c.div+=a+b}}
    const H=c.pxH,n=H.length;if(n>=3&&S.T-c.ceoT>=CE.grace&&H[n-1]<H[n-2]*.95&&H[n-2]<H[n-3]*.95){const old=c.ceo;c.ceo=pick(CE.ceos.filter(x=>x!==old));c.ceoT=S.T;ceNews(m,`'s board has replaced its CEO after two hours of shares falling 5% or more: out goes a ${old}, in comes a ${c.ceo}.`)}}
  ceFloor()}
// (user, 8 Nov 2026) "if a company's stock is on the floor long enough it's liquidated and a new maker created". The floor is
// the bottom of the market: a share price under 60% of the median of the live makers' prices. Three hourly valuations
// there in a row (not counting a company's first two) and the company is wound up: its cash goes to its shareholders (as dividends: 60% its home, 40% the Compact),
// then it closes as a failed company does, and a new company opens in its works 30 to 60 minutes later.
function ceFloor(){const L=Object.keys(MAKERS).filter(m=>ceAlive(m)&&ceOf(m).px>0);if(L.length<4)return;const ps=L.map(m=>ceOf(m).px).sort((a,b)=>a-b),med=ps[Math.floor(ps.length/2)];
  for(const m of L){const c=ceOf(m);c.vals=(c.vals||0)+1;c.floorH=c.vals>2&&c.px<CE.floor0*med?(c.floorH||0)+1:0;if(c.floorH>=CE.floorH){const left=ceT(m);transfer(ceW(m),ceHomeWallet(m),Math.floor(left*CE.divHome));transfer(ceW(m),'neutral',ceT(m));ceFail(m,'floor')}}}
// ---- the powers refit their fleets from the markets
function ceRefitRate(f){let w=false,t=false;for(const g of FAC_IDS){if(g===f)continue;try{if(warWith(f,g))w=true;else if(S.rel&&relOf&&relOf(f,g)<=-25)t=true}catch(e){}}return w?CE.refit.war:t?CE.refit.tension:CE.refit.peace}
function ceRefit(){for(const f of FAC_IDS){const st=S.econ.stock[f];if(!st)continue;const pool=(S.corpFit=S.corpFit||{})[f]=S.corpFit[f]||{};
    // wear: half an hour's share of the fitted parts falls as debris in its space
    const tot=Object.values(pool).reduce((a,b)=>a+b,0);let lose=Math.floor(tot*CE.wear*CE.refit.every/3600+Math.random());const terr=[...territory(f)].filter(id=>S.sectors[id]);
    while(lose-->0&&terr.length){const ks=Object.keys(pool).filter(k=>pool[k]>0);if(!ks.length)break;const k=pick(ks);inv.take(pool,k,1);toDebris(S.sectors[pick(terr)],{[k]:1})}
    // buy
    let n=Math.floor(ceRefitRate(f)*CE.refit.every/3600+Math.random());const where=Object.values(S.stations).filter(R=>R&&(R.owner===f||R.owner==='neutral')&&R.sid!==WRACK.sid);
    while(n-->0){if((S.econ.treasury[f]||0)<CE.refit.keep)break;const c=[];
      for(const R of where){let ms;try{ms=mkStock(R)}catch(e){continue}for(const id in ms){const I=ITEMS[id];if(!I||!I.maker||!(ms[id]>0))continue;const pr=stPrice(R,id),bv=Math.max(1,baseValue(id));
        const w=((CE_TASTE[f]||{})[I.part]||1)*(CORP_W.has(I.part)?1:.6)*(1+2*ceGood(I.tr||{}))/Math.pow(pr/bv,.5)*(R.owner===f?1.3:1);if(w>0)c.push([[R,id,pr],w])}}
      if(!c.length)break;const[R,id,pr]=wpickArr(c),ms=mkStock(R),wl=R.owner==='neutral'?'neutral':R.owner,p=Math.ceil(pr);if((S.econ.treasury[f]||0)<p)break;
      transfer(f,wl,p);inv.take(ms,id,1);inv.add(pool,id,1);if(R.mk)R.mk[id]=(R.mk[id]||0)-1;ceSale(ITEMS[id].maker,id,1,p,wl,R.sid)}}}
{const o=ledger;ledger=function(){const r=o.apply(this,arguments);try{const L=r.L['Fleets in muster'];for(const f in S.corpFit||{}){const v=invVec(S.corpFit[f]);for(const e of RAWS){L[e]+=v[e];r.tot[e]+=v[e]}}}catch(e){}return r}}
function ceTick(){if(NET.cl||!S||S.training||!S.corp)return;const T=S.T;
  if(T>=(S.ceMin||0)){S.ceMin=T+60;ceMinute()}if(T>=(S.ceRef||0)){S.ceRef=T+CE.refit.every;ceRefit()}ceReview();if(T>=(S.ceHr||3600)){S.ceHr=T+3600;ceHour()}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{ceTick()}catch(e){console.error(e)}return r}}
// ---- the Company screen: Economy → Corporations
function ceState(m){const c=ceOf(m);if(!c)return['var(--dim)','—'];if(c.dead)return['#ff5d4f','failed'];if(c.str)return['#ff9a4f','struggling'];if(c.floorH)return['#ff9a4f',`shares on the floor (${c.floorH} h)`];const h=c.hist.slice(-2);const p=h.length?h[h.length-1][1]:0;return p>150?['#7ad9a7','thriving']:p<0?['#f0b24a','losing money']:['var(--dim)','steady']}
function ceSpark(H){const L=H.slice(-12);if(!L.length)return'';const lo=Math.min(...L),hi=Math.max(...L),r=Math.max(.01,hi-lo);return`<span class="cospark">${L.map(x=>`<i style="height:${Math.max(2,Math.round((x-lo)/r*20))}px;background:#5fa8ff"></i>`).join('')}</span>`}
function ceHtml(P){let h=coViews('economy',[['hour','Hour'],['3h','3 hours'],['corps','Corporations']]);if(!S.corp)return h+'<div class="empty">The corporations\' books open with a new galaxy.</div>';
  const ms=Object.keys(MAKERS);if(!coPk.economy||!String(coPk.economy).startsWith('corp:'))coPk.economy='corp:'+ms[0];const sel=String(coPk.economy).slice(5);
  h+=`<div class="cowrap"><div class="colist">`;for(const m of ms){const c=ceOf(m),[col,word]=ceState(m),hm=MAKERS[m].home;
    h+=coRowH({tab:'economy',key:'corp:'+m,on:sel===m,icon:mkLogoSvg(m,22,true),title:esc(MAKERS[m].name),sub:`${esc(FAC_IDS.includes(hm)?FACTIONS[hm].short:DEF[hm].name)} · CEO ${esc(c.ceo)}`,mid:ceSpark(c.pxH),right:`${coStat(col,word)}<b class="mono" style="margin-left:10px">${c.dead||!c.px?'—':fmt(Math.round(c.px))+' cr'}</b>`})}
  const m=sel,c=ceOf(m),[col,word]=ceState(m),last=c.hist.slice(-1)[0];
  let d=`<div class="lab">Corporation · ${esc(word)}</div><div class="ldname" style="display:flex;gap:10px;align-items:center">${mkLogoSvg(m,40,true)}<span><b>${esc(MAKERS[m].name)}</b><br><span class="note" style="margin:0">Its mark: ${esc(MK_LOGO[mkLogoOf(m)].n)}</span></span></div>`+coKV([['Home',esc(DEF[mkHomeSid(m)].name)],['CEO',esc(c.ceo)],['Treasury',`${fmt(ceT(m))} cr`],['Share price',c.dead?'worthless':c.px?`${fmt(Math.round(c.px))} cr (rough value; shares aren't traded yet)`:'valued after its first hour'],
    ['Last hour',last?`${last[1]>=0?'+':''}${fmt(last[1])} cr`:'not yet'],['Running costs',`${fmt(Math.round(ceUpkeep(m)))} cr an hour`],['Dividends paid',`${fmt(c.div)} cr`]]);
  d+=`<div class="lab" style="margin-top:12px">Its lines</div>`+(MK_LINE[m]||[]).map(id=>{const I=ITEMS[id],L=c.ln[id];return`<div class="coln">${gIcon(id,14)}<span style="flex:1;min-width:0">${esc(I.name)} <span class="mass">${id.startsWith('mq_')?'standard':esc(trText(I.tr)||'standard')}${L&&L.tw?` · revised ${L.tw}×`:''}</span></span><span class="mono note" style="margin:0">${ceSold(m,id,3600)} sold this hour</span></div>`}).join('');
  d+=`<p class="note" style="margin-top:12px">A maker earns from every sale of its parts (the station keeps 15%), pays its host for components and running costs, tweaks lines its buyers pass by, and pays dividends to its home and the Compact. One that can't pay its way fails, and a new company takes over its works.</p>`;
  return h+`</div><div class="codet">${d}</div></div>`}
{const o=ecHtml;ecHtml=function(P){if(coV.economy==='corps')return ceHtml(P);if(String(coPk.economy||'').startsWith('corp:'))coPk.economy='co';let h=o.apply(this,arguments);return h.replace(/(<button class="cov[^"]*" type="button" data-co="cov" data-arg="economy:3h">3 hours<\/button>)/,`$1<button class="cov" type="button" data-co="cov" data-arg="economy:corps">Corporations</button>`)}}
// the market's note on the works says how they build now
{const o=fbMarketHtml;fbMarketHtml=function(c,P){let h=o.apply(this,arguments);if(!S||!S.corp)return h;return h.replace(/These corporations build their parts here from this station's components, one every \d+ s up to \d+ on sale\./,`These corporations buy this station's components to build their parts here, one every ${MK_WORKS.every} s, stocking each line to what it sells (up to ${CE.cap}). Their books are on the Company screen: Economy → Corporations.`)}}
