# Driftgate Beyond: miners and haulers (preview, not in the model pack yet).
# Baseline: Driftgate 1's work ships, built from the Kenney Space Kit (tools/kits): miners keep the craft_miner hull with its
# forward drills (turned about as in Driftgate 1), haulers keep the craft_cargoA / craft_cargoB cargo hulls. Each faction then
# dresses them in its own kit parts and adds its design language, and each size has its own silhouette:
#   Halcyon: streamlined pods and cones, glass domes, swept fins, emitter nodes
#   Varkesh: generators, turrets, guns, container stacks, armour plates, square drives
#   Ostrova: dishes, antennas, halos, crystal cargo
import math
import numpy as np
from beyond_hulls import Mesh,LIGHT,MID,DARK,ACC,GLASS,GLOW,WIN,loft,box,plate,barrel,ring
from d1kit import part,place
PI=math.pi;UP=-PI/2   # tilt UP lays a kit rocket part along +z (its top pointing forward); -UP points it back

def kit(M,parts):place(M,part(parts))
def finish(M,length):
    # normalise to nose +z, the given length, centred
    P=np.array(M.T,float);lo=P.reshape(-1,3).min(0);hi=P.reshape(-1,3).max(0);c=(lo+hi)/2;k=length/(hi[2]-lo[2])
    M.T=list((P-c)*k);return M
MINER=('craft_miner',(0,0,0),PI,1)   # Driftgate 1's miner hull, drills forward

# ============================================================== HALCYON
def wren():      # light miner: the miner hull under a glass dome, a smooth cowl and swept fins
    M=Mesh(51)
    kit(M,[MINER,('hangar_roundGlass',(0,.62,-.2),0,.22),('rocket_topA',(0,.35,-1.25),0,.55,False,-UP),('rocket_finsA',(0,.1,-1.35),0,.7,False,-UP)])
    for sx in (1,-1):M.blob((sx*.95,.35,-.5),.08,WIN,sub=1,noise=0)
    return finish(M,2.0)
def plover():    # medium miner: the miner hull with two streamlined ore pods on outriggers
    M=Mesh(52)
    kit(M,[MINER,('hangar_roundGlass',(0,.62,-.1),0,.24),('rocket_finsA',(0,.1,-1.4),0,.8,False,-UP)])
    for sx in (1,-1):
        kit(M,[('rocket_fuelA',(sx*1.45,.15,z),0,.75,False,UP) for z in (-.55,.0)]+[('rocket_topA',(sx*1.45,.15,.38),0,.75,False,UP),('rocket_topA',(sx*1.45,.15,-.95),0,.75,False,-UP)])
        plate(M,[(sx*.85,.3,.2),(sx*1.2,.35,.15),(sx*1.2,.35,-.6),(sx*.85,.3,-.55)],.05,LIGHT)                       # outrigger
        M.blob((sx*1.45,.55,-.3),.07,WIN,sub=1,noise=0)
    return finish(M,2.5)
def heron():     # heavy miner: the miner hull at the head of a long streamlined body with a tall tail and a big glass bridge
    M=Mesh(53)
    kit(M,[('craft_miner',(0,0,1.1),PI,1.15),('hangar_roundGlass',(0,.55,-.35),0,.42)]
          +[('rocket_fuelA',(0,.35,z),0,1.15,False,-UP) for z in (-.3,-.85,-1.4)]+[('rocket_finsA',(0,.35,-2.05),0,1.25,False,-UP)])
    for sx in (1,-1):
        kit(M,[('rocket_sidesA',(sx*.9,.2,-.9),0,.7,False,-UP)])
        plate(M,[(sx*.5,.3,-.5),(sx*1.3,.25,-1.3),(sx*1.25,.25,-1.55),(sx*.5,.3,-1.4)],.05,LIGHT)
        M.blob((sx*1.28,.25,-1.42),.08,WIN,sub=1,noise=0)
    return finish(M,3.2)
def tern():      # light hauler: the small cargo hull with a pointed cowl and a forked tail
    M=Mesh(54)
    kit(M,[('craft_cargoA',(0,0,0),0,1),('hangar_roundGlass',(0,.8,.7),0,.2),('rocket_topA',(0,.4,-1.3),0,.6,False,-UP)])
    for sx in (1,-1):plate(M,[(sx*.4,.6,-.9),(sx*.95,.9,-1.6),(sx*.8,.9,-1.6),(sx*.3,.6,-1.25)],.04,ACC)
    return finish(M,2.0)
def albatross(): # medium hauler: the big cargo hull with two long cargo pods slung beneath and fins
    M=Mesh(55)
    kit(M,[('craft_cargoB',(0,0,0),0,1),('hangar_roundGlass',(0,.9,.75),0,.24),('rocket_finsA',(0,.4,-1.45),0,.85,False,-UP)])
    for sx in (1,-1):
        kit(M,[('rocket_fuelA',(sx*.85,-.35,z),0,.6,False,UP) for z in (-.6,-.15,.3)]+[('rocket_topA',(sx*.85,-.35,.62),0,.6,False,UP),('rocket_topA',(sx*.85,-.35,-.92),0,.6,False,-UP)])
        plate(M,[(sx*.7,.1,.5),(sx*.85,-.1,.5),(sx*.85,-.1,-.6),(sx*.7,.1,-.6)],.04,MID)
    return finish(M,2.7)
def pelican():   # heavy hauler: the big cargo hull riding on a huge glass-domed cargo pouch, four drives
    M=Mesh(56)
    kit(M,[('craft_cargoB',(0,.35,0),0,1.15),('hangar_roundGlass',(0,.3,-.1),0,.62,True),('hangar_roundGlass',(0,1.3,.9),0,.24),
           ('rocket_finsA',(0,.75,-1.55),0,1.0,False,-UP)])
    for sx in (1,-1):
        for dx in (.45,1.05):kit(M,[('rocket_topA',(sx*dx,.25,-1.55),0,.42,False,-UP)])
        M.blob((sx*1.0,-.1,-.1),.09,WIN,sub=1,noise=0)
    return finish(M,3.3)

# ============================================================== VARKESH
def pick():      # light miner: the miner hull with a generator on its back and twin guns
    M=Mesh(61)
    kit(M,[MINER,('machine_generator',(0,.68,-.3),0,1.1),('weapon_gun',(.5,.68,.5),0,1.6),('weapon_gun',(-.5,.68,.5),0,1.6)])
    box(M,(0,.3,-1.4),(.9,.4,.2),DARK);M.vent((.25,.3,-1.52),.12);M.vent((-.25,.3,-1.52),.12)
    return finish(M,2.0)
def gouge():     # medium miner: the miner hull between two big ore drums, a turret on top, an armoured scoop
    M=Mesh(62)
    kit(M,[MINER,('turret_single',(0,.68,-.2),0,.9)])
    for sx in (1,-1):
        kit(M,[('machine_barrelLarge',(sx*1.25,.0,z),0,1.1) for z in (-.55,.25)])
        box(M,(sx*1.0,.35,-.15),(.25,.12,.9),DARK)
    plate(M,[(-.95,-.02,.6),(.95,-.02,.6),(1.05,-.06,1.35),(-1.05,-.06,1.35)],.08,ACC)                              # scoop floor under the drills
    for sx in (1,-1):plate(M,[(sx*.98,-.02,.6),(sx*1.08,-.06,1.35),(sx*1.08,.35,1.3),(sx*.98,.35,.6)],.06,DARK)        # scoop walls
    box(M,(0,.3,-1.45),(1.0,.45,.2),DARK);[M.vent((x,.3,-1.57),.12) for x in (-.3,.3)]
    return finish(M,2.6)
def sledge():    # heavy miner: two miner hulls side by side under a heavy frame, a double turret, a big generator aft
    M=Mesh(63)
    kit(M,[('craft_miner',(1.0,0,.3),PI,1),('craft_miner',(-1.0,0,.3),PI,1),('machine_generatorLarge',(0,.55,-1.2),0,1.2),
           ('turret_double',(0,1.05,.0),0,1.1)])
    box(M,(0,.75,.0),(2.2,.12,1.4),MID);box(M,(0,.75,.7),(2.25,.14,.1),ACC)                                         # the frame across both hulls
    for sx in (1,-1):box(M,(sx*.95,.4,-1.6),(.6,.45,.25),DARK);M.vent((sx*.95,.4,-1.74),.15)
    return finish(M,3.2)
def runner():    # light hauler: the small cargo hull carrying one container box
    M=Mesh(64)
    kit(M,[('craft_cargoA',(0,0,0),0,1),('monorail_trainBox',(0,.8,-.3),0,1.2),('weapon_gun',(0,.55,1.1),0,1.6)])
    box(M,(0,.4,-1.35),(.9,.45,.2),DARK);[M.vent((x,.4,-1.47),.12) for x in (-.25,.25)]
    return finish(M,2.0)
def bulwark():   # medium hauler: the big cargo hull stacked with two rows of containers and a double turret
    M=Mesh(65)
    kit(M,[('craft_cargoB',(0,0,0),0,1),('turret_double',(0,.9,.85),0,.8)]+[('monorail_trainBox',(x,.9,z),0,1) for x in (-.3,.3) for z in (-.8,.0)])
    for sx in (1,-1):box(M,(sx*.82,.5,-.35),(.1,.75,1.6),MID)                                                      # armour plates on the sides
    box(M,(0,.45,-1.4),(1.2,.5,.2),DARK);[M.vent((x,.45,-1.52),.13) for x in (-.35,.35)]
    return finish(M,2.6)
def rampart():   # heavy hauler: a cargo-hull tug pulling a train of armoured cargo cars, turrets along it
    M=Mesh(66)
    kit(M,[('craft_cargoB',(0,0,1.75),0,1),('turret_single',(0,.9,1.55),0,.8)])
    for k,z in enumerate((-.0,-1.3,-2.6)):                                                                         # a train of armoured cargo cars
        box(M,(0,.45,z),(1.35,.8,1.1),MID);box(M,(0,.86,z),(1.4,.06,1.12),ACC,sh=.9)
        for sx in (1,-1):box(M,(sx*.7,.45,z),(.06,.7,.9),DARK)
        for x in (-.35,.35):box(M,(x,.92,z),(.5,.08,.9),DARK,sh=.95)
        box(M,(0,.4,z+.65),(.3,.2,.2),DARK)                                                                          # coupling
    for z in (-1.3,):kit(M,[('turret_single',(0,.9,z),0,.6)])
    box(M,(0,.45,-3.25),(1.0,.5,.2),DARK);[M.vent((x,.45,-3.37),.12) for x in (-.3,.3)]
    return finish(M,3.4)

# ============================================================== OSTROVA
def glim():      # light miner: the miner hull with a dish and a crystal cluster on its back
    M=Mesh(71)
    kit(M,[MINER,('satelliteDish',(0,.68,-.6),0,1.1),('rock_crystals',(0,.68,.35),0,.9),('machine_wireless',(.55,.68,-.2),0,.7)])
    return finish(M,2.0)
def lumen():     # medium miner: the miner hull inside a halo, antennas forward, crystal ore aft
    M=Mesh(72)
    kit(M,[MINER,('rock_crystalsLargeA',(0,.68,-.6),0,1.0),('satelliteDish',(0,.68,.35),0,.9)]+[('machine_wireless',(sx*.65,.68,.6),0,.7) for sx in (1,-1)])
    ring(M,(0,.35,-.1),1.35,.06,ACC,seg=36,sides=6)
    for k in range(4):a=k*PI/2+PI/4;M.blob((math.cos(a)*1.35,.35+math.sin(a)*1.35,-.1),.1,GLASS,sub=1,noise=0)
    return finish(M,2.6)
def delve():     # heavy miner: the miner hull pushing a long sensor spire, two halos, a great crystal cargo
    M=Mesh(73)
    kit(M,[('craft_miner',(0,0,.6),PI,1.15),('rock_crystalsLargeA',(0,.75,-.9),0,1.5),('rock_crystalsLargeB',(0,.75,-.1),0,1.2),
           ('satelliteDish_large',(0,.8,1.0),0,.7)])
    for z in (-.4,-1.2):ring(M,(0,.45,z),1.25,.055,ACC,seg=36,sides=6)
    M.tube([(0,.45,-1.6),(0,.45,-2.4)],[.12,.03],6,lambda i,j,n,p:(LIGHT,.95))                                        # aft spire
    for z,r in ((-1.9,.25),(-2.15,.17)):ring(M,(0,.45,z),r,.03,ACC,seg=16,sides=5)
    return finish(M,3.2)
def drift():     # light hauler: the small cargo hull with a halo and an antenna mast
    M=Mesh(74)
    kit(M,[('craft_cargoA',(0,0,0),0,1),('machine_wireless',(0,.8,-.6),0,.9),('satelliteDish',(0,.8,.5),0,.8)])
    ring(M,(0,.4,-.2),1.15,.05,ACC,seg=32,sides=6)
    return finish(M,2.0)
def cairn():     # medium hauler: the big cargo hull carrying a stacked cairn of crystal cargo, a halo round it
    M=Mesh(75)
    kit(M,[('craft_cargoB',(0,0,0),0,1),('rock_crystalsLargeA',(0,.9,-.5),0,1.1),('rock_crystalsLargeB',(0,1.35,-.5),0,.8),
           ('rock_crystals',(0,.9,.35),0,.9),('machine_wireless',(0,.9,1.0),0,.7)])
    ring(M,(0,1.15,-.5),.75,.05,ACC,seg=30,sides=6,axis='y')
    return finish(M,2.6)
def monolith():  # heavy hauler: the big cargo hull carrying a tall crystal-veined slab, two upright halos
    M=Mesh(76)
    kit(M,[('craft_cargoB',(0,0,0),0,1.2),('satelliteDish_large',(0,1.05,1.15),0,.55)])
    box(M,(0,1.85,-.4),(.55,1.7,1.7),MID,taper=(.8,.7))                                                           # the slab
    for sx in (1,-1):
        for k in range(3):plate(M,[(sx*.28,1.2+k*.35,.35),(sx*.28,1.45+k*.35,.35),(sx*.25,1.35+k*.35,-1.1),(sx*.25,1.1+k*.35,-1.1)],.01,WIN,.85)
    for z in (.2,-1.0):
        pts=[np.array([0,1.2,z])+[math.cos(a)*1.25,math.sin(a)*1.25,0] for a in np.linspace(0,2*PI,33)]
        M.tube(pts,[.05]*len(pts),6,lambda i,j,n,p:(ACC,1.0),cap0=False,cap1=False)
    return finish(M,3.3)

WORK=[('halcyon','Halcyon Accord',[('Wren','Light miner',wren),('Plover','Medium miner',plover),('Heron','Heavy miner',heron),('Tern','Light hauler',tern),('Albatross','Medium hauler',albatross),('Pelican','Heavy hauler',pelican)]),
      ('varkesh','Varkesh Dominion',[('Pick','Light miner',pick),('Gouge','Medium miner',gouge),('Sledge','Heavy miner',sledge),('Runner','Light hauler',runner),('Bulwark','Medium hauler',bulwark),('Rampart','Heavy hauler',rampart)]),
      ('ostrova','Ostrova Collective',[('Glim','Light miner',glim),('Lumen','Medium miner',lumen),('Delve','Heavy miner',delve),('Drift','Light hauler',drift),('Cairn','Medium hauler',cairn),('Monolith','Heavy hauler',monolith)])]
