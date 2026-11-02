# Driftgate Beyond: miners and haulers in the three faction design languages (preview, not in the model pack yet).
# Same conventions and helpers as beyond_hulls.py. Miners carry a mining-laser head (lens forward) and charge launchers;
# haulers show their cargo. Within a faction every size has its own silhouette.
import math
import numpy as np
from beyond_hulls import Mesh,LIGHT,MID,DARK,ACC,GLASS,GLOW,WIN,loft,box,plate,barrel,ring,LENS,HEX,DIA,lens_role,hex_role

def tube(M,pts,rad,role,sh=1.0,sides=8,cap0=True,cap1=True):
    M.tube(pts,rad,sides,lambda i,j,n,p:(role,sh),cap0=cap0,cap1=cap1)
def laserhead(M,base,size,role=ACC,glass=GLASS,dz=1):
    # a mining-laser head: a collar, a short barrel and a lens at the front
    b=np.array(base,float)
    tube(M,[b,b+[0,0,dz*size*.9]],[size*.55,size*.45],MID,.95)
    ring(M,tuple(b+[0,0,dz*size*.25]),size*.6,size*.08,role,seg=14,sides=5)
    M.blob(tuple(b+[0,0,dz*size*1.0]),size*.4,glass,sub=1,squash=(1,1,.6),noise=0)
def launcher(M,base,n,role=DARK):
    # a row of charge-launcher tubes
    for k in range(n):tube(M,[np.array(base)+[k*.07-(n-1)*.035,0,0],np.array(base)+[k*.07-(n-1)*.035,0,.18]],[.028,.028],role,.9,6)
def container(M,c,size,stripe=ACC,role=MID):
    box(M,c,size,role);w,h,l=size
    for z in (-l*.3,l*.3):box(M,(c[0],c[1],c[2]+z),(w*1.02,h*1.02,l*.06),stripe,sh=.9)

# ============================================================== HALCYON: swept, bird-like, glass canopies, emitter nodes
def wren():      # light miner: a small bird with a laser beak under the nose
    M=Mesh(51)
    loft(M,[(-.8,LENS(.13,.11)),(-.5,LENS(.18,.15)),(.1,LENS(.18,.16)),(.5,LENS(.12,.11)),(.75,LENS(.04,.04,-.02))],lens_role)
    M.blob((0,.15,.25),.1,GLASS,sub=2,squash=(.9,.75,2.0),noise=0)
    laserhead(M,(0,-.22,.5),.16)
    tube(M,[(0,-.14,.2),(0,-.22,.5)],[.06,.06],MID,.9,6)
    loft(M,[(-.65,LENS(.16,.1,-.18)),(-.35,LENS(.28,.2,-.24)),(.05,LENS(.28,.2,-.24)),(.3,LENS(.14,.1,-.18))],(MID,.9))   # fat ore hopper belly
    for z in (-.3,-.05):plate(M,[(-.27,-.25,z),(.27,-.25,z),(.25,-.4,z),(-.25,-.4,z)],.02,ACC,.9)
    for sx in (1,-1):
        plate(M,[(sx*.15,.02,.0),(sx*.45,.05,-.3),(sx*.42,.05,-.45),(sx*.15,.02,-.45)],.03,LIGHT)
        M.blob((sx*.44,.05,-.38),.04,WIN,sub=1,noise=0)
        plate(M,[(sx*.1,.1,-.5),(sx*.22,.32,-.78),(sx*.22,.32,-.86),(sx*.1,.1,-.82)],.02,ACC,.95)
        launcher(M,(sx*.24,-.08,-.1),2)
    M.vent((0,0,-.82),.09)
    return M
def plover():    # medium miner: wide body, two streamlined ore hoppers, twin laser legs forward
    M=Mesh(52)
    loft(M,[(-1.0,LENS(.18,.13)),(-.6,LENS(.26,.18)),(.2,LENS(.25,.19)),(.65,LENS(.15,.13)),(.95,LENS(.04,.04,-.02))],lens_role)
    M.blob((0,.2,.38),.12,GLASS,sub=2,squash=(.9,.75,2.2),noise=0)
    for sx in (1,-1):
        pts=[(sx*.42,-.05,z) for z in (-.85,-.6,0,.3)]
        tube(M,pts,[.04,.13,.14,.05],MID,.95,10)                                                                   # ore hopper
        for z in (-.45,-.15,.12):ring(M,(sx*.42,-.05,z),.14,.012,ACC,seg=14,sides=4)
        tube(M,[(sx*.18,-.12,.4),(sx*.2,-.2,.85)],[.035,.035],LIGHT,.9,6);laserhead(M,(sx*.2,-.2,.85),.1)          # laser legs
        plate(M,[(sx*.22,.04,-.1),(sx*.8,.06,-.55),(sx*.76,.06,-.66),(sx*.22,.04,-.62)],.03,LIGHT,.95)
        M.blob((sx*.78,.06,-.6),.045,WIN,sub=1,noise=0)
        launcher(M,(sx*.42,.08,.25),2)
        M.vent((sx*.42,-.05,-.87),.05)
    plate(M,[(0,.15,-.55),(0,.45,-.92),(0,.45,-1.0),(0,.13,-.98)],.025,ACC)
    M.vent((0,0,-1.02),.1)
    return M
def heron():     # heavy miner: a long neck carrying a great laser head, a deep belly hold, drone bays at the wingtips
    M=Mesh(53)
    loft(M,[(-1.25,LENS(.2,.15)),(-.8,LENS(.34,.26)),(-.1,LENS(.36,.3)),(.35,LENS(.24,.2)),(.55,LENS(.1,.1,.05))],lens_role)
    loft(M,[(-1.05,LENS(.26,.16,-.3)),(-.6,LENS(.44,.34,-.42)),(.0,LENS(.44,.34,-.42)),(.35,LENS(.26,.18,-.3))],(MID,.9))   # deep belly hold
    for z in (-.55,-.3,-.05):plate(M,[(-.3,-.75,z),(.3,-.75,z),(.3,-.75,z-.18),(-.3,-.75,z-.18)],.02,DARK)              # hold hatches
    for z in (-.7,.15):plate(M,[(-.45,-.42,z),(.45,-.42,z),(.4,-.68,z),(-.4,-.68,z)],.02,ACC,.9)
    tube(M,[(0,.1,.5),(0,.35,.95),(0,.4,1.35)],[.08,.07,.07],LIGHT,1.0,8)                                         # the neck, raised
    laserhead(M,(0,.4,1.35),.2)
    M.blob((0,.33,.05),.13,GLASS,sub=2,squash=(.9,.7,2.0),noise=0)
    for sx in (1,-1):
        plate(M,[(sx*.32,.05,.2),(sx*1.25,.0,-.5),(sx*1.2,.0,-.68),(sx*.32,.05,-.7)],.05,LIGHT)
        box(M,(sx*1.2,-.02,-.55),(.18,.14,.36),MID);plate(M,[(sx*1.11,-.09,-.44),(sx*1.29,-.09,-.44),(sx*1.29,-.09,-.66),(sx*1.11,-.09,-.66)],.01,DARK)   # drone bay
        M.blob((sx*1.2,.08,-.55),.05,WIN,sub=1,noise=0)
        launcher(M,(sx*.3,.18,.25),3)
        plate(M,[(sx*.15,.2,-.8),(sx*.3,.6,-1.2),(sx*.3,.6,-1.3),(sx*.15,.18,-1.25)],.03,ACC,.95)
        M.vent((sx*.13,0,-1.27),.09)
    return M
def tern():      # light hauler: a slim dart with a cargo spine and a forked tail
    M=Mesh(54)
    loft(M,[(-.85,LENS(.12,.1)),(-.4,LENS(.17,.15)),(.3,LENS(.15,.13)),(.7,LENS(.05,.05,-.02)),(.85,LENS(.01,.01,-.03))],lens_role)
    M.blob((0,.14,.38),.09,GLASS,sub=2,squash=(.9,.75,2.0),noise=0)
    for k in range(3):container(M,(0,.2,-.05-k*.24),(.2,.12,.2))                                                 # cargo spine
    for sx in (1,-1):
        plate(M,[(sx*.12,0,.15),(sx*.55,0,-.25),(sx*.5,0,-.35),(sx*.12,0,-.3)],.025,LIGHT)
        plate(M,[(sx*.06,.02,-.6),(sx*.42,.05,-1.15),(sx*.36,.05,-1.15),(sx*.04,.02,-.8)],.02,ACC)                  # forked tail
        M.blob((sx*.52,0,-.3),.035,WIN,sub=1,noise=0)
    M.vent((0,0,-.87),.08)
    barrel(M,(0,-.1,.3),.3,.018)
    return M
def albatross(): # medium hauler: a glider's long wings over a cargo body, twin engines
    M=Mesh(55)
    loft(M,[(-1.05,LENS(.18,.16)),(-.5,LENS(.28,.24)),(.4,LENS(.26,.22)),(.85,LENS(.12,.11)),(1.05,LENS(.03,.03,-.02))],lens_role)
    M.blob((0,.23,.6),.11,GLASS,sub=2,squash=(.9,.7,2.0),noise=0)
    for k in range(4):container(M,(0,-.22,.35-k*.3),(.36,.16,.26),role=DARK)                                      # cargo under the body
    for sx in (1,-1):
        plate(M,[(sx*.25,.12,.25),(sx*1.75,.18,-.15),(sx*1.72,.18,-.32),(sx*.25,.12,-.3)],.035,LIGHT)                # long glider wing
        M.blob((sx*1.74,.18,-.24),.05,WIN,sub=1,noise=0)
        tube(M,[(sx*.55,.05,.1),(sx*.55,.05,-.7),(sx*.55,.05,-.8)],[.07,.09,.08],MID,.95,10,cap1=False);M.vent((sx*.55,.05,-.8),.07)
        tube(M,[(sx*.32,.26,.75),(sx*.32,.26,.6),(sx*.32,.26,-.45),(sx*.32,.26,-.6)],[.04,.13,.13,.05],LIGHT,.95,10)  # long cargo pod over the wing root
        for z in (.35,.0,-.3):ring(M,(sx*.32,.26,z),.135,.012,ACC,seg=14,sides=4)
        plate(M,[(sx*.15,.2,-.7),(sx*.32,.52,-1.05),(sx*.32,.52,-1.13),(sx*.15,.2,-1.05)],.025,ACC,.95)
    barrel(M,(0,-.1,.7),.3,.02)
    return M
def pelican():   # heavy hauler: a deep cargo pouch under the forward body, broad and four-engined
    M=Mesh(56)
    loft(M,[(-1.35,LENS(.32,.26)),(-.7,LENS(.46,.36)),(.4,LENS(.42,.34)),(1.0,LENS(.2,.16,.08)),(1.25,LENS(.05,.05,.1))],lens_role)
    loft(M,[(-.6,LENS(.36,.2,-.35)),(.0,LENS(.44,.32,-.45)),(.6,LENS(.36,.3,-.4)),(1.0,LENS(.12,.1,-.2))],(MID,.9))   # the pouch
    for z in (-.3,.1,.5):plate(M,[(-.44,-.43,z),(.44,-.43,z),(.4,-.7,z),(-.4,-.7,z)],.02,ACC,.9)                     # pouch ribs
    M.blob((0,.36,.75),.14,GLASS,sub=2,squash=(.9,.7,1.8),noise=0)
    for sx in (1,-1):
        plate(M,[(sx*.42,.1,.3),(sx*1.3,.12,-.4),(sx*1.26,.12,-.6),(sx*.42,.1,-.65)],.05,LIGHT)
        M.blob((sx*1.28,.12,-.5),.06,WIN,sub=1,noise=0)
        for dx in (.25,.75):tube(M,[(sx*dx,.0,-.6),(sx*dx,.0,-1.35),(sx*dx,0,-1.45)],[.09,.12,.1],MID,.95,10,cap1=False);M.vent((sx*dx,0,-1.45),.09)
        plate(M,[(sx*.25,.3,-.9),(sx*.42,.7,-1.3),(sx*.42,.7,-1.4),(sx*.25,.28,-1.35)],.03,ACC,.95)
    for k in range(4):plate(M,[(-.16,.37,.3-k*.25),(.16,.37,.3-k*.25),(.16,.37,.22-k*.25),(-.16,.37,.22-k*.25)],.006,ACC,.9)
    return M

# ============================================================== VARKESH: blocky slabs, exposed guns, square drives
def pick():      # light miner: a box with one heavy pick forward
    M=Mesh(61)
    loft(M,[(-.75,HEX(.24,.2)),(-.2,HEX(.28,.23)),(.35,HEX(.24,.2)),(.55,HEX(.16,.14,-.02))],hex_role)
    plate(M,[(-.07,.22,.4),(.07,.22,.4),(.07,.25,.15),(-.07,.25,.15)],.025,GLASS)
    box(M,(0,-.12,.62),(.14,.14,.3),DARK);plate(M,[(0,-.05,.75),(0,-.22,.75),(0,-.3,1.08),(0,-.12,1.02)],.06,ACC)   # the pick
    laserhead(M,(0,.12,.55),.08)
    for sx in (1,-1):
        box(M,(sx*.32,-.05,-.2),(.12,.22,.6),MID)
        launcher(M,(sx*.32,.1,.05),2)
        box(M,(sx*.13,0,-.82),(.17,.16,.12),DARK);M.vent((sx*.13,0,-.88),.06)
    box(M,(0,-.25,-.25),(.3,.12,.5),DARK)                                                                         # ore bin
    return M
def gouge():     # medium miner: a wide armoured scoop with laser emitters on its lip, side ore bins
    M=Mesh(62)
    loft(M,[(-.95,HEX(.3,.26)),(-.3,HEX(.36,.3)),(.25,HEX(.32,.28))],hex_role)
    plate(M,[(-.09,.29,.2),(.09,.29,.2),(.09,.33,-.05),(-.09,.33,-.05)],.025,GLASS)
    plate(M,[(-.55,-.25,.3),(.55,-.25,.3),(.6,-.3,.95),(-.6,-.3,.95)],.06,DARK)                                    # scoop floor
    for sx in (1,-1):plate(M,[(sx*.55,-.25,.3),(sx*.6,-.3,.95),(sx*.62,.12,.85),(sx*.56,.2,.3)],.06,MID)            # scoop walls
    plate(M,[(-.56,.2,.3),(.56,.2,.3),(.5,.22,.45),(-.5,.22,.45)],.05,MID)
    for x in (-.4,0,.4):laserhead(M,(x,-.28,.95),.07)                                                              # emitters on the lip
    box(M,(0,-.27,.98),(1.25,.05,.06),ACC)
    for sx in (1,-1):
        box(M,(sx*.48,0,-.45),(.2,.34,.7),MID);box(M,(sx*.48,.19,-.45),(.22,.04,.72),ACC,sh=.9)                    # ore bins
        launcher(M,(sx*.48,.22,-.05),2)
        for dy in (.1,-.1):box(M,(sx*.16,dy,-1.02),(.17,.15,.12),DARK);M.vent((sx*.16,dy,-1.08),.06)
    return M
def sledge():    # heavy miner: a hammerhead charge battery on a thick spine, ore bins aft
    M=Mesh(63)
    box(M,(0,0,.95),(1.3,.5,.5),MID,taper=(.95,.95))                                                             # the hammerhead
    for x in (-.45,-.15,.15,.45):
        for y in (.1,-.1):tube(M,[(x,y,1.2),(x,y,1.3)],[.06,.06],DARK,.9,6)                                         # charge launcher battery
    for x in (-.55,.55):laserhead(M,(x,.0,1.2),.12)
    box(M,(0,.27,.95),(1.32,.04,.3),ACC,sh=.9)
    loft(M,[(-1.3,HEX(.36,.32)),(-.6,HEX(.4,.36)),(.2,HEX(.32,.3)),(.7,HEX(.28,.26))],hex_role)                    # thick spine
    box(M,(0,.45,.3),(.3,.16,.36),MID);plate(M,[(-.11,.54,.46),(.11,.54,.46),(.11,.54,.3),(-.11,.54,.3)],.02,GLASS)
    for sx in (1,-1):
        for k,z in enumerate((-.25,-.75)):box(M,(sx*.55,-.05,z),(.28,.4,.42),MID if k else DARK);box(M,(sx*.55,.16,z),(.3,.04,.44),ACC,sh=.9)
        for dy in (.15,-.15):box(M,(sx*.2,dy,-1.38),(.2,.18,.14),DARK);M.vent((sx*.2,dy,-1.45),.07)
        box(M,(sx*.7,-.05,.95),(.08,.4,.4),DARK)
    return M
def runner():    # light hauler: a blocky box hauler with one container rack, twin drives
    M=Mesh(64)
    loft(M,[(-.2,HEX(.22,.2)),(.35,HEX(.24,.2)),(.62,HEX(.14,.12,-.02))],hex_role)
    plate(M,[(-.07,.2,.48),(.07,.2,.48),(.07,.23,.2),(-.07,.23,.2)],.025,GLASS)
    container(M,(0,.02,-.6),(.5,.42,.95))                                                                         # one big container
    for sx in (1,-1):
        for sy in (1,-1):box(M,(sx*.3,sy*.25,-.6),(.06,.06,1.1),DARK)                                               # open frame rails
        for z in (-.12,-.6,-1.08):box(M,(sx*.3,0,z),(.06,.56,.06),DARK)
        box(M,(sx*.2,0,-1.22),(.18,.18,.14),DARK);M.vent((sx*.2,0,-1.29),.065)
    box(M,(0,0,-1.12),(.6,.12,.1),DARK)
    barrel(M,(0,-.17,.3),.35,.025)
    return M
def bulwark():   # medium hauler: stacked containers in an armoured frame, gun turret on top
    M=Mesh(65)
    loft(M,[(.3,HEX(.3,.26)),(.75,HEX(.26,.22)),(.98,HEX(.14,.12,-.02))],hex_role)
    plate(M,[(-.08,.27,.78),(.08,.27,.78),(.08,.3,.5),(-.08,.3,.5)],.025,GLASS)
    for y in (.22,-.22):
        for k in range(3):container(M,(0,y,-.0-k*.38),(.56,.38,.34))
    for sx in (1,-1):
        box(M,(sx*.36,0,-.38),(.08,.92,1.25),MID)                                                                 # armoured frame side
        for k in range(3):box(M,(sx*.41,0,.15-k*.4),(.03,.8,.1),ACC,sh=.9)
        for dy in (.22,-.22):box(M,(sx*.18,dy,-1.08),(.18,.18,.14),DARK);M.vent((sx*.18,dy,-1.15),.065)
    box(M,(0,.5,-.38),(.74,.06,1.25),MID)
    box(M,(0,.6,.0),(.22,.14,.26),DARK)
    for sx in (1,-1):barrel(M,(sx*.05,.62,.1),.4,.022)
    return M
def rampart():   # heavy hauler: a long cargo barge walled by armour ramparts, guns on the wall corners
    M=Mesh(66)
    box(M,(0,-.25,-.1),(1.0,.1,2.4),DARK)                                                                         # barge deck
    for x in (-.25,.25):
        for k in range(5):container(M,(x,.0,.85-k*.45),(.42,.4,.38))
    for sx in (1,-1):
        box(M,(sx*.55,.05,-.1),(.12,.6,2.4),MID)                                                                  # rampart walls
        for k in range(6):box(M,(sx*.55,.39,.95-k*.42),(.14,.08,.18),MID,sh=1.05)                                 # crenellations
        for z in (1.05,-1.25):box(M,(sx*.55,.45,z),(.18,.12,.18),DARK);barrel(M,(sx*.55,.5,z+.05),.35,.025)        # corner guns
        for dy in (.15,-.12):box(M,(sx*.3,dy,-1.42),(.22,.2,.16),DARK);M.vent((sx*.3,dy,-1.5),.08)
    loft(M,[(1.25,HEX(.36,.3,.05)),(1.6,HEX(.3,.25,.03)),(1.82,HEX(.16,.14,.0))],hex_role)                         # bridge prow
    plate(M,[(-.1,.33,1.62),(.1,.33,1.62),(.1,.36,1.35),(-.1,.36,1.35)],.025,GLASS)
    box(M,(0,0,1.15),(1.0,.5,.2),MID)
    return M

# ============================================================== OSTROVA: spires, halos, sensor masts, crystal
SP=lambda i,j:((LIGHT,1.0) if j in (0,1) else (MID,.92))
def glim():      # light miner: a small spire with a glowing crystal lens at the nose and a halo
    M=Mesh(71)
    loft(M,[(-.85,DIA(.05,.05)),(-.5,DIA(.13,.11)),(.05,DIA(.15,.14)),(.45,DIA(.09,.09)),(.62,DIA(.05,.05))],SP)
    M.blob((0,0,.72),.11,WIN,sub=2,squash=(1,1,1.3),noise=0);ring(M,(0,0,.66),.12,.015,ACC,seg=16,sides=5)       # crystal mining lens
    ring(M,(0,0,-.3),.34,.03,ACC)
    for k in range(3):
        a=math.pi/2+k*2*math.pi/3;ca,sa=math.cos(a),math.sin(a)
        plate(M,[(ca*.1,sa*.1,-.1),(ca*.34,sa*.34,-.25),(ca*.34,sa*.34,-.35),(ca*.1,sa*.1,-.6)],.02,LIGHT,.95)
        M.blob((ca*.34,sa*.34,-.3),.045,GLASS,sub=1,noise=0)
    M.blob((0,.12,.2),.07,GLASS,sub=2,squash=(.9,.7,2.0),noise=0)
    launcher(M,(0,-.13,-.15),2,ACC)
    M.vent((0,0,-.87),.05)
    return M
def lumen():     # medium miner: a crown of three crystal lenses on forward arms, glass ore spheres
    M=Mesh(72)
    loft(M,[(-1.0,DIA(.06,.06)),(-.6,DIA(.16,.14)),(.0,DIA(.19,.18)),(.45,DIA(.12,.12)),(.7,DIA(.04,.04))],SP)
    for k in range(3):
        a=math.pi/2+k*2*math.pi/3;ca,sa=math.cos(a),math.sin(a)
        tube(M,[(ca*.12,sa*.12,.2),(ca*.32,sa*.32,.6),(ca*.3,sa*.3,.85)],[.03,.025,.025],LIGHT,.9,6)                   # crown arms
        M.blob((ca*.3,sa*.3,.92),.08,WIN,sub=2,squash=(1,1,1.3),noise=0)
        b=a+math.pi/3;M.blob((math.cos(b)*.3,math.sin(b)*.3,-.35),.12,GLASS,sub=2,noise=0)                         # ore spheres
        tube(M,[(math.cos(b)*.15,math.sin(b)*.15,-.35),(math.cos(b)*.22,math.sin(b)*.22,-.35)],[.02,.02],LIGHT,.9,5)
        plate(M,[(ca*.1,sa*.1,-.6),(ca*.5,sa*.5,-.9),(ca*.46,sa*.46,-1.0),(ca*.08,sa*.08,-.95)],.02,MID)
    ring(M,(0,0,.6),.32,.02,ACC,seg=22,sides=5)
    M.blob((0,.15,.25),.08,GLASS,sub=2,squash=(.9,.7,2.0),noise=0)
    M.vent((0,0,-1.02),.06)
    return M
def delve():     # heavy miner: a long drill-spire with stacked halos and a great crystal focus; ore in crystal sacs
    M=Mesh(73)
    loft(M,[(-1.3,DIA(.08,.08)),(-.8,DIA(.26,.24)),(.0,DIA(.3,.28)),(.7,DIA(.2,.2)),(1.15,DIA(.1,.1))],SP)
    star=lambda w:[(math.cos(a)*(w if k%2==0 else w*.6),math.sin(a)*(w if k%2==0 else w*.6)) for k,a in enumerate(np.linspace(0,2*math.pi,10,endpoint=False))]
    loft(M,[(1.1,star(.1)),(1.3,star(.22)),(1.6,star(.02))],lambda i,j:((WIN,1.0) if j%2 else (GLASS,1.0)))      # the great focus
    for z,R in ((.95,.32),(.75,.4),(.55,.46)):ring(M,(0,0,z),R,.025,ACC,seg=24,sides=5)                           # stacked halos
    for k in range(4):
        a=math.pi/4+k*math.pi/2;ca,sa=math.cos(a),math.sin(a)
        loft(M,[(-.9,DIA(.03,.03,ca*.4,sa*.4)),(-.55,DIA(.12,.12,ca*.42,sa*.42)),(-.15,DIA(.11,.11,ca*.4,sa*.4)),(.1,DIA(.03,.03,ca*.36,sa*.36))],lambda i,j:((GLASS,1.0) if j%2 else (WIN,.8)))   # crystal ore sacs
        tube(M,[(ca*.22,sa*.22,-.4),(ca*.36,sa*.36,-.4)],[.02,.02],LIGHT,.9,5)
        plate(M,[(ca*.2,sa*.2,-.9),(ca*.7,sa*.7,-1.25),(ca*.64,sa*.64,-1.35),(ca*.16,sa*.16,-1.3)],.025,MID)
    M.blob((0,.3,.25),.1,GLASS,sub=2,squash=(.9,.7,2.0),noise=0)
    launcher(M,(0,-.3,.4),3,ACC)
    M.vent((0,0,-1.32),.07)
    return M
def drift():     # light hauler: a slim spire with two long cargo capsules slung either side
    M=Mesh(74)
    loft(M,[(-.85,DIA(.05,.05)),(-.4,DIA(.12,.11)),(.3,DIA(.12,.11)),(.7,DIA(.04,.04)),(.85,DIA(.005,.005))],SP)
    for sx in (1,-1):
        tube(M,[(sx*.26,0,-.65),(sx*.26,0,-.45),(sx*.26,0,.25),(sx*.26,0,.45)],[.03,.1,.1,.03],LIGHT,.95,10)
        for z in (-.3,.1):ring(M,(sx*.26,0,z),.105,.012,ACC,seg=14,sides=4)
        tube(M,[(sx*.08,0,-.1),(sx*.18,0,-.1)],[.02,.02],LIGHT,.9,5)
    ring(M,(0,0,-.55),.3,.022,ACC)
    M.blob((0,.11,.25),.07,GLASS,sub=2,squash=(.9,.7,2.0),noise=0)
    plate(M,[(0,.08,-.5),(0,.3,-.75),(0,.28,-.85),(0,.06,-.8)],.02,MID)
    M.vent((0,0,-.87),.05)
    return M
def cairn():     # medium hauler: a spire threaded through stacked cargo drums, like stones in a cairn
    M=Mesh(75)
    loft(M,[(-1.1,DIA(.05,.05)),(-.8,DIA(.1,.1)),(.6,DIA(.1,.1)),(.95,DIA(.04,.04)),(1.1,DIA(.005,.005))],SP)
    for k,(z,R) in enumerate(((-.55,.3),(-.25,.36),(.05,.33),(.33,.27))):
        tube(M,[(0,0,z-.12),(0,0,z+.12)],[R,R],MID if k%2 else LIGHT,.95,12)                                       # cargo drums
        ring(M,(0,0,z+.12),R,.014,ACC,seg=22,sides=4)
    ring(M,(0,0,-.85),.36,.026,ACC)
    M.blob((0,.12,.65),.07,GLASS,sub=2,squash=(.9,.7,2.0),noise=0)
    for k in range(3):
        a=math.pi/2+k*2*math.pi/3;ca,sa=math.cos(a),math.sin(a)
        plate(M,[(ca*.1,sa*.1,-.75),(ca*.55,sa*.55,-1.0),(ca*.5,sa*.5,-1.1),(ca*.08,sa*.08,-1.05)],.02,MID)
    M.vent((0,0,-1.12),.06)
    return M
def monolith():  # heavy hauler: a great slab obelisk veined with crystal, cargo inside, a halo aft
    M=Mesh(76)
    box(M,(0,0,0),(.55,.95,2.4),MID,taper=(.75,.7))                                                               # the slab
    loft(M,[(1.2,[(-.21,-.33),(.21,-.33),(.21,.33),(-.21,.33)]),(1.55,[(-.02,-.05),(.02,-.05),(.02,.05),(-.02,.05)])],(LIGHT,1.0))   # tapered crown
    for sx in (1,-1):
        for k in range(4):plate(M,[(sx*.28,-.38+k*.04,.9-k*.5),(sx*.28,.38-k*.04,.75-k*.5),(sx*.28,.38-k*.04,.55-k*.5),(sx*.28,-.38+k*.04,.7-k*.5)],.01,WIN,.85)   # crystal veins
        plate(M,[(sx*.27,0,-.6),(sx*.7,0,-.95),(sx*.66,0,-1.05),(sx*.27,0,-1.05)],.025,MID)
    ring(M,(0,0,-.95),.62,.035,ACC)
    for k in range(4):a=k*math.pi/2+math.pi/4;M.blob((math.cos(a)*.62,math.sin(a)*.62,-.95),.06,GLASS,sub=1,noise=0)
    M.blob((0,.48,.7),.09,GLASS,sub=2,squash=(.8,.6,1.8),noise=0)
    M.tube([(0,.48,.2),(0,.85,.2)],[.02,.012],6,lambda i,j,n,p:(LIGHT,.9))
    for y,r in ((.72,.06),(.82,.04)):ring(M,(0,y,.2),r,.011,ACC,seg=12,sides=4,axis='y')
    for dy in (.25,-.25):M.vent((0,dy,-1.22),.08)
    return M

WORK=[('halcyon','Halcyon Accord',[('Wren','Light miner',wren),('Plover','Medium miner',plover),('Heron','Heavy miner',heron),('Tern','Light hauler',tern),('Albatross','Medium hauler',albatross),('Pelican','Heavy hauler',pelican)]),
      ('varkesh','Varkesh Dominion',[('Pick','Light miner',pick),('Gouge','Medium miner',gouge),('Sledge','Heavy miner',sledge),('Runner','Light hauler',runner),('Bulwark','Medium hauler',bulwark),('Rampart','Heavy hauler',rampart)]),
      ('ostrova','Ostrova Collective',[('Glim','Light miner',glim),('Lumen','Medium miner',lumen),('Delve','Heavy miner',delve),('Drift','Light hauler',drift),('Cairn','Medium hauler',cairn),('Monolith','Heavy hauler',monolith)])]
