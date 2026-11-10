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
// ---- (user, 9 Nov 2026: "I cannot dock at my Lair" / "it worked after a bit") a new Lair takes 60 s to build; near your own
// Lair the prompt now says so, with the seconds left, and once it's ready "E — dock at your Lair"
{const o=hudUpdate;hudUpdate=function(){const r=o.apply(this,arguments);try{if(!W||!W.player||S.player.docked||W.dead||S.unb||W.lairIn)return r;const el=$('hPrompt');if(!el||el.textContent)return r;const k=curPid()||'me',p=W.player;
  const L=(S.lairs||[]).find(x=>x.sid===W.sid&&x.hull>0&&x.pid===k&&d3(x,p)<600);if(!L)return r;
  el.innerHTML=`<span>${L.build>S.T?`Your Lair is still being built: ${Math.ceil(L.build-S.T)} s`:d3(L,p)<260?`${actKey()} — dock at your Lair`:'Your Lair: fly closer to dock'}</span>`}catch(e){}return r}}
// ---- (user, 9 Nov 2026: "it's not targetable though") your own Lairs in the system are targets: in the target cycle, with a
// panel (level, stash, building or ready, who has found it) and the autopilot flies you to it
function myLairsHere(){if(!W||!S)return[];const k=curPid()||'me';return(S.lairs||[]).filter(L=>L.sid===W.sid&&L.hull>0&&L.pid===k)}
{const o=targetables;targetables=function(){const out=o.apply(this,arguments);try{for(const L of myLairsHere())out.push({kind:'lair',ref:L})}catch(e){}return out}}
{const o=validTgt;validTgt=function(t){if(t&&t.kind==='lair')return myLairsHere().includes(t.ref);return o.apply(this,arguments)}}
{const o=tRad;tRad=function(t){if(t&&t.kind==='lair')return 90;return o.apply(this,arguments)}}
{const o=hudUpdate;hudUpdate=function(){const r=o.apply(this,arguments);try{if(W&&W.tgt&&W.tgt.kind==='lair'&&validTgt(W.tgt)&&W.player){const L=W.tgt.ref,d=Math.round(d3(L,W.player)),seen=Object.keys(L.seen||{}).filter(f=>L.seen[f]);
  $('hTgt').innerHTML=`<div class="tp"><div class="tn" style="color:#f0b24a">Your Lair</div><div class="ts">Level ${L.lvl||1} · stash ${invMass(L.stash||{})}/${typeof lairStash==='function'?lairStash(L):200} t${L.build>S.T?` · being built: ${Math.ceil(L.build-S.T)} s`:''}</div>
    <div class="row">Range<b>${fmt(d)} m</b></div><div class="row">Hull<b>${Math.round(L.hull)}</b></div><div class="ts">${seen.length?`<span style="color:var(--amber)">Found by ${seen.map(f=>esc(FACTIONS[f].short)).join(', ')}: their ships attack it on sight.</span>`:'Hidden: no power has found it.'}</div>
    <div class="ts">${L.build>S.T?'Not ready yet.':d<260?`${actKey()} to dock.`:`Fly within 260 m and press ${actKey()} to dock (${kb('autopilot')} flies you there).`}</div></div>`}}catch(e){}return r}}
