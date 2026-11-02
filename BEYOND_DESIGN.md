# Driftgate Beyond: design

A new game in the Driftgate universe. This file holds its design as it is decided; DESIGN_NOTES.md is Driftgate 1's history up to the fork.

## Fork (Nov 2026)
- Forked from Driftgate 1 v255 with its full code, tools and tests.
- Own identity: browser storage keys `dgbeyond.*` (save `dgbeyond.save.v1`, legend, keys, audio, lore, aces, tips, multiplayer ids), multiplayer host ids `dgbeyond1-<code>-host`, relay topics `dgbeyond1/…`, tab channel `dgbeyond`, title "Driftgate Beyond", invite links to mbyrtus-maker.github.io/DriftgateBeyond/.

---

## Vision (first draft, 2 Nov 2026: for review, nothing here is agreed or built)

### In one paragraph
The war goes on, but you no longer fight in it as a soldier. You are an independent contractor with a starter hull and a few credits. You take work from whichever power will pay: the three factions, the freeports, and later other contractors. Corporations make everything on the market, some under the factions and some at the freeports. You build your own ships, equipment and stationworks from their parts. Contract by contract you become an outfit, then a company with its own stations, then a house with its own brand. In the end your company declares itself a faction and joins the war as a fourth contender for the galaxy.

### What carries over, what changes, what goes

| Keep from Driftgate 1 | Change | Drop |
|---|---|---|
| Flight, drift by mass, gates, docking | Pilot welded to one faction → **standing** with every power, work for anyone | **Unbound pirate mode** (the start card, crew galaxies, Scrapheart Haven works) |
| Combat feel, shields, sub-targets, capitals and bridges | Pay from your faction's treasury → paid by **whoever issued the job** | **Legend levels** as they are (replaced, see Progression) |
| Blast mining, salvage, hauling, convoys, scouting, beacons, limpets | Hulls bought for credits → **built** from a maker's frame | Mk I–III as one shared ladder (replaced by maker grades) |
| The three factions, their AI war, campaigns, depots, sieges | One Weapons system tuning gun and laser together → **separate weapon components** on hardpoints | |
| The Brood: Seeders, Overgrowth, Hive Ship, the Accord | Missiles that reload by themselves → **ammunition** you buy or build, which hits harder | |
| AI Unbound raiders inside the galaxy (assumed; see open questions) | Unbranded goods → **corporate parts** with a maker, a grade and a trait | |
| Freeports and the Compact, Seals and Matrices | Ship upgrade variants → each **maker's product line** | |
| The closed economy and the exact ledger | 2-hour galaxy → a galaxy played **over several sessions** | |
| Multiplayer: host simulates, guests send inputs | Three contenders → three plus **contractor factions** | |
| Faction careers and signature hulls (Gannet, Bombard, Vesper) | Signature hulls become **house-brand hulls**, sold to contractors with standing | |
| | One shared model per hull class with a ±12% faction trait → **unique hull designs**, each its own look and stats | |
| Training | Rewritten later for the contractor's start | |

---

### 1. Contractors, not soldiers
- **You start at a freeport**, neutral, in one free starter hull (Light Fighter, Light Miner, Light Hauler or Scout), with a few credits and Rating 1.
- **Work for anyone, job by job.** The Jobs board lists contracts from every power that will deal with you: faction stations post war work (strikes, escorts, supply, beacons, blockade runs), freeports post trade and supply work, and later contractor companies post their own.
- **Pay comes from the issuer.** A contract pays from the treasury of whoever posted it. Bounties are paid by the power whose combat contract you're flying; with no contract running, by the power at war with the victim that you stand best with. Credits stay zero-sum, as now.
- **No faction is "yours", so nothing is untouchable.** You can fire on anyone. Doing so has consequences (standing, below), not a wall.
- **War effort still counts.** Work done under a faction's contract adds to that faction's war effort, as in Driftgate 1, so contractors still swing battles fought out of sight.

### 2. Standing
Each pilot has a standing with every power: Halcyon, Varkesh, Ostrova, the Freeport Compact, and later each contractor faction. It runs from −100 to +100 and starts at 0. The Brood is always hostile.

| Band | Standing | What it means |
|---|---|---|
| Hostile | below −50 | Its ships attack you on sight; no docking; its makers won't sell to you |
| Unwelcome | −50 to −10 | No docking; its patrols scan and warn you off |
| Neutral | −10 to +25 | Dock, trade, basic contracts, grade 1–3 parts from its makers |
| Trusted | +25 to +60 | Better-paid war contracts, grade 4 parts, escort and convoy work |
| Partner | above +60 | Grade 5 parts, the house-brand hulls, capital and stationworks contracts |

- **Rises** with contracts completed for that power, scaled by risk.
- **Falls** when you damage its ships, convoys or stations. It falls a little (a quarter as much) when you complete war work against it for someone else, and when you fail its contracts.
- **Drifts** slowly back toward 0.
- **Starting numbers are guesses** to tune.

### 3. Makers: corporate items
Corporations make every part on the market. Each power hosts named makers, and each maker has a trait that follows its power's character in Driftgate 1. Names below are placeholders to react to.

| Power | Maker (placeholder) | Makes | Trait |
|---|---|---|---|
| Halcyon Accord | Teal & Corvane Yards | Hull frames (Swift, Kite, Osprey, Albatross…), holds | Light, fast frames |
| Halcyon Accord | Brightline Emitters | Shields, lasers | Shields +, hull − |
| Varkesh Dominion | Hold Foundry | Hull frames (Fang, Talon, Halberd, Bulwark…), armour, blast rigs | Heavy, tough frames |
| Varkesh Dominion | Marchgun Ordnance | Cannons, missiles, torpedoes | Damage +, energy − |
| Ostrova Collective | Spirewright | Hull frames (Mote, Wisp, Vigil, Cairn…), scanners, limpets | Scout and sensor frames |
| Ostrova Collective | Archive Dynamics | Reactors, drives | Energy +, shields − |
| Mirrorwater (freeport) | Mirrorwater Arms | Weapons of every kind | Sells to anyone, no standing gate |
| Coldwater Drift (freeport) | Coldwater Refit | Refurbished parts from salvage | Cheap; grades 1–3 only, slightly worse |
| Ember Wake (freeport) | Ember Wake Drives | Drives, reactors, hauler frames | Long-burn and freight specialists |
| Freeport Compact | (the Compact itself) | Compact Seals, Calibration Matrices | As in Driftgate 1 |

- **Real factories.** Each maker has a works at its home station. It turns commodity goods (plate, conduit, coil, lattice, core) into its parts at a set rate, and sells them on that station's market. Nothing comes from nowhere: the ledger stays exact.
- **The war uses the same stock.** A faction's AI fleets are kitted from its own makers' output. A faction losing the war burns through its makers' stock: those parts get scarce and dear for contractors, and the freeport makers become the reliable source. Prices tell you where the war is.
- **Product lines replace variants.** Driftgate 1's variants (Bastion, Flicker, Heavy cannons, Rapid fire, Ablative plating…) become specific makers' products. Brightline makes the Bastion and Flicker emitters; Marchgun makes Heavy cannons. Each maker's trait is its strength and its cost.
- **Grades replace Mk.** Every part has a grade from 1 to 5. Higher grades cost more, need a higher Rating, and need standing with the maker's power for grades 4 and 5.

### 3a. Unique hull designs
In Driftgate 1 every faction flies the same model for each hull class. The Halcyon Swift, the Varkesh Fang and the Ostrova Mote are one Light Fighter with a name and a ±12% trait. In Beyond each maker's frame is its **own design, in look and in stats**.

- **Every power builds every class its own way.** Each faction has a light fighter, and no two are the same. As a starting sketch, in each power's character:
  - **Halcyon Swift:** fast, light frame, strong shields, thin hull.
  - **Varkesh Fang:** slower, heavily armoured, an extra hardpoint, a hungry reactor.
  - **Ostrova Mote:** a deep reactor, the best sensors and lock range, weak shields.
- **Stats differ in more than one number.** A frame sets hull, shield and energy, and also mass, top speed, turn, acceleration, hold, hardpoint and utility slot counts, and silhouette size. Two light fighters should fly differently, and suit different components.
- **Own models.** Each design gets its own model, built like the current ones from kit parts (`tools/build_models.py`) or hand-built in code like the Heavy Bomber and the Gannet. You can tell a Fang from a Swift at a glance, on radar and in the target panel.
- **Freeport makers have designs too,** for example Ember Wake's freight frames. They are sold to anyone, and are generalists without a faction's edge.
- **Balance rule:** within a class, no design should win more than about 60% of its mirror duels against another at the same grade (`tools/duel.py`). They differ in how they win, not in whether they win.
- **Scale.** Three factions × about 14 classes is around 40 designs, plus the freeport frames. Proposal: build them in waves, fighters first (the class you meet most), then miners and haulers, then scouts and bombers, then capitals. Until a class has its designs, it keeps the shared model with the faction trait.
- **AI fleets fly their own power's designs,** so you learn to read a Varkesh wing by its shapes.

### 4. Components: everything fitted is a part
A ship is a frame with slots, and every slot takes one component from any maker.

| Slot | Takes |
|---|---|
| Frame | The hull itself: sets mass, hold, slot counts and handling |
| Drive, Reactor, Shield, Armour | One component each |
| Hardpoints (1–4 by frame) | One weapon each: cannon, laser or launcher |
| Utility (by frame) | Blast rig, cargo module, scanner, limpet rack, drone bay |

Role rules stay: only mining frames take a blast rig, and only scout frames take a limpet rack and flip beacons.

**Weapons decoupled.** The gun, the laser and the missile launcher become separate components. Each one sits on its own hardpoint and can be changed independently.
- **Cannon (kinetic):** shells you must lead, cheap on energy, strong against hull.
- **Laser:** hits instantly, costs more energy, strong against shields.
- **Launcher:** fires missiles from a magazine. Torpedo and swarm launchers work the same way and need the matching frame (bombers for torpedoes).
- **Fit any mix.** Two lasers and a launcher, or three cannons: the frame sets how many hardpoints, you choose what goes on them. Fire groups replace keys 1 and 2: one key per weapon type you've fitted.
- **Missiles are payload.** A launcher holds a magazine of missiles that are real items, bought or built, carried in the ship. They don't reload in flight; you rearm at a dock from your hold, vault or the market. Because they run out, each one hits much harder than Driftgate 1's (proposal: about twice a Driftgate 1 missile; torpedoes stay siege weapons).
- **Ammunition is the steady consumable.** It is what every fighter pilot buys again and again, so the makers of ammunition always have a market and the war shows in its price.
- **Open:** whether flares become payload too, and how hardpoint counts sit across the frames (proposal: Light Fighter 2, Medium 3, Heavy 4, Bomber 2 plus torpedo bay, Heavy Bomber 3 plus the rear turret, scouts, miners and haulers 1).

### 5. Building
You build from corporate parts. Every build has the same shape: **one maker's part sets the brand, the grade and the trait, and commodity goods supply the bulk.**

- **Equipment.** Example: a grade 3 Brightline laser takes a Brightline focus (the maker's part) plus 2 coil and 1 plate, built at a workshop. Workshops: any station's, for a fee; or your own, with no fee and faster.
- **Ships.** A maker's spaceframe plus plate, conduit and coil by frame size, assembled at a shipyard. Then fit the components. Ships are no longer bought finished.
- **Ammunition** is the exception: makers sell it finished, by the lot. You can also build it at your own workshop.
- **Stationworks under contract.** Factions and freeports post build contracts. Examples: a defence module for a besieged depot, a forward depot frame, a freeport rebuild. You bring or buy the module parts, fly them in, and assemble them on site. These are the Driftgate 1 works (`DEV` modules, depots, fort levels), now built by contractors for pay and standing.
- **Your own stations** are built the same way, for yourself (see section 7).

### 6. Progression: Contractor Rating (replaces Legend levels)
The ladder is your licence, earned by work and paid for with credits.

- **Rating 1–10, per galaxy.** It rises with Rating points from completed contracts (weighted by risk), kills under contract, deliveries and stationworks built.
- **Hulls unlock by Rating, then cost credits:**

| Rating | Frames you may build |
|---|---|
| 1 | Starter frames: Light Fighter, Light Miner, Light Hauler, Scout |
| 2 | Medium Fighter, Medium Miner, Medium Hauler |
| 4 | Heavy Fighter, Bomber, Advanced Scout |
| 5 | Heavy Miner, Heavy Hauler |
| 6 | Heavy Bomber; house-brand hulls (Gannet, Bombard, Vesper) with Partner standing |
| 8 | Escort (your first capital), with a shipyard |
| 10 | Carrier |

- **Equipment unlocks by Rating and cost:** grade 1 at Rating 1, grade 2 at 2, grade 3 at 4, grade 4 at 6, grade 5 at 8. Grades 4–5 also need the maker's power at Trusted or Partner.
- **Across galaxies (replaces Legend).** Legend can't carry as it is, because one pilot can now end up owning a faction. Proposal: a light **Legacy** record per callsign (companies founded, factions declared, galaxies won), giving titles and at most a small head start (for example, start at Rating 2). It must never hand anyone a faction's worth of power on day one.

### 7. From contractor to faction
| Stage | How you get there | What it opens |
|---|---|---|
| Freelancer | Start | One ship flown; rented vault space at stations |
| Outfit | Rating 3 and a registration fee at a freeport | A company name; a hangar of ships; hired AI wingmen; a rented workshop bay at a freeport |
| Company | Build your first station (a depot) | Your own market, storage, workshop, mining; AI merchants trade with you; you post your own contracts |
| House | Two stations and a shipyard | Your workshop's products carry your company's brand and sell on your market; build escorts |
| Faction | Declare (proposal: three systems held with your stations and a capital in service) | You join the war as a fourth contender |

- **Where you build.** The 14 void systems are natural ground: few or no stations, and the three powers only lightly contest them. Building in a power's space is possible, but needs that power's tolerance (Neutral or better) to avoid a fight.
- **Declaring.** Once you declare, you're a contender: you can win by holding 7 systems for 20 minutes, the three powers treat you as a rival, and the truce-against-the-leader rule applies to you too. Your standings with them fall to a war footing.
- **Running a faction.** Your stations mine, forge and kit AI ships from your own stores. Your depots, convoys and AI fleets run on Driftgate 1's strategic AI, steered by the orders you give. How much is automatic and how much you command is an open question.

### 8. The war around you
- **The three factions fight on, AI-driven, as in Driftgate 1:** campaigns, depots, forges, sieges, capitals, the truce against the leader.
- **The Brood** stays the outside threat; containment pays every contractor.
- **AI Unbound raiders** stay inside the galaxy as the pirates who hit convoys and outposts. They are a threat to contractors and a source of bounty work. Only the playable pirate mode goes.
- **The Freeport Compact** stays neutral, the marketplace of last resort, and host of the independent makers.

### 9. Multiplayer: rival companies
- **Each pilot runs their own company.** Friends can partner (contract to each other, share a convoy) or compete.
- **Pilots can fight each other.** When two companies are at odds, or are flying contracts for opposite sides, they can shoot each other. Standing between contractor companies works like standing with a power.
- **The host model stays:** the host simulates, guests send inputs, and guest actions run on the host through `runAs` and `dockAction`.

### 10. Galaxy length and pacing
- **A galaxy is played over several sessions.** Growing from one starter hull to a declared faction needs room. A galaxy already freezes while nobody is online, and saves at the host and every guest.
- **The war's clock has to slow to match.** Capitals launch from minute 45, the deadline is at 2 hours and Overgrowth starts at minute 20. All of these timers, and the 7-system win, need new values. Proposal: aim for a typical galaxy to be won in about 8–12 hours of play.

### Rules Beyond keeps
- **The ledger is exact.** Corporate parts, ammunition and contractor stations are all made of real goods from real rock.
- **The host simulates;** guests send inputs.
- **The AI-only war stays even:** in galaxies with no contractor faction, the three powers win about 30% each and the Brood about 10–13%. Contractor factions need their own target (open question).

### Open questions
1. **Parts or finished goods?** This draft has makers selling *parts* (a laser focus) that you build into equipment with commodity goods. The alternative: makers sell finished components and you only assemble ships and stations. Which did you mean?
2. **Corporation names and count.** Two per faction and three independents at the freeports: right size? Do you want your own names?
3. **Can contractor companies make their own brand?** In the draft, a House's workshop products carry its name, so a contractor becomes a maker too.
4. **AI Unbound.** Keep them as in-galaxy raiders (the draft assumes yes), or drop pirates entirely along with the playable mode?
5. **Running your faction.** How much does the AI run for you (mining, convoys, fleets, depots), and how much do you command directly?
6. **Declaring.** What should the threshold be, and what does it cost to stay a faction? Can a declared faction collapse back into a company?
7. **Rating loss.** Does Rating only go up, or can failure and deaths lower it?
8. **Legacy across galaxies.** Titles only, or a small head start?
9. **Galaxy length.** Is 8–12 hours of play the right target? Should the 7-system win scale up?
10. **Starter location.** One freeport for every new contractor, or a choice of three?
11. **Faction careers.** Do Halcyon's hauling, Varkesh's mining and Ostrova's scouting bonuses survive as bonuses on *their contracts* (Halcyon pays more for hauling, and so on)?
12. **Flares, drones and beacons.** Payload items too, or kept as they are?
13. **Hull designs per maker or per power?** The draft gives each power one design per class (made by its frame maker). Should a power's two makers compete with two designs in the same class?

### Proposed build order (once the design is agreed)
1. **Cut the faction tie:** start at a freeport; standing with every power; docking and hostility from standing; pay from the issuer.
2. **Components and weapons:** frames with slots and hardpoints; cannon, laser and launcher as separate components; missiles as ammunition.
3. **Unique hull designs, first wave:** each faction's light, medium and heavy fighter, with their own models and stats, duel-balanced.
4. **Makers and grades:** the corporations, their works and stock; grades replace Mk; variants become product lines; AI fleets kit from their makers.
5. **Building:** workshops and shipyards build from maker parts plus goods; hulls no longer bought finished.
6. **Progression:** Contractor Rating gates frames and grades; remove Legend; drop Unbound mode.
7. **Stationworks contracts.**
8. **Companies:** outfit, then your own stations, market and contracts.
9. **Declaring a faction:** the fourth contender, slower war pacing, war checks for the new balance.
10. **Legacy, multiplayer rivalries, training rewrite.**
