# Beyond: Control Markers are fitted parts. Bought for a power at a freeport (the Market tiles list them, in the power's colour);
# fitted in a utility slot from the Loadout (only beacons you have; the Jobs board's Buy & fit buys one); refused on a miner; in the hold they don't claim,
# fitted they do; the claim uses the fitted beacon up and empties the slot; no grades; the ledger stays exact
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
    print('tiles',await ev("(()=>{transfer('halcyon','player',5000);$('dock').hidden=false;dockTab='market';mkFilter='bcn';renderDock();const t=$('dBody').innerText;const i=t.indexOf('CONTROL MARKERS');return t.slice(i,i+200).replace(/\\n/g,' | ')})()"))
    print('icon colour',await ev("JSON.stringify([giKind('bc_varkesh'),giCol('bc_varkesh'),FACTIONS.varkesh.col])"))
    print('buy',await ev("(()=>{mkFilter='bcn';renderDock();document.querySelector('[data-act=buyfb][data-arg=varkesh]').click();return $('dErr').textContent.slice(0,80)+' | hold '+(S.player.cargo.bc_varkesh||0)})()"))
    print('hold only',await ev("(()=>{const o={owner:null};return String(fbHeld(S.player,o))})()"))
    print('loadout',await ev("(()=>{dockTab='upg';ldSel='u:0';renderDock();const t=$('dBody').innerText;return JSON.stringify({fitRow:/Control Marker \\(Varkesh\\)/.test(t),buyFit:(t.match(/Buy & fit/gi)||[]).length})})()"))
    print('fit',await ev("(()=>{dockAction('fit','u:0:bc_varkesh');const F=fitOf(S.player);return dockErr.slice(0,90)+' | '+JSON.stringify({u:F.u,ui:F.ui,hold:S.player.cargo.bc_varkesh||0,pup:pupQuote(dockCtx(),S.player,'u:0')})})()"))
    print('buy & fit',await ev("(()=>{const c0=S.player.credits;dockAction('fit','u:0:bc_ostrova');const refused=dockErr.slice(0,40);dockAction('cbfit','ostrova:0');const F=fitOf(S.player);return 'loadout: '+refused+' · board: '+dockErr.slice(0,60)+' | '+JSON.stringify({ui:F.ui,paid:c0-S.player.credits,vault:S.player.vault.bc_varkesh||0})})()"))
    print('refit varkesh',await ev("(()=>{dockAction('fit','u:0:bc_varkesh');return dockErr.slice(0,70)+' | '+JSON.stringify(fitOf(S.player).ui)})()"))
    print('fitted claims',await ev("(()=>{return String(fbHeld(S.player,{owner:null}))+' / owned by varkesh: '+String(fbHeld(S.player,{owner:'varkesh'}))})()"))
    print('miner refused',await ev("(()=>{const P=S.player,c0=P.cls;P.cls='prospector';const r=fitDo(dockCtx(),P,'u:0:bc_halcyon');P.cls=c0;return r})()"))
    print('claim',await ev("""(()=>{const P=S.player;const o=Object.values(S.outposts).find(o=>!o.owner);if(!o)return 'no unclaimed outpost';const c0=P.credits;fbClaim(o,'varkesh','me');const F=fitOf(P);return JSON.stringify({owner:o.owner,u:F.u,ui:F.ui,paid:P.credits-c0,hold:P.cargo.bc_varkesh||0})})()"""))
    # the claim job on the board carries Buy & fit (user, 3 Nov 2026): clear the fit, open Jobs, press it
    print('board buy & fit',await ev("""(()=>{const P=S.player;dockAction('fit','u:0:');devLedger(()=>{for(const f of FAC_IDS){delete P.cargo['bc_'+f];delete P.vault['bc_'+f]}});dockTab='jobs';jobFilter='all';renderDock();
      const j=(JOBS_LAST||[]).find(x=>String(x.id).startsWith('cl:'));if(!j)return 'no claim job';jobSel=j.id;renderDock();const b=[...document.querySelectorAll('#dBody .jdet2 button,#dBody .codet button')].find(x=>/Buy & fit/.test(x.textContent));if(!b)return 'no button: '+JSON.stringify(j.btn2)+' direct '+JSON.stringify(jobsList(dockCtx(),P,[P.cargo,P.vault],true,false).filter(x=>String(x.id).startsWith('cl:')).map(x=>[x.id,x.btn2]))+' sold '+JSON.stringify(fbSold(dockCtx(),P))+' docked '+P.docked+' slot '+cbSlot(P)+' cls '+P.cls+' '+(document.querySelector('#dBody .jdet2')||{innerText:'no jdet2'}).innerText.slice(0,400);
      const f=j.id.split(':')[2],lab=b.textContent,c0=P.credits;b.click();return JSON.stringify({lab,fitted:cbFitted(P).map(x=>x.f),f,paid:c0-P.credits,err:dockErr.slice(0,80)})})()"""))
    print('ledger with the beacon fitted',await ev(LED))
    print('board after',await ev("(()=>{dockTab='jobs';renderDock();const j=(JOBS_LAST||[]).find(x=>String(x.id).startsWith('cl:'));return j?j.sub.replace(/<[^>]+>/g,''):'none'})()"))
    print('board in a miner',await ev("(()=>{const P=S.player,c=P.cls;P.cls='skiff';const L=jobsList(dockCtx(),P,[P.cargo,P.vault]).filter(x=>String(x.id).startsWith('cl:'));P.cls=c;return L.length?JSON.stringify({need:L[0].need,fix:L[0].fix&&L[0].fix[2]}):'none'})()"))
    print('ledger',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
