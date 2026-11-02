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
| Utility | Cargo module, scanner, drone bay; on scout hulls only, beacon device or limpet rack |

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
- **A station counts for the system**: owning it gives you the system, as Driftgate 1's `sectorOwner` does for faction stations. This is the road to winning the galaxy (section 11).
- **Levels 1–5 come from external buildings.** Each new level lets you add **one building of your choice** around the station: shipyard, external storage, defence platform, hangar, forge, market wing and so on. Five levels, five buildings, so no two stations are the same. You see your station grow, and an attacker can target its buildings one at a time.
- **The shipyard** is one of these buildings: it builds hulls for you and your AI.
- **Capital ships** are built at the yard (proposal: escorts once the station is level 3, carriers at level 5, in both cases with a yard among its buildings).

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

- **Hulls are generated in code, one design language per faction**, the way the Brood is: Halcyon long, swept and bird-like with glass canopies; Varkesh blocky armoured slabs with exposed guns; Ostrova slender spires with a reactor halo, sensor masts and crystal. Each class is a set of parameters in its faction's language. Previews (approved as the method, 2 Nov 2026): `tools/previews/beyond_light_fighters.png` (Swift, Fang, Mote from four angles) and `beyond_fighters_by_faction.png` (Light, Medium and Heavy fighters: Halcyon Swift, Kite, Osprey; Varkesh Fang, Talon (a pincer), Halberd (a brawler: an armoured core with a chisel prow and four gun-and-drive pods on an X of slab arms); Ostrova Mote (one halo), Wisp (a crescent joined to the spire by one pair of wings), Vigil (a tuning fork: a broad crystal-veined body, twin forward prongs holding a focus crystal, and two halos crossed in an X round the hull; close-up in `beyond_vigil.png`)). Rule from review: within a faction, every size has its own silhouette, not a bigger copy of the light one, from `tools/previews/beyond_hulls.py` and `render_beyond.py`.
- **Kits:** Driftgate 1's kits are now in the repo (`tools/kits/`: Kenney Space Kit, Quaternius Lowpoly Spaceships), so the model pack can be rebuilt the normal way with `tools/build_models.py`.
- **Asset packs may still be needed** for variety (more CC0 ship kits to mix with the generated hulls). The build shell can't download from the asset sites, so any further pack has to be attached to the session or added to `tools/kits/`. New generated models can be added to the existing pack without the kits.
- **Every design is previewed and approved** before it goes in the game, as Driftgate 1's signature hulls were.

### Rules Beyond keeps
- **The ledger is exact.** Components, parts, payload, bases and AI ships are all made of real goods from real rock.
- **The host simulates;** guests send inputs.
- **The faction status ledger** logs every interaction between factions; relations come only from it.
- **The war is checked by simulation.** New target for AI-only galaxies: the Brood about 20%, the three factions sharing the rest evenly (about 27% each). Until the Brood change is built, Driftgate 1's target in CLAUDE.md still applies.

### Decided in review (2 Nov 2026)
Hull upgrades are stats only · a blast breaks a rock's ring · AI upkeep is credits plus goods · your own brand from Depot level · Brood about 20% · Rating only goes up · a pilot at Partner standing may declare allegiance (to a player's faction at any time, no standing needed, once its founder accepts), shown on an Allegiance screen with standings between factions; swearing hands the faction all your assets, renouncing costs your standing with it, and re-swearing to an AI faction needs Partner again, and fly for that faction instead of building their own (11a) · factions become allied by trading and not fighting, tracked in a background faction status ledger (11b); all factions start Neutral; allies still hire contractors against each other; leaders with personalities drive reasoned faction events, and successors' traits come from their faction's history, so relations can swing from annihilation to friendship over a storyline; leaders fly in the galaxy with an ace escort, in ships their traits lean toward, and can be killed, which triggers a Vengeful succession; they make escort, hunt and sighting work, show on radar by name and open their best jobs where they dock (11c) · Legend reworked: levels unlock perks you pick from each galaxy with a start-point budget, level 10's Station stays, and Conqueror's spoils go in full to the winning faction and half to its allies (10a) · a choice of three starting freeports · faction careers become job bonuses and the signature hulls survive · scouting returns as intel, with scout hulls (Rating 2 and 4, not a starter) the only hulls for beacon devices and limpets · a beacon flip earns a fee and standing · your brand's trait is a net-zero point system · Unbound designs are pirates' only · Station levels come from external buildings · freeport yards roll a random set of faction designs; house-brand hulls only at their faction's station · AI wages go to the Compact · two-thirds of the galaxy for 10 minutes wins, with no deadline, and the others unite once the timer starts · you choose one external building per station level · flares stay on energy, drones restock at dock · only factions (and the Unbound and Brood) design hulls; freeports build faction designs · Lair 2 levels, Depot 3, Station 5 · makers' names kept for now · declaring needs only a Station · losing your last Station drops you back to a company · asteroid or standard station look.

### Open questions
1. **Lair, Depot, Station costs.** All numbers are guesses to tune.
2. **Allies and the win.** Do allies' systems count together toward two-thirds? And when a faction starts the timer, do its allies join the truce against it, or stand with it?

### Proposed build order (once the design is agreed)
1. **Cut the faction tie:** start at a chosen freeport with three equipped starters; standing with every power; docking and hostility from standing; pay from the issuer; faction job bonuses.
2. **Faction relations and leaders:** the faction status ledger, all factions starting Neutral, leaders with traits, the event table and successions, the chronicle; war checks that galaxies still go to war. (It comes this early because the Neutral start only works once leaders can start wars.)
3. **Weapon slots and weapons:** slot counts per hull; machine gun with ammunition, laser on reactor energy, missile and torpedo payload; mining laser with rings and charge launchers in mining hulls' weapon slots.
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
