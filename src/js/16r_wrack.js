//@src 16r_wrack.js
// ============================================================ Scrapheart Haven for contractors (Beyond stage 12b)
// The Wrack sits hidden inside deep space. Its haven, Scrapheart, is neutral ground for contractors who keep the peace: its
// guns and the Unbound ships in the Wrack leave you alone unless you've attacked the Unbound in the last minute. Dock there
// for its market (sell anything: stolen goods and contraband included; the Unbound's stores buy and sell, paid from their
// treasury) and the Rusty Tankard's rumours: black-market runs out of Scrapheart into the powers' stations, paid by the
// Unbound. The Unbound fly bigger holds than they did.
const WRACK={sid:'wr',holdK:1.4};
for(const k of['raider','corsair','plunderer','uskiff'])if(CLASSES[k])CLASSES[k].cargo=Math.round(CLASSES[k].cargo*WRACK.holdK);
function wrHaven(R){return!!R&&R.owner==='pirate'&&R.sid===WRACK.sid}
function wrPeace(P){return!!P&&!P.sworn&&!(P.aggro&&P.aggro.pirate>S.T)}
{const o=tradeOK;tradeOK=function(P,owner){if(owner==='pirate'&&!S.unb){P=P||S.player;return!!P&&!P.sworn&&wrPeace(P)&&P.sector===WRACK.sid}return o.apply(this,arguments)}}
{const o=pilotHostile;pilotHostile=function(P,x){if(x==='pirate'&&!S.unb&&W&&W.sid===WRACK.sid&&wrPeace(P||S.player))return false;return o.apply(this,arguments)}}
{const o=dockCtx;dockCtx=function(){const c=o.apply(this,arguments);const P=S.player;if(S.unb||!c||c.kind!=='station'||c.owner!=='pirate')return c;const R=S.stations[P.sector];if(!wrHaven(R))return c;
  return Object.assign(c,{haven:false,rum:true,market:mkStock(R),wallet:'pirate',fee:true,contracts:true,storage:P.vault,storageName:'Vault',sub:`Scrapheart Haven · the Unbound's port · The Wrack · neutral ground while you keep the peace`})}}
// the Rusty Tankard's rumours: black-market runs out of Scrapheart, paid by the Unbound
{const o=fixerTick;fixerTick=function(){o.apply(this,arguments);if(NET.cl||S.training||S.unb)return;const R=S.stations[WRACK.sid];if(!wrHaven(R))return;S.bm=S.bm||[];if(S.bm.filter(x=>x.from===WRACK.sid&&!x.taken).length>=BM_MAX||Math.random()>.2)return;
  const st=mkStock(R),goods=Object.keys(st).filter(k=>(st[k]||0)>=6&&ITEMS[k]&&!ITEMS[k].part&&!String(k).startsWith('v_'));if(!goods.length)return;const dests=Object.keys(S.stations).filter(s=>{const D=S.stations[s];return D&&FAC_IDS.includes(D.owner)&&HOP[WRACK.sid]&&HOP[WRACK.sid][s]!=null&&HOP[WRACK.sid][s]<=6});if(!dests.length)return;
  const to=pick(dests),f=S.stations[to].owner,core=S.stations[to].kind==='core',rating=core?'Severe':'Heavy',item=pick(goods),n=Math.min(st[item],ri(5,12));
  S.bm.push({id:S.nextId++,from:WRACK.sid,to,f,item,n,rating,payer:'pirate',rum:1,pay:Math.round(baseValue(item)*n*(1+BM_RATE[rating])+250+80*HOP[WRACK.sid][to]),until:S.T+900})}}
{const o=jobsList;jobsList=function(c,P,srcs){const out=o.apply(this,arguments);if(!c||!c.rum)return out;try{for(const x of(S.bm||[]).filter(x=>x.from===P.sector&&!x.taken&&S.T<x.until)){const h=HOP[P.sector][x.to],fs=FACTIONS[x.f].short;
    out.push({id:'bmr:'+x.id,by:'pirate',sid:x.to,ty:'haul',title:`Rumour at the Rusty Tankard: ${x.n} ${esc(ITEMS[x.item].name)} into ${esc(S.stations[x.to].name)}`,sub:`${x.rating} heat with ${esc(fs)} if caught`,hops:h,where:`${h} jump${h===1?'':'s'}`,payN:x.pay,pay:`${fmt(x.pay)} cr`,btn:P.run?null:['bmtake',x.id,'Take the run'],need:P.run?'You are already on a run.':'',
      detail:()=>`<p class="note" style="margin:0">Unbound goods, loaded into your hold here. Dock at ${esc(S.stations[x.to].name)} to hand them over; the Unbound pay. ${esc(fs)} patrols treat them as contraband: <b>${x.rating}</b> heat with ${esc(fs)} if a scan finds them.</p>`})}}catch(err){console.error(err)}return out}}
// the run's goods come out of the Unbound's stores; delivery is paid by whoever posted the run
{const o=dockAction;dockAction=function(act,arg){if(act==='bmtake'){const x=(S.bm||[]).find(y=>String(y.id)===String(arg)&&!y.taken);if(x&&x.from===WRACK.sid){const P=S.player,st=mkStock(S.stations[x.from]),m=mass(x.item)*x.n,room=W&&W.player?W.player.st.cargo-invMass(P.cargo):0;
    if(P.run){dockErr='You are already on a run.';return}if(room<m){dockErr=`It needs ${m} t of hold space.`;return}const n=inv.take(st,x.item,x.n);if(!n){dockErr='The goods are gone.';return}inv.add(P.cargo,x.item,n);x.taken=1;P.run={id:x.id,item:x.item,n,f:x.f,to:x.to,rating:x.rating,pay:Math.round(x.pay*n/x.n),payer:'pirate'};P.route=x.to;
    dockErr=`✓ Loaded ${n} ${ITEMS[x.item].name}. Course set to ${S.stations[x.to].name}: ${x.rating} heat with ${FACTIONS[x.f].short} if you're caught.`;return}}return o.apply(this,arguments)}}
{const o=openDock;openDock=function(){const P=S.player,R=P&&P.run;if(R&&R.payer==='pirate'&&!NET.cl&&P.docked==='station'&&P.sector===R.to){const st=mkStock(S.stations[R.to]),n=inv.take(P.cargo,R.item,R.n);inv.add(st,R.item,n);const pay=transfer('pirate','player',Math.round(R.pay*n/R.n));P.run=null;feed(`✓ Run delivered: ${n} ${ITEMS[R.item].name}, +${fmt(pay)} cr from the Unbound.`,'good');try{rpAdd(P,RATING.run,'a black-market run')}catch(e){}}return o.apply(this,arguments)}}
// Scrapheart's guns hold their fire on contractors keeping the peace (attacking the Unbound breaks it for a minute)
{const o=stHostile;stHostile=function(SE,e){if(!S.unb&&SE&&SE.fac==='pirate'&&W&&W.sid===WRACK.sid){const P=pilotOfEnt(e);if(P&&wrPeace(P))return false}return o.apply(this,arguments)}}
// attacking the Unbound breaks the peace for a minute
{const o=standHit;standHit=function(P,f){if(f==='pirate'&&P&&!S.unb)(P.aggro||(P.aggro={})).pirate=S.T+STAND.aggro;return o.apply(this,arguments)}}
