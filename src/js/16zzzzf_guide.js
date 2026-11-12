//@src 16zzzzf_guide.js
// ============================================================ Beyond: the guided start (user, 11 Nov 2026)
// "Stick the onboarding section as an option in the training menu": the top entry of Flight school, "Guided start: your
// first contract", launches a REAL galaxy exactly as Launch does (same callsign, freeport, role and hull) with a guide on
// that pilot (P.guide, saved with the game). Solo pilots and hosts only; a guest joins as a normal pilot.
//   The first contract is five steps. Each shows what to do and why, in the flight HUD (the training panel) and at the top
//   of the dock's Overview, completes from real game events, and is paid by the Freeport Compact's treasury (the wallet
//   every freeport pays from) with a real transfer. A step can be skipped (no pay) and the guide ended at any time.
//     1 Shakedown      fly to a marker 2 km out and dock again                                          150 cr
//     2 First work     combat: guard an independent miner for one short trip in this system
//                      mining: mine 5 t here and sell it at the freeport
//                      hauling: a Freeport request, bought here and delivered to the nearest freeport      400 cr
//     3 First jump     combat: guard a miner to the next system and back (you jump when it jumps)
//                      mining: mine 8 t in the next system and sell it at home
//                      hauling: a Freeport request bought at another freeport and delivered home           700 cr
//     4 First upgrade  buy a part on the Market and fit it (Ship)                    the price you paid for it
//     5 Your choice    take any job from the board                                                         250 cr
//   Where the board has no suitable job the guide makes a real one the way the game does: a guard hire on one of the home
//   freeport's independent miners (16zzzi; one in port, else for step 2 one already mining the system, else a newcomer
//   with its 1,500 cr stake from the Compact, once a guide), a Freeport request (S.contracts). Nothing is made from nothing: the ledger stays exact.
//   Your path: a panel on the Overview while the guide is on, the whole ladder with the pilot's place on it, every figure
//   read from the game's own values.
//   Fewer controls on day one (guided pilots only, gdHide): the intel-work picker until a first scouting job, Build here
//   until a kit or a company, the Black market tabs until Rating 2 or stolen goods, the Company key until the first contract
//   is done. Each appears with a one-line note.
const GD={pay:[150,400,700,0,250],ore:[0,5,8],capT:[0,6,8],near:30,wait:300,mark:2000,markR:220,spend:.6,want:false,clicking:false,dirty:false,acc:0,endAsk:0};
const GD_STEPS=[{k:'shake',name:'Shakedown',teach:'launching, steering and docking'},{k:'work',name:'First work',teach:'your role\'s everyday work'},
  {k:'jump',name:'First jump',teach:'gates, the map and autopilot'},{k:'part',name:'First upgrade',teach:'the Market, parts and the Ship tab'},{k:'choice',name:'Your choice',teach:'the Jobs board'}];
function gdOf(P){const G=P&&P.guide;return G&&G.on&&S&&!S.training&&!S.unb?G:null}
function gdStepOn(P){const G=gdOf(P);return G&&G.i<GD_STEPS.length?G:null}
function gdAtHome(G,P){return P.docked==='station'&&P.sector===G.home}
function gdOre(P){let n=0;for(const k of RAWS)n+=P.cargo[k]||0;return n}
function gdK(id){return`<kbd>${kb(id)}</kbd>`}
function gdStaName(sid){return S.stations[sid]?S.stations[sid].name:DEF[sid]?DEF[sid].name:'the freeport'}
// what the part step pays back at most: what the first three steps paid
function gdPartCap(){return GD.pay[0]+GD.pay[1]+GD.pay[2]}
// ---- starting: the Training menu's top entry launches as Launch does, with the guide wanted
function gdBegin(P){if(!P||P.guide||!S||S.training||S.unb||P.sworn||NET.cl)return false;let role=typeof roleOf==='function'?roleOf(P.cls):'combat';if(!['combat','mining','hauling'].includes(role))role='combat';
  P.guide={v:1,on:1,i:0,role,home:P.home||P.sector,paid:[],skip:[],sv:{},note:{},T0:S.T};
  feed(`Guided start: your first contract is five paid steps for ${gdStaName(P.guide.home)}. The step is at the top left in flight and at the top of the Overview when docked; skip a step or end the guide whenever you like.`,'good');return true}
function gdLaunch(){$('trPick').hidden=true;if(selFac==='pirate'||testSworn()){$('ssum').innerHTML='<b style="color:var(--amber)">The guided start is for independent contractors: pick a freeport first.</b>';return}
  GD.want=true;GD.clicking=true;try{$('bLaunch').click()}finally{GD.clicking=false}
  // a launch that was refused (no callsign yet) leaves nothing pending
  if(!(S&&S.player&&running)&&!MP.autoLaunch&&!NET.on)GD.want=false}
{const o=startWith;startWith=function(state){const r=o.apply(this,arguments);try{if(GD.want&&!NET.on){GD.want=false;gdBegin(S.player)}}catch(e){console.error(e)}return r}}
{const o=trainStart;trainStart=function(track){if(track==='guided'){gdLaunch();return}return o.apply(this,arguments)}}
{const o=trPickHtml;trPickHtml=function(){const h=o.apply(this,arguments),b=`<button class="btn pri" type="button" data-trk="guided" style="text-align:left;white-space:normal;margin:8px 0 12px;width:100%" title="Launches a real galaxy, as Launch does, with a guide on your pilot"><b>Guided start: your first contract</b><br><span style="font-size:12px;letter-spacing:0;text-transform:none;font-weight:400">A real galaxy, not practice: five paid steps from your freeport teach launching and docking, your role's work, your first jump, your first part and the Jobs board.${NET.cl?' (Solo pilots and hosts: as a guest you join normally.)':''}</span></button>`;
  return h.includes('<p>')?h.replace('<p>',b+'<p>'):b+h}}
// the Launch button pressed by hand is never a guided start
document.addEventListener('click',e=>{try{if(e.target&&e.target.id==='bLaunch'&&!GD.clicking)GD.want=false}catch(err){}},true);
// ---- pay, moving on, skipping, ending
function gdPay(P,n){return n>0?payKey(pkeyOf(P),'neutral',n):0}
function gdDone(G,P,payN,extra){const i=G.i,st=GD_STEPS[i],want=payN==null?GD.pay[i]:payN;gdRelease(G,P);const got=gdPay(P,want);G.paid[i]=got;
  const msg=`✔ Guided start ${i+1}/${GD_STEPS.length} · ${st.name} done${got?`: +${fmt(got)} cr from the Freeport Compact`:''}${want>got?' (its treasury could spare no more)':''}.${extra?' '+extra:''}`;
  feed(msg,'good');flash(msg);try{SFX.count&&SFX.count(true)}catch(e){}gdNext(G,P)}
function gdNext(G,P){G.i++;G.sv={};GD.dirty=true;if(G.i>=GD_STEPS.length){G.done=S.T;const tot=G.paid.reduce((a,b)=>a+(b||0),0);
  feed(`★ Your first contract is complete: ${fmt(tot)} cr paid by the Freeport Compact in all. Your path, on the Overview, shows what comes next.`,'good')}}
function gdSkip(P){const G=gdStepOn(P);if(!G)return;const i=G.i;gdRelease(G,P);G.skip[i]=1;G.paid[i]=0;feed(`Guided start: ${GD_STEPS[i].name} skipped. A skipped step pays nothing.`,'warn');gdNext(G,P)}
function gdEnd(P){const G=gdOf(P);if(!G)return;gdRelease(G,P);G.on=0;G.ended=S.T;GD.dirty=true;try{cmSig.s=''}catch(e){}
  feed('Guided start ended. Every control is back, and the Overview shows a next step as it does for any pilot.','info')}
// what a step holds for itself is let go when it ends: the miner's hire, the request's reservation
function gdRelease(G,P){try{const I=G.sv.mid!=null?indById(G.sv.mid):null;if(I&&I.hire&&I.hire.gd){if(I.run&&I.run.capT)delete I.run.capT;I.guard=null;I.hire=null}
  const k=G.sv.kid!=null?(S.contracts||[]).find(x=>x.id===G.sv.kid):null;if(k&&k.ind==='gd')k.ind=null}catch(e){console.error(e)}}
// ---- step 1: the shakedown marker, 2 km from the freeport on the clearest of twelve bearings
function gdMarker(G){if(G.sv.m)return G.sv.m;if(!W||W.sid!==G.home)return null;const SE=W.stationEnt,s=S.sectors[W.sid];if(!SE||!s)return null;let best=null,bs=-1;
  for(let i=0;i<12;i++){const a=i/12*TAU,q={x:SE.x+Math.cos(a)*GD.mark,y:SE.y,z:SE.z+Math.sin(a)*GD.mark};let c=1e9;for(const r of s.ast)c=Math.min(c,d3(r,q)-astR(r));for(const g of GATES[W.sid]||[])c=Math.min(c,d3(g,q));if(c>bs){bs=c;best=q}}
  G.sv.m={x:Math.round(best.x),y:Math.round(best.y),z:Math.round(best.z)};return G.sv.m}
function gdRunShake(G,P){const v=G.sv;if(P.docked){if(v.hit&&gdAtHome(G,P))gdDone(G,P);return}if(!W||!W.player||W.sid!==G.home)return;
  const m=gdMarker(G);if(m&&!v.hit&&d3(W.player,m)<GD.markR){v.hit=1;flash('Marker reached. Now back to the freeport.');try{SFX.count&&SFX.count(true)}catch(e){}}}
function gdMarkDraw(){const P=S&&S.player,G=P&&gdStepOn(P);if(!G||G.i!==0||G.sv.hit||!W||!W.player||P.docked||W.dead||W.sid!==G.home||W.bridge||W.gunseat)return;const m=gdMarker(G);if(!m)return;
  const c=octx,Q=proj(m.x,m.y,m.z),d=Math.round(d3(m,W.player)/10)*10;
  if(!Q.behind&&Q.x>20&&Q.y>20&&Q.x<VW-20&&Q.y<VH-20){const r=Math.max(12,projR(Q.d,GD.markR)),x=Q.x,y=Q.y;c.save();c.strokeStyle='#f0b24a';c.lineWidth=1.5;c.setLineDash([7,5]);c.beginPath();c.arc(x,y,r,0,TAU);c.stroke();c.setLineDash([]);
    c.textAlign='center';c.fillStyle='#f0b24a';c.fillText('SHAKEDOWN MARKER',x,y+r+16);c.fillStyle='rgba(140,145,165,.9)';c.fillText(fmt(d)+' m',x,y+r+30);c.restore()}
  else edgeMark(Q,'Shakedown marker  '+fmt(d)+' m','#f0b24a')}
{const o=drawOverlay;drawOverlay=function(){const r=o.apply(this,arguments);try{gdMarkDraw()}catch(e){}return r}}
// ---- mining: ore that comes aboard in flight is counted (step 3: only outside the home system); a sale at home ends it
function gdMineTrack(G,P,away){const v=G.sv,n=gdOre(P);if(P.docked||v.last==null){v.last=n;return}if(n>v.last&&(!away||P.sector!==G.home))v.got=(v.got||0)+n-v.last;v.last=n}
function gdOreAll(P){let n=gdOre(P);for(const k of RAWS)n+=(P.vault||{})[k]||0;return n}
function gdRunMine(G,P){gdMineTrack(G,P,G.i===2);
  // the ore lost before it was sold (shot down, jettisoned, sold elsewhere): it has to be mined again
  if((G.sv.got||0)>=GD.ore[G.i]&&!G.sv.sold&&gdOreAll(P)<=0){G.sv.got=0;G.sv.why='That ore is gone before it was sold at home: mine it again.'}else if(G.sv.why&&(G.sv.got||0)>0)G.sv.why='';if(G.i===2&&P.sector!==G.home)G.sv.out=1;if(G.i===2&&!G.sv.to)G.sv.to=gdNextSys(G);if(G.sv.sold>0)gdDone(G,P)}
// the system next door to work in: one with rock, not the Brood's, the gate open, the safest first
function gdNextSys(G){const N=(NEIGH[G.home]||[]).filter(s=>!broodHeld(s)&&!S.gateDown[gateKey(G.home,s)]),L=N.map(s=>({s,o:indOreIn(s),d:indDanger(s)})).filter(x=>x.o>=60).sort((a,b)=>a.d-b.d||b.o-a.o);
  return L.length?L[0].s:N[0]||(NEIGH[G.home]||[])[0]||null}
// ---- combat: a guard hire on an independent miner of the home freeport, as miners post them (16zzzi), paid by the Compact
function gdMiner(G){return G.sv.mid!=null?indById(G.sv.mid):null}
function gdMinerLoad(I){const w=I.live&&WORLDS[I.sector],e=w&&w.ents.find(x=>x.alive&&x.indId===I.id);return invMass(e?e.cargo:I.hold)}
function gdGuardPost(G,P,to){const me=pkeyOf(P),local=to===G.home,free=x=>x.role==='miner'&&x.sector===G.home&&x.port===G.home&&!x.hire&&!x.guard;let I=indAll().find(x=>free(x)&&x.st==='dock'),out=false;
  // none in port: for the trip in this system, a miner already at work on its rocks will do (its trip is cut short only
  // once the job is taken)
  if(!I&&local){I=indAll().find(x=>free(x)&&x.st==='work'&&x.run&&x.run.k==='mine'&&!x.run.c);out=!!I}
  // still none: the Compact stakes a newcomer, as it does every independent (once a guide, and only below the port's cap)
  if(!I&&!G.made&&indAll().filter(x=>indAlive(x)&&x.port===G.home).length<IND.cap){I=indNew(G.home,'miner');if(I){G.made=1;feed(`${I.name}, an independent miner, has set up at ${gdStaName(G.home)}.`,'info')}}
  if(!I)return null;
  // the trip is the Compact's idea, so the Compact pays for the guard: nothing comes out of the miner's purse (cap 0)
  I.hire={to,x:{},capT:GD.capT[G.i],T0:S.T,why:local?'out to the rocks of this system':(igWhy(I,to)||'to the next system'),cap:0,T:S.T,st:out?'out':'wait',gd:me,gn:0,gj:0,ls:I.sector,fee:GD.pay[G.i]};
  G.sv.mid=I.id;G.sv.why='';G.sv.lapsed=0;feed(`📋 ${I.name} wants a guard ${out?'while it mines here':`for a short trip ${I.hire.why}`}: the Freeport Compact pays ${fmt(GD.pay[G.i])} cr (Jobs).`,'info');GD.dirty=true;return I}
function gdRunGuard(G,P,d){const v=G.sv,me=pkeyOf(P);if(v.to==null)v.to=G.i===1?G.home:gdNextSys(G);let I=gdMiner(G);
  if(I&&(I.st==='down'||!I.hire||I.hire.gd!==me)){v.mid=null;I=null}
  if(!I){if(P.sector===G.home&&v.to&&!v.lapsed)gdGuardPost(G,P,v.to);return}
  const H=I.hire,mine=I.guard&&sameK(I.guard.k,me);
  if(!mine){
    // the miner waits for its guard while the pilot is in the system; the pilot gone, it goes back to its own plans
    // (five minutes at most: after that it is let go, and the job is posted again when the pilot next uses the dock)
    if(I.guard){return}if(P.sector!==G.home||(H.st==='wait'&&S.T-(H.T0||0)>GD.wait)){I.hire=null;v.mid=null;v.lapsed=P.sector===G.home?1:0}else if(H.st==='wait')H.T=S.T;return}
  if(H.ls!==I.sector){if(H.ls&&(P.sector===H.ls||P.sector===I.sector))H.gj=(H.gj||0)+1;H.ls=I.sector}
  if(I.sector!==P.sector&&P.route!==I.sector&&!P.docked)P.route=I.sector;
  // time near it counts wherever it is out in the system it works (mining, or running from raiders with its guard)
  if(I.st!=='dock'&&I.live&&I.sector===H.to&&!P.docked&&W&&W.player&&W.sid===I.sector){const e=W.ents.find(x=>x.alive&&x.indId===I.id);if(e&&d3(W.player,e)<IGD.reach)H.gn=(H.gn||0)+d}}
// the trip is over (the miner docked, or was lost): the Compact pays if the guard was there for it
function gdGuardEnd(I,H,was,ok){const P=xPilotOfKey(H.gd),G=P&&gdStepOn(P);if(!G||G.sv.mid!==I.id)return;const away=H.to!==G.home,me=was&&sameK(was.k,H.gd);G.sv.mid=null;
  if(!was){GD.dirty=true;return}
  if(ok&&me&&(H.gn||0)>=GD.near&&(!away||(H.gj||0)>=1)){gdDone(G,P);return}
  G.sv.why=!ok?`The guard job for ${I.name} ended early. Another is being posted.`:!me?`${I.name} made its trip without you. The job is posted again.`:`${I.name} finished its trip, but you were not with it for long enough: stay within ${(IGD.reach/1000).toFixed(1)} km of it out there${away?', and jump when it jumps':''}. The job is posted again.`;
  keyFeed(H.gd,G.sv.why,'warn');GD.dirty=true}
{const o=igEnd;igEnd=function(I,why){const H=I&&I.hire;if(!H||!H.gd)return o.apply(this,arguments);const was=I.guard;
  // its own purse paid something (a trip into deep space): the miner's usual sign-off; otherwise only the guide speaks
  if(was&&was.paid>0)o.apply(this,arguments);else{if(why&&was)keyFeed(was.k,why,'bad');I.guard=null;I.hire=null}
  try{gdGuardEnd(I,H,was,!why)}catch(e){console.error(e)}}}
{const o=igPay;igPay=function(I,n,what){if(I&&I.hire&&I.hire.gd&&!(I.hire.cap>0))return;return o.apply(this,arguments)}}
// a guide's trip is a short one: the miner turns for home with capT tonnes aboard (live, and out of sight)
function gdTripFull(I,load){const r=I&&I.run;return!!(r&&r.capT&&r.k==='mine'&&I.st==='work'&&load>=r.capT)}
{const o=npcThink;npcThink=function(e,dt){try{if(e.indId&&!e.pjRun&&!NET.cl){const I=indById(e.indId);if(I&&gdTripFull(I,invMass(e.cargo))){inv.addAll(I.hold,e.cargo);e.cargo={};indMineDone(I);inv.addAll(e.cargo,I.hold);I.hold={};I.live=true;return}}}catch(err){console.error(err)}return o.apply(this,arguments)}}
{const o=indMineOff;indMineOff=function(I){if(gdTripFull(I,invMass(I.hold))){indMineDone(I);return}return o.apply(this,arguments)}}
// the Jobs board: the guide's guard job reads as the Compact's, with its flat fee; nobody else is offered it
{const o=jobsList;jobsList=function(c,P){let out=o.apply(this,arguments);try{const me=pkeyOf(P);out=out.filter(j=>{if(!String(j.id).startsWith('igd:'))return true;const I=indById(String(j.id).slice(4)),H=I&&I.hire;if(!H||!H.gd)return true;if(!sameK(H.gd,me))return false;
    const mine=I.guard&&sameK(I.guard.k,me),local=H.to===I.port,fee=H.fee||0;j.by='neutral';j.payN=fee;j.pay=`${fmt(fee)} cr`;
    j.sub=mine?`your job · the Compact pays ${fmt(fee)} cr when it docks again`:`a short trip ${esc(H.why)} · ${H.st==='wait'?'waiting at':'mining in'} ${esc(DEF[I.sector].name)} · guided start`;
    j.detail=()=>`<p class="note" style="margin:0">${esc(I.name)}, an independent miner, is making a short trip ${esc(H.why)} to mine ${esc(DEF[H.to].name)}, and the Freeport Compact is paying for a guard: ${fmt(fee)} cr when it docks again, if you stayed within ${(IGD.reach/1000).toFixed(1)} km of it for ${GD.near} s while it was out there${local?'':' and made a jump with it'}.${H.cap>0?` Its own purse adds ${IGD.jump} cr a jump and ${IGD.min} cr a minute, up to ${fmt(H.cap)} cr.`:''} Target it and press ${kb('autopilot')} to fly in formation${local?'':': you jump when it jumps'}.</p>`;return true})}catch(e){console.error(e)}return out}}
{const o=myJobRows;myJobRows=function(){let h=o.apply(this,arguments);try{const P=S.player,G=P&&gdStepOn(P),I=G&&gdMiner(G);if(I&&I.hire&&I.hire.gd&&!(I.hire.cap>0))h=h.replace('paid 0 of 0 cr',`${fmt(I.hire.fee||0)} cr when it docks`)}catch(e){}return h}}
// ---- hauling: a Freeport request the pilot can fill from the dock it is at; one already posted, or a new one posted as the
// freeports post theirs (it carries nothing until it is delivered; the Compact pays on delivery, as for any request)
function gdPorts(){return FREEPORTS.map(F=>F.sid).filter(s=>S.stations[s]&&S.stations[s].owner==='neutral')}
function gdNearPort(from,not){const L=gdPorts().filter(s=>s!==not&&s!==from&&HOP[from]&&HOP[from][s]!=null).sort((a,b)=>HOP[from][a]-HOP[from][b]);return L[0]||null}
// the freeport to load at for the run home: the one the pilot is at, else the nearest other than home
function gdPortFrom(P,G){const hop=s=>s===P.sector?0:(HOP[P.sector]&&HOP[P.sector][s]!=null?HOP[P.sector][s]:99);return gdPorts().filter(s=>s!==G.home).sort((a,b)=>hop(a)-hop(b))[0]||null}
function gdContract(G){return G.sv.kid!=null?(S.contracts||[]).find(x=>x.id===G.sv.kid)||null:null}
function gdKn(G){const k=gdContract(G);return k?k.n:0}
function gdReq(G,P,to){let c;try{c=dockCtx()}catch(e){return null}if(!c||!c.market||!W||!W.player)return null;const free=Math.max(0,W.player.st.cargo-invMass(P.cargo)),purse=P.credits*GD.spend;
  const can=(i,n)=>n>0&&(c.market[i]||0)>=n&&n*mass(i)<=free&&n*mBuy(c,i)<=purse;
  let k=(S.contracts||[]).find(x=>x.fac==='neutral'&&x.st===to&&!x.blk&&!x.ind&&ITEMS[x.item]&&x.n>0&&x.until>S.T+1200&&can(x.item,x.n));
  if(!k){const L=['plate','wire','coil','lattice','ir','cu','fe','xc'].filter(i=>ITEMS[i]&&!S.contracts.some(x=>x.st===to&&x.item===i)).map(i=>({i,n:Math.min(6,c.market[i]||0,Math.floor(free/Math.max(1,mass(i))),Math.floor(purse/Math.max(1,mBuy(c,i))))})).filter(x=>x.n>=2);
    // made goods before ore, and a load of four or more before a smaller one
    if(!L.length)return null;const{i,n}=L.find(x=>x.n>=4)||L[0],reward=Math.ceil(baseValue(i)*n*3/10)*10;k={id:S.nextId++,fac:'neutral',st:to,item:i,n,n0:n,reward,until:S.T+3600};S.contracts.push(k);
    feed(`📦 Freeport request · ${gdStaName(to)}: ${n} ${ITEMS[i].name} for ${fmt(reward)} cr. Deliver there in person.`,'info')}
  k.ind='gd';G.sv.kid=k.id;G.sv.item=null;GD.dirty=true;return k}
function gdRunHaul(G,P){const v=G.sv;if(v.deliv){gdDone(G,P);return}
  if(G.i===1){v.from=G.home;if(!v.to)v.to=gdNearPort(G.home,G.home)}
  else{v.to=G.home;if(!v.from||v.from===G.home)v.from=gdPortFrom(P,G)}
  if(!v.to||!v.from)return;let k=gdContract(G);
  if(!k){
    // the request ran out or was filled with the goods already aboard: it is posted again for what the pilot carries
    if(v.item&&(P.cargo[v.item]||0)>0&&P.sector!==v.to){const n=P.cargo[v.item],reward=Math.ceil(baseValue(v.item)*n*3/10)*10;k={id:S.nextId++,fac:'neutral',st:v.to,item:v.item,n,n0:n,reward,until:S.T+3600,ind:'gd'};S.contracts.push(k);v.kid=k.id}
    else{v.kid=null;v.item=null;if(P.docked==='station'&&P.sector===v.from)k=gdReq(G,P,v.to)}}
  if(k&&!v.item&&fpDeliverable(P,k,[P.cargo])>=jobMin(k))v.item=k.item}
// ---- step 5: any job taken that the pilot wasn't already on
function gdJobSig(P){const me=pkeyOf(P),L=[];try{if(JTRACK)L.push('t:'+JTRACK.id);if(P.job&&P.job.id)L.push('t:'+P.job.id);
  for(const j of(typeof mfjAll==='function'?mfjAll():[]))if(j.st==='taken'&&sameK(j.pk,me))L.push('mf:'+j.id);
  for(const t of S.traders||[])if(t.esc&&sameK(t.esc.k,me))L.push('ce:'+t.id);
  for(const I of indAll())if(I.guard&&sameK(I.guard.k,me))L.push('ig:'+I.id);
  if(P.run)L.push('run:'+P.run.to+':'+P.run.item);
  for(const x of(typeof bmoAll==='function'?bmoAll():[]))if(x.taker&&bmoKeyOk(x.taker,P))L.push('bmo:'+x.id)}catch(e){}return L}
function gdRunChoice(G,P){const v=G.sv,L=gdJobSig(P);if(!v.j0){v.j0=L;return}const got=L.find(x=>!v.j0.includes(x));if(got)gdDone(G,P);else v.j0=v.j0.filter(x=>L.includes(x))}
// ---- the clock (host and solo): the current step's own check, and the controls that have just appeared
function gdWantCheck(){if(!GD.want||!S||!S.player||!running)return;GD.want=false;if(NET.cl)feed('The guided start is for solo pilots and hosts for now: you have joined as a normal pilot.','info');else gdBegin(S.player)}
function gdTick(dt){gdWantCheck();if(NET.cl||!S||!S.player)return;const P=S.player;
  const G=gdOf(P);if(!G)return;GD.acc+=dt;if(GD.acc<.25)return;const d=GD.acc;GD.acc=0;
  if(G.i<GD_STEPS.length){const k=GD_STEPS[G.i].k;
    if(k==='shake')gdRunShake(G,P);else if(k==='part'){}else if(k==='choice')gdRunChoice(G,P);
    else if(G.role==='mining')gdRunMine(G,P);else if(G.role==='hauling')gdRunHaul(G,P);else gdRunGuard(G,P,d)}
  if(!G.note.intel){const J=P.job;if((J&&J.kind==='scout')||(JTRACK&&JTRACK.ty==='scout')||P.intelFor)gdNote(G,'intel')}
  for(const k of['build','bm','co'])if(!G.note[k]&&!gdHide(k))gdNote(G,k)}
{const o=step;step=function(dt){const r=o.apply(this,arguments);try{gdTick(dt)}catch(e){console.error(e)}return r}}
// ---- what a dock action did: sales, deliveries, parts bought and fitted
function gdActed(G,P,act,arg,pre){const v=G.sv,i=G.i;if(i>=GD_STEPS.length)return;const k=GD_STEPS[i].k,ok=typeof dockErr==='string'&&dockErr.startsWith('✓'),me=pkeyOf(P);
  if(act==='igtake'){const I=indById(arg);if(I&&I.hire&&I.hire.gd&&I.guard&&sameK(I.guard.k,me)){I.hire.ls=I.sector;if(I.st!=='dock'&&I.run&&I.run.k==='mine')I.run.capT=gdMinerLoad(I)+I.hire.capT;else I.hire.x.capT=I.hire.capT;dockErr=`✓ You're guarding ${I.name}: the Freeport Compact pays ${fmt(I.hire.fee||0)} cr when it docks again. Launch (${kb('act')}): it is targeted for you, and ${kb('autopilot')} flies you in formation with it.`}}
  if(G.role==='mining'&&(k==='work'||k==='jump')){const sold=pre.ore-gdOreAll(P);if(sold>0&&P.credits>pre.cr&&gdAtHome(G,P)&&(v.got||0)>=GD.ore[i])v.sold=(v.sold||0)+sold}
  if(G.role==='hauling'&&(k==='work'||k==='jump')&&act==='deliver'&&v.kid!=null&&arg===String(v.kid)&&gdKn(G)<pre.kn)v.deliv=1;
  if(k!=='part')return;
  if(act==='buy'){const it=arg.split(':')[0],I=ITEMS[it],n=ownedOf(P,it)-pre.own;if(I&&(I.part||I.sys)&&n>0&&pre.cr>P.credits)(v.px=v.px||{})[it]=Math.round((pre.cr-P.credits)/n);return}
  if(!ok)return;
  if(act==='fit'||act==='sysfit'){const it=arg.split(':')[act==='fit'?2:1];if(!it||!ITEMS[it]||!/fitted|installed/.test(dockErr))return;const px=(v.px||{})[it]||0;
    gdDone(G,P,Math.min(px,gdPartCap()),px?`That is the ${fmt(px)} cr the ${ITEMS[it].name} cost you.`:`Nothing to pay back: you already owned the ${ITEMS[it].name}.`)}
  else if(act==='upg'||act==='pup')gdDone(G,P,Math.min(Math.max(0,pre.cr-P.credits),gdPartCap()),'That is the workshop fee back.')}
{const o=dockAction;dockAction=function(act,arg){const P=S&&S.player,G=P&&!NET.cl?gdOf(P):null;if(!G)return o.apply(this,arguments);
  const a=String(arg==null?'':arg),pre={cr:P.credits,ore:gdOreAll(P),kn:gdKn(G),own:act==='buy'?ownedOf(P,a.split(':')[0]):0};const r=o.apply(this,arguments);try{gdActed(G,P,act,a,pre)}catch(e){console.error(e)}return r}}
// ---- fewer controls on day one: hidden for a guided pilot until its condition, then shown with a note
function gdBuildOK(P){try{return coReady(P)||KIT_IDS.some(k=>ownedOf(P,k)>0)}catch(e){return true}}
function gdBmOK(P){try{if(ratingOf(P)>=2)return true;stolSync(P);return Object.keys(P.stol||{}).length>0}catch(e){return true}}
let GD_C={P:null,t:-1e9,build:true,bm:true};
function gdCond(P){const t=performance.now();if(GD_C.P!==P||t-GD_C.t>1000)GD_C={P,t,build:gdBuildOK(P),bm:gdBmOK(P)};return GD_C}
function gdHide(k){const P=S&&S.player,G=P&&gdOf(P);if(!G)return false;
  if(k==='co')return G.i<GD_STEPS.length;if(k==='intel')return!G.note.intel;if(k==='build')return!gdCond(P).build;if(k==='bm')return!gdCond(P).bm;return false}
const GD_NOTES={intel:()=>'New on the Jobs board: "Intel work for" picks the power your beacon flips, limpets and scans are done for.',
  build:()=>`New in the quick keys: ${kb('op')} opens Build here (a Lair, a Depot or a Station from a kit in your hold).`,
  bm:()=>'New at the dock: the Black market tab (Jobs) has runs and contracts the powers would rather not see.',
  co:()=>`New in the top bar: Company (${kb('company')}) is where a company of your own, its bases and crews are run.`};
function gdNote(G,k){G.note[k]=1;try{cmSig.s=''}catch(e){}GD.dirty=true;const m=GD_NOTES[k]();feed(m,'info');flash(m)}
{const o=intelBarHtml;intelBarHtml=function(c,P){if(gdHide('intel'))return'';return o.apply(this,arguments)}}
{const o=toggleCompany;toggleCompany=function(){const el=$('company');if(gdHide('co')&&el&&el.hidden){flash('The Company screen opens when your first contract is done (or end the guide).');return}return o.apply(this,arguments)}}
{const o=ctrBuildMenu;ctrBuildMenu=function(){if(gdHide('build')){flash('Building opens once you own a kit or have a company.');return}return o.apply(this,arguments)}}
// ---- the step, in words: what to do now (one thing, with its key), why, and a button for the dock
// getting docked at the station in a system, one move at a time
function gdGoDock(P,sid){const name=gdStaName(sid);
  if(P.sector!==sid){if(P.route!==sid)return`Open the galaxy map (${gdK('map')}), click <b>${esc(DEF[sid].name)}</b> and press <b>Set course</b>.`;
    if(P.docked)return`Press ${gdK('act')} to launch: your course to ${esc(DEF[sid].name)} is set.`;return`Press ${gdK('autopilot')}: autopilot flies your course gate by gate to ${esc(DEF[sid].name)}.`}
  if(P.docked)return`Press ${gdK('act')} to launch.`;const SE=W&&W.stationEnt,p=W&&W.player,d=SE&&p?d3(SE,p):1e9;
  if(d<420)return`Press ${gdK('act')} to dock at ${esc(name)}.`;if(W&&W.tgt&&W.tgt.kind==='station')return`Press ${gdK('autopilot')}: autopilot flies you to ${esc(name)}.`;return`Press ${gdK('cycle')} until ${esc(name)} is targeted.`}
function gdMineHint(G,P){const v=G.sv,need=GD.ore[G.i],got=Math.min(need,v.got||0),s=W&&S.sectors[W.sid],me=blKey(P),tool=mtoolOf(P),prog=` <span class="mass">${got} of ${need} t</span>`;if(!s)return'';
  if((s.clouds||[]).some(c=>c.o===me&&oreTotal(c)>0))return`Fly through the chunks to scoop them.${prog}`;
  if((s.charges||[]).some(c=>c.o===me))return`Back off ${BL.blastR} m and press ${gdK('det')} to detonate.`;
  if(!(W.tgt&&W.tgt.kind==='ast'))return`Press ${gdK('ast')} to target the nearest rock.${prog}`;
  if(tool==='mlaser')return`Fly within ${LOAD.ml.range} m, point at the rock and hold ${gdK('mine')}: the beam cuts ore into your hold.${prog}`;
  return`Fly within 300 m, put your sight on a fault point until it reads ON POINT, and press ${gdK('mine')} to fire a charge.${prog}`}
// a part on this Market the ship can take and the purse covers: a maker's part for a slot it already uses (as the
// independents choose theirs), else any other part that fits and isn't the one fitted, a maker's and a cheap one first
function gdPartPick(c,P){try{const R=mR(c),F=fitOf(P),kinds=[...new Set([...F.w,...F.u])].filter(k=>k&&k!=='land'&&k!=='claim'),budget=P.credits*GD.spend,cap=gradeCap(P);const id=aipBest(R,kinds,cap,budget,P.cls,0);if(id)return id;
  const ms=mkStock(R),was=k=>ldTarget(P,k).was,L=Object.keys(ms).filter(k=>ms[k]>0&&ITEMS[k]&&ITEMS[k].part&&ITEMS[k].part!=='claim'&&(ITEMS[k].grade||1)<=cap&&mBuy(c,k)<=budget).filter(k=>{const T=ldTarget(P,k);return!!T&&(((T.g==='w'?F.wi:F.ui)||[])[T.i]||PART[T.was])!==k});
  L.sort((a,b)=>((was(a)==='land')-(was(b)==='land'))||(!!ITEMS[b].maker-!!ITEMS[a].maker)||mBuy(c,a)-mBuy(c,b));return L[0]||null}catch(e){return null}}
function gdNow(G,P){const i=G.i,st=GD_STEPS[i];if(!st)return null;const v=G.sv,home=gdStaName(G.home),o={i,name:st.name,pay:GD.pay[i]?`${fmt(GD.pay[i])} cr`:'',d:'',why:'',btn:null},jobsKey=btTab('jobs');
  if(st.k==='shake'){o.why='A shakedown proves the ship, and you: launch, steer out to a marker, come back and dock.';
    if(P.docked&&!v.hit)o.d=`Press ${gdK('act')} to launch.`;
    else if(!v.hit){const m=W&&W.sid===G.home?gdMarker(G):null,p=W&&W.player;o.d=P.sector!==G.home?gdGoDock(P,G.home):`Fly to the <b>shakedown marker</b>${m&&p?`, ${fmt(Math.round(d3(m,p)/10)*10)} m out`:''}: the mouse steers, ${gdK('thrust')} thrusts.`}
    else o.d=gdGoDock(P,G.home)}
  else if(st.k==='part'){o.pay='the price of the part';o.why=`A maker's part does its job better than the stock one it replaces. Buy one, fit it, and the Compact pays back what it cost (up to ${fmt(gdPartCap())} cr).`;
    const got=Object.keys(v.px||{}).filter(it=>ownedOf(P,it)>0);let c=null;try{c=P.docked?dockCtx():null}catch(e){}
    if(!c||!c.market)o.d=P.docked?`This dock has no Market: launch (${gdK('act')}) and fly to ${esc(home)}.`:gdGoDock(P,S.stations[P.sector]&&S.stations[P.sector].owner==='neutral'?P.sector:G.home);
    else if(!got.length){let sug='';const id=gdPartPick(c,P);if(id)sug=` The <b>${esc(ITEMS[id].name)}</b> (${fmt(mBuy(c,id))} cr) would suit this ship.`;
      o.d=`Open <b>Trade → Market</b> (${gdK2(btTab('market'))}), pick <b>Parts</b> and buy one part your ship can fit.${sug}`;o.btn=['tab','market','Open the Market']}
    else{o.d=`Open <b>Ship</b> (${gdK2(btTab('upg'))}): under <b>Your parts</b>, press <b>Fit</b> on the ${esc(ITEMS[got[0]].name)}.`;o.btn=['tab','upg','Open Ship']}}
  else if(st.k==='choice'){o.why='From here the work is yours to choose. The Jobs board lists who is hiring, what it pays and how far it is; work for a power raises your standing with it and your Contractor Rating.';
    if(!P.docked)o.d=gdGoDock(P,S.stations[P.sector]?P.sector:G.home);
    else{o.d=`Open <b>Jobs</b> (${gdK2(jobsKey)}) and take any job: <b>Select job</b>, <b>Take the job</b> or <b>Escort</b> on the one you want.`;let j=null;try{j=nsJob(dockCtx(),P)}catch(e){}o.btn=j?['gdjob',j.id,'Show me a job']:['tab','jobs','Open Jobs']}}
  else if(G.role==='mining'){const need=GD.ore[i],away=i===2,to=v.to;
    o.why=away?'The rich rock is out in deep space next door, and it is yours for the taking. One jump out, fill up, one jump home.':'Every unit of ore in the galaxy comes out of a real rock, and the freeport\'s market buys it: this is a miner\'s day.';
    if(!mtools(P).length)o.d='This step needs a mining tool (a Light Miner carries a charge launcher). Buy a mining ship at Ship → Shipyard, or skip the step.';
    else if((v.got||0)<need){
      if(away&&P.sector===G.home&&to){o.d=P.route!==to?`Open the galaxy map (${gdK('map')}), click <b>${esc(DEF[to].name)}</b> next door and press <b>Set course</b>.`:P.docked?`Press ${gdK('act')} to launch: your course to ${esc(DEF[to].name)} is set.`:`Press ${gdK('autopilot')}: autopilot flies you through the gate marked NEXT JUMP.`}
      else if(P.docked)o.d=`Press ${gdK('act')} to launch.`;else o.d=gdMineHint(G,P)}
    else if(!gdAtHome(G,P))o.d=`You have your ${need} t. ${gdGoDock(P,G.home)}`;
    else{o.d=`Sell your ore: <b>Sell all here</b> below, or <b>Trade → Market</b> (${gdK2(btTab('market'))}).`;o.btn=['sellhold','','Sell all here']}}
  else if(G.role==='hauling'){const k=gdContract(G),away=i===2,from=v.from,to=v.to;
    o.why=away?'A hauler never flies empty: there is always a load wanted at the other end. Bring one home.':`Buy where it is sold, carry it to where it is wanted: a Freeport request pays on delivery${from&&to&&HOP[from]&&HOP[from][to]?`, and the nearest freeport is ${HOP[from][to]} jump${HOP[from][to]===1?'':'s'} away through open space`:''}.`;
    if(!from||!to)o.d='Working out the run…';
    else if(v.item&&k){const have=fpDeliverable(P,k,[P.cargo]);
      if(have<1)o.d=`You have lost the ${esc(ITEMS[k.item].name)}: buy more at any freeport but ${esc(gdStaName(to))}.`;
      else if(P.docked==='station'&&P.sector===to){o.d=`Open <b>Jobs</b> (${gdK2(jobsKey)}) and press <b>Deliver</b> on the request.`;o.btn=['gdjob','k:'+k.id,'Show me the request']}
      else o.d=gdGoDock(P,to)}
    else if(!(P.docked==='station'&&P.sector===from))o.d=gdGoDock(P,from);
    else if(!k)o.d=`Nothing here can be bought for a request you could carry and afford: sell something or skip the step.`;
    else{o.d=`Open <b>Jobs</b> (${gdK2(jobsKey)}), pick <b>Freeport request: ${k.n} ${esc(ITEMS[k.item].name)} to ${esc(gdStaName(to))}</b> and press <b>Buy ${k.n} to hold</b>.`;o.btn=['gdjob','r:'+k.id,'Show me the request']}}
  else{const I=gdMiner(G),H=I&&I.hire,me=pkeyOf(P),mine=!!(H&&I.guard&&sameK(I.guard.k,me)),away=i===2,nm=I?esc(I.name):'';
    o.why=away?'Deep space next door has the rich rock, and the raiders. Fly in formation and you jump when your charge jumps: every escort works this way.':'Guard work is a fighter\'s bread and butter: a miner works easier with guns nearby. This one the Freeport Compact pays for.';
    if(!I)o.d=gdAtHome(G,P)?`No miner is in port at ${esc(home)} yet: the job posts as soon as one docks.`:gdGoDock(P,G.home);
    else if(!mine){if(!gdAtHome(G,P))o.d=gdGoDock(P,G.home);else{o.d=`Open <b>Jobs</b> (${gdK2(jobsKey)}), pick <b>Guard: ${nm}'s ${esc(CLASSES[I.cls].name)}</b> and press <b>Take the job</b>.`;o.btn=['gdjob','igd:'+I.id,'Show me the job']}}
    else if(P.docked)o.d=`Press ${gdK('act')} to launch: ${nm} is on its way.`;
    else if(P.sector!==I.sector)o.d=`${nm} is in ${esc(DEF[I.sector].name)}: press ${gdK('autopilot')} to fly your course there.`;
    else if(I.st==='work'){const gn=Math.floor(H.gn||0),e=W&&W.player?W.ents.find(x=>x.alive&&x.indId===I.id):null,far=e?d3(e,W.player):0;
      o.d=far>IGD.reach&&!W.fmn?`${nm} is mining ${(far/1000).toFixed(1)} km off and is targeted for you: press ${gdK('autopilot')} to fly to it in formation.`:gn>=GD.near?`Long enough: stay with ${nm} until it has docked at ${esc(home)}.`:`Stay within ${(IGD.reach/1000).toFixed(1)} km of ${nm} while it mines. ${gdK('tgtH')} targets anything hostile. <span class="mass">${gn} of ${GD.near} s</span>`}
    else if(W&&W.fmn)o.d=`In formation with ${nm}${away?': you jump when it jumps':''}. Steer or thrust to break off.`;
    else o.d=`${nm} is targeted for you: press ${gdK('autopilot')} to fly in formation with it.`}
  if(v.why)o.d+=`<br><i>${esc(v.why)}</i>`;return o}
function gdK2(k){return`<kbd>${esc(k)}</kbd>`}
// ---- in flight: the step in the training panel
function gdPips(G){return GD_STEPS.map((_,k)=>`<i class="${k<G.i?'d':k===G.i?'c':''}"></i>`).join('')}
function gdHud(){const el=$('train');if(!el||!S||S.training)return;gdWantCheck();const P=S.player,G=P&&running?gdStepOn(P):null,b=$('bCompany');
  if(b){const hide=gdHide('co')?'none':'';if(b.style.display!==hide)b.style.display=hide}
  if(gdHide('build')){const K=$('cKeys');if(K)for(const d of K.children)if(d.textContent===kb('op')+'Build here'||/^.Build here$/.test(d.textContent)){d.remove();break}}
  if(GD.dirty){GD.dirty=false;try{if(P&&P.docked&&!$('dock').hidden)renderDock()}catch(e){}}
  // docked, the step is in the dock itself: the card on the Overview, a strip on every other tab
  if(!G||(P.docked&&!$('dock').hidden)){if(!el.hidden){el.hidden=true;el._g=''}return}
  const n=gdNow(G,P);if(!n){el.hidden=true;return}const ask=performance.now()<GD.endAsk;
  const h=`<div class="trh"><b>Guided start · ${n.i+1}/${GD_STEPS.length} · ${esc(n.name)}</b><button type="button" class="trx" data-gd="min" aria-label="Collapse">${G.min?'+':'–'}</button></div>`
    +(G.min?'':`<div class="trs">${n.d}${n.pay?`<br><span class="mass">Pays ${esc(n.pay)} · ${esc(n.why)}</span>`:''}</div><div class="trp">${gdPips(G)}</div><div class="trb"><button type="button" class="btn sm" data-gd="skip">Skip step</button><button type="button" class="btn sm" data-gd="end">${ask?'Really end the guide?':'End guide'}</button></div>`);
  if(el._g!==h){el._g=h;el.innerHTML=h}el.hidden=false;
  {const tl=$('hTL');if(tl&&innerWidth>640){const y=Math.round(Math.max(118,tl.getBoundingClientRect().bottom+12));if(el._y!==y){el._y=y;el.style.top=y+'px'}}}}
{const o=hudUpdate;hudUpdate=function(){const r=o.apply(this,arguments);try{gdHud()}catch(e){console.error(e)}return r}}
function gdClick(k){const P=S&&S.player;if(!P||!gdOf(P))return;const G=gdOf(P);
  if(k==='min'){G.min=!G.min}else if(k==='skip')gdSkip(P);
  else if(k==='end'){if(performance.now()<GD.endAsk){GD.endAsk=0;gdEnd(P)}else GD.endAsk=performance.now()+4000}
  else if(k==='pathhide')G.hideP=1;else if(k==='pathshow')G.hideP=0;
  const el=$('train');if(el)el._g='';GD.dirty=true}
$('train').addEventListener('click',e=>{const b=e.target.closest('[data-gd]');if(!b||!S||S.training)return;gdClick(b.dataset.gd)});
{const o=openDock;openDock=function(){const r=o.apply(this,arguments);try{const G=gdStepOn(S.player);if(G)G.sv.lapsed=0}catch(e){}return r}}
{const o=dockClick;dockClick=function(act,arg){try{const G=S&&S.player&&gdStepOn(S.player);if(G&&G.sv.lapsed)G.sv.lapsed=0}catch(e){}if(act==='gd'){gdClick(arg);GD.dirty=false;renderDock();return}
  // the Jobs board with this job picked (the board's default for the hull, set on its first drawing after docking, is settled first)
  if(act==='gdjob'){dockTab='jobs';try{jbDefKey=S.player.cls+'|'+jbDockN;jobFilter='all';jobSel=arg}catch(e){}renderDock();return}return o.apply(this,arguments)}}
// ---- your path: the whole ladder, each rung's needs, cost and what it opens, from the game's own values
function gdRecipe(r){return Object.keys(r).map(k=>`${r[k]} ${ITEMS[k].name}`).join(', ')}
function gdKitCost(c,k){let p=0;try{if(c&&c.market&&(c.market[k]||0)>0)p=mBuy(c,k)}catch(e){}return p?`${fmt(p)} cr here`:`about ${fmt(baseValue(k))} cr`}
function gdPath(c,P){const G=P.guide,me=pkeyOf(P),R=[],r=ratingOf(P),hh=CLASSES[KIT_HULL].name,line=(ROLES[G.role]||ROLES.combat).ships,ci=line.indexOf(P.cls),nx=line[ci+1]||line.find(k=>!START_HULLS.includes(k)),
    lairs=lairsOf(P).length,deps=myDepots(P),stas=myStations(P),tot=(G.paid||[]).reduce((a,b)=>a+(b||0),0),stN=CLASSES[P.cls].name;
  R.push({n:'Your first contract',done:G.i>=GD_STEPS.length,need:`Five paid steps for ${esc(gdStaName(G.home))}${G.i<GD_STEPS.length?`: you are on step ${G.i+1}, ${esc(GD_STEPS[G.i].name)}`:''}`,cost:'Nothing',open:`${fmt(GD.pay.reduce((a,b)=>a+b,0))} cr and a part paid for (${fmt(tot)} cr so far); the Company key`});
  R.push({n:'Contractor Rating 2',done:r>=2,need:`${fmt(RATING.need[2])} Rating points (you have ${fmt(Math.floor(P.rp||0))}): ${RATING.k} for each point of standing your work earns with a power, ${RATING.anom} for an anomaly scanned, ${RATING.run} for a black-market run`,cost:'Nothing but the work',
    open:`${hullsAt(2).map(k=>CLASSES[k].name).join(', ')}; grade ${GRADE_RATING.indexOf(2)} parts and systems; the Black market tab`});
  if(!START_HULLS.includes(P.cls))R.push({n:'A better hull',done:true,need:`You fly a ${esc(stN)}`,cost:'',open:nx?`Next in the line: the ${esc(CLASSES[nx].name)}, ${fmt(hullPrice(nx))} cr at Contractor Rating ${HULL_RATING[nx]||1}`:''});
  else if(nx){const s0=shipStats(P.faction,P.cls,baseTiers()),s1=shipStats(P.faction,nx,baseTiers()),D=slotsOf(nx,P.faction);
    R.push({n:`A better hull: the ${esc(CLASSES[nx].name)}`,done:false,need:`Contractor Rating ${HULL_RATING[nx]||1}; a freeport's or a power's home Shipyard (Ship → Shipyard)`,cost:`${fmt(hullPrice(nx))} cr`,
      open:`${D.w.length} weapon and ${D.u.length} utility slots, a ${Math.round(s1.cargo)} t hold and ${Math.round(s1.hull)} hull (your ${esc(stN)}: ${Math.round(s0.cargo)} t, ${Math.round(s0.hull)})`})}
  else R.push({n:'A better hull',done:true,need:`You fly the top of the ${esc((ROLES[G.role]||ROLES.combat).name.toLowerCase())} line`,cost:'',open:''});
  R.push({n:'A company',done:coFunded(P),need:'A profile (Company → Profile): a name, a logo, a base design, a colour and your fees',cost:`${fmt(COP.deposit)} cr, which opens its treasury (it stays yours: deposit and withdraw by hand)`,open:'Depot and Station Kits are sold to companies only; its treasury pays your bases, crews and posted jobs'});
  R.push({n:'A Lair',done:lairs>0,need:`A Lair Kit (${gdRecipe(ITEMS.kit_lair.recipe)}; ${KIT_T.kit_lair} t) in your hold, beside a large rock in a system with no station: ${kb('op')} in flight, Build a Lair here. No company needed`,cost:gdKitCost(c,'kit_lair'),
    open:`A hidden base of your own: a ${LAIR_B.stash[1]} t stash, repairs and rearming (up to ${LAIR_B.max} Lairs)`,
    rule:`Every kit rides only in a ${esc(hh)}'s hold (${fmt(hullPrice(KIT_HULL))} cr, Contractor Rating ${HULL_RATING[KIT_HULL]}). Bought in any other hull it waits in that dock's hangar.`});
  R.push({n:'A Depot',done:deps.length>0,need:`A company, and a Depot Kit (${gdRecipe(ITEMS.kit_depot.recipe)}; ${KIT_T.kit_depot} t) carried in a ${esc(hh)} to a system with no station, outside the powers' home space; or the same kit used on your Lair`,cost:gdKitCost(c,'kit_depot'),
    open:`A market of your own, hired crews (${fmt(DEP.wage)} cr an hour each) and posted jobs. A Depot does not hold its system`});
  R.push({n:'A Station',done:stas.length>0,need:`Your own Depot, and a Station Kit (${gdRecipe(ITEMS.kit_station.recipe)}; ${KIT_T.kit_station} t) carried to it in a ${esc(hh)}`,cost:gdKitCost(c,'kit_station'),
    open:`It holds its system for you, with a hull and shield ${STA.hK} times a Depot's, and up to five buildings (${gdRecipe(STA.bcost)} each): ${Object.values(STA.B).map(b=>b[0].toLowerCase()).join(', ')}`,
    rule:'A Station is upgraded from a Depot: it cannot be built on empty space. Its buildings set its level and are separate from the development modules on the Works tab (storage, production, defence, armour, hangar).'});
  R.push({n:'A faction',done:!!P.decl,need:'A Station of your own, then Declare on the Allegiance tab',cost:'Nothing to declare; lead the galaxy and the three powers turn on you together',open:`Your Stations count toward the galaxy: hold ${VIC_NEED} systems for ${Math.round(WIN_TIME/60)} minutes and it is yours`});
  const cur=R.findIndex(x=>!x.done);R.forEach((x,k)=>{x.cur=k===cur});return R}
function gdPathHtml(c,P){const G=gdOf(P);if(!G)return'';let R;try{R=gdPath(c,P)}catch(e){console.error(e);return''}const cur=R.find(x=>x.cur);
  if(G.hideP)return`<div class="note gdpath" style="margin:0 0 12px">Your path · next: <b>${cur?cur.n:'everything done'}</b> <button class="btn sm" type="button" data-act="gd" data-arg="pathshow">Show your path</button></div>`;
  let h=`<div class="rcard gdpath" style="margin:16px 0 0"><div class="h3" style="margin:0 0 6px;display:flex;justify-content:space-between;align-items:baseline"><span>Your path</span><button class="btn sm" type="button" data-act="gd" data-arg="pathhide">Hide</button></div><div class="tblw"><table class="t"><thead><tr><th></th><th>Rung</th><th>Needs</th><th>Costs</th><th>Opens</th></tr></thead><tbody>`;
  R.forEach((x,k)=>{h+=`<tr data-rung="${k}"${x.cur?' data-cur="1" style="background:rgba(240,178,74,.08)"':''}><td style="width:22px;color:${x.done?'var(--ok,#7ad9a7)':x.cur?'var(--amber,#f0b24a)':'var(--faint,#667)'}">${x.done?'✓':x.cur?'▶':'·'}</td><td><b${x.cur?' style="color:var(--amber,#f0b24a)"':''}>${x.n}</b>${x.cur?'<br><span class="mass" style="margin:0">you are here</span>':''}</td><td>${x.need||''}</td><td>${x.cost||''}</td><td>${x.open||''}</td></tr>`;
    if(x.rule)h+=`<tr><td></td><td colspan="4" class="note" style="margin:0;color:var(--amber,#f0b24a)">${x.rule}</td></tr>`});
  return h+'</tbody></table></div></div>'}
// ---- the dock's Overview: the guide's step first (it takes the Next step card's place), then Your path
{const o=nextStep;nextStep=function(c,P){const G=gdStepOn(P||S.player);if(G){const n=gdNow(G,P||S.player);if(n)return{t:`Guided start: ${n.name}`,d:n.d,act:n.btn?n.btn[0]:'tab',arg:n.btn?n.btn[1]:'home',btn:n.btn?n.btn[2]:'Overview',gd:1}}return o.apply(this,arguments)}}
function gdCardHtml(c,P){const G=gdStepOn(P);if(!G)return'';const n=gdNow(G,P);if(!n)return'';const ask=performance.now()<GD.endAsk;
  return`<div class="gdcard" style="display:flex;gap:14px;align-items:center;flex-wrap:wrap;padding:12px 14px;margin:0 0 14px;border:1px solid var(--amber,#f0b24a);border-left-width:3px;background:rgba(240,178,74,.05)"><span style="flex:1;min-width:260px"><span class="lab" style="margin:0 0 4px;display:block">Guided start · step ${n.i+1} of ${GD_STEPS.length}${n.pay?` · pays ${esc(n.pay)}`:''}</span><b style="font-size:15px">${esc(n.name)}</b><br><span class="gdd">${n.d}</span><br><span class="note" style="margin:0">Why: ${esc(n.why)}</span></span>`
    +`<span style="display:flex;gap:6px;flex-wrap:wrap">${n.btn?`<button class="btn pri" type="button" data-act="${n.btn[0]}" data-arg="${esc(n.btn[1])}">${esc(n.btn[2])}</button>`:''}<button class="btn" type="button" data-act="gd" data-arg="skip">Skip step</button><button class="btn" type="button" data-act="gd" data-arg="end">${ask?'Really end the guide?':'End guide'}</button></span></div>`}
// the dock's other tabs carry the step as a strip above their content
function gdDockBar(){const P=S&&S.player,G=P&&gdStepOn(P),B=$('dBody');if(!G||!B||dockTab==='home'||B.querySelector('.gdbar'))return;const n=gdNow(G,P);if(!n)return;
  B.insertAdjacentHTML('afterbegin',`<div class="gdbar" style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;padding:8px 12px;margin:0 0 12px;border:1px solid var(--amber,#f0b24a);border-left-width:3px;background:rgba(240,178,74,.05)"><span style="flex:1;min-width:240px"><span class="lab" style="margin:0 8px 0 0;display:inline">Guided start ${n.i+1}/${GD_STEPS.length} · ${esc(n.name)}</span>${n.d}</span><button class="btn sm" type="button" data-act="tab" data-arg="home">Overview</button><button class="btn sm" type="button" data-act="gd" data-arg="skip">Skip step</button></div>`)}
{const o=renderDock;renderDock=function(){const r=o.apply(this,arguments);try{gdDockBar()}catch(e){console.error(e)}return r}}
{const o=homeHtml;homeHtml=function(c,P){let h=o.apply(this,arguments);try{const Q=P||S.player,G=gdOf(Q);if(!G)return h;
    if(gdStepOn(Q))h=h.replace(/<div class="nstep"[\s\S]*?<\/div>/,'<div class="empty">Nothing else is waiting here: your guided step is at the top.</div>');
    // the step on top, the usual Overview, then the ladder (hidden, its one line sits under the step instead)
    h=gdCardHtml(c,Q)+(G.hideP?gdPathHtml(c,Q)+h:h+gdPathHtml(c,Q))}catch(e){console.error(e)}return h}}
