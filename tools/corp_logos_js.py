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
# (8 Nov 2026) the twelve marks for player companies (tools/previews/beyond_cologos.py), written as src/js/16zzz_cologos.js:
# CO_LOGO in order (the company profile stores the index), and coLogoSvg to draw one
from beyond_cologos import CO_LOGOS
co=[{'n':n,'d':path(P)} for _,n,P in CO_LOGOS]
js2=f"""//@src 16zzz_cologos.js
// ============================================================ the player companies' marks (generated: do not edit)
// Written by tools/corp_logos_js.py from tools/previews/beyond_cologos.py (CO_LOGOS). Twelve heraldic marks for player
// companies, in the makers' logo style but apart from every maker's and spare mark. Each: its name and its glyph as an SVG
// path in a [-1,1] box (y down). Your company profile keeps the index.
const CO_LOGO={json.dumps(co,separators=(',',':'),ensure_ascii=False)};
// mark i as inline SVG, size px square, in colour col: the glyph alone, or (board) on a dark board with a rim like a maker's
function coLogoSvg(i,size,col,board){{const L=CO_LOGO[i];if(!L)return'';col=col||'#e8c878';const t=board?`<rect x="-1.08" y="-1.08" width="2.16" height="2.16" rx=".12" fill="#0e121e" stroke="${{col}}" stroke-width=".14"/><path d="${{L.d}}" fill="${{col}}" transform="scale(.74)"/>`:`<path d="${{L.d}}" fill="${{col}}"/>`;
  return`<svg class="mklogo cologo" width="${{size}}" height="${{size}}" viewBox="-1.16 -1.16 2.32 2.32" role="img" aria-label="${{esc(L.n)}}" style="vertical-align:middle;flex:none"><title>${{esc(L.n)}}</title>${{t}}</svg>`}}
"""
out2=os.path.join(R,'..','src','js','16zzz_cologos.js');open(out2,'w').write(js2);print('wrote',os.path.abspath(out2),len(js2),'bytes')
