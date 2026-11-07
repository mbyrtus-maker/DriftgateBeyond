# Beyond live space stage 4 (6 Nov 2026): goods go by hauler. No chance haulers; an outpost's surplus goes home by convoy; a
# depot's and an outpost's miners and garrison are kitted from what is there and ask the warehouse by convoy when short;
# plunder goes home by convoy; an aid shipment goes from one power's home to the other's; a convoy whose station is lost turns
# for home; the ledger stays exact throughout
import asyncio,json
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
RUN="""((pred,max)=>{for(let i=0;i<max;i++){if(pred())return i;S.T+=10;tradersTick()}return -1})"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await ev("window.RUN="+RUN+";1")
    print('no chance haulers',await ev("(()=>{const P=S.player;undock();exitSector();P.sector='hp';P.docked=null;enterSector('hp');const r=popWants().filter(w=>w[0]==='hauler').length+' '+W.ents.filter(e=>e.role==='hauler').length;exitSector();P.sector='mw';enterSector('mw');return r})()"))
    print('outpost surplus ships home',await ev("""(()=>{const o=S.outposts.kestrel;o.owner='halcyon';devLedger(()=>{inv.add(o.stock,'fe',70);inv.add(o.stock,'plate',40)});const h0=S.econ.stock.halcyon.fe||0;frOutpost('kestrel');const t=S.traders.find(x=>x.key==='op:kestrel');
      const n=RUN(()=>!S.traders.includes(t),400);return JSON.stringify({convoy:!!t,load:t&&t.load,left:o.stock.fe,plateKept:o.stock.plate,arrived:n>=0,home:(S.econ.stock.halcyon.fe||0)-h0})})()"""))
    print('ledger',await ev(LED))
    print('depot asks for kits',await ev("""(()=>{const R=S.stations.hr,ds=dStore(R);const ro=S.mrs['S.hr'];devLedger(()=>{const m=ro.m.pop();inv.addAll(S.econ.stock.halcyon,m.load)});const pl=ds.plate||0,wi=ds.wire||0;devLedger(()=>{inv.take(ds,'plate',pl);inv.take(ds,'wire',wi);inv.add(S.econ.stock.halcyon,'plate',pl);inv.add(S.econ.stock.halcyon,'wire',wi)});
      ro.t=S.T-1;mrTick();const t=S.traders.find(x=>x.key==='kit:hr');const n=RUN(()=>!S.traders.includes(t),400);ro.t=S.T-1;mrTick();return JSON.stringify({asked:!!t,load:t&&t.load,arrived:n>=0,roster:ro.m.length})})()"""))
    print('ledger',await ev(LED))
    print('outpost garrison by convoy',await ev("""(()=>{grTick();const ro=S.gar['O.kestrel'];const n0=ro?ro.m.length:0;const t=S.traders.find(x=>x.key==='okit:kestrel');const n=t?RUN(()=>!S.traders.includes(t),400):-2;if(ro)ro.t=S.T-1;grTick();return JSON.stringify({built0:n0,asked:!!t,okit:t&&t.okit,arrived:n>=0,after:ro&&ro.m.length,line:grLine('O.kestrel')})})()"""))
    print('ledger',await ev(LED))
    print('plunder goes home',await ev("""(()=>{const o=S.outposts.kestrel;devLedger(()=>{inv.add(o.stock,'cu',40)});const n0=S.traders.length;capture(o,'varkesh');const t=S.traders.find(x=>String(x.key).startsWith('plunder:'));return JSON.stringify({convoy:!!t,side:t&&t.side,to:t&&t.to,load:t&&t.load})})()"""))
    print('ledger',await ev(LED))
    print('aid between powers',await ev("""(()=>{devLedger(()=>{inv.add(S.econ.stock.halcyon,'plate',60);inv.add(S.econ.stock.halcyon,'wire',60)});const v0=S.econ.stock.varkesh.plate||0;evAid('halcyon','varkesh');const t=S.traders.find(x=>String(x.key).startsWith('aid:'));const n=t?RUN(()=>!S.traders.includes(t),400):-2;return JSON.stringify({convoy:!!t,intoF:t&&t.intoF,arrived:n>=0,varkeshGot:(S.econ.stock.varkesh.plate||0)-v0})})()"""))
    print('ledger',await ev(LED))
    print('lost station: turns home',await ev("""(()=>{const R=S.stations.hr;let t=null;devLedger(()=>{t=haulSend('halcyon','hp','hr',{plate:5},'test:1','supplies')});const own=R.owner;const n=RUN(()=>t.leg>=t.path.length-2,400);R.owner='varkesh';RUN(()=>!S.traders.includes(t),400);R.owner=own;const back=S.traders.find(x=>String(x.key).startsWith('back:'));return JSON.stringify({rerouted:!!back,to:back&&back.to})})()"""))
    print('ledger',await ev(LED))
    print('Brood outpost: a Gorger to the hive',await ev("""(()=>{const o=S.outposts.shoal;o.owner='brood';devLedger(()=>{inv.add(o.stock,'cu',70)});const h0=S.econ.stock.brood.cu||0;frOutpost('shoal');const t=S.traders.find(x=>x.key==='op:shoal');const n=RUN(()=>!S.traders.includes(t),400);return JSON.stringify({convoy:!!t,side:t&&t.side,cls:t&&hullName('brood',t.cls),to:t&&t.to,arrived:n>=0,hive:(S.econ.stock.brood.cu||0)-h0})})()"""))
    print('ledger',await ev(LED))
    print('Brood depot keeps its own store',await ev("""(()=>{const R=S.stations.hr;const own=R.owner;R.owner='brood';const same=storeOf(R)===dStore(R);devLedger(()=>{inv.add(dStore(R),'fe',60)});frBroodTick();const t=S.traders.find(x=>x.key==='bd:hr');R.owner=own;return JSON.stringify({own:same,convoy:!!t,to:t&&t.to,load:t&&t.load})})()"""))
    print('ledger',await ev(LED))
    for i in range(3):await ev("(()=>{for(let i=0;i<30;i++){S.T+=10;strategicTick();updateEvents()}})()")
    print('an hour on',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
