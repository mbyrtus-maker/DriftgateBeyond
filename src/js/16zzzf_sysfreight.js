//@src 16zzzf_sysfreight.js
// ============================================================ Beyond: makers ship their systems (user, 8 Nov 2026)
// The user found no drives, reactors, shield emitters, armour, cargo holds or payload bays on the markets. A new galaxy seeds
// about 50 systems over 9 stations; after that only each maker's home works built them, and those stalled within the hour
// once their market ran out of wire. Payload bays never appeared at all (a grade 1 bay is built into every hull and has no
// recipe). Agreed: "Makers ship them".
//   - Out: every 1.5 to 2.5 minutes a maker with no freighter of its systems under way sends one from its home to the market
//     that lacks most of its systems (the freeports and core stations first, where pilots dock most; nearest first on a tie): up to 4 systems, at the line's current grade, toward one of
//     each line on every shelf it serves. A power's maker serves its own power's stations and the three freeports; a
//     freeport's maker the three freeports and each power's core station. The maker pays the carrier 40 cr + 10 a jump.
//     The freighter flies under the home's colours (a power's, or the Compact's for a freeport maker): a real convoy, raided
//     and escorted like any other. Whatever it lands goes on the destination's market; a sale there pays the maker as at home.
//   - In: when the home market lacks what the next systems take (wire, plate, coil, or what a Calibration Matrix, lattice or
//     core is made of), the maker buys it at the nearest market that has spare (keeping 8 there; never at a power's station
//     at war with the home's owner), pays that market's price to its owner, and ships it home, up to 12 units a run.
//   - A maker ships, and buys for its systems, only while it holds 1,500 cr above its reserve: stocking far shelves is
//     what a maker does with spare money.
//   - The home works build systems for the shelves they serve as well as their own (up to 4 of a line on the home shelf).
//   - A maker's payload bay line starts at grade 2 (a bay you can buy is at least grade 2).
// Host only; the ledger stays exact (goods only move between stores and freighters; credits between wallets).
const SYF={every:[90,150],load:4,tgt:1,fee:40,hop:10,res:8,inMax:12,cushion:1500};
function syfLines(m){return(MK_LINE[m]||[]).filter(id=>ITEMS[id]&&ITEMS[id].sys)}
function syfGid(m,id){const g=rdGid(id,rdLineG(m,id));return ITEMS[g]&&Object.keys(ITEMS[g].recipe).length?g:null}
function syfHave(st,id){let n=0;for(let g=1;g<=5;g++)n+=st[rdGid(id,g)]||0;return n}
function syfSide(R){return R.owner==='neutral'?'neutral':R.owner}
function syfOk(R){return!!R&&R.sid!==WRACK.sid&&(R.owner==='neutral'&&isFreeF(R)||FAC_IDS.includes(R.owner))}
// the markets a maker's systems are shipped to
function syfDests(m){const R0=mkAtHome(m);if(!R0)return[];const h=MAKERS[m].home,fac=FAC_IDS.includes(h);
  return Object.values(S.stations).filter(R=>syfOk(R)&&R!==R0&&HOP[R0.sid]&&HOP[R0.sid][R.sid]!=null&&(R.owner==='neutral'||(fac?R.owner===h:R.kind==='core')))}
// how many more of a line the shelves a maker serves still lack (cached per tick)
let SYF_W={t:-1,S:null,w:{}};
function syfWant(m,id){if(!S||!ITEMS[id]||!ITEMS[id].sys)return 0;if(SYF_W.t!==S.T||SYF_W.S!==S)SYF_W={t:S.T,S,w:{}};const k=m+'|'+id;
  if(SYF_W.w[k]===undefined){let n=0;try{for(const R of syfDests(m))n+=Math.max(0,SYF.tgt-syfHave(mkStock(R),id))}catch(e){}SYF_W.w[k]=Math.min(SYF.load,n)}return SYF_W.w[k]}
function syfBusy(m,k){return(S.traders||[]).some(t=>t.syf&&t.syf.m===m&&t.syf.k===k)}
function syfOut(m){const R0=mkAtHome(m);if(!R0)return false;const st=mkStock(R0);let best=null;
  for(const R of syfDests(m)){const ds=mkStock(R),want={};let n=0;
    for(const id of syfLines(m)){const gid=syfGid(m,id);if(!gid)continue;const q=Math.min(SYF.tgt-syfHave(ds,id),st[gid]||0);if(q>0){want[gid]=q;n+=q}}
    if(!n)continue;const h=HOP[R0.sid][R.sid],sc=n*100-h+(R.kind==='core'||isFreeF(R)?500:0);if(!best||sc>best.sc)best={R,want,sc,h}}
  if(!best)return false;const fee=SYF.fee+SYF.hop*best.h;if(ceT(m)-fee<ceReserve(m)+SYF.cushion)return false;
  const load={};let k=0;for(const gid in best.want){const q=Math.min(best.want[gid],SYF.load-k);if(q<=0)break;load[gid]=inv.take(st,gid,q);k+=load[gid]}
  for(const g in load)if(!load[g])delete load[g];if(!k)return false;
  const t=haulSend(syfSide(R0),R0.sid,best.R.sid,load,'syf:'+m,`${MAKERS[m].short} systems`,null);if(!t){inv.addAll(st,load);return false}
  t.syf={m,k:'out'};const paid=transfer(ceW(m),syfSide(R0),fee);ceOf(m).cost+=paid;return true}
// what the next systems need that the home market hasn't got (a matrix, lattice or core counts as what it's made of)
function syfNeed(m){const R0=mkAtHome(m),st=mkStock(R0),need={};
  const add=(rc,x,d)=>{for(const k in rc){const q=rc[k]*x;if(RD_CRAFT.has(k)&&d<3&&ITEMS[k].recipe&&!(ITEMS[k].forge&&!rdForgeAt(R0))){const sh=q-(st[k]||0);if(sh>0)add(ITEMS[k].recipe,sh,d+1)}else need[k]=(need[k]||0)+q}};
  for(const id of syfLines(m)){const gid=syfGid(m,id);if(!gid)continue;const w=Math.min(CE.cap,CE.shelf+ceSold(m,id,3600)+syfWant(m,id))-(st[gid]||0);if(w<=0)continue;add(ITEMS[gid].recipe,Math.min(2,w),0)}
  for(const k in need){need[k]=Math.ceil(need[k]-(st[k]||0));if(need[k]<=0)delete need[k]}return need}
function syfIn(m){const R0=mkAtHome(m);if(!R0)return false;const need=syfNeed(m);if(!Object.keys(need).length)return false;let best=null;
  for(const R of Object.values(S.stations)){if(!syfOk(R)||R===R0||!HOP[R0.sid]||HOP[R0.sid][R.sid]==null)continue;if(R.owner!=='neutral'&&R0.owner!=='neutral'&&R.owner!==R0.owner&&hostile(R0.owner,R.owner))continue;
    const ss=mkStock(R);if(ss===mkStock(R0))continue;const buy={};let n=0;for(const k in need){const q=Math.min(need[k],Math.floor((ss[k]||0)-SYF.res),SYF.inMax-n);if(q>0){buy[k]=q;n+=q}}
    if(!n)continue;const h=HOP[R0.sid][R.sid],sc=n*10-h;if(!best||sc>best.sc)best={R,buy,sc,h}}
  if(!best)return false;const R=best.R,ss=mkStock(R),wl=syfSide(R);let cost=SYF.fee+SYF.hop*best.h;for(const k in best.buy)cost+=stPrice(R,k)*best.buy[k];cost=Math.ceil(cost);
  if(ceT(m)-cost<ceReserve(m)+SYF.cushion)return false;const load={};for(const k in best.buy){const q=inv.take(ss,k,best.buy[k]);if(q>0)load[k]=q}if(!Object.keys(load).length)return false;
  const t=haulSend(syfSide(R0),R.sid,R0.sid,load,'syf:'+m,`${MAKERS[m].short} supplies`,null);if(!t){inv.addAll(ss,load);return false}
  t.syf={m,k:'in'};let paid=0;for(const k in load)paid+=transfer(ceW(m),wl,Math.ceil(stPrice(R,k)*load[k]));paid+=transfer(ceW(m),syfSide(R0),SYF.fee+SYF.hop*best.h);ceOf(m).cost+=paid;return true}
function syfTick(){if(NET.cl||!S||S.training||S.unb||!rdOn())return;S.syf=S.syf||{};
  for(const m in MAKERS){if(!ceAlive(m)||!mkAtHome(m))continue;const A=S.syf[m]=S.syf[m]||{t:S.T+rnd(20,120)};if(S.T<A.t)continue;A.t=S.T+rnd(...SYF.every);
    try{if(!syfBusy(m,'out'))syfOut(m);if(!syfBusy(m,'in'))syfIn(m)}catch(e){console.error(e)}}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{syfTick()}catch(e){console.error(e)}return r}}
// a maker's freighter lands on the destination's market (its home's, if the destination has fallen to the Brood or a pilot)
{const o=haulArrive;haulArrive=function(t){if(!t||!t.syf)return o.apply(this,arguments);cvEnd(t,true);const R=S.stations[t.to];let into=syfOk(R)?mkStock(R):null;
  if(!into){const H=mkAtHome(t.syf.m);into=H?mkStock(H):(S.econ.stock[t.side]||S.econ.stock.pirate)}inv.addAll(into,t.load);t.load={}}}
