# Beyond stage 1: the contractor start. A pilot starts unsworn at a freeport, Neutral with every power; hostility, docking,
# bounty payers, jobs by issuer and standing moves follow standing; a minute of flight with no simulation errors; ledger exact
import asyncio,json
from playwright.async_api import async_playwright
import os,tempfile
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'ERR_TUNNEL' not in m.text and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    # the start screen offers the three freeports and three roles, no scouting
    print('start',await ev("JSON.stringify({ports:[...document.querySelectorAll('#facs [data-port]')].map(b=>b.dataset.port),roles:[...document.querySelectorAll('#roles [data-role]')].map(b=>b.dataset.role)})"))
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.querySelector('#facs [data-port=cw]').click()")
    await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    print('pilot',await ev("JSON.stringify({sworn:S.player.sworn,home:S.player.home,sector:S.player.sector,docked:S.player.docked,design:S.player.faction,stand:S.player.stand,station:S.stations[S.player.sector].name})"))
    print('hostile',await ev("JSON.stringify({halcyon:hostile('player','halcyon'),compact:hostile('player','neutral'),brood:hostile('player','brood'),unbound:hostile('player','pirate'),aiVarkesh:hostile('varkesh','player')})"))
    # bands, hostility below -50, docking at -10 or better
    print('bands',await ev("JSON.stringify([-60,-50,-20,-10,0,25,40,61].map(v=>standName(v)))"))
    print('by standing',await ev("""(()=>{const P=S.player,R=S.stations.hr,out={};for(const v of[-60,-20,-5,30]){P.stand.halcyon=v;out[v]={hostile:hostile('player','halcyon'),dock:tradeOK(P,'halcyon')}}P.stand.halcyon=0;return JSON.stringify(out)})()"""))
    # bounty payers: no job, the power at war with the victim you stand best with; on a job, its issuer; nobody for the Compact's ships
    print('payer',await ev("""(()=>{const P=S.player;P.stand.ostrova=30;const a=bountyPayer('varkesh');P.job={by:'halcyon',kind:'fight'};const b=bountyPayer('varkesh');P.job=null;P.stand.ostrova=0;return JSON.stringify({best:a,job:b,compact:bountyPayer('neutral'),brood:!!bountyPayer('brood')})})()"""))
    print('kill pay',await ev("""(()=>{const P=S.player;P.stand.ostrova=30;const c0=P.credits,t0=S.econ.treasury.ostrova;payKill({side:'varkesh',role:'patrol',cls:'interceptor',tier:1,dmg:{me:100}},'player',null);const r={got:P.credits-c0,fromOstrova:t0-S.econ.treasury.ostrova,ostrova:+P.stand.ostrova.toFixed(2),halcyon:+P.stand.halcyon.toFixed(2)};P.stand.ostrova=0;P.stand.halcyon=0;P.stand.varkesh=0;return JSON.stringify(r)})()"""))
    # jobs by issuer: at a Halcyon depot, Halcyon's contracts with its +20% bonus; at the freeport, Freeport requests
    print('jobs here',await ev("""(()=>{for(let i=0;i<9;i++)scheduleContract();dockTab='jobs';renderDock();return JSON.stringify({n:JOBS_LAST.length,by:[...new Set(JOBS_LAST.map(j=>j.by))]})})()"""))
    print('jobs at a Halcyon depot',await ev("""(()=>{exitSector();S.player.sector='hr';enterSector('hr');S.player.docked='station';dockTab='jobs';renderDock();const L=JOBS_LAST.filter(j=>String(j.id).startsWith('k:'));return JSON.stringify({n:L.length,by:[...new Set(L.map(j=>j.by))],bonus:L.some(j=>String(j.pay).includes('+20%'))})})()"""))
    print('jobs when Unwelcome',await ev("""(()=>{S.player.stand.halcyon=-20;dockTab='jobs';renderDock();const n=JOBS_LAST.filter(j=>String(j.id).startsWith('k:')).length;S.player.stand.halcyon=0;return n})()"""))
    # attacking a power's ship costs standing and turns its ships on you for a minute
    print('attack',await ev("""(()=>{undock();const P=S.player;let e=W.ents.find(x=>x.type==='ship'&&x.alive&&x.npc&&x.side==='halcyon');if(!e){e=makeNPC('patrol','halcyon','interceptor',1,{},null);e.x=W.player.x+400;e.y=W.player.y;e.z=W.player.z;W.ents.push(e)}
      const s0=P.stand.halcyon,h0=hostile('halcyon','player');damageShip(e,150,'player',{src:W.player,x:e.x,y:e.y,z:e.z},'kinetic');return JSON.stringify({before:s0,after:+P.stand.halcyon.toFixed(2),hostileBefore:h0,hostileAfter:hostile('halcyon','player'),hitsAllowed:hostAt('player',W.player,e)})})()"""))
    print('aggro ends',await ev("(()=>{S.player.aggro.halcyon=S.T-1;return hostile('halcyon','player')})()"))
    print('drift',await ev("(()=>{S.player.stand.varkesh=40;standDrift(100);return +S.player.stand.varkesh.toFixed(2)})()"))
    print('ledger',await ev(LED))
    # a minute of flight
    await ev("(()=>{if(S.player.docked)undock();return 1})()");await pg.wait_for_timeout(60000)
    print('after a minute',await ev("JSON.stringify({T:Math.round(S.T),contracts:S.contracts.length})"),await ev(LED))
    # death sends a contractor home to their freeport in a free starter
    print('respawn',await ev("""(()=>{S.player.cls='striker';refreshPlayerStats();W.player.hull=1;damageShip(W.player,999,'brood',null,'kinetic');return 1})()"""))
    await pg.wait_for_timeout(9000);print('after',await ev("JSON.stringify({sector:S.player.sector,home:S.player.home,cls:S.player.cls,docked:S.player.docked})"))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
