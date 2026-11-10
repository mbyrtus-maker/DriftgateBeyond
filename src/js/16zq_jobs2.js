//@src 16zq_jobs2.js
// ============================================================ the docked Jobs board, minimal (Beyond screens pass, 3 Nov 2026)
// The same jobs, filters, sort and buttons as before (data-act jfil, jsort, jsel and each job's own), drawn quietly:
// the kinds as words with counts, "Sort: Pay ▾"; each row an icon for its kind in its issuer's colour, the title, the
// issuer and the line under it, where, and the pay. The panel: kind and where, the title, who issues it and your standing
// with them, Where / Pays / Paid by, the job's own notes and buttons. At a freeport, a line says whose jobs you can't see
// because your standing is too low. The intel bar above and the convoy section below stay.
const JB_SH={haul:'5,5 25,5 25,25 5,25',mine:'15,2 26,9 27,21 16,28 4,22 3,9',fight:'15,2 24,26 15,20 6,26',scout:'15,3 28,26 2,26',camp:'15,2 27,7 25,20 15,28 5,20 3,7'};
function jbIssuer(j){return j.by?(j.by==='neutral'?'Freeport Compact':j.by==='pirate'?'The Unbound':FACTIONS[j.by]?FACTIONS[j.by].name:sideName(j.by)):null}
// (user, 8 Nov 2026) the board opens on the jobs your hull is for: Fight (escorts are fight jobs) in a fighter or bomber, Mine
// in a miner, Haul in a hauler, Scout in a scout; All and the other kinds are a click away. It defaults again each time you
// dock or change hull; a pick you make holds until then.
let jbDefKey=null,jbDockN=0,JB_BM=false;
// (user, 8 Nov 2026) "Blackmarket jobs should have their own tab under jobs": at a freeport (and at the Rusty Tankard) the
// fixers' runs are on Jobs → Black market, not on the main board; same rows and panel, no kind filter (they are all hauls)
function jbBmHtml(c,P,srcs){const f=jobFilter;JB_BM=true;jobFilter='all';let h='';try{h=jbBoard(c,P,srcs,false,false).replace(/<div class="coviews">[\s\S]*?<\/div>/,'')}finally{JB_BM=false;jobFilter=f}
  return`<p class="note" style="margin:0 0 10px">A fixer's goods, loaded into your hold here and carried into a power's station past its customs. Each run pays by the heat it risks if you're caught. The Company screen's Black Market tab has every offer your contacts have, galaxy-wide.</p>`+(/class="cowrap/.test(h)?h:`<div class="empty">No black-market runs on offer here right now.</div>`)}
{const o=openDock;openDock=function(){jbDockN++;return o.apply(this,arguments)}}
function jbBoard(c,P,srcs,hasOrders,hasMis){const dk=P.cls+'|'+jbDockN;if(!JB_BM&&jbDefKey!==dk){jbDefKey=dk;const f=(typeof jobFit==='function'?jobFit(P.cls):[])[0];jobFilter=f&&JOB_TY[f]?f:'all';jobSel=null}
const all=jobsList(c,P,srcs,hasOrders,hasMis).filter(j=>JB_BM===(String(j.id).startsWith('bmr:')||!!j.bm)),cnt=t=>t==='all'?all.length:all.filter(j=>j.ty===t).length;
  if(jobFilter!=='all'&&!JOB_TY[jobFilter])jobFilter='all';
  const L=all.filter(j=>jobFilter==='all'||j.ty===jobFilter).sort((a,b)=>(jobRank(a,P)-jobRank(b,P))||(b.pin||0)-(a.pin||0)||(!!a.need-!!b.need)||(jobSort==='dist'?(a.hops-b.hops)||(b.payN-a.payN):((b.ok?1:0)-(a.ok?1:0))||(b.payN-a.payN)));
  JOBS_LAST=all;for(const j of L)jobOpenBtns(j);
  if(!L.some(j=>j.id===jobSel))jobSel=L.length?L[0].id:null;const sel=L.find(j=>j.id===jobSel);
  let h=`<div class="coviews">${[['all','All'],...Object.entries(JOB_TY)].map(([k,n])=>`<button class="cov${jobFilter===k?' on':''}" type="button" data-act="jfil" data-arg="${k}" aria-pressed="${jobFilter===k}">${n} ${cnt(k)}</button>`).join('')}</div>`;
  if(!L.length)h+=`<div class="empty">${all.length?'No jobs of this kind right now. Try All.':'No jobs posted here right now. Contracts come every minute or so, and command posts orders with each campaign move.'}</div>`;
  else{h+=`<div class="cowrap jb2"><div class="colist">`;
    // (user, 9 Nov 2026) the sort sits at the top of the list, above the pay the jobs offer
    h+=`<div class="jsorthd" style="display:flex;justify-content:flex-end;padding:0 10px 4px"><button class="cov" type="button" data-act="jsort" data-arg="${jobSort==='pay'?'dist':'pay'}">Sort: ${jobSort==='pay'?'Pay':'Distance'} ▾</button></div>`;
    for(const j of L){const col=j.by?sideCol(j.by):j.pin?'#f0b24a':'#8c91a5',iss=jbIssuer(j),on=j.id===jobSel;
      h+=`<button class="corow jrow2${on?' on':''}${j.need?' dim':''}" type="button" data-act="jsel" data-arg="${j.id}"><svg width="20" height="20" viewBox="0 0 30 30" aria-hidden="true"><polygon points="${JB_SH[j.pin?'camp':j.ty]||JB_SH.haul}" fill="none" stroke="${col}" stroke-width="2.2"/></svg><span style="min-width:0"><b class="cosub" style="font-weight:600">${j.title}</b><span class="note cosub" style="margin:0">${iss?`<span style="color:${col}">${esc(iss)}</span> · `:''}${j.need?`<span style="color:var(--amber)">${esc(j.need)}</span>`:`<span${j.ok?' style="color:#7ad9a7"':''}>${j.sub}</span>`}</span></span><span class="note jw" style="margin:0;white-space:nowrap">${jobIsMine(j)?'<span style="color:#7ad9a7">✓ yours</span> · ':''}${j.where||''}</span><span class="cost mono" style="color:var(--ivory,#ece4cf)">${j.pay}</span></button>`}
    if(c&&c.owner==='neutral'&&!P.sworn&&!S.unb){const hid=FAC_IDS.filter(f=>standOf(f,P)<STAND.dock);if(hid.length)h+=`<div class="coln" style="border:0;color:var(--dim)"><span class="cdot" style="background:#ff9a4a"></span>${hid.map(f=>esc(FACTIONS[f].short)).join(', ')} jobs hidden: your standing is ${standName(Math.min(...hid.map(f=>standOf(f,P))))}</div>`}
    h+=`</div><div class="codet jdet2">`;
    if(sel){const iss=jbIssuer(sel),v=sel.by&&STAND_POW.includes(sel.by)?standOf(sel.by,P):null;
      h+=`<div class="lab">${sel.pin?'Campaign':JOB_TY[sel.ty]}${sel.where?' · '+sel.where:''}</div><div class="ldname" style="align-items:flex-start"><b style="font-size:20px;line-height:1.15">${sel.title}</b></div>`;
      if(iss)h+=`<div style="font-size:13px;color:${sideCol(sel.by)};margin:0 0 10px">Issued by ${esc(iss)}${v!=null?` · you are ${standName(v)} (${v>0?'+':''}${Math.round(v)})`:''}</div>`;
      h+=coKV([sel.where?['Where',esc(sel.where)+(sel.sid&&DEF[sel.sid]?` · ${esc(DEF[sel.sid].name)}`:'')]:null,['Pays',`<b class="amber">${sel.pay}</b>`],iss&&sel.by!=='pirate'?['Paid by',`${esc(iss)}'s treasury`]:null]);
      h+=`<div style="margin-top:12px">${sel.need?`<p class="note" style="color:var(--amber);margin:0 0 8px">${esc(sel.need)}</p>`:''}${sel.detail?sel.detail():''}</div>`;
      if(sel.fix||sel.btn||sel.btn2||sel.btn3)h+=`<div class="act" style="margin-top:14px;flex-wrap:wrap;justify-content:flex-start">${sel.fix?`<button class="btn pri" style="max-width:100%;white-space:normal;text-align:left" type="button" data-act="${sel.fix[0]}" data-arg="${sel.fix[1]}">${esc(sel.fix[2])}</button>`:''}${sel.btn?`<button class="btn${sel.fix?'':' pri'}" type="button" data-act="${sel.btn[0]}" data-arg="${sel.btn[1]}">${sel.btn[2]}</button>`:''}${sel.btn3?`<button class="btn" type="button" data-act="${sel.btn3[0]}" data-arg="${sel.btn3[1]}">${sel.btn3[2]}</button>`:''}${sel.btn2?`<button class="btn" type="button" data-act="${sel.btn2[0]}" data-arg="${sel.btn2[1]}">${sel.btn2[2]}</button>`:''}</div>`}
    h+=`</div></div>`}
  if(hasOrders)h+=convoyHtml(c,P);
  return h}
{const o=jobsHtml;jobsHtml=function(c,P,srcs,hasOrders,hasMis){if(!S||S.unb)return o.apply(this,arguments);let bar='';try{bar=typeof intelBarHtml==='function'?intelBarHtml(c,P):''}catch(e){}return bar+jbBoard(c,P,srcs,hasOrders,hasMis)}}
