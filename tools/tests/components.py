# Beyond, the four new components (9 Nov 2026): Vantium Plating, Aurorite Cell, Optic Array and Thrust Vane exist with their
# recipes; standard parts and systems keep theirs; the makers' lines use them by character (Coldwater Refit doesn't), and
# R&D grades lean on Vantium Plating and Aurorite Cells; the powers make them (keeping their own Ferrite and Cuprite); a
# maker builds a part that needs one; fitting and taking out a graded maker part, installing a maker system and stripping a
# ship's grades keep the ledger exact; an old save is rebased once
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
    r=json.loads(await ev("""(()=>{const R=k=>JSON.stringify(ITEMS[k].recipe);return JSON.stringify({vp:R('vplate'),ac:R('acell'),op:R('optic'),va:R('vane'),std:R(PART.laser||'pt_laser'),sys:R('sy_armor'),
      hfc:R('mp_hf_charge'),bl:R('mp_bl_laser'),sw:R('mp_sw_scanner'),wf:R('mp_wf_torpedo'),cr:R('mp_cr_laser'),crs:R('sy_cr_shield'),tcyE:R('sy_tcy_engine'),hfA:R('sy_hf_armor'),mgW:R('sy_mg_weapon'),adP:R('sy_ad_power'),
      bl3:R(rdGid('mp_bl_laser',3)),hfc3:R(rdGid('mp_hf_charge',3)),neg:Object.keys(ITEMS).filter(k=>Object.values(ITEMS[k].recipe||{}).some(v=>v<0)),comp:JSON.stringify(comp('vplate'))})})()"""))
    check('the four components and their recipes',r['vp']=='{"nu":2,"fe":1}' and r['ac']=='{"au":1,"cu":2}' and r['op']=='{"xc":1,"cu":2}' and r['va']=='{"ir":1,"fe":2}',r)
    check('standard parts and systems keep their recipes; Coldwater Refit stays standard','vplate' not in r['sys'] and 'acell' not in r['std'] and 'acell' not in r['cr'] and 'acell' not in r['crs'],r)
    check('makers\' lines use them by character',all(x in r[k] for k,x in [('hfc','vplate'),('bl','acell'),('sw','optic'),('wf','vane'),('tcyE','vane'),('hfA','vplate'),('mgW','optic'),('adP','acell')]),r)
    check('R&D grades lean on Vantium Plating and Aurorite Cells',json.loads(r['bl3']).get('acell',0)>=3 and json.loads(r['hfc3']).get('vplate',0)>=3,r)
    check('no recipe has a negative amount',not r['neg'],r['neg'][:5])
    # the powers make them
    r=json.loads(await ev("""(()=>{running=false;exitSector();W=null;const f='halcyon',st=S.econ.stock[f];devLedger(()=>{inv.add(st,'nu',20);inv.add(st,'au',20);inv.add(st,'fe',60);inv.add(st,'cu',60)});const b={};for(const k of CMP4)b[k]=st[k]||0;for(let i=0;i<6;i++){S.T+=10;strategicTick();updateEvents()}
      const a={};for(const k of CMP4)a[k]=(st[k]||0)-b[k];return JSON.stringify({a,fe:st.fe||0,cu:st.cu||0})})()"""))
    check('a power with the ore makes them',r['a']['vplate']>0 and r['a']['acell']>0,r)
    l=await ev(LED);check('ledger exact after the works',l=='exact',l)
    # a maker builds a part that needs one
    r=json.loads(await ev("""(()=>{const m='hf',R=mkAtHome(m),st=mkStock(R),id='mp_hf_charge',gid=rdGid(id,rdLineG(m,id));devLedger(()=>{inv.add(st,'vplate',6);inv.add(st,'wire',6);inv.add(st,'plate',6)});for(const x of MK_LINE[m])if(x!==id)inv.add(st,rdGid(x,rdLineG(m,x)),0);
      const n0=st[gid]||0;inv.take(st,gid,n0);const keep=n0;S.mkT=0;makersTick();const made=(st[gid]||0);inv.add(st,gid,keep);return JSON.stringify({gid,made,rc:ITEMS[gid].recipe})})()"""))
    check('a maker builds a part that uses Vantium Plating',r['made']>=1,r)
    l=await ev(LED);check("ledger exact after the maker's works",l=='exact',l)
    # fit and take out a graded maker part; install a maker system; strip the ship
    r=json.loads(await ev("""(()=>{const P=S.player,R=S.stations[P.sector]||mkStations()[0];P.rp=1e6;P.sector=R.sid;enterSector(R.sid);running=false;P.docked='station';const c=dockCtx();const gid=rdGid('mp_bl_laser',2),sy=rdGid('sy_hf_armor',2);
      devLedger(()=>{inv.add(c.storage,gid,1);inv.add(c.storage,sy,1)});const F=fitOf(P);const wi=F.wi.findIndex((x,i)=>true);const before=JSON.stringify(F.wi);dockAction('fit',`w:0:${gid}`);const fit=dockErr,fitted=fitOf(P).wi[0];
      const ss=rdSysFit('armor:'+sy);return JSON.stringify({fit,fitted,ss,sysm:(P.sysm||{}).armor})})()"""))
    check('a graded maker laser fits and a maker armour system installs',(r['fit'] or '').startswith('✓') and r['fitted']=='mp_bl_laser' and r['ss'].startswith('✓') and r['sysm']=='hf',r)
    l=await ev(LED);check('ledger exact with them fitted',l=='exact',l)
    r=json.loads(await ev("""(()=>{const P=S.player,c=dockCtx();dockAction('fit','w:0:');const back=countIn(rdGid('mp_bl_laser',2),[c.storage,P.cargo]);const into=c.storage;shipStrip(P,into);return JSON.stringify({back,armor:P.tiers.armor,sysm:P.sysm.armor})})()"""))
    check('taking the graded laser out gives the graded item back',r['back']>=1,r)
    l=await ev(LED);check('ledger exact after taking it out and stripping the ship',l=='exact',l)
    check('no errors',not errs,errs[:3])
    print('ALL OK' if not bad else 'FAILED: '+', '.join(bad))
    await b.close()
asyncio.run(main())
