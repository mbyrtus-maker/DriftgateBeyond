# usage: python3 tools/tests/mp_guest_trade.py $PWD/index.html  (needs Playwright with Chromium)
# A guest trades over the faked link (4 Nov 2026, the user's ask: market sales and delivery missions), each step checked on
# the host: buying and selling on a freeport's market (goods, credits, the market's stock and the treasury all move), a
# freeport contract delivered here from the Jobs board, and a freeport request elsewhere: bought here with the board's
# button, flown to the other freeport and delivered there. The ledger stays exact.
import json,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from mpkit import run,HP
CTX="runAs('clipid1',()=>dockCtx())"
async def body(K):
  G,Hh,check=K.G,K.Hh,K.check
  sec=await G("S.player.sector")
  # ================= market: buy
  pick=json.loads(await Hh("""(()=>{const c=%s,P=%s;const L=Object.keys(c.market).filter(k=>c.market[k]>=6&&ITEMS[k]&&!MUNITIONS.has(k)&&!FP_ONLY.has(k)&&mass(k)<=2&&mBuy(c,k)*3<P.credits).sort((a,b)=>c.market[b]-c.market[a]);
    const sl=Object.keys(c.market).filter(k=>ITEMS[k]&&!MUNITIONS.has(k)&&k!==L[0]&&k!=='matrix'&&mass(k)<=2&&mSell(c,k)>0).sort((a,b)=>mSell(c,b)-mSell(c,a));return JSON.stringify({buy:L[0],sell:sl[0],pr:mBuy(c,L[0]),sp:mSell(c,sl[0]),stock:c.market[L[0]]})})()"""%(CTX,HP)))
  print('market picks:',pick)
  k=pick['buy']
  snap="(()=>{const c=%s,P=%s;return JSON.stringify({hold:P.cargo[%s]||0,cr:P.credits,mk:c.market[%s]||0,tr:S.econ.treasury[c.wallet]})})()"
  a=json.loads(await Hh(snap%(CTX,HP,json.dumps(k),json.dumps(k))))
  m=await K.act('buy',k+':3')
  b=json.loads(await Hh(snap%(CTX,HP,json.dumps(k),json.dumps(k))))
  spent=a['cr']-b['cr']
  # (the freeport's market and treasury also move with its NPC traders meanwhile: check the guest's side exactly, the market's roughly)
  check('buy 3 %s (host)'%k,b['hold']-a['hold']==3 and a['mk']-b['mk']>=3 and spent>0 and ('for %d cr'%spent) in m,'%s -> %s · %s'%(a,b,m[:90]))
  gv=json.loads(await G("JSON.stringify({hold:S.player.cargo[%s]||0,cr:S.player.credits})"%json.dumps(k)))
  check('the guest sees its purchase',gv['hold']==b['hold'] and gv['cr']==b['cr'],gv)
  m=await K.act('sell',k+':3')
  c=json.loads(await Hh(snap%(CTX,HP,json.dumps(k),json.dumps(k))))
  check('sell them back (host)',c['hold']==a['hold'] and ('for %d cr'%(c['cr']-b['cr'])) in m and c['cr']>b['cr'] and c['cr']<=a['cr'],'%s · lost on the spread %s cr · %s'%(c,a['cr']-c['cr'],m[:80]))
  # ================= market: sell goods you brought (the host puts 5 in the guest's hold, as if mined)
  k2=pick['sell']
  await Hh("(()=>{devLedger(()=>inv.add(%s.cargo,%s,5));return 1})()"%(HP,json.dumps(k2)));await K.wait(1200)
  a=json.loads(await Hh(snap%(CTX,HP,json.dumps(k2),json.dumps(k2))))
  m=await K.act('sell',k2+':all')
  b=json.loads(await Hh(snap%(CTX,HP,json.dumps(k2),json.dumps(k2))))
  check('sell 5 %s (host)'%k2,b['hold']==a['hold']-5 and b['mk']>=a['mk']+1 and ('for %d cr'%(b['cr']-a['cr'])) in m,'%s -> %s · %s'%(a,b,m[:90]))
  check('the market screen renders on the guest',await G("(()=>{dockTab='market';mkFilter='comp';renderDock();return document.querySelectorAll('.mkt').length})()")>0)
  await K.ledger('after the market')
  # ================= a freeport contract here, delivered from the Jobs board
  kc=json.loads(await Hh("""(()=>{const P=%s;let k=S.contracts.find(x=>x.st===%s&&!x.blk&&x.fac==='neutral');const made=!k;
    if(!k){const item='plate',n=6;k={id:S.nextId++,fac:'neutral',st:%s,item,n,n0:n,reward:Math.ceil(baseValue(item)*n*1.6/10)*10,until:S.T+1800};S.contracts.push(k)}
    devLedger(()=>inv.add(P.cargo,k.item,k.n));return JSON.stringify({id:k.id,item:k.item,n:k.n,reward:k.reward,made})})()"""%(HP,json.dumps(sec),json.dumps(sec))))
  print('contract here:',kc)
  # (the whole state reaches guests every 5 s of game time: wait for the new contract to arrive)
  for i in range(40):
    if await G("(S.contracts||[]).some(x=>x.id===%d)&&(S.player.cargo[%s]||0)>=%d"%(kc['id'],json.dumps(kc['item']),kc['n'])):break
    await K.wait(1000)
  btn=await G("(()=>{dockTab='jobs';jobFilter='all';jobSel='k:%s';renderDock();const b=document.querySelector('#dBody [data-act=deliver][data-arg=\"%s\"]');return b?b.textContent.trim()+(b.disabled?' (disabled)':''):'none: '+[...document.querySelectorAll('#dBody [data-act]')].map(x=>x.dataset.act).join(',')})()"%(kc['id'],kc['id']))
  print('board button:',btn)
  c0=await Hh("%s.credits"%HP)
  await G("(()=>{const b=document.querySelector('#dBody [data-act=deliver][data-arg=\"%s\"]');if(b)b.click();else netSend({t:'act',act:'deliver',arg:'%s'});return 1})()"%(kc['id'],kc['id']));await K.wait(2500)
  st=json.loads(await Hh("(()=>{const k=S.contracts.find(x=>x.id===%d);return JSON.stringify({left:k?k.n:0,cr:%s.credits,hold:%s.cargo[%s]||0})})()"%(kc['id'],HP,HP,json.dumps(kc['item']))))
  check('contract delivered from the board',btn.startswith('Deliver') and st['left']==0 and st['cr']-c0>0,'%s · +%s cr · %s'%(st,st['cr']-c0,(await G("dockErr"))[:90]))
  await K.ledger('after the contract')
  # ================= a freeport request elsewhere: buy here, fly it there, deliver
  rq=json.loads(await Hh("""(()=>{const c=%s,P=%s;const fps=Object.values(S.stations).filter(R=>R.owner==='neutral'&&R.sid!==%s&&!R.dark).map(R=>R.sid).sort((a,b)=>HOP[%s][a]-HOP[%s][b]);
    let k=S.contracts.find(x=>x.st&&x.st!==%s&&!x.blk&&fpBuyable(c,P,x)&&fpBuyable(c,P,x).n>0&&HOP[%s][x.st]<=6);const made=!k;
    if(!k&&fps.length){const item=Object.keys(c.market).filter(i=>c.market[i]>=8&&ITEMS[i]&&!MUNITIONS.has(i)&&!FP_ONLY.has(i)&&mass(i)<=1).sort((a,b)=>c.market[b]-c.market[a])[0],n=4;k={id:S.nextId++,fac:'neutral',st:fps[0],item,n,n0:n,reward:Math.ceil(baseValue(item)*n*2/10)*10,until:S.T+3600};S.contracts.push(k)}
    return JSON.stringify(k?{id:k.id,item:k.item,n:k.n,st:k.st,h:HOP[%s][k.st],reward:k.reward,made,b:fpBuyable(c,P,k)}:null)})()"""%(CTX,HP,json.dumps(sec),json.dumps(sec),json.dumps(sec),json.dumps(sec),json.dumps(sec),json.dumps(sec))))
  print('request:',rq)
  if not rq:check('a freeport request to run',False);return
  for i in range(40):
    if await G("(S.contracts||[]).some(x=>x.id===%d)"%rq['id']):break
    await K.wait(1000)
  btn=await G("(()=>{dockTab='jobs';jobSel='r:%s';renderDock();const b=document.querySelector('#dBody [data-act=hbuy][data-arg=\"%s\"]');return b?b.textContent.trim():'none'})()"%(rq['id'],rq['id']))
  print('board button:',btn)
  await G("(()=>{const b=document.querySelector('#dBody [data-act=hbuy][data-arg=\"%s\"]');if(b)b.click();return 1})()"%rq['id']);await K.wait(2500)
  h=await Hh("%s.cargo[%s]||0"%(HP,json.dumps(rq['item'])))
  want=int(btn.split(' ')[1]) if btn.startswith('Buy') else rq['n']
  check('request goods bought from the board (host)',btn.startswith('Buy') and h>=want,'%s in the hold · %s'%(h,(await G("dockErr"))[:90]))
  # the board's Set course, then fly it there
  await G("(()=>{jobTrack('r:%s');return 1})()"%rq['id'])
  await K.undock()
  ok=await K.goto(rq['st'])
  check('flew to the freeport %s (%s jumps)'%(rq['st'],rq['h']),ok,await G("S.player.sector"))
  check('docked at %s (host)'%rq['st'],await K.dock()=='station')
  await G("(()=>{dockTab='jobs';jobSel='k:%s';renderDock();return 1})()"%rq['id']);await K.wait(500)
  btn=await G("(()=>{const b=document.querySelector('#dBody [data-act=deliver][data-arg=\"%s\"]');return b?b.textContent.trim():'none'})()"%rq['id'])
  c0=await Hh("%s.credits"%HP)
  m=await K.act('deliver',rq['id'],2500)
  st=json.loads(await Hh("(()=>{const k=S.contracts.find(x=>x.id===%d);return JSON.stringify({left:k?k.n:0,cr:%s.credits,docked:%s.docked,sec:%s.sector})})()"%(rq['id'],HP,HP,HP)))
  check('request delivered at %s'%rq['st'],st['left']==max(0,rq['n']-h) and st['cr']-c0>0,'board: %s · %s · +%s cr · %s'%(btn,st,st['cr']-c0,m[:90]))
run(body,gcls='courier')
