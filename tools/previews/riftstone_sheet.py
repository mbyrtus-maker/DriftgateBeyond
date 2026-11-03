# Riftstone preview sheet: python3 riftstone_sheet.py OUT.png
import math,sys,os
import numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from render_beyond import render,rgb,FAC_HEX,rot
from beyond_riftstone import riftstone,plain_rock
from PIL import Image,ImageDraw,ImageFont
out=sys.argv[1] if len(sys.argv)>1 else 'beyond_riftstone.png'
class _M:pass
def centred(M):
    T=np.array(M.T);cen=(T.reshape(-1,3).max(0)+T.reshape(-1,3).min(0))/2;N=_M();N.T=list(T-cen);N.R=M.R;return N,T-cen
CW,CH=400,360;W=CW*3;H=110+CH*2+30
bg=Image.new('RGB',(W,H),(7,9,14));g=ImageDraw.Draw(bg)
fb=lambda s:ImageFont.truetype('DejaVuSans-Bold.ttf',s);fr=lambda s:ImageFont.truetype('DejaVuSans.ttf',s)
F=tuple(int(v*255) for v in rgb(FAC_HEX['rift']))
g.text((20,16),'Driftgate Beyond · Riftstone',font=fb(26),fill=F)
g.text((20,52),'A dark, jagged rock split by glowing rifts in its own hot pink (no power uses it), loose shards drifting off it and rift discharges',font=fr(14),fill=(160,168,182))
g.text((20,72),'arcing from the cracks: you can see from a distance that it is unstable. Rare, mostly in deep space; embargoed by most powers.',font=fr(14),fill=(160,168,182))
R,TR=centred(riftstone());P,TP=centred(plain_rock())
views=[('Riftstone · 3/4',R,TR,'rift',math.radians(-30),math.radians(20)),('Riftstone · side',R,TR,'rift',math.radians(-100),math.radians(2)),('Riftstone · from above',R,TR,'rift',math.radians(40),math.radians(70)),
       ('Riftstone · from below',R,TR,'rift',math.radians(160),math.radians(-35)),('Riftstone · close',R,TR,'rift',math.radians(-60),math.radians(10)),('An ordinary asteroid, same size',P,TP,'company',math.radians(-30),math.radians(20))]
for k,(n,N,T,fac,yaw,p) in enumerate(views):
    ext=max(np.abs((T.reshape(-1,3)@rot(yaw,p).T)[:,:2]).max(0)/np.array([CW/2,(CH-30)/2]));z=.85 if 'close' not in n else 1.35
    x0=CW*(k%3);y0=110+CH*(k//3);im=render(N,fac,yaw,p,CW,CH-30,z/ext,zbuf=True);bg.paste(im,(x0,y0+24),im);g.text((x0+14,y0),n,font=fr(13),fill=(130,140,155))
g.text((20,H-24),'Preview only · effects (discharges flickering, the mining-laser ring flickering out, chain blasts) are drawn in code in the game',font=fr(12),fill=(110,118,130))
bg.save(out);print('wrote',out,bg.size)
