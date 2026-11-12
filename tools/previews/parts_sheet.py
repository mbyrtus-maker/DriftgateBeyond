# Driftgate Beyond: the shared parts the hull builders use (11 Nov 2026), drawn large and alone for review: the drive nozzle
# of each design language (brood.Mesh.vent), the Varkesh drive housing (beyond_hulls.drivebox) and the gun of each language
# (beyond_hulls.barrel), from behind, three-quarters and the side.
# Usage: python3 tools/previews/parts_sheet.py OUT.png
import math,os,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,HERE)
from render_beyond import render_z
import beyond_hulls as BH
from beyond_hulls import Mesh,DARK,MID,ACC,LIGHT,box
import brood
def centred(M,k=None):
    T=np.array(M.T,float);lo=T.reshape(-1,3).min(0);hi=T.reshape(-1,3).max(0);N=Mesh();N.T=list((T-(lo+hi)/2)/(max(hi-lo)/2));N.R=M.R;return N
def nozzle(st):
    M=Mesh();M.style=st
    if st=='varkesh':BH.drivebox(M,(0,0,.1),(.26,.24,.3),-.06,.1)
    else:
        M.tube([(0,0,.3),(0,0,.02)],[.13,.115],12,lambda i,j,n,p:(MID if st!='brood' else ACC,.95),cap0=True,cap1=False);M.vent((0,0,-.06),.1)
    return centred(M)
def gun(st,role=DARK):
    M=Mesh();M.style=st;box(M,(0,0,-.06),(.16,.12,.14),MID);BH.barrel(M,(0,0,0),.5,.03,role);return centred(M)
PARTS=[('nozzle: Halcyon bell','halcyon',lambda:nozzle('halcyon')),('drive: Varkesh square','varkesh',lambda:nozzle('varkesh')),('nozzle: Ostrova ring and crystal','ostrova',lambda:nozzle('ostrova')),('pore: Brood','brood',lambda:nozzle('brood')),
       ('gun: Halcyon','halcyon',lambda:gun('halcyon')),('gun: Varkesh','varkesh',lambda:gun('varkesh')),('lance: Ostrova','ostrova',lambda:gun('ostrova',ACC))]
VIEWS=[('from behind',math.radians(180+14),math.radians(10)),('rear three-quarters',math.radians(180+48),math.radians(22)),('side',math.radians(-90),0.0),('front three-quarters',math.radians(-40),math.radians(20))]
def main(out):
    px=330;H=250;fb=ImageFont.truetype('DejaVuSans-Bold.ttf',14);fr=ImageFont.truetype('DejaVuSans.ttf',11)
    sh=Image.new('RGB',(px*len(VIEWS)+170,(H)*len(PARTS)+26),(12,15,22));g=ImageDraw.Draw(sh)
    for j,(v,_,_) in enumerate(VIEWS):g.text((170+px*j+6,6),v,font=fr,fill=(130,140,155))
    for r,(lab,fac,fn) in enumerate(PARTS):
        M=fn();y0=26+H*r;g.text((8,y0+8),lab,font=fb,fill=(225,228,235));g.text((8,y0+28),f'{len(M.T)} triangles',font=fr,fill=(130,140,155))
        for j,(v,yaw,pit) in enumerate(VIEWS):
            im=render_z(M,fac,yaw,pit,px,H,H*.42,ss=2);sh.paste(im,(170+px*j,y0),im)
    sh.save(out);print('wrote',out,sh.size)
if __name__=='__main__':main(sys.argv[1])
