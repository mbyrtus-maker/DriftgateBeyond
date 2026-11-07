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
// ---- Bloom Nodes hold off carriers with Overgrowth (user, 6 Nov 2026). A carrier's strike wing flies through the gate, so a
// gate sealed by Overgrowth stops it: an off-screen carrier strike, or a launched one still on its way, can't cross a sealed
// gate (the carrier must come into the system itself, or have the growth burned off first). And a Bloom Node with a hostile
// capital ship next door seeds Overgrowth on the gate between at once (over the usual two or three growths, one gate per
// node at a time), from the Brood's stores or its surge mass. The seed takes 90 seconds to seal the gate, as any other.
function ogSeedAt(a,b){const st=S.econ.stock.brood,g=S.surge&&S.surge.store,srcs=[st,g].filter(Boolean);if(!haveIn(OG.cost,srcs))return null;const load={};takeFrom(OG.cost,srcs);inv.addAll(load,OG.cost);
  const O={id:S.nextId++,a,b,key:gateKey(a,b),stage:'seed',t0:S.T,hp:OG.hp*.25,hitT:-1e9,load,strikeT:S.T+rnd(OG.strike[0],OG.strike[1]),guard:1};(S.og=S.og||[]).push(O);
  ogSay(O,`⚠ A Bloom Node is growing Overgrowth over ${ogName(O)} against the capital ship next door.`,'warn');return O}
function ogGuardTick(){if(NET.cl||!S||S.training)return;for(const t of S.frigates||[]){if(!(t.hull>0)||t.side==='brood'||!hostile('brood',t.side))continue;
  for(const n of NEIGH[t.sector]||[]){const R=S.stations[n];if(!R||R.owner!=='brood'||R.kind!=='depot')continue;const k=gateKey(n,t.sector);if(ogAt(n,t.sector)||(S.gateDown&&S.gateDown[k]))continue;
    if((S.og||[]).some(O=>O.guard&&(O.a===n||O.b===n)&&!ogSealed(O.a,O.b)))continue;if(ogOpenGates(t.sector,k)<1)continue;ogSeedAt(n,t.sector)}}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{ogGuardTick()}catch(e){console.error(e)}return r}}
{const o=carStrikeOff;carStrikeOff=function(t,sid){if(t&&t.side!=='brood'&&sid!==t.sector&&ogSealed(t.sector,sid))return;return o.apply(this,arguments)}}
{const o=sortieStart;sortieStart=function(t,E,to){if(t&&t.side!=='brood'&&to!==t.sector&&ogSealed(t.sector,to))return 0;return o.apply(this,arguments)}}
{const o=sortieTick;sortieTick=function(){try{for(const ev of S.events)if(ev.type==='sortie'&&ev.stage==='out'&&!ev.recall&&sortieSide(ev)!=='brood'&&ev.from!==ev.to&&ogSealed(ev.from,ev.to))ev.recall=1}catch(e){console.error(e)}return o.apply(this,arguments)}}
