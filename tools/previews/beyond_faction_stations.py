# Driftgate Beyond: the factions' stations and depots, each in its faction's design language, and the freeport
# (preview, not in the model pack yet). Up is +y.
#   Halcyon  a great lens disc with a glass crown, a spire and dish, three swept arms ending in emitter nodes, hangars in the rim
#   Varkesh  the Talon Citadel: a blade-topped hex keep gripped by three great curved talons, armour scales, heavy turrets
#   Ostrova  nothing touches: a spire in floating sections, floating crystal spires, a helix of shards, three free-floating halos,
#            docking pods floating outside the halos, energy bridges linking the key pieces
#   Freeport a welcoming trade spindle: a lit glass atrium, promenade rings, welcome gates and berth flowers at both ends,
#            two corporate towers, hanging lanterns and strings of lights
import math
import numpy as np
from beyond_hulls import Mesh,LIGHT,MID,DARK,ACC,GLASS,GLOW,WIN,box,plate,ring
from beyond_work import crystal
from beyond_capitals import tube,mouth,bridge_varkesh,main_turret
from beyond_recon import dish
from beyond_stations import ry,frame_y,put,outward,drum,truss,tank,radiator,floods,mast,collar,market_wing,container
PI=math.pi
ZY=np.array([[1.,0,0],[0,0,1],[0,-1,0]])    # local +z to world +y

def lathe(M,prof,n=24,top=(LIGHT,1.0),side=(LIGHT,.93),bot=(MID,.88),c=(0,0,0),off=0.0,alt=0.0,caps=True,pick=None):
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
            role,sh=pick(i,j) if pick else top if nn[1]>.45 else bot if nn[1]<-.45 else side
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
def bridge(M,a,b,r=.045):
    # an Ostrova energy bridge: a thin glowing beam between two floating pieces, with a bright node at each end
    a=np.array(a,float);b=np.array(b,float);tube(M,[a,b],[r,r],GLOW,1.0,5,cap0=False,cap1=False);node(M,a,r*2.2);node(M,b,r*2.2)
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
def talon(M,a,path,w0,t0,edge=True):
    # a great curved claw in the radial plane at angle a: path is (radius,y) from root to tip; a hex section, deep in the plane of
    # the curve and thin across it, tapering to a point; a lit amber edge along its inner curve
    u=np.array([math.cos(a),0,math.sin(a)]);side=np.array([-math.sin(a),0,math.cos(a)])
    P=[u*r+[0,y,0] for r,y in path];n=len(P);S=[]
    for k in range(n):
        T=P[min(k+1,n-1)]-P[max(k-1,0)];T/=np.linalg.norm(T);N=np.cross(side,T);N/=np.linalg.norm(N)
        f=(1-k/(n-1))**.8;w=w0*f+.02;t=t0*f+.015
        S.append([P[k]+N*w,P[k]+N*w*.45+side*t,P[k]-N*w*.45+side*t,P[k]-N*w,P[k]-N*w*.45-side*t,P[k]+N*w*.45-side*t])
    for k in range(n-1):
        for j in range(6):
            role,sh=(LIGHT,1.0) if j in (1,2) else (MID,.95) if j in (0,3) else (LIGHT,.9)
            M.tri(S[k][j],S[k][(j+1)%6],S[k+1][(j+1)%6],role,sh,ref=P[k]);M.tri(S[k][j],S[k+1][(j+1)%6],S[k+1][j],role,sh,ref=P[k])
    if edge:tube(M,[s_[3] for s_ in S[1:-1]],[.05]*(n-2),ACC,1.0,4,cap0=False,cap1=False)
    return P
def varkesh_station():
    # the Talon Citadel: a tall hex keep with a blade-sharp crown and a chisel keel, gripped by three great curved talons that rise
    # from beneath it and curl in over its head, heavy turrets riding the talons, a collar of angled armour scales round its waist,
    # hangar slots between the talons, pincer clamps below, lit slits and a war beacon on the crown
    M=Mesh(311)
    lathe(M,[(-3.0,.03),(-2.0,.9),(-.9,1.75),(1.4,1.55),(3.0,1.15),(4.4,.7),(5.6,.03)],6,(MID,1.0),(LIGHT,.97),(LIGHT,1.6),off=PI/2,alt=.07)   # the keep
    for y,r in ((-.2,1.68),(2.2,1.36),(3.7,.92)):band(M,y,r,6,.09,WIN,PI/2)
    band(M,.5,1.62,6,.12,ACC,PI/2);band(M,-1.5,1.33,6,.08,WIN,PI/2)
    for k in range(12):                                                                                           # armour scales
        a=k*PI/6;u=np.array([math.cos(a),0,math.sin(a)]);t=np.array([-math.sin(a),0,math.cos(a)])
        r0,y0,r1,y1=1.6,1.25,2.45,.05
        plate(M,[u*r0+t*.45+[0,y0,0],u*r0-t*.45+[0,y0,0],u*r1-t*.62+[0,y1,0],u*r1+t*.62+[0,y1,0]],.1,LIGHT if k%2 else MID,1.0)
        tube(M,[u*r1-t*.6+[0,y1,0],u*r1+t*.6+[0,y1,0]],[.035,.035],ACC,1.0,4)
    for k in range(3):                                                                                            # three great talons
        a=PI/2+k*2*PI/3
        path=[(1.1,-2.3),(2.6,-2.0),(3.9,-.9),(4.5,.8),(4.3,2.6),(3.5,4.2),(2.4,5.3),(1.2,5.9)]
        talon(M,a,path,.85,.32)
        for (r,y) in ((4.55,.2),(4.2,2.9)):
            u=np.array([math.cos(a),0,math.sin(a)]);B=Mesh();main_turret(B,(0,0,0),1.6);put(M,B,u*(r+.25)+[0,y+.2,0],outward(a))
        a2=a+PI/3;u=np.array([math.cos(a2),0,math.sin(a2)])
        turned(M,lambda B:mouth(B,(0,0,0),1.1,.5,.6),u*1.62+[0,-.4,0],a2)                                           # hangar slots
        floods(M,[u*1.7+np.array([-math.sin(a2),0,math.cos(a2)])*s_*.7+[0,-.4,0] for s_ in (-1,1)],.07)
        turned(M,lambda B:pincer_clamp(B,1.1,.55),u*1.25+[0,-1.6,0],a2)                                            # pincer clamps
    tube(M,[(0,5.5,0),(0,7.0,0)],[.07,.02],LIGHT,.9,5);node(M,(0,7.05,0),.12,GLOW)                                # war beacon
    ring(M,(0,6.2,0),.3,.04,ACC,seg=12,sides=4,axis='y');node(M,(0,-3.05,0),.12)
    return M
def varkesh_depot():
    # the citadel in small: a hex keep with a blade crown, two talons curling over it, one hangar, one clamp, a heavy turret
    M=Mesh(312)
    lathe(M,[(-1.4,.03),(-.9,.45),(-.4,.8),(.6,.72),(1.4,.5),(2.1,.25),(2.6,.02)],6,(MID,1.0),(LIGHT,.97),(LIGHT,1.6),off=PI/2,alt=.07)
    band(M,.15,.78,6,.06,ACC,PI/2);band(M,1.0,.62,6,.05,WIN,PI/2)
    for a in (PI/2,PI/2+PI):
        talon(M,a,[(.5,-1.0),(1.3,-.85),(1.9,-.2),(2.1,.7),(1.8,1.6),(1.2,2.3),(.6,2.7)],.42,.16)
    a=0.0;turned(M,lambda B:mouth(B,(0,0,0),.6,.3,.35),(.72,-.2,0),a)
    turned(M,lambda B:pincer_clamp(B,.6,.32),(-.55,-.7,0),PI)
    B=Mesh();main_turret(B,(0,0,0),1.1);put(M,B,(0,.75,.62))
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
    # nothing touches: a main spire in four floating faceted sections with glowing lenses in the gaps and a crown shard, six great
    # crystal spires floating in a ring round it, a helix of crystal shards, three halos floating free (one thrown well off kilter),
    # an inverted crystal cluster below, docking pods floating outside the halos as separate faceted boxes, and energy bridges
    # linking the key pieces: the spire sections, the spires to the core, the halos to the core, the pods to the halos
    M=Mesh(321);O=(0,0,0)
    SEG=((-1.6,.2,1.15),(.55,2.5,1.0),(2.85,4.5,.72),(4.85,6.2,.45))
    for y0,y1,r in SEG:float_seg(M,O,y0,y1,r)
    for (a0,b0,_),(a1,b1,_) in zip(SEG,SEG[1:]):bridge(M,(0,b0+.02,0),(0,a1-.02,0),.06)
    crystal_at(M,(0,6.3,0),(0,1,0),1.6,.22)
    for k in range(6):
        a=k*PI/3+PI/6;L=(3.4,5.0,2.8,4.6,3.1,5.4)[k];yb=(-1.2,-.4,-.9,-.2,-1.0,-.6)[k];lean=.14+.06*(k%2)
        d=np.array([math.cos(a)*lean,1,math.sin(a)*lean]);b=np.array([math.cos(a)*2.5,yb,math.sin(a)*2.5]);crystal_at(M,b,d,L,.42+.05*(k%3))
        bridge(M,b+d/np.linalg.norm(d)*L*.3,(math.cos(a)*1.05,b[1]+L*.3,math.sin(a)*1.05))                          # spire to core
    for k in range(16):
        t=k/15;a=t*3.2*PI;r=3.9-2.1*t;y=-1.4+7.0*t
        d=np.array([-math.sin(a),.9,math.cos(a)]);crystal_at(M,(math.cos(a)*r,y,math.sin(a)*r),d,.65-.25*t,.13-.04*t)
    RINGS=((4.8,.2,0.0,.9,4,.2),(5.6,-.14,PI/3,1.6,6,.12),(6.3,.62,2*PI/3+.3,.3,5,.14))
    rm=[]
    for (R,tilt,yaw,y,n,th) in RINGS:
        Rm=tilted_ring(M,(0,y,0),R,th,tilt,yaw);rm.append((R,Rm,y))
        for k in range(n):
            a=k*2*PI/n;p=Rm@np.array([math.cos(a)*R,0,math.sin(a)*R])+[0,y,0]
            if n==4:hpd(M,p+Rm@np.array([0,.2,0]),1.2,ACC)
            a2=a+PI/n;q=Rm@np.array([math.cos(a2)*R,0,math.sin(a2)*R])+[0,y,0];t_=Rm@np.array([-math.sin(a2),0,math.cos(a2)])
            crystal_at(M,q-t_*.6,t_,1.2,.28 if n==4 else .2)
        for k in range(3):                                                                                        # halo to core
            a=k*2*PI/3+yaw*.5;p=Rm@np.array([math.cos(a)*(R-.15),0,math.sin(a)*(R-.15)])+[0,y,0]
            q=np.array([p[0],0,p[2]]);q=q/np.linalg.norm(q)*1.15+[0,p[1],0];bridge(M,p,q,.035)
    for k in range(6):
        a=k*PI/3;d=np.array([math.cos(a)*.35,-1,math.sin(a)*.35]);crystal_at(M,(math.cos(a)*.45,-2.5,math.sin(a)*.45),d,1.2+.6*(k%2),.24)
    crystal_at(M,(0,-2.4,0),(0,-1,0),2.6,.32);bridge(M,(0,-1.62,0),(0,-2.35,0),.06)
    for k in range(4):                                                                                            # docking pods outside the halos
        a=k*PI/2+PI/4;u=np.array([math.cos(a),0,math.sin(a)]);e=u*7.6+[0,-.3+.5*(k%2),0]
        B=Mesh();box(B,(0,0,0),(1.0,.62,1.3),LIGHT,(.8,.8));box(B,(0,0,.0),(1.04,.1,1.2),WIN);box(B,(0,0,.68),(.55,.32,.08),GLOW)
        put(M,B,e,outward(a+PI))
        R,Rm,y=rm[0];p=None;best=1e9
        for kk in range(48):
            aa=kk*2*PI/48;q=Rm@np.array([math.cos(aa)*R,0,math.sin(aa)*R])+[0,y,0];dd=np.linalg.norm(q-e)
            if dd<best:best=dd;p=q
        bridge(M,e-u*.75,p+(e-p)/np.linalg.norm(e-p)*.25,.04)
    return M
def ostrova_depot():
    # floating parts in small: a two-section faceted pylon with an energy bridge across the gap, three crystal pillars floating
    # round it, a ring floating round its middle, a docking pod floating outside the ring, energy bridges to each piece
    M=Mesh(322);O=(0,0,0)
    float_seg(M,O,-1.2,.3,.62,False);float_seg(M,O,.6,1.5,.42);bridge(M,(0,.32,0),(0,.58,0),.05)
    for k in range(3):
        a=PI/2+k*2*PI/3;crystal_at(M,(math.cos(a)*1.3,-.9,math.sin(a)*1.3),(0,1,0),2.4,.26)
        bridge(M,(math.cos(a)*1.15,0,math.sin(a)*1.15),(math.cos(a)*.66,0,math.sin(a)*.66),.035)
    tilted_ring(M,(0,-.05,0),1.75,.08,.1,PI/5)
    crystal_at(M,(0,1.6,0),(0,1,0),.9,.13)
    for k in range(3):a=k*2*PI/3+PI/3;crystal_at(M,(math.cos(a)*.2,-1.45,math.sin(a)*.2),(math.cos(a)*.4,-1,math.sin(a)*.4),.6,.12)
    a=-PI/6;u=np.array([math.cos(a),0,math.sin(a)]);e=u*2.7+[0,-.35,0]
    B=Mesh();box(B,(0,0,0),(.5,.32,.65),LIGHT,(.8,.8));box(B,(0,0,0),(.52,.05,.6),WIN);box(B,(0,0,.34),(.28,.16,.05),GLOW);put(M,B,e,outward(a+PI))
    bridge(M,e-u*.37,u*1.82+[0,-.1,0],.03)
    return M

# ============================================================== FREEPORT
YZ=ZY.T    # local +y to world +z
def lights_string(M,a,b,sag=.6,n=12):
    # a string of festival lights hanging between two points, alternating warm white and amber
    a=np.array(a,float);b=np.array(b,float)
    pts=[a+(b-a)*t-np.array([0,sag*4*t*(1-t),0]) for t in np.linspace(0,1,n)]
    tube(M,pts,[.015]*n,DARK,.9,4,cap0=False,cap1=False)
    for k,p in enumerate(pts[1:-1]):M.blob(tuple(p),.07,WIN if k%2 else ACC,sub=1,noise=0)
def freeport():
    # a welcoming trade spindle, not a player station: a lit glass atrium (the bazaar) in the middle of a smooth capsule spine,
    # two promenade rings with lit window stripes and lantern lights, welcome gates at both ends with flowers of berths inside them,
    # two corporate towers (one per corporation, unlike each other), lanterns hanging below the atrium, strings of lights between
    # the towers and the rings, lit billboards on the rings
    M=Mesh(331)
    B=Mesh();lathe(B,[(-6.6,.05),(-6.4,.6),(-6.0,.85),(6.0,.85),(6.4,.6),(6.6,.05)],18,(LIGHT,1.0),(LIGHT,.95),(MID,.9));put(M,B,(0,0,0),YZ)   # capsule spine
    for z in (-5.2,-1.9,1.9,5.2):B=Mesh();band(B,0,.87,18,.12,ACC);put(M,B,(0,0,z),YZ)
    prof=[(math.sin(t)*2.4,max(math.cos(t)*2.4,.03)) for t in np.linspace(-PI/2,PI/2,15)]                          # glass atrium
    lathe(M,prof,24,pick=lambda i,j:(WIN,1.0) if i in (3,5,7,9,11) else (GLASS,1.0))
    for k in range(6):B=Mesh();ring(B,(0,0,0),2.42,.05,LIGHT,seg=40,sides=4,axis='z');put(M,B,(0,0,0),ry(k*PI/6))   # ribs
    ring(M,(0,0,0),2.45,.09,ACC,seg=48,sides=5,axis='y')
    for z in (-3.7,3.7):                                                                                          # promenade rings
        ring(M,(0,0,z),3.5,.42,LIGHT,seg=64,sides=12,axis='z');ring(M,(0,0,z),3.92,.13,WIN,seg=64,sides=4,axis='z')
        for a in np.linspace(0,2*PI,4,endpoint=False)+PI/4:
            tube(M,[(math.cos(a)*.85,math.sin(a)*.85,z),(math.cos(a)*3.1,math.sin(a)*3.1,z)],[.1,.1],LIGHT,.95,8);node(M,(math.cos(a)*2.0,math.sin(a)*2.0,z),.13)
        for k in range(24):a=k*PI/12;M.blob((math.cos(a)*3.5,math.sin(a)*3.5,z+.46),.07,WIN if k%2 else ACC,sub=1,noise=0)
        plate(M,[(-1.0,3.95,z-.15),(1.0,3.95,z-.15),(1.0,4.75,z-.15),(-1.0,4.75,z-.15)],.08,ACC,1.0)               # billboard
        plate(M,[(-.85,4.05,z-.21),(.85,4.05,z-.21),(.85,4.65,z-.21),(-.85,4.65,z-.21)],.01,WIN,1.0)
    for z,sg in ((-6.6,-1),(6.6,1)):                                                                               # welcome gates and berth flowers
        zg=z+sg*1.6;ring(M,(0,0,zg),2.8,.16,ACC,seg=48,sides=6,axis='z')
        for k in range(16):a=k*PI/8;M.blob((math.cos(a)*2.8,math.sin(a)*2.8,zg+sg*.18),.09,WIN if k%2 else GLOW,sub=1,noise=0)
        for a in (PI/2,PI/2+2*PI/3,PI/2+4*PI/3):tube(M,[(math.cos(a)*.5,math.sin(a)*.5,z),(math.cos(a)*2.7,math.sin(a)*2.7,zg)],[.06,.06],LIGHT,.9,5)
        for k in range(6):
            a=k*PI/3+PI/6;e=np.array([math.cos(a)*2.0,math.sin(a)*2.0,z+sg*.3])
            tube(M,[(math.cos(a)*.6,math.sin(a)*.6,z-sg*.4),e],[.07,.05],LIGHT,.92,6)
            B=Mesh();plate(B,[(math.cos(t)*.42,0,math.sin(t)*.42) for t in np.linspace(0,2*PI,8,endpoint=False)],.05,MID,1.0)
            ring(B,(0,.04,0),.32,.03,ACC,seg=16,sides=4,axis='y');node(B,(0,.06,0),.06)
            put(M,B,e,frame_y((math.cos(a),math.sin(a),0)))
    for x,lit in ((-1.1,True),(1.1,False)):                                                                        # two corporate towers
        b=np.array([x,1.9,0.0])
        if lit:
            lathe(M,[(0,.55),(1.6,.48),(3.4,.36),(4.4,.2),(5.0,.02)],12,c=b,alt=.04)
            for y in (1.0,2.0,3.0):band(M,y,.5-.05*y+.02,12,.12,WIN,c=b)
            ring(M,tuple(b+[0,3.9,0]),.75,.06,ACC,seg=24,sides=4,axis='y');node(M,b+[0,5.05,0],.1)
            plate(M,[b+[-.7,2.2,.55],b+[.7,2.2,.55],b+[.7,2.9,.55],b+[-.7,2.9,.55]],.06,ACC,1.0)
        else:
            lathe(M,[(0,.6),(1.4,.6),(1.4,.48),(2.6,.48),(2.6,.36),(3.6,.36),(3.6,.02)],4,c=b,off=PI/4,alt=.06)
            for y in (.7,2.0,3.1):band(M,y,{.7:.61,2.0:.49,3.1:.37}[y],4,.1,WIN,PI/4,b)
            plate(M,[b+[-.9,3.7,0],b+[.9,3.7,0],b+[.9,4.5,0],b+[-.9,4.5,0]],.08,ACC,1.0);mast(M,b+[0,4.5,0],.7,.03)
    for (x,z) in ((-1.2,-.6),(0,.9),(1.1,-.3),(.4,-1.2),(-.7,1.1)):                                                 # lanterns under the atrium
        y0=-math.sqrt(max(2.4**2-x*x-z*z,0))+.05;L=.8+.5*((x+z)%1)
        tube(M,[(x,y0,z),(x,y0-L,z)],[.012,.012],DARK,.9,4);M.blob((x,y0-L-.15,z),.16,WIN,sub=1,squash=(1,1.3,1),noise=0)
    lights_string(M,(-1.1,6.4,0),(0,3.9,-3.7),1.0,14);lights_string(M,(-1.1,6.4,0),(0,3.9,3.7),1.0,14)            # strings of lights
    lights_string(M,(1.1,5.5,0),(2.76,2.76,-3.7),.8,12);lights_string(M,(1.1,5.5,0),(2.76,2.76,3.7),.8,12)
    return M

FACTION_STATIONS=[('halcyon','Halcyon Accord',halcyon_station,halcyon_depot),('varkesh','Varkesh Dominion',varkesh_station,varkesh_depot),
                  ('ostrova','Ostrova Collective',ostrova_station,ostrova_depot)]
