//@src 16zzf_audience.js
// ============================================================ an audience with a power's leader (Beyond, 3 Nov 2026)
// The user's ask and choices: at a power's station you can request an audience with its leader, once you lead a declared
// faction. You're told how long until the leader docks there; while the leader is docked (five minutes) you can ask for
// agreements, paying with your standing with that power. Agreements last a set time. Leaders can refuse: their traits and
// what they think of you sway it, and a refusal costs nothing (that request waits a few minutes before you can ask again).
// Requests: non-aggression pact, ceasefire, open trade, alliance against a power or the Brood, war on a power, trade pact,
// aid, joint defence, and three more (shared intel, a pardon, yard access).
const AUD={hop:45,base:30,open:300,cool:600,refuse:180};
const AUD_REQ={
  nap:{n:'Non-aggression pact',cost:15,min:-40,dur:1800,lean:['Cautious','Patient','Honourable','Mercantile'],never:['Ambitious'],d:'Their ships and strikes leave you and your bases alone.'},
  cease:{n:'Ceasefire',cost:10,min:-90,dur:1200,lean:['Cautious','Patient','Honourable','Mercantile'],never:[],d:'Ends their aggression on you and lifts their hostility for a while.',only:(P,f)=>standOf(f,P)<STAND.dock||(P.aggro&&P.aggro[f]>S.T)},
  trade:{n:'Open trade',cost:20,min:-10,dur:1800,lean:['Mercantile','Industrious'],never:['Isolationist'],d:'Their markets buy from you 10% higher and sell to you 10% lower.'},
  tpact:{n:'Trade pact',cost:15,min:0,dur:1800,lean:['Mercantile','Industrious','Patient'],never:['Isolationist'],d:'Their merchants call at your bases, and pay their fees.'},
  aid:{n:'Aid shipment',cost:20,min:0,dur:0,lean:['Cautious','Patient','Loyal','Honourable'],never:['Isolationist'],d:'Materials from their warehouse to your Station: alloy plate, wire and coils.'},
  def:{n:'Joint defence',cost:20,min:10,dur:900,lean:['Honourable','Loyal','Cautious'],never:['Isolationist'],d:'A wing of theirs guards your Station.'},
  intel:{n:'Shared intel',cost:10,min:0,dur:1800,lean:['Scheming','Mercantile','Opportunist'],never:[],d:'Their sensors show you every system they watch.'},
  pardon:{n:'Pardon',cost:15,min:-40,dur:0,lean:['Patient','Honourable','Mercantile'],never:['Vengeful'],d:'Clears your heat with them and their grudge for recent attacks.'},
  yard:{n:'Yard access',cost:15,min:10,dur:1800,lean:['Mercantile','Industrious','Ambitious'],never:[],d:'Their shipyards sell you hulls one Contractor Rating above yours.'},
  ally:{n:'Alliance against',cost:30,min:25,dur:1800,lean:['Patient','Cautious','Honourable','Loyal','Opportunist'],never:['Isolationist'],d:'They turn their strikes on the side you name, and treat you as an ally.',tgt:'ally'},
  war:{n:'War on',cost:35,min:25,dur:1800,lean:['Ambitious','Vengeful','Opportunist','Ruthless'],never:['Cautious','Isolationist'],d:'They declare war on the power you name.',tgt:'war'}};
function audOn(P){return!!(P&&P.decl&&!P.sworn&&!S.unb&&!S.training)}
function audOf(P,f){P.aud=P.aud||{};return P.aud[f]||null}
function audDeal(P,f,k){return(P.deals||[]).find(d=>d.f===f&&d.k===k&&S.T<d.until)||null}
function audDeals(P,k){return(P.deals||[]).filter(d=>d.k===k&&S.T<d.until)}
// how a leader leans on a request: 0 won't, otherwise a chance
function audChance(f,k,P,x){const R=AUD_REQ[k],L=leaderOf(f);if(!L)return 0;if((R.never||[]).some(t=>L.traits.includes(t)))return 0;if(k==='cease'&&L.traits.includes('Vengeful')&&standOf(f,P)<-60)return 0;
  if((k==='war'||k==='ally')&&x&&x===f)return 0;let n=0;for(const t of L.traits)if(R.lean.includes(t))n++;let c=.35+.15*n+standOf(f,P)/250;
  if(k==='war'&&x&&isPow(x)){const r=relOf(f,x);c+=-r/200;if(pairOf(f,x)&&pairOf(f,x).ally)c-=.4}if(k==='ally'&&x&&isPow(x))c+=-relOf(f,x)/250;return clamp(c,.05,.95)}
function audWord(c){return c<=0?['won\'t hear of it','var(--danger)']:c<.3?['reluctant','#ff9a4a']:c<.6?['open to it','var(--dim)']:['keen','#7ad9a7']}
// ---- requesting: the leader's flagship sets course for this station
function audRequest(P,f){if(!audOn(P))return'Leaders grant audiences only to the heads of declared factions.';const R=S.stations[P.sector];if(!R||R.owner!==f)return'Ask at one of their stations.';
  const L=leaderOf(f);if(!L||!L.ship)return'They have no leader right now.';if(!L.ship.alive)return`${lName(f)} isn't flying: back in ${fmtT(Math.max(0,L.ship.back-S.T))}.`;
  if(standOf(f,P)<=STAND.hostile)return`${lName(f)} won't receive you: you're Hostile with ${FACTIONS[f].short}.`;const A=audOf(P,f);if(A&&A.stage!=='done')return'You already have an audience requested.';
  if(A&&S.T<A.next)return`${lName(f)} will receive you again in ${fmtT(A.next-S.T)}.`;if(L.ship.aud&&L.ship.aud.pk!==pkeyOf(P)&&L.ship.aud.until>S.T)return`${lName(f)} is busy with another audience.`;
  const h=HOP[L.ship.sid]&&HOP[L.ship.sid][R.sid]!=null?HOP[L.ship.sid][R.sid]:3;P.aud[f]={sid:R.sid,stage:'coming',T:S.T,eta:S.T+AUD.base+h*AUD.hop,next:0};
  L.ship.aud={pk:pkeyOf(P),sid:R.sid,eta:P.aud[f].eta,until:P.aud[f].eta+AUD.open};
  return`✓ ${lName(f)} will receive you at ${R.name}: about ${fmtT(P.aud[f].eta-S.T)} until the flagship docks.`}
// the flagship flies there (one jump at a time), docks and stays for the audience; then it goes about its business
{const o=leaderShipTick;leaderShipTick=function(){if(!NET.cl&&S&&S.leaders&&!S.training)for(const f of FAC_IDS){const L=leaderOf(f),Sh=L&&L.ship,A=Sh&&Sh.aud;if(!A)continue;
    if(!Sh.alive||S.T>A.until){Sh.aud=null;continue}
    if(Sh.sid!==A.sid){const steps=HOP[Sh.sid]&&HOP[Sh.sid][A.sid];const left=A.eta-S.T;if(steps!=null&&left<=steps*AUD.hop){const nx=(NEIGH[Sh.sid]||[]).find(n=>HOP[n]&&HOP[n][A.sid]===steps-1);if(nx){if(Sh.live){const e=leaderEnt(f);if(e)try{despawn(e)}catch(x){}Sh.live=0}Sh.sid=nx}}}
    Sh.move=S.T+60}
  const r=o.apply(this,arguments);try{audTick()}catch(e){console.error(e)}return r}}
function audTick(){if(NET.cl||!S)return;for(const P of allPilots()){if(!P||!P.aud)continue;const k=pkeyOf(P);
  for(const f in P.aud){const A=P.aud[f],L=leaderOf(f),Sh=L&&L.ship;if(!A||A.stage==='done')continue;
    if(!Sh||!Sh.alive||!Sh.aud||Sh.aud.pk!==k){A.stage='done';A.next=S.T+AUD.cool;audTell(P,`♛ ${lName(f)} won't be coming: the audience is off.`,'warn');continue}
    if(A.stage==='coming'&&Sh.sid===A.sid&&S.T>=A.eta){A.stage='here';A.until=S.T+AUD.open;Sh.aud.until=A.until;audTell(P,`♛ ${lName(f)} has docked at ${S.stations[A.sid].name}: your audience is open for ${Math.round(AUD.open/60)} minutes (Allegiance tab, docked there).`,'good')}
    else if(A.stage==='here'&&S.T>A.until){A.stage='done';A.next=S.T+AUD.cool;Sh.aud=null;audTell(P,`♛ ${lName(f)} leaves ${S.stations[A.sid].name}: the audience is over.`,'info')}}}
  if(S.deals0!==1)S.deals0=1}
function audTell(P,m,k){if(P===S.player)feed(m,k);else{const id=Object.keys(S.pilots||{}).find(x=>S.pilots[x]===P);if(id)netMsg(id,'feed',m,k)}}
// ---- asking
function audAsk(P,f,k,x){const A=audOf(P,f),R=AUD_REQ[k];if(!R)return'';if(!A||A.stage!=='here')return'No audience is open.';if(P.sector!==A.sid||P.docked!=='station')return`Dock at ${S.stations[A.sid].name} for the audience.`;
  A.cd=A.cd||{};if(A.cd[k]>S.T)return`${lName(f)} has already answered that: ask again in ${fmtT(A.cd[k]-S.T)}.`;if(R.only&&!R.only(P,f))return'There is no quarrel to end.';
  if(R.tgt&&!(x&&(x==='brood'&&k==='ally'||FAC_IDS.includes(x)&&x!==f)))return'Name the side.';if(standOf(f,P)<R.min)return`It takes ${standName(R.min)} standing or better with ${FACTIONS[f].short}.`;
  if(standOf(f,P)-R.cost<-100)return'You have no standing left to spend.';if(R.dur&&audDeal(P,f,k)&&!R.tgt)return'That agreement already holds.';
  if(k==='aid'&&!myStations(P).length)return'Aid goes to a Station of yours: you have none.';if(k==='def'&&!myStations(P).length)return'Joint defence guards a Station of yours: you have none.';
  const c=audChance(f,k,P,x);if(Math.random()>=c){A.cd[k]=S.T+AUD.refuse;return`✕ ${lName(f)} refuses${c<=0?': '+(leaderOf(f).traits.join(' and ').toLowerCase()||'unmoved')+', and not to be moved on this':''}. It costs you nothing.`}
  standAdd(f,-R.cost,`${R.n.toLowerCase()} granted`,P);A.cd[k]=S.T+AUD.refuse;const nm=P.decl?P.decl.name:'your faction';
  if(R.dur){P.deals=(P.deals||[]).filter(d=>!(d.f===f&&d.k===k));P.deals.push({f,k,x:x||null,until:S.T+R.dur})}
  if(k==='cease'){if(P.aggro)delete P.aggro[f];if(standOf(f,P)<STAND.dock)standAdd(f,STAND.dock-standOf(f,P)+1,'a ceasefire',P)}
  if(k==='pardon'){if(P.heat)P.heat[f]=0;if(P.aggro)delete P.aggro[f]}
  if(k==='ally'){if(isPow(x)){relAdd(f,x,-25,`at ${nm}'s request`);S.ai[f].focus={on:x,until:S.T+R.dur};S.ai[f].next=Math.min(S.ai[f].next,S.T+30)}P.allied=P.allied||{};P.allied[f]=1}
  if(k==='war'&&isPow(x)){const Pp=pairOf(f,x);if(Pp&&!Pp.war)evWar(f,x)}
  if(k==='aid'){const R2=myStations(P)[0],st=S.econ.stock[f]||{},give={};for(const[i,n]of[['plate',20],['wire',10],['coil',6]]){const g=inv.take(st,i,n);if(g)give[i]=g}inv.addAll(R2.stock,give);const t=Object.entries(give).map(([i,n])=>`${n} ${ITEMS[i].name}`).join(', ');
    chron(`${lName(f)} sends aid to ${nm}: ${t||'nothing to spare'}.`,'good',[f]);return`✓ ${lName(f)} agrees${t?`: ${t} delivered to ${R2.name}`:', but the warehouse is bare'}. −${R.cost} standing.`}
  chron(`${lName(f)} grants ${nm} ${R.tgt?`${R.n.toLowerCase()} ${x==='brood'?'the Brood':FACTIONS[x].name}`:`a ${R.n.toLowerCase()}`}.`,R.tgt?'big':'good',[f]);
  return`✓ ${lName(f)} grants it: ${R.n}${R.tgt?' '+(x==='brood'?'the Brood':FACTIONS[x].short):''}${R.dur?` for ${Math.round(R.dur/60)} minutes`:''}. −${R.cost} standing with ${FACTIONS[f].short}.`}
// ---- what the agreements do
{const o=pilotHostile;pilotHostile=function(P,x){P=P||S.player;if(P&&P.deals&&FAC_IDS.includes(x)&&(audDeal(P,x,'nap')||audDeal(P,x,'cease')))return false;return o.apply(this,arguments)}}
{const o=mBuy;mBuy=function(c,id){const v=o.apply(this,arguments);try{const f=c&&c.wallet;if(FAC_IDS.includes(f)&&audDeal(S.player,f,'trade'))return Math.max(1,Math.round(v*.9))}catch(e){}return v}}
{const o=mSell;mSell=function(c,id){const v=o.apply(this,arguments);try{const f=c&&c.wallet;if(FAC_IDS.includes(f)&&audDeal(S.player,f,'trade'))return Math.round(v*1.1)}catch(e){}return v}}
{const o=depTraders;depTraders=function(P){const L=o.apply(this,arguments);try{for(const d of audDeals(P,'tpact'))L.push(d.f)}catch(e){}return L}}
{const o=covered;covered=function(sid){if(o.apply(this,arguments))return true;try{for(const d of audDeals(S.player,'intel'))if(covOf(d.f,true).has(sid))return true}catch(e){}return false}}
{const o=hullRatingOK;hullRatingOK=function(P,k){if(o.apply(this,arguments))return true;try{const R=S.stations[P.sector];if(R&&FAC_IDS.includes(R.owner)&&audDeal(P,R.owner,'yard'))return ratingOf(P)+1>=(HULL_RATING[k]||1)}catch(e){}return false}}
// joint defence: a wing of theirs patrols your Station's system while it's live
{const o=worldUpdate;worldUpdate=function(dt){const r=o.apply(this,arguments);try{if(NET.cl||!S||!W)return r;const P=S.player;for(const d of audDeals(P,'def')){const R=myStations(P)[0];if(!R||W.sid!==R.sid)continue;d.sp=d.sp||{};if(d.sp[W.sid]&&W.ents.some(e=>e.jdef===d.f&&e.alive))continue;d.sp[W.sid]=1;
    for(let i=0;i<3;i++){const e=makeNPC('patrol',d.f,i?'striker':'heavy',3,{},R.sid);e.jdef=d.f;const a=i/3*TAU;e.x=(W.stationEnt?W.stationEnt.x:0)+Math.cos(a)*600;e.y=(W.stationEnt?W.stationEnt.y:0)+80;e.z=(W.stationEnt?W.stationEnt.z:0)+Math.sin(a)*600;W.ents.push(e)}
    feed(`♛ A ${FACTIONS[d.f].short} wing is guarding ${R.name}.`,'good')}}catch(e){}return r}}
// ---- the panel: the Allegiance tab, docked at a power's station
function audHtml(c,P){const R=S.stations[P.sector];if(!P.docked||P.docked!=='station'||!R||!FAC_IDS.includes(R.owner))return'';const f=R.owner,L=leaderOf(f),col=FACTIONS[f].col;
  let h=`<div class="ldbox" style="margin:0 0 18px;border-left:3px solid ${col}"><div class="lab">Audience</div><div class="ldname"><b style="color:${col}">${esc(L?`${L.title} ${L.name}`:FACTIONS[f].short)}</b></div>`;
  if(!audOn(P))return h+`<div class="note" style="margin:4px 0 0">Leaders grant audiences only to the heads of factions. Declare your own (Company → Holdings, with a Station of your own) to request one.</div></div>`;
  const A=audOf(P,f),st=standOf(f,P);h+=`<div class="note" style="margin:2px 0 10px">${L?esc(L.traits.join(', ')||'no known leanings'):''} · your standing ${standName(st)} (${st>0?'+':''}${Math.round(st)})</div>`;
  if(!A||A.stage==='done'){h+=`<div class="act" style="justify-content:flex-start"><button class="btn pri" type="button" data-act="audreq" data-arg="${f}">Request an audience</button></div>`;if(A&&S.T<A.next)h+=`<div class="note">Next audience possible in ${fmtT(A.next-S.T)}.</div>`;return h+audDealsHtml(P,f)+'</div>'}
  if(A.stage==='coming'){const sh=L.ship,hp=HOP[sh.sid]&&HOP[sh.sid][A.sid];return h+`<div class="note" style="margin:0">Requested at ${esc(S.stations[A.sid].name)}. The flagship is ${sh.sid===A.sid?'here, docking':`${hp} jump${hp===1?'':'s'} away, in ${esc(DEF[sh.sid].name)}`}: <b>about ${fmtT(Math.max(0,A.eta-S.T))}</b> until it docks.</div>`+audDealsHtml(P,f)+'</div>'}
  if(A.sid!==P.sector)return h+`<div class="note">Your audience is at ${esc(S.stations[A.sid].name)} for another ${fmtT(A.until-S.T)}.</div></div>`;
  h+=`<div class="note" style="margin:0 0 10px;color:#7ad9a7">${esc(lName(f))} receives you · ${fmtT(Math.max(0,A.until-S.T))} left. Each request is paid in standing; a refusal costs nothing.</div>`;
  for(const k in AUD_REQ){const Q=AUD_REQ[k];if(Q.only&&!Q.only(P,f))continue;const cd=A.cd&&A.cd[k]>S.T,lowSt=st<Q.min,held=Q.dur&&!Q.tgt&&audDeal(P,f,k);
    const tg=Q.tgt?(k==='ally'?[...FAC_IDS.filter(g=>g!==f),'brood']:FAC_IDS.filter(g=>g!==f)):[null];
    h+=`<div class="ldopt" style="align-items:flex-start"><span style="flex:1;min-width:0"><b>${esc(Q.n)}</b> <span class="mass" style="margin:0">−${Q.cost} standing${Q.dur?` · ${Math.round(Q.dur/60)} min`:''}${Q.min>-100?` · needs ${esc(standName(Q.min))}`:''}</span><br><span class="note" style="margin:0">${esc(Q.d)}</span></span><span class="act" style="flex-wrap:wrap;justify-content:flex-end">`;
    for(const x of tg){const ch=audChance(f,k,P,x),w=audWord(ch),dis=cd||lowSt||held||ch<=0;h+=`<button class="btn sm" type="button" data-act="audask" data-arg="${f}:${k}:${x||''}" ${dis?'disabled':''} title="${esc(w[0])}">${x?esc(x==='brood'?'Brood':FACTIONS[x].short):'Ask'} <span style="color:${w[1]};font-weight:400;text-transform:none;letter-spacing:0">· ${esc(w[0])}</span></button>`}
    h+=`</span></div>`}
  return h+audDealsHtml(P,f)+'</div>'}
function audDealsHtml(P,f){const L=(P.deals||[]).filter(d=>d.f===f&&S.T<d.until);if(!L.length)return'';return`<div class="lab" style="margin-top:12px">In force with ${esc(FACTIONS[f].short)}</div>`+L.map(d=>`<div class="coln"><span style="flex:1">${esc(AUD_REQ[d.k].n)}${d.x?' '+esc(d.x==='brood'?'the Brood':FACTIONS[d.x].short):''}</span><span class="mono">${fmtT(d.until-S.T)}</span></div>`).join('')}
{const o=allegianceHtml;allegianceHtml=function(P){P=P||S.player;let a='';try{const c=P.docked?dockCtx():null;a=c?audHtml(c,P):''}catch(e){console.error(e)}return a+o.apply(this,arguments)}}
{const o=dockAction;dockAction=function(act,arg){const P=S.player;if(act==='audreq'){dockErr=audRequest(P,String(arg));return}if(act==='audask'){const[f,k,x]=String(arg).split(':');dockErr=audAsk(P,f,k,x||null);return}return o.apply(this,arguments)}}
