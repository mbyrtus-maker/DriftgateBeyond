//@src 16zzzr_stdparts.js
// ============================================================ Beyond: standard parts and systems at every station (user, 9 Nov 2026)
// "I'm docked at Mirrorwater and standard parts aren't available. Standard parts should start at all stations with all systems
// with some stock." This reverses part of 3 Nov 2026 ("markets sell only corporations' parts"): the makers' parts stay, and
// beside them every power's and freeport's market now starts with STD.part of each standard (unbranded) part and STD.sys of
// each standard grade 1 system, and keeps them: every STD.every seconds a station short of one builds it from its own store
// (as the powers build plate and conduit), so the ledger stays exact. A save from before gets the starting stock once (the
// ledger is rebased then, as at a new galaxy's start).
const STD={part:3,sys:2,depot:1,every:600,keep:{fe:80,cu:80}};
function stdSysIds(){return Object.keys(SYS_LINES).map(sl=>rdGid('sy_'+sl,1)).filter(id=>ITEMS[id]&&Object.keys(ITEMS[id].recipe).length)}
function stdWant(){const o={};for(const k in PART)o[PART[k]]=STD.part;for(const id of stdSysIds())o[id]=STD.sys;return o}
function stdSeed(){for(const R of mkStations()){let st;try{st=mkStock(R)}catch(e){continue}if(!st)continue;const W0=stdWantAt(R);for(const id in W0){const n=W0[id]-(st[id]||0);if(n>0)inv.add(st,id,n)}}}
{const o=partsSeed;partsSeed=function(){const r=o.apply(this,arguments);try{stdSeed();S.stdSeed=1}catch(e){console.error(e)}return r}}
{const o=migrate;migrate=function(){const r=o.apply(this,arguments);try{if(S&&!S.stdSeed&&!S.training){stdSeed();S.stdSeed=1;const l=ledger();S.ledger0={tot:l.tot,credits:l.credits}}}catch(e){console.error(e)}return r}}
// kept in stock: every STD.every seconds a station short of one builds it, from its own store first (turning its ore into
// the plate, conduit or coil the recipe needs), else, at a power's depot, from its power's warehouse (the core's store).
// A power's depot keeps STD.depot of each (cores and freeports the full STD.part / STD.sys); depots built during the game
// start empty and fill as they can. A power's warehouse turns ore into components only above 80 Ferrite and 80 Cuprite (what
// the powers keep for their own plate and conduit making); a depot's or freeport's own ore is used as it is.
function stdWantAt(R){const W0=stdWant();if(isDepotF(R))for(const k in W0)W0[k]=Math.min(W0[k],STD.depot);return W0}
function stdComp(rc,src,depth,keep){for(const k in rc){const need=rc[k]-(src[k]||0);if(need<=0)continue;const c=ITEMS[k]&&ITEMS[k].recipe;if(!c||depth>1||!['plate','wire','coil'].includes(k))return false;
  for(let i=0;i<need;i++){if(!stdComp(c,src,depth+1,keep)||!Object.keys(c).every(e=>(src[e]||0)-c[e]>=(keep[e]||0)))return false;takeFrom(c,[src]);inv.add(src,k,1)}}return haveIn(rc,[src])}
function stdBuild(id,st,srcs){const rc=ITEMS[id].recipe;for(const src of srcs){if(!src)continue;const keep=stdIsWh(src)?STD.keep:{};if(haveIn(rc,[src])||stdComp(rc,src,0,keep)){takeFrom(rc,[src]);inv.add(st,id,1);return true}}return false}
function stdIsWh(src){return!!S.econ&&FAC_IDS.some(f=>S.econ.stock[f]===src)}
function stdTick(){if(NET.cl||!S||S.training||S.unb||S.T<(S.stdT||0))return;S.stdT=S.T+STD.every;
  for(const R of mkStations()){let st;try{st=mkStock(R)}catch(e){continue}if(!st)continue;const W0=stdWantAt(R),wh=isDepotF(R)&&S.econ&&S.econ.stock[R.owner];const srcs=[st,wh!==st?wh:null];
    for(const id in W0){let n=W0[id]-(st[id]||0);while(n-->0&&stdBuild(id,st,srcs));}}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{stdTick()}catch(e){console.error(e)}return r}}
for(const k in PART)if(ITEMS[PART[k]])ITEMS[PART[k]].trTxt='Standard: no strength, no weakness. Every station keeps a few.';
for(const id of stdSysIds())ITEMS[id].trTxt='Standard: the system ships come with. Every station keeps a few.';
