# Support craft (constructors and drones) and, with an argument 'brand', the house-brand hulls: python3 support_sheet.py OUT.png [brand]
import math,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from render_beyond import rgb,FAC_HEX
from stations_sheet import fit
from PIL import Image,ImageDraw,ImageFont
out=sys.argv[1];brand=len(sys.argv)>2 and sys.argv[2]=='brand'
if brand:
    from beyond_brand import BRAND as ROWS
    title='Driftgate Beyond · House-brand hulls and the Wraith, centuries on';sub='The Gannet, Bombard and Vesper rebuilt in their factions\' Beyond languages; the Wraith as a conqueror\'s trophy · each scaled to fit'
else:
    from beyond_support import SUPPORT as ROWS
    title='Driftgate Beyond · Support craft: constructors and drones';sub='One of each per faction, in its design language · each scaled to fit (drones are far smaller in game)'
V=[(-36,22),(0,89)]
CW,RH,LW=330,300,220;ncol=max(len(sh) for _,_,sh in ROWS)*2;W=LW+CW*ncol;H=90+RH*len(ROWS)+20
bg=Image.new('RGB',(W,H),(9,12,18));g=ImageDraw.Draw(bg)
for y in range(H):g.line([(0,y),(W,y)],fill=(9+int(6*y/H),12+int(8*y/H),18+int(12*y/H)))
fb=lambda s:ImageFont.truetype('DejaVuSans-Bold.ttf',s);fr=lambda s:ImageFont.truetype('DejaVuSans.ttf',s)
g.text((24,18),title,font=fb(24),fill=(230,232,236));g.text((24,48),sub,font=fr(14),fill=(140,150,165))
for r,(fac,fname,ships) in enumerate(ROWS):
    y0=80+RH*r;F=tuple(int(v*255) for v in rgb(FAC_HEX[fac]))
    g.rectangle([16,y0+8,20,y0+RH-20],fill=F);g.text((32,y0+12),fname.split()[0],font=fb(24),fill=F);g.text((32,y0+44),' '.join(fname.split()[1:]),font=fr(13),fill=(200,204,212))
    for k,(n,c,fn) in enumerate(ships):
        M=fn()
        for j,(yw,pt) in enumerate(V):
            x0=LW+CW*(k*2+j);im=fit(M,math.radians(yw),math.radians(pt),CW-10,RH-60,fac,.86);bg.paste(im,(x0+5,y0+4),im)
        x0=LW+CW*k*2;g.text((x0+14,y0+RH-52),n,font=fb(17),fill=F);g.text((x0+14,y0+RH-28),f'{c} · {len(M.T)} tris · 3/4 and from above',font=fr(12),fill=(120,128,140))
    if r:g.line([(16,y0),(W-16,y0)],fill=(30,36,48))
bg.save(out);print('wrote',out)
