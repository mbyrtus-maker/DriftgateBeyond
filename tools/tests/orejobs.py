# Beyond, ore requests and Riftstone (9 Nov 2026): makers short of Aurorite or Vantium post mining jobs; a power or maker short
# of an ore has a quiet buyer ask for Riftstone on Jobs → Black market (not the main board); delivering ore pays from the
# maker's purse and fills its store; delivering Riftstone stands each unit in for one unit of the short ore pulled from the
# outer drift; the ledger stays exact throughout
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
    r=json.loads(await ev("""(()=>{running=false;exitSector();W=null;for(let i=0;i<70;i++){S.T+=10;strategicTick();updateEvents()}
      const oq=oreqAll(),rs=rsjAll();return JSON.stringify({oq:oq.length,oqOres:[...new Set(oq.map(j=>j.ore))],rs:rs.length,rsBy:[...new Set(rs.map(j=>j.by.startsWith('corp_')?'maker':'power'))],rating:rs.map(j=>j.rating)})})()"""))
    check('makers short of Aurorite and Vantium post ore requests',r['oq']>0 and set(r['oqOres'])=={'au','nu'},r)
    check('powers and makers short of an ore have Riftstone buyers',r['rs']>0 and set(r['rsBy'])=={'maker','power'},r)
    r=json.loads(await ev("""(()=>{const j=oreqAll()[0],P=S.player;P.sector=j.to;enterSector(j.to);running=false;P.docked='station';const c=dockCtx(),srcs=[P.cargo,c.storage];const L=jobsList(c,P,srcs);
      const oq=L.find(x=>x.id==='oq:'+j.id),rs=L.find(x=>String(x.id).startsWith('rs:'));const main=jbBoard(c,P,srcs,false,false),bm=jbBmHtml(c,P,srcs);
      devLedger(()=>inv.add(P.cargo,j.ore,10));const c0=P.credits,s0=ceStore(j.m)[j.ore]||0;dockAction('oreqdel',j.id);
      return JSON.stringify({oq:!!oq&&oq.ty==='mine',btn:oq&&oq.btn,rsBm:!!rs&&rs.bm===1,inMain:/Riftstone for/.test(main),inBm:/Riftstone for/.test(bm),msg:dockErr,paid:P.credits-c0,stored:(ceStore(j.m)[j.ore]||0)-s0,unit:j.unit})})()"""))
    check('the ore request is a mining job on the board at the works',r['oq'],r)
    check('Riftstone buyers are on Jobs → Black market, not the main board',r['rsBm'] and r['inBm'] and not r['inMain'],r)
    check('delivering 10 ore pays 10 × the unit price and fills the maker\'s store',r['stored']==10 and r['paid']==10*r['unit'],r)
    r=json.loads(await ev("""(()=>{const P=S.player,j=rsjAll().find(x=>!x.by.startsWith('corp_')&&x.ore!=='xc');exitSector();W=null;P.sector=j.sid;enterSector(j.sid);running=false;P.docked='station';
      devLedger(()=>{S.drift[j.ore]=(S.drift[j.ore]||0)+2;inv.add(P.cargo,'rift',3)});const st=rsjStore(j.by),o0=st[j.ore]||0,r0=st.rift||0,d0=S.drift[j.ore],x0=S.drift.xc||0,c0=P.credits;dockAction('rsjdel',j.id);
      return JSON.stringify({msg:dockErr,ore:(st[j.ore]||0)-o0,rift:(st.rift||0)-r0,drift:d0-S.drift[j.ore],xc:(S.drift.xc||0)-x0,paid:P.credits-c0,unit:j.unit,same:j.ore==='xc'})})()"""))
    check('3 Riftstone delivered: 2 stand in for the short ore from the drift, 1 kept as Riftstone',r['ore']==2 and r['rift']==1 and (r['same'] or (r['drift']==2 and r['xc']==2)) and r['paid']==3*r['unit'],r)
    l=await ev(LED);check('ledger exact',l=='exact',l)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
