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
  HJ.h={s,g,end:t+b.duration-off,cd:!!cd,go:!cd};try{voice(b.duration-off)}catch(e){}return true}
// rem = seconds until the jump, every frame of the countdown
function gjCharge(rem){if(rem<=HJ.lead&&rem>.4&&!hjLive())hjStart(HJ.lead-rem,true)}
// a whole second of the countdown has passed; n seconds remain
function gjCount(n){if(!SND.b.cdBeep){SFX.count(n===1);return}if(n<=3)smp('cdBeep',HJ.beep,1/PITCH,0,0)}
// the ship jumps
function gjGo(){if(SND.b.cdGo)smp('cdGo',HJ.go,1/PITCH,0,0);if(hjLive()){HJ.h.go=true;return}SFX.jump()}
// every other jump sound: the blast, unless the clip is already playing (the arrival after a gate jump)
{const o=SFX.jump;SFX.jump=function(){if(hjLive()){HJ.h.go=true;return}if(hjStart(HJ.lead-.12))return;return o.apply(this,arguments)}}
// a countdown that ends without a jump fades the charge out
{const o=auFrame;auFrame=function(){try{const h=HJ.h;if(h&&h.cd&&!h.go&&!(W&&W.gc))hjStop(.25)}catch(e){}return o.apply(this,arguments)}}
