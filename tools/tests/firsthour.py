# Beyond, the first hour for every pilot (11 Nov 2026): the starter ship arrives armed (no rearm bill on arrival); the dock's
# Overview names a next step where "Ready now" had nothing, and its button opens that job; the Jobs board shows one row per
# target with a power picker; the Shipyard marks the hull you fly as current; the ledger stays exact
import asyncio,json,os
from playwright.async_api import async_playwright
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="(()=>{const L=ledger();for(const e of RAWS)if(Math.abs(L.tot[e]-S.ledger0.tot[e])>1e-6)return 'ore '+e;return Math.abs(L.credits-S.ledger0.credits)<1e-6?'exact':'credits '+(L.credits-S.ledger0.credits)})()"
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1440,'height':900});errs=[];bad=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    def check(n,ok,d=''):
      print(('ok  ' if ok else 'FAIL'),n,str(d)[:300])
      if not ok:bad.append(n)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()")
    await pg.wait_for_function('__dg.ev("!!(S&&S.player)")',timeout=60000);await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    r=json.loads(await ev("""(()=>{const P=S.player;return JSON.stringify({cr:P.credits,ammo:P.ammo,cap:ammoCap(P),feed:FEED.map(f=>f.msg||f.t||'').join('|').includes('Rearmed')})})()"""))
    check('a new pilot starts with a full gun and 1,800 cr: no rearm bill on arrival',r['cr']==1800 and r['ammo']==r['cap'] and not r['feed'],r)
    r=json.loads(await ev("""(()=>{$('dock').hidden=true;openDock('home');const n=document.querySelector('#dock .nstep'),b=n&&n.querySelector('button'),txt=n?n.innerText:'',empty=/Nothing waiting here\\. Your hold/.test($('dock').innerText);const arg=b&&b.dataset.arg,act=b&&b.dataset.act;if(b)b.click();
      return JSON.stringify({txt:txt.slice(0,160),empty,act,tab:dockTab,sel:jobSel===arg,onBoard:!!document.querySelector(`#dock [data-act=jsel][data-arg="${arg}"]`)})})()"""))
    check("the Overview shows a next step, a job for this ship, not 'Nothing waiting here'",('Next step' in r['txt'] or 'NEXT STEP' in r['txt']) and not r['empty'] and r['act']=='nsjob',r)
    check('its button opens the Jobs tab with that job selected',r['tab']=='jobs' and r['sel'] and r['onBoard'],r)
    r=json.loads(await ev("""(()=>{dockTab='jobs';jobFilter='all';renderDock();const rows=[...document.querySelectorAll('#dock [data-act=jsel]')].map(b=>b.querySelector('b').textContent.trim());const claims=rows.filter(t=>/^Claim /.test(t));
      const all=JOBS_LAST.filter(j=>String(j.id).startsWith('cl:'));const first=all[0];jobSel=first.id;renderDock();const pick=[...document.querySelectorAll('#dock [data-act=jpow]')];const other=pick.find(b=>b.getAttribute('aria-pressed')==='false');const oid=other&&other.dataset.arg;if(other)other.click();
      const title=document.querySelector('#dock .jdet2 .ldname b').textContent;const rows2=[...document.querySelectorAll('#dock [data-act=jsel]')].map(b=>b.querySelector('b').textContent.trim()).filter(t=>/^Claim /.test(t));
      return JSON.stringify({claims,nAll:all.length,dup:claims.length!==new Set(claims).size,forIn:claims.some(t=>/ for (Halcyon|Varkesh|Ostrova)$/.test(t)),picks:pick.length,switched:jobSel===oid,title,same:rows2.length===claims.length})})()"""))
    check('the Jobs board shows one row per claim target (three powers each), with no power in the row title',r['nAll']>=3 and len(r['claims'])*3==r['nAll'] and not r['dup'] and not r['forIn'],r)
    check('the detail panel picks the power, and the pick switches the job without adding rows',r['picks']==3 and r['switched'] and r['same'],r)
    r=json.loads(await ev("""(()=>{dockTab='ship';renderDock();const P=S.player;const mine=FAC(P.faction).hulls[P.cls];const cur=document.querySelector('#dBody .cls.on');const t=cur?cur.textContent:'';return JSON.stringify({mine,t:t.slice(0,120),ok:t.includes(mine)&&/current/.test(t)&&!/design · current/.test(t)})})()"""))
    check('the Shipyard marks the hull you fly as current, under its own name',r['ok'],r)
    l=await ev(LED);check('ledger exact',l=='exact',l)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
