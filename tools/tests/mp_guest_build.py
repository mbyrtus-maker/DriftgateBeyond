# usage: python3 tools/tests/mp_guest_build.py $PWD/index.html  (needs Playwright with Chromium)
# A guest builds its holdings over the faked link (4 Nov 2026, the user's ask: lairs, depots and stations, and eventually its
# own faction), each step checked on the host: a Lair built beside a big asteroid in an empty system (the guest's Build), docked
# at and stocked; the Lair raised to a Depot from its dock; the Depot raised to a Station and given a building (hangar), from
# the Company screen's actions; and with a Station of its own the guest declares its own faction. The ledger stays exact.
import json,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from mpkit import run,HP
J=json.dumps
async def body(K):
  G,Hh,check=K.G,K.Hh,K.check
  sec=await G("S.player.sector")
  # an empty system near the guest: no station or outpost, buildable, with a big asteroid
  sid=await Hh("""(()=>{const L=SECTOR_DEFS.map(d=>d.id).filter(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id]&&!DEF[id].home&&S.sectors[id].ast.some(a=>oreTotal(a)>=LAIR_B.rockMin+20&&!a.rift&&!a.comet));
    return L.sort((a,b)=>HOP[%s][a]-HOP[%s][b])[0]})()"""%(J(sec),J(sec)))
  print('building in',sid,'(%s jumps)'%await Hh("HOP[%s][%s]"%(J(sec),J(sid))))
  # the host gives the guest the materials for each step (as if bought) and a Contractor Rating to match
  await Hh("(()=>{const P=%s;P.rp=5000;devLedger(()=>{inv.add(P.cargo,'frame',3);inv.add(P.cargo,'plate',6)});return 1})()"%HP)
  await K.undock()
  check('flew to %s'%sid,await K.goto(sid),await G("S.player.sector"))
  # ================= a Lair
  await G("""(()=>{const a=S.sectors[S.player.sector].ast.filter(r=>oreTotal(r)>=LAIR_B.rockMin+20&&!r.rift&&!r.comet)[0],p=W.player;p.x=a.x+astR(a)+150;p.y=a.y;p.z=a.z;p.vx=p.vy=p.vz=0;return 1})()""");await K.wait(2000)
  why=await G("JSON.stringify(lairSpot(S.player).why||'ok')")
  m=await G("lairBuildB()");await K.wait(2500)
  L=json.loads(await Hh("(()=>{const L=lairsOf(%s)[0];return JSON.stringify(L?{id:L.id,sid:L.sid,build:Math.round(L.build-S.T),cargo:%s.cargo}:null)})()"%(HP,HP)))
  check('Lair built (host)',L and L['sid']==sid,'spot %s · %s · %s'%(why,m,L))
  if not L:return
  await K.ledger('after the Lair')
  # finish its building time, then dock at it once the guest's copy of the state has it
  await Hh("(()=>{const L=lairsOf(%s)[0];L.build=Math.min(L.build,S.T);return 1})()"%HP)
  for i in range(40):
    if await G("(()=>{const L=(S.lairs||[]).find(x=>x.id===%d);return !!L&&!(L.build>S.T)})()"%L['id']):break
    await K.wait(1000)
  await K.wait(2500)
  await G("(()=>{const L=S.lairs.find(x=>x.id===%d);lairDock(L);return 1})()"%L['id']);await K.wait(2500)
  check('docked at the Lair (host)',await Hh("%s.docked"%HP)=='lair',await Hh("%s.docked"%HP))
  check('the Lair\'s dock screen on the guest',await G("(()=>{renderDock();return document.getElementById('dBody').innerText.length})()")>100)
  # ================= a Depot from the Lair
  await Hh("(()=>{devLedger(()=>inv.add(%s.cargo,'frame',2));return 1})()"%HP);await K.wait(1500)
  m=await K.act('depotup','',3000)
  R=json.loads(await Hh("(()=>{const R=S.stations[%s];return JSON.stringify(R?{owner:R.owner,pid:R.pid,kind:R.kind,pst:!!R.pst}:null)})()"%J(sid)))
  check('Lair raised to a Depot (host)',R and R['owner']=='player' and R['pid']=='clipid1','%s · %s'%(R,m[:120]))
  st=await Hh("%s.docked"%HP)
  gd=await G("S.player.docked")
  check('the guest follows its berth to the Depot',st=='station' and gd=='station','host %s · guest %s'%(st,gd))
  if st!='station':
    await K.undock(2500)
    check('docks at its Depot',await K.dock()=='station')
  check('the Depot\'s screens on the guest',await G("(()=>{const out={};for(const t of ['home','storage','station']){dockTab=t;renderDock();out[t]=document.getElementById('dBody').innerText.length}return Math.min(...Object.values(out))})()")>50)
  await K.ledger('after the Depot')
  # ================= a Station, and a building on it (the Company screen's actions run on the host for the guest)
  await Hh("(()=>{const R=S.stations[%s];devLedger(()=>{inv.addAll(R.stock,{keel:1,frame:3,seal:1,plate:20,coil:4})});return 1})()"%J(sid));await K.wait(1500)
  m=await K.act('staup',sid,2500)
  pst=await Hh("!!S.stations[%s].pst"%J(sid))
  check('Depot raised to a Station (host)',pst,m[:120])
  m=await K.act('stabld',sid+':hangar',2500)
  b=await Hh("JSON.stringify((S.stations[%s].bld||[]))"%J(sid))
  check('a hangar built on it (host)','hangar' in b,'%s · %s'%(b,m[:120]))
  await K.ledger('after the Station')
  # ================= its own faction
  m=await K.act('declare','',3000)
  d=json.loads(await Hh("JSON.stringify({decl:%s.decl||null,owner:sectorOwner(%s)})"%(HP,J(sid))))
  check('the guest declares its own faction (host)',bool(d['decl']),'%s · %s'%(d,m[:140]))
  for i in range(30):
    if await G("!!S.player.decl"):break
    await K.wait(1000)
  check('the guest knows it leads a faction',await G("!!S.player.decl"),await G("JSON.stringify(S.player.decl||null)"))
  t=await G("(()=>{toggleCompany();coTab='allegiance';renderCompany();const t=$('coBody').innerText.slice(0,240).split(String.fromCharCode(10)).join(' | ');toggleCompany();return t})()")
  print('company allegiance tab:',t)
  check('the Company screen shows the faction',len(t)>40)
  # and it can still fly and dock at its own Station
  await K.undock(2500)
  check('docks at its own Station as a faction leader',await K.dock()=='station')
  # ================= sleep mode for the guest's faction (4 Nov 2026)
  m=await K.act('rgset','Juno Castell|Cautious|Mercantile|0.5|1',2000)
  check('the guest appoints a stand-in (host)',await Hh("JSON.stringify(%s.regent&&%s.regent.traits)"%(HP,HP))=='["Cautious","Mercantile"]',m[:120])
  await G("(()=>{dockTab='allegiance';renderDock();document.querySelector('[data-rg=sleep]').click();return 1})()");await K.wait(3000)
  check('Sleep hands over on the host',await Hh("!!%s.asleep&&%s.asleep.by==='button'"%(HP,HP)))
  check('the guest sees the overlay',await G("!!S.player.asleep&&!document.getElementById('rgOv').hidden"))
  # the stand-in answers a demand for the guest's faction
  await Hh("(()=>{const P=%s;P.props=P.props||[];P.props.push({id:S.nextId++,f:FAC_IDS[0],k:'demand',amt:500,until:S.T+300});strategicTick();return 1})()"%HP);await K.wait(1500)
  lg=json.loads(await Hh("JSON.stringify(%s.asleep.log.map(x=>x.msg))"%HP))
  check('it answers the powers for the guest',any('tribute' in l for l in lg),lg[-2:])
  await K.wait(800);await K.C.keyboard.press('KeyW');await K.wait(3000)
  check('a key wakes the guest: the stand-in resigns (host)',await Hh("!%s.asleep&&!!%s.rgRep"%(HP,HP)))
  check('the guest gets the report',await G("!S.player.asleep&&!!document.getElementById('rgRepPop')&&!document.getElementById('rgRepPop').hidden"))
  # the guest leaves the galaxy: its stand-in holds the faction, its ship berthed at its Station
  await G("(()=>{document.getElementById('rgRepOk').click();netSend({t:'bye'});return 1})()");await K.wait(2500)
  aw=json.loads(await Hh("JSON.stringify({asleep:%s.asleep&&%s.asleep.by,docked:%s.docked,sector:%s.sector})"%(HP,HP,HP,HP)))
  check('leaving hands the faction to the stand-in (host)',aw['asleep']=='away' and aw['docked']=='station' and aw['sector']==sid,aw)
  # back again: the stand-in resigns at the next turn
  await Hh("(()=>{const c=Object.values(MP.cl).find(x=>x.pid==='clipid1');if(c)c.ready=true;else MP.cl.__back={pid:'clipid1',ready:true,L:{peer:'__back'}};strategicTick();return 1})()")
  check('coming back, the stand-in resigns (host)',await Hh("!%s.asleep&&%s.rgRep&&%s.rgRep.by==='away'"%(HP,HP,HP)))
  await Hh("(()=>{delete MP.cl.__back;return 1})()")
if __name__=="__main__":run(body,gcls='courier')
