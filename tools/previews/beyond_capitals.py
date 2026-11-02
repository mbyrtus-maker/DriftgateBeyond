# Driftgate Beyond: capital ships, an escort and a carrier per faction (preview, not in the model pack yet). Second pass.
# Capital ships, not resized fighters: long layered hulls, plating, sponsons and superstructure, a raised BRIDGE with a lit
# window band (no fighter canopies), no fighter fins.
# Driftgate 1's two capitals set the working parts every design keeps (see DESIGN_NOTES "Capital ship models"):
#   escort  - forward torpedo tubes, point-defence turrets on the flanks (3 a side), a bridge, a ventral assault bay, a shield
#             generator, a main drive and auxiliaries, hull berths for docking
#   carrier - a flight deck players land on from above (spots fore and aft), launch mouths at the bow, point-defence turrets,
#             a bridge, a shield generator, several drives
import math
import numpy as np
from beyond_hulls import Mesh,LIGHT,MID,DARK,ACC,GLASS,GLOW,WIN,loft,box,plate,barrel,ring,LENS,HEX,DIA,lens_role,hex_role
from beyond_work import finish,abox,crystal,lights,SP,STAR
from beyond_recon import dish,torpedo,SMH,smh_role
PI=math.pi

def tube(M,pts,rad,role,sh=1.0,sides=8,cap0=True,cap1=True):
    # as beyond_work.tube, but picks a frame that also works for tubes standing straight up
    p=np.array(pts,float);d=p[-1]-p[0];up=(0,0,1) if abs(d[1])>.9*(np.linalg.norm(d)+1e-12) else (0,1,0)
    M.tube(pts,rad,sides,lambda i,j,n,q:(role,sh),cap0=cap0,cap1=cap1,up=up)
def stacks(M,base,n,sp=.16,h=.3):
    for k in range(n):
        b=np.array(base,float)+[k*sp-(n-1)*sp/2,0,0];box(M,tuple(b+[0,.03,0]),(.13,.06,.13),DARK);tube(M,[b,b+[0,h,0]],[.065,.06],MID,1.0,8);ring(M,tuple(b+[0,h*.75,0]),.07,.014,ACC,seg=12,sides=4,axis='y');M.blob(tuple(b+[0,h+.005,0]),.045,DARK,sub=1,squash=(1,.3,1),noise=0)

def pd(M,c,r=.07,role=MID,up=True):
    # a point-defence turret: a base, a dome and twin barrels pointing forward
    c=np.array(c,float);s=1 if up else -1
    tube(M,[c,c+[0,s*r*.5,0]],[r*1.2,r*1.1],DARK,.9,8);M.blob(tuple(c+[0,s*r*.7,0]),r,role,sub=1,squash=(1,.7,1),noise=0)
    for sx in (1,-1):tube(M,[c+[sx*r*.35,s*r*.8,r*.3],c+[sx*r*.35,s*r*.8,r*1.9]],[.012,.011],DARK,1.0,5)
def spots(M,pts,r=.12,y=0):
    # deck landing spots: an accent ring with a bar
    for x,z in pts:
        ring(M,(x,y+.01,z),r,.012,ACC,seg=16,sides=4,axis='y')
        plate(M,[(x-r*.7,y+.012,z-.012),(x+r*.7,y+.012,z-.012),(x+r*.7,y+.012,z+.012),(x-r*.7,y+.012,z+.012)],.004,ACC)
def mouth(M,c,w,h,d=.25):
    # a hangar launch mouth: a dark recess with a lit lip
    abox(M,(c[0],c[1],c[2]-d/2),(w,h,d),DARK,(1,1),.6)
    for a,b in (((-w/2,-h/2),(w/2,-h/2)),((w/2,-h/2),(w/2,h/2)),((w/2,h/2),(-w/2,h/2)),((-w/2,h/2),(-w/2,-h/2))):
        tube(M,[(c[0]+a[0],c[1]+a[1],c[2]+.01),(c[0]+b[0],c[1]+b[1],c[2]+.01)],[.012,.012],WIN,1.0,4,cap0=False,cap1=False)
def shieldgen(M,c,r=.14,up=True):
    c=np.array(c,float);s=1 if up else -1;tube(M,[c-[0,s*r*.6,0],c],[r*.7,r*.6],DARK,.9,10);M.blob(tuple(c+[0,s*r*.15,0]),r,GLASS,sub=2,squash=(1,.65,1),noise=0)
    ring(M,tuple(c),r*1.1,.016,WIN,seg=18,sides=4,axis='y')
def windows(M,c,w,y,z,n=None):
    # a lit window band facing forward
    plate(M,[(c-w/2,y-.018,z),(c+w/2,y-.018,z),(c+w/2,y+.018,z),(c-w/2,y+.018,z)],.012,WIN,1.0)
def sidewin(M,x,y,z0,z1):
    plate(M,[(x,y-.015,z0),(x,y-.015,z1),(x,y+.015,z1),(x,y+.015,z0)],.01,WIN,1.0)

def bridge_halcyon(M,c,s=1.0):
    # a streamlined lens bridge pod on a pedestal, a wrap-round window band, a dish
    x,y,z=c
    loft(M,[(z-.45*s,[(a+x,b+y) for a,b in LENS(.1*s,.08*s)]),(z-.3*s,[(a+x,b+y) for a,b in LENS(.16*s,.12*s)]),(z+.1*s,[(a+x,b+y) for a,b in LENS(.15*s,.12*s)]),(z+.2*s,[(a+x,b+y) for a,b in LENS(.08*s,.07*s)])],lens_role)   # pedestal
    yb=y+.16*s
    loft(M,[(z-.3*s,[(a+x,b+yb) for a,b in LENS(.18*s,.08*s)]),(z-.15*s,[(a+x,b+yb) for a,b in LENS(.26*s,.11*s)]),(z+.2*s,[(a+x,b+yb) for a,b in LENS(.24*s,.1*s)]),(z+.33*s,[(a+x,b+yb) for a,b in LENS(.12*s,.05*s)])],lens_role)   # bridge pod
    windows(M,x,.36*s,yb+.03*s,z+.27*s)
    for sx in (1,-1):sidewin(M,x+sx*.252*s,yb+.03*s,z-.1*s,z+.18*s)
    dish(M,(x,yb+.13*s,z-.18*s),.08*s);tube(M,[(x,yb+.08*s,z-.18*s),(x,yb+.12*s,z-.18*s)],[.015,.015],LIGHT,.9,5)
def bridge_varkesh(M,c,s=1.0):
    # stepped smoothed-hex tiers, a slit window band on the top tier, a mast
    x,y,z=c
    for k,(w,h,l,dy) in enumerate(((.42,.14,.7,0),(.32,.12,.52,.13),(.22,.1,.36,.24))):
        loft(M,[(z-l/2*s,[(a+x,b+y+dy*s) for a,b in SMH(w/2*s,h/2*s)]),(z+l/2*s,[(a+x,b+y+dy*s) for a,b in SMH(w/2*s*.92,h/2*s*.92)])],smh_role)
    windows(M,x,.18*s,y+.25*s,z+.18*s);[sidewin(M,x+sx*.105*s,y+.25*s,z-.12*s,z+.14*s) for sx in (1,-1)]
    tube(M,[(x,y+.3*s,z-.08*s),(x,y+.62*s,z-.1*s)],[.016,.01],LIGHT,.9,5);ring(M,(x,y+.5*s,z-.09*s),.04*s,.008,ACC,seg=10,sides=4,axis='y')
def bridge_ostrova(M,c,s=1.0):
    # a faceted spire tower, a crystal window band round its head, a slender mast
    x,y,z=c;b=np.array([x,y,z])
    tube(M,[b,b+[0,.12*s,0],b+[0,.2*s,0]],[.16*s,.13*s,.15*s],MID,1.0,6)
    tube(M,[b+[0,.2*s,0],b+[0,.28*s,0]],[.15*s,.13*s],WIN,1.0,6,cap0=False,cap1=False)
    tube(M,[b+[0,.28*s,0],b+[0,.34*s,0],b+[0,.38*s,0]],[.13*s,.08*s,.01],LIGHT,1.0,6)
    tube(M,[b+[0,.37*s,0],b+[0,.55*s,0]],[.012,.006],LIGHT,.9,5);ring(M,tuple(b+[0,.47*s,0]),.05*s,.008,ACC,seg=10,sides=4,axis='y')

# ============================================================== HALCYON
def shrike():    # escort: a long layered lens hull: a broad torpedo prow, a raised dorsal superstructure spine, turret sponsons
                 # faired along the flanks, a bridge pod aft of amidships, emitter nodes on short pylons, a three-drive engine block
    M=Mesh(111)
    loft(M,[(-2.3,LENS(.42,.3)),(-1.9,LENS(.5,.34)),(.9,LENS(.5,.34)),(1.6,LENS(.42,.28,-.02)),(2.05,LENS(.3,.18,-.04)),(2.25,LENS(.16,.1,-.05))],lens_role)   # main hull
    loft(M,[(-1.8,LENS(.12,.06,.3)),(-1.5,LENS(.22,.12,.34)),(.8,LENS(.2,.11,.33)),(1.4,LENS(.08,.04,.3))],lens_role)   # dorsal superstructure spine
    for z in (-1.0,-.2,.6):plate(M,[(-.16,.47,z+.18),(.16,.47,z+.18),(.16,.47,z-.18),(-.16,.47,z-.18)],.006,ACC,.9)
    for sx in (1,-1):
        for dy in (.04,-.1):tube(M,[(sx*.18,dy-.05,2.0),(sx*.18,dy-.05,2.3)],[.06,.06],DARK,.85,8,cap1=False);M.blob((sx*.18,dy-.05,2.27),.045,ACC,sub=1,noise=0)   # torpedo tubes
        loft(M,[(-1.5,[(a+sx*.5,b-.04) for a,b in LENS(.05,.05)]),(-1.2,[(a+sx*.5,b-.04) for a,b in LENS(.15,.14)]),(.9,[(a+sx*.5,b-.04) for a,b in LENS(.15,.14)]),(1.3,[(a+sx*.5,b-.04) for a,b in LENS(.05,.05)])],lens_role)   # turret sponson
        for z in (-.85,-.1,.65):pd(M,(sx*.56,.1,z),.07)
        tube(M,[(sx*.5,.05,-1.65),(sx*.78,.12,-1.75)],[.025,.02],LIGHT,.9,5);M.blob((sx*.8,.13,-1.76),.06,WIN,sub=1,noise=0)   # emitter nodes on pylons
        sidewin(M,sx*.505,.12,-.5,.5)
    bridge_halcyon(M,(0,.42,-1.0),1.0)
    shieldgen(M,(0,-.33,.75),.12,up=False)
    abox(M,(0,-.36,-.4),(.34,.12,.6),DARK,(.9,.9))                                                                   # ventral assault bay
    loft(M,[(-2.6,LENS(.36,.26)),(-2.3,LENS(.44,.31))],(MID,.95))                                                    # engine block
    M.vent((0,0,-2.62),.2)
    for sx in (1,-1):M.vent((sx*.28,.0,-2.6),.11)
    lights(M,[(.3,-.08,2.18),(-.3,-.08,2.18)],.04)
    return finish(M,3.6,1.0)
def sovereign(): # carrier: a broad blended lens hull with a flat flight deck, twin hangar mouths in the bow, twin engine booms aft
                 # (no tail fins), a bridge pod beside the deck, turret sponsons and a shield generator
    M=Mesh(112)
    loft(M,[(-2.2,LENS(.7,.32)),(-1.5,LENS(1.1,.42)),(1.0,LENS(1.05,.42)),(1.9,LENS(.7,.32)),(2.3,LENS(.32,.18))],lens_role)
    plate(M,[(-.62,.44,2.05),(.62,.44,2.05),(.7,.44,-1.2),(-.7,.44,-1.2)],.03,MID,.95)                               # flight deck
    spots(M,[(-.3,1.35),(.3,1.35),(-.3,-.45),(.3,-.45)],.14,.46)
    for x in (-.32,.32):plate(M,[(x-.012,.465,1.9),(x+.012,.465,1.9),(x+.012,.465,-1.1),(x-.012,.465,-1.1)],.003,WIN,.9)
    for sx in (1,-1):mouth(M,(sx*.42,.05,2.28),.42,.26)
    for sx in (1,-1):
        loft(M,[(-1.6,[(a+sx*1.05,b) for a,b in LENS(.05,.05)]),(-1.3,[(a+sx*1.05,b) for a,b in LENS(.14,.14)]),(1.3,[(a+sx*1.05,b) for a,b in LENS(.14,.14)]),(1.6,[(a+sx*1.05,b) for a,b in LENS(.05,.05)])],lens_role)
        for z in (-.9,-.1,.7):pd(M,(sx*1.1,.12,z),.07)
        tube(M,[(sx*1.15,-.05,-1.0),(sx*1.15,-.05,-2.5),(sx*1.15,-.05,-2.65)],[.16,.2,.19],MID,.95,12,cap1=False);M.vent((sx*1.15,-.05,-2.65),.16)   # engine booms
        for z in (-1.5,-2.1):ring(M,(sx*1.15,-.05,z),.205,.014,ACC,seg=18,sides=4)
        M.blob((sx*1.2,.15,-1.5),.07,WIN,sub=1,noise=0)
        sidewin(M,sx*1.07,.08,-1.2,1.2)
    bridge_halcyon(M,(.85,.42,-.6),1.1)                                                                             # bridge beside the deck
    shieldgen(M,(0,.48,-1.75),.18)
    loft(M,[(-2.36,LENS(.6,.29)),(-2.2,LENS(.7,.32))],(MID,.95))                                                    # engine block: five drives
    for x in (0,.34,-.34):M.vent((x,.07,-2.37),.14)
    for x in (.17,-.17):M.vent((x,-.12,-2.37),.11)
    return finish(M,4.6,1.0)

# ============================================================== VARKESH
def vanguard():  # escort: a clean armoured smoothed-hex hull, a chisel prow with four torpedo tubes, long turret sponsons, a stepped bridge,
                 # a four-drive engine block
    M=Mesh(121)
    loft(M,[(-2.2,SMH(.48,.36)),(1.0,SMH(.48,.36)),(1.7,SMH(.36,.26,-.02)),(2.15,SMH(.18,.1,-.05))],smh_role)
    for x in (-.14,.14):
        for y in (.0,-.14):tube(M,[(x,y,1.75),(x,y,1.95)],[.055,.055],DARK,.85,8,cap1=False);M.blob((x,y,1.92),.04,ACC,sub=1,noise=0)   # torpedo tubes
    for sx in (1,-1):
        loft(M,[(-1.6,[(a+sx*.56,b-.02) for a,b in SMH(.06,.07)]),(-1.3,[(a+sx*.56,b-.02) for a,b in SMH(.14,.16)]),(.9,[(a+sx*.56,b-.02) for a,b in SMH(.14,.16)]),(1.2,[(a+sx*.56,b-.02) for a,b in SMH(.06,.07)])],smh_role)   # turret sponson
        for z in (-1.0,-.25,.5):pd(M,(sx*.58,.14,z),.07,MID)
        sidewin(M,sx*.485,.06,-1.5,.8)
    for z in (-1.4,-.4,.6):loft(M,[(z-.05,SMH(.5,.38)),(z+.05,SMH(.5,.38))],(ACC,.95))                                # armour bands
    bridge_varkesh(M,(0,.32,-.9),1.0)
    shieldgen(M,(0,-.35,.6),.12,up=False)
    abox(M,(0,-.36,-.3),(.36,.1,.6),DARK,(.9,.9))
    loft(M,[(-2.55,SMH(.42,.32)),(-2.2,SMH(.5,.38))],smh_role)                                                       # engine block
    for x in (-.2,.2):
        for y in (-.12,.12):M.vent((x,y,-2.57),.11)
    stacks(M,(0,.36,-1.8),2,.22,.28)
    lights(M,[(.2,-.06,2.1),(-.2,-.06,2.1)],.04)
    return finish(M,3.6,1.0)
def bastille():  # carrier: a smooth slab fortress, a railed flight deck, hangar mouths in a blunt bow, faired turret sponsons,
                 # a stepped bridge aft, armour bands, an eight-drive engine block
    M=Mesh(122)
    loft(M,[(-2.3,SMH(1.0,.5)),(1.75,SMH(1.0,.5)),(2.25,SMH(.85,.4,-.04))],smh_role)                               # slab hull
    plate(M,[(-.78,.5,2.05),(.78,.5,2.05),(.78,.5,-1.25),(-.78,.5,-1.25)],.03,DARK,.95)                              # flight deck
    spots(M,[(-.35,1.4),(.35,1.4),(-.35,-.5),(.35,-.5)],.15,.51)
    for sx in (1,-1):
        loft(M,[(-1.3,[(a+sx*.82,b+.56) for a,b in SMH(.04,.04)]),(1.95,[(a+sx*.82,b+.56) for a,b in SMH(.04,.04)])],(ACC,.95))   # deck rail
        mouth(M,(sx*.45,.0,2.26),.48,.3)
        loft(M,[(-1.9,[(a+sx*1.02,b-.04) for a,b in SMH(.08,.1)]),(-1.6,[(a+sx*1.02,b-.04) for a,b in SMH(.18,.24)]),(1.4,[(a+sx*1.02,b-.04) for a,b in SMH(.18,.24)]),(1.7,[(a+sx*1.02,b-.04) for a,b in SMH(.08,.1)])],smh_role)   # faired turret sponson
        for z in (-1.2,-.4,.4,1.1):pd(M,(sx*1.05,.2,z),.075,MID)
        sidewin(M,sx*1.0,.1,-1.8,1.6)
    for z in (-1.8,-.9,0,.9):loft(M,[(z-.05,SMH(1.03,.5)),(z+.05,SMH(1.03,.5))],(ACC,.95))                          # armour bands
    bridge_varkesh(M,(0,.5,-1.75),1.35)
    shieldgen(M,(0,.6,-.95),.16)
    loft(M,[(-2.65,SMH(.85,.42)),(-2.3,SMH(1.0,.5))],smh_role)                                                       # engine block
    for x in (-.6,-.2,.2,.6):
        for y in (-.15,.15):M.vent((x,y,-2.67),.12)
    lights(M,[(.6,.3,2.3),(-.6,.3,2.3)],.045)
    return finish(M,4.6,1.0)

# ============================================================== OSTROVA
def lantern():   # escort: a long faceted spire hull in three sections, two turret halos round it, crystal cores between them,
                 # four torpedo tubes in the prow, a spire bridge, a drive cluster
    M=Mesh(131)
    OCT=lambda w,h,dy=0:[(math.cos(a)*w,math.sin(a)*h+dy) for a in np.linspace(PI/8,2*PI+PI/8,8,endpoint=False)]
    oct_role=lambda i,j:([LIGHT,LIGHT,LIGHT,MID,MID,DARK,DARK,MID][j],[1,.97,1,.95,.9,.85,.85,.92][j])
    loft(M,[(-2.3,OCT(.3,.28)),(-1.9,OCT(.4,.36)),(1.0,OCT(.38,.34)),(1.75,OCT(.24,.22)),(2.2,OCT(.08,.07))],oct_role)   # long faceted hull
    for z in (-1.15,.15):                                                                                          # two turret halos round the hull
        ring(M,(0,0,z),.66,.045,ACC,seg=36,sides=6)
        for k in range(6):
            a=PI/6+k*PI/3;x,y=math.cos(a)*.66,math.sin(a)*.66
            if abs(math.cos(a))>.5:pd(M,(x,y,z),.06,ACC,up=y>0)
            else:tube(M,[(math.cos(a)*.38,math.sin(a)*.38,z),(x*.95,y*.95,z)],[.03,.03],LIGHT,.9,5,cap0=False,cap1=False)
        for k in (0,3):a=PI/6+k*PI/3;tube(M,[(math.cos(a)*.38,math.sin(a)*.38,z),(math.cos(a)*.62,math.sin(a)*.62,z)],[.03,.03],LIGHT,.9,5,cap0=False,cap1=False)
    for sx in (1,-1):crystal(M,-.95,-.05,.14,.16,sx*.4,0)                                                            # crystal cores between the halos
    for k in range(4):a=PI/4+k*PI/2;tube(M,[(math.cos(a)*.18,math.sin(a)*.16,1.7),(math.cos(a)*.18,math.sin(a)*.16,1.95)],[.045,.045],DARK,.85,8,cap1=False);M.blob((math.cos(a)*.18,math.sin(a)*.16,1.92),.035,ACC,sub=1,noise=0)
    bridge_ostrova(M,(0,.33,-.55),1.0)
    shieldgen(M,(0,-.33,.7),.12,up=False)
    abox(M,(0,-.36,-.5),(.3,.1,.55),DARK,(.9,.9))
    for k in range(3):a=PI/2+k*2*PI/3;M.vent((math.cos(a)*.16,math.sin(a)*.15,-2.32),.1)
    return finish(M,3.6,1.0)
def cathedral(): # carrier: a smooth, great crystal-veined hull with a flight deck along its back, hangar mouths in the bow, two horizontal
                 # rings round the hull fore and aft carrying turrets and crystal holds, a spire bridge, a drive cluster
    M=Mesh(132)
    OCT=lambda w,h,dy=0:[(math.cos(a)*w,math.sin(a)*h+dy) for a in np.linspace(PI/8,2*PI+PI/8,8,endpoint=False)]
    oct_role=lambda i,j:([LIGHT,LIGHT,LIGHT,MID,MID,DARK,DARK,MID][j],[1,.97,1,.95,.9,.85,.85,.92][j])
    loft(M,[(-2.4,OCT(.5,.36)),(-1.9,OCT(.85,.55)),(1.4,OCT(.82,.54)),(2.1,OCT(.5,.34)),(2.45,OCT(.18,.12))],oct_role)   # smooth great hull
    for sx in (1,-1):
        for k in range(2):plate(M,[(sx*.8,-.05+k*.14,1.6),(sx*.8,.05+k*.14,1.6),(sx*.79,.05+k*.14,-1.6),(sx*.79,-.05+k*.14,-1.6)],.01,WIN,.85)   # crystal veins
        mouth(M,(sx*.3,-.02,2.3),.3,.2)
    plate(M,[(-.46,.51,1.4),(.46,.51,1.4),(.46,.51,-.95),(-.46,.51,-.95)],.03,MID,.95)                          # flight deck along the back
    spots(M,[(-.22,1.0),(.22,1.0),(-.22,-.45),(.22,-.45)],.13,.53)
    for z0 in (1.2,-1.45):                                                                                         # two horizontal rings round the hull, fore and aft
        R=1.25;ring(M,(0,0,z0),R,.06,ACC,seg=48,sides=6,axis='y')
        for sx in (1,-1):
            tube(M,[(sx*.8,0,z0),(sx*R*.97,0,z0)],[.05,.05],LIGHT,.9,6,cap0=False,cap1=False)                         # spoke from the hull
            crystal(M,z0-.42,z0+.42,.17,.2,sx*R,0)                                                                   # crystal hold on the ring
            for a in (.55,-.55):pd(M,(sx*math.cos(a)*R,.05,z0+math.sin(a)*R),.08,ACC)                                 # turrets on the ring
    bridge_ostrova(M,(0,.5,-1.55),1.4)
    shieldgen(M,(0,.56,-1.12),.13)
    for k in range(3):a=PI/2+k*2*PI/3;M.vent((math.cos(a)*.3,math.sin(a)*.22,-2.42),.14)
    lights(M,[(.3,-.1,2.4),(-.3,-.1,2.4)],.045)
    return finish(M,4.6,1.0)

CAPITALS=[('halcyon','Halcyon Accord',[('Shrike','Escort',shrike),('Sovereign','Carrier',sovereign)]),
          ('varkesh','Varkesh Dominion',[('Vanguard','Escort',vanguard),('Bastille','Carrier',bastille)]),
          ('ostrova','Ostrova Collective',[('Lantern','Escort',lantern),('Cathedral','Carrier',cathedral)])]
