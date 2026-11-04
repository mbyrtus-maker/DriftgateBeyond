//@src 16k_makers.js
// ============================================================ makers: the corporations (Beyond stage 7)
// Each power hosts two makers and each freeport two more. A maker's works sit at its home station and turn components from
// that station's market into its products at a set rate, for sale on that market. A maker's part is the slot part with the
// maker's trait: a strength and usually a weakness. Fitted, upgraded or moved, a maker's part keeps its maker.
// Trait keys: dmg (gun or laser damage), e (laser or mining-laser energy draw), ammo (machine-gun rounds), mag (missiles,
// torpedoes or charges per launcher), lock (lock time), ml (mining-laser rate), cargo (cargo-module hold), scan (scanner reach),
// speed (the whole ship's top speed); maxG: the top grade its parts take.
const MAKERS={
  tcy:{name:'Teal & Corvane Yards',short:'Corvane',home:'halcyon',parts:{cargo:{cargo:.06,speed:-.01},dronec:{dh:.2}}},
  bl:{name:'Brightline Emitters',short:'Brightline',home:'halcyon',parts:{laser:{dmg:.1,e:.1}}},
  hf:{name:'Hold Foundry',short:'Foundry',home:'varkesh',parts:{charge:{mag:1,speed:-.01}}},
  mg:{name:'Marchgun Ordnance',short:'Marchgun',home:'varkesh',parts:{gun:{dmg:.12,ammo:-.15},missile:{mag:1,lock:.1}}},
  sw:{name:'Spirewright',short:'Spirewright',home:'ostrova',parts:{scanner:{scan:.25},mlaser:{ml:.1,e:.15}}},
  ad:{name:'Archive Dynamics',short:'Archive',home:'ostrova',parts:{laser:{e:-.15,dmg:-.04}}},
  mwa:{name:'Mirrorwater Arms',short:'Mirrorwater',home:'mw',parts:{gun:{ammo:.1},laser:{},missile:{},torpedo:{}}},
  qs:{name:'Quicksilver Hullworks',short:'Quicksilver',home:'mw',parts:{cargo:{cargo:.03},land:{}}},
  cr:{name:'Coldwater Refit',short:'Refit',home:'cw',maxG:3,parts:{gun:{dmg:-.05},laser:{dmg:-.05},missile:{}}},
  cp:{name:'Coldwater Prospecting',short:'Prospecting',home:'cw',parts:{mlaser:{ml:.12},charge:{mag:1},scanner:{scan:.1},dronec:{dd:.15}}},
  ewd:{name:'Ember Wake Drives',short:'Ember',home:'ew',parts:{cargo:{cargo:.08,speed:-.02}}},
  wf:{name:'Wakefire Munitions',short:'Wakefire',home:'ew',parts:{missile:{mag:1},torpedo:{mag:1}}}};
const MK_WORKS={every:90,cap:4,seed:2};
const TR_TXT={dmg:'damage',e:'energy draw',ammo:'rounds',mag:'per launcher',lock:'lock time',ml:'cutting rate',cargo:'hold',scan:'scanner reach',speed:'top speed',dh:'drone hull',dd:'drone damage'};
function trText(tr){return Object.keys(tr).map(k=>k==='mag'?`${tr[k]>0?'+':''}${tr[k]} ${TR_TXT[k]}`:`${tr[k]>0?'+':'−'}${Math.round(Math.abs(tr[k])*100)}% ${TR_TXT[k]}`).join(', ')}
const MK_ITEMS={};
for(const m in MAKERS)for(const k in MAKERS[m].parts){const id=`mp_${m}_${k}`,tr=MAKERS[m].parts[k];ITEMS[id]={name:`${MAKERS[m].short} ${(WPN[k]||UTIL[k]).name.replace(/^./,x=>x.toLowerCase())}`.replace(/^./,x=>x.toUpperCase()),recipe:{...PART_RC[k]},col:PART_COL[k],part:k,maker:m,tr,trTxt:trText(tr)?`${MAKERS[m].name}: ${trText(tr)}.`:`${MAKERS[m].name}: standard.`};
  ITEM_ORDER.push(id);(MK_ITEMS[k]=MK_ITEMS[k]||[]).push(id)}
// every item that can go in a slot of this kind: the standard part, then the makers'
function partItems(k){return[PART[k],...(MK_ITEMS[k]||[])]}
function mkHomeSid(m){const h=MAKERS[m].home;return FAC_IDS.includes(h)?FAC_HOME(h):h}
function mkAtHome(m){const sid=mkHomeSid(m),R=S.stations[sid],h=MAKERS[m].home;return R&&(FAC_IDS.includes(h)?R.owner===h:R.owner==='neutral')?R:null}
// the trait of the parts fitted in slots of a kind: averaged (sum: summed) over those slots
function mkTr(P,kind,key,sum){const F=fitOf(P);let s=0,n=0;F.w.forEach((k,i)=>{if(k!==kind)return;n++;const it=F.wi&&F.wi[i];s+=(it&&ITEMS[it]&&ITEMS[it].tr&&ITEMS[it].tr[key])||0});
  (F.u||[]).forEach((k,i)=>{if(k!==kind)return;n++;const it=F.ui&&F.ui[i];s+=(it&&ITEMS[it]&&ITEMS[it].tr&&ITEMS[it].tr[key])||0});return sum?s:n?s/n:0}
function mkShip(F,key){let s=0;const add=it=>{const t=it&&ITEMS[it]&&ITEMS[it].tr;if(t&&t[key])s+=t[key]};(F.wi||[]).forEach(add);(F.ui||[]).forEach(add);return s}
// ---- traits applied
{const o=ammoCap;ammoCap=function(P){const v=o.apply(this,arguments);return loadOn()&&P?Math.round(v*(1+mkTr(P,'gun','ammo'))):v}}
{const o=pRack;pRack=function(P){const v=o.apply(this,arguments);if(!loadOn()||!P||!v)return v;return v+mkTr(P,isTorpHull(P.cls)?'torpedo':'missile','mag',true)}}
{const o=blCap;blCap=function(P){const v=o.apply(this,arguments);if(!loadOn()||!P||!v)return v;return v+mkTr(P,'charge','mag',true)}}
{const o=mlRate;mlRate=function(P){return o.apply(this,arguments)*(1+mkTr(P,'mlaser','ml'))}}
{const o=vK;vK=function(P,key){const v=o.apply(this,arguments);if(key==='lockK'&&P&&loadOn()&&P.fit)return v*(1+mkTr(P,isTorpHull(P.cls)?'torpedo':'missile','lock'));return v}}
{const o=fire;fire=function(e){const P=loadOn()&&pilotOfEnt(e);if(!P)return o.apply(this,arguments);const d=e.st.dmg;e.st.dmg=d*(1+mkTr(P,'gun','dmg'));try{return o.apply(this,arguments)}finally{e.st.dmg=d}}}
{const o=fireLaser;fireLaser=function(e){const P=loadOn()&&pilotOfEnt(e);if(!P)return o.apply(this,arguments);const d=e.st.dmg,c=e.st.shotCost;e.st.dmg=d*(1+mkTr(P,'laser','dmg'));e.st.shotCost=c*(1+mkTr(P,'laser','e'));try{return o.apply(this,arguments)}finally{e.st.dmg=d;e.st.shotCost=c}}}
{const o=mlCut;mlCut=function(e,P,a,dt){const k=1+mkTr(P,'mlaser','e');if(k===1)return o.apply(this,arguments);const E0=e.energy;const r=o.apply(this,arguments);if(e.energy<E0)e.energy=Math.max(0,E0-(E0-e.energy)*k);return r}}
{const o=shipStats;shipStats=function(fac,cls,T,U){const B=o.apply(this,arguments);const F=U&&typeof U==='object'&&FIT_T.get(U);if(F&&F.cls===cls&&loadOn()){
  let k=0;(F.u||[]).forEach((x,i)=>{if(x==='cargo'){const it=F.ui&&F.ui[i];k+=(it&&ITEMS[it].tr.cargo)||0}});if(k&&B.cargo)B.cargo=Math.round(B.cargo*(1+k));const sp=mkShip(F,'speed');if(sp){B.maxSpd*=1+sp}}return B}}
{const o=vF;vF=function(P,key){const v=o.apply(this,arguments);if(key==='blScanR'&&v&&loadOn()&&P&&P.fit)return v*(1+mkTr(P,'scanner','scan'));return v}}
{const o=pupQuote;pupQuote=function(c,P,arg){const q=o.apply(this,arguments);if(!q)return q;const[g,i0]=String(arg).split(':'),F=fitOf(P),it=((g==='w'?F.wi:F.ui)||[])[+i0],m=it&&ITEMS[it]&&ITEMS[it].maker;if(m&&MAKERS[m].maxG&&q.t>MAKERS[m].maxG)return null;return q}}
// ---- the works: every 90 s each maker at home builds one of its products from its station's components, up to 4 on sale
function makersTick(){if(NET.cl||!S||S.training||S.unb)return;S.mkT=S.mkT||0;if(S.T<S.mkT)return;S.mkT=S.T+MK_WORKS.every;
  for(const m in MAKERS){const R=mkAtHome(m);if(!R)continue;const st=mkStock(R),ids=Object.keys(MAKERS[m].parts).map(k=>`mp_${m}_${k}`).filter(id=>(st[id]||0)<MK_WORKS.cap).sort((a,b)=>(st[a]||0)-(st[b]||0));
    for(const id of ids){const rc=ITEMS[id].recipe;if(haveIn(rc,[st])){takeFrom(rc,[st]);inv.add(st,id,1);break}}}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{makersTick()}catch(err){console.error(err)}return r}}
// the first stock, made with the galaxy before its baseline is taken
{const o=partsSeed;partsSeed=function(){o.apply(this,arguments);for(const m in MAKERS){const R=mkAtHome(m);if(!R)continue;const st=mkStock(R);for(const k in MAKERS[m].parts)inv.add(st,`mp_${m}_${k}`,MK_WORKS.seed)}}}
// the market tab lists the makers whose works are here
{const o=fbMarketHtml;fbMarketHtml=function(c,P){let h=o.apply(this,arguments);const here=Object.keys(MAKERS).filter(m=>mkHomeSid(m)===P.sector&&mkAtHome(m));if(!here.length)return h;
  return h+`<div class="h3" style="margin-top:18px">Makers' works here</div><p class="note" style="margin:0 0 8px">These corporations build their parts here from this station's components, one every ${MK_WORKS.every} s up to ${MK_WORKS.cap} on sale. Fit them from the Ship tab's Loadout.</p>`+here.map(m=>`<div class="note" style="margin:0 0 4px"><b>${esc(MAKERS[m].name)}</b> · ${Object.keys(MAKERS[m].parts).map(k=>{const id=`mp_${m}_${k}`;return`${esc(ITEMS[id].name)} (${trText(MAKERS[m].parts[k])||'standard'}; ${c.market&&c.market[id]||0} in stock)`}).join(' · ')}${MAKERS[m].maxG?` · upgrades to grade ${MAKERS[m].maxG} only`:''}</div>`).join('')}}
