# Driftgate Beyond: working notes for Claude

**What this is.** A new game in the Driftgate universe, forked from Driftgate 1 v255 (Nov 2026). The code here starts as Driftgate 1's complete game (a 3D browser space game: three factions, the alien Brood, the Unbound pirates, a closed economy, multiplayer for up to four pilots). We are designing something new on top of it. **Design comes first:** agree the change in `BEYOND_DESIGN.md` with the user before building it.

**Driftgate 1 is a separate game that is still being developed** in `mbyrtus-maker/driftgate` (published at https://claude.ai/artifact/BpiqjUvanRKdLfRecpwdz2; the fork point is its branch `driftgate1-v255`). Its changes after the fork do **not** carry into Beyond, and Beyond's changes never go back to it: don't touch that repository from a Beyond session, and port a Driftgate 1 change only if the user asks. Its history and every design decision up to the fork are in `DESIGN_NOTES.md` here (read the relevant section before changing a system) and `ECONOMY_DESIGN.md`.

**Beyond's identity (keep it):** browser storage keys `dgbeyond.*` (save `dgbeyond.save.v1`), multiplayer host ids `dgbeyond1-<code>-host`, relay topics `dgbeyond1/…`, tab channel `dgbeyond`, title "Driftgate Beyond". Published page: https://claude.ai/artifact/9DnfnBp7b1bfJEMe25nkJv (publish with the Artifact tool and that `url`).

## Settled findings (read before stating a cause)
Causes and decisions the user has confirmed or corrected. They override anything older in `BEYOND_DESIGN.md`. **Before you state why something happened, look it up here or in the design notes; don't go from memory or an earlier summary.** When the user corrects a finding, add or fix it here in the same turn, and mark the old claim where it stands in `BEYOND_DESIGN.md` with a one-line *Superseded: …* note.
- **The Brood's gain with independent pilots (7–8 Nov 2026):** not a warehouse drain. Independent miners sold ore to the freeports, every power's warehouse swelled evenly, and wars between even powers stalled. Fixed by no truce against a power at 20 systems, the Containment Accord at 10 (off below 8), and Brood grazing 1.9 (1.3 since 8 Nov 2026, below). Result: Brood 20%, powers 23–26%, unfinished 4%. See "Independents' supply runs: war check and tuning" and "No truce against the powers".
- **Galaxy stalls (6 Nov 2026):** the powers ran short of Ferrite and Cuprite, while their warehouses filled with Crystal, Iridium and Aurorite. Fixed by miners passing over ore their power holds 300 of (`mineSkip`). See "Brood surges".
- **Ostrova's lead after the corporate economy (7 Nov 2026):** the Hollow Relay's tolls. The Relay is removed (the user).
- **The Brood (6 Nov 2026, the user):** every Brood ship, node upgrade and capital is made from ore alone. Spending order: defence, then node upgrades, then capitals, then everything else. Bloom Nodes hold off carriers with Overgrowth.
- **Maker failures are fine** (the user, 7 Nov 2026: "I'm fine with multiple failings"). Don't tune to avoid them.
- **The convoy test's raid failures (8 Nov 2026)** were the test's timing (guest sync, relations not yet set up), not the game.
- **The Brood's gain with the makers' shipping (8 Nov 2026):** after systems shipping (`5ff1b3e`) the Brood rose from 20% to 31%. Ruled out: the makers' extra production for far shelves, supply runs, shipping to depots, and the `FAC_HOME` crash fix. Richer makers (8,000 cr and their own components) brought it to 26%. The exact cause is not traced (the payload-bay check was cancelled). **Balanced by Brood grazing 1.3** (the user: "I like the even of it"). Sweep, 300 galaxies each: 1.6: 25%; 1.3: Brood 23%, Ostrova 25, Varkesh 24, Halcyon 24, unfinished 4; 1.0: Brood 20%, Halcyon 29, Ostrova 27, Varkesh 23. A tune file sets `BR0.brGraze`, not `BAL.brGraze` (the Brood's ramp resets BAL from BR0 every tick).

## Source and build
- The game is one file, `index.html`, built from `src/`: `src/page.html` (markup and CSS), `src/data/*.html` (sound and model packs), `src/js/NN_name.js` in the order of `src/ORDER.txt`, `src/end.html`. Edit `src/`, never `index.html` directly.
- Build: `python3 tools/build.py`. It refuses duplicate function names across files and code after a mid-line `//` comment (put comments on their own line).
- **Always** syntax-check after building (the build's `--check` doesn't catch syntax errors):
  `node -e "const fs=require('fs');const h=fs.readFileSync('index.html','utf8');const m=[...h.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(x=>x[1]);for(const s of m){try{new Function(s);console.log('syntax ok')}catch(e){console.log('SYNTAX',e.message)}}"`
- The whole script is one closure. Systems are extended with the wrapper pattern `{const o=fn;fn=function(){...;return o.apply(this,arguments)}}` (function declarations can be reassigned). `16_expansion.js` and `16f_factions.js` are mostly wrappers on earlier files.
- Model pack: `cd tools && python3 build_models.py`, then write `src/data/mdlidx.html` as `<script type="application/json" id="mdlidx">`+`tools/models_idx.json`+`</script>` and `src/data/mdlbin.html` as `<script type="text/plain" id="mdlbin">`+`tools/models_gz.b64`+`</script>`. The CC0 model kits it reads are in `tools/kits/` (Kenney Space Kit GLTF, Quaternius Lowpoly Spaceships OBJ). After changing a model, `python3 tools/mdlcheck.py NAME` reports faces that z-fight and parts that hang in space (the build lifts z-fighting faces itself; the island list needs a look, not blind fixing).
- In-page debugging: `__dg.ev(code)` runs code inside the game's scope (Playwright tests use it).

## Rules the game keeps
- **The ledger is exact:** goods are never created or destroyed except by mining real rock; every unit moves between stores, holds, debris and wrecks. `ledger()` must stay exact (`devLedger(fn)` checks a change).
- **Multiplayer:** the host simulates; guests send inputs. Code that acts for a guest runs on the host inside `runAs(pid,fn)`; guest dock actions arrive as `{t:'act'}` and run through `dockAction` on the host.
- Faction balance target (Beyond, 3 Nov 2026): the Brood about 20%, the three powers about 25% each, balanced on stats with neutral leaders (traits are left to sway real galaxies), checked with a war check after any change that moves faction strength.
- **Every power mines at the same rate** (`BAL.ext` 1.0 each; the user, 3 and 7 Nov 2026). Never balance with mining rates. Each power's edge is its in-game faction perk: Halcyon the Trade Charter (mercantile), Varkesh the Dominion hulls, Ostrova its own perk (being redesigned, 7 Nov 2026). Tune those perks, the Brood's dials, or real game changes.

## Tests and checks
- Browser tests: `tools/tests/run.sh` (quick, ~10 min) or `run.sh full` (adds the training courses); multiplayer tests take `$PWD/index.html` (see `tools/tests/README.md`). The limpet test is timing-sensitive under load.
- War check: balance on stats only: `fastsim.py` starts every leader without traits (set `LEADERS=1` to keep them). Run Beyond's with `PPORT=mw` (the player an idle contractor) and **16 hours** (`... FILE 600 16 - 2 OUT.json`, about 25 min): Beyond has no deadline and galaxies take about 4.5 h to settle, so a 2.2 h run reports nearly every galaxy unfinished. Driftgate 1's form: `PFAC=<halcyon|varkesh|ostrova|pirate> python3 tools/fastsim.py FILE GAMES HOURS TUNE_JS|- WORKERS OUT.json` (480 games, 2.2 h per side; run the four sides, ~25 min). `fastsim.py` has a hard-coded scratch directory `D=` at the top: point it at your own scratchpad and copy the page there first. Run-to-run noise is about ±2 points.
- Don't `pkill -f` with a pattern that matches your own command line (it kills the shell).

## Sub-bots
Six agents in `.claude/agents/` take whole jobs off the main session: `war-sim` (war check and duels), `economy` (ledger, prices, pay rates, corporations), `mp-test` (host/guest tests), `training-mission` (training courses), `visuals` (models, preview sheets, art), `trait-check` (leader and pilot traits on every AI entity, `tools/tests/traits.py`). They report back and leave any changes uncommitted; the main session agrees design with the user, commits and publishes.

## Working in parallel
Several chats (each with its own machine and clone) and several sub-bots may work on Beyond at once. To keep out of each other's way:
- **Never merge `index.html`.** It is built output. When a pull or rebase conflicts on it, rebuild instead: `python3 tools/build.py`, syntax check, `git add index.html`, `git rebase --continue`. Same for `src/data/mdlidx.html` and `src/data/mdlbin.html` (rerun the model pack steps above).
- **`BEYOND_DESIGN.md`:** add new notes under their own new `###` heading rather than editing a section another chat may be editing, with one exception: a claim that has been disproved gets a one-line *Superseded: see …* note where it stands (and the finding goes on the Settled findings list above). On a conflict keep both sides' text.
- **Pull before you start and before every push** (`git pull -q --rebase`), and push small commits often so others rebase onto less.
- **Sub-bots in one chat share its CPU.** Run one heavy simulation at a time (a war check, `run.sh mp`, `run.sh full`) alongside lighter work; timing-sensitive tests (limpet, multiplayer) can fail falsely under load, so rerun a failure alone before believing it. When several sub-bots share a machine, wrap every browser run (a test, `fastsim.py`, `duel.py`, a preview render through Chromium) in `flock /tmp/dgbeyond-browser.lock <command>` so they take turns; read code while you wait.
- **Sub-bots that edit code** (visuals, training-mission, economy fixes) run in their own worktree (`isolation: "worktree"`), so two of them never build into the same folder. The main session brings their changes in, rebuilds and commits.
- **Say which chat is doing what.** Two chats shouldn't take the same system at once; if the user splits work across chats, name each chat's area in its first commit message.

## Workflow
- Every change: update `BEYOND_DESIGN.md` (and `DESIGN_NOTES.md` only for Driftgate 1-era systems you change), build, syntax check, test what you touched, commit, `git pull -q --rebase`, push.
- Commit messages end with the Co-Authored-By / Claude-Session lines the session gives you.
- Publish to the Beyond artifact URL above when a change is ready to play.
