# Beyond: an audience with a power's leader (3 Nov 2026). Before declaring, the panel only explains; declared, you request an
# audience at a power's station and get an ETA; the leader's flagship flies there and docks; the audience opens for five
# minutes; requests cost standing and last a set time; a refusal costs nothing; open trade changes prices; the ledger stays exact
import asyncio,json,os
from playwright.async_api import async_playwright
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':900});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    # a Station and a declared faction (as declare.py does)
    print('station',await ev("""(()=>{const P=S.player;undock();relInit();P.rp=5000;const sid=SECTOR_DEFS.map(d=>d.id).find(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id]);exitSector();P.sector=sid;P.docked=null;enterSector(sid);P.cls='bulker';fitOf(P);refreshPlayerStats();devLedger(()=>{P.cargo={frame:2}});depFresh(P);const R=S.stations[sid];
      devLedger(()=>{inv.add(R.stock,'keel',1);inv.add(R.stock,'frame',2);inv.add(R.stock,'seal',1)});staUp(P,R);window._R=R;return sid})()"""))
    # dock at Varkesh's home station
    go="(()=>{const P=S.player,sid=FAC_HOME('varkesh');exitSector();P.sector=sid;enterSector(sid);P.docked='station';openDock('allegiance');dockTab='allegiance';renderDock();return 1})()"
    await ev(go)
    print('before declaring',await ev("(()=>{const t=document.getElementById('dBody').innerText;const i=t.indexOf('AUDIENCE');return t.slice(i,i+230).replace(/\\n/g,' | ')})()"))
    print('declare',await ev("(()=>{dockAction('declare');return S.player.decl&&S.player.decl.name})()"))
    await ev(go)
    print('request',await ev("(()=>{const P=S.player;P.stand.varkesh=40;dockAction('audreq','varkesh');return dockErr+' | '+JSON.stringify(P.aud.varkesh)+' | flagship in '+leaderOf('varkesh').ship.sid})()"))
    print('panel coming',await ev("(()=>{renderDock();const t=document.getElementById('dBody').innerText;const i=t.indexOf('AUDIENCE');return t.slice(i,i+260).replace(/\\n/g,' | ')})()"))
    # run the strategic clock until the leader docks
    print('arrives',await ev("""(()=>{const P=S.player,A=P.aud.varkesh,t0=S.T;let n=0;while(A.stage!=='here'&&n<400){S.T+=5;strategicTick();n++}return JSON.stringify({stage:A.stage,took:Math.round(S.T-t0),eta:Math.round(A.eta-t0),at:leaderOf('varkesh').ship.sid,feed:FEED.slice(-2).map(f=>f.msg)})})()"""))
    await ev(go)
    print('panel open',await ev("(()=>{const t=document.getElementById('dBody').innerText;const i=t.indexOf('AUDIENCE');return t.slice(i,i+700).replace(/\\n/g,' | ')})()"))
    # ask for open trade until granted (refusals are free); check prices move
    print('open trade',await ev("""(()=>{const P=S.player,c=dockCtx(),k='plate',b0=mBuy(c,k),s0=mSell(c,k),st0=standOf('varkesh',P);let tries=0,msg='';const L=leaderOf('varkesh');L.traits=['Mercantile','Patient'];
      while(!audDeal(P,'varkesh','trade')&&tries<20){P.aud.varkesh.cd={};dockAction('audask','varkesh:trade:');msg=dockErr;tries++}
      return JSON.stringify({msg,tries,deal:!!audDeal(P,'varkesh','trade'),buy:[b0,mBuy(c,k)],sell:[s0,mSell(c,k)],standing:[Math.round(st0),Math.round(standOf('varkesh',P))]})})()"""))
    print('refusal is free',await ev("""(()=>{const P=S.player,L=leaderOf('varkesh');L.traits=['Isolationist'];P.aud.varkesh.cd={};const s0=standOf('varkesh',P);dockAction('audask','varkesh:tpact:');return dockErr+' | standing change '+Math.round(standOf('varkesh',P)-s0)})()"""))
    print('aid',await ev("""(()=>{const P=S.player,L=leaderOf('varkesh');L.traits=['Loyal','Honourable'];P.aud.varkesh.cd={};devLedger(()=>{inv.add(S.econ.stock.varkesh,'plate',40);inv.add(S.econ.stock.varkesh,'wire',20);inv.add(S.econ.stock.varkesh,'coil',10)});const p0=_R.stock.plate||0;let m='';for(let i=0;i<20&&!/aid|agrees/.test(m);i++){P.aud.varkesh.cd={};dockAction('audask','varkesh:aid:');m=dockErr}return m+' | plate at your Station +'+((_R.stock.plate||0)-p0)})()"""))
    print('war on',await ev("""(()=>{const P=S.player,L=leaderOf('varkesh');L.traits=['Ambitious','Vengeful'];P.stand.varkesh=80;let m='';for(let i=0;i<30&&!pairOf('varkesh','ostrova').war;i++){P.aud.varkesh.cd={};dockAction('audask','varkesh:war:ostrova');m=dockErr}return m+' | war '+!!pairOf('varkesh','ostrova').war})()"""))
    print('ends',await ev("(()=>{const P=S.player,A=P.aud.varkesh;S.T=A.until+1;strategicTick();return A.stage+' · next in '+Math.round(A.next-S.T)+' s · deals '+P.deals.map(d=>d.k+':'+Math.round(d.until-S.T)).join(',')})()"))
    print('ledger',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
