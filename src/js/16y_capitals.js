//@src 16y_capitals.js
// ============================================================ destroyers and the Ravager (Beyond, after stage 14)
// Driftgate 1 v255 removed its frigates, but their code paths survive wherever a capital isn't an escort or a carrier: the lance,
// the stand-off from a station, the line-ship orders (frigOrders), the hardest-hitting abstract fight. Beyond's destroyer is that
// line ship brought back (internal class 'frigate', shown as "destroyer"), with the approved models (Peregrine, Ironclad, Prism;
// the Brood's Gullet) and a charged main gun: it charges, and while it charges its shields are down. Two assault ships.
// The Unbound's carrier becomes the Ravager (approved model) and gains a charged main gun of its own; they build no sloops.
const DST={hull:4200,shield:2000,assault:2,cap:1,costK:1.5,timeK:1.5,seal:2,lvl:4,range:2600,
  gun:{charge:3,dmg:600,cd:4},maw:{charge:4,dmg:900,cd:7,len:2600,w:50},rav:{charge:3,dmg:500,cd:6},
  names:['Resolute','Tempest','Sentinel','Vindicator','Retribution','Thunderer','Valiant','Relentless','Indomitable','Reckoning'],
  mdl:{halcyon:'dz_peregrine',varkesh:'dz_ironclad',ostrova:'dz_prism',pirate:'dz_ravager'},
  dname:{halcyon:'Peregrine',varkesh:'Ironclad',ostrova:'Prism',brood:'Gullet'}};
CLASSES.frigate.name='Destroyer';CLASSES.frigate.desc='Capital ship: the line ship, built round a charged main gun.';
BROOD_MDL.frigate='b_gullet';
function isDst(t){return!!t&&t.cls==='frigate'}
function dstCost(f){const o={};for(const k in ESCORT_COST)if(k!=='missile')o[k]=Math.ceil(ESCORT_COST[k]*DST.costK);if(sealed(f))o.seal=DST.seal;return o}
function dstName(side){S.dstSeq=(S.dstSeq||0)+1;return DST.names[(S.dstSeq+FAC_IDS.indexOf(side)*3+DST.names.length)%DST.names.length]}
function makeDestroyer(side,sector,load,owner){const t={id:S.nextId++,side,sector,dest:null,cls:'frigate',hull:DST.hull,shield:side==='brood'?0:DST.shield,load,name:dstName(side),hold:0,aload:0};if(owner)t.owner=owner;
  S.frigates.push(t);capRefill(t);if(WORLDS[sector])inW(WORLDS[sector],()=>spawnFrigate(t,true));return t}
function facDst(f){return(S.frigates||[]).filter(t=>t.side===f&&isDst(t)&&(!t.owner||t.cmd))}
// Driftgate 1's save migration drops frigates from saves made before its capital rework: Beyond's saves are all after it
{const o=newGame;newGame=function(){const r=o.apply(this,arguments);if(S)S.capV=1;return r}}
// names
{const o=capName;capName=function(t){if(isDst(t))return'destroyer';if(t&&t.side==='pirate'&&isCar(t))return'Ravager';return o.apply(this,arguments)}}
{const o=broodCap;broodCap=function(t){if(isDst(t))return'Gullet';return o.apply(this,arguments)}}
{const o=capHullMax;capHullMax=function(t){if(isDst(t))return DST.hull;return o.apply(this,arguments)}}
// two assault ships aboard (none for the Brood), from the same stores as an escort's
{const o=capRefill;capRefill=function(t){const r=o.apply(this,arguments);if(!isDst(t))return r;const f=t.side==='player'?sideNorm('player'):t.side;if(f==='brood'||f==='pirate')return r;
  const own=carOwned(t),st=own&&S.pilots&&S.pilots[t.owner]?S.pilots[t.owner].vault:S.econ.stock[f];if(!st)return r;const srcs=own?[st]:[S.econ.fleet[f],st].filter(Boolean);
  t.aload=t.aload||0;while(t.aload<DST.assault&&takeFrom(ASSAULT_LD,srcs)){inv.addAll(t.load,ASSAULT_LD);t.aload++}return r}}
// in the world: the destroyer's shield, the Brood's none
{const o=spawnFrigate;spawnFrigate=function(t,arrive){const e=o.apply(this,arguments);if(e&&isDst(t)){const sc=t.side==='brood'?0:DST.shield;e.st={...e.st,sCap:sc};e.shield=Math.min(t.shield==null?sc:t.shield,sc)}return e}}
// models: each power's destroyer, the Brood's Gullet (through BROOD_MDL), the Ravager
function dstMdl(fac,cls){if(cls==='frigate'&&DST.mdl[fac]&&fac!=='pirate')return DST.mdl[fac];if(cls==='carrier'&&fac==='pirate')return DST.mdl.pirate;return null}
{const o=shipMesh;shipMesh=function(fac,cls){const m=dstMdl(fac,cls);if(m&&mdlHas(m)){const key='dst'+fac+cls;if(MESH[key])return MESH[key];const L=new GB();L.seg([0,0,0],[0,0,0],[0,0,0]);return MESH[key]={hull:mdlMesh(m,fac,1),rim:L.upload(true),eng:engFix(m).map(e=>e.slice()),mdl:true}}return o.apply(this,arguments)}}
// turrets on the models' own point-defence mounts (the Peregrine has eight: its middle pair stays bare, so six fire)
{const o=mdlFrigTurrets;mdlFrigTurrets=function(e){const m=e&&!e._mt&&MDL.ready&&e.side!=='brood'&&e.turrets&&dstMdl(e.side==='pirate'?'pirate':e.fac,e.cls);const M=m&&MDL.i[m];if(M&&M.tp&&M.tp.length){e._mt=1;let tp=M.tp;if(tp.length===8)tp=tp.filter((_,i)=>i!==1&&i!==5);
  const k=1.25/1.1;if(isDst(e.tok)&&e.turrets.length<tp.length)for(let i=e.turrets.length;i<tp.length;i++)e.turrets.push({p:[0,0,0],cool:rnd(.5)});e.turrets.forEach((tu,i)=>{const p=tp[i%tp.length];tu.p=[p[0]*k,p[1]*k,p[2]*k]});return}return o.apply(this,arguments)}}
// ---- the charged main gun (destroyers, the Ravager) and the Brood's Maw Cannon
function mgSpec(e){if(e.role!=='frigate'||!e.tok)return null;if(isDst(e.tok))return e.side==='brood'?DST.maw:DST.gun;if(isCar(e.tok)&&e.side==='pirate')return DST.rav;return null}
function mgNose(e){qRot(e.q,0,0,1,_f);const r=e.st.radius;return{x:e.x+_f.x*r*.95,y:e.y+_f.y*r*.95+r*.1,z:e.z+_f.z*r*.95}}
function mgShot(e,G,T){const n=mgNose(e),spd=900,lp=T.type==='ship'?leadPoint({x:n.x,y:n.y,z:n.z,vx:0,vy:0,vz:0},T,spd):T;let dx=lp.x-n.x,dy=lp.y-n.y,dz=lp.z-n.z;const l=hyp(dx,dy,dz)||1;dx/=l;dy/=l;dz/=l;
  W.shots.push(gfxShot(e,{x:n.x,y:n.y,z:n.z,vx:dx*spd,vy:dy*spd,vz:dz*spd,dmg:G.dmg,side:e.side,src:e,ttl:3.4,col:sideCol(e.side),sty:'capital',cap:true,mg:1}));if(!MUTE){fxBoom(n,60,'#ffe2b0');const v=vAt(e);if(v>.05)SFX.lance(Math.min(1,v*1.5))}
  qRot(e.q,0,0,1,_f);e.vx-=_f.x*8;e.vy-=_f.y*8;e.vz-=_f.z*8}
// the maw: a beam straight ahead, hitting every hostile ship, station and works it passes near
function segD(ax,ay,az,ux,uy,uz,L,p){const px=p.x-ax,py=p.y-ay,pz=p.z-az;const t=clamp(px*ux+py*uy+pz*uz,0,L);return hyp(px-ux*t,py-uy*t,pz-uz*t)}
function mawFire(e,G){const n=mgNose(e);qRot(e.q,0,0,1,_f);const ux=_f.x,uy=_f.y,uz=_f.z,L=G.len,ex=n.x+ux*L,ey=n.y+uy*L,ez=n.z+uz*L;let hits=0;
  for(const o of W.ents.slice()){if(o.type!=='ship'||!o.alive||o===e||!hostE(e.side,o))continue;if(o.isPlayer&&(S.player.docked||W.dead))continue;if(segD(n.x,n.y,n.z,ux,uy,uz,L,o)<G.w+o.st.radius){damageShip(o,G.dmg,e.side,{x:o.x,y:o.y,z:o.z,vx:ux,vy:uy,vz:uz,src:e},'capital');hits++;if(!MUTE)fxBoom(o,50,'#d9ff9a')}}
  const SE=W.stationEnt;if(SE&&hostile(e.side,SE.fac)&&(SE.shield>0&&!SE.offline?bubSeg(stBub(SE),n.x,n.y,n.z,ex,ey,ez,G.w)>=0:segD(n.x,n.y,n.z,ux,uy,uz,L,SE)<G.w+120)){damageStation(SE,G.dmg,e.side,'capital',e);hits++}
  const OE=W.outpostEnt;if(OE&&OE.o.owner&&!OE.o.breached&&hostile(e.side,OE.o.owner)&&(OE.o.shield>0?bubSeg(opBub(OE),n.x,n.y,n.z,ex,ey,ez,G.w)>=0:segD(n.x,n.y,n.z,ux,uy,uz,L,OE)<G.w+OE.r)){damageOutpost(OE,G.dmg,e.side);hits++}
  if(W.works&&W.works.length){const b={x:ex,y:ey,z:ez,vx:ux,vy:uy,vz:uz,dmg:G.dmg,side:e.side,src:e,cap:true};try{if(wkShot(b,n.x,n.y,n.z))hits++}catch(err){}}
  W.beams.push({src:e,x:ex,y:ey,z:ez,ttl:1.1,col:'#c8ff7a'});if(!MUTE){fxBoom(n,90,'#c8ff7a');const v=vAt(e);if(v>.05)SFX.lance(Math.min(1,v*1.6));W.shake=Math.max(W.shake||0,v*.6)}return hits}
function mgTick(e,G,dt,manual,C){const m=e.mg||(e.mg={cd:rnd(1,3),ch:0}),t=e.tok,lm=pmul(t,'lance'),brood=e.side==='brood'&&isDst(t);if(brood)e.shield=0;
  if(m.ch>0){e.shield=0;m.ch-=dt;if(!MUTE&&Math.random()<dt*10){const n=mgNose(e);fxSpark(n,brood?'#c8ff7a':'#ffe2b0',2)}
    if(m.ch<=0){if(brood)mawFire(e,G);else{const T=m.T;const ok=T&&(T.type==='ship'?T.alive&&W.ents.includes(T):T.type==='station'?W.stationEnt===T:T.type==='works'?W.works.includes(T):T.type==='outpost'?W.outpostEnt===T:true);mgShot(e,G,ok?T:(()=>{qRot(e.q,0,0,1,_f);return{x:e.x+_f.x*2400,y:e.y+_f.y*2400,z:e.z+_f.z*2400}})())}
      if(!brood)e.shield=Math.min(e.st.sCap,m.sh||0);m.cd=G.cd;m.T=null}return}
  if(m.cd>0){m.cd-=dt*lm;return}if(lm<=0)return;
  const T=e.lanceT,hold=C&&C.lanceMode==='hold';let go=null;
  if(manual){qRot(e.q,0,0,1,_f);go=T&&d3(T,e)<DST.range?T:{x:e.x+_f.x*2400,y:e.y+_f.y*2400,z:e.z+_f.z*2400}}
  else if(T&&!hold&&d3(T,e)<DST.range){if(brood){qRot(e.q,0,0,1,_f);const dx=T.x-e.x,dy=T.y-e.y,dz=T.z-e.z,l=hyp(dx,dy,dz)||1;if((dx*_f.x+dy*_f.y+dz*_f.z)/l>.97)go=T}else go=T}
  if(!go)return;m.ch=G.charge;m.T=go;m.sh=e.shield;e.shield=0;if(!MUTE&&W.player&&d3(e,W.player)<3000)fxBoom(mgNose(e),30,brood?'#c8ff7a':'#ffe2b0')}
{const o=frigateThink;frigateThink=function(e,dt){const G=mgSpec(e);if(!G||NET.cl)return o.apply(this,arguments);const t=e.tok,C=t&&fOwn(t)?fctl(t):null,manual=!!(C&&C.fire);if(C)C.fire=0;if(isDst(t))e.lanceCd=99;
  o.apply(this,arguments);if(!e.alive||e.role!=='frigate'||!t||!S.frigates.includes(t)||t.dummy||jamDark(e))return;
  // the Gullet turns its whole body onto its target to bring the maw to bear
  if(e.side==='brood'&&isDst(t)&&e.lanceT&&!(e.mg&&e.mg.ch>0))faceTo(e,e.lanceT,dt);
  mgTick(e,G,dt,manual,C);if(isDst(t)){t.shield=e.shield;e.lanceCd=e.mg.ch>0?e.mg.ch:Math.max(0,e.mg.cd)}}}
// the bridge's weapons console describes the main gun (it reads the time to the next shot from lanceCd)
{const o=renderConsole;renderConsole=function(full){const r=o.apply(this,arguments);try{const B=W&&W.bridge,t=B&&B.f&&B.f.tok;if(B&&B.panel==='wpn'&&isDst(t)){const h=[...$('fcBody').querySelectorAll('.h3')].find(x=>x.textContent==='Capital battery');if(h){h.textContent='Main gun';const n=h.nextElementSibling;const ch=B.f.mg&&B.f.mg.ch>0;if(n)n.innerHTML=`A charged shot that cracks station, depot, outpost and capital-ship hulls (${DST.gun.dmg} a hit). It charges for ${DST.gun.charge} s before each shot, and <b>while it charges your shields are down</b>. Range 2.6 km, ${DST.gun.cd} s to reload at full power.${ch?' <b class="amber">Charging: shields down.</b>':''}`}}}catch(err){}return r}}
// ---- who builds them: one per power (and the Brood), at the capital yard, once the yard is up
{const o=capitalTick;capitalTick=function(){const r=o.apply(this,arguments);try{dstTick()}catch(err){console.error(err)}return r}}
function dstTick(){if(NET.cl||!S||S.training)return;const T=S.T;
  for(const f of[...FAC_IDS,'brood']){const st=S.econ.stock[f];if(!st||!S.yards[f])continue;const busy=S.events.some(e=>e.type==='dstbuild'&&e.att===f&&e.stage!=='done');if(busy||facDst(f).length>=DST.cap)continue;
    const war=S.ai[f]&&S.ai[f].war>T,C=dstCost(f),time=ESCORT_TIME*DST.timeK;if(!capGateOK(f,time)||(f==='brood'&&T<=BAL.brLevT))continue;
    const both={...carCostF(f)};for(const k in C)both[k]=(both[k]||0)+C[k];if(!(facCar(f).length>=1||haveIn(both,[st])||!haveIn(carCostF(f),[st])))continue;
    if(!haveIn(C,[st])||Math.random()>=(war?.6:.25))continue;const force={};takeFrom(C,[st]);inv.addAll(force,C);S.events.push({id:S.nextId++,type:'dstbuild',t0:T,yard:f,att:f,sector:S.yards[f].sector,force,until:T+time*(war?.7:1),stage:'building'})}
  for(const ev of S.events){if(ev.type!=='dstbuild'||ev.stage==='done'||T<ev.until)continue;ev.stage='done';const evp=ykPid(ev.att);
    if(evp){const P=S.pilots&&S.pilots[evp];if(P){const t=makeDestroyer(P.sworn||P.faction,ev.sector,ev.force,evp);feedTo(evp,`Destroyer ${t.name} has launched from ${DEF[ev.sector].name}. Order it from the galaxy map (M).`,'good')}else inv.addAll(S.econ.stock[sideNorm('player')],ev.force);ev.force={};continue}
    const t=makeDestroyer(ev.att,ev.sector,ev.force);ev.force={};
    if(ev.att==='player')feed(`Destroyer ${t.name} has launched from ${DEF[ev.sector].name}. Order it from the galaxy map (M).`,'good');
    else if(friendSide(ev.att)||covered(ev.sector))feed(ev.att==='brood'?`⚠ A Brood Gullet has been grown at ${DEF[ev.sector].name}.`:`${FACTIONS[ev.att].short} destroyer ${t.name} has launched at ${DEF[ev.sector].name}.`,ev.att==='brood'?'bad':friendSide(ev.att)?'good':'warn')}}
// ---- your own: a level 4 Station with a shipyard lays one down
{const o=capBuild;capBuild=function(P,R,kind){if(kind!=='dst')return o.apply(this,arguments);if(!isPSta(R)||!hasB(R,'yard'))return'Capital ships need your station\'s shipyard.';if(staLvl(R)<DST.lvl)return`A Destroyer needs a level ${DST.lvl} station.`;
  const k=yardKeyOf(R),cost=dstCost('player'),srcs=[P.cargo,R.stock];if(S.events.some(e=>e.type==='dstbuild'&&e.att===k&&e.stage!=='done'))return'A Destroyer is already in the slip.';
  if(S.frigates.filter(t=>fMine(t)&&isDst(t)).length>=DST.cap)return'You can keep one Destroyer.';if(!haveIn(cost,srcs))return`It needs ${lackText(cost,Object.assign({},R.stock,P.cargo))}.`;
  S.yards[k]=S.yards[k]||{sector:R.sid,fort:{},pst:R.sid};const force={};takeFrom(cost,srcs);inv.addAll(force,cost);
  S.events.push({id:S.nextId++,type:'dstbuild',t0:S.T,yard:k,att:k,sector:R.sid,force,until:S.T+ESCORT_TIME*DST.timeK,stage:'building'});return`✓ A Destroyer is laid down in your slip at ${R.name}.`}}
{const o=holdingsHtml;holdingsHtml=function(P){let h=o.apply(this,arguments);try{P=P||S.player;for(const R of myStations(P)){if(!hasB(R,'yard'))continue;const ok=staLvl(R)>=DST.lvl&&haveIn(dstCost('player'),[P.cargo,R.stock]),sl=S.events.find(e=>e.type==='dstbuild'&&e.att===yardKeyOf(R)&&e.stage==='building');
  const btn=`<button class="btn sm" type="button" data-co="capbld" data-arg="${R.sid}:dst" ${ok?'':'disabled'}>Destroyer (level ${DST.lvl})</button>${sl?`<span class="note">Destroyer in the slip: ${fmtT(Math.max(0,sl.until-S.T))}</span>`:''}`;
  const mk=`data-arg="${R.sid}:car"`,i=h.indexOf(mk);if(i<0)continue;const j=h.indexOf('</button>',i)+9;h=h.slice(0,j)+btn+h.slice(j)}}catch(err){console.error(err)}return h}}
