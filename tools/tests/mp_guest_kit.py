# usage: python3 tools/tests/mp_guest_kit.py $PWD/index.html  (needs Playwright with Chromium)
# A guest's kit over the faked link (4 Nov 2026, the user's ask; rewritten for R&D on 7 Nov 2026, when upgrades in place
# went): the Loadout (a graded maker part bought on the market and fitted, Rating-gated with the message; an upgrade in
# place refused; a system installed through the Loadout's real Install button; Rearm), the helm of each capital (an
# escort, a carrier and a frigate: board, take the helm, set throttle and a move point, the frigate jumps with the guest
# aboard, step off), and a Claim Beacon (the Jobs board's Buy & fit, then holding it in an unclaimed outpost's ring claims
# the outpost). Every step is checked on the host; the ledger stays exact.
import json
from mpkit import run,HP,LED
GP='mp_mg_gun_g2'
SY='sy_ewd_engine_g2'
async def body(K):
  G,Hh,check,act=K.G,K.Hh,K.check,K.act
  if not await G("S.player.docked"):print('dock:',await K.dock())
  check('R&D is on for both',await G("rdOn()") and await Hh("rdOn()"))
  # ================= the Loadout
  # a grade 2 gun on this station's market and credits for it (both through devLedger, so the ledger stays exact)
  pr=await Hh("(()=>{const P=%s,c=runAs('clipid1',()=>dockCtx());devLedger(()=>{inv.add(c.market,%s,1);P.credits+=6000});return Math.ceil(runAs('clipid1',()=>mBuy(c,%s)))})()"%(HP,json.dumps(GP),json.dumps(GP)))
  await K.wait(1500)
  cr0=await Hh("%s.credits"%HP)
  m=await act('buy',GP+':1',2500)
  have=await Hh("countIn(%s,[%s.cargo,%s.vault])"%(json.dumps(GP),HP,HP))
  check('guest buys a grade 2 gun (host)',have==1,'%s on hand · paid %s (price %s) · %s'%(have,cr0-await Hh("%s.credits"%HP),pr,m[:100]))
  await Hh("(()=>{sendPR(Object.values(MP.cl)[0],true,true);return 1})()");await K.wait(1500)
  check('the gun is in the guest\'s hold on its own screen',await G("countIn(%s,[S.player.cargo,S.player.vault])"%json.dumps(GP))==1)
  # a grade above the Rating is refused, with the reason
  F0=json.loads(await Hh("JSON.stringify(fitOf(%s))"%HP))
  m=await act('fit','w:0:'+GP)
  F1=json.loads(await Hh("JSON.stringify(fitOf(%s))"%HP))
  check('a grade above your Rating says so',F1['wi']==F0['wi'] and 'Rating' in m,m[:110])
  # Contractor Rating 3 opens grade 2 parts and systems
  await Hh("(()=>{%s.rp=400;return 1})()"%HP)
  m=await act('fit','w:0:'+GP)
  F=json.loads(await Hh("JSON.stringify(fitOf(%s))"%HP))
  check('graded gun fitted (host)',(F.get('wi') or [None])[0]=='mp_mg_gun' and F['g'][0]==2,'%s g %s · %s'%(F.get('wi'),F['g'],m[:100]))
  await Hh("(()=>{sendPR(Object.values(MP.cl)[0],true,true);return 1})()");await K.wait(1500)
  Fg=json.loads(await G("JSON.stringify(fitOf(S.player))"))
  check('fit seen on the guest',Fg.get('wi')==F.get('wi') and Fg['g']==F['g'],Fg)
  # upgrades in place are gone
  sl=await Hh("Object.keys(%s.tiers).find(k=>%s.tiers[k]<2)||Object.keys(%s.tiers)[0]"%(HP,HP,HP))
  t0=await Hh("%s.tiers[%s]"%(HP,json.dumps(sl)))
  m=await act('upg',sl)
  check('an upgrade in place is refused (%s)'%sl,await Hh("%s.tiers[%s]"%(HP,json.dumps(sl)))==t0 and 'gone' in m,m[:100])
  # a system installed through the Loadout's own Install button (the click goes to the host as {t:'act'})
  await Hh("(()=>{devLedger(()=>inv.add(%s.vault,%s,1));sendPR(Object.values(MP.cl)[0],true,true);return 1})()"%(HP,json.dumps(SY)));await K.wait(2000)
  e0=json.loads(await Hh("JSON.stringify({t:%s.tiers.engine||1,m:(%s.sysm||{}).engine||null,old:%s.vault['sy_engine']||0})"%(HP,HP,HP)))
  clk=await G("(()=>{window.__sent=[];const o=netSend;netSend=function(m){__sent.push(m.t+':'+(m.act||''));return o.apply(this,arguments)};try{dockTab='upg';ldSel='sys:engine';renderDock();const b=document.querySelector('#dBody [data-act=sysfit][data-arg=\"engine:%s\"]');if(!b)return JSON.stringify({err:'no Install button'});b.click()}finally{netSend=o}return JSON.stringify({sent:__sent,err:dockErr,local:(S.player.sysm||{}).engine||null})})()"%SY)
  print('guest Install:',clk)
  cj=json.loads(clk)
  check('the Install click goes to the host',any(x=='act:sysfit' for x in cj.get('sent',[])),clk)
  await K.wait(3000)
  e1=json.loads(await Hh("JSON.stringify({t:%s.tiers.engine||1,m:(%s.sysm||{}).engine||null,old:%s.vault['sy_engine']||0,v:%s.vault[%s]||0})"%(HP,HP,HP,HP,json.dumps(SY))))
  check('system installed (host)',e1['t']==2 and e1['m']=='ewd' and e1['v']==0 and e1['old']==e0['old']+1,'%s -> %s'%(e0,e1))
  gs=json.loads(await G("JSON.stringify({t:S.player.tiers.engine,m:(S.player.sysm||{}).engine||null,err:dockErr})"))
  check('the guest sees it installed',gs['t']==2 and gs['m']=='ewd',gs)
  # Rearm
  await Hh("(()=>{const P=%s;P.ammo=0;P.rack=0;return 1})()"%HP)
  m=await act('rearm','')
  r=json.loads(await Hh("(()=>{const P=%s,q=rearmQuote(P);return JSON.stringify({ammo:P.ammo,rack:P.rack,left:q.n})})()"%HP))
  check('rearm',r['left']==0 and (r['ammo']>0 or r['rack']>0),'%s · %s'%(r,m[:100]))
  lo=await G("(()=>{dockTab='upg';ldSel='parts';renderDock();return JSON.stringify({plus:document.querySelectorAll('.ldplus').length,len:$('dBody').innerText.length})})()")
  lj=json.loads(lo)
  check('the Loadout renders on the guest, with no upgrade buttons',lj['len']>200 and lj['plus']==0,lo)
  await K.ledger('after the Loadout')
  # ================= the Claim Beacon: the Jobs board's Buy & fit
  tg=json.loads(await Hh("""(()=>{const P=%s,c=runAs('clipid1',()=>dockCtx()),L=runAs('clipid1',()=>fbSold(c,P));let best=null;
    for(const f of L)for(const x of claimTargets(f,P))if(!x.o.owner&&(!best||x.h<best.h))best={f,o:x.o.id,sec:x.o.sector,h:x.h,name:x.o.name};return JSON.stringify(best)})()"""%HP))
  print('claim target:',tg)
  if tg:
    f=tg['f']
    await G("(()=>{dockTab='jobs';renderDock();return 1})()");await K.wait(500)
    btn=await G("(()=>{const b=[...document.querySelectorAll('#dBody [data-act=cbfit]')];return JSON.stringify(b.map(x=>x.dataset.arg+' '+x.textContent.trim()))})()")
    print('cbfit buttons on the guest\'s board:',btn)
    arg=next((x.split(' ')[0] for x in json.loads(btn) if x.startswith(f+':')),None)
    if not arg:arg='%s:%d'%(f,await Hh("runAs('clipid1',()=>cbSlot(%s))"%HP))
    c0=await G("S.player.credits")
    m=await act('cbfit',arg)
    fit=json.loads(await Hh("JSON.stringify(cbFitted(%s))"%HP))
    check('Buy & fit a beacon',any(x['f']==f for x in fit),'%s · paid %s · %s'%(fit,c0-(await G("S.player.credits")),m[:110]))
    await K.ledger('after the beacon')
  # ================= capital helms
  await K.undock()
  await G("(()=>{const p=W.player,E=W.stationEnt;p.x=E.x+5000;p.y=E.y+400;p.z=E.z+800;p.vx=p.vy=p.vz=0;return 1})()");await K.wait(1500)
  for kind in ['escort','carrier','frigate']:
    mk=json.loads(await Hh("""(()=>{const P=%s,g=MP.rp.clipid1,w=worldOf(g),mk={escort:makeEscort,carrier:makeCarrier,frigate:makeDestroyer}[%s];const t=devLedger(()=>mk(P.faction,w.sid,{},'clipid1'));let e=null;
      inW(w,()=>{e=W.ents.find(x=>x.alive&&x.tok===t)});if(e){e.x=g.x+e.st.radius+500;e.y=g.y;e.z=g.z;e.vx=e.vy=e.vz=0}window._T=t;return JSON.stringify({id:t.id,cls:t.cls,name:t.name,ent:!!e,r:e&&Math.round(e.st.radius)})})()"""%(HP,json.dumps(kind))))
    print(kind+':',mk)
    await K.wait(2500)
    tid=mk['id']
    seen=await G("""(()=>{const F=W.ents.find(e=>e.role==='frigate'&&e.alive&&e.tok&&e.tok.id===%d);if(!F)return 'not seen: '+W.ents.filter(e=>e.role==='frigate').map(e=>(e.tok&&e.tok.id)+':'+e.tokId).join(',');window._F=F;
      window._pin=setInterval(()=>{const p=W.player;if(S.player.docked)return;p.x=F.x-F.st.radius-150;p.y=F.y;p.z=F.z;p.vx=F.vx;p.vy=F.vy;p.vz=F.vz},40);return 'seen '+F.tok.name+' owner '+F.tok.owner})()"""%tid)
    print('  guest sees:',seen)
    await K.wait(1500)
    await G("(()=>{clearInterval(_pin);enterBridge(_F);return 1})()");await K.wait(2500)
    st=json.loads(await Hh("(()=>{const P=%s;return JSON.stringify({docked:P.docked,bid:P.bridgeId,ship:!!MP.rp.clipid1})})()"%HP))
    check(kind+': boarded (host)',st['docked']=='bridge' and st['bid']==tid,st)
    check(kind+': on the bridge (guest)',await G("!!(W.bridge&&S.player.docked==='bridge')"))
    await G("(()=>{const t=_F.tok;fconSend(t,'helm:manual');fconSend(t,'thrset:0.4');fconSend(t,'helm:auto');fconSend(t,'move:600:-300:50');fconSend(t,'pw:pd:-1');fconSend(t,'pw:eng:1');return 1})()");await K.wait(1500)
    ctl=json.loads(await Hh("(()=>{const C=fctl(_T);return JSON.stringify({thr:C.throttle,move:C.movePt,eng:C.power.eng,helm:C.helm})})()"))
    check(kind+': helm orders applied (host)',abs(ctl['thr']-0.4)<1e-6 and ctl['move'] and ctl['move']['x']==600 and ctl['eng']==4,ctl)
    if kind=='frigate':
      to=await Hh("(()=>{const nb=NEIGH[_T.sector].filter(s=>!(S.gateDown||{})[s]);return nb[0]})()")
      s0=await Hh("_T.sector")
      await G("(()=>{fconSend(_F.tok,'jump:%s');return 1})()"%to)
      ok=False
      # (the two pages share one machine and the simulation runs slow: once the drive is spinning, hurry it along)
      for i in range(60):
        await K.wait(1000)
        if await Hh("_T.sector")==to:ok=True;break
        if i==8:print('  spinning:',await Hh("(()=>{const s=_T.spin;if(s&&s.p>.1)s.p=.97;return JSON.stringify(s)})()"))
      check('frigate jumps %s -> %s (host)'%(s0,to),ok,await Hh("JSON.stringify({sector:_T.sector,jumpTo:_T.jumpTo,spin:_T.spin})"))
      await K.wait(5000)
      gj=json.loads(await G("(()=>JSON.stringify({sector:S.player.sector,sid:W.sid,bridge:!!W.bridge,docked:S.player.docked,fade:$('fade').style.opacity}))()"))
      check('guest rides the jump',gj['sector']==to and gj['sid']==to and gj['bridge'],gj)
      check('host has the guest in '+to,await Hh("%s.sector"%HP)==to)
      await G("(()=>{window._F=W.bridge&&W.bridge.f;return 1})()")
    await G("(()=>{exitBridge();return 1})()");await K.wait(3000)
    st=json.loads(await Hh("(()=>{const P=%s,e=MP.rp.clipid1;return JSON.stringify({docked:P.docked,ship:!!e,sec:e&&worldOf(e)&&worldOf(e).sid})})()"%HP))
    check(kind+': stepped off, flying again (host)',not st['docked'] and st['ship'],st)
    await G("(()=>{const p=W.player;p.x+=1500;p.vx=p.vy=p.vz=0;return 1})()");await K.wait(800)
  await K.ledger('after the helms')
  # ================= the claim: fly to the outpost and hold in its ring
  if tg:
    await K.goto(tg['sec'],6)
    here=await G("S.player.sector");print('at',here,'for',tg['name'])
    c1=await G("S.player.credits")
    await G("(()=>{const O=W.outpostEnt;window._pin=setInterval(()=>{const p=W.player;p.x=O.x+180;p.y=O.y+60;p.z=O.z;p.vx=p.vy=p.vz=0},40);return 1})()")
    ok=False
    for i in range(60):
      await K.wait(1000)
      if await Hh("S.outposts[%s].owner"%json.dumps(tg['o']))==f:ok=True;break
      if i==10:print('  claiming:',await Hh("(()=>{const o=S.outposts[%s];if(o.cap&&o.cap.side===%s&&o.cap.p>.15)o.cap.p=.97;return JSON.stringify(o.cap)})()"%(json.dumps(tg['o']),json.dumps(f))))
    await G("(()=>{clearInterval(_pin);return 1})()");await K.wait(2000)
    o=json.loads(await Hh("(()=>{const o=S.outposts[%s];return JSON.stringify({owner:o.owner,cap:o.cap,fitted:cbFitted(%s)})})()"%(json.dumps(tg['o']),HP)))
    check('outpost claimed for %s'%f,ok and o['fitted']==[],o)
    pay=(await G("S.player.credits"))-c1
    check('claim fee paid to the guest',pay>0,'%s cr · %s'%(pay,await G("FEED.slice(-6).map(x=>x.msg).filter(m=>/claim/i.test(m)).join(' / ').slice(0,200)")))
run(body)
