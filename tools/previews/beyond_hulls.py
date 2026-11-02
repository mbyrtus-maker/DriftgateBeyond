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

DESIGNS=[('halcyon','Swift','Halcyon Accord',swift,['Fast and light, thin hull','Strong shields; emitter nodes on the wingtips','3 weapon slots: twin guns under the canards, one more']),
         ('varkesh','Fang','Varkesh Dominion',fang,['Slow, heavily armoured, wide','Hungry reactor; square twin drives','4 weapon slots: two wing pods and a chin gun']),
         ('ostrova','Mote','Ostrova Collective',mote,['Deep reactor in a glowing halo','Best sensors and lock range; weak shields','3 weapon slots: emitter lances round the spire'])]
