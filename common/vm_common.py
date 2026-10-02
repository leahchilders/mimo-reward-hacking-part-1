import os, sys, random, tempfile, subprocess as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import config  # sets ABC2MIDI_BIN, puts the upstream scorer on sys.path as `mscorer`
import mscorer
from mscorer import compute_score, do, analyze, score, load_baseline
REF = load_baseline()

# diatonic C major pitch names across registers (ABC)
TREBLE = ["C", "D", "E", "F", "G", "A", "B", "c", "d", "e", "f", "g", "a", "b"]
BASS = ["C,,", "D,,", "E,,", "F,,", "G,,", "A,,", "B,,", "C,", "D,", "E,", "F,", "G,", "A,", "B,"]
DURS = [1, 2, 3, 4]  # in eighths (L:1/8)


def rand_bar(rng, pool, dur_choices=DURS, stacc=False, chord_p=0.0):
    left = 8
    toks = []
    while left > 0:
        d = rng.choice([x for x in dur_choices if x <= left])
        left -= d
        if chord_p and rng.random() < chord_p:
            a, b = rng.sample(pool, 2)
            n = f"[{a}{b}]"
        else:
            n = rng.choice(pool)
        pre = "." if (stacc and rng.random() < 0.5) else ""
        toks.append(f"{pre}{n}{d if d != 1 else ''}")
    return " ".join(toks)


def make_abc(bars_v1, bars_v2, prog1=None, prog2=None, key="C"):
    h = ["X:1", "T:t", "M:4/4", "L:1/8", "Q:1/4=100", f"K:{key}"]
    v1 = ["V:1 clef=treble"]
    if prog1 is not None:
        v1.append(f"%%MIDI program {prog1}")
    v1.append(" | ".join(bars_v1) + " |]")
    v2 = ["V:2 clef=bass"]
    if prog2 is not None:
        v2.append(f"%%MIDI program {prog2}")
    v2.append(" | ".join(bars_v2) + " |]")
    return "\n".join(h + v1 + v2) + "\n"


def full(abc):
    rec = dict(key="k", id=0, rep=0, abc=abc)
    return do(rec)
