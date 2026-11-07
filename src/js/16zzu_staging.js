//@src 16zzu_staging.js
// ============================================================ Beyond: the Varkesh foundries and forward staging (6 Nov 2026)
// Two game rules the user chose to bring live space back into balance (no hidden mining rates).
//
// The Varkesh foundries (Varkesh's third perk, with its tougher hulls): the Dominion turns its ore into Alloy Plate and Conduit
// wherever it has it. Its warehouse smelts down to a smaller ore reserve (40 Ferrite or Cuprite kept back, against 80 for the
// others), and every Varkesh depot smelts plate and conduit from its own ore, as a depot with a production module does, without
// needing one (so its miners and garrison are fitted from their own depot instead of waiting on the warehouse). Each plate
// still takes 3 Ferrite, each conduit 3 Cuprite: nothing is created.
//
// Forward staging: each power, and the Brood, keeps a staging stock (war materiel: plate, conduit, coil, missiles, torpedoes)
// at its forward depot, the one nearest a hostile system, shipped out from home by convoy (raidable). An offensive whose force
// the staging stock can supply launches from there instead of from home: its force is taken from the staging stock (and what
// home had set aside for it goes back into the warehouse), so the strike group flies a short way to its target.
const VF={keep:40,depot:12};
const STG={kit:{plate:36,wire:24,coil:14,missile:10,torpedo:10},every:180,min:1};
// ---- the Varkesh foundries
{const o=craftDown;craftDown=function(st,item,keep,max){if(S&&S.econ&&st===S.econ.stock.varkesh&&(item==='plate'||item==='wire')&&keep){const k={};for(const x in keep)k[x]=Math.min(keep[x],VF.keep);return o.call(this,st,item,k,max)}return o.apply(this,arguments)}}
function vfTick(){for(const id in S.stations){const R=S.stations[id];if(!R||R.owner!=='varkesh'||R.kind!=='depot'||(devOf(R).prod||0)>=1||starving(R))continue;const ds=dStore(R);craftDown(ds,'plate',{fe:20},VF.depot);craftDown(ds,'wire',{cu:20},VF.depot)}}
// ---- forward staging
function stgHome(f){return f==='brood'?'bl':FAC_IDS.includes(f)?FAC_HOME(f):null}
function stgDepots(f){return Object.values(S.stations).filter(R=>R&&R.owner===f&&R.kind==='depot'&&(f==='brood'||isDepotF(R)))}
// the forward depot: the one fewest jumps from a system held by a power it fights (or the Brood, for the powers)
function stgFront(f){let best=null,bh=99;const foes=SECTOR_DEFS.map(d=>d.id).filter(id=>{const o=sectorOwner(id);return o&&o!==f&&o!=='neutral'&&o!=='pirate'&&hostile(f,o)});if(!foes.length)return null;
  for(const R of stgDepots(f)){let h=99;for(const id of foes){const x=HOP[R.sid][id];if(x!=null&&x<h)h=x}if(h<bh){bh=h;best=R}}return best}
function stgTick(){S.stg=S.stg||{};for(const f of[...FAC_IDS,'brood']){const g=S.stg[f]=S.stg[f]||{t:0};if(S.T<g.t)continue;g.t=S.T+STG.every;const R=stgFront(f);g.sid=R?R.sid:null;if(!R)continue;
  const key='stg:'+R.sid;if(haulBusy(key))continue;const home=S.econ.stock[f],ds=dStore(R),load={};if(!home)continue;
  for(const k in STG.kit){const lack=STG.kit[k]-(ds[k]||0);if(lack<=0)continue;const spare=Math.max(0,(home[k]||0)-STG.kit[k]);const n=Math.min(lack,spare);if(n>0)load[k]=inv.take(home,k,n)}
  if(Object.keys(load).length)haulSend(f,stgHome(f),R.sid,load,key,'staging')}}
{const o=strategicTick;strategicTick=function(){const x=o.apply(this,arguments);try{if(!NET.cl&&!S.training){vfTick();stgTick()}}catch(e){console.error(e)}return x}}
// an offensive launches from the forward depot when its staging stock can field the whole force
{const o=prwStrikeStart;prwStrikeStart=function(ev){try{const g=S.stg&&S.stg[ev.att],R=g&&g.sid&&S.stations[g.sid];
  if(R&&R.owner===ev.att&&R.sid!==ev.sector&&Object.keys(ev.force).length){const ds=dStore(R),hf=HOP[R.sid][ev.sector],hh=HOP[stgHome(ev.att)]?HOP[stgHome(ev.att)][ev.sector]:99;
    if(hf!=null&&hf<hh&&haveIn(ev.force,[ds])){const home=S.econ.stock[ev.att]||S.econ.stock.pirate,swap={...ev.force};inv.addAll(home,swap);for(const k in ev.force)delete ev.force[k];takeFrom(swap,[ds]);inv.addAll(ev.force,swap);ev.staged=R.sid}}}catch(e){console.error(e)}
  if(!ev.staged)return o.apply(this,arguments);
  // launch from the staging depot
  const from=ev.staged,path=trPath(from,ev.sector);if(!path||path.length<2){ev.trDone=1;return}const ships=[];(ev.cls||[]).forEach(c=>ships.push({cls:c,tier:ev.tier,ld:loadout(ev.att==='pirate'?'pirate':'patrol',ev.tier,c)}));if(!ships.length){ev.trDone=1;return}
  const r={id:S.nextId++,side:ev.att,src:from,cap:null,tgt:null,dep:null,dest:ev.sector,sector:from,path,leg:0,next:S.T+RAID.hop,state:'out',ships,kit:{},loot:{},back:[],T0:S.T,strike:ev.id};
  inv.addAll(r.kit,ev.force);for(const k in ev.force)delete ev.force[k];ev.tr=r.id;ev.eta=1e12;(S.raids=S.raids||[]).push(r);if(WORLDS[r.sector])inW(WORLDS[r.sector],()=>raidSpawn(r,false))}}
// the map panel: the forward depot
{const o=mapSectorNow;mapSectorNow=function(sid){let h=o.apply(this,arguments);try{for(const f in S.stg||{})if(S.stg[f].sid===sid){const R=S.stations[sid],ds=R&&dStore(R);let m=0;for(const k in STG.kit)m+=ds&&ds[k]||0;h+=`<span>Staging</span><b>${esc(sideName(f))} forward depot · ${m} units of war materiel</b>`}}catch(e){}return h}}
