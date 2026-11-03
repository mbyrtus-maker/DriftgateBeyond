//@src 02b_standing.js
// ============================================================ standing (Beyond)
// A pilot is an independent contractor with a standing toward every power, -100..100, starting at 0:
//   P.stand  {halcyon, varkesh, ostrova, neutral}  (neutral = the Freeport Compact)
//   P.sworn  the faction a pilot has sworn to (declared allegiance), or null for an independent contractor
//   P.faction  the design faction only: which hull models, stats, names and cockpit colours the pilot flies
//   P.home   the freeport sector a contractor starts and respawns at (null for a sworn pilot: their faction's core)
//   P.job    the job being flown: {by: issuing power, kind, at: start time}, or null
// The Brood and the Unbound are always hostile and have no standing.
const STAND_POW=['halcyon','varkesh','ostrova','neutral'];
// bands: Hostile below -50, Unwelcome -50 to -10, Neutral -10 to +25, Trusted +25 to +60, Partner above +60
const STAND_BANDS=[['Hostile','#ff5d4f'],['Unwelcome','#ff9a4a'],['Neutral','#ece4cf'],['Trusted','#9fd8a8'],['Partner','#7ad9a7']];
// hitK: standing lost per point of damage to a power's ship or station (a Light Fighter's ~200 hull is about -8);
// aggro: seconds a power's ships and guns treat a contractor who just attacked one of theirs as hostile, whatever its standing;
// drift: standing per second back toward 0
const STAND={hostile:-50,dock:-10,drift:.01,hitK:.04,aggro:60,contract:3,escort:4,war:.25};
function standInit(P){if(!P)return;if(!P.stand||typeof P.stand!=='object')P.stand={};for(const f of STAND_POW)if(typeof P.stand[f]!=='number')P.stand[f]=0;
  if(P.sworn===undefined)P.sworn=null;if(P.home===undefined)P.home=null;if(P.job===undefined)P.job=null}
function swornOf(P){P=P||S.player;return P&&P.sworn||null}
function standOf(f,P){P=P||S.player;if(!P||!P.stand)return 0;const v=P.stand[f];return typeof v==='number'?v:0}
function standBand(v){return v<-50?0:v<-10?1:v<=25?2:v<=60?3:4}
function standName(v){return STAND_BANDS[standBand(v)][0]}
function standCol(v){return STAND_BANDS[standBand(v)][1]}
// the power that answers a pilot's distress call: their sworn faction, or for a contractor the power they stand best with (Neutral or better)
function helpFac(P){P=P||S.player;if(!P)return null;if(P.sworn)return FAC_IDS.includes(P.sworn)?P.sworn:null;let b=null,bv=STAND.dock;for(const f of FAC_IDS){const v=standOf(f,P);if(v>bv){bv=v;b=f}}return b}
// the sector a pilot starts and respawns at: a contractor's freeport, or a sworn pilot's faction core
function pilotHome(P){P=P||S.player;return P.home||FAC_HOME(P.sworn&&(FAC_IDS.includes(P.sworn)||P.sworn==='pirate')?P.sworn:P.faction)}
// whose intel a pilot shares: their sworn faction's, or every power's for an independent contractor (Beyond decision 3)
function intelSide(P,x){P=P||S.player;return P.sworn?x===P.sworn:FAC_IDS.includes(x)}
// is this side hostile to this pilot: a sworn pilot follows its faction; a contractor goes by standing (Hostile below -50).
// The Brood and the Unbound are always hostile. Allocation-free: it runs inside AI targeting.
function pilotHostile(P,x){P=P||S.player;if(!x||x==='player')return false;if(P.sworn)return hostile(P.sworn,x);if(x==='brood'||x==='pirate')return true;if(P.aggro&&P.aggro[x]>S.T)return true;if(x==='neutral')return false;return standOf(x,P)<STAND.hostile}
// can this pilot dock and trade at a station of this owner: sworn pilots at their faction's and the freeports (as in Driftgate 1);
// a contractor anywhere it stands Neutral or better (the freeports by its Compact standing)
function tradeOK(P,owner){P=P||S.player;if(owner==='player')return true;if(P.sworn)return owner===P.sworn||owner==='neutral';if(owner!=='neutral'&&!FAC_IDS.includes(owner))return false;return standOf(owner,P)>=STAND.dock}
// who pays a pilot's containment work (Seeder spotting, Brood kills with no job running): their sworn faction, or for a
// contractor the power they stand best with (containment pays every contractor)
function containPayer(P){P=P||S.player;if(!P||S.unb)return null;if(P.sworn)return FAC_IDS.includes(P.sworn)?P.sworn:null;let b=FAC_IDS[0],bv=-1e9;for(const f of FAC_IDS){const v=standOf(f,P);if(v>bv){bv=v;b=f}}return b}
// can this pilot fly escort for a convoy of this side: a sworn pilot for its own faction; a contractor for any power it
// stands Neutral or better with (the job is the power's, and the power pays)
function escortOK(P,side){P=P||S.player;if(P.sworn)return side===P.sworn;return FAC_IDS.includes(side)&&standOf(side,P)>=STAND.dock}
// who pays a pilot's bounty for a kill: a sworn pilot's faction (if it is at war with the victim); a contractor's job issuer
// if the job is running and the issuer is at war with the victim; otherwise the power at war with the victim that the pilot
// stands best with (and isn't hostile to the pilot); otherwise nobody. Credits stay zero-sum: the payer's treasury pays.
function bountyPayer(victim,P){P=P||S.player;if(!P||!victim||victim==='player')return null;
  if(P.sworn)return hostile(P.sworn,victim)?P.sworn:null;
  const j=P.job&&P.job.by;if(j&&FAC_IDS.includes(j)&&j!==victim&&hostile(j,victim))return j;
  let b=null,bv=STAND.hostile;for(const f of FAC_IDS){if(f===victim||!hostile(f,victim))continue;const v=standOf(f,P);if(v>=bv){bv=v;b=f}}return b}
// the side a pilot's war effort counts for: their sworn faction, or the issuer of the job they're flying (nobody without one)
function weSide(P){P=P||S.player;if(P.sworn)return P.sworn;const j=P.job&&P.job.by;return j&&FAC_IDS.includes(j)?j:null}
// whose jobs a pilot sees at this dock: a sworn pilot its faction's; a contractor the station owner's (Neutral or better), or at
// a freeport every power it stands Neutral or better with
function jobIssuers(c,P){P=P||S.player;if(P.sworn)return FAC_IDS.includes(P.sworn)?[P.sworn]:[];if(!c)return[];if(FAC_IDS.includes(c.owner))return standOf(c.owner,P)>=STAND.dock?[c.owner]:[];if(c.owner==='neutral')return FAC_IDS.filter(f=>standOf(f,P)>=STAND.dock);return[]}
// a pilot attacked a power's ship, convoy or station: standing falls with the damage done, and that power's ships fight back
// for a minute whatever the standing (sworn pilots lose standing too, but their hostility follows their faction)
function standHit(P,f,dmg,what){if(!P||!STAND_POW.includes(f)||!(dmg>0))return;standAdd(f,-dmg*STAND.hitK,what?`you attacked its ${what}`:'',P);if(!P.sworn)(P.aggro||(P.aggro={}))[f]=S.T+STAND.aggro}
// work done for a power: standing rises with it, and falls a quarter as much with the powers at war with it
function standWork(P,f,n,what){if(!P||!STAND_POW.includes(f)||!(n>0))return;standAdd(f,n,what,P);if(FAC_IDS.includes(f))for(const g of FAC_IDS)if(g!==f&&hostile(f,g))standAdd(g,-n*STAND.war,`war work for ${sideName(f)}`,P)}
// standing drifts slowly back toward 0
function standDrift(dt){for(const P of[S.player,...Object.values(S.pilots||{})]){if(!P||!P.stand)continue;for(const f of STAND_POW){const v=P.stand[f];if(v)P.stand[f]=v>0?Math.max(0,v-STAND.drift*dt):Math.min(0,v+STAND.drift*dt)}}}
// raise or lower a pilot's standing with a power; a change of band goes to the pilot's feed with the reason
function standAdd(f,n,why,P){P=P||S.player;if(!P||!P.stand||!STAND_POW.includes(f)||!n||!isFinite(n))return 0;
  const v0=P.stand[f],v1=clamp(v0+n,-100,100);P.stand[f]=v1;const b0=standBand(v0),b1=standBand(v1);
  if(b0!==b1&&P===S.player)feed(`${b1>b0?'▲':'▼'} ${sideName(f)}: ${STAND_BANDS[b1][0]}${why?` (${why})`:''}.`,b1>b0?'good':'bad');return v1-v0}
