//@src 16zw_ports.js
// ============================================================ docking ports you can see (Beyond, 3 Nov 2026)
// Within 4 km of a station, depot or outpost, each docking port is marked in flight: a pulsing ring on the port, green where
// you may dock and red where you may not, with a line of approach chevrons running out from it the way you come in. The port
// nearest you is labelled (DOCK, its distance, and "press E" once you're close enough; NO DOCKING where you're refused).
// A base with no arm ports (you set down over its hangar) shows one port above it.
const PRT={show:4000,guide:[70,140,210,280],ring:26};
function prtList(E){const L=portsW(E);if(L&&L.length)return L;const u=dockUp(E),R=(E.r||95)+30;return[{x:E.x+u.x*R,y:E.y+u.y*R,z:E.z+u.z*R,dx:u.x,dy:u.y,dz:u.z,top:1}]}
function prtDraw(c){if(!W||!W.player||S.player.docked||W.dead||W.docking||W.bridge||W.gunseat)return;const p=W.player,t=W.t;
  for(const E of W.ents){if(E.type!=='station'&&E.type!=='outpost')continue;if(E.type==='station'&&E.fac==='brood')continue;const dE=d3(E,p);if(dE>PRT.show)continue;
    let ok=false;try{ok=canDock(E)}catch(e){}const col=ok?'122,217,167':'255,93,79',L=prtList(E);let near=-1,nd=1e18;L.forEach((q,i)=>{const d=(q.x-p.x)**2+(q.y-p.y)**2+(q.z-p.z)**2;if(d<nd){nd=d;near=i}});
    const fade=Math.min(1,(PRT.show-dE)/800);
    L.forEach((q,i)=>{const P=proj(q.x,q.y,q.z);if(P.behind||P.x<-40||P.y<-40||P.x>VW+40||P.y>VH+40)return;const isN=i===near,a=(isN?.95:.55)*fade,r=Math.max(5,Math.min(28,projR(P.d,PRT.ring)));const px=P.x,py=P.y,pd=P.d;
      // approach chevrons running out from the port
      if(ok||isN){let prev=null;for(const k of PRT.guide){const Q=proj(q.x+q.dx*k,q.y+q.dy*k,q.z+q.dz*k);if(Q.behind){prev=null;continue}const cx=Q.x,cy=Q.y,s=Math.max(2.5,Math.min(9,projR(Q.d,9))),ph=(t*1.6-k/PRT.guide[PRT.guide.length-1])%1;
          c.fillStyle=`rgba(${col},${(.25+.6*(1-((ph+1)%1)))*a})`;c.beginPath();c.arc(cx,cy,s*.55,0,TAU);c.fill();prev=[cx,cy]}}
      c.lineWidth=isN?2:1.4;c.strokeStyle=`rgba(${col},${a})`;c.beginPath();c.arc(px,py,r,0,TAU);c.stroke();
      const pr=r+3+(r*.6)*((t*1.2+i*.37)%1);c.strokeStyle=`rgba(${col},${a*(1-((t*1.2+i*.37)%1))*.8})`;c.beginPath();c.arc(px,py,pr,0,TAU);c.stroke();
      c.fillStyle=`rgba(${col},${a})`;c.beginPath();c.arc(px,py,Math.max(1.8,r*.18),0,TAU);c.fill();
      if(isN){const inR=dE<(E.type==='outpost'?(E.r||95)+(E.r>95?260:195):290);c.font='700 11px "Saira Semi Condensed",sans-serif';c.textAlign='left';c.lineJoin='round';c.lineWidth=3;c.strokeStyle='rgba(4,8,16,.85)';
        const lab=ok?(inR?`DOCK · PRESS ${typeof actKey==='function'?actKey().toUpperCase():'E'}`:`DOCK · ${pd>=1000?(pd/1000).toFixed(1)+' km':Math.round(pd)+' m'}`):'NO DOCKING';c.strokeText(lab,px+r*.7+6,py-r*.7-4);c.fillStyle=`rgba(${col},1)`;c.fillText(lab,px+r*.7+6,py-r*.7-4)}})}}
{const o=drawOverlay;drawOverlay=function(){const r=o.apply(this,arguments);try{prtDraw(octx)}catch(e){}return r}}
// ---- the ports' art (user, 3 Nov 2026): a docking collar at every port, a lit ring inside it, guide lights round it and a line
// of approach lights running out from it; tinted red where you may not dock. Drawn with the station or outpost.
let PRT_MESH=null;
function prtMesh(){if(PRT_MESH)return PRT_MESH;const g=new GB(),H=[.52,.55,.6],D=[.22,.24,.28],GR=[.48,.92,.66],AM=[1,.76,.36];
  g.set(0,0,0,QX90).torus(15,2.4,28,6,H,0);g.set(0,0,-1.5,QX90).torus(15.5,1.2,28,4,D,0);g.set(0,0,1.2,QX90).torus(11.5,.7,28,4,GR,1);
  for(const[a,b]of[[1,0],[-1,0],[0,1],[0,-1]]){g.set(a*18.5,b*18.5,0).box(2.6,2.6,2.6,AM,1)}
  for(const z of[22,38,54,70])for(const s of[-1,1]){g.set(s*9,0,z).box(1.6,1.6,1.6,GR,1)}
  return PRT_MESH=g.upload()}
{const o=drawWorks;drawWorks=function(t){const r=o.apply(this,arguments);try{if(!W||!MDL.ready||S.unb&&false)return r;const p=W.player;
  for(const E of[W.stationEnt,W.outpostEnt]){if(!E||(E.type==='station'&&E.fac==='brood'))continue;if(p&&d3(E,p)>6000)continue;let ok=true;try{ok=canDock(E)}catch(e){}
    const L=portsW(E);if(!L||!L.length)continue;const m=prtMesh();for(const q of L){qLook(q.dx,q.dy,q.dz,0,1,0,_qs);mModel(MM,q.x+q.dx*3,q.y+q.dy*3,q.z+q.dz*3,_qs,1,1,1);drawMesh(m,MM,ok?ONE3:[1,.42,.36])}}}catch(e){}return r}}
// ---- turrets never sit on a docking port: the outermost hull point in each turret's direction that is clear of the ports
{const o=stSurf;stSurf=function(name,size,n){const key='px:'+name+':'+size+':'+n;stSurf.c=stSurf.c||{};if(stSurf.c[key])return stSurf.c[key];const PT=mdlPorts(name);if(!PT||!PT.length)return o.apply(this,arguments);
  const M=MDL.i[name],P=new Int16Array(MDL.b,M.o,M.n*9),h=(M.h||1)/32767,s=size/(M.h||1),ex=size*.3,ps=PT.map(v=>v.map(x=>x*size/(M.s||size))),out=[];
  for(let i=0;i<n;i++){const a=i/n*TAU+.4,dx=Math.cos(a),dy=i%2?.55:-.25,dz=Math.sin(a),l=Math.hypot(dx,dy,dz);let best=null,bd=-1e9;
    for(let t=0;t<M.n;t++){const q=t*9;const x=(P[q]+P[q+3]+P[q+6])/3*h*s,y=(P[q+1]+P[q+4]+P[q+7])/3*h*s,z=(P[q+2]+P[q+5]+P[q+8])/3*h*s;if(ps.some(v=>Math.hypot(v[0]-x,v[1]-y,v[2]-z)<ex))continue;const d=(x*dx+y*dy+z*dz)/l;if(d>bd){bd=d;best=[x,y,z]}}
    out.push(best||[0,size*.3,0])}return stSurf.c[key]=out}}
