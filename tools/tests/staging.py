# Beyond (6 Nov 2026): the Varkesh foundries and forward staging. Varkesh's warehouse smelts down to a 40-ore reserve; a
# Varkesh depot smelts plate and conduit from its own ore without a production module; a power ships a staging stock to its
# forward depot by convoy; an offensive whose force the staging stock can field launches from there; the ledger stays exact
import asyncio,json
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
RUN="""((pred,max)=>{for(let i=0;i<max;i++){if(pred())return i;S.T+=10;tradersTick();raidsTick();updateEvents()}return -1})"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await ev("window.RUN="+RUN+";VF.on=true;STG.on=true;(()=>{exitSector();W=null;running=false;return 1})()")
    print('Varkesh smelts deeper',await ev("""(()=>{const st=S.econ.stock.varkesh,h=S.econ.stock.halcyon;let a,b;devLedger(()=>{st.fe=100;h.fe=100});const p0=st.plate||0,q0=h.plate||0;craftDown(st,'plate',{fe:80},400);craftDown(h,'plate',{fe:80},400);return JSON.stringify({varkeshPlate:(st.plate||0)-p0,varkeshFe:st.fe,halcyonPlate:(h.plate||0)-q0,halcyonFe:h.fe})})()"""))
    print('ledger',await ev(LED))
    print('a Varkesh depot smelts',await ev("""(()=>{const R=S.stations.vm,ds=dStore(R);devLedger(()=>{inv.add(ds,'fe',60);inv.add(ds,'cu',60)});const p0=ds.plate||0,w0=ds.wire||0;vfTick();return JSON.stringify({prod:devOf(R).prod||0,plate:(ds.plate||0)-p0,wire:(ds.wire||0)-w0})})()"""))
    print('ledger',await ev(LED))
    print('staging ships out',await ev("""(()=>{devLedger(()=>{for(const k in STG.kit)inv.add(S.econ.stock.halcyon,k,STG.kit[k]*2)});S.stg={};stgTick();const g=S.stg.halcyon;const t=g&&g.sid&&S.traders.find(x=>x.key==='stg:'+g.sid);const n=t?RUN(()=>!S.traders.includes(t),300):-2;const ds=g&&g.sid?dStore(S.stations[g.sid]):{};return JSON.stringify({front:g&&g.sid,convoy:!!t,arrived:n>=0,plate:ds.plate||0,torpedo:ds.torpedo||0})})()"""))
    print('ledger',await ev(LED))
    print('an offensive launches from the front',await ev("""(()=>{const g=S.stg.halcyon;if(!g||!g.sid)return 'no front';const R=S.stations[g.sid];const foes=SECTOR_DEFS.map(d=>d.id).filter(id=>{const o=sectorOwner(id);return o&&o!=='halcyon'&&hostile('halcyon',o)});const tgt=foes.sort((a,b)=>HOP[R.sid][a]-HOP[R.sid][b])[0];
      const force={};devLedger(()=>{});const cls=['striker','striker','interceptor','heavy'];for(const c of cls){const ld=loadout('patrol',1,c);takeFrom(ld,[S.econ.stock.halcyon]);inv.addAll(force,ld)}devLedger(()=>{for(const k in force)inv.add(dStore(R),k,force[k])});
      const ev={id:S.nextId++,type:'offensive',att:'halcyon',target:null,st:S.stations[tgt]?tgt:undefined,stName:'x',sector:tgt,eta:S.T+60,force,n:4,tier:1,cls,stage:'inbound'};if(!ev.st){const oid=OUT_BY_SECTOR[tgt];ev.target=oid}S.events.push(ev);updateEvents();const r=S.raids.find(x=>x.strike===ev.id);
      return JSON.stringify({staged:ev.staged,from:r&&r.src,home:FAC_HOME('halcyon'),hops:r?r.path.length-1:-1,homeHops:HOP[FAC_HOME('halcyon')][tgt]})})()"""))
    print('ledger',await ev(LED))
    print('map line',await ev("(()=>{const g=S.stg.halcyon;return g&&g.sid?mapSectorNow(g.sid).replace(/<[^>]+>/g,' ').replace(/\\s+/g,' ').slice(-70):'none'})()"))
    for i in range(3):await ev("(()=>{for(let i=0;i<30;i++){S.T+=10;strategicTick();updateEvents()}})()")
    print('an hour on',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
