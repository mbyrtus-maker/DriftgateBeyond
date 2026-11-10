//@src 16zzzv_depotwork.js
// ============================================================ Beyond: reasons to stop at a depot (agreed with the user 9 Nov 2026)
// BEYOND_DESIGN.md, "Proposal: reasons to stop at a depot" and "Depot missions and salvage: agreed". Built: front levels,
// Depot missions (their own Jobs category) and salvage buyers. Shortage buy orders were turned down.
// Front level (every minute, S.dpf): Front (2) an enemy power or the Brood holds a neighbouring system, or the depot is
// damaged or raided; Border (1) it borders a system its power doesn't hold; Interior (0) neither. Pay ×1, ×1.25, ×1.5.
// Depot missions: a Front or Border depot posts up to DPM.max at once: Defend (a raid or strike coming), Sweep (Front only),
// Picket (hold the gate into others' space), Convoy in (its inbound supply convoy), Recover the wreck (a capital wreck in or
// next to its system). Listed on every Jobs board within DPM.near jumps under "Depot missions"; taken only docked at the
// depot. One at a time per pilot. Paid from the power's treasury; standing rises as with any of its work.
// Salvage: goods scooped from a ship's spilled cargo, or from a wreck's chunks, carry a salvage mark (P.salv[item][source],
// a mark on real goods like the stolen tag). Sold at a power's depot: Brood salvage +80% anywhere, salvage from the power's
// enemies (and the Unbound) +40% at a Front or Border depot, the premium paid by the power. Cargo stolen from the depot's
// own power can be handed back there for a 25% finder's fee, clearing the mark and its heat.
// The ledger: credits move from treasuries; goods move between holds and stores only.
const DPM={near:6,max:3,every:30,open:1200,life:3600,mult:[1,1.25,1.5],raidT:1800,
  defMin:60,defHold:1500,defKill:.5,swpN:4,swpT:1200,swpKill:250,swpDone:1200,pickT:600,pickR:2500,pickPay:900,scoutK:1.5,convK:.5,wreckT:25,wreckN:40,stand:2};
const SALV={enemy:.4,brood:.8,fee:.25};
const DPM_NAME={def:'Defend',swp:'Sweep',pick:'Picket',conv:'Convoy in',wreck:'Recover the wreck'};
JOB_TY.depot='Depot missions';JB_SH.depot='4,4 26,4 26,18 15,27 4,18';if(!JOB_ORDER.includes('depot'))JOB_ORDER.push('depot');
// ---- front levels
function dpFront(R){if(!isDepotF(R))return 0;const f=R.owner,nb=NEIGH[R.sid]||[];
  if(nb.some(n=>{const o=sectorOwner(n);return o==='brood'||(FAC_IDS.includes(o)&&o!==f&&hostile(f,o))})||R.hull<R.hMax*.98||(S.raids||[]).some(r=>r.dep===R.sid)||(R.hitT&&S.T-R.hitT<DPM.raidT))return 2;
  return edgeDepot(R)?1:0}
function dpLvl(sid){return(S.dpf||{})[sid]||0}
function dpMult(sid){return DPM.mult[dpLvl(sid)]||1}
function dpmAll(){return S.dpm=S.dpm||[]}
function dpmMine(P){const k=pkeyOf(P);return dpmAll().find(m=>m.taker&&sameK(m.taker,k))||null}
function dpThreat(R){const f=R.owner,r=(S.raids||[]).find(x=>x.dep===R.sid);if(r)return{k:'raid',id:r.id,who:r.side};
  const ev=(S.events||[]).find(e=>e.type==='offensive'&&e.sector===R.sid&&e.stage!=='done'&&e.stage!=='failed'&&e.att!==f&&(e.att==='brood'||hostile(f,e.att)));return ev?{k:'ev',id:ev.id,who:ev.att}:null}
function dpThreatLive(m){if(m.th==='raid')return(S.raids||[]).some(r=>r.id===m.tid);const ev=(S.events||[]).find(e=>e.id===m.tid);return!!ev&&ev.stage!=='done'&&ev.stage!=='failed'}
function dpEnemy(f,side){return side==='brood'||side==='pirate'||(FAC_IDS.includes(side)&&side!==f&&hostile(f,side))}
function dpPickGate(R){const f=R.owner,nb=(NEIGH[R.sid]||[]).filter(n=>sectorOwner(n)!==f);return nb.find(n=>dpEnemy(f,sectorOwner(n)))||nb[0]||null}
function dpWreckNear(R){for(const sid of[R.sid,...(NEIGH[R.sid]||[])]){const s=S.sectors[sid];for(const w of(s&&s.wrecks)||[])if(w.pts&&w.pts.some(p=>oreTotal(p)>0)&&w.until>S.T+120)return{w,sid}}return null}
function dpPay(k,f,n,why){n=Math.round(n);if(!(n>0))return 0;const got=payKey(k,f,n);if(got){keyFeed(k,`◆ ${why}: +${fmt(got)} cr from ${FACTIONS[f].short}.`,'good');runAs(isMe(k)?null:k,()=>standWork(S.player,f,DPM.stand,'depot mission'))}return got}
function dpEnd(m,ok,msg){const A=dpmAll(),i=A.indexOf(m);if(i>=0)A.splice(i,1);if(m.taker&&msg)keyFeed(m.taker,msg,ok?'good':'warn')}
function dpShipOf(k){if(!W)return null;if(isMe(k))return S.player.docked||W.dead?null:W.player;return W.ents.find(e=>e.rp===k&&e.alive)||null}
// ---- posting and the clock (host)
function dpmTick(){if(NET.cl||!S||S.training||S.unb||!S.econ)return;const dt=S.T-(S.dpmT0||S.T);if(S.T<(S.dpmT||0))return;S.dpmT=S.T+DPM.every;S.dpmT0=S.T;S.dpf={};
  for(const R of Object.values(S.stations)){if(!isDepotF(R))continue;if(R._lh!=null&&R.hull<R._lh)R.hitT=S.T;R._lh=R.hull;S.dpf[R.sid]=dpFront(R)}
  // missions in hand: tidy, progress, expire
  for(const m of dpmAll().slice()){const R=S.stations[m.sid];if(!R||R.owner!==m.f){dpEnd(m,false,`Depot mission ended: ${DEF[m.sid].name} is no longer ${FACTIONS[m.f].short}'s.`);continue}
    if(!m.taker){if(S.T>m.until||dpLvl(m.sid)<1&&m.k!=='def'||(m.k==='def'&&!dpThreatLive(m))||(m.k==='conv'&&!(S.traders||[]).some(t=>t.id===m.tid&&!t.esc))||(m.k==='wreck'&&!dpWreckLive(m)))dpEnd(m,false);continue}
    if(S.T>m.tk+DPM.life){dpEnd(m,false,`Depot mission timed out: ${dpTitle(m)}.`);continue}
    const sh=dpShipOf(m.taker),here=sh&&W&&W.sid===m.sid;
    if(m.k==='def'){if(here&&dt>0){m.here=1;dpPay(m.taker,m.f,DPM.defMin*dpMult(m.sid)*dt/60,`Defending ${R.name}`)}
      if(!dpThreatLive(m)){if(m.here)dpPay(m.taker,m.f,DPM.defHold*dpMult(m.sid),`${R.name} held`);dpEnd(m,!!m.here,m.here?`Depot mission done: ${R.name} held.`:`Depot mission over: the attack on ${R.name} ended before you got there.`)}}
    else if(m.k==='swp'){if(S.T>m.tk+DPM.swpT)dpEnd(m,false,`Sweep over: ${m.prog||0} of ${m.n} kills in time.`)}
    else if(m.k==='pick'){const g=here&&(GATES[m.sid]||[]).find(x=>x.to===m.to);if(g&&d3(sh,g)<=DPM.pickR&&dt>0){m.prog=(m.prog||0)+dt;m.seen=S.T}
      if((m.prog||0)>=DPM.pickT){const P=xPilotOfKey(m.taker);dpPay(m.taker,m.f,DPM.pickPay*dpMult(m.sid)*(P&&isScoutCls(P.cls)?DPM.scoutK:1),`Picket at the ${DEF[m.to].name} gate`);dpEnd(m,true,`Depot mission done: picket held.`)}}
    else if(m.k==='conv'){if(!(S.traders||[]).some(t=>t.id===m.tid))dpEnd(m,false)}
    else if(m.k==='wreck'){if(S.T>m.until+900)dpEnd(m,false,`Recover the wreck: time's up (${Math.round(m.prog||0)} of ${m.n} t brought in).`)}}
  // new missions at Front and Border depots
  for(const R of Object.values(S.stations)){if(!isDepotF(R)||dpLvl(R.sid)<1)continue;const L=dpmAll().filter(m=>m.sid===R.sid),has=k=>L.some(m=>m.k===k);if(L.length>=DPM.max)continue;const f=R.owner,add=o=>{if(L.length<DPM.max){const m={id:S.nextId++,sid:R.sid,f,t0:S.T,until:S.T+DPM.open,taker:null,...o};dpmAll().push(m);L.push(m)}};
    const th=dpThreat(R);if(th&&!has('def'))add({k:'def',th:th.k,tid:th.id,who:th.who});
    const t=(S.traders||[]).find(x=>x.kind==='haul'&&x.side===f&&x.to===R.sid&&!x.esc&&cvLeft(x)>=1&&cvLeft(x)<=3);if(t&&!L.some(m=>m.k==='conv'&&m.tid===t.id))add({k:'conv',tid:t.id});
    const wk=dpWreckNear(R);if(wk&&!L.some(m=>m.k==='wreck'&&m.wid===wk.w.id))add({k:'wreck',wid:wk.w.id,wsid:wk.sid,wname:wk.w.name,wside:wk.w.side,n:Math.min(DPM.wreckN,Math.max(10,Math.round(wk.w.pts.reduce((a,p)=>a+oreTotal(p),0)/4))),until:wk.w.until});
    if(dpLvl(R.sid)>=2&&!has('swp'))add({k:'swp',n:DPM.swpN,sys:[R.sid,...(NEIGH[R.sid]||[]).filter(n=>dpEnemy(f,sectorOwner(n)))]});
    const to=dpPickGate(R);if(to&&!has('pick'))add({k:'pick',to})}}
function dpWreckLive(m){const s=S.sectors[m.wsid];return!!(s&&(s.wrecks||[]).some(w=>w.id===m.wid&&w.pts.some(p=>oreTotal(p)>0)))}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{dpmTick()}catch(e){console.error(e)}return r}}
// ---- kills: Defend pays half the bounty again, Sweep counts them
{const o=sideKill;sideKill=function(e,sh,killer){const r=o.apply(this,arguments);try{if(!W||NET.cl)return r;const ks=Object.keys(sh||{});if(!ks.length&&killer)ks.push(killer);
  for(const k of ks){const m=dpmAll().find(x=>x.taker&&sameK(x.taker,k));if(!m||!dpEnemy(m.f,e.side)||e.role==='limpet')continue;const x=(sh&&sh[k])||1;
    if(m.k==='def'&&W.sid===m.sid){dpPay(k,m.f,bountyOf(e)*DPM.defKill*x,`Defending ${S.stations[m.sid].name}: kill bonus`)}
    else if(m.k==='swp'&&m.sys.includes(W.sid)&&x>=.25){m.prog=(m.prog||0)+1;dpPay(k,m.f,DPM.swpKill*dpMult(m.sid),`Sweep ${m.prog}/${m.n}`);if(m.prog>=m.n){dpPay(k,m.f,DPM.swpDone*dpMult(m.sid),'Sweep complete');dpEnd(m,true,'Depot mission done: sweep complete.')}}}}catch(err){console.error(err)}return r}}
// ---- the convoy reaches the depot with you: a front bonus on the escort pay
{const o=cvEnd;cvEnd=function(t,ok){const E=t&&t.esc,m=E&&dpmAll().find(x=>x.k==='conv'&&x.tid===t.id&&x.taker&&sameK(x.taker,E.k));const r=o.apply(this,arguments);
  try{if(m){if(ok)dpPay(m.taker,m.f,cvPay(t,E.need||1)*DPM.convK*dpMult(m.sid),'Convoy in: front bonus');dpEnd(m,!!ok,ok?'Depot mission done: the convoy is in.':'Depot mission failed: the convoy was lost.')}}catch(e){console.error(e)}return r}}
// ---- the Jobs board
function dpTitle(m){const R=S.stations[m.sid],n=R?R.name:DEF[m.sid].name;
  return m.k==='def'?`Defend ${n}`:m.k==='swp'?`Sweep: ${m.n} hostiles near ${n}`:m.k==='pick'?`Picket the ${DEF[m.to].name} gate at ${n}`:m.k==='conv'?`Convoy in: escort supplies to ${n}`:`Recover the ${m.wname} wreck for ${n}`}
function dpPayTxt(m){const k=dpMult(m.sid);if(m.k==='def')return[`${fmt(Math.round(DPM.defMin*k))} cr/min`,DPM.defHold*k];if(m.k==='swp')return[`${fmt(Math.round(DPM.swpKill*k))} cr a kill`,DPM.swpKill*k*m.n+DPM.swpDone*k];
  if(m.k==='pick'){const n=Math.round(DPM.pickPay*k*(isScoutCls(S.player.cls)?DPM.scoutK:1));return[`${fmt(n)} cr`,n]}if(m.k==='conv'){const t=(S.traders||[]).find(x=>x.id===m.tid),n=t?Math.round(cvPay(t,cvLeft(t))*(1+DPM.convK*k)):0;return[`${fmt(n)} cr`,n]}
  return[`${fmt(Math.round(DPM.wreckT*k))} cr/t`,DPM.wreckT*k*m.n]}
function dpDetail(m){const R=S.stations[m.sid],k=dpMult(m.sid),lv=['Interior','Border','Front'][dpLvl(m.sid)],f=FACTIONS[m.f].short;
  const what=m.k==='def'?`${m.who==='brood'?'The Brood are':m.who==='pirate'?'Unbound raiders are':`${FACTIONS[m.who]?FACTIONS[m.who].short:'An enemy'} is`} coming for ${esc(R.name)}. Be in its system while the attack lasts: ${fmt(Math.round(DPM.defMin*k))} cr a minute, half again of every kill's bounty, and ${fmt(Math.round(DPM.defHold*k))} cr if the depot still stands when it's over.`
    :m.k==='swp'?`Kill ${m.n} of ${esc(f)}'s enemies (the Brood, the Unbound, powers at war with it) in ${m.sys.map(s=>esc(DEF[s].name)).join(', ')} within ${Math.round(DPM.swpT/60)} minutes of taking it: ${fmt(Math.round(DPM.swpKill*k))} cr a kill and ${fmt(Math.round(DPM.swpDone*k))} cr at ${m.n}, on top of the bounties.`
    :m.k==='pick'?`Hold station within ${DPM.pickR/1000} km of the gate to ${esc(DEF[m.to].name)} in ${esc(DEF[m.sid].name)} for ${DPM.pickT/60} minutes in all. While you hold it, ${esc(f)} sees into ${esc(DEF[m.to].name)}. Scouts are paid half again.`
    :m.k==='conv'?`${esc(f)}'s supply convoy for ${esc(R.name)} is ${(()=>{const t=(S.traders||[]).find(x=>x.id===m.tid);return t?`in ${esc(DEF[t.sector].name)}, ${cvLeft(t)} jump${cvLeft(t)===1?'':'s'} out`:'gone'})()}. Taking this signs you on as its escort; when it docks you get the escort pay and a front bonus of ${Math.round(DPM.convK*k*100)}% of it.`
    :`The ${esc(m.wname)} wreck is drifting in ${esc(DEF[m.wsid].name)}. Blast it apart, scoop the chunks and sell ${m.n} t of them at ${esc(R.name)}'s Market: ${fmt(Math.round(DPM.wreckT*k))} cr a tonne on top of the salvage price.`;
  return`<p class="note" style="margin:0 0 6px">${what}</p><p class="note" style="margin:0">${esc(R.name)} is a <b>${lv}</b> depot (pay ×${k}). Depot missions are taken in person: fly there and take it from its Jobs board.</p>`}
{const o=jobsList;jobsList=function(c,P,srcs){const out=o.apply(this,arguments);try{if(S.unb||S.training||!c||c.kind!=='station')return out;const me=pkeyOf(P),cur=dpmMine(P),hop=sid=>HOP[P.sector]&&HOP[P.sector][sid]!=null?HOP[P.sector][sid]:99;
  for(const m of dpmAll()){const R=S.stations[m.sid];if(!R)continue;const mine=m.taker&&sameK(m.taker,me);if(m.taker&&!mine)continue;if(P.sworn&&P.sworn!==m.f&&hostile(P.sworn,m.f))continue;const h=hop(m.sid);if(h>DPM.near&&!mine)continue;
    const at=P.docked==='station'&&P.sector===m.sid,low=!P.sworn&&standOf(m.f,P)<STAND.dock,[pt,pn]=dpPayTxt(m);
    const need=mine?'':low?`Your standing with ${FACTIONS[m.f].short} is too low.`:cur?'You are already on a depot mission.':at?'':`Fly to ${R.name} to take this mission.`;
    const where=mine&&m.k==='def'?m.sid:mine&&m.k==='pick'?m.sid:mine&&m.k==='wreck'?m.wsid:mine&&m.k==='conv'?(((S.traders||[]).find(t=>t.id===m.tid)||{}).sector||m.sid):m.sid,hw=hop(where);
    out.push({id:'dpm:'+m.id,by:m.f,sid:where,ty:'depot',title:esc(dpTitle(m)),sub:mine?`your mission · ${m.k==='swp'?`${m.prog||0}/${m.n} kills`:m.k==='pick'?`${Math.floor((m.prog||0)/60)}/${DPM.pickT/60} min held`:m.k==='wreck'?`${Math.round(m.prog||0)}/${m.n} t in`:'under way'}`:`${['','Border','Front'][dpLvl(m.sid)]} depot · ${DPM_NAME[m.k]} · taken at ${esc(R.name)}`,
      hops:hw,where:hw?`${hw} jump${hw===1?'':'s'}`:'here',payN:pn,pay:pt,need,
      btn:mine?(where!==P.sector?['croute',where,'Set course']:null):need&&!at&&!low&&!cur?['croute',m.sid,'Set course']:need?null:['dpmtake',m.id,'Take the mission'],btn2:mine&&P.docked?['dpmdrop',m.id,'Drop mission']:null,detail:()=>dpDetail(m)})}}catch(err){console.error(err)}return out}}
{const o=dockAction;dockAction=function(act,arg){if(act!=='dpmtake'&&act!=='dpmdrop')return o.apply(this,arguments);const P=S.player,m=dpmAll().find(x=>String(x.id)===String(arg));
  if(act==='dpmdrop'){if(m&&m.taker&&sameK(m.taker,pkeyOf(P))){if(m.k==='conv'){const t=(S.traders||[]).find(x=>x.id===m.tid);if(t&&t.esc&&sameK(t.esc.k,pkeyOf(P)))t.esc=null}m.taker=null;m.until=S.T+DPM.open;dockErr='Mission dropped.'}return}
  if(!m||m.taker){dockErr='That mission is gone.';return}if(!(P.docked==='station'&&P.sector===m.sid)){dockErr=`Fly to ${S.stations[m.sid].name} to take this mission.`;return}if(dpmMine(P)){dockErr='You are already on a depot mission.';return}
  if(!P.sworn&&standOf(m.f,P)<STAND.dock){dockErr=`Your standing with ${FACTIONS[m.f].short} is too low.`;return}
  if(m.k==='conv'){dockErr='';o.call(this,'cvesc',String(m.tid));if(!String(dockErr).startsWith('✓'))return}
  m.taker=pkeyOf(P);m.tk=S.T;m.prog=0;m.here=0;const msg=`✓ ${dpTitle(m)}: mission taken.`;dockErr=m.k==='conv'?dockErr+' '+msg:m.k==='wreck'?(P.route=m.wsid,`${msg} Course set to ${DEF[m.wsid].name}.`):msg}}
// ---- your mission on the HUD in flight
{const o=myJobRows;myJobRows=function(){let h=o.apply(this,arguments);try{const m=dpmMine(S.player);if(m){const st=m.k==='swp'?`${m.prog||0}/${m.n} kills`:m.k==='pick'?`${Math.floor((m.prog||0)/60)}/${DPM.pickT/60} min at the gate`:m.k==='wreck'?`${Math.round(m.prog||0)}/${m.n} t`:m.k==='def'?'hold the depot':'escorting';
  h+=myJobRow('cmb','Depot',dpTitle(m),m.k==='wreck'?m.wsid:m.k==='conv'?(((S.traders||[]).find(t=>t.id===m.tid)||{}).sector||m.sid):m.sid,st)}}catch(e){}return h}}
// ---- a picket's eyes: the power sees into the next system while it's held
{const o=covOf;covOf=function(side){const C=o.apply(this,arguments);try{for(const m of dpmAll())if(m.k==='pick'&&m.taker&&m.f===side&&m.seen&&S.T-m.seen<DPM.every*2+5)C.add(m.to)}catch(e){}return C}}
// ---- the map: Front depots ringed red, Border amber; the system panel lists its depot missions
{const o=sxHtml;sxHtml=function(sid){let h=o.apply(this,arguments);try{const R=S.stations[sid];if(isDepotF(R)&&dpLvl(sid)){const L=dpmAll().filter(m=>m.sid===sid&&!m.taker);h+=`<div class="note" style="margin:8px 0 0"><b style="color:${dpLvl(sid)>1?'#ff5d4f':'#f0b24a'}">${dpLvl(sid)>1?'Front':'Border'} depot</b>${L.length?` · depot missions: ${L.map(m=>DPM_NAME[m.k]).join(', ')} (taken at the depot)`:''}</div>`}}catch(e){}return h}}
// ============================================================ salvage
function salvAdd(P,k,src,n){if(!P||!src||!(n>0))return;P.salv=P.salv||{};const t=P.salv[k]=P.salv[k]||{};t[src]=(t[src]||0)+n}
function salvSide(src){return String(src).startsWith('wk:')?String(src).split(':')[2]:src}
function salvSync(P){if(!P||!P.salv)return;for(const k in P.salv){const have=(P.cargo[k]||0)+((P.vault||{})[k]||0),t=P.salv[k];let tot=0;for(const s in t)tot+=t[s];if(tot>have){const r=tot?have/tot:0;for(const s in t){t[s]=Math.floor(t[s]*r);if(!t[s])delete t[s]}}if(!Object.keys(t).length)delete P.salv[k]}}
function salvPct(f,lvl,src){const s=salvSide(src);if(s==='brood')return SALV.brood;if(lvl>=1&&dpEnemy(f,s))return SALV.enemy;return 0}
// marks: a ship's spilled cargo (the crate names whose ship it was) and a wreck's chunks
{const o=crateTake;crateTake=function(P,cr,k){const r=o.apply(this,arguments);try{if(cr&&cr.side&&cr.side!=='player'&&cr.side!=='neutral')salvAdd(P,k,cr.side,1)}catch(e){}return r}}
{const o=blCloud;blCloud=function(s,at,ore,R0,extra,ow,v,scrap){const n0=(s.clouds||[]).length,r=o.apply(this,arguments);try{if(scrap&&s.clouds&&s.clouds.length>n0){let w=null,bd=1e9;for(const x of s.wrecks||[]){const d=d3(x,at);if(d<bd){bd=d;w=x}}if(w)s.clouds[s.clouds.length-1].wk=`wk:${w.id}:${w.side}`}}catch(e){}return r}}
{const o=blCollect;blCollect=function(e,P,c,dt,s){const b=c&&c.wk?{...c.ore}:null;const r=o.apply(this,arguments);try{if(b)for(const k in b){const n=b[k]-((c.ore||{})[k]||0);if(n>0)salvAdd(P,k,c.wk,n)}}catch(err){}return r}}
// selling at a power's depot: the premium, and a Recover the wreck mission's tonnes
{const o=dockAction;dockAction=function(act,arg){if(act==='dpret')return dpReturn(arg);if(act!=='sell'||S.unb)return o.apply(this,arguments);const P=S.player,R=S.stations[P.sector];if(P.docked!=='station'||!isDepotF(R))return o.apply(this,arguments);
  const c=dockCtx(),k=String(arg).split(':')[0],srcs=[P.cargo,c.storage],h0=countIn(k,srcs),pr=mSell(c,k);salvSync(P);const r=o.apply(this,arguments);
  try{let sold=h0-countIn(k,srcs);const t=P.salv&&P.salv[k];if(sold>0&&t){const f=R.owner,lvl=dpLvl(R.sid),m=dpmMine(P),wm=m&&m.k==='wreck'&&m.sid===R.sid?m:null;let prem=0,tons=0;
    const order=Object.keys(t).sort((a,b)=>(wm&&b.startsWith(`wk:${wm.wid}:`)?1:0)-(wm&&a.startsWith(`wk:${wm.wid}:`)?1:0)||salvPct(f,lvl,b)-salvPct(f,lvl,a));
    for(const s of order){if(sold<=0)break;const n=Math.min(sold,t[s]);sold-=n;t[s]-=n;if(!t[s])delete t[s];prem+=n*pr*salvPct(f,lvl,s);if(wm&&s.startsWith(`wk:${wm.wid}:`))tons+=n*mass(k)}
    if(!Object.keys(t).length)delete P.salv[k];
    if(prem>=1){const got=transfer(f,'player',Math.round(prem));if(got)dockErr=`${dockErr||''} Salvage premium: +${fmt(got)} cr from ${FACTIONS[f].short}.`.trim()}
    if(wm&&tons>0){const left=wm.n-(wm.prog||0),use=Math.min(left,tons);wm.prog=(wm.prog||0)+use;dpPay(wm.taker,wm.f,use*DPM.wreckT*dpMult(wm.sid),'Recover the wreck');if(wm.prog>=wm.n)dpEnd(wm,true,'Depot mission done: the wreck is recovered.')}}}catch(e){console.error(e)}return r}}
// handing a power's own stolen cargo back at its depot
function dpReturn(k){const P=S.player,R=S.stations[P.sector];if(P.docked!=='station'||!isDepotF(R)){dockErr='Only at a power\'s depot.';return}const f=R.owner;stolSync(P);const c=dockCtx();
  const want=(P.stol&&P.stol[k]&&P.stol[k][f])||0,n=Math.min(want,countIn(k,[P.cargo,c.storage]));if(!(n>0)){dockErr='You carry none of its cargo.';return}
  let left=n;for(const s of[P.cargo,c.storage]){const x=Math.min(left,s[k]||0);if(x>0){inv.take(s,k,x);inv.add(dStore(R),k,x);left-=x}}
  delete P.stol[k][f];if(!Object.keys(P.stol[k]).length)delete P.stol[k];salvSync(P);const fee=transfer(f,'player',Math.round(baseValue(k)*n*SALV.fee));
  smHeat(P,f,-n*SM.theft/10,'returned cargo');standWork(P,f,Math.min(3,n*.1),'returned cargo');dockErr=`✓ ${n} ${ITEMS[k].name} handed back to ${FACTIONS[f].short}: finder's fee ${fmt(fee)} cr, heat eased.`}
// the Market at a power's depot: what you carry that it pays a salvage premium for, and its own cargo to hand back
function dpSalvHtml(c,P){const R=S.stations[P.sector];if(S.unb||P.docked!=='station'||!isDepotF(R))return'';const f=R.owner,lvl=dpLvl(R.sid);salvSync(P);try{stolSync(P)}catch(e){}const rows=[];
  for(const k in P.salv||{}){let best=0,n=0;for(const s in P.salv[k]){const p=salvPct(f,lvl,s);if(p>0){n+=P.salv[k][s];best=Math.max(best,p)}}if(n)rows.push(`<div class="coln"><span style="flex:1">${n} ${esc(ITEMS[k].name)} · salvage</span><b class="amber">+${Math.round(best*100)}% when sold here</b></div>`)}
  for(const k in P.stol||{}){const n=(P.stol[k]||{})[f];if(n)rows.push(`<div class="coln"><span style="flex:1">${n} ${esc(ITEMS[k].name)} · ${esc(FACTIONS[f].short)}'s own lost cargo</span><button class="btn sm" type="button" data-act="dpret" data-arg="${k}">Hand back · +${fmt(Math.round(baseValue(k)*n*SALV.fee))} cr</button></div>`)}
  const lv=['an Interior','a Border','a Front'][lvl];
  return`<div class="ldbox" style="margin:0 0 12px;border-left:3px solid ${lvl>1?'#ff5d4f':lvl?'#f0b24a':'#5a647c'}"><div class="lab">Salvage at ${lv} depot</div><p class="note" style="margin:2px 0 ${rows.length?8:0}px">${esc(FACTIONS[f].short)} pays +${Math.round(SALV.brood*100)}% for Brood salvage${lvl?` and +${Math.round(SALV.enemy*100)}% for salvage from its enemies`:''} on top of the price, and a finder's fee for its own lost cargo.${rows.length?'':' You carry none.'}</p>${rows.join('')}</div>`}
{const o=mkHtml;mkHtml=function(c,P){const h=o.apply(this,arguments);try{return dpSalvHtml(c,P)+h}catch(e){return h}}}
