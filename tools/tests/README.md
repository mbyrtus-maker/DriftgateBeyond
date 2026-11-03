# Driftgate browser tests

Each test opens the built game (`index.html` at the repo root) in headless Chromium with Playwright and drives it through
`window.__dg.ev(code)`, which runs code inside the game. Build first, then run:

    python3 tools/build.py
    tools/tests/run.sh          # quick tests
    tools/tests/run.sh full     # plus every training course

Set `DG_GAME` to test another file, and `DG_OUT` for where screenshots go (default: the temp folder).

| Test | Checks |
|---|---|
| load.py | the game loads with no page errors |
| standing.py | Beyond stage 1: freeport start unsworn, standing bands, hostility and docking by standing, bounty payers, jobs by issuer, attacking costs standing and draws aggro, drift, respawn at the freeport, ledger, a minute of flight |
| relations.py | Beyond stage 2: relation bands and hostility, war declared on its trigger, ceasefire, border demand, succession, Allegiance tab, a leader shot down and succeeded, an hour of strategy |
| loadout.py | Beyond stage 3: default fits and slot rules, machine-gun rounds, unfitted weapons refuse, no reload in flight, missiles x2, rearm paid to the treasury, landing kit, cargo module, mining laser on the ring (ledger exact), a blast breaks the ring, Loadout section, a minute of flight |
| intel.py | Beyond stage 5: Claim Beacons sold by power, buying one, claim jobs, a claim paid by its power with standing (ledger exact), a claim in the ring in flight, intel work routed to a chosen power (beacon flips, limpets), scanners see anomalies, anomalies beyond the gates, the intel bar |
| designs.py | Beyond stage 6: the powers' fighter designs: models in use, stats by design, undesigned classes keep the trait, freeport yard rolls, buying a design (design line and slots follow), AI ships fly their design, ledger exact |
| makers.py | Beyond stage 7: makers and their homes, product traits, first stock, works building from components (ledger exact), traits applied (Marchgun, Wakefire), Coldwater Refit grade cap, makers kept through a hull change, market works list, Loadout offers |
| smuggling.py | Beyond stage 7b: stolen tags, contraband by power, heat, a customs scan answered by surrender (goods to stores, ledger exact), bribe and run (hostile while hot), cooling, the hidden container, Riftstone (placed and cut, ledger exact), a black-market run taken and delivered |
| rating.py | Beyond stage 8: no Unbound start card, Rating 1 at start, a hull refused then allowed as work raises the Rating, grade caps for parts and systems, Rating never falls, the Allegiance tab shows it |
| lairs.py | Beyond stage 9: the Company screen, building a Lair (where, materials, ledger exact), docking, the stash (capacity by level, laundering), lying low, level 2, paid rearming, the Holdings tab, a hostile scout finds it and ships wear it down |
| depots.py | Beyond stage 10: a Lair upgraded to a Depot (ledger exact), your market trading through visiting traders, AI crews hired, mining, wages, laid up, leaving unpaid, the Economy and Post jobs tabs |
| stations.py | Beyond stage 11: a Depot does not hold the system, a Station does (ledger exact), buildings and their effects, an Escort laid down at level 3 and launched, the Carrier needs level 5 |
| strategic.py | Beyond stage 12: the sector view on the galaxy map (live and from intel), ship and threat counts, a capital ordered from it |
| galaxy.py | Beyond stage 12b: the new galaxy (46 systems, no crossing gates, freeports gated into deep space), bigger Unbound holds, Scrapheart for a peaceful contractor (market, rumours, a run paid by the Unbound, ledger exact), the peace breaking |
| declare.py | Beyond stage 13: 20 systems for 10 minutes and no deadline, declaring needs a Station, the truce on a declared leader, proposals (alliance, tribute), the faction ends with its last Station, the Brood strength scale |
| legend.py | Beyond stage 14: Legend points once per galaxy, the start package picker, a level 10 package applied (ledger exact), a win banking Conqueror's spoils carried into the next galaxy |
| piracy.py | Beyond: pirate gear: Scrapheart stock, jammer and hook fitted, a hauler jammed dark and hooked (stolen tags, heat, standing, ledger exact), customs heat for gear |
| train_flight.py | Beyond training section 1: the picker, the contractor start, all 21 steps of Flight and your first job |
| train_contracts.py | Beyond training section 2: Contracts and standing, all 13 steps, a freeport request bought, flown and delivered, ledger exact |
| crews.py | Beyond: AI crews as ships: miner, hauler and guard flying their jobs, a job change, laid up, a crew ship lost, none elsewhere, ledger exact |
| destroyers.py | Beyond: destroyers and the Ravager: laid down and launched, assault ships, model and mounts, the charged gun (shields down), the Gullet beam, your level 4 Station, no sloops, ledger exact |
| start_screen.py | the Training button stands out without moving the other buttons |
| keys.py | key list, rebinding with swap, saved bindings, the keys strip |
| brood_ui.py | Brood HUD chip, alerts at 5/6/7 systems, map meter |
| dock.py | five dock tabs, keys 1-5, Overview cards, sell hold, beacon purchase |
| jobs.py | the Jobs list: filters, sort, detail, delivery; 12 t beacon, scouts can't load one |
| ship.py | shipping a vault's goods: quote, fee, freighter, arrival, loss |
| limpet.py | limpet plant, damage bonus, turrets ignore it, fighters shoot it off, drones go dark when jammed |
| map.py | sector panel without ore tonnage, scanned prices, the map key |
| mining_sight.py | only the charge reticle on a mining hull aimed at a rock (screenshots) |
| stores.py | depots and freeports trade from their own stores, treasuries shared, ledger balances (the old-save migration is printed, not asserted: Beyond keeps no old saves) |
| haul_rates.py | trade bots per hauler hull for an hour of game time: cr/hour against the pay ladder (slow, run by hand) |
| dock_sweep.py | renders every dock tab at every station and outpost (and a Lair) for each faction and the Unbound, clicks the buttons on one of each kind; prints any exception (slow, ~20 min) |
| soak.py | a bot pilot fights, jumps, docks, lands, mines and fires missiles for N sim minutes in eight hull/faction setups; prints frame errors: `python3 tools/tests/soak.py 15` |
| mine_rates.py | mining pay model per miner hull at real market prices (relative check against an older build; optimistic in absolute terms) |
| training.py | flies a training course end to end; `TRK=full\|combat\|mining\|hauling\|scouting` |
| mp_loopback.py | **retired with Unbound mode (stage 8)**: it starts an Unbound crew galaxy, which Beyond no longer offers. `mp_contractor.py` covers two pages joined over a faked link |
| mp_guest_jump.py | a guest in a Light Miner (with Ward Drones) jumps Varkesh Hold → Iron Hush: no exception, the screen fades back in, host and guest agree: `python3 tools/tests/mp_guest_jump.py $PWD/index.html` |
| mp_subtargets.py | sub-targets over the faked link: a hostile escort's damaged systems reach the guest, the guest's Shift+T, systems panel, lead point and HUD markers, a guest's shots disable a turret on the host, ledger: `python3 tools/tests/mp_subtargets.py $PWD/index.html` |
| mp_signature.py | faction signature hulls flown by a guest: a Varkesh guest converts a Heavy Miner to a Bombard through the dock, its shells fire on the host and hit; a guest Gannet's barrage and a guest Vesper's charged railgun fire on the host: `python3 tools/tests/mp_signature.py $PWD/index.html` |
| mp_contractor.py | host and guest both start as contractors at freeports: the guest flies as its own side, AI hostility follows its own standing, its job's issuer pays its bounty, standing reaches the guest, ledger: `python3 tools/tests/mp_contractor.py $PWD/index.html` |
| mp_guest_faction.py | a faction guest over the faked link: hired wingman follows, stands down when docked or dead, rejoins; insurance and a covered loss; patronage; charge reticle; ledger: `python3 tools/tests/mp_guest_faction.py $PWD/index.html` |

Tests of faction behaviour open the page with `?sworn=halcyon`, which starts a pilot sworn to Halcyon as Driftgate 1 did; without it a pilot starts as an independent contractor at a freeport.

Run them before publishing a change that touches what they cover; training.py after any change to lessons or the dock.
`tools/old/` holds one-off patch scripts from before the source split: history only, not to be run again.
