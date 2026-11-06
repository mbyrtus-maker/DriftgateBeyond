# Corporations model (Beyond, 5 Nov 2026)

A minute-by-minute model of the corporate economy proposed in BEYOND_DESIGN.md ("Corporations with money"), on the game's
real makers, product lines, traits, prices and component costs. Version 2 follows the user's rules: every upgradable system
is a part; every maker part trades a strength for a sensible weakness (standard parts stay at zero); parts sell at a profit
after the station's cut and fees; demand moves the prices of wanted parts; a disliked part gets up to 3 tweaks, then a new
product replaces it and its unsold stock goes back to raw ore.

- `extract.py`, `extract2.py`: read the game's data (makers, lines, prices, system recipes, ore) from `index.html` into
  `data.json` and `data2.json` (Playwright). Re-run after changing makers or parts.
- `sim2.py`: the model (`sim(seed, params)`; the defaults are the recommended numbers).
- `run_v2.py`: 200 galaxies of 16 h for each setting; prints the results and writes `res_v2.json`. About 20 s.
- `sim17.py`, `run_v17.py`: version 17 (v16 with buyers who weigh price against quality by their means, strapped/steady/flush, and a launch that keeps the old grade on sale as the maker's budget line, with older stock on clearance). `run_v17.py` writes `res_v17.json`.
- `order_v17.py`: a faction's bulk order with one maker (sim17's `orders` setting): how long it takes to fill and what it does to other buyers and rivals.
- `sim16.py`, `run_v16.py`: version 16 (v15 with makers tweaking a line, instantly and for all stock, when a rival maker outsells it 2 to 1 in the review window; being outsold doesn't start R&D by itself). `run_v16.py` measures tweaks and projects by cause, failures and how long one maker leads a kind of part; writes `res_v16.json`.
- `whale2_v15.py`: the same bulk buying, seen from the other makers of that part and its buyers (sales, price, tweaks, R&D, earnings, shares).
- `whale_v15.py`: a wealthy pilot buying one line in bulk from hour 4 to hour 8 (sim15's `whale` setting), compared with the same galaxies without them.
- `sim15.py`, `run_v15.py`: version 15 (v14 with CEOs replaced after the share price falls 2 hours running, and steadier prices so a pilot's 2-hour round trip is usually ahead: R&D counted at cost while it runs, the launch premium used up as earnings arrive, calmer investors). `run_v15.py` adds the 2-hour round trip (`FEE=` broker's fee each way, default 0.01; `IMP=` price moved per share of the pilot's own order, default 0.005) and writes `res_v15.json`; about a minute at N=200.
- `sim14.py`, `run_v14.py`: version 14 (v13's market with R&D paid from the maker's own money, dividends that grow with success, the powers' peace/tension/war moving the weapon makers, an hourly analysts' rating, calmer investors and a 200 cr/h earnings prior). `run_v14.py` writes `res_v14.json` (`N=`, `W=`); about a minute at N=200 on two cores.
- `sim13.py`, `run_v13.py`: version 13 (v12 with the products evened out, and a stock market: price chases book value + smoothed earnings x 8 h + R&D pipeline + dividends, moved by investor mood and news; optional share issues for R&D). `run_v13.py` writes `res_v13.json` (`N=` galaxies, default 200; `W=` workers); under a minute at N=100.
- `sim12.py`, `run_v12.py`: version 12 (v11 with running costs doubled for the bigger market and R&D funded with 3 hours of running costs kept back). `run_v12.py` writes `res_v12.json`; about three minutes.
- `sim11.py`, `run_v11.py`: version 11 (v10 with the powers refitting their whole fleets: miners, haulers and scouts as well as warships; popular mining gear). `run_v11.py` writes `res_v11.json`; about three minutes.
- `sim10.py`, `run_v10.py`: version 10 (v9 with the goods divided evenly: every maker has at least one solid line). `run_v10.py` writes `res_v10.json`; about two minutes.
- `sim9.py`, `run_v9.py`: version 9 (v8 tuned for a first R&D launch at about 3 hours). `run_v9.py` writes `res_v9.json`; about a minute.
- `sim8.py`, `run_v8.py`: version 8 (v7 with faster judging and tweaks, half-price R&D, the powers' tastes from their doctrines, spying that speeds the spy's own R&D and sabotage that slows the target's). `run_v8.py` writes `res_v8.json`; about a minute.
- `sim7.py`, `run_v7.py`: version 7 (corporate R&D: grade 1 launches, tweaks, then projects for the next grade with design, materials and trials; rival spying and sabotage; missions counted; no random events). `run_v7.py` writes `res_v7.json`; about 40 s.
- `sim6.py`, `run_v6.py`: version 6 (standard parts stocked by the factions, makers sell only trait lines). `run_v6.py` writes `res_v6.json`; about 30 s.
- `sim5.py`, `run_v5.py`: version 5 (every maker sells at every station, fixed line-ups with fixed starting traits; CEOs and events random). `run_v5.py` writes `res_v5.json`; about 40 s.
- `sim4.py`, `run_v4.py`: version 4 (every maker sells at the freeports, station standard parts, galaxy events: famine, feast, plague, war scare, ore boom, shortage). `run_v4.py` writes `res_v4.json`; about 40 s.
- `sim3.py`, `run_v3.py`: version 3 (no upgrades, Unbound gear out, ore to the station holding the stock, random line-ups per galaxy, CEO traits). `run_v3.py` writes `res_v3.json`; about 30 s.

Report: https://claude.ai/artifact/TXz37kLRJcGkfqaoAiWQhC
