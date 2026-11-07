# Writes the makers' logos and accents into the game (src/js/16zzz_logos.js) from tools/previews/beyond_corp.py, so the
# approved art and the game can't drift apart. Run after changing LOGOS, SPARE_LOGOS or MAKERS there, then build.
# Usage: python3 tools/corp_logos_js.py
import os,sys,json
R=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,os.path.join(R,'previews'))
from beyond_corp import LOGOS,SPARE_LOGOS,MAKERS,logo_names
def ccw(P):
    a=sum(P[i][0]*P[(i+1)%len(P)][1]-P[(i+1)%len(P)][0]*P[i][1] for i in range(len(P)));return P if a>0 else P[::-1]
def path(polys):
    # SVG path in a [-1,1] box with y down; every piece wound the same way so overlapping pieces fill as one (nonzero rule)
    out=[]
    for P in polys:
        P=ccw([(float(x),float(y)) for x,y in P]);out.append('M'+' '.join('%g,%g'%(round(x,3),round(-y,3)) for x,y in P)+'Z')
    return ''.join(out)
N=logo_names()
lo={k:{'n':N[k],'d':path(v)} for k,v in LOGOS.items()}
acc={m:c for m,_,_,c in MAKERS}
js=f"""//@src 16zzz_logos.js
// ============================================================ the makers' logos and accents (generated: do not edit)
// Written by tools/corp_logos_js.py from tools/previews/beyond_corp.py (LOGOS, SPARE_LOGOS, MAKERS), the approved art.
// MK_LOGO: each logo's name and its glyph as an SVG path in a [-1,1] box (y down). The twelve makers' own marks are keyed by
// the maker; MK_SPARE are the spare marks a reborn maker takes. MK_ACC: each maker's accent, a shade of its home's colour.
const MK_LOGO={json.dumps(lo,separators=(',',':'),ensure_ascii=False)};
const MK_SPARE={json.dumps(list(SPARE_LOGOS))};
const MK_ACC={json.dumps(acc)};
"""
out=os.path.join(R,'..','src','js','16zzz_logos.js');open(out,'w').write(js);print('wrote',os.path.abspath(out),len(js),'bytes')
