//@src 16zzzg_rdroll.js
// ============================================================ Beyond: R&D can fail its trials; R&D is investment (user, 8 Nov 2026)
// The economy test (BEYOND_DESIGN.md, "Economy test: do slow makers fail and leaders' shares climb?") found R&D quick and
// certain and share prices falling after every launch. The user: "Add an R&D random roll for success in each launch window.
// And then we need to fix investment vs product launch."
//   - The roll: when a project's trials end (its test pilot home, or the trials timer where no flight could go), it succeeds
//     on 75% at grade 2, 65% at 3, 55% at 4, 45% at 5 (an Innovator CEO +10%), and each failed trial before adds 10% (the lab
//     learns). Success launches the line as before. Failure: the prototype is broken back into its components (into the
//     maker's own store), and the project goes back to a redesign (half the grade's design time), then new materials and
//     another test flight.
//   - The lab costs money while a project runs: 60 cr an hour at grade 2, 150 at 3, 300 at 4, 600 at 5, paid to the host
//     station's owner. A slow or unlucky project drains cash.
//   - Investment: what a maker spends on R&D (funding, the lab's running costs, prototype materials and their freight) is
//     counted in its share price while the project runs, and fades 20% an hour after it ends. The price rides on operating
//     profit (the margin on what sold, less running costs; 16zzz_corp.js, ceHour), so spending on R&D or stock no longer
//     reads as a loss, and a launch that sells lifts the price.
// Host only. The ledger stays exact: a failed prototype's components only move into the maker's store.
const RD_WIN={2:.75,3:.65,4:.55,5:.45},RD_LAB={2:60,3:150,4:300,5:600},RD_LEARN=.1;
function rdWinChance(m,P){const c=ceOf(m);return Math.min(.95,(RD_WIN[P.g]||.5)+(c&&c.ceo==='Innovator'?.1:0)+RD_LEARN*(P.fails||0))}
// the roll in the launch window
{const o=rdLaunch;rdLaunch=function(m){const c=ceOf(m),P=c&&c.rd;if(!P||NET.cl)return o.apply(this,arguments);
  if(Math.random()<rdWinChance(m,P))return o.apply(this,arguments);
  P.fails=(P.fails||0)+1;inv.addAll(ceStore(m),P.proto);P.proto={};P.got=0;P.ivm=0;P.fly=null;P.pilot=null;P.mj=null;P.mjT=0;P.stage='design';P.until=S.T+Math.round(RD.design[P.g]*.5);
  ceNews(m,`'s ${ITEMS[rdGid(P.id,P.g)].name} prototype failed its trials${P.fails>1?` (${P.fails} failures so far)`:''}. Back to the drawing board: a redesign, new materials and another test flight.`)}}
// funding is investment
{const o=rdStart;rdStart=function(m,id,why){const r=o.apply(this,arguments);if(r){const c=ceOf(m);if(c&&c.rd)c.iv=(c.iv||0)+(RD.cost[c.rd.g]||0)}return r}}
// the lab's running costs while a project runs (each minute, with the works' running costs)
{const o=ceMinute;ceMinute=function(){const r=o.apply(this,arguments);try{if(!NET.cl)for(const m in MAKERS){const c=ceOf(m);if(!c||c.dead||!c.rd)continue;
    const due=Math.round((RD_LAB[c.rd.g]||0)/60);if(due<=0)continue;const paid=transfer(ceW(m),ceHostWallet(m),due);c.cost+=paid;c.iv=(c.iv||0)+paid}}catch(e){console.error(e)}return r}}
// prototype materials bought at home (no materials job) are investment too
{const o=rdTick;rdTick=function(){const r=o.apply(this,arguments);try{if(rdOn()&&!NET.cl)for(const m in MAKERS){const c=ceOf(m);if(!c||c.dead||!c.rd)continue;const P=c.rd;
    if(P.got&&!P.ivm){P.ivm=1;const R=mkAtHome(m);c.iv=(c.iv||0)+Math.ceil(R?ceComp(R.sid,rdGid(P.id,P.g)):invValue(P.proto))}}}catch(e){console.error(e)}return r}}
// a company that fails loses what it had put in
{const o=ceFail;ceFail=function(m){const c=ceOf(m);if(c)c.iv=0;return o.apply(this,arguments)}}
