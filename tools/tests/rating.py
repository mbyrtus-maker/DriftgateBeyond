# Beyond stage 8: Contractor Rating. Starts at 1; work for the powers raises it (never falls); it gates hulls at the yard and
# the grades parts and systems upgrade to; the Allegiance tab shows it; the start screen has no Unbound card
import asyncio,json
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    print('start cards',await ev("JSON.stringify([...document.querySelectorAll('#facs [data-fac]')].map(b=>b.dataset.fac+':'+(b.dataset.port||'-')))"))
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    print('start',await ev("JSON.stringify({rating:ratingOf(),rp:S.player.rp||0,cap:gradeCap(S.player),unb:!!S.unb})"))
    print('hull refused',await ev("(()=>{const P=S.player;P.credits+=0;dockAction('hull','striker');return JSON.stringify({msg:dockErr,cls:P.cls})})()"))
    print('work',await ev("(()=>{const P=S.player;const r=[];for(let i=0;i<8;i++){standWork(P,'halcyon',4,'a delivery');r.push(ratingOf(P))}P.stand.halcyon=0;return JSON.stringify({ratings:r,rp:P.rp,feed:FEED.slice(0,3).map(f=>f.t||f.msg||f.text||'')})})()"))
    print('hull allowed',await ev("(()=>{const P=S.player;dockAction('hull','striker');return JSON.stringify({msg:String(dockErr).slice(0,80),cls:P.cls})})()"))
    print('grade caps',await ev("JSON.stringify([1,2,3,4,5,6,7,8,9,10].map(r=>{const P={rp:RATING.need[r]};return r+':'+gradeCap(P)}))"))
    print('part upgrade capped',await ev("""(()=>{const P=S.player,F=fitOf(P);devLedger(()=>{F.g[0]=Math.max(F.g[0],gradeCap(P))});const q=pupQuote({fee:false},P,'w:0');return JSON.stringify({rating:ratingOf(P),grade:F.g[0],next:q})})()"""))
    print('systems capped',await ev("(()=>{const P=S.player;P.tiers.weapon=gradeCap(P);dockAction('upg','weapon');return dockErr})()"))
    print('never falls',await ev("(()=>{const P=S.player,r=ratingOf(P);standAdd('halcyon',-80,'test',P);return JSON.stringify({before:r,after:ratingOf(P)})})()"))
    print('allegiance',await ev("(()=>{dockTab='allegiance';renderDock();const t=document.querySelector('#dBody').innerText;const i=t.search(/contractor rating/i);return i>=0?t.slice(i,i+120).replace(/\\n/g,' | '):'missing'})()"))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
