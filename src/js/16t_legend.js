//@src 16t_legend.js
// ============================================================ Legend, reworked for Beyond (stage 14)
// Legend points are earned for what you build and achieve in a galaxy (each once per galaxy), kept per callsign on the device:
// Rating 5 (1) and Rating 10 (1 more), a Lair (1), a Depot (1), a Station (2), declaring a faction (2), an ace or a Brood Hive
// Ship (1), your faction winning the galaxy (6), being allied with the winner (3). When the Brood wins, nobody scores the win.
// Legend levels (2, 4, 7, 10, 14, 18, 23, 28, 34, 40 points) unlock perks; each new galaxy you pick a start package from the
// unlocked perks, each costing its level in start points, with your level as the budget. One Rating perk, one base perk.
// Winning gives Conqueror's spoils for the next galaxy: your flagship, a war chest, three veteran crews, Renown, the Wraith.
// Driftgate 1's Legend perks (scout, freight, miner bonuses and the rest) no longer apply.
const LEGB={lv:[2,4,7,10,14,18,23,28,34,40],pts:{r5:1,r10:1,lair:1,depot:1,station:2,declare:2,ace:1,win:6,ally:3},chestMax:25000,chestK:.1,vetT:7200};
const LEGB_PERKS=[null,
  {k:'r2',name:'Start at Rating 2',title:'Journeyman',grp:'rating'},{k:'cr',name:'+5,000 starting credits'},{k:'med',name:'Start in a fully equipped medium hull'},
  {k:'g2',name:'Three grade 2 parts, fitted free'},{k:'r4',name:'Start at Rating 4',title:'Veteran',grp:'rating'},{k:'lair',name:'A Lair kit: build a level 1 Lair anywhere, without materials',grp:'base'},
  {k:'trust',name:'House-brand hulls need only Trusted standing'},{k:'depot',name:'Start with a level 1 Depot',grp:'base'},{k:'r6',name:'Start at Rating 6',grp:'rating'},
  {k:'station',name:'Start with a level 1 Station',title:'Founder',grp:'base'}];
function legbLevel(pts){let l=0;for(let i=0;i<LEGB.lv.length;i++)if((pts||0)>=LEGB.lv[i])l=i+1;return l}
function legbTitle(l){let t='';for(let i=1;i<=l;i++)if(LEGB_PERKS[i].title)t=LEGB_PERKS[i].title;return t}
// a valid start package from the levels picked: within the budget, one Rating perk, one base perk
function legbPkg(picks,lvl){const out=[];let cost=0;const grp={};for(const i of[...new Set((picks||[]).map(Number))].sort((a,b)=>b-a)){const pk=LEGB_PERKS[i];if(!pk||i>lvl||cost+i>lvl)continue;if(pk.grp&&grp[pk.grp])continue;if(pk.grp)grp[pk.grp]=1;cost+=i;out.push(i)}return out}
// award points to the local pilot's record, once per galaxy per achievement
function legbAward(P,key,why){if(!P||!S||S.training||NET.cl&&P!==S.player)return;const k=pkeyOf(P);if(!(P===S.player||isMe(k)))return;S.legGot=S.legGot||{};const id=k+':'+key;if(S.legGot[id])return;S.legGot[id]=1;
  const n=LEGB.pts[key]||0;if(!n||!P.name)return;const d=legLoad(),r=legRec(P.name,d);if(!r)return;const l0=legbLevel(r.bp||0);r.bp=(r.bp||0)+n;const l1=legbLevel(r.bp);legSave(d);
  feed(`✦ Legend +${n} (${why}): ${r.bp} point${r.bp===1?'':'s'}${l1>l0?` · level ${l1}: ${LEGB_PERKS[l1].name}`:''}.`,'good')}
{const o=rpAdd;rpAdd=function(P,n,why){const r0=ratingOf(P);const r=o.apply(this,arguments);const r1=ratingOf(P);if(r0<5&&r1>=5)legbAward(P,'r5','Rating 5');if(r0<10&&r1>=10)legbAward(P,'r10','Rating 10');return r}}
{const o=lairMake;lairMake=function(P){const r=o.apply(this,arguments);legbAward(P,'lair','your first Lair');return r}}
{const o=depMake;depMake=function(P){const r=o.apply(this,arguments);legbAward(P,'depot','your first Depot');return r}}
{const o=staUp;staUp=function(P){const r=o.apply(this,arguments);if(String(r).startsWith('✓'))legbAward(P,'station','your first Station');return r}}
{const o=declare;declare=function(P){const r=o.apply(this,arguments);if(String(r).startsWith('✓'))legbAward(P,'declare','declaring a faction');return r}}
{const o=killShip;killShip=function(e,src,at){const ace=e&&e.alive&&(e.aceId||e.side==='brood'&&(e.cls==='carrier'||e.role==='frigate'&&isCar(e.tok||{})));const r=o.apply(this,arguments);try{if(ace&&(src==='player'||at&&(at.src===W.player)))legbAward(S.player,'ace','an ace or Hive Ship')}catch(err){}return r}}
// the galaxy ends: the win and the allied win; spoils for the winners
{const o=legAward;legAward=function(side){if(!S||S.training||S.unb)return o.apply(this,arguments);const P=S.player;if(!P||!P.name)return;
  if(side==='player'&&P.decl){legbAward(P,'win','your faction won the galaxy');const d=legLoad(),r=legRec(P.name,d);if(r){r.spoils={flag:{cls:P.cls,fit:JSON.parse(JSON.stringify(fitOf(P)))},chest:Math.min(LEGB.chestMax,Math.round(P.credits*LEGB.chestK)),vets:3,renown:25,wraith:1};legSave(d)}}
  else if(side&&side!=='brood'&&P.allied&&P.allied[side]){legbAward(P,'ally','allied with the winner');const d=legLoad(),r=legRec(P.name,d);if(r){r.spoils={chest:Math.min(LEGB.chestMax/2,Math.round(P.credits*LEGB.chestK/2)),vets:1,renown:12};legSave(d)}}}}
// the start package and spoils, applied as the galaxy (or the pilot) is made, before its ledger baseline
{const o=legPack;legPack=function(name){const pk=o.apply(this,arguments);const r=legPeek(name)||{};const lvl=legbLevel(r.bp||0);pk.blvl=lvl;pk.pkg=legbPkg(r.pkg||[],lvl);pk.medCls=r.medCls||'striker';pk.spoils=r.spoils||null;return pk}}
{const o=legendStart;legendStart=function(P,pk){if(S&&S.unb)return o.apply(this,arguments);pk=pk||{};P.lvl=0;P.tune=P.tune||{};P.tune.lv=0;const has=k=>(pk.pkg||[]).some(i=>LEGB_PERKS[i].k===k);P.legPkg=(pk.pkg||[]).slice();P.legTitle=legbTitle(pk.blvl||0);
  if(has('r2'))P.rp=Math.max(P.rp||0,RATING.need[2]);if(has('r4'))P.rp=Math.max(P.rp||0,RATING.need[4]);if(has('r6'))P.rp=Math.max(P.rp||0,RATING.need[6]);if(has('cr'))P.credits+=5000;
  if(has('med')){const c=['striker','prospector','freighter'].includes(pk.medCls)?pk.medCls:'striker';P.cls=c;P.rack=rackCapC(c,P.tiers.weapon);P.swarm=CLASSES[c].swarm||0;P.bay={drone:CLASSES[c].drones||0}}
  if(has('trust'))P.trustBrand=1;if(has('lair'))P.lairKit=1;if(has('depot'))P.startBase='depot';if(has('station'))P.startBase='station';if(has('g2'))P.startG2=3;
  const sp=pk.spoils;if(sp){P.spoils=sp;if(sp.flag&&legValidCls(sp.flag.cls,10)){P.cls=sp.flag.cls;P.fit=sp.flag.fit;P.fit.cls=P.cls}if(sp.chest)P.credits+=sp.chest;if(sp.vets)P.vets=sp.vets;if(sp.renown)for(const f of FAC_IDS)P.stand[f]=Math.max(P.stand[f]||0,sp.renown);if(sp.wraith)P.wraith=1}
  P.lvl=0}}
// after the default fit exists: grade 2 parts and a starting base, then the baseline is taken again; spoils are used up
function legbFinish(P){if(!P||S.training||S.unb)return;let ch=0;if(P.startG2){const F=fitOf(P);let n=P.startG2;F.w.forEach((k,i)=>{if(k&&n>0){F.g[i]=Math.max(F.g[i]||1,2);n--}});P.startG2=0;ch=1}
  if(P.startBase){const home=P.home||P.sector;let best=null,bh=99;for(const d of SECTOR_DEFS){if(!depCan(d.id))continue;const h=HOP[home]&&HOP[home][d.id];if(h!=null&&h>=1&&h<bh){bh=h;best=d.id}}
    if(best){const R=depMake(P,best,stationSite(best),{...DEP.cost},{});if(P.startBase==='station'){inv.addAll(R.fort,STA.cost);R.pst=1;R.bld=[];R.hMax=Math.round(R.hMax*STA.hK);R.sMax=Math.round(R.sMax*STA.hK);R.hull=R.hMax;R.shield=R.sMax;R.name=`${DEF[best].name} Station`}
      feed(`✦ Legend start: your ${P.startBase==='station'?'Station':'Depot'} stands in ${DEF[best].name}.`,'good')}P.startBase=null;ch=1}
  if(P.spoils){if(P===S.player){const d=legLoad(),r=legRec(P.name,d);if(r){delete r.spoils;legSave(d)}}feed('✦ Conqueror\'s spoils carried into this galaxy.','good');P.spoils=null}return ch}
{const o=newGame;newGame=function(){const r=o.apply(this,arguments);try{if(S&&S.player&&legbFinish(S.player)){const l=ledger();S.ledger0={tot:l.tot,credits:l.credits}}}catch(err){console.error(err)}return r}}
{const o=newPilot;newPilot=function(pid){const r=o.apply(this,arguments);try{const P=S.pilots&&S.pilots[pid];if(P)devLedger(()=>legbFinish(P))}catch(err){}return r}}
// perk effects in play
{const o=lairSpot;lairSpot=function(P){const r=o.apply(this,arguments);if(P&&P.lairKit&&r.a&&r.why&&r.why.startsWith('You need'))return{a:r.a};return r}}
{const o=lairMake;lairMake=function(P,a){if(P&&P.lairKit&&!haveIn(LAIR_B.cost,[P.cargo])){P.lairKit=0;const keep={...LAIR_B.cost};for(const k in LAIR_B.cost)LAIR_B.cost[k]=0;try{return o.apply(this,arguments)}finally{Object.assign(LAIR_B.cost,keep)}}return o.apply(this,arguments)}}
{const o=sigOK;sigOK=function(c,P){if(o.apply(this,arguments))return true;return!!P&&P.trustBrand&&!!c&&FAC_IDS.includes(c.owner)&&c.owner===P.faction&&standOf(c.owner,P)>25}}
{const o=crewHire;crewHire=function(R,P,cls){if(!(P&&P.vets>0))return o.apply(this,arguments);const add=1e9;P.credits+=add;LEGB.free=1;let r;try{r=o.apply(this,arguments)}finally{LEGB.free=0;P.credits-=add}
  if(String(r).startsWith('✓')){P.vets--;const c=R.crew[R.crew.length-1];c.vet=S.T+LEGB.vetT;r+=' A veteran: no hire cost, and no wages for two hours.'}return r}}
{const o=payFrom;payFrom=function(P,to,n){if(LEGB.free)return 0;return o.apply(this,arguments)}}
{const o=crewTick;crewTick=function(){const saved=[];for(const R of Object.values(S.stations||{}))for(const c of(R&&R.crew)||[])if(c.vet>S.T){saved.push([c,c.owe||0]);c.owe=-1e9}try{return o.apply(this,arguments)}finally{for(const[c,ow]of saved)c.owe=ow}}}
{const o=hullRatingOK;hullRatingOK=function(P,k){if(k==='wraith')return!!(P&&P.wraith);return o.apply(this,arguments)}}
// ---- the leaderboard by Legend level, the start package and the spoils (start screen)
{const o=legRows;legRows=function(){return o.apply(this,arguments).sort((a,b)=>(b.bp||0)-(a.bp||0)||String(a.name).localeCompare(b.name))}}
function legSetB(k,v){const me=cleanCall($('mpName').value);if(!me)return;const d=legLoad(),r=legRec(me,d);if(k.startsWith('pk')){const i=+k.slice(2);r.pkg=(r.pkg||[]).filter(x=>x!==i);if(v)r.pkg.push(i);r.pkg=legbPkg(r.pkg,legbLevel(r.bp||0))}else if(k==='medCls')r.medCls=v;legSave(d)}
{const o=legSet;legSet=function(k,v){if(String(k).startsWith('pk')||k==='medCls'){legSetB(k,v);return}return o.apply(this,arguments)}}
{const o=legHtml;legHtml=function(){const me=cleanCall($('mpName').value),rows=legRows();
  let h=`<div class="h3">Leaderboard</div><p class="note" style="margin:0 0 8px">Ranked by Legend level. Legend points come from what you build and achieve in each galaxy: Rating 5 and 10, your first Lair, Depot and Station, declaring a faction, an ace or a Hive Ship, and your faction winning (6) or being allied with the winner (3). Kept on this device.</p>`;
  h+=rows.length?`<table class="lgt"><tr><th>#</th><th>Pilot</th><th>Level</th><th>Points</th><th>Title</th></tr>${rows.map((x,i)=>{const l=legbLevel(x.bp||0);return`<tr${legKey(x.name)===legKey(me)?' class="me"':''}><td>${i+1}</td><td>${esc(x.name)}</td><td>${l}</td><td>${x.bp||0}</td><td>${esc(legbTitle(l)||'—')}</td></tr>`}).join('')}</table>`:'<p class="note">No pilots yet.</p>';
  if(!me)return h+`<p class="note" style="margin-top:12px">Enter your callsign (step 1) to choose your start package.</p>`;
  const r=legPeek(me)||{},lvl=legbLevel(r.bp||0),pkg=legbPkg(r.pkg||[],lvl),spent=pkg.reduce((a,b)=>a+b,0);
  h+=`<div class="h3" style="margin-top:16px">${esc(me)} · level ${lvl}${legbTitle(lvl)?' · '+esc(legbTitle(lvl)):''}</div><p class="note" style="margin:0 0 8px">${r.bp||0} Legend point${(r.bp||0)===1?'':'s'}${lvl<10?` · ${LEGB.lv[lvl]-(r.bp||0)} more to level ${lvl+1}`:' · top level'}. Start package: ${spent} of ${lvl} start point${lvl===1?'':'s'} spent (each perk costs its level; one Rating perk, one base perk).</p><div class="lgs">`;
  for(let i=1;i<=10;i++){const pk=LEGB_PERKS[i],on=pkg.includes(i);h+=`<label style="${i>lvl?'opacity:.45':''}"><input type="checkbox" data-lg="pk${i}"${on?' checked':''}${i>lvl?' disabled':''}> ${i}. ${esc(pk.name)}${pk.title?` · title ${esc(pk.title)}`:''}</label>`}
  h+=`</div>`;if(pkg.includes(3))h+=`<label class="note">Medium hull <select data-lg="medCls">${[['striker','Medium Fighter'],['prospector','Medium Miner'],['freighter','Medium Hauler']].map(([v,n])=>`<option value="${v}"${(r.medCls||'striker')===v?' selected':''}>${n}</option>`).join('')}</select></label>`;
  if(r.spoils)h+=`<div class="h3" style="margin-top:14px">Conqueror's spoils for your next galaxy</div><p class="note">${[r.spoils.flag?`your flagship (${esc(CLASSES[r.spoils.flag.cls]?CLASSES[r.spoils.flag.cls].name:r.spoils.flag.cls)})`:'',r.spoils.chest?`a ${fmt(r.spoils.chest)} cr war chest`:'',r.spoils.vets?`${r.spoils.vets} veteran crew${r.spoils.vets>1?'s':''}`:'',r.spoils.renown?`Renown (+${r.spoils.renown} with every power)`:'',r.spoils.wraith?'the Wraith':''].filter(Boolean).join(', ')}.</p>`;
  h+=`<div style="margin-top:14px"><button type="button" class="btn sm" data-lgact="reset">${legResetArm?'Click again to erase '+esc(me)+'’s legend':'Reset my legend'}</button></div>`;return h}}
