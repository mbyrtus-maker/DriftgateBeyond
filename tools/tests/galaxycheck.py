# usage: python3 tools/tests/galaxycheck.py [page] [hours=4]
# Beyond, an end-to-end look at the galaxy's new work (9 Nov 2026, the user: "check to make sure all the new components
# parts are being made, stocked, delivered and the new missions work"). Runs a galaxy for some hours with no pilot taking
# work and reports, every hour: the makers' parts made and on the shelves, their freight (jobs posted, NPC freighters,
# deliveries), R&D (stages, trials, launches, failures), the kits a docked pilot finds at every market, the makers' ore
# requests and the Riftstone buyers, the independents' guard hires, CEO shuttles and the black-market contracts, and the
# ledger. It fails if any of those never happens.
import asyncio,json,os,sys
from playwright.async_api import async_playwright
GAME='file://'+os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html'))
HOURS=int(sys.argv[2]) if len(sys.argv)>2 else 4
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.join(' ')||'exact'})()"""
HOOKS="""(()=>{running=false;exitSector();W=null;S.player.docked='station';const C=window.__gc={fjPost:0,fjNpc:0,fjLand:0,oreq:0,rsj:0,hire:0,ceo:0,kill:0,ceoK:0,launch:0,fail:0,trial:0};
  {const o=mfjPost;mfjPost=function(){C.fjPost++;return o.apply(this,arguments)}}
  {const o=mfjLand;mfjLand=function(){C.fjLand++;return o.apply(this,arguments)}}
  {const o=rdLaunch;rdLaunch=function(m){const c=ceOf(m),g=c&&c.rd&&c.rd.g;const r=o.apply(this,arguments);if(c&&!c.rd&&g)C.launch++;else if(c&&c.rd&&c.rd.fails)C.fail++;return r}}
  {const o=rdFlyStart;rdFlyStart=function(){C.trial++;return o.apply(this,arguments)}}
  {const o=ceoLaunch;ceoLaunch=function(){const t=o.apply(this,arguments);if(t)C.ceo++;return t}}
  return 1})()"""
STEP="""(()=>{const C=window.__gc;const seen=window.__gs=window.__gs||{oq:new Set(),rs:new Set(),hire:new Set(),bk:new Set(),npc:new Set()};
  for(let i=0;i<360;i++){S.T+=10;strategicTick();updateEvents();for(const j of oreqAll())seen.oq.add(j.id);for(const j of rsjAll())seen.rs.add(j.id);for(const I of indAll())if(I.hire)seen.hire.add(I.id+':'+I.hire.T);for(const x of bmoAll())seen.bk.add(x.k+':'+x.id);for(const t of S.traders||[])if(t.syf)seen.npc.add(t.id)}
  // parts made and stocked: makers' items on every market
  let shelf=0,kinds=new Set(),g2=0;for(const sid in S.stations){const R=S.stations[sid];let st;try{st=mkStock(R)}catch(e){continue}for(const k in st){const I=ITEMS[k];if(I&&I.maker&&st[k]>0){shelf+=st[k];kinds.add(I.sys||I.part);if((I.grade||1)>1)g2+=st[k]}}}
  let sold=0;for(const m in MAKERS){const c=ceOf(m);if(c)sold+=(c.sales||[]).filter(x=>x[0]>S.T-3600).reduce((a,x)=>a+x[2],0)}
  const rd={};for(const m in MAKERS){const c=ceOf(m);if(c&&c.rd)rd[c.rd.stage]=(rd[c.rd.stage]||0)+1}
  // kits: dock at every market for a moment
  let kitOK=0,kitN=0;for(const R of mkStations()){kitN++;const P=S.player,sv=P.sector;P.sector=R.sid;P.docked='station';kitTick();const st=storeOf(R);if(KIT_IDS.every(k=>(st[k]||0)>=1))kitOK++;P.docked=null;kitTick();P.sector=sv}P.docked='station';
  const dead=Object.keys(MAKERS).filter(m=>{const c=ceOf(m);return!c||c.dead}).length;
  return JSON.stringify({h:Math.round(S.T/3600*10)/10,shelf,kinds:kinds.size,g2,sold1h:sold,rd,launch:C.launch,trial:C.trial,fail:C.fail,dead,fjPost:C.fjPost,npcFreighters:seen.npc.size,fjLand:C.fjLand,kits:kitOK+'/'+kitN,oreq:seen.oq.size,oreqOpen:oreqAll().length,rsj:seen.rs.size,rsjOpen:rsjAll().length,hires:seen.hire.size,ceoFlights:C.ceo,contracts:[...seen.bk].reduce((o,x)=>{const k=x.split(':')[0];o[k]=(o[k]||0)+1;return o},{}),drift:Object.fromEntries(RAWS.map(e=>[e,Math.round(S.drift[e]||0)]))})})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await ev(HOOKS);last=None
    for h in range(HOURS):
      last=json.loads(await ev(STEP));print('hour',json.dumps(last),flush=True)
    led=await ev(LED);print('ledger',led)
    bad=[]
    def need(name,ok):
      print(('ok   ' if ok else 'FAIL ')+name)
      if not ok:bad.append(name)
    need('makers\' parts on the shelves, in several kinds',last['shelf']>0 and last['kinds']>=5)
    need('makers\' parts selling',last['sold1h']>0)
    need('R&D trials flown and lines launched',last['trial']>0 and last['launch']>0)
    need('graded (G2+) parts on the shelves',last['g2']>0)
    need('freight jobs posted, NPC freighters flying, deliveries landing',last['fjPost']>0 and last['npcFreighters']>0 and last['fjLand']>0)
    need('every market has all three kits for a docked pilot',last['kits'].split('/')[0]==last['kits'].split('/')[1])
    need('makers\' ore requests posted',last['oreq']>0)
    need('Riftstone buyers posted',last['rsj']>0)
    need('independent miners hire guards',last['hires']>0)
    need('CEO shuttles fly and black-market contracts are posted',last['ceoFlights']>0 and last['contracts'].get('ceo',0)>0)
    need('ledger exact',led=='exact')
    need('no page errors',not errs)
    if errs:print(errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
