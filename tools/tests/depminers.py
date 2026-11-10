# Beyond, your Depot's miners (9 Nov 2026): a Depot built from a Depot Kit comes with 3 miners built from the kit's makings;
# off-screen it mines only through its miners (none, no ore); live they fly from the depot; one shot down leaves the roster
# and is rebuilt from the store; the ledger stays exact
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
    r=json.loads(await ev("""(()=>{const P=S.player;coDefault(P);undock();const sid=SECTOR_DEFS.map(d=>d.id).filter(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id]&&S.sectors[id].ast.length>5)[0];exitSector();P.sector=sid;P.docked=null;enterSector(sid);running=false;
      devLedger(()=>{P.cargo={kit_depot:1}});const m=depFresh(P);const R=S.stations[sid],ro=S.mrs['S.'+sid];window._S=sid;return JSON.stringify({m,n:ro?ro.m.length:0,work:mrWork('S.'+sid),cargo:P.cargo})})()"""))
    check("a Depot built from a kit comes with 3 miners from the kit's makings",r['n']==3 and abs(r['work']-1)<0.35 and 'miners launched' in r['m'],r)
    r=json.loads(await ev("""(()=>{const sid=_S,R=S.stations[sid],P=S.player;exitSector();W=null;P.sector=Object.keys(S.stations).find(x=>x!==sid&&S.stations[x].owner==='halcyon');enterSector(P.sector);running=false;
      const o0=invMass(R.stock);for(let i=0;i<30;i++){S.T+=10;strategicTick()}const with3=invMass(R.stock)-o0;const ro=S.mrs['S.'+sid];const keep=ro.m.splice(0);const o1=invMass(R.stock);ro.t=S.T+1e9;for(let i=0;i<30;i++){S.T+=10;strategicTick()}const none=invMass(R.stock)-o1;ro.m.push(...keep);ro.t=S.T;
      return JSON.stringify({with3,none})})()"""))
    check('off-screen the depot mines through its miners only (none, no ore)',r['with3']>0 and r['none']<=0,r)
    r=json.loads(await ev("""(()=>{const sid=_S,R=S.stations[sid],P=S.player;exitSector();W=null;P.sector=sid;P.docked=null;enterSector(sid);running=false;for(let i=0;i<60;i++){S.T+=1;worldUpdate(1/60)}populate(true);
      const ships=W.ents.filter(e=>e.alive&&e.mrKey==='S.'+sid);const n0=S.mrs['S.'+sid].m.length;let killed=false;if(ships[0]){killShip(ships[0]);killed=true}const n1=S.mrs['S.'+sid].m.length;
      devLedger(()=>{inv.addAll(R.stock,{plate:4,wire:4})});S.mrs['S.'+sid].t=S.T;mrTick();const n2=S.mrs['S.'+sid].m.length;return JSON.stringify({live:ships.length,side:ships[0]&&ships[0].side,killed,n0,n1,n2})})()"""))
    check('live, the miners fly; one shot down leaves the roster, and the store builds another',r['live']>=1 and r['killed'] and r['n1']==r['n0']-1 and r['n2']==r['n0'],r)
    r=json.loads(await ev("""(()=>{const e=W&&W.ents.find(x=>x.alive&&x.mrKey&&x.side==='player');return JSON.stringify({lab:e?shipLabel(e):null})})()"""))
    check("your Depot's miners are labelled as its miners, not wingmen",r['lab'] and 'miner' in r['lab'] and 'wingman' not in r['lab'],r)
    l=await ev(LED);check('ledger exact',l=='exact',l)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
