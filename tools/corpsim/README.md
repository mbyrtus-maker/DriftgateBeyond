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

Report: https://claude.ai/artifact/TXz37kLRJcGkfqaoAiWQhC
