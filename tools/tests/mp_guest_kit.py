# usage: python3 tools/tests/mp_guest_kit.py $PWD/index.html  (needs Playwright with Chromium)
# A guest over the faked link (4 Nov 2026, the user's ask): the Loadout (fit a part, a part's grade, a system's grade,
# Rearm), the helm of each capital (an escort, a carrier and a frigate: board, take the helm, set throttle and a move
# point, the frigate jumps with the guest aboard, step off), and a Claim Beacon (the Jobs board's Buy & fit, then holding
# it in an unclaimed outpost's ring claims the outpost). Every step is checked on the host; the ledger stays exact.
import asyncio,json,sys
from playwright.async_api import async_playwright
FILE=sys.argv[1]
LINK=r"""(to)=>{window.__mk=(peer,fn)=>({peer,open:true,dead:false,parts:{},n:'',r:{readyState:'open',send:s=>fn(s)},u:{readyState:'open',send:s=>fn(s)},pc:{close(){},connectionState:'connected'}});return 1}"""
FAILS=[]
def check(name,ok,info=''):
  print(('ok   ' if ok else 'FAIL ')+name+(' · '+str(info) if info!='' else ''))
  if not ok:FAILS.append(name)
async def boot(ctx,name,errs):
  pg=await ctx.new_page();pg.on('pageerror',lambda e:errs.append(name+': '+str(e.stack)[:500]))
  pg.on('console',lambda m:errs.append(name+' console: '+m.text[:400]) if m.type=='error' and 'TUNNEL' not in m.text and 'fonts' not in m.text and 'favicon' not in m.text else None)
  await pg.goto('file://'+FILE+'?name='+name,timeout=400000);await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=400000)
  await pg.evaluate("c=>__dg.ev(c)",f"(()=>{{$('mpName').value='{name}';legGrant('{name}','halcyon',true,'interceptor',null);return 1}})()")
  return pg
async def ev(pg,code):
  return await pg.evaluate("c=>__dg.ev(c)",code)
async def main():
  errs=[]
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows'])
    H=await boot(await b.new_context(viewport={'width':1200,'height':800}),'Hosty',errs);C=await boot(await b.new_context(viewport={'width':1200,'height':800}),'Clie',errs)
    async def toC(s):
      try:await C.evaluate("d=>{if(window.MPHOST_READY)__dg.ev('linkRecv(MP.host,'+JSON.stringify(d)+')')}",s)
      except Exception as e:errs.append('relay->C '+str(e)[:200])
    async def toH(s):
      try:await H.evaluate("d=>__dg.ev('linkRecv(window.__HL,'+JSON.stringify(d)+')')",s)
      except Exception as e:errs.append('relay->H '+str(e)[:200])
    await H.expose_function('__toClient',toC);await C.expose_function('__toHost',toH)
    await H.evaluate(LINK);await C.evaluate(LINK)
    await ev(H,"(()=>{MP.pid='hostpid1';MP.name='Hosty';MP.code='crew';MP.cl={};MP.rp={};MP.inp={};MP.roster=[];hostBegin(false);selFac='halcyon';mpLaunch('halcyon','interceptor','mw');window.__HL=__mk('cli',s=>__toClient(s));return 1})()")
    await H.wait_for_timeout(1500)
    await ev(C,"(()=>{NET.on=true;NET.cl=true;NET.host=false;MP.pid='clipid1';NET.me=MP.pid;MP.name='Clie';MP.code='crew';MP.roster=[];MP.host=__mk('host',s=>__toHost(s));window.MPHOST_READY=1;linkUp(MP.host);return 1})()")
    await C.wait_for_timeout(2500)
    await ev(C,"(()=>{selFac='varkesh';mpLaunch('varkesh','interceptor','ew');return 1})()");await C.wait_for_timeout(4000)
    G=lambda c:ev(C,c)
    Hh=lambda c:ev(H,c)
    LED="(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(1));return b.length?'DRIFT '+b:'exact'})()"
    HP="S.pilots.clipid1"
    print('guest joined:',await G("(()=>JSON.stringify({fac:S.player.faction,cls:S.player.cls,sector:S.player.sector,docked:S.player.docked}))()"))
    async def act(a,arg,wait=2000):
      await G("(()=>{dockErr='';netSend({t:'act',act:%s,arg:%s});return 1})()"%(json.dumps(a),json.dumps(arg)));await C.wait_for_timeout(wait)
      return await G("dockErr")
    # ================= the Loadout
    # the host gives the guest materials (10 of everything in the vault) and a spare laser in the hold
    print('materials:',await Hh("(()=>{const P=%s;runAs('clipid1',()=>devRes(P));devLedger(()=>inv.add(P.cargo,'pt_laser',1));P.credits+=0;const c=runAs('clipid1',()=>dockCtx());return 'store is vault: '+(c.storage===P.vault||!c.storage)})()"%HP))
    await C.wait_for_timeout(1500)
    w0=json.loads(await Hh("JSON.stringify(fitOf(%s).w)"%HP))
    slot=next((i for i,k in enumerate(w0) if k!='laser'),len(w0)-1)
    m=await act('fit','w:%d:pt_laser'%slot)
    w1=json.loads(await Hh("JSON.stringify(fitOf(%s).w)"%HP))
    check('fit a laser (host)',w1[slot]=='laser','%s -> %s · %s'%(w0,w1,m[:90]))
    check('fit seen on the guest',json.loads(await G("JSON.stringify(fitOf(S.player).w)"))==w1)
    g0=await Hh("(fitOf(%s).g||[])[0]||1"%HP)
    m=await act('pup','w:0')
    check('a grade above your Rating says so',g0==await Hh("(fitOf(%s).g||[])[0]||1"%HP) and 'Rating' in m,m[:100])
    # Contractor Rating 3 opens grade 2 parts and systems
    await Hh("(()=>{%s.rp=400;return 1})()"%HP)
    m=await act('pup','w:0')
    g1=await Hh("(fitOf(%s).g||[])[0]||1"%HP)
    check('part upgrade (weapon slot 1)',g1==g0+1,'grade %s -> %s · %s'%(g0,g1,m[:90]))
    sl=await Hh("Object.keys(%s.tiers).find(k=>%s.tiers[k]<2)||Object.keys(%s.tiers)[0]"%(HP,HP,HP))
    t0=await Hh("%s.tiers[%s]"%(HP,json.dumps(sl)))
    m=await act('upg',sl)
    t1=await Hh("%s.tiers[%s]"%(HP,json.dumps(sl)))
    check('system upgrade (%s)'%sl,t1==t0+1,'grade %s -> %s · %s'%(t0,t1,m[:90]))
    await Hh("(()=>{const P=%s;P.ammo=0;P.rack=0;return 1})()"%HP)
    m=await act('rearm','')
    r=json.loads(await Hh("(()=>{const P=%s,q=rearmQuote(P);return JSON.stringify({ammo:P.ammo,rack:P.rack,left:q.n})})()"%HP))
    check('rearm',r['left']==0 and (r['ammo']>0 or r['rack']>0),'%s · %s'%(r,m[:100]))
    lo=await G("(()=>{dockTab='upg';ldSel='parts';renderDock();return JSON.stringify({plus:document.querySelectorAll('.ldplus').length,len:$('dBody').innerText.length})})()")
    check('the Loadout renders on the guest',json.loads(lo)['len']>200,lo)
    print('ledger after the Loadout:',await Hh(LED))
    # ================= the Claim Beacon: the Jobs board's Buy & fit
    tg=json.loads(await Hh("""(()=>{const P=%s,c=runAs('clipid1',()=>dockCtx()),L=runAs('clipid1',()=>fbSold(c,P));let best=null;
      for(const f of L)for(const x of claimTargets(f,P))if(!x.o.owner&&(!best||x.h<best.h))best={f,o:x.o.id,sec:x.o.sector,h:x.h,name:x.o.name};return JSON.stringify(best)})()"""%HP))
    print('claim target:',tg)
    if tg:
      f=tg['f']
      await G("(()=>{dockTab='jobs';renderDock();return 1})()");await C.wait_for_timeout(500)
      btn=await G("(()=>{const b=[...document.querySelectorAll('#dBody [data-act=cbfit]')];return JSON.stringify(b.map(x=>x.dataset.arg+' '+x.textContent.trim()))})()")
      print('cbfit buttons on the guest\'s board:',btn)
      arg=next((x.split(' ')[0] for x in json.loads(btn) if x.startswith(f+':')),None)
      if not arg:arg='%s:%d'%(f,await Hh("runAs('clipid1',()=>cbSlot(%s))"%HP))
      c0=await G("S.player.credits")
      m=await act('cbfit',arg)
      fit=json.loads(await Hh("JSON.stringify(cbFitted(%s))"%HP))
      check('Buy & fit a beacon',any(x['f']==f for x in fit),'%s · paid %s · %s'%(fit,c0-(await G("S.player.credits")),m[:110]))
      print('ledger after the beacon:',await Hh(LED))
    # ================= capital helms
    await G("(()=>{dockTab='home';undock();return 1})()");await C.wait_for_timeout(3000)
    await G("(()=>{const p=W.player,E=W.stationEnt;p.x=E.x+5000;p.y=E.y+400;p.z=E.z+800;p.vx=p.vy=p.vz=0;return 1})()");await C.wait_for_timeout(1500)
    for K in ['escort','carrier','frigate']:
      mk=json.loads(await Hh("""(()=>{const P=%s,g=MP.rp.clipid1,w=worldOf(g),mk={escort:makeEscort,carrier:makeCarrier,frigate:makeDestroyer}[%s];const t=devLedger(()=>mk(P.faction,w.sid,{},'clipid1'));let e=null;
        inW(w,()=>{e=W.ents.find(x=>x.alive&&x.tok===t)});if(e){e.x=g.x+e.st.radius+500;e.y=g.y;e.z=g.z;e.vx=e.vy=e.vz=0}window._T=t;return JSON.stringify({id:t.id,cls:t.cls,name:t.name,ent:!!e,r:e&&Math.round(e.st.radius)})})()"""%(HP,json.dumps(K))))
      print(K+':',mk)
      await C.wait_for_timeout(2500)
      tid=mk['id']
      seen=await G("""(()=>{const F=W.ents.find(e=>e.role==='frigate'&&e.alive&&e.tok&&e.tok.id===%d);if(!F)return 'not seen: '+W.ents.filter(e=>e.role==='frigate').map(e=>(e.tok&&e.tok.id)+':'+e.tokId).join(',');window._F=F;
        window._pin=setInterval(()=>{const p=W.player;if(S.player.docked)return;p.x=F.x-F.st.radius-150;p.y=F.y;p.z=F.z;p.vx=F.vx;p.vy=F.vy;p.vz=F.vz},40);return 'seen '+F.tok.name+' owner '+F.tok.owner})()"""%tid)
      print('  guest sees:',seen)
      await C.wait_for_timeout(1500)
      await G("(()=>{clearInterval(_pin);enterBridge(_F);return 1})()");await C.wait_for_timeout(2500)
      st=json.loads(await Hh("(()=>{const P=%s;return JSON.stringify({docked:P.docked,bid:P.bridgeId,ship:!!MP.rp.clipid1})})()"%HP))
      check(K+': boarded (host)',st['docked']=='bridge' and st['bid']==tid,st)
      check(K+': on the bridge (guest)',await G("!!(W.bridge&&S.player.docked==='bridge')"))
      await G("(()=>{const t=_F.tok;fconSend(t,'helm:manual');fconSend(t,'thrset:0.4');fconSend(t,'helm:auto');fconSend(t,'move:600:-300:50');fconSend(t,'pw:pd:-1');fconSend(t,'pw:eng:1');return 1})()");await C.wait_for_timeout(1500)
      ctl=json.loads(await Hh("(()=>{const C=fctl(_T);return JSON.stringify({thr:C.throttle,move:C.movePt,eng:C.power.eng,helm:C.helm})})()"))
      check(K+': helm orders applied (host)',abs(ctl['thr']-0.4)<1e-6 and ctl['move'] and ctl['move']['x']==600 and ctl['eng']==4,ctl)
      if K=='frigate':
        to=await Hh("(()=>{const nb=NEIGH[_T.sector].filter(s=>!(S.gateDown||{})[s]);return nb[0]})()")
        s0=await Hh("_T.sector")
        await G("(()=>{fconSend(_F.tok,'jump:%s');return 1})()"%to)
        ok=False
        # (the two pages share one machine and the simulation runs slow: once the drive is spinning, hurry it along)
        for i in range(60):
          await C.wait_for_timeout(1000)
          if await Hh("_T.sector")==to:ok=True;break
          if i==8:print('  spinning:',await Hh("(()=>{const s=_T.spin;if(s&&s.p>.1)s.p=.97;return JSON.stringify(s)})()"))
        check('frigate jumps %s -> %s (host)'%(s0,to),ok,await Hh("JSON.stringify({sector:_T.sector,jumpTo:_T.jumpTo,spin:_T.spin})"))
        await C.wait_for_timeout(5000)
        gs=json.loads(await G("(()=>JSON.stringify({sector:S.player.sector,sid:W.sid,bridge:!!W.bridge,docked:S.player.docked,fade:$('fade').style.opacity}))()"))
        check('guest rides the jump',gs['sector']==to and gs['sid']==to and gs['bridge'],gs)
        check('host has the guest in '+to,await Hh("%s.sector"%HP)==to)
        await G("(()=>{window._F=W.bridge&&W.bridge.f;return 1})()")
      await G("(()=>{exitBridge();return 1})()");await C.wait_for_timeout(3000)
      st=json.loads(await Hh("(()=>{const P=%s,e=MP.rp.clipid1;return JSON.stringify({docked:P.docked,ship:!!e,sec:e&&worldOf(e)&&worldOf(e).sid})})()"%HP))
      check(K+': stepped off, flying again (host)',not st['docked'] and st['ship'],st)
      await G("(()=>{const p=W.player;p.x+=1500;p.vx=p.vy=p.vz=0;return 1})()");await C.wait_for_timeout(800)
    print('ledger after the helms:',await Hh(LED))
    # ================= the claim: fly to the outpost and hold in its ring
    if tg:
      for hop in range(6):
        here=await G("S.player.sector")
        if here==tg['sec']:break
        nxt=await G("(()=>{const nb=NEIGH[S.player.sector].slice().sort((a,b)=>HOP[a][%s]-HOP[b][%s]);return nb[0]})()"%(json.dumps(tg['sec']),json.dumps(tg['sec'])))
        await G("(()=>{doJump(%s);return 1})()"%json.dumps(nxt));await C.wait_for_timeout(5000)
      here=await G("S.player.sector");print('at',here,'for',tg['name'])
      c1=await G("S.player.credits")
      await G("(()=>{const O=W.outpostEnt;window._pin=setInterval(()=>{const p=W.player;p.x=O.x+180;p.y=O.y+60;p.z=O.z;p.vx=p.vy=p.vz=0},40);return 1})()")
      ok=False
      for i in range(60):
        await C.wait_for_timeout(1000)
        if await Hh("S.outposts[%s].owner"%json.dumps(tg['o']))==f:ok=True;break
        if i==10:print('  claiming:',await Hh("(()=>{const o=S.outposts[%s];if(o.cap&&o.cap.side===%s&&o.cap.p>.15)o.cap.p=.97;return JSON.stringify(o.cap)})()"%(json.dumps(tg['o']),json.dumps(f))))
      await G("(()=>{clearInterval(_pin);return 1})()");await C.wait_for_timeout(2000)
      o=json.loads(await Hh("(()=>{const o=S.outposts[%s];return JSON.stringify({owner:o.owner,cap:o.cap,fitted:cbFitted(%s)})})()"%(json.dumps(tg['o']),HP)))
      check('outpost claimed for %s'%f,ok and o['fitted']==[],o)
      pay=(await G("S.player.credits"))-c1
      check('claim fee paid to the guest',pay>0,'%s cr · %s'%(pay,await G("FEED.slice(-6).map(x=>x.msg).filter(m=>/claim/i.test(m)).join(' / ').slice(0,200)")))
    led=await Hh(LED)
    check('ledger exact',led=='exact',led)
    E=[e for e in errs if 'favicon' not in e]
    check('no errors',not E,E[:6])
    await b.close()
  print('FAILED: '+', '.join(FAILS) if FAILS else 'ALL OK')
  sys.exit(1 if FAILS else 0)
asyncio.run(main())
