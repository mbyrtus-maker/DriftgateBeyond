# Four-view close-up sheet of the Beyond capital ships: python3 capitals_closeup.py
import math,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from render_beyond import render,rgb,FAC_HEX
from beyond_capitals import CAPITALS
from PIL import Image,ImageDraw,ImageFont
V=[('3/4 front',math.radians(-36),math.radians(22)),('side',math.radians(-90),0.0),('top',0.0,math.radians(89)),('3/4 rear',math.radians(-145),math.radians(20))]
rows=[(f,n,c,fn) for f,fname,ships in CAPITALS for n,c,fn in ships]
CW,RH,LW=360,260,200;W=LW+CW*4;H=70+RH*len(rows)+20
bg=Image.new('RGB',(W,H),(10,13,20));g=ImageDraw.Draw(bg);fb=ImageFont.truetype('DejaVuSans-Bold.ttf',22);fr=ImageFont.truetype('DejaVuSans.ttf',13);fbs=ImageFont.truetype('DejaVuSans-Bold.ttf',20)
g.text((20,14),'Driftgate Beyond · Capital ships, close up',font=fb,fill=(230,232,236))
for j,(n,_,_) in enumerate(V):g.text((LW+CW*j+10,48),n,font=fr,fill=(120,130,145))
for r,(f,n,c,fn) in enumerate(rows):
    M=fn();y0=70+RH*r;F=tuple(int(v*255) for v in rgb(FAC_HEX[f]))
    g.text((20,y0+20),n,font=fbs,fill=F);g.text((20,y0+48),f'{f.capitalize()} {c.lower()}',font=fr,fill=(190,195,205));g.text((20,y0+68),f'{len(M.T)} triangles',font=fr,fill=(110,118,130))
    for j,(_,yaw,p) in enumerate(V):
        im=render(M,f,yaw,p,CW,RH-10,52 if j==2 else 66);bg.paste(im,(LW+CW*j,y0),im)
    if r:g.line([(16,y0),(W-16,y0)],fill=(30,36,48))
bg.save('beyond_capitals_closeup.png');print(bg.size)
