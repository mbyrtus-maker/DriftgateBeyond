import asyncio,json
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=await b.new_page();await pg.goto('file://'+__import__('os').path.abspath(__file__.rsplit('/',1)[0]+'/../../index.html')+'',timeout=400000);await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=400000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(6000)
    ev=lambda c:pg.evaluate("c=>__dg.ev(c)",c)
    r=await ev("""(()=>{const items={};for(const id in ITEMS){const I=ITEMS[id];if(!(id.startsWith('mp_')||I.part))continue;items[id]={name:I.name,part:I.part||id.split('_').slice(2).join('_'),maker:I.maker||(id.startsWith('mp_')?id.split('_')[1]:null),tr:I.tr||{},base:Math.round(baseValue(id)),comp:Math.round(Object.entries(I.recipe||{}).reduce((a,[k,n])=>a+baseValue(k)*n,0))}}
      const makers={};for(const m in MAKERS)makers[m]={name:MAKERS[m].name,home:MAKERS[m].home,sid:mkHomeSid(m),parts:Object.keys(MAKERS[m].parts)};
      const slots={};for(const c in HULL_SLOTS)slots[c]=HULL_SLOTS[c];
      const prices={};for(const sid in S.stations){const R=S.stations[sid];if(!R||!R.market&&!mkStock)continue;try{const st=mkStock(R);const L={};for(const id in st)if(items[id])L[id]=st[id];prices[sid]={owner:R.owner,kind:R.kind,stock:L}}catch(e){}}
      const corp=typeof CORP!=='undefined'?CORP:null;
      return JSON.stringify({items,makers,slots,stations:prices,corpSells:typeof corpSells==='function'?Object.fromEntries(Object.keys(MAKERS).map(m=>[m,(()=>{try{return corpSells(m)}catch(e){return String(e)}})()])):null,mkWorks:MK_WORKS,classes:Object.fromEntries(Object.entries(CLASSES).map(([k,c])=>[k,{name:c.name,cargo:c.cargo,drones:c.drones||0}]))})})()""")
    open(__file__.rsplit('/',1)[0]+'/data.json','w').write(r);d=json.loads(r)
    print(len(d['items']),'items',list(d['makers'])[:3],len(d['stations']),'stations');print(json.dumps(d['corpSells'])[:600])
    await b.close()
asyncio.run(main())
