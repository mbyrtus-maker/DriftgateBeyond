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
- `sim8.py`, `run_v8.py`: version 8 (v7 with faster judging and tweaks, half-price R&D, the powers' tastes from their doctrines, spying that speeds the spy's own R&D and sabotage that slows the target's). `run_v8.py` writes `res_v8.json`; about a minute.
- `sim7.py`, `run_v7.py`: version 7 (corporate R&D: grade 1 launches, tweaks, then projects for the next grade with design, materials and trials; rival spying and sabotage; missions counted; no random events). `run_v7.py` writes `res_v7.json`; about 40 s.
- `sim6.py`, `run_v6.py`: version 6 (standard parts stocked by the factions, makers sell only trait lines). `run_v6.py` writes `res_v6.json`; about 30 s.
- `sim5.py`, `run_v5.py`: version 5 (every maker sells at every station, fixed line-ups with fixed starting traits; CEOs and events random). `run_v5.py` writes `res_v5.json`; about 40 s.
- `sim4.py`, `run_v4.py`: version 4 (every maker sells at the freeports, station standard parts, galaxy events: famine, feast, plague, war scare, ore boom, shortage). `run_v4.py` writes `res_v4.json`; about 40 s.
- `sim3.py`, `run_v3.py`: version 3 (no upgrades, Unbound gear out, ore to the station holding the stock, random line-ups per galaxy, CEO traits). `run_v3.py` writes `res_v3.json`; about 30 s.

Report: https://claude.ai/artifact/TXz37kLRJcGkfqaoAiWQhC
