# Beyond, the corporate economy stage 1 (7 Nov 2026): makers have treasuries (capitalised by their homes); a sale pays the
# maker less the station's 15% dues; the works pay for components; running costs; the powers refit from the markets; tweaks
# change a line for every unit; a maker that can't pay fails and a new company takes its works; the Corporations view;
# names and traits survive a save; the ledger stays exact (credits too) throughout. Logos (7 Nov 2026): every maker starts with
# its own mark and accent; a reborn maker keeps its accent and takes a spare mark no other maker shows; the view draws it; a
# save keeps it, and a galaxy saved before logos gets the original marks
import asyncio,json
from playwright.async_api import async_playwright
import os
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
LED="""(()=>{const l=ledger();let b=[];for(const e of RAWS)if(Math.abs(l.tot[e]-S.ledger0.tot[e])>1e-6)b.push(e+':'+(l.tot[e]-S.ledger0.tot[e]).toFixed(2));if(Math.abs(l.credits-S.ledger0.credits)>1e-6)b.push('cr:'+(l.credits-S.ledger0.credits));return b.length?'DRIFT '+b.join(' '):'exact'})()"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1400,'height':860});errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console: '+m.text[:300]) if m.type=='error' and 'Failed to load resource' not in m.text else None)
    await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
    await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    print('start',await ev("JSON.stringify({makers:Object.keys(S.corp).length,treasury:ceT('mg'),ceo:ceOf('mg').ceo})"),await ev(LED))
    print('logos at the start',await ev("(()=>{const ms=Object.keys(MAKERS),bad=ms.filter(m=>ceOf(m).logo!==m||mkLogoOf(m)!==m||!MK_LOGO[m]||!/^#[0-9a-f]{6}$/.test(mkAcc(m)));return bad.length?'BAD '+bad.join(','):'ok: '+ms.length+' makers, own marks and accents'})()"))
    # a pilot buys a Marchgun gun at Marchgun's home: the maker gets 85%
    print('a sale',await ev("""(()=>{const sid=mkHomeSid('mg'),R=S.stations[sid],P=S.player;undock();exitSector();P.sector=sid;enterSector(sid);P.docked='station';S.ledger0.credits+=50000-P.credits;P.credits=50000;
      const st=mkStock(R),id='mp_mg_gun';st[id]=(st[id]||0);if(!st[id]){st.plate=(st.plate||0);}const t0=ceT('mg');if(!st[id])return 'none in stock';const pr=Math.ceil(stPrice(R,id)),c0=P.credits;dockAction('buy',id+':1');const paid=c0-P.credits;
      return JSON.stringify({paid,maker:ceT('mg')-t0,share:+((ceT('mg')-t0)/paid).toFixed(2),floor:pr>=ceComp(sid,id)*CE.floor/(1-CE.dues)-1})})()"""))
    print('ledger',await ev(LED))
    # an hour on: works, running costs, refits, reviews
    print('an hour on',await ev("""(()=>{running=false;exitSector();W=null;for(let i=0;i<360;i++){S.T+=10;strategicTick();updateEvents()}let fit=0;for(const f in S.corpFit)fit+=Object.values(S.corpFit[f]).reduce((a,b)=>a+b,0);
      return JSON.stringify({fitted:fit,treasuries:Object.keys(MAKERS).map(m=>Math.round(ceT(m))).join(','),sales:Object.keys(MAKERS).reduce((a,m)=>a+ceOf(m).sales.length,0)})})()"""),await ev(LED))
    print('a tweak',await ev("""(()=>{const id='mp_bl_laser',t0=JSON.stringify(ITEMS[id].tr);ceOf('bl').ln={};const ok=ceTweak('bl',id,'test');return JSON.stringify({ok,before:t0,after:ITEMS[id].tr,txt:ITEMS[id].trTxt,parts:MAKERS.bl.parts.laser})})()"""))
    print('fail and reborn',await ev("""(()=>{const m='hf',old=MAKERS[m].name;transfer(ceW(m),'varkesh',ceT(m));ceMinute();const dead=ceOf(m).dead;ceOf(m).reborn=S.T;ceMinute();return JSON.stringify({old,dead:!!dead,now:MAKERS[m].name,alive:ceAlive(m),treasury:ceT(m),item:ITEMS['mp_hf_charge'].name})})()"""),await ev(LED))
    print('new mark',await ev("(()=>{const m='hf',k=ceOf(m).logo,others=Object.keys(MAKERS).filter(x=>x!==m).map(mkLogoOf);return JSON.stringify({logo:k,spare:MK_SPARE.includes(k),unique:!others.includes(k),acc:mkAcc(m),accSame:mkAcc(m)==='#e8583a',news:JSON.stringify(S.news||[]).includes('new mark')||FEED.some(f=>/new mark/.test(f.msg))})})()"))
    print('view logo',await ev("(()=>{coV.economy='corps';coPk.economy='corp:hf';const h=ecHtml(S.player),d=MK_LOGO[ceOf('hf').logo].d;return JSON.stringify({svg:(h.match(/class=.mklogo/g)||[]).length,hfLogo:h.includes(d),acc:h.includes('#e8583a')})})()"))
    print('second rebirth',await ev("(()=>{const m='hf',k0=ceOf(m).logo;transfer(ceW(m),'varkesh',ceT(m));ceMinute();ceOf(m).reborn=S.T;ceMinute();const k=ceOf(m).logo;return JSON.stringify({k0,k,fresh:k!==k0&&MK_SPARE.includes(k),used:S.corpLogos})})()"),await ev(LED))
    print('the view',await ev("""(()=>{coV.economy='corps';coPk.economy='corp:hf';const h=ecHtml(S.player);return /Corporations/.test(h)&&h.includes(MAKERS.hf.name)?'shown':'missing'})()"""))
    print('saved and loaded',await ev("""(()=>{const nm=MAKERS.hf.name,tr=JSON.stringify(ITEMS.mp_bl_laser.tr);const s=JSON.parse(JSON.stringify(S));newGame('halcyon',launchCls(),'Tester','mw');startWith(S);const fresh=MAKERS.hf.name;startWith(s);
      return JSON.stringify({fresh,back:MAKERS.hf.name===nm,trBack:JSON.stringify(ITEMS.mp_bl_laser.tr)===tr})})()"""))
    print('logo saved',await ev("(()=>{const k=ceOf('hf').logo;const s=JSON.parse(JSON.stringify(S));startWith(s);return JSON.stringify({k,back:ceOf('hf').logo===k&&mkLogoOf('hf')===k})})()"))
    print('old save',await ev("(()=>{const s=JSON.parse(JSON.stringify(S));for(const m in s.corp)delete s.corp[m].logo;startWith(s);const bad=Object.keys(MAKERS).filter(m=>ceOf(m).logo!==m);return bad.length?'BAD '+bad:'original marks'})()"))
    print('ledger',await ev(LED))
    print('errors',errs[:5] or 'none')
    await b.close()
asyncio.run(main())
