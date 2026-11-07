# usage: python3 tools/tests/mp_contractor.py $PWD/index.html  (needs Playwright with Chromium)
# Beyond stage 1 over the faked link: host and guest both start as independent contractors at freeports; the guest's ship
# flies as its own side on the host, AI hostility to it follows the guest's own standing, its bounty is paid by its job's issuer
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
    await ev(C,"(()=>{selFac='varkesh';mpLaunch('varkesh','interceptor','ew');return 1})()");await C.wait_for_timeout(4000)
    print('guest joined:',await ev(C,"(()=>JSON.stringify({running,sworn:S.player.sworn,home:S.player.home,fac:S.player.faction,sector:S.player.sector,docked:S.player.docked}))()"))
    print('host sees guest:',await ev(H,"(()=>{const P=S.pilots.clipid1;return JSON.stringify({sworn:P.sworn,home:P.home,sector:P.sector,stand:P.stand})})()"))
    # the guest undocks: its ship flies on the host as an independent (side Compact), and hostility to it follows the guest's own standing
    await ev(C,"(()=>{undock();return 1})()");await C.wait_for_timeout(3000)
    print('guest ship on host:',await ev(H,"(()=>{const e=MP.rp.clipid1;if(!e)return 'no ship';return JSON.stringify({side:e.side,fac:e.fac,varkesh:hostE('varkesh',e),brood:hostE('brood',e)})})()"))
    # an independent pilot (simulated on the host) flies in the guest's system: the guest sees its label, and has the
    # independents in its synced state for the freeport's Overview
    print('independent on host:',await ev(H,"(()=>{indInit();const sid=S.pilots.clipid1.sector,w=WORLDS[sid];if(!w)return 'no world for the guest';const I=indL().find(x=>!x.live&&x.at!=='job');I.sector=sid;I.at='fly';I.path=[sid,NEIGH[sid][0]];I.leg=0;I.go={k:'look'};const e=inW(w,()=>indSpawn(I,false));window._IE=e&&e.id;return JSON.stringify({sid,name:I.name,id:e&&e.id,label:e&&shipLabel(e)})})()"))
    # the host's state reaches the guest with its five-second sync (the host's clock runs slowly under the test renderer)
    g=None
    for i in range(12):
      await C.wait_for_timeout(2500)
      g=json.loads(await ev(C,"(()=>{const L=Object.values((LW&&LW.pup)||{}).filter(e=>e.indLbl).map(e=>shipLabel(e));return JSON.stringify({labels:L,synced:((S.ind&&S.ind.L)||[]).length,overview:indDockedHtml(S.ind&&S.ind.L[0]?S.ind.L[0].home:'mw').includes('Independents here')})})()"))
      if g['synced'] and g['labels']:break
    print('guest sees independents:',json.dumps(g))
    if not g['labels'] or not all(x.startswith('Independent · ') for x in g['labels']) or not g['synced'] or not g['overview']:errs.append('guest view of independents: '+json.dumps(g))
    print('guest hated by Varkesh:',await ev(H,"(()=>{const P=S.pilots.clipid1,e=MP.rp.clipid1;P.stand.varkesh=-70;const a=hostE('varkesh',e),b=hostE('halcyon',e);P.stand.varkesh=0;return JSON.stringify({varkesh:a,halcyon:b,hostStillFine:hostile('varkesh','player')})})()"))
    print('guest job and pay:',await ev(H,"(()=>{relInit();S.rel.varkesh.ostrova=S.rel.ostrova.varkesh=-60;Object.assign(pairOf('varkesh','ostrova'),{war:true,warT:S.T});const P=S.pilots.clipid1;P.job={by:'ostrova',kind:'fight'};const t0=S.econ.treasury.ostrova,c0=P.credits;payKill({side:'varkesh',role:'patrol',cls:'interceptor',tier:1,dmg:{clipid1:100}},null,{src:MP.rp.clipid1});P.job=null;return JSON.stringify({got:P.credits-c0,fromOstrova:t0-S.econ.treasury.ostrova})})()"))
    await C.wait_for_timeout(8000)
    print('guest sees standing:',await ev(C,"JSON.stringify(S.player.stand)"))
    print('ledger:',await ev(H,"(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e);return b.length?'DRIFT '+b:'exact'})()"))
    print('errors',[e for e in errs if 'GL Driver' not in e][:8]);await b.close()
asyncio.run(main())
