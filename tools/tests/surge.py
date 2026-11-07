# Beyond Brood surges (6 Nov 2026): the war's salvage fills a galaxy-wide surge meter; the Bloom eats the debris in and next
# to its space into a surge mass (capped); full, it throws one big telegraphed wave (an offensive several times the usual
# size, grown from the mass) at a border system; beaten off, the next bar is higher; the ledger stays exact throughout
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
    print('ledger',await ev(LED))
    # salvage next to Brood space feeds the meter double, inside it not at all (the test makes the debris and books it)
    print('feed',await ev("""(()=>{running=false;exitSector();W=null;const g=surgeOf();g.m=0;const hv='bl',nb=NEIGH[hv].find(n=>!broodHeld(n)),far=SECTOR_DEFS.map(d=>d.id).find(id=>!broodHeld(id)&&!NEIGH[id].some(n=>broodHeld(n)));
      toDebris(S.sectors[hv],{fe:100});const a=g.m;toDebris(S.sectors[nb],{fe:100});const b=g.m-a;toDebris(S.sectors[far],{fe:100});const c=g.m-a-b;S.ledger0.tot.fe+=300;return JSON.stringify({inside:a,border:b,far:c,ok:a===0&&b===2*c&&c>0})})()"""))
    print('ledger',await ev(LED))
    # the Bloom eats the debris in its zone, up to its cap
    print('harvest',await ev("""(()=>{const g=surgeOf();const z=[...surgeZone()];const d=S.sectors[z[0]].debris;d.fe+=0;const before=z.reduce((a,id)=>a+S.sectors[id].debris.fe,0),s0=g.store.fe||0;for(let i=0;i<40;i++)surgeHarvest();const after=z.reduce((a,id)=>a+S.sectors[id].debris.fe,0);
      return JSON.stringify({zone:z.length,eaten:before-after,store:g.store.fe-s0,capped:(g.store.fe||0)<=SURGE.cap.fe})})()"""))
    print('ledger',await ev(LED))
    # play on until a power has a station or outpost on the Brood's border, fill the meter and surge (the test adds the debris, so it books it into the ledger's start)
    print('launch',await ev("""(()=>{const g=surgeOf();for(const e in SURGE.cap){const id=[...surgeZone()][0];S.sectors[id].debris[e]+=SURGE.cap[e];S.ledger0.tot[e]+=SURGE.cap[e]}for(let i=0;i<200;i++)surgeHarvest();
      let i=0;while(!surgeTarget()&&i<1440){S.T+=10;strategicTick();updateEvents();g.m=0;g.last=S.T;i++}g.last=-1e9;g.retry=0;g.m=surgeBar()*1.01;const n0=S.events.length;surgeTick();const ev=S.events.find(e=>e.id===g.live);
      return JSON.stringify({live:!!ev,n:ev&&ev.n,surge:ev&&ev.surge,tgt:ev&&(ev.st||ev.target),meter:g.m})})()"""))
    print('ledger',await ev(LED))
    print('resolve',await ev("""(()=>{const g=surgeOf(),k0=g.k;let i=0;while(g.live&&i<200){S.T+=10;strategicTick();updateEvents();i++}return JSON.stringify({done:!g.live,k0,k:g.k,mins:i/6})})()"""))
    print('ledger',await ev(LED))
    # a surge that breaks through digs in (the test builds a power's depot on the border if there isn't one, and books it): a razed station is seeded with a Bloom Node guarded by the survivors, who garrison it
    print('dig in (station)',await ev("""(()=>{const g=surgeOf();for(const e in SURGE.cap){const id=[...surgeZone()][0];S.sectors[id].debris[e]+=SURGE.cap[e]*3;S.ledger0.tot[e]+=SURGE.cap[e]*3}for(let i=0;i<300;i++)surgeHarvest();
      let T=null;for(const d of SECTOR_DEFS){const sid=d.id;if(broodHeld(sid)||!NEIGH[sid].some(n=>broodHeld(n)))continue;const R=S.stations[sid];if(R&&R.kind==='depot'&&R.owner!=='brood'&&fightsAt('brood',R.owner)){T=sid;break}}
      if(!T){const sid=SECTOR_DEFS.map(d=>d.id).find(id=>!broodHeld(id)&&NEIGH[id].some(n=>broodHeld(n))&&canBuildIn(id,'halcyon'));if(!sid)return 'no site';completeBuild({att:'halcyon',sector:sid,site:stationSite(sid),force:{}},{...FWD_COST});const v=invVec(FWD_COST);for(const e of RAWS)S.ledger0.tot[e]+=v[e];T=sid}
      g.last=-1e9;g.retry=0;g.live=null;const ot=surgeTarget;surgeTarget=()=>({sid:T,tgt:{st:T}});const ok=surgeLaunch();surgeTarget=ot;const ev=S.events.find(e=>e.id===g.live);if(!ok||!ev)return 'no launch';
      razeStation(T,'brood');ev.stage='done';finishOffensive(ev);const b=S.events.find(e=>e.type==='build'&&e.surgeDig&&e.sector===T);if(!b)return 'no seed';
      let i=0;while(b.stage!=='done'&&i<60){S.T+=10;updateEvents();i++}const R=S.stations[T],ro=S.gar&&S.gar['S.'+T];g.live=null;
      return JSON.stringify({seeded:!!b,node:R&&R.owner,garrison:ro&&ro.m.length,usual:R&&grTarget(grSite('S.'+T))})})()"""))
    print('ledger',await ev(LED))
    print('gauge',await ev("(()=>{const h=mapSectorNow('bl');return /The Bloom stirs/.test(h)?'shown':'missing'})()"))
    print('errors',errs[:5] or 'none')
    await b.close()
asyncio.run(main())
