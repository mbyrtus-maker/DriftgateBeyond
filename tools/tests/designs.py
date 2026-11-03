# Beyond stage 6: the powers' own fighter designs. Each power's three fighters use their own model and stats (not the flat
# trait); AI ships fly their power's designs; freeport yards roll a mix of designs; buying a fighter takes the yard's design
# (your design line follows it) and its slot layout (the Fang's extra weapon slot), with the ledger exact
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
    print('models',await ev("JSON.stringify(FAC_IDS.map(f=>['interceptor','striker','heavy'].map(c=>designOf(f,c).name+':'+(mdlHas(designOf(f,c).m)&&shipMesh(f,c).mdl?'ok':'missing')).join(' ')))"))
    print('light stats',await ev("JSON.stringify(Object.fromEntries(FAC_IDS.map(f=>{const s=shipStats(f,'interceptor',1);return[designOf(f,'interceptor').name,{hull:Math.round(s.hull),shield:Math.round(s.sCap),energy:Math.round(s.eCap),speed:Math.round(s.maxSpd),turn:+s.turn.toFixed(2),r:Math.round(s.radius),slots:slotsOf('interceptor',f).w.length}]})))"))
    print('undesigned class keeps the trait',await ev("JSON.stringify({halcyonMinerShield:Math.round(shipStats('halcyon','skiff',1).sCap),varkeshMinerShield:Math.round(shipStats('varkesh','skiff',1).sCap)})"))
    print('freeport yards',await ev("(()=>{yardRoll();return JSON.stringify(Object.fromEntries(Object.entries(S.yardRoll).map(([k,v])=>[k,v])))})()"))
    # buy a Medium Fighter at this freeport: the yard's design and its slots; the fitted parts move across, the ledger stays exact
    print('buy',await ev("""(()=>{const P=S.player,c=dockCtx(),f=yardDesign(c,'striker'),f0=P.faction;P.rp=5000;devLedger(()=>{P.credits+=20000});dockAction('hull','striker');
      return JSON.stringify({yard:f,before:f0,after:P.faction,cls:P.cls,msg:dockErr,fit:fitOf(P),design:W.player.st.design})})()"""))
    print('ledger',await ev(LED))
    print('fang slots',await ev("""(()=>{const P=S.player;devLedger(()=>{P.credits+=20000});const c={kind:'station',owner:'varkesh'};P.faction='varkesh';P.cls='interceptor';const F=fitOf(P);refreshPlayerStats();return JSON.stringify({w:F.w,d:F.d,design:W.player.st.design})})()"""))
    print('ledger',await ev(LED))
    print('ship tab',await ev("(()=>{dockTab='ship';renderDock();const t=document.querySelector('#dBody').innerText;const i=t.search(/ design/i);return i>=0?t.slice(Math.max(0,i-60),i+40).replace(/\\n/g,' | '):'no design label'})()"))
    print('ai design',await ev("(()=>{const e=makeNPC('patrol','ostrova','heavy',1,{},null);return JSON.stringify({design:e.st.design,mesh:shipMesh(e.fac||e.side,e.cls).mdl})})()"))
    await ev("(()=>{undock();return 1})()");await pg.wait_for_timeout(40000)
    print('after flight',await ev("JSON.stringify({T:Math.round(S.T)})"),await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
