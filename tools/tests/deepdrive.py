# Beyond (7 Nov 2026): Ostrova's Deep Drive. FPK.deep (0.75) shortens every travel time and jump spin-up of things Ostrova
# owns: a capital's spin-up live (against a Halcyon one side by side), its hops off-screen, a response wing's ETA for the same
# hops, a convoy's and a raid party's hops on the lanes, a pilot in an Ostrova-line hull (the gate's hold and the peek spool);
# the trait text and the Allegiance tab show it, and the figure follows the dial; the ledger stays exact; no page errors
import asyncio,json
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
fails=[]
def check(name,ok,v):
  print(name,'OK' if ok else 'FAIL',v)
  if not ok:fails.append(name)
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await ev("S.T=Math.max(S.T,400);1")
    v=json.loads(await ev("JSON.stringify({deep:FPK.deep,ext:FAC_IDS.map(f=>BAL.ext&&BAL.ext[f]!==undefined?BAL.ext[f]:1)})"))
    check('dial',v['deep']==0.75,v)
    # 1. live spin-up: an Ostrova escort and a Halcyon escort side by side in the open, both told to jump to the same neighbour
    v=json.loads(await ev("""(()=>{const P=S.player;const sid=P.sector;const nx=NEIGH[sid][0];let a=null,h=null;devLedger(()=>{a=makeEscort('ostrova',sid,{});h=makeEscort('halcyon',sid,{})});
      for(const t of[a,h]){t.dest=nx;t.call={until:S.T+1e6,sid:nx};t.jumpTo=nx}window._A=a;window._H=h;window._A0=sid;strategicTick();
      return JSON.stringify({sid,nx,liveA:!!a.live,liveH:!!h.live,kA:+capJumpK(a).toFixed(3),kH:+capJumpK(h).toFixed(3),sA:+(JUMP_TIME/capJumpK(a)).toFixed(1),sH:+(JUMP_TIME/capJumpK(h)).toFixed(1)})})()"""))
    check('capital spin-up rate',abs(v['kA']/v['kH']-1/0.75)<1e-3,v)
    await pg.wait_for_timeout(3000)
    v=json.loads(await ev("""(()=>{const a=window._A,h=window._H;const pa=a.spin?a.spin.p:(a.sector!==window._A0?1:0),ph=h.spin?h.spin.p:0;return JSON.stringify({pA:+pa.toFixed(3),pH:+ph.toFixed(3),r:ph>0?+(pa/ph).toFixed(2):null,secA:a.sector,secH:h.sector})})()"""))
    check('Ostrova spins up faster live',v['pH']>0 and v['pA']>v['pH'] and abs(v['r']-1/0.75)<0.15,v)
    await ev("(()=>{for(const t of[window._A,window._H]){t.dest=null;t.jumpTo=null;t.call=null;t.spin=null}return 1})()")
    print('ledger',await ev(LED))
    # 2. off-screen hops: the same capital, counted in strategic ticks per hop
    v=json.loads(await ev("""(()=>{const run=side=>{const t={side,cls:'carrier',moveT:0};let ticks=0,hops=0;while(hops<40&&ticks<400){ticks++;if(capMoveStep(t))hops++}return ticks};
      const r={halcyon:run('halcyon'),ostrova:run('ostrova'),varkesh:run('varkesh'),escO:(()=>{const t={side:'ostrova',cls:'escort',moveT:0};let k=0,h=0;while(h<40&&k<400){k++;if(capMoveStep(t))h++}return k})()};return JSON.stringify(r)})()"""))
    check('Ostrova capital hops off-screen in 3/4 the ticks (40 hops)',v['halcyon']==80 and v['varkesh']==80 and abs(v['ostrova']-60)<=1 and abs(v['escO']-60)<=1,v)
    # 3. a response wing: the ETA for the same hops
    v=json.loads(await ev("""(()=>{const out={};for(const f of['ostrova','halcyon']){let ev=null,sid=null;for(const d of SECTOR_DEFS){const s=respSource(f,d.id);if(!s||s.h!==2)continue;if(S.events.some(e=>e.type==='response'&&e.att===f&&e.sector===d.id))continue;ev=dispatchResponse(f,d.id,'distress');if(ev){sid=d.id;break}}
      if(!ev){out[f]='none';continue}const h=respSource(f,sid).h;out[f]={hops:h,eta:Math.round(ev.eta-S.T),base:25+22*h};inv.addAll(S.econ.stock[f],ev.force);ev.force={};ev.stage='done';S.events=S.events.filter(e=>e!==ev)}return JSON.stringify(out)})()"""))
    check('response wing ETA',isinstance(v.get('ostrova'),dict) and isinstance(v.get('halcyon'),dict) and v['halcyon']['eta']==v['halcyon']['base'] and abs(v['ostrova']['eta']-v['ostrova']['base']*0.75)<=1,v)
    print('ledger',await ev(LED))
    # 4. a convoy's hop and a raid party's hop on the lanes
    v=json.loads(await ev("""(()=>{const out={},P0=S.player.sector;const L=SECTOR_DEFS.map(d=>d.id);let a=null,c=null;for(const x of L){for(const y of L){const p=trPath(x,y);if(x!==P0&&p&&p.length>=4){a=x;c=y;break}}if(a)break}
      for(const f of['ostrova','halcyon']){let t=null;devLedger(()=>{t=haulSend(f,a,c,{plate:6},'ddtest:'+f,'supplies')});tradersTick();const first=+(t.next-S.T).toFixed(2);t.next=S.T;t.live=false;tradersTick();out[f]={first,hop:+(t.next-S.T).toFixed(2),leg:t.leg}}
      return JSON.stringify(out)})()"""))
    check('convoy hop',abs(v['halcyon']['hop']-45)<1e-6 and abs(v['ostrova']['hop']-45*0.75)<1e-6 and abs(v['ostrova']['first']-v['halcyon']['first']*0.75)<.02,v)
    v=json.loads(await ev("""(()=>{const out={};for(const f of['ostrova','halcyon']){const srcs=[S.econ.fleet[f],S.econ.stock[f]];const kit=raidShips(f,srcs);if(!kit){out[f]='no kit';continue}const from=homeOf(f),to=NEIGH[from].find(n=>NEIGH[n].length>1)||NEIGH[from][0];
      const r=raidSend(f,{src:{sid:from,srcs,cap:null,reach:3,deep:true},tgt:null,dep:null,c:NEIGH[to].find(n=>n!==from)||to},kit);r.prowl=true;raidsTick();updateEvents();out[f]={hop:+(r.next-S.T).toFixed(2),state:r.state}}return JSON.stringify(out)})()"""))
    check('raid hop',isinstance(v.get('ostrova'),dict) and isinstance(v.get('halcyon'),dict) and abs(v['halcyon']['hop']-35)<1e-6 and abs(v['ostrova']['hop']-35*0.75)<1e-6,v)
    print('ledger',await ev(LED))
    # 5. a pilot flying an Ostrova design-line hull: the gate's hold and the peek spool
    v=json.loads(await ev("""(()=>{const P=S.player,f0=P.faction,o={};for(const f of['halcyon','varkesh','ostrova']){P.faction=f;o[f]={gate:unbGateHold(),peek:PEEK.spool}}P.faction=f0;return JSON.stringify(o)})()"""))
    check('pilot in an Ostrova line',v['halcyon']['gate']==5 and v['varkesh']['gate']==5 and abs(v['ostrova']['gate']-3.75)<1e-9 and abs(v['ostrova']['peek']-6)<1e-9,v)
    # 6. shown in the game: trait text, the Allegiance tab's table, and the figure follows the dial
    v=json.loads(await ev("""(()=>{const t=FACTIONS.ostrova.traitText,h=allegianceHtml(S.player);FPK.deep=.7;const t7=FACTIONS.ostrova.traitText;FPK.deep=.75;return JSON.stringify({t,inTab:h.includes('Deep Drive: jumps and travel a quarter faster'),t7:t7.match(/Deep Drive[^<]*/)[0],others:FACTIONS.halcyon.traitText.includes('Deep Drive')||FACTIONS.varkesh.traitText.includes('Deep Drive'),archive:t.includes('Archive fleet')})})()"""))
    check('trait text',('Deep Drive: jumps and travel a quarter faster' in v['t']) and v['inTab'] and v['t7']=='Deep Drive: jumps and travel 30% faster' and not v['others'] and v['archive'],v)
    # 7. half an hour of the galaxy with everything flying: still exact
    for i in range(3):await ev("(()=>{for(let i=0;i<60;i++){S.T+=10;strategicTick();updateEvents()}})()")
    led=await ev(LED);check('ledger after an hour',led=='exact',led)
    print('errors',errs[:4])
    print('ALL OK' if not fails and not errs else 'FAILED '+','.join(fails));await b.close()
asyncio.run(main())
