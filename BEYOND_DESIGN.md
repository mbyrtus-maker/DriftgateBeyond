# Driftgate Beyond: design

A new game in the Driftgate universe. This file holds its design as it is decided; DESIGN_NOTES.md is Driftgate 1's history up to the fork.

## Fork (Nov 2026)
- Forked from Driftgate 1 v255 with its full code, tools and tests.
- Own identity: browser storage keys `dgbeyond.*` (save `dgbeyond.save.v1`, legend, keys, audio, lore, aces, tips, multiplayer ids), multiplayer host ids `dgbeyond1-<code>-host`, relay topics `dgbeyond1/…`, tab channel `dgbeyond`, title "Driftgate Beyond", invite links to mbyrtus-maker.github.io/DriftgateBeyond/.

---

## Vision (draft 3, 2 Nov 2026; approved, and built in stages 1 to 14: see the "as built" sections at the end for what is in the game and what is not yet)

### In one paragraph
The war goes on, but you no longer fight in it as a soldier. You are an independent contractor who starts at a freeport with one light ship and a few credits, and you take work from whoever will pay. Corporations under the factions and at the freeports (two at each) make what the market sells, and you can make it yourself: ore into components, components into parts, parts into better parts. Your money and materials go up a ladder: ships, then upgrades to those hulls, then a Lair (2 levels), then a Depot (3), then a full Station (5), and finally capital ships built at your stations. From the Depot on you hire AI pilots and ships, pay their upkeep, earn from your own market, post your own jobs and command them from a strategic map. In the end your company declares itself a faction and joins the war as a fourth contender.

### What carries over, what changes, what goes

| Keep from Driftgate 1 | Change | Drop |
|---|---|---|
| Flight, drift by mass, gates, docking | Pilot welded to one faction → **standing** with every power, work for anyone | **Unbound pirate mode** (the start card, crew galaxies, most of Scrapheart Haven's works; its rum bar and market stay open to contractors, section 12) |
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
  - **Light Hauler:** guard drones and a cargo module (decided 2 Nov 2026: drones, not a machine gun).
- **There is no scout start.** The powers' AI scouts still do most of the routine recon. Contractors scout in a different way: intel as a trade good (section 6a).
- **Work for anyone, job by job.** Factions and freeports offer you jobs (the Faction jobs screen, section 9). Later you post your own.
- **Pay comes from whoever issued the job,** out of their treasury. Bounties are paid by the power whose combat job you're flying; with no job running, by the power at war with the victim that you stand best with. Credits stay zero-sum, as now.
- **Nothing is untouchable.** You can fire on anyone; doing so costs standing (section 2).
- **Death, loss and insurance work as in Driftgate 1** (decided 2 Nov 2026): what you lose with a destroyed ship and what insurance pays back are unchanged. **A free starter is always available,** so a pilot who is broke and shipless can always fly again.
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
| Utility | Cargo module, scanner, drone bay, landing kit, hidden cargo container (6b); on scout hulls only, beacon device or limpet rack |

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
- **Claim Beacons for any faction** (decided 2 Nov 2026). Driftgate 1's Claim Beacon (12 t of cargo; carry it into an unclaimed outpost's ring, or a breached depot, and hold there to claim it) is now an item you buy **for any faction you choose**: at a power's station for that power, at a freeport for any power, and, once you own a Depot, for your own company. The beacon claims for the faction it was bought for, whoever carries it. Claiming moves standing like a beacon flip: up with the faction you claimed for, down with the one that held it. As in Driftgate 1 only combat hulls can claim, and a beacon bought for credits is built from that station's plate and conduit, so the ledger stays exact.
- **Claim jobs.** Powers (and later player factions) post jobs to **claim a depot or outpost for them**: carry their beacon in, break or slip past what guards it, and hold the ring. Paid by the issuer, often with a war bonus, and sometimes posted as deniable proxy work (11c) when a power wants ground taken without being seen to take it.
- **Hired intel work.** Factions hire you to **ping a rival's capital ships** (find and mark them) or **place a limpet** on a target, as in Driftgate 1 (a limpeted target is hit harder by the side that ordered it).
- **Discoveries.** Find and sell **comets, derelict cargo and wreckage from anomalies**. Sell the find as intel to a faction or the Compact, or salvage it yourself. (Proposal: finding them needs a scanner, which any hull can fit in a utility slot; scout hulls find them farthest out.)
- **Anomalies move out beyond the gates.** They sit far out past the gate ring, away from the lanes, so finding them means flying out into the empty edge of a system.
- **Ostrova's edge.** Ostrova pays a bonus on intel work (section 12a).

### 6b. Smuggling: contraband, hidden cargo and scanners (decided 2 Nov 2026)
Smuggling is a way to make money outside the law, with its own parts. Names are placeholders.

**What is contraband**
- **Stolen goods.** Cargo taken from a power's ships, convoys or wrecks stays tagged as that power's property, and is contraband in its space. The tag is a mark on real goods, not a new good, so the ledger is unchanged.
- **Embargo goods.** While one power embargoes another (a leader event, 11c), the other's goods are contraband in its space. Embargoes make smuggling pay: demand for the embargoed goods climbs, and smugglers get a premium for running them in.
- **Cash-only contraband.** A few goods that are illegal in every power's space and can only be bought and sold for credits (no crafting use). Proposal: **Ghost relics** (artefacts from anomalies out beyond the gates), **Black data cores** (salvaged from destroyed stations and capitals), **Vael spore extract** (harvested from Brood wrecks). Each comes only from a real find, so the ledger stays exact; markets that buy them use them up, like life support.
- **Riftstone,** a new asteroid type. **Very dangerous** to mine: the rock is unstable, throws off rift discharges that damage nearby ships, its mining-laser ring flickers out, and a blast can set off a chain reaction. Rare, found mostly out beyond the gates. **Embargoed by most powers** (contraband in their space). Refined, it is a **wild-card crafting resource**: a Rift Shard stands in for any one component in any recipe, or adds a random trait to a part as it is upgraded.

- **Pirate gear** (decided 2 Nov 2026). The Unbound's jammers, shock harpoons, jamming torpedoes and cargo hooks can be fitted to your own ship: a jammer in a weapon slot (it fires jam rounds), harpoons and jamming torpedoes as payload for a missile launcher or torpedo bay, a cargo hook in a utility slot. They work as the Unbound's do (section 12): jam a ship dark, then hook its hold, and what you take is tagged stolen from its owner. Bought at Scrapheart Haven's market and from black-market contacts, or taken from Unbound wrecks. **Owning it is no crime, but it is contraband to carry:** if a patrol's scan finds pirate gear on your ship, **that power's heat on you rises** (proposal: Light heat, Heavy if you have jammed one of its ships in the last hour), whether the gear is fitted or in the hold. A hidden cargo container can hide gear carried as cargo, but not gear that is fitted. Using it on a power's ship raises that power's heat as any theft does.

**Hidden cargo containers** (a utility part). A concealed hold that keeps goods out of scans. Its grade sets how much it holds and how well it hides it (proposal: 4 t at grade 1 up to 20 t at grade 5). It takes a utility slot, so hiding cargo costs a scanner, a drone bay or a landing kit. Sold by freeport makers, or built.

**Scanners** (a utility part, already used to find discoveries). **Only the powers' AI patrols do customs:** they scan ships in their space now and then, more often near stations and gates and the lower your standing; a scan takes a few seconds in range and you are warned it is coming. A patrol's scanner grade against your hidden container's grade decides how likely it is to find what is hidden. Players' scanners are for discoveries and do no customs work.

**When a scan finds contraband,** you choose:
- **Bribe:** pay credits into that power's treasury. More likely to work at better standing; patrols of a Vengeful leader refuse. A refused bribe counts as a worse offence.
- **Surrender:** the goods are confiscated into that power's stores (the ledger stays exact), a fine, and a small standing hit.
- **Run:** you keep the goods, but that power turns hostile to you for a while and posts a bounty on you.

**Heat** (decided 2 Nov 2026). Each power keeps a heat level on you, separate from standing: how hard its patrols are looking for you right now. Getting caught, a refused bribe, running from a scan, and taking cargo from its ships all raise it. While it is up, its patrols scan you more often and with less warning, and after a run it is what keeps that power hostile and the bounty open. Heat cools off on its own over time; standing only takes the lasting hits (the fine and the surrender hit above). The HUD and the Black market tab show your heat with each power as a word (Cool, Warm, Hot, Burning), with no numbers.

**Lairs are a smuggler's base** (decided 2 Nov 2026):
- **Heat cools faster** while you lie low at one of your Lairs (proposal: three times as fast while docked there).
- **Stolen goods are laundered there:** cargo stored in a Lair's stash loses its stolen tag (proposal: after a short spell in the stash, longer for more tonnes), so it sells and is carried as ordinary goods afterwards. Only the stolen tag comes off: embargo goods and cash-only contraband stay contraband, since what makes them illegal is what they are, not whose they were. The goods themselves never change, so the ledger is unchanged.

**The Black market tab** (on the Company screen, decided 2 Nov 2026) is where smuggling is run as a business. **Request** black-market work from your contacts (fixers at the freeports, quiet buyers at the powers' stations, and the Rusty Tankard's rumours once you have been to Scrapheart Haven, section 12): smuggling runs, contraband buys and sells, Riftstone hauls, each priced by supply and demand, with embargo premiums showing. **Black-market work pays by the heat it would bring if you are caught** (decided 2 Nov 2026): every offer is rated **None, Light, Heavy or Severe** with the power whose heat it raises (running embargo goods into the embargoing power's core systems is Severe; buying contraband at a freeport is None), and the pay rises with the rating on top of the goods' market value (proposal: +0%, +25%, +50%, +75%). You can filter offers by it. If caught, the job's heat lands on whoever ran it: half of it if a bribe works, all of it on surrender, double if you run. **Assign** each run to yourself, to one of your AI pilots (whose ship's hidden cargo container sets how much it can hide), or to a contractor, and follow the runs in progress: where they are, which patrols are near, and what each run was caught for or paid.

**Where it sells: everywhere that wants it,** by supply and demand. Each market's demand sets the price, whether the goods are legal there or not; an embargo or a ban pushes demand and price up where the goods are scarce. Powers and freeports may post smuggling runs as jobs (deniable proxy work, 11c).

### 7. What you spend on: the ladder
Players have several things to spend money and materials on, in this order, each with its own levels:

| Step | What it is | Levels (proposal) |
|---|---|---|
| 1. Ships | Build hulls up the Rating ladder | Light → Medium → Heavy → specialist |
| 2. Hull upgrades | Upgrade the hull you fly | Levels 1–3: stats only (hull, shield, energy or hold); slots never change |
| 3. **Lair** | Your first base, hidden in a large asteroid | 1–2 |
| 4. **Depot** | Your first open base, with a market and a hangar | 1–3 |
| 5. **Station** | A full station that counts for the system | 1–5 (one external building per level) |
| 6. Capital ships | Built at your stations | Escorts, then destroyers, then carriers |

#### Lair (from Driftgate 1's Unbound Lair)
- **Building:** a Rigger kit (proposal: 1 Depot Frame + 20 plate) set into a large asteroid in any system with no station.
- **Hidden** until a scout of a hostile power comes within range (AI scouts find Lairs, as in Driftgate 1).
- **Level 1:** stash (200 t), repairs and rearming. **Lie low** (heat cools faster while you are docked) and **launder** stolen goods in the stash (section 6b).
- **Level 2:** your own workshop (components, parts, upgrades and payload with no fee), a forge (lattice, core), a bigger stash, and a spare berth to keep a second ship.
- **Up to four Lairs per company** (decided 2 Nov 2026), anywhere on the map. **A system holds one Lair per player or faction:** several companies (and the Unbound) can each have a Lair hidden in the same system, but no one can have two there.

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
- **You can fly your capitals yourself,** much as in Driftgate 1: the bridge you walk, the helm and consoles, landing aboard and launching from the hangar, guests riding along (decided 2 Nov 2026).
- **When a base falls** (decided 2 Nov 2026): the AI that takes one of your Lairs, Depots or Stations decides whether to **capture** it, gaining it at least 75% intact with its buildings and stores, or **destroy** it, so everything there is lost. A captured base can be taken back; a destroyed one is gone.
- **Capital ships** are built at the yard, which must be among the station's buildings: **escorts** from station level 3, **destroyers** from level 4, **carriers** at level 5.
- **The destroyer** (decided 2 Nov 2026) is the line ship between the escort and the carrier: bigger than an escort, smaller than a carrier, built around a **main gun** that kills other capitals and stations, with **point-defence turrets** like the other capitals. It has no hull berths, so it is weak against swarms of small ships on its own, but it carries **two assault ships** (decided 2 Nov 2026), between the escort's one and the carrier's three: its main gun breaches a station and its assault ships take it. **The Brood have their own destroyer** (the Gullet): no shields, and a **Maw Cannon** that charges and then fires a beam doing incredible damage to everything along its firing path. **The main gun fires a charged shot:** it has to charge before each shot, and **while it charges the ship's shields are down**, so every shot is a window an enemy can punish (charge time, damage and the shield drop are tuning numbers).
- **Assault ships carry over from Driftgate 1** (decided 2 Nov 2026): a depot or outpost is captured by breaching it and landing assault ships until its garrison is spent, with at most three in flight per faction. Escorts carry one, destroyers two, carriers three. **Your own capitals carry them the same way,** your stations with a shipyard build them, and you call them in from your own shipyard as a faction pilot calls in theirs. The Unbound have none: the Ravager's boarding pinnaces take cargo, never ground. **Art:** one shared assault ship model for every faction for now, in each faction's colours (and your company's). Driftgate 1 never drew its assault ships (they were loads aboard capitals), so the shared model is new: **approved** (2 Nov 2026), `tools/previews/beyond_assault.png` (from `beyond_assault.py`, sheet `assault_sheet.py`), a squat armoured dropship with a slit cockpit in a blunt nose, a troop bay with a marine door each side and a ramp astern, four vectoring thrusters on stub pylons, landing skids and a roof point-defence gun.

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
| **Economy** | Income and costs: market sales, jobs, AI upkeep, wages. Treasury, stock at each base, and what each base buys and sells. **A credit trend for the company and for each base** (decided 2 Nov 2026): whether each Station, Depot and Lair is gaining or losing credits, its net per hour and its trend over the last hours, and **why**, in plain words with the lines behind it ("Losing: the Varkesh embargo cut trader visits by half; market +1,200, defence and guards −1,640"). |
| **Job creation** | Post jobs: to your own AI pilots (mine this field, haul this cargo, **guard** (one kind for escorting a ship or convoy and defending a base, decided 2 Nov 2026), patrol, hunt, **intel**: flip a beacon, ping a capital, plant a limpet, survey for discoveries, flown by scout hulls), to other contractors in multiplayer, and to **other factions' pilots** (their AI and the players sworn to them), paid from your treasury. |
| **Faction jobs** | What the factions and freeports will hire you for, filtered by your standing: pay, risk, standing gained, the faction bonus. |
| **Allegiance** | Your standing with every power (the three factions, the Compact, each player faction) **shown as a bar with its band's name (Hostile, Unwelcome, Neutral, Trusted, Partner) and no numbers** (decided 2 Nov 2026), and what it opens; the relations between the factions **shown as their band's word, coloured accordingly** (War in red, Hostile, Neutral, Friendly, Allied in green), with no numbers; the relations between the factions themselves (at war, truce, allied, neutral), so you can see how a job for one lands with the others; each leader and their recent decisions. Declare or renounce allegiance here; a founder answers other factions' proposals here. |
| **Strategic map** | The galaxy map, zoomable into a sector to see your bases, AI ships and the threats there, and give orders to your AI in that sector. |

**Bidding on posted jobs (decided 2 Nov 2026).** The pay for a job you post is a bid against the **galactic mean**: what that kind of job pays across the galaxy, for its distance and risk. Three presets:
- **Low:** the floor; the job is picked up slower (a longer wait before anyone arrives).
- **Medium:** the mean; normal arrival time.
- **Fast:** higher pay; the job is taken and done sooner.
- **Mins and maxes:** you can't bid below Low, and there is a maximum; between them you can set an exact figure. Proposal: Low 75% of the mean, Fast 140%, the maximum 200%, all tuning numbers. Pilots who can take a job (contractors, other factions' pilots) weigh its pay against the mean, so the higher the bid, the sooner one signs on. Your own AI pilots are paid wages, so a job posted only to them needs no bid.

These reuse what Driftgate 1 has where they can: the station's task tabs, the Jobs board, the galaxy map and its sector panel.

**Where they live (decided 2 Nov 2026).** Driftgate 1 has no in-game menu: docked screens have five tabs (Overview, Trade, Jobs, Ship, Station, keys 1–5), and M opens the galaxy map.
- **One new Company screen** holds, in this order, **Allegiance** (it opens there), **Holdings, Economy, Post jobs, Black market**, and a **read-only Faction jobs** tab so you can browse work in flight. It opens anywhere, in flight or docked, with its own key (proposal: **0**, since every letter is taken) and a **Company** button on the HUD beside Map, and works like the galaxy map: a full screen over a running game, closed with Esc.
- **The Strategic map grows out of the galaxy map** (still M): click a sector to zoom into a live view of it, with your bases, your AI ships and the threats there, and give your AI orders (guard, mine here, escort, patrol), as the capital bridge's Strategic console already does for one ship.
- **Faction jobs replace the dock's Jobs tab,** where you sign on; the Company screen's copy is for browsing.
- **The title screen offers:** the freeport and role cards (in place of the faction cards), the **Legend start package** (spend start points on your unlocked perks), and keeps **Training** and the **Leaderboard**, which ranks pilots by **Legend level** (decided 2 Nov 2026). The company's name and colour are not chosen there.
- **Mockups: approved (2 Nov 2026), with the tab order above, the Light Hauler's drones, posted jobs open to other factions' pilots, bidding, the per-base credit trend, the Black market tab, and the Allegiance tab without numbers.** the Design canvas "Driftgate Beyond screens" (https://claude.ai/artifact/J1zRwXEc74WSmS59L2fjbP) holds seven screens in Driftgate's own look (Big Shoulders Display, Saira Semi Condensed, JetBrains Mono, amber on near-black): the title screen; the Company screen's Holdings, Economy, Post jobs and Allegiance tabs (their tabs link to one another in Play); the docked Jobs tab with faction jobs; and the galaxy map zoomed into a sector with orders. The example company is "Ashfall Hauling" in sky blue.

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
| Station level 4, with a yard | Destroyer |
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
- **Once declared,** you're a contender: you can win the galaxy (below), and the truce against whoever starts the win timer applies to you too. Your faction starts Neutral with every other faction (11b); how the powers treat you from then on is up to the ledger and their leaders.
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
| Alliance proposal | Relation above +60 and a shared threat (a faction nearing the 20 systems that win, or the Brood spreading) | Patient, Cautious, Honourable (never Isolationist) | Formal alliance if the other accepts | + large |
| Border dispute | Both factions build or hold depots in neighbouring systems | Ambitious, Industrious, Isolationist | A demand to withdraw; announced with a deadline | − small |
| Embargo | Relation Hostile, or the other undercut its markets or raided its trade | Mercantile, Vengeful | Trade between them stops | − |
| Proxy work | A rival (or even an ally) is getting ahead | Scheming | Deniable contractor jobs posted against it | none, unless exposed |
| Exposure | A proxy job is traced (more likely if many run, or a sworn pilot does it) | (anyone exposed) | The victim learns who posted it | − large |
| Reprisal | A large negative from the other (a siege, a capture, repeated convoy raids) | Vengeful, Ruthless | A strike or raid back at the offender | − |
| Declaration of war | Relation below −50 and an unanswered wrong, or a rival leading in systems | Ambitious, Vengeful | Formal war: campaigns and sieges begin | − large |
| Ceasefire offer | War-weary: heavy losses, a low treasury, or the Brood pressing both | Cautious, Mercantile, Honourable | Offer of peace; holds if the other is also weary | + |
| Betrayal | Allied, but the ally nears the 20 systems that win, or is rich and weak | Ambitious, Scheming, Opportunist | Alliance broken; telegraphed by cooling relations first | − very large |
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
| Long peace with treaties kept on both sides | Honourable |
| Its stations razed, or its leader killed by treachery | Ruthless |
| Short of goods and parts after a long war | Industrious |
| Lost a war fought far from home | Isolationist |
| A neighbour weakened by the Brood or a long war | Opportunist |

**AI pilots fly like their leader** (decided 2 Nov 2026). Every AI pilot of a power (fighters, escorts, miners, haulers, scouts, capitals) behaves the way its current leader's traits lean, so a faction's character shows in how its ships fight and work, not only in the events feed. A leader has two traits, so pilots blend both.

| Leader trait | How that power's pilots behave |
|---|---|
| Ambitious | Aggressive: press attacks, chase further, contest outposts, take more risk |
| Vengeful | Never break off when a squadmate is destroyed: they stay and fight; they remember who killed theirs and go for that faction or pilot first |
| Mercantile | Guard convoys and traders before miners and outposts; avoid costly fights; break off to protect cargo |
| Cautious | Break off sooner when outnumbered or damaged; keep formation; defend home space first |
| Scheming | Hit and run, pick off isolated ships, ambush at gates, use scouts and contractors more |
| Patient | Hold positions and wait for reinforcements; attack late and in force; slow, careful sieges |
| Wary (successor) | Keep their distance from allied ships; patrols scan more often |
| Loyal (successor) | Answer allies' distress calls; guard allied convoys |
| Zealous (successor) | Put the Brood above every other target; push into Brood space |
| Honourable | Never fire on disabled or fleeing ships; accept surrender; rescue downed pilots; keep to treaties (and post no proxy work) |
| Ruthless | Finish off disabled ships; go for miners, haulers and convoys first; raze bases rather than capture them |
| Industrious | Guard miners and constructors first; build depots and outposts; avoid wars while building up |
| Isolationist | Stay in home space and hold the borders; never answer allies' calls outside it; refuse alliances |
| Opportunist | Strike whoever is weakest right now; join fights already under way as a third party; loot wrecks; switch targets fast |

- **A new leader changes the fleet.** After a succession, pilots shift to the new leader's style as new orders go out, so a war-weary Cautious successor's ships really do start breaking off.
- **Aces and a leader's own escort** fly the same way, more skilfully.
- **Checked by simulation** with the leaders (stage 2): trait behaviour moves faction strength, so it goes through the war checks.
- **Your faction's traits:** when you **declare your faction**, you pick its two traits from the whole list (decided 2 Nov 2026), and your AI pilots fly by them from then on, so a founder's faction has a character too. Before you declare, your company's AI pilots fly a plain, balanced style.
- **Five more traits** (decided 2 Nov 2026): Honourable, Ruthless, Industrious, Isolationist and Opportunist join the list, for leaders, successors and founders alike.

**Distress calls in Brood space are answered by every faction** (decided 2 Nov 2026). A distress call sent from a system the Brood holds brings nearby pilots of every power, whatever their relations, even at war; while answering they fight only the Brood.

**Storylines, not fixed alignments.** Nothing is permanent. Over a galaxy, two factions can go from wars of annihilation to friendship and back: a war, a weary ceasefire, a new Cautious leader, a trade pact, a shared fight against the Brood, an alliance, then a betrayal by an Ambitious successor. Each step has its trigger, and the Allegiance screen keeps a **chronicle** of each faction's leaders and decisions so the story can be read back.

**Rules that keep it reasoned, not chaotic**
- **Cause first.** An event fires only when its trigger is true in the galaxy right now; personality only chooses among eligible events.
- **Escalation, not jumps.** Relations change by steps: dispute → embargo → reprisal → war, and back down through ceasefire → pact → alliance. No faction goes from Friendly to war in one event, except a telegraphed betrayal. Big turns usually come with a new leader.
- **Memory.** Leaders remember the ledger: grudges fade slowly (more slowly for a Vengeful leader), favours too.
- **Pace.** Each leader acts at most once every few minutes, and each pair of factions has its own cooldown.
- **Announced with a reason.** Every event goes to the feed in plain words: who, against whom, and why ("The Marshal declares war on the Accord after the siege of Tessellate Reach").
- **Checked by simulation.** Leaders drive whether the war happens at all, so their weights and cooldowns are tuned with war checks: the galaxy must still go to war, and the Brood must still win only about 20%.

#### Winning the galaxy
- **Twenty systems win** (decided 2 Nov 2026). Any faction (the three powers, the Brood, or a declared contractor faction) that controls **20 systems** starts a 10-minute timer. Hold 20 to the end and it wins. A fixed number, not a share of the map: on the new map that is 20 of the 42 systems that can be held, just under half.
- **Freeports can't be captured and don't count** (decided 2 Nov 2026): freeport systems can't be held, nor can the Wrack, whose haven can't be destroyed; on the new map that leaves 42 systems that can be held, of 46.
- **The others unite when the timer starts.** As in Driftgate 1, the rest of the factions call a truce and turn on whoever has started the win timer; the truce breaks if the timer stops.
- **No other time limit.** There is no deadline and no tie-break count: a galaxy runs until someone wins. (Driftgate 1's 7 systems for 20 minutes and its 2-hour deadline go.)

### 12. The war around you
- **The three factions fight on, AI-driven:** campaigns, depots, forges, sieges, capitals, the truce against the leader.
- **The Brood is stronger:** more presence, and it wins about **20%** of AI-only galaxies (Driftgate 1: 10–13%). Containment pays every contractor.
- **The Brood starts slow and grows with what it holds** (decided 2 Nov 2026). Early in a galaxy it holds only the Bloom and is a nuisance: small swarms, slow regrowth, rare offensives, little Overgrowth, and Gullets and Hive Ships kept home. **Every system it takes makes it stronger:** more biomass, faster regrowth, bigger and more frequent offensives, more Overgrowth, and its heavy ships coming out. A Brood that is pushed back shrinks again, so containment early is cheap and containment late is a war. Proposal: one strength scale driven by the systems it holds (about 0.5× of today's Driftgate 1 Brood with the Bloom alone, 1× at about five systems, up to 2× at twelve or more), with its heavy ships unlocked by size (Hive Ships from about four systems, the Gullet from about eight). The curve is tuned with the war check so the Brood still wins about 20% overall: rarely, but unstoppably once it gets going. The Containment front (11c) fires as it ramps up, so the powers turn on it when it is getting dangerous, not before.
- **The AI Unbound stay** as the galaxy's raiders: a threat to your convoys and bases, and bounty work for you. Decided 2 Nov 2026:
  - **They hold no systems.** They ambush and they build **Lairs** (hidden asteroid bases like a contractor's) to raid from.
  - **They have no economy but plunder.** Everything they have, they took: goods, payload and hulls come from raids, ambushes and wrecks, so the ledger stays exact.
  - **They fly only their six designs** (Raider, Skiff, Corsair, Plunderer, Wrecker, Ravager).
  - **The Ravager is their only capital, and it fills every capital role** (decided 2 Nov 2026), where Driftgate 1 had a Corsair Sloop and a Destroyer:
    - **Escort:** it rides with raiding parties and guards a Lair, its point defence covering the wing.
    - **Line ship:** its Varkesh giant gun is a charged main gun like a destroyer's (shields down while it charges), and the salvaged rail cannon backs it up.
    - **Carrier:** a hangar launches a small wing of whatever hulls the Unbound have plundered (proposal: up to four Raiders, Skiffs or Wreckers, refilled only from stock at Scrapheart Haven or a Lair, never grown or built).
    - **Boarding:** two boarding pinnaces (back from Driftgate 1's Destroyer) dock with a capital, station or depot that has been jammed dark and hook its material store into the 400 t plunder hold. This is how the Unbound take a capital's cargo instead of just fighting it.
    - It does each role less well than a faction's dedicated ship, and there are few of them (proposal: one per galaxy at first, a second once the Unbound's plunder can crew it). Art **approved** (2 Nov 2026): `tools/previews/beyond_ravager.png` (sheet `ravager_sheet.py`): a Varkesh hangar keel under the midsection with bay doors hinged open and a lit bay, and two boarding pinnaces (sand-plated Varkesh wedges, Halcyon canopies, grapple claws) held off the Ostrova stern on clamp arms.
  - **Scrapheart Haven is their one main station, one per galaxy,** in the Wrack, out in deep space (12b). It can be **deactivated** (knocked out for a while) but **never destroyed**. **Deactivated, it is closed and looted** (decided 2 Nov 2026): its rum bar and market shut and Unbound raids slow (proposal: for 30 minutes), and the attackers take a share of the Unbound's plundered stores (proposal: a quarter of each good and of their credits), moved into their own stores so the ledger stays exact.
  - **The Dread Pirate leads them** (decided 2 Nov 2026): a leader like the powers' leaders, with its own personality table (12c).
  - **Jammers and hooks, as in Driftgate 1** (decided 2 Nov 2026). Unbound guns fire jam rounds that knock shields down and then fill the target's **Jam bar**; at a full bar the ship goes dark (no thrust, guns, shields or radar, and it can't jump) for a window by size, and an Unbound ship within 150 m runs its **cargo hook** (8 t/s, most valuable first) until the window closes. Shock harpoons (35% of the bar, stretching the hook to 400 m), jamming torpedoes (Plunderer and Wrecker; the only way to jam a capital, turret by turret), one disable per ship then 60 s hardened, and the being-jammed effects all carry over. What they hook is plunder: it goes into the Unbound's stores, tagged stolen from whoever owned it. **Contractors can fit them too** (decided 2 Nov 2026): they are pirate gear, contraband in every power's space (6b). Driftgate 1's anti-jam parts (Faraday plating, fast-reboot reactor, snap-back emitter, sealed hold) become makers' products, so a convoy runner can buy protection.
  - **Bigger holds** (decided 2 Nov 2026): Unbound hulls are built to carry plunder, about half again the matching faction hull's hold. Proposal from Driftgate 1's holds: Skiff 50 t (was 35), Raider 60 t (40), Corsair 100 t (70), Plunderer 160 t (110), Wrecker 60 t, and the Ravager a 400 t plunder hold.
  - **You can dock at Scrapheart Haven** (decided 2 Nov 2026). The haven is open ground: its guns and the Unbound in the Wrack hold fire on any ship that comes in without firing on them (proposal: attack an Unbound ship in the Wrack and the haven bars you for an hour). Out in the lanes the Unbound still hunt you. No power's patrols scan there, so it is the one dock where contraband is never a risk.
    - **The rum bar** (the Rusty Tankard, from Driftgate 1) sells **rumours, which are black-market jobs:** smuggling runs, contraband buys and sells, Riftstone hauls, and word of rich convoys and wrecks, priced by the heat they'd bring (6b). Once you have drunk there, the Tankard is a contact on your Company screen's Black market tab, so you can take its rumours from anywhere.
    - **The market** buys and sells **regular goods and black-market goods alike,** at supply-and-demand prices, with no questions about the stolen tag. It trades from the Unbound's plundered stores and pays from their plundered credits, so the ledger stays exact: selling there feeds the pirates.
- **The Freeport Compact stays neutral,** the marketplace of last resort and the independent makers' home.

### 12a. Faction job bonuses (from Driftgate 1's careers)
Each faction pays contractors a bonus on the work it cares most about, out of its own treasury, shown on the job:
- **Halcyon:** hauling jobs.
- **Varkesh:** mining jobs.
- **Ostrova:** intel work (beacon flips, pings, limpets, discoveries) and escorts.

Their signature hulls survive as house-brand hulls built with Partner standing: the Gannet (Halcyon), the Bombard (Varkesh) and the Vesper (Ostrova).

### 12b. The galaxy map (approved 2 Nov 2026)
A new map, not Driftgate 1's, built on the same rules: **no two gate lines cross and no line runs past another system.** Preview: `tools/previews/beyond_map.png`, from `tools/previews/beyond_map.py`, which also runs the checks (planar, clear of other systems, freeports' exits, every system reachable). Names are placeholders.

- **Deep space is the middle of the galaxy.** **The Bloom sits at its centre,** with gates to all five systems of an inner deep ring (Glass Shallows, Corona Deep, Lantern Deep, Ashen Expanse, Umbral Deep), and a deep rim of six (Gloam Deep, Mournwater, Thornmere, Rustmere, Sunken Reach, Blackwater Rift). Both rings are linked round.
- **The Wrack is the most remote place in the galaxy** (decided 2 Nov 2026): a pocket between the two deep rings. It has three gates, all to empty deep systems: one to the inner ring (Umbral Deep), and two to small deep systems of its own, **Bilgewater** and **Scuttle Rift**, each of which leads on to the outer deep ring (Thornmere and Rustmere). Nothing that matters is one jump away: the Bloom is two jumps, the nearest freeport and the nearest open space three, every power's frontier four or more. Deep space holds aurorite, anomalies, Riftstone and the Brood, far from any power's guns.
- **Every route to a freeport crosses deep space** (decided 2 Nov 2026). The freeports are not in deep space: each sits in its own pocket just outside it, but **both of its two exits are gates into the deep rim,** so there is no way to a freeport that doesn't pass through deep space. Mirrorwater (Sunken Reach, Blackwater Rift) lies behind Kestrel Drift, between Halcyon and Varkesh; Coldwater Drift (Thornmere, Rustmere) behind The Shoal, between Ostrova and Halcyon; Ember Wake (Gloam Deep, Mournwater) behind Cinder Reach, between Varkesh and Ostrova. The Compact's trade, contractors' freight and a new pilot's first trip out all run through deep space, which is one reason the Brood starts slow.
- **Open space is the doors to deep space.** A ring of twelve around it alternates the powers' frontiers, the three forges and six quiet systems (Dusk Lanes, Fathom's Edge, Quietwater Sound, Hushfall, Coldlight Void, Brinewell). The powers reach deep space only through those quiet systems.
- **The three powers sit at even distances from the Bloom:** Varkesh to the north-east, Ostrova to the south, Halcyon to the north-west, each a core on the outer ring with its frontier inside it. Each forge lies between two powers' frontiers: Kestrel Drift (Halcyon and Varkesh), Cinder Reach (Varkesh and Ostrova), The Shoal (Ostrova and Halcyon). Hollow Verge, the relay, sits by Ostrova.
- **More open space:** 46 systems (Driftgate 1: 29), 21 of them open space (18 quiet systems and the 3 freeports, against Driftgate 1's 14), with quiet systems out to all four corners. **No dead ends:** every system has at least two gates.
- **Rebalance.** The Bloom moves from the edge (one gate, Driftgate 1) to the centre with five, so the Brood reaches every power. That suits the stronger Brood (about 20%, section 12), but the faction mining and Brood knobs are retuned with the war check when the map is built.

### 12c. The Dread Pirate: the Unbound's leader (decided 2 Nov 2026)
The Unbound are led from the Wrack by **the Dread Pirate** (the title passes with the hat; names are placeholders, e.g. "the Dread Pirate Marrow"). The Dread Pirate is a **leader in every respect** (11c): out flying, rarely docked (only ever at Scrapheart Haven), in the Ravager when it's out or a Corsair otherwise, **always with an ace escort**, met in the world and shown on radar by name. It **can die,** which triggers a succession, and every power pays a large bounty to whoever kills it. It **makes work:** powers post jobs to hunt it, rumours of its movements sell at the Rusty Tankard, and its events go to the feed with a reason. **Unbound pilots fly like it** (as the powers' pilots fly like their leaders), and it acts at most once every few minutes.

It has **two traits from its own table,** not the powers' list. The Unbound have no relations with anyone, so its events don't move relations: they move credits, goods and heat, and set where the raiders go.

| Pirate trait | How the Unbound fly |
|---|---|
| Bloodthirsty | Kill rather than take: finish jammed ships, hit escorts and patrols, raid depots for the fight |
| Greedy | Take, never kill when a take is possible: richest holds first, mercy takes, long hook windows; hoards plunder at Scrapheart |
| Cunning | Ambush at gates in deep space, bait with false distress calls, strike from Lairs and slip away before patrols come |
| Showman | Go after famous targets (aces, leaders' escorts, the leading power's convoys) and announce raids in the feed beforehand |
| Superstitious | Avoid Brood-held systems and the Bloom; break off at the first lost capital or a bad omen (a Riftstone blast, an ace's death) |
| Gallant | Let crews go after a take, keep bargains and bribes, never touch rescue or aid convoys; ransom rather than kill |
| Paranoid | Keep raiders close to the Wrack and the Lairs, many Lairs, few far raids; bar contractors from the haven at the first offence |
| Kingmaker | Raid whichever power is leading the galaxy, and sell plunder cheap to whichever is losing |

**Its events** (each needs its trigger; traits choose among eligible ones):

| Event | Trigger | Who leans to it | What happens | Ledger |
|---|---|---|---|---|
| Raiding season | A power's convoys run rich and lightly guarded | Greedy, Bloodthirsty | Raids focus on that power's lanes for a while | none (raids are real) |
| Tribute demand | A power's trade runs past Unbound Lairs | Greedy, Cunning | The power pays credits to be spared for a while; refusal brings a raiding season | credits move |
| Ransom | The Unbound jam a leader's escort, an ace or a rich convoy | Gallant, Greedy | Its owner can buy the ship or cargo back, or lose it | credits or goods move |
| Bounty on a pilot | A contractor sinks Unbound ships or hunts the Dread Pirate | Bloodthirsty, Paranoid | A pirate bounty on that pilot, paid at Scrapheart | credits move when paid |
| Ravager raid | The Ravager is ready and a depot or station is weak | Bloodthirsty, Showman | The Ravager sails to board it | goods move |
| Hoard sale | Scrapheart's stores are full | Greedy, Kingmaker | The market sells plunder cheap for a while | trades |
| Open house | Quiet times, a full treasury | Showman, Gallant | The rum bar's rumours pay more for a while | none |
| Lair spree | Raiders are being hunted in the lanes | Cunning, Paranoid | New Unbound Lairs go up | goods consumed |
| Lie low | The Brood is spreading, or the Dread Pirate's ship was badly hurt | Superstitious, Paranoid | Raids pause; the raiders stay in the Wrack | none |
| Succession | The Dread Pirate is killed, the haven is looted, or the captains lose faith after a long run of losses | (any) | A captain takes the hat | none |

**Successors** come from the Unbound's aces and are shaped by what happened:

| What happened to the Unbound | The new Dread Pirate is likely to be |
|---|---|
| The Dread Pirate killed by a power | Bloodthirsty, with a grudge against that power |
| Killed by a contractor | Paranoid, and puts a bounty on that pilot |
| Scrapheart Haven deactivated and looted | Paranoid or Cunning |
| Fat years of plunder | Greedy or Showman |
| Many raiders lost to the Brood | Superstitious |
| A power growing toward 20 systems | Kingmaker |
| A long run of failed raids | Cunning |
| Bargains kept, ransoms paid | Gallant |

### 13. Multiplayer: rival companies
- **Each pilot runs their own company.** Friends can partner (post jobs for each other, share convoys) or compete.
- **Pilots can fight each other** when their companies are at odds, or on jobs for opposite sides. Standing between companies works like standing with a power.
- **The host model stays:** the host simulates, guests send inputs, and guest actions run on the host through `runAs` and `dockAction`.

### 14. Galaxy length and pacing
- **A galaxy is played over several sessions.** Growing from one light ship to a declared faction needs room. A galaxy already freezes while nobody is online.
- **No deadline.** The galaxy runs until a faction holds 20 systems for 10 minutes.
- **The war's clock slows to match.** Capitals from minute 45 and Overgrowth from minute 20 need new values. Working target for tuning: a typical galaxy is won in about 8–12 hours of play.

### Assets: models and art
**What exists (from Driftgate 1's model pack):** 17 ship models shared by every faction (the fighters are 5 Quaternius "Lowpoly Spaceships"; miners, haulers and the constructor are Kenney Space Kit craft with parts added; carrier and escort are assembled from Kenney parts in `tools/capitals.py`), 11 Brood models generated in code (`tools/brood.py`), and the structures: station, depot, asteroid base, yard, forge, relay and six works modules. All CC0.

| Need | Covered? |
|---|---|
| Unique hulls: 13 classes × 3 factions, three capitals each, the Unbound set and the Brood destroyer | **Designed and approved** as previews (below); not in the model pack yet. Constructors and drones designed and approved too (support sheet) |
| Lair, Depot, Station (standard and asteroid look) | **Designed and approved** (below) |
| Station external buildings | **Designed and approved:** the six buildings |
| Faction stations and depots, the freeport, Scrapheart Haven | **Designed and approved** (below) |
| Brood, leaders, ace escorts | Yes (leaders fly ordinary hulls) |
| Mining-laser ring, comets, anomalies, beacon devices, Riftstone asteroids | Effects drawn in code. **Riftstone look: approved** (2 Nov 2026): `tools/previews/beyond_riftstone.png` (from `beyond_riftstone.py`, sheet `riftstone_sheet.py`): a dark, jagged rock with flat-cut facets, split by zigzag rifts glowing in its own hot pink (`#ff4fc8`, unlike any power), white-hot points along them, loose shards drifting off, and discharges arcing from the cracks |
| New screens | HTML and CSS, no assets |

- **Hulls are generated in code, one design language per faction**, the way the Brood is: Halcyon long, swept and bird-like with glass canopies; Varkesh blocky armoured slabs with exposed guns; Ostrova slender spires with a reactor halo, sensor masts and crystal. Each class is a set of parameters in its faction's language. Previews (the method approved, and all nine fighter designs approved, 2 Nov 2026): `tools/previews/beyond_light_fighters.png` (Swift, Fang, Mote from four angles) and `beyond_fighters_by_faction.png` (Light, Medium and Heavy fighters: Halcyon Swift, Kite, Osprey; Varkesh Fang, Talon (a pincer), Halberd (a brawler: an armoured core with a chisel prow and four gun-and-drive pods on an X of slab arms); Ostrova Mote (one halo), Wisp (a crescent joined to the spire by one pair of wings), Vigil (a tuning fork: a broad crystal-veined body, twin forward prongs holding a focus crystal, and two halos crossed in an X round the hull; close-up in `beyond_vigil.png`)). Rule from review: within a faction, every size has its own silhouette, not a bigger copy of the light one, from `tools/previews/beyond_hulls.py` and `render_beyond.py`.
- **Miners and haulers: all 18 approved (2 Nov 2026) after several rounds of review.** set further apart from the fighters without leaving the faction look: about 12% more girth, blunter noses, smaller Halcyon tail fins, no gun barrels on the Varkesh haulers, and industrial details (exhaust stacks on Varkesh, hull ribs on Halcyon, floodlights at the front of every ship). `beyond_miners_by_faction.png` and `beyond_haulers_by_faction.png`, from `tools/previews/beyond_work.py`. The first pass looked like fighters; the second bolted kit parts onto Driftgate 1's work ships. The third pass is wholly new craft built in code, taking **proportion and purpose from Driftgate 1's work ships** (stubby, wide industrial bodies; miners with forward drill arms, mining lenses, ore hoppers and charge launchers; haulers with big holds and containers) and **shape language from each faction's approved fighters**. Halcyon (lens hulls, glass, twin tails, the Osprey's booms): Wren (a chubby lens pod, bubble canopy, two drill arms hugging the nose), Plover (twin hopper booms with drills either side of a cockpit pod, no spoiler), Heron (a broad flattened hull with two stacked hoppers, drills and four drives, no nose laser); Tern (a short cockpit hull with its cargo hold joined on behind, forked tail), Albatross (a thick flying-wing whose wings are cargo bays), Pelican (a huge cargo pouch hull between two big engine pylons, no spoiler). Varkesh (hex slabs, chisel prows, pincer sponsons, square drives): Pick (a stubby hull with two short drill sponsons), Gouge (a broad hull with three mining lasers across the prow, every box angled: chamfered ore bins, mount and drives), Sledge (the Heron's layout in Varkesh form: a broad, bulky hex hull, two stacked hex hoppers, four mining lasers, drone bays, eight square drives); Runner (an armoured courier wedge: a chisel prow widening into a boxy cargo body, cargo doors on top, side skirts), Bulwark (two armoured holds as sponsons, two smoothed cargo pods on the spine), Rampart (a six-shooter: six ribbed armoured cargo pylons in a cylinder round a central axle, a nose tapering down from the cylinder to a cockpit canopy, a four-engine block astern, in Varkesh orange and light plating). Ostrova (spires, halos, crescents, prongs, crystal): Glim (a spire cockpit inside a halo, a crystal cargo hold set in the halo either side, prongs holding a lens), Lumen (a central spire cockpit forward with mining lenses at its nose; four long crystal holds set in two rings crossed in an X toward the stern, each stretched from the front of the rings to the back), Delve (a great drill spire with a lens ring at its prow; four crystal ore holds held by two halos, one at their fronts and one at their backs); Drift (a slim spire with two long crystal cargo containers, one either side and almost the ship's length, held by a front and a back ring), Cairn (a pointed spire, two rings, and three crystal cargo containers set in the rings; nothing else), Monolith (a solid spire fuselage with crystal seams and a bridge, four large crystal holds set in two halos round it, three spire drives astern).
- **Scouts and bombers: all 12 approved (2 Nov 2026).** `beyond_scouts_bombers_by_faction.png`, from `tools/previews/beyond_recon.py`. Combat and recon craft, so they stay close to the fighters' proportions, with a signature per class: scouts carry sensor masts, dishes and limpet racks (advanced scouts a beacon device too); bombers carry visible torpedoes; heavy bombers have two seats in tandem and a rear turret. Halcyon: Lark (a needle with a long sensor boom), Skylark (a big radome on twin pylons), Condor (a great swept wing with four slung torpedoes), Harrier (tandem canopies, a large forward-swept wing with a torpedo pod under each side, a rear ball turret). Varkesh: streamlined but bulky smoothed-hex hulls: Jackal (a slim, sleek, flat wedge with its sensor faired into the nose, a raked mast), Wolfhound (a slim, sleek hull with sensor blisters faired into its flanks, a big dorsal radar dish), Maul (compact, the torpedo magazine faired into its belly), Warhound (compact, two seats, a turret faired into the aft spine, tail fins, torpedoes along the flanks). Ostrova: Seer (a spire behind a sensor halo with a crystal eye, one pair of swept wings), Oracle (a spire with a great flat radome, set like the Skylark's on pylons, between two rings crossed in an X), Obelisk (the Sentinel's single-seat cousin: a spire with crystal fins, four torpedo lances on a halo, two tail fins at 45 degrees either side), Sentinel (tandem seats, a gun pod on the aft fuselage, torpedo lances under crystal fins, two tail fins at 45 degrees either side).
- **Capital ships: approved (2 Nov 2026).** `beyond_capitals_by_faction.png` (at one scale) and `beyond_capitals_closeup.png` (four views each), from `tools/previews/beyond_capitals.py`. Rules from the first-pass review: capitals are not resized fighters, so there are no glass canopies and no fighter fins; each has a raised **bridge** superstructure with a lit window band, in its faction's style (Halcyon a lens pod on a pedestal with a dish, Varkesh stepped smoothed-hex tiers with a mast, Ostrova a faceted spire tower with a crystal window band). Each keeps Driftgate 1's working parts: escorts carry forward torpedo tubes, point-defence turrets (three a side), a bridge, a ventral assault bay, a shield generator and drives; carriers carry a flight deck with four landing spots, launch mouths at the bow, point-defence turrets, a bridge, a shield generator and drives. Class names are placeholders. Halcyon: Shrike (redesigned: a long layered lens hull with a dorsal superstructure spine, four torpedo tubes, faired turret sponsons, emitter nodes on pylons, a three-drive engine block), Sovereign (tail fin and stabiliser gone; the broad lens deck carrier with four engine booms (an outer pair at the flanks and an inner pair under the hull), a five-drive engine block between them, and its bridge beside the deck). Varkesh: Vanguard (cleaned up: a smooth armoured hull with armour bands, four torpedo tubes in the chisel prow, long turret pylons standing off the hull on two beams each, fore and aft, four drives), Bastille (smoothed: a slab fortress with a railed deck, turret pylons standing off the hull on two beams each, armour bands and eight drives). Ostrova: Lantern (redesigned: a long faceted three-section hull with two turret halos round it, crystal cores between them and four torpedo tubes in the prow, no prow ring), Cathedral (smoothed: an octagonal crystal-veined hull, the deck along its back, and two horizontal rings round the hull fore and aft carrying turrets and crystal holds). Third-pass changes: the escorts' shield generators moved under the hull, so nothing bubbles up from their tops; the Lantern lost its prow ring; the Cathedral's rings lie flat; the Ostrova spire bridges are lower; the Sovereign has five drives in its engine block (nine with its four booms). (The preview renderer now splits big triangles, so flight decks show cleanly in the angled views; the game draws with a depth buffer and never had that problem.)
- **Destroyers: approved (2 Nov 2026).** on the same two sheets, between each faction's escort and carrier, from `tools/previews/beyond_capitals.py`. Each is built around its main gun, in its faction's language, with point-defence turrets and a bridge. Names are placeholders. Halcyon **Peregrine**: a lens hull that splits into two prongs round a spinal rail cannon, glowing accelerator rings between the prongs, a capacitor bank along its back, faired drive nacelles, a bridge pod aft. Varkesh **Ironclad**: an armoured hull on a flared armour belt with two giant single-barrelled main guns on the centreline (the second raised on a barbette to fire over the first), the stepped bridge behind them, turrets along the belt. Ostrova **Prism**: a faceted hull carrying three long spars (two above, one below) that converge on a great crystal lens in the prow, the spinal lance, fed by an energy conduit, turrets riding the spars, a low spire bridge, a small halo round the stern.
- **Player bases: approved (2 Nov 2026).** `beyond_player_bases.png`, from `tools/previews/beyond_stations.py` (sheet: `stations_sheet.py`). In the neutral company style, each picture scaled to fit. **Lair 1** a large asteroid with one framed hangar cut into it, a hatch and a whip antenna, little else showing (it is hidden); **Lair 2** adds a second berth, a forge vent glowing in a crack, a stash of containers clamped to the rock, a dish and a radiator. **Depot 1** a hub drum with a dome, a docking arm with a lit collar, containers and a tank (storage), a beacon mast; **Depot 2** adds a production module with radiators and a hangar; **Depot 3** adds defence turrets on the dome rim, armour plates and a life-support ring. **Station core**, standard: a spine, a central hub, a habitat ring on four trusses, a docking crown with four collars, tanks, radiators, and five **hardpoints** (lit pads on truss arms) where the buildings go; asteroid: the same crown and spine coming out of a large rock with three hangars cut into it. **Buildings** (each attaches to a hardpoint): shipyard (an open gantry with portal frames, two cranes and a keel taking shape), external storage (a rack of containers and three tanks), defence platform (a hex gun deck: two heavy turrets, four point-defence turrets, a ventral turret, a mast), hangar (a half-drum hall with a lit mouth and an apron), forge (a furnace drum glowing at its mouth, stacks, radiator wings, ore hoppers), market wing (a lit concourse with three trader docking collars and a sign). **Level 5** examples show both looks with five buildings fitted.
- **Faction stations, faction depots and the freeport: approved (2 Nov 2026).** `beyond_faction_stations.png`, from `tools/previews/beyond_faction_stations.py` (sheet: `faction_stations_sheet.py`). **Halcyon** station: a great lens disc with a glass crown, a spire with a dish and emitter, three swept arms (a pinwheel from above) ending in emitter nodes, hangars in the rim, point-defence turrets on the upper surface, a stem to a lower lens pod; depot: a small lens with two swept arms, one hangar, a dish. **Varkesh**, the **Talon Citadel**: a triangular spire standing up from an armoured waist with a same-sized one hanging down, three great curved talons rising from the waist corners and curling in over the top apex and three more stretching down and curling under the bottom apex (amber-edged, heavy turrets riding them), hangar slots with floodlights in the waist faces, a heavy turret on each upper face and a pincer clamp on each lower face, lit slits, a war beacon on top and a lit tip below; depot: the same in small, with short talons up and down, one hangar, one clamp, a heavy turret. **Ostrova**, built of floating parts held by **energy bridges** (thin glowing beams with bright end nodes, an Ostrova signature): a main spire in four floating faceted sections bridged across the gaps, six great crystal spires floating in a ring and bridged to the core, a helix of crystal shards, **three free-floating halos** (the third thrown well off kilter) each bridged to the core, an inverted crystal cluster below, and **docking pods floating outside the halos as separate faceted boxes**, each bridged to the nearest halo; depot: a two-section floating pylon bridged across its gap, three crystal pillars bridged to it, **a ring floating round its middle**, a docking box floating outside the ring and bridged in. **Freeport**, a welcoming trade spire standing upright, with its own parts (no player-station pieces): a smooth capsule spine, a **glass atrium** at its heart (the bazaar) with lit floors and ribs, two **promenade rings** round it with lit window stripes, lantern lights and lit billboards, **four docking arms reaching out from the centre**, each lined with berths above and below and ending in a docking head with collars, **welcome gates** above and below ringed with lights, **two corporate towers** standing on the upper promenade, unlike each other (a round glass spire with a halo sign, a square tiered tower with a billboard), lanterns hanging under the atrium, strings of festival lights from the towers. Freeports have no depots. **Lighting** on all of them: lit windows scattered over the hull plating (lined up horizontally, a quarter of them glowing in the faction colour) and navigation beacons at their outermost points, on top of each design's own lit bands, slits and floodlights.
- **Unbound hulls: all six approved (2 Nov 2026).** `beyond_unbound.png` (four views of each, sheet: `unbound_sheet.py`), from `tools/previews/beyond_unbound.py`. The Unbound design nothing of their own: every hull is **parts of all three factions' ships welded into one** (Halcyon lens pods, swept wings and emitter nodes in light plating; Varkesh hex slabs, square drives and guns in dark plating; Ostrova faceted spires, crystals and halos), often lopsided, joined with weld seams and scrap patches, in the Unbound sand colour. Driftgate 1's four Unbound hulls and two more: **Raider** (light, scout radar: an asymmetric twin-body with an **off-centre cockpit**: a long Ostrova faceted boom to port carrying the drive and the tail, a short stolen Halcyon cockpit pod with its canopy to starboard with a Varkesh engine behind it, one large swept Varkesh wing running through both bodies to amber-edged tips with guns slung under it, a Halcyon tailplane and fin on the boom side only, an Ostrova crystal radar fin, ram spikes), **Skiff** (scout, fast, jammers: an Ostrova spire hull, a larger Halcyon radome set flush on the hull, small forward-swept Halcyon wings, Varkesh square drives strapped on, jammer rods), **Corsair** (medium, the muscle with the best jammers: a Varkesh chisel body with chin guns, a Halcyon drive section, four Halcyon wings in an X, a small Ostrova ring on the nose and a jammer halo round the tail), **Plunderer** (heavy, the hold: a Halcyon cockpit pod on a Varkesh spine, mismatched holds, a Varkesh container to port and an Ostrova crystal to starboard, a crystal-clad boom engine on a pylon on top matching the Ostrova crystal pontoon underneath, a Varkesh drive block), **Wrecker** (bomber: a Varkesh fuselage, stolen Halcyon wings, Ostrova crystal torpedoes, a faceted tail spire and halo), **Ravager** (the Unbound's destroyer-class capital: a Varkesh prow with ram spikes, a Halcyon midsection and an Ostrova stern in a turret halo welded end to end, a salvaged Halcyon rail cannon along the spine, a Varkesh giant gun and stepped bridge, a Halcyon sponson to port and a Varkesh pylon to starboard, mismatched drives). Names are placeholders.
- **Scrapheart Haven, the Unbound's main station: approved (2 Nov 2026).** `beyond_unbound_haven.png`, from `tools/previews/beyond_unbound_base.py` (sheet: `unbound_base_sheet.py`). A unique asteroid base built the Unbound way, from pieces of every other station jammed into or clamped onto one big rock, deliberately ugly: a Halcyon lens disc with its glass crown, spire, dish and a swept arm rammed tilted into the crown; a Varkesh triangular spire rammed into one flank with three talons clutching the rock and heavy turrets; Ostrova crystal spires growing out of the other flank under a floating halo, with energy bridges and a floating spire section; a broken freeport promenade ring round the base and one freeport docking arm with berths and a docking head; player-base parts (a shipyard gantry, a container stash, tanks, hangars cut into the rock as a Lair's are); weld seams, strings of festival lights between the pieces, a beacon mast and lit windows everywhere. The name is Driftgate 1's Unbound haven.
- **The Brood destroyer, the Gullet: approved (2 Nov 2026).** `beyond_brood_destroyer.png`, from `tools/previews/beyond_brood.py` (sheet: `brood_sheet.py`), in `tools/brood.py`'s grown language. It sits between the Brood's Prowler (escort) and Hive Ship (carrier). **It has no shields and carries a Maw Cannon:** it charges, then fires a beam out of its open maw that does incredible damage along its whole firing path. The model is built around that maw: a long armoured serpent whose front is a great bell of chitin opening forward, ringed with teeth and four jaw-mandibles, the charge glowing deep in its throat; three pairs of glowing charging bladders swell along the neck, veined into the maw; heavy overlapping carapace and bone arches instead of shields; dorsal spines, fins below, tail tendrils and drive vents.
- **Brood fins (decided 2 Nov 2026):** every Brood model's legs are replaced by **fins**, a flesh membrane swept back and down from the flank with a bone rib along its leading edge (fewer, larger fins than there were legs). Done in `tools/brood.py` itself, so the game's Brood models change when the model pack is next rebuilt; scythes, maw tentacles, the Hive Ship's mandibles and the Prowler's folded forelimbs stay. `beyond_brood_all.png` (sheet: `brood_all_sheet.py`) shows every Brood model with the new destroyer.
- **Constructors and drones: approved (2 Nov 2026).** `beyond_support.png`, from `tools/previews/beyond_support.py` (sheet: `support_sheet.py`). Constructors (the AI's builders): **Architect** (Halcyon: a broad lens hull with two swept fabricator arms holding a great printing lens whose beams lay down the frame, a folded depot module slung beneath, twin booms), **Foundry** (Varkesh: an armoured hull with two great crane arms ending in pincer manipulators, a girder bundle clamped along its back, stacks, a square drive block), **Loom** (Ostrova: a faceted spire with a cockpit, in a halo, three long prongs whose glowing threads weave a crystal frame between their tips, crystal girders along the spire). Drones (carried by mining hulls): **Aegis** (Halcyon: a slim lens body with a sensor slit and no cockpit, emitter vanes, a chin gun), **Ward** (Varkesh: a squat armoured hex box with amber armour bands and spine plate, twin guns and a square drive), **Halo** (Ostrova: a crystal core floating in a ring on energy bridges, a small turret riding the ring).
- **House-brand hulls and the Wraith, centuries on: approved (2 Nov 2026).** `beyond_brand.png`, from `tools/previews/beyond_brand.py` (sheet: `support_sheet.py OUT brand`). Beyond is many centuries after Driftgate 1, so the signature hulls are no longer conversions of a stock hull: each is its own design in its faction's language, built round the weapon that made its name. **Gannet** (Halcyon house-brand hauler): the hauler line's thick lens flying wing, a little narrower, (the Albatross's frame, centuries on), its outer wing bays turned into banks of missile launch cells (the barrage), freight hatches on the spine, a glass cockpit set straight into the hull, small tail plates, floodlights. **Bombard** (Varkesh house-brand miner): one huge shell cannon running the whole length of the ship down its centre, carried between two armoured side hulls joined by braces over it and disappearing astern into a broad armoured aft section; the port hull carries the cockpit, the starboard hull an ore hopper and a docked Ward Drone; glowing vents along each side hull's outer flank, a very small wing on each side hull, stacks and drives. **Vesper** (Ostrova house-brand scout): a slender faceted spire that is itself a railgun, two long crystal rails reaching forward through three accelerator halos with a glowing slug between them, two rings crossed in an X round the stern as wings with the drive pontoons on their four tips, a scout radome low on the spine. **The Wraith** (the conqueror's trophy, no faction's design): a clean faceted stealth flying wing with some depth, one faceted body with the spine ridge built into it, evenly shaded planes, thick wings joined into the body with straight swept edges, drives buried in slit vents, two heavy guns hidden in the leading edge, a faceted canopy, faint edge lights running along the wings' leading edges, in a dark trophy finish.
- **Preview renderer:** `render_beyond.py` can draw with a per-pixel depth buffer (`zbuf=True`), as the game does, which removes the sorting artefacts the painter's-algorithm previews show where parts meet; the house-brand sheet uses it.
- **Next designs:** none outstanding.
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
Hull upgrades are stats only · a blast breaks a rock's ring · AI upkeep is credits plus goods · your own brand from Depot level · Brood about 20% · Rating only goes up · a pilot at Partner standing may declare allegiance (to a player's faction at any time, no standing needed, once its founder accepts), shown on an Allegiance screen with standings between factions; swearing hands the faction all your assets, renouncing costs your standing with it, and re-swearing to an AI faction needs Partner again, and fly for that faction instead of building their own (11a) · factions become allied by trading and not fighting, tracked in a background faction status ledger (11b); all factions start Neutral; allies still hire contractors against each other; leaders with personalities drive reasoned faction events, and successors' traits come from their faction's history, so relations can swing from annihilation to friendship over a storyline; leaders fly in the galaxy with an ace escort, in ships their traits lean toward, and can be killed, which triggers a Vengeful succession; they make escort, hunt and sighting work, show on radar by name and open their best jobs where they dock (11c) · Legend reworked: levels unlock perks you pick from each galaxy with a start-point budget, level 10's Station stays, and Conqueror's spoils go in full to the winning faction and half to its allies (10a) · a choice of three starting freeports · faction careers become job bonuses and the signature hulls survive · scouting returns as intel, with scout hulls (Rating 2 and 4, not a starter) the only hulls for beacon devices and limpets · a beacon flip earns a fee and standing · your brand's trait is a net-zero point system · Unbound designs are pirates' only · the nine fighter designs (Swift, Kite, Osprey; Fang, Talon, Halberd; Mote, Wisp, Vigil) are approved · the 18 miner and hauler designs are approved · the 12 scout and bomber designs are approved · the capital ships (escort, destroyer, carrier per faction) are approved; the destroyer sits between escort and carrier, unlocks at station level 4 and its main gun fires a charged shot with shields down while charging · the player bases (Lair, Depot, Station in both looks, the six buildings) are approved · **allies and the win:** allies' systems do **not** count together toward the 20 systems that win, each faction wins on its own; when a faction starts the 10-minute timer, **every alliance with that faction breaks, with no penalty** to anyone's relations, and the others unite against it as before · the Brood is left as Driftgate 1 has it for now, except for a new **destroyer** with **no shields and a Maw Cannon** that charges, then fires a beam doing incredible damage along its whole firing path · **Unbound designs are kitbashed:** each Unbound hull is assembled from parts of all three factions' designs welded into a single hull · the six Unbound hulls (Raider, Skiff, Corsair, Plunderer, Wrecker, Ravager) are approved · the Unbound's main station is Scrapheart Haven, a unique asteroid base kitbashed from pieces of every other station (approved) · the faction stations and depots (Halcyon lens, Varkesh Talon Citadel, Ostrova floating crystal spires with energy bridges) and the upright freeport trade spire are approved · Station levels come from external buildings · freeport yards roll a random set of faction designs; house-brand hulls only at their faction's station · AI wages go to the Compact · 20 systems held for 10 minutes wins (decided 2 Nov 2026; was two-thirds), with no deadline, and the others unite once the timer starts · you choose one external building per station level · asteroid landing needs an installed landing kit, not offered automatically · flares stay on energy, drones restock at dock · only factions (and the Unbound and Brood) design hulls; freeports build faction designs · Lair 2 levels, Depot 3, Station 5 · makers' names kept for now · declaring needs only a Station · losing your last Station drops you back to a company · asteroid or standard station look.

### Open questions
1. **Lair, Depot, Station costs.** All numbers are guesses to tune.
4. ~~Company name and colour~~ (decided 2 Nov 2026): you **name your company and pick its colour when you build your first Depot**, when your brand begins. The colour can't be close to any power's: not near Halcyon teal, Varkesh orange, Ostrova violet, Brood green, or the Unbound's and the Compact's sand.
3. **Names:** placeholders that follow each power's naming conventions are fine as they are (decided 2 Nov 2026); no naming pass needed.
2. ~~Allies and the win~~ (decided 2 Nov 2026, see below).

### Proposed build order (once the design is agreed)
1. **Cut the faction tie:** start at a chosen freeport with three equipped starters; standing with every power; docking and hostility from standing; pay from the issuer; faction job bonuses.
2. **Faction relations and leaders** (and the Dread Pirate, 12c, once the Unbound's Ravager and haven are in): the faction status ledger, all factions starting Neutral, leaders with traits, the event table and successions, the chronicle; war checks that galaxies still go to war. (It comes this early because the Neutral start only works once leaders can start wars.)
3. **Weapon slots and weapons** (and the landing kit as a utility part): slot counts per hull; machine gun with ammunition, laser on reactor energy, missile and torpedo payload; mining laser with rings and charge launchers in mining hulls' weapon slots.
4. **Making things:** ore → components → parts → upgraded parts; grades replace Mk.
5. **Faction jobs screen,** with Claim Beacons for any faction and claim jobs, and intel jobs: beacon devices, capital pings, limpets, and discoveries out beyond the gates.
6. **Unique hull designs, first wave:** each faction's fighters, with their own models and stats, duel-balanced; freeport yards build them.
7. **Makers:** the corporations, their works and stock; product lines replace variants; AI fleets fitted from their makers.
7b. **Smuggling:** contraband tags (stolen, embargo, cash-only), hidden cargo containers, patrol scans with bribe, surrender or run, Riftstone and Rift Shards.
8. **Progression:** Contractor Rating gates hulls and grades; hull upgrades; drop Unbound mode.
9. **Lairs and the Holdings screen.**
10. **Depots:** markets, hiring and building AI with upkeep; the Economy and Job creation screens.
11. **Stations and their buildings;** capital ships built at your stations.
12. **Strategic map** with sector zoom and orders.
12b. **The new galaxy map** (12b): deep space at the centre with the Bloom and the Wrack, freeports in pockets reached only through deep space, the open-space ring; Scrapheart docking with the rum bar and market; the Unbound's jammers, hooks and bigger holds; retuned with the war check.
13. **Declaring a faction;** player factions in the ledger and leaders' proposals to founders; slower war pacing; a stronger Brood (about 20%); war checks for the new balance.
14. **Legend rework and Conqueror's spoils, multiplayer rivalries, training rewrite.**

**Parked until the stages are done (2 Nov 2026): a graphical market.** The market tab as tiles with item art (ore rocks, part glyphs), stock meters and demand marks, your hold as a coloured bar, and a detail panel for the picked item: its price here against the galaxy from your scans, its recent price history, a quantity slider, and the best places to sell. First sketch: `tools/previews/market_mockup.html`. Not agreed yet; to be designed with the user after stage 14.

---

## Build spec and as-built notes (stages 1 and 2 specified 2 Nov 2026; stages 1 to 14 built 2 Nov 2026, each with its "as built" section below)
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

**War check:** stage 1 doesn't change how the powers fight each other. **Beyond's balance targets are not set yet** (2 Nov 2026): the faction and Brood shares get decided later, so war checks are not run against Driftgate 1's percentages for now.

### Stage 1: as built (2 Nov 2026)
- **New file `02b_standing.js`** holds the standing model: `P.stand` (Halcyon, Varkesh, Ostrova and the Compact, −100..100), `P.sworn` (null for a contractor), `P.home` (the freeport), `P.job` (`{by, kind, id}`), and the helpers `standOf`, `standAdd`, `standBand`/`standName`, `pilotHostile`, `tradeOK`, `escortOK`, `intelSide`, `jobIssuers`, `bountyPayer`, `weSide`, `containPayer`, `helpFac`, `pilotHome`, `standHit`, `standWork`, `standDrift`. Tunables in `STAND`.
- **`P.faction` is now the design faction only;** every allegiance read across the 16 files uses `P.sworn` (about 250 sites). `sideNorm('player')` is the sworn faction, or the Compact for a contractor. Save version 3 (older saves are refused).
- **Hostility:** `hostile()` sends the unsworn player through `pilotHostile`: the Brood and the Unbound always, a power below −50, or for 60 s after you attacked one of its ships (aggro); the Compact never. It's a constant-time read. **Guests** fly as side `neutral` (the Compact) when unsworn, and AI targeting asks `hostE(side, ship)` per pilot (about 40 targeting sites), so each guest is judged by their own standing.
- **You can fire on anyone:** a contractor's shots hit any power's ship (`hostAt`), except ships escorting or hired by them. Damage costs standing (`STAND.hitK`, about −8 for a Light Fighter killed) and starts the 60 s aggro; stations and outposts cost a quarter as much per point.
- **Docking** (`canDock`, guests' `hDock`) and vault access follow `tradeOK`: a contractor docks where it stands −10 or better (freeports by Compact standing); sworn pilots as in Driftgate 1.
- **Pay:** `payKill` and ace kills are paid by `bountyPayer`: a sworn pilot's faction; a contractor's job issuer if at war with the victim; else the power at war with the victim that the pilot stands best with (not Hostile); else nobody (the Compact's ships carry no bounty). War effort goes to the job's issuer (`weSide`). Seeder spotting, Brood node burns and anomaly scans are paid by `containPayer` (the best-standing power).
- **Jobs by issuer:** every power now posts delivery contracts (up to three open each, a new one every 20–35 s). A contractor sees the station owner's contracts at Neutral or better, and convoy raids and escorts for the station owner (at a freeport, for every power it stands Neutral or better with). Selecting a job records `P.job` with its issuer (guests send it to the host). **Bonuses keyed by the issuer:** Halcyon +20% on the delivery contracts it issues, Varkesh +20% on its Aurorite jobs, Ostrova +40% on intel and escort pay it issues. Signature hulls need Partner standing with the station's owner (and, until stage 6, flying that faction's design line).
- **Standing moves:** deliveries (+3 and +1 per 1,500 cr, double for blockade runs), escorts (+4 and +0.5 a jump), kills paid by a power (up to +3); a quarter as much lost with the issuer's enemies; damage as above; drift toward 0 at 0.01 a second.
- **Start:** the start screen offers the three freeports and three roles (no Scouting); `START_HULLS` drops the scout. You launch unsworn, docked at the freeport, Neutral with everyone; each freeport's starters use the nearest power's design line until stage 6 (Mirrorwater Halcyon, Coldwater Drift Ostrova, Ember Wake Varkesh). Death respawns you at your freeport. Training still starts sworn to a faction. The Unbound card stays until stage 8.
- **What a contractor doesn't get yet:** faction-only services (command wings and orders, patronage, hired wingmen, campaign moves, beacon flips and limpets, convoy calls, vault shipping, capital yards) need a sworn pilot, as before; they come back for contractors with later stages. The HUD orders card shows "Contract work" with the selected job's issuer and your standing.
- **Tests:** `?sworn=halcyon` on the page URL starts a pilot sworn to that faction (dock, jobs, ship, limpet, contacts and hull_tags use it). New: `standing.py` (in the quick suite) and `mp_contractor.py`. The fast simulator takes `PPORT=mw|cw|ew` for a contractor start, and `FS_DIR` for its scratch folder.

### Stage 2: faction relations and leaders
**New state** (on `S`, so saved and sent to guests already): `S.rel` (relation per pair), `S.relLog` (recent entries, capped), `S.leaders` (per power: name, traits, ship, escort, grudges, cooldowns), `S.facEv` (cooldowns per pair), `S.chron` (the chronicle). New file `src/js/16g_leaders.js` after `16f_factions.js`.

**Steps:**
1. **The ledger, read-only.** `relAdd`, `relBand`, the log, and an Allegiance tab at docks showing standings, relations between factions and the chronicle. No effect on play.
2. **Feed it, still at permanent war.** Hooks: trade (`traderArrive`, `fpImport`), ships destroyed (the death path before `payKill`), captures and razes (`capture`, `captureDepot`, `razeStation`), sieges (`resolveSiege`), raids (`raidFight`), beacon flips (`beaconFlip`). Run the fast simulator and record how relations move, to size the numbers.
3. **Leaders in shadow mode.** Leaders with traits, the event table, triggers, cooldowns and successions, logged as what they *would* do ("would declare war") without acting.
4. **Switch on.** All factions start Neutral. `hostile()` between powers follows the ledger (Hostile and War fight); new `warWith()` for sieges and campaigns; `planOffensive` also stops targeting outposts held by a power it isn't at war with; `campTargets`, `resolveAbstract`, `resolveSiege` use `warWith`. The Containment Accord stays as the "containment front" and still overrides the ledger. Traders may use Friendly factions' markets, which is how trade builds alliances.
5. **Pilots fly like their leader:** trait-driven AI behaviour (the table in 11c): aggression, pursuit, break-off thresholds, staying when a squadmate dies (Vengeful), convoy-first guarding (Mercantile), and all powers answering distress calls in Brood space; shifted on succession; war checks.
6. **Leaders as ships.** Built on Driftgate 1's ace system (an ace with a wing of escorts, a kill reported by `aceKilled`), plus an off-screen mover so a leader keeps travelling when nobody is watching; a killed leader triggers a succession shaped by history. Leaders never go into the aces record that carries between galaxies.
7. **Leader jobs** (escort a leader, hunt one, sell a sighting) and proxy work can wait for the Faction jobs screen (stage 5).

**The main risk.** If everyone starts Neutral, nobody shoots, nothing goes negative, and no war ever starts. The first negatives must come from AI scouts flipping beacons, building in contested systems, and leader events (border dispute, then embargo, then war). So leaders are built and tuned (steps 3 and 5) before and alongside the switch (step 4).

**War check** (four sides, 480 games each): nearly every galaxy has its first war by about 30 minutes; the Brood wins about 20%; the three powers share the rest evenly; and games that end on the deadline don't rise (the 2-hour deadline stays until the pacing work in stage 13, so a late first war would push wins onto it). The simulator reports when the first war starts, minutes each pair spends at war, alliances, betrayals, leader deaths and successions. New tests: relations (ledger arithmetic and bands) and leaders (an event fires on its trigger, the chronicle records it, a killed leader is succeeded).

### Stage 2: as built (2 Nov 2026)
- **New file `16g_leaders.js`** (after `16f_factions.js`) holds relations and leaders; tunables in `REL`.
- **The ledger.** `S.rel` is a symmetric relation per pair of powers, −100..100, starting at 0 (Neutral). Bands: War below −50 (shown as War only once declared, Hostile until then), Hostile −50..−10, Neutral −10..25, Friendly 25..60, Allied above 60. `S.pair['a|b']` holds the pair's state: declared war, alliance, trade pact, embargo, cooldown, open demand, betrayal and when the war started. `relAdd` moves it and logs the reason; `S.chron` is the chronicle shown at docks.
- **What moves it:** ships shot down (−0.8, capitals −5), beacon flips (−3), strikes planned (−4), captures (−12), depots taken (−18), stations razed (−24), raids (−3); pact trade warms it; a common enemy (a war with the same third power) warms it +0.3 a tick; it drifts back toward 0 slowly.
- **Hostility between powers** follows the ledger: hostile below −10 or at war, never when allied; the Containment Accord and the coalition against a leader still override it. **`warWith`** (declared war, or the coalition against the leader) gates sieges, campaigns, `campTargets`, `resolveAbstract` and `resolveSiege` (through `fightsAt`); `planOffensive` skips outposts held by a power it isn't at war with, and a reprisal focus weights one target ×3.
- **Leaders.** Each power has a leader with two of 14 traits, a title and a line of succession (Halcyon: Chair of the Merchant Houses, Mercantile and Cautious; Varkesh: Marshal, Ambitious and Vengeful; Ostrova: First Archivist, Scheming and Patient). Every strategic tick a leader may act, weighted by traits, on triggers and cooldowns: border dispute (a demand with a deadline), embargo, trade pact, aid, alliance, reprisal, declaration of war, ceasefire, betrayal. Grudges are kept per power. **Successions** follow a leader's death, a core falling, or a long losing war; the successor's traits are shaped by how the last one fell, and a killed leader's successor holds a grudge against the killer.
- **Pilots fly like their leader:** detection range, pursuit, Ruthless finishing, Zealous Brood focus, Honourable sparing, Cautious and Mercantile break-off; every power answers distress calls in Brood space.
- **Leaders as ships:** a leader flies as an ace with a wing, travels between sectors off-screen, and fights with a boost; shooting one down pays a 6,000 cr bounty (from `bountyPayer`), drops relations with its power by 40 and starts a succession. Leaders are never kept in the aces record.
- **The Allegiance tab** at every dock (not in training): your standing with each power, the relations table, the leaders and their traits, and the chronicle.
- **Not yet:** leader jobs and proxy work (stage 5), the Dread Pirate (once the Ravager and haven are in, stage 12b), player factions in the ledger (stage 13).
- **First fast-simulator run** (60 games, 2.2 h, Mirrorwater start): the first war at a median of 35 minutes, 3 of 60 games with no war; about 3.4 wars and 2.1 ceasefires a game; alliances and successions rare. Balance targets are still undecided, so these numbers are recorded, not tuned to.
- **Tests:** `relations.py` (in the quick suite): bands and hostility, a war declared on its trigger and a ceasefire, a border demand settled, a succession, the Allegiance tab, a leader spawned, shot down and succeeded, an hour of strategy. The fast simulator reports `relStats()`.

### Stage 3: as built (2 Nov 2026)
- **New file `16h_loadout.js`.** A pilot's ship has weapon and utility slots: `P.fit = {cls, w: [...], u: [...]}`, reset to the hull's default fit when the hull changes. Tunables in `LOAD`; slot counts and default fits in `HULL_SLOTS`.
- **Slot counts** (the design's starting proposal): Light Fighter 3 weapon + 1 utility; Medium Fighter 4 + 1; Heavy Fighter 5 + 2; Bomber 3 + 1 (the first is its torpedo launcher); Heavy Bomber 4 + 2; Light, Medium and Heavy Miner 2 + 1, 3 + 1, 3 + 2; haulers 1 + 2, 2 + 2, 2 + 2; Scout 2 + 2, Advanced Scout 3 + 2. Mining tools fit only mining hulls, torpedoes only bombers.
- **Weapons:**
  - The **machine gun** (key 1) spends a round a shot, 600 rounds per gun, and only 30% of a shot's old energy.
  - The **laser** (key 2) is limited by the reactor as before.
  - **Missile and torpedo launchers:** the magazine is sized per launcher and never reloads in flight. A pilot's missiles hit twice as hard.
  - Each extra gun or laser of a kind adds 20% damage. An unfitted weapon refuses with a message.
- **Payload is rearmed at a dock.** Docking rearms automatically with whatever the credits cover, and there is a Rearm button in the Ship tab. It is paid to the station owner's treasury (credits stay exact): 0.15 cr a round, 25 a missile, 90 a torpedo, 6 a charge. At your own bases the supplies are bought from the Compact (paid to the freeport treasury).
- **Mining:**
  - **Charge launcher:** blast mining as in Driftgate 1. The charges are payload; extra launchers add half a magazine each.
  - **Mining laser:** every rock has a **ring**, a seam fixed by its seed and drawn on the targeted rock when scanned or close. Hold F with the beam on the ring to cut ore steadily into the hold: 0.17, 0.25 and 0.33 t a second for the Light, Medium and Heavy Miner, +20% per drill Mk. It draws 8 energy a second. Off the ring it only sparks.
  - **A blast breaks a rock's ring for good,** so each rock is worked one way.
  - Key 7 switches the mining tool when both are fitted. A guest's laser is cut by the host from the rock id in its input.
- **Utility parts:**
  - **Landing kit:** without one, E never offers to land on a rock.
  - **Cargo module:** +20% hold.
  - **Scanner:** rock scans reach every rock within 1.5 km and last 40 s.
- **Refits** were free in stage 3. Stage 4 made parts real items (below).
- **The HUD gun readout** shows rounds left, and the mining tool on a mining hull.
- **Unchanged for now:**
  - AI ships fly as before.
  - Swarm pods stay a hull feature and still reload on their own.
  - Flares and drones are as in Driftgate 1.
  - Training and the Unbound mode keep Driftgate 1's weapons.
- **Tests:** `loadout.py` (in the quick suite). It covers default fits, slot rules, rounds, refusals, no reload in flight, missile damage, rearm payments, the landing kit, cargo modules, cutting on and off the ring with the ledger exact, a blast breaking the ring, and the Loadout section. `limpet.py` now sets Halcyon and Varkesh at war, since the powers start Neutral.

### Stage 4: as built (2 Nov 2026)
- **Grades replace Mk.** Ship systems (drive, reactor, shield emitter, weapons, armour, blast rig, cargo hold, payload bay) go from grade 1 to **grade 5** (`MK_TOP` 5). Each grade above 1 takes that grade's components (the old Mk recipes; grades 4 and 5 use Flux Coils, Crystal Lattices and Resonance Cores), and **grades 3 to 5 also need a Calibration Matrix**. Grade 3 has the old Mk III strength; grades 4 and 5 add two more steps (combat curve 0.48 and 0.6). AI ships stay at grades 1 to 3. Every "Mk" in the interface reads "grade".
- **Parts are items.** The nine slot parts (machine gun, laser, missile launcher, torpedo launcher, mining laser, charge launcher, landing kit, cargo module, scanner) are items with mass, built from components at any workshop (the Fabricate tab), traded on markets and kept in the hold or vault:

  | Part | Recipe |
  |---|---|
  | Machine gun | 2 Alloy Plate, 1 Conduit |
  | Laser | 2 Conduit, 1 Flux Coil |
  | Missile launcher | 2 Alloy Plate, 2 Conduit |
  | Torpedo launcher | 3 Alloy Plate, 1 Flux Coil |
  | Mining laser | 1 Alloy Plate, 1 Conduit, 1 Flux Coil |
  | Charge launcher | 1 Alloy Plate, 2 Conduit |
  | Landing kit | 2 Alloy Plate |
  | Cargo module | 4 Alloy Plate |
  | Scanner | 1 Conduit, 1 Flux Coil |

- **Fitting:**
  - The Loadout section fits a part from your hold or storage into a slot. If the market has one and you have none, it buys one.
  - **Take out** puts a part in storage.
  - A part that comes out of a slot goes to storage together with the components of its upgrades, so nothing is lost or made.
- **Upgrading a fitted part:** feed the next grade's components into it in place (with an 8% workshop fee at a power's or a freeport's dock). Each grade above 1 adds:
  - guns and lasers: +10% damage
  - machine gun: +25% rounds
  - missile, torpedo and charge launchers: one more missile, torpedo or charge each
  - mining laser: +15% cutting rate
  - cargo module: +5% hold
  - scanner: +20% reach
  - Landing kits have one grade.
- **A new hull** takes your fitted parts across into the slots that take them, in order. What doesn't fit goes to your vault, and empty slots stay empty until you fit something. Fitted parts survive the ship's destruction, like systems do.
- **The ledger counts fitted parts** with your ship. A pilot's first fit and the stations' first stock of parts are made with the galaxy, before its baseline is taken: freeports stock 3 of every part, and the powers' core stations 2 of each combat and utility part. Makers take over supply in stage 7.
- **Payload stays bought by the lot** when rearming (credits only, as in stage 3). Building payload from components needs fired payload to go back into debris, so it waits for the makers.
- **Not yet:**
  - Your own brand and its trait points (with Depots, stage 10).
  - Maker parts (stage 7).
  - Systems as removable parts: drive, reactor, shield and armour stay upgraded in place under Ship → Systems.
- **Tests:** `loadout.py` also covers the part items, fitting from storage, moving parts to a new hull, a grade upgrade, and the ledger after each step.

### Stage 5: as built (2 Nov 2026)
- **New file `16i_intel.js`.** Tunables are in `FB`.
- **Claim Beacons for any power.** Each power has its own beacon item (`bc_halcyon`, `bc_varkesh`, `bc_ostrova`, same recipe and mass as Driftgate 1's).
  - **Where they're sold:** a power's station sells its own power's beacon; a freeport sells all three. They are bought in the market tab's Claim Beacons section for the usual price, built from the station's plate and conduit, and paid to the seller's treasury.
  - **How a claim works:** a beacon claims for the power it was bought for, whoever carries it. Hold it in an unclaimed or breached outpost's ring in a fighter or bomber.
  - **Pay and standing:** the claiming power pays a 400 cr fee from its treasury, and your standing with it rises by 6. The power that held the outpost loses 6. The beacon's materials go into the outpost's fortifications, as before.
  - **Sworn pilots** still have Driftgate 1's own-faction beacon at their faction's stations.
- **Claim jobs.** Every power posts up to three: outposts within four jumps that are unclaimed, or held by a power it is at war with (or the Unbound), and not under a station's lock. They pay 1,400 cr for an unclaimed outpost and 2,600 cr for a taken one, on top of the fee, when the claim is made with that power's beacon while the job is selected. A job's row offers that power's beacon when the dock sells it.
- **Intel work for a power:**
  - A contractor's scouting goes to one power, chosen in the Jobs tab's "Intel work for" bar (Neutral standing or better). A selected intel job's issuer overrides it. A sworn pilot's always goes to its faction.
  - **Contractors can now flip beacons and plant limpets** in scouts for that power, paid by it: +3 standing per flip (−3 with the power the beacon was taken from) and +3 per limpet.
  - **Anomaly scans** are paid by that power.
  - **Intel jobs listed for contractors:** the powers' beacon missions, and limpets on enemy capital ships within three jumps (paid if the ship is destroyed with the limpet on).
- **Discoveries out beyond the gates.** Anomalies in quiet space now appear 700 to 1,800 m beyond the system's outermost gate. Any hull with a **scanner** fitted can see and scan them, not only scouts.
- **Not yet:**
  - Leader jobs and proxy work (in the faction jobs screen of later stages).
  - Comets and derelicts sold as intel to the Compact.
  - The scout hulls' beacon devices and limpet racks as fitted parts. Scouts still flip beacons and carry one limpet as in Driftgate 1, until the scout rework with Rating in stage 8.
- **Tests:** `intel.py` (in the quick suite). It covers beacons sold by power, buying one, the market section, claim jobs listed, a claim's pay and standing, a claim in the ring in flight, intel routing, a contractor's beacon flip and limpet, scanners seeing anomalies, anomalies placed beyond the gates, and the intel bar, with the ledger checked throughout.

### Stage 6: as built (2 Nov 2026), first wave: the fighters
- **New file `16j_designs.js`.**
- **Models:** the nine approved fighter designs are in the model pack as `dz_swift`, `dz_kite`, `dz_osprey`, `dz_fang`, `dz_talon`, `dz_halberd`, `dz_mote`, `dz_wisp` and `dz_vigil`. `tools/build_models.py` packs them straight from `tools/previews/beyond_hulls.py`. `shipMesh` draws a power's design for its fighters, with the faction palette, so AI wings fly their own power's shapes.
- **Stats:** a design replaces the faction's flat ±12% trait for its class, with multipliers on hull, shield, reactor capacity and recharge, top speed, thrust, turn and size (`DESIGN`):

  | Power | Light | Medium | Heavy |
  |---|---|---|---|
  | Halcyon | **Swift** (`dz_swift`): thin hull, strong shields, quick | **Kite** (`dz_kite`): well shielded, lightly built | **Osprey** (`dz_osprey`): shield-heavy, and a scanner in a second utility slot |
  | Varkesh | **Fang** (`dz_fang`): heavy armour, slower, a hungrier reactor, a fourth weapon slot | **Talon** (`dz_talon`): armoured, a hungry reactor | **Halberd** (`dz_halberd`): a thick-armoured brawler, slow to turn, six weapon slots |
  | Ostrova | **Mote** (`dz_mote`): a deep reactor, 20% faster locks, weaker shields | **Wisp** (`dz_wisp`): agile, a deep reactor, faster locks | **Vigil** (`dz_vigil`): a deep reactor, faster locks |

  Classes without a design yet (miners, haulers, bombers, scouts, capitals) keep the shared model and the trait.
- **Duel-balanced:** every pair of designs within a class was run through mirror duels (120 each, grade 1, AI against AI). Every result is between 45% and 55%, except the Swift against the Fang (55–62% over three runs) and the Halberd against the Vigil (54–59%), all within the 60% rule.
- **Yards:**
  - **Every freeport now has a yard.** Its fighter designs are rolled for each freeport when the galaxy is made (`S.yardRoll`). A power's core yard builds its own power's designs.
  - The hull cards show the design's name, and "· Halcyon design" (or Varkesh, or Ostrova) when it isn't your current line.
  - **Buying a fighter takes the yard's design.** Your design line (`P.faction`) becomes that power's, and your fitted parts move into the new design's slots.
- **Tests:**
  - `designs.py` (in the quick suite) covers the models in use, the stats by design, a class without a design keeping the trait, freeport yard rolls, buying a design at a freeport, the Fang's slots, the ship tab's design label and an AI ship's design, with the ledger checked throughout.
  - The duel harness is `tools/duel_designs.py`.

### Stage 7: as built (2 Nov 2026)
- **New file `16k_makers.js`.** The twelve makers in `MAKERS` (names still placeholders), each with its home station and its products. Every product is the slot part with the maker's trait (`mp_<maker>_<part>` items, same recipe and mass as the standard part):

  | Maker | Home | Products and trait |
  |---|---|---|
  | Teal & Corvane Yards | Halcyon core | cargo module: +6% hold, −1% top speed |
  | Brightline Emitters | Halcyon core | laser: +10% damage, +10% energy draw |
  | Hold Foundry | Varkesh core | charge launcher: +1 charge, −1% top speed |
  | Marchgun Ordnance | Varkesh core | machine gun: +12% damage, −15% rounds; missile launcher: +1 missile, +10% lock time |
  | Spirewright | Ostrova core | scanner: +25% reach; mining laser: +10% cutting rate, +15% energy draw |
  | Archive Dynamics | Ostrova core | laser: −15% energy draw, −4% damage |
  | Mirrorwater Arms | Mirrorwater | machine gun (+10% rounds), laser, missile and torpedo launchers: standard, sold to anyone |
  | Quicksilver Hullworks | Mirrorwater | cargo module (+3% hold), landing kit |
  | Coldwater Refit | Coldwater Drift | machine gun and laser (−5% damage), missile launcher; upgrades to grade 3 only |
  | Coldwater Prospecting | Coldwater Drift | mining laser (+12% rate), charge launcher (+1 charge), scanner (+10% reach) |
  | Ember Wake Drives | Ember Wake | cargo module: +8% hold, −2% top speed |
  | Wakefire Munitions | Ember Wake | missile and torpedo launchers: +1 per launcher |

- **The works are real factories.** Every 90 s each maker whose home station is still held by its home power (or is still a freeport) builds one of its products from that station's market components, up to 4 of each on sale. The ledger stays exact, since components become parts. Each maker starts with 2 of each product, made with the galaxy.
- **A maker's part keeps its maker** when fitted (`P.fit.wi` / `ui`), upgraded, taken out or moved to a new hull. A trait applies to the slots of its kind, averaged; magazine and charge bonuses add per launcher. The Loadout offers makers' parts on hand or on sale at the dock, with the trait in the tooltip. The market tab lists the makers whose works are at that station.
- **Not yet:**
  - **Product lines replacing Driftgate 1's variants.** The Systems variants stay as they are.
  - **AI fleets fitted from their makers' stock.** AI ships still fly without slots, so war doesn't drain the makers yet.
  - Makers of drives, reactors and shields (Archive Dynamics and Ember Wake Drives make only the slot parts above), which wait for systems becoming removable parts.
- **Tests:** `makers.py` (in the quick suite). It covers the makers and their homes, product names and traits, the first stock, the works building from components with the ledger exact, Marchgun's damage and rounds, Wakefire's magazine, Coldwater Refit's grade cap, makers kept through a hull change, the market's works list, the Loadout offering makers' parts, and half an hour of works.

### Stage 7b: as built (2 Nov 2026)
- **New file `16l_smuggling.js`.** Tunables are in `SM`.
- **Contraband** is a mark on real goods, never a new good, so the ledger is unchanged:
  - **Stolen:** crates spilled by a power's ships or convoys carry its mark. Scooping them tags the goods (`P.stol[item][power]`), and the tags shrink as the goods leave your hold and vault.
  - **Black-market run goods:** contraband for the power whose space they are run into.
  - **Cash-only contraband:** Ghost relics, which anomaly caches now hold (made from Xenocrystal in the recycling pools), and Riftstone and Rift Shards, which are legal only in Ostrova space.
  - A power's own market refuses goods stolen from it.
- **Heat** per power (`P.heat`): Cool, Warm, Hot or Burning. It is raised by being caught, a refused bribe, running, and scooping a power's cargo, and it cools at 0.05 a second. The Allegiance tab shows it as words.
- **Customs:**
  - **Who scans, and how often:** a power's patrols, escorts, pickets and frigates within 900 m scan contractors in its space (a sector it holds, its home, or one with its station). A check comes about every 3 s; its chance rises with heat, low standing, and being within 3 km of a station.
  - **The scan:** it takes 5 s and you are warned.
  - **The hidden cargo container** (a new utility part: 2 Alloy Plate and 1 Conduit) keeps 4 t of contraband out of a scan (+4 t a grade), the most valuable first. The patrol's grade, from its power's forges, against the container's grade decides how often it is found anyway.
- **When contraband is found,** a box offers three answers:
  - **Bribe:** half the goods' value to the power's treasury. It is likelier at better standing, never works on a Vengeful leader's patrols, and leaves half the heat. A refused bribe adds heat, and you choose again.
  - **Surrender:** the goods go into the power's stores and you pay a 15% fine, −3 standing and the heat.
  - **Run:** double heat +40, and the power's ships treat you as hostile until your heat with it drops below Hot.
  - **No answer in 15 s** is a surrender.
  - **Guests** answer through the host. Their scans run on the host.
- **Riftstone:** the two richest Xenocrystal rocks in each deep and quiet system are Riftstone, moved out beyond the gate ring. Its Xenocrystal comes out as Riftstone (1 t of Xenocrystal each).
  - **Dangers:** it throws rift discharges every few seconds that hurt a ship within 260 m, its mining-laser ring flickers out, and a blast on it sets off a chain reaction that damages ships within 300 m.
  - **Rift Shards** (3 Riftstone at a workshop) are a valuable cash-only good for now.
- **Black-market runs.** Fixers at the freeports post runs: carry goods from the freeport's stock into a power's station within five jumps, rated by the heat they'd bring if caught.
  - **Light:** +25%.
  - **Heavy:** +50% (the destination power has an embargo running).
  - **Severe:** +75% (Heavy and into its core).
  - Delivery is paid by the freeport on docking at the destination, and the goods go into that station's market.
- **Not yet:**
  - The Black market tab on the Company screen, assigning runs to AI pilots, and contacts at the powers' stations (stage 10 and later).
  - Embargo contraband by origin.
  - Pirate gear (with the Unbound rework, stage 12b).
  - Lairs laundering goods and cooling heat (stage 9).
  - The Rift Shard as a wild-card component.
- **Tests:** `smuggling.py` (in the quick suite). It covers stolen tags, contraband by power, heat words, a surrender, a bribe, a run and its hostility, cooling, the hidden container, Riftstone placement and cutting, and a black-market run taken and delivered, with the ledger checked throughout.

### Stage 8: as built (2 Nov 2026)
- **New file `16m_rating.js`.** **Contractor Rating 1–10** per galaxy, kept as Rating points in `P.rp`.
  - **Points come from:** 20 points per standing point earned through work for a power (deliveries, escorts, kills paid by a power, claims, beacon flips, limpets: everything that goes through `standWork`), 60 per anomaly scan and 80 per black-market run delivered.
  - **Thresholds:** 150, 350, 600, 950, 1,400, 1,950, 2,600, 3,400 and 4,300 points for Ratings 2 to 10. A delivery is worth roughly 60–120 points.
  - **Rating never falls.** A level-up is announced with what it opens.
- **Hulls by Rating** (contractors; sworn pilots and training are not gated): Light Fighter, Light Miner and Light Hauler at 1; Medium Fighter, Medium Miner, Medium Hauler and Scout at 2; Heavy Fighter, Bomber and Advanced Scout at 4; Heavy Miner and Heavy Hauler at 5; Heavy Bomber at 6. Yards refuse a hull above your Rating, and the hull cards say what it needs. House-brand hulls still need Partner standing.
- **Grades by Rating:** grade 2 at Rating 2, 3 at 4, 4 at 6, 5 at 8, for both slot parts and ship systems. A maker's grade 4 and 5 parts also need Trusted standing with its power.
- **Unbound mode dropped:** the Unbound card is gone from the start screen, so every new galaxy is a contractors' galaxy (`S.unb` is never set). The old Unbound-mode code stays in the files, unused, until the Unbound rework in stage 12b.
- **The Allegiance tab** shows your Rating, your points and what each level opens.
- **Not yet:**
  - Hull upgrades.
  - Capital ships by station level (stage 11).
  - Legend's rework (stage 14).
- **Tests:** `rating.py` (in the quick suite). It covers the start screen cards, starting at Rating 1, a hull refused at Rating 1, work raising the Rating, the hull allowed at Rating 2, the grade caps, a part upgrade and a system upgrade capped, Rating not falling with standing, and the Allegiance tab. `designs.py` and `loadout.py` now give their pilot a high Rating first.

### Stage 9: as built (2 Nov 2026)
- **New file `16n_holdings.js`.** It builds on Driftgate 1's Unbound Lair (docking into the rock, the stash, repairs), now for contractors.
- **Building a Lair:**
  - **Materials:** a Depot Frame and 6 Alloy Plate in your hold (lighter than the proposal's 20 plate, so a Medium Hauler can carry it).
  - **Where:** within 700 m of a large asteroid (50 t of ore or more, not Riftstone) in any system with no station.
  - **How:** the comms build order or the Holdings tab. The materials become the Lair's fortifications, and it is ready after 60 s.
  - **Limits:** up to four per pilot, and one per pilot per system, so several pilots can each hide one in the same system.
- **Level 1:**
  - a 200 t stash, repairs and rearming
  - **lying low:** heat cools three times as fast while docked there
  - **laundering:** goods stored in the stash lose their stolen tag
- **Level 2** (a Depot Frame, 10 Alloy Plate and 4 Flux Coils, while docked there): a 400 t stash, and a workshop and forge with no fee.
- **Hidden:** a Lair is unseen until a scout of a power that is hostile to its owner comes within 5 km. From then on, that power's ships wear it down whenever they pass within 2.5 km; it has no guns. A destroyed Lair's stash drifts as salvage and its fortifications become debris.
- **Rearming is never free:** at your own bases, the supplies are bought from the Compact (paid to the freeport treasury).
- **The Company screen:** key 0, or the Company button on the HUD. It opens anywhere, over the running game, and closes with Esc or 0. For now it has two tabs:
  - **Allegiance:** Rating, standing, heat, relations and leaders.
  - **Holdings:** each base's system, level, stash, status (building, hidden, or found and by whom) and upgrade, plus building a Lair where you are.
  - Economy, Post jobs and Black market come with the Depots (stage 10).
- **Tests:** `lairs.py` (in the quick suite). It covers the Company screen, no Lair where there's a station, missing materials, building with the ledger exact, ready after the build time, one per system, docking, laundering in the stash, the stash's capacity, lying low, level 2, paid rearming at a Lair, the Holdings tab, and a hostile scout finding the Lair and ships wearing it down.

### Stage 10: as built (2 Nov 2026)
- **New file `16o_depots.js`.** Tunables are in `DEP`.
- **Depots:**
  - **Building one:** upgrade a Lair in place (2 Depot Frames from your hold or its stash, while docked there), or build fresh in flight (2 Depot Frames in your hold) in a system with no station, outside the powers' home space.
  - **Upgrading a Lair in place:** the stash becomes the depot's store, and the Lair's fortifications become the depot's.
  - **What it is:** a player-owned depot station (Driftgate 1's `makeStation`, owner `player`, with `R.pid` naming its pilot). It is on every map, with Driftgate 1's depot modules in the Works tab.
  - **Level:** 1, then 2 with three modules, 3 with six.
- **Your market:**
  - On the Economy tab, mark each good in the store **Sell** (keeping a reserve), **Buy** (up to a target) or **Off**.
  - About every minute, traders of a power that will deal with you (Neutral standing or better, not hostile) visit. They buy up to 10 of each good for sale at the market price, paid from their power's treasury, and sell you up to 10 of each good you want from their power's stores.
  - Credits and goods only move, so both ledgers stay exact.
- **AI crews** (the Post jobs tab):
  - **Hiring:** a pilot comes with a hull, for the hull's price (at least 800 cr) paid to the Compact. Your Rating gates the hull. Each depot's hangar holds one crew plus one per hangar module.
  - **Orders:**
    - **Mine:** 3, 5 or 7 t a minute of this system's ore into the store.
    - **Haul:** every two minutes, 20, 35 or 70 t of goods marked for sale, sold at the nearest market that deals with you.
    - **Guard:** +25% to the depot's guns each.
    - **Idle.**
  - **Upkeep:** 300 cr an hour each to the Compact (paid each minute), and an Alloy Plate an hour of running costs from the store, into the outer drift. Unpaid crews leave; without plate the ship is laid up.
  - Crews work while you're away, abstractly, every minute of game time.
- **The Economy tab:** for each depot, the last hour's net (gaining or losing), its trend against the hour before, the lines behind it (market, hauling, hire, wages) and the latest reasons in plain words, plus the company's total. Each base keeps its log in `R.eco`.
- **Not yet:**
  - Crews as ships in the world (they work abstractly).
  - Posting jobs to other contractors and other factions' pilots, and bidding.
  - The Black market tab.
  - Base capture-or-destroy choices.
  - Guests can't change crews from flight (actions go through the dock).
- **Tests:** `depots.py` (in the quick suite). It covers a Lair upgraded to a Depot with the store from the stash, your market selling and buying through traders, hiring within the hangar's room, crews mining and paying wages, laid-up ships, an unpaid crew leaving, and the Holdings, Economy and Post jobs tabs, with the ledger checked throughout.

### Stage 11: as built (2 Nov 2026)
- **New file `16p_stations.js`.**
- **Upgrading a Depot to a Station** (Holdings tab): a Capital Keel, 2 Depot Frames and a Compact Seal, from the depot's store or your hold. It gets 1.8× hull and shield.
- **Only a Station holds the system for you.** A Depot alone doesn't count (`sectorOwner` skips it).
- **Buildings:** one per level, up to five, chosen from six. Each takes a Depot Frame, 20 Alloy Plate and 4 Flux Coils, which go into the station's fortifications. A station's level is its number of buildings (at least 1).
  - **Shipyard:** the dock sells hulls (your own design line), and the slip builds capitals.
  - **External storage:** traders take and bring twice the lot.
  - **Defence platform:** +50% guns and +50% hull.
  - **Hangar:** two more crews.
  - **Forge:** a workshop and forge with no fee.
  - **Market wing:** traders call twice as often and pay 10% more.
- **Capital ships at your slip:** an **Escort from level 3** and a **Carrier at level 5**, at Driftgate 1's costs and build times. They are paid from the station's store or your hold and launch as your own capitals (Driftgate 1's player capitals: ordered from the galaxy map, flyable from the bridge). The limits are two escorts and one carrier.
- **Not yet:**
  - The destroyer (it comes with its model and main gun).
  - The approved station and building models (stations still draw as Driftgate 1's depot).
  - AI choosing to capture or destroy a fallen base.
  - Station hull upgrades.
  - In multiplayer, a guest's capitals launch on its design faction's side.
- **Tests:** `stations.py` (in the quick suite). It covers a Depot not holding the system, a Station that does, four buildings and their effects, an Escort laid down at level 3 and launched, and the Carrier refused below level 5, with the ledger checked throughout.

### Stage 12: as built (2 Nov 2026)
- **New file `16q_strategic.js`.** The galaxy map (M) now opens a **sector view** for the selected system, above its usual detail.
  - **What it draws:** top-down, its gates (named for where they lead), its station in its owner's colour, its rocks (Riftstone in pink), your Lairs, and the ships there. Ships are live when the system is loaded; elsewhere it shows the capitals and convoys your intel knows of.
  - It counts ships and threats (the Brood, the Unbound, and powers hostile to you).
- **Orders from the view:**
  - Your capital ships: **Guard here** (hold this system) or **Come here** (from elsewhere).
  - The AI crews at your depot in that system: mine, haul, guard or idle.
- **Not yet:**
  - Zooming the map itself into the sector.
  - Orders to escort or patrol.
  - Crews as ships you can see in the view (they work abstractly, stage 10).
- **Tests:** `strategic.py` (in the quick suite). It covers the sector view in the loaded system and in another, and a capital ordered from the view.

### Stage 12b: as built (2 Nov 2026)
- **The new galaxy** (from the approved `tools/previews/beyond_map.py`) replaces Driftgate 1's map in `SECTOR_DEFS` and `LINKS`: 46 systems and 77 gates.
  - **Layout:** deep space at the centre round the Bloom (an inner ring of five deep systems and a rim of six), and the Wrack hidden inside it, gated to three deep systems. The freeports sit in pockets whose two gates both lead into deep space. Then the open ring of twelve (frontiers, forges and quiet doors), the cores, the relay and quiet space out to the corners.
  - **Map drawing:** systems are drawn spread out from the centre (radius r becomes 0.48·(r/0.48)^0.72) so the crowded inner rings have room. Quiet systems' names are smaller and dimmer.
  - **System ids:** existing ones keep their ore; new systems take their kind's ore mix. The freeports keep their ids, and their start-screen blurbs describe where they now sit.
  - The test checks no two gate lines cross, and that every freeport's two gates lead into deep space.
- **Scrapheart Haven for contractors** (new file `16r_wrack.js`):
  - **Neutral ground:** while you keep the peace, its guns and the Unbound in the Wrack hold their fire. Attacking an Unbound ship breaks the peace for a minute.
  - **Its market** buys and sells anything, stolen goods and contraband included, from the Unbound's stores and treasury.
  - **The Rusty Tankard's rumours** are black-market runs out of Scrapheart into the powers' stations within six jumps: Heavy heat, or Severe into a core. They are paid by the Unbound on delivery and count for your Rating.
- **The Unbound fly bigger holds:** Raider, Corsair, Plunderer and Skiff carry 40% more.
- **Not yet:**
  - Pirate gear for contractors (jammers, harpoons and cargo hooks as fitted parts).
  - The Ravager and the Dread Pirate.
  - A war check on the new map (balance targets are still undecided).
- **Tests:**
  - `galaxy.py` (in the quick suite) covers the system and gate counts, no crossings, freeports gated into deep space, the Wrack's neighbours, bigger Unbound holds, docking at Scrapheart in peace, its market and rumours, a rumour run paid by the Unbound with the ledger exact, and the peace breaking.
  - `mp_loopback.py` is retired with Unbound mode.

### Stage 13: as built (2 Nov 2026)
- **New file `16s_declare.js`.**
- **Winning:** **20 systems held for 10 minutes** (`VIC_NEED` 20, `WIN_TIME` 600). The freeports and the Wrack can't be held, which leaves 42 of the 46 systems. **No deadline:** the two-hour tie-break is gone, so a galaxy runs until someone wins, and the HUD clock is hidden.
- **Declaring a faction** (Allegiance tab) takes a Station of your own.
  - Declared, your Stations count toward the galaxy as your faction's systems, and you can win. Lead, and the three powers' truce turns on you (their ships become hostile).
  - **Losing your last Station** ends the faction. You keep your company, and can declare again with a Station.
- **Leaders' proposals to a founder,** about every ten minutes per power, answered on the Allegiance tab within five minutes:
  - **An alliance,** when standing is +40 or better and the leader isn't Vengeful. Accepting it opens that power's stations to you, gives +10 standing with it, and −8 with its enemies.
  - **A demand for 2,000 cr tribute,** when standing is −20 or worse. Paying gives +12. Refusing gives −15, and its ships attack you for ten minutes.
- **Slower war pacing:** leaders act less often (cooldowns 240–480 s, from 150–300) and pairs wait longer between events (450 s, from 300).
- **The Brood starts slow and grows with what it holds:** one strength scale from the systems it holds. It is 0.5 with the Bloom alone, 1 at five systems and 2 at twelve or more, and it scales its building, offensives, grazing and regrowth. Its Hive Ships come out from four systems. The fast simulator reports the scale (`relStats().broodK`) and the counts.
- **Not yet:**
  - Player factions in the faction status ledger as their own column; their standing with you stands in for it.
  - Swearing to another player's faction.
  - Your faction running Driftgate 1's strategic AI on its own.
  - Tuning to the Brood's 20% target, since balance targets are not set.
- **Tests:** `declare.py` (in the quick suite). It covers the win rules, declaring refused without a Station, a Station and declaring, the truce on a declared leader, an alliance accepted and a tribute refused, the Allegiance tab, the faction ending with its last Station, and the Brood's scale.

### Stage 14: as built (2 Nov 2026)
- **New file `16t_legend.js`: Legend reworked** (kept per callsign on the device, beside Driftgate 1's record).
- **Legend points**, each once per galaxy:
  - Rating 5: 1, and Rating 10: 1 more
  - your first Lair: 1, Depot: 1, Station: 2
  - declaring a faction: 2
  - shooting down an ace or a Brood Hive Ship: 1
  - your faction winning: 6, or being allied with the winner: 3
  - Nobody scores the win when the Brood wins.
- **Legend levels** come at 2, 4, 7, 10, 14, 18, 23, 28, 34 and 40 points, with titles Journeyman (1), Veteran (5) and Founder (10).
- **The start package:** on the leaderboard sheet you tick the perks you've unlocked, each costing its level in start points, with your level as the budget. You can take one Rating perk and one base perk. The package is applied as the galaxy is made, before its ledger baseline:
  - Rating 2, 4 or 6
  - +5,000 credits
  - a fully equipped medium hull (fighter, miner or hauler)
  - three grade 2 parts in your first weapon slots
  - a Lair kit (your first Lair needs no materials)
  - house-brand hulls at Trusted standing
  - a level 1 Depot, or a level 1 Station, in the nearest system where one can be built
- **Conqueror's spoils** are banked when your declared faction wins:
  - your flagship and its parts
  - a war chest (10% of your credits, at most 25,000)
  - three veteran crews (no hire cost and no wages for two hours)
  - Renown (+25 with every power)
  - the Wraith in yards
  - Allied winners get half (a smaller chest, one veteran, Renown +12).
  - The spoils are carried into the next galaxy and then used up.
- **Driftgate 1's Legend perks no longer apply** (`P.lvl` is 0 in Beyond galaxies). The leaderboard ranks by Legend level.
- **Not yet:**
  - **Multiplayer rivalries.** Pilots in one galaxy each have their own bases and crews (`R.pid`), but guests' Legend points, other pilots' bases as targets, and posting jobs to rival companies are still to do.
  - **The training rewrite.** Training still teaches Driftgate 1's systems in its own sandbox (Beyond's slots, payload, standing and bases are off there).
- **Tests:** `legend.py` (in the quick suite). It covers the package picker, a level 10 start package with the ledger exact, a point awarded once per galaxy, a win banking spoils, and the next galaxy carrying them (Renown, war chest, the Wraith) with a starting Station and the ledger exact.

### After stage 14: pirate gear (2 Nov 2026)
- **New file `16u_piracy.js`.**
- **The gear:**
  - **Jammer:** a weapon part. Key 4 toggles jam mode: guns fire jam rounds and missiles fly as shock harpoons, as the Unbound's do. Jammers never kill and do nothing to a shielded ship.
  - **Cargo hook:** a utility part. Hold E beside a ship jammed dark (150 m, or 400 m on a harpoon tether) to hook its hold at 8 t a second, most valuable first. What you take is tagged stolen from its owner and costs heat and standing with it.
  - **Where to get it:** Scrapheart sells both (3 each at the start). They are never built at a workshop.
- **Carrying it is contraband:** a customs scan that finds pirate gear raises that power's heat: Light (+15), or Heavy (+30) if you've jammed one of its ships in the last hour. Gear in the hold can be hidden in a hidden container; fitted gear can't.
- **A fix found on the way:** a contractor's gunfire now hits any power's ship, as Driftgate 1's lasers and missiles already did through `hostAt` (stage 1 had missed the guns).
- **Not yet:** a guest's cargo hook (the host hooks for its own pilot only).
- **Tests:** `piracy.py` covers Scrapheart's stock, fitting the gear, jamming a hauler dark and hooking its hold (stolen tags, heat, standing, ledger exact), and the customs heat.

### Training rewrite: section 1 (2 Nov 2026)
- **New file `16v_training.js`.** Training is now ten short sections, each started on its own from the Training button. The picker lists all ten, with the unbuilt ones marked "coming soon".
  - A section starts you as an independent contractor docked at the freeport picked on the start screen, in a private practice galaxy.
  - Beyond's ship systems (slots, payload, the landing kit) are on; customs, Rating and crews stay quiet.
- **Section 1, Flight and your first job** (agreed with the user: flight, the controls, the ways to fly, and simple job acceptance), 21 steps:
  1. Launch.
  2. Thrust and steer to 150 m/s.
  3. Brake below 20 m/s.
  4. Roll.
  5. The afterburner above 200 m/s.
  6. Flight assist off: drift and turn while coasting.
  7. Flight assist back on.
  8. Auto-level off.
  9. Auto-level back on.
  10. The cockpit camera.
  11. The chase camera.
  12. Target a rock.
  13. Land on it.
  14. Lift off.
  15. Autopilot to the freeport.
  16. Dock.
  17. Open the Jobs tab.
  18. Select a job.
  19. How issuers, pay and standing work.
  20. Launch and make a jump on the job's course with autopilot.
  21. Wrap-up.
- **Driftgate 1's old courses** stay in the code (the full suite's `training.py` still drives them) but are no longer offered.
- **The start screen** now describes Beyond: 46 systems, starting as a contractor, and 20 systems for 10 minutes with no deadline.
- **Sections 2–10** come next, each agreed before it's built.
- **Tests:** `train_flight.py` covers the picker and the start state, then walks all 21 steps through the game's own controls and state.

### After stage 14: AI crews as ships you can see (2 Nov 2026)
- **New file `16w_crews.js`.** While a depot's system is loaded, each of its working crews flies there as a ship on your side, labelled with the pilot's name and job:
  - **Miners** hover at the system's nearest rock with their beams on.
  - **Haulers** shuttle between the depot and the nearest gate.
  - **Guards** circle the depot and fight anything hostile that comes within about 2.6 km of it.
  - **Idle crews** wait beside the depot. **Laid-up crews** stay in the hangar (no ship).
- **The work itself is still abstract** (stage 10's minute tick), so the ships move no goods: a miner's beam is for show, and the store fills from the tick as before.
- **A crew ship destroyed is a crew lost:** the pilot and the hull leave the hangar, and you're told. Crew ships carry nothing, so a loss drops nothing and the ledger is untouched.
- Changing a crew's job swaps its ship; crew ships don't take room from the system's ordinary traffic.
- **Not yet:** in multiplayer, only the host's own crews fly (a guest's crews keep working abstractly).
- **Tests:** `crews.py` (in the quick suite) covers a miner, a hauler and a guard flying their jobs, a job change, a laid-up crew, a crew ship destroyed and the crew lost, no crew ships in other systems, and the ledger.

### After stage 14: base models (2 Nov 2026)
- **The approved company-style models** from `tools/previews/beyond_stations.py` are in the model pack (`by_*`, kind `base`: no stern glow, dark trusses stay dark). The pack records each base model's centre and half-extent so the game can reassemble them.
- **New file `16x_bases.js`** draws your bases with them:
  - **Lairs:** the rock with its hangar cut in (level 1), or with the second berth, forge vent, stash and dish (level 2).
  - **Depots:** by level (1 storage; 2 production and hangar; 3 turrets, armour plates and the life-support ring).
  - **Stations:** the core with its five hardpoints, and each building you've added on a hardpoint, in the order you built them (shipyard, external storage, defence platform, hangar, forge, market wing). Each shape is assembled once and cached.
  - The base's turrets sit on the model (a Depot's dome rim, keel and arm; a Station's habitat ring and crown) and re-seat when the base changes shape.
- **The model pack** grows by about 350 KB (12 models).
- **Not yet:**
  - Driftgate 1's module works (the targetable store, production, armour and life-support blocks, and the shipyard slip) still draw round a player base as they always did. Folding them into the new models is a later pass.
  - The powers' stations, the freeports and Scrapheart Haven in their approved Beyond looks (`beyond_faction_stations.py`, `beyond_unbound_base.py`).

### Destroyers and the Ravager: as built (2 Nov 2026)
Driftgate 1 v255 removed its frigates, but their code paths survive everywhere a capital isn't an escort or a carrier: the lance (a heavy capital shot at stations, works and capitals within 2.6 km), the stand-off at 1.6 km from a station, the line-ship orders (`frigOrders`: go for hostile depots, open systems and enemy capitals), the hardest-hitting abstract fight. **Beyond's destroyer is that line ship brought back** (internal class `frigate`, shown everywhere as "destroyer"), with the approved models and a charged main gun.
- **Stats (proposals, to tune):** hull 4,200 (escort 3,100, carrier 5,000), shield 2,000. Two assault ships. No hull berths (as decided), the frigate's five point-defence turrets.
- **The main gun fires a charged shot.** It charges for 3 s, and **while it charges the ship's shields are down** (whatever shield it had comes back when it fires). One shot does 600 to its target (about the old lance's damage over time), then 4 s to reload. The bridge's fire control fires it by hand as it did the lance. Off-screen fights resolve as Driftgate 1's frigates did.
- **The Brood's destroyer, the Gullet:** no shields at all. Its **Maw Cannon** charges for 4 s, then fires a beam 2.6 km straight ahead that does 900 to every hostile ship, station and works it passes within 50 m of; 7 s to recover.
- **Who builds them:** each power and the Brood keep **one** destroyer (proposal), built at their capital shipyard after the yard is up, as escorts are (Escort cost plus half again, and the escort's build time plus half). The Brood grow theirs only once their Hive Ships are out (the stage 13 ramp).
- **Your own:** a level 4 Station with a shipyard lays one down (from its store or your hold), one at a time; you keep one. It launches as your capital like an escort, ordered from the map and flyable from the bridge.
- **Models:** the approved Peregrine (Halcyon), Ironclad (Varkesh), Prism (Ostrova) and Gullet (Brood) go into the model pack; turrets sit on the models' own point-defence mounts.
- **The Ravager** (the Unbound's only capital): Driftgate 1's Unbound "destroyer" (their carrier, with its plundered wing and boarding pinnaces) becomes the Ravager with the approved model, and gains the charged main gun (its Varkesh giant gun: 3 s charge with shields down, 500 a shot, 6 s to reload). **The Unbound stop building sloops** (their escorts), so the Ravager is their one capital: one per galaxy at first, laid down at Scrapheart from minute 80 as their carrier was.
- **Balance:** this adds a capital to every power and takes the sloops from the Unbound, so it moves faction strength. The targets aren't set yet; a war check on the new map comes after.
- **New file `16y_capitals.js`**; the Unbound's slip changes are in `16_expansion.js` (`pirTick`).
- **As built, beyond the spec:** the Gullet turns its whole body onto its target and fires only when the maw bears. The Peregrine has eight mounts; six carry turrets (its middle pair stays bare), so every destroyer fires six. AI powers lay one down when the carrier is out (or they can afford both), more readily at war, and rush it at war as they do carriers. A destroyer's shield is down for as long as its gun charges: anything hitting it then goes straight to the hull.
- **Not yet:**
  - Beyond's approved escorts and carriers (Shrike, Sovereign and the rest) and the other Unbound hulls in the model pack; escorts and carriers still draw as Driftgate 1's.
  - The bridge's weapons console still calls the main gun the lance.
  - A guest doesn't see the charge glow (the shot and the beam do reach guests).
  - The Dread Pirate.
  - A war check (balance targets aren't set).
- **Tests:** `destroyers.py` (in the quick suite) covers a power laying one down and launching it (two assault ships, hull and shield, model, turrets on its mounts), a destroyer duel (shields down while charging, a 600 hit), the Gullet's beam hitting three ships in a line, your level 4 Station laying one down (refused below level 4, one at a time), the Ravager's name, model and gun, no sloops laid down, and the ledger throughout.

### Training rewrite: section 2 (2 Nov 2026)
- **Section 2, Contracts and standing** (agreed with the user 2 Nov 2026), 13 steps, in `16v_training.js`. It starts at the picked freeport with a freeport request set up to the nearest other freeport (three jumps), for a good this freeport sells and you don't already own.
  1. Open the Allegiance tab.
  2. Standing: the scale, the five bands and what each opens or closes, how work raises it and damage lowers it, the drift back to 0, the Compact's standing.
  3. Between the powers: the relations table, leaders and the Chronicle; war work costs a quarter of its standing with the enemy, and freeport work never does.
  4. Open the Jobs tab.
  5. The kinds of job: supply contracts (own goods only, partial delivery), freeport requests, blockade runs, convoy raids and escorts, and their time limits.
  6. Select a job and drop it.
  7. Select the freeport request (its course is set).
  8. Buy the goods here.
  9. Fly the three jumps on autopilot.
  10. Dock.
  11. Deliver.
  12. Paid by the Compact's treasury, and the standing gained; a power's contract works the same way.
  13. Wrap-up.
- **The Allegiance tab** now shows in Beyond's training sections.
- **A fix found on the way:** a station's Overview crashed when a freeport request could be delivered there (it looked up the Compact as a faction).
- **Tests:** `train_contracts.py` (in the quick suite) walks all 13 steps through the game's own actions, with the payment, the standing and the ledger checked.

### Training rewrite: section 3 (2 Nov 2026)
- **Section 3, Combat** (agreed with the user 2 Nov 2026), 14 steps, in `16v_training.js`. It puts you in a Light Fighter at the picked freeport.
  1. Launch; three Unbound target drones (they don't fire) wait ahead.
  2. Target the nearest hostile.
  3. Cycle hostiles (and the other targeting keys).
  4. The machine gun (ammunition, rearmed and paid at a dock) and the laser (reactor energy); switch to the laser.
  5. Shoot one down: the lead marker and tracking.
  6. Shields and hull: what each takes, recharge, repair; lasers bite shields, rounds bite hull.
  7. A missile lock and launch.
  8. Flares.
  9. Finish the drones.
  10. Scoop a salvage crate (and what scooping a power's goods means).
  11. A live fight: two Unbound raiders jump in and shoot back.
  12. A distress call.
  13. What attacking a power costs: standing, a minute as its hostile, and convoy raids as the paid way to do it.
  14. Wrap-up.
- The practice crate's goods are added to the practice galaxy's books, so its ledger stays exact.
- **Tests:** `train_combat.py` (in the quick suite) walks all 14 steps through the game's own actions, with the ledger checked.

### Training rewrite: section 4 (2 Nov 2026)
- **Section 4, Mining** (agreed with the user 2 Nov 2026), 13 steps, in `16v_training.js`. It puts you in a Medium Miner with its stock tools: a charge launcher, a mining laser and a gun, and the landing kit. The hull swap goes through the practice galaxy's books, so the ledger stays exact.
  1. Launch.
  2. Target a rock.
  3. Reading a rock: its ring, fault points and rescanning.
  4. Cut 3 ore with the mining laser held on the ring.
  5. Switch to charges (and why charges crack the ring).
  6. Fire a charge onto a fault point.
  7. Back off and detonate (cancelling explained).
  8. Scoop 3 ore from the chunks.
  9. The ores and where they lie (Aurorite deep, Vantium contested, Riftstone and its contraband status), weight and handling, bigger miners.
  10. Dock at the freeport.
  11. Deliver half your ore to a request set up there (and why supply contracts want your own ore).
  12. Sell the rest at the Market.
  13. Wrap-up.
- **Tests:** `train_mining.py` (in the quick suite) walks all 13 steps with the game's own controls (the laser held with F on the ring, a charge fired, detonated and scooped), with the ledger checked.

### Every approved design in the game (2 Nov 2026)
- **Asked by the user:** the starter miners and haulers still drew as Driftgate 1's; push the entire design live.
- **The model pack now holds every approved Beyond model** (about 3 MB in the page, 79 new models), built from the preview scripts by `tools/build_models.py`:
  - **Each power's work ships** (Wren, Plover, Heron, Tern, Albatross, Pelican; Pick, Gouge, Sledge, Runner, Bulwark, Rampart; Glim, Lumen, Delve, Drift, Cairn, Monolith), mapped in `16j_designs.js`.
  - **Scouts, advanced scouts, bombers and heavy bombers** (Lark, Skylark, Condor, Harrier; Jackal, Wolfhound, Maul, Warhound; Seer, Oracle, Obelisk, Sentinel).
  - **Constructors and drones** (Architect, Foundry, Loom; Aegis, Ward and Halo drones).
  - **Escorts and carriers** (Shrike, Sovereign; Vanguard, Bastille; Lantern, Cathedral). Their turret mounts, sub-target points (drives, shield generator, torpedo tubes, bays) and the carriers' deck spots are recorded from the models as they're built, so turrets, Shift+T systems and deck landings sit on the new hulls.
  - **The house-brand hulls and the Wraith** (Gannet, Bombard, Vesper, Wraith).
  - **The Unbound hulls** (Raider, Skiff, Corsair, Plunderer; the Wrecker is packed but no class flies it yet).
  - **The powers' stations and depots** (the Halcyon lens, the Varkesh Talon Citadel, the Ostrova station, and their depots), **the freeport** and **Scrapheart Haven**. Station turrets are set onto each model's own surface, and docking ports come from the new geometry.
  - **The Riftstone rock**, in its hot pink.
  - Brood fins come from `tools/brood.py`, already in the pack.
- **New file `16z_models.js`** maps classes to models (models only: no stat changes come with them) and fixes each power's destroyer name in its hull list (Peregrine, Ironclad, Prism).
- **Not yet:** the shared assault ship model (assault ships are still loads aboard capitals, never drawn); Driftgate 1's station works modules still draw round stations as before.

### Bug sweep (2 Nov 2026)
- **Single player:** the quick suite, Driftgate 1's training courses (`training.py` now starts them directly, as Beyond's picker offers only its sections), `contacts`, `hull_tags`, `designs`, a 15-minute soak in eleven hull and faction setups, and the dock sweep over every station, outpost and Lair tab. Fixed:
  - A station's Overview crashed when a freeport request could be delivered there (found by training section 2).
  - The job board's "Switch to a … here · free" button offered paid hulls as free; it now shows the price (a Lark at a freeport is 1,350 cr).
- **Multiplayer:** the five faked-link tests and a new one, `mp_beyond.py`, for Beyond's late additions seen and used by a guest.

### Win check without players (2 Nov 2026)
- `PPORT=mw python3 tools/fastsim.py FILE 300 16 - 2 OUT.json`: 300 strategic-only galaxies, the player idle at a freeport, capped at 16 hours, on the build with destroyers, the Ravager and no sloops.
- **Who wins:** Halcyon 36%, the Brood 34%, Ostrova 15%, Varkesh 10%, no winner within 16 hours 5%.
- **How long:** median 6 hours (quartiles 3.8 h and 9.4 h). Powers win at a median of about 4–5 hours; the Brood wins late (median 9.4 hours), after the powers have fought each other down. Ten Brood wins came in galaxies where the powers never went to war.
- About 9 wars per galaxy; no errors in any game.
- **Against the working targets** (Brood about 20%, a galaxy won in 8–12 hours): the Brood is high, Halcyon strong, Varkesh weak, and power wins come early. No tuning yet: the targets aren't settled.

### Balance tuning toward the new target (2 Nov 2026, in progress)
- **Target (from the user):** the Brood about 20%, each power about 25%, no winner about 5%.
- **A fix first:** a station's extraction each tick was rounded to whole units, so `BAL.ext` moved the balance in steps (Halcyon's depots went from 2 units to 1 at a mining rate of about 0.536, swinging its wins from 36% to 14%). Extraction now rounds up or down at random (`sRound`), so its average is the exact rate.
- **Runs so far** (no players, 16-hour cap): with the fix and the old rates, Halcyon 39%, Brood 23%, Ostrova 21%, Varkesh 12%, none 5%. Best so far, 600 galaxies with mining rates Halcyon 0.52, Varkesh 2.1, Ostrova 0.86 and a weaker Brood ramp ([[1,.4],[5,.78],[12,1.45]]): Ostrova 26%, Brood 25%, Varkesh 24%, Halcyon 22%, none 3%. Varkesh needs the most help: its Ambitious, Vengeful leader keeps it at war with both other powers. The numbers aren't in the game yet.
- **The user's direction (2 Nov 2026):** don't balance on leader traits; the balance pass is neutral (every starting leader without traits in the balance runs), and traits are left to cause problems in play. A power that is cut down or bleeds enough ousts its own leader.
- **Leaders ousted (built, `16g_leaders.js`, `LEAD_OUST`):** from 30 minutes into a leader's rule, a power that loses half the systems it held at its best under that leader (at least 5), or runs up 30 ships' worth of recent losses, ousts the leader. The successor shares none of the ousted leader's traits and leans Cautious or Patient; after an ousting the new leader has an hour's grace. About 3 ousted leaders a galaxy in the runs, mostly from a power in collapse.
- **Neutral runs (300 galaxies):** original rates: Halcyon 37%, Brood 31%, Ostrova 17%, Varkesh 12%, none 3% (100 galaxies). Rates Halcyon 0.55, Varkesh 1.5, Ostrova 1.0 with the Brood ramp [[1,.4],[5,.78],[12,1.45]]: Brood 27%, Ostrova 25%, Halcyon 23%, Varkesh 22%, none 3%. Not in the game yet; "none" still runs short of 5%.
- **Tuned on stats with neutral leaders (3 Nov 2026), now in the game:** `BAL.ext` Halcyon 0.54, Varkesh 1.7, Ostrova 0.95 (was 0.712, 1.2, 0.84); the Brood ramp [[1,.37],[5,.73],[12,1.37]] (was [[1,.5],[5,1],[12,2]]). 600 galaxies: Halcyon 27%, Ostrova 25%, Varkesh 25%, Brood 21%, none 2%. A second 300-galaxy check of the built game gave Brood 28%, Halcyon 25%, Varkesh 23%, Ostrova 22%, so the Brood may sit a few points over 20%; a larger confirming run was under way. `fastsim.py` now starts every leader neutral unless `LEADERS=1`. Game length and the no-winner share aren't targets (the user, 3 Nov 2026).

### Why the powers need different mining rates (3 Nov 2026)
Asked by the user: why would a side need a boost to compete? Each test below is 300 galaxies with neutral leaders, every power on the same mining rate (1.0), and one more asymmetry switched off each time:

| Test | Halcyon | Ostrova | Varkesh | Brood |
|---|---|---|---|---|
| Equal mining, everything else as built | 58% | 14% | 11% | 16% |
| … without Halcyon's protected freeport convoys | 56% | 18% | 8% | 16% |
| … without Ostrova's perks (third escort, cheaper carrier, safer scouts) | 58% | 17% | 6% | 18% |
| … without Halcyon's Trade Charter | 20% | 32% | 12% | 35% |
| … without the Charter and Ostrova's perks | 22% | 26% | 14% | 36% |
| … and without the ship traits (+12% / −12% stats) | 20% | 21% | 17% | 39% |

- **Halcyon: the Trade Charter.** Driftgate 1 gave Halcyon two AI economy perks: when its ore runs low it hires Freeport prospectors to mine its own systems, and it imports from the freeports at twice the volume at a discount. It never starves of ore, so at an equal mining rate it wins nearly 60% of galaxies. Its own mining rate is cut to compensate (0.53).
- **Varkesh: no AI perk at all.** Its perks (Aurorite job pay, Ward drones on mining hulls) only help human pilots and live fights; nothing helps the AI's economy. Its hull-for-reactor trade costs it a few points in AI fights too. So it needs the biggest mining boost (1.75).
- **Ostrova: small perks** worth a few points (a third escort, carriers 8% cheaper, scouts that survive more): a modest rate (0.95).
- **The map is even:** each power's home is 4 jumps from the Bloom and from each other power, with 10 systems within 2 jumps; with every perk and trait removed the three powers come out within a few points of each other.
- **Leaders aren't balanced on** (the user's direction): their traits sway real galaxies.
- **Final values in the game (3 Nov 2026):** `BAL.ext` Halcyon 0.53, Varkesh 1.75, Ostrova 0.95; Brood ramp [[1,.37],[5,.73],[12,1.37]].
  - **Neutral leaders (the balance), 600 galaxies:** Varkesh 27%, Halcyon 26%, Ostrova 26%, Brood 18%, none 3%. Across the last four 600-galaxy runs at nearby values the Brood averaged about 20%.
  - **With the starting leaders' traits (`LEADERS=1`), 600 galaxies:** Ostrova 32%, Varkesh 23%, Halcyon 22%, Brood 20%, none 2%. Ostrova's Scheming, Patient leader is worth about 6 points; Varkesh's Ambitious, Vengeful leader costs it about 4 (the ousting rule replaces it when Varkesh is cut down); Halcyon's Mercantile, Cautious leader costs it about 4. About 3.3 successions a galaxy.

### Starting leaders rolled for each galaxy (3 Nov 2026, built)
- **Asked by the user:** so the same story doesn't play out every galaxy, the starting leaders' traits differ each time.
- **As built (`16g_leaders.js`, `LEADT`, `leadRoll`):** every new galaxy gives each power's first leader two different traits drawn from the fourteen, and no two leaders get the same pair. Titles stay with the power (Chair of the Merchant Houses, Marshal, First Archivist); names were already drawn at random. `fastsim.py` starts leaders neutral for balance runs (`LEADT.mode='neutral'`), and `LEADERS=1` rolls them as a real galaxy does.
- **The live balance with rolled leaders (600 galaxies):** Varkesh 28%, Halcyon 26%, Ostrova 22%, Brood 20%, none 4%. Rolled traits average out across galaxies, where the fixed pairs had given Ostrova 32%.

### Proposal: balance through perks instead of hidden mining rates (3 Nov 2026, not built)
Today each power's AI mines at its own hidden rate (Halcyon 0.53, Varkesh 1.75, Ostrova 0.95) to make up for its perks. The alternative: every power mines at the same rate, and each power's edge is a named perk, sized so that they come out even.

| Power | Perk | Size in the proposal |
|---|---|---|
| Halcyon | **Trade Charter** (Driftgate 1's, kept): when short of ore it hires Freeport prospectors to work its own systems, and at times buys from the freeports at double volume and 20% off | prospectors on 5% of chances (was 50%), bulk buying on 2% of ticks (was 8%) |
| Varkesh | **Deep Bore** (new): Dominion stations and depots mine more ore, fitting its mining identity (Aurorite jobs, Ward drones on mining hulls) | +85% station mining |
| Ostrova | **Archive fleet** (as built): a third escort, carriers 8% cheaper, scouts that survive more | unchanged |

- **Neutral leaders (900 galaxies across two runs):** Halcyon 26%, Varkesh 25%, Ostrova 25%, Brood 22%, none 1%.
- **With rolled leaders (600 galaxies):** Halcyon 28%, Ostrova 28%, Varkesh 21%, Brood 21%, none 2%.
- If adopted, the perks would be shown on the start screen and in each power's description, and the Brood's ramp trimmed slightly to bring it back to 20%.

### Balance through perks: as built (3 Nov 2026)
- **The user's choice:** balance through perks, with Varkesh's perk as tougher ships: more hull, its reactor penalty changed to a speed penalty, and hulls that repair themselves slowly (in place of the proposed Deep Bore).
- **Every power mines at the same rate** (`BAL.ext` 1.0 each). The hidden rates are gone.
- **Halcyon, Trade Charter** (kept, scaled down): prospectors on 5% of chances when ore is short (was 50%), bulk freeport buying on 2% of ticks (was 8%). Ships: shields +12%, hull −12% (unchanged).
- **Varkesh, Dominion hulls** (new): hull +25%, speed and thrust −10% (the old −12% reactor is gone); every Varkesh-built ship regains 0.4% of its hull a second (capitals 0.12%) from 8 s after its last hit, and its capitals repair off-screen too. In battles nobody watches it fights 14% harder and loses 14% less (`FACTIONS.varkesh.tough`), so the perk counts in the AI's war as it does in the open. A pilot flying a Varkesh design line gets the self-repair too; the fighter designs keep their own approved numbers.
- **Ostrova, Archive fleet** (unchanged): a third escort, carriers 8% cheaper, scouts that survive more. Ships: reactor +12%, shields −12%.
- **Shown in the game:** the Allegiance tab has a new "The powers" table with each power's perks.
- **The Brood ramp** trimmed to [[1,.31],[5,.6],[12,1.15]] to stay at 20%.
- **Results (600 galaxies each):** neutral leaders: Ostrova 28%, Halcyon 27%, Varkesh 24%, Brood 20%, none 1%. Rolled leaders: Varkesh 27%, Halcyon 26%, Ostrova 24%, Brood 21%, none 2%.
- **Tests:** quick checks of hull and speed (a Varkesh Medium Hauler 425 hull and 183 m/s against Halcyon's 299 and 203), self-repair (213 to 230 hull in 10 s), the Allegiance table, and the load, start screen, relations, designs, loadout, ship, destroyers and jobs tests.

### Lairs: laundering takes time (3 Nov 2026)
- Lying low (heat cools three times as fast while docked at your Lair) and laundering were built in stage 9; the stage 7b "not yet" list was out of date.
- **New file `16za_launder.js`:** as the design says, laundering now takes a spell instead of being instant. Stolen goods put in a Lair's stash keep their tag for 60 s plus 5 s a tonne (10 t of Iridium: 1 min 50 s). Taken out early, they come out still tagged; when the spell ends the tag is gone and you're told. The dock header shows what's still being laundered. Only tags move, never goods.
- **Tests:** `lairs.py` now also covers goods taken out early (still tagged) and the spell ending.

### Scrapheart Haven knocked out (3 Nov 2026)
- **New file `16zb_haven.js`.** When Scrapheart's hull is broken it is knocked out, never destroyed, for 30 minutes:
  - its market and the Rusty Tankard shut (docking still works), and no new rumours are posted;
  - its guns stay dark;
  - Unbound wings turn up half as often, and their slip stops (a build in it waits);
  - whoever broke it takes a quarter of every good in the Unbound's stores and a quarter of their treasury: a power into its own stores and treasury, a pilot into the vault where they last docked and their credits. Everything only moves, so the ledger stays exact.
- It comes back lit at half hull, with everyone told.
- **Tests:** `galaxy.py` covers the knock-out (the haven at 1 hull, a quarter of the plate and credits moved, the market and rumours shut), the reopening at half hull, and the ledger.

### The Dread Pirate: as built (3 Nov 2026)
- **New file `16zc_dread.js`.** The Unbound are led by the Dread Pirate (the title passes with the hat). Each galaxy rolls a name (Marrow, Black Agnes, Saltjaw, Iron Nell…) and two traits from the pirate table: Bloodthirsty, Greedy, Cunning, Showman, Superstitious, Gallant, Paranoid, Kingmaker. The war check starts it without traits, like the powers' leaders.
- **Its ship.** Aboard the Ravager while the Ravager is afloat (going down with it if it's sunk); otherwise a Corsair with three times the hull, twice the shields and an ace escort, moving every few minutes among the Wrack and nearby systems (a Paranoid captain stays within two jumps, a Superstitious one keeps out of Brood space). Met in a system, it's named on radar (☠ the Dread Pirate …).
- **Killed.** Every power pays its killer 3,000 cr (9,000 in all). It's back with a new captain after 15 minutes. The successor's traits follow what happened: killed by a power → Bloodthirsty, with a grudge against that power; killed by a contractor → Paranoid, with a 2,500 cr bounty on that pilot; Scrapheart looted → Paranoid or Cunning; a rich treasury → Greedy or Showman; a power within four systems of winning → Kingmaker (these last two are checked now and then after an hour in the hat).
- **Pilots fly like it:** its traits set the Unbound's leader profile (how far they chase, whether they break off, whether they spare a beaten ship), the same way the powers' leaders set theirs.
- **Where the raids go:** a raiding season, a grudge or (for a Kingmaker) the leading power steers the Unbound capital toward that power's systems; Superstitious captains won't go into Brood space; Paranoid ones stay near home; lying low sends everything home.
- **Events**, at most one every 4–8 minutes, chosen among those whose trigger holds and weighted three to one toward its traits (none while Scrapheart is knocked out):
  - *Raiding season* on one power's lanes for 20 minutes.
  - *Tribute demand*: a power pays 1,500 cr (more likely if its leader is Mercantile or Cautious) or gets a raiding season.
  - *Bounty on a pilot* who has sunk six or more Unbound ships: Unbound ships go for that pilot first, and the Allegiance tab tells you.
  - *Hoard sale*: Scrapheart's market 30% cheaper for 15 minutes.
  - *Open house* at the Rusty Tankard: new rumours pay 30% more for 15 minutes.
  - *Lie low* when the Brood hold six or more systems or the Ravager is badly hurt: Unbound wings turn up a third as often for 15 minutes.
  - *Ravager raid* on a battered power depot within three jumps.
  - Not built yet: ransoms, a lair spree, and the "Unbound raiders lost to the Brood", "failed raids" and "bargains kept" successions.
- **Where you see it:** an Unbound row under the powers' leaders on the Allegiance tab (name, traits, whether it's flying or aboard the Ravager); a hunt job at every power's station (9,000 cr, its system shown if that power's sensors cover it); word of its whereabouts for 300 cr at Scrapheart.
- Everything moves credits between wallets and treasuries; no goods are made. **Test:** `dread.py` (roll, spawn, killed by you with the bounties and a Paranoid successor, aboard and sunk with the Ravager, events, hoard prices, the hunt job, the rumour, the ledger).

### When your base falls: capture or destroy (3 Nov 2026)
- **New file `16zd_fall.js`.** However a power breaks one of your Depots or Stations (assault ships, a siege, or guns alone), its leader chooses:
  - **Capture** (a Station 85%, a Depot 55% of the time to start with; +20 points for an Ambitious, Mercantile, Industrious or Opportunist leader, −15 for a Vengeful one, −30 if the base is away from the power's own space; a Ruthless leader always destroys). The base flies the power's flag at 75–90% hull with its buildings and modules and its store, less up to a quarter lost as debris in the fighting. A captured Station holds the system for that power. Your crews leave and your market orders lapse; your vault there stays yours. You're told, and the dock says it was captured from a contractor.
  - **Destroy:** Driftgate 1's raze (its stores spill and drift).
- **Taking it back:** break a captured base's hull yourself (or land assault ships on it) and it's yours again, with its store, at a third of its hull.
- **Lairs:** a power that wears one down impounds it (half the time to start with, the same leader leanings): the stash, less up to a quarter, goes into its stores and the Lair is shut. Otherwise it's destroyed and the stash drifts. An impounded Lair can't be taken back.
- The Brood and the Unbound always destroy. Goods only move, so the ledger stays exact.
- **Test:** `fall.py` (a Station captured with its building and store, holding the system for Varkesh, crews gone; taken back; destroyed; a Lair impounded; the ledger).

### The Black market tab: as built (3 Nov 2026)
- **New file `16ze_blackmarket.js`;** a sixth Company tab, **Black market**.
- **Contacts:** a freeport's fixers and a power's quiet buyers become your contacts when you dock there; the Rusty Tankard once you've been to Scrapheart.
- **Offers** from your contacts, each with its heat rating and the power whose heat it raises, its pay, and how far away it is:
  - **runs** (the fixers' and the Tankard's, from stages 9 and 12b), now priced at the destination's market rather than the goods' base value;
  - **contraband buys** (None): a fixer sells Riftstone, relics or Rift Shards from the freeport's stock at 85% of its price;
  - **quiet buyers** at a power's station pay over the odds for cash-only contraband (Heavy, +50%; Severe at a core, +75%);
  - **fences** at a power's station buy goods stolen from another power at 1.4× their value (Light with the power they were stolen from); the stolen tag goes with them.
  - Contacts post new buys and quiet buys on their own now and then; **Request work** asks the fixers, the quiet buyers or the Tankard for one now (once every 2 minutes).
- **Filter** by heat: All, None, Light, Heavy, Severe.
- **Assign a run** to:
  - **yourself:** loaded at once if you're docked at its source, otherwise your course is set there;
  - **one of your AI crews:** it flies the run abstractly (a minute plus 45 s a jump) if its hull's hold is big enough. The chance of being caught is 12%, 22% or 35% by rating, raised by your heat with that power and lowered for a Courier (×0.7) or Skiff (×0.85). If caught, that power seizes the goods and the heat lands on you; otherwise the goods reach the destination's market and you're paid. The crew drops its other orders while away;
  - **a Compact contractor:** you take a 25% broker's cut and nothing lands on you if they're caught.
- **Runs:** yours, your crews' and your contractors' in progress (which jump they're on, when they're due, your heat with the power at the other end) and the last results (paid or caught, and for what).
- Buys, quiet buys and fences are dealt in person: the button sets your course to the contact or deals when you're docked there.
- Goods only move (a run's load is counted in the ledger while it's under way). **Test:** `blackmarket.py`.

### Posting jobs to other pilots, with bidding: as built (3 Nov 2026)
- **New file `16zf_posted.js`;** the Post jobs tab gains **Jobs for other pilots**, below your crews. Four kinds, for any of your depots:
  - **Supply:** bring N of a good to the depot. The taker buys it at the nearest market that has it, at your expense, as far as your credits go.
  - **Haul:** sell N of a good from the depot's store at the nearest market that deals with you. The proceeds are yours.
  - **Mine:** cut N t of ore from the depot's system into its store.
  - **Guard:** stand guard over the depot for 20 minutes (its guns +50%).
- **The galactic mean** for a job is worked out live: the premium the powers' and the Compact's own jobs pay over their goods' value across the galaxy now, times the goods' value, scaled by the distance to the nearest market (Supply, Haul); by the tonnes (Mine); or by how many powers' homes are within three jumps and whether the Brood are next door (Guard).
- **Bids:** Low 75% (the floor), Medium 100%, Fast 140%; an exact figure can't go above 200%. The wait before an AI taker signs on is 3 minutes × (mean ÷ bid)²: Low about 5:20, Medium 3:00, Fast 1:32. The taker is a Compact contractor or a pilot of a power that deals with you, and does the job in 1.5 minutes plus 40 s a jump. The fee goes to the Compact or that power when it's done. Up to six jobs open at once; an open job can be withdrawn.
- **In multiplayer** another player can do an open Supply job first: it shows in their dock's Jobs list at your depot, and delivering pays them your bid pro rata.
- Depot spending shows on the Economy tab under "jobs". Goods only move. **Test:** `postjobs.py`.

### Your own brand: as built (3 Nov 2026)
- **New file `16zg_brand.js`;** a **Your brand** section on the Holdings tab once you have a Depot.
- **Company name:** you name your company there (24 characters; it starts as "<your name>'s Works"). Picking its colour is not built yet.
- **The trait, with points:** for each kind of part (machine gun, laser, missile, torpedo and charge launchers, mining laser, cargo module, scanner), each trait can be set from −3 to +3 steps. Strengths cost points and weaknesses pay them back, and each kind's points must net to zero (or to a bonus, which the Legend can give later). Steps:
  - damage ±4%, rounds ±8%, energy draw ∓5%, lock time ∓5%, cutting rate ±5%, hold ±3%, scanner reach ±10%, top speed ±1%;
  - one more or one fewer missile, torpedo or charge per launcher, at 2 points a step.
  - The first shape is free; reshaping costs 1,500 cr (to the Compact) and reshapes every part of your brand you have, fitted or stored. Renaming is free.
- **Built at your Depot's or Station's workshop,** a standard part comes out as your brand's ("Kestrel Works machine gun"), with your trait, and sells on your market like any maker's. A Lair's workshop and other stations' still build standard parts. Fitted, a brand part works through the makers' trait code (stage 7), so a brand is a shape and not a free gain.
- **Items:** four fixed brand slots per galaxy (one for each pilot), `bp<N>_<kind>`, with the standard part's recipe, so the ledger is untouched. Their name and trait are read live from `S.brands`.
- **Test:** `brand.py`.

### The strategic map zooms in; escort and patrol orders (3 Nov 2026)
- **New file `16zh_zoom.js`.** The galaxy map (M) **zooms into the selected system**: the whole map becomes its sector view, live when the system is loaded and from your intel otherwise. Your capitals, your crews, you, any leader or the Dread Pirate there, and the station are named. Zoom in with the side panel's **Zoom in** button, a double click on a system or the mouse wheel. Zoom out the same way, or with the **◀ Galaxy** box.
- **Two new orders for your capital ships**, under Patrols and escorts in the side panel:
  - **Patrol:** it sweeps the selected system and its neighbours (not the powers' home systems, the freeports or the Wrack), two minutes in each, round and round.
  - **Escort me:** it follows you from system to system (in multiplayer, whoever gave the order).
  - Guard here and Come here clear either.
- **Fix:** a contractor's capitals now take their owner's own yard as their base. The base lookup assumed a sworn pilot, and an unsworn pilot's capital broke the capital tick.
- **Test:** `zoom.py`.

### The smaller items (3 Nov 2026)
- **New file `16zi_small.js`.**
- **Beacon rigs and limpet racks are fitted parts** (utility slots, scout hulls only, built at any workshop, stocked at the freeports and at Ostrova's core).
  - A beacon rig holds one beacon device a grade, and a limpet rack one limpet a grade. Both are restocked whenever you dock.
  - With no rig you can't flip beacons, and with no rack you carry no limpets.
  - Scouts get a third utility slot and the Advanced Scout a fourth. A new pilot's Scout comes with a scanner, a rig and a rack; an Advanced Scout adds a landing kit.
- **Comets and derelicts sold as intel to the Compact:**
  - Fly within 2.5 km of one (3.5 km with a scanner) to log it.
  - Sell the find at any freeport while it lasts, from the dock's Jobs list. A comet pays 3 cr a tonne of its ore (at least 150); a derelict pays a fifth of its cargo's value (at least 120).
  - You can still work it yourself.
- **Embargo contraband by origin:**
  - Goods bought at a power's market carry its origin, a tag like the stolen tag that shrinks as the goods leave your hold and vault.
  - While two powers have an embargo running, each one's goods are contraband in the other's space: Heavy heat (30) if a scan finds them.
- **The Rift Shard as a wild card:**
  - At a workshop, a Rift Shard stands in for one missing component of a recipe. The rift pulls that component's makings out of the outer drift, so it only works while the drift holds them, and the shard's Riftstone goes into the drift; the ledger stays exact.
  - Fed into a part's upgrade (Loadout → Rift Shards), it leaves the part a random trait: a strength 65% of the time (one or two steps of the brand table), a one-step weakness otherwise. Taking the part out or changing hulls loses the trait.
- **Tests:** `smallitems.py`. `intel.py` and `limpet.py` now fit a rig and a rack to their scouts.

### Proposal: the graphical market, the Loadout screen and the Hangar (mockups, 3 Nov 2026, being reviewed)
Three new screens on the "Driftgate Beyond screens" canvas (https://claude.ai/artifact/J1zRwXEc74WSmS59L2fjbP), bottom row. They replace the parked graphical-market sketch.
- **Docked · Trade (graphical market).** Tiles grouped as Ore, Components, Weapons, Utility parts and Payload, with a filter for each.
  - Each tile has an icon, the price, a stock meter, and a ▲ (wanted here) or ▼ (glut) mark. Your hold shows as a coloured bar.
  - Picking a tile opens a detail panel: buy, sell and galaxy-average prices, a 30-minute price graph, a quantity slider with Buy and Sell totals, and the best places to sell from your scans.
  - **Icons by kind (user, 3 Nov):** ore a hexagon, components a square, weapons a dart, utility parts a plus, missiles a rocket, charges an octagon.
  - **Colours (user, 3 Nov):**
    - Ores keep their colours.
    - Components take the colour of the ore they use most (by raw units: Alloy Plate and Crystal Lattice Ferrite tan; Conduit, Flux Coil, Depot Frame and Calibration Matrix Cuprite copper).
    - Weapons are reds, utility parts cyans, and payload magentas.
    - Open question: count by value instead, which would make Crystal Lattice and Resonance Core Xenocrystal violet and Flux Coil Iridium blue.
- **Docked · Ship → Loadout.** A top-down schematic of the hull with every weapon and utility slot labelled, its part and its grade as pips. Clicking a slot shows:
  - its trait (a maker's, your brand's, or a Rift Shard's);
  - the next upgrade, with component chips in red where you're short, the fee, and Upgrade or Upgrade with a Rift Shard;
  - Take out → hangar or hold;
  - Fit instead: parts that fit, tagged with where they are (hangar, hold, or the market with its price).

  **Systems** (Drive, Reactor, Shield, Armour) are clickable too, and show:
  - the tier and what the next one gives (e.g. top speed 236 → 262 m/s);
  - the components it needs, with what you have;
  - a "Missing:" line;
  - Upgrade, greyed out until you have everything;
  - Buy what's missing, with its total, linking to the market.
- **Docked · Ship → Hangar** (the per-station Vault, renamed and given a sub-tab). It holds your cargo and the ships you aren't flying, and has three columns:
  - **Hangar:** berthed ships as cards (class, slots fitted, tonnes aboard, hull %) above the cargo list;
  - **Hold:** with a capacity bar;
  - **Ship:** the slots of the ship you're flying.

  What you can do there:
  - Move 1, 10 or all between hangar and hold.
  - **Fit to ship** puts a part in a slot and sends whatever was there to the hangar.
  - Taking a part out returns its upgrade components with it.
  - **Fly this ship** swaps ships: each keeps its own parts and hold, and the one you were flying is berthed.
  - **Sell hull** takes the parts and hold off into the hangar first.
  - Free hulls are never berthed.
  - Proposal: 2 berths at a freeport or a power's station, more at your own Depot or Station with its hangar building.

### War check after the 3 Nov features (neutral leaders, 600 galaxies, 16 h)
Varkesh 28%, Brood 24%, Ostrova 24%, Halcyon 23%, nobody 1%. Before these features it was Ostrova 28, Halcyon 27, Varkesh 24, Brood 20. The spread is a little wider than run-to-run noise (about ±2 to 3 points); the Brood are 4 points over the 20% target. No retune yet.
- **Retune (user, 3 Nov):** ease Varkesh's edge in unwatched battles a little: `FACTIONS.varkesh.tough` 1.14 → 1.10. War check (neutral leaders, 600 galaxies, 16 h): Halcyon 30%, Ostrova 25%, Varkesh 23%, Brood 21%, nobody 1%. Varkesh fell 5 points and the Brood 3; Halcyon rose 7, more than the change explains on its own, so part of that is run-to-run noise.
- **Second step (user, 3 Nov):** split the difference: `tough` 1.12, and cut Halcyon's Trade Charter if Halcyon stays high. War check (neutral leaders, 600 galaxies, 16 h): **Ostrova 26%, Varkesh 26%, Halcyon 25%, Brood 23%, nobody 1%**. The three powers are level, so the Trade Charter stays as it is. The Brood are 3 points over their 20%, near the edge of run-to-run noise.

### Proposal: the minimal pass over every screen (mockups, 3 Nov 2026, being reviewed)
The canvas's "Minimal pass" rows hold a minimal version of every screen; the originals stay beside them.
- **Screens:** title, Company (Allegiance, Holdings, Economy, Jobs, Black market), docked (Jobs, Trade, Ship → Loadout, Ship → Hangar), and the sector map.
- **The pattern:**
  - a quiet list on the left (icon, name, one status as a dot and a word, one number);
  - everything else for the picked row in a detail panel on the right;
  - no boxes, one amber button per screen, secondary actions as text links;
  - alert lines only when something needs you;
  - levels as pips, forms as numbered steps;
  - a slim header (company or station, credits, rating or hold, upkeep).
- **Tabs merged:** the Company screen's Post jobs and Faction jobs become one Jobs tab (All · Your pilots · Posted out · Faction jobs); the Ship tab's Systems sub-tab folds into Loadout.
- **Checked against the originals:** each one's buttons, inputs and readouts were listed and placed in the minimal version.
- **Kind icons for jobs:** mine is an ore hexagon, haul a component square, guard a shield, intel a triangle, hunt a dart.
- **User review (3 Nov):**
  - Loadout and Hangar keep their original (fuller) layouts; their minimal versions were dropped.
  - Title screen: the order is Callsign, Legend (collapsed), Freeport and Ship (both expanded). On the right, a picture of the chosen freeport with the chosen ship; in the game these are the live 3D models.

### Screens pass: as built, part 1 (3 Nov 2026)
- **Goods icons and colours** (`16zj_icons.js`): every good in the dock's lists, chips and swatches carries the agreed shape and colour, through `gIcon(k)`.
  - Components take the colour of the most valuable ore in them.
  - Weapons are reds, utility parts yellows, payload magentas, cash-only contraband a violet diamond.
- **The Hangar** (`16zk_hangar.js`): the Vault is called the Hangar everywhere it shows, and one Ship → Hangar sub-tab holds both:
  - **ships berthed here:** Fly this ship, Sell, upgrade while berthed, and berth the one you're flying;
  - your cargo (store and load);
  - ships berthed elsewhere;
  - your other hangars, with **Ship here**.

  The rules:
  - Berths are per station: 2 at a freeport or a power's station; at your own Depot, one more per hangar module; at your own Station, two more with a hangar building.
  - Old saves' berthed ships are placed where you next dock.
  - Contractors can use Ship here: a Compact freighter (`haulSend('neutral', …)`) brings up to 120 t for 60 cr + 2 cr a tonne a jump, and can be raided.
- **Loadout** (`16zl_loadout2.js`): Ship → Loadout (was Systems) is the agreed screen. It shows:
  - a top-down schematic (fighter, miner or hauler outline) with every weapon and utility slot around it, each showing its part icon, name and grade pips;
  - the systems strip below, with pips and Aurora ✦;
  - Rearm and the payload counts.

  Picking a part opens its panel:
  - the trait (including a Rift Shard's);
  - the next upgrade, with chips showing what you have, a "Missing:" line and the fee;
  - Upgrade and With a Rift Shard;
  - Buy what's missing (to the market);
  - Take out;
  - every part that fits, with where it is or its price ("Fit" / "Buy & fit").

  Picking a system shows its full old Systems row (grade, components, fee, To Grade, Attune, variants) and the upgrade note. The Shipyard tab's old loadout block is gone, since it lives here now.
- **Graphical market** (`16zm_market2.js`): Trade → Market shows the agreed design:
  - tiles in groups (Ore, Components, Weapons, Utility parts, Payload), with a filter for each;
  - each tile has an icon, the buy price, a ▲ / ▼ mark, a stock meter, the stock and what you hold;
  - your hold as a coloured bar.

  Picking a tile opens the detail panel:
  - buy, sell and galaxy-average prices (the average from your scans);
  - the price here as you've watched it (one reading a minute while docked);
  - a quantity slider, Buy and Sell;
  - Fill hold, Sell all, Store all and Load to hold;
  - the best places to sell, from your scans.

  "Table" switches back to the old list, with every button it had. Claim Beacons, where sold, also have their own line under the tiles (Buy 1, Load, the hull fix).. The makers' works and salvage sales stay underneath.

### Screens pass: as built, part 2: the Company screen (3 Nov 2026)
- **Files:** `16zo_company2.js` (the header and Holdings), `16zp_company3.js` (Allegiance, Economy, Jobs, Black market). CSS `.co*` in `page.html`.
- **Every tab is a list on the left and the picked row's detail on the right**, with a few views across the top. **Full view** on every tab shows the old screen with everything on it, so no control is lost (checked against the old screens).
- **Header:** the company's name (your brand's, or your faction's once declared), then credits · Rating · upkeep an hour · bases. The tab once called Post jobs is now **Jobs**.
- **Holdings:**
  - Alert lines appear only when they apply: you can declare a faction; a base is under a strike, with **Send a guard**. Send a guard sets one of that depot's crews to guarding, or, if it has none, posts a Guard job at Medium pay.
  - The rows show your Stations, Depots and Lairs: icon, name, kind and level, level pips, and one status (holds the system, market open, under threat, damaged, hidden, found).
  - The footer shows systems held, AI pilots, capitals, + Build a Lair here (or why not), and + Build a Depot here.
  - The detail panel holds a base's controls:
    - **Lair:** To level 2, Upgrade to a Depot.
    - **Depot:** modules, Upgrade to a Station with cost chips.
    - **Station:** the five building plots, the next building with cost chips and a button per building, capital ships (Escort, Destroyer, Carrier) with their slips.
    - Links go to Economy (with that base picked) and to Jobs.
  - Your brand stays underneath.
- **Allegiance:**
  - Rating (with what it opens), your faction, the declare banner and proposals (Accept / Pay, Decline / Refuse) sit on top.
  - Views: **Your standing** (the three powers, the Compact and the Unbound: band, bar, leader, heat if not Cool), **Between the powers** (the grid; pick a pair), **Chronicle**.
  - A power's detail shows: what your standing opens, the next band up and down, heat, its leader (traits, where it is), its perks, its relations with the other two, and **what moved the picked pair** (the last entries of the relations log).
  - The Unbound's detail shows the Dread Pirate, its traits, its bounty on you and its kills.
- **Economy:**
  - Views: Hour or 3 hours.
  - Rows: the company and each base, with net, a spark of the period in twelve steps, the trend against the period before, and the latest reason. A line flags the worst losing base.
  - Detail: the lines (sales, wages, running costs and so on), the latest five entries, and **your market at that base** (Sell / Buy / Off per good, as before).
  - The mockup's company credit history and goods-used panel aren't built: the game keeps no such record yet.
- **Jobs:**
  - Views: All, Your pilots (each crew: job, base, wage), Posted out (each posted job: state, fee).
  - **+ Hire a pilot** opens a form: base, then hull with price.
  - **+ Post a job** opens a form: What, Where (which depot), the good and amount, Pay (Low, Medium, Fast with fee and wait), Post.
  - A crew's detail has its job (Mining, Hauling, Guarding, Idle) and Let go. A posted job's detail has its status, fee and Withdraw.
  - The mockup's "Faction jobs" view isn't here: the powers' jobs stay on the docked Jobs board, since they're offered at a station.
- **Black market:**
  - Your heat with each power sits on top.
  - Views: Offers and Runs, with a heat filter and **+ Request work** (fixers, quiet buyers, the Tankard once met).
  - An offer's detail: heat if caught (and with whom), pay, from and to, then **who runs it**: you, each crew with its hold and its chance of being caught, or a Compact contractor (your 25% cut). Deals show Buy, Sell or Set course.
  - A run's detail: its progress or result, and the pay.
- **Phone width:** the Company sheet fits the screen; its tabs scroll sideways, and the list sits above the detail.
- **Tests:** `company2.py` is new. `blackmarket.py`, `declare.py` and `stations.py` read the new screens.

### Screens pass: the docked Jobs board (3 Nov 2026)
- **File:** `16zq_jobs2.js`. It shows the same jobs, filters, sort and buttons as before, drawn quietly.
- **Filters and sort:** the kinds are words with counts (All, Haul, Mine, Fight, Scout), with "Sort: Pay ▾" (or Distance) beside them.
- **Each row:** an icon for its kind (square haul, hexagon mine, dart fight, triangle scout, shield campaign) in the issuer's colour; the title; the issuer and the job's line; where (with ✓ yours); and the pay.
- **The panel:**
  - kind and where, the title;
  - who issues it and your standing with them;
  - Where, Pays, Paid by;
  - the job's own notes and buttons.
- **At a freeport,** a line says whose jobs you can't see because your standing is too low.
- **What stays:** the intel bar above and the convoy section below.
- **Tests:** `jobs.py`, `ship.py` and `hull_tags.py` read the new classes (`.jrow2`, `.jdet2`).

### Screens pass: the map's side panel (3 Nov 2026)
- **File:** `16zr_mapside.js`.
- **For the picked system, on top:**
  - its name (live or from intel), Zoom in ▸ / ◀ Galaxy;
  - who holds it, its station and your base there, and how far it is;
  - Set course / Clear course;
  - a threat line when a strike is coming. On your base, **Guards intercept** sets that base's crews to guarding (or posts a Guard job).
- **Your forces:** your crews based in this system and all your capitals, each with a tick box and its status (mining, hauling, guarding; here, on its way, N jumps away, patrolling, escorting).
- **Orders for the ticked forces:**
  - crews: Mine here, Haul home, Guard the depot, Idle;
  - capitals: Come here, Guard here, Patrol around here, Escort me.
- **What stays:** the sector picture (hidden while the map itself is zoomed in). Everything the panel showed before is under **More ▾**: galaxy control, operations, the capital fleet, vaults, recent news, pilots online, New pilot.
- The mockup's "Move to…" (click the map to place a crew) isn't built: crews don't take map positions.

### Screens pass: the title screen (3 Nov 2026)
- **File:** `16zs_start2.js`. The layout has two columns, built from the existing sheet, so every id, card and button is unchanged.
- **Left column:** the title, then the steps:
  1. Callsign.
  2. **Legend**, collapsed. Its header shows your level and start package; open, it shows the perk choices (the next locked level shown greyed), the medium-hull choice, any Conqueror's spoils, and a link to the Leaderboard.
  3. Freeport, 4 Role and 5 Ship, open. Each header shows what's picked and folds its cards away.

  Play with friends and the controls line follow.
- **Right column:** a picture of the freeport and the ship you picked, drawn by the start screen's small renderer from their real models, with their names underneath. The freeports share one station model, so the station looks the same for each; the ship changes with the design line.
- On narrow screens the picture is hidden.
- **Ship offers only the hulls you can start in** (user, 3 Nov). You never start with credits, so the hulls you'd have to buy (with their prices) are no longer listed: each role shows its starter hull, and the Unbound their two. The Legend medium-hull perk still swaps in its hull at launch.

### The developer panel without a faction (Ctrl+Alt+D, 3 Nov 2026)
- **New file `16zn_dev.js`.**
- Every power can now be picked as the enemy side, along with the Unbound and the Brood.
- The friendly heavy bomber flies as yours, and "Vault" reads Hangar.
- **A new Beyond section:**
  - standing +25 or −25 with a chosen power or the Compact;
  - Contractor Rating +1;
  - clear heat, or heat +40 with every power;
  - Lair, Depot, Station and building kits (into your hangar when docked, your hold in flight);
  - an AI crew at your depot;
  - Rift Shards and contraband;
  - the Dread Pirate spawned in this system;
  - Scrapheart knocked out;
  - ten minutes of the galaxy run forward.
- Anything that makes goods moves the ledger baseline, and guests' requests run on the host.
- **Test:** `dev_beyond.py`.

### Your base's fees (agreed 3 Nov 2026)
- **The user's choices:** you set your own fees at a Depot or Station you own: **market prices, a services fee and a docking fee**. Each is a stepper between a minimum and a maximum, and all of them **start at the galaxy default**. Fees change **traffic only**: how many traders and pilots come, never your standing. No transit toll.
- **The settings, per base:**

  | Fee | Range | Default | Who pays it |
  |---|---|---|---|
  | Your sell price | 80–130% of the market price | 100% | the powers' traders buying from you |
  | Your buy offer | 80–120% of the market price | 100% | you, to the traders selling to you |
  | Services | 50–200% of the standard rate | 100% | visiting pilots who repair and rearm |
  | Docking | 0–100 cr a visit | 0 cr | every trader and visiting pilot, as they dock |

- **How traffic answers:**
  - **Traders** (the powers that deal with you, every minute or so):
    - visits fall 7% for every 10 cr of docking fee (0 cr: as now; 100 cr: under a third as often). At about 25 cr the fee's income makes up for the trade it turns away; above that it pays only when your store is thin;
    - each visit's lot shrinks 22% per 10% of price above the default (130%: about a third), and grows the same below it, up to 1.4 times;
    - your buy offer works the other way round;
    - each visit pays the docking fee from its power's treasury.
  - **Visiting pilots** (new): Compact contractors and the pilots of the powers that deal with you stop now and then to repair and rearm, about six an hour at the defaults (a Station draws half as many again). Each pays 60–180 cr of services (scaled by your services fee) and the docking fee, from the Compact's or its power's treasury.
    - Every 10% of services fee above the default sends 8% fewer of them, down to a fifth at 200%; every 10% below draws 8% more, up to 1.4 times at 50%.
    - The docking fee thins them as it does traders.
  - **Takers for the jobs you post** at that base wait longer the higher its docking fee (twice as long at 100 cr).
  - The trade-off: steep prices earn more on each unit but sell far fewer, so they suit a base with little to sell. Cheap prices move a big store fast.
- **Where it shows:**
  - **Holdings,** in a base's detail: **Fees**, with − and + for each fee, its default, and what it does to traffic now ("traders: about 40 visits an hour, 60 at the defaults").
  - **Economy,** with lines for docking and services income.
  - **The map's side panel** shows any contractor base's fees.
- **Ledger:** only credits move: from the powers' and the Compact's treasuries to you, as trade already does.
- **Not yet:** other players docking at your base in multiplayer. A visitor's view of someone else's base (its market at the owner's prices, repairs at the owner's services fee, the docking fee as you dock) doesn't exist yet; until it does, the fees reach other players only through the AI traffic above.

### The cargo scanner (agreed 3 Nov 2026)
- **The user's choices:**
  - Every Unbound hull has one built in; anyone else fits it as a utility part.
  - The reading is rough at once and exact once the scan completes.
  - The scanned ship notices, with consequences.
- **The part:** Cargo scanner (`pt_cscan`), made from a Copper Wire and a Flux Coil. Every freeport stocks three in a new galaxy and Scrapheart three.
  - **Unbound hulls** scan at grade 1 without it, or at the fitted part's grade if better.
  - **Range:** 1,200 m, plus 150 m a grade.
  - **Scan time:** 4 s, half a second less a grade (at least 2 s).
- **Using it:** target a ship within range; the scan runs while you hold it in range (moving out pauses it, a new target starts again).
  - **At once:** the kinds of goods (ore, components, parts, payload, contraband), roughly how many tonnes, and roughly what they're worth.
  - **When the scan completes:** the exact manifest, each good with its icon and tonnes, and its value.
  - Both show in the target panel.
  - **What it reads:** a freighter's or trader's hold, a capital's store, a pilot's hold.
  - **Hidden cargo containers** keep their share out of every reading (the contraband first), as they do from customs.
  - Each ship's reading stays with it while it's in the system.
- **Noticing:**
  - **Pilots** (other players) are warned that someone is scanning their cargo.
  - **AI freighters, traders and miners** notice half the time; one that notices breaks off and runs at full burn.
  - **Heat:** completing a scan of a power's ship inside that power's own space adds a little heat with it (+6). Elsewhere scanning is nobody's business.
- **Not yet:** guests in multiplayer, whose game doesn't hold other ships' cargo; their scanner shows nothing until the host relays readings.

### The three freeports, told apart (3 Nov 2026)
- **The user's ask:** a slightly altered station for each freeport, some distinction but not much.
- All three keep the approved freeport design (`freeport(v)` in `tools/previews/beyond_faction_stations.py`, `FREEPORT_V`):
  - **Mirrorwater:** the approved design as it was: four docking arms.
  - **Coldwater Drift:** three longer docking arms, and a lit ring round its waist on three spokes.
  - **Ember Wake:** four arms swept down like a crown, and a short beacon mast above the upper welcome gate.
- **Models:** `by_freeport`, `by_freeport_cw` and `by_freeport_ew`, chosen by the station's system (`FP_MDL` in `16z_models.js`). All three are the same overall size.
- **Docking ports:** each freeport's ports are now set at the heads of its docking arms (`PTS` in `build_models.py`), not found from the silhouette. So Coldwater has three ports.
- **The title screen's picture** now shows the real freeport model for the picked port (it showed the generic station before).

### The galaxy map's names, readable (3 Nov 2026)
- **The user's report:** names on the galaxy map overlapped or were hidden under other systems.
- **Room for every system:** systems that sat too close are eased apart on the map (`mapSpread`). Each pair keeps both radii plus a gap clear, and each system stays near its old place, with the same gates. Clicks, routes and overlays all use the same positions (`mapXY`).
- **Names drawn last, each placed where it fits** (`mapLabels`):
  - The candidate spots are below its system, above, right, left, then the diagonals. A name takes the first spot that clears every system and every name already placed, and sits nearer its own system than any other.
  - Each name is drawn over a dark halo, so gate lines and rings don't cut through it.
  - If no spot near its system is free, the name goes a little further out with a thin line to its system.
  - A freeport's "FREEPORT" tag sits on the line above its name.
- **Smaller windows:** systems and names scale down with the map, to about two thirds of their size at most.

### Claim Beacons are fitted parts (3 Nov 2026)
- **The user's report:**
  - You couldn't equip or buy a power's Claim Beacon: the new Market tiles had dropped the "Claim Beacons" section.
  - Asked for: (a) a beacon takes a utility slot; (b) you fit it on the Loadout screen; (c) you buy a specific power's beacon, in its colour.
- **As built** (`16zv_claimfit.js`):
  - **The beacon is a utility part:** a power's Claim Beacon (Halcyon, Varkesh, Ostrova) carries that power's colour on the utility icon. It fits fighters and bombers only (as before), it has no grades, and it claims only while fitted (in a hold it's just cargo).
  - **Fitting:** on the Loadout, pick a utility slot. Its "Fit instead" list offers the beacons you have, and "Buy & fit" for each power this station sells beacons for (every power at a freeport, its own at a power's station), at 450 cr.
  - **Claiming:** hold a fitted beacon in an unclaimed or breached outpost's ring (as before). The claim uses the beacon up and leaves the slot empty: fit your landing kit back.
  - **Buying:** the Market's tiles list the Claim Beacons sold here, one per power, with what you have and which is fitted. The job board's claim jobs say to fit one.
- **Tests:** `claimfit.py`.

### Docking ports you can see (3 Nov 2026)
- **The user's report:** the docking ports on stations and depots weren't obvious.
- **In flight** (`16zw_ports.js`), within 4 km of a station, depot or outpost, every docking port is marked:
  - a ring on the port, with a pulse spreading out from it;
  - a line of approach lights running out from the port the way you come in, chasing inward;
  - **green** where you may dock, **red** where you're refused.
- **The port nearest you is labelled:** DOCK and its distance, then "DOCK · PRESS E" once you're in range, or NO DOCKING.
- A base without arm ports (you set down over its hangar) shows one port above it.
- The marks fade in over the last 800 m of that 4 km and hide while you're docking.

### The free Light Miner's fit (3 Nov 2026)
- **The user's ask:** free miners start with a mining laser, not a combat weapon.
- The Light Miner (Wren, Pick, Glim) now comes with a **mining laser and its charge launcher** (`HULL_SLOTS.skiff`). The machine gun is gone.
- A new pilot's mining tool is the laser, so F works the ring of a targeted rock at once; switch to charges as before.
- It has no combat weapon now, so its guard drones do the fighting. A gun can be fitted in either slot on the Loadout.
- Pilots who already fly one keep their current fit.

### The mining laser, made to work in play (3 Nov 2026)
- **The user's report:** the mining laser didn't seem to work.
- **What was wrong:** it did cut, but only when the beam sat on the rock's thin ring, which you rarely see from range. Even then it took six seconds a tonne on a Light Miner, and it said nothing while it worked.
- **The fixes** (`16zx_mlaser.js`):
  - **The beam finds the ring:** when the beam strikes the rock off the ring and the nearest ring point facing you is within 25 degrees of your nose and in range (380 m), it swings onto the ring and cuts there. Aiming at the rock is enough.
  - **About twice as fast:** a tonne every three seconds on a Light Miner (Medium 2 s, Heavy 1.5 s).
  - **On screen:** a ring at the beam's spot fills as the next tonne comes free, with "CUTTING CUPRITE · 84 t LEFT", and each tonne that lands is called out with your hold ("+1 t Cuprite · hold 12 / 30 t").
  - **Instructions:** the rock's target panel explains the laser when it's your tool (or that the ring is broken). The key hint reads "hold: cut the ring".
- Charges are unchanged: faster and riskier, and a blast still breaks a rock's ring for good.

### Charges aim with the standard sight (3 Nov 2026)
- **The user's ask:** the charge launcher should use the standard gun or laser sight for aiming, not a third reticle in an odd place.
- **Why it sat oddly:** the old reticle was drawn where the charge would land on the rock, close in. Seen from the chase camera above and behind the ship, that point sits well below the sight, which is drawn 900 m out along the nose.
- **Now:**
  - Charges aim with the standard sight. A charge flies from the launcher to the point on the targeted rock under the sight, where the camera's line through the sight meets the rock. So it lands where the sight shows (in a check, 4 m from the aim point).
  - The separate charge reticle and its flight line are gone. The standard sight takes the charge's colour (green on a fault point, amber near one, red off, grey out of range) and its label underneath ("ON POINT · FIRE (F)", "OFF · 33 M", "OUT OF RANGE", "MISSES THE ROCK").
  - Without a rock under the sight, a charge flies along the nose as before.
- **In multiplayer,** a guest sends its aim point with the shot, and the host fires the charge at it.
- **Unchanged:** the fault-point rings on the rock and the dashed line to the nearest one.

### The mining training course (3 Nov 2026)
- **The user's ask:** fix the mining training course.
- **The cause:** the course itself completes in play. Its test was stuck at "Back to the freeport": it put the ship back beside the station every quarter second, even while the docking run was under way, and gave the slow headless browser only ten seconds to dock. The test now leaves the docking run alone and allows it thirty seconds. All 13 steps pass, and the ledger is exact.
- **Two lessons now match today's changes:**
  - **The laser:** point at the rock and hold F; the beam finds the ring, and its spot fills as each tonne comes free.
  - **Charges:** put the sight on a fault point until it turns green and reads ON POINT.

### The mining laser: one beam, and a reward for precision (3 Nov 2026)
- **The user's report:** the scoop beam showed at the same time as the mining laser. Also asked for a faster yield when the laser is held on the ring.
- **One beam:** the laser no longer marks the rock as being scooped (`p.mlRock` in place of `p.mining`), so the old drill/scoop beam isn't drawn beside it. The scoop beam still shows when you scoop chunks and clouds.
- **Precision pays:**
  - Held right on the ring yourself, the laser cuts **twice as fast**: "ON THE RING · ×2", about 0.7 t a second on a Light Miner.
  - Swung onto the ring by the beam's 25° help, it cuts at the base rate ("CUTTING").
  - In a check of 20 seconds each: 13 t on the ring, 6 t assisted.

### Market detail: "Galaxy" is the sell average (3 Nov 2026)
- **The user's question:** is the galaxy average a buy or a sell price?
- **The answer:** it's the **sell** price, the average of what the stations you've scanned would pay you. The label now reads **Galaxy sell**, with a tooltip saying so.
- The sparkline is this station's sell price while you've watched it, and its caption now says so.

### Claim Beacons say they're single use (3 Nov 2026)
- **The user's ask:** note that a Claim Beacon is a single-use item.
- Everywhere it's described, it now reads **Single use (ammo: 1)**: the part's description and trait line on the Loadout, the Buy & fit rows, and the Market's beacon tiles and their heading.

### Every item has a maker (3 Nov 2026)
- **The user's ask:** every item except ore and parts you craft yourself should be tied to a corporation.
- **The user's choices:**
  - Markets sell only corporations' parts.
  - Components and payload carry a made-by label, with no traits.
- **As built** (`16zy_corps.js`):
  - **Parts:**
    - Each power's core station and each freeport sells only its two makers' parts.
    - Each maker now has a **plain line** (no trait, "standard") beside its trait parts, for every slot it covers.
    - A slot no local maker covered goes to one of them: weapons and mining tools to the arms maker, utility parts to the other. Every slot is covered at every maker's market.
    - The lines: Halcyon (Corvane Yards, Brightline Emitters), Varkesh (Hold Foundry, Marchgun Ordnance), Ostrova (Spirewright, Archive Dynamics), Mirrorwater (Quicksilver Hullworks, Mirrorwater Arms), Coldwater (Coldwater Prospecting, Coldwater Refit), Ember Wake (Ember Wake Drives, Wakefire Munitions).
    - The works build the whole line, plain parts included.
    - Standard parts already on those markets became the local makers' plain parts (same recipe, so the ledger is unchanged; done once for existing galaxies).
    - The unbranded standard part now only comes from a workshop ("Unbranded: built in a workshop, by you or another pilot"). Your own brand's parts stay yours.
  - **Components and payload:** the Market's detail shows who makes them, a power's or freeport's first maker for components and its second for payload ("Made by Quicksilver Hullworks · here"), with the maker in the tile's tooltip. They stay one item each in the economy.
- **Left out:** ore, contraband, Scrapheart's salvage, and your own depots' and stations' markets (your own brand covers those).
- **Tests:** `corps.py`.

### Claim messages and the Ship tab (3 Nov 2026)
- **The user's report:** an outpost's ring said you needed a Claim Beacon in your hold, with one fitted on the Loadout.
- **The fix:** the ring's messages now match fitted beacons (`cbWhy`):
  - a beacon in the hold but not fitted: fit it on the Loadout;
  - a fitted beacon on a hull that can't carry one: fighters and bombers only;
  - a fitted beacon for the power that already holds the outpost: it's already theirs;
  - no beacon at all: buy one and fit it.
- **The Ship tab opens on the Loadout** (user, 3 Nov). Loadout leads the Ship group (Loadout, Shipyard, Hangar, Refits), and the Ship tab always opens there, whatever sub-tab you used last.

### Docking ports get their art; turrets keep off them (3 Nov 2026)
- **The user's report:** docking ports needed their art, and a docking at Ember Wake seemed to go into a turret.
- **Art** (`16zw_ports.js`): every port of a station, depot or outpost now has a docking collar in the world:
  - a hull-grey ring with a dark lip;
  - a green lit ring inside it;
  - four amber guide lights round it;
  - two lines of green approach lights running 70 m out from it.

  It's tinted red where you may not dock. The flight markers stay as well.
- **Turrets:** a station's turrets went on the outermost hull point in each turret's direction, which on the freeports is often a docking arm's head. They now take the outermost point at least 38% of the station's size (and never under 55 m) away from every port, so no turret sits on or beside a docking port. Measured nearest turret to any port: depots 55–64 m, cores 65–74 m, freeports 80 m, Scrapheart 95 m.

### A lived-in market at launch (3 Nov 2026)
- **The user's ask:** randomize the markets at the start of a galaxy, so that parts from various makers are spread around. Local makers should have more; you don't need one piece from every maker at each station, just a good random selection.
- **As built:** each new galaxy's markets get a random selection of makers' parts in place of one of everything.
  - A lot is from the local makers three times in four, and local lots are bigger (1–3, against 1–2 for imports). Other makers' parts turn up as imports.
  - **Lots:** freeports get 8 to 12, the powers' core stations 7 to 10, and their other stations (which sold no parts before) 2 to 4.
  - A freeport or core station always has at least one gun, laser, missile launcher, landing kit and cargo module.
  - In a sample galaxy: freeports had 10–11 kinds from 3–4 makers; cores 8–9 kinds from 4–6 makers; other power stations 2–3 kinds.
- **Over time:** the makers' works restock their own lines as before, so a station's local range fills out as the galaxy runs.
- Existing galaxies keep their markets.

### The leaders' news box (3 Nov 2026)
- **The user's ask:** a news report on top of the ticker showing each faction leader's latest position or declaration, keeping up to three before they fade.
- **What goes in** (`16zz_news.js`, a wrapper on the chronicle):
  - every chronicle line a leader speaks, which opens with their title and name: border demands, embargoes, trade pacts, aid, alliance offers and refusals, reprisals, declarations of war, ceasefire offers, betrayals;
  - the galaxy's big turns: alliances, ceasefires, successions;
  - the Dread Pirate's fortunes (shot down, taking the hat), under the Unbound.
  - Relations simply drifting between bands ("now Cool") and a power ignoring a demand stay in the Recent ticker only.
- **The box** (`#hNews`, above Recent): titled News, newest first, at most three items. Each has its faction's colour on the left, the faction and the speaker's title and name in small capitals above, and the declaration under it (two lines at most; the big turns in bold).
- **Fading:** each item stays three minutes of game time and fades over its last thirty seconds; a fourth pushes the oldest out. The box hides when empty.
- It shows every power's news whoever you serve: it's galactic news, not your own channel. The host keeps it in the state (`S.news`), so guests see the same box. On a phone it shows the newest two.
- **Test:** `news.py` (in the quick suite).

### Comms: Jobs here (designed and built 3 Nov 2026)
- **The user's question:** can Comms show the missions in the sector you're in? For example an escort job if you fly a fighter, or an ore request if you fly a miner.
- **What Comms does today:**
  - The Command page (I) offers escort me, guard me, build, distress and your capital ship's supply run.
  - Targeting a friendly ship offers guard, escort and "where are you bound?". Two jobs show up there only if you target the right ship: a friendly convoy freighter offers its escort contract, and a carrier offers its resupply run.
  - The Comms panel on screen lists up to three operations (O joins one), and a sworn pilot has command orders (P).
  - Nothing lists the jobs in your system. Contracts, ore requests, escorts and posted jobs are only on the docked Jobs board; a freeport request scrolls past in Recent and is gone.
- **The proposal: a "Jobs here" page in Comms.**
  - **Where it sits:** I opens Command as now, I again opens **Jobs here**, and I after that steps through the ships around you as before. The Comms panel's quick-keys line shows a count when there are any ("Jobs here: 3").
  - **What it lists:** the jobs located in this system, the ones the docked board marks "here", from the same board you'd see docked at this system's station, under the same rules about who hires you (your sworn power; a contractor needs Neutral or better). In a system with no station, or one that won't deal with you, it still lists what's happening here from the powers that hire you: convoys to escort or raid, operations, beacon missions, stations to claim, a carrier needing supplies.
  - **Only your hull's jobs** (the user's choice), by the same fit the board uses: a fighter sees Fight (convoy escorts and raids, operations, claims, the Dread Pirate's bounty), a miner Mine (ore contracts), a hauler Haul (contracts, freeport requests to this freeport, posted jobs, blockade runs into this system), a scout Scout (beacon missions, intel). The signature hulls see their two kinds (Vesper scout and fight, Bombard mine and fight, Gannet haul and fight). Other jobs are hidden, with one line saying how many ("3 jobs for other ships: on the station's board"). Best pay first.
  - **Each line:** the job, its pay, and a word on what it takes ("deliver at the freeport", "fly with it", "kill the freighter"). Keys 1–3 pick a job; 4 is "More ▸" when there are more than four.
  - **Picking a job** does what Select job does on the board: it signs you on and tracks it, with its marker and course. A convoy escort signs you on to the convoy at once, an operation joins you to it, and a beacon mission or claim marks its target.
  - **What still needs the dock:** handing over goods (contract and posted-job deliveries go into a store), buying goods or a beacon for a job, and the jobs that start with cargo loaded at the dock (smuggling and black-market runs) or a purchase (the Dread Pirate rumour, selling a find). Delivery jobs show "deliver at the dock"; the dock-only jobs stay off the page, with one line: "2 more on the station's board: dock to see them".
  - **This system only** (the user's choice). **Nothing here:** "No jobs for your ship in this system right now", and the nearest system that has some, with its jumps.
  - **The Unbound** (the user's choice): their page is **Prey here**: the convoys and freighters of the powers in this system worth taking, each with its side, where it's bound and its cargo (the rough or exact cargo-scanner reading if you have one, otherwise "unknown"), biggest haul first. Picking one targets it.
  - **Multiplayer:** as built, a guest's pick uses the messages the board and Comms already send (`job` for the tracked job and its issuer, `plan` for a campaign or side order, `cvesc` for an escort, run on the host inside `runAs`), so no new message was needed. It can only sign on, track, join or target; anything that moves goods stays a docked action.
  - **Training:** off.
- **Decided (user, 3 Nov 2026):** jobs that don't fit your hull are hidden; this system only; the Unbound get Prey here.
- **As built** (`16zza_cjobs.js`): the page reads the board's own job list (`jobsList`) for a board built for this system without docking. The same convoy offered by two issuers shows once, at the better pay. The quick-keys line in the Comms panel reads "I I Jobs here: 2" (or "Prey here"). Picking a convoy raid targets the freighter if it's in range of your sensors; picking an escort also points Comms at the freighter.
- **Test:** `comms_jobs.py` (in the quick suite): a fighter and a miner in the same freeport system see their own kinds first; picking an escort signs on, and picking a contract tracks it; jobs for other hulls and dock-only jobs stay off with their count line; an Unbound pilot sees Prey here with scanner readings; a guest's pick runs on the host; the ledger stays exact.

### Engine glows round over their nozzles (3 Nov 2026)
- **The user's report:** the engine glows on Varkesh ships didn't look rounded to match the circular nozzles they come out of.
- **Why:** an engine glow is a disc turned to face the camera. The chase camera sits behind and above, so the disc leaned forward into the hull. On the Varkesh hulls the nozzles sit recessed in square housings, and the housing cut the top of the glow off flat, leaving a D shape.
- **Now** (`engGlow` in `12_render.js`): the glow is pulled towards the camera by its own size, in proportion to how far behind the engine the camera sits. From behind it shows as a whole round glow over the nozzle (checked on the Fang, Halberd and Bulwark, and the Halcyon Swift is unchanged). From the side or the front it stays on the nozzle, so the hull still hides it as before. This applies to every ship.

### Smaller drones (3 Nov 2026)
- **The user's ask:** reduce the size of all drones.
- Guard drones (the Aegis, Ward and Halo, and the Brood's mite drones on its miners and haulers) were radius 9, three quarters of a light fighter (12). They are now radius 5, a little over half their old size, both as drawn and as a target (`CLASSES.drone.radius`). Their engine glows shrink with them.
- Limpets keep their own size (radius 5, set when they launch).

