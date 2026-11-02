# Close-up sheet of the Unbound hulls, four views each, each ship fitted to its row: python3 unbound_sheet.py OUT.png
import math,sys,os
import numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from render_beyond import render,rgb,FAC_HEX,rot
from beyond_unbound import UNBOUND
from PIL import Image,ImageDraw,ImageFont
out=sys.argv[1] if len(sys.argv)>1 else 'beyond_unbound.png'
V=[('3/4 front',math.radians(-36),math.radians(22)),('side',math.radians(-90),0.0),('top',0.0,math.radians(89)),('3/4 rear',math.radians(-145),math.radians(20))]
rows=[(n,c,fn) for _,_,ships in UNBOUND for n,c,fn in ships]
NOTES={'Raider':'Ostrova boom with drive and tail · Halcyon cockpit pod off centre to starboard · Varkesh wing slab and guns · crystal radar fin',
       'Skiff':'Ostrova spire hull · Halcyon radome and forward-swept wings · Varkesh square drives strapped on · jammer rods',
       'Corsair':'Varkesh chisel body and chin guns · Halcyon drive section · four Halcyon wings in an X · Ostrova nose ring and jammer halo',
       'Plunderer':'Halcyon cockpit pod · Varkesh spine · mismatched holds · crystal-clad boom engine on top · Ostrova crystal pontoon below',
       'Wrecker':'Varkesh fuselage · stolen Halcyon wings · Ostrova crystal torpedoes, faceted tail spire and halo',
       'Ravager':'Varkesh prow · Halcyon midsection · Ostrova stern and halo · Halcyon rail cannon · Varkesh giant gun and bridge'}
class _M:pass
CW,RH,LW=330,250,250;W=LW+CW*4;H=96+RH*len(rows)+30
bg=Image.new('RGB',(W,H),(9,12,18));g=ImageDraw.Draw(bg)
for y in range(H):g.line([(0,y),(W,y)],fill=(9+int(6*y/H),12+int(8*y/H),18+int(12*y/H)))
fb=lambda s:ImageFont.truetype('DejaVuSans-Bold.ttf',s);fr=lambda s:ImageFont.truetype('DejaVuSans.ttf',s)
F=tuple(int(v*255) for v in rgb(FAC_HEX['pirate']))
g.text((20,16),'Driftgate Beyond · The Unbound: hulls kitbashed from all three factions',font=fb(24),fill=(230,232,236))
g.text((20,46),'Every Unbound hull is Halcyon, Varkesh and Ostrova parts welded into one, in the Unbound sand colour · each ship fitted to its row',font=fr(14),fill=(140,150,165))
for j,(n,_,_) in enumerate(V):g.text((LW+CW*j+10,74),n,font=fr(13),fill=(120,130,145))
for r,(n,c,fn) in enumerate(rows):
    M=fn();y0=96+RH*r;T=np.array(M.T);cen=(T.reshape(-1,3).max(0)+T.reshape(-1,3).min(0))/2;N=_M();N.T=list(T-cen);N.R=M.R
    ext=max(max(np.abs(((T-cen).reshape(-1,3)@rot(yaw,p).T)[:,:2]).max(0)/np.array([CW/2,(RH-20)/2])) for _,yaw,p in V)
    g.text((20,y0+16),n,font=fb(22),fill=F);g.text((20,y0+46),c,font=fr(13),fill=(190,195,205));g.text((20,y0+66),f'{len(M.T)} triangles',font=fr(12),fill=(110,118,130))
    words=NOTES[n].split(' · ');[g.text((20,y0+92+i*17),'· '+w_,font=fr(11),fill=(150,156,168)) for i,w_ in enumerate(words)]
    for j,(_,yaw,p) in enumerate(V):im=render(N,'pirate',yaw,p,CW,RH-20,.88/ext);bg.paste(im,(LW+CW*j,y0),im)
    if r:g.line([(16,y0),(W-16,y0)],fill=(30,36,48))
g.text((20,H-24),'Preview only: not in the game yet. Names are placeholders; Raider, Skiff, Corsair and Plunderer are Driftgate 1\'s Unbound hulls.',font=fr(12),fill=(110,118,130))
bg.save(out);print('wrote',out,bg.size)
