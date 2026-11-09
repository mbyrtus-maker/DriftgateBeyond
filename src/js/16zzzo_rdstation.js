//@src 16zzzo_rdstation.js
// ============================================================ Beyond: the makers' R&D stations in space (decided 6–7 Nov 2026; built 9 Nov 2026)
// BEYOND_DESIGN.md, "A maker's R&D station" and "Ore requests, Riftstone, and the black market's ...". Each maker keeps a
// small station of its own in its home system, RDS_G.dist from the host station on its own side of it, not dockable, drawn
// by 16zzzn_rdsdraw.js (a lab in a socket for each product line it has taken through R&D, at its grade; its current
// project's lab too). No shields (the user, 9 Nov 2026): it is defended by its two turret mounts, its own security wing
// (launched when it is attacked) and the host's garrison (a distress call; a contractor who fires on it is fair game for the
// host's ships for a minute). It is a grey area, not a crime: no standing is lost.
//   Systems: the control centre (cc), a lab per socket, two turrets. Shots and lasers hit the system they pass through.
//   A lab disabled: the project it is developing loses RDS_G.labDelay seconds (once each time it goes down).
//   The control centre disabled: the station goes offline for RDS_G.offT. Offline, the maker's sales go into an escrow wallet
//     (paid over when it comes back), its R&D clock stops and it makes no tweaks. Kept offline RDS_G.ceoT in one stretch, its
//     board replaces the CEO.
//   Repairs: a system untouched for 90 s mends 5% every 10 s; the control centre comes back with the station.
//   Black market: spying (a limpet on a rival's R&D station: the client's next trial +20%, user 9 Nov 2026) and sabotage
//   (disable the lab of a rival's current project) are posted by a rival while a maker runs a project (16zzzm_bmops.js).
// Host only for damage and effects; every page builds the entities from S.rds. Credits only move: the ledger stays exact.
const RDS_G={dist:4500,hp:{cc:1600,lab:700,tur:450},labDelay:600,offT:600,ceoT:7200,secN:3,secCls:'interceptor',secCool:300,aggro:60,tur:{range:1800,cool:.9,dmg:9,spd:900},spy:.2,pay:{spy:3000,sab:4000},hitR:{cc:12,lab:11,tur:7}};
function rdsAll(){return S.rds=S.rds||{}}
function rdsOf(m){return rdsAll()[m]||null}
function rdsHost(m){return S.stations[mkHomeSid(m)]||null}
function rdsHostSide(m){const R=rdsHost(m);return R?(R.owner==='neutral'?'neutral':R.owner):'neutral'}
// where it stands: on its own side of the host station, clear of the gates
function rdsPlace(m){const sid=mkHomeSid(m),R=S.stations[sid];if(!R)return null;const mates=Object.keys(MAKERS).filter(x=>mkHomeSid(x)===sid).sort(),i=Math.max(0,mates.indexOf(m));
  let h=0;for(const ch of sid)h=(h*31+ch.charCodeAt(0))%997;let a=h/997*TAU+i*Math.PI;
  for(let k=0;k<12;k++){const x=R.x+Math.cos(a)*RDS_G.dist,z=R.z+Math.sin(a)*RDS_G.dist;if((GATES[sid]||[]).every(g=>hyp(g.x-x,g.y-(R.y||0),g.z-z)>2000))return{sid,x:Math.round(x),y:Math.round((R.y||0)+180),z:Math.round(z)};a+=.45}
  return{sid,x:Math.round(R.x+Math.cos(a)*RDS_G.dist),y:Math.round((R.y||0)+180),z:Math.round(R.z+Math.sin(a)*RDS_G.dist)}}
function rdsInit(){if(NET.cl||!S||!S.corp)return;const A=rdsAll();for(const m in MAKERS){const c=ceOf(m);if(!c)continue;const pl=rdsPlace(m);if(!pl)continue;const D=A[m];
  if(!D||D.sid!==pl.sid)A[m]={...pl,hp:{},off:0,offStart:0,hit:-1e9,sec:-1e9,esc:0,labDown:{}}}}
// the labs: each line taken through R&D (and the current project's line), highest grade first, up to four sockets
function rdsLabs(m){const c=ceOf(m);if(!c)return{ids:[],g:[0,0,0,0]};const L=[];for(const id of MK_LINE[m]||[]){const g=Math.max((c.g&&c.g[id])||1,c.rd&&c.rd.id===id?c.rd.g:0);if(g>=2)L.push({id,g})}
  L.sort((a,b)=>(c.rd&&b.id===c.rd.id)-(c.rd&&a.id===c.rd.id)||b.g-a.g);const out=L.slice(0,4);return{ids:out.map(x=>x.id),g:[0,1,2,3].map(i=>out[i]?out[i].g:0)}}
function rdsKeys(m){const L=rdsLabs(m),k=[{k:'cc',i:0}];L.g.forEach((g,i)=>{if(g)k.push({k:'lab',i})});k.push({k:'tur',i:0},{k:'tur',i:1});return k}
function rdsHp(D,k,i){const v=D.hp[k+i];return v===undefined?RDS_G.hp[k]:v}
function rdsName(m,k,i){if(k==='cc')return'Control centre';if(k==='tur')return`Turret mount ${i+1}`;const L=rdsLabs(m),id=L.ids[i];return id?`${ITEMS[rdGid(id,L.g[i])]?ITEMS[rdGid(id,L.g[i])].name:ITEMS[id].name} lab`:`Lab ${i+1}`}
function rdsOffline(m){const D=rdsOf(m);return!!(D&&D.off&&S.T<D.off)}
// ---- the entities: every page builds them from S.rds (like the station works)
function rdsSync(){if(!W||!S||!S.rds)return;const want=[];for(const m in S.rds){const D=S.rds[m];if(D.sid===W.sid&&ceAlive(m))want.push(m)}
  for(const e of W.ents.slice())if(e.type==='rds'&&!want.includes(e.m)){W.ents.splice(W.ents.indexOf(e),1);if(W.tgt&&W.tgt.ref===e)W.tgt=null}
  for(const m of want){const D=S.rds[m];let e=W.ents.find(x=>x.type==='rds'&&x.m===m);if(!e){e={type:'rds',m,x:D.x,y:D.y,z:D.z,q:qAxis(0,1,0,(D.x*7+D.z*3)%TAU,q0()),lastHit:-99,alive:true};W.ents.push(e)}
    const L=rdsLabs(m);e.labs=L.g.map((g,i)=>D.labDown&&D.labDown[i]?Math.max(2,g):g);e.offline=rdsOffline(m);e.name=`${MAKERS[m].name} R&D station`;e.fac=rdsHostSide(m);const P=rdsPoints(m);e.r=P?P.r:50}}
{const o=worldUpdate;worldUpdate=function(dt){const r=o.apply(this,arguments);try{rdsSync();if(!NET.cl)rdsLive(dt)}catch(e){console.error(e)}return r}}
{const o=strategicTick;strategicTick=function(){const r=o.apply(this,arguments);try{rdsInit();rdsTick()}catch(e){console.error(e)}return r}}
// ---- its systems in the world
function rdsSubPts(e){const P=rdsPoints(e.m);if(!P)return[];const D=rdsOf(e.m),out=[],L=rdsLabs(e.m);if(!D)return out;
  out.push({k:'cc',i:0,...rdsAt(e,P.cc),r:RDS_G.hitR.cc});L.g.forEach((g,i)=>{if(g&&P.sockets[i])out.push({k:'lab',i,...rdsAt(e,P.sockets[i].c),r:RDS_G.hitR.lab})});P.tp.forEach((p,i)=>out.push({k:'tur',i,...rdsAt(e,p),r:RDS_G.hitR.tur}));return out}
function rdsRay(e,ox,oy,oz,dx,dy,dz,L){const D=rdsOf(e.m);if(!D)return null;let best=null,bt=L;for(const s of rdsSubPts(e)){if(rdsHp(D,s.k,s.i)<=0)continue;const lx=s.x-ox,ly=s.y-oy,lz=s.z-oz,t=lx*dx+ly*dy+lz*dz;if(t<0||t>=bt)continue;const d2=lx*lx+ly*ly+lz*lz-t*t;if(d2>s.r*s.r)continue;bt=t;best=s}return best?Object.assign(best,{t:bt}):null}
function rdsPilotOf(src){if(!src)return null;if(src.isPlayer)return S.player;if(src.rp)return S.pilots&&S.pilots[src.rp]||null;return null}
function rdsDamage(e,s,dmg,side,src){if(NET.cl||!(dmg>0))return;const m=e.m,D=rdsOf(m);if(!D)return;const hs=rdsHostSide(m);if(side===hs)return;const k=s.k+s.i,mx=RDS_G.hp[s.k],was=rdsHp(D,s.k,s.i),v=Math.max(0,was-dmg);D.hp[k]=v;D.hit=S.T;e.lastHit=W.t;fxSpark(s,'#ffd9a0',2);
  const P=rdsPilotOf(src),key=P?pkeyOf(P):null;if(P&&!P.sworn)(P.aggro||(P.aggro={}))[hs]=S.T+RDS_G.aggro;D.by=key||D.by;D.byT=S.T;
  // the host's garrison answers, and the maker's own security launches
  if(S.T-(D.dist||-1e9)>30){D.dist=S.T;const R=rdsHost(m);try{if(R&&hs!=='neutral')distressCall(W.sid,e.name,hs,P?(P.sworn||'player'):side)}catch(x){}}
  if(S.T-D.sec>RDS_G.secCool){D.sec=S.T;rdsSecurity(e,hs)}
  const nm=rdsName(m,s.k,s.i);if(was>0&&v<=0){fxBoom(s,26,'#ffb070');if(src)subTell(src,`${e.name}: ${nm} disabled.`);rdsDown(m,s.k,s.i,key)}else if(was>=mx*.5&&v<mx*.5&&src)subTell(src,`${e.name}: ${nm} damaged.`)}
function rdsSecurity(e,side){const n=RDS_G.secN;for(let i=0;i<n;i++){const s=makeNPC('patrol',side,RDS_G.secCls,2,{},'rdsec:'+e.m);const o=rdir(1);s.x=e.x+o.x*120;s.y=e.y+o.y*60;s.z=e.z+o.z*120;s.pname=`${MAKERS[e.m].short} security`;s.ai.retireAt=W.t+300;W.ents.push(s)}
  if(W===LW)feed(`⚠ ${MAKERS[e.m].short} security launches from its R&D station.`,'warn')}
// a system goes down
function rdsDown(m,k,i,by){const D=rdsOf(m),c=ceOf(m);if(!D||!c)return;
  if(k==='lab'){const L=rdsLabs(m),id=L.ids[i];D.labDown=D.labDown||{};D.labDown[i]=1;if(c.rd&&id===c.rd.id&&c.rd.until<1e9){c.rd.until+=RDS_G.labDelay;ceNews(m,`'s R&D station was attacked: the ${rdsName(m,k,i)} is down, and the project loses ${Math.round(RDS_G.labDelay/60)} minutes.`)}
    for(const x of bmoAll())if(x.k==='sab'&&x.tgt===m&&x.taker&&by&&(x.taker===by||(isMe(x.taker)&&isMe(by)))&&c.rd&&id===c.rd.id){const P=xPilotOfKey(by);const got=bmoPay(x,by,P);bmoHeat(P,rdsHostSide(m),'Heavy','sabotage');keyFeed(by,`🧨 Sabotage done: ${bmoClientName(x.by)} pays +${fmt(got)} cr.`,'good');break}}
  if(k==='cc'){if(!rdsOffline(m)){D.offStart=D.offStart&&S.T-D.off<60?D.offStart:S.T}D.off=S.T+RDS_G.offT;ceNews(m,`'s R&D station is offline: its control centre was knocked out. Its sales are held in escrow until it comes back.`,true)}}
// ---- the host: turrets, repairs, coming back online, the escrow, a CEO lost to a long outage
function rdsLive(dt){if(!W)return;for(const e of W.ents){if(e.type!=='rds')continue;const D=rdsOf(e.m);if(!D)continue;e.tc=(e.tc||0)-dt;if(e.tc>0)continue;e.tc=RDS_G.tur.cool;
    const hs=rdsHostSide(e.m),P=rdsPoints(e.m);if(!P)continue;P.tp.forEach((p,i)=>{if(rdsHp(D,'tur',i)<=0)return;const at=rdsAt(e,p);let best=null,bd=RDS_G.tur.range;
      for(const o of W.ents){if(o.type!=='ship'||!o.alive)continue;if(o.isPlayer&&(S.player.docked||W.dead))continue;if(!hostE(hs,o))continue;const d=d3(o,at);if(d<bd){bd=d;best=o}}
      if(best)turretShot(at,best,RDS_G.tur.spd,RDS_G.tur.dmg,hs,8)})}}
function rdsTick(){if(NET.cl||!S||!S.rds)return;for(const m in S.rds){const D=S.rds[m],c=ceOf(m);if(!c||c.dead)continue;
    if(S.T-D.hit>90)for(const k in D.hp){const kk=k.replace(/\d+$/,''),mx=RDS_G.hp[kk];if(kk==='cc'&&rdsOffline(m))continue;D.hp[k]=Math.min(mx,D.hp[k]+mx*.05);if(D.hp[k]>=mx){delete D.hp[k];if(kk==='lab'&&D.labDown)delete D.labDown[k.slice(3)]}}
    if(D.off&&S.T>=D.off){D.off=0;D.offStart=0;delete D.hp.cc0;const w='rdsx_'+m,x=S.econ.treasury[w]||0;if(x>0)transfer(w,ceW(m),x);ceNews(m,`'s R&D station is back online${x>0?`; ${fmt(x)} cr held in escrow reaches the company`:''}.`)}
    if(rdsOffline(m)){if(c.rd&&c.rd.until<1e9)c.rd.until+=10;if(D.offStart&&S.T-D.offStart>=RDS_G.ceoT){const old=c.ceo;c.ceo=pick(CE.ceos.filter(z=>z!==old));c.ceoT=S.T;D.offStart=S.T;ceNews(m,`'s board replaces its CEO after two hours with the R&D station offline (now ${c.ceo}).`,true)}}}}
// offline: sales go into escrow; no tweaks
{const o=ceSale;ceSale=function(m){if(!rdsOffline(m))return o.apply(this,arguments);const t0=ceT(m);const r=o.apply(this,arguments);const d=ceT(m)-t0;if(d>0)transfer(ceW(m),'rdsx_'+m,d);return r}}
{const o=ceTweak;ceTweak=function(m){if(rdsOffline(m))return false;return o.apply(this,arguments)}}
// ---- weapons: kinetic shots (tested before anything else in the shot's path) and lasers
{const o=subShot;subShot=function(b,ox,oy,oz){if(!NET.cl&&W&&!b.jam){for(const e of W.ents){if(e.type!=='rds'||b.side===rdsHostSide(e.m))continue;if(!segHit(ox,oy,oz,b.x,b.y,b.z,e,(e.r||50)+10))continue;
      const sx=b.x-ox,sy=b.y-oy,sz=b.z-oz,sl=hyp(sx,sy,sz)||1,s=rdsRay(e,ox,oy,oz,sx/sl,sy/sl,sz/sl,sl+(e.r||50)*2);if(s){rdsDamage(e,s,b.dmg,b.side,b.src);return true}
      if(segHit(ox,oy,oz,b.x,b.y,b.z,e,(e.r||50)*.45)){fxSpark(b,'#c8c0b0',2);e.lastHit=W.t;return true}}}return o.apply(this,arguments)}}
let RDS_FIRE=null;
{const o=fireLaser;fireLaser=function(e){RDS_FIRE=e;try{return o.apply(this,arguments)}finally{RDS_FIRE=null}}}
{const o=laserRay;laserRay=function(e,range){const r=o.apply(this,arguments);try{if(!W||RDS_FIRE!==e||NET.cl)return r;qRot(e.q,0,0,1,_f);const fx=_f.x,fy=_f.y,fz=_f.z,R0=e.st.radius,ox=e.x+fx*R0,oy=e.y+fy*R0,oz=e.z+fz*R0;
    for(const E of W.ents){if(E.type!=='rds'||e.side===rdsHostSide(E.m))continue;const s=rdsRay(E,ox,oy,oz,fx,fy,fz,Math.min(range,r.d||range));if(!s)continue;rdsDamage(E,s,e.st.dmg*.5,e.side,e);return{hit:{kind:'block'},x:s.x,y:s.y,z:s.z,d:s.t}}}catch(err){console.error(err)}return r}}
// ---- targeting and the target panel
{const o=targetables;targetables=function(){const out=o.apply(this,arguments);try{for(const e of W.ents)if(e.type==='rds')out.push({kind:'rds',ref:e})}catch(e){}return out}}
{const o=validTgt;validTgt=function(t){if(t&&t.kind==='rds')return!!(W&&W.ents.includes(t.ref));return o.apply(this,arguments)}}
function rdsTgtHtml(e,dist){const m=e.m,D=rdsOf(m);if(!D)return'';const rows=rdsKeys(m).map(s=>{const hp=rdsHp(D,s.k,s.i),mx=RDS_G.hp[s.k];return`<div class="row">${esc(rdsName(m,s.k,s.i))}<b style="color:${hp<=0?'var(--danger)':hp<mx*.5?'var(--amber)':'inherit'}">${hp<=0?'DOWN':Math.round(hp/mx*100)+'%'}</b></div>`}).join('');
  return`<div class="tp"><div class="tn" style="color:${MK_ACC[m]||sideCol(e.fac)}">${esc(e.name)}</div><div class="ts">${esc(sideName(e.fac))} space · no shields${rdsOffline(m)?' · <b style="color:var(--amber)">OFFLINE</b>':''}${ceOf(m)&&ceOf(m).rd?` · developing the ${esc(ITEMS[rdGid(ceOf(m).rd.id,ceOf(m).rd.g)].name)}`:''}</div>${rows}<div class="row">Range<b>${fmt(dist)} m</b></div></div>`}
// ---- spying: a scout's limpet on a rival's R&D station
{const o=limpetTarget;limpetTarget=function(){const r=o.apply(this,arguments);if(r)return r;try{const t=W&&W.tgt;if(!t||t.kind!=='rds'||!isScoutCls(S.player.cls))return null;const e=t.ref,me=pkeyOf(S.player);
    if(!bmoAll().some(x=>x.k==='spy'&&x.tgt===e.m&&x.taker&&(x.taker===me||(isMe(x.taker)&&isMe(me)))))return null;return e}catch(err){return null}}}
{const o=limpetPlant;limpetPlant=function(E,f,by,at){if(!E||E.type!=='rds')return o.apply(this,arguments);const m=E.m,x=bmoAll().find(y=>y.k==='spy'&&y.tgt===m&&y.taker&&by&&(y.taker===by||(isMe(y.taker)&&isMe(by))));if(!x)return false;
  const P=xPilotOfKey(by),cm=x.by.slice(5),cc=ceOf(cm);if(cc)cc.spy=(cc.spy||0)+RDS_G.spy;const got=bmoPay(x,by,P);bmoHeat(P,rdsHostSide(m),'Light','spying');
  keyFeed(by,`🧲 Limpet on ${E.name}: ${MAKERS[cm].short} reads ${MAKERS[m].short}'s R&D (its next trial +${Math.round(RDS_G.spy*100)}%). +${fmt(got)} cr.`,'good');ceNews(m,`found a spy limpet on its R&D station.`);return true}}
{const o=rdWinChance;rdWinChance=function(m,P){return Math.min(.95,o.apply(this,arguments)+((ceOf(m)||{}).spy||0))}}
{const o=rdLaunch;rdLaunch=function(m){const c=ceOf(m);const r=o.apply(this,arguments);if(c&&c.spy&&!NET.cl)c.spy=0;return r}}
// ---- the black market: spying and sabotage contracts (a rival posts them while a maker runs a project)
{const o=bmoTick;bmoTick=function(){const due=!NET.cl&&S&&!S.training&&!S.unb&&S.econ&&S.T>=(S.bmoT||0);const r=o.apply(this,arguments);try{if(!due)return r;const L=bmoAll(),T=S.T;
    for(let i=L.length-1;i>=0;i--){const x=L[i];if((x.k==='spy'||x.k==='sab')&&(!ceAlive(x.tgt)||!(ceOf(x.tgt)||{}).rd||!rdsOf(x.tgt)))L.splice(i,1)}
    for(const m in MAKERS){const c=ceOf(m);if(!ceAlive(m)||!c.rd||!rdsOf(m))continue;for(const k of['spy','sab']){if(L.some(x=>x.k===k&&x.tgt===m))continue;const rv=bmoRival(m);if(!rv||ceT(rv)<RDS_G.pay[k])continue;
      L.push({id:S.nextId++,k,by:'corp_'+rv,tgt:m,pay:RDS_G.pay[k],T0:T,until:T+BMO.life,taker:null})}}}catch(e){console.error(e)}return r}}
{const o=bmoTake;bmoTake=function(P,id){const x=bmoAll().find(y=>String(y.id)===String(id));if(!x||(x.k!=='spy'&&x.k!=='sab'))return o.apply(this,arguments);if(x.taker&&!bmoKeyOk(x.taker,P))return'Someone else has taken it.';x.taker=pkeyOf(P);
  const D=rdsOf(x.tgt);if(D&&D.sid!==P.sector)P.route=D.sid;return x.k==='spy'?`✓ Contract taken: plant a limpet on ${MAKERS[x.tgt].name}'s R&D station in ${DEF[D.sid].name} (a scout: target it, hold the limpet key within 600 m). ${bmoClientName(x.by)} pays ${fmt(x.pay)} cr.`:`✓ Contract taken: knock out the lab of ${MAKERS[x.tgt].name}'s current project at its R&D station in ${DEF[D.sid].name}. ${bmoClientName(x.by)} pays ${fmt(x.pay)} cr. Its security and ${sideName(rdsHostSide(x.tgt))}'s garrison will come for you.`}}
{const o=jobsList;jobsList=function(c,P,srcs){const out=o.apply(this,arguments);try{if(S.unb||!c||c.kind!=='station')return out;const hop=sid=>sid&&HOP[P.sector]&&HOP[P.sector][sid]!=null?HOP[P.sector][sid]:0,far=n=>n?`${n} jump${n>1?'s':''}`:'here';
  for(const x of bmoAll()){if(x.k!=='spy'&&x.k!=='sab')continue;const mine=x.taker&&bmoKeyOk(x.taker,P);if(x.taker&&!mine)continue;const D=rdsOf(x.tgt),cr=ceOf(x.tgt);if(!D||!cr||!cr.rd)continue;const h=hop(D.sid),hs=rdsHostSide(x.tgt),proj=ITEMS[rdGid(cr.rd.id,cr.rd.g)];
    const title=x.k==='spy'?`Spy on ${esc(MAKERS[x.tgt].short)}'s R&D`:`Sabotage ${esc(MAKERS[x.tgt].short)}'s R&D`,sub=`for ${esc(bmoClientName(x.by))} · R&D station in ${esc(DEF[D.sid].name)} · ${x.k==='spy'?'a scout and a limpet · Light heat':'knock out the project\'s lab · Heavy heat'}`;
    out.push({id:'bk:'+x.id,bm:1,by:x.by,sid:D.sid,ty:x.k==='spy'?'scout':'fight',title,sub:mine?`your contract · ${sub}`:sub,hops:h,where:far(h),payN:x.pay,pay:`${fmt(x.pay)} cr`,btn:mine?(D.sid!==P.sector?['croute',D.sid,'Set course']:null):['bmotake',x.id,'Take the contract'],
      detail:()=>`<p class="note" style="margin:0">${esc(MAKERS[x.tgt].name)} is developing the ${esc(proj?proj.name:'a new grade')} at its R&D station, ${fmt(RDS_G.dist/1000)} km from the ${esc(sideName(hs))} station in ${esc(DEF[D.sid].name)}. ${x.k==='spy'?`Fly a scout to it, target it and hold the limpet key within 600 m. ${esc(bmoClientName(x.by))} learns from the work: its next trial is ${Math.round(RDS_G.spy*100)}% likelier to succeed.`:`It has no shields. Knock out the lab for that project (target the station: the panel shows its systems; shots hit what they pass through). The project loses ${Math.round(RDS_G.labDelay/60)} minutes. Its two turrets, its security wing and ${esc(sideName(hs))}'s garrison defend it.`}</p>`})}}catch(err){console.error(err)}return out}}
