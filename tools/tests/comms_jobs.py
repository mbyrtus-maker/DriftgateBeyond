# Beyond: Comms "Jobs here". I opens Command, I again Jobs here (this system's jobs for your hull, best pay first), I again
# the ships around you. A fighter and a miner in the same freeport system see their own kinds; jobs for other hulls and
# dock-only jobs are counted, not listed; picking an escort signs on to the convoy, picking a contract tracks it; More pages
# through a long list; an Unbound pilot gets Prey here with scanner readings; the quick-keys line counts the jobs; the
# ledger stays exact
import asyncio,json,os
from playwright.async_api import async_playwright
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
SHOT=os.environ.get('DG_SHOT')
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
PAGE="(()=>{const c=$('comms');return (c.hidden?'HIDDEN ':'')+$('cmTo').textContent+' || '+[...$('cmList').querySelectorAll('.cm-o')].map(b=>b.innerText.replace(/\\n/g,' ')).join(' | ')+' || '+$('cmN').textContent})()"
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    # two ore contracts and a hauling contract at this freeport, and a convoy of a power we can work for passing through
    print('setup',await ev("""(()=>{undock();const P=S.player,sid=P.sector;const R0=RAWS[0],R1=RAWS[1];
      S.contracts.push({id:9901,item:R0,n:20,reward:1500,until:S.T+900,st:sid},{id:9902,item:R1,n:10,reward:800,until:S.T+900,st:sid},{id:9903,item:'plate',n:10,reward:600,until:S.T+900,st:sid});
      const f=FAC_IDS.find(x=>standOf(x,P)>=STAND.dock);let t=null;devLedger(()=>{t=haulSend(f,sid,FAC_HOME(f),{plate:10},'cjtest','supplies')});window._T=t
      return JSON.stringify({sid,f,cls:P.cls,convoy:!!t,left:t?cvLeft(t):null})})()"""))
    await pg.wait_for_timeout(800)
    print('fighter',await ev("(()=>{const r=cjList();return JSON.stringify({jobs:r.jobs.map(j=>j.id+' '+j.ty),other:r.other,dock:r.dock})})()"))
    await pg.keyboard.press('KeyI');await pg.wait_for_timeout(200)
    print('page1',await ev(PAGE))
    await pg.keyboard.press('KeyI');await pg.wait_for_timeout(200)
    print('page2',await ev(PAGE))
    if SHOT:await pg.screenshot(path=SHOT)
    print('keys line',await ev("(()=>{hudUpdate();const e=$('cKeys').querySelector('.cjc');return e?e.innerText:'none'})()"))
    print('pick escort',await ev("(()=>{const i=W.cmOpts.findIndex(o=>String(o.id||'').startsWith('ce:'));if(i<0)return 'no escort';commsPick(String(i));return JSON.stringify({esc:_T.esc&&_T.esc.k,track:JTRACK&&JTRACK.id,open:commsOpen()})})()"))
    await pg.keyboard.press('KeyI');await pg.keyboard.press('KeyI');await pg.keyboard.press('KeyI');await pg.wait_for_timeout(200)
    print('page3 (ships)',await ev(PAGE))
    await pg.keyboard.press('Escape')
    print('miner',await ev("(()=>{S.player.cls='skiff';const r=cjList();return JSON.stringify({jobs:r.jobs.map(j=>j.id+' '+j.ty+' '+j.payN),other:r.other})})()"))
    print('pick contract',await ev("(()=>{W.ftgt=W.player;openComms();cycleFriendly();const i=W.cmOpts.findIndex(o=>o.id==='k:9901');commsPick(String(i));return JSON.stringify({track:JTRACK&&JTRACK.id,flash:($('flash')||{}).textContent||''})})()"))
    print('more',await ev("""(()=>{const sid=S.player.sector;for(let i=0;i<5;i++)S.contracts.push({id:9910+i,item:RAWS[i%RAWS.length],n:10,reward:300+i,until:S.T+900,st:sid});W.ftgt=W.player;openComms();cycleFriendly();const a=W.cmOpts.map(o=>o.l.split(' · ')[0]);const m=W.cmOpts.findIndex(o=>o.k==='cjmore');commsPick(String(m));const b2=W.cmOpts.map(o=>o.l.split(' · ')[0]);closeComms();return JSON.stringify({a,b:b2})})()"""))
    print('ledger',await ev(LED))
    # the Unbound, in a power's home system
    print('unbound',await ev("(()=>{FEED.length=0;newGame('halcyon',launchCls(),'Raider');S.unb=1;unbP();S.player.cls='raider';S.player.faction='pirate';startWith(S);undock();const sid=FAC_HOME('varkesh');exitSector();S.player.sector=sid;S.player.docked=null;enterSector(sid);return S.unb+' '+W.sid})()"))
    await pg.wait_for_timeout(1500)
    print('prey',await ev("""(()=>{const L0=cjPrey();if(!L0.length)return 'no prey here';L0[L0.length-1].e._csc={p:1,done:true,seen:true};const L=cjPrey();W.ftgt=W.player;openComms();cycleFriendly();const pg=$('cmTo').textContent+' || '+W.cmOpts.map(o=>o.l).join(' | ');commsPick('0');return pg+' || first is the scanned one '+(L[0]===L.find(x=>x.r.known===2))+' || targeted '+(W.tgt&&W.tgt.ref===L[0].e)})()"""))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
