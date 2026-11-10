//@src 16zzzzb_depminers.js
// ============================================================ Beyond: your Depot's miners (user, 9 Nov 2026)
// "Depots should not automatically mine; they should come with a few miners that then begin mining in that sector, and they
// have to be rebuilt if destroyed." A Depot (or Station) you own used to fill its store from the system's rocks at a flat
// rate with no ships. Now it keeps a roster of miners like the powers' depots (16zzn_miners.js): DM.n of them, built from
// its own store (each a miner's kit: plate, conduit, drones it can spare), flying out to the rocks and home to unload when
// the system is live, and mining at their share of the rate off-screen. No miners, no mining. A miner shot down is gone with
// its kit; the depot builds another from its store, one every 4 minutes, while the store holds the makings.
// It comes with them: the Depot Kit now also carries the makings of DM.n miners (DM.kit), which go into the new depot's
// store, and the roster is built at once. (Your hired crews' miners work as before, on top.)
// The ledger stays exact: miners are built from goods in the store; a save from before (its kits hold the old recipe) is
// rebased once on load.
const DM={n:3,kit:{plate:8,wire:6}};
ITEMS.kit_depot.recipe={...ITEMS.kit_depot.recipe,...DM.kit};
function dmOn(R){return!!R&&R.owner==='player'&&R.kind==='depot'}
{const o=mrSites;mrSites=function(){const L=o.apply(this,arguments);try{for(const sid in S.stations){const R=S.stations[sid];if(dmOn(R)&&!L.includes('S.'+sid))L.push('S.'+sid)}}catch(e){}return L}}
{const o=mrOn;mrOn=function(st){if(st&&st.R&&dmOn(st.R)&&st.owner==='player')return true;return o.apply(this,arguments)}}
{const o=mrTarget;mrTarget=function(st){if(st&&st.R&&dmOn(st.R))return DM.n;return o.apply(this,arguments)}}
// a kit coming home with no roster entry left goes to the depot's store
{const o=holderIn;holderIn=function(st,path){try{if(typeof path==='string'&&path.startsWith('mrs:')){const p=path.split(':'),k=p[1]||'',R=k[0]==='S'&&st.stations&&st.stations[k.slice(2)],ro=st.mrs&&st.mrs[k],m=ro&&ro.m.find(x=>String(x.id)===p[2]);
  if(!m&&R&&R.owner==='player')return R.stock=R.stock||{}}}catch(e){}return o.apply(this,arguments)}}
// a new depot: the kit's miner makings go into its store and its miners are built at once
function dmSeed(R){if(!dmOn(R)||NET.cl)return 0;const key='S.'+R.sid,M=(S.mrs=S.mrs||{});const ro=M[key]||(M[key]={f:'player',sid:R.sid,m:[],t:S.T,nid:1});const st=mrSite(key);let n=0;
  while(ro.m.length<DM.n){const k=mrKit(st);if(!k)break;ro.m.push({id:ro.nid++,c:k.c,load:k.load,live:false,next:S.T+rnd(5,20)});n++}ro.t=S.T+MR.build;return n}
function dmBuilt(P,before,srcs){const R=Object.values(S.stations).find(x=>dmOn(x)&&!before.has(x.sid));if(!R)return'';const mk={};for(const k in DM.kit){const n=Math.min(DM.kit[k],countIn(k,srcs));if(n>0)mk[k]=n}
  if(Object.keys(mk).length){takeFrom(mk,srcs);inv.addAll(R.stock=R.stock||{},mk)}const n=dmSeed(R);return n?` ${n} miner${n>1?'s':''} launched from its store: they mine this system.`:` It has no miners yet: put ${lackText(DM.kit,{})} in its store and it builds them.`}
{const o=depFresh;depFresh=function(P){const before=new Set(Object.keys(S.stations)),r=o.apply(this,arguments);try{if(String(r).startsWith('✓'))return r+dmBuilt(P,before,[P.cargo])}catch(e){console.error(e)}return r}}
{const o=depFromLair;depFromLair=function(P,L){const before=new Set(Object.keys(S.stations)),r=o.apply(this,arguments);try{if(String(r).startsWith('✓'))return r+dmBuilt(P,before,[P.cargo,L&&L.stash].filter(Boolean))}catch(e){console.error(e)}return r}}
// the depot's own screen says how its miners are doing
{const o=worksHtml;worksHtml=function(c,P,srcs,R){let h=o.apply(this,arguments);try{if(dmOn(R)){const L=mrLine('S.'+R.sid);if(L)h=`<div class="kv" style="margin:0 0 10px"><span>Miners</span><b>${esc(L.replace(/^Miners /,''))}</b></div><p class="note" style="margin:-6px 0 12px">Your depot's miners mine this system and bring the ore home; one lost is rebuilt from the store (${esc(Object.keys(DM.kit).map(k=>ITEMS[k].name).join(' and '))}, drones if it can spare them), one every 4 minutes.</p>`+h}}catch(e){console.error(e)}return h}}
// a save from before: its kits hold the old recipe; rebase the ledger once
{const o=newGame;newGame=function(){const r=o.apply(this,arguments);try{if(S)S.dmk=1}catch(e){}return r}}
{const o=migrate;migrate=function(){const r=o.apply(this,arguments);try{if(S&&!S.dmk){S.dmk=1;const l=ledger();S.ledger0={tot:l.tot,credits:l.credits}}}catch(e){console.error(e)}return r}}
