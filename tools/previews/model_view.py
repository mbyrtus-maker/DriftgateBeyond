# Driftgate Beyond: a quick look at pack models straight from their builders (11 Nov 2026), without rebuilding the pack or
# opening the game: each model normalised as the pack does it, drawn with a depth buffer in its power's palette from several
# angles, big enough to judge nozzles, guns and joins. For working on a model; the in-game check is audit_game.py.
# Usage: python3 tools/previews/model_view.py OUT.png NAME[:faction] [NAME ...] [views=rear,front,side,top,below,stern,bow] [px=420]
import math,os,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,HERE)
from render_beyond import render_z,FAC_HEX
import d1kit
VIEW={'rear':(math.radians(180+28),math.radians(20)),'front':(math.radians(-36),math.radians(20)),'side':(math.radians(-90),0.0),'top':(0.0,math.radians(89.9)),
      'below':(math.radians(-40),math.radians(-32)),'stern':(math.radians(180+12),math.radians(8)),'bow':(math.radians(-10),math.radians(8)),'rearlow':(math.radians(180-35),math.radians(-18))}
class K:
    def __init__(s,T,R):s.T=T;s.R=R
def fac_of(name):
    for f,keys in (('halcyon','swift kite osprey wren plover heron tern albatross pelican lark skylark condor harrier architect aegis gannet peregrine shrike sovereign'),
                   ('varkesh','fang talon halberd pick gouge sledge runner bulwark rampart jackal wolfhound maul warhound foundry ward bombard ironclad vanguard bastille'),
                   ('ostrova','mote wisp vigil glim lumen delve drift cairn monolith seer oracle obelisk sentinel loom halo vesper prism lantern cathedral'),
                   ('pirate','raider skiff corsair plunderer wrecker ravager haven'),('wraith','wraith')):
        if name.startswith('dz_') and name[3:] in keys.split():return f
    for f in ('halcyon','varkesh','ostrova'):
        if f in name:return f
    if name.startswith('b_'):return 'brood'
    if name=='by_haven':return 'pirate'
    if name=='by_rift':return 'rift'
    return 'company' if name.startswith('by_') else 'freeport'
def load(name):
    # the model as the pack would hold it: centred on its box, longest half-extent 1; returns it with what its builder recorded
    import brood
    brood.LAST=None
    kind,fn=d1kit.NS['MODELS'][name];P,N,R=fn();P=np.array(P,float).reshape(-1,3,3);lo=P.reshape(-1,3).min(0);hi=P.reshape(-1,3).max(0);c=(lo+hi)/2;h=max(hi-lo)/2
    meta=getattr(brood,'LAST',None);pts={}
    if meta:
        for k in ('eng','gun','mine','seat'):pts[k]=[((np.array(p[0],float)-c)/h,p[1]/h if k=='eng' else 0) for p in meta.get(k,[])]
    return K(list((P-c)/h),list(R)),pts,kind
def mark(M,p,r,role):
    # a small octahedron marker
    p=np.array(p,float);V=[p+[r,0,0],p-[r,0,0],p+[0,r,0],p-[0,r,0],p+[0,0,r],p-[0,0,r]]
    for a,b,c in ((0,2,4),(2,1,4),(1,3,4),(3,0,4),(2,0,5),(1,2,5),(3,1,5),(0,3,5)):M.T.append(np.array([V[a],V[b],V[c]]));M.R.append((role,1.0))
def main(a):
    out=a[0];views=['rear','front','side','top'];px=420;names=[];marks=True
    for x in a[1:]:
        if x.startswith('views='):views=x[6:].split(',')
        elif x.startswith('px='):px=int(x[3:])
        elif x=='nomarks':marks=False
        else:names.append(x)
    fb=ImageFont.truetype('DejaVuSans-Bold.ttf',15);fr=ImageFont.truetype('DejaVuSans.ttf',12)
    H=int(px*.72);W=px*len(views);sh=Image.new('RGB',(W,(H+22)*len(names)),(12,15,22));g=ImageDraw.Draw(sh)
    for r,nm in enumerate(names):
        name,_,fac=nm.partition(':');fac=fac or fac_of(name);M,pts,kind=load(name);n=len(M.T)
        if marks:
            for p,_ in pts.get('gun',[]):mark(M,p,.018,6)
            for p,_ in pts.get('mine',[]):mark(M,p,.018,3)
        y0=(H+22)*r;g.text((8,y0+3),f'{name} · {fac} · {n} tris · engines {len(pts.get("eng",[]))} · gun muzzles {len(pts.get("gun",[]))} · mining heads {len(pts.get("mine",[]))}',font=fb,fill=(225,228,235))
        for j,v in enumerate(views):
            yaw,pit=VIEW[v];im=render_z(M,fac if fac in FAC_HEX else 'company',yaw,pit,px,H,px*.36,ss=2);sh.paste(im,(px*j,y0+22),im);g.text((px*j+6,y0+24),v,font=fr,fill=(120,130,145))
    sh.save(out);print('wrote',out,sh.size)
if __name__=='__main__':main(sys.argv[1:])
