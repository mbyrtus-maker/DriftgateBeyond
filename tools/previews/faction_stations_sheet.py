# Preview sheet of the faction stations, faction depots and the freeport: python3 faction_stations_sheet.py OUT.png
import math,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from render_beyond import rgb,FAC_HEX
from stations_sheet import fit
from beyond_faction_stations import FACTION_STATIONS,freeport
from PIL import Image,ImageDraw,ImageFont
out=sys.argv[1] if len(sys.argv)>1 else 'beyond_faction_stations.png'
YAW,PIT=math.radians(-35),math.radians(24)
LW,HD,RH=200,74,420;C=[(660,'Station'),(330,'Station from above'),(470,'Depot')]
W=LW+sum(c for c,_ in C);rows=FACTION_STATIONS+[('freeport','Freeport Compact',freeport,None)];H=HD+RH*len(rows)+30
bg=Image.new('RGB',(W,H),(9,12,18));g=ImageDraw.Draw(bg)
for y in range(H):g.line([(0,y),(W,y)],fill=(9+int(6*y/H),12+int(8*y/H),18+int(12*y/H)))
fb=lambda s:ImageFont.truetype('DejaVuSans-Bold.ttf',s);fr=lambda s:ImageFont.truetype('DejaVuSans.ttf',s)
g.text((24,18),'Driftgate Beyond · Faction stations and depots, and the freeport',font=fb(24),fill=(230,232,236))
g.text((24,48),'Generated in code · each faction in its ships\' design language, the freeport a welcoming trade spindle · each picture scaled to fit',font=fr(14),fill=(140,150,165))
x=LW
for cw,t in C:g.text((x+14,HD-4),t,font=fr(14),fill=(130,140,155));x+=cw
for r,(fac,fname,st,dp) in enumerate(rows):
    y0=HD+RH*r+14;F=tuple(int(v*255) for v in rgb(FAC_HEX[fac]))
    g.rectangle([16,y0+8,20,y0+RH-24],fill=F);g.text((32,y0+12),fname.split()[0],font=fb(26),fill=F);g.text((32,y0+46),' '.join(fname.split()[1:]),font=fr(14),fill=(200,204,212))
    M=st();x=LW
    for (cw,t),(yaw,pit) in zip(C[:2],((YAW,PIT),(0.0,math.radians(89)))):
        im=fit(M,yaw,pit,cw-20,RH-40,fac);bg.paste(im,(x+10,y0),im);x+=cw
    g.text((32,y0+RH-48),f'Station · {len(M.T)} tris',font=fr(12),fill=(120,128,140))
    if dp:
        D=dp();im=fit(D,YAW,PIT,C[2][0]-20,RH-40,fac,.7);bg.paste(im,(x+10,y0),im);g.text((x+14,y0+RH-48),f'Depot · {len(D.T)} tris',font=fr(12),fill=(120,128,140))
    else:g.text((x+14,y0+RH/2-20),'Freeports are trade hubs:\nno depots of their own.',font=fr(14),fill=(120,128,140))
    print(fname,len(M.T))
    if r:g.line([(16,y0-6),(W-16,y0-6)],fill=(30,36,48))
g.text((24,H-24),'Preview only: not in the game yet. Pictures are scaled to fit their cells; in the game a depot is much smaller than a station.',font=fr(12),fill=(110,118,130))
bg.save(out);print('wrote',out,bg.size)
