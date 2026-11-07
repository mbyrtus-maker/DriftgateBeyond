# Beyond, the corporate economy stage 2 (7 Nov 2026): grades by invention. No upgrades in place; a graded maker part fits at
# its grade and comes out as itself; systems are parts installed at a dock (the old one to the hangar); Contractor Rating
# gates grades; an R&D project goes through funding, design, materials and trials to a launch that retires the old grade;
# makers' parts can't be fabricated; the ledger stays exact throughout
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
    print('no upgrades in place',await ev("""(()=>{const P=S.player;P.docked='station';dockErr='';dockAction('upg','engine');const a=dockErr;return JSON.stringify({upg:/gone/.test(a),pup:pupQuote(dockCtx(),P,'w:0')===null,tier:P.tiers.engine})})()"""))
    # (the test makes the parts it hands the pilot and books them into the ledger's start)
    print('a grade 2 gun',await ev("""(()=>{const P=S.player,give=id=>{inv.add(P.cargo,id,1);const v=invVec({[id]:1});for(const e of RAWS)S.ledger0.tot[e]+=v[e]};give('mp_mg_gun_g2');
      const og=gradeCap;gradeCap=()=>1;dockErr='';dockAction('fit','w:0:mp_mg_gun_g2');const refused=dockErr;gradeCap=()=>5;dockAction('fit','w:0:mp_mg_gun_g2');const ok=dockErr,F=fitOf(P);
      const fitted={kind:F.w[0],grade:F.g[0],id:F.wi[0]};dockAction('fit','w:0:');const back=countIn('mp_mg_gun_g2',[P.cargo,dockCtx().storage||P.vault]);gradeCap=og;
      return JSON.stringify({refused:/Rating/.test(refused),ok,fitted,backAsItself:back})})()"""))
    print('ledger',await ev(LED))
    print('a system installed',await ev("""(()=>{const P=S.player,id='sy_ewd_engine_g2';inv.add(P.cargo,id,1);const v=invVec({[id]:1});for(const e of RAWS)S.ledger0.tot[e]+=v[e];const og=gradeCap;gradeCap=()=>5;dockErr='';dockAction('sysfit','engine:'+id);gradeCap=og;
      const st=dockCtx().storage||P.vault;return JSON.stringify({msg:dockErr,tier:P.tiers.engine,maker:(P.sysm||{}).engine,oldOut:countIn('sy_engine',[P.cargo,st])})})()"""))
    print('ledger',await ev(LED))
    print('no fabricating a maker part',await ev("(()=>{dockErr='';dockAction('make','sy_engine_g3:1');return dockErr})()"))
    print('R&D to a launch',await ev("""(()=>{running=false;exitSector();W=null;const m='mg',id='mp_mg_gun';S.econ.treasury[ceW(m)]+=20000;S.econ.treasury.varkesh-=20000;const R=mkAtHome(m),st=mkStock(R);st.mp_mg_gun=(st.mp_mg_gun||0);
      const before=st.mp_mg_gun,ok=rdStart(m,id,'test'),P0=ceOf(m).rd&&ceOf(m).rd.stage;let i=0;while(ceOf(m).rd&&i<600){S.T+=10;strategicTick();updateEvents();i++}
      return JSON.stringify({started:ok,stage0:P0,mins:Math.round(i/6),grade:rdLineG(m,id),g2OnShelf:st.mp_mg_gun_g2||0,g1Left:st.mp_mg_gun||0,lab:ceOf(m).labs})})()"""))
    print('ledger',await ev(LED))
    print('errors',errs[:5] or 'none')
    await b.close()
asyncio.run(main())
