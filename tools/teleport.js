// Teleport audit harness (tools/teleport.py loads this into the page with __dg.ev). It gives every store of goods a place
// (a system, 'B' for the Brood's stores, 'N' for the outer drift), snapshots them around every game function that runs in a
// strategic tick, and records each window in which goods left one system and appeared in another with no ship carrying them.
//   - a ship's hold (a convoy, a raid, a scout, a capital, an independent, a fleet on its way) moves with the ship;
//   - Brood stores are one place, so the Brood may move goods as it likes (the user, 24 Nov 2026);
//   - goods held in a local variable in the middle of a transfer are waited out (a window closes only when the galaxy's
//     total is whole again);
//   - debris drifting between systems and the drift re-seeding rock are nature, and are passed over;
//   - a capital's strike craft lost in the system next door flew there.
// A new store added to ledger() must be given a place in T.snap below, or the totals stop matching the ledger.
(()=>{
const T=window._tp={agg:{},cnt:{},C:null,mode:0,on:false,inSnap:false,stack:[],last:null,snaps:0,ms:0,orig:{}};
const Z=()=>[0,0,0,0,0,0];
const outSec={};for(const sid in OUT_BY_SECTOR)outSec[OUT_BY_SECTOR[sid]]=sid;
const RW=['fe','cu','ir','xc','au','nu'];
function vec(o){const v=invVec(o);return[v.fe,v.cu,v.ir,v.xc,v.au,v.nu]}
function any(o){if(!o)return false;for(const k in o)if(o[k])return true;return false}
T.snap=function(){
  const st={},mob=[];
  const add=(sid,lab,o)=>{if(!any(o))return;const v=vec(o),key=sid+'|'+lab,a=st[key]||(st[key]=Z());for(let i=0;i<6;i++)a[i]+=v[i]};
  const addM=(own,fn,lab,o)=>{if(!any(o))return;mob.push({own,fn,lab,v:vec(o),loc:fn(own)})};
  const sec=x=>x.sector;
  for(const id in S.sectors){const s=S.sectors[id];const a=st[id+'|rock']=Z();for(const r of s.ast)for(const k in r.ore){const i=RW.indexOf(k);if(i>=0)a[i]+=r.ore[k];else add(id,'rock',{[k]:r.ore[k]})}
    const d=st[id+'|debris']=Z();for(let i=0;i<6;i++)d[i]+=s.debris[RW[i]]||0;for(const c of s.crates)add(id,'crate',c.inv);for(const c of s.clouds||[])add(id,'crate',c.ore);for(const w of s.wrecks||[])for(const p of w.pts)add(id,'wreck',p.ore)}
  for(const k in S.econ.stock){const o=S.econ.stock[k];if(k==='brood')add('B','brood:wh',o);else if(k==='neutral')add('?neutral','pool:neutral',o);else add(FAC_HOME(k)||('?'+k),'wh:'+k,o)}
  for(const O of S.og||[])add('B','brood:og',O.load);
  for(const k in S.econ.fleet){if(k==='brood')add('B','brood:fleet',S.econ.fleet[k]);else add(FAC_HOME(k)||('?'+k),'fleet:'+k,S.econ.fleet[k])}
  for(const k in S.plans||{})add(FAC_HOME(k)||'?plan','plan:'+k,S.plans[k].res);
  for(const ev of S.events)if(ev.force){if(ev.att==='brood'||ev.side==='brood')add('B','brood:ev',ev.force);else addM(ev,evLoc,'ev:'+ev.type+(ev.kind?'/'+ev.kind:'')+':'+(ev.att||ev.side||ev.pid||''),ev.force)}
  for(const r of S.raids||[]){const b=r.side==='brood'||r.f==='brood';if(b){add('B','brood:raid',r.kit);add('B','brood:raid',r.loot)}else{addM(r,sec,'raid:'+(r.side||r.f||'pirate'),r.kit);addM(r,sec,'raidloot',r.loot)}}
  for(const f in S.ai||{})if(S.ai[f]&&S.ai[f].hm){if(f==='brood')add('B','brood:hm',S.ai[f].hm.force);else add(FAC_HOME(f),'hm:'+f,S.ai[f].hm.force)}
  for(const t of S.scouts||[]){if(t.side==='brood')add('B','brood:scout',t.load);else addM(t,sec,'scout:'+t.side,t.load)}
  for(const t of S.traders||[]){if(t.side==='brood')add('B','brood:trader',t.load);else addM(t,x=>x.sector||x.to,'trader:'+t.side+':'+(t.kind||'trade')+':'+(t.why||''),t.load)}
  for(const t of S.frigates||[]){if(t.side==='brood'){add('B','brood:cap',t.load);add('B','brood:cap',t.store);if(t.fab)add('B','brood:cap',t.fab.kit)}else{addM(t,sec,'cap:'+t.side,t.load);addM(t,sec,'capstore:'+t.side,t.store);if(t.fab)addM(t,sec,'capfab:'+t.side,t.fab.kit)}}
  for(const id in S.outposts){const o=S.outposts[id],s=outSec[id]||('?out'+id);if(o.owner==='brood'){add('B','brood:out',o.stock);add('B','brood:out',o.fort)}else{add(s,'outpost:'+o.owner,o.stock);add(s,'outfort:'+o.owner,o.fort)}}
  for(const id in S.stations||{}){const R=S.stations[id];if(R.owner==='brood'){for(const x of[R.fort,R.stock,R.store,R.ustock,R.gut])add('B','brood:station',x);for(const h of R.hg||[])add('B','brood:station',h.load);continue}
    const t=R.kind+':'+R.owner;add(id,'stfort:'+t,R.fort);add(id,'ststock:'+t,R.stock);add(id,'store:'+t,R.store);add(id,'ustock:'+t,R.ustock);add(id,'gut:'+t,R.gut);for(const h of R.hg||[])add(id,'hangar:'+t,h.load)}
  for(const k in S.yards||{})add(S.yards[k].sector,'yard:'+k,S.yards[k].fort);
  for(const L of S.lairs||[]){add(L.sid,'lair',L.stash);add(L.sid,'lair',L.fort)}
  add('N','drift',S.drift);
  for(const P of allPilots()){add(P.sector,'pilot',P.cargo);add('?vault','vault',P.vault);for(const k in P.vaults||{})add(k,'vaultAt',P.vaults[k]);if(P.convoy)for(const t of P.convoy.ships)add('?pconvoy','pconvoy',t.load)}
  for(const x of S.bmRuns||[])add('?bm','bmrun',x.load);
  for(const x of S.glocks||[])add(x.a,'glock',x.load);
  for(const k in S.mrs||{}){const ro=S.mrs[k];for(const m of ro.m)add(ro.f==='brood'?'B':ro.sid,(ro.f==='brood'?'brood:':'')+'miner:'+ro.f,m.load)}
  for(const k in S.gar||{}){const ro=S.gar[k];for(const m of ro.m)add(ro.f==='brood'?'B':ro.sid,(ro.f==='brood'?'brood:':'')+'garrison:'+ro.f,m.load)}
  for(const x of S.pjRuns||[])addM(x,sec,'pjrun',x.load);
  for(const x of S.crRuns||[])addM(x,sec,'crrun',x.load);
  if(S.surge)add('B','brood:surge',S.surge.store);
  add('ho','unbcamp',S.econ.unbCamp);
  if(S.bxm)add('B','brood:bxm',S.bxm);
  for(const m in S.corp||{}){const c=S.corp[m],h=mkHomeSid(m);add(h,'corp:'+m,c.store);if(c.rd&&c.rd.proto)add(h,'corpproto:'+m,c.rd.proto)}
  for(const f in S.corpFit||{})add(FAC_HOME(f),'corpfit:'+f,S.corpFit[f]);
  for(const k in S.aip||{})add(S.aip[k].sid||'?aip','aipkit',S.aip[k].kit);
  for(const I of(S.ind&&S.ind.list)||[]){addM(I,sec,'ind:hold',I.hold);addM(I,sec,'ind:kit',I.kit);try{addM(I,sec,'ind:sys',indSysInv(I))}catch(e){}}
  for(const n in S.brands||{}){const P2=S.brands[n]&&S.brands[n].rd;if(P2&&P2.proto)add('?brand','brandproto',P2.proto)}
  return{st,mob}};
T.total=function(sn){const t=Z();for(const k in sn.st)for(let i=0;i<6;i++)t[i]+=sn.st[k][i];for(const m of sn.mob)for(let i=0;i<6;i++)t[i]+=m.v[i];return t};
function hm0(f){try{return homeOf(f)}catch(e){return FAC_HOME(f)}}
function evLoc(ev){const t=ev.type;if(t==='offensive')return ev.trDone?ev.sector:(ev.staged||hm0(ev.att));
  if(t==='response'||t==='build')return ev.stage==='inbound'&&S.T<ev.eta&&!ev.trDone?(ev.from||hm0(ev.att)):ev.sector;
  if(t==='sortie'){if(ev.stage==='back'||ev.stage==='done'){const c=(S.frigates||[]).find(x=>x.id===ev.car);return c?c.sector:ev.from}return ev.stage==='gather'||ev.stage==='out'?ev.from:ev.to}
  if(ev.stage==='fly')return S.T<ev.eta?ev.from:ev.sector;
  return ev.sector||'?ev'}
const mass=v=>v[0]+v[1]+v[2]+v[3]+v[4]+v[5];
T.mark=function(name){
  T.inSnap=true;const t0=performance.now();let B;try{B=T.snap()}finally{T.inSnap=false}
  const A=T.last;T.snaps++;
  if(A){const ta=A.tot||(A.tot=T.total(A)),tb=B.tot=T.total(B);if(ta.some((x,i)=>Math.abs(x-tb[i])>1e-6)){if(name!=='updateEvents'){T.defer=(T.defer||0)+1;T.ms+=performance.now()-t0;return}T.leak=(T.leak||[]);if(T.leak.length<20)T.leak.push('T='+S.T+' '+tb.map((x,i)=>Math.round(x-ta[i])).join(','))}}
  T.last=B;
  if(A){
    // where each ship's hold is counted: where the ship is now (a hold that left one system and unloaded in the next), or, if that
    // shows a flow, where it was when the window opened (a hold loaded and then flown on): a flow is one only if both show it
    const calc=(old)=>{const was=old?new Map(A.mob.map(m=>[m.own,m.loc])):null,d={};const put=(key,v,s)=>{const a=d[key]||(d[key]=Z());for(let i=0;i<6;i++)a[i]+=s*v[i]};
      for(const k in B.st)put(k,B.st[k],1);for(const k in A.st)put(k,A.st[k],-1);
      for(const m of B.mob)put((old&&was.has(m.own)?was.get(m.own):m.fn(m.own))+'|'+m.lab,m.v,1);for(const m of A.mob)put((old?m.loc:m.fn(m.own))+'|'+m.lab,m.v,-1);
      const nb={};let dirty=false;for(const key in d){const v=d[key];if(!v.some(x=>Math.abs(x)>1e-6)){delete d[key];continue}dirty=true;const sid=key.split('|')[0];if(sid==='B'||sid==='N')continue;const a=nb[sid]||(nb[sid]=Z());for(let i=0;i<6;i++)a[i]+=v[i]}
    let mv=0;if(dirty){for(let i=0;i<6;i++){let p=0,n=0;for(const s in nb){const x=nb[s][i];if(x>1e-6)p+=x;else if(x<-1e-6)n-=x}mv+=Math.min(p,n)}
      }return{d,nb,mv}};
    let{d,nb,mv}=calc(false);if(mv>1e-6&&calc(true).mv<=1e-6)mv=0;
    {if(mv>1e-6){const rem={};for(const key in d){const[sid,lab]=key.split('|');if(sid==='B'||sid==='N'||lab==='debris'||lab.startsWith('cap:')||lab.startsWith('ev:sortie'))continue;const a=rem[sid]||(rem[sid]=Z());for(let i=0;i<6;i++)a[i]+=d[key][i]}let capOnly=true;for(const sid in rem)if(rem[sid].some(x=>Math.abs(x)>1e-6))capOnly=false;if(capOnly){T.capStrike=(T.capStrike||0)+mv;mv=0}}
      if(mv>1e-6){const G=T.agg[name]||(T.agg[name]={n:0,mass:0,sig:{}});G.n++;G.mass+=mv;
        const fr=[],to=[];let ex='';for(const key in d){const[sid,lab]=key.split('|');if(sid==='B'||sid==='N')continue;if(!nb[sid]||!nb[sid].some(x=>Math.abs(x)>1e-6))continue;const m=mass(d[key]);if(Math.abs(m)<1e-6&&!d[key].some(x=>Math.abs(x)>1e-6))continue;(m<0?fr:to).push(lab.replace(/^(trader:[^:]*:[^:]*:).*$/,'$1'));ex+=`${m<0?'':'+'}${Math.round(m)} ${lab}@${sid}; `}
        if(T.dbgN&&T.dbgN[name]&&(T.dbg[name]=T.dbg[name]||[]).length<6){let full='';for(const key in d)full+=key+':'+d[key].map(x=>Math.round(x)).join(',')+' ; ';T.dbg[name].push('T='+S.T+' stack='+T.stack.join('>')+' :: '+full)}const sig=[...new Set(fr)].sort().join(',')+' -> '+[...new Set(to)].sort().join(',');const g=G.sig[sig]||(G.sig[sig]={n:0,mass:0,ex:''});g.n++;g.mass+=mv;if(!g.ex)g.ex=`T=${Math.round(S.T)} `+ex}}}
  T.ms+=performance.now()-t0};
T.ver=0;T.sv=-1;T.SW={diffuse:1,driftSeed:1,richReplenish:1};T.dbg={};T.dbgN=null;T.P={takeFrom:1,toDebris:1,extract:1,craftDown:1,craftAbstract:1,regrow:1,diffuse:1,driftSeed:1,removeAst:1};
for(const k of Object.keys(inv)){if(typeof inv[k]!=='function')continue;const o=inv[k];inv[k]=function(){T.ver++;return o.apply(this,arguments)}}
T.w=function(name,o){const P=!!T.P[name];const w=function(){
  if(T.inSnap||!T.on)return o.apply(this,arguments);
  if(T.mode===1&&T.SW[name]){T.mark('(pre-'+name+')');try{return o.apply(this,arguments)}finally{T.inSnap=true;try{T.last=T.snap();T.last.tot=T.total(T.last)}finally{T.inSnap=false}T.ver++;T.sv=T.ver}}
  if(P)T.ver++;
  if(T.mode===0){T.cnt[name]=(T.cnt[name]||0)+1;return o.apply(this,arguments)}
  if(!T.C[name]){if(!P)return o.apply(this,arguments);try{return o.apply(this,arguments)}finally{T.ver++}}
  if(T.ver!==T.sv){T.sv=T.ver;T.mark(T.stack.length?T.stack[T.stack.length-1]:'(top)')}T.stack.push(name);
  try{return o.apply(this,arguments)}finally{if(P)T.ver++;T.stack.pop();if(T.ver!==T.sv){T.sv=T.ver;T.mark(name)}}};
  try{Object.assign(w,o)}catch(e){}return w};
return 1})()
