# Beyond live space stage 5 (6 Nov 2026): AI contractors fly the jobs. A taken job is a tracked ship: live, a Mine taker
# drills a real rock and unloads into the depot; a Supply taker flies in through a gate to the depot; a taker shot down fails
# the job (no fee, its hold as salvage); a Guard taker patrols the depot; the ledger stays exact throughout
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
    print('depot',await ev("""(()=>{const P=S.player;undock();P.rp=5000;const sid=SECTOR_DEFS.map(d=>d.id).find(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id]&&S.sectors[id].ast.some(a=>!a.rift&&oreTotal(a)>40));exitSector();P.sector=sid;P.docked=null;enterSector(sid);P.cls='bulker';fitOf(P);refreshPlayerStats();devLedger(()=>{P.cargo={frame:2}});
      depFresh(P);transfer('halcyon','player',20000);window._SID=sid;const p=W.player;p.x=4000;p.y=2000;p.z=4000;return sid})()"""))
    print('mine taken',await ev("""(()=>{const P=S.player,sid=window._SID;for(const I of indL())if(!I.live&&I.at!=='job'){if(I.go&&I.go.kid){const k=(S.contracts||[]).find(c=>c.id===I.go.kid);if(k)k.ind=null}I.go=null;I.at='dock';I.restT=0};pjPost(P,`${sid}:mine:x:12:fast`);const j=S.pj[S.pj.length-1];j.claimAt=S.T;pjTick();const r=pjRunOf(j.run);r.leg=r.path.length-1;r.sector=sid;r.state='work';r.until=1e12;r.live=false;pjSpawn(r,false);window._J=j;window._RR=r;const e=W.ents.find(x=>x.pjRun===r.id);return JSON.stringify({run:!!r,ship:e&&e.cls,side:e&&e.side})})()"""))
    await pg.wait_for_timeout(25000)
    print('drilling',await ev("(()=>{const r=window._RR,e=W.ents.find(x=>x.pjRun===r.id);return JSON.stringify({cargo:e?Math.round(invMass(e.cargo)*10)/10:-1,mining:!!(e&&e.mining),cut:r.cut})})()"))
    print('ledger',await ev(LED))
    print('unload',await ev("(()=>{const r=window._RR,j=window._J,e=W.ents.find(x=>x.pjRun===r.id);if(!e)return 'no ship';const st0=invMass(S.stations[window._SID].stock);r.cut=j.n-invMass(e.cargo);const SE=W.stationEnt;e.x=SE.x+120;e.y=SE.y;e.z=SE.z;window._st0=st0;return 'ok'})()"))
    await pg.wait_for_timeout(3000)
    print('done',await ev("(()=>{const j=window._J;return JSON.stringify({state:j.state,msg:j.msg,store:Math.round(invMass(S.stations[window._SID].stock)-window._st0)})})()"))
    print('ledger',await ev(LED))
    print('supply in by the gate',await ev("""(()=>{const P=S.player,sid=window._SID;const R=S.stations[sid];devLedger(()=>{});for(const I of indL())if(!I.live&&I.at!=='job'){if(I.go&&I.go.kid){const k=(S.contracts||[]).find(c=>c.id===I.go.kid);if(k)k.ind=null}I.go=null;I.at='dock';I.restT=0};pjPost(P,`${sid}:supply:plate:8:fast`);const j=S.pj[S.pj.length-1];j.claimAt=S.T;pjTick();const r=pjRunOf(j.run);if(!r)return j.msg||'no run';if(r.pick)pjPick(r);const nb=NEIGH[sid][0];r.path=[nb,sid];r.leg=1;r.sector=sid;r.live=false;pjSpawn(r,true);window._S=r;window._SJ=j;window._pl0=R.stock.plate||0;const e=W.ents.find(x=>x.pjRun===r.id);return JSON.stringify({ship:e&&e.cls,load:e&&e.cargo})})()"""))
    for i in range(12):
      await pg.wait_for_timeout(5000)
      if await ev("window._SJ.state==='done'"):break
    print('delivered',await ev("(()=>{const j=window._SJ;return JSON.stringify({state:j.state,msg:j.msg,plate:(S.stations[window._SID].stock.plate||0)-window._pl0})})()"))
    print('ledger',await ev(LED))
    print('shot down',await ev("""(()=>{const P=S.player,sid=window._SID;for(const I of indL())if(!I.live&&I.at!=='job'){if(I.go&&I.go.kid){const k=(S.contracts||[]).find(c=>c.id===I.go.kid);if(k)k.ind=null}I.go=null;I.at='dock';I.restT=0};pjPost(P,`${sid}:supply:plate:5:fast`);const j=S.pj[S.pj.length-1];j.claimAt=S.T;pjTick();const r=pjRunOf(j.run);if(!r)return j.msg||'no run';if(r.pick)pjPick(r);const nb=NEIGH[sid][0];r.path=[nb,sid];r.leg=1;r.sector=sid;r.live=false;pjSpawn(r,true);const e=W.ents.find(x=>x.pjRun===r.id);const c0=P.credits;killShip(e,'pirate',{});return JSON.stringify({state:j.state,msg:j.msg,feePaid:P.credits-c0})})()"""))
    print('ledger',await ev(LED))
    print('guard on patrol',await ev("""(()=>{const P=S.player,sid=window._SID;for(const I of indL())if(!I.live&&I.at!=='job'){if(I.go&&I.go.kid){const k=(S.contracts||[]).find(c=>c.id===I.go.kid);if(k)k.ind=null}I.go=null;I.at='dock';I.restT=0};pjPost(P,`${sid}:guard:x:0:fast`);const j=S.pj[S.pj.length-1];j.claimAt=S.T;pjTick();const r=pjRunOf(j.run);r.leg=r.path.length-1;r.sector=sid;r.state='work';r.until=S.T+1200;r.live=false;pjSpawn(r,false);const e=W.ents.find(x=>x.pjRun===r.id);return JSON.stringify({role:e&&e.role,line:pjRunLine(j),gun:depGunK(W.stationEnt,{role:'raider',side:'pirate'})})})()"""))
    await pg.wait_for_timeout(4000)
    print('ledger',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
