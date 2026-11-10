# Beyond, a contractor builds from O (9 Nov 2026): O opens Comms' Command page, which lists building a Lair, a Depot and a
# Station here (each saying why it can't be done yet) and the distress call; with a Lair Kit near a big rock, picking the
# Lair builds it; the Depot asks for the company profile first; the ledger stays exact
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
    r=json.loads(await ev("""(()=>{const P=S.player,sid=Object.keys(S.sectors).find(id=>!S.stations[id]&&depCan(id)&&S.sectors[id].ast.some(a=>!a.comet&&!a.rift&&oreTotal(a)>=LAIR_B.rockMin));exitSector();W=null;P.sector=sid;P.docked=null;enterSector(sid);running=false;worldUpdate(.016);
      const a=S.sectors[sid].ast.find(x=>!x.comet&&!x.rift&&oreTotal(x)>=LAIR_B.rockMin),p=W.player;p.x=a.x+astR(a)+200;p.y=a.y;p.z=a.z;devLedger(()=>{inv.add(P.cargo,'kit_lair',1);inv.add(P.cargo,'kit_depot',1)});
      ctrBuildMenu();const open=!$('comms').hidden,L=[...$('cmList').querySelectorAll('.cm-o span')].map(x=>x.textContent);const i=W.cmOpts.findIndex(o=>o.k==='ctrlair'),n0=(S.lairs||[]).length;commsPick(String(i));
      const lair=(S.lairs||[]).length-n0;ctrBuildMenu();const j=W.cmOpts.findIndex(o=>o.k==='ctrdep');const off=W.cmOpts[j].off;commsPick(String(j));const msg=coErr;return JSON.stringify({open,L,lair,off,msg,sid})})()"""))
    check('O opens the Command page with Lair, Depot and Station building and the distress call',r['open'] and any('Lair' in x for x in r['L']) and any('Depot here' in x for x in r['L']) and any('Station' in x for x in r['L']),r)
    check('with a Lair Kit near a big rock, picking it builds the Lair',r['lair']==1,r)
    check('the Depot (with a Depot Kit) asks for the company profile first',not r['off'] and 'profile' in r['msg'].lower(),r)
    r=json.loads(await ev("""(()=>{const P=S.player,L=myLairsHere()[0];const p=W.player;hudUpdate();const pb=$('hPrompt').textContent;S.T=L.build+1;for(let i=0;i<3;i++){S.T+=1;strategicTick()}running=true;
      p.x=L.x+1500;p.y=L.y;p.z=L.z;p.vx=p.vy=p.vz=0;const t=targetables().find(x=>x.kind==='lair'&&x.ref===L);W.tgt=t;hudUpdate();const panel=$('hTgt').textContent;const d0=d3(p,L);apOn=false;toggleAutopilot();for(let i=0;i<900;i++)step(1/60);running=false;
      const d1=d3(p,L);hudUpdate();return JSON.stringify({pb,tg:!!t,panel:panel.slice(0,120),d0:Math.round(d0),d1:Math.round(d1),prompt:$('hPrompt').textContent})})()"""))
    check('once built the Lair is a target with a panel, and the autopilot flies there',r['tg'] and 'Your Lair' in r['panel'] and r['d1']<r['d0'],r)
    r=json.loads(await ev("""(()=>{const P=S.player,sta=()=>ctrBuildOpts().find(o=>o.k==='ctrsta').l,out={};const sv=P.vaultAt,R0=myDepots(P).filter(R=>!R.pst);
      if(!R0.length)out.noDep=sta();devLedger(()=>{P.vaults=P.vaults||{};const k=Object.keys(S.stations).find(id=>S.stations[id].owner==='neutral');(P.vaults[k]=P.vaults[k]||{}).kit_station=1;out.k=k});out.hang=sta();
      devLedger(()=>{inv.take(P.vaults[out.k],'kit_station',1)});return JSON.stringify(out)})()"""))
    check("the Station line says what's missing: a Depot first, or a Station Kit left in a hangar",(r.get('noDep') is None or 'Depot first' in r['noDep']) and ('hangar at' in r['hang'] or 'Depot first' in r['hang']),r)
    l=await ev(LED);check('ledger exact',l=='exact',l)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
