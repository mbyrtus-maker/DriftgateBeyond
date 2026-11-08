//@src 16zzzc_deepdrive.js
// ============================================================ Beyond: Ostrova's Deep Drive (user, 7 Nov 2026)
// Ostrova's faction perk, with its Archive fleet: the drive-mystics' deep reactors carry its ships across the galaxy faster.
// One dial, FPK.deep (0.75: a quarter less time), multiplies every travel time and jump spin-up of things Ostrova owns:
//   live    a capital's jump drive spin-up (carriers and escorts, AI or a pilot's in Ostrova's line), host and guest alike
//           (capJumpK, 04_strategy.js; used by frigateThink and the guest's bridge mirror in 08_world.js)
//   off-screen
//           a capital's hop between systems (capMoveStep: a hop is two strategic ticks; Ostrova banks the time it saves
//           and a whole banked tick takes one off a later hop, so on average a hop takes 2 x FPK.deep ticks);
//           every inbound ETA it sets: offensives, campaign strikes and builds, constructor convoys, response wings and
//           hunter groups (and their follow-on), carrier sorties out and back, the leader's flagship coming to an audience
//           (ddK(side) at each place the ETA is computed);
//           every hop of a tracked party on the lanes: merchants, haulers, supply, kit, staging and import convoys
//           (S.traders), raids, prowls, strike groups flying to an offensive and parties flying home (S.raids): each time
//           one of these sets its next hop time, ddSweep() shortens what is left of it (it runs right after the code that
//           sets them, at the same S.T, so it is exact off-screen and within a frame live)
//   pilots  a pilot flying an Ostrova design-line hull (P.faction, as Varkesh's self-repair goes with its line): the gate's
//           hold countdown, and the Seer and Oracle's peek-drive spool
// Planning that counts in hop times (where a raid can intercept a convoy, interdiction jobs, the traders table) uses the
// same factor. Nothing is created or destroyed: only timers move, so the ledger is untouched. The host simulates; guests
// only draw (the guest's spin-up mirror and its own gate countdown use the same functions).
FPK.deep=.75;
function ddK(side){return side==='ostrova'&&FPK.deep>0?FPK.deep:1}
// a capital's line: its side, or for a solo pilot's own capital the line its stats follow (spawnFrigate's fac)
function ddCapK(t){if(!t)return 1;return ddK(t.side==='player'?(S&&S.player&&S.player.faction):t.side)}
// the pilot's own hull
function ddPilotK(){const P=S&&S.player;return P&&!S.unb?ddK(P.faction):1}
// the share of time saved, in words: "a quarter", "a third", or a percentage
function ddWords(){const k=1-(FPK.deep>0?FPK.deep:1),p=Math.round(k*100);return p===25?'a quarter':p===33?'a third':p===20?'a fifth':p===50?'half':p+'%'}
function ddText(){return`Deep Drive: jumps and travel ${ddWords()} faster`}

// ---- capitals: spin-up live, hops off-screen
{const o=capJumpK;capJumpK=function(t){return o.apply(this,arguments)/ddCapK(t)}}
{const o=capMoveStep;capMoveStep=function(t){const K=ddCapK(t);if(K>=1)return o.apply(this,arguments);
  if(!(t.moveT>0))t.ddN=0;t.ddN=(t.ddN||0)+1;const r=o.apply(this,arguments);
  if(r){t.ddB=(t.ddB||0)+t.ddN*(1-K);t.ddN=0;if(t.ddB>=1){t.ddB-=1;t.moveT=pmul(t,'eng');t.ddN=1}}
  return r}}

// ---- tracked parties on the lanes: shorten each newly set hop
function ddSweep(){if(!S||(typeof NET!=='undefined'&&NET.cl))return;const K=FPK.deep;if(!(K>0)||K===1)return;const T=S.T;
  const one=x=>{const n=x.next;if(n===x._ddN)return;if(typeof n==='number'&&n>T)x.next=T+(n-T)*K;x._ddN=x.next};
  for(const t of S.traders||[])if(t&&t.side==='ostrova')one(t);
  for(const r of S.raids||[])if(r&&r.side==='ostrova')one(r)}
{const o=tradersTick;tradersTick=function(){const r=o.apply(this,arguments);try{ddSweep()}catch(e){console.error(e)}return r}}
{const o=updateEvents;updateEvents=function(){try{ddSweep()}catch(e){console.error(e)}const r=o.apply(this,arguments);try{ddSweep()}catch(e){console.error(e)}return r}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{ddSweep()}catch(e){console.error(e)}return r}}
{const o=worldUpdate;worldUpdate=function(dt){const r=o.apply(this,arguments);try{ddSweep()}catch(e){console.error(e)}return r}}
// a raid's launch points carry their side, so interception planning knows how fast the party flies
{const o=raidSources;raidSources=function(side){const L=o.apply(this,arguments);for(const s of L||[])s.side=side;return L}}

// ---- pilots in an Ostrova line
{const o=unbGateHold;unbGateHold=function(){return o.apply(this,arguments)*ddPilotK()}}
{const s0=PEEK.spool;Object.defineProperty(PEEK,'spool',{get(){return s0*ddPilotK()},enumerable:true,configurable:true})}

// ---- shown in the game: Ostrova's trait text (the Allegiance tab's "The powers" table reads it too); the figure follows the dial
{const F=FACTIONS.ostrova;let base=F.traitText;Object.defineProperty(F,'traitText',{get(){const i=base.indexOf('<br>');return i<0?`${base} · ${ddText()}`:`${base.slice(0,i)} · ${ddText()}${base.slice(i)}`},set(v){base=String(v).replace(/ · Deep Drive: [^<]*/,'')},enumerable:true,configurable:true})}
