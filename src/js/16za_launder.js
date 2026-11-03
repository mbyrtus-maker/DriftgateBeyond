//@src 16za_launder.js
// ============================================================ laundering takes time in a Lair's stash (Beyond, 3 Nov 2026)
// Stage 9 took the stolen tag off goods the moment they went into a Lair's stash. The design says after a short spell, longer
// for more tonnes: stolen goods stashed now carry their tag in the stash (L.lt, a list of batches) for 60 s plus 5 s a tonne.
// Taken out before then, they come out still tagged; once the spell is over the tag is gone. Only tags move: the goods
// themselves never change, so the ledger is untouched.
const LAUND={base:60,perT:5};
function lairOfDock(){const c=dockCtx();return c&&c.lairRec||null}
function stolTot(P,k){const t=P.stol&&P.stol[k];let n=0;if(t)for(const f in t)n+=t[f];return n}
{const o=dockAction;dockAction=function(act,arg){const L=(act==='mv'||act==='mvall'||act==='stashall')&&!S.unb?lairOfDock():null;if(!L)return o.apply(this,arguments);const P=S.player;
  const before={};for(const k in L.stash)before[k]=L.stash[k]||0;const tags={};for(const k in P.stol||{})tags[k]=Object.assign({},P.stol[k]);
  const r=o.apply(this,arguments);L.lt=L.lt||[];
  const keys=new Set([...Object.keys(before),...Object.keys(L.stash)]);
  for(const k of keys){const d=(L.stash[k]||0)-(before[k]||0);if(!d)continue;
    if(d>0){const t=tags[k];if(!t)continue;let tagged=0;for(const f in t)tagged+=t[f];const have=(P.cargo[k]||0)+((P.vault||{})[k]||0);let moved=Math.min(d,Math.max(0,tagged-have));if(moved<=0)continue;
      const split={};for(const f in t){const m=Math.min(t[f],moved);if(m>0){split[f]=m;moved-=m}if(moved<=0)break}const n=Object.values(split).reduce((a,b)=>a+b,0);
      for(const f in split){P.stol[k][f]-=split[f];if(P.stol[k][f]<=0)delete P.stol[k][f]}if(P.stol[k]&&!Object.keys(P.stol[k]).length)delete P.stol[k];
      L.lt.push({k,by:split,n,until:S.T+LAUND.base+LAUND.perT*mass(k)*n});dockErr=(dockErr?dockErr+' ':'')+`🧺 ${n} stolen ${ITEMS[k].name} will be clean in ${fmtT(LAUND.base+LAUND.perT*mass(k)*n)}.`}
    else{let out=-d;for(const B of L.lt.filter(x=>x.k===k)){if(out<=0)break;const m=Math.min(out,B.n);for(const f in B.by){const q=Math.min(B.by[f],m);if(q>0){stolAdd(P,k,f,q);B.by[f]-=q}}B.n-=m;out-=m}L.lt=L.lt.filter(x=>x.n>0)}}
  return r}}
// the spell ends: the tag is gone
function launderTick(){for(const L of S.lairs||[]){if(!L.lt||!L.lt.length)continue;const done=L.lt.filter(x=>S.T>=x.until);if(!done.length)continue;L.lt=L.lt.filter(x=>S.T<x.until);
  for(const B of done){const O=lairOwner(L);if(O)keyFeed(L.pid,`🧺 ${B.n} ${ITEMS[B.k].name} in your ${DEF[L.sid].name} Lair are clean now.`,'good')}}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{if(!NET.cl&&!S.unb)launderTick()}catch(err){console.error(err)}return r}}
// the stash shows what is still being laundered
{const o=dockCtx;dockCtx=function(){const c=o.apply(this,arguments);try{const L=c&&c.lairRec;if(L&&L.lt&&L.lt.length){const n=L.lt.reduce((a,b)=>a+b.n,0),t=Math.max(...L.lt.map(b=>b.until))-S.T;c.sub+=` · laundering ${n} (${fmtT(Math.max(0,t))})`}}catch(err){}return c}}
