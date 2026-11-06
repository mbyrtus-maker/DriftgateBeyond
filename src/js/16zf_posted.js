//@src 16zf_posted.js
// ============================================================ posting jobs to other pilots, with bidding (Beyond section 9, 3 Nov 2026)
// The Post jobs tab gains jobs for pilots who aren't yours: the Compact's contractors and the pilots of the powers that deal
// with you (in multiplayer, the other players too). Four kinds, each for one of your depots:
//   Supply: bring N of a good to the depot (the taker buys it at the nearest market that has it, at your expense);
//   Haul:   sell N of a good from the depot's store at the nearest market that deals with you (the proceeds are yours);
//   Mine:   cut N t of ore from the depot's system into its store;
//   Guard:  stand guard over the depot for 20 minutes (its guns +50%).
// The fee is a bid against the galactic mean for that kind of job, its distance and risk: Low (75%, the floor) waits longest
// for a taker, Medium (the mean) normal, Fast (140%) soonest; you can't bid above 200%. The wait before an AI pilot signs on
// is 3 minutes × (mean ÷ bid)². In multiplayer another player can do a Supply job first: dock at the depot with the goods.
// The fee is paid on completion to whoever did it (the Compact, the power whose pilot it was, or the player); goods only move.
const PJB={kinds:{supply:'Supply',haul:'Haul',mine:'Mine',guard:'Guard'},bids:{low:.75,medium:1,fast:1.4},max:2,wait:180,guardT:1200,guardK:.5,max_open:6,run:[90,40]};
function pjMean(kind,R,item,n){const prem=pjPrem();if(kind==='guard')return Math.round(900*(1+.5*pjThreat(R)));if(kind==='mine')return Math.max(120,Math.round(n*4*prem*1.4));
  const v=baseValue(item)*n,h=pjHops(R,item,kind);return Math.max(150,Math.round(v*prem*(.5+.12*h)+mass(item)*n*1.5))}
// the premium the powers' and the Compact's own jobs pay over the goods' value, across the galaxy now
function pjPrem(){const L=(S.contracts||[]).filter(k=>k.item&&ITEMS[k.item]&&k.n>0);if(!L.length)return .8;let a=0;for(const k of L)a+=clamp(k.reward/(baseValue(k.item)*k.n)-1,.2,2);return clamp(a/L.length,.3,1.5)}
function pjThreat(R){const fs=FAC_IDS.filter(f=>(HOP[R.sid]||{})[FAC_HOME(f)]!=null&&HOP[R.sid][FAC_HOME(f)]<=3).length;return fs+((S.stations[R.sid]&&broodHeld&&NEIGH[R.sid].some(s=>broodHeld(s)))?1:0)}
function pjSrc(R,item,kind,P){let best=null,bh=99;const deal=kind==='haul'?depTraders(P):[...depTraders(P),'neutral'];for(const id in S.stations){const D=S.stations[id];if(!D||D===R||!deal.includes(D.owner))continue;if(kind==='supply'&&(mkStock(D)[item]||0)<1)continue;const h=HOP[R.sid]&&HOP[R.sid][id];if(h!=null&&h<bh){bh=h;best=D}}return best?{D:best,h:bh}:null}
function pjHops(R,item,kind){const s=pjSrc(R,item,kind,S.player);return s?s.h:4}
function pjList(){return S.pj=S.pj||[]}
function pjPost(P,arg){const[sid,kind,item,nS,bidS]=String(arg).split(':'),R=S.stations[sid],n=Math.max(1,Math.min(500,+nS||0));if(!R||R.owner!=='player'||(R.pid||'me')!==pkeyOf(P))return'Not your depot.';if(!PJB.kinds[kind])return'No such job.';
  if(kind!=='guard'&&kind!=='mine'&&!ITEMS[item])return'Pick a good.';const k=pkeyOf(P);if(pjList().filter(j=>j.pid===k&&j.state!=='done').length>=PJB.max_open)return`You have ${PJB.max_open} jobs posted already.`;
  if(kind==='haul'&&(R.stock[item]||0)<n)return`The store has only ${R.stock[item]||0} ${ITEMS[item].name}.`;if(kind==='mine'&&!S.sectors[sid].ast.some(a=>!a.rift&&!a.comet&&oreTotal(a)>0))return'No rock left in that system.';
  const mean=pjMean(kind,R,item,n),bid=PJB.bids[bidS]?Math.round(mean*PJB.bids[bidS]):Math.round(clamp(+bidS||0,mean*PJB.bids.low,mean*PJB.max));if(P.credits<bid)return`The fee is ${fmt(bid)} cr: you have ${fmt(P.credits)} cr.`;
  const j={id:S.nextId++,pid:k,sid,kind,item:kind==='guard'?null:kind==='mine'?'ore':item,n:kind==='guard'?0:n,mean,bid,posted:S.T,claimAt:S.T+PJB.wait*Math.pow(mean/bid,2),state:'open'};pjList().push(j);
  return`✓ Posted: ${pjTitle(j)} for ${fmt(bid)} cr (${Math.round(bid/mean*100)}% of the galactic mean of ${fmt(mean)} cr). A taker should sign on in about ${fmtT(j.claimAt-S.T)}.`}
function pjTitle(j){const R=S.stations[j.sid],nm=R?R.name:DEF[j.sid].name;return j.kind==='supply'?`Bring ${j.n} ${ITEMS[j.item].name} to ${nm}`:j.kind==='haul'?`Sell ${j.n} ${ITEMS[j.item].name} from ${nm}`:j.kind==='mine'?`Mine ${j.n} t of ore for ${nm}`:`Guard ${nm} for ${PJB.guardT/60} minutes`}
// AI takers sign on when the wait is over, then do the job abstractly
function pjTick(){if(NET.cl||!S||S.unb)return;for(const j of pjList()){const R=S.stations[j.sid],P=xPilotOfKey(j.pid);if(j.state==='done')continue;
    if(!R||R.owner!=='player'||!P){j.state='done';j.msg='cancelled: the depot is gone';continue}
    if(j.state==='open'&&S.T>=j.claimAt){const fs=depTraders(P),by=Math.random()<.5||!fs.length?'neutral':pick(fs);j.by=by;j.who=by==='neutral'?'a Compact contractor':`${/^[AEIOU]/.test(FACTIONS[by].short)?'an':'a'} ${FACTIONS[by].short} pilot`;j.state='taken';
      const h=j.kind==='guard'?0:j.kind==='mine'?1:pjHops(R,j.item,j.kind);j.due=S.T+(j.kind==='guard'?PJB.guardT:PJB.run[0]+PJB.run[1]*h);keyFeed(j.pid,`📋 ${j.who} took your job: ${pjTitle(j)}.`,'info')}
    else if(j.state==='taken'&&S.T>=j.due)pjFinish(j,R,P)}
  const done=pjList().filter(j=>j.state==='done');if(done.length>30)S.pj=pjList().filter(j=>j.state!=='done'||done.indexOf(j)>=done.length-30)}
function pjFinish(j,R,P){let note='';
  if(j.kind==='supply'){const s=pjSrc(R,j.item,'supply',P);let n=0;if(s){const mk=mkStock(s.D),pr=Math.ceil(stPrice(s.D,j.item));n=Math.min(j.n,mk[j.item]||0,Math.floor(P.credits/pr));if(n>0){inv.take(mk,j.item,n);inv.add(R.stock,j.item,n);payFrom(P,s.D.owner,n*pr);eco(R,'jobs',-n*pr,`${n} ${ITEMS[j.item].name} bought at ${s.D.name}`)}}note=` ${n} of ${j.n} brought in`}
  if(j.kind==='haul'){const s=pjSrc(R,j.item,'haul',P);let n=0,got=0;if(s){const mk=mkStock(s.D),f=s.D.owner,pr=Math.max(1,Math.floor(stPrice(s.D,j.item)*.95));n=Math.min(j.n,R.stock[j.item]||0,Math.floor((S.econ.treasury[f]||0)/pr));if(n>0){inv.take(R.stock,j.item,n);inv.add(mk,j.item,n);got=payTo(P,f,n*pr);eco(R,'jobs',got,`${n} ${ITEMS[j.item].name} sold at ${s.D.name}`)}}note=` ${n} sold for ${fmt(got)} cr`}
  if(j.kind==='mine'){const s=S.sectors[j.sid];let want=j.n,got=0;for(const a of s.ast.filter(x=>!x.rift&&!x.comet&&oreTotal(x)>0)){if(want<=0)break;while(want>0&&oreTotal(a)>0){const q=mainOre(a);inv.take(a.ore,q,1);inv.add(R.stock,q,1);want--;got++}if(oreTotal(a)<=0)removeAst(s,a)}note=` ${got} t cut`}
  const fee=payFrom(P,j.by,Math.min(j.bid,P.credits));eco(R,'jobs',-fee,`${j.who}'s fee`);j.state='done';j.paid=fee;j.msg=`done by ${j.who}:${note}${note?',':''} paid ${fmt(fee)} cr`;keyFeed(j.pid,`📋 ${pjTitle(j)}: ${j.msg}.`,'good')}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{pjTick()}catch(err){console.error(err)}return r}}
// a guarded depot's guns
{const o=depGunK;depGunK=function(SE,t){const v=o.apply(this,arguments);const R=SE&&SE.rec;if(R&&R.owner==='player'&&pjList().some(j=>j.sid===R.sid&&j.kind==='guard'&&j.state==='taken'))return v*(1+PJB.guardK);return v}}
// in multiplayer, another player can do a Supply job: dock at the depot with the goods
{const o=jobsList;jobsList=function(c,P,srcs){const out=o.apply(this,arguments);try{if(S.unb||!c||c.kind!=='station')return out;const me=pkeyOf(P);
  for(const j of pjList().filter(j=>j.kind==='supply'&&j.state==='open'&&j.pid!==me&&j.sid===P.sector)){const O=xPilotOfKey(j.pid),have=Math.min(j.n,P.cargo[j.item]||0);
    out.push({id:'pj:'+j.id,by:'player',sid:j.sid,ty:'haul',title:`${esc((O&&O.name)||'A contractor')} posts: ${j.n} ${esc(ITEMS[j.item].name)}`,sub:have?`You can deliver ${have} now`:`You carry none`,ok:have>0,hops:0,where:'here',payN:j.bid,pay:`${fmt(j.bid)} cr`,btn:have?['pjdo',j.id,`Deliver ${have} · +${fmt(Math.round(j.bid*have/j.n))} cr`]:null,
      detail:()=>`<p class="note" style="margin:0">A job posted by another company: the goods go into its depot's store and it pays its bid.</p>`})}}catch(err){console.error(err)}return out}}
function pjDo(P,id){const j=pjList().find(x=>String(x.id)===String(id)&&x.state==='open'&&x.kind==='supply');if(!j)return'That job is gone.';const R=S.stations[j.sid],O=xPilotOfKey(j.pid);if(!R||P.sector!==j.sid||P.docked!=='station')return'Dock at that depot.';
  const n=Math.min(j.n,P.cargo[j.item]||0);if(!n)return`You carry no ${ITEMS[j.item].name}.`;const fee=Math.min(Math.round(j.bid*n/j.n),O.credits);inv.take(P.cargo,j.item,n);inv.add(R.stock,j.item,n);
  let got=0;if(O!==P){got=payFrom(O,'neutral',fee);payTo(P,'neutral',got)}eco(R,'jobs',-got,`${P.name||'a contractor'} brought ${n} ${ITEMS[j.item].name}`);
  j.n-=n;j.bid-=Math.round(j.bid*n/(j.n+n));if(j.n<=0){j.state='done';j.who=P.name||'a contractor';j.paid=got;j.msg=`done by ${j.who}: paid ${fmt(got)} cr`}keyFeed(j.pid,`📋 ${P.name||'A contractor'} brought ${n} ${ITEMS[j.item].name} to ${R.name}: −${fmt(got)} cr.`,'info');return`✓ Delivered ${n} ${ITEMS[j.item].name}: +${fmt(got)} cr.`}
function pjCancel(P,id){const j=pjList().find(x=>String(x.id)===String(id)&&x.pid===pkeyOf(P)&&x.state==='open');if(!j)return'Only an open job can be withdrawn.';j.state='done';j.msg='withdrawn';return'✓ Job withdrawn.'}
{const o=dockAction;dockAction=function(act,arg){const P=S.player;if(act==='pjpost'){dockErr=pjPost(P,arg);return}if(act==='pjdo'){dockErr=pjDo(P,arg);return}if(act==='pjcancel'){dockErr=pjCancel(P,arg);return}return o.apply(this,arguments)}}
// ---- the Post jobs tab: a form per depot, the bids, and your posted jobs
let pjForm={kind:'supply',item:'plate',n:20,bid:'medium'};
{const o=coClick;coClick=function(act,arg){if(act==='pjf'){const[k,v]=String(arg).split(':');pjForm[k]=k==='n'?Math.max(1,(pjForm.n||0)+(+v)):v;renderCompany();return}
  if(['pjpost','pjcancel'].includes(act)){if(NET.cl){netSend({t:'act',act,arg});coErr='Working…';renderCompany();return}dockAction(act,arg);coErr=dockErr;renderCompany();return}return o.apply(this,arguments)}}
{const o=crewsHtml;crewsHtml=function(P){let h=o.apply(this,arguments);try{h+=pjHtml(P)}catch(err){console.error(err)}return h}}
function pjHtml(P){const D=myDepots(P);let h=`<div class="h3" style="margin-top:18px">Jobs for other pilots</div><p class="note" style="margin:0 0 8px">Post work to the Compact's contractors and the pilots of the powers that deal with you (and, in multiplayer, the other players). The fee is your bid against the galactic mean for that job: Low (75%) waits longest for a taker, Fast (140%) the least; it's paid when the job is done.</p>`;
  if(!D.length)return h+'<div class="note">Posting jobs needs a Depot.</div>';const F=pjForm,goods=['fe','cu','ir','au','nu','xc','plate','wire','coil','lattice','frame'].filter(k=>ITEMS[k]);
  h+=`<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:6px">${Object.entries(PJB.kinds).map(([k,n])=>`<button class="btn sm${F.kind===k?' pri':''}" type="button" data-co="pjf" data-arg="kind:${k}">${n}</button>`).join('')}</div>`;
  if(F.kind==='supply'||F.kind==='haul')h+=`<div style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:6px">${goods.map(k=>`<button class="btn sm${F.item===k?' pri':''}" type="button" data-co="pjf" data-arg="item:${k}">${esc(ITEMS[k].name)}</button>`).join('')}</div>`;
  if(F.kind!=='guard')h+=`<div style="display:flex;gap:6px;align-items:center;margin-bottom:6px"><span class="note" style="margin:0">${F.kind==='mine'?'Tonnes':'Amount'}:</span>${[-10,-1].map(d=>`<button class="btn sm" type="button" data-co="pjf" data-arg="n:${d}">${d}</button>`).join('')}<b>${F.n}</b>${[1,10].map(d=>`<button class="btn sm" type="button" data-co="pjf" data-arg="n:${d}">+${d}</button>`).join('')}</div>`;
  h+=`<div style="display:flex;gap:6px;align-items:center;margin-bottom:6px"><span class="note" style="margin:0">Bid:</span>${Object.keys(PJB.bids).map(b=>`<button class="btn sm${F.bid===b?' pri':''}" type="button" data-co="pjf" data-arg="bid:${b}">${b[0].toUpperCase()+b.slice(1)} · ${Math.round(PJB.bids[b]*100)}%</button>`).join('')}</div>`;
  h+=`<div class="tblw"><table class="t"><tbody>${D.map(R=>{const mean=pjMean(F.kind,R,F.item,F.n),bid=Math.round(mean*(PJB.bids[F.bid]||1));return`<tr><td class="iname">${esc(R.name)}</td><td class="note">galactic mean ${fmt(mean)} cr · wait about ${fmtT(PJB.wait*Math.pow(mean/bid,2))}</td><td><button class="btn sm pri" type="button" data-co="pjpost" data-arg="${R.sid}:${F.kind}:${F.item}:${F.n}:${F.bid}" ${P.credits>=bid?'':'disabled'}>Post · ${fmt(bid)} cr</button></td></tr>`}).join('')}</tbody></table></div>`;
  const k=pkeyOf(P),L=pjList().filter(j=>j.pid===k).slice(-12).reverse();
  if(L.length)h+=`<div class="tblw" style="margin-top:8px"><table class="t"><thead><tr><th>Posted</th><th>Status</th><th class="r">Fee</th><th></th></tr></thead><tbody>${L.map(j=>`<tr><td class="iname" style="white-space:normal">${esc(pjTitle(j))}</td><td style="white-space:normal">${j.state==='open'?`waiting for a taker (${fmtT(Math.max(0,j.claimAt-S.T))})`:j.state==='taken'?`${esc(j.who)} on it · ${j.run&&typeof pjRunLine==='function'?esc(pjRunLine(j)):fmtT(Math.max(0,j.due-S.T))}`:esc(j.msg||'done')}</td><td class="r num">${fmt(j.state==='done'&&j.paid!=null?j.paid:j.bid)} cr</td><td>${j.state==='open'?`<button class="btn sm" type="button" data-co="pjcancel" data-arg="${j.id}">Withdraw</button>`:''}</td></tr>`).join('')}</tbody></table></div>`;
  return h}
