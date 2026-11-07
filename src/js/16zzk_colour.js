//@src 16zzk_colour.js
// ============================================================ your company's colour (Beyond, decided 2 Nov 2026; built 6 Nov 2026)
// You pick your company's colour with its name, from your first Depot (Holdings → Your brand), from a palette kept clear of
// the powers', the Brood's, the Unbound's and the Compact's colours. It shows wherever your company does: your Lairs, Depots
// and Stations (their lights, and their systems on the galaxy map), your AI pilots on radar, your declared faction. Free to
// change until you declare a faction; fixed after. Each pilot of a multiplayer galaxy has their own; your own screen draws
// "you" (PLAYER_COL) in yours. Nothing here touches the ledger.
// (7 Nov 2026) Crimson and Magenta kept (user): Forest and Bronze were tried for an hour and dropped. A save that holds
// one of those reads as the colour it replaced (CO_OLD).
const CO_PAL=[{n:'Gold',c:'#f0b24a'},{n:'Crimson',c:'#e0485e'},{n:'Rose',c:'#ff86b6'},{n:'Cobalt',c:'#4f7cff'},{n:'Sky',c:'#7cc0ff'},
  {n:'Magenta',c:'#e34fd6'},{n:'Lemon',c:'#f2ea55'},{n:'Pearl',c:'#e6ebf2'}];
const CO_DEF=CO_PAL[0].c,CO_OLD={'#078c19':CO_PAL[1].c,'#8c6407':CO_PAL[5].c};
function coCol(key){const N=S&&S.brandOf&&S.brandOf[key],B=N!=null&&S.brands&&S.brands[N],c=B&&B.col;return c?CO_OLD[c]||c:CO_DEF}
function coMine(){return coCol(pkeyOf(S.player))}
// the colour of whoever holds a system for 'player' (a pilot's Station there)
function coColAt(sid){const R=S.stations&&S.stations[sid];if(R&&R.owner==='player')return coCol(R.pid||'me');return PLAYER_COL}
// a company colour as a side name for the meshes: 'co:#rrggbb'
{const o=sideCol;sideCol=function(s){if(typeof s==='string'&&s.startsWith('co:'))return s.slice(3);return o.apply(this,arguments)}}
{const o=mdlPal;mdlPal=function(fac){if(typeof fac==='string'&&fac.startsWith('co:')){const F=hexRGB(fac.slice(3)),base=[.57,.58,.6];
  return{c:[mixC(base,F,.1),mixC([.36,.38,.43],F,.04),[.15,.16,.19],scaleC(F,.92),[.16,.3,.4],F,mixC([.2,.33,.42],F,.25),[.43,.4,.36],[.25,.23,.21]],e:[0,0,0,0,.15,.85,.4,0,0]}}return o.apply(this,arguments)}}
// each pilot's bases in their own colour; your Lairs (only your own are drawn) in yours
{const o=bmBase;bmBase=function(R,fac){if(fac==='player'&&R&&R.owner==='player')fac='co:'+coCol(R.pid||'me');return o.call(this,R,fac)}}
{const o=bmLair;bmLair=function(lvl,fac){if(fac==='player')fac='co:'+coMine();return o.call(this,lvl,fac)}}
// keep "you" in your colour: meshes drawn for the 'player' side are rebuilt when it changes
function coSync(){if(!S||!S.player)return;const c=coMine();if(c===PLAYER_COL)return;PLAYER_COL=c;for(const k of Object.keys(MESH))if(k.includes('player'))delete MESH[k]}
{const o=worldUpdate;worldUpdate=function(dt){const r=o.apply(this,arguments);try{coSync()}catch(e){}return r}}
{const o=drawMap;drawMap=function(){try{coSync()}catch(e){}return o.apply(this,arguments)}}
// choosing it (a dock action, so a guest's choice runs on the host)
function coSet(P,i){if(!myDepots(P).length)return'Your company picks its colour with its first Depot.';if(P.decl)return'Your colour is fixed now that you have declared a faction.';
  const C=CO_PAL[+i];if(!C)return'No such colour.';const N=brSlot(P,true);if(N==null)return'No brand slot free in this galaxy.';S.brands[N].col=C.c;return`✓ Your company's colour is now ${C.n}.`}
{const o=dockAction;dockAction=function(act,arg){if(act==='cocol'){dockErr=coSet(S.player,arg);return}return o.apply(this,arguments)}}
{const o=coClick;coClick=function(act,arg){if(act==='cocol'){if(NET.cl){netSend({t:'act',act,arg});coErr='Working…';renderCompany();return}dockAction(act,arg);coErr=dockErr;renderCompany();return}return o.apply(this,arguments)}}
// the picker, under the company name in Your brand
{const o=brHtml;brHtml=function(P){let h=o.apply(this,arguments);try{if(!myDepots(P).length)return h;const cur=coCol(pkeyOf(P)),fixed=!!P.decl;
  const row=`<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:8px"><span class="note" style="margin:0">Company colour</span>${CO_PAL.map((C,i)=>`<button class="btn sm" type="button" data-co="cocol" data-arg="${i}" title="${C.n}" aria-pressed="${C.c===cur}" ${fixed&&C.c!==cur?'disabled':''} style="min-width:0;padding:3px 8px;border-color:${C.c===cur?C.c:'var(--line)'}"><span style="display:inline-block;width:12px;height:12px;border-radius:3px;background:${C.c};vertical-align:-1px"></span> ${C.n}</button>`).join('')}<span class="note" style="margin:0">${fixed?'Fixed now that you have declared.':'Free to change until you declare a faction.'}</span></div>`;
  const at=h.indexOf('<div class="tblw">');if(at>=0)h=h.slice(0,at)+row+h.slice(at);else h+=row}catch(err){console.error(err)}return h}}
