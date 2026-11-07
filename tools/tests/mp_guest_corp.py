# usage: python3 tools/tests/mp_guest_corp.py $PWD/index.html  (needs Playwright with Chromium)
# A guest and the corporations (7 Nov 2026, the corporations bug pass). The guest's copy of the makers follows the host's:
#   - the guest fits a maker's cargo module; the maker tweaks that line on the host (ceTweak): the guest's ITEMS traits and
#     trait text match the host's, and the guest's own ship stats (the ones its physics use) match the host's figure for it;
#   - the maker fails and a new company takes its works (ceFail, ceReborn): the guest's maker name, part names and traits
#     match the host's, and so do its ship stats again;
#   - a guest's system install from the Loadout (the real Install button) reaches the host and is done there.
# Ledger exact.
import json
from mpkit import run,HP
# the stats a pilot's own ship flies with, worked out on each page: the guest's W.player.st, the host's for the guest
KEYS=['cargo','maxSpd','hull','sCap','eCap']
GST="(()=>{const s=W.player.st;return JSON.stringify(%s.map(k=>Math.round((s[k]||0)*1000)/1000))})()"%json.dumps(KEYS)
HST="runAs('clipid1',()=>{const P=S.player,s=shipStats(P.faction,P.cls,P.tiers,P.tune);return JSON.stringify(%s.map(k=>Math.round((s[k]||0)*1000)/1000))})"%json.dumps(KEYS)
async def body(K):
  G,Hh,check=K.G,K.Hh,K.check
  if not await G("S.player.docked"):print('dock:',await K.dock())
  check('guest joined with the makers applied',await G("MP_CESIG!==null&&MP_CESIG===mpCeSig()"),await G("String(MP_CESIG).slice(0,60)"))
  # ---- a cargo line that can be tweaked, its module in the guest's hold (moved in on the host, ledger-checked)
  pick=json.loads(await Hh("""(()=>{for(const m in MAKERS){if(!ceAlive(m))continue;for(const id of ceTrLines(m)){if(ITEMS[id].part==='cargo'&&CE_KSTAT.cargo)return JSON.stringify({m,id})}}return 'null'})()"""))
  print('cargo line:',pick)
  if not pick:check('a cargo line to tweak',False);return
  m,pid=pick['m'],pick['id']
  slot=await Hh("(()=>{const U=fitOf(%s).u||[];const i=U.findIndex(k=>!k);return i>=0?i:U.length-1})()"%HP)
  await Hh("(()=>{devLedger(()=>inv.add(%s.cargo,%s,1));return 1})()"%(HP,json.dumps(pid)))
  msg=await K.act('fit','u:%d:%s'%(slot,pid),2500)
  fitted=await Hh("(fitOf(%s).ui||[])[%d]||''"%(HP,slot))
  check('guest fits the %s (host)'%pid,fitted==pid,'%s · %s'%(fitted,msg[:100]))
  await Hh("(()=>{MP.syT=0;sendPR(Object.values(MP.cl)[0],true,true);return 1})()");await K.wait(3000)
  s0g,s0h=await G(GST),await Hh(HST)
  check('stats agree before the tweak',s0g==s0h,'guest %s · host %s'%(s0g,s0h))
  # ---- a tweak on the host
  tw=None
  for i in range(4):
    r=await Hh("(()=>ceTweak(%s,%s,'test')?JSON.stringify({tr:ITEMS[%s].tr,txt:ITEMS[%s].trTxt}):'')()"%(json.dumps(m),json.dumps(pid),json.dumps(pid),json.dumps(pid)))
    if r:tw=json.loads(r);break
  print('host tweak:',tw)
  check('the host tweaks the line',bool(tw))
  await Hh("(()=>{MP.syT=0;return 1})()");await K.wait(3500)
  g=json.loads(await G("JSON.stringify({tr:ITEMS[%s].tr,txt:ITEMS[%s].trTxt})"%(json.dumps(pid),json.dumps(pid))))
  check('guest ITEMS traits follow the tweak',tw and g['tr']==tw['tr'],'host %s · guest %s'%(tw and tw['tr'],g['tr']))
  check('guest trait text follows the tweak',tw and g['txt']==tw['txt'],g['txt'][:100])
  g2=await G("JSON.stringify(ITEMS[%s].tr)"%json.dumps(pid+'_g2'))
  check('the guest\'s grade 2 of the line follows too',tw and json.loads(g2)==tw['tr'],g2)
  s1g,s1h=await G(GST),await Hh(HST)
  check('guest ship stats match the host after the tweak',s1g==s1h,'guest %s · host %s'%(s1g,s1h))
  check('the tweak changed the hold',s1h!=s0h,'%s -> %s'%(s0h,s1h))
  hent=await Hh("(()=>{const e=MP.rp.clipid1;return e?JSON.stringify(%s.map(k=>Math.round((e.st[k]||0)*1000)/1000)):'none'})()"%json.dumps(KEYS))
  if hent!='none':check('the host flies the guest\'s ship with the new stats',hent==s1h,'%s · %s'%(hent,s1h))
  # ---- the maker fails; a new company takes its works
  nb=json.loads(await Hh("""(()=>{const m=%s,old=MAKERS[m].name;ceFail(m);const home=ceHomeWallet(m);if((S.econ.treasury[home]||0)<CE.start+10)devLedger(()=>{S.econ.treasury[home]=(S.econ.treasury[home]||0)+CE.start+10});
     ceReborn(m);const c=ceOf(m);return JSON.stringify({old,name:MAKERS[m].name,short:MAKERS[m].short,dead:c.dead,tr:ITEMS[%s].tr,iname:ITEMS[%s].name,g2:ITEMS[%s].name,txt:ITEMS[%s].trTxt})})()"""%(json.dumps(m),json.dumps(pid),json.dumps(pid),json.dumps(pid+'_g2'),json.dumps(pid))))
  print('new company:',nb)
  check('the host has a new company',not nb['dead'] and nb['name']!=nb['old'],nb)
  await Hh("(()=>{MP.syT=0;return 1})()");await K.wait(3500)
  g=json.loads(await G("JSON.stringify({name:MAKERS[%s].name,short:MAKERS[%s].short,tr:ITEMS[%s].tr,iname:ITEMS[%s].name,g2:ITEMS[%s].name,txt:ITEMS[%s].trTxt})"%(json.dumps(m),json.dumps(m),json.dumps(pid),json.dumps(pid),json.dumps(pid+'_g2'),json.dumps(pid))))
  check('guest maker name follows the new company',g['name']==nb['name'] and g['short']==nb['short'],'%s / %s'%(g['name'],g['short']))
  check('guest part names follow',g['iname']==nb['iname'] and g['g2']==nb['g2'],'%s · %s'%(g['iname'],g['g2']))
  check('guest traits follow the new company',g['tr']==nb['tr'] and g['txt']==nb['txt'],'host %s · guest %s'%(nb['tr'],g['tr']))
  s2g,s2h=await G(GST),await Hh(HST)
  check('guest ship stats match the host after the new company',s2g==s2h,'guest %s · host %s'%(s2g,s2h))
  # a quiet sync doesn't apply the makers again
  await G("(()=>{window.__ca=0;const o=ceApply;window.__cao=o;ceApply=function(){__ca++;return o.apply(this,arguments)};return 1})()")
  await Hh("(()=>{MP.syT=0;return 1})()");await K.wait(3000)
  n=await G("(()=>{const n=__ca;ceApply=__cao;return n})()")
  check('a sync with no change to the makers leaves them be',n==0,'%s re-applies'%n)
  # ---- a guest's system install from the Loadout reaches the host
  sid='sy_ad_shield'
  await Hh("(()=>{devLedger(()=>inv.add(%s.vault,%s,1));sendPR(Object.values(MP.cl)[0],true,true);return 1})()"%(HP,json.dumps(sid)));await K.wait(2000)
  b0=json.loads(await Hh("JSON.stringify({m:(%s.sysm||{}).shield||null,v:%s.vault[%s]||0})"%(HP,HP,json.dumps(sid))))
  clk=await G("(()=>{dockTab='upg';ldSel='sys:shield';renderDock();const b=document.querySelector('#dBody [data-act=sysfit][data-arg=\"shield:%s\"]');if(!b)return 'no button';b.click();return 'clicked: '+dockErr})()"%sid)
  print('guest Install:',clk)
  await K.wait(3000)
  b1=json.loads(await Hh("JSON.stringify({m:(%s.sysm||{}).shield||null,v:%s.vault[%s]||0})"%(HP,HP,json.dumps(sid))))
  check('guest Install reaches the host',b1['m']=='ad' and b1['v']==b0['v']-1,'before %s after %s'%(b0,b1))
  gm=await G("JSON.stringify({m:(S.player.sysm||{}).shield||null,err:dockErr})")
  check('the guest sees it installed',json.loads(gm)['m']=='ad',gm[:160])
  await K.ledger('end')
run(body)
