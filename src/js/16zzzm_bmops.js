//@src 16zzzm_bmops.js
// ============================================================ Beyond: the black market's assassinations, spying and sabotage (user, 9 Nov 2026)
// Jobs → Black market. Each contract is taken by one pilot and paid by its client when the work is done.
//   Assassination of a power leader: a power at war with another posts a contract on the enemy leader's flagship (where it is
//     flying is on the card). Shot down by the taker: the client pays BMO.kill (on top of the bounty that killing a leader
//     already brings), Severe heat with the dead leader's power; the usual succession follows.
//   Assassination of a maker's CEO: every so often a maker's CEO flies a shuttle from the works to a freeport and back (a
//     named courier, like a test pilot); a rival maker posts a contract on it. Shot down by the taker: the client pays
//     BMO.ceo; the maker gets a new CEO, and its share price takes a 10% knock for the next hour's valuation.
//   (The Dread Pirate's hunt is on the black market too: 16zc_dread.js, marked bm.)
// Host only; credits only move between wallets, so the ledger stays exact.
const BMO={kill:4000,ceo:3000,every:60,ceoEvery:[1800,3600],ceoCls:'courier',life:2400};
function bmoAll(){return S.bmo=S.bmo||[]}
function bmoKeyOk(k,P){return P&&k&&(k===pkeyOf(P)||(isMe(k)&&P===S.player))}
function bmoClientName(by){return by.startsWith('corp_')?(MAKERS[by.slice(5)]||{}).name||'a maker':FACTIONS[by]?FACTIONS[by].name:sideName(by)}
function bmoClientW(by){return by.startsWith('corp_')?ceW(by.slice(5)):by}
// ---- CEOs and their shuttles
function ceoName(m){const c=ceOf(m);if(!c)return'the CEO';if(!c.ceoName||c.ceoNameT!==c.ceoT){c.ceoName=pick(IND_FIRST)+' '+pick(IND_LAST);c.ceoNameT=c.ceoT}return c.ceoName}
function ceoShuttle(m){return(S.traders||[]).find(t=>t.ceo&&t.ceo.m===m)||null}
function ceoLaunch(m){const R0=mkAtHome(m);if(!R0)return null;const fps=FREEPORTS.map(f=>f.sid).filter(s=>S.stations[s]&&s!==R0.sid&&HOP[R0.sid][s]!=null).sort((a,b)=>HOP[R0.sid][a]-HOP[R0.sid][b]);if(!fps.length)return null;
  const to=fps[0],path=trPath(R0.sid,to).concat(trPath(to,R0.sid).slice(1));if(path.length<3)return null;const name=ceoName(m);
  const t={id:S.nextId++,side:syfSide(R0),kind:'haul',key:'ceo:'+m,why:`${MAKERS[m].short} CEO`,car:null,item:null,n:0,from:R0.sid,to:R0.sid,path,leg:0,sector:R0.sid,next:S.T+TRADER_HOP*.5,load:{},cls:BMO.ceoCls,T0:S.T,ceo:{m,name,fp:to}};
  (S.traders=S.traders||[]).push(t);if(WORLDS[t.sector])inW(WORLDS[t.sector],()=>spawnTrader(t,false));return t}
// a rival: the maker selling most in the same kinds of part, else any other
function bmoRival(m){let best=null,bv=-1;const mine=new Set((MK_LINE[m]||[]).map(ceKind));for(const x in MAKERS){if(x===m||!ceAlive(x))continue;let v=0;for(const id of MK_LINE[x]||[])if(mine.has(ceKind(id)))v++;v+=Math.random()*.5;if(v>bv){bv=v;best=x}}return best}
function bmoTick(){if(NET.cl||!S||S.training||S.unb||!S.econ)return;const T=S.T;if(T<(S.bmoT||0))return;S.bmoT=T+BMO.every;const L=bmoAll();
  for(let i=L.length-1;i>=0;i--){const x=L[i];let gone=T>x.until;if(x.k==='kill'){const Ld=leaderOf(x.tgt);if(!Ld||!Ld.ship||!Ld.ship.alive||!warWith(x.by,x.tgt))gone=true}if(x.k==='ceo'&&!(S.traders||[]).some(t=>t.id===x.tid))gone=true;if(gone)L.splice(i,1)}
  // leaders: a power at war posts on its enemy's leader
  if(S.leaders)for(const f of FAC_IDS)for(const g of FAC_IDS){if(f===g||!warWith(f,g))continue;const Ld=leaderOf(g);if(!Ld||!Ld.ship||!Ld.ship.alive||L.some(x=>x.k==='kill'&&x.tgt===g))continue;
    if((S.econ.treasury[f]||0)<BMO.kill*2)continue;L.push({id:S.nextId++,k:'kill',by:f,tgt:g,pay:BMO.kill,T0:T,until:T+BMO.life,taker:null})}
  // CEOs: a shuttle now and then; a rival posts on it while it flies
  S.ceoT=S.ceoT||{};if(S.corp)for(const m in MAKERS){if(!ceAlive(m)||!mkAtHome(m))continue;if(S.ceoT[m]==null)S.ceoT[m]=T+rnd(...BMO.ceoEvery);if(T<S.ceoT[m]||ceoShuttle(m))continue;S.ceoT[m]=T+rnd(...BMO.ceoEvery);
    const t=ceoLaunch(m);if(!t)continue;const r=bmoRival(m);if(r&&ceT(r)>=BMO.ceo*1.5)L.push({id:S.nextId++,k:'ceo',by:'corp_'+r,tgt:m,tid:t.id,pay:BMO.ceo,T0:T,until:T+BMO.life,taker:null})}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{bmoTick()}catch(e){console.error(e)}return r}}
// the shuttle's label, and it is no convoy for the powers' escorts (nor a maker's escort job)
{const o=shipLabel;shipLabel=function(e){const t=e&&e.tradeT;if(t&&t.ceo&&MAKERS[t.ceo.m])return`${MAKERS[t.ceo.m].short} CEO ${t.ceo.name} · shuttle`;return o.apply(this,arguments)}}
// ---- the work done
function bmoPay(x,k,P){const w=bmoClientW(x.by),got=payKey(k,w,x.pay);bmoAll().splice(bmoAll().indexOf(x),1);return got}
function bmoKillerKey(src,at){const a=at&&at.src;if(a&&a.rp)return a.rp;if(a&&a.isPlayer)return pkeyOf(S.player);if(src==='player')return pkeyOf(S.player);return null}
{const o=killShip;killShip=function(e,src,at){let pre=null;try{if(e&&!NET.cl){if(e.leaderOf)pre={k:'kill',f:e.leaderOf};else if(e.tradeT&&e.tradeT.ceo)pre={k:'ceo',t:e.tradeT}}}catch(err){}
  const r=o.apply(this,arguments);
  try{if(pre){const key=bmoKillerKey(src,at),P=key?xPilotOfKey(key):null;
    if(pre.k==='kill'){const x=bmoAll().find(y=>y.k==='kill'&&y.tgt===pre.f&&y.taker&&key&&(y.taker===key||(isMe(y.taker)&&isMe(key))));if(x&&P){const got=bmoPay(x,key,P);smHeat(P,pre.f,SM.heat.Severe,'an assassination');keyFeed(key,`🗡 Contract done: ${bmoClientName(x.by)} pays +${fmt(got)} cr. ${FACTIONS[pre.f].short} will not forget it (Severe heat).`,'good')}}
    if(pre.k==='ceo'){const t=pre.t,m=t.ceo.m,c=ceOf(m);if(c&&!c.dead){const old=c.ceo;c.ceo=pick(CE.ceos.filter(z=>z!==old));c.ceoT=S.T;c.ceoHit=S.T+3600;ceNews(m,`'s CEO ${t.ceo.name} was killed when the company shuttle was shot down. The board names a new CEO (${c.ceo}).`,true)}
      const x=bmoAll().find(y=>y.k==='ceo'&&y.tid===t.id);if(x&&x.taker&&key&&(x.taker===key||(isMe(x.taker)&&isMe(key)))&&P){const got=bmoPay(x,key,P);const sd=sideNorm(t.side);if(FAC_IDS.includes(sd))smHeat(P,sd,SM.heat.Heavy,'a killing in its space');keyFeed(key,`🗡 Contract done: ${bmoClientName(x.by)} pays +${fmt(got)} cr.`,'good')}}}}catch(err){console.error(err)}return r}}
// the knock to the share price at the next valuation
{const o=ceHour;ceHour=function(){const r=o.apply(this,arguments);try{for(const m in MAKERS){const c=ceOf(m);if(c&&!c.dead&&c.ceoHit&&S.T<=c.ceoHit){c.px*=.9;if(c.pxH&&c.pxH.length)c.pxH[c.pxH.length-1]=Math.round(c.px*10)/10;c.ceoHit=0}}}catch(e){console.error(e)}return r}}
// ---- taking a contract
function bmoTake(P,id){const x=bmoAll().find(y=>String(y.id)===String(id));if(!x)return'That contract is gone.';if(x.taker&&!bmoKeyOk(x.taker,P))return'Someone else has taken it.';x.taker=pkeyOf(P);
  if(x.k==='kill'){const Ld=leaderOf(x.tgt);if(Ld&&Ld.ship&&Ld.ship.sid&&Ld.ship.sid!==P.sector)P.route=Ld.ship.sid;return`✓ Contract taken: ${lName(x.tgt)} of ${FACTIONS[x.tgt].short}. ${bmoClientName(x.by)} pays ${fmt(x.pay)} cr when the flagship goes down to your guns.`}
  const t=(S.traders||[]).find(z=>z.id===x.tid);if(t&&t.sector!==P.sector)P.route=t.sector;return`✓ Contract taken: ${MAKERS[x.tgt].short}'s CEO ${t?t.ceo.name:''}. ${bmoClientName(x.by)} pays ${fmt(x.pay)} cr when the shuttle goes down to your guns.`}
{const o=dockAction;dockAction=function(act,arg){if(act==='bmotake'){if(NET.cl)return o.apply(this,arguments);dockErr=bmoTake(S.player,arg);return}return o.apply(this,arguments)}}
// ---- the board (Jobs → Black market)
{const o=jobsList;jobsList=function(c,P,srcs){const out=o.apply(this,arguments);try{if(S.unb||!c||c.kind!=='station')return out;const me=pkeyOf(P),hop=sid=>sid&&HOP[P.sector]&&HOP[P.sector][sid]!=null?HOP[P.sector][sid]:0,far=n=>n?`${n} jump${n>1?'s':''}`:'here';
  // CEO shuttles are no one's convoy to escort
  for(let i=out.length-1;i>=0;i--){const id=String(out[i].id);if(id.startsWith('ce:')||id.startsWith('mfe:')){const tid=id.split(':')[1],t=(S.traders||[]).find(z=>String(z.id)===tid);if(t&&t.ceo)out.splice(i,1)}}
  for(const x of bmoAll()){const mine=x.taker&&bmoKeyOk(x.taker,P);if(x.taker&&!mine)continue;let sid=null,title='',sub='',det='';
    if(x.k==='kill'){const Ld=leaderOf(x.tgt);sid=Ld&&Ld.ship&&Ld.ship.sid;title=`Assassinate ${esc(lName(x.tgt))} of ${esc(FACTIONS[x.tgt].short)}`;sub=`for ${esc(bmoClientName(x.by))} · flagship in ${sid?esc(DEF[sid].name):'?'} · Severe heat with ${esc(FACTIONS[x.tgt].short)}`;
      det=`${esc(bmoClientName(x.by))} is at war with ${esc(FACTIONS[x.tgt].name)} and wants its leader dead. The flagship flies with an ace escort. Shoot it down after taking the contract: ${fmt(x.pay)} cr from the client, on top of any bounty. ${esc(FACTIONS[x.tgt].short)} will hunt you for it.`}
    else{const t=(S.traders||[]).find(z=>z.id===x.tid);if(!t)continue;sid=t.sector;title=`Assassinate ${esc(MAKERS[x.tgt].short)}'s CEO ${esc(t.ceo.name)}`;sub=`for ${esc(bmoClientName(x.by))} · shuttle now in ${esc(DEF[sid].name)}, bound for ${esc(DEF[t.ceo.fp].name)} and back`;
      det=`${esc(bmoClientName(x.by))} wants its rival's CEO gone. The CEO flies a light shuttle from the works at ${esc(DEF[t.from].name)} to ${esc(DEF[t.ceo.fp].name)} and back. Shoot it down after taking the contract: ${fmt(x.pay)} cr. The maker gets a new CEO and its shares take a knock.`}
    const h=hop(sid);out.push({id:'bk:'+x.id,bm:1,by:x.by,sid,ty:'fight',title,sub:mine?`your contract · ${sub}`:sub,hops:h,where:sid?far(h):'?',payN:x.pay,pay:`${fmt(x.pay)} cr`,btn:mine?(sid&&sid!==P.sector?['croute',sid,'Set course']:null):['bmotake',x.id,'Take the contract'],detail:()=>`<p class="note" style="margin:0">${det}</p>`})}}catch(err){console.error(err)}return out}}
// a shuttle lost is no supply convoy (no convoy news, no spilled cargo: it carries none)
{const o=traderLost;traderLost=function(e){try{const id=e&&e.home&&e.home.split(':')[1],t=(S.traders||[]).find(x=>String(x.id)===id);if(t&&t.ceo){S.traders=S.traders.filter(x=>x!==t);return}}catch(err){console.error(err)}return o.apply(this,arguments)}}
// (the caller takes it off the trader list)
{const o=haulLost;haulLost=function(t){if(t&&t.ceo){t.load={};return}return o.apply(this,arguments)}}
