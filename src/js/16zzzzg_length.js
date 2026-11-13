//@src 16zzzzg_length.js
// ============================================================ Beyond: game length (user, 11 Nov 2026)
// "Game length needs to extend to 12-14 hours with the option to go longer." Wars ended at a median of 5.8 h (war check of
// 10 Nov: 51% before hour 6; the Brood's wins at a median of 3.7 h), about when a pilot can first afford a company.
// A galaxy carries a length setting, S.glen: 'std' (about 8 hours) or 'long', chosen on the start screen (the user settled
// near 8 hours on 12 Nov 2026 rather than slow the off-screen galaxy or add new war rules). A save from before this
// has none and keeps the old rules ('legacy'). The setting's dials, LEN (from LEN_SET[S.glen]):
//   quiet, full, bq  the Brood's quiet opening: its growth dials run at bq of full strength until `quiet` seconds, then rise
//                    to full strength by `full` seconds (bq 1 = no quiet opening)
//   floor            no side's hold on the galaxy starts before this many seconds
//   hold             seconds a side must hold `need` systems to win (WIN_TIME)
//   need             systems to win (VIC_NEED)
//   tempo            the time between any side's offensives is multiplied by this (1 = as before)
//   truce            1 = the other powers call a truce against a power on the win clock (TRUCE_POWERS; the user turned
//                    this off on 8 Nov 2026, so it is 0 in every setting and only war checks try it)
// The values are tuned by war checks (BEYOND_DESIGN.md "Game length"); a tune file sets LEN_SET.std.* or LEN_SET.long.*.
const LEN_SET={legacy:{quiet:0,full:0,bq:1,floor:0,hold:600,need:20,tempo:1,truce:0},
  std:{quiet:0,full:0,bq:1,floor:21600,hold:1800,need:24,tempo:1,truce:0},
  long:{quiet:0,full:0,bq:1,floor:36000,hold:3600,need:24,tempo:1,truce:0}};
const LEN={...LEN_SET.legacy};
let LEN_NEW='std';
try{const k=localStorage.getItem('dgbeyond.glen');if(k==='std'||k==='long')LEN_NEW=k}catch(e){}
// the start screen's choice (step 6, under the ship): made when a galaxy is made; a saved galaxy or one you join keeps its own
const LEN_INFO={std:['Standard','About 8 hours.'],long:['Long','About 11 hours or more.']};
function lenLine(k){const L=LEN_SET[k];return`${L.need} systems held for ${L.hold>=3600?(L.hold/3600===1?'an hour':Math.round(L.hold/360)/10+' hours'):Math.round(L.hold/60)+' minutes'} wins${L.floor?`, and no win before hour ${Math.round(L.floor/3600)}`:''}`}
function lenPickDraw(){const el=$('glens');if(!el)return;el.innerHTML=Object.keys(LEN_INFO).map(k=>`<button class="role" type="button" data-glen="${k}" aria-pressed="${k===LEN_NEW}"><b>${LEN_INFO[k][0]}</b><span>${LEN_INFO[k][1]} ${lenLine(k)}.</span></button>`).join('')}
(function(){const sp=$('start')&&$('start').querySelector('.shippick');if(!sp||$('glens'))return;
  sp.insertAdjacentHTML('afterend','<div class="step"><i>6</i><span>Game length</span></div><div class="roles" id="glens"></div><div class="note" style="margin:0;padding:6px 26px 0;font-size:12px">The length is set when a galaxy is made. A saved galaxy, or one you join, keeps its own.</div>')})();
{const o=showStart;showStart=function(){const r=o.apply(this,arguments);try{lenPickDraw()}catch(e){console.error(e)}return r}}
try{document.addEventListener('click',e=>{const b=e.target&&e.target.closest&&e.target.closest('#glens [data-glen]');if(!b)return;const k=b.dataset.glen;if(!LEN_INFO[k])return;LEN_NEW=k;try{localStorage.setItem('dgbeyond.glen',k)}catch(err){}lenPickDraw()})}catch(e){}
// a guest takes the host's setting from the galaxy it was sent
try{setInterval(()=>{try{if(S&&NET.cl)lenApply()}catch(e){}},3000)}catch(e){}
// the galaxy map's line under "Galaxy control"
function lenMapNote(){const k=lenKey();if(k==='legacy')return'';return` · ${LEN_INFO[k][0]} length${LEN.floor>S.T?` · no win before hour ${Math.round(LEN.floor/3600)}`:''}`}
function lenKey(){return S&&!S.training&&S.glen&&LEN_SET[S.glen]?S.glen:'legacy'}
function lenApply(){Object.assign(LEN,LEN_SET[lenKey()]);WIN_TIME=LEN.hold;VIC_NEED=LEN.need;TRUCE_POWERS=!!LEN.truce}
{const o=newGame;newGame=function(){const r=o.apply(this,arguments);try{if(S&&!S.training&&!S.glen)S.glen=LEN_NEW;lenApply()}catch(e){console.error(e)}return r}}
{const o=migrate;migrate=function(){const r=o.apply(this,arguments);try{lenApply()}catch(e){}return r}}
// the Brood's quiet opening
function lenBroodF(){if(!(LEN.bq<1)||!S)return 1;const a=LEN.quiet,b=Math.max(LEN.full,a+1);return LEN.bq+(1-LEN.bq)*clamp((S.T-a)/(b-a),0,1)}
{const o=broodRamp;broodRamp=function(){const r=o.apply(this,arguments);try{const f=lenBroodF();if(f<1){BAL.brBuild/=f;BAL.brOff/=f;BAL.brGraze*=f;BAL.hiveRegrow/=f}}catch(e){}return r}}
// no hold on the galaxy before the floor: the clock doesn't start, and every pilot is told once per would-be winner
{const o=victoryTick;victoryTick=function(){if(S&&!S.training&&!S.won&&LEN.floor>0&&S.T<LEN.floor){try{const n=controlCounts();broodWatch(n);S.victory=null;S.vicLastT=S.T;let lead=null;for(const k in n)if(n[k]>=VIC_NEED&&(!lead||n[k]>n[lead]))lead=k;
      if(lead&&S.lenTold!==lead){S.lenTold=lead;if(!STRAT_SIM())allFeed(`${lead==='brood'?'The Brood':sideName(lead)} holds ${n[lead]} systems, but no claim on the galaxy stands before hour ${Math.round(LEN.floor/3600)}.`,'warn')}}catch(e){console.error(e)}return}
  return o.apply(this,arguments)}}
// tempo: the wait until a side's next offensive, stretched
{const o=planOffensive;planOffensive=function(f){const r=o.apply(this,arguments);try{const a=S.ai&&S.ai[f];if(LEN.tempo!==1&&a&&a.next>S.T)a.next=S.T+(a.next-S.T)*LEN.tempo}catch(e){}return r}}
{const o=strategicTick;strategicTick=function(){try{lenApply()}catch(e){}return o.apply(this,arguments)}}
// the war check's record: the setting and its dials
{const o=relStats;relStats=function(){const r=o.apply(this,arguments);try{r.glen=lenKey();r.len={...LEN}}catch(e){}return r}}
