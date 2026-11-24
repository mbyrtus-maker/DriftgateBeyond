# Teleport audit (the user, 24 Nov 2026: "In system teleportation is fine, but between systems is a haul job, getting ore is
# a mining job"; only the Brood may move goods between systems without a ship). Plays one AI galaxy off-screen and lists
# every game function that moved goods from one system to another with no ship carrying them (see tools/teleport.js).
# usage: [PPORT=mw] python3 tools/teleport.py PAGE HOURS OUT.json [MAXCALLS=10]      (10 hours takes about 6 minutes)
# Copy the page to a scratch folder first, as for fastsim.py. Ends "ALL OK" when the only flows left are rock and debris
# (nature, and the Brood's grazing). It covers the galaxy's own turn only: what a pilot does at a dock or meets in a live
# system is not played (BEYOND_DESIGN.md, "Real jobs", lists what was read by hand).
import asyncio,json,sys,re,os,glob,time
from playwright.async_api import async_playwright
PAGE=os.path.abspath(sys.argv[1]);H=float(sys.argv[2]);OUT=sys.argv[3];MAXC=float(sys.argv[4]) if len(sys.argv)>4 else 10
ONLY=sys.argv[5].split(',') if len(sys.argv)>5 else None
HERE=os.path.dirname(os.path.abspath(__file__));SRC=os.environ.get('SRC',os.path.dirname(HERE)+'/src/js')
names=set()
for f in glob.glob(SRC+'/*.js'):names|=set(re.findall(r'\bfunction\s+([a-z]\w*)\s*\(',open(f).read()))
SKIP={'invVec','comp','allPilots','indSysInv','fitItems','cmpFitDelta','mkHomeSid','strategicTick','updateEvents','frame','loop','eval','rnd','pick','clamp','ri'}
names=sorted(names-SKIP)
PP=os.environ.get('PPORT','mw')
# flows left in on purpose until the user decides (BEYOND_DESIGN.md, "Real jobs"): a function's name and why
KNOWN={'kitTick':'a kit on the shelf where a pilot is docked may draw ore from other markets'}
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:300]));pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' else None)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await pg.goto('file://'+PAGE+'?name=Tester',timeout=180000,wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("selFac='halcyon';document.getElementById('bLaunch').click()");await pg.wait_for_timeout(800)
    await ev("LEADT.mode='neutral';1")
    await ev(f"FEED.length=0;for(const k of Object.keys(WORLDS))delete WORLDS[k];W=null;newGame('halcyon',launchCls(),'Tester',{PP!r});S.player.name='Tester';startWith(S);running=false;exitSector();W=null;galaxyWon=function(s){{S.won=s}};1")
    await ev(open(HERE+'/teleport.js').read())
    ok=await ev("(()=>{let n=0;for(const nm of "+json.dumps(names)+"){try{if(eval('typeof '+nm)==='function'){eval(nm+'=_tp.w(\"'+nm+'\",'+nm+')');n++}}catch(e){}}return n})()")
    print('wrapped',ok,'of',len(names),flush=True)
    step="(n=>{for(let i=0;i<n;i++){S.T+=10;if(_tp.mode)_tp.mark('(between ticks)');_tp.stack.push('strategicTick');strategicTick();_tp.stack.pop();if(_tp.mode)_tp.mark('strategicTick');_tp.stack.push('updateEvents');updateEvents();_tp.stack.pop();if(_tp.mode)_tp.mark('updateEvents')}return S.T})"
    # phase A: count calls over 5 minutes of game time (after a 10-minute warm-up so most systems have started)
    await ev(step+"(60)");await ev("_tp.on=true;_tp.mode=0;1");await ev(step+"(60)")
    cnt=json.loads(await ev("JSON.stringify(_tp.cnt)"))
    C={k:1 for k,v in cnt.items() if v/60<=MAXC}
    if ONLY:C={k:1 for k in ONLY}
    hot=sorted(((v,k) for k,v in cnt.items() if v/60>MAXC),reverse=True)
    print('called',len(cnt),'tracked',len(C),'too hot:',[k for v,k in hot][:40],flush=True)
    await ev("_tp.C="+json.dumps(C)+";_tp.mode=1;_tp.last=null;_tp.dbgN="+json.dumps({k:1 for k in os.environ.get('DBG','').split(',') if k})+";1")
    t0=time.time();T=0;end=H*3600+1200
    while T<end:
      T=await ev(step+"(30)")
      if int(T)%1800<300:print('T',round(T/3600,2),'h',round(time.time()-t0),'s snaps',await ev("_tp.snaps"),'ms',round(await ev("_tp.ms")),flush=True)
    res=json.loads(await ev("JSON.stringify({capStrike:_tp.capStrike,leak:_tp.leak,defer:_tp.defer,dbg:_tp.dbg,agg:_tp.agg,T:S.T,tot:_tp.total(_tp.last),led:ledger().tot})"));res['errs']=errs[:12];res['cnt']=cnt
    json.dump(res,open(OUT,'w'),indent=1);await b.close()
    rows=sorted(res['agg'].items(),key=lambda kv:-kv[1]['mass']);bad=0
    print('hours',round(res['T']/3600,1),'| strike craft lost next door',round(res.get('capStrike') or 0),'| ledger',res['led'],'| snapshot',res['tot'])
    for k,g in rows:
      for s,x in sorted(g['sig'].items(),key=lambda kv:-kv[1]['mass']):
        labs=set(l for part in s.split(' -> ') for l in part.split(',') if l)
        nature=labs<=set(['rock','debris'])
        known=KNOWN.get(k) if not nature else None
        if not nature and not known:bad+=x['mass']
        print(('  nature/Brood' if nature else '  known: '+known if known else 'FLOW')+' %5dx %7d units  [%s]  %s'%(x['n'],round(x['mass']),k,s[:160]));print('          e.g. '+x['ex'][:260])
    real=[e for e in errs if 'ERR_TUNNEL' not in e and 'Failed to load resource' not in e]
    print('errors',real[:6]);print('ALL OK' if not bad and not real else f'FAILED: {round(bad)} units moved between systems with no ship')
    sys.exit(0 if not bad and not real else 1)
asyncio.run(main())
