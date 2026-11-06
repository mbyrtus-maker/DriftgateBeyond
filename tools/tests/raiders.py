# Beyond live space stage 3 (6 Nov 2026): raiders are tracked. No chance raider or Unbound wings; prowls go out to hunting
# grounds and wait there, springing on hostile convoys; live a prowl holds by a gate as a wing; off-screen raiders and a hostile
# garrison fight by the odds; a finished offensive's force flies home as a tracked party; the ledger stays exact throughout
import asyncio,json
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
RUN="""((pred,max)=>{for(let i=0;i<max;i++){if(pred())return i;S.T+=10;raidsTick();tradersTick()}return -1})"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await ev("window.RUN="+RUN+";S.T=Math.max(S.T,400);1")
    print('no chance raiders',await ev("""(()=>{const P=S.player;undock();const ids=SECTOR_DEFS.filter(d=>d.kind==='deep'||d.kind==='contested'||d.kind==='frontier').map(d=>d.id);let n=0;for(const sid of ids.slice(0,6)){exitSector();P.sector=sid;P.docked=null;enterSector(sid);n+=popWants().filter(w=>w[0]==='raider'||w[0]==='pirate').length+W.ents.filter(e=>e.npc&&(e.role==='raider'||e.role==='pirate')&&!e.raidR).length}exitSector();P.sector='mw';enterSector('mw');return n})()"""))
    print('an Unbound prowl',await ev("""(()=>{const r=prwSend('pirate');window._R=r;if(!r)return 'none';const n=RUN(()=>r.state==='wait'||!S.raids.includes(r),60);return JSON.stringify({prowl:r.prowl,ships:r.ships.length,dest:r.dest,kind:DEF[r.dest].kind,state:r.state,wait:Math.round((r.until||0)-S.T)})})()"""))
    print('ledger',await ev(LED))
    print('springs on a convoy',await ev("""(()=>{const r=window._R;if(!r||!S.raids.includes(r))return 'gone';let t=null;devLedger(()=>{t=haulSend('halcyon','hp','hr',{plate:20,wire:10},'test:2','supplies')});t.sector=r.sector;t.path=[r.sector,'hr'];t.leg=0;
      const n0=S.raids.includes(r);prwCatch();return JSON.stringify({convoyGone:!S.traders.includes(t),raid:S.raids.includes(r)?r.state:'wiped',loot:invMass(r.loot)})})()"""))
    print('ledger',await ev(LED))
    print('live prowl holds a gate',await ev("""(()=>{let r=null;S.T+=200;for(let i=0;i<20&&!r;i++)r=prwSend('pirate');if(!r)return 'none';RUN(()=>r.state==='wait'||!S.raids.includes(r),60);if(!S.raids.includes(r))return 'gone';const P=S.player;exitSector();P.sector=r.sector;P.docked=null;enterSector(r.sector);
      const g=Object.values(W.groups).find(x=>x.raid===r.id);const G=raidGoal(r);window._L=r;return JSON.stringify({live:r.live,wing:g&&g.members.length,goal:G.hold?'hold gate':Object.keys(G)[0]})})()"""))
    print('ledger',await ev(LED))
    print('it leaves when the wait is up',await ev("""(()=>{const r=window._L;if(!r)return 'none';r.until=S.T-1;return JSON.stringify({goal:Object.keys(raidGoal(r))[0]})})()"""))
    print('back out of sight',await ev("(()=>{const P=S.player;exitSector();P.sector='mw';enterSector('mw');return 'ok'})()"))
    print('ledger',await ev(LED))
    print('prowl meets a garrison',await ev("""(()=>{const ro=S.gar['S.hr'];const n0=ro.m.length;let r=null;const kit=raidShips('varkesh',[S.econ.fleet.varkesh,S.econ.stock.varkesh]);if(!kit)return 'no kit';r=raidSend('varkesh',{src:{sid:'vb',srcs:[S.econ.fleet.varkesh,S.econ.stock.varkesh],cap:null,reach:3,deep:true},tgt:null,dep:null,c:'hr'},kit);r.prowl=true;
      RUN(()=>r.state==='wait'||!S.raids.includes(r),80);const rnd0=Math.random;Math.random=()=>0;let res;try{r.skT=0;prwSkirmishes();res={raid:S.raids.includes(r)?r.ships.length:'wiped',garrison:n0+'->'+ro.m.length}}finally{Math.random=rnd0}return JSON.stringify(res)})()"""))
    print('ledger',await ev(LED))
    print('a force flies home',await ev("""(()=>{const st=S.econ.stock.halcyon,p0=st.plate||0,force={};devLedger(()=>{inv.add(st,'plate',9);inv.add(st,'wire',6)});for(let i=0;i<3;i++){const ld=loadout('patrol',1,'striker');takeFrom(ld,[st]);inv.addAll(force,ld)}const r=prwHome('halcyon','ke',force);const n=RUN(()=>!S.raids.includes(r),80);return JSON.stringify({token:!!r,ret:r&&r.ret,ships:r&&r.ships.length,home:n>=0,plateBack:(st.plate||0)-p0})})()"""))
    print('ledger',await ev(LED))
    print('an offensive flies to its target',await ev("""(()=>{let ev=null;for(let k=0;k<40&&!ev;k++){for(const f of ['varkesh','halcyon','ostrova','brood']){const n0=S.events.length;S.ai[f].next=0;planOffensive(f);const e=S.events.find(x=>x.type==='offensive'&&x.att===f&&x.stage==='inbound'&&!x.tr&&!x.trDone);if(e){ev=e;break}}}
      if(!ev)return 'no offensive';updateEvents();const r=S.raids.find(x=>x.strike===ev.id);window._EV=ev;return JSON.stringify({att:ev.att,to:ev.sector,token:!!r,hops:r?r.path.length-1:0,ships:r?r.ships.length:0,eta:ev.eta>1e11?'in transit':ev.eta})})()"""))
    print('ledger',await ev(LED))
    print('arrives and fights',await ev("""(()=>{const ev=window._EV;if(!ev)return 'none';for(let i=0;i<120&&ev.stage==='inbound';i++){S.T+=10;raidsTick();updateEvents()}return JSON.stringify({stage:ev.stage,token:!!S.raids.find(x=>x.strike===ev.id)})})()"""))
    print('ledger',await ev(LED))
    for i in range(3):await ev("(()=>{for(let i=0;i<30;i++){S.T+=10;strategicTick();updateEvents()}})()")
    print('an hour on',await ev(LED),await ev("JSON.stringify({raids:S.raids.length,prowls:S.raids.filter(r=>r.prowl).length,home:S.raids.filter(r=>r.ret).length})"))
    print('errors',errs[:4]);await b.close()
asyncio.run(main())
