# Beyond, the makers' R&D stations (9 Nov 2026): every maker has one in its home system 4.5 km from the host station; it is
# a target with systems (control centre, labs, turrets) and no shields; a shot hits the system it passes through; spying (a
# scout's limpet) pays and gives the client's next trial +20%; sabotage (the current project's lab knocked out) pays, costs the
# project 10 minutes, launches the maker's security and makes the host's ships hostile to a contractor for a minute; the
# control centre knocked out takes it offline (sales into escrow, paid over when it comes back); the ledger stays exact
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
    r=json.loads(await ev("""(()=>{running=false;exitSector();W=null;for(let i=0;i<3;i++){S.T+=10;strategicTick();updateEvents()}const A=rdsAll(),ms=Object.keys(MAKERS).filter(m=>ceAlive(m));
      const ok=ms.every(m=>{const D=A[m],R=rdsHost(m);return D&&D.sid===mkHomeSid(m)&&R&&Math.abs(hyp(D.x-R.x,0,D.z-R.z)-RDS_G.dist)<5});
      const m=ms.find(x=>mkAtHome(x)&&MK_LINE[x].some(id=>ITEMS[rdGid(id,2)]));const c=ceOf(m);c.rd=null;const id=MK_LINE[m].find(i=>ITEMS[rdGid(i,2)]);const st=rdStart(m,id,'test');
      return JSON.stringify({n:ms.length,ok,m,rd:!!c.rd,id})})()"""))
    check('every live maker has an R&D station in its home system, 4.5 km from the host station',r['ok'],r)
    check('a project starts (its lab is on the station)',r['rd'],r)
    m=r['m']
    r=json.loads(await ev(f"""(()=>{{const m={json.dumps(m)},D=rdsOf(m),P=S.player;exitSector();W=null;P.sector=D.sid;P.docked=null;enterSector(D.sid);running=false;worldUpdate(.016);const e=W.ents.find(x=>x.type==='rds'&&x.m===m);
      const tg=targetables().some(t=>t.kind==='rds'&&t.ref===e),html=e?rdsTgtHtml(e,1000):'',labs=e?e.labs.filter(g=>g>0).length:0;return JSON.stringify({{e:!!e,tg,panel:/Control centre/.test(html)&&/lab/.test(html),labs}})}})()"""))
    check('in its system: an entity, targetable, with a panel listing its systems',r['e'] and r['tg'] and r['panel'] and r['labs']>=1,r)
    # spying: a scout's limpet
    r=json.loads(await ev(f"""(()=>{{const m={json.dumps(m)},P=S.player,e=W.ents.find(x=>x.type==='rds'&&x.m===m);S.bmoT=0;bmoTick();const x=bmoAll().find(y=>y.k==='spy'&&y.tgt===m),s=bmoAll().find(y=>y.k==='sab'&&y.tgt===m);if(!x||!s)return JSON.stringify({{posted:false}});
      const cm=x.by.slice(5),c0=ceOf(cm).spy||0;{{const l0=ledger();P.cls='scout';P.fit=fitNew('scout',null);const l1=ledger();for(const k of RAWS)S.ledger0.tot[k]+=l1.tot[k]-l0.tot[k]}}exitSector();enterSector(P.sector);running=false;worldUpdate(.016);
      const E=W.ents.find(y=>y.type==='rds'&&y.m===m);dockAction('bmotake',x.id);W.tgt={{kind:'rds',ref:E}};const p=W.player;p.x=E.x+300;p.y=E.y;p.z=E.z;const lt=limpetTarget()===E;const cr0=P.credits;const ok=limpetPlant(E,intelFor(P),pkeyOf(P),p);
      return JSON.stringify({{posted:true,lt,ok,paid:P.credits-cr0,boost:(ceOf(cm).spy||0)-c0,gone:!bmoAll().includes(x)}})}})()"""))
    check('a rival posts spying and sabotage contracts while the project runs',r.get('posted'),r)
    check('spying: a scout\'s limpet on the R&D station pays and gives the client\'s next trial +20%',r.get('lt') and r.get('ok') and r.get('paid',0)>=3000 and abs(r.get('boost',0)-0.2)<1e-9 and r.get('gone'),r)
    # sabotage: the project's lab knocked out
    r=json.loads(await ev(f"""(()=>{{const m={json.dumps(m)},P=S.player,E=W.ents.find(y=>y.type==='rds'&&y.m===m),c=ceOf(m);const x=bmoAll().find(y=>y.k==='sab'&&y.tgt===m);dockAction('bmotake',x.id);
      const L=rdsLabs(m),i=L.ids.indexOf(c.rd.id),s=rdsSubPts(E).find(q=>q.k==='lab'&&q.i===i);const u0=c.rd.until,cr0=P.credits,n0=W.ents.filter(y=>y.home==='rdsec:'+m).length;rdsDamage(E,s,99999,'player',W.player);
      const hs=rdsHostSide(m);return JSON.stringify({{i,delay:c.rd.until-u0,paid:P.credits-cr0,sec:W.ents.filter(y=>y.home==='rdsec:'+m).length-n0,aggro:hs==='neutral'||((P.aggro||{{}})[hs]||0)>S.T,gone:!bmoAll().includes(x),down:rdsHp(rdsOf(m),'lab',i)<=0}})}})()"""))
    check('sabotage: the lab is knocked out, the project loses 10 minutes, the contract pays',r['down'] and r['delay']>=599 and r['paid']>=4000 and r['gone'],r)
    check('the maker\'s security launches and the host\'s ships turn on the attacker',r['sec']>=3 and r['aggro'],r)
    # a shot hits the system it passes through
    r=json.loads(await ev(f"""(()=>{{const m={json.dumps(m)},E=W.ents.find(y=>y.type==='rds'&&y.m===m),D=rdsOf(m),s=rdsSubPts(E).find(q=>q.k==='tur');const sum=()=>rdsKeys(m).reduce((a,q)=>a+rdsHp(D,q.k,q.i),0),h0=sum();
      const ox=s.x+200,oy=s.y,oz=s.z;W.shots.push({{x:ox,y:oy,z:oz,vx:-1500,vy:0,vz:0,dmg:20,side:'player',src:W.player,ttl:1}});for(let k=0;k<20;k++)shotsUpdate(1/60);return JSON.stringify({{h0,h1:sum()}})}})()"""))
    check('a kinetic shot hits the system it flies through',r['h1']<r['h0'],r)
    # the control centre: offline, sales into escrow, back online
    r=json.loads(await ev(f"""(()=>{{const m={json.dumps(m)},E=W.ents.find(y=>y.type==='rds'&&y.m===m),s=rdsSubPts(E).find(q=>q.k==='cc');rdsDamage(E,s,99999,'player',W.player);const off=rdsOffline(m);
      const R=mkAtHome(m),id=MK_LINE[m][0],t0=ceT(m),w='rdsx_'+m,e0=S.econ.treasury[w]||0;transfer('neutral',w,0);const pay=500;devLedger(()=>{{S.econ.treasury.tmpbuyer=pay}});ceSale(m,id,1,pay,'tmpbuyer',R.sid);const esc=(S.econ.treasury[w]||0)-e0,kept=ceT(m)-t0;
      S.T=rdsOf(m).off+1;rdsTick();const back=!rdsOffline(m),after=S.econ.treasury[w]||0;return JSON.stringify({{off,esc,kept,back,after}})}})()"""))
    check('the control centre knocked out: offline, and its sales go into escrow',r['off'] and r['esc']>0 and r['kept']==0,r)
    check('back online after the repairs, the escrow reaches the company',r['back'] and r['after']==0,r)
    l=await ev(LED);check('ledger exact',l=='exact',l)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
