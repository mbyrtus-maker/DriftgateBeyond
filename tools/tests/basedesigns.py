# Beyond, base designs (8 Nov 2026): a player's Depot and Station draw in the design bmDesignOf gives (six, picked on the
# company profile; looks only). Every design's models are in the pack; a Depot at levels 1-3 and a Station with buildings
# build a mesh in each design (cached per design), with the buildings on the same hardpoints; the turret seats come from the
# design's model and sit on it; changing the design re-seats the turrets; an unknown design falls back to the standard set;
# the twelve player marks draw as SVG. Screenshots of each design in game go to DG_OUT. No errors.
# (A visual test: the base is made with depMake, not from a kit, so the ledger isn't checked here.)
import asyncio,json,os,tempfile
from playwright.async_api import async_playwright
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
D=os.path.join(os.environ.get('DG_OUT',tempfile.gettempdir()),'')
FAILS=[]
def check(n,ok,info=''):
  print(('ok   ' if ok else 'FAIL ')+n+(' · '+str(info) if info!='' else ''),flush=True)
  if not ok:FAILS.append(n)
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1200,'height':760});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)[:300]))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(3000)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    r=json.loads(await ev("""JSON.stringify({n:BM_DESIGNS.length,ids:BM_DESIGNS.map(d=>d.id),miss:BM_DESIGNS.flatMap(d=>[d.core,d.depot(1),d.depot(2),d.depot(3)]).filter(m=>!mdlHas(m)),
      tp:BM_DESIGNS.filter(d=>d.id>1).map(d=>[MDL.i[d.core].tp.length,MDL.i[d.depot(1)].tp.length])})"""))
    check('six designs, every model in the pack',r['n']==6 and r['ids']==[1,2,3,4,5,6] and not r['miss'],r)
    check('designs 2-6 carry turret seats (8 on the core, 6 on the depot)',all(t==[8,6] for t in r['tp']),r['tp'])
    # (the cache key ends in the owner's colour: a later wrapper passes the player's hue as co:<hex>)
    # a player Depot in an empty system, the player parked off it
    r=json.loads(await ev("""(()=>{const P=S.player;undock();const sid=Object.keys(DEF).find(s=>depCan(s)&&DEF[s].kind!=='hive'&&DEF[s].kind!=='den');exitSector();W=null;P.sector=sid;enterSector(sid);
      const R=depMake(P,sid,{x:0,y:0,z:0},{},{});depEnt(R);window.__R=R;return JSON.stringify({sid,ent:!!(W.stationEnt&&W.stationEnt.rec===R)})})()"""))
    check('a player Depot stands in an empty system',r['ent'],r)
    view=lambda d:ev(f"""(()=>{{const E=W.stationEnt,p=W.player;p.x=E.x+{d};p.y=E.y+{d}*.32;p.z=E.z+{d}*.85;p.vx=p.vy=p.vz=0;faceInstant(p,E.x-p.x,E.y-p.y,E.z-p.z);cam.snap=true;return 1}})()""")
    shapes={};seats={}
    for n in range(1,7):
      for lv,dv in ((1,0),(2,3),(3,6)):
        r=json.loads(await ev(f"""(()=>{{const R=__R;R.design={n};const d=devOf(R);d.store={dv};d.prod=0;d.def=0;d.armor=0;d.hangar=0;const SE=W.stationEnt;
          const m=bmBase(R,'player'),T=bmTurrets(R);let far=0;for(const t of T)far=Math.max(far,Math.hypot(...t));
          return JSON.stringify({{lv:depLvl(R),key:Object.keys(MESH).filter(k=>k.startsWith('bm{n}d')).length,ok:!!(m&&m.core),nt:T.length,far:Math.round(far),model:bmModel(R)}})}})()"""))
        check(f'design {n}: Depot {lv} builds ({r["model"]}), turret seats on it',r['lv']==lv and r['ok'] and r['nt']>=6 and r['far']<3.2*48,r)
        if lv==3:
          await view(520);await pg.wait_for_timeout(900);await pg.screenshot(path=D+f'basedesign_{n}_depot3.png')
      seats[n]=await ev("JSON.stringify(bmTurrets(__R).map(t=>t.map(Math.round)))")
    check('each design seats its Depot turrets differently',len(set(seats.values()))==6)
    # the game re-seats a base's turrets when its design changes
    r=json.loads(await ev("""(()=>{const R=__R,SE=W.stationEnt;R.design=1;SE._mt=0;mdlStationTurrets(SE);const a=JSON.stringify(SE.turrets.filter(t=>!t.mod).map(t=>t.p));
      R.design=4;worldUpdate(.016);mdlStationTurrets(SE);const b=JSON.stringify(SE.turrets.filter(t=>!t.mod).map(t=>t.p));return JSON.stringify({moved:a!==b,n:SE.turrets.length,shape:SE._bmShape})})()"""))
    check('a new design re-seats the Depot\'s turrets',r['moved'] and r['shape'].startswith('4'),r)
    # upgrade to a Station with three buildings: each design's core takes them on the same hardpoints
    await ev("(()=>{const R=__R;R.pst=1;R.bld=['yard','storage','market'];return 1})()")
    for n in range(1,7):
      r=json.loads(await ev(f"""(()=>{{const R=__R;R.design={n};const m=bmBase(R,'player'),T=bmTurrets(R);let far=0;for(const t of T)far=Math.max(far,Math.hypot(...t));
        return JSON.stringify({{ok:!!(m&&m.core),nt:T.length,far:Math.round(far),model:bmModel(R),bld:(R.bld||[]).join(','),keys:Object.keys(MESH).filter(k=>k.startsWith('bm{n}s')),key:Object.keys(MESH).some(k=>k.startsWith('bm{n}s'+(R.bld||[]).join(',')))}})}})()"""))
      check(f'design {n}: Station with three buildings builds ({r["model"]}), turret seats on the core',r['ok'] and r['key'] and r['nt']>=8 and r['far']<5.5*32,r)
      await ev("(()=>{const SE=W.stationEnt;SE._mt=0;mdlStationTurrets(SE);return 1})()");await view(1050);await pg.wait_for_timeout(900);await pg.screenshot(path=D+f'basedesign_{n}_station.png')
    r=await ev("(()=>{const R=__R;R.design=9;return bmDesign(R).id+':'+bmModel(R)})()")
    check('an unknown design falls back to the standard set',r=='1:by_core',r)
    r=json.loads(await ev("JSON.stringify({n:CO_LOGO.length,svg:CO_LOGO.every((L,i)=>/^<svg[^>]*>.*<path d=\"M/.test(coLogoSvg(i,20,'#4a8cff',true))&&coLogoSvg(i,40).includes(L.d)),names:CO_LOGO.map(L=>L.n),clash:CO_LOGO.filter(L=>Object.values(MK_LOGO).some(M=>M.n===L.n||M.d===L.d)).length})"))
    check('twelve player marks draw as SVG, none a maker\'s or spare mark',r['n']==12 and r['svg'] and r['clash']==0,r['names'])
    check('no errors',not errs,errs[:3])
    print('screenshots in',D)
    print('ALL OK' if not FAILS else 'FAILED: '+', '.join(FAILS))
    await b.close()
asyncio.run(main())
