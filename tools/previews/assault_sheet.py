# The assault ship in every faction's colours: python3 assault_sheet.py OUT.png
import math,sys,os
import numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from render_beyond import render,rgb,FAC_HEX,rot
from beyond_assault import assault
from PIL import Image,ImageDraw,ImageFont
out=sys.argv[1] if len(sys.argv)>1 else 'beyond_assault.png'
V=[('3/4 front',math.radians(-36),math.radians(22)),('side',math.radians(-90),0.0),('top',0.0,math.radians(89)),('3/4 rear: the ramp',math.radians(-150),math.radians(18))]
F=[('halcyon','Halcyon Accord'),('varkesh','Varkesh Dominion'),('ostrova','Ostrova Collective'),('company','Your company (amber shown)')]
class _M:pass
CW,RH,LW=280,220,220;W=LW+CW*4;H=96+RH*len(F)+30
bg=Image.new('RGB',(W,H),(9,12,18));g=ImageDraw.Draw(bg)
fb=lambda s:ImageFont.truetype('DejaVuSans-Bold.ttf',s);fr=lambda s:ImageFont.truetype('DejaVuSans.ttf',s)
g.text((20,16),'Driftgate Beyond · the assault ship: one shared model in each faction\'s colours',font=fb(24),fill=(230,232,236))
g.text((20,46),'A squat armoured dropship: blunt nose with a slit cockpit, troop bay with a marine door each side and a ramp astern, four vectoring thrusters, landing skids',font=fr(13),fill=(140,150,165))
for j,(n,_,_) in enumerate(V):g.text((LW+CW*j+10,74),n,font=fr(13),fill=(120,130,145))
M=assault();T=np.array(M.T);cen=(T.reshape(-1,3).max(0)+T.reshape(-1,3).min(0))/2;N=_M();N.T=list(T-cen);N.R=M.R
ext=max(max(np.abs(((T-cen).reshape(-1,3)@rot(yaw,p).T)[:,:2]).max(0)/np.array([CW/2,(RH-20)/2])) for _,yaw,p in V)
for r,(fac,name) in enumerate(F):
    y0=96+RH*r;g.text((20,y0+20),name,font=fb(17),fill=tuple(int(v*255) for v in rgb(FAC_HEX[fac])))
    for j,(_,yaw,p) in enumerate(V):im=render(N,fac,yaw,p,CW,RH-20,.86/ext,zbuf=True);bg.paste(im,(LW+CW*j,y0),im)
    if r:g.line([(16,y0),(W-16,y0)],fill=(30,36,48))
g.text((20,H-24),f'Preview only · {len(M.T)} triangles · Driftgate 1 never drew its assault ships, so this is the first model',font=fr(12),fill=(110,118,130))
bg.save(out);print('wrote',out,bg.size)
