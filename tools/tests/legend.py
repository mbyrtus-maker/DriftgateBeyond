# Beyond stage 14: Legend. A level 10 callsign's start package (Rating 2, +5,000 cr, a medium hull, three grade 2 parts) applied
# with the ledger exact; achievements award points once per galaxy; the leaderboard and package picker render; a win banks
# Conqueror's spoils, carried into the next galaxy (Renown, war chest, the Wraith) and then used up; a base perk starts a Station
import asyncio,json
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
async def launch(pg):
  await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
async def go(pg):
  await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);ctx=await b.new_context(viewport={'width':1400,'height':860});pg=await ctx.new_page();errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await launch(pg);ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await ev("(()=>{localStorage.setItem(LEG_KEY,JSON.stringify({recs:{tester:{name:'Tester',pts:0,wins:{},bp:40,pkg:[1,2,3,4]}}}));$('mpName').value='Tester';return 1})()")
    print('picker',await ev("(()=>{legOpen();return $('legBody').innerText.slice(0,400).replace(/\\n/g,' | ')})()"))
    await ev("(()=>{$('legend').hidden=true;return 1})()");await go(pg)
    print('start package',await ev("JSON.stringify({rating:ratingOf(),credits:S.player.credits,cls:S.player.cls,grades:fitOf(S.player).g,lvl:S.player.lvl})"))
    print('ledger',await ev(LED))
    print('award once',await ev("(()=>{const P=S.player;legbAward(P,'lair','test');legbAward(P,'lair','again');return JSON.stringify({bp:legPeek('Tester').bp})})()"))
    print('win banks spoils',await ev("(()=>{const P=S.player;P.decl={name:'Test Co',T:0};P.credits=60000;legAward('player');const r=legPeek('Tester');return JSON.stringify({bp:r.bp,spoils:r.spoils&&{cls:r.spoils.flag.cls,chest:r.spoils.chest,renown:r.spoils.renown,wraith:r.spoils.wraith}})})()"))
    # the next galaxy: pick a base perk instead, and carry the spoils
    await ev("(()=>{const d=legLoad();d.recs.tester.pkg=[10];legSave(d);try{localStorage.removeItem(SAVE_KEY)}catch(e){}return 1})()")
    await launch(pg);await go(pg)
    print('next galaxy',await ev("JSON.stringify({stand:S.player.stand,credits:S.player.credits,wraith:!!S.player.wraith,stations:myStations(S.player).map(R=>R.name),spoilsLeft:!!legPeek('Tester').spoils})"))
    print('ledger',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
