//@src 16zzv_bounty.js
// ============================================================ Beyond: a richer galaxy, replenished (6 Nov 2026)
// The user's call: with everything in the galaxy real, galaxies were running dry (a third of the fields' ore gone in 4 hours)
// and stalling: sides that lost ground couldn't afford to build it back. So a galaxy starts richer and keeps getting fresh rock:
//   - every asteroid field starts with half as much ore again, and every side's stores (the powers', the Brood's, the
//     Unbound's, the muster pools and the freeports') start half as full again;
//   - every hour fresh rock drifts in from the outer drift: new asteroids, a share of the galaxy's starting ore, placed in the
//     systems whose fields are most worked out, of the ores those systems carry. It is new matter, counted into the ledger's
//     starting totals as it arrives (as charting new space was), so the ledger stays exact.
const RICH={field:1.5,store:1.5,every:3600,rep:.08,rock:[40,90],cap:70};
// the Brood starts stronger (user, 6 Nov 2026): its stores and muster start this many times fuller again, on top of the richer start
const BRST={store:1};
// the Brood fields the biggest swarms (user, 6 Nov 2026): its offensives up to 16 ships (the powers' 8; it was 10), with 5 more than
// a power would send to the same target (was 2), and its raiding and prowling parties 6 strong (the others' 3)
const BRSW={max:16,raid:6};BAL.brN=5;
function richStart(){for(const id in S.sectors)for(const a of S.sectors[id].ast)for(const k in a.ore)a.ore[k]=Math.round(a.ore[k]*RICH.field);
  const mul=o=>{if(!o)return;for(const k in o)if(typeof o[k]==='number')o[k]=Math.round(o[k]*RICH.store)};
  for(const f in S.econ.stock)mul(S.econ.stock[f]);if(BRST.store!==1){const m2=o=>{if(!o)return;for(const k in o)if(typeof o[k]==='number')o[k]=Math.round(o[k]*BRST.store)};m2(S.econ.stock.brood);m2(S.econ.fleet.brood)}for(const f in S.econ.fleet)mul(S.econ.fleet[f]);for(const id in S.stations){const R=S.stations[id];if(R&&R.kind==='free'&&R.store)mul(R.store)}
  let m=0;for(const id in S.sectors)for(const a of S.sectors[id].ast)if(!a.comet)m+=oreTotal(a);S.ore0=m;S.repT=RICH.every;S.rich=1}
{const o=newGame;newGame=function(){const r=o.apply(this,arguments);try{if(S&&!S.training){richStart();const l=ledger();S.ledger0={tot:l.tot,credits:l.credits}}}catch(e){console.error(e)}return r}}
// the hourly drift: fresh rock where the fields are most worked out
function richReplenish(){if(!S.ore0){let m=0;for(const id in S.sectors)for(const a of S.sectors[id].ast)if(!a.comet)m+=oreTotal(a);S.ore0=m}let left=Math.round(S.ore0*RICH.rep);const added={};
  for(let guard=0;left>0&&guard<400;guard++){const c=[];for(const d of SECTOR_DEFS){if(d.kind==='hive')continue;const s=S.sectors[d.id];if(s.ast.length>=RICH.cap)continue;if(s.base0===undefined)s.base0=fieldMass(s);const f=s.base0?fieldMass(s)/s.base0:1;c.push([d,Math.max(.05,1.1-f)])}
    if(!c.length)break;const d=wpickArr(c),s=S.sectors[d.id],ores=Object.keys(d.ores||{fe:1}).filter(e=>oreHere(e,d.id));if(!ores.length)continue;const k=wpick(Object.fromEntries(ores.map(e=>[e,d.ores[e]||1])));
    const m=Math.min(left,ri(RICH.rock[0],RICH.rock[1]));s.ast.push({id:S.nextId++,...newAstPos(s),ore:{[k]:m},seed:ri(1,1e9),fresh:S.T});added[k]=(added[k]||0)+m;left-=m}
  for(const e in added)S.ledger0.tot[e]=(S.ledger0.tot[e]||0)+added[e];return added}
{const o=strategicTick;strategicTick=function(){const x=o.apply(this,arguments);try{if(!NET.cl&&!S.training&&S.ledger0){if(S.repT===undefined)S.repT=S.T+RICH.every;if(S.T>=S.repT){S.repT+=RICH.every;const a=richReplenish();const n=Object.values(a).reduce((p,q)=>p+q,0);if(n)feed(`Fresh rock has drifted in from the outer drift: ${fmt(n)} t across the worked-out fields.`,'news')}}}catch(e){console.error(e)}return x}}
