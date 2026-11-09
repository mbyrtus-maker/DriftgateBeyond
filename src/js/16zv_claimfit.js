//@src 16zv_claimfit.js
// ============================================================ Claim Beacons are fitted, one per utility slot (Beyond, 3 Nov 2026)
// A power's Claim Beacon (bought for Halcyon, Varkesh or Ostrova, in that power's colour) is a utility part: it takes a
// utility slot on a fighter or bomber, and claims only while fitted (in your hold it is just cargo). Fit it on the Loadout
// screen, from your hold or hangar, or buy one there for a power this station sells to ("Buy & fit"). Holding a fitted beacon
// in an unclaimed or breached outpost's ring claims it for that power, and the claim uses the beacon up (the slot is left
// empty: fit your landing kit back). Beacons have no grades. The Market's tiles show the beacons sold here, one per power.
UTIL.claim={name:'Claim Beacon',desc:'Single use (ammo: 1). Fighters and bombers only. Hold it in an unclaimed or breached outpost\'s ring to claim it for the power it was bought for; the claim uses it up.'};
for(const f of FAC_IDS){const I=ITEMS['bc_'+f];if(I){I.part='claim';I.col=FACTIONS[f].col;I.trTxt=`Single use (ammo: 1). Claims one outpost for ${FACTIONS[f].short}; the claim uses it up`}}
function cbItems(){return FAC_IDS.map(f=>'bc_'+f)}
{const o=partItems;partItems=function(k){return k==='claim'?cbItems():o.apply(this,arguments)}}
// the fitted beacons (a pilot's own fit), and the power each claims for
function cbFitted(P){const F=P&&fitOf(P),out=[];if(!F)return out;(F.u||[]).forEach((k,i)=>{if(k==='claim'){const it=(F.ui||[])[i];const f=it&&ITEMS[it]&&ITEMS[it].fb;if(f)out.push({i,f})}});return out}
fbHeld=function(P,o){for(const x of cbFitted(P))if(o.owner!==x.f)return x.f;return null};
{const o=fbClaim;fbClaim=function(o2,f,by){const me=by==='me'||isMe(by),P=me?S.player:(S.pilots||{})[by];if(!P)return;const x=cbFitted(P).find(y=>y.f===f);if(!x)return;
  const F=fitOf(P);F.u[x.i]='';F.ui[x.i]=null;F.ug[x.i]=1;inv.add(P.cargo,'bc_'+f,1);const r=o.apply(this,arguments);try{if(me&&W&&W.player)refreshPlayerStats()}catch(e){}return r}}
// fitting: fighters and bombers only; the Loadout fits only beacons you have; the Jobs board's Buy & fit (cbfit) buys one first
let cbBuyOK=false;
{const o=fitDo;fitDo=function(c,P,arg){const[g,i0,k]=String(arg).split(':'),I=k&&ITEMS[k];if(I&&I.part==='claim'){if(!beaconCls(P.cls))return'Claim Beacons fit fighters and bombers only.';
    const srcs=[P.cargo,c.storage||P.vault];if(countIn(k,srcs)<1){if(!cbBuyOK)return`No ${I.name} in your hold or hangar: buy one on the Market (where ${FACTIONS[I.fb].short} beacons are sold), then fit it.`;if(!fbSold(c,P).includes(I.fb))return`${FACTIONS[I.fb].short} beacons aren't sold here.`;const m=fbBuy(c,P,I.fb);if(!String(m).startsWith('✓'))return m}}
  return o.apply(this,arguments)}}
// no grades for beacons
{const o=pupQuote;pupQuote=function(c,P,arg){const[g,i0]=String(arg).split(':'),F=fitOf(P);if(g==='u'&&(F.u||[])[+i0]==='claim')return null;return o.apply(this,arguments)}}
// the Loadout slot panel: beacons only for hulls that carry them (only the ones you have are offered, as for every part)
{const o=ldSlotHtml;ldSlotHtml=function(c,P,g,i){const ok=beaconCls(P.cls),U=UTIL.claim;if(!ok)delete UTIL.claim;let h;try{h=o.apply(this,arguments)}finally{UTIL.claim=U}
  return h}}
// the Market's tiles: the beacons sold here
{const o=mkHtml;mkHtml=function(c,P){let h=o.apply(this,arguments);try{const L=fbSold(c,P);if(!L.length||mkFilter!=='p_util')return h;const srcs=[P.cargo,c.storage];
  h+=`<div class="mkgrp" style="margin-top:14px"><div class="lab">Claim Beacons · single use · fit one in a utility slot (fighters and bombers) and hold it in an outpost's ring to claim it for that power</div><div class="mkrow">${L.map(f=>{const k='bc_'+f,n=countIn(k,srcs);
    return`<div class="mkt" style="cursor:default">${''}<span class="mktt">${gIcon(k,22)}<span><b style="color:${FACTIONS[f].col}">${esc(FACTIONS[f].short)}</b><br><span class="mono amber">${fmt(CLAIM_PRICE)}</span></span></span><span class="mass" style="margin:0">single use (ammo: 1) · you ${n||'·'}${cbFitted(P).some(x=>x.f===f)?' · fitted':''}</span><button class="btn sm" type="button" data-act="buyfb" data-arg="${f}" ${P.credits>=CLAIM_PRICE?'':'disabled'}>Buy</button></div>`}).join('')}</div></div>`}catch(e){console.error(e)}return h}}
// the job board says where the beacon goes
// (user, 3 Nov 2026) a claim job carries the button that gets you its beacon: "Buy & fit" where that power's beacons are
// sold (or "Fit the beacon" when one is in your hold or vault), straight into a utility slot (an empty one first, else the
// landing kit's, which goes to your vault); in a hull that can't carry one, the board's hull switch, as other jobs have.
// It rides in the job's fix slot (the board's first button), which Select job and Drop job leave alone.
function cbSlot(P){const U=fitOf(P).u||[];if(!U.length)return -1;let i=U.findIndex(k=>!k);if(i<0)i=U.indexOf('land');if(i<0)i=U.findIndex(k=>k!=='claim');return i<0?0:i}
{const o=jobsList;jobsList=function(c,P,srcs){const out=o.apply(this,arguments);try{for(const j of out)if(String(j.id).startsWith('cl:')){const f=String(j.id).split(':')[2],sh=FACTIONS[f].short,bc='bc_'+f;
    if(!beaconCls(P.cls)){j.need='Needs a fighter or bomber with a Claim Beacon fitted';try{const fx=hullFix(c,P,beaconCls,'interceptor');if(fx)j.fix=fx}catch(e){}continue}
    if(cbFitted(P).some(x=>x.f===f)){j.sub+=` · ${sh} beacon fitted`;continue}
    const i=cbSlot(P),have=countIn(bc,[P.cargo,(c&&c.storage)||P.vault])>0,sold=fbSold(c,P).includes(f),was=i>=0?(fitOf(P).u||[])[i]:'';
    if(i<0){j.sub+=` · needs a utility slot for the beacon`;continue}
    j.btn2=null;if(have)j.fix=['cbfit',`${f}:${i}`,`Fit the ${sh} beacon`];else if(sold)j.fix=['cbfit',`${f}:${i}`,`Buy & fit a ${sh} beacon · ${fmt(CLAIM_PRICE)} cr`];
    j.sub+=have?` · your ${sh} beacon isn't fitted`:` · needs a ${sh} beacon`;
    const d0=j.detail;j.detail=()=>(d0?d0():'')+`<p class="note" style="margin:8px 0 0">${have||sold?`${have?'Fit the':'Buy & fit puts a'} ${esc(sh)} Claim Beacon in utility slot ${i+1}${was?` (your ${esc((UTIL[was]||{}).name||was)} goes to your ${c&&c.storage&&c.storage!==P.vault?esc(c.storageName||'store'):'vault'})`:''}. Then fly to the outpost, break its defences if it's held, and hold position inside its ring: the beacon claims it for ${esc(sh)} and is used up.`:`${esc(sh)} Claim Beacons aren't sold here: buy one at a freeport or a ${esc(sh)} station, then fit it on the Loadout.`}</p>`}}catch(e){console.error(e)}return out}}
{const o=fbBuy;fbBuy=function(c,P,f){const r=o.apply(this,arguments);return typeof r==='string'?r.replace(/Carry it into an unclaimed or breached outpost's ring in a fighter or bomber and hold there/,"Fit it in a utility slot on the Loadout (fighters and bombers), then hold it in an unclaimed or breached outpost's ring"):r}}
// why you can't claim this outpost from its ring, in words that match the fitted beacons (it used to ask for one in the hold)
function cbWhy(P,o){const own=o.owner?(FACTIONS[o.owner]?FACTIONS[o.owner].short:sideName(o.owner)):null,pre=o.owner?'Defenses down. ':'Unclaimed outpost. ';if(!P)return pre+'Fit a Claim Beacon (Loadout) to claim it.';
  const fit=cbFitted(P);if(fit.length){if(!beaconCls(P.cls))return pre+'Claim Beacons work only on fighters and bombers: switch hulls to claim it.';if(fit.every(x=>x.f===o.owner))return`${o.name} is already ${own}'s: your beacon claims for ${own} too.`}
  const hold=FAC_IDS.filter(f=>countIn('bc_'+f,[P.cargo,P.vault||{}])>0);if(hold.length)return pre+`Your ${hold.map(f=>FACTIONS[f].short).join(' and ')} Claim Beacon is in your hold, not fitted: fit it in a utility slot (Loadout) to claim.`;
  return pre+'Fit a Claim Beacon in a utility slot (buy one at a freeport or a power\'s station, then Loadout) to claim it.'}
{const o=dockAction;dockAction=function(act,arg){if(act==='cbfit'){const[f,i]=String(arg).split(':');if(!FAC_IDS.includes(f)){dockErr='';return}const c=dockCtx(),P=S.player;cbBuyOK=true;try{dockErr=fitDo(c,P,`u:${+i}:bc_${f}`)}finally{cbBuyOK=false}return}return o.apply(this,arguments)}}
