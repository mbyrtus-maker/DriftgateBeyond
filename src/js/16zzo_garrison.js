//@src 16zzo_garrison.js
// ============================================================ Beyond: garrisons (live space stage 2, 6 Nov 2026)
// Every station, depot and outpost a power or the Brood holds keeps a garrison: fighters with their kits aboard (the patrol
// loadout of the power's tier when built). Live they fly as the system's patrol wing (wings of three; the hive keeps two);
// a ship that breaks off flies home and docks, and launches again with the others once rearmed. Off-screen, when the site
// is attacked, its garrison is what defends it (plus a ship sent from the muster when the power saw it coming), and the
// ships lost in that fight are gone until the garrison is made up from the power's stores. No
// patrol is spawned by chance any more. Three minutes after its last loss, a garrison is made up to full at once (kits allowing).
const GR={n:{core:3,depot:3,hive:4,out:3},wing:3,build:180,retry:60,turn:[40,80],topup:false};   // build: 3 minutes after its last loss the whole garrison is made up at once (user, 6 Nov 2026)   // topup: a short garrison is made up from the muster in a fight off-screen, to the old 3 (home) or 2
function grSites(){const L=[];for(const sid in S.stations){const R=S.stations[sid];if(R&&FACTIONS[R.owner]&&GR.n[R.kind])L.push('S.'+sid)}
  for(const oid in S.outposts){const o=S.outposts[oid];if(o&&FACTIONS[o.owner])L.push('O.'+oid)}return L}
function grSite(key){const id=key.slice(2);if(key[0]==='S'){const R=S.stations[id];return R?{key,kind:R.kind,owner:R.owner,sid:id,R}:null}const o=S.outposts[id];return o?{key,kind:'out',owner:o.owner,sid:o.sector,o}:null}
function grOn(st){return!!st&&!!FACTIONS[st.owner]&&!!GR.n[st.kind]}
// a garrison grows with the site (user, 6 Nov 2026): a home station 3, plus one for each level its defence, armour and hangar
// modules come to (as a depot's level counts them); a depot one more than its level (a forward depot 1); an outpost one more
// than its level; the Brood's hive 4
function grLvl(R){const d=devOf(R);return Math.floor(((d.def||0)+(d.armor||0)+Math.min(3,d.hangar||0))/3)}
function grTarget(st){if(st.o)return 1+(st.o.level||1);const R=st.R;if(!R)return 0;if(R.kind==='core')return 3+grLvl(R);if(R.kind==='depot')return R.fwd?1:1+depotLevel(R);if(R.kind==='hive')return GR.n.hive;return GR.n[R.kind]||0}
function grRoster(key){return(S.gar=S.gar||{})[key]}
function grEntry(key,id){const ro=grRoster(key);return ro&&ro.m.find(m=>String(m.id)===String(id))||null}
// a fighter's kit from the muster first, then the warehouse, at the best tier the stores allow
function grKit(f){const srcs=[S.econ.fleet[f],S.econ.stock[f]].filter(Boolean);let tier=factionTier(f),c=pickFighter('patrol'),ld=loadout('patrol',tier,c);
  if(!haveIn(ld,srcs)){c='interceptor';ld=loadout('patrol',tier,c)}while(!haveIn(ld,srcs)&&tier>1){tier--;ld=loadout('patrol',tier,c)}if(!takeFrom(ld,srcs))return null;return{c,t:tier,load:ld}}
function grTick(){const R=(S.gar=S.gar||{}),keys=grSites(),init=!S.grInit;S.grInit=1;
  for(const key in R){const st=grSite(key),ro=R[key];if(grOn(st)&&ro.f===st.owner)continue;const s=S.sectors[ro.sid];for(const m of ro.m)if(!m.live&&s)toDebris(s,m.load);delete R[key]}
  for(const key of keys){const st=grSite(key);let ro=R[key];if(!ro)ro=R[key]={f:st.owner,sid:st.sid,m:[],t:S.T,nid:1};const want=grTarget(st);
    while(ro.m.length<want&&S.T>=ro.t){const k=grKit(st.owner,st);if(!k){ro.t=S.T+GR.retry;break}ro.m.push({id:ro.nid++,c:k.c,t:k.t,load:k.load,live:false,next:0})}}}
// ships that left the world some other way are docked again; whatever isn't kit goes to the site's store
const GR_KIT=new Set(['plate','wire','coil','lattice','missile','torpedo','drone','swarm','tune']);
function grMend(){const R=S.gar||{};for(const key in R){const ro=R[key];for(const m of ro.m){if(!m.live){for(const k in m.load||{})if(!GR_KIT.has(k)){const st=grSite(key),h=(st&&(st.R?storeOf(st.R):st.o.stock))||S.econ.stock[ro.f]||S.econ.stock.pirate;inv.add(h,k,inv.take(m.load,k,m.load[k]))}continue}
  const w=WORLDS[ro.sid];if(!w||!w.ents.some(e=>e.alive&&e.grKey===key&&String(e.grId)===String(m.id))){m.live=false;m.next=S.T+GR.turn[0]}}}}
{const o=strategicTick;strategicTick=function(){try{grTick();grMend()}catch(e){console.error(e)}return o.apply(this,arguments)}}
{const o=ledger;ledger=function(){const r=o.apply(this,arguments);try{const L=r.L['Fleets in muster'];for(const k in S.gar||{})for(const m of S.gar[k].m){const v=invVec(m.load||{});for(const e of RAWS){L[e]+=v[e];r.tot[e]+=v[e]}}}catch(e){}return r}}
{const o=holderIn;holderIn=function(st,path){if(typeof path==='string'&&path.startsWith('gar:')){const p=path.split(':'),ro=st.gar&&st.gar[p[1]],m=ro&&ro.m.find(x=>String(x.id)===p[2]);if(m)return m.load=m.load||{};
  return ro&&st.econ.fleet[ro.f]||ro&&st.econ.stock[ro.f]||st.econ.stock.pirate}return o.apply(this,arguments)}}
{const o=returnHome;returnHome=function(e){if(e&&e.grKey){const m=grEntry(e.grKey,e.grId);if(m){inv.addAll(m.load,e.load);e.load={};if(invMass(e.cargo)>0){const st=grSite(e.grKey),h=st&&(st.R?storeOf(st.R):st.o.stock)||S.econ.stock[e.side]||S.econ.stock.pirate;inv.addAll(h,e.cargo);e.cargo={}}
  m.live=false;m.next=S.T+rnd(GR.turn[0],GR.turn[1])}}return o.apply(this,arguments)}}
{const o=killShip;killShip=function(e){if(e&&e.grKey&&e.role!=='limpet'){const ro=grRoster(e.grKey);if(ro){const i=ro.m.findIndex(m=>String(m.id)===String(e.grId));if(i>=0)ro.m.splice(i,1);if(ro.m.length<grTarget(grSite(e.grKey)||{}))ro.t=Math.max(ro.t,S.T+GR.build)}e.grKey=null}return o.apply(this,arguments)}}
// a garrison ship that breaks off flies home and docks instead of leaving the system
{const o=npcThink;npcThink=function(e,dt){if(e.grKey&&e.role==='flee'&&!NET.cl){const st=grSite(e.grKey),D=st&&(st.R?W.stationEnt:W.outpostEnt);if(D&&(st.R?D.fac===e.side:D.o.owner===e.side)){e.ai.t-=dt;e.life+=dt;e.boosting=true;const d=steer(e,D.x,D.y,D.z,dt,true);faceTo(e,D,dt);if(d<(D.r||120)+40)despawn(e);return}}return o.apply(this,arguments)}}
// live: the docked ships ready to fly launch together as a wing (wings of three, the hive two of them); when the system
// opens they're already out on patrol
function grSpawnWing(st,ships,initial){const side=st.owner,g={id:'g'+(RID++),side,role:'patrol',members:[],n0:0,fleeing:false,gar:st.key};let lead=null;const D=st.R?W.stationEnt:W.outpostEnt;
  for(const m of ships){const e=makeNPC('patrol',side,m.c,m.t,m.load,`gar:${st.key}:${m.id}`);m.load={};m.live=true;e.grKey=st.key;e.grId=m.id;docFit(e,0);
    if(lead){const o=rdir();e.x=lead.x+o.x*70;e.y=lead.y+o.y*70;e.z=lead.z+o.z*70;qCopy(e.q,lead.q)}
    else if(initial){Object.assign(e,randPos(600*SPACE,2300*SPACE));faceInstant(e,-e.x+rnd(-300,300),-e.y,-e.z+rnd(-300,300))}
    else if(D){const o=rdir(1),r=(D.r||120)+110;e.x=D.x+o.x*r;e.y=D.y+o.y*r;e.z=D.z+o.z*r;faceInstant(e,o.x,o.y,o.z)}
    else{const gt=pick(GATES[W.sid]);e.x=gt.x*.93;e.y=gt.y*.93;e.z=gt.z*.93;faceInstant(e,-e.x,-e.y,-e.z)}
    e.grp=g;e.slot=g.members.length;g.members.push(e);if(!lead)lead=e;W.ents.push(e);if(e.load.drone)deployDrones(e)}
  g.n0=g.members.length;W.groups[g.id]=g;return g}
function grLive(initial){if(!W||NET.cl)return;const R=S.gar||{};for(const key in R){const ro=R[key];if(ro.sid!==W.sid)continue;const st=grSite(key);if(!grOn(st)||st.owner!==ro.f)continue;
  const ready=ro.m.filter(m=>!m.live&&(initial||S.T>=m.next)),docked=ro.m.filter(m=>!m.live).length;if(!ready.length)continue;
  // a wing goes out once at least two are ready (or every docked ship is), never more than the ship cap allows
  if(!initial&&ready.length<Math.min(2,docked))continue;
  for(let i=0;i<ready.length;i+=GR.wing){const room=popCap()-W.ents.filter(e=>e.npc&&e.role!=='drone').length;if(room<=0)return;grSpawnWing(st,ready.slice(i,i+Math.min(GR.wing,room)),initial)}}}
{const o=popWants;popWants=function(){return o.apply(this,arguments).filter(w=>w[0]!=='patrol')}}
{const o=populateAll;populateAll=function(){try{if(!S.grInit)grTick();grLive(true)}catch(e){console.error(e)}return o.apply(this,arguments)}}
{const o=populate;populate=function(initial){try{grLive(!!initial)}catch(e){console.error(e)}return o.apply(this,arguments)}}
// off-screen: the garrison defends its site. grForce moves the docked ships' kits into the defending force (listing each
// ship); grSettle loses each ship with the battle's loss share (its kit falling as debris) and puts the survivors' kits
// back aboard
function grForce(key,force){const ro=grRoster(key),ships=[];if(!ro)return ships;for(const m of ro.m){if(m.live)continue;const kit={...m.load};inv.addAll(force,kit);m.load={};ships.push({m,kit})}return ships}
function grSettle(key,ships,force,lf,s){const ro=grRoster(key);let lost=0;for(const x of ships){const got={};for(const k in x.kit)inv.add(got,k,inv.take(force,k,x.kit[k]));
  if(Math.random()<lf){toDebris(s,got);lost++;if(ro){const i=ro.m.indexOf(x.m);if(i>=0)ro.m.splice(i,1)}}else inv.addAll(x.m.load,got)}
  if(lost&&ro)ro.t=Math.max(ro.t,S.T+GR.build);return lost}
function grLine(key){const st=grSite(key);if(!grOn(st))return'';const ro=grRoster(key),n=ro&&ro.f===st.owner?ro.m.length:0,want=grTarget(st),out=ro?ro.m.filter(m=>m.live).length:0;
  return`${n}/${want}${out?` (${out} out)`:''}${n<want&&ro?` · made up in ${Math.max(0,Math.round((ro.t-S.T)/60))} min`:''}`}
{const o=mapSectorNow;mapSectorNow=function(sid){let h=o.apply(this,arguments);try{const keys=[];if(S.stations[sid])keys.push('S.'+sid);const oid=OUT_BY_SECTOR[sid];if(oid)keys.push('O.'+oid);for(const k of keys){const L=grLine(k);if(L)h+=`<span>Garrison</span><b>${esc(L)}</b>`}}catch(e){}return h}}
