# Preview sheet of the Beyond player bases: python3 stations_sheet.py OUT.png
import math,sys,os
import numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from render_beyond import render,rgb,FAC_HEX,rot
from beyond_stations import *
from PIL import Image,ImageDraw,ImageFont
class _M:pass
def fit(M,yaw,pitch,W,H,fac='company',fill=.86,zbuf=False):
    T=np.array(M.T);c=(T.reshape(-1,3).max(0)+T.reshape(-1,3).min(0))/2;N=_M();N.T=list(T-c);N.R=M.R
    P=(T-c).reshape(-1,3)@rot(yaw,pitch).T;ex=np.abs(P[:,0]).max();ey=np.abs(P[:,1]).max()
    return render(N,fac,yaw,pitch,W,H,min(W/2/ex,H/2/ey)*fill,zbuf=zbuf)
ROWS=[('Lair',[('Lair 1','hidden: one hangar, a hatch, a whip antenna',lambda:lair(1)),('Lair 2','+ second berth, forge vent, container stash, dish',lambda:lair(2))]),
      ('Depot',[('Depot 1','hub, docking arm, storage',lambda:depot(1)),('Depot 2','+ production module, hangar',lambda:depot(2)),('Depot 3','+ defence turrets, armour, life-support ring',lambda:depot(3))]),
      ('Station',[('Station core, standard','spine, habitat ring, crown dock, 5 hardpoints',lambda:station_core('standard')),('Station core, asteroid','the same core set into rock, 5 hardpoints',lambda:station_core('asteroid'))]),
      ('Buildings',[(n,'one per station level',fn) for n,fn in BUILDINGS]),
      ('Level 5',[('Standard station, level 5','yard, storage, defence, hangar, market',lambda:station_full('standard')),('Asteroid station, level 5','forge, yard, defence, storage, market',lambda:station_full('asteroid'))])]
if __name__=='__main__':
    out=sys.argv[1] if len(sys.argv)>1 else 'beyond_player_bases.png'
    YAW,PIT=math.radians(-35),math.radians(24)
    CW,LW,HD=330,170,74;RHs=[300,280,380,250,460]
    W=LW+CW*6;H=HD+sum(RHs)+30
    bg=Image.new('RGB',(W,H),(9,12,18));g=ImageDraw.Draw(bg)
    for y in range(H):g.line([(0,y),(W,y)],fill=(9+int(6*y/H),12+int(8*y/H),18+int(12*y/H)))
    fb=lambda s:ImageFont.truetype('DejaVuSans-Bold.ttf',s);fr=lambda s:ImageFont.truetype('DejaVuSans.ttf',s)
    F=tuple(int(v*255) for v in rgb(FAC_HEX['company']))
    g.text((24,18),'Driftgate Beyond · Player bases: Lair, Depot, Station and buildings',font=fb(24),fill=(230,232,236))
    g.text((24,48),'Generated in code · the neutral company style (shared with the freeports) in company amber · each picture scaled to fit, not to one scale',font=fr(14),fill=(140,150,165))
    y0=HD
    for (rname,items),RH in zip(ROWS,RHs):
        g.rectangle([16,y0+8,20,y0+RH-14],fill=F);g.text((32,y0+12),rname,font=fb(22),fill=F)
        n=len(items);cw=CW*6//n if n<6 else CW
        for k,(name,note,fn) in enumerate(items):
            M=fn();x0=LW+cw*k
            im=fit(M,YAW,PIT,cw-20,RH-62);bg.paste(im,(x0+10,y0+8),im)
            g.text((x0+14,y0+RH-50),name,font=fb(15),fill=F);g.text((x0+14,y0+RH-29),f'{note} · {len(M.T)} tris',font=fr(11),fill=(130,138,150))
            print(name,len(M.T))
        y0+=RH;g.line([(16,y0-4),(W-16,y0-4)],fill=(30,36,48))
    g.text((24,H-24),'Preview only: not in the game yet. Faction stations and the freeports come next.',font=fr(12),fill=(110,118,130))
    bg.save(out);print('wrote',out,bg.size)
