# Driftgate Beyond: a check of the live turret seats on a player company's bases (10 Nov 2026). For every design's Depot 1-3
# and Station core (with every building on every hardpoint), each seat the game uses (position, outward normal) is tested:
#   gap    how far the seat is off the hull along its normal, in metres in game (+ floats above, - sunk in)
#   tilt   the angle between the seat's normal and the hull's own normal where it lands (degrees)
#   hits   model faces inside the turret's own space: a drum round the seat's normal, as wide as the turret's turntable and
#          as tall as the turret (anything there cuts through the drawn turret)
#   skirt  the plinth's height from the hull's lowest point under its rim to its deck (m); rim: how many of 12 rim rays find hull
# Usage: python3 tools/previews/base_seats_check.py [DESIGN...]
import math,sys,os
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,HERE)
import beyond_stations as BS
import beyond_base_designs as BD
K={'depot':48.0,'station':40.0}
TS=1.15                       # the turret's scale on a model-seated base (12_render.js draw3D)
LIFT=13.2*TS                  # the turntable's underside below the turret's origin (turretMesh: base ring to y -13.2)
RAD=11.0*TS                   # the turntable's radius (10.6) with a little room
TOP=LIFT+7.0*TS               # the head's roof above the turntable's underside
def tris(M):return np.array([np.array(t,float) for t in M.T]).reshape(-1,3,3)
def ray(T,o,d):
    # nearest hit distance of the ray o + t d (t>0) on triangles T, or None
    e1=T[:,1]-T[:,0];e2=T[:,2]-T[:,0];p=np.cross(d,e2);det=(e1*p).sum(1);ok=np.abs(det)>1e-12;inv=np.where(ok,1/np.where(ok,det,1),0)
    s=o-T[:,0];u=(s*p).sum(1)*inv;q=np.cross(s,e1);v=(q@d)*inv;t=(e2*q).sum(1)*inv
    m=ok&(u>=0)&(v>=0)&(u+v<=1)&(t>1e-6)
    if not m.any():return None,None
    i=np.argmin(np.where(m,t,np.inf));n=np.cross(e1[i],e2[i]);n/=np.linalg.norm(n)+1e-12
    return t[i],(n if n@d<0 else -n)
def samples(T):
    c=T.mean(1);return np.concatenate([T.reshape(-1,3),c,(T[:,0]+T[:,1])/2,(T[:,1]+T[:,2])/2,(T[:,2]+T[:,0])/2])
def check(M,seats,kind,skip=None):
    T=tris(M);k=K[kind];S=samples(T);out=[]
    for p,n in seats:
        p=np.array(p,float);n=np.array(n,float);n/=np.linalg.norm(n)
        t,hn=ray(T,p+n*(60/k),-n);gap=(t-60/k)*-1*k if t is not None else None
        tilt=math.degrees(math.acos(max(-1,min(1,float(hn@n))))) if hn is not None else None
        base=p if t is None else p+n*(60/k-t)    # the hull point under the seat
        r=S-base;h=r@n;rad=np.linalg.norm(r-np.outer(h,n),axis=1)
        hit=int(((h*k>2.0)&(h*k<TOP)&(rad*k<RAD)).sum())
        out.append((gap,tilt,hit))
    return out
def fmt(r):
    g,t,h=r;return f"gap {'  none' if g is None else '%+6.1f'%g} m  tilt {' none' if t is None else '%4.0f'%t}°  hits {h:4d}"
def all_buildings(core):
    M=core
    for a in BS.HP_A:
        for fn in (BS.shipyard,BS.ext_storage,BS.defence_platform,BS.hangar,BS.forge,BS.market_wing):BS.put(M,fn(),(math.cos(a)*BS.HP_R,BS.HP_Y,math.sin(a)*BS.HP_R),BS.outward(a),BS.HP_S if hasattr(BS,'HP_S') else .8)
    return M
def run(designs):
    bad=0
    for n in designs:
        rows=[('depot%d'%lv,BD._DEP[n](lv),BD.depot_model(n,lv),BD._DS[n],'depot') for lv in (1,2,3)]
        rows.append(('station',BD._CORE[n](),all_buildings(BD.core_model(n)),BD._CS[n],'station'))
        for lab,raw,full,seats,kind in rows:
            k=K[kind];T=tris(raw);S=BD.snap(raw,seats[:BD.NLIVE],kind);Tf=tris(full);P=samples(Tf)
            for i,(top,bot,nn) in enumerate(S):
                t,hn=ray(T,top+nn*.001,-nn);gap=None if t is None else t*k
                tilt=None if hn is None else math.degrees(math.acos(max(-1,min(1,float(hn@nn)))))
                r=P-top;h=r@nn;rad=np.linalg.norm(r-np.outer(h,nn),axis=1)
                hit=int(((h*k>2.0)&(h*k<TOP)&(rad*k<RAD)).sum());skirt=float((top-bot)@nn)*k
                flag=gap is None or gap>6 or skirt>40 or hit>0;bad+=flag
                print(f"design {n} {lab:8s} seat {i}: centre {'  none' if gap is None else '%5.1f'%gap} m  skirt {skirt:5.1f} m  tilt {' none' if tilt is None else '%3.0f'%tilt}°  hits {hit:4d}{'   <<' if flag else ''}",flush=True)
            # (10 Nov 2026) each docking port sits on the hull (a collar's face) and its approach lane (straight out from the
            # base's axis, 260 m) keeps clear of the live turrets
            for j,pp in enumerate(BD.ports(n,kind)):
                dd=np.array([pp[0],0,pp[2]]);dd/=np.linalg.norm(dd);pw=pp*k
                dmin=min(float(BD._dist_seg(np.array([top*k+nn*BD.TU_LIFT]),pw,pw+dd*260)[0]) for top,_,nn in S)
                t,_=ray(T,pp+dd*.5,-dd);back=None if t is None else (t-.5)*k
                flag=dmin<40 or back is None or back>12;bad+=flag
                print(f"design {n} {lab:8s} port {j}: nearest turret {dmin:5.0f} m from its lane, hull {'none' if back is None else '%.0f m'%back} behind it{'   <<' if flag else ''}",flush=True)
    print('seats or ports out of place:',bad)
    return bad
if __name__=='__main__':
    run([int(a) for a in sys.argv[1:]] or range(1,7))
