//@src 16s_declare.js
// ============================================================ declaring a faction, the 20-system win, the Brood's ramp (Beyond stage 13)
// Owning a Station lets you declare your own faction (Allegiance tab). Declared, your Stations count toward the galaxy (20
// systems held for 10 minutes wins; freeports and the Wrack can't be held) and the truce against whoever starts the clock
// applies to you too: lead, and the three powers turn on you together. Losing your last Station ends the faction (you keep
// your company). The powers' leaders send a founder proposals: an alliance when they think well of you, a demand for tribute
// when they don't. Wars come slower than Driftgate 1's. The Brood starts slow and grows with every system it holds.
const DECL={propEvery:600,tribute:2000,allyStand:40,demandStand:-20,brood:[[1,.31],[5,.6],[12,1.15]],hiveAt:4};
REL.leadCool=[240,480];REL.pairCool=450;
function myStations(P){return myDepots(P).filter(R=>R.pst)}
function declOK(P){return!P.sworn&&!P.decl&&myStations(P).length>0&&!S.unb}
function declare(P){if(P.sworn)return'You fly for a faction: renounce it first.';if(P.decl)return'You have already declared.';if(!myStations(P).length)return'Declaring takes a Station of your own.';
  P.decl={name:`${P.name||'Your'} Free Company`.replace(/^Your Free/,'Your Free'),T:S.T};P.props=[];allFeed(`⚑ ${P.name||'A contractor'} declares a faction: ${P.decl.name}. It holds ${controlCounts().player||0} system${(controlCounts().player||0)===1?'':'s'}.`,'news');
  return`✓ ${P.decl.name} is declared. Hold ${VIC_NEED} systems for ${Math.round(WIN_TIME/60)} minutes to win the galaxy; lead, and the powers will unite against you.`}
// the coalition aimed at a declared faction makes its members hostile to the founder
{const o=pilotHostile;pilotHostile=function(P,x){if(o.apply(this,arguments))return true;P=P||S.player;const C=S.coal;return!!(P&&P.decl&&C&&C.lead==='player'&&C.mem.includes(x))}}
// allies proposed and accepted: their stations are open and their ships friendly while standing holds
{const o=tradeOK;tradeOK=function(P,owner){P=P||S.player;if(P&&P.allied&&P.allied[owner]&&standOf(owner,P)>=0)return true;return o.apply(this,arguments)}}
// leaders' proposals to a founder
function declTick(){const P=S.player;if(!P||!P.decl)return;if(!myStations(P).length){feed(`✕ ${P.decl.name} has lost its last Station: it falls back into a company. Build or win back a Station to declare again.`,'bad');P.decl=null;P.props=[];return}
  P.props=(P.props||[]).filter(x=>S.T<x.until);S.propT=S.propT||{};
  for(const f of FAC_IDS){if((S.propT[f]||0)>S.T||P.props.some(x=>x.f===f))continue;S.propT[f]=S.T+DECL.propEvery*rnd(.8,1.4);const st=standOf(f,P),L=leaderOf(f);
    if(st>=DECL.allyStand&&!(P.allied&&P.allied[f])&&!hasT(f,'Vengeful')){P.props.push({id:S.nextId++,f,k:'ally',until:S.T+300});feed(`✉ ${lName(f)} of ${FACTIONS[f].short} proposes an alliance with ${P.decl.name}. Answer on the Allegiance tab.`,'info')}
    else if(st<=DECL.demandStand){P.props.push({id:S.nextId++,f,k:'demand',amt:DECL.tribute,until:S.T+300});feed(`✉ ${lName(f)} of ${FACTIONS[f].short} demands ${fmt(DECL.tribute)} cr in tribute from ${P.decl.name}, or its fleets will come. Answer on the Allegiance tab.`,'warn')}}}
function propAnswer(P,id,yes){const x=(P.props||[]).find(y=>String(y.id)===String(id));if(!x)return'That proposal has lapsed.';P.props=P.props.filter(y=>y!==x);const f=x.f;
  if(x.k==='ally'){if(!yes){standAdd(f,-5,'you refused an alliance',P);return`You decline ${FACTIONS[f].short}'s alliance.`}P.allied=P.allied||{};P.allied[f]=1;standAdd(f,10,'alliance',P);for(const g of FAC_IDS)if(g!==f&&hostile(f,g))standAdd(g,-8,`allied with ${FACTIONS[f].short}`,P);chron(`${P.decl.name} and ${FACTIONS[f].name} are allied.`);return`✓ Allied with ${FACTIONS[f].short}: its stations are open to you and its standing with you rises.`}
  if(x.k==='demand'){if(yes){if(P.credits<x.amt)return'Not enough credits for the tribute.';transfer('player',f,x.amt);standAdd(f,12,'tribute paid',P);return`✓ Tribute paid: ${FACTIONS[f].short} is appeased for now.`}
    standAdd(f,-15,'tribute refused',P);(P.aggro||(P.aggro={}))[f]=S.T+600;chron(`${P.decl.name} refused ${FACTIONS[f].short}'s demand.`);return`You refuse. ${FACTIONS[f].short}'s ships will attack you for ten minutes.`}return''}
{const o=dockAction;dockAction=function(act,arg){const P=S.player;if(act==='declare'){dockErr=declare(P);return}if(act==='prop'){const[id,yn]=String(arg).split(':');dockErr=propAnswer(P,id,yn==='y');return}return o.apply(this,arguments)}}
{const o=coClick;coClick=function(act,arg){if(act==='declare'||act==='prop'){if(NET.cl){netSend({t:'act',act,arg});coErr='Working…';renderCompany();return}dockAction(act,arg);coErr=dockErr;renderCompany();return}return o.apply(this,arguments)}}
{const o=allegianceHtml;allegianceHtml=function(P){P=P||S.player;let h=o.apply(this,arguments);if(P.sworn||S.unb)return h;const n=controlCounts().player||0;
  let d=`<div class="h3" style="margin-top:18px">Your faction</div>`;
  if(P.decl){d+=`<div class="kv"><span>${esc(P.decl.name)}</span><b class="amber">${n} of ${VIC_NEED} systems</b></div><p class="note" style="margin:2px 0 8px">Hold ${VIC_NEED} systems for ${Math.round(WIN_TIME/60)} minutes to win the galaxy. Lose your last Station and the faction falls back into a company.${P.allied&&Object.keys(P.allied).length?` Allied with ${Object.keys(P.allied).map(f=>esc(FACTIONS[f].short)).join(', ')}.`:''}</p>`;
    for(const x of P.props||[])d+=`<div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:4px 0"><span>${x.k==='ally'?`✉ ${esc(lName(x.f))} proposes an alliance`:`✉ ${esc(lName(x.f))} demands ${fmt(x.amt)} cr tribute`} · ${fmtT(Math.max(0,x.until-S.T))}</span><button class="btn sm" type="button" data-co="prop" data-arg="${x.id}:y">${x.k==='ally'?'Accept':'Pay'}</button><button class="btn sm" type="button" data-co="prop" data-arg="${x.id}:n">${x.k==='ally'?'Decline':'Refuse'}</button></div>`}
  else d+=`<p class="note" style="margin:0 0 8px">Owning a Station lets you declare your own faction and contend for the galaxy: ${VIC_NEED} systems held for ${Math.round(WIN_TIME/60)} minutes wins.</p><button class="btn${declOK(P)?' pri':''}" type="button" data-co="declare" ${declOK(P)?'':'disabled'}>Declare your faction</button>`;
  return h+d}}
// ---- the Brood grows with what it holds: one strength scale from the systems it holds (0.31 with the Bloom alone, 0.6 at
// five, 1.15 at twelve or more; tuned 3 Nov 2026 with the powers' perks), and its Hive Ships come out from four systems
// brOff and brBuild are intervals (time between offensives, between Seeder builds) and hiveRegrow a regrowth time, so they
// are divided by the scale (it starts slow, then attacks bigger and more often); brGraze is bites a tick, so it is multiplied.
// A tune file sets BR0.*, not BAL.*: broodRamp resets BAL's Brood dials from BR0 every tick.
// base intervals retuned 7 Nov 2026 when the ramp was turned the right way round, with grazing at 3.2 (quick looks, 120
// galaxies: .13/.3 gave the Brood 23%, .15/.35 22%, .16/.38 20%): at the Bloom alone an offensive every 49 to 77 s and a
// Seeder every 4.5 to 7 minutes, at twelve systems every 13 to 21 s and 1.2 to 1.9 minutes
const BR0={brBuild:.38,brOff:.16,brGraze:BAL.brGraze,hiveRegrow:BAL.hiveRegrow,brLevT:BAL.brLevT};
function broodK(n){const T=DECL.brood;if(n<=T[0][0])return T[0][1];for(let i=1;i<T.length;i++)if(n<=T[i][0]){const[a,ka]=T[i-1],[b,kb]=T[i];return ka+(kb-ka)*(n-a)/(b-a)}return T[T.length-1][1]}
function broodRamp(){const n=controlCounts().brood||0,k=broodK(n);S.broodK=k;BAL.brBuild=BR0.brBuild/k;BAL.brOff=BR0.brOff/k;BAL.brGraze=BR0.brGraze*k;BAL.hiveRegrow=BR0.hiveRegrow/k;BAL.brLevT=n>=DECL.hiveAt?Math.min(BR0.brLevT,S.T):1e12}
{const o=strategicTick;strategicTick=function(){try{if(!S.training&&!S.unb)broodRamp()}catch(err){}const r=o.apply(this,arguments);try{if(!NET.cl&&!S.training)declTick()}catch(err){console.error(err)}return r}}
{const o=relStats;relStats=function(){const r=o.apply(this,arguments);try{r.broodK=+(S.broodK||0).toFixed(2);r.counts=controlCounts()}catch(e){}return r}}
