//@src 16zza_cjobs.js
// ============================================================ Comms: Jobs here (Beyond, agreed 3 Nov 2026)
// I opens Command; I again opens Jobs here; I after that steps through the ships around you. Jobs here lists the jobs in
// this system (the docked board's "here" jobs) that suit your hull (jobFit), best pay first, from this system's station
// board under the usual hiring rules; with no station that deals with you, what's happening here for the powers that hire
// you. Keys 1-3 pick a job (4 is "More" when there are more than four). Picking does what Select job does on the board:
// it signs you on and tracks it; an escort signs you on to the convoy, an operation joins you, a convoy raid or the Dread
// Pirate targets the ship. Handing over goods and buying stay docked; the dock-only jobs (smuggling and black-market runs,
// the rumour, selling a find) stay off the page, counted with the jobs for other hulls in one line. The Unbound get Prey
// here instead: the powers' and freeports' freighters, traders and miners in this system, with the cargo scanner's
// reading, biggest haul first; picking one targets it. Guests use the messages the board and Comms already send
// (job, plan, cvesc), so the host keeps the ledger.
const CJ={per:4,dockOnly:['bmr','find','dpw','bmo'],hint:{k:'deliver at the dock',pj:'deliver at the dock',b:'deliver at the dock',r:'deliver at the dock',s:'land on its deck',ce:'fly with it',cv:'kill the freighter',op:'join the fight',bm:'hold the beacon',cl:'fire a Control Marker',dp:'shoot him down'}};
function cjTxt(s){return String(s||'').replace(/<[^>]+>/g,'').replace(/&amp;/g,'&').replace(/&#39;/g,"'").replace(/&quot;/g,'"').replace(/&lt;/g,'<').replace(/&gt;/g,'>')}
// the board you'd hail from here
function cjCtx(P){const sid=P.sector,R=S.stations[sid];
  if(R&&(R.owner==='neutral'||FAC_IDS.includes(R.owner))){let mk=null;try{mk=mkStock(R)}catch(e){}
    const c={kind:'station',name:R.name,owner:R.owner,market:mk,wallet:R.owner,fee:true,storage:P.vaultAt===sid?P.vault:{},contracts:true,works:true,cjSid:sid};
    if(R.owner==='neutral'||jobIssuers(c,P).length)return c}
  return{kind:'space',name:DEF[sid].name,owner:P.sworn&&FAC_IDS.includes(P.sworn)?P.sworn:'neutral',market:null,wallet:null,storage:{},contracts:false,cjSid:sid}}
// { jobs: this system's jobs for your hull, other: how many for other hulls, dock: how many dock-only, near: the nearest fitting job elsewhere, all }
function cjList(){const P=S.player;if(!W||!P||S.training||S.unb)return{jobs:[],other:0,dock:0,near:null,all:[]};
  const c=cjCtx(P);let all=[];try{all=jobsList(c,P,[P.cargo],!!(c.contracts||P.sworn),!!FACTIONS[P.sworn])}catch(e){console.error(e);all=[]}
  const F=jobFit(P.cls),here=j=>j.where==='here'||(j.sid&&j.sid===P.sector),pre=j=>jobPre(j.id);
  const seen=new Set(),H=all.filter(here).sort((a,b)=>(b.payN||0)-(a.payN||0)).filter(j=>!seen.has(j.id)&&seen.add(j.id)),dock=H.filter(j=>CJ.dockOnly.includes(pre(j))),ok=H.filter(j=>!CJ.dockOnly.includes(pre(j))),jobs=ok.filter(j=>F.includes(j.ty)),other=ok.length-jobs.length;
  jobs.sort((a,b)=>(b.pin||0)-(a.pin||0)||(jobRank(a,P)-jobRank(b,P))||(!!a.need-!!b.need)||((b.payN||0)-(a.payN||0)));
  const near=all.filter(j=>!here(j)&&F.includes(j.ty)&&!CJ.dockOnly.includes(pre(j))&&j.sid&&DEF[j.sid]&&(j.hops||0)>0).sort((a,b)=>a.hops-b.hops||(b.payN||0)-(a.payN||0))[0]||null;
  return{jobs,other,dock:dock.length,near,all}}
// ---- the Unbound: prey in this system
function cjPreyRead(T){const R=T._csc;let C={};try{C=cscLoad(T)}catch(e){}if(R&&R.done)return{txt:invMass(C)>0?`${fmt(invMass(C))} t · about ${fmt(Math.round(invValue(C)))} cr`:'empty hold',v:invValue(C),known:2};if(R&&R.seen)return{txt:cscRough(C),v:invValue(C),known:1};return{txt:'cargo unknown',v:0,known:0}}
function cjPrey(){if(!W||!W.player||!S.unb)return[];const p=W.player,out=[];
  for(const e of W.ents){if(e.type!=='ship'||!e.alive||e.isPlayer||e.rp)continue;if(!['trader','hauler','miner','flee'].includes(e.role))continue;const sd=sideNorm(e.side);if(!(FAC_IDS.includes(sd)||sd==='neutral'))continue;
    const t=e.tradeT||null,r=cjPreyRead(e);out.push({e,sd,t,r,d:d3(e,p)})}
  return out.sort((a,b)=>b.r.known-a.r.known||b.r.v-a.r.v||a.d-b.d)}
// ---- the page
let cjPg=0;
function cjOpts(){const O=[];
  if(S.unb){const L=cjPrey(),n=L.length,pages=Math.max(1,Math.ceil(n/(CJ.per-1)));if(cjPg>=pages)cjPg=0;const per=n>CJ.per?CJ.per-1:CJ.per,sl=L.slice(cjPg*per,cjPg*per+per);
    for(const x of sl){const who=x.sd==='neutral'?'Freeport':FAC(x.sd).short,what=x.t&&x.t.kind==='haul'&&DEF[x.t.to]?`freighter → ${DEF[x.t.to].name}`:x.e.role==='miner'?'miner':x.e.role==='hauler'?'hauler':'trader';
      O.push({k:'cjprey',e:x.e,l:`${who} ${what} · ${x.r.txt} · ${fmt(x.d)} m`})}
    if(!n)O.push({k:'none',off:1,l:'No prey in this system right now'});if(n>CJ.per)O.push({k:'cjmore',l:`More ▸ (${cjPg+1} of ${pages})`});return{O,note:n?'Pick one to target it. Hold it in range and your cargo scanner reads its hold.':'Freighters, traders and miners of the powers and the freeports show here.'}}
  const R=cjList();JOBS_LAST=R.all;for(const j of R.all)jobOpenBtns(j);
  const n=R.jobs.length,pages=Math.max(1,Math.ceil(n/(CJ.per-1)));if(cjPg>=pages)cjPg=0;const per=n>CJ.per?CJ.per-1:CJ.per,sl=R.jobs.slice(cjPg*per,cjPg*per+per);
  for(const j of sl){const pre=jobPre(j.id),hint=j.need?j.need:pre==='o'||j.id==='camp'?cjTxt(j.sub).split(' · ')[0]:CJ.hint[pre]||'';
    O.push({k:'cjjob',id:j.id,l:`${cjTxt(j.title)} · ${cjTxt(j.pay)}${hint?' · '+hint:''}${jobIsMine(j)?' · ✓ yours':''}`,dim:!!j.need})}
  if(!n)O.push({k:'none',off:1,l:'No jobs for your ship in this system right now'});
  if(n>CJ.per)O.push({k:'cjmore',l:`More ▸ (${cjPg+1} of ${pages})`});
  const bits=[];if(R.other)bits.push(`${R.other} for other ships`);if(R.dock)bits.push(`${R.dock} dock-only`);
  let note=bits.length?`${bits.join(', ')}: on the station's board.`:'';if(!n&&R.near)note=`Nearest: ${DEF[R.near.sid].name}, ${R.near.hops} jump${R.near.hops>1?'s':''}. `+note;
  return{O,note:(note+' I: the ships around you.').trim()}}
function cjOpen(){const r=cjOpts();W.cmOpts=r.O;const P=S.player;
  $('cmTo').textContent=S.unb?`Prey here · ${DEF[P.sector].name}`:`Jobs here · ${DEF[P.sector].name}`;
  $('cmList').innerHTML=r.O.map((o,i)=>`<button type="button" class="cm-o${o.dim?' cjdim':''}" data-cm="${i}"${o.off?' disabled':''}><kbd>${i+1}</kbd><span>${esc(o.l)}</span></button>`).join('')+`<button type="button" class="cm-o" data-cm="close"><kbd>Esc</kbd><span>Close</span></button>`;
  $('cmN').textContent=r.note;$('comms').classList.add('cj');$('comms').hidden=false;W.commsT=W.t}
function cjOn(){return!!(W&&W.player&&S&&S.player&&!S.training&&!S.player.docked&&!W.dead)}
function cjTarget(e,why){if(!e||!e.alive){flash('It has gone.',true);return}W.tgt={kind:'ship',ref:e};apOn=false;flash(why)}
function cjShipOf(t){if(!t)return null;return W.ents.find(e=>e.type==='ship'&&e.alive&&(e.tradeT===t||(e.pup&&e.role==='trader'&&sideNorm(e.side)===t.side&&t.sector===W.sid)))||null}
function cjPick(o){const P=S.player;
  if(o.k==='cjprey'){cjTarget(o.e,`Targeted ${shipLabel(o.e)}. Hold it in range to scan its hold.`);return}
  const j=(JOBS_LAST||[]).find(x=>x.id===o.id);if(!j){flash('That job is gone.',true);return}const pre=jobPre(j.id);
  if(j.need){flash(j.need,true);return}
  if(j.id==='camp'){const C=myCamp(),m=C&&C.mv;if(m){const k=pkey();if(!m.acc.includes(k)){if(NET.cl){netSend({t:'plan',id:m.id});m.acc.push(k);feed(`Signed on: ${m.title}. ${campHow(m)}`,'good')}else campAccept(k,m)}campCourse(m)}flash(`Signed on: ${cjTxt(j.title)}.`);return}
  if(pre==='o'){const C=myCamp(),x=C&&sideOf(C).find(y=>'o:'+y.id===j.id);if(x)sideTake(x);flash(`Signed on: ${cjTxt(j.title)}.`);return}
  if(JOB_OPEN.includes(pre)){if(!jobIsMine(j))jobTrack(j.id);
    if(pre==='ce'){const t=(S.traders||[]).find(x=>'ce:'+x.id===j.id);if(t){if(NET.cl){netSend({t:'cvesc',id:t.id});flash('Signing on as escort…')}else cvTake(t);const e=cjShipOf(t);if(e)W.ftgt=e}return}
    if(pre==='cv'){const t=(S.traders||[]).find(x=>'cv:'+x.id===j.id),e=cjShipOf(t);if(e)cjTarget(e,`Targeted ${shipLabel(e)}: destroy it for the bounty.`);else flash('Job selected. The freighter is somewhere in this system.');return}
    if(pre==='op'){joinOp(friendlyOps()[j.opi]);return}
    if(['k','pj','b','r'].includes(pre)){const R=S.stations[P.sector];flash(`Job selected: ${cjTxt(j.title)}. Dock${R?' at '+R.name:''} to deliver.`);return}
    flash(`Job selected: ${cjTxt(j.title)}.`);return}
  if(pre==='dp'){const D=typeof dpOf==='function'&&dpOf(),e=D&&W.ents.find(x=>x.alive&&x.dreadOf);if(e)cjTarget(e,`Targeted ${shipLabel(e)}.`);else flash(`${cjTxt(j.title)}: he's somewhere in this system.`);return}
  if(pre==='pj'){flash('Dock here to deliver it from the Jobs board.');return}
  if(pre==='cl'){flash(`${cjTxt(j.title)}: fly to it, break its defences and fire your Control Marker there.`);return}
  flash(cjTxt(j.title))}
// ---- the wiring
{const o=cycleFriendly;cycleFriendly=function(){if(cjOn()&&commsOpen()&&W.ftgt===W.player&&!W.cmJobs){W.cmJobs=1;cjPg=0;cjOpen();return}if(W)W.cmJobs=0;try{$('comms').classList.remove('cj')}catch(e){}return o.apply(this,arguments)}}
{const o=closeComms;closeComms=function(){if(W)W.cmJobs=0;try{$('comms').classList.remove('cj')}catch(e){}return o.apply(this,arguments)}}
{const o=commsPick;commsPick=function(k){if(W&&W.cmJobs&&k!=='close'){const x=W.cmOpts&&W.cmOpts[+k];if(!x||x.off)return;if(x.k==='cjmore'){cjPg++;cjOpen();return}closeComms();try{cjPick(x)}catch(e){console.error(e)}return}return o.apply(this,arguments)}}
// the quick-keys line: how many jobs here
let cjCnt={t:-9,n:0};
{const o=hudUpdate;hudUpdate=function(){const r=o.apply(this,arguments);try{if(!cjOn())return r;const k=$('cKeys');if(!k)return r;
  if(W.t-cjCnt.t>2){cjCnt.t=W.t;cjCnt.n=S.unb?cjPrey().length:cjList().jobs.length}let el=k.querySelector('.cjc');if(!el){el=document.createElement('div');el.className='sub cjc';k.appendChild(el)}
  const t=cjCnt.n?`<kbd>I</kbd><kbd>I</kbd> ${S.unb?'Prey':'Jobs'} here: ${cjCnt.n}`:'';if(el.innerHTML!==t)el.innerHTML=t;el.hidden=!t}catch(e){}return r}}
