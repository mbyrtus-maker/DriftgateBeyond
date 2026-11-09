# Beyond screens pass: the minimal Company screen. Holdings lists your bases and the picked one's detail (station buildings
# built from the panel, Send a guard on a threatened depot); every tab renders without errors in its simple and Full view;
# Jobs hires a pilot and posts a job from its forms, and changes a crew's job; Economy switches a good's trade at your
# market; Allegiance picks a pair of powers; Black market lists offers and assigns a run to a contractor; the ledger stays exact
import asyncio,json,os
from playwright.async_api import async_playwright
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    await pg.wait_for_function('window.__dg&&__dg.ev("!!(S&&S.player)")',timeout=30000);await pg.evaluate("__dg.ev('coDefault(S.player)')")  # a company profile (8 Nov 2026: no Depot without one)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    click=lambda sel:ev(f"(()=>{{const b=document.querySelector('#company {sel}');if(!b)return 'MISSING {sel}';b.click();return ($('coErr').textContent||'ok').slice(0,140)}})()")
    print('setup',await ev("""(()=>{const P=S.player;undock();P.rp=5000;transfer('halcyon','player',20000);const ids=SECTOR_DEFS.map(d=>d.id).filter(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id]);const a=ids[0],c=ids[1];
      for(const sid of[a,c]){exitSector();P.sector=sid;P.docked=null;enterSector(sid);devLedger(()=>{P.cargo={frame:2}});depFresh(P)}
      const R=S.stations[a];devLedger(()=>{inv.addAll(R.stock,{keel:1,frame:4,seal:1,plate:60,coil:8})});dockAction('staup',a);window._A=a;window._C=c;
      S.events.push({id:S.nextId++,type:'offensive',att:'varkesh',st:c,stName:'x',sector:c,eta:S.T+60,force:{},n:3,tier:1,cls:[],stage:'inbound'});
      $('company').hidden=false;coTab='holdings';renderCompany();return dockErr})()"""))
    print('rows',await ev("[...document.querySelectorAll('#coBody .corow')].map(b=>b.innerText.replace(/\\n/g,' ')).join(' / ')"))
    print('alerts',await ev("[...document.querySelectorAll('#coBody .coalert')].map(b=>b.innerText.replace(/\\n/g,' ')).join(' / ')"))
    print('pick station',await ev("(()=>{coClick('cosel','D:'+_A);return $('coBody').querySelector('.codet').innerText.slice(0,120).replace(/\\n/g,' | ')})()"))
    print('build',await click('[data-co=stabld][data-arg$=":yard"]'),await ev("JSON.stringify(S.stations[_A].bld)"))
    print('guard',await click('.coalert [data-co=hgguard]'))
    print('full holdings',await click('[data-co=cofull][data-arg=holdings]'),await ev("$('coBody').innerText.slice(0,80).replace(/\\n/g,' | ')"))
    await click('[data-co=cofull][data-arg=holdings]')
    for t in['allegiance','economy','crews','bm']:
      await ev(f"coClick('tab','{t}')");s=await ev("$('coBody').innerText.slice(0,90).replace(/\\n/g,' | ')")
      await click(f'[data-co=cofull][data-arg={t}]');f=await ev("$('coBody').innerText.slice(0,60).replace(/\\n/g,' | ')");await click(f'[data-co=cofull][data-arg={t}]')
      print('tab',t,'| simple:',s,'| full:',f)
    await ev("coClick('tab','crews')")
    print('hire form',await click('[data-co=copk][data-arg="crews:hire"]'))
    print('hire',await click('.codet [data-co=crewhire][data-arg$=":prospector"]'),await ev("(S.stations[_A].crew||[]).length+(S.stations[_C].crew||[]).length"))
    print('crew job',await ev("(()=>{const c=(S.stations[_A].crew||[])[0]||(S.stations[_C].crew||[])[0];if(!c)return 'none';const R=(S.stations[_A].crew||[]).includes(c)?_A:_C;coClick('copk','crews:c:'+R+':'+c.id);document.querySelector('#company .codet [data-co=crewjob][data-arg$=\":guard\"]').click();return c.job})()"))
    print('post form',await click('[data-co=copk][data-arg="crews:post"]'),await click('.codet [data-co=pjf][data-arg="kind:supply"]'),await click('.codet [data-co=pjf][data-arg="item:coil"]'))
    print('post',await click('.codet [data-co=pjpost]'),await ev("JSON.stringify(pjList().map(j=>[j.kind,j.item,j.state]))"))
    print('rows',await ev("[...document.querySelectorAll('#coBody .corow')].length"))
    await ev("coClick('tab','economy')")
    print('market',await ev("(()=>{coClick('copk','economy:'+_A);const b=document.querySelector('#company .codet [data-co=mkset][data-arg*=\":plate:sell\"]');if(!b)return'MISSING';b.click();return JSON.stringify(S.stations[_A].sell)})()"))
    await ev("coClick('tab','allegiance')")
    print('pair',await ev("(()=>{relAdd('halcyon','ostrova',-6,'a border clash');coClick('alpair','halcyon:ostrova');return $('coBody').querySelector('.codet').innerText.split(/WHAT MOVED/i)[1].slice(0,90).replace(/\\n/g,' | ')})()"))
    print('views',await ev("(()=>{const o=[];for(const v of['rel','chron','standing']){coClick('cov','allegiance:'+v);o.push($('coBody').querySelectorAll('.colist *').length)}return JSON.stringify(o)})()"))
    await ev("coClick('tab','bm')")
    print('offers',await ev("(()=>{const P=S.player;P.bmMet={};for(const s of Object.keys(S.stations))if(S.stations[s].owner==='neutral')P.bmMet[s]=1;for(let i=0;i<6;i++)bmRun(pick(Object.keys(P.bmMet)));renderCompany();return document.querySelectorAll('#coBody .corow').length})()"))
    print('assign',await ev("(()=>{const r=document.querySelector('#coBody .corow');if(!r)return'none';r.click();const b=document.querySelector('#company .codet [data-co=bmassign][data-arg$=\":hire\"]');if(!b)return'no hire button: '+$('coBody').querySelector('.codet').innerText.slice(0,80);b.click();return $('coErr').textContent.slice(0,100)})()"))
    print('runs',await ev("(()=>{coClick('cov','bm:runs');return [...document.querySelectorAll('#coBody .corow')].map(b=>b.innerText.replace(/\\n/g,' ')).join(' / ').slice(0,200)})()"))
    print('ledger',await ev(LED))
    await pg.wait_for_timeout(3000)
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
