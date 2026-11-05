# Shared harness for the Beyond guest tests over the faked link (two pages in one Chromium; the host relays to the guest
# through exposed functions). Host: a Halcyon contractor ('mw'); guest: a Varkesh contractor in an Interceptor ('ew').
#   from mpkit import run
#   async def body(K): ...   K.H / K.C pages, await K.G(js) on the guest, await K.Hh(js) on the host, K.check(name, ok, info)
#   run(body)
import asyncio,json,sys,os
from playwright.async_api import async_playwright
FILE=sys.argv[1] if len(sys.argv)>1 else os.path.abspath('index.html')
LINK=r"""(to)=>{window.__mk=(peer,fn)=>({peer,open:true,dead:false,parts:{},n:'',r:{readyState:'open',send:s=>fn(s)},u:{readyState:'open',send:s=>fn(s)},pc:{close(){},connectionState:'connected'}});return 1}"""
LED="(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(1));return b.length?'DRIFT '+b:'exact'})()"
HP="S.pilots.clipid1"
class Kit:
  def __init__(s):s.fails=[];s.errs=[]
  def check(s,name,ok,info=''):
    print(('ok   ' if ok else 'FAIL ')+name+(' · '+str(info) if info!='' else ''),flush=True)
    if not ok:s.fails.append(name)
  async def G(s,c):return await s.C.evaluate("c=>__dg.ev(c)",c)
  async def Hh(s,c):return await s.H.evaluate("c=>__dg.ev(c)",c)
  async def wait(s,ms):await s.C.wait_for_timeout(ms)
  async def act(s,a,arg,wait=2000):
    await s.G("(()=>{dockErr='';netSend({t:'act',act:%s,arg:%s});return 1})()"%(json.dumps(a),json.dumps(str(arg))));await s.wait(wait)
    return await s.G("dockErr")
  async def dock(s,wait=3000):
    # fly in close first (the host refuses a dock from beyond 520 m), then dock
    await s.G("(()=>{const p=W.player,E=W.stationEnt;if(E&&!S.player.docked){p.x=E.x+(E.st&&E.st.radius||200)+150;p.y=E.y;p.z=E.z;p.vx=p.vy=p.vz=0}return 1})()");await s.wait(1500)
    await s.G("(()=>{const P=S.player;P.docked='station';netSend({t:'dock',d:'station'});openDock('home');return 1})()");await s.wait(wait)
    return await s.Hh("S.pilots.clipid1.docked")
  async def undock(s,wait=3000):
    await s.G("(()=>{dockTab='home';undock();return 1})()");await s.wait(wait)
  async def goto(s,sid,maxHops=12):
    # jump by jump toward a system (the guest has to be in flight)
    for i in range(maxHops):
      here=await s.G("S.player.sector")
      if here==sid:return True
      nxt=await s.G("(()=>{const nb=NEIGH[S.player.sector].slice().sort((a,b)=>HOP[a][%s]-HOP[b][%s]);return nb[0]})()"%(json.dumps(sid),json.dumps(sid)))
      await s.G("(()=>{doJump(%s);return 1})()"%json.dumps(nxt));await s.wait(5000)
    return await s.G("S.player.sector")==sid
  async def ledger(s,label):
    l=await s.Hh(LED);print('ledger '+label+':',l,flush=True);return l
async def _boot(ctx,name,errs):
  pg=await ctx.new_page();pg.on('pageerror',lambda e:errs.append(name+': '+str(e.stack)[:500]))
  pg.on('console',lambda m:errs.append(name+' console: '+m.text[:400]) if m.type=='error' and 'TUNNEL' not in m.text and 'fonts' not in m.text and 'favicon' not in m.text else None)
  await pg.goto('file://'+FILE+'?name='+name,timeout=400000);await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=400000)
  await pg.evaluate("c=>__dg.ev(c)",f"(()=>{{$('mpName').value='{name}';legGrant('{name}','halcyon',true,'interceptor',null);return 1}})()")
  return pg
async def _main(body,gcls,gfac,gport):
  K=Kit()
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows'])
    K.H=await _boot(await b.new_context(viewport={'width':1200,'height':800}),'Hosty',K.errs);K.C=await _boot(await b.new_context(viewport={'width':1200,'height':800}),'Clie',K.errs)
    async def toC(s):
      try:await K.C.evaluate("d=>{if(window.MPHOST_READY)__dg.ev('linkRecv(MP.host,'+JSON.stringify(d)+')')}",s)
      except Exception as e:K.errs.append('relay->C '+str(e)[:200])
    async def toH(s):
      try:await K.H.evaluate("d=>__dg.ev('linkRecv(window.__HL,'+JSON.stringify(d)+')')",s)
      except Exception as e:K.errs.append('relay->H '+str(e)[:200])
    await K.H.expose_function('__toClient',toC);await K.C.expose_function('__toHost',toH)
    await K.H.evaluate(LINK);await K.C.evaluate(LINK)
    await K.Hh("(()=>{MP.pid='hostpid1';MP.name='Hosty';MP.code='crew';MP.cl={};MP.rp={};MP.inp={};MP.roster=[];hostBegin(false);selFac='halcyon';mpLaunch('halcyon','interceptor','mw');window.__HL=__mk('cli',s=>__toClient(s));return 1})()")
    await K.wait(1500)
    await K.G("(()=>{NET.on=true;NET.cl=true;NET.host=false;MP.pid='clipid1';NET.me=MP.pid;MP.name='Clie';MP.code='crew';MP.roster=[];MP.host=__mk('host',s=>__toHost(s));window.MPHOST_READY=1;linkUp(MP.host);return 1})()")
    await K.wait(2500)
    await K.G("(()=>{selFac=%s;mpLaunch(%s,%s,%s);return 1})()"%(json.dumps(gfac),json.dumps(gfac),json.dumps(gcls),json.dumps(gport)));await K.wait(4000)
    print('guest joined:',await K.G("(()=>JSON.stringify({fac:S.player.faction,cls:S.player.cls,sector:S.player.sector,docked:S.player.docked,cr:S.player.credits}))()"),flush=True)
    try:await body(K)
    except Exception as e:
      import traceback;traceback.print_exc();K.fails.append('exception: '+str(e)[:200])
    led=await K.Hh(LED);K.check('ledger exact',led=='exact',led)
    E=[e for e in K.errs if 'favicon' not in e];K.check('no errors',not E,E[:6])
    await b.close()
  print('FAILED: '+', '.join(K.fails) if K.fails else 'ALL OK',flush=True)
  sys.exit(1 if K.fails else 0)
def run(body,gcls='interceptor',gfac='varkesh',gport='ew'):asyncio.run(_main(body,gcls,gfac,gport))
