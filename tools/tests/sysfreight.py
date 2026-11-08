# Beyond, makers ship their systems (8 Nov 2026): maker freighters carry systems from home to the shelves they serve and
# bring missing components home; a maker's payload bay line starts at grade 2; the Loadout shows every system on the ship;
# the ledger stays exact throughout
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
    # the Loadout: every system has its place on the ship
    lo=json.loads(await ev("""(()=>{const P=S.player;P.docked='station';openDock();dockTab='upg';ldSel='parts';renderDock();const n=document.querySelectorAll('.ldsysp').length,strip=document.querySelectorAll('.ldsysrow').length;
      document.querySelector('.ldsysp[data-arg="sys:engine"]').click();const panel=!!document.querySelector('#ldSysHost');dockTab='home';renderDock();return JSON.stringify({n,strip,panel})})()"""))
    check('every system has a place on the ship (7 on a fighter), no strip, a click opens its panel',lo['n']==7 and lo['strip']==0 and lo['panel'],lo)
    check('a maker\'s payload bay line starts at grade 2',await ev("rdLineG('wf','sy_wf_payload')===2&&rdLineG('mwa','sy_mwa_payload')===2"))
    r=json.loads(await ev("""(()=>{const cen=()=>{let n=0;for(const sid in S.stations){const R=S.stations[sid];if(!syfOk(R))continue;const st=mkStock(R);if(Object.keys(st).some(id=>ITEMS[id]&&ITEMS[id].sys&&st[id]>0))n++}return n};
      const a=cen();running=false;exitSector();W=null;const seen={out:0,in:0},ids=new Set();let land=0;
      for(let i=0;i<540;i++){S.T+=10;strategicTick();updateEvents();for(const t of S.traders||[])if(t.syf&&!ids.has(t.id)){ids.add(t.id);seen[t.syf.k]++}}
      const live=new Set((S.traders||[]).filter(t=>t.syf).map(t=>t.id));for(const id of ids)if(!live.has(id))land++;
      return JSON.stringify({before:a,after:cen(),of:Object.values(S.stations).filter(syfOk).length,seen,landed:land})})()"""))
    check('maker freighters went out and brought supplies in',r['seen']['out']>=5 and r['seen']['in']>=1 and r['landed']>=3,r)
    check('more markets carry systems after an hour and a half',r['after']>r['before'],r)
    l=await ev(LED);check('ledger exact',l=='exact',l)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
