//@src 16zj_icons.js
// ============================================================ goods icons and colours (Beyond screens pass, 3 Nov 2026)
// Every good shows a shape by kind and a colour (user, 3 Nov): ore a hexagon in its own colour; components a square in the
// colour of the most valuable ore they contain; weapons a dart in reds; utility parts a plus in yellows; missiles and torpedoes
// a rocket and charges an octagon in magentas; machine-gun rounds a bullet; cash-only contraband a violet diamond.
// sw(k), the old diamond swatch, now draws the icon; chip() gains it too.
const GI_SH={ore:'15,2 26,9 27,21 16,28 4,22 3,9',comp:'5,5 25,5 25,25 5,25',wpn:'15,2 24,26 15,20 6,26',util:'11,3 19,3 19,11 27,11 27,19 19,19 19,27 11,27 11,19 3,19 3,11 11,11',
  msl:'15,2 19,9 19,22 23,28 7,28 11,22 11,9',chg:'10,3 20,3 27,10 27,20 20,27 10,27 3,20 3,10',rnd:'15,2 19,8 19,28 11,28 11,8',con:'15,3 27,15 15,27 3,15'};
const GI_PART={gun:'#ff6b6b',laser:'#ff9aa8',missile:'#ff8a7a',torpedo:'#ff8a7a',charge:'#e2505f',mlaser:'#ff7f6b',jammer:'#c44a6a',cargo:'#f5e663',scanner:'#f5e663',land:'#fff09a',hide:'#d9c43a',hook:'#d9c43a',bdev:'#f5e663',lrack:'#f5e663'};
const GI_C={};
function giKind(k){const I=ITEMS[k]||{};if(RAWS.includes(k)||k==='rift')return'ore';if(I.cash)return'con';if(I.part)return WPN[I.part]?'wpn':'util';if(MUNITIONS.has(k))return'msl';if(k==='ammo'||k==='rounds')return'rnd';if(k==='charges'||k==='chg')return'chg';return'comp'}
function giCol(k){if(GI_C[k])return GI_C[k];const I=ITEMS[k]||{},kd=giKind(k);let c=I.col||'#8c91a5';
  if(kd==='comp'){try{const v=comp(k);let best=null,bv=-1;for(const e of RAWS)if(v[e]>0&&ITEMS[e].base>bv){bv=ITEMS[e].base;best=e}if(best)c=ITEMS[best].col}catch(e){}}
  else if(kd==='wpn'||kd==='util')c=GI_PART[I.part]||c;else if(kd==='msl')c='#ff6fcf';else if(kd==='chg')c='#d65aa8';else if(kd==='rnd')c='#e86ac0';else if(kd==='con'&&k!=='rift')c='#b07cff';
  return GI_C[k]=c}
function gIcon(k,sz){sz=sz||13;const c=giCol(k),p=GI_SH[giKind(k)];return`<svg class="gi" width="${sz}" height="${sz}" viewBox="0 0 30 30" aria-hidden="true"><polygon points="${p}" fill="${c}33" stroke="${c}" stroke-width="2.5"/></svg>`}
sw=function(k){return ITEMS[k]?gIcon(k):''};
{const o=chip;chip=function(k,need,have){const r=o.apply(this,arguments);return ITEMS[k]?r.replace(/^(<span class="req [^"]*">)/,'$1'+gIcon(k,11)):r}}
