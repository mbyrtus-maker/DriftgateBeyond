//@src 16zzzc_indep.js
// ============================================================ Beyond: independent pilots (agreed 7 Nov 2026, built 7 Nov 2026)
// A standing population of independent AI contractors living the player's life on a small scale (BEYOND_DESIGN.md,
// "Proposal: independent pilots" and "Independent pilots: agreed"). Each is a tracked pilot (S.ind.list) with a name, a home
// freeport, a hull and its fitted makers' parts (I.kit), a hold (I.hold), a purse (wallet ind_<id> in S.econ.treasury), a
// Contractor Rating (I.rp) and standing with the powers (I.stand), and a personality (I.pt, 16zzzd_ptraits.js).
//   Arrival: 4 per freeport at the start; a newcomer every 20 to 40 minutes while a freeport has fewer than 4 (6 at most,
//            18 a galaxy). A newcomer flies a free light hull (a starter, as yours), has a stake of 1,500 cr moved from the
//            Compact's treasury (credits zero-sum) and fits its first parts off its freeport's shelf with it.
//   Work:    posted jobs (Supply, Haul, Mine, Guard) go to the nearest free independent whose hull fits (the one-off Compact
//            contractor only when none is free), flown by the same tracked run (16zzr_contract.js) and paid into its purse;
//            the boards' jobs (freeport requests, blockade and containment runs, the powers' ore orders) once a job has gone
//            untaken for 8 minutes; between jobs a hauler makes supply runs (buys only at a freeport, sells anywhere where the
//            margin beats the fees: goods go into the powers, never out of their warehouses) and a miner mines real rock.
//   Buying:  as a pilot does, only at freeports, above a reserve (400 cr plus a rebuy of its hull): a part for every weapon and
//            utility slot, upgraded up to its Rating (best value by traits, grade and price), a system grade a visit (goods off
//            the market plus the 8% fee), worn parts replaced; it saves first for the next hull of its line when its Rating allows.
//            A sale into a power's or a freeport's market counts as work (Rating points, standing).
//   Risk:    it flies the lanes and can be shot down like any ship, live or (in Brood-held systems and pirate dens) out of
//            sight. Shot down, it loses its hull, kit and hold (salvage where it fell); after 5 minutes it rebuys a hull at
//            home if it has the money (its lost hull, else a free light hull), with a new trait learned from how it died,
//            or retires and its purse goes to the Compact. Shooting one costs no standing with anyone (the user: a
//            free-for-all for now).
// Everything moves exactly: goods only between stores, holds, kits, rocks and debris; credits only between wallets.
const IND={trade:true,start:4,cap:6,max:18,arrive:[1200,2400],stake:1500,reserve:400,hop:45,pass:60,back:300,boardAge:480,minProfit:60,minPurse:300,
  mineT:{skiff:3,prospector:5,dredger:7},fill:.9,
  line:{fighter:['interceptor','striker','heavy'],miner:['skiff','prospector','dredger'],hauler:['courier','freighter','bulker']},
  slots:{hauler:[['cargo']],miner:[['mlaser']],fighter:[['laser','gun']]},sys:{hauler:['cargo','engine','armor','shield'],miner:['drill','cargo','armor','shield'],fighter:['weapon','shield','armor','engine']},buys:3,risk:{brood:.06,den:.05,near:.015}};
const IND_GOODS=['fe','cu','ir','xc','au','nu','plate','wire','coil','lattice','core','missile','drone'];
const IND_FIRST=['Mara','Tobin','Ilse','Corvin','Neve','Bastian','Yara','Dorran','Petra','Halvard','Isolde','Rhett','Sunniva','Cato','Liesel','Emeric','Ondine','Ferris','Greta','Joss','Anouk','Silas','Thea','Wolf'];
const IND_LAST=['Venn','Okafor','Brask','Lindqvist','Moreau','Kade','Szabo','Ferreira','Thorne','Abara','Kowal','Hesketh','Duval','Rourke','Vasquez','Ingram','Nakai','Sorel','Petrakis','Wyle'];
let IND_HOLD=null;
function indOn(){return!!(S&&!S.training&&!S.unb&&!NET.cl)}
function indAll(){S.ind=S.ind||{list:[],arr:{}};return S.ind.list}
function indById(id){return indAll().find(I=>String(I.id)===String(id))||null}
function indW(I){return'ind_'+I.id}
function indStore(I){const R=S.stations[I.port];return R&&R.owner==='neutral'?dStore(R):S.econ.stock.pirate}
function indPurse(I){return S.econ.treasury[indW(I)]||0}
function indPorts(){return FREEPORTS.map(f=>f.sid).filter(sid=>S.stations[sid]&&S.stations[sid].owner==='neutral')}
function indRoleOfJob(kind){return kind==='guard'?'fighter':kind==='mine'?'miner':'hauler'}
function indAlive(I){return I.st!=='down'}
function indDoing(I){const r=I.run;if(I.st==='pj')return'On a job';if(I.st==='down')return'Shot down';if(I.st==='work')return'Mining';if(I.st==='dock')return'Docked';
  return r&&r.k==='trade'?'Trading':r&&r.k==='board'?'Delivering':r&&r.k==='mine'?'Off to mine':'Heading home'}
function indLabel(I){return`Independent · ${I.name} · ${indDoing(I)}${I.pt?' · '+ptName(I.pt):''}`}
function indName(){const used=new Set(indAll().map(I=>I.name));for(let i=0;i<40;i++){const n=pick(IND_FIRST)+' '+pick(IND_LAST);if(!used.has(n))return n}return pick(IND_FIRST)+' '+pick(IND_LAST)+' '+ri(2,9)}
function indCargo(I){return shipStats(null,I.cls,indGrades(I)||baseTiers()).cargo}
function indTiers(I){return I.tiers=I.tiers||{engine:1,power:1,shield:1,weapon:1,armor:1,drill:1,cargo:1,payload:1}}
// the goods an independent's system upgrades hold (in the ship, as yours are)
function indSysInv(I){const o={};for(const sl in I.tiers||{})for(let k=2;k<=(I.tiers[sl]||1);k++){const r=upgRecipe(sl,k);for(const i in r)o[i]=(o[i]||0)+r[i]}return o}
function indFree(R){return!!R&&R.owner==='neutral'&&R.kind==='free'}
function indGrades(I){const T={...indTiers(I)};let any=Object.values(T).some(v=>v>1);
  for(const id in I.kit||{}){const It=ITEMS[id];if(!It||!(I.kit[id]>0))continue;const g=It.grade||1,sl=It.part==='cargo'?'cargo':It.part==='mlaser'?'drill':It.part==='gun'||It.part==='laser'?'weapon':null;if(sl&&g>T[sl]){T[sl]=g;any=true}}return any?T:null}
function indFly(e,I){const T=indGrades(I);if(T){e.st=shipStats(e.fac,e.cls,T);e.hull=e.st.hull;e.shield=e.st.sCap;e.energy=e.st.eCap}return e}
// a market an independent may use: the freeports always; a power's station unless the power counts it hostile
function indMarketOK(I,R){if(!R)return false;if(R.owner==='neutral')return R.kind==='free';if(!FAC_IDS.includes(R.owner))return false;if(ptHas(I,'Smuggler'))return false;return(I.stand[R.owner]||0)>STAND.dock}
// how dangerous a system is to fly through out of sight (Brood space, pirate dens, and next to them)
function indDanger(sid){if(broodHeld(sid))return IND.risk.brood;if(DEF[sid]&&DEF[sid].kind==='den')return IND.risk.den;if((NEIGH[sid]||[]).some(n=>broodHeld(n)||(DEF[n]&&DEF[n].kind==='den')))return IND.risk.near;return 0}
// a path: the shortest, or one that keeps out of danger (Safe Routes, Convoy Only), or a different one from last time (Route Changer)
function indPath(I,a,b){if(a===b)return[a];const avoid=ptHas(I,'Safe Routes')||ptHas(I,'Convoy Only')||ptHas(I,'Edge Walker'),alt=ptHas(I,'Route Changer');
  if(avoid||alt){const cost=s=>1+(avoid?indDanger(s)*60:0)+(alt&&I.lastPath&&I.lastPath.includes(s)&&s!==a&&s!==b?2:0);const dist={[a]:0},prev={},open=[a];
    while(open.length){open.sort((x,y)=>dist[x]-dist[y]);const u=open.shift();if(u===b)break;for(const v of NEIGH[u]||[]){const d=dist[u]+cost(v);if(dist[v]==null||d<dist[v]){dist[v]=d;prev[v]=u;if(!open.includes(v))open.push(v)}}}
    if(dist[b]!=null){const p=[b];let c=b;while(c!==a){c=prev[c];p.unshift(c)}I.lastPath=p;return p}}
  const p=trPath(a,b)||[a];I.lastPath=p;return p}
function indHops(a,b){return a===b?0:(HOP[a]&&HOP[a][b]!=null?HOP[a][b]:99)}
// ---- arrival
function indNew(sid){if(indAll().filter(indAlive).length>=IND.max)return null;if((S.econ.treasury.neutral||0)<IND.stake)return null;
  const role=wpick({hauler:4,miner:3.5,fighter:2.5}),I={id:S.nextId++,name:indName(),port:sid,role,cls:IND.line[role][0],kit:{},hold:{},rp:0,stand:{halcyon:0,varkesh:0,ostrova:0},sector:sid,st:'dock',run:null,pt:null,deaths:0,born:S.T,jobs:0,earned:0,idleT:S.T};
  I.pt=ptRoll(role);indAll().push(I);transfer('neutral',indW(I),IND.stake);try{indShop(I,S.stations[sid])}catch(e){console.error(e)}return I}
function indArrivals(){const A=S.ind.arr;for(const sid of indPorts()){const n=indAll().filter(I=>indAlive(I)&&I.port===sid).length;
  if(A[sid]==null){for(let i=n;i<IND.start;i++)indNew(sid);A[sid]=S.T+rnd(IND.arrive[0],IND.arrive[1]);continue}
  if(S.T>=A[sid]){if(n<IND.start&&n<IND.cap)indNew(sid);A[sid]=S.T+rnd(IND.arrive[0],IND.arrive[1])}}}
// ---- buying parts and hulls, as a pilot does
// what a hull's slots want: a part for every weapon and utility slot (the landing kit and claim mounts aside)
function indWants(I){const D=slotsOf(I.cls),c={};for(const k of[...(D.w||[]),...(D.u||[])]){if(k==='land'||k==='claim')continue;c[k]=(c[k]||0)+1}return c}
function indSaving(I){const L=IND.line[I.role],nx=L[L.indexOf(I.cls)+1];return!!nx&&ratingOf(I)>=(HULL_RATING[nx]||1)&&indPurse(I)<hullPrice(nx)+IND.reserve+300}
// buying, as a pilot does, and only at a freeport: empty slots first, then upgrades (not while saving for the next hull)
function indShop(I,R){if(!indFree(R)||!S.corp)return 0;const w=indW(I),cls=I.cls,gcap=gradeCap(I),keep=IND.reserve+(START_HULLS.includes(cls)?0:hullPrice(cls)),want=indWants(I),save=indSaving(I);let n=0;
  const ofKind=k=>{const L=[];for(const id in I.kit)if(I.kit[id]>0&&ITEMS[id]&&ITEMS[id].part===k)for(let i=0;i<I.kit[id];i++)L.push(id);return L};
  for(const k in want){while(n<IND.buys&&ofKind(k).length<want[k]){const budget=indPurse(I)-keep;if(budget<=0)break;const id=aipBest(R,[k],gcap,budget,cls,0);if(!id||!mkBuyOne(R,id,w,cls,I.kit))break;n++}}
  if(!save)for(const k in want){if(n>=IND.buys)break;const L=ofKind(k);if(!L.length)continue;const low=L.sort((a,b)=>(ITEMS[a].grade||1)-(ITEMS[b].grade||1))[0],g=ITEMS[low].grade||1;
    const budget=indPurse(I)-keep;if(budget<=0)break;const id=aipBest(R,[k],gcap,budget+mkPartSell(R,low,cls),cls,g);if(!id)continue;if(mkSellOne(R,low,w,cls,I.kit)&&mkBuyOne(R,id,w,cls,I.kit))n++}
  if(!save)indSysUp(I,R);return n}
// one system grade a visit, as yours: the recipe's goods off the freeport's market and the station's 8% fee
function indSysUp(I,R){if(!indFree(R))return false;const T=indTiers(I),cap=Math.min(gradeCap(I),MK_TOP),keep=IND.reserve+(START_HULLS.includes(I.cls)?0:hullPrice(I.cls)),mk=mkStock(R);
  for(const sl of IND.sys[I.role]||[]){const t=T[sl]||1;if(t>=cap)continue;const r=upgRecipe(sl,t+1);let cost=0,ok=true;for(const k in r){if((mk[k]||0)<r[k]){ok=false;break}cost+=mkPartPrice(R,k,I.cls)*r[k]}if(!ok)continue;
    const fee=Math.ceil(invValue(r)*.08);if(indPurse(I)-keep<cost+fee)return false;const paid=transfer(indW(I),'neutral',cost+fee);if(paid<cost+fee){transfer('neutral',indW(I),paid);return false}
    for(const k in r)inv.take(mk,k,r[k]);T[sl]=t+1;return true}return false}
function indYardOK(R){return!!R&&((R.owner==='neutral'&&R.kind==='free')||(FAC_IDS.includes(R.owner)&&R.kind==='core'))}
function indUpgrade(I,R){if(!indYardOK(R)||!indMarketOK(I,R))return false;const L=IND.line[I.role],i=L.indexOf(I.cls),nx=L[i+1];if(!nx||ratingOf(I)<(HULL_RATING[nx]||1))return false;
  const pr=hullPrice(nx),old=I.cls,wl=R.owner==='neutral'?'neutral':R.owner;if(indPurse(I)<pr+IND.reserve+300)return false;if(transfer(indW(I),wl,pr)<pr)return false;
  const ti=START_HULLS.includes(old)?0:Math.floor(Math.min(hullPrice(old),I.paid==null?hullPrice(old):I.paid)*TRADE_IN);if(ti)transfer(wl,indW(I),ti);
  I.cls=nx;I.paid=pr;return true}
// ---- selling: the station's owner pays the Market's sell price for what it can afford; the rest stays aboard
function indSell(I,R,only){if(!R||!indMarketOK(I,R))return 0;const wl=R.owner==='neutral'?'neutral':R.owner,mk=mkStock(R);let got=0;
  for(const k of Object.keys(I.hold)){if(only&&k!==only)continue;if(I.res&&I.res[k])continue;const have=I.hold[k]||0;if(!have||!ITEMS[k])continue;const pr=mkPartSell(R,k,I.cls),n=Math.min(have,Math.floor((S.econ.treasury[wl]||0)/pr));if(n<=0)continue;
    inv.take(I.hold,k,n);inv.add(mk,k,n);got+=transfer(wl,indW(I),n*pr)}
  // a sale into a power's or a freeport's market is work for it: Rating points and standing
  if(got>0)indWork(I,R.owner,1+got/1500);I.earned+=got;return got}
function indBuy(I,R,k,n){const wl=R.owner==='neutral'?'neutral':R.owner,mk=mkStock(R),pr=mkPartPrice(R,k,I.cls);n=Math.min(n,mk[k]||0,Math.floor(indPurse(I)/pr),Math.floor((indCargo(I)-invMass(I.hold))/mass(k)));if(n<=0)return 0;
  const paid=transfer(indW(I),wl,n*pr);if(paid<n*pr){transfer(wl,indW(I),paid);return 0}inv.take(mk,k,n);inv.add(I.hold,k,n);if(ITEMS[k].maker&&typeof ceSale==='function')ceSale(ITEMS[k].maker,k,n,paid,wl,R.sid);return n}
// ---- deciding what to do next, docked
function indGo(I,k,to,extra){const p=indPath(I,I.sector,to);I.run=Object.assign({k,to,path:p,leg:0,next:S.T+IND.hop*.5*ptHopK(I),T0:S.T},extra||{});I.st='go';I.idleT=S.T;
  if(WORLDS[I.sector])inW(WORLDS[I.sector],()=>indSpawn(I,false))}
function indMarkets(I,from,maxH){const L=[];for(const id in S.stations){const D=S.stations[id];if(!D||!indMarketOK(I,D))continue;const h=indHops(from,id);if(h<=maxH)L.push({D,h})}return L}
// a hauler's trade: the best margin from here, per hop
function indTradePlan(I,R){if(!IND.trade||!indFree(R)||!indMarketOK(I,R))return null;const mk=mkStock(R),cap=indCargo(I)*(ptHas(I,'Overloader')?1:.8),budget=indPurse(I)-IND.reserve;if(budget<200)return null;let best=null;
  for(const{D,h}of indMarkets(I,R.sid,ptHas(I,'Speed Demon')?3:4)){if(D===R)continue;const wl=D.owner==='neutral'?'neutral':D.owner,tr=S.econ.treasury[wl]||0;
    const risk=indPath(I,R.sid,D.sid).reduce((a,s)=>a+indDanger(s),0);if(risk>.12&&!ptHas(I,'Greedy')&&!ptHas(I,'Speed Demon'))continue;
    for(const k of IND_GOODS){if(!(mk[k]>0)||ITEMS[k].maker)continue;const b=mkPartPrice(R,k,I.cls),s=mkPartSell(D,k,I.cls),m=s-b;if(m<=0)continue;const n=Math.min(mk[k],Math.floor(cap/mass(k)),Math.floor(budget/b),Math.floor(tr/s));if(n<=0)continue;
      const pr=m*n,sc=pr/(h+(ptHas(I,'Speed Demon')?.3:1))*(ptHas(I,'Greedy')?1:1-risk*3);if(pr>=IND.minProfit&&(!best||sc>best.sc))best={k,n,to:D.sid,sc,pr}}}
  return best}
// a freeport request (or a blockade or containment run) left 8 minutes: buy it here and carry it in
function indBoardHaul(I,R){if(!IND.trade||!indFree(R)||!indMarketOK(I,R))return null;const mk=mkStock(R);let best=null;
  for(const c of S.contracts||[]){if(!c.st||c.ind||!(c.n>0)||!ITEMS[c.item]||c.st===R.sid)continue;c.seen=c.seen||S.T;if(S.T-c.seen<IND.boardAge)continue;const D=S.stations[c.st];if(!D)continue;
    if(c.fac!=='neutral'&&(!FAC_IDS.includes(c.fac)||(I.stand[c.fac]||0)<=STAND.dock))continue;const h=indHops(R.sid,c.st);if(h>5||(c.until&&c.until<S.T+IND.hop*(h+1)))continue;
    const pr=mkPartPrice(R,c.item,I.cls),n=Math.min(c.n,mk[c.item]||0,Math.floor(indCargo(I)/mass(c.item)),Math.floor((indPurse(I)-100)/pr));if(n<Math.min(c.n,jobMin(c)))continue;
    const gain=Math.round(c.reward*n/c.n)-pr*n;if(gain<IND.minProfit*.5)continue;if(!best||gain/(h+1)>best.sc)best={c,n,sc:gain/(h+1)}}
  return best}
// a power's ore order left 8 minutes: a miner cuts that ore and carries it to the power's nearest station
function indBoardOre(I){let best=null;for(const c of S.contracts||[]){if(c.st||c.ind||!(c.n>0)||!RAWS.includes(c.item)||!FAC_IDS.includes(c.fac))continue;c.seen=c.seen||S.T;if(S.T-c.seen<IND.boardAge)continue;if((I.stand[c.fac]||0)<=STAND.dock)continue;
    const at=indMineSys(I,c.item);if(!at)continue;const h=indHops(I.sector,at);if(c.until&&c.until<S.T+IND.hop*(h*2+3)+600)continue;if(!best||c.reward>best.c.reward)best={c,at}}return best}
function indOreIn(sid,k){const s=S.sectors[sid];if(!s)return 0;let n=0;for(const a of s.ast){if(a.comet)continue;n+=k?(a.ore[k]||0):oreTotal(a)}return n}
// where a miner goes: home (Homebody), farther for richer rock (Prospector), dangerous space for rare ore (Rock Diver), else the
// nearest system with ore worth cutting
function indMineSys(I,want){const near=[];for(const id in S.sectors){const h=indHops(I.port,id);if(h>3||broodHeld(id))continue;const o=indOreIn(id,want);if(o<(want?10:60))continue;near.push({id,h,o,d:indDanger(id),rare:indOreIn(id,'au')+indOreIn(id,'xc')+indOreIn(id,'nu')})}
  if(!near.length)return null;if(want)return near.sort((a,b)=>a.h-b.h||b.o-a.o)[0].id;
  if(ptHas(I,'Homebody')){const x=near.find(n=>n.id===I.port)||near.sort((a,b)=>a.h-b.h)[0];return x.id}
  if(ptHas(I,'Rock Diver')){const x=near.filter(n=>n.d>0||n.rare>40).sort((a,b)=>b.rare-a.rare)[0];if(x)return x.id}
  if(ptHas(I,'Prospector')){const x=near.filter(n=>n.h>=1).sort((a,b)=>b.o-a.o)[0];if(x)return x.id}
  return near.sort((a,b)=>a.h-b.h||b.o-a.o)[0].id}
function indPlan(I){const R=S.stations[I.sector];if(I.st!=='dock')return;
  if(R){indSell(I,R);indUpgrade(I,R);indShop(I,R)}
  // haulers waiting for company (Convoy Lover, Convoy Only) set off when another independent leaves with them, or after a while
  if(I.role==='hauler'&&(ptHas(I,'Convoy Lover')||ptHas(I,'Convoy Only'))){const pal=indAll().some(o=>o!==I&&o.st==='go'&&o.run&&o.run.T0>S.T-120&&o.run.path[0]===I.sector);if(!pal&&S.T-I.idleT<(ptHas(I,'Convoy Only')?900:300))return}
  if(I.role==='hauler'&&R){const b=indBoardHaul(I,R);if(b){const n=indBuy(I,R,b.c.item,b.n);if(n>0){b.c.ind=I.id;I.res={[b.c.item]:n};indGo(I,'board',b.c.st,{c:b.c.id,item:b.c.item});return}}
    const t=indTradePlan(I,R);if(t){const n=indBuy(I,R,t.k,t.n);if(n>0){indGo(I,'trade',t.to,{item:t.k});return}}}
  if(I.role==='miner'){const o=indBoardOre(I);if(o){o.c.ind=I.id;indGo(I,'mine',o.at,{c:o.c.id,want:o.c.item});return}
    const at=indMineSys(I);if(at){indGo(I,'mine',at,{});return}}
  // a hauler that sold at a power's market goes to the nearest freeport to load; anyone else home after a while
  if(I.role==='hauler'&&!indFree(R)){let to=I.port,bh=indHops(I.sector,I.port);for(const sid of indPorts()){const h=indHops(I.sector,sid);if(h<bh){bh=h;to=sid}}indGo(I,'home',to,{});return}
  if(I.sector!==I.port&&S.T-I.idleT>240)indGo(I,'home',I.port,{})}
// ---- the clock: hops out of sight, mining out of sight
function indMineOff(I){const s=S.sectors[I.sector];if(!s)return;const r=I.run,cap=indCargo(I),fill=ptHas(I,'Light Load')?.5:ptHas(I,'Hoarder')?1:IND.fill;
  let n=Math.round((IND.mineT[I.cls]||3)*(IND.pass/60)*(1+.15*(((indGrades(I)||{}).drill||1)-1)));n=Math.min(n,Math.floor(cap-invMass(I.hold)));let got={};
  if(n>0){const skip=r.want?Object.fromEntries(RAWS.filter(k=>k!==r.want).map(k=>[k,1])):null;got=extract(s,n,false,skip);inv.addAll(I.hold,got)}
  if(invMass(I.hold)>=cap*fill-1e-9||!invMass(got)){indMineDone(I)}}
function indMineDone(I){const r=I.run;let to=I.port;if(r&&r.c){const c=(S.contracts||[]).find(x=>x.id===r.c);if(c&&(I.hold[c.item]||0)>0){let bh=99;for(const id in S.stations){const D=S.stations[id];if(D&&D.owner===c.fac&&D.kind!=='depot'){const h=indHops(I.sector,id);if(h<bh){bh=h;to=id}}}I.res={[c.item]:I.hold[c.item]};indGo(I,'board',to,{c:c.id,item:c.item,ore:1});return}}
  indGo(I,'home',to,{})}
function indTick(){if(!indOn()||!S.econ)return;indAll();const pass=S.T>=(S.ind.passT||0);if(pass){S.ind.passT=S.T+IND.pass;indArrivals()}
  for(const I of indAll().slice()){
    if(I.st==='down'){if(!(I.back>0))I.back=S.T;if(S.T>=I.back)indBack(I);continue}
    if(pass)indWear(I);
    if(I.st==='pj'){const r=pjRunOf(I.pj);if(!r){I.st='dock';I.pj=null;if(!S.stations[I.sector])indGo(I,'home',I.port,{})}else I.sector=r.sector;continue}
    if(I.st==='dock'){if(pass)indPlan(I);continue}
    const r=I.run;if(!r){I.st='dock';continue}if(I.live)continue;
    if(I.st==='work'){if(pass)indMineOff(I);continue}
    if(S.T<r.next)continue;if(r.leg>=r.path.length-1){indArrive(I);continue}
    r.leg++;I.sector=r.path[r.leg];r.next=S.T+IND.hop*ptHopK(I);
    if(WORLDS[I.sector]){inW(WORLDS[I.sector],()=>indSpawn(I,true));continue}
    const d=indDanger(I.sector)*ptRiskK(I);if(d>0&&Math.random()<d)indDownOff(I)}}
// fitted parts wear out as the fleets' and crews' do, falling as debris where the ship is
function indWear(I){const s=S.sectors[I.sector];for(const id of Object.keys(I.kit||{})){let n=I.kit[id];while(n-->0)if(Math.random()<CE.wear*IND.pass/3600){inv.take(I.kit,id,1);if(s)toDebris(s,{[id]:1});else inv.addAll(indStore(I),{[id]:1})}}}
// at the end of a route
function indArrive(I){const r=I.run;if(!r){I.st='dock';return}
  if(r.k==='mine'){I.st='work';r.cut=0;return}
  const R=S.stations[I.sector];I.st='dock';I.idleT=S.T;I.run=null;
  if(r.k==='board'){const c=(S.contracts||[]).find(x=>x.id===r.c);I.res=null;if(c&&R&&(c.st?c.st===R.sid:R.owner===c.fac)){const d=Math.min(c.n,I.hold[c.item]||0);if(d>0){const share=Math.round(c.reward*d/c.n);c.reward-=share;c.n-=d;inv.take(I.hold,c.item,d);inv.add((S.stations[c.st]&&storeOf(S.stations[c.st]))||S.econ.stock[c.fac]||storeOf(R),c.item,d);
      if(c.blk&&c.st){const R2=S.stations[c.st];if(R2&&R2.hMax)R2.hull=Math.min(R2.hMax,(R2.hull||0)+R2.hMax*.1*d/(c.n0||d))}
      const got=transfer(c.fac,indW(I),share);I.earned+=got;I.jobs++;indWork(I,c.fac,STAND.contract+share/1500);if(c.n<=0)S.contracts.splice(S.contracts.indexOf(c),1)}}
    if(c)c.ind=null}
  if(!R){indGo(I,'home',I.port,{});return}
  indSell(I,R);if(r.k==='trade')I.jobs++}
// Rating and standing from work done for a power
function indWork(I,f,n){if(!(n>0))return;const r0=ratingOf(I);I.rp=(I.rp||0)+n*RATING.k;if(FAC_IDS.includes(f))I.stand[f]=clamp((I.stand[f]||0)+n*.5,-100,100);const r1=ratingOf(I);
  if(r1>r0&&r1===6)allFeed(`★ ${I.name}, an independent out of ${DEF[I.port].name}, has reached Contractor Rating 6.`,'info')}
// ---- shot down, and coming back
function indDown(I,cause,sid){const s=S.sectors[sid]||S.sectors[I.sector],sys=indSysInv(I);if(s){toDebris(s,I.kit);toDebris(s,I.hold);toDebris(s,sys)}else{inv.addAll(indStore(I),I.kit);inv.addAll(indStore(I),I.hold);inv.addAll(indStore(I),sys)}I.tiers=null;
  I.kit={};I.hold={};I.res=null;if(I.run&&I.run.c){const c=(S.contracts||[]).find(x=>x.id===I.run.c);if(c)c.ind=null}
  I.lost=I.cls;I.st='down';I.live=false;I.run=null;I.pj=null;I.deaths++;I.back=S.T+IND.back;I.cause=cause||'unknown';I.sector=sid||I.sector;
  if(cause==='pirate'||cause==='raided'||cause==='ambush')allFeed(`${I.name}, an independent out of ${DEF[I.port].name}, was lost to raiders in ${DEF[I.sector].name}.`,'info')}
function indDownOff(I){const r=I.run||{},by=broodHeld(I.sector)?'brood':'pirate';let cause='unknown';
  if(I.role==='hauler')cause=broodHeld(I.sector)||DEF[I.sector].kind==='den'?'hostile':indAll().some(o=>o!==I&&o.sector===I.sector&&o.st==='go')?'ambush':'alone';
  else if(I.role==='miner')cause=invMass(I.hold)>=indCargo(I)*.85?'full':indHops(I.sector,I.port)>=2?'far':'raided';
  else cause='outnumbered';I.killer=by;indDown(I,cause,I.sector)}
function indBack(I){const port=I.port,R=S.stations[port];if(!R){indRetire(I);return}
  const lost=I.lost||I.cls,pr=START_HULLS.includes(lost)?0:hullPrice(lost);let cls=null;
  if(indPurse(I)>=pr+IND.reserve&&(!pr||transfer(indW(I),'neutral',pr)>=pr))cls=lost;else if(indPurse(I)>=IND.minPurse)cls=IND.line[I.role][0];
  if(!cls){indRetire(I);return}
  const old=I.pt;I.pt=ptDeath(I.role,I.cause,I);I.cls=cls;I.paid=pr||null;I.st='dock';I.sector=port;I.run=null;I.idleT=S.T;
  if(old!==I.pt)allFeed(`${I.name} is flying again out of ${DEF[port].name}, ${ptName(I.pt)} now${I.cause&&I.cause!=='unknown'?'':' after a bad loss'}.`,'info');
  try{indShop(I,R)}catch(e){console.error(e)}}
function indRetire(I){transfer(indW(I),'neutral',indPurse(I));delete S.econ.treasury[indW(I)];inv.addAll(indStore(I),I.hold);inv.addAll(indStore(I),I.kit);inv.addAll(indStore(I),indSysInv(I));I.tiers=null;I.hold={};I.kit={};
  const L=indAll(),i=L.indexOf(I);if(i>=0)L.splice(i,1);allFeed(`${I.name} has hung up their flight suit: an independent retires from ${DEF[I.port].name}.`,'info')}
// ---- posted jobs: an independent signs on when one is free and its hull fits
function indTake(j){const R=S.stations[j.sid];if(!R)return null;const role=indRoleOfJob(j.kind);let best=null,bh=99;
  for(const I of indAll()){if(I.st!=='dock'||I.role!==role)continue;const h=indHops(I.sector,R.sid);if(h<bh){bh=h;best=I}}return bh<=8?best:null}
{const o=pjTick;pjTick=function(){try{if(indOn()&&!S.unb)for(const j of pjList()){if(j.state!=='open'||S.T<j.claimAt)continue;const R=S.stations[j.sid],P=xPilotOfKey(j.pid);if(!R||R.owner!=='player'||!P)continue;
      const I=indTake(j);if(!I)continue;I.st='pj';I.pj=null;j.by='neutral';j.who=`${I.name}, an independent`;j.indPick=I.id;j.state='taken';j.due=1e12;keyFeed(j.pid,`📋 ${j.who} took your job: ${pjTitle(j)}.`,'info')}}catch(e){console.error(e)}
  return o.apply(this,arguments)}}
{const o=pjRunStart;pjRunStart=function(j){const I=j&&j.indPick!=null?indById(j.indPick):null;if(!I)return o.apply(this,arguments);
  const n0=pjRuns().length;IND_HOLD=I;let x;try{x=o.apply(this,arguments)}finally{IND_HOLD=null}const r=pjRuns().length>n0?pjRuns()[pjRuns().length-1]:null;
  if(!r||r.job!==j.id){I.st='dock';I.pj=null;return x}
  r.ind=I.id;r.cls=I.cls;const pre=indPath(I,I.sector,r.path[0]);if(pre.length>1){r.path=pre.concat(r.path.slice(1));r.leg=0;r.sector=I.sector;r.next=S.T+PJR.hop*.5}
  I.pj=r.id;I.sector=r.sector;if(WORLDS[r.sector])inW(WORLDS[r.sector],()=>pjSpawn(r,false));return x}}
{const o=pjSpawn;pjSpawn=function(r){if(IND_HOLD&&r&&!r.ind)return null;const e=o.apply(this,arguments);try{const I=e&&r&&r.ind!=null?indById(r.ind):null;if(I){e.indId=I.id;e.pt=I.pt;indFly(e,I);e.pname=indLabel(I)}}catch(err){console.error(err)}return e}}
{const o=pjRunEnd;pjRunEnd=function(r,ok,why){const I=r&&r.ind!=null?indById(r.ind):null;if(!I)return o.apply(this,arguments);const j=pjJob(r),by=j&&j.by;
  if(j&&ok)j.by=indW(I);let x;try{x=o.apply(this,arguments)}finally{if(j)j.by=by}
  if(I.st==='down')return x;if(ok&&j){I.jobs++;I.earned+=j.paid||0;indWork(I,null,STAND.contract+(j.paid||0)/1500)}
  I.st='dock';I.pj=null;I.sector=r.sector||I.sector;I.idleT=S.T;
  // its ship, if it's in a live system, flies on as the independent's own
  let e=null;for(const sid in WORLDS)for(const x2 of WORLDS[sid].ents)if(x2.indId===I.id&&x2.alive)e={x:x2,sid};
  const R=S.stations[I.sector];if(R&&indMarketOK(I,R)&&!e)return x;
  const p=indPath(I,I.sector,I.port);I.run={k:'home',to:I.port,path:p,leg:0,next:S.T+IND.hop*.5,T0:S.T};I.st='go';
  if(e){const E=e.x;E.pjRun=null;E.home='ind:'+I.id;I.live=true;E.pname=indLabel(I)}return x}}
// ---- live: the independent's own ship
function indSpawn(I,arrive){if(!W||I.live||I.st==='down'||I.st==='dock'||I.st==='pj')return null;const r=I.run;if(!r)return null;
  const role=I.st==='work'?'miner':I.role==='fighter'?'patrol':'hauler',e=makeNPC(role,'neutral',I.cls,1,{},'ind:'+I.id);e.cargo=I.hold;I.hold={};e.indId=I.id;e.pt=I.pt;I.live=true;indFly(e,I);e.pname=indLabel(I);
  const gs=GATES[W.sid]||[],prev=r.path[r.leg-1],gin=gs.find(g=>g.to===prev),SE=W.stationEnt;
  if(arrive&&gin){e.x=gin.x*.93;e.y=gin.y*.93;e.z=gin.z*.93;fxWarp(e,sideCol('neutral'))}
  else if(I.st==='work'){const s=S.sectors[W.sid],a=s&&s.ast.find(x=>!x.comet&&oreTotal(x)>0);const o=rdir(1);if(a){e.x=a.x+o.x*300;e.y=a.y+o.y*200;e.z=a.z+o.z*300}else if(SE){e.x=SE.x+o.x*400;e.y=SE.y;e.z=SE.z+o.z*400}}
  else if(SE&&r.leg===0){const o=rdir(1);e.x=SE.x+o.x*300;e.y=SE.y+o.y*150;e.z=SE.z+o.z*300}else{const at=gin||pick(gs);if(at){e.x=at.x*.9;e.y=at.y*.9;e.z=at.z*.9}}
  faceInstant(e,-e.x||1,-e.y,-e.z);W.ents.push(e);return e}
function indRock(e,s,I){const L=s.ast.filter(x=>!x.comet&&oreTotal(x)>0);if(!L.length)return null;const want=I.run&&I.run.want,SE=W.stationEnt;
  if(want){const w=L.filter(a=>(a.ore[want]||0)>0);if(w.length)return w.sort((a,b)=>d3(a,e)-d3(b,e))[0]}
  if(typeof ptRock==='function'){const a=ptRock(e,L,SE);if(a)return a}return L.sort((a,b)=>d3(a,e)-d3(b,e))[0]}
{const o=npcThink;npcThink=function(e,dt){if(!e.indId||e.pjRun||NET.cl)return o.apply(this,arguments);const I=indById(e.indId);
  if(!I||I.st==='down'||!I.run){e.indId=null;e.role='leave';return o.apply(this,arguments)}
  const r=I.run,SE=W.stationEnt,ai=e.ai;ai.t-=dt;e.life+=dt;e.mining=null;e.thrusting=false;if(jamDark(e)){e.boosting=false;return}e.pname=indLabel(I);
  const flee=typeof ptFlee==='function'&&ptFlee(e);
  if(I.st==='work'){const s=S.sectors[W.sid],cap=e.st.cargo,fill=ptHas(I,'Light Load')?.5:ptHas(I,'Hoarder')?1:IND.fill,hurt=W.t-e.lastHit<4&&e.hull<e.st.hull*(ptHas(I,'Hoarder')?.4:.75);
    if(flee||hurt||invMass(e.cargo)>=cap*fill-1e-9){inv.addAll(I.hold,e.cargo);e.cargo={};indMineDone(I);inv.addAll(e.cargo,I.hold);I.hold={};I.live=true;return}
    let a=ai.ast;if(!a||!s.ast.includes(a)||oreTotal(a)<=0){a=indRock(e,s,I);ai.ast=a}if(!a){inv.addAll(I.hold,e.cargo);e.cargo={};indMineDone(I);inv.addAll(e.cargo,I.hold);I.hold={};I.live=true;return}
    const d=d3(a,e),rr=astR(a);if(d>rr+150){steer(e,a.x,a.y,a.z,dt,true);faceTo(e,a,dt);return}brake(e,dt);
    if(faceTo(e,a,dt)<.3){e.mining=a;e.mineAcc+=(IND.mineT[I.cls]||3)/60*dt*(1+.15*(((indGrades(I)||{}).drill||1)-1));const want=r.want;
      while(e.mineAcc>=1){e.mineAcc-=1;const k=want&&(a.ore[want]||0)>0?want:mainOre(a);if(!k)break;a.ore[k]--;if(!a.ore[k])delete a.ore[k];inv.add(e.cargo,k,1);if(oreTotal(a)<=0){removeAst(s,a);ai.ast=null;break}}}return}
  e.boosting=flee||W.t-e.lastHit<5||ptHas(I,'Speed Demon');
  if(r.leg<r.path.length-1){const g=W.ents.find(x=>x.type==='gate'&&x.to===r.path[r.leg+1]);if(g){npcGateJump(e,g,dt,e.boosting?1.15:.8);return}}
  if(r.k==='mine'&&r.to===W.sid){I.st='work';r.cut=0;e.role='miner';return}
  if(SE){const d=steer(e,SE.x,SE.y,SE.z,dt,true,e.boosting?1.15:.8);faceTo(e,SE,dt);if(d<(SE.r||150)+60){r.arrived=true;despawn(e)}return}
  e.role='leave';return o.apply(this,arguments)}}
{const o=returnHome;returnHome=function(e){if(e&&e.indId&&!e.pjRun){const I=indById(e.indId);if(I){inv.addAll(I.hold,e.cargo);inv.addAll(I.hold,e.load);e.cargo={};e.load={};I.live=false;const r=I.run;
    if(r&&r.arrived){r.arrived=false;r.leg=r.path.length-1;indArrive(I)}
    else if(r&&I.st==='go'&&r.leg<r.path.length-1&&e.gj){r.leg++;I.sector=r.path[r.leg];r.next=S.T+IND.hop*ptHopK(I);if(WORLDS[I.sector])inW(WORLDS[I.sector],()=>indSpawn(I,true))}}}
  return o.apply(this,arguments)}}
{const o=killShip;killShip=function(e,src,at){if(e&&e.indId&&!NET.cl){const I=indById(e.indId),sid=W&&W.sid;if(I&&I.st!=='down'){let cause='unknown';try{cause=ptCause(e,src,at,I.role)}catch(err){}
    I.killer=typeof ptKillerTag==='function'?ptKillerTag(at&&at.src&&at.src.type==='ship'?at.src:null):null;if(I.role==='miner'&&(src==='pirate'||src==='brood'||FAC_IDS.includes(src))&&cause!=='named')cause=invMass(e.cargo)>=e.st.cargo*.85?'full':indHops(sid,I.port)>=2?'far':'raided';
    if(I.role==='hauler'&&cause!=='named')cause=broodHeld(sid)||DEF[sid].kind==='den'?'hostile':W.ents.some(x=>x!==e&&x.alive&&x.indId&&x.type==='ship')?'ambush':'alone';
    I.st='down';try{return o.apply(this,arguments)}finally{I.st='go';indDown(I,cause,sid)}}}return o.apply(this,arguments)}}
{const o=openWorld;openWorld=function(sid){const w=o.apply(this,arguments);try{if(indOn())inW(w,()=>{for(const I of indAll())if(I.sector===sid&&(I.st==='go'||I.st==='work')&&I.run){I.live=false;indSpawn(I,false)}})}catch(e){console.error(e)}return w}}
// shooting an independent costs no standing (it's nobody's ship)
{const o=dmgRec;dmgRec=function(e){if(e&&e.indId){const s=e.side;e.side='_ind';try{return o.apply(this,arguments)}finally{e.side=s}}return o.apply(this,arguments)}}
{const o=holderIn;holderIn=function(st,path){if(typeof path==='string'&&path.startsWith('ind:')){const I=((st.ind&&st.ind.list)||[]).find(x=>String(x.id)===path.split(':')[1]);return I?(I.hold=I.hold||{}):(st.econ.stock.pirate)}return o.apply(this,arguments)}}
{const o=ledger;ledger=function(){const r=o.apply(this,arguments);try{const L=r.L['Fleets in muster'];for(const I of(S.ind&&S.ind.list)||[]){for(const x of[I.hold||{},I.kit||{},indSysInv(I)]){const v=invVec(x);for(const k of RAWS){L[k]+=v[k];r.tot[k]+=v[k]}}}}catch(e){}return r}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{indTick()}catch(e){console.error(e)}return r}}
// ---- where you see them: a freeport's panel on the galaxy map lists its independents
{const o=mpHtml;mpHtml=function(sid){let h=o.apply(this,arguments);try{if(S&&S.ind&&FREEPORTS.some(f=>f.sid===sid)){const L=indAll().filter(I=>I.port===sid);if(L.length)h+=`<div class="h3" style="margin-top:12px">Independents</div><div class="note" style="margin-bottom:4px">Contractors out of this freeport: they take jobs nobody else does, trade and mine.</div>`+L.map(I=>`<div class="kv"><span>${esc(I.name)} · ${esc(CLASSES[I.cls].name)}</span><b>${esc(ptName(I.pt)||'')} · ${esc(indDoing(I))}${I.sector!==sid&&I.st!=='down'?' in '+esc(DEF[I.sector].name):''}</b></div>`).join('')}}catch(e){console.error(e)}return h}}
// a saved galaxy: nothing is live on load
{const o=migrate;migrate=function(st){const r=o.apply(this,arguments);try{for(const I of(S&&S.ind&&S.ind.list)||[])I.live=false}catch(e){}return r}}
