# usage: python3 tools/tests/mp_coop.py $PWD/index.html  (needs Playwright with Chromium)
# The co-op audit against the Ace of the Airways lessons (21 Nov 2026), from a guest's side over the faked link:
#   no copy of the guest's own ship; an AI ship's name set at spawn and one set after it was first sent both reach the
#   guest; an AI ship leaving by a gate leaves its lunge-through-the-ring picture on the guest's screen (it blinked out);
#   an old snapshot arriving after a newer one is dropped, and so is an old or wrong-system flight input on the host;
#   the Jobs-here count is worked out again in a new system; two pilots through one gate come out apart; a guest's own
#   shield hit is drawn where the shot struck; the guest has the galaxy's length rule; the Guided start refuses a guest;
#   a won galaxy keeps every pilot's solo save, and a guest (re)joining a won galaxy sees the win screen without the win
#   counted twice; ledger exact.
import json
from mpkit import run

async def body(K):
  G,Hh,chk=K.G,K.Hh,K.check
  await K.undock();await K.wait(2000)
  sid=await G("S.player.sector");print('guest in',sid,flush=True)
  # recorders on the guest: gate pictures made, the last snapshot applied
  await G("(()=>{window.__go=[];const o=gateOutFx;gateOutFx=function(e,g){const r=o.apply(this,arguments);__go.push([e&&e.id,r]);return r};window.__sn=null;const a=applySnap;applySnap=function(m){window.__sn=JSON.stringify(m);return a.apply(this,arguments)};return 1})()")
  await Hh("(()=>{window.__u=null;const o=hostRecv;hostRecv=function(L,m){if(m&&m.t==='u')window.__u=JSON.stringify(m);return o.apply(this,arguments)};return 1})()")
  # 2. no copy of your own ship
  r=await G("(()=>{const w=LW;return JSON.stringify({pup:!!(w.pup&&w.pup['p_clipid1']),twins:w.ents.filter(e=>e!==w.player&&e.type==='ship'&&(e.rp==='clipid1'||e.id==='p_clipid1')).length})})()")
  r=json.loads(r);chk('no copy of the guest\'s own ship',not r['pup'] and r['twins']==0,r)
  # 1. names: one set at spawn, one set after the ship was first sent
  ids=await Hh("""(()=>{const w=WORLDS[%s],me=MP.rp.clipid1;let A,B;inW(w,()=>{devLedger(()=>{A=makeNPC('patrol','neutral','interceptor',1,{},'coop:a');B=makeNPC('patrol','neutral','interceptor',1,{},'coop:b')});
    A.pname='★ Early Name';for(const[e,k]of[[A,1],[B,-1]]){e.x=me.x+900*k;e.y=me.y+200;e.z=me.z;W.ents.push(e)}});window.__AB=[A,B];return JSON.stringify([A.id,B.id])})()"""%json.dumps(sid))
  A,B=json.loads(ids);await K.wait(1500)
  await Hh("(()=>{__AB[1].pname='☠ Late Name';window.__f0=0;return 1})()")
  # full rows go out every 31 snapshots (2 s at 15 a second; headless frames run slower): wait for 40 snapshots
  await G("(()=>{window.__nsn=0;const a=applySnap;applySnap=function(m){__nsn++;return a.apply(this,arguments)};return 1})()")
  for i in range(40):
    await K.wait(500)
    if await G("__nsn>=40"):break
  r=json.loads(await G("(()=>{const w=LW,a=w.pup[%s],b=w.pup[%s];return JSON.stringify({a:a?a.pname||null:'nopup',b:b?b.pname||null:'nopup',lb:b?shipLabel(b):null,snaps:__nsn})})()"%(json.dumps(A),json.dumps(B))))
  chk('a name set at spawn reaches the guest',r['a']=='★ Early Name',r)
  chk('a name set after the first announcement reaches the guest',r['b']=='☠ Late Name' and 'Late Name' in (r['lb'] or ''),r)
  # 3. an AI ship through a gate: the guest gets the picture
  cid=await Hh("""(()=>{const w=WORLDS[%s];let C;inW(w,()=>{devLedger(()=>{C=makeNPC('patrol','neutral','interceptor',1,{},'coop:c')});const g=GATES[W.sid][0],d=gateAxis(g);C.x=g.x-d.x*80;C.y=g.y-d.y*80;C.z=g.z-d.z*80;W.ents.push(C)});window.__C=C;return C.id})()"""%json.dumps(sid))
  await K.wait(1500)
  known=await G("!!LW.pup[%s]"%json.dumps(cid))
  r=await Hh("""(()=>{const w=WORLDS[%s],C=__C;let out=null;inW(w,()=>{const g=GATES[W.sid][0],d=gateAxis(g);C.x=g.x-d.x*80;C.y=g.y-d.y*80;C.z=g.z-d.z*80;C.gj={g,t:GATE_HOLD};const n0=(W.gouts||[]).length;out=npcGateJump(C,g,.02);out=JSON.stringify({jumped:out,alive:C.alive,gouts:(W.gouts||[]).length-n0})});return out})()"""%json.dumps(sid))
  print('host gate jump:',r,flush=True);await K.wait(800)
  g=json.loads(await G("JSON.stringify({go:__go,pup:!!LW.pup[%s]})"%json.dumps(cid)))
  chk('an AI ship\'s gate departure is drawn on the guest',known and any(x[0]==cid and x[1] for x in g['go']),{'known':known,**g})
  # 6. ordering: an old snapshot after a newer one; an old or wrong-system input on the host
  old=await G("__sn");await K.wait(600)
  r=json.loads(await G("""(()=>{const m=JSON.parse(%s),id=%s,e=LW.pup[id];if(!e)return JSON.stringify({err:'no pup'});const tx0=e.tx;for(const row of m.e)if(row[0]===id)row[row.length>16?8:1]+=5000;m.ev=[];const n0=MP.nst?MP.nst.old:0;clientRecv(m);return JSON.stringify({tx0,tx1:e.tx,old:(MP.nst?MP.nst.old:0)-n0})})()"""%(json.dumps(old),json.dumps(A))))
  chk('an old snapshot after a newer one is dropped',r.get('tx0') is not None and abs(r['tx1']-r['tx0'])<1000,r)
  uo=await Hh("__u");await K.wait(600)
  r=json.loads(await Hh("""(()=>{const m=JSON.parse(%s),P=S.pilots.clipid1,x0=P.x;m.x+=5000;linkRecv(window.__HL,JSON.stringify(m));const x1=P.x;const m2=JSON.parse(%s);m2.x+=7000;m2.n=(m2.n||0)+1e6;m2.s=P.sector==='mw'?'ew':'mw';linkRecv(window.__HL,JSON.stringify(m2));const x2=P.x;return JSON.stringify({x0,x1,x2,nst:MP.nst||null})})()"""%(json.dumps(uo),json.dumps(uo))))
  chk('an old flight input is dropped on the host',abs(r['x1']-r['x0'])<1000,r)
  chk('a flight input from another system is dropped on the host',abs(r['x2']-r['x0'])<1000,r)
  await K.wait(800)
  r=json.loads(await Hh("JSON.stringify({x:S.pilots.clipid1.x,ex:MP.rp.clipid1&&MP.rp.clipid1.x})"))
  r2=json.loads(await G("JSON.stringify({x:W.player.x})"))
  chk('the guest\'s next real inputs still land on the host',abs(r['x']-r2['x'])<600,[r,r2])
  # leads: a guest's own shield hit drawn where the shot struck
  r=json.loads(await G("""(()=>{const p=W.player;qRot(p.q,0,0,1,_f);const sh0=p.shield;W.shots.push({x:p.x+_f.x*120,y:p.y+_f.y*120,z:p.z+_f.z*120,vx:p.vx-_f.x*1400,vy:p.vy-_f.y*1400,vz:p.vz-_f.z*1400,ttl:1,col:'#fff',side:'brood',src:null,dmg:0});return JSON.stringify({sh0,hostile:hostE('brood',p)})})()"""))
  await K.wait(400)
  r2=json.loads(await G("JSON.stringify({shh:!!W.player._shh,last:W.player._shh?Math.max(W.player._shh[3],W.player._shh[7],W.player._shh[11]):null,t:W.t})"))
  chk('a guest\'s own shield hit is drawn where the shot struck',r['sh0']>0 and r2['shh'] and r2['t']-r2['last']<2,[r,r2])
  # 10. the Jobs-here count and 13. arrival spot, with one jump
  # (the old count was kept until the new system's clock passed the old one's, so let this one's clock run a while first)
  for i in range(40):
    if await G("W.t>12"):break
    await K.wait(500)
  await G("(()=>{cjCnt.t=W.t;cjCnt.n=77;cjCnt.w=W;return 1})()")
  wt=await G("W.t");print('guest world clock before the jump',wt,flush=True)
  r=json.loads(await G("""(()=>{const from=W.sid,to=NEIGH[from].find(s=>!S.gateDown[gateKey(from,s)]);doJump(to);const g=GATES[to].find(x=>x.to===from),p=W.player,l=hyp(g.x,g.y,g.z),ux=g.x/l,uy=g.y/l,uz=g.z/l,rx=p.x-g.x,ry=p.y-g.y,rz=p.z-g.z,al=rx*ux+ry*uy+rz*uz;return JSON.stringify({to,lat:Math.round(hyp(rx-ux*al,ry-uy*al,rz-uz*al)),slot:typeof arrSlot==='function'?arrSlot(S.player.pid):null,roster:MP.roster.map(r=>r[0])})})()"""))
  print('jump:',r,flush=True)
  chk('a second pilot through a gate comes out beside the axis, not on it',r['lat']>=50,r)
  await K.wait(4500)
  r=json.loads(await G("JSON.stringify({n:cjCnt.n,same:cjCnt.w===W,t:W.t,sid:W.sid})"))
  chk('the Jobs-here count is worked out again in the new system',r['n']!=77,r)
  # leads: the galaxy's length rule on the guest
  hg=json.loads(await Hh("JSON.stringify({g:S.glen,need:LEN.need,floor:LEN.floor})"));cg=json.loads(await G("JSON.stringify({g:S.glen,need:LEN.need,floor:LEN.floor,note:lenMapNote()})"))
  chk('the guest has the host\'s game-length rule',hg['g']==cg['g'] and hg['need']==cg['need'] and hg['floor']==cg['floor'] and 'length' in cg['note'],[hg,cg])
  # leads: the Guided start refuses a guest with a message
  r=json.loads(await G("(()=>{const n=FEED.length;GD.want=true;gdWantCheck();return JSON.stringify({guide:!!S.player.guide,want:GD.want,msg:FEED.slice(n).map(f=>f.msg).join(' | ').slice(0,160)})})()"))
  chk('the Guided start refuses a guest with a message',not r['guide'] and not r['want'] and 'guided' in r['msg'].lower(),r)
  # 11. the win: solo saves kept; a guest joining a won galaxy sees the win screen, the win not counted twice
  for pg in (K.H,K.C):await pg.evaluate("c=>__dg.ev(c)","(()=>{localStorage.setItem(SAVE_KEY,'coop-sentinel');return 1})()")
  await Hh("(()=>{galaxyWon('halcyon');return 1})()");await K.wait(1500)
  r=json.loads(await G("JSON.stringify({win:!$('win').hidden,save:localStorage.getItem(SAVE_KEY),lg:localStorage.getItem('dgbeyond.legacy')})"))
  hs=await Hh("localStorage.getItem(SAVE_KEY)")
  chk('the guest sees the win',r['win'],r)
  chk('a shared win keeps every pilot\'s solo save',r['save']=='coop-sentinel' and hs=='coop-sentinel',{'guest':r['save'],'host':hs})
  lg0=r['lg']
  await G("(()=>{$('win').hidden=true;return 1})()")
  await Hh("(()=>{const c=Object.values(MP.cl)[0];hJoin(c);return 1})()");await K.wait(2500)
  r=json.loads(await G("JSON.stringify({win:!$('win').hidden,lg:localStorage.getItem('dgbeyond.legacy'),running})"))
  chk('a guest (re)joining a won galaxy sees the win screen',r['win'],r)
  chk('seeing it again does not count the win twice',r['lg']==lg0,{'before':lg0,'after':r['lg']})
  for pg in (K.H,K.C):await pg.evaluate("c=>__dg.ev(c)","(()=>{localStorage.removeItem(SAVE_KEY);return 1})()")

run(body)
