//@src 16p_stations.js
// ============================================================ Stations, their buildings and your capital ships (Beyond stage 11)
// A Station is an upgraded Depot (a Capital Keel, 2 Depot Frames and a Compact Seal, from its store or your hold). It counts
// for the system (a Depot doesn't), has a stronger hull and shield, and grows by buildings: each level adds one building of
// your choice around it, up to five: shipyard, external storage, defence platform, hangar, forge, market wing. Level = the
// number of buildings (at least 1). The shipyard builds hulls for you (your own design line) and capital ships: Escorts from
// level 3 and Carriers at level 5 (the destroyer comes with its model).
const STA={cost:{keel:1,frame:2,seal:1},bcost:{frame:1,plate:20,coil:4},hK:1.8,
  B:{yard:['Shipyard','builds hulls for you, and capital ships: Escorts from level 3, Carriers at level 5'],storage:['External storage','traders take and bring twice the lot'],defence:['Defence platform','+50% to the guns and +50% hull'],
     hangar:['Hangar','room for two more crews'],forge:['Forge','a workshop and forge with no fee'],market:['Market wing','traders call twice as often and pay 10% more']}};
function isPSta(R){return!!R&&R.owner==='player'&&!!R.pst}
function staLvl(R){return Math.max(1,(R.bld||[]).length)}
function hasB(R,k){return!!R&&(R.bld||[]).includes(k)}
// a Depot doesn't hold the system for you; a Station does
{const o=sectorOwner;sectorOwner=function(id){const R=S.stations[id];if(R&&R.owner==='player'&&R.kind==='depot'&&!R.pst){const d=DEF[id];if(d.home)return d.home;const oid=OUT_BY_SECTOR[id];return oid?S.outposts[oid].owner:null}return o.apply(this,arguments)}}
function staUp(P,R){if(!R||R.owner!=='player'||(R.pid||'me')!==pkeyOf(P))return'Not your depot.';if(R.pst)return'It is already a Station.';const srcs=[P.cargo,R.stock];
  if(!haveIn(STA.cost,srcs))return`A Station needs a Station Kit in your hold or the depot's store: one purchase on a station's Market (it rides in a Heavy Hauler).`;takeFrom(STA.cost,srcs);inv.addAll(R.fort=R.fort||{},STA.cost);R.pst=1;R.bld=[];R.hMax=Math.round(R.hMax*STA.hK);R.sMax=Math.round(R.sMax*STA.hK);R.hull=R.hMax;R.shield=R.sMax;
  R.name=`${DEF[R.sid].name} Station`;return`✓ ${R.name}: it holds ${DEF[R.sid].name} for you now. Add a building at each level (Company → Holdings).`}
function staBuild(P,R,k){if(!isPSta(R)||(R.pid||'me')!==pkeyOf(P))return'Not your station.';if(!STA.B[k])return'No such building.';if(hasB(R,k))return'It already has one.';if((R.bld||[]).length>=5)return'All five building berths are taken.';
  const srcs=[P.cargo,R.stock];if(!haveIn(STA.bcost,srcs))return`A building needs ${lackText(STA.bcost,Object.assign({},R.stock,P.cargo))}.`;takeFrom(STA.bcost,srcs);inv.addAll(R.fort=R.fort||{},STA.bcost);R.bld.push(k);
  if(k==='defence'){R.hMax=Math.round(R.hMax*1.5);R.hull=Math.min(R.hMax,R.hull*1.5)}if(k==='yard')S.yards[yardKeyOf(R)]={sector:R.sid,fort:{},pst:R.sid};return`✓ ${STA.B[k][0]} built: ${R.name} is level ${staLvl(R)}.`}
function yardKeyOf(R){return R.pid&&R.pid!=='me'?'p:'+R.pid:'player'}
// building effects
{const o=crewCap;crewCap=function(R){return o.apply(this,arguments)+(hasB(R,'hangar')?2:0)}}
{const o=depGunK;depGunK=function(SE,t){const v=o.apply(this,arguments);return SE&&SE.rec&&hasB(SE.rec,'defence')?v*1.5:v}}
{const o=dockCtx;dockCtx=function(){const c=o.apply(this,arguments);const P=S.player;if(c&&c.kind==='station'&&c.owner==='player'){const R=S.stations[P.sector];if(isPSta(R)){c.sub=`Your station · level ${staLvl(R)} · ${DEF[R.sid].name} · ${(R.bld||[]).map(k=>STA.B[k][0]).join(', ')||'no buildings yet'}`;if(hasB(R,'forge')){c.fab=true;c.forge=true;c.fee=false}if(hasB(R,'yard'))c.hulls=true}}return c}}
// capitals at your station's shipyard: an Escort from level 3, a Carrier at level 5 (DG1's capital slips, for your company)
function capBuild(P,R,kind){if(!isPSta(R)||!hasB(R,'yard'))return'Capital ships need your station\'s shipyard.';const need=kind==='esc'?3:5;if(staLvl(R)<need)return`${kind==='esc'?'An Escort':'A Carrier'} needs a level ${need} station.`;
  const k=yardKeyOf(R),type=kind==='esc'?'escbuild':'frigbuild',cost=kind==='esc'?escCost('player'):carCostF('player'),srcs=[P.cargo,R.stock];if(S.events.some(e=>e.type===type&&e.att===k&&e.stage!=='done'))return'A ship of that kind is already in the slip.';
  if(kind==='esc'&&S.frigates.filter(t=>fMine(t)&&isEsc(t)).length>=ESC_CAP.player)return`You can keep ${ESC_CAP.player} escorts.`;if(kind!=='esc'&&S.frigates.filter(t=>fMine(t)&&isCar(t)).length>=1)return'You can keep one carrier.';
  if(!haveIn(cost,srcs))return`It needs ${lackText(cost,Object.assign({},R.stock,P.cargo))}.`;S.yards[k]=S.yards[k]||{sector:R.sid,fort:{},pst:R.sid};const force={};takeFrom(cost,srcs);inv.addAll(force,cost);
  S.events.push({id:S.nextId++,type,t0:S.T,yard:k,att:k,sector:R.sid,force,until:S.T+(kind==='esc'?ESCORT_TIME:FRIGATE_TIME),stage:'building'});return`✓ ${kind==='esc'?'An Escort':'A Carrier'} is laid down in your slip at ${R.name}.`}
{const o=dockAction;dockAction=function(act,arg){const P=S.player;
  if(act==='staup'){dockErr=staUp(P,S.stations[arg]);return}
  if(act==='stabld'){const[sid,k]=String(arg).split(':');dockErr=staBuild(P,S.stations[sid],k);return}
  if(act==='capbld'){const[sid,k]=String(arg).split(':');dockErr=capBuild(P,S.stations[sid],k);return}return o.apply(this,arguments)}}
{const o=coClick;coClick=function(act,arg){if(['staup','stabld','capbld'].includes(act)){if(NET.cl){netSend({t:'act',act,arg});coErr='Working…';renderCompany();return}dockAction(act,arg);coErr=dockErr;renderCompany();return}return o.apply(this,arguments)}}
// Holdings: each depot's road to a Station, and each Station's buildings and slips
{const o=holdingsHtml;holdingsHtml=function(P){let h=o.apply(this,arguments);const D=myDepots(P);if(!D.length)return h;
  h+=`<div class="h3" style="margin-top:16px">Stations</div><p class="note" style="margin:0 0 8px">Upgrade a Depot to a Station with a Station Kit (in its store or your hold): one purchase on a station's Market (it rides in a Heavy Hauler). A Station holds the system for you and grows one building per level, up to five; each building takes a Depot Frame, 20 Alloy Plate and 4 Flux Coils.</p>`;
  for(const R of D){if(!R.pst){h+=`<div style="margin:4px 0"><b>${esc(R.name)}</b> <button class="btn sm" type="button" data-co="staup" data-arg="${R.sid}" ${kitOr(STA.cost,[P.cargo,R.stock],'kit_station')?'':'disabled'}>Upgrade to a Station · a Station Kit</button></div>`;continue}
    h+=`<div style="border-top:1px solid var(--line);padding:6px 0"><b>${esc(R.name)}</b> · level ${staLvl(R)} · ${(R.bld||[]).map(k=>esc(STA.B[k][0])).join(', ')||'no buildings yet'}<div class="act" style="flex-wrap:wrap;margin-top:4px">`;
    if((R.bld||[]).length<5)for(const k in STA.B)if(!hasB(R,k))h+=`<button class="btn sm" type="button" data-co="stabld" data-arg="${R.sid}:${k}" title="${esc(STA.B[k][1])}" ${haveIn(STA.bcost,[P.cargo,R.stock])?'':'disabled'}>${esc(STA.B[k][0])}</button>`;
    if(hasB(R,'yard'))h+=`<button class="btn sm" type="button" data-co="capbld" data-arg="${R.sid}:esc" ${staLvl(R)>=3&&haveIn(escCost('player'),[P.cargo,R.stock])?'':'disabled'}>Escort (level 3)</button><button class="btn sm" type="button" data-co="capbld" data-arg="${R.sid}:car" ${staLvl(R)>=5&&haveIn(carCostF('player'),[P.cargo,R.stock])?'':'disabled'}>Carrier (level 5)</button>`;
    const slip=S.events.find(e=>(e.type==='escbuild'||e.type==='frigbuild')&&e.att===yardKeyOf(R)&&e.stage==='building');if(slip)h+=`<span class="note">${slip.type==='escbuild'?'Escort':'Carrier'} in the slip: ${fmtT(Math.max(0,slip.until-S.T))}</span>`;h+='</div></div>'}return h}}
