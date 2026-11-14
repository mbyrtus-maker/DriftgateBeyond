//@src 16zs_start2.js
// ============================================================ the title screen (Beyond screens pass, 3 Nov 2026)
// Two columns. Left: the title, then the steps in order: 1 Callsign; 2 Legend (collapsed: your level and start package,
// opening to the perk choices and any Conqueror's spoils); 3 Freeport, 4 Role and 5 Ship (open: each header shows what's
// picked and folds its cards away; Ship offers only the hulls you can start in); then Play with friends and the controls line. Right: a picture of the freeport you
// picked and the ship you picked (the station's and the ship's real models, drawn by the start screen's small renderer),
// with their names, turning slowly. Nothing else changes: the same cards, buttons and ids, so the start code and its tests still work.
let stOpen={legend:false,port:true,role:true,ship:true};
// the picture moves (user, 7 Nov 2026): the station turns slowly (its ring faster), the ship sways and bobs; about 30 frames
// a second while the title screen is up (fewer on a slow machine: a frame never takes more than a third of the time), still
// for anyone who asks for reduced motion
let stT=0,stAnimLast=0,stAnimGap=33;
function stAnim(ts){const st=$('start');if(!st||st.hidden||document.hidden){setTimeout(()=>requestAnimationFrame(stAnim),500);return}
  if(ts-stAnimLast>=stAnimGap){stAnimLast=ts;const t0=performance.now();try{stPic(ts/1000)}catch(e){}const dt=performance.now()-t0;stAnimGap=Math.max(33,Math.min(200,dt*3))}requestAnimationFrame(stAnim)}
try{if(!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches))requestAnimationFrame(stAnim)}catch(e){}
function stDraw(c,d,q,cx,cy,s,dim){const Ld=[.35,.55,.76],tris=[],v={x:0,y:0,z:0},n={x:0,y:0,z:0};
  for(let i=0;i<d.length;i+=30){qRot(q,d[i+3],d[i+4],d[i+5],n);if(n.z<=.02)continue;const P=[];let z=0;for(let k=0;k<3;k++){const o=i+k*10;qRot(q,d[o],d[o+1],d[o+2],v);P.push(cx+v.x*s,cy-v.y*s);z+=v.z}
    const lit=.3+.85*Math.max(0,n.x*Ld[0]+n.y*Ld[1]+n.z*Ld[2]),em=d[i+9],f=k=>Math.min(255,Math.round(255*d[i+6+k]*(lit*(1-em)+em)*(dim||1)));tris.push([z,P,`rgb(${f(0)},${f(1)},${f(2)})`])}
  tris.sort((a,b)=>a[0]-b[0]);c.lineJoin='round';c.lineWidth=.6;for(const[,P,col]of tris){c.fillStyle=col;c.strokeStyle=col;c.beginPath();c.moveTo(P[0],P[1]);c.lineTo(P[2],P[3]);c.lineTo(P[4],P[5]);c.closePath();c.fill();c.stroke()}}
function stR(d){let m=1;for(let i=0;i<d.length;i+=10)m=Math.max(m,Math.hypot(d[i],d[i+1],d[i+2]));return m}
const ST_Q=(()=>{const A=(x,y,z,a)=>qAxis(x,y,z,a,q0());return qMul(A(1,0,0,.42),A(0,1,0,.7),q0())})();
// the ship's show on the title picture: which way it is turned t seconds in. Each axis gets ST_SHOW.turn s for one full
// turn (eased), then ST_SHOW.rest s still; a full turn brings it back to its pose, so the three follow on without a jump.
const ST_SHOW={turn:5,rest:.7,axes:[[0,1,0],[1,0,0],[0,0,1]]};
function stShowQ(t){const P=ST_SHOW.turn+ST_SHOW.rest,n=ST_SHOW.axes.length,c=((t%(P*n))+P*n)%(P*n),i=Math.min(n-1,Math.floor(c/P)),u=Math.min(1,(c-i*P)/ST_SHOW.turn),e=u*u*(3-2*u),A=ST_SHOW.axes[i];return qAxis(A[0],A[1],A[2],e*TAU,q0())}
// (14 Nov 2026) The title's two pictures are drawn by the game's own renderer, with its depth buffer and lighting. They used
// to be painted triangle by triangle, back to front, straight onto the 2D canvas; that has no depth buffer, so a thin part
// lying on a big face (a slit canopy on a hull) was painted over by the face from some angles. Once the ship began to turn
// through every axis the user saw it: "cockpit on the fang overlaps with the hull from some angles".
// How: stPic only notes that a picture is wanted; the next 3D frame draws the models into a corner of the 3D canvas before
// the frame's own drawing clears it (stGL), reads that corner back, makes the background colour clear, and lays the result
// over each panel's 2D backdrop. If the 3D canvas is smaller than a panel, the old painter is used (stDraw).
let stWant=null,stOff=null,stBuf=null,stImg=null;
const ST_KEY=(255<<24|15<<16|8<<8|5)>>>0,ST_FOV=16,ST_D=1000;
function stPic(t){t=t||stT;stT=t;stWant=t}
// the camera for a panel W x H device pixels: straight on from ST_D away through a long lens, so it reads like the flat
// drawing it replaces. stPut places a mesh so its centre is at (cx,cy) and its radius r covers rpx pixels (panel units).
function stGL(c,cv,draw){const W=cv.width,H=cv.height,w=cv.clientWidth,h=cv.clientHeight;if(!G||!W||!H||glc.width<W||glc.height<H)return false;const sv=VP.slice();
  try{const f=1/Math.tan(ST_FOV*Math.PI/360),n=ST_D*.4,fa=ST_D*1.6,Pp=new Float32Array(16),Vv=new Float32Array([1,0,0,0,0,1,0,0,0,0,1,0,0,0,-ST_D,1]);Pp[0]=f/(W/H);Pp[5]=f;Pp[10]=(fa+n)/(n-fa);Pp[11]=-1;Pp[14]=2*fa*n/(n-fa);mMul(VP,Pp,Vv);
    G.viewport(0,0,W,H);G.enable(G.SCISSOR_TEST);G.scissor(0,0,W,H);G.clearColor(5/255,8/255,15/255,1);G.clear(G.COLOR_BUFFER_BIT|G.DEPTH_BUFFER_BIT);G.enable(G.DEPTH_TEST);G.depthMask(true);G.depthFunc(G.LEQUAL);G.disable(G.BLEND);
    useMesh();G.uniform3f(PM.u.uL,.35,.55,.76);G.uniform3f(PM.u.uSun,1,.96,.88);G.uniform3f(PM.u.uAmb,.3,.32,.38);
    draw((m,q,cx,cy,rpx,r)=>{if(!m||!m.buf)return;const k=rpx*ST_D/(f*r*h/2);mModel(MM,((cx/w)*2-1)*ST_D*(W/H)/f,(1-(cy/h)*2)*ST_D/f,0,q,k,k,k);drawMesh(m,MM)});
    if(!stBuf||stBuf.length!==W*H*4){stBuf=new Uint8Array(W*H*4);stImg=new ImageData(W,H)}
    G.readPixels(0,0,W,H,G.RGBA,G.UNSIGNED_BYTE,stBuf);const S32=new Uint32Array(stBuf.buffer),D32=new Uint32Array(stImg.data.buffer);
    for(let y=0;y<H;y++){const so=(H-1-y)*W,dn=y*W;for(let x=0;x<W;x++){const v=S32[so+x];D32[dn+x]=v===ST_KEY?0:v}}
    if(!stOff)stOff=document.createElement('canvas');if(stOff.width!==W||stOff.height!==H){stOff.width=W;stOff.height=H}stOff.getContext('2d').putImageData(stImg,0,0);c.drawImage(stOff,0,0,w,h);return true}
  catch(e){return false}finally{G.disable(G.SCISSOR_TEST);VP.set(sv)}}
function stPicNow(t){const cv=$('stPic');if(!cv||!G||!MDL.ready)return;const w=cv.clientWidth,h=cv.clientHeight;if(!w||!h)return;if(cv.width!==Math.round(w*DPR)||cv.height!==Math.round(h*DPR)){cv.width=w*DPR;cv.height=h*DPR}const c=cv.getContext('2d');c.setTransform(DPR,0,0,DPR,0,0);c.clearRect(0,0,w,h);
  const pir=selFac==='pirate',port=pir?WRACK.sid:selPort,col=pir?sideCol('pirate'):'#e8c878',line=FAC(selFac).col||'#5fa8ff';
  const sy=Math.min(144,h*.55),sr=Math.min(w,400)*.36;const g=c.createRadialGradient(w*.62,sy,10,w*.62,sy,Math.max(w,h)*.7);g.addColorStop(0,'rgba(40,52,84,.55)');g.addColorStop(1,'rgba(5,7,13,0)');c.fillStyle=g;c.fillRect(0,0,w,h);
  let sd=port.split('').reduce((a,ch)=>a*31+ch.charCodeAt(0),7)>>>0;const rr=()=>(sd=(sd*1664525+1013904223)>>>0)/4294967296;c.fillStyle='rgba(236,228,207,.55)';for(let i=0;i<70;i++){c.beginPath();c.arc(rr()*w,rr()*h,rr()*1.1+.2,0,TAU);c.fill()}
  try{const nm=pir?'by_haven':stMdlName('neutral','free',port),m=nm&&MDL.i[nm]?stMesh(nm,pir?'pirate':'neutral',pir?240:210):stationMesh(pir?'pirate':'neutral','station');const r=stR(m.core.data),qs=qMul(ST_Q,qAxis(0,1,0,t*.12,q0()),q0()),spin=m.spin&&m.spin.data&&m.spin.data.length>30?qMul(qs,qAxis(0,1,0,t*.35,q0()),q0()):null;
    if(!stGL(c,cv,put=>{put(m.core,qs,w*.6,sy,sr,r);if(spin)put(m.spin,spin,w*.6,sy,sr,r)})){stDraw(c,m.core.data,qs,w*.6,sy,sr/r,.95);if(spin)stDraw(c,m.spin.data,spin,w*.6,sy,sr/r,.95)}}catch(e){}
  $('stCap').innerHTML=`<div><span class="lab">Freeport</span><b style="color:${col}">${esc(DEF[port].name)}</b></div>`;
  try{stShipPic(t,port,line)}catch(e){}}
// (14 Nov 2026) The ship's own picture, under the station's and its title, with a rule between them (the user: "separate the
// animated ship from the station. Two different animations ... have the ship model spin through the various axis so you can
// see it fully", then "move the ship animation further down below the title of the station animation so there's a clean
// break between the two animations"). From its three-quarter pose the ship turns once about each of its axes in turn (round
// to either side, a loop nose over tail, a roll), easing in and out with a short rest between, so every face comes round.
function stShipPic(t,port,line){const cv=$('stShip');if(!cv)return;const w=cv.clientWidth,h=cv.clientHeight;if(!w||!h)return;if(cv.width!==Math.round(w*DPR)||cv.height!==Math.round(h*DPR)){cv.width=w*DPR;cv.height=h*DPR}const c=cv.getContext('2d');c.setTransform(DPR,0,0,DPR,0,0);c.clearRect(0,0,w,h);
  const g=c.createRadialGradient(w*.5,h*.5,10,w*.5,h*.5,Math.max(w,h)*.7);g.addColorStop(0,'rgba(40,52,84,.5)');g.addColorStop(1,'rgba(5,7,13,0)');c.fillStyle=g;c.fillRect(0,0,w,h);
  let sd=(port+'ship').split('').reduce((a,ch)=>a*31+ch.charCodeAt(0),7)>>>0;const rr=()=>(sd=(sd*1664525+1013904223)>>>0)/4294967296;c.fillStyle='rgba(236,228,207,.5)';for(let i=0;i<34;i++){c.beginPath();c.arc(rr()*w,rr()*h,rr()*1.1+.2,0,TAU);c.fill()}
  try{const m=shipMesh(selFac,selCls),d=m.hull.data,r=stR(d),rp=Math.min(w,h)*.43,q=qMul(SHIP2D_Q,stShowQ(t),q0());
    if(!stGL(c,cv,put=>{put(m.hull,q,w*.5,h*.5,rp,r);if(m.rim)put(m.rim,q,w*.5,h*.5,rp,r)}))stDraw(c,d,q,w*.5,h*.5,rp/r,1)}catch(e){}
  $('stShipCap').innerHTML=`<div><span class="lab">Ship</span><b style="color:${line}">${esc(FAC(selFac).hulls[selCls])}</b><span class="note" style="margin:0;display:block">${esc(CLASSES[selCls].name)}</span></div>`}
// the wanted picture is drawn at the start of the next 3D frame, before that frame clears the canvas
{const o=draw3D;draw3D=function(){if(stWant!==null){const t=stWant;stWant=null;try{const st=$('start');if(st&&!st.hidden)stPicNow(t)}catch(e){}}return o.apply(this,arguments)}}
// ---- the layout: built once from the existing sheet
(function(){const sb=$('start')&&$('start').querySelector('.sbody');if(!sb)return;const kids=[...sb.children],steps=kids.filter(e=>e.classList.contains('step'));if(steps.length<4)return;
  const L=document.createElement('div');L.className='st2l';const R=document.createElement('div');R.className='st2r';R.innerHTML=`<canvas id="stPic" aria-label="Your freeport"></canvas><div id="stCap" class="st2cap"></div><canvas id="stShip" aria-label="Your ship"></canvas><div id="stShipCap" class="st2cap"></div>`;
  const W2=document.createElement('div');W2.className='st2';W2.appendChild(L);W2.appendChild(R);
  const brand=sb.querySelector('.brand'),legacy=$('legacy'),ver=$('ver'),mp=$('mpBox'),nameRow=$('mpName').closest('.mprow'),notes=kids.filter(e=>e.classList.contains('snote')&&e!==legacy&&e!==ver);
  const [sCall,sPort,sRole,sShip]=steps,legStep=document.createElement('div');legStep.className='step';legStep.innerHTML='<i>2</i><span>Legend</span>';const legBody=document.createElement('div');legBody.id='stLeg';legBody.className='st2leg';
  for(const el of[brand,legacy,ver,sCall,nameRow,legStep,legBody,sPort,$('facs'),sRole,$('roles'),sShip,sb.querySelector('.shippick'),mp,...notes])if(el)L.appendChild(el);
  for(const el of kids)if(el.parentElement===sb)L.appendChild(el);
  sb.appendChild(W2);
  const mk=(st,k,n)=>{st.dataset.st=k;st.classList.add('st2h');st.setAttribute('role','button');st.tabIndex=0;st.querySelector('i').textContent=n;st.insertAdjacentHTML('beforeend','<em class="st2v"></em><b class="st2c"></b>')};
  mk(legStep,'legend',2);mk(sPort,'port',3);mk(sRole,'role',4);mk(sShip,'ship',5);
  const tog=e=>{const h=e.target.closest('.st2h');if(!h)return;stOpen[h.dataset.st]=!stOpen[h.dataset.st];stSync()};
  L.addEventListener('click',tog);L.addEventListener('keydown',e=>{if((e.key==='Enter'||e.key===' ')&&e.target.classList&&e.target.classList.contains('st2h')){e.preventDefault();tog(e)}});
  legBody.addEventListener('change',e=>{const el=e.target.closest('[data-lg]');if(!el)return;legSet(el.dataset.lg,el.type==='checkbox'?el.checked:el.value);stSync()});
  legBody.addEventListener('click',e=>{if(e.target.closest('[data-st2="board"]'))$('bLegend').click()});
  $('mpName').addEventListener('input',()=>{try{stSync()}catch(err){}});
  addEventListener('resize',()=>{if(!$('start').hidden)stPic()})})();
function stLegHtml(){const me=cleanCall($('mpName').value);if(!me)return{sum:'enter a callsign first',h:'<p class="note" style="margin:0">Enter your callsign to choose your start package: perks unlocked by your Legend level.</p>'};
  const r=legPeek(me)||{},lvl=legbLevel(r.bp||0),pkg=legbPkg(r.pkg||[],lvl),spent=pkg.reduce((a,b)=>a+b,0);
  let h=`<p class="note" style="margin:0 0 8px">${esc(me)} · level ${lvl}${legbTitle(lvl)?' · '+esc(legbTitle(lvl)):''} · ${r.bp||0} Legend point${(r.bp||0)===1?'':'s'}${lvl<10?`, ${LEGB.lv[lvl]-(r.bp||0)} more to level ${lvl+1}`:''}. Start package: ${spent} of ${lvl} point${lvl===1?'':'s'} spent; each perk costs its level, one Rating perk and one base perk.</p><div class="lgs">`;
  for(let i=1;i<=10;i++){const pk=LEGB_PERKS[i],on=pkg.includes(i);if(i>lvl+1)continue;h+=`<label style="${i>lvl?'opacity:.45':''}"><input type="checkbox" data-lg="pk${i}"${on?' checked':''}${i>lvl?' disabled':''}> ${i}. ${esc(pk.name)}${pk.title?` · title ${esc(pk.title)}`:''}</label>`}
  h+='</div>';if(lvl<9)h+=`<p class="note" style="margin:6px 0 0">Levels ${lvl+2}–10 not yet reached.</p>`;
  if(pkg.includes(3))h+=`<label class="note">Medium hull <select data-lg="medCls">${[['striker','Medium Fighter'],['prospector','Medium Miner'],['freighter','Medium Hauler']].map(([v,n])=>`<option value="${v}"${(r.medCls||'striker')===v?' selected':''}>${n}</option>`).join('')}</select></label>`;
  if(r.spoils)h+=`<p class="note" style="margin:8px 0 0;color:var(--amber)">Conqueror's spoils from your last galaxy: ${[r.spoils.flag?'your flagship':'',r.spoils.chest?`a ${fmt(r.spoils.chest)} cr war chest`:'',r.spoils.vets?`${r.spoils.vets} veteran crew${r.spoils.vets>1?'s':''}`:'',r.spoils.renown?`Renown (+${r.spoils.renown} with every power)`:'',r.spoils.wraith?'the Wraith':''].filter(Boolean).join(', ')}.</p>`;
  h+=`<button class="cov" type="button" data-st2="board" style="margin-top:8px">Leaderboard ›</button>`;
  return{sum:`level ${lvl}${legbTitle(lvl)?' · '+legbTitle(lvl):''} · ${pkg.length?pkg.map(i=>LEGB_PERKS[i].name).join(', '):'no perks picked'}`,h}}
function stSync(){const sb=$('start');if(!sb||!sb.querySelector('.st2'))return;const set=(k,v,body)=>{const h=sb.querySelector(`.st2h[data-st="${k}"]`);if(!h)return;h.querySelector('.st2v').textContent=v;h.querySelector('.st2c').textContent=stOpen[k]?'▴':'▾';h.setAttribute('aria-expanded',stOpen[k]);for(const b of body)if(b)b.hidden=!stOpen[k]};
  let lg;try{lg=stLegHtml()}catch(e){lg={sum:'',h:''}}const LB=$('stLeg');if(stOpen.legend)LB.innerHTML=lg.h;
  const pir=selFac==='pirate';set('legend',lg.sum,[LB]);set('port',pir?FAC('pirate').name:`${DEF[selPort].name} · ${FAC(selFac).short} design line`,[$('facs')]);set('role',pir?'Unbound':ROLES[selRole].name,[$('roles')]);
  set('ship',`${FAC(selFac).hulls[selCls]} · ${CLASSES[selCls].name}`,[sb.querySelector('.shippick')]);stPic()}
// only the hulls you can start in are offered: you never start with credits, so the bought hulls stay off the title screen
function stStartable(k){return selFac==='pirate'?UNB_START.includes(k):START_HULLS.includes(k)}
{const o=showStart;showStart=function(){try{if(!stStartable(selCls)){const L=selFac==='pirate'?UNB_START:(ROLES[selRole]||ROLES.combat).ships;selCls=L.find(stStartable)||(selFac==='pirate'?UNB_START[0]:START_HULLS[0])}}catch(e){}
  const r=o.apply(this,arguments);try{for(const b of $('clsrow').querySelectorAll('[data-cls]'))if(!stStartable(b.dataset.cls))b.hidden=true;stSync()}catch(e){console.error(e)}return r}}
