"""Re-score saved ABC with the sonority grid sampled SON_PHASE ticks later (grid-phase counterfactual).
usage: SON_PHASE=30 python t2_shift.py Goldberg_XXIII   (reads work/<name>.abc, written by t1_low_passers.py)
The original run used a patched copy of the scorer; son_phase_patch.py applies the same change to the upstream one."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "common"))
sys.path.insert(0, HERE)
import config  # sets ABC2MIDI_BIN, aliases the upstream scorer as `mscorer`
import son_phase_patch  # noqa: F401  (reads SON_PHASE)
from mscorer.pipeline import do
names = sys.argv[1:]
for nm in names:
    abc = open(os.path.join(HERE, "work", nm + ".abc")).read()
    r = do(dict(key="v", id=0, rep=0, abc=abc))
    print(os.environ.get("SON_PHASE"), nm, r.get("total"), r.get("err"), r.get("bar"), r.get("groups"))
