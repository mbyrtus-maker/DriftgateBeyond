# Beyond: the cargo scanner. No scanner, no reading; fitted (or an Unbound hull) a target in range gives a rough reading at
# once and the exact manifest after the scan; out of range it pauses; a pilot's hidden container hides its share; a power's
# ship scanned in its own space adds heat; freeports stock the part; the ledger stays exact
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
    print('stock',await ev("JSON.stringify(Object.values(S.stations).filter(R=>R.owner==='neutral').map(R=>mkStock(R).pt_cscan||0))"))
    # a power's hauler beside us in that power's own space
    print('setup',await ev("""(()=>{const P=S.player;undock();const f='halcyon',sid=FAC_HOME(f);exitSector();P.sector=sid;P.docked=null;enterSector(sid);
      const e=spawnNPC('hauler',f,false);e.x=W.player.x+300;e.y=W.player.y;e.z=W.player.z;e.vx=e.vy=e.vz=0;window._E=e;W.tgt={kind:'ship',ref:e};return JSON.stringify({side:e.side,role:e.role,cargo:e.cargo,own:sectorOwner(sid)})})()"""))
    print('no scanner',await ev("(()=>{hudUpdate();return JSON.stringify({g:cscG(S.player),panel:/Cargo scan/.test($('hTgt').innerText)})})()"))
    print('fit',await ev("""(()=>{const P=S.player,F=fitOf(P);devLedger(()=>{F.u[0]='cscan';F.ui=F.ui||[];F.ui[0]='pt_cscan';F.ug[0]=1});return cscG(P)})()"""))
    print('rough',await ev("(()=>{_E.npcFled=1;hudUpdate();return $('hTgt').innerText.split('Cargo scan')[1].slice(0,140).replace(/\\n/g,' | ')})()"))
    h0=await ev("(S.player.heat||{}).halcyon||0")
    print('exact',await ev("(()=>{for(let i=0;i<12;i++){_E.x=W.player.x+300;_E.y=W.player.y;_E.z=W.player.z;W.tgt={kind:'ship',ref:_E};W.t+=.5;hudUpdate()}return JSON.stringify({done:_E._csc.done,txt:$('hTgt').innerText.split('Cargo scan')[1].slice(0,160).replace(/\\n/g,' | ')})})()"))
    print('heat',h0,'->',await ev("Math.round((S.player.heat||{}).halcyon||0)"))
    print('out of range',await ev("""(()=>{const e=spawnNPC('hauler','halcyon',false);e.x=W.player.x+5000;e.y=W.player.y;e.z=W.player.z;e.npcFled=1;W.tgt={kind:'ship',ref:e};hudUpdate();return $('hTgt').innerText.split('Cargo scan')[1].slice(0,80).replace(/\\n/g,' | ')})()"""))
    print('unbound hull',await ev("(()=>{const P=S.player,c=P.cls;P.cls='raider';const F=fitOf(P);const u=F.u[0];F.u[0]='land';const g=cscG(P);F.u[0]=u;P.cls=c;return g})()"))
    print('hidden',await ev("""(()=>{const P=S.player,T={isPlayer:true};const c0=P.cargo;devLedger(()=>{P.cargo={relic:2,fe:30}});const F=fitOf(P);const u=F.u.slice();F.u[1]=F.u[1]||'hide';F.u[1]='hide';F.ug[1]=1;const r=cscLoad(T);F.u=u;devLedger(()=>{P.cargo=c0});return JSON.stringify({hideCap:4,seen:r})})()"""))
    print('ledger',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
