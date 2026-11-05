# Beyond, 4 Nov 2026: sleep mode. A declared faction's stand-in (a name, two traits, a reserve) is appointed on the Allegiance
# panel; the Sleep button hands over; asleep, it answers the powers (alliance offer, tribute), defends an attacked Station
# (crews home, a building added by an Industrious stand-in), sends envoys; any key wakes you and it resigns with a report.
# Idle for 15 minutes hands over on its own. A closed game catches up on the hours away under the stand-in. Ledger exact.
import asyncio,json,os
from playwright.async_api import async_playwright
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
FAILS=[]
def check(n,ok,info=''):
  print(('ok   ' if ok else 'FAIL ')+n+(' · '+str(info) if info!='' else ''),flush=True)
  if not ok:FAILS.append(n)
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);ctx=await b.new_context(viewport={'width':1400,'height':860});pg=await ctx.new_page();errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    # a Station of your own, a crew, and a declared faction
    setup=await ev("""(()=>{const P=S.player;undock();P.rp=5000;const br=SECTOR_DEFS.map(d=>d.id).filter(id=>sectorOwner(id)==='brood'||DEF[id].kind==='hive'),far=id=>Math.min(99,...br.map(b=>HOP[id][b]));const sid=SECTOR_DEFS.map(d=>d.id).filter(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id]&&!DEF[id].home).sort((a,b)=>far(b)-far(a))[0];exitSector();P.sector=sid;P.docked=null;enterSector(sid);P.cls='bulker';fitOf(P);refreshPlayerStats();devLedger(()=>{P.cargo={frame:2};P.credits+=30000});depFresh(P);const R=S.stations[sid];
      devLedger(()=>{inv.add(R.stock,'keel',1);inv.add(R.stock,'frame',2);inv.add(R.stock,'seal',1);inv.add(R.stock,'plate',40)});staUp(P,R);crewHire(R,P,'skiff');R.hMax=R.hull=5e6;window._R=R;dockAction('declare');const E=W.stationEnt,p=W.player;p.x=E.x+300;p.y=E.y;p.z=E.z;finishDock(E);return JSON.stringify({sid,decl:P.decl&&P.decl.name,crew:R.crew.map(c=>c.cls+':'+c.job),docked:P.docked})})()""")
    print('setup',setup);SID=json.loads(setup)['sid']
    # ---- appointing on the Allegiance panel
    pan=await ev("""(()=>{dockTab='allegiance';renderDock();const box=document.getElementById('rgBox');if(!box)return 'no box';document.getElementById('rgName').value='Ada Merrow';const a=document.getElementById('rgT1'),b=document.getElementById('rgT2');a.value='Patient';a.dispatchEvent(new Event('change',{bubbles:true}));b.value='Industrious';b.dispatchEvent(new Event('change',{bubbles:true}));
      document.getElementById('rgRes').value='0.25';const tx=document.getElementById('rgTx').textContent;document.querySelector('[data-rg=set]').click();return JSON.stringify({tx,regent:S.player.regent,msg:dockErr})})()""")
    print('appoint',pan)
    G=json.loads(pan) if pan.startswith('{') else {}
    check('appointed from the Allegiance panel',G.get('regent',{}).get('name')=='Ada Merrow' and G['regent']['traits']==['Patient','Industrious'] and abs(G['regent']['reserve']-.25)<1e-9,pan[:200])
    check('the traits explain themselves','Industrious: adds Station buildings' in G.get('tx',''))
    c0=await ev("S.player.credits")
    await ev("(()=>{dockTab='allegiance';renderDock();document.querySelector('[data-rg=sleep]').click();return 1})()");await pg.wait_for_timeout(1800)
    st=json.loads(await ev("JSON.stringify({asleep:!!S.player.asleep,by:S.player.asleep&&S.player.asleep.by,ov:!document.getElementById('rgOv').hidden,t:document.getElementById('rgOvT').textContent,floor:S.player.asleep&&S.player.asleep.floor})"))
    check('the Sleep button hands over (overlay shown)',st['asleep'] and st['by']=='button' and st['ov'] and 'Ada Merrow holds' in st['t'],st)
    # ---- asleep: the powers propose, the Station is attacked, the stores fill for a building
    await ev("""(()=>{const P=S.player,R=_R;P.props=P.props||[];const[f,g]=FAC_IDS;P.props.push({id:S.nextId++,f,k:'demand',amt:2000,until:S.T+300});P.props.push({id:S.nextId++,f:g,k:'ally',until:S.T+300});
      devLedger(()=>inv.addAll(R.stock,STA.bcost));distressCall(R.sid,R.name,'player',FAC_IDS[2]);R.hull-=200;return 1})()""")
    await ev("(()=>{for(let i=0;i<4;i++){S.T+=10;strategicTick();updateEvents()}return 1})()")
    a=json.loads(await ev("""(()=>{const P=S.player,R=_R;return JSON.stringify({props:(P.props||[]).length,allied:P.allied||{},crew:R.crew.map(c=>c.job),log:P.asleep.log.map(x=>x.msg),bld:R.bld||[]})})()"""))
    for l in a['log']:print('   log:',l[:160])
    check('answers the powers (Patient pays tribute within the reserve, accepts an alliance)',a['props']==0 and any('tribute' in l and 'paid' in l for l in a['log']) and any('alliance offer: accepted' in l for l in a['log']),a['allied'])
    check('defends the Station: crews called home',a['crew']==['guard'] and any('under attack' in l for l in a['log']),a['crew'])
    check('Industrious: a building added when the stores allow',len(a['bld'])>=1 and any('built' in l for l in a['log']),a['bld'])
    # calm again: the crew goes back to work; a Patient stand-in sends an envoy
    await ev("(()=>{for(let i=0;i<40;i++){S.T+=10;strategicTick();updateEvents()}return 1})()")
    a=json.loads(await ev("""(()=>{const P=S.player,R=_R;return JSON.stringify({crew:R.crew.map(c=>c.job),log:P.asleep.log.map(x=>x.msg)})})()"""))
    print('  hits',await ev("JSON.stringify({hit:S.player.asleep.hit,hp:S.player.asleep.hp,hull:_R.hull,T:S.T,dist:(S.distress||[]).map(d=>d.sid+':'+Math.round(d.T2))})"))
    check('the attack over, crews back to work',a['crew']==['mine'] and any('holds: the attack is over' in l for l in a['log']),a['crew'])
    check('diplomacy by envoy',any(l.startswith('Envoy to') for l in a['log']),[l for l in a['log'] if 'Envoy' in l][:2])
    check('never below the reserve',await ev("S.player.credits>=S.player.asleep.floor"),await ev("S.player.credits+' / '+S.player.asleep.floor"))
    # ---- any key wakes you: the stand-in resigns and reports
    print('  before key',await ev("JSON.stringify({rgCU,shown:performance.now()-rgShown,asleep:!!S.player.asleep,focus:document.activeElement&&document.activeElement.tagName})"))
    await pg.keyboard.press('KeyW');await pg.wait_for_timeout(1800)
    print('  after key',await ev("JSON.stringify({asleep:!!S.player.asleep,err:(window.__dgErr||[]).slice(-3),de:dockErr})"))
    w=json.loads(await ev("JSON.stringify({asleep:!!S.player.asleep,rep:S.player.rgRep&&{name:S.player.rgRep.name,lines:S.player.rgRep.log.length,cr:S.player.rgRep.cr1-S.player.rgRep.cr0},ov:!document.getElementById('rgOv').hidden,pop:!!document.getElementById('rgRepPop')&&!document.getElementById('rgRepPop').hidden})"))
    check('a key wakes you; the report pops up',not w['asleep'] and w['rep'] and w['rep']['lines']>=4 and not w['ov'] and w['pop'],w)
    await ev("(()=>{document.getElementById('rgRepOk').click();dockTab='allegiance';renderDock();return 1})()")
    check('the report stays on the Allegiance tab',await ev("document.getElementById('dBody').innerText.toLowerCase().includes(\"ada merrow's report\")"))
    print('ledger',await ev(LED))
    # ---- idle for 15 minutes: it takes over on its own
    await ev("(()=>{rgIn=performance.now()-16*60*1000;return 1})()");await pg.wait_for_timeout(2500)
    check('idle 15 minutes: the stand-in takes over',await ev("!!S.player.asleep&&S.player.asleep.by==='idle'"),await ev("JSON.stringify(S.player.asleep&&S.player.asleep.by)"))
    print('  before click',await ev("JSON.stringify({shown:performance.now()-rgShown,asleep:!!S.player.asleep,pop:document.getElementById('rgRepPop').hidden})"))
    await pg.wait_for_timeout(1500);await pg.mouse.click(400,400);await pg.wait_for_timeout(1500)
    check('a click wakes you',await ev("!S.player.asleep"))
    # ---- a closed game: three hours away, caught up under the stand-in
    T0=await ev("S.T")
    await ev("(()=>{save();const o=JSON.parse(localStorage.getItem(SAVE_KEY));o.savedAt=Date.now()-3600*1000;localStorage.setItem(SAVE_KEY,JSON.stringify(o));removeEventListener('beforeunload',save);save=function(){};return 1})()")
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    print('  saved',await ev("(()=>{const o=loadSave();return JSON.stringify({decl:!!o.player.decl,asleep:o.player.asleep,savedAt:Date.now()-o.savedAt,st:Object.values(o.stations).filter(R=>R.owner==='player').map(R=>R.sid+':'+R.kind+':'+R.pid+':'+R.pst+':'+Math.round(R.hull))})})()"))
    await ev("(()=>{window.__rz=[];const o=razeStation;razeStation=function(sid,by){if(sid===%s){__rz.push(['raze',sid,by,Math.round(S.T)]);return}return o.apply(this,arguments)};const c=captureDepot;captureDepot=function(sid,side){if(sid===%s){__rz.push(['cap',sid,side,Math.round(S.T)]);return}return c.apply(this,arguments)};return 1})()"%(json.dumps(SID),json.dumps(SID)))
    await pg.evaluate("document.getElementById('bContinue').click()")
    for i in range(4):
      print('  t',i,await ev("JSON.stringify({decl:!!S.player.decl,sta:myStations(S.player).length,dep:myDepots(S.player).length,T:Math.round(S.T),asleep:S.player.asleep&&S.player.asleep.by,log:S.player.asleep&&S.player.asleep.log.map(x=>x.msg).slice(-3)})"))
      await pg.wait_for_timeout(300)
    await pg.wait_for_timeout(800)
    print('catching up:',await ev("(()=>{const e=document.getElementById('rgOvS');return e?e.textContent:'(no overlay)'})()"))
    for i in range(120):
      st=await ev("JSON.stringify({decl:!!S.player.decl,reg:!!S.player.regent,sta:myStations(S.player).length,T:Math.round(S.T),cu:!!rgCU,stop:rgCU&&rgCU.stop,running,asleep:S.player.asleep&&S.player.asleep.by,won:S.won||null})")
      if i%3==0:print('  ',st)
      if await ev("running&&!rgCU"):break
      await pg.wait_for_timeout(2000)
    r=json.loads(await ev("JSON.stringify({running,T:Math.round(S.T),rep:S.player.rgRep&&{by:S.player.rgRep.by,dur:Math.round(S.player.rgRep.dur),lines:S.player.rgRep.log.length},docked:S.player.docked,sector:S.player.sector,asleep:!!S.player.asleep,pop:!!document.getElementById('rgRepPop')&&!document.getElementById('rgRepPop').hidden})"))
    check('the closed game caught up an hour under the stand-in',r['running'] and r['rep'] and r['rep']['by']=='closed' and abs(r['rep']['dur']-3600)<30 and r['T']-T0>=3590 and not r['asleep'] and r['pop'],'%s (S.T %s -> %s)'%(r,T0,r['T']))
    print('  razes',await ev("JSON.stringify(__rz)"))
    print('  report',await ev("JSON.stringify({won:S.won||null,log:S.player.rgRep.log.map(x=>x.msg),counts:controlCounts()})"))
    print('  station',await ev("JSON.stringify(Object.values(S.stations).filter(R=>R.sid==='gs'||R.owner==='player').map(R=>[R.sid,R.owner,R.kind,R.pid,Math.round(R.hull),R.hMax]))"),await ev("JSON.stringify(S.chron.slice(-30).map(c=>c.msg).filter(m=>/Glass|Tester/.test(m)))"))
    check('docked at your Station after it',r['docked']=='station')
    led=await ev(LED);check('ledger exact',led=='exact',led)
    check('no errors',not errs,errs[:4])
    await b.close()
  print('FAILED: '+', '.join(FAILS) if FAILS else 'ALL OK')
asyncio.run(main())
