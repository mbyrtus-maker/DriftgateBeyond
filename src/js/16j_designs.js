//@src 16j_designs.js
// ============================================================ faction hull designs (Beyond stage 6, first wave: the fighters)
// Each power builds each fighter class its own way, with its own model (generated in code: tools/previews/beyond_hulls.py,
// packed by tools/build_models.py as dz_*) and its own stats in more than one number. A design replaces the faction's flat
// trait for that class; classes without a design yet keep the shared model and the trait. AI fleets fly their power's designs.
// A pilot's design line (P.faction) follows the hull it last bought: a power's yard builds that power's designs, and each
// freeport's yard builds a mix of designs rolled when the galaxy is made.
// m: model; multipliers on hull, shield, energy (capacity), regen, speed, acc (thrust), turn, radius, dmg; lock: lock-time
// factor; w/u: weapon and utility slots when they differ from the class's
const DESIGN={
  halcyon:{interceptor:{m:'dz_swift',name:'Swift',hull:.84,shield:1.06,speed:1.03,acc:1.03,radius:.95,txt:'Fast and light, strong shields, thin hull'},
    striker:{m:'dz_kite',name:'Kite',hull:.9,shield:1.16,speed:1.04,turn:1.02,txt:'Quick, well shielded, lightly built'},
    heavy:{m:'dz_osprey',name:'Osprey',hull:.88,shield:1.18,speed:1.04,u:['land','scanner'],txt:'Shield-heavy gun platform on twin booms'}},
  varkesh:{interceptor:{m:'dz_fang',name:'Fang',hull:1.24,shield:.95,energy:.92,regen:.92,speed:.92,acc:.92,turn:.97,radius:1.04,w:['gun','gun','laser','missile'],txt:'Slow, heavily armoured, an extra weapon slot, a hungry reactor'},
    striker:{m:'dz_talon',name:'Talon',hull:1.2,energy:.88,regen:.88,speed:.95,turn:.96,txt:'Armoured pincer with a hungry reactor'},
    heavy:{m:'dz_halberd',name:'Halberd',hull:1.12,energy:.9,regen:.9,speed:.9,turn:.92,w:['gun','gun','gun','laser','missile','missile'],txt:'A brawler: thick armour, six weapon slots, slow to turn'}},
  ostrova:{interceptor:{m:'dz_mote',name:'Mote',hull:1,shield:.92,energy:1.25,regen:1.2,turn:1.04,lock:.8,txt:'Deep reactor, the best lock range and sensors, weak shields'},
    striker:{m:'dz_wisp',name:'Wisp',hull:1.02,shield:1,energy:1.2,regen:1.15,turn:1.05,lock:.85,txt:'Agile crescent with a deep reactor'},
    heavy:{m:'dz_vigil',name:'Vigil',hull:1.03,shield:1,energy:1.25,regen:1.2,turn:.97,lock:.85,txt:'A deep-reactor focus platform; quick locks'}}};
function designOf(fac,cls){return(DESIGN[fac]||{})[cls]||null}
{const o=shipStatsBase;shipStatsBase=function(fac,cls,T){const d=designOf(fac,cls);if(!d)return o.apply(this,arguments);const B=o.call(this,null,cls,T),k=x=>d[x]||1;
  B.hull*=k('hull');B.sCap*=k('shield');B.eCap*=k('energy');B.eRegen*=d.regen||k('energy');B.maxSpd*=k('speed');B.thrust*=k('acc');B.turn*=k('turn');B.radius*=k('radius');B.dmg*=k('dmg');B.design=d.name;return B}}
{const o=vK;vK=function(P,key){const v=o.apply(this,arguments);if(key==='lockK'&&P){const d=designOf(P.faction,P.cls);if(d&&d.lock)return v*d.lock}return v}}
// the design a dock's yard builds for a class: a power's yard its own, a freeport's the one rolled for it
// (Beyond, 3 Nov 2026, the user: each freeport a random mix of hulls) every hull a freeport's yard builds is rolled to one
// power's line, work ships and scouts too, so each freeport offers a mix; older saves fill in the classes they lack
// (user) favouring the nearest power: its line half the time, the other two a quarter each
function yardNear(id){let best=null,bd=1e9;for(const f of FAC_IDS){const h=HOP[id]&&HOP[id][FAC_HOME(f)];if(h!=null&&h<bd){bd=h;best=f}}return best}
function yardPick(id){const n=yardNear(id);if(!n)return pick(FAC_IDS);if(Math.random()<.5)return n;return pick(FAC_IDS.filter(f=>f!==n))}
function yardRoll(){S.yardRoll=S.yardRoll||{};for(const id in S.stations||{}){const R=S.stations[id];if(!R||R.owner!=='neutral')continue;const o=S.yardRoll[id]=S.yardRoll[id]||{};for(const k of YARD_IDS)if(!o[k])o[k]=yardPick(id)}}
function yardDesign(c,cls){if(!c||c.kind!=='station')return null;if(c.owner==='neutral'){yardRoll();const r=(S.yardRoll||{})[S.player.sector];return r&&r[cls]||null}if(!designOf('halcyon',cls))return null;if(FAC_IDS.includes(c.owner))return c.owner;return null}
{const o=newGame;newGame=function(){const r=o.apply(this,arguments);if(S)yardRoll();return r}}
// buying a fighter takes this yard's design: your design line becomes that power's (it goes back if the purchase fails)
{const o=dockAction;dockAction=function(act,arg){if(act==='hull'&&!S.unb){const c=dockCtx(),P=S.player,f=yardDesign(c,arg);if(f&&f!==P.faction){const f0=P.faction;P.faction=f;dockErr='';o.apply(this,arguments);
      if(!String(dockErr).startsWith('✓')){P.faction=f0;return}fitOf(P);if(W&&W.player){refreshPlayerStats();W.player.fac=f}dockErr+=` It's ${/^[AEIOU]/.test(FACTIONS[f].short)?'an':'a'} ${FACTIONS[f].short} design: the ${designOf(f,arg)?designOf(f,arg).name:FAC(f).hulls[arg]}.`;return}}return o.apply(this,arguments)}}
// every freeport has a yard (Beyond): it builds the faction designs rolled for it, for anyone who can dock
{const o=dockCtx;dockCtx=function(){const c=o.apply(this,arguments);if(c&&c.kind==='station'&&c.owner==='neutral'&&!S.unb)c.hulls=true;return c}}
// ---- the powers' work ships (miners and haulers): their own approved models (tools/previews/beyond_work.py, packed as dz_*).
// Models only for now: the classes keep Driftgate 1's stats and slots, so no design line or stat changes come with them.
const WORK_MDL={halcyon:{skiff:'dz_wren',prospector:'dz_plover',dredger:'dz_heron',courier:'dz_tern',freighter:'dz_albatross',bulker:'dz_pelican'},
  varkesh:{skiff:'dz_pick',prospector:'dz_gouge',dredger:'dz_sledge',courier:'dz_runner',freighter:'dz_bulwark',bulker:'dz_rampart'},
  ostrova:{skiff:'dz_glim',prospector:'dz_lumen',dredger:'dz_delve',courier:'dz_drift',freighter:'dz_cairn',bulker:'dz_monolith'}};
{const o=shipMesh;shipMesh=function(fac,cls){const m=WORK_MDL[fac]&&WORK_MDL[fac][cls];if(m&&mdlHas(m)){const key='wk'+fac+cls;if(MESH[key])return MESH[key];const L=new GB();L.seg([0,0,0],[0,0,0],[0,0,0]);
  return MESH[key]={hull:mdlMesh(m,fac,1),rim:L.upload(true),eng:engFix(m).map(e=>e.slice()),mdl:true}}return o.apply(this,arguments)}}

