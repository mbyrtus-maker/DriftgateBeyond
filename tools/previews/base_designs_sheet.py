# Driftgate Beyond: the company profile's art for review (8 Nov 2026): the six base designs (Depot 1/2/3 and the Station core
# with three buildings on its hardpoints) in a sample player hue, and the twelve player-company marks as the game draws them
# (coLogoSvg from src/js/16zzz_cologos.js), with the makers' and spare marks beside them for comparison.
# Usage: python3 tools/previews/base_designs_sheet.py OUT.png [render|shot]
#   render: the model pictures only (no browser); shot: the page only (Chromium, deviceScaleFactor 2); default both.
import math,os,sys,json
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,HERE)
import render_beyond as RB
from render_beyond import render,rot
import beyond_stations as BS
import beyond_base_designs as BD
HUE='#4a8cff'
RB.FAC_HEX['player']=HUE;RB.HULL['player']=[.57,.58,.6]
class _M:pass
def shot(M,W,H,ppu,yaw=math.radians(-35),pitch=math.radians(24)):
    # one scale for a whole column, centred on the model's bounding box as seen
    T=np.array(M.T,float);R=rot(yaw,pitch);P=T.reshape(-1,3)@R.T;lo,hi=P.min(0),P.max(0);c=((lo+hi)/2)@R
    N=_M();N.T=list(T-c);N.R=M.R;return render(N,'player',yaw,pitch,W,H,ppu)
def station(core):
    M=core
    for a,fn in zip(BS.HP_A,[BS.shipyard,BS.ext_storage,BS.market_wing]):BS.put(M,fn(),(math.cos(a)*BS.HP_R,BS.HP_Y,math.sin(a)*BS.HP_R),BS.outward(a),.8)
    return M
ROWS=[(1,'Company standard','a drum hub with a docking arm; the Station a tall spine and habitat ring',BS.depot,lambda:BS.station_core('standard',True))]+[(n,name,note,dep,core) for n,name,note,dep,core,_,_ in BD.DESIGNS]
import tempfile
WORK=os.environ.get('DG_SHEET_TMP',os.path.join(tempfile.gettempdir(),'dg_base_designs'))   # the pictures and the page (not kept)
OUTD=os.path.join(WORK,'base_designs_parts')
DW,SW,CH=300,520,300
def renders():
    os.makedirs(OUTD,exist_ok=True)
    for n,name,note,dep,core in ROWS:
        for lv in (1,2,3):
            im=shot(dep(lv),DW*2,CH*2,2*CH/2/3.3);im.save(os.path.join(OUTD,'d%d_depot%d.png'%(n,lv)));print(n,lv,flush=True)
        im=shot(station(core()),SW*2,CH*2,2*CH/2/5.8);im.save(os.path.join(OUTD,'d%d_station.png'%n));print(n,'station',flush=True)
def page():
    R=os.path.join(HERE,'..','..','src','js')
    co=open(os.path.join(R,'16zzz_cologos.js')).read();mk=open(os.path.join(R,'16zzz_logos.js')).read()
    rows=''.join(f"""<div class="row"><div class="lab"><b>{n}. {name}</b><span>{note}</span><code>by_{'d%d_'%n if n>1 else ''}depot1-3 · by_{'d%d_'%n if n>1 else ''}core</code></div>
      {''.join(f'<figure><img src="base_designs_parts/d{n}_depot{lv}.png" width="{DW}" height="{CH}"><figcaption>Depot {lv}</figcaption></figure>' for lv in (1,2,3))}
      <figure><img src="base_designs_parts/d{n}_station.png" width="{SW}" height="{CH}"><figcaption>Station core + shipyard, storage, market wing</figcaption></figure></div>""" for n,name,note,_,_ in ROWS)
    html=f"""<!doctype html><meta charset="utf-8"><style>
body{{margin:0;background:#0a0d14;color:#dfe3ea;font:13px/1.35 DejaVu Sans,sans-serif;width:{220+3*DW+SW+40}px;padding:20px 20px 30px}}
h1{{font-size:24px;margin:0 0 4px}} h2{{font-size:18px;margin:26px 0 6px;color:{HUE}}} .sub{{color:#8c96a8;margin:0 0 10px}}
.row{{display:flex;align-items:stretch;border-top:1px solid #1d2433}} .lab{{width:220px;flex:none;padding:14px 10px 0 0;border-left:4px solid {HUE};padding-left:10px}}
.lab b{{display:block;font-size:17px;color:{HUE}}} .lab span{{display:block;color:#a9b1c0;margin:6px 0}} .lab code{{color:#6f7a8c;font-size:11px}}
figure{{margin:0;position:relative}} figcaption{{position:absolute;left:10px;bottom:6px;color:#7f8a9c;font-size:11px}}
.logos{{display:grid;grid-template-columns:repeat(6,1fr);gap:10px}} .lg{{background:#0f1420;border:1px solid #1d2433;border-radius:8px;padding:10px;text-align:center}}
.lg .n{{color:#c6ccd8;margin-top:6px}} .lg .k{{color:#6f7a8c;font-size:11px}} .sm{{display:flex;gap:8px;justify-content:center;align-items:center;margin-top:6px}}
.cmp{{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}} .cmp div{{text-align:center;width:74px;color:#6f7a8c;font-size:10px}}
</style><body><h1>Driftgate Beyond · Your company: base designs and marks</h1>
<p class="sub">Six designs for your Depots and Stations (looks only; the same five hardpoints, so every building attaches unchanged) · painted in a sample player hue {HUE} · Depots at one scale, Stations at another (in game a Depot draws at 48, a Station core at 32 units per model unit)</p>
{rows}
<h2>Twelve marks for player companies</h2><p class="sub">As the game draws them (coLogoSvg): on a board at 96 px, plain at 40 px, and at the 20 px icon size, in the sample hue and two others</p>
<div class="logos" id="co"></div>
<h2 style="color:#8c96a8">For comparison: the makers' marks and the spare marks (not for players)</h2><div class="cmp" id="mk"></div>
<script>const esc=s=>String(s).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));</script>
<script>{co}</script><script>{mk}</script>
<script>
const H=['{HUE}','#e05a8a','#d8e070'];
document.getElementById('co').innerHTML=CO_LOGO.map((L,i)=>`<div class="lg">${{coLogoSvg(i,96,H[0],true)}}<div class="sm">${{coLogoSvg(i,40,H[0])}}${{coLogoSvg(i,20,H[0],true)}}${{coLogoSvg(i,20,H[1],true)}}${{coLogoSvg(i,20,H[2],true)}}</div><div class="n">${{esc(L.n)}}</div><div class="k">CO_LOGO[${{i}}]</div></div>`).join('');
document.getElementById('mk').innerHTML=Object.keys(MK_LOGO).map(k=>`<div>${{logoSvg(k,'#8a93a6',40,true)}}<br>${{esc(MK_LOGO[k].n)}}</div>`).join('');
function logoSvg(key,col,px,board){{const L=MK_LOGO[key];return`<svg width="${{px}}" height="${{px}}" viewBox="-1.16 -1.16 2.32 2.32"><rect x="-1.08" y="-1.08" width="2.16" height="2.16" rx=".12" fill="#0e121e" stroke="${{col}}" stroke-width=".14"/><path d="${{L.d}}" fill="${{col}}" transform="scale(.74)"/></svg>`}}
</script></body>"""
    p=os.path.join(WORK,'base_designs_sheet.html');open(p,'w').write(html);return p
def screenshot(html,out):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b=pw.chromium.launch();pg=b.new_page(viewport={'width':220+3*DW+SW+80,'height':900},device_scale_factor=2)
        pg.goto('file://'+html);pg.wait_for_timeout(500);pg.screenshot(path=out,full_page=True);b.close()
    print('wrote',out)
if __name__=='__main__':
    out=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.join(HERE,'beyond_base_designs.png'));mode=sys.argv[2] if len(sys.argv)>2 else 'both'
    if mode in ('both','render'):renders()
    if mode in ('both','shot'):screenshot(page(),out)
