# Driftgate Beyond: the factions' stations and depots, each in its faction's design language, and the freeport in the neutral
# company style (preview, not in the model pack yet). First pass. Up is +y.
#   Halcyon  a great lens disc with a glass crown, a spire and dish, three swept arms ending in emitter nodes, hangars in the rim
#   Varkesh  a stepped hex fortress: armoured tiers, hangar slots in the walls, pincer docking clamps, heavy turrets, exhaust stacks
#   Ostrova  nothing touches: a spire in floating faceted sections, floating crystal spires, a helix of shards, free-floating halos,
#            a crystal cluster at the root, docking spars
#   Freeport the company style rebuilt as a grand horizontal spindle: two great wheels, a lit bazaar hub, two corporate towers,
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
    plate(M,P,th,LIGHT,1.05)
    tube(M,[P[-1],P[-2]],[th*.32,th*.32],ACC,1.0,5,cap0=False,cap1=False)
    if turret:r,y,sc=turret;B=Mesh();main_turret(B,(0,0,0),sc);put(M,B,(math.cos(a)*r,y,math.sin(a)*r),outward(a))
def varkesh_station():
    # a war fortress: a smooth twelve-faceted double spike with a knife-edged waist, six armoured blades rising from the waist like a
    # crown of spikes with heavy turrets riding them, three smaller blades below, hangar slots and pincer clamps in the waist,
    # a lit command band near the top spike
    M=Mesh(311)
    P=[(-3.4,.04),(-1.8,1.3),(-.7,2.9),(-.05,3.45),(.05,3.45),(.6,2.85),(1.5,1.7),(2.6,.95),(3.9,.3),(4.8,.02)]
    lathe(M,P,12,(MID,1.0),(LIGHT,.97),(LIGHT,1.7),alt=.06)
    band(M,0,3.47,12,.1,ACC);band(M,1.5,1.72,12,.07,WIN);band(M,-.75,2.86,12,.06,WIN);band(M,2.95,.72,12,.12,WIN)
    band(M,-1.25,2.2,12,.08,WIN);band(M,-1.75,1.36,12,.07,ACC);band(M,-2.3,.98,12,.07,WIN);node(M,(0,-3.45,0),.14)   # a lit underside
    floods(M,[(math.cos(k*PI/3)*1.95,-1.45,math.sin(k*PI/3)*1.95) for k in range(6)],.08)
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
    lathe(M,[(-1.5,.03),(-.75,.6),(-.3,1.25),(.0,1.4),(.3,1.15),(.8,.7),(1.4,.3),(1.9,.02)],12,(MID,1.0),(LIGHT,.97),(LIGHT,1.7),alt=.06)
    band(M,-.5,.84,12,.04,WIN);band(M,-.9,.48,12,.04,ACC)
    band(M,0,1.41,12,.06,ACC);band(M,.6,.82,12,.04,WIN)
    for k in range(3):a=PI/2+k*2*PI/3;war_blade(M,a,[(1.2,.25),(1.2,-.35),(2.0,-.1),(2.8,.85),(1.9,.5)],.16)
    a=PI/2+PI/3;turned(M,lambda B:mouth(B,(0,0,0),.6,.25,.3),(math.cos(a)*1.33,-.1,math.sin(a)*1.33),a)
    a=PI/2+PI;turned(M,lambda B:pincer_clamp(B,.6,.32),(math.cos(a)*1.05,-.4,math.sin(a)*1.05),a)
    main_turret(M,(0,1.15,.0),1.1)
    return M

# ============================================================== OSTROVA
OFF8=PI/8
def float_seg(M,c,y0,y1,r,glow=True):
    # one floating section of a faceted spire: an octagonal bipyramid-ended prism, with a glowing lens hovering under it
    h=y1-y0;lathe(M,[(y0,.02),(y0+h*.3,r),(y1-h*.42,r*.78),(y1,.02)],8,(LIGHT,1.0),(LIGHT,.95),(MID,.9),c=c,off=OFF8,alt=.08)
    band(M,y0+h*.45,r*.95+.01,8,h*.08,WIN,OFF8,c)
    if glow:M.blob(tuple(np.array(c,float)+[0,y0-.18,0]),r*.45,WIN,sub=1,squash=(1,.25,1),noise=0)
def tilted_ring(M,c,R,r,tilt,yaw,role=ACC,seg=64):
    B=Mesh();ring(B,(0,0,0),R,r,role,seg=seg,sides=8,axis='y')
    c_,s_=math.cos(tilt),math.sin(tilt);Rx=np.array([[1,0,0],[0,c_,-s_],[0,s_,c_]])
    put(M,B,c,ry(yaw)@Rx)
    return ry(yaw)@Rx
def ostrova_station():
    # nothing touches: a main spire in four floating faceted sections with glowing lenses in the gaps, six great crystal spires
    # floating in a ring round it at different heights, a helix of crystal shards climbing it, two halos floating free at different
    # tilts with turrets and crystal holds, an inverted crystal cluster hanging below, floating docking pods
    M=Mesh(321);O=(0,0,0)
    for y0,y1,r in ((-1.6,.2,1.15),(.55,2.5,1.0),(2.85,4.5,.72),(4.85,6.2,.45)):float_seg(M,O,y0,y1,r)
    crystal_at(M,(0,6.3,0),(0,1,0),1.6,.22)                                                                      # the crown shard
    for k in range(6):                                                                                            # six floating crystal spires
        a=k*PI/3+PI/6;L=(3.4,5.0,2.8,4.6,3.1,5.4)[k];yb=(-1.2,-.4,-.9,-.2,-1.0,-.6)[k];lean=.14+.06*(k%2)
        d=np.array([math.cos(a)*lean,1,math.sin(a)*lean]);crystal_at(M,(math.cos(a)*2.5,yb,math.sin(a)*2.5),d,L,.42+.05*(k%3))
    for k in range(16):                                                                                           # helix of shards
        t=k/15;a=t*3.2*PI;r=3.9-2.1*t;y=-1.4+7.0*t
        d=np.array([-math.sin(a),.9,math.cos(a)]);crystal_at(M,(math.cos(a)*r,y,math.sin(a)*r),d,.65-.25*t,.13-.04*t)
    for (R,tilt,yaw,y,turrets) in ((4.8,.2,0.0,.9,True),(5.6,-.14,PI/3,1.6,False)):                               # two free-floating halos
        Rm=tilted_ring(M,(0,y,0),R,.2 if turrets else .12,tilt,yaw)
        for k in range(4 if turrets else 6):
            a=k*2*PI/(4 if turrets else 6);p=Rm@np.array([math.cos(a)*R,0,math.sin(a)*R])+[0,y,0]
            if turrets:hpd(M,p+Rm@np.array([0,.2,0]),1.2,ACC)
            a2=a+PI/(4 if turrets else 6);q=Rm@np.array([math.cos(a2)*R,0,math.sin(a2)*R])+[0,y,0];t_=Rm@np.array([-math.sin(a2),0,math.cos(a2)])
            crystal_at(M,q-t_*.7,t_,1.4,.3 if turrets else .22)
    for k in range(6):                                                                                            # inverted cluster hanging below
        a=k*PI/3;d=np.array([math.cos(a)*.35,-1,math.sin(a)*.35]);crystal_at(M,(math.cos(a)*.45,-2.5,math.sin(a)*.45),d,1.2+.6*(k%2),.24)
    crystal_at(M,(0,-2.4,0),(0,-1,0),2.6,.32)
    for k in range(3):                                                                                            # floating docking pods
        a=k*2*PI/3+PI/2;e=np.array([math.cos(a)*3.7,-1.9,math.sin(a)*3.7])
        B=Mesh();lathe(B,[(-.55,.02),(-.25,.32),(.25,.32),(.55,.02)],8,off=OFF8,alt=.08);band(B,0,.33,8,.07,WIN,OFF8);put(M,B,e,frame_y((math.cos(a),0,math.sin(a))))
        node(M,e-np.array([math.cos(a),0,math.sin(a)])*.75,.09)
    return M
def ostrova_depot():
    # floating parts in small: a two-section faceted pylon with a glowing lens in the gap, three crystal holds floating round it as
    # pillars, a crown ring hovering over their tips, a crystal hanging below, a floating docking pod
    M=Mesh(322);O=(0,0,0)
    float_seg(M,O,-1.2,.3,.62,False);float_seg(M,O,.6,1.5,.42)
    for k in range(3):
        a=PI/2+k*2*PI/3;crystal_at(M,(math.cos(a)*1.3,-.9,math.sin(a)*1.3),(0,1,0),2.4,.26)
    tilted_ring(M,(0,1.85,0),1.3,.07,.12,PI/5)
    crystal_at(M,(0,1.6,0),(0,1,0),.9,.13)
    for k in range(3):a=k*2*PI/3+PI/3;crystal_at(M,(math.cos(a)*.2,-1.45,math.sin(a)*.2),(math.cos(a)*.4,-1,math.sin(a)*.4),.6,.12)
    e=np.array([1.9,-.5,-1.0]);B=Mesh();lathe(B,[(-.28,.02),(-.14,.17),(.14,.17),(.28,.02)],8,off=OFF8);band(B,0,.18,8,.04,WIN,OFF8);put(M,B,e,frame_y((1,0,-.5)))
    return M

# ============================================================== FREEPORT
def freeport():
    # the company style (drums, lattice trusses, rings, containers, radiators, floodlights) rebuilt as a grand horizontal spindle,
    # unlike the upright player station: a long spine with a docking crown at each end, two great wheels turning on it, a lit
    # bazaar hub in the middle, two corporate towers rising from the hub (one per corporation), three market wings hanging below,
    # container yards and tanks along the spine, radiator wings, floodlights everywhere
    M=Mesh(331)
    drum(M,(0,0,-6.0),(0,0,6.0),.8,MID,16,bands=(.08,.3,.7,.92))                                                 # spine
    drum(M,(0,0,-1.4),(0,0,1.4),1.9,LIGHT,24,bands=(.08,.92))                                                    # bazaar hub
    for z in (-.7,-.2,.3,.8):B=Mesh();ring(B,(0,0,0),1.92,.05,WIN,seg=48,sides=4,axis='z');put(M,B,(0,0,z))
    for z in (-3.8,3.8):                                                                                          # two great wheels
        ring(M,(0,0,z),3.6,.36,MID,seg=64,sides=10,axis='z');ring(M,(0,0,z),3.6,.37,WIN,seg=64,sides=4,axis='z')
        drum(M,(0,0,z-.5),(0,0,z+.5),1.1,LIGHT,16,bands=(.2,.8))
        for a in np.linspace(0,2*PI,6,endpoint=False)+PI/6:truss(M,(math.cos(a)*1.1,math.sin(a)*1.1,z),(math.cos(a)*3.3,math.sin(a)*3.3,z),.3,.03)
        floods(M,[(math.cos(a)*3.6,math.sin(a)*3.6,z+.42) for a in np.linspace(0,2*PI,12,endpoint=False)],.07)
    for z,s_ in ((-6.0,-1),(6.0,1)):                                                                               # docking crowns at both ends
        drum(M,(0,0,z),(0,0,z+s_*.7),1.35,DARK,18)
        for a in np.linspace(0,2*PI,6,endpoint=False):collar(M,(math.cos(a)*1.3,math.sin(a)*1.3,z+s_*.35),.24,(math.cos(a),math.sin(a),0))
        tube(M,[(0,0,z+s_*.7),(0,0,z+s_*2.2)],[.08,.03],LIGHT,.9,6);M.blob((0,0,z+s_*2.25),.12,WIN,sub=1,noise=0)
    for x,h,lit in ((-.85,3.6,True),(.85,2.9,False)):                                                              # two corporate towers
        b=np.array([x,1.7,0.0]);drum(M,b,b+[0,h,0],.48,LIGHT,12,bands=() if lit else (.3,.55,.8))
        if lit:
            for f in (.35,.6,.85):B=Mesh();ring(B,(0,0,0),.49,.05,WIN,seg=20,sides=4,axis='y');put(M,B,b+[0,h*f,0])
        M.blob(tuple(b+[0,h,0]),.48,LIGHT,sub=2,squash=(1,.5,1),noise=0);mast(M,b+[0,h+.2,0],1.0,.04)
        sx=1 if x>0 else -1;cc=b+[sx*.55,h*.65,0]
        plate(M,[cc+[0,-.45,-.8],cc+[0,-.45,.8],cc+[0,.45,.8],cc+[0,.45,-.8]],.08,ACC,1.0)                         # corporate sign
    for k,a in enumerate((-PI/2,-PI/2-.75,-PI/2+.75)):                                                             # three market wings below
        d=np.array([math.cos(a),math.sin(a),0]);put(M,market_wing(),d*1.85,zdir(d),1.15)
    for z in (-2.3,2.3):                                                                                          # container yards on the spine
        for sx in (1,-1):
            truss(M,(sx*.8,0,z-.7),(sx*1.6,0,z-.7),.2,.02,3);truss(M,(sx*.8,0,z+.7),(sx*1.6,0,z+.7),.2,.02,3)
            for y in (-.42,0,.42):container(M,(sx*1.3,y,z),(.5,.4,1.5),MID if y else LIGHT)
    for z in (-5.0,5.0):
        for a in (PI/4,3*PI/4,5*PI/4,7*PI/4):tank(M,(math.cos(a)*1.15,math.sin(a)*1.15,z),.5)
    for z in (-4.8,4.8):radiator(M,(0,.8,z),(0,2.6,z),.9,3)
    return M

FACTION_STATIONS=[('halcyon','Halcyon Accord',halcyon_station,halcyon_depot),('varkesh','Varkesh Dominion',varkesh_station,varkesh_depot),
                  ('ostrova','Ostrova Collective',ostrova_station,ostrova_depot)]
