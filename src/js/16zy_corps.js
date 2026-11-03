//@src 16zy_corps.js
// ============================================================ every item has a maker (Beyond, 3 Nov 2026)
// The user's choices: markets sell only corporations' parts; components and payload carry a made-by label, with no traits.
//  - Parts: each power's core station and each freeport sells only its two makers' parts. Each maker has a plain line (no
//    trait) for every slot it covers, beside its trait parts; a slot no local maker covers goes to one of them (weapons and
//    mining tools to the arms maker, utility parts to the other). The unbranded standard part is now only what you build in a
//    workshop yourself (or under your own brand). Standard parts already on those markets become the local makers' plain
//    parts (same recipe, so the ledger is unchanged).
//  - Components and payload: a market of a power or a freeport shows which of its makers makes each one (components the
//    first maker, payload the second). They stay one item each in the economy.
const CORP_HOME={halcyon:['tcy','bl'],varkesh:['hf','mg'],ostrova:['sw','ad'],mw:['qs','mwa'],cw:['cp','cr'],ew:['ewd','wf']};
const CORP_W=new Set(['gun','laser','missile','torpedo','mlaser','charge']);
const CORP_PAY=new Set(['missile','torpedo','ammo','rounds','charges','chg','drone','limpet','mine','decoy']);
function corpSells(h){if(FAC_IDS.includes(h))return['gun','laser','missile','torpedo','land','cargo','scanner',...(h==='ostrova'?['bdev','lrack']:[])];return Object.keys(PART)}
const MK_LINE={},MK_PLAIN={};
(function(){for(const h in CORP_HOME){const L=CORP_HOME[h];
  const plain=(m,k)=>{MK_PLAIN[m]=MK_PLAIN[m]||{};if(MK_PLAIN[m][k])return;const P0=MAKERS[m].parts[k];let id;
    if(P0&&!Object.keys(P0).length)id=`mp_${m}_${k}`;
    else{id=`mq_${m}_${k}`;const nm=(WPN[k]||UTIL[k]).name;ITEMS[id]={name:`${MAKERS[m].short} ${P0?'standard ':''}${nm.replace(/^./,x=>x.toLowerCase())}`,recipe:{...PART_RC[k]},col:PART_COL[k],part:k,maker:m,tr:{},trTxt:`${MAKERS[m].name}: standard.`};ITEM_ORDER.push(id);(MK_ITEMS[k]=MK_ITEMS[k]||[]).push(id)}
    MK_PLAIN[m][k]=id};
  for(const m of L)for(const k in MAKERS[m].parts)plain(m,k);
  for(const k of corpSells(h)){if(!PART[k])continue;if(L.some(m=>MAKERS[m].parts[k]||(MK_PLAIN[m]&&MK_PLAIN[m][k])))continue;plain(CORP_W.has(k)?L[1]:L[0],k)}}
  for(const m in MAKERS){const ids=new Set(Object.keys(MAKERS[m].parts).map(k=>`mp_${m}_${k}`));for(const k in MK_PLAIN[m]||{})ids.add(MK_PLAIN[m][k]);MK_LINE[m]=[...ids]}})();
// the self-built part says what it is
for(const k in PART)if(ITEMS[PART[k]])ITEMS[PART[k]].trTxt='Unbranded: built in a workshop, by you or another pilot.';
// the plain part a station's makers sell for a slot
function corpPlainAt(sid,k){const R=S.stations[sid],h=R&&(R.owner==='neutral'?sid:FAC_IDS.includes(R.owner)&&R.kind==='core'?R.owner:null);const L=h&&CORP_HOME[h];if(!L)return null;
  for(const m of L)if(MK_PLAIN[m]&&MK_PLAIN[m][k]&&mkHomeSid(m)===sid)return MK_PLAIN[m][k];return null}
// standard parts on the makers' markets become their plain parts (same recipe: the ledger is unchanged)
function corpConvert(){for(const sid in S.stations||{}){const R=S.stations[sid];if(!R||R.owner==='player')continue;let st;try{st=mkStock(R)}catch(e){continue}if(!st)continue;
  for(const k in PART){const id=PART[k],n=st[id]||0;if(!n)continue;const to=corpPlainAt(sid,k);if(!to)continue;inv.take(st,id,n);inv.add(st,to,n)}}}
{const o=partsSeed;partsSeed=function(){o.apply(this,arguments);try{for(const m in MAKERS){const R=mkAtHome(m);if(!R)continue;const st=mkStock(R);for(const id of MK_LINE[m])if(id.startsWith('mq_'))inv.add(st,id,MK_WORKS.seed)}corpConvert();S.corpConv=1}catch(e){console.error(e)}}}
// the works build their whole line, plain parts included
makersTick=function(){if(NET.cl||!S||S.training||S.unb)return;S.mkT=S.mkT||0;if(S.T<S.mkT)return;S.mkT=S.T+MK_WORKS.every;
  if(!S.corpConv){try{corpConvert()}catch(e){}S.corpConv=1}
  for(const m in MAKERS){const R=mkAtHome(m);if(!R)continue;const st=mkStock(R),ids=MK_LINE[m].filter(id=>(st[id]||0)<MK_WORKS.cap).sort((a,b)=>(st[a]||0)-(st[b]||0));
    for(const id of ids){const rc=ITEMS[id].recipe;if(haveIn(rc,[st])){takeFrom(rc,[st]);inv.add(st,id,1);break}}}};
// ---- made-by labels for components and payload
function corpKindOf(k){const I=ITEMS[k];if(!I||RAWS.includes(k)||k==='rift'||I.cash||I.part||String(k).startsWith('bc_')||k==='beacon')return null;const g=giKind(k);return g==='comp'?(CORP_PAY.has(k)?1:0):(g==='msl'||g==='chg'||g==='rnd')?1:null}
function corpMakerOf(sid,k){const R=S.stations[sid];if(!R)return null;const L=R.owner==='neutral'?CORP_HOME[sid]:FAC_IDS.includes(R.owner)?CORP_HOME[R.owner]:null;if(!L)return null;const i=corpKindOf(k);return i==null?null:L[i]}
function corpLine(k){const I=ITEMS[k];if(!I)return'';if(I.maker)return MAKERS[I.maker].name;if(I.part)return ITEMS[k].trTxt&&/^Unbranded/.test(ITEMS[k].trTxt)?'Unbranded (workshop-built)':'';const m=S&&S.player&&corpMakerOf(S.player.sector,k);return m?MAKERS[m].name:''}
{const o=mkHtml;mkHtml=function(c,P){let h=o.apply(this,arguments);try{const k=mkSel;if(!k)return h;const who=corpLine(k);if(!who)return h;const i=h.indexOf('<div class="ldname">',h.indexOf('<div class="mkdet">'));if(i<0)return h;const j=h.indexOf('</div>',i)+6;
  return h.slice(0,j)+`<div class="note" style="margin:0 0 4px">${ITEMS[k].maker||/^Unbranded/.test(who)?'':'Made by '}<b style="color:var(--ivory,#ece4cf)">${esc(who)}</b>${ITEMS[k].maker?'':ITEMS[k].part?'':' · here'}</div>`+h.slice(j)}catch(e){return h}}}
// tiles: the maker's short name under each component and payload
{const o=mkHtml;mkHtml=function(c,P){let h=o.apply(this,arguments);try{h=h.replace(/(<button class="mkt[^"]*" type="button" data-act="mksel" data-arg="([^"]+)">)/g,(all,b,k)=>{const m=corpMakerOf(P.sector,k);return m?b.replace('type="button"',`type="button" title="Made by ${esc(MAKERS[m].name)}"`):b})}catch(e){}return h}}
