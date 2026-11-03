# Beyond stage 3: weapon and utility slots. Default fits per hull; the machine gun spends rounds; unfitted weapons refuse;
# payload never reloads in flight; a pilot's missiles hit twice as hard; docking rearms, paid to the treasury (credits exact);
# the landing kit gates landing; cargo modules add hold; the mining laser cuts ore along a rock's ring (ledger exact) and a
# blast breaks the ring; the Loadout section renders; a minute of flight with no simulation errors
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
    await ev("(()=>{S.player.rp=5000;window.give=(k,n)=>devLedger(()=>inv.add(S.player.vault,k,n||1));window.FC={storageName:'Vault',get storage(){return S.player.vault}};return 1})()")
    print('start',await ev("(()=>{const P=S.player;magTick(P,.1);return JSON.stringify({cls:P.cls,fit:fitOf(P),ammo:P.ammo,rack:P.rack,rackCap:pRack(P)})})()"))
    print('slots',await ev("JSON.stringify(Object.fromEntries(['interceptor','striker','heavy','bomber','skiff','prospector','dredger','courier','freighter','bulker'].map(k=>[k,slotsOf(k).w.length+'w '+slotsOf(k).u.length+'u'])))"))
    print('allowed',await ev("JSON.stringify({fighterMine:wpnOK('interceptor','mlaser',0),minerMine:wpnOK('prospector','mlaser',1),bomberTorp0:wpnOK('bomber','torpedo',0),bomberMsl:wpnOK('bomber','missile',1),fighterTorp:wpnOK('interceptor','torpedo',0)})"))
    # the gun spends a round a shot; with none left it stays silent
    print('gun',await ev("""(()=>{undock();const P=S.player,e=W.player;P.wpn='kinetic';P.ammo=10;e.cool=0;e.energy=e.st.eCap;e.boot=0;const lf=e.lastFire;fire(e);const a=P.ammo,fired=e.lastFire!==lf;
      P.ammo=0;e.cool=0;const lf2=e.lastFire;fire(e);const r={afterShot:a,fired,firedEmpty:e.lastFire!==lf2};P.ammo=ammoCap(P);return JSON.stringify(r)})()"""))
    print('no laser',await ev("""(()=>{const P=S.player;give('pt_msl');const m=fitDo(FC,P,'w:1:missile');setWeapon('laser');const r={msg:m,wpn:P.wpn,rackCap:pRack(P),laserInVault:P.vault.pt_laser||0};fitDo(FC,P,'w:1:laser');return JSON.stringify(r)})()"""))
    print('no reload in flight',await ev("""(()=>{const P=S.player;P.rack=0;magTick(P,200);return JSON.stringify({rack:P.rack,mslT:P.mslT})})()"""))
    print('missile damage',await ev("""(()=>{const e=W.player;launchMissile(e,null,1,'missile');const m=W.missiles[W.missiles.length-1];const r={dmg:Math.round(m.dmg),base:Math.round(missileDmg(1)*((e.st&&e.st.mslK)||1))};W.missiles.pop();return JSON.stringify(r)})()"""))
    # the landing kit
    print('landing',await ev("""(()=>{const P=S.player,e=W.player,s=S.sectors[W.sid],a=s.ast[0];if(!a)return 'no rock';const R=astR(a);e.x=a.x+R+e.st.radius+10;e.y=a.y;e.z=a.z;e.vx=e.vy=e.vz=0;
      const w=!!landCandidate();fitDo(FC,P,'u:0:');const wo=!!landCandidate();fitDo(FC,P,'u:0:land');return JSON.stringify({withKit:w,withoutKit:wo})})()"""))
    print('ledger',await ev(LED))
    # rearm at the freeport: paid to its treasury, credits stay exact
    print('rearm',await ev("""(()=>{const P=S.player;P.ammo=100;P.rack=0;exitSector();enterSector(P.sector);P.docked='station';const c=dockCtx(),c0=P.credits,t0=S.econ.treasury[c.wallet],q=rearmQuote(P);
      const msg=rearmDo(c,P);return JSON.stringify({quote:q.tot,paid:c0-P.credits,toTreasury:S.econ.treasury[c.wallet]-t0,ammo:P.ammo,rack:P.rack,msg})})()"""))
    print('auto rearm on dock',await ev("""(()=>{const P=S.player;P.ammo=5;openDock('ship');return JSON.stringify({ammo:P.ammo,cap:ammoCap(P),feed:(FEED[0]||{}).t||(FEED[0]||{}).msg||''})})()"""))
    print('loadout tab',await ev("""(()=>{dockTab='ship';renderDock();const t=document.querySelector('#dBody').innerText;const i=t.indexOf('LOADOUT')>=0?t.indexOf('LOADOUT'):t.indexOf('Loadout');return t.slice(i,i+300).replace(/\\n/g,' | ')})()"""))
    print('ledger',await ev(LED))
    # a courier's cargo module
    print('cargo module',await ev("""(()=>{const P=S.player,c0=P.cls;P.cls='courier';const F=fitOf(P);const moved={w:F.w.slice(),u:F.u.slice(),vault:{laser:P.vault.pt_laser||0,msl:P.vault.pt_msl||0}};give('pt_cargo');const m=fitDo(FC,P,'u:1:cargo');const a=W.player.st.cargo;fitDo(FC,P,'u:1:');const b=W.player.st.cargo;
      P.cls=c0;fitOf(P);fitDo(FC,P,'w:1:laser');fitDo(FC,P,'w:2:missile');refreshPlayerStats();return JSON.stringify({moved,msg:m,withModule:a,without:b,base:CLASSES.courier.cargo,back:fitOf(P).w})})()"""))
    # the mining laser on a Medium Miner: on the ring it cuts ore into the hold, off it only sparks
    print('mining laser',await ev("""(()=>{undock();const P=S.player,e=W.player;P.cls='prospector';fitOf(P);give('pt_mlaser');give('pt_charge');fitDo(FC,P,'w:0:charge');fitDo(FC,P,'w:1:mlaser');refreshPlayerStats();magTick(P,.1);P.mtool='mlaser';P.cargo={};const s=S.sectors[W.sid];
      const a=s.ast.filter(x=>!x.comet&&oreTotal(x)>0).sort((x,y)=>oreTotal(y)-oreTotal(x))[0];if(!a)return 'no rock';const n=ringN(a),R=astR(a),ax=Math.abs(n.x)<.9?{x:1,y:0,z:0}:{x:0,y:1,z:0};let w={x:n.y*ax.z-n.z*ax.y,y:n.z*ax.x-n.x*ax.z,z:n.x*ax.y-n.y*ax.x};const l=hyp(w.x,w.y,w.z);w={x:w.x/l,y:w.y/l,z:w.z/l};
      const put=(d)=>{e.x=a.x+d.x*(R+150);e.y=a.y+d.y*(R+150);e.z=a.z+d.z*(R+150);faceInstant(e,-d.x,-d.y,-d.z);e.vx=e.vy=e.vz=0};put(w);const o0=oreTotal(a);let r='';
      for(let i=0;i<40;i++){e.energy=e.st.eCap;r=mlCut(e,P,a,1,s)}const on={result:r,cut:o0-oreTotal(a),hold:invMass(P.cargo),beam:mlBeam(e,a)};put(n);e.energy=e.st.eCap;const off=mlCut(e,P,a,1,s);
      window._A=a;return JSON.stringify({on,offRing:off,rate:mlRate(P)})})()"""))
    print('ledger',await ev(LED))
    print('blast breaks ring',await ev("""(()=>{const P=S.player,e=W.player,s=S.sectors[W.sid],a=_A;P.blN=blCap(P);s.charges=s.charges||[];const pt=blPts(a)[0];s.charges.push({id:S.nextId++,o:blKey(P),side:e.side,a:a.id,wp:false,x:pt.x,y:pt.y,z:pt.z,pi:0,q:'on'});
      e.x=a.x+2000;blDetonate(P,e);return JSON.stringify({noRing:!!a.noRing,ringOK:ringOK(a)})})()"""))
    print('ledger',await ev(LED))
    # stage 4: parts are items; build one at the freeport workshop, upgrade a fitted part a grade, ledger exact
    print('parts',await ev("JSON.stringify({gun:ITEMS.pt_gun,mass:mass('pt_gun'),inOrder:ITEM_ORDER.includes('pt_laser'),craft:CRAFTABLE.includes('pt_scan'),fpStock:mkStock(S.stations[S.player.home]).pt_gun||0})"))
    print('upgrade',await ev("""(()=>{const P=S.player,F=fitOf(P),i=F.w.indexOf('mlaser'),r0=mlRate(P);give('plate',2);give('wire',2);const q=pupQuote(FC,P,'w:'+i);const m=pupDo(FC,P,'w:'+i);return JSON.stringify({q:q&&q.r,msg:m,grade:F.g[i],rate0:r0,rate1:mlRate(P)})})()"""))
    print('ledger',await ev(LED))
    print('hud',await ev("(()=>{const P=S.player;P.cls='interceptor';fitOf(P);fitDo(FC,P,'w:0:gun');refreshPlayerStats();magTick(P,.1);P.wpn='kinetic';hudUpdate();return document.getElementById('hWpn').textContent})()"))
    await pg.wait_for_timeout(60000)
    print('after a minute',await ev("JSON.stringify({T:Math.round(S.T),ammo:S.player.ammo})"),await ev(LED))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
