# Driftgate Beyond: the makers' R&D stations for the model pack (built 9 Nov 2026 from the approved preview of 6 Nov 2026,
# tools/previews/beyond_corp.py; no shields: the maker's security wing and the host power's garrison defend it).
# The station is assembled in the game from parts, so it can grow a lab per product line:
#   rds_<style>          the tower: the CEO's launch bay at its foot, the socket struts or clamps, the logo boards (blank: the
#                        game draws the maker's mark on them), two turret seats; style halcyon | varkesh | ostrova | free
#   rdl_<style>_g<2..5>  a lab at its grade, built in its socket's frame (+z outward, the socket at the origin, in lab units:
#                        the socket's scale takes it to tower units); Ostrova's lab brings its energy bridge back to the tower
#   rdp_<style>          what an empty socket shows (a lit pad; Ostrova a glowing node; Varkesh only under the lower spire)
# Each tower's pack entry carries its points (model space, packed like 'tp' and 'sub'): sub.cc the control centre, sub.bay the
# launch bay, sub.sock the four sockets, sub.lab each lab's centre (a sub-system), sub.logo the boards; tp the two turret seats;
# and, unpacked: sk [yaw, pitch, scale, pad] per socket (a lab's +z turned by pitch then yaw: yaw from +z toward +x), lg
# [yaw, pitch, size] per board (its face +z), rr the radius of the whole station with four labs, from the tower's centre.
import math,os,sys
import numpy as np
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'previews'))
import beyond_corp as BC
from beyond_hulls import Mesh,LIGHT,MID,DARK,ACC,GLASS,GLOW,WIN,plate,ring,box
from beyond_capitals import tube
from beyond_stations import put,outward,ry,drum
from beyond_faction_stations import lathe,band,node,bridge,talon,tri_spire,pincer_clamp,turned,zdir,UP_CLAW
PI=math.pi
STYLES={'halcyon':'halcyon','varkesh':'varkesh','ostrova':'ostrova','free':'freeport'}   # pack name -> the preview's style

def lit(M,windows,sz,seed=7,navs=True):
    # beyond_faction_stations.light_up with the window size given (so a lab built alone gets the same windows as on the
    # assembled station): lit windows on LIGHT and MID plating, navigation beacons at the outermost points
    T=np.array(M.T);V=T.reshape(-1,3);cen=(V.max(0)+V.min(0))/2
    g=np.random.default_rng(seed);cand=[];area=[]
    for t,(role,sh) in zip(T,M.R):
        if role not in (LIGHT,MID):continue
        a=np.linalg.norm(np.cross(t[1]-t[0],t[2]-t[0]))/2
        if a>(sz*4)**2:cand.append(t);area.append(a)
    if cand and windows:
        area=np.array(area);pick=g.choice(len(cand),size=windows,p=area/area.sum())
        for k in pick:
            t=cand[k];r1,r2=g.random(),g.random()
            if r1+r2>1:r1,r2=1-r1,1-r2
            p=t[0]+(t[1]-t[0])*r1+(t[2]-t[0])*r2;n=np.cross(t[1]-t[0],t[2]-t[0]);n/=np.linalg.norm(n)
            if n@(p-cen)<0:n=-n
            u=np.cross([0,1.,0],n)
            if np.linalg.norm(u)<.3:u=t[1]-t[0]
            u/=np.linalg.norm(u);v=np.cross(n,u);q=p+n*sz*.08;w=sz*(1.8 if g.random()<.35 else 1.0)
            A,B,C,D=q+u*w+v*sz*.5,q-u*w+v*sz*.5,q-u*w-v*sz*.5,q+u*w-v*sz*.5;role=GLOW if g.random()<.25 else WIN
            M.tri(A,B,C,role,1.0,ref=q-n);M.tri(A,C,D,role,1.0,ref=q-n)
    if navs:
        out=[]
        for d in [(1,0,0),(-1,0,0),(0,0,1),(0,0,-1),(0,1,0),(0,-1,0),(1,0,1),(-1,0,1),(1,0,-1),(-1,0,-1)]:
            d=np.array(d,float);d/=np.linalg.norm(d);p=V[np.argmax((V-cen)@d)]+d*sz
            if any(np.linalg.norm(p-q)<sz*10 for q in out):continue
            out.append(p);M.blob(tuple(p),sz*1.3,GLOW,sub=1,noise=0)
    return M
_SZ={}
def win_size(style):
    # the window size the approved preview gives the station with four labs (light_up: .0065 of its diagonal)
    if style not in _SZ:
        M=BC.corp_station(STYLES[style],(5,5,5,5));V=np.array(M.T).reshape(-1,3);_SZ[style]=float(np.linalg.norm(V.max(0)-V.min(0))*.0065)
    return _SZ[style]
def yaw_pitch(R):
    # R takes local +z to d: yaw from +z toward +x, then pitch up; checked against the full rotation (roll stays zero)
    d=R[:,2];pitch=math.asin(max(-1,min(1,d[1])))
    yaw=math.atan2(d[0],d[2]) if abs(d[1])<.999 else math.atan2(-R[2,0],R[0,0])   # straight up or down: the yaw that carries local +x where R does
    cy,sy,cp,sp=math.cos(yaw),math.sin(yaw),math.cos(pitch),math.sin(pitch)
    Ry=np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]]);Rp=np.array([[1,0,0],[0,cp,sp],[0,-sp,cp]]);Q=Ry@Rp
    assert np.allclose(Q@[0,0,1],R@[0,0,1],atol=1e-6) and np.allclose(Q@[1,0,0],R@[1,0,0],atol=1e-6),(R,Q)
    return yaw,pitch
def rot(yaw,pitch):
    cy,sy,cp,sp=math.cos(yaw),math.sin(yaw),math.cos(pitch),math.sin(pitch)
    return np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]])@np.array([[1,0,0],[0,cp,sp],[0,-sp,cp]])
def to_local(M,p,R,s):
    # a mesh built in the tower's frame, taken into a socket's frame (the inverse of put(M,B,p,R,s))
    N=Mesh();N.T=[((np.array(t)-p)@R)/s for t in M.T];N.R=list(M.R);return N

def board_blank(M,c,a,size):
    # beyond_corp.logo_board without the emblem: the dark board and its accent rim (the game draws the maker's mark on it)
    B=Mesh();h=size/2
    plate(B,[(-h,-h,0),(h,-h,0),(h,h,0),(-h,h,0)],.03,DARK,.75)
    for p,q in (((-h,-h),(h,-h)),((h,-h),(h,h)),((h,h),(-h,h)),((-h,h),(-h,-h))):tube(B,[(p[0],p[1],.02),(q[0],q[1],.02)],[.016,.016],ACC,1.0,4,cap0=False,cap1=False)
    put(M,B,c,outward(a))

# ------------------------------------------------------------------ the model check's fixes (9 Nov 2026)
# Parts the preview left hanging in space, held on now: rings round a mast get three spokes, the bay's guide lights a rail
# each, the test cell a back plate with its rails run on to the target ring, the freeport lab's radiators a root, Halcyon's
# crown mast reaches its pod, Halcyon's logo boards a strut each to the spire, the test piece a mount. Ostrova's pieces float by design.
def spokes(M,c,R,n=3,r=.012,off=PI/6):
    c=np.array(c,float)
    for k in range(n):a=off+k*2*PI/n;tube(M,[c,c+[math.cos(a)*R,0,math.sin(a)*R]],[r,r],DARK,.9,4)
def bay_rails(B,c,w,h):
    # under each row of the bay's guide lights (beyond_corp.ceo_bay), a dark rail from the hull out past the last light
    for sx in (-1,1):x=c[0]+sx*w*.45;y=c[1]-h/2-.01;tube(B,[(x,y,c[2]-.2),(x,y,c[2]+.47)],[.014,.014],DARK,.9,4)
def lab_fixes(B,s,grade):
    if grade>=3 and s!='ostrova':
        box(B,(0,-.15,1.30),(.36,.36,.03),DARK)
        tube(B,[(0,-.15,1.3),(0,-.15,1.42)],[.016,.012],DARK,.9,5)   # the test piece's mount
        for sx in (-1,1):
            for sy in (-1,1):tube(B,[(sx*.16,-.15+sy*.16,1.6),(sx*.16,-.15+sy*.16,1.69)],[.018,.018],DARK,.9,4)
    if grade>=4 and s=='freeport':
        for sx in (-1,1):tube(B,[(sx*.24,0,.45),(sx*.4,0,.45)],[.045,.045],DARK,.9,6)
    if grade>=5 and s!='ostrova':
        top=.42 if s!='varkesh' else .36
        if s=='halcyon':tube(B,[(0,.18,.45),(0,top,.45)],[.06,.05],LIGHT,.95,6)
        spokes(B,(0,top+.3,.45),.17,3,.01)

# ------------------------------------------------------------------ sockets: where each lab sits
def sockets(style):
    s=STYLES[style];out=[]
    if s=='varkesh':
        for k in range(3):
            a=BC.v_face(k);u=np.array([math.cos(a),0,math.sin(a)]);base=u*(BC.VR*.5*.62)+[0,.55,0]
            out.append(dict(p=base+u*1.3,R=outward(a),s=1.25,pad=0))
        out.append(dict(p=np.array([0,-BC.VH+.15,0]),R=zdir((0,-1,0)),s=1.2,pad=1))
    else:
        for a in BC.SOCK:out.append(dict(p=np.array([math.cos(a),0,math.sin(a)])*BC.R_SOCK,R=outward(a),s=1.35,pad=1))
    return out
def lab_local(style,grade):
    # the lab as the preview builds it, in its socket's frame
    s=STYLES[style];B=Mesh();BC.lab_pod(B,s)
    if grade>=3:BC.lab_gantry(B,s)
    if grade>=4:BC.lab_radiators(B,s)
    if grade>=5:BC.lab_crown(B,s)
    lab_fixes(B,s,grade)
    if s=='ostrova':
        # the energy bridge back to the tower (the preview draws it with the socket when a lab is in it)
        S=sockets(style)[0];c=S['p']/BC.R_SOCK;Wm=Mesh();bridge(Wm,c*.7,c*(BC.R_SOCK-.05),.03);L=to_local(Wm,S['p'],S['R'],S['s'])
        B.T+=L.T;B.R+=L.R
    return B
def lab_model(style,grade):
    S=sockets(style)[0];B=lab_local(style,grade);return lit(B,6+3*grade,win_size(style)/S['s'],seed=11+grade,navs=False)
def pad_model(style):
    # an empty socket, in the frame of the socket it marks (with that socket's scale)
    s=STYLES[style];SK=sockets(style);Wm=Mesh()
    if s=='varkesh':S=SK[3];node(Wm,(0,-BC.VH-.08,0),.09,GLOW)
    elif s=='ostrova':S=SK[0];c=S['p']/BC.R_SOCK;node(Wm,c*1.0,.05,GLOW)
    else:
        S=SK[0];c=S['p']/BC.R_SOCK;p1=c*(BC.R_SOCK-.02);B=Mesh()
        plate(B,[(math.cos(t)*.22,0,math.sin(t)*.22) for t in np.linspace(0,2*PI,6,endpoint=False)],.04,DARK,.9);ring(B,(0,.03,0),.17,.018,ACC,seg=18,sides=4,axis='y')
        put(Wm,B,p1+[0,-.02,0])
    return to_local(Wm,S['p'],S['R'],S['s'])

# ------------------------------------------------------------------ towers
def ray(M,o,d):
    # the nearest hit of a ray on the hull plating (light, mid and dark faces: not rings, glass or lights): the point and the
    # face normal turned toward the ray's start
    T=np.array([t for t,r in zip(M.T,M.R) if r[0] in (LIGHT,MID,DARK)],float);o=np.array(o,float);d=np.array(d,float);d/=np.linalg.norm(d)
    e1=T[:,1]-T[:,0];e2=T[:,2]-T[:,0];p=np.cross(d,e2);det=(e1*p).sum(1);ok=np.abs(det)>1e-12;inv=np.where(ok,1/np.where(ok,det,1),0)
    s=o-T[:,0];u=(s*p).sum(1)*inv;q=np.cross(s,e1);v=(q*d).sum(1)*inv;t=(e2*q).sum(1)*inv
    hit=ok&(u>=0)&(v>=0)&(u+v<=1)&(t>1e-6);t=np.where(hit,t,np.inf);k=int(np.argmin(t));assert np.isfinite(t[k]),('no hit',o,d)
    n=np.cross(e1[k],e2[k]);n/=np.linalg.norm(n)
    if n@d>0:n=-n
    return o+d*t[k],n
def seat(M,o,d):
    # a turret seat where the ray meets the hull: a short dark drum on the surface with an accent ring; returns the turret point
    p,n=ray(M,o,d);top=p+n*.07
    drum(M,p-n*.02,top,.12,DARK,10);B=Mesh();ring(B,(0,0,0),.1,.016,ACC,seg=16,sides=4,axis='y')
    from beyond_stations import frame_y
    put(M,B,top,frame_y(n));return top
# the two turret seats per style, each a ray (start, direction) onto the tower; kept clear of the launch bay (+z, low), the
# sockets (the four diagonals) and the logo boards: one covering above, one below
TURRET_RAYS={
 'halcyon':[((.52,2.5,0),(0,-1,0)),((-.52,-2.5,0),(0,1,0))],                      # on the lens disc: top at +x, underside at -x
 'varkesh':None,                                                                    # set below: on the spires' clear faces
 'ostrova':[((-1.6,1.12,-1.6),(1,0,1)),((0,-3,0),(0,1,0))],                         # the third segment, back left between boards; the lowest segment's tip
 'free':[((0,.18,-2),(0,0,1)),((0,-3,0),(0,1,0))]}                                 # the drum's back between the struts, its base
def _vk(k,y):a=BC.v_face(k);u=np.array([math.cos(a),0,math.sin(a)]);return (tuple(u*2+[0,y,0]),tuple(-u))
TURRET_RAYS['varkesh']=[_vk(1,1.02),_vk(2,-1.02)]                                  # upper spire on face 1, lower spire on face 2
def varkesh_tower(M):
    # beyond_corp.varkesh_rd without its labs: two triangular spires on an armoured waist, three talons up and three down,
    # the pincer clamps on the upper faces (the labs' sockets), the CEO's bay in the first waist face, blank boards below
    VH,VR=BC.VH,BC.VR
    tri_spire(M,0,VH,VR,1);tri_spire(M,0,VH,VR,-1)
    lathe(M,[(-.12,VR*1.02),(-.05,VR*1.08),(.05,VR*1.08),(.12,VR*1.02)],3,(MID,1.0),(LIGHT,1.0),(LIGHT,1.4),off=PI/2,caps=False)
    band(M,0,VR*1.09,3,.05,ACC,PI/2);band(M,.75,VR*.58,3,.04,WIN,PI/2)
    C=[(r*.31,y*.31) for r,y in UP_CLAW];CD=[(r*.31*.8,-y*.31*1.05) for r,y in UP_CLAW]
    for k in range(3):a=PI/2+k*2*PI/3;talon(M,a,C,.28,.1);talon(M,a,CD,.26,.1)
    tube(M,[(0,VH-.1,0),(0,VH+.55,0)],[.05,.02],LIGHT,.9,5);node(M,(0,VH+.6,0),.08,GLOW);ring(M,(0,VH+.3,0),.16,.03,ACC,seg=12,sides=4,axis='y');spokes(M,(0,VH+.3,0),.16,3,.014)
    a0=BC.v_face(0);u0=np.array([math.cos(a0),0,math.sin(a0)]);turned(M,lambda B:(BC.ceo_bay(B,(0,0,0),.5,.22,.25),bay_rails(B,(0,0,0),.5,.22)),u0*(VR*.5+.08),a0)
    boards=[]
    for k in range(3):
        a=BC.v_face(k);u=np.array([math.cos(a),0,math.sin(a)]);base=u*(VR*.5*.62)+[0,.55,0]
        turned(M,lambda B:pincer_clamp(B,.95,.42),base,a)
        c=u*(VR*.5*.62+.05)+[0,-.62,0];board_blank(M,c,a,.5);boards.append((c,a,.5))
    return dict(bay=u0*(VR*.5+.08),bay_d=u0,cc=np.array([0,.75,0.]),boards=boards)
BAY={'halcyon':((0,-.26,.62),.5,.24,.25),'ostrova':((0,-.65,.38),.42,.22,.22),'free':((0,-.5,.52),.5,.3,.26)}
CC={'halcyon':(0,.36,0),'ostrova':(0,.18,0),'free':(0,1.5,0)}   # the glass dome; the great middle segment; the drum's crown
def tower_model(style):
    s=STYLES[style];M=Mesh()
    if s=='varkesh':info=varkesh_tower(M)
    else:
        # beyond_corp.tower (bay and the company band included), the socket struts (always there), blank boards
        BC.tower(M,s);boards=[]
        if s!='ostrova':c,w,h,_=BAY[style];bay_rails(M,c,w,h)
        if s=='halcyon':
            for y in (1.45,1.55):spokes(M,(0,y,0),.2,3,.014)
            for a in (PI/2,0,-PI/2,PI):tube(M,[(0,BC.BOARD[s][0],0),(math.cos(a)*.39,BC.BOARD[s][0],math.sin(a)*.39)],[.025,.025],DARK,.9,6)
        if s=='freeport':spokes(M,(0,2.1+.28,0),.09,3,.008)
        y,r,sz=BC.BOARD[s]
        for a in (PI/2,0,-PI/2,PI):c=np.array([math.cos(a)*r,y,math.sin(a)*r]);board_blank(M,c,a,sz);boards.append((c,a,sz))
        if s!='ostrova':
            for a in BC.SOCK:
                c=np.array([math.cos(a),0,math.sin(a)]);p0=c*(.62 if s=='halcyon' else .44);p1=c*(BC.R_SOCK-.02)
                if s=='halcyon':tube(M,[p0,(p0+p1)/2+[0,.08,0],p1],[.07,.06,.05],LIGHT,.92,8)
                else:BC.truss(M,p0,p1,.14,.018)
        info=dict(bay=np.array(BAY[style][0],float),bay_d=np.array([0,0,1.]),cc=np.array(CC[style],float),boards=boards)
    tp=[seat(M,o,d) for o,d in TURRET_RAYS[style]]
    lit(M,40,win_size(style),seed=7)
    SK=sockets(style)
    # the radius of the whole station with a grade-5 lab in every socket, from the tower's centre
    V=np.array(M.T).reshape(-1,3);c0=(V.max(0)+V.min(0))/2;rr=float(np.linalg.norm(V-c0,axis=1).max())
    for S in SK:
        L=np.array(lab_local(style,5).T).reshape(-1,3)@S['R'].T*S['s']+S['p'];rr=max(rr,float(np.linalg.norm(L-c0,axis=1).max()))
    lab_c=[S['p']+S['R']@np.array([0,0,.45])*S['s'] for S in SK]
    sub={'cc':[info['cc']],'bay':[info['bay']],'sock':[S['p'] for S in SK],'lab':lab_c,'logo':[b[0] for b in info['boards']]}
    sk=[];lg=[]
    for S in SK:yw,pt=yaw_pitch(S['R']);sk.append([round(yw,4),round(pt,4),S['s'],S['pad']])
    for c,a,sz in info['boards']:yw,pt=yaw_pitch(outward(a));lg.append([round(yw,4),round(pt,4),sz])
    return M,dict(tp=tp,sub=sub,extra={'sk':sk,'lg':lg,'rr':round(rr,3),'bd':[round(float(v),4) for v in info['bay_d']]})
# what build_models.py packs: name -> builder returning (Mesh, info or None)
def models():
    out={}
    for st in STYLES:
        out['rds_'+st]=(lambda st:lambda:tower_model(st))(st)
        for g in (2,3,4,5):out['rdl_%s_g%d'%(st,g)]=(lambda st,g:lambda:(lab_model(st,g),None))(st,g)
        out['rdp_'+st]=(lambda st:lambda:(pad_model(st),None))(st)
    return out
