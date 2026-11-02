# Driftgate Beyond: the house-brand hulls and the Wraith, centuries on from Driftgate 1 (preview, not in the model pack yet). First pass.
# Driftgate 1's Gannet, Bombard and Vesper were conversions of a stock hull; in Beyond each is its own design in its faction's
# language, built around the weapon that made its name. The Wraith, a conqueror's trophy, belongs to no faction: a faceted stealth wing.
import math
import numpy as np
from beyond_hulls import Mesh,LIGHT,MID,DARK,ACC,GLASS,GLOW,WIN,loft,box,plate,ring,LENS,HEX,lens_role
from beyond_work import finish,abox,crystal,lights,sqdrive
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
    # Halcyon: a gull-winged lens flying wing; the inner wings are banks of missile launch cells (the barrage), a slim freight spine
    # between them, a glass canopy, twin tails, wingtip emitters
    M=Mesh(701)
    loft(M,[(-1.15,LENS(.18,.14)),(-.6,LENS(.3,.2)),(.6,LENS(.28,.19)),(1.05,LENS(.12,.08)),(1.2,LENS(.03,.03))],lens_role)
    M.blob((0,.17,.62),.15,GLASS,sub=2,squash=(1,.7,1.6),noise=0)
    for sx in (1,-1):
        plate(M,[(sx*.25,.0,.55),(sx*.85,.12,.05),(sx*.85,.12,-.75),(sx*.25,0,-.75)],.09,LIGHT,1.0)                 # inner wing, kinked up
        plate(M,[(sx*.85,.12,.05),(sx*1.55,-.08,-.45),(sx*1.55,-.08,-.75),(sx*.85,.12,-.75)],.05,LIGHT,1.0)          # outer wing, kinked down
        cells(M,sx*.3,sx*.82,-.68,.0,.055,3,4,.14) if sx>0 else cells(M,sx*.82,sx*.3,-.68,.0,.055,3,4,.14)
        M.blob((sx*1.55,-.08,-.6),.05,WIN,sub=1,noise=0)
        plate(M,[(sx*.18,.1,-.7),(sx*.32,.5,-1.05),(sx*.32,.5,-1.25),(sx*.18,.1,-1.15)],.03,LIGHT,.95)               # twin tails
        M.vent((sx*.11,0,-1.16),.07)
    tube(M,[(0,.22,-.1),(0,.22,-.6)],[.07,.07],ACC,.95,8)                                                             # freight spine hatch
    lights(M,[(.15,-.08,1.0),(-.15,-.08,1.0)],.03)
    return finish(M,2.8,1.0)
def bombard():
    # Varkesh: a heavy armoured hex hull built round one huge shell cannon on the centreline (a long barrel with a muzzle brake, a big
    # breech block), ore hoppers cut down to two, Ward Drones docked in its flanks, exhaust stacks and a square drive block
    M=Mesh(702)
    loft(M,[(-1.3,SMH(.5,.32)),(.5,SMH(.55,.34)),(1.0,SMH(.36,.24,-.03)),(1.2,SMH(.14,.08,-.05))],smh_role)
    M.blob((.0,.3,.55),.14,GLASS,sub=2,squash=(1,.6,1.4),noise=0)
    abox(M,(0,.36,-.35),(.5,.26,.7),DARK,(.9,.9),.8)                                                                 # breech block
    tube(M,[(0,.4,0),(0,.4,.3),(0,.4,1.7)],[.13,.1,.085],DARK,1.0,10,cap0=False,cap1=False)                           # the shell cannon
    for z in (.3,.9):ring(M,(0,.4,z),.11,.02,ACC,seg=14,sides=4)
    tube(M,[(0,.4,1.65),(0,.4,1.95)],[.12,.12],MID,.95,8,cap1=False)
    for z in (1.73,1.83):ring(M,(0,.4,z),.125,.015,DARK,seg=12,sides=4)
    for sx in (1,-1):
        abox(M,(sx*.48,-.05,-.55),(.26,.28,.55),MID,(.9,.9))                                                           # hoppers
        box(M,(sx*.57,-.02,.2),(.12,.16,.22),DARK,sh=.8);box(M,(sx*.62,-.02,.2),(.1,.12,.18),MID)                      # docked Ward Drone
    stacks(M,(0,.3,-.95),2,.34,.3)
    box(M,(0,0,-1.42),(.8,.5,.26),DARK,sh=.8)
    for x in (-.2,.2):
        for y in (-.12,.12):M.vent((x,y,-1.56),.09)
    lights(M,[(.22,-.12,1.1),(-.22,-.12,1.1)],.03)
    return finish(M,3.0,1.0)
def vesper():
    # Ostrova: a slender faceted spire that is itself a railgun: two long crystal rails reach forward from the hull with three
    # accelerator halos along them and a glowing slug between, a scout radome set low on the spine, spire drives
    M=Mesh(703)
    loft(M,[(-1.25,OCT(.1,.1)),(-.8,OCT(.2,.19)),(.3,OCT(.19,.18)),(.6,OCT(.1,.1)),(.7,OCT(.03,.03))],oct_role)
    M.blob((0,.16,.25),.09,GLASS,sub=2,squash=(1,.7,1.8),noise=0)
    for sx in (1,-1):
        crystal(M,.0,2.0,.07,.07,sx*.17,0)                                                                            # the rails
        tube(M,[(sx*.08,0,.1),(sx*.17,0,.1)],[.03,.03],LIGHT,.9,5)
    for z in (.7,1.15,1.6):ring(M,(0,0,z),.26,.03,ACC,seg=24,sides=5);ring(M,(0,0,z),.25,.012,WIN,seg=24,sides=4)       # accelerator halos
    crystal(M,1.0,1.45,.05,.05,0,0);M.blob((0,0,1.22),.07,GLOW,sub=1,noise=0)                                        # the slug
    dish(M,(0,.2,-.35),.16)
    for sx in (1,-1):loft(M,[(-1.0,[(a+sx*.24,b) for a,b in OCT(.05,.05)]),(-.45,[(a+sx*.24,b) for a,b in OCT(.06,.06)]),(-.25,[(a+sx*.2,b) for a,b in OCT(.02,.02)])],oct_role)
    for k in range(3):a=PI/2+k*2*PI/3;M.vent((math.cos(a)*.06,math.sin(a)*.06,-1.26),.04)
    return finish(M,2.7,1.0)
def wraith():
    # the Wraith: a faceted stealth flying wing, all hard angles and flat planes, a sawtooth trailing edge, its drives buried in slit
    # vents, two heavy guns hidden in the leading edge, a faceted canopy, faint edge lights
    M=Mesh(704)
    # faceted body: diamond sections, flat and sharp
    D=lambda w,h,dy=0:[(w,dy),(w*.35,h+dy),(-w*.35,h+dy),(-w,dy),(-w*.35,-h*.6+dy),(w*.35,-h*.6+dy)]
    loft(M,[(-.9,D(.4,.06)),(-.3,D(.5,.13)),(.5,D(.32,.11)),(1.05,D(.04,.02))],lambda i,j:([LIGHT,MID,MID,LIGHT,DARK,DARK][j],[1,.95,.9,1,.8,.8][j]))
    for sx in (1,-1):
        plate(M,[(sx*.45,0,.25),(sx*1.25,-.02,-.65),(sx*1.1,-.02,-.85),(sx*.75,-.02,-.62),(sx*.55,-.01,-.88),(sx*.4,0,-.7)],.04,MID,.9)   # wing, sawtooth trailing edge
        tube(M,[(sx*.45,0,.27),(sx*1.25,-.02,-.63)],[.012,.012],GLOW,1.0,4,cap0=False,cap1=False)                                   # faint edge light
        tube(M,[(sx*.32,-.03,.35),(sx*.32,-.03,.62)],[.025,.02],DARK,1.0,6)                                                        # hidden guns
        plate(M,[(sx*.1,-.02,-.88),(sx*.32,-.02,-.86),(sx*.32,-.02,-.9),(sx*.1,-.02,-.92)],.01,GLOW,1.0)                            # slit vents
    loft(M,[(.15,D(.12,.04,.11)),(.45,D(.1,.06,.1)),(.65,D(.03,.02,.08))],(GLASS,1.0))
    return finish(M,2.0,1.0)

BRAND=[('halcyon','Halcyon Accord',[('Gannet','House-brand hauler: missile barrage',gannet)]),
       ('varkesh','Varkesh Dominion',[('Bombard','House-brand miner: shell cannon',bombard)]),
       ('ostrova','Ostrova Collective',[('Vesper','House-brand scout: railgun',vesper)]),
       ('wraith','The Wraith trophy',[('Wraith','Conqueror\'s trophy: stealth fighter',wraith)])]
