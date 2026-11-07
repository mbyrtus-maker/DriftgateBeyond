//@src 16zzzc_indep.js
// ============================================================ Beyond: independent pilots (agreed by the user 7 Nov 2026)
// From "Proposal: independent pilots" and "Independent pilots: agreed" in BEYOND_DESIGN.md. A standing population of AI
// contractors living the player's life on a small scale. Each is a tracked pilot (S.ind.L) with a name, a home freeport, a
// line of work (hauling, mining or guarding), a hull with its systems and fitted parts, a hold, a purse (wallet pil_i<id>), a
// Contractor Rating and standing with the powers.
//   Arrival: about 4 a freeport at the start, a newcomer every 20 to 40 minutes while a freeport has fewer than 4 (18 at most
//     in the galaxy). A newcomer's light hull, systems, fitted parts and drones are built from its freeport yard's store goods
//     (as your starting ship) and its stake of 1,500 cr comes from the Compact. If the yard can't build it, nobody arrives.
//   Posted jobs: the nearest free independent whose hull fits takes your Supply, Haul, Mine or Guard job (the one-off AI
//     contractors are gone) and flies it from where it is (16zzr_contract.js runs the flight); the fee goes into its purse.
//   Board jobs: a freeport request, a blockade run or a power's supply contract that has gone untaken for 8 minutes may be
//     taken by an independent: it buys the goods at a freeport (a power's supply contract only with ore it mined itself),
//     flies them in and is paid by the issuer, as you are.
//   Between jobs: haulers (and fighters, in their small holds) trade, buying a freeport's surplus and selling where the
//     margin beats the fees (your prices, fees and lots); miners mine real rock in their home freeport's system and sell the
//     ore there. A rest docked after each run, and a full purse takes only posted jobs (the throttles, below in IND).
//   Buying: docked at a market with money above its reserve (400 cr and the price of a light hull), an independent fills
//     empty slots, replaces unbranded parts and systems with makers' and takes higher grades up to its Rating, at the
//     Market's price, off the shelf, the maker paid (mkBuyOne / ceSale); it pays to rearm after a fight; at Rating 2 and 5 it
//     buys the next hull of its line at a freeport yard. Fitted parts wear out as the crews' do.
//   Risk: attacking one is a free-for-all (no standing lost with anyone). Shot down, its hull, systems, parts and hold are
//     salvage as any ship's; it rebuys a light hull at home if its purse allows, otherwise it retires and its purse goes to
//     the Compact. They never declare, build or fly for the Unbound.
//   Live: in an open system they fly as ships labelled "Independent · <name> · <job>"; out of sight they hop lane by lane
//     every 45 s. A departure from a station in an open system at the ship cap waits docked.
const IND={per:4,max:6,cap:18,arrive:[1200,2400],stake:1500,reserve:400,keep:100,every:60,hop:45,board:480,mix:{haul:2,mine:1,guard:1},
  light:{haul:'courier',mine:'skiff',guard:'interceptor'},next:{courier:'freighter',freighter:'bulker',skiff:'prospector',prospector:'dredger',interceptor:'striker',striker:'heavy'},
  margin:.12,minProfit:60,tradeHops:4,perVisit:3,mineMax:1500,rearm:{guard:120,other:45},rp:60,look:.35,rest:[420,900],rich:1500,lotCr:600,shopT:600};
const IND_GOODS=TRADE_ITEMS.filter(k=>k!=='seal'&&k!=='drone');
const IND_FIRST=['Ada','Bram','Cass','Dov','Edda','Fenn','Gale','Hollis','Ines','Jory','Kael','Lio','Mara','Nell','Oren','Pell','Quill','Rhea','Sable','Tamsin','Ulla','Vey','Wren','Yara','Zeb','Ash','Brisk','Corin','Dace','Elm','Fable','Greer','Hask','Isa','Juno','Kit','Lark','Moss','Noor','Pike'];
const IND_LAST=['Varga','Okafor','Lindqvist','Moreau','Tal','Achebe','Sorensen','Quist','Halloran','Ferro','Nakamura','Ilves','Brandt','Oduya','Castell','Mbeki','Rourke','Szabo','Teague','Vance','Aldane','Brook','Corvo','Dunmore','Easton','Faro','Gryce','Hale','Ivers','Jessop','Kestrel','Lowe','Marsh','Nyle','Orme','Prior','Quell','Rask','Stroud','Thorn'];
function indS(){return S.ind||(S.ind={n:1,L:[],arr:{},T:0})}
function indL(){return indS().L}
function indOf(id){return indL().find(I=>I.id===id)||null}
function indW(I){return'pil_i'+I.id}
function indPurse(I){return S.econ.treasury[indW(I)]||0}
function indOn(){return!!S&&!S.training&&!S.unb}
function indWl(R){return R.owner==='neutral'?'neutral':R.owner}
// the markets an independent deals at: the freeports, and the powers' stations and depots where its standing lets it dock
function indMkt(R,I){if(!R)return false;if(isFreeF(R))return true;return FAC_IDS.includes(R.owner)&&(R.kind==='core'||isDepotF(R))&&standOf(R.owner,I)>=STAND.dock}
function indMarkets(I){const L=[];for(const sid in S.stations){const R=S.stations[sid];if(indMkt(R,I))L.push(R)}return L}
// "buy low": an independent buys trade goods and board-job goods only at a freeport, and only out of a surplus (the price at
// or under the good's base value); it sells anywhere. A power's core market is its whole war stock: twelve AI pilots buying
// its plate and coil there moved the war check about 10 points to the Brood (still 7 with surplus-only buying anywhere)
function indSurplus(R,k){return isFreeF(R)&&stPrice(R,k)<=baseValue(k)}
function indHop(a,b){const h=HOP[a]&&HOP[a][b];return h==null?99:h}
// ---- prices, as yours: the station's price and your market fee for the hull, in lots at one quoted price
function indBuyP(R,id,cls){return Math.ceil(stPrice(R,id)*(1+mFee(cls)))}
function indSellP(R,id,cls){return Math.max(1,Math.floor(stPrice(R,id)*(1-mFee(cls))))}
function indLot(R,k,dir,maxN,cls){if(!(maxN>=1))return 0;maxN=Math.floor(maxN);if(maxN<=1)return maxN;const st=mkStock(R),mk=mkOf(R),s0=st[k],m0=mk[k]||0,K=HAUL_MK[cls]||1,p0=stPrice(R,k);
  const at=n=>{st[k]=(s0||0)+dir*n;mk[k]=m0+dir*n*K;const p=stPrice(R,k);if(s0===undefined)delete st[k];else st[k]=s0;mk[k]=m0;return p};
  const ok=n=>dir>0?at(n)>=p0*LOT_TOL.sell:at(n)<=p0*LOT_TOL.buy;let lo=1,hi=maxN;if(ok(hi))return hi;while(hi-lo>1){const m=(lo+hi)>>1;if(ok(m))lo=m;else hi=m}return lo}
// buy up to n of k at R into the hold, a lot at a time, never above maxP a unit; the price moves as your buy moves it
function indBuy(I,R,k,n,maxP){const st=mkStock(R),K=HAUL_MK[I.cls]||1,w=indW(I),wl=indWl(R);let got=0;
  for(let g=0;g<4&&got<n;g++){const pr=indBuyP(R,k,I.cls);if(maxP&&pr>maxP)break;const m=Math.min(indLot(R,k,-1,Math.min(n-got,st[k]||0),I.cls),Math.floor(indPurse(I)/pr));if(m<=0)break;
    const paid=transfer(w,wl,m*pr);if(paid<m*pr){transfer(wl,w,paid);break}inv.take(st,k,m);inv.add(I.hold,k,m);mkOf(R)[k]=(R.mk[k]||0)-m*K;got+=m;const t=indS().tot=indS().tot||{};t.buy=(t.buy||0)+paid;const q=(t.bw=t.bw||{});q[wl+':'+k]=(q[wl+':'+k]||0)+paid}
  if(got){I.hb=I.hb||{};I.hb[k]=indBuyP(R,k,I.cls);I.hT=S.T}return got}
// sell up to n of k from the hold at R, a lot at a time, never below minP a unit, as far as the owner's treasury pays
function indSell(I,R,k,n,minP){const st=mkStock(R),K=HAUL_MK[I.cls]||1,w=indW(I),wl=indWl(R);let sold=0,earn=0;n=Math.min(n,I.hold[k]||0);
  for(let g=0;g<6&&sold<n;g++){const pr=indSellP(R,k,I.cls);if(minP&&pr<minP)break;const m=Math.min(indLot(R,k,1,n-sold,I.cls),Math.floor((S.econ.treasury[wl]||0)/pr));if(m<=0)break;
    inv.take(I.hold,k,m);inv.add(st,k,m);mkOf(R)[k]=(R.mk[k]||0)+m*K;earn+=transfer(wl,w,m*pr);sold+=m}
  if(earn){const t=indS().tot=indS().tot||{};t.sell=(t.sell||0)+earn;const q=(t.sw=t.sw||{});q[wl+':'+k]=(q[wl+':'+k]||0)+earn}
  if(sold&&!(I.hold[k]>0)&&I.hb)delete I.hb[k];I.earn=(I.earn||0)+earn;return sold}
// what's in the hold sold where it is: parts and systems taken out (and mined ore) at any price, trade goods not below what
// they cost unless they have been aboard 20 minutes
function indSellAll(I,R,force,junkOnly){if(!R||!indMkt(R,I))return;const old=S.T-(I.hT||S.T)>1200;for(const k of Object.keys(I.hold)){if(!(I.hold[k]>0)||k==='matrix'&&!isFreeF(R))continue;
  const it=ITEMS[k],junk=it&&(it.part||it.sys);if(junkOnly&&!junk)continue;const min=junk||force||old||!(I.hb&&I.hb[k])?1:Math.floor(I.hb[k]*.97);indSell(I,R,k,I.hold[k],min)}}
// ---- the ship: systems (I.sys: slot -> item), fitted parts (I.sl: {g,k,it}), hull goods and drones (I.hull), the hold
function indNeed(cls){const D=slotsOf(cls,null),o=baseKit();for(const k of[...D.w,...D.u])if(PART_RC[k])inv.addAll(o,PART_RC[k]);inv.addAll(o,HULL_COST[cls]||{});return o}
function indKitCost(R,cls){const need=indNeed(cls);let c=0;for(const k in need)c+=indBuyP(R,k,cls)*need[k];return c}
// build a light hull at R's yard from its store: unbranded systems and parts fabricated from the components, drones off the
// shelf; paid at the Market's price when pay (a rebuy), free for a newcomer (as your starting ship)
function indBuild(I,cls,R,pay){if(!R)return false;const st=mkStock(R),need=indNeed(cls);if(!haveIn(need,[st]))return false;const cost=pay?indKitCost(R,cls):0;if(pay&&indPurse(I)<cost)return false;
  if(cost&&transfer(indW(I),indWl(R),cost)<cost)return false;takeFrom(need,[st]);
  I.sys={};for(const sl of SLOTS)I.sys[sl.id]='sy_'+sl.id;const D=slotsOf(cls,null);I.sl=[...D.w.map(k=>({g:'w',k,it:PART[k]})),...D.u.map(k=>({g:'u',k,it:PART[k]}))];
  I.hull={...(HULL_COST[cls]||{})};
  const nd=Math.min(CLASSES[cls].drones||0,st.drone||0);if(nd>0){const pr=pay?indBuyP(R,'drone',cls):0,m=pay?Math.min(nd,Math.floor(indPurse(I)/Math.max(1,pr))):nd;if(m>0){if(pr)transfer(indW(I),indWl(R),m*pr);inv.take(st,'drone',m);I.hull.drone=m}}
  I.cls=cls;return true}
function indItems(I){const o={};for(const sl in I.sys||{})if(I.sys[sl])inv.add(o,I.sys[sl],1);for(const s of I.sl||[])if(s.it)inv.add(o,s.it,1);return o}
function indT(I){const T=baseTiers();for(const sl in I.sys||{}){const it=ITEMS[I.sys[sl]];if(it)T[sl]=it.grade||1}
  for(const s of I.sl||[]){const it=s.it&&ITEMS[s.it];if(!it)continue;const g=it.grade||1,sl=s.k==='cargo'?'cargo':s.k==='mlaser'||s.k==='charge'?'drill':s.k==='gun'||s.k==='laser'||s.k==='missile'?'weapon':null;if(sl&&g>T[sl])T[sl]=g}return T}
function indCap(I){if(!I.cls)return 0;let c=shipStats('neutral',I.cls,indT(I)).cargo,k=1;for(const s of I.sl||[])if(s.k==='cargo'&&s.it){const it=ITEMS[s.it];k+=LOAD.cargoK*(1+PG.cargo*((it.grade||1)-1))+((it.tr&&it.tr.cargo)||0)}return Math.floor(c*k)}
function indRoom(I){return Math.max(0,indCap(I)-invMass(I.hold))}
function indMineRate(I){const T=indT(I);let k=1+.15*(T.drill-1);for(const s of I.sl||[])if(s.it&&(s.k==='mlaser'||s.k==='charge')){const it=ITEMS[s.it];k+=.1+((it.tr&&(it.tr.ml||it.tr.mag*.05))||0)}return(DEP.mine[I.cls]||3)*k}
// a purse this far above the reserve (or the next hull's price, saving for it) takes it easy: posted jobs only
function indRich(I){const nx=IND.next[I.cls],h=nx&&ratingOf(I)>=(HULL_RATING[nx]||1)?hullPrice(nx):0;return indReserve(I)+Math.max(IND.rich,h)}
function indReserve(I){const R=S.stations[I.home];return IND.reserve+(R?indKitCost(R,IND.light[I.line]):600)}
function indFly(e,I){e.st=shipStats('neutral',I.cls,indT(I));e.st.cargo=indCap(I);e.hull=e.st.hull;e.shield=e.st.sCap;e.energy=e.st.eCap;return e}
// ---- the population
function indName(){const used=new Set(indL().map(I=>I.name));for(let i=0;i<60;i++){const n=pick(IND_FIRST)+' '+pick(IND_LAST);if(!used.has(n))return n}return pick(IND_FIRST)+' '+pick(IND_LAST)+' '+ri(2,9)}
function indHomeN(sid){return indL().filter(I=>I.home===sid).length}
function indPickLine(sid){const have={haul:0,mine:0,guard:0};for(const I of indL())if(I.home===sid)have[I.line]++;let best='haul',bv=-1e9;for(const k in IND.mix){const v=IND.mix[k]-have[k];if(v>bv){bv=v;best=k}}return best}
function indAdd(sid,line,seed){const R=S.stations[sid];if(!isFreeF(R)||indL().length>=IND.cap||indHomeN(sid)>=IND.max||(S.econ.treasury.neutral||0)<IND.stake)return null;line=line||indPickLine(sid);const S0=indS();
  const I={id:S0.n,name:indName(),home:sid,line,cls:null,sys:{},sl:[],hull:{},hold:{},rp:0,stand:{halcyon:0,varkesh:0,ostrova:0,neutral:0},sector:sid,at:'dock',go:null,T0:S.T,jobs:0,earn:0,spent:0,r:1};
  if(seed)inv.addAll(mkStock(R),indNeed(IND.light[line]));if(!indBuild(I,IND.light[line],R,false))return null;S0.n++;S0.L.push(I);transfer('neutral',indW(I),IND.stake);return I}
// the opening population is part of a new galaxy, as your own ship is (its ships counted into the starting ledger); a galaxy
// saved before independents gets only what its yards can build
function indInit(){const S0=indS();if(S0.init||!indOn())return;S0.init=1;const seed=S.T<120&&!!S.ledger0;const go=()=>{for(const F of FREEPORTS)for(let i=0;i<IND.per;i++)indAdd(F.sid,null,seed)};if(seed)devLedger(go);else go();for(const F of FREEPORTS)S0.arr[F.sid]=S.T+rnd(IND.arrive[0],IND.arrive[1])}
function indArrivals(){const S0=indS();for(const F of FREEPORTS){const R=S.stations[F.sid];if(!isFreeF(R))continue;if(indHomeN(F.sid)>=IND.per||indL().length>=IND.cap){S0.arr[F.sid]=null;continue}
  if(S0.arr[F.sid]==null){S0.arr[F.sid]=S.T+rnd(IND.arrive[0],IND.arrive[1]);continue}if(S.T<S0.arr[F.sid])continue;S0.arr[F.sid]=S.T+rnd(IND.arrive[0],IND.arrive[1]);
  const I=indAdd(F.sid);if(I&&(covered(F.sid)||(W&&W.sid===F.sid)))feed(`An independent pilot, ${I.name}, has set up at ${R.name} in a ${CLASSES[I.cls].name}.`,'info')}}
// ---- the clock: hops and mining every strategic tick; arrivals, wear and decisions once a minute
function indTick(){if(NET.cl||!S||!indOn())return;indInit();const S0=indS();indStamp();for(const I of indL().slice())indMove(I);if(S.T<(S0.T||0))return;S0.T=S.T+IND.every;indArrivals();
  for(const I of indL().slice()){indWear(I);indRateNews(I);if(I.at==='dock'&&!I.go)indDecide(I);else if(I.at==='dock'&&I.go&&I.wait)indResume(I)}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{indTick()}catch(e){console.error(e)}return r}}
function indWear(I){if(!S.corp)return;const r=I.at==='job'&&pjRunOf(I.run),s=S.sectors[r?r.sector:I.sector];for(const sl of I.sl||[]){if(sl.it&&Math.random()<CE.wear*IND.every/3600){const it=sl.it;sl.it=null;if(s)toDebris(s,{[it]:1});else inv.add(S.econ.stock.neutral,it,1)}}}
function indRateNews(I){const r=ratingOf(I);if(r>(I.r||1)){const r0=I.r||1;I.r=r;if(r>=6&&r0<6)indNews(`${I.name}, an independent out of ${S.stations[I.home]?S.stations[I.home].name:DEF[I.home].name}, has reached Contractor Rating 6.`)}}
function indNews(msg){try{if(newsOK()){newsAdd({f:'neutral',who:'Freeport Compact',msg},false);return}}catch(e){}allFeed(msg,'news')}
function indMove(I){
  if(I.at==='fly'){if(I.live||S.T<I.next)return;if(I.leg>=I.path.length-1){indArrive(I);return}I.leg++;I.sector=I.path[I.leg];I.next=S.T+IND.hop;if(WORLDS[I.sector])inW(WORLDS[I.sector],()=>indSpawn(I,true));return}
  if(I.at==='mine'){if(I.live)return;if(WORLDS[I.sector]&&indRoomW(WORLDS[I.sector])){inW(WORLDS[I.sector],()=>indSpawn(I,'rock'));if(I.live)return}
    const s=S.sectors[I.sector];I.macc=(I.macc||0)+indMineRate(I)/60*10;const n=Math.floor(I.macc);if(n>0&&s){I.macc-=n;const got=extract(s,Math.min(n,Math.ceil(indRoom(I))),true);inv.addAll(I.hold,got);if(!invMass(got))I.dry=(I.dry||0)+1}
    if(indRoom(I)<2||S.T>=(I.until||0)||(I.dry||0)>=3){I.dry=0;I.restT=S.T+rnd(IND.rest[0],IND.rest[1]);indDock(I,I.sector)}}}
function indRoomW(w){let n=0;for(const e of w.ents)if(e.npc&&e.role!=='drone')n++;return inW(w,()=>n<popCap())}
// leave the dock for sid; in an open system at the ship cap it waits docked (I.wait) and tries again next minute
function indGo(I,sid,go){const w=WORLDS[I.sector];if(w&&!indRoomW(w)){I.go=go;I.wait=sid;return false}I.wait=null;I.go=go;I.at='fly';I.path=trPath(I.sector,sid)||[I.sector];I.leg=0;I.next=S.T+IND.hop*.5;
  if(w)inW(w,()=>indSpawn(I,false));return true}
function indResume(I){const sid=I.wait;if(sid)indGo(I,sid,I.go)}
function indArrive(I){I.path=null;indDock(I,I.sector)}
// docked: a task's step here (deliver, buy at the source, sell trade goods), then rearm, sell what was taken out, shop, a hull
function indDock(I,sid){I.at='dock';I.sector=sid;I.live=false;I.wait=null;const R=S.stations[sid],mk=indMkt(R,I);if(I.go)indStep(I,R);if(I.at!=='dock')return;
  if(mk){indRearm(I,R);indSellAll(I,R,false,true);indShop(I,R);indHullUp(I,R)}if(!I.go)indDecide(I)}
function indStep(I,R){const g=I.go;if(!g)return;if(g.k==='trade'||g.k==='board'&&g.stage==='dst')I.restT=S.T+rnd(IND.rest[0],IND.rest[1]);
  if(g.k==='trade'){if(R&&R.sid===g.to&&indMkt(R,I)){indSell(I,R,g.item,I.hold[g.item]||0,Math.floor(g.bp*.97))}I.go=null;return}
  if(g.k==='board'){const k=(S.contracts||[]).find(x=>x.id===g.kid);if(g.stage==='src'){const D=R&&R.sid===g.src?R:null;let n=0;if(k&&D&&indMkt(D,I))n=indBuy(I,D,g.item,Math.min(g.n,k.n),Math.ceil(g.bp*1.15));
      if(!k||n<jobMin(k)){if(k&&k.ind===I.id)k.ind=null;I.go=null;return}g.n=n;g.stage='dst';I.go=null;if(!indGo(I,g.dst,g))I.go=g;return}
    if(R&&R.sid===g.dst&&k)indDeliver(I,k,R);else if(k&&k.ind===I.id)k.ind=null;I.go=null;return}
  I.go=null}
function indDeliver(I,k,R){const have=Math.min(k.n,I.hold[k.item]||0);if(have<Math.min(k.n,jobMin(k))){k.ind=null;return}k.n0=k.n0||k.n;const share=Math.round(k.reward*have/k.n),fr=have/k.n0;k.reward-=share;k.n-=have;
  inv.take(I.hold,k.item,have);inv.add((k.st&&S.stations[k.st]&&storeOf(S.stations[k.st]))||S.econ.stock[k.fac],k.item,have);if(I.hb&&!(I.hold[k.item]>0))delete I.hb[k.item];
  if(k.blk){const R2=S.stations[k.st];if(R2&&R2.hMax)R2.hull=Math.min(R2.hMax,(R2.hull||0)+R2.hMax*.1*fr)}
  const got=transfer(k.fac,indW(I),share);I.earn=(I.earn||0)+got;I.jobs++;{const t=indS().tot=indS().tot||{};t[k.blk?'blk':k.st?'fpreq':'sup']=(t[k.blk?'blk':k.st?'fpreq':'sup']||0)+got}if(STAND_POW.includes(k.fac))standWork(I,k.fac,(STAND.contract+share/1500)*(k.blk?2:1),'a delivery');else rpAdd(I,IND.rp,'a delivery');
  k.ind=null;if(k.n<=0)S.contracts=S.contracts.filter(x=>x!==k)}
function indRearm(I,R){if(!I.fought)return;I.fought=0;const c=Math.min(indPurse(I),I.line==='guard'?IND.rearm.guard:IND.rearm.other);if(c>0)I.spent=(I.spent||0)+transfer(indW(I),indWl(R),c)}
// ---- what it does next, docked and idle
function indDecide(I){if(I.at!=='dock'||I.go||I.dead)return;const R=S.stations[I.sector],mk=indMkt(R,I);
  if(mk&&S.T>=(I.shopT||0)){I.shopT=S.T+IND.shopT;indShop(I,R);indHullUp(I,R)}
  if(S.T<(I.restT||0))return;const rich=indPurse(I)>indRich(I);
  if(!rich&&indBoardTry(I))return;
  if(mk&&invMass(I.hold)>0)indSellAll(I,R,I.line==='mine');
  if(I.line==='mine'){if(I.sector!==I.home){indGo(I,I.home,{k:'home'});return}if(rich)return;const s=S.sectors[I.sector];if(!s||!s.ast.some(a=>!a.comet&&oreTotal(a)>0))return;
    const w=WORLDS[I.sector];if(w&&!indRoomW(w))return;I.at='mine';I.until=S.T+IND.mineMax;I.dry=0;if(w)inW(w,()=>indSpawn(I,false));return}
  if(!rich&&mk&&indTradeTry(I,R))return;
  if(I.sector!==I.home&&!mk){indGo(I,I.home,{k:'home'});return}
  if(I.sector!==I.home&&Math.random()<.5){indGo(I,I.home,{k:'home'});return}
  if(!rich&&Math.random()<IND.look){const L=indMarkets(I).filter(x=>x.sid!==I.sector&&indHop(I.sector,x.sid)<=3);if(L.length)indGo(I,pick(L).sid,{k:'look'})}}
// trade: the best lot from here to a market within 4 jumps whose sell price beats the buy price by the margin, by profit a jump
function indTradeTry(I,A){const room=indRoom(I),budget=Math.min(IND.lotCr,indPurse(I)-IND.keep);if(room<2||budget<50)return false;const st=mkStock(A);let best=null,bv=0;
  const Ms=indMarkets(I).filter(B=>B!==A&&indHop(A.sid,B.sid)<=IND.tradeHops);if(!Ms.length)return false;
  for(const k of IND_GOODS){const s=st[k]||0;if(s<3||FP_ONLY.has(k)&&!isFreeF(A)||!indSurplus(A,k))continue;const bp=indBuyP(A,k,I.cls),cap=Math.min(Math.floor(room/mass(k)),Math.floor(budget/bp),Math.floor(s*.5));if(cap<1)continue;
    // the price margin first (cheap), the lots only for routes that clear it
    const Bs=[];for(const B of Ms){if(k==='matrix'&&!isFreeF(B))continue;const sp=indSellP(B,k,I.cls);if(sp>=bp*(1+IND.margin)&&(sp-bp)*cap>=IND.minProfit)Bs.push([B,sp])}if(!Bs.length)continue;
    const lot=indLot(A,k,-1,cap,I.cls);if(lot<1)continue;
    for(const[B,sp]of Bs){const n=Math.min(lot,indLot(B,k,1,lot,I.cls),Math.floor((S.econ.treasury[indWl(B)]||0)/sp));if(n<1)continue;
      const prof=(sp-bp)*n,v=prof/(indHop(I.sector,A.sid)+indHop(A.sid,B.sid)+1);if(prof>=IND.minProfit&&v>bv){bv=v;best={k,n,B,bp}}}}
  if(!best)return false;const w=WORLDS[I.sector];if(w&&!indRoomW(w))return false;const got=indBuy(I,A,best.k,best.n,best.bp);if(!got)return false;
  return indGo(I,best.B.sid,{k:'trade',item:best.k,bp:best.bp,to:best.B.sid})}
// ---- the boards' jobs: untaken for 8 minutes (no delivery to it in that time) and nobody else's
function indStamp(){for(const k of S.contracts||[])if(k.iT==null||k.iN!==k.n){k.iT=S.T;k.iN=k.n}}
function indBoardOpen(k){return S.T-(k.iT==null?S.T:k.iT)>=IND.board&&!(k.ind&&indOf(k.ind))}
function indNearOwn(sid,f){let best=null,bh=99;for(const id in S.stations){const R=S.stations[id];if(!R||R.owner!==f)continue;const h=indHop(sid,id);if(h<bh){bh=h;best=R}}return best}
function indBoardTry(I){if(S.unb||!S.contracts)return false;const room=indRoom(I),budget=indPurse(I)-IND.keep;let best=null,bv=0;
  for(const k of S.contracts){if(!k.item||!ITEMS[k.item]||!(k.n>0)||!indBoardOpen(k))continue;const blk=!!k.blk,fp=k.fac==='neutral'&&!!k.st&&!blk,sup=!k.st&&!blk&&FAC_IDS.includes(k.fac);if(!fp&&!blk&&!sup)continue;
    if(FAC_IDS.includes(k.fac)&&standOf(k.fac,I)<STAND.dock)continue;const left=(k.until||0)-S.T,mn=Math.min(k.n,jobMin(k)),ms=Math.max(.01,mass(k.item));
    if(sup){if(I.line!=='mine')continue;const have=Math.min(k.n,I.hold[k.item]||0);if(have<mn)continue;const D=indNearOwn(I.sector,k.fac);if(!D)continue;const h=indHop(I.sector,D.sid);if(h*IND.hop+60>left)continue;
      const v=Math.round(k.reward*have/k.n)/(h+1);if(v>bv){bv=v;best={k,n:have,src:null,dst:D.sid,bp:0}}continue}
    const dst=k.st;if(!S.stations[dst])continue;
    for(const Q of indMarkets(I)){if(Q.sid===dst)continue;const s=mkStock(Q)[k.item]||0;if(s<mn||!indSurplus(Q,k.item))continue;if(FP_ONLY.has(k.item)&&!isFreeF(Q))continue;const bp=indBuyP(Q,k.item,I.cls),n=Math.min(k.n,Math.floor(room/ms),Math.floor(budget/bp),Math.floor(s*.6));if(n<mn)continue;
      const h=indHop(I.sector,Q.sid)+indHop(Q.sid,dst);if(h*IND.hop+90>left)continue;const prof=Math.round(k.reward*n/k.n)-n*bp;if(prof<IND.minProfit)continue;const v=prof/(h+1);if(v>bv){bv=v;best={k,n,src:Q.sid,dst,bp}}}}
  if(!best)return false;const k=best.k,g={k:'board',kid:k.id,item:k.item,n:best.n,src:best.src,dst:best.dst,bp:best.bp,stage:best.src?'src':'dst',T:S.T};k.ind=I.id;
  if(g.stage==='src'&&g.src===I.sector){I.go=g;indStep(I,S.stations[I.sector]);return true}
  indGo(I,g.stage==='src'?g.src:g.dst,g);return true}
// ---- buying parts and systems, as you do, off the shelf at the Market's price, the maker paid
const IND_SYS={haul:['cargo','engine','shield','armor','power','weapon','drill','payload'],mine:['drill','cargo','power','shield','engine','armor','weapon','payload'],guard:['weapon','shield','engine','armor','power','payload','cargo','drill']};
const IND_WORK={haul:['cargo','dronec','gun','laser'],mine:['mlaser','charge','gun','laser','scanner'],guard:['gun','laser','missile']};
function indSlotOrder(I){const w=IND_WORK[I.line]||[],L=(I.sl||[]).slice();return L.sort((a,b)=>{const x=w.indexOf(a.k),y=w.indexOf(b.k);return(x<0?9:x)-(y<0?9:y)||(a.it?1:0)-(b.it?1:0)})}
function indSysBest(R,sl,gcap,budget,cls,cur){const ms=mkStock(R),C=cur&&ITEMS[cur],cg=C?(C.grade||1):0,cb=!!(C&&C.maker);let best=null,bs=-1;
  for(const id in ms){const it=ITEMS[id];if(!it||!it.maker||it.sys!==sl||!(ms[id]>0))continue;const g=it.grade||1;if(g>gcap||g<cg||(cb&&g<=cg))continue;const pr=mkPartPrice(R,id,cls);if(pr>budget)continue;
    const sc=(1+.35*(g-1))/Math.pow(pr/Math.max(1,baseValue(id)),.5);if(sc>bs){bs=sc;best=id}}return best}
// swap the fitted `old` for `id` off R's shelf: the old one sold back to the market (or into the hold if its treasury can't
// pay), the new one bought; returns what is fitted afterwards
function indSwap(I,R,old,id){const t=indS().tot=indS().tot||{};const w=indW(I),wl=indWl(R),pr=mkPartPrice(R,id,I.cls),back=old?mkPartSell(R,old,I.cls):0,sell=!!old&&(S.econ.treasury[wl]||0)>=back;if(indPurse(I)+(sell?back:0)<pr)return old;
  if(old){const tmp={[old]:1};if(!(sell&&mkSellOne(R,old,w,I.cls,tmp)))inv.add(I.hold,old,1)}const got=mkBuyOne(R,id,w,I.cls,{});if(got){I.spent=(I.spent||0)+got;t.parts=(t.parts||0)+got;t.nparts=(t.nparts||0)+1;return id}
  if(old&&I.hold[old]>0){inv.take(I.hold,old,1);return old}return null}
function indShop(I,R){if(!S.corp||!R)return 0;const res=indReserve(I),gc=gradeCap(I);let n=0;
  for(const s of indSlotOrder(I)){if(n>=IND.perVisit)break;const budget=indPurse(I)-res;if(budget<=0)break;const C=s.it&&ITEMS[s.it],cb=!!(C&&C.maker),back=C?mkPartSell(R,s.it,I.cls):0;
    const id=aipBest(R,[s.k],gc,budget+back,I.cls,cb?(C.grade||1):0);if(!id)continue;s.it=indSwap(I,R,s.it,id);if(s.it===id)n++}
  for(const sl of IND_SYS[I.line]||[]){if(n>=IND.perVisit)break;const budget=indPurse(I)-res;if(budget<=0)break;const cur=I.sys[sl],back=cur?mkPartSell(R,cur,I.cls):0,id=indSysBest(R,sl,gc,budget+back,I.cls,cur);if(!id)continue;
    I.sys[sl]=indSwap(I,R,cur,id);if(I.sys[sl]===id)n++}
  return n}
// the next hull of its line at a freeport yard, at Rating 2 and 5, when the purse holds its price and the reserve: the parts
// move across into slots that take them, the rest go to the hold to be sold; drones bought for the bigger bay
function indHullUp(I,R){if(!isFreeF(R))return false;const nx=IND.next[I.cls];if(!nx||ratingOf(I)<(HULL_RATING[nx]||1))return false;const pr=hullPrice(nx);if(indPurse(I)<pr+indReserve(I))return false;
  if(invMass(I.hold)>shipStats('neutral',nx,indT(I)).cargo)return false;if(transfer(indW(I),indWl(R),pr)<pr)return false;I.spent=(I.spent||0)+pr;
  const D=slotsOf(nx,null),N=[...D.w.map(k=>({g:'w',k,it:null})),...D.u.map(k=>({g:'u',k,it:null}))];for(const s of I.sl||[]){if(!s.it)continue;const t=N.find(x=>!x.it&&x.k===s.k);if(t)t.it=s.it;else inv.add(I.hold,s.it,1)}
  I.sl=N;I.cls=nx;const want=(CLASSES[nx].drones||0)-((I.hull&&I.hull.drone)||0);if(want>0){const m=indBuy(I,R,'drone',want);if(m){inv.take(I.hold,'drone',m);I.hull.drone=(I.hull.drone||0)+m}}
  if(covered(R.sid)||(W&&W.sid===R.sid))feed(`${I.name}, an independent, now flies a ${CLASSES[nx].name}.`,'info');return true}
// ---- the posted jobs (16zf_posted.js, 16zzr_contract.js): the nearest free independent whose hull fits takes one
function indFits(I,kind){return kind==='mine'?I.line==='mine':kind==='guard'?I.line==='guard':I.line==='haul'}
function indFree(I){return!I.dead&&!I.live&&I.at!=='job'&&!(I.go&&(I.go.k==='board'||I.go.k==='trade'))}
function indTake(j){const R=S.stations[j.sid];if(!R)return null;const P=xPilotOfKey(j.pid),s=j.kind==='supply'?pjSrc(R,j.item,'supply',P):null,start=j.kind==='supply'?(s&&s.D):R;if(!start)return null;
  const need=j.kind==='supply'||j.kind==='haul'?j.n*mass(j.item):0;let best=null,bv=1e9;for(const I of indL()){if(!indFits(I,j.kind)||!indFree(I))continue;const v=indHop(I.sector,start.sid)+(need>indCap(I)?.5:0);if(v<bv){bv=v;best=I}}return best}
{const o=pjTick;pjTick=function(){try{if(!NET.cl&&S&&indOn()){indInit();for(const j of pjList()){if(j.state!=='open'||S.T<j.claimAt)continue;const R=S.stations[j.sid];if(!R||R.owner!=='player')continue;const I=indTake(j);
    if(!I){j.claimAt=S.T+60;j.noInd=1;continue}if(I.at==='mine')I.at='dock';if(I.wait)I.wait=null;
    j.by=indW(I);j.who=`${I.name} (independent)`;j.ind=I.id;j.state='taken';j.due=1e12;j.noInd=0;I.go=null;I.at='job';keyFeed(j.pid,`📋 ${j.who} took your job: ${pjTitle(j)}.`,'info')}}}catch(e){console.error(e)}return o.apply(this,arguments)}}
// the run starts where the independent is: Supply flies to the market first and buys there, Haul to the depot to load
{const o=pjRunStart;pjRunStart=function(j){const I=j&&j.ind&&indOf(j.ind);if(j&&j.ind&&(!I||I.at!=='job')){pjRunEnd({job:j.id},false,'the independent was lost');return}if(!I)return o.apply(this,arguments);const R=S.stations[j.sid],P=xPilotOfKey(j.pid);if(!R||!P)return;let to=R.sid,pk=null,src=null;
  if(j.kind==='supply'){const s=pjSrc(R,j.item,'supply',P);if(!s){pjRunEnd({job:j.id},false,'no market has it');return}src=s.D.sid;to=src;pk='buy'}
  else if(j.kind==='haul'){if(!(R.stock[j.item]>0)){pjRunEnd({job:j.id},false,'nothing in the store to haul');return}pk='load'}
  const r={id:S.nextId++,job:j.id,kind:j.kind,side:'neutral',cls:I.cls,from:I.sector,to,dst:R.sid,depot:R.sid,path:trPath(I.sector,to)||[I.sector],leg:0,sector:I.sector,next:S.T+PJR.hop*.5,load:{},state:'go',cut:0,T0:S.T,ind:I.id,pick:pk,src};
  pjRuns().push(r);j.run=r.id;j.due=1e12;I.run=r.id;if(WORLDS[r.sector])inW(WORLDS[r.sector],()=>pjSpawn(r,false))}}
// at the first stop: buy the goods (Supply, at the poster's expense) or load them at the depot (Haul), as much as the hold takes
function pjPick(r){const j=pjJob(r),R=j&&S.stations[j.sid],P=j&&xPilotOfKey(j.pid),I=indOf(r.ind),cap=I?indCap(I):1e9;if(!j||!R||R.owner!=='player'||!P){r.pick=null;pjRunEnd(r,false,'the depot is gone');return}
  if(r.pick==='buy'){const D=S.stations[r.src];if(!D){r.pick=null;pjRunEnd(r,false,'the market is gone');return}const mk=mkStock(D),pr=Math.ceil(stPrice(D,j.item)),n=Math.min(j.n,mk[j.item]||0,Math.floor(P.credits/pr),Math.floor(cap/Math.max(.01,mass(j.item))));
    if(n<=0){r.pick=null;pjRunEnd(r,false,'nothing bought');return}inv.take(mk,j.item,n);r.load[j.item]=n;{const paid=payFrom(P,D.owner,n*pr);if(ITEMS[j.item].maker&&typeof ceSale==='function')ceSale(ITEMS[j.item].maker,j.item,n,paid,D.owner==='neutral'?'neutral':D.owner,D.sid)}
    eco(R,'jobs',-n*pr,`${n} ${ITEMS[j.item].name} bought at ${D.name}`);r.feeK0=n/j.n;r.pick=null;r.from=D.sid;r.to=R.sid;r.path=trPath(D.sid,R.sid)||[D.sid]}
  else if(r.pick==='load'){const s=pjSrc(R,j.item,'haul',P);if(!s){r.pick=null;pjRunEnd(r,false,'no market will take it');return}const n=Math.min(j.n,R.stock[j.item]||0,Math.floor(cap/Math.max(.01,mass(j.item))));
    if(n<=0){r.pick=null;pjRunEnd(r,false,'nothing in the store to haul');return}inv.take(R.stock,j.item,n);r.load[j.item]=n;r.feeK0=n/j.n;r.pick=null;r.from=R.sid;r.to=s.D.sid;r.dst=s.D.sid;r.path=trPath(R.sid,s.D.sid)||[R.sid]}
  else{r.pick=null;return}
  r.leg=0;r.sector=r.path[0];r.next=S.T+PJR.hop*.5;if(WORLDS[r.sector]&&!r.live)inW(WORLDS[r.sector],()=>pjSpawn(r,false))}
{const o=pjArrive;pjArrive=function(r){if(r&&r.pick){pjPick(r);return}return o.apply(this,arguments)}}
// the job over: the fee scaled to what the hold could take, a Rating point or so, and the independent free where it ended
{const o=pjRunEnd;pjRunEnd=function(r,ok,why){const j=r&&pjJob(r),id=(r&&r.ind)||(j&&j.ind),I=id?indOf(id):null,was=!!j&&j.state!=='done';if(r&&r.feeK0!=null)r.feeK=(r.feeK!=null?r.feeK:1)*r.feeK0;
  const x=o.apply(this,arguments);try{if(I&&was&&!I.dead&&I.at==='job'){if(ok){I.jobs++;rpAdd(I,IND.rp,'a posted job');I.earn=(I.earn||0)+(j.paid||0)}I.run=null;const sid=(r&&r.sector)||I.sector;I.sector=sid;
    const e=r&&r.live?indEntIn(WORLDS[sid],I):null;if(e){e.pjRun=null;e.pjName=null;e.home='ind:'+I.id;e.role=I.line==='guard'?'patrol':'hauler';I.live=true;I.at='fly';I.go={k:'home'};I.path=trPath(sid,I.home)||[sid];I.leg=0;e.indLbl=indLabel(I)}
    else if(S.stations[sid]){I.at='dock';I.go=null}else{I.at='dock';I.go=null;indGo(I,I.home,{k:'home'})}}}catch(e){console.error(e)}return x}}
function indEntIn(w,I){if(!w)return null;return w.ents.find(e=>e.indId===I.id&&e.alive)||null}
// the run's ship is the independent's: its stats, its name
{const o=pjSpawn;pjSpawn=function(r){const e=o.apply(this,arguments);try{const I=e&&r&&r.ind&&indOf(r.ind);if(I){e.indId=I.id;indFly(e,I);e.indLbl=indLabel(I,r.kind)}}catch(err){console.error(err)}return e}}
// ---- live: its own flights and mining
function indJob(I,kind){if(kind)return PJB.kinds[kind]||'On a job';const g=I.go;if(I.at==='mine')return'Mining';if(I.at==='job'){const r=pjRunOf(I.run);return r?PJB.kinds[r.kind]:'On a job'}
  if(g&&g.k==='trade')return'Trading';if(g&&g.k==='board'){const k=(S.contracts||[]).find(x=>x.id===g.kid);return k&&k.blk?'Blockade run':k&&k.fac==='neutral'?'Freeport request':'Supply contract'}if(g&&g.k==='home')return'Heading home';return'Between jobs'}
function indLabel(I,kind){return`Independent · ${I.name} · ${indJob(I,kind)}`}
function indSpawn(I,how){if(I.live||!W)return null;const role=I.at==='mine'?'miner':I.line==='guard'?'patrol':'hauler',e=makeNPC(role,'neutral',I.cls,1,{},'ind:'+I.id);indFly(e,I);e.cargo=I.hold;I.hold={};e.indId=I.id;e.indLbl=indLabel(I);I.live=true;
  const gs=GATES[W.sid]||[],SE=W.stationEnt;let placed=false;
  if(I.at==='fly'){const prev=I.path[I.leg-1],gin=gs.find(g=>g.to===prev);if(how===true&&gin){e.x=gin.x*.93;e.y=gin.y*.93;e.z=gin.z*.93;fxWarp(e,sideCol('neutral'));placed=true}}
  if(!placed&&how==='rock'){const a=S.sectors[W.sid].ast.find(x=>!x.comet&&oreTotal(x)>0);if(a){const o=rdir(1),r=astR(a)+200;e.x=a.x+o.x*r;e.y=a.y+o.y*r;e.z=a.z+o.z*r;placed=true}}
  if(!placed&&SE){const o=rdir(1);e.x=SE.x+o.x*300;e.y=SE.y+o.y*100;e.z=SE.z+o.z*300;placed=true}
  if(!placed){const g=pick(gs);if(g){e.x=g.x*.9;e.y=g.y*.9;e.z=g.z*.9}}
  faceInstant(e,-e.x,-e.y,-e.z);W.ents.push(e);return e}
{const o=npcThink;npcThink=function(e,dt){if(e.indId&&!e.pjRun&&!NET.cl){const I=indOf(e.indId);if(!I||!I.live||I.dead){e.indId=null;e.role='leave';return o.apply(this,arguments)}
  if(I.line==='guard'&&W.t-e.lastHit<6){e.role='patrol';return o.apply(this,arguments)}e.ai.t-=dt;e.life+=dt;const SE=W.stationEnt;
  if(I.at==='fly'){e.mining=null;if(I.leg<I.path.length-1){const g=W.ents.find(x=>x.type==='gate'&&x.to===I.path[I.leg+1]);if(g){npcGateJump(e,g,dt,.8);return}}
    if(SE){const d=steer(e,SE.x,SE.y,SE.z,dt,true,.8);faceTo(e,SE,dt);if(d<(SE.r||150)+60){e.indDock=1;despawn(e)}return}e.indDock=1;despawn(e);return}
  if(I.at==='mine'){const s=S.sectors[W.sid],full=invMass(e.cargo)>=Math.max(1,e.st.cargo-2)||S.T>=(I.until||0);
    if(full){e.mining=null;if(SE){const d=steer(e,SE.x,SE.y,SE.z,dt,true);faceTo(e,SE,dt);if(d<(SE.r||150)+60){e.indDock=1;despawn(e)}return}e.indDock=1;despawn(e);return}
    let a=e.ai.ast;if(!a||!s.ast.includes(a)||oreTotal(a)<=0){a=s.ast.filter(x=>!x.comet&&oreTotal(x)>0).sort((p,q)=>d3(p,e)-d3(q,e))[0];e.ai.ast=a}if(!a){I.until=S.T;return}
    const rr=astR(a)+120,d=d3(a,e);if(d>rr+60){e.mining=null;steer(e,a.x,a.y,a.z,dt,true);faceTo(e,a,dt);return}brake(e,dt);faceTo(e,a,dt);e.mining=a;e.mineAcc=(e.mineAcc||0)+indMineRate(I)/60*dt;
    while(e.mineAcc>=1){e.mineAcc-=1;const k=mainOre(a);if(!k)break;a.ore[k]--;if(!a.ore[k])delete a.ore[k];inv.add(e.cargo,k,1);if(oreTotal(a)<=0){removeAst(s,a);e.ai.ast=null;break}}return}
  e.indId=null;e.role='leave';return o.apply(this,arguments)}return o.apply(this,arguments)}}
// out of the world: the hold comes back aboard (default returnHome via 'ind:<id>'), then a gate means the next hop, the
// station means docked; a system closing leaves it flying or mining out of sight
{const o=returnHome;returnHome=function(e){const id=e&&e.indId&&!e.pjRun?e.indId:null;const x=o.apply(this,arguments);if(id){try{const I=indOf(id);if(I&&I.live){I.live=false;
    if(I.at==='fly'){if(e.indDock){I.leg=I.path.length-1;indArrive(I)}else if(e.gj&&I.leg<I.path.length-1){I.leg++;I.sector=I.path[I.leg];I.next=S.T+IND.hop;if(WORLDS[I.sector])inW(WORLDS[I.sector],()=>indSpawn(I,true))}}
    else if(I.at==='mine'&&e.indDock){I.restT=S.T+rnd(IND.rest[0],IND.rest[1]);indDock(I,I.sector)}}}catch(err){console.error(err)}}return x}}
{const o=holderIn;holderIn=function(st,path){if(typeof path==='string'&&path.startsWith('ind:')){const I=((st.ind&&st.ind.L)||[]).find(x=>String(x.id)===path.slice(4));return I?(I.hold=I.hold||{}):st.econ.stock.neutral}return o.apply(this,arguments)}}
{const o=openWorld;openWorld=function(sid){const w=o.apply(this,arguments);try{if(!NET.cl&&S&&S.ind)inW(w,()=>{for(const I of indL())if(!I.live&&I.sector===sid&&(I.at==='fly'||I.at==='mine')&&indRoomW(w))indSpawn(I,I.at==='mine'?'rock':false)})}catch(e){console.error(e)}return w}}
{const o=migrate;migrate=function(st){const r=o.apply(this,arguments);try{for(const I of((st&&st.ind&&st.ind.L)||[]))I.live=false}catch(e){}return r}}
// ---- loss: free-for-all (no standing), its ship salvage, a rebuy at home or retirement
{const o=dmgRec;dmgRec=function(e){if(e&&e.indId){const I=indOf(e.indId);if(I)I.fought=1;const sd=e.side;e.side='indep';try{return o.apply(this,arguments)}finally{e.side=sd}}return o.apply(this,arguments)}}
{const o=killShip;killShip=function(e,src,at){const I=e&&e.indId&&e.role!=='limpet'&&e.alive?indOf(e.indId):null;if(I){try{inv.addAll(e.load,indItems(I));inv.addAll(e.load,I.hull||{});inv.addAll(e.load,I.hold||{});I.sys={};I.sl=[];I.hull={};I.hold={};I.dead=1}catch(err){console.error(err)}}
  const x=o.apply(this,arguments);if(I&&!e.alive){try{indLost(I,src)}catch(err){console.error(err)}}else if(I)I.dead=0;return x}}
function indLost(I,src){const where=DEF[(W&&W.sid)||I.sector].name;I.live=false;I.lost=(I.lost||0)+1;I.run=null;if(I.go&&I.go.kid){const k=(S.contracts||[]).find(x=>x.id===I.go.kid);if(k&&k.ind===I.id)k.ind=null}I.go=null;I.wait=null;I.hb={};
  if(sideNorm(src)==='pirate')indNews(`${I.name}, an independent pilot, was lost to the Unbound in ${where}.`);
  const homes=[I.home,...FREEPORTS.map(F=>F.sid).filter(s=>s!==I.home&&indHomeN(s)<IND.max)];
  for(const sid of homes){const R=S.stations[sid];if(isFreeF(R)&&indBuild(I,IND.light[I.line],R,true)){I.home=sid;I.sector=sid;I.at='dock';I.dead=0;
    if(covered(sid)||(W&&W.sid===sid))feed(`${I.name}, an independent, was shot down in ${where} and has bought a new ${CLASSES[I.cls].name} at ${R.name}.`,'info');return}}
  indRetire(I,`shot down in ${where}`)}
function indRetire(I,why){const R=S.stations[I.home],s=S.sectors[I.sector];transfer(indW(I),'neutral',indPurse(I));delete S.econ.treasury[indW(I)];
  const rest={...indItems(I),...(I.hull||{})};inv.addAll(rest,I.hold||{});if(Object.keys(rest).length){if(isFreeF(R))inv.addAll(mkStock(R),rest);else if(s)toDebris(s,rest);else inv.addAll(S.econ.stock.neutral,rest)}
  I.sys={};I.sl=[];I.hull={};I.hold={};indS().L=indL().filter(x=>x!==I);if(covered(I.home)||(W&&W.sid===I.home))feed(`${I.name}, an independent pilot (${why}), has retired.`,'info')}
// ---- the books: their ships and holds are in the ledger (their purses are wallets, counted with the treasuries)
{const o=ledger;ledger=function(){const r=o.apply(this,arguments);try{const L=r.L['Fleets in muster'];for(const I of(S.ind&&S.ind.L)||[]){const v=invVec(indItems(I));invVec(I.hull||{},v);invVec(I.hold||{},v);for(const e of RAWS){L[e]+=v[e];r.tot[e]+=v[e]}}}catch(e){}return r}}
// ---- seen: labels (the guest takes the label from the host's ship row), the freeport's Overview
{const o=shipLabel;shipLabel=function(e){if(e&&e.indLbl)return e.indLbl;return o.apply(this,arguments)}}
{const o=shipRow;shipRow=function(e,full){const r=o.apply(this,arguments);if(full&&e&&e.indLbl&&Array.isArray(r))r[7]=e.indLbl;return r}}
{const o=mkPup;mkPup=function(r){const e=o.apply(this,arguments);try{if(e&&typeof r[7]==='string'&&r[7].startsWith('Independent · '))e.indLbl=r[7]}catch(err){}return e}}
function indDockedHtml(sid){const L=((S.ind&&S.ind.L)||[]).filter(I=>I.sector===sid&&(I.at==='dock'||I.at==='mine'));if(!L.length&&!((S.ind&&S.ind.L)||[]).some(I=>I.home===sid))return'';
  const W2={haul:'hauler',mine:'miner',guard:'fighter'};let h=`<div class="h3" style="margin-top:14px">Independents here</div>`;
  if(!L.length)return h+`<div class="note">None docked just now; ${((S.ind&&S.ind.L)||[]).filter(I=>I.home===sid).length} call this freeport home.</div>`;
  return h+`<div class="tblw"><table class="t"><tbody>${L.map(I=>`<tr><td class="iname">${esc(I.name)}</td><td>${esc(CLASSES[I.cls]?CLASSES[I.cls].name:I.cls)} · ${W2[I.line]}</td><td class="note">Rating ${ratingOf(I)}${I.home===sid?' · home':''}</td><td class="note">${esc(I.at==='mine'?'mining the field':I.go&&I.wait?'waiting to launch':'between jobs')}</td></tr>`).join('')}</tbody></table></div>`}
{const o=homeHtml;homeHtml=function(c,P){let h=o.apply(this,arguments);try{if(c&&c.owner==='neutral'&&!S.unb&&!S.training&&P&&isFreeF(S.stations[P.sector]))h+=indDockedHtml(P.sector)}catch(e){console.error(e)}return h}}
