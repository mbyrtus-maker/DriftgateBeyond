//@src 16zz_news.js
// ============================================================ the leaders' news box (Beyond, 3 Nov 2026)
// The user's ask: a news report on top of the "Recent" ticker showing the latest position or declaration from a faction's
// leader, keeping up to three before they fade. Every chronicle entry a leader speaks (it opens with their title and name:
// a border demand, an embargo, a trade pact, aid, an alliance offer or refusal, a reprisal, war, a ceasefire, a betrayal),
// every major turn of the galaxy (alliances, ceasefires, successions, a leader shot down) and the Dread Pirate's fortunes go
// into S.news (the host's; guests get it with the rest of the state). The box shows the newest three, each under its
// faction's colour and leader, for three minutes of game time, fading over the last thirty seconds. It shows whatever
// power you serve: this is galactic news, not your own channel.
const NEWS={max:3,life:180,fade:30,log:60};
function newsOf(msg,kind,who){if(!msg)return null;const m=String(msg);
  for(const f of FAC_IDS){const n=lName(f);if(n&&m.startsWith(n+' ')){const rest=m.slice(n.length+1);if(/^of /.test(rest))break;return{f,who:n,msg:rest.replace(/^./,c=>c.toUpperCase())}}}
  if(/^the Dread Pirate/i.test(m)){let n='';try{n=dpName()}catch(e){}if(n&&m.startsWith(n+' '))return{f:'pirate',who:n.replace(/^the /,''),msg:m.slice(n.length+1).replace(/^./,c=>c.toUpperCase())};return{f:'pirate',who:'The Unbound',msg:m.replace(/^the /,'The ')}}
  if(kind==='big'&&who&&who.length&&FAC_IDS.includes(who[0])){const f=who[0],pre=FAC(f).name+': ';return{f,who:lName(f),msg:m.startsWith(pre)?m.slice(pre.length):m}}
  return null}
// News items leave the Recent ticker (user, 3 Nov 2026): a chronicle line that goes into the box isn't fed to Recent too.
// The Dread Pirate's own announcements (☠ lines: taking the hat, going down, a raiding season, tribute, a bounty, a sale, an
// open house, lying low, the Ravager sailing) go into the box under the Unbound instead of Recent; the chronicle's shorter
// copies of the same events are left out of both.
let newsMute=0;
function newsOK(){return!!(S&&!S.training&&!(typeof STRAT_SIM==='function'&&STRAT_SIM()))}
function newsAdd(n,big){S.news=S.news||[];S.newsN=(S.newsN||0)+1;const x={id:S.newsN,T:S.T,f:n.f,who:n.who,msg:n.msg,big:big?1:0};S.news.push(x);while(S.news.length>NEWS.max)S.news.shift();
  S.newsLog=S.newsLog||[];S.newsLog.push(x);while(S.newsLog.length>NEWS.log)S.newsLog.shift()}
// (user, 8 Nov 2026) "A subtab in the overview should be the news report which shows all the recent galaxy news while docked":
// Overview → News lists the last 60 stories that went into the news box (the leaders' declarations, the galaxy's turns, the
// Dread Pirate's fortunes, the makers' launches, failures and liquidations), newest first, each under its side's colour,
// with how long ago it ran. A galaxy saved before keeps what was in the box.
// (user, 8 Nov 2026: "Galaxy news is blank when docked") the report also carries the galaxy's chronicle (wars, ceasefires,
// pacts, embargoes, successions: S.chron, which every galaxy has kept since it began), so an older save and a young galaxy
// aren't empty; a chronicle line already in the news log isn't shown twice.
function newsReportItems(){const N=(S.newsLog&&S.newsLog.length?S.newsLog:(S.news||[])).slice(),seen=new Set(N.map(x=>Math.round(x.T)+'|'+String(x.msg).slice(-40)));
  for(const c of S.chron||[]){const n=(typeof newsOf==='function'?newsOf(c.msg,'big',c.who):null)||{f:(c.who&&c.who[0])||'neutral',who:'',msg:c.msg};const key=Math.round(c.T)+'|'+String(n.msg).slice(-40);if(seen.has(key))continue;seen.add(key);
    N.push({T:c.T,f:n.f,who:n.who||(FAC(n.f)?FAC(n.f).name:''),msg:n.msg,big:0})}
  return N.sort((a,b)=>b.T-a.T).slice(0,NEWS.log)}
function newsReportHtml(P){const L=newsReportItems();
  let h=`<div class="h3">Galaxy news</div><p class="note" style="margin:0 0 10px">Newest first: the leaders' declarations and the galaxy's chronicle, the Unbound's and the makers' news.</p>`;
  if(!L.length)return h+`<div class="empty">No news yet.</div>`;
  h+=`<div class="nwrep">`+L.map(x=>{const col=sideCol(x.f),fac=x.f==='pirate'?'The Unbound':FAC(x.f)?FAC(x.f).short:sideName(x.f),ago=Math.max(0,S.T-x.T);
    return`<div class="nwi${x.big?' big':''}" style="border-left-color:${col};opacity:1"><div class="nwh"><b style="color:${col}">${esc(fac)}</b> · ${esc(x.who||'')}<span class="mass" style="float:right;margin:0">${ago<60?'just now':fmtT(ago)+' ago'}</span></div><div class="nwm">${esc(x.msg)}</div></div>`}).join('')+`</div>`;
  return h}
{const o=feed;feed=function(){if(newsMute)return;return o.apply(this,arguments)}}
{const o=chron;chron=function(msg,kind,who){let n=null;try{if(newsOK())n=newsOf(msg,kind,who)}catch(e){}
  if(!n)return o.apply(this,arguments);newsMute++;let r;try{r=o.apply(this,arguments)}finally{newsMute--}
  try{if(n.f!=='pirate')newsAdd(n,kind==='big')}catch(e){}return r}}
function newsDread(msg){let t=String(msg).replace(/^☠\s*/,''),n='';try{n=dpName()}catch(e){}const who=n?n.replace(/^the /,''):'The Unbound';
  if(n&&t.startsWith(n+' '))t=t.slice(n.length+1);return{f:'pirate',who:who.replace(/^./,c=>c.toUpperCase()),msg:t.replace(/^./,c=>c.toUpperCase())}}
{const o=allFeed;allFeed=function(msg,kind){try{if(!NET.cl&&newsOK()&&/^☠/.test(String(msg))){newsAdd(newsDread(msg),/takes the hat|is dead|went down/.test(msg));return}}catch(e){}return o.apply(this,arguments)}}
let newsSig='';
function newsRender(){const el=$('hNews');if(!el)return;const L=(S&&!S.training&&S.news||[]).filter(x=>S.T-x.T<NEWS.life);
  const sig=L.map(x=>x.id).join(',')+'|'+L.map(x=>Math.ceil(Math.min(NEWS.fade,NEWS.life-(S.T-x.T)))).join(',');if(sig===newsSig)return;newsSig=sig;
  el.hidden=!L.length;if(!L.length){el.innerHTML='';return}
  el.innerHTML=`<div class="cmt">News</div>`+L.slice().reverse().map(x=>{const left=NEWS.life-(S.T-x.T),op=left<NEWS.fade?Math.max(.08,left/NEWS.fade):1,col=sideCol(x.f),fac=x.f==='pirate'?'The Unbound':FAC(x.f)?FAC(x.f).short:sideName(x.f);
    return`<div class="nwi${x.big?' big':''}" style="border-left-color:${col};opacity:${op.toFixed(2)}"><div class="nwh"><b style="color:${col}">${esc(fac)}</b> · ${esc(x.who)}</div><div class="nwm">${esc(x.msg)}</div></div>`}).join('')}
{const o=hudUpdate;hudUpdate=function(){const r=o.apply(this,arguments);try{newsRender()}catch(e){}return r}}
