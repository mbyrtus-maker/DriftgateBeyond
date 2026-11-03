//@src 16zi_small.js
// ============================================================ the smaller items (Beyond, 3 Nov 2026)
// 1. Beacon rigs and limpet racks are fitted parts, on scout hulls only. A beacon rig holds one beacon device a grade, a limpet
//    rack one limpet a grade; both are restocked whenever you dock. No rig, no beacon flips; no rack, no limpets.
// 2. Comets and derelicts are sold as intel to the Compact: fly within 2.5 km of one (3.5 km with a scanner) to log it, then
//    sell the find at any freeport while it lasts. A comet pays 3 cr a tonne of its ore (at least 150), a derelict a fifth of
//    its cargo's value (at least 120).
// 3. Embargo contraband by origin: goods bought at a power's market carry its origin (a tag, like the stolen tag). While two
//    powers have an embargo running, each one's goods are contraband in the other's space (Heavy heat if caught).
// 4. The Rift Shard as a wild card: at a workshop, a Rift Shard stands in for one missing component of a recipe (the rift
//    pulls its makings out of the outer drift, so it only works while the drift holds them); fed into a part's upgrade, it
//    gives that part a random trait (most often a strength). Taking the part out loses the trait.
// Ledger: tags only mark goods; a shard's Riftstone goes into the outer drift, and anything it stands in for comes out of it.
const SMX={findR:2500,findScan:3500,cometCr:3,cometMin:150,derK:.2,derMin:120,embHeat:30,riftGood:.65};
// ---- 1. beacon rigs and limpet racks
UTIL.bdev={name:'Beacon rig',desc:'Scout hulls only. Holds one beacon device a grade, restocked when you dock: flip a system\'s beacon for the power you do intel work for.'};
UTIL.lrack={name:'Limpet rack',desc:'Scout hulls only. Holds one limpet a grade, restocked when you dock.'};
PART.bdev='pt_bdev';PART.lrack='pt_lrack';PART_RC.bdev={wire:1,coil:1};PART_RC.lrack={plate:1,wire:1};PART_COL.bdev='#7ad9f0';PART_COL.lrack='#c9a0ff';
for(const k of['bdev','lrack']){ITEMS[PART[k]]={name:UTIL[k].name,recipe:PART_RC[k],col:PART_COL[k],part:k};ITEM_ORDER.push(PART[k]);CRAFTABLE.push(PART[k])}
HULL_SLOTS.scout.u=['scanner','bdev','lrack'];HULL_SLOTS.scout2.u=['land','scanner','bdev','lrack'];
function smxN(P,k){if(!loadOn())return 1;const F=fitOf(P);let n=0;F.u.forEach((x,i)=>{if(x===k)n+=F.ug[i]||1});return n}
{const o=fitDo;fitDo=function(c,P,arg){const[g,i0,k0]=String(arg).split(':');const k=k0&&ITEMS[k0]&&ITEMS[k0].part||k0;if((k==='bdev'||k==='lrack')&&!isScoutCls(P.cls))return'Beacon rigs and limpet racks fit scout hulls only.';
  const F=fitOf(P);if(F.rt)delete F.rt[g+i0];return o.apply(this,arguments)}}
{const o=loadoutHtml;loadoutHtml=function(c,P){if(isScoutCls(P.cls))return o.apply(this,arguments);const a=UTIL.bdev,b=UTIL.lrack;delete UTIL.bdev;delete UTIL.lrack;try{return o.apply(this,arguments)}finally{UTIL.bdev=a;UTIL.lrack=b}}}
{const o=partsSeed;partsSeed=function(){o.apply(this,arguments);for(const id in S.stations||{}){const R=S.stations[id];if(R&&id===FAC_HOME('ostrova')&&R.owner==='ostrova'){const st=mkStock(R);inv.add(st,'pt_bdev',2);inv.add(st,'pt_lrack',2)}}}}
// flipping takes a beacon device from the rig
{const o=bcnFlipper;bcnFlipper=function(e){const r=o.apply(this,arguments);if(!r||!r.by||!loadOn()||S.unb)return r;const P=xPilotOfKey(r.by);if(!P)return r;return(P.bdUsed||0)<smxN(P,'bdev')?r:null}}
{const o=beaconFlip;beaconFlip=function(sid,side,by){const B=S.beacons&&S.beacons[sid],was=B&&B.owner;const r=o.apply(this,arguments);try{if(by&&loadOn()&&B&&B.owner!==was){const P=xPilotOfKey(by);if(P)P.bdUsed=(P.bdUsed||0)+1}}catch(e){}return r}}
{const o=beaconChip;beaconChip=function(){const r=o.apply(this,arguments);try{const P=S.player,B=S.beacons&&S.beacons[W.sid];if(loadOn()&&isScoutCls(P.cls)&&B&&W.player&&!P.docked&&d3(W.player,B)<=BCN_R*3&&(P.bdUsed||0)>=smxN(P,'bdev')&&!(P.sworn&&B.owner===P.sworn))return[smxN(P,'bdev')?'Beacon: your beacon rig is spent · dock to restock':'Beacon: fit a beacon rig to flip it','warn']}catch(e){}return r}}
// limpets from the rack: a pilot without one has none aboard; with one, a limpet a grade
{const o=limpetHold;limpetHold=function(hold,dt){const P=S.player;if(loadOn()&&!smxN(P,'lrack')){const F=W.lpF||(W.lpF={E:null,t:0,h:false});if(hold&&!F.h&&W.t-(W.drillMsg||0)>3){W.drillMsg=W.t;flash('No limpet rack fitted: fit one in a utility slot to carry limpets.')}F.h=hold;return}return o.apply(this,arguments)}}
{const o=limpetChip;limpetChip=function(){const P=S.player;if(loadOn()&&isScoutCls(P.cls)&&!smxN(P,'lrack'))return null;const r=o.apply(this,arguments);try{if(r&&loadOn()&&!P.limpetUsed&&smxN(P,'lrack')>1&&/ready/.test(r[0]))r[0]=r[0].replace('Limpet ready',`Limpet ready (${smxN(P,'lrack')-(P.lpN||0)} aboard)`)}catch(e){}return r}}
function smxRigTick(){if(!loadOn()||S.unb)return;for(const P of allPilots()){if(!P)continue;if(P.docked&&P.docked!=='turret'){P.bdUsed=0;P.lpN=0}
    if(!isScoutCls(P.cls))continue;const n=smxN(P,'lrack');if(!n){P.limpetUsed=true;P._lpW=true;continue}
    if(P.limpetUsed&&!P._lpW){P.lpN=(P.lpN||0)+1;if(P.lpN<n)P.limpetUsed=false}if(P.docked&&P.docked!=='turret')P.limpetUsed=false;P._lpW=P.limpetUsed}}
// ---- 2. comets and derelicts logged and sold to the Compact
function smxFindTick(){if(!W||NET.cl||S.unb||S.training)return;const s=S.sectors[W.sid];if(!s)return;const objs=[...s.ast.filter(a=>a.comet).map(a=>({o:a,k:'comet',key:'c'+a.id,until:(S.events.find(v=>v.type==='comet'&&v.sector===W.sid)||{}).until||S.T+200})),...s.crates.filter(c=>c.derelict).map(c=>({o:c,k:'derelict',key:'d'+c.id,until:c.until}))];if(!objs.length)return;
  for(const e of W.ents){if(e.type!=='ship'||!e.alive)continue;const P=e.isPlayer?S.player:e.rp?S.pilots&&S.pilots[e.rp]:null;if(!P||P.docked)continue;const R=fitHas(P,'scanner')?SMX.findScan:SMX.findR;
    for(const x of objs){P.finds=P.finds||{};if(P.finds[x.key]||d3(e,x.o)>R)continue;const pay=x.k==='comet'?Math.max(SMX.cometMin,Math.round(oreTotal(x.o)*SMX.cometCr)):Math.max(SMX.derMin,Math.round(invValue(x.o.inv)*SMX.derK));
      P.finds[x.key]={k:x.k,sid:W.sid,until:x.until,pay};keyFeed(e.isPlayer?'me':e.rp,`🔭 ${x.k==='comet'?'Comet':'Derelict'} logged in ${DEF[W.sid].name}: sell the find as intel at any freeport (${fmt(pay)} cr) while it lasts.`,'good')}}}
{const o=worldUpdate;worldUpdate=function(dt){const r=o.apply(this,arguments);try{if(W&&!NET.cl){W._smx=(W._smx||0)-dt;if(W._smx<=0){W._smx=1;smxFindTick();smxRigTick()}}}catch(err){console.error(err)}return r}}
{const o=jobsList;jobsList=function(c,P,srcs){const out=o.apply(this,arguments);try{if(S.unb||!c||c.owner!=='neutral'||c.kind!=='station')return out;for(const key in P.finds||{}){const F=P.finds[key];if(F.sold||S.T>F.until){if(S.T>F.until)delete P.finds[key];continue}
    out.push({id:'find:'+key,by:'neutral',sid:F.sid,ty:'scout',title:`Intel: a ${F.k} in ${esc(DEF[F.sid].name)}`,sub:`${Math.max(0,Math.round((F.until-S.T)/60))} min before it's gone`,hops:0,where:'here',payN:F.pay,pay:`${fmt(F.pay)} cr`,btn:['findsell',key,`Sell to the Compact · +${fmt(F.pay)} cr`],
      detail:()=>`<p class="note" style="margin:0">The Compact pays for word of a ${F.k} while it lasts, to send its own ${F.k==='comet'?'prospectors':'salvagers'}. You can still work it yourself.</p>`})}}catch(err){console.error(err)}return out}}
// ---- 3. embargo contraband by origin
function origSync(P){if(!P||!P.orig)return;for(const k in P.orig){const have=(P.cargo[k]||0)+((P.vault||{})[k]||0),t=P.orig[k];let tot=0;for(const f in t)tot+=t[f];if(tot>have){const r=tot?have/tot:0;for(const f in t){t[f]=Math.floor(t[f]*r);if(!t[f])delete t[f]}}if(!Object.keys(t).length)delete P.orig[k]}}
function embargoed(f,g){return f!==g&&FAC_IDS.includes(f)&&FAC_IDS.includes(g)&&!!(pairOf(f,g)||{}).emb}
{const o=dockAction;dockAction=function(act,arg){if(act==='findsell'){const P=S.player,F=P.finds&&P.finds[arg],c=dockCtx();if(!F||F.sold||S.T>F.until){dockErr='That find is stale.';return}if(!c||c.owner!=='neutral'){dockErr='Sell finds at a freeport.';return}const got=payTo(P,'neutral',F.pay);F.sold=1;dockErr=`✓ The Compact pays ${fmt(got)} cr for word of the ${F.k} in ${DEF[F.sid].name}.`;return}
  if(act==='buy'&&!S.unb){const c=dockCtx(),P=S.player,k=String(arg).split(':')[0];if(c&&FAC_IDS.includes(c.owner)){const n0=P.cargo[k]||0;const r=o.apply(this,arguments);const d=(P.cargo[k]||0)-n0;if(d>0){P.orig=P.orig||{};const t=P.orig[k]=P.orig[k]||{};t[c.owner]=(t[c.owner]||0)+d}return r}}
  return o.apply(this,arguments)}}
{const o=contraFor;contraFor=function(P,f){const L=o.apply(this,arguments);try{origSync(P);for(const k in P.orig||{}){if(L.some(x=>x.k===k))continue;let n=0;for(const g in P.orig[k])if(embargoed(f,g))n+=P.orig[k][g];n=Math.min(n,P.cargo[k]||0);if(n>0)L.push({k,n,why:'embargo'})}}catch(e){}return L}}
SM.heat.embargo=SMX.embHeat;
// ---- 4. the Rift Shard as a wild card
function riftCover(k){const c=comp(k),D=S.drift||{};return RAWS.every(e=>(D[e]||0)>=c[e]-1e-9)}
function riftSwap(k,srcs){const c=comp(k),s=comp('riftshard');takeFrom({riftshard:1},srcs);S.drift=S.drift||{};for(const e of RAWS){S.drift[e]=(S.drift[e]||0)+s[e]-c[e]}}
{const o=dockAction;dockAction=function(act,arg){if(act==='make'&&!S.unb&&loadOn()){const c=dockCtx(),P=S.player;const[k]=String(arg).split(':'),I=ITEMS[k];if(c&&I&&I.recipe&&k!=='riftshard'){const st=c.storage||P.vault,srcs=[P.cargo,st].filter(Boolean),r=I.recipe;
    const lack=Object.keys(r).filter(x=>countIn(x,srcs)<r[x]);if(lack.length===1&&r[lack[0]]-countIn(lack[0],srcs)===1&&countIn('riftshard',srcs)>=1&&riftCover(lack[0])&&!(lack[0]==='riftshard')){
      riftSwap(lack[0],srcs);inv.add(P.cargo,lack[0],1);const r2=o.call(this,act,`${k}:1`);if(String(dockErr).startsWith('✓'))dockErr+=` A Rift Shard stood in for the ${ITEMS[lack[0]].name}.`;else{inv.take(P.cargo,lack[0],1);dockErr+=' (the shard was spent)'}return r2}}}
  if(act==='pupr'){const c=dockCtx(),P=S.player;const srcs=[P.cargo,(c&&c.storage)||P.vault];if(countIn('riftshard',srcs)<1){dockErr='No Rift Shard on hand.';return}dockAction('pup',arg);if(!String(dockErr).startsWith('✓'))return;
    const[g,i0]=String(arg).split(':'),F=fitOf(P),kind=(g==='w'?F.w:F.u)[+i0];takeFrom({riftshard:1},srcs);const s=comp('riftshard');S.drift=S.drift||{};for(const e of RAWS)S.drift[e]=(S.drift[e]||0)+s[e];
    const St=BR.step[kind];if(!St){dockErr+=' The shard burned out: that part takes no trait.';return}const keys=Object.keys(St).filter(t=>t!=='speed'),t=pick(keys),good=Math.random()<SMX.riftGood,steps=good?ri(1,2):-1,v=Math.round(steps*St[t][0]*St[t][1]*1000)/1000;
    F.rt=F.rt||{};F.rt[g+i0]={k:kind,tr:{[t]:v}};dockErr+=` The Rift Shard left a trait: ${trText({[t]:v})}.`;return}
  return o.apply(this,arguments)}}
// a rift trait counts with the part's maker trait
{const o=mkTr;mkTr=function(P,kind,key,sum){const v=o.apply(this,arguments);try{const F=fitOf(P);if(!F.rt)return v;let s=0,n=0;const cnt=(arr,g)=>arr.forEach((k,i)=>{if(k!==kind)return;n++;const R=F.rt[g+i];if(R&&R.k===kind&&R.tr[key])s+=R.tr[key]});cnt(F.w,'w');cnt(F.u,'u');if(!s)return v;return v+(sum?s:n?s/n:0)}catch(e){return v}}}
{const o=fitMigrate;fitMigrate=function(P,F){F.rt={};return o.apply(this,arguments)}}
{const o=dockClick;dockClick=function(act,arg){if(act==='findsell'||act==='pupr'){if(NET.cl){netSend({t:'act',act,arg});return}dockAction(act,arg);renderDock();return}return o.apply(this,arguments)}}
// the Loadout section: upgrade with a Rift Shard, and the traits shards have left
{const o=loadoutHtml;loadoutHtml=function(c,P){let h=o.apply(this,arguments);try{if(!loadOn())return h;const F=fitOf(P),srcs=[P.cargo,c.storage||P.vault],n=countIn('riftshard',srcs),rows=[];
  F.w.forEach((k,i)=>{if(k)rows.push(['w',i,k,F.g[i]||1])});F.u.forEach((k,i)=>{if(k)rows.push(['u',i,k,F.ug[i]||1])});const has=rows.filter(r=>F.rt&&F.rt[r[0]+r[1]]);
  if(!n&&!has.length)return h;h+=`<div class="h3" style="margin-top:14px">Rift Shards</div><p class="note" style="margin:0 0 6px">A Rift Shard fed into a part's upgrade leaves a random trait (most often a strength; taking the part out loses it). At a workshop, a shard also stands in for one missing component. You have ${n}.</p>`;
  for(const r of rows){const R=F.rt&&F.rt[r[0]+r[1]],q=pupQuote(c,P,`${r[0]}:${r[1]}`),nm=ITEMS[PART[r[2]]]?ITEMS[PART[r[2]]].name:r[2];if(!R&&!q)continue;
    h+=`<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:3px 0"><span class="note" style="margin:0;min-width:160px">${esc(nm)} · grade ${r[3]}</span>${R?`<span class="req ok">${esc(trText(R.tr))}</span>`:''}${q&&n?`<button class="btn sm" type="button" data-act="pupr" data-arg="${r[0]}:${r[1]}" ${haveIn(q.r,srcs)&&P.credits>=q.fee?'':'disabled'}>To grade ${q.t} with a Rift Shard</button>`:''}</div>`}}catch(err){console.error(err)}return h}}
// the free Light Miner starts with a mining laser and its charge launcher, not a machine gun (user, 3 Nov 2026)
HULL_SLOTS.skiff.w=['mlaser','charge'];
{const o=newGame;newGame=function(){const r=o.apply(this,arguments);try{const P=S&&S.player;if(P&&P.cls==='skiff'&&fitOf(P).w.includes('mlaser'))P.mtool='mlaser'}catch(e){}return r}}
{const o=newPilot;newPilot=function(pid){const r=o.apply(this,arguments);try{const P=S.pilots&&S.pilots[pid];if(P&&P.cls==='skiff'&&fitOf(P).w.includes('mlaser'))P.mtool='mlaser'}catch(e){}return r}}
