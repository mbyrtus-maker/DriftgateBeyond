//@src 16zzzt_tags.js
// ============================================================ Beyond: pilot tags (user, 9 Nov 2026)
// "On pilot tags rather than saying 'Independent' just use [I] [H] [O] [V] [U] [B] as tags." Ships in the contacts list (and
// an independent's name wherever it shows) carry a one-letter tag for their side: [I] independents (and the freeports'
// neutral ships), [H] Halcyon, [O] Ostrova, [V] Varkesh, [U] the Unbound, [B] the Brood. Your own ships carry none.
const PTAG={neutral:'I',halcyon:'H',ostrova:'O',varkesh:'V',pirate:'U',brood:'B'};
function pTag(e){const s=e&&(e.indId!=null?'neutral':e.side);return PTAG[s]?`[${PTAG[s]}]`:''}
indLabel=function(I){return`[I] ${I.name} · ${indDoing(I)}${I.pt?' · '+ptName(I.pt):''}`};
{const o=ctName;ctName=function(e){const n=o.apply(this,arguments);try{if(!e||e.side==='player'||/^\[/.test(n))return n;const t=pTag(e);return t?`${t} ${n}`:n}catch(x){return n}}}
