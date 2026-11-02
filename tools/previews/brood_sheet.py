# Preview of the Brood destroyer (the Gullet), four views, with the Brood escort and carrier beside it: python3 brood_sheet.py OUT.png
import math,sys,os
import numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from render_beyond import rgb,FAC_HEX
from stations_sheet import fit
from beyond_brood import gullet
import brood
from PIL import Image,ImageDraw,ImageFont
class W_:
    def __init__(s,o):s.T,s.R=list(o[0]),list(o[2])
out=sys.argv[1] if len(sys.argv)>1 else 'beyond_brood_destroyer.png'
G=gullet();print(len(G.T))
W,H=1640,880;bg=Image.new('RGB',(W,H),(9,12,18));g=ImageDraw.Draw(bg)
for y in range(H):g.line([(0,y),(W,y)],fill=(9+int(6*y/H),12+int(8*y/H),18+int(12*y/H)))
fb=lambda s:ImageFont.truetype('DejaVuSans-Bold.ttf',s);fr=lambda s:ImageFont.truetype('DejaVuSans.ttf',s);F=tuple(int(v*255) for v in rgb(FAC_HEX['brood']))
g.text((24,18),'Driftgate Beyond · The Brood destroyer: the Gullet (placeholder name)',font=fb(24),fill=(230,232,236))
g.text((24,48),'No shields. Its maw cannon charges, then fires a beam out of its open maw that does incredible damage along the whole firing path.',font=fr(14),fill=(140,150,165))
V=[('3/4 front',-36,22),('side',-90,0),('top',0,89),('head on',-12,8)]
for j,(n,yw,pt) in enumerate(V):
    im=fit(G,math.radians(yw),math.radians(pt),390,360,'brood',.88);bg.paste(im,(20+400*j,90),im);g.text((30+400*j,80),n,font=fr(13),fill=(120,130,145))
g.line([(16,470),(W-16,470)],fill=(30,36,48));g.text((24,482),'The Brood capital line, each scaled to fit:',font=fr(13),fill=(130,140,155))
for j,(n,c,M) in enumerate((('Prowler','escort (Driftgate 1)',W_(brood.prowler())),('Gullet','destroyer (new)',G),('Hive Ship','carrier (Driftgate 1)',W_(brood.hive())))):
    im=fit(M,math.radians(-36),math.radians(22),500,320,'brood',.85);bg.paste(im,(30+530*j,505),im)
    g.text((40+530*j,820),n,font=fb(17),fill=F);g.text((40+530*j,845),f'{c} · {len(M.T)} tris',font=fr(12),fill=(120,128,140))
bg.save(out);print('wrote',out)
