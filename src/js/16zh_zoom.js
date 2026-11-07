//@src 16zh_zoom.js
// ============================================================ the strategic map zooms in; escort and patrol orders (Beyond section 9, 3 Nov 2026)
// The galaxy map (M) zooms into the selected system: the whole map becomes its sector view (live when the system is loaded,
// otherwise from your intel), with your capitals and crews named. Zoom with the side panel's button, a double click on a
// system or the mouse wheel; zoom out the same way (or the "◀ Galaxy" box). Two new orders for your capital ships:
//   Patrol: it sweeps the system and its neighbours (not the powers' home systems), two minutes in each, round and round;
//   Escort me: it follows you from system to system (in multiplayer, whoever gave the order).
// Guard here / Come here clear a patrol or an escort.
let mapZoom=null;
const ZM={stay:120};
{const o=drawMap;drawMap=function(){if(!mapZoom||!S||S.unb||S.training)return o.apply(this,arguments);try{capSightTick&&capSightTick()}catch(e){}
  const w=mcv.clientWidth,h=mcv.clientHeight;if(!w||!h)return;mcv.width=w*DPR;mcv.height=h*DPR;const c=mctx;c.setTransform(DPR,0,0,DPR,0,0);const sz=Math.min(w,h);
  c.fillStyle='#05080f';c.fillRect(0,0,w,h);c.save();c.translate((w-sz)/2,(h-sz)/2);const r=sxDraw({width:sz,height:sz,getContext:()=>c,noCap:true},mapZoom);zmLabels(c,sz,mapZoom);c.restore();
  c.fillStyle='rgba(16,22,36,.9)';c.fillRect(10,10,96,26);c.strokeStyle='#6fb7ff';c.strokeRect(10.5,10.5,95,25);c.fillStyle='#cfe3ff';c.font='12px sans-serif';c.fillText('◀ Galaxy',24,28);
  c.font='bold 15px sans-serif';c.fillStyle='#ece4cf';c.fillText(DEF[mapZoom].name.toUpperCase(),120,28);c.font='11px sans-serif';c.fillStyle='#9aa6bd';c.fillText(`${r.live?'live':'from intel'} · ${DEF[mapZoom].kind||''} · ${r.ships} ship${r.ships===1?'':'s'} · ${r.threats} threat${r.threats===1?'':'s'}`,120,44)}}
// (7 Nov 2026) the sector view's own caption (live or from intel, ships, threats) joins the one under the system's name at the
// top: at the foot of the square it was cut off in a short window
// names for your capitals and crews in the zoomed view
function zmLabels(c,sz,sid){const w=WORLDS[sid];if(!w)return;let R=2600;for(const g of GATES[sid]||[])R=Math.max(R,hyp(g.x,g.z)+400);const k=(sz/2-10)/R,X=x=>sz/2+x*k,Y=z=>sz/2+z*k;c.font='10px sans-serif';
  for(const e of w.ents){if(e.type!=='ship'||!e.alive)continue;let lab=null;if(e.tok&&fMine(e.tok))lab=e.tok.name;else if(e.crewId)lab=e.pname||'crew';else if(e.isPlayer)lab='you';else if(e.pname&&(e.leaderOf||e.dreadOf))lab=e.pname;if(!lab)continue;c.fillStyle=e.tok&&fMine(e.tok)?PLAYER_COL:'#ece4cf';c.fillText(lab,X(e.x)+6,Y(e.z)-5)}
  const R0=S.stations[sid];if(R0){c.fillStyle='#ece4cf';c.fillText(R0.name,X(R0.x)+10,Y(R0.z)+4)}}
function zmSet(sid){mapZoom=sid||null;if(sid)mapSel=sid;try{drawMap();renderMapSide()}catch(e){}}
// zooming: double click, the wheel, the "◀ Galaxy" box (a click in the zoomed view does nothing else)
mcv.addEventListener('click',e=>{if(!mapZoom)return;e.stopImmediatePropagation();const r=mcv.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top;if(x<110&&y<40)zmSet(null)},true);
mcv.addEventListener('dblclick',e=>{if(mapZoom||!S||S.unb||S.training)return;const r=mcv.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top;let best=null,bd=34;for(const d of SECTOR_DEFS){const[sx,sy]=mapXY(d,r.width,r.height),dd=hyp(sx-x,sy-y);if(dd<bd){bd=dd;best=d.id}}if(best)zmSet(best)});
mcv.addEventListener('wheel',e=>{if(!S||S.unb||S.training)return;if(e.deltaY<0&&!mapZoom&&mapSel){zmSet(mapSel);e.preventDefault()}else if(e.deltaY>0&&mapZoom){zmSet(null);e.preventDefault()}},{passive:false});
{const o=toggleMap;toggleMap=function(){if($('map').hidden)mapZoom=null;return o.apply(this,arguments)}}
// ---- the side panel: the zoom button and the new orders
{const o=sxHtml;sxHtml=function(sid){let h=o.apply(this,arguments);const P=S.player,mine=(S.frigates||[]).filter(t=>fMine(t)),me=pkeyOf(P);
  const zb=`<div class="act" style="margin:6px 0"><button class="btn sm" type="button" data-sx="zoom" data-arg="${mapZoom?'':sid}">${mapZoom?'◀ Back to the galaxy':'Zoom in ▸'}</button></div>`;h=h.replace('<div class="h3">Sector view</div>',`<div class="h3">Sector view</div>${zb}`);
  if(mine.length){h=h.replace(/<\/div>$/,'');h+=`<div class="h3" style="margin-top:8px">Patrols and escorts</div>`;
    for(const t of mine){const st=t.patrol?`patrolling around ${esc(DEF[t.patrol.base].name)}`:t.escort?`escorting ${t.escort.pid===me?'you':esc((xPilotOfKey(t.escort.pid)||{}).name||'a pilot')}`:'';
      h+=`<div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin:3px 0"><b>${esc(t.name)}</b>${st?`<span class="note" style="margin:0">${st}</span>`:''}<button class="btn sm" type="button" data-sx="patrol" data-arg="${t.id}" aria-pressed="${!!(t.patrol&&t.patrol.base===sid)}">Patrol ${esc(DEF[sid].name.split(' ')[0])}</button><button class="btn sm" type="button" data-sx="escort" data-arg="${t.id}" aria-pressed="${!!(t.escort&&t.escort.pid===me)}">Escort me</button></div>`}
    h+=`</div>`}return h}}
function zmRoute(sid){return[sid,...NEIGH[sid].filter(s=>!DEF[s].home&&DEF[s].kind!=='free'&&s!==WRACK.sid)]}
function zmOrder(P,act,arg){const[id,sid]=String(arg).split(':'),t=(S.frigates||[]).find(x=>String(x.id)===String(id)&&(x.side==='player'||x.owner===pkeyOf(P)));if(!t)return'';
  if(act==='patrol'){t.escort=null;t.patrol={base:sid,route:zmRoute(sid),i:0,next:0};t.dest=sid;t.jumpTo=null;return`${t.name} will patrol ${DEF[sid].name} and its neighbours.`}
  if(act==='escort'){t.patrol=null;t.escort={pid:pkeyOf(P)};t.dest=P.sector;t.jumpTo=null;return`${t.name} will escort you.`}return''}
{const o=sxOrder;sxOrder=function(act,arg){if(act==='zoom'){zmSet(arg||null);return''}
  if(act==='patrol'||act==='escort'){const a=`${arg}:${mapSel}`;if(NET.cl){netSend({t:'act',act:'zm'+act,arg:a});return'Working…'}const m=zmOrder(S.player,act,a);if(m)feed(m,'info');return m}
  if(act==='come'||act==='hold'){const t=(S.frigates||[]).find(x=>String(x.id)===String(arg)&&fMine(x));if(t){t.patrol=null;t.escort=null}}return o.apply(this,arguments)}}
{const o=dockAction;dockAction=function(act,arg){if(act==='zmpatrol'||act==='zmescort'){dockErr=zmOrder(S.player,act.slice(2),arg);return}return o.apply(this,arguments)}}
// the orders carried out (host): patrols move on after two minutes in each system; escorts follow their pilot
function zmTick(){if(NET.cl||!S||S.unb)return;for(const t of S.frigates||[]){if(!(t.side==='player'||t.owner))continue;
    if(t.patrol){const p=t.patrol,want=p.route[p.i%p.route.length];if(t.sector===want){if(!p.next)p.next=S.T+ZM.stay;else if(S.T>=p.next){p.i=(p.i+1)%p.route.length;p.next=0;t.dest=p.route[p.i];t.jumpTo=null}}else if(t.dest!==want){t.dest=want;t.jumpTo=null}}
    else if(t.escort){const P=xPilotOfKey(t.escort.pid);if(!P){t.escort=null;continue}if(P.sector&&t.sector!==P.sector&&t.dest!==P.sector){t.dest=P.sector;t.jumpTo=null}}}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{zmTick()}catch(err){console.error(err)}return r}}
// a contractor's capitals are based at their owner's own yard (the base lookup assumed a sworn pilot and failed otherwise)
{const o=capBase;capBase=function(t){if(t&&(t.side==='player'||t.owner)&&!S.unb){const k=t.owner&&t.owner!=='me'?'p:'+t.owner:'player';if(S.yards&&S.yards[k])return S.yards[k].sector;const f=t.side==='player'?sideNorm('player'):t.side;if(!FAC_IDS.includes(f))return t.sector}return o.apply(this,arguments)}}
