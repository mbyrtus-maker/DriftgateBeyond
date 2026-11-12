//@src 16zzzze_firsthour.js
// ============================================================ Beyond: the first hour, for every pilot (user, 11 Nov 2026)
// From the review and the onboarding design (the user chose these four for everyone; the guided first contract itself is an
// option on the Training menu): the starter ship arrives armed; the dock's Overview never says "Nothing waiting here" but
// names one next step; (the Shipyard's current-hull label and the standing line are fixed in 13_hud_dock_map.js; one Jobs
// row per target is in 16zq_jobs2.js).
// ---- a new pilot's ship arrives armed: rounds, rack and charges full, so the first dock doesn't bill a rearm
function armFull(P){try{P.ammo=ammoCap(P);P.rack=pRack(P);P.blN=blCap(P)}catch(e){}}
{const o=newGame;newGame=function(){const r=o.apply(this,arguments);try{if(S&&S.player&&typeof loadOn==='function'&&loadOn())armFull(S.player)}catch(e){}return r}}
{const o=newPilot;newPilot=function(){const P=o.apply(this,arguments);try{if(P&&typeof loadOn==='function'&&loadOn())armFull(P)}catch(e){}return P}}
// ---- the Overview's next step: shown where "Ready now" had nothing
function nsJob(c,P){try{const L=jobsList(c,P,[P.cargo],!!(c.contracts||P.sworn),!!FACTIONS[P.sworn]).filter(j=>!(j.bm||String(j.id).startsWith('bmr:'))&&!j.need&&!jobIsMine(j)&&j.payN>0);
    // within 2 jumps first; none that close (a galaxy's first minute) → the nearest
    const far=j=>(j.hops||0)>2?1:0;L.sort((a,b)=>(far(a)-far(b))||(jobRank(a,P)-jobRank(b,P))||(far(a)?(a.hops-b.hops):0)||(b.payN-a.payN));return L[0]||null}catch(e){return null}}
function nextStep(c,P){if(!c||!P||S.unb||S.training)return null;
  try{if(myJobRows())return{t:'You have a job under way',d:`Launch (${kb('act')}) and follow its course marker. The job shows in your flight HUD, and the Jobs tab has its details.`,act:'tab',arg:'jobs',btn:'Open Jobs'}}catch(e){}
  const j=nsJob(c,P);if(j)return{t:`Take a job: ${String(typeof jbKey==='function'&&jbKey(j)?String(j.title).replace(/ for [^ ]+$/,''):j.title).replace(/<[^>]*>/g,'')}`,d:`${j.where?esc(j.where)+' · ':''}pays ${j.pay}. It suits your ${esc(CLASSES[P.cls].name)}.`,act:'nsjob',arg:j.id,btn:'Show me the job'};
  if(!P.sworn){const ready=typeof coReady==='function'&&coReady(P),funded=typeof coFunded==='function'&&coFunded(P);
    if(!funded&&P.credits>=COP.deposit)return{t:'Set up your company',d:`You hold ${fmt(P.credits)} cr: enough for the ${fmt(COP.deposit)} cr treasury a company opens with. A company builds Depots and Stations, hires crews and posts jobs.`,act:'coprof',arg:'',btn:ready?'Company profile':'Set up my company'};
    if(funded&&!myDepots(P).length)return{t:'Build your first base',d:'Buy a Lair Kit or a Depot Kit (Trade → Market → Components). Kits are heavy: a Heavy Hauler carries them. Fly it to a free system and press O to build.',act:'tab',arg:'market',btn:'Open the Market'};
    if(funded&&myDepots(P).some(R=>!R.pst)&&!myStations(P).length)return{t:'Upgrade a Depot to a Station',d:`A Station grows from a Depot: ${esc(ctrStaWhy(P))}.`,act:'tab',arg:'market',btn:'Open the Market'}}
  return{t:'Nothing to pick up here',d:'No job here suits your ship right now. Trade → Best runs lists what sells where nearby, and the galaxy map (M) shows where the fighting and the freeports are.',act:'tab',arg:'trade',btn:'Best runs'}}
{const o=homeHtml;homeHtml=function(c,P){let h=o.apply(this,arguments);try{const E='<div class="empty">Nothing waiting here. Your hold sells nowhere here, no contract matches it, and no upgrade is in reach yet.</div>';
    if(h.includes(E)){const n=nextStep(c,P||S.player);if(n)h=h.replace(E,`<div class="nstep" style="display:flex;gap:14px;align-items:center;flex-wrap:wrap;padding:12px 14px;border:1px solid var(--line,#1d2740);border-left:3px solid var(--amber,#f0b24a)"><span style="flex:1;min-width:240px"><span class="lab" style="margin:0 0 4px;display:block">Next step</span><b style="font-size:15px">${n.t}</b><br><span class="note" style="margin:0">${n.d}</span></span><button class="btn pri" type="button" data-act="${n.act}" data-arg="${esc(n.arg)}">${esc(n.btn)}</button></div>`)}}catch(e){console.error(e)}return h}}
{const o=dockClick;dockClick=function(act,arg){if(act==='nsjob'){dockTab='jobs';try{jobFilter='all';jobSel=arg}catch(e){}renderDock();return}return o.apply(this,arguments)}}
