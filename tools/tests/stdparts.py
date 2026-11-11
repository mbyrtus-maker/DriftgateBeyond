# Beyond, standard parts and systems at every station (9 Nov 2026): every power's and freeport's market (Mirrorwater
# included) starts with standard parts of every kind and standard grade 1 systems; they show on the Market; bought, the
# station builds a replacement from its own store; the ledger stays exact; depots built during the game fill from their own store or their power's warehouse
import asyncio,json
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.join(' ')||'exact'})()"""
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
    r=json.loads(await ev("""(()=>{running=false;const W0=stdWant(),miss=[];for(const R of mkStations()){const st=mkStock(R);for(const id in W0)if((st[id]||0)<1)miss.push(R.sid+':'+id)}return JSON.stringify({n:mkStations().length,kinds:Object.keys(W0).length,miss:miss.slice(0,8),nm:miss.length})})()"""))
    check("every power's and freeport's market starts with every standard part and standard system",r['nm']==0 and r['kinds']>=20,r)
    r=json.loads(await ev("""(()=>{const out={},bad=[];for(const R of mkStations()){const st=mkStock(R);for(const f of stdBcAt(R))if((st['bc_'+f]||0)<2)bad.push(R.sid+':'+f)}
      const P=S.player;exitSector();W=null;P.sector='mw';enterSector('mw');running=false;P.docked='station';const c=dockCtx(),st=c.market,n0=st.bc_varkesh||0,pl=st.plate||0;devLedger(()=>{P.credits+=5000});dockAction('buyfb','varkesh');
      mkFilter='p_util';const h=mkHtml(c,P);return JSON.stringify({bad:bad.slice(0,6),nb:bad.length,took:n0-(st.bc_varkesh||0),plate:pl-(st.plate||0),msg:dockErr,shown:(h.match(/data-act="buyfb"/g)||[]).length})})()"""))
    check('every station starts with 2 Control Markers for each power it sells for; a purchase comes off the shelf',r['nb']==0 and r['took']==1 and r['plate']==0 and r['shown']>=3,r)
    r=json.loads(await ev("""(()=>{const P=S.player;exitSector();W=null;P.sector='mw';enterSector('mw');running=false;P.docked='station';const c=dockCtx(),st=c.market;const id=rdGid('sy_engine',1);mkFilter=mkGroup(id);mkView='tiles';const h=mkHtml(c,P),n0=st[id]||0;devLedger(()=>{P.credits+=20000});const want=stdWant()[id],nb=Math.max(1,n0-want+1);for(let i=0;i<nb;i++)dockAction('buy',id+':1');const bought=n0-(st[id]||0),low=st[id]||0;const src=storeOf(S.stations.mw);devLedger(()=>inv.addAll(src,ITEMS[id].recipe));S.stdT=0;stdTick();
      return JSON.stringify({shown:h.includes(ITEMS[id].name),bought,nb,low,back:st[id]||0,n0,want})})()"""))
    check('at Mirrorwater the standard drive is on the Market, sells, and the station builds another',r['shown'] and r['bought']==r['nb'] and r['back']==r['low']+1,r)
    r=json.loads(await ev("""(()=>{exitSector();W=null;S.player.docked=null;const st0=new Set(mkStations().map(R=>R.sid));let nb=0;const ob=stdBuild;stdBuild=function(){const r=ob.apply(this,arguments);if(r)nb++;return r};for(let i=0;i<720;i++){S.T+=10;strategicTick();updateEvents()}stdBuild=ob;const miss=[];let nk=0,have=0,nd=0;
      for(const R of mkStations()){const st=mkStock(R),W0=stdWantAt(R);if(st0.has(R.sid)&&R.kind!=='depot'){for(const id in W0)if((st[id]||0)<1)miss.push(R.sid+':'+id)}else if(!st0.has(R.sid)){nd++;for(const id in W0){nk++;if((st[id]||0)>0)have++}}}
      return JSON.stringify({nm:miss.length,miss:miss.slice(0,6),newDepots:nd,share:nk?have/nk:0,built:nb})})()"""))
    check('two hours on, the cores and freeports still have every standard part and system',r['nm']==0,r)
    check("with nothing sold, nothing is rebuilt in two hours, and depots built since keep an empty shelf (no drain on the powers' ore)",r['built']==0 and r['share']==0,r)
    l=await ev(LED);check('ledger exact',l=='exact',l)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
