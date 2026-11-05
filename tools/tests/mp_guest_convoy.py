# usage: python3 tools/tests/mp_guest_convoy.py $PWD/index.html  (needs Playwright with Chromium)
# A guest flies convoy jobs over the faked link (4 Nov 2026, the user's ask: escorts and raids), each step checked on the host:
#  - a power's convoy raid from a freeport's Jobs board: the guest selects it (its issuer is recorded on the host), shoots the
#    freighter with its own guns, and the issuer pays the raid bounty;
#  - a convoy escort: signed on from the board, the guest jumps with the convoy system by system, and the power pays when
#    it docks;
#  - a Rusty Tankard rumour at Scrapheart: plunder a power's convoy, and the Unbound pay their share.
# The convoys are made by the host (as a power's supply convoy) where the test needs them; the test hurries a convoy that
# has reached its gate (the simulation runs slow with two pages on one machine). The ledger stays exact.
import json,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from mpkit import run,HP
CTX="runAs('clipid1',()=>dockCtx())"
J=json.dumps
async def mkConvoy(K,side,frm,to,load):
  r=json.loads(await K.Hh("""(()=>{const t=devLedger(()=>haulSend(%s,%s,%s,%s,'test:'+S.nextId,'test supplies',null));if(!t)return 'null';t.next=S.T+600;window._CV=window._CV||{};_CV[t.id]=t;
    return JSON.stringify({id:t.id,path:t.path,bounty:raidBounty(t),val:Math.round(invValue(%s)),live:!!t.live})})()"""%(J(side),J(frm),J(to),J(load),J(load))))
  # wait for the guest's copy of the state to have it
  for i in range(40):
    if await K.G("(S.traders||[]).some(x=>x.id===%d)"%r['id']):break
    await K.wait(1000)
  return r
async def board(K,jid):
  return json.loads(await K.G("""(()=>{dockTab='jobs';jobFilter='all';jobSel=%s;renderDock();const j=(JOBS_LAST||[]).find(x=>x.id===%s);const b=j?[...document.querySelectorAll('#dBody [data-act]')].filter(x=>x.dataset.arg==String(j.btn&&j.btn[1])&&x.dataset.act===(j.btn&&j.btn[0])).map(x=>x.textContent.trim()):[];
    return JSON.stringify(j?{title:j.title.replace(/<[^>]+>/g,''),pay:j.pay,by:j.by,btn:j.btn,sub:j.sub.replace(/<[^>]+>/g,''),shown:b}:null)})()"""%(J(jid),J(jid))))
async def shoot(K,tid):
  # the host pins the freighter just ahead of the guest; the guest aims and holds fire with its own guns
  await K.Hh("window._FE=null")
  await K.Hh("""(()=>{const g=MP.rp.clipid1,w=worldOf(g),t=_CV[%d];const e=w.ents.find(x=>x.alive&&x.tradeT===t);if(!e)return 'no freighter';window._FE=e;e.shield=0;e.hull=Math.min(e.hull,e.st.hull*.1);
    window._pin=setInterval(()=>{if(e.alive){e.x=g.x+240;e.y=g.y;e.z=g.z;e.vx=g.vx;e.vy=g.vy;e.vz=g.vz;e.shield=0}},50);return 1})()"""%tid)
  await K.wait(2000)
  r=await K.G("""(()=>{const T=W.ents.find(e=>e.alive&&e.type==='ship'&&e.role==='trader'&&d3(e,W.player)<600);window._aim=0;if(!T)return 'not seen';W.tgt={kind:'ship',ref:T};S.player.wpn='laser';
    window._aim=setInterval(()=>{const p=W.player;if(!T.alive)return;faceInstant(p,T.x-p.x,T.y-p.y,T.z-p.z);p.vx=p.vy=p.vz=0},40);keys.Space=true;return 'aiming at '+Math.round(d3(T,W.player))+' m'})()""")
  print('  guest:',r)
  for i in range(60):
    if await K.Hh("!_FE||!_FE.alive"):break
    await K.wait(500)
  await K.G("(()=>{keys.Space=false;clearInterval(_aim);return 1})()");await K.Hh("(()=>{clearInterval(window._pin);return 1})()")
  await K.wait(2500)
  print('  freighter:',await K.Hh("_FE&&JSON.stringify({alive:_FE.alive,hull:Math.round(_FE.hull),max:Math.round(_FE.st.hull),dmg:_FE.dmg,side:_FE.side})"),'· guest energy',await K.G("Math.round(W.player.energy)+' wpn '+S.player.wpn+' docked '+S.player.docked"))
  return await K.Hh("!!_FE&&!_FE.alive")
async def clear(K):
  # out past the station's guns, so the guest's own guns do the work
  await K.G("(()=>{const p=W.player,E=W.stationEnt;if(E){p.x=E.x+4500;p.y=E.y+300;p.z=E.z}p.vx=p.vy=p.vz=0;return 1})()");await K.wait(1500)
async def body(K):
  G,Hh,check=K.G,K.Hh,K.check
  sec=await G("S.player.sector")
  # (the powers' relations settle in the first seconds of a galaxy: every pair reads as at war until then)
  await K.wait(10000)
  # the guest stands Neutral or better with every power at a freeport; pick a power to work for and one it fights
  pk=json.loads(await Hh("""(()=>{const P=%s,c=%s,I=jobIssuers(c,P);let f=null,g=null;for(const a of I)for(const b of FAC_IDS)if(!f&&b!==a&&hostile(a,b)){f=a;g=b}
    return JSON.stringify({issuers:I,f,g,wars:FAC_IDS.flatMap(a=>FAC_IDS.filter(b=>a<b&&hostile(a,b)).map(b=>a+'-'+b))})})()"""%(HP,CTX)))
  print('sides:',pk)
  if not pk['f']:
    # no war in this galaxy yet: start one between two powers the guest works for (the board raids only an issuer's enemies)
    await Hh("(()=>{const a=%s[0],b=%s[1];evWar(a,b);return 1})()"%(J(pk['issuers']),J(pk['issuers'])))
    pk=json.loads(await Hh("""(()=>{const P=%s,c=%s,I=jobIssuers(c,P);let f=null,g=null;for(const a of I)for(const b of FAC_IDS)if(!f&&b!==a&&hostile(a,b)){f=a;g=b}return JSON.stringify({issuers:I,f,g})})()"""%(HP,CTX)))
    print('sides after a declared war:',pk)
  f,g=pk['f'],pk['g']
  far=await Hh("(()=>{const L=Object.keys(DEF).filter(s=>HOP[%s][s]===2);return L.find(s=>S.stations[s]&&S.stations[s].owner===%s)||L[0]})()"%(J(sec),J(g)))
  # ================= a power's convoy raid
  cv=await mkConvoy(K,g,sec,far,{'plate':30,'coil':6})
  print('raid convoy:',cv)
  j=await board(K,'cv:%d'%cv['id'])
  print('board:',j)
  check('the raid is on the guest\'s board for %s'%f,bool(j) and j['by']==f,j)
  await G("(()=>{jobTrack('cv:%d');return 1})()"%cv['id']);await K.wait(1500)
  jb=json.loads(await Hh("JSON.stringify(%s.job||null)"%HP))
  check('the job is recorded on the host',jb and jb['by']==f and jb['id']=='cv:%d'%cv['id'],jb)
  await K.undock();await clear(K)
  tr0=await Hh("S.econ.treasury[%s]"%J(f));c0=await G("S.player.credits")
  dead=await shoot(K,cv['id'])
  got=(await G("S.player.credits"))-c0
  fd=await G("FEED.slice(-8).map(x=>x.msg).filter(m=>/raid|convoy|freighter/i.test(m)).join(' / ').slice(0,260)")
  check('the guest destroyed the freighter',dead,await Hh("JSON.stringify(_FE.dmg)"))
  want=round((cv['val']*.85+400)/10)*10
  check('the board shows the full raid bounty',j and j['pay']=='%s cr'%format(want,','),'%s (worth %s)'%(j and j['pay'],cv['val']))
  check('%s paid the raid bounty'%f,got>=want,'+%s cr (board said %s, convoy worth %s) · %s'%(got,j and j['pay'],cv['val'],fd))
  await K.ledger('after the raid')
  # ================= a convoy escort
  check('back at the freeport',await K.dock()=='station')
  ce=await mkConvoy(K,f,sec,far,{'plate':30,'coil':6})
  print('escort convoy:',ce)
  j=await board(K,'ce:%d'%ce['id'])
  print('board:',j)
  check('the escort is on the guest\'s board',bool(j) and j['by']==f and j['shown']==['Select job'],j)
  # the board's Select job signs on
  await G("(()=>{const b=document.querySelector('#dBody [data-act=jtrack][data-arg=\"ce:%d\"]');if(b)b.click();return 1})()"%ce['id']);await K.wait(2500)
  E=json.loads(await Hh("JSON.stringify(_CV[%d].esc||null)"%ce['id']))
  check('signed on (host)',E and E['k']=='clipid1','%s · %s'%(E,(await G("dockErr"))[:100]))
  await K.undock()
  c0=await G("S.player.credits");done=False
  for step in range(30):
    st=json.loads(await Hh("""(()=>{const t=_CV[%d];if(!S.traders.includes(t))return JSON.stringify({gone:true,esc:t.esc});const w=WORLDS[t.sector],e=w&&w.ents.find(x=>x.alive&&x.tradeT===t);
      if(e&&!e.ai.arrived&&d3(e,e.ai.dest)>0){e.x=e.ai.dest.x;e.y=e.ai.dest.y;e.z=e.ai.dest.z;e.ai.arrived=true}t.next=Math.min(t.next,S.T);if(e&&e.ai.arrived)tradersTick();return JSON.stringify({sector:t.sector,leg:t.leg,live:!!t.live,esc:t.esc})})()"""%ce['id']))
    if st.get('gone'):done=True;break
    here=await G("S.player.sector")
    print('  ',st,'guest in',here)
    if st['sector']!=here and not await G("S.player.docked"):
      print('  convoy in',st['sector'],'· guest follows from',here,'· escort',st['esc'])
      await G("(()=>{doJump(%s);return 1})()"%J(st['sector']));await K.wait(5000)
    await K.wait(1500)
  await K.wait(2500)
  got=(await G("S.player.credits"))-c0
  fd=await G("FEED.slice(-8).map(x=>x.msg).filter(m=>/escort/i.test(m)).join(' / ').slice(0,220)")
  check('the convoy docked at %s with the guest along'%far,done and await G("S.player.sector")==far,await G("S.player.sector"))
  check('%s paid the escort'%f,got>0 and 'Escort complete' in fd,'+%s cr · %s'%(got,fd))
  await K.ledger('after the escort')
  # ================= a Rusty Tankard rumour: plunder a convoy for the Unbound
  ok=await K.goto('wr')
  check('flew to Scrapheart',ok,await G("S.player.sector"))
  check('docked at Scrapheart',await K.dock()=='station')
  # a convoy one jump out from Scrapheart (the Wrack's own guns would see to one in its system)
  w1=await Hh("NEIGH.wr.find(s=>!S.stations[s]||S.stations[s].owner!=='pirate')||NEIGH.wr[0]")
  w2=await Hh("NEIGH[%s].find(s=>s!=='wr')"%J(w1))
  wc=await mkConvoy(K,g,w1,w2,{'plate':24,'wire':8})
  print('tankard convoy:',wc)
  j=await board(K,'cv:%d'%wc['id'])
  print('board:',j)
  check('the rumour is on the Tavern board',bool(j) and j['by']=='pirate',j)
  await G("(()=>{jobTrack('cv:%d');return 1})()"%wc['id']);await K.wait(1500)
  await K.undock()
  check('flew out to the convoy in %s'%w1,await K.goto(w1))
  await K.wait(2000)
  pt0=await Hh("S.econ.treasury.pirate");c0=await G("S.player.credits")
  dead=await shoot(K,wc['id'])
  got=(await G("S.player.credits"))-c0;pt1=await Hh("S.econ.treasury.pirate")
  fd=await G("FEED.slice(-8).map(x=>x.msg).filter(m=>/Unbound|convoy|raid/i.test(m)).join(' / ').slice(0,260)")
  check('the guest destroyed the Tankard's freighter',dead)
  check('the Unbound paid their share',pt0-pt1>0 and 'Unbound pay' in fd,'+%s cr in all · Unbound paid %s · %s'%(got,pt0-pt1,fd))
if __name__=="__main__":run(body)
