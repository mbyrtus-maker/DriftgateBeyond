//@src 16zzg_marque.js
// ============================================================ Scrapheart's own tabs; letters of marque (Beyond, 3 Nov 2026)
// The user's asks: docked at Scrapheart (the Wrack), the top tabs have their own names: Overview, Plunder (Trade), Tavern
// (Jobs), Ship, Marques (Allegiance). On Marques an independent pilot can take a power's letter of marque and fly its
// privateer flag: while flying it you count as one of that power's own (its ships are friends; its enemies' ships attack you
// and their stations refuse you; its stations take you in), except that the Unbound see a privateer, not a power's pilot,
// and leave you be. The sponsor pays the bounty for every ship you destroy of a power it's at war with, and of the Brood.
// Strike the flag at Scrapheart any time; it's struck for you if you swear to a faction, declare your own, or fall to
// Hostile with your sponsor.
const MARQ={min:-10};
function marqOf(P){P=P||S.player;const f=P&&P.marque;if(!f||!FAC_IDS.includes(f)||P.sworn||P.decl||S.unb)return null;return f}
function marqWar(f,x){return x==='brood'||(FAC_IDS.includes(x)&&x!==f&&warWith(f,x))}
{const o=pilotHostile;pilotHostile=function(P,x){P=P||S.player;const f=marqOf(P);if(f&&x&&x!=='player'){if(x==='pirate'){if(P.aggro&&P.aggro.pirate>S.T)return true;return false}if(x===f)return false;if(FAC_IDS.includes(x))return hostile(f,x)||o.apply(this,arguments);if(x==='brood')return true}return o.apply(this,arguments)}}
{const o=tradeOK;tradeOK=function(P,owner){P=P||S.player;const f=marqOf(P);if(f&&FAC_IDS.includes(owner)){if(owner===f)return true;if(hostile(f,owner))return false}return o.apply(this,arguments)}}
{const o=bountyPayer;bountyPayer=function(victim,P){P=P||S.player;const f=marqOf(P);if(f&&marqWar(f,victim))return f;return o.apply(this,arguments)}}
{const o=standAdd;standAdd=function(f,n,why,P){const r=o.apply(this,arguments);try{P=P||S.player;if(P&&P.marque===f&&standOf(f,P)<=STAND.hostile){P.marque=null;const m=`⚑ ${FACTIONS[f].short} revokes your letter of marque: you're Hostile with them.`;audTell(P,m,'bad')}}catch(e){}return r}}
function marqTake(P,f){if(P.sworn)return'You fly for a faction: privateers are independents.';if(P.decl)return'You lead your own faction.';if(!FAC_IDS.includes(f))return'';
  if(P.marque===f){P.marque=null;return`You strike the ${FACTIONS[f].short} flag: you fly as an independent again.`}
  if(standOf(f,P)<MARQ.min)return`${FACTIONS[f].short} won't sponsor you: your standing with them is ${standName(standOf(f,P))}.`;
  const was=P.marque;P.marque=f;const foes=[...FAC_IDS.filter(g=>g!==f&&warWith(f,g)).map(g=>FACTIONS[g].short),'the Brood'].join(', ');
  return`✓ You fly the ${FACTIONS[f].short} privateer flag${was&&was!==f?` (the ${FACTIONS[was].short} flag struck)`:''}. ${FACTIONS[f].short} pays for every ship you destroy of ${foes}; its enemies' ships will come for you.`}
function marqHtml(P){const f=marqOf(P);let h=`<div class="ldbox" style="margin:0 0 18px;border-left:3px solid ${f?FACTIONS[f].col:'#f0b24a'}"><div class="lab">Letters of marque</div><div class="ldname"><b>${f?`Flying the ${esc(FACTIONS[f].short)} flag`:'No flag'}</b></div>`;
  h+=`<div class="note" style="margin:4px 0 10px">A power's privateer counts as one of its own: its ships are friends, its enemies' ships attack you and their stations refuse you. The Unbound see a privateer and leave you be. Your sponsor pays the bounty for every ship you destroy of a power it's at war with, and of the Brood.${P.sworn?' <b>You fly for a faction: privateers are independents.</b>':P.decl?' <b>You lead your own faction.</b>':''}</div>`;
  if(P.sworn||P.decl)return h+'</div>';
  for(const g of FAC_IDS){const st=standOf(g,P),foes=[...FAC_IDS.filter(x=>x!==g&&warWith(g,x)).map(x=>FACTIONS[x].short),'Brood'],on=f===g;
    h+=`<div class="ldopt"><span style="flex:1;min-width:0"><b style="color:${FACTIONS[g].col}">${esc(FACTIONS[g].name)}</b><br><span class="mass" style="margin:0">pays for: ${esc(foes.join(', '))} · your standing ${esc(standName(st))}</span></span><button class="btn sm${on?'':' pri'}" type="button" data-act="marque" data-arg="${g}" ${on||st>=MARQ.min?'':'disabled'}>${on?'Strike the flag':'Fly this flag'}</button></div>`}
  return h+'</div>'}
{const o=allegianceHtml;allegianceHtml=function(P){P=P||S.player;let a='';try{const c=P.docked?dockCtx():null;if(c&&c.rum)a=marqHtml(P)}catch(e){}return a+o.apply(this,arguments)}}
{const o=dockAction;dockAction=function(act,arg){if(act==='marque'){const c=dockCtx();if(!c||!c.rum){dockErr='Letters of marque are had at Scrapheart.';return}dockErr=marqTake(S.player,String(arg));return}return o.apply(this,arguments)}}
// Scrapheart's tab names
const WR_TABS={trade:'Plunder',jobs:'Tavern',allegiance:'Marques'};
{const o=renderDock;renderDock=function(){let c=null;try{c=S&&S.player&&S.player.docked?dockCtx():null}catch(e){}if(!c||!c.rum)return o.apply(this,arguments);
  const keep=DOCK_TOP.map(g=>g[1]);for(const g of DOCK_TOP)if(WR_TABS[g[0]])g[1]=WR_TABS[g[0]];try{return o.apply(this,arguments)}finally{DOCK_TOP.forEach((g,i)=>g[1]=keep[i])}}}
// the HUD's ship line shows the flag
{const o=hudUpdate;hudUpdate=function(){const r=o.apply(this,arguments);try{const f=marqOf(S.player),el=$('hSub');if(el&&f&&!/privateer/.test(el.textContent))el.insertAdjacentHTML('beforeend',` · <span style="color:${FACTIONS[f].col}">⚑ ${esc(FACTIONS[f].short)} privateer</span>`)}catch(e){}return r}}
// ---- (user) the black market at Scrapheart: under Plunder, a Black market tab (the Company screen's Black market: every offer
// your contacts have, runs, buys, quiet buyers and fences, to take, assign or broker); and the Tavern lists those offers as jobs
{const T=DOCK_TOP.find(g=>g[0]==='trade');if(T&&!T[2].includes('bmk')){const i=T[2].indexOf('market');T[2].splice(i>=0?i+1:0,0,'bmk')}}
{const o=renderDock;renderDock=function(){const r=o.apply(this,arguments);try{if(dockTab!=='bmk'||S.unb)return r;const c=dockCtx(),B=$('dBody');if(!c||!c.rum||!B)return r;
  B.innerHTML=`<p class="note" style="margin:0 0 12px">The Rusty Tankard's back room: every offer your contacts have for you, from Scrapheart and every station where you've met a fixer or a quiet buyer. Take a run yourself, give it to one of your crews, or broker it to a contractor.</p>`+bmxHtml(S.player)}catch(e){console.error(e)}return r}}
{const B=$('dBody');if(B)B.addEventListener('click',e=>{if(dockTab!=='bmk')return;const b=e.target.closest('[data-co]');if(!b||b.disabled)return;e.stopPropagation();try{coClick(b.dataset.co,b.dataset.arg)}catch(x){console.error(x)}dockErr=coErr||'';renderDock()})}
{const o=jobsList;jobsList=function(c,P,srcs){const out=o.apply(this,arguments);if(!c||!c.rum||S.unb)return out;try{
  for(const x of bmOffers(P)){if(x.rum&&!x.kind&&x.from===WRACK.sid)continue;const at=x.kind?x.from:x.from,h=HOP[P.sector]&&HOP[P.sector][at]!=null?HOP[P.sector][at]:0,pay=bmPay(x);
    out.push({id:'bmo:'+x.id,by:'pirate',sid:at,ty:'haul',title:`Black market · ${esc(bmKind(x))}: ${bmDesc(x)}`,sub:`${x.rating||'None'} heat${x.f&&FACTIONS[x.f]?' with '+esc(FACTIONS[x.f].short):''} · ${Math.max(0,Math.round((x.until-S.T)/60))} min left`,hops:h,where:h?`${h} jump${h>1?'s':''}`:'here',payN:pay,pay:`${pay<0?'−':''}${fmt(Math.abs(pay))} cr`,btn:['tab','bmk','Open in the Black market'],
      detail:()=>`<p class="note" style="margin:0">${bmDesc(x)}. Take it, give it to a crew or broker it from Plunder → Black market. ${x.rating&&x.rating!=='None'?`Caught, it adds <b>${esc(x.rating)}</b> heat${x.f&&FACTIONS[x.f]?' with '+esc(FACTIONS[x.f].short):''}.`:''}</p>`})}}catch(err){console.error(err)}return out}}
