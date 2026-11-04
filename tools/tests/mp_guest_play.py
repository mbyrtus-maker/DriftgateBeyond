# usage: python3 tools/tests/mp_guest_play.py $PWD/index.html  (needs Playwright with Chromium)
# Beyond, 4 Nov 2026: a guest plays over the faked link. Combat through the real input path (the guest aims and holds fire;
# the host fires its guns, the raider dies, a power pays the bounty); drones (a Light Miner taken at the yard comes with its
# controller and drones, they launch on the host and show on the guest, lost ones refill at Rearm when it docks); every dock menu on the guest's screen (Market categories, Fabricate, Loadout's parts and Fit, the shipyard
# dropdown, Hangar, Jobs, Allegiance), Comms Jobs here in flight and the Company screen; no errors; the ledger stays exact
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
    G=lambda c:ev(C,c)
    Hh=lambda c:ev(H,c)
    LED="(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(1));return b.length?'DRIFT '+b:'exact'})()"
    print('guest joined:',await G("(()=>JSON.stringify({running,fac:S.player.faction,cls:S.player.cls,sector:S.player.sector,docked:S.player.docked,fit:fitOf(S.player).w}))()"))
    # ---------------- menus, docked, on the guest's screen
    menus="""(()=>{const out={};const tabs=['home','market','bmk','trade','fab','jobs','upg','ship','storage','refit','allegiance'];for(const t of tabs){try{dockTab=t;renderDock();out[t]=dockTab===t?document.getElementById('dBody').innerText.length:'(not here)'}catch(e){out[t]='ERR '+e.message}}
      return JSON.stringify({tabs:out,top:[...document.querySelectorAll('#dTabs .mtab')].map(b=>b.textContent.replace(/[0-9]/g,'').trim()).join('|')})})()"""
    print('guest menus:',await G(menus))
    print('market categories:',await G("(()=>{dockTab='market';mkFilter='none';renderDock();const boxes=[...document.querySelectorAll('.obox')].map(b=>b.textContent.trim());const u=document.querySelector('.obox[data-arg=util]');if(u)u.click();const tiles=document.querySelectorAll('.mkt').length;return JSON.stringify({boxes,utilTiles:tiles,picked:mkFilter})})()"))
    print('fabricate:',await G("(()=>{dockTab='fab';fabKind=null;renderDock();const b=[...document.querySelectorAll('.obox')].map(x=>x.textContent.trim());const w=document.querySelector('.obox[data-arg=wpn]');if(w)w.click();return JSON.stringify({boxes:b,rows:document.querySelectorAll('#dBody tbody tr').length})})()"))
    print('shipyard:',await G("(()=>{dockTab='ship';renderDock();const s=document.getElementById('yardSelEl');if(!s)return 'no dropdown';const groups=[...s.querySelectorAll('optgroup')].map(g=>g.label+':'+g.children.length);s.value='skiff';s.dispatchEvent(new Event('change'));const btn=document.querySelector('.ydleft .act button');return JSON.stringify({groups,picked:yardSel,btn:btn&&btn.textContent,card:!!document.querySelector('.ydcard .cls')})})()"))
    # take the Light Miner through the dock (a guest's dock action runs on the host)
    await G("(()=>{document.querySelector('.ydleft .act button').click();return 1})()");await C.wait_for_timeout(2500)
    print('light miner (host):',await Hh("(()=>{const P=S.pilots.clipid1;return JSON.stringify({cls:P.cls,w:fitOf(P).w,u:fitOf(P).u,bay:P.bay,ctl:drnCtl(P)})})()"))
    print('light miner (guest):',await G("(()=>JSON.stringify({cls:S.player.cls,w:fitOf(S.player).w,u:fitOf(S.player).u,bay:S.player.bay,msg:dockErr.slice(0,160)}))()"))
    print('loadout parts:',await G("(()=>{dockTab='upg';ldSel='parts';renderDock();const t=document.querySelector('.ldr');const plus=document.querySelectorAll('.ldplus').length;return JSON.stringify({panel:t?t.innerText.slice(0,120).split(String.fromCharCode(10)).join(' | '):'none',plus})})()"))
    print('hangar:',await G("(()=>{dockTab='storage';renderDock();return [...document.querySelectorAll('#dBody .h3')].map(x=>x.textContent).join(' | ')})()"))
    print('allegiance:',await G("(()=>{dockTab='allegiance';renderDock();const t=document.getElementById('dBody').innerText;return /AUDIENCE/.test(t)?'audience panel shown':'no audience panel (contractor at a freeport: right)'})()"))
    # ---------------- drones in flight
    await G("(()=>{dockTab='home';undock();return 1})()");await C.wait_for_timeout(3500)
    print('drones on host:',await Hh("(()=>{const e=MP.rp.clipid1;const L=[];for(const w of Object.values(WORLDS))for(const d of w.ents)if(d.role==='drone'&&d.mom===e&&d.alive)L.push(d);window._GD=L;return JSON.stringify({n:L.length,hull:L[0]&&Math.round(L[0].st.hull),bay:S.pilots.clipid1.bay})})()"))
    print('drones on guest:',await G("(()=>{const L=W.ents.filter(e=>e.role==='drone'&&e.alive);return JSON.stringify({n:L.length,mine:L.filter(d=>d.mom===W.player).length})})()"))
    print('comms jobs here:',await G("(()=>{W.ftgt=W.player;openComms();cycleFriendly();const r=$('cmTo').textContent+' || '+W.cmOpts.map(o=>o.l).slice(0,3).join(' | ');closeComms();return r})()"))
    print('company screen:',await G("(()=>{toggleCompany();const ok=!$('company').hidden;const t=$('company').innerText.length;toggleCompany();return ok+' '+t})()"))
    # lose both drones on the host, dock: the bay refills at Rearm (built by the freeport, paid)
    print('drones lost:',await Hh("(()=>{for(const d of _GD){d.shield=0;inW(worldOf(d),()=>damageShip(d,9999,'brood',null,'kinetic'))}return _GD.filter(d=>d.alive).length})()"))
    c0=await G("S.player.credits")
    await G("(()=>{const P=S.player;P.docked='station';netSend({t:'dock',d:'station'});openDock('ship');return 1})()");await C.wait_for_timeout(3000)
    print('rearm on dock:',await Hh("(()=>{const P=S.pilots.clipid1;return JSON.stringify({docked:P.docked,bay:P.bay})})()"),'| guest paid',c0-(await G("S.player.credits")),'|',await G("dockErr.slice(0,120)"))
    # ---------------- combat through the input path: back in a fighter, a raider pinned ahead, the guest aims and holds fire
    await G("(()=>{netSend({t:'act',act:'hull',arg:'interceptor'});return 1})()");await C.wait_for_timeout(2500)
    await G("(()=>{undock();return 1})()");await C.wait_for_timeout(2000)
    # out of the freeport's guns' reach, so the guest's own guns do the work
    await G("(()=>{const p=W.player,E=W.stationEnt;p.x=E.x+4500;p.y=E.y+300;p.z=E.z;p.vx=p.vy=p.vz=0;return 1})()");await C.wait_for_timeout(2000)
    print('raider:',await Hh("""(()=>{const g=MP.rp.clipid1,w=worldOf(g);let e=null;inW(w,()=>{e=spawnNPC('pirate','pirate',true);e.x=g.x+260;e.y=g.y;e.z=g.z;e.vx=e.vy=e.vz=0;e.shield=0;e.hull=e.st.hull*.25});window._RE=e;
      window._pin=setInterval(()=>{if(e.alive){e.x=g.x+260;e.y=g.y;e.z=g.z;e.vx=g.vx;e.vy=g.vy;e.vz=g.vz;e.shield=0}},50);return e.id+' hull '+Math.round(e.hull)})()"""))
    await C.wait_for_timeout(2000)
    rid=await Hh("_RE.id")
    c1=await G("S.player.credits")
    print('guest aims:',await G("""(()=>{const T=W.ents.find(e=>e.id===%s);window._aim=0;if(!T)return 'not seen: '+W.ents.filter(e=>e.type==='ship').map(e=>e.id+':'+e.role).join(',');W.tgt={kind:'ship',ref:T};S.player.wpn='laser';window._aim=setInterval(()=>{const p=W.player;if(!T.alive)return;faceInstant(p,T.x-p.x,T.y-p.y,T.z-p.z);p.vx=p.vy=p.vz=0},40);keys.Space=true;return 'ok '+Math.round(d3(T,W.player))+' m'})()""" % json.dumps(rid)))
    for i in range(20):
      if await Hh("!_RE.alive"):break
      await C.wait_for_timeout(500)
    await G("(()=>{keys.Space=false;clearInterval(_aim);return 1})()");await Hh("(()=>{clearInterval(_pin);return 1})()")
    await C.wait_for_timeout(2500)
    print('raider dead (host):',await Hh("JSON.stringify({dead:!_RE.alive,kills:S.pilots.clipid1.kills||0})"))
    print('bounty (guest):',(await G("S.player.credits"))-c1,'cr |',await G("FEED.slice(-5).map(f=>f.msg).filter(m=>/bount|Unbound|raider|\\+/i.test(m)).join(' / ').slice(0,200)"))
    print('ledger:',await Hh(LED))
    print('errors',[e for e in errs if 'favicon' not in e][:8]);await b.close()
asyncio.run(main())
