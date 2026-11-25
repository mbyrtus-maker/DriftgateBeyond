//@src 16zzzzj_realjobs.js
// ============================================================ Beyond: real jobs (user, 24 Nov 2026)
// "In system teleportation is fine, but between systems is a haul job, getting ore is a mining job." Only the Brood may move
// goods between systems without a ship. tools/teleport.py plays an AI galaxy and lists every flow that breaks the rule; this
// file (with small changes where the flows were) puts each one on a ship:
//   - the Unbound have freighters: plunder from a depot or outpost, the fence's goods and the ore of their camp in the Verge
//     ride a convoy to or from the Wrack (they went straight into the Wrack's store);
//   - a raid is kitted from the store of the station it leaves and unloads where it lands (every station drew on the home
//     warehouse); a station with no kit asks the warehouse for some by convoy;
//   - a response wing is raised at home and flies from home (it launched from the nearest station with the home
//     warehouse's kit);
//   - the powers' refit parts, bought at a freeport or a depot, ride home before they are fitted;
//   - plunder from a battered core station rides home; a convoy that can't deliver turns for home; a strike wing whose
//     carrier is gone flies home; bombers sent to burn Overgrowth fly there and back.
const RJ={fenceMin:30,fenceHold:120,campMin:30,campWait:300,buy:{cu:40,nu:12,wire:24}};
// ---- Unbound freighters (16_expansion.js turns every other Unbound shipment straight into the Wrack's store)
function unbHaul(from,to,load,key,why){rjUnbFly=true;try{return haulSend('pirate',from,to,load,key,why)}finally{rjUnbFly=false}}
function unbShip(fromSid,load,key,why){if(!load||!Object.keys(load).length)return null;
  if(!fromSid||fromSid==='wr'||!DEF[fromSid]||!S.econ.stock.pirate){inv.addAll(S.econ.stock.pirate,load);return null}
  return unbHaul(fromSid,'wr',load,key+':'+S.nextId,why)}
function unbFenced(got){const F=S.econ.fenced=S.econ.fenced||{};for(const k in got)if(!RAWS.includes(k)&&!['plate','wire','coil','missile','torpedo','drone'].includes(k))F[k]=(F[k]||0)+got[k]}
// plunder: a prize freighter carries it home from where it was taken
{const o=pirLootTo;pirLootTo=function(got,sid){if(!sid||sid==='wr'||!DEF[sid])return o.apply(this,arguments);const t=unbShip(sid,{...got},'loot','plunder');if(t)t.loot=1}}
// plunder from a battered core station rides home with the victor's freighters (the Brood devours it where it is)
function rjPlunder(att,sid,got){if(att==='pirate'){pirLootTo(got,sid);return}if(att==='brood'||!frCv(att)){inv.addAll(S.econ.stock[att]||S.econ.stock.pirate,got);return}frShip(att,sid,got,'plunder','plunder')}
// ---- the fence: an Unbound freighter carries surplus loot to the nearest freeport and sells it there, buys the copper,
// Vantium and conduit the Wrack lacks with the proceeds, and carries those home (goods and credits swapped places at once)
{pirFence=function(want){const st=S.econ.stock.pirate,fp=fpNear('wr');if(!st||!fp)return;S.econ.fenceWant={...want};
  if((S.traders||[]).some(t=>t.side==='pirate'&&t.fence))return;
  const F=S.econ.fenced||{},load={};let m=0;
  for(const[k,keep]of[['xc',40],['ir',140],['fe',260],['nu',Math.max(30,(want.nu||0)+20)],['cu',Math.max(80,(want.cu||0)+40)]]){const n=Math.min((st[k]||0)-keep,Math.floor((RJ.fenceHold-m)/mass(k)));if(n>0){load[k]=n;m+=n*mass(k)}}
  for(const k of Object.keys(F)){if(MUNITIONS.has(k)||!ITEMS[k]){delete F[k];continue}const n=Math.min(F[k],(st[k]||0)-((want[k]||0)+5),Math.floor((RJ.fenceHold-m)/mass(k)));if(n>0){load[k]=(load[k]||0)+n;m+=n*mass(k)}}
  let short=false;for(const k of['cu','nu','wire'])if((want[k]||0)>(st[k]||0))short=true;
  if(m<=0||(m<RJ.fenceMin&&!(short&&(S.econ.treasury.pirate||0)>=2500)))return;
  for(const k in load)load[k]=inv.take(st,k,load[k]);
  const t=unbHaul('wr',fp.sid,load,'fence:'+S.nextId,'the fence');if(t)t.fence=1;else inv.addAll(st,load)}}
function fenceArrive(t){const fp=S.stations[t.to],st=S.econ.stock.pirate,F=S.econ.fenced||{},want=S.econ.fenceWant||{};cvEnd(t,true);
  // the freeport fell or went dark on the way: bring it all home
  if(!isFreeF(fp)){unbShip(t.to,t.load,'fenceback','the fence');t.load={};return}
  const N=dStore(fp);
  for(const k of Object.keys(t.load)){const n=t.load[k];if(!(n>0)||!ITEMS[k])continue;const pr=RAWS.includes(k)?Math.floor(baseValue(k)*.8):Math.max(1,Math.floor(price(N,k,MK_SC.free)*.9));if(pr<1)continue;
    const pay=transfer('neutral','pirate',pr*n),sold=Math.min(n,Math.floor(pay/pr));if(sold>0){inv.take(t.load,k,sold);inv.add(N,k,sold);if(F[k]){F[k]-=sold;if(F[k]<=0)delete F[k]}}}
  const back={};for(const k in t.load)if(t.load[k]>0)back[k]=t.load[k];t.load={};let m=invMass(back);
  for(const k of['cu','nu','wire']){const need=(want[k]||0)-(st[k]||0);if(need<=0)continue;const n=Math.min(RJ.buy[k],need,(N[k]||0)-(k==='nu'?4:k==='wire'?7:8),Math.floor((RJ.fenceHold-m)/mass(k)));if(n<=0)continue;
    const pr=Math.ceil(baseValue(k)*(k==='wire'?1.4:1.5)),cost=pr*n;if((S.econ.treasury.pirate||0)<cost+1500)continue;back[k]=(back[k]||0)+inv.take(N,k,n);transfer('pirate','neutral',cost);m+=n*mass(k)}
  if(Object.keys(back).length){const b=unbHaul(t.to,'wr',back,'fenceback:'+S.nextId,'the fence');if(b)b.fence=2;else inv.addAll(st,back)}}
// ---- the Unbound's camp in the Verge: what its crews dig waits there for a freighter (it landed in the Wrack's store)
function rjUnbCamp(got){const C=S.econ.unbCamp=S.econ.unbCamp||{};if(got&&Object.keys(got).length){if(!invMass(C))S.econ.unbCampT=S.T;inv.addAll(C,got)}
  const m=invMass(C);if(m>0&&(m>=RJ.campMin||S.T-(S.econ.unbCampT||0)>=RJ.campWait)){S.econ.unbCamp={};unbShip('ho',C,'camp','ore')}}
{const o=ledger;ledger=function(){const r=o.apply(this,arguments);try{const L=r.L['Faction & Unbound stores'],v=invVec((S.econ&&S.econ.unbCamp)||{});for(const e of RAWS){L[e]+=v[e];r.tot[e]+=v[e]}}catch(e){}return r}}
// ---- convoys with somewhere particular to go
{const o=haulArrive;haulArrive=function(t){try{
  if(t&&t.side==='pirate'){if(t.fence===1){fenceArrive(t);return}if(t.loot)unbFenced(t.load)}
  if(t&&t.fit&&S.econ.stock[t.fit]){cvEnd(t,true);const pool=(S.corpFit=S.corpFit||{})[t.fit]=S.corpFit[t.fit]||{};inv.addAll(pool,t.load);t.load={};return}
  }catch(e){console.error(e)}return o.apply(this,arguments)}}
// ---- raids: kitted where they leave, unloaded where they land
function rjRaidLd(side){const ld=loadout('patrol',factionTier(side)||1,'striker'),o={};for(const k in ld)o[k]=ld[k]*2;return o}
function rjKitAsk(side,src){try{if(!src||src.cap||!FAC_IDS.includes(side)||src.sid===FAC_HOME(side))return;const R=S.stations[src.sid];if(!isDepotF(R)||R.owner!==side)return;frAsk({R,owner:side,key:'S.'+src.sid},rjRaidLd(side))}catch(e){console.error(e)}}
{const o=raidSources;raidSources=function(side){const L=o.apply(this,arguments);if(!FAC_IDS.includes(side))return L;const home=FAC_HOME(side),out=[];
  for(const s of L){if(s.cap||s.sid===home){out.push(s);continue}const R=S.stations[s.sid];if(isDepotF(R))out.push({sid:s.sid,srcs:[dStore(R)],cap:null,reach:s.reach,deep:s.deep})}return out}}
{const o=raidUnload;raidUnload=function(r){try{if(r&&r.side!=='brood'){const side=r.side,home=homeOf(side),sid=r.sector,C=r.cap&&(S.frigates||[]).find(x=>x.id===r.cap&&x.sector===sid);
  if(!C&&sid!==home){const R=S.stations[sid];
    if(FAC_IDS.includes(side)&&R&&R.owner===side&&isDepotF(R)){const ds=dStore(R);inv.addAll(ds,r.kit);inv.addAll(ds,r.loot);r.kit={};r.loot={};S.raids.splice(S.raids.indexOf(r),1);return}
    // nowhere of its own to land here: it flies on home with everything aboard
    r.state='home';r.src=home;r.cap=null;r.dest=home;r.path=trPath(sid,home);r.leg=0;r.next=S.T+RAID.hop;return}
  // back aboard an Unbound capital in the field: the kit goes into its store, the loot home on a prize freighter
  if(C&&side==='pirate'&&sid!==home&&Object.keys(r.loot||{}).length){const loot=r.loot;r.loot={};const t=unbShip(sid,loot,'loot','plunder');if(t)t.loot=1}}}catch(e){console.error(e)}return o.apply(this,arguments)}}
// the Unbound's gate lock rides out with the raid (it was taken from the Wrack's shelf at the gate it clamped)
{const o=raidSend;raidSend=function(side,pk,kit){const r=o.apply(this,arguments);try{if(r&&side==='pirate'&&pk.src&&pk.src.sid==='wr'&&!pk.src.cap&&!havenDown()&&Math.random()<glUnbChance()){const st=S.econ.stock.pirate;if(st.glock>0)inv.add(r.kit,'glock',inv.take(st,'glock',1))}}catch(e){console.error(e)}return r}}
// ---- response wings: raised at home from the muster and the warehouse, and flown from home (they launched from the nearest
// station with the home's kit). A wing still goes only where a station of its power is within range. (A first build raised
// them from the nearest depot's own store: the powers then answered far more calls, the Brood's share fell from 24% to 8%,
// and putting this one piece back restored it; see "Real jobs" in BEYOND_DESIGN.md.)
function rjRespSrcs(f,sid,maxH){const near=respSource(f,sid),home=FAC_HOME(f);if(!near||near.h>maxH||!home||!HOP[home])return[];const R=S.stations[home];
  if(!R||R.owner!==f)return[{sid:near.sid,h:near.h,srcs:[S.econ.fleet[f],S.econ.stock[f]].filter(Boolean)}];
  return[{sid:home,h:HOP[home][sid]||0,srcs:[S.econ.fleet[f],S.econ.stock[f]].filter(Boolean)}]}
// ---- the powers' refit parts ride home from where they were bought
let rjFitBuf=null;
function rjFitGot(f,R,id,pool){const home=FAC_HOME(f);if(!rjFitBuf||!home||R.sid===home){inv.add(pool,id,1);return}const k=f+'|'+R.sid;inv.add(rjFitBuf[k]=rjFitBuf[k]||{},id,1)}
{const o=ceRefit;ceRefit=function(){rjFitBuf={};try{return o.apply(this,arguments)}finally{const B=rjFitBuf;rjFitBuf=null;for(const k in B){const[f,sid]=k.split('|');let t=null;try{t=haulSend(f,sid,FAC_HOME(f),B[k],'fit:'+f+':'+S.nextId,'refit parts')}catch(e){console.error(e)}if(t)t.fit=f;else inv.addAll(S.corpFit[f],B[k])}}}}
// ---- bombers sent to burn Overgrowth off a gate fly there and home again
function rjOgSend(O,f,force,tier){const home=FAC_HOME(f),h=home?(HOP[home][O.a]||0):0;if(!h){ogStrikeHit(O,f,force,tier);return}
  S.events.push({id:S.nextId++,type:'ogstrike',att:f,sector:O.a,from:home,og:O.id,force,tier,eta:S.T+RAID.hop*h,until:1e12,stage:'fly'})}
function rjOgTick(){for(const ev of S.events||[]){if(ev.type!=='ogstrike'||ev.stage!=='fly'||S.T<ev.eta)continue;ev.stage='done';const O=(S.og||[]).find(x=>x.id===ev.og);
    const live=O&&WORLDS[O.a]&&WORLDS[O.a].ents.some(e=>e.alive&&e.ogId===O.id);if(O&&O.stage!=='seed'&&!live)ogStrikeHit(O,ev.att,ev.force,ev.tier);else prwHome(ev.att,ev.sector,ev.force);ev.force={}}}
// ---- small rules used where the flows were
// a build party's trip takes its jumps (it took 80 s from anywhere)
function rjHomeHops(f,sid,d){const home=FAC_IDS.includes(f)?FAC_HOME(f):null;return home&&HOP[home]&&HOP[home][sid]!=null?HOP[home][sid]:d}
function rjBuildEta(f,sid){return f==='brood'?80:Math.max(80,RAID.hop*rjHomeHops(f,sid,0))}
// defenders are raised where the fight is: at home from the muster and the warehouse, elsewhere from the site's own store
function rjDefSrcs(f,sid,site){if(f==='brood'||sid===homeOf(f)||!site)return[S.econ.fleet[f],S.econ.stock[f]].filter(Boolean);return[site]}
function rjDefBack(f,sid,site){if(f==='brood'||sid===homeOf(f)||!site)return S.econ.fleet[f]||S.econ.stock[f];return site}
// a capital refills from the store where it is: the muster and the warehouse at home, a depot's own store at a depot
function rjCapSrcs(t,f){if(f==='brood'||t.sector===homeOf(f))return[S.econ.fleet[f],S.econ.stock[f]].filter(Boolean);const R=S.stations[t.sector];if(R&&R.owner===f&&isDepotF(R))return[dStore(R)];return null}
// ---- at a dock: what a station makes, sells or takes in comes from and goes to the store that is there
function rjWhAt(f,sid,which){const E=S.econ[which||'stock'];if(!E)return null;if(FAC_IDS.includes(f)||f==='pirate')return sid===homeOf(f)?E[f]||null:null;return E[f]||null}
function rjDockStore(c,f){return(c&&c.market)||S.econ.stock[f]}
function rjDockMk(P,fac){const R=P.docked==='station'&&S.stations[P.sector];if(R&&R.owner===fac)return storeOf(R);return rjWhAt(fac,P.sector)}
// contraband a pilot gives up goes to the power's station in that system, or home on a convoy
function rjSeized(f,sid,got){if(!Object.keys(got).length)return;const R=S.stations[sid];if(R&&R.owner===f&&storeOf(R)){inv.addAll(storeOf(R),got);return}if(frCv(f))frShip(f,sid,got,'seized','seized goods');else inv.addAll(S.econ.stock[f]||S.econ.stock.pirate,got)}
// ---- traders at your depot: what they buy rides home with them, what you buy comes out from their home and is paid for
// when it lands (both changed stores at once)
let rjDepBuf=null;
function rjDepOf(R){return lairOwner({pid:R.pid||'me'})||S.player}
function rjDepEnroute(R,k){let n=0;for(const t of S.traders||[])if(t.pd&&t.pd.sid===R.sid)n+=(t.load&&t.load[k])||0;if(rjDepBuf)for(const key in rjDepBuf)if(key.startsWith(R.sid+'|')&&key.endsWith('|i'))n+=rjDepBuf[key].load[k]||0;return n}
function rjDepOut(R,f,k,n){if(!(n>0))return;const home=FAC_HOME(f);if(!rjDepBuf||!home||home===R.sid){inv.add(S.econ.stock[f],k,n);return}const key=R.sid+'|'+f+'|o',b=rjDepBuf[key]=rjDepBuf[key]||{load:{},cost:0};inv.add(b.load,k,n)}
function rjDepIn(R,f,k,n,pr){if(!(n>0))return;const home=FAC_HOME(f);
  if(!rjDepBuf||!home||home===R.sid){inv.add(R.stock,k,n);payFrom(rjDepOf(R),f,n*pr);eco(R,'market',-n*pr,`bought ${n} ${ITEMS[k].name} from ${FACTIONS[f].short} traders`);return}
  const key=R.sid+'|'+f+'|i',b=rjDepBuf[key]=rjDepBuf[key]||{load:{},cost:0};inv.add(b.load,k,n);b.cost+=n*pr}
{const o=depTradeTick;depTradeTick=function(){rjDepBuf={};try{return o.apply(this,arguments)}finally{const B=rjDepBuf;rjDepBuf=null;for(const key in B){const[sid,f,d]=key.split('|'),b=B[key];
  if(d==='o'){frShip(f,sid,b.load,'pdep','trade');continue}
  let t=null;try{t=haulSend(f,FAC_HOME(f),sid,b.load,'pdin:'+sid+':'+S.nextId,'trade')}catch(e){console.error(e)}if(t)t.pd={sid,cost:b.cost};else inv.addAll(S.econ.stock[f],b.load)}}}}
// aid a leader grants comes out from the power's home the same way
function rjAidSend(R2,f,give){const home=FAC_HOME(f);if(!R2||!Object.keys(give).length)return;if(!home||home===R2.sid){inv.addAll(R2.stock,give);return}const t=haulSend(f,home,R2.sid,give,'aid:'+S.nextId,'aid');if(t)t.pd={sid:R2.sid,cost:0};else inv.addAll(R2.stock,give)}
{const o=haulArrive;haulArrive=function(t){if(!t||!t.pd)return o.apply(this,arguments);cvEnd(t,true);const R=S.stations[t.pd.sid];
  if(R&&R.owner==='player'&&t.to===t.pd.sid){const what=haulWhat(t);inv.addAll(R.stock,t.load);t.load={};if(t.pd.cost>0){const paid=payFrom(rjDepOf(R),t.side,t.pd.cost);eco(R,'market',-paid,`bought ${what} from ${FACTIONS[t.side].short} traders`)}return}
  // the depot is gone or changed hands: the goods go home again
  frShip(t.side,t.to,t.load,'back','return');t.load={}}}
// a depot short of what its standard stock takes asks the warehouse; the parts ride out on their own convoy
function rjStdAsk(R,need){const f=R.owner,key='std:'+R.sid,home=FAC_HOME(f),st=S.econ.stock[f];if(!st||!home||home===R.sid||haulBusy(key))return false;const capR=capNeed(f)||{},ds=dStore(R),load={};
  for(const k in need){const lack=need[k]-(ds[k]||0);if(lack<=0)continue;const n=Math.min(lack,Math.max(0,(st[k]||0)-Math.ceil((capR[k]||0)*.5)-(STD.keep[k]||0)));if(n>0)load[k]=inv.take(st,k,n)}
  if(!Object.keys(load).length)return false;return!!haulSend(f,home,R.sid,load,key,'supplies')}
// in a freeport's own system the fence's freighter flies the Compact's colours, so the port's guns and guards let it dock
// (the Compact and the Unbound are otherwise hostile: out of sight nothing stops the run at the port, and nor does it in view)
{const o=spawnTrader;spawnTrader=function(t,arrive){const e=o.apply(this,arguments);try{if(e&&t&&t.side==='pirate'&&t.fence&&W&&isFreeF(S.stations[W.sid])){e.side='neutral';e.fac='neutral'}}catch(err){console.error(err)}return e}}
