# Beyond, running your base from its own screen (9 Nov 2026): Station → Jobs hires this base's pilots, sets their jobs and lets
# them go (paid from the company treasury); the Jobs tab's Black market is open at your base; a pilot the owner lets in can
# hire and post jobs there on the owner's behalf (from the owner's treasury) but has no Company sub-tab; the ledger stays exact
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
    r=json.loads(await ev("""(()=>{const P=S.player;devLedger(()=>{P.credits+=160000});let hh=40;while(coHueClash(hh))hh+=11;coSave(P,`name=Tester%20Works;logo=2;design=2;hue=${hh};tx=0.05;svc=100;dock=0`);undock();const sid=SECTOR_DEFS.map(d=>d.id).filter(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id])[0];exitSector();P.sector=sid;P.docked=null;enterSector(sid);running=false;devLedger(()=>{P.cargo={kit_depot:1}});depFresh(P);P.rp=RATING.need[4];const R=S.stations[sid];window._S=sid;
      P.docked='station';openDock('works');dockTab='bjobs';renderDock();const t0=S.econ.treasury[P.co.w],c0=P.credits;document.querySelector('#dock [data-act=crewhire][data-arg$=":prospector"]').click();const hired=(R.crew||[]).length;renderDock();
      const q=R.crew[0];document.querySelector(`#dock [data-act=crewjob][data-arg="${sid}:${q.id}:guard"]`).click();const job=q.job;renderDock();
      const tabs=dockG.map(g=>g[2].map(t=>t[0])).flat();document.querySelector(`#dock [data-act=crewfire][data-arg="${sid}:${q.id}"]`).click();
      return JSON.stringify({hired,job,left:(R.crew||[]).length,paidT:t0-S.econ.treasury[P.co.w],paidC:c0-P.credits,bm:tabs.includes('bmjobs'),co:tabs.includes('bco'),jobs:tabs.includes('jobs')})})()"""))
    check('Station → Jobs hires a pilot, sets its job and lets it go; paid from the treasury',r['hired']==1 and r['job']=='guard' and r['left']==0 and r['paidT']>0 and r['paidC']==0,r)
    check("Jobs (the regular board), the Black market and Company are on your base's screen",r['bm'] and r['co'] and r['jobs'],r)
    r=json.loads(await ev("""(()=>{const P=S.player,R=myDepots(P)[0];P.rp=RATING.need[6];devLedger(()=>{S.econ.treasury[P.co.w]+=60000});R.crew=[];renderDock();const btn=k=>!!document.querySelector(`#dock [data-act=crewhire][data-arg$=":${k}"]`);const b={heavy:btn('heavy'),bomber:btn('bomber'),gunboat:btn('gunboat')};
      const msg=[];for(const k of['heavy','bomber','gunboat']){dockAction('crewhire',R.sid+':'+k);msg.push(dockErr)}const cls=R.crew.map(q=>q.cls),jobs=R.crew.map(q=>q.job);
      let flown=0;try{for(const q of R.crew){const e=crewSpawn(R,R.sid,q);if(e&&e.cls===q.cls)flown++}}catch(err){msg.push(String(err))}R.crew=[];
      return JSON.stringify({b,cls,jobs,flown,msg})})()"""))
    check('Heavy Fighters, Bombers and Heavy Bombers can be hired (guards) and fly',all(r['b'].values()) and r['cls']==['heavy','bomber','gunboat'] and set(r['jobs'])=={'guard'} and r['flown']==3,r)
    r=json.loads(await ev("""(()=>{const sid=_S,R=S.stations[sid],P=S.player;S.pilots=S.pilots||{};const n0={on:NET.on,me:NET.me};NET.on=true;NET.me='host1';R.pid='host1';const G={...JSON.parse(JSON.stringify(P)),pid:'g1',name:'Guest',co:null,credits:500,sector:sid,docked:'station'};S.pilots.g1=G;
      const deny=runAs('g1',()=>{dockAction('crewhire',sid+':skiff');return dockErr});dockAction('baseacc','g1:1');const t0=S.econ.treasury[P.co.w];
      const ok=runAs('g1',()=>{dockAction('crewhire',sid+':skiff');return dockErr});const tabs=runAs('g1',()=>{const c=dockCtx();return JSON.stringify({own:!!c.ownBase,owner:!!c.baseOwner})});
      const post=runAs('g1',()=>{dockAction('pjpost',sid+':mine:plate:10:medium');return dockErr});const crew=(R.crew||[]).length;delete S.pilots.g1;NET.on=n0.on;NET.me=n0.me;R.pid='me';
      return JSON.stringify({deny,ok,tabs:JSON.parse(tabs),post,crew,paid:t0-S.econ.treasury[P.co.w],gcred:G.credits})})()"""))
    check("a pilot without access is refused; let in, they hire on the owner's treasury and post jobs, but get no Company tab",('Not your' in r['deny']) and r['ok'].startswith('✓') and r['crew']==1 and r['paid']>0 and r['gcred']==500 and r['post'].startswith('✓') and r['tabs']['own'] and not r['tabs']['owner'],r)
    r=json.loads(await ev("""(()=>{const P=S.player,R=myDepots(P)[0];exitSector();W=null;P.sector=R.sid;P.docked=null;enterSector(R.sid);running=false;if(!R.pst){devLedger(()=>{P.cargo.kit_station=1});staUp(P,R)}
      P.docked='station';$('dock').hidden=true;openDock('allegiance');const b=document.querySelector('#dock [data-co=declare]');if(b)b.click();const out={btn:!!b,decl:!!P.decl,msg:dockErr,tab:dockTab,sw:P.sworn||null,decl0:declOK(P)};$('dock').hidden=true;return JSON.stringify(out)})()"""))
    check("Declare your faction works from the dock's Allegiance tab",r['btn'] and r['decl'],r)
    r=json.loads(await ev("""(()=>{const P=S.player,R=myDepots(P).find(x=>x.pst);devLedger(()=>inv.addAll(R.stock,STA.bcost));P.docked='station';$('dock').hidden=true;openDock('works');const n0=(R.bld||[]).length;
      const b=document.querySelector('#dock [data-act=stabld]');const txt=$('dBody').textContent;if(b)b.click();const n1=(R.bld||[]).length;coSel='S:'+R.sid;coTab='holdings';$('company').hidden=false;renderCompany();const hold=$('coBody').textContent;$('company').hidden=true;$('dock').hidden=true;
      return JSON.stringify({btn:!!b,n0,n1,sec:/Station buildings/.test(txt)&&/Development modules/.test(txt),hold:/they set the Station's level/.test(hold)&&/Development modules \\(Works tab/.test(hold),msg:dockErr})})()"""))
    check("a Station's buildings are built on its Works tab (above the modules), and Holdings tells buildings and modules apart",r['btn'] and r['sec'] and r['n1']==r['n0']+1 and r['hold'],r)
    r=json.loads(await ev("""(()=>{const P=S.player,R=myDepots(P)[0];const f=FAC_IDS.find(x=>homeOf(x)&&homeOf(x)!==R.sid&&trPath(homeOf(x),R.sid));const ev={id:S.nextId++,type:'offensive',att:f,st:R.sid,stName:R.name,sector:R.sid,eta:S.T+60,force:{},n:1,tier:1,cls:['interceptor'],stage:'inbound'};
      S.events.push(ev);prwStrikeStart(ev);const h=holdingsHtml(P);const m=h.match(/under threat[^<]*/);S.events.splice(S.events.indexOf(ev),1);S.raids=(S.raids||[]).filter(x=>x.strike!==ev.id);return JSON.stringify({tr:!!ev.tr,lab:m?m[0]:null})})()"""))
    check("a strike flying the lanes shows jumps out and a sane arrival time on Holdings",r['tr'] and r['lab'] and 'jump' in r['lab'] and not __import__('re').search(r'\d{6,}',r['lab']),r)
    l=await ev(LED);check('ledger exact',l=='exact',l)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
