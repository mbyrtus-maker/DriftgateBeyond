# Driftgate Beyond: miners and haulers (preview, not in the model pack yet). Third pass.
# Wholly new craft built in code, mixing two sources:
#  - Driftgate 1's work ships for proportion and purpose: stubby, wide industrial bodies; miners with forward drill arms and
#    mining lenses, ore hoppers and charge launchers; haulers with big holds, containers and intakes.
#  - Each faction's approved fighters for shape language:
#      Halcyon  lens hulls, glass canopies, swept and twin tails, emitter nodes, the Osprey's twin booms
#      Varkesh  hex slabs, chisel prows, the Talon's pincer sponsons, the Halberd's X of pods, square drives, armour bands
#      Ostrova  diamond spires, halos, the Wisp's crescent, the Vigil's prongs and crossed rings, crystal bodies
import math
import numpy as np
from beyond_hulls import Mesh,LIGHT,MID,DARK,ACC,GLASS,GLOW,WIN,loft,box,plate,barrel,ring,LENS,HEX,DIA,lens_role,hex_role
PI=math.pi

def finish(M,length,girth=1.12):
    # work ships: about 12% more girth than the fighters' proportions
    P=np.array(M.T,float);lo=P.reshape(-1,3).min(0);hi=P.reshape(-1,3).max(0);c=(lo+hi)/2;k=length/(hi[2]-lo[2])
    M.T=list((P-c)*k*np.array([girth,girth,1.0]));return M
def tube(M,pts,rad,role,sh=1.0,sides=8,cap0=True,cap1=True):M.tube(pts,rad,sides,lambda i,j,n,p:(role,sh),cap0=cap0,cap1=cap1)
def drill(M,base,length,r,role=DARK):
    # a drill bit: a cone with collar bands, pointing +z
    b=np.array(base,float);tube(M,[b,b+[0,0,length*.35],b+[0,0,length]],[r,r*.8,r*.04],role,.95,8,cap0=True,cap1=False)
    for t in (.12,.42):ring(M,tuple(b+[0,0,length*t]),r*(1-.25*t)+.005,r*.12,ACC,seg=12,sides=4)
def lens_head(M,base,r,glow=WIN):
    # a mining-laser lens on a collar, facing +z
    b=np.array(base,float);ring(M,tuple(b),r*1.1,r*.18,ACC,seg=14,sides=5);M.blob(tuple(b+[0,0,r*.25]),r*.8,glow,sub=1,squash=(1,1,.55),noise=0)
def launcher(M,base,n,role=DARK,sp=.08):
    for k in range(n):tube(M,[np.array(base)+[k*sp-(n-1)*sp/2,0,0],np.array(base)+[k*sp-(n-1)*sp/2,0,.2]],[.032,.032],role,.9,6)
def vents(M,pts,r):[M.vent(p,r) for p in pts]
def sqdrive(M,c,s):box(M,c,(s,s*.9,s*.7),DARK);M.vent((c[0],c[1],c[2]-s*.38),s*.38)
def hatch(M,c,w,l,y=None):plate(M,[(c[0]-w/2,c[1],c[2]+l/2),(c[0]+w/2,c[1],c[2]+l/2),(c[0]+w/2,c[1],c[2]-l/2),(c[0]-w/2,c[1],c[2]-l/2)],.012,DARK,.95)
def stacks(M,base,n,sp=.16,h=.3):
    # exhaust stacks standing up off the back
    for k in range(n):
        b=np.array(base,float)+[k*sp-(n-1)*sp/2,0,0];box(M,tuple(b+[0,.03,0]),(.13,.06,.13),DARK);tube(M,[b,b+[0,h,0]],[.065,.06],MID,1.0,8,cap1=True);ring(M,tuple(b+[0,h*.75,0]),.07,.014,ACC,seg=12,sides=4,axis='y');M.blob(tuple(b+[0,h+.005,0]),.045,DARK,sub=1,squash=(1,.3,1),noise=0)
def lights(M,pts,r=.035):
    # floodlights
    for p in pts:M.blob(p,r,WIN,sub=1,noise=0)
def ribs(M,zs,R,dy=0,r=.016):
    for z in zs:ring(M,(0,dy,z),R,r,ACC,seg=22,sides=4)
SP=lambda i,j:((LIGHT,1.0) if j in (0,1) else (MID,.92))
STAR=lambda w,h,n=10:[(math.cos(a)*(w if k%2==0 else w*.62),math.sin(a)*(h if k%2==0 else h*.62)) for k,a in enumerate(np.linspace(0,2*PI,n,endpoint=False))]
def crystal(M,z0,z1,w,h,dx=0,dy=0):
    loft(M,[(z0,[(x+dx,y+dy) for x,y in STAR(.02,.02)]),(z0+(z1-z0)*.25,[(x+dx,y+dy) for x,y in STAR(w,h)]),(z0+(z1-z0)*.7,[(x+dx,y+dy) for x,y in STAR(w*.85,h*.85)]),(z1,[(x+dx,y+dy) for x,y in STAR(.02,.02)])],
         lambda i,j:((WIN,1.0) if j%2 else (GLASS,1.0)))

# ============================================================== HALCYON
def wren():      # light miner: a chubby lens pod with a bubble canopy, two drill arms hugging the nose, stub wings, twin tails
    M=Mesh(51)
    loft(M,[(-.75,LENS(.2,.17)),(-.45,LENS(.34,.28)),(.1,LENS(.36,.3)),(.45,LENS(.3,.26)),(.62,LENS(.24,.2,.02)),(.72,LENS(.15,.12,.02))],lens_role)
    M.blob((0,.27,.32),.17,GLASS,sub=2,squash=(1,.8,1.4),noise=0)
    loft(M,[(-.5,LENS(.24,.12,-.24)),(-.1,LENS(.3,.16,-.28)),(.3,LENS(.2,.1,-.22))],(MID,.9))                     # ore hopper belly
    for sx in (1,-1):
        tube(M,[(sx*.36,-.06,-.25),(sx*.4,-.08,.35),(sx*.3,-.1,.72)],[.09,.085,.07],LIGHT,.95,10,cap1=False)        # drill arm
        drill(M,(sx*.3,-.1,.7),.35,.075)
        plate(M,[(sx*.34,.05,-.1),(sx*.72,.1,-.35),(sx*.68,.1,-.48),(sx*.34,.05,-.45)],.035,LIGHT)                    # stub wing
        M.blob((sx*.7,.1,-.41),.045,WIN,sub=1,noise=0)
        plate(M,[(sx*.14,.22,-.5),(sx*.22,.38,-.68),(sx*.22,.38,-.76),(sx*.14,.2,-.76)],.025,ACC,.95)                   # twin canted tails
        launcher(M,(sx*.2,-.3,-.05),2)
    lens_head(M,(0,-.12,.72),.07)                                                                                  # mining lens under the nose
    vents(M,[(.12,0,-.78),(-.12,0,-.78)],.08)
    ribs(M,(-.3,.05),.37);lights(M,[(.2,-.02,.72),(-.2,-.02,.72)])
    return finish(M,2.0)
def plover():    # medium miner: the Osprey's twin booms become fat ore hoppers with drills; a cockpit pod between
    M=Mesh(52)
    loft(M,[(-.6,LENS(.18,.15)),(-.2,LENS(.24,.2)),(.45,LENS(.2,.17)),(.8,LENS(.15,.13,-.01))],lens_role)            # cockpit pod
    M.blob((0,.2,.42),.13,GLASS,sub=2,squash=(.9,.75,2.0),noise=0)
    for sx in (1,-1):
        loft(M,[(-1.15,[(x+sx*.72,y) for x,y in LENS(.12,.12)]),(-.85,[(x+sx*.72,y) for x,y in LENS(.3,.27)]),(.15,[(x+sx*.72,y) for x,y in LENS(.32,.28)]),
                (.7,[(x+sx*.72,y) for x,y in LENS(.22,.2)]),(.95,[(x+sx*.72,y) for x,y in LENS(.1,.1)])],lens_role)        # hopper boom
        for z in (-.6,-.25,.1):hatch(M,(sx*.72,.285,z),.32,.22)
        drill(M,(sx*.72,0,.95),.45,.1)
        lens_head(M,(sx*.5,-.18,.8),.06)
        plate(M,[(sx*.2,.0,.2),(sx*.45,.0,.2),(sx*.45,.0,-.5),(sx*.2,.0,-.5)],.06,MID)                               # struts to the pod
        plate(M,[(sx*.72,.25,-.9),(sx*.72,.45,-1.1),(sx*.72,.45,-1.2),(sx*.72,.24,-1.2)],.03,ACC,.95)
        M.blob((sx*1.04,0,-.3),.05,WIN,sub=1,noise=0)
        M.vent((sx*.72,0,-1.16),.1)
        launcher(M,(sx*.72,-.27,.3),3)
    for sx in (1,-1):[ring(M,(sx*.72,0,z),.33,.016,ACC,seg=22,sides=4) for z in (-.75,.5)]
    lights(M,[(.15,-.04,.82),(-.15,-.04,.82)])
    return finish(M,2.6)
def heron():     # heavy miner: a broad flattened lens hull with two stacked hoppers, drills, four drives
    M=Mesh(53)
    loft(M,[(-1.2,LENS(.4,.22)),(-.7,LENS(.75,.32)),(.2,LENS(.8,.34)),(.75,LENS(.5,.26)),(1.0,LENS(.22,.14,.04))],lens_role)   # broad hull
    for x in (-.35,.35):loft(M,[(-.9,[(a+x,b+.28) for a,b in LENS(.12,.08)]),(-.6,[(a+x,b+.3) for a,b in LENS(.26,.2)]),(.3,[(a+x,b+.3) for a,b in LENS(.26,.2)]),(.55,[(a+x,b+.28) for a,b in LENS(.1,.07)])],lens_role)   # stacked hoppers
    for x in (-.35,.35):
        for z in (-.4,-.05,.25):ring(M,(x,.3,z),.265,.015,ACC,seg=18,sides=4)
    M.blob((0,.36,.72),.16,GLASS,sub=2,squash=(1.2,.7,1.5),noise=0)
    for sx in (1,-1):
        drill(M,(sx*.55,-.08,.9),.55,.12)
        plate(M,[(sx*.75,.0,-.1),(sx*1.25,.02,-.55),(sx*1.2,.02,-.75),(sx*.7,.0,-.7)],.06,LIGHT)
        box(M,(sx*1.15,-.04,-.6),(.18,.14,.3),MID);M.blob((sx*1.15,.08,-.6),.05,WIN,sub=1,noise=0)                # drone bays
        plate(M,[(sx*.55,.2,-.85),(sx*.65,.48,-1.12),(sx*.65,.48,-1.22),(sx*.55,.2,-1.2)],.035,ACC,.95)
        launcher(M,(sx*.6,-.3,.4),3)
        for dx in (.2,.5):M.vent((sx*dx,0,-1.22),.11)
    lights(M,[(.4,.0,1.0),(-.4,.0,1.0),(0,.18,1.02)])
    return finish(M,3.2)
def tern():      # light hauler: a short lens cockpit hull with its cargo hold joined on behind it, a forked tail and a glass canopy
    M=Mesh(54)
    loft(M,[(-.05,LENS(.2,.17)),(.25,LENS(.22,.19)),(.55,LENS(.18,.16)),(.72,LENS(.12,.1,-.01))],lens_role)            # cockpit hull
    M.blob((0,.17,.45),.11,GLASS,sub=2,squash=(.9,.75,1.8),noise=0)
    loft(M,[(-.9,LENS(.2,.17,.02)),(-.75,LENS(.3,.26,.02)),(-.25,LENS(.31,.27,.02)),(-.02,LENS(.21,.18))],lens_role)  # cargo hold, joined on behind
    for z in (-.65,-.45,-.25):ring(M,(0,.02,z),.31,.016,ACC,seg=20,sides=4)
    for k,z in enumerate((-.6,-.35)):hatch(M,(0,.285,z),.26,.18)
    for sx in (1,-1):
        plate(M,[(sx*.12,.18,-.75),(sx*.42,.24,-1.05),(sx*.34,.24,-1.05),(sx*.1,.18,-.88)],.03,ACC)                  # forked tail
        plate(M,[(sx*.2,.0,.35),(sx*.42,.02,.15),(sx*.4,.02,.05),(sx*.2,.0,.08)],.03,LIGHT)
        M.blob((sx*.41,.02,.1),.04,WIN,sub=1,noise=0)
        M.vent((sx*.12,.02,-.92),.08)
    lights(M,[(.09,-.04,.72),(-.09,-.04,.72)])
    return finish(M,2.0)
def albatross(): # medium hauler: a broad, thick flying-wing whose wings are cargo bays, twin tails, a raised glass bridge
    M=Mesh(55)
    sec=lambda w,h,dy=0:[(math.cos(a)*w,math.sin(a)*h*(1 if math.sin(a)>0 else .55)+dy) for a in np.linspace(0,2*PI,16,endpoint=False)]
    loft(M,[(-1.0,sec(.7,.14)),(-.6,sec(1.25,.24)),(.2,sec(1.1,.26)),(.75,sec(.55,.2)),(1.05,sec(.15,.08))],lambda i,j:((LIGHT,1.0) if j<8 else (MID,.92)))   # the flying-wing hull
    for sx in (1,-1):
        for k,z in enumerate((-.45,-.1,.25)):hatch(M,(sx*(.55+.0*k),.24 if z>-.3 else .22,z),.35,.25)
        plate(M,[(sx*.45,.2,-.7),(sx*.55,.45,-.95),(sx*.55,.45,-1.05),(sx*.45,.2,-1.0)],.035,ACC,.95)
        M.blob((sx*1.2,.0,-.4),.06,WIN,sub=1,noise=0)
        for dx in (.3,.75):M.vent((sx*dx,0,-1.0),.09)
    loft(M,[(.2,LENS(.14,.1,.22)),(.45,LENS(.16,.13,.26)),(.75,LENS(.08,.06,.22))],lens_role);M.blob((0,.38,.5),.11,GLASS,sub=2,squash=(1,.7,1.6),noise=0)
    lights(M,[(.35,-.02,1.0),(-.35,-.02,1.0)])
    return finish(M,2.6)
def pelican():   # heavy hauler: a huge bulbous cargo pouch hull between two big engine pylons
    M=Mesh(56)
    loft(M,[(-1.25,LENS(.3,.24)),(-.8,LENS(.6,.5,-.05)),(.2,LENS(.7,.62,-.12)),(.85,LENS(.5,.45,-.12)),(1.25,LENS(.15,.12,.05))],lens_role)   # the pouch hull
    for z in (-.4,.0,.4):ring(M,(0,-.12,z),.7 if z<.3 else .62,.02,ACC,seg=28,sides=4)
    M.blob((0,.45,.85),.16,GLASS,sub=2,squash=(1,.7,1.6),noise=0)
    for sx in (1,-1):
        tube(M,[(sx*1.0,.15,.6),(sx*1.0,.15,.35),(sx*1.0,.15,-1.35),(sx*1.0,.15,-1.5)],[.12,.24,.27,.25],MID,.95,12,cap1=False);M.vent((sx*1.0,.15,-1.5),.22)   # big engine pylons
        for z in (-.9,-.3,.2):ring(M,(sx*1.0,.15,z),.275,.016,ACC,seg=20,sides=4)
        plate(M,[(sx*.6,.2,.2),(sx*.8,.2,.15),(sx*.8,.2,-.55),(sx*.6,.2,-.6)],.08,LIGHT)
        plate(M,[(sx*1.0,.38,-1.05),(sx*1.0,.68,-1.3),(sx*1.0,.68,-1.42),(sx*1.0,.38,-1.4)],.035,ACC,.95)
        M.blob((sx*1.0,.42,.3),.06,WIN,sub=1,noise=0)
        hatch(M,(sx*.3,.5,-.1),.3,.6)
    M.vent((0,0,-1.27),.18)
    lights(M,[(.3,-.05,1.24),(-.3,-.05,1.24)])
    return finish(M,3.3)

# ============================================================== VARKESH
def pick():      # light miner: a stubby hex body with two short claw sponsons, each ending in a drill: the pick
    M=Mesh(61)
    loft(M,[(-.75,HEX(.26,.22)),(-.2,HEX(.32,.26)),(.35,HEX(.28,.23)),(.6,HEX(.24,.2,-.02))],hex_role)
    plate(M,[(-.08,.24,.45),(.08,.24,.45),(.08,.27,.18),(-.08,.27,.18)],.025,GLASS)
    for sx in (1,-1):
        loft(M,[(-.55,HEX(.11,.13,0,sx*.45)),(.1,HEX(.13,.15,0,sx*.47)),(.55,HEX(.1,.12,-.01,sx*.42))],hex_role)        # claw sponson
        drill(M,(sx*.42,-.01,.55),.42,.1)
        launcher(M,(sx*.45,.16,-.1),2)
        sqdrive(M,(sx*.15,0,-.85),.18)
    box(M,(0,-.27,-.15),(.42,.12,.6),DARK);box(M,(0,-.2,-.15),(.46,.03,.62),ACC,sh=.9)                          # ore bin
    for z in (-.4,.05):box(M,(0,.27,z),(.24,.03,.12),ACC,sh=.9)
    stacks(M,(0,.24,-.5),2);lights(M,[(.12,-.05,.62),(-.12,-.05,.62)])
    return finish(M,2.0)
def laser(M,base,length=.35,r=.07):
    # a mining laser: a barrel on a mount block, a collar and a glowing lens at the muzzle, facing +z
    b=np.array(base,float);box(M,tuple(b+[0,0,-.05]),(r*2.6,r*2.4,.18),DARK)
    tube(M,[b,b+[0,0,length]],[r,r*.85],MID,1.0,8,cap0=False,cap1=False);ring(M,tuple(b+[0,0,length*.5]),r*1.05,r*.16,ACC,seg=12,sides=4)
    lens_head(M,tuple(b+[0,0,length]),r*.95)
def gouge():     # medium miner: a broad hex hull with three mining lasers across its prow, ore bins on the flanks
    M=Mesh(62)
    loft(M,[(-1.0,HEX(.42,.3)),(-.4,HEX(.48,.34)),(.25,HEX(.46,.32)),(.55,HEX(.4,.28,-.02)),(.7,HEX(.34,.22,-.03))],hex_role)
    plate(M,[(-.1,.33,.35),(.1,.33,.35),(.1,.36,.05),(-.1,.36,.05)],.025,GLASS)
    box(M,(0,-.02,.72),(.95,.2,.14),DARK);box(M,(0,.09,.72),(.97,.03,.15),ACC,sh=.9)                              # laser mount across the prow
    for x in (-.32,0,.32):laser(M,(x,-.02,.8))                                                                       # three mining lasers
    for sx in (1,-1):
        box(M,(sx*.62,-.02,-.35),(.26,.42,.95),DARK,taper=(.92,.92));box(M,(sx*.62,.2,-.35),(.28,.04,.97),ACC,sh=.9)   # ore bins on the flanks
        for dy in (.12,-.12):sqdrive(M,(sx*.24,dy,-1.1),.18)
        launcher(M,(sx*.3,.34,.3),2)
    for z in (-.55,-.1):box(M,(0,.35,z),(.3,.03,.13),ACC,sh=.9)
    stacks(M,(0,.32,-.75),3);lights(M,[(.25,.3,.48),(-.25,.3,.48)])
    return finish(M,2.6)
def sledge():    # heavy miner: a low heavy crawler with four mining lasers across its prow, a conveyor spine and a big rear hopper
    M=Mesh(63)
    loft(M,[(-1.3,HEX(.6,.32)),(-.6,HEX(.66,.36)),(.55,HEX(.62,.34)),(.8,HEX(.5,.26,-.02))],hex_role)               # low wide hull
    box(M,(0,-.02,.88),(1.5,.28,.2),DARK);box(M,(0,.13,.88),(1.52,.03,.21),ACC,sh=.9)                              # laser mount across the prow
    for x in (-.54,-.18,.18,.54):laser(M,(x,-.02,.98),.42,.085)                                                      # four mining lasers
    for sx in (1,-1):
        box(M,(sx*.68,-.12,-.3),(.12,.3,1.6),DARK)                                                                 # skids
        for dy in (.12,-.12):sqdrive(M,(sx*.35,dy,-1.45),.22)
        lights(M,[(sx*.6,.3,.82)])
    box(M,(0,.38,.1),(.36,.08,1.2),DARK);[box(M,(0,.43,z),(.4,.03,.06),ACC,sh=.9) for z in np.linspace(-.4,.6,6)]   # conveyor spine
    box(M,(0,.55,-.85),(.95,.5,.75),MID,taper=(1.1,1.0));box(M,(0,.81,-.85),(1.0,.04,.78),ACC,sh=.9)               # rear ore hopper
    plate(M,[(-.11,.36,.65),(.11,.36,.65),(.11,.4,.35),(-.11,.4,.35)],.025,GLASS)
    stacks(M,(0,.82,-1.15),3,.22,.32)
    return finish(M,3.2)
def runner():    # light hauler: an armoured courier wedge: a chisel prow widening into a boxy cargo body, cargo doors on top, side skirts
    M=Mesh(64)
    chis=lambda w,h,dy=0:[(w,dy),(w*.8,h+dy),(-w*.8,h+dy),(-w,dy),(-w*.7,-h*.7+dy),(w*.7,-h*.7+dy)]
    loft(M,[(-.85,HEX(.42,.32)),(-.2,HEX(.44,.34)),(.3,chis(.36,.27,-.02)),(.65,chis(.26,.16,-.05)),(.8,chis(.2,.08,-.07))],hex_role)   # the wedge
    plate(M,[(-.09,.26,.4),(.09,.26,.4),(.09,.3,.15),(-.09,.3,.15)],.025,GLASS)
    for z in (-.6,-.25):plate(M,[(-.34,.345,z+.14),(.34,.345,z+.14),(.34,.345,z-.14),(-.34,.345,z-.14)],.012,ACC,.9)   # cargo doors on top
    plate(M,[(0,.35,-.78),(0,.35,-.08),(0,.36,-.08),(0,.36,-.78)],.02,DARK)
    for sx in (1,-1):
        box(M,(sx*.45,-.08,-.35),(.06,.3,1.0),DARK)                                                                  # side skirts
        for z in (-.7,-.35,0):box(M,(sx*.47,.08,z),(.03,.12,.2),ACC,sh=.9)
        sqdrive(M,(sx*.2,.0,-.95),.22)
        plate(M,[(sx*.3,.3,-.45),(sx*.38,.5,-.7),(sx*.38,.5,-.8),(sx*.3,.3,-.8)],.05,ACC,.9)
    stacks(M,(0,.35,.05),2,.16,.22);lights(M,[(.15,-.06,.78),(-.15,-.06,.78)])
    return finish(M,2.0)
def bulwark():   # medium hauler: the Talon's pincer sponsons become two armoured holds; two smoothed cargo pods on the spine
    M=Mesh(65)
    loft(M,[(-.95,HEX(.24,.22)),(-.2,HEX(.28,.26)),(.55,HEX(.24,.22)),(.82,HEX(.22,.19,-.02))],hex_role)
    plate(M,[(-.08,.25,.7),(.08,.25,.7),(.08,.28,.4),(-.08,.28,.4)],.025,GLASS)
    for sx in (1,-1):
        loft(M,[(-1.0,HEX(.24,.3,0,sx*.62)),(-.2,HEX(.27,.33,0,sx*.65)),(.6,HEX(.24,.3,-.01,sx*.62)),(.85,HEX(.14,.18,-.02,sx*.55))],hex_role)   # armoured hold
        for z in (-.6,-.2,.2):box(M,(sx*.65,.34,z),(.4,.03,.28),ACC,sh=.9)
        plate(M,[(sx*.25,.0,.4),(sx*.42,.0,.4),(sx*.42,.0,-.6),(sx*.25,.0,-.6)],.08,DARK)
        for dy in (.12,-.12):sqdrive(M,(sx*.62,dy,-1.08),.2)
    oct=lambda w,h,dy:[(math.cos(a)*w,math.sin(a)*h+dy) for a in np.linspace(PI/8,2*PI+PI/8,8,endpoint=False)]
    for z in (-.55,-.05):                                                                                            # smoothed spine pods
        loft(M,[(z-.22,oct(.14,.1,.4)),(z-.16,oct(.22,.17,.4)),(z+.16,oct(.22,.17,.4)),(z+.22,oct(.14,.1,.4))],lambda i,j:((MID,1.0) if j in (1,2,3) else (MID,.9)))
        ring(M,(0,.4,z),.215,.012,ACC,seg=16,sides=4)
    stacks(M,(0,.27,-.85),2);lights(M,[(.1,-.04,.84),(-.1,-.04,.84)])
    return finish(M,2.6)
def rampart():   # heavy hauler: a long chisel-prowed hull of ribbed armoured hold segments, crenellated walls, four corner pods (Varkesh colours)
    M=Mesh(66)
    chis=lambda w,h,dy=0:[(w,dy),(w*.8,h+dy),(-w*.8,h+dy),(-w,dy),(-w*.7,-h*.7+dy),(w*.7,-h*.7+dy)]
    hull_role=lambda i,j:([MID,LIGHT,LIGHT,MID,DARK,DARK][j],[1,.95,1,1,.85,.9][j])
    loft(M,[(-1.5,HEX(.5,.4)),(.9,HEX(.5,.4)),(1.25,chis(.44,.32,-.02)),(1.45,chis(.36,.24,-.04))],hull_role)
    plate(M,[(-.12,.38,1.3),(.12,.38,1.3),(.12,.42,1.02),(-.12,.42,1.02)],.025,GLASS)
    for k,z in enumerate((-1.2,-.7,-.2,.3,.8)):
        loft(M,[(z-.08,HEX(.55,.45)),(z+.08,HEX(.55,.45))],(ACC,.95))                                             # armour ribs in Varkesh orange
        plate(M,[(-.25,.41,z+.4),(.25,.41,z+.4),(.25,.41,z+.12),(-.25,.41,z+.12)],.012,DARK,.95)
    for sx in (1,-1):
        for k in range(6):box(M,(sx*.42,.48,1.0-k*.45),(.1,.14,.2),LIGHT,sh=.95);box(M,(sx*.42,.56,1.0-k*.45),(.11,.02,.21),ACC,sh=.9)   # crenellations
        for sz in (1,-1):
            px,pz=sx*.78,(1.0 if sz>0 else -1.3)
            plate(M,[(sx*.45,.0,pz+.25),(px,.0,pz+.2),(px,.0,pz-.2),(sx*.45,.0,pz-.25)],.08,MID)
            box(M,(px,0,pz),(.26,.3,.5),LIGHT,sh=.95);box(M,(px,.16,pz),(.27,.03,.51),ACC,sh=.9)
            if sz>0:barrel(M,(px,.06,pz+.25),.4,.03)
            else:sqdrive(M,(px,0,pz-.35),.24)
    stacks(M,(0,.42,-1.3),4,.2,.35);lights(M,[(.25,0,1.45),(-.25,0,1.45)])
    return finish(M,3.4)
# ============================================================== OSTROVA
def glim():      # light miner: a spire cockpit with a crystal cargo hold either side, all in a halo; prongs holding a mining lens
    M=Mesh(71)
    loft(M,[(-.8,DIA(.07,.07)),(-.45,DIA(.18,.16)),(.2,DIA(.2,.18)),(.55,DIA(.12,.11)),(.68,DIA(.07,.06))],SP)      # spire cockpit
    M.blob((0,.17,.22),.09,GLASS,sub=2,squash=(.9,.7,1.8),noise=0)
    for sx in (1,-1):
        crystal(M,-.65,.35,.2,.24,sx*.36,0)                                                                         # crystal cargo hold, either side
        tube(M,[(sx*.12,0,-.15),(sx*.26,0,-.15)],[.03,.03],LIGHT,.9,5)
        loft(M,[(.3,DIA(.05,.06,sx*.18)),(.68,DIA(.04,.05,sx*.13)),(.82,DIA(.004,.004,sx*.1))],SP)                 # prongs
    ring(M,(0,0,-.15),.62,.045,ACC)
    for k in range(3):a=PI/2+k*2*PI/3;M.blob((math.cos(a)*.62,math.sin(a)*.62,-.15),.06,GLASS,sub=1,noise=0)
    lens_head(M,(0,-.02,.7),.09)
    for k in range(3):a=PI/2+k*2*PI/3;plate(M,[(math.cos(a)*.12,math.sin(a)*.12,-.55),(math.cos(a)*.5,math.sin(a)*.5,-.82),(math.cos(a)*.45,math.sin(a)*.45,-.9),(math.cos(a)*.1,math.sin(a)*.1,-.85)],.025,MID)
    launcher(M,(0,-.2,.0),2,ACC)
    M.vent((0,0,-.82),.06)
    lights(M,[(.1,-.1,.6),(-.1,-.1,.6)])
    return finish(M,2.0)
def lumen():     # medium miner: a central spire cockpit with crystal holds on three sides, inside two rings crossed in an X, lenses at the tips
    M=Mesh(72)
    loft(M,[(-.85,DIA(.07,.07)),(-.5,DIA(.17,.16)),(.3,DIA(.18,.17)),(.7,DIA(.11,.1)),(.82,DIA(.06,.05))],SP)        # central spire cockpit
    M.blob((0,.17,.35),.09,GLASS,sub=2,squash=(.9,.7,1.8),noise=0)
    for k in range(3):
        a=-PI/2+k*2*PI/3;dx,dy=math.cos(a)*.36,math.sin(a)*.36
        crystal(M,-.75,.4,.2,.2,dx,dy)                                                                              # crystal holds on three sides
        tube(M,[(dx*.35,dy*.35,-.15),(dx*.7,dy*.7,-.15)],[.03,.03],LIGHT,.9,5)
    for th in (PI/4,-PI/4):
        u=np.array([math.sin(th),math.cos(th),0.])
        pts=[np.array([0,0,-.15])+u*math.cos(a)*.78+np.array([0,0,math.sin(a)*.78]) for a in np.linspace(0,2*PI,37)]
        M.tube(pts,[.045]*len(pts),6,lambda i,j,n,p:(ACC,1.0),cap0=False,cap1=False)                                # crossed rings
        for sg in (1,-1):
            tip=np.array([0,0,-.15])+u*sg*.78
            lens_head(M,tuple(tip+[0,0,.05]),.08)
    for k in range(3):a=PI/2+k*2*PI/3;plate(M,[(math.cos(a)*.15,math.sin(a)*.15,-.75),(math.cos(a)*.5,math.sin(a)*.5,-1.0),(math.cos(a)*.45,math.sin(a)*.45,-1.08),(math.cos(a)*.12,math.sin(a)*.12,-1.02)],.025,MID)
    M.vent((0,0,-.87),.07)
    lights(M,[(.1,-.08,.72),(-.1,-.08,.72)])
    return finish(M,2.6)
def delve():     # heavy miner: four crystal ore pods round a great drill spire, all inside one big halo, a lens ring at the prow
    M=Mesh(73)
    loft(M,[(-1.25,DIA(.1,.1)),(-.8,DIA(.22,.22)),(.6,DIA(.2,.2)),(.95,DIA(.12,.12))],SP)                          # core spire
    tube(M,[(0,0,.95),(0,0,1.15)],[.14,.12],LIGHT,1.0,8);drill(M,(0,0,1.15),.75,.14,MID)
    ring(M,(0,0,1.0),.42,.035,ACC,seg=24,sides=5)
    for k in range(6):a=k*PI/3;lens_head(M,(math.cos(a)*.42,math.sin(a)*.42,1.05),.06)
    for k in range(4):
        a=PI/4+k*PI/2;dx,dy=math.cos(a)*.55,math.sin(a)*.55
        crystal(M,-1.0,.55,.24,.24,dx,dy)                                                                            # crystal ore pods
        tube(M,[(dx*.35,dy*.35,-.2),(dx*.75,dy*.75,-.2)],[.03,.03],LIGHT,.9,5)
        plate(M,[(dx*1.2,dy*1.2,-.75),(dx*1.6,dy*1.6,-1.05),(dx*1.5,dy*1.5,-1.15),(dx*1.15,dy*1.15,-1.05)],.03,MID)
    ring(M,(0,0,-.2),.98,.05,ACC,seg=40,sides=6)
    M.blob((0,.24,.45),.1,GLASS,sub=2,squash=(.9,.7,1.8),noise=0)
    M.vent((0,0,-1.27),.09)
    lights(M,[(.22,.15,.95),(-.22,.15,.95)])
    return finish(M,3.2)
def drift():     # light hauler: a spire through a revolver of six cargo capsules on a halo
    M=Mesh(74)
    loft(M,[(-.8,DIA(.06,.06)),(-.4,DIA(.14,.13)),(.4,DIA(.14,.13)),(.75,DIA(.1,.09))],SP)
    ring(M,(0,0,-.15),.32,.03,ACC)
    for k in range(6):
        a=k*PI/3;cx,cy=math.cos(a)*.32,math.sin(a)*.32
        tube(M,[(cx,cy,-.55),(cx,cy,-.45),(cx,cy,.15),(cx,cy,.25)],[.03,.1,.1,.03],LIGHT if k%2 else MID,.95,8)
    M.blob((0,.15,.5),.07,GLASS,sub=2,squash=(.9,.7,1.8),noise=0)
    for k in range(3):a=PI/2+k*2*PI/3;plate(M,[(math.cos(a)*.1,math.sin(a)*.1,-.55),(math.cos(a)*.48,math.sin(a)*.48,-.78),(math.cos(a)*.44,math.sin(a)*.44,-.86),(math.cos(a)*.08,math.sin(a)*.08,-.82)],.02,MID)
    M.vent((0,0,-.82),.06)
    lights(M,[(.08,-.05,.75),(-.08,-.05,.75)])
    return finish(M,2.0)
def cairn():     # medium hauler: a spire threaded through three stacked faceted cargo blocks that taper forward to a point
    M=Mesh(75)
    loft(M,[(-1.05,DIA(.06,.06)),(-.8,DIA(.12,.12)),(.6,DIA(.11,.11)),(1.0,DIA(.05,.05)),(1.3,DIA(.004,.004))],SP)   # spire, drawn to a point
    for k,(z0,z1,w) in enumerate(((-.75,-.3,.52),(-.25,.2,.42),(.25,.65,.3))):
        loft(M,[(z0,HEX(w*.75,w*.65)),(z0+.08,HEX(w,w*.85)),(z1-.08,HEX(w*.88,w*.75)),(z1,HEX(w*.62,w*.52))],lambda i,j,k=k:((LIGHT if k%2 else MID),[1,.95,1,.9,.85,.9][j]))
        for sx in (1,-1):plate(M,[(sx*w*.98,0,z0+.12),(sx*w*.86,0,z1-.12),(sx*w*.7,w*.36,z1-.12),(sx*w*.8,w*.4,z0+.12)],.008,WIN,.85)
    loft(M,[(.65,HEX(.19,.16)),(.95,HEX(.06,.05))],(MID,.95))                                                        # the point
    for z,R in ((-.28,.55),(.22,.45)):ring(M,(0,0,z),R,.03,ACC,seg=28,sides=5)
    M.blob((0,.27,.5),.07,GLASS,sub=2,squash=(.9,.7,1.8),noise=0)
    for k in range(3):a=PI/2+k*2*PI/3;plate(M,[(math.cos(a)*.1,math.sin(a)*.1,-.8),(math.cos(a)*.6,math.sin(a)*.6,-1.0),(math.cos(a)*.55,math.sin(a)*.55,-1.08),(math.cos(a)*.08,math.sin(a)*.08,-1.05)],.02,MID)
    M.vent((0,0,-1.07),.07)
    lights(M,[(.08,-.06,.9),(-.08,-.06,.9)])
    return finish(M,2.6)
def monolith():  # heavy hauler: the ship is the monolith: a great square obelisk laid along its course, a pyramid prow, crystal seams,
                 # one halo at its waist on spokes, three spire drives astern
    M=Mesh(76)
    sq=lambda w,h,dy=0:[(w,-h+dy),(w,h+dy),(-w,h+dy),(-w,-h+dy)]
    loft(M,[(-1.3,sq(.42,.5)),(.85,sq(.36,.44)),(1.3,sq(.03,.03))],lambda i,j:([LIGHT,MID,LIGHT,DARK][j],[1,.95,.9,.85][j]))   # the obelisk with its pyramid prow
    for sx in (1,-1):
        for k in range(3):plate(M,[(sx*.4,-.38+k*.36,-1.15),(sx*.4,-.3+k*.36,-1.15),(sx*.36,-.26+k*.33,.8),(sx*.36,-.32+k*.33,.8)],.01,WIN,.85)   # crystal seams along the flanks
    for k in range(2):plate(M,[(-.3+k*.6-.04,.48,-1.1),(-.3+k*.6+.04,.48,-1.1),(-.3+k*.6+.04,.42,.75),(-.3+k*.6-.04,.42,.75)],.01,WIN,.85)
    plate(M,[(-.14,.45,.75),(.14,.45,.75),(.12,.36,1.0),(-.12,.36,1.0)],.02,GLASS)                                # bridge slit near the prow
    ring(M,(0,0,-.3),.95,.05,ACC,seg=40,sides=6)
    for k in range(4):
        a=PI/4+k*PI/2;ca,sa=math.cos(a),math.sin(a)
        tube(M,[(ca*.5,sa*.5,-.3),(ca*.92,sa*.92,-.3)],[.03,.03],LIGHT,.9,5,cap0=False,cap1=False)
        M.blob((ca*.95,sa*.95,-.3),.07,GLASS,sub=1,noise=0)
    for k in range(3):
        a=PI/2+k*2*PI/3;dx,dy=math.cos(a)*.3,math.sin(a)*.3
        loft(M,[(-1.75,DIA(.03,.03,dx,dy)),(-1.55,DIA(.1,.1,dx,dy)),(-1.25,DIA(.1,.1,dx,dy))],SP);M.vent((dx,dy,-1.77),.05)   # spire drives astern
        plate(M,[(dx*1.3,dy*1.3,-1.2),(dx*2.6,dy*2.6,-1.45),(dx*2.5,dy*2.5,-1.55),(dx*1.3,dy*1.3,-1.5)],.03,MID)
    lights(M,[(.22,-.3,.95),(-.22,-.3,.95)])
    return finish(M,3.3)
WORK=[('halcyon','Halcyon Accord',[('Wren','Light miner',wren),('Plover','Medium miner',plover),('Heron','Heavy miner',heron),('Tern','Light hauler',tern),('Albatross','Medium hauler',albatross),('Pelican','Heavy hauler',pelican)]),
      ('varkesh','Varkesh Dominion',[('Pick','Light miner',pick),('Gouge','Medium miner',gouge),('Sledge','Heavy miner',sledge),('Runner','Light hauler',runner),('Bulwark','Medium hauler',bulwark),('Rampart','Heavy hauler',rampart)]),
      ('ostrova','Ostrova Collective',[('Glim','Light miner',glim),('Lumen','Medium miner',lumen),('Delve','Heavy miner',delve),('Drift','Light hauler',drift),('Cairn','Medium hauler',cairn),('Monolith','Heavy hauler',monolith)])]
