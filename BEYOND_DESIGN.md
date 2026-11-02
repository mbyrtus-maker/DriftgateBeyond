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
| Combat feel, shields, sub-targets, capitals and bridges | Pay from your faction's treasury → paid by **whoever issued the job** | **Legend levels** as they are (reworked, see section 10a) |
| Blast charges, salvage, hauling, convoys | Blast rig only → **mining lasers back** alongside charges, both in a mining hull's weapon slots | Mk I–III as one shared ladder (replaced by grades) |
| The three factions, their AI war, campaigns, depots, sieges | One Weapons system for gun and laser together → **separate parts in weapon slots**; slot count varies by ship | Scout hulls as a starter |
| **The Brood,** stronger: more presence, about 20% of galaxies | Free kinetic fire → **machine guns use ammunition**; lasers draw on the reactor | |
| **AI Unbound raiders** in the galaxy | Missiles that reload by themselves → **payload** you carry, which hits harder | |
| AI scouts: beacons, limpets, recon, Seeder spotting | Scouting as a career → **intel as a trade good**: beacon devices, pings, limpets and discoveries you sell | |
| Anomalies, wrecks, quiet-space signals | Moved **out beyond the gates**, as discoveries to find and sell | |
| Freeports and the Compact, Seals and Matrices (freeport yards build a random set of faction designs) | Unbranded goods → **corporate parts** with a maker and a trait | |
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
- **Your own brand, from Depot level.** Parts built at your Depot's or Station's workshop carry your company's name and your trait, and sell on your market like any maker's. Parts from a Lair are standard.
- **Your trait is set with points, with trade-offs.** Each strength you buy (more damage, more shield, faster recharge, more hold…) costs points, and you earn points back by taking weaknesses. The budget nets to zero, so a brand is a shape, not a free gain. Proposal: one set of points per part type (weapons, shields, drives…), changeable at a cost.
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
- **The Unbound have their own designs,** carried over and extended from Driftgate 1's Raider, Corsair, Plunderer and Skiff. They fly them only: contractors meet and salvage Unbound ships but never build them. **The Brood** keeps its grown ships.
- **Freeport yards build a random assortment of faction designs,** rolled for each freeport when the galaxy is created. So a contractor in poor standing with a faction may still fly its ships, if a freeport happens to build them.
- **House-brand hulls are never traded.** The Gannet, Bombard and Vesper are only sold at their own faction's station.
- **AI fleets fly their own power's designs,** so you learn to read a Varkesh wing by its shapes.
- **Balance rule:** within a class, no design wins more than about 60% of its mirror duels against another at the same grade (`tools/duel.py`). They differ in how they win, not whether.
- **Scale:** three factions × about 12 classes is around 36 designs, plus the Unbound set. Build in waves: fighters first, then miners and haulers, then bombers, then the scouts, then capitals. A class keeps the shared model with the faction trait until its designs exist.

### 6. Ships: slots and weapons
A ship is a hull with slots. Each slot takes one part from any maker, or one you built.

| Slot | Takes |
|---|---|
| Hull | Sets mass, hold, slot counts and handling |
| Drive, Reactor, Shield, Armour | One part each |
| **Weapon slots** (number varies by ship) | One each: machine gun, laser, missile launcher, torpedo launcher; on mining hulls only, mining laser or charge launcher |
| Utility | Cargo module, scanner, drone bay, landing kit; on scout hulls only, beacon device or limpet rack |

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

**Asteroid landing is a kit you install.** In Driftgate 1 any ship can land on a rock (E with nothing to dock at): it settles on the surface, its systems go down and it drops off enemy sensors beyond close range. In Beyond that needs a **landing kit** fitted in a utility slot; without one, E never offers to land on a rock. It's a part like any other (built, bought or from a maker), so hiding on an asteroid costs a slot.

**Flares and drones stay as in Driftgate 1.** Flares run on reactor energy with a cooldown; drones are restocked when you dock.

**Fire controls:** one key per weapon type fitted (replacing 1 and 2), C for launchers as now, the mining keys as now. Starting proposal for slot counts: Light Fighter 3, Medium 3–4, Heavy 4–5; miners 2–3; haulers 1–2; bombers 2 plus the torpedo launcher. These vary by power's design.

### 6a. Scouting: intel as a trade good
Player scouting comes back in a different form: what you find and do is intel, and intel sells. The powers' AI scouts still fly the routine recon.

- **Scout hulls return,** not as a starter: each faction designs a Scout and an Advanced Scout, unlocked by Rating. Only scout hulls carry beacon devices and limpet racks, as only mining hulls carry mining gear.
- **Beacon device.** Load a beacon device (payload, one use) and flip a sector's beacon to the faction **you choose**. That faction pays you a fee and you gain standing with it; you lose standing with the faction you flipped it from. Choosing who to flip a beacon to is how you court a faction, or sell a sector to its rival.
- **Hired intel work.** Factions hire you to **ping a rival's capital ships** (find and mark them) or **place a limpet** on a target, as in Driftgate 1 (a limpeted target is hit harder by the side that ordered it).
- **Discoveries.** Find and sell **comets, derelict cargo and wreckage from anomalies**. Sell the find as intel to a faction or the Compact, or salvage it yourself. (Proposal: finding them needs a scanner, which any hull can fit in a utility slot; scout hulls find them farthest out.)
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
| 6. Capital ships | Built at your stations | Escorts, then destroyers, then carriers |

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
- **Your choice of look:** an asteroid station, built into the rock like Driftgate 1's Scrapheart Haven, or a standard station. Purely cosmetic: both have the same stats, levels and upgrades. **The standard look is the neutral company style** (decided 2 Nov 2026), shared with the freeports and painted in your company colour: round drums, lattice trusses, cargo containers, radiators, tanks, amber trim and floodlights. **Each of the three factions' own stations has its own design language,** as their ships do.
- **A station counts for the system**: owning it gives you the system, as Driftgate 1's `sectorOwner` does for faction stations. This is the road to winning the galaxy (section 11).
- **Levels 1–5 come from external buildings.** Each new level lets you add **one building of your choice** around the station, from six: **shipyard, external storage, defence platform, hangar, forge, market wing** (decided 2 Nov 2026). Five levels, five buildings, so no two stations are the same. You see your station grow, and an attacker can target its buildings one at a time.
- **The shipyard** is one of these buildings: it builds hulls for you and your AI.
- **Capital ships** are built at the yard, which must be among the station's buildings: **escorts** from station level 3, **destroyers** from level 4, **carriers** at level 5.
- **The destroyer** (decided 2 Nov 2026) is the line ship between the escort and the carrier: bigger than an escort, smaller than a carrier, built around a **main gun** that kills other capitals and stations, with **point-defence turrets** like the other capitals. It has no hull berths and no assault bay (the escort keeps those), so it is weak against swarms of small ships on its own. **The main gun fires a charged shot:** it has to charge before each shot, and **while it charges the ship's shields are down**, so every shot is a window an enemy can punish (charge time, damage and the shield drop are tuning numbers).

### 8. Your AI: pilots, ships and upkeep
- **From the Depot on,** you hire AI pilots and build or buy them ships. They fly for you: mining, hauling between your bases, guarding, escorting your convoys, patrolling, raiding.
- **Upkeep is credits plus goods.** Each AI pilot draws wages in credits every hour. Each ship uses up goods from your stores for repairs, payload and running costs.
- **Income:** your markets' sales, jobs you complete, and your AI's work (the ore your miners bring home, the goods your haulers sell).
- **Credits stay zero-sum.** Wages go to the Compact, which supplies the crews, and running costs consume goods into Driftgate 1's drift, as life support already does.
- **If you can't pay,** pilots leave and ships are laid up until you can.

### 9. Screens to build
| Screen | What it does |
|---|---|
| **Holdings** (Lair → Depot → Station) | Every base you own, its level, its modules, and what the next level or upgrade costs in goods and credits. Build and upgrade from here. |
| **Economy** | Income and costs: market sales, jobs, AI upkeep, wages. Treasury, stock at each base, and what each base buys and sells. |
| **Job creation** | Post jobs: to your own AI pilots (mine this field, haul this cargo, escort, patrol, defend) and, in multiplayer, to other contractors, paid from your treasury. |
| **Faction jobs** | What the factions and freeports will hire you for, filtered by your standing: pay, risk, standing gained, the faction bonus. |
| **Allegiance** | Your standing with every power (the three factions, the Compact, each player faction), its band and what it opens; the relations between the factions themselves (at war, truce, allied, neutral), so you can see how a job for one lands with the others; each leader and their recent decisions. Declare or renounce allegiance here; a founder answers other factions' proposals here. |
| **Strategic map** | The galaxy map, zoomable into a sector to see your bases, AI ships and the threats there, and give orders to your AI in that sector. |

These reuse what Driftgate 1 has where they can: the station's task tabs, the Jobs board, the galaxy map and its sector panel.

### 10. Progression: Contractor Rating (replaces Legend levels)
- **Rating 1–10, per galaxy,** rising with Rating points from completed jobs (weighted by risk), kills on a job, deliveries, intel sold and stationworks built.
- **Rating only goes up.** Failure costs standing and money, never Rating.
- **Hulls unlock by Rating, then cost credits and materials:**

| Rating | Hulls you may build |
|---|---|
| 1 | Starters: Light Fighter, Light Miner, Light Hauler |
| 2 | Medium Fighter, Medium Miner, Medium Hauler, Scout |
| 4 | Heavy Fighter, Bomber, Advanced Scout |
| 5 | Heavy Miner, Heavy Hauler |
| 6 | Heavy Bomber; house-brand hulls with Partner standing |
| Station level 3, with a yard | Escort |
| Station level 5, with a yard | Carrier |

- **Parts unlock by Rating and cost:** grade 1 at Rating 1, 2 at 2, 3 at 4, 4 at 6, 5 at 8. A maker's grade 4–5 parts also need Trusted or Partner standing with its power.
- **Across galaxies:** Legend, reworked (section 10a).

### 10a. Legend: what carries between galaxies
Starting from nothing in every galaxy doesn't fit a game where you can build up to a Station. Legend has two parts: **Legend levels**, which build up across every galaxy you play, and **Conqueror's spoils**, a one-off reward for the pilots who won the last galaxy. Kept per callsign on the device, as Driftgate 1's Legend is.

**Earning Legend points** (kept for good)

| Achievement in a galaxy | Points |
|---|---|
| Reach Rating 5 | 1 |
| Reach Rating 10 | 1 more |
| Build a Lair | 1 |
| Build a Depot | 1 |
| Build a Station | 2 |
| Declare a faction | 2 |
| Kill an ace, or a Brood Hive Ship | 1 |
| Your faction wins the galaxy | 6 |
| Your faction is allied with the winner | 3 |
| The Brood wins | No win points for anyone |

A solid galaxy that ends at Depot level earns about 4 points. A founder whose faction conquers the galaxy earns 15 or more.

**Legend levels: pick your start.** Each level unlocks a perk. At the start of every galaxy you choose a start package from the perks you've unlocked: each perk costs as many start points as its level, and your budget is your Legend level. A level 10 pilot can take the Station on its own, or Rating 2, the credits, a medium hull and three grade 2 parts (1+2+3+4), or any other mix up to 10. So veterans start differently.
- **Titles are free:** you always carry the highest title you've earned.
- **Rating perks don't stack:** pick one (Rating 2, 4 or 6).
- **One base perk:** a Lair kit, a Depot or a Station, not more than one.

| Level | Points to reach | Perk (costs its level in start points) |
|---|---|---|
| 1 | 2 | Start at Rating 2 · title *Journeyman* |
| 2 | 4 | +5,000 starting credits |
| 3 | 7 | Start in a fully equipped medium hull of your choice |
| 4 | 10 | Three grade 2 parts of your choice, fitted free |
| 5 | 14 | Start at Rating 4 · title *Veteran* |
| 6 | 18 | A Lair kit in your hold: build a level 1 Lair anywhere at the start |
| 7 | 23 | House-brand hulls need only Trusted standing, not Partner |
| 8 | 28 | Start with a level 1 Depot in a system of your choice |
| 9 | 34 | Start at Rating 6 · your brand starts with extra trait points |
| 10 | 40 | Start with a level 1 Station (you can declare a faction from the first minute) · title *Founder* |

**Conqueror's spoils** (next galaxy only, on top of the start package; not paid for with start points)

| Spoil | What you get |
|---|---|
| Flagship | The ship you left the last galaxy with carries forward, with its fitted parts (not a capital ship) |
| War chest | 10% of your faction's treasury at the win, up to 25,000 cr |
| Veteran crew | Three AI pilots who serve without wages for your first 2 hours once you own a Depot |
| Renown | Start Trusted (+25) with every power |
| The Wraith | Driftgate 1's top hull returns as a trophy, built only by former conquerors |

- **The winning faction** (every pilot who flew for it: its founder, and every pilot sworn to it by allegiance) gets the full spoils.
- **Allied factions** get half: half the war chest, one veteran pilot, Renown at +12. The Flagship and the Wraith are for the winning faction only.

- **The ledger:** anything a pilot carries into a new galaxy (a flagship, parts, kits, a starting base) is added when the galaxy is created and counted in its starting ledger, so the economy stays exact from that point on.

### 11. Declaring a faction
- **The only requirement is a Station.** Once you own one base at Station level, you can declare.
- **Losing your last Station ends it.** A declared faction that loses its last Station falls back into a company: it is no longer a contender, but keeps its Lairs, Depots, ships and AI. Win back or build a Station and you can declare again.
- **Once declared,** you're a contender: you can win the galaxy (below), and the truce against whoever starts the two-thirds timer applies to you too. Your faction starts Neutral with every other faction (11b); how the powers treat you from then on is up to the ledger and their leaders.
- **Your faction runs on Driftgate 1's strategic AI,** steered by your orders on the strategic map and the jobs you post.

### 11a. Allegiance: flying for a faction instead (an option)
A pilot doesn't have to build their own faction. At **Partner** standing (the top band) with a faction, you may **declare allegiance** and fly for that faction, much as a Driftgate 1 pilot did.
- **You fly as one of theirs:** you dock at its stations as a member, earn its war effort, get its job bonuses and house-brand hulls, and share its win in full (6 Legend points and the full Conqueror's spoils).
- **Its enemies become yours:** your standing with its rivals drops to a war footing.
- **Your owned assets become the faction's.** When you swear, your Lairs, Depots and Stations with their stores, and your AI pilots with the ships they fly, become that faction's, so a Station you held now counts as one of its systems.
- **Your personal holds and wealth stay yours:** your credits, the ship you fly, its hold and your personal vault space.
- **You can't declare your own faction while sworn.**
- **Player factions: any time.** You can apply to swear allegiance to another player's declared faction at any time; no Partner standing is needed, but its founder must accept your application. That's how a multiplayer crew joins one pilot's faction.
- **Renouncing costs your reputation** with that faction: your standing with it is lost (back to 0). What you handed over when you swore stays with the faction.
- **Swearing again** to one of the three factions needs Partner standing with it again, earned from scratch.
- **Player factions have no such limits.** A pilot can swear, renounce and swear again to any player faction, the same or another, at any time; the only gate is the founder's approval or denial.

### 11b. Relations between factions: the faction status ledger
Factions aren't locked at war with each other. Every pair of factions (the three powers and each player faction) has a **relation** from −100 to +100, kept in a background **faction status ledger**. Every interaction between two factions is logged as a positive or a negative and moves their relation. Factions become allies simply by trading and not fighting.

| Interaction between two factions | Effect (starting guesses) |
|---|---|
| Trade: a sale at the other's station, a merchant or convoy run to it, an import from it | + small, scaled by value |
| A job done for the other (by its ships or its sworn pilots) | + small |
| A ship of the other destroyed | − small (more for capitals) |
| A convoy raided, a beacon flipped away from it | − |
| A siege, or a depot or station captured or razed | − large |

| Relation | Band | What it means |
|---|---|---|
| below −50 | War | Ships fight on sight; sieges and campaigns against each other |
| −50 to −10 | Hostile | Skirmishes; no docking for each other's ships |
| −10 to +25 | Neutral | Trade and docking; no campaigns against each other |
| +25 to +60 | Friendly | Trade at better prices; convoys pass unharmed |
| above +60 | **Allied** | Never fight; dock at each other's stations; share in each other's win (half spoils) |

- **What counts:** the acts of a faction's own ships and of pilots sworn to it. An unsworn contractor's work counts only for the pilot's own standing.
- **Allies still hire contractors against each other.** Because contractor work doesn't touch the ledger, it's deniable: an ally can quietly post jobs against its ally on the Faction jobs board (raid this convoy, flip that beacon). Only if the job is exposed (event table, 11c) does it count.
- **All factions start Neutral,** the three powers included, and so does a newly declared player faction. Wars aren't given; they grow out of what happens: interactions on the ledger and the leaders' decisions (11c).
- **Never:** the Brood and the Unbound have no relations; they're always hostile.
- **The AI joins in.** AI factions trade, avoid fights and drift toward alliance by the same ledger, so an alliance between two powers can form, or break, on its own. That moves the war's balance, so it goes through a war check.
- **Shown on the Allegiance screen** as the relations between every pair of factions, with the recent entries that moved them.

### 11c. Leaders and faction events
Each of the three powers is run by a **leader with a personality**. Leaders make decisions for or against other factions: pacts, embargoes, reprisals, wars, peace, betrayals. Events must never feel random. **Every event has a cause in the galaxy, a leader whose character explains it, and a clear announcement of why.**

**Leaders** (names and traits are placeholders)

| Power | Leader | Traits | Leans toward |
|---|---|---|---|
| Halcyon Accord | Chair of the Merchant Houses | Mercantile, Cautious | Trade pacts and embargoes over war; makes peace when trade suffers |
| Varkesh Dominion | the Marshal | Ambitious, Vengeful | Border claims, reprisals, war; remembers every wrong |
| Ostrova Collective | the First Archivist | Scheming, Patient | Deniable contractor jobs, intrigue, alliances of convenience; strikes late |

A player faction's leader is its founder: AI leaders send it proposals and demands, and the founder answers them on the Allegiance screen.

**Leaders exist in the world.** A leader is a pilot you can meet, not a name in a menu.
- **Out flying, rarely docked.** A leader docks only for a few minutes at a time; the rest of the time they're in space doing what their faction does.
- **Their ship fits their role.** An admiral on a capital ship; an ace in a combat ship; a renowned trader or miner in a hauler or miner, the best in the galaxy at it. Their traits lean the choice: an Ambitious leader commands a carrier, a Mercantile one runs freight.
- **Always with an ace escort,** whatever hull they're in.
- **They can die.** A leader shot down is a huge event: it triggers a succession, and the killer's faction (or the pilot, if an unsworn contractor did it) takes a very large hit on the ledger and in standing. A successor whose leader was killed leans Vengeful against the killer.
- **They make work.** Factions hire contractors to escort their leader, and rivals post deniable jobs to hunt one. A leader sighting is intel that sells.
- **Meeting one matters:** a leader's ships appear on radar by name, and docking where a leader is docked can open their faction's best jobs.

**Events** (each needs its trigger; personality weights which eligible event a leader picks)

| Event | Trigger (the reason) | Who leans to it | What happens | Ledger |
|---|---|---|---|---|
| Trade pact | Relation Neutral or better, and each is short of goods the other has in surplus | Mercantile | Cheaper trade, merchants run between them | + |
| Aid convoy | A Friendly or Allied faction is under siege or starved | Cautious, Patient | Goods sent by real convoy (raidable) | + |
| Alliance proposal | Relation above +60 and a shared threat (a faction nearing two-thirds, or the Brood spreading) | Patient, Cautious | Formal alliance if the other accepts | + large |
| Border dispute | Both factions build or hold depots in neighbouring systems | Ambitious | A demand to withdraw; announced with a deadline | − small |
| Embargo | Relation Hostile, or the other undercut its markets or raided its trade | Mercantile, Vengeful | Trade between them stops | − |
| Proxy work | A rival (or even an ally) is getting ahead | Scheming | Deniable contractor jobs posted against it | none, unless exposed |
| Exposure | A proxy job is traced (more likely if many run, or a sworn pilot does it) | (anyone exposed) | The victim learns who posted it | − large |
| Reprisal | A large negative from the other (a siege, a capture, repeated convoy raids) | Vengeful | A strike or raid back at the offender | − |
| Declaration of war | Relation below −50 and an unanswered wrong, or a rival leading in systems | Ambitious, Vengeful | Formal war: campaigns and sieges begin | − large |
| Ceasefire offer | War-weary: heavy losses, a low treasury, or the Brood pressing both | Cautious, Mercantile | Offer of peace; holds if the other is also weary | + |
| Betrayal | Allied, but the ally nears two-thirds or is rich and weak | Ambitious, Scheming | Alliance broken; telegraphed by cooling relations first | − very large |
| Containment front | The Brood holds enough systems | Everyone | Driftgate 1's Containment Accord: all unite against the Brood | + between all |
| Bounty on a pilot | A contractor badly hurts the faction | Vengeful | A public bounty on that pilot (affects standing, not the ledger) | none |
| Succession | The leader is killed, its core station falls, a long losing war, a betrayal by an ally, or an exposed scheme | (any) | A new leader whose traits come from the faction's history (below) | partial reset, or a new grudge |

**Successors are shaped by what happened.** A new leader's traits come from the faction's story in this galaxy, so a reversal always has a reason:

| What happened to the faction | The successor is likely to be |
|---|---|
| Lost systems or its core station to a rival, or its leader killed | Vengeful, with a grudge against that rival or killer |
| Bled by a long war, heavy losses | Cautious: seeks ceasefires and pacts |
| Trade ruined by embargoes | Mercantile |
| Betrayed by an ally | Wary: slow to trust, quick to break pacts |
| Saved by allies or aid convoys | Loyal: honours alliances, never betrays |
| Grew fast by conquest | Ambitious |
| Ravaged by the Brood | Zealous: puts containment above everything |
| Hurt by an exposed proxy campaign | Scheming: answers in kind |
| Long peace and full treasuries | Patient or Mercantile |

**Storylines, not fixed alignments.** Nothing is permanent. Over a galaxy, two factions can go from wars of annihilation to friendship and back: a war, a weary ceasefire, a new Cautious leader, a trade pact, a shared fight against the Brood, an alliance, then a betrayal by an Ambitious successor. Each step has its trigger, and the Allegiance screen keeps a **chronicle** of each faction's leaders and decisions so the story can be read back.

**Rules that keep it reasoned, not chaotic**
- **Cause first.** An event fires only when its trigger is true in the galaxy right now; personality only chooses among eligible events.
- **Escalation, not jumps.** Relations change by steps: dispute → embargo → reprisal → war, and back down through ceasefire → pact → alliance. No faction goes from Friendly to war in one event, except a telegraphed betrayal. Big turns usually come with a new leader.
- **Memory.** Leaders remember the ledger: grudges fade slowly (more slowly for a Vengeful leader), favours too.
- **Pace.** Each leader acts at most once every few minutes, and each pair of factions has its own cooldown.
- **Announced with a reason.** Every event goes to the feed in plain words: who, against whom, and why ("The Marshal declares war on the Accord after the siege of Tessellate Reach").
- **Checked by simulation.** Leaders drive whether the war happens at all, so their weights and cooldowns are tuned with war checks: the galaxy must still go to war, and the Brood must still win only about 20%.

#### Winning the galaxy
- **Two-thirds of the galaxy wins.** Any faction (the three powers, the Brood, or a declared contractor faction) that controls two-thirds of the systems (20 of 29) starts a 10-minute timer. Hold it to the end and it wins.
- **The others unite when the timer starts.** As in Driftgate 1, the rest of the factions call a truce and turn on whoever has started the two-thirds timer; the truce breaks if the timer stops.
- **No other time limit.** There is no deadline and no tie-break count: a galaxy runs until someone wins. (Driftgate 1's 7 systems for 20 minutes and its 2-hour deadline go.)

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
- **No deadline.** The galaxy runs until a faction holds two-thirds for 10 minutes.
- **The war's clock slows to match.** Capitals from minute 45 and Overgrowth from minute 20 need new values. Working target for tuning: a typical galaxy is won in about 8–12 hours of play.

### Assets: models and art
**What exists (from Driftgate 1's model pack):** 17 ship models shared by every faction (the fighters are 5 Quaternius "Lowpoly Spaceships"; miners, haulers and the constructor are Kenney Space Kit craft with parts added; carrier and escort are assembled from Kenney parts in `tools/capitals.py`), 11 Brood models generated in code (`tools/brood.py`), and the structures: station, depot, asteroid base, yard, forge, relay and six works modules. All CC0.

| Need | Covered? |
|---|---|
| Unique hulls: about 13 classes × 3 factions, plus scouts, Unbound designs and faction capitals (about 45–50) | **No.** The main gap |
| Lair, Depot, Station (standard and asteroid look) | Yes |
| Station external buildings | Mostly (yard, forge, works modules); a market wing and a defence platform may need making |
| Brood, leaders, ace escorts | Yes (leaders fly ordinary hulls) |
| Mining-laser ring, comets, anomalies, beacon devices | Effects drawn in code |
| New screens | HTML and CSS, no assets |

- **Hulls are generated in code, one design language per faction**, the way the Brood is: Halcyon long, swept and bird-like with glass canopies; Varkesh blocky armoured slabs with exposed guns; Ostrova slender spires with a reactor halo, sensor masts and crystal. Each class is a set of parameters in its faction's language. Previews (the method approved, and all nine fighter designs approved, 2 Nov 2026): `tools/previews/beyond_light_fighters.png` (Swift, Fang, Mote from four angles) and `beyond_fighters_by_faction.png` (Light, Medium and Heavy fighters: Halcyon Swift, Kite, Osprey; Varkesh Fang, Talon (a pincer), Halberd (a brawler: an armoured core with a chisel prow and four gun-and-drive pods on an X of slab arms); Ostrova Mote (one halo), Wisp (a crescent joined to the spire by one pair of wings), Vigil (a tuning fork: a broad crystal-veined body, twin forward prongs holding a focus crystal, and two halos crossed in an X round the hull; close-up in `beyond_vigil.png`)). Rule from review: within a faction, every size has its own silhouette, not a bigger copy of the light one, from `tools/previews/beyond_hulls.py` and `render_beyond.py`.
- **Miners and haulers: all 18 approved (2 Nov 2026) after several rounds of review.** set further apart from the fighters without leaving the faction look: about 12% more girth, blunter noses, smaller Halcyon tail fins, no gun barrels on the Varkesh haulers, and industrial details (exhaust stacks on Varkesh, hull ribs on Halcyon, floodlights at the front of every ship). `beyond_miners_by_faction.png` and `beyond_haulers_by_faction.png`, from `tools/previews/beyond_work.py`. The first pass looked like fighters; the second bolted kit parts onto Driftgate 1's work ships. The third pass is wholly new craft built in code, taking **proportion and purpose from Driftgate 1's work ships** (stubby, wide industrial bodies; miners with forward drill arms, mining lenses, ore hoppers and charge launchers; haulers with big holds and containers) and **shape language from each faction's approved fighters**. Halcyon (lens hulls, glass, twin tails, the Osprey's booms): Wren (a chubby lens pod, bubble canopy, two drill arms hugging the nose), Plover (twin hopper booms with drills either side of a cockpit pod, no spoiler), Heron (a broad flattened hull with two stacked hoppers, drills and four drives, no nose laser); Tern (a short cockpit hull with its cargo hold joined on behind, forked tail), Albatross (a thick flying-wing whose wings are cargo bays), Pelican (a huge cargo pouch hull between two big engine pylons, no spoiler). Varkesh (hex slabs, chisel prows, pincer sponsons, square drives): Pick (a stubby hull with two short drill sponsons), Gouge (a broad hull with three mining lasers across the prow, every box angled: chamfered ore bins, mount and drives), Sledge (the Heron's layout in Varkesh form: a broad, bulky hex hull, two stacked hex hoppers, four mining lasers, drone bays, eight square drives); Runner (an armoured courier wedge: a chisel prow widening into a boxy cargo body, cargo doors on top, side skirts), Bulwark (two armoured holds as sponsons, two smoothed cargo pods on the spine), Rampart (a six-shooter: six ribbed armoured cargo pylons in a cylinder round a central axle, a nose tapering down from the cylinder to a cockpit canopy, a four-engine block astern, in Varkesh orange and light plating). Ostrova (spires, halos, crescents, prongs, crystal): Glim (a spire cockpit inside a halo, a crystal cargo hold set in the halo either side, prongs holding a lens), Lumen (a central spire cockpit forward with mining lenses at its nose; four long crystal holds set in two rings crossed in an X toward the stern, each stretched from the front of the rings to the back), Delve (a great drill spire with a lens ring at its prow; four crystal ore holds held by two halos, one at their fronts and one at their backs); Drift (a slim spire with two long crystal cargo containers, one either side and almost the ship's length, held by a front and a back ring), Cairn (a pointed spire, two rings, and three crystal cargo containers set in the rings; nothing else), Monolith (a solid spire fuselage with crystal seams and a bridge, four large crystal holds set in two halos round it, three spire drives astern).
- **Scouts and bombers: all 12 approved (2 Nov 2026).** `beyond_scouts_bombers_by_faction.png`, from `tools/previews/beyond_recon.py`. Combat and recon craft, so they stay close to the fighters' proportions, with a signature per class: scouts carry sensor masts, dishes and limpet racks (advanced scouts a beacon device too); bombers carry visible torpedoes; heavy bombers have two seats in tandem and a rear turret. Halcyon: Lark (a needle with a long sensor boom), Skylark (a big radome on twin pylons), Condor (a great swept wing with four slung torpedoes), Harrier (tandem canopies, a large forward-swept wing with a torpedo pod under each side, a rear ball turret). Varkesh: streamlined but bulky smoothed-hex hulls: Jackal (a slim, sleek, flat wedge with its sensor faired into the nose, a raked mast), Wolfhound (a slim, sleek hull with sensor blisters faired into its flanks, a big dorsal radar dish), Maul (compact, the torpedo magazine faired into its belly), Warhound (compact, two seats, a turret faired into the aft spine, tail fins, torpedoes along the flanks). Ostrova: Seer (a spire behind a sensor halo with a crystal eye, one pair of swept wings), Oracle (a spire with a great flat radome, set like the Skylark's on pylons, between two rings crossed in an X), Obelisk (the Sentinel's single-seat cousin: a spire with crystal fins, four torpedo lances on a halo, two tail fins at 45 degrees either side), Sentinel (tandem seats, a gun pod on the aft fuselage, torpedo lances under crystal fins, two tail fins at 45 degrees either side).
- **Capital ships, third pass (for review):** `beyond_capitals_by_faction.png` (at one scale) and `beyond_capitals_closeup.png` (four views each), from `tools/previews/beyond_capitals.py`. Rules from the first-pass review: capitals are not resized fighters, so there are no glass canopies and no fighter fins; each has a raised **bridge** superstructure with a lit window band, in its faction's style (Halcyon a lens pod on a pedestal with a dish, Varkesh stepped smoothed-hex tiers with a mast, Ostrova a faceted spire tower with a crystal window band). Each keeps Driftgate 1's working parts: escorts carry forward torpedo tubes, point-defence turrets (three a side), a bridge, a ventral assault bay, a shield generator and drives; carriers carry a flight deck with four landing spots, launch mouths at the bow, point-defence turrets, a bridge, a shield generator and drives. Class names are placeholders. Halcyon: Shrike (redesigned: a long layered lens hull with a dorsal superstructure spine, four torpedo tubes, faired turret sponsons, emitter nodes on pylons, a three-drive engine block), Sovereign (tail fin and stabiliser gone; the broad lens deck carrier with four engine booms (an outer pair at the flanks and an inner pair under the hull), a five-drive engine block between them, and its bridge beside the deck). Varkesh: Vanguard (cleaned up: a smooth armoured hull with armour bands, four torpedo tubes in the chisel prow, long turret pylons standing off the hull on two beams each, fore and aft, four drives), Bastille (smoothed: a slab fortress with a railed deck, turret pylons standing off the hull on two beams each, armour bands and eight drives). Ostrova: Lantern (redesigned: a long faceted three-section hull with two turret halos round it, crystal cores between them and four torpedo tubes in the prow, no prow ring), Cathedral (smoothed: an octagonal crystal-veined hull, the deck along its back, and two horizontal rings round the hull fore and aft carrying turrets and crystal holds). Third-pass changes: the escorts' shield generators moved under the hull, so nothing bubbles up from their tops; the Lantern lost its prow ring; the Cathedral's rings lie flat; the Ostrova spire bridges are lower; the Sovereign has five drives in its engine block (nine with its four booms). (The preview renderer now splits big triangles, so flight decks show cleanly in the angled views; the game draws with a depth buffer and never had that problem.)
- **Destroyers, first pass (for review):** on the same two sheets, between each faction's escort and carrier, from `tools/previews/beyond_capitals.py`. Each is built around its main gun, in its faction's language, with point-defence turrets and a bridge. Names are placeholders. Halcyon **Peregrine**: a lens hull that splits into two prongs round a spinal rail cannon, glowing accelerator rings between the prongs, a capacitor bank along its back, faired drive nacelles, a bridge pod aft. Varkesh **Ironclad**: an armoured hull on a flared armour belt with two giant single-barrelled main guns on the centreline (the second raised on a barbette to fire over the first), the stepped bridge behind them, turrets along the belt. Ostrova **Prism**: a faceted hull carrying three long spars (two above, one below) that converge on a great crystal lens in the prow, the spinal lance, fed by an energy conduit, turrets riding the spars, a low spire bridge, a small halo round the stern.
- **Player bases: approved (2 Nov 2026).** `beyond_player_bases.png`, from `tools/previews/beyond_stations.py` (sheet: `stations_sheet.py`). In the neutral company style, each picture scaled to fit. **Lair 1** a large asteroid with one framed hangar cut into it, a hatch and a whip antenna, little else showing (it is hidden); **Lair 2** adds a second berth, a forge vent glowing in a crack, a stash of containers clamped to the rock, a dish and a radiator. **Depot 1** a hub drum with a dome, a docking arm with a lit collar, containers and a tank (storage), a beacon mast; **Depot 2** adds a production module with radiators and a hangar; **Depot 3** adds defence turrets on the dome rim, armour plates and a life-support ring. **Station core**, standard: a spine, a central hub, a habitat ring on four trusses, a docking crown with four collars, tanks, radiators, and five **hardpoints** (lit pads on truss arms) where the buildings go; asteroid: the same crown and spine coming out of a large rock with three hangars cut into it. **Buildings** (each attaches to a hardpoint): shipyard (an open gantry with portal frames, two cranes and a keel taking shape), external storage (a rack of containers and three tanks), defence platform (a hex gun deck: two heavy turrets, four point-defence turrets, a ventral turret, a mast), hangar (a half-drum hall with a lit mouth and an apron), forge (a furnace drum glowing at its mouth, stacks, radiator wings, ore hoppers), market wing (a lit concourse with three trader docking collars and a sign). **Level 5** examples show both looks with five buildings fitted.
- **Faction stations, faction depots and the freeport, second pass (for review):** `beyond_faction_stations.png`, from `tools/previews/beyond_faction_stations.py` (sheet: `faction_stations_sheet.py`). **Halcyon** (approved as drawn) station: a great lens disc with a glass crown, a spire with a dish and emitter, three swept arms (a pinwheel from above) ending in emitter nodes, hangars in the rim, point-defence turrets on the upper surface, a stem to a lower lens pod; depot: a small lens with two swept arms, one hangar, a dish. **Varkesh** (redrawn: smoother, sharper, warlike, not boxy) station: a war fortress, a smooth twelve-faceted double spike with a knife-edged waist, six armoured blades rising from the waist like a crown of spikes with heavy turrets riding them, three blades below, six more heavy turrets on the upper slope, hangar slots and pincer clamps in the waist, a lit command band near the top; depot: the same in small, with three blades, one hangar, one clamp and a heavy turret on top. **Ostrova** (redrawn as several crystal spires) station: a tall faceted main spire with lit crystal bands on a faceted plinth, six great crystal spires of different heights leaning out round it, smaller crystals between, a crystal root, the great halo with turrets and crystal holds circling the cluster, three docking spars; depot: a squat faceted pylon ringed by three tall crystal holds standing like pillars, a crown ring over their tips, a crystal root, one docking spar. **Freeport** (redrawn to look nothing like a player base): a trade harbour, a great lit bazaar globe on a broad docking plaza with twelve berths round its rim, four long cargo piers stacked with containers, **two corporate spires** (one per corporation, each with its sign), the freeport light on a mast above, a keel of tanks below, in the Compact's sand colour. Freeports have no depots.
- **Kits:** Driftgate 1's kits are now in the repo (`tools/kits/`: Kenney Space Kit, Quaternius Lowpoly Spaceships), so the model pack can be rebuilt the normal way with `tools/build_models.py`.
- **Asset packs may still be needed** for variety (more CC0 ship kits to mix with the generated hulls). The build shell can't download from the asset sites, so any further pack has to be attached to the session or added to `tools/kits/`. New generated models can be added to the existing pack without the kits.
- **Every design is previewed and approved** before it goes in the game, as Driftgate 1's signature hulls were.

### Rules Beyond keeps
- **The ledger is exact.** Components, parts, payload, bases and AI ships are all made of real goods from real rock.
- **The host simulates;** guests send inputs.
- **The faction status ledger** logs every interaction between factions; relations come only from it.
- **The war is checked by simulation.** New target for AI-only galaxies: the Brood about 20%, the three factions sharing the rest evenly (about 27% each). Until the Brood change is built, Driftgate 1's target in CLAUDE.md still applies.
- **Build specs** for each stage are written below the vision and approved before code changes; stages 1 and 2 are the first.

### Decided in review (2 Nov 2026)
Hull upgrades are stats only · a blast breaks a rock's ring · AI upkeep is credits plus goods · your own brand from Depot level · Brood about 20% · Rating only goes up · a pilot at Partner standing may declare allegiance (to a player's faction at any time, no standing needed, once its founder accepts), shown on an Allegiance screen with standings between factions; swearing hands the faction all your assets, renouncing costs your standing with it, and re-swearing to an AI faction needs Partner again, and fly for that faction instead of building their own (11a) · factions become allied by trading and not fighting, tracked in a background faction status ledger (11b); all factions start Neutral; allies still hire contractors against each other; leaders with personalities drive reasoned faction events, and successors' traits come from their faction's history, so relations can swing from annihilation to friendship over a storyline; leaders fly in the galaxy with an ace escort, in ships their traits lean toward, and can be killed, which triggers a Vengeful succession; they make escort, hunt and sighting work, show on radar by name and open their best jobs where they dock (11c) · Legend reworked: levels unlock perks you pick from each galaxy with a start-point budget, level 10's Station stays, and Conqueror's spoils go in full to the winning faction and half to its allies (10a) · a choice of three starting freeports · faction careers become job bonuses and the signature hulls survive · scouting returns as intel, with scout hulls (Rating 2 and 4, not a starter) the only hulls for beacon devices and limpets · a beacon flip earns a fee and standing · your brand's trait is a net-zero point system · Unbound designs are pirates' only · the nine fighter designs (Swift, Kite, Osprey; Fang, Talon, Halberd; Mote, Wisp, Vigil) are approved · the 18 miner and hauler designs are approved · the 12 scout and bomber designs are approved · Station levels come from external buildings · freeport yards roll a random set of faction designs; house-brand hulls only at their faction's station · AI wages go to the Compact · two-thirds of the galaxy for 10 minutes wins, with no deadline, and the others unite once the timer starts · you choose one external building per station level · asteroid landing needs an installed landing kit, not offered automatically · flares stay on energy, drones restock at dock · only factions (and the Unbound and Brood) design hulls; freeports build faction designs · Lair 2 levels, Depot 3, Station 5 · makers' names kept for now · declaring needs only a Station · losing your last Station drops you back to a company · asteroid or standard station look.

### Open questions
1. **Lair, Depot, Station costs.** All numbers are guesses to tune.
2. **Allies and the win.** Do allies' systems count together toward two-thirds? And when a faction starts the timer, do its allies join the truce against it, or stand with it?

### Proposed build order (once the design is agreed)
1. **Cut the faction tie:** start at a chosen freeport with three equipped starters; standing with every power; docking and hostility from standing; pay from the issuer; faction job bonuses.
2. **Faction relations and leaders:** the faction status ledger, all factions starting Neutral, leaders with traits, the event table and successions, the chronicle; war checks that galaxies still go to war. (It comes this early because the Neutral start only works once leaders can start wars.)
3. **Weapon slots and weapons** (and the landing kit as a utility part): slot counts per hull; machine gun with ammunition, laser on reactor energy, missile and torpedo payload; mining laser with rings and charge launchers in mining hulls' weapon slots.
4. **Making things:** ore → components → parts → upgraded parts; grades replace Mk.
5. **Faction jobs screen,** with intel jobs: beacon devices, capital pings, limpets, and discoveries out beyond the gates.
6. **Unique hull designs, first wave:** each faction's fighters, with their own models and stats, duel-balanced; freeport yards build them.
7. **Makers:** the corporations, their works and stock; product lines replace variants; AI fleets fitted from their makers.
8. **Progression:** Contractor Rating gates hulls and grades; hull upgrades; drop Unbound mode.
9. **Lairs and the Holdings screen.**
10. **Depots:** markets, hiring and building AI with upkeep; the Economy and Job creation screens.
11. **Stations and station upgrades;** capital ships built at your stations.
12. **Strategic map** with sector zoom and orders.
13. **Declaring a faction;** player factions in the ledger and leaders' proposals to founders; slower war pacing; a stronger Brood (about 20%); war checks for the new balance.
14. **Legend rework and Conqueror's spoils, multiplayer rivalries, training rewrite.**

---

## Build spec: stages 1 and 2 (draft for approval, 2 Nov 2026; nothing built yet)
Concrete plan for the first two build stages, mapped against the Driftgate 1 code. File references are to `src/js/`.

### Decisions (2 Nov 2026)
1. **Halcyon's hauling bonus:** Halcyon pays +20% on hauling jobs **Halcyon issues**; the Compact pays nothing extra.
2. **A starter's design:** a freeport starter is built in one of the designs that freeport's yard rolled (stage 6); until the new designs exist, it uses the shared model with the faction trait.
3. **The map:** **until you declare your own faction, you see every faction's intel as if it were yours** (every power's beacons, scouts, traders and price scans).
4. **Saves:** there are no old Beyond saves and none are kept in the repository; Beyond's browser saves use their own `dgbeyond.*` keys, so Driftgate 1's are never read. No old-save compatibility is needed: the save version is bumped and anything older is refused.

### The key technical choice
Today one field, the pilot's `faction`, does two jobs: it picks the **hull design** (model, stats, names, cockpit colours) and it sets **allegiance** (who you fight, where you dock, who pays you). About 160 lines across 16 files read it. Rather than delete it, Beyond splits it:
- `P.faction` stays, meaning **design faction** only.
- New `P.sworn` (null for a contractor) means **allegiance**. Setting `P.sworn` to a faction gives back Driftgate 1's behaviour exactly, which is also the **allegiance stub** and keeps training and the old tests working while everything else moves over.

### Stage 1: cut the faction tie
**New state** (saved with `S.player` and `S.pilots[pid]`, so single-player and multiplayer saves carry it already): `P.stand` (standing with halcyon, varkesh, ostrova and the Compact), `P.home` (starting freeport), `P.sworn`, `P.job` (the job you're on: issuer and kind).

**Steps, each tested before the next:**
1. **Add the fields with no change in play.** `standOf`, `standAdd`, `standBand`; bump the save version (decision 4); every pilot starts sworn to their chosen faction for now. Quick tests must still pass.
2. **Move allegiance reads to `P.sworn`,** one file at a time: `friendSide` (11), `sideNorm` (04), `isFacSide` (02), coverage and map intel (an unsworn pilot sees every power's intel, decision 3), strategy feeds (`coalTick`, `galaxyWon`, `planOffensive`), command wings (09). Tests still pass, since `sworn` is still set.
3. **Hostility and docking from standing.** `hostile()` (02): for an unsworn pilot, Brood and Unbound are always hostile, a power is hostile below −50, otherwise not. It runs every frame inside AI targeting, so the lookup must be a constant-time read with no allocation. `canDock()` (11): standing −10 or better with the station's owner (freeports check the Compact).
4. **Pay from the issuer.** A new `bountyPayer`: the issuer of your running combat job if it's hostile to the victim; otherwise the power at war with the victim you stand best with; otherwise nobody. Used by `payKill` (04) and its ace wrapper, `aceKilled` (16), containment pay (10). `weKill` adds war effort only to your job's issuer. Spot pay (01) changes too. Checked with `devLedger`, since credits must stay zero-sum.
5. **Jobs by issuer.** `jobsList` (13) shows the docked station's owner's jobs (standing −10 or better); at a freeport, the Compact's jobs plus each power's posted jobs, filtered by standing. Signing on records `P.job`. Faction job bonuses (16f) are keyed by the issuer: Halcyon on the hauling jobs it issues (decision 1), Varkesh on its mining and Aurorite jobs, Ostrova on its intel and escort pay. Signature hull conversions need Partner standing with the station's owner.
6. **Standing moves.** Rises on job completion (scaled by risk); falls when you damage a power's ships, convoys or stations (hooked where damage is credited to the player, 10), and a quarter as much for war work against it; drifts toward 0 each strategic tick.
7. **The new start.** The start screen offers the three freeports (Mirrorwater, Coldwater Drift, Ember Wake) instead of factions, and three roles (no Scouting). `START_HULLS` drops the scout. `newGame` starts you docked at your freeport, unsworn. Respawn after death goes to `P.home` (`playerDeath`, and `rpDeath` for guests). Training starts a pilot sworn to Halcyon until it's rewritten. The playable Unbound card stays until stage 8 drops it.
8. **Multiplayer.** `newPilot` and the host's join check take a freeport, not a faction. Guests' ships need their own side (each pilot's standing is different), so AI targeting asks "is this pilot hostile to me" per pilot rather than per faction. The five multiplayer tests are rerun.

**Tests:** about 12 browser tests assume a faction start (jobs, hulls, ships, limpets, contacts, docks, soak, haul rates, the five multiplayer tests). Each gets a one-line setup that swears the test pilot to Halcyon where it tests faction behaviour; new tests cover standing bands, docking by standing, bounty payers and the freeport start. The fast simulator's `PFAC` becomes `PPORT` (mw, cw or ew).

**War check:** stage 1 doesn't change how the powers fight each other, so the AI-only war should be unchanged; run the war check once to prove it (Driftgate 1's target until stage 2).

### Stage 2: faction relations and leaders
**New state** (on `S`, so saved and sent to guests already): `S.rel` (relation per pair), `S.relLog` (recent entries, capped), `S.leaders` (per power: name, traits, ship, escort, grudges, cooldowns), `S.facEv` (cooldowns per pair), `S.chron` (the chronicle). New file `src/js/16g_leaders.js` after `16f_factions.js`.

**Steps:**
1. **The ledger, read-only.** `relAdd`, `relBand`, the log, and an Allegiance tab at docks showing standings, relations between factions and the chronicle. No effect on play.
2. **Feed it, still at permanent war.** Hooks: trade (`traderArrive`, `fpImport`), ships destroyed (the death path before `payKill`), captures and razes (`capture`, `captureDepot`, `razeStation`), sieges (`resolveSiege`), raids (`raidFight`), beacon flips (`beaconFlip`). Run the fast simulator and record how relations move, to size the numbers.
3. **Leaders in shadow mode.** Leaders with traits, the event table, triggers, cooldowns and successions, logged as what they *would* do ("would declare war") without acting.
4. **Switch on.** All factions start Neutral. `hostile()` between powers follows the ledger (Hostile and War fight); new `warWith()` for sieges and campaigns; `planOffensive` also stops targeting outposts held by a power it isn't at war with; `campTargets`, `resolveAbstract`, `resolveSiege` use `warWith`. The Containment Accord stays as the "containment front" and still overrides the ledger. Traders may use Friendly factions' markets, which is how trade builds alliances.
5. **Leaders as ships.** Built on Driftgate 1's ace system (an ace with a wing of escorts, a kill reported by `aceKilled`), plus an off-screen mover so a leader keeps travelling when nobody is watching; a killed leader triggers a succession shaped by history. Leaders never go into the aces record that carries between galaxies.
6. **Leader jobs** (escort a leader, hunt one, sell a sighting) and proxy work can wait for the Faction jobs screen (stage 5).

**The main risk.** If everyone starts Neutral, nobody shoots, nothing goes negative, and no war ever starts. The first negatives must come from AI scouts flipping beacons, building in contested systems, and leader events (border dispute, then embargo, then war). So leaders are built and tuned (steps 3 and 5) before and alongside the switch (step 4).

**War check** (four sides, 480 games each): nearly every galaxy has its first war by about 30 minutes; the Brood wins about 20%; the three powers share the rest evenly; and games that end on the deadline don't rise (the 2-hour deadline stays until the pacing work in stage 13, so a late first war would push wins onto it). The simulator reports when the first war starts, minutes each pair spends at war, alliances, betrayals, leader deaths and successions. New tests: relations (ledger arithmetic and bands) and leaders (an event fires on its trigger, the chronicle records it, a killed leader is succeeded).
