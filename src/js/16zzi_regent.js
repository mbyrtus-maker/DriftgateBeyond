//@src 16zzi_regent.js
// ============================================================ sleep mode: a stand-in leader for your own faction (Beyond, 4 Nov 2026)
// The user's ask: when the player is asleep, their faction still reacts. They appoint a leader with two traits (Allegiance tab);
// it holds the faction while they're away and resigns when they come back. It takes over four ways: the Sleep button, after
// 15 minutes idle, when a faction-leading guest leaves a multiplayer game, and while the game is closed (the galaxy catches up
// on up to 12 hours when it's reopened). It answers the powers, makes its own diplomacy, defends your holdings and runs the
// economy, each leaning on its traits, never spending below the reserve you set. Coming back, you get its report.
// (user, 4 Nov 2026) for now the galaxy pauses while no player is connected: a closed game doesn't catch up (catchUp off; the
// catch-up code stays, to revisit later)
const RG={catchUp:false,idle:15*60,cap:12*3600,minAway:120,diplo:300,econ:120,askCool:900,calm:120,logMax:80,
  names:['Ada Merrow','Cassius Vane','Imre Holt','Juno Castell','Lio Brandt','Mira Solenne','Oren Tasker','Petra Quill','Rhys Calder','Sela Wyn']};
const RG_TXT={Ambitious:'presses a friendly power to war on a weak neighbour',Vengeful:'goes after whoever hurt you most; refuses tribute',
  Mercantile:'pays tribute when cheaper than a fight; seeks trade pacts; sells surplus ore',Cautious:'pays tribute; asks for ceasefires early; pulls crews home from any fight',
  Scheming:'trades for shared intel',Patient:'pays tribute; seeks non-aggression pacts',Wary:'turns down alliances; pulls crews home from any fight',
  Loyal:'stands with its allies against their enemies',Zealous:'refuses tribute; strikes back at an attacker',Honourable:'refuses tribute; keeps every pact',
  Ruthless:'refuses tribute; strikes back; presses for wars',Industrious:'adds Station buildings when the stores allow; seeks trade pacts',
  Isolationist:'turns down alliances; seeks non-aggression pacts, never wars',Opportunist:'presses for wars on the weak; joins winning sides'};
function rgOn(P){return!!(P&&P.decl&&!P.sworn&&!S.unb&&!S.training)}
function rgHas(P,t){return!!(P&&P.regent&&P.regent.traits.includes(t))}
function rgName(P){return(P&&P.regent&&P.regent.name)||'Your stand-in'}
function rgSet(P,arg){if(!rgOn(P))return'A stand-in leads a declared faction: declare yours first.';const[n0,t1,t2,res,idle]=String(arg).split('|');
  const name=String(n0||'').replace(/[<>]/g,'').trim().slice(0,28)||pick(RG.names);if(!TRAITS.includes(t1)||!TRAITS.includes(t2)||t1===t2)return'Pick two different traits.';
  P.regent={name,traits:[t1,t2],reserve:clamp(+res||0,0,.9),idle:idle!=='0'};return`✓ ${name} (${t1}, ${t2}) will hold ${P.decl.name} while you're away.`}
function rgCount(P){return myStations(P).length}
function rgLog(P,msg,kind){const A=P.asleep;if(!A)return;A.log.push({T:S.T,msg,kind:kind||'info'});if(A.log.length>RG.logMax)A.log.shift()}
function rgSleep(P,by){if(!rgOn(P))return'Sleep mode needs a declared faction.';if(!P.regent)return'Appoint a stand-in first (name and two traits).';if(P.asleep)return'';
  P.asleep={by:by||'button',T0:S.T,cr0:P.credits,floor:Math.round(P.credits*P.regent.reserve),sys0:rgCount(P),log:[],hp:{},hit:{},hurt:{},ask:{},next:{d:S.T+20,e:S.T+30},crew0:{}};
  for(const R of myDepots(P))P.asleep.crew0[R.sid]=(R.crew||[]).map(c=>c.cls);
  rgLog(P,`${rgName(P)} takes charge of ${P.decl.name}${by==='idle'?' (you were idle)':by==='away'?' (you left the galaxy)':by==='closed'?' (the game was closed)':''}.`,'good');
  chron(`${rgName(P)} holds ${P.decl.name} for ${P.name||'its founder'}.`,'news',[]);return`✓ ${rgName(P)} holds ${P.decl.name}. Sleep well.`}
function rgWake(P){const A=P.asleep;if(!A)return'';const dur=S.T-A.T0,c1=P.credits,s1=rgCount(P);
  // crews back to the work they were doing
  for(const R of myDepots(P))for(const c of R.crew||[])if(c.rgJob){if(c.job==='guard')c.job=c.rgJob;delete c.rgJob}
  P.rgRep={name:rgName(P),traits:P.regent?P.regent.traits.slice():[],by:A.by,T0:A.T0,T1:S.T,dur,cr0:A.cr0,cr1:c1,sys0:A.sys0,sys1:s1,log:A.log.slice(),seen:0};
  P.asleep=null;chron(`${P.rgRep.name} hands ${P.decl?P.decl.name:'the faction'} back to ${P.name||'its founder'}.`,'news',[]);
  return`✓ ${P.rgRep.name} hands ${P.decl?P.decl.name:'your faction'} back to you after ${rgDur(dur)}.`}
function rgDur(t){t=Math.max(0,Math.round(t));const h=Math.floor(t/3600),m=Math.floor(t%3600/60);return h?`${h} h ${m} min`:m?`${m} min`:`${t} s`}
function rgSpend(P,n){const A=P.asleep;return!!A&&P.credits-n>=A.floor}
// a request made by envoy (the stand-in doesn't fly to an audience): the leader's answer and the price are the audience's
function rgAsk(P,f,k,x){const A=P.asleep,key=f+':'+k+':'+(x||'');if(!A||(A.ask[key]||0)>S.T)return'';A.ask[key]=S.T+RG.askCool;
  P.aud=P.aud||{};const a0=P.aud[f],dk=P.docked,cd=(P.rgCd=P.rgCd||{})[f]||{};let m='';
  P.aud[f]={stage:'here',sid:P.sector,cd,T:S.T,until:S.T+60};P.docked='station';
  try{m=audAsk(P,f,k,x)}catch(e){console.error(e)}finally{P.rgCd[f]=P.aud[f].cd||cd;if(a0)P.aud[f]=a0;else delete P.aud[f];P.docked=dk}
  if(/^[✓✕]/.test(m))rgLog(P,`Envoy to ${FACTIONS[f].short}, asking for ${AUD_REQ[k].n.toLowerCase()}${x?' '+(x==='brood'?'the Brood':FACTIONS[x].short):''}: ${m.replace(/^[✓✕]\s*/,'')}`,m[0]==='✓'?'good':'warn');return m}
// ---- the stand-in's turn (host and single player)
function rgTick(P){const A=P.asleep;if(!A||!rgOn(P)||!P.regent){if(A&&!rgOn(P)){rgLog(P,`✕ ${P.decl?P.decl.name:'Your faction'} lost its last Station and fell back into a company: ${rgName(P)} resigns.`,'bad');rgWake(P)}return}
  {const now=myDepots(P).map(R=>R.sid);for(const sid of A.have||now)if(!now.includes(sid))rgLog(P,`✕ ${DEF[sid].name}: your ${A.haveN&&A.haveN[sid]||'base'} was lost.`,'bad');A.have=now;A.haveN=Object.fromEntries(myDepots(P).map(R=>[R.sid,R.pst?'Station':'Depot']))}
  rgPowers(P);rgDefend(P);if(S.T>=A.next.d){A.next.d=S.T+RG.diplo;rgDiplo(P)}if(S.T>=A.next.e){A.next.e=S.T+RG.econ;rgEcon(P)}}
function rgPowers(P){for(const x of(P.props||[]).slice()){const f=x.f;let yes;
  if(x.k==='ally')yes=!rgHas(P,'Isolationist')&&!rgHas(P,'Wary')&&!(rgHas(P,'Vengeful')&&(P.asleep.hurt[f]||0)>0);
  else if(x.k==='demand')yes=(rgHas(P,'Cautious')||rgHas(P,'Patient')||rgHas(P,'Mercantile'))&&!['Vengeful','Zealous','Ruthless','Honourable'].some(t=>rgHas(P,t))&&rgSpend(P,x.amt||0);else continue;
  const m=propAnswer(P,x.id,yes);rgLog(P,`${FACTIONS[f].short}'s ${x.k==='ally'?'alliance offer':`demand for ${fmt(x.amt||0)} cr tribute`}: ${yes?(x.k==='ally'?'accepted':'paid'):(x.k==='ally'?'declined':'refused')}. ${m.replace(/^✓\s*/,'')}`,yes?'good':'warn')}}
function rgHitBy(R){const d=(S.distress||[]).find(x=>x.sid===R.sid&&x.T2>S.T-60&&x.fac==='player');return d?d.by||'unknown':null}
function rgDefend(P){const A=P.asleep,hit=[];
  for(const R of myDepots(P)){const h0=A.hp[R.sid];A.hp[R.sid]=R.hull;const by=rgHitBy(R);if(by||(h0!=null&&R.hull<h0-Math.max(1,(R.hMax||1000)*.005))){hit.push(R);const who=by&&by!=='unknown'?by:A.hit[R.sid]&&A.hit[R.sid].by||null;
    if(who&&FAC_IDS.includes(who))A.hurt[who]=(A.hurt[who]||0)+1;
    const first=!A.hit[R.sid]||S.T-A.hit[R.sid].last>RG.calm;A.hit[R.sid]={by:who,last:S.T,since:first?S.T:A.hit[R.sid].since};
    if(first){rgLog(P,`⚠ ${R.name} is under attack${who?` by ${who==='brood'?'the Brood':who==='pirate'?'the Unbound':FACTIONS[who]?FACTIONS[who].short:who}`:''}. ${rgRally(P,R)}`,'bad');
      for(const f of FAC_IDS)if((P.allied&&P.allied[f])||standOf(f,P)>=AUD_REQ.def.min)if(rgAsk(P,f,'def'))break}}}
  // calm again: crews back to work; a Zealous or Ruthless stand-in strikes back at the attacker
  for(const sid in A.hit){const H=A.hit[sid];if(S.T-H.last<RG.calm||H.done)continue;H.done=1;const R=S.stations[sid];if(!R)continue;
    if(!(rgHas(P,'Wary')||rgHas(P,'Cautious')))for(const c of R.crew||[])if(c.rgJob){if(c.job==='guard')c.job=c.rgJob;delete c.rgJob}
    rgLog(P,`${R.name} holds: the attack is over.`,'good');
    if((rgHas(P,'Zealous')||rgHas(P,'Ruthless'))&&H.by&&FAC_IDS.includes(H.by)){const tg=Object.values(S.stations).filter(x=>x&&x.owner===H.by&&HOP[sid]&&HOP[sid][x.sid]!=null).sort((a,b)=>HOP[sid][a.sid]-HOP[sid][b.sid])[0];
      const caps=rgCaps(P);if(tg&&caps.length){for(const t of caps)zmOrder(P,'patrol',`${t.id}:${tg.sid}`);rgLog(P,`Strikes back: ${caps.map(t=>t.name).join(', ')} sent against ${FACTIONS[H.by].short} at ${tg.name}.`,'warn')}}}
  if(hit.length&&(rgHas(P,'Wary')||rgHas(P,'Cautious')))for(const R of myDepots(P))for(const c of R.crew||[])if(c.job!=='guard'&&c.job!=='run'){c.rgJob=c.job;c.job='guard'}
  return hit}
function rgCaps(P){const k=pkeyOf(P);return(S.frigates||[]).filter(t=>t.owner===k||(!NET.on&&t.side==='player'&&!t.owner))}
function rgRally(P,R){const out=[];const cr=(R.crew||[]).filter(c=>c.job!=='guard'&&c.job!=='run');for(const c of cr){c.rgJob=c.job;c.job='guard'}if(cr.length)out.push(`${cr.length} crew${cr.length>1?'s':''} called home to guard it`);
  const caps=rgCaps(P);for(const t of caps)zmOrder(P,'patrol',`${t.id}:${R.sid}`);if(caps.length)out.push(`${caps.map(t=>t.name).join(', ')} sent to defend it`);
  return out.length?out.join('; ')+'.':'Nothing of yours is near enough to help.'}
function rgDiplo(P){const A=P.asleep,hurt=Object.keys(A.hurt).filter(f=>A.hurt[f]>0).sort((a,b)=>A.hurt[b]-A.hurt[a]),iso=rgHas(P,'Isolationist');
  // ceasefire with whoever is fighting you (a careful stand-in asks at once; others when a system has been lost)
  const losing=rgCount(P)<A.sys0;for(const f of FAC_IDS){const at=(P.aggro&&P.aggro[f]>S.T)||standOf(f,P)<STAND.dock;if(!at)continue;if(hurt.includes(f)&&(losing||rgHas(P,'Cautious')||rgHas(P,'Patient')||iso)&&!(rgHas(P,'Vengeful')&&hurt[0]===f))rgAsk(P,f,'cease')}
  if(rgHas(P,'Cautious')||rgHas(P,'Patient')||iso||rgHas(P,'Honourable'))for(const f of FAC_IDS){const s=standOf(f,P);if(s>=-40&&s<10&&!audDeal(P,f,'nap')&&!(rgHas(P,'Vengeful')&&hurt[0]===f)){rgAsk(P,f,'nap');break}}
  if(!iso&&(rgHas(P,'Mercantile')||rgHas(P,'Industrious')))for(const f of FAC_IDS)if(standOf(f,P)>=0&&!audDeal(P,f,'tpact')){rgAsk(P,f,'tpact');break}
  if(rgHas(P,'Scheming'))for(const f of FAC_IDS)if(standOf(f,P)>=0&&!audDeal(P,f,'intel')){rgAsk(P,f,'intel');break}
  if(!iso&&rgHas(P,'Loyal'))for(const f of Object.keys(P.allied||{}))for(const x of FAC_IDS)if(x!==f&&warWith(f,x)&&!audDeal(P,f,'ally')){rgAsk(P,f,'ally',x);break}
  // war: on whoever hurt you (Vengeful), or a weak neighbour holding systems next to yours (Ambitious, Opportunist, Ruthless)
  if(!iso&&['Ambitious','Opportunist','Ruthless','Vengeful'].some(t=>rgHas(P,t))){let x=rgHas(P,'Vengeful')&&hurt[0]?hurt[0]:null;
    if(!x&&['Ambitious','Opportunist','Ruthless'].some(t=>rgHas(P,t))){const mine=new Set(myStations(P).map(R=>R.sid)),cnt=controlCounts();
      const nb=FAC_IDS.filter(f=>Object.values(S.stations).some(R=>R&&R.owner===f&&[...mine].some(s=>(NEIGH[s]||[]).includes(R.sid))));x=nb.sort((a,b)=>(cnt[a]||0)-(cnt[b]||0))[0]||null}
    if(x)for(const f of FAC_IDS.filter(g=>g!==x&&standOf(g,P)>=AUD_REQ.war.min&&!warWith(g,x)).sort((a,b)=>standOf(b,P)-standOf(a,P))){if(rgAsk(P,f,'war',x))break}}}
function rgEcon(P){const A=P.asleep,order=['hangar','defence','storage','forge','market','yard'].filter(k=>STA.B[k]);
  for(const R of myDepots(P)){R.buy=R.buy||{};R.sell=R.sell||{};
    // laid-up crews need Alloy Plate for running costs: put in a standing order for it
    if((R.crew||[]).some(c=>c.laid)&&!(R.buy.plate>0)){R.buy.plate=20;rgLog(P,`${R.name}: crews laid up for want of Alloy Plate; a buy order for 20 is posted.`,'info')}
    // crews lost (wages unpaid or ships destroyed) are hired again when the money is there
    const was=(A.crew0[R.sid]||[]).slice(),now=(R.crew||[]).map(c=>c.cls);for(const c of now){const i=was.indexOf(c);if(i>=0)was.splice(i,1)}
    for(const cls of was){const pr=Math.max(800,hullPrice(cls));if(!rgSpend(P,pr))break;const m=crewHire(R,P,cls);if(String(m).startsWith('✓')){rgLog(P,`${R.name}: hired a new ${CLASSES[cls].name} crew (${fmt(pr)} cr).`,'info');A.crew0[R.sid]=(R.crew||[]).map(c=>c.cls)}else break}
    if(rgHas(P,'Mercantile'))for(const k of RAWS.filter(e=>ITEMS[e]))if((R.stock[k]||0)>150&&R.sell[k]==null&&R.buy[k]==null){R.sell[k]=100;rgLog(P,`${R.name}: selling surplus ${ITEMS[k].name} (keeping 100).`,'info')}
    if(rgHas(P,'Industrious')&&R.pst&&(R.bld||[]).length<5){const k=order.find(b=>!hasB(R,b));if(k&&haveIn(STA.bcost,[R.stock])){const m=staBuild(P,R,k);if(String(m).startsWith('✓'))rgLog(P,`${R.name}: ${m.replace(/^✓\s*/,'')}`,'good')}}}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{if(!NET.cl&&S&&!S.training&&!S.unb)for(const P of allPilots()){if(!P||!P.asleep)continue;const pid=P===S.player?null:pkeyOf(P);
    if(pid&&P.asleep.by==='away'&&Object.values(MP.cl||{}).some(c=>c.pid===pid&&c.ready)){rgWake(P);continue}runAs(pid,()=>rgTick(P))}}catch(e){console.error(e)}return r}}
// a guest's faction proposals and its fall come from the same tick as the host's (they used to reach the host's faction only)
{const o=declTick;declTick=function(){const r=o.apply(this,arguments);try{if(NET.host&&S.pilots)for(const pid in S.pilots){const P=S.pilots[pid];if(!P||P===S.player||!P.decl||P.off&&!P.asleep)continue;
    const keep=S.propT;S.propT=P.propT=P.propT||{};try{runAs(pid,()=>o.apply(this,arguments))}finally{S.propT=keep}}}catch(e){console.error(e)}return r}}
// ---- a faction-leading guest leaves: its stand-in holds the faction, its ship berthed at its Station
{const o=pilotLeft;pilotLeft=function(c){const P=S.pilots&&S.pilots[c.pid];const r=o.apply(this,arguments);try{if(P&&rgOn(P)&&P.regent&&!P.asleep){const R=myStations(P)[0];if(R){P.sector=R.sid;P.docked='station';P.x=P.y=P.z=0;P.vx=P.vy=P.vz=0}runAs(c.pid,()=>rgSleep(P,'away'))}}catch(e){console.error(e)}return r}}
// ---- the Allegiance panel: appointing the stand-in, Sleep, and the last report
function rgHtml(P){if(!rgOn(P))return'';const G=P.regent||{name:'',traits:['Cautious','Industrious'],reserve:.5,idle:true},opt=v=>TRAITS.map(t=>`<option value="${t}"${t===v?' selected':''}>${t}</option>`).join('');
  let h=`<div class="ldbox" id="rgBox" style="margin:14px 0;border-left:3px solid var(--amber)"><div class="lab">Stand-in leader (sleep mode)</div>
    <p class="note" style="margin:4px 0 8px">While you're away, your stand-in holds ${esc(P.decl.name)}: it answers the powers, makes its own diplomacy, defends your holdings and runs the economy as its traits lean, and never spends below your reserve. It takes over when you press Sleep, after ${RG.idle/60} minutes idle (if you allow it), ${RG.catchUp?`when you leave a multiplayer game, and while the game is closed (the galaxy catches up on up to ${RG.cap/3600} hours when you return)`:'or when you leave a multiplayer game'}. ${RG.catchUp?'':'While nobody is playing, the galaxy waits.'} When you come back it resigns and reports.</p>
    <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:flex-end"><label class="mass" style="margin:0">Name<br><input id="rgName" class="ydsel" style="width:170px" maxlength="28" value="${esc(G.name||'')}" placeholder="${esc(RG.names[0])}"></label>
    <label class="mass" style="margin:0">Trait<br><select id="rgT1" class="ydsel">${opt(G.traits[0])}</select></label><label class="mass" style="margin:0">Trait<br><select id="rgT2" class="ydsel">${opt(G.traits[1])}</select></label>
    <label class="mass" style="margin:0">Reserve<br><select id="rgRes" class="ydsel">${[0,.25,.5,.75,.9].map(v=>`<option value="${v}"${Math.abs(v-G.reserve)<.01?' selected':''}>${Math.round(v*100)}% of credits</option>`).join('')}</select></label>
    <label class="mass" style="margin:0 0 6px"><input type="checkbox" id="rgIdle"${G.idle!==false?' checked':''}> take over when I'm idle</label></div>
    <p class="note" id="rgTx" style="margin:6px 0 8px">${esc(G.traits[0])}: ${esc(RG_TXT[G.traits[0]]||'')}. ${esc(G.traits[1])}: ${esc(RG_TXT[G.traits[1]]||'')}.</p>
    <div class="act" style="justify-content:flex-start;gap:8px"><button class="btn${P.regent?'':' pri'}" type="button" data-rg="set">${P.regent?'Update the appointment':'Appoint'}</button><button class="btn${P.regent?' pri':''}" type="button" data-rg="sleep" ${P.regent?'':'disabled'}>Hand over to ${esc(rgName(P))} and sleep</button></div></div>`;
  if(P.rgRep)h+=rgRepHtml(P.rgRep,true);return h}
function rgRepHtml(R,box){const d=R.cr1-R.cr0,ls=(R.log||[]).map(x=>`<li style="margin:2px 0;color:${x.kind==='bad'?'var(--danger)':x.kind==='warn'?'#ff9a4a':x.kind==='good'?'#9fd8a8':'var(--text)'}">${esc(x.msg)}</li>`).join('');
  return`<div class="ldbox"${box?' style="margin:0 0 14px"':''}><div class="lab">${esc(R.name)}'s report</div><div class="note" style="margin:2px 0 6px">${esc(R.name)} (${esc((R.traits||[]).join(', '))}) held your faction for ${rgDur(R.dur)}${R.by==='closed'?' while the game was closed':R.by==='away'?' while you were out of the galaxy':R.by==='idle'?' while you were idle':''}. Credits ${d>=0?'+':'−'}${fmt(Math.abs(Math.round(d)))} · Stations ${R.sys0} → ${R.sys1}.</div><ul style="margin:0;padding-left:18px;max-height:260px;overflow:auto">${ls||'<li>A quiet watch: nothing needed deciding.</li>'}</ul>${box?`<div class="act" style="justify-content:flex-start;margin-top:6px"><button class="btn sm" type="button" data-rg="dis">Dismiss the report</button></div>`:''}</div>`}
{const o=allegianceHtml;allegianceHtml=function(P){P=P||S.player;const h=o.apply(this,arguments);try{if(rgOn(P))return h+rgHtml(P)}catch(e){console.error(e)}return h}}
for(const k of['rgset','rgsleep','rgwake','rgdis'])CO_REMOTE.add(k);
{const o=dockAction;dockAction=function(act,arg){const P=S.player;if(act==='rgset'){dockErr=rgSet(P,arg);return}if(act==='rgsleep'){dockErr=rgSleep(P,arg==='idle'?'idle':'button');return}
  if(act==='rgwake'){dockErr=rgWake(P);return}if(act==='rgdis'){if(P.rgRep)P.rgRep=null;dockErr='';return}return o.apply(this,arguments)}}
function rgAct(act,arg){if(NET.cl){netSend({t:'act',act:'rg'+act,arg:String(arg||'')});return'Working…'}dockErr='';dockAction('rg'+act,arg);return dockErr}
function rgRerender(m){try{if($('company')&&!$('company').hidden){coErr=m||'';renderCompany()}else if(!$('dock').hidden){dockErr=m||'';renderDock()}}catch(e){}}
document.addEventListener('change',e=>{const t=e.target;if(!t||(t.id!=='rgT1'&&t.id!=='rgT2'))return;const a=$('rgT1').value,b=$('rgT2').value,tx=$('rgTx');if(tx)tx.textContent=`${a}: ${RG_TXT[a]}. ${b}: ${RG_TXT[b]}.`});
document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('[data-rg]');if(!b||b.disabled)return;e.stopPropagation();const k=b.dataset.rg;let m='';
  if(k==='set')m=rgAct('set',[($('rgName')||{}).value||'',$('rgT1').value,$('rgT2').value,$('rgRes').value,$('rgIdle').checked?1:0].map(v=>String(v).replace(/\|/g,'/')).join('|'));
  else if(k==='sleep'){m=rgAct('sleep','button');rgShown=performance.now()}else if(k==='dis')m=rgAct('dis','');rgRerender(m)},true);
// ---- the screen while you sleep, waking, and the report
let rgIn=performance.now(),rgShown=0,rgWas=false,rgCU=null,rgLastRep=null;
for(const ev of['keydown','mousedown','mousemove','wheel','touchstart'])addEventListener(ev,e=>{rgIn=performance.now();const P=S&&S.player;
  if(ev!=='mousemove'&&P&&P.asleep&&!rgCU&&performance.now()-rgShown>600){e.preventDefault();e.stopPropagation();rgShown=performance.now();const m=rgAct('wake','');if(!NET.cl)rgRerender(m)}},true);
function rgOv(){let el=$('rgOv');if(!el){el=document.createElement('div');el.id='rgOv';el.setAttribute('role','dialog');el.setAttribute('aria-live','polite');
    el.style.cssText='position:fixed;inset:0;z-index:60;background:rgba(4,7,11,.86);display:flex;align-items:center;justify-content:center;padding:16px;font:14px/1.45 system-ui,sans-serif;color:#ece4cf';
    el.innerHTML='<div style="max-width:560px;width:100%;background:rgba(18,22,28,.94);border:1px solid rgba(240,178,74,.35);border-radius:10px;padding:18px 20px"><div id="rgOvT" style="font-size:20px;font-weight:700;color:#f0b24a"></div><div id="rgOvS" style="opacity:.75;margin:2px 0 10px"></div><div id="rgOvP"></div><ul id="rgOvL" style="margin:0;padding-left:18px;max-height:46vh;overflow:auto"></ul><div id="rgOvH" style="opacity:.6;margin-top:12px;font-size:12px"></div></div>';document.body.appendChild(el)}return el}
function rgShowReport(R){let el=$('rgRepPop');if(!el){el=document.createElement('div');el.id='rgRepPop';el.setAttribute('role','dialog');el.style.cssText='position:fixed;inset:0;z-index:61;background:rgba(4,7,11,.7);display:flex;align-items:center;justify-content:center;padding:16px';document.body.appendChild(el)}
  el.innerHTML=`<div style="max-width:600px;width:100%;background:var(--panel,#12161c);border:1px solid rgba(240,178,74,.4);border-radius:10px;padding:16px 18px;color:var(--text,#ece4cf)">${rgRepHtml(R,false)}<div class="act" style="justify-content:flex-end;margin-top:10px"><button class="btn pri" type="button" id="rgRepOk">Back to it</button></div></div>`;el.hidden=false;
  $('rgRepOk').onclick=()=>{el.hidden=true}}
setInterval(()=>{try{const P=S&&S.player;if(!running||!P){if($('rgOv')&&!rgCU)$('rgOv').hidden=true;return}
  if(P.asleep&&!rgCU){const el=rgOv();el.hidden=false;if(!rgWas)rgShown=performance.now();rgWas=true;$('rgOvT').textContent=`${rgName(P)} holds ${P.decl?P.decl.name:'your faction'}`;
    $('rgOvS').textContent=`For ${rgDur(S.T-P.asleep.T0)} so far · ${(P.regent&&P.regent.traits||[]).join(', ')}`;$('rgOvP').textContent='';
    $('rgOvL').innerHTML=(P.asleep.log||[]).slice(-10).map(x=>`<li>${esc(x.msg)}</li>`).join('');$('rgOvH').textContent='Press any key or click to wake: your stand-in resigns and reports.'}
  else if(!rgCU){if($('rgOv'))$('rgOv').hidden=true;rgWas=false;if(P.rgRep&&!P.asleep&&P.rgRep.T1!==rgLastRep&&S.T-P.rgRep.T1<120){rgLastRep=P.rgRep.T1;rgShowReport(P.rgRep)}}
  // idle: no input for 15 minutes and the stand-in may take over
  if(!P.asleep&&!rgCU&&rgOn(P)&&P.regent&&P.regent.idle!==false&&performance.now()-rgIn>RG.idle*1000){rgIn=performance.now();rgShown=performance.now();rgAct('sleep','idle')}}catch(e){}},1000);
// ---- the closed game: the save notes when you left; on reopening, the galaxy catches up while the stand-in holds the faction
{const o=serialize;serialize=function(){if(S)S.savedAt=Date.now();return o.apply(this,arguments)}}
{const o=startWith;startWith=function(state){const r=o.apply(this,arguments);try{const P=S.player,away=S.savedAt?(Date.now()-S.savedAt)/1000:0;
    if(RG.catchUp&&!NET.on&&rgOn(P)&&P.regent&&away>=RG.minAway&&myStations(P).length)rgCatchUp(Math.min(away,RG.cap))}catch(e){console.error(e)}return r}}
function rgCatchUp(secs){const P=S.player,R=myStations(P)[0],T1=S.T+secs,T0=S.T;
  try{if(W&&W.docking)W.docking=null;$('dock').hidden=true}catch(e){}
  for(const w of Object.values(WORLDS))try{closeWorld(w)}catch(e){console.error(e)}WORLDS={};LW=null;W=null;running=false;
  P.sector=R.sid;P.docked='station';P.x=P.y=P.z=0;P.vx=P.vy=P.vz=0;if(!P.asleep)rgSleep(P,'closed');window._fs=window._fs||{rg:1};rgCU={stop:false};
  const el=rgOv();el.hidden=false;$('rgOvT').textContent=`${rgName(P)} holds ${P.decl.name}`;$('rgOvL').innerHTML='';
  $('rgOvH').innerHTML='<button class="btn sm" type="button" id="rgStop">Stop here (skip the rest)</button>';$('rgStop').onclick=()=>{rgCU.stop=true};
  const step=()=>{const t0=performance.now();try{while(performance.now()-t0<40&&S.T<T1&&!rgCU.stop&&!S.won){S.T+=10;strategicTick();updateEvents()}}catch(e){console.error(e)}
    const left=Math.max(0,T1-S.T);$('rgOvS').textContent=`Catching up ${rgDur(left)} of ${rgDur(secs)} you were away…`;
    $('rgOvP').innerHTML=`<div style="height:6px;background:rgba(255,255,255,.08);border-radius:3px;margin:0 0 10px"><div style="height:6px;width:${Math.round(100*(S.T-T0)/secs)}%;background:#f0b24a;border-radius:3px"></div></div>`;
    $('rgOvL').innerHTML=((P.asleep&&P.asleep.log)||[]).slice(-8).map(x=>`<li>${esc(x.msg)}</li>`).join('');
    if(S.T<T1&&!rgCU.stop&&!S.won){setTimeout(step,0);return}
    if(window._fs&&window._fs.rg)delete window._fs;rgCU=null;el.hidden=true;S.savedAt=Date.now();running=true;
    try{const own=S.stations[P.sector];if(!(own&&own.owner==='player'&&(own.pid||'me')===pkeyOf(P))){const R2=myDepots(P)[0];if(R2)P.sector=R2.sid;else P.sector=pilotHome(P)}P.docked='station';enterSector(P.sector);if(W&&W.stationEnt&&canDock(W.stationEnt))openDock();else P.docked=null}catch(e){console.error(e)}
    rgWake(P);rgWas=false;if(P.rgRep){rgLastRep=P.rgRep.T1;rgShowReport(P.rgRep)}};
  setTimeout(step,50)}
// single player asleep with the tab hidden: keep the galaxy running (the browser stops drawing frames in a background tab)
{const wk=(()=>{try{return new Worker(URL.createObjectURL(new Blob(['setInterval(()=>postMessage(0),100)'],{type:'text/javascript'})))}catch(e){return null}})();let rgH=0;
  if(wk)wk.onmessage=()=>{try{if(!document.hidden||NET.on||!S||!running||!S.player||!S.player.asleep||!W){rgH=0;return}const now=performance.now(),dt=Math.min(.1,rgH?(now-rgH)/1000:.1);rgH=now;frameRun('simulation',()=>step(dt))}catch(e){}}}
