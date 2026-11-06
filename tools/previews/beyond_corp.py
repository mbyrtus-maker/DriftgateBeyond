# Driftgate Beyond: a maker's R&D station (preview, not in the model pack yet; proposal 6 Nov 2026).
# Each maker keeps a small station of its own in its home system, not dockable: a tower with the CEO's launch bay at its
# foot (the CEO flies out from here when summoned) and the company's band at its crown, and four sockets round it. Each
# product line the maker takes through R&D adds a lab in a socket, and the lab grows with the grade:
#   G2 a lab pod with a lit window band        G3 + a test gantry with a test cell and target ring out beyond it
#   G4 + heat radiators on the pod             G5 + a sensor crown with a glowing core
# Styled by the maker's home: Halcyon lens and glass, Varkesh hex slabs, Ostrova floating crystal held in halos and joined by
# energy bridges, the freeports' company style (drums, trusses, containers, tanks). Up is +y.
import math,sys,os
import numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from beyond_hulls import Mesh,LIGHT,MID,DARK,ACC,GLASS,GLOW,WIN,box,plate,ring
from beyond_capitals import tube
from beyond_stations import ry,frame_y,put,outward,drum,truss,tank,radiator,floods,mast,container
from beyond_faction_stations import lathe,band,node,bridge,crystal_at,tilted_ring,float_seg,light_up,talon,tri_spire,pincer_clamp,turned,zdir,UP_CLAW
from beyond_work import abox
PI=math.pi
SOCK=[PI/4,3*PI/4,5*PI/4,7*PI/4]
R_SOCK=1.6

def ceo_bay(M,c,w=.62,h=.34,d=.3):
    # the CEO's launch bay: a dark recess facing +z with a lit lip and two guide lights out in front
    abox(M,(c[0],c[1],c[2]-d/2),(w,h,d),DARK,(1,1),.6)
    for a,b in (((-w/2,-h/2),(w/2,-h/2)),((w/2,-h/2),(w/2,h/2)),((w/2,h/2),(-w/2,h/2)),((-w/2,h/2),(-w/2,-h/2))):
        tube(M,[(c[0]+a[0],c[1]+a[1],c[2]+.01),(c[0]+b[0],c[1]+b[1],c[2]+.01)],[.014,.014],WIN,1.0,4,cap0=False,cap1=False)
    for sx in (-1,1):
        for k in range(3):M.blob((c[0]+sx*w*.45,c[1]-h/2-.02,c[2]+.12+k*.16),.028,GLOW,sub=1,noise=0)

# ------------------------------------------------------------------ labs: built facing +z (outward), centred on the socket
def lab_pod(M,style):
    if style=='halcyon':
        M.blob((0,0,.45),.42,LIGHT,sub=2,squash=(1,.62,1.25),noise=0);band(M,0,.4,20,.05,WIN,c=(0,0,.45))
        M.blob((0,.2,.42),.2,GLASS,sub=2,squash=(1,.6,1.2),noise=0)
    elif style=='varkesh':
        box(M,(0,0,.45),(.7,.48,.82),MID,(.82,.9));box(M,(0,.27,.45),(.56,.08,.66),DARK)
        for z in (.16,.45,.74):box(M,(0,0,z),(.74,.5,.04),DARK)
        box(M,(0,.05,.87),(.42,.07,.02),WIN)
    elif style=='ostrova':
        crystal_at(M,(0,0,.05),(0,0,1),.85,.32);ring(M,(0,0,.45),.46,.035,ACC,seg=32,sides=6,axis='z');node(M,(0,0,.45),.09,GLOW)
    else:
        drum(M,(0,0,.08),(0,0,.82),.3,MID,14,bands=(.2,.8));container(M,(0,.38,.45),(.34,.24,.62),LIGHT)
        floods(M,[(.31,0,.45),(-.31,0,.45)],.035)
def lab_gantry(M,style):
    # the test range: a gantry out past the pod, a test cell and a target ring at its end
    if style=='ostrova':
        bridge(M,(0,0,.9),(0,0,1.35),.03);tilted_ring(M,(0,0,1.48),.28,.03,PI/2,0,ACC,40);node(M,(0,0,1.48),.07,GLOW)
        crystal_at(M,(0,.25,1.2),(0,1,0),.3,.1)
    else:
        if style=='varkesh':box(M,(0,-.15,1.08),(.18,.14,.46),DARK)
        else:truss(M,(0,-.15,.85),(0,-.15,1.3),.16,.02,bays=3)
        cell=(0,-.15,1.46)
        for sx in (-1,1):
            for sy in (-1,1):tube(M,[(cell[0]+sx*.16,cell[1]+sy*.16,cell[2]-.16),(cell[0]+sx*.16,cell[1]+sy*.16,cell[2]+.16)],[.018,.018],DARK,.9,4)
        ring(M,(0,-.15,1.68),.22,.022,WIN,seg=24,sides=4,axis='z');node(M,cell,.06,GLOW)
def lab_radiators(M,style):
    if style=='ostrova':
        for sx in (-1,1):crystal_at(M,(sx*.3,0,.45),(sx,.35,0),.45,.09)
    else:
        for sx in (-1,1):radiator(M,(sx*.36,0,.45),(sx*1.05,.1,.45),.34,3)
def lab_crown(M,style):
    top=.42 if style!='varkesh' else .36
    if style=='ostrova':
        tilted_ring(M,(0,.62,.45),.24,.025,0,0,GLOW,32);node(M,(0,.62,.45),.11,GLOW);crystal_at(M,(0,.3,.45),(0,1,0),.25,.08)
    else:
        tube(M,[(0,top-.05,.45),(0,top+.4,.45)],[.05,.025],LIGHT,.95,6);M.blob((0,top+.48,.45),.1,GLOW,sub=1,noise=0)
        ring(M,(0,top+.3,.45),.17,.018,ACC,seg=20,sides=4,axis='y')
def lab(M,style,grade,a):
    B=Mesh();lab_pod(B,style)
    if grade>=3:lab_gantry(B,style)
    if grade>=4:lab_radiators(B,style)
    if grade>=5:lab_crown(B,style)
    pos=(math.cos(a)*R_SOCK,0,math.sin(a)*R_SOCK);put(M,B,pos,outward(a),1.35)

# ------------------------------------------------------------------ towers and sockets
def socket(M,style,a,used):
    # what joins a socket to the tower: struts (Halcyon), pylons (Varkesh), a bridge (Ostrova), a truss (freeports);
    # an empty socket shows a small lit pad where a lab will go
    c=np.array([math.cos(a),0,math.sin(a)]);p0=c*.62;p1=c*(R_SOCK-.02)
    if style=='halcyon':tube(M,[p0,(p0+p1)/2+[0,.08,0],p1],[.07,.06,.05],LIGHT,.92,8)
    elif style=='varkesh':B=Mesh();box(B,(0,0,(R_SOCK-.62)/2),(.26,.2,R_SOCK-.62),DARK);put(M,B,p0,outward(a))
    elif style=='ostrova':bridge(M,c*.7,c*(R_SOCK-.05),.03) if used else node(M,c*1.0,.05,GLOW)
    else:truss(M,p0,p1,.14,.018)
    if not used and style!='ostrova':
        B=Mesh();plate(B,[(math.cos(t)*.22,0,math.sin(t)*.22) for t in np.linspace(0,2*PI,6,endpoint=False)],.04,DARK,.9);ring(B,(0,.03,0),.17,.018,ACC,seg=18,sides=4,axis='y')
        put(M,B,p1+[0,-.02,0])
def tower(M,style):
    if style=='halcyon':
        lathe(M,[(-.5,.05),(-.32,.62),(-.06,.82),(.12,.72),(.3,.3),(.42,.05)],28,c=(0,0,0))
        band(M,-.06,.83,28,.05,WIN);M.blob((0,.36,0),.34,GLASS,sub=2,squash=(1,.7,1),noise=0)
        tube(M,[(0,.55,0),(0,2.0,0)],[.07,.025],LIGHT,.95,8);node(M,(0,2.05,0),.07,GLOW)
        ring(M,(0,1.45,0),.2,.03,ACC,seg=24,sides=4,axis='y');ring(M,(0,1.55,0),.2,.03,ACC,seg=24,sides=4,axis='y')
        lathe(M,[(-.5,.05),(-.9,.22),(-1.25,.03)],14,c=(0,0,0))
        ceo_bay(M,(0,-.26,.62),.5,.24,.25)
    elif style=='varkesh':
        for y0,y1,w in ((-.85,-.15,1.15),(-.15,.75,.95),(.75,1.45,.7)):
            box(M,(0,(y0+y1)/2,0),(w,y1-y0,w*.86),MID if y0<0 else LIGHT,(.88,.88))
            box(M,(0,y1-.03,0),(w*.92,.06,w*.8),DARK)
        box(M,(0,1.62,0),(.5,.34,.4),ACC,(.8,.8));box(M,(0,1.9,0),(.12,.3,.12),DARK);node(M,(0,2.08,0),.06,GLOW)
        for sx in (-1,1):box(M,(sx*.62,.3,0),(.12,1.0,.6),DARK)
        ceo_bay(M,(0,-.55,.5),.62,.3,.3)
    elif style=='ostrova':
        for y0,y1,r in ((-.95,-.35,.38),(-.2,.55,.48),(.7,1.35,.36),(1.5,1.95,.22)):float_seg(M,(0,0,0),y0,y1,r)
        tilted_ring(M,(0,.18,0),.9,.04,.25,0,ACC);tilted_ring(M,(0,1.05,0),.62,.035,-.3,1.2,ACC)
        crystal_at(M,(0,1.95,0),(0,1,0),.4,.12)
        ceo_bay(M,(0,-.65,.38),.42,.22,.22)
    else:
        drum(M,(0,-.9,0),(0,1.4,0),.5,MID,16,bands=(.18,.5,.82));drum(M,(0,1.4,0),(0,1.62,0),.36,LIGHT,16)
        tank(M,(.0,1.86,0),.26);mast(M,(0,2.1,0),.4)
        for a in (0,PI):radiator(M,(math.cos(a)*.5,.9,math.sin(a)*.5),(math.cos(a)*1.05,1.2,math.sin(a)*1.05),.3,2)
        for a in (PI/2,3*PI/2):tank(M,(math.cos(a)*.62,1.15,math.sin(a)*.62),.18)
        ceo_bay(M,(0,-.5,.52),.5,.3,.26)
    # the company's band near the crown
    y={'halcyon':1.2,'varkesh':1.62,'ostrova':1.4,'freeport':1.3}[style];r={'halcyon':.1,'varkesh':.36,'ostrova':.3,'freeport':.52}[style]
    ring(M,(0,y,0),r,.05,ACC,seg=28,sides=6,axis='y')

# ------------------------------------------------------------------ the makers: home style, accent colour, logo
# Each maker's accent is a shade of its home power's colour (the Compact's gold at the freeports), so a company reads as
# belonging to its power and still stands apart from its neighbour. Logos are flat emblems of convex pieces in [-1,1]^2,
# lit in the accent on a dark board with an accent rim, four boards round the tower's crown so one always faces you.
def _circ(cx,cy,r,n=14):return [(cx+math.cos(a)*r,cy+math.sin(a)*r) for a in np.linspace(0,2*PI,n,endpoint=False)]
def _bar(x0,y0,x1,y1,w):
    d=np.array([x1-x0,y1-y0],float);d/=np.linalg.norm(d);n=np.array([-d[1],d[0]])*w/2
    return [(x0+n[0],y0+n[1]),(x1+n[0],y1+n[1]),(x1-n[0],y1-n[1]),(x0-n[0],y0-n[1])]
def _chev(y,w=.7,h=.38,t=.2):return [_bar(-w,y-h,0,y,t*1.1),_bar(0,y,w,y-h,t*1.1)]
def _hexring(r,t,skip=()):
    P=[(math.cos(a)*r,math.sin(a)*r) for a in np.linspace(PI/6,2*PI+PI/6,6,endpoint=False)];out=[]
    for i in range(6):
        if i in skip:continue
        a,b=np.array(P[i]),np.array(P[(i+1)%6]);ia,ib=a*(r-t)/r,b*(r-t)/r;out.append([tuple(a),tuple(b),tuple(ib),tuple(ia)])
    return out
LOGOS={
 'tcy':_chev(.55,.85,.55,.22)+[_bar(-.55,-.55,.55,-.55,.16),[(0,.05),(.18,-.2),(0,-.38),(-.18,-.2)]],     # Teal & Corvane: a corvid's wings over a slipway
 'bl':[_bar(-1,0,1,0,.1),[(0,.7),(.28,0),(0,-.7),(-.28,0)]]+[_bar(math.cos(a)*.42,math.sin(a)*.42,math.cos(a)*.62,math.sin(a)*.62,.07) for a in (PI/4,3*PI/4,5*PI/4,7*PI/4)],   # Brightline: a beam and a burst
 'hf':[[(-.75,.45),(.75,.45),(.42,-.35),(-.42,-.35)],_bar(-.62,-.6,.62,-.6,.18),[(0,1.0),(.2,.66),(0,.55),(-.2,.66)]],   # Hold Foundry: a crucible and a drop
 'mg':_chev(.75)+_chev(.2)+_chev(-.35),                                                                    # Marchgun: three chevrons on the march
 'sw':[[(0,1),(.2,0),(0,-1),(-.2,0)],_bar(-.6,.25,.6,.25,.12),_bar(-.38,-.25,.38,-.25,.1)],                 # Spirewright: a spire
 'ad':[_bar(-.8,-.8,.8,-.8,.12),_bar(.8,-.8,.8,.8,.12),_bar(.8,.8,-.8,.8,.12),_bar(-.8,.8,-.8,-.8,.12)]+[_bar(-.5,y,.5,y,.13) for y in (.38,0,-.38)],   # Archive: the stacks in their case
 'mwa':[[(-.85,.08),(.85,.08),(0,.85)],[(-.85,-.08),(0,-.85),(.85,-.08)],_bar(-1,0,1,0,.05)],               # Mirrorwater: a peak and its reflection
 'qs':[_circ(0,-.28,.52,16),[(0,.95),(.4,-.1),(-.4,-.1)]],                                                  # Quicksilver: a drop
 'cr':_hexring(.85,.2,skip=(1,))+[_bar(-.4,0,.4,0,.16)],                                                    # Coldwater Refit: a broken hex, a bar to mend it
 'cp':[[(0,.95),(.5,.4),(.5,-.15),(0,-.6),(-.5,-.15),(-.5,.4)],_bar(-.65,-.82,.65,-.82,.12)],               # Coldwater Prospecting: a cut gem on a seam
 'ewd':[[(-.5,-.55),(-.2,-.55),(-.36,.4)],[(-.16,-.55),(.16,-.55),(0,.95)],[(.2,-.55),(.5,-.55),(.36,.4)],_bar(-.7,-.72,.7,-.72,.14)],   # Ember Wake: three flames
 'wf':[[(0,1),(.28,.55),(-.28,.55)],_bar(0,.55,0,-.45,.24),_bar(-.2,-.5,-.55,-.95,.1),_bar(.2,-.5,.55,-.95,.1),_bar(0,-.55,0,-.98,.1)]}   # Wakefire: a missile and its wake
MAKERS=[('tcy','Teal & Corvane Yards','halcyon','#3fb8e6'),('bl','Brightline Emitters','halcyon','#72efbe'),
        ('hf','Hold Foundry','varkesh','#e8583a'),('mg','Marchgun Ordnance','varkesh','#ffa040'),
        ('sw','Spirewright','ostrova','#9b7bff'),('ad','Archive Dynamics','ostrova','#d6a4ff'),
        ('mwa','Mirrorwater Arms','freeport','#e9dc9a'),('qs','Quicksilver Hullworks','freeport','#d2d4c6'),
        ('cr','Coldwater Refit','freeport','#c6d28e'),('cp','Coldwater Prospecting','freeport','#e0b552'),
        ('ewd','Ember Wake Drives','freeport','#f2a24e'),('wf','Wakefire Munitions','freeport','#e8803c')]
def logo_board(M,logo,c,a,size):
    # a board facing outward along angle a, centred at c: dark plate, accent rim, the emblem lit in front
    B=Mesh();h=size/2
    plate(B,[(-h,-h,0),(h,-h,0),(h,h,0),(-h,h,0)],.03,DARK,.75)
    for p,q in (((-h,-h),(h,-h)),((h,-h),(h,h)),((h,h),(-h,h)),((-h,h),(-h,-h))):tube(B,[(p[0],p[1],.02),(q[0],q[1],.02)],[.016,.016],ACC,1.0,4,cap0=False,cap1=False)
    k=h*.78
    for poly in LOGOS[logo]:plate(B,[(x*k,y*k,.03) for x,y in poly],.012,GLOW,1.0)
    put(M,B,c,outward(a))
BOARD={'halcyon':(.95,.4,.6),'varkesh':(1.12,.42,.62),'ostrova':(1.0,.56,.56),'freeport':(.62,.54,.62)}   # (height, radius, size)
# Varkesh: the Talon Citadel in small, as the depot: two triangular spires on an armoured waist, three talons curling up and
# three down. Three labs are held out from the upper faces in pincer clamps; the fourth hangs under the lower spire, clutched by
# the three lower talons. The CEO's bay is a hangar slot in one waist face; the logo boards sit on the lower faces.
VH,VR=1.6,.95
def v_face(k):return PI/2+PI/3+k*2*PI/3
def varkesh_rd(grades,logo):
    M=Mesh();tri_spire(M,0,VH,VR,1);tri_spire(M,0,VH,VR,-1)
    lathe(M,[(-.12,VR*1.02),(-.05,VR*1.08),(.05,VR*1.08),(.12,VR*1.02)],3,(MID,1.0),(LIGHT,1.0),(LIGHT,1.4),off=PI/2,caps=False)
    band(M,0,VR*1.09,3,.05,ACC,PI/2);band(M,.75,VR*.58,3,.04,WIN,PI/2)
    C=[(r*.31,y*.31) for r,y in UP_CLAW];CD=[(r*.31*.8,-y*.31*1.05) for r,y in UP_CLAW]
    for k in range(3):a=PI/2+k*2*PI/3;talon(M,a,C,.28,.1);talon(M,a,CD,.26,.1)
    tube(M,[(0,VH-.1,0),(0,VH+.55,0)],[.05,.02],LIGHT,.9,5);node(M,(0,VH+.6,0),.08,GLOW);ring(M,(0,VH+.3,0),.16,.03,ACC,seg=12,sides=4,axis='y')
    # the CEO's bay in the first waist face
    a0=v_face(0);u0=np.array([math.cos(a0),0,math.sin(a0)]);turned(M,lambda B:ceo_bay(B,(0,0,0),.5,.22,.25),u0*(VR*.5+.08),a0)
    for k in range(3):
        a=v_face(k);u=np.array([math.cos(a),0,math.sin(a)]);g=grades[k] if k<len(grades) else 0
        base=u*(VR*.5*.62)+[0,.55,0]
        turned(M,lambda B:pincer_clamp(B,.95,.42),base,a)
        if g:B=Mesh();lab_pod(B,'varkesh');(lab_gantry(B,'varkesh') if g>=3 else None);(lab_radiators(B,'varkesh') if g>=4 else None);(lab_crown(B,'varkesh') if g>=5 else None);put(M,B,base+u*1.3,outward(a),1.25)
        if logo:logo_board(M,logo,u*(VR*.5*.62+.05)+[0,-.62,0],a,.5)
    if len(grades)>3 and grades[3]:
        B=Mesh();lab_pod(B,'varkesh');g=grades[3]
        if g>=3:lab_gantry(B,'varkesh')
        if g>=4:lab_radiators(B,'varkesh')
        if g>=5:lab_crown(B,'varkesh')
        put(M,B,(0,-VH+.15,0),zdir((0,-1,0)),1.2)
    else:node(M,(0,-VH-.08,0),.09,GLOW)
    return M
def corp_station(style,grades=(),logo=None):
    # grades: the labs' grades, filling the sockets in order (up to four)
    if style=='varkesh':return light_up(varkesh_rd(grades,logo),40+15*len(grades))
    M=Mesh();tower(M,style)
    if logo:
        y,r,sz=BOARD[style]
        for a in (PI/2,0,-PI/2,PI):logo_board(M,logo,(math.cos(a)*r,y,math.sin(a)*r),a,sz)
    for i,a in enumerate(SOCK):
        g=grades[i] if i<len(grades) else 0;socket(M,style,a,g>0)
        if g:lab(M,style,g,a)
    return light_up(M,40+15*len(grades))
STYLES=[('halcyon','Halcyon home','Teal & Corvane Yards · Brightline Emitters'),('varkesh','Varkesh home','Hold Foundry · Marchgun Ordnance'),
        ('ostrova','Ostrova home','Spirewright · Archive Dynamics'),('freeport','Freeports','Mirrorwater, Quicksilver · the Coldwaters · Ember Wake, Wakefire')]
