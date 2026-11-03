# Beyond: the smaller items. Beacon rigs and limpet racks fit scouts only; no rig, no flip; a grade 2 rig flips twice and is
# restocked on docking; a grade 2 rack carries two limpets; a comet logged and sold to the Compact; goods bought at a power's
# market carry its origin and are contraband in the space of a power embargoing it; a Rift Shard standing in for a missing
# component and leaving a trait on an upgrade; the ledger stays exact
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
    print('scouts only',await ev("""(()=>{const P=S.player;P.rp=5000;P.cls='striker';fitOf(P);const c=dockCtx();devLedger(()=>{inv.add(P.cargo,'pt_bdev',1)});const m=fitDo(c,P,'u:0:pt_bdev');devLedger(()=>{inv.take(P.cargo,'pt_bdev',1)});return m})()"""))
    print('no rig',await ev("""(()=>{const P=S.player;P.cls='scout';fitOf(P);devLedger(()=>{const F=fitOf(P);F.u=['scanner','','lrack'];F.ug=[1,1,2];F.ui=[null,null,null]});refreshPlayerStats();P.docked=null;W.player.ghost=0;P.intelFor='ostrova';if(standOf('ostrova',P)<STAND.dock)standAdd('ostrova',40,'test',P);return JSON.stringify(bcnFlipper(W.player))})()"""))
    print('rig grade 2',await ev("""(()=>{const P=S.player;devLedger(()=>{const F=fitOf(P);F.u=['scanner','bdev','lrack'];F.ug=[1,2,2]});P.bdUsed=0;const out=[];for(let i=0;i<3;i++){const f=bcnFlipper(W.player);out.push(!!f);if(f){const B=S.beacons[W.sid];B.owner=null;beaconFlip(W.sid,f.side,f.by)}}
      P.docked='station';smxRigTick();P.docked=null;return JSON.stringify({flips:out,afterDock:!!bcnFlipper(W.player)})})()"""))
    print('rack grade 2',await ev("""(()=>{const P=S.player;P.limpetUsed=false;P._lpW=false;P.lpN=0;const out=[];for(let i=0;i<2;i++){P.limpetUsed=true;smxRigTick();out.push(P.limpetUsed)}return JSON.stringify({usedAfter:out})})()"""))
    print('ledger',await ev(LED))
    print('comet sold',await ev("""(()=>{const P=S.player,s=S.sectors[W.sid],p=W.player;let a;devLedger(()=>{a={id:S.nextId++,x:p.x+800,y:p.y,z:p.z,ore:{xc:60},seed:7,comet:true,until:S.T+260};s.ast.push(a)});S.events.push({id:S.nextId++,type:'comet',sector:W.sid,until:S.T+260});smxFindTick();
      const key='c'+a.id,F=P.finds&&P.finds[key];if(!F)return 'not logged';const fp=Object.keys(S.stations).find(x=>S.stations[x].owner==='neutral');P.docked='station';const sec=P.sector;P.sector=fp;const c0=P.credits;dockAction('findsell',key);P.sector=sec;P.docked=null;return JSON.stringify({pay:F.pay,msg:dockErr,got:P.credits-c0})})()"""))
    print('ledger',await ev(LED))
    print('embargo origin',await ev("""(()=>{const P=S.player;relInit();pairOf('halcyon','varkesh').emb=1;const hs=Object.keys(S.stations).find(s=>S.stations[s].owner==='varkesh'&&S.stations[s].kind==='core');P.cls='bulker';fitOf(P);refreshPlayerStats();devLedger(()=>{P.cargo={}});const sec=P.sector;P.sector=hs;P.docked='station';transfer('halcyon','player',3000);dockAction('buy','plate:10');P.docked=null;P.sector=sec;
      return JSON.stringify({bought:P.cargo.plate||0,orig:P.orig,inHalcyon:contraFor(P,'halcyon'),inOstrova:contraFor(P,'ostrova')})})()"""))
    print('ledger',await ev(LED))
    print('rift shard stands in',await ev("""(()=>{const P=S.player;const fp=Object.keys(S.stations).find(x=>S.stations[x].owner==='neutral');P.sector=fp;P.docked='station';devLedger(()=>{P.cargo={plate:2,riftshard:2};const st0=dockCtx().storage;for(const k in st0)delete st0[k];S.drift.fe+=50;S.drift.cu+=50});const m0=JSON.stringify({rc:PART_RC.gun,wire:countIn('wire',[P.cargo,dockCtx().storage]),st:Object.keys(dockCtx().storage||{}).length});dockAction('make','pt_gun:1');return JSON.stringify({recipe:m0,msg:dockErr,cargo:P.cargo})})()"""))
    print('ledger',await ev(LED))
    print('rift trait',await ev("""(()=>{const P=S.player;P.rp=5000;P.cls='striker';fitOf(P);refreshPlayerStats();const F=fitOf(P);const i=0;devLedger(()=>{F.w[0]='gun';F.g[0]=1;(F.wi=F.wi||[])[0]=null;inv.add(P.cargo,'plate',4);inv.add(P.cargo,'wire',4);inv.add(P.cargo,'riftshard',1)});transfer('halcyon','player',2000);const a=mkTr(P,'gun','dmg')+mkTr(P,'gun','ammo');dockAction('pupr','w:'+i);return JSON.stringify({msg:dockErr,rt:F.rt,before:a})})()"""))
    print('ledger',await ev(LED))
    await pg.wait_for_timeout(8000)
    print('after flight',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
