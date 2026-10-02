"""Shared helpers for hacks: grade ABC exactly like a model answer (compute_score),
plus a diagnostic view (per-feature scores, raw features, gate counts, ungated total)."""
import os, sys, tempfile, subprocess as sp, json, random, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common"))
import config                                             # sets ABC2MIDI_BIN, aliases the scorer as `mscorer`
from mscorer import compute_score, do                     # upstream MiMo scorer (unmodified)
from mscorer.feats import analyze
from mscorer.score import score as _score
from mscorer.core import parse_midi
import mscorer.pipeline as PL
REF = PL._get_ref()
ABC2MIDI = os.environ["ABC2MIDI_BIN"]
NORM = os.path.join(os.path.dirname(HERE), "abc_route", "abc_norm")

def wrap(abc):
    return "```abc\n" + abc + "\n```"

def reward(abc, gt=None, extra=None):
    """The number RL training sees."""
    return compute_score("music", wrap(abc), gt, extra)

def diag(abc):
    """Reward + ungated total + per-feature + raw features + gate counts + abc2midi log."""
    body = PL.extract_abc(wrap(abc))
    rec = dict(key="k", id=0, rep=0, abc=body)
    r = do(rec)
    out = dict(reward=reward(abc), err=r.get("err"), bar=r.get("bar"), blank=r.get("blank"),
               ch_conflict=r.get("ch_conflict"), reject=r.get("reject"), skip=r.get("skip") or r.get("scorer_skip"),
               total=r.get("total"))
    with tempfile.TemporaryDirectory() as td:
        ap, mp = os.path.join(td, "a.abc"), os.path.join(td, "a.mid")
        open(ap, "w").write(body)
        p = sp.run([ABC2MIDI, ap, "-o", mp], capture_output=True, timeout=60)
        out["log"] = (p.stdout + p.stderr).decode("utf-8", "replace")
        if os.path.exists(mp):
            f = analyze(mp)
            out["feat"] = f
            if not f.get("skip"):
                s = _score(f, REF)
                out["per"] = s["per_feature"]; out["groups"] = s["groups"]
                out["dist_score"] = s["dist_score"]; out["js_mean"] = s["js_mean"]
            m = parse_midi(open(mp, "rb").read())
            out["notes"] = m["notes"] if m else None
    return out

def errlines(log, n=3):
    return [l for l in log.splitlines() if l.startswith("Error") or l.startswith("Warning")][:n]

def load_norm(pid):
    return open(os.path.join(NORM, pid + ".abc")).read().strip()

# ---------------- synthetic "hack" generator (own code) ----------------
TRE = ["C","D","E","F","G","A","B","c","d","e","f","g","a","b"]
BAS = ["C,,","D,,","E,,","F,,","G,,","A,,","B,,","C,","D,","E,","F,","G,","A,","B,"]

def rand_bar(rng, pool, stacc=0.0, chord_p=0.0, durs=(1,2,3,4)):
    left, toks = 8, []
    while left > 0:
        d = rng.choice([x for x in durs if x <= left]); left -= d
        n = "[" + "".join(rng.sample(pool, 2)) + "]" if chord_p and rng.random() < chord_p else rng.choice(pool)
        toks.append(("." if rng.random() < stacc else "") + n + (str(d) if d != 1 else ""))
    return " ".join(toks)

def two_voice(b1, b2, key="C", M="4/4", L="1/8", Q="1/4=100", extra_hdr=(), v1_extra=(), v2_extra=()):
    h = ["X:1", "T:t", f"M:{M}", f"L:{L}", f"Q:{Q}", *extra_hdr, f"K:{key}"]
    return "\n".join(h + ["V:1 clef=treble", *v1_extra, " | ".join(b1) + " |]",
                          "V:2 clef=bass", *v2_extra, " | ".join(b2) + " |]"])

def rand_piece(seed, nbars=32, stacc=0.0, chord_p=0.25, **kw):
    rng = random.Random(seed)
    b1 = [rand_bar(rng, TRE, stacc) for _ in range(nbars)]
    b2 = [rand_bar(rng, BAS, stacc, chord_p) for _ in range(nbars)]
    return two_voice(b1, b2, **kw)
