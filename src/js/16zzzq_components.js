//@src 16zzzq_components.js
// ============================================================ Beyond: four new components (agreed 8 Nov 2026; "Push the new components", 9 Nov 2026)
// BEYOND_DESIGN.md, "Proposal, revised: four components as alternatives". Standard parts, standard systems and the AI fleets'
// kits keep today's recipes. The makers' own lines use the new components in place of a standard one, one for one, by the
// maker's character, and R&D grades lean on Vantium and Aurorite:
//   Vantium Plating 2 Vantium + 1 Ferrite · Aurorite Cell 1 Aurorite + 2 Cuprite · Optic Array 1 Xenocrystal + 2 Cuprite ·
//   Thrust Vane 1 Iridium + 2 Ferrite.
//   - characterful parts (mp_): Hold Foundry and Quicksilver armour, cargo and charges Vantium Plating for a plate; Brightline
//     and Archive lasers and Spirewright mining lasers an Aurorite Cell for a coil (or conduit); Spirewright scanners and the
//     Mirrorwater and Marchgun launchers an Optic Array for a conduit; Wakefire launchers a Thrust Vane for a plate;
//   - systems by slot: drives a Thrust Vane for a plate; reactors and shields an Aurorite Cell for a coil (or conduit);
//     weapons systems an Optic Array for a conduit; armour, cargo and blast rigs Vantium Plating for a plate; payload bays a
//     Thrust Vane for a plate (from grade 2, where they have one);
//   - each grade above 1 of any maker line swaps one more plate for Vantium Plating (structural kinds) or one coil (else a
//     conduit) for an Aurorite Cell (energy kinds);
//   - Coldwater Refit, the budget maker, stays on standard components.
// Made: at the powers' works (keeping 80 Ferrite and 80 Cuprite, as their plate and conduit making does), at freeports with production, by the
// makers' works from the station's ore when the market has none, and by Fabricate. A maker whose host is short of Aurorite or
// Vantium asks for it to be mined (16zzzl_orejobs.js).
// The ledger: a fitted maker system counts as the item it is, not as a standard system; a fitted graded maker part as its
// graded item; a save from before is rebased once on load.
ITEMS.vplate={name:'Vantium Plating',recipe:{nu:2,fe:1},col:'#8fd6c8'};
ITEMS.acell={name:'Aurorite Cell',recipe:{au:1,cu:2},col:'#ffcf6a'};
ITEMS.optic={name:'Optic Array',recipe:{xc:1,cu:2},col:'#c8b0ff'};
ITEMS.vane={name:'Thrust Vane',recipe:{ir:1,fe:2},col:'#ff9f7a'};
const CMP4=['vplate','acell','optic','vane'];
for(const k of CMP4){ITEM_ORDER.push(k);CRAFTABLE.push(k);if(!TRADE_ITEMS.includes(k))TRADE_ITEMS.push(k);RD_CRAFT.add(k)}
{const o=stockTarget;stockTarget=function(id){return CMP4.includes(id)?30:o.apply(this,arguments)}}
// ---- the makers' recipes
const CMP_PART={hf:{charge:['plate','vplate'],cargo:['plate','vplate'],armor:['plate','vplate']},qs:{charge:['plate','vplate'],cargo:['plate','vplate'],armor:['plate','vplate']},
  bl:{laser:['coil','acell']},ad:{laser:['coil','acell']},sw:{mlaser:['coil','acell'],scanner:['wire','optic']},mwa:{missile:['wire','optic'],torpedo:['wire','optic']},mg:{missile:['wire','optic']},wf:{missile:['plate','vane'],torpedo:['plate','vane']}};
const CMP_SYS={engine:['plate','vane'],power:['coil','acell'],shield:['coil','acell'],weapon:['wire','optic'],armor:['plate','vplate'],cargo:['plate','vplate'],drill:['plate','vplate'],payload:['plate','vane']};
const CMP_ENERGY=new Set(['laser','mlaser','scanner','dronec','jammer','bdev','cscan','shield','power','weapon']);
// swap n of one component for another in a recipe (a coil swap falls back to conduit where there is no coil)
function cmpSwap(rc,from,to,n){for(let i=0;i<n;i++){let f=from;if(!(rc[f]>0)&&f==='coil')f='wire';if(!(rc[f]>0))return;rc[f]--;if(!rc[f])delete rc[f];rc[to]=(rc[to]||0)+1}}
(function(){for(const m in MK_LINE){if(m==='cr')continue;for(const id of MK_LINE[m]){const B=ITEMS[id];if(!B)continue;const kind=B.sys||B.part;if(kind==='land')continue;
    const base=B.sys?CMP_SYS[kind]:id.startsWith('mp_')?(CMP_PART[m]||{})[kind]:null;
    for(let g=1;g<=5;g++){const G=g>1?ITEMS[rdGid(id,g)]:B;if(!G||!G.recipe)continue;const rc={...G.recipe};if(base)cmpSwap(rc,base[0],base[1],1);
      if(g>1)CMP_ENERGY.has(kind)?cmpSwap(rc,'coil','acell',g-1):cmpSwap(rc,'plate','vplate',g-1);G.recipe=rc}}}
  for(const k in COMP)delete COMP[k];for(const k in DEPTH)delete DEPTH[k]})();
// ---- made at the powers' works and at freeports with production
function cmpCraft(st,item,max,cap,keep){const r=ITEMS[item].recipe;let n=0;while(n<max&&(st[item]||0)<cap&&Object.keys(r).every(k=>(st[k]||0)-r[k]>=(keep[k]||0))){takeFrom(r,[st]);inv.add(st,item,1);n++}return n}
function cmpIndustry(st){const keep={fe:80,cu:80};for(const k of CMP4)cmpCraft(st,k,2,30,keep)}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{if(!NET.cl&&S&&!S.training&&S.econ){for(const f of FAC_IDS){const st=S.econ.stock[f];if(st)cmpIndustry(st)}
    for(const R of mkStations())if(R.owner==='neutral'&&(devOf(R).prod||0)>=1&&!starving(R))cmpIndustry(storeOf(R))}}catch(e){console.error(e)}return r}}
// ---- the ledger: fitted maker systems and graded maker parts count as what they are
function cmpFitDelta(R){const d={};const sub=(o,s)=>{for(const k in s)d[k]=(d[k]||0)-s[k]},add=(o)=>{for(const k in o)d[k]=(d[k]||0)+o[k]};
  for(const sl in(R.sysm||{})){const m=R.sysm[sl];if(!m)continue;const t=(R.tiers||{})[sl]||1,I=ITEMS[rdGid(`sy_${m}_${sl}`,t)];if(!I)continue;add(I.recipe);sub(null,compInv(sl,t))}
  const F=R.fit;if(F){for(const[ids,gr]of[[F.wi,F.g],[F.ui,F.ug]]){if(!ids)continue;ids.forEach((it,i)=>{const g=(gr||[])[i]||1;if(!it||g<2||!ITEMS[it]||!ITEMS[it].maker)return;const G=ITEMS[rdGid(it,g)];if(!G)return;add(G.recipe);sub(null,ITEMS[it].recipe);for(let t=2;t<=g;t++)sub(null,partUpg(t))})}}return d}
{const o=ledger;ledger=function(){const r=o.apply(this,arguments);try{const Y=r.L['Your ship, hold, vault'];for(const P of allPilots()){if(!P)continue;for(const R of[P,...(P.ships||[])]){const v=invVec(cmpFitDelta(R));for(const e of RAWS){Y[e]+=v[e];r.tot[e]+=v[e]}}}}catch(e){console.error(e)}return r}}
// (fitting a graded maker part already unpacks it into its line's part and the standard grade components; cmpFitDelta books
// what its grade really holds, and taking it out gives the graded item back, so that stays exact)
// stripping a ship's grades (a sale): a maker system gives back what its grades really hold, and stays fitted at its grade 1
{const o=shipStrip;shipStrip=function(R,into){const L=[];for(const sl in(R&&R.sysm)||{}){const m=R.sysm[sl],t=(R.tiers||{})[sl]||1;if(m&&t>1&&ITEMS[rdGid(`sy_${m}_${sl}`,t)])L.push([sl,m,t])}
  const r=o.apply(this,arguments);try{for(const[sl,m,t]of L){const std={};const a=compInv(sl,t),b=compInv(sl,1);for(const k in a){const n=a[k]-(b[k]||0);if(n>0)std[k]=n}
    const act={};const A=ITEMS[rdGid(`sy_${m}_${sl}`,t)].recipe,B=ITEMS[rdGid(`sy_${m}_${sl}`,1)].recipe;for(const k in A){const n=A[k]-(B[k]||0);if(n>0)act[k]=n}
    if(haveIn(std,[into])){takeFrom(std,[into]);inv.addAll(into,act)}}}catch(e){console.error(e)}return r}}
// a save from before the four components: rebase the ledger once
{const o=newGame;newGame=function(){const r=o.apply(this,arguments);try{if(S)S.cmp4=1}catch(e){}return r}}
{const o=migrate;migrate=function(){const r=o.apply(this,arguments);try{if(S&&!S.cmp4){S.cmp4=1;const l=ledger();S.ledger0={tot:l.tot,credits:l.credits}}}catch(e){console.error(e)}return r}}
