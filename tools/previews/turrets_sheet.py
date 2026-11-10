# Driftgate Beyond: the model pack's station gun turret (beyond_stations.turret, 9 Nov 2026), before and after, for review:
# the turret alone from four angles in each power's colours, and the models that carry it (Depot 3, the defence platform,
# design 2's Depot 3), old and new side by side. The old turret is kept here only for the comparison.
# Usage: python3 tools/previews/turrets_sheet.py OUT.png   (the review copy: tools/previews/beyond_turrets.png)
import math,os,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,HERE)
from render_beyond import render
import beyond_stations as BS
from beyond_hulls import Mesh,MID,DARK,box
from beyond_capitals import tube
import beyond_base_designs as BD
def turret_old(M,c,s=1.0,up=True):
    c=np.array(c,float);k=1 if up else -1
    BS.drum(M,c,c+[0,k*.08*s,0],.2*s,DARK,10)
    box(M,tuple(c+[0,k*.17*s,0]),(.3*s,.16*s,.36*s),MID,(.8,.8))
    for sx in (1,-1):tube(M,[c+[sx*.07*s,k*.17*s,.16*s],c+[sx*.07*s,k*.17*s,.7*s]],[.03*s,.025*s],DARK,1.0,6)
NEW=BS.turret
def with_turret(fn,old):
    BS.turret=turret_old if old else NEW;BD.turret=BS.turret
    try:return fn()
    finally:BS.turret=NEW;BD.turret=NEW
def centred(M):
    T=np.array(M.T,float);lo=T.reshape(-1,3).min(0);hi=T.reshape(-1,3).max(0);N=Mesh();N.T=list(T-(lo+hi)/2);N.R=M.R;return N
def one(old):
    M=Mesh();(turret_old if old else NEW)(M,(0,0,0),1.0);return centred(M)
try:F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16);FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
except Exception:F=FB=ImageFont.load_default()
def main(out):
    TW,TH=340,260;views=[(-35,22),(35,14),(150,25),(-90,5)];facs=['company','halcyon','varkesh','ostrova']
    tiles=[]
    for old in (True,False):
        M=one(old)
        tiles.append([render(M,facs[i],math.radians(y),math.radians(p),TW,TH,TH/1.0) for i,(y,p) in enumerate(views)])
    parts=[('Depot 3 (by_depot3)',lambda:BS.depot(3),1.6),('defence platform (by_defence)',BS.defence_platform,1.25),('design 2 Depot 3',lambda:[d for d in BD.DESIGNS if d[0]==2][0][3](3),1.7)]
    ptiles=[]
    for old in (True,False):
        ptiles.append([render(centred(with_turret(fn,old)),'company',math.radians(-35),math.radians(24),TW,TH,TH/2/sz) for _,fn,sz in parts])
    W=40+4*TW+60;H=80+2*(TH+30)+60+2*(TH+30)
    im=Image.new('RGB',(W,H),(16,18,24));d=ImageDraw.Draw(im)
    d.text((12,10),'Station gun turret (model pack), before and after: company, Halcyon, Varkesh, Ostrova colours',font=FB,fill=(235,235,240))
    y=50
    for r,lab in enumerate(('before','after')):
        d.text((12,y),lab,font=F,fill=(200,205,215) if r==0 else (160,230,170));y+=24
        for j,t in enumerate(tiles[r]):im.paste(t.convert('RGB'),(20+j*TW,y))
        y+=TH+6
    d.text((12,y+10),'On the models that carry it (company colours)',font=FB,fill=(235,235,240));y+=50
    for r,lab in enumerate(('before','after')):
        d.text((12,y),lab+':  '+'   |   '.join(p[0] for p in parts),font=F,fill=(200,205,215) if r==0 else (160,230,170));y+=24
        for j,t in enumerate(ptiles[r]):im.paste(t.convert('RGB'),(20+j*TW,y))
        y+=TH+6
    im.save(out);print(out)
if __name__=='__main__':main(sys.argv[1])
