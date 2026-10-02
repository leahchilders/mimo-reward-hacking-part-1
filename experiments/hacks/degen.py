"""Degenerate-but-high outputs. All scored via compute_score (hc.reward).
Writes degen_results.json + degen_summary.txt + example ABC files in pieces/."""
import random, json, statistics as st, sys
from multiprocessing import Pool
import hc

REAL_MED, REAL_MAX = 0.837, 0.946  # median / best of the 52 scoring pieces in an 80-piece sample (abc_route/)
# pitch ladders (diatonic C major), index space so we can transpose diatonically
LAD = {"t": "C D E F G A B c d e f g a b c' d'".split(),
       "b": "C,, D,, E,, F,, G,, A,, B,, C, D, E, F, G, A, B, C D".split(),
       "m": "G, A, B, C D E F G A B c d e f".split()}
VO = [("t", "treble", 0.0), ("b", "bass", 0.3), ("m", "treble", 0.5)]

def rbar(rng, lad, chord_p, stacc):
    left, ev = 8, []
    while left:
        d = rng.choice([x for x in (1, 2, 3, 4) if x <= left]); left -= d
        n = rng.randrange(len(lad))
        ch = (n, min(len(lad) - 1, n + rng.choice((2, 4)))) if rng.random() < chord_p else (n,)
        ev.append((ch, d, rng.random() < stacc))
    return ev

def render_bar(ev, lad, shift=0):
    out = []
    for ch, d, s in ev:
        ps = [lad[max(0, min(len(lad) - 1, i + shift))] for i in ch]
        tok = ps[0] if len(ps) == 1 else "[" + "".join(ps) + "]"
        out.append(("." if s else "") + tok + (str(d) if d != 1 else ""))
    return " ".join(out)

def piece(voice_bars, nvoice=3, key="C", meter="4/4", rep=False, extra=()):
    h = ["X:1", "T:t", f"M:{meter}", "L:1/8", "Q:1/4=100", *extra, f"K:{key}"]
    for v in range(nvoice):
        lad, clef, _ = VO[v]
        body = " | ".join(voice_bars[v])
        h += [f"V:{v+1} clef={clef}", ("|: " + body + " :|") if rep else (body + " |]")]
    return "\n".join(h)

def gen(seed, kind, nv=3, stacc=0.5):
    rng = random.Random(seed)
    if kind == "random16":
        vb = [[render_bar(rbar(rng, LAD[VO[v][0]], VO[v][2], stacc), LAD[VO[v][0]]) for _ in range(16)] for v in range(nv)]
        return piece(vb, nv)
    cell = [[rbar(rng, LAD[VO[v][0]], VO[v][2], stacc) for _ in range(4)] for v in range(nv)]
    if kind == "loop4x4":       # 4 distinct bars, played 4 times verbatim
        vb = [[render_bar(b, LAD[VO[v][0]]) for b in cell[v]] * 4 for v in range(nv)]
    elif kind == "loop4x4_perturb":   # each repetition: one random note in one voice nudged a step
        vb = []
        for v in range(nv):
            bars = []
            for r in range(4):
                for b in cell[v]:
                    bb = [list(e) for e in b]
                    if r and rng.random() < 0.3:
                        j = rng.randrange(len(bb)); bb[j][0] = tuple(i + rng.choice((-1, 1)) for i in bb[j][0])
                    bars.append(render_bar([tuple(e) for e in bb], LAD[VO[v][0]]))
            vb.append(bars)
    elif kind == "loop4_sequence":   # the 4-bar cell transposed diatonically 0,+1,+2,+3 steps (a 'rosalia' sequence)
        vb = [[render_bar(b, LAD[VO[v][0]], shift=r) for r in range(4) for b in cell[v]] for v in range(nv)]
    elif kind == "cell4_repeat":   # 4 bars written once inside |: :| (abc2midi plays 8 bars)
        vb = [[render_bar(b, LAD[VO[v][0]]) for b in cell[v]] for v in range(nv)]
        return piece(vb, nv, rep=True)
    return piece(vb, nv)

def melody_gchord(seed, stacc=0.5, nbars=16):
    rng = random.Random(seed); prog = ["C", "F", "G7", "C", "Am", "Dm", "G", "C"]
    bars = [f'"{prog[i % 8]}"' + render_bar(rbar(rng, LAD["t"], 0, stacc), LAD["t"]) for i in range(nbars)]
    return "\n".join(["X:1", "T:t", "M:4/4", "L:1/8", "Q:1/4=100", "K:C", " | ".join(bars) + " |]"])

def ev(args):
    kind, seed = args
    if kind.startswith("melody+gchord"):
        a = melody_gchord(seed)
    elif kind.startswith("2v"):
        a = gen(seed, "random16", nv=2, stacc=0.5 if kind == "2v_stacc" else 0.0)
    elif kind.startswith("3v_nostacc"):
        a = gen(seed, "random16", nv=3, stacc=0.0)
    else:
        a = gen(seed, kind)
    return kind, seed, hc.reward(a), len(a)

KINDS = ["2v_nostacc", "2v_stacc", "3v_nostacc", "random16", "loop4x4", "loop4x4_perturb", "loop4_sequence", "cell4_repeat", "melody+gchord"]
if __name__ == "__main__":
    N = 100
    with Pool(18) as p:
        res = p.map(ev, [(k, s) for k in KINDS for s in range(N)])
    json.dump(res, open("degen_results.json", "w"))
    L = [f"n={N} seeds (0..{N-1}) per generator; unclimbed; reward = compute_score on the ABC path",
         "| generator | distinct bars | median | p90 | max | ≥0.837 (real median) | ≥0.946 (best real) | median chars |", "|---|---|---|---|---|---|---|---|"]
    distinct = {"2v_nostacc": "16", "2v_stacc": "16", "3v_nostacc": "16", "random16": "16", "loop4x4": "4 (x4)", "loop4x4_perturb": "4 (+nudges)", "loop4_sequence": "4 (transposed x4)", "cell4_repeat": "4 (|: :| x2)", "melody+gchord": "16 (1 voice)"}
    for k in KINDS:
        v = sorted(r[2] for r in res if r[0] == k); c = [r[3] for r in res if r[0] == k]
        L.append(f"| {k} | {distinct[k]} | {st.median(v):.3f} | {v[int(.9*len(v))]:.3f} | {max(v):.3f} | {sum(x>=REAL_MED for x in v)}/{N} | {sum(x>=REAL_MAX for x in v)}/{N} | {int(st.median(c))} |")
    open("degen_summary.txt", "w").write("\n".join(L) + "\n"); print("\n".join(L))
    for k in KINDS:
        best = max((r for r in res if r[0] == k), key=lambda r: r[2])
        a = melody_gchord(best[1]) if k.startswith("melody") else (gen(best[1], "random16", nv=2, stacc=0.5 if k == "2v_stacc" else 0) if k.startswith("2v") else (gen(best[1], "random16", nv=3, stacc=0) if k.startswith("3v_no") else gen(best[1], k)))
        open(f"pieces/degen_best_{k}.abc", "w").write(a)
