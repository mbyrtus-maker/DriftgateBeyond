import asyncio,json
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=await b.new_page();await pg.goto('file://'+__import__('os').path.abspath(__file__.rsplit('/',1)[0]+'/../../index.html')+'',timeout=400000);await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=400000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(6000)
    ev=lambda c:pg.evaluate("c=>__dg.ev(c)",c)
    r=await ev("""(()=>{const val=o=>Object.entries(o).reduce((a,[k,n])=>a+baseValue(k)*n,0);
      const raws={};for(const e of RAWS)raws[e]=baseValue(e);
      const ore=id=>{const c=comp(id);const o={};for(const e of RAWS)if(c[e])o[e]=+c[e].toFixed(3);return o};
      const items={};for(const id in ITEMS){const I=ITEMS[id];if(!(id.startsWith('mp_')||id.startsWith('mq_')||I.part))continue;items[id]={ore:ore(id),oreVal:Math.round(RAWS.reduce((a,e)=>a+comp(id)[e]*raws[e],0))}}
      const sys={};for(const s of SLOTS){if(s.id==='payload')continue;sys[s.id]={name:s.name,g:{}};for(let t=1;t<=5;t++){const ci=compInv(s.id,t);const v={fe:0,cu:0,ir:0,xc:0,au:0,nu:0};invVec(ci,v);sys[s.id].g[t]={comp:ci,cv:Math.round(val(ci)),ore:Object.fromEntries(Object.entries(v).filter(x=>x[1]).map(([k,n])=>[k,+n.toFixed(3)])),oreVal:Math.round(RAWS.reduce((a,e)=>a+v[e]*raws[e],0))}}}
      const comps={};for(const k of ['plate','wire','coil','lattice','core','matrix'])comps[k]=Math.round(baseValue(k));
      return JSON.stringify({raws,comps,items,sys,tune:{step:TUNE_STEP,cmb:TUNE_CMB}})})()""")
    open(__file__.rsplit('/',1)[0]+'/data2.json','w').write(r);d=json.loads(r);print(d['raws'],d['comps'],d['tune']);print(json.dumps(d['sys'])[:1500]);print(list(d['items'].items())[:3])
    await b.close()
asyncio.run(main())
