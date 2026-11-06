# Beyond: posting jobs to other pilots, with bidding. The galactic mean and the three bids (Low waits longest, Fast least),
# the 200% cap; Supply (goods bought at the nearest market at your expense), Haul (sold for you), Mine (ore cut into the store)
# and Guard (the depot's guns up) done by AI takers flying the jobs (16zzr_contract.js) and paid; a job withdrawn; another player delivering a Supply job; the
# tab renders; the ledger stays exact
import asyncio,json
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    print('depot',await ev("""(()=>{const P=S.player;undock();P.rp=5000;const sid=SECTOR_DEFS.map(d=>d.id).find(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id]&&S.sectors[id].ast.some(a=>!a.rift&&oreTotal(a)>40));exitSector();P.sector=sid;P.docked=null;enterSector(sid);P.cls='bulker';fitOf(P);refreshPlayerStats();devLedger(()=>{P.cargo={frame:2}});
      depFresh(P);const R=S.stations[sid];devLedger(()=>{inv.add(R.stock,'plate',60)});transfer('halcyon','player',20000);window._SID=sid;return JSON.stringify({sid,credits:P.credits})})()"""))
    print('bids',await ev("""(()=>{const P=S.player,sid=window._SID,out={};for(const b of['low','medium','fast']){const m=pjPost(P,`${sid}:supply:plate:20:${b}`);const j=S.pj[S.pj.length-1];out[b]={bid:j.bid,mean:j.mean,wait:Math.round(j.claimAt-S.T)}}
      const m=pjPost(P,`${sid}:supply:plate:20:999999`);const j=S.pj[S.pj.length-1];out.cap=Math.round(j.bid/j.mean*100)+'%';out.withdraw=pjCancel(P,j.id);return JSON.stringify(out)})()"""))
    print('ledger',await ev(LED))
    print('done by AI',await ev("""(()=>{const P=S.player,sid=window._SID,R=S.stations[sid];pjPost(P,`${sid}:haul:plate:20:fast`);pjPost(P,`${sid}:mine:x:15:medium`);pjPost(P,`${sid}:guard:x:0:medium`);
      const pl0=R.stock.plate||0,st0=invMass(R.stock),c0=P.credits;for(const j of S.pj)if(j.state==='open')j.claimAt=S.T;pjTick();const guard=depGunK({rec:R},{role:'raider',side:'pirate'});exitSector();for(let i=0;i<300&&S.pj.some(j=>j.state==='taken');i++){S.T+=10;pjTick()}enterSector(sid);
      return JSON.stringify({states:S.pj.map(j=>j.kind+':'+j.state),msgs:S.pj.filter(j=>j.msg).map(j=>j.msg).slice(-5),plate:[pl0,R.stock.plate||0],store:[st0,invMass(R.stock)],spent:c0-P.credits,guardK:guard})})()"""))
    print('still taken',await ev("JSON.stringify(S.pj.filter(j=>j.state==='taken').map(j=>({kind:j.kind,run:j.run,due:j.due,r:JSON.stringify(pjRunOf(j.run))})))"))
    print('ledger',await ev(LED))
    print('another player delivers',await ev("""(()=>{const P=S.player,sid=window._SID,R=S.stations[sid];pjPost(P,`${sid}:supply:fe:10:medium`);const j=S.pj[S.pj.length-1];const Q={name:'Guest',cargo:{fe:10},credits:0,docked:'station',sector:sid};
      const k=pkeyOf(P);j.pid='zz';const save=xPilotOfKey;S.pilots=S.pilots||{};S.pilots.zz=P;let m;devLedger(()=>{m=pjDo(Q,j.id)});delete S.pilots.zz;return JSON.stringify({m,state:j.state,fe:R.stock.fe||0})})()"""))
    print('tab',await ev("(()=>{coTab='crews';$('company').hidden=false;renderCompany();return $('coBody').innerText.slice(-500).replace(/\\n/g,' | ')})()"))
    await pg.wait_for_timeout(10000)
    print('after flight',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
