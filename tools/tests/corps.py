# Beyond: every item has a maker. The makers' markets (power cores, freeports) sell no unbranded parts, and start with a random
# selection, mostly local makers' with some imports (basics always there at freeports and cores); each maker's line includes plain parts for the slots it covers; the works build them;
# components and payload show their maker in the Market detail; the ledger stays exact
import asyncio,json,os
from playwright.async_api import async_playwright
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    print('lines',await ev("JSON.stringify(Object.fromEntries(Object.keys(MK_LINE).map(m=>[m,MK_LINE[m].map(id=>ITEMS[id].name)])))"))
    print('unbranded on makers markets',await ev("JSON.stringify(Object.keys(S.stations).filter(s=>{const R=S.stations[s];return R.owner==='neutral'||(FAC_IDS.includes(R.owner)&&R.kind==='core')}).map(s=>[s,Object.keys(PART).filter(k=>(mkStock(S.stations[s])[PART[k]]||0)>0).length,Object.keys(mkStock(S.stations[s])).filter(k=>k.startsWith('mq_')).length]))"))
    print('markets at launch',await ev("(()=>{const o={};for(const sid in S.stations){const R=S.stations[sid],L=corpLocal(R);if(!L||sid===WRACK.sid)continue;const st=mkStock(R),ids=Object.keys(st).filter(k=>ITEMS[k]&&ITEMS[k].part&&st[k]>0),loc=ids.filter(k=>L.includes(ITEMS[k].maker)),makers=new Set(ids.map(k=>ITEMS[k].maker));o[sid]=`${R.kind}: ${ids.length} kinds, ${loc.length} local, makers ${makers.size}, basics missing ${CORP_SEED.basics.filter(b=>corpSells(R.owner==='neutral'?sid:R.owner).includes(b)&&!ids.some(k=>ITEMS[k].part===b)).join('/')||'none'}`}return JSON.stringify(o)})()"))
    print('works',await ev("(()=>{const R=S.stations[S.player.sector],st=mkStock(R),id=MK_LINE.qs.find(x=>x.startsWith('mq_'));devLedger(()=>{st[id]=0;inv.addAll(st,{plate:50,wire:50,coil:20})});for(let i=0;i<30;i++){S.mkT=0;makersTick()}return id+' '+(st[id]||0)})()"))
    print('labels',await ev("(()=>{$('dock').hidden=false;dockTab='market';const out=[];for(const k of['plate','coil','wire',MK_LINE.mwa[0],MK_LINE.qs.find(x=>x.startsWith('mq_'))]){mkSel=k;renderDock();const d=$('dBody').querySelector('.mkdet');out.push(k+': '+(d?d.innerText.split('\\n').slice(0,2).join(' / '):'-'))}return out.join(' || ')})()"))
    print('ledger',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
