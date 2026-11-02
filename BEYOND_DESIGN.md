# Driftgate Beyond: design

A new game in the Driftgate universe. This file holds its design as it is decided; DESIGN_NOTES.md is Driftgate 1's history up to the fork.

## Fork (Nov 2026)
- Forked from Driftgate 1 v255 with its full code, tools and tests.
- Own identity: browser storage keys `dgbeyond.*` (save `dgbeyond.save.v1`, legend, keys, audio, lore, aces, tips, multiplayer ids), multiplayer host ids `dgbeyond1-<code>-host`, relay topics `dgbeyond1/…`, tab channel `dgbeyond`, title "Driftgate Beyond", invite links to mbyrtus-maker.github.io/DriftgateBeyond/.

---

## Vision (draft 2, 2 Nov 2026: for review, nothing here is built)

### In one paragraph
The war goes on, but you no longer fight in it as a soldier. You are an independent contractor who starts at a freeport with one light ship and a few credits, and you take work from whoever will pay. Corporations under the factions and at the freeports (two at each) make what the market sells, and you can make it yourself: ore into components, components into parts, parts into better parts. Your money and materials go up a ladder: ships, then upgrades to those hulls, then a Lair, then a Depot, then a full Station, each with its own levels, and finally capital ships built at your stations. From the Depot on you hire AI pilots and ships, pay their upkeep, earn from your own market, post your own jobs and command them from a strategic map. In the end your company declares itself a faction and joins the war as a fourth contender.

### What carries over, what changes, what goes

| Keep from Driftgate 1 | Change | Drop |
|---|---|---|
| Flight, drift by mass, gates, docking | Pilot welded to one faction → **standing** with every power, work for anyone | **Unbound pirate mode** (the start card, crew galaxies, Scrapheart Haven works) |
| Combat feel, shields, sub-targets, capitals and bridges | Pay from your faction's treasury → paid by **whoever issued the job** | **Legend levels** as they are (replaced, see Progression) |
| Blast charges, salvage, hauling, convoys | Blast rig only → **mining lasers back** alongside charges, both in a mining hull's weapon slots | Mk I–III as one shared ladder (replaced by grades) |
| The three factions, their AI war, campaigns, depots, sieges | One Weapons system for gun and laser together → **separate parts in weapon slots**; slot count varies by ship | Scout hulls for contractors |
| **The Brood,** probably with more presence and a higher win rate | Free kinetic fire → **machine guns use ammunition**; lasers draw on the reactor | |
| **AI Unbound raiders** in the galaxy | Missiles that reload by themselves → **payload** you carry, which hits harder | |
| AI scouts: beacons, limpets, recon, Seeder spotting | Scouting as a pilot career → **mostly an AI function** | |
| Freeports and the Compact, Seals and Matrices | Unbranded goods → **corporate parts** with a maker and a trait | |
| The closed economy and the exact ledger | A short crafting list → **ore → components → parts → upgraded parts** | |
| D1's Unbound Lair, depots, depot modules, stations | Faction-only bases → **your own Lair → Depot → Station**, each with levels | |
| Capital ships and their bridges | Commissioned at a faction yard → **built at your own stations** | |
| Multiplayer: host simulates, guests send inputs | Three contenders → three plus **contractor factions** | |
| Signature hulls (Gannet, Bombard, Vesper) | Become **house-brand hulls**, built with standing | |
| | One shared model per class with a ±12% trait → **unique hull designs** in look and stats | |
| Galaxy map with its sector panel | → a **strategic map** you zoom into a sector to command your AI | |
| Training | Rewritten later for the contractor's start | |

---

### 1. Contractors, not soldiers
- **You start at a freeport, not a faction.** You're neutral with every power, at Rating 1, with a few credits.
- **Three starters, fully equipped.** Choose one; each comes with drive, reactor, shield and armour fitted, plus its role kit:
  - **Light Fighter:** a machine gun with ammunition, a laser and a missile launcher with a first magazine.
  - **Light Miner:** a mining laser, a charge launcher with charges, and drones.
  - **Light Hauler:** a machine gun and a cargo module.
- **There is no scout start.** The powers fly their own scouts to flip beacons, plant limpets, run recon and spot Seeders. Contractors use what those scouts find (beacon intel, raid boards, price scans), and escort or shoot down scouts as jobs.
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
- **Corporate parts.** The makers (section 4) sell parts too. A maker's part carries its maker's trait, a strength and a weakness, like Driftgate 1's variants. A part you build yourself is standard, with no trait. You can upgrade either; an upgraded corporate part keeps its maker and trait.

### 4. Makers: corporate items
Corporations make much of what's on the market. Each faction hosts two named makers and each freeport two more, each with a trait that follows its home's character. Names are placeholders.

| Power | Maker (placeholder) | Makes | Trait |
|---|---|---|---|
| Halcyon Accord | Teal & Corvane Yards | Halcyon hull designs, cargo modules | Light, fast frames |
| Halcyon Accord | Brightline Emitters | Shields, lasers | Shields +, hull − |
| Varkesh Dominion | Hold Foundry | Varkesh hull designs, armour, charge launchers | Heavy, tough frames |
| Varkesh Dominion | Marchgun Ordnance | Machine guns, missile launchers, ammunition | Damage +, energy − |
| Ostrova Collective | Spirewright | Ostrova hull designs, scanners, mining lasers | Sensor-heavy frames |
| Ostrova Collective | Archive Dynamics | Reactors, drives | Energy +, shields − |
| Mirrorwater (freeport) | Mirrorwater Arms | Weapons of every kind | Sells to anyone, no standing gate |
| Mirrorwater (freeport) | Quicksilver Hullworks | Freeport fighter and bomber designs | Generalists, sold to anyone |
| Coldwater Drift (freeport) | Coldwater Refit | Refurbished parts from salvage | Cheap; grades 1–3 only, slightly worse |
| Coldwater Drift (freeport) | Coldwater Prospecting | Mining lasers, charge launchers, miner designs | Mining yield +, combat − |
| Ember Wake (freeport) | Ember Wake Drives | Drives, reactors, hauler designs | Long-burn and freight specialists |
| Ember Wake (freeport) | Wakefire Munitions | Ammunition, missiles, torpedoes, blast charges | Payload for anyone; the steady seller |
| Freeport Compact | (the Compact itself) | Compact Seals, Calibration Matrices | As in Driftgate 1 |

- **Real factories.** Each maker's works sits at its home station and turns components into parts at a set rate, for sale on that station's market.
- **The war uses the same stock.** A faction's AI fleets are fitted from its makers' output. A faction that's losing burns through that stock, so those parts get scarce and dear for contractors, and the freeport makers become the reliable source. Prices tell you where the war is.
- **Product lines replace variants.** Driftgate 1's variants become specific makers' products: Brightline makes the Bastion and Flicker shields, Marchgun makes Heavy and Rapid machine guns, and so on.

### 5. Unique hull designs
In Driftgate 1 every faction flies the same model for each hull class, with a name and a ±12% trait. In Beyond each power's design is **its own, in look and in stats**.

- **Every power builds every class its own way.** Each faction has a light fighter, and no two are the same. As a starting sketch:
  - **Halcyon Swift:** fast and light, strong shields, thin hull.
  - **Varkesh Fang:** slower and heavily armoured, an extra weapon slot, a hungry reactor.
  - **Ostrova Mote:** a deep reactor, the best sensors and lock range, weak shields.
- **Stats differ in more than one number:** hull, shield, energy, mass, top speed, turn, acceleration, hold, weapon slots, other slots and silhouette size. Two light fighters should fly differently and suit different parts.
- **Own models,** built from kit parts (`tools/build_models.py`) or hand-built in code like the Heavy Bomber and the Gannet, so you tell a Fang from a Swift at a glance.
- **Freeport makers have designs too** (Quicksilver's fighters, Coldwater Prospecting's miners, Ember Wake's haulers): sold to anyone, generalists without a faction's edge.
- **AI fleets fly their own power's designs,** so you learn to read a Varkesh wing by its shapes.
- **Balance rule:** within a class, no design wins more than about 60% of its mirror duels against another at the same grade (`tools/duel.py`). They differ in how they win, not whether.
- **Scale:** three factions × about 12 contractor classes is around 36 designs, plus freeport frames. Build in waves: fighters first, then miners and haulers, then bombers, then capitals; AI-only scouts last. A class keeps the shared model with the faction trait until its designs exist.

### 6. Ships: slots and weapons
A ship is a hull with slots. Each slot takes one part from any maker, or one you built.

| Slot | Takes |
|---|---|
| Hull | Sets mass, hold, slot counts and handling |
| Drive, Reactor, Shield, Armour | One part each |
| **Weapon slots** (number varies by ship) | One each: machine gun, laser, missile launcher, torpedo launcher; on mining hulls only, mining laser or charge launcher |
| Utility | Cargo module, scanner, drone bay |

**Weapons, each in its own slot, each limited differently:**
- **Machine gun (kinetic):** strong against hull; you must lead your shots. **Limited by ammunition:** rounds are payload, bought or built, carried in the ship.
- **Laser:** hits instantly, strong against shields. **Limited by reactor energy:** no ammunition, but it drains the reactor fast, so a better reactor means more laser time.
- **Missile launcher:** fires missiles from a magazine. **Limited by payload:** missiles are items, rearmed at a dock, never reloaded in flight. Because they run out, each hits harder (proposal: about twice a Driftgate 1 missile).
- **Torpedo launcher:** the same, on bomber hulls only; still the siege weapon.

**Mining, in the same slots:**
- **Mining laser (back from Driftgate 1, reworked):** slow, steady mining. Scan a rock and it shows its **ring**, a seam around the rock; hold the beam on the ring to cut ore steadily. Draws on the reactor like a combat laser. Quiet and safe, but slow.
- **Charge launcher:** Driftgate 1's blast charges. Scan for fault points, place charges and blow the rock apart for a big, fast yield with the risk of a bad blast. Charges are payload.
- **Only mining hulls can fit mining equipment.** Mining lasers and charge launchers go only in a mining hull's weapon slots. A miner can still carry a gun in a spare slot, at the cost of mining tools; no other hull can mine.

**Fire controls:** one key per weapon type fitted (replacing 1 and 2), C for launchers as now, the mining keys as now. Starting proposal for slot counts: Light Fighter 3, Medium 3–4, Heavy 4–5; miners 2–3; haulers 1–2; bombers 2 plus the torpedo launcher. These vary by power's design.

### 7. What you spend on: the ladder
Players have several things to spend money and materials on, in this order, each with its own levels:

| Step | What it is | Levels (proposal) |
|---|---|---|
| 1. Ships | Build hulls up the Rating ladder | Light → Medium → Heavy → specialist |
| 2. Hull upgrades | Upgrade the hull you fly | Levels 1–3: more hull, hold or energy; the top level adds a slot |
| 3. **Lair** | Your first base, hidden in a large asteroid | 1–3 |
| 4. **Depot** | Your first open base, with a market and a hangar | 1–3 |
| 5. **Station** | A full station that counts for the system | 1–3, plus station upgrades |
| 6. Capital ships | Built at your stations | Escorts, then carriers |

#### Lair (from Driftgate 1's Unbound Lair)
- **Building:** a Rigger kit (proposal: 1 Depot Frame + 20 plate) set into a large asteroid in any system with no station.
- **Hidden** until a scout of a hostile power comes within range (AI scouts find Lairs, as in Driftgate 1).
- **Level 1:** stash (200 t), repairs and rearming.
- **Level 2:** your own workshop, building components, parts, upgrades and payload with no fee.
- **Level 3:** a forge (lattice, core), a bigger stash, and a spare berth to keep a second ship.
- One Lair per system.

#### Depot
- **Building:** upgrade a Lair in place, or build fresh (proposal: 2 Depot Frames, as Driftgate 1's `DEPOT_COST`). Visible on every map, with a market.
- **From Depot level 1 you can hire and build AI ships and pilots** (section 8). Its hangar holds them.
- **Your market earns.** AI merchants and other pilots trade with your depot; you set what it buys and sells, and the margins are your income.
- **Levels 1–3** reuse Driftgate 1's depot modules: storage, production, defence, armour, hangar, life support.

#### Station
- **Building:** upgrade a Depot (proposal: Capital Keels, Depot Frames and Compact Seals).
- **A station counts for the system**: owning it gives you the system, as Driftgate 1's `sectorOwner` does for faction stations. This is the road to the 7-system win.
- **A shipyard:** builds hulls for you and your AI.
- **Levels 1–3, plus station upgrades** (defence, shields, armour, hangar, production, docks).
- **Capital ships** are built here: escorts from Station level 2, carriers from level 3.

### 8. Your AI: pilots, ships and upkeep
- **From the Depot on,** you hire AI pilots and build or buy them ships. They fly for you: mining, hauling between your bases, guarding, escorting your convoys, patrolling, raiding.
- **Upkeep:** every AI pilot and ship costs maintenance per hour while in service. Repairs, payload and lost ships come out of your stores.
- **Income:** your markets' sales, jobs you complete, and your AI's work (the ore your miners bring home, the goods your haulers sell).
- **Credits stay zero-sum.** Wages go to the Compact (it supplies the crews) and running costs consume goods into Driftgate 1's drift, as life support already does. Both open to change.
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
- **Rating 1–10, per galaxy,** rising with Rating points from completed jobs (weighted by risk), kills on a job, deliveries and stationworks built.
- **Hulls unlock by Rating, then cost credits and materials:**

| Rating | Hulls you may build |
|---|---|
| 1 | Starters: Light Fighter, Light Miner, Light Hauler |
| 2 | Medium Fighter, Medium Miner, Medium Hauler |
| 4 | Heavy Fighter, Bomber |
| 5 | Heavy Miner, Heavy Hauler |
| 6 | Heavy Bomber; house-brand hulls with Partner standing |
| Station level 2 | Escort |
| Station level 3 | Carrier |

- **Parts unlock by Rating and cost:** grade 1 at Rating 1, 2 at 2, 3 at 4, 4 at 6, 5 at 8. A maker's grade 4–5 parts also need Trusted or Partner standing with its power.
- **Across galaxies (replaces Legend).** Legend can't carry over as it is, because one pilot can now own a faction. Proposal: a light **Legacy** record per callsign (bases built, factions declared, galaxies won), giving titles and at most a small head start, never a base or a fleet.

### 11. Declaring a faction
- **When your holdings are big enough** (proposal: three stations, each holding its system, and a capital in service), you can declare.
- **Once declared,** you're a contender: you win by holding 7 systems for 20 minutes, the three powers treat you as a rival, and the truce-against-the-leader rule applies to you. Your standings with them drop to a war footing.
- **Your faction runs on Driftgate 1's strategic AI,** steered by your orders on the strategic map and the jobs you post.

### 12. The war around you
- **The three factions fight on, AI-driven:** campaigns, depots, forges, sieges, capitals, the truce against the leader.
- **The Brood stays, probably stronger.** More presence and a higher win rate than Driftgate 1's 10–13%; the new target is open. Containment pays every contractor.
- **The AI Unbound stay** as the galaxy's raiders: a threat to your convoys and bases, and bounty work for you.
- **The Freeport Compact stays neutral,** the marketplace of last resort and the independent makers' home.

### 13. Multiplayer: rival companies
- **Each pilot runs their own company.** Friends can partner (post jobs for each other, share convoys) or compete.
- **Pilots can fight each other** when their companies are at odds, or on jobs for opposite sides. Standing between companies works like standing with a power.
- **The host model stays:** the host simulates, guests send inputs, and guest actions run on the host through `runAs` and `dockAction`.

### 14. Galaxy length and pacing
- **A galaxy is played over several sessions.** Growing from one light ship to a declared faction needs room. A galaxy already freezes while nobody is online.
- **The war's clock slows to match.** Capitals from minute 45, the 2-hour deadline and Overgrowth from minute 20 all need new values. Proposal: a typical galaxy is won in about 8–12 hours of play.

### Rules Beyond keeps
- **The ledger is exact.** Components, parts, payload, bases and AI ships are all made of real goods from real rock.
- **The host simulates;** guests send inputs.
- **The war is checked by simulation.** Driftgate 1's target (the three powers about 30% each, the Brood 10–13%) changes with a stronger Brood; new targets to agree.

### Open questions
1. **Corporation names.** Two per faction and two per freeport, twelve in all: your own names, or keep these?
2. **Your own brand.** Can a contractor with a Station become a maker, with its own trait on the parts it builds?
3. **Hull upgrades.** What should levels 1–3 give: more hull, hold, energy, a slot? Can every hull reach the extra slot?
4. **Mining laser and charges together.** Scanning a rock shows its ring for the laser and its fault points for charges. Should a charge blast destroy the ring, so you choose one way per rock?
5. **AI upkeep.** Credits only, or credits plus goods (fuel, repairs, payload)? Who receives wages: the Compact, as drafted?
6. **Lair, Depot, Station costs and levels.** The numbers above are guesses; three levels each?
7. **Brood.** What win rate and how much more presence?
8. **Declaring.** What threshold, and can a declared faction collapse back into a company?
9. **Rating loss.** Does Rating only go up, or can failure and deaths lower it?
10. **Legacy across galaxies.** Titles only, or a small head start?
11. **Galaxy length.** Is 8–12 hours of play the right target? Should the 7-system win scale up?
12. **Starting freeport.** One for every new contractor, or a choice of three?
13. **Faction careers.** Do Halcyon's hauling and Varkesh's mining bonuses survive as bonuses on their jobs? With scouting gone to the AI, what is Ostrova's edge, and does the Vesper (built on the Advanced Scout) survive as a house-brand fighter?
14. **Any scouting left for contractors?** None, or a scanner part that reveals the system you're in?
15. **Flares and drones.** Payload too, or kept as they are?
16. **Hull designs per maker or per power?** One design per class per power, or rival designs from a power's two makers?

### Proposed build order (once the design is agreed)
1. **Cut the faction tie:** start at a freeport with three equipped starters; standing with every power; docking and hostility from standing; pay from the issuer; scouts become AI-only.
2. **Weapon slots and weapons:** slot counts per hull; machine gun with ammunition, laser on reactor energy, missile and torpedo payload; mining laser with rings and charge launchers in mining hulls' weapon slots.
3. **Making things:** ore → components → parts → upgraded parts; grades replace Mk.
4. **Faction jobs screen.**
5. **Unique hull designs, first wave:** each faction's fighters, with their own models and stats, duel-balanced.
6. **Makers:** the corporations, their works and stock; product lines replace variants; AI fleets fitted from their makers.
7. **Progression:** Contractor Rating gates hulls and grades; hull upgrades; remove Legend; drop Unbound mode.
8. **Lairs and the Holdings screen.**
9. **Depots:** markets, hiring and building AI with upkeep; the Economy and Job creation screens.
10. **Stations and station upgrades;** capital ships built at your stations.
11. **Strategic map** with sector zoom and orders.
12. **Declaring a faction;** slower war pacing; a stronger Brood; war checks for the new balance.
13. **Legacy, multiplayer rivalries, training rewrite.**
