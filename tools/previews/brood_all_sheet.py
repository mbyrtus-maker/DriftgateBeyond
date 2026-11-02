# Every Brood model (Driftgate 1's, with fins in place of legs, plus the new destroyer): python3 brood_all_sheet.py OUT.png
import math,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from render_beyond import rgb,FAC_HEX
from stations_sheet import fit
from beyond_brood import gullet
import brood
from PIL import Image,ImageDraw,ImageFont
class W_:
    def __init__(s,o):s.T,s.R=list(o[0]),list(o[2])
out=sys.argv[1] if len(sys.argv)>1 else 'beyond_brood_all.png'
NAMES={'b_skitter':'Skitter · interceptor','b_thresher':'Thresher · striker','b_carapace':'Carapace · heavy','b_sporemaw':'Sporemaw · bomber','b_grazer':'Grazer · miner',
       'b_gorger':'Gorger · hauler','b_weaver':'Weaver · constructor','b_watcher':'Watcher · scout','b_mite':'Mite · drone','b_leviathan':'Leviathan · frigate',
       'b_prowler':'Prowler · escort','b_hive':'Hive Ship · carrier'}
items=[(NAMES[k],W_(fn())) for k,fn in brood.BROOD_MODELS.items()]
items.insert(11,('Gullet · destroyer (new)',gullet()));items[10],items[12]=items[12],items[10]   # escort, destroyer, carrier
C=5;CW,RH=320,280;rows=(len(items)+C-1)//C;W,H=C*CW+20,90+rows*RH+20
bg=Image.new('RGB',(W,H),(9,12,18));g=ImageDraw.Draw(bg)
for y in range(H):g.line([(0,y),(W,y)],fill=(9+int(6*y/H),12+int(8*y/H),18+int(12*y/H)))
fb=lambda s:ImageFont.truetype('DejaVuSans-Bold.ttf',s);fr=lambda s:ImageFont.truetype('DejaVuSans.ttf',s);F=tuple(int(v*255) for v in rgb(FAC_HEX['brood']))
g.text((24,18),'Driftgate Beyond · The Brood, with fins in place of legs',font=fb(24),fill=(230,232,236))
g.text((24,48),'Driftgate 1\'s Brood models (tools/brood.py) with every set of legs replaced by fins, and the new destroyer · each scaled to fit',font=fr(14),fill=(140,150,165))
for i,(n,M) in enumerate(items):
    x0=10+CW*(i%C);y0=80+RH*(i//C)
    im=fit(M,math.radians(-36),math.radians(22),CW-10,RH-50,'brood',.85);bg.paste(im,(x0+5,y0),im)
    g.text((x0+14,y0+RH-46),n,font=fb(14),fill=F);g.text((x0+14,y0+RH-26),f'{len(M.T)} tris',font=fr(11),fill=(120,128,140))
bg.save(out);print('wrote',out,len(items))
