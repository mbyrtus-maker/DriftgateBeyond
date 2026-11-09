# Beyond, base kits (8 Nov 2026): Lair, Depot and Station kits made from the bases' recipes, 150 / 180 / 220 t, only a Heavy
# Hauler's hold takes one; every market has one of each while a pilot is docked (assembled from its own store) and breaks
# unsold ones back into exactly what they were made from when nobody is docked; a kit in the hold builds a Lair, a Depot
# (any hull, no Constructor) and upgrades a Depot to a Station; the ledger stays exact throughout
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
    check('three kits: 150, 180 and 220 t, made from the bases\' recipes',await ev("mass('kit_lair')===150&&mass('kit_depot')===180&&mass('kit_station')===220&&ITEMS.kit_depot.recipe.frame===2&&ITEMS.kit_station.recipe.keel===1&&CRAFTABLE.includes('kit_station')"))
    # docked at a power's station: one of each on its market, from its own store
    r=json.loads(await ev("""(()=>{running=false;const P=S.player;const R=mkStations().find(x=>FAC_IDS.includes(x.owner)&&x.kind==='core');exitSector();W=null;P.sector=R.sid;enterSector(R.sid);running=false;P.docked='station';
      const mk=storeOf(R),c0={...mk};kitTick();const c=dockCtx(),on=['kit_lair','kit_depot','kit_station'].map(k=>c.market[k]||0);
      const grp=mkGroup('kit_depot'),v=invVec(c0),cv=comp('kit_station');return JSON.stringify({sid:R.sid,on,rec:(S.kitShelf[kitKey(R)]||[]).length,grp,short:RAWS.filter(e=>v[e]<cv[e]).map(e=>e+':'+Math.round(v[e])+'<'+cv[e]),raw:RAWS.map(e=>e+(c0[e]||0)).join(' ')})})()"""))
    check('a docked pilot finds the kits its store can make on a power\'s market (Components)',r['on'][:2]==[1,1] and r['on'][2]==(0 if r['short'] else 1) and r['rec']==sum(r['on']) and r['grp']=='comp',r)
    l=await ev(LED);check('ledger exact with kits on the shelf',l=='exact',l)
    # a Light Hauler buys a Depot Kit: it goes to the hangar and can't be loaded; a Heavy Hauler loads it
    r=json.loads(await ev("""(()=>{const P=S.player,c=dockCtx();transfer(c.wallet,'player',200000);{const l0=ledger();P.cls='courier';P.fit=fitNew('courier',null);const l1=ledger();for(const e of RAWS)S.ledger0.tot[e]+=l1.tot[e]-l0.tot[e]}
      exitSector();enterSector(P.sector);running=false;P.docked='station';const c2=dockCtx();dockAction('buy','kit_depot:1');const bought=dockErr,inVault=c2.storage.kit_depot||0,inHold=P.cargo.kit_depot||0;dockAction('mv','kit_depot:out:1');const refused=dockErr;
      {const l0=ledger();P.cls='bulker';P.fit=fitNew('bulker',null);const l1=ledger();for(const e of RAWS)S.ledger0.tot[e]+=l1.tot[e]-l0.tot[e]}exitSector();enterSector(P.sector);running=false;P.docked='station';
      dockAction('mv','kit_depot:out:1');const loaded=P.cargo.kit_depot||0;kitTick();const restock=dockCtx().market.kit_depot||0;
      return JSON.stringify({bought,inVault,inHold,refused,loaded,restock})})()"""))
    check('bought in a Light Hauler, a Depot Kit goes to the hangar and won\'t load',r['inVault']==1 and r['inHold']==0 and 'Heavy Hauler' in r['refused'],r)
    check('a Heavy Hauler loads it, and the market restocks another',r['loaded']==1 and r['restock']==1,r)
    # buy the Station Kit and the Lair Kit too, then leave: the unsold shelf is broken back into its store
    r=json.loads(await ev("""(()=>{const P=S.player;const R=S.stations[P.sector];P.docked=null;kitTick();const mk=storeOf(R);const left=['kit_lair','kit_depot','kit_station'].map(k=>mk[k]||0),rec=!!S.kitShelf[kitKey(R)];
      return JSON.stringify({a:1,left,rec})})()"""))
    check('undocked, the shelf\'s kits are broken back into its store',r['a']==1 and r['left']==[0,0,0] and not r['rec'],r)
    l=await ev(LED);check('ledger exact after buying and breaking up kits',l=='exact',l)
    # deploy: a Depot from the kit (no Constructor), then the Station Kit upgrades it
    r=json.loads(await ev("""(()=>{const P=S.player;const sid=Object.keys(DEF).find(s=>depCan(s)&&DEF[s].kind!=='hive'&&DEF[s].kind!=='den');exitSector();W=null;P.sector=sid;enterSector(sid);running=false;P.docked=null;
      const msg=depFresh(P),R=S.stations[sid];const dep=!!(R&&R.owner==='player'),kit=P.cargo.kit_depot||0;
      const F=mkStations().find(x=>x.owner==='neutral'&&kitPlan(storeOf(x),'kit_station'));exitSector();W=null;P.sector=F.sid;enterSector(F.sid);running=false;P.docked='station';kitTick();dockAction('buy','kit_station:1');const inHold=P.cargo.kit_station||0;P.docked=null;kitTick();
      const up=staUp(P,R);return JSON.stringify({sid,msg,dep,kit,inHold,up,pst:!!(R&&R.pst),sk:P.cargo.kit_station||0})})()"""))
    check('a Depot Kit in a Heavy Hauler\'s hold builds a Depot (no Constructor)',r['dep'] and r['kit']==0,r)
    check('a Station Kit (220 t) bought at a freeport into the Heavy Hauler upgrades that Depot to a Station',r['inHold']==1 and r['pst'] and r['sk']==0,r)
    l=await ev(LED);check('ledger exact after building from kits',l=='exact',l)
    # a Lair from a Lair Kit: buy one at a freeport, fly to a rock, build
    r=json.loads(await ev("""(()=>{const P=S.player,R=mkStations().find(x=>x.owner==='neutral');exitSector();W=null;P.sector=R.sid;enterSector(R.sid);running=false;P.docked='station';kitTick();dockAction('buy','kit_lair:1');const got=P.cargo.kit_lair||0;P.docked=null;kitTick();
      const sid=Object.keys(DEF).find(s=>!S.stations[s]&&S.sectors[s].ast.some(a=>!a.comet&&!a.rift&&oreTotal(a)>=LAIR_B.rockMin)&&DEF[s].kind!=='hive');exitSector();W=null;P.sector=sid;enterSector(sid);running=false;
      const a=S.sectors[sid].ast.find(x=>!x.comet&&!x.rift&&oreTotal(x)>=LAIR_B.rockMin),p=W.player;p.x=a.x+astR(a)+200;p.y=a.y;p.z=a.z;const n0=(S.lairs||[]).length;const sp=lairSpot(P);const msg=lairBuildB();
      return JSON.stringify({got,spot:!sp.why,msg,lair:(S.lairs||[]).length===n0+1,kit:P.cargo.kit_lair||0})})()"""))
    check('a Lair Kit bought at a freeport builds a Lair by a rock',r['got']==1 and r['spot'] and r['lair'] and r['kit']==0,r)
    l=await ev(LED);check('ledger exact at the end',l=='exact',l)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
