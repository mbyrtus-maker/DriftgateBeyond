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
def plover():    # medium miner: the Osprey's twin booms become fat ore hoppers with drills; a cockpit pod between; tail spar
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
    plate(M,[(-.72,.44,-1.1),(.72,.44,-1.1),(.72,.44,-1.2),(-.72,.44,-1.2)],.03,ACC)
    for sx in (1,-1):[ring(M,(sx*.72,0,z),.33,.016,ACC,seg=22,sides=4) for z in (-.75,.5)]
    lights(M,[(.15,-.04,.82),(-.15,-.04,.82)])
    return finish(M,2.6)
def heron():     # heavy miner: a broad flattened lens hull with two stacked hoppers, a crane neck with a big lens, four drives
    M=Mesh(53)
    loft(M,[(-1.2,LENS(.4,.22)),(-.7,LENS(.75,.32)),(.2,LENS(.8,.34)),(.75,LENS(.5,.26)),(1.0,LENS(.22,.14,.04))],lens_role)   # broad hull
    for x in (-.35,.35):loft(M,[(-.9,[(a+x,b+.28) for a,b in LENS(.12,.08)]),(-.6,[(a+x,b+.3) for a,b in LENS(.26,.2)]),(.3,[(a+x,b+.3) for a,b in LENS(.26,.2)]),(.55,[(a+x,b+.28) for a,b in LENS(.1,.07)])],lens_role)   # stacked hoppers
    for x in (-.35,.35):
        for z in (-.4,-.05,.25):ring(M,(x,.3,z),.265,.015,ACC,seg=18,sides=4)
    M.blob((0,.36,.72),.16,GLASS,sub=2,squash=(1.2,.7,1.5),noise=0)
    tube(M,[(0,.2,.9),(0,.42,1.25),(0,.4,1.6)],[.09,.08,.08],LIGHT,1.0,8)                                        # crane neck
    lens_head(M,(0,.4,1.62),.16)
    for sx in (1,-1):
        drill(M,(sx*.55,-.08,.9),.55,.12)
        plate(M,[(sx*.75,.0,-.1),(sx*1.25,.02,-.55),(sx*1.2,.02,-.75),(sx*.7,.0,-.7)],.06,LIGHT)
        box(M,(sx*1.15,-.04,-.6),(.18,.14,.3),MID);M.blob((sx*1.15,.08,-.6),.05,WIN,sub=1,noise=0)                # drone bays
        plate(M,[(sx*.55,.2,-.85),(sx*.65,.48,-1.12),(sx*.65,.48,-1.22),(sx*.55,.2,-1.2)],.035,ACC,.95)
        launcher(M,(sx*.6,-.3,.4),3)
        for dx in (.2,.5):M.vent((sx*dx,0,-1.22),.11)
    lights(M,[(.4,.0,1.0),(-.4,.0,1.0),(0,.18,1.02)])
    return finish(M,3.2)
def tern():      # light hauler: a short lens hull riding on a fat belly cargo pod, a forked tail and a glass canopy
    M=Mesh(54)
    loft(M,[(-.8,LENS(.16,.13)),(-.4,LENS(.24,.2)),(.3,LENS(.22,.19)),(.65,LENS(.17,.15,-.01))],lens_role)
    M.blob((0,.18,.35),.12,GLASS,sub=2,squash=(.9,.75,2.0),noise=0)
    loft(M,[(-.6,LENS(.14,.12,-.3)),(-.35,LENS(.3,.24,-.34)),(.25,LENS(.3,.24,-.34)),(.5,LENS(.12,.1,-.3))],lens_role)  # belly cargo pod
    for z in (-.2,.1):ring(M,(0,-.34,z),.3,.016,ACC,seg=18,sides=4)
    for sx in (1,-1):
        plate(M,[(sx*.08,.05,-.6),(sx*.36,.08,-.92),(sx*.28,.08,-.92),(sx*.05,.05,-.75)],.03,ACC)                    # forked tail
        plate(M,[(sx*.2,.0,.1),(sx*.48,.02,-.12),(sx*.45,.02,-.25),(sx*.2,.0,-.22)],.03,LIGHT)
        M.blob((sx*.47,.02,-.19),.04,WIN,sub=1,noise=0)
    M.vent((0,0,-.82),.1)
    ribs(M,(-.45,.0),.25);lights(M,[(.1,-.04,.67),(-.1,-.04,.67)])
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
def pelican():   # heavy hauler: a huge bulbous cargo pouch hull between the Osprey's twin engine booms, a high stabiliser
    M=Mesh(56)
    loft(M,[(-1.25,LENS(.3,.24)),(-.8,LENS(.6,.5,-.05)),(.2,LENS(.7,.62,-.12)),(.85,LENS(.5,.45,-.12)),(1.25,LENS(.15,.12,.05))],lens_role)   # the pouch hull
    for z in (-.4,.0,.4):ring(M,(0,-.12,z),.7 if z<.3 else .62,.02,ACC,seg=28,sides=4)
    M.blob((0,.45,.85),.16,GLASS,sub=2,squash=(1,.7,1.6),noise=0)
    for sx in (1,-1):
        tube(M,[(sx*.95,.15,.45),(sx*.95,.15,-1.35),(sx*.95,.15,-1.5)],[.1,.16,.15],MID,.95,10,cap1=False);M.vent((sx*.95,.15,-1.5),.13)   # engine booms
        plate(M,[(sx*.6,.2,.2),(sx*.95,.2,.15),(sx*.95,.2,-.55),(sx*.6,.2,-.6)],.06,LIGHT)
        plate(M,[(sx*.95,.25,-1.05),(sx*.95,.62,-1.3),(sx*.95,.62,-1.42),(sx*.95,.25,-1.4)],.035,ACC,.95)
        M.blob((sx*.95,.32,.3),.06,WIN,sub=1,noise=0)
        hatch(M,(sx*.3,.5,-.1),.3,.6)
    plate(M,[(-.95,.6,-1.3),(.95,.6,-1.3),(.95,.6,-1.42),(-.95,.6,-1.42)],.035,ACC)
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
def gouge():     # medium miner: a broad hex hull, an armoured scoop between pincer sponsons, lenses on the scoop lip
    M=Mesh(62)
    loft(M,[(-1.0,HEX(.4,.28)),(-.4,HEX(.46,.32)),(.2,HEX(.42,.3)),(.45,HEX(.3,.22,-.02))],hex_role)
    plate(M,[(-.1,.31,.35),(.1,.31,.35),(.1,.34,.05),(-.1,.34,.05)],.025,GLASS)
    for sx in (1,-1):
        loft(M,[(-.9,HEX(.15,.18,0,sx*.68)),(-.1,HEX(.17,.2,0,sx*.7)),(.8,HEX(.14,.17,-.01,sx*.66)),(1.1,HEX(.08,.1,-.02,sx*.58))],hex_role)   # pincer sponsons
        plate(M,[(sx*.6,.12,1.0),(sx*.66,-.12,1.0),(sx*.46,-.08,1.22),(sx*.44,.06,1.2)],.06,ACC)
        plate(M,[(sx*.53,-.22,.45),(sx*.53,-.22,1.05),(sx*.53,.12,1.0),(sx*.53,.16,.45)],.05,DARK)                  # scoop wall
        for dy in (.1,-.1):sqdrive(M,(sx*.22,dy,-1.1),.18)
        launcher(M,(sx*.7,.2,.3),3)
        for k,z in enumerate((.4,-.05,-.5)):box(M,(sx*.86,.05,z),(.05,.24,.3),MID,taper=(.9,.85),sh=.96+.03*k)
    plate(M,[(-.53,-.22,.45),(.53,-.22,.45),(.5,-.24,1.1),(-.5,-.24,1.1)],.06,DARK)                                # scoop floor
    box(M,(0,-.23,1.12),(1.0,.05,.06),ACC)
    for x in (-.3,0,.3):lens_head(M,(x,-.18,1.14),.06)
    stacks(M,(0,.32,-.75),3);lights(M,[(.25,.3,.42),(-.25,.3,.42)])
    return finish(M,2.6)
def sledge():    # heavy miner: a hammerhead: a broad charge-battery bar across the prow of a thick armoured hull, ore bins, a great drill
    M=Mesh(63)
    loft(M,[(-1.25,HEX(.42,.36)),(-.5,HEX(.5,.42)),(.45,HEX(.46,.4)),(.7,HEX(.34,.3,-.02))],hex_role)              # thick hull
    plate(M,[(-.12,.41,.4),(.12,.41,.4),(.12,.45,.1),(-.12,.45,.1)],.025,GLASS)
    box(M,(0,.05,.9),(2.2,.5,.42),MID,taper=(.96,.9));box(M,(0,.32,.9),(2.24,.05,.44),ACC,sh=.9)                 # the hammerhead bar
    for x in np.linspace(-.9,.9,7):
        for y in (.13,-.05):tube(M,[(x,y,1.1),(x,y,1.22)],[.055,.055],DARK,.9,6)                                  # charge battery
    for sx in (1,-1):
        box(M,(sx*1.12,.05,.9),(.14,.6,.5),DARK)
        lens_head(M,(sx*1.0,-.24,1.12),.08)
        box(M,(sx*.62,-.05,-.35),(.32,.5,1.1),DARK,taper=(.9,.9));box(M,(sx*.62,.22,-.35),(.34,.04,1.12),ACC,sh=.9)  # ore bins
        for dy in (.15,-.15):sqdrive(M,(sx*.24,dy,-1.38),.24)
        plate(M,[(sx*.3,.38,-.6),(sx*.42,.7,-.95),(sx*.42,.7,-1.08),(sx*.3,.38,-1.08)],.07,ACC,.9)
    drill(M,(0,-.3,1.0),.75,.17)
    for z in (-.8,-.3,.2):box(M,(0,.43,z),(.38,.04,.16),ACC,sh=.9)
    stacks(M,(0,.42,-1.0),3,.2,.38);lights(M,[(.5,.32,1.1),(-.5,.32,1.1)])
    return finish(M,3.2)
def runner():    # light hauler: a Fang-like hex cab clamped onto one big armoured container, square drives
    M=Mesh(64)
    loft(M,[(.1,HEX(.24,.2)),(.45,HEX(.26,.21)),(.72,HEX(.22,.18,-.02))],hex_role)
    plate(M,[(-.07,.22,.6),(.07,.22,.6),(.07,.25,.32),(-.07,.25,.32)],.025,GLASS)
    box(M,(0,.02,-.45),(.62,.5,1.0),MID);box(M,(0,.29,-.45),(.66,.04,1.02),ACC,sh=.9)                          # the container
    for z in (-.85,-.45,-.05):box(M,(0,.02,z),(.66,.54,.05),DARK)
    for sx in (1,-1):
        box(M,(sx*.34,.02,-.45),(.05,.56,1.06),DARK)                                                                 # clamps
        sqdrive(M,(sx*.18,0,-1.05),.18)
        plate(M,[(sx*.22,.25,.05),(sx*.3,.45,-.2),(sx*.3,.45,-.3),(sx*.22,.25,-.3)],.05,ACC,.9)
    stacks(M,(0,.24,.2),2,.14,.25);lights(M,[(.12,-.04,.73),(-.12,-.04,.73)])
    return finish(M,2.0)
def bulwark():   # medium hauler: the Talon's pincer sponsons become two armoured holds; containers on the spine; guns
    M=Mesh(65)
    loft(M,[(-.95,HEX(.24,.22)),(-.2,HEX(.28,.26)),(.55,HEX(.24,.22)),(.82,HEX(.22,.19,-.02))],hex_role)
    plate(M,[(-.08,.25,.7),(.08,.25,.7),(.08,.28,.4),(-.08,.28,.4)],.025,GLASS)
    for sx in (1,-1):
        loft(M,[(-1.0,HEX(.24,.3,0,sx*.62)),(-.2,HEX(.27,.33,0,sx*.65)),(.6,HEX(.24,.3,-.01,sx*.62)),(.85,HEX(.14,.18,-.02,sx*.55))],hex_role)   # armoured hold
        for z in (-.6,-.2,.2):box(M,(sx*.65,.34,z),(.4,.03,.28),ACC,sh=.9)
        plate(M,[(sx*.25,.0,.4),(sx*.42,.0,.4),(sx*.42,.0,-.6),(sx*.25,.0,-.6)],.08,DARK)
        for dy in (.12,-.12):sqdrive(M,(sx*.62,dy,-1.08),.2)
    for z in (-.55,-.05):box(M,(0,.4,z),(.4,.3,.42),MID);box(M,(0,.56,z),(.42,.03,.44),ACC,sh=.9)                 # spine containers
    stacks(M,(0,.27,-.85),2);lights(M,[(.1,-.04,.84),(-.1,-.04,.84)])
    return finish(M,2.6)
def rampart():   # heavy hauler: a long chisel-prowed hull of ribbed armoured hold segments, crenellated walls, four corner pods
    M=Mesh(66)
    chis=lambda w,h,dy=0:[(w,dy),(w*.8,h+dy),(-w*.8,h+dy),(-w,dy),(-w*.7,-h*.7+dy),(w*.7,-h*.7+dy)]
    loft(M,[(-1.5,HEX(.5,.4)),(.9,HEX(.5,.4)),(1.25,chis(.44,.32,-.02)),(1.45,chis(.36,.24,-.04))],hex_role)
    plate(M,[(-.12,.38,1.3),(.12,.38,1.3),(.12,.42,1.02),(-.12,.42,1.02)],.025,GLASS)
    for k,z in enumerate((-1.2,-.7,-.2,.3,.8)):
        loft(M,[(z-.12,HEX(.56,.46)),(z+.12,HEX(.56,.46))],(DARK,.9))                                             # armour ribs
        hatch(M,(0,.41,z+.25),.5,.3)
    for sx in (1,-1):
        for k in range(6):box(M,(sx*.42,.48,1.0-k*.45),(.1,.14,.2),MID,sh=1.05)                                      # crenellations
        for sz in (1,-1):
            px,pz=sx*.78,(1.0 if sz>0 else -1.3)
            plate(M,[(sx*.45,.0,pz+.25),(px,.0,pz+.2),(px,.0,pz-.2),(sx*.45,.0,pz-.25)],.08,DARK)
            box(M,(px,0,pz),(.26,.3,.5),MID)
            if sz>0:barrel(M,(px,.06,pz+.25),.4,.03)
            else:sqdrive(M,(px,0,pz-.35),.24)
    stacks(M,(0,.42,-1.3),4,.2,.35);lights(M,[(.25,0,1.45),(-.25,0,1.45)])
    return finish(M,3.4)

# ============================================================== OSTROVA
def glim():      # light miner: a fat crystal ore hopper in a halo, a small spire cab on top, prongs holding a mining lens
    M=Mesh(71)
    crystal(M,-.75,.45,.36,.32)                                                                                     # the ore hopper
    loft(M,[(-.55,DIA(.06,.05,0,.3)),(-.2,DIA(.13,.1,0,.34)),(.35,DIA(.1,.08,0,.32)),(.6,DIA(.07,.06,0,.29))],SP)  # spire cab on top
    M.blob((0,.42,.25),.08,GLASS,sub=2,squash=(.9,.7,1.8),noise=0)
    ring(M,(0,0,-.15),.48,.045,ACC)
    for k in range(3):a=PI/2+k*2*PI/3;M.blob((math.cos(a)*.48,math.sin(a)*.48,-.15),.06,GLASS,sub=1,noise=0)
    for sx in (1,-1):loft(M,[(.2,DIA(.05,.06,sx*.2)),(.65,DIA(.04,.05,sx*.15)),(.8,DIA(.004,.004,sx*.12))],SP)       # prongs
    lens_head(M,(0,0,.62),.1)
    for k in range(3):a=PI/2+k*2*PI/3;plate(M,[(math.cos(a)*.25,math.sin(a)*.25,-.55),(math.cos(a)*.55,math.sin(a)*.55,-.8),(math.cos(a)*.5,math.sin(a)*.5,-.88),(math.cos(a)*.2,math.sin(a)*.2,-.82)],.025,MID)
    launcher(M,(0,-.34,.0),2,ACC)
    for k in range(2):M.vent(((-1)**k*.12,0,-.8),.06)
    lights(M,[(.1,-.1,.55),(-.1,-.1,.55)])
    return finish(M,2.0)
def lumen():     # medium miner: twin crystal ore hoppers side by side, joined at the front by a crescent carrying three mining lenses
    M=Mesh(72)
    for sx in (1,-1):
        crystal(M,-1.0,.5,.3,.3,sx*.5,0)                                                                            # crystal hoppers
        plate(M,[(sx*.5,.3,-.8),(sx*.5,.62,-1.05),(sx*.5,.6,-1.15),(sx*.5,.28,-1.1)],.025,MID)
        M.vent((sx*.5,0,-.98),.07)
    loft(M,[(-.6,DIA(.08,.08)),(-.2,DIA(.16,.14)),(.5,DIA(.13,.12)),(.8,DIA(.09,.08))],SP)                        # central spire cab
    M.blob((0,.17,.3),.08,GLASS,sub=2,squash=(.9,.7,1.8),noise=0)
    pts=[np.array([math.cos(a)*.75,0,.15+math.sin(a)*.55]) for a in np.linspace(.15,PI-.15,21)]
    M.tube(pts,[.05]*len(pts),6,lambda i,j,n,p:(ACC,1.0),cap0=True,cap1=True)                                     # the crescent across the front
    for k in (3,10,17):lens_head(M,tuple(pts[k]+[0,0,.04]),.08)
    for sx in (1,-1):tube(M,[(sx*.12,0,-.3),(sx*.42,0,-.3)],[.03,.03],LIGHT,.9,5);tube(M,[(sx*.12,0,.2),(sx*.42,0,.2)],[.03,.03],LIGHT,.9,5)
    lights(M,[(.12,-.06,.8),(-.12,-.06,.8)])
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
def cairn():     # medium hauler: a spire threaded through three stacked faceted cargo blocks, halos between them
    M=Mesh(75)
    loft(M,[(-1.05,DIA(.06,.06)),(-.8,DIA(.12,.12)),(.75,DIA(.12,.12)),(1.0,DIA(.09,.09))],SP)
    for k,(z0,z1,w) in enumerate(((-.75,-.3,.42),(-.25,.2,.5),(.25,.65,.38))):
        loft(M,[(z0,HEX(w*.7,w*.6)),(z0+.08,HEX(w,w*.85)),(z1-.08,HEX(w,w*.85)),(z1,HEX(w*.7,w*.6))],lambda i,j,k=k:((LIGHT if k%2 else MID),[1,.95,1,.9,.85,.9][j]))
        plate(M,[(w*.98,0,z0+.12),(w*.98,0,z1-.12),(w*.8,w*.4,z1-.12),(w*.8,w*.4,z0+.12)],.008,WIN,.85)
        plate(M,[(-w*.98,0,z0+.12),(-w*.98,0,z1-.12),(-w*.8,w*.4,z1-.12),(-w*.8,w*.4,z0+.12)],.008,WIN,.85)
    for z,R in ((-.28,.52),(.23,.5)):ring(M,(0,0,z),R,.03,ACC,seg=28,sides=5)
    M.blob((0,.36,.5),.08,GLASS,sub=2,squash=(.9,.7,1.8),noise=0)
    for k in range(3):a=PI/2+k*2*PI/3;plate(M,[(math.cos(a)*.1,math.sin(a)*.1,-.8),(math.cos(a)*.6,math.sin(a)*.6,-1.0),(math.cos(a)*.55,math.sin(a)*.55,-1.08),(math.cos(a)*.08,math.sin(a)*.08,-1.05)],.02,MID)
    M.vent((0,0,-1.07),.07)
    lights(M,[(.08,-.05,1.0),(-.08,-.05,1.0)])
    return finish(M,2.6)
def monolith():  # heavy hauler: a tall crystal-veined slab over a spire keel, the Vigil's two crossed halos round it, fins
    M=Mesh(76)
    box(M,(0,.35,-.1),(.6,1.3,2.2),MID,taper=(.8,.7))                                                             # the slab
    loft(M,[(1.0,[(-.24,-.12),(.24,-.12),(.24,.82),(-.24,.82)]),(1.35,[(-.03,.2),(.03,.2),(.03,.35),(-.03,.35)])],(LIGHT,1.0))
    for sx in (1,-1):
        for k in range(4):plate(M,[(sx*.31,-.15+k*.24,.8-k*.15),(sx*.31,.05+k*.24,.8-k*.15),(sx*.31,.02+k*.24,-.9+k*.1),(sx*.31,-.18+k*.24,-.9+k*.1)],.01,WIN,.85)   # crystal veins
    loft(M,[(-1.4,DIA(.06,.06,0,-.45)),(-1.0,DIA(.16,.14,0,-.45)),(.9,DIA(.14,.12,0,-.45)),(1.2,DIA(.08,.07,0,-.45))],SP)   # spire keel
    for th in (PI/4,-PI/4):
        u=np.array([math.sin(th),math.cos(th),0.])
        pts=[np.array([0,.2,-.2])+u*math.cos(a)*1.05+np.array([0,0,math.sin(a)*1.05]) for a in np.linspace(0,2*PI,37)]
        M.tube(pts,[.045]*len(pts),6,lambda i,j,n,p:(ACC,1.0),cap0=False,cap1=False)
        for sg in (1,-1):M.blob(tuple(np.array([0,.2,-.2])+u*sg*1.05),.07,GLASS,sub=1,noise=0)
    for sx in (1,-1):plate(M,[(sx*.3,-.2,-.9),(sx*.85,-.35,-1.25),(sx*.8,-.35,-1.38),(sx*.3,-.2,-1.3)],.03,MID)
    M.blob((0,1.05,.75),.1,GLASS,sub=2,squash=(.8,.6,1.6),noise=0)
    for dy in (.2,-.2):M.vent((0,dy,-1.22),.09)
    lights(M,[(.2,-.45,1.2),(-.2,-.45,1.2)])
    return finish(M,3.3)

WORK=[('halcyon','Halcyon Accord',[('Wren','Light miner',wren),('Plover','Medium miner',plover),('Heron','Heavy miner',heron),('Tern','Light hauler',tern),('Albatross','Medium hauler',albatross),('Pelican','Heavy hauler',pelican)]),
      ('varkesh','Varkesh Dominion',[('Pick','Light miner',pick),('Gouge','Medium miner',gouge),('Sledge','Heavy miner',sledge),('Runner','Light hauler',runner),('Bulwark','Medium hauler',bulwark),('Rampart','Heavy hauler',rampart)]),
      ('ostrova','Ostrova Collective',[('Glim','Light miner',glim),('Lumen','Medium miner',lumen),('Delve','Heavy miner',delve),('Drift','Light hauler',drift),('Cairn','Medium hauler',cairn),('Monolith','Heavy hauler',monolith)])]
