//@src 16n_holdings.js
// ============================================================ Lairs and the Company screen (Beyond stage 9)
// A Lair is a contractor's first base: hidden beside a large asteroid in any system with no station. Build one from your hold
// (a Depot Frame and 6 Alloy Plate) near a large rock, with the comms build order or the Company screen's Holdings tab.
// Up to four per pilot; one per pilot per system (several pilots can each hide one in the same system).
//   Level 1: a 200 t stash, repairs and rearming; lie low (heat cools three times as fast while docked there); stolen goods
//            put in the stash lose their stolen tag.
//   Level 2: a 400 t stash, a workshop and forge with no fee.
// A Lair has no guns: it stays hidden until a scout of a power hostile to its owner comes within 5 km; from then on that
// power's ships wear it down whenever they pass close. A destroyed Lair's stash drifts as salvage.
// The Company screen (key 0, or the Company button) opens anywhere: Allegiance and Holdings for now.
const LAIR_B={max:4,rockR:700,rockMin:50,build:60,cost:{frame:1,plate:6},up:{frame:1,plate:10,coil:4},stash:[0,200,400],cool:3,hull:1500,seeR:5000};
function pkeyOf(P){if(!P||P===S.player)return curPid()||'me';return Object.keys(S.pilots||{}).find(k=>S.pilots[k]===P)||'me'}
function lairsOf(P){const k=pkeyOf(P);return(S.lairs||[]).filter(L=>L.pid===k&&L.hull>0)}
function lairOwner(L){if(!L)return null;if(L.pid==='me'||isMe(L.pid))return S.player;return(S.pilots||{})[L.pid]||null}
function lairStash(L){return LAIR_B.stash[L&&L.lvl||1]||200}
// your own Lair in this system (for docking and drawing)
{const o=lairHere;lairHere=function(){if(S.unb)return o.apply(this,arguments);const k=curPid()||'me';return(S.lairs||[]).find(L=>L.sid===W.sid&&L.hull>0&&L.pid===k)}}
{const o=lairNear;lairNear=function(){if(S.unb)return o.apply(this,arguments);const L=W&&lairHere(),p=W&&W.player;return L&&p&&!(L.build>S.T)&&d3(L,p)<260?L:null}}
// where a Lair could go from here: the nearest large rock within 700 m, in a system with no station
function lairSpot(P){if(!W||!W.player)return{why:'Launch first.'};const p=W.player;if(S.stations[W.sid])return{why:'A Lair needs a system with no station.'};if(lairHere())return{why:'You already have a Lair in this system.'};
  if(lairsOf(P).length>=LAIR_B.max)return{why:`You have ${LAIR_B.max} Lairs, the most one pilot can keep.`};let a=null,bd=LAIR_B.rockR;for(const r of S.sectors[W.sid].ast){if(r.comet||r.rift||oreTotal(r)<LAIR_B.rockMin)continue;const d=d3(r,p)-astR(r);if(d<bd){bd=d;a=r}}
  if(!a)return{why:`Fly within ${LAIR_B.rockR} m of a large asteroid.`};if(!haveIn(LAIR_B.cost,[P.cargo]))return{why:`You need ${lackText(LAIR_B.cost,P.cargo)} in your hold.`,a};return{a}}
function lairBuildB(){const P=S.player,sp=lairSpot(P);if(!sp.a||sp.why){flash(sp.why||'No spot for a Lair here.',true);return sp.why||''}if(NET.cl){netSend({t:'lairb'});return'✓ Building…'}return lairMake(P,sp.a)}
function lairMake(P,a){const force={};takeFrom(LAIR_B.cost,[P.cargo]);inv.addAll(force,LAIR_B.cost);const o=rdir(.3),R=astR(a)+120;
  const L={id:S.nextId++,pid:pkeyOf(P),sid:W.sid,x:Math.round(a.x+o.x*R),y:Math.round(a.y+o.y*R),z:Math.round(a.z+o.z*R),stash:{},fort:force,hull:LAIR_B.hull,seen:{},lvl:1,build:S.T+LAIR_B.build};(S.lairs=S.lairs||[]).push(L);
  const msg=`⛏ Building your Lair beside the rock (${LAIR_B.build} s). It's hidden from every power until one of their scouts finds it.`;keyFeed(L.pid,msg,'good');return msg}
// host / single player, every frame in a loaded system: scouts find Lairs; ships of a power that found one wear it down
function lairWorldB(dt){const Ls=(S.lairs||[]).filter(L=>L.sid===W.sid&&L.hull>0);if(!Ls.length)return;
  for(const L of Ls){const O=lairOwner(L);if(!O)continue;if(L.build&&S.T>=L.build){L.build=0;keyFeed(L.pid,`⛏ Your Lair in ${DEF[L.sid].name} is ready: dock with E nearby.`,'good')}
    for(const e of W.ents){if(e.type!=='ship'||!e.alive||!FAC_IDS.includes(e.side)||!e.npc)continue;if(!pilotHostile(O,e.side))continue;
      if(e.role==='scout'&&!L.seen[e.side]&&d3(e,L)<LAIR_B.seeR){L.seen[e.side]=1;keyFeed(L.pid,`⚠ A ${FACTIONS[e.side].short} scout has found your Lair in ${DEF[W.sid].name}. Their ships will attack it on sight.`,'bad')}
      if(L.seen[e.side]&&d3(e,L)<2500)L.hull-=6*dt}
    if(L.hull<=0){const s=S.sectors[W.sid];if(Object.keys(L.stash).length)s.crates.push({id:S.nextId++,x:L.x,y:L.y,z:L.z,inv:L.stash,until:S.T+600});toDebris(s,L.fort||{});L.stash={};L.fort={};S.lairs=S.lairs.filter(x=>x!==L);
      if(!MUTE)fxBoom(L,260,'#ffcf5a');keyFeed(L.pid,`✕ Your Lair in ${DEF[W.sid].name} was destroyed. Its stash is drifting as salvage.`,'bad');lairEvict(L)}}}
function lairDrawB(){const k=curPid()||'me';for(const L of(S.lairs||[])){if(L.sid!==W.sid||L.hull<=0||L.pid!==k||!inView(L.x,L.y,L.z,120))continue;qAxis(.2,1,.1,.6,_xq);qNorm(_xq);mModel(MM,L.x,L.y,L.z,_xq,90,70,84);drawMesh(astMesh(3,'fe'),MM);
    sprite(L.x,L.y+70,L.z,18+4*Math.sin(W.t*3),L.build>S.T?[.9,.6,.3]:[.85,.8,.55],.7)}}
{const o=drawWorks;drawWorks=function(t){const r=o.apply(this,arguments);try{if(S&&!S.unb&&W)lairDrawB()}catch(e){}return r}}
{const o=worldUpdate;worldUpdate=function(dt){const r=o.apply(this,arguments);try{if(W&&!NET.cl&&!S.unb&&!S.training)lairWorldB(dt)}catch(err){console.error(err)}return r}}
// docked at a Lair: its level sets the stash, workshop and forge; heat cools faster; stolen tags come off what's in the stash
{const o=dockCtx;dockCtx=function(){const c=o.apply(this,arguments);if(!c||c.kind!=='lair'||S.unb)return c;const P=S.player,L=(S.lairs||[]).find(x=>x.id===P.lairId);if(!L)return c;
  c.owner='player';c.sub=`Your Lair · level ${L.lvl||1} · ${DEF[L.sid].name} · stash ${invMass(L.stash)}/${lairStash(L)} t`;c.fab=(L.lvl||1)>=2;c.forge=(L.lvl||1)>=2;c.fee=false;c.lairRec=L;return c}}
{const o=scanStep;scanStep=function(dt){const r=o.apply(this,arguments);for(const P of[S.player,...Object.values(S.pilots||{})]){if(!P||P.docked!=='lair'||!P.heat)continue;for(const f in P.heat)P.heat[f]=Math.max(0,P.heat[f]-SM.cool*(LAIR_B.cool-1)*dt)}return r}}
// the stash's size follows the Lair's level (Driftgate 1 read a fixed 200 t)
{const o=dockAction;dockAction=function(act,arg){const c=dockCtx();if(c&&c.lairRec&&(act==='mv'||act==='mvall')&&String(arg).includes(':in')||c&&c.lairRec&&act==='stashall'){const L=c.lairRec,cap=lairStash(L),keep=LAIR.stash;LAIR.stash=cap;try{return o.apply(this,arguments)}finally{LAIR.stash=keep}}
  if(act==='lairup'){const P=S.player,L=(S.lairs||[]).find(x=>String(x.id)===String(arg)&&x.pid===pkeyOf(P));if(!L){dockErr='No such Lair.';return}if((L.lvl||1)>=2){dockErr='That Lair is already level 2.';return}
    const srcs=[P.cargo,c&&c.storage||P.vault];if(!haveIn(LAIR_B.up,srcs)){dockErr=`Level 2 needs ${lackText(LAIR_B.up,Object.assign({},P.cargo,c&&c.storage||{}))}.`;return}takeFrom(LAIR_B.up,srcs);inv.addAll(L.fort=L.fort||{},LAIR_B.up);L.lvl=2;dockErr=`✓ Your Lair in ${DEF[L.sid].name} is level 2: a 400 t stash, a workshop and a forge with no fee.`;return}
  if(act==='lairbuild'){dockErr=lairBuildB();return}return o.apply(this,arguments)}}
// LAIR.stash is a const object field, so the wrapper above can lend it a level's capacity for the duration of a move
// ---- guests: build a Lair (host side)
function hLairBuild(pid){const P=S.pilots&&S.pilots[pid],e=MP.rp&&MP.rp[pid];if(!P||!e)return;inW(worldOf(e),()=>runAs(pid,()=>{const sp=lairSpot(P);if(sp.why||!sp.a){netMsg(pid,'flash',sp.why||'No spot for a Lair here.',true);return}lairMake(P,sp.a)}))}
// ============================================================ the Company screen
let coTab='holdings';
function coTabs(){return[['allegiance','Allegiance'],['holdings','Holdings']]}
function holdingsHtml(P){const Ls=lairsOf(P),sp=!P.docked&&W&&W.player?lairSpot(P):null;
  let h=`<p class="note" style="margin:0 0 10px">Your bases. A Lair is your first: hidden beside a large asteroid in a system with no station, with a stash, repairs and rearming. Up to ${LAIR_B.max}, one per system. Depots and Stations are below.</p>`;
  h+=`<div class="tblw"><table class="t"><thead><tr><th>Base</th><th>System</th><th>Level</th><th class="r">Stash</th><th>Status</th><th></th></tr></thead><tbody>`;
  for(const L of Ls){const seen=Object.keys(L.seen||{}).filter(f=>L.seen[f]);h+=`<tr><td class="iname">Lair</td><td>${esc(DEF[L.sid].name)}</td><td>${L.lvl||1}</td><td class="r num">${invMass(L.stash)}/${lairStash(L)} t</td><td>${L.build>S.T?`building · ${Math.ceil(L.build-S.T)} s`:seen.length?`<span style="color:var(--danger)">found by ${seen.map(f=>esc(FACTIONS[f].short)).join(', ')}</span> · hull ${Math.round(L.hull/LAIR_B.hull*100)}%`:'hidden'}</td>
    <td>${(L.lvl||1)<2?`<button class="btn sm" type="button" data-co="lairup" data-arg="${L.id}" title="${esc(lackText(LAIR_B.up,{})||'')}">To level 2 · ${Object.keys(LAIR_B.up).map(k=>`${LAIR_B.up[k]} ${esc(ITEMS[k].name)}`).join(', ')}</button>`:''}</td></tr>`}
  if(!Ls.length)h+=`<tr><td colspan="6" class="note">No bases yet.</td></tr>`;h+=`</tbody></table></div>`;
  h+=`<div class="h3" style="margin-top:16px">Build a Lair</div><p class="note" style="margin:0 0 8px">Carry a Depot Frame and 6 Alloy Plate in your hold to a large asteroid in a system with no station, then build here or with the comms build order. Upgrading to level 2 (a Depot Frame, 10 Alloy Plate and 4 Flux Coils, from your hold or the stash, while docked there) adds a workshop, a forge and a 400 t stash.</p>`;
  if(sp)h+=sp.why?`<div class="note" style="color:var(--amber)">${esc(sp.why)}</div>`:`<button class="btn pri" type="button" data-co="lairbuild">Build a Lair here · ${esc(DEF[W.sid].name)}</button>`;else h+=`<div class="note">Launch to build.</div>`;return h}
function renderCompany(){const el=$('company');if(!el||el.hidden||!S||!S.player)return;const P=S.player;$('coTitle').textContent=P.name?`${P.name}'s company`:'Company';$('coSub').textContent=`Contractor Rating ${ratingOf(P)} · ${fmt(P.credits)} cr · ${lairsOf(P).length} base${lairsOf(P).length===1?'':'s'}`;
  $('coTabs').innerHTML=coTabs().map(([k,n])=>`<button class="tab" type="button" role="tab" data-co="tab" data-arg="${k}" aria-selected="${coTab===k}">${n}</button>`).join('');
  $('coBody').innerHTML=coTab==='allegiance'?allegianceHtml(P):coTab==='holdings'?holdingsHtml(P):'';$('coErr').textContent=coErr||''}
let coErr='';
function toggleCompany(){const el=$('company');if(!el||!S||!running)return;el.hidden=!el.hidden;if(!el.hidden){$('map').hidden=true;$('help').hidden=true;coErr='';renderCompany()}}
function coClick(act,arg){coErr='';if(act==='tab'){coTab=arg;renderCompany();return}
  if(act==='lairbuild'){coErr=lairBuildB()||'';renderCompany();return}
  if(act==='lairup'){if(!S.player.docked||S.player.docked!=='lair'){coErr='Dock at that Lair to upgrade it: the materials go in from your hold or its stash.';renderCompany();return}if(NET.cl){netSend({t:'act',act:'lairup',arg});coErr='Working…';renderCompany();return}dockAction('lairup',arg);coErr=dockErr;renderCompany();return}}
{const el=$('company');if(el)el.addEventListener('click',e=>{const b=e.target.closest('[data-co]');if(!b||b.disabled)return;coClick(b.dataset.co,b.dataset.arg)})}
{const b=$('bCompany');if(b)b.addEventListener('click',()=>toggleCompany())}
{const o=hudUpdate;hudUpdate=function(){const r=o.apply(this,arguments);try{const el=$('company');if(el&&!el.hidden&&(!W||!W._coT||W.t-W._coT>1)){if(W)W._coT=W.t;renderCompany()}}catch(err){}return r}}
