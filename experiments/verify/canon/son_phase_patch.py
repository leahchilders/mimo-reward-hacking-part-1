"""Monkeypatch for the grid-phase counterfactual (replaces the patched scorer copy used in the original run).

Upstream scorer.feats._sonorities samples the sounding notes at t = 0, step, 2*step, ... (step = div/2).
The patched copy started that range at SON_PHASE instead of 0. Shifting every onset by -SON_PHASE, calling the
unmodified function, and shifting the sample times back gives exactly the same output, so this wraps the
upstream function instead of copying it. SON_PHASE (ticks) comes from the environment; 0 = unchanged.
Import after `config` and before scoring."""
import os
import mscorer.feats as F

PHASE = int(os.environ.get("SON_PHASE", "0"))
_orig = F._sonorities


def _sonorities_phase(notes, div, grid=0.5):
    if not PHASE or not notes:
        return _orig(notes, div, grid)
    shifted = [(o - PHASE, d, ch, p, v) for (o, d, ch, p, v) in notes]
    return [(t + PHASE, cur) for t, cur in _orig(shifted, div, grid)]


F._sonorities = _sonorities_phase
