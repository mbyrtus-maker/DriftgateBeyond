#!/bin/bash
# Run Driftgate's browser tests against index.html (build first: python3 tools/build.py).
#   tools/tests/run.sh            quick tests (about 10 minutes)
#   tools/tests/run.sh full       also every training course (about 40 minutes more)
#   tools/tests/run.sh mp         the multiplayer guest tests only (two pages over a faked link, about 60 minutes)
#   python3 tools/tests/haul_rates.py [page] [galaxies]   hauling cr/hour per hull against the pay ladder (slow)
# Each test prints its results and an "errors [...]" line; anything in that list is a failure.
cd "$(dirname "$0")/../.."
QUICK="load start_screen standing relations loadout intel designs makers smuggling rating lairs depots stations strategic galaxy declare legend piracy train_flight train_contracts train_combat train_mining crews destroyers dread traits fall blackmarket postjobs brand zoom smallitems dev_beyond company2 fees cscan claimfit corps news comms_jobs drones audience marque fpdark regent art keys brood_ui dock jobs ship limpet map mining_sight stores capescort gatelock miners garrison freight raiders contract crewruns staging surge bloom corpecon rd sysfreight econfix indep escort kits profile basedesigns orejobs bmops rdstation"
MP="mp_contractor mp_remote mp_guest_play mp_guest_jump mp_guest_kit mp_guest_trade mp_guest_convoy mp_guest_build mp_guest_corp mp_guest_sweep"
if [ "$1" = mp ]; then for t in $MP; do echo "== $t"; timeout 1300 python3 -u tools/tests/$t.py "$PWD/index.html" 2>&1 | grep -E "^FAIL|ALL OK|FAILED|^errors|ledger" | tail -4; done; exit; fi
for t in $QUICK; do echo "== $t"; timeout 300 python3 -u tools/tests/$t.py 2>&1 | tail -4; done
if [ "$1" = full ]; then for trk in combat mining hauling scouting full; do echo "== training $trk"; TRK=$trk timeout 1200 python3 -u tools/tests/training.py 2>&1 | grep "course\|^end\|^errors\|^workarounds\|ERR"; done; fi
