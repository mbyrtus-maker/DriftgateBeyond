//@src 16o_depots.js
// ============================================================ Depots, your market, your AI crews and the Economy (Beyond stage 10)
// A Depot is your first open base: on every map, with Driftgate 1's depot modules (storage, production, defence, armour,
// hangar, life support), a market, and a hangar for AI crews. Upgrade a Lair in place (2 Depot Frames, from your hold or its
// stash, while docked there) or build one fresh in a system with no station (2 Depot Frames in your hold).
// Level: 1, 2 with three modules, 3 with six.
// Your market: mark goods in the depot's store for sale (keeping a reserve) or to buy (up to a target). Traders of the powers
// that will deal with you visit every minute or so: they buy what's for sale at the market price, paid from their power's
// treasury, and sell you what you want from their power's stores. Goods and credits only move, so both ledgers stay exact.
// AI crews: hire a pilot with a hull at your depot (the hull's price, to the Compact's yards). Each draws a wage every hour
// (to the Compact, which supplies the crews) and uses up an Alloy Plate of running costs from the depot's store (into the outer
// drift). If the wage can't be paid the pilot leaves; without the plate the ship is laid up. Orders: Mine (cuts ore from this
// system's rocks into the store), Haul (sells goods marked for sale at the nearest power market that deals with you), Guard
// (stiffens the depot's guns), Idle.
const DEP={cost:{frame:2},tradeT:60,lot:10,crewT:60,wage:300,run:{plate:1},guardK:.25,mine:{skiff:3,prospector:5,dredger:7},haul:{courier:20,freighter:35,bulker:70},hangar0:1};
function myDepots(P){const k=pkeyOf(P);return Object.values(S.stations||{}).filter(R=>R&&R.owner==='player'&&R.kind==='depot'&&(R.pid||'me')===k)}
function depLvl(R){const u=devUsed(R);return u>=6?3:u>=3?2:1}
function depCan(sid){return!S.stations[sid]&&canBuildIn(sid,'player')}
function depMake(P,sid,pos,fort,stock){const R=makeStation(sid,'player','depot',pos,fort);R.pid=pkeyOf(P);R.stock=stock||{};R.sell={};R.buy={};R.crew=[];R.eco=[];sectorOwnerReset&&sectorOwnerReset();return R}
// put the new depot into the loaded system's world, as a captured station is
function depEnt(R){try{const w=WORLDS[R.sid];if(w&&!w.stationEnt)inW(w,()=>addStationEnt(R))}catch(e){}}
function sectorOwnerReset(){try{if(S.ctrlCache)S.ctrlCache={}}catch(e){}}
// from a Lair (docked there): the stash becomes the depot's store, the Lair's fortifications its own
function depFromLair(P,L){if(!depCan(L.sid))return'A Depot needs a system with no station.';const st=L.stash,srcs=[P.cargo,st];if(!haveIn(DEP.cost,srcs))return`A Depot needs ${lackText(DEP.cost,Object.assign({},st,P.cargo))}.`;
  takeFrom(DEP.cost,srcs);const fort={...(L.fort||{})};inv.addAll(fort,DEP.cost);const R=depMake(P,L.sid,{x:L.x,y:L.y,z:L.z},fort,st);L.stash={};L.fort={};S.lairs=S.lairs.filter(x=>x!==L);
  depEnt(R);if(P.docked==='lair'&&P.lairId===L.id){P.docked='station';P.lairId=null}return`✓ ${R.name} stands where your Lair was: on every map now, with a market and a hangar.`}
function depFresh(P){if(!W||!W.player)return'Launch first.';if(!depCan(W.sid))return'A Depot needs a system with no station, outside the powers\' home space.';if(!haveIn(DEP.cost,[P.cargo]))return`A Depot needs ${lackText(DEP.cost,P.cargo)} in your hold.`;
  takeFrom(DEP.cost,[P.cargo]);const fort={};inv.addAll(fort,DEP.cost);const R=depMake(P,W.sid,stationSite(W.sid),fort,{});depEnt(R);return`✓ ${R.name} is built. Dock there to fit its modules and hire crews.`}
// ---- the economy log: every credit a base earns or spends, with its reason
function eco(R,kind,n,why){if(!R||!n)return;R.eco=R.eco||[];R.eco.push({t:Math.round(S.T),k:kind,n:Math.round(n),w:why});if(R.eco.length>400)R.eco.splice(0,R.eco.length-400)}
function ecoSum(R,from,to){const o={};for(const e of R.eco||[])if(e.t>=from&&e.t<to)o[e.k]=(o[e.k]||0)+e.n;return o}
// ---- traders at your market
function depTraders(P){return FAC_IDS.filter(f=>standOf(f,P)>=STAND.dock&&!pilotHostile(P,f))}
function depTradeTick(){for(const R of Object.values(S.stations||{})){if(!R||R.owner!=='player'||R.kind!=='depot'||!R.sell)continue;const O=lairOwner({pid:R.pid||'me'})||S.player,fs=depTraders(O),reps=typeof hasB==='function'&&hasB(R,'market')?2:1,lot=DEP.lot*(typeof hasB==='function'&&hasB(R,'storage')?2:1),mg=(R.mg||1)*(reps>1?1.1:1);if(!fs.length)continue;for(let rep=0;rep<reps;rep++){if(Math.random()<.35)continue;const f=pick(fs),st=R.stock,fst=S.econ.stock[f]=S.econ.stock[f]||{};
  for(const k in R.sell){const n=Math.min(lot,(st[k]||0)-(R.sell[k]||0));if(n<=0)continue;const pr=Math.max(1,Math.round(price(st,k)*mg));const pay=Math.min(n*pr,S.econ.treasury[f]||0);const m=Math.floor(pay/pr);if(m<=0)continue;inv.take(st,k,m);inv.add(fst,k,m);const got=payTo(O,f,m*pr);eco(R,'market',got,`${FACTIONS[f].short} traders bought ${m} ${ITEMS[k].name}`)}
  for(const k in R.buy){const n=Math.min(lot,(R.buy[k]||0)-(st[k]||0),fst[k]||0);if(n<=0)continue;const pr=Math.max(1,Math.round(price(fst,k)));const m=Math.min(n,Math.floor(O.credits/pr));if(m<=0)continue;inv.take(fst,k,m);inv.add(st,k,m);payFrom(O,f,m*pr);eco(R,'market',-m*pr,`bought ${m} ${ITEMS[k].name} from ${FACTIONS[f].short} traders`)}}}}
// pay credits from a pilot to a treasury (guests' credits live on their own record)
function payFrom(P,to,n){if(P===S.player)return transfer('player',to,n);const k=pkeyOf(P);let got=0;runAs(k,()=>{got=transfer('player',to,n)});return got}
function payTo(P,from,n){if(P===S.player)return transfer(from,'player',n);const k=pkeyOf(P);let got=0;runAs(k,()=>{got=transfer(from,'player',n)});return got}
// ---- AI crews (abstract: they work while you're away, every minute of game time)
function crewCap(R){return DEP.hangar0+((devOf(R).hangar)||0)}
function crewHire(R,P,cls){R.crew=R.crew||[];if(R.crew.length>=crewCap(R))return`The hangar holds ${crewCap(R)} crew${crewCap(R)>1?'s':''}: add a hangar module for more.`;if(!hullRatingOK(P,cls))return`The ${CLASSES[cls].name} needs Contractor Rating ${HULL_RATING[cls]}.`;
  const pr=Math.max(800,hullPrice(cls));if(P.credits<pr)return`A crew with a ${CLASSES[cls].name} costs ${fmt(pr)} cr.`;payFrom(P,'neutral',pr);eco(R,'hire',-pr,`hired a crew and a ${CLASSES[cls].name}`);
  const nm=pick(['Ash','Brannock','Cole','Dace','Ember','Fenn','Garrow','Hale','Iver','Juno','Kestrel','Lark','Maro','Nell','Orrin','Pike','Quill','Rook','Sable','Tamsin','Vale','Wren'])+' '+pick(['Ostler','Varga','Mire','Coyle','Strand','Holt','Dray','Penn','Rask','Tull']);
  R.crew.push({id:S.nextId++,name:nm,cls,job:blHull(cls)?'mine':isHaulCls(cls)?'haul':'guard',laid:false,hired:S.T});return`✓ ${nm} signs on with a ${CLASSES[cls].name}.`}
function crewTick(){for(const R of Object.values(S.stations||{})){if(!R||R.owner!=='player'||R.kind!=='depot'||!(R.crew||[]).length)continue;const O=lairOwner({pid:R.pid||'me'})||S.player,s=S.sectors[R.sid],k=DEP.crewT/3600;
  for(const c of R.crew.slice()){
    // wages and running costs, pro rata every minute
    c.owe=(c.owe||0)+DEP.wage*k;if(c.owe>=1){const n=Math.floor(c.owe);const got=payFrom(O,'neutral',Math.min(n,O.credits));c.owe-=got;if(got)eco(R,'wages',-got,`${c.name}'s wages`);if(got<n){R.crew=R.crew.filter(x=>x!==c);keyFeed(R.pid||'me',`✕ ${c.name} left ${R.name}: you couldn't pay the wage.`,'bad');continue}}
    c.runK=(c.runK||0)+k;if(c.runK>=1){c.runK-=1;if(haveIn(DEP.run,[R.stock])){takeFrom(DEP.run,[R.stock]);const v=invVec(DEP.run);S.drift=S.drift||{};for(const e of RAWS)S.drift[e]=(S.drift[e]||0)+v[e];c.laid=false}else{c.laid=true;keyFeed(R.pid||'me',`⚠ ${c.name}'s ship at ${R.name} is laid up: the depot has no Alloy Plate for running costs.`,'warn')}}
    if(c.laid)continue;
    if(c.job==='mine'&&DEP.mine[c.cls]&&!WORLDS[R.sid]){let want=DEP.mine[c.cls]*DEP.crewT/60;const room=Math.max(0,1e9);for(const a of s.ast.filter(x=>!x.rift&&!x.comet&&oreTotal(x)>0)){if(want<=0)break;while(want>0&&oreTotal(a)>0){const q=mainOre(a);inv.take(a.ore,q,1);inv.add(R.stock,q,1);want--}if(oreTotal(a)<=0)removeAst(s,a)}}
    if(c.job==='haul'&&DEP.haul[c.cls]&&typeof crewHaulStart==='function'){if(c.run)continue;c.hT=(c.hT||0)+DEP.crewT;if(c.hT<120)continue;c.hT=0;crewHaulStart(R,c,O);continue}
    if(c.job==='haul'&&DEP.haul[c.cls]){c.hT=(c.hT||0)+DEP.crewT;if(c.hT<120)continue;c.hT=0;const fs=depTraders(O);let best=null,bh=99;for(const id in S.stations){const D=S.stations[id];if(!D||!fs.includes(D.owner))continue;const h=HOP[R.sid]&&HOP[R.sid][id];if(h!=null&&h<bh){bh=h;best=D}}if(!best)continue;
      let cap=DEP.haul[c.cls];const mk=mkStock(best),f=best.owner;for(const q in R.sell){if(cap<=0)break;const m=Math.min(Math.floor(cap/mass(q)),(R.stock[q]||0)-(R.sell[q]||0));if(m<=0)continue;const pr=Math.max(1,Math.floor(price(mk,q)*.95));const n=Math.min(m,Math.floor((S.econ.treasury[f]||0)/pr));if(n<=0)continue;inv.take(R.stock,q,n);inv.add(mk,q,n);const got=payTo(O,f,n*pr);cap-=n*mass(q);eco(R,'hauling',got,`${c.name} sold ${n} ${ITEMS[q].name} at ${best.name}`)}}}}}
{const o=depGunK;depGunK=function(SE,t){const v=o.apply(this,arguments);const R=SE&&SE.rec;if(R&&R.owner==='player'&&R.crew){const g=R.crew.filter(c=>c.job==='guard'&&!c.laid).length;if(g)return v*(1+DEP.guardK*g)}return v}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{if(!NET.cl&&!S.training&&!S.unb){S.depT=S.depT||0;if(S.T>=S.depT){S.depT=S.T+DEP.tradeT;depTradeTick();crewTick()}}}catch(err){console.error(err)}return r}}
// ---- actions (docked, or from the Company screen)
{const o=dockAction;dockAction=function(act,arg){const P=S.player;
  if(act==='depotup'){const L=(S.lairs||[]).find(x=>x.id===P.lairId);if(!L){dockErr='Dock at the Lair you want to upgrade.';return}const m=depFromLair(P,L);if(m.startsWith('✓'))try{openDock('home')}catch(e){}dockErr=m;return}
  if(act==='depotbuild'){dockErr=depFresh(P);return}
  if(act==='crewhire'){const[sid,cls]=String(arg).split(':'),R=S.stations[sid];if(!R||R.owner!=='player'||(R.pid||'me')!==pkeyOf(P)){dockErr='Not your depot.';return}dockErr=crewHire(R,P,cls);return}
  if(act==='crewjob'){const[sid,id,job]=String(arg).split(':'),R=S.stations[sid],c=R&&(R.crew||[]).find(x=>String(x.id)===id);if(!c||(R.pid||'me')!==pkeyOf(P)){dockErr='No such crew.';return}c.job=job;dockErr=`✓ ${c.name}: ${job}.`;return}
  if(act==='crewfire'){const[sid,id]=String(arg).split(':'),R=S.stations[sid];if(!R||(R.pid||'me')!==pkeyOf(P)){dockErr='Not your depot.';return}R.crew=(R.crew||[]).filter(x=>String(x.id)!==id);dockErr='✓ Crew let go.';return}
  if(act==='mkset'){const[sid,k,mode,n]=String(arg).split(':'),R=S.stations[sid];if(!R||(R.pid||'me')!==pkeyOf(P)||!ITEMS[k]){dockErr='Not your depot.';return}R.sell=R.sell||{};R.buy=R.buy||{};delete R.sell[k];delete R.buy[k];if(mode==='sell')R.sell[k]=Math.max(0,+n||0);if(mode==='buy')R.buy[k]=Math.max(0,+n||0);dockErr=mode==='off'?`✓ ${ITEMS[k].name}: not traded.`:`✓ ${ITEMS[k].name}: ${mode} ${mode==='sell'?`(keeping ${+n||0})`:`(up to ${+n||0})`}.`;return}
  return o.apply(this,arguments)}}
// ---- the Company screen: Holdings lists depots too; Economy; Post jobs (your crews)
{const o=coTabs;coTabs=function(){return[...o.apply(this,arguments),['economy','Economy'],['crews','Post jobs']]}}
{const o=holdingsHtml;holdingsHtml=function(P){let h=o.apply(this,arguments);const D=myDepots(P);const L=P.docked==='lair'&&(S.lairs||[]).find(x=>x.id===P.lairId);
  let d=`<div class="h3" style="margin-top:16px">Depots</div><p class="note" style="margin:0 0 8px">A Depot is on every map, with a market, Driftgate 1's modules (Works tab when docked) and a hangar for AI crews. Upgrade a Lair in place (2 Depot Frames from your hold or its stash, docked there), or build fresh with 2 Depot Frames in your hold in a system with no station.</p>`;
  d+=D.length?`<div class="tblw"><table class="t"><thead><tr><th>Depot</th><th>Level</th><th class="r">Store</th><th class="r">Crews</th><th>Hull</th></tr></thead><tbody>${D.map(R=>`<tr><td class="iname">${esc(R.name)}</td><td>${depLvl(R)}</td><td class="r num">${invMass(R.stock)} t</td><td class="r num">${(R.crew||[]).length}/${crewCap(R)}</td><td>${Math.round(R.hull/R.hMax*100)}%</td></tr>`).join('')}</tbody></table></div>`:'<div class="note">No depots yet.</div>';
  if(L)d+=`<button class="btn pri" type="button" data-co="depotup" style="margin-top:8px">Upgrade this Lair to a Depot · 2 Depot Frames or a Depot Kit</button>`;else if(!P.docked&&W&&W.player)d+=`<button class="btn" type="button" data-co="depotbuild" style="margin-top:8px" ${depCan(W.sid)&&kitOr(DEP.cost,[P.cargo],'kit_depot')?'':'disabled'}>Build a Depot here · 2 Depot Frames or a Depot Kit in your hold</button>`;return h+d}}
function economyHtml(P){const D=myDepots(P),now=S.T;let h=`<p class="note" style="margin:0 0 10px">What each base earned and spent over the last hour, its trend over the last three, and why. Credits only ever move between you, the powers' treasuries and the Compact.</p>`;let tot=0;
  for(const R of D){const H=[0,1,2].map(i=>{const s=ecoSum(R,now-3600*(i+1),now-3600*i);return{s,n:Object.values(s).reduce((a,b)=>a+b,0)}}),net=H[0].n;tot+=net;const tr=H[0].n>H[1].n+50?'rising':H[0].n<H[1].n-50?'falling':'steady';
    const lines=Object.entries(H[0].s).sort((a,b)=>Math.abs(b[1])-Math.abs(a[1]));const why=(R.eco||[]).slice(-3).reverse().map(e=>e.w);
    h+=`<div style="border-top:1px solid var(--line);padding:8px 0"><div class="kv"><span><b>${esc(R.name)}</b> · ${net>=0?'gaining':'losing'} · trend ${tr}</span><b class="${net>=0?'amber':''}" style="${net<0?'color:var(--danger)':''}">${net>=0?'+':''}${fmt(net)} cr/h</b></div>
      <div class="note" style="margin:2px 0">${lines.length?lines.map(([k,n])=>`${k} ${n>=0?'+':''}${fmt(n)}`).join(' · '):'Nothing yet this hour.'}${why.length?` · latest: ${why.map(esc).join('; ')}`:''}</div>${depMarketHtml(R)}</div>`}
  if(!D.length)h+='<div class="note">No depots yet: the Economy tracks your depots\' markets, crews and wages.</div>';else h=`<div class="kv" style="margin-bottom:8px"><span>Company, last hour</span><b>${tot>=0?'+':''}${fmt(tot)} cr</b></div>`+h;return h}
function depMarketHtml(R){const ks=ITEM_ORDER.filter(k=>(R.stock[k]||0)>0||R.sell&&k in R.sell||R.buy&&k in R.buy||RAWS.includes(k)||['plate','wire','coil'].includes(k)).slice(0,16);
  return`<details style="margin-top:4px"><summary class="note">Your market at ${esc(R.name)}: what it sells and buys</summary><table class="t" style="margin-top:6px"><tbody>${ks.map(k=>{const mode=R.sell&&k in R.sell?'sell':R.buy&&k in R.buy?'buy':'off',sid=R.sid;
    return`<tr><td class="iname">${esc(ITEMS[k].name)}</td><td class="r num">${R.stock[k]||0}</td><td>${mode==='sell'?`selling, keeping ${R.sell[k]}`:mode==='buy'?`buying up to ${R.buy[k]}`:'not traded'}</td><td><div class="act"><button class="btn sm" type="button" data-co="mkset" data-arg="${sid}:${k}:sell:${Math.floor((R.stock[k]||0)/4)}">Sell</button><button class="btn sm" type="button" data-co="mkset" data-arg="${sid}:${k}:buy:${Math.max(20,(R.stock[k]||0)+20)}">Buy</button><button class="btn sm" type="button" data-co="mkset" data-arg="${sid}:${k}:off:0">Off</button></div></td></tr>`}).join('')}</tbody></table></details>`}
function crewsHtml(P){const D=myDepots(P);let h=`<p class="note" style="margin:0 0 10px">Your AI crews work from your depots while you fly: miners cut this system's rocks into the store, haulers sell what you mark for sale at the nearest market that deals with you, guards stiffen the depot's guns. Each draws ${fmt(DEP.wage)} cr an hour (to the Compact) and an Alloy Plate of running costs from the store; unpaid crews leave, unsupplied ships are laid up.</p>`;
  for(const R of D){h+=`<div class="h3" style="margin-top:12px">${esc(R.name)} · ${(R.crew||[]).length}/${crewCap(R)} crews</div>`;
    for(const c of R.crew||[])h+=`<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:4px 0"><b>${esc(c.name)}</b><span class="note" style="margin:0">${esc(CLASSES[c.cls].name)}${c.laid?' · <span style="color:var(--danger)">laid up</span>':''}</span>${['mine','haul','guard','idle'].map(j=>`<button class="btn sm" type="button" data-co="crewjob" data-arg="${R.sid}:${c.id}:${j}" aria-pressed="${c.job===j}" ${j==='mine'&&!DEP.mine[c.cls]||j==='haul'&&!DEP.haul[c.cls]?'disabled':''}>${j}</button>`).join('')}<button class="btn sm" type="button" data-co="crewfire" data-arg="${R.sid}:${c.id}">Let go</button></div>`;
    if((R.crew||[]).length<crewCap(R))h+=`<div class="act" style="flex-wrap:wrap;margin-top:6px">${['skiff','prospector','dredger','courier','freighter','bulker','interceptor','striker'].map(k=>`<button class="btn sm" type="button" data-co="crewhire" data-arg="${R.sid}:${k}" ${hullRatingOK(P,k)&&P.credits>=Math.max(800,hullPrice(k))?'':'disabled'}>Hire · ${esc(CLASSES[k].name)} · ${fmt(Math.max(800,hullPrice(k)))} cr</button>`).join('')}</div>`}
  if(!D.length)h+='<div class="note">Crews need a Depot.</div>';return h}
{const o=renderCompany;renderCompany=function(){o.apply(this,arguments);try{if(coTab==='economy')$('coBody').innerHTML=economyHtml(S.player);else if(coTab==='crews')$('coBody').innerHTML=crewsHtml(S.player)}catch(err){console.error(err)}}}
{const o=coClick;coClick=function(act,arg){if(['depotup','depotbuild','crewhire','crewjob','crewfire','mkset'].includes(act)){if(NET.cl){netSend({t:'act',act,arg});coErr='Working…';renderCompany();return}dockAction(act,arg);coErr=dockErr;renderCompany();return}return o.apply(this,arguments)}}
