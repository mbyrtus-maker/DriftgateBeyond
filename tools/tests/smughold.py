# Beyond, the Smuggler's hold (9 Nov 2026): Unbound gear made at Scrapheart from the Unbound's stores and sold there; installed as
# the cargo system it cuts the hold by 20% and a customs scan that finds contraband comes out clear about half the time; the
# ledger stays exact
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
    r=json.loads(await ev("""(()=>{running=false;const P=S.player;exitSector();W=null;S.smhT=0;smhTick();const R=S.stations.wr,st=mkStock(R),shelf=st.sy_smug_cargo||0;
      P.sector='wr';enterSector('wr');running=false;P.docked='station';devLedger(()=>{P.credits+=10000});const c0=P.credits,cg0=shipStats(P.faction,P.cls,P.tiers,P.tune).cargo;dockAction('buy','sy_smug_cargo:1');const paid=c0-P.credits,got=countIn('sy_smug_cargo',[P.cargo,P.vault]);
      dockAction('sysfit','cargo:sy_smug_cargo');const fit=dockErr,cg1=shipStats(P.faction,P.cls,P.tiers,P.tune).cargo;return JSON.stringify({shelf,paid,got,fit,on:smhOn(P),cg0,cg1,name:ldSysName(P,'cargo')})})()"""))
    check('Scrapheart makes and shelves the Smuggler\'s hold; it sells for 3,500 cr',r['shelf']>=1 and r['paid']==3500 and r['got']==1,r)
    check('installed as the cargo system: 20% less hold',r['on'] and r['fit'].startswith('✓') and r['cg1']<=round(r['cg0']*0.8)+1 and r['cg1']<r['cg0'] and r['name']=="Smuggler's hold",r)
    r=json.loads(await ev("""(()=>{const P=S.player;P.docked=null;devLedger(()=>inv.add(P.cargo,'rift',3));let clear=0,n=200;for(let i=0;i<n;i++){P.caught=null;scanResolve(P,'halcyon','me');if(!P.caught)clear++}P.caught=null;
      const sm=P.sysm.cargo;P.sysm.cargo=null;let clear0=0;for(let i=0;i<n;i++){P.caught=null;scanResolve(P,'halcyon','me');if(!P.caught)clear0++}P.caught=null;P.sysm.cargo=sm;devLedger(()=>inv.take(P.cargo,'rift',3));return JSON.stringify({clear,clear0,n})})()"""))
    check('with contraband aboard, about half the scans come out clear (none without it)',r['clear0']==0 and 70<=r['clear']<=130,r)
    l=await ev(LED);check('ledger exact',l=='exact',l)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
