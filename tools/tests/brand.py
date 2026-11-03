# Beyond: your own brand. No brand without a Depot; a name and a trait shaped with points that net to zero (an unpaid strength
# refused); a gun built at your Depot's workshop carries the brand's name and trait, and fitted it changes the gun's damage;
# reshaping costs credits and reshapes the parts you have; the tab renders; the ledger stays exact
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
    print('no depot',await ev("brSave(S.player,'x|gun:dmg=1,ammo=-1')"))
    print('depot',await ev("""(()=>{const P=S.player;undock();P.rp=5000;const sid=SECTOR_DEFS.map(d=>d.id).find(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id]);exitSector();P.sector=sid;P.docked=null;enterSector(sid);P.cls='bulker';fitOf(P);refreshPlayerStats();devLedger(()=>{P.cargo={frame:2}});
      depFresh(P);const R=S.stations[sid];devLedger(()=>{inv.add(R.stock,'plate',20);inv.add(R.stock,'wire',10)});transfer('halcyon','player',5000);window._SID=sid;return sid})()"""))
    print('unpaid strength',await ev("brSave(S.player,encodeURIComponent('Kestrel Works')+'|gun:dmg=3,ammo=-1')"))
    print('set',await ev("(()=>{const m=brSave(S.player,encodeURIComponent('Kestrel Works')+'|gun:dmg=3,ammo=-3;cargo:cargo=2,speed=-2');const N=brSlot(S.player);return JSON.stringify({m,N,brand:S.brands[N]})})()"))
    print('built at the depot',await ev("""(()=>{const P=S.player,sid=window._SID;P.docked='station';openDock();const c=dockCtx();dockAction('make','pt_gun:1');const N=brSlot(P),id='bp'+N+'_gun';return JSON.stringify({msg:dockErr,stock:S.stations[sid].stock[id]||0,name:ITEMS[id].name,tr:ITEMS[id].tr,txt:ITEMS[id].trTxt})})()"""))
    print('ledger',await ev(LED))
    print('fitted',await ev("""(()=>{const P=S.player,N=brSlot(P),id='bp'+N+'_gun';P.cls='striker';fitOf(P);refreshPlayerStats();const F=fitOf(P);const i=F.w.indexOf('gun');if(i<0)return 'no gun slot '+JSON.stringify(F.w);const a=mkTr(P,'gun','dmg');const old=F.wi[i];devLedger(()=>{F.wi[i]=id});return JSON.stringify({before:a,after:mkTr(P,'gun','dmg'),ammo:mkTr(P,'gun','ammo')})})()"""))
    print('reshape',await ev("(()=>{const P=S.player,c0=P.credits;const m=brSave(P,encodeURIComponent('Kestrel Works')+'|gun:dmg=1,ammo=-1');return JSON.stringify({m,paid:c0-P.credits,now:mkTr(P,'gun','dmg')})})()"))
    print('ledger',await ev(LED))
    print('tab',await ev("(()=>{undock();coTab='holdings';$('company').hidden=false;renderCompany();return $('coBody').innerText.split(/your brand/i).slice(-1)[0].slice(0,300).replace(/\\n/g,' | ')})()"))
    await pg.wait_for_timeout(8000)
    print('after flight',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
