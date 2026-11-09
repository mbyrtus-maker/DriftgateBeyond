//@src 16zm_market2.js
// ============================================================ the graphical market (Beyond screens pass, 3 Nov 2026)
// Trade → Market shows tiles grouped as Ore, Components, Weapons, Utility parts and Payload (a filter for each), each with
// its icon, price here, a stock meter and a mark (▲ wanted here, ▼ oversupplied). Your hold is a coloured bar on top. Pick a
// tile: buy, sell and galaxy-average prices (from your scans), the price here while you've watched it, a quantity slider with
// Buy and Sell, Load and Store against your hangar, and the best places to sell from your scans. "Table" shows the old list
// (every button it had, Control Markers included); the makers' works and salvage sales stay underneath.
let mkSel=null,mkFilter='none',mkView='tiles',mkQty=1;
// (user, 8 Nov 2026) the Parts filters, the user's final list: Drive, Reactors, Shields, Weapons, Armor, Cargo, Mining, Utility.
// Weapons: guns, lasers, launchers, the weapon system and payload bays, missiles, torpedoes and rounds. Cargo: cargo holds and
// cargo pods. Mining: blast rigs, mining lasers, charge launchers and charges. Utility: every other utility part, and beacons.
const MK_PARTS=['p_drive','p_reactor','p_shield','p_wpn','p_armor','p_cargo','p_mining','p_util'];
const MK_SYSG={engine:'p_drive',power:'p_reactor',shield:'p_shield',weapon:'p_wpn',payload:'p_wpn',armor:'p_armor',cargo:'p_cargo',drill:'p_mining'};
function mkGroup(k){const I=ITEMS[k]||{};if(I.sys)return MK_SYSG[I.sys]||'p_util';const g=giKind(k);if(g==='ore'||g==='con')return'ore';if(g==='chg')return'p_mining';if(g==='msl'||g==='rnd')return'p_wpn';
  if(I.part){if(I.part==='mlaser'||I.part==='charge')return'p_mining';if(I.part==='cargo')return'p_cargo';return WPN[I.part]?'p_wpn':'p_util'}return g}
const MK_GN={parts:'Parts',ore:'Ore',comp:'Components',p_drive:'Drive',p_reactor:'Reactors',p_shield:'Shields',p_wpn:'Weapons',p_armor:'Armor',p_cargo:'Cargo',p_mining:'Mining',p_util:'Utility'};
// prices seen here, while docked (a minute apart, 30 readings)
function mkWatch(){const P=S.player;if(!P||!P.docked||S.unb)return;let c;try{c=dockCtx()}catch(e){return}if(!c||!c.market)return;const key=P.sector;P.pxh=P.pxh||{};const H=P.pxh[key]=P.pxh[key]||{T:0,p:{}};if(S.T-H.T<60)return;H.T=S.T;
  for(const k of Object.keys(c.market)){if(!(c.market[k]>0)||!ITEMS[k])continue;const a=H.p[k]=H.p[k]||[];a.push(mSell(c,k));if(a.length>30)a.shift()}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{mkWatch()}catch(e){}return r}}
function mkScan(P,k){const I=P.pintel||{},L=[];for(const sid in I){const x=I[sid];if(x&&x.s&&x.s[k]>0)L.push({sid,s:x.s[k],T:x.T})}return L}
function mkHtml(c,P){const st=c.market,srcs=[P.cargo,c.storage],p=W.player,cap=p.st.cargo,used=invMass(P.cargo);
  const items=ITEM_ORDER.filter(k=>k!=='beacon'&&!String(k).startsWith('bc_')&&!MUNITIONS.has(k)&&ITEMS[k]&&((st[k]||0)>0||countIn(k,srcs)>0));
  if(!mkSel||!items.includes(mkSel))mkSel=items[0]||null;
  let bar='';for(const k of Object.keys(P.cargo)){const m=(P.cargo[k]||0)*mass(k);if(m>0)bar+=`<i title="${esc(ITEMS[k].name)} ${P.cargo[k]}" style="display:block;height:100%;width:${m/cap*100}%;background:${giCol(k)};margin-right:1px"></i>`}
  let h=`<div class="mkbar"><span class="lab">Hold</span><span class="mkhold">${bar}</span><span class="note" style="margin:0">${used} / ${cap} t</span><span style="flex:1"></span>`;
  // (user, 3 Nov 2026) first pick a category (Ore, Components, Weapons, Utility parts, Beacons; Payload when stocked), then its goods
  // (user, 8 Nov 2026) the main menu is Ore, Components, Parts; Parts opens a second row: Drive, Reactors, Shields, Weapons,
  // Armor, Cargo, Mining, Utility (beacons under Utility)
  const nB=(typeof fbSold==='function'?fbSold(c,P).length:0)+(claimSold(c,P)?1:0),cnt0=g=>items.filter(k=>mkGroup(k)===g).length+(g==='p_util'?nB:0),PARTS=MK_PARTS,
    cnt=g=>g==='parts'?PARTS.reduce((a,x)=>a+cnt0(x),0):cnt0(g),CATS=['ore','comp','parts'];
  if(mkFilter==='parts'){mkFilter=PARTS.find(g=>cnt0(g))||'parts'}const inParts=mkFilter==='parts'||PARTS.includes(mkFilter);
  if(mkFilter==='all')mkFilter='none';
  h+=`<button class="mkf" type="button" data-act="mkview" data-arg="table" style="margin-left:14px">Table</button></div>`;
  // (user) the categories stay across the top as orange boxes, the picked one filled, so you can move between them
  h+=`<div class="obox-row">${CATS.map(g=>{const on=g==='parts'?inParts:mkFilter===g;return`<button class="obox${on?' on':''}" type="button" data-act="mkf" data-arg="${g}" ${cnt(g)?'':'disabled'} aria-pressed="${on}">${MK_GN[g]} <span>${cnt(g)}</span></button>`}).join('')}</div>`;
  // the second row, under Parts (every filter shown, dimmed when none is on sale here)
  if(inParts)h+=`<div class="obox-row obox-sys">${PARTS.map(g=>`<button class="obox${mkFilter===g?' on':''}" type="button" data-act="mkf" data-arg="${g}" ${cnt0(g)?'':'disabled'} aria-pressed="${mkFilter===g}">${MK_GN[g]} <span>${cnt0(g)}</span></button>`).join('')}</div>`;
  if(mkFilter==='parts'){h+=`<div class="note" style="margin:10px 0 0">No parts on sale here.</div>`;return h}
  if(mkFilter==='none'){h+=`<div class="note" style="margin:10px 0 0">Pick a category to see what this market has.</div>`;return h}
  if(!(mkFilter==='p_util'&&nB)&&!items.some(k=>mkGroup(k)===mkFilter)){mkFilter='none';return mkHtml(c,P)}
  if(mkSel&&mkGroup(mkSel)!==mkFilter)mkSel=items.find(k=>mkGroup(k)===mkFilter)||null;
  h+=`<div class="mkwrap"><div class="mktiles">`;
  for(const g of['ore','comp',...MK_PARTS]){if(mkFilter!=='all'&&mkFilter!==g)continue;const L=items.filter(k=>mkGroup(k)===g);if(!L.length)continue;
    h+=`<div class="mkgrp"><div class="lab">${MK_GN[g]}</div><div class="mkrow">`;
    for(const k of L){const dm=demandOf(mR(c),k),stk=st[k]||0,on=k===mkSel,tgt=Math.max(1,stockTarget(k)),r=stk/tgt;
      h+=`<button class="mkt${on?' on':''}" type="button" data-act="mksel" data-arg="${k}"><span class="mktt">${gIcon(k,22)}<span><b>${esc(ITEMS[k].name)}</b><br><span class="mono amber">${fmt(mBuy(c,k))}</span>${dm==='high'?' <span style="color:#7ad9a7">▲</span>':dm==='low'?' <span style="color:#ff9a4a">▼</span>':''}</span></span>
        <span class="mkm"><i style="width:${Math.min(100,Math.round(r*50))}%;background:${dm==='high'?'#7ad9a7':dm==='low'?'#ff9a4a':'#5a647c'}"></i></span><span class="mass" style="margin:0">${stk} in stock · you ${countIn(k,srcs)||'·'}</span></button>`}
    h+=`</div></div>`}
  if(!items.length&&mkFilter!=='p_util')h+=`<div class="empty">Nothing in stock.</div>`;
  h+=`</div><div class="mkdet">`;
  if(mkSel){const k=mkSel,b=mBuy(c,k),s=mSell(c,k),sc=mkScan(P,k),avg=sc.length?Math.round(sc.reduce((a,x)=>a+x.s,0)/sc.length):null,stk=st[k]||0,hold=P.cargo[k]||0,hv=c.storage[k]||0,have=hold+hv;
    const room=Math.max(0,Math.floor((cap-used)/mass(k))),maxQ=Math.max(1,stk,have);mkQty=Math.min(Math.max(1,mkQty),maxQ);
    const H=(P.pxh&&P.pxh[P.sector]&&P.pxh[P.sector].p[k])||[];let spark='';if(H.length>1){const lo=Math.min(...H,avg||Infinity)*.95,hi=Math.max(...H,avg||0)*1.05,Y=v=>Math.round(48-(v-lo)/Math.max(1,hi-lo)*44);
      spark=`<svg width="320" height="52" viewBox="0 0 320 52" role="img" aria-label="Price here"><polyline points="${H.map((v,i)=>Math.round(i*320/(H.length-1))+','+Y(v)).join(' ')}" fill="none" stroke="#f0b24a" stroke-width="1.6"/>${avg?`<line x1="0" x2="320" y1="${Y(avg)}" y2="${Y(avg)}" stroke="#36435f" stroke-dasharray="3 4"/>`:''}</svg>`}
    const best=sc.filter(x=>x.sid!==P.sector).sort((a,b2)=>b2.s-a.s).slice(0,3);
    h+=`<div class="ldname">${gIcon(k,30)}<b>${esc(ITEMS[k].name)}</b></div><div class="note" style="margin:0 0 10px">${mass(k)} t · ${stk} in stock · you carry ${hold}, ${hv} in your ${esc(c.storageName==='Vault'?'hangar':c.storageName.toLowerCase())}${ITEMS[k].trTxt?' · '+esc(ITEMS[k].trTxt):''}</div>${mkVsStd(k,P)}
      <div class="mkpx"><span>Buy<b class="mono">${fmt(b)}</b></span><span>Sell<b class="mono">${fmt(s)}</b></span><span title="The average price you'd get selling this at the stations you've scanned">Galaxy sell<b class="mono" style="color:var(--dim)">${avg?fmt(avg):'—'}</b></span></div>
      ${spark?`${spark}<div class="note" style="margin:0 0 10px">Sell price here while you've watched${avg?' · dashed: the average sell price at the stations you\'ve scanned':''}</div>`:`<div class="note" style="margin:6px 0 10px">Stay docked a while to see how the price moves.</div>`}
      <div style="display:flex;justify-content:space-between;align-items:baseline"><span class="lab">Quantity</span><b class="mono">${mkQty}</b></div>
      <input type="range" id="mkQ" min="1" max="${maxQ}" value="${mkQty}" aria-label="Quantity" style="width:100%;accent-color:#f0b24a">
      <div class="act" style="margin:8px 0"><button class="btn pri" data-act="buy" data-arg="${k}:${mkQty}" ${!(stk>0)||P.credits<b?'disabled':''}>Buy ${mkQty} · ${fmt(b*mkQty)} cr</button><button class="btn" data-act="sell" data-arg="${k}:${Math.min(mkQty,have)}" ${have<1?'disabled':''}>Sell ${Math.min(mkQty,have)} · ${fmt(s*Math.min(mkQty,have))} cr</button></div>
      <div class="act" style="margin-bottom:12px"><button class="btn sm" data-act="buy" data-arg="${k}:fill" ${!(stk>0)||P.credits<b||room<1?'disabled':''}>Fill hold</button><button class="btn sm" data-act="sell" data-arg="${k}:all" ${have<1?'disabled':''}>Sell all</button>${hold?`<button class="btn sm" data-act="mv" data-arg="${k}:in:all">Store all</button>`:''}${hv?`<button class="btn sm" data-act="mv" data-arg="${k}:out:all">Load to hold</button>`:''}</div>
      <div class="lab">Sells best at (your scans)</div>${best.length?best.map(x=>`<div class="mkbest"><span>${esc(S.stations[x.sid]?S.stations[x.sid].name:DEF[x.sid].name)} <span class="mass" style="margin:0">${HOP[P.sector][x.sid]??'?'} jumps · ${fmtT(Math.max(0,S.T-x.T))} ago</span></span><span class="mono" style="color:${x.s>s?'#7ad9a7':'inherit'}">${fmt(x.s)}</span></div>`).join(''):`<div class="note">No other prices scanned yet.</div>`}`}
  h+=`</div></div>`;
  // Control Markers, where they're sold: a line under the tiles (the buy, load and hull-fix buttons the table had)
  if(mkFilter==='p_util'&&claimSold(c,P))h+=`<div class="mkbest" style="margin-top:14px;align-items:center;gap:10px"><span style="display:inline-flex;gap:8px;align-items:center">${gIcon('beacon',18)}<b>Control Marker</b> <span class="mass" style="margin:0">${mass('beacon')} t · takes an unclaimed or breached outpost · you ${P.cargo.beacon||0} · hangar ${c.storage.beacon||0}</span></span><span class="act"><button class="btn sm" data-act="buybeacon" ${P.credits>=CLAIM_PRICE?'':'disabled'}>Buy 1 · ${fmt(CLAIM_PRICE)} cr</button>${P.cargo.beacon?'':(c.storage.beacon?(beaconCls(P.cls)?`<button class="btn sm" data-act="mv" data-arg="beacon:out:1">Load</button>`:(f=>f?`<button class="btn sm" data-act="${f[0]}" data-arg="${f[1]}">${esc(f[2])}</button>`:'<span class="mass" style="margin:0">fighters and bombers only</span>')(hullFix(c,P,beaconCls,'interceptor'))):'')}</span></div>`;
  return h}
{const o=renderDock;renderDock=function(){const r=o.apply(this,arguments);try{if(dockTab!=='market'||S.unb||mkView!=='tiles')return r;const c=dockCtx(),P=S.player,B=$('dBody');if(!c||!c.market||!B)return r;
  const keep=[];let seen=false;for(const el of B.children){if(/Makers' works here/.test(el.textContent||'')&&el.classList.contains('h3'))seen=true;if(seen)keep.push(el)}
  const salv=[...B.querySelectorAll('p.note')].filter(n=>/aren't traded/.test(n.textContent));const salvAct=salv.length?salv[0].nextElementSibling:null;
  const host=document.createElement('div');host.innerHTML=mkHtml(c,P);const tailBox=document.createElement('div');tailBox.style.marginTop='18px';
  for(const el of keep)tailBox.appendChild(el);if(salv[0]){tailBox.appendChild(salv[0]);if(salvAct)tailBox.appendChild(salvAct)}
  B.innerHTML='';B.appendChild(host);B.appendChild(tailBox);const q=$('mkQ');if(q){q.addEventListener('change',e=>{mkQty=+e.target.value;renderDock()});q.addEventListener('input',e=>{const l=q.previousElementSibling&&q.previousElementSibling.querySelector('b');if(l)l.textContent=e.target.value})}}catch(err){console.error(err)}return r}}
{const o=dockClick;dockClick=function(act,arg){if(act==='fabk'){fabKind=arg||null;renderDock();return}if(act==='mksel'){mkSel=arg;mkQty=1;renderDock();return}if(act==='mkf'){mkFilter=arg;renderDock();return}if(act==='mkview'){mkView=arg;renderDock();return}return o.apply(this,arguments)}}
// the table view gets a way back
{const o=renderDock;renderDock=function(){const r=o.apply(this,arguments);try{if(dockTab==='market'&&!S.unb&&mkView==='table'){const B=$('dBody');if(B)B.insertAdjacentHTML('afterbegin',`<div class="act" style="margin-bottom:8px"><button class="btn sm" data-act="mkview" data-arg="tiles">Tiles view</button></div>`)}}catch(e){}return r}}
// ---- (user, 8 Nov 2026: "the parts don't show their strengths and weaknesses over a standard part", in the market) the
// Market's detail panel compares a part with the standard one: a maker's traits (strengths green, weaknesses red), what its
// grade adds; for a system, the difference it makes to your current hull's stats against the standard grade 1 system.
const TR_GOOD={dmg:1,e:-1,ammo:1,mag:1,lock:-1,ml:1,cargo:1,scan:1,speed:1,dh:1,dd:1};
const MK_ST={thrust:['thrust',1],maxSpd:['top speed',1],turn:['turning',1],eCap:['energy capacity',1],eRegen:['recharge',1],sCap:['shields',1],hull:['hull',1],dr:['damage resisted',1,'pt'],dmg:['gun and laser damage',1],shotCost:['laser energy a shot',-1],drill:['drilling',1],cargo:['hold',1],reload:['reload time',-1]};
function mkVsRow(txt,good){return`<div style="color:${good?'#7ad9a7':'#ff7a6a'}">${good?'▲':'▼'} ${esc(txt)}</div>`}
function mkVsStd(k,P){try{const I=ITEMS[k];if(!I)return'';const B=I.base&&ITEMS[I.base]?ITEMS[I.base]:I,g=I.grade||1,rows=[];
  if(I.sys){const sl=I.sys,T0={...P.tiers,[sl]:1},T1={...P.tiers,[sl]:g},a=shipStats(P.faction,P.cls,T0),b=shipStats(P.faction,P.cls,T1);
    for(const key in MK_ST){const A=a[key],Bv=b[key];if(typeof A!=='number'||typeof Bv!=='number'||Math.abs(Bv-A)<1e-9)continue;const[n,dir,u]=MK_ST[key];
      const d=u==='pt'?`${Bv>A?'+':'−'}${Math.round(Math.abs(Bv-A)*100)} pts ${n}`:`${Bv>A?'+':'−'}${Math.round(Math.abs(Bv/A-1)*100)}% ${n}`;rows.push(mkVsRow(d,(Bv>A)===(dir>0)))}
    for(const t in I.tr||{}){const v=I.tr[t];if(!v||!TR_TXT[t])continue;rows.push(mkVsRow(`${v>0?'+':'−'}${Math.round(Math.abs(v)*100)}% ${TR_TXT[t]} (its maker's trait)`,(v>0)===((TR_GOOD[t]||1)>0)))}
    if(sl==='weapon'){const r0=rackCapC(P.cls,1),r1=rackCapC(P.cls,g);if(r1>r0)rows.push(mkVsRow(`+${r1-r0} ${CLASSES[P.cls].torp?'torpedoes':'missiles'} carried`,true));if(g>1)rows.push(mkVsRow(`−${Math.round((1-(1-.07*(g-1)))*100)}% lock time`,true))}
    const nm=(FAC(P.faction)||{hulls:{}}).hulls[P.cls]||CLASSES[P.cls].name;
    return`<div class="mkvs"><div class="lab">Against a standard grade 1 system · on your ${esc(nm)}</div>${rows.length?rows.join(''):'<div class="note" style="margin:0">The same as a standard system.</div>'}</div>`}
  const kind=I.part||B.part;if(!kind)return'';const tr=I.tr||B.tr||{};
  for(const t in tr){const v=tr[t];if(!v||!TR_TXT[t])continue;const txt=t==='mag'?`${v>0?'+':''}${v} ${TR_TXT[t]}`:`${v>0?'+':'−'}${Math.round(Math.abs(v)*100)}% ${TR_TXT[t]}`;rows.push(mkVsRow(txt,(v>0)===((TR_GOOD[t]||1)>0)))}
  if(g>1&&typeof LD_EFF!=='undefined'&&LD_EFF[kind])rows.push(mkVsRow(`grade ${g}: ${LD_EFF[kind]} over grade 1`,true));
  return`<div class="mkvs"><div class="lab">Against the standard ${esc((WPN[kind]||UTIL[kind]||{}).name||'part')}</div>${rows.length?rows.join(''):'<div class="note" style="margin:0">The same as the standard part.</div>'}</div>`}catch(e){return''}}

