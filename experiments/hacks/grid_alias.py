"""The six sonority features (polyphony_rate/mean, roughness, harmonicity, tensile strain -> tension_peaks) sample the
texture only at exact half-beat ticks (feats._sonorities, grid=0.5, test o <= t < o+d). Notes that start just after a
grid tick and end before the next are invisible to them. Two ways to make such notes: off-beat 16ths, and abc2midi
guitar-chord accompaniment (rendered 1 tick late, 239 ticks long)."""
import json, hc
BASE = open("pieces/climb_s2_st1_b16.abc").read().rstrip()
def add_voice(body): return BASE + "\nV:9 clef=bass\n" + body
on16  = " | ".join(["[C,E,G,]/ z/ z [C,E,G,]/ z/ z [C,E,G,]/ z/ z [C,E,G,]/ z/ z"] * 16) + " |]"
off16 = " | ".join(["z/ [C,E,G,]/ z z/ [C,E,G,]/ z z/ [C,E,G,]/ z z/ [C,E,G,]/ z"] * 16) + " |]"
gch   = " | ".join(['"C"x8'] * 16) + " |]"
rows = {}
for name, a in [("base", BASE), ("+ on-beat 16th triads", add_voice(on16)), ("+ off-beat 16th triads", add_voice(off16)),
                ("+ guitar-chord accompaniment (\"C\" on rests)", add_voice(gch))]:
    d = hc.diag(a); f = d["feat"]
    rows[name] = dict(reward=d["reward"], n_note=f["n_note"], polyphony_rate=f["polyphony_rate"], polyphony_mean=f["polyphony_mean"],
                      roughness_p90=f["roughness_p90"], harmonicity_mean=f["harmonicity_mean"], tension_peaks=f["tension_peaks"],
                      pitch_min=f["pitch_min"], key_certainty=f["key_certainty"], n_chan=f["n_chan"])
json.dump(rows, open("grid_alias.json", "w"), indent=1); print(json.dumps(rows, indent=1))

# part 2: abc2midi starts every note 1 tick late but ends it on time (1 tick short); how many notes never cover a sampling tick?
import csv, os, statistics as st, glob
def invisible_frac(abc):
    d = hc.diag(abc); div = 480  # abc2midi default division
    from mscorer.core import parse_midi
    step = 240
    notes = [n for n in d["notes"] if n[2] != 9]
    inv = sum(1 for o, du, ch, p, v in notes if not any(o <= t < o + max(du, 1) for t in range(((o + step - 1) // step) * step, o + du, step)))
    return inv / len(notes)
demo = "X:1\nT:t\nM:4/4\nL:1/8\nK:C\nV:1\nc d .e .f c2 .c2 | c8 |]\nV:2\nC,8 | C,8 |]"
dd = hc.diag(demo)
real = [r["id"] for r in csv.DictReader(open(os.path.join(os.path.dirname(hc.HERE), "abc_route", "per_piece.csv"))) if float(r["abc_norm"]) > 0]
fr = [invisible_frac(hc.load_norm(p)) for p in real]
hk = [invisible_frac(open(p).read()) for p in sorted(glob.glob("pieces/climb_s*_b16.abc"))]
part2 = dict(demo_notes=dd["notes"], real_n=len(fr), real_invisible_median=round(st.median(fr), 3), real_invisible_range=[round(min(fr), 3), round(max(fr), 3)],
             hack_n=len(hk), hack_invisible_median=round(st.median(hk), 3))
json.dump(dict(add_voice=rows, invisible=part2), open("grid_alias.json", "w"), indent=1); print(json.dumps(part2))
