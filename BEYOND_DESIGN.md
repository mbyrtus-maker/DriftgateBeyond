# Driftgate Beyond: design

A new game in the Driftgate universe. This file holds its design as it is decided; DESIGN_NOTES.md is Driftgate 1's history up to the fork.

## Fork (Nov 2026)
- Forked from Driftgate 1 v255 with its full code, tools and tests.
- Own identity: browser storage keys `dgbeyond.*` (save `dgbeyond.save.v1`, legend, keys, audio, lore, aces, tips, multiplayer ids), multiplayer host ids `dgbeyond1-<code>-host`, relay topics `dgbeyond1/…`, tab channel `dgbeyond`, title "Driftgate Beyond", invite links to mbyrtus-maker.github.io/DriftgateBeyond/.

---

## Vision (draft 3, 2 Nov 2026: for review, nothing here is built)

### In one paragraph
The war goes on, but you no longer fight in it as a soldier. You are an independent contractor who starts at a freeport with one light ship and a few credits, and you take work from whoever will pay. Corporations under the factions and at the freeports (two at each) make what the market sells, and you can make it yourself: ore into components, components into parts, parts into better parts. Your money and materials go up a ladder: ships, then upgrades to those hulls, then a Lair (2 levels), then a Depot (3), then a full Station (5), and finally capital ships built at your stations. From the Depot on you hire AI pilots and ships, pay their upkeep, earn from your own market, post your own jobs and command them from a strategic map. In the end your company declares itself a faction and joins the war as a fourth contender.

### What carries over, what changes, what goes

| Keep from Driftgate 1 | Change | Drop |
|---|---|---|
| Flight, drift by mass, gates, docking | Pilot welded to one faction → **standing** with every power, work for anyone | **Unbound pirate mode** (the start card, crew galaxies, Scrapheart Haven works) |
| Combat feel, shields, sub-targets, capitals and bridges | Pay from your faction's treasury → paid by **whoever issued the job** | **Legend levels** as they are (replaced, see Progression) |
| Blast charges, salvage, hauling, convoys | Blast rig only → **mining lasers back** alongside charges, both in a mining hull's weapon slots | Mk I–III as one shared ladder (replaced by grades) |
| The three factions, their AI war, campaigns, depots, sieges | One Weapons system for gun and laser together → **separate parts in weapon slots**; slot count varies by ship | Scout hulls as a starter |
| **The Brood,** stronger: more presence, about 20% of galaxies | Free kinetic fire → **machine guns use ammunition**; lasers draw on the reactor | |
| **AI Unbound raiders** in the galaxy | Missiles that reload by themselves → **payload** you carry, which hits harder | |
| AI scouts: beacons, limpets, recon, Seeder spotting | Scouting as a career → **intel as a trade good**: beacon devices, pings, limpets and discoveries you sell | |
| Anomalies, wrecks, quiet-space signals | Moved **out beyond the gates**, as discoveries to find and sell | |
| Freeports and the Compact, Seals and Matrices | Unbranded goods → **corporate parts** with a maker and a trait | |
| The closed economy and the exact ledger | A short crafting list → **ore → components → parts → upgraded parts** | |
| D1's Unbound Lair, depots, depot modules, stations | Faction-only bases → **your own Lair → Depot → Station**, each with levels | |
| Capital ships and their bridges | Commissioned at a faction yard → **built at your own stations** | |
| Multiplayer: host simulates, guests send inputs | Three contenders → three plus **contractor factions** | |
| Signature hulls (Gannet, Bombard, Vesper) | Become **house-brand hulls**, built with standing | |
| Faction careers (hauling, mining, scouting) | Become **bonuses on that faction's jobs** | |
| | One shared model per class with a ±12% trait → **unique hull designs** for each faction and the Unbound | |
| Flares on energy and a cooldown; drones restocked at dock | Unchanged | |
| Galaxy map with its sector panel | → a **strategic map** you zoom into a sector to command your AI | |
| Training | Rewritten later for the contractor's start | |

---

### 1. Contractors, not soldiers
- **You start at a freeport, not a faction,** and you choose which: Mirrorwater, Coldwater Drift or Ember Wake, each near different factions and makers. You're neutral with every power, at Rating 1, with a few credits.
- **Three starters, fully equipped.** Choose one; each comes with drive, reactor, shield and armour fitted, plus its role kit:
  - **Light Fighter:** a machine gun with ammunition, a laser and a missile launcher with a first magazine.
  - **Light Miner:** a mining laser, a charge launcher with charges, and drones.
  - **Light Hauler:** a machine gun and a cargo module.
- **There is no scout start.** The powers' AI scouts still do most of the routine recon. Contractors scout in a different way: intel as a trade good (section 6a).
- **Work for anyone, job by job.** Factions and freeports offer you jobs (the Faction jobs screen, section 9). Later you post your own.
- **Pay comes from whoever issued the job,** out of their treasury. Bounties are paid by the power whose combat job you're flying; with no job running, by the power at war with the victim that you stand best with. Credits stay zero-sum, as now.
- **Nothing is untouchable.** You can fire on anyone; doing so costs standing (section 2).
- **War effort still counts.** Work done on a faction's job adds to that faction's war effort, as in Driftgate 1, so contractors still swing battles fought out of sight.

### 2. Standing
Each pilot has a standing with every power: Halcyon, Varkesh, Ostrova, the Freeport Compact, and later each contractor faction. It runs from −100 to +100 and starts at 0. The Brood and the Unbound are always hostile.

| Band | Standing | What it means |
|---|---|---|
| Hostile | below −50 | Its ships attack you on sight; no docking; its makers won't sell to you |
| Unwelcome | −50 to −10 | No docking; its patrols scan you and warn you off |
| Neutral | −10 to +25 | Dock, trade, basic jobs, grade 1–3 parts from its makers |
| Trusted | +25 to +60 | Better-paid war jobs, grade 4 parts, escort and convoy work |
| Partner | above +60 | Grade 5 parts, the house-brand hulls, stationworks and capital jobs |

- **Rises** with jobs completed for that power, scaled by risk.
- **Falls** when you damage its ships, convoys or stations. It falls a quarter as much when you do war work against it for someone else, or fail one of its jobs.
- **Drifts** slowly back toward 0.
- **Building in a power's space** needs Neutral or better, or it treats your Lair, Depot or Station as a target.

### 3. Making things: ore → components → parts → upgraded parts
Everything comes from mined rock, so the ledger stays exact.

| Tier | What it is | Examples | Made where |
|---|---|---|---|
| Ore | Mined from rock | Ferrite, Cuprite, Iridium, Xenocrystal, Vantium, Aurorite | Mining |
| Components | Made from ore | Alloy Plate, Conduit, Flux Coil, Crystal Lattice, Resonance Core, Depot Frame, Capital Keel | Any workshop; lattice and core need a forge |
| Parts | Made from components; what you fit to a ship | Machine gun, laser, missile launcher, mining laser, charge launcher, drive, reactor, shield, armour, cargo module | Any workshop |
| Upgraded parts | A part plus new components, giving the next grade | A grade 1 laser + 2 Flux Coil + 1 Crystal Lattice → a grade 2 laser | Any workshop; the top grades also need a Compact Calibration Matrix |
| Payload | Made from components; used up | Machine gun ammunition, missiles, torpedoes, blast charges | Any workshop, or bought by the lot |

- **Grades 1–5 replace Mk I–III.** You upgrade a part by feeding it into the next grade's recipe, so your investment carries forward instead of being thrown away.
- **Workshops.** Any faction or freeport station's workshop builds for a fee. Your own (from Lair level 2) builds with no fee.
- **Your own brand, from Depot level.** Parts built at your Depot's or Station's workshop carry your company's name and a trait you choose, and sell on your market like any maker's. Parts from a Lair are standard.
- **Corporate parts.** The makers (section 4) sell parts too. A maker's part carries its maker's trait, a strength and a weakness, like Driftgate 1's variants. A part you build yourself before you own a Depot is standard, with no trait. You can upgrade either; an upgraded corporate part keeps its maker and trait.

### 4. Makers: corporate items
Corporations make much of what's on the market. Each faction hosts two named makers and each freeport two more, each with a trait that follows its home's character. Only the factions' frame makers design hulls; the freeport makers make parts and build the factions' designs under licence. Names are placeholders, kept for now.

| Power | Maker (placeholder) | Makes | Trait |
|---|---|---|---|
| Halcyon Accord | Teal & Corvane Yards | Halcyon hulls, cargo modules | Light, fast frames |
| Halcyon Accord | Brightline Emitters | Shields, lasers | Shields +, hull − |
| Varkesh Dominion | Hold Foundry | Varkesh hulls, armour, charge launchers | Heavy, tough frames |
| Varkesh Dominion | Marchgun Ordnance | Machine guns, missile launchers, ammunition | Damage +, energy − |
| Ostrova Collective | Spirewright | Ostrova hulls, scanners, beacon devices, limpets, mining lasers | Sensor-heavy frames |
| Ostrova Collective | Archive Dynamics | Reactors, drives | Energy +, shields − |
| Mirrorwater (freeport) | Mirrorwater Arms | Weapons of every kind | Sells to anyone, no standing gate |
| Mirrorwater (freeport) | Quicksilver Hullworks | Hull upgrade kits, armour, and licensed builds of faction hulls | Builds any faction's design for anyone |
| Coldwater Drift (freeport) | Coldwater Refit | Refurbished parts from salvage | Cheap; grades 1–3 only, slightly worse |
| Coldwater Drift (freeport) | Coldwater Prospecting | Mining lasers, charge launchers, scanners | Mining yield +, combat − |
| Ember Wake (freeport) | Ember Wake Drives | Drives, reactors, cargo modules | Long-burn and freight specialists |
| Ember Wake (freeport) | Wakefire Munitions | Ammunition, missiles, torpedoes, blast charges | Payload for anyone; the steady seller |
| Freeport Compact | (the Compact itself) | Compact Seals, Calibration Matrices | As in Driftgate 1 |

- **Real factories.** Each maker's works sits at its home station and turns components into parts at a set rate, for sale on that station's market.
- **The war uses the same stock.** A faction's AI fleets are fitted from its makers' output. A faction that's losing burns through that stock, so those parts get scarce and dear for contractors, and the freeport makers become the reliable source. Prices tell you where the war is.
- **Product lines replace variants.** Driftgate 1's variants become specific makers' products: Brightline makes the Bastion and Flicker shields, Marchgun makes Heavy and Rapid machine guns, and so on.

### 5. Unique hull designs
In Driftgate 1 every faction flies the same model for each hull class, with a name and a ±12% trait. In Beyond each design is **its own, in look and in stats**. **Only the factions design hulls:** distinct faction ships, distinct Unbound ships, and the Brood's grown ships. The freeports have no designs of their own; their yards build the factions' designs.

- **Every faction builds every class its own way,** one design per class. Each faction has a light fighter, and no two are the same. As a starting sketch:
  - **Halcyon Swift:** fast and light, strong shields, thin hull.
  - **Varkesh Fang:** slower and heavily armoured, an extra weapon slot, a hungry reactor.
  - **Ostrova Mote:** a deep reactor, the best sensors and lock range, weak shields.
- **Stats differ in more than one number:** hull, shield, energy, mass, top speed, turn, acceleration, hold, weapon slots, other slots and silhouette size. Two light fighters should fly differently and suit different parts.
- **Own models,** built from kit parts (`tools/build_models.py`) or hand-built in code like the Heavy Bomber and the Gannet, so you tell a Fang from a Swift at a glance.
- **The Unbound have their own designs,** carried over and extended from Driftgate 1's Raider, Corsair, Plunderer and Skiff. **The Brood** keeps its grown ships.
- **Freeport yards build faction designs** (Quicksilver Hullworks at Mirrorwater), so a contractor in poor standing with a faction can still fly its ships, at a freeport price.
- **AI fleets fly their own power's designs,** so you learn to read a Varkesh wing by its shapes.
- **Balance rule:** within a class, no design wins more than about 60% of its mirror duels against another at the same grade (`tools/duel.py`). They differ in how they win, not whether.
- **Scale:** three factions × about 12 classes is around 36 designs, plus the Unbound set. Build in waves: fighters first, then miners and haulers, then bombers, then scouts, then capitals. A class keeps the shared model with the faction trait until its designs exist.

### 6. Ships: slots and weapons
A ship is a hull with slots. Each slot takes one part from any maker, or one you built.

| Slot | Takes |
|---|---|
| Hull | Sets mass, hold, slot counts and handling |
| Drive, Reactor, Shield, Armour | One part each |
| **Weapon slots** (number varies by ship) | One each: machine gun, laser, missile launcher, torpedo launcher; on mining hulls only, mining laser or charge launcher |
| Utility | Cargo module, scanner, drone bay, beacon device, limpet rack |

**Weapons, each in its own slot, each limited differently:**
- **Machine gun (kinetic):** strong against hull; you must lead your shots. **Limited by ammunition:** rounds are payload, bought or built, carried in the ship.
- **Laser:** hits instantly, strong against shields. **Limited by reactor energy:** no ammunition, but it drains the reactor fast, so a better reactor means more laser time.
- **Missile launcher:** fires missiles from a magazine. **Limited by payload:** missiles are items, rearmed at a dock, never reloaded in flight. Because they run out, each hits harder (proposal: about twice a Driftgate 1 missile).
- **Torpedo launcher:** the same, on bomber hulls only; still the siege weapon.

**Mining, in the same slots:**
- **Mining laser (back from Driftgate 1, reworked):** slow, steady mining. Scan a rock and it shows its **ring**, a seam around the rock; hold the beam on the ring to cut ore steadily. Draws on the reactor like a combat laser. Quiet and safe, but slow.
- **Charge launcher:** Driftgate 1's blast charges. Scan for fault points, place charges and blow the rock apart for a big, fast yield with the risk of a bad blast. Charges are payload.
- **One way per rock.** A blast breaks the rock's ring, so for each rock you choose: slow and safe with the laser, or fast and risky with charges.
- **Only mining hulls can fit mining equipment.** Mining lasers and charge launchers go only in a mining hull's weapon slots. A miner can still carry a gun in a spare slot, at the cost of mining tools; no other hull can mine.

**Flares and drones stay as in Driftgate 1.** Flares run on reactor energy with a cooldown; drones are restocked when you dock.

**Fire controls:** one key per weapon type fitted (replacing 1 and 2), C for launchers as now, the mining keys as now. Starting proposal for slot counts: Light Fighter 3, Medium 3–4, Heavy 4–5; miners 2–3; haulers 1–2; bombers 2 plus the torpedo launcher. These vary by power's design.

### 6a. Scouting: intel as a trade good
Player scouting comes back in a different form: what you find and do is intel, and intel sells. The powers' AI scouts still fly the routine recon.

- **Beacon device.** Load a beacon device (payload, one use) and flip a sector's beacon to the faction **you choose**. That faction pays for it, offers you jobs in that sector, and you get the beacon's intel: a scan of the system and its prices. Choosing who to flip a beacon to is a way to court a faction, or to sell a sector to its rival.
- **Hired intel work.** Factions hire you to **ping a rival's capital ships** (find and mark them) or **place a limpet** on a target, as in Driftgate 1 (a limpeted target is hit harder by the side that ordered it).
- **Discoveries.** Find and sell **comets, derelict cargo and wreckage from anomalies**. Sell the find as intel to a faction or the Compact, or salvage it yourself.
- **Anomalies move out beyond the gates.** They sit far out past the gate ring, away from the lanes, so finding them means flying out into the empty edge of a system.
- **Ostrova's edge.** Ostrova pays a bonus on intel work (section 12a).

### 7. What you spend on: the ladder
Players have several things to spend money and materials on, in this order, each with its own levels:

| Step | What it is | Levels (proposal) |
|---|---|---|
| 1. Ships | Build hulls up the Rating ladder | Light → Medium → Heavy → specialist |
| 2. Hull upgrades | Upgrade the hull you fly | Levels 1–3: stats only (hull, shield, energy or hold); slots never change |
| 3. **Lair** | Your first base, hidden in a large asteroid | 1–2 |
| 4. **Depot** | Your first open base, with a market and a hangar | 1–3 |
| 5. **Station** | A full station that counts for the system | 1–5, plus station upgrades |
| 6. Capital ships | Built at your stations | Escorts, then carriers |

#### Lair (from Driftgate 1's Unbound Lair)
- **Building:** a Rigger kit (proposal: 1 Depot Frame + 20 plate) set into a large asteroid in any system with no station.
- **Hidden** until a scout of a hostile power comes within range (AI scouts find Lairs, as in Driftgate 1).
- **Level 1:** stash (200 t), repairs and rearming.
- **Level 2:** your own workshop (components, parts, upgrades and payload with no fee), a forge (lattice, core), a bigger stash, and a spare berth to keep a second ship.
- One Lair per system.

#### Depot
- **Building:** upgrade a Lair in place, or build fresh (proposal: 2 Depot Frames, as Driftgate 1's `DEPOT_COST`). Visible on every map, with a market.
- **From Depot level 1 you can hire and build AI ships and pilots** (section 8). Its hangar holds them.
- **Your market earns.** AI merchants and other pilots trade with your depot; you set what it buys and sells, and the margins are your income.
- **Levels 1–3** reuse Driftgate 1's depot modules: storage, production, defence, armour, hangar, life support.

#### Station
- **Building:** upgrade a Depot (proposal: Capital Keels, Depot Frames and Compact Seals).
- **Your choice of look:** an asteroid station, built into the rock like Driftgate 1's Scrapheart Haven, or a standard station like the factions' own. Purely cosmetic: both have the same stats, levels and upgrades.
- **A station counts for the system**: owning it gives you the system, as Driftgate 1's `sectorOwner` does for faction stations. This is the road to the 7-system win.
- **A shipyard:** builds hulls for you and your AI.
- **Levels 1–5, plus station upgrades** (defence, shields, armour, hangar, production, docks). What each level opens is still to design.
- **Capital ships** are built here (proposal: escorts from Station level 3, carriers from level 5).

### 8. Your AI: pilots, ships and upkeep
- **From the Depot on,** you hire AI pilots and build or buy them ships. They fly for you: mining, hauling between your bases, guarding, escorting your convoys, patrolling, raiding.
- **Upkeep is credits plus goods.** Each AI pilot draws wages in credits every hour. Each ship uses up goods from your stores for repairs, payload and running costs.
- **Income:** your markets' sales, jobs you complete, and your AI's work (the ore your miners bring home, the goods your haulers sell).
- **Credits stay zero-sum.** Wages go to the Compact (it supplies the crews; proposal) and running costs consume goods into Driftgate 1's drift, as life support already does.
- **If you can't pay,** pilots leave and ships are laid up until you can.

### 9. Screens to build
| Screen | What it does |
|---|---|
| **Holdings** (Lair → Depot → Station) | Every base you own, its level, its modules, and what the next level or upgrade costs in goods and credits. Build and upgrade from here. |
| **Economy** | Income and costs: market sales, jobs, AI upkeep, wages. Treasury, stock at each base, and what each base buys and sells. |
| **Job creation** | Post jobs: to your own AI pilots (mine this field, haul this cargo, escort, patrol, defend) and, in multiplayer, to other contractors, paid from your treasury. |
| **Faction jobs** | What the factions and freeports will hire you for, filtered by your standing: pay, risk, standing gained, the faction bonus. |
| **Strategic map** | The galaxy map, zoomable into a sector to see your bases, AI ships and the threats there, and give orders to your AI in that sector. |

These reuse what Driftgate 1 has where they can: the station's task tabs, the Jobs board, the galaxy map and its sector panel.

### 10. Progression: Contractor Rating (replaces Legend levels)
- **Rating 1–10, per galaxy,** rising with Rating points from completed jobs (weighted by risk), kills on a job, deliveries, intel sold and stationworks built.
- **Rating only goes up.** Failure costs standing and money, never Rating.
- **Hulls unlock by Rating, then cost credits and materials:**

| Rating | Hulls you may build |
|---|---|
| 1 | Starters: Light Fighter, Light Miner, Light Hauler |
| 2 | Medium Fighter, Medium Miner, Medium Hauler |
| 4 | Heavy Fighter, Bomber |
| 5 | Heavy Miner, Heavy Hauler |
| 6 | Heavy Bomber; house-brand hulls with Partner standing |
| Station level 3 | Escort |
| Station level 5 | Carrier |

- **Parts unlock by Rating and cost:** grade 1 at Rating 1, 2 at 2, 3 at 4, 4 at 6, 5 at 8. A maker's grade 4–5 parts also need Trusted or Partner standing with its power.
- **Across galaxies (replaces Legend): deferred.** Legend can't carry over as it is, because one pilot can now own a faction. We'll come back to what a callsign carries between galaxies.

### 11. Declaring a faction
- **The only requirement is a Station.** Once you own one base at Station level, you can declare.
- **Losing your last Station ends it.** A declared faction that loses its last Station falls back into a company: it is no longer a contender, but keeps its Lairs, Depots, ships and AI. Win back or build a Station and you can declare again.
- **Once declared,** you're a contender: you win by holding 7 systems for 20 minutes, the three powers treat you as a rival, and the truce-against-the-leader rule applies to you. Your standings with them drop to a war footing.
- **Your faction runs on Driftgate 1's strategic AI,** steered by your orders on the strategic map and the jobs you post.

### 12. The war around you
- **The three factions fight on, AI-driven:** campaigns, depots, forges, sieges, capitals, the truce against the leader.
- **The Brood is stronger:** more presence, and it wins about **20%** of AI-only galaxies (Driftgate 1: 10–13%). Containment pays every contractor.
- **The AI Unbound stay** as the galaxy's raiders: a threat to your convoys and bases, and bounty work for you.
- **The Freeport Compact stays neutral,** the marketplace of last resort and the independent makers' home.

### 12a. Faction job bonuses (from Driftgate 1's careers)
Each faction pays contractors a bonus on the work it cares most about, out of its own treasury, shown on the job:
- **Halcyon:** hauling jobs.
- **Varkesh:** mining jobs.
- **Ostrova:** intel work (beacon flips, pings, limpets, discoveries) and escorts.

Their signature hulls survive as house-brand hulls built with Partner standing: the Gannet (Halcyon), the Bombard (Varkesh) and the Vesper (Ostrova).

### 13. Multiplayer: rival companies
- **Each pilot runs their own company.** Friends can partner (post jobs for each other, share convoys) or compete.
- **Pilots can fight each other** when their companies are at odds, or on jobs for opposite sides. Standing between companies works like standing with a power.
- **The host model stays:** the host simulates, guests send inputs, and guest actions run on the host through `runAs` and `dockAction`.

### 14. Galaxy length and pacing
- **A galaxy is played over several sessions.** Growing from one light ship to a declared faction needs room. A galaxy already freezes while nobody is online.
- **The war's clock slows to match.** Capitals from minute 45, the 2-hour deadline and Overgrowth from minute 20 all need new values. Working target for tuning: a typical galaxy is won in about 8–12 hours of play (no firm preference yet).

### Rules Beyond keeps
- **The ledger is exact.** Components, parts, payload, bases and AI ships are all made of real goods from real rock.
- **The host simulates;** guests send inputs.
- **The war is checked by simulation.** New target for AI-only galaxies: the Brood about 20%, the three factions sharing the rest evenly (about 27% each). Until the Brood change is built, Driftgate 1's target in CLAUDE.md still applies.

### Decided in review (2 Nov 2026)
Hull upgrades are stats only · a blast breaks a rock's ring · AI upkeep is credits plus goods · your own brand from Depot level · Brood about 20% · Rating only goes up · a choice of three starting freeports · faction careers become job bonuses and the signature hulls survive · scouting returns as intel · flares stay on energy, drones restock at dock · only factions (and the Unbound and Brood) design hulls; freeports build faction designs · Lair 2 levels, Depot 3, Station 5 · makers' names kept for now · declaring needs only a Station · losing your last Station drops you back to a company · asteroid or standard station look.

### Open questions
1. **Legacy across galaxies** (deferred). What does a callsign carry from one galaxy to the next?
2. **Which hulls carry intel gear?** Beacon devices and limpet racks: scout hulls only (scout hulls return, not as a starter), or any hull with a utility slot?
3. **Beacon rights.** What does flipping a beacon to a faction earn you exactly, and how long does it hold?
4. **Station levels 1–5.** What does each level open (modules, yard size, capitals, defences)?
5. **Lair, Depot, Station costs.** All numbers are guesses to tune.
6. **Own-brand traits.** Choose from a fixed list of traits, or build your own strength-and-weakness pair?
7. **Unbound designs for contractors.** Can a contractor build Unbound ships, and where?
8. **Freeport licensed builds.** Which faction designs do freeport yards sell, and do the house-brand hulls stay faction-only?
9. **AI wages.** Paid to the Compact, as drafted?
10. **Galaxy length.** Confirm 8–12 hours of play in tuning; should the 7-system win scale up?

### Proposed build order (once the design is agreed)
1. **Cut the faction tie:** start at a chosen freeport with three equipped starters; standing with every power; docking and hostility from standing; pay from the issuer; faction job bonuses.
2. **Weapon slots and weapons:** slot counts per hull; machine gun with ammunition, laser on reactor energy, missile and torpedo payload; mining laser with rings and charge launchers in mining hulls' weapon slots.
3. **Making things:** ore → components → parts → upgraded parts; grades replace Mk.
4. **Faction jobs screen,** with intel jobs: beacon devices, capital pings, limpets, and discoveries out beyond the gates.
5. **Unique hull designs, first wave:** each faction's fighters, with their own models and stats, duel-balanced; freeport yards build them.
6. **Makers:** the corporations, their works and stock; product lines replace variants; AI fleets fitted from their makers.
7. **Progression:** Contractor Rating gates hulls and grades; hull upgrades; remove Legend; drop Unbound mode.
8. **Lairs and the Holdings screen.**
9. **Depots:** markets, hiring and building AI with upkeep; the Economy and Job creation screens.
10. **Stations and station upgrades;** capital ships built at your stations.
11. **Strategic map** with sector zoom and orders.
12. **Declaring a faction;** slower war pacing; a stronger Brood (about 20%); war checks for the new balance.
13. **Legacy, multiplayer rivalries, training rewrite.**
