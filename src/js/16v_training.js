//@src 16v_training.js
// ============================================================ training, rewritten for Beyond in sections
// Each section is its own short course, started from Training on the start screen in a private practice galaxy. The pilot
// starts as an independent contractor docked at the freeport picked on the start screen, with Beyond's ship systems (slots,
// payload, the landing kit) switched on; the rest of Beyond (customs, Rating, crews) stays quiet so the lesson is calm.
// Section 1, Flight: the controls, the ways to fly (by hand, afterburner, flight assist off, auto-level, autopilot, landing on
// a rock, docking, jumping a gate on a set course) and taking a first job.
const BT_SECTIONS=[{k:'b1',name:'1 · Flight and your first job',les:'Flight and your first job',blurb:'The controls and every way to fly: thrust and steering, braking, rolling, the afterburner, flight assist off, auto-level, the cameras, landing on a rock, autopilot and docking, then taking a job and flying its course through a gate.'},
  {k:'b2',name:'2 · Contracts and standing',soon:1},{k:'b3',name:'3 · Combat',soon:1},{k:'b4',name:'4 · Mining',soon:1},{k:'b5',name:'5 · Trade and makers',soon:1},
  {k:'b6',name:'6 · Outfitting',soon:1},{k:'b7',name:'7 · Intel',soon:1},{k:'b8',name:'8 · Smuggling',soon:1},{k:'b9',name:'9 · Building up',soon:1},{k:'b10',name:'10 · The powers',soon:1}];
{const o=loadOn;loadOn=function(){return!!S&&!S.unb&&(!S.training||!!S.training.by)}}
const btSpd=()=>W&&W.player?hyp(W.player.vx,W.player.vy,W.player.vz):0;
function btHeld(id,k,secs){const T=S.training;T.v=T.v||{};const on=!!keys[KEY_DEF[id]]||!!keys[keyOf(KEY_DEF[id])];if(!on){T.v[k]=0;return false}T.v[k]=T.v[k]||W.t;return W.t-T.v[k]>=secs}
TRAIN.push({t:'Flight and your first job',setup:()=>{const T=S.training;T.v={home:S.player.sector}},steps:[
  {x:()=>`Welcome to flight school. You're an independent contractor, docked at ${esc(S.stations[S.player.sector].name)}: no faction owns you, and every power will hire you if your standing allows. This lesson covers flying your ship every way it flies, then taking your first job. Skip any step with the buttons below. Press <kbd>${kb('act')}</kbd> to launch.`,ok:()=>!S.player.docked},
  {x:()=>`<b>Thrust and steering.</b> <kbd>${kb('thrust')}</kbd> thrusts. The mouse steers: the further the pointer sits from the centre ring, the harder you turn (the arrow keys work too). Reach <b>150 m/s</b>.`,ok:()=>btSpd()>150},
  {x:()=>`<b>Braking.</b> <kbd>${kb('brake')}</kbd> brakes. Slow to under <b>20 m/s</b>.`,ok:()=>btSpd()<20},
  {x:()=>`<b>Rolling.</b> <kbd>${kb('rollL')}</kbd> and <kbd>${kb('rollR')}</kbd> roll the ship round its nose. Hold one for a second.`,ok:()=>btHeld('rollL','rl',.8)||btHeld('rollR','rr',.8)},
  {x:()=>`<b>The afterburner.</b> Hold <kbd>${kb('thrust')}</kbd> and <kbd>Shift</kbd>: a kick of speed, then a higher top speed while you hold it. It drains energy and needs a little back before it lights again. Get above <b>200 m/s</b>.`,ok:()=>(keys.ShiftLeft||keys.ShiftRight)&&btSpd()>200},
  {x:()=>`<b>Flight assist off.</b> With assist on, your ship bleeds off sideways slip, so it flies where it points. Press <kbd>${kb('fa')}</kbd> to switch it off: now you drift on your heading and can turn your nose freely, firing behind you while you fly away. Thrust changes your course.`,ok:()=>S.player.fa===false},
  {x:()=>`Turn while you coast and watch the speed hold as your nose swings. Press <kbd>${kb('fa')}</kbd> again to switch assist back on.`,ok:()=>S.player.fa!==false},
  {x:()=>`<b>Auto-level.</b> By default the ship rolls back level with the system's plane. Press <kbd>${kb('level')}</kbd> to switch auto-level off for full six-axis freedom.`,ok:()=>S.player.level===false},
  {x:()=>`Press <kbd>${kb('level')}</kbd> again to switch auto-level back on.`,ok:()=>S.player.level!==false},
  {x:()=>`<b>Cameras.</b> <kbd>${kb('cam')}</kbd> switches to the cockpit view.`,ok:()=>cam.mode==='cockpit'},
  {x:()=>`<kbd>${kb('cam')}</kbd> again for the chase camera. The mouse wheel sets how far behind it sits.`,ok:()=>cam.mode==='chase'},
  {x:()=>`<b>Landing on a rock.</b> Your ship carries a landing kit. Press <kbd>${kb('ast')}</kbd> to target the nearest rock.`,ok:()=>W.tgt&&W.tgt.kind==='ast'},
  {x:()=>`Fly to it, slow below ${LAND_SPD} m/s close to its surface, and press <kbd>${kb('act')}</kbd> to land. Landed, your systems power down and you drop off enemy sensors beyond close range.`,ok:()=>!!(W.player&&W.player.landed)},
  {x:()=>`Press <kbd>${kb('act')}</kbd> to lift off. Your weapons and shields take a few seconds to reboot.`,ok:()=>W.player&&!W.player.landed},
  {x:()=>`<b>Autopilot.</b> Press <kbd>${kb('cycle')}</kbd> until the freeport is targeted, then <kbd>${kb('autopilot')}</kbd>: autopilot flies you to your target.`,ok:()=>apOn&&W.tgt&&W.tgt.kind==='station'},
  {x:()=>`<b>Docking.</b> Near the station, press <kbd>${kb('act')}</kbd> to dock: the clamps line you up and draw you in. (<kbd>${kb('autopilot')}</kbd> takes the stick back any time.)`,ok:()=>S.player.docked==='station'},
  {x:()=>`<b>Your first job.</b> Docking repaired and rearmed you. Open the <b>Jobs</b> tab (<kbd>3</kbd>).`,setup:()=>{for(let i=0;i<8;i++)try{scheduleContract()}catch(e){}},ok:()=>!$('dock').hidden&&dockTab==='jobs'},
  {x:()=>`Every job here names who issues it and what it pays. A power pays from its own treasury, and work for it raises your standing with it. Pick a job from the list and press <b>Select job</b>.`,ok:()=>!!(JTRACK||S.player.job)},
  {ack:1,ok:()=>!!S.training.ack,x:()=>`<b>Your job is set.</b> Its course is on your map and HUD, and its issuer pays when it's done. Delivery jobs want goods you mined, salvaged or made; escorts and raids want you there with your guns. Standing opens doors: Unwelcome powers won't hire you, Trusted ones pay their bonuses, and below Hostile their ships shoot on sight.`},
  {x:()=>`<b>Jumping.</b> Launch (<kbd>${kb('act')}</kbd>) and press <kbd>${kb('autopilot')}</kbd>: with a course set, autopilot flies it gate by gate. To jump by hand, point your nose through a gate ring and hold steady. Make one jump.`,setup:()=>{const P=S.player;if(!P.route||P.route===P.sector)P.route=NEIGH[P.sector][0]},ok:()=>S.player.sector!==S.training.v.home&&!S.player.docked},
  {ack:1,ok:()=>!!S.training.ack,x:()=>`<b>That's flight.</b> You've flown by hand and on autopilot, with assist on and off, landed on a rock, docked and jumped. Keep flying this practice galaxy, finish your job, or exit; the next sections cover contracts and standing, combat, mining and more.`}]});
TR_TRACKS.b1={name:'Flight and your first job',les:['Flight and your first job']};
{const o=trPlan;trPlan=function(track){if(String(track).startsWith('b')){const s=BT_SECTIONS.find(x=>x.k===track);const i=s&&trIdx(s.les);return i>=0?[i]:[]}return o.apply(this,arguments)}}
// a Beyond section starts as a contractor at the freeport picked on the start screen, with Beyond's ship systems on
{const o=trainStart;trainStart=function(track){if(!String(track).startsWith('b'))return o.apply(this,arguments);$('trPick').hidden=true;const plan=trPlan(track),cs=cleanCall($('mpName').value)||'Cadet';auInit();auApply();FEED.length=0;
  const port=START_PORTS[selPort]?selPort:'mw';newGame(START_PORTS[port].design,'interceptor',cs,port);S.player.name=cs;S.training={plan,k:0,i:plan[0],track,j:0,done:[],v:{},html:'',by:1};document.body.classList.add('trn');startWith(S);
  feed(`Welcome to flight school, ${cs}. This is a private practice galaxy: nothing here touches your saved pilot.`,'good');trEnter()}}
{const o=trPickHtml;trPickHtml=function(){return`<div class="trh2">Flight school</div><p>Short sections, each on its own, in a private practice galaxy. You start as a contractor at the freeport you picked.</p><div class="trbs" style="flex-direction:column;align-items:stretch">${BT_SECTIONS.map(s=>`<button class="btn ${s.soon?'':'pri'}" type="button" data-trk="${s.k}" ${s.soon?'disabled':''} title="${esc(s.blurb||'Coming soon')}">${esc(s.name)}${s.soon?' · coming soon':''}</button>`).join('')}<button class="btn" type="button" data-trk="x">Close</button></div>`}}
