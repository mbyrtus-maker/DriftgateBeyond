# Beyond: the leaders' news box above the Recent ticker. A leader's declaration (war, embargo, a pact) goes into the box under
# their faction and name and not into Recent; a relations band change stays in Recent only; the Dread Pirate's ☠ announcements
# go into the box (the chronicle's copy doesn't); only the newest three stay; each fades and goes after three
# minutes; it renders in the HUD
import asyncio,json,os
from playwright.async_api import async_playwright
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
SHOT=os.environ.get('DG_SHOT')
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    print('undock',await ev("(()=>{undock();relInit();S.news=[];return 1})()"));await pg.wait_for_timeout(1500)
    print('band',await ev("(()=>{chron('Halcyon and Varkesh are now Cool.','bad',['halcyon','varkesh']);return (S.news||[]).length})()"))
    print('war',await ev("(()=>{evWar('varkesh','ostrova');const x=S.news[S.news.length-1];return JSON.stringify(x)})()"))
    print('embargo',await ev("(()=>{evEmbargo('halcyon','varkesh');return S.news.length})()"))
    print('dread',await ev("(()=>{const n0=S.news.length;chron(dpName()+' went down with the Ravager.');const dup=S.news.length-n0;allFeed('☠ '+dpName()+' declares a raiding season on Halcyon lanes.','warn');const x=S.news[S.news.length-1];return 'chron copy added '+dup+' · '+JSON.stringify(x)})()"))
    print('pact',await ev("(()=>{evPact('ostrova','halcyon','plate');return S.news.length+' '+S.news.map(x=>x.f).join(',')})()"))
    await pg.wait_for_timeout(1200)
    print('recent',await ev("(()=>{const L=FEED.map(f=>f.msg);return JSON.stringify({band:L.some(m=>/now Cool/.test(m)),war:L.some(m=>/declares war/.test(m)),embargo:L.some(m=>/embargo/.test(m)),dread:L.some(m=>/Dread Pirate/.test(m)),pact:L.some(m=>/trade pact/.test(m))})})()"))
    print('hud',await ev("(()=>{const e=$('hNews');return (e.hidden?'HIDDEN ':'')+e.innerText.replace(/\\n/g,' | ')})()"))
    if SHOT:await pg.screenshot(path=SHOT)
    print('fading',await ev("(()=>{S.T+=165;hudUpdate();return [...$('hNews').querySelectorAll('.nwi')].map(e=>e.style.opacity).join(',')})()"))
    print('gone',await ev("(()=>{S.T+=20;hudUpdate();return $('hNews').hidden})()"))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
