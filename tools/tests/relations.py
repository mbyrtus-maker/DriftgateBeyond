# Beyond stage 2: relations between the powers and their leaders. Ledger arithmetic and bands; hostility and war follow the
# ledger; an event fires on its trigger and the chronicle records it; a killed leader is succeeded; the Allegiance tab renders;
# a minute of flight with leaders in the world and no simulation errors
import asyncio,json
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    print('start',await ev("(()=>{relInit();return JSON.stringify({rel:relOf('halcyon','varkesh'),band:REL_BANDS[relBandOf('halcyon','varkesh')][0],hostile:hostile('halcyon','varkesh'),war:warWith('halcyon','varkesh'),leaders:FAC_IDS.map(f=>lName(f)+' '+leaderOf(f).traits.join('/'))})})()"))
    print('arithmetic',await ev("(()=>{relAdd('halcyon','varkesh',-30,'test');const a=relOf('varkesh','halcyon');relAdd('halcyon','varkesh',200,'test');const b=relOf('halcyon','varkesh');S.rel.halcyon.varkesh=S.rel.varkesh.halcyon=0;return JSON.stringify({sym:a,clamp:b,bands:[-60,-30,0,40,70].map(v=>REL_BANDS[relBand(v)][0])})})()"))
    print('hostility',await ev("(()=>{const o={};for(const v of[-60,-20,0]){S.rel.halcyon.ostrova=S.rel.ostrova.halcyon=v;o[v]={hostile:hostile('halcyon','ostrova'),war:warWith('halcyon','ostrova')}}S.rel.halcyon.ostrova=S.rel.ostrova.halcyon=0;return JSON.stringify(o)})()"))
    # a war declared on its trigger: relation below War and a grudge
    print('war event',await ev("(()=>{S.rel.varkesh.ostrova=S.rel.ostrova.varkesh=-55;leaderOf('varkesh').grudge.ostrova=2;pairOf('varkesh','ostrova').cool=0;const o=leaderOptions('varkesh').filter(x=>x.g==='ostrova').map(x=>x.k);const w=o.includes('war');if(w)leaderOptions('varkesh').find(x=>x.k==='war'&&x.g==='ostrova').fn();return JSON.stringify({options:o,war:warWith('varkesh','ostrova'),rel:relOf('varkesh','ostrova'),chron:(S.chron.slice(-1)[0]||{}).msg})})()"))
    print('ceasefire',await ev("(()=>{const P=pairOf('varkesh','ostrova');P.warT=S.T-3000;evCeasefire('ostrova','varkesh');return JSON.stringify({war:warWith('varkesh','ostrova'),rel:relOf('varkesh','ostrova'),chron:(S.chron.slice(-1)[0]||{}).msg})})()"))
    print('border',await ev("(()=>{evBorder('halcyon','ostrova','sh');const D=pairOf('halcyon','ostrova').demand;D.until=S.T;leaderTick();return JSON.stringify({demand:pairOf('halcyon','ostrova').demand,rel:Math.round(relOf('halcyon','ostrova')),chron:S.chron.slice(-2).map(x=>x.msg)})})()"))
    print('succession',await ev("(()=>{const old=leaderOf('halcyon').name;succession('halcyon','killed','varkesh');const N=leaderOf('halcyon');return JSON.stringify({old,new:N.name,traits:N.traits,grudge:N.grudge,chron:(S.chron.slice(-1)[0]||{}).msg})})()"))
    print('allegiance tab',await ev("(()=>{dockTab='allegiance';renderDock();return document.querySelector('#dBody').innerText.slice(0,500).replace(/\\n/g,' | ')})()"))
    print('leader in the world',await ev("(()=>{undock();const L=leaderOf('varkesh');L.ship.sid=W.sid;L.ship.alive=true;L.ship.live=0;leaderShipTick();const e=leaderEnt('varkesh');if(!e)return 'not spawned';const old=L.name;killShip(e,'halcyon',null);const N=leaderOf('varkesh');return JSON.stringify({spawned:e.pname,succeeded:N.name!==old,rel:Math.round(relOf('halcyon','varkesh')),chron:(S.chron.slice(-1)[0]||{}).msg})})()"))
    print('strategic hour',await ev("(()=>{const W0=W,L=LW;running=false;exitSector();W=null;const t0=S.T;while(S.T<t0+3600){S.T+=10;strategicTick();updateEvents()}return JSON.stringify(relStats())})()"))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
