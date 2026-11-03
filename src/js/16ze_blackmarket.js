//@src 16ze_blackmarket.js
// ============================================================ the Black market tab: smuggling run as a business (Beyond section 6, 3 Nov 2026)
// On the Company screen. Your contacts are the freeports' fixers and the powers' quiet buyers wherever you've docked, and the
// Rusty Tankard once you've been to Scrapheart. The tab lists every offer they have for you:
//   - runs (the fixers' and the Tankard's, from 16l/16r): their goods carried into a power's station past its customs;
//   - contraband buys: a fixer sells cash-only contraband (Riftstone, relics, Rift Shards) from the freeport's stock (None);
//   - contraband sells: a quiet buyer at a power's station pays over the odds for cash-only contraband (Heavy, Severe at a
//     core) or fences goods stolen from another power (Light with the power they were stolen from).
// Every offer shows its heat rating (None, Light, Heavy, Severe: what it adds if you're caught) and pays by it, on top of
// the goods' price where the work is to be done. Filter by rating; Request work from a kind of contact (once every 2 minutes).
// Assign a run to yourself (loaded when you dock at its source; otherwise your course is set there), to one of your AI crews
// (it flies the run abstractly: caught or paid when it arrives; its hull's hold sets what it can carry; if caught the goods
// are seized by that power and the heat lands on you), or to a Compact contractor (you take a 25% broker's cut; if caught,
// the heat is theirs). Runs in progress and the last results are listed with where they are and the heat at their goal.
// Ledger: goods only move (freeport or Unbound stock → a run's load → the destination's market, or the seizing power's stores).
const BMX={req:120,broker:.25,crewT:[60,45],catch:{None:0,Light:.12,Heavy:.22,Severe:.35},fast:{courier:.7,skiff:.85},buyK:.85,sellK:{Heavy:.5,Severe:.75},fenceK:1.4,log:8,RATES:['None','Light','Heavy','Severe']};
let bmFilter='all';
function bmRate(r){return r==='None'?0:BM_RATE[r]||0}
function bmMet(P){return(P&&P.bmMet)||{}}
{const o=openDock;openDock=function(){const r=o.apply(this,arguments);try{const P=S.player;if(P&&P.docked==='station'&&!S.unb){P.bmMet=P.bmMet||{};P.bmMet[P.sector]=1}}catch(e){}return r}}
// ---- new offers: runs from a contact, contraband buys at freeports, quiet buyers at the powers' stations
function bmRun(from){const R=S.stations[from];if(!R)return null;S.bm=S.bm||[];const rum=from===WRACK.sid,st=mkStock(R);
  const goods=Object.keys(st).filter(k=>(st[k]||0)>=6&&ITEMS[k]&&!ITEMS[k].part&&!String(k).startsWith('v_')&&!ITEMS[k].cash);if(!goods.length)return null;
  const dests=Object.keys(S.stations).filter(s=>{const D=S.stations[s];return D&&FAC_IDS.includes(D.owner)&&HOP[from]&&HOP[from][s]!=null&&HOP[from][s]<=(rum?6:5)});if(!dests.length)return null;
  const to=pick(dests),D=S.stations[to],f=D.owner,core=D.kind==='core',emb=FAC_IDS.some(g=>g!==f&&(pairOf(f,g)||{}).emb),rating=rum?(core?'Severe':'Heavy'):emb?(core?'Severe':'Heavy'):'Light',item=pick(goods),n=Math.min(st[item],ri(6,14));
  const x={id:S.nextId++,from,to,f,item,n,rating,pay:Math.round(stPrice(D,item)*n*(1+BM_RATE[rating])+(rum?250:150)+(rum?80:60)*HOP[from][to]),until:S.T+900};if(rum){x.payer='pirate';x.rum=1}S.bm.push(x);return x}
function bmBuy(from){S.bm=S.bm||[];const R=S.stations[from];if(!R||R.owner!=='neutral')return null;const st=mkStock(R),goods=Object.keys(st).filter(k=>ITEMS[k]&&ITEMS[k].cash&&(st[k]||0)>=2);if(!goods.length)return null;const item=pick(goods),n=Math.min(st[item],ri(2,8));
  const x={id:S.nextId++,kind:'buy',from,to:from,f:null,item,n,rating:'None',unit:Math.max(1,Math.round(stPrice(R,item)*BMX.buyK)),until:S.T+900};S.bm.push(x);return x}
function bmSell(at){S.bm=S.bm||[];const D=S.stations[at];if(!D||!FAC_IDS.includes(D.owner))return null;const f=D.owner;
  if(Math.random()<.5){const gs=FAC_IDS.filter(g=>g!==f);const g=pick(gs),item=pick(['fe','cu','ir','au','nu','plate','wire','coil']),n=ri(6,20);
    const x={id:S.nextId++,kind:'fence',from:at,to:at,f:g,buyer:f,item,n,rating:'Light',unit:Math.round(baseValue(item)*BMX.fenceK),until:S.T+1200};S.bm.push(x);return x}
  const items=['rift','relic','riftshard'].filter(k=>ITEMS[k]&&!(ITEMS[k].legal||[]).includes(f));if(!items.length)return null;const item=pick(items),rating=D.kind==='core'?'Severe':'Heavy',n=ri(2,8);
  const x={id:S.nextId++,kind:'sell',from:at,to:at,f,buyer:f,item,n,rating,unit:Math.round(baseValue(item)*(1+BMX.sellK[rating])),until:S.T+1200};S.bm.push(x);return x}
// contacts post buys and quiet buys on their own now and then, as the fixers post runs
{const o=fixerTick;fixerTick=function(){const r=o.apply(this,arguments);try{if(NET.cl||S.training||S.unb)return r;S.bm=S.bm||[];
  if(Math.random()<.05){const fps=Object.keys(S.stations).filter(s=>S.stations[s].owner==='neutral'&&!S.bm.some(x=>x.kind==='buy'&&x.from===s&&!x.taken));if(fps.length)bmBuy(pick(fps))}
  if(Math.random()<.08){const ps=Object.keys(S.stations).filter(s=>FAC_IDS.includes(S.stations[s].owner)&&S.bm.filter(x=>(x.kind==='sell'||x.kind==='fence')&&x.from===s&&!x.taken).length<2);if(ps.length)bmSell(pick(ps))}}catch(e){console.error(e)}return r}}
// ---- what you can see: offers from your contacts
function bmOffers(P){const met=bmMet(P),T=S.T;return(S.bm||[]).filter(x=>!x.taken&&T<x.until&&met[x.from]&&S.stations[x.from]&&S.stations[x.to])}
function bmKind(x){return x.kind==='buy'?'Contraband buy':x.kind==='sell'?'Quiet buyer':x.kind==='fence'?'Fence':x.rum?'Rumour':'Run'}
function bmDesc(x){const fn=k=>esc(ITEMS[k].name),st=s=>esc(S.stations[s].name);
  if(x.kind==='buy')return`${x.n} ${fn(x.item)} for sale at ${st(x.from)}, ${fmt(x.unit)} cr each`;
  if(x.kind==='sell')return`${x.n} ${fn(x.item)} wanted at ${st(x.from)}, ${fmt(x.unit)} cr each`;
  if(x.kind==='fence')return`Up to ${x.n} ${fn(x.item)} stolen from ${esc(FACTIONS[x.f].short)}, fenced at ${st(x.from)} for ${fmt(x.unit)} cr each`;
  return`${x.n} ${fn(x.item)} from ${st(x.from)} into ${st(x.to)}`}
function bmPay(x){return x.kind==='buy'?-x.unit*x.n:x.kind?x.unit*x.n:x.pay}
// ---- runs assigned to crews or contractors
function bmRuns(){return S.bmRuns=S.bmRuns||[]}
function bmCrews(P){const out=[];for(const R of myDepots(P))for(const c of R.crew||[])if(!c.laid&&c.job!=='run')out.push({R,c});return out}
function bmCatch(x,cls,P){let p=BMX.catch[x.rating]||0;p*=(1+heatOf(x.f,P)/100);if(cls&&BMX.fast[cls])p*=BMX.fast[cls];return clamp(p,0,.9)}
function bmAssign(P,id,who){const x=(S.bm||[]).find(y=>String(y.id)===String(id)&&!y.taken);if(!x||x.kind)return'That run is gone.';const R=S.stations[x.from],k=pkeyOf(P);
  if(who==='me'){if(P.run)return'You are already on a run.';if(P.docked==='station'&&P.sector===x.from){dockAction('bmtake',x.id);return dockErr}P.route=x.from;return`Course set to ${R.name}: dock there to load the run.`}
  let crew=null,cls=null;if(who!=='hire'){const L=bmCrews(P),q=L.find(z=>String(z.c.id)===String(who));if(!q)return'That crew is busy or gone.';crew=q;cls=q.c.cls;
    const cap=(CLASSES[cls]&&CLASSES[cls].cargo)||0;if(cap<mass(x.item)*x.n)return`${q.c.name}'s ${CLASSES[cls].name} holds ${cap} t: the run needs ${mass(x.item)*x.n} t.`}
  const st=mkStock(R),n=inv.take(st,x.item,x.n);if(!n)return'The goods are gone.';x.taken=1;const h=HOP[x.from][x.to]||1;
  const run={id:S.nextId++,pid:k,x:{from:x.from,to:x.to,f:x.f,item:x.item,n,rating:x.rating,pay:Math.round(x.pay*n/x.n),payer:x.payer||'neutral'},load:{[x.item]:n},who:crew?'crew':'hire',name:crew?crew.c.name:'a Compact contractor',crewR:crew&&crew.R.sid,crewId:crew&&crew.c.id,
    start:S.T,eta:S.T+BMX.crewT[0]+BMX.crewT[1]*h,caught:Math.random()<bmCatch(x,cls,P),state:'run'};
  if(crew){crew.c.prevJob=crew.c.job;crew.c.job='run'}bmRuns().push(run);return`✓ ${run.name} takes the run: ${bmDesc(x)}. Due in ${fmtT(run.eta-S.T)}.`}
function bmRunTick(){if(NET.cl||!S||S.unb)return;for(const r of bmRuns()){if(r.state!=='run'||S.T<r.eta)continue;const x=r.x,P=xPilotOfKey(r.pid)||S.player,D=S.stations[x.to],crewDone=()=>{const R=S.stations[r.crewR],c=R&&(R.crew||[]).find(y=>y.id===r.crewId);if(c&&c.job==='run')c.job=c.prevJob||'idle'};
    if(r.caught&&FAC_IDS.includes(x.f)){inv.addAll(S.econ.stock[x.f],r.load);r.load={};r.state='caught';if(r.who==='crew')smHeat(P,x.f,SM.heat[x.rating]||20,'a run caught');
      r.msg=`caught by ${FACTIONS[x.f].short} customs: the goods were seized${r.who==='crew'?`, and ${x.rating} heat landed on you`:''}`;keyFeed(r.pid,`✕ ${r.name}'s run into ${D?D.name:DEF[x.to].name} was ${r.msg}.`,'bad')}
    else{const mk=D?mkStock(D):S.econ.stock[x.f]||S.econ.stock.neutral;inv.addAll(mk,r.load);r.load={};let got=0;
      if(r.who==='crew')got=payTo(P,x.payer,x.pay);else{got=payTo(P,x.payer,Math.round(x.pay*BMX.broker));if(x.payer!=='neutral')transfer(x.payer,'neutral',x.pay-got)}
      r.state='paid';r.got=got;r.msg=`delivered: +${fmt(got)} cr${r.who==='hire'?' (your broker\'s cut)':''}`;keyFeed(r.pid,`✓ ${r.name}'s run into ${D?D.name:DEF[x.to].name} ${r.msg}.`,'good')}
    r.done=S.T;crewDone()}
  const done=bmRuns().filter(r=>r.state!=='run');if(done.length>BMX.log*4)S.bmRuns=bmRuns().filter(r=>r.state==='run'||done.indexOf(r)>=done.length-BMX.log*4)}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{bmRunTick()}catch(err){console.error(err)}return r}}
{const o=ledger;ledger=function(){const r=o.apply(this,arguments);try{const L=r.L['Fleets in muster'];for(const x of S.bmRuns||[]){const v=invVec(x.load||{});for(const e of RAWS){L[e]+=v[e];r.tot[e]+=v[e]}}}catch(e){}return r}}
// a crew away on a run isn't in the world and can't be given other orders
{const o=crewSync;crewSync=function(){const L=[];for(const R of Object.values(S.stations||{}))for(const c of(R&&R.crew)||[])if(c.job==='run'&&!c.laid){c.laid=true;L.push(c)}try{return o.apply(this,arguments)}finally{for(const c of L)c.laid=false}}}
// ---- buying and selling at the contact (docked there)
function bmDeal(P,id){const x=(S.bm||[]).find(y=>String(y.id)===String(id)&&!y.taken&&S.T<y.until);if(!x||!x.kind)return'That offer is gone.';const R=S.stations[x.from];
  if(!(P.docked==='station'&&P.sector===x.from)){P.route=x.from;return`Course set to ${R.name}: dock there to deal.`}
  if(x.kind==='buy'){const room=W&&W.player?W.player.st.cargo-invMass(P.cargo):0,n=Math.min(x.n,Math.floor(room/mass(x.item)),Math.floor(P.credits/x.unit));if(n<=0)return room<mass(x.item)?'No hold space.':'Not enough credits.';
    const st=mkStock(R),got=inv.take(st,x.item,n);if(!got)return'The goods are gone.';payFrom(P,'neutral',got*x.unit);inv.add(P.cargo,x.item,got);x.n-=got;if(x.n<=0)x.taken=1;return`✓ Bought ${got} ${ITEMS[x.item].name} for ${fmt(got*x.unit)} cr. Cash-only contraband: keep it from the powers' scans.`}
  stolSync(P);let have=P.cargo[x.item]||0;if(x.kind==='fence')have=Math.min(have,(P.stol&&P.stol[x.item]&&P.stol[x.item][x.f])||0);const n=Math.min(have,x.n,Math.floor((S.econ.treasury[x.buyer]||0)/x.unit));if(n<=0)return x.kind==='fence'?`You carry no ${ITEMS[x.item].name} stolen from ${FACTIONS[x.f].short}.`:`You carry no ${ITEMS[x.item].name}.`;
  inv.take(P.cargo,x.item,n);inv.add(mkStock(R),x.item,n);if(x.kind==='fence'){P.stol[x.item][x.f]-=n;if(P.stol[x.item][x.f]<=0)delete P.stol[x.item][x.f]}const got=payTo(P,x.buyer,n*x.unit);x.n-=n;if(x.n<=0)x.taken=1;return`✓ Sold ${n} ${ITEMS[x.item].name} quietly: +${fmt(got)} cr.`}
// ---- requesting work
function bmRequest(P,kind){if(S.T<(P.bmReqT||0))return`Your contacts need ${fmtT(P.bmReqT-S.T)} before they'll have more.`;const met=Object.keys(bmMet(P)).filter(s=>S.stations[s]);let x=null;
  if(kind==='fix'){const L=met.filter(s=>S.stations[s].owner==='neutral');if(!L.length)return'Dock at a freeport first: its fixers are your contacts.';for(let i=0;i<6&&!x;i++){const s=pick(L);x=Math.random()<.7?bmRun(s):bmBuy(s)||bmRun(s)}}
  else if(kind==='rum'){if(!met.includes(WRACK.sid))return'Go to Scrapheart Haven first: the Rusty Tankard only talks to faces it knows.';if(typeof havenDown==='function'&&havenDown())return'Scrapheart is dark.';x=bmRun(WRACK.sid)}
  else if(kind==='buy'){const L=met.filter(s=>FAC_IDS.includes(S.stations[s].owner));if(!L.length)return"Dock at a power's station first: its quiet buyers are your contacts.";for(let i=0;i<6&&!x;i++)x=bmSell(pick(L))}
  if(!x)return'Nothing doing just now.';P.bmReqT=S.T+BMX.req;return`✓ New offer: ${bmDesc(x)}.`}
{const o=dockAction;dockAction=function(act,arg){const P=S.player;if(act==='bmassign'){const[id,who]=String(arg).split(':');dockErr=bmAssign(P,id,who);return}if(act==='bmdeal'){dockErr=bmDeal(P,arg);return}if(act==='bmreq'){dockErr=bmRequest(P,arg);return}
  if(act==='crewjob'){const[sid,id]=String(arg).split(':'),R=S.stations[sid],c=R&&(R.crew||[]).find(x=>String(x.id)===id);if(c&&c.job==='run'){dockErr=`${c.name} is away on a run.`;return}}return o.apply(this,arguments)}}
{const o=coClick;coClick=function(act,arg){if(act==='bmfilt'){bmFilter=arg;renderCompany();return}if(['bmassign','bmdeal','bmreq'].includes(act)){if(NET.cl){netSend({t:'act',act,arg});coErr='Working…';renderCompany();return}dockAction(act,arg);coErr=dockErr;renderCompany();return}return o.apply(this,arguments)}}
// ---- the tab
{const o=coTabs;coTabs=function(){const L=o.apply(this,arguments);return S&&S.unb?L:[...L,['bm','Black market']]}}
{const o=renderCompany;renderCompany=function(){o.apply(this,arguments);try{if(coTab==='bm')$('coBody').innerHTML=bmHtml(S.player)}catch(err){console.error(err)}}}
function bmHtml(P){const rc={None:'var(--dim)',Light:'#f0d070',Heavy:'#ff9a4a',Severe:'#ff5d4f'},met=bmMet(P);
  let h=`<p class="note" style="margin:0 0 10px">Smuggling run as a business. Your contacts are the freeports' fixers and the powers' quiet buyers wherever you've docked${met[WRACK.sid]?', and the Rusty Tankard':''}. Every offer is rated by the heat it brings if you're caught, and pays by it (Light +25%, Heavy +50%, Severe +75%).</p>`;
  h+=`<div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:10px">${FAC_IDS.map(f=>{const w=heatWord(heatOf(f,P));return`<span><span style="color:${FACTIONS[f].col}">${esc(FACTIONS[f].short)}</span> heat: <b style="color:${w[1]}">${w[0]}</b></span>`}).join('')}</div>`;
  h+=`<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px"><span class="note" style="margin:0;align-self:center">Request work:</span><button class="btn sm" type="button" data-co="bmreq" data-arg="fix">From the fixers</button><button class="btn sm" type="button" data-co="bmreq" data-arg="buy">From the quiet buyers</button>${met[WRACK.sid]?`<button class="btn sm" type="button" data-co="bmreq" data-arg="rum">At the Rusty Tankard</button>`:''}
    <span style="flex:1"></span><span class="note" style="margin:0;align-self:center">Heat:</span>${['all',...BMX.RATES].map(r=>`<button class="btn sm${bmFilter===r?' pri':''}" type="button" data-co="bmfilt" data-arg="${r}">${r==='all'?'All':r}</button>`).join('')}</div>`;
  const L=bmOffers(P).filter(x=>bmFilter==='all'||x.rating===bmFilter),crews=bmCrews(P);
  h+=`<div class="tblw"><table class="t"><thead><tr><th>Offer</th><th>Heat if caught</th><th class="r">Pays</th><th>Take it</th></tr></thead><tbody>`;
  for(const x of L){const pay=bmPay(x),hf=x.f&&FACTIONS[x.f]?` with ${esc(FACTIONS[x.f].short)}`:'',h2=HOP[P.sector]&&HOP[P.sector][x.from];
    let act;if(x.kind)act=`<button class="btn sm" type="button" data-co="bmdeal" data-arg="${x.id}">${P.docked==='station'&&P.sector===x.from?(x.kind==='buy'?'Buy':'Sell'):'Set course'}</button>`;
    else act=`<button class="btn sm" type="button" data-co="bmassign" data-arg="${x.id}:me"${P.run?' disabled':''}>Myself</button>${crews.map(z=>`<button class="btn sm" type="button" data-co="bmassign" data-arg="${x.id}:${z.c.id}" title="${esc(CLASSES[z.c.cls].name)} · ${Math.round(bmCatch(x,z.c.cls,P)*100)}% chance of being caught">${esc(z.c.name)}</button>`).join('')}<button class="btn sm" type="button" data-co="bmassign" data-arg="${x.id}:hire" title="${Math.round(BMX.broker*100)}% of the pay to you; their heat if caught">A contractor</button>`;
    h+=`<tr><td class="iname" style="white-space:normal"><span class="mass">${bmKind(x)}${h2!=null?` · ${h2?h2+' jump'+(h2>1?'s':''):'here'}`:''}</span><br>${bmDesc(x)}</td><td><b style="color:${rc[x.rating]}">${x.rating}</b>${x.rating!=='None'?hf:''}</td><td class="r num">${pay<0?`−${fmt(-pay)}`:fmt(pay)} cr</td><td style="white-space:normal">${act}</td></tr>`}
  if(!L.length)h+=`<tr><td colspan="4" class="note">${Object.keys(met).length?'No offers right now: request work, or check back.':'No contacts yet: dock at a freeport or a power\'s station.'}</td></tr>`;h+=`</tbody></table></div>`;
  const k=pkeyOf(P),mine=bmRuns().filter(r=>r.pid===k),live=mine.filter(r=>r.state==='run'),past=mine.filter(r=>r.state!=='run').slice(-BMX.log).reverse();
  h+=`<div class="h3" style="margin-top:16px">Runs</div><div class="tblw"><table class="t"><tbody>`;
  if(P.run){const R2=S.stations[P.run.to];h+=`<tr><td class="iname">You</td><td>${P.run.n} ${esc(ITEMS[P.run.item].name)} into ${esc(R2?R2.name:'?')}</td><td><b style="color:${rc[P.run.rating]}">${P.run.rating}</b> · ${esc(FACTIONS[P.run.f].short)} heat ${heatWord(heatOf(P.run.f,P))[0]}</td><td class="r">${fmt(P.run.pay)} cr</td></tr>`}
  for(const r of live){const x=r.x,h0=HOP[x.from][x.to]||1,frac=clamp((S.T-r.start)/(r.eta-r.start),0,1),at=Math.min(h0,Math.floor(frac*h0));h+=`<tr><td class="iname">${esc(r.name)}</td><td>${x.n} ${esc(ITEMS[x.item].name)} into ${esc(S.stations[x.to]?S.stations[x.to].name:DEF[x.to].name)} · jump ${at} of ${h0}, due in ${fmtT(Math.max(0,r.eta-S.T))}</td><td><b style="color:${rc[x.rating]}">${x.rating}</b> · ${esc(FACTIONS[x.f].short)} heat ${heatWord(heatOf(x.f,P))[0]}</td><td class="r">${fmt(r.who==='hire'?Math.round(x.pay*BMX.broker):x.pay)} cr</td></tr>`}
  for(const r of past)h+=`<tr><td class="iname">${esc(r.name)}</td><td colspan="2" style="color:${r.state==='paid'?'var(--ok,#7ad9a7)':'var(--danger)'}">${r.x.n} ${esc(ITEMS[r.x.item].name)}: ${esc(r.msg)}</td><td class="r note">${fmtT(Math.max(0,S.T-r.done))} ago</td></tr>`;
  if(!P.run&&!live.length&&!past.length)h+=`<tr><td class="note">No runs yet.</td></tr>`;return h+`</tbody></table></div>`}
