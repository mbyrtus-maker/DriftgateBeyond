//@src 16g_leaders.js
// ============================================================ relations between the powers, and their leaders (Beyond stage 2)
// Every pair of powers has a relation, -100..100, starting at 0 (Neutral). Interactions between their own ships and sworn
// pilots move it: beacon flips, ships destroyed, strikes, captures and razes are negatives; trade pacts, aid and ceasefires
// are positives. Bands: War below -50 (formally declared), Hostile -50..-10 (ships fight on sight), Neutral -10..25 (trade and
// docking, no campaigns), Friendly 25..60, Allied above 60 (never fight). The Brood and the Unbound have no relations.
// Leaders (one per power, two traits) choose among the events whose triggers are true right now, and announce them with a reason.
const REL={on:true,war:-50,hostile:-10,friendly:25,allied:60,drift:.004,
  kill:.8,capKill:5,beacon:3,strike:4,capture:12,depot:18,raze:24,raid:3,leader:40,
  leadCool:[150,300],pairCool:300,logMax:80,chronMax:160};
const REL_BANDS=[['War','#ff3b30'],['Hostile','#ff8a5c'],['Neutral','#ece4cf'],['Friendly','#9fd8a8'],['Allied','#5fe0a0']];
const TRAITS=['Ambitious','Vengeful','Mercantile','Cautious','Scheming','Patient','Wary','Loyal','Zealous','Honourable','Ruthless','Industrious','Isolationist','Opportunist'];
const LEAD0={halcyon:{title:'Chair of the Merchant Houses',traits:['Mercantile','Cautious']},varkesh:{title:'Marshal',traits:['Ambitious','Vengeful']},ostrova:{title:'First Archivist',traits:['Scheming','Patient']}};
const LEAD_NAMES={halcyon:['Aurelia Voss','Tobias Wren','Cassandra Lyle','Marius Hale','Ilse Varga','Benedict Rowe'],varkesh:['Draven Kol','Sabine Tarr','Ruslan Hesk','Veska Morn','Orrin Gault','Yarra Kettle'],ostrova:['Ilvane Sorre','Coren Abel','Senna Vey','Tovik Haar','Maren Ost','Quell Iver']};
function pkey2(a,b){return a<b?a+'|'+b:b+'|'+a}
function relInit(){if(!S||S.rel)return;S.rel={};for(const a of FAC_IDS){S.rel[a]={};for(const b of FAC_IDS)if(a!==b)S.rel[a][b]=0}
  S.relLog=[];S.chron=[];S.pair={};for(let i=0;i<FAC_IDS.length;i++)for(let j=i+1;j<FAC_IDS.length;j++)S.pair[pkey2(FAC_IDS[i],FAC_IDS[j])]={war:0,ally:0,pact:0,emb:0,cool:0,demand:null,betray:0,warT:0};
  S.hurt={};S.loss={};leadersInit()}
function pairOf(a,b){return S.pair&&S.pair[pkey2(a,b)]}
function relOf(a,b){if(!S||!S.rel||!S.rel[a])return 0;const v=S.rel[a][b];return typeof v==='number'?v:0}
function relBand(v){return v<REL.war?0:v<REL.hostile?1:v<=REL.friendly?2:v<=REL.allied?3:4}
function relBandOf(a,b){const P=pairOf(a,b);if(P&&P.war)return 0;if(P&&P.ally)return 4;return Math.max(1,Math.min(3,relBand(relOf(a,b))))}
function isPow(x){return FAC_IDS.includes(x)}
// relation between two powers moves; the ledger entry is kept (merged with a recent one of the same kind)
function relAdd(a,b,n,why){if(!S||!S.rel||!isPow(a)||!isPow(b)||a===b||!n||!isFinite(n))return;const P=pairOf(a,b),v0=S.rel[a][b];let v=clamp(v0+n,-100,100);
  if(P&&P.war)v=Math.min(v,REL.war-1);if(P&&P.ally)v=Math.max(v,REL.friendly);S.rel[a][b]=S.rel[b][a]=v;
  const L=S.relLog,last=L[L.length-1];if(why){if(last&&last.why===why&&pkey2(last.a,last.b)===pkey2(a,b)&&S.T-last.T<120){last.n+=n;last.T=S.T}else{L.push({T:S.T,a,b,n,why});if(L.length>REL.logMax)L.shift()}}
  const b0=relBand(v0),b1=relBand(v);if(b0!==b1&&!(P&&(P.war||P.ally)))chron(`${FAC(a).short} and ${FAC(b).short} are now ${REL_BANDS[b1][0]}${why?` (${why})`:''}.`,b1<b0?'bad':'good',[a,b])}
function hurtAdd(f,by,n){if(!isPow(f)||!isPow(by)||f===by)return;S.hurt=S.hurt||{};const H=S.hurt[f]=S.hurt[f]||{};H[by]=(H[by]||0)+n;if(n>=REL.capture){S.loss=S.loss||{};const L=S.loss[f]=S.loss[f]||{};L[by]=(L[by]||0)+4}}
// the chronicle: every leader decision and every turn in relations, readable on the Allegiance tab
function chron(msg,kind,who){if(!S)return;S.chron=S.chron||[];S.chron.push({T:S.T,msg,who:who||[]});if(S.chron.length>REL.chronMax)S.chron.shift();
  if(!STRAT_SIM()&&S.player&&(!S.player.sworn||!who||!who.length||who.includes(S.player.sworn)||kind==='big'))feed(msg,kind==='good'?'good':kind==='bad'?'bad':kind==='big'?'warn':'news')}
// war and hostility between powers. hostile(): ships fight (Hostile or War, or the truce against a leader); warWith(): campaigns
// and sieges (a declared war, or the truce turned on whoever is near winning). The Containment Accord overrides both.
function relHostile(A,B){const C=S.coal;if(C){if(C.lead==='brood'&&C.mem.includes(A)&&C.mem.includes(B))return false;if(C.lead!=='brood'&&((C.mem.includes(A)&&B===C.lead)||(C.mem.includes(B)&&A===C.lead)))return true}
  const P=pairOf(A,B);if(P){if(P.ally)return false;if(P.war)return true}return relOf(A,B)<REL.hostile}
function warWith(a,b){a=sideNorm(a);b=sideNorm(b);if(!REL.on||!S.rel||!isPow(a)||!isPow(b))return hostile(a,b);if(a===b)return false;const C=S.coal;
  if(C){if(C.lead==='brood'&&C.mem.includes(a)&&C.mem.includes(b))return false;if(C.lead!=='brood'){if((C.mem.includes(a)&&b===C.lead)||(C.mem.includes(b)&&a===C.lead))return true;if(C.mem.includes(a)&&C.mem.includes(b))return false}}
  const P=pairOf(a,b);return!!(P&&P.war)}
// ---- leaders
function leaderNew(f,traits,n){const used=new Set(Object.values(S.leaders||{}).map(L=>L.name).concat((S.chron||[]).length?[]:[]));const pool=LEAD_NAMES[f].filter(x=>!used.has(x)&&!(S.leadPast||[]).includes(x));
  return{f,name:pick(pool.length?pool:LEAD_NAMES[f]),title:LEAD0[f].title,traits:traits.slice(0,2),since:S.T,cool:S.T+(S.T<60?rnd(90,200):rnd(REL.leadCool[0],REL.leadCool[1])),grudge:{},n:n||1,
    ship:{sid:FAC_HOME(f),alive:true,back:0,move:S.T+rnd(60,180)}}}
// Beyond: each galaxy rolls its starting leaders' traits afresh (two different traits each, no two leaders with the same
// pair), so the same story doesn't play out every time; LEADT.mode 'neutral' starts them with none (the balance runs) and
// 'fixed' uses LEAD0's (Driftgate 1's) pairs
const LEADT={mode:'random'};
function leadRoll(){const out={},seen=new Set();for(const f of FAC_IDS){let t;do{const a=pick(TRAITS);let b=pick(TRAITS);while(b===a)b=pick(TRAITS);t=[a,b]}while(seen.has([...t].sort().join('|')));seen.add([...t].sort().join('|'));out[f]=t}return out}
function leadersInit(){if(S.leaders)return;S.leaders={};const R=LEADT.mode==='random'?leadRoll():null;for(const f of FAC_IDS){S.leaders[f]=leaderNew(f,LEADT.mode==='neutral'?[]:R?R[f]:LEAD0[f].traits,1)}leaderProfiles()}
function leaderOf(f){return S&&S.leaders&&S.leaders[f]||null}
function lName(f){const L=leaderOf(f);return L?`${L.title} ${L.name}`:FAC(f).short}
function hasT(f,t){const L=leaderOf(f);return!!L&&L.traits.includes(t)}
// how much a leader leans to an event: 1 base, +2 for each trait that leans that way, 0 if a trait forbids it
const EV_LEAN={border:['Ambitious','Industrious','Isolationist'],embargo:['Mercantile','Vengeful'],pact:['Mercantile','Industrious','Patient'],aid:['Cautious','Patient','Loyal','Honourable'],
  alliance:['Patient','Cautious','Honourable','Loyal'],reprisal:['Vengeful','Ruthless'],war:['Ambitious','Vengeful','Opportunist','Ruthless'],ceasefire:['Cautious','Mercantile','Honourable','Patient'],betrayal:['Ambitious','Scheming','Opportunist']};
const EV_NEVER={alliance:['Isolationist'],betrayal:['Loyal','Honourable'],aid:['Isolationist']};
function evWeight(f,k){const L=leaderOf(f);if(!L)return 0;if((EV_NEVER[k]||[]).some(t=>L.traits.includes(t)))return 0;let w=1;for(const t of L.traits)if((EV_LEAN[k]||[]).includes(t))w+=2;return w}
function sysCount(f){return controlCounts()[f]||0}
function heldNear(f,g){// f holds a depot or outpost one jump from one of g's (a border)
  const mine=[],theirs=new Set();for(const sid in S.stations){const R=S.stations[sid];if(R.kind==='core')continue;if(R.owner===f)mine.push(sid);else if(R.owner===g)theirs.add(sid)}
  for(const id in S.outposts){const o=S.outposts[id];if(o.owner===f)mine.push(o.sector);else if(o.owner===g)theirs.add(o.sector)}
  for(const s of mine)if(NEIGH[s].some(n=>theirs.has(n)))return s;return null}
function short(f,k){const st=S.econ.stock[f]||{};return(st[k]||0)<(k==='fe'||k==='cu'?80:30)}
function surplus(f,k){const st=S.econ.stock[f]||{};return(st[k]||0)>(k==='fe'||k==='cu'?260:90)}
const PACT_ITEMS=['fe','cu','ir','xc','plate','wire','coil'];
function pactNeed(f,g){for(const k of PACT_ITEMS)if((short(f,k)&&surplus(g,k))||(short(g,k)&&surplus(f,k)))return k;return null}
function underSiege(f){return S.events.some(e=>e.type==='offensive'&&e.stage!=='done'&&e.st&&S.stations[e.st]&&S.stations[e.st].owner===f)}
function weary(f,g){const lost=((S.loss||{})[f]||{})[g]||0,P=pairOf(f,g);return lost>=8||(S.econ.treasury[f]||0)<60000||(controlCounts().brood||0)>=3||(P&&P.war&&S.T-P.warT>2400)}
// the events a leader can choose from right now, each with its cause
function leaderOptions(f){const out=[],n=controlCounts();
  for(const g of FAC_IDS){if(g===f)continue;const P=pairOf(f,g),v=relOf(f,g);if(!P||S.T<P.cool)continue;const hurt=((S.hurt||{})[f]||{})[g]||0,gr=(leaderOf(f).grudge||{})[g]||0;
    const add=(k,why,fn)=>{const w=evWeight(f,k);if(w>0)out.push({k,g,why,fn,w})};
    if(!P.war&&!P.ally&&v<REL.friendly&&!P.demand){const s=heldNear(f,g);if(s)add('border',`${FAC(g).short} holds ground beside ${f==='halcyon'?'Accord':FAC(f).short} space at ${DEF[s].name}`,()=>evBorder(f,g,s))}
    if(!P.emb&&!P.ally&&(v<REL.hostile||hurt>=6))add('embargo',hurt>=6?`${FAC(g).short} raided ${FAC(f).short} trade`:`relations have turned hostile`,()=>evEmbargo(f,g));
    if(!P.war&&!P.emb&&!P.pact&&v>=REL.hostile){const k=pactNeed(f,g);if(k)add('pact',`each is short of what the other has (${ITEMS[k].name})`,()=>evPact(f,g,k))}
    if(!P.war&&v>REL.friendly&&(underSiege(g)||short(g,'plate')))add('aid',underSiege(g)?`${FAC(g).short} is under siege`:`${FAC(g).short} is short of plate`,()=>evAid(f,g));
    if(!P.ally&&!P.war&&v>REL.allied){const th=FAC_IDS.find(h=>h!==f&&h!==g&&(n[h]||0)>=VIC_NEED-2)||((n.brood||0)>=3?'brood':null);if(th)add('alliance',th==='brood'?'the Brood is spreading':`${FAC(th).short} is nearing control of the galaxy`,()=>evAlliance(f,g,th))}
    if(!P.ally&&hurt>=12)add('reprisal',`${FAC(g).short} struck ${FAC(f).short} hard`,()=>evReprisal(f,g));
    if(!P.war&&!P.ally&&((v<REL.war&&(gr>0||hurt>0))||(v<REL.hostile&&gr>=1&&(hasT(f,'Vengeful')||hasT(f,'Ambitious')||hasT(f,'Ruthless')))||(v<REL.hostile&&(n[g]||0)>=(n[f]||0)+2&&(hasT(f,'Ambitious')||hasT(f,'Opportunist')))))add('war',v<REL.war?`an unanswered wrong`:`${FAC(g).short} is leading in systems`,()=>evWar(f,g));
    if(P.war&&S.T-P.warT>600&&weary(f,g))add('ceasefire',`the war is bleeding ${FAC(f).short}`,()=>evCeasefire(f,g));
    if(P.ally&&((n[g]||0)>=VIC_NEED-2||((S.econ.treasury[g]||0)>(S.econ.treasury[f]||0)*1.5&&(n[g]||0)<(n[f]||0))))add('betrayal',(n[g]||0)>=VIC_NEED-2?`${FAC(g).short} is nearing control of the galaxy`:`${FAC(g).short} is rich and weak`,()=>evBetrayal(f,g))}
  return out}
function leaderTick(){if(!S||!S.leaders||!REL.on)return;
  for(const f of FAC_IDS){const L=leaderOf(f);if(!L||S.T<L.cool)continue;const opts=leaderOptions(f);L.cool=S.T+rnd(REL.leadCool[0],REL.leadCool[1]);if(!opts.length)continue;
    const o=wpickArr(opts.map(x=>[x,x.w]));const P=pairOf(f,o.g);P.cool=S.T+REL.pairCool;o.fn()}
  // demands come due: complied (a payment to settle it) or ignored (an unanswered wrong)
  for(const k in S.pair){const P=S.pair[k];const D=P.demand;if(!D||S.T<D.until)continue;P.demand=null;const by=D.by,to=D.to;
    const comply=!P.war&&(hasT(to,'Cautious')||hasT(to,'Mercantile')||hasT(to,'Honourable')||hasT(to,'Patient'))&&Math.random()<.55&&(S.econ.treasury[to]||0)>30000;
    if(comply){const n=transfer(to,by,2500);relAdd(by,to,5,'a border settled');chron(`${lName(to)} settles the border dispute with ${FAC(by).short}: ${fmt(n)} cr paid.`,'good',[by,to])}
    else{relAdd(by,to,-8,'a demand ignored');const G=leaderOf(by).grudge;G[to]=(G[to]||0)+1;chron(`${FAC(to).short} ignores ${lName(by)}'s demand over ${DEF[D.sid].name}. ${FAC(by).short} will remember it.`,'bad',[by,to])}}}
function evBorder(f,g,s){relAdd(f,g,-6,'a border dispute');pairOf(f,g).demand={by:f,to:g,sid:s,until:S.T+420};chron(`${lName(f)} demands that ${FAC(g).short} withdraw from beside ${DEF[s].name} within 7 minutes.`,'bad',[f,g])}
function evEmbargo(f,g){const P=pairOf(f,g);P.emb=1;P.pact=0;relAdd(f,g,-8,'an embargo');chron(`${lName(f)} declares an embargo on ${FAC(g).name}: trade between them stops.`,'bad',[f,g])}
function evPact(f,g,k){const P=pairOf(f,g);P.pact=S.T+1800;relAdd(f,g,6,'a trade pact');chron(`${lName(f)} signs a trade pact with ${FAC(g).name}: merchants will run between them (${ITEMS[k].name} first).`,'good',[f,g])}
function evAid(f,g){const st=S.econ.stock[f],give={};for(const k of['plate','wire','coil'])if((st[k]||0)>40)give[k]=Math.min(25,Math.floor(st[k]*.15));if(!Object.keys(give).length)return;
  inv.addAll(S.econ.stock[g],takeSome(st,give));relAdd(f,g,8,'aid sent');chron(`${lName(f)} sends ${FAC(g).short} an aid shipment: ${Object.entries(give).map(([k,n])=>n+' '+ITEMS[k].name).join(', ')}.`,'good',[f,g])}
function takeSome(st,want){const got={};for(const k in want){const n=Math.min(st[k]||0,want[k]);if(n>0)got[k]=inv.take(st,k,n)}return got}
function evAlliance(f,g,th){const P=pairOf(f,g),ok=!hasT(g,'Isolationist')&&relOf(f,g)>(hasT(g,'Wary')?75:55);
  if(!ok){relAdd(f,g,-3,'an alliance refused');chron(`${lName(g)} turns down ${lName(f)}'s offer of alliance.`,'news',[f,g]);return}
  P.ally=1;P.pact=Math.max(P.pact,S.T+1800);P.emb=0;relAdd(f,g,10,'an alliance');chron(`${FAC(f).name} and ${FAC(g).name} form an alliance: ${th==='brood'?'the Brood is spreading':FAC(th).short+' is nearing control of the galaxy'}.`,'big',[f,g])}
function evReprisal(f,g){relAdd(f,g,-6,'a reprisal');S.ai[f].focus={on:g,until:S.T+420};S.ai[f].next=Math.min(S.ai[f].next,S.T+20);S.hurt[f][g]=0;chron(`${lName(f)} orders a reprisal against ${FAC(g).short}.`,'bad',[f,g])}
function evWar(f,g){const P=pairOf(f,g);P.war=1;P.warT=S.T;P.pact=0;P.ally=0;S.rel[f][g]=S.rel[g][f]=Math.min(relOf(f,g)-15,-60);(leaderOf(f).grudge||{})[g]=0;S.loss=S.loss||{};for(const x of[f,g]){S.loss[x]=S.loss[x]||{};S.loss[x][x===f?g:f]=0}
  S.firstWar=S.firstWar||S.T;chron(`${lName(f)} declares war on ${FAC(g).name}.`,'big',[f,g])}
function evCeasefire(f,g){const P=pairOf(f,g),ok=weary(g,f)||((hasT(g,'Cautious')||hasT(g,'Mercantile')||hasT(g,'Honourable')||hasT(g,'Patient'))&&Math.random()<.5)||Math.random()<.25;
  if(!ok){relAdd(f,g,-2,'a ceasefire refused');chron(`${FAC(g).short} refuses ${lName(f)}'s offer of a ceasefire.`,'bad',[f,g]);return}
  P.war=0;S.rel[f][g]=S.rel[g][f]=-30;chron(`${FAC(f).name} and ${FAC(g).name} agree a ceasefire. The war is over, for now.`,'big',[f,g])}
function evBetrayal(f,g){const P=pairOf(f,g);if(!P.betray){P.betray=S.T;relAdd(f,g,-20,'relations cooling');P.cool=S.T+240;chron(`Relations between ${FAC(f).short} and ${FAC(g).short} are cooling: ${lName(f)} recalls envoys.`,'bad',[f,g]);return}
  P.ally=0;P.betray=0;P.war=1;P.warT=S.T;S.rel[f][g]=S.rel[g][f]=-70;(leaderOf(g).grudge||{})[f]=3;S.betrayed=S.betrayed||{};S.betrayed[g]=f;chron(`${lName(f)} breaks the alliance and declares war on ${FAC(g).name}. A betrayal.`,'big',[f,g])}
// ---- successions: the new leader's traits come from what happened to the faction
const LEAD_OUST={tenure:1800,grace:3600,drop:.5,minDrop:5,lost:30};
const SUCC={ousted:['Cautious','Patient'],killed:['Vengeful'],core:['Vengeful'],bled:['Cautious'],embargo:['Mercantile'],betrayed:['Wary'],saved:['Loyal'],conquest:['Ambitious'],brood:['Zealous'],peace:['Patient','Mercantile','Honourable'],razed:['Ruthless'],short:['Industrious'],far:['Isolationist'],neighbour:['Opportunist']};
function succession(f,cause,by){const L0=leaderOf(f);if(!L0)return;const hist=[cause];
  const n=controlCounts(),lost=Object.values(((S.loss||{})[f])||{}).reduce((a,b)=>a+b,0);if(lost>=12)hist.push('bled');if((n.brood||0)>=4)hist.push('brood');if(short(f,'plate')&&short(f,'wire'))hist.push('short');
  if(S.betrayed&&S.betrayed[f])hist.push('betrayed');if((n[f]||0)>=5)hist.push('conquest');if(!FAC_IDS.some(g=>g!==f&&(pairOf(f,g)||{}).war))hist.push('peace');
  const bar=cause==='ousted'?L0.traits:[],pool=[];for(const h of hist)for(const t of SUCC[h]||[])if(!pool.includes(t)&&!bar.includes(t))pool.push(t);while(pool.length<2){const t=pick(TRAITS);if(!pool.includes(t)&&!bar.includes(t))pool.push(t)}
  const traits=[pool[0],pool.slice(1)[Math.floor(Math.random()*(pool.length-1))]];S.leadPast=S.leadPast||[];S.leadPast.push(L0.name);
  const N=leaderNew(f,traits,(L0.n||1)+1);if(by&&isPow(by)&&traits.includes('Vengeful'))N.grudge[by]=3;S.leaders[f]=N;leaderProfiles();
  const why={killed:`${L0.name} was killed${by?' by '+(isPow(by)?FAC(by).short:by):''}`,core:`the fall of ${FAC(f).station}`,bled:'a long, losing war',betrayed:'betrayal by an ally',far:'a lost war',ousted:`being ousted: ${L0.ousted||'the power is failing'}`}[cause]||cause;
  chron(`${FAC(f).name}: ${N.title} ${N.name} succeeds ${L0.name} after ${why}. ${N.name} is ${traits.join(' and ')}.`,'big',[f])}
// ---- what pilots do: a leader's traits shape how its power's AI ships fight (steps of stage 2)
let LEADP={};
function leaderProfiles(){LEADP={};if(!S||!S.leaders)return;for(const f of FAC_IDS){const L=leaderOf(f),t=x=>L.traits.includes(x),p={range:1,breakoff:0,stay:false,honour:false,ruthless:false,zeal:false};
  if(t('Ambitious'))p.range*=1.3;if(t('Opportunist'))p.range*=1.15;if(t('Cautious')){p.range*=.85;p.breakoff=.3}if(t('Patient'))p.range*=.9;if(t('Isolationist'))p.range*=.9;if(t('Mercantile'))p.breakoff=Math.max(p.breakoff,.2);
  if(t('Vengeful')){p.stay=true;p.breakoff=0}if(t('Honourable'))p.honour=true;if(t('Ruthless'))p.ruthless=true;if(t('Zealous'))p.zeal=true;LEADP[f]=p}}
function leadP(side){return LEADP[side]||null}
// ---- relation drift, pacts trading, losses and hurts fading
function relTick(){if(!S||!S.rel)return;
  for(const k in S.pair){const P=S.pair[k],[a,b]=k.split('|');const v=S.rel[a][b];
    if(!P.war&&!P.ally&&v){const d=REL.drift*10*(v>0?.5:1);S.rel[a][b]=S.rel[b][a]=v>0?Math.max(0,v-d):Math.min(0,v+d)}
    if(P.pact&&S.T>P.pact&&!P.ally)P.pact=0;if(P.emb&&relOf(a,b)>REL.friendly)P.emb=0;
    if(P.pact&&!P.emb&&Math.random()<.08)pactTrade(a,b);
    // the enemy of my enemy: two powers at war with the same third warm to each other
    if(!P.war&&!P.ally&&FAC_IDS.some(c=>c!==a&&c!==b&&(pairOf(a,c)||{}).war&&(pairOf(b,c)||{}).war)&&relOf(a,b)<REL.allied+10)relAdd(a,b,.3,'a common enemy')}
  // a long losing war brings a new leader
  if(Math.random()<.05)for(const f of FAC_IDS){const L=leaderOf(f);if(!L||S.T-L.since<1800)continue;const lost=Object.values((S.loss||{})[f]||{}).reduce((x,y)=>x+y,0),wars=FAC_IDS.filter(g=>g!==f&&(pairOf(f,g)||{}).war);
    if(wars.length&&lost>=14&&wars.some(g=>S.T-pairOf(f,g).warT>1800&&sysCount(g)>sysCount(f)))succession(f,'bled')}
  // a power cut down or bleeding ships ousts its own leader (Beyond): from 30 minutes into a leader's rule, losing half of the
  // systems it held at its best under this leader (at least 5), or 30 ships' worth of recent losses, brings a successor who
  // shares none of the ousted leader's traits; a successor who replaced an ousted leader gets an hour before it can happen again
  {S.lpk=S.lpk||{};const n=controlCounts();for(const f of FAC_IDS){const L=leaderOf(f);if(!L)continue;const k=L.name+L.n;const P=S.lpk[f]&&S.lpk[f].k===k?S.lpk[f]:(S.lpk[f]={k,pk:0});const h=n[f]||0;P.pk=Math.max(P.pk,h);
    S.oustT=S.oustT||{};if(S.T-L.since<LEAD_OUST.tenure||S.T-(S.oustT[f]||-1e9)<LEAD_OUST.grace||Math.random()>=.1)continue;const lost=Object.values((S.loss||{})[f]||{}).reduce((x,y)=>x+y,0);
    const why=P.pk-h>=LEAD_OUST.minDrop&&h<=P.pk*(1-LEAD_OUST.drop)?`${FAC(f).short} has fallen from ${P.pk} systems to ${h}`:lost>=LEAD_OUST.lost?`${FAC(f).short} has lost ship after ship`:null;
    if(why){L.ousted=why;S.oustT[f]=S.T;succession(f,'ousted')}}}
  for(const f in S.hurt||{})for(const g in S.hurt[f])S.hurt[f][g]*=.985;
  for(const f in S.loss||{})for(const g in S.loss[f])S.loss[f][g]*=.995;
  for(const f of FAC_IDS){const G=(leaderOf(f)||{}).grudge||{};for(const g in G)G[g]*=hasT(f,'Vengeful')?.9995:.998}}
// merchants under a pact: goods one side is short of, from the other's surplus, paid for at base value (goods and credits only move)
function pactTrade(a,b){for(const[f,g]of[[a,b],[b,a]]){for(const k of PACT_ITEMS){if(!short(f,k)||!surplus(g,k))continue;const n=Math.min(20,Math.floor((S.econ.stock[g][k]||0)*.1));if(n<1)continue;
  const cost=Math.round(baseValue(k)*n);if((S.econ.treasury[f]||0)<cost)continue;transfer(f,g,cost);inv.add(S.econ.stock[f],k,inv.take(S.econ.stock[g],k,n));relAdd(a,b,1,'trade');return}}}
// ---- hooks: what the powers' own ships do to each other moves their relation
{const o=strategicTick;strategicTick=function(){relInit();const r=o.apply(this,arguments);try{relTick();leaderTick();leaderShipTick()}catch(e){frameErr&&frameErr('leaders',e)}return r}}
{const o=beaconFlip;beaconFlip=function(sid,side,by){const B=S.beacons&&S.beacons[sid],old=B&&B.owner;const r=o.apply(this,arguments);if(old&&isPow(old)&&isPow(sideNorm(side))&&S.beacons[sid].owner!==old)relAdd(sideNorm(side),old,-REL.beacon,'beacons flipped');return r}}
{const o=killShip;killShip=function(e,src,at){try{const v=e.side,k=src?sideNorm(src):null;if(isPow(v)&&isPow(k)&&k!==v){relAdd(k,v,-(e.role==='frigate'?REL.capKill:REL.kill),'ships lost');S.loss=S.loss||{};const L=S.loss[v]=S.loss[v]||{};L[k]=(L[k]||0)+(e.role==='frigate'?4:1)}
  if(e.leaderOf)leaderKilled(e,src,at)}catch(err){}return o.apply(this,arguments)}}
{const o=capture;capture=function(o2,side){const prev=o2.owner;const r=o.apply(this,arguments);const s=sideNorm(side);if(isPow(prev)&&isPow(s)&&prev!==s){relAdd(s,prev,-REL.capture,`${o2.name} captured`);hurtAdd(prev,s,REL.capture)}return r}}
{const o=captureDepot;captureDepot=function(sid,side){const R=S.stations[sid],prev=R&&R.owner;const r=o.apply(this,arguments);const s=sideNorm(side),R2=S.stations[sid];if(R2&&isPow(prev)&&isPow(s)&&R2.owner===s&&prev!==s){relAdd(s,prev,-REL.depot,`${R2.name} captured`);hurtAdd(prev,s,REL.depot);if(R2.kind==='core')succession(prev,'core',s)}return r}}
{const o=razeStation;razeStation=function(sid,by){const R=S.stations[sid],prev=R&&R.owner;const r=o.apply(this,arguments);const s=sideNorm(by);if(isPow(prev)&&isPow(s)&&prev!==s&&!S.stations[sid]){relAdd(s,prev,-REL.raze,'a station razed');hurtAdd(prev,s,REL.raze)}return r}}
{const o=planOffensive;planOffensive=function(f){const n0=S.events.length;const r=o.apply(this,arguments);for(let i=n0;i<S.events.length;i++){const ev=S.events[i];if(ev.type!=='offensive')continue;const ow=sideNorm(ev.st?(S.stations[ev.st]||{}).owner:(S.outposts[ev.target]||{}).owner);if(isPow(f)&&isPow(ow)&&ow!==f){relAdd(f,ow,-REL.strike,'strikes');hurtAdd(ow,f,REL.strike*.5)}}return r}}
// ---- leaders as ships: a leader flies with an ace-grade escort; off-screen it moves between its power's systems; in a live
// system it is spawned with its wing; shot down, it is succeeded (and the killer's side pays heavily on the ledger)
function leaderShipTick(){if(NET.cl||!S||!S.leaders||S.training)return;
  for(const f of FAC_IDS){const L=leaderOf(f),Sh=L&&L.ship;if(!Sh)continue;
    if(!Sh.alive)continue;
    if(Sh.live){if(!leaderEnt(f)){Sh.live=0}else continue}
    if(S.T>=Sh.move){const terr=[...territory(f)],opts=terr.filter(s=>s!==Sh.sid&&NEIGH[Sh.sid].includes(s));Sh.sid=opts.length&&Math.random()<.7?pick(opts):FAC_HOME(f);Sh.move=S.T+rnd(150,300)}
    const w=WORLDS[Sh.sid];if(w&&!STRAT_SIM())leaderSpawn(f,w)}}
function leaderEnt(f){for(const sid in WORLDS)for(const e of WORLDS[sid].ents)if(e.leaderOf===f&&e.alive)return e;return null}
function leaderSpawn(f,w){const L=leaderOf(f),Sh=L.ship;let g=null;inW(w,()=>{try{xNoAce=true;const A={id:'L'+f,side:f,name:L.name,nick:L.title,cls:hasT(f,'Mercantile')?'freighter':hasT(f,'Ambitious')?'heavy':'striker'};
    g=aceWing(A);if(g){const e=g.members[0];leaderBoost(e,f);for(const m of g.members.slice(1)){m.tier=4}}}finally{xNoAce=false}});
  if(g){Sh.live=1;if(w===LW)feed(`♛ ${lName(f)} of ${FAC(f).name} is in this system, with an escort.`,'warn')}}
function leaderBoost(e,f){const L=leaderOf(f),st=shipStats(f,e.cls,3,1);st.hull*=3;st.sCap*=2;st.dmg*=1.3;e.st=st;e.hull=st.hull;e.shield=st.sCap;e.energy=st.eCap;e.tier=4;e.tuned=1;e.leaderOf=f;e.pname=`♛ ${L.title} ${L.name}`}
function leaderKilled(e,src,at){const f=e.leaderOf,L=leaderOf(f);if(!L)return;L.ship.alive=false;L.ship.live=0;const k=src?sideNorm(src):null,kp=at&&at.src&&at.src.rp,killer=kp||(src==='player'?'me':null);
  const P=killer?xPilotOfKey(killer):null,who=P&&!P.sworn?(P.name||'a contractor'):isPow(k)?FAC(k).short:k==='brood'?'the Brood':k==='pirate'?'the Unbound':'unknown guns';
  if(isPow(k)&&k!==f){relAdd(k,f,-REL.leader,'a leader killed');hurtAdd(f,k,REL.leader)}if(P&&!P.sworn)standAdd(f,-REL.leader,`you killed ${L.name}`,P);
  if(P){const pay=bountyPayer(f,P);if(pay)runAs(isMe(killer)?null:killer,()=>{const got=transfer(pay,'player',6000);if(got)feed(`♛ ${lName(f)} is dead. ${FAC(pay).short} pays +${fmt(got)} cr.`,'good')})}
  succession(f,'killed',isPow(k)?k:null);const N=leaderOf(f);N.ship.alive=false;N.ship.back=S.T+600;
  chron(`${L.title} ${L.name} of ${FAC(f).name} was shot down by ${who} in ${DEF[W.sid].name}.`,'big',[f])}
{const o=leaderShipTick;leaderShipTick=function(){for(const f of FAC_IDS){const L=leaderOf(f);if(L&&L.ship&&!L.ship.alive&&S.T>=L.ship.back){L.ship.alive=true;L.ship.sid=FAC_HOME(f);L.ship.move=S.T+rnd(60,180)}}return o.apply(this,arguments)}}
// ---- the Allegiance tab: your standing, the relations between the powers, their leaders and the chronicle
function allegianceHtml(P){relInit();let h='';
  h+=`<div class="h3">Your standing</div><div class="tblw"><table class="t"><tbody>${STAND_POW.map(f=>{const v=standOf(f,P),pct=Math.round((v+100)/2);return`<tr><td style="width:120px"><b style="color:${sideCol(f)}">${esc(sideName(f))}</b></td><td><div style="height:6px;background:rgba(255,255,255,.08);position:relative;max-width:320px"><i style="position:absolute;left:0;top:0;bottom:0;width:${pct}%;background:${standCol(v)}"></i><i style="position:absolute;left:50%;top:-2px;bottom:-2px;width:1px;background:rgba(236,228,207,.4)"></i></div></td><td style="width:100px;color:${standCol(v)}">${standName(v)}</td></tr>`}).join('')}</tbody></table></div>`;
  if(P.sworn)h+=`<p class="note">You fly for ${esc(FAC(P.sworn).name)}.</p>`;
  h+=`<div class="h3" style="margin-top:16px">Between the powers</div><div class="tblw"><table class="t"><thead><tr><th></th>${FAC_IDS.map(f=>`<th style="color:${sideCol(f)}">${esc(FAC(f).short)}</th>`).join('')}</tr></thead><tbody>${FAC_IDS.map(a=>`<tr><td style="color:${sideCol(a)}"><b>${esc(FAC(a).short)}</b></td>${FAC_IDS.map(b=>{if(a===b)return'<td class="r" style="color:var(--faint)">·</td>';const bd=relBandOf(a,b),P2=pairOf(a,b),tags=[P2.pact?'pact':'',P2.emb?'embargo':''].filter(Boolean).join(', ');return`<td><b style="color:${REL_BANDS[bd][1]}">${REL_BANDS[bd][0]}</b>${tags?`<span class="mass">${tags}</span>`:''}</td>`}).join('')}</tr>`).join('')}</tbody></table></div>`;
  h+=`<div class="h3" style="margin-top:16px">Leaders</div><div class="tblw"><table class="t"><tbody>${FAC_IDS.map(f=>{const L=leaderOf(f);return`<tr><td style="color:${sideCol(f)};width:120px"><b>${esc(FAC(f).short)}</b></td><td>${esc(L.title)} ${esc(L.name)}${L.n>1?` <span class="mass">${ordinal(L.n)} of the line</span>`:''}</td><td>${L.traits.map(esc).join(' · ')}</td><td class="r" style="color:var(--dim)">${L.ship&&!L.ship.alive?'not flying':L.ship?`in ${esc(DEF[L.ship.sid].name)}`:''}</td></tr>`}).join('')}</tbody></table></div>`;
  const C=(S.chron||[]).slice(-14).reverse();h+=`<div class="h3" style="margin-top:16px">Chronicle</div>`+(C.length?`<div class="log">${C.map(x=>`<div><b>${fmtT(x.T)}</b>${esc(x.msg)}</div>`).join('')}</div>`:'<div class="empty">Nothing yet: the powers are watching each other.</div>');
  return h}
function ordinal(n){return n===2?'second':n===3?'third':n===4?'fourth':n===5?'fifth':n+'th'}
// ---- AI pilots fly like their leader: reach (Ambitious chase further, Cautious and Patient less), break-off (Cautious and
// Mercantile ships pull out when badly hurt; Vengeful never do), who they go for first (Ruthless: miners, haulers and freight;
// Zealous: the Brood), and Honourable ships leave a jammed-dark ship alone
{const o=findHostile;findHostile=function(e,range){const p=leadP(e.side);if(!p)return o.apply(this,arguments);const R=range*p.range;let t=o.call(this,e,R);
  if(p.ruthless||p.zeal){let best=null,bd=R*1.2;for(const x of W.ents){if(x.type!=='ship'||!x.alive||x===e||!hostE(e.side,x)||mHid(x,e)||(x.isPlayer&&(S.player.docked||W.dead)))continue;
      if(p.ruthless&&!(x.role==='miner'||x.role==='hauler'||x.role==='trader'))continue;if(p.zeal&&!p.ruthless&&x.side!=='brood')continue;const d=d3(x,e);if(d<bd){bd=d;best=x}}if(best)t=best}
  if(t&&p.honour&&jamDark(t))t=null;return t}}
{const o=npcThink;npcThink=function(e,dt){const p=e.npc&&leadP(e.side);if(p&&p.breakoff&&(e.role==='patrol'||e.role==='escort'||e.role==='raider')&&e.ai&&e.ai.tgt&&!e.leaderOf&&e.hull<e.st.hull*p.breakoff&&!e.order){e.role='leave';e.ai.tgt=null}return o.apply(this,arguments)}}
// distress calls in Brood space are answered by every power, whatever their relations (truce zones keep them off each other)
{const o=distressCall;distressCall=function(sid,name,owner,by){const r=o.apply(this,arguments);try{if(!NET.cl&&S&&broodHeld(sid))for(const f of FAC_IDS)if(f!==owner)dispatchResponse(f,sid,'distress')}catch(e){}return r}}
{const o=pilotDistress;pilotDistress=function(){const sid=W&&W.sid,t0=S.player&&S.player.distT;const r=o.apply(this,arguments);try{if(sid&&broodHeld(sid)&&S.player.distT!==t0){const h=helpFac(S.player);for(const f of FAC_IDS)if(f!==h)dispatchResponse(f,sid,'pilot',{pid:CTX||(NET.on?NET.me:null),name:S.player.name||'pilot'})}}catch(e){}return r}}
// the Containment Accord: fighting the Brood side by side warms every pair a little
{const o=coalTick;coalTick=function(){const was=!!(S.coal&&S.coal.lead==='brood');const r=o.apply(this,arguments);if(!was&&S.coal&&S.coal.lead==='brood'&&S.rel){for(let i=0;i<FAC_IDS.length;i++)for(let j=i+1;j<FAC_IDS.length;j++)relAdd(FAC_IDS[i],FAC_IDS[j],5,'the Containment Accord')}return r}}
// sieges, strikes and campaigns between powers need a war (or the truce against a leader); against anyone else, hostility
function fightsAt(a,b){const A=sideNorm(a),B=sideNorm(b);return isPow(A)&&isPow(B)?warWith(A,B):hostile(a,b)}
// for the fast simulator: how the relations went this galaxy
function relStats(){const C=S.chron||[],cnt=re=>C.filter(x=>re.test(x.msg)).length,w={};for(const k in S.pair||{})w[k]=S.pair[k].war?1:0;
  return{firstWar:S.firstWar?Math.round(S.firstWar/60):null,wars:cnt(/declares war/),ceasefires:cnt(/ceasefire\./),alliances:cnt(/form an alliance/),betrayals:cnt(/A betrayal/),successions:cnt(/ succeeds /),pacts:cnt(/trade pact/),embargoes:cnt(/embargo on/),disputes:cnt(/demands that/),atWar:w,
    rel:Object.fromEntries(Object.keys(S.pair||{}).map(k=>{const[a,b]=k.split('|');return[k,Math.round(relOf(a,b))]}))}}
