//@src 16zv_claimfit.js
// ============================================================ Claim Beacons are fitted, one per utility slot (Beyond, 3 Nov 2026)
// A power's Claim Beacon (bought for Halcyon, Varkesh or Ostrova, in that power's colour) is a utility part: it takes a
// utility slot on a fighter or bomber, and claims only while fitted (in your hold it is just cargo). Fit it on the Loadout
// screen, from your hold or hangar, or buy one there for a power this station sells to ("Buy & fit"). Holding a fitted beacon
// in an unclaimed or breached outpost's ring claims it for that power, and the claim uses the beacon up (the slot is left
// empty: fit your landing kit back). Beacons have no grades. The Market's tiles show the beacons sold here, one per power.
UTIL.claim={name:'Claim Beacon',desc:'Fighters and bombers only. Hold it in an unclaimed or breached outpost\'s ring to claim it for the power it was bought for; the claim uses it up.'};
for(const f of FAC_IDS){const I=ITEMS['bc_'+f];if(I){I.part='claim';I.col=FACTIONS[f].col;I.trTxt=`Claims for ${FACTIONS[f].short}; the claim uses it up`}}
function cbItems(){return FAC_IDS.map(f=>'bc_'+f)}
{const o=partItems;partItems=function(k){return k==='claim'?cbItems():o.apply(this,arguments)}}
// the fitted beacons (a pilot's own fit), and the power each claims for
function cbFitted(P){const F=P&&fitOf(P),out=[];if(!F)return out;(F.u||[]).forEach((k,i)=>{if(k==='claim'){const it=(F.ui||[])[i];const f=it&&ITEMS[it]&&ITEMS[it].fb;if(f)out.push({i,f})}});return out}
fbHeld=function(P,o){for(const x of cbFitted(P))if(o.owner!==x.f)return x.f;return null};
{const o=fbClaim;fbClaim=function(o2,f,by){const me=by==='me'||isMe(by),P=me?S.player:(S.pilots||{})[by];if(!P)return;const x=cbFitted(P).find(y=>y.f===f);if(!x)return;
  const F=fitOf(P);F.u[x.i]='';F.ui[x.i]=null;F.ug[x.i]=1;inv.add(P.cargo,'bc_'+f,1);const r=o.apply(this,arguments);try{if(me&&W&&W.player)refreshPlayerStats()}catch(e){}return r}}
// fitting: fighters and bombers only; a beacon you don't have is bought here if this station sells that power's
{const o=fitDo;fitDo=function(c,P,arg){const[g,i0,k]=String(arg).split(':'),I=k&&ITEMS[k];if(I&&I.part==='claim'){if(!beaconCls(P.cls))return'Claim Beacons fit fighters and bombers only.';
    const srcs=[P.cargo,c.storage||P.vault];if(countIn(k,srcs)<1){if(!fbSold(c,P).includes(I.fb))return`No ${I.name} on hand: buy one where ${FACTIONS[I.fb].short} beacons are sold.`;const m=fbBuy(c,P,I.fb);if(!String(m).startsWith('✓'))return m}}
  return o.apply(this,arguments)}}
// no grades for beacons
{const o=pupQuote;pupQuote=function(c,P,arg){const[g,i0]=String(arg).split(':'),F=fitOf(P);if(g==='u'&&(F.u||[])[+i0]==='claim')return null;return o.apply(this,arguments)}}
// the Loadout slot panel: beacons only for hulls that carry them, and the ones you can buy here offered as Buy & fit
{const o=ldSlotHtml;ldSlotHtml=function(c,P,g,i){const ok=beaconCls(P.cls),U=UTIL.claim;if(!ok)delete UTIL.claim;let h;try{h=o.apply(this,arguments)}finally{UTIL.claim=U}
  try{if(g==='u'&&ok){const srcs=[P.cargo,c.storage||P.vault],cur=((fitOf(P).ui)||[])[i];const rows=fbSold(c,P).map(f=>'bc_'+f).filter(it=>it!==cur&&!countIn(it,srcs)).map(it=>`<div class="ldopt">${gIcon(it,15)}<span style="flex:1;min-width:0"><span>${esc(ITEMS[it].name)}</span><br><span class="mass" style="margin:0">claims for ${esc(FACTIONS[ITEMS[it].fb].short)} · ${fmt(CLAIM_PRICE)} cr here</span></span><button class="btn sm" data-act="fit" data-arg="u:${i}:${it}" ${P.credits>=CLAIM_PRICE?'':'disabled'}>Buy & fit</button></div>`).join('');
    if(rows)h+=(/Fit instead/.test(h)?'':`<div class="lab" style="margin-top:12px">Fit instead</div>`)+rows}}catch(e){console.error(e)}return h}}
// the Market's tiles: the beacons sold here
{const o=mkHtml;mkHtml=function(c,P){let h=o.apply(this,arguments);try{const L=fbSold(c,P);if(!L.length)return h;const srcs=[P.cargo,c.storage];
  h+=`<div class="mkgrp" style="margin-top:14px"><div class="lab">Claim Beacons · fit one in a utility slot (fighters and bombers) and hold it in an outpost's ring to claim it for that power</div><div class="mkrow">${L.map(f=>{const k='bc_'+f,n=countIn(k,srcs);
    return`<div class="mkt" style="cursor:default">${''}<span class="mktt">${gIcon(k,22)}<span><b style="color:${FACTIONS[f].col}">${esc(FACTIONS[f].short)}</b><br><span class="mono amber">${fmt(CLAIM_PRICE)}</span></span></span><span class="mass" style="margin:0">you ${n||'·'}${cbFitted(P).some(x=>x.f===f)?' · fitted':''}</span><button class="btn sm" type="button" data-act="buyfb" data-arg="${f}" ${P.credits>=CLAIM_PRICE?'':'disabled'}>Buy</button></div>`}).join('')}</div></div>`}catch(e){console.error(e)}return h}}
// the job board says where the beacon goes
{const o=jobsList;jobsList=function(c,P,srcs){const out=o.apply(this,arguments);try{for(const j of out)if(String(j.id).startsWith('cl:')){if(!beaconCls(P.cls))j.need='Needs a fighter or bomber with a Claim Beacon fitted';else{const f=String(j.id).split(':')[2];if(!cbFitted(P).some(x=>x.f===f))j.sub+=` · fit a ${FACTIONS[f].short} beacon (Loadout)`}}}catch(e){}return out}}
