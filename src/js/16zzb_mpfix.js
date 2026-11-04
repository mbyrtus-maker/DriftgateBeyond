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
