# Beyond stage 9: Lairs and the Company screen. The Company screen opens (Allegiance, Holdings); a Lair can't go where there's
# a station; built from the hold beside a large rock (ledger exact), ready after its build time; docking at it, the stash
# (capacity by level, stolen tags come off), lying low (heat cools 3x), level 2 (workshop, forge, 400 t), one per system and
# four per pilot; a hostile power's scout finds it and its ships wear it down
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
    await ev("(()=>{undock();return 1})()")
    await pg.keyboard.press('Digit0');await pg.wait_for_timeout(300)
    print('company',await ev("(()=>{const el=$('company');return JSON.stringify({open:!el.hidden,tabs:[...document.querySelectorAll('#coTabs [data-arg]')].map(b=>b.dataset.arg),body:$('coBody').innerText.slice(0,160).replace(/\\n/g,' | ')})})()"))
    print('at the freeport',await ev("JSON.stringify(lairSpot(S.player).why)"))
    print('no materials',await ev("""(()=>{const P=S.player;const sid=SECTOR_DEFS.map(d=>d.id).find(id=>!S.stations[id]&&S.sectors[id].ast.some(a=>oreTotal(a)>=60&&!a.rift)&&!DEF[id].home);exitSector();P.sector=sid;P.docked=null;enterSector(sid);
      const a=S.sectors[sid].ast.filter(r=>oreTotal(r)>=60&&!r.rift)[0],e=W.player;e.x=a.x+astR(a)+200;e.y=a.y;e.z=a.z;window._SID=sid;return JSON.stringify({sid,why:lairSpot(P).why})})()"""))
    print('build',await ev("""(()=>{const P=S.player;P.cls='freighter';fitOf(P);refreshPlayerStats();devLedger(()=>{P.cargo={frame:1,plate:6}});const m=lairBuildB();const L=lairsOf(P)[0];return JSON.stringify({msg:m,lair:L&&{lvl:L.lvl,building:L.build>S.T,fort:L.fort},cargo:P.cargo})})()"""))
    print('ledger',await ev(LED))
    print('ready',await ev("""(()=>{const L=lairsOf(S.player)[0];S.T=L.build+1;lairWorldB(.1);return JSON.stringify({building:!!L.build,near:!!lairNear()||d3(L,W.player)})})()"""))
    print('one per system',await ev("""(()=>{devLedger(()=>{S.player.cargo={frame:1,plate:6}});return JSON.stringify(lairSpot(S.player).why)})()"""))
    print('dock',await ev("""(()=>{const L=lairsOf(S.player)[0];lairDock(L);const c=dockCtx();return JSON.stringify({docked:S.player.docked,sub:c.sub,fab:c.fab,forge:c.forge})})()"""))
    print('stash launders',await ev("""(()=>{const P=S.player;devLedger(()=>{P.cargo={ir:10}});stolAdd(P,'ir','varkesh',10);dockAction('mv','ir:in:all');stolSync(P);return JSON.stringify({msg:dockErr,stash:dockCtx().storage,tags:P.stol||{}})})()"""))
    print('taken out early',await ev("""(()=>{const P=S.player,L=dockCtx().lairRec;dockAction('mv','ir:out:1');const t=JSON.stringify(P.stol||{});dockAction('mv','ir:in:1');return JSON.stringify({out:t,batches:(L.lt||[]).map(b=>b.n+':'+Math.round(b.until-S.T))})})()"""))
    print('after the spell',await ev("""(()=>{const P=S.player,L=dockCtx().lairRec;S.T+=200;launderTick();dockAction('mv','ir:out:all');stolSync(P);return JSON.stringify({batches:(L.lt||[]).length,tags:P.stol||{},cargo:P.cargo.ir})})()"""))
    print('stash cap',await ev("""(()=>{const P=S.player;P.cls='bulker';fitOf(P);refreshPlayerStats();devLedger(()=>{P.cargo={fe:300}});dockAction('mv','fe:in:all');return JSON.stringify({msg:dockErr,stash:invMass(dockCtx().storage)})})()"""))
    print('lie low',await ev("""(()=>{const P=S.player;P.heat={varkesh:60};scanStep(100);const a=heatOf('varkesh');return JSON.stringify({after100s:Math.round(a),openSpace:60-SM.cool*100})})()"""))
    print('level 2',await ev("""(()=>{const P=S.player,L=lairsOf(P)[0];devLedger(()=>{inv.add(P.cargo,'frame',1);inv.add(P.cargo,'plate',10);inv.add(P.cargo,'coil',4)});dockAction('lairup',L.id);const c=dockCtx();dockAction('mv','fe:in:all');return JSON.stringify({msg:dockErr,lvl:L.lvl,fab:c.fab,forge:c.forge,stash:invMass(c.storage),cap:lairStash(L)})})()"""))
    print('ledger',await ev(LED))
    print('rearm here',await ev("""(()=>{const P=S.player;P.ammo=0;const c0=P.credits,t0=S.econ.treasury.neutral;dockAction('rearm');return JSON.stringify({msg:dockErr,paid:c0-P.credits,toCompact:S.econ.treasury.neutral-t0})})()"""))
    print('holdings',await ev("(()=>{undock();coTab='holdings';$('company').hidden=false;renderCompany();return $('coBody').innerText.slice(0,300).replace(/\\n/g,' | ')})()"))
    print('found and worn down',await ev("""(()=>{const P=S.player,L=lairsOf(P)[0];P.stand.varkesh=-70;const e=makeNPC('scout','varkesh','scout',1,{},null);e.role='scout';e.x=L.x+800;e.y=L.y;e.z=L.z;W.ents.push(e);const h0=L.hull;lairWorldB(1);lairWorldB(10);return JSON.stringify({seen:L.seen,hullLost:Math.round(h0-L.hull)})})()"""))
    print('ledger',await ev(LED))
    await pg.wait_for_timeout(20000)
    print('after flight',await ev("JSON.stringify({T:Math.round(S.T),lairs:(S.lairs||[]).length})"),await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
