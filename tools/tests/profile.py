# Beyond, the company profile (8 Nov 2026): no Depot or Station any way (or their kits) without one; Company → Profile shows
# name, twelve logos, six base designs, a hue slider and fees; a hue too close to a power's is refused; saving takes a
# 100,000 cr deposit into the company treasury; new bases take the profile's design and fees; the base business (a crew hired)
# is paid from the treasury, not your credits; Deposit and Withdraw; the ledger stays exact throughout
import asyncio,json
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.join(' ')||'exact'})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[];bad=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    def check(name,ok,info=''):
      print(('ok   ' if ok else 'FAIL ')+name,info)
      if not ok:bad.append(name)
    r=json.loads(await ev("""(()=>{running=false;const P=S.player;const sid=Object.keys(DEF).find(s=>depCan(s)&&DEF[s].kind!=='hive'&&DEF[s].kind!=='den');exitSector();W=null;P.sector=sid;enterSector(sid);running=false;P.docked=null;
      devLedger(()=>inv.add(P.cargo,'frame',2));const m=depFresh(P);return JSON.stringify({sid,m,none:!S.stations[sid]})})()"""))
    check('no Depot without a company profile',r['none'] and 'Profile' in r['m'],r)
    r=json.loads(await ev("""(()=>{$('company').hidden=false;coTab='profile';renderCompany();const B=$('coBody');return JSON.stringify({name:!!$('coNm'),hue:!!$('coHue'),logos:B.querySelectorAll('[data-arg^="logo:"]').length,designs:B.querySelectorAll('[data-arg^="design:"]').length,fees:B.querySelectorAll('[data-arg^="fee:"]').length,tab:!!document.querySelector('#coTabs [data-arg="profile"]')})})()"""))
    check('Company → Profile: name, 12 logos, 6 designs, a hue slider, three fees',r['name'] and r['hue'] and r['logos']==12 and r['designs']==6 and r['fees']==6 and r['tab'],r)
    r=json.loads(await ev("""(()=>{const P=S.player,hh=Math.round(hexHue(FACTIONS.halcyon.col));const a=coSave(P,`name=Tester%20Works;logo=3;design=6;hue=${hh};tx=0.08;svc=150;dock=20`);
      P.credits=Math.min(P.credits,5000);let ok=40;while(coHueClash(ok))ok+=11;const b=coSave(P,`name=Tester%20Works;logo=3;design=6;hue=${ok};tx=0.08;svc=150;dock=20`);
      devLedger(()=>{P.credits+=150000});const c0=P.credits,cs=coSave(P,`name=Tester%20Works;logo=3;design=6;hue=${ok};tx=0.08;svc=150;dock=20`);
      return JSON.stringify({a,b,cs,paid:c0-P.credits,tr:S.econ.treasury[P.co.w]||0,name:coName(P),col:coCol(pkeyOf(P))===coHueCol(ok)})})()"""))
    check('a hue too close to a power\'s colour is refused',"too close" in r['a'],r)
    check('saving needs the 100,000 cr deposit',"100,000" in r['b'],r)
    check('saved: 100,000 cr into the treasury, the name and colour set',r['cs'].startswith('✓') and r['paid']==100000 and r['tr']==100000 and r['name']=='Tester Works' and r['col'],r)
    l=await ev(LED);check('ledger exact after opening the treasury',l=='exact',l)
    r=json.loads(await ev("""(()=>{const P=S.player;$('company').hidden=true;const m=depFresh(P),R=S.stations[P.sector];const c0=P.credits,t0=S.econ.treasury[P.co.w];const h=crewHire(R,P,'skiff');
      return JSON.stringify({m,design:R&&R.design,fees:R&&R.fees,h,cr:P.credits-c0,tr:S.econ.treasury[P.co.w]-t0,crew:(R.crew||[]).length})})()"""))
    check('with a profile the Depot is built, in its design and with its fees',r['m'].startswith('✓') and r['design']==6 and r['fees'] and r['fees'].get('dock')==20,r)
    check('a crew hired at it is paid from the treasury, not your credits',r['crew']==1 and r['cr']==0 and r['tr']<0,r)
    r=json.loads(await ev("""(()=>{const P=S.player,w=P.co.w,t0=S.econ.treasury[w],c0=P.credits;const a=coTreas(P,'in:10000'),t1=S.econ.treasury[w];const b=coTreas(P,'out:all');return JSON.stringify({a,b,dep:t1-t0,back:P.credits-c0,left:S.econ.treasury[w]})})()"""))
    check('Deposit and Withdraw move credits between you and the treasury',r['dep']==10000 and r['left']==0,r)
    r=json.loads(await ev("""(()=>{const P=S.player,col=coCol(pkeyOf(P)),h=allegianceHtml(P);return JSON.stringify({col,inLogo:h.includes(col),nm:brName(brSlot(P)),hasNm:h.includes(esc(brName(brSlot(P))))})})()"""))
    check("Allegiance → Your company draws the logo and name in the company's chosen colour",r['inLogo'] and r['hasNm'],r)
    l=await ev(LED);check('ledger exact at the end',l=='exact',l)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
