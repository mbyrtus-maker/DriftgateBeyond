//@src 16zzzb_aipilots.js
// ============================================================ Beyond: AI pilots buy makers' parts like a player (7 Nov 2026)
// The user (7 Nov 2026): "AI soaks should work just like player purchases". An AI pilot with a hull of its own and pay of its
// own buys, fits and replaces makers' parts on the markets the way a pilot does: at the Market's price (mkPartPrice: the
// station's price for the part, stPrice, and the pilot's market fee for its hull), off the station's shelf, the maker credited
// through ceSale, the local price moved as a player's buy moves it.
//   Who: your depot's crews (16o_depots.js) are the AI pilots with a hull and a wage. Half a crew's wage (AIP.keep) is
//        its own pay, kept in its own purse (wallet pil_c<id>, up to AIP.max); the rest goes to the Compact as before.
//        (The AI contractors who take posted jobs are one-off pilots with no wallet or ship of their own, so they don't shop.)
//   When: a hauling crew docked at a market to sell your goods shops there before flying home.
//   What: one part for each slot its work uses (hauler: a cargo module; miner: a mining laser; guard: a laser or a gun),
//        grades up to its owner's Contractor Rating. A slot that is empty (worn out or never fitted) gets the best value the
//        purse affords above a reserve (AIP.reserve), by the refits' measure: traits, grade (+35% a grade) and price; a
//        fitted slot is upgraded when a higher grade is affordable once the old part is sold back to that market (at the
//        Market's sell price). One pass a visit.
//   Wear: fitted parts wear out like the powers' fleets' (CE.wear, half an hour's share each hour), falling as debris in the
//        crew's home system. A crew that leaves or is lost: its purse goes to the Compact, its parts fall as debris there.
//   Use: a crew's ship flies with its parts' grades (cargo, weapons, drill).
const AIP={keep:.5,max:1500,reserve:100,every:60,slots:{haul:[['cargo']],mine:[['mlaser']],guard:[['laser','gun']]}};
function aipW(k){return'pil_'+k}
function aipPurse(k){return S.econ.treasury[aipW(k)]||0}
function aipRec(k,sid){S.aip=S.aip||{};const A=S.aip[k]||(S.aip[k]={kit:{},sid:sid||null,acc:0});if(sid)A.sid=sid;return A}
function aipFitted(A,kinds){for(const id in A.kit)if(A.kit[id]>0&&ITEMS[id]&&kinds.includes(ITEMS[id].part))return id;return null}
function aipScore(R,id,cls){const I=ITEMS[id],pr=mkPartPrice(R,id,cls);return(1+2*ceGood(I.tr||{}))*(1+.35*((I.grade||1)-1))/Math.pow(pr/Math.max(1,baseValue(id)),.5)}
function aipBest(R,kinds,gcap,budget,cls,overG){const ms=mkStock(R);let best=null,bs=-1;
  for(const id in ms){const I=ITEMS[id];if(!I||!I.maker||!(ms[id]>0)||!kinds.includes(I.part)||(I.grade||1)>gcap||(I.grade||1)<=overG)continue;if(mkPartPrice(R,id,cls)>budget)continue;const sc=aipScore(R,id,cls);if(sc>bs){bs=sc;best=id}}return best}
// one maker's part off R's shelf, paid from wallet `from` and put in `into`, moved exactly as a player's buy moves it
function mkBuyOne(R,id,from,cls,into){const ms=mkStock(R),I=ITEMS[id];if(!I||!I.maker||!(ms[id]>0))return 0;const pr=mkPartPrice(R,id,cls),wl=R.owner==='neutral'?'neutral':R.owner;
  if(wallet(from).get()<pr)return 0;const paid=transfer(from,wl,pr);if(paid<pr){transfer(wl,from,paid);return 0}
  inv.take(ms,id,1);inv.add(into,id,1);mkOf(R)[id]=(R.mk[id]||0)-(HAUL_MK[cls]||1);ceSale(I.maker,id,1,paid,wl,R.sid);return paid}
// and one sold back onto R's shelf, as a player's sale: the station's owner pays the Market's sell price
function mkSellOne(R,id,to,cls,from){const wl=R.owner==='neutral'?'neutral':R.owner,pr=mkPartSell(R,id,cls);if(!(from[id]>0)||(S.econ.treasury[wl]||0)<pr)return 0;
  inv.take(from,id,1);inv.add(mkStock(R),id,1);mkOf(R)[id]=(R.mk[id]||0)+(HAUL_MK[cls]||1);return transfer(wl,to,pr)}
// an AI pilot docked at market R shops: an empty slot filled, a fitted one upgraded when it can afford it
function aipShop(k,R,cls,job,gcap,home){if(!R||!S.corp||S.training||S.unb||!(R.owner==='neutral'||FAC_IDS.includes(R.owner)))return 0;const A=aipRec(k,home),w=aipW(k);let n=0;
  for(const kinds of AIP.slots[job]||[]){const budget=aipPurse(k)-AIP.reserve;if(budget<=0)break;const have=aipFitted(A,kinds);
    if(!have){const id=aipBest(R,kinds,gcap,budget,cls,0);if(id&&mkBuyOne(R,id,w,cls,A.kit))n++;continue}
    const g=ITEMS[have].grade||1,id=aipBest(R,kinds,gcap,budget+mkPartSell(R,have,cls),cls,g);if(!id)continue;
    if(mkSellOne(R,have,w,cls,A.kit)&&mkBuyOne(R,id,w,cls,A.kit))n++}
  return n}
// ---- the crews: their pay, their wear, and settling up when one is gone
function aipCrews(){const m=new Map();for(const sid in S.stations||{}){const R=S.stations[sid];if(!R||R.owner!=='player'||R.kind!=='depot')continue;for(const c of R.crew||[])m.set('c'+c.id,[R,c])}return m}
function aipTick(){if(NET.cl||!S||S.training||S.unb)return;S.aipT=S.aipT||0;if(S.T<S.aipT)return;S.aipT=S.T+AIP.every;const crews=aipCrews();
  for(const[k,[R]]of crews){const A=aipRec(k,R.sid);A.acc=(A.acc||0)+DEP.wage*AIP.keep*AIP.every/3600;const n=Math.min(Math.floor(A.acc),Math.max(0,AIP.max-aipPurse(k)));if(n>=1){A.acc-=transfer('neutral',aipW(k),n)}if(A.acc>5)A.acc=5}
  for(const k in S.aip||{}){const A=S.aip[k],s=A.sid&&S.sectors[A.sid],drop=o=>{if(s)toDebris(s,o);else inv.addAll(S.econ.stock.neutral,o)};
    if(!crews.has(k)){drop(A.kit);A.kit={};transfer(aipW(k),'neutral',aipPurse(k));delete S.econ.treasury[aipW(k)];delete S.aip[k];continue}
    for(const id of Object.keys(A.kit)){let n=A.kit[id];while(n-->0)if(Math.random()<CE.wear*AIP.every/3600){inv.take(A.kit,id,1);drop({[id]:1})}}}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{aipTick()}catch(e){console.error(e)}return r}}
{const o=ledger;ledger=function(){const r=o.apply(this,arguments);try{const L=r.L['Fleets in muster'];for(const k in S.aip||{}){const v=invVec(S.aip[k].kit||{});for(const e of RAWS){L[e]+=v[e];r.tot[e]+=v[e]}}}catch(e){}return r}}
// a hauling crew shops at the market where it sold your goods
{const o=crSell;crSell=function(r){const x=o.apply(this,arguments);try{const D=S.stations[r.mk],c=crCrew(r),O=lairOwner({pid:r.pid||'me'})||S.player;if(D&&c)aipShop('c'+c.id,D,c.cls,'haul',typeof gradeCap==='function'?gradeCap(O):1,r.depot)}catch(e){console.error(e)}return x}}
// a crew's ship flies with its parts' grades
function aipGrades(k){const A=S.aip&&S.aip[k],T={engine:1,power:1,shield:1,weapon:1,armor:1,drill:1,cargo:1,payload:1};if(!A)return null;let any=false;
  for(const id in A.kit){const I=ITEMS[id];if(!I||!(A.kit[id]>0))continue;const g=I.grade||1,sl=I.part==='cargo'?'cargo':I.part==='mlaser'?'drill':I.part==='gun'||I.part==='laser'?'weapon':null;if(sl&&g>T[sl]){T[sl]=g;any=true}}return any?T:null}
function aipFly(e,k){const T=e&&aipGrades(k);if(!T)return e;e.st=shipStats(e.fac,e.cls,T);e.hull=e.st.hull;e.shield=e.st.sCap;e.energy=e.st.eCap;return e}
{const o=crewSpawn;crewSpawn=function(R,id,c){const e=o.apply(this,arguments);try{if(e&&c)aipFly(e,'c'+c.id)}catch(err){console.error(err)}return e}}
{const o=crSpawn;crSpawn=function(r){const e=o.apply(this,arguments);try{if(e&&r)aipFly(e,'c'+r.crew)}catch(err){console.error(err)}return e}}
