# Beyond: the strategic map zooms into a system (button, wheel, double click, the Galaxy box) and draws it full size with
# your capitals named; a capital ordered to patrol sweeps the system and its neighbours; one ordered to escort follows you
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
    print('zoom',await ev("""(()=>{toggleMap();const sid=S.player.sector;mapSel=sid;renderMapSide();const b=document.querySelector('#mapSide [data-sx=zoom]');b.click();return JSON.stringify({zoom:mapZoom,btn:document.querySelector('#mapSide [data-sx=zoom]').textContent})})()"""))
    await pg.wait_for_timeout(300)
    print('drawn',await ev("(()=>{const c=mctx.getImageData(0,0,mcv.width,mcv.height).data;let n=0;for(let i=0;i<c.length;i+=4)if(c[i]+c[i+1]+c[i+2]>120)n++;return n})()"))
    box=await pg.evaluate("(()=>{const r=document.getElementById('mapCv').getBoundingClientRect();return [r.left,r.top]})()")
    await pg.mouse.click(box[0]+40,box[1]+20)
    print('back',await ev("String(mapZoom)"))
    await pg.mouse.move(box[0]+300,box[1]+300);await pg.mouse.wheel(0,-200);await pg.wait_for_timeout(200)
    print('wheel in',await ev("String(mapZoom)"))
    await pg.mouse.wheel(0,200);await pg.wait_for_timeout(200)
    print('wheel out',await ev("String(mapZoom)"))
    print('patrol',await ev("""(()=>{const t=makeEscort('player',S.player.sector,{});window._T=t;const sid=S.player.sector;mapSel=sid;renderMapSide();const b=[...document.querySelectorAll('#mapSide [data-sx=patrol]')].find(x=>x.dataset.arg===String(t.id));if(!b)return 'no button';b.click();
      const seen=[t.sector];for(let i=0;i<40;i++){S.T+=70;strategicTick();if(t.dest&&t.dest!==t.sector){t.sector=t.dest;t.dest=null}if(seen[seen.length-1]!==t.sector)seen.push(t.sector)}return JSON.stringify({route:t.patrol.route,visited:seen.slice(0,6)})})()"""))
    print('escort',await ev("""(()=>{const t=window._T,P=S.player;mapSel=t.sector;renderMapSide();const b=[...document.querySelectorAll('#mapSide [data-sx=escort]')].find(x=>x.dataset.arg===String(t.id));b.click();const to=NEIGH[P.sector].find(s=>s!==t.sector)||NEIGH[P.sector][0];P.docked=null;exitSector();P.sector=to;enterSector(to);strategicTick();return JSON.stringify({patrol:t.patrol,escort:!!t.escort,dest:t.dest,you:P.sector})})()"""))
    print('hold clears',await ev("""(()=>{const t=window._T;mapSel=t.sector;renderMapSide();sxOrder('hold',String(t.id));return JSON.stringify({patrol:t.patrol,escort:t.escort})})()"""))
    print('ledger',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
