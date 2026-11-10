# Beyond, reasons to stop at a depot (9 Nov 2026): front levels; Depot missions as their own Jobs category, listed within
# 6 jumps and taken only at the depot; Defend pays by the minute and a hold bonus; Sweep counts kills; salvage sells at a
# premium at a power's depot; a power's own stolen cargo is handed back for a finder's fee; the ledger stays exact
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
    # a depot made Front (damaged) with a raid on its way
    r=json.loads(await ev("""(()=>{running=false;exitSector();W=null;for(let i=0;i<4;i++){S.T+=10;strategicTick();updateEvents()}const P=S.player;
      const R=Object.values(S.stations).find(x=>isDepotF(x)&&HOP[P.sector][x.sid]<=DPM.near);R.hull=R.hMax*.8;S.raids=S.raids||[];S.raids.push({id:999001,dep:R.sid,side:'pirate',fake:1});S.dpmT=0;dpmTick();
      const L=dpmAll().filter(m=>m.sid===R.sid);window._R=R.sid;return JSON.stringify({sid:R.sid,lvl:dpLvl(R.sid),kinds:L.map(m=>m.k),levels:Object.values(S.dpf).filter(x=>x>0).length})})()"""))
    check('a damaged depot is Front and posts depot missions, Defend among them',r['lvl']==2 and 'def' in r['kinds'] and len(r['kinds'])<=3,r)
    # elsewhere: listed under Depot missions, taken only at the depot
    r=json.loads(await ev("""(()=>{const P=S.player,sid=window._R;P.sector='mw';P.docked='station';enterSector('mw');running=false;const c=dockCtx();const L=jobsList(c,P,[P.cargo,c.storage]).filter(j=>j.ty==='depot');
      dockTab='jobs';jobFilter='depot';renderDock();const bar=[...document.querySelectorAll('[data-act=jfil]')].map(b=>b.textContent).join('|');
      const d=L.find(j=>j.id.startsWith('dpm:')&&dpmAll().find(m=>'dpm:'+m.id===j.id).k==='def');const id=d&&+d.id.slice(4);dockAction('dpmtake',id);const msg=dockErr;
      return JSON.stringify({n:L.length,need:d&&d.need,btn:d&&d.btn,bar,msg,taken:!!(dpmAll().find(m=>m.id===id)||{}).taker,id})})()"""))
    check('elsewhere it is listed under Depot missions, telling the pilot to fly there',r['n']>0 and 'Depot missions' in r['bar'] and 'Fly to' in (r['need'] or '') and r['btn'][0]=='croute',r)
    check('it can\'t be taken from another station',not r['taken'] and 'Fly to' in r['msg'],r)
    did=r['id']
    r=json.loads(await ev(f"""(()=>{{const P=S.player,sid=window._R;exitSector();W=null;P.sector=sid;enterSector(sid);running=false;P.docked='station';dockAction('dpmtake',{did});const m=dpmAll().find(x=>x.id==={did});const msg=dockErr;
      const other=dpmAll().find(x=>x.sid===sid&&!x.taker);let msg2='';if(other){{dockAction('dpmtake',other.id);msg2=dockErr}}
      P.docked=null;const c0=P.credits,t0=S.econ.treasury[m.f];S.T+=60;S.dpmT=0;dpmTick();const perMin=P.credits-c0;
      S.raids=S.raids.filter(x=>!x.fake);S.T+=30;S.dpmT=0;dpmTick();const hold=P.credits-c0-perMin;return JSON.stringify({{msg,taken:!!m.taker,msg2,perMin,hold,gone:!dpmAll().includes(m),paidBy:t0-S.econ.treasury[m.f]}})}})()"""))
    check('at the depot the pilot takes it; a second depot mission is refused',r['taken'] and ('already' in r['msg2'] or r['msg2']==''),r)
    check('Defend pays by the minute in the system and a hold bonus when the attack ends, from the power',r['perMin']>=80 and r['hold']>=2000 and r['gone'] and r['paidBy']>=r['perMin']+r['hold']-1,r)
    # Sweep: kills count
    r=json.loads(await ev("""(()=>{const P=S.player,sid=window._R;let m=dpmAll().find(x=>x.sid===sid&&x.k==='swp');if(!m){S.dpmT=0;dpmTick();m=dpmAll().find(x=>x.sid===sid&&x.k==='swp')}if(!m)return JSON.stringify({none:1});
      m.taker=pkeyOf(P);m.tk=S.T;m.prog=0;const c0=P.credits;for(let i=0;i<m.n;i++)sideKill({side:'brood',role:'patrol',cls:'interceptor',alive:false},{[pkeyOf(P)]:1},pkeyOf(P));return JSON.stringify({paid:P.credits-c0,gone:!dpmAll().includes(m),n:m.n})})()"""))
    check("Sweep: kills of the power's enemies count, pay each, and the last pays the completion bonus",r.get('gone') and r.get('paid',0)>=r.get('n',4)*300+1800,r)
    # salvage and a stolen return at the depot
    r=json.loads(await ev("""(()=>{const P=S.player,sid=window._R,R=S.stations[sid],f=R.owner;P.docked='station';const c=dockCtx();devLedger(()=>{inv.add(P.cargo,'plate',6);inv.add(P.cargo,'wire',4)});
      crateTake(P,{side:'brood'},'plate');for(let i=0;i<5;i++)salvAdd(P,'plate','brood',1);const pr=mSell(c,'plate'),c0=P.credits;mkFilter=mkGroup('plate');const html=mkHtml(c,P);
      let prem=0;for(let i=0;i<6;i++){dockErr='';dockAction('sell','plate:1');const mm=/Salvage premium: \\+([\\d,]+)/.exec(dockErr||'');if(mm)prem+=+mm[1].replace(/,/g,'')}const got=P.credits-c0;
      stolAdd(P,'wire',f,4);P.heat={[f]:30};const s0=dStore(R).wire||0,c1=P.credits;dockAction('dpret','wire');return JSON.stringify({pr,got,prem,box:/Salvage at/.test(html)&&/\\+80%/.test(html),ret:(dStore(R).wire||0)-s0,fee:P.credits-c1,heat:P.heat[f],msg:dockErr,stol:!!(P.stol&&P.stol.wire)})})()"""))
    check("Brood salvage sells at a power's depot for 80% over the price, and the Market says so",r['box'] and r['prem']>=6*r['pr']*.8*.8 and r['prem']<=6*r['pr']*.8+1,r)
    check("a power's own stolen cargo goes back into the depot's store for a finder's fee, with the heat eased",r['ret']==4 and r['fee']>0 and r['heat']<30 and not r['stol'],r)
    r=json.loads(await ev("""(()=>{const P=S.player;P.docked=null;const s=S.sectors[W.sid];s.wrecks=s.wrecks||[];const w={id:999002,side:'varkesh',name:'Test hulk',x:W.player.x+50,y:W.player.y,z:W.player.z,pts:[],until:S.T+200};s.wrecks.push(w);
      devLedger(()=>blCloud(s,{x:w.x,y:w.y,z:w.z},{plate:3},10,0,'x',null,1));const c=s.clouds[s.clouds.length-1];const p0=(P.salv&&P.salv.plate&&P.salv.plate['wk:999002:varkesh'])||0;
      const bc=blColl;blColl=()=>5;for(let i=0;i<40&&s.clouds.includes(c);i++)blCollect(W.player,P,c,1,s);blColl=bc;s.wrecks=s.wrecks.filter(x=>x!==w);return JSON.stringify({ore:c.ore,left:s.clouds.includes(c),room:W.player.st.cargo-invMass(P.cargo),coll:blColl(P),wk:c.wk,marked:((P.salv&&P.salv.plate&&P.salv.plate['wk:999002:varkesh'])||0)-p0})})()"""))
    check('chunks blasted off a wreck carry its salvage mark when scooped',r['wk']=='wk:999002:varkesh' and r['marked']==3,r)
    l=await ev(LED);check('ledger exact',l=='exact',l)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
