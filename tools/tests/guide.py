# Beyond, the guided start (11 Nov 2026): the top entry of the Training menu launches a real galaxy with a guide on the pilot.
# For each role (ROLES=combat,mining,hauling) the five steps are driven from real game events (flying is fast-forwarded by
# placing the ship and stepping the simulation; nothing is done that a player couldn't do): each step's pay is a real transfer
# from the Freeport Compact's treasury, the guide ends, Your path shows the right rung, the hidden controls appear on their
# conditions, the ledger stays exact. A fourth pilot checks that a skipped step pays nothing, that a save and load keeps the
# guide's state, that End guide gives every control back, and that a pilot who used Launch has no guide at all.
import asyncio,json,os,sys
from playwright.async_api import async_playwright
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
ROLES=[r for r in os.environ.get('ROLES','combat,mining,hauling').split(',') if r]
LED="(()=>{const L=ledger();for(const e of RAWS)if(Math.abs(L.tot[e]-S.ledger0.tot[e])>1e-6)return 'ore '+e+' '+(L.tot[e]-S.ledger0.tot[e]);return Math.abs(L.credits-S.ledger0.credits)<1e-6?'exact':'credits '+(L.credits-S.ledger0.credits)})()"
# test helpers inside the game's scope: the pay log (what each step asked the treasury for and what moved), fast-forward,
# and the moves a player makes, with the flying between them skipped
INJ="""(()=>{window._pay=[];const o=gdPay;gdPay=function(P,n){const G=P.guide,i=G.i,t0=S.econ.treasury.neutral,c0=P.credits,r=o.apply(this,arguments);_pay.push({i,want:n,got:r,dt:t0-S.econ.treasury.neutral,dc:P.credits-c0,T:Math.round(S.T)});return r};
window._ff=(n,dt)=>{for(let i=0;i<n;i++)step(dt||.05);return 1};
window._dock=()=>{const P=S.player;if(P.docked)return 1;if(W.docking||W.jump||W.dead)return 0;const SE=W.stationEnt,p=W.player;if(!SE||!p)return 0;apOn=false;W.fmn=null;keys.KeyF=false;p.x=SE.x+200;p.y=SE.y;p.z=SE.z;p.vx=p.vy=p.vz=0;p.boot=0;actPress();return 0};
window._gate=()=>{const P=S.player;if(P.docked){undock();return 0}if(W.jump||W.dead||!W.player)return 0;const g=routeNext();if(!g)return 1;const p=W.player;if(d3(p,g)>700){const dx=p.x-g.x,dz=p.z-g.z,l=Math.hypot(dx,dz)||1;p.x=g.x+dx/l*500;p.y=g.y;p.z=g.z+dz/l*500;p.vx=p.vy=p.vz=0;faceInstant(p,g.x-p.x,g.y-p.y,g.z-p.z)}apOn=true;return 0};
window._rock=()=>{const s=S.sectors[W.sid],SE=W.stationEnt;let a=s.ast.find(x=>x.id===window._rk);if(!a||oreTotal(a)<12){a=s.ast.filter(x=>!x.comet&&!x.rift&&oreTotal(x)>=30&&(!SE||d3(x,SE)>1200)&&(GATES[W.sid]||[]).every(g=>d3(x,g)>1200)).sort((x,y)=>oreTotal(y)-oreTotal(x))[0];window._rk=a&&a.id}return a};
window._mine=()=>{const P=S.player,p=W.player,s=S.sectors[W.sid],me=blKey(P);if(P.docked){undock();return 'undock'}if(W.jump||W.dead||!p)return 'wait';
  const cl=(s.clouds||[]).filter(x=>oreTotal(x)>0).sort((x,y)=>d3(x,p)-d3(y,p))[0];if(cl){p.x=cl.x;p.y=cl.y;p.z=cl.z;p.vx=cl.vx||0;p.vy=cl.vy||0;p.vz=cl.vz||0;keys.KeyF=true;return 'scoop'}
  keys.KeyF=false;const a=_rock();if(!a)return 'norock';
  if((s.charges||[]).some(c=>c.o===me)){const dx=p.x-a.x,dy=p.y-a.y,dz=p.z-a.z,l=Math.hypot(dx,dy,dz)||1,R=astR(a)+260;p.x=a.x+dx/l*R;p.y=a.y+dy/l*R;p.z=a.z+dz/l*R;p.vx=p.vy=p.vz=0;blDetonate(P,p);return 'det'}
  if(!(P.blN>0))return 'reload';const q=blPts(a)[0],dx=q.x-a.x,dy=q.y-a.y,dz=q.z-a.z,l=Math.hypot(dx,dy,dz);p.x=a.x+dx/l*(l+150);p.y=a.y+dy/l*(l+150);p.z=a.z+dz/l*(l+150);p.vx=p.vy=p.vz=0;faceInstant(p,-dx,-dy,-dz);W.tgt={kind:'ast',ref:a};p.blCd=0;blFire(p,P);return 'fire'};
window._form=()=>{const P=S.player;if(P.docked){undock();return 'undock'}if(W.jump||W.dead||!W.player)return 'wait';const E=fmEnt();if(!E)return 'nocharge';if(!W.fmn){W.tgt={kind:'ship',ref:E};apOn=false;toggleAutopilot()}return W.fmn?'formation':'no'};
// a guard job flown as a player would: take it at the dock (again, if a trip went wrong and it was posted again), fly in formation
window._guard=()=>{const P=S.player,G=P.guide,I=G.sv.mid!=null?indById(G.sv.mid):null,mine=!!(I&&I.guard&&sameK(I.guard.k,pkeyOf(P)));if(W.jump||W.dead||!W.player)return 'wait';
  if(mine&&I.sector!==P.sector&&!P.docked){W.fmn=null;return _gate()?'there':'following'}if(mine)return _form();if(!P.docked)return _dock()?'docked':'docking';if(!I)return 'nojob';$('dock').hidden=false;dockTab='home';renderDock();const sb=document.querySelector('#dock .gdcard [data-act=gdjob]');if(sb)sb.click();
  const tb=document.querySelector('#dock [data-act=igtake][data-arg="'+I.id+'"]');if(tb){tb.click();window._takes=(window._takes||0)+1;return 'take'}return 'notake'};
window._g=()=>JSON.stringify(S.player.guide);return 1})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);bad=[];errs=[]
    def check(n,ok,d=''):
      print(('ok  ' if ok else 'FAIL'),n,str(d)[:420])
      if not ok:bad.append(n)
    async def start(role,guided=True):
      cx=await b.new_context(viewport={'width':1440,'height':900});pg=await cx.new_page();pg.on('pageerror',lambda e:errs.append(role+': '+str(e)))
      pg.on('console',lambda m:errs.append(role+' console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
      await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
      await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.querySelector('#roles [data-role=%s]').click()"%role)
      if guided:
        await pg.evaluate("document.getElementById('bTrain').click()");await pg.wait_for_timeout(200)
        first=await pg.evaluate("(()=>{const L=[...document.querySelectorAll('#trPick [data-trk]')];return JSON.stringify({first:L[0].dataset.trk,txt:L[0].innerText.slice(0,200),n:L.length})})()")
        await pg.evaluate("document.querySelector('#trPick [data-trk=guided]').click()")
      else:
        first='{}';await pg.evaluate("document.getElementById('bLaunch').click()")
      await pg.wait_for_function('__dg.ev("!!(S&&S.player&&running)")',timeout=60000);await pg.wait_for_timeout(800)
      ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
      return pg,ev,json.loads(first)
    async def until(ev,cond,act,limit=200,ff=20):
      for i in range(limit):
        if await ev(cond):return True
        if act:await ev(act)
        await ev("_ff(%d)"%ff)
      return bool(await ev(cond))
    stepi="S.player.guide.i"
    async def now(ev):
      return await ev("(()=>{const G=S.player.guide,n=gdStepOn(S.player)&&gdNow(G,S.player);return n?String(n.d).replace(/<[^>]+>/g,'').slice(0,150):'done'})()")
    async def fail_at(ev,role,n,waited):
      print('FAIL %s step %d stuck: prompt "%s"; waited for: %s; state %s'%(role,n,await now(ev),waited,await ev("JSON.stringify({i:S.player.guide.i,sv:S.player.guide.sv,sector:S.player.sector,docked:S.player.docked,dead:!!(W&&W.dead),docking:!!(W&&W.docking),jump:!!(W&&W.jump),wsid:W&&W.sid,dSE:W&&W.stationEnt&&W.player?Math.round(d3(W.stationEnt,W.player)):null,landed:!!(W&&W.player&&W.player.landed),hull:W&&W.player?Math.round(W.player.hull):null,flash:flashMsg&&flashMsg.m,err:dockErr||''})")));bad.append('%s step %d'%(role,n))
    async def paid(ev,role,i,want,name):
      r=json.loads(await ev("JSON.stringify(_pay.filter(x=>x.i===%d))"%i));x=r[-1] if r else {}
      ok=len(r)==1 and x.get('got')==x.get('dt')==x.get('dc') and (want is None or x.get('got')==want) and x.get('got',0)>0
      check('%s step %d (%s): paid %s cr by a real transfer from the Compact treasury'%(role,i+1,name,x.get('got')),ok,r);l=await ev(LED);check('%s step %d: ledger exact'%(role,i+1),l=='exact',l);return x.get('T',0)
    async def shake(ev,role):
      await ev("(()=>{undock();return 1})()");await ev("_ff(40)")
      hud=await ev("(()=>{hudUpdate();const el=$('train');return JSON.stringify({hidden:el.hidden,txt:el.innerText.slice(0,160)})})()");h=json.loads(hud)
      check('%s: in flight the step shows in the HUD panel'%role,not h['hidden'] and 'GUIDED START' in h['txt'].upper() and 'SHAKEDOWN' in h['txt'].upper(),h)
      await ev("(()=>{const m=gdMarker(S.player.guide),p=W.player;p.x=m.x-60;p.y=m.y;p.z=m.z;p.vx=p.vy=p.vz=0;return 1})()")
      if not await until(ev,"!!S.player.guide.sv.hit||%s>0"%stepi,None,30):return await fail_at(ev,role,1,'the ship within %s m of the marker'%'220')
      if not await until(ev,stepi+">0","_dock()",200):return await fail_at(ev,role,1,'docked at the home freeport after the marker')
      return True
    async def part_choice(ev,role,scout=False):
      # step 4: buy a part on the Market and fit it
      if not await until(ev,"!!S.player.docked","_dock()",200):return await fail_at(ev,role,4,'docked')
      await ev("_ff(10)")
      r=json.loads(await ev("""(()=>{const P=S.player,c=dockCtx(),id=gdPartPick(c,P);if(!id)return JSON.stringify({id:null,cr:P.credits});
        const pr=mBuy(c,id),c0=P.credits;dockTab='market';renderDock();dockClick('buy',id+':1');const spent=c0-P.credits,px=(P.guide.sv.px||{})[id],T=ldTarget(P,id),n0=gdNow(P.guide,P);dockTab='upg';renderDock();dockClick('fit',T.g+':'+T.i+':'+id);
        return JSON.stringify({id,pr,spent,px,prompt:String(n0.d).replace(/<[^>]+>/g,'').slice(0,120),err:dockErr,i:P.guide.i,fitted:(T.g==='w'?fitOf(P).wi:fitOf(P).ui)[T.i]})})()"""))
      check('%s step 4: a part bought on the Market and fitted completes it'%role,r.get('id') and r.get('spent')>0 and r.get('px')==r.get('spent') and r.get('fitted')==r.get('id') and r.get('i')==4,r)
      if r.get('i')!=4:return await fail_at(ev,role,4,'a part fitted (dock action fit)')
      await paid(ev,role,3,r.get('spent'),'First upgrade')
      # step 5: any job from the board
      await ev("_ff(10)")
      r=json.loads(await ev("""(()=>{const P=S.player;dockTab='jobs';jobFilter='all';renderDock();const hid=!document.querySelector('#dock [data-act=intelfor]');const L=JOBS_LAST.filter(j=>%s);const j=L[0];if(!j)return JSON.stringify({job:null,n:JOBS_LAST.length});
        jobSel=j.id;renderDock();dockClick('jtrack',j.id);return JSON.stringify({job:j.id,ty:j.ty,hid,track:JTRACK&&JTRACK.id,err:dockErr})})()"""%("j.ty==='scout'" if scout else "j.ty!=='scout'&&!String(j.id).startsWith('igd:')")))
      check('%s step 5: a job taken from the board (%s)'%(role,r.get('job')),bool(r.get('track')),r)
      if not await until(ev,stepi+">4",None,20):return await fail_at(ev,role,5,'a job taken that the pilot was not on')
      t=await paid(ev,role,4,250,'Your choice')
      return r,t
    async def finish(ev,role,r5,T):
      r=json.loads(await ev("""(()=>{const P=S.player,G=P.guide;openDock('home');dockTab='home';renderDock();hudUpdate();const cur=document.querySelector('#dock .gdpath tr[data-cur]'),R=gdPath(dockCtx(),P),txt=(document.querySelector('#dock .gdpath')||{}).innerText||'';
        return JSON.stringify({i:G.i,done:!!G.done,on:G.on,card:!!document.querySelector('#dock .gdcard'),rung:cur&&+cur.dataset.rung,curName:R.find(x=>x.cur).n,first:R[0].done,co:$('bCompany').style.display,coNote:FEED.some(f=>/New in the top bar: Company/.test(f.msg)),
          vals:[fmt(COP.deposit),fmt(RATING.need[2]),CLASSES[KIT_HULL].name,'upgraded from a Depot','separate from the development modules',String(VIC_NEED)].filter(x=>!txt.includes(x)),paid:G.paid,tot:_pay.reduce((a,x)=>a+x.got,0),rating:ratingOf(P)})})()"""))
      check('%s: the guide ends after step 5, its card gone'%role,r['i']==5 and r['done'] and not r['card'],r)
      check('%s: Your path shows the next rung (Contractor Rating 2), the first ticked, its figures the game\'s own'%role,r['rung']==1 and 'Rating 2' in r['curName'] and r['first'] and not r['vals'],r)
      check('%s: the Company key appears when the first contract is finished, with a note'%role,r['co']=='' and r['coNote'],r)
      print('%s: all five steps done at %d simulated seconds; paid %s cr in all %s'%(role,T,r['tot'],r['paid']))
      l=await ev(LED);check('%s: ledger exact at the end'%role,l=='exact',l)
    async def hidden0(ev,role):
      r=json.loads(await ev("""(()=>{const P=S.player,G=P.guide;openDock('home');dockTab='home';renderDock();hudUpdate();const card=document.querySelector('#dock .gdcard'),cur=document.querySelector('#dock .gdpath tr[data-cur]'),ns=nextStep(dockCtx(),P);
        dockTab='jobs';renderDock();const intel=!!document.querySelector('#dock [data-act=intelfor]'),bm=dockG.some(g=>g[2].some(t=>t[0]==='bmjobs'||t[0]==='bmk'));dockTab='bmjobs';renderDock();const bmTab=dockTab;dockTab='home';renderDock();
        return JSON.stringify({guide:!!G,role:G&&G.role,home:G&&G.home,port:P.home,cls:P.cls,cr:P.credits,training:!!S.training,card:card?card.innerText.slice(0,200):'',nstep:!!document.querySelector('#dock .nstep'),nsGd:!!(ns&&ns.gd),rung:cur&&+cur.dataset.rung,intel,bm,bmTab,co:$('bCompany').style.display,saved:!!localStorage.getItem(SAVE_KEY)})})()"""))
      cls={'combat':'interceptor','mining':'skiff','hauling':'courier'}[role]
      check('%s: the entry starts a real galaxy as Launch does (the role\'s starter, 1,800 cr, saved), with the guide on the pilot'%role,r['guide'] and r['role']==role and r['cls']==cls and r['cr']==1800 and not r['training'] and r['home']==r['port'] and r['saved'],r)
      check('%s: the Overview shows the guide\'s step first (step 1 of 5, pays 150 cr) in place of the Next step card'%role,'STEP 1 OF 5' in r['card'].upper() and '150' in r['card'] and 'Skip step' in r['card'] and not r['nstep'] and r['nsGd'],r)
      check('%s: Your path is on the Overview with the pilot on the first rung'%role,r['rung']==0,r)
      check('%s: day one hides the intel picker, the Black market tabs and the Company key'%role,not r['intel'] and not r['bm'] and r['bmTab']!='bmjobs' and r['co']=='none',r)
    # ---------------------------------------------------------------- the three roles
    async def combat():
      role='combat';pg,ev,first=await start(role);await ev(INJ)
      check('the Training menu\'s first entry is "Guided start: your first contract"',first.get('first')=='guided' and 'GUIDED START: YOUR FIRST CONTRACT' in first.get('txt','').upper(),first)
      await hidden0(ev,role)
      if not await shake(ev,role):return
      await paid(ev,role,0,150,'Shakedown')
      for i,name,want in((1,'First work',400),(2,'First jump',700)):
        if not await until(ev,"!!S.player.docked","_dock()",200):return await fail_at(ev,role,i+1,'docked at home')
        if not await until(ev,"S.player.guide.sv.mid!=null",None,20):return await fail_at(ev,role,i+1,'a guard job posted (a miner in port)')
        r=json.loads(await ev("""(()=>{const P=S.player,G=P.guide,I=indById(G.sv.mid),H=I.hire;dockTab='home';renderDock();const sb=document.querySelector('#dock .gdcard [data-act=gdjob]');if(sb)sb.click();const j=JOBS_LAST.find(x=>x.id==='igd:'+I.id),shown=dockTab==='jobs'&&jobSel==='igd:'+I.id,tb=document.querySelector('#dock [data-act=igtake][data-arg="'+I.id+'"]');if(tb)tb.click();else dockClick('igtake',String(I.id));
          return JSON.stringify({row:!!j,shown,take:!!tb,by:j&&jbIssuer(j),pay:j&&j.pay,to:H.to,home:G.home,capT:H.capT,cap:H.cap,st:I.st,made:!!G.made,took:dockErr,guard:!!I.guard,name:I.name})})()"""))
        check('%s step %d: a real guard job is on the board, issued by the Freeport Compact for %d cr, and is taken'%(role,i+1,want),r['row'] and r['shown'] and r['take'] and r['by']=='Freeport Compact' and str(want) in r['pay'].replace(',','') and r['guard'] and (r['to']==r['home'])==(i==1),r)
        if not await until(ev,stepi+">%d"%i,"_guard()",900,40):return await fail_at(ev,role,i+1,'the miner docked again with its guard near (igEnd)')
        again=await ev("(()=>{const n=window._takes||0;window._takes=0;return n})()")
        if again:print('combat step %d: the trip went wrong %d time(s) (raiders, or the miner lost) and the job was taken again'%(i+1,again))
        await paid(ev,role,i,want,name)
      x=await part_choice(ev,role)
      if not x:return
      await finish(ev,role,x[0],x[1])
      # the Black market tab comes with Rating 2 (the game's own Rating points)
      r=json.loads(await ev("(()=>{const P=S.player;rpAdd(P,RATING.need[2]-(P.rp||0),'test');GD_C.t=-1e9;_ff(10);dockTab='jobs';renderDock();return JSON.stringify({rating:ratingOf(P),bm:dockG.some(g=>g[2].some(t=>t[0]==='bmjobs')),note:FEED.some(f=>/New at the dock: the Black market/.test(f.msg))})})()"))
      check('combat: the Black market tab appears at Contractor Rating 2, with a note',r['rating']==2 and r['bm'] and r['note'],r)
      await pg.close()
    async def mining():
      role='mining';pg,ev,first=await start(role);await ev(INJ);await hidden0(ev,role)
      if not await shake(ev,role):return
      await paid(ev,role,0,150,'Shakedown')
      # step 2: mine 5 t here and sell it at the freeport
      if not await until(ev,"(S.player.guide.sv.got||0)>=GD.ore[1]","_mine()",260,12):return await fail_at(ev,role,2,'5 t of ore mined into the hold')
      await ev("keys.KeyF=false");
      if not await until(ev,"!!S.player.docked","_dock()",200):return await fail_at(ev,role,2,'docked at home with the ore')
      r=json.loads(await ev("(()=>{const P=S.player,o0=gdOre(P),c0=P.credits;dockTab='home';renderDock();const b=document.querySelector('#dock .gdcard [data-act=sellhold]');dockClick('sellhold','');return JSON.stringify({btn:!!b,sold:o0-gdOre(P),cr:P.credits-c0,err:dockErr})})()"))
      check('mining step 2: ore from a real rock sold at the freeport',r['sold']>=5 and r['cr']>0 and r['btn'],r)
      if not await until(ev,stepi+">1",None,20):return await fail_at(ev,role,2,'the ore sold at home (dock action sell)')
      await paid(ev,role,1,400,'First work')
      # step 3: the next system, 8 t, and home again
      to=await ev("(()=>{_ff(10);const G=S.player.guide;S.player.route=G.sv.to;window._rk=null;return G.sv.to})()")
      check('mining step 3: the guide names a system next door with rock',bool(to) and await ev("NEIGH[S.player.guide.home].includes(%s)&&indOreIn(%s)>=60"%(json.dumps(to),json.dumps(to))),to)
      if not await until(ev,"S.player.sector===%s&&!W.jump"%json.dumps(to),"_gate()",200,20):return await fail_at(ev,role,3,'the jump to the next system')
      if not await until(ev,"(S.player.guide.sv.got||0)>=GD.ore[2]","_mine()",300,12):return await fail_at(ev,role,3,'8 t mined outside the home system')
      await ev("(()=>{keys.KeyF=false;S.player.route=S.player.guide.home;return 1})()")
      if not await until(ev,"S.player.sector===S.player.guide.home&&!W.jump","_gate()",200,20):return await fail_at(ev,role,3,'the jump home')
      if not await until(ev,"!!S.player.docked","_dock()",200):return await fail_at(ev,role,3,'docked at home')
      await ev("(()=>{dockClick('sellhold','');return 1})()")
      if not await until(ev,stepi+">2",None,20):return await fail_at(ev,role,3,'the ore sold at home')
      await paid(ev,role,2,700,'First jump')
      x=await part_choice(ev,role,scout=True)
      if not x:return
      r5=x[0]
      r=json.loads(await ev("(()=>{dockTab='jobs';renderDock();return JSON.stringify({intel:!!document.querySelector('#dock [data-act=intelfor]'),note:FEED.some(f=>/Intel work for/.test(f.msg))})})()"))
      check('mining: the intel-work picker was hidden, and appears once a scouting job is taken, with a note',r5.get('hid') and r5.get('ty')=='scout' and r['intel'] and r['note'],[r5,r])
      await finish(ev,role,x[0],x[1])
      # Build here comes with a kit (staged into the hangar, the ledger's baseline moved with it)
      r=json.loads(await ev("""(()=>{const P=S.player;undock();_ff(30);hudUpdate();const k0=[...$('cKeys').children].some(d=>/Build here/.test(d.textContent));devLedger(()=>inv.add(P.vault,'kit_lair',1));GD_C.t=-1e9;_ff(30);hudUpdate();
        return JSON.stringify({before:k0,after:[...$('cKeys').children].some(d=>/Build here/.test(d.textContent)),note:FEED.some(f=>/New in the quick keys/.test(f.msg))})})()"""))
      check('mining: Build here is out of the quick keys until the pilot owns a kit, then shown with a note',not r['before'] and r['after'] and r['note'],r)
      await pg.close()
    async def hauling():
      role='hauling';pg,ev,first=await start(role);await ev(INJ);await hidden0(ev,role)
      if not await shake(ev,role):return
      await paid(ev,role,0,150,'Shakedown')
      for i,name,want in((1,'First work',400),(2,'First jump',700)):
        if not await until(ev,"!!S.player.docked","_dock()",200):return await fail_at(ev,role,i+1,'docked')
        if not await until(ev,"S.player.guide.sv.kid!=null",None,20):return await fail_at(ev,role,i+1,'a Freeport request the pilot can fill from this dock')
        r=json.loads(await ev("""(()=>{const P=S.player,G=P.guide,k=gdContract(G);dockTab='jobs';jobFilter='all';renderDock();const j=JOBS_LAST.find(x=>x.id==='r:'+k.id),c0=P.credits;jobSel=j&&j.id;renderDock();dockClick('hbuy',String(k.id));_ff(10);
          return JSON.stringify({row:!!j,by:j&&jbIssuer(j),item:k.item,n:k.n,reward:k.reward,from:G.sv.from,to:G.sv.to,home:G.home,hops:HOP[P.sector][k.st],spent:c0-P.credits,have:P.cargo[k.item]||0,bought:G.sv.item,route:P.route,err:dockErr})})()"""))
        check('%s step %d: a real Freeport request (%s %s to %s, %s jumps) is on the board, and its goods are bought to the hold'%(role,i+1,r.get('n'),r.get('item'),r.get('to'),r.get('hops')),r['row'] and r['by']=='Freeport Compact' and r['have']>0 and r['spent']>0 and r['bought']==r['item'] and r['route']==r['to'] and (r['to']==r['home'])==(i==2) and (r['from']==r['home'])==(i==1),r)
        if not await until(ev,"S.player.sector===S.player.guide.sv.to&&!W.jump","_gate()",500,20):return await fail_at(ev,role,i+1,'the flight to the destination freeport')
        if not await until(ev,"!!S.player.docked","_dock()",200):return await fail_at(ev,role,i+1,'docked at the destination')
        r=json.loads(await ev("(()=>{const P=S.player,G=P.guide,k=gdContract(G),c0=P.credits;dockTab='jobs';renderDock();dockClick('deliver',String(k.id));return JSON.stringify({got:P.credits-c0,reward:k.reward,err:dockErr})})()"))
        if not await until(ev,stepi+">%d"%i,None,20):return await fail_at(ev,role,i+1,'the request delivered (dock action deliver)')
        check('%s step %d: delivered; the request itself paid %s cr'%(role,i+1,r.get('got')),r['got']>0,r)
        await paid(ev,role,i,want,name)
      x=await part_choice(ev,role)
      if not x:return
      await finish(ev,role,x[0],x[1])
      # the Black market tab also comes with stolen goods aboard (one plate staged and tagged, the ledger's baseline moved)
      r=json.loads(await ev("(()=>{const P=S.player;const b0=dockG.some(g=>g[2].some(t=>t[0]==='bmjobs'));devLedger(()=>inv.add(P.cargo,'plate',1));stolAdd(P,'plate','halcyon',1);GD_C.t=-1e9;_ff(10);dockTab='jobs';renderDock();return JSON.stringify({before:b0,rating:ratingOf(P),bm:dockG.some(g=>g[2].some(t=>t[0]==='bmjobs'))})})()"))
      check('hauling: the Black market tab appears when the pilot holds stolen goods',(not r['before'] or r['rating']>=2) and r['bm'],r)
      await pg.close()
    # ---------------------------------------------------------------- skipping, saving and loading, ending; and Launch
    async def extras():
      role='combat';pg,ev,first=await start(role);await ev(INJ)
      r=json.loads(await ev("(()=>{const P=S.player,c0=P.credits,t0=S.econ.treasury.neutral;undock();_ff(30);hudUpdate();const b=document.querySelector('#train [data-gd=skip]');if(b)b.click();_ff(10);return JSON.stringify({btn:!!b,i:P.guide.i,paid:P.guide.paid,skip:P.guide.skip,dc:P.credits-c0,pays:_pay.length})})()"))
      check('a skipped step pays nothing and the guide moves on',r['btn'] and r['i']==1 and r['paid']==[0] and r['skip']==[1] and r['dc']==0 and r['pays']==0,r)
      if not await until(ev,"!!S.player.docked","_dock()",200):return await fail_at(ev,'extras',2,'docked at home')
      await until(ev,"S.player.guide.sv.mid!=null",None,20)
      g0=json.loads(await ev("(()=>{save();const I=indById(S.player.guide.sv.mid);return JSON.stringify({g:S.player.guide,hire:!!(I&&I.hire&&I.hire.gd),T:S.T})})()"))
      await pg.reload(wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
      await pg.evaluate("document.getElementById('bContinue').click()");await pg.wait_for_function('__dg.ev("!!(S&&S.player&&running)")',timeout=60000);await pg.wait_for_timeout(500)
      g1=json.loads(await ev("(()=>{const I=indById(S.player.guide.sv.mid);return JSON.stringify({g:S.player.guide,hire:!!(I&&I.hire&&I.hire.gd),card:!!document.querySelector('#dock .gdcard'),co:$('bCompany').style.display})})()"))
      check('a save and load keeps the guide\'s state (step, role, pay, the posted job) and the guide carries on',g0['g']==g1['g'] and g0['hire'] and g1['hire'] and g1['g']['i']==1 and g1['card'],[g0,g1])
      await ev(INJ)
      r=json.loads(await ev("""(()=>{const P=S.player,mid=P.guide.sv.mid;openDock('home');dockTab='home';renderDock();dockClick('gd','pathhide');const hid=!document.querySelector('#dock .gdpath table')&&/show your path/i.test($('dock').innerText);dockClick('gd','pathshow');const shown=!!document.querySelector('#dock .gdpath table');
        dockClick('gd','end');const still=P.guide.on;dockClick('gd','end');hudUpdate();dockTab='jobs';renderDock();const I=indById(mid);
        const o={hid,shown,still,on:P.guide.on,hire:!!(I&&I.hire),co:$('bCompany').style.display,intel:!!document.querySelector('#dock [data-act=intelfor]'),bm:dockG.some(g=>g[2].some(t=>t[0]==='bmjobs'))};dockTab='home';renderDock();o.card=!!document.querySelector('#dock .gdcard');o.path=!!document.querySelector('#dock .gdpath');o.nstep=!!document.querySelector('#dock .nstep')||!/Nothing waiting here/.test($('dock').innerText);return JSON.stringify(o)})()"""))
      check('Your path can be hidden and shown again',r['hid'] and r['shown'],r)
      check('End guide asks twice, then every control is back, the miner is let go and the Overview is the usual one',r['still']==1 and r['on']==0 and not r['hire'] and r['co']=='' and r['intel'] and r['bm'] and not r['card'] and not r['path'] and r['nstep'],r)
      l=await ev(LED);check('extras: ledger exact',l=='exact',l);await pg.close()
      pg,ev,first=await start('combat',guided=False)
      r=json.loads(await ev("""(()=>{const P=S.player;openDock('home');dockTab='jobs';renderDock();hudUpdate();const o={guide:P.guide===undefined,co:$('bCompany').style.display,intel:!!document.querySelector('#dock [data-act=intelfor]'),bm:dockG.some(g=>g[2].some(t=>t[0]==='bmjobs'))};dockTab='home';renderDock();o.card=!!document.querySelector('#dock .gdcard');o.path=!!document.querySelector('#dock .gdpath');
        undock();_ff(30);hudUpdate();o.build=[...$('cKeys').children].some(d=>/Build here/.test(d.textContent));o.train=$('train').hidden;return JSON.stringify(o)})()""".replace('_ff(30)','for(let i=0;i<30;i++)step(.05)')))
      check('a pilot who used Launch has no guide and loses nothing',r['guide'] and r['co']=='' and r['intel'] and r['bm'] and not r['card'] and not r['path'] and r['build'] and r['train'],r)
      await pg.close()
    jobs={'combat':combat,'mining':mining,'hauling':hauling}
    await asyncio.gather(*[jobs[r]() for r in ROLES],*( [extras()] if os.environ.get('EXTRAS','1')=='1' else []))
    check('no errors',not errs,errs[:4])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
