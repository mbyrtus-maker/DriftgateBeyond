//@src 16zz_news.js
// ============================================================ the leaders' news box (Beyond, 3 Nov 2026)
// The user's ask: a news report on top of the "Recent" ticker showing the latest position or declaration from a faction's
// leader, keeping up to three before they fade. Every chronicle entry a leader speaks (it opens with their title and name:
// a border demand, an embargo, a trade pact, aid, an alliance offer or refusal, a reprisal, war, a ceasefire, a betrayal),
// every major turn of the galaxy (alliances, ceasefires, successions, a leader shot down) and the Dread Pirate's fortunes go
// into S.news (the host's; guests get it with the rest of the state). The box shows the newest three, each under its
// faction's colour and leader, for three minutes of game time, fading over the last thirty seconds. It shows whatever
// power you serve: this is galactic news, not your own channel.
const NEWS={max:3,life:180,fade:30};
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
function newsAdd(n,big){S.news=S.news||[];S.newsN=(S.newsN||0)+1;S.news.push({id:S.newsN,T:S.T,f:n.f,who:n.who,msg:n.msg,big:big?1:0});while(S.news.length>NEWS.max)S.news.shift()}
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
  el.innerHTML=`<div class="cmt">News</div>`+L.slice().reverse().map(x=>{const left=NEWS.life-(S.T-x.T),op=left<NEWS.fade?Math.max(.08,left/NEWS.fade):1,col=sideCol(x.f),fac=x.f==='pirate'?'The Unbound':FAC(x.f).short;
    return`<div class="nwi${x.big?' big':''}" style="border-left-color:${col};opacity:${op.toFixed(2)}"><div class="nwh"><b style="color:${col}">${esc(fac)}</b> · ${esc(x.who)}</div><div class="nwm">${esc(x.msg)}</div></div>`}).join('')}
{const o=hudUpdate;hudUpdate=function(){const r=o.apply(this,arguments);try{newsRender()}catch(e){}return r}}
