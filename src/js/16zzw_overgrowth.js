//@src 16zzw_overgrowth.js
// ============================================================ Beyond: the Brood passes its own Overgrowth (6 Nov 2026)
// The user: growth on the gates blocks the powers while the Brood can still jump. A gate sealed by Brood Overgrowth is a wall to
// everyone but the Brood: the Brood's ships, raids, strike groups and Gorgers go through it as if it were open; everyone
// else's (the powers', the Unbound's, contractors', your crews', you) can't. Out of sight, their parties now find a way round
// it or wait (only convoys did before; raids, strike groups and forces home went straight through); live, their ships hold at
// the sealed gate and their raids pick another way. A gate lock kit still seals a gate both ways, for everyone.
function ogWall(side,a,b){return side!=='brood'&&!!ogSealed(a,b)}
// a tracked party's next hop is walled: take the way round (or wait half a minute and look again)
function ogDetour(r,side,dest){const nx=r.path&&r.path[r.leg+1];if(!nx||!ogWall(side,r.sector,nx))return;const alt=ogRoute(r.sector,dest);if(alt&&alt.length>1){r.path=alt;r.leg=0}else r.next=Math.max(r.next||0,S.T+30)}
{const o=raidsTick;raidsTick=function(){try{for(const r of S.raids||[])ogDetour(r,r.side,r.dest)}catch(e){console.error(e)}return o.apply(this,arguments)}}
{const o=pjRunsTick;pjRunsTick=function(){try{for(const r of S.pjRuns||[])if(!r.live&&r.state!=='work')ogDetour(r,r.side,r.path[r.path.length-1])}catch(e){console.error(e)}return o.apply(this,arguments)}}
{const o=crRunsTick;crRunsTick=function(){try{for(const r of S.crRuns||[])if(!r.live)ogDetour(r,'player',r.path[r.path.length-1])}catch(e){console.error(e)}return o.apply(this,arguments)}}
// live: a non-Brood ship can't take a gate the Brood has grown over (the Brood can)
function ogGateOf(e){if(e.gj&&e.gj.g)return e.gj.g;const D=e.ai&&e.ai.dest;if(D&&D.type==='gate')return D;if(e.raidR){const r=raidOf(e.raidR);const nx=r&&r.path[r.leg+1];if(nx)return(GATES[W.sid]||[]).find(g=>g.to===nx)||null}if(e.pjRun){const r=pjRunOf(e.pjRun);const nx=r&&r.path[r.leg+1];if(nx)return(GATES[W.sid]||[]).find(g=>g.to===nx)||null}if(e.crRun){const r=crRunOf(e.crRun);const nx=r&&r.path[r.leg+1];if(nx)return(GATES[W.sid]||[]).find(g=>g.to===nx)||null}return null}
{const o=gateLocked;gateLocked=function(e){const r=o.apply(this,arguments);if(r)return r;try{if(e&&!e.isPlayer&&W){const g=ogGateOf(e);if(g&&g.to!==undefined&&ogWall(e.side==='player'?'player':e.side,W.sid,g.to))return true}}catch(err){}return false}}
// a raid in an open system whose next gate is walled picks another way out
{const o=raidLiveFrame;raidLiveFrame=function(){try{for(const r of S.raids||[])if(r.live&&r.sector===W.sid)ogDetour(r,r.side,r.dest)}catch(e){console.error(e)}return o.apply(this,arguments)}}
