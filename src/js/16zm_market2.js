//@src 16zm_market2.js
// ============================================================ the graphical market (Beyond screens pass, 3 Nov 2026)
// Trade → Market shows tiles grouped as Ore, Components, Weapons, Utility parts and Payload (a filter for each), each with
// its icon, price here, a stock meter and a mark (▲ wanted here, ▼ oversupplied). Your hold is a coloured bar on top. Pick a
// tile: buy, sell and galaxy-average prices (from your scans), the price here while you've watched it, a quantity slider with
// Buy and Sell, Load and Store against your hangar, and the best places to sell from your scans. "Table" shows the old list
// (every button it had, Claim Beacons included); the makers' works and salvage sales stay underneath.
let mkSel=null,mkFilter='none',mkView='tiles',mkQty=1;
// (user, 8 Nov 2026) systems are parts now: each system slot is its own filter under Parts (they used to fall under Components)
const MK_SYS=['engine','power','shield','weapon','armor','cargo','payload','drill'];
function mkGroup(k){const I=ITEMS[k];if(I&&I.sys)return'sys_'+I.sys;const g=giKind(k);return g==='msl'||g==='chg'||g==='rnd'?'pay':g==='con'?'ore':g}
const MK_GN={parts:'Parts',ore:'Ore',comp:'Components',wpn:'Weapons',util:'Utility parts',bcn:'Beacons',pay:'Payload',sys_engine:'Drives',sys_power:'Reactors',sys_shield:'Shield emitters',sys_weapon:'Fire control',sys_armor:'Armour',sys_cargo:'Cargo holds',sys_payload:'Payload bays',sys_drill:'Blast rigs'};
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
  // (user, 8 Nov 2026) the main menu is Ore, Components, Parts; Parts opens a second row of filters: each system slot, then
  // Weapons, Utility parts, Payload and Beacons
  const cnt0=g=>g==='bcn'?((typeof fbSold==='function'?fbSold(c,P).length:0)+(claimSold(c,P)?1:0)):items.filter(k=>mkGroup(k)===g).length,PARTS=[...MK_SYS.map(sl=>'sys_'+sl),'wpn','util','pay','bcn'],
    cnt=g=>g==='parts'?PARTS.reduce((a,x)=>a+cnt0(x),0):cnt0(g),CATS=['ore','comp','parts'];
  if(mkFilter==='parts'){mkFilter=PARTS.find(g=>cnt0(g))||'parts'}const inParts=mkFilter==='parts'||PARTS.includes(mkFilter);
  if(mkFilter==='all')mkFilter='none';
  h+=`<button class="mkf" type="button" data-act="mkview" data-arg="table" style="margin-left:14px">Table</button></div>`;
  // (user) the categories stay across the top as orange boxes, the picked one filled, so you can move between them
  h+=`<div class="obox-row">${CATS.map(g=>{const on=g==='parts'?inParts:mkFilter===g;return`<button class="obox${on?' on':''}" type="button" data-act="mkf" data-arg="${g}" ${cnt(g)?'':'disabled'} aria-pressed="${on}">${MK_GN[g]} <span>${cnt(g)}</span></button>`}).join('')}</div>`;
  // the second row, under Parts: one box for each system slot, then Weapons, Utility parts, Payload and Beacons (every one shown, dimmed
  // when none is on sale here)
  if(inParts)h+=`<div class="obox-row obox-sys">${PARTS.map(g=>`<button class="obox${mkFilter===g?' on':''}" type="button" data-act="mkf" data-arg="${g}" ${cnt0(g)?'':'disabled'} aria-pressed="${mkFilter===g}">${MK_GN[g]} <span>${cnt0(g)}</span></button>`).join('')}</div>`;
  if(mkFilter==='parts'){h+=`<div class="note" style="margin:10px 0 0">No parts on sale here.</div>`;return h}
  if(mkFilter==='none'){h+=`<div class="note" style="margin:10px 0 0">Pick a category to see what this market has.</div>`;return h}
  if(mkFilter!=='bcn'&&!items.some(k=>mkGroup(k)===mkFilter)){mkFilter='none';return mkHtml(c,P)}
  if(mkSel&&mkFilter!=='bcn'&&mkGroup(mkSel)!==mkFilter)mkSel=items.find(k=>mkGroup(k)===mkFilter)||null;
  if(mkFilter==='bcn')mkSel=null;
  h+=`<div class="mkwrap"><div class="mktiles">`;
  for(const g of['ore','comp','wpn','util','pay',...MK_SYS.map(sl=>'sys_'+sl)]){if(mkFilter!=='all'&&mkFilter!==g)continue;const L=items.filter(k=>mkGroup(k)===g);if(!L.length)continue;
    h+=`<div class="mkgrp"><div class="lab">${MK_GN[g]}</div><div class="mkrow">`;
    for(const k of L){const dm=demandOf(mR(c),k),stk=st[k]||0,on=k===mkSel,tgt=Math.max(1,stockTarget(k)),r=stk/tgt;
      h+=`<button class="mkt${on?' on':''}" type="button" data-act="mksel" data-arg="${k}"><span class="mktt">${gIcon(k,22)}<span><b>${esc(ITEMS[k].name)}</b><br><span class="mono amber">${fmt(mBuy(c,k))}</span>${dm==='high'?' <span style="color:#7ad9a7">▲</span>':dm==='low'?' <span style="color:#ff9a4a">▼</span>':''}</span></span>
        <span class="mkm"><i style="width:${Math.min(100,Math.round(r*50))}%;background:${dm==='high'?'#7ad9a7':dm==='low'?'#ff9a4a':'#5a647c'}"></i></span><span class="mass" style="margin:0">${stk} in stock · you ${countIn(k,srcs)||'·'}</span></button>`}
    h+=`</div></div>`}
  if(!items.length&&mkFilter!=='bcn')h+=`<div class="empty">Nothing in stock.</div>`;
  h+=`</div><div class="mkdet">`;
  if(mkSel){const k=mkSel,b=mBuy(c,k),s=mSell(c,k),sc=mkScan(P,k),avg=sc.length?Math.round(sc.reduce((a,x)=>a+x.s,0)/sc.length):null,stk=st[k]||0,hold=P.cargo[k]||0,hv=c.storage[k]||0,have=hold+hv;
    const room=Math.max(0,Math.floor((cap-used)/mass(k))),maxQ=Math.max(1,stk,have);mkQty=Math.min(Math.max(1,mkQty),maxQ);
    const H=(P.pxh&&P.pxh[P.sector]&&P.pxh[P.sector].p[k])||[];let spark='';if(H.length>1){const lo=Math.min(...H,avg||Infinity)*.95,hi=Math.max(...H,avg||0)*1.05,Y=v=>Math.round(48-(v-lo)/Math.max(1,hi-lo)*44);
      spark=`<svg width="320" height="52" viewBox="0 0 320 52" role="img" aria-label="Price here"><polyline points="${H.map((v,i)=>Math.round(i*320/(H.length-1))+','+Y(v)).join(' ')}" fill="none" stroke="#f0b24a" stroke-width="1.6"/>${avg?`<line x1="0" x2="320" y1="${Y(avg)}" y2="${Y(avg)}" stroke="#36435f" stroke-dasharray="3 4"/>`:''}</svg>`}
    const best=sc.filter(x=>x.sid!==P.sector).sort((a,b2)=>b2.s-a.s).slice(0,3);
    h+=`<div class="ldname">${gIcon(k,30)}<b>${esc(ITEMS[k].name)}</b></div><div class="note" style="margin:0 0 10px">${mass(k)} t · ${stk} in stock · you carry ${hold}, ${hv} in your ${esc(c.storageName==='Vault'?'hangar':c.storageName.toLowerCase())}${ITEMS[k].trTxt?' · '+esc(ITEMS[k].trTxt):''}</div>
      <div class="mkpx"><span>Buy<b class="mono">${fmt(b)}</b></span><span>Sell<b class="mono">${fmt(s)}</b></span><span title="The average price you'd get selling this at the stations you've scanned">Galaxy sell<b class="mono" style="color:var(--dim)">${avg?fmt(avg):'—'}</b></span></div>
      ${spark?`${spark}<div class="note" style="margin:0 0 10px">Sell price here while you've watched${avg?' · dashed: the average sell price at the stations you\'ve scanned':''}</div>`:`<div class="note" style="margin:6px 0 10px">Stay docked a while to see how the price moves.</div>`}
      <div style="display:flex;justify-content:space-between;align-items:baseline"><span class="lab">Quantity</span><b class="mono">${mkQty}</b></div>
      <input type="range" id="mkQ" min="1" max="${maxQ}" value="${mkQty}" aria-label="Quantity" style="width:100%;accent-color:#f0b24a">
      <div class="act" style="margin:8px 0"><button class="btn pri" data-act="buy" data-arg="${k}:${mkQty}" ${!(stk>0)||P.credits<b?'disabled':''}>Buy ${mkQty} · ${fmt(b*mkQty)} cr</button><button class="btn" data-act="sell" data-arg="${k}:${Math.min(mkQty,have)}" ${have<1?'disabled':''}>Sell ${Math.min(mkQty,have)} · ${fmt(s*Math.min(mkQty,have))} cr</button></div>
      <div class="act" style="margin-bottom:12px"><button class="btn sm" data-act="buy" data-arg="${k}:fill" ${!(stk>0)||P.credits<b||room<1?'disabled':''}>Fill hold</button><button class="btn sm" data-act="sell" data-arg="${k}:all" ${have<1?'disabled':''}>Sell all</button>${hold?`<button class="btn sm" data-act="mv" data-arg="${k}:in:all">Store all</button>`:''}${hv?`<button class="btn sm" data-act="mv" data-arg="${k}:out:all">Load to hold</button>`:''}</div>
      <div class="lab">Sells best at (your scans)</div>${best.length?best.map(x=>`<div class="mkbest"><span>${esc(S.stations[x.sid]?S.stations[x.sid].name:DEF[x.sid].name)} <span class="mass" style="margin:0">${HOP[P.sector][x.sid]??'?'} jumps · ${fmtT(Math.max(0,S.T-x.T))} ago</span></span><span class="mono" style="color:${x.s>s?'#7ad9a7':'inherit'}">${fmt(x.s)}</span></div>`).join(''):`<div class="note">No other prices scanned yet.</div>`}`}
  h+=`</div></div>`;
  // Claim Beacons, where they're sold: a line under the tiles (the buy, load and hull-fix buttons the table had)
  if(mkFilter==='bcn'&&claimSold(c,P))h+=`<div class="mkbest" style="margin-top:14px;align-items:center;gap:10px"><span style="display:inline-flex;gap:8px;align-items:center">${gIcon('beacon',18)}<b>Claim Beacon</b> <span class="mass" style="margin:0">${mass('beacon')} t · takes an unclaimed or breached outpost · you ${P.cargo.beacon||0} · hangar ${c.storage.beacon||0}</span></span><span class="act"><button class="btn sm" data-act="buybeacon" ${P.credits>=CLAIM_PRICE?'':'disabled'}>Buy 1 · ${fmt(CLAIM_PRICE)} cr</button>${P.cargo.beacon?'':(c.storage.beacon?(beaconCls(P.cls)?`<button class="btn sm" data-act="mv" data-arg="beacon:out:1">Load</button>`:(f=>f?`<button class="btn sm" data-act="${f[0]}" data-arg="${f[1]}">${esc(f[2])}</button>`:'<span class="mass" style="margin:0">fighters and bombers only</span>')(hullFix(c,P,beaconCls,'interceptor'))):'')}</span></div>`;
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
