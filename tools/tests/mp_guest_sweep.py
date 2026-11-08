# usage: python3 tools/tests/mp_guest_sweep.py $PWD/index.html  (needs Playwright with Chromium)
# The bug sweep of 8 Nov 2026, from a guest's side: the week's new systems as a guest pilot meets them.
#   - every dock tab, every Loadout system panel and every Company tab and view (the Corporations view for every maker) render
#     on the guest with no errors;
#   - upgrades in place are refused for a guest too (the host's answer comes back), and so is fabricating a maker's part;
#   - the guest buys a maker's part at the Market: the host takes the guest's credits and the maker gets its share;
#   - the guest fits a grade 2 part (it goes in at grade 2 on the host) and takes it out again (back as the graded part);
#   - the guest installs a system part (done on the host; the old one goes to the guest's hangar);
#   - the galaxy map's panels on the guest (the Bloom's gauge, Hollow Verge with no Relay);
# Ledger exact throughout, no page errors on either page.
import json
from mpkit import run,HP
async def body(K):
  G,Hh,check=K.G,K.Hh,K.check
  if not await G("S.player.docked"):print('dock:',await K.dock())
  check('guest docked (host)',bool(await Hh(HP+".docked")))
  # ---- the screens
  ui=await G("""(()=>{const out=[];try{openDock();for(const g of dockG)for(const t of g[2]){dockTab=t[0];try{renderDock()}catch(e){out.push('dock '+t[0]+': '+e.message)}}
    dockTab='upg';for(const sl in SLOT){ldSel='sys:'+sl;try{renderDock()}catch(e){out.push('ldsys '+sl+': '+e.message)}}
    $('company').hidden=false;for(const t of ['holdings','economy','crews','bm','allegiance','jobs']){coTab=t;try{renderCompany()}catch(e){out.push('co '+t+': '+e.message)}}
    coTab='economy';coV.economy='corps';for(const m in MAKERS){coPk.economy='corp:'+m;try{renderCompany()}catch(e){out.push('corp '+m+': '+e.message)}}
    const h=ceHtml(S.player);if(!/Corporations/.test(h))out.push('no Corporations view');$('company').hidden=true;dockTab='home';renderDock()}catch(e){out.push(e.message)}return out.join(' | ')||'ok'})()""")
  check('every dock tab, Loadout system panel and Company view renders on the guest',ui=='ok',ui)
  # ---- upgrades in place and fabricating a maker's part are refused
  r=await K.act('upg','engine',2500)
  check('an upgrade in place is refused for the guest',('gone' in r),r[:120])
  r=await K.act('make','sy_engine_g3:1',2500)
  check('fabricating a maker\'s part is refused for the guest',('Only its maker' in r),r[:120])
  # ---- a Market buy of a maker's part: the maker gets its share
  pick=json.loads(await Hh("""(()=>{const P=%s,R=S.stations[P.sector];if(!R)return'null';const st=mkStock(R);for(const id in st)if(st[id]>0&&ITEMS[id]&&ITEMS[id].maker&&ITEMS[id].part&&ceAlive(ITEMS[id].maker))return JSON.stringify({id,m:ITEMS[id].maker});return'null'})()"""%HP))
  if pick:
    t0=await Hh("(()=>Math.round(ceT(%s)))()"%json.dumps(pick['m']));c0=await Hh(HP+".credits")
    if c0<5000:await Hh("(()=>{const n=5000;S.econ.treasury.neutral-=n;%s.credits+=n;return 1})()"%HP)
    c0=await Hh(HP+".credits")
    r=await K.act('buy',pick['id']+':1',3000)
    t1=await Hh("(()=>Math.round(ceT(%s)))()"%json.dumps(pick['m']));c1=await Hh(HP+".credits")
    paid=c0-c1;got=t1-t0
    check('the guest buys %s and its maker gets about 85%%'%pick['id'],paid>0 and abs(got-paid*.85)<=2,'paid %s · maker +%s · %s'%(paid,got,r[:80]))
  else:check('a maker\'s part on sale where the guest docked',False,'none')
  await K.ledger('after the buy')
  # ---- a grade 2 part fitted and taken out again
  await Hh("(()=>{devLedger(()=>inv.add(%s.cargo,'mp_mg_gun_g2',1));window.__gc=gradeCap;gradeCap=()=>5;return 1})()"%HP)
  r=await K.act('fit','w:0:mp_mg_gun_g2',3000)
  f=json.loads(await Hh("(()=>{const F=fitOf(%s);return JSON.stringify({w:F.w[0],id:F.wi[0],g:F.g[0]})})()"%HP))
  check('the guest fits a grade 2 gun (host: at grade 2)',f.get('id')=='mp_mg_gun' and f.get('g')==2,'%s · %s'%(f,r[:80]))
  r=await K.act('fit','w:0:',3000)
  back=await Hh("countIn('mp_mg_gun_g2',[%s.cargo,%s.vault,(S.stations[%s.sector]&&runAs('clipid1',()=>dockCtx().storage))||{}])"%(HP,HP,HP))
  check('taken out, it comes back as the grade 2 gun',back>=1,'%s · %s'%(back,r[:80]))
  await K.ledger('after the fit')
  # ---- a system installed
  await Hh("(()=>{devLedger(()=>inv.add(%s.cargo,'sy_ewd_engine_g2',1));return 1})()"%HP)
  r=await K.act('sysfit','engine:sy_ewd_engine_g2',3000)
  s=json.loads(await Hh("(()=>JSON.stringify({t:%s.tiers.engine,m:(%s.sysm||{}).engine}))()"%(HP,HP)))
  await Hh("(()=>{gradeCap=window.__gc;return 1})()")
  check('the guest installs a grade 2 drive (host)',s.get('t')==2 and s.get('m')=='ewd','%s · %s'%(s,r[:100]))
  await K.wait(3000)
  gt=await G("S.player.tiers.engine")
  check('the guest\'s copy shows the new drive',gt==2,gt)
  await K.ledger('after the install')
  # ---- the map's panels on the guest
  mp=await G("""(()=>{const out=[];for(const d of SECTOR_DEFS){try{mapSectorNow(d.id)}catch(e){out.push(d.id+': '+e.message)}}const h=mapSectorNow('bl');if(!/Bloom stirs/.test(h))out.push('no Bloom gauge');if(S.outposts.hollow)out.push('the Relay is still there');return out.join(' | ')||'ok'})()""")
  check('the map panels on the guest (the Bloom gauge, no Relay)',mp=='ok',mp)
run(body)
