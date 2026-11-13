# Beyond, game length (12 Nov 2026): a new galaxy carries the Standard setting; the setting's dials drive the win rule
# (systems to win, hold time), the earliest hour a hold can start, the Brood's quiet opening and the offensive tempo; a
# save without a setting keeps the old rules; the ledger stays exact
import asyncio,json,os
from playwright.async_api import async_playwright
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="(()=>{const L=ledger();for(const e of RAWS)if(Math.abs(L.tot[e]-S.ledger0.tot[e])>1e-6)return 'ore '+e;return Math.abs(L.credits-S.ledger0.credits)<1e-6?'exact':'credits '+(L.credits-S.ledger0.credits)})()"
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1280,'height':800});errs=[];bad=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    def check(n,ok,d=''):
      print(('ok  ' if ok else 'FAIL'),n,str(d)[:300])
      if not ok:bad.append(n)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'")
    # the start screen's length choice: Standard is chosen; Long can be picked and is remembered; back to Standard for the rest
    r0=await pg.evaluate("(()=>{const b=[...document.querySelectorAll('#glens [data-glen]')];return{n:b.length,on:b.filter(x=>x.getAttribute('aria-pressed')==='true').map(x=>x.dataset.glen),txt:b.map(x=>x.textContent)}})()")
    await pg.click('#glens [data-glen="long"]');r1=await pg.evaluate("(()=>({new:__dg.ev('LEN_NEW'),on:[...document.querySelectorAll('#glens [aria-pressed=true]')].map(x=>x.dataset.glen),ls:localStorage.getItem('dgbeyond.glen')}))()")
    await pg.click('#glens [data-glen="std"]');r2=await pg.evaluate("__dg.ev('LEN_NEW')")
    check('the start screen offers Standard and Long, with Standard chosen',r0['n']==2 and r0['on']==['std'] and '24 systems held for 30 minutes' in r0['txt'][0] and 'hour 6' in r0['txt'][0],r0)
    check('picking Long sets the next galaxy\'s length and is remembered; Standard can be picked back',r1=={'new':'long','on':['long'],'ls':'long'} and r2=='std',[r1,r2])
    await pg.evaluate("document.getElementById('bLaunch').click()")
    await pg.wait_for_function('__dg.ev("!!(S&&S.player)")',timeout=60000);await pg.wait_for_timeout(1200)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    r=json.loads(await ev("JSON.stringify({glen:S.glen,key:lenKey(),need:VIC_NEED,hold:WIN_TIME,std:LEN_SET.std})"))
    check('Standard is 24 systems for 30 minutes with no win before hour 6; the map says so',r['need']==24 and r['hold']==1800 and r['std']['floor']==21600 and 'no win before hour 6' in await ev("lenMapNote()"),await ev("lenMapNote()"))
    check('a new galaxy carries the Standard length setting, and the win rule reads its dials',r['glen']=='std' and r['key']=='std' and r['need']==r['std']['need'] and r['hold']==r['std']['hold'],r)
    r=json.loads(await ev("""(()=>{running=false;const keep={...LEN_SET.std};Object.assign(LEN_SET.std,{quiet:3600,full:7200,bq:.4,floor:7200,hold:1800,need:22,tempo:2});
      S.T=10;strategicTick();const out={need:VIC_NEED,hold:WIN_TIME,f0:lenBroodF()};const b0=BR0.brOff/(S.broodK||1);out.brOff=BAL.brOff/b0;
      S.T=5400;lenApply();out.fMid=lenBroodF();S.T=7300;out.fFull=lenBroodF();
      // the floor: a side at the win count before the floor starts no clock
      S.T=100;const cc=controlCounts;controlCounts=()=>({halcyon:25});victoryTick();out.vicEarly=S.victory;S.T=7300;victoryTick();out.vicLate=S.victory&&S.victory.side;controlCounts=cc;S.victory=null;
      // tempo: the wait to the next offensive is doubled
      S.T=8000;const po=S.ai.varkesh;LEN_SET.std.tempo=1;lenApply();const camp=campBusy;campBusy=()=>true;const r0=[];for(let i=0;i<40;i++){planOffensive('varkesh');r0.push(po.next-S.T)}LEN_SET.std.tempo=2;lenApply();const r1=[];for(let i=0;i<40;i++){planOffensive('varkesh');r1.push(po.next-S.T)}campBusy=camp;
      out.t1=r0.reduce((a,b)=>a+b,0)/40;out.t2=r1.reduce((a,b)=>a+b,0)/40;
      const g=S.glen;S.glen=undefined;lenApply();out.legacy={need:VIC_NEED,hold:WIN_TIME,key:lenKey()};S.glen=g;Object.assign(LEN_SET.std,keep);lenApply();S.T=10;return JSON.stringify(out)})()"""))
    check('the dials set the systems to win and the hold time',r['need']==22 and r['hold']==1800,r)
    check("the Brood's quiet opening: 40% strength at first, rising to full by the set hour",abs(r['f0']-.4)<1e-9 and abs(r['fMid']-.7)<1e-9 and r['fFull']==1 and abs(r['brOff']-2.5)<1e-6,r)
    check('no hold starts before the floor; after it the clock starts as before',r['vicEarly'] is None and r['vicLate']=='halcyon',r)
    check('tempo 2 doubles the wait to the next offensive',1.7<r['t2']/r['t1']<2.3,r)
    check('a galaxy with no setting keeps the old rules (20 systems, 10 minutes)',r['legacy']=={'need':20,'hold':600,'key':'legacy'},r)
    l=await ev(LED);check('ledger exact',l=='exact',l)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
