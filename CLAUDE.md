# Driftgate Beyond: working notes for Claude

**What this is.** A new game in the Driftgate universe, forked from Driftgate 1 v255 (Nov 2026). The code here starts as Driftgate 1's complete game (a 3D browser space game: three factions, the alien Brood, the Unbound pirates, a closed economy, multiplayer for up to four pilots). We are designing something new on top of it. **Design comes first:** agree the change in `BEYOND_DESIGN.md` with the user before building it.

**Driftgate 1 is a separate game that is still being developed** in `mbyrtus-maker/driftgate` (published at https://claude.ai/artifact/BpiqjUvanRKdLfRecpwdz2; the fork point is its branch `driftgate1-v255`). Its changes after the fork do **not** carry into Beyond, and Beyond's changes never go back to it: don't touch that repository from a Beyond session, and port a Driftgate 1 change only if the user asks. Its history and every design decision up to the fork are in `DESIGN_NOTES.md` here (read the relevant section before changing a system) and `ECONOMY_DESIGN.md`.

**Beyond's identity (keep it):** browser storage keys `dgbeyond.*` (save `dgbeyond.save.v1`), multiplayer host ids `dgbeyond1-<code>-host`, relay topics `dgbeyond1/…`, tab channel `dgbeyond`, title "Driftgate Beyond". Published page: https://claude.ai/artifact/9DnfnBp7b1bfJEMe25nkJv (publish with the Artifact tool and that `url`).

## Source and build
- The game is one file, `index.html`, built from `src/`: `src/page.html` (markup and CSS), `src/data/*.html` (sound and model packs), `src/js/NN_name.js` in the order of `src/ORDER.txt`, `src/end.html`. Edit `src/`, never `index.html` directly.
- Build: `python3 tools/build.py`. It refuses duplicate function names across files and code after a mid-line `//` comment (put comments on their own line).
- **Always** syntax-check after building (the build's `--check` doesn't catch syntax errors):
  `node -e "const fs=require('fs');const h=fs.readFileSync('index.html','utf8');const m=[...h.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(x=>x[1]);for(const s of m){try{new Function(s);console.log('syntax ok')}catch(e){console.log('SYNTAX',e.message)}}"`
- The whole script is one closure. Systems are extended with the wrapper pattern `{const o=fn;fn=function(){...;return o.apply(this,arguments)}}` (function declarations can be reassigned). `16_expansion.js` and `16f_factions.js` are mostly wrappers on earlier files.
- Model pack: `cd tools && python3 build_models.py`, then write `src/data/mdlidx.html` as `<script type="application/json" id="mdlidx">`+`tools/models_idx.json`+`</script>` and `src/data/mdlbin.html` as `<script type="text/plain" id="mdlbin">`+`tools/models_gz.b64`+`</script>`. The CC0 model kits it reads are in `tools/kits/` (Kenney Space Kit GLTF, Quaternius Lowpoly Spaceships OBJ).
- In-page debugging: `__dg.ev(code)` runs code inside the game's scope (Playwright tests use it).

## Rules the game keeps
- **The ledger is exact:** goods are never created or destroyed except by mining real rock; every unit moves between stores, holds, debris and wrecks. `ledger()` must stay exact (`devLedger(fn)` checks a change).
- **Multiplayer:** the host simulates; guests send inputs. Code that acts for a guest runs on the host inside `runAs(pid,fn)`; guest dock actions arrive as `{t:'act'}` and run through `dockAction` on the host.
- Faction balance target (Beyond, 3 Nov 2026): the Brood about 20%, the three powers about 25% each, balanced on stats with neutral leaders (traits are left to sway real galaxies), checked with a war check after any change that moves faction strength.

## Tests and checks
- Browser tests: `tools/tests/run.sh` (quick, ~10 min) or `run.sh full` (adds the training courses); multiplayer tests take `$PWD/index.html` (see `tools/tests/README.md`). The limpet test is timing-sensitive under load.
- War check: balance on stats only: `fastsim.py` starts every leader without traits (set `LEADERS=1` to keep them). Run Beyond's with `PPORT=mw` (the player an idle contractor) and **16 hours** (`... FILE 600 16 - 2 OUT.json`, about 25 min): Beyond has no deadline and galaxies take about 4.5 h to settle, so a 2.2 h run reports nearly every galaxy unfinished. Driftgate 1's form: `PFAC=<halcyon|varkesh|ostrova|pirate> python3 tools/fastsim.py FILE GAMES HOURS TUNE_JS|- WORKERS OUT.json` (480 games, 2.2 h per side; run the four sides, ~25 min). `fastsim.py` has a hard-coded scratch directory `D=` at the top: point it at your own scratchpad and copy the page there first. Run-to-run noise is about ±2 points.
- Don't `pkill -f` with a pattern that matches your own command line (it kills the shell).

## Workflow
- Every change: update `BEYOND_DESIGN.md` (and `DESIGN_NOTES.md` only for Driftgate 1-era systems you change), build, syntax check, test what you touched, commit, `git pull -q --rebase`, push.
- Commit messages end with the Co-Authored-By / Claude-Session lines the session gives you.
- Publish to the Beyond artifact URL above when a change is ready to play.
