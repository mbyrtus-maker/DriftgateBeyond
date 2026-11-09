# usage: python3 tools/ecotrace/ecotrace.py PAGE.html GALAXIES HOURS OUT.json [WORKERS]; then python3 tools/ecotrace/ecoan.py OUT.json
# economy trace: per maker, hourly treasury, share price, sales by kind; events (tweaks, R&D starts/launches, failures, rebirths, CEO changes)
import asyncio,json,sys,os
from playwright.async_api import async_playwright
FILE=sys.argv[1];N=int(sys.argv[2]);H=int(sys.argv[3]);OUT=sys.argv[4];WK=int(sys.argv[5]) if len(sys.argv)>5 else 2
PROBE=r"""(()=>{window._et={ev:[],sales:{}};const E=(k,o)=>_et.ev.push(Object.assign({k,T:Math.round(S.T/60)},o));
 {const o=ceSale;ceSale=function(m,id,n,paid,wallet,sid){const c=ceOf(m),alive=c&&!c.dead;const r=o.apply(this,arguments);if(alive&&paid>0){const k=ceKind(ITEMS[id].base||id),key=m+'|'+k;const s=_et.sales[key]=_et.sales[key]||[0,0];s[0]+=n;s[1]+=paid}return r}}
 {const o=ceTweak;ceTweak=function(m,id,why){const r=o.apply(this,arguments);if(r!==false)E('tweak',{m,id,why});return r}}
 {const o=rdStart;rdStart=function(m,id,why){const r=o.apply(this,arguments);if(r)E('rdstart',{m,id,why,g:ceOf(m).rd&&ceOf(m).rd.g});return r}}
 {const o=rdLaunch;rdLaunch=function(m){const P=ceOf(m).rd;const x=P?{id:P.id,g:P.g,t0:Math.round(P.t0/60)}:{};const r=o.apply(this,arguments);E(ceOf(m).rd?'trialfail':'launch',Object.assign({m},x));return r}}
 {const o=rdFlyLost;rdFlyLost=function(t,sid){E('flylost',{m:t.test&&t.test.m});return o.apply(this,arguments)}}
 {const o=ceFail;ceFail=function(m){const c=ceOf(m);E('fail',{m,cash:Math.round(ceT(m)),up:Math.round(ceUpkeep(m)),pxH:(c.pxH||[]).slice(-4),rd:c.rd?c.rd.stage:null});return o.apply(this,arguments)}}
 {const o=ceReborn;ceReborn=function(m){const r=o.apply(this,arguments);if(!ceOf(m).dead)E('reborn',{m});return r}}
 window._etSnap=function(){const o={T:Math.round(S.T/3600),m:{}};for(const m in MAKERS){const c=ceOf(m);if(!c)continue;o.m[m]={dead:!!c.dead,gen:c.gen,cash:Math.round(ceT(m)),px:Math.round((c.px||0)*10)/10,E:Math.round(c.E||0),ceo:c.ceo,str:!!c.str,g:Object.values(c.g||{}).reduce((a,b)=>Math.max(a,b),1),rd:c.rd?c.rd.stage:null}}
   o.sales=_et.sales;_et.sales={};o.ev=_et.ev;_et.ev=[];return JSON.stringify(o)};return 1})()"""
async def worker(b,n,res,wid):
  pg=await b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:200]))
  await pg.goto('file://'+os.path.abspath(FILE)+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
  await pg.evaluate("selFac='halcyon';document.getElementById('bLaunch').click()");await pg.wait_for_timeout(800)
  ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
  await ev("LEADT.mode='neutral';1");await ev(PROBE)
  for g in range(n):
    await ev("(()=>{FEED.length=0;for(const k of Object.keys(WORLDS))delete WORLDS[k];W=null;newGame('halcyon',launchCls(),'Tester','mw');S.player.name='Tester';startWith(S);running=false;W=null;galaxyWon=function(s){if(!S.won)S.won=[s,Math.round(S.T/60)]};_et.ev=[];_et.sales={};return 1})()")
    rows=[]
    for h in range(1,H+1):
      await asyncio.wait_for(ev("(()=>{while(S.T<%d){S.T+=10;strategicTick();updateEvents()}return 1})()"%(h*3600)),timeout=900)
      rows.append(json.loads(await ev("_etSnap()")))
    res.append({'won':await ev("S.won||null"),'rows':rows,'errs':errs[:3]});print(wid,len(res),flush=True)
async def main():
  res=[]
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    per=[N//WK+(1 if i<N%WK else 0) for i in range(WK)]
    await asyncio.gather(*[worker(b,per[i],res,i) for i in range(WK)])
    await b.close()
  json.dump(res,open(OUT,'w'))
asyncio.run(main())
