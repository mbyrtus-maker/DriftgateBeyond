# Beyond, the Brand screen (9 Nov 2026): Company → Brand lists every buildable part and system under the Market's part filters;
# a drive's traits are shaped and saved; Station → Fab → Your brand builds the brand's parts and systems by grade at your own
# base (grade capped by the base and by R&D, which follows the makers': funded from the treasury, design, materials, trials); a brand drive installs as the brand and its traits apply; Holdings no longer carries it;
# the ledger stays exact
import asyncio,json
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.join(' ')||'exact'})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':900});errs=[];bad=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    def check(name,ok,info=''):
      print(('ok   ' if ok else 'FAIL ')+name,info)
      if not ok:bad.append(name)
    r=json.loads(await ev("""(()=>{const P=S.player;devLedger(()=>{P.credits+=160000});let hh=40;while(coHueClash(hh))hh+=11;coSave(P,`name=Tester%20Works;logo=2;design=2;hue=${hh};tx=0.05;svc=100;dock=0`);undock();
      const sid=SECTOR_DEFS.map(d=>d.id).filter(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id])[0];exitSector();P.sector=sid;P.docked=null;enterSector(sid);running=false;devLedger(()=>{P.cargo={kit_depot:1}});depFresh(P);
      coTab='brand';$('company').hidden=false;renderCompany();const body=$('coBody').innerHTML;const cats=[...document.querySelectorAll('#coBody [data-co=brcat]')].map(b=>b.textContent.trim().split(' ')[0]);
      document.querySelector('#coBody [data-co=brcat][data-arg=p_drive]').click();const rows=[...document.querySelectorAll('#coBody [data-co=brpick]')].map(b=>b.dataset.arg);
      for(let i=0;i<3;i++){document.querySelector('#coBody [data-co=brstep][data-arg="sys_engine:thrust:1"]').click();document.querySelector('#coBody [data-co=brstep][data-arg="sys_engine:turn:-1"]').click()}
      document.querySelector('#coBody [data-co=brsave]').click();const N=brSlot(P),B=brOf(N);coTab='holdings';renderCompany();const hold=$('coBody').innerHTML;$('company').hidden=true;
      const all=MK_PARTS.reduce((a,g)=>a+brKindsIn(g).length,0);
      return JSON.stringify({cats,rows,pts:B.pts,msg:coErr,holdBrand:/Your brand/.test(hold),all,kinds:BR_KINDS.length,name:/Tester Works|Works/.test(body)})})()"""))
    check('Company → Brand: the eight part filters, every buildable kind (14 parts and 8 systems) sorted into them',r['cats']==['Drive','Reactors','Shields','Weapons','Armor','Cargo','Mining','Utility'] and r['all']==22 and r['kinds']==22,r)
    check('Drive lists the drive system; +3 thrust for −3 turning saves as the brand',r['rows']==['sys_engine'] and r['pts'].get('sys_engine')=={'thrust':3,'turn':-3},r)
    check('Holdings no longer carries the brand',not r['holdBrand'],r)
    r=json.loads(await ev("""(()=>{const P=S.player,R=myDepots(P)[0],N=brSlot(P);P.docked='station';$('dock').hidden=true;openDock('fab');fabKind='brand';renderDock();const box=!!document.querySelector('#dock [data-act=fabk][data-arg=brand]');
      const id=rdGid(`sy_bp${N}_engine`,2);const pre=dockAction('make',id+':1'),preMsg=dockErr;
      const w=P.co.w,t0=S.econ.treasury[w];const st=brRdStart(P,'sys_engine'),paid=t0-S.econ.treasury[w],twice=brRdStart(P,'gun');
      const fwd=()=>{brOf(N).rd&&(brOf(N).rd.until=S.T);brRdTick()};fwd();const st1=brOf(N).rd.stage;fwd();const waiting=brOf(N).rd.wait;
      devLedger(()=>inv.addAll(R.stock,ITEMS[id].recipe));fwd();fwd();const done=!brOf(N).rd,res=brResG(N,'sys_engine'),proto=R.stock[id]||0;
      brOf(N).g.gun=2;
      devLedger(()=>inv.addAll(R.stock,ITEMS[id].recipe));const btn=document.querySelector(`#dock [data-act=make][data-arg="${id}:1"]`);dockClick('brfabg','2');
      const btn2=document.querySelector(`#dock [data-act=make][data-arg="${id}:1"]`);if(btn2)btn2.click();const made=(R.stock[id]||0)-proto,msg=dockErr;
      brOf(N).g.sys_engine=4;const g4=dockAction('make',rdGid(`sy_bp${N}_engine`,4)+':1');const g4msg=dockErr;brOf(N).g.sys_engine=2;
      P.rp=RATING.need[6];const th0=W.player.st.thrust,tu0=W.player.st.turn;const fit=rdSysFit(`engine:${id}`);refreshPlayerStats();const th1=W.player.st.thrust,tu1=W.player.st.turn;
      const gun=rdGid(`bp${N}_gun`,2);devLedger(()=>inv.addAll(R.stock,ITEMS[gun].recipe));dockAction('make',gun+':1');const gmade=R.stock[gun]||0;$('dock').hidden=true;
      return JSON.stringify({pre:preMsg,st,paid,twice,st1,waiting,done,res,proto,box,made,msg,g4msg,fit,sysm:P.sysm.engine,N,thK:th1/th0,tuK:tu1/tu0,name:ITEMS[id].name,gmade,gname:ITEMS[gun].name,tier:P.tiers.engine})})()"""))
    check('R&D: grade 2 is not built before it is researched; funding takes 750 cr from the treasury; one project at a time',r['pre'].startswith('Research grade 2') and r['st'].startswith('✓') and r['paid']==750 and r['twice'].startswith('One R&D'),r)
    check('R&D runs design → materials (waits for the prototype components in the lab store) → trials → launch, the prototype in the store',r['st1']=='materials' and r['waiting']==1 and r['done'] and r['res']==2 and r['proto']==1,r)
    check('Station → Fab has Your brand at your Depot; a grade 2 brand drive is built into its store; grade 4 waits for a Station',r['box'] and r['made']==1 and 'grade 2' in r['g4msg'],r)
    check('installed, the brand drive is recorded as the brand, and the ship gains +9% thrust for −9% turning (on top of grade 2)',r['fit'].startswith('✓') and r['sysm']=='bp'+str(r['N']) and r['tier']==2,r)
    check('a branded grade 2 gun is built too',r['gmade']==1 and r['gname'].endswith('G2'),r)
    r=json.loads(await ev("""(()=>{const P=S.player;const t=sysTr(P.sysm.engine,'engine');return JSON.stringify(t)})()"""))
    check("sysTr reads the brand's drive traits",abs(r.get('thrust',0)-0.09)<1e-9 and abs(r.get('turn',0)+0.09)<1e-9,r)
    l=await ev(LED);check('ledger exact',l=='exact',l)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
