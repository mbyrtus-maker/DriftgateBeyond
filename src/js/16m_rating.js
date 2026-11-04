//@src 16m_rating.js
// ============================================================ Contractor Rating (Beyond stage 8)
// Rating 1-10, per galaxy, rising with Rating points from work done for the powers (everything that raises standing through
// standWork: deliveries, escorts, kills paid by a power, claims, beacon flips, limpets), anomaly scans and black-market runs.
// Rating only goes up. It gates which hulls a yard will sell you and which grade your parts and systems can be upgraded to.
const RATING={k:20,anom:60,run:80,need:[0,0,150,350,600,950,1400,1950,2600,3400,4300]};
const HULL_RATING={interceptor:1,skiff:1,courier:1,striker:2,prospector:2,freighter:2,scout:2,heavy:4,bomber:4,scout2:4,dredger:5,bulker:5,gunboat:6,wraith:1};
const GRADE_RATING=[0,1,2,4,6,8];
function ratingOf(P){P=P||S.player;const p=(P&&P.rp)||0;let r=1;for(let i=2;i<=10;i++)if(p>=RATING.need[i])r=i;return r}
function ratingNext(P){const r=ratingOf(P);return r>=10?null:RATING.need[r+1]}
function gradeCap(P){const r=ratingOf(P);let g=1;for(let i=1;i<=5;i++)if(r>=GRADE_RATING[i])g=i;return g}
function rpAdd(P,n,why){if(!P||!(n>0)||S.training)return;const r0=ratingOf(P);P.rp=(P.rp||0)+n;const r1=ratingOf(P);
  if(r1>r0){const msg=`★ Contractor Rating ${r1}${why?` (${why})`:''}. ${hullsAt(r1).length?`New hulls: ${hullsAt(r1).map(k=>CLASSES[k].name).join(', ')}. `:''}${GRADE_RATING.indexOf(r1)>0?`Parts and systems now upgrade to grade ${GRADE_RATING.indexOf(r1)}.`:''}`;
    if(P===S.player){feed(msg,'good');flash(msg)}else{const k=Object.keys(S.pilots||{}).find(x=>S.pilots[x]===P);if(k)netMsg(k,'feed',msg,'good')}}}
function hullsAt(r){return Object.keys(HULL_RATING).filter(k=>HULL_RATING[k]===r&&k!=='wraith')}
{const o=standWork;standWork=function(P,f,n,what){const r=o.apply(this,arguments);try{if(n>0)rpAdd(P,n*RATING.k,what)}catch(err){}return r}}
{const o=anomOpen;anomOpen=function(sid,A,k){const r=o.apply(this,arguments);try{const P=xPilotOfKey(k)||S.player;rpAdd(P,RATING.anom,'a discovery')}catch(err){}return r}}
// a black-market run delivered counts too
{const o=openDock;openDock=function(){const had=S.player&&S.player.run;const r=o.apply(this,arguments);try{if(had&&!S.player.run)rpAdd(S.player,RATING.run,'a black-market run')}catch(err){}return r}}
// ---- hulls by Rating: a yard won't sell a hull above your Rating (the free starters and the Wraith aside)
function hullRatingOK(P,k){return S.unb||S.training||!!P.sworn||ratingOf(P)>=(HULL_RATING[k]||1)}
{const o=dockAction;dockAction=function(act,arg){if((act==='hull'||act==='hullsw')&&!hullRatingOK(S.player,arg)){dockErr=`The ${CLASSES[arg].name} needs Contractor Rating ${HULL_RATING[arg]} (you're ${ratingOf(S.player)}).`;return}
  // (4 Nov 2026, a guest test) a part's next grade above your Rating says so, as a system's does (it said the part couldn't be upgraded further)
  if(act==='pup'&&!S.unb&&!S.training){const P=S.player,[g,i0]=String(arg).split(':'),F=fitOf(P),k=((g==='w'?F.w:F.u)||[])[+i0],t=(((g==='w'?F.g:F.ug)||[])[+i0]||1)+1;if(k&&k!=='land'&&k!=='claim'&&t<=MK_TOP&&t>gradeCap(P)){dockErr=`Grade ${t} parts need Contractor Rating ${GRADE_RATING[t]} (you're ${ratingOf(P)}).`;return}}
  if(act==='upg'&&!S.unb&&!S.training){const P=S.player,t=(P.tiers[arg]||1)+1;if(t>gradeCap(P)){dockErr=`Grade ${t} needs Contractor Rating ${GRADE_RATING[t]} (you're ${ratingOf(P)}).`;return}}return o.apply(this,arguments)}}
{const o=upgReady;upgReady=function(c,P,srcs){const u=o.apply(this,arguments);if(u&&!S.unb&&!S.training&&u.t+1>gradeCap(P))return null;return u}}
// ---- part grades by Rating; a maker's grade 4 and 5 parts also need Trusted standing with its power
{const o=pupQuote;pupQuote=function(c,P,arg){const q=o.apply(this,arguments);if(!q||S.training)return q;if(q.t>gradeCap(P))return null;
  const[g,i0]=String(arg).split(':'),F=fitOf(P),it=((g==='w'?F.wi:F.ui)||[])[+i0],m=it&&ITEMS[it]&&ITEMS[it].maker,h=m&&MAKERS[m].home;if(q.t>=4&&FAC_IDS.includes(h)&&standOf(h,P)<=25&&P.sworn!==h)return null;return q}}
// ---- where it shows: the Overview's standing row and the Allegiance tab, and the hull cards' requirement
function ratingHtml(P){const r=ratingOf(P),nx=ratingNext(P);return`<div class="kv"><span>Contractor Rating</span><b class="amber">${r}${nx?` <span class="mass" style="margin:0">${fmt(P.rp||0)} / ${fmt(nx)} points</span>`:' · top'}</b></div><p class="note" style="margin:2px 0 8px">Work done for the powers raises it, and it never falls. It opens bigger hulls (2: Medium hulls and the Scout; 4: Heavy Fighter, Bomber and Advanced Scout; 5: Heavy Miner and Hauler; 6: Heavy Bomber) and higher grades (2 at Rating 2, 3 at 4, 4 at 6, 5 at 8).</p>`}
{const o=allegianceHtml;allegianceHtml=function(P){P=P||S.player;return(P.sworn||S.unb?'':ratingHtml(P))+o.apply(this,arguments)}}
