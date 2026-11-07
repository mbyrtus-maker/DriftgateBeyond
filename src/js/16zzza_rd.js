//@src 16zzza_rd.js
// ============================================================ Beyond: the corporate economy, stage 2: grades by invention (7 Nov 2026)
// The user (7 Nov 2026): "R&D replaces Mk upgrades." From "Corporate R&D: grades by invention" in BEYOND_DESIGN.md.
//   - No upgrades in place: a part or a system no longer goes up a grade at a dock. A better part is a higher grade bought
//     from the maker that invented it. (Training keeps the old upgrades.)
//   - Systems are parts: drives, reactors, shield emitters, fire control, armour, blast rigs, cargo holds and payload bays
//     are made by makers too (the line-up of simulation v10), in grades 1 to 5. Installing one at a dock (Loadout, the system)
//     swaps it for the one in the ship, which goes to your hold or hangar as a part you can sell or install elsewhere. The
//     systems ships came with are unbranded.
//   - Every line of parts starts at grade 1; a maker raises a line a grade through R&D. Its works then build that grade only,
//     and the old grade is retired: its unsold stock, wherever it is, is broken back into raw ore at that station.
//   - R&D (one project at a time per maker): a line that keeps losing (bought less than half its fair share after its two
//     tweaks, or a system line straight away), or one a rival has out-graded and is outselling, gets a project for its next
//     grade when the maker can fund it with 3 hours of running costs to spare (Innovator: 1; Cautious: 6). Funding (G2 750,
//     G3 2,000, G4 4,500, G5 9,000 cr) builds the grade's lab, paid to the host station's owner; then design (G2 15, G3 30,
//     G4 45, G5 60 minutes), materials (the prototype's components bought from the host's market, 10 to 20 minutes), trials
//     (5 to 15 minutes), and the launch: the prototype is the first unit on the shelf.
//   - Contractor Rating still gates the grades you may fit or install; the powers' refits buy up to one grade above their tech.
//   - The ledger stays exact: a grade-g part's recipe is the part plus its grade components, the same as a part upgraded in
//     place, so fitting one, taking it out or installing a system only moves goods.
const RD={cost:{2:750,3:2000,4:4500,5:9000},design:{2:900,3:1800,4:2700,5:3600},mat:[600,1200],trial:[300,900],spare:3,lose:.5};
const SYS_LINES={engine:['tcy','ewd','cr'],power:['ad','sw','ewd'],shield:['ad','bl','cr'],weapon:['wf','sw','mg'],armor:['tcy','hf','qs'],cargo:['hf','qs','cp'],drill:['hf','cp'],payload:['wf','mwa']};
const SYS_TASTE={halcyon:{shield:1.5,engine:1.4,cargo:1.2},varkesh:{armor:1.5,weapon:1.5,drill:1.3},ostrova:{power:1.6,weapon:1.2,shield:1.1}};
function rdGid(id,g){return g>1?`${id}_g${g}`:id}
// ---- graded parts: every maker part line in grades 2 to 5 (landing kits and beacons have no grades)
(function(){for(const m in MK_LINE)for(const id of MK_LINE[m].slice()){const I=ITEMS[id];if(!I||!I.part||I.part==='land'||I.part==='claim')continue;
    for(let g=2;g<=5;g++){const gid=rdGid(id,g),rc={...I.recipe};for(let t=2;t<=g;t++)for(const k in partUpg(t))rc[k]=(rc[k]||0)+partUpg(t)[k];
      ITEMS[gid]={name:`${I.name} G${g}`,recipe:rc,col:I.col,part:I.part,maker:m,grade:g,base:id,tr:I.tr,trTxt:I.trTxt};ITEM_ORDER.push(gid);(MK_ITEMS[I.part]=MK_ITEMS[I.part]||[]).push(gid)}}
  // systems as parts: the makers' lines, and the unbranded systems ships come with
  const SYSN={engine:'drive',power:'reactor',shield:'shield emitter',weapon:'fire control',armor:'armour',drill:'blast rig',cargo:'cargo hold',payload:'payload bay'};
  for(const sl in SYS_LINES){for(let g=1;g<=5;g++){const id=`sy_${sl}`,gid=rdGid(id,g);ITEMS[gid]={name:`${SLOT[sl].name} G${g} (unbranded)`,recipe:compInv(sl,g),col:'#9fb3d8',sys:sl,grade:g,base:id,trTxt:'Unbranded: the system a ship came with.'};ITEM_ORDER.push(gid)}
    for(const m of SYS_LINES[sl]){const id=`sy_${m}_${sl}`;for(let g=1;g<=5;g++){const gid=rdGid(id,g);ITEMS[gid]={name:`${MAKERS[m].short} ${SYSN[sl]}${g>1?' G'+g:''}`,recipe:compInv(sl,g),col:'#9fb3d8',sys:sl,grade:g,base:id,maker:m,tr:{},trTxt:`${MAKERS[m].name}: ${SYSN[sl]}, grade ${g}.`};ITEM_ORDER.push(gid)}
      MK_LINE[m].push(id);CE_DEF.it[id]={name:ITEMS[id].name,tr:{}}}}
  for(const m in MK_LINE)for(const id of MK_LINE[m])for(let g=2;g<=5;g++){const gid=rdGid(id,g);if(ITEMS[gid]&&!CE_DEF.it[gid])CE_DEF.it[gid]={name:ITEMS[gid].name,tr:ITEMS[gid].tr||{}}}})();
function rdLineG(m,id){const c=ceOf(m);return(c&&c.g&&c.g[id])||1}
function rdOn(){return!!(S&&S.corp&&!S.training)}
// names and traits follow the line (a tweak or a new company)
const RD_SYSN={engine:'drive',power:'reactor',shield:'shield emitter',weapon:'fire control',armor:'armour',drill:'blast rig',cargo:'cargo hold',payload:'payload bay'};
{const o=ceApply;ceApply=function(){o.apply(this,arguments);for(const m in MK_LINE)for(const id of MK_LINE[m]){const B=ITEMS[id];if(B.sys)B.trTxt=`${MAKERS[m].name}: ${RD_SYSN[B.sys]}, grade 1.`;
  for(let g=2;g<=5;g++){const G=ITEMS[rdGid(id,g)];if(!G)continue;G.tr=B.tr;G.trTxt=B.sys?`${MAKERS[m].name}: ${RD_SYSN[B.sys]}, grade ${g}.`:B.trTxt;G.name=`${B.name} G${g}`}}}}
// ---- no upgrades in place
{const o=pupQuote;pupQuote=function(){return rdOn()?null:o.apply(this,arguments)}}
{const o=dockAction;dockAction=function(act,arg){if(rdOn()&&(act==='upg'||act==='bupg'||act==='pup'||act==='pupr')){dockErr='Upgrades in place are gone: a better part or system is a higher grade bought from the maker that invented it (Market), then fitted or installed (Loadout).';return}
  if(rdOn()&&act==='sysfit'){dockErr=rdSysFit(String(arg));return}
  if(rdOn()&&act==='make'){const I=ITEMS[String(arg).split(':')[0]];if(I&&(I.maker||I.sys)){dockErr=`Only its maker builds the ${I.name}.`;return}}return o.apply(this,arguments)}}
// fitting a graded part: it goes in as its line's part at that grade (and comes out again as the graded part)
{const o=fitDo;fitDo=function(c,P,arg){const[g,i0,k]=String(arg).split(':'),G=k&&ITEMS[k];if(!G||!G.grade||G.grade<2||!G.base||G.sys)return o.apply(this,arguments);
  if(typeof gradeCap==='function'&&!S.unb&&G.grade>gradeCap(P))return`Your Contractor Rating allows grade ${gradeCap(P)} parts: the ${G.name} is grade ${G.grade}.`;
  const st=c.storage||P.vault,srcs=[P.cargo,st];if(countIn(k,srcs)<1)return`No ${G.name} in your hold or hangar.`;
  // unpack it into its line's part and its grade components, fit the part, then set the slot's grade (taking the components)
  takeFrom({[k]:1},srcs);const up={};for(let t=2;t<=G.grade;t++)inv.addAll(up,partUpg(t));inv.add(st,G.base,1);inv.addAll(st,up);
  const r=o.call(this,c,P,`${g}:${i0}:${G.base}`);const F=fitOf(P),ws=g==='w',ids=ws?F.wi:F.ui,gr=ws?F.g:F.ug;
  if(ids&&(ids[+i0]===G.base)&&(gr[+i0]||1)===1&&haveIn(up,[st])){takeFrom(up,[st]);gr[+i0]=G.grade;if(W&&W.player)refreshPlayerStats();return`✓ ${G.name} fitted${/; the /.test(r)?r.slice(r.indexOf(';')):'.'}`}
  // it didn't go in: pack it back up
  if(countIn(G.base,[st])>0&&haveIn(up,[st])){takeFrom({[G.base]:1},[st]);takeFrom(up,[st]);inv.add(st,k,1)}return r}}
{const o=partToStore;partToStore=function(st,k,g,it){const base=it||PART[k],gid=rdGid(base,g||1);if(rdOn()&&(g||1)>1&&ITEMS[gid]&&ITEMS[gid].grade===g){inv.add(st,gid,1);return}return o.apply(this,arguments)}}
// ---- installing a system: swap it for the one in the ship
function rdSysFit(arg){const[sl,id]=arg.split(':'),I=ITEMS[id],c=dockCtx(),P=S.player;if(!c||!I||I.sys!==sl||!SLOT[sl])return'That isn\'t a system for that slot.';
  if(sl==='drill'&&typeof blHull==='function'&&!blHull(P.cls))return'This hull has no blast rig.';
  if(typeof gradeCap==='function'&&I.grade>gradeCap(P))return`Your Contractor Rating allows grade ${gradeCap(P)} systems: the ${I.name} is grade ${I.grade}.`;
  const st=c.storage||P.vault,srcs=[P.cargo,st];if(countIn(id,srcs)<1)return`No ${I.name} in your hold or hangar.`;
  const t=P.tiers[sl]||1,m=(P.sysm||{})[sl],outId=rdGid(m?`sy_${m}_${sl}`:`sy_${sl}`,t),out=ITEMS[outId]?outId:rdGid(`sy_${sl}`,t);
  takeFrom({[id]:1},srcs);if(Object.keys(ITEMS[out].recipe).length)inv.add(st,out,1);P.tiers[sl]=I.grade;(P.sysm=P.sysm||{})[sl]=I.maker||null;if(W&&W.player)refreshPlayerStats();
  return`✓ ${I.name} installed; the ${ITEMS[out].name} went to your ${String(c.storageName||'vault').toLowerCase()}.`}
// ---- the works build each line's current grade
makersTick=(function(o){return function(){if(!rdOn())return o.apply(this,arguments);if(NET.cl||!S||S.training||S.unb)return;S.mkT=S.mkT||0;if(S.T<S.mkT)return;S.mkT=S.T+MK_WORKS.every;
  if(!S.corpConv){try{corpConvert()}catch(e){}S.corpConv=1}
  for(const m in MAKERS){const R=mkAtHome(m);if(!R||!ceAlive(m))continue;const st=mkStock(R),gidOf=id=>rdGid(id,rdLineG(m,id)),want=id=>Math.min(CE.cap,CE.shelf+ceSold(m,id,3600));
    const ids=MK_LINE[m].filter(id=>{const gid=gidOf(id);return ITEMS[gid]&&Object.keys(ITEMS[gid].recipe).length&&(st[gid]||0)<want(id)&&!(S.T>CE.shut&&!ceSold(m,id,CE.shut)&&(st[gid]||0)>0)}).sort((a,b)=>(st[gidOf(a)]||0)/want(a)-(st[gidOf(b)]||0)/want(b));
    for(const id of ids){const gid=gidOf(id),rc=ITEMS[gid].recipe;rdCraftFor(st,rc);if(!haveIn(rc,[st]))continue;const cost=Math.ceil(ceComp(R.sid,gid));if(ceT(m)-cost<ceReserve(m))continue;
      transfer(ceW(m),R.owner==='neutral'?'neutral':R.owner,cost);ceOf(m).cost+=cost;takeFrom(rc,[st]);inv.add(st,gid,1);break}}}})(makersTick);
// a grade's inputs the station doesn't stock (Calibration Matrices, lattices, cores) are made in the works from what it does
function rdCraftFor(st,rc,depth){depth=depth||0;if(depth>3)return;for(const k in rc){const need=rc[k]-(st[k]||0);if(need<=0||RAWS.includes(k))continue;const r=ITEMS[k]&&ITEMS[k].recipe;if(!r)continue;
  for(let i=0;i<need;i++){rdCraftFor(st,r,depth+1);if(!haveIn(r,[st]))break;takeFrom(r,[st]);inv.add(st,k,1)}}}
// ---- R&D
function rdKindOf(id){return ceKind(id)}
function rdCan(m,g){const c=ceOf(m),sp=c.ceo==='Innovator'?1:c.ceo==='Cautious'?6:RD.spare;return ceT(m)>=RD.cost[g]+sp*ceUpkeep(m)+ceReserve(m)}
function rdStart(m,id,why){const c=ceOf(m),g=rdLineG(m,id)+1;if(g>5||c.rd||!rdCan(m,g))return false;const R=mkAtHome(m);if(!R)return false;
  transfer(ceW(m),ceHostWallet(m),RD.cost[g]);c.cost+=RD.cost[g];(c.labs=c.labs||{})[id]=g;
  c.rd={id,g,stage:'design',until:S.T+RD.design[g],proto:{},t0:S.T};ceNews(m,`has opened an R&D project: ${ITEMS[rdGid(id,g)].name} (${why}). Its lab is going up at ${DEF[mkHomeSid(m)].name}.`);return true}
function rdTick(){if(!rdOn())return;const T=S.T;for(const m in MAKERS){const c=ceOf(m);if(!c||c.dead||!c.rd)continue;const P=c.rd;if(T<P.until)continue;
    if(P.stage==='design'){P.stage='materials';P.until=T+rnd(...RD.mat);continue}
    if(P.stage==='materials'){if(!P.got){const R=mkAtHome(m);if(!R){P.until=T+60;continue}const st=mkStock(R),gid=rdGid(P.id,P.g),rc=ITEMS[gid].recipe;rdCraftFor(st,rc);
        const cost=Math.ceil(ceComp(R.sid,gid));if(!haveIn(rc,[st])||ceT(m)<cost){P.until=T+60;continue}transfer(ceW(m),R.owner==='neutral'?'neutral':R.owner,cost);c.cost+=cost;takeFrom(rc,[st]);inv.addAll(P.proto,rc);P.got=1}
      P.stage='trials';P.until=T+rnd(...RD.trial);continue}
    if(P.stage==='trials')rdLaunch(m)}}
function rdLaunch(m){const c=ceOf(m),P=c.rd,id=P.id,g=P.g,gid=rdGid(id,g),R=mkAtHome(m);(c.g=c.g||{})[id]=g;c.rd=null;
  // the prototype is the first unit on the shelf
  const st=R?mkStock(R):S.econ.stock.neutral;inv.addAll(st,P.proto);P.proto={};const rc=ITEMS[gid].recipe;if(haveIn(rc,[st])){takeFrom(rc,[st]);inv.add(st,gid,1)}
  // the old grades are retired: broken into raw ore wherever they sit on a market
  let n=0;for(const sid in S.stations){const X=S.stations[sid];if(!X)continue;let ms;try{ms=mkStock(X)}catch(e){continue}for(let h=1;h<g;h++){const old=rdGid(id,h);const k=ms[old]||0;if(!k)continue;inv.take(ms,old,k);const v=invVec({[old]:k});for(const e of RAWS)if(v[e])inv.add(ms,e,v[e]);n+=k}}
  ceNews(m,`launches the ${ITEMS[gid].name}.${n?` ${n} unsold units of the old grade are broken back into ore.`:''}`,g>=3);c.ln[id]={tw:0,last:S.T}}
// when a line keeps losing, or a rival's higher grade outsells it
function rdReview(){if(!rdOn())return;const T=S.T,sold={},grade={},byKind={};for(const m in MAKERS){const c=ceOf(m);if(!c||c.dead)continue;for(const id of MK_LINE[m]){sold[id]=ceSold(m,id,CE.window);grade[id]=rdLineG(m,id);const k=rdKindOf(id);(byKind[k]=byKind[k]||[]).push([m,id])}}
  for(const m in MAKERS){const c=ceOf(m);if(!c||c.dead||c.rd||T<(c.rdRev||0))continue;c.rdRev=T+CE.review;
    const cand=[];for(const id of MK_LINE[m]){if(grade[id]>=5||!ITEMS[rdGid(id,grade[id]+1)])continue;const peers=byKind[rdKindOf(id)]||[],tot=peers.reduce((a,[,x])=>a+sold[x],0),fair=tot/Math.max(1,peers.length),mine=sold[id];
      const L=c.ln[id]||{tw:0},tweakable=!!CE_KSTAT[ITEMS[id].part]&&id.startsWith('mp_');
      const outg=peers.some(([mm,x])=>mm!==m&&grade[x]>grade[id]&&sold[x]>mine);
      if(outg)cand.push([id,'a rival\'s higher grade is outselling it',fair-mine+5]);else if(fair>=1&&mine<fair*RD.lose&&(!tweakable||L.tw>=2))cand.push([id,'its buyers keep passing it by',fair-mine])}
    if(!cand.length)continue;cand.sort((a,b)=>b[2]-a[2]);rdStart(m,cand[0][0],cand[0][1])}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{if(rdOn()&&!NET.cl){rdTick();rdReview()}}catch(e){console.error(e)}return r}}
{const o=ledger;ledger=function(){const r=o.apply(this,arguments);try{const L=r.L.Stations;for(const m in S.corp||{}){const P=S.corp[m].rd;if(!P||!P.proto)continue;const v=invVec(P.proto);for(const e of RAWS){L[e]+=v[e];r.tot[e]+=v[e]}}}catch(e){}return r}}
// a maker that fails mid-project: its prototype's components go back to the host's market
{const o=ceFail;ceFail=function(m){const c=ceOf(m);try{if(c&&c.rd){const R=mkAtHome(m),st=R?mkStock(R):S.econ.stock.neutral;inv.addAll(st,c.rd.proto||{});c.rd=null}}catch(e){console.error(e)}return o.apply(this,arguments)}}
// a new company starts its lines at grade 1 again (the old lab's grades went with the old company)
{const o=ceReborn;ceReborn=function(m){const r=o.apply(this,arguments);const c=ceOf(m);if(c&&!c.dead){c.g={};c.labs={};c.rd=null}return r}}
// ---- the powers' refits take systems too, and graded parts up to a grade above their tech
{const o=ceRefit;ceRefit=function(){if(!rdOn())return o.apply(this,arguments);for(const f of FAC_IDS){const st=S.econ.stock[f];if(!st)continue;const pool=(S.corpFit=S.corpFit||{})[f]=S.corpFit[f]||{};
    const tot=Object.values(pool).reduce((a,b)=>a+b,0);let lose=Math.floor(tot*CE.wear*CE.refit.every/3600+Math.random());const terr=[...territory(f)].filter(id=>S.sectors[id]);
    while(lose-->0&&terr.length){const ks=Object.keys(pool).filter(k=>pool[k]>0);if(!ks.length)break;const k=pick(ks);inv.take(pool,k,1);toDebris(S.sectors[pick(terr)],{[k]:1})}
    let n=Math.floor(ceRefitRate(f)*CE.refit.every/3600+Math.random());const gmax=factionTier(f)+1,where=Object.values(S.stations).filter(R=>R&&(R.owner===f||R.owner==='neutral')&&R.sid!==WRACK.sid);
    while(n-->0){if((S.econ.treasury[f]||0)<CE.refit.keep)break;const c=[];
      for(const R of where){let ms;try{ms=mkStock(R)}catch(e){continue}for(const id in ms){const I=ITEMS[id];if(!I||!I.maker||!(ms[id]>0)||(I.grade||1)>gmax)continue;const pr=stPrice(R,id),bv=Math.max(1,baseValue(id));
        const tw=I.sys?((SYS_TASTE[f]||{})[I.sys]||1)*.8:((CE_TASTE[f]||{})[I.part]||1)*(CORP_W.has(I.part)?1:.6);
        const w=tw*(1+2*ceGood(I.tr||{}))*(1+.35*((I.grade||1)-1))/Math.pow(pr/bv,.5)*(R.owner===f?1.3:1);if(w>0)c.push([[R,id,pr],w])}}
      if(!c.length)break;const[R,id,pr]=wpickArr(c),ms=mkStock(R),wl=R.owner==='neutral'?'neutral':R.owner,p=Math.ceil(pr);if((S.econ.treasury[f]||0)<p)break;
      transfer(f,wl,p);inv.take(ms,id,1);inv.add(pool,id,1);if(R.mk)R.mk[id]=(R.mk[id]||0)-1;ceSale(ITEMS[id].maker,id,1,p,wl,R.sid)}}}}
// ---- the Loadout: systems are installed, not upgraded
function rdSysHtml(c,P,sl){const t=P.tiers[sl]||1,m=(P.sysm||{})[sl],cur=ITEMS[rdGid(m?`sy_${m}_${sl}`:`sy_${sl}`,t)],srcs=[P.cargo,c.storage||P.vault],cap=typeof gradeCap==='function'?gradeCap(P):5;
  const have=ITEM_ORDER.filter(id=>ITEMS[id]&&ITEMS[id].sys===sl&&countIn(id,srcs)>0);
  let h=`<div class="note" style="margin:0 0 10px">Fitted: <b>${esc(cur?cur.name:SLOT[sl].name+' G'+t)}</b>. Systems are parts now: a better one is a higher grade bought from the maker that invented it, then installed here. The one it replaces goes to your ${esc(String(c.storageName||'vault').toLowerCase())}. Your Contractor Rating allows grade ${cap}.</div>`;
  h+=have.length?have.map(id=>{const I=ITEMS[id],ok=I.grade<=cap;return`<div class="ldopt">${gIcon(id,15)}<span style="flex:1;min-width:0"><span>${esc(I.name)}</span><br><span class="mass" style="margin:0">grade ${I.grade} · ${countIn(id,srcs)} on hand${ok?'':` · needs Rating for grade ${I.grade}`}</span></span><button class="btn sm" data-act="sysfit" data-arg="${sl}:${id}" ${ok?'':'disabled'}>Install</button></div>`}).join(''):`<div class="empty">No ${esc(SLOT[sl].name.toLowerCase())} parts in your hold or hangar. Makers' systems are on the Market.</div>`;
  return h}
{const o=renderDock;renderDock=function(){const r=o.apply(this,arguments);try{if(!rdOn()||S.unb)return r;const B=$('dBody');if(!B)return r;
  for(const b of B.querySelectorAll('.ldplus'))b.remove();for(const b of B.querySelectorAll('[data-act="bupg"]'))b.remove();
  if(dockTab==='upg'&&typeof ldSel==='string'&&ldSel.startsWith('sys:')){const H=B.querySelector('#ldSysHost'),sl=ldSel.slice(4);if(H&&SLOT[sl]){H.innerHTML=rdSysHtml(dockCtx(),S.player,sl);const n=H.parentElement&&H.parentElement.querySelector('.note');if(n&&/upgraded in place/.test(n.textContent))n.textContent='A system part, installed in the hull. Swap it for a better one from a maker.'}}}catch(e){console.error(e)}return r}}
{const o=dockClick;dockClick=function(act,arg){if(act==='sysfit'){dockAction('sysfit',arg);renderDock();return}return o.apply(this,arguments)}}
// ---- the Corporations view shows each line's grade and the R&D project
{const o=ceHtml;ceHtml=function(P){let h=o.apply(this,arguments);try{const m=String(coPk.economy||'').slice(5),c=ceOf(m);if(!c)return h;
  for(const id of MK_LINE[m]||[]){const g=rdLineG(m,id);if(g>1)h=h.replace(`${esc(ITEMS[id].name)} <span class="mass">`,`${esc(ITEMS[rdGid(id,g)].name)} <span class="mass">`)}
  const P2=c.rd;const stx=P2?`${esc(ITEMS[rdGid(P2.id,P2.g)].name)}: ${P2.stage==='design'?'design':P2.stage==='materials'?'materials':'trials'}, ${fmtT(Math.max(0,P2.until-S.T))} left in this stage`:'none running';
  const labs=Object.entries(c.labs||{}).map(([id,g])=>`${esc(ITEMS[id].name.replace(MAKERS[m].short+' ',''))} G${g}`).join(', ');
  h=h.replace('<div class="lab" style="margin-top:12px">Its lines</div>',`<div class="lab" style="margin-top:12px">R&D</div><div class="note" style="margin:2px 0 8px">${stx}${labs?` · labs: ${labs}`:''}</div><div class="lab" style="margin-top:12px">Its lines</div>`)}catch(e){}return h}}
