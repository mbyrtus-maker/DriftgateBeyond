# Driftgate Beyond: scouts and bombers (preview, not in the model pack yet). Combat and recon craft, so they keep close to the
# approved fighters' proportions and shape language, with a signature per class:
#   Scout / Advanced Scout: slim hulls, sensor masts, dishes and radomes, limpet racks and a beacon device (Advanced)
#   Bomber: heavier hulls with visible torpedoes (the siege weapon)
#   Heavy Bomber: two seats in tandem and a rear turret, torpedoes
import math
import numpy as np
from beyond_hulls import Mesh,LIGHT,MID,DARK,ACC,GLASS,GLOW,WIN,loft,box,plate,barrel,ring,LENS,HEX,DIA,lens_role,hex_role
from beyond_work import finish,tube,abox,crystal,lights,sqdrive,SP,STAR
PI=math.pi

def torpedo(M,base,length=.6,r=.05,role=MID):
    # a torpedo slung along +z: body, an accent warhead and small tail fins
    b=np.array(base,float)
    tube(M,[b,b+[0,0,length*.8]],[r*.85,r],role,.95,8,cap0=True,cap1=False)
    tube(M,[b+[0,0,length*.8],b+[0,0,length]],[r,r*.1],ACC,1.0,8,cap0=False,cap1=False)
    for a in (0,PI/2):plate(M,[b+[0,0,.02],b+[math.cos(a)*r*2.2,math.sin(a)*r*2.2,-.02],b+[math.cos(a)*r*2.2,math.sin(a)*r*2.2,.06],b+[0,0,.12]],.006,DARK)
def turret(M,c,r=.1,role=MID,back=True):
    # a turret dome with twin barrels (pointing aft for a rear gunner)
    c=np.array(c,float);M.blob(tuple(c),r,GLASS,sub=2,squash=(1,.7,1),noise=0);ring(M,tuple(c-[0,r*.25,0]),r*1.05,r*.15,role,seg=14,sides=4,axis='y')
    d=-1 if back else 1
    for sx in (1,-1):tube(M,[c+[sx*r*.35,0,d*r*.6],c+[sx*r*.35,0,d*(r*.6+.32)]],[.018,.016],DARK,1.0,6)
def mast(M,base,h,r=.012,role=LIGHT,rings=2):
    b=np.array(base,float);tube(M,[b,b+[0,h,0]],[r,r*.6],role,.9,5)
    for k in range(rings):ring(M,tuple(b+[0,h*(.55+.25*k),0]),.05-.012*k,.008,ACC,seg=10,sides=4,axis='y')
def dish(M,c,r,role=MID,axis='y'):
    M.blob(tuple(c),r,role,sub=2,squash=(1,.28,1) if axis=='y' else (1,1,.28),noise=0);ring(M,tuple(c),r,.014,ACC,seg=20,sides=4,axis=axis)
def limpets(M,c,n=3):
    for k in range(n):M.blob((c[0],c[1],c[2]-k*.07),.03,ACC,sub=1,noise=0)

# ============================================================== HALCYON
def lark():      # scout: a slim needle with a long sensor boom forward, a small dorsal dish, swept wings with emitter nodes
    M=Mesh(81)
    loft(M,[(-.8,LENS(.08,.07)),(-.4,LENS(.13,.11)),(.2,LENS(.12,.11)),(.6,LENS(.05,.05,-.01))],lens_role)
    M.blob((0,.1,.15),.07,GLASS,sub=2,squash=(.9,.75,2.2),noise=0)
    tube(M,[(0,0,.6),(0,0,1.15)],[.015,.01],LIGHT,.9,5);ring(M,(0,0,.95),.04,.008,ACC,seg=10,sides=4)               # sensor boom
    dish(M,(0,.15,-.3),.08)
    for sx in (1,-1):
        plate(M,[(sx*.1,0,.05),(sx*.6,.04,-.35),(sx*.56,.04,-.45),(sx*.1,0,-.35)],.02,LIGHT)
        M.blob((sx*.58,.04,-.4),.035,WIN,sub=1,noise=0)
        plate(M,[(sx*.05,.08,-.55),(sx*.16,.28,-.78),(sx*.16,.28,-.84),(sx*.05,.07,-.8)],.018,ACC,.95)
    limpets(M,(0,-.1,-.1))
    M.vent((0,0,-.82),.06)
    return finish(M,1.9,1.0)
def skylark():   # advanced scout: a larger lens body carrying a big radome on twin pylons, limpet pods under the wings, twin tails
    M=Mesh(82)
    loft(M,[(-1.0,LENS(.12,.1)),(-.5,LENS(.2,.16)),(.3,LENS(.18,.15)),(.75,LENS(.07,.07,-.01))],lens_role)
    M.blob((0,.14,.3),.09,GLASS,sub=2,squash=(.9,.75,2.2),noise=0)
    for sx in (1,-1):plate(M,[(sx*.04,.14,-.1),(sx*.08,.38,-.2),(sx*.08,.38,-.35),(sx*.04,.14,-.4)],.02,LIGHT)      # radome pylons
    M.blob((0,.42,-.28),.34,MID,sub=2,squash=(1,.17,1),noise=0);ring(M,(0,.42,-.28),.34,.018,ACC,seg=26,sides=4,axis='y')   # the radome
    for sx in (1,-1):
        plate(M,[(sx*.15,0,.1),(sx*.75,.03,-.4),(sx*.7,.03,-.52),(sx*.15,0,-.45)],.025,LIGHT)
        tube(M,[(sx*.45,-.06,-.05),(sx*.45,-.06,-.4)],[.035,.035],DARK,.9,6);limpets(M,(sx*.45,-.1,-.1),3)          # limpet pods
        M.blob((sx*.72,.03,-.46),.04,WIN,sub=1,noise=0)
        plate(M,[(sx*.08,.1,-.7),(sx*.2,.35,-.98),(sx*.2,.35,-1.04),(sx*.08,.09,-1.0)],.02,ACC,.95)
    box(M,(0,-.13,.0),(.1,.06,.2),ACC)                                                                               # beacon device
    M.vent((0,0,-1.02),.07)
    return finish(M,2.3,1.0)
def condor():    # bomber: a heavy lens fuselage, a great swept wing span with two torpedoes slung under each wing, twin tails
    M=Mesh(83)
    loft(M,[(-1.1,LENS(.16,.13)),(-.6,LENS(.27,.21)),(.3,LENS(.25,.2)),(.85,LENS(.1,.09,-.01)),(1.05,LENS(.02,.02,-.02))],lens_role)
    M.blob((0,.19,.5),.11,GLASS,sub=2,squash=(.9,.75,2.2),noise=0)
    for sx in (1,-1):
        plate(M,[(sx*.22,.02,.35),(sx*1.25,.08,-.45),(sx*1.2,.08,-.62),(sx*.22,.02,-.5)],.04,LIGHT)                 # great swept wing
        M.blob((sx*1.22,.08,-.54),.05,WIN,sub=1,noise=0)
        for dx in (.5,.85):tube(M,[(sx*dx,-.02,0),(sx*dx,-.07,0)],[.02,.02],DARK,.9,4);torpedo(M,(sx*dx,-.12,-.45),.75,.055)   # slung torpedoes
        plate(M,[(sx*.12,.15,-.65),(sx*.28,.48,-1.0),(sx*.28,.48,-1.08),(sx*.12,.14,-1.02)],.025,ACC,.95)
        M.vent((sx*.12,0,-1.1),.08)
    plate(M,[(-.14,-.2,.3),(.14,-.2,.3),(.14,-.2,-.5),(-.14,-.2,-.5)],.02,DARK)                                    # bomb-bay doors
    return finish(M,2.7,1.0)
def harrier():   # heavy bomber: a long hull with tandem canopies, inverted-gull wings with torpedo pods, a rear ball turret
    M=Mesh(84)
    loft(M,[(-1.25,LENS(.15,.13)),(-.7,LENS(.28,.22)),(.4,LENS(.27,.22)),(.95,LENS(.1,.09,-.01)),(1.15,LENS(.02,.02,-.02))],lens_role)
    for z in (.65,.3):M.blob((0,.2,z),.1,GLASS,sub=2,squash=(.9,.75,1.6),noise=0)                                  # tandem canopies: two seats
    turret(M,(0,.24,-1.0),.11)                                                                                       # rear turret
    for sx in (1,-1):
        plate(M,[(sx*.25,.0,.25),(sx*.6,-.15,-.05),(sx*.58,-.15,-.3),(sx*.25,.0,-.4)],.04,LIGHT)                     # inverted gull, inner
        plate(M,[(sx*.6,-.15,-.05),(sx*1.15,-.02,-.35),(sx*1.1,-.02,-.5),(sx*.58,-.15,-.3)],.035,LIGHT,.95)
        loft(M,[(-.65,[(a+sx*.62,b-.2) for a,b in LENS(.04,.04)]),(-.45,[(a+sx*.62,b-.2) for a,b in LENS(.11,.1)]),(.25,[(a+sx*.62,b-.2) for a,b in LENS(.11,.1)]),(.42,[(a+sx*.62,b-.2) for a,b in LENS(.04,.04)])],(MID,.95))   # torpedo pod
        torpedo(M,(sx*.62,-.33,-.35),.75,.05)
        M.blob((sx*1.12,-.02,-.44),.045,WIN,sub=1,noise=0)
        plate(M,[(sx*.14,.17,-.65),(sx*.25,.42,-.95),(sx*.25,.42,-1.02),(sx*.14,.16,-.98)],.025,ACC,.95)
        M.vent((sx*.13,0,-1.27),.08)
    return finish(M,2.9,1.0)

# ============================================================== VARKESH
def jackal():    # scout: a small hex wedge with a forward sensor box and a tall antenna mast
    M=Mesh(91)
    loft(M,[(-.7,HEX(.14,.12)),(-.2,HEX(.18,.15)),(.3,HEX(.15,.12)),(.55,HEX(.08,.07,-.02))],hex_role)
    plate(M,[(-.05,.15,.3),(.05,.15,.3),(.05,.17,.1),(-.05,.17,.1)],.02,GLASS)
    abox(M,(0,-.05,.65),(.12,.1,.22),DARK,(.7,.7));M.blob((0,-.05,.78),.04,WIN,sub=1,noise=0)                         # sensor box
    mast(M,(0,.15,-.25),.4)
    for sx in (1,-1):
        plate(M,[(sx*.15,-.02,.1),(sx*.45,-.04,-.15),(sx*.45,-.04,-.35),(sx*.15,-.02,-.45)],.05,DARK)
        plate(M,[(sx*.12,.15,-.35),(sx*.18,.3,-.55),(sx*.18,.3,-.62),(sx*.12,.15,-.62)],.04,ACC,.9)
        sqdrive(M,(sx*.08,0,-.75),.13)
    limpets(M,(0,-.17,-.05))
    return finish(M,1.9,1.0)
def wolfhound(): # advanced scout: a hex hull with two sensor sponsons carrying dishes, a mast cluster, limpet racks, a beacon device
    M=Mesh(92)
    loft(M,[(-.95,HEX(.18,.15)),(-.3,HEX(.22,.18)),(.4,HEX(.19,.16)),(.7,HEX(.1,.08,-.02))],hex_role)
    plate(M,[(-.06,.18,.45),(.06,.18,.45),(.06,.2,.2),(-.06,.2,.2)],.02,GLASS)
    for sx in (1,-1):
        loft(M,[(-.6,HEX(.08,.09,0,sx*.42)),(.2,HEX(.09,.1,0,sx*.43)),(.45,HEX(.06,.07,-.01,sx*.4))],hex_role)        # sensor sponson
        dish(M,(sx*.43,.13,-.1),.1)
        plate(M,[(sx*.17,0,.1),(sx*.36,0,.1),(sx*.36,0,-.35),(sx*.17,0,-.35)],.05,DARK)
        limpets(M,(sx*.43,-.12,.1),3)
        sqdrive(M,(sx*.1,0,-1.02),.15)
    for dx,h in ((-.05,.42),(.06,.32)):mast(M,(dx,.17,-.45),h,rings=1)
    abox(M,(0,-.17,.0),(.12,.06,.22),ACC,(1,1))                                                                      # beacon device
    return finish(M,2.3,1.0)
def maul():      # bomber: a fat armoured hex hull over a torpedo magazine with four tubes in its face, stubby wings
    M=Mesh(93)
    loft(M,[(-1.0,HEX(.3,.24)),(-.4,HEX(.36,.28)),(.4,HEX(.34,.27)),(.7,HEX(.22,.17,-.02)),(.88,HEX(.12,.09,-.03))],hex_role)
    plate(M,[(-.08,.27,.55),(.08,.27,.55),(.08,.3,.25),(-.08,.3,.25)],.025,GLASS)
    abox(M,(0,-.3,-.05),(.55,.22,1.2),DARK,(.85,.85))                                                                # torpedo magazine
    for x in (-.13,.13):
        for y in (-.25,-.36):tube(M,[(x,y,.55),(x,y,.62)],[.05,.05],DARK,.8,8,cap0=False,cap1=False);M.blob((x,y,.6),.04,ACC,sub=1,noise=0)   # tubes with warheads
    for sx in (1,-1):
        plate(M,[(sx*.32,-.02,.2),(sx*.75,-.04,-.1),(sx*.75,-.04,-.45),(sx*.32,-.02,-.65)],.08,MID)
        torpedo(M,(sx*.62,-.13,-.4),.65,.05)
        for k,z in enumerate((.25,-.15,-.55)):abox(M,(sx*.36,.13,z),(.07,.2,.3),MID,(.9,.85),.96+.03*k)
        for dy in (.1,-.1):sqdrive(M,(sx*.16,dy,-1.08),.17)
        plate(M,[(sx*.25,.26,-.5),(sx*.33,.48,-.78),(sx*.33,.48,-.88),(sx*.25,.26,-.88)],.06,ACC,.9)
    return finish(M,2.6,1.0)
def warhound():  # heavy bomber: a long hex hull with two seats, a dorsal turret aft, torpedo racks on armoured sponsons
    M=Mesh(94)
    chis=lambda w,h,dy=0:[(w,dy),(w*.8,h+dy),(-w*.8,h+dy),(-w,dy),(-w*.7,-h*.7+dy),(w*.7,-h*.7+dy)]
    loft(M,[(-1.2,HEX(.3,.26)),(-.5,HEX(.36,.3)),(.5,HEX(.33,.28)),(.9,chis(.26,.2,-.02)),(1.15,chis(.17,.08,-.05))],hex_role)
    for z in (.7,.35):plate(M,[(-.08,.29,z+.12),(.08,.29,z+.12),(.08,.32,z-.1),(-.08,.32,z-.1)],.025,GLASS)       # two seats
    abox(M,(0,.38,-.7),(.26,.14,.34),DARK,(.9,.9));turret(M,(0,.5,-.75),.11,MID)                                   # dorsal turret aft
    for sx in (1,-1):
        loft(M,[(-1.0,HEX(.13,.15,0,sx*.55)),(.1,HEX(.15,.17,0,sx*.57)),(.55,HEX(.11,.13,-.01,sx*.52))],hex_role)   # armoured sponson
        for dy in (.06,-.12):torpedo(M,(sx*.72,dy,-.45),.7,.05)                                                      # torpedo rack
        plate(M,[(sx*.25,0,.3),(sx*.45,0,.3),(sx*.45,0,-.6),(sx*.25,0,-.6)],.07,DARK)
        for dy in (.1,-.1):sqdrive(M,(sx*.2,dy,-1.3),.18)
    return finish(M,2.9,1.0)

# ============================================================== OSTROVA
def seer():      # scout: a thin spire behind a forward sensor halo with a crystal eye, a long mast
    M=Mesh(101)
    loft(M,[(-.8,DIA(.04,.04)),(-.45,DIA(.1,.09)),(.2,DIA(.11,.1)),(.5,DIA(.05,.05))],SP)
    ring(M,(0,0,.62),.16,.02,ACC,seg=20,sides=5);crystal(M,.5,.78,.06,.06)                                          # sensor halo and crystal eye
    for k in range(3):a=PI/2+k*2*PI/3;tube(M,[(math.cos(a)*.04,math.sin(a)*.04,.45),(math.cos(a)*.15,math.sin(a)*.15,.62)],[.01,.01],LIGHT,.9,4)
    M.blob((0,.09,.1),.06,GLASS,sub=2,squash=(.9,.7,1.8),noise=0)
    mast(M,(0,.08,-.35),.35)
    for k in range(3):a=PI/2+k*2*PI/3;plate(M,[(math.cos(a)*.08,math.sin(a)*.08,-.45),(math.cos(a)*.38,math.sin(a)*.38,-.72),(math.cos(a)*.34,math.sin(a)*.34,-.8),(math.cos(a)*.06,math.sin(a)*.06,-.75)],.02,MID)
    limpets(M,(0,-.1,-.05))
    M.vent((0,0,-.82),.05)
    return finish(M,1.9,1.0)
def oracle():    # advanced scout: a spire under a great sensor dish, two rings crossed in an X, crystal nodes, limpet launchers, a beacon device
    M=Mesh(102)
    loft(M,[(-1.0,DIA(.05,.05)),(-.55,DIA(.13,.12)),(.35,DIA(.13,.12)),(.75,DIA(.04,.04))],SP)
    dish(M,(0,.3,.1),.28);tube(M,[(0,.08,.1),(0,.24,.1)],[.03,.03],LIGHT,.9,5);M.blob((0,.36,.1),.05,WIN,sub=1,noise=0)   # great sensor dish
    for th in (PI/4,-PI/4):
        u=np.array([math.sin(th),math.cos(th),0.])
        pts=[np.array([0,0,-.5])+u*math.cos(a)*.42+np.array([0,0,math.sin(a)*.42]) for a in np.linspace(0,2*PI,33)]
        M.tube(pts,[.025]*len(pts),5,lambda i,j,n,p:(ACC,1.0),cap0=False,cap1=False)
        for sg in (1,-1):M.blob(tuple(np.array([0,0,-.5])+u*sg*.42),.045,GLASS,sub=1,noise=0)
    for sx in (1,-1):tube(M,[(sx*.13,-.05,.2),(sx*.13,-.05,-.2)],[.03,.03],DARK,.9,6);limpets(M,(sx*.13,-.1,.1),3)
    box(M,(0,-.14,.35),(.08,.05,.16),ACC)                                                                              # beacon device
    M.blob((0,.12,.5),.06,GLASS,sub=2,squash=(.9,.7,1.8),noise=0)
    M.vent((0,0,-1.02),.05)
    return finish(M,2.3,1.0)
def obelisk():   # bomber: a square crystal-veined obelisk hull with a pyramid prow, torpedo lances on a halo round it
    M=Mesh(103)
    sq=lambda w,h:[(w,-h),(w,h),(-w,h),(-w,-h)]
    loft(M,[(-1.0,sq(.2,.24)),(.6,sq(.17,.21)),(.95,sq(.02,.02))],lambda i,j:([LIGHT,MID,LIGHT,DARK][j],[1,.95,.9,.85][j]))   # the obelisk
    for sx in (1,-1):plate(M,[(sx*.21,-.15,-.8),(sx*.21,.15,-.8),(sx*.18,.12,.5),(sx*.18,-.12,.5)],.01,WIN,.85)
    plate(M,[(-.08,.25,.5),(.08,.25,.5),(.07,.22,.68),(-.07,.22,.68)],.02,GLASS)
    ring(M,(0,0,-.3),.5,.035,ACC)
    for k in range(4):
        a=PI/4+k*PI/2;x,y=math.cos(a)*.5,math.sin(a)*.5
        torpedo(M,(x,y,-.75),.85,.055,LIGHT)                                                                         # torpedo lances on the halo
        tube(M,[(math.cos(a)*.24,math.sin(a)*.24,-.3),(x*.9,y*.9,-.3)],[.02,.02],LIGHT,.9,4)
    for k in range(3):a=PI/2+k*2*PI/3;plate(M,[(math.cos(a)*.15,math.sin(a)*.15,-.7),(math.cos(a)*.45,math.sin(a)*.45,-.98),(math.cos(a)*.4,math.sin(a)*.4,-1.06),(math.cos(a)*.12,math.sin(a)*.12,-1.0)],.025,MID)
    for dy in (.12,-.12):M.vent((0,dy,-1.02),.06)
    return finish(M,2.6,1.0)
def sentinel():  # heavy bomber: a spire with tandem seats, a turret riding a halo aft, torpedo lances under crystal fins
    M=Mesh(104)
    loft(M,[(-1.2,DIA(.07,.07)),(-.7,DIA(.19,.18)),(.4,DIA(.2,.19)),(.95,DIA(.08,.08)),(1.15,DIA(.01,.01))],SP)
    for z in (.65,.3):M.blob((0,.17,z),.08,GLASS,sub=2,squash=(.9,.7,1.6),noise=0)                                 # two seats
    ring(M,(0,0,-.75),.42,.035,ACC);turret(M,(0,.48,-.75),.1,ACC)                                                    # turret riding the aft halo
    for k in range(3):
        a=PI/2+k*2*PI/3;ca,sa=math.cos(a),math.sin(a)
        tube(M,[(ca*.15,sa*.15,-.75),(ca*.38,sa*.38,-.75)],[.022,.022],LIGHT,.9,4)
        plate(M,[(ca*.12,sa*.12,-.95),(ca*.55,sa*.55,-1.2),(ca*.5,sa*.5,-1.28),(ca*.1,sa*.1,-1.22)],.025,MID)
    for sx in (1,-1):
        plate(M,[(sx*.15,-.05,.35),(sx*.5,-.1,.0),(sx*.48,-.1,-.25),(sx*.15,-.05,-.35)],.025,WIN,.85)              # crystal fins
        torpedo(M,(sx*.36,-.18,-.4),.8,.05,LIGHT)                                                                      # torpedo lances
    M.vent((0,0,-1.22),.06)
    return finish(M,2.9,1.0)

RECON=[('halcyon','Halcyon Accord',[('Lark','Scout',lark),('Skylark','Advanced scout',skylark),('Condor','Bomber',condor),('Harrier','Heavy bomber',harrier)]),
       ('varkesh','Varkesh Dominion',[('Jackal','Scout',jackal),('Wolfhound','Advanced scout',wolfhound),('Maul','Bomber',maul),('Warhound','Heavy bomber',warhound)]),
       ('ostrova','Ostrova Collective',[('Seer','Scout',seer),('Oracle','Advanced scout',oracle),('Obelisk','Bomber',obelisk),('Sentinel','Heavy bomber',sentinel)])]
