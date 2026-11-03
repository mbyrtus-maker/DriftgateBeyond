# Driftgate Beyond: the assault ship (preview). One shared model for every faction (and your company), painted in its colours,
# until each faction gets its own. A squat armoured dropship: a blunt armoured nose with a slit cockpit, a boxy troop bay with
# a marine door each side and a ramp at the stern, four vectoring thrusters on stub pylons, landing skids, a point-defence gun.
import math
import numpy as np
from beyond_hulls import Mesh,LIGHT,MID,DARK,ACC,GLASS,WIN,loft,box,plate
from beyond_work import finish,abox,lights,tube
def assault():
    M=Mesh(77)
    # troop bay: a chamfered box, wider than tall, with an accent band
    loft(M,[(-.75,[(-.42,-.2),(.42,-.2),(.48,.05),(.36,.3),(-.36,.3),(-.48,.05)]),(.55,[(-.44,-.22),(.44,-.22),(.5,.05),(.38,.32),(-.38,.32),(-.5,.05)])],(MID,.95))
    # armoured nose sloping down to the cockpit
    loft(M,[(.55,[(-.44,-.22),(.44,-.22),(.5,.05),(.38,.32),(-.38,.32),(-.5,.05)]),(1.05,[(-.3,-.18),(.3,-.18),(.34,.0),(.24,.16),(-.24,.16),(-.34,.0)])],(LIGHT,1.0))
    plate(M,[(-.2,.2,.98),(.2,.2,.98),(.28,.3,.68),(-.28,.3,.68)],.02,GLASS,1.0)                                   # slit canopy
    for z in (-.3,.3):loft(M,[(z-.03,[(-.43,-.21),(.43,-.21),(.49,.05),(.37,.31),(-.37,.31),(-.49,.05)]),(z+.03,[(-.43,-.21),(.43,-.21),(.49,.05),(.37,.31),(-.37,.31),(-.49,.05)])],(ACC,.9),cap0=False,cap1=False)
    # marine doors either side, with lights
    for s in (-1,1):
        plate(M,[(s*.495,-.12,-.12),(s*.495,-.12,.18),(s*.495,.2,.18),(s*.495,.2,-.12)],.02,DARK,.7)
        lights(M,[(s*.51,.24,-.14),(s*.51,.24,.2)],.025)
    # stern ramp, lowered a little
    plate(M,[(-.36,-.2,-.75),(.36,-.2,-.75),(.32,-.36,-1.05),(-.32,-.36,-1.05)],.03,DARK,.8)
    plate(M,[(-.36,.28,-.76),(.36,.28,-.76),(.36,-.18,-.76),(-.36,-.18,-.76)],.01,DARK,.35)                          # dark bay mouth
    lights(M,[(-.3,.24,-.8),(.3,.24,-.8)],.03)
    # four vectoring thrusters on stub pylons
    for s in (-1,1):
        for z in (-.5,.35):
            tube(M,[(s*.48,.05,z),(s*.72,.05,z)],[.05,.05],DARK,.85,6)
            loft(M,[(z-.2,[(s*.82+.1*math.cos(a),.05+.1*math.sin(a)) for a in np.linspace(0,2*math.pi,10,endpoint=False)]),(z+.16,[(s*.82+.11*math.cos(a),.05+.11*math.sin(a)) for a in np.linspace(0,2*math.pi,10,endpoint=False)])],(DARK,.8))
            M.vent((s*.82,.05,z-.21),.08)
            loft(M,[(z+.0,[(s*.82+.115*math.cos(a),.05+.115*math.sin(a)) for a in np.linspace(0,2*math.pi,10,endpoint=False)]),(z+.04,[(s*.82+.115*math.cos(a),.05+.115*math.sin(a)) for a in np.linspace(0,2*math.pi,10,endpoint=False)])],(ACC,.9),cap0=False,cap1=False)
    # landing skids
    for s in (-1,1):
        for z in (-.5,.4):tube(M,[(s*.3,-.22,z),(s*.38,-.38,z)],[.025,.025],DARK,.8,5)
        tube(M,[(s*.38,-.38,-.65),(s*.38,-.38,.55)],[.03,.03],DARK,.8,5)
    # a point-defence gun on the roof and an antenna
    abox(M,(0,.36,.25),(.16,.08,.2),DARK,(1,1),.85);tube(M,[(0,.4,.3),(0,.4,.6)],[.02,.018],DARK,.9,5)
    tube(M,[(-.25,.32,-.5),(-.25,.62,-.55)],[.012,.004],DARK,.9,4)
    lights(M,[(-.3,-.12,1.02),(.3,-.12,1.02)],.03)
    return finish(M,1.9,1.0)
