# The Ravager in every capital role (hangar and boarding pinnaces), five views: python3 ravager_sheet.py OUT.png
import math,sys,os
import numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from render_beyond import render,rgb,FAC_HEX,rot
from beyond_unbound import ravager
from PIL import Image,ImageDraw,ImageFont
out=sys.argv[1] if len(sys.argv)>1 else 'beyond_ravager.png'
V=[('3/4 front',math.radians(-36),math.radians(22)),('side',math.radians(-90),0.0),('top',0.0,math.radians(89)),('3/4 rear: the boarding pinnaces',math.radians(-145),math.radians(20)),('3/4 below: the hangar, bay doors open',math.radians(-40),math.radians(-30)),('below, from astern',math.radians(-150),math.radians(-28))]
class _M:pass
CW,CH=620,330;W=CW*2;H=110+CH*3+40
bg=Image.new('RGB',(W,H),(9,12,18));g=ImageDraw.Draw(bg)
for y in range(H):g.line([(0,y),(W,y)],fill=(9+int(6*y/H),12+int(8*y/H),18+int(12*y/H)))
fb=lambda s:ImageFont.truetype('DejaVuSans-Bold.ttf',s);fr=lambda s:ImageFont.truetype('DejaVuSans.ttf',s)
F=tuple(int(v*255) for v in rgb(FAC_HEX['pirate']))
g.text((20,16),'Driftgate Beyond · the Ravager fills every Unbound capital role',font=fb(24),fill=F)
g.text((20,48),'Escort and line ship as approved, plus a Varkesh hangar keel with open bay doors under the midsection (its small plundered wing)',font=fr(14),fill=(160,168,182))
g.text((20,68),'and two boarding pinnaces clamped to the Ostrova stern: Varkesh wedges, Halcyon canopies, grapple claws forward',font=fr(14),fill=(160,168,182))
M=ravager();T=np.array(M.T);cen=(T.reshape(-1,3).max(0)+T.reshape(-1,3).min(0))/2;N=_M();N.T=list(T-cen);N.R=M.R
for k,(n,yaw,p) in enumerate(V):
    ext=max(np.abs(((T-cen).reshape(-1,3)@rot(yaw,p).T)[:,:2]).max(0)/np.array([CW/2,(CH-30)/2]))
    x0=CW*(k%2);y0=110+CH*(k//2);im=render(N,'pirate',yaw,p,CW,CH-30,.92/ext,zbuf=True);bg.paste(im,(x0,y0+24),im);g.text((x0+14,y0),n,font=fr(13),fill=(130,140,155))
g.text((20,H-26),f'Preview only · {len(M.T)} triangles · names are placeholders',font=fr(12),fill=(110,118,130))
bg.save(out);print('wrote',out,bg.size)
