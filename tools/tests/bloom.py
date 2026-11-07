# Beyond, the Bloom grows from raw ore (6 Nov 2026): Bloom Nodes grow weapons and hull-and-shield modules from the mass of ore
# they'd be made of (any ore, node store first, then the hive's spare), with no crew; the Brood grows its Leviathan and
# Prowlers at a Bloom Node the same way; the ledger stays exact throughout
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
    print('ledger',await ev(LED))
    # a Bloom Node (the test grows one and books its frames) with 3000 t of Iridium in the hive: it grows on Iridium alone
    print('node grows',await ev("""(()=>{running=false;exitSector();W=null;const n=SECTOR_DEFS.map(d=>d.id).find(id=>canBuildIn(id,'brood')&&NEIGH[id].some(x=>broodHeld(x)));
      const R=makeStation(n,'brood','depot',stationSite(n),{...DEPOT_COST});const hv=S.econ.stock.brood;hv.ir=(hv.ir||0)+3000;const v=invVec(DEPOT_COST);for(const e of RAWS)S.ledger0.tot[e]+=v[e];S.ledger0.tot.ir+=3000;
      for(const x of bloomNodes())if(x!==R){x.dev=x.dev||{};x.dev.def=3;x.dev.armor=3}
      const ir0=hv.ir,lv0=depotLevel(R);for(let i=0;i<8;i++){S.ai.brood.grow=0;bloomGrowTick()}const d=devOf(R);
      return JSON.stringify({node:n,level:[lv0,depotLevel(R)],def:d.def,armor:d.armor,irEaten:ir0-hv.ir,fort:invMass(R.fort),noCrew:devCap(R)>10})})()"""))
    print('ledger',await ev(LED))
    print('Leviathan grown at a node',await ev("""(()=>{const hv=S.econ.stock.brood;hv.xc=(hv.xc||0)+4000;S.ledger0.tot.xc+=4000;S.T=Math.max(S.T,BAL.brLevT+1);for(const t of S.frigates.filter(x=>x.side==='brood'))t.hull=0;S.frigates=S.frigates.filter(x=>x.side!=='brood');
      const L=ledger().tot;S.ai.brood.capT=0;bloomCapTick();const ev=S.events.find(e=>e.type==='frigbuild'&&e.att==='brood'&&e.bloom);if(!ev)return 'none';const at=ev.sector,m=invMass(ev.force);
      let i=0;while(ev.stage!=='done'&&i<40){S.T+=10;capitalTick();i++}const t=S.frigates.find(x=>x.side==='brood'&&isCar(x));return JSON.stringify({grownAt:at,node:!!S.stations[at]&&S.stations[at].owner==='brood',mass:m,launched:!!t,in:t&&t.sector})})()"""))
    print('ledger',await ev(LED))
    print('an hour on',await ev("(()=>{for(let i=0;i<360;i++){S.T+=10;strategicTick();updateEvents()}return bloomNodes().map(R=>depotLevel(R)).join(',')})()"),await ev(LED))
    print('errors',errs[:5] or 'none')
    await b.close()
asyncio.run(main())
