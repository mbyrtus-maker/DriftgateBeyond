//@src 16l_smuggling.js
// ============================================================ smuggling: contraband, heat, customs scans (Beyond stage 7b)
// Contraband is a mark on real goods, never a new good, so the ledger is unchanged:
//   stolen      cargo salvaged from a power's ships or convoys stays tagged as that power's (P.stol[item][power] = units)
//   run         goods carried on a black-market run, contraband for the power whose space they are smuggled into (P.run)
//   cash-only   Ghost relics (from anomaly caches) and Riftstone: illegal in every power's space (Riftstone is legal in
//               Ostrova space, where it is studied)
// Heat (P.heat[power], 0-100) is how hard a power's patrols are looking for you: caught, a refused bribe, a run and theft raise
// it; it cools on its own. While a power's heat is up its patrols scan you more often; after you run from one of its scans its
// ships treat you as hostile until the heat drops below Hot.
// Customs: a power's patrols scan pilots in its space now and then (more near its stations, the hotter you are, the lower your
// standing). A scan takes 5 s in range. A hidden cargo container (utility part) keeps its contents out of most scans.
// When a scan finds contraband: Bribe (credits to that power's treasury; may be refused), Surrender (the goods go to that
// power's stores, a fine, a little standing) or Run (you keep the goods; heat, and its ships turn on you). No answer in 15 s
// is a surrender.
const SM={cool:.05,scanR:900,scanT:5,decide:15,every:3,hot:35,hostile:70,heat:{stolen:20,cash:20,Light:15,Heavy:30,Severe:50},bribeK:.5,fineK:.15,runHeat:40,refused:25,stand:-3,theft:6,
  hide:{base:4,step:4},rift:{n:2,zap:3,zapR:260,dmg:[6,14],blast:60}};
const SM_BANDS=[['Cool','#7ad9a7',10],['Warm','#f0d070',SM.hot],['Hot','#ff9a4a',SM.hostile],['Burning','#ff5d4f',101]];
function heatOf(f,P){P=P||S.player;return(P&&P.heat&&P.heat[f])||0}
function heatWord(v){return SM_BANDS.find(b=>v<b[2])||SM_BANDS[3]}
function smHeat(P,f,n,why){if(!P||!FAC_IDS.includes(f)||!n)return;P.heat=P.heat||{};const v0=P.heat[f]||0,v1=clamp(v0+n,0,100);P.heat[f]=v1;const a=heatWord(v0)[0],b=heatWord(v1)[0];
  if(a!==b&&(P===S.player))feed(`${v1>v0?'🔥':'❄'} ${FACTIONS[f].short} heat: ${b}${why?` (${why})`:''}.`,v1>v0?'bad':'good')}
// ---- items: the hidden cargo container (a utility part), Ghost relics, Riftstone and Rift Shards
UTIL.hide={name:'Hidden cargo container',desc:'A concealed hold: up to 4 t of what you carry stays out of customs scans (+4 t a grade), and better grades are harder to find.'};
PART.hide='pt_hide';PART_RC.hide={plate:2,wire:1};PART_COL.hide='#9aa0b4';ITEMS.pt_hide={name:UTIL.hide.name,recipe:PART_RC.hide,col:PART_COL.hide,part:'hide'};ITEM_ORDER.push('pt_hide');CRAFTABLE.push('pt_hide');
ITEMS.relic={name:'Ghost relic',recipe:{xc:1},col:'#e0d0ff',cash:1};ITEMS.rift={name:'Riftstone',recipe:{xc:1},col:'#ff4fc8',cash:1,legal:['ostrova']};ITEMS.riftshard={name:'Rift Shard',recipe:{rift:3},col:'#ff7ad8',cash:1,legal:['ostrova']};
for(const k of['relic','rift','riftshard'])ITEM_ORDER.push(k);CRAFTABLE.push('riftshard');
function hideCap(P){if(!loadOn())return 0;const F=fitOf(P);let c=0;F.u.forEach((k,i)=>{if(k==='hide')c+=SM.hide.base+SM.hide.step*((F.ug[i]||1)-1)});return c}
function hideGrade(P){return fitUG(P,'hide')}
// ---- stolen tags
function stolAdd(P,k,f,n){if(!P||!FAC_IDS.includes(f)||!(n>0))return;P.stol=P.stol||{};const t=P.stol[k]=P.stol[k]||{};t[f]=(t[f]||0)+n}
// tags follow the goods: once fewer units are held (hold and vault) than are tagged, the tags shrink with them
function stolSync(P){if(!P||!P.stol)return;for(const k in P.stol){const have=(P.cargo[k]||0)+((P.vault||{})[k]||0),t=P.stol[k];let tot=0;for(const f in t)tot+=t[f];if(tot>have){const r=tot?have/tot:0;for(const f in t){t[f]=Math.floor(t[f]*r);if(!t[f])delete t[f]}}if(!Object.keys(t).length)delete P.stol[k]}}
// what in the hold is contraband for power f: [{k,n,why}]
function contraFor(P,f){stolSync(P);const out=[];for(const k in P.cargo){const n=P.cargo[k]||0;if(!n)continue;const I=ITEMS[k]||{};
    if(I.cash&&!(I.legal||[]).includes(f)){out.push({k,n,why:'cash'});continue}
    const s=P.stol&&P.stol[k]&&P.stol[k][f];if(s){out.push({k,n:Math.min(n,s),why:'stolen'});continue}
    if(P.run&&P.run.f===f&&P.run.item===k){out.push({k,n:Math.min(n,P.run.n),why:P.run.rating})}}return out}
function contraValue(L){return L.reduce((v,x)=>v+baseValue(x.k)*x.n,0)}
// crates spilled from a power's ships carry its mark; scooping them tags the goods
function crateTake(P,cr,k){if(cr&&cr.own&&FAC_IDS.includes(cr.own)){stolAdd(P,k,cr.own,1);P._theft=(P._theft||0)+1;P._theftF=cr.own}}
// ---- customs scans (host and single player; a guest's scans run on the host, and an unanswered scan is a surrender)
function inSpaceOf(sid,f){const R=S.stations[sid];if(R&&R.owner===f)return true;if(DEF[sid]&&DEF[sid].home===f)return true;try{return sectorOwner(sid)===f}catch(e){return false}}
function scanTick(dt){if(NET.cl||!W||!S||S.training||S.unb)return;W.scT=(W.scT||0)-dt;if(W.scT>0)return;W.scT=SM.every;
  const pilots=[];if(W===LW&&W.player&&W.player.alive&&!S.player.docked&&!W.dead)pilots.push([W.player,S.player,'me']);for(const e of W.ents)if(e.rp&&e.alive&&S.pilots&&S.pilots[e.rp]&&!S.pilots[e.rp].docked)pilots.push([e,S.pilots[e.rp],e.rp]);
  for(const[e,P,key]of pilots){if(P.sworn||P.scan||P.caught)continue;
    for(const f of FAC_IDS){if(!inSpaceOf(W.sid,f))continue;const pat=W.ents.find(x=>x.npc&&x.alive&&x.type==='ship'&&x.side===f&&(x.role==='patrol'||x.role==='escort'||x.role==='picket'||x.role==='frigate')&&d3(x,e)<SM.scanR);if(!pat)continue;
      const st=standOf(f,P),near=W.stationEnt&&d3(W.stationEnt,e)<3000?2:1,pr=(.02+heatOf(f,P)/1500+(st<0?-st/2500:0))*near;if(Math.random()>pr)continue;
      P.scan={f,t:SM.scanT,by:pat.id,key};scanSay(key,`⚠ ${FACTIONS[f].short} customs: a patrol is scanning you (${SM.scanT} s).`,true);break}}}
function scanSay(key,msg,bad){if(key==='me'||isMe(key)){flash(msg,!!bad);feed(msg,bad?'warn':'info')}else netMsg(key,'flash',msg,!!bad)}
function scanStep(dt){if(NET.cl||!S)return;for(const[P,key]of[[S.player,'me'],...Object.entries(S.pilots||{}).filter(([k])=>!isMe(k)).map(([k,P])=>[P,k])]){if(!P)continue;
    if(P.scan){P.scan.t-=dt;if(P.scan.t<=0){const f=P.scan.f;P.scan=null;scanResolve(P,f,key)}}
    if(P.caught){P.caught.t-=dt;if(P.caught.t<=0&&!P.caught.done)scanChoice('surrender',P)}
    if(P.heat)for(const f in P.heat){P.heat[f]=Math.max(0,P.heat[f]-SM.cool*dt);if(!P.heat[f])delete P.heat[f]}
    if(P._theft){smHeat(P,P._theftF,P._theft*SM.theft/10,'stolen cargo');P._theft=0}}}
function scanResolve(P,f,key){const L=contraFor(P,f);if(!L.length){scanSay(key,`✓ ${FACTIONS[f].short} customs: scan clear.`);return}
  // the hidden container: up to its capacity of contraband (most valuable first) stays hidden unless the patrol beats its grade
  let cap=hideCap(P);const g=hideGrade(P),found=[];if(cap>0){const pg=Math.min(5,factionTier(f)+1),beat=Math.random()<clamp(.25+.15*(pg-g),.05,.9);
    for(const x of L.sort((a,b)=>baseValue(b.k)-baseValue(a.k))){const m=mass(x.k),h=beat?0:Math.min(x.n,Math.floor(cap/m));cap-=h*m;if(x.n-h>0)found.push({...x,n:x.n-h})}}else found.push(...L);
  if(!found.length){scanSay(key,`✓ ${FACTIONS[f].short} customs: scan clear (your hidden container held).`);return}
  const v=contraValue(found),rate=Math.max(...found.map(x=>SM.heat[x.why]||15));
  P.caught={f,L:found,v,heat:rate,bribe:Math.max(50,Math.ceil(v*SM.bribeK)),fine:Math.ceil(v*SM.fineK),t:SM.decide,key};
  scanSay(key,`⛔ ${FACTIONS[f].short} customs found contraband: ${found.map(x=>`${x.n} ${ITEMS[x.k].name}`).join(', ')}. Bribe, surrender or run.`,true);if(key!=='me'&&!isMe(key))netMsg(key,'caught',P.caught)}
// the pilot's answer to a scan that found contraband
function scanChoice(ch,P){P=P||S.player;const C=P.caught;if(!C||C.done)return'';const f=C.f,key=C.key||'me';C.done=1;let msg='';
  if(ch==='bribe'){const L=leaderOf(f),ok=!(L&&hasT(L,'Vengeful'))&&Math.random()<clamp(.45+standOf(f,P)/150,.1,.9)&&P.credits>=C.bribe;
    if(ok){transfer('player',f,C.bribe);smHeat(P,f,C.heat/2,'bribed a patrol');msg=`💰 The ${FACTIONS[f].short} patrol takes ${fmt(C.bribe)} cr and looks the other way.`;P.caught=null;scanSay(key,msg);return msg}
    smHeat(P,f,SM.refused,'a refused bribe');C.done=0;C.heat+=SM.refused;C.t=SM.decide;C.noBribe=1;msg=`✋ The ${FACTIONS[f].short} patrol refuses your bribe. Surrender or run.`;scanSay(key,msg,true);return msg}
  if(ch==='surrender'){const st=S.econ.stock[f]=S.econ.stock[f]||{};for(const x of C.L){const n=Math.min(x.n,P.cargo[x.k]||0);inv.take(P.cargo,x.k,n);inv.add(st,x.k,n);if(x.why==='run'||P.run&&P.run.item===x.k)P.run=null}
    const fine=transfer('player',f,Math.min(C.fine,P.credits));standAdd(f,SM.stand,'contraband',P);smHeat(P,f,C.heat,'caught with contraband');stolSync(P);
    msg=`⛔ Contraband confiscated by ${FACTIONS[f].short}${fine?`, and a ${fmt(fine)} cr fine`:''}.`;P.caught=null;scanSay(key,msg,true);return msg}
  if(ch==='run'){smHeat(P,f,C.heat*2+SM.runHeat,'ran from customs');P.ranF=P.ranF||{};P.ranF[f]=1;(P.aggro||(P.aggro={}))[f]=S.T+120;msg=`🏃 You run. ${FACTIONS[f].short} ships will hunt you until your heat with them cools below Hot.`;P.caught=null;scanSay(key,msg,true);return msg}return''}
// after a run, a hot power's ships treat the pilot as hostile
{const o=pilotHostile;pilotHostile=function(P,x){if(o.apply(this,arguments))return true;P=P||S.player;return!!(P&&P.ranF&&P.ranF[x]&&heatOf(x,P)>=SM.hostile)}}
{const o=worldUpdate;worldUpdate=function(dt){const r=o.apply(this,arguments);try{if(W&&!NET.cl){scanTick(dt);riftTick(dt);const d=S.T-(S._smLast==null?S.T:S._smLast);S._smLast=S.T;if(d>0)scanStep(d)}}catch(err){console.error(err)}return r}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{fixerTick()}catch(err){console.error(err)}return r}}
// the decision box (local pilot)
function scanBox(){let el=document.getElementById('scanBox');const C=S&&S.player&&S.player.caught;if(!C||C.done&&!C.noBribe){if(el)el.hidden=true;return}
  if(!el){el=document.createElement('div');el.id='scanBox';el.style.cssText='position:fixed;left:50%;top:22%;transform:translateX(-50%);z-index:40;background:rgba(10,15,29,.95);border:1px solid #ff5d4f;padding:12px 16px;color:#ece4cf;font:500 14px "Saira Semi Condensed",sans-serif;max-width:520px;text-align:center';
    el.addEventListener('click',ev=>{const b=ev.target.closest('[data-sc]');if(!b)return;if(NET.cl){netSend({t:'scanch',ch:b.dataset.sc});S.player.caught=null}else scanChoice(b.dataset.sc)});document.body.appendChild(el)}
  el.hidden=false;const f=C.f;el.innerHTML=`<div style="color:#ff5d4f;font-weight:700;letter-spacing:.08em">${esc(FACTIONS[f].short.toUpperCase())} CUSTOMS · ${Math.ceil(C.t)} s</div><div style="margin:6px 0 10px">Contraband found: ${C.L.map(x=>`${x.n} ${esc(ITEMS[x.k].name)}`).join(', ')} (${fmt(Math.round(C.v))} cr).</div>`+
    `<div style="display:flex;gap:8px;justify-content:center">${C.noBribe?'':`<button class="btn" data-sc="bribe">Bribe · ${fmt(C.bribe)} cr</button>`}<button class="btn" data-sc="surrender">Surrender${C.fine?` · ${fmt(C.fine)} cr fine`:''}</button><button class="btn" data-sc="run">Run</button></div>`}
{const o=hudUpdate;hudUpdate=function(){const r=o.apply(this,arguments);try{scanBox()}catch(err){}return r}}
// ============================================================ Riftstone: rare unstable rocks out beyond the gates
// A few rocks rich in Xenocrystal in deep space are Riftstone (flagged when the galaxy is made and moved out beyond the gate
// ring). Its Xenocrystal comes out as Riftstone (1 t of Xenocrystal each, so the ledger is unchanged). It throws rift
// discharges that hurt ships nearby, its ring flickers out, and a blast on it sets off a chain reaction.
function riftInit(){if(S.riftV)return;S.riftV=1;for(const d of SECTOR_DEFS.filter(d=>d.kind==='deep'||d.kind==='void')){const s=S.sectors[d.id];if(!s)continue;const gr=Math.max(1500*SPACE,...(GATES[d.id]||[]).map(g=>hyp(g.x,g.y,g.z)));
    const L=s.ast.filter(a=>!a.comet&&!a.rift&&(a.ore.xc||0)>=8).sort((a,b)=>(b.ore.xc||0)-(a.ore.xc||0)).slice(0,SM.rift.n);for(const a of L){a.rift=1;const p=randPos(gr+500,gr+1400);a.x=Math.round(p.x);a.y=Math.round(p.y);a.z=Math.round(p.z)}}}
{const o=newGame;newGame=function(){const r=o.apply(this,arguments);try{if(S)riftInit()}catch(err){}return r}}
function riftTick(dt){const s=S.sectors[W.sid];if(!s)return;W.rfT=(W.rfT||0)-dt;if(W.rfT>0)return;W.rfT=SM.rift.zap*rnd(.7,1.3);
  for(const a of s.ast){if(!a.rift)continue;const near=W.ents.filter(e=>e.type==='ship'&&e.alive&&d3(e,a)<astR(a)+SM.rift.zapR);if(!near.length)continue;const e=pick(near);
    if(!MUTE)fxSpark(e,'#ff4fc8',8);damageShip(e,rnd(SM.rift.dmg[0],SM.rift.dmg[1]),null,{x:a.x,y:a.y,z:a.z},'blast');if(e===W.player)flash('⚡ Rift discharge!',true)}}
{const o=ringOK;ringOK=function(a){if(!o.apply(this,arguments))return false;if(a.rift&&W&&Math.sin(W.t*1.7+a.id)<-.3)return false;return true}}
// cutting Riftstone: each unit of Xenocrystal comes out as a unit of Riftstone
{const o=mlCut;mlCut=function(e,P,a,dt,sec,show){if(!a||!a.rift||show)return o.apply(this,arguments);const x0=a.ore.xc||0,h0=P.cargo.xc||0;const r=o.apply(this,arguments);const got=Math.min((P.cargo.xc||0)-h0,x0-(a.ore.xc||0));if(got>0){inv.take(P.cargo,'xc',got);inv.add(P.cargo,'rift',got)}return r}}
{const o=blDetonate;blDetonate=function(P,e){const s=S.sectors[W.sid],k=blKey(P),rifts=(s.charges||[]).filter(c=>c.o===k&&!c.wp).map(c=>s.ast.find(a=>a.id===c.a)).filter(a=>a&&a.rift);const n0=(s.clouds||[]).length;const r=o.apply(this,arguments);
  for(const c of(s.clouds||[]).slice(n0))if(c.ore&&c.ore.xc&&rifts.length){c.rift=1}
  for(const a of rifts){if(!MUTE){fxBoom(a,astR(a)*2.4,'#ff4fc8');W.shake=Math.max(W.shake||0,.7)}for(const x of W.ents.slice())if(x.type==='ship'&&x.alive){const d=d3(x,a);if(d<300)damageShip(x,SM.rift.blast*(1-d/300)+10,null,a,'blast')}if(P===S.player)feed('⚡ The Riftstone went up in a chain reaction.','bad')}return r}}
{const o=blCollect;blCollect=function(e,P,c){if(!c||!c.rift)return o.apply(this,arguments);const h0=P.cargo.xc||0,x0=c.ore.xc||0;const r=o.apply(this,arguments);const got=Math.min((P.cargo.xc||0)-h0,x0-(c.ore.xc||0));if(got>0){inv.take(P.cargo,'xc',got);inv.add(P.cargo,'rift',got)}return r}}
// anomaly caches now hold a Ghost relic (made from Xenocrystal in the recycling pools)
{const o=anomOpen;anomOpen=function(sid,A,k){const kind=A&&A.kind;const s=S.sectors[sid],n0=s?s.crates.length:0;const r=o.apply(this,arguments);try{if(kind==='cache'&&s&&s.crates.length>n0){const x=driftTake(1,['xc'],sid);if(x.xc){inv.add(s.crates[s.crates.length-1].inv,'relic',1)}}}catch(err){}return r}}
// ============================================================ black-market runs (fixers at the freeports)
// Fixers post runs: carry goods from this freeport's market into a power's station past its customs. The goods come out of
// the freeport's stock and go into the destination's market; the freeport's fixer pays on delivery, by the heat the run would
// bring if caught: Light +25%, Heavy +50% (a power with an embargo running), Severe +75% (into that power's core).
const BM_RATE={Light:.25,Heavy:.5,Severe:.75},BM_MAX=3;
function fixerTick(){if(NET.cl||S.training||S.unb)return;S.bm=(S.bm||[]).filter(x=>S.T<x.until||x.taken);for(const id in S.stations){const R=S.stations[id];if(!R||R.owner!=='neutral')continue;
    if(S.bm.filter(x=>x.from===id&&!x.taken).length>=BM_MAX||Math.random()>.15)continue;const st=mkStock(R),goods=Object.keys(st).filter(k=>RAWS.includes(k)||['plate','wire','coil','lattice'].includes(k)).filter(k=>(st[k]||0)>=8);if(!goods.length)continue;
    const dests=Object.keys(S.stations).filter(s=>{const D=S.stations[s];return D&&FAC_IDS.includes(D.owner)&&HOP[id]&&HOP[id][s]!=null&&HOP[id][s]<=5});if(!dests.length)continue;
    const to=pick(dests),f=S.stations[to].owner,emb=FAC_IDS.some(g=>g!==f&&(pairOf(f,g)||{}).emb),core=S.stations[to].kind==='core',rating=emb?(core?'Severe':'Heavy'):'Light',item=pick(goods),n=Math.min(st[item],ri(6,16));
    S.bm.push({id:S.nextId++,from:id,to,f,item,n,rating,pay:Math.round(baseValue(item)*n*(1+BM_RATE[rating])+150+60*HOP[id][to]),until:S.T+900})}}
{const o=jobsList;jobsList=function(c,P,srcs){const out=o.apply(this,arguments);if(S.unb||S.training||!c||c.owner!=='neutral')return out;try{
  for(const x of(S.bm||[]).filter(x=>x.from===P.sector&&!x.taken&&S.T<x.until)){const h=HOP[P.sector][x.to],fs=FACTIONS[x.f].short;
    out.push({id:'bmr:'+x.id,by:'neutral',sid:x.to,ty:'haul',title:`Black-market run: ${x.n} ${esc(ITEMS[x.item].name)} into ${esc(S.stations[x.to].name)}`,sub:`${x.rating} heat with ${esc(fs)} if caught · ${Math.max(0,Math.round((x.until-S.T)/60))} min to take it`,hops:h,where:`${h} jump${h===1?'':'s'}`,payN:x.pay,pay:`${fmt(x.pay)} cr`,
      btn:P.run?null:['bmtake',x.id,'Take the run'],need:P.run?'You are already on a run.':'',detail:()=>`<p class="note" style="margin:0">A fixer's goods, loaded into your hold here. Dock at ${esc(S.stations[x.to].name)} to hand them over and be paid. ${esc(fs)} patrols treat them as contraband: if a scan finds them it's <b>${x.rating}</b> heat with ${esc(fs)} (half if a bribe works, double if you run), and surrendered goods are lost with the pay. A hidden cargo container helps. Pays by the heat it risks: +${Math.round(BM_RATE[x.rating]*100)}% on the goods' value.</p>`})}}catch(err){console.error(err)}return out}}
{const o=dockAction;dockAction=function(act,arg){if(act==='bmtake'||act==='scanch'){const c=dockCtx(),P=S.player;if(act==='scanch'){dockErr=scanChoice(arg,P);return}
    const x=(S.bm||[]).find(y=>String(y.id)===String(arg)&&!y.taken);if(!x){dockErr='That run is gone.';return}if(P.run){dockErr='You are already on a run.';return}const st=mkStock(S.stations[x.from]),m=mass(x.item)*x.n,room=W&&W.player?W.player.st.cargo-invMass(P.cargo):0;
    if(room<m){dockErr=`It needs ${m} t of hold space.`;return}const n=inv.take(st,x.item,x.n);if(!n){dockErr='The goods are gone.';return}inv.add(P.cargo,x.item,n);x.taken=1;P.run={id:x.id,item:x.item,n,f:x.f,to:x.to,rating:x.rating,pay:Math.round(x.pay*n/x.n)};P.route=x.to;
    dockErr=`✓ Loaded ${n} ${ITEMS[x.item].name}. Course set to ${S.stations[x.to].name}: ${x.rating} heat with ${FACTIONS[x.f].short} if you're caught.`;return}return o.apply(this,arguments)}}
// docking at the run's destination hands the goods over and the fixer's freeport pays
{const o=openDock;openDock=function(){const r=o.apply(this,arguments);try{const P=S.player,R=P.run;if(R&&!NET.cl&&P.docked==='station'&&P.sector===R.to){const st=mkStock(S.stations[R.to]),n=inv.take(P.cargo,R.item,R.n);inv.add(st,R.item,n);const pay=transfer('neutral','player',Math.round(R.pay*n/R.n));P.run=null;feed(`✓ Black-market run delivered: ${n} ${ITEMS[R.item].name}, +${fmt(pay)} cr from the fixer.`,'good')}}catch(err){console.error(err)}return r}}
// selling goods stolen from a power to that power's own market is refused
{const o=dockAction;dockAction=function(act,arg){if(act==='sell'&&!S.unb){const c=dockCtx(),P=S.player,k=String(arg).split(':')[0];stolSync(P);if(FAC_IDS.includes(c.owner)&&P.stol&&P.stol[k]&&P.stol[k][c.owner]){dockErr=`${FACTIONS[c.owner].short} would know its own cargo: sell the stolen ${ITEMS[k].name} elsewhere.`;return}}return o.apply(this,arguments)}}
// heat shows on the Allegiance tab beside standing
{const o=allegianceHtml;allegianceHtml=function(P){let h=o.apply(this,arguments);P=P||S.player;if(P.sworn)return h;
  return h+`<div class="h3" style="margin-top:18px">Heat</div><p class="note" style="margin:0 0 6px">How hard each power's patrols are looking for you right now. It cools on its own.</p><div style="display:flex;gap:14px;flex-wrap:wrap">${FAC_IDS.map(f=>{const w=heatWord(heatOf(f,P));return`<span>${esc(FACTIONS[f].short)} <b style="color:${w[1]}">${w[0]}</b></span>`}).join('')}</div>`}}
