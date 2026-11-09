# Beyond, makers' goods seek buyers by haul job (8 Nov 2026): every system has its place on the Loadout ship; a maker's
# payload bay line starts at grade 2; makers post freight jobs at the source's Jobs board; a pilot takes one (goods to the
# hold, collateral in escrow) and delivers it (pay and collateral back, goods on the destination's market); a job nobody
# takes goes by the maker's own freighter; R&D materials go by haul job and a named test pilot flies the trials (shot down,
# the project goes back to materials; home, the line launches); the ledger stays exact throughout
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
    st=json.loads(await ev("JSON.stringify({store:Object.keys(MAKERS).every(m=>ceStore(m).plate===60&&ceStore(m).wire===40&&ceStore(m).coil===20),cr:Math.min(...Object.keys(MAKERS).map(m=>Math.round(ceT(m))))})"))
    check('makers start with 8,000 cr and their own 60 plate, 40 conduit and 20 coil',st['store'] and st['cr']>=7500,st)
    l=await ev(LED);check('ledger exact at the start (the makers\' starting components are part of the galaxy)',l=='exact',l)
    lo=json.loads(await ev("""(()=>{const P=S.player;P.docked='station';openDock();dockTab='upg';ldSel='parts';renderDock();const n=document.querySelectorAll('.ldsysp').length,strip=document.querySelectorAll('.ldsysrow').length;
      document.querySelector('.ldsysp[data-arg="sys:engine"]').click();const panel=!!document.querySelector('#ldSysHost');dockTab='home';renderDock();return JSON.stringify({n,strip,panel})})()"""))
    check('every system has a place on the ship (7 on a fighter), no strip, a click opens its panel',lo['n']==7 and lo['strip']==0 and lo['panel'],lo)
    check('a maker\'s payload bay line starts at grade 2',await ev("rdLineG('wf','sy_wf_payload')===2&&rdLineG('mwa','sy_mwa_payload')===2"))
    # a freight job posted, taken by the pilot (flying a light hauler: the test books the hull swap into the ledger's start) and delivered
    r=json.loads(await ev("""(()=>{running=false;exitSector();W=null;let j=null,i=0;while(!j&&i<200){S.T+=10;strategicTick();updateEvents();j=mfjAll().find(x=>x.k==='out'&&x.st==='open');i++}
      if(!j)return JSON.stringify({posted:false});const P=S.player;{const l0=ledger();P.cls='courier';P.fit=fitNew('courier',null);const l1=ledger();for(const e of RAWS)S.ledger0.tot[e]+=l1.tot[e]-l0.tot[e]}P.sector=j.from;enterSector(j.from);running=false;P.docked='station';P.cargo={};P.credits+=0;const need=mfjVal(j)+10;if(P.credits<need){const n=need-P.credits;S.econ.treasury.neutral-=n;P.credits+=n}
      const c0=P.credits,c=dockCtx(),L=jobsList(c,P,[P.cargo,P.vault]),onBoard=L.some(x=>x.id==='mf:'+j.id&&x.btn&&x.btn[0]==='mftake');
      dockAction('mftake',j.id);const took=dockErr,inHold=Object.keys(j.load).every(k=>(P.cargo[k]||0)>=j.load[k]),esc=S.econ.treasury[mfjW(j)]||0,coll=c0-P.credits;
      const D=S.stations[j.to],ds=mkStock(D),before={};for(const k in j.load)before[k]=ds[k]||0;exitSector();P.sector=j.to;enterSector(j.to);running=false;P.docked='station';const L2=jobsList(dockCtx(),P,[P.cargo,P.vault]),delBtn=L2.some(x=>x.id==='mf:'+j.id&&x.btn&&x.btn[0]==='mfdel');
      const c1=P.credits;dockAction('mfdel',j.id);const del=dockErr,onShelf=Object.keys(j.load).every(k=>(ds[k]||0)>=before[k]+j.load[k]),got=P.credits-c1;
      return JSON.stringify({posted:true,onBoard,took,inHold,esc,coll,delBtn,del,onShelf,got,pay:j.pay,gone:!mfjAll().includes(j),escLeft:S.econ.treasury[mfjW(j)]||0})})()"""))
    check('a maker posts a freight job and it shows on the source\'s board',r.get('posted') and r.get('onBoard'),r)
    check('taking it loads the goods and puts their value in escrow',r.get('inHold') and r.get('esc')>0 and r.get('coll')==r.get('esc'),r)
    check('Deliver at the destination: goods on its market, pay and collateral back',r.get('delBtn') and r.get('onShelf') and r.get('got')==r.get('pay')+r.get('coll') and r.get('gone') and r.get('escLeft')==0,r)
    l=await ev(LED);check('ledger exact after the freight job',l=='exact',l)
    # a job nobody takes goes by the maker's own freighter
    r=json.loads(await ev("""(()=>{exitSector();W=null;let i=0,n0=0;const seen=new Set();let npc=0;for(;i<120;i++){S.T+=10;strategicTick();updateEvents();for(const t of S.traders||[])if(t.syf&&!seen.has(t.id)){seen.add(t.id);npc++}}
      return JSON.stringify({npc,open:mfjAll().filter(j=>j.st==='open').length})})()"""))
    check('untaken jobs go by the makers\' own freighters',r['npc']>=2,r)
    # R&D: materials by haul job, trials by a named test pilot (shot down once, then home). The test stocks the nearest other
    # market with the prototype's components (booked into the ledger's start), so there is a market to buy them at.
    r=json.loads(await ev("""(()=>{const m='mg',id='mp_mg_gun';const c=ceOf(m);c.rd=null;S.econ.treasury[ceW(m)]+=20000;S.econ.treasury.varkesh-=20000;const R0=mkAtHome(m),src=Object.values(S.stations).filter(R=>syfSrcOk(R0,R)).sort((a,b)=>HOP[R0.sid][a.sid]-HOP[R0.sid][b.sid])[0],rc=ITEMS[rdGid(id,2)].recipe;for(const k in rc){const q=rc[k]+4;inv.add(mkStock(src),k,q);const v=invVec({[k]:q});for(const e of RAWS)S.ledger0.tot[e]+=v[e]}
      const ok=rdStart(m,id,'test');c.rd.until=S.T;
      const st={};let i=0,lost=false,flew=null,mat=null,news=[];
      for(;i<1500&&rdLineG(m,id)<2;i++){S.T+=10;strategicTick();updateEvents();const P=c.rd;if(!P)continue;if(P.mj&&!mat)mat=P.mj;st[P.stage]=1;
        const t=(S.traders||[]).find(x=>x.test&&x.test.m===m);if(t&&!flew)flew={name:t.test.name,cls:t.cls,path:t.path.length};
        if(t&&!lost&&t.leg>=1){lost=true;const i2=S.traders.indexOf(t);S.traders.splice(i2,1);haulLost(t,t.sector,'pirate');news.push(c.rd&&c.rd.stage)}}
      const P=c.rd,tt=(S.traders||[]).find(x=>x.test&&x.test.m===m);return JSON.stringify({ok,mat:!!mat,flew,lost,backTo:news[0],launched:rdLineG(m,id)>=2,end:P?P.stage+' mj'+(P.mj||0)+' fly'+(P.fly||0)+(tt?' at '+tt.sector+' leg '+tt.leg:''):'none',grade:rdLineG(m,id),mins:Math.round(i/6),stages:Object.keys(st)})})()"""))
    check('R&D materials are posted as a haul job',r['ok'] and r['mat'],r)
    check('a named test pilot flies the prototype out and home',bool(r['flew']) and ' ' in r['flew']['name'] and r['flew']['cls']=='striker' and r['flew']['path']>=5,r)
    check('shot down, the project goes back to materials',r['lost'] and r['backTo']=='materials',r)
    check('home again, the line launches at grade 2',r['launched'] and r['grade']==2,r)
    l=await ev(LED);check('ledger exact after R&D',l=='exact',l)
    # the launch window's roll: a failed trial sends the project back to a redesign (the prototype's components to the maker's
    # store); a success launches; R&D spending counts in the share price (the test gives the prototype, booked into the ledger)
    r=json.loads(await ev("""(()=>{const m='tcy',id=MK_LINE[m].find(x=>ITEMS[x]&&ITEMS[x].part&&!ITEMS[x].sys);const c=ceOf(m);c.rd=null;c.ceo=CE.ceos.find(x=>x!=='Innovator');S.econ.treasury[ceW(m)]+=20000;S.econ.treasury.halcyon-=20000;
      const g0=rdLineG(m,id),iv0=c.iv||0,ok=rdStart(m,id,'test'),ivUp=(c.iv||0)-iv0,P=c.rd,rc=ITEMS[rdGid(id,P.g)].recipe;const prep=()=>{P.stage='trials';P.got=1;P.ivm=1;P.proto={...rc};const v=invVec(rc);for(const e of RAWS)S.ledger0.tot[e]+=v[e]};
      prep();const st0={...ceStore(m)},R0=Math.random;Math.random=()=>.999;rdLaunch(m);Math.random=R0;const back=Object.keys(rc).every(k=>(ceStore(m)[k]||0)-(st0[k]||0)===rc[k]);
      const failed={stage:P.stage,fails:P.fails,grade:rdLineG(m,id),back,chance:Math.round(100*rdWinChance(m,P))};prep();Math.random=()=>0;rdLaunch(m);Math.random=R0;
      return JSON.stringify({ok,ivUp,failed,launched:rdLineG(m,id)===g0+1&&!c.rd,ivAfter:c.iv||0})})()"""))
    check('R&D funding counts as investment in the share price',r['ok'] and r['ivUp']>0,r)
    check('a failed trial: back to a redesign, the prototype\'s components to the maker\'s store, the next roll 10% better',r['failed']['stage']=='design' and r['failed']['fails']==1 and r['failed']['grade']==1 and r['failed']['back'] and r['failed']['chance']==85,r)
    check('a successful roll launches the line',r['launched'],r)
    l=await ev(LED);check('ledger exact after the rolls',l=='exact',l)
    # liquidation: three hours with the shares under 60% of the market's median price and the company is wound up (the test
    # holds the company's price at 1 at each valuation) (its cash to its
    # shareholders), and a new company opens in its works
    r=json.loads(await ev("""(()=>{const m='qs',c=ceOf(m);const o0=ceFloor;ceFloor=function(){if(ceAlive(m))c.px=1;return o0.apply(this,arguments)};const h0=S.ceHr;let i=0,liq=false,cash=0;const home0=S.econ.treasury[ceHomeWallet(m)]||0;
      while(i<2600&&!(liq&&!c.dead)){S.T+=10;strategicTick();updateEvents();if(!liq&&c.dead){liq=true;cash=ceT(m)}i++}ceFloor=o0;
      return JSON.stringify({liq,leftCash:cash,reborn:liq&&!c.dead,gen:c.gen,mins:Math.round(i/6)})})()"""))
    check('3 hours on the floor: the company is liquidated and a new one opens in its works',r['liq'] and r['leftCash']==0 and r['reborn'] and r['gen']>=2,r)
    l=await ev(LED);check('ledger exact after the liquidation',l=='exact',l)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
