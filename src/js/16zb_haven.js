//@src 16zb_haven.js
// ============================================================ Scrapheart Haven knocked out: closed and looted (Beyond, 3 Nov 2026)
// Scrapheart can be deactivated but never destroyed. When its hull is broken it goes dark for 30 minutes: its market and the
// Rusty Tankard shut, the Unbound's raids thin to half, and their slip stops. Whoever broke it takes a quarter of every good
// in the Unbound's stores and a quarter of their treasury, moved into the attacker's own stores (a power's stocks and treasury,
// or a pilot's vault and credits), so the ledger stays exact. It comes back at half hull.
const HAVEN={down:1800,loot:.25,raids:.5,back:.5};
function havenDown(){return!!(S&&S.havenDown&&S.T<S.havenDown.until)}
function havenKnock(by,P){const R=S.stations.wr;if(!R||havenDown())return;S.havenDown={until:S.T+HAVEN.down,by};const st=S.econ.stock.pirate||{},got={};
  for(const k in st){const n=Math.floor((st[k]||0)*HAVEN.loot);if(n>0)got[k]=inv.take(st,k,n)}const cr=Math.floor((S.econ.treasury.pirate||0)*HAVEN.loot);
  let who;if(P){inv.addAll(P.vault=P.vault||{},got);payTo(P,'pirate',cr);who=P.name||'a pilot'}
  else if(FAC_IDS.includes(by)){inv.addAll(S.econ.stock[by],got);transfer('pirate',by,cr);who=FACTIONS[by].short}else{inv.addAll(S.econ.stock.pirate,got);who=null}
  const t=invMass(got);allFeed(`☠ Scrapheart Haven is knocked out${who?` by ${who}`:''}: dark for ${HAVEN.down/60} minutes, its market and the Rusty Tankard shut.${who?` ${t} t of plunder and ${fmt(cr)} cr carried off${P?` to your vault${P.vaultAt?' at '+vaultName(P.vaultAt):''}`:''}.`:''}`,'news');
  chron&&chron(`Scrapheart Haven was knocked out${who?' by '+who:''}.`);if(W&&W.sid==='wr'&&W.stationEnt)W.stationEnt.offline=W.t+HAVEN.down}
// its hull broken (it never falls)
{const o=damageStation;damageStation=function(E,dmg,by,kind,src){const r=o.apply(this,arguments);try{const R=E&&E.rec;if(!S.unb&&!NET.cl&&R&&R.sid==='wr'&&R.kind==='haven'&&R.hull<=1&&!havenDown()){const P=src&&src.rp?S.pilots[src.rp]:by==='player'?S.player:null;havenKnock(P?'player':sideNorm(by),P)}}catch(err){console.error(err)}return r}}
// coming back
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{if(!S.unb&&!NET.cl&&S.havenDown&&S.T>=S.havenDown.until){const R=S.stations.wr;S.havenDown=null;if(R){R.hull=Math.max(R.hull,Math.round(R.hMax*HAVEN.back));R.shield=R.sMax}allFeed('☠ Scrapheart Haven is lit again: its market and the Rusty Tankard reopen.','news')}}catch(err){console.error(err)}return r}}
// closed: no market, no rumours, no new runs; its guns stay dark
{const o=dockCtx;dockCtx=function(){const c=o.apply(this,arguments);if(c&&!S.unb&&havenDown()&&S.player&&S.player.sector==='wr'&&c.kind==='station'&&c.owner==='pirate'){c.market=null;c.rum=false;c.contracts=false;c.sub=`Scrapheart Haven · knocked out · back in ${fmtT(Math.max(0,S.havenDown.until-S.T))}`}return c}}
{const o=fixerTick;fixerTick=function(){if(havenDown()&&!S.unb){const n=(S.bm||[]).length;o.apply(this,arguments);if(S.bm)S.bm=S.bm.filter((x,i)=>i<n||x.from!=='wr');return}return o.apply(this,arguments)}}
{const o=stHostile;stHostile=function(SE,e){if(!S.unb&&SE&&SE.rec&&SE.rec.sid==='wr'&&havenDown())return false;return o.apply(this,arguments)}}
// the Unbound's raids thin out, and their slip stops, while the haven is dark
{const o=popWants;popWants=function(){const L=o.apply(this,arguments);if(!havenDown()||S.unb)return L;return L.map(w=>w[1]==='pirate'?[w[0],w[1],w[2],w[3]*HAVEN.raids,w[4]]:w)}}
{const o=pirTick;pirTick=function(){if(havenDown()&&!S.unb){for(const ev of S.events)if(ev.type==='pirbuild'&&ev.stage!=='done')ev.until+=10;return}return o.apply(this,arguments)}}
