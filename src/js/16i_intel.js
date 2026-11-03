//@src 16i_intel.js
// ============================================================ intel and claim work for contractors (Beyond stage 5)
// A contractor's scouting is sold to one power at a time: the power whose intel job it has selected, or the one it picked
// under "Intel work for" in the Jobs tab (Neutral standing or better). Beacon flips, limpets and anomaly finds go to that power
// and are paid from its treasury; a sworn pilot's always go to its faction.
// Claim Beacons can be bought for any power: at a power's station for that power, at a freeport for any power. A beacon claims
// for the power it was bought for, whoever carries it, and the power pays a claim fee. Powers post claim jobs for outposts they
// want taken, and intel jobs: beacon flips and limpets on enemy capital ships.
const FB={fee:400,stand:6,job:[1400,2600],flipStand:3,lpStand:3,maxJobs:3};
function intelFor(P){P=P||S.player;if(!P)return null;if(P.sworn)return P.sworn;const ok=f=>FAC_IDS.includes(f)&&standOf(f,P)>=STAND.dock;
  const j=P.job;if(j&&j.kind==='scout'&&ok(j.by))return j.by;return ok(P.intelFor)?P.intelFor:null}
for(const f of FAC_IDS){ITEMS['bc_'+f]={name:`Claim Beacon (${FACTIONS[f].short})`,recipe:{...ITEMS.beacon.recipe},col:FACTIONS[f].col,fb:f};ITEM_ORDER.push('bc_'+f)}
// the power a beacon in this pilot's hold would claim this outpost for (not its current owner)
function fbHeld(P,o){if(!P||!P.cargo)return null;for(const f of FAC_IDS)if((P.cargo['bc_'+f]||0)>0&&o.owner!==f)return f;return null}
// which powers' beacons this dock sells
function fbSold(c,P){if(!c||!c.wallet||c.kind!=='station'||S.unb)return[];if(c.owner==='neutral')return FAC_IDS.slice();if(FAC_IDS.includes(c.owner))return[c.owner];return[]}
function fbBuy(c,P,f){if(!fbSold(c,P).includes(f))return'Not sold here.';if(P.credits<CLAIM_PRICE)return'Not enough credits.';const rc=ITEMS.beacon.recipe,src=[c.market,S.econ.stock[c.wallet]].filter(Boolean);
  if(!haveIn(rc,src))return'The station has no plate and conduit to spare for a beacon right now.';takeFrom(rc,src);transfer('player',c.wallet,CLAIM_PRICE);const k='bc_'+f,room=W&&W.player&&W.player.st?W.player.st.cargo-invMass(P.cargo):0,toHold=room>=mass(k);
  inv.add(toHold?P.cargo:c.storage,k,1);return`✓ Bought a Claim Beacon for ${FACTIONS[f].short} for ${fmt(CLAIM_PRICE)} cr. It's in your ${toHold?'hold':String(c.storageName).toLowerCase()}. Carry it into an unclaimed or breached outpost's ring in a fighter or bomber and hold there to claim it for ${FACTIONS[f].short}.`}
function fbMarketHtml(c,P){const L=fbSold(c,P);if(!L.length)return'';const srcs=[P.cargo,c.storage];
  return`<div class="h3" style="margin-top:18px">Claim Beacons</div><p class="note" style="margin:0 0 8px">A beacon claims for the power it was bought for, whoever carries it: hold it in an unclaimed or breached outpost's ring in a fighter or bomber. That power pays you a ${fmt(FB.fee)} cr claim fee (more on a claim job) and your standing with it rises; the power that held the outpost takes it badly. ${mass('beacon')} t each.</p><div class="act" style="flex-wrap:wrap">${L.map(f=>`<button class="btn sm" type="button" data-act="buyfb" data-arg="${f}" ${P.credits>=CLAIM_PRICE?'':'disabled'}>Buy for ${esc(FACTIONS[f].short)} · ${fmt(CLAIM_PRICE)} cr${countIn('bc_'+f,srcs)?` · ${countIn('bc_'+f,srcs)} on hand`:''}</button>`).join('')}</div>`}
// a claim completed with a power's beacon (host and single player)
function claimJobPay(o,f,old){return old?FB.job[1]:FB.job[0]}
function fbClaim(o,f,by){const me=by==='me'||isMe(by),P=me?S.player:(S.pilots||{})[by];if(!P)return;const k='bc_'+f;inv.take(P.cargo,k,1);const v=invVec({[k]:1});for(const e of RAWS)o.fort[e]+=v[e];
  const old=o.owner,key=me?pkey():by,J=P.job&&P.job.id===`cl:${o.id}:${f}`;capture(o,f);let pay=FB.fee+(J?claimJobPay(o,f,old):0);const got=payKey(key,f,pay);
  standWork(P,f,FB.stand,'claimed an outpost');if(FAC_IDS.includes(old)&&old!==f)standAdd(old,-FB.stand,'you claimed its outpost',P);if(J)P.job=null;
  keyFeed(key,`⚑ You claimed ${o.name} for ${FACTIONS[f].short}: +${fmt(got)} cr${J?' (claim job)':' claim fee'}.`,'good')}
// outposts a power wants claimed: unclaimed ones, and ones held by a power it is at war with, within four jumps, not under a station's lock
function claimTargets(f,P){const out=[];for(const id in S.outposts){const o=S.outposts[id];if(!o||o.owner===f||o.owner==='player'||o.owner==='brood')continue;if(o.owner&&!(FAC_IDS.includes(o.owner)&&warWith(f,o.owner))&&o.owner!=='pirate')continue;
    if(outLock(o.sector))continue;const h=HOP[P.sector]&&HOP[P.sector][o.sector];if(h==null||h>4)continue;out.push({o,h})}return out.sort((a,b)=>a.h-b.h).slice(0,FB.maxJobs)}
// enemy capital ships a power will pay a limpet on
function lpTargets(f,P){return(S.frigates||[]).filter(t=>t.side!=='brood'&&hostile(f,t.side)&&t.side!=='neutral'&&!capPinged(t,f)&&HOP[P.sector]&&HOP[P.sector][t.sector]!=null&&HOP[P.sector][t.sector]<=3).slice(0,2)}
JOB_OPEN.push('cl','lpj');
{const o=jobsList;jobsList=function(c,P,srcs){const out=o.apply(this,arguments);if(S.unb||S.training)return out;try{const hop=sid=>HOP[P.sector]&&HOP[P.sector][sid]!=null?HOP[P.sector][sid]:0,far=n=>n?`${n} jump${n>1?'s':''}`:'here',scout=isScoutCls(P.cls);
  for(const f of jobIssuers(c,P)){const sh=FACTIONS[f].short;
    for(const{o:op,h}of claimTargets(f,P)){const pay=claimJobPay(op,f,op.owner)+FB.fee,have=countIn('bc_'+f,[P.cargo,c.storage]);
      out.push({id:`cl:${op.id}:${f}`,by:f,sid:op.sector,ty:'fight',title:`Claim ${esc(op.name)} for ${esc(sh)}`,sub:`${op.owner?`held by ${esc(sideName(op.owner))} · break its defenses first`:'unclaimed'} · ${esc(DEF[op.sector].name)}${have?` · beacon on hand`:''}`,hops:h,where:far(h),payN:pay,pay:`${fmt(pay)} cr`,
        need:beaconCls(P.cls)?'':'Needs a fighter or bomber to carry the beacon',btn:h?['croute',op.sector,'Set course']:null,btn2:!have&&fbSold(c,P).includes(f)?['buyfb',f,`Buy a ${sh} beacon · ${fmt(CLAIM_PRICE)} cr`]:null,
        detail:()=>`<p class="note" style="margin:0">${esc(sh)} wants ${esc(op.name)}. Carry a Claim Beacon bought for ${esc(sh)} into its ring and hold there${op.owner?' once its defenses are down (break them, or come when they are)':''}. ${esc(sh)} pays on the claim, and your standing with it rises.${op.owner?` ${esc(sideName(op.owner))} will take it badly.`:''}</p>`})}
    for(const x of(S.bcnMis&&S.bcnMis[f]||[]).filter(x=>S.T<x.until&&!P.sworn)){const B=S.beacons[x.sid],j=hop(x.sid);
      out.push({id:'bm:'+x.id,by:f,sid:x.sid,ty:'scout',title:`Beacon: ${esc(DEF[x.sid].name)} for ${esc(sh)}`,sub:`${B&&B.owner?`held by ${esc(FAC(B.owner).short)}`:'unclaimed'} · ${Math.max(0,Math.round((x.until-S.T)/60))} min left`,hops:j,where:far(j),payN:x.reward,pay:`+${fmt(x.reward)} cr`,need:scout?'':'Needs a Scout or Advanced Scout',btn:x.sid===P.sector?null:['croute',x.sid,'Set course'],
        detail:()=>`<p class="note" style="margin:0">Flip this system's beacon to ${esc(sh)}: hold within ${BCN_R} m of it for ${BCN_T} s in a scout. ${esc(sh)} pays this bounty on top of the ${BCN_FLIP} cr flip bonus and ${BCN_RES} cr a minute while it holds the beacon. Selecting this job makes your intel work go to ${esc(sh)}.</p>`})}
    if(!P.sworn)for(const t of lpTargets(f,P)){const j=hop(t.sector),pay=PING_PAY[t.cls]||300;
      out.push({id:`lpj:${t.id}:${f}`,by:f,sid:t.sector,ty:'scout',title:`Limpet: ${esc(sideName(t.side))} ${esc(capName(t))} ${esc(t.name)}`,sub:`for ${esc(sh)} · now in ${esc(DEF[t.sector].name)}`,hops:j,where:far(j),payN:pay,pay:`${fmt(pay)} cr if destroyed`,need:scout?'':'Needs a Scout or Advanced Scout',btn:j?['croute',t.sector,'Set course']:null,
        detail:()=>`<p class="note" style="margin:0">Plant a limpet on this capital ship (hold F within ${LIMPET_R} m in a scout). ${esc(sh)}'s weapons hit it ${Math.round((LIMPET_DMG-1)*100)}% harder for ${LIMPET_LIFE/60} minutes and its maps track it; if it's destroyed with the limpet on, ${esc(sh)} pays you ${fmt(pay)} cr. Selecting this job makes your intel work go to ${esc(sh)}.</p>`})}}}catch(err){console.error(err)}return out}}
{const o=jobLive;jobLive=function(T){if(!T)return false;const pre=jobPre(T.id),p=String(T.id).split(':');
  if(pre==='cl'){const op=S.outposts[p[1]];return!!op&&op.owner!==p[2]}if(pre==='lpj'){const t=(S.frigates||[]).find(x=>String(x.id)===p[1]);if(t)T.sid=t.sector;return!!t}
  if(pre==='bm'&&!S.player.sworn){const f=S.player.job&&S.player.job.by;return(S.bcnMis&&S.bcnMis[f]||[]).some(x=>String(x.id)===p[1]&&S.T<x.until)}return o.apply(this,arguments)}}
// "Intel work for": a contractor picks the power its scouting goes to (above the jobs list)
function intelBarHtml(c,P){if(P.sworn||S.unb||S.training)return'';const cur=intelFor(P);
  return`<div class="note" style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin:0 0 10px">Intel work for <b>${cur?esc(FACTIONS[cur].short):'nobody'}</b>:${FAC_IDS.map(f=>`<button class="btn sm" type="button" data-act="intelfor" data-arg="${f}" aria-pressed="${P.intelFor===f}" ${standOf(f,P)>=STAND.dock?'':'disabled'}>${esc(FACTIONS[f].short)}</button>`).join('')}<span>Beacon flips, limpets and anomaly scans go to this power and are paid by it. An intel job you select overrides it.</span></div>`}
{const o=jobsHtml;jobsHtml=function(c,P){return intelBarHtml(c,P)+o.apply(this,arguments)}}
{const o=dockAction;dockAction=function(act,arg){if(act==='buyfb'||act==='intelfor'){const c=dockCtx(),P=S.player;
    if(act==='buyfb')dockErr=fbBuy(c,P,arg);else{if(FAC_IDS.includes(arg)&&standOf(arg,P)>=STAND.dock){P.intelFor=arg;dockErr=`✓ Your intel work now goes to ${FACTIONS[arg].short}.`}else dockErr='Your standing is too low for that.'}return}return o.apply(this,arguments)}}
// standing for intel work: a beacon flipped for a power raises it (and lowers the power it was taken from); so does a limpet
{const o=beaconFlip;beaconFlip=function(sid,side,by){const B=S.beacons&&S.beacons[sid],old=B&&B.owner;const r=o.apply(this,arguments);try{const P=by?xPilotOfKey(by):null;if(P&&!P.sworn&&FAC_IDS.includes(side)){standWork(P,side,FB.flipStand,'beacon flip');if(FAC_IDS.includes(old)&&old!==side)standAdd(old,-FB.flipStand,'you flipped its beacon',P)}}catch(err){}return r}}
{const o=limpetPlant;limpetPlant=function(E,f,by){const r=o.apply(this,arguments);try{if(r!==false&&by){const P=xPilotOfKey(by);if(P&&!P.sworn)standWork(P,f,FB.lpStand,'limpet')}}catch(err){}return r}}
// discoveries: any hull with a scanner fitted picks up anomalies, not only scouts
{const o=scoutSees;scoutSees=function(P){if(o.apply(this,arguments))return true;return!!P&&!P.docked&&loadOn()&&fitHas(P,'scanner')}}
