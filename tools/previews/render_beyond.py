# Renders preview sheets of the Beyond hull designs (tools/previews/beyond_hulls.py) in the game's faction palettes.
# Usage: python3 render_beyond.py OUT.png   (flat-shaded, painter's algorithm, 3x supersampled)
import math,sys,os
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,os.path.dirname(__file__))
from beyond_hulls import DESIGNS

FAC_HEX={'halcyon':'#4fd8d0','varkesh':'#ff7a3d','ostrova':'#b893ff'}
HULL={'halcyon':[.6,.61,.62],'varkesh':[.43,.41,.4],'ostrova':[.56,.54,.6]}
def rgb(h):return np.array([int(h[i:i+2],16)/255 for i in (1,3,5)])
def mix(a,b,t):return np.array(a)*(1-t)+np.array(b)*t
def pal(fac):
    # mirrors mdlPal() in src/js/12_render.js: hull light, hull mid, dark metal, accent, glass, glow, lit window
    F=rgb(FAC_HEX[fac]);base=HULL[fac]
    c=[mix(base,F,.1),mix([.36,.38,.43],F,.04),np.array([.15,.16,.19]),F*.92,np.array([.16,.3,.4]),F,mix([.2,.33,.42],F,.25)]
    e=[0,0,0,0,.15,.85,.55]
    return c,e
def rot(yaw,pitch):
    cy,sy,cp,sp=math.cos(yaw),math.sin(yaw),math.cos(pitch),math.sin(pitch)
    Ry=np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]]);Rx=np.array([[1,0,0],[0,cp,-sp],[0,sp,cp]])
    return Rx@Ry
L=np.array([-.45,.75,.5]);L/=np.linalg.norm(L)
def render(M,fac,yaw,pitch,W,H,ppu,ss=3):
    T=np.array(M.T);RS=M.R;c,e=pal(fac);R=rot(yaw,pitch)
    P=T@R.T;W2,H2,k=W*ss,H*ss,ppu*ss
    img=Image.new('RGBA',(W2,H2),(0,0,0,0));d=ImageDraw.Draw(img)
    order=np.argsort(P[:,:,2].mean(1))
    for i in order:
        t=P[i];n=np.cross(t[1]-t[0],t[2]-t[0]);ln=np.linalg.norm(n)
        if ln<1e-12:continue
        n/=ln
        if n[2]<0:n=-n
        role,sh=RS[i];base=c[role]*sh
        lit=.32+.68*max(0.,float(n@L))+.18*max(0.,n[2])**8
        col=base*lit*(1-e[role])+c[role]*e[role]*1.15
        col=tuple(int(max(0,min(1,v))*255) for v in col)+(255,)
        pts=[(W2/2+p[0]*k,H2/2-p[1]*k) for p in t]
        d.polygon(pts,fill=col,outline=col)
    return img.resize((W,H),Image.LANCZOS)

VIEWS=[('3/4 front',math.radians(-38),math.radians(22)),('side',math.radians(-90),0.0),('top',0.0,math.radians(89)),('3/4 rear',math.radians(-145),math.radians(18))]
def sheet(out):
    CW,RH,LW,HD=300,300,330,74;W=LW+CW*len(VIEWS);Hh=HD+RH*len(DESIGNS)+34
    bg=Image.new('RGB',(W,Hh),(9,12,18));g=ImageDraw.Draw(bg)
    for y in range(Hh):g.line([(0,y),(W,y)],fill=(9+int(6*y/Hh),12+int(8*y/Hh),18+int(12*y/Hh)))
    fb=lambda s:ImageFont.truetype('DejaVuSans-Bold.ttf',s);fr=lambda s:ImageFont.truetype('DejaVuSans.ttf',s)
    g.text((24,18),'Driftgate Beyond · Light Fighters, one per faction',font=fb(24),fill=(230,232,236))
    g.text((24,48),'Generated in code, one design language per faction · painted in the game palette · same scale',font=fr(14),fill=(140,150,165))
    for j,(v,_,_) in enumerate(VIEWS):g.text((LW+CW*j+12,HD-2),v,font=fr(13),fill=(120,130,145))
    for r,(fac,name,fname,fn,notes) in enumerate(DESIGNS):
        M=fn();y0=HD+RH*r+14;F=tuple(int(v*255) for v in rgb(FAC_HEX[fac]))
        g.rectangle([16,y0+10,20,y0+RH-30],fill=F)
        g.text((32,y0+14),name,font=fb(30),fill=F);g.text((32,y0+52),fname+' · Light Fighter',font=fr(14),fill=(200,204,212))
        for i,t in enumerate(notes):g.text((32,y0+88+i*24),'· '+t,font=fr(13),fill=(170,176,188))
        g.text((32,y0+RH-52),f'{len(M.T)} triangles',font=fr(12),fill=(110,118,130))
        for j,(v,yaw,pitch) in enumerate(VIEWS):
            im=render(M,fac,yaw,pitch,CW,RH-20,112)
            bg.paste(im,(LW+CW*j,y0),im)
        if r:g.line([(16,y0-6),(W-16,y0-6)],fill=(30,36,48))
    g.text((24,Hh-26),'Preview only: not in the game yet. Halcyon: swept, bird-like, glass canopy · Varkesh: blocky slabs, exposed guns · Ostrova: spires, reactor halo, crystal',font=fr(12),fill=(110,118,130))
    bg.save(out);print('wrote',out,bg.size)
if __name__=='__main__':sheet(sys.argv[1] if len(sys.argv)>1 else 'beyond_light_fighters.png')
