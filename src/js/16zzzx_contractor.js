//@src 16zzzx_contractor.js
// ============================================================ Beyond: a contractor's keys (user, 9 Nov 2026)
// "I think the take order and drop order and join operation are carry overs from Driftgate 1, they can be hidden until you have
// your own faction or declare an allegiance" and "O is engaging autopilot". For a pilot who neither flies for a power nor has
// declared a faction: O (join operation) and P / Shift+P (take or pick an order) do nothing but say so, the operations list
// is empty (so nothing sets a course and engages the autopilot for them), and the quick keys don't show them (05). Backspace
// still drops a selected job. The training courses keep them.
function ctrOnly(){const P=S&&S.player;return!!P&&!S.unb&&!S.training&&!P.sworn&&!P.decl}
{const o=planKey;planKey=function(){if(ctrOnly()){flash('Orders are for pilots who fly for a power or their own faction. Contract work is on the Jobs board.');return}return o.apply(this,arguments)}}
{const o=friendlyOps;friendlyOps=function(){if(ctrOnly())return[];return o.apply(this,arguments)}}
