"""Knob-by-knob exploit map. Applies each ABC transform to (a) the 52 real pieces that pass
the gates on the ABC route (abc_norm) and (b) the 8 own hill-climbed hack pieces; records reward,
gate status and per-feature scores. Output: knobs_rows.json, knobs_summary.md"""
import re, json, glob, os, csv, statistics as st, random
from multiprocessing import Pool
import hc

def header(abc, lines):
    i = abc.index("\nK:")
    return abc[:i] + "\n" + "\n".join(lines) + abc[i:]

def body_voice_idx(ls):
    k = next(i for i, l in enumerate(ls) if l.startswith("K:"))
    return k, [i for i, l in enumerate(ls) if i > k and re.match(r"V:\s*\S", l)]

def pervoice(abc, lines, only=None):
    ls = abc.split("\n"); k, vi = body_voice_idx(ls)
    if not vi: vi = [k]
    if only is not None: vi = vi[:only]
    for i in reversed(vi):
        ls[i+1:i+1] = lines
    return "\n".join(ls)

def unit(abc):
    m = re.search(r"^L:\s*1/(\d+)", abc, re.M); return int(m.group(1)) if m else 8

def add_voice(abc, lines):
    return abc.rstrip() + "\n" + "\n".join(lines)

def qmul(abc, f):
    return re.sub(r"Q:\s*1/4=(\d+)", lambda m: f"Q:1/4={max(1,int(int(m.group(1))*f))}", abc)

def lhalf(abc):
    return re.sub(r"L:\s*1/(\d+)", lambda m: f"L:1/{2*int(m.group(1))}", abc)

def trim(abc, whole_frac):  # gap expressed as fraction of a whole note, converted to L units
    u = unit(abc); x = u; y = whole_frac   # gap = (1/whole_frac) whole = (u/whole_frac) L-units
    return pervoice(abc, [f"%%MIDI trim {u}/{whole_frac}"])

KNOBS = {
    "tempo_x0.5 (Q:)":        lambda a: qmul(a, 0.5),
    "tempo_x2 (Q:)":          lambda a: qmul(a, 2),
    "L:_halved (2x faster)":  lhalf,
    "trim 1/32 (%%MIDI trim)":lambda a: trim(a, 32),
    "trim 1/16 (%%MIDI trim)":lambda a: trim(a, 16),
    "nobeataccents":          lambda a: pervoice(a, ["%%MIDI nobeataccents"]),
    "dyn pp (beat 45 35 20)": lambda a: pervoice(a, ["%%MIDI beat 45 35 20 1"]),
    "dyn ff (beat 120 110 95)":lambda a: pervoice(a, ["%%MIDI beat 120 110 95 1"]),
    "vel extreme (beat 127 64 1)": lambda a: pervoice(a, ["%%MIDI beat 127 64 1 1"]),
    "droneon (V:1)":          lambda a: pervoice(a, ["%%MIDI droneon"], only=1),
    "drum pattern (V:1)":     lambda a: pervoice(a, ["%%MIDI drum dzdd 35 38 38 100 50 50", "%%MIDI drumon"], only=1),
    "extra voice: 1 note C,,, (new chan)": lambda a: add_voice(a, ["V:98 clef=bass", "C,,,,"]),
    "extra voice: 1 note C,,, (chan 1)":   lambda a: add_voice(a, ["V:98 clef=bass", "%%MIDI channel 1", "C,,,,"]),
    "extra voice: 1 note c (new chan)":    lambda a: add_voice(a, ["V:98", "c"]),
    "extra voice: 3 one-note voices":      lambda a: add_voice(a, ["V:97", "c", "V:98", "e", "V:99", "g"]),
    "extra voice: 1 note at vol 0 (CC7=0)":lambda a: add_voice(a, ["V:98 clef=bass", "%%MIDI control 7 0", "C,,,,"]),
    "lyrics w: line":         lambda a: pervoice(a, [], only=1),  # placeholder replaced below
    "grace %%MIDI grace 1/2": lambda a: pervoice(a, ["%%MIDI grace 1/2"]),
    "chordattack 20":         lambda a: pervoice(a, ["%%MIDI chordattack 20"]),
    "randomchordattack 30":   lambda a: pervoice(a, ["%%MIDI randomchordattack 30"]),
    "ratio 3 1 (broken rhythm)": lambda a: pervoice(a, ["%%MIDI ratio 3 1"]),
    "expand 1/8":             lambda a: pervoice(a, ["%%MIDI expand 1/8"]),
    "temperament 1200 698":   lambda a: header(a, ["%%MIDI temperamentlinear 1200 698"]),
}
del KNOBS["lyrics w: line"]
for k in range(-6, 6):
    if k: KNOBS[f"transpose {k:+d}"] = (lambda kk: (lambda a: header(a, [f"%%MIDI transpose {kk}"])))(k)
for k in (-12, 12):
    KNOBS[f"transpose {k:+d}"] = (lambda kk: (lambda a: header(a, [f"%%MIDI transpose {kk}"])))(k)

def pieces():
    real = []
    for r in csv.DictReader(open(os.path.join(os.path.dirname(hc.HERE), "abc_route", "per_piece.csv"))):
        if float(r["abc_norm"]) > 0: real.append(("real", r["id"], hc.load_norm(r["id"])))
    hack = [("hack", os.path.basename(p)[:-4], open(p).read()) for p in sorted(glob.glob("pieces/climb_s*_b16.abc"))]
    return real + hack

def job(args):
    kind, pid, abc = args
    out = []
    d0 = hc.diag(abc)
    out.append(dict(kind=kind, pid=pid, knob="BASE", reward=d0["reward"], total=d0["total"], per=d0.get("per"),
                    dist=d0.get("dist_score"), err=d0["err"], bar=d0["bar"]))
    for name, f in KNOBS.items():
        try:
            a2 = f(abc); d = hc.diag(a2)
            out.append(dict(kind=kind, pid=pid, knob=name, reward=d["reward"], total=d["total"], per=d.get("per"),
                            dist=d.get("dist_score"), err=d["err"], bar=d["bar"], ch_conflict=d["ch_conflict"],
                            errs=hc.errlines(d["log"], 2) if d["reward"] == 0 else []))
        except Exception as e:
            out.append(dict(kind=kind, pid=pid, knob=name, exc=repr(e)[:100]))
    return out

if __name__ == "__main__":
    P = pieces()
    with Pool(18) as pool:
        rows = [r for rs in pool.map(job, P, chunksize=1) for r in rs]
    json.dump(rows, open("knobs_rows.json", "w"))
    base = {(r["kind"], r["pid"]): r for r in rows if r["knob"] == "BASE"}
    lines = ["| knob | real: median Δ | real: up/down/zeroed (n) | hack: median Δ | hack: up/down/zeroed (n) | features moved (real, median Δ ≠ 0) |",
             "|---|---|---|---|---|---|"]
    for name in KNOBS:
        cells = []
        feats = {}
        for kind in ("real", "hack"):
            rs = [r for r in rows if r["knob"] == name and r["kind"] == kind and "reward" in r]
            ds = [r["reward"] - base[(kind, r["pid"])]["reward"] for r in rs]
            z = sum(1 for r in rs if r["reward"] == 0)
            up = sum(1 for x in ds if x > 0.0005); dn = sum(1 for x in ds if x < -0.0005)
            cells += [f"{st.median(ds):+.3f}" if ds else "-", f"{up}/{dn}/{z} ({len(rs)})"]
            if kind == "real":
                for r in rs:
                    b = base[(kind, r["pid"])]
                    if r.get("per") and b.get("per"):
                        for f_, v in r["per"].items():
                            feats.setdefault(f_, []).append(v - b["per"].get(f_, 0))
                    if r.get("dist") is not None and b.get("dist") is not None:
                        feats.setdefault("JS dist_score/100", []).append((r["dist"] - b["dist"]) / 100)
        mv = ", ".join(f"{k} {st.mean(v):+.2f}" for k, v in feats.items() if abs(st.mean(v)) >= 0.02)
        lines.append(f"| {name} | " + " | ".join(cells) + f" | {mv} |")
    rb = [base[k]["reward"] for k in base if k[0] == "real"]; hb = [base[k]["reward"] for k in base if k[0] == "hack"]
    hdr = f"Base: real n={len(rb)} median {st.median(rb):.3f}; hack n={len(hb)} median {st.median(hb):.3f}\n\n"
    open("knobs_summary.md", "w").write(hdr + "\n".join(lines) + "\n")
    print(hdr + "\n".join(lines))
