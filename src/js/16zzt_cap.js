//@src 16zzt_cap.js
// ============================================================ Beyond: the ship cap raised (live space stage 6, 6 Nov 2026)
// Measured on the test renderer (software WebGL, 1280x720) in a home system: the simulation costs 0.2 ms a frame with 10
// ships, 0.5 to 0.8 ms with 27 to 58, 1.1 ms with 74; drawing is the cost (software rendering 50 to 83 ms a frame up to 50
// ships, 100 ms at 58 and over; a real GPU is many times faster). Every ship in a system is now a tracked unit, so the cap is
// where tracked units over it wait out of sight (miners and garrison fighters docked) rather than a quota for chance spawns:
// a home system or hub 40, any other 32, the deep 24, the void 12 (was 17, the void 6). Your crews don't count against it.
const CAP={core:40,hub:40,deep:24,void:12,other:32};
{const o=popCap;popCap=function(){const base=o.apply(this,arguments),k=DEF[W.sid].kind;return base-(DEF[W.sid].kind==='void'?6:17)+(CAP[k]||CAP.other)}}
