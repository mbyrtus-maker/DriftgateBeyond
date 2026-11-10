//@src 16zzzx_contractor.js
// ============================================================ Beyond: a contractor's keys (user, 9 Nov 2026)
// "I think the take order and drop order and join operation are carry overs from Driftgate 1, they can be hidden until you have
// your own faction or declare an allegiance" and "O is engaging autopilot". For a pilot who neither flies for a power nor has
// declared a faction: O (join operation) and P / Shift+P (take or pick an order) do nothing but say so, the operations list
// is empty (so nothing sets a course and engages the autopilot for them), and the quick keys don't show them (05). Backspace
// still drops a selected job. The training courses keep them.
// (user, 9 Nov 2026: "I need O to work for establishing lairs, depots and stations; the comms command isn't working") For a
// contractor, O opens the Command page of Comms, which now lists: build a Lair here, build a Depot here (Depot Kit), upgrade
// your Depot here to a Station (Station Kit), and the distress call. Each says why it can't be done yet. (The Command page
// used to offer a contractor the distress call only.)
function ctrOnly(){const P=S&&S.player;return!!P&&!S.unb&&!S.training&&!P.sworn&&!P.decl}
{const o=planKey;planKey=function(){if(ctrOnly()){flash('Orders are for pilots who fly for a power or their own faction. Contract work is on the Jobs board.');return}return o.apply(this,arguments)}}
{const o=friendlyOps;friendlyOps=function(){if(ctrOnly())return[];return o.apply(this,arguments)}}
// ---- the contractor's Command page: building
function ctrBuildMenu(){if(!W||!W.player||W.dead){flash('Launch first.');return}if(S.player.docked){flash('Launch first: you build in flight.');return}W.ftgt=W.player;openComms()}
function ctrBuildOpts(){const P=S.player,O=[];let sp;try{sp=lairSpot(P)}catch(e){sp={why:'No spot for a Lair here.'}}
  O.push({k:'ctrlair',l:`Build a Lair here${sp.why?` · ${sp.why}`:''}`,off:!!(sp.why||!sp.a)&&!(sp.a&&(P.cargo.kit_lair||0)>0)});
  const can=depCan(W.sid),kit=kitOr(DEP.cost,[P.cargo],'kit_depot');O.push({k:'ctrdep',l:`Build a Depot here${!can?' · not in a system with a station or in a power\'s home space':!kit?' · needs a Depot Kit (or 2 Depot Frames) in your hold':''}`,off:!can||!kit});
  const R=S.stations[W.sid],mine=R&&R.owner==='player'&&(R.pid||'me')===pkeyOf(P);
  if(mine&&!R.pst){const k2=kitOr(STA.cost,[P.cargo,R.stock],'kit_station');O.push({k:'ctrsta',l:`Upgrade ${R.name} to a Station${k2?'':' · needs a Station Kit (in your hold or its stock)'}`,off:!k2})}
  else O.push({k:'ctrsta',l:mine?`${R.name} is already a Station`:'Upgrade your Depot to a Station · fly to your Depot\'s system',off:true});
  O.push({k:'help',l:'Distress: send help to me'});return O}
{const o=cmOpts;cmOpts=function(T){if(ctrOnly()&&W&&T===W.player)return ctrBuildOpts();return o.apply(this,arguments)}}
{const o=cmDo;cmDo=function(k,T){if(k==='ctrlair'){const m=lairBuildB();if(m)flash(m,!String(m).startsWith('✓'));return}
  if(k==='ctrdep'||k==='ctrsta'){coErr='';coClick(k==='ctrdep'?'depotbuild':'staup',k==='ctrsta'?W.sid:'');if(coErr)flash(coErr,!String(coErr).startsWith('✓')&&coErr!=='Working…');return}return o.apply(this,arguments)}}
