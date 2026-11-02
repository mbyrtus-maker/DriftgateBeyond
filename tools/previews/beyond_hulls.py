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

# ------------------------------------------------------------------ Varkesh Talon: medium fighter (a pincer: two claw sponsons reach past a short cockpit pod)
def talon():
    M=Mesh(24)
    loft(M,[(-.75,HEX(.24,.2)),(-.2,HEX(.28,.23)),(.3,HEX(.24,.2)),(.55,HEX(.14,.12,-.02))],hex_role)              # short cockpit pod
    plate(M,[(-.08,.22,.42),(.08,.22,.42),(.08,.25,.08),(-.08,.25,.08)],.025,GLASS)
    box(M,(0,0,-.92),(1.3,.3,.34),DARK,taper=(.92,.9))                                                             # wide drive block
    for sx in (1,-1):
        loft(M,[(-.85,HEX(.15,.17,0,sx*.62)),(-.1,HEX(.17,.19,0,sx*.64)),(.75,HEX(.13,.15,-.01,sx*.6)),(1.15,HEX(.07,.08,-.02,sx*.5))],hex_role)  # claw sponson
        plate(M,[(sx*.47,.1,1.05),(sx*.53,-.1,1.05),(sx*.3,-.06,1.32),(sx*.27,.05,1.3)],.06,ACC)                      # claw tip curling inward
        plate(M,[(sx*.22,-.02,.25),(sx*.5,-.03,.45),(sx*.5,-.03,-.6),(sx*.22,-.02,-.6)],.06,DARK)                   # slab joining pod and sponson
        for dy in (.07,-.07):barrel(M,(sx*.72,dy,.55),.5,.03)
        for k,z in enumerate((.45,.05,-.35)):box(M,(sx*.79,.06,z),(.05,.2,.3),MID,taper=(.9,.85),sh=.96+.03*k)
        for dx in (.22,.48):box(M,(sx*dx,0,-1.12),(.2,.18,.12),DARK);M.vent((sx*dx,0,-1.18),.065)
        plate(M,[(sx*.62,.18,-.45),(sx*.66,.48,-.75),(sx*.66,.48,-.86),(sx*.62,.18,-.86)],.06,ACC,.9)
    for z in (-.45,.05):box(M,(0,.24,z),(.2,.03,.12),ACC,sh=.9)
    return M

# ------------------------------------------------------------------ Varkesh Halberd: heavy fighter (a brawler: an armoured core with four gun-and-drive pods on an X of slab arms)
def halberd():
    M=Mesh(25)
    loft(M,[(-1.0,HEX(.32,.3)),(-.4,HEX(.38,.36)),(.35,HEX(.34,.32)),(.75,HEX(.22,.2,-.02)),(.95,HEX(.1,.1,-.03))],hex_role)   # armoured core
    plate(M,[(-.1,.33,.55),(.1,.33,.55),(.1,.37,.2),(-.1,.37,.2)],.025,GLASS)
    plate(M,[(-.3,.18,.82),(.3,.18,.82),(.22,-.2,1.02),(-.22,-.2,1.02)],.07,ACC)                                       # ram plate across the prow
    for z in (-.55,-.1,.3):box(M,(0,.37,z),(.3,.03,.14),ACC,sh=.9)
    for sx in (1,-1):
        for sy in (1,-1):
            px,py=sx*.78,sy*.5
            plate(M,[(sx*.25,sy*.15,.25),(px*.95,py*.95,.05),(px*.95,py*.95,-.55),(sx*.25,sy*.15,-.75)],.07,DARK if sy<0 else MID)   # slab arm
            box(M,(px,py,-.15),(.22,.22,1.1),MID,taper=(.8,.8))                                                  # pod
            box(M,(px,py,.38),(.16,.16,.12),ACC,sh=.95)
            barrel(M,(px,py,.42),.45,.034)                                                                         # gun out of each pod
            box(M,(px,py,-.75),(.2,.2,.14),DARK);M.vent((px,py,-.82),.07)                                         # drive at the back of each pod
            for k in range(3):box(M,(px+sx*.12,py,.1-k*.25),(.03,.18,.18),DARK,sh=.95)                              # armour ribs on the pod
    box(M,(0,-.38,.0),(.22,.12,.4),DARK);barrel(M,(0,-.4,.2),.5,.03)                                                 # ventral gun
    return M

# ------------------------------------------------------------------ Ostrova Wisp: medium fighter (a crescent on rods)
def arc(M,c,R,r,role,a0,a1,seg=16,sides=6):
    c=np.array(c,float);pts=[]
    for k in range(seg+1):
        a=a0+(a1-a0)*k/seg;pts.append(c+[math.cos(a)*R,0,math.sin(a)*R])
    M.tube(pts,[r*(.6+.4*math.sin(math.pi*k/seg)) for k in range(seg+1)],sides,lambda i,j,n,p:(role,1.0),cap0=True,cap1=True)
    return pts
def wisp():
    M=Mesh(38)
    loft(M,[(-.9,DIA(.06,.06)),(-.55,DIA(.15,.12)),(-.05,DIA(.17,.16)),(.45,DIA(.1,.1)),(.95,DIA(.035,.035)),(1.1,DIA(.004,.004))],lambda i,j:((LIGHT,1.0) if j in (0,1) else (MID,.92)))
    for sx in (1,-1):
        a0,a1=(-1.25,1.05) if sx>0 else (math.pi-1.05,math.pi+1.25)
        pts=arc(M,(0,0,-.25),.78,.045,ACC,a0,a1)
        for k in (2,8,14):                                                                                       # rods from the spire to the crescent
            p=pts[k];base=np.array([sx*.08,0,p[2]*.6-.05])
            M.tube([base,(base+p)/2,p],[.016,.013,.016],6,lambda i,j,n,q:(LIGHT,.9),cap0=False,cap1=False)
            M.blob(tuple(p),.035,WIN,sub=1,noise=0)
        for p in (pts[0],pts[-1]):M.blob(tuple(p),.06,GLASS,sub=1,squash=(1,1,1.4),noise=0)
        barrel(M,tuple(pts[-1]+[0,0,.02]),.3,.016,ACC)
    for sy in (1,-1):plate(M,[(0,sy*.1,-.5),(0,sy*.42,-.85),(0,sy*.38,-.95),(0,sy*.08,-.9)],.02,MID)
    M.blob((0,.12,.32),.075,GLASS,sub=2,squash=(.9,.7,2.0),noise=0)
    M.tube([(0,0,1.0),(0,0,1.42)],[.02,.012],6,lambda i,j,n,p:(LIGHT,.9))
    for z,r in ((1.2,.065),(1.34,.045)):ring(M,(0,0,z),r,.011,ACC,seg=14,sides=5)
    M.vent((0,0,-.92),.055)
    return M

# ------------------------------------------------------------------ Ostrova Vigil: heavy fighter (a reliquary: a great faceted crystal held by three parallel spires and three halos)
def vigil():
    M=Mesh(39)
    star=lambda w,h:[(math.cos(a)*(w if k%2==0 else w*.62),math.sin(a)*(h if k%2==0 else h*.62)) for k,a in enumerate(np.linspace(0,2*math.pi,12,endpoint=False))]
    loft(M,[(-.85,star(.03,.03)),(-.55,star(.2,.2)),(.1,star(.24,.24)),(.6,star(.14,.14)),(.85,star(.02,.02))],lambda i,j:((GLASS,1.0) if j%2 else (WIN,.8)))   # the crystal
    M.blob((0,0,-.1),.13,WIN,sub=2,squash=(1,1,2.4),noise=0)
    R=.46
    for k in range(3):
        a=math.pi/2+k*2*math.pi/3;dx,dy=math.cos(a)*R,math.sin(a)*R
        loft(M,[(-1.25,DIA(.04,.04,dx,dy)),(-.95,DIA(.11,.11,dx,dy)),(.5,DIA(.1,.1,dx,dy)),(1.2,DIA(.01,.01,dx,dy))],lambda i,j:((LIGHT,1.0) if j in (0,1) else (MID,.92)))   # parallel spires, prongs forward
        M.vent((dx,dy,-1.27),.04)
        plate(M,[(dx,dy,-.7),(dx*1.75,dy*1.75,-1.0),(dx*1.65,dy*1.65,-1.12),(dx,dy,-1.08)],.025,MID)                    # outer fins
        barrel(M,(dx*1.08,dy*1.08,.3),.45,.02,ACC)
        for z in (-.5,.15):                                                                                        # struts from spire to crystal
            M.tube([(dx,dy,z),(dx*.3,dy*.3,z+.05)],[.014,.014],5,lambda i,j,n,p:(LIGHT,.9),cap0=False,cap1=False)
    for z in (-.85,-.15,.55):ring(M,(0,0,z),R,.03,ACC,seg=30,sides=6)                                               # three halos binding the spires
    ring(M,(0,0,-.15),R+.08,.01,WIN,seg=30,sides=4)
    M.blob((0,R+.12,-.15),.11,MID,sub=2,squash=(1,.35,1),noise=0);ring(M,(0,R+.16,-.15),.11,.015,ACC,seg=18,sides=5,axis='y')   # sensor dish on the top halo
    M.tube([(0,0,.85),(0,0,1.45)],[.022,.01],6,lambda i,j,n,p:(LIGHT,.9))
    for z,r in ((1.2,.075),(1.36,.05)):ring(M,(0,0,z),r,.012,ACC,seg=14,sides=5)
    return M

FAMILY=[('halcyon','Halcyon Accord',[('Swift','Light',swift),('Kite','Medium',kite),('Osprey','Heavy',osprey)]),
        ('varkesh','Varkesh Dominion',[('Fang','Light',fang),('Talon','Medium',talon),('Halberd','Heavy',halberd)]),
        ('ostrova','Ostrova Collective',[('Mote','Light',mote),('Wisp','Medium',wisp),('Vigil','Heavy',vigil)])]

DESIGNS=[('halcyon','Swift','Halcyon Accord',swift,['Fast and light, thin hull','Strong shields; emitter nodes on the wingtips','3 weapon slots: twin guns under the canards, one more']),
         ('varkesh','Fang','Varkesh Dominion',fang,['Slow, heavily armoured, wide','Hungry reactor; square twin drives','4 weapon slots: two wing pods and a chin gun']),
         ('ostrova','Mote','Ostrova Collective',mote,['Deep reactor in a glowing halo','Best sensors and lock range; weak shields','3 weapon slots: emitter lances round the spire'])]
