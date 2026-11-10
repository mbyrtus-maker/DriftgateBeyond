//@src 16zzzu_myjobs.js
// ============================================================ Beyond: the jobs you're on, in flight (user, 9 Nov 2026)
// "I can't see the job I'm currently on while in flight." The HUD's orders card showed only a job picked with Select job;
// the jobs taken with their own button (freight, escorts, guard jobs, black-market runs and contracts) had no row. Each now
// shows there while it lasts: what it is, where (and how far), and its pay or progress.
function myJobRow(ty,tag,title,sid,stat){const P=S.player,hp=sid&&HOP[P.sector]&&HOP[P.sector][sid]!=null?HOP[P.sector][sid]:null,
    where=!sid||!DEF[sid]?'':sid===P.sector?'here':`${DEF[sid].name} · ${hp} jump${hp===1?'':'s'}`;
  return`<div class="oi sd"><div class="om"><i class="otg ${ty}">${tag}</i>${esc(title)}</div><div class="os"><span>${esc(where)}</span><span class="ok">${esc(stat)}</span></div></div>`}
function myJobRows(){const P=S.player;if(!P||S.unb)return'';const me=pkeyOf(P),rows=[];
  try{for(const j of(typeof mfjAll==='function'?mfjAll():[])){if(j.st!=='taken'||!sameK(j.pk,me))continue;rows.push(myJobRow('log','Freight',mfjTitle(j),j.to,`${fmt(j.pay)} cr · ${Math.max(0,Math.ceil((j.due-S.T)/60))} min left`))}}catch(e){}
  try{for(const t of S.traders||[]){const E=t.esc;if(!E||!sameK(E.k,me))continue;const m=(t.syf||t.test||{}).m,to=t.to&&DEF[t.to]?DEF[t.to].name:'';
    rows.push(myJobRow('cmb','Escort',t.test?`Test pilot ${t.test.name}`:m&&MAKERS[m]?`${MAKERS[m].short} freighter to ${to}`:`${t.why||'Supplies'} to ${to}`,t.sector,`${E.hops}/${E.need} jumps`))}}catch(e){}
  try{for(const I of(typeof indAll==='function'?indAll():[])){const G=I.guard;if(!G||!sameK(G.k,me))continue;rows.push(myJobRow('cmb','Guard',`${I.name}'s ${CLASSES[I.cls]?CLASSES[I.cls].name:'miner'}`,I.sector,`paid ${fmt(G.paid||0)} of ${fmt((I.hire&&I.hire.cap)||0)} cr`))}}catch(e){}
  try{const R=P.run;if(R&&S.stations[R.to])rows.push(myJobRow('log','Run',`${R.n} ${ITEMS[R.item].name} into ${S.stations[R.to].name}`,R.to,`${fmt(R.pay)} cr · ${R.rating} heat`))}catch(e){}
  try{for(const x of(typeof bmoAll==='function'?bmoAll():[])){if(!x.taker||!bmoKeyOk(x.taker,P))continue;let title='',sid=null;
    if(x.k==='kill'){const L=leaderOf(x.tgt);title=`Assassinate ${lName(x.tgt)}`;sid=L&&L.ship&&L.ship.sid}
    else if(x.k==='ceo'){const t=(S.traders||[]).find(z=>z.id===x.tid);title=`Assassinate ${MAKERS[x.tgt]?MAKERS[x.tgt].short:'a maker'}'s CEO`;sid=t&&t.sector}
    else{const D=typeof rdsOf==='function'&&rdsOf(x.tgt);title=`${x.k==='spy'?'Spy on':'Sabotage'} ${MAKERS[x.tgt]?MAKERS[x.tgt].short:'a maker'}'s R&D`;sid=D&&D.sid}
    rows.push(myJobRow('cmb','Contract',title,sid,`${fmt(x.pay)} cr`))}}catch(e){}
  return rows.join('')}
{const o=jobHudRow;jobHudRow=function(){return o.apply(this,arguments)+myJobRows()}}
