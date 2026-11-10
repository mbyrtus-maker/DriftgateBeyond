# Beyond, the jobs you're on in flight (9 Nov 2026): the HUD's orders card lists every job you've taken, not only one
# picked with Select job: freight, escorts, guard jobs, black-market runs and contracts, each with where it is and its pay
import asyncio,json
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
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
    r=json.loads(await ev("""(()=>{const P=S.player,me=pkeyOf(P);running=false;for(let i=0;i<6;i++){S.T+=10;strategicTick();updateEvents()}P.docked=null;
      const empty=(campHud(),$('hOrd').hidden?'':$('hOrd').innerText);
      const m=Object.keys(MAKERS)[0];bmoAll().push({id:99901,k:'spy',by:'corp_'+Object.keys(MAKERS)[1],tgt:m,pay:3000,taker:me});
      const to=Object.keys(S.stations).find(s=>FAC_IDS.includes(S.stations[s].owner));P.run={id:99902,item:'fe',n:8,f:S.stations[to].owner,to,rating:'Light',pay:900};
      const t=(S.traders||[]).find(x=>x.kind==='haul'&&!x.esc);if(t)t.esc={k:me,hops:1,need:3,name:'Tester'};
      campHud();const txt=$('hOrd').hidden?'':$('hOrd').innerText;
      bmoAll().splice(bmoAll().findIndex(x=>x.id===99901),1);P.run=null;if(t)t.esc=null;campHud();const after=$('hOrd').hidden?'':$('hOrd').innerText;
      return JSON.stringify({empty,txt,after,esc:!!t})})()"""))
    t=r['txt']
    tl=t.lower()
    check('a contract, a black-market run and an escort each show on the HUD in flight','spy on' in tl and 'run' in tl and 'into' in tl and (not r['esc'] or 'escort' in tl),r)
    check('they leave the card when they end','spy on' not in r['after'].lower() and 'into' not in r['after'].lower(),r)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
