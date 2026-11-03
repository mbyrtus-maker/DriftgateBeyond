# Beyond: the developer panel without a faction: every power as an enemy side, the Beyond tools (standing, Rating, heat,
# base kits, crews, Rift Shards, the Dread Pirate, Scrapheart, time), the old tools, the ledger exact after each
import asyncio
from playwright.async_api import async_playwright
import os
G='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
SP='/tmp/claude-0/-home-claude/82d47366-d8e2-5d87-95a4-e70ca203b8c5/scratchpad'
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e);if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr');return b.length?'DRIFT '+b:'exact'})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':900});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text[:200]) if m.type=='error' and 'Failed to load' not in m.text else None)
    await pg.goto(G+'?name=Tester');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await ev("(()=>{undock();devToggle();return 1})()");await pg.wait_for_timeout(300)
    for k in ['bx:st+','bx:rp','bx:hot','bx:cool','bx:klair','bx:kst','bx:rift','bx:dread','bx:haven','bx:time','gbwing','cr','res']:
      print(k,await ev(f"(()=>{{devDo('{k}');return $('devMsg').textContent}})()"),await ev(LED))
    print('sides',await ev("[...$('devSide').options].map(o=>o.value).join(',')"))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
