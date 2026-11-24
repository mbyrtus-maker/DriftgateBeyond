# Real jobs (the user, 24 Nov 2026): between systems goods ride a ship; only the Brood may move them without one.
# Checks the flows that used to change stores at once: the Unbound's fence and plunder, raids and response wings kitted from
# the station they leave, the powers' refit parts, a depot's standard stock, traders at a pilot's depot, a supply drive, and
# that the ledger stays exact throughout. tools/teleport.py audits a whole AI galaxy for anything else.
import asyncio,json,os
from playwright.async_api import async_playwright
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
RUN="""((pred,max)=>{for(let i=0;i<max;i++){if(pred())return i;S.T+=10;tradersTick()}return -1})"""
fails=[]
def check(name,ok,info=''):
  print(('ok  ' if ok else 'FAIL'),name,info if not ok or os.environ.get('V') else '')
  if not ok:fails.append(name)
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await ev("window.RUN="+RUN+";undock();exitSector();W=null;running=false;1")
    led=lambda:ev(LED)
    # ---- the Unbound's fence: a freighter out with the surplus, sold at the freeport, home with what the Wrack lacks
    r=json.loads(await ev("""(()=>{const st=S.econ.stock.pirate,fp=fpNear('wr'),N=dStore(fp);devLedger(()=>{inv.add(st,'fe',400);inv.add(N,'cu',120);S.econ.treasury.pirate+=9000;S.econ.treasury.neutral+=9000});
      const fe0=st.fe,cu0=st.cu||0,nfe0=N.fe||0,cr0=S.econ.treasury.pirate;pirFence({cu:cu0+60,wire:0});const t=S.traders.find(x=>x.side==='pirate'&&x.fence===1);
      const at0={from:t&&t.from,to:t&&t.to,load:t&&{...t.load},whFe:st.fe,fpFe:N.fe||0};pirFence({cu:cu0+60,wire:0});const one=S.traders.filter(x=>x.side==='pirate'&&x.fence).length;
      const n1=RUN(()=>!S.traders.includes(t),400);const b=S.traders.find(x=>x.side==='pirate'&&x.fence===2);const mid={fpFe:(N.fe||0)-nfe0,paid:S.econ.treasury.pirate-cr0,back:b&&{...b.load},whCu:st.cu||0};
      const n2=b?RUN(()=>!S.traders.includes(b),400):-2;return JSON.stringify({fp:fp.sid,fe0,cu0,at0,one,n1,mid,n2,whCu:(st.cu||0)-cu0})})()"""))
    check('the fence: a freighter leaves the Wrack with the surplus (nothing changes hands yet)',r['at0']['from']=='wr' and r['at0']['to']==r['fp'] and (r['at0']['load'] or {}).get('fe',0)>0 and r['at0']['fpFe']==0 or r['at0']['whFe']<r['fe0'] and r['at0']['from']=='wr',r)
    check('one fence run at a time',r['one']==1,r)
    check('it sells at the freeport when it arrives',r['n1']>0 and r['mid']['fpFe']>0 and r['mid']['paid']!=0,r)
    check('the copper it buys rides home',bool(r['mid']['back']) and r['mid']['back'].get('cu',0)>0 and r['mid']['whCu']==r['cu0'] and r['n2']>0 and r['whCu']>0,r)
    check('ledger exact after the fence',await led()=='exact',await led())
    # ---- plunder rides a prize freighter home
    r=json.loads(await ev("""(()=>{const R=S.stations.hr,ds=dStore(R);devLedger(()=>{inv.add(ds,'plate',60)});const p0=S.econ.stock.pirate.plate||0;pirRaidDepot('hr');const t=S.traders.find(x=>x.side==='pirate'&&x.loot);
      const now=(S.econ.stock.pirate.plate||0)-p0,ld=t&&{...t.load};const n=t?RUN(()=>!S.traders.includes(t),400):-2;return JSON.stringify({convoy:!!t,from:t&&t.from,to:t&&t.to,ld,now,n,home:(S.econ.stock.pirate.plate||0)-p0})})()"""))
    check('plunder from a depot leaves on an Unbound freighter',r['convoy'] and r['from']=='hr' and r['to']=='wr' and r['now']==0,r)
    check('it lands in the Wrack when the freighter arrives',r['n']>0 and r['home']>0,r)
    check('ledger exact after the plunder',await led()=='exact',await led())
    # ---- raids: a depot launches from its own store
    r=json.loads(await ev("""(()=>{const L=raidSources('halcyon'),d=L.find(s=>s.sid==='hr'),h=L.find(s=>s.sid==='hp');const ds=dStore(S.stations.hr);
      return JSON.stringify({depotOwn:!!d&&d.srcs.length===1&&d.srcs[0]===ds,home:!!h&&h.srcs.includes(S.econ.stock.halcyon),n:L.length})})()"""))
    check('a depot is a raid source with its own store, the home with the warehouse',r['depotOwn'] and r['home'],r)
    r=json.loads(await ev("""(()=>{const R=S.stations.hr,ds=dStore(R),wh=S.econ.stock.halcyon;devLedger(()=>{for(const k of['plate','wire','coil','missile'])inv.add(wh,k,inv.take(ds,k,ds[k]||0))});
      for(const t of S.traders.filter(x=>x.key==='kit:hr'))S.traders.splice(S.traders.indexOf(t),1),devLedger(()=>inv.addAll(wh,t.load));
      const kit=raidShips('halcyon',[ds]);rjKitAsk('halcyon',{sid:'hr',srcs:[ds]});const t=S.traders.find(x=>x.key==='kit:hr');const n=t?RUN(()=>!S.traders.includes(t),400):-2;
      const kit2=raidShips('halcyon',[ds]);const r=kit2&&raidSend('halcyon',{src:{sid:'hr',srcs:[ds],cap:null},tgt:null,dep:null,c:'cv'},kit2);const wh0=JSON.stringify(wh);
      if(r){r.state='home';r.dest='hr';r.path=['hr'];r.leg=0;r.sector='hr';const k0=invMass(ds);raidUnload(r);return JSON.stringify({bare:!kit,asked:!!t,from:t&&t.from,n,fit:!!kit2,sent:!!r,back:invMass(ds)-k0,whSame:wh0===JSON.stringify(wh)})}
      return JSON.stringify({bare:!kit,asked:!!t,n,fit:!!kit2,sent:false})})()"""))
    check('a depot with no kit asks the warehouse for some by convoy',r['bare'] and r['asked'] and r.get('from')=='hp' and r['n']>0,r)
    check('the raid is kitted from the depot and unloads into it',r['fit'] and r['sent'] and r['back']>0 and r['whSame'],r)
    check('ledger exact after the raid',await led()=='exact',await led())
    # ---- response wings: raised from the depot's own store when it can field one, else from home
    r=json.loads(await ev("""(()=>{const R=S.stations.hr,ds=dStore(R),wh=S.econ.stock.halcyon,fl=S.econ.fleet.halcyon;devLedger(()=>{inv.add(ds,'plate',40);inv.add(ds,'wire',30)});
      const w0=JSON.stringify([wh,fl]),d0=invMass(ds);const ev1=dispatchResponse('halcyon','hr','distress');const a={from:ev1&&ev1.from,depot:d0-invMass(ds),whSame:w0===JSON.stringify([wh,fl]),n:ev1&&ev1.n};
      if(ev1){ev1.stage='done';inv.addAll(wh,ev1.force);ev1.force={}}
      devLedger(()=>{for(const k of['plate','wire','coil','missile'])inv.add(wh,k,inv.take(ds,k,ds[k]||0))});const ev2=dispatchResponse('halcyon','hr','distress');
      const b={from:ev2&&ev2.from,eta:ev2&&Math.round(ev2.eta-S.T),hops:HOP.hp.hr};if(ev2){ev2.stage='done';inv.addAll(wh,ev2.force);ev2.force={}}return JSON.stringify({a,b})})()"""))
    check('a depot with kit raises the wing from its own store',r['a']['from']=='hr' and r['a']['depot']>0 and r['a']['whSame'],r)
    check('a bare depot: the wing comes from home, with the trip from home',r['b']['from']=='hp' and r['b']['eta']==25+22*r['b']['hops'],r)
    check('ledger exact after the responses',await led()=='exact',await led())
    # ---- the powers' refit parts ride home from a freeport
    r=json.loads(await ev("""(()=>{const R=S.stations.mw,pool=(S.corpFit=S.corpFit||{}).halcyon=S.corpFit.halcyon||{};const id=Object.keys(ITEMS).find(k=>ITEMS[k].maker&&(mkStock(R)[k]||0)>0);if(!id)return JSON.stringify({none:true});
      const p0=pool[id]||0;rjFitBuf={};rjFitGot('halcyon',R,id,pool);const buf=JSON.stringify(rjFitBuf);rjFitBuf=null;devLedger(()=>{});
      let mid=0,n=-1,tries=0;devLedger(()=>{inv.add(mkStock(R),id,4)});
      // (a convoy can be raided on the way: try again until one gets home)
      for(;tries<4&&(pool[id]||0)-p0<1;tries++){inv.take(mkStock(R),id,1);const t=haulSend('halcyon','mw','hp',{[id]:1},'fit:test'+tries,'refit parts');t.fit='halcyon';mid=(pool[id]||0)-p0;n=RUN(()=>!S.traders.includes(t),400)}return JSON.stringify({buf,mid,n,tries,got:(pool[id]||0)-p0})})()"""))
    check('a part bought at a freeport is held for the convoy, not fitted at once',not r.get('none') and 'halcyon|mw' in r['buf'] and r['mid']==0,r)
    check('it is fitted when the convoy reaches home',r.get('n',-1)>0 and r.get('got')==1,r)
    # ---- a depot's standard stock: from its own store, asking the warehouse by convoy
    r=json.loads(await ev("""(()=>{const R=S.stations.hr,st=mkStock(R),W0=stdWantAt(R),id=Object.keys(W0).find(k=>(st[k]||0)>0);if(!id)return JSON.stringify({none:true});const wh=S.econ.stock.halcyon;
      devLedger(()=>{for(const k of['fe','cu','ir','plate','wire','coil'])inv.add(wh,k,inv.take(st,k,st[k]||0));inv.add(wh,id,inv.take(st,id,1))});const w0=invMass(wh);S.stdT=0;stdTick();
      const t=S.traders.find(x=>x.key==='std:hr'),built=st[id]||0,ld=t&&{...t.load};let after=built,tries=0;
      // (the convoy can be raided: the depot asks again)
      for(;tries<4&&after<1;tries++){const c=S.traders.find(x=>x.key==='std:hr');if(c)RUN(()=>!S.traders.includes(c),400);S.stdT=0;stdTick();after=st[id]||0}
      return JSON.stringify({id,built,asked:!!t,from:t&&t.from,load:ld,whDown:w0-invMass(wh),after,tries})})()"""))
    check('a depot that lacks the materials does not build from the warehouse',not r.get('none') and r['built']==0,r)
    check('it asks the warehouse for them by convoy',r.get('asked') and r.get('from')=='hp',r)
    check('when the convoy lands the depot builds the part',r.get('after',0)>=1,r)
    check('ledger exact after refit and standard stock',await led()=='exact',await led())
    # ---- an Overgrowth strike flies out and home
    r=json.loads(await ev("""(()=>{const O={id:S.nextId++,a:'cv',b:'hr',key:gateKey('cv','hr'),stage:'grown',t0:S.T,hp:OG.hp,hitT:-1e9,load:{},strikeT:S.T+1e9};(S.og=S.og||[]).push(O);const wh=S.econ.stock.halcyon,force={};
      const ld=loadout('patrol',1,'bomber');devLedger(()=>{inv.addAll(wh,ld)});takeFrom(ld,[wh]);inv.addAll(force,ld);rjOgSend(O,'halcyon',force,1);const e=S.events.find(x=>x.type==='ogstrike');const eta=e&&Math.round(e.eta-S.T);
      const hp0=O.hp;S.T=e.eta+1;rjOgTick();const party=(S.raids||[]).find(x=>x.ret&&x.side==='halcyon'&&x.sector==='cv');return JSON.stringify({ev:!!e,eta,hops:HOP.hp.cv,done:e.stage,hit:O.hp<hp0||!S.og.includes(O),party:!!party})})()"""))
    check('bombers sent at Overgrowth take the trip there',r['ev'] and r['eta']==35*r['hops'],r)
    check('they strike when they arrive and fly home as a party',r['done']=='done' and r['hit'] and r['party'],r)
    check('ledger exact after the strike',await led()=='exact',await led())
    # ---- traders at a pilot's depot: what they buy rides home, what the depot buys comes out and is paid for on landing
    r=json.loads(await ev("""(()=>{const P=S.player;coDefault(P);const sid=SECTOR_DEFS.map(d=>d.id).filter(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id])[0];P.sector=sid;P.docked=null;enterSector(sid);devLedger(()=>{P.cargo={frame:2}});depFresh(P);const R=S.stations[sid];for(const f of FAC_IDS)standAdd(f,60,'test',P);
      devLedger(()=>{inv.add(R.stock,'plate',200);P.credits+=20000});R.sell={plate:0};R.buy={wire:40};exitSector();W=null;const pl0=R.stock.plate,wh0={};for(const f of FAC_IDS)wh0[f]=S.econ.stock[f].plate||0;const cr0=P.credits,w0=R.stock.wire||0;
      for(let i=0;i<6&&!S.traders.some(t=>t.pd&&t.pd.sid===sid);i++)depTradeTick();
      const out=S.traders.filter(t=>String(t.key).startsWith('pdep:')),inn=S.traders.filter(t=>t.pd&&t.pd.sid===sid);let whNow=0;for(const f of FAC_IDS)whNow+=(S.econ.stock[f].plate||0)-wh0[f];
      const a={sold:pl0-R.stock.plate,out:out.length,outFrom:out[0]&&out[0].from,whNow,inn:inn.length,innFrom:inn[0]&&inn[0].from,wireNow:(R.stock.wire||0)-w0,paidNow:cr0-P.credits<0?0:Math.max(0,0)};
      // (a convoy can be lost on the way, more so from a deep system: trade on until one of each has landed)
      const crMid=P.credits;let n=-1,cost=0,rounds=0,whEnd=0;const seen=new Set();
      for(;rounds<8;rounds++){for(const t of S.traders)if(t.pd&&t.pd.sid===sid&&!seen.has(t.id)){seen.add(t.id);cost+=t.pd.cost}
        n=RUN(()=>!S.traders.some(t=>(t.pd&&t.pd.sid===sid)||String(t.key).startsWith('pdep:')),600);whEnd=0;for(const f of FAC_IDS)whEnd+=(S.econ.stock[f].plate||0)-wh0[f];
        if(whEnd>0&&(R.stock.wire||0)-w0>0)break;depTradeTick()}
      return JSON.stringify({sid,a,n,rounds,whEnd,wireEnd:(R.stock.wire||0)-w0,paid:crMid-P.credits,cost})})()"""))
    check('plate a trader buys at the depot leaves on its convoy',r['a']['sold']>0 and r['a']['out']>=1 and r['a']['outFrom']==r['sid'] and r['a']['whNow']==0,r)
    check('wire the depot buys comes out from the power\'s home',r['a']['inn']>=1 and r['a']['innFrom'] in('hp','vb','os') and r['a']['wireNow']==0,r)
    check('both land, and the depot pays on delivery',r['whEnd']>0 and r['wireEnd']>0 and 0<r['paid']<=r['cost'],r)
    check('ledger exact after the depot trade',await led()=='exact',await led())
    # ---- a short AI stretch with everything running, and the ledger
    await ev("(()=>{for(let i=0;i<360;i++){S.T+=10;strategicTick();updateEvents()}return 1})()")
    check('ledger exact after an hour on',await led()=='exact',await led())
    check('no errors',not errs,errs[:4])
    print('errors',errs[:4]);print('ALL OK' if not fails else 'FAILED: '+', '.join(fails));await b.close()
asyncio.run(main())
