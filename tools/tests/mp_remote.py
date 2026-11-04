# usage: python3 tools/tests/mp_remote.py $PWD/index.html  (needs Playwright with Chromium)
# Beyond, 3 Nov 2026, over the faked link: a flying guest runs its company from the Company screen and the map (fees, a
# crew's job) on the host; a dock-only action is still refused in flight; a guest's cargo scan gets the reading from the
# host (rough, then exact) and the host runs the noticing; the ledger stays exact
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
    print('guest joined:',await ev(C,"(()=>JSON.stringify({running,fac:S.player.faction,sector:S.player.sector,docked:S.player.docked}))()"))
    await ev(C,"(()=>{undock();return 1})()");await C.wait_for_timeout(3000)
    # the host gives the guest a depot in an empty system, with a crew
    print('guest depot:',await ev(H,"""(()=>{const sid=SECTOR_DEFS.map(d=>d.id).filter(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id])[0];let R;runAs('clipid1',()=>{R=depMake(S.player,sid,stationSite(sid),{},{});R.crew.push({id:1,name:'Crew Test',cls:'skiff',job:'idle'})});window._D=sid;return sid+' '+R.pid})()"""))
    await H.wait_for_timeout(5000)
    D=await ev(H,"_D")
    # fees from the Company screen while flying
    print('fee from flight:',await ev(C,"(()=>{coClick('feeset','%s:dock:1');coClick('feeset','%s:dock:1');return S.player.docked+' '+coErr})()" % (D,D)))
    await C.wait_for_timeout(1500)
    print('host fee:',await ev(H,"JSON.stringify(feeOf(S.stations[_D]))"))
    # a crew's job from the map while flying
    print('crew job from map:',await ev(C,"(()=>{mapSel='%s';mpPick.clear();mpPick.add('c:%s:1');mpOrder('crew','mine');return mpMsg})()" % (D,D)))
    await C.wait_for_timeout(1500)
    print('host crew:',await ev(H,"S.stations[_D].crew[0].job"))
    # a dock-only action is still refused in flight
    await ev(C,"(()=>{netSend({t:'act',act:'sellhold',arg:''});return 1})()");await C.wait_for_timeout(1000)
    print('dock-only refused:',await ev(C,"dockErr"))
    # the cargo scan: the guest fits a cargo scanner; a Halcyon supply freighter beside it
    print('scan setup:',await ev(H,"""(()=>{const P=S.pilots.clipid1;devLedger(()=>{fitOf(P).u[0]='cscan'});const e0=MP.rp.clipid1,w=worldOf(e0);let t=null;devLedger(()=>{t=haulSend('halcyon',w.sid,FAC_HOME('halcyon'),{plate:12,wire:5},'mptest','supplies')});const T=w.ents.find(e=>e.type==='ship'&&e.alive&&e.tradeT===t);if(!T)return 'no ship in '+w.sid;T.x=e0.x+300;T.y=e0.y;T.z=e0.z;devLedger(()=>{if(t.load&&Object.keys(t.load).length)t.load={plate:12,wire:5};else T.cargo={plate:12,wire:5}});window._T=T;return T.id+' '+T.role+' in '+w.sid})()"""))
    await ev(H,"(()=>{const e0=MP.rp.clipid1;window._hold=setInterval(()=>{if(_T&&e0){_T.x=e0.x+300;_T.y=e0.y;_T.z=e0.z;_T.vx=e0.vx;_T.vy=e0.vy;_T.vz=e0.vz}},100);return 1})()")
    await C.wait_for_timeout(2500)
    tid=await ev(H,"_T.id")
    print('guest targets:',await ev(C,"(()=>{fitOf(S.player).u[0]='cscan';const T=W.ents.find(e=>e.id===%s);if(!T)return 'not seen: '+W.sid+' '+W.ents.filter(e=>e.type==='ship').map(e=>e.id+':'+e.role).join(',');W.tgt={kind:'ship',ref:T};return 'ok '+d3(T,W.player).toFixed(0)})()" % json.dumps(tid)))
    await C.wait_for_timeout(1500)
    print('rough:',await ev(C,"(()=>{const T=W.tgt&&W.tgt.ref;if(!T)return 'no target';return JSON.stringify({seen:!!(T._csc&&T._csc.seen),C:T._cscC||null,txt:(document.querySelector('#hTgt .tp')||{}).innerText||''})})()"))
    await C.wait_for_timeout(12000)
    print('exact:',await ev(C,"(()=>{const T=W.tgt&&W.tgt.ref;if(!T)return 'no target';return JSON.stringify({done:!!(T._csc&&T._csc.done),p:T._csc&&T._csc.p,C:T._cscC||null,d:d3(T,W.player)|0,same:W.tgt.ref===W.ents.find(e=>e.id===T.id)})})()"))
    print('host reading:',await ev(H,"(()=>{const oW=W;W=worldOf(_T);try{return JSON.stringify(cscLoad(_T))}finally{W=oW}})()"))
    print('ledger:',await ev(H,"(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(1));return b.length?'DRIFT '+b:'exact'})()"))
    print('errors',errs[:8]);await b.close()
asyncio.run(main())
