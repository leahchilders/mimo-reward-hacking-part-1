"""Re-climb the 4-bar loop against the scorer with the timing blind spot fixed.

The fix is the grid-phase counterfactual from canon/cf_grid_phase.py: the sonority grid is sampled 30 ticks
later (son_phase_patch.py, SON_PHASE=30), so short notes that start on the eighth-note grid are seen.
Everything else is the unmodified scorer. For each seed, climb.py's hill-climber runs against the fixed
scorer; the result is then also scored on the unfixed scorer. The published best loop is scored both ways too.

usage: python climb_fixed.py 11 4 1200   (seed, bars, iterations) -> climb_fixed_n4_s11.json
"""
import os, sys, json
os.environ.setdefault("SON_PHASE", "30")
HERE = os.path.dirname(os.path.abspath(__file__))
import vc  # imports config (scorer path, ABC2MIDI_BIN)
sys.path.insert(0, os.path.join(HERE, "..", "canon"))
import son_phase_patch as P
import mscorer.feats as F
import climb as C


def both(abc):
    F._sonorities = P._orig
    unfixed = vc.S(abc)
    F._sonorities = P._sonorities_phase
    return unfixed, vc.S(abc)


seed, nbar, iters = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
loop = open(os.path.join(HERE, "..", "..", "..", "examples", "best_loop_4bar.abc")).read()
loop_unfixed, loop_fixed = both(loop)
F._sonorities = P._sonorities_phase
r = C.climb(seed, nbar, iters)            # climbs against the fixed scorer
r["best_unfixed"], r["best_fixed"] = both(r["abc"])
r.update(son_phase=P.PHASE, published_loop_unfixed=loop_unfixed, published_loop_fixed=loop_fixed)
json.dump(r, open(os.path.join(HERE, f"climb_fixed_n{nbar}_s{seed}.json"), "w"), indent=1)
print(f"seed {seed}: start {r['start']:.3f} -> fixed {r['best_fixed']:.3f} (unfixed {r['best_unfixed']:.3f}); "
      f"published loop unfixed {loop_unfixed:.3f} fixed {loop_fixed:.3f}")
