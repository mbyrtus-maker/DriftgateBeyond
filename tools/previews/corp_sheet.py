# Preview sheet of the makers' R&D stations: python3 corp_sheet.py OUT.png [logos OUT2.png]
import math,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import render_beyond
from render_beyond import rgb,FAC_HEX,HULL
from stations_sheet import fit
import numpy as np
from render_beyond import render,rot
from beyond_corp import corp_station,MAKERS,LOGOS,logo_board
from beyond_hulls import Mesh
from PIL import Image,ImageDraw,ImageFont
for m,_,home,col in MAKERS:FAC_HEX['mk_'+m]=col;HULL['mk_'+m]=HULL[home]
out=sys.argv[1] if len(sys.argv)>1 else 'beyond_corp.png'
YAW,PIT=math.radians(-35),math.radians(22)
fb=lambda s:ImageFont.truetype('DejaVuSans-Bold.ttf',s);fr=lambda s:ImageFont.truetype('DejaVuSans.ttf',s)
def bgimg(W,H):
    bg=Image.new('RGB',(W,H),(9,12,18));g=ImageDraw.Draw(bg)
    for y in range(H):g.line([(0,y),(W,y)],fill=(9+int(6*y/H),12+int(8*y/H),18+int(12*y/H)))
    return bg,g
# sheet 1: one maker per home style, the station growing: new (no labs), one G2 lab, G2 + G3 + G4, four labs up to G5
COLS=[('New maker','no labs yet: four empty sockets',()),('First R&D','one lab, grade 2',(2,)),('Three lines','labs at grades 2, 3 and 4',(2,3,4)),('Four lines','grades 3, 4, 5 and 5',(3,4,5,5))]
ROWS=[('tcy','halcyon'),('mg','varkesh'),('sw','ostrova'),('cp','freeport')]
LW,HD,CW,RH=210,84,360,330
W=LW+CW*len(COLS);H=HD+RH*len(ROWS)+34;bg,g=bgimg(W,H)
g.text((24,18),"Driftgate Beyond · A maker's R&D station",font=fb(24),fill=(230,232,236))
g.text((24,50),"Not dockable · the CEO launches from the bay at the tower's foot · a lab per product line taken through R&D, growing with its grade · the maker's logo on four boards at the crown",font=fr(13),fill=(140,150,165))
for i,(t,sub,_) in enumerate(COLS):g.text((LW+CW*i+14,HD-6),t,font=fb(14),fill=(170,178,190));g.text((LW+CW*i+14,HD+12),sub,font=fr(12),fill=(120,128,140))
NAME={m:n for m,n,_,_ in MAKERS};HOME={m:h for m,_,h,_ in MAKERS};COL={m:c for m,_,_,c in MAKERS}
for r,(mk,style) in enumerate(ROWS):
    y0=HD+RH*r+30;F=tuple(int(v*255) for v in rgb(COL[mk]))
    g.rectangle([16,y0+8,20,y0+RH-40],fill=F);g.text((32,y0+10),{'halcyon':'Halcyon','varkesh':'Varkesh','ostrova':'Ostrova','freeport':'Freeports'}[style],font=fb(22),fill=F)
    g.text((32,y0+42),'shown: '+NAME[mk],font=fr(13),fill=(200,204,212))
    Ms=[corp_station(style,gr,mk) for _,_,gr in COLS];BIG=np.array(Ms[-1].T).reshape(-1,3);c=(BIG.max(0)+BIG.min(0))/2
    P=(BIG-c)@rot(YAW,PIT).T;ppu=min((CW-20)/2/np.abs(P[:,0]).max(),(RH-50)/2/np.abs(P[:,1]).max())*.9
    for i,M in enumerate(Ms):
        N=Mesh();N.T=[np.array(t)-c for t in M.T];N.R=M.R;im=render(N,'mk_'+mk,YAW,PIT,CW-20,RH-50,ppu);bg.paste(im,(LW+CW*i+10,y0+10),im)
    if r:g.line([(16,y0-4),(W-16,y0-4)],fill=(30,36,48))
g.text((24,H-26),'Preview only, not in the game. Pictures scaled to fit; in the game an R&D station is smaller than a depot.',font=fr(12),fill=(110,118,130))
bg.save(out);print('wrote',out,bg.size)
# sheet 2: all twelve makers, their accent and logo, each on its station at four labs
out2=out.replace('.png','_makers.png');CW2,RH2,NC=300,300,4
W2=CW2*NC+40;H2=84+RH2*3+30;bg,g=bgimg(W2,H2)
g.text((24,18),"Driftgate Beyond · The twelve makers: accents and logos",font=fb(24),fill=(230,232,236))
g.text((24,50),"Each accent a shade of its home power's colour (the Compact's gold at the freeports) · each station shown with four labs",font=fr(13),fill=(140,150,165))
for i,(m,name,home,col) in enumerate(MAKERS):
    cx=20+CW2*(i%NC);cy=84+RH2*(i//NC);F=tuple(int(v*255) for v in rgb(col))
    M=corp_station(home,(2,3,4,5),m);im=fit(M,YAW,PIT,CW2-10,RH2-70,'mk_'+m,.95);bg.paste(im,(cx-5,cy+58),im)
    L=Mesh();logo_board(L,m,(0,0,0),math.pi/2,1.0);im2=fit(L,0.0,0.0,56,56,'mk_'+m,.95);bg.paste(im2,(cx+4,cy+2),im2)
    g.text((cx+70,cy+8),name,font=fb(15),fill=F);g.text((cx+70,cy+30),{'tcy':'Halcyon','bl':'Halcyon','hf':'Varkesh','mg':'Varkesh','sw':'Ostrova','ad':'Ostrova','mwa':'Mirrorwater','qs':'Mirrorwater','cr':'Coldwater Drift','cp':'Coldwater Drift','ewd':'Ember Wake','wf':'Ember Wake'}[m]+' · '+col,font=fr(12),fill=(150,158,170))
bg.save(out2);print('wrote',out2,bg.size)
