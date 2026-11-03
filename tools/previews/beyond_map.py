"""Driftgate Beyond galaxy map preview: systems, gates, checks (planar, clear of other systems, freeports with two exits)."""
import sys, itertools, math
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import patheffects as pe

def pol(ang,r,c=(.5,.5)):
    t=math.radians(ang);return (round(c[0]+r*math.cos(t),3),round(c[1]+r*math.sin(t),3))
def sy(name,ang,r,kind,own=None):
    x,y=pol(ang,r);return (name,x,y,kind,own)
# Deep space is the middle of the galaxy: the Bloom at its centre, an inner ring of five deep systems, and a rim of six
# with the Wrack (Scrapheart Haven) among them. The freeports sit just outside deep space, each in a pocket whose two gates
# both lead into the deep-space rim: every route to a freeport crosses deep space.
# Around that, a ring of twelve: the three frontiers, the three forges, and six quiet systems that are the doors to deep space.
# Outside, the three cores, the relay, and more quiet space out to the corners.
R1,R2,RF,R3,R4=.10,.19,.28,.36,.47
DISC=.235
S = {
 'bl':("The Bloom",.5,.5,'hive','brood'),
 'gs':sy("Glass Shallows",270,R1,'deep'),
 'cd':sy("Corona Deep",342,R1,'deep'),
 'ld':sy("Lantern Deep",54,R1,'deep'),
 'ae':sy("Ashen Expanse",126,R1,'deep'),
 'ud':sy("Umbral Deep",198,R1,'deep'),
 'gd':sy("Gloam Deep",0,R2,'deep'),
 'mn':sy("Mournwater",60,R2,'deep'),
 'tm':sy("Thornmere",120,R2,'deep'),
 'wr':sy("The Wrack",180,R2,'den','pirate'),
 'sk':sy("Sunken Reach",240,R2,'deep'),
 'br':sy("Blackwater Rift",300,R2,'deep'),
 'ew':sy("Ember Wake",30,RF,'freeport','freeport'),
 'cw':sy("Coldwater Drift",150,RF,'freeport','freeport'),
 'mw':sy("Mirrorwater",270,RF,'freeport','freeport'),
 'vm':sy("Sundered Marches",330,R3,'frontier','varkesh'),
 'dl':sy("Dusk Lanes",0,R3,'void'),
 'ci':sy("Cinder Reach",30,R3,'contested'),
 'fh':sy("Fathom's Edge",60,R3,'void'),
 'of':sy("Veil Fringe",90,R3,'frontier','ostrova'),
 'qs':sy("Quietwater Sound",120,R3,'void'),
 'sh':sy("The Shoal",150,R3,'contested'),
 'hu':sy("Hushfall",180,R3,'void'),
 'hr':sy("Tessellate Reach",210,R3,'frontier','halcyon'),
 'cv':sy("Coldlight Void",240,R3,'void'),
 'ke':sy("Kestrel Drift",270,R3,'contested'),
 'bw':sy("Brinewell",300,R3,'void'),
 'vb':sy("Varkesh Hold",330,R4,'core','varkesh'),
 'sg':sy("Saltglass Verge",0,R4,'void'),
 'rh':sy("Rook's Hollow",30,R4,'void'),
 'ho':sy("Hollow Verge",60,R4,'hub'),
 'os':sy("Ostrova Spire",90,R4,'core','ostrova'),
 'eb':sy("Ebbwater",120,R4,'void'),
 'gw':sy("Greywater Shelf",150,R4,'void'),
 'dm':sy("Driftmoor",180,R4,'void'),
 'hp':sy("Halcyon Prime",210,R4,'core','halcyon'),
 'nv':sy("Northgap Void",240,R4,'void'),
 'sf':sy("Starless Fold",270,R4,'void'),
 'av':sy("Ashwind Void",300,R4,'void'),
 'pr':("Pale Reach",.05,.05,'void',None),
 'ih':("Iron Hush",.95,.05,'void',None),
 'sm':("Saltmoor",.05,.95,'void',None),
 'll':("Lastlight Shoals",.95,.95,'void',None),
}
L = """bl-gs bl-cd bl-ld bl-ae bl-ud gs-cd cd-ld ld-ae ae-ud ud-gs
gd-cd mn-ld tm-ae wr-ud sk-gs br-gs gd-mn mn-tm tm-wr wr-sk sk-br br-gd
ew-gd ew-mn cw-tm cw-wr mw-sk mw-br
dl-gd fh-mn qs-tm hu-wr cv-sk bw-br
vm-dl dl-ci ci-fh fh-of of-qs qs-sh sh-hu hu-hr hr-cv cv-ke ke-bw bw-vm
vb-vm os-of hp-hr sg-dl sg-rh eb-qs eb-sm nv-cv nv-pr
rh-ci rh-ho ho-of ho-os os-ll ll-rh gw-sh gw-dm dm-hp gw-sm hp-pr sf-ke sf-av av-bw av-vb vb-ih ih-av dm-hu""".split()
L = [tuple(e.split('-')) for e in L]

def P(i): return (S[i][1], S[i][2])
def cross(a,b,c,d):
    def o(p,q,r): return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    A,B,C,D = P(a),P(b),P(c),P(d)
    return o(A,B,C)*o(A,B,D) < 0 and o(C,D,A)*o(C,D,B) < 0
def segdist(p,a,b):
    ax,ay=a;bx,by=b;px,py=p;dx,dy=bx-ax,by-ay
    t=max(0,min(1,((px-ax)*dx+(py-ay)*dy)/(dx*dx+dy*dy)));return math.hypot(px-ax-t*dx,py-ay-t*dy)

def check():
    ok=True;nb={k:[] for k in S}
    for a,b in L:
        assert a in S and b in S,(a,b);nb[a].append(b);nb[b].append(a)
    if len(set(frozenset(e) for e in L))!=len(L): print('DUPLICATE LINK');ok=False
    for (a,b),(c,d) in itertools.combinations(L,2):
        if len({a,b,c,d})==4 and cross(a,b,c,d): print('CROSS',a,b,'x',c,d);ok=False
    for a,b in L:
        for k in S:
            if k not in(a,b) and segdist(P(k),P(a),P(b))<.045: print('CLOSE',k,'to',a,b,round(segdist(P(k),P(a),P(b)),3));ok=False
    for k,v in S.items():
        if v[3]=='freeport' and len(nb[k])!=2: print('FREEPORT EXITS',k,len(nb[k]));ok=False
        if not nb[k]: print('ISOLATED',k);ok=False
    seen={'hp'};st=['hp']
    while st:
        x=st.pop()
        for y in nb[x]:
            if y not in seen: seen.add(y);st.append(y)
    if len(seen)!=len(S): print('DISCONNECTED',set(S)-seen);ok=False
    from collections import Counter
    print(len(S),'systems,',len(L),'gates; kinds',dict(Counter(v[3] for v in S.values())),'; ok' if ok else '; PROBLEMS')
    return nb

COL={'halcyon':'#4fd8d0','varkesh':'#ff7a3d','ostrova':'#b893ff','brood':'#9be35a','freeport':'#e8c878','pirate':'#d8cd98'}
def draw(out,nb):
    fig=plt.figure(figsize=(12,12),dpi=110);ax=fig.add_axes([0,0,1,1]);fig.patch.set_facecolor('#05070d');ax.set_facecolor('#05070d')
    from matplotlib.patches import Circle
    ax.add_patch(Circle((.5,.5),DISC,facecolor='#0d1428',edgecolor='#232d45',lw=1,zorder=0))
    ax.text(.5,.5+DISC-.014,'DEEP SPACE',ha='center',va='bottom',fontsize=9,color='#4a5675',zorder=0)
    for a,b in L:
        (x1,y1),(x2,y2)=P(a),P(b);ax.plot([x1,x2],[y1,y2],color='#36435f',lw=1.6,zorder=1)
    for k,(n,x,y,kind,own) in S.items():
        c=COL.get(own,'#8c91a5');r={'core':300,'hive':300,'frontier':170,'freeport':210,'den':190,'hub':170,'contested':150,'deep':130,'void':70}[kind]
        mk={'freeport':'D','den':'X','hive':'h'}.get(kind,'o')
        face=c if kind!='void' else '#0c1222'
        ax.scatter([x],[y],s=r,c=face,edgecolors=c if kind=='void' else '#ece4cf',linewidths=1.4,marker=mk,zorder=3)
        lab=n+('' if kind in('void',) else f"\n{ {'core':'core','frontier':'frontier','hive':'Brood hive','contested':'forge','hub':'relay','den':'Scrapheart Haven','deep':'deep','freeport':'freeport'}[kind] }")
        t=ax.text(x,y+.028,lab,ha='center',va='top',fontsize=9.5 if kind!='void' else 8.5,color='#ece4cf' if kind!='void' else '#8c91a5',zorder=4,family='DejaVu Sans')
        t.set_path_effects([pe.withStroke(linewidth=3,foreground='#05070d')])
    ax.set_xlim(-.04,1.04);ax.set_ylim(1.06,-.04);ax.axis('off')
    fig.savefig(out,facecolor=fig.get_facecolor());print('wrote',out)

if __name__=='__main__':
    nb=check()
    if len(sys.argv)>1: draw(sys.argv[1],nb)
