# Beyond: the economy fixes of 7 Nov 2026. (1) a maker's part costs a pilot what the station prices it at (stPrice: list price,
# profit floor, CEO), the Market quote, the intel price and the charge agree, and the maker clears its margin; (2) a posted Supply
# run whose job ends mid-flight drops its load as debris; (3) a Haul run whose buyer can pay for only part of the load sells that
# part, brings the rest home and is paid a scaled fee; (4) makers' parts' local price levels drift back to neutral; (5) an R&D
# launch leaves a pilot's depot stock alone; (6) the works craft a grade's inputs only after the money checks, and no lattice
# without a forge; (7) a merchant the Compact can't pay in full delivers only what was paid for; (8) the share price counts
# graded stock; (9) an AI pilot (a depot crew) buys and upgrades a maker's part at the player's price. Ledger exact throughout.
import asyncio,json
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text and 'ERR_TUNNEL' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    bad=[]
    await ev("(()=>{galaxyWon=()=>{};const e=S.T+1200;exitSector();W=null;while(S.T<e){S.T+=10;strategicTick();updateEvents()}return 1})()")
    # (1) prices: at a few makers' homes, the Market quote, the intel price, stPrice with the fee and the real charge agree
    r=json.loads(await ev("""(()=>{const P=S.player,out=[];transfer('neutral','player',20000);
      for(const m of Object.keys(MAKERS)){if(out.length>=4)break;const R=mkAtHome(m);if(!R||!ceAlive(m)||!(R.owner==='neutral'||tradeOK(P,R.owner)))continue;const st=mkStock(R),id=MK_LINE[m].map(i=>rdGid(i,rdLineG(m,i))).find(i=>st[i]>0);if(!id)continue;
        exitSector();P.sector=R.sid;P.docked=null;enterSector(R.sid);P.docked='station';const c=dockCtx(),q=mBuy(c,id),qs=mSell(c,id),sp=stPrice(R,id),fee=mFee(P.cls);intelTick(P);const it=P.pintel[R.sid];
        const c0=P.credits,t0=ceT(m),n0=st[id];dockAction('buy',id+':1');const paid=c0-P.credits,got=n0-(st[id]||0);
        out.push({m,id,quote:q,want:Math.ceil(sp*(1+fee)),intel:it&&it.b[id],sell:qs,wantSell:Math.max(1,Math.floor(sp*(1-fee))),paid,got,makerGot:ceT(m)-t0,cost:Math.ceil(ceComp(R.sid,id)),msg:String(dockErr).slice(0,80)})}
      P.docked=null;return JSON.stringify(out)})()"""))
    print('prices',json.dumps(r))
    if not r: bad.append('no maker home to test prices at')
    for x in r:
      if x['quote']!=x['want'] or (x.get('intel') is not None and x['intel']!=x['quote']) or x['sell']!=x['wantSell']: bad.append(f"price mismatch {x}")
      if x['got']==1 and x['paid']!=x['quote']: bad.append(f"charged {x['paid']} for a quote of {x['quote']} ({x['id']})")
      if x['got']==1 and not (x['makerGot']>=x['cost']): bad.append(f"maker {x['m']} got {x['makerGot']} for a part costing {x['cost']}")
    print('ledger',l:=await ev(LED))
    if l!='exact': bad.append('ledger after buys: '+l)
    # (2) a Supply run in flight when its depot changes hands: the load is dumped where the run is
    r=json.loads(await ev("""(()=>{const P=S.player;exitSector();W=null;transfer('neutral','player',20000);const sid=Object.keys(S.sectors).find(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id]);let R;devLedger(()=>{R=depMake(P,sid,stationSite(sid),{},{})});window._SID=sid;
      const msg=pjPost(P,sid+':supply:plate:10:fast');const j=pjList()[pjList().length-1];j.claimAt=S.T;pjTick();const r=pjRunOf(j.run);if(!r)return JSON.stringify({err:'no run: '+msg+' '+j.msg});
      const s=S.sectors[r.sector],d0=s.debris.fe,load=JSON.stringify(r.load);R.owner='varkesh';pjTick();R.owner='player';return JSON.stringify({load,runs:pjRuns().length,state:j.state,debrisFe:Math.round((s.debris.fe-d0)*100)/100})})()"""))
    print('supply lost',json.dumps(r))
    if r.get('err') or r['runs']!=0 or r['debrisFe']!=3*json.loads(r['load']).get('plate',0) or not r['debrisFe']: bad.append(f"supply run lost mid-flight: {r}")
    print('ledger',l:=await ev(LED))
    if l!='exact': bad.append('ledger after the lost supply run: '+l)
    # (3) Haul 20 plate to a market that can pay for 5: paid for 5, 15 ride home into the store, the fee a quarter
    r=json.loads(await ev("""(()=>{const P=S.player,sid=window._SID,R=S.stations[sid];devLedger(()=>{R.stock.plate=40});const msg=pjPost(P,sid+':haul:plate:20:fast');const j=pjList()[pjList().length-1];j.claimAt=S.T;pjTick();
      const r=pjRunOf(j.run);if(!r)return JSON.stringify({err:'no run: '+msg+' '+j.state+' '+j.msg});const D=S.stations[r.dst],f=D.owner,pr=Math.max(1,Math.floor(stPrice(D,'plate')*.95));
      const spare=Math.max(0,(S.econ.treasury[f]||0)-pr*5),park=f==='neutral'?'halcyon':'neutral';transfer(f,park,spare);const st0=mkStock(D).plate||0,c0=P.credits,store0=R.stock.plate||0;
      r.leg=r.path.length-1;r.next=S.T;pjRunsTick();const sold=(mkStock(D).plate||0)-st0,paid=P.credits-c0,back=r.load.plate||0,going=pjRuns().includes(r);transfer(park,f,spare);
      for(let i=0;i<100&&pjRuns().includes(r);i++){S.T+=10;pjRunsTick()}const c1=P.credits;
      return JSON.stringify({f,pr,sold,paid,back,going,store:(R.stock.plate||0)-store0,state:j.state,bid:j.bid,fee:j.paid,msg:j.msg})})()"""))
    print('haul partial',json.dumps(r))
    if r.get('err'): bad.append('haul: '+r['err'])
    else:
      if r['sold']!=5 or r['paid']!=5*r['pr']: bad.append(f"haul sold {r['sold']} paid {r['paid']} (want 5 for {5*r['pr']})")
      if r['back']!=15 or not r['going']: bad.append(f"haul: {r['back']} on the run home (want 15)")
      if r['store']!=15: bad.append(f"haul: {r['store']} came back into the store (want 15)")
      if r['fee']!=round(r['bid']*5/20): bad.append(f"haul fee {r['fee']} (want {round(r['bid']*5/20)} of {r['bid']})")
    print('ledger',l:=await ev(LED))
    if l!='exact': bad.append('ledger after the haul: '+l)
    # (4) a maker's part's local level drifts back to neutral
    r=json.loads(await ev("""(()=>{const R=mkStations().find(x=>x.owner==='neutral');const id=Object.keys(ITEMS).find(k=>ITEMS[k].maker);mkOf(R)[id]=-10;const a=R.mk[id];for(let i=0;i<30;i++)mkTick();return JSON.stringify({id,a,b:R.mk[id]||0})})()"""))
    print('drift',json.dumps(r))
    if not abs(r['b'])<abs(r['a'])*.2: bad.append(f"maker part level didn't drift back: {r}")
    # (5) an R&D launch keeps a pilot's depot stock; (6) works: no crafting before the money checks, no lattice without a forge
    r=json.loads(await ev("""(()=>{const P=S.player,R=S.stations[window._SID];const m=Object.keys(MAKERS).find(x=>ceAlive(x)&&mkAtHome(x)&&!ceOf(x).rd);const id=MK_LINE[m].find(i=>ITEMS[rdGid(i,2)]&&rdLineG(m,i)===1);
      devLedger(()=>inv.add(R.stock,id,3));const c=ceOf(m);c.rd={id,g:2,stage:'trials',until:S.T,proto:{},t0:S.T};rdTick();const kept=R.stock[id]||0;
      const fp=Object.values(S.stations).find(x=>x&&x.owner==='neutral'&&!rdForgeAt(x)),st={plate:10,xc:10,fe:30};const rc={lattice:1};const can=rdCanMake(st,rc,fp);rdCraftFor(st,rc,fp);
      const st2={fe:30,xc:5,wire:2,coil:1};const can2=rdCanMake(st2,{plate:1},fp),can3=rdCanMake(st2,{matrix:1},fp),snap=JSON.stringify(st2);
      const H=mkAtHome(m),hs=mkStock(H),before=JSON.stringify(hs),parked={};for(const x in MAKERS){parked[x]=transfer(ceW(x),'neutral',ceT(x))}S.mkT=0;makersTick();const after=JSON.stringify(hs);for(const x in parked)transfer('neutral',ceW(x),parked[x]);
      return JSON.stringify({m,id,kept,latticeNoForge:can,latticeMade:st.lattice||0,plateFromOre:can2,matrix:can3,probeLeft:JSON.stringify(st2)===snap,brokeStockWhenPoor:before!==after})})()"""))
    print('rd',json.dumps(r))
    if r['kept']!=3: bad.append(f"R&D launch broke the depot's old-grade stock: {r['kept']} of 3 left")
    if r['latticeNoForge'] or r['latticeMade']: bad.append('a lattice was made at a station without a forge')
    if r['plateFromOre']: bad.append('the works would make plate from ore')
    if not r['matrix'] or not r['probeLeft']: bad.append(f"matrix check / probe touched the stock: {r}")
    if r['brokeStockWhenPoor']: bad.append("a maker with no money still crafted or built at its works")
    print('ledger',l:=await ev(LED))
    if l!='exact': bad.append('ledger after R&D: '+l)
    # (7) a merchant the Compact can pay only 5 of 20 for: 5 delivered and paid, 15 go home
    r=json.loads(await ev("""(()=>{const B=Object.values(S.stations).find(x=>x&&x.owner==='neutral'&&isFreeF(x));const f='halcyon',k='plate',n=20;const pr=Math.max(1,Math.floor(stPrice(B,k)*.94));
      const spare=Math.max(0,S.econ.treasury.neutral-pr*5);transfer('neutral','varkesh',spare);let t;devLedger(()=>{t={id:S.nextId++,side:f,item:k,n,from:B.sid,to:B.sid,path:[B.sid],leg:0,sector:B.sid,next:S.T,load:{[k]:n},cls:'freighter',T0:S.T};S.traders.push(t)});
      const st0=mkStock(B)[k]||0,t0=S.econ.treasury[f],h0=S.traders.length;const i=S.traders.indexOf(t);S.traders.splice(i,1);traderArrive(t);const got=(mkStock(B)[k]||0)-st0,paid=S.econ.treasury[f]-t0;
      const home=S.traders.filter(x=>x.kind==='haul'&&x.load&&x.load[k]).slice(-1)[0];transfer('varkesh','neutral',spare);return JSON.stringify({pr,got,paid,home:home?home.load[k]:0,left:JSON.stringify(t.load)})})()"""))
    print('trader',json.dumps(r))
    if r['got']!=5 or r['paid']!=5*r['pr']: bad.append(f"merchant delivered {r['got']} for {r['paid']} (want 5 for {5*r['pr']})")
    if r['home']!=15: bad.append(f"merchant: {r['home']} going home (want 15)")
    print('ledger',l:=await ev(LED))
    if l!='exact': bad.append('ledger after the merchant: '+l)
    # (8) the share price counts graded stock on the shelves
    r=json.loads(await ev("""(()=>{const m=Object.keys(MAKERS).find(x=>ceAlive(x)&&mkAtHome(x));const id=MK_LINE[m].find(i=>ITEMS[rdGid(i,2)]),gid=rdGid(id,2),c=ceOf(m),st=mkStock(mkAtHome(m));const keep=JSON.stringify(c),cc=JSON.parse(keep);
      const run=()=>{Object.assign(c,JSON.parse(keep));for(const x in MAKERS){const o=ceOf(x);if(o){o.inc=0;o.cost=0}}ceHour();return c.px};const a=run();devLedger(()=>inv.add(st,gid,1));const b2=run();devLedger(()=>inv.take(st,gid,1));Object.assign(c,cc);
      return JSON.stringify({m,gid,diff:Math.round((b2-a)*100)/100,want:Math.round(ceComp(mkHomeSid(m),gid)/100*100)/100})})()"""))
    print('shares',json.dumps(r))
    if abs(r['diff']-r['want'])>.05: bad.append(f"share price doesn't count graded stock: {r}")
    print('ledger',l:=await ev(LED))
    if l!='exact': bad.append('ledger at the end: '+l)
    # (9) an AI pilot (a hauling crew at your depot) with credits in its purse docks at a market and buys a maker's part as a
    # player would: the player's price for its hull, the maker credited 85%, the shelf one down; a second visit with a higher
    # grade on the shelf upgrades (the old part sold back); then the crew leaves: its purse goes to the Compact, its part to debris
    r=json.loads(await ev("""(()=>{const P=S.player,R=S.stations[window._SID];P.rp=Math.max(P.rp||0,5000);transfer('neutral','player',20000);R.crew=R.crew||[];const hm=crewHire(R,P,'freighter');const c=R.crew[R.crew.length-1];if(!c)return JSON.stringify({err:'no crew: '+hm});
      const k='c'+c.id,D=Object.values(S.stations).find(x=>x&&x.owner==='neutral'&&isFreeF(x));const ms=mkStock(D),base=Object.keys(ITEMS).find(i=>ITEMS[i].maker&&ITEMS[i].part==='cargo'&&!ITEMS[i].grade&&i.startsWith('mp_')),m=ITEMS[base].maker;
      for(const i of Object.keys(ms))if(ITEMS[i]&&ITEMS[i].part==='cargo'&&ITEMS[i].maker)devLedger(()=>{const n=ms[i];inv.take(ms,i,n);inv.add(S.econ.stock.neutral,i,n)});
      devLedger(()=>inv.add(ms,base,1));transfer('neutral',aipW(k),2000);const want=mkPartPrice(D,base,c.cls);
      const keep=S.player.cls;S.player.cls=c.cls;exitSector();S.player.sector=D.sid;const pl=mBuy({kind:'station',market:ms},base);S.player.sector=window._SID;S.player.cls=keep;
      const p0=aipPurse(k),t0=ceT(m),n0=ms[base]||0,f0=S.econ.treasury.neutral;const got=aipShop(k,D,c.cls,'haul',5,R.sid);
      const one={k,base,want,playerQuote:pl,paid:p0-aipPurse(k),makerGot:ceT(m)-t0,makerWant:Math.floor(want*(1-CE.dues)),shelf:[n0,ms[base]||0],fitted:JSON.stringify(S.aip[k].kit),got};
      const g2=rdGid(base,2);devLedger(()=>inv.add(ms,g2,1));const p1=aipPurse(k);const up=aipShop(k,D,c.cls,'haul',5,R.sid);one.up=up;one.kit2=JSON.stringify(S.aip[k].kit);one.upCost=p1-aipPurse(k);one.upWant=mkPartPrice(D,g2,c.cls)-mkPartSell(D,base,c.cls);one.oldBack=ms[base]||0;
      const fly=aipGrades(k);one.cargoG=fly&&fly.cargo;
      const pu=aipPurse(k),fN=S.econ.treasury.neutral,dS=S.sectors[R.sid].debris.fe+S.sectors[R.sid].debris.cu+S.sectors[R.sid].debris.ir+S.sectors[R.sid].debris.xc;R.crew=R.crew.filter(x=>x!==c);S.aipT=0;aipTick();
      one.purseToCompact=S.econ.treasury.neutral-fN===pu;one.gone=!S.aip[k]&&!(aipW(k) in S.econ.treasury);one.debris=Math.round((S.sectors[R.sid].debris.fe+S.sectors[R.sid].debris.cu+S.sectors[R.sid].debris.ir+S.sectors[R.sid].debris.xc-dS)*100)/100;
      return JSON.stringify(one)})()"""))
    print('ai pilot buys',json.dumps(r))
    if r.get('err'): bad.append('ai pilot: '+r['err'])
    else:
      if r['got']!=1 or r['paid']!=r['want'] or r['paid']!=r['playerQuote']: bad.append(f"AI pilot paid {r['paid']} (Market quote {r['playerQuote']}, mkPartPrice {r['want']})")
      if r['makerGot']!=r['makerWant']: bad.append(f"maker credited {r['makerGot']} (want {r['makerWant']})")
      if r['shelf'][1]!=r['shelf'][0]-1: bad.append(f"shelf {r['shelf']} (want one down)")
      if r['up']!=1 or r['upCost']!=r['upWant'] or r['oldBack']!=1 or r['cargoG']!=2: bad.append(f"AI pilot upgrade: {r}")
      if not r['purseToCompact'] or not r['gone'] or not r['debris']>0: bad.append(f"crew gone: purse/kit not settled {r}")
    print('ledger',l:=await ev(LED))
    if l!='exact': bad.append('ledger after the AI pilot: '+l)
    print('errors',bad+errs[:5])
    await b.close()
asyncio.run(main())
