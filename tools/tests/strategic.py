# Beyond stage 12: the strategic map. Clicking a system shows a sector view (live in the loaded system, from intel elsewhere)
# with ship and threat counts; your capitals and crews there take orders from it
import asyncio,json,sys
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
SHOT=sys.argv[1] if len(sys.argv)>1 else None
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await ev("(()=>{undock();return 1})()")
    print('here',await ev("(()=>{toggleMap();mapSel=S.player.sector;renderMapSide();const cv=$('sxCv');return JSON.stringify({canvas:!!cv,view:sxDraw(cv,mapSel),head:$('mapSide').innerText.slice(0,40)})})()"))
    print('elsewhere',await ev("(()=>{mapSel=NEIGH[S.player.sector][0];renderMapSide();return JSON.stringify(sxDraw($('sxCv'),mapSel))})()"))
    # your capital takes an order from the view
    print('order',await ev("""(()=>{const t=makeEscort('player',S.player.sector,{});const sid=NEIGH[S.player.sector][0];mapSel=sid;renderMapSide();const b=[...document.querySelectorAll('#mapSide [data-sx=come]')].find(x=>x.dataset.arg===String(t.id));if(!b)return 'no button';b.click();return JSON.stringify({dest:t.dest,sid})})()"""))
    if SHOT:
      await ev("(()=>{mapSel=S.player.sector;renderMapSide();drawMap();return 1})()");await pg.wait_for_timeout(400);await pg.screenshot(path=SHOT)
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
