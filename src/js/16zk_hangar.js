//@src 16zk_hangar.js
// ============================================================ the Hangar (Beyond screens pass, 3 Nov 2026)
// The per-station Vault is the Hangar: it holds your cargo and the ships you aren't flying, at that station. One sub-tab under
// Ship holds both (the old Vault and Hangar tabs merged). Berths: 2 at a freeport or a power's station, more at your own Depot
// (one more per hangar module) or Station (one more with a hangar building). Free hulls are never berthed (as before). Ships
// berthed elsewhere are listed with where they are; fly them from there. Ship here works for contractors too: a Compact
// freighter brings up to 120 t from another hangar (60 cr + 2 cr a tonne a jump), and can be raided on the way.
// Ledger: unchanged (only goods' and ships' places change).
const HG={berths:2};
function hgKey(P){return vaultKey(P)}
function hgBerths(P,key){key=key||hgKey(P);const R=key&&S.stations[key];let n=HG.berths;if(R&&R.owner==='player'&&(R.pid||'me')===pkeyOf(P)){n+=((devOf(R).hangar)||0);if(R.pst&&(R.bld||[]).includes('hangar'))n+=2}return n}
function hgTag(P){const k=hgKey(P);for(const r of P.ships||[])if(r.at==null)r.at=k}
function hgHere(P){const k=hgKey(P);hgTag(P);return(P.ships||[]).filter(r=>r.at===k)}
// actions on berthed ships see only the ships berthed here; indices are into that list
function hgSwap(P,fn){const k=hgKey(P);hgTag(P);const all=P.ships||[],here=all.filter(r=>r.at===k),else_=all.filter(r=>r.at!==k);P.ships=here;try{return fn()}finally{for(const r of P.ships)r.at=k;P.ships=else_.concat(P.ships)}}
{const o=dockAction;dockAction=function(act,arg){const P=S.player;if(!S.unb&&['bstore','bfly','bsell','bupg'].includes(act)){
    if(act==='bstore'&&hgHere(P).length>=hgBerths(P)){dockErr=`This hangar has ${hgBerths(P)} berths, all taken: fly or sell a ship first.`;return}
    return hgSwap(P,()=>o.apply(this,arguments))}
  if(act==='shipv'&&!S.unb&&!P.sworn){dockErr=hgShipOrder(P,arg);return}
  return o.apply(this,arguments)}}
// the berth count shown where the old bay count was
{const o=shipsCount;shipsCount=function(P){return S&&!S.unb&&P===S.player&&P.docked?hgHere(P).length:o.apply(this,arguments)}}
// ---- Ship here, for contractors (Compact freighters)
{const o=shipQuote;shipQuote=function(P,k){const r=o.apply(this,arguments);if(r||S.unb||P.sworn)return r;
  const to=vaultKey(P),src=P.vaults&&P.vaults[k],sid=vaultSid(k);if(!to||!src||!sid||k===to)return null;if(!vaultOpen(k,P))return{why:vaultWhy(k,P)};
  const load=shipPick(src),m=invMass(load);if(!m)return null;const j=HOP[sid][P.sector]||0;return{load,m,j,fee:shipFee(m,j),all:m>=invMass(src)}}}
function hgShipOrder(P,k){const q=shipQuote(P,k);if(!q||q.why)return q&&q.why?`Can't ship from there: ${q.why}.`:'Nothing to ship.';if(P.credits<q.fee)return`Shipping costs ${fmt(q.fee)} cr.`;
  const src=P.vaults[k];for(const i in q.load)inv.take(src,i,q.load[i]);if(!invMass(src))delete P.vaults[k];payFrom(P,'neutral',q.fee);
  const t=haulSend('neutral',vaultSid(k),P.sector,q.load,'ship:'+S.nextId,`${P.name||'a pilot'}'s goods`,null);if(!t){inv.addAll(src,q.load);return'No route.'}t.own={k:pkey(),to:vaultKey(P),from:k};
  return`✓ A Compact freighter is bringing ${fmt(q.m)} t from ${vaultName(k)} (${q.j} jump${q.j===1?'':'s'}) for ${fmt(q.fee)} cr.${q.all?'':' That was a full load: order again for the rest.'} It can be raided on the way; pilots can escort it from Jobs.`}
// ---- one Hangar sub-tab under Ship: cargo, ships berthed here, ships elsewhere, other hangars
DOCK_TOP[1][2]=DOCK_TOP[1][2].filter(k=>k!=='storage');{const i=DOCK_TOP[3][2].indexOf('bay');DOCK_TOP[3][2].splice(i>=0?i:2,i>=0?1:0,'storage')}
// a hangar is where your vault was: the old "Vault" checks still hold
{const o=renderDock;renderDock=function(){const P=S.player;if(!S||S.unb||!P||!P.docked||dockTab!=='storage')return hgWords(o.apply(this,arguments));
  const c=dockCtx();if(!c||c.storage!==P.vault)return hgWords(o.apply(this,arguments));
  let bay='';try{dockTab='bay';o.apply(this,arguments);if(dockTab==='bay')bay=$('dBody').innerHTML}catch(e){}dockTab='storage';const r=o.apply(this,arguments);
  const here=hgHere(P),far=(P.ships||[]).filter(x=>x.at&&x.at!==hgKey(P)),HN=k=>esc((FAC(P.faction)||{hulls:{}}).hulls[k]||CLASSES[k].name);
  let h=`<div class="h3">Ships berthed here · ${here.length} / ${hgBerths(P)}</div>`+(bay?`<div class="hgbay">${bay}</div>`:'');
  if(far.length)h+=`<p class="note" style="margin:6px 0 14px">Berthed elsewhere: ${far.map(x=>`${HN(x.cls)} at ${esc(vaultName(x.at))}`).join(' · ')}. Fly them from there.</p>`;
  h+=`<div class="h3" style="margin-top:18px">Cargo</div>`;$('dBody').insertAdjacentHTML('afterbegin',h);hgWords();return r}}
// the bay view inside the Hangar drops its own intro and the "In the bay" heading (the berth heading replaces them)
function hgWords(r){try{const B=$('dBody');if(!B)return r;for(const el of B.querySelectorAll('.hgbay > p.note:first-child'))el.remove();
  const tw=document.createTreeWalker(B,NodeFilter.SHOW_TEXT);const L=[];while(tw.nextNode())L.push(tw.currentNode);
  for(const n of L){const t=n.nodeValue;if(!/[Vv]ault|In the bay|the bay|Store this ship in the bay/.test(t))continue;n.nodeValue=t.replace(/Store this ship in the bay/g,'Berth this ship here').replace(/In the bay · \d+ \/ \d+/g,'Your other ships here').replace(/\bthe bay\b/g,'the hangar').replace(/\bvaults\b/g,'hangars').replace(/\bVaults\b/g,'Hangars').replace(/\bvault\b/g,'hangar').replace(/\bVault\b/g,'Hangar')}
  const M=$('dMeta');if(M)for(const d of M.querySelectorAll('div'))if(d.firstChild&&d.firstChild.nodeType===3&&d.firstChild.nodeValue==='Vault')d.firstChild.nodeValue='Hangar';
  const E=$('dErr');if(E&&E.textContent)E.textContent=E.textContent.replace(/\bvaults\b/g,'hangars').replace(/\bvault\b/g,'hangar').replace(/\bVault\b/g,'Hangar').replace(/\bthe bay\b/g,'the hangar').replace(/ \(\d+\/3\)/g,'');
  const T=$('dTabs');if(T)for(const b of T.querySelectorAll('button')){if(/^Vault/.test(b.textContent))b.firstChild&&(b.firstChild.nodeValue=b.firstChild.nodeValue.replace('Vault','Hangar'))}}catch(e){}return r}
{const o=feed;feed=function(msg){if(typeof msg==='string'&&S&&!S.unb)arguments[0]=msg.replace(/\bvaults\b/g,'hangars').replace(/\bvault\b/g,'hangar').replace(/\bVault\b/g,'Hangar');return o.apply(this,arguments)}}
// Ship opens on the Loadout (user, 3 Nov 2026): it leads the Ship group, and the Ship tab always opens there
{const g=DOCK_TOP.find(x=>x[0]==='ship');if(g){g[2]=['upg',...g[2].filter(k=>k!=='upg')]}}
{const o=dockTop;dockTop=function(i){try{const T=DOCK_TOP[i];if(T&&T[0]==='ship'&&!S.unb)dockSubMem.ship='upg'}catch(e){}return o.apply(this,arguments)}}
{const o=renderDock;renderDock=function(){const r=o.apply(this,arguments);try{if(S&&!S.unb){const g=DOCK_TOP.find(x=>x[0]==='ship');for(const b of document.querySelectorAll('#dTabs .mtab'))if(b.getAttribute('aria-selected')!=='true'&&g[2].includes(b.dataset.arg)&&g[2].includes('upg')&&dockG.some(x=>x[0]==='ship'&&x[2].some(t=>t[0]==='upg')))b.dataset.arg='upg'}}catch(e){}return r}}
