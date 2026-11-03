# Beyond stage 7b: smuggling. Stolen tags from a power's crates; contraband by power; heat words and cooling; a customs scan
# that finds contraband, and each answer (surrender: goods to the power's stores, ledger exact; bribe; run: hostile while hot);
# the hidden container; Riftstone (flagged, cutting yields Riftstone, ledger exact); a black-market run taken and delivered
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
    # scoop a crate spilled by a Varkesh ship: the goods are tagged as Varkesh's
    print('stolen',await ev("""(()=>{undock();const P=S.player,s=S.sectors[W.sid],e=W.player;P.cargo={};devLedger(()=>s.crates.push({id:S.nextId++,x:e.x+10,y:e.y,z:e.z,inv:{plate:3,ir:4},until:S.T+300,own:'varkesh'}));pickupAndGates(e,P,e.st);
      return JSON.stringify({cargo:P.cargo,tags:P.stol,forVarkesh:contraFor(P,'varkesh'),forHalcyon:contraFor(P,'halcyon')})})()"""))
    print('ledger',await ev(LED))
    print('heat words',await ev("JSON.stringify([0,12,40,80].map(v=>heatWord(v)[0]))"))
    # a Varkesh scan finds it: surrender sends the goods to Varkesh stores, a fine, standing and heat
    print('surrender',await ev("""(()=>{const P=S.player,c0=P.credits,st0=(S.econ.stock.varkesh.ir||0);scanResolve(P,'varkesh','me');const C=P.caught;const m=scanChoice('surrender');return JSON.stringify({found:C&&C.L,msg:m,fine:c0-P.credits,toStores:(S.econ.stock.varkesh.ir||0)-st0,heat:Math.round(heatOf('varkesh')),stand:+standOf('varkesh').toFixed(1),cargo:P.cargo})})()"""))
    print('ledger',await ev(LED))
    print('bribe',await ev("""(()=>{const P=S.player;devLedger(()=>{inv.add(P.cargo,'relic',2)});scanResolve(P,'halcyon','me');const C=P.caught,bribe=C&&C.bribe,c0=P.credits;P.stand.halcyon=60;const m=scanChoice('bribe');const r={found:C&&C.L,msg:m,paid:c0-P.credits,bribe,still:!!P.caught};if(P.caught)scanChoice('surrender');P.stand.halcyon=0;return JSON.stringify(r)})()"""))
    print('ledger',await ev(LED))
    print('run',await ev("""(()=>{const P=S.player;devLedger(()=>{inv.add(P.cargo,'relic',1)});scanResolve(P,'ostrova','me');scanChoice('run');return JSON.stringify({heat:Math.round(heatOf('ostrova')),word:heatWord(heatOf('ostrova'))[0],hostile:hostile('ostrova','player'),relic:P.cargo.relic||0})})()"""))
    print('cools',await ev("""(()=>{const P=S.player;P.aggro={};const h0=heatOf('ostrova');scanStep(1200);return JSON.stringify({before:Math.round(h0),after:Math.round(heatOf('ostrova')),hostile:hostile('ostrova','player')})})()"""))
    # the hidden container keeps up to its capacity out of a scan (most of the time)
    print('hidden',await ev("""(()=>{const P=S.player;devLedger(()=>inv.add(P.vault,'pt_hide',1));fitDo({storage:P.vault,storageName:'Vault'},P,'u:0:pt_hide');let clear=0;for(let i=0;i<40;i++){P.caught=null;scanResolve(P,'halcyon','me');if(!P.caught)clear++}P.caught=null;fitDo({storage:P.vault,storageName:'Vault'},P,'u:0:land');return JSON.stringify({cap:4,relics:P.cargo.relic||0,clearOf40:clear})})()"""))
    print('ledger',await ev(LED))
    # Riftstone: flagged rocks out beyond the gates; cutting them yields Riftstone
    print('riftstone',await ev("""(()=>{const L=[];for(const id in S.sectors)for(const a of S.sectors[id].ast)if(a.rift)L.push({sid:id,xc:a.ore.xc||0});return JSON.stringify({n:L.length,first:L.slice(0,3)})})()"""))
    print('cut riftstone',await ev("""(()=>{const P=S.player;let sid=null,a=null;for(const id in S.sectors){const x=S.sectors[id].ast.find(r=>r.rift);if(x){sid=id;a=x;break}}if(!a)return 'none';exitSector();P.sector=sid;P.docked=null;enterSector(sid);const e=W.player;
      P.cls='prospector';fitOf(P);devLedger(()=>inv.add(P.vault,'pt_mlaser',1));fitDo({storage:P.vault,storageName:'Vault'},P,'w:1:pt_mlaser');refreshPlayerStats();devLedger(()=>{P.cargo={}});
      const n=ringN(a),R=astR(a),ax=Math.abs(n.x)<.9?{x:1,y:0,z:0}:{x:0,y:1,z:0};let w={x:n.y*ax.z-n.z*ax.y,y:n.z*ax.x-n.x*ax.z,z:n.x*ax.y-n.y*ax.x};const l=hyp(w.x,w.y,w.z);w={x:w.x/l,y:w.y/l,z:w.z/l};e.x=a.x+w.x*(R+150);e.y=a.y+w.y*(R+150);e.z=a.z+w.z*(R+150);faceInstant(e,-w.x,-w.y,-w.z);
      let res={};for(let i=0;i<60;i++){W.t+=.1;e.energy=e.st.eCap;const r=mlCut(e,P,a,1,S.sectors[sid]);res[r]=(res[r]||0)+1}return JSON.stringify({results:res,cargo:P.cargo})})()"""))
    print('ledger',await ev(LED))
    # a black-market run from the freeport
    print('run offers',await ev("""(()=>{const P=S.player;exitSector();P.sector=P.home;enterSector(P.home);P.docked='station';P.cls='courier';fitOf(P);refreshPlayerStats();devLedger(()=>{P.cargo={}});P.run=null;for(let i=0;i<60;i++)fixerTick();dockTab='jobs';renderDock();const L=JOBS_LAST.filter(j=>String(j.id).startsWith('bmr:'));return JSON.stringify(L.map(j=>j.title+' · '+j.sub+' · '+j.pay))})()"""))
    print('take and deliver',await ev("""(()=>{const P=S.player,x=(S.bm||[]).find(y=>y.from===P.sector&&!y.taken);if(!x)return 'no run';dockAction('bmtake',x.id);const m1=dockErr,R=P.run;if(!R)return m1;const c0=P.credits;exitSector();P.sector=R.to;enterSector(R.to);P.docked='station';openDock();return JSON.stringify({take:m1,paid:P.credits-c0,run:P.run,cargo:P.cargo})})()"""))
    print('ledger',await ev(LED))
    print('heat on allegiance tab',await ev("(()=>{dockTab='allegiance';renderDock();const t=document.querySelector('#dBody').innerText;const i=t.search(/heat/i);return i>=0?t.slice(i,i+160).replace(/\\n/g,' | '):'missing'})()"))
    await ev("(()=>{undock();return 1})()");await pg.wait_for_timeout(30000)
    print('after flight',await ev("JSON.stringify({T:Math.round(S.T)})"),await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
