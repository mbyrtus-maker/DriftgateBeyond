# Preview of Scrapheart Haven, the Unbound's main station: python3 unbound_base_sheet.py OUT.png
import math,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from render_beyond import rgb,FAC_HEX
from stations_sheet import fit
from beyond_unbound_base import scrapheart
from PIL import Image,ImageDraw,ImageFont
out=sys.argv[1] if len(sys.argv)>1 else 'beyond_unbound_haven.png'
M=scrapheart();print(len(M.T))
W,H=1700,1080;bg=Image.new('RGB',(W,H),(9,12,18));g=ImageDraw.Draw(bg)
for y in range(H):g.line([(0,y),(W,y)],fill=(9+int(6*y/H),12+int(8*y/H),18+int(12*y/H)))
fb=lambda s:ImageFont.truetype('DejaVuSans-Bold.ttf',s);fr=lambda s:ImageFont.truetype('DejaVuSans.ttf',s);F=tuple(int(v*255) for v in rgb(FAC_HEX['pirate']))
g.text((24,18),'Driftgate Beyond · Scrapheart Haven, the Unbound\'s main station',font=fb(24),fill=(230,232,236))
g.text((24,48),'A unique asteroid base built from pieces of every other station: Halcyon, Varkesh, Ostrova, the freeport and the player bases',font=fr(14),fill=(140,150,165))
bg.paste(im:=fit(M,math.radians(-35),math.radians(22),1000,640,'pirate',.9),(10,80),im)
bg.paste(im:=fit(M,math.radians(145),math.radians(18),660,640,'pirate',.9),(1020,80),im)
bg.paste(im:=fit(M,0.0,math.radians(89),520,330,'pirate',.9),(30,730),im)
bg.paste(im:=fit(M,math.radians(-90),0.0,520,330,'pirate',.9),(580,730),im)
for x,t in ((30,'from above'),(580,'from the side'),(1020,'from behind'),(10,'3/4 front')):g.text((x+10,(730 if x in (30,580) else 80)),t,font=fr(13),fill=(120,130,145))
notes=['Halcyon: a lens disc, glass crown, spire, dish and swept arm, rammed tilted into the crown','Varkesh: a triangular spire rammed into a flank, three talons clutching the rock, turrets',
       'Ostrova: crystal spires out of the other flank, a halo floating over them, energy bridges, a floating spire section','Freeport: a broken promenade ring round the base and a docking arm with berths',
       'Player bases: a shipyard gantry, a container stash, tanks, hangars cut into the rock','Unbound: weld seams, strings of lights between the pieces, a beacon mast, lit windows']
for i,t in enumerate(notes):g.text((1130,760+i*36),'· '+t if len(t)<62 else '· '+t[:t.rfind(' ',0,62)]+'\n   '+t[t.rfind(' ',0,62)+1:],font=fr(12),fill=(170,176,188))
g.text((1130,730),f'Scrapheart Haven · {len(M.T)} tris',font=fb(15),fill=F)
g.text((24,H-24),'Preview only: not in the game yet. The name is Driftgate 1\'s Unbound haven.',font=fr(12),fill=(110,118,130))
bg.save(out);print('wrote',out)
