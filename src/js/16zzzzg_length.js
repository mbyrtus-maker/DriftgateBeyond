//@src 16zzzzg_length.js
// ============================================================ Beyond: game length (user, 11 Nov 2026)
// "Game length needs to extend to 12-14 hours with the option to go longer." Wars ended at a median of 5.8 h (war check of
// 10 Nov: 51% before hour 6; the Brood's wins at a median of 3.7 h), about when a pilot can first afford a company.
// A galaxy carries a length setting, S.glen: 'std' (12 to 14 hours, every new galaxy) or 'long'. A save from before this
// has none and keeps the old rules ('legacy'). The setting's dials, LEN (from LEN_SET[S.glen]):
//   quiet, full, bq  the Brood's quiet opening: its growth dials run at bq of full strength until `quiet` seconds, then rise
//                    to full strength by `full` seconds (bq 1 = no quiet opening)
//   floor            no side's hold on the galaxy starts before this many seconds
//   hold             seconds a side must hold `need` systems to win (WIN_TIME)
//   need             systems to win (VIC_NEED)
//   tempo            the time between any side's offensives is multiplied by this (1 = as before)
//   truce            1 = the other powers call a truce against a power on the win clock (TRUCE_POWERS; the user turned
//                    this off on 8 Nov 2026, so it is 0 in every setting and only war checks try it)
//   clock            the galaxy's clock: the strategic turn (mining into the warehouses, industry, every side's decisions,
//                    the makers and the rest of the off-screen galaxy) runs once every `clock` beats of 10 s instead of
//                    every beat, and each side's waits for its next offensive and next build are stretched to match.
//                    Battles, sieges, convoys and the hold on the galaxy keep real time. (1 = as before)
// The values are tuned by war checks (BEYOND_DESIGN.md "Game length"); a tune file sets LEN_SET.std.* or LEN_SET.long.*.
const LEN_SET={legacy:{quiet:0,full:0,bq:1,floor:0,hold:600,need:20,tempo:1,truce:0,clock:1},
  std:{quiet:0,full:0,bq:1,floor:0,hold:600,need:20,tempo:1,truce:0,clock:1},
  long:{quiet:0,full:0,bq:1,floor:0,hold:600,need:20,tempo:1,truce:0,clock:1}};
const LEN={...LEN_SET.legacy};
let LEN_NEW='std';
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
{const o=strategicTick;strategicTick=function(){try{lenApply()}catch(e){}
  const k=LEN.clock>1?LEN.clock:1;if(k===1)return o.apply(this,arguments);
  S.lenAcc=(S.lenAcc||0)+1;if(S.lenAcc<k)return;S.lenAcc-=k;
  const b={};for(const f in S.ai)b[f]=[S.ai[f].next,S.ai[f].build];
  const r=o.apply(this,arguments);
  try{for(const f in S.ai){const a=S.ai[f],p=b[f]||[];if(a.next!==p[0]&&a.next>S.T)a.next=S.T+(a.next-S.T)*k;if(a.build!==p[1]&&a.build>S.T)a.build=S.T+(a.build-S.T)*k}}catch(e){console.error(e)}
  return r}}
// the war check's record: the setting and its dials
{const o=relStats;relStats=function(){const r=o.apply(this,arguments);try{r.glen=lenKey();r.len={...LEN}}catch(e){}return r}}
