# Driftgate Beyond: the house-brand hulls and the Wraith, centuries on from Driftgate 1 (preview, not in the model pack yet). First pass.
# Driftgate 1's Gannet, Bombard and Vesper were conversions of a stock hull; in Beyond each is its own design in its faction's
# language, built around the weapon that made its name. The Wraith, a conqueror's trophy, belongs to no faction: a faceted stealth wing.
import math
import numpy as np
from beyond_hulls import Mesh,LIGHT,MID,DARK,ACC,GLASS,GLOW,WIN,loft,box,plate,ring,LENS,HEX,lens_role
from beyond_work import finish,abox,crystal,lights,sqdrive,hatch
from beyond_recon import SMH,smh_role,dish
from beyond_capitals import tube,giant_gun,stacks
PI=math.pi
OCT=lambda w,h,dx=0,dy=0:[(math.cos(a)*w+dx,math.sin(a)*h+dy) for a in np.linspace(PI/8,2*PI+PI/8,8,endpoint=False)]
def oct_role(i,j):return ([LIGHT,LIGHT,LIGHT,MID,MID,DARK,DARK,MID][j],[1,.97,1,.95,.9,.85,.85,.92][j])

def cells(M,x0,x1,z0,z1,y,nx,nz,dy=0.0):
    # a bank of missile launch cells: dark square hatches with amber rims and a glow in each
    for i in range(nx):
        for k in range(nz):
            x=x0+(x1-x0)*(i+.5)/nx;z=z0+(z1-z0)*(k+.5)/nz;yy=y+dy*abs(x)
            w=(x1-x0)/nx*.38;l=(z1-z0)/nz*.38
            plate(M,[(x-w,yy,z-l),(x+w,yy,z-l),(x+w,yy,z+l),(x-w,yy,z+l)],.012,DARK,.8)
            M.blob((x,yy+.008,z),min(w,l)*.45,WIN,sub=1,squash=(1,.3,1),noise=0)

def gannet():
    # Halcyon house-brand hauler: the hauler line's thick lens flying wing (the Albatross's frame, centuries on), its wing bays split
    # between freight hatches and banks of missile launch cells (the barrage), a glass cockpit set straight into the hull, small tail plates, floodlights
    M=Mesh(701)
    sec=lambda w,h,dy=0:[(math.cos(a)*w,math.sin(a)*h*(1 if math.sin(a)>0 else .55)+dy) for a in np.linspace(0,2*PI,16,endpoint=False)]
    loft(M,[(-1.0,sec(.75,.15)),(-.6,sec(1.3,.26)),(.2,sec(1.15,.28)),(.75,sec(.6,.22)),(1.1,sec(.2,.1))],lambda i,j:((LIGHT,1.0) if j<8 else (MID,.92)))
    for sx in (1,-1):
        cells(M,sx*.35,sx*1.0,-.55,.25,.27,3,4,-.02) if sx>0 else cells(M,sx*1.0,sx*.35,-.55,.25,.27,3,4,-.02)   # launch cells in the outer bays
        hatch(M,(sx*.22,.28,-.2),.22,.5)                                                                        # freight hatches on the spine
        plate(M,[(sx*.4,.22,-.7),(sx*.5,.42,-.92),(sx*.5,.42,-1.02),(sx*.4,.22,-.98)],.035,ACC,.95)
        M.blob((sx*1.28,.0,-.4),.06,WIN,sub=1,noise=0)
        for dx in (.3,.75):M.vent((sx*dx,0,-1.0),.09)
    M.blob((0,.24,.62),.15,GLASS,sub=2,squash=(1,.55,1.6),noise=0)                                                 # cockpit set straight into the hull
    lights(M,[(.38,-.02,1.05),(-.38,-.02,1.05)],.035)
    return finish(M,2.8,1.0)
def bombard():
    # Varkesh house-brand miner: one huge shell cannon running the whole length of the ship down its centre, carried between two
    # armoured side hulls joined by braces over it, disappearing astern into a broad armoured aft section; the port hull carries the
    # cockpit, the starboard hull the ore hopper and a docked Ward Drone; vents along each side hull's outer flank, stacks and drives
    M=Mesh(702)
    tube(M,[(0,0,-.7),(0,0,-.4),(0,0,1.5)],[.15,.12,.09],DARK,1.0,10,cap0=True,cap1=False)                          # the cannon, out of the aft section
    for z in (-.4,.3,.9):ring(M,(0,0,z),.12,.02,ACC,seg=14,sides=4)
    tube(M,[(0,0,1.45),(0,0,1.8)],[.13,.13],MID,.95,8,cap1=False)
    for z in (1.56,1.68):ring(M,(0,0,z),.135,.015,DARK,seg=12,sides=4)
    loft(M,[(-1.55,SMH(.62,.3)),(-.65,SMH(.66,.32)),(-.45,SMH(.5,.24))],smh_role)                                   # aft section the gun runs into
    for sx in (1,-1):
        loft(M,[(-1.3,[(a+sx*.45,b) for a,b in SMH(.2,.22)]),(.6,[(a+sx*.45,b) for a,b in SMH(.22,.24)]),(1.0,[(a+sx*.45,b-.02) for a,b in SMH(.14,.15)]),(1.2,[(a+sx*.45,b-.04) for a,b in SMH(.05,.05)])],smh_role)   # side hull
        sqdrive(M,(sx*.45,0,-1.68),.26);stacks(M,(sx*.45,.3,-1.1),1,.2,.26)
        for k in range(4):                                                                                       # vents along the outer flank
            z=-.1+k*.22;plate(M,[(sx*.665,-.08,z-.07),(sx*.665,.08,z-.07),(sx*.665,.08,z+.07),(sx*.665,-.08,z+.07)],.012,DARK,.7)
            plate(M,[(sx*.672,-.05,z-.04),(sx*.672,.05,z-.04),(sx*.672,.05,z+.04),(sx*.672,-.05,z+.04)],.006,GLOW,1.0)
        lights(M,[(sx*.45,-.12,1.1)],.03)
    for z in (-.55,.35):abox(M,(0,.16,z),(.7,.12,.2),MID,(1,1),.9)                                                   # braces over the cannon
    M.blob((-.45,.25,.55),.13,GLASS,sub=2,squash=(1,.65,1.5),noise=0)                                                # cockpit, port hull
    abox(M,(.45,.3,-.3),(.3,.18,.55),MID,(.9,.9));box(M,(.62,-.02,.25),(.1,.14,.2),MID)                             # hopper and docked Ward Drone, starboard
    return finish(M,3.0,1.0)
def vesper():
    # Ostrova house-brand scout: a slender faceted spire that is itself a railgun, two long crystal rails reaching forward through three
    # accelerator halos with a glowing slug between them; two rings crossed in an X round the stern for wings, the drive pontoons set on
    # the rings' four tips; a scout radome low on the spine
    M=Mesh(703)
    loft(M,[(-1.25,OCT(.1,.1)),(-.8,OCT(.2,.19)),(.3,OCT(.19,.18)),(.6,OCT(.1,.1)),(.7,OCT(.03,.03))],oct_role)
    M.blob((0,.16,.25),.09,GLASS,sub=2,squash=(1,.7,1.8),noise=0)
    for sx in (1,-1):
        crystal(M,.0,2.0,.07,.07,sx*.17,0)
        tube(M,[(sx*.08,0,.1),(sx*.17,0,.1)],[.03,.03],LIGHT,.9,5)
    for z in (.7,1.15,1.6):ring(M,(0,0,z),.26,.03,ACC,seg=24,sides=5);ring(M,(0,0,z),.25,.012,WIN,seg=24,sides=4)
    crystal(M,1.0,1.45,.05,.05,0,0);M.blob((0,0,1.22),.07,GLOW,sub=1,noise=0)
    dish(M,(0,.2,-.25),.16)
    zc=-.75;R=.55
    for th in (PI/4,-PI/4):                                                                                          # X-wing rings
        u=np.array([math.sin(th),math.cos(th),0.])
        pts=[np.array([0,0,zc])+u*math.cos(a)*R+np.array([0,0,math.sin(a)*R*.55]) for a in np.linspace(0,2*PI,37)]
        M.tube(pts,[.03]*len(pts),6,lambda i,j,n,p:(ACC,1.0),cap0=False,cap1=False)
        for sg in (1,-1):
            tip=np.array([0,0,zc])+u*sg*R
            loft(M,[(zc-.35,[(a+tip[0],b+tip[1]) for a,b in OCT(.05,.05)]),(zc+.1,[(a+tip[0],b+tip[1]) for a,b in OCT(.065,.065)]),(zc+.3,[(a+tip[0],b+tip[1]) for a,b in OCT(.02,.02)])],oct_role)   # pontoon on the ring
            M.vent((tip[0],tip[1],zc-.36),.035)
            tube(M,[u*sg*.18+[0,0,zc],u*sg*(R-.05)+[0,0,zc]],[.018,.018],LIGHT,.9,5,cap0=False,cap1=False)
    for k in range(3):a=PI/2+k*2*PI/3;M.vent((math.cos(a)*.06,math.sin(a)*.06,-1.26),.04)
    return finish(M,2.7,1.0)
def wraith():
    # the Wraith: a faceted stealth flying wing, clean and hard-angled, with some depth to it: a raised diamond body and spine, thick
    # wings blended into it with straight swept edges, drives buried in slit vents, two heavy guns hidden in the leading edge, a faceted
    # canopy, faint edge lights; a dark trophy finish
    M=Mesh(704)
    D=lambda w,h,dy=0:[(w,dy),(w*.4,h+dy),(-w*.4,h+dy),(-w,dy),(-w*.4,-h*.6+dy),(w*.4,-h*.6+dy)]
    role=lambda i,j:([LIGHT,MID,MID,LIGHT,DARK,DARK][j],[1,.95,.9,1,.8,.8][j])
    loft(M,[(-.95,D(.42,.1)),(-.35,D(.52,.2)),(.45,D(.34,.17)),(1.05,D(.04,.03))],role)                               # raised diamond body
    loft(M,[(-.85,D(.12,.08,.08)),(-.1,D(.14,.13,.14)),(.5,D(.07,.07,.12))],role)                                     # spine ridge, seated in the body
    for sx in (1,-1):
        W=[(sx*.25,.02,.42),(sx*1.2,-.03,-.6),(sx*1.08,-.03,-.82),(sx*.25,0,-.9)]
        plate(M,W,.08,MID,.92)                                                                                         # thick swept wing
        tube(M,[(sx*.48,.03,.32),(sx*1.2,-.02,-.58)],[.012,.012],GLOW,1.0,4,cap0=False,cap1=False)                      # edge light
        tube(M,[(sx*.33,-.04,.38),(sx*.33,-.04,.66)],[.025,.02],DARK,1.0,6)                                             # hidden guns
        plate(M,[(sx*.12,-.01,-.96),(sx*.34,-.01,-.94),(sx*.34,-.01,-.99),(sx*.12,-.01,-1.01)],.012,GLOW,1.0)            # slit vents
    loft(M,[(.12,D(.12,.05,.17)),(.45,D(.1,.07,.16)),(.68,D(.03,.02,.13))],(GLASS,1.0))
    return finish(M,2.0,1.0)

BRAND=[('halcyon','Halcyon Accord',[('Gannet','House-brand hauler: missile barrage',gannet)]),
       ('varkesh','Varkesh Dominion',[('Bombard','House-brand miner: shell cannon',bombard)]),
       ('ostrova','Ostrova Collective',[('Vesper','House-brand scout: railgun',vesper)]),
       ('wraith','The Wraith trophy',[('Wraith','Conqueror\'s trophy: stealth fighter',wraith)])]
