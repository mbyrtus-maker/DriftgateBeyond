# Driftgate browser tests

Each test opens the built game (`index.html` at the repo root) in headless Chromium with Playwright and drives it through
`window.__dg.ev(code)`, which runs code inside the game. Build first, then run:

    python3 tools/build.py
    tools/tests/run.sh          # quick tests
    tools/tests/run.sh full     # plus every training course
    tools/tests/run.sh mp       # the multiplayer guest tests (about an hour)

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
| train_combat.py | Beyond training section 3: Combat, all 14 steps: drones, laser, missile, flares, salvage, two live raiders, distress, ledger exact |
| train_mining.py | Beyond training section 4: Mining, all 13 steps: laser on the ring, a charge fired and detonated, chunks scooped, ore delivered and sold, ledger exact |
| crews.py | Beyond: AI crews as ships: miner, hauler and guard flying their jobs, a job change, laid up, a crew ship lost, none elsewhere, ledger exact |
| destroyers.py | Beyond: destroyers and the Ravager: laid down and launched, assault ships, model and mounts, the charged gun (shields down), the Gullet beam, your level 4 Station, no sloops, ledger exact |
| dread.py | Beyond 12c: the Dread Pirate: rolled traits, Allegiance row, spawned with an escort, killed by you (bounties from every power, Paranoid successor with a bounty on you), aboard and sunk with the Ravager, events, hoard-sale prices, the hunt job, the rumour, successions after raiders lost to the Brood, failed raids and bargains kept, ledger exact |
| capescort.py | Beyond: capital escorts and the carrier's defence set: the set aboard, launched on a raider, landed 20 s after, the scout flipping the beacon and limpeting an attacking capital, everything landing past 75% of the spin-up and jumping with the carrier, a guard docking on an escort capital's hull, undocking when the spin breaks, riding the jump and arriving beside it, ledger exact |
| gatelock.py | Beyond 6c: gate lock kits: made at Scrapheart, bought (one an hour), pirate gear, set at a gate, armed, a convoy waiting at it, off-screen routing round it, the powers' job to break it, broken from the far side and paid, burnt out, an Unbound lock for a convoy, ledger exact |
| fall.py | Beyond: when your base falls: a Station captured (hull, buildings, store, holds the system for the power, crews leave), taken back, destroyed; a Lair impounded; ledger exact |
| blackmarket.py | Beyond: the Black market tab: contacts, requested work, the heat filter, a run given to a contractor (broker cut) and to an AI crew (paid; caught: seized, heat on you), a contraband buy, a quiet buyer, a fence, the tab, ledger exact |
| postjobs.py | Beyond: jobs posted to other pilots: the galactic mean and the bids (wait times, the 200% cap), Supply, Haul, Mine and Guard done by AI takers and paid, a job withdrawn, another player delivering, the tab, ledger exact |
| brand.py | Beyond: your own brand: none without a Depot, name and points netting to zero (an unpaid strength refused), a gun built at your Depot carrying the brand and its trait, fitted damage, reshaping for credits, the tab, the company colour (picked from the palette, shown for you and on the map, fixed once declared), ledger exact |
| zoom.py | Beyond: the strategic map zoomed into a system (button, wheel, the Galaxy box, drawn full size), a capital on patrol sweeping its route, one escorting you, Guard here clearing both |
| smallitems.py | Beyond: rigs and racks on scouts only, flips and limpets by grade and restocked on docking, a comet sold to the Compact, embargo contraband by origin, a Rift Shard standing in and leaving a trait, ledger exact |
| dev_beyond.py | Beyond: the developer panel without a faction: all powers as enemy sides, the Beyond tools and the old ones, ledger exact after each |
| company2.py | Beyond screens pass: the minimal Company screen (Holdings list and detail, Send a guard, buildings; every tab in simple and Full view; hire and post from the Jobs forms; market trade switch; relations pair; Black market assign); ledger exact |
| fees.py | Beyond: your base's fees: defaults, limits, trade volume at steep and cheap prices, docking fee income and thinner traffic, visiting pilots' services, posted-job waits, the Holdings Fees panel; ledger exact |
| cscan.py | Beyond: the cargo scanner: none without the part, rough then exact readings, out of range, Unbound built-in, hidden containers, heat in a power's own space, freeport stock; ledger exact |
| claimfit.py | Beyond: Claim Beacons as fitted parts: Market tiles per power in its colour, buy, Loadout Fit and Buy & fit, refused on a miner, hold-only beacons don't claim, fitted ones do and are used up; ledger exact |
| corps.py | Beyond: every item has a maker: the makers' lines with plain parts, no unbranded parts on the makers' markets, every slot covered at a freeport, the works build plain parts, made-by labels in the Market; ledger exact |
| news.py | Beyond: the leaders' news box: a leader's declaration (war, embargo, pact) and the Dread Pirate's fortunes go in under their faction and name, a relations band change doesn't, the newest three stay, they fade and go after three minutes, the box renders in the HUD |
| comms_jobs.py | Beyond: Comms Jobs here: I, I opens it; a fighter sees the convoy raid and escort, a miner the ore contracts; other hulls' jobs counted not listed; picking an escort signs on, a contract tracks; More pages; the quick-keys count; an Unbound pilot's Prey here with the scanned ship first and picking targets it; ledger exact |
| drones.py | Beyond: the Drone controller: a new Light Miner has one fitted in its own slot; without one no drones launch; a fighter can't fit one; lost drones refill at Rearm (built by the station, paid to its treasury); a maker's grade 2 controller makes tougher drones; an older miner's fit gets the slot and a controller; where the makers' controllers are sold; ledger exact |
| audience.py | Beyond: an audience with a leader: the panel only explains before you declare; declared, a request gives an ETA, the flagship docks and the audience opens; open trade moves prices and costs standing; a refusal is free; aid reaches your Station; war on a power; the audience ends with a cooldown; ledger exact |
| marque.py | Beyond: Scrapheart's tabs (Overview, Plunder, Tavern, Ship, Marques); Tavern convoy raids out to five jumps, not six; a letter of marque: the sponsor's ships friendly, its war enemies and the Brood hostile, the Unbound neutral, enemy stations shut, the sponsor pays a war enemy's bounty; the HUD shows the flag; striking it; Hostile revokes it; ledger exact |
| fpdark.py | Beyond: freeports never fall: the Brood razing one knocks it out (dark five minutes: no market, jobs or docking), then it relights at half hull; a lost freeport is rebuilt; ledger exact |
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
| training.py | flies one of Driftgate 1's training courses end to end (started with trainStart: Beyond's picker offers only its own sections); `TRK=full\|combat\|mining\|hauling\|scouting` |
| mp_loopback.py | **retired with Unbound mode (stage 8)**: it starts an Unbound crew galaxy, which Beyond no longer offers. `mp_contractor.py` covers two pages joined over a faked link |
| mp_guest_jump.py | a guest in a Light Miner (with Ward Drones) jumps Varkesh Hold → Iron Hush and back: no exception, the screen fades back in, host and guest agree, the two drones arrive with the ship each time on both screens (none left behind or doubled), ledger exact: `python3 tools/tests/mp_guest_jump.py $PWD/index.html` |
| mp_subtargets.py | sub-targets over the faked link: a hostile escort's damaged systems reach the guest, the guest's Shift+T, systems panel, lead point and HUD markers, a guest's shots disable a turret on the host, ledger: `python3 tools/tests/mp_subtargets.py $PWD/index.html` |
| mp_signature.py | faction signature hulls flown by a guest: a Varkesh guest converts a Heavy Miner to a Bombard through the dock, its shells fire on the host and hit; a guest Gannet's barrage and a guest Vesper's charged railgun fire on the host: `python3 tools/tests/mp_signature.py $PWD/index.html` |
| mp_beyond.py | Beyond's late additions over the faked link: the guest sees the new models (destroyers, Gullet, escorts, carriers, Unbound and work ships), a destroyer duel and the Gullet beam with the guest watching, a guest Medium Miner cutting with the mining laser on the host, ledger: `python3 tools/tests/mp_beyond.py $PWD/index.html` |
| mp_contractor.py | host and guest both start as contractors at freeports: the guest flies as its own side, AI hostility follows its own standing, its job's issuer pays its bounty, standing reaches the guest, ledger: `python3 tools/tests/mp_contractor.py $PWD/index.html` |
| mp_remote.py | Beyond: a flying guest runs its company on the host: fees from the Company screen and a crew's job from the map; a dock-only action is still refused in flight; a guest's cargo scan gets the host's reading (rough, then exact) of a supply freighter's hold; ledger: `python3 tools/tests/mp_remote.py $PWD/index.html` |
| mp_guest_play.py | Beyond: a guest plays: every dock menu on the guest's screen (Market categories, Fabricate, Loadout's parts, shipyard dropdown, Hangar, Allegiance), takes a Light Miner through the yard (tools, controller, drones), its drones launch on the host and show on the guest, lost drones refill at Rearm on docking, Comms Jobs here and the Company screen, then a fighter fight through the real input path (aim, hold fire, the raider dies on the host, the bounty reaches the guest); ledger: `python3 tools/tests/mp_guest_play.py $PWD/index.html` |
| regent.py | Beyond: sleep mode: appoint a stand-in (name, two traits, reserve) on the Allegiance panel, Sleep, and while asleep it pays a tribute and accepts an alliance (Patient), guards an attacked Station with its crew and lets it back to work after, adds a building (Industrious), sends envoys, stays above the reserve; a key wakes you with a report; 15 minutes idle hands over; a game closed for an hour waits (the catch-up is switched off for now); ledger exact |
| art.py | Beyond: the last approved art: every power's constructor draws as its approved model, every Unbound class as one of their six designs (the bomber as the Wrecker), and assault ships fly from a capital to the base it assaults (one shot down on the way, the others land and fly back) |
| mp_guest_kit.py | Beyond: a guest's kit: fit a part, a part grade and a system grade (Rating-gated, with the message), Rearm; the helm of an escort, a carrier and a frigate (board, helm/throttle/move/power orders reach the host, the frigate jumps with the guest aboard, step off); the Jobs board's beacon Buy & fit, then an outpost claimed from its ring, fee paid; ledger exact: `python3 tools/tests/mp_guest_kit.py $PWD/index.html` |
| mp_guest_trade.py | Beyond: a guest trades: buy and sell on a freeport's market (goods, credits, stock and treasury checked on the host), a freeport contract delivered from the Jobs board, a freeport request bought with the board's button, flown three jumps and delivered; ledger exact: `python3 tools/tests/mp_guest_trade.py $PWD/index.html` |
| mp_guest_convoy.py | Beyond: a guest's convoy jobs: a power's raid from the board shot down with its own guns (issuer's bounty, the full figure the board shows), an escort signed on with Select job and flown to the convoy's dock (fee paid), a Rusty Tankard rumour one jump out from Scrapheart (the Unbound's share); ledger exact: `python3 tools/tests/mp_guest_convoy.py $PWD/index.html` |
| mp_guest_build.py | Beyond: a guest's holdings: a Lair built and docked at, raised to a Depot (the guest's berth follows), the Depot raised to a Station with a hangar, then the guest declares its own faction and docks at its Station; its stand-in: appointed, Sleep, answers a demand, a key wakes it with the report, leaving hands the faction over and coming back ends it; ledger exact: `python3 tools/tests/mp_guest_build.py $PWD/index.html` |
| mpkit.py | the shared harness for the guest tests above (two pages over the faked link: a Halcyon contractor host, a Varkesh contractor guest) |
| mp_guest_faction.py | a faction guest over the faked link: hired wingman follows, stands down when docked or dead, rejoins; insurance and a covered loss; patronage; charge reticle; ledger: `python3 tools/tests/mp_guest_faction.py $PWD/index.html` |

Tests of faction behaviour open the page with `?sworn=halcyon`, which starts a pilot sworn to Halcyon as Driftgate 1 did; without it a pilot starts as an independent contractor at a freeport.

Run them before publishing a change that touches what they cover; training.py after any change to lessons or the dock.
`tools/old/` holds one-off patch scripts from before the source split: history only, not to be run again.
