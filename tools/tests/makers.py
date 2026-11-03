# Beyond stage 7: makers. Maker products exist with their traits; the first stock sits at each maker's home; the works build
# from the station's components (ledger exact); fitting a maker's part applies its trait (Marchgun damage and rounds, Wakefire
# magazine, Coldwater Refit's grade cap) and keeps its maker through a hull change; the market lists the works
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
    await ev("(()=>{window.give=(k,n)=>devLedger(()=>inv.add(S.player.vault,k,n||1));window.FC={storageName:'Vault',get storage(){return S.player.vault}};return 1})()")
    print('makers',await ev("JSON.stringify(Object.keys(MAKERS).map(m=>MAKERS[m].short+'@'+mkHomeSid(m)+':'+(mkAtHome(m)?'home':'gone')))"))
    print('items',await ev("JSON.stringify(['mp_mg_gun','mp_bl_laser','mp_wf_missile','mp_cr_gun'].map(k=>ITEMS[k].name+' · '+ITEMS[k].trTxt))"))
    print('first stock',await ev("JSON.stringify(Object.fromEntries(['mp_mg_gun','mp_mwa_laser','mp_cp_mlaser'].map(k=>{const m=ITEMS[k].maker;return[k,(mkStock(mkAtHome(m))[k])||0]})))"))
    print('works',await ev("""(()=>{const R=mkAtHome('mwa'),st=mkStock(R),n0=Object.keys(MAKERS.mwa.parts).reduce((s,k)=>s+(st['mp_mwa_'+k]||0),0);devLedger(()=>{for(const k in MAKERS.mwa.parts)inv.take(st,'mp_mwa_'+k,9)});
      devLedger(()=>{inv.add(st,'plate',30);inv.add(st,'wire',30);inv.add(st,'coil',10)});const L0=ledger();S.mkT=0;makersTick();S.mkT=0;makersTick();const n1=Object.keys(MAKERS.mwa.parts).reduce((s,k)=>s+(st['mp_mwa_'+k]||0),0);return JSON.stringify({before:n0,after:n1})})()"""))
    print('ledger',await ev(LED))
    print('marchgun',await ev("""(()=>{const P=S.player;undock();magTick(P,.1);const a0=ammoCap(P),e=W.player;give('mp_mg_gun');const m=fitDo(FC,P,'w:0:mp_mg_gun');magTick(P,.1);const a1=ammoCap(P);
      let d0=0,d1=0;const o=W.shots.length;P.ammo=50;e.cool=0;e.energy=e.st.eCap;e.boot=0;fire(e);d1=W.shots.length>o?W.shots[W.shots.length-1].dmg:0;return JSON.stringify({msg:m,ammo0:a0,ammo1:a1,shotDmg:+d1.toFixed(2),base:+e.st.dmg.toFixed(2),fit:fitOf(P).wi})})()"""))
    print('wakefire',await ev("""(()=>{const P=S.player;const r0=pRack(P);give('mp_wf_missile');fitDo(FC,P,'w:2:mp_wf_missile');return JSON.stringify({rack0:r0,rack1:pRack(P)})})()"""))
    print('refit cap',await ev("""(()=>{const P=S.player;give('mp_cr_laser');fitDo(FC,P,'w:1:mp_cr_laser');const F=fitOf(P);devLedger(()=>{F.g[1]=3});return JSON.stringify({q:pupQuote(FC,P,'w:1')})})()"""))
    print('ledger',await ev(LED))
    print('hull change keeps makers',await ev("""(()=>{const P=S.player;P.cls='heavy';const F=fitOf(P);const r={w:F.w,wi:F.wi,g:F.g};P.cls='interceptor';fitOf(P);return JSON.stringify(r)})()"""))
    print('ledger',await ev(LED))
    print('market works',await ev("(()=>{exitSector();S.player.sector=S.player.home;enterSector(S.player.home);S.player.docked='station';dockTab='market';renderDock();const t=document.querySelector('#dBody').innerText;const i=t.search(/works here/i);return i>=0?t.slice(i,i+300).replace(/\\n/g,' | '):'missing'})()"))
    print('loadout offers makers',await ev("(()=>{dockTab='ship';renderDock();return [...document.querySelectorAll('#dBody [data-act=fit]')].map(b=>b.dataset.arg).filter(a=>a.includes('mp_')).slice(0,6).join(' ')})()"))
    print('strategic hour',await ev("(()=>{running=false;exitSector();W=null;const t0=S.T;while(S.T<t0+1800){S.T+=10;strategicTick();updateEvents()}return JSON.stringify(Object.fromEntries(Object.keys(MAKERS).map(m=>{const R=mkAtHome(m);return[m,R?Object.keys(MAKERS[m].parts).map(k=>mkStock(R)['mp_'+m+'_'+k]||0).join('/'):'gone']})))})()"))
    print('ledger',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
