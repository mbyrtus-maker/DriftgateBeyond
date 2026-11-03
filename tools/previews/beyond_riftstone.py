# Driftgate Beyond: Riftstone, the dangerous embargoed asteroid (preview). A dark, jagged rock split by glowing rifts, with
# loose shards drifting off it and rift discharges arcing from the cracks; beside it an ordinary asteroid for scale and contrast.
# The rift glow uses its own colour ('rift'), unlike any power's.
import math
import numpy as np
from beyond_hulls import Mesh,GLOW,WIN,DARK
from beyond_capitals import tube
from beyond_stations import Rock,ROCK,ROCKD,put,frame_y,icosphere

class Jagged(Rock):
    # a sharper, more broken rock: deeper bumps and flat-cut facets
    def __init__(s,c,R,seed):
        super().__init__(c,R,seed,squash=(1.2,.82,1.05),nb=46,nc=5)
        g=np.random.default_rng(seed+1);s.B=[(c_,a*1.6,w*.75) for c_,a,w in s.B]
        s.cuts=[(v/np.linalg.norm(v),g.uniform(.82,.93)) for v in g.normal(size=(7,3))]
    def rad(s,d):
        r=super().rad(d);d=d/np.linalg.norm(d)
        for n,k in s.cuts:
            dot=d@n
            if dot>k:r=min(r,r*k/dot)
        return r
    def build(s,M,sub=3):
        V,F=icosphere(sub);P=[s.surf(v) for v in V];g=np.random.default_rng(5)
        for a,b,c in F:M.tri(P[a],P[b],P[c],ROCKD if g.random()<.7 else ROCK,.8+.15*g.random(),ref=s.c)

def arc(rk,a,b,n=28,jit=.05,seed=0):
    # surface points along the great circle from direction a to b, jittered into a zigzag crack
    g=np.random.default_rng(seed);a=np.array(a,float);b=np.array(b,float);a/=np.linalg.norm(a);b/=np.linalg.norm(b)
    om=math.acos(np.clip(a@b,-1,1));pts=[]
    for i in range(n+1):
        t=i/n;d=(math.sin((1-t)*om)*a+math.sin(t*om)*b)/math.sin(om)
        if 0<i<n:d=d+g.normal(size=3)*jit;d/=np.linalg.norm(d)
        pts.append(rk.surf(d,-.012))
    return pts

def riftstone(seed=11,R=1.0):
    M=Mesh(seed);rk=Jagged((0,0,0),R,seed);rk.build(M);g=np.random.default_rng(seed+7)
    # rifts: glowing cracks across the rock, the widest one splitting it nearly in two
    rifts=[((1,.2,.1),(-1,.3,-.2),.045),((0,1,.3),(.2,-.4,1),.03),((.6,-.5,-.8),(-.4,.6,-.7),.028),((-.8,-.3,.5),(.3,-1,.2),.024),((.9,.6,-.2),(.1,.2,1),.02)]
    for k,(a,b,r) in enumerate(rifts):
        P=arc(rk,a,b,seed=seed+k);tube(M,P,[r*(.4+.6*math.sin(math.pi*i/(len(P)-1))) for i in range(len(P))],GLOW,1.0,5,cap0=False,cap1=False)
        for i in range(3,len(P)-3,7):M.blob(tuple(P[i]),r*1.5,WIN,sub=1,noise=0)
    # loose shards drifting off the surface, some glowing from inside
    for k in range(9):
        d=g.normal(size=3);d/=np.linalg.norm(d);base=rk.surf(d)+d*R*g.uniform(.12,.4);L=R*g.uniform(.12,.26);w=L*.28
        B=Mesh();tube(B,[(0,-L/2,0),(0,0,0),(0,L/2,0)],[.002,w,.002],GLOW if k%3==0 else ROCKD,.9,5)
        tilt=d+g.normal(size=3)*.8;put(M,B,base,frame_y(tilt/np.linalg.norm(tilt)))
    # rift discharges: jagged arcs leaping off the cracks
    for k,(a,b,r) in enumerate(rifts[:3]):
        P=arc(rk,a,b,seed=seed+k);p=np.array(P[len(P)//2+k*3-3]);n=p/np.linalg.norm(p);u=np.cross(n,[0,1,0]);u/=np.linalg.norm(u)+1e-9
        pts=[p];q=p.copy()
        for i in range(6):q=q+n*R*.11+u*R*g.uniform(-.09,.09)+np.cross(n,u)*R*g.uniform(-.06,.06);pts.append(q.copy())
        pts.append(pts[-1]+u*R*.12-n*R*.05)
        tube(M,pts,[.014*R]*len(pts),WIN,1.0,4,cap0=False,cap1=False);M.blob(tuple(pts[-1]),.03*R,WIN,sub=1,noise=0)
    return M

def plain_rock(seed=4,R=1.0):
    M=Mesh(seed);Rock((0,0,0),R,seed).build(M);return M
