//@src 16zzp_freight.js
// ============================================================ Beyond: goods go by hauler (live space stage 4, 6 Nov 2026)
// No chance-spawned haulers: every freighter in space is a tracked convoy (S.traders). And goods that used to jump between
// places now ride a convoy (haulSend), which flies the lanes, shows in a live system and can be raided:
//   - an outpost's surplus goes home (it went straight into the warehouse);
//   - a depot's or outpost's miners and garrison are kitted from what is there, and ask the warehouse for kits by convoy
//     (they were taken straight from the warehouse);
//   - plunder from a captured station or outpost goes home to the victor;
//   - aid shipments and pact trades go from one power's home to the other's;
//   - a merchant whose market is gone, or a convoy whose station was lost, turns for home instead of vanishing into it.
// The Brood too (6 Nov 2026, the user): its depots (Bloom Nodes) and outposts keep their own stores, and Gorgers and Bloaters
// carry their ore and kits to and from the hive. The Unbound's loot still comes home with their raids.
const FR={opMin:30,opKeep:25,kitAsk:2};
const FR_KIT=new Set(['plate','wire','coil','lattice','drone','missile','torpedo','swarm','tune']);
function frPower(f){return FAC_IDS.includes(f)}
// the sides with freighters, and where their warehouse is
function frCv(f){return FAC_IDS.includes(f)||f==='brood'}
function frHomeSid(f){return f==='brood'?'bl':FAC_IDS.includes(f)?FAC_HOME(f):null}
// ship a load to a power's home (or into another power's warehouse with intoF); straight in when it's already there
function frShip(f,fromSid,load,key,why,intoF){if(!load||!Object.keys(load).length)return null;const dest=intoF||f,to=frCv(dest)?frHomeSid(dest):null;
  if(!frCv(f)||!frCv(dest)||!to||fromSid===to||!trPath(fromSid,to)){inv.addAll(S.econ.stock[dest]||S.econ.stock.pirate,load);return null}
  const t=haulSend(f,fromSid,to,load,key+':'+S.nextId,why);if(t&&intoF&&intoF!==f)t.intoF=intoF;return t}
// convoys with somewhere particular to go: an outpost's store, another power's warehouse; a convoy that can't deliver turns
// for its own home
{const o=haulArrive;haulArrive=function(t){try{
  if(t&&t.okit){const ob=S.outposts[t.okit];if(ob&&ob.owner===t.side){cvEnd(t,true);inv.addAll(ob.stock,t.load);t.load={};return}}
  if(t&&t.intoF&&S.econ.stock[t.intoF]){cvEnd(t,true);inv.addAll(S.econ.stock[t.intoF],t.load);t.load={};return}
  if(t&&!t.own&&!t.car&&!t.okit&&frCv(t.side)){const B=S.stations[t.to];if((!B||B.owner!==t.side)&&t.to!==frHomeSid(t.side)&&Object.keys(t.load||{}).length){cvEnd(t,true);frShip(t.side,t.to,t.load,'back','return');t.load={};return}}
  }catch(e){console.error(e)}return o.apply(this,arguments)}}
// ---- outposts: the surplus over 25 of each good (not kits) ships home once there's a hold's worth
function frOutpost(oid){const o=S.outposts[oid];if(!o||!frCv(o.owner))return false;const key='op:'+oid;if(haulBusy(key))return true;
  const load={};let m=0;for(const k in o.stock){if(FR_KIT.has(k))continue;const n=(o.stock[k]||0)-FR.opKeep;if(n>0){load[k]=n;m+=n}}
  if(m<FR.opMin)return true;for(const k in load)inv.take(o.stock,k,load[k]);haulSend(o.owner,o.sector,frHomeSid(o.owner),load,key,'ore');return true}
// ---- kits at a site: the site's own store away from home; short, it asks the warehouse for a couple of kits by convoy
// (when a galaxy starts, the first rosters and garrisons are fitted from the warehouse: the depots were founded stocked)
let frSeed=false;
function frAway(st){return!frSeed&&frCv(st.owner)&&!(st.R&&(st.R.kind==='core'||st.R.kind==='hive'))}
{const o=mrTick;mrTick=function(){frSeed=!S.mrInit;try{return o.apply(this,arguments)}finally{frSeed=false}}}
{const o=grTick;grTick=function(){frSeed=!S.grInit;try{return o.apply(this,arguments)}finally{frSeed=false}}}
function frSiteStore(st){return st.R?dStore(st.R):st.o.stock}
function frAsk(st,ld){const f=st.owner,want={};for(const k in ld)want[k]=ld[k]*FR.kitAsk;
  // a depot's kits come on their own convoy, so they don't hold up its other supplies (upgrades, capital kits)
  if(st.R){const R=st.R,key='kit:'+R.sid;if(haulBusy(key))return false;const home=S.econ.stock[f],load={};for(const k in want){const lack=want[k]-(dStore(R)[k]||0);if(lack<=0)continue;const n=Math.min(lack,home[k]||0);if(n>0)load[k]=inv.take(home,k,n)}
    if(!Object.keys(load).length)return false;return!!haulSend(f,frHomeSid(f),R.sid,load,key,'supplies')}
  const o=st.o,oid=st.key.slice(2),key='okit:'+oid;if(haulBusy(key))return false;const home=S.econ.stock[f],load={};
  for(const k in want){const lack=want[k]-(o.stock[k]||0);if(lack<=0)continue;const n=Math.min(lack,home[k]||0);if(n>0)load[k]=inv.take(home,k,n)}
  if(!Object.keys(load).length)return false;const t=haulSend(f,frHomeSid(f),o.sector,load,key,'supplies');if(t)t.okit=oid;return!!t}
// miners: kit from the site's store when away from home
{const o=mrSrcs;mrSrcs=function(st){if(frAway(st))return[frSiteStore(st)];return o.apply(this,arguments)}}
{const o=mrKit;mrKit=function(st){const k=o.apply(this,arguments);if(!k&&frAway(st))try{frAsk(st,loadout('miner',1,'prospector'))}catch(e){}return k}}
// garrisons: the same, from the site's store (at a power's home: the muster, then the warehouse)
{const o=grKit;grKit=function(f,st){if(!st||!frAway(st))return o.call(this,f);const srcs=[frSiteStore(st)];let tier=factionTier(f),c=pickFighter('patrol'),ld=loadout('patrol',tier,c);
  if(!haveIn(ld,srcs)){c='interceptor';ld=loadout('patrol',tier,c)}while(!haveIn(ld,srcs)&&tier>1){tier--;ld=loadout('patrol',tier,c)}
  if(!takeFrom(ld,srcs)){try{frAsk(st,loadout('patrol',factionTier(f),'striker'))}catch(e){}return null}return{c,t:tier,load:ld}}}
// an outpost's kit stays in its store for its own crews; the surplus run leaves it
// ---- no chance haulers in a live system: what you see hauling is a tracked convoy
{const o=popWants;popWants=function(){return o.apply(this,arguments).filter(w=>w[0]!=='hauler')}}
// ---- the Brood's depots (Bloom Nodes) keep their own store: their mining lands there, and a Gorger carries the ore to the hive
// once there's a hold's worth (it all went straight into the hive's store before)
function frBroodDepot(R){return!!R&&R.kind==='depot'&&R.owner==='brood'}
{const o=storeOf;storeOf=function(R){if(frBroodDepot(R))return dStore(R);return o.apply(this,arguments)}}
function frBroodTick(){for(const id in S.stations){const R=S.stations[id];if(!frBroodDepot(R))continue;const key='bd:'+id;if(haulBusy(key))continue;const ds=dStore(R),load={};let m=0;
  for(const k in ds){if(FR_KIT.has(k))continue;const n=(ds[k]||0)-FR.opKeep;if(n>0){load[k]=n;m+=n}}if(m<FR.opMin)continue;for(const k in load)inv.take(ds,k,load[k]);haulSend('brood',id,'bl',load,key,'ore')}}
{const o=strategicTick;strategicTick=function(){const x=o.apply(this,arguments);try{if(!NET.cl)frBroodTick()}catch(e){console.error(e)}return x}}
