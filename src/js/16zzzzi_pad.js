//@src 16zzzzi_pad.js
// ============================================================ game controller (gamepad) support (user, 21 Nov 2026: "Also add controller support")
// Any pad the browser reports (Xbox, PlayStation, Switch Pro, generic; the "standard" mapping is the one designed for).
// How it works:
//  - Flight: the left stick steers (through steerInput, so the bridge and gun seat look with it too), the right stick rolls and
//    zooms the chase camera. Every button does what a key does by sending that action's key to the game's own key handler
//    (the physical key the pilot has bound to it), so rebinding and every rule the keyboard path enforces still apply.
//  - Layers: buttons alone, with LB held, or with Back (View/Create) held. A short tap of Back alone opens the galaxy map.
//  - Screens: when any screen is open the left stick moves an on-screen pointer, A clicks, B goes back (what Esc does),
//    the D-pad jumps the pointer to the next button, the right stick scrolls, LB/RB step the tabs, LT/RT the sub-tabs.
//  - Stick lessons from the airplane game: a stick's rest point is learned from steady readings (never taken from the first
//    frame), an axis nobody has touched reads 0, an axis parked at +-1 on a non-standard layout is a trigger and ignored,
//    the deadzone is round, and the mouse only steers again once it has moved since the pad was last used.
// Everything is local input, so a guest in multiplayer flies with it exactly as the host does.
const PADIN={yaw:0,pitch:0,roll:0};
const PAD_B={A:0,B:1,X:2,Y:3,LB:4,RB:5,LT:6,RT:7,BACK:8,START:9,L3:10,R3:11,UP:12,DOWN:13,LEFT:14,RIGHT:15};
// THE MAPPING TABLE. One row per button: [button, alone, with LB held, with Back held]. An action is a key-binding id from
// KEY_ACTS, or one of: boost (Shift), gunsel (machine gun / laser, whichever is not selected), cycleBack (Shift+Tab),
// subCycle (Shift+T), ordNext (Shift+P). '' means the button does nothing on that layer.
// LB and Back are the layer buttons themselves; sticks and the camera are described in PAD_STICKS below.
const PAD_MAP=[
 ['RT','fire','fire','fire'],
 ['LT','thrust','brake','thrust'],
 ['RB','boost','track','subCycle'],
 ['A','act','ahead','comms'],
 ['B','msl','swarm','distress'],
 ['X','tgtH','cycleH','op'],
 ['Y','mine','ast','orders'],
 ['UP','gunsel','det','ordNext'],
 ['DOWN','flare','cancel','ordDrop'],
 ['LEFT','cycleBack','mtool','stealth'],
 ['RIGHT','cycle','jam','assist'],
 ['L3','autopilot','fa',''],
 ['R3','cam','level','sound'],
 ['START','help','company','touch']];
const PAD_STICKS=[['Left stick','Steer: pitch and yaw (further = harder), the same as the mouse'],['Right stick left / right','Roll'],['Right stick up / down','Chase camera: zoom in / out'],['Back, tapped','Galaxy map (held, it is the second layer)'],['LB, held','The first layer: targets, weapons and mining']];
const PAD_SHORT={fire:'Fire the selected gun',thrust:'Thrust',brake:'Brake / reverse',boost:'Afterburner',track:'Hold: turn onto the target\'s lead marker',subCycle:'Pick a system on the target',act:'Dock, launch, land, board, hook',ahead:'Target the ship closest to my nose',comms:'Comms',msl:'Launch a missile',swarm:'Swarm pods',distress:'Distress call',tgtH:'Target the nearest hostile',cycleH:'Cycle hostiles',op:'Join the top operation',mine:'Mine: charge, scoop, limpet',ast:'Target the nearest rock',orders:'Sign on to the picked order',gunsel:'Switch gun: machine gun or laser',det:'Detonate charges',cancel:'Cancel charges',ordNext:'Pick the next order',flare:'Flares',ordDrop:'Drop the order or job',cycleBack:'Previous target',mtool:'Mining tool: launcher or laser',stealth:'Stealth, or false colours',cycle:'Next target (gates too)',jam:'Jam mode',assist:'Target whoever attacks a friendly',autopilot:'Autopilot',fa:'Flight assist on/off',cam:'Chase or cockpit camera',level:'Auto-level on/off',sound:'Sound: on, music off, muted',help:'This manual',company:'Company screen',touch:'Touch buttons on/off',map:'Galaxy map'};
const PAD_NAMES={xb:['A','B','X','Y','LB','RB','LT','RT','View','Menu','L3','R3','D-pad up','D-pad down','D-pad left','D-pad right'],ps:['Cross','Circle','Square','Triangle','L1','R1','L2','R2','Create','Options','L3','R3','D-pad up','D-pad down','D-pad left','D-pad right']};
const PAD_ROW=[];
for(const r of PAD_MAP)PAD_ROW[PAD_B[r[0]]]=[r[1],r[2],r[3]];
const PAD={
  cfg:{dz:.21,inv:false},
  live:false,idx:-1,id:'',std:true,ps:false,gp:null,tScan:-1e9,tLast:0,fresh:true,
  b:new Uint8Array(18),pb:new Uint8Array(18),v:new Float64Array(18),swallow:new Uint8Array(18),held:[],
  rest:[],trig:[],calm:[],restId:null,t0:0,s:new Float64Array(4),lx:0,ly:0,rx:0,ry:0,
  tPad:0,tOther:0,synth:false,ui:false,placed:false,px:0,py:0,ptr:null,ptrOn:false,hoverT:0,sacc:0,wheelT:0,
  backT:0,combo:false,rev:null,revPs:null,audioAsked:false,audioTold:false,uiEls:null,dirty:true,liveT:0,
  kbEl:null,kbTarget:null,kbShift:false,steering:false
};
try{const c=JSON.parse(localStorage.getItem('dgbeyond.pad')||'null');if(c){if(c.dz>=.05&&c.dz<=.45)PAD.cfg.dz=+c.dz;PAD.cfg.inv=!!c.inv}}catch(e){}
function padSave(){try{localStorage.setItem('dgbeyond.pad',JSON.stringify(PAD.cfg))}catch(e){}}
function padBtnName(i){return(PAD.ps?PAD_NAMES.ps:PAD_NAMES.xb)[i]||('Button '+i)}
// the same action list, as the player would read it for the connected pad
function padRevBuild(){const R={},nm=r=>padBtnName(PAD_B[r]),lb=padBtnName(4),bk=padBtnName(8);
  for(const r of PAD_MAP){const n=nm(r[0]);if(r[1]&&!R[r[1]])R[r[1]]=n;if(r[2]&&!R[r[2]])R[r[2]]=lb+' + '+n;if(r[3]&&!R[r[3]])R[r[3]]=bk+' + '+n}
  R.kin=R.las=R.gunsel;R.rollL='Right stick left';R.rollR='Right stick right';R.map=bk+' (tap)';PAD.rev=R;PAD.revPs=PAD.ps}
function padKbName(id){if(!PAD.rev||PAD.revPs!==PAD.ps)padRevBuild();return PAD.rev[id]||''}
// prompts, lessons and the manual name the controller button while the controller was the last thing used
function padLead(){return PAD.live&&PAD.tPad>PAD.tOther}
{const o=kb;kb=function(id){if(id==='subCycle'){return padLead()?(padKbName('subCycle')||o('tgtH')):'Shift+'+o('tgtH')}if(padLead()){const n=padKbName(id);if(n)return n}return o.apply(this,arguments)}}
{const o=steerInput;steerInput=function(){const r=o.apply(this,arguments);if(PADIN.yaw||PADIN.pitch){r.yaw=clamp(r.yaw+PADIN.yaw,-1,1);r.pitch=clamp(r.pitch+PADIN.pitch,-1,1)}return r}}
{const o=fmMan;fmMan=function(){return o.apply(this,arguments)||PAD.steering}}
// what the pad is doing counts as the pad being used; anything else the pilot touches hands the prompts and the steering back
for(const ev of['mousemove','mousedown','keydown','touchstart','wheel'])addEventListener(ev,()=>{if(!PAD.synth)PAD.tOther=performance.now()},{capture:true,passive:true});
addEventListener('gamepadconnected',e=>{PAD.dirty=true;try{if(running)flash('Controller connected: '+String(e.gamepad.id).replace(/\(.*?\)/g,'').trim().slice(0,40))}catch(er){}});
addEventListener('gamepaddisconnected',()=>{PAD.dirty=true;try{if(running)flash('Controller disconnected.')}catch(er){}});

// ---- reading the pad
function padGet(now){
  if(!navigator.getGamepads)return null;
  if(!PAD.live&&now-PAD.tScan<250)return null;
  PAD.tScan=now;
  let list=null;try{list=navigator.getGamepads()}catch(e){}
  if(!list)return null;
  let gp=PAD.idx>=0?list[PAD.idx]:null;
  if(!gp||!gp.connected){gp=null;
    for(let i=0;i<list.length;i++){const p=list[i];if(p&&p.connected&&p.mapping==='standard'){gp=p;break}}
    if(!gp)for(let i=0;i<list.length;i++){const p=list[i];if(p&&p.connected){gp=p;break}}}
  if(!gp){PAD.idx=-1;return null}
  if(gp.index!==PAD.idx||gp.id!==PAD.id){PAD.idx=gp.index;PAD.id=gp.id||'';PAD.std=gp.mapping==='standard';PAD.ps=/054c|dualsense|dualshock|playstation|wireless controller/i.test(PAD.id);PAD.dirty=true}
  return gp}
// where each axis rests: not taken from the first frame (browsers can report 0 for a moment, a worn stick rests off centre, and a
// trigger can report -1 on what should be a stick axis). In the first 3 s an axis that sits still is measured; later an axis
// left alone for 2 s is re-centred. An axis nobody has moved yet reads 0 whatever it says.
function padSticks(gp,T){
  const ax=gp.axes||[],R0=PAD.rest;
  if(PAD.restId!==gp.id){PAD.restId=gp.id;PAD.rest=[];PAD.trig=[];PAD.calm=[];PAD.t0=T;return padSticks(gp,T)}
  const early=T-PAD.t0<3000;
  if(!PAD.calm.length){let any=false;for(let i=0;i<ax.length;i++)if(ax[i])any=true;if(!any){PAD.t0=T;PAD.lx=PAD.ly=PAD.rx=PAD.ry=0;return}}
  for(let i=0;i<ax.length;i++){
    const v=+ax[i]||0;let c=PAD.calm[i];if(!c)c=PAD.calm[i]={lo:v,hi:v,t:T,first:v,moved:false};
    if(v<c.lo)c.lo=v;if(v>c.hi)c.hi=v;
    if(!c.moved&&Math.abs(v)>.45&&(gp.mapping==='standard'||Math.abs(v)<.9))c.moved=true;
    if(c.hi-c.lo>(early?.03:.012)){c.lo=c.hi=v;c.t=T;const r=R0[i]!==undefined?R0[i]:c.first;if(Math.abs(v-r)>.08)c.moved=true;continue}
    const still=T-c.t;
    if(early&&still>700){
      if(gp.mapping!=='standard'&&Math.abs(v)>.9)PAD.trig[i]=true;
      else if(Math.abs(v)<.35){R0[i]=v;PAD.trig[i]=false}
    }else if(!early&&still>2000&&!PAD.trig[i]&&Math.abs(v-(R0[i]||0))<.3&&Math.abs(v)<.35)R0[i]=v;
  }
  const a=i=>{const c=PAD.calm[i];if(PAD.trig[i]||!c||!c.moved)return 0;const v=+ax[i]||0;return Math.max(-1,Math.min(1,v-(R0[i]||0)))};
  padRadial(a(0),a(1),0);padRadial(a(2),a(3),2);
  PAD.lx=PAD.s[0];PAD.ly=PAD.s[1];PAD.rx=PAD.s[2];PAD.ry=PAD.s[3]}
// a round deadzone: the stick's distance from centre, not each axis alone
function padRadial(x,y,k){const d=Math.hypot(x,y),z=PAD.cfg.dz;if(d<z){PAD.s[k]=PAD.s[k+1]=0;return}const f=Math.min(1,(d-z)/(1-z))/d;PAD.s[k]=x*f;PAD.s[k+1]=y*f}
function padRead(gp){
  const bs=gp.buttons||[],n=Math.min(bs.length,17);
  for(let i=0;i<17;i++){
    const bt=i<n?bs[i]:null,v=bt?(bt.value>0?bt.value:(bt.pressed?1:0)):0;PAD.v[i]=v;
    const pr=!!(bt&&bt.pressed);
    PAD.b[i]=PAD.b[i]?((pr||v>.2)?1:0):((pr||v>.35)?1:0)}}

// ---- sending actions to the game
function padKey(code,down,shift){PAD.synth=true;try{dispatchEvent(new KeyboardEvent(down?'keydown':'keyup',{code,key:code,shiftKey:!!shift,bubbles:true,cancelable:true}))}catch(e){}PAD.synth=false}
function padTap(code,shift){padKey(code,true,shift);padKey(code,false,shift)}
// the physical key code the pilot has bound to a key action (the game translates it back to the action)
function padCode(id){return KEYB[id]||KEY_DEF[id]||''}
function padResolve(id){
  switch(id){
    case'boost':return['ShiftLeft',false];
    case'gunsel':return[padCode(S&&S.player&&S.player.wpn==='laser'?'kin':'las'),false];
    case'cycleBack':return[padCode('cycle'),true];
    case'subCycle':return[padCode('tgtH'),true];
    case'ordNext':return[padCode('orders'),true]}
  return[padCode(id),false]}
function padFire(i,id){
  if(keyWait)return;
  const r=padResolve(id);if(!r[0])return;
  PAD.held[i]=r;padKey(r[0],true,r[1])}
function padRelease(i){const h=PAD.held[i];if(h){PAD.held[i]=null;padKey(h[0],false,h[1])}}
function padReleaseAll(){for(let i=0;i<18;i++)padRelease(i);PADIN.yaw=PADIN.pitch=PADIN.roll=0;PAD.steering=false}

// ---- screens
function padUiOpen(){
  if(!PAD.uiEls){PAD.uiEls=['padKb','sndPop','comms','start','legend','win','fcon','dock','map','company','help'].map(id=>$(id))}
  const E=PAD.uiEls;for(let i=0;i<E.length;i++){const el=E[i];if(el&&!el.hidden)return true}
  return false}
function padTopRoot(){
  const k=PAD.kbEl;if(k&&!k.hidden)return k;
  const sp=$('sndPop');if(sp&&!sp.hidden)return sp;
  if(commsOpen())return $('comms');
  const el=document.elementFromPoint(innerWidth/2,innerHeight/2);
  return(el&&el.closest&&el.closest('.sheet'))||null}
const PAD_CAND='button,a[href],input,select,textarea,label,summary,[role=tab],[role=button],[data-act],[data-co],[data-cid],[data-fc],[data-op],[data-cm],[data-rebind],[data-close],[data-pk],[onclick],[tabindex]:not([tabindex="-1"]),canvas';
function padVis(el,x,y){const t=document.elementFromPoint(x,y);return!!t&&(t===el||el.contains(t)||t.contains(el))}
// move the pointer to the nearest button in a direction (dx,dy in -1..1; 0,0 = nearest to the pointer)
function padSnap(dx,dy){
  const root=padTopRoot()||document.body,list=root.querySelectorAll(PAD_CAND),W2=innerWidth,H2=innerHeight,px=PAD.px,py=PAD.py,out=[];
  for(let i=0;i<list.length;i++){
    const el=list[i];if(el.disabled||el.type==='hidden')continue;
    const r=el.getBoundingClientRect();if(r.width<6||r.height<6||r.right<0||r.bottom<0||r.left>W2||r.top>H2)continue;
    const cx=(r.left+r.right)/2,cy=(r.top+r.bottom)/2;let sc;
    if(dx===0&&dy===0)sc=Math.hypot(cx-px,cy-py);
    else if(dy!==0){const along=(cy-py)*dy;if(along<6)continue;const perp=Math.max(0,r.left-px,px-r.right);sc=along+perp*2.5}
    else{const along=(cx-px)*dx;if(along<6)continue;const perp=Math.max(0,r.top-py,py-r.bottom);sc=along+perp*2.5}
    out.push({el,r,sc,cx,cy})}
  out.sort((a,b)=>a.sc-b.sc);
  for(let k=0;k<out.length&&k<14;k++){
    const c=out[k],r=c.r;let x=c.cx,y=c.cy;
    if(dy!==0){x=Math.min(r.right-3,Math.max(r.left+3,px))}else if(dx!==0){y=Math.min(r.bottom-3,Math.max(r.top+3,py))}
    x=Math.min(W2-2,Math.max(2,x));y=Math.min(H2-2,Math.max(2,y));
    if(padVis(c.el,x,y)){PAD.px=x;PAD.py=y;padPtrMove();return true}}
  return false}
function padScrollable(el,horiz){
  while(el&&el!==document.body&&el!==document.documentElement){
    const cs=getComputedStyle(el),o=horiz?cs.overflowX:cs.overflowY;
    if((o==='auto'||o==='scroll')&&(horiz?el.scrollWidth>el.clientWidth+2:el.scrollHeight>el.clientHeight+2))return el;
    el=el.parentElement}
  return null}
function padScroll(dx,dy){
  const el=document.elementFromPoint(PAD.px,PAD.py);if(!el)return false;
  let done=false;
  if(dy){const s=padScrollable(el,false);if(s){const b=s.scrollTop;s.scrollTop+=dy;done=s.scrollTop!==b}}
  if(dx){const s=padScrollable(el,true);if(s){const b=s.scrollLeft;s.scrollLeft+=dx;done=done||s.scrollLeft!==b}}
  return done}
function padEv(el,type,x,y,btns){
  const o={bubbles:true,cancelable:true,clientX:x,clientY:y,button:0,buttons:btns,view:window};
  if(type.startsWith('pointer')){o.pointerType='mouse';o.isPrimary=true;o.pointerId=1;el.dispatchEvent(new PointerEvent(type,o))}
  else el.dispatchEvent(new MouseEvent(type,o))}
function padClickAt(x,y){
  const el=document.elementFromPoint(x,y);if(!el)return false;
  PAD.synth=true;
  try{
    const inp=el.closest('input,select,textarea');
    if(inp&&inp.type==='range'){const r=inp.getBoundingClientRect(),mn=+inp.min||0,mx=inp.max===''?100:+inp.max,st=+inp.step||1;let v=mn+Math.min(1,Math.max(0,(x-r.left)/r.width))*(mx-mn);v=Math.round(v/st)*st;inp.value=String(Math.min(mx,Math.max(mn,v)));inp.dispatchEvent(new Event('input',{bubbles:true}));inp.dispatchEvent(new Event('change',{bubbles:true}));return true}
    if(inp&&inp.tagName==='SELECT'){if(inp.options.length){inp.selectedIndex=(inp.selectedIndex+1)%inp.options.length;inp.dispatchEvent(new Event('input',{bubbles:true}));inp.dispatchEvent(new Event('change',{bubbles:true}))}return true}
    if(inp&&(inp.tagName==='TEXTAREA'||/^(text|search|number|email|url|password|tel|)$/.test(inp.type))){padKbOpen(inp);return true}
    padEv(el,'pointerdown',x,y,1);padEv(el,'mousedown',x,y,1);padEv(el,'pointerup',x,y,0);padEv(el,'mouseup',x,y,0);padEv(el,'click',x,y,0)}
  finally{PAD.synth=false}
  return true}
function padTab(dir,sub){
  const root=padTopRoot();if(!root)return false;
  const row=sub?root.querySelector('.stabs'):(root.querySelector('.mtabs')||root.querySelector('[role=tablist]'));if(!row)return false;
  const tabs=row.querySelectorAll('[role=tab],.tab');if(tabs.length<2)return false;
  let cur=-1;for(let i=0;i<tabs.length;i++)if(tabs[i].getAttribute('aria-selected')==='true')cur=i;
  const n=Math.max(0,Math.min(tabs.length-1,(cur<0?0:cur+dir)));if(n===cur)return false;
  const r=tabs[n].getBoundingClientRect();padClickAt(r.left+r.width/2,r.top+r.height/2);return true}
function padTopSheet(){const el=document.elementFromPoint(innerWidth/2,innerHeight/2);return(el&&el.closest&&el.closest('.sheet'))||null}
// B: what Esc does. Where Esc does nothing (the title screen's side sheets) the sheet's own Close button does it.
function padBack(){
  if(PAD.kbEl&&!PAD.kbEl.hidden){padKbClose();return}
  const before=padTopSheet();
  if(running){padTap('Escape',false)}
  const after=padTopSheet();
  if(after&&before===after){const b=after.querySelector('[data-close]');if(b&&b.getBoundingClientRect().width)padClickAt(b.getBoundingClientRect().left+4,b.getBoundingClientRect().top+4)}}
function padPtrMake(){
  const st=document.createElement('style');
  st.textContent='#padPtr{position:fixed;left:0;top:0;width:34px;height:34px;z-index:2147483000;pointer-events:none;display:none;filter:drop-shadow(0 0 3px rgba(0,0,0,.9))}#padPtr.on{display:block}#padKb{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:2147482000;background:rgba(8,10,16,.97);border:1px solid var(--line-hi,#5a5648);padding:10px;max-width:calc(100% - 20px)}#padKb[hidden]{display:none}#padKb .pk-v{font-family:var(--f-mono,monospace);font-size:15px;color:var(--ivory,#ece4cf);min-height:22px;margin-bottom:6px;border-bottom:1px solid var(--line-hi,#5a5648);padding-bottom:4px;word-break:break-all}#padKb .pk-r{display:flex;gap:4px;margin-top:4px;justify-content:center}#padKb button{min-width:34px;padding:6px 8px}.padtab{display:grid;grid-template-columns:auto 1fr 1fr 1fr;gap:3px 12px;font-size:12px;margin-top:6px}.padtab b{color:var(--ivory,#ece4cf);font-weight:600}.padtab .h{color:var(--faint,#8a846f);font-size:11px;text-transform:uppercase;letter-spacing:.05em}.padlive{font-family:var(--f-mono,monospace);font-size:11px;color:var(--dim,#b5ae98);white-space:pre-wrap;margin-top:6px}.padcfg{display:flex;gap:10px;align-items:center;margin:6px 0;font-size:13px;flex-wrap:wrap}.padcfg input[type=range]{width:180px}';
  document.head.appendChild(st);
  const d=document.createElement('div');d.id='padPtr';
  d.innerHTML='<svg width="34" height="34" viewBox="0 0 34 34"><circle cx="9" cy="9" r="8" fill="none" stroke="#f0b24a" stroke-width="1.6" opacity=".9"/><path d="M9 3 L9 6 M9 12 L9 15 M3 9 L6 9 M12 9 L15 9" stroke="#f0b24a" stroke-width="1.4"/><path d="M6 6 L6 26 L12 20.5 L16.5 30 L20 28.5 L15.5 19.5 L23.5 19.5 Z" fill="#ece4cf" stroke="#0a0c12" stroke-width="1.6" stroke-linejoin="round" transform="translate(-4 -4) scale(.9)"/></svg>';
  document.body.appendChild(d);PAD.ptr=d}
function padPtrMove(){const d=PAD.ptr;if(d)d.style.transform='translate('+Math.round(PAD.px-9)+'px,'+Math.round(PAD.py-9)+'px)'}
function padPtrShow(on){if(on===PAD.ptrOn)return;PAD.ptrOn=on;if(!PAD.ptr&&on)padPtrMake();if(PAD.ptr)PAD.ptr.classList.toggle('on',on);if(on)padPtrMove()}

// ---- the on-screen keyboard: opens when A is pressed on a text box (the callsign, a galaxy code)
const PAD_KB_ROWS=['1234567890','qwertyuiop','asdfghjkl-','zxcvbnm_.'];
function padKbOpen(inp){
  if(!PAD.kbEl){
    const d=document.createElement('div');d.id='padKb';d.hidden=true;
    let h='<div class="pk-v" id="padKbV"></div>';
    for(const row of PAD_KB_ROWS)h+='<div class="pk-r">'+[...row].map(ch=>`<button class="btn sm" type="button" data-pk="${ch}">${ch}</button>`).join('')+'</div>';
    h+='<div class="pk-r"><button class="btn sm" type="button" data-pk="#shift">Shift</button><button class="btn sm" type="button" data-pk=" " style="min-width:120px">Space</button><button class="btn sm" type="button" data-pk="#back">Delete</button><button class="btn sm pri" type="button" data-pk="#done">Done</button></div>';
    d.innerHTML=h;document.body.appendChild(d);PAD.kbEl=d;PAD.uiEls=null;
    d.addEventListener('click',e=>{const b=e.target.closest('[data-pk]');if(b)padKbKey(b.dataset.pk)})}
  PAD.kbTarget=inp;PAD.kbShift=false;PAD.kbEl.hidden=false;padKbShow();
  const r=PAD.kbEl.getBoundingClientRect();PAD.px=r.left+r.width/2;PAD.py=r.top+r.height/2;padSnap(0,0)}
function padKbShow(){const v=$('padKbV');if(v)v.textContent=(PAD.kbTarget?PAD.kbTarget.value:'')+'_'}
function padKbClose(){if(PAD.kbEl)PAD.kbEl.hidden=true;const t=PAD.kbTarget;PAD.kbTarget=null;if(t&&t.dispatchEvent)t.dispatchEvent(new Event('change',{bubbles:true}))}
function padKbKey(k){
  const t=PAD.kbTarget;if(!t)return;
  if(k==='#done'){padKbClose();return}
  if(k==='#shift'){PAD.kbShift=!PAD.kbShift;return}
  if(k==='#back')t.value=t.value.slice(0,-1);
  else if(!(t.maxLength>0&&t.value.length>=t.maxLength)){t.value+=PAD.kbShift?k.toUpperCase():k;PAD.kbShift=false}
  t.dispatchEvent(new Event('input',{bubbles:true}));padKbShow()}

// ---- the Controller section of the Pilot's Manual
function padHelpRender(){
  const el=$('padList');if(!el)return;
  const nm=i=>esc(padBtnName(i)),lb=nm(4),bk=nm(8);
  const act=a=>a?esc(PAD_SHORT[a]||a):'';
  const status=PAD.live?`Connected: ${esc(String(PAD.id).replace(/\(.*?\)/g,'').trim().slice(0,60))}${PAD.std?'':' (not the standard layout: buttons may be numbered differently)'}`:'No controller found. Plug one in or pair it, then press any button.';
  let h=`<p class="note" id="padStat" style="margin:0 0 6px">${status}</p>
   <div class="padcfg"><label>Stick deadzone <input type="range" min="0.05" max="0.45" step="0.01" value="${PAD.cfg.dz}" data-padcfg="dz"> <span id="padDzv">${PAD.cfg.dz.toFixed(2)}</span></label><label><input type="checkbox" data-padcfg="inv"${PAD.cfg.inv?' checked':''}> Invert pitch (stick up dives)</label></div>
   <p class="note" style="margin:0">Raise the deadzone if the ship drifts with the stick let go. A stick that has never been touched is read as centred, and a resting offset is learned over the first seconds.</p>`;
  h+='<div class="padtab"><span class="h">Control</span><span class="h">Alone</span><span class="h">'+lb+' held</span><span class="h">'+bk+' held</span>';
  for(const r of PAD_MAP)h+=`<b>${nm(PAD_B[r[0]])}</b><span>${act(r[1])}</span><span>${act(r[2])}</span><span>${act(r[3])}</span>`;
  h+='</div><div class="padtab" style="grid-template-columns:auto 1fr">';
  for(const[a,b]of PAD_STICKS)h+=`<b>${esc(a.replace('LB',padBtnName(4)).replace('Back',padBtnName(8)))}</b><span>${esc(b.replace('LB',padBtnName(4)).replace('Back',padBtnName(8)))}</span>`;
  h+=`</div><p class="note" style="margin:8px 0 0">On a screen: left stick moves the pointer, ${nm(0)} clicks, ${nm(1)} goes back, the D-pad jumps to the next button, right stick scrolls, ${lb} and ${nm(5)} change tab, ${nm(6)} and ${nm(7)} change the sub-tab, ${nm(9)} opens and closes this manual. On a text box ${nm(0)} opens an on-screen keyboard. With comms open the D-pad picks options 1 to 4.</p>
   <div class="padlive" id="padLive"></div>`;
  el.innerHTML=h;PAD.dirty=false}
function padLiveTick(now){
  if(now-PAD.liveT<100)return;PAD.liveT=now;
  const el=$('padLive');if(!el)return;
  if(!PAD.live||!PAD.gp){el.textContent='Live readout: no controller.';return}
  const f=v=>(v>=0?' ':'')+(+v||0).toFixed(2),ax=PAD.gp.axes||[];let s='Raw axes: ';
  for(let i=0;i<Math.min(ax.length,8);i++)s+=i+':'+f(ax[i])+(PAD.trig[i]?'(trigger, ignored) ':' ');
  let bt='';for(let i=0;i<17;i++)if(PAD.b[i])bt+=padBtnName(i)+' ';
  el.textContent=s+'\nPressed: '+(bt||'nothing')+'\nAfter rest and deadzone: steer '+f(PAD.lx)+f(PAD.ly)+'  right stick '+f(PAD.rx)+f(PAD.ry)}
document.addEventListener('input',e=>{const t=e.target,k=t&&t.dataset&&t.dataset.padcfg;if(!k)return;
  if(k==='dz'){PAD.cfg.dz=Math.max(.05,Math.min(.45,+t.value||.21));const v=$('padDzv');if(v)v.textContent=PAD.cfg.dz.toFixed(2)}
  else if(k==='inv')PAD.cfg.inv=!!t.checked;
  padSave()});
document.addEventListener('change',e=>{const t=e.target;if(t&&t.dataset&&t.dataset.padcfg==='inv'){PAD.cfg.inv=!!t.checked;padSave()}});

// ---- the frame
function padModeChange(ui){
  padReleaseAll();PAD.ui=ui;
  for(let i=0;i<17;i++)if(PAD.b[i])PAD.swallow[i]=1;
  if(ui)PAD.placed=false;else padPtrShow(false)}
function padLost(){padReleaseAll();PAD.live=false;PAD.gp=null;PAD.fresh=true;PAD.b.fill(0);PAD.pb.fill(0);PAD.swallow.fill(0);padPtrShow(false);PAD.dirty=true}
function padPress(i,now){
  if(i===8){PAD.backT=now;PAD.combo=false;return}
  if(PAD.b[8])PAD.combo=true;
  if(PAD.ui){padUiPress(i);return}
  if(i===4)return;
  const row=PAD_ROW[i];if(!row)return;
  const id=row[PAD.b[8]?2:PAD.b[4]?1:0];if(id)padFire(i,id)}
function padUiPress(i){
  const comms=commsOpen();
  switch(i){
    case 0:padClickAt(PAD.px,PAD.py);break;
    case 1:padBack();break;
    case 9:if(running&&!(PAD.kbEl&&!PAD.kbEl.hidden))padTap(padCode('help'),false);break;
    case 4:if(!comms)padTab(-1,false);break;
    case 5:if(comms)padTap(padCode('comms')||'KeyI',false);else padTab(1,false);break;
    case 6:padTab(-1,true);break;
    case 7:padTab(1,true);break;
    case 12:if(comms)padTap('Digit1',false);else padSnap(0,-1)||padScroll(0,-180);break;
    case 13:if(comms)padTap('Digit3',false);else padSnap(0,1)||padScroll(0,180);break;
    case 14:if(comms)padTap('Digit4',false);else padSnap(-1,0)||padScroll(-180,0);break;
    case 15:if(comms)padTap('Digit2',false);else padSnap(1,0)||padScroll(180,0);break}}
function padFrame(now){
  const gp=padGet(now);
  if(!gp){if(PAD.live)padLost();return}
  if(!PAD.live){PAD.live=true;PAD.fresh=true;PAD.dirty=true}
  PAD.gp=gp;padRead(gp);padSticks(gp,now);
  if(PAD.fresh){PAD.pb.set(PAD.b);PAD.fresh=false;PAD.tLast=now}
  const dt=Math.min(.05,Math.max(0,(now-PAD.tLast)/1000));PAD.tLast=now;
  const T=performance.now();
  let edge=false;for(let i=0;i<17;i++)if(PAD.b[i]&&!PAD.pb[i])edge=true;
  const sticky=!!(PAD.lx||PAD.ly||PAD.rx||PAD.ry);
  if(edge||sticky){PAD.tPad=T;touchLast=false}
  if(edge&&!auOK()){
    auInit();
    if(!PAD.audioAsked){PAD.audioAsked=true;setTimeout(()=>{if(!auOK()&&AU.on.sfx&&!PAD.audioTold){PAD.audioTold=true;try{flash('No sound yet: the browser needs a click or a key press, it does not count a controller. Click once or press any key.')}catch(e){}}},700)}}
  if(PAD.dirty)padHelpRender();
  const hp=$('help');if(hp&&!hp.hidden)padLiveTick(now);
  const ui=padUiOpen();
  if(ui!==PAD.ui)padModeChange(ui);
  for(let i=0;i<17;i++){
    const d=PAD.b[i],p=PAD.pb[i];
    if(d&&!p){if(!PAD.swallow[i])padPress(i,now)}
    else if(!d&&p){
      PAD.swallow[i]=0;padRelease(i);
      if(i===8&&!PAD.combo&&now-PAD.backT<500&&running&&!(PAD.kbEl&&!PAD.kbEl.hidden))padTap(padCode('map'),false)}}
  PAD.pb.set(PAD.b);
  if(ui)padUiFrame(dt,edge||sticky);else padFlyFrame(dt,edge||sticky)}
function padUiFrame(dt,used){
  PADIN.yaw=PADIN.pitch=PADIN.roll=0;PAD.steering=false;
  const show=padLead();
  if(show&&used&&!PAD.placed){PAD.placed=true;PAD.px=innerWidth/2;PAD.py=innerHeight/2;padSnap(0,0)}
  padPtrShow(show&&PAD.placed);
  if(!PAD.placed)return;
  if(PAD.lx||PAD.ly){
    const m=Math.hypot(PAD.lx,PAD.ly),k=Math.pow(m,1.7)/m*1000*dt;
    PAD.px=Math.min(innerWidth-1,Math.max(0,PAD.px+PAD.lx*k));PAD.py=Math.min(innerHeight-1,Math.max(0,PAD.py+PAD.ly*k));padPtrMove();
    const t=performance.now();
    if(t-PAD.hoverT>66){PAD.hoverT=t;const el=document.elementFromPoint(PAD.px,PAD.py);if(el){PAD.synth=true;try{padEv(el,'pointermove',PAD.px,PAD.py,0);padEv(el,'mousemove',PAD.px,PAD.py,0)}finally{PAD.synth=false}}}}
  if(PAD.rx||PAD.ry){
    const sy=PAD.ry*900*dt,sx=PAD.rx*900*dt;PAD.sacc+=Math.abs(sy)+Math.abs(sx);
    const done=padScroll(Math.abs(sx)>.5?sx:0,Math.abs(sy)>.5?sy:0);
    const t=performance.now();
    if(!done&&Math.abs(PAD.ry)>.6&&t-PAD.wheelT>260){PAD.wheelT=t;const el=document.elementFromPoint(PAD.px,PAD.py);if(el){PAD.synth=true;try{el.dispatchEvent(new WheelEvent('wheel',{bubbles:true,cancelable:true,clientX:PAD.px,clientY:PAD.py,deltaY:PAD.ry>0?100:-100}))}finally{PAD.synth=false}}}}}
function padFlyFrame(dt,used){
  PAD.ptrOn&&padPtrShow(false);
  const m=Math.hypot(PAD.lx,PAD.ly);
  if(m>0){const k=Math.pow(m,1.35)/m;PADIN.yaw=-PAD.lx*k;PADIN.pitch=PAD.ly*k*(PAD.cfg.inv?-1:1)}else{PADIN.yaw=PADIN.pitch=0}
  PAD.steering=m>.3;
  const r=Math.abs(PAD.rx);PADIN.roll=r>0?Math.sign(PAD.rx)*Math.pow(r,1.35):0;
  if(used){mouse.aim=false}
  if(PAD.steering&&apOn){apOn=false;flash('Autopilot off.')}
  if(PAD.ry)cam.dist=clamp(cam.dist*Math.exp(PAD.ry*dt*1.4),.6,3)}
{const o=frame;frame=function(now){try{padFrame(now)}catch(e){frameErr('controller',e)}return o.apply(this,arguments)}}
