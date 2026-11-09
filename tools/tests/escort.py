# Beyond, escorts (8 Nov 2026): escort pay 150 cr a jump; an independent miner going into deep or unfriendly space hires a
# guard (Jobs), waits for it, and pays it 150 cr a jump and 50 cr a minute while it mines, from its own purse, up to what it
# set aside; the host marks the ship each pilot escorts (P.fmE); J on it flies in formation, hostile fighters break it off,
# and when it vanishes at a gate you jump with it; an escorted freighter at its gate with its escort near jumps at once;
# the ledger stays exact throughout
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
    check('escort pay is 150 cr a jump',await ev("ESC_CV.hop===150&&cvPay({load:{}},3)===510"))
    # an independent miner hires a guard for a trip into deep space
    r=json.loads(await ev("""(()=>{running=false;for(let i=0;i<6&&!indAll().some(x=>x.role==='miner');i++){S.T+=10;strategicTick()}const I=indAll().find(x=>x.role==='miner'&&x.st!=='down'&&!x.live);if(!I)return JSON.stringify({miner:false});I.st='dock';I.sector=I.port;I.run=null;I.hire=null;I.guard=null;
      transfer('neutral',indW(I),4000);const to=Object.keys(DEF).filter(s=>DEF[s].kind==='deep'&&indHops(I.sector,s)<=3).sort((a,b)=>indHops(I.sector,a)-indHops(I.sector,b))[0];
      const P=S.player;exitSector();W=null;P.sector=I.sector;enterSector(I.sector);running=false;P.docked='station';
      indGo(I,'mine',to,{});const H=I.hire,waits=I.st==='dock'&&H&&H.st==='wait';indPlan(I);const still=I.st==='dock';
      const L=jobsList(dockCtx(),P,[P.cargo,P.vault]),row=L.find(x=>x.id==='igd:'+I.id);dockAction('igtake',I.id);const took=dockErr;
      return JSON.stringify({miner:true,id:I.id,to,why:H&&H.why,cap:H&&H.cap,waits,still,onBoard:!!(row&&row.btn&&row.btn[0]==='igtake'),issuer:row?jbIssuer(row):'',took,guard:!!I.guard})})()"""))
    check('a miner going into deep space hires a guard and waits at its freeport',r.get('miner') and r.get('why')=='into deep space' and r.get('cap',0)>=400 and r.get('waits') and r.get('still'),r)
    check('the guard job is on the Jobs board, from the miner, and the pilot takes it',r.get('onBoard') and 'independent' in r.get('issuer','') and r.get('guard'),r)
    iid=r.get('id')
    r=json.loads(await ev(f"""(()=>{{const I=indById({json.dumps(iid)});igStep(I);return JSON.stringify({{st:I.st,hire:I.hire&&I.hire.st,run:I.run&&I.run.k}})}})()"""))
    check('with its guard in the system it sets off',r['st']=='go' and r['hire']=='out' and r['run']=='mine',r)
    # a jump with it pays 150 cr; a minute within 2.5 km while it mines pays 50 cr
    r=json.loads(await ev(f"""(()=>{{const I=indById({json.dumps(iid)}),P=S.player,G=I.guard,c0=P.credits,p0=indPurse(I);
      const nx=I.run.path[1]||I.run.to;I.sector=nx;fmHost(.01);const jump=P.credits-c0;
      I.run.to=nx;I.st='work';I.live=false;exitSector();W=null;P.sector=nx;P.docked=null;enterSector(nx);running=false;const e=W.ents.find(x=>x.alive&&x.indId===I.id)||indSpawn(I,false);
      const p=W.player;p.x=e.x+200;p.y=e.y;p.z=e.z;p.vx=p.vy=p.vz=0;const c1=P.credits;fmHost(.3);fmHost(61);const min=P.credits-c1;
      return JSON.stringify({{jump,min,paid:G.paid,purse:p0-indPurse(I),fmE:P.fmE,eid:e.id}})}})()"""))
    check('a jump with it pays 150 cr and a minute guarding it pays 50 cr, from its purse',r['jump']==150 and r['min']==50 and r['paid']==200 and r['purse']==200,r)
    check('the host marks the ship the pilot is guarding (P.fmE)',r['fmE']==r['eid'],r)
    l=await ev(LED);check('ledger exact after guard pay',l=='exact',l)
    # formation: J on it flies alongside; a hostile fighter breaks it off; it vanishing at a gate takes you through with it
    r=json.loads(await ev("""(()=>{const p=W.player,E=fmEnt();W.tgt={kind:'ship',ref:E};apOn=false;toggleAutopilot();const on=!!(W.fmn&&apOn&&W.fmn.ref===E);
      for(const x of W.ents.slice())if(x.type==='ship'&&x.alive&&!x.isPlayer&&x!==E&&hostile('player',x.side))despawn(x);E.vx=60;E.vy=0;E.vz=0;p.x=E.x+600;p.y=E.y;p.z=E.z;p.vx=p.vy=p.vz=0;const d0=d3(p,E);for(let i=0;i<90;i++){autopilot(p,1/30);p.x+=p.vx/30;p.y+=p.vy/30;p.z+=p.vz/30;E.x+=E.vx/30}const closing=!!W.fmn&&d3(p,E)<d0-100;
      const H=makeNPC('patrol','pirate','interceptor',1,{},'test');H.x=p.x+900;H.y=p.y;H.z=p.z;W.ents.push(H);autopilot(p,1/30);const broke=!W.fmn&&!apOn&&W.tgt&&W.tgt.ref===H;H.alive=false;W.ents.splice(W.ents.indexOf(H),1);
      W.tgt={kind:'ship',ref:E};toggleAutopilot();const back=!!W.fmn;const g=GATES[W.sid][0];E.x=g.x*.97;E.y=g.y*.97;E.z=g.z*.97;p.x=E.x+150;p.y=E.y;p.z=E.z;autopilot(p,1/30);despawn(E);autopilot(p,1/30);
      const J=W.jump;return JSON.stringify({on,closing,broke,back,jump:J?J.to:null,gate:g.to})})()"""))
    check('J on the guarded ship starts formation and closes on its slot',r['on'] and r['closing'],r)
    check('a hostile fighter near breaks formation and is targeted',r['broke'],r)
    check('when it vanishes at a gate you jump through with it',r['back'] and r['jump']==r['gate'],r)
    r=json.loads(await ev(f"""(()=>{{W.jump=null;W.player.inJump=false;const I=indById({json.dumps(iid)});I.live=false;I.st='go';I.run={{k:'home',to:I.sector,path:[I.sector],leg:0,next:S.T,T0:S.T}};indArrive(I);return JSON.stringify({{hire:!!I.hire,guard:!!I.guard}})}})()"""))
    check('the job ends when the miner docks again',not r['hire'] and not r['guard'],r)
    # an escorted freighter at its gate with its escort near jumps at once
    r=json.loads(await ev("""(()=>{const P=S.player,f=P.sworn||'halcyon';const g=GATES[W.sid][0];const st=S.econ.stock[f];inv.add(st,'fe',0);const n=Math.min(5,st.fe||0);if(!n)return JSON.stringify({sent:false,why:'no fe'});inv.take(st,'fe',n);const t=haulSend(f,W.sid,g.to,{fe:n},'test:hop','test',null);if(!t){inv.add(st,'fe',n);return JSON.stringify({sent:false})}
      cvSign(t,pkeyOf(P),P.name);let e=W.ents.find(x=>x.alive&&x.tradeT===t);if(!e){t.live=false;e=spawnTrader(t,false)}const ge=W.ents.find(x=>x.type==='gate'&&x.to===g.to);e.ai.dest=ge;e.ai.arrived=false;
      e.x=ge.x*.97;e.y=ge.y*.97;e.z=ge.z*.97;const p=W.player;p.x=e.x+150;p.y=e.y;p.z=e.z;const s0=t.sector;traderThink(e,1/30);
      return JSON.stringify({sent:true,hopped:t.sector===g.to&&s0!==t.sector,gone:!W.ents.includes(e),hops:t.esc?t.esc.hops:-1})})()"""))
    check('an escorted freighter reaching its gate with its escort near jumps at once (and the jump counts)',r.get('hopped') and r.get('gone') and r.get('hops')==1,r)
    l=await ev(LED);check('ledger exact at the end',l=='exact',l)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
