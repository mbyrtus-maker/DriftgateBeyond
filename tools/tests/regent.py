# Beyond, 4 Nov 2026: sleep mode. A declared faction's stand-in (a name, two traits, a reserve) is appointed on the Allegiance
# panel; the Sleep button hands over; asleep, it answers the powers (alliance offer, tribute), defends an attacked Station
# (crews home, a building added by an Industrious stand-in), sends envoys; any key wakes you and it resigns with a report.
# Idle for 15 minutes hands over on its own. For now a closed game waits (no catch-up while nobody plays). Ledger exact.
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
    # ---- a closed game: an hour away, then reopened
    T0=await ev("S.T")
    await ev("(()=>{save();const o=JSON.parse(localStorage.getItem(SAVE_KEY));o.savedAt=Date.now()-3600*1000;localStorage.setItem(SAVE_KEY,JSON.stringify(o));removeEventListener('beforeunload',save);save=function(){};return 1})()")
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await pg.evaluate("document.getElementById('bContinue').click()");await pg.wait_for_timeout(3000)
    r=json.loads(await ev("JSON.stringify({running,T:Math.round(S.T),asleep:!!S.player.asleep,ov:!!document.getElementById('rgOv')&&!document.getElementById('rgOv').hidden,rep:S.player.rgRep&&S.player.rgRep.by})"))
    # (user, 4 Nov 2026) for now the galaxy waits while nobody is playing: an hour closed, and it picks up where you left it
    check('a closed game waits: no catch-up on reopening',r['running'] and abs(r['T']-T0)<60 and not r['asleep'] and not r['ov'] and r['rep']!='closed','%s (S.T %s -> %s)'%(r,T0,r['T']))
    led=await ev(LED);check('ledger exact',led=='exact',led)
    check('no errors',not errs,errs[:4])
    await b.close()
  print('FAILED: '+', '.join(FAILS) if FAILS else 'ALL OK')
asyncio.run(main())
