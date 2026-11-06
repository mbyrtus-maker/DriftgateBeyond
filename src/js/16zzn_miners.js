//@src 16zzn_miners.js
// ============================================================ Beyond: station miners (live space stage 1, 6 Nov 2026)
// Every power's station and depot, the Brood's hive and each outpost a power or the Brood holds keeps a roster of miners,
// each with its kit (plate, coil, guard drones) aboard. Off-screen the site's ore is its roster's work: the old flat rate at
// full strength, less for every miner missing. In a live system the roster flies: out at the rocks, home to unload, a
// short turnaround docked, out again; live they drill at the same average rate they mine off-screen. A miner killed is
// gone from the roster with its kit; the site builds another from its stores (one at a time, every 4 minutes). No miner
// is spawned by chance any more: every one in space belongs to a roster.
const MR={n:{core:4,depot:3,hive:4,out:2},build:240,retry:60,turn:[30,60],duty:.6,mix:{skiff:1,prospector:2,dredger:1},droneKeep:6};
const MR_W=(()=>{let t=0,m=0;for(const k in MR.mix){t+=MR.mix[k];m+=MR.mix[k]*CLASSES[k].drill}const avg=m/t,w={};for(const k in MR.mix)w[k]=CLASSES[k].drill/avg;return w})();
// the sites: 'S.<station sector>' and 'O.<outpost id>'
function mrSites(){const L=[];for(const sid in S.stations){const R=S.stations[sid];if(R&&FACTIONS[R.owner]&&MR.n[R.kind])L.push('S.'+sid)}
  for(const oid in S.outposts){const o=S.outposts[oid];if(o&&FACTIONS[o.owner]&&o.type!=='yard')L.push('O.'+oid)}return L}
function mrSite(key){const id=key.slice(2);if(key[0]==='S'){const R=S.stations[id];return R?{key,kind:R.kind,owner:R.owner,sid:id,R}:null}const o=S.outposts[id];return o?{key,kind:'out',owner:o.owner,sid:o.sector,o}:null}
function mrOn(st){return!!st&&!!FACTIONS[st.owner]&&!!MR.n[st.kind]&&!(st.o&&st.o.type==='yard')}
function mrTarget(st){return MR.n[st.kind]||0}
function mrRoster(key){const R=(S.mrs=S.mrs||{});return R[key]}
// the share of the site's full mining its roster can do now (1 for anything that has no roster: the player's stations, freeports)
function mrWork(key){const st=mrSite(key);if(!mrOn(st))return 1;const ro=mrRoster(key);if(!ro||ro.f!==st.owner)return 0;let w=0;for(const m of ro.m)w+=MR_W[m.c]||1;return Math.min(1.5,w/mrTarget(st))}
// a site's full mining per 10 s, as the off-screen tick has it
function mrBase(st){if(st.o)return 2+st.o.level;const R=st.R,cn=S.T>150&&capNeed(R.owner);return stRate(R,cn)}
function mrSrcs(st){const L=[];if(st.R){const s=storeOf(st.R);if(s)L.push(s)}const h=S.econ.stock[st.owner];if(h&&!L.includes(h))L.push(h);return L}
function mrKit(st){const c=wpick(MR.mix),srcs=mrSrcs(st),ld=loadout('miner',1,c);const dr=ld.drone||0;delete ld.drone;if(!takeFrom(ld,srcs))return null;
  let have=0;for(const s of srcs)have+=s.drone||0;const n=Math.min(dr,Math.max(0,have-MR.droneKeep));if(n>0){takeFrom({drone:n},srcs);ld.drone=n}return{c,load:ld}}
// keep each roster: a site that changed hands loses its miners (kits docked there go to the system's debris), a short one builds
function mrTick(){const R=(S.mrs=S.mrs||{}),keys=mrSites(),init=!S.mrInit;S.mrInit=1;
  for(const key in R){const st=mrSite(key),ro=R[key];if(mrOn(st)&&ro.f===st.owner)continue;const s=S.sectors[ro.sid];for(const m of ro.m)if(!m.live&&s)toDebris(s,m.load);delete R[key]}
  for(const key of keys){const st=mrSite(key);let ro=R[key];if(!ro)ro=R[key]={f:st.owner,sid:st.sid,m:[],t:S.T,nid:1};const want=mrTarget(st);
    while(ro.m.length<want&&S.T>=ro.t){const k=mrKit(st);if(!k){ro.t=S.T+MR.retry;break}ro.m.push({id:ro.nid++,c:k.c,load:k.load,live:false,next:0});ro.t=init?S.T:S.T+MR.build;if(!init)break}}}
{const o=strategicTick;strategicTick=function(){try{mrTick()}catch(e){console.error(e)}return o.apply(this,arguments)}}
// the kits docked count with the stations
{const o=ledger;ledger=function(){const r=o.apply(this,arguments);try{const L=r.L.Stations;for(const k in S.mrs||{})for(const m of S.mrs[k].m){const v=invVec(m.load||{});for(const e of RAWS){L[e]+=v[e];r.tot[e]+=v[e]}}}catch(e){}return r}}
// 'mrs:<site>:<id>' holds a roster miner's kit; once it's gone the site's store (or its owner's) takes what comes home
function mrEntry(key,id){const ro=mrRoster(key);return ro&&ro.m.find(m=>String(m.id)===String(id))||null}
{const o=holderIn;holderIn=function(st,path){if(typeof path==='string'&&path.startsWith('mrs:')){const p=path.split(':'),ro=st.mrs&&st.mrs[p[1]],m=ro&&ro.m.find(x=>String(x.id)===p[2]);if(m)return m.load=m.load||{};
  const k=p[1]||'',id=k.slice(2);if(k[0]==='S'&&st.stations[id]){const R=st.stations[id];return(isDepotF(R)?(R.store=R.store||{}):st.econ.stock[R.owner])||st.econ.stock[ro?ro.f:'pirate']||st.econ.stock.pirate}
  if(k[0]==='O'&&st.outposts[id]&&st.econ.stock[st.outposts[id].owner])return st.econ.stock[st.outposts[id].owner];return ro&&st.econ.stock[ro.f]||st.econ.stock.pirate}return o.apply(this,arguments)}}
// home: the kit goes back aboard (docked), whatever is in the hold goes to the site's store
{const o=returnHome;returnHome=function(e){if(e&&e.mrKey){const m=mrEntry(e.mrKey,e.mrId);if(m){const st=mrSite(e.mrKey);inv.addAll(m.load,e.load);e.load={};if(invMass(e.cargo)>0){const h=st&&(st.R?storeOf(st.R):st.o.stock)||S.econ.stock[e.side]||S.econ.stock.pirate;inv.addAll(h,e.cargo);e.cargo={}}
  m.live=false;m.next=S.T+rnd(MR.turn[0],MR.turn[1])}}return o.apply(this,arguments)}}
// killed: off the roster for good
{const o=killShip;killShip=function(e){if(e&&e.mrKey&&e.role!=='limpet'){const ro=mrRoster(e.mrKey);if(ro){const i=ro.m.findIndex(m=>String(m.id)===String(e.mrId));if(i>=0)ro.m.splice(i,1);if(ro.m.length<mrTarget(mrSite(e.mrKey)||{}))ro.t=Math.max(ro.t,S.T+MR.build)}e.mrKey=null}return o.apply(this,arguments)}}
// live: the roster flies. A miner spawns from its kit, drills at the rate its share of the site's mining comes to, and is
// placed at the rocks when the system opens (the work already under way) or launched from the station after its turnaround
function mrSpawn(st,ro,m,initial){const side=st.owner,e=makeNPC('miner',side,m.c,1,m.load,`mrs:${st.key}:${m.id}`);m.load={};m.live=true;e.mrKey=st.key;e.mrId=m.id;
  const per=mrBase(st)/mrTarget(st)/10*(MR_W[m.c]||1),nom=e.st.drill*(side==='brood'?1:BAL.aiEff);e.mrK=Math.min(1,per/MR.duty/Math.max(.01,nom));
  const s=S.sectors[W.sid],D=st.R?W.stationEnt:W.outpostEnt,rocks=s.ast.filter(x=>!x.comet);
  if(initial&&rocks.length){const a=pick(rocks),o=rdir(.6),k=astR(a)+rnd(70,140);e.x=a.x+o.x*k;e.y=a.y+o.y*k;e.z=a.z+o.z*k;e.ai.ast=a;e.mineAcc=Math.random();faceInstant(e,a.x-e.x,a.y-e.y,a.z-e.z)}
  else if(D){const o=rdir(1),r=(D.r||120)+90;e.x=D.x+o.x*r;e.y=D.y+o.y*r;e.z=D.z+o.z*r;faceInstant(e,o.x,o.y,o.z)}
  else{const g=pick(GATES[W.sid]);e.x=g.x*.93;e.y=g.y*.93;e.z=g.z*.93;faceInstant(e,-e.x,-e.y,-e.z)}
  W.ents.push(e);if(e.load.drone)deployDrones(e);return e}
function mrLive(initial){if(!W||NET.cl)return;const R=S.mrs||{};for(const key in R){const ro=R[key];if(ro.sid!==W.sid)continue;const st=mrSite(key);if(!mrOn(st)||st.owner!==ro.f)continue;
  for(const m of ro.m){if(m.live)continue;if(!initial&&S.T<m.next)continue;if(W.ents.filter(e=>e.npc&&e.role!=='drone').length>=popCap())return;mrSpawn(st,ro,m,initial)}}}
// a miner whose ship left the world some other way (a lost entity) is docked again rather than stuck out
const MR_KIT=new Set(['plate','wire','drone']);
function mrMend(){const R=S.mrs||{};for(const key in R){const ro=R[key];for(const m of ro.m)if(!m.live){let h=null;for(const k in m.load||{})if(!MR_KIT.has(k)){const st=mrSite(key);h=h||(st&&(st.R?storeOf(st.R):st.o.stock))||S.econ.stock[ro.f]||S.econ.stock.pirate;inv.add(h,k,inv.take(m.load,k,m.load[k]))}}
  for(const m of ro.m)if(m.live){const w=WORLDS[ro.sid];if(!w||!w.ents.some(e=>e.alive&&e.mrKey===key&&String(e.mrId)===String(m.id))){m.live=false;m.next=S.T+MR.turn[0]}}}}
{const o=strategicTick;strategicTick=function(){try{mrMend()}catch(e){console.error(e)}return o.apply(this,arguments)}}
// no chance-spawned miners: the rosters are the miners
{const o=popWants;popWants=function(){return o.apply(this,arguments).filter(w=>w[0]!=='miner')}}
{const o=populateAll;populateAll=function(){try{if(!S.mrInit)mrTick();mrLive(true)}catch(e){console.error(e)}return o.apply(this,arguments)}}
{const o=populate;populate=function(initial){try{mrLive(!!initial)}catch(e){console.error(e)}return o.apply(this,arguments)}}
// what a site's miners are up to, for the station's and outpost's panels
function mrLine(key){const st=mrSite(key);if(!mrOn(st))return'';const ro=mrRoster(key),n=ro&&ro.f===st.owner?ro.m.length:0,want=mrTarget(st),out=ro?ro.m.filter(m=>m.live).length:0;
  return`Miners ${n}/${want}${out?` (${out} out)`:''} · mining at ${Math.round(mrWork(key)*100)}%${n<want&&ro?` · next built in ${Math.max(0,Math.round((ro.t-S.T)/60))} min`:''}`}
{const o=mapSectorNow;mapSectorNow=function(sid){let h=o.apply(this,arguments);try{const keys=[];if(S.stations[sid])keys.push('S.'+sid);const oid=OUT_BY_SECTOR[sid];if(oid)keys.push('O.'+oid);for(const k of keys){const L=mrLine(k);if(L){const i=L.indexOf(' · ');h+=`<span>${L.slice(0,i<0?L.length:i).replace(/ \d.*$/,'')}</span><b>${esc(L.replace(/^Miners /,''))}</b>`}}}catch(e){}return h}}
