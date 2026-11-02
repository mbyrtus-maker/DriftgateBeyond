# Driftgate Beyond: capital ships, an escort and a carrier per faction (preview, not in the model pack yet).
# Driftgate 1's two capitals set the working parts every design must keep (see DESIGN_NOTES "Capital ship models"):
#   escort  - a torpedo destroyer: forward torpedo tubes, point-defence turrets on the flanks (3 a side), a bridge, a ventral
#             assault bay, a main drive and auxiliaries, hull berths for docking, a shield generator
#   carrier - a flight deck players land on from above (spots fore and aft), launch mouths at the bow, point-defence sponsons,
#             a bridge tower, a shield generator, several drives
# Sub-targets in the game: point defence, engines, shield generator, torpedo bays, launch bay. Each faction builds these its own way.
import math
import numpy as np
from beyond_hulls import Mesh,LIGHT,MID,DARK,ACC,GLASS,GLOW,WIN,loft,box,plate,barrel,ring,LENS,HEX,DIA,lens_role,hex_role
from beyond_work import finish,tube,abox,crystal,lights,stacks,SP,STAR
from beyond_recon import turret,dish,torpedo,SMH,smh_role
PI=math.pi

def pd(M,c,r=.07,role=MID,up=True):
    # a point-defence turret: a base, a dome and twin barrels pointing forward
    c=np.array(c,float);s=1 if up else -1
    tube(M,[c,c+[0,s*r*.5,0]],[r*1.2,r*1.1],DARK,.9,8);M.blob(tuple(c+[0,s*r*.7,0]),r,role,sub=1,squash=(1,.7,1),noise=0)
    for sx in (1,-1):tube(M,[c+[sx*r*.35,s*r*.8,r*.3],c+[sx*r*.35,s*r*.8,r*1.9]],[.012,.011],DARK,1.0,5)
def spots(M,pts,r=.12,y=0):
    # deck landing spots: an accent ring with a cross
    for x,z in pts:
        ring(M,(x,y+.01,z),r,.012,ACC,seg=16,sides=4,axis='y')
        plate(M,[(x-r*.7,y+.012,z-.012),(x+r*.7,y+.012,z-.012),(x+r*.7,y+.012,z+.012),(x-r*.7,y+.012,z+.012)],.004,ACC)
def mouth(M,c,w,h,d=.25):
    # a hangar launch mouth: a dark recess with a lit lip
    abox(M,(c[0],c[1],c[2]-d/2),(w,h,d),DARK,(1,1),.6);ring(M,tuple(c),max(w,h)*.55,.015,WIN,seg=4,sides=4)
def shieldgen(M,c,r=.14):
    c=np.array(c,float);M.blob(tuple(c),r,GLASS,sub=2,squash=(1,.75,1),noise=0);ring(M,tuple(c-[0,r*.2,0]),r*1.12,.018,WIN,seg=18,sides=4,axis='y')

# ============================================================== HALCYON
def shrike():    # escort: a long lens hull with a swept prow, twin torpedo tubes in the nose, smooth turret sponsons, a glass bridge,
                 # emitter nodes on swept fins, twin tails, three drives
    M=Mesh(111)
    loft(M,[(-2.0,LENS(.3,.24)),(-1.4,LENS(.42,.32)),(.4,LENS(.4,.3)),(1.3,LENS(.24,.2,-.02)),(1.9,LENS(.06,.06,-.04))],lens_role)
    for sx in (1,-1):
        tube(M,[(sx*.14,-.08,1.35),(sx*.14,-.08,1.75)],[.07,.065],DARK,.9,8,cap1=False);M.blob((sx*.14,-.08,1.72),.05,ACC,sub=1,noise=0)   # torpedo tubes
        loft(M,[(-1.3,[(a+sx*.42,b) for a,b in LENS(.05,.05)]),(-1.0,[(a+sx*.42,b) for a,b in LENS(.12,.12)]),(.5,[(a+sx*.42,b) for a,b in LENS(.12,.12)]),(.8,[(a+sx*.42,b) for a,b in LENS(.04,.04)])],lens_role)   # turret sponson
        for z in (-.7,-.15,.4):pd(M,(sx*.45,.1,z),.065)
        plate(M,[(sx*.38,.05,-1.0),(sx*1.0,.02,-1.6),(sx*.96,.02,-1.78),(sx*.38,.05,-1.6)],.04,LIGHT)                # swept fins
        M.blob((sx*.98,.02,-1.69),.06,WIN,sub=1,noise=0)
        plate(M,[(sx*.15,.28,-1.2),(sx*.3,.68,-1.68),(sx*.3,.68,-1.8),(sx*.15,.26,-1.78)],.035,ACC,.95)
    loft(M,[(-.3,LENS(.14,.1,.32)),(.2,LENS(.17,.13,.36)),(.55,LENS(.08,.06,.32))],lens_role);M.blob((0,.47,.25),.12,GLASS,sub=2,squash=(1.1,.6,1.7),noise=0)   # bridge
    shieldgen(M,(0,.36,-.75),.13)
    abox(M,(0,-.33,-.3),(.3,.1,.5),DARK,(.9,.9))                                                                       # ventral assault bay
    M.vent((0,0,-2.03),.2)
    for sx in (1,-1):M.vent((sx*.26,.0,-1.98),.11)
    lights(M,[(.2,-.12,1.7),(-.2,-.12,1.7)],.04)
    return finish(M,3.4,1.0)
def sovereign(): # carrier: a broad blended lens hull with a flat flight deck, twin hangar mouths in the bow, the Osprey's twin engine
                 # booms aft, a glass bridge tower, turret sponsons and a shield emitter dish
    M=Mesh(112)
    loft(M,[(-2.2,LENS(.7,.32)),(-1.5,LENS(1.1,.42)),(1.0,LENS(1.05,.42)),(1.9,LENS(.7,.32)),(2.3,LENS(.32,.18))],lens_role)   # broad hull
    plate(M,[(-.62,.44,2.05),(.62,.44,2.05),(.7,.44,-1.2),(-.7,.44,-1.2)],.03,MID,.95)                               # flight deck
    spots(M,[(-.3,1.35),(.3,1.35),(-.3,-.45),(.3,-.45)],.14,.46)
    for x in (-.32,.32):plate(M,[(x-.012,.465,1.9),(x+.012,.465,1.9),(x+.012,.465,-1.1),(x-.012,.465,-1.1)],.003,WIN,.9)
    for sx in (1,-1):mouth(M,(sx*.42,.05,2.28),.42,.26)                                                              # launch mouths
    for sx in (1,-1):
        loft(M,[(-1.6,[(a+sx*1.05,b) for a,b in LENS(.05,.05)]),(-1.3,[(a+sx*1.05,b) for a,b in LENS(.14,.14)]),(1.3,[(a+sx*1.05,b) for a,b in LENS(.14,.14)]),(1.6,[(a+sx*1.05,b) for a,b in LENS(.05,.05)])],lens_role)   # turret sponson
        for z in (-.9,-.1,.7):pd(M,(sx*1.1,.12,z),.07)
        tube(M,[(sx*1.15,-.05,-1.0),(sx*1.15,-.05,-2.5),(sx*1.15,-.05,-2.65)],[.16,.2,.19],MID,.95,12,cap1=False);M.vent((sx*1.15,-.05,-2.65),.16)   # engine booms
        plate(M,[(sx*1.15,.12,-1.9),(sx*1.15,.65,-2.35),(sx*1.15,.65,-2.48),(sx*1.15,.12,-2.45)],.04,ACC,.95)
        M.blob((sx*1.2,.15,-1.5),.07,WIN,sub=1,noise=0)
    plate(M,[(-1.15,.62,-2.35),(1.15,.62,-2.35),(1.15,.62,-2.48),(-1.15,.62,-2.48)],.04,ACC)
    loft(M,[(-1.75,LENS(.24,.2,.6)),(-1.3,LENS(.26,.24,.66)),(-.95,LENS(.12,.1,.62))],lens_role)                     # bridge tower aft of the deck
    M.blob((0,.88,-1.25),.15,GLASS,sub=2,squash=(1.2,.6,1.4),noise=0);dish(M,(0,1.0,-1.55),.14)
    shieldgen(M,(0,.5,-1.9),.18)
    for sx in (0,1,-1):M.vent((sx*.35,0,-2.25),.18)
    return finish(M,4.6,1.0)

# ============================================================== VARKESH
def vanguard():  # escort: a long armoured hex hull with a chisel prow, Talon-like torpedo sponsons forward, turret sponsons, a slit bridge,
                 # four square drives and stacks
    M=Mesh(121)
    chis=lambda w,h,dy=0:[(w,dy),(w*.8,h+dy),(-w*.8,h+dy),(-w,dy),(-w*.7,-h*.7+dy),(w*.7,-h*.7+dy)]
    loft(M,[(-2.0,HEX(.42,.32)),(-1.2,HEX(.48,.36)),(.6,HEX(.46,.34)),(1.3,chis(.36,.26,-.02)),(1.8,chis(.2,.1,-.06))],hex_role)
    for sx in (1,-1):
        loft(M,[(.0,HEX(.12,.12,0,sx*.55)),(1.3,HEX(.12,.12,-.01,sx*.55)),(1.65,HEX(.06,.06,-.02,sx*.46))],hex_role)   # torpedo sponson
        tube(M,[(sx*.55,0,1.3),(sx*.55,0,1.62)],[.06,.06],DARK,.85,8,cap1=False);M.blob((sx*.55,0,1.58),.045,ACC,sub=1,noise=0)
        abox(M,(sx*.55,.0,-.75),(.24,.3,1.5),MID,(.85,.85))                                                          # turret sponson
        for z in (-1.3,-.75,-.2):pd(M,(sx*.55,.15,z),.065,MID)
        for k in range(3):abox(M,(sx*.48,.26,.6-k*.5),(.06,.18,.32),MID,(.9,.85),.96)
        for dy in (.13,-.13):abox(M,(sx*.2,dy,-2.15),(.26,.24,.2),DARK,(1.1,1.1));M.vent((sx*.2,dy,-2.27),.1)
        plate(M,[(sx*.32,.35,-1.3),(sx*.42,.68,-1.7),(sx*.42,.68,-1.82),(sx*.32,.35,-1.82)],.07,ACC,.9)
    abox(M,(0,.44,.1),(.34,.16,.6),MID,(.85,.8));plate(M,[(-.12,.53,.38),(.12,.53,.38),(.12,.56,.12),(-.12,.56,.12)],.025,GLASS)   # slit bridge
    shieldgen(M,(0,.4,-.85),.13)
    abox(M,(0,-.36,-.4),(.36,.12,.6),DARK,(.9,.9))
    for z in (-1.5,-.6,.3):abox(M,(0,.37,z),(.36,.04,.14),ACC,(1,1),.9)
    stacks(M,(0,.37,-1.7),3,.2,.32)
    return finish(M,3.4,1.0)
def bastille():  # carrier: a massive slab fortress, a crenellated flight deck, hangar mouths in a blunt bow, turret sponsons,
                 # a stepped bridge tower aft, six square drives, armour ribs
    M=Mesh(122)
    loft(M,[(-2.3,HEX(1.0,.48)),(1.8,HEX(1.0,.48)),(2.25,HEX(.82,.38,-.04))],hex_role)                             # slab hull
    plate(M,[(-.75,.49,2.1),(.75,.49,2.1),(.75,.49,-1.2),(-.75,.49,-1.2)],.03,DARK,.95)                              # flight deck
    spots(M,[(-.35,1.4),(.35,1.4),(-.35,-.5),(.35,-.5)],.15,.5)
    for sx in (1,-1):
        for k in range(8):abox(M,(sx*.82,.56,1.95-k*.42),(.1,.14,.2),MID,(1,1),1.05)                                 # crenellated deck edge
        mouth(M,(sx*.45,.0,2.26),.48,.3)
        abox(M,(sx*1.05,-.05,.0),(.3,.42,3.4),MID,(.95,.95))                                                          # turret sponson
        for z in (-1.3,-.5,.3,1.1):pd(M,(sx*1.08,.17,z),.075,MID)
        for dy in (.22,-.1):
            for dx in (.3,.7):abox(M,(sx*dx,dy,-2.45),(.32,.28,.22),DARK,(1.1,1.1));M.vent((sx*dx,dy,-2.58),.12)
    for z in (-1.8,-.9,0,.9):loft(M,[(z-.06,HEX(1.04,.52)),(z+.06,HEX(1.04,.52))],(ACC,.95))                        # armour ribs
    for k,(z,w,h,y) in enumerate(((-1.7,.6,.3,.65),(-1.75,.42,.26,.92),(-1.8,.28,.2,1.14))):abox(M,(0,y,z),(w,h,.7-k*.12),MID,(.9,.85))   # stepped bridge tower
    plate(M,[(-.13,1.2,-1.55),(.13,1.2,-1.55),(.13,1.24,-1.75),(-.13,1.24,-1.75)],.02,GLASS)
    shieldgen(M,(0,.62,-2.15),.16)
    stacks(M,(0,1.25,-1.95),2,.18,.3)
    lights(M,[(.6,.3,2.3),(-.6,.3,2.3)],.045)
    return finish(M,4.6,1.0)

# ============================================================== OSTROVA
def lantern():   # escort: a long spire with a crystal core, the Vigil's prongs holding torpedo lances forward, a halo carrying the
                 # turrets, crystal fins, two tail fins at 45 degrees
    M=Mesh(131)
    loft(M,[(-2.0,DIA(.12,.12)),(-1.4,DIA(.32,.3)),(.7,DIA(.32,.3)),(1.4,DIA(.14,.13)),(1.7,DIA(.03,.03))],SP)
    crystal(M,-1.0,.5,.22,.22,0,.22)                                                                                 # crystal core on the back
    for sx in (1,-1):
        loft(M,[(.6,DIA(.07,.08,sx*.32)),(1.5,DIA(.06,.07,sx*.3)),(1.85,DIA(.006,.006,sx*.26))],SP)                  # prongs
        torpedo(M,(sx*.32,-.12,1.0),.75,.06,LIGHT)                                                                    # torpedo lances
        plate(M,[(sx*.2,-.05,.3),(sx*.62,-.1,.0),(sx*.6,-.1,-.3),(sx*.2,-.05,-.4)],.025,WIN,.85)                    # crystal fins
    ring(M,(0,0,-.55),.78,.05,ACC,seg=36,sides=6)                                                                    # the turret halo
    for k in range(6):
        a=k*PI/3;x,y=math.cos(a)*.78,math.sin(a)*.78
        pd(M,(x,y,-.55),.065,ACC,up=y>=-.01) if abs(y)>.3 else M.blob((x,y,-.55),.07,GLASS,sub=1,noise=0)
    for k in range(3):a=PI/2+k*2*PI/3;tube(M,[(math.cos(a)*.25,math.sin(a)*.25,-.55),(math.cos(a)*.72,math.sin(a)*.72,-.55)],[.03,.03],LIGHT,.9,5)
    for a in (PI/4,3*PI/4):
        ca,sa=math.cos(a),math.sin(a);plate(M,[(ca*.2,sa*.2,-1.4),(ca*.9,sa*.9,-1.85),(ca*.84,sa*.84,-1.98),(ca*.16,sa*.16,-1.85)],.035,MID)
    M.blob((0,.3,.75),.12,GLASS,sub=2,squash=(1,.6,1.8),noise=0)                                                     # bridge
    shieldgen(M,(0,.32,-1.25),.12)
    abox(M,(0,-.3,-.2),(.26,.1,.5),DARK,(.9,.9))
    M.vent((0,0,-2.03),.12)
    for sx in (1,-1):M.vent((sx*.18,0,-1.98),.07)
    return finish(M,3.4,1.0)
def cathedral(): # carrier: a great crystal-veined spire with a flight deck along its back, hangar mouths in the bow, two halos crossed
                 # in an X aft carrying turrets and crystal holds, a tall bridge spire, drives in a triangle
    M=Mesh(132)
    loft(M,[(-2.3,DIA(.3,.3)),(-1.6,DIA(.8,.55)),(1.3,DIA(.78,.54)),(2.1,DIA(.42,.3)),(2.4,DIA(.08,.06))],SP)        # great spire hull
    for sx in (1,-1):
        for k in range(3):plate(M,[(sx*.5,.12+k*.06,1.5-k*.2),(sx*.42,.2+k*.06,1.5-k*.2),(sx*.42,.18+k*.06,-1.4),(sx*.5,.1+k*.06,-1.4)],.01,WIN,.85)   # crystal veins
        mouth(M,(sx*.32,-.02,2.22),.3,.2)
    plate(M,[(-.5,.5,1.8),(.5,.5,1.8),(.5,.5,-1.0),(-.5,.5,-1.0)],.03,MID,.95)                                      # flight deck along the back
    for x in (-.5,.5):plate(M,[(x,.5,1.8),(x*1.0,.42,1.8),(x*1.0,.42,-1.0),(x,.5,-1.0)],.02,LIGHT)
    spots(M,[(-.25,1.35),(.25,1.35),(-.25,-.4),(.25,-.4)],.13,.52)
    for th in (PI/4,-PI/4):                                                                                          # two halos crossed in an X aft
        u=np.array([math.sin(th),math.cos(th),0.])
        pts=[np.array([0,0,-1.5])+u*math.cos(a)*1.25+np.array([0,0,math.sin(a)*1.25]) for a in np.linspace(0,2*PI,41)]
        M.tube(pts,[.06]*len(pts),6,lambda i,j,n,p:(ACC,1.0),cap0=False,cap1=False)
        for sg in (1,-1):
            tip=np.array([0,0,-1.5])+u*sg*1.25
            if tip[1]>0:pd(M,tuple(tip+[0,.04,0]),.08,ACC)
            else:crystal(M,-2.1,-.9,.18,.18,tip[0],tip[1])
    loft(M,[(-1.3,DIA(.12,.12,0,.55)),(-.9,DIA(.16,.14,0,.75)),(-.6,DIA(.06,.05,0,.95))],SP);M.blob((0,.85,-.95),.13,GLASS,sub=2,squash=(1,.6,1.5),noise=0)   # bridge spire
    tube(M,[(0,.95,-.95),(0,1.4,-.95)],[.025,.012],LIGHT,.9,6)
    for z,r in ((1.2,.08),(1.32,.055)):ring(M,(0,z,-.95),r,.012,ACC,seg=12,sides=4,axis='y')
    shieldgen(M,(0,.58,-1.4),.16)
    for k in range(3):a=PI/2+k*2*PI/3;M.vent((math.cos(a)*.3,math.sin(a)*.22,-2.33),.14)
    lights(M,[(.3,-.1,2.35),(-.3,-.1,2.35)],.045)
    return finish(M,4.6,1.0)

CAPITALS=[('halcyon','Halcyon Accord',[('Shrike','Escort',shrike),('Sovereign','Carrier',sovereign)]),
          ('varkesh','Varkesh Dominion',[('Vanguard','Escort',vanguard),('Bastille','Carrier',bastille)]),
          ('ostrova','Ostrova Collective',[('Lantern','Escort',lantern),('Cathedral','Carrier',cathedral)])]
