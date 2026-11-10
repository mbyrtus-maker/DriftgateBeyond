//@src 16x3_baselogos.js
// ============================================================ your company's logo on your bases (10 Nov 2026)
// The user: "The company logos should show somewhere on the company depots and stations." Every player Depot and Station
// carries its owner's mark (CO_LOGO, the profile's logo) on boards lying on its hull, in the company's colour (coCol) and
// lit, so it reads from normal flying distance. The pack gives each base model its board spots ('lg': centre, outward normal,
// half-size; tools/previews/beyond_base_designs.logo_spots): two on a Depot, three on a Station, each on a nearly flat stretch
// of hull with nothing in front of it, clear of the turrets, the docking lanes and the modules, facing well apart. The glyph is rasterised once per logo (a canvas, Path2D) into lit tiles on a dark board
// with a rim, one mesh per logo and colour, so two companies' bases differ. Looks only.
BM.lgN=40
// the pilot who owns a base record
function bmOwnerP(R){const k=R&&R.pid||'me';if(k==='me')return S.player;if(S.pilots&&S.pilots[k])return S.pilots[k];return pkeyOf(S.player)===k?S.player:null}
function bmLogoOf(R){const P=bmOwnerP(R),i=P&&P.co&&P.co.logo;return Number.isInteger(i)&&i>=0&&i<CO_LOGO.length?i:0}
// the glyph's filled cells on an N x N grid, merged into rectangles [x0,y0,x1,y1] in the [-1,1] box (y down)
function bmLogoRects(i){bmLogoRects.c=bmLogoRects.c||{};if(bmLogoRects.c[i])return bmLogoRects.c[i];const N=BM.lgN,out=[];
  try{const cv=document.createElement('canvas');cv.width=cv.height=N;const x=cv.getContext('2d');x.setTransform(N/2,0,0,N/2,N/2,N/2);x.fillStyle='#fff';x.fill(new Path2D(CO_LOGO[i].d));
    const D=x.getImageData(0,0,N,N).data,on=(cx,cy)=>D[(cy*N+cx)*4+3]>110,used=new Uint8Array(N*N);
    for(let cy=0;cy<N;cy++)for(let cx=0;cx<N;cx++){if(used[cy*N+cx]||!on(cx,cy))continue;let w=1;while(cx+w<N&&on(cx+w,cy)&&!used[cy*N+cx+w])w++;
      let h=1;for(;cy+h<N;h++){let ok=true;for(let k=0;k<w;k++)if(!on(cx+k,cy+h)||used[(cy+h)*N+cx+k]){ok=false;break}if(!ok)break}
      for(let j=0;j<h;j++)for(let k=0;k<w;k++)used[(cy+j)*N+cx+k]=1;out.push([cx/N*2-1,cy/N*2-1,(cx+w)/N*2-1,(cy+h)/N*2-1])}}catch(err){}
  return bmLogoRects.c[i]=out}
// a board one unit in half-size facing +z (+y up): a dark plate, a rim in the colour, the glyph in lit tiles
function bmLogoMesh(i,col){const key='bmlg'+i+col;if(MESH[key])return MESH[key];const g=new GB(),F=hexRGB(col),B=[.055,.065,.1],k=.74;
  g.set(0,0,-.05).box(2.16,2.16,.1,B);for(const s of[-1,1]){g.set(s*1.04,0,.01).box(.1,2.18,.06,F,.55);g.set(0,s*1.04,.01).box(2.18,.1,.06,F,.55)}
  for(const r of bmLogoRects(i)){const w=(r[2]-r[0])*k,h=(r[3]-r[1])*k;g.set((r[0]+r[2])/2*k,-(r[1]+r[3])/2*k,.02).box(w,h,.04,F,.9)}
  return MESH[key]=g.upload()}
const _blp={x:0,y:0,z:0},_bln={x:0,y:0,z:0},_blq=q0();
function bmLogos(){const SE=W&&W.stationEnt,R=SE&&SE.rec;if(!SE||!bmOwned(R)||!bmReady()||!inView(SE.x,SE.y,SE.z,900))return;const M=MDL.i[bmModel(R)];if(!M||!M.lg||!M.lg.length)return;
  const K=R.pst?BM.K.station:BM.K.depot,c=M.c||[0,0,0],h=M.h||1,m=bmLogoMesh(bmLogoOf(R),coCol(R.pid||'me')),k=SE.sc||1;
  for(const L of M.lg){const p=L[0],n=L[1],s=L[2]*h*K*k;qRot(SE.q,(p[0]*h+c[0])*K*k,(p[1]*h+c[1])*K*k,(p[2]*h+c[2])*K*k,_blp);qRot(SE.q,n[0],n[1],n[2],_bln);if(Math.abs(n[1])>.9)qRot(SE.q,1,0,0,_u);else qRot(SE.q,0,1,0,_u);
    qLook(_bln.x,_bln.y,_bln.z,_u.x,_u.y,_u.z,_blq);mModel(MM,SE.x+_blp.x,SE.y+_blp.y,SE.z+_blp.z,_blq,s,s,s);drawMesh(m,MM)}}
{const o=drawWorks;drawWorks=function(t){const r=o.apply(this,arguments);try{bmLogos()}catch(err){}return r}}
