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
                             rock_mouth,HP_R,HP_Y,HP_A,ROCK,ROCKD,depot as BS_depot,station_core as BS_core)
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
    return M
def wheel_core():
    # (10 Nov 2026) twin habitat wheels on a long axle, a lit command sphere between them, docking collars at both axle ends;
    # a keel drum under the sphere holds the five hardpoints; tanks and radiators off the keel, a mast on the sphere's crown.
    # (The Depot is one small wheel; the Station reads as two big wheels round a command hub.)
    M=Mesh(330);C=np.array([0,1.0,0]);W=3.0;ZW=1.25;ZA=2.6
    for zw in (ZW,-ZW):
        c=C+[0,0,zw]
        ring(M,c,W,.3,MID,seg=60,sides=12,axis='z');ring(M,c,W,.31,WIN,seg=60,sides=4,axis='z')
        for s in (1,-1):ring(M,c+[0,0,s*.32],W-.16,.045,ACC,seg=60,sides=4,axis='z')
        for k in range(6):
            a=k*PI/3;d=np.array([math.cos(a),math.sin(a),0]);truss(M,c+d*.74,c+d*(W-.27),.26,.028)
        floods(M,[c+np.array([math.cos(a)*W,math.sin(a)*W,.32*(1 if zw>0 else -1)]) for a in np.linspace(0,2*PI,10,endpoint=False)+PI/10],.07)
    drum(M,C+[0,0,-ZA],C+[0,0,ZA],.72,LIGHT,16,bands=(.1,.3,.7,.9))
    for z in (-2.0,2.0):ring(M,C+[0,0,z],.725,.035,WIN,seg=32,sides=4,axis='z')
    for s in (1,-1):collar(M,C+[0,0,s*ZA],.36,(0,0,s))
    M.blob(tuple(C),1.15,LIGHT,sub=2,noise=0)                                                        # the command sphere
    for y,R in ((0,1.16),(.38,1.09),(-.38,1.09)):ring(M,C+[0,y,0],R*1.004,.04,WIN,seg=40,sides=4,axis='y')
    ring(M,C+[0,.7,0],.92,.05,ACC,seg=36,sides=4,axis='y')
    mast(M,C+[0,1.12,0],1.5,.05)
    drum(M,(0,-1.4,0),(0,-.5,0),1.0,MID,16,bands=(.5,));drum(M,(0,-.52,0),(0,.0,0),.5,DARK,12)       # keel and its pylon
    winband(M,(0,-.95,0),1.0)
    for a in (PI*1.35,PI*1.65):tank(M,(math.cos(a)*.95,-1.6,math.sin(a)*.95),.38)
    for sx in (1,-1):radiator(M,(sx*1.0,-.95,0),(sx*2.0,-.95,0),.5,2)
    hpads(M,lambda a:u(a)*.98+[0,HP_Y,0])
    return M

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
        ring_y(M,2.2,1.0,.09,MID,40,8)                                                                   # (10 Nov 2026: raised from 2.0, clear of the balcony's guns)
        for a in (0,2*PI/3,4*PI/3):tube(M,[u(a)*.25+[0,2.2,0],u(a)*.92+[0,2.2,0]],[.035,.035],DARK,.9,5)
    return M
def spire_core():
    # a tall tower: a skirt deck at hardpoint height holds the five pads; a wide column with window bands; a big balcony with
    # five docking collars on its rim; a slim upper shaft with radiators and a small balcony; a needle with a beacon; below,
    # a keel with tanks tapering to a point. (10 Nov 2026) Three lesser spires stand round it on bridges, each with its
    # own window bands and needle: the Station reads as a cluster of towers, the Depot as one.
    M=Mesh(350)
    lathe_y(M,[(-1.3,.7),(-1.15,1.75),(-.65,1.75),(-.5,.7)],24,lambda i:(MID,.95));winband(M,(0,-.9,0),1.75,r=.06)
    drum(M,(0,-.55,0),(0,2.55,0),.85,LIGHT,18,bands=(.25,.75))
    for y in (.35,.9,1.45,2.0):winband(M,(0,y,0),.85,seg=36)
    lathe_y(M,[(2.45,.8),(2.6,2.1),(2.9,2.1),(3.05,.6)],28,lambda i:(MID,.95));winband(M,(0,2.75,0),2.1,r=.05)
    for a in HP_A:collar(M,u(a)*2.05+[0,2.75,0],.22,u(a))
    drum(M,(0,3.0,0),(0,4.85,0),.5,MID,14,bands=(.3,.7))
    for a in (PI/3,PI,5*PI/3):radiator(M,u(a)*.48+[0,3.95,0],u(a)*1.85+[0,3.95,0],.7,3)
    lathe_y(M,[(4.8,.45),(4.88,1.15),(5.06,1.15),(5.14,.4)],22,lambda i:(DARK,.9));winband(M,(0,4.97,0),1.15,r=.03)
    tube(M,[(0,5.1,0),(0,6.6,0)],[.32,.04],LIGHT,.95,10);ring(M,(0,5.9,0),.24,.04,ACC,seg=16,sides=4,axis='y');M.blob((0,6.65,0),.1,WIN,sub=1,noise=0)
    drum(M,(0,-3.0,0),(0,-1.25,0),.62,DARK,14,bands=(.5,))
    tube(M,[(0,-3.0,0),(0,-4.0,0),(0,-4.5,0)],[.62,.25,.05],DARK,.95,14)
    for a in (PI/6,PI*5/6,PI*3/2):tank(M,u(a)*.85+[0,-2.2,0],.42)
    for a in SPIRE_SIDE:                                                                             # the lesser spires
        c=u(a)*2.75
        tube(M,[c+[0,-1.05,0],c+[0,-.45,0]],[.08,.4],DARK,.95,12)
        drum(M,c+[0,-.45,0],c+[0,3.4,0],.4,MID,12,bands=(.2,.55,.9))
        for y in (.2,.75,1.3,1.85,2.4):winband(M,c+[0,y,0],.4,seg=24)
        B=Mesh();lathe_y(B,[(3.35,.45),(3.42,.72),(3.56,.72),(3.62,.35)],18,lambda i:(DARK,.9));put(M,B,c)
        tube(M,[c+[0,3.6,0],c+[0,4.6,0]],[.22,.03],LIGHT,.95,8);M.blob(tuple(c+[0,4.65,0]),.07,WIN,sub=1,noise=0)
        for y,r0 in ((.95,.8),(3.3,.48)):truss(M,u(a)*r0+[0,y,0],u(a)*2.38+[0,y,0],.24,.026)
        floods(M,[c+u(a)*.42+[0,y,0] for y in (-.2,1.6)],.05)
    floods(M,[u(a)*2.1+[0,2.95,0] for a in np.linspace(0,2*PI,8,endpoint=False)+PI/4]+[u(a)*1.75+[0,-.62,0] for a in np.array(HP_A)+PI/5],.065)
    hpads(M,lambda a:u(a)*1.72+[0,HP_Y,0])
    return M
SPIRE_SIDE=[HP_A[4]+PI/5,HP_A[1]+PI/5,HP_A[3]+PI/5]

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
    return M
CH=1.85
def cluster_core():
    # three cube frames stacked off-centre round a spine: the main frame holds a long hab drum and a truss belt at hardpoint
    # height (the pads hang off it); a smaller frame on its deck carries a big module, radiators and the mast; a third hangs
    # below with tanks. Containers, spheres and docking collars on trusses, nothing quite symmetric. (10 Nov 2026) A lattice
    # tower rises from the upper frame to a lit command pod with a dish, and the hab drum ends in two big lit spheres outside
    # the frame: the Station is twice the Depot's height and wider than its frame.
    M=Mesh(370);h=CH;c0=np.array([0,-.2,0])
    cube_frame(M,c0,h,.26,.03,decks=('top','bottom'),belt=HP_Y)
    drum(M,(-h-.55,.15,0),(h+.55,.15,0),.72,LIGHT,16,bands=(.1,.5,.9))
    B=Mesh();winband(B,(0,0,0),.72,'y',32);put(M,B,(-.75,.15,0),frame_y((1,0,0)));B=Mesh();winband(B,(0,0,0),.72,'y',32);put(M,B,(.75,.15,0),frame_y((1,0,0)))
    for sx in (1,-1):
        c=np.array([sx*(h+1.25),.15,0]);M.blob(tuple(c),.8,LIGHT,sub=2,noise=0)
        for y,R in ((0,.81),(.3,.75),(-.3,.75)):ring(M,c+[0,y,0],R,.03,WIN,seg=32,sides=4,axis='y')
    truss(M,(0,c0[1]-h,0),(0,c0[1]+h,0),.3,.03)
    yt=c0[1]+h+.17                                                                                       # the deck: containers
    for x,z in ((-1.0,.75),(-.45,.75),(-1.0,-.1)):container(M,(x,yt+.2,z),(.5,.4,.95),MID)
    container(M,(-.72,yt+.6,.75),(.5,.4,.95),LIGHT)
    c1=np.array([.55,yt+.95,-.55]);cube_frame(M,c1,.9,.2,.025)                                          # upper frame and its module
    box(M,tuple(c1+[0,-.235,0]),(1.25,1.47,1.25),MID);box(M,tuple(c1+[0,.53,0]),(.8,.08,.8),DARK)
    for k in range(3):plate(M,[c1+[-.5,.2-k*.28,.635],c1+[.5,.2-k*.28,.635],c1+[.5,.25-k*.28,.635],c1+[-.5,.25-k*.28,.635]],.01,WIN,1.0)
    for sx in (1,-1):radiator(M,c1+[sx*.6,.3,0],c1+[sx*2.4,.55,0],.7,3)
    t0=c1+[0,.56,0];t1=t0+[0,2.44,0]                                                                     # the command tower
    truss(M,t0,t1,.42,.034)
    for y in (.7,1.4):B=Mesh();box(B,(0,0,0),(.62,.05,.62),DARK);put(M,B,t0+[0,y,0])
    box(M,tuple(t1+[0,.38,0]),(1.25,.76,1.25),LIGHT);box(M,tuple(t1+[0,.8,0]),(1.0,.08,1.0),DARK)
    for s in (1,-1):
        for k in range(2):
            plate(M,[t1+[-.48,.22+k*.26,s*.645],t1+[.48,.22+k*.26,s*.645],t1+[.48,.3+k*.26,s*.645],t1+[-.48,.3+k*.26,s*.645]],.01,WIN,1.0)
            plate(M,[t1+[s*.645,.22+k*.26,-.48],t1+[s*.645,.22+k*.26,.48],t1+[s*.645,.3+k*.26,.48],t1+[s*.645,.3+k*.26,-.48]],.01,WIN,1.0)
    tube(M,[t1+[0,.84,0],t1+[0,1.15,0]],[.06,.06],DARK,.9,6);dish(M,t1+[0,1.2,0],.55)
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
    return M
DISC_C=[(-1.25,.0),(-1.25,1.2),(-1.05,2.2),(-.7,3.2),(-.4,3.55),(-.2,3.85),(0,3.55),(.12,3.1),(.2,1.8),(.22,0)]
def disc_core():
    # a broad lens with a lit rim and five docking slots between the hardpoints; an upper tier with its own window band.
    # (10 Nov 2026) A tall column lifts a second, smaller lens with its own lit rim, a dome and the mast: stacked saucers,
    # where the Depot is one small lens. A keel drum and cone with tanks below. The pads sit just out from the rim.
    M=Mesh(390);y0=-.75
    B=Mesh();lathe_y(B,DISC_C,40,lambda i:((MID,.92) if i<5 else (LIGHT,1.0)));put(M,B,(0,y0,0))
    winband(M,(0,y0-.2,0),3.85,r=.07,seg=72)
    for a in DISC_SLOTS:B=Mesh();mouth(B,(0,0,0),.95,.24,.6);put(M,B,u(a)*3.79+[0,y0-.2,0],outward(a))
    drum(M,(0,y0+.15,0),(0,.45,0),1.25,MID,18);lathe_y(M,[(.3,1.2),(.42,2.1),(.62,2.1),(.75,1.0)],32,lambda i:(LIGHT,.95))
    winband(M,(0,.52,0),2.1,r=.05,seg=48)
    drum(M,(0,.7,0),(0,3.0,0),.6,MID,16,bands=(.2,.5,.8))
    for y in (1.2,1.8,2.4):winband(M,(0,y,0),.6,seg=28)
    yu=3.25;B=Mesh();lathe_y(B,[(-.32,.0),(-.32,.6),(-.24,1.5),(-.08,2.3),(0,2.45),(.08,2.25),(.16,1.6),(.2,.7),(.2,0)],36,lambda i:((MID,.92) if i<4 else (LIGHT,1.0)));put(M,B,(0,yu,0))
    winband(M,(0,yu,0),2.45,r=.06,seg=56)
    M.blob((0,yu+.2,0),.8,LIGHT,sub=2,squash=(1,.5,1),noise=0);M.blob((0,yu+.55,0),.32,GLASS,sub=2,squash=(1,.7,1),noise=0)
    ring(M,(0,yu+.22,0),.82,.035,ACC,seg=28,sides=4,axis='y');mast(M,(0,yu+.74,0),1.3,.045)
    floods(M,[u(a)*2.3+[0,yu+.05,0] for a in np.linspace(0,2*PI,8,endpoint=False)+PI/8],.06)
    for a in (PI/2+PI/5,PI*1.5+PI/5):radiator(M,u(a)*.6+[0,1.6,0],u(a)*1.9+[0,1.7,0],.55,2)
    drum(M,(0,-2.4,0),(0,y0-1.1,0),1.0,DARK,16,bands=(.5,));tube(M,[(0,-2.4,0),(0,-3.0,0),(0,-3.25,0)],[1.0,.4,.08],DARK,.95,16)
    for a in (PI/6,PI*5/6,PI*3/2):tank(M,u(a)*1.22+[0,-2.0,0],.45)
    floods(M,[u(a)*3.5+[0,y0+.18,0] for a in np.linspace(0,2*PI,10,endpoint=False)]+[u(a)*2.05+[0,.68,0] for a in np.linspace(0,2*PI,6,endpoint=False)],.065)
    hpads(M,lambda a:u(a)*3.6+[0,HP_Y,0])
    return M
DISC_SLOTS=list(np.array(HP_A)+PI/5)

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
    return M
_RK_D=Rock((0,0,0),1.4,61,squash=(1.18,.86,1.0))
def _rs(rk,d,ins=.06):
    d=np.array(d,float);d/=np.linalg.norm(d);p=rk.surf(d,ins);return (p,d)
_RK_C=Rock((0,0,0),3.3,41,squash=(1.1,.8,1.05))
def asteroid_core():
    # a big rock: a crown dock rising from its top, glass hab domes in clusters, two docking arms with collars, hangars cut
    # into its flanks, radiators, a keel drum below; the five pads stand out from its rim on trusses. (10 Nov 2026) A lit
    # habitat ring circles the crown dock on four spokes, and a second, smaller rock rides off one shoulder on a lattice
    # bridge with a dome and lights of its own: the Station is a small rock group, the Depot one rock.
    M=Mesh(410);rk=_RK_C;rk.build(M,3)
    top=rk.surf((0,1,0),.2);bot=rk.surf((0,-1,0),.2)
    drum(M,top,top+[0,1.0,0],.85,MID,16,bands=(.5,));drum(M,top+[0,1.0,0],top+[0,1.5,0],1.0,DARK,16)
    for a in np.linspace(0,2*PI,4,endpoint=False):collar(M,top+[math.cos(a)*.95,1.25,math.sin(a)*.95],.2,(math.cos(a),0,math.sin(a)))
    mast(M,top+[0,1.5,0],1.6,.05)
    yr=top[1]+.55;ring(M,(0,yr,0),2.35,.2,MID,seg=56,sides=10,axis='y');ring(M,(0,yr,0),2.35,.205,WIN,seg=56,sides=4,axis='y')
    for a in np.linspace(0,2*PI,4,endpoint=False)+PI/4:truss(M,u(a)*.83+[0,yr,0],u(a)*2.18+[0,yr,0],.22,.026)
    drum(M,bot,bot-[0,.8,0],.6,MID,14);tube(M,[bot-[0,.8,0],bot-[0,1.2,0]],[.6,.12],DARK,.95,14)
    for d in ((1,-.1,.2),(-.8,-.15,.7),(.1,-.1,-1)):rock_mouth(M,rk,np.array(d),1.3,.7)
    for d,r in (((.55,.8,.45),.85),((.9,.55,.1),.5),((-.6,.75,-.3),.75),((-.3,.8,-.8),.45),((-.15,.85,.75),.55)):
        p=rk.surf(d,-.02);M.blob(tuple(p),r,GLASS,sub=2,squash=(1,.6,1),noise=0);ring(M,tuple(p+[0,.02,0]),r,.04,ACC,seg=24,sides=4,axis='y')
    for a,yv in AST_ARMS:                                                                                # docking arms
        d=u(a)+[0,yv,0];p=rk.surf(d,.3);e=u(a)*4.7+[0,1.0,0];truss(M,p,e,.26,.028);collar(M,e,.3,u(a))
        floods(M,[e-u(a)*.6+[0,.15,0]],.06)
    p=rk.surf((-.2,1,.6),.05);radiator(M,p,p+[-1.6,.4,.6],.6,3)
    p=rk.surf((.4,.9,-.7),.05);radiator(M,p,p+[1.2,.5,-1.2],.6,3)
    floods(M,[rk.surf(d,.04) for d in ((1,.5,-.5),(-1,.4,-.2),(.3,.3,1),(.7,-.5,.8),(-.6,-.5,-.9),(0,.2,-1),(-1,-.2,.6))],.08)
    mr=_RK_M;mr.build(M,3)                                                                               # the moonlet and its bridge
    a0=rk.surf(mr.c-rk.c,.25);a1=mr.surf(rk.c-mr.c,.15);truss(M,a0,a1,.34,.034);truss(M,a0+[0,-.5,0],a1+[0,-.4,0],.22,.026)
    q=mr.surf((0,1,0),-.02);M.blob(tuple(q),.62,GLASS,sub=2,squash=(1,.6,1),noise=0);ring(M,tuple(q+[0,.02,0]),.62,.04,ACC,seg=24,sides=4,axis='y')
    mast(M,mr.surf((.4,1,.3),.05),1.1,.04)
    floods(M,[mr.surf(d,.03) for d in ((1,.3,0),(-1,.2,.4),(0,-.4,1),(.3,.1,-1))],.07)
    def st(a):
        d=np.array([math.cos(a),HP_Y/HP_R*.6,math.sin(a)]);return rk.surf(d,.3)
    hpads(M,st)
    return M
AST_ARMS=((PI*.3,.25),(PI*1.3,.3))
_RK_M=Rock((-4.0,2.4,2.3),1.15,43,squash=(1.1,.85,1.0))

# ================================================================== DESIGN 1: COMPANY STANDARD, the Station
def std_core():
    # beyond_stations.station_core('standard'): spine, hub, habitat ring, crown dock, tanks, radiators, the five pads. (10 Nov
    # 2026) Over the crown a command tower lifts a wide lit command deck with a dome and mast, and a second, smaller habitat
    # ring circles the spine below the hub: the Station has two rings and a bridge, the Depot one drum and (at level 3) a ring.
    M=BS_core('standard',True)
    drum(M,(0,2.7,0),(0,3.95,0),.45,MID,14,bands=(.3,.7))
    for y in (3.1,3.55):winband(M,(0,y,0),.45,seg=24)
    lathe_y(M,[(3.9,.5),(4.02,1.4),(4.36,1.4),(4.52,.62)],32,lambda i:(LIGHT,.95));winband(M,(0,4.2,0),1.4,r=.05,seg=48)
    M.blob((0,4.52,0),.62,LIGHT,sub=2,squash=(1,.45,1),noise=0);M.blob((0,4.74,0),.22,GLASS,sub=2,squash=(1,.7,1),noise=0)
    mast(M,(0,4.88,0),1.3,.045)
    floods(M,[u(a)*1.42+[0,4.12,0] for a in np.linspace(0,2*PI,8,endpoint=False)+PI/8],.055)
    ring(M,(0,-1.6,0),2.3,.24,MID,seg=48,sides=10,axis='y');ring(M,(0,-1.6,0),2.3,.245,WIN,seg=48,sides=4,axis='y')
    for a in (PI/3,PI,5*PI/3):truss(M,u(a)*.74+[0,-1.6,0],u(a)*2.1+[0,-1.6,0],.24,.026)
    return M

# ------------------------------------------------------------------ docking ports (10 Nov 2026)
# Where ships dock: the face of each modelled docking collar (the game's ports for a player base, 'pt' in the pack; the game
# takes each port's approach as straight out from the base's axis, so every collar here faces out horizontally)
PORTS_D={1:[(2.42,.1,0)],2:[(0,0,1.12)],3:[(1.75,.5,0)],4:[(2.08,0,0)],5:[(1.94,0,0)],6:[(2.78,.42,0)]}
def _ports_c(n):
    if n==1:return [tuple(u(a)*1.16+[0,2.45,0]) for a in np.linspace(0,2*PI,4,endpoint=False)]
    if n==2:return [(0,1.0,2.9),(0,1.0,-2.9)]
    if n==3:return [tuple(u(a)*2.26+[0,2.75,0]) for a in HP_A]
    if n==4:return [(.4,.15,CH+1.1+.25),(.4,.15,-CH-1.1-.25)]
    if n==5:return [tuple(u(a)*3.92+[0,-.95,0]) for a in DISC_SLOTS]
    if n==6:return [tuple(u(a)*4.98+[0,1.0,0]) for a,_ in AST_ARMS]
def ports(n,kind):return [np.array(p,float) for p in (PORTS_D[n] if kind=='depot' else _ports_c(n))]

# ------------------------------------------------------------------ the live turret seats (10 Nov 2026)
# The game draws a player base's guns live (turretMesh, aiming at targets) on these seats; the models carry no guns of their
# own. Each seat is (point near the hull, outward normal): the pack snaps it onto the hull along its normal and builds a
# turret plinth there (a drum whose skirt reaches the hull all round, so the turntable never hangs over a curve), and packs
# the plinth's top as 'tp' and the normal as 'tn'. The game sets the turret's turntable on the plinth, standing along the
# normal. A player base has four live turrets (STN.depot.tur), so the first NLIVE seats get plinths; the rest are spares the
# game cycles through if a base ever has more. tools/previews/base_seats_check.py checks every live seat: on the hull, upright,
# and nothing of the base (or of any building on any hardpoint) inside the turret's own space.
NLIVE=4
PL_R={'depot':.3,'station':.32}       # plinth radius in model units: the turret's 12 m turntable at BM.K.depot 48 / station 40
_U,_D=np.array([0,1.,0]),np.array([0,-1.,0])
def _n(v):v=np.array(v,float);return v/np.linalg.norm(v)
def _ring_seat(a,r,y,n=None):return (u(a)*r+[0,y,0],_U if n is None else n)
# design 1, the company standard: on the dome's shoulder either side of the mast, on the hub's flank over the docking arm, on
# the tank, under the keel
STD_DSEATS=[_ring_seat(PI*1.5+.35,.34,1.25),_ring_seat(PI*.5-.35,.34,1.25),(np.array([.7,.64,.05]),np.array([1.,0,0])),(np.array([-.2,.2,-1.0]),_U),
            (np.array([0,-1.62,0]),_D),_ring_seat(PI,.34,1.25)]
# its Station: on the habitat ring between the floodlights, on the crown beside the mast, under the keel
STD_CSEATS=[_ring_seat(a,3.1,.45) for a in (PI/8,PI/8+PI/2,PI/8+PI,PI/8+3*PI/2)]+[_ring_seat(a,2.3,-1.85,_D) for a in (PI/4,5*PI/4)]+[(np.array([0,-3.32,0]),_D),_ring_seat(5*PI/8,3.1,.45)]
# Wheel: on the wheel's outer rim (normals out from the axle), on the tank behind it; the Station's on both wheels' rims
_wd=lambda a,r=1.9:(np.array([math.cos(a)*r,math.sin(a)*r,.3]),np.array([math.cos(a),math.sin(a),0]))
WHEEL_DSEATS=[_wd(PI/4),_wd(3*PI/4),_wd(.08),(np.array([0,.4,-1.24]),_U),_wd(PI),_wd(-PI/2+.5)]
_wc=lambda a,z:(np.array([math.cos(a)*3.32,1.0+math.sin(a)*3.32,z]),np.array([math.cos(a),math.sin(a),0]))
WHEEL_CSEATS=[_wc(PI/2-.7,1.25),_wc(PI/2+.7,-1.25),_wc(PI/2+.7,1.25),_wc(PI/2-.7,-1.25),_wc(PI/9,1.25),_wc(PI-PI/9,-1.25),_wc(PI/9,-1.25),_wc(PI-PI/9,1.25)]
# Spire: on the balcony between its production modules, under the foot
SPIRE_DSEATS=[_ring_seat(a,.86,1.46) for a in (PI/6,PI*5/6,PI*3/2)]+[(np.array([0,-2.32,0]),_D),(np.array([1.4,.66,0]),_U),(np.array([0,2.46,.0]),_U)]
SPIRE_CSEATS=[_ring_seat(a,1.75,2.95) for a in np.radians([36,126,216,288])]+[_ring_seat(a,.85,5.12) for a in (PI/2,3*PI/2)]+[(np.array([0,-1.32,1.35]),_D),(np.array([0,-1.32,-1.35]),_D)]
# Truss cluster: on the top deck's corners, on the corner tank, under the frame (the Station: two on its deck, two under it)
CLUSTER_DSEATS=[(np.array([.98,1.2,.98]),_U),(np.array([-.98,1.2,.98]),_U),(np.array([1.0,1.45,-1.0]),_U),(np.array([-1.0,-1.1,-1.0]),_D),
                (np.array([1.85,.25,0]),_U),(np.array([-1.0,-.68,1.0]),_U)]
_c1=np.array([.55,CH-.2+.17+.95,-.55]);_c2=np.array([-.5,-.2-CH-.9,.4])
CLUSTER_CSEATS=[(np.array([CH-.05,CH-.2+.2,CH-.05]),_U),(np.array([-CH+.05,CH-.2+.2,-.3]),_U),(np.array([-CH+.05,-.2-CH-.2,CH-.05]),_D),(np.array([CH-.05,-.2-CH-.2,-CH+.05]),_D),
                (_c1+[-.9,1.0,.9],_U),(_c1+[.9,1.0,.9],_U),(_c2+[-.75,-.88,.75],_D),(np.array([CH-.05,CH-.2+.2,-CH+.05]),_U)]
# Disc: on the deck between the containers, under the keel; the Station's on the lens deck above each hardpoint
DISC_DSEATS=[_ring_seat(a,1.05,.26) for a in (PI/2,PI,7*PI/4)]+[(np.array([0,-1.06,0]),_D),_ring_seat(3*PI/2+.2,1.05,.26),_ring_seat(PI/4+.6,1.05,.26)]
DISC_CSEATS=[_ring_seat(a,2.65,-.5) for a in HP_A]+[_ring_seat(a,1.55,.72) for a in (HP_A[0]+PI/5,HP_A[2]+PI/5)]+[(np.array([0,-3.27,0]),_D)]
# Asteroid: on the rock, along its own outward direction, clear of the domes, the arm and the waist ring
_RK_D=Rock((0,0,0),1.4,61,squash=(1.18,.86,1.0))
def _rs(rk,d,ins=0.0):
    d=_n(d);return (rk.surf(d,ins),d)
AST_DSEATS=[_rs(_RK_D,d) for d in ((.7,.6,.55),(.3,.6,-.9),(.5,-.9,-.3),(-.7,-.8,.3),(.15,.45,1),(-.85,.15,.8))]
_RK_C=Rock((0,0,0),3.3,41,squash=(1.1,.8,1.05))
AST_CSEATS=[_rs(_RK_C,d) for d in ((1,.35,-.45),(-.95,.35,-.1),(.15,.4,1),(-.35,.4,-1),(-.3,-.9,.5),(.6,-.85,-.3),(-.4,.9,.2),(1,.1,-.5))]

def _tris(M):return np.array([np.array(t,float) for t in M.T]).reshape(-1,3,3)
def _ray(T,o,d):
    # nearest hit distance along o + t d (t>0) on triangles T, or None
    e1=T[:,1]-T[:,0];e2=T[:,2]-T[:,0];p=np.cross(d,e2);det=(e1*p).sum(1);ok=np.abs(det)>1e-12;inv=np.where(ok,1/np.where(ok,det,1),0)
    s=o-T[:,0];uu=(s*p).sum(1)*inv;q=np.cross(s,e1);v=(q@d)*inv;t=(e2*q).sum(1)*inv
    m=ok&(uu>=0)&(v>=0)&(uu+v<=1)&(t>1e-6)
    return float(np.min(np.where(m,t,np.inf))) if m.any() else None
def snap(M,seats,kind,up=.35,deep=.8):
    # each seat onto the hull along its normal: (plinth top, plinth bottom, normal). The plinth's top clears the highest hull
    # point under its rim; its skirt reaches the lowest (at most `deep` below the seat)
    T=_tris(M);r=PL_R[kind];out=[]
    for p,n in seats:
        p=np.array(p,float);n=_n(n);a=np.cross(n,[0,0,1.] if abs(n[2])<.9 else [1.,0,0]);a=_n(a);b=np.cross(n,a);H=[]
        for k in range(-1,12):
            o=p if k<0 else p+(a*math.cos(k*PI/6)+b*math.sin(k*PI/6))*r*(1 if k%2 else .6)
            t=_ray(T,o+n*up,-n)
            if t is not None and t<up+deep:H.append(up-t)
        if not H:H=[0.0]
        top=p+n*(max(H)+(.02 if kind=='depot' else .042));bot=p+n*(min(H)-.03)
        out.append((top,bot,n))
    return out
def plinth(M,top,bot,n,kind):
    # a turret plinth: a drum from the hull up to the seat, a dark deck ring and an amber edge, lit marker lamps round its skirt
    r=PL_R[kind];top=np.array(top,float);bot=np.array(bot,float);n=_n(n)
    if np.linalg.norm(top-bot)<.04:bot=top-n*.04
    drum(M,bot,top-n*r*.07,r*.9,MID,12)                                                 # its top cap hidden inside the deck
    drum(M,top-n*r*.15,top,r,DARK,12)
    R=frame_y(n);C=Mesh();ring(C,(0,0,0),r*1.01,r*.05,ACC,seg=24,sides=4,axis='y');put(M,C,top-n*r*.04,R)
    a=_n(np.cross(n,[0,0,1.] if abs(n[2])<.9 else [1.,0,0]));b=np.cross(n,a)
    for k in range(4):
        q=top-n*r*.2+(a*math.cos(k*PI/2+PI/4)+b*math.sin(k*PI/2+PI/4))*r*.91;M.blob(tuple(q),r*.06,WIN,sub=1,noise=0)
def _seated(M,seats,kind):
    S=snap(M,seats,kind)
    for top,bot,n in S[:NLIVE]:plinth(M,top,bot,n,kind)
    return M,[(top,n) for top,_,n in S]
_DEP={1:lambda lv:BS_depot(lv,guns=False)}
_CORE={1:lambda:std_core()}
_DS={1:STD_DSEATS};_CS={1:STD_CSEATS}
def depot_model(n,lv,seats=False):
    # design n's Depot at level lv as the pack holds it: no modelled guns, a plinth on each live seat
    M,S=_seated(_DEP[n](lv),_DS[n],'depot');return (M,S) if seats else M
def core_model(n,seats=False):
    M,S=_seated(_CORE[n](),_CS[n],'station');return (M,S) if seats else M
def live_seats():
    # {design: (depot seats, core seats)} as (plinth top, normal), snapped on the level-1 depot and the bare core
    return {n:(depot_model(n,1,True)[1],core_model(n,True)[1]) for n in range(1,7)}

# ------------------------------------------------------------------ development modules' berths (10 Nov 2026)
# A player base's development modules (the game's works: storage vaults, production works, habitat, shield works, fighter
# hangar, defence platform; each a stack of one unit per level) stand on the base, each on a truss strut from the hull to its
# stack, at half their free-standing size. Each model gets a berth per kind, found here: out from the hull at the stack's
# height, clear of the hull, of the live turrets (and their barrels' sweep), of the docking ports' approach lanes, of the
# Station's buildings on every hardpoint, and of each other, spread round the base. Packed as 'wb': {kind: [hull point,
# stack centre]}; the game stacks a kind's units on its centre (one per level, upward and downward in turn).
WK_FS=.5                                                       # the modules' size on a player base (the game's BM.wkS)
WK_U={'hangar':58,'store':55,'armor':60,'prod':72,'life':64,'def':62}   # each unit's half-size in metres (WKU)
WK_N={'hangar':4,'store':3,'armor':3,'prod':2,'life':2,'def':1}         # most units a kind has (DEV levels)
WK_STEP=2.15                                                   # stack spacing, in unit half-sizes
WK_KIND=['hangar','store','armor','prod','life','def']
KS={'depot':48.0,'station':40.0}
TU_LIFT=13.2*1.15
def _seg_pts(a,b,k=12):return [a+(b-a)*t for t in np.linspace(0,1,k)]
def _dist_seg(P,a,b):
    # distance from points P (N,3) to the segment a-b
    d=b-a;L=d@d;t=np.clip(((P-a)@d)/(L if L>0 else 1),0,1);return np.linalg.norm(P-(a+np.outer(t,d)),axis=1)
def _samples(T):
    c=T.mean(1);return np.concatenate([T.reshape(-1,3),c])
def all_buildings_mesh(M):
    from beyond_stations import shipyard,ext_storage,defence_platform,hangar,forge,market_wing
    for a in HP_A:
        for fn in (shipyard,ext_storage,defence_platform,hangar,forge,market_wing):put(M,fn(),(math.cos(a)*HP_R,HP_Y,math.sin(a)*HP_R),outward(a),.8)
    return M
def berths(M,Mc,seats,prts,kind):
    # M: the model with its plinths (struts start on it); Mc: the same with, on a core, every building on every hardpoint (the
    # stacks keep clear of it); in model units. seats: the live seats (plinth top, normal); prts: the docking ports
    K=KS[kind];T=_tris(M);P=_samples(_tris(Mc))*K;out={};chosen=[]
    tur=[np.array(t,float)*K+np.array(n,float)*TU_LIFT for t,n in seats[:NLIVE]]
    lanes=[]
    for p in prts:
        p=np.array(p,float)*K;d=np.array([p[0],0,p[2]]);d/=np.linalg.norm(d);lanes.append((p,p+d*260))
    ys=np.arange(-2.2,2.21,.2) if kind=='depot' else np.arange(-3.2,4.81,.25)
    AN=np.radians(np.arange(0,360,7.5));PRJ={};HIT={}
    for a in AN:
        d=np.array([math.cos(a),0,math.sin(a)]);s=np.array([-d[2],0,d[0]]);PRJ[a]=(P@d,np.abs(P@s))
        for y in ys:HIT[(a,y)]=_ray(T,np.array([0,y,0])+d*12,-d)
    for k in WK_KIND:
        r=WK_U[k]*WK_FS*(1.25 if k=='def' else 1.1);hh=(WK_N[k]-1)*WK_STEP*WK_U[k]*WK_FS/2+(28 if k=='def' else 0)
        best=None
        for f in (1,.75,.5,.3):                                                          # margins eased only if nothing fits
          if best is not None:break
          for a in AN:
              d=np.array([math.cos(a),0,math.sin(a)]);pd,lat=PRJ[a]
              for y in ys:
                  y0=y*K;m=(lat<r+8)&(np.abs(P[:,1]-y0)<hh+r+8)&(pd>0)
                  Rout=float(pd[m].max()) if m.any() else 0.0
                  hit=HIT[(a,y)]
                  if hit is None:continue
                  H=np.array([0,y,0])+d*(12-hit);Hw=H*K
                  if np.linalg.norm(Hw-np.array([0,y0,0]))<1:continue
                  gap=Rout-Hw@d;C=d*(Rout+16+r)+[0,y0,0]                                        # the stack's centre
                  top,bot=C+[0,hh,0],C-[0,hh,0];strut=(Hw,C-d*r)
                  if gap>4*r:continue                                                      # no long reach past a thin part
                  if any(np.min(_dist_seg(np.array([t]),top,bot))<r+42*f for t in tur):continue
                  if any(np.min(_dist_seg(np.array(_seg_pts(*strut)),t,t))<12+14*f for t in tur):continue
                  if any(np.min(_dist_seg(np.array(_seg_pts(top,bot)),a0,b0))<r+38*f for a0,b0 in lanes):continue
                  if any(np.min(_dist_seg(np.array(_seg_pts(*strut)),a0,b0))<10+14*f for a0,b0 in lanes):continue
                  if any(np.min(_dist_seg(np.array(_seg_pts(top,bot)),c0-[0,h0,0],c0+[0,h0,0]))<r+r0+18*f for c0,h0,r0 in chosen):continue
                  sep=min([abs(((a-math.atan2(c0[2],c0[0])+3*PI)%(2*PI))-PI) for c0,_,_ in chosen]+[PI])
                  score=min(sep,PI/2)*400-np.linalg.norm(C-Hw)-abs(y0)*.6
                  if best is None or score>best[0]:best=(score,H,C/K,(C,hh,r))
        if best is None:raise RuntimeError('no berth for %s (%s)'%(k,kind))
        out[k]=(best[1],best[2]);chosen.append(best[3])
    return out
# ------------------------------------------------------------------ the company's logo boards (10 Nov 2026)
# Each base model carries spots for its owner's logo: a board lying on the hull (the game draws the owner's glyph on it, lit,
# in the company's colour, from the profile). Found by looking at the model from many directions (round it, from above and
# below at 35°, straight up and down): a depth map of the model seen along each direction, and a board wherever the hull under
# it is nearly flat and nothing (no building, mast or ring) stands in front of it, clear of the live turrets, the docking
# lanes and the module stacks. The best two on a Depot, three on a Station, facing well apart. Packed as 'lg': [centre,
# outward normal, half-size] in the model's frame.
LG_HALF={'depot':(.42,.34,.27),'station':(.6,.48,.38)}      # board half-sizes tried, in model units (20/16/13 m; 24/19/15 m)
def _dense(T,cell):
    # points over every triangle, about five per grid cell
    e1=T[:,1]-T[:,0];e2=T[:,2]-T[:,0];A=np.linalg.norm(np.cross(e1,e2),axis=1)/2;n=np.clip(np.ceil(A/(cell*cell)*5).astype(int),1,2000)
    idx=np.repeat(np.arange(len(T)),n);r1=np.random.default_rng(5).random(len(idx));r2=np.random.default_rng(6).random(len(idx));f=r1+r2>1;r1[f]=1-r1[f];r2[f]=1-r2[f]
    return T[idx,0]+e1[idx]*r1[:,None]+e2[idx]*r2[:,None]
def _dirs():
    out=[]
    for el in (0,35,-35):
        for a in np.radians(np.arange(0,360,15 if el==0 else 30)):out.append((np.array([math.cos(a)*math.cos(math.radians(el)),math.sin(math.radians(el)),math.sin(a)*math.cos(math.radians(el))]),abs(el)))
    out+= [(np.array([0,1.,0]),90),(np.array([0,-1.,0]),90)]
    return out
def logo_spots(M,Mc,seats,prts,wb,kind,count=None):
    from numpy.lib.stride_tricks import sliding_window_view as sw
    K=KS[kind];count=count or (2 if kind=='depot' else 3);cell=.06 if kind=='depot' else .09;EX=3.6 if kind=='depot' else 7.6
    Qm=_dense(_tris(M),cell);Qc=_dense(_tris(Mc),cell) if Mc is not M else Qm
    tur=[np.array(t,float)+np.array(n,float)*TU_LIFT/K for t,n in seats[:NLIVE]]
    lanes=[]
    for p in prts:
        p=np.array(p,float);d=np.array([p[0],0,p[2]]);d/=np.linalg.norm(d);lanes.append((p,p+d*260/K))
    stacks=[(np.array(C,float),WK_U[k]*WK_FS*1.15/K,(WK_N[k]-1)*WK_STEP*WK_U[k]*WK_FS/2/K) for k,(H,C) in wb.items()]
    cands=[]
    for d,el in _dirs():
        up=np.array([0,1.,0]) if abs(d[1])<.9 else np.array([1.,0,0]);s=np.cross(up,d);s/=np.linalg.norm(s);v=np.cross(d,s)
        def dmap(Q):
            a=Q@s;b=Q@v;z=Q@d;i=np.floor((a+EX)/cell).astype(int);j=np.floor((b+EX)/cell).astype(int);G=int(2*EX/cell);D=np.full((G,G),-np.inf);ok=(i>=0)&(i<G)&(j>=0)&(j<G)
            np.maximum.at(D,(i[ok],j[ok]),z[ok]);return D
        Dm=dmap(Qm);Dc=dmap(Qc) if Qc is not Qm else Dm
        for hs in LG_HALF[kind]:
            w=int(round(2*hs/cell));Wm=sw(Dm,(w,w));Wc=sw(Dc,(w,w))
            fin=np.isfinite(Wm);cov=fin.mean(axis=(2,3));mx=Wm.max(axis=(2,3));mn=np.where(fin,Wm,np.inf).min(axis=(2,3));cx=Wc.max(axis=(2,3))
            with np.errstate(invalid='ignore'):ok=(cov>.97)&(mx-mn<.35*hs)&(cx<=mx+1e-6)
            for i,j in zip(*np.nonzero(ok)):
                a=(i+w/2)*cell-EX;b=(j+w/2)*cell-EX;c=s*a+v*b+d*(mx[i,j]+.025)
                cands.append((el,hs,c,d,s,float(mx[i,j]-mn[i,j])))
    good=[]
    for el,hs,c,d,s,fl in cands:
        if any(np.linalg.norm(c-t)<hs+18/K for t in tur):continue
        if any(float(_dist_seg(np.array([c]),a0,b0)[0])<hs*1.2+22/K for a0,b0 in lanes):continue
        if any(float(_dist_seg(np.array([c]),C-[0,hh,0],C+[0,hh,0])[0])<hs*1.3+r for C,r,hh in stacks):continue
        good.append((hs*4-el/40-fl*2-abs(c[1])*.05-math.hypot(c[0],c[2])*.12,el,hs,c,d))
    good.sort(key=lambda x:-x[0]);out=[]
    for sc,el,hs,c,d in good:
        if len(out)>=count:break
        if any(float(d@d0)>math.cos(math.radians(75 if count==2 else 60)) for _,d0,_ in out):continue
        if any(np.linalg.norm(c-c0)<hs+h0+.2 for c0,_,h0 in out):continue
        out.append((c,d,hs))
    return out
def _extra(M,S,n,kind,Mc=None):
    Mc=Mc if Mc is not None else M;pr=ports(n,kind);wb=berths(M,Mc,S,pr,kind)
    return {'pt':pr,'wb':wb,'lg':logo_spots(M,Mc,S,pr,wb,kind)}
def _depot_full(n,lv):
    M,S=depot_model(n,lv,True);return M,S,_extra(M,S,n,'depot')
def _core_full(n):
    M,S=core_model(n,True);Mc=Mesh();Mc.T=list(M.T);Mc.R=list(M.R);all_buildings_mesh(Mc);return M,S,_extra(M,S,n,'station',Mc)

# ------------------------------------------------------------------ the families
DESIGNS=[(2,'Wheel','a standing habitat wheel on an axle',wheel_depot,wheel_core,WHEEL_DSEATS,WHEEL_CSEATS),
         (3,'Spire','a tall stepped tower with balconies and a needle',spire_depot,spire_core,SPIRE_DSEATS,SPIRE_CSEATS),
         (4,'Truss cluster','modules bolted into open cube frames',cluster_depot,cluster_core,CLUSTER_DSEATS,CLUSTER_CSEATS),
         (5,'Disc','a flat lens with a lit rim and docking slots',disc_depot,disc_core,DISC_DSEATS,DISC_CSEATS),
         (6,'Asteroid','built into a large rock: domes, docking arms, lights',asteroid_depot,asteroid_core,AST_DSEATS,AST_CSEATS)]
for _n_,_,_,_dep,_core,_ds,_cs in DESIGNS:_DEP[_n_]=_dep;_CORE[_n_]=_core;_DS[_n_]=_ds;_CS[_n_]=_cs
def models():
    # name -> builder returning (mesh, seats as (plinth top, normal), {'pt': docking ports, 'wb': module berths}) for the model
    # pack: designs 2-6 and the standard set's
    # Depots and core (by_depot1-3, by_core: the same models with the guns left off and plinths on the seats)
    out={}
    for n in range(1,7):
        pre='by_' if n==1 else 'by_d%d_'%n
        for lv in (1,2,3):out[pre+'depot%d'%lv]=(lambda n,l:lambda:_depot_full(n,l))(n,lv)
        out[pre+'core']=(lambda n:lambda:_core_full(n))(n)
    return out
