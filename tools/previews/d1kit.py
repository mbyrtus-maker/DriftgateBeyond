# Loads Driftgate 1's model builders (tools/build_models.py) without running its packing step, so preview code can reuse
# the Kenney kit parts and Driftgate 1's own hull models as a baseline. Models come back as a Mesh-like object
# (T: triangles, R: (role, shade)), normalised to nose +z, about 2 long, centred.
import os,sys,numpy as np
TOOLS=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.insert(0,TOOLS)
_src=open(os.path.join(TOOLS,'build_models.py')).read()
_src=_src[:_src.index('\nFIT=')]
_cwd=os.getcwd();os.chdir(TOOLS);NS={'__file__':os.path.join(TOOLS,'build_models.py')};exec(compile(_src,'build_models.py','exec'),NS);os.chdir(_cwd)
class K:
    def __init__(s,T,R):s.T=list(T);s.R=list(R)
def norm(P,length=2.0):
    P=np.array(P,float).reshape(-1,3,3);lo=P.reshape(-1,3).min(0);hi=P.reshape(-1,3).max(0)
    c=(lo+hi)/2;k=length/max(hi[2]-lo[2],1e-6);return (P-c)*k
def d1(name,length=2.0):
    # one of Driftgate 1's packed models by name ('skiff', 'prospector', 'courier'...), normalised
    kind,fn=NS['MODELS'][name];P,N,R=fn()
    return K(norm(P,length),R)
def part(parts,length=None,scale=1.0):
    # a Kenney kit assembly: [(model, (x,y,z), yaw, scale)]; returns triangles in kit units times scale
    P,N,R=NS['comp'](parts);P=np.array(P,float).reshape(-1,3,3)*scale
    return K(P,R)
def place(M,k,offset=(0,0,0),scale=1.0,about=False):
    # add a kit model's triangles into a Mesh at an offset (about=True turns it to face the other way)
    P=np.array(k.T,float)
    if about:P=P*np.array([-1,1,-1])
    for t,r in zip(P*scale+np.array(offset),k.R):M.T.append(t);M.R.append(r)
