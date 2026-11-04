# Beyond: Scrapheart's tabs and letters of marque (3 Nov 2026). Docked at Scrapheart the tabs read Overview, Plunder, Tavern,
# Ship, Marques; Plunder has a Black market tab and the Tavern lists black-market offers; the Tavern's convoy raids reach
# five jumps; taking a power's flag makes its ships friends, its war enemies
# and the Brood hostile, the Unbound neutral, its enemies' stations shut; the sponsor pays the bounty for a war enemy's
# ship; striking the flag ends it; falling Hostile with the sponsor revokes it; the ledger stays exact
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
    print('at the Wrack',await ev("""(()=>{const P=S.player;undock();relInit();exitSector();P.sector='wr';P.docked=null;enterSector('wr');P.docked='station';openDock('home');renderDock();return [...document.querySelectorAll('#dTabs .mtab')].map(b=>b.textContent.replace(/\\d/g,'').trim()).join(' | ')})()"""))
    print('tavern raids',await ev("""(()=>{const P=S.player;const far=SECTOR_DEFS.map(d=>d.id).find(id=>HOP.wr[id]===5&&id!==FAC_HOME('halcyon')),far6=SECTOR_DEFS.map(d=>d.id).find(id=>HOP.wr[id]===6&&id!==FAC_HOME('halcyon'));let t=null,t6=null;devLedger(()=>{t=haulSend('halcyon',far,FAC_HOME('halcyon'),{plate:5},'mq1','supplies');if(far6)t6=haulSend('halcyon',far6,FAC_HOME('halcyon'),{plate:5},'mq2','supplies')});
      const J=jobsList(dockCtx(),P,[P.cargo,P.vault]);return JSON.stringify({five:far,listed:J.some(j=>j.id==='cv:'+t.id),six:far6||null,sixListed:t6?J.some(j=>j.id==='cv:'+t6.id):null,pay:(J.find(j=>j.id==='cv:'+t.id)||{}).pay})})()"""))
    print('black market',await ev("""(()=>{const P=S.player;P.bmMet=P.bmMet||{};P.bmMet[P.home]=1;P.bmMet.wr=1;for(let i=0;i<40;i++){try{fixerTick()}catch(e){}}dockTab='bmk';renderDock();const t=document.getElementById('dBody').innerText;const subs=[...document.querySelectorAll('#dTabs button')].map(b=>b.textContent.trim()).filter(Boolean).join(' | ');
      const J=jobsList(dockCtx(),P,[P.cargo,P.vault]).filter(j=>String(j.id).startsWith('bmo:')||String(j.id).startsWith('bmr:'));return JSON.stringify({subtabs:subs.slice(0,200),body:t.slice(0,160).split(String.fromCharCode(10)).join(' | '),tavern:J.length,offers:bmOffers(P).length})})()"""))
    if os.environ.get('DG_SHOT'):await pg.screenshot(path=os.environ['DG_SHOT'])
    print('black market click',await ev("""(()=>{const b=document.querySelector('#dBody [data-co]');if(!b)return 'no buttons';const a=b.dataset.co;b.click();return a+' -> '+dockTab+' '+(dockErr||'').slice(0,60)})()"""))
    print('marques tab',await ev("(()=>{dockTab='allegiance';renderDock();const t=document.getElementById('dBody').innerText;const i=t.indexOf('LETTERS OF MARQUE');return t.slice(i,i+300).replace(/\\n/g,' | ')})()"))
    print('take Varkesh',await ev("""(()=>{const P=S.player;P.stand.varkesh=10;const pr=pairOf('varkesh','ostrova');if(!pr.war)evWar('varkesh','ostrova');dockAction('marque','varkesh');
      return dockErr+' || '+JSON.stringify({marque:P.marque,varkesh:pilotHostile(P,'varkesh'),ostrova:pilotHostile(P,'ostrova'),brood:pilotHostile(P,'brood'),pirate:pilotHostile(P,'pirate'),dockOstrova:tradeOK(P,'ostrova'),dockVarkesh:tradeOK(P,'varkesh'),payOstrova:bountyPayer('ostrova',P),payBrood:bountyPayer('brood',P)})})()"""))
    print('bounty paid',await ev("""(()=>{const P=S.player,c0=P.credits,t0=S.econ.treasury.varkesh;payKill({side:'ostrova',role:'patrol',cls:'interceptor',tier:1,dmg:{me:100}},'player',null);return JSON.stringify({got:P.credits-c0,fromVarkesh:t0-S.econ.treasury.varkesh})})()"""))
    print('hud',await ev("(()=>{hudUpdate();return $('hSub').textContent})()"))
    print('strike',await ev("(()=>{const P=S.player;dockAction('marque','varkesh');return dockErr+' | '+P.marque})()"))
    print('revoked',await ev("(()=>{const P=S.player;dockAction('marque','varkesh');standAdd('varkesh',-80,'test',P);return String(P.marque)})()"))
    print('ledger',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
