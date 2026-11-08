//@src 16zzzf_sysfreight.js
// ============================================================ Beyond: makers' goods seek buyers, by haul job (user, 8 Nov 2026)
// Morning: the user found no systems on the markets ("Makers ship them" agreed). Midday, the user's design check: "R&D
// stages should be jobs. All parts made by makers should seek buyers. Haul jobs should be made." (BEYOND_DESIGN.md, "Makers'
// parts seek buyers; freight and materials are haul jobs; named test pilots").
//   - Shelves: a maker keeps one of each of its lines on the shelves it serves (a power's maker: its power's core station and
//     the freeports for every line, its power's other stations for its systems; a freeport maker: the freeports and each
//     power's core station), two where the line sold at that shelf in the last hour. A shelf holding a line that hasn't sold
//     there in 2 hours sends one on to a shelf that lacks it (and doesn't ask for it again for 2 hours).
//   - Freight jobs: each shipment is posted on the source station's Jobs board, paid by the maker: 40 cr + 15 a jump + 4% of
//     the goods' value. Taking one loads the goods into your hold and puts their value in escrow from your credits; Deliver
//     at the destination's Jobs board pays you and returns the collateral (pro rata for part of a load). Deadline: 5 minutes
//     + 4 a jump; miss it, or lose the goods, and the maker keeps the collateral. Supply runs (components bought at another
//     market for the maker's works) and R&D materials are freight jobs too: the maker buys the goods there as you take them.
//   - A job nobody takes in 5 minutes is flown by the maker's own freighter under its home's colours (the maker pays the
//     carrier the same fee), a real convoy listed for escort on the boards within 3 jumps (the maker pays 60% of a power's
//     escort rate).
//   - R&D: after design, the prototype's components are bought at the nearest other market that has them all (else made at
//     home as before) and hauled to the works as a materials job. Trials: a named test pilot flies the prototype two jumps
//     out and home in a hull that suits it; back home, the line launches; shot down, the prototype is lost and the project
//     goes back to materials. The flight can be escorted.
//   - A maker ships, and buys for its works, only while it holds 1,500 cr above its reserve. A maker's payload bay line
//     starts at grade 2 (a grade 1 bay is built into every hull).
// Host only; the ledger stays exact (goods move between stores, holds and freighters; credits between wallets and escrow).
const SYF={every:[90,150],load:4,tgt:1,fee:40,hop:15,val:.04,res:8,inMax:12,cushion:1500,wait:300,due:[300,240],esc:.6,stale:7200,outMax:2};
function syfAll(m){return(MK_LINE[m]||[]).filter(id=>ITEMS[id])}
function syfLines(m){return syfAll(m).filter(id=>ITEMS[id].sys)}
function syfGid(m,id){const g=rdGid(id,rdLineG(m,id));return ITEMS[g]&&Object.keys(ITEMS[g].recipe).length?g:null}
function syfHave(st,id){let n=0;for(let g=1;g<=5;g++)n+=st[rdGid(id,g)]||0;return n}
function syfSide(R){return R.owner==='neutral'?'neutral':R.owner}
function syfOk(R){return!!R&&R.sid!==WRACK.sid&&(R.owner==='neutral'&&isFreeF(R)||FAC_IDS.includes(R.owner))}
function syfHub(R){return isFreeF(R)||R.kind==='core'}
// does maker m keep line id on shelf R
function syfServes(m,R,id){const R0=mkAtHome(m);if(!R0||!syfOk(R)||R===R0||!HOP[R0.sid]||HOP[R0.sid][R.sid]==null)return false;const h=MAKERS[m].home,fac=FAC_IDS.includes(h);
  if(R.owner==='neutral')return true;if(fac)return R.owner===h&&(R.kind==='core'||!!ITEMS[id].sys);return R.kind==='core'}
function syfDests(m){const R0=mkAtHome(m);if(!R0)return[];return Object.values(S.stations).filter(R=>syfOk(R)&&R!==R0&&HOP[R0.sid]&&HOP[R0.sid][R.sid]!=null)}
function syfSoldAt(m,id,sid,span){const c=ceOf(m);let n=0;if(c)for(const x of c.sales)if(x[1]===id&&x[4]===sid&&x[0]>S.T-span)n+=x[2];return n}
function syfCold(sid,id){return((S.syf&&S.syf.cold||{})[sid+'|'+id]||0)>S.T}
function syfTgt(m,R,id){if(!syfServes(m,R,id)||syfCold(R.sid,id))return 0;return SYF.tgt+(syfSoldAt(m,id,R.sid,3600)>0?1:0)}
// how many more of a line the shelves a maker serves still lack (cached per tick; the home works build for them too)
let SYF_W={t:-1,S:null,w:{}};
function syfWant(m,id){if(!S||!ITEMS[id]||!MAKERS[m])return 0;if(SYF_W.t!==S.T||SYF_W.S!==S)SYF_W={t:S.T,S,w:{}};const k=m+'|'+id;
  if(SYF_W.w[k]===undefined){let n=0;try{for(const R of syfDests(m))n+=Math.max(0,syfTgt(m,R,id)-syfHave(mkStock(R),id))}catch(e){}SYF_W.w[k]=Math.min(SYF.load,n)}return SYF_W.w[k]}
// ---- the jobs
function mfjAll(){return S.mfj=S.mfj||[]}
function mfjW(j){return'mfj_'+j.id}
function mfjPay(j){return Math.round(SYF.fee+SYF.hop*j.hops+invValue(j.load)*SYF.val)}
function mfjVal(j){return Math.ceil(invValue(j.load))}
function mfjCount(m,k){return mfjAll().filter(j=>j.m===m&&j.k===k).length+(S.traders||[]).filter(t=>t.syf&&t.syf.m===m&&t.syf.k===k).length}
function mfjPost(m,k,from,to,load,buy,extra){const h=HOP[from]&&HOP[from][to]!=null?HOP[from][to]:0;const j=Object.assign({id:S.nextId++,m,k,from,to,load,buy:!!buy,hops:h,T0:S.T,st:'open'},extra||{});j.pay=mfjPay(j);mfjAll().push(j);return j}
function mfjDrop(j){S.mfj=mfjAll().filter(x=>x!==j);const w=mfjW(j);if(S.econ.treasury[w]===0)delete S.econ.treasury[w]}
function mfjWhat(j){const ks=Object.keys(j.load);const n=ks.reduce((a,k)=>a+j.load[k],0);return ks.length===1?`${j.load[ks[0]]} ${ITEMS[ks[0]].name}`:`${n} ${j.k==='out'?'parts':'goods'}`}
function mfjTitle(j){const mk=MAKERS[j.m]?MAKERS[j.m].short:'a maker',R=S.stations[j.to],to=R?R.name:DEF[j.to].name;
  return j.k==='mat'?`R&D materials for ${mk}: ${mfjWhat(j)} to its works at ${to}`:j.k==='in'?`Supplies for ${mk}: ${mfjWhat(j)} to its works at ${to}`:`Freight for ${mk}: ${mfjWhat(j)} to ${to}`}
// the goods a job's source can still hand over (all or nothing)
function mfjReady(j){const R=S.stations[j.from];if(!syfOk(R))return false;const st=mkStock(R);for(const k in j.load)if((st[k]||0)<j.load[k])return false;return true}
function mfjCost(j){const R=S.stations[j.from];let c=0;if(j.buy)for(const k in j.load)c+=Math.ceil(stPrice(R,k)*j.load[k]);return c}
// take the goods off the source's shelf (buying them for the maker if it must); returns the load or null
function mfjLift(j,extra){const R=S.stations[j.from];if(!mfjReady(j))return null;const cost=mfjCost(j);if(cost+(extra||0)>0&&ceT(j.m)<cost+(extra||0))return null;
  const st=mkStock(R),load={};for(const k in j.load){const q=inv.take(st,k,j.load[k]);if(q>0)load[k]=q}if(cost){const paid=transfer(ceW(j.m),syfSide(R),cost);ceOf(j.m).cost+=paid}return load}
// where a delivered load goes: an out shipment onto the destination's market; supplies into the works' market; materials into the prototype
function mfjLand(m,k,to,load,rid){const c=ceOf(m);if(k==='mat'&&c&&c.rd&&c.rd.mj===rid){inv.addAll(c.rd.proto,load);c.rd.got=1;c.rd.mj=null;c.rd.stage='trials';c.rd.until=S.T+1e7;return}
  const R=S.stations[to];let into=syfOk(R)?mkStock(R):null;if(!into){const H=mkAtHome(m);into=H?mkStock(H):(S.econ.stock.neutral||S.econ.stock.pirate)}inv.addAll(into,load)}
// a job untaken for 5 minutes goes by the maker's own freighter
function mfjNpc(j){const R=S.stations[j.from],R0=mkAtHome(j.m);if(!R||!R0)return false;const fee=mfjPay(j);if(ceT(j.m)<fee+mfjCost(j))return false;
  const load=mfjLift(j,fee);if(!load||!Object.keys(load).length)return false;const t=haulSend(syfSide(R0),j.from,j.to,load,'syf:'+j.m,j.k==='out'?`${MAKERS[j.m].short} parts`:j.k==='mat'?`${MAKERS[j.m].short} R&D materials`:`${MAKERS[j.m].short} supplies`,null);
  if(!t){inv.addAll(mkStock(R),load);return false}t.syf={m:j.m,k:j.k,rid:j.rid||null};const paid=transfer(ceW(j.m),syfSide(R0),fee);ceOf(j.m).cost+=paid;return true}
function mfjTick(){for(const j of mfjAll().slice()){
  if(j.st==='open'&&S.T>=j.T0+SYF.wait){if(!ceAlive(j.m)||!mfjReady(j)){mfjFailed(j);mfjDrop(j);continue}if(mfjNpc(j))mfjDrop(j);continue}
  if(j.st==='taken'&&S.T>j.due){const P=xPilotOfKey(j.pk),paid=transfer(mfjW(j),ceW(j.m),S.econ.treasury[mfjW(j)]||0);
    keyFeed(j.pk,`✖ Freight job lapsed: ${mfjTitle(j)}. ${MAKERS[j.m].short} keeps your ${fmt(paid)} cr collateral.`,'bad');if(P&&P.mfj===j.id)P.mfj=null;mfjFailed(j);mfjDrop(j)}}}
// a materials job that won't be done: the project posts it again
function mfjFailed(j){if(j.k!=='mat')return;const c=ceOf(j.m);if(c&&c.rd&&c.rd.mj===j.id)c.rd.mj=null}
function mfjTake(P,id){const j=mfjAll().find(x=>String(x.id)===String(id));if(!j||j.st!=='open')return'That job is gone.';if(P.mfj&&mfjAll().some(x=>x.id===P.mfj&&x.st==='taken'))return'You are already on a freight job.';
  if(P.docked!=='station'||P.sector!==j.from)return`Dock at ${S.stations[j.from]?S.stations[j.from].name:DEF[j.from].name} to load it.`;const D=S.stations[j.to];if(!D)return'Its destination is gone.';
  if(!tradeOK(P,D.owner))return`You can't trade at ${D.name}.`;const room=shipStats(P.faction,P.cls,P.tiers,P.tune).cargo-invMass(P.cargo),m=invMass(j.load);if(room<m)return`It needs ${m} t of hold space.`;
  const val=mfjVal(j);if(P.credits<val)return`It needs ${fmt(val)} cr collateral.`;if(!mfjReady(j))return'The goods aren\'t here any more.';const load=mfjLift(j);if(!load)return`${MAKERS[j.m].short} can't pay for the goods right now.`;
  inv.addAll(P.cargo,load);j.load=load;transfer('player',mfjW(j),val);j.coll=val;j.st='taken';j.pk=pkeyOf(P);j.who=P.name||'a pilot';j.due=S.T+SYF.due[0]+SYF.due[1]*j.hops;P.mfj=j.id;P.route=j.to;
  return`✓ Loaded ${mfjWhat(j)}. Deliver at ${D.name} within ${Math.round((j.due-S.T)/60)} min: ${fmt(j.pay)} cr and your ${fmt(val)} cr collateral back.`}
function mfjDeliver(P,id){const j=mfjAll().find(x=>String(x.id)===String(id));if(!j||j.st!=='taken'||j.pk!==pkeyOf(P))return'That job is gone.';if(P.docked!=='station'||P.sector!==j.to)return'Dock at its destination.';
  let tot=0,have=0;const got={};for(const k in j.load){tot+=j.load[k];const q=Math.min(j.load[k],P.cargo[k]||0);if(q>0){got[k]=q;have+=q}}if(!have)return'You carry none of its goods.';
  for(const k in got)inv.take(P.cargo,k,got[k]);mfjLand(j.m,j.k,j.to,got,j.id);const fr=have/tot,w=mfjW(j),esc=S.econ.treasury[w]||0,back=Math.min(esc,Math.round(j.coll*fr));
  const pay=transfer(ceW(j.m),'player',Math.round(j.pay*fr)),ret=transfer(w,'player',back);transfer(w,ceW(j.m),S.econ.treasury[w]||0);P.mfj=null;mfjDrop(j);
  try{rpAdd(P,RATING.k*(1+j.hops),'a freight job')}catch(e){}
  return`✓ Delivered ${have} of ${tot}. ${MAKERS[j.m].short} pays ${fmt(pay)} cr; ${fmt(ret)} cr collateral back.`}
// ---- planning: what to ship, buy or move
function syfPlanOut(m){const R0=mkAtHome(m);if(!R0)return null;const st0=mkStock(R0),st={...st0};let best=null;S.syf.seen=S.syf.seen||{};const pend={};
  for(const j of mfjAll())if(j.m===m&&j.k==='out'){for(const k in j.load){if(j.st==='open'&&j.from===R0.sid)st[k]=(st[k]||0)-j.load[k];const b=(ITEMS[k]&&ITEMS[k].base)||k;pend[j.to+'|'+b]=(pend[j.to+'|'+b]||0)+j.load[k]}}
  // the shelves' stale stock: a line unsold at a shelf for 2 hours is free to move on
  const stale=[];for(const R of syfDests(m)){const ss=mkStock(R);for(const id of syfAll(m)){const key=R.sid+'|'+id,n=syfHave(ss,id);if(!n){delete S.syf.seen[key];continue}if(!S.syf.seen[key])S.syf.seen[key]=S.T;
    if(S.T-S.syf.seen[key]>=SYF.stale&&!syfSoldAt(m,id,R.sid,SYF.stale)){let g=5;while(g>1&&!ss[rdGid(id,g)])g--;stale.push({R,id,gid:rdGid(id,g)})}}}
  for(const R of syfDests(m)){const ds=mkStock(R),want={};let n=0;
    for(const id of syfAll(m)){const gap=syfTgt(m,R,id)-syfHave(ds,id)-(pend[R.sid+'|'+id]||0);if(gap<=0)continue;const gid=syfGid(m,id);if(!gid)continue;const q=Math.min(gap,st[gid]||0);if(q>0){want[gid]=q;n+=q}}
    if(!n)continue;const h=HOP[R0.sid][R.sid],sc=n*100-h+(syfHub(R)?500:0);if(!best||sc>best.sc)best={from:R0.sid,R,want,sc}}
  if(best){const load={};let k=0;for(const gid in best.want){const q=Math.min(best.want[gid],SYF.load-k);if(q<=0)break;load[gid]=q;k+=q}return{from:best.from,to:best.R.sid,load}}
  for(const x of stale){const to=syfDests(m).filter(R=>R!==x.R&&syfTgt(m,R,x.id)>syfHave(mkStock(R),x.id)).sort((a,b)=>HOP[x.R.sid][a.sid]-HOP[x.R.sid][b.sid])[0];if(!to)continue;
    (S.syf.cold=S.syf.cold||{})[x.R.sid+'|'+x.id]=S.T+SYF.stale;delete S.syf.seen[x.R.sid+'|'+x.id];return{from:x.R.sid,to:to.sid,load:{[x.gid]:1}}}
  return null}
// what the works' next goods need that the home market hasn't got (a matrix, lattice or core counts as what it's made of)
function syfNeed(m){const R0=mkAtHome(m),st=mkStock(R0),need={};
  const add=(rc,x,d)=>{for(const k in rc){const q=rc[k]*x;if(RD_CRAFT.has(k)&&d<3&&ITEMS[k].recipe&&!(ITEMS[k].forge&&!rdForgeAt(R0))){const sh=q-(st[k]||0);if(sh>0)add(ITEMS[k].recipe,sh,d+1)}else need[k]=(need[k]||0)+q}};
  for(const id of syfAll(m)){const gid=syfGid(m,id);if(!gid)continue;const w=Math.min(CE.cap,CE.shelf+ceSold(m,id,3600)+syfWant(m,id))-(st[gid]||0);if(w<=0)continue;add(ITEMS[gid].recipe,Math.min(2,w),0)}
  for(const k in need){need[k]=Math.ceil(need[k]-(st[k]||0));if(need[k]<=0)delete need[k]}return need}
function syfSrcOk(R0,R){return syfOk(R)&&R!==R0&&HOP[R0.sid]&&HOP[R0.sid][R.sid]!=null&&mkStock(R)!==mkStock(R0)&&!(R.owner!=='neutral'&&R0.owner!=='neutral'&&R.owner!==R0.owner&&hostile(R0.owner,R.owner))}
function syfPlanIn(m){const R0=mkAtHome(m);if(!R0)return null;const need=syfNeed(m);if(!Object.keys(need).length)return null;let best=null;
  for(const R of Object.values(S.stations)){if(!syfSrcOk(R0,R))continue;const ss=mkStock(R),buy={};let n=0;for(const k in need){const q=Math.min(need[k],Math.floor((ss[k]||0)-SYF.res),SYF.inMax-n);if(q>0){buy[k]=q;n+=q}}
    if(!n)continue;const h=HOP[R0.sid][R.sid],sc=n*10-h;if(!best||sc>best.sc)best={from:R.sid,to:R0.sid,load:buy,sc}}return best}
function syfTick(){if(NET.cl||!S||S.training||S.unb||!rdOn())return;S.syf=S.syf||{};mfjTick();
  for(const m in MAKERS){if(!ceAlive(m)||!mkAtHome(m))continue;const A=S.syf[m]=S.syf[m]||{t:S.T+rnd(20,120)};if(S.T<A.t)continue;A.t=S.T+rnd(...SYF.every);
    try{const spare=ceT(m)-ceReserve(m)-SYF.cushion;if(spare<=0)continue;
      if(mfjCount(m,'out')<SYF.outMax){const p=syfPlanOut(m);if(p)mfjPost(m,'out',p.from,p.to,p.load,false)}
      if(mfjCount(m,'in')<1){const p=syfPlanIn(m);if(p){const j=mfjPost(m,'in',p.from,p.to,p.load,true);if(mfjCost(j)+j.pay>spare)mfjDrop(j)}}}catch(e){console.error(e)}}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{syfTick()}catch(e){console.error(e)}return r}}
// ---- R&D: materials by haul job, trials by a named test pilot
function rdMatStart(m){const c=ceOf(m),P=c.rd,R0=mkAtHome(m);if(!R0)return;const gid=rdGid(P.id,P.g),rc=ITEMS[gid].recipe;let best=null;
  for(const R of Object.values(S.stations)){if(!syfSrcOk(R0,R))continue;const ss=mkStock(R);if(!Object.keys(rc).every(k=>(ss[k]||0)>=rc[k]+(RD_CRAFT.has(k)?0:2)))continue;const h=HOP[R0.sid][R.sid];if(!best||h<best.h)best={R,h}}
  if(!best){P.mjT=S.T+1e7;return}
  const j=mfjPost(m,'mat',best.R.sid,R0.sid,{...rc},true);j.rid=j.id;P.mj=j.id;P.until=S.T+1e7}
const RD_FLY={gun:'striker',laser:'striker',missile:'striker',torpedo:'striker',weapon:'striker',mlaser:'prospector',charge:'prospector',drill:'prospector',cargo:'courier',scanner:'scout',dronec:'striker'};
function rdFlyStart(m){const c=ceOf(m),P=c.rd,R0=mkAtHome(m),gid=rdGid(P.id,P.g),I=ITEMS[gid];if(!R0||!I){rdLaunch(m);return}
  const rc=I.recipe;if(!haveIn(rc,[P.proto])){P.fly=-1;P.until=S.T;return}
  const far=Object.keys(DEF).filter(s=>HOP[R0.sid][s]===2&&!broodHeld(s)&&DEF[s].kind!=='hive'&&DEF[s].kind!=='den');if(!far.length){P.fly=-1;P.until=S.T;return}
  const to=pick(far),path=trPath(R0.sid,to).concat(trPath(to,R0.sid).slice(1));if(path.length<3){P.fly=-1;P.until=S.T;return}takeFrom(rc,[P.proto]);const name=pick(IND_FIRST)+' '+pick(IND_LAST);
  const t={id:S.nextId++,side:syfSide(R0),kind:'haul',key:'rdtest:'+m,why:`${MAKERS[m].short} prototype`,car:null,item:gid,n:1,from:R0.sid,to:R0.sid,path,leg:0,sector:R0.sid,next:S.T+TRADER_HOP*.5,load:{[gid]:1},cls:RD_FLY[(ITEMS[P.id]||I).part||(ITEMS[P.id]||I).sys]||'interceptor',T0:S.T,test:{m,name}};
  (S.traders=S.traders||[]).push(t);if(WORLDS[t.sector])inW(WORLDS[t.sector],()=>spawnTrader(t,false));P.fly=t.id;P.pilot=name;P.until=S.T+1e7;
  ceNews(m,`'s test pilot ${name} takes the ${I.name} prototype out on its trials from ${DEF[R0.sid].name}.`)}
{const o=rdTick;rdTick=function(){const r=o.apply(this,arguments);try{if(rdOn()&&!NET.cl)for(const m in MAKERS){const c=ceOf(m);if(!c||c.dead||!c.rd)continue;const P=c.rd;
    if(P.stage==='materials'&&!P.got&&!P.mj&&S.T>=(P.mjT||0))rdMatStart(m);
    else if(P.stage==='trials'&&P.got&&!P.fly)rdFlyStart(m)}}catch(e){console.error(e)}return r}}
// the flight is home: the line launches
function rdFlyHome(t){const m=t.test.m,c=ceOf(m),I=ITEMS[Object.keys(t.load)[0]],P=c&&c.rd;
  if(P&&P.fly===t.id&&I){const n=t.load[Object.keys(t.load)[0]]||0;if(n>0){inv.take(t.load,Object.keys(t.load)[0],n);inv.addAll(P.proto,I.recipe)}t.load={};rdLaunch(m);return}
  const H=mkAtHome(m);inv.addAll(H?mkStock(H):S.econ.stock.neutral,t.load);t.load={}}
// shot down: the prototype is lost and the project goes back to materials
function rdFlyLost(t,sid){const m=t.test.m,c=ceOf(m),P=c&&c.rd;if(!P||P.fly!==t.id)return;P.fly=null;P.got=0;P.mj=null;P.mjT=0;P.stage='materials';P.until=S.T+60;
  ceNews(m,`'s test pilot ${t.test.name} was shot down in ${DEF[sid]?DEF[sid].name:'deep space'} with the prototype. The project goes back to materials.`)}
// ---- arrivals and losses
{const o=haulArrive;haulArrive=function(t){if(!t||!(t.syf||t.test))return o.apply(this,arguments);cvEnd(t,true);
  if(t.test){rdFlyHome(t);return}mfjLand(t.syf.m,t.syf.k,t.to,t.load,t.syf.rid);t.load={}}}
function syfLost(t,sid){if(!t)return;if(t.test)rdFlyLost(t,sid);else if(t.syf&&t.syf.k==='mat'){const c=ceOf(t.syf.m);if(c&&c.rd&&c.rd.mj===t.syf.rid){c.rd.mj=null}}}
{const o=haulLost;haulLost=function(t,sid,by){try{syfLost(t,sid)}catch(e){console.error(e)}return o.apply(this,arguments)}}
{const o=traderLost;traderLost=function(e){try{const id=e&&e.home&&e.home.split(':')[1],t=(S.traders||[]).find(x=>String(x.id)===id);if(t&&(t.syf||t.test))syfLost(t,W.sid)}catch(err){console.error(err)}return o.apply(this,arguments)}}
// ---- escorts for the makers' freighters and test flights (paid by the maker)
{const o=cvEnd;cvEnd=function(t,ok,sid){if(!t||!(t.syf||t.test))return o.apply(this,arguments);const E=t.esc;if(!E)return;t.esc=null;const m=(t.syf||t.test).m,mk=MAKERS[m]?MAKERS[m].short:'The maker',what=t.test?`${mk} test flight`:`${mk} freighter`;
  if(!ok){keyFeed(E.k,`✖ Escort failed: the ${what} was destroyed in ${DEF[sid]?DEF[sid].name:'deep space'}.`,'bad');return}
  if(E.hops<E.need){keyFeed(E.k,`The ${what} reached ${DEF[t.to].name}, but you were with it for only ${E.hops} of the ${E.need} jumps. No pay.`,'warn');return}
  const got=payKey(E.k,ceW(m),mfEscPay(t,E.hops));keyFeed(E.k,`✔ Escort complete: the ${what} reached ${DEF[t.to].name}. ${mk} pays +${fmt(got)} cr.`,'good')}}
function mfEscPay(t,hops){return Math.round(cvPay(t,hops)*SYF.esc/10)*10}
function mfEscOK(P,t){return!(P.sworn&&t.side!=='neutral'&&hostile(P.sworn,t.side))}
function mfEsc(P,id){const t=(S.traders||[]).find(x=>String(x.id)===String(id)&&(x.syf||x.test));if(!t||!mfEscOK(P,t)||t.esc||cvLeft(t)<1)return'That flight no longer needs an escort.';
  const k=pkeyOf(P);for(const x of S.traders)if(x.esc&&x.esc.k===k)x.esc=null;const E=cvSign(t,k,P.name);if(t.sector!==P.sector)P.route=t.sector;
  return`✓ Signed on to escort the ${MAKERS[(t.syf||t.test).m].short} ${t.test?'test flight':'freighter'}: be with it for ${E.need} of its jumps.`}
{const o=dockAction;dockAction=function(act,arg){if(act==='mftake'||act==='mfdel'||act==='mfesc'){if(NET.cl)return o.apply(this,arguments);const P=S.player;dockErr=act==='mftake'?mfjTake(P,arg):act==='mfdel'?mfjDeliver(P,arg):mfEsc(P,arg);return}return o.apply(this,arguments)}}
// ---- the Jobs board: freight jobs at their source, Deliver at the destination, escorts within 3 jumps
{const o=jobsList;jobsList=function(c,P,srcs){const out=o.apply(this,arguments);try{if(S.unb||!c||c.kind!=='station'||!S.mfj&&!(S.traders||[]).some(t=>t.syf||t.test))return out;const me=pkeyOf(P),hop=sid=>HOP[P.sector]&&HOP[P.sector][sid]!=null?HOP[P.sector][sid]:0,far=n=>n?`${n} jump${n>1?'s':''}`:'here';
  for(let i=out.length-1;i>=0;i--){const id=String(out[i].id);if(id.startsWith('ce:')){const t=(S.traders||[]).find(x=>'ce:'+x.id===id);if(t&&(t.syf||t.test))out.splice(i,1)}}
  for(const j of mfjAll()){const mine=j.st==='taken'&&j.pk===me,D=S.stations[j.to];if(!D)continue;
    if(j.st==='open'&&j.from===P.sector){const val=mfjVal(j),room=shipStats(P.faction,P.cls,P.tiers,P.tune).cargo-invMass(P.cargo),mass0=invMass(j.load),busy=P.mfj&&mfjAll().some(x=>x.id===P.mfj&&x.st==='taken');
      const need=busy?'You are already on a freight job.':!tradeOK(P,D.owner)?`You can't trade at ${D.name}.`:room<mass0?`It needs ${mass0} t of hold space.`:P.credits<val?`It needs ${fmt(val)} cr collateral.`:'';
      out.push({id:'mf:'+j.id,by:'corp_'+j.m,sid:j.to,ty:'haul',title:esc(mfjTitle(j)),sub:`${mass0} t · collateral ${fmt(val)} cr · deliver within ${Math.round((SYF.due[0]+SYF.due[1]*j.hops)/60)} min · ${Math.max(0,Math.ceil((j.T0+SYF.wait-S.T)/60))} min before ${MAKERS[j.m].short} sends its own freighter`,hops:j.hops,where:far(j.hops),payN:j.pay,pay:`${fmt(j.pay)} cr`,
        btn:need?null:['mftake',j.id,'Take the job'],need,detail:()=>`<div style="margin-bottom:8px">${Object.keys(j.load).map(k=>chip(k,j.load[k],0)).join('')}</div><p class="note" style="margin:0">${j.k==='out'?`${esc(MAKERS[j.m].name)}'s goods, looking for buyers: loaded into your hold here.`:`${esc(MAKERS[j.m].name)} buys these here for its works${j.k==='mat'?' (the next grade\'s prototype)':''}; they're loaded into your hold.`} Deliver at ${esc(D.name)} (its Jobs board) for ${fmt(j.pay)} cr. Their value, ${fmt(val)} cr, is held as collateral and comes back when you deliver; miss the deadline or lose the goods and ${esc(MAKERS[j.m].short)} keeps it.</p>`})}
    else if(mine){const here=P.sector===j.to&&P.docked==='station';
      out.push({id:'mf:'+j.id,by:'corp_'+j.m,sid:j.to,ty:'haul',title:esc(mfjTitle(j)),sub:`your job · ${Math.max(0,Math.ceil((j.due-S.T)/60))} min left · collateral ${fmt(j.coll||0)} cr`,hops:hop(j.to),where:far(hop(j.to)),payN:j.pay,pay:`${fmt(j.pay)} cr`,
        btn:here?['mfdel',j.id,'Deliver']:['croute',j.to,'Set course'],detail:()=>`<p class="note" style="margin:0">Carry the goods to ${esc(D.name)} and Deliver on its Jobs board: ${fmt(j.pay)} cr and your collateral back.</p>`})}}
  for(const t of (S.traders||[]).filter(t=>(t.syf||t.test)&&cvLeft(t)>=1&&hop(t.sector)<=3)){if(!mfEscOK(P,t))continue;const E=t.esc,mine=E&&E.k===me,m=(t.syf||t.test).m,j=hop(t.sector),pay=mfEscPay(t,mine?Math.max(E.hops,E.need):Math.ceil(cvLeft(t)*ESC_CV.need));
    out.push({id:'mfe:'+t.id,by:'corp_'+m,sid:t.sector,ty:'fight',title:t.test?`Escort: test pilot ${esc(t.test.name)} (${esc(MAKERS[m].short)} prototype)`:`Escort: ${esc(MAKERS[m].short)} freighter to ${esc(DEF[t.to].name)}`,
      sub:mine?`escorting · ${E.hops}/${E.need} jumps`:E?`escorted by ${esc(E.name||'another pilot')}`:`${cvLeft(t)} jumps left · now in ${esc(DEF[t.sector].name)}`,hops:j,where:far(j),payN:pay,pay:`${fmt(pay)} cr`,btn:mine||E?null:['mfesc',t.id,'Escort'],
      detail:()=>`<p class="note" style="margin:0">${t.test?`A prototype on its trials, flown out and home by ${esc(MAKERS[m].name)}'s test pilot. If it's shot down the prototype is lost.`:`${esc(MAKERS[m].name)}'s own freighter.`} Fly with it: each jump it makes with you in the system it leaves or enters counts. ${esc(MAKERS[m].short)} pays when it docks, if you were with it for at least ${Math.round(ESC_CV.need*100)}% of the jumps left when you signed on.</p>`})}}catch(err){console.error(err)}return out}}
{const o=jbIssuer;jbIssuer=function(j){if(j&&typeof j.by==='string'&&j.by.startsWith('corp_')){const m=j.by.slice(5);return MAKERS[m]?MAKERS[m].name:'A maker'}return o.apply(this,arguments)}}
{const o=sideCol;sideCol=function(s){if(typeof s==='string'&&s.startsWith('corp_'))return'#9fb3d8';return o.apply(this,arguments)}}
// the labels of a maker's freighter and test pilot
{const o=shipLabel;shipLabel=function(e){const t=e&&e.tradeT;if(t&&t.test&&MAKERS[t.test.m])return`Test pilot ${t.test.name} · ${MAKERS[t.test.m].short} prototype`;if(t&&t.syf&&MAKERS[t.syf.m])return`${MAKERS[t.syf.m].short} freighter`;return o.apply(this,arguments)}}
// the escrow is counted in the ledger as a treasury wallet; a pilot's job record survives in the save
