//@src 16zzb_mpfix.js
// ============================================================ multiplayer gaps closed (Beyond, 3 Nov 2026)
// The user asked whether all the multiplayer code was in place. An audit of the systems built this pass found two gaps:
//  1. Company and map orders from flight: the host can run its company from anywhere (the Company screen and the map's
//     side panel call dockAction directly), but a guest's same orders went as {t:'act'}, which the host refuses unless the
//     guest is docked. So a flying guest couldn't set crews' jobs, order guards to intercept, set fees, send capitals on
//     patrol or escort, upgrade or build depots and stations, post jobs, run black-market deals, save a brand or declare.
//     Those company actions (CO_REMOTE) now run for a guest wherever they are, exactly as they do for the host; everything
//     else still needs the dock. The answer reaches the Company screen and the map panel (they sat on "Working…").
//  2. The cargo scanner was the host's only: a guest scans on its own screen with the same range and timing, and asks the
//     host for the reading ({t:'cscan'} when the scan starts and when it completes); the host checks the guest's scanner
//     and range, sends the hold back ({t:'cscr'}), and runs the noticing and the heat for that guest.
const CO_REMOTE=new Set(['crewjob','crewhire','crewfire','hgguard','feeset','mkset','depotup','depotbuild','staup','stabld','capbld','zmpatrol','zmescort','pjpost','pjcancel','bmassign','bmdeal','bmreq','brsave','declare','prop']);
function mpDockedNow(P){return P.docked==='station'||P.docked==='lair'||!!(S.outposts&&S.outposts[P.docked])}
{const o=hostRecv;hostRecv=function(L,m){try{const c=MP.cl[L.peer],P=c&&c.ready&&S&&S.pilots&&S.pilots[c.pid];
    if(P&&m&&m.t==='act'&&CO_REMOTE.has(m.act)&&!mpDockedNow(P)){const pid=c.pid;let err='';
      try{err=runAs(pid,()=>{dockErr='';dockAction(m.act,String(m.arg||''));return dockErr})}catch(x){err='That did not work.';frameErr('guest company action',x)}
      send(L,{t:'actr',err,co:1});sendPR(c,false,true);send(L,syncMsg(c));return}
    if(P&&m&&m.t==='cscan'){const pid=c.pid,e0=MP.rp[pid],w=e0?worldOf(e0):WORLDS[P.sector],E=w&&entInWorld(w,String(m.id)),g=cscG(P);
      if(!E||!E.alive||!g||!e0||d3(E,e0)>cscR(g)+(E.st&&E.st.radius||0)*1.5+200)return;
      const oW=W;W=w;let C={};try{C=cscLoad(E)}finally{W=oW}
      runAs(pid,()=>{if(m.k==='seen')cscNotice(E,S.player);else if(m.k==='done')cscDone(E,S.player)});
      send(L,{t:'cscr',id:m.id,C});return}}catch(x){frameErr('guest message',x)}
  return o.apply(this,arguments)}}
{const o=clientRecv;clientRecv=function(m){try{
    if(m&&m.t==='cscr'){const E=W&&W.ents.find(e=>String(e.id)===String(m.id));if(E)E._cscC=m.C||{};return}
    if(m&&m.t==='actr'){const r=o.apply(this,arguments);if(typeof coErr!=='undefined'&&$('company')&&!$('company').hidden){coErr=m.err||'';try{renderCompany()}catch(e){}}
      if($('map')&&!$('map').hidden){if(typeof mpMsg!=='undefined'&&m.err)mpMsg=m.err;try{renderMapSide()}catch(e){}}return r}}catch(x){}
  return o.apply(this,arguments)}}
// ---- (4 Nov 2026, a guest convoy test) a convoy's goods ride in its freighter while it flies through an open system, and its
// record's load is empty meanwhile: the raid bounty (paid at the kill, which is always in an open system) fell to the 400 cr
// base, the boards showed that, and the boards' "what it carries" was blank, for the host and for guests alike. The record now
// keeps a manifest of what it set off with on each leg (just a note: the goods themselves are in the freighter, so the
// ledger is untouched), and the bounty, the escort fee and the boards read it while the load is aboard.
function cvLoad(t){const L=t&&t.load;if(L&&Object.keys(L).some(k=>L[k]>0))return L;return(t&&t.live&&t.man)||L||{}}
{const o=spawnTrader;spawnTrader=function(t){const man={...(t.load||{})};const r=o.apply(this,arguments);if(Object.keys(man).length)t.man=man;return r}}
{const o=raidBounty;raidBounty=function(t){return o.call(this,t?{...t,load:cvLoad(t)}:t)}}
{const o=haulWhat;haulWhat=function(t){return o.call(this,t?{...t,load:cvLoad(t)}:t)}}
{const o=cvPay;cvPay=function(t,hops){return o.call(this,t?{...t,load:cvLoad(t)}:t,hops)}}
// ---- (4 Nov 2026, a guest building test) a dock action can move the guest's berth on the host (a Lair raised to a Depot leaves
// you docked at the new Depot's station): tell the guest, so its own record and screens follow
{const o=hostRecv;hostRecv=function(L,m){let c=null,P=null,d0;try{c=MP.cl[L.peer];P=c&&c.ready&&S&&S.pilots&&S.pilots[c.pid];if(P&&m&&m.t==='act')d0=P.docked}catch(x){}
  const r=o.apply(this,arguments);try{if(P&&m&&m.t==='act'&&P.docked!==d0&&P.docked)send(L,{t:'dkset',d:P.docked})}catch(x){}return r}}
{const o=clientRecv;clientRecv=function(m){if(m&&m.t==='dkset'){try{if(S&&S.player&&S.player.docked){S.player.docked=String(m.d);if(m.d!=='lair')S.player.lairId=null;if(!$('dock').hidden)renderDock()}}catch(x){}return}return o.apply(this,arguments)}}
// ---- (7 Nov 2026, the corporations bug pass) a warning about one system reaches every pilot who covers it or is in it, the
// host's guests too (Bloom growth, a Leviathan swelling); a pilot's coverage is worked out as that pilot
function pilotCovered(pid,sid){const R=S.pilots&&S.pilots[pid];if(!R)return false;const oP=S.player,oC=CTX;S.player=R;CTX=pid;try{return covered(sid)}catch(e){return false}finally{S.player=oP;CTX=oC}}
function sidFeed(sid,msg,kind){if(NET.cl||!S)return;if(S.player&&(covered(sid)||S.player.sector===sid))feed(msg,kind);
  if(NET.host)for(const pid in S.pilots||{}){const R=S.pilots[pid];if(pid===NET.me||!R||R===S.player)continue;if(R.sector===sid||pilotCovered(pid,sid))feedTo(pid,msg,kind)}}
// ---- the guest's copy of the makers: names, traits and grades live in S.corp, but a guest's ITEMS and MAKERS are only set
// from it by ceApply, which only the host ran. The guest applies them when it joins and when a sync brings a change to them
// (a tweak, a launch, a new company), then refreshes its own ship's stats, which its own physics use.
// A ship's stats find its fit through FIT_T (keyed by the pilot's tune object, filled by fitOf); every 'pr' and sync hands a
// guest a fresh tune object and refreshes its stats at once, before anything had called fitOf, so a guest flew without its
// fitted parts (cargo modules, makers' speed traits, part grades). Look the fit up first.
{const o=refreshPlayerStats;refreshPlayerStats=function(){try{if(S&&S.player&&typeof fitOf==='function')fitOf(S.player)}catch(e){}return o.apply(this,arguments)}}
let MP_CESIG=null;
function mpCeSig(){if(!S||!S.corp)return'';let s='';for(const m in S.corp){const c=S.corp[m]||{};s+=m+'|'+(c.name||'')+'|'+(c.short||'')+'|'+(c.dead?1:0)+'|'+JSON.stringify(c.tr||{})+'|'+JSON.stringify(c.g||{})+'|';
  for(const id in c.ln||{})s+=id+':'+((c.ln[id]&&c.ln[id].tw)||0)+',';s+=';'}return s}
function mpCeApply(force){if(!NET.cl||!S||typeof ceApply!=='function')return;const k=mpCeSig();if(!force&&k===MP_CESIG)return;MP_CESIG=k;
  try{ceApply();if(W&&W.player&&S.player)refreshPlayerStats()}catch(e){console.error(e)}}
{const o=mpClientStart;mpClientStart=function(){const r=o.apply(this,arguments);mpCeApply(true);return r}}
{const o=applySync;applySync=function(){const r=o.apply(this,arguments);mpCeApply(false);return r}}
