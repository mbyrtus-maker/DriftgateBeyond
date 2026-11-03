//@src 16zc_dread.js
// ============================================================ the Dread Pirate: the Unbound's leader (Beyond 12c, 3 Nov 2026)
// The Unbound are led from the Wrack by the Dread Pirate (the title passes with the hat). It has two traits from the pirate
// table, flies the Ravager when it's afloat or a Corsair with an ace escort otherwise, is met in the world and on radar by name,
// and can be killed: every power pays the killer a bounty and a captain takes the hat. Unbound pilots fly like it, its traits
// steer where the raiders go, and every few minutes it may act on an event (raiding seasons, tribute, hoard sales, open house,
// lying low, Ravager raids, bounties on pilots). The Unbound have no relations, so its events move credits, goods and heat.
// Ledger: credits only move between treasuries and wallets; goods never appear.
const DP_TRAITS=['Bloodthirsty','Greedy','Cunning','Showman','Superstitious','Gallant','Paranoid','Kingmaker'];
const DP_NAMES=['Marrow','Black Agnes','Saltjaw','Rook Vane','Calloway Thorn','Mad Ottilie','Grimsby','Iron Nell','Vasquez Crane','Old Teague','Red Sorrel','Hollow Jack'];
const DP={cool:[240,480],back:900,bounty:3000,pBounty:2500,tribute:1500,season:1200,sale:900,saleK:.7,house:900,houseK:1.3,low:900,lowK:.3,kills:6};
const DP_SUCC={killedPow:['Bloodthirsty'],killedPilot:['Paranoid'],looted:['Paranoid','Cunning'],fat:['Greedy','Showman'],brood:['Superstitious'],leader:['Kingmaker'],failed:['Cunning'],kept:['Gallant']};
function dpOf(){return S&&S.dread||null}
function dpHas(t){const D=dpOf();return!!(D&&D.traits.includes(t))}
function dpName(D){D=D||dpOf();return D?`the Dread Pirate ${D.name}`:'the Dread Pirate'}
function dpNew(traits,n,why){const used=new Set([...(S.dpPast||[])]);const pool=DP_NAMES.filter(x=>!used.has(x));
  return{name:pick(pool.length?pool:DP_NAMES),traits:traits.slice(0,2),n:n||1,since:S.T,cool:S.T+rnd(300,600),why:why||null,grudge:{},bounty:{},kills:{},ship:{sid:'wr',alive:true,back:0,move:S.T+rnd(120,240),live:0}}}
function dpRoll(){const a=pick(DP_TRAITS);let b=pick(DP_TRAITS);while(b===a)b=pick(DP_TRAITS);return[a,b]}
function dpInit(){if(!S||S.dread||S.unb)return;S.dread=dpNew(LEADT&&LEADT.mode==='neutral'?[]:dpRoll(),1);dpProfile()}
{const o=newGame;newGame=function(){const r=o.apply(this,arguments);try{if(S&&!S.unb)dpInit()}catch(e){}return r}}
// ---- succession: a captain takes the hat, shaped by what happened
function dpSucceed(why,by){const D0=dpOf();if(!D0)return;S.dpPast=S.dpPast||[];S.dpPast.push(D0.name);const pool=[...(DP_SUCC[why]||[])];
  while(pool.length<2){const t=pick(DP_TRAITS);if(!pool.includes(t)&&!D0.traits.includes(t))pool.push(t)}const traits=LEADT&&LEADT.mode==='neutral'?[]:[pool[0],pool[1+Math.floor(Math.random()*(pool.length-1))]];
  const N=dpNew(traits,(D0.n||1)+1,why);if(why==='killedPow'&&by)N.grudge[by]=1;if(why==='killedPilot'&&by)N.bounty[by]=DP.pBounty;N.ship.alive=false;N.ship.back=S.T+DP.back;S.dread=N;dpProfile();
  const txt={killedPow:'its captain was killed',killedPilot:'its captain was killed by a contractor',looted:'Scrapheart was looted',fat:'years of plunder',brood:'raiders lost to the Brood',leader:'a power closing on the galaxy',failed:'a long run of failed raids',kept:'bargains kept'}[why]||why;
  allFeed(`☠ ${dpName(N)} takes the hat after ${txt}. ${N.traits.length?`${N.name} is ${N.traits.join(' and ')}.`:''}`,'news');chron&&chron(`${dpName(N)} took the hat from ${D0.name} after ${txt}.`)}
// ---- pilots fly like it (through the powers' leader profiles, by side)
function dpProfile(){const D=dpOf();if(!D)return;const t=x=>D.traits.includes(x),p={range:1,breakoff:0,stay:false,honour:false,ruthless:false,zeal:false};
  if(t('Bloodthirsty')){p.range*=1.3;p.stay=true}if(t('Showman'))p.range*=1.15;if(t('Cunning'))p.range*=.9;if(t('Paranoid')){p.range*=.8;p.breakoff=.25}if(t('Superstitious'))p.breakoff=Math.max(p.breakoff,.3);
  if(t('Greedy')||t('Gallant'))p.honour=true;if(t('Greedy'))p.ruthless=true;LEADP.pirate=p}
{const o=leaderProfiles;leaderProfiles=function(){const r=o.apply(this,arguments);try{dpProfile()}catch(e){}return r}}
// ---- the ship: the Ravager when it's afloat, a Corsair with an ace escort otherwise; spawned in a live system, moving off-screen
function dpRav(){return(S.frigates||[]).find(t=>t.side==='pirate'&&isCar(t)&&t.hull>0)||null}
function dpEnt(){for(const sid in WORLDS)for(const e of WORLDS[sid].ents)if(e.dreadOf&&e.alive)return e;return null}
function dpTick(){const D=dpOf();if(!D||NET.cl||S.training)return;const Sh=D.ship;
  if(!Sh.alive){if(S.T>=Sh.back){Sh.alive=true;Sh.sid='wr';Sh.move=S.T+rnd(60,180);allFeed(`☠ ${dpName()} is flying again.`,'news')}return}
  if(Sh.rav&&!(S.frigates||[]).some(t=>t.id===Sh.rav&&t.hull>0)){Sh.rav=null;Sh.alive=false;allFeed(`☠ ${dpName()} went down with the Ravager.`,'news');chron&&chron(`${dpName()} went down with the Ravager.`);dpSucceed('killedPow',null);return}
  const R=dpRav();if(R){Sh.sid=R.sector;Sh.rav=R.id;const e=carEnt(R);if(e&&!e.dreadOf)dpMark(e);Sh.live=e?1:0;return}Sh.rav=null;
  if(Sh.live){if(dpEnt())return;Sh.live=0}
  if(S.T>=Sh.move){const opts=NEIGH[Sh.sid].filter(s=>!DEF[s].home&&!(dpHas('Superstitious')&&broodHeld(s))&&(!dpHas('Paranoid')||(HOP.wr[s]||9)<=2));Sh.sid=opts.length&&Math.random()<.7?pick(opts):'wr';Sh.move=S.T+rnd(150,300)}
  const w=WORLDS[Sh.sid];if(w&&!(typeof STRAT_SIM==='function'&&STRAT_SIM()))dpSpawn(w)}
function dpMark(e){const D=dpOf();e.dreadOf=1;if(!e.tok)e.pname=`☠ ${dpName(D)}`}
function dpSpawn(w){const D=dpOf();let g=null;inW(w,()=>{try{xNoAce=true;g=aceWing({id:'DP',side:'pirate',name:D.name,nick:'the Dread Pirate',cls:'corsair'});if(g){const e=g.members[0];
  const st=shipStats(null,e.cls,3,1);st.hull*=3;st.sCap*=2;st.dmg*=1.3;e.st=st;e.hull=st.hull;e.shield=st.sCap;e.energy=st.eCap;e.tier=4;e.tuned=1;dpMark(e);for(const m of g.members.slice(1))m.tier=4}}finally{xNoAce=false}});
  if(g){D.ship.live=1;if(w===LW)feed(`☠ ${dpName(D)} is in this system, with an escort.`,'warn')}}
// ---- killed: every power pays the killer, and a captain takes the hat
{const o=killShip;killShip=function(e,src,at){try{if(e&&e.dreadOf&&e.alive&&!S.unb)dpKilled(e,src,at)}catch(err){console.error(err)}return o.apply(this,arguments)}}
function dpKilled(e,src,at){const D=dpOf();if(!D)return;D.ship.alive=false;D.ship.live=0;const k=src?sideNorm(src):null,kp=at&&at.src&&at.src.rp,killer=kp||(src==='player'?'me':null),P=killer?xPilotOfKey(killer):null;
  let paid=0;if(P)for(const f of FAC_IDS){const got=payTo(P,f,DP.bounty);paid+=got}
  allFeed(`☠ ${dpName(D)} is dead, shot down by ${P?(P.name||'a pilot'):FAC_IDS.includes(k)?FACTIONS[k].short:k==='brood'?'the Brood':'unknown guns'} in ${DEF[W.sid].name}.${paid?` The powers pay ${fmt(paid)} cr in bounties.`:''}`,'news');
  chron&&chron(`${dpName(D)} was shot down in ${DEF[W.sid].name}.`);dpSucceed(P?'killedPilot':'killedPow',P?pkeyOf(P):FAC_IDS.includes(k)?k:null)}
{const o=havenKnock;havenKnock=function(by,P){const was=havenDown();const r=o.apply(this,arguments);try{if(!was&&havenDown()&&Math.random()<.6)dpSucceed('looted')}catch(e){}return r}}
// ---- where the raiders go: seasons, grudges, Kingmaker, Superstitious and Paranoid captains
{const o=pirOrders;pirOrders=function(t){let r=o.apply(this,arguments);try{const D=dpOf();if(!D)return r;const from=HOPP[t.sector]||HOPP.wr,near=sid=>from[sid]!=null&&from[sid]<=3;
  const tgtF=D.season&&S.T<D.season.until?D.season.f:dpHas('Kingmaker')?dpLeader():Object.keys(D.grudge||{})[0];
  if(tgtF&&r!=='wr'&&Math.random()<.6){const L=SECTOR_DEFS.map(d=>d.id).filter(s=>PIR_OK.has(s)&&near(s)&&sideNorm(sectorOwner(s))===tgtF);if(L.length)r=pick(L)}
  if(D.ravage&&S.T<D.ravage.until&&t===dpRav()&&t.hull/capHullMax(t)>=.55)r=D.ravage.sid;
  if(dpHas('Superstitious')&&broodHeld(r))r='wr';if(dpHas('Paranoid')&&HOPP.wr[r]!=null&&HOPP.wr[r]>2)r='wr';if(D.low&&S.T<D.low)r='wr'}catch(e){}return r}}
function dpLeader(){const n=controlCounts();let b=null,bv=-1;for(const f of FAC_IDS)if((n[f]||0)>bv){bv=n[f]||0;b=f}return b}
// ---- lying low thins the raids; a hoard sale cuts the haven's prices; open house raises the rumours' pay
{const o=popWants;popWants=function(){const L=o.apply(this,arguments);const D=dpOf();if(!D||S.unb||!(D.low&&S.T<D.low))return L;return L.map(w=>w[1]==='pirate'?[w[0],w[1],w[2],w[3]*DP.lowK,w[4]]:w)}}
{const o=stPrice;stPrice=function(R,k){const v=o.apply(this,arguments);try{const D=dpOf();if(D&&D.sale&&S.T<D.sale&&R&&R===S.stations.wr)return v*DP.saleK}catch(e){}return v}}
{const o=fixerTick;fixerTick=function(){const n=(S.bm||[]).length;const r=o.apply(this,arguments);try{const D=dpOf();if(D&&D.house&&S.T<D.house)for(const x of(S.bm||[]).slice(n))if(x.rum&&!x.dpK){x.pay=Math.round(x.pay*DP.houseK);x.dpK=1}}catch(e){}return r}}
// a pirate bounty on a pilot: Unbound ships go for that pilot first
{const o=findHostile;findHostile=function(e,range){const t=o.apply(this,arguments);try{const D=dpOf();if(e&&e.side==='pirate'&&D&&Object.keys(D.bounty||{}).length){for(const x of W.ents){if(x.type!=='ship'||!x.alive)continue;const P=pilotOfEnt(x);if(P&&D.bounty[pkeyOf(P)]&&d3(x,e)<range*1.4&&hostE('pirate',x))return x}}}catch(err){}return t}}
// Unbound ships sunk by a contractor are counted against them
{const o=payKill;payKill=function(e,src,at){try{const D=dpOf();if(D&&e&&e.side==='pirate'){const kp=at&&at.gk?at.gk:at&&at.src&&at.src.rp,killer=kp||(src==='player'?'me':null);if(killer){const k=isMe(killer)?pkeyOf(S.player):killer;D.kills[k]=(D.kills[k]||0)+1}}}catch(err){}return o.apply(this,arguments)}}
// ---- its events: one at most every few minutes, chosen among those whose trigger holds, leaning to its traits
function dpEvents(){const D=dpOf(),out=[],T=S.T,st=S.econ.stock.pirate||{},tr=S.econ.treasury.pirate||0;
  {const f=pick(FAC_IDS);if(!(D.season&&T<D.season.until))out.push({k:'season',w:(dpHas('Greedy')||dpHas('Bloodthirsty'))?3:1,f})}
  {const f=pick(FAC_IDS);if((S.econ.treasury[f]||0)>DP.tribute*4)out.push({k:'tribute',w:(dpHas('Greedy')||dpHas('Cunning'))?3:1,f})}
  {const k=Object.keys(D.kills).find(x=>D.kills[x]>=DP.kills&&!D.bounty[x]);if(k)out.push({k:'bounty',w:(dpHas('Bloodthirsty')||dpHas('Paranoid'))?3:1,pid:k})}
  if(invMass(st)>600&&!(D.sale&&T<D.sale))out.push({k:'sale',w:(dpHas('Greedy')||dpHas('Kingmaker'))?3:1});
  if(tr>20000&&!(D.house&&T<D.house))out.push({k:'house',w:(dpHas('Showman')||dpHas('Gallant'))?3:1});
  if(((controlCounts().brood||0)>=6||(dpRav()&&dpRav().hull<capHullMax(dpRav())*.5))&&!(D.low&&T<D.low))out.push({k:'low',w:(dpHas('Superstitious')||dpHas('Paranoid'))?3:1});
  {const R=dpRav();if(R&&!R.live){const tg=Object.keys(S.stations).filter(s=>{const X=S.stations[s];return X&&FAC_IDS.includes(X.owner)&&X.kind==='depot'&&PIR_OK.has(s)&&HOPP[R.sector]&&HOPP[R.sector][s]!=null&&HOPP[R.sector][s]<=3&&X.hull<X.hMax*.6});if(tg.length)out.push({k:'ravage',w:(dpHas('Bloodthirsty')||dpHas('Showman'))?3:1,sid:pick(tg),t:R})}}
  return out}
function dpAct(){const D=dpOf();if(!D||NET.cl||S.training||S.unb||S.T<D.cool)return;D.cool=S.T+rnd(DP.cool[0],DP.cool[1]);if(havenDown())return;const L=dpEvents();if(!L.length)return;
  let tot=L.reduce((a,b)=>a+b.w,0),r=Math.random()*tot,E=L[0];for(const x of L){r-=x.w;if(r<=0){E=x;break}}const nm=dpName(D),T=S.T;
  if(E.k==='season'){D.season={f:E.f,until:T+DP.season};allFeed(`☠ ${nm} declares a raiding season on ${FACTIONS[E.f].short} lanes.`,'warn')}
  else if(E.k==='tribute'){const L2=leaderOf(E.f),pays=L2&&(L2.traits.includes('Mercantile')||L2.traits.includes('Cautious'))?.8:.4;if(Math.random()<pays){const got=transfer(E.f,'pirate',DP.tribute);D.spare=D.spare||{};D.spare[E.f]=T+DP.season;allFeed(`☠ ${FACTIONS[E.f].short} pays ${nm} ${fmt(got)} cr to keep the raiders off its lanes.`,'news')}else{D.season={f:E.f,until:T+DP.season};allFeed(`☠ ${FACTIONS[E.f].short} refuses ${nm}'s demand for tribute: a raiding season on its lanes.`,'warn')}}
  else if(E.k==='bounty'){D.bounty[E.pid]=DP.pBounty;const P=xPilotOfKey(E.pid);allFeed(`☠ ${nm} puts a ${fmt(DP.pBounty)} cr bounty on ${P&&P.name||'a contractor'} for the Unbound ships they've sunk.`,'warn')}
  else if(E.k==='sale'){D.sale=T+DP.sale;allFeed(`☠ ${nm} is selling off the hoard: Scrapheart's market is ${Math.round((1-DP.saleK)*100)}% cheaper for a while.`,'news')}
  else if(E.k==='house'){D.house=T+DP.house;allFeed(`☠ Open house at the Rusty Tankard: ${nm}'s rumours pay ${Math.round((DP.houseK-1)*100)}% more for a while.`,'news')}
  else if(E.k==='low'){D.low=T+DP.low;allFeed(`☠ ${nm} has the raiders lie low in the Wrack.`,'news')}
  else if(E.k==='ravage'){D.ravage={sid:E.sid,until:T+900};allFeed(`☠ ${nm} sails the Ravager for ${S.stations[E.sid].name}.`,'warn')}}
// captains lose faith: a long run of losses, or the Brood eating raiders; a power closing on the galaxy breeds a Kingmaker
function dpFaith(){const D=dpOf();if(!D||S.T-D.since<3600||Math.random()>.02)return;const n=controlCounts();
  if(Math.max(...FAC_IDS.map(f=>n[f]||0))>=VIC_NEED-4&&!dpHas('Kingmaker'))dpSucceed('leader');else if((S.econ.treasury.pirate||0)>60000&&!dpHas('Greedy'))dpSucceed('fat')}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{if(!S.unb&&!S.training){dpInit();dpTick();dpAct();dpFaith()}}catch(err){console.error(err)}return r}}
// ---- the Allegiance tab: the Dread Pirate beside the powers' leaders; its bounty on you
{const o=allegianceHtml;allegianceHtml=function(P){let h=o.apply(this,arguments);try{const D=dpOf();if(!D)return h;P=P||S.player;const b=D.bounty&&D.bounty[pkeyOf(P)];
  h+=`<div class="h3" style="margin-top:16px">The Unbound</div><div class="tblw"><table class="t"><tbody><tr><td style="color:${sideCol('pirate')};width:120px"><b>Unbound</b></td><td>${esc(dpName(D))}${D.n>1?` <span class="mass">${ordinal(D.n)} to wear the hat</span>`:''}</td><td>${D.traits.map(esc).join(' · ')}</td><td class="r" style="color:var(--dim)">${D.ship.alive?(D.ship.rav?'aboard the Ravager':'flying'):'not flying'}</td></tr></tbody></table></div>${b?`<p class="note" style="color:var(--danger)">☠ ${esc(dpName(D))} has a ${fmt(b)} cr bounty on you: Unbound ships go for you first.</p>`:''}`}catch(e){}return h}}
// ---- work: the powers post the hunt; the Rusty Tankard sells word of where it is
{const o=jobsList;jobsList=function(c,P,srcs){const out=o.apply(this,arguments);try{const D=dpOf();if(!D||!D.ship.alive||S.unb||!c||c.kind!=='station')return out;
  if(FAC_IDS.includes(c.owner)){const known=covOf(c.owner,true).has(D.ship.sid),j=known&&HOP[P.sector][D.ship.sid];out.push({id:'dp:'+c.owner,by:c.owner,sid:known?D.ship.sid:null,ty:'fight',title:`Hunt ${esc(dpName(D))}`,sub:known?`seen in ${esc(DEF[D.ship.sid].name)}`:'whereabouts unknown: ask at the Rusty Tankard',hops:j||0,where:known?`${j} jump${j===1?'':'s'}`:'',payN:DP.bounty*FAC_IDS.length,pay:`${fmt(DP.bounty*FAC_IDS.length)} cr`,btn:known&&D.ship.sid!==P.sector?['croute',D.ship.sid,'Set course']:null,
    detail:()=>`<p class="note" style="margin:0">Every power pays ${fmt(DP.bounty)} cr to whoever shoots the Dread Pirate down. It flies ${D.ship.rav?'the Ravager':'a Corsair with an ace escort'}.</p>`})}
  if(c.rum)out.push({id:'dpw',by:'pirate',sid:null,ty:'scout',title:`Word of ${esc(dpName(D))}'s whereabouts`,sub:'a rumour, 300 cr',hops:0,where:'here',payN:-300,pay:'−300 cr',btn:['dpword','','Buy the rumour · 300 cr'],detail:()=>`<p class="note" style="margin:0">Someone at the Rusty Tankard always knows where the hat is.</p>`})}catch(err){console.error(err)}return out}}
{const o=dockAction;dockAction=function(act,arg){if(act==='dpword'){const D=dpOf(),P=S.player;if(!D){dockErr='Nobody knows.';return}if(P.credits<300){dockErr='The rumour costs 300 cr.';return}payFrom(P,'pirate',300);dockErr=D.ship.alive?`☠ Word is ${dpName(D)} is in ${DEF[D.ship.sid].name}${D.ship.rav?', aboard the Ravager':''}.`:`☠ Word is ${dpName(D)} isn't flying: back in ${fmtT(Math.max(0,D.ship.back-S.T))}.`;feed(dockErr,'info');return}return o.apply(this,arguments)}}
{const o=dockClick;dockClick=function(act,arg){if(act==='dpword'){if(NET.cl){netSend({t:'act',act,arg});return}dockAction(act,arg);renderDock();return}return o.apply(this,arguments)}}
