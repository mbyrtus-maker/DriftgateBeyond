# Beyond: independent pilots (16zzzc_indep.js, agreed 7 Nov 2026). The opening population (4 a freeport, hauler / miner /
# fighter); a newcomer built from its freeport yard's store goods with a stake from the Compact, and nobody when the yard
# can't build; a posted job taken by the nearest free independent of the right line, flown from where it is and paid into its
# purse; the boards' jobs left alone for 8 minutes, then taken, flown and paid by the issuer; a maker's part bought off the
# shelf at the Market's price with the maker paid; shot down: no standing lost, its ship salvage, a rebuy at home, or
# retirement with its purse to the Compact; the label, the freeport's Overview; save and load. The ledger exact throughout.
import asyncio,json
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[];bad=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text and 'ERR_TUNNEL' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    async def led(what):
      l=await ev(LED);print('ledger',what,l)
      if l!='exact':bad.append(f'ledger after {what}: {l}')
    # the opening population
    r=json.loads(await ev("""(()=>{indInit();const L=indL(),by={};for(const I of L){const k=I.home+':'+I.line;by[k]=(by[k]||0)+1}return JSON.stringify({n:L.length,by,purses:[...new Set(L.map(I=>indPurse(I)))],cls:[...new Set(L.map(I=>I.cls))],sys:L.every(I=>Object.keys(I.sys).length===SLOTS.length),parts:L.every(I=>I.sl.length&&I.sl.every(s=>s.it))})})()"""))
    print('start',json.dumps(r))
    if r['n']!=12 or any(r['by'].get(f+':haul')!=2 or r['by'].get(f+':mine')!=1 or r['by'].get(f+':guard')!=1 for f in['mw','cw','ew']):bad.append(f'opening population: {r}')
    if not r['sys'] or not r['parts']:bad.append('an opening ship without its systems or parts')
    await led('the start')
    # a newcomer from the yard's goods and the Compact's stake; an empty yard sends nobody
    r=json.loads(await ev("""(()=>{running=false;const R=S.stations.cw,st=mkStock(R),need=indNeed('courier');devLedger(()=>inv.addAll(st,need));const s0={...st},n0=S.econ.treasury.neutral;
      const I=indAdd('cw','haul');const used={};for(const k in need)used[k]=(s0[k]||0)-(st[k]||0);const out={ok:!!I,cls:I&&I.cls,purse:I&&indPurse(I),compact:n0-S.econ.treasury.neutral,used,need};
      const park={...st};for(const k in park)inv.take(st,k,park[k]);const J=indAdd('cw','haul');inv.addAll(st,park);out.empty=J?'arrived':'nobody';return JSON.stringify(out)})()"""))
    print('newcomer',json.dumps(r))
    if not r['ok'] or r['cls']!='courier' or r['purse']!=1500 or r['compact']!=1500 or any(r['used'].get(k)!=v for k,v in r['need'].items()):bad.append(f'newcomer: {r}')
    if r['empty']!='nobody':bad.append('a newcomer arrived from an empty yard')
    await led('a newcomer')
    # a posted job: the nearest free independent hauler takes it, flies it and is paid into its purse
    print('depot',await ev("""(()=>{const P=S.player;undock();P.rp=5000;const sid=SECTOR_DEFS.map(d=>d.id).find(id=>!S.stations[id]&&canBuildIn(id,'player')&&!OUT_BY_SECTOR[id]&&S.sectors[id].ast.some(a=>!a.rift&&oreTotal(a)>40));exitSector();P.sector=sid;P.docked=null;enterSector(sid);P.cls='bulker';fitOf(P);refreshPlayerStats();devLedger(()=>{P.cargo={frame:2}});
      depFresh(P);const R=S.stations[sid];devLedger(()=>{inv.add(R.stock,'plate',40)});transfer('halcyon','player',20000);window._SID=sid;return sid})()"""))
    r=json.loads(await ev("""(()=>{const P=S.player,sid=window._SID;for(const I of indL())if(I.line==='haul'&&I.at==='dock'&&!I.live)I.go=null;pjPost(P,`${sid}:haul:plate:12:fast`);const j=S.pj[S.pj.length-1];j.claimAt=S.T;pjTick();const I=indOf(j.ind),r=pjRunOf(j.run);
      if(!I)return JSON.stringify({err:'not taken',state:j.state});window._J=j;window._I=I.id;window._p0=indPurse(I);const near=Math.min(...indL().filter(x=>x.line==='haul'&&x!==I&&indFree(x)).map(x=>indHop(x.sector,sid)));
      return JSON.stringify({who:j.who,by:j.by,line:I.line,at:I.at,run:!!r,rind:r&&r.ind,pick:r&&r.pick,cls:r&&r.cls,hops:indHop(I.sector,sid),nearestOther:near})})()"""))
    print('posted job taken',json.dumps(r))
    if r.get('err') or r['line']!='haul' or r['at']!='job' or not r['run'] or r['rind'] is None or r['pick']!='load' or not r['who'].endswith('(independent)') or r['hops']>r['nearestOther']:bad.append(f'posted job taken: {r}')
    r=json.loads(await ev("""(()=>{exitSector();W=null;const j=window._J;for(let i=0;i<600&&j.state!=='done';i++){S.T+=10;pjTick()}const I=indOf(window._I);enterSector(window._SID);
      return JSON.stringify({state:j.state,msg:j.msg,paid:j.paid,gain:indPurse(I)-window._p0,at:I.at,jobs:I.jobs,line:(()=>{coTab='crews';$('company').hidden=false;renderCompany();const t=$('coBody').innerText;$('company').hidden=true;return t.includes(I.name)})()})})()"""))
    print('posted job flown',json.dumps(r))
    if r['state']!='done' or not r['paid'] or r['gain']!=r['paid'] or r['at']=='job' or not r['line']:bad.append(f'posted job flown: {r}')
    await led('a posted job')
    # the boards: a freeport request untaken for less than 8 minutes is left alone, then taken, flown and paid by the Compact
    r=json.loads(await ev("""(()=>{exitSector();W=null;const A='mw',B='cw',R=S.stations[A];devLedger(()=>{inv.add(mkStock(R),'plate',30);for(let i=0;i<40&&!indSurplus(R,'plate');i++)inv.add(mkStock(R),'plate',10)});
      const L=indL().filter(I=>I.line==='haul'&&indFree(I)&&I.at==='dock');if(L.length<2)return JSON.stringify({err:'no free haulers'});const I=L[0],J=L[1];for(const X of[I,J]){X.sector=A;X.at='dock';X.go=null;X.restT=0;const top=indReserve(X)+300-indPurse(X);if(top>0)transfer('neutral',indW(X),top);else transfer(indW(X),'neutral',-top)}
      const k={id:S.nextId++,fac:'neutral',st:B,item:'plate',n:6,n0:6,reward:2400,until:S.T+3600};S.contracts.push(k);indStamp();window._K=k;
      const t0=IND.tradeHops;IND.tradeHops=0;indDecide(I);const early={ind:k.ind||null,go:I.go&&I.go.k};k.iT=S.T-IND.board-1;indDecide(J);IND.tradeHops=t0;window._BJ=J.id;window._bp0=indPurse(J);window._bn0=S.econ.treasury.neutral;
      return JSON.stringify({early,late:{ind:k.ind,me:J.id,go:J.go&&J.go.k,stage:J.go&&J.go.stage,src:J.go&&J.go.src,dst:J.go&&J.go.dst,held:J.hold.plate||0}})})()"""))
    print('board job',json.dumps(r))
    if r.get('err') or r['early']['ind'] or r['early']['go']=='board' or r['late']['ind']!=r['late']['me'] or r['late']['go']!='board' or r['late']['held']<1:bad.append(f'board job taken: {r}')
    r=json.loads(await ev("""(()=>{const k=window._K,J=indOf(window._BJ);for(let i=0;i<120&&S.contracts.includes(k)&&k.n>0;i++){S.T+=10;strategicTick();updateEvents()}
      return JSON.stringify({left:S.contracts.includes(k)?k.n:0,gain:indPurse(J)-window._bp0,stand:Math.round(standOf('neutral',J)*100)/100,rp:J.rp,at:J.at,sector:J.sector})})()"""))
    print('board job flown',json.dumps(r))
    if r['left']!=0 or r['gain']<2000 or r['stand']<=0 or r['sector']!='cw':bad.append(f'board job flown: {r}')
    await led('a board job')
    # buying: an empty slot filled with a maker's part off the shelf, the maker paid (85% after the station's dues)
    r=json.loads(await ev("""(()=>{for(const sid of FREEPORTS.map(F=>F.sid)){const R=S.stations[sid],ms=mkStock(R);for(const I of indL()){if(!indFree(I)||I.at!=='dock')continue;for(const s of I.sl){const id=Object.keys(ms).find(x=>ITEMS[x]&&ITEMS[x].maker&&ITEMS[x].part===s.k&&ms[x]>0&&(ITEMS[x].grade||1)<=gradeCap(I));if(!id)continue;
        I.sector=sid;inv.add(I.hold,s.it,1);s.it=null;transfer('neutral',indW(I),6000);const m=ITEMS[id].maker,t0=ceT(m),n0=ms[id],c0=indPurse(I),pr=mkPartPrice(R,id,I.cls);const others=I.sl.filter(x=>x!==s);const keep=others.map(x=>x.it);for(const x of others)x.it=x.it||'_';
        const sysK={...I.sys};for(const k in I.sys)I.sys[k]=I.sys[k];const P0=IND.perVisit;IND.perVisit=1;const n=indShop(I,R);IND.perVisit=P0;others.forEach((x,i)=>x.it=keep[i]);
        return JSON.stringify({kind:s.k,fitted:s.it,maker:ITEMS[s.it||'_']?ITEMS[s.it].maker:null,paid:c0-indPurse(I),quote:pr,makerGot:ceT(m)-t0,shelf:n0-(ms[id]||0),n})}}}return JSON.stringify({err:'no shelf part found'})})()"""))
    print('buys a part',json.dumps(r))
    if r.get('err'):print('  (skipped: no maker part on a freeport shelf for a fitted kind)')
    elif not r['fitted'] or not r['maker'] or r['paid']<r['quote'] or r['makerGot']<=0:bad.append(f'buying a part: {r}')
    await led('buying a part')
    # shot down in a live system: no standing lost, its ship and hold salvage, a rebuy at home; then one that can't pay retires
    r=json.loads(await ev("""(()=>{const P=S.player,sid=window._SID;if(!W||W.sid!==sid){exitSector();P.sector=sid;enterSector(sid)}const I=indL().find(x=>x.line==='guard'&&!x.live&&x.at!=='job');if(I.go&&I.go.kid){const k=S.contracts.find(c=>c.id===I.go.kid);if(k)k.ind=null}I.sector=sid;I.at='fly';I.path=[sid,NEIGH[sid][0]];I.leg=0;I.go={k:'look'};
      const H=S.stations[I.home];devLedger(()=>inv.addAll(mkStock(H),indNeed(IND.light[I.line])));transfer('neutral',indW(I),3000);const e=indSpawn(I,false);const lbl=shipLabel(e),st0=JSON.stringify(P.stand),cr0=S.sectors[sid].crates.length,lost0=I.lost||0;
      damageShip(e,5,'player',{src:W.player});killShip(e,'player',{src:W.player});const after=JSON.stringify(P.stand);
      return JSON.stringify({lbl,standSame:st0===after,crates:S.sectors[sid].crates.length-cr0,alive:!!indOf(I.id),cls:I.cls,at:I.at,home:I.sector===I.home,lost:(I.lost||0)-lost0,sys:Object.keys(I.sys).length})})()"""))
    print('shot down',json.dumps(r))
    if not r['lbl'].startswith('Independent · ') or not r['standSame'] or r['crates']<1 or not r['alive'] or r['at']!='dock' or not r['home'] or r['lost']!=1 or r['sys']!=8:bad.append(f'shot down: {r}')
    await led('shot down and rebought')
    r=json.loads(await ev("""(()=>{const sid=window._SID,I=indL().find(x=>x.line==='mine'&&!x.live&&x.at!=='job');I.sector=sid;I.at='fly';I.path=[sid,NEIGH[sid][0]];I.leg=0;I.go={k:'look'};transfer(indW(I),'player',indPurse(I));const n0=S.econ.treasury.neutral;
      const e=indSpawn(I,false);killShip(e,'pirate',{});return JSON.stringify({gone:!indOf(I.id),wallet:indW(I) in S.econ.treasury,n:indL().length})})()"""))
    print('retired',json.dumps(r))
    if not r['gone'] or r['wallet']:bad.append(f'retirement: {r}')
    await led('a retirement')
    # the freeport's Overview lists who is docked there
    r=await ev("""(()=>{const P=S.player,sid='mw';exitSector();P.sector=sid;enterSector(sid);P.docked='station';const I=indL().find(x=>x.at==='dock');if(I){I.sector=sid}const h=homeHtml(dockCtx(),P,[],W.player);P.docked=null;return JSON.stringify({has:h.includes('Independents here'),name:!!I&&h.includes(esc(I.name))})})()""")
    print('overview',r)
    if '"has":true' not in r or '"name":true' not in r:bad.append('freeport Overview: '+r)
    # save and load, with one in flight in the open system
    r=json.loads(await ev("""(()=>{const sid=S.player.sector,I=indL().find(x=>x.line==='haul'&&!x.live&&x.at!=='job');if(I.go&&I.go.kid){const k=S.contracts.find(c=>c.id===I.go.kid);if(k)k.ind=null}I.sector=sid;I.at='fly';I.path=[sid,NEIGH[sid][0]];I.leg=0;I.go={k:'look'};devLedger(()=>{I.hold.fe=(I.hold.fe||0)+3});const e=indSpawn(I,false);
      const names=indL().map(x=>x.name+':'+indPurse(x)).join('|'),s=serialize(),txt=JSON.stringify(s);exitSector();W=null;for(const x of indL())x.name='?';const fresh=indL().map(x=>x.name).join('|');startWith(JSON.parse(txt));
      const back=indL().map(x=>x.name+':'+indPurse(x)).join('|'),J=indOf(I.id),live=!!W&&W.ents.some(x=>x.indId===I.id),full=!!W&&!indRoomW(W);return JSON.stringify({same:back===names,fresh:fresh!==names,live,full,fe:J?(J.hold.fe||0)+(((W.ents.find(x=>x.indId===I.id)||{}).cargo||{}).fe||0):-1})})()"""))
    print('save and load',json.dumps(r))
    if not r['same'] or not r['fresh'] or not (r['live'] or r['full']) or r['fe']<3:bad.append(f'save and load: {r}')
    await led('save and load')
    print('errors',errs[:4]+bad);await b.close()
asyncio.run(main())
