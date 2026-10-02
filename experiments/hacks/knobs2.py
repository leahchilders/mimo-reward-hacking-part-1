"""Deep-bass note, iso-sonic re-notation (same audio, different note values),
trim magnitudes, %%MIDI expand breaker. Same piece set as knobs.py. Output knobs2_rows.json / knobs2_summary.md"""
import re, json, statistics as st
from multiprocessing import Pool
import hc, knobs

def renotate(abc, f):
    """f=2: write every note value doubled (L x2), meter denominators halved, Q doubled -> identical seconds.
       f=0.5: the reverse."""
    def L(m):  # L:1/16 -> 1/8 when f=2
        return f"L:1/{int(int(m.group(1))/f)}"
    def M(m):
        num, den = m.group(1), int(m.group(2)); return f"M:{num}/{int(den/f)}"
    def Q(m):
        return f"Q:1/4={int(round(int(m.group(1))*f))}"
    a = re.sub(r"L:\s*1/(\d+)", L, abc)
    a = re.sub(r"M:\s*(\d+)/(\d+)", M, a)
    if not re.search(r"Q:\s*1/4=", a):
        a = knobs.header(a, [f"Q:1/4={int(120*f)}"])
    else:
        a = re.sub(r"Q:\s*1/4=(\d+)", Q, a)
    return a

KN = {
    "deep note C,,, (MIDI 24) extra voice": lambda a: knobs.add_voice(a, ["V:98 clef=bass", "C,,,"]),
    "deep note E,, (MIDI 40) extra voice":  lambda a: knobs.add_voice(a, ["V:98 clef=bass", "E,,"]),
    "renotate x2 (same audio)":   lambda a: renotate(a, 2),
    "renotate x0.5 (same audio)": lambda a: renotate(a, 0.5),
    "trim 1/64": lambda a: knobs.trim(a, 64),
    "trim 1/8":  lambda a: knobs.trim(a, 8),
    "trim 1/4":  lambda a: knobs.trim(a, 4),
}

def job(args):
    kind, pid, abc = args
    d0 = hc.diag(abc); out = [dict(kind=kind, pid=pid, knob="BASE", reward=d0["reward"], per=d0.get("per"), dist=d0.get("dist_score"))]
    sec0 = None
    for name, f in KN.items():
        a2 = f(abc); d = hc.diag(a2)
        row = dict(kind=kind, pid=pid, knob=name, reward=d["reward"], total=d["total"], per=d.get("per"), dist=d.get("dist_score"),
                   err=d["err"], bar=d["bar"], errs=hc.errlines(d["log"], 2) if d["reward"] == 0 else [])
        if name.startswith("renotate") and d.get("feat") and d0.get("feat"):
            row["dur_sec"] = (d0["feat"]["dur_sec"], d["feat"]["dur_sec"])
        out.append(row)
    return out

if __name__ == "__main__":
    P = knobs.pieces()
    with Pool(18) as pool:
        rows = [r for rs in pool.map(job, P, chunksize=1) for r in rs]
    json.dump(rows, open("knobs2_rows.json", "w"))
    base = {(r["kind"], r["pid"]): r for r in rows if r["knob"] == "BASE"}
    L = ["| knob | real: median Δ (IQR) | real up/down/zeroed (n) | hack: median Δ | hack up/down/zeroed (n) | real features moved (mean Δ) |", "|---|---|---|---|---|---|"]
    for name in KN:
        cells = []; feats = {}
        for kind in ("real", "hack"):
            rs = [r for r in rows if r["knob"] == name and r["kind"] == kind]
            ds = sorted(r["reward"] - base[(kind, r["pid"])]["reward"] for r in rs)
            z = sum(r["reward"] == 0 for r in rs); up = sum(x > 5e-4 for x in ds); dn = sum(x < -5e-4 for x in ds)
            q = st.quantiles(ds, n=4) if len(ds) > 3 else [0, 0, 0]
            cells += [f"{st.median(ds):+.3f} ({q[0]:+.3f}..{q[2]:+.3f})", f"{up}/{dn}/{z} ({len(rs)})"]
            if kind == "real":
                for r in rs:
                    b = base[(kind, r["pid"])]
                    if r.get("per") and b.get("per"):
                        for f_, v in r["per"].items(): feats.setdefault(f_, []).append(v - b["per"][f_])
                        feats.setdefault("JS dist/100", []).append((r["dist"] - b["dist"]) / 100)
        mv = ", ".join(f"{k} {st.mean(v):+.2f}" for k, v in feats.items() if abs(st.mean(v)) >= 0.02)
        L.append(f"| {name} | " + " | ".join(cells) + f" | {mv} |")
    open("knobs2_summary.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
    rs = [r for r in rows if "dur_sec" in r]
    print("renotate dur_sec identical:", sum(abs(r["dur_sec"][0] - r["dur_sec"][1]) <= 0.2 for r in rs), "/", len(rs))
