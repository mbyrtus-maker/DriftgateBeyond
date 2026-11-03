# Beyond: the Black market tab. Contacts made by docking; requested runs; offers filtered by heat; a run given to a Compact
# contractor (broker's cut) and one to your AI crew (paid, then one caught: goods seized, heat on you); a contraband buy at a
# freeport, a quiet buyer and a fence at a power's station; the tab renders; the ledger stays exact
import asyncio,json
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    print('contacts',await ev("""(()=>{const P=S.player;const fp=Object.keys(S.stations).find(s=>S.stations[s].owner==='neutral');exitSector();P.sector=fp;P.docked=null;enterSector(fp);P.docked='station';openDock();window._FP=fp;
      const a=bmRequest(P,'buy'),b=bmRequest(P,'fix'),c=bmRequest(P,'fix');return JSON.stringify({met:Object.keys(P.bmMet),noBuyer:a,fix:b,again:c,offers:bmOffers(P).length})})()"""))
    print('filter',await ev("""(()=>{const P=S.player;bmFilter='Severe';const n=bmOffers(P).filter(x=>x.rating==='Severe').length;coTab='bm';$('company').hidden=false;renderCompany();const rows=document.querySelectorAll('#coBody .corow').length;bmFilter='all';return JSON.stringify({severe:n,rows})})()"""))
    print('contractor',await ev("""(()=>{const P=S.player;let x=bmOffers(P).find(y=>!y.kind);if(!x){P.bmReqT=0;bmRequest(P,'fix');x=bmOffers(P).find(y=>!y.kind)}if(!x)return 'no run';const c0=P.credits;const m=bmAssign(P,x.id,'hire');const r=S.bmRuns[S.bmRuns.length-1];r.caught=false;S.T=r.eta+1;bmRunTick();return JSON.stringify({m,state:r.state,cut:P.credits-c0,pay:r.x.pay})})()"""))
    print('ledger',await ev(LED))
    print('crew run',await ev("""(()=>{const P=S.player;undock();P.rp=5000;const sid=SECTOR_DEFS.map(d=>d.id).find(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id]);exitSector();P.sector=sid;P.docked=null;enterSector(sid);P.cls='bulker';fitOf(P);refreshPlayerStats();devLedger(()=>{P.cargo={frame:2}});depFresh(P);const R=S.stations[sid];
      R.crew=[{id:S.nextId++,name:'Vex',cls:'freighter',job:'idle',laid:false,hired:S.T}];const fp=window._FP;exitSector();P.sector=fp;enterSector(fp);P.docked='station';openDock();
      const out=[];for(const caught of[false,true]){P.bmReqT=0;let x=null;for(let i=0;i<8&&!x;i++){bmRun(fp);x=bmOffers(P).find(y=>!y.kind&&y.from===fp&&mass(y.item)*y.n<=CLASSES.freighter.cargo)}if(!x){out.push('no run');continue}
        const c0=P.credits,h0=heatOf(x.f,P),cr=R.crew[0];const m=bmAssign(P,x.id,String(cr.id));const r=S.bmRuns[S.bmRuns.length-1];const away=cr.job;r.caught=caught;S.T=r.eta+1;bmRunTick();out.push({m:m.slice(0,60),away,back:cr.job,state:r.state,paid:P.credits-c0,heat:[h0,heatOf(x.f,P)]})}return JSON.stringify(out)})()"""))
    print('ledger',await ev(LED))
    print('contraband buy',await ev("""(()=>{const P=S.player,fp=window._FP,R=S.stations[fp];P.cls='freighter';fitOf(P);refreshPlayerStats();devLedger(()=>{inv.add(mkStock(R),'rift',6);P.cargo={}});const x=bmBuy(fp);if(!x)return 'none';transfer('halcyon','player',5000);const c0=P.credits;const m=bmDeal(P,x.id);return JSON.stringify({m,paid:c0-P.credits,cargo:P.cargo})})()"""))
    print('ledger',await ev(LED))
    print('quiet buyer and fence',await ev("""(()=>{const P=S.player;const st=Object.keys(S.stations).find(s=>S.stations[s].owner==='varkesh'&&S.stations[s].kind==='core');exitSector();P.sector=st;enterSector(st);P.docked='station';openDock();
      let q=null;for(let i=0;i<30&&!(q&&q.kind==='sell');i++)q=bmSell(st);let f=null;for(let i=0;i<30&&!(f&&f.kind==='fence');i++)f=bmSell(st);
      devLedger(()=>{inv.add(P.cargo,q.item,q.n);inv.add(P.cargo,f.item,f.n)});stolAdd(P,f.item,f.f,f.n);const c0=P.credits;const a=bmDeal(P,q.id),c1=P.credits,b=bmDeal(P,f.id);
      return JSON.stringify({quiet:[q.rating,a,c1-c0],fence:[f.rating,b,P.credits-c1],tags:P.stol&&P.stol[f.item]})})()"""))
    print('ledger',await ev(LED))
    print('tab',await ev("(()=>{coTab='bm';$('company').hidden=false;renderCompany();return $('coBody').innerText.slice(0,400).replace(/\\n/g,' | ')})()"))
    await pg.wait_for_timeout(10000)
    print('after flight',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
