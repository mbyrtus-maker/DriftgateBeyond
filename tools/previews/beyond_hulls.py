# Driftgate Beyond: faction hull designs generated in code, one design language per faction (preview, not in the model pack yet).
# Same conventions as tools/brood.py: nose +z, up +y, about 2 long, a colour ROLE per triangle painted from the faction palette.
#   Halcyon Accord   - long, swept and bird-like: lens-section fuselage, needle nose, glass canopy, gull wings, shield nodes
#   Varkesh Dominion - blocky armoured slabs: hexagonal hull, bolted plates, exposed gun barrels, slit canopy, square drives
#   Ostrova Collective - slender spires: diamond-section mast, a glowing reactor halo, three fins, sensor mast and crystal panels
import math,sys,os
import numpy as np
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..'))
from brood import Mesh,LIGHT,MID,DARK,ACC,GLASS,GLOW,WIN

def loft(M,secs,role,cap0=True,cap1=True,sh0=1.0):
    # secs: [(z,[(x,y),...])] with the same point count; quads between sections, oriented outward from each section's centre
    S=[(z,[np.array([x,y,z],float) for x,y in pts]) for z,pts in secs];n=len(S[0][1])
    for i in range(len(S)-1):
        a,b=S[i][1],S[i+1][1];ref=(sum(a)/n+sum(b)/n)/2
        for j in range(n):
            r,sh=role(i,j) if callable(role) else (role,sh0)
            M.tri(a[j],a[(j+1)%n],b[(j+1)%n],r,sh,ref=ref);M.tri(a[j],b[(j+1)%n],b[j],r,sh,ref=ref)
    for k,cap,dz in ((0,cap0,.01),(-1,cap1,-.01)):
        if not cap:continue
        P=S[k][1];c=sum(P)/n
        r,sh=role(-1,0) if callable(role) else (role,sh0)
        for j in range(n):M.tri(c,P[j],P[(j+1)%n],r,sh*.9,ref=c+np.array([0,0,dz]))
def box(M,c,size,role,taper=(1,1),sh=1.0):
    # a box centred on c, size (w,h,l) along x,y,z; taper scales the front (+z) face
    cx,cy,cz=c;w,h,l=size;tw,th=taper
    rect=lambda sw,sh_:[(cx-sw/2,cy-sh_/2),(cx+sw/2,cy-sh_/2),(cx+sw/2,cy+sh_/2),(cx-sw/2,cy+sh_/2)]
    loft(M,[(cz-l/2,rect(w,h)),(cz+l/2,rect(w*tw,h*th))],role,sh0=sh)
def plate(M,pts,thick,role,sh=1.0):
    # a thin convex plate through planar points (a wing, fin or armour panel), both faces and edges
    P=[np.array(p,float) for p in pts];n=np.cross(P[1]-P[0],P[2]-P[0]);n/=np.linalg.norm(n)+1e-12;o=n*thick/2;c=sum(P)/len(P)
    top=[p+o for p in P];bot=[p-o for p in P]
    for i in range(1,len(P)-1):M.tri(top[0],top[i],top[i+1],role,sh,ref=c);M.tri(bot[0],bot[i+1],bot[i],role,sh*.8,ref=c)
    for i in range(len(P)):j=(i+1)%len(P);M.tri(top[i],bot[i],bot[j],role,sh*.9,ref=c);M.tri(top[i],bot[j],top[j],role,sh*.9,ref=c)
def barrel(M,base,length,r,role=DARK):
    b=np.array(base,float);M.tube([b,b+[0,0,length*.5],b+[0,0,length]],[r*1.25,r,r*.9],7,lambda i,j,n,p:(role,.95),cap0=True,cap1=True)
def ring(M,c,R,r,role,seg=28,sides=6,axis='z'):
    pts=[];c=np.array(c,float)
    for k in range(seg+1):
        a=k/seg*2*math.pi;v=[math.cos(a)*R,math.sin(a)*R,0] if axis=='z' else [math.cos(a)*R,0,math.sin(a)*R]
        pts.append(c+v)
    M.tube(pts,[r]*len(pts),sides,lambda i,j,n,p:(role,1.0),cap0=False,cap1=False)

# ------------------------------------------------------------------ Halcyon Swift: light fighter
def swift():
    M=Mesh(11)
    lens=lambda w,h,dy=0:[(math.cos(a)*w,math.sin(a)*h*(1 if math.sin(a)>0 else .7)+dy) for a in np.linspace(0,2*math.pi,12,endpoint=False)]
    fus=[(-1.0,lens(.13,.11)),(-.75,lens(.17,.14)),(-.2,lens(.18,.16)),(.35,lens(.14,.14)),(.75,lens(.07,.07,-.01)),(1.05,lens(.012,.012,-.02))]
    loft(M,fus,lambda i,j:(LIGHT if j<6 else MID,1.0 if j<6 else .92))
    M.blob((0,.14,.38),.11,GLASS,sub=2,squash=(.85,.75,2.4),noise=0)
    for sx in (1,-1):
        # gull wings: root rises, then sweeps back and down to a long tip
        plate(M,[(sx*.12,.02,.05),(sx*.55,.12,-.25),(sx*.5,.12,-.48),(sx*.12,.02,-.42)],.035,LIGHT)
        plate(M,[(sx*.55,.12,-.25),(sx*1.02,.0,-.62),(sx*.98,.0,-.72),(sx*.5,.12,-.48)],.025,LIGHT,.95)
        plate(M,[(sx*.98,.0,-.62),(sx*1.02,.0,-.62),(sx*.98,.0,-.72)],.03,ACC)
        M.blob((sx*1.0,.0,-.66),.045,WIN,sub=1,squash=(1,1,1.6),noise=0)          # shield emitter node
        plate(M,[(sx*.1,.1,-.6),(sx*.24,.38,-.92),(sx*.24,.38,-1.02),(sx*.1,.1,-.98)],.025,ACC,.95)   # canted twin tail
        plate(M,[(sx*.18,.0,.12),(sx*.3,-.02,-.05),(sx*.28,-.02,-.12),(sx*.16,0,-.04)],.02,MID)       # canards
        barrel(M,(sx*.2,-.04,.0),.32,.018)
    M.tube([(0,0,-.98),(0,0,-1.08)],[.12,.1],12,lambda i,j,n,p:(DARK,.9),cap0=False,cap1=False);M.vent((0,0,-1.08),.1)
    for k in range(4):plate(M,[(-.12,.165,-.1-k*.18),(.12,.165,-.1-k*.18),(.12,.165,-.16-k*.18),(-.12,.165,-.16-k*.18)],.005,ACC,.9)  # spine stripe
    return M

# ------------------------------------------------------------------ Varkesh Fang: light fighter
def fang():
    M=Mesh(23)
    hexs=lambda w,h,dy=0:[(w,dy),(w*.55,h+dy),(-w*.55,h+dy),(-w,dy),(-w*.55,-h+dy),(w*.55,-h+dy)]
    body=[(-.85,hexs(.3,.2)),(-.3,hexs(.34,.24)),(.3,hexs(.3,.22)),(.62,hexs(.2,.14,-.02)),(.8,hexs(.1,.08,-.03))]
    loft(M,body,lambda i,j:([MID,MID,MID,DARK,DARK,DARK][j],[1,1.05,1,.9,.85,.9][j]))
    plate(M,[(-.07,.23,.42),(.07,.23,.42),(.07,.26,.12),(-.07,.26,.12)],.02,GLASS)                    # slit canopy
    for sx in (1,-1):
        for k,z in enumerate((.18,-.15,-.48)):box(M,(sx*.3,.13,z),(.08,.16,.3),MID,taper=(.9,.85),sh=.96+.04*k)   # bolted side armour
        plate(M,[(sx*.3,-.04,.15),(sx*.72,-.06,-.12),(sx*.72,-.06,-.4),(sx*.3,-.04,-.55)],.07,DARK)               # stubby slab wing
        box(M,(sx*.72,-.06,-.12),(.13,.13,.42),MID)                                                               # gun pod
        barrel(M,(sx*.72,-.03,.09),.38,.028)
        barrel(M,(sx*.72,-.09,.09),.34,.028)
        plate(M,[(sx*.18,.05,.78),(sx*.12,-.06,.78),(sx*.09,-.07,1.02),(sx*.11,.0,1.06)],.05,ACC)                  # the fangs
        box(M,(sx*.16,0,-.9),(.2,.2,.14),DARK);M.vent((sx*.16,0,-.97),.08)                                          # square drives
        plate(M,[(sx*.25,.24,-.45),(sx*.33,.42,-.7),(sx*.33,.42,-.8),(sx*.25,.24,-.8)],.05,ACC,.9)                  # stub fins
    barrel(M,(0,-.2,.25),.5,.035)                                                                                  # chin gun: the extra slot
    box(M,(0,-.2,.18),(.14,.1,.22),DARK)
    for z in (-.55,-.1,.35):box(M,(0,.25,z),(.22,.03,.12),ACC,sh=.9)                                               # armour bands
    return M

# ------------------------------------------------------------------ Ostrova Mote: light fighter
def mote():
    M=Mesh(37)
    dia=lambda w,h:[(w,0),(0,h),(-w,0),(0,-h)]
    spire=[(-.95,dia(.05,.05)),(-.6,dia(.13,.11)),(-.1,dia(.16,.15)),(.4,dia(.1,.1)),(.85,dia(.035,.035)),(1.0,dia(.004,.004))]
    loft(M,spire,lambda i,j:((LIGHT,1.0) if j in (0,1) else (MID,.92)))
    ring(M,(0,0,-.32),.42,.035,ACC)                                          # the reactor halo
    ring(M,(0,0,-.32),.36,.012,WIN,sides=5)
    for k in range(3):
        a=math.pi/2+k*2*math.pi/3;ca,sa=math.cos(a),math.sin(a)
        plate(M,[(ca*.12,sa*.12,-.05),(ca*.42,sa*.42,-.28),(ca*.42,sa*.42,-.38),(ca*.12,sa*.12,-.75)],.025,LIGHT,.95)   # three spokes to the halo
        plate(M,[(ca*.1,sa*.1,-.55),(ca*.55,sa*.55,-.9),(ca*.5,sa*.5,-1.0),(ca*.08,sa*.08,-.9)],.02,MID)                 # tri fins
        M.blob((ca*.42,sa*.42,-.32),.05,GLASS,sub=1,squash=(1,1,1.5),noise=0)                                           # crystal nodes on the halo
        barrel(M,(ca*.16,sa*.16,.1),.3,.016,ACC)                                                                         # emitter lances
    M.blob((0,.11,.28),.07,GLASS,sub=2,squash=(.9,.7,2.0),noise=0)
    M.tube([(0,0,.9),(0,0,1.32)],[.02,.012],6,lambda i,j,n,p:(LIGHT,.9))                                          # sensor mast
    for z,r in ((1.1,.06),(1.23,.042)):ring(M,(0,0,z),r,.011,ACC,seg=14,sides=5)
    for z in (1.1,1.23):plate(M,[(-.06,0,z),(.06,0,z),(0,.006,z+.004)],.006,ACC)
    plate(M,[(0,.1,-.2),(0,.3,-.45),(0,.3,-.55),(0,.1,-.6)],.015,WIN,.9)                                             # crystal panel
    M.vent((0,0,-.97),.05)
    return M

# ------------------------------------------------------------------ shared section shapes for the bigger hulls
def LENS(w,h,dy=0,n=12):return [(math.cos(a)*w,math.sin(a)*h*(1 if math.sin(a)>0 else .7)+dy) for a in np.linspace(0,2*math.pi,n,endpoint=False)]
def HEX(w,h,dy=0,dx=0):return [(w+dx,dy),(w*.55+dx,h+dy),(-w*.55+dx,h+dy),(-w+dx,dy),(-w*.55+dx,-h+dy),(w*.55+dx,-h+dy)]
def DIA(w,h,dx=0,dy=0):return [(w+dx,dy),(dx,h+dy),(-w+dx,dy),(dx,-h+dy)]
def lens_role(i,j):return (LIGHT,1.0) if j<6 else (MID,.92)
def hex_role(i,j):return ([MID,MID,MID,DARK,DARK,DARK][j],[1,1.05,1,.9,.85,.9][j])

# ------------------------------------------------------------------ Halcyon Kite: medium fighter (double delta, twin engines)
def kite():
    M=Mesh(12)
    loft(M,[(-1.15,LENS(.16,.12)),(-.85,LENS(.22,.16)),(-.2,LENS(.23,.19)),(.45,LENS(.17,.16)),(.95,LENS(.08,.08,-.01)),(1.28,LENS(.012,.012,-.02))],lens_role)
    M.blob((0,.17,.45),.13,GLASS,sub=2,squash=(.85,.75,2.6),noise=0)
    for sx in (1,-1):
        plate(M,[(sx*.15,.02,.7),(sx*.42,.04,-.05),(sx*.2,.03,-.1)],.03,LIGHT)                                     # forward strake
        plate(M,[(sx*.2,.03,.25),(sx*1.0,-.02,-.86),(sx*.96,-.02,-.98),(sx*.2,.03,-.95)],.04,LIGHT)                 # one broad delta wing
        plate(M,[(sx*.45,.06,-.3),(sx*.8,.03,-.75),(sx*.45,.06,-.75)],.012,ACC,.9)                                    # wing panel
        M.blob((sx*.98,-.02,-.92),.055,WIN,sub=1,squash=(1,1,1.7),noise=0)
        M.tube([(sx*.2,-.02,-.3),(sx*.2,-.02,-1.12),(sx*.2,-.02,-1.22)],[.1,.11,.1],10,lambda i,j,n,p:(MID,.95),cap0=True,cap1=False)
        M.vent((sx*.2,-.02,-1.22),.085)
        plate(M,[(sx*.22,.12,-.62),(sx*.4,.58,-1.02),(sx*.4,.58,-1.14),(sx*.22,.12,-1.15)],.025,ACC,.95)        # tall canted twin tail
        barrel(M,(sx*.26,-.05,.1),.38,.02)
        M.tube([(sx*.6,-.06,-.25),(sx*.6,-.06,-.7)],[.035,.035],8,lambda i,j,n,p:(DARK,.9))                     # missile launcher pod
    for k in range(5):plate(M,[(-.13,.2,-.05-k*.17),(.13,.2,-.05-k*.17),(.13,.2,-.11-k*.17),(-.13,.2,-.11-k*.17)],.005,ACC,.9)
    return M

# ------------------------------------------------------------------ Halcyon Osprey: heavy fighter (blended wing, twin booms, three drives)
def osprey():
    M=Mesh(13)
    loft(M,[(-1.2,LENS(.2,.15)),(-.8,LENS(.3,.2)),(-.1,LENS(.32,.24)),(.55,LENS(.22,.19)),(1.1,LENS(.1,.09,-.01)),(1.42,LENS(.015,.015,-.02))],lens_role)
    M.blob((0,.22,.55),.15,GLASS,sub=2,squash=(.9,.75,2.5),noise=0)
    for sx in (1,-1):
        plate(M,[(sx*.28,.02,.45),(sx*.7,.05,-.1),(sx*.66,.05,-.55),(sx*.28,.02,-.75)],.06,LIGHT)                    # blended inner wing
        plate(M,[(sx*.7,.05,-.1),(sx*1.42,-.04,-.6),(sx*1.36,-.04,-.75),(sx*.66,.05,-.55)],.04,LIGHT,.95)
        M.blob((sx*1.4,-.04,-.68),.065,WIN,sub=1,squash=(1,1,1.7),noise=0)
        M.tube([(sx*.68,.04,.15),(sx*.68,.04,-1.25),(sx*.68,.04,-1.38)],[.07,.09,.085],10,lambda i,j,n,p:(MID,.95),cap0=True,cap1=False)   # booms
        M.vent((sx*.68,.04,-1.38),.07)
        plate(M,[(sx*.68,.1,-.85),(sx*.68,.5,-1.22),(sx*.68,.5,-1.34),(sx*.68,.1,-1.32)],.03,ACC,.95)              # boom tails
        for z in (.15,-.05):barrel(M,(sx*.5,-.06,z),.42,.022)
        M.tube([(sx*1.0,-.08,-.3),(sx*1.0,-.08,-.75)],[.04,.04],8,lambda i,j,n,p:(DARK,.9))
    plate(M,[(-.68,.42,-1.22),(.68,.42,-1.22),(.68,.42,-1.32),(-.68,.42,-1.32)],.025,ACC)                          # stabiliser between the booms
    M.vent((0,0,-1.2),.13)
    M.blob((0,.27,-.35),.13,MID,sub=2,squash=(1,.4,1),noise=0);ring(M,(0,.33,-.35),.13,.018,WIN,seg=18,sides=5,axis='y')   # dorsal emitter dish
    for k in range(6):plate(M,[(-.15,.25,.25-k*.17),(.15,.25,.25-k*.17),(.15,.25,.19-k*.17),(-.15,.25,.19-k*.17)],.005,ACC,.9)
    return M

# ------------------------------------------------------------------ Varkesh Talon: medium fighter (sponsons, claw prow, four drives)
def talon():
    M=Mesh(24)
    loft(M,[(-1.0,HEX(.34,.24)),(-.35,HEX(.4,.28)),(.35,HEX(.36,.26)),(.72,HEX(.24,.17,-.02)),(.95,HEX(.12,.09,-.03))],hex_role)
    plate(M,[(-.09,.27,.5),(.09,.27,.5),(.09,.3,.15),(-.09,.3,.15)],.025,GLASS)
    for sx in (1,-1):
        box(M,(sx*.52,-.02,-.15),(.2,.22,1.15),MID,taper=(.85,.8))                                                   # sponson
        for dy in (.05,-.08):barrel(M,(sx*.52,dy,.4),.42,.03)
        for k,z in enumerate((.25,-.1,-.45)):box(M,(sx*.36,.16,z),(.07,.18,.3),MID,taper=(.9,.85),sh=.96+.03*k)
        for k in range(3):plate(M,[(sx*.18,.06-k*.05,.93),(sx*.12,-.06-k*.05,.93),(sx*.06,-.1-k*.05,1.22-k*.06),(sx*.1,-.02-k*.05,1.24-k*.06)],.045,ACC)   # the claw
        for dy in (.09,-.09):box(M,(sx*.17,dy,-1.07),(.18,.15,.14),DARK);M.vent((sx*.17,dy,-1.14),.06)
        plate(M,[(sx*.3,.28,-.5),(sx*.4,.52,-.8),(sx*.4,.52,-.92),(sx*.3,.28,-.92)],.06,ACC,.9)
    barrel(M,(0,-.25,.3),.55,.04);box(M,(0,-.25,.2),(.16,.11,.26),DARK)
    for z in (-.6,-.15,.3):box(M,(0,.29,z),(.26,.03,.13),ACC,sh=.9)
    return M

# ------------------------------------------------------------------ Varkesh Halberd: heavy fighter (prow blade, dorsal turret, missile racks)
def halberd():
    M=Mesh(25)
    loft(M,[(-1.25,HEX(.38,.3)),(-.5,HEX(.46,.34)),(.45,HEX(.42,.32)),(.9,HEX(.28,.22,-.02)),(1.15,HEX(.14,.12,-.03))],hex_role)
    plate(M,[(-.1,.33,.62),(.1,.33,.62),(.1,.36,.32),(-.1,.36,.32)],.025,GLASS)
    plate(M,[(0,.12,1.1),(0,-.32,1.0),(0,-.42,1.42),(0,-.05,1.5)],.05,ACC)                                          # the halberd blade under the prow
    M.tube([(0,0,1.12),(0,0,1.6)],[.05,.005],6,lambda i,j,n,p:(DARK,1.0))                                            # spike
    box(M,(0,.42,-.1),(.3,.14,.36),DARK);box(M,(0,.52,-.1),(.22,.1,.26),MID)                                       # dorsal turret
    for sx in (1,-1):barrel(M,(sx*.06,.53,.0),.5,.025)
    for sx in (1,-1):
        box(M,(sx*.56,-.05,-.25),(.24,.3,1.35),MID,taper=(.85,.85))                                                  # armour slab
        box(M,(sx*.72,.02,.0),(.12,.2,.5),DARK)                                                                       # missile rack
        for a in range(2):
            for b in range(3):box(M,(sx*.785,-.04+a*.1,.14-b*.14),(.02,.07,.1),ACC,sh=.95)
        for dy in (.05,-.1):barrel(M,(sx*.56,dy,.42),.45,.032)
        for k,z in enumerate((.3,-.05,-.4,-.75)):box(M,(sx*.42,.2,z),(.07,.2,.3),MID,taper=(.9,.85),sh=.96+.02*k)
        for dx in (.13,.33):
            for dy in (.11,-.11):box(M,(sx*dx,dy,-1.32),(.17,.15,.14),DARK);M.vent((sx*dx,dy,-1.39),.06)
        plate(M,[(sx*.4,.32,-.65),(sx*.5,.62,-1.0),(sx*.5,.62,-1.14),(sx*.4,.32,-1.14)],.07,ACC,.9)
    for z in (-.85,-.4,.4):box(M,(0,.35,z),(.3,.03,.14),ACC,sh=.9)
    return M

# ------------------------------------------------------------------ Ostrova Wisp: medium fighter (two halos)
def wisp():
    M=Mesh(38)
    loft(M,[(-1.1,DIA(.06,.06)),(-.7,DIA(.16,.13)),(-.15,DIA(.19,.18)),(.45,DIA(.12,.12)),(1.0,DIA(.04,.04)),(1.18,DIA(.004,.004))],lambda i,j:((LIGHT,1.0) if j in (0,1) else (MID,.92)))
    for zc,R in ((-.2,.5),(-.62,.4)):ring(M,(0,0,zc),R,.035,ACC);ring(M,(0,0,zc),R-.06,.012,WIN,sides=5)
    for k in range(3):
        a=math.pi/2+k*2*math.pi/3;ca,sa=math.cos(a),math.sin(a)
        plate(M,[(ca*.14,sa*.14,.1),(ca*.5,sa*.5,-.15),(ca*.4,sa*.4,-.62),(ca*.12,sa*.12,-.85)],.025,LIGHT,.95)
        plate(M,[(ca*.1,sa*.1,-.7),(ca*.62,sa*.62,-1.05),(ca*.56,sa*.56,-1.16),(ca*.08,sa*.08,-1.06)],.02,MID)
        for zc,R in ((-.2,.5),(-.62,.4)):M.blob((ca*R,sa*R,zc),.055,GLASS,sub=1,squash=(1,1,1.5),noise=0)
        barrel(M,(ca*.18,sa*.18,.2),.36,.018,ACC)
        a2=a+math.pi/3;plate(M,[(math.cos(a2)*.1,math.sin(a2)*.1,-.05),(math.cos(a2)*.3,math.sin(a2)*.3,-.3),(math.cos(a2)*.1,math.sin(a2)*.1,-.5)],.012,WIN,.9)   # crystal panels
    M.blob((0,.13,.35),.08,GLASS,sub=2,squash=(.9,.7,2.0),noise=0)
    M.tube([(0,0,1.05),(0,0,1.5)],[.022,.012],6,lambda i,j,n,p:(LIGHT,.9))
    for z,r in ((1.25,.07),(1.4,.05)):ring(M,(0,0,z),r,.012,ACC,seg=14,sides=5)
    M.vent((0,0,-1.12),.06)
    return M

# ------------------------------------------------------------------ Ostrova Vigil: heavy fighter (three bundled spires, a great halo, sensor dish)
def vigil():
    M=Mesh(39)
    for k in range(3):
        a=math.pi/2+k*2*math.pi/3;dx,dy=math.cos(a)*.17,math.sin(a)*.17
        loft(M,[(-1.15,DIA(.05,.05,dx,dy)),(-.7,DIA(.12,.11,dx,dy)),(-.1,DIA(.14,.14,dx,dy)),(.5,DIA(.09,.09,dx*.7,dy*.7)),(1.05,DIA(.02,.02,dx*.2,dy*.2))],lambda i,j:((LIGHT,1.0) if j in (0,1) else (MID,.92)))
        M.vent((dx,dy,-1.17),.045)
    ring(M,(0,0,-.35),.68,.045,ACC);ring(M,(0,0,-.35),.6,.015,WIN,sides=5);ring(M,(0,0,-.35),.76,.012,ACC,sides=4)
    for k in range(6):
        a=math.pi/2+k*math.pi/3;ca,sa=math.cos(a),math.sin(a)
        M.blob((ca*.68,sa*.68,-.35),.065,GLASS,sub=1,squash=(1,1,1.5),noise=0)
        if k%2==0:
            plate(M,[(ca*.25,sa*.25,0),(ca*.66,sa*.66,-.25),(ca*.66,sa*.66,-.45),(ca*.25,sa*.25,-.85)],.03,LIGHT,.95)
            plate(M,[(ca*.2,sa*.2,-.75),(ca*.8,sa*.8,-1.12),(ca*.74,sa*.74,-1.25),(ca*.18,sa*.18,-1.12)],.025,MID)
            barrel(M,(ca*.3,sa*.3,.25),.42,.022,ACC)
        else:
            plate(M,[(ca*.12,sa*.12,.05),(ca*.42,sa*.42,-.3),(ca*.12,sa*.12,-.65)],.014,WIN,.9)
    M.blob((0,0,.95),.18,MID,sub=2,squash=(1,1,.3),noise=0);ring(M,(0,0,.98),.19,.02,ACC,seg=22,sides=5)            # sensor dish at the prow
    M.blob((0,0,1.02),.07,GLASS,sub=1,noise=0)
    M.tube([(0,0,1.05),(0,0,1.55)],[.025,.012],6,lambda i,j,n,p:(LIGHT,.9))
    for z,r in ((1.3,.08),(1.45,.055)):ring(M,(0,0,z),r,.013,ACC,seg=14,sides=5)
    M.blob((0,.28,.2),.09,GLASS,sub=2,squash=(.9,.7,2.0),noise=0)
    return M

FAMILY=[('halcyon','Halcyon Accord',[('Swift','Light',swift),('Kite','Medium',kite),('Osprey','Heavy',osprey)]),
        ('varkesh','Varkesh Dominion',[('Fang','Light',fang),('Talon','Medium',talon),('Halberd','Heavy',halberd)]),
        ('ostrova','Ostrova Collective',[('Mote','Light',mote),('Wisp','Medium',wisp),('Vigil','Heavy',vigil)])]

DESIGNS=[('halcyon','Swift','Halcyon Accord',swift,['Fast and light, thin hull','Strong shields; emitter nodes on the wingtips','3 weapon slots: twin guns under the canards, one more']),
         ('varkesh','Fang','Varkesh Dominion',fang,['Slow, heavily armoured, wide','Hungry reactor; square twin drives','4 weapon slots: two wing pods and a chin gun']),
         ('ostrova','Mote','Ostrova Collective',mote,['Deep reactor in a glowing halo','Best sensors and lock range; weak shields','3 weapon slots: emitter lances round the spire'])]
