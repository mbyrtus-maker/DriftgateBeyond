// Gate jump sounds, from two clips the user supplied (14 Nov 2026): a countdown (three low beeps a second apart, then a
// high one) and a hyper-jump effect (a 4.8 s charge, the blast, a 4 s tail). In the pack they are cdBeep, cdGo and hjump
// (tools/snd_add.py). They play at their own pitch, not the pack's lowered one.
//   - On a gate's approach the charge starts so that its blast lands on the moment of the jump (HJ.lead s before it).
//   - The low beep sounds at 3, 2 and 1 seconds to go; the high beep sounds with the blast as the ship jumps.
//   - Leaving the approach, losing alignment or being jammed fades the charge out.
//   - A jump with no countdown (in formation with a capital, from a gunner's seat) plays from just before the blast.
//   - The arrival 1.3 s later no longer plays a second jump sound; the blast's tail carries through it.
// With the clips not loaded (sound off at start, an old browser) the old beeps and warp play as before.
const HJ={lead:4.85,vol:.3,beep:.13,go:.15,h:null};
function hjLive(){return!!(HJ.h&&AU.ctx&&AU.ctx.currentTime<HJ.h.end)}
function hjStop(fade){const h=HJ.h;if(!h)return;HJ.h=null;try{const t=AU.ctx.currentTime;h.g.gain.cancelScheduledValues(t);h.g.gain.setValueAtTime(h.g.gain.value,t);h.g.gain.linearRampToValueAtTime(0,t+fade);h.s.stop(t+fade+.03)}catch(e){}}
// start the jump clip `off` seconds in; cd marks a charge that a cancelled countdown may stop
function hjStart(off,cd){if(MUTE||!auOK()||!AU.on.sfx||!AU.sx)return false;const b=SND.b.hjump;if(!b)return false;hjStop(.05);
  const c=AU.ctx,s=c.createBufferSource(),g=c.createGain(),t=c.currentTime;off=clamp(off||0,0,b.duration-.2);s.buffer=b;
  g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(HJ.vol,t+(off>.1?.04:.2));s.connect(g);g.connect(AU.sx);s.start(t,off);
  HJ.h={s,g,end:t+b.duration-off,cd:!!cd,go:!cd,t0:t,off0:off};try{voice(b.duration-off)}catch(e){}return true}
// rem = seconds until the jump, every frame of the countdown
// While the charge plays, the countdown follows the sound's own clock, so the beeps and the jump land where the clip puts
// them even when frames run slow (the game's clock can lag real time; the sound cannot). A gap of over a second (the game
// was paused) restarts the clip at the right place instead.
function gjCharge(rem){const h=HJ.h;if(h&&h.cd&&!h.go&&h.s&&W.gc&&hjLive()){const ar=HJ.lead-(AU.ctx.currentTime-h.t0+h.off0);
    if(Math.abs(ar-rem)>1)hjStop(.1);else{if(Math.abs(ar-rem)>.02)W.gc.t=unbGateHold()-ar;return}}
  if(rem<=HJ.lead&&rem>.4&&!hjLive())hjStart(HJ.lead-rem,true)}
// a whole second of the countdown has passed; n seconds remain
function gjCount(n){if(!SND.b.cdBeep){SFX.count(n===1);return}if(n<=3)smp('cdBeep',HJ.beep,1/PITCH,0,0)}
// the ship jumps
function gjGo(){if(SND.b.cdGo)smp('cdGo',HJ.go,1/PITCH,0,0);if(hjLive()){HJ.h.go=true;return}SFX.jump()}
// every other jump sound: the blast, unless the clip is already playing (the arrival after a gate jump)
{const o=SFX.jump;SFX.jump=function(){if(hjLive()){HJ.h.go=true;return}if(hjStart(HJ.lead-.12))return;return o.apply(this,arguments)}}
// a countdown that ends without a jump fades the charge out
{const o=auFrame;auFrame=function(){try{const h=HJ.h;if(h&&h.cd&&!h.go&&!(W&&W.gc))hjStop(.25)}catch(e){}return o.apply(this,arguments)}}
// ---- the gate powers up with the charge (14 Nov 2026; the user: "the build up needs a visual at the gate showing that
// powerup"). k runs from 0 as the charge starts to 1 at the jump, so the picture follows the sound:
//   - the twelve emitters light one after another round the ring, each throwing a beam toward the centre that reaches
//     further as the charge builds;
//   - a core of light grows at the ring's centre and pulses faster, sparks are drawn inward, the ring's film brightens;
//   - at the jump the core flashes and a ring of light is thrown outward.
function gateChK(g){if(!W)return 0;if(W.gc&&W.gc.g===g)return clamp(1-(unbGateHold()-W.gc.t)/HJ.lead,0,1);if(W.jump&&W.jump.g===g)return 1;return 0}
const GATE_C0=[.45,.7,1],GATE_C1=[0,0,0];
function gateDiscC(g){const k=gateChK(g);if(k<=0)return GATE_C0;GATE_C1[0]=.45+.4*k;GATE_C1[1]=.7+.24*k;GATE_C1[2]=1;return GATE_C1}
function gateDiscA(g,t){const k=gateChK(g),a=.2+.06*Math.sin(t*3);if(k<=0)return a;const jt=W.jump&&W.jump.g===g?W.jump.t:-1;return a+k*(.2+.06*Math.sin(t*(6+20*k)))+(jt>=0?.25*Math.max(0,1-jt/.5):0)}
function gateFx(t){const g=W.gc?W.gc.g:W.jump?W.jump.g:null;if(!g)return;const k=gateChK(g);if(k<=0)return;const jt=W.jump?W.jump.t:-1,fade=jt>=0?Math.max(0,1-jt/.9):1,C=GATE_C0,WT=ONE3;
  qLook(-g.x,-g.y,-g.z,0,1,0,_qs);qMul(_qs,qAxis(0,0,1,t*.15,_qs2),_qs);
  if(fade>0){const n=jt>=0?12:Math.min(12,Math.ceil(k*12));
    for(let i=0;i<n;i++){const a=i/12*TAU;qRot(_qs,Math.cos(a)*86,Math.sin(a)*86,0,_u);const ox=_u.x,oy=_u.y,oz=_u.z,x=g.x+ox,y=g.y+oy,z=g.z+oz,on=jt>=0?1:clamp(k*12-i,0,1),fl=.75+.25*Math.sin(t*23+i*1.7);
      sprite(x,y,z,(7+7*k)*on*fl,C,.8*on*fade);sprite(x,y,z,3.5*on,WT,.9*on*fade);
      const r=jt>=0?1:clamp((k*12-i)/4,0,1)*(.25+.75*k);streak(x,y,z,x-ox*r,y-oy*r,z-oz*r,1.2+2.2*k,C,(.25+.45*k)*fl*fade)}
    const pu=1+.08*Math.sin(t*(8+18*k));sprite(g.x,g.y,g.z,(6+38*k*k)*pu,WT,(.25+.5*k)*fade);sprite(g.x,g.y,g.z,(20+85*k*k)*pu,C,(.1+.18*k)*fade);
    for(let i=0;i<18;i++){const u=(i*.618+t*(.35+.9*k))%1,a=i*2.399+t*1.3+u*3,r=92*(1-u);qRot(_qs,Math.cos(a)*r,Math.sin(a)*r,0,_u);sprite(g.x+_u.x,g.y+_u.y,g.z+_u.z,2+3*k,C,.7*k*u*fade)}}
  if(jt>=0){const f=Math.max(0,1-jt/.7);if(f>0){sprite(g.x,g.y,g.z,120+900*Math.min(1,jt/.25),WT,.85*f);
      for(let i=0;i<24;i++){const a=i/24*TAU,r=100+jt*700;qRot(_qs,Math.cos(a)*r,Math.sin(a)*r,0,_u);sprite(g.x+_u.x,g.y+_u.y,g.z+_u.z,14+30*f,C,.6*f)}}}}
