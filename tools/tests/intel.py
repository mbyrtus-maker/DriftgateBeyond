# Beyond stage 5: Claim Beacons for any power, claim jobs, and intel work for contractors. Beacons sold by power at a
# freeport; a claim in the ring with a power's beacon claims for that power, pays its fee and moves standing (ledger exact);
# claim and intel jobs listed; "Intel work for" routes beacon flips and limpets; scanners see anomalies; anomalies sit out
# beyond the gates; a minute of flight with no simulation errors
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
    print('sold here',await ev("(()=>{const c=dockCtx();return JSON.stringify({dock:c.name,powers:fbSold(c,S.player)})})()"))
    print('buy',await ev("""(()=>{const c=dockCtx(),P=S.player,c0=P.credits,t0=S.econ.treasury[c.wallet];dockAction('buyfb','halcyon');return JSON.stringify({msg:dockErr,paid:c0-P.credits,toTreasury:S.econ.treasury[c.wallet]-t0,hold:P.cargo.bc_halcyon||0,vault:P.vault.bc_halcyon||0})})()"""))
    print('market section',await ev("(()=>{dockTab='market';renderDock();const t=document.querySelector('#dBody').innerText;const i=t.indexOf('CLAIM BEACONS')>=0?t.indexOf('CLAIM BEACONS'):t.indexOf('Claim Beacons');return i>=0?t.slice(i,i+160).replace(/\\n/g,' | '):'missing'})()"))
    print('ledger',await ev(LED))
    print('claim jobs',await ev("(()=>{dockTab='jobs';renderDock();const L=JOBS_LAST.filter(j=>String(j.id).startsWith('cl:'));return JSON.stringify({n:L.length,first:L.slice(0,3).map(j=>j.title+' · '+j.pay+' · '+j.where)})})()"))
    # a claim completed with a Halcyon beacon (the claim fee from Halcyon's treasury, standing up, the outpost Halcyon's)
    print('claim',await ev("""(()=>{const P=S.player;const o=Object.values(S.outposts).find(x=>!x.owner);if(!o)return 'no unclaimed outpost';if(!P.cargo.bc_halcyon){inv.take(P.vault,'bc_halcyon',1);inv.add(P.cargo,'bc_halcyon',1)}
      P.job={by:'halcyon',kind:'fight',id:`cl:${o.id}:halcyon`,at:S.T};const c0=P.credits,t0=S.econ.treasury.halcyon,s0=standOf('halcyon');fbClaim(o,'halcyon','me');
      return JSON.stringify({outpost:o.name,owner:o.owner,got:P.credits-c0,fromHalcyon:t0-S.econ.treasury.halcyon,stand:+(standOf('halcyon')-s0).toFixed(2),beacon:P.cargo.bc_halcyon||0,job:P.job})})()"""))
    print('ledger',await ev(LED))
    # a claim in the ring, in flight: an interceptor with a beacon sitting in an unclaimed outpost's ring
    print('ring setup',await ev("""(()=>{const P=S.player;const o=Object.values(S.outposts).find(x=>!x.owner&&!outLock(x.sector));if(!o)return 'none';devLedger(()=>inv.add(P.cargo,'bc_ostrova',1));exitSector();P.sector=o.sector;P.docked=null;enterSector(o.sector);
      const OE=W.outpostEnt;if(!OE)return 'no outpost entity';const e=W.player;e.x=OE.x+150;e.y=OE.y;e.z=OE.z;e.vx=e.vy=e.vz=0;window._O=o;for(const x of W.ents)if(x.npc&&x.type==='ship'&&d3(x,OE)<900)x.alive=false;return JSON.stringify({outpost:o.name,sector:o.sector,held:fbHeld(P,o)})})()"""))
    for i in range(70):
      await pg.wait_for_timeout(1000)
      r=await ev("(()=>{const e=W.player,OE=W.outpostEnt;if(OE){e.x=OE.x+150;e.y=OE.y;e.z=OE.z;e.vx=e.vy=e.vz=0}return JSON.stringify({owner:_O.owner,p:+(_O.cap.p||0).toFixed(2)})})()")
      if json.loads(r)['owner']=='ostrova':break
    print('ring claim',r)
    print('ledger',await ev(LED))
    # intel work for a power: beacon flips and limpets route to it, with standing
    print('intel for',await ev("""(()=>{const P=S.player;const a=intelFor(P);P.intelFor='ostrova';const b=intelFor(P);P.job={by:'varkesh',kind:'scout',id:'bm:1',at:S.T};const c=intelFor(P);P.job=null;P.stand.varkesh=-30;P.intelFor='varkesh';const d=intelFor(P);P.stand.varkesh=0;P.intelFor='ostrova';return JSON.stringify({none:a,picked:b,job:c,unwelcome:d})})()"""))
    print('flipper',await ev("""(()=>{const P=S.player;P.cls='scout';fitOf(P);refreshPlayerStats();const f=bcnFlipper(W.player);const s0=standOf('ostrova'),c0=P.credits;beaconFlip(W.sid,'ostrova',pkey());return JSON.stringify({flipper:f,stand:+(standOf('ostrova')-s0).toFixed(2),paid:P.credits-c0})})()"""))
    print('limpet stand',await ev("""(()=>{const P=S.player;relInit();S.rel.ostrova.varkesh=S.rel.varkesh.ostrova=-60;Object.assign(pairOf('ostrova','varkesh'),{war:true,warT:S.T});const t=makeEscort('varkesh',W.sid,{});t.dummy=true;const E=W.ents.find(x=>x.tok===t);
      const s0=standOf('ostrova');const ok=limpetPlant(E,intelFor(P),pkey(),W.player);W.tgt={kind:'ship',ref:E};return JSON.stringify({planted:ok!==false,stand:+(standOf('ostrova')-s0).toFixed(2),target:!!limpetTarget(),jobs:lpTargets('ostrova',P).length})})()"""))
    print('scanner sees',await ev("""(()=>{const P=S.player;P.cls='interceptor';fitOf(P);const a=scoutSees(P);devLedger(()=>inv.add(P.vault,'pt_scan',1));fitDo({storage:P.vault,storageName:'Vault'},P,'u:0:scanner');const b=scoutSees(P);fitDo({storage:P.vault,storageName:'Vault'},P,'u:0:land');return JSON.stringify({without:a,withScanner:b})})()"""))
    print('anomalies beyond the gates',await ev("""(()=>{const sid=anomSects()[0];const gr=Math.max(...GATES[sid].map(g=>hyp(g.x,g.y,g.z)));const d=[];for(let i=0;i<20;i++){const p=anomPos(sid);d.push(Math.round(hyp(p.x,p.y,p.z)))}return JSON.stringify({gateRing:Math.round(gr),min:Math.min(...d),max:Math.max(...d)})})()"""))
    print('intel bar',await ev("(()=>{exitSector();S.player.sector=S.player.home;enterSector(S.player.home);S.player.docked='station';openDock('jobs');dockTab='jobs';renderDock();const t=document.querySelector('#dBody').innerText;return t.slice(0,220).replace(/\\n/g,' | ')})()"))
    print('ledger',await ev(LED))
    await ev("(()=>{undock();return 1})()");await pg.wait_for_timeout(45000)
    print('after flight',await ev("JSON.stringify({T:Math.round(S.T)})"),await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
