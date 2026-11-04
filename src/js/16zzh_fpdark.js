//@src 16zzh_fpdark.js
// ============================================================ freeports never fall (Beyond, 3 Nov 2026)
// The user's call: the Brood can assault a freeport and disable it, but it comes back on in five minutes and is never
// destroyed. Where the Brood (taking a system, or breaking its hull) would raze a freeport, it goes dark instead: no
// docking, market or jobs and its guns silent, for five minutes; then it relights at half hull with full shields. A
// freeport an older galaxy lost is rebuilt when the game loads. (Scrapheart works the same way, for 30 minutes.)
const FPD={down:300,back:.5};
function fpDark(sid){const D=S&&S.fpDark;return!!(D&&D[sid]&&S.T<D[sid])}
function fpKnock(sid){S.fpDark=S.fpDark||{};if(fpDark(sid))return;try{const R0=S.stations[sid];if(R0)distressCall(sid,R0.name,'neutral','brood')}catch(e){}S.fpDark[sid]=S.T+FPD.down;const R=S.stations[sid];if(R){R.hull=1;R.shield=0}
  allFeed(`⚠ ${R?R.name:'A freeport'} is knocked out by the Brood: dark for ${FPD.down/60} minutes.`,'warn');if(W&&W.sid===sid&&W.stationEnt)W.stationEnt.offline=W.t+FPD.down;
  for(const P of[S.player,...Object.values(S.pilots||{})])if(P&&P.sector===sid&&P.docked==='station'){P.docked=null}}
function fpIs(sid){return FREEPORTS.some(f=>f.sid===sid)}
{const o=razeStation;razeStation=function(sid,by){const R=S.stations[sid];if(R&&R.owner==='neutral'&&fpIs(sid)){fpKnock(sid);return}return o.apply(this,arguments)}}
{const o=damageStation;damageStation=function(E,dmg,by,kind,src){if(E&&E.rec&&E.rec.owner==='neutral'&&fpIs(E.rec.sid)&&fpDark(E.rec.sid))return;const r=o.apply(this,arguments);
  try{const R=E&&E.rec;if(!NET.cl&&R&&R.owner==='neutral'&&fpIs(R.sid)&&R.hull<=1&&!fpDark(R.sid))fpKnock(R.sid)}catch(e){console.error(e)}return r}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{if(NET.cl||!S)return r;
    for(const sid in S.fpDark||{}){if(S.T<S.fpDark[sid])continue;delete S.fpDark[sid];const R=S.stations[sid];if(R){R.hull=Math.max(R.hull,Math.round(R.hMax*FPD.back));R.shield=R.sMax}if(W&&W.sid===sid&&W.stationEnt)W.stationEnt.offline=0;allFeed(`${R?R.name:'The freeport'} is lit again: open for trade.`,'good')}
    // an older galaxy's lost freeport comes back at once
    for(const F of FREEPORTS){if(S.stations[F.sid])continue;const R=makeStation(F.sid,'neutral','free',{x:0,y:0,z:0},{});R.dev={life:0,def:0,store:0,prod:0,armor:0};applyDev(R);R.hull=Math.round(R.hMax*FPD.back);if(S.fpDown)delete S.fpDown[F.sid];
      if(WORLDS[F.sid])inW(WORLDS[F.sid],()=>{if(!W.stationEnt)addStationEnt(R)});allFeed(`The Freeport Compact has rebuilt ${R.name} in ${DEF[F.sid].name}. It's open for trade again.`,'good')}}catch(e){console.error(e)}return r}}
// dark: no docking, market or jobs; its guns hold
{const o=dockCtx;dockCtx=function(){const c=o.apply(this,arguments);try{const P=S.player;if(c&&c.kind==='station'&&c.owner==='neutral'&&fpDark(P.sector)){c.market=null;c.contracts=false;c.hulls=false;c.sub=`${c.name} · knocked out · back in ${fmtT(Math.max(0,S.fpDark[P.sector]-S.T))}`}}catch(e){}return c}}
{const o=canDock;canDock=function(E){if(E&&E.rec&&E.rec.owner==='neutral'&&fpDark(E.rec.sid))return false;return o.apply(this,arguments)}}
{const o=stHostile;stHostile=function(SE,e){if(SE&&SE.rec&&SE.rec.owner==='neutral'&&fpDark(SE.rec.sid))return false;return o.apply(this,arguments)}}
// ---- (user) freeports call for help and are hard to break: they already send a distress call when hit (the powers answer
// with wings, and every pilot hears it); now one goes out too when the Brood knocks one out or its swarm closes in, and
// their defences double: shields 3,600 → 7,200, hull 10,000 → 20,000, twelve turrets (from six) hitting harder (16 → 22)
// and reaching further (1,500 → 2,000 m)
Object.assign(STN.free,{sMax:7200,hMax:20000,tur:12,dmg:22,range:2000});
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{if(!NET.cl&&S&&S.fpDef!==2){S.fpDef=2;for(const F of FREEPORTS){const R=S.stations[F.sid];if(R&&R.owner==='neutral')applyDev(R)}}
  if(!NET.cl&&S&&S.events)for(const ev of S.events){if(ev.att!=='brood'||ev.stage==='done'||ev.fpCall||!fpIs(ev.sector))continue;const R=S.stations[ev.sector];if(!R||R.owner!=='neutral')continue;if(ev.stage==='engaged'||(ev.eta&&ev.eta-S.T<60)){ev.fpCall=1;distressCall(ev.sector,R.name,'neutral','brood')}}}catch(e){console.error(e)}return r}}
// twelve turrets: the station's base list holds six, so a freeport gets the rest (placed on its hull with the others)
{const o=addStationEnt;addStationEnt=function(R){const r=o.apply(this,arguments);try{const E=(r&&r.type==='station')?r:W.stationEnt;if(E&&R&&R.kind==='free'){while(E.turrets.filter(t=>!t.mod).length<STN.free.tur)E.turrets.push({p:[0,0,0],aim:{x:0,y:0,z:1},cool:rnd(.6)})}}catch(e){}return r}}
