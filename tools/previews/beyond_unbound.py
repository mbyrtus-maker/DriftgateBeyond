# Driftgate Beyond: the Unbound's hulls (preview, not in the model pack yet). First pass.
# The Unbound design nothing of their own: every hull is parts of all three factions' ships welded into one, often lopsided.
#   Halcyon parts  lens pods and fuselages, swept wings, emitter nodes, glass canopies, dishes   (light plating, shade up)
#   Varkesh parts  hex and smoothed-hex slabs, chisel prows, square drives, exposed guns         (dark plating, shade down)
#   Ostrova parts  octagonal faceted spires, crystals, halos                                     (mid plating with crystal)
#   Unbound marks  weld seams round every joint, scrap patches, ram spikes
# Nose is +z, up +y; finish() sets the length (fighters 2.0, medium 2.6, heavy 3.2, capitals 3.6-4.6).
import math
import numpy as np
from beyond_hulls import Mesh,LIGHT,MID,DARK,ACC,GLASS,GLOW,WIN,loft,box,plate,barrel,ring,LENS,HEX,lens_role,hex_role
from beyond_work import finish,crystal,abox,lights,STAR
from beyond_recon import dish,SMH,smh_role
from beyond_capitals import tube,pd,bridge_varkesh,giant_gun
PI=math.pi
OCT=lambda w,h,dx=0,dy=0:[(math.cos(a)*w+dx,math.sin(a)*h+dy) for a in np.linspace(PI/8,2*PI+PI/8,8,endpoint=False)]
def oct_role(i,j):return ([LIGHT,LIGHT,LIGHT,MID,MID,DARK,DARK,MID][j],[.95,.92,.95,.9,.85,.8,.8,.88][j])
def at(sec,dx=0,dy=0):return [(a+dx,b+dy) for a,b in sec]
def dark_hex(i,j):r,sh=hex_role(i,j);return (r,sh*.78)
def dark_smh(i,j):r,sh=smh_role(i,j);return (r,sh*.78)
def light_lens(i,j):r,sh=lens_role(i,j);return (r,min(sh*1.08,1.1))

# ------------------------------------------------------------------ parts
def hal_pod(M,secs,dx=0,dy=0):loft(M,[(z,at(LENS(w,h),dx,dy)) for z,w,h in secs],light_lens)
def var_slab(M,secs,dx=0,dy=0,smooth=False):loft(M,[(z,at((SMH if smooth else HEX)(w,h),dx,dy)) for z,w,h in secs],dark_smh if smooth else dark_hex)
def ost_spire(M,secs,dx=0,dy=0):loft(M,[(z,OCT(w,h,dx,dy)) for z,w,h in secs],oct_role)
def weld(M,z,sec):
    # a weld seam: a thin bright band round a joint
    loft(M,[(z-.012,[(a*1.04,b*1.04) for a,b in sec]),(z+.012,[(a*1.04,b*1.04) for a,b in sec])],(ACC,.85),cap0=False,cap1=False)
def patch(M,c,w,l,n=(0,1,0)):
    # a scrap patch plate riveted over the hull
    c=np.array(c,float);n=np.array(n,float);n/=np.linalg.norm(n);u=np.cross(n,[0,0,1.]) if abs(n[2])<.9 else np.array([1.,0,0]);u/=np.linalg.norm(u);v=np.cross(n,u)
    plate(M,[c-u*w/2-v*l/2,c+u*w/2-v*l/2*.8,c+u*w/2+v*l/2,c-u*w/2*.7+v*l/2],.012,DARK,.75)
def spikes(M,pts,d=(0,0,1),L=.12,r=.025):
    d=np.array(d,float)
    for p in pts:p=np.array(p,float);tube(M,[p,p+d*L],[r,.002],DARK,.9,5,cap0=True,cap1=False)
def hal_wing(M,root,tip,chord=.4,node=True):
    # a swept Halcyon wing from root to tip with an emitter node
    r=np.array(root,float);t=np.array(tip,float)
    plate(M,[r+[0,0,chord*.5],t+[0,0,chord*.18],t-[0,0,chord*.12],r-[0,0,chord*.5]],.025,LIGHT,1.05)
    if node:M.blob(tuple(t),.05,WIN,sub=1,noise=0)
def var_stub(M,c,size):abox(M,c,size,DARK,(.8,.8),.8)
def var_gun(M,c,L=.35,r=.03,n=1,sp=.07):
    c=np.array(c,float);abox(M,tuple(c+[0,0,-.06]),(r*3.2+sp*(n-1),r*2.6,.16),DARK,(.8,.8),.75)
    for k in range(n):x=(k-(n-1)/2)*sp;tube(M,[c+[x,0,0],c+[x,0,L]],[r,r*.85],DARK,1.0,6)
def sq_drive(M,c,s):box(M,c,(s,s*.85,s*.8),DARK,sh=.75);M.vent((c[0],c[1],c[2]-s*.42),s*.36)
def canopy(M,c,r,sq=(1,.75,1.6)):M.blob(tuple(c),r,GLASS,sub=2,squash=sq,noise=0)

# ------------------------------------------------------------------ hulls
def raider():
    # light: a stolen Halcyon lens fuselage and canopy on a Varkesh hex drive block, a Halcyon swept wing mounted high on top reaching
    # right to a small Varkesh pontoon braced back to the fuselage, a Varkesh gun stub on the left, an Ostrova crystal for a radar mast, a scrap cargo pod under the belly, ram spikes on the nose
    M=Mesh(401)
    hal_pod(M,[(-.45,.2,.16),(.5,.22,.17),(1.0,.12,.09),(1.22,.03,.03)])
    var_slab(M,[(-1.2,.26,.2),(-.42,.3,.22)]);weld(M,-.43,HEX(.3,.22))
    for x in (-.14,.14):M.vent((x,0,-1.21),.09)
    canopy(M,(0,.14,.5),.13)
    hal_wing(M,(.08,.2,.0),(.95,.3,-.5),.45,node=False)                                                          # high wing on top, to the right
    var_slab(M,[(-.85,.05,.04),(-.75,.08,.07),(-.2,.08,.07),(-.1,.05,.04)],dx=.95,dy=.22)                          # small pontoon at its tip
    var_gun(M,(.95,.22,-.1),.4,.028);M.blob((.95,.3,-.78),.04,WIN,sub=1,noise=0)
    tube(M,[(.92,.16,-.45),(.18,-.05,-.3)],[.018,.018],DARK,.85,5)                                                # brace back to the fuselage
    var_stub(M,(-.38,-.02,-.2),(.42,.12,.4));var_gun(M,(-.55,-.02,.0),.45,.032)
    crystal(M,-.95,-.55,.05,.05,0,.27);tube(M,[(0,.18,-.75),(0,.3,-.75)],[.015,.015],LIGHT,.9,4)
    box(M,(0,-.2,-.25),(.22,.12,.45),MID,sh=.8)
    patch(M,(.08,.2,-.1),.1,.16);spikes(M,[(.06,-.05,1.05),(-.06,-.05,1.05)])
    return finish(M,2.0,1.0)
def skiff():
    # scout: a slender Ostrova faceted spire for a hull, a salvaged Halcyon radome dish on a strut, two Varkesh square drives
    # strapped to its flanks, small forward-swept Halcyon wings,
    # a jammer array of rods aft
    M=Mesh(402)
    ost_spire(M,[(-1.1,.14,.13),(-.6,.2,.18),(.6,.18,.16),(1.15,.05,.05),(1.3,.01,.01)])
    weld(M,-.6,OCT(.2,.18));weld(M,.6,OCT(.18,.16))
    for sx in (1,-1):
        sq_drive(M,(sx*.27,-.02,-.75),.16)
        for z in (-.62,-.88):ring(M,(sx*.27,-.02,z),.1,.012,ACC,seg=10,sides=4)
        tube(M,[(sx*.17,-.02,-.75),(sx*.2,-.02,-.75)],[.03,.03],DARK,.8,4)
    tube(M,[(0,.15,.0),(0,.42,.05)],[.025,.02],LIGHT,.9,5);dish(M,(0,.47,.05),.17)
    canopy(M,(0,.12,.62),.09,(1,.7,1.8))
    for sx in (1,-1):hal_wing(M,(sx*.16,-.02,-.25),(sx*.62,-.05,.12),.3)                                           # small forward-swept wings
    for k,x in enumerate((-.1,0,.1)):tube(M,[(x,.1,-.9),(x*1.6,.4+.06*(k%2),-1.15)],[.01,.006],LIGHT,.9,4);M.blob((x*1.6,.4+.06*(k%2),-1.15),.025,WIN,sub=1,noise=0)
    patch(M,(-.12,.14,.2),.08,.2,(-.5,1,0))
    return finish(M,2.2,1.0)
def corsair():
    # medium: a Varkesh hex body with a chisel prow and twin chin guns, welded to a Halcyon lens drive section, matching Halcyon swept
    # wings, a small Ostrova ring on the nose, an Ostrova halo round the tail as a jammer
    M=Mesh(403)
    var_slab(M,[(-.3,.3,.22),(.9,.3,.22),(1.35,.16,.12),(1.55,.04,.03)],smooth=True)
    hal_pod(M,[(-1.35,.22,.18),(-.85,.3,.22),(-.28,.3,.22)]);weld(M,-.29,SMH(.3,.22))
    for x in (-.11,.11):M.vent((x,0,-1.36),.1)
    canopy(M,(0,.2,.65),.14)
    for sx in (1,-1):hal_wing(M,(sx*.26,0,-.1),(sx*1.05,-.05,-.7),.55)                                             # matching wings
    ring(M,(0,-.02,1.18),.3,.025,ACC,seg=24,sides=5)                                                                # small Ostrova ring on the nose
    for sx in (1,-1):tube(M,[(sx*.19,-.02,1.18),(sx*.28,-.02,1.18)],[.015,.015],LIGHT,.9,4)
    for x in (-.1,.1):var_gun(M,(x,-.2,.7),.55,.03)
    ring(M,(0,.02,-1.05),.48,.03,ACC,seg=28,sides=5);tube(M,[(0,.2,-1.05),(0,.47,-1.05)],[.02,.02],LIGHT,.9,4);tube(M,[(0,-.15,-1.05),(0,-.47,-1.05)],[.02,.02],LIGHT,.9,4)
    for a in (PI/4,3*PI/4,5*PI/4,7*PI/4):M.blob((math.cos(a)*.48,math.sin(a)*.48+.02,-1.05),.03,WIN,sub=1,noise=0)
    patch(M,(.12,.22,.3),.12,.25);patch(M,(-.2,.15,-.6),.1,.18,(-.6,1,0));spikes(M,[(.08,0,1.45),(-.08,0,1.45)],L=.14)
    return finish(M,2.6,1.0)
def plunderer():
    # heavy: a Halcyon lens cockpit pod on a Varkesh box spine; the holds don't match (a Varkesh hex container to port, a long Ostrova
    # crystal hold to starboard), a Halcyon engine boom on a pylon on top, an Ostrova crystal
    # pontoon underneath, a Varkesh drive block on the right, a turret on top
    M=Mesh(404)
    hal_pod(M,[(.55,.24,.2),(1.1,.26,.21),(1.5,.14,.1),(1.68,.03,.03)]);canopy(M,(0,.2,1.05),.15)
    var_slab(M,[(-1.35,.22,.2),(.6,.24,.22)]);weld(M,.56,HEX(.24,.22))
    for z in (-.9,-.1):tube(M,[(-.18,0,z),(-.42,0,z)],[.04,.04],DARK,.8,5);tube(M,[(.18,0,z),(.42,0,z)],[.04,.04],DARK,.8,5)
    var_slab(M,[(-1.15,.16,.2),(.25,.16,.2)],dx=-.58,smooth=True);weld(M,-.45,SMH(.16,.2))                          # Varkesh container hold
    for z in (-.95,-.45,.05):loft(M,[(z-.02,at(SMH(.17,.21),-.58)),(z+.02,at(SMH(.17,.21),-.58))],(ACC,.85))
    crystal(M,-1.25,.4,.19,.2,.6,0)                                                                                 # Ostrova crystal hold
    tube(M,[(0,.46,-.45),(0,.46,-1.75)],[.12,.14],LIGHT,1.05,10,cap1=False);M.vent((0,.46,-1.76),.11)               # Halcyon boom engine on a pylon on top
    for z in (-.8,-1.35):abox(M,(0,.33,z),(.08,.2,.16),DARK,(1,1),.75)
    crystal(M,-1.15,.35,.13,.13,0,-.47)                                                                            # crystal pontoon underneath
    for z in (-.75,-.1):tube(M,[(0,-.2,z),(0,-.38,z)],[.03,.03],DARK,.8,5)
    sq_drive(M,(.3,-.02,-1.45),.26);M.vent((-.0,0,-1.36),.11)                                                       # Varkesh drive block
    pd(M,(0,.22,.25),.09,MID)
    patch(M,(0,.24,.1),.16,.3);patch(M,(.1,.23,-.9),.12,.2);spikes(M,[(.1,-.06,1.55),(-.1,-.06,1.55),(0,-.12,1.5)],L=.15)
    lights(M,[(.16,-.06,1.5),(-.16,-.06,1.5)],.03)
    return finish(M,3.2,1.0)
def wrecker():
    # bomber: a heavy Varkesh smoothed-hex fuselage under a pair of big stolen Halcyon wings, Ostrova crystals slung under the wings as
    # torpedoes, an Ostrova faceted tail spire with a small halo, a Halcyon canopy set crooked on top
    M=Mesh(405)
    var_slab(M,[(-1.0,.24,.2),(.8,.3,.24),(1.25,.16,.12),(1.45,.04,.03)],smooth=True)
    ost_spire(M,[(-1.7,.05,.05),(-1.3,.16,.15),(-.95,.22,.19)]);weld(M,-.98,OCT(.22,.19))
    ring(M,(0,.0,-1.42),.26,.025,ACC,seg=24,sides=5)
    for x in (-.11,.11):M.vent((x,0,-1.72),.06)
    canopy(M,(.04,.22,.55),.14)
    for sx in (1,-1):
        hal_wing(M,(sx*.24,.02,.2),(sx*1.25,-.05,-.55),.65)
        tube(M,[(sx*.62,-.04,-.1),(sx*.62,-.13,-.1)],[.02,.02],DARK,.8,4)
        crystal(M,-.55,.35,.07,.07,sx*.62,-.18)                                                                     # crystal torpedoes
        crystal(M,-.45,.3,.055,.055,sx*.95,-.13)
    var_gun(M,(0,-.2,.95),.4,.03,2,.08)
    patch(M,(-.1,.25,.0),.14,.3);patch(M,(.15,.22,-.5),.1,.2,(.6,1,0))
    return finish(M,2.7,1.0)
def ravager():
    # capital (destroyer class): three faction hulls welded end to end, a Varkesh chisel prow with ram spikes, a Halcyon lens
    # midsection, an Ostrova faceted stern inside a halo carrying turrets; a salvaged Halcyon rail cannon along the spine with
    # glowing accelerator rings, a Varkesh giant gun on top, a stepped Varkesh bridge with a Halcyon dish; a Halcyon turret sponson
    # to port and a Varkesh turret pylon to starboard; mismatched drives
    M=Mesh(406)
    var_slab(M,[(.85,.42,.32),(1.7,.36,.26),(2.3,.14,.1),(2.45,.03,.03)],smooth=True)                                # Varkesh prow
    hal_pod(M,[(-.9,.5,.34),(.0,.56,.38),(.9,.46,.34)]);weld(M,.88,SMH(.42,.32))                                     # Halcyon midsection
    ost_spire(M,[(-2.5,.24,.22),(-2.2,.38,.32),(-.9,.44,.34)]);weld(M,-.9,OCT(.44,.34))                              # Ostrova stern
    tube(M,[(0,.42,-.4),(0,.42,2.6)],[.06,.05],DARK,.95,10,cap1=False)                                              # rail cannon
    for z in (1.2,1.6,2.0,2.35):ring(M,(0,.42,z),.13,.02,WIN,seg=16,sides=5)
    for z in (-.3,.5):tube(M,[(0,.3,z),(0,.4,z)],[.05,.05],DARK,.85,6)
    giant_gun(M,(.22,.36,-.3))
    bridge_varkesh(M,(-.2,.38,-1.15),.9);dish(M,(-.2,.86,-1.25),.12)
    ring(M,(0,0,-1.7),.72,.05,ACC,seg=36,sides=6)                                                                     # halo with turrets
    for a in (PI/2+.5,PI/2-.5,-PI/2):pd(M,(math.cos(a)*.72,math.sin(a)*.72+(.05 if math.sin(a)>0 else -.05),-1.7),.07,ACC,up=math.sin(a)>0)
    for a in (0,PI):tube(M,[(math.cos(a)*.4,0,-1.7),(math.cos(a)*.68,0,-1.7)],[.03,.03],LIGHT,.9,5)
    hal_pod(M,[(-.7,.06,.06),(-.4,.14,.13),(.6,.14,.13),(.85,.05,.05)],dx=-.62,dy=-.05)                              # Halcyon sponson to port
    for z in (-.3,.4):pd(M,(-.64,.1,z),.065,LIGHT)
    abox(M,(.95,-.05,.05),(.22,.2,1.3),DARK,(.8,.8),.75)                                                             # Varkesh pylon to starboard
    for z in (-.2,.6):abox(M,(.68,-.05,z),(.4,.08,.12),DARK,(1,1),.7);pd(M,(.95,.08,z),.065,MID)
    for x,y in ((-.12,-.1),(.12,-.1)):sq_drive(M,(x,y,-2.55),.16)
    for k in range(3):a=PI/2+k*2*PI/3;M.vent((math.cos(a)*.13,math.sin(a)*.12+.08,-2.52),.06)
    M.vent((-.62,-.05,-.72),.07)
    spikes(M,[(.16,-.1,2.25),(-.16,-.1,2.25),(.25,.05,2.0),(-.25,.05,2.0)],(0,0,1),.25,.04)
    for c,n in (((.2,.36,.3),(0,1,0)),((-.3,.32,-.5),(-.4,1,0)),((.35,-.2,1.3),(.5,-1,0)),((-.35,.1,-2.0),(-1,.3,0))):patch(M,c,.22,.4,n)
    lights(M,[(.2,-.15,2.0),(-.2,-.15,2.0)],.04)
    return finish(M,4.0,1.0)

UNBOUND=[('pirate','The Unbound',[('Raider','Light',raider),('Skiff','Scout',skiff),('Corsair','Medium',corsair)]),
         ('pirate','The Unbound',[('Plunderer','Heavy (hold)',plunderer),('Wrecker','Bomber',wrecker),('Ravager','Capital (destroyer class)',ravager)])]
