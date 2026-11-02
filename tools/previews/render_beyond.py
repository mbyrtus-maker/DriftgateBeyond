# Renders preview sheets of the Beyond hull designs (tools/previews/beyond_hulls.py) in the game's faction palettes.
# Usage: python3 render_beyond.py OUT.png   (flat-shaded, painter's algorithm, 3x supersampled)
import math,sys,os
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,os.path.dirname(__file__))
from beyond_hulls import DESIGNS,FAMILY

FAC_HEX={'halcyon':'#4fd8d0','varkesh':'#ff7a3d','ostrova':'#b893ff','company':'#f0b24a','freeport':'#e8c878','pirate':'#d8cd98'}
HULL={'halcyon':[.6,.61,.62],'varkesh':[.43,.41,.4],'ostrova':[.56,.54,.6],'company':[.57,.58,.6],'freeport':[.57,.58,.6],'pirate':[.5,.47,.42]}
def rgb(h):return np.array([int(h[i:i+2],16)/255 for i in (1,3,5)])
def mix(a,b,t):return np.array(a)*(1-t)+np.array(b)*t
def pal(fac):
    # mirrors mdlPal() in src/js/12_render.js: hull light, hull mid, dark metal, accent, glass, glow, lit window
    F=rgb(FAC_HEX[fac]);base=HULL[fac]
    c=[mix(base,F,.1),mix([.36,.38,.43],F,.04),np.array([.15,.16,.19]),F*.92,np.array([.16,.3,.4]),F,mix([.2,.33,.42],F,.25),np.array([.43,.4,.36]),np.array([.25,.23,.21])]
    e=[0,0,0,0,.15,.85,.55,0,0]   # roles 7 and 8 are rock and dark rock, as in mdlPal()
    return c,e
def rot(yaw,pitch):
    cy,sy,cp,sp=math.cos(yaw),math.sin(yaw),math.cos(pitch),math.sin(pitch)
    Ry=np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]]);Rx=np.array([[1,0,0],[0,cp,-sp],[0,sp,cp]])
    return Rx@Ry
L=np.array([-.45,.75,.5]);L/=np.linalg.norm(L)
def split(T,RS,lim=.18):
    # preview only: split long triangles into four until no edge is longer than lim, so the painter's algorithm sorts big flat
    # panels (flight decks) correctly; the game draws with a depth buffer and doesn't need this
    T=np.array(T,float);RS=list(RS)
    for _ in range(6):
        e=np.max(np.linalg.norm(T-np.roll(T,1,axis=1),axis=2),axis=1);big=e>lim
        if not big.any():break
        B=T[big];a,b,c=B[:,0],B[:,1],B[:,2];ab,bc,ca=(a+b)/2,(b+c)/2,(c+a)/2
        new=np.concatenate([np.stack(t,1) for t in ((a,ab,ca),(ab,b,bc),(ca,bc,c),(ab,bc,ca))])
        rb=[r for r,k in zip(RS,big) if k];RS=[r for r,k in zip(RS,big) if not k]+rb*4
        T=np.concatenate([T[~big],new])
    return T,RS
def render(M,fac,yaw,pitch,W,H,ppu,ss=3):
    T,RS=split(M.T,M.R);c,e=pal(fac);R=rot(yaw,pitch)
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
def family(out,fam=None,title='Driftgate Beyond · Fighters by faction: Light, Medium, Heavy',cols=('Light fighter','Medium fighter','Heavy fighter'),ppu=92,cw=450):
    fam=fam or FAMILY
    # three factions x Light/Medium/Heavy fighters: a big 3/4 view per cell with the planform inset, all at one scale
    CW,RH,LW,HD=cw,330,230,74;W=LW+CW*len(cols);Hh=HD+RH*len(fam)+34
    bg=Image.new('RGB',(W,Hh),(9,12,18));g=ImageDraw.Draw(bg)
    for y in range(Hh):g.line([(0,y),(W,y)],fill=(9+int(6*y/Hh),12+int(8*y/Hh),18+int(12*y/Hh)))
    fb=lambda s:ImageFont.truetype('DejaVuSans-Bold.ttf',s);fr=lambda s:ImageFont.truetype('DejaVuSans.ttf',s)
    g.text((24,18),title,font=fb(24),fill=(230,232,236))
    g.text((24,48),'Generated in code, one design language per faction · game palette · one scale throughout · inset: from above',font=fr(14),fill=(140,150,165))
    for c,cl in enumerate(cols):g.text((LW+CW*c+14,HD-4),cl,font=fr(14),fill=(130,140,155))
    for r,(fac,fname,ships) in enumerate(fam):
        y0=HD+RH*r+14;F=tuple(int(v*255) for v in rgb(FAC_HEX[fac]))
        g.rectangle([16,y0+8,20,y0+RH-24],fill=F);g.text((32,y0+12),fname.split()[0],font=fb(26),fill=F);g.text((32,y0+46),fname.split()[1],font=fr(14),fill=(200,204,212))
        for c,(name,cl,fn) in enumerate(ships):
            M=fn();x0=LW+CW*c
            im=render(M,fac,math.radians(-36),math.radians(22),CW-150,RH-40,ppu);bg.paste(im,(x0-6,y0+6),im)
            ins=render(M,fac,0.0,math.radians(89),130,150,42*ppu/92);g.rectangle([x0+CW-150,y0+RH-176,x0+CW-14,y0+RH-22],outline=(34,40,54));bg.paste(ins,(x0+CW-147,y0+RH-174),ins)
            g.text((x0+14,y0+RH-48),name,font=fb(18),fill=F);g.text((x0+14,y0+RH-24),f'{cl} · {len(M.T)} tris',font=fr(12),fill=(120,128,140))
        if r:g.line([(16,y0-6),(W-16,y0-6)],fill=(30,36,48))
    g.text((24,Hh-26),'Preview only: not in the game yet. Hull names are Driftgate 1\'s faction names for each class.',font=fr(12),fill=(110,118,130))
    bg.save(out);print('wrote',out,bg.size)
if __name__=='__main__':
    a=sys.argv[1] if len(sys.argv)>1 else 'beyond_light_fighters.png'
    if 'miners' in a or 'haulers' in a:
        from beyond_work import WORK
        k=0 if 'miners' in a else 3
        fam=[(f,n,s[k:k+3]) for f,n,s in WORK]
        family(a,fam,'Driftgate Beyond · '+('Miners' if k==0 else 'Haulers')+' by faction: Light, Medium, Heavy',
               tuple(c+(' miner' if k==0 else ' hauler') for c in ('Light','Medium','Heavy')),ppu=60)
    elif 'capitals' in a:
        from beyond_capitals import CAPITALS
        family(a,CAPITALS,'Driftgate Beyond · Capital ships by faction',('Escort','Destroyer','Carrier'),ppu=56,cw=560)
    elif 'unbound' in a:
        from beyond_unbound import UNBOUND
        family(a,UNBOUND,'Driftgate Beyond · The Unbound: hulls kitbashed from all three factions',('','',''),ppu=64,cw=520)
    elif 'scouts_bombers' in a:
        from beyond_recon import RECON
        family(a,RECON,'Driftgate Beyond · Scouts and bombers by faction',('Scout','Advanced scout','Bomber','Heavy bomber (two seats)'),ppu=78)
    else:family(a) if 'family' in a or 'fighters_by' in a else sheet(a)
