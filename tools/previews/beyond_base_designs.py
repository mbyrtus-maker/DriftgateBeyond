# Driftgate Beyond: base designs for a player company's Depots and Stations (8 Nov 2026; the company profile picks one).
# Looks only: every design has a Depot at levels 1-3 and a Station core with today's five hardpoints (HP_A at radius HP_R,
# height HP_Y), so the six station buildings attach unchanged. Same company style as tools/previews/beyond_stations.py
# (drums, square trusses, containers, radiators, tanks, amber trim, floodlights) and the same units: a Depot spans about
# +-2.5, a Station core about +-5 (the game draws them at BM.K.depot and BM.K.station).
#   Design 1  Company standard   today's by_depot1-3 and by_core (beyond_stations.py, unchanged)
#   Design 2  Wheel              a standing habitat wheel on an axle; the Station's wheel rides on a keel that holds the pads
#   Design 3  Spire              a tall stepped tower with balconies and a needle; the Station's pads hang off a skirt
#   Design 4  Truss cluster      modules bolted into open cube frames, deliberately uneven
#   Design 5  Disc               a flat lens with a lit rim and docking slots, a dome and a keel; the Station's pads ring the rim
#   Design 6  Asteroid           built into a large rock: hab domes, docking arms, lights; the Station's pads on its rim
# Each level adds to the one below: Depot 1 storage; Depot 2 production and a hangar; Depot 3 turrets, armour and a
# life-support ring. SEATS gives each model's turret seats (position, outward normal), packed as the model's 'tp' so the
# game puts its guns on the model. Up is +y.
import math
import numpy as np
from beyond_hulls import Mesh,LIGHT,MID,DARK,ACC,GLASS,GLOW,WIN,box,plate,ring
from beyond_capitals import tube,mouth
from beyond_recon import dish
from beyond_stations import (ry,frame_y,put,outward,drum,truss,tank,container,radiator,floods,mast,collar,turret,pad,Rock,
                             rock_mouth,HP_R,HP_Y,HP_A,ROCK,ROCKD)
PI=math.pi

# ------------------------------------------------------------------ shared pieces
def lathe_y(M,prof,sides,role,caps=True):
    # a surface of revolution about +y through (y, r) pairs; role(i) or a role
    pts=[(0,y,0) for y,_ in prof];rad=[r for _,r in prof]
    rf=role if callable(role) else (lambda i:(role,1.0))
    M.tube(pts,rad,sides,lambda i,j,n,p:(rf(i)[0],rf(i)[1]*(.94+.06*(j%2))),cap0=caps,cap1=caps,up=(0,0,1))
def winband(M,c,R,axis='y',seg=40,r=None):
    # a lit window band: a four-sided ring just proud of a round surface of radius R (shows as a stripe of lit panes)
    ring(M,tuple(c),R*1.005,r or max(.03,R*.03),WIN,seg=seg,sides=4,axis=axis)
def ontoR(M,B,pos,n,hint=(0,1,0)):
    # place a part built facing +y (a turret, a dome) on a surface at pos with outward normal n
    put(M,B,pos,frame_y(n,hint))
def gun(M,pos,n,s=.85):
    B=Mesh();turret(B,(0,0,0),s);ontoR(M,B,pos,n,(0,0,1) if abs(n[1])>.9 else (0,1,0))
def armour(M,c,u,w,h,t=.05,role=LIGHT):
    # a flat armour plate centred on c, its face along normal u, w wide (horizontal) and h tall
    u=np.array(u,float);u/=np.linalg.norm(u);up=np.array([0,1.,0]) if abs(u[1])<.9 else np.array([1.,0,0]);s=np.cross(u,up);s/=np.linalg.norm(s);v=np.cross(s,u)
    c=np.array(c,float);plate(M,[c-s*w/2-v*h/2,c+s*w/2-v*h/2,c+s*w/2+v*h/2,c-s*w/2+v*h/2],t,role,.9)
def hpads(M,start):
    # the five Station hardpoints: a truss from start(a) out to each pad
    for a in HP_A:
        c=np.array([math.cos(a)*HP_R,HP_Y,math.sin(a)*HP_R]);truss(M,start(a),c-[math.cos(a)*.38,0,math.sin(a)*.38],.26,.028);pad(M,c,.4)
def ring_y(M,y,R,r,role=MID,seg=48,sides=10,band=True):
    ring(M,(0,y,0),R,r,role,seg=seg,sides=sides,axis='y')
    if band:ring(M,(0,y,0),R,r*1.03,WIN,seg=seg,sides=4,axis='y')
def u(a):return np.array([math.cos(a),0,math.sin(a)])
SEATS={}
def mast(M,base,h,r=.03):
    # beyond_stations.mast with its halo held on three small spokes (there it floats round the mast)
    b=np.array(base,float);tube(M,[b,b+[0,h,0]],[r,r*.5],LIGHT,.9,5);M.blob(tuple(b+[0,h,0]),r*1.6,WIN,sub=1,noise=0)
    y=b+[0,h*.7,0];ring(M,tuple(y),r*3,r*.4,ACC,seg=12,sides=4,axis='y')
    for a in (0,2*PI/3,4*PI/3):tube(M,[y+u(a)*r*.4,y+u(a)*r*2.75],[r*.22,r*.22],DARK,.9,4,cap0=False,cap1=False)
def container(M,c,size=(.5,.36,.9),role=MID,yaw=0.0):
    # beyond_stations.container with its amber stripe stood clear of the ribs (set at an angle, the two nearly met and flickered)
    B=Mesh();w,h,l=size
    box(B,(0,0,0),size,role)
    for z in np.linspace(-l/2+.04,l/2-.04,4):box(B,(0,0,z),(w*1.04,h*1.04,.03),DARK)
    box(B,(0,h*.18,0),(w*1.1,h*.12,l*.9),ACC)
    put(M,B,c,ry(yaw))

# ================================================================== DESIGN 2: WHEEL
def wheel_depot(level=1):
    # a short axle (+z) carrying a standing habitat wheel, a docking collar at the front and a tank at the back.
    # 1: storage pods on the wheel's lower rim; 2: a production module on the axle behind, a hangar gondola under the wheel;
    # 3: a second, lit life-support wheel, armour round the axle, turrets on the rim
    M=Mesh(320+level);W=1.7;zw=.3
    drum(M,(0,0,-.9),(0,0,.9),.45,MID,14,bands=(.12,.88))
    ring(M,(0,0,zw),W,.2,MID,seg=44,sides=10,axis='z');ring(M,(0,0,zw),W,.205,WIN,seg=44,sides=4,axis='z')
    for k in range(6):
        a=PI/6+k*PI/3;d=np.array([math.cos(a),math.sin(a),0]);truss(M,d*.44+[0,0,zw],d*(W-.17)+[0,0,zw],.16,.02)
    collar(M,(0,0,.9),.26,(0,0,1));tank(M,(0,0,-1.24),.36)
    for a in (PI*7/6,PI*11/6,PI*5/6):                                                                   # storage pods on the rim
        d=np.array([math.cos(a),math.sin(a),0]);B=Mesh();container(B,(0,0,0),(.42,.32,.8),MID);ontoR(M,B,d*(W+.33)+[0,0,zw],d,(0,0,1))
        truss(M,d*(W+.12)+[0,0,zw],d*(W+.2)+[0,0,zw],.12,.016,bays=1)
    mast(M,(0,W+.18,zw),.9,.035)
    floods(M,[np.array([math.cos(a)*W,math.sin(a)*W,zw+.21]) for a in (0,PI/3,2*PI/3,PI)],.045)
    if level>=2:
        truss(M,(0,0,-1.58),(0,0,-2.0),.2,.022)                                                         # production module
        box(M,(0,0,-2.4),(.9,.62,.8),MID);box(M,(0,.33,-2.4),(.5,.06,.5),DARK)
        for sx in (1,-1):radiator(M,(sx*.45,0,-2.4),(sx*1.3,0,-2.4),.45,2)
        floods(M,[(0,0,-2.82)],.05)
        truss(M,(0,-W-.16,zw),(0,-W-.55,zw),.18,.022)                                                   # hangar gondola under the wheel
        B=Mesh();box(B,(0,0,0),(1.3,.62,1.1),MID);mouth(B,(0,-.02,.55),.9,.4,.22);put(M,B,(0,-W-.86,zw))
        floods(M,[(.5,-W-.62,zw+.6),(-.5,-W-.62,zw+.6)],.04)
    if level>=3:
        zl=-.5;Wl=1.35                                                                                   # life-support wheel
        ring(M,(0,0,zl),Wl,.12,MID,seg=40,sides=8,axis='z');ring(M,(0,0,zl),Wl,.125,WIN,seg=40,sides=4,axis='z')
        for k in range(4):a=PI/4+k*PI/2;d=np.array([math.cos(a),math.sin(a),0]);tube(M,[d*.44+[0,0,zl],d*(Wl-.1)+[0,0,zl]],[.04,.04],DARK,.9,5)
        for k in range(6):                                                                                # armour round the axle
            a=k*PI/3;d=np.array([math.cos(a),math.sin(a),0]);s=np.array([-math.sin(a),math.cos(a),0])
            for z0,z1 in ((.42,.86),(-.86,-.62)):plate(M,[d*.47+s*.2+[0,0,z0],d*.47-s*.2+[0,0,z0],d*.47-s*.2+[0,0,z1],d*.47+s*.2+[0,0,z1]],.04,LIGHT,.9)
    for p,n in WHEEL_DSEATS[:3 if level>=3 else 0]:gun(M,p,n)
    return M
_wd=lambda a,r=1.9:(np.array([math.cos(a)*r,math.sin(a)*r,.3]),np.array([math.cos(a),math.sin(a),0]))
WHEEL_DSEATS=[_wd(PI/4),_wd(3*PI/4),_wd(PI/2+.32),_wd(0),_wd(PI),(np.array([0,.36,-1.24]),np.array([0,1.,0]))]
def wheel_core():
    # a big standing wheel on a long axle with docking collars at both ends; a keel drum hangs under the axle and holds the
    # five hardpoints; the wheel's foot rests on the keel; radiators off the keel's back, a mast on the wheel's crown
    M=Mesh(330);C=np.array([0,1.0,0]);W=3.0
    ring(M,C,W,.34,MID,seg=60,sides=12,axis='z');ring(M,C,W,.35,WIN,seg=60,sides=4,axis='z')
    ring(M,C+[0,0,.36],W-.18,.05,ACC,seg=60,sides=4,axis='z');ring(M,C-[0,0,.36],W-.18,.05,ACC,seg=60,sides=4,axis='z')
    drum(M,C+[0,0,-1.5],C+[0,0,1.5],.8,LIGHT,16,bands=(.12,.5,.88))
    for z in (-.85,.85):ring(M,C+[0,0,z],.805,.035,WIN,seg=32,sides=4,axis='z')
    for k in range(8):
        a=PI/8+k*PI/4;d=np.array([math.cos(a),math.sin(a),0]);truss(M,C+d*.78,C+d*(W-.3),.28,.03)
    for s in (1,-1):collar(M,C+[0,0,s*1.5],.36,(0,0,s))
    drum(M,(0,-1.4,0),(0,-.4,0),1.1,MID,16,bands=(.5,));drum(M,(0,-.42,0),(0,.3,0),.5,DARK,12)        # keel and its pylon
    drum(M,(0,-1.75,0),(0,-1.38,0),.32,DARK,10)                                                      # the wheel's foot
    winband(M,(0,-.9,0),1.1)
    for a in (PI*1.35,PI*1.65):tank(M,(math.cos(a)*1.0,-1.55,math.sin(a)*1.0),.4)
    for sx in (1,-1):radiator(M,(sx*.3,-.9,-1.08),(sx*.3,-.9,-2.7),.55,3)
    mast(M,C+[0,W+.32,0],1.3,.05)
    floods(M,[C+np.array([math.cos(a)*W,math.sin(a)*W,.36]) for a in np.linspace(0,2*PI,10,endpoint=False)],.07)
    hpads(M,lambda a:u(a)*1.08+[0,HP_Y,0])
    return M
_wc=lambda a:(np.array([math.cos(a)*3.36,1.0+math.sin(a)*3.36,0]),np.array([math.cos(a),math.sin(a),0]))
WHEEL_CSEATS=[_wc(PI/2-.5),_wc(PI/2+.5),_wc(PI/6),_wc(5*PI/6),_wc(0),_wc(PI),(np.array([0,1.8,1.0]),np.array([0,1.,0])),(np.array([0,1.8,-1.0]),np.array([0,1.,0]))]

# ================================================================== DESIGN 3: SPIRE
def spire_depot(level=1):
    # a tall stepped tower: a storage drum with containers stood round it, a balcony deck, a slim upper shaft and a needle;
    # 2: production modules on the balcony, a hangar pod at the foot; 3: turrets on the balcony, armour on the foot,
    # a life-support ring round the upper shaft
    M=Mesh(340+level)
    tube(M,[(0,-2.3,0),(0,-1.7,0)],[.12,.52],DARK,.95,14)
    drum(M,(0,-1.7,0),(0,-.25,0),.55,MID,14,bands=(.08,.92))
    lathe_y(M,[(-.32,.62),(-.25,.95),(-.16,.95),(-.08,.4)],20,lambda i:(DARK,.9))                     # lower deck
    drum(M,(0,-.2,0),(0,1.3,0),.38,LIGHT,14,bands=(.1,))
    for y in (.3,.8):winband(M,(0,y,0),.38)
    lathe_y(M,[(1.22,.36),(1.3,1.05),(1.4,1.05),(1.48,.3)],24,lambda i:(MID,.95))                     # balcony
    winband(M,(0,1.35,0),1.05,r=.035)
    drum(M,(0,1.45,0),(0,2.4,0),.26,MID,12,bands=(.5,))
    tube(M,[(0,2.4,0),(0,2.75,0)],[.26,.06],DARK,.95,12);mast(M,(0,2.72,0),1.0,.035)
    for a in (PI/3,2*PI/3,PI*1.15,PI*1.85):                                                          # storage stood round the foot
        B=Mesh();container(B,(0,0,0),(.4,.3,.8),MID);put(M,B,u(a)*.69+[0,-1.0,0],frame_y(u(a),(0,1,0)))
    truss(M,(.37,.5,0),(1.55,.5,0),.2,.022);collar(M,(1.55,.5,0),.22,(1,0,0))                        # docking arm
    floods(M,[u(a)*1.05+[0,1.42,0] for a in np.linspace(0,2*PI,6,endpoint=False)+PI/6]+[(1.0,.66,.12),(1.0,.66,-.12)],.04)
    if level>=2:
        for a in (PI/2,PI*7/6,PI*11/6):                                                                  # production on the balcony
            B=Mesh();box(B,(0,.22,0),(.42,.44,.5),MID);box(B,(0,.47,0),(.3,.06,.36),DARK);put(M,B,u(a)*.68+[0,1.38,0],outward(a))
        for a in (PI/2+PI/3,PI*3/2):radiator(M,u(a)*1.02+[0,1.3,0],u(a)*1.02+[0,.1,0],.4,2)
        B=Mesh();box(B,(0,0,0),(1.1,.68,1.0),MID);mouth(B,(0,-.02,.5),.78,.4,.22);put(M,B,(0,-1.25,-1.02),ry(PI))   # hangar pod
        floods(M,[(.42,-.86,-1.55),(-.42,-.86,-1.55)],.04)
    if level>=3:
        for k in range(6):a=k*PI/3+PI/6;armour(M,u(a)*.585+[0,-1.35,0],u(a),.5,.5)
        ring_y(M,2.0,1.0,.09,MID,40,8)
        for a in (0,2*PI/3,4*PI/3):tube(M,[u(a)*.25+[0,2.0,0],u(a)*.92+[0,2.0,0]],[.035,.035],DARK,.9,5)
        for p,n in SPIRE_DSEATS[:3]:gun(M,p,n)
    return M
SPIRE_DSEATS=[(u(a)*.9+[0,1.4,0],np.array([0,1.,0])) for a in (PI/6,PI*5/6,PI*3/2)]+[(np.array([0,-2.3,0]),np.array([0,-1.,0])),(np.array([1.55,.75,0]),np.array([0,1.,0])),(np.array([0,2.42,.2]),np.array([0,1.,0]))]
def spire_core():
    # a tall tower: a skirt deck at hardpoint height holds the five pads; a wide column with window bands; a big balcony with
    # four docking collars on its rim; a slim upper shaft with radiators and a small balcony; a needle with a beacon; below,
    # a keel with tanks tapering to a point
    M=Mesh(350)
    lathe_y(M,[(-1.3,.7),(-1.15,1.75),(-.65,1.75),(-.5,.7)],24,lambda i:(MID,.95));winband(M,(0,-.9,0),1.75,r=.06)
    drum(M,(0,-.55,0),(0,2.55,0),.85,LIGHT,18,bands=(.25,.75))
    for y in (.35,.9,1.45,2.0):winband(M,(0,y,0),.85,seg=36)
    lathe_y(M,[(2.45,.8),(2.6,2.1),(2.9,2.1),(3.05,.6)],28,lambda i:(MID,.95));winband(M,(0,2.75,0),2.1,r=.05)
    for a in (0,PI/2,PI,3*PI/2):collar(M,u(a)*2.05+[0,2.75,0],.22,u(a))
    drum(M,(0,3.0,0),(0,4.85,0),.5,MID,14,bands=(.3,.7))
    for a in (PI/3,PI,5*PI/3):radiator(M,u(a)*.48+[0,3.95,0],u(a)*1.85+[0,3.95,0],.7,3)
    lathe_y(M,[(4.8,.45),(4.88,1.15),(5.06,1.15),(5.14,.4)],22,lambda i:(DARK,.9));winband(M,(0,4.97,0),1.15,r=.03)
    tube(M,[(0,5.1,0),(0,6.6,0)],[.32,.04],LIGHT,.95,10);ring(M,(0,5.9,0),.24,.04,ACC,seg=16,sides=4,axis='y');M.blob((0,6.65,0),.1,WIN,sub=1,noise=0)
    drum(M,(0,-3.0,0),(0,-1.25,0),.62,DARK,14,bands=(.5,))
    tube(M,[(0,-3.0,0),(0,-4.0,0),(0,-4.5,0)],[.62,.25,.05],DARK,.95,14)
    for a in (PI/6,PI*5/6,PI*3/2):tank(M,u(a)*.85+[0,-2.2,0],.42)
    floods(M,[u(a)*2.1+[0,2.95,0] for a in np.linspace(0,2*PI,8,endpoint=False)+PI/4]+[u(a)*1.75+[0,-.62,0] for a in np.array(HP_A)+PI/5],.065)
    hpads(M,lambda a:u(a)*1.72+[0,HP_Y,0])
    return M
SPIRE_CSEATS=[(u(a)*1.8+[0,2.92,0],np.array([0,1.,0])) for a in (PI/4,3*PI/4,5*PI/4,7*PI/4)]+[(u(a)*.95+[0,5.15,0],np.array([0,1.,0])) for a in (PI/2,3*PI/2)]+[(np.array([0,-1.3,1.35]),np.array([0,-1.,0])),(np.array([0,-1.3,-1.35]),np.array([0,-1.,0]))]

# ================================================================== DESIGN 4: TRUSS CLUSTER
def cube_frame(M,c,h,w=.16,r=.022,decks=(),belt=None):
    # an open cube of square trusses, centre c, half-size h; decks: 'top'/'bottom' grating plates; belt: a ring of trusses
    # round the frame at that height
    c=np.array(c,float);P=lambda sx,sy,sz:c+np.array([sx,sy,sz])*h
    for s1 in (-1,1):
        for s2 in (-1,1):
            k=max(2,int(round(2*h/(w*2.6))));truss(M,P(-1,s1,s2),P(1,s1,s2),w,r,k);truss(M,P(s1,-1,s2),P(s1,1,s2),w,r,k);truss(M,P(s1,s2,-1),P(s1,s2,1),w,r,k)
    for sx in (-1,1):
        for sy in (-1,1):
            for sz in (-1,1):box(M,tuple(P(sx,sy,sz)),(w*1.25,w*1.25,w*1.25),DARK)
    for d in decks:
        y=c[1]+(h if d=='top' else -h)+(w/2+.02 if d=='top' else -w/2-.02)
        plate(M,[(c[0]-h,y,c[2]-h),(c[0]+h,y,c[2]-h),(c[0]+h,y,c[2]+h),(c[0]-h,y,c[2]+h)],.04,DARK,.85)
    if belt is not None:
        for (x0,z0),(x1,z1) in (((-1,-1),(1,-1)),((1,-1),(1,1)),((1,1),(-1,1)),((-1,1),(-1,-1))):truss(M,c+[x0*h,belt-c[1],z0*h],c+[x1*h,belt-c[1],z1*h],w*.9,r)
def cluster_depot(level=1):
    # a cube frame round a hab drum, a grating deck on top with containers, a tank and a utility box on two corners, a
    # docking collar out on a truss; 2: a production module out on the -x side, a hangar hung under the frame;
    # 3: turrets on the top corners, armour on the hab, a ring of life-support pods round the frame
    M=Mesh(360+level);h=1.0
    cube_frame(M,(0,0,0),h,decks=('top',))
    drum(M,(0,-.65,0),(0,.65,0),.5,MID,14,bands=(.15,.85));winband(M,(0,0,0),.5,seg=28)
    for sx,sz in ((1,1),(-1,1),(1,-1),(-1,-1)):tube(M,[(sx*.35,.3,sz*.35),(sx*h,.3,sz*h)],[.035,.035],DARK,.9,5)
    tube(M,[(0,.64,0),(0,h,0)],[.12,.12],DARK,.9,8)
    yt=h+.1
    for x,z,yaw in ((-.45,-.1,0),(.05,-.1,0),(.55,.45,PI/2)):container(M,(x,yt+.16,z),(.42,.32,.8),MID,yaw)
    container(M,(-.2,yt+.48,-.1),(.42,.32,.8),LIGHT)
    tank(M,(h,h,-h),.4);B=Mesh();box(B,(0,0,0),(.62,.52,.62),MID);box(B,(0,.3,0),(.4,.06,.4),DARK);put(M,B,(-h,-h,h))
    truss(M,(.5,0,0),(1.85,0,0),.2,.022);collar(M,(1.85,0,0),.22,(1,0,0))
    radiator(M,(h,-h,h),(h+.9,-h-.6,h+.3),.4,2)
    mast(M,(-h,h+.08,-h),.9,.03)
    floods(M,[(h,h+.06,h),(-h,h+.06,h),(h,-h-.06,-h),(1.3,.16,.12),(1.3,.16,-.12)],.045)
    if level>=2:
        truss(M,(-.5,0,0),(-1.5,0,0),.2,.022)                                                           # production module
        box(M,(-1.95,0,0),(.9,.7,.95),MID);box(M,(-1.95,.38,0),(.55,.06,.6),DARK);floods(M,[(-2.42,0,0)],.05)
        for sz in (1,-1):radiator(M,(-1.95,0,sz*.48),(-1.95,0,sz*1.3),.45,2)
        B=Mesh();box(B,(0,0,0),(1.4,.6,2.08),MID);mouth(B,(0,-.02,1.04),1.0,.38,.22);put(M,B,(0,-h-.38,0))   # hangar under the frame
        floods(M,[(.6,-h-.66,1.1),(-.6,-h-.66,1.1)],.04)
    if level>=3:
        for k in range(4):a=PI/4+k*PI/2;armour(M,u(a)*.53+[0,-.3,0],u(a),.42,.5)
        ring_y(M,.6,1.85,.07,DARK,48,6,band=False)
        for a in np.linspace(0,2*PI,8,endpoint=False)+PI/8:M.blob(tuple(u(a)*1.85+[0,.6,0]),.2,LIGHT,sub=2,noise=0);ring(M,tuple(u(a)*1.85+[0,.6,0]),.2,.025,WIN,seg=16,sides=4,axis='y')
        for a in (PI/4,3*PI/4,5*PI/4,7*PI/4):tube(M,[u(a)*1.4+[0,.6,0],u(a)*1.82+[0,.6,0]],[.04,.04],DARK,.9,5)
        for p,n in CLUSTER_DSEATS[:3]:gun(M,p,n)
    return M
CLUSTER_DSEATS=[(np.array([1.0,1.08,1.0]),np.array([0,1.,0])),(np.array([-1.0,1.08,1.0]),np.array([0,1.,0])),(np.array([-1.0,1.48,-1.0]),np.array([0,1.,0])),
               (np.array([1.0,-1.08,-1.0]),np.array([0,-1.,0])),(np.array([1.85,.22,0]),np.array([0,1.,0])),(np.array([-1.0,-.72,1.0]),np.array([0,1.,0]))]
CH=1.85
def cluster_core():
    # three cube frames stacked off-centre round a spine: the main frame holds a long hab drum and a truss belt at hardpoint
    # height (the pads hang off it); a smaller frame on its deck carries a big module, radiators and the mast; a third hangs
    # below with tanks. Containers, spheres and docking collars on trusses, nothing quite symmetric.
    M=Mesh(370);h=CH;c0=np.array([0,-.2,0])
    cube_frame(M,c0,h,.26,.03,decks=('top','bottom'),belt=HP_Y)
    drum(M,(-h,.15,0),(h,.15,0),.72,LIGHT,16,bands=(.1,.5,.9))
    B=Mesh();winband(B,(0,0,0),.72,'y',32);put(M,B,(-.75,.15,0),frame_y((1,0,0)));B=Mesh();winband(B,(0,0,0),.72,'y',32);put(M,B,(.75,.15,0),frame_y((1,0,0)))
    truss(M,(0,c0[1]-h,0),(0,c0[1]+h,0),.3,.03)
    yt=c0[1]+h+.17                                                                                       # the deck: containers
    for x,z in ((-1.0,.75),(-.45,.75),(-1.0,-.1)):container(M,(x,yt+.2,z),(.5,.4,.95),MID)
    container(M,(-.72,yt+.6,.75),(.5,.4,.95),LIGHT)
    c1=np.array([.55,yt+.95,-.55]);cube_frame(M,c1,.9,.2,.025)                                          # upper frame and its module
    box(M,tuple(c1+[0,-.235,0]),(1.25,1.47,1.25),MID);box(M,tuple(c1+[0,.53,0]),(.8,.08,.8),DARK)
    for k in range(3):plate(M,[c1+[-.5,.2-k*.28,.635],c1+[.5,.2-k*.28,.635],c1+[.5,.25-k*.28,.635],c1+[-.5,.25-k*.28,.635]],.01,WIN,1.0)
    for sx in (1,-1):radiator(M,c1+[sx*.6,.3,0],c1+[sx*2.4,.55,0],.7,3)
    mast(M,c1+[-.9,.9,-.9],1.4,.045)
    c2=np.array([-.5,c0[1]-h-.9,.4]);cube_frame(M,c2,.75,.2,.025)                                        # lower frame and tanks
    tank(M,c2,.6);tube(M,[c2+[0,.5,0],c2+[0,.8,0]],[.14,.14],DARK,.9,8)
    tank(M,c2+[.75,-.75,-.75],.38);tank(M,(h,c0[1]-h,-h),.55);tank(M,(-h,c0[1]+h,-h),.5)
    for z,s in ((h+.1,1),(-h-.1,-1)):truss(M,(.4,.15,s*.6),(.4,.15,z+s*1.0),.24,.026);collar(M,(.4,.15,z+s*1.0),.3,(0,0,s))
    floods(M,[c0+np.array([sx*h,h+.1,sz*h]) for sx in (-1,1) for sz in (-1,1)]+[c1+[.9,.95,.9],c2+[-.75,-.82,.75]],.07)
    def st(a):
        d=u(a);t=h/max(abs(d[0]),abs(d[2]));return d*t+[0,HP_Y,0]
    hpads(M,st)
    return M
_U,_D=np.array([0,1.,0]),np.array([0,-1.,0]);_c1=np.array([.55,CH-.2+.17+.95,-.55]);_c2=np.array([-.5,-.2-CH-.9,.4])
CLUSTER_CSEATS=[(np.array([CH,CH-.2+.17,CH]),_U),(np.array([-CH,CH-.2+.17,-.25]),_U),(np.array([CH,CH-.2+.17,-CH]),_U),
               (_c1+[-.9,1.0,.9],_U),(_c1+[.9,1.0,.9],_U),(_c2+[-.75,-.88,.75],_D),(np.array([CH,-.2-CH-.17,CH]),_D),(np.array([-CH,-.2-CH-.17,-CH]),_D)]

# ================================================================== DESIGN 5: DISC
DISC_D=[(-.36,.0),(-.36,.72),(-.3,1.2),(-.14,1.66),(0,1.8),(.14,1.66),(.2,1.4),(.22,.9),(.22,0)]
def disc_depot(level=1):
    # a flat lens with a lit rim, a dome on top and a keel cone below; a docking collar in the rim; containers round the dome
    # 2: a production drum under the lens with radiators, a hangar slot in the rim; 3: turrets on the deck, armour on the rim,
    # a raised life-support ring over the deck on posts
    M=Mesh(380+level)
    lathe_y(M,DISC_D,28,lambda i:((MID,.92) if i<4 else (LIGHT,1.0)));winband(M,(0,0,0),1.8,r=.05,seg=56)
    M.blob((0,.22,0),.66,LIGHT,sub=2,squash=(1,.55,1),noise=0);M.blob((0,.56,0),.24,GLASS,sub=2,squash=(1,.6,1),noise=0)
    ring(M,(0,.24,0),.68,.035,ACC,seg=28,sides=4,axis='y');mast(M,(0,.66,0),.9,.03)
    tube(M,[(0,-.36,0),(0,-.85,0),(0,-1.05,0)],[.72,.3,.08],DARK,.95,16)
    collar(M,(1.72,0,0),.13,(1,0,0))
    for a in (PI/4,3*PI/4,5*PI/4):container(M,u(a)*1.1+[0,.38,0],(.36,.3,.62),MID,PI/2-a+PI/2)
    floods(M,[u(a)*1.72+[0,.08,0] for a in np.linspace(0,2*PI,8,endpoint=False)+PI/8],.04)
    if level>=2:
        drum(M,(0,-.7,0),(0,-.32,0),1.0,MID,18,bands=(.5,))                                            # production deck under the lens
        for a in (PI/2,PI*7/6,PI*11/6):radiator(M,u(a)*1.0+[0,-.55,0],u(a)*1.9+[0,-.55,0],.3,2)
        B=Mesh();mouth(B,(0,0,0),.8,.17,.5);put(M,B,(-1.77,0,0),outward(PI))                           # hangar slot in the rim
        floods(M,[u(PI+.32)*1.7+[0,.1,0],u(PI-.32)*1.7+[0,.1,0]],.04)
    if level>=3:
        for k in range(10):
            a=k*PI/5+PI/10
            if abs(((a-PI+PI)%(2*PI))-PI)<.4 or abs(((a+PI)%(2*PI))-PI)<.3:continue
            d=u(a);s=np.array([-d[2],0,d[0]]);plate(M,[d*1.74+s*.3+[0,-.12,0],d*1.74-s*.3+[0,-.12,0],d*1.52-s*.25+[0,-.28,0],d*1.52+s*.25+[0,-.28,0]],.04,LIGHT,.9)
        ring_y(M,.62,1.45,.08,MID,48,8)
        for a in np.linspace(0,2*PI,6,endpoint=False):tube(M,[u(a)*1.45+[0,.16,0],u(a)*1.45+[0,.6,0]],[.035,.035],DARK,.9,5)
        for p,n in DISC_DSEATS[:3]:gun(M,p,n)
    return M
DISC_DSEATS=[(u(a)*1.1+[0,.23,0],np.array([0,1.,0])) for a in (0,PI*2/3+.3,PI*4/3-.3)]+[(np.array([0,-1.05,0]),np.array([0,-1.,0])),(u(PI/2)*1.3+[0,-.27,0],np.array([0,-1.,0])),(u(3*PI/2)*1.3+[0,-.27,0],np.array([0,-1.,0]))]
DISC_C=[(-1.25,.0),(-1.25,1.2),(-1.05,2.2),(-.7,3.2),(-.4,3.55),(-.2,3.85),(0,3.55),(.12,3.1),(.2,1.8),(.22,0)]
def disc_core():
    # a broad lens with a lit rim and five docking slots between the hardpoints; an upper tier with its own window band; a
    # tower, dome and mast on top; a keel drum and cone with tanks below. The pads sit just out from the rim.
    M=Mesh(390);y0=-.75
    B=Mesh();lathe_y(B,DISC_C,40,lambda i:((MID,.92) if i<5 else (LIGHT,1.0)));put(M,B,(0,y0,0))
    winband(M,(0,y0-.2,0),3.85,r=.07,seg=72)
    for a in np.array(HP_A)+PI/5:B=Mesh();mouth(B,(0,0,0),.95,.24,.6);put(M,B,u(a)*3.79+[0,y0-.2,0],outward(a))
    drum(M,(0,y0+.15,0),(0,.45,0),1.25,MID,18);lathe_y(M,[(.3,1.2),(.42,2.1),(.62,2.1),(.75,1.0)],32,lambda i:(LIGHT,.95))
    winband(M,(0,.52,0),2.1,r=.05,seg=48)
    drum(M,(0,.7,0),(0,1.75,0),.62,MID,16,bands=(.3,.7));M.blob((0,1.75,0),.62,LIGHT,sub=2,squash=(1,.5,1),noise=0)
    M.blob((0,2.08,0),.24,GLASS,sub=2,squash=(1,.7,1),noise=0);mast(M,(0,2.22,0),1.2,.045)
    for a in (PI/2+PI/5,PI*1.5+PI/5):radiator(M,u(a)*.6+[0,1.25,0],u(a)*1.9+[0,1.35,0],.55,2)
    drum(M,(0,-2.4,0),(0,y0-1.1,0),1.0,DARK,16,bands=(.5,));tube(M,[(0,-2.4,0),(0,-3.0,0),(0,-3.25,0)],[1.0,.4,.08],DARK,.95,16)
    for a in (PI/6,PI*5/6,PI*3/2):tank(M,u(a)*1.22+[0,-2.0,0],.45)
    floods(M,[u(a)*3.5+[0,y0+.18,0] for a in np.linspace(0,2*PI,10,endpoint=False)]+[u(a)*2.05+[0,.68,0] for a in np.linspace(0,2*PI,6,endpoint=False)],.065)
    hpads(M,lambda a:u(a)*3.6+[0,HP_Y,0])
    return M
DISC_CSEATS=[(u(a)*1.85+[0,.75,0],np.array([0,1.,0])) for a in np.array(HP_A)+PI/5]+[(u(a)*3.0+[0,-.32,0],np.array([0,1.,0])) for a in (PI/2,PI*1.5+.3)]+[(np.array([0,-3.25,0]),np.array([0,-1.,0]))]

# ================================================================== DESIGN 6: ASTEROID
def asteroid_depot(level=1):
    # a large rock with a glass hab dome on top, a docking arm, a container stash clamped to its flank, lights and a mast;
    # 2: a production module with radiators on the far side, a hangar cut into the rock; 3: turrets on the rock, armour
    # bolted over its face, a life-support ring round its waist on four struts
    M=Mesh(400+level);rk=Rock((0,0,0),1.4,61,squash=(1.18,.86,1.0));rk.build(M,3)
    p=rk.surf((.1,1,.1),.12);M.blob(tuple(p),.62,GLASS,sub=2,squash=(1,.62,1),noise=0);ring(M,tuple(p+[0,.02,0]),.62,.05,ACC,seg=28,sides=4,axis='y')
    p2=rk.surf((-.55,.8,.45),.08);M.blob(tuple(p2),.34,LIGHT,sub=2,squash=(1,.7,1),noise=0);ring(M,tuple(p2+[0,.02,0]),.34,.03,WIN,seg=20,sides=4,axis='y')
    a0=rk.surf((1,.25,0),.2);truss(M,a0,(2.55,.42,0),.2,.022);collar(M,(2.55,.42,0),.22,(1,0,0));floods(M,[(2.0,.52,.1),(2.0,.52,-.1)],.04)
    dd=np.array([-.6,-.1,-1.]);dd/=np.linalg.norm(dd);B=Mesh()                                          # container stash on a clamp frame
    for x in (-.3,.3):container(B,(x,.33,0),(.48,.34,.86),MID)
    container(B,(0,.69,0),(.48,.34,.86),LIGHT);truss(B,(-.65,.1,-.45),(.65,.1,-.45),.12,.018);truss(B,(-.65,.1,.45),(.65,.1,.45),.12,.018)
    put(M,B,rk.surf(dd,.12),frame_y(dd,(1,0,0)))
    pm=rk.surf((.45,.9,-.4),.05);mast(M,pm,1.0,.03)
    floods(M,[rk.surf(d,.03) for d in ((1,.6,.6),(.3,-.2,1),(-1,.1,.4),(.2,-1,-.2))],.05)
    if level>=2:
        dd=np.array([-1.,.25,.2]);dd/=np.linalg.norm(dd);B=Mesh()                                        # production module
        box(B,(0,.3,0),(.8,.6,.9),MID);box(B,(0,.63,0),(.5,.06,.5),DARK)
        for sz in (1,-1):radiator(B,(0,.3,sz*.45),(0,.5,sz*1.2),.4,2)
        put(M,B,rk.surf(dd,.12),frame_y(dd,(0,1,0)))
        rock_mouth(M,rk,np.array([.35,-.35,1.]),.85,.45)
    if level>=3:
        for d in ((.9,.2,.9),(-.2,.15,1.),(.95,-.35,-.6)):                                                 # armour bolted over the face
            d=np.array(d,float);d/=np.linalg.norm(d);armour(M,rk.surf(d,-.01),d,.6,.45,.06)
        ring_y(M,-.15,2.15,.1,MID,52,8)
        for a in (PI/4,3*PI/4,5*PI/4,7*PI/4):d=u(a)+[0,-.1,0];tube(M,[rk.surf(d,.15)+[0,-.02,0],u(a)*2.07+[0,-.15,0]],[.045,.045],DARK,.9,5)
        for p,n in AST_DSEATS[:3]:gun(M,p,n)
    return M
_RK_D=Rock((0,0,0),1.4,61,squash=(1.18,.86,1.0))
def _rs(rk,d,ins=.06):
    d=np.array(d,float);d/=np.linalg.norm(d);p=rk.surf(d,ins);return (p,d)
AST_DSEATS=[_rs(_RK_D,d) for d in ((.75,.5,.6),(.35,.55,-.9),(.5,-.9,-.3),(-.7,-.8,.3),(.15,.45,1),(-.85,.15,.8))]
_RK_C=Rock((0,0,0),3.3,41,squash=(1.1,.8,1.05))
def asteroid_core():
    # a big rock: a crown dock rising from its top, glass hab domes in clusters, two docking arms with collars, hangars cut
    # into its flanks, radiators, a keel drum below; the five pads stand out from its rim on trusses
    M=Mesh(410);rk=_RK_C;rk.build(M,3)
    top=rk.surf((0,1,0),.2);bot=rk.surf((0,-1,0),.2)
    drum(M,top,top+[0,1.0,0],.85,MID,16,bands=(.5,));drum(M,top+[0,1.0,0],top+[0,1.5,0],1.0,DARK,16)
    for a in np.linspace(0,2*PI,4,endpoint=False):collar(M,top+[math.cos(a)*.95,1.25,math.sin(a)*.95],.2,(math.cos(a),0,math.sin(a)))
    mast(M,top+[0,1.5,0],1.6,.05)
    drum(M,bot,bot-[0,.8,0],.6,MID,14);tube(M,[bot-[0,.8,0],bot-[0,1.2,0]],[.6,.12],DARK,.95,14)
    for d in ((1,-.1,.2),(-.8,-.15,.7),(.1,-.1,-1)):rock_mouth(M,rk,np.array(d),1.3,.7)
    for d,r in (((.55,.8,.45),.85),((.9,.55,.1),.5),((-.6,.75,-.3),.75),((-.3,.8,-.8),.45),((-.15,.85,.75),.55)):
        p=rk.surf(d,-.02);M.blob(tuple(p),r,GLASS,sub=2,squash=(1,.6,1),noise=0);ring(M,tuple(p+[0,.02,0]),r,.04,ACC,seg=24,sides=4,axis='y')
    for a,yv in ((PI*.3,.25),(PI*1.3,.3)):                                                               # docking arms
        d=u(a)+[0,yv,0];p=rk.surf(d,.3);e=u(a)*4.7+[0,1.0,0];truss(M,p,e,.26,.028);collar(M,e,.3,u(a))
        floods(M,[e-u(a)*.6+[0,.15,0]],.06)
    p=rk.surf((-.2,1,.6),.05);radiator(M,p,p+[-1.6,.4,.6],.6,3)
    p=rk.surf((.4,.9,-.7),.05);radiator(M,p,p+[1.2,.5,-1.2],.6,3)
    floods(M,[rk.surf(d,.04) for d in ((1,.5,-.5),(-1,.4,-.2),(.3,.3,1),(.7,-.5,.8),(-.6,-.5,-.9),(0,.2,-1),(-1,-.2,.6))],.08)
    def st(a):
        d=np.array([math.cos(a),HP_Y/HP_R*.6,math.sin(a)]);return rk.surf(d,.3)
    hpads(M,st)
    return M
AST_CSEATS=[_rs(_RK_C,d,.08) for d in ((.3,.85,-.4),(-.8,.6,.3),(.7,.6,-.5),(.2,.7,.95),(-.3,-.9,.5),(.6,-.85,-.3),(-.4,.9,.2),(1,.1,-.5))]

# ------------------------------------------------------------------ the families
DESIGNS=[(2,'Wheel','a standing habitat wheel on an axle',wheel_depot,wheel_core,WHEEL_DSEATS,WHEEL_CSEATS),
         (3,'Spire','a tall stepped tower with balconies and a needle',spire_depot,spire_core,SPIRE_DSEATS,SPIRE_CSEATS),
         (4,'Truss cluster','modules bolted into open cube frames',cluster_depot,cluster_core,CLUSTER_DSEATS,CLUSTER_CSEATS),
         (5,'Disc','a flat lens with a lit rim and docking slots',disc_depot,disc_core,DISC_DSEATS,DISC_CSEATS),
         (6,'Asteroid','built into a large rock: domes, docking arms, lights',asteroid_depot,asteroid_core,AST_DSEATS,AST_CSEATS)]
def models():
    # name -> (builder, turret seats) for the model pack
    out={}
    for n,_,_,dep,core,ds,cs in DESIGNS:
        for lv in (1,2,3):out['by_d%d_depot%d'%(n,lv)]=((lambda f,l:lambda:f(l))(dep,lv),[p for p,_ in ds])
        out['by_d%d_core'%n]=(core,[p for p,_ in cs])
    return out
