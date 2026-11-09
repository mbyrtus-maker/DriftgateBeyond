//@src 16zzzl_orejobs.js
// ============================================================ Beyond: makers ask for Aurorite and Vantium; Riftstone covers a shortage (user, 9 Nov 2026)
// "Makers need to request it be mined. Job creation." (whenever they're short; no recipe change) and "If a power or maker is
// short an ore, Riftstone black market missions should go live since it's a wild card ore and can make anything" (a
// delivered Riftstone "stands in for one ore unit").
//   (user, 9 Nov 2026: "Makers don't store those ores; they go to the powers to make the new components that makers need.")
//   Ore requests (Jobs, mining): a maker whose host (the power whose station holds its works, or the Compact at a freeport)
//     has under OREQ.low of Aurorite or Vantium posts a job to bring it up to OREQ.keep, one maker per host and ore at a time,
//     at stations within 3 jumps of the works. Delivered at the works (part loads too) into the host's store, for OREQ.k × the
//     ore's base value a unit from the maker's purse; open OREQ.life, then posted again while still short.
//   Riftstone (Jobs → Black market): a power whose warehouse holds under RSJ.low of an ore, or a freeport hosting makers whose
//     ore request has gone unfilled for RSJ.wait, has a quiet buyer at its station ask for Riftstone. Each delivered
//     Riftstone stands in for one unit of the short ore: the rift pulls that unit out of the outer drift (S.drift) into the
//     buyer's store, and the Riftstone's own makings go into the drift. One the drift can't cover goes into the buyer's store
//     as Riftstone. Riftstone is Light heat everywhere if a scan catches it (user: "Rift stone causes light heat everywhere").
// Host only; goods and credits only move, so the ledger stays exact.
const OREQ={ores:['au','nu'],keep:60,low:40,k:1.5,life:1800,near:3,every:60};
const RSJ={low:50,n:20,k:3.3,life:1800,every:60,wait:600};
ITEMS.rift.legal=[];
{const o=contraFor;contraFor=function(){const L=o.apply(this,arguments);for(const x of L)if(x.k==='rift'&&x.why==='cash')x.why='Light';return L}}
function oreqAll(){return S.oreq=S.oreq||[]}
function rsjAll(){return S.rsj=S.rsj||[]}
function oreqHost(m){const R=mkAtHome(m);return R?storeOf(R):null}
function rsjBuyerName(by){return by==='neutral'?'the Freeport Compact':FACTIONS[by]?FACTIONS[by].name:sideName(by)}
function rsjStoreOf(j){const R=S.stations[j.sid];return j.by==='neutral'?(R?storeOf(R):null):S.econ.stock[j.by]}
function rsjRating(){return'Light'}
function oreqTick(){if(NET.cl||!S||S.training||S.unb||!S.econ)return;const T=S.T;if(T<(S.oreqT||0))return;S.oreqT=T+OREQ.every;
  const L=oreqAll();for(let i=L.length-1;i>=0;i--){const j=L[i];if(T>j.until||j.got>=j.n||!ceAlive(j.m))L.splice(i,1)}
  for(const m in MAKERS){if(!ceAlive(m))continue;const R=mkAtHome(m);if(!R)continue;const st=storeOf(R);if(!st)continue;
    for(const e of OREQ.ores){const have=st[e]||0;if(have>=OREQ.low||L.some(j=>j.to===R.sid&&j.ore===e))continue;L.push({id:S.nextId++,m,ore:e,n:OREQ.keep-have,got:0,to:R.sid,unit:Math.round(baseValue(e)*OREQ.k),T0:T,until:T+OREQ.life})}}
  const Q=rsjAll();for(let i=Q.length-1;i>=0;i--){const j=Q[i];if(T>j.until||j.got>=j.n)Q.splice(i,1)}
  const want=[];for(const f of FAC_IDS){const R=S.stations[FAC_HOME(f)];if(!R||R.owner!==f)continue;const st=S.econ.stock[f]||{};for(const e of RAWS)if((st[e]||0)<RSJ.low)want.push({by:f,ore:e,sid:R.sid,n:RSJ.n})}
  for(const j of L){const R=S.stations[j.to];if(!R||R.owner!=='neutral'||T-j.T0<RSJ.wait)continue;if(!want.some(w=>w.by==='neutral'&&w.sid===R.sid&&w.ore===j.ore))want.push({by:'neutral',ore:j.ore,sid:R.sid,n:Math.max(4,j.n-j.got)})}
  for(const w of want){if(Q.some(j=>j.by===w.by&&j.sid===w.sid&&j.ore===w.ore))continue;const rating=rsjRating();Q.push({id:S.nextId++,...w,got:0,rating,unit:Math.round(baseValue('rift')*RSJ.k*(1+(BM_RATE[rating]||0))),T0:T,until:T+RSJ.life})}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{oreqTick()}catch(e){console.error(e)}return r}}
// ---- delivering
function oreqDeliver(P,id){const j=oreqAll().find(x=>String(x.id)===String(id));if(!j)return'That request is over.';if(P.sector!==j.to||P.docked!=='station')return`Deliver at ${S.stations[j.to].name}.`;
  const per=Math.max(1,j.unit),can=Math.floor(ceT(j.m)/per);let d=Math.min(j.n-j.got,P.cargo[j.ore]||0,can);if(d<=0)return(P.cargo[j.ore]||0)?`${MAKERS[j.m].short} can't pay for more just now.`:`No ${ITEMS[j.ore].name} in your hold.`;
  inv.take(P.cargo,j.ore,d);inv.add(oreqHost(j.m)||storeOf(S.stations[j.to]),j.ore,d);const got=transfer(ceW(j.m),'player',d*per);j.got+=d;if(j.got>=j.n)oreqAll().splice(oreqAll().indexOf(j),1);
  return`✓ Delivered ${d} ${ITEMS[j.ore].name} for ${MAKERS[j.m].name} to ${S.stations[j.to].name}'s works: +${fmt(got)} cr.${j.got<j.n?` ${j.n-j.got} more wanted.`:''}`}
function rsjDeliver(P,id){const j=rsjAll().find(x=>String(x.id)===String(id));if(!j)return'That buyer has gone quiet.';if(P.sector!==j.sid||P.docked!=='station')return`The buyer is at ${S.stations[j.sid].name}.`;
  const per=Math.max(1,j.unit),w=j.by,can=Math.floor((S.econ.treasury[w]||0)/per);let d=Math.min(j.n-j.got,P.cargo.rift||0,can);if(d<=0)return(P.cargo.rift||0)?'The buyer can\'t pay for more just now.':'No Riftstone in your hold.';
  const st=rsjStoreOf(j);if(!st)return'The buyer has nowhere to put it.';S.drift=S.drift||{};const rc=comp('rift');let stood=0;
  for(let i=0;i<d;i++){inv.take(P.cargo,'rift',1);if((S.drift[j.ore]||0)>=1){S.drift[j.ore]-=1;for(const e of RAWS)S.drift[e]=(S.drift[e]||0)+rc[e];inv.add(st,j.ore,1);stood++}else inv.add(st,'rift',1)}
  const got=transfer(w,'player',d*per);bmoHeat(P,S.stations[j.sid]&&S.stations[j.sid].owner,'Light','a Riftstone sale');j.got+=d;if(j.got>=j.n)rsjAll().splice(rsjAll().indexOf(j),1);
  return`✓ ${d} Riftstone to ${rsjBuyerName(j.by)}'s buyer: +${fmt(got)} cr. ${stood?`${stood} stood in for ${ITEMS[j.ore].name}`:'The rift had nothing to pull'}${stood<d&&stood?`; ${d-stood} kept as Riftstone`:''}.`}
{const o=dockAction;dockAction=function(act,arg){if(act==='oreqdel'){if(NET.cl)return o.apply(this,arguments);dockErr=oreqDeliver(S.player,arg);return}if(act==='rsjdel'){if(NET.cl)return o.apply(this,arguments);dockErr=rsjDeliver(S.player,arg);return}return o.apply(this,arguments)}}
// ---- the Jobs board
{const o=jobsList;jobsList=function(c,P,srcs){const out=o.apply(this,arguments);try{if(S.unb||!c||c.kind!=='station')return out;const hop=sid=>HOP[P.sector]&&HOP[P.sector][sid]!=null?HOP[P.sector][sid]:0,far=n=>n?`${n} jump${n>1?'s':''}`:'here';
  for(const j of oreqAll()){const h=hop(j.to);if(h>OREQ.near)continue;const here=P.sector===j.to,have=P.cargo[j.ore]||0,left=j.n-j.got,R=S.stations[j.to];if(!R)continue;
    out.push({id:'oq:'+j.id,by:'corp_'+j.m,sid:j.to,ty:'mine',title:`Mine ${left} ${esc(ITEMS[j.ore].name)} for ${esc(MAKERS[j.m].short)}`,sub:`deliver at ${esc(R.name)} · ${fmt(j.unit)} cr a unit · ${Math.max(0,Math.round((j.until-S.T)/60))} min left`,hops:h,where:far(h),payN:j.unit*left,pay:`${fmt(j.unit*left)} cr`,
      btn:here&&have?['oreqdel',j.id,`Deliver ${Math.min(have,left)}`]:!here?['croute',j.to,'Set course']:null,need:here&&!have?`No ${ITEMS[j.ore].name} in your hold.`:'',
      detail:()=>`<p class="note" style="margin:0">${esc(MAKERS[j.m].name)} needs ${esc(ITEMS[j.ore].name)} for the components ${esc(R.owner==='neutral'?'the Compact':FACTIONS[R.owner].short)} makes for it, and pays ${fmt(j.unit)} cr a unit for up to ${left}, delivered at its works at ${esc(R.name)} (part loads welcome). ${esc(ITEMS[j.ore].name)} is in the rock of ${esc(Object.keys(DEF).filter(s=>(DEF[s].ores||{})[j.ore]).slice(0,4).map(s=>DEF[s].name).join(', '))}${Object.keys(DEF).filter(s=>(DEF[s].ores||{})[j.ore]).length>4?' and more':''}.</p>`})}
  for(const j of rsjAll()){const h=hop(j.sid);if(h>3)continue;const here=P.sector===j.sid,have=P.cargo.rift||0,left=j.n-j.got,R=S.stations[j.sid];if(!R)continue;
    out.push({id:'rs:'+j.id,bm:1,by:j.by,sid:j.sid,ty:'haul',title:`Riftstone for ${esc(rsjBuyerName(j.by))}: ${left} to ${esc(R.name)}`,sub:`short of ${esc(ITEMS[j.ore].name)} · Light heat · ${fmt(j.unit)} cr a unit`,hops:h,where:far(h),payN:j.unit*left,pay:`${fmt(j.unit*left)} cr`,
      btn:here&&have?['rsjdel',j.id,`Deliver ${Math.min(have,left)}`]:!here?['croute',j.sid,'Set course']:null,need:here&&!have?'No Riftstone in your hold.':'',
      detail:()=>`<p class="note" style="margin:0">A quiet buyer for ${esc(rsjBuyerName(j.by))} wants Riftstone: they're short of ${esc(ITEMS[j.ore].name)}, and a Riftstone stands in for one unit of any ore (the rift pulls it out of the outer drift). Cut it from a rift rock (they discharge: keep your shields up) and bring it here. Riftstone is contraband everywhere: the sale brings Light heat with ${esc(R.owner==='neutral'?'the Compact (its standing)':FACTIONS[R.owner].short)}, and a patrol that scans it in your hold adds more.</p>`})}}catch(err){console.error(err)}return out}}
{const o=jbIssuer;jbIssuer=function(j){if(j&&j.bm&&String(j.id).startsWith('rs:'))return`A quiet buyer (${rsjBuyerName(j.by)})`;return o.apply(this,arguments)}}
