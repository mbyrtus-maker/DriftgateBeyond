//@src 16zzzy_coprev.js
// ============================================================ Beyond: the base design, shown (user, 9 Nov 2026)
// "On the base design need to show the selected design (and spin it animation) on the right side." The Company screen's
// Profile tab shows the chosen base design on its right, turning slowly, as a Station (with buildings) or a Depot (toggle),
// in the chosen colour. Drawn by the game's own renderer into a corner of its canvas at the start of a frame, copied to the
// preview, and then painted over by the frame itself, so nothing shows on the main view.
// (user, 10 Nov 2026: "The preview should include the station model as well so depot and station") both at once, side by
// side, each turning, with the company's logo boards on the hull in its colour: a full Depot (level 3) and a Station with its
// five buildings.
const CPV={k:'both'};
function coPrevBox(F){const D=BM_DESIGNS.find(x=>x.id===F.design)||BM_DESIGNS[0];const cvs=(id,lab)=>`<div style="flex:1;min-width:0"><canvas id="${id}" width="440" height="360" style="width:100%;aspect-ratio:11/9;display:block;background:#070b16;border:1px solid var(--line,#1d2740)"></canvas><div class="lab" style="margin:4px 0 0">${lab}</div></div>`;
  return`<div id="coPrevBox" style="float:right;width:460px;max-width:100%;margin:0 0 12px 20px;text-align:center"><div style="display:flex;gap:10px">${cvs('coPrevD','Depot')}${cvs('coPrevS','Station')}</div>
    <div style="margin-top:8px"><b id="coPrevNm" style="color:${coHueCol(F.hue)}">${esc(D.name)}</b></div><div class="note" style="margin:2px 0 8px">${esc(D.note||'')}</div></div>`}
{const o=renderCompany;renderCompany=function(){const r=o.apply(this,arguments);try{if(coTab==='profile'&&S&&!S.unb&&!$('company').hidden){const b=$('coBody');if(b&&!$('coPrevBox'))b.insertAdjacentHTML('afterbegin',coPrevBox(coFormOf(S.player)))}}catch(e){console.error(e)}return r}}
function coPrevRec(F,k){return k==='depot'?{design:F.design,pst:0,dev:{life:0,store:2,prod:2,def:1,armor:1,hangar:0}}:{design:F.design,pst:1,bld:['market','hangar','defence','storage','yard']}}
function coPrevMesh(F,k){return bmBase(coPrevRec(F,k||'station'),'co:'+coHueCol(F.hue)).core}
const _cpp={x:0,y:0,z:0},_cpn={x:0,y:0,z:0},_cpu={x:0,y:0,z:0},_cpq=q0();
function coPrevOne(cv,F,k){const w=cv.width,h=cv.height;if(glc.width<w||glc.height<h)return;const R=coPrevRec(F,k),m=coPrevMesh(F,k);if(!m||!m.data)return;
  if(m._pr==null){let r=0;for(let i=0;i<m.data.length;i+=10)r=Math.max(r,Math.hypot(m.data[i],m.data[i+1],m.data[i+2]));m._pr=r||100}
  const r=m._pr,d=r*2.3,ex=0,ey=r*.75,ez=d,fl=Math.hypot(ex,ey,ez),f=[-ex/fl,-ey/fl,-ez/fl];let s=[f[1]*0-f[2]*1,f[2]*0-f[0]*0,f[0]*1-f[1]*0];const sl=Math.hypot(...s);s=s.map(v=>v/sl);const u=[s[1]*f[2]-s[2]*f[1],s[2]*f[0]-s[0]*f[2],s[0]*f[1]-s[1]*f[0]];
  const Vv=new Float32Array([s[0],u[0],-f[0],0,s[1],u[1],-f[1],0,s[2],u[2],-f[2],0,-(s[0]*ex+s[1]*ey+s[2]*ez),-(u[0]*ex+u[1]*ey+u[2]*ez),f[0]*ex+f[1]*ey+f[2]*ez,1]);
  const fo=1/Math.tan(38*Math.PI/360),n=Math.max(1,r*.05),fa=d*4,Pp=new Float32Array(16);Pp[0]=fo/(w/h);Pp[5]=fo;Pp[10]=(fa+n)/(n-fa);Pp[11]=-1;Pp[14]=2*fa*n/(n-fa);
  const sv=VP.slice();mMul(VP,Pp,Vv);
  try{G.viewport(0,0,w,h);G.enable(G.SCISSOR_TEST);G.scissor(0,0,w,h);G.clearColor(.027,.043,.086,1);G.clear(G.COLOR_BUFFER_BIT|G.DEPTH_BUFFER_BIT);G.enable(G.DEPTH_TEST);G.depthMask(true);G.disable(G.BLEND);
    useMesh();const a=performance.now()/1000*.45,q={x:0,y:Math.sin(a/2),z:0,w:Math.cos(a/2)};mModel(MM,0,0,0,q,1,1,1);drawMesh(m,MM);
    // the logo boards, placed as on a live base (bmLogos)
    try{const M=MDL.i[bmModel(R)];if(M&&M.lg&&M.lg.length&&typeof bmLogoMesh==='function'){const K=R.pst?BM.K.station:BM.K.depot,c=M.c||[0,0,0],hh=M.h||1,li=Number.isInteger(F.logo)&&F.logo>=0&&F.logo<CO_LOGO.length?F.logo:0,lm=bmLogoMesh(li,coHueCol(F.hue));
      for(const L of M.lg){const p=L[0],nn=L[1],sz=L[2]*hh*K;qRot(q,(p[0]*hh+c[0])*K,(p[1]*hh+c[1])*K,(p[2]*hh+c[2])*K,_cpp);qRot(q,nn[0],nn[1],nn[2],_cpn);if(Math.abs(nn[1])>.9)qRot(q,1,0,0,_cpu);else qRot(q,0,1,0,_cpu);
        qLook(_cpn.x,_cpn.y,_cpn.z,_cpu.x,_cpu.y,_cpu.z,_cpq);mModel(MM,_cpp.x,_cpp.y,_cpp.z,_cpq,sz,sz,sz);drawMesh(lm,MM)}}}catch(e){}
    cv.getContext('2d').drawImage(glc,0,glc.height-h,w,h,0,0,w,h)}finally{G.disable(G.SCISSOR_TEST);VP.set(sv)}}
function coPrevDraw(){const co=$('company'),dk=$('dock'),inCo=co&&!co.hidden&&coTab==='profile',inDock=dk&&!dk.hidden&&dockTab==='bco';if(!(inCo||inDock)||!S||!S.player||!bmReady()||!SCN||!SCN.sun)return;
  const F=coFormOf(S.player);for(const[id,k]of[['coPrevD','depot'],['coPrevS','station']]){const cv=$(id);if(cv)coPrevOne(cv,F,k)}}
{const o=draw3D;draw3D=function(){try{coPrevDraw()}catch(e){}return o.apply(this,arguments)}}
