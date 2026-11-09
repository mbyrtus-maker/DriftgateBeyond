# Driftgate Beyond: twelve marks for player companies (8 Nov 2026; the company profile picks one). Same style as the makers'
# logos in beyond_corp.py (a flat glyph of a few pieces in a [-1,1] box, y up here, readable on a 20 px icon) but heraldic
# emblems, so none reads as a maker's or a spare mark. tools/corp_logos_js.py writes them into the game as
# src/js/16zzz_cologos.js (CO_LOGO, in this order: the profile stores the index).
import math
import numpy as np
from beyond_corp import _circ,_bar,_arc,_rot
PI=math.pi
def _star(cx,cy,R,r,n=5,rot=90):
    P=[];a0=math.radians(rot)
    for k in range(2*n):a=a0+k*PI/n;rr=R if k%2==0 else r;P.append((cx+math.cos(a)*rr,cy+math.sin(a)*rr))
    return P
def _sine(y0,amp=.16,t=.17,x0=-.92,x1=.92,per=.92,n=16):
    # a wavy strip as quads
    X=np.linspace(x0,x1,n+1);Y=y0+amp*np.sin((X-x0)/per*2*PI);o=[]
    for i in range(n):o.append([(X[i],Y[i]+t/2),(X[i+1],Y[i+1]+t/2),(X[i+1],Y[i+1]-t/2),(X[i],Y[i]-t/2)])
    return o
def _spiral(turns=2.1,r0=.1,r1=.86,t=.15,n=40):
    o=[];T=np.linspace(0,turns*2*PI,n+1);R=np.linspace(r0,r1,n+1);tt=np.linspace(t*.6,t,n+1)
    for i in range(n):
        a,b=T[i],T[i+1];o.append([(math.cos(a)*(R[i]+tt[i]/2),math.sin(a)*(R[i]+tt[i]/2)),(math.cos(b)*(R[i+1]+tt[i+1]/2),math.sin(b)*(R[i+1]+tt[i+1]/2)),
                                  (math.cos(b)*(R[i+1]-tt[i+1]/2),math.sin(b)*(R[i+1]-tt[i+1]/2)),(math.cos(a)*(R[i]-tt[i]/2),math.sin(a)*(R[i]-tt[i]/2))])
    return o
def _mx(P):return [(-x,y) for x,y in P][::-1]
_HAWK_L=[[(-.08,.3),(-.55,.5),(-.99,.66),(-.9,.44),(-.99,.34),(-.86,.18),(-.93,.06),(-.74,-.06),(-.76,-.18),(-.5,-.16),(-.08,-.22)]]
_HAMMER=[_bar(-.68,-.82,.5,.5,.14),_bar(.33,.74,.76,.31,.3)]
CO_LOGOS=[
 ('crown','a crown',[[(-.75,-.72),(.75,-.72),(.75,-.46),(-.75,-.46)],[(-.75,-.38),(.75,-.38),(.75,-.08),(-.75,-.08)],
   [(-.78,-.1),(-.3,-.1),(-.85,.48)],[(-.3,-.1),(.3,-.1),(0,.62)],[(.3,-.1),(.78,-.1),(.85,.48)],_circ(-.85,.58,.11,10),_circ(0,.74,.12,10),_circ(.85,.58,.11,10)]),
 ('anchor','an anchor',_arc(0,.72,.2,.08,0,360,10)+[_bar(0,.5,0,-.78,.16),_bar(-.44,.3,.44,.3,.13)]+_arc(0,-.14,.72,.16,198,342,10)+
   [[(-.84,-.46),(-.44,-.32),(-.78,-.04)],_mx([(-.84,-.46),(-.44,-.32),(-.78,-.04)])]),
 ('spiral','a spiral',_spiral()),
 ('tower','a watchtower',[[(-.4,-.82),(.4,-.82),(.31,.34),(-.31,.34)],[(-.56,-.97),(.56,-.97),(.56,-.8),(-.56,-.8)],[(-.5,.32),(.5,.32),(.5,.52),(-.5,.52)],
   [(-.5,.5),(-.3,.5),(-.3,.72),(-.5,.72)],[(-.1,.5),(.1,.5),(.1,.72),(-.1,.72)],[(.3,.5),(.5,.5),(.5,.72),(.3,.72)],_bar(0,.7,0,.99,.06),[(0,.99),(.36,.9),(0,.81)]]),
 ('hawk','a hawk with its wings spread',[[(0,.5),(.2,.3),(.17,-.42),(0,-.58),(-.17,-.42),(-.2,.3)],_circ(0,.62,.17,12),[(-.08,.56),(.08,.56),(0,.36)],
   [(-.12,-.5),(.12,-.5),(.32,-.92),(.1,-.84),(0,-.97),(-.1,-.84),(-.32,-.92)]]+_HAWK_L+[_mx(P) for P in _HAWK_L]),
 ('starring','a star in a ring',_arc(0,0,.97,.15,0,360,18)+[_star(0,0,.68,.28)]),
 ('hammers','crossed hammers',_HAMMER+[_mx(P) for P in _HAMMER]),
 ('waves','three waves',_sine(.5)+_sine(0)+_sine(-.5)),
 ('shield','a shield and chevron',[_bar(-.78,.8,.78,.8,.14),_bar(-.78,.86,-.78,.0,.14),_bar(.78,.86,.78,.0,.14),_bar(-.81,.04,.04,-.95,.14),_bar(.81,.04,-.04,-.95,.14),
   _bar(-.5,-.2,.06,.4,.22),_bar(-.06,.4,.5,-.2,.22)]),
 ('trident','a trident',[_bar(0,-.82,0,.6,.14),_bar(-.56,.08,.56,.08,.14),_bar(-.56,.02,-.56,.58,.12),_bar(.56,.02,.56,.58,.12),
   [(-.7,.56),(-.42,.56),(-.56,.9)],[(.42,.56),(.7,.56),(.56,.9)],[(-.15,.56),(.15,.56),(0,.98)],[(0,-.72),(.13,-.85),(0,-.98),(-.13,-.85)]]),
 ('hourglass','an hourglass',[[(-.62,.97),(.62,.97),(.62,.8),(-.62,.8)],[(-.62,-.97),(.62,-.97),(.62,-.8),(-.62,-.8)],_bar(-.66,.82,-.66,-.82,.08),_bar(.66,.82,.66,-.82,.08),
   [(-.48,.72),(.48,.72),(.06,.05),(-.06,.05)],[(-.4,-.72),(.4,-.72),(.06,-.12),(-.06,-.12)]]),
 ('fox','a fox\'s head',[[(-.86,.42),(.86,.42),(.36,-.2),(0,-.86),(-.36,-.2)],[(-.86,.4),(-.6,.95),(-.28,.4)],[(.28,.4),(.6,.95),(.86,.4)],[(-.98,.1),(-.6,.42),(-.86,.42)],[(.98,.1),(.86,.42),(.6,.42)]])]
CO_LOGO_POLYS={k:p for k,_,p in CO_LOGOS}
