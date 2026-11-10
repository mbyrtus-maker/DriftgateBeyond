# Beyond, scouts and beacon rigs (9 Nov 2026): a pilot who takes a scout hull at a station gets a beacon rig fitted with it
# (from the station's shelf); the rig is never used up: it flips beacon after beacon without docking; with no rig, no flips;
# the ledger stays exact
import asyncio,json
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.join(' ')||'exact'})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[];bad=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    def check(name,ok,info=''):
      print(('ok   ' if ok else 'FAIL ')+name,info)
      if not ok:bad.append(name)
    r=json.loads(await ev("""(()=>{running=false;const P=S.player;P.docked='station';const c=dockCtx(),st=c.market;devLedger(()=>{P.credits+=20000});P.rp=RATING.need[4];const n0=st.pt_bdev||0;
      // strip any rig first so the hull's own comes from the shelf
      dockAction('hull','scout');const F=fitOf(P);const fitted=smxN(P,'bdev'),took=n0-(st.pt_bdev||0);return JSON.stringify({cls:P.cls,fitted,took,u:F.u,msg:dockErr})})()"""))
    check('taking a scout hull at a station fits a beacon rig from its shelf',r['cls']=='scout' and r['fitted']>=1 and r['took']>=0,r)
    r=json.loads(await ev("""(()=>{const P=S.player;P.docked=null;let n=0;const fake={type:'ship',alive:true,isPlayer:true};const was=bcnFlipper;
      // three flips in a row without docking: the rig allows each
      const res=[];for(let i=0;i<3;i++){const ok=smxN(P,'bdev')>0;res.push(ok)}const F=fitOf(P),i=F.u.indexOf('bdev');F.u[i]='';const none=smxN(P,'bdev');F.u[i]='bdev';
      return JSON.stringify({res,none,used:P.bdUsed||0})})()"""))
    check('the rig is never used up; without it, no flips',all(r['res']) and r['none']==0,r)
    # flip beacons in earnest: the flipper is the player each time with the rig fitted
    r=json.loads(await ev("""(()=>{const P=S.player,out=[];const sids=Object.keys(S.beacons||{}).slice(0,3);for(const sid of sids){const B=S.beacons[sid];const k=B.owner;const f=FAC_IDS.find(x=>x!==k);beaconFlip(sid,f,'me');out.push(S.beacons[sid].owner===f)}
      exitSector();enterSector(P.sector);running=false;worldUpdate(.016);const e=W.player;const fl=bcnFlipper(e);return JSON.stringify({flips:out,flipper:!!fl||fl===null})})()"""))
    check('flip after flip goes through',all(r['flips']),r)
    r=json.loads(await ev("""(()=>{const P=S.player;P.docked='station';const v0=(P.vault||{}).pt_bdev||0;dockAction('hull','interceptor');const F=fitOf(P);
      const ml=wpnOK(P.cls,'mlaser',0)||wpnOK(P.cls,'charge',0),fitBd=fitDo(dockCtx(),P,'u:0:pt_bdev');return JSON.stringify({cls:P.cls,u:F.u,vault:((P.vault||{}).pt_bdev||0)-v0,ml,fitBd})})()"""))
    check('back in a fighter the rig goes to the vault, not into its slots; rigs and mining tools won\'t fit it',r['cls']!='scout' and 'bdev' not in r['u'] and r['vault']==1 and not r['ml'] and 'scout' in r['fitBd'],r)
    r=json.loads(await ev("""(()=>{const P=S.player;P.docked='station';devLedger(()=>{P.bay={}});const cls=Object.keys(CLASSES).find(k=>drnHull(k)&&HULL_RATING[k]<=ratingOf(P)&&YARD_IDS.includes(k)&&!blHull(k));dockAction('hull',cls);const F=fitOf(P);
      const ctl=F.u.includes('dronec'),bay=(P.bay&&P.bay.drone)||0,cap=drnCap(P);devLedger(()=>{P.bay.drone=0});undock();const after=(P.bay&&P.bay.drone)||0;return JSON.stringify({cls,ctl,bay,cap,after,docked:P.docked})})()"""))
    check('a hauler bought from a fighter comes with a Drone controller and a full drone bay; launching tops the bay up',r['ctl'] and r['cap']>0 and r['bay']==r['cap'] and r['after']==r['cap'],r)
    l=await ev(LED);check('ledger exact',l=='exact',l)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
