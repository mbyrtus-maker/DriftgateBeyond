# The corporate soak with independent pilots: AI-only galaxies (strategic ticks only, no live system, the player an idle
# contractor at a freeport) for HOURS each, several pages at once. Reports per galaxy and pooled: each maker's treasury
# against its start, failures, the powers' and the Compact's treasuries, the independents (population, purses, Ratings,
# hulls, what they earned and spent) and the ledger.
# usage: python3 tools/indsoak.py FILE [GALAXIES=4] [HOURS=4] [WORKERS=2] [TUNE_JS|-] [OUT.json]
#   OFF=1 runs the same galaxies without independents (a baseline).  Wrap in flock /tmp/dgbeyond-browser.lock.
import asyncio,json,sys,os,statistics
from playwright.async_api import async_playwright
FILE=os.path.abspath(sys.argv[1]);G=int(sys.argv[2]) if len(sys.argv)>2 else 4;H=float(sys.argv[3]) if len(sys.argv)>3 else 4
WK=int(sys.argv[4]) if len(sys.argv)>4 else 2;TUNE=open(sys.argv[5]).read() if len(sys.argv)>5 and sys.argv[5] not in('','-') else ''
OUT=sys.argv[6] if len(sys.argv)>6 else None;OFF=os.environ.get('OFF')=='1'
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
START="""(()=>{running=false;exitSector();W=null;if(%s){IND.cap=0;for(const I of indL().slice())indRetire(I,'baseline')}
  window._s0={mk:Object.fromEntries(Object.keys(MAKERS).map(m=>[m,ceT(m)])),tr:Object.fromEntries([...FAC_IDS,'neutral'].map(f=>[f,S.econ.treasury[f]||0]))};return 1})()"""%('true' if OFF else 'false')
CHUNK="""(n=>{for(let i=0;i<n;i++){S.T+=10;strategicTick();updateEvents()}return S.T})"""
REPORT="""(()=>{const L=indL(),t=(S.ind&&S.ind.tot)||{};return JSON.stringify({T:Math.round(S.T/60),mk:Object.fromEntries(Object.keys(MAKERS).map(m=>[m,Math.round(ceT(m)-_s0.mk[m])])),
  fails:Object.values(S.corp).reduce((a,c)=>a+((c.gen||1)-1)+(c.dead?1:0),0),dead:Object.keys(S.corp).filter(m=>S.corp[m].dead),
  tr:Object.fromEntries([...FAC_IDS,'neutral'].map(f=>[f,Math.round((S.econ.treasury[f]||0)-_s0.tr[f])])),stk:Object.fromEntries(FAC_IDS.map(f=>[f,['plate','wire','coil'].map(k=>(S.econ.stock[f]||{})[k]||0).join('/')])),
  ind:{n:L.length,ever:(S.ind&&S.ind.n||1)-1,purse:Math.round(L.reduce((a,I)=>a+indPurse(I),0)),rating:L.map(I=>ratingOf(I)).join(''),cls:L.map(I=>I.cls).join(','),jobs:L.reduce((a,I)=>a+(I.jobs||0),0),lost:L.reduce((a,I)=>a+(I.lost||0),0),
    parts:Math.round(t.parts||0),nparts:t.nparts||0,tradeProfit:Math.round((t.sell||0)-(t.buy||0)),fpreq:Math.round(t.fpreq||0),blk:Math.round(t.blk||0),sup:Math.round(t.sup||0)},
  won:S.won||null})})()"""
async def worker(b,jobs,res,wid):
  while jobs:
    gi=jobs.pop(0);pg=await b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
    try:
      await pg.goto('file://'+FILE+'?name=Tester',timeout=180000,wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=90000)
      await pg.evaluate('c=>__dg.ev(c)',"LEADT.mode='neutral';1")
      if TUNE:await pg.evaluate('c=>__dg.ev(c)',TUNE+';1')
      await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1000)
      ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
      await ev(START);hrs=[]
      while True:
        T=await ev(CHUNK+"(60)")
        if T%3600<10:hrs.append(json.loads(await ev(REPORT)))
        if T>=H*3600:break
      r=json.loads(await ev(REPORT));r['led']=await ev(LED);r['hours']=[{'T':x['T'],'mk':x['mk'],'tr':x['tr']} for x in hrs];r['errs']=errs[:4];res.append(r)
      print(f"galaxy {gi}: makers {r['mk']} fails {r['fails']} tr {r['tr']} ind {r['ind']} ledger {r['led']} errs {errs[:2]}",flush=True)
    except Exception as e:print('galaxy',gi,'FAILED',str(e)[:300],flush=True)
    await pg.close()
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);res=[];jobs=list(range(G))
    await asyncio.gather(*[worker(b,jobs,res,i) for i in range(WK)]);await b.close()
  if not res:return
  ds=[v for r in res for v in r['mk'].values()];inb=sum(1 for v in ds if abs(v)<=1000)
  print(f"\n{len(res)} galaxies x {H} h{' (baseline, no independents)' if OFF else ''}")
  print(f"makers within +-1,000 cr of start: {inb}/{len(ds)} ({round(100*inb/len(ds))}%); median {statistics.median(ds):+.0f}, mean {statistics.mean(ds):+.0f}, min {min(ds):+.0f}, max {max(ds):+.0f}")
  print(f"failures a galaxy: {[r['fails'] for r in res]} (mean {statistics.mean([r['fails'] for r in res]):.2f})")
  for f in ['halcyon','varkesh','ostrova','neutral']:print(f"  treasury {f}: mean {statistics.mean([r['tr'][f] for r in res]):+.0f}")
  for f in ['halcyon','varkesh','ostrova']:print(f"  stock plate/wire/coil {f}: {[r['stk'][f] for r in res]}")
  if not OFF:
    for k in ['n','purse','jobs','lost','parts','nparts','tradeProfit','fpreq','blk','sup']:print(f"  independents {k}: mean {statistics.mean([r['ind'][k] for r in res]):.0f}")
  print('ledgers',[r['led'] for r in res])
  if OUT:json.dump(res,open(OUT,'w'))
asyncio.run(main())
