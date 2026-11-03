# usage: python3 tools/tests/mp_beyond.py $PWD/index.html  (needs Playwright with Chromium)
# Beyond's late additions over the faked link: a guest in the host's system sees the new models (destroyers, the Gullet,
# escorts and carriers, Unbound and work ships) as the host spawns them; a destroyer duel and the Gullet's beam play out
# with the guest watching; the guest buys a Medium Miner through the dock and cuts ore with the mining laser on the host;
# no errors on either page, ledger exact
import asyncio,json,sys
from playwright.async_api import async_playwright
FILE=sys.argv[1]
LINK=r"""(to)=>{window.__mk=(peer,fn)=>({peer,open:true,dead:false,parts:{},n:'',r:{readyState:'open',send:s=>fn(s)},u:{readyState:'open',send:s=>fn(s)},pc:{close(){},connectionState:'connected'}});return 1}"""
async def boot(ctx,name,errs):
  pg=await ctx.new_page();pg.on('pageerror',lambda e:errs.append(name+': '+str(e.stack)[:500]))
  pg.on('console',lambda m:errs.append(name+' console: '+m.text[:400]) if m.type in ('error','warning') and 'TUNNEL' not in m.text and 'fonts' not in m.text else None)
  await pg.goto('file://'+FILE+'?name='+name,timeout=400000);await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=400000)
  await pg.evaluate("c=>__dg.ev(c)",f"(()=>{{$('mpName').value='{name}';legGrant('{name}','halcyon',true,'interceptor',null);return 1}})()")
  return pg
async def ev(pg,code):
  return await pg.evaluate("c=>__dg.ev(c)",code)
async def main():
  errs=[]
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows'])
    H=await boot(await b.new_context(viewport={'width':1200,'height':800}),'Hosty',errs);C=await boot(await b.new_context(viewport={'width':1200,'height':800}),'Clie',errs)
    async def toC(s):
      try:await C.evaluate("d=>{if(window.MPHOST_READY)__dg.ev('linkRecv(MP.host,'+JSON.stringify(d)+')')}",s)
      except Exception as e:errs.append('relay->C '+str(e)[:200])
    async def toH(s):
      try:await H.evaluate("d=>__dg.ev('linkRecv(window.__HL,'+JSON.stringify(d)+')')",s)
      except Exception as e:errs.append('relay->H '+str(e)[:200])
    await H.expose_function('__toClient',toC);await C.expose_function('__toHost',toH)
    await H.evaluate(LINK);await C.evaluate(LINK)
    print('host:',await ev(H,"(()=>{MP.pid='hostpid1';MP.name='Hosty';MP.code='crew';MP.cl={};MP.rp={};MP.inp={};MP.roster=[];hostBegin(false);selFac='halcyon';mpLaunch('halcyon','interceptor','mw');window.__HL=__mk('cli',s=>__toClient(s));return JSON.stringify({sworn:S.player.sworn,home:S.player.home,sector:S.player.sector})})()"))
    await H.wait_for_timeout(1500)
    await ev(C,"(()=>{NET.on=true;NET.cl=true;NET.host=false;MP.pid='clipid1';NET.me=MP.pid;MP.name='Clie';MP.code='crew';MP.roster=[];MP.host=__mk('host',s=>__toHost(s));window.MPHOST_READY=1;linkUp(MP.host);return 1})()")
    await C.wait_for_timeout(2500)
    await ev(C,"(()=>{selFac='varkesh';mpLaunch('halcyon','interceptor','mw');return 1})()");await C.wait_for_timeout(4000)
    print('guest joined:',await ev(C,"(()=>JSON.stringify({running,sector:S.player.sector,docked:S.player.docked}))()"))
    # a Medium Miner bought through the dock, then the mining laser on the host
    await ev(H,"(()=>{const P=S.pilots.clipid1;devLedger(()=>{P.credits+=20000});P.rp=5000;return 1})()")
    await ev(C,"(()=>{netSend({t:'act',act:'hull',arg:'prospector'});return 1})()");await C.wait_for_timeout(3000)
    await ev(H,"(()=>{const P=S.pilots.clipid1;if(P.cls==='prospector'&&!mtools(P).includes('mlaser'))devLedger(()=>{const F=fitOf(P);const i=F.w.findIndex((k,j)=>wpnOK(P.cls,'mlaser',j));F.w[i>=0?i:0]='mlaser'});return 1})()");await C.wait_for_timeout(1500)
    print('guest hull:',await ev(H,"(()=>{const P=S.pilots.clipid1;return JSON.stringify({cls:P.cls,docked:P.docked,tools:mtools(P),cr:Math.round(P.credits)})})()"))
    await ev(C,"(()=>{undock();return 1})()");await C.wait_for_timeout(2500)
    print('spawn on host:',await ev(H,"""(()=>{relInit();S.rel.halcyon.varkesh=S.rel.varkesh.halcyon=-60;Object.assign(pairOf('halcyon','varkesh'),{war:true,warT:S.T});const g=MP.rp.clipid1||W.player,out=[];
      const put=(t,dx,dz)=>{let e=W.ents.find(x=>x.tok===t);if(!e){inW(W,()=>spawnFrigate(t,false));e=W.ents.find(x=>x.tok===t)}if(e){e.x=g.x+dx;e.y=g.y+120;e.z=g.z+dz;t.dest=W.sid}out.push(e?e.cls+':'+e.side:'none')};
      put(makeDestroyer('halcyon',W.sid,{}),900,600);put(makeDestroyer('varkesh',W.sid,{}),1500,600);put(makeDestroyer('brood',W.sid,{}),-1600,900);put(makeEscort('ostrova',W.sid,{}),-900,-900);put(makeCarrier('varkesh',W.sid,{}),2000,-1500);
      for(const[c,f]of[['raider','pirate'],['prospector','varkesh'],['scout','ostrova']]){const e=makeNPC('miner',f,c,1,{},null);e.role='og';e.x=g.x+300;e.y=g.y;e.z=g.z-400;W.ents.push(e);out.push(c)}return out.join(' ')})()"""))
    await C.wait_for_timeout(4000)
    print('guest sees:',await ev(C,"""(()=>{const L=W.ents.filter(e=>e.type==='ship'&&(e.role==='frigate'||['raider','prospector','scout'].includes(e.cls)));return JSON.stringify(L.map(e=>{const m=shipMesh(e.side==='pirate'?'pirate':e.fac,e.cls);return e.cls+':'+(e.side||e.fac)+':'+(m&&m.mdl?'model':'old')}))})()"""))
    await C.wait_for_timeout(20000)
    print('after the fight (host):',await ev(H,"""JSON.stringify((S.frigates||[]).filter(t=>t.sector===W.sid).map(t=>capName(t)+':'+t.side+':'+Math.round(t.hull)))"""))
    print('guest beams seen:',await ev(C,"JSON.stringify({beams:(W.beams||[]).length,ents:W.ents.length})"))
    await ev(C,"(()=>{undock();return 1})()");await C.wait_for_timeout(3000)
    print('laser set:',await ev(C,"""(()=>{const P=S.player;P.mtool='mlaser';const s=S.sectors[W.sid],SE=W.stationEnt;const a=s.ast.filter(x=>!x.comet&&!x.rift&&ringOK(x)&&oreTotal(x)>=30&&(!SE||d3(x,SE)>1500)).sort((x,y)=>d3(x,W.player)-d3(y,W.player))[0];if(!a)return 'no rock';
      const p=W.player,n=ringN(a);let d={x:-n.z,y:0,z:n.x};const l=Math.hypot(d.x,d.y,d.z)||1;d.x/=l;d.z/=l;const R=astR(a)+60;p.x=a.x+d.x*R;p.y=a.y;p.z=a.z+d.z*R;p.vx=p.vy=p.vz=0;faceInstant(p,-d.x,0,-d.z);W.tgt={kind:'ast',ref:a};keys.KeyF=true;window._rk=a.id;return 'rock '+a.id})()"""))
    for i in range(40):
      await C.wait_for_timeout(2000)
      if await ev(H,"invMass(S.pilots.clipid1.cargo)")>=1:break
    await ev(C,"(()=>{keys.KeyF=false;return 1})()")
    print('guest cut:',await ev(H,"(()=>{const P=S.pilots.clipid1;return JSON.stringify(P.cargo)})()"))
    print('ledger:',await ev(H,"(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(1));return b.length?'DRIFT '+b:'exact'})()"))
    print('errors',errs[:8]);await b.close()
asyncio.run(main())
