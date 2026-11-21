# game controller support: a scripted fake pad (navigator.getGamepads replaced) drives the real game.
# Stick rest points (zeros first, a resting offset, a drifting stick, a trigger parked at -1), steering direction and invert, the mapping table
# (every layer, every key action covered, rebinding honoured), screens (pointer, click, back, tabs, scroll), the mouse retaking steering only
# after it moves, prompts naming pad buttons or keys by what was used last, disconnect, audio wake, the on-screen keyboard; two screenshots.
import asyncio,json,os,tempfile
from playwright.async_api import async_playwright
GAME='file://'+os.path.abspath(os.environ.get('DG_GAME',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','index.html')))
D=os.path.join(os.environ.get('DG_OUT',tempfile.gettempdir()),'')
fails=[]
def check(name,ok,info=''):
  print(('ok   ' if ok else 'FAIL ')+name+(' '+str(info) if info!='' else ''))
  if not ok:fails.append(name)
FAKE="""(()=>{const mk=(id,mapping,axes)=>({id,index:0,connected:true,mapping,axes:axes.slice(),buttons:Array.from({length:17},()=>({pressed:false,value:0}))});
window.__fp=mk('Xbox 360 Controller (STANDARD GAMEPAD Vendor: 045e Product: 028e)','standard',[0,0,0,0]);window.__fon=false;
window.__mk=mk;navigator.getGamepads=()=>window.__fon?[window.__fp]:[];
})()"""
SPY="""window.__ks=[];window.__spy=false;
addEventListener('keydown',e=>{if(!e.isTrusted){__ks.push(e.code+(e.shiftKey?'+S':''));if(__spy)e.stopImmediatePropagation()}},true);
addEventListener('keyup',e=>{if(!e.isTrusted&&__spy)e.stopImmediatePropagation()},true);"""
errs=[]
async def boot(b,w=1400,h=860,dsf=1):
  ctx=await b.new_context(viewport={'width':w,'height':h},device_scale_factor=dsf);await ctx.add_init_script(SPY);pg=await ctx.new_page()
  pg.on('pageerror',lambda e:errs.append(str(e)))
  await pg.goto(GAME+'?name=Tester',wait_until='domcontentloaded');await pg.evaluate('localStorage.clear()');await pg.reload(wait_until='domcontentloaded');await pg.wait_for_function('window.__dg&&__dg.ev("MDL.ready")',timeout=60000)
  await pg.evaluate("document.getElementById('mpName').value='Tester'");await pg.evaluate("document.getElementById('bLaunch').click()");await pg.wait_for_timeout(1500)
  await pg.evaluate(FAKE)
  return pg
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg=await boot(b)
    ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    W=lambda ms:pg.wait_for_timeout(ms)
    F=lambda n=3:pg.evaluate('n=>new Promise(r=>{let k=n;const f=()=>--k<=0?r():requestAnimationFrame(f);requestAnimationFrame(f)})',n)
    async def setb(i,down,val=None):
      await pg.evaluate("([i,d,v])=>{const b=__fp.buttons[i];b.pressed=d;b.value=v==null?(d?1:0):v}",[i,down,val])
    async def tap(i,hold=500):
      await setb(i,True);await F(4);await W(60);await F(3);await setb(i,False);await F(4)
    async def axes(a):await pg.evaluate("a=>{__fp.axes=a}",a)
    # ---- no pad: nothing changes
    check('docked at start',await ev("!!S.player.docked"))
    check('no pad: kb names keys',await ev("kb('fire')+'|'+kb('act')")=='Space|E')
    check('no pad: not live',await ev("PAD.live===false&&padLead()===false"))
    await W(600)
    check('no pad: still not live',await ev("PAD.live===false"))
    # ---- every key action is on the pad (nothing keyboard-only)
    r=await ev("""(()=>{const ids=new Set();for(const r of PAD_MAP)for(const a of [r[1],r[2],r[3]])if(a)ids.add(a);const miss=[];
      for(const[,L]of KEY_ACTS)for(const[id]of L){if(['rollL','rollR','map'].includes(id))continue;if(id==='kin'||id==='las'){if(!ids.has('gunsel'))miss.push(id);continue}if(!ids.has(id))miss.push(id)}
      for(const a of ids)if(!['boost','gunsel','cycleBack','subCycle','ordNext'].includes(a)&&!KEY_DEF[a])miss.push('?'+a);return JSON.stringify(miss)})()""")
    check('every key action has a pad button',r=='[]',r)
    # ---- connect
    await pg.evaluate("__fon=true");await W(500)
    check('pad found',await ev("PAD.live&&PAD.std&&!PAD.ps"))
    check('connected but unused: keys still named',await ev("kb('fire')")=='Space')
    # screens first: docked, the dock sheet is open; the pad takes the pointer once it is used
    check('dock open',await ev("!$('dock').hidden"))
    await tap(15)
    check('pad used: kb names pad buttons',await ev("kb('act')+'|'+kb('fire')+'|'+kb('thrust')")=='A|RT|LT')
    check('pointer shown on a screen',await ev("PAD.ptrOn&&$('padPtr').classList.contains('on')"))
    check('pointer snapped onto the screen',await ev("PAD.placed&&PAD.px>0&&PAD.py>0&&!!document.elementFromPoint(PAD.px,PAD.py)"))
    # move with the left stick
    x0=await ev("PAD.px");await axes([1,0,0,0]);await W(120);await axes([1,0,0,0]);await W(500);await axes([0,0,0,0]);await W(200)
    x1=await ev("PAD.px");check('left stick moves the pointer right',x1>x0+40,[x0,x1])
    # click a dock tab with A: put the pointer on Trade
    await ev("(()=>{const b=[...document.querySelectorAll('#dTabs .mtab')].find(x=>/Trade/.test(x.textContent));if(!b)return;const r=b.getBoundingClientRect();PAD.px=r.left+r.width/2;PAD.py=r.top+r.height/2})()")
    await tap(0)
    check('A clicks a dock tab',await ev("dockTopOf(dockTab)")=='trade',await ev("dockTab"))
    await tap(5);check('RB steps to the next top tab',await ev("dockTopOf(dockTab)")=='jobs',await ev("dockTab"))
    await tap(4);check('LB steps back',await ev("dockTopOf(dockTab)")=='trade',await ev("dockTab"))
    s0=await ev("dockTab");await tap(7);s1=await ev("dockTab");check('RT steps the sub-tab',s0!=s1,[s0,s1])
    # D-pad snap
    p0=await ev("[PAD.px,PAD.py]");await tap(13);p1=await ev("[PAD.px,PAD.py]");check('D-pad down jumps the pointer',p1!=p0,[p0,p1])
    # the manual: Start opens it; right stick scrolls; A on Close; B closes
    await tap(9);check('Start opens the manual',await ev("!$('help').hidden"))
    await ev("PAD.dirty=true");await W(300)
    check('manual lists the controller',await ev("$('padList').innerText.includes('Right stick')&&$('padList').innerText.includes('Afterburner')"))
    await ev("(()=>{const r=document.querySelector('#help .c-body').getBoundingClientRect();PAD.px=r.left+r.width/2;PAD.py=r.top+r.height/2})()")
    await axes([0,0,0,1]);await W(150);await axes([0,0,0,1]);await W(700);await axes([0,0,0,0]);await W(150)
    st=await ev("(()=>{const e=document.querySelector('#help .c-body');let m=0;for(const x of [e,...e.querySelectorAll('*')])m=Math.max(m,x.scrollTop);return m})()")
    check('right stick scrolls the manual',st>20,st)
    await tap(1);check('B closes the manual',await ev("$('help').hidden"))
    await tap(9);await tap(9);check('Start twice opens then closes',await ev("$('help').hidden"),await ev("JSON.stringify({ui:PAD.ui,open:PAD.uiEls.map(e=>e&&!e.hidden?e.id:0).filter(x=>x),sw:Array.from(PAD.swallow).join('')})"))
    await tap(9);await ev("(()=>{const b=document.querySelector('[data-close=help]');const r=b.getBoundingClientRect();PAD.px=r.left+r.width/2;PAD.py=r.top+r.height/2})()");await tap(0)
    check('A on Close closes it',await ev("$('help').hidden"))
    # B on the dock sheet is what Esc does: undock
    await tap(1);await W(300)
    check('B on the dock undocks (what Esc does)',await ev("!S.player.docked&&$('dock').hidden"))
    check('pointer gone back in flight',await ev("!PAD.ptrOn&&!PAD.ui"))
    # ---- flight: first frames zero, then a resting offset: no turn
    await pg.evaluate("__fon=false");await W(300)
    await pg.evaluate("__fp=__mk('Pad A (STANDARD GAMEPAD)','standard',[0,0,0,0]);__fon=true");await W(700)
    await axes([0.18,-0.15,0.1,0.12]);await W(1500)
    r=await ev("JSON.stringify({y:PADIN.yaw,p:PADIN.pitch,r:PADIN.roll,wy:Math.abs(W.player.wy||0),wx:Math.abs(W.player.wx||0)})");j=json.loads(r)
    check('zeros then a resting offset does not turn the ship',j['y']==0 and j['p']==0 and j['r']==0 and j['wy']<.01 and j['wx']<.01,r)
    # a trigger axis parked at -1 on a non-standard pad is ignored
    await pg.evaluate("__fp=__mk('Generic Pad','',[0,0,-1,0,0,-1]);__fon=true");await W(500);await axes([0,0,-1,0,0,-1]);await W(1500)
    r=await ev("JSON.stringify({rx:PAD.rx,ry:PAD.ry,roll:PADIN.roll,trig:PAD.trig.slice(0,6),std:PAD.std})")
    j=json.loads(r);check('non-standard layout: axis parked at -1 ignored',j['rx']==0 and j['roll']==0 and j['std']==False,r)
    # back to a standard pad; a deflected stick turns the right way
    await pg.evaluate("__fp=__mk('Pad B (STANDARD GAMEPAD)','standard',[0,0,0,0]);__fon=true");await W(600)
    await axes([0.02,0.01,0,0]);await W(900)
    await axes([1,0,0,0]);await W(700)
    r=await ev("JSON.stringify({yaw:PADIN.yaw,wy:W.player.wy,si:steerInput().yaw})");j=json.loads(r)
    check('stick right turns right (yaw like ArrowRight, negative)',j['yaw']<-.9 and j['wy']<-.05 and j['si']<-.9,r)
    await axes([0,0,0,0]);await W(900)
    await axes([0,-1,0,0]);await W(500)
    r=await ev("JSON.stringify({p:PADIN.pitch,si:steerInput().pitch,wx:W.player.wx})");j=json.loads(r)
    arrow=await ev("(()=>{keys.ArrowUp=true;const v=steerInput().pitch;keys.ArrowUp=false;return v})()")
    check('stick up pitches like ArrowUp',j['p']<-.9 and j['si']<-.9 and arrow<0,r)
    await ev("PAD.cfg.inv=true");await W(150)
    check('invert pitch flips it',await ev("PADIN.pitch")>.9)
    await ev("PAD.cfg.inv=false");await axes([0,0,0,0]);await W(300)
    # right stick rolls
    await axes([0,0,1,0]);await W(500);r=await ev("JSON.stringify({roll:PADIN.roll,wz:W.player.wz})");j=json.loads(r)
    check('right stick rolls',j['roll']>.9 and abs(j['wz'])>.05,r)
    await axes([0,0,0,1]);await W(400);c0=await ev("cam.dist");await W(400);c1=await ev("cam.dist");check('right stick down zooms the camera out',c1>c0,[c0,c1])
    await axes([0,0,0,0]);await W(300)
    # a drifting stick is re-centred: deflect, then let it rest off centre
    await axes([0.9,0,0,0]);await W(400);await axes([0.28,0,0,0]);await W(300)
    a=await ev("PAD.lx");await W(2600);b2=await ev("PAD.lx")
    check('a stick resting off centre is re-centred after 2 s',a>.03 and b2==0,[a,b2])
    await axes([0,0,0,0]);await W(2600)
    # autopilot is cancelled by the stick
    await ev("apOn=true");await axes([1,0,0,0]);await W(500);check('stick cancels autopilot',await ev("apOn===false"));await axes([0,0,0,0]);await W(300)
    # ---- the mouse retakes steering only after it moves
    await pg.mouse.move(1150,430);await W(200)
    check('mouse steers before the pad is used',await ev("steerInput().yaw")<-.1)
    await tap(2);await W(100)
    check('pad used: the off-centre mouse is ignored',abs(await ev("steerInput().yaw"))<.001)
    await pg.mouse.move(1120,420);await W(250)
    check('mouse moved: it steers again',await ev("steerInput().yaw")<-.1)
    await pg.keyboard.press('KeyZ');await W(100)
    check('key pressed: prompts name keys',await ev("kb('fire')+'|'+kb('act')")=='Space|E')
    await tap(2)
    check('pad pressed: prompts name pad again',await ev("kb('fire')")=='RT')
    await pg.mouse.move(700,430);await W(300)
    # ---- the mapping table: spy on the keys sent, the game does not see them
    exp=json.loads(await ev("JSON.stringify(PAD_MAP.map(r=>[r[0],r[1],r[2],r[3]]))"))
    code=json.loads(await ev("JSON.stringify(Object.assign({},KEY_DEF,{boost:'ShiftLeft'}))"))
    await ev("window.__spy=true");bi={'A':0,'B':1,'X':2,'Y':3,'LB':4,'RB':5,'LT':6,'RT':7,'BACK':8,'START':9,'L3':10,'R3':11,'UP':12,'DOWN':13,'LEFT':14,'RIGHT':15}
    spec={'cycleBack':'Tab+S','subCycle':'KeyT+S','ordNext':'KeyP+S'}
    bad=[]
    for lay,mods in enumerate([[],[4],[8]]):
      for r in exp:
        act=r[1+lay]
        if not act:continue
        await ev("__ks.length=0")
        for m in mods:await setb(m,True)
        if mods:await F(4)
        await setb(bi[r[0]],True);await F(4);await W(60);await F(3);await setb(bi[r[0]],False);await F(4)
        for m in mods:await setb(m,False)
        await F(4)
        ks=await ev("__ks.slice()")
        if act=='gunsel':want='Digit1' if await ev("S.player.wpn==='laser'") else 'Digit2'
        elif act in spec:want=spec[act]
        else:want=code[act]
        if not ks or ks[0]!=want:bad.append((lay,r[0],act,ks,want))
    check('every button on every layer sends its action key',not bad,bad[:4])
    await ev("window.__spy=false")
    # Back tapped alone opens the map; held with a button it does not
    await setb(8,True);await F(1);await setb(8,False);await F(4);check('Back tap opens the galaxy map',await ev("!$('map').hidden"))
    await tap(1);check('B closes the map',await ev("$('map').hidden"),await ev("JSON.stringify({ui:PAD.ui,open:PAD.uiEls.map(e=>e&&!e.hidden?e.id:0).filter(x=>x),b:Array.from(PAD.b).join(''),sw:Array.from(PAD.swallow).join(''),live:PAD.live,kw:keyWait,run:running})"))
    await setb(8,True);await W(150);await tap(13);await setb(8,False);await W(200);check('Back held with a button does not open the map',await ev("$('map').hidden"))
    # real handlers: thrust, afterburner and fire are held, released with the button
    await setb(6,True);await setb(7,True);await setb(5,True);await F(5);await W(100)
    check('LT RT RB hold thrust, fire, afterburner',await ev("!!(keys.KeyW&&keys.Space&&keys.ShiftLeft)"))
    await setb(6,False);await setb(7,False);await setb(5,False);await F(5)
    check('released with the buttons',await ev("!(keys.KeyW||keys.Space||keys.ShiftLeft)"))
    # rebinding is honoured: the pad sends the physical key bound to the action
    await ev("KEYB={flare:'KeyX',fa:'KeyB'};keyRemap()");await ev("__ks.length=0;window.__spy=true");await tap(13);ks=await ev("__ks.slice()");await ev("window.__spy=false;KEYB={};keyRemap()")
    check('rebinding honoured (flare moved to X sends KeyX)',ks[:1]==['KeyX'],ks)
    # held buttons are released when the pad vanishes
    await setb(6,True);await F(5);await W(100);k1=await ev("!!keys.KeyW");await pg.evaluate("__fon=false");await W(300);k2=await ev("!!keys.KeyW")
    check('thrust held then pad unplugged: released',k1 and not k2 and await ev("PAD.live===false"),[k1,k2])
    check('unplugged: prompts back to keys',await ev("kb('fire')")=='Space')
    await setb(6,False);await pg.evaluate("__fon=true");await W(500)
    # PlayStation naming
    await pg.evaluate("__fp=__mk('DualSense Wireless Controller (STANDARD GAMEPAD Vendor: 054c Product: 0ce6)','standard',[0,0,0,0]);__fon=true");await W(500);await tap(2)
    nm=await ev("kb('act')+'|'+kb('fire')+'|'+kb('mine')")
    check('PlayStation pad: Cross, R2, Triangle',nm=='Cross|R2|Triangle',nm)
    # audio wake
    check('first pad press tried to wake the audio',await ev("!!AU.ctx"))
    # on-screen keyboard
    await ev("padKbOpen($('mpName'))");await W(200);await ev("padKbKey('#shift');padKbKey('q');padKbKey('x')")
    v=await ev("$('mpName').value")
    check('on-screen keyboard types into a text box',v=='TesterQx',v)
    await ev("padKbKey('#done')");await W(100)
    # comms open: it is a screen; B closes it
    await pg.evaluate("__fp=__mk('Pad C (STANDARD GAMEPAD)','standard',[0,0,0,0]);__fon=true");await W(500)
    await tap(2);await ev("W.ftgt=W.player;openComms()");await W(300)
    check('comms is a screen: pointer mode',await ev("PAD.ui&&commsOpen()"))
    await tap(1);await W(200);check('B closes comms',await ev("!commsOpen()"))
    check('no page errors so far',not errs,errs[:2])
    await pg.context.close()
    # ---- screenshots at 2x
    pg=await boot(b,1280,800,2);ev=lambda c:pg.evaluate('c=>__dg.ev(c)',c)
    await pg.evaluate("__fp=__mk('Xbox 360 Controller (STANDARD GAMEPAD Vendor: 045e Product: 028e)','standard',[0,0,0,0]);__fon=true");await pg.wait_for_timeout(600)
    async def tap2(i):
      await pg.evaluate("i=>{__fp.buttons[i].pressed=true;__fp.buttons[i].value=1}",i);await pg.wait_for_timeout(300);await pg.evaluate("i=>{__fp.buttons[i].pressed=false;__fp.buttons[i].value=0}",i);await pg.wait_for_timeout(150)
    await tap2(15);await ev("(()=>{const b=[...document.querySelectorAll('#dTabs .mtab')].find(x=>/Trade/.test(x.textContent));const r=b.getBoundingClientRect();PAD.px=r.left+r.width/2+10;PAD.py=r.top+r.height/2+6;padPtrMove()})()");await pg.wait_for_timeout(300)
    await pg.screenshot(path=D+'pad_dock_pointer.png')
    await tap2(9);await ev("PAD.dirty=true");await pg.wait_for_timeout(400)
    await ev("$('padList').scrollIntoView({block:'start'})");await pg.wait_for_timeout(300)
    await pg.screenshot(path=D+'pad_controller_section.png')
    check('no page errors',not errs,errs[:2])
    print('FAILED' if fails else 'ALL OK',fails)
    print('errors',errs[:3]);await b.close()
asyncio.run(main())
