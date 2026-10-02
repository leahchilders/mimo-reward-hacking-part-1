"""Counterfactual: how much of each piece's score is the sonority-grid phase artifact?

abc2midi writes every note onset at +1 tick (chord members at +11/+21...) but ends it on time, so it is 1 tick short, while
feats._sonorities() samples 'sounding notes' only at exact grid points t = k * div/2 (every eighth note) with the
half-open test o <= t < o+d. A note of an eighth or shorter therefore never contains a grid point, so
fast-moving textures read as monophonic/silent to polyphony_rate, polyphony_mean, roughness_p90,
harmonicity_mean and (via the chord clouds) tension_peaks.
Here we re-score the SAME abc2midi MIDI with the grid sampled at t + 30 ticks (div=480 -> 1/64 note later),
everything else unchanged. 'orig' re-derives the shipped ungated total (sanity check).
Writes cf_grid_phase.csv. Usage: cf_grid_phase.py [workers]
"""
import os, sys, csv, json, glob, tempfile, subprocess as sp
from multiprocessing import Pool

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "common"))
import config  # sets ABC2MIDI_BIN, aliases the upstream scorer as `music_scorer`
import music_scorer.feats as F
from music_scorer.score import score
REF = json.load(open(config.REF_PATH))
ABC2MIDI = config.ABC2MIDI_BIN
_orig_son = F._sonorities
OFF = 30


def _son_shift(notes, div, grid=0.5):
    if not notes:
        return []
    step = max(1, int(div * grid)); off = OFF * div // 480
    end = max(n[0] + n[1] for n in notes)
    out = []
    for t in range(0, end + 1, step):
        cur = [(p, v) for (o, d, ch, p, v) in notes if ch != F.DRUM_CH and o <= t + off < o + max(d, 1)]
        if cur:
            out.append((t, cur))
    return out


def job(item):
    try:
        return _job(item)
    except Exception as e:
        return dict(key=item[0], status="exc:" + repr(e)[:80])


def _job(item):
    key, abc_path = item
    with tempfile.TemporaryDirectory() as td:
        mp = td + "/a.mid"
        sp.run([ABC2MIDI, abc_path, "-o", mp], capture_output=True, timeout=120)
        if not os.path.exists(mp):
            return dict(key=key, status="no_midi")
        res = dict(key=key)
        for tag, fn in (("orig", _orig_son), ("shift", _son_shift)):
            F._sonorities = fn
            f = F.analyze(mp)
            if f.get("skip"):
                return dict(key=key, status=f["skip"])
            s = score(f, REF)
            res[tag + "_total"] = s["total"]
            for g, v in s["groups"].items(): res[f"{tag}_grp_{g}"] = v
            for k in ("polyphony_rate", "polyphony_mean", "roughness_p90", "harmonicity_mean", "tension_peaks"):
                res[f"{tag}_{k}"] = f[k]
        res["status"] = "ok"
        return res


if __name__ == "__main__":
    items = [(os.path.basename(p)[:-4], p) for p in sorted(glob.glob(D + "/abc/*.abc"))]
    items += [("HACK:" + os.path.relpath(p, config.ROOT), p) for p in sorted(glob.glob(config.EXAMPLES + "/hack_hillclimb*.abc") + glob.glob(config.EXPERIMENTS + "/abc_route/hack_pieces/climb_*.abc"))]
    with Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 14) as pool:
        rows = []
        for i, r in enumerate(pool.imap_unordered(job, items, chunksize=2), 1):
            rows.append(r)
            if i % 200 == 0: print(i, flush=True)
    keys = sorted({k for r in rows for k in r})
    keys.remove("key"); keys = ["key"] + keys
    with open(D + "/cf_grid_phase.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(sorted(rows, key=lambda r: r["key"]))
    print("done", len(rows))
