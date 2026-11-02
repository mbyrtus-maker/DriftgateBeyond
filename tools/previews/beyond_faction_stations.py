# Driftgate Beyond: the factions' stations and depots, each in its faction's design language, and the freeport in the neutral
# company style (preview, not in the model pack yet). First pass. Up is +y.
#   Halcyon  a great lens disc with a glass crown, a spire and dish, three swept arms ending in emitter nodes, hangars in the rim
#   Varkesh  a stepped hex fortress: armoured tiers, hangar slots in the walls, pincer docking clamps, heavy turrets, exhaust stacks
#   Ostrova  a faceted crystal spire: a great horizontal halo with crystal holds, two reactor halos crossed in an X round the head,
#            a crystal cluster at the root, docking spars
#   Freeport a trade harbour unlike any player base: a lit bazaar globe on a docking plaza, cargo piers, two corporate spires
import math
import numpy as np
from beyond_hulls import Mesh,LIGHT,MID,DARK,ACC,GLASS,GLOW,WIN,box,plate,ring
from beyond_work import crystal
from beyond_capitals import tube,mouth,bridge_varkesh,main_turret
from beyond_recon import dish
from beyond_stations import ry,frame_y,put,outward,drum,truss,tank,radiator,floods,mast,collar,market_wing,container
PI=math.pi
ZY=np.array([[1.,0,0],[0,0,1],[0,-1,0]])    # local +z to world +y

def lathe(M,prof,n=24,top=(LIGHT,1.0),side=(LIGHT,.93),bot=(MID,.88),c=(0,0,0),off=0.0,alt=0.0,caps=True):
    # a solid of revolution with n sides from a profile [(y,r)]; faces shaded by which way they face (up, out, down)
    c=np.array(c,float);A=[off+2*PI*j/n for j in range(n)]
    R=[[c+[math.cos(a)*r,y,math.sin(a)*r] for a in A] for y,r in prof]
    for i in range(len(prof)-1):
        ax=c+[0,(prof[i][0]+prof[i+1][0])/2,0]
        for j in range(n):
            p,q,r_,s=R[i][j],R[i][(j+1)%n],R[i+1][(j+1)%n],R[i+1][j]
            nn=np.cross(r_-p,q-p);ln=np.linalg.norm(nn)
            if ln<1e-9:nn=np.cross(s-p,q-p);ln=np.linalg.norm(nn)
            if ln<1e-9:continue
            nn/=ln;cen=(p+q+r_+s)/4
            if nn@(cen-ax)<0:nn=-nn
            role,sh=top if nn[1]>.45 else bot if nn[1]<-.45 else side
            sh*=1-alt*(j%2)
            M.tri(p,q,r_,role,sh,ref=ax);M.tri(p,r_,s,role,sh,ref=ax)
    if caps:
        for k,dy in ((0,-1),(-1,1)):
            y,r=prof[k]
            if r<1e-3:continue
            cc=c+[0,y,0];role,sh=top if dy>0 else bot
            for j in range(n):M.tri(cc,R[k][j],R[k][(j+1)%n],role,sh*.95,ref=cc-[0,dy,0])
def band(M,y,r,n=24,h=.06,role=WIN,off=0.0,c=(0,0,0)):
    lathe(M,[(y-h/2,r),(y+h/2,r)],n,(role,1.0),(role,1.0),(role,1.0),c,off,caps=False)
def zdir(d):
    # a rotation taking local +z to direction d
    return frame_y(d)@ZY
def crystal_at(M,base,d,length,w):
    B=Mesh();crystal(B,0,length,w,w);put(M,B,base,zdir(d))
def node(M,c,r,role=WIN):M.blob(tuple(c),r,role,sub=1,noise=0)
def hpd(M,c,s=1.0,role=MID,up=True):
    # a point-defence turret at station scale: a base, a dome, twin barrels (+z)
    c=np.array(c,float);k=1 if up else -1
    drum(M,c,c+[0,k*.08*s,0],.22*s,DARK,10);M.blob(tuple(c+[0,k*.14*s,0]),.18*s,role,sub=1,squash=(1,.7,1),noise=0)
    for sx in (1,-1):tube(M,[c+[sx*.06*s,k*.16*s,.08*s],c+[sx*.06*s,k*.16*s,.55*s]],[.025*s,.02*s],DARK,1.0,5)
def turned(M,fn,pos,a,*args):
    # build something that faces +z, then turn it to face outward along angle a
    B=Mesh();fn(B,*args);put(M,B,pos,outward(a))

# ============================================================== HALCYON
def swept_arm(M,a0,r0,r1,y0,y1,w0,h0,sweep=.9,n=9):
    pts=[];rad=[]
    for k in range(n):
        t=k/(n-1);a=a0+t*sweep;r=r0+(r1-r0)*t
        pts.append((math.cos(a)*r,y0+(y1-y0)*t*t,math.sin(a)*r));rad.append((w0*(1-t)+.1,h0*(1-t)+.05))
    M.tube(pts,rad,10,lambda i,j,n_,p:(LIGHT,.95 if j<5 else .85),cap0=False,cap1=True)
    e=np.array(pts[-1]);node(M,e,.24);ring(M,tuple(e),.27,.04,ACC,seg=16,sides=4,axis='y')
    return pts
def halcyon_station():
    M=Mesh(301)
    lathe(M,[(-1.3,.2),(-1.1,1.0),(-.55,2.7),(-.12,3.5),(.12,3.5),(.55,2.7),(.95,1.5),(1.2,.6),(1.3,.2)],36)   # the great lens
    for y in (-.05,.05):band(M,y,3.52,36,.04)
    M.blob((0,1.15,0),1.05,GLASS,sub=2,squash=(1,.42,1),noise=0)                                                # glass crown
    band(M,1.12,1.06,24,.05)
    tube(M,[(0,1.3,0),(0,3.0,0),(0,4.6,0)],[.28,.14,.04],LIGHT,.95,10)                                          # spire, dish, emitter
    dish(M,(0,2.5,0),.8);node(M,(0,3.6,0),.12);ring(M,(0,3.6,0),.32,.03,ACC,seg=16,sides=4,axis='y')
    for k in range(3):
        a0=PI/2+k*2*PI/3
        swept_arm(M,a0,3.1,6.2,-.05,-.55,.55,.2)                                                                  # three swept arms
        a=a0+PI/3;turned(M,lambda B:mouth(B,(0,0,0),1.2,.42,.45),(math.cos(a)*3.42,0,math.sin(a)*3.42),a)          # hangar in the rim
        floods(M,[(math.cos(a+s)*3.5,-.1,math.sin(a+s)*3.5) for s in (-.22,.22)],.06)
    for k in range(6):a=k*PI/3+PI/6;hpd(M,(math.cos(a)*2.05,.76,math.sin(a)*2.05),1.1)
    tube(M,[(0,-1.3,0),(0,-2.3,0)],[.32,.26],DARK,.9,10)                                                       # stem and lower pod
    lathe(M,[(-3.1,.1),(-2.85,.7),(-2.55,.95),(-2.3,.6),(-2.2,.2)],20,(LIGHT,1),(LIGHT,.92),(MID,.85))
    band(M,-2.6,.97,20,.05);node(M,(0,-3.15,0),.18,GLOW)
    return M
def halcyon_depot():
    M=Mesh(302)
    lathe(M,[(-.55,.1),(-.4,.7),(-.1,1.35),(.1,1.35),(.35,1.0),(.55,.5),(.62,.15)],28)
    for y in (-.03,.03):band(M,y,1.36,28,.03)
    M.blob((0,.55,0),.5,GLASS,sub=2,squash=(1,.45,1),noise=0)
    for a0 in (PI/2,PI/2+PI):swept_arm(M,a0,1.2,2.8,-.02,-.3,.32,.12,.8,7)
    a=0.0;turned(M,lambda B:mouth(B,(0,0,0),.75,.28,.3),(1.33,0,0),a)
    tube(M,[(0,.6,0),(0,1.6,0)],[.08,.03],LIGHT,.95,8);dish(M,(0,1.2,0),.32)
    tube(M,[(0,-.55,0),(0,-1.2,0)],[.14,.1],DARK,.9,8);lathe(M,[(-1.55,.05),(-1.4,.35),(-1.2,.4),(-1.1,.15)],16);node(M,(0,-1.58,0),.09,GLOW)
    for a in (PI/4,-3*PI/4):hpd(M,(math.cos(a)*.9,.42,math.sin(a)*.9),.7)
    return M

# ============================================================== VARKESH
def pincer_clamp(B,L=1.4,w=.7):
    # a Varkesh docking clamp: an armoured arm ending in two pincer prongs with lit tips
    from beyond_work import abox
    abox(B,(0,0,L/2),(w,w*.6,L),MID,(.9,.9))
    for sx in (1,-1):
        abox(B,(sx*w*.42,0,L+.35),(w*.28,w*.45,.7),MID,(.6,.6));node(B,(sx*w*.42,0,L+.72),.06)
    box(B,(0,0,L+.02),(w*1.05,w*.35,.12),ACC)
def vstack(M,base,h=1.2,r=.22):
    b=np.array(base,float);box(M,tuple(b+[0,.08,0]),(r*2.4,.16,r*2.4),DARK);drum(M,b,b+[0,h,0],r,MID,8)
    ring(M,tuple(b+[0,h*.78,0]),r*1.05,r*.12,ACC,seg=12,sides=4,axis='y');M.blob(tuple(b+[0,h,0]),r*.8,DARK,sub=1,squash=(1,.3,1),noise=0)
def war_blade(M,a,pts,th=.28,turret=None):
    # a thick armoured blade standing out from the hull along angle a; pts are (radius,y) of a convex outline,
    # with an amber edge along its top and an optional turret riding it
    P=[np.array([math.cos(a)*r,y,math.sin(a)*r]) for r,y in pts]
    plate(M,P,th,MID,.95)
    tube(M,[P[-1],P[-2]],[th*.32,th*.32],ACC,1.0,5,cap0=False,cap1=False)
    if turret:r,y,sc=turret;B=Mesh();main_turret(B,(0,0,0),sc);put(M,B,(math.cos(a)*r,y,math.sin(a)*r),outward(a))
def varkesh_station():
    # a war fortress: a smooth twelve-faceted double spike with a knife-edged waist, six armoured blades rising from the waist like a
    # crown of spikes with heavy turrets riding them, three smaller blades below, hangar slots and pincer clamps in the waist,
    # a lit command band near the top spike
    M=Mesh(311)
    P=[(-3.4,.04),(-1.8,1.3),(-.7,2.9),(-.05,3.45),(.05,3.45),(.6,2.85),(1.5,1.7),(2.6,.95),(3.9,.3),(4.8,.02)]
    lathe(M,P,12,(MID,1.0),(LIGHT,.95),(DARK,.85),alt=.06)
    band(M,0,3.47,12,.1,ACC);band(M,1.5,1.72,12,.07,WIN);band(M,-.75,2.86,12,.06,WIN);band(M,2.95,.72,12,.12,WIN)
    for k in range(6):
        a=k*PI/3
        war_blade(M,a,[(2.9,.55),(2.9,-.75),(4.7,-.25),(6.6,1.9),(4.5,1.15)],.3,(5.4,1.45,1.6))                    # crown blades
    for k in range(3):
        a=PI/6+k*2*PI/3+PI/3
        war_blade(M,a,[(1.6,-1.9),(2.5,-.9),(3.5,-1.6),(4.2,-3.2)],.24)                                            # lower blades
    for k in range(6):
        a=PI/6+k*PI/3;r=3.3
        if k%2==0:turned(M,lambda B:mouth(B,(0,0,0),1.3,.45,.6),(math.cos(a)*r,-.25,math.sin(a)*r),a)               # hangar slots
        else:turned(M,lambda B:pincer_clamp(B,1.0,.55),(math.cos(a)*2.55,-.95,math.sin(a)*2.55),a)                   # pincer clamps
    for k in range(6):a=PI/6+k*PI/3;turned(M,lambda B:main_turret(B,(0,0,0),1.4),(math.cos(a)*2.0,1.35,math.sin(a)*2.0),a)
    tube(M,[(0,4.6,0),(0,6.0,0)],[.06,.02],LIGHT,.9,5);ring(M,(0,5.3,0),.25,.03,ACC,seg=12,sides=4,axis='y')
    floods(M,[(math.cos(PI/6+k*PI/3)*3.5,.15,math.sin(PI/6+k*PI/3)*3.5) for k in range(6)],.07)
    return M
def varkesh_depot():
    # the fortress in small: a twelve-faceted double spike, three crown blades, one hangar slot, one pincer clamp, a heavy turret on top
    M=Mesh(312)
    lathe(M,[(-1.5,.03),(-.75,.6),(-.3,1.25),(.0,1.4),(.3,1.15),(.8,.7),(1.4,.3),(1.9,.02)],12,(MID,1.0),(LIGHT,.95),(DARK,.85),alt=.06)
    band(M,0,1.41,12,.06,ACC);band(M,.6,.82,12,.04,WIN)
    for k in range(3):a=PI/2+k*2*PI/3;war_blade(M,a,[(1.2,.25),(1.2,-.35),(2.0,-.1),(2.8,.85),(1.9,.5)],.16)
    a=PI/2+PI/3;turned(M,lambda B:mouth(B,(0,0,0),.6,.25,.3),(math.cos(a)*1.33,-.1,math.sin(a)*1.33),a)
    a=PI/2+PI;turned(M,lambda B:pincer_clamp(B,.6,.32),(math.cos(a)*1.05,-.4,math.sin(a)*1.05),a)
    main_turret(M,(0,1.15,.0),1.1)
    return M

# ============================================================== OSTROVA
OFF8=PI/8
def ostrova_station():
    # a cluster of crystal spires: a tall faceted main spire with lit crystal bands rising from a faceted plinth, six great crystals of
    # different heights round it leaning outward, smaller crystals between, a crystal root below, the great halo with turrets and
    # crystal holds circling the cluster, docking spars ending in faceted pods
    M=Mesh(321)
    lathe(M,[(-1.6,.6),(-1.0,2.2),(-.2,2.5),(.3,2.2),(.5,1.4)],8,(LIGHT,1.0),(LIGHT,.95),(MID,.88),off=OFF8,alt=.08)   # plinth
    band(M,-.45,2.36,8,.1,WIN,OFF8)
    lathe(M,[(.3,1.0),(1.5,1.05),(3.5,.8),(5.5,.42),(7.2,.02)],8,(LIGHT,1.0),(LIGHT,.95),(MID,.88),off=OFF8,alt=.08)   # main spire
    for y,r in ((1.6,1.06),(3.6,.79),(5.2,.48)):band(M,y,r,8,.12,WIN,OFF8)
    g=np.random.default_rng(5)
    for k in range(6):                                                                                            # six great crystal spires
        a=k*PI/3+PI/6;L=(3.6,5.2,3.0,4.6,3.3,5.6)[k];lean=.22+.08*(k%2)
        b=np.array([math.cos(a)*1.55,-.4,math.sin(a)*1.55]);d=np.array([math.cos(a)*lean,1,math.sin(a)*lean])
        crystal_at(M,b-d/np.linalg.norm(d)*.9,d,L+.9,.42+.04*(k%3))
    for k in range(6):                                                                                            # smaller crystals between
        a=k*PI/3;b=np.array([math.cos(a)*2.1,-.2,math.sin(a)*2.1]);d=np.array([math.cos(a)*.6,1,math.sin(a)*.6])
        crystal_at(M,b-d/np.linalg.norm(d)*.5,d,1.6+.5*(k%2),.24)
    for k in range(7):                                                                                            # crystal root
        a=k*2*PI/7;d=np.array([math.cos(a)*.5,-1,math.sin(a)*.5]);crystal_at(M,(math.cos(a)*.6,-1.3,math.sin(a)*.6),d,1.3+.5*(k%3),.26)
    ring(M,(0,.9,0),4.9,.2,ACC,seg=64,sides=8,axis='y')                                                          # the great halo
    for k in range(4):
        a=k*PI/2;tube(M,[(math.cos(a)*1.2,.9,math.sin(a)*1.2),(math.cos(a)*4.75,.9,math.sin(a)*4.75)],[.11,.08],LIGHT,.92,6)
        hpd(M,(math.cos(a)*4.9,1.1,math.sin(a)*4.9),1.2,ACC)
        a2=a+PI/4;c=np.array([math.cos(a2)*4.9,.9,math.sin(a2)*4.9]);t=np.array([-math.sin(a2),0,math.cos(a2)])
        crystal_at(M,c-t*.8,t,1.6,.36)
    for k in range(3):                                                                                            # docking spars with faceted pods
        a=k*2*PI/3+PI/2;e=np.array([math.cos(a)*3.6,-1.2,math.sin(a)*3.6])
        tube(M,[(math.cos(a)*1.9,-1.1,math.sin(a)*1.9),e],[.12,.08],MID,.95,6)
        B=Mesh();lathe(B,[(-.5,.02),(-.25,.3),(.25,.3),(.5,.02)],8,off=OFF8,alt=.08);band(B,0,.31,8,.06,WIN,OFF8);put(M,B,e,frame_y((math.cos(a),0,math.sin(a))))
    return M
def ostrova_depot():
    # a squat faceted pylon ringed by three tall crystal holds standing like pillars, a crown ring tying their tips together,
    # a crystal root and one docking spar: the station's halo and spire, but its own silhouette
    M=Mesh(322)
    lathe(M,[(-1.2,.03),(-.8,.4),(-.3,.62),(.7,.62),(1.1,.4),(1.35,.03)],8,(LIGHT,1.0),(LIGHT,.95),(MID,.88),off=OFF8,alt=.08)
    band(M,.2,.63,8,.1,WIN,OFF8)
    for k in range(3):
        a=PI/2+k*2*PI/3;c=np.array([math.cos(a)*1.15,0,math.sin(a)*1.15])
        crystal_at(M,c-[0,.9,0],(0,1,0),2.4,.26)                                                                    # crystal holds as pillars
        tube(M,[(math.cos(a)*.6,-.1,math.sin(a)*.6),c-[0,.1,0]],[.06,.05],LIGHT,.92,5)
        tube(M,[(math.cos(a)*.62,.5,math.sin(a)*.62),c+[0,.5,0]],[.05,.04],LIGHT,.92,5)
    ring(M,(0,1.55,0),1.15,.07,ACC,seg=36,sides=6,axis='y')                                                         # crown ring over the tips
    for k in range(3):a=PI/2+k*2*PI/3+PI/3;crystal_at(M,(math.cos(a)*.12,-1.0,math.sin(a)*.12),(math.cos(a)*.4,-1,math.sin(a)*.4),.6,.12)
    e=np.array([1.7,-.4,-.9]);tube(M,[(.45,-.35,-.25),e],[.06,.045],MID,.95,6)
    B=Mesh();lathe(B,[(-.28,.02),(-.14,.17),(.14,.17),(.28,.02)],8,off=OFF8);band(B,0,.18,8,.04,WIN,OFF8);put(M,B,e,frame_y((1,0,-.5)))
    hpd(M,(0,1.35,0),.8,ACC)
    return M

# ============================================================== FREEPORT
def freeport():
    # a trade harbour, nothing like a player station: a great lit globe (the bazaar) sitting on a broad docking plaza with twelve
    # berths round its rim, four long cargo piers stacked with containers, two tall corporate spires (one per corporation) each with
    # its sign, the freeport light on a mast above, a keel of tanks below
    M=Mesh(331)
    prof=[(y,max(r,.02)) for y,r in sorted([(math.sin(t)*2.3+1.5,math.cos(t)*2.3) for t in np.linspace(-PI/2,PI/2,13)])]
    lathe(M,prof,28,(LIGHT,1.0),(LIGHT,.94),(MID,.88),alt=.05)                                                  # the bazaar globe
    for t in (-.3,.05,.4,.75):band(M,math.sin(t)*2.3+1.5,math.cos(t)*2.3+.02,28,.09)                              # lit decks
    lathe(M,[(-.25,2.0),(-.25,5.9),(-.05,6.1),(.15,5.9),(.15,2.0)],48,(MID,1.0),(LIGHT,.92),(DARK,.85),caps=False)   # docking plaza
    band(M,-.05,6.11,48,.06,ACC);band(M,.16,2.6,48,.1,ACC);band(M,.16,4.6,48,.05,WIN)
    for k in range(12):                                                                                          # twelve berths on the rim
        a=k*PI/6+PI/12;c=np.array([math.cos(a)*5.3,.17,math.sin(a)*5.3]);t=np.array([-math.sin(a),0,math.cos(a)]);n=np.array([math.cos(a),0,math.sin(a)])
        plate(M,[c-t*.35-n*.4,c+t*.35-n*.4,c+t*.35+n*.4,c-t*.35+n*.4],.03,DARK,.9);ring(M,tuple(c+[0,.03,0]),.28,.025,ACC,seg=16,sides=4,axis='y')
        floods(M,[c+n*.75+[0,.05,0]],.05)
    for k in range(4):                                                                                           # four cargo piers with container stacks
        a=k*PI/2+PI/4;n=np.array([math.cos(a),0,math.sin(a)]);t=np.array([-math.sin(a),0,math.cos(a)])
        B=Mesh();box(B,(0,0,1.9),(.7,.3,3.8),MID)
        for z in (.8,1.7,2.6,3.5):
            for x in (-.5,.5):container(B,(x,.1,z),(.4,.34,.75),MID)
            container(B,(0,.42,z),(.4,.34,.75),MID if z!=1.7 else LIGHT)
        floods(B,[(0,.2,3.85)],.06)
        put(M,B,n*5.9+[0,-.08,0],outward(a))
    for a,h in ((0.0,6.2),(PI,5.2)):                                                                              # two corporate spires
        b=np.array([math.cos(a)*3.6,.15,math.sin(a)*3.6]);n=np.array([math.cos(a),0,math.sin(a)]);t=np.array([-math.sin(a),0,math.cos(a)])
        lathe(M,[(0,.55),(h*.5,.4),(h*.85,.25),(h,.02)],4,(LIGHT,1.0),(LIGHT,.93),(MID,.88),c=b,off=PI/4+a,alt=.08)
        for f in (.3,.5,.7):band(M,h*f,.5-.3*f+.02,4,.06,WIN,PI/4+a,b)
        cc=b+[0,h*.62,0]+n*.42
        plate(M,[cc-t*.75-[0,.45,0],cc+t*.75-[0,.45,0],cc+t*.75+[0,.45,0],cc-t*.75+[0,.45,0]],.08,ACC,1.0)        # corporate sign
        tube(M,[b+[0,h*.62,0],cc],[.05,.05],DARK,.9,5)
    tube(M,[(0,3.75,0),(0,5.7,0)],[.12,.05],LIGHT,.9,8);node(M,(0,5.8,0),.3)                                      # the freeport light
    ring(M,(0,5.8,0),.6,.05,WIN,seg=24,sides=4,axis='y');ring(M,(0,4.9,0),.4,.04,ACC,seg=20,sides=4,axis='y')
    lathe(M,[(-.25,1.9),(-1.4,1.2),(-2.6,.5),(-3.4,.08)],16,(MID,1.0),(MID,.92),(DARK,.85),alt=.05)             # keel
    for a in np.linspace(0,2*PI,4,endpoint=False)+PI/4:tank(M,(math.cos(a)*1.5,-1.4,math.sin(a)*1.5),.55)
    tube(M,[(0,-3.4,0),(0,-4.6,0)],[.06,.02],LIGHT,.9,5);node(M,(0,-4.65,0),.1)
    return M

FACTION_STATIONS=[('halcyon','Halcyon Accord',halcyon_station,halcyon_depot),('varkesh','Varkesh Dominion',varkesh_station,varkesh_depot),
                  ('ostrova','Ostrova Collective',ostrova_station,ostrova_depot)]
