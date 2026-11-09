//@src 16zzzh_systraits.js
// ============================================================ Beyond: makers' systems have a strength and a weakness (user, 8 Nov 2026)
// "All non-standard parts should have a weakness and a strength." A maker's system (drive, reactor, shield emitter, weapons
// system, armour, cargo hold, blast rig, payload bay) now carries a trait: one stat up, another down, on top of what its grade
// gives. The unbranded systems a ship comes with stay standard. The traits act on the pilot whose ship has the system
// installed (P.sysm records whose it is); AI ships' systems are unbranded.
//   key: maxSpd top speed, thrust, turn turning, eCap energy capacity, eRegen recharge, sCap shields, hull, dmg gun and laser
//   damage, shotCost laser energy a shot, lockT lock time, cargo hold, drill drilling, reload reload time
const SYS_TR={
  tcy:{engine:{thrust:.08,maxSpd:-.03},armor:{hull:.08,maxSpd:-.03}},
  ewd:{engine:{maxSpd:.08,turn:-.04},power:{eRegen:.1,eCap:-.06}},
  cr:{engine:{turn:.06,thrust:-.03},shield:{sCap:.05,eCap:-.03}},
  ad:{power:{eCap:.08,eRegen:-.04},shield:{sCap:.08,eRegen:-.04}},
  sw:{power:{eRegen:.06,eCap:-.03},weapon:{dmg:.06,shotCost:.08}},
  bl:{shield:{sCap:.12,maxSpd:-.02}},
  wf:{weapon:{lockT:-.12,dmg:-.03},payload:{reload:-.1,cargo:-.03}},
  mg:{weapon:{dmg:.08,lockT:.08}},
  hf:{armor:{hull:.12,turn:-.05},cargo:{cargo:.1,maxSpd:-.04},drill:{drill:.12,eRegen:-.04}},
  qs:{armor:{hull:.06,thrust:-.03},cargo:{cargo:.06,turn:-.03}},
  cp:{cargo:{cargo:.08,thrust:-.04},drill:{drill:.08,maxSpd:-.02}},
  mwa:{payload:{reload:-.06,thrust:-.02}}};
Object.assign(TR_TXT,{maxSpd:'top speed',thrust:'thrust',turn:'turning',eCap:'energy capacity',eRegen:'recharge',sCap:'shields',hull:'hull',shotCost:'laser energy a shot',lockT:'lock time',drill:'drilling',reload:'reload time'});
Object.assign(TR_GOOD,{maxSpd:1,thrust:1,turn:1,eCap:1,eRegen:1,sCap:1,hull:1,shotCost:-1,lockT:-1,drill:1,reload:-1});
function sysTr(m,sl){return(SYS_TR[m]&&SYS_TR[m][sl])||null}
// the systems' items carry their trait (every grade), shown wherever the item is
{const o=ceApply;ceApply=function(){o.apply(this,arguments);try{for(const m in MK_LINE)for(const id of MK_LINE[m]){const B=ITEMS[id];if(!B||!B.sys)continue;const tr=sysTr(m,B.sys)||{};
    for(let g=1;g<=5;g++){const G=g>1?ITEMS[rdGid(id,g)]:B;if(!G)continue;G.tr={...tr};G.trTxt=`${MAKERS[m].name}: ${RD_SYSN[B.sys]}, grade ${g}${Object.keys(tr).length?' · '+trText(tr):''}.`}}}catch(e){console.error(e)}}}
// whose ship a stats call is for: the pilot record behind its tune object
const SYS_P=new WeakMap();
{const o=fitOf;fitOf=function(P){const F=o.apply(this,arguments);try{if(P&&P.tune&&typeof P.tune==='object')SYS_P.set(P.tune,P)}catch(e){}return F}}
function sysTrSum(P,key){let s=0;const M=P&&P.sysm;if(!M)return 0;for(const sl in M){const t=sysTr(M[sl],sl);if(t&&t[key])s+=t[key]}return s}
{const o=shipStats;shipStats=function(fac,cls,T,U){const B=o.apply(this,arguments);try{const P=U&&typeof U==='object'?SYS_P.get(U):null;if(!P||!P.sysm||S.training)return B;
    for(const k of['maxSpd','thrust','turn','eCap','eRegen','sCap','hull','dmg','shotCost','drill','reload']){const v=sysTrSum(P,k);if(v&&typeof B[k]==='number')B[k]*=1+v}
    const c=sysTrSum(P,'cargo');if(c&&B.cargo)B.cargo=Math.round(B.cargo*(1+c))}catch(e){}return B}}
{const o=vK;vK=function(P,key){const v=o.apply(this,arguments);if(key==='lockK'&&P&&P.sysm&&!S.training){const t=sysTrSum(P,'lockT');if(t)return v*(1+t)}return v}}
