//@src 16zzd_yard.js
// ============================================================ the shipyard, reorganised (Beyond, 3 Nov 2026)
// The user's asks: the hull picked in a dropdown (grouped by kind: Fighters, Bombers, Haulers, Miners, Scouts, Other, with
// prices) shows its full card and a button to take it, and turns in a box on the right with its numbers against yours; a hull your Rating
// doesn't reach says what it needs in plain words (one Contractor Rating, earned by work for any power, not a power's own).
// Station works shows only at your own base: elsewhere it had nothing to do.
const YARD_CAT=[['fighters','Fighters',['interceptor','striker','heavy','wraith']],['bombers','Bombers',['bomber','gunboat']],['haulers','Haulers',['courier','freighter','bulker']],['miners','Miners',['skiff','prospector','dredger']],['scouts','Scouts',['scout','scout2']]];
let yardSel=null,yardRaf=0;
function yardCatOf(k){const c=YARD_CAT.find(x=>x[2].includes(k));return c?c[0]:'other'}
function yardFac(c,P,k){if(k===P.cls)return P.faction;return(typeof yardDesign==='function'&&yardDesign(c,k))||P.faction}
function yardPrice(P,k){if(P.cls===k)return'yours';const pr=hullOwned(P,k)?0:hullPrice(k)-vchOf(P,k),t=pr>0?`${fmt(pr)} cr`:'free';return hullRatingOK(P,k)?t:`${t} · needs Rating ${HULL_RATING[k]}`}
function yardStats(c,P,k){const st=k===P.cls?shipStats(P.faction,P.cls,P.tiers,P.tune):shipStats(yardFac(c,P,k),k,baseTiers()),C=CLASSES[k],D=slotsOf(k,designOf(yardFac(c,P,k),k)?yardFac(c,P,k):null);
  return{hull:Math.round(st.hull),shield:Math.round(st.sCap),speed:Math.round(st.maxSpd),hold:st.cargo,drones:C.drones||0,w:D.w.length,u:D.u.length}}
function yardInfo(c,P,k){const a=yardStats(c,P,k),b=k===P.cls?null:yardStats(c,P,P.cls),C=CLASSES[k],d=(x,y,u)=>b&&x!==y?` <span class="mass" style="margin:0;color:${x>y?'#7ad9a7':'var(--danger)'}">${x>y?'+':'−'}${fmt(Math.abs(x-y))}${u||''}</span>`:'',kv=(n,x,y,u)=>`<div class="kv"><span>${n}</span><b>${fmt(x)}${u||''}${d(x,y,u)}</b></div>`;
  return`<div class="lab">${k===P.cls?'You fly':'Selected'}</div><div style="font-size:20px;font-weight:700;line-height:1.1">${esc(FAC(yardFac(c,P,k)).hulls[k]||C.name)}</div><div class="note" style="margin:2px 0 8px">${esc(C.name)}${b?' · compared with yours':''}</div>`+
    kv('Hull',a.hull,b&&b.hull)+kv('Shield',a.shield,b&&b.shield)+kv('Top speed',a.speed,b&&b.speed,' m/s')+kv('Hold',a.hold,b&&b.hold,' t')+(a.drones||(b&&b.drones)?kv('Drones',a.drones,b&&b.drones):'')+kv('Weapon slots',a.w,b&&b.w)+kv('Utility slots',a.u,b&&b.u)}
function yardSpin(){yardRaf=0;const cv=$('yardPic');if(!cv||$('dock').hidden||!G||!MDL.ready)return;const w=cv.clientWidth,h=cv.clientHeight;if(w&&h){if(cv.width!==w*DPR){cv.width=w*DPR;cv.height=h*DPR}
    const c=cv.getContext('2d');c.setTransform(DPR,0,0,DPR,0,0);c.clearRect(0,0,w,h);const P=S.player,k=yardSel||P.cls,f=cv.dataset.fac||P.faction;
    try{const d=shipMesh(f,k).hull.data,a=performance.now()/1000*.6,q=qMul(qAxis(1,0,0,.38,q0()),qAxis(0,1,0,a,q0()),q0()),s=Math.min(w,h)*.46/stR(d);stDraw(c,d,q,w/2,h/2,s,1)}catch(e){}}
  yardRaf=requestAnimationFrame(yardSpin)}
// the user's second pass: a dropdown of hulls in their kinds, with prices; the picked hull's full card and a button to take it
// on the left; the turning picture and its numbers (against your current hull) on the right
{const o=renderDock;renderDock=function(){const r=o.apply(this,arguments);try{if(dockTab!=='ship'||S.unb)return r;const body=$('dBody'),box=body&&body.querySelector('.ships');if(!box||box.dataset.yd)return r;
  const btns=[...box.querySelectorAll('button.cls[data-act="hull"]')];if(!btns.length)return r;const P=S.player,c=dockCtx(),keys=btns.map(b=>b.dataset.arg);if(!yardSel||!keys.includes(yardSel))yardSel=P.cls;
  for(const b of btns)for(const t of b.querySelectorAll('.req.no'))t.textContent=t.textContent.replace(/^needs Rating (\d+)$/,(m,n)=>`needs Contractor Rating ${n} (you're ${ratingOf(P)}): earned by work for any power`);
  const cats=[...YARD_CAT,['other','Other',[]]];let opts='';
  for(const[k,n]of cats){const L=keys.filter(x=>yardCatOf(x)===k);if(!L.length)continue;opts+=`<optgroup label="${n}">${L.map(x=>`<option value="${x}"${x===yardSel?' selected':''}>${esc(FAC(yardFac(c,P,x)).hulls[x]||CLASSES[x].name)} · ${esc(CLASSES[x].name)} · ${esc(yardPrice(P,x))}</option>`).join('')}</optgroup>`}
  const sb=btns.find(b=>b.dataset.arg===yardSel),k=yardSel,can=sb&&!sb.disabled&&P.cls!==k,pr=yardPrice(P,k);
  const wrap=document.createElement('div');wrap.className='yd2';
  wrap.innerHTML=`<div class="ydleft"><label class="lab" for="yardSelEl" style="display:block;margin-bottom:4px">Hull</label><select id="yardSelEl" class="ydsel">${opts}</select><div class="ydcard"></div>
      <div class="act" style="margin-top:10px;justify-content:flex-start"><button class="btn${can?' pri':''}" type="button" data-act="hull" data-arg="${k}" ${can?'':'disabled'}>${P.cls===k?'Your current hull':can?`Take the ${esc(FAC(yardFac(c,P,k)).hulls[k]||CLASSES[k].name)} · ${esc(pr)}`:(!hullRatingOK(P,k)?`Needs Contractor Rating ${HULL_RATING[k]} (you're ${ratingOf(P)})`:sb&&/orbital docks/.test(sb.textContent)?'Sold at orbital docks only':P.credits<(hullPrice(k)-vchOf(P,k))?`${esc(pr)}: not enough credits`:`Not available here`)}</button></div></div>
    <div class="ydpic"><canvas id="yardPic" data-fac="${yardFac(c,P,k)}" aria-label="The selected ship"></canvas><div class="ydinfo">${yardInfo(c,P,k)}</div></div>`;
  if(sb){const card=document.createElement('div');card.className='cls ydc'+(P.cls===k?' on':'');card.innerHTML=sb.innerHTML;wrap.querySelector('.ydcard').appendChild(card)}
  wrap.querySelector('#yardSelEl').addEventListener('change',e=>{yardSel=e.target.value;renderDock()});
  box.dataset.yd=1;box.replaceWith(wrap);if(!yardRaf)yardRaf=requestAnimationFrame(yardSpin)}catch(e){console.error(e)}return r}}
// Station works: your own base (or your power's station when sworn) only
{const o=dockCtx;dockCtx=function(){const c=o.apply(this,arguments);try{if(c&&c.works&&!c.haven&&c.owner!=='player'){c.works=false;if(dockTab==='works')dockTab='home'}}catch(e){}return c}}
// the dock's top menu (user, 3 Nov 2026): Fabricate moves under Trade; Patronage (sponsoring a power's projects) under
// Allegiance; Allegiance becomes 5 and Station 6, and Station (works, your outpost) shows only at your own base
{const T=DOCK_TOP,g=k=>T.find(x=>x[0]===k),tr=g('trade'),st=g('station'),al=g('allegiance');
  if(tr&&!tr[2].includes('fab')){const i=tr[2].indexOf('trade');tr[2].splice(i>=0?i+1:tr[2].length,0,'fab')}
  if(st)st[2]=st[2].filter(k=>k!=='fab'&&k!=='patron');if(al&&!al[2].includes('patron'))al[2].push('patron');
  if(st&&al){T.splice(T.indexOf(st),1);T.splice(T.indexOf(al),1);T.push(al,st)}}
CLASSES.prospector.desc='A charge launcher, a mining laser and a gun, 3 guard drones (with its drone controller), mid hold.';CLASSES.dredger.desc='A charge launcher, a mining laser and a gun, 4 guard drones (with its drone controller), the deepest miner hold. Slow and armoured.';
CLASSES.skiff.desc='A mining laser and a charge launcher, 2 guard drones (with its drone controller), small hold. Nimble enough to run.';
