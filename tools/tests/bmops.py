# Beyond, black-market contracts (9 Nov 2026): a power at war posts an assassination contract on the enemy leader; a maker's
# CEO flies a shuttle and a rival posts a contract on it; both show only on Jobs → Black market; taking and completing them
# pays from the client; the dead CEO is replaced and the maker's share price takes a knock; Severe heat for a leader; the
# ledger stays exact throughout
import asyncio,json
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.join(' ')||'exact'})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[];bad=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    def check(name,ok,info=''):
      print(('ok   ' if ok else 'FAIL ')+name,info)
      if not ok:bad.append(name)
    r=json.loads(await ev("""(()=>{running=false;exitSector();W=null;for(let i=0;i<30&&!(leaderOf('varkesh')&&leaderOf('varkesh').ship);i++){S.T+=10;strategicTick();updateEvents()}const[a,b]=['halcyon','varkesh'];S.pair=S.pair||{};const k=pkey2(a,b);S.pair[k]=S.pair[k]||{};S.pair[k].war=1;S.coal=null;
      const Lb=leaderOf(b);Lb.ship.alive=true;const m=Object.keys(MAKERS).find(x=>ceAlive(x)&&mkAtHome(x));S.ceoT={};for(const x in MAKERS)S.ceoT[x]=S.T+1e6;S.ceoT[m]=0;S.bmoT=0;bmoTick();
      const L=bmoAll();return JSON.stringify({war:warWith(a,b),kill:L.filter(x=>x.k==='kill'&&x.by===a&&x.tgt===b).length,ceo:L.filter(x=>x.k==='ceo'&&x.tgt===m).length,m,sh:!!ceoShuttle(m)})})()"""))
    check('a power at war posts a contract on the enemy leader',r['war'] and r['kill']==1,r)
    check('a maker\'s CEO flies a shuttle and a rival posts a contract on it',r['sh'] and r['ceo']==1,r)
    m=r['m']
    r=json.loads(await ev(f"""(()=>{{const P=S.player,R=S.stations[FAC_HOME('halcyon')]||mkStations()[0];P.sector=R.sid;enterSector(R.sid);running=false;P.docked='station';const c=dockCtx(),srcs=[P.cargo,c.storage];
      const L=jobsList(c,P,srcs).filter(x=>String(x.id).startsWith('bk:'));const main=jbBoard(c,P,srcs,false,false),bm=jbBmHtml(c,P,srcs);
      const x=bmoAll().find(y=>y.k==='ceo');dockAction('bmotake',x.id);return JSON.stringify({{n:L.length,allBm:L.every(j=>j.bm),inMain:/Assassinate/.test(main),inBm:/Assassinate/.test(bm),took:dockErr,taker:x.taker}})}})()"""))
    check('the contracts are on Jobs → Black market only',r['n']>=2 and r['allBm'] and r['inBm'] and not r['inMain'],r)
    check('taking the CEO contract',r['took'].startswith('✓') and r['taker'],r)
    r=json.loads(await ev(f"""(()=>{{const P=S.player,m={json.dumps(m)},t=ceoShuttle(m),c=ceOf(m),ceo0=c.ceo;exitSector();W=null;P.sector=t.sector;P.docked=null;enterSector(t.sector);running=false;
      let e=W.ents.find(x=>x.alive&&x.tradeT===t);if(!e){{t.live=false;e=spawnTrader(t,false)}}const c0=P.credits,cl0=ceT(Object.keys(MAKERS).find(x=>bmoAll().some(y=>y.k==='ceo'&&y.by==='corp_'+x))||m);killShip(e,'player',{{src:W.player}});
      return JSON.stringify({{paid:P.credits-c0,newCeo:c.ceo!==ceo0,hit:!!c.ceoHit,gone:!ceoShuttle(m),left:bmoAll().filter(y=>y.k==='ceo').length}})}})()"""))
    check('shooting the shuttle down pays the contract, and the maker gets a new CEO',r['paid']>=3000 and r['newCeo'] and r['hit'] and r['gone'] and r['left']==0,r)
    r=json.loads(await ev("""(()=>{const P=S.player,b='varkesh',x=bmoAll().find(y=>y.k==='kill'&&y.tgt===b);dockAction('bmotake',x.id);const Lb=leaderOf(b);Lb.ship.sid=W.sid;Lb.ship.alive=true;Lb.ship.live=0;leaderSpawn(b,W);
      const e=leaderEnt(b);if(!e)return JSON.stringify({spawned:false});const c0=P.credits,h0=heatOf(b,P);killShip(e,'player',{src:W.player});
      return JSON.stringify({spawned:true,paid:P.credits-c0,heat:heatOf(b,P)-h0,left:bmoAll().filter(y=>y.k==='kill'&&y.tgt===b).length})})()"""))
    check('the enemy leader shot down: the contract pays (on top of any bounty) and brings Severe heat',r.get('spawned') and r['paid']>=4000 and r['heat']>=40 and r['left']==0,r)
    l=await ev(LED);check('ledger exact',l=='exact',l)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
