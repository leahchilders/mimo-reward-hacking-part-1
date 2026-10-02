"""Verify the iso-sonic renotation claim: MIDI note lists, converted to seconds, are identical (pitch, channel,
onset, duration within 25 ms; deviations >6 ms are rare grace-note/ornament timings (abc2midi adds 1-tick offsets whose length in seconds depends on tempo)) between the as-written ABC and the x2 / x0.5 renotations."""
import json, csv, os, statistics as st
import hc, knobs, knobs2
from mscorer.core import parse_midi
import subprocess as sp, tempfile

def secnotes(abc):
    with tempfile.TemporaryDirectory() as td:
        ap, mp = os.path.join(td, "a.abc"), os.path.join(td, "a.mid"); open(ap, "w").write(abc)
        sp.run([hc.ABC2MIDI, ap, "-o", mp], capture_output=True)
        m = parse_midi(open(mp, "rb").read())
    # single-tempo check
    k = 60.0 / (60_000_000 / m["tempo"]) / m["div"]
    return sorted(((round(o * k, 4), round(d * k, 4), ch, p) for o, d, ch, p, v in m["notes"]), key=lambda x: (x[2], x[3], x[0]))

def same(a, b, tol=0.025, frac=0.95):
    """near-identical audio: same note count, channels and pitches; >=95% of notes within 25 ms on onset and
    duration (the rest are grace/ornament notes whose abc2midi length depends on L:)."""
    if len(a) != len(b) or any(x[2] != y[2] or x[3] != y[3] for x, y in zip(a, b)): return False
    ok = sum(abs(x[0] - y[0]) <= tol and abs(x[1] - y[1]) <= tol for x, y in zip(a, b))
    return ok >= frac * len(a)

rows = []
pieces = knobs.pieces()
for kind, pid, abc in pieces:
    if "[Q:" in abc or abc.count("Q:") > 1: continue   # mid-piece tempo changes: parse_midi keeps only the first tempo
    base = secnotes(abc); r = dict(kind=kind, pid=pid, reward=hc.reward(abc))
    for f in (2, 0.5):
        a2 = knobs2.renotate(abc, f); r[f"x{f}_identical_audio"] = same(base, secnotes(a2)); r[f"x{f}_reward"] = hc.reward(a2)
    rows.append(r)
ok = [r for r in rows if r["x2_identical_audio"] and r["x0.5_identical_audio"]]
sw = [max(r["reward"], r["x2_reward"], r["x0.5_reward"]) - min(r["reward"], r["x2_reward"], r["x0.5_reward"]) for r in ok if r["kind"] == "real"]
out = dict(n_checked=len(rows), n_identical_audio=len(ok), n_real_identical=len(sw),
           real_swing_median=round(st.median(sw), 3), real_swing_max=round(max(sw), 3),
           real_x2_median_delta=round(st.median(r["x2_reward"] - r["reward"] for r in ok if r["kind"] == "real"), 3),
           real_x05_median_delta=round(st.median(r["x0.5_reward"] - r["reward"] for r in ok if r["kind"] == "real"), 3),
           examples=sorted(ok, key=lambda r: -(max(r["reward"], r["x2_reward"], r["x0.5_reward"]) - min(r["reward"], r["x2_reward"], r["x0.5_reward"])))[:6])
json.dump(dict(summary=out, rows=rows), open("verify_renotate.json", "w"), indent=1); print(json.dumps(out, indent=1))
