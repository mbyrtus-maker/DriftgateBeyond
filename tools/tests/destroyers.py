# Beyond: destroyers and the Ravager. A power lays down and launches a destroyer (two assault ships, its model, shield 2,000,
# hull 4,200, turrets on its mounts); its charged main gun drops its shields while it charges and hits for 600; the Brood's
# Gullet beam hits everything along its path; your level 4 Station lays one down; the Unbound's carrier is the Ravager with its
# own gun and model, and they lay down no sloops; the ledger stays exact throughout
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
    print('ai destroyer',await ev("""(()=>{relInit();S.T=Math.max(S.T,CAP_GATE+60);const f='halcyon',st=S.econ.stock[f];S.yards[f]=S.yards[f]||{sector:FAC_HOME(f),fort:{}};devLedger(()=>{inv.addAll(st,dstCost(f));inv.add(st,'plate',40);inv.add(st,'coil',20)});
      let n=0;while(!S.events.some(e=>e.type==='dstbuild'&&e.att===f)&&n++<200)dstTick();const ev=S.events.find(e=>e.type==='dstbuild'&&e.att===f);if(!ev)return 'not laid down';S.T=ev.until+1;dstTick();const t=facDst(f)[0];
      return JSON.stringify({laid:n,cost:dstCost(f),name:t&&t.name,cls:t&&t.cls,cap:t&&capName(t),hull:t&&t.hull,aload:t&&t.aload,max:t&&capHullMax(t)})})()"""))
    print('ledger',await ev(LED))
    print('in the world',await ev("""(()=>{const t=facDst('halcyon')[0];t.sector=W.sid;t.dest=W.sid;inW(W,()=>spawnFrigate(t,false));const e=W.ents.find(x=>x.tok===t);const p=W.player;e.x=p.x+600;e.y=p.y;e.z=p.z+600;
      const m=shipMesh(e.fac,e.cls);return JSON.stringify({sCap:e.st.sCap,shield:e.shield,hull:e.hull,mdl:!!m.mdl,turrets:e.turrets.length,label:shipLabel(e)})})()"""))
    await pg.wait_for_timeout(1500)
    print('turrets on mounts',await ev("""(()=>{const e=W.ents.find(x=>x.tok&&isDst(x.tok));return JSON.stringify(e.turrets.map(t=>t.p.map(v=>+v.toFixed(2))))})()"""))
    # a hostile Varkesh destroyer next to it: the guns charge (shields down) and fire
    print('duel set',await ev("""(()=>{window._t0=W.t;relInit();S.rel.halcyon.varkesh=S.rel.varkesh.halcyon=-60;Object.assign(pairOf('halcyon','varkesh'),{war:true,warT:S.T});const e=W.ents.find(x=>x.tok&&isDst(x.tok));
      const t2=makeDestroyer('varkesh',W.sid,{});inW(W,()=>{});let f=W.ents.find(x=>x.tok===t2);if(!f){inW(W,()=>spawnFrigate(t2,false));f=W.ents.find(x=>x.tok===t2)}f.x=e.x+900;f.y=e.y;f.z=e.z;e.mg={cd:0,ch:0};f.mg={cd:2,ch:0};
      window._smp=[];window._iv=setInterval(()=>{try{__dg.ev("(()=>{const e=W.ents.find(x=>x.tok&&isDst(x.tok)&&x.side==='halcyon');if(e)window._smp.push([e.mg?+e.mg.ch.toFixed(2):-1,Math.round(e.shield),Math.round(e.hull)]);return 1})()")}catch(err){}},100);return JSON.stringify({a:e.hull,b:f.hull,mesh:!!shipMesh(f.fac,f.cls).mdl})})()"""))
    t0=await ev("W.t");await pg.wait_for_function(f'window.__dg&&__dg.ev("W.t")>{t0}+12',timeout=90000)
    print('duel',await ev("""(()=>{clearInterval(window._iv);const S2=window._smp,ch=S2.filter(s=>s[0]>0),f=W.ents.find(x=>x.tok&&isDst(x.tok)&&x.side==='varkesh'),t2=S.frigates.find(x=>isDst(x)&&x.side==='varkesh');
      return JSON.stringify({samples:S2.length,charging:ch.length,shieldWhileCharging:Math.max(0,...ch.map(s=>s[1])),shieldOther:Math.max(0,...S2.filter(s=>s[0]<=0).map(s=>s[1])),varkeshHull:f?Math.round(f.hull):(t2?t2.hull:'gone')})})()"""))
    print('ledger',await ev(LED))
    print('gullet',await ev("""(()=>{relInit();const g=makeDestroyer('brood',W.sid,{});let e=W.ents.find(x=>x.tok===g);if(!e){inW(W,()=>spawnFrigate(g,false));e=W.ents.find(x=>x.tok===g)}e.x=0;e.y=4000;e.z=0;qLook(0,0,1,0,1,0,e.q);
      const v=[];for(let i=0;i<3;i++){const n=makeNPC('patrol','ostrova','interceptor',1,{},null);n.x=e.x+(i-1)*20;n.y=e.y;n.z=e.z+500+i*600;W.ents.push(n);v.push(n)}const h0=v.map(n=>n.hull);
      const hits=mawFire(e,DST.maw);return JSON.stringify({sCap:e.st.sCap,shield:e.shield,cap:broodCap(g),hits,alive:v.map(n=>n.alive),mdl:!!shipMesh('brood','frigate').mdl})})()"""))
    print('ledger',await ev(LED))
    print('your destroyer',await ev("""(()=>{const P=S.player;exitSector();const sid=SECTOR_DEFS.map(d=>d.id).find(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id]);P.sector=sid;P.docked=null;enterSector(sid);P.cls='bulker';fitOf(P);refreshPlayerStats();devLedger(()=>{P.cargo={frame:2}});depFresh(P);
      const R=S.stations[sid];devLedger(()=>{inv.add(R.stock,'keel',1);inv.add(R.stock,'frame',6);inv.add(R.stock,'seal',1);inv.add(R.stock,'plate',100);inv.add(R.stock,'coil',20)});staUp(P,R);const b=[];for(const k of['yard','storage','defence'])b.push(staBuild(P,R,k));
      const low=capBuild(P,R,'dst');staBuild(P,R,'hangar');devLedger(()=>{inv.addAll(R.stock,dstCost('player'))});const m=capBuild(P,R,'dst');const ev=S.events.find(e=>e.type==='dstbuild'&&e.att===yardKeyOf(R));S.T=ev.until+1;dstTick();const t=S.frigates.find(x=>isDst(x)&&fMine(x));
      $('company').hidden=false;coTab='holdings';renderCompany();const btn=!!$('coBody').querySelector('[data-arg$=":dst"]');$('company').hidden=true;
      return JSON.stringify({low,m,lvl:staLvl(R),mine:!!t,side:t&&t.side,aload:t&&t.aload,btn,again:capBuild(P,R,'dst')})})()"""))
    print('ledger',await ev(LED))
    print('ravager',await ev("""(()=>{const t=makeCarrier('pirate',S.player.sector,{});let e=W.ents.find(x=>x.tok===t);return JSON.stringify({name:capName(t),mdl:!!shipMesh('pirate','carrier').mdl,gun:!!(e&&mgSpec(e)),spec:e&&mgSpec(e)})})()"""))
    print('no sloops',await ev("""(()=>{S.T=4000;for(let i=0;i<20;i++)pirTick();return JSON.stringify(S.events.filter(e=>e.type==='pirbuild').map(e=>e.cls))})()"""))
    print('ledger',await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
