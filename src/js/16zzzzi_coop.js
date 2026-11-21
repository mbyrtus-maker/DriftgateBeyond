//@src 16zzzzi_coop.js
// ============================================================ co-op audit fixes (mp-test bot, 21 Nov 2026)
// Driftgate Beyond's multiplayer gone over against the co-op lessons from Ace of the Airways (BEYOND_DESIGN.md "Co-op audit
// against the Ace of the Airways lessons"). The fixes made inside other files: snapshot and flight-input order numbers
// (15_multiplayer_dev.js: applySnap, netTick, hostRecv 'u'), full rows refreshing names, roles and weapons, AI ships'
// gate departures sent to guests (gateOutFx, event 'go'), the Jobs-here count per system (16zza_cjobs.js), a shared win no
// longer deleting each pilot's solo save (galaxyWon), a guest's own shield hit drawn where the shot struck (damageShip).
// Here, the ones that wrap a whole function:
//  - a guest takes the galaxy's length setting the moment it joins (it waited up to 3 s for lenApply's timer, so the map
//    could show the wrong rule for a moment);
//  - a guest joining (or reconnecting to) a galaxy that has already been won sees the win screen: the host's simulation has
//    stopped, so no 'won' message comes and the guest sat in a frozen galaxy with no word why. Seeing it again doesn't
//    count the win a second time in this browser's record;
//  - pilots arriving through one gate together come out side by side instead of inside each other: in a shared galaxy each
//    pilot's arrival point is set off the gate's axis by its place on the roster (the host on the axis, as before).
{const o=mpClientStart;mpClientStart=function(){const r=o.apply(this,arguments);
  try{if(S)lenApply()}catch(e){}
  try{const wv=$('win');if(S&&S.won&&running&&wv&&wv.hidden){let lg=null;try{lg=localStorage.getItem('dgbeyond.legacy')}catch(e){}
      galaxyWon(S.won);try{if(lg!==null)localStorage.setItem('dgbeyond.legacy',lg);else localStorage.removeItem('dgbeyond.legacy')}catch(e){}}}catch(e){console.error(e)}
  return r}}
// a pilot's arrival slot in a shared galaxy: 0 for the first on the roster (on the axis), 1 to 3 for the others
function arrSlot(pid){if(!NET.on||!pid)return 0;const i=(MP.roster||[]).findIndex(r=>r[0]===pid);return i>0?i%4:0}
{const o=doJump;doJump=function(to){const from=W&&W.sid;const r=o.apply(this,arguments);
  try{const k=arrSlot(S.player.pid||NET.me),g=from&&GATES[to]&&GATES[to].find(x=>x.to===from),p=W&&W.player;
    if(k&&g&&p&&W.sid===to&&!S.player.docked){const l=hyp(g.x,g.y,g.z)||1,ux=g.x/l,uy=g.y/l,uz=g.z/l;
      // two directions square to the gate's axis
      let ax=uy,ay=-ux,az=0;if(hyp(ax,ay,az)<.2){ax=0;ay=uz;az=-uy}const al=hyp(ax,ay,az)||1;ax/=al;ay/=al;az/=al;const bx=uy*az-uz*ay,by=uz*ax-ux*az,bz=ux*ay-uy*ax;
      const a=(k-1)*TAU/3,R=70,dx=(Math.cos(a)*ax+Math.sin(a)*bx)*R,dy=(Math.cos(a)*ay+Math.sin(a)*by)*R,dz=(Math.cos(a)*az+Math.sin(a)*bz)*R;
      p.x+=dx;p.y+=dy;p.z+=dz;const P=S.player;P.x=p.x;P.y=p.y;P.z=p.z}}catch(e){console.error(e)}
  return r}}
