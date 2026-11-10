//@src 16zzzy_coprev.js
// ============================================================ Beyond: the base design, shown (user, 9 Nov 2026)
// "On the base design need to show the selected design (and spin it animation) on the right side." The Company screen's
// Profile tab shows the chosen base design on its right, turning slowly, as a Station (with buildings) or a Depot (toggle),
// in the chosen colour. Drawn by the game's own renderer into a corner of its canvas at the start of a frame, copied to the
// preview, and then painted over by the frame itself, so nothing shows on the main view.
const CPV={k:'station'};
function coPrevBox(F){const D=BM_DESIGNS.find(x=>x.id===F.design)||BM_DESIGNS[0];
  return`<div id="coPrevBox" style="float:right;width:300px;margin:0 0 12px 20px;text-align:center"><canvas id="coPrev" width="600" height="480" style="width:300px;height:240px;display:block;background:#070b16;border:1px solid var(--line,#1d2740)"></canvas>
    <div style="margin-top:8px"><b id="coPrevNm" style="color:${coHueCol(F.hue)}">${esc(D.name)}</b></div><div class="note" style="margin:2px 0 8px">${esc(D.note||'')}</div>
    <div class="act" style="justify-content:center;gap:6px">${['station','depot'].map(k=>`<button class="cov${CPV.k===k?' on':''}" type="button" data-co="coprevk" data-arg="${k}">${k==='station'?'Station':'Depot'}</button>`).join('')}</div></div>`}
{const o=renderCompany;renderCompany=function(){const r=o.apply(this,arguments);try{if(coTab==='profile'&&S&&!S.unb&&!$('company').hidden){const b=$('coBody');if(b&&!$('coPrevBox'))b.insertAdjacentHTML('afterbegin',coPrevBox(coFormOf(S.player)))}}catch(e){console.error(e)}return r}}
{const o=coClick;coClick=function(act,arg){if(act==='coprevk'){CPV.k=arg==='depot'?'depot':'station';renderCompany();return}return o.apply(this,arguments)}}
function coPrevMesh(F){const R=CPV.k==='depot'?{design:F.design,pst:0}:{design:F.design,pst:1,bld:['market','hangar','defence','storage','yard']};return bmBase(R,'co:'+coHueCol(F.hue)).core}
function coPrevDraw(){const cv=$('coPrev'),co=$('company');if(!cv||!co||co.hidden||coTab!=='profile'||!S||!S.player||!bmReady()||!SCN||!SCN.sun)return;const w=cv.width,h=cv.height;if(glc.width<w||glc.height<h)return;
  const F=coFormOf(S.player),m=coPrevMesh(F);if(!m||!m.data)return;if(m._pr==null){let r=0;for(let i=0;i<m.data.length;i+=10)r=Math.max(r,Math.hypot(m.data[i],m.data[i+1],m.data[i+2]));m._pr=r||100}
  const r=m._pr,d=r*2.3,ex=0,ey=r*.75,ez=d,fl=Math.hypot(ex,ey,ez),f=[-ex/fl,-ey/fl,-ez/fl];let s=[f[1]*0-f[2]*1,f[2]*0-f[0]*0,f[0]*1-f[1]*0];const sl=Math.hypot(...s);s=s.map(v=>v/sl);const u=[s[1]*f[2]-s[2]*f[1],s[2]*f[0]-s[0]*f[2],s[0]*f[1]-s[1]*f[0]];
  const Vv=new Float32Array([s[0],u[0],-f[0],0,s[1],u[1],-f[1],0,s[2],u[2],-f[2],0,-(s[0]*ex+s[1]*ey+s[2]*ez),-(u[0]*ex+u[1]*ey+u[2]*ez),f[0]*ex+f[1]*ey+f[2]*ez,1]);
  const fo=1/Math.tan(38*Math.PI/360),n=Math.max(1,r*.05),fa=d*4,Pp=new Float32Array(16);Pp[0]=fo/(w/h);Pp[5]=fo;Pp[10]=(fa+n)/(n-fa);Pp[11]=-1;Pp[14]=2*fa*n/(n-fa);
  const sv=VP.slice();mMul(VP,Pp,Vv);
  try{G.viewport(0,0,w,h);G.enable(G.SCISSOR_TEST);G.scissor(0,0,w,h);G.clearColor(.027,.043,.086,1);G.clear(G.COLOR_BUFFER_BIT|G.DEPTH_BUFFER_BIT);G.enable(G.DEPTH_TEST);G.depthMask(true);G.disable(G.BLEND);
    useMesh();const a=performance.now()/1000*.45,q={x:0,y:Math.sin(a/2),z:0,w:Math.cos(a/2)};mModel(MM,0,0,0,q,1,1,1);drawMesh(m,MM);
    cv.getContext('2d').drawImage(glc,0,glc.height-h,w,h,0,0,w,h)}finally{G.disable(G.SCISSOR_TEST);VP.set(sv)}}
{const o=draw3D;draw3D=function(){try{coPrevDraw()}catch(e){}return o.apply(this,arguments)}}
