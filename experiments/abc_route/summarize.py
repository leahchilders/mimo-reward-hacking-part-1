"""Aggregate per_piece.csv + hacks.json into summary statistics (printed)."""
import csv, json, statistics as st, collections
rows = list(csv.DictReader(open("per_piece.csv"))); hk = json.load(open("hacks.json"))["hacks"]
def stats(v): return f"n={len(v)} median {st.median(v):.3f} mean {st.mean(v):.3f} min {min(v):.3f} max {max(v):.3f}"
for samp in ["A", "B", "all"]:
    R = [r for r in rows if samp == "all" or r["id"][0] == samp]
    print(f"--- sample {samp}")
    for k in ["abc_raw", "abc_stripped", "abc_norm"]:
        v = [float(r[k]) for r in R]; p = [x for x in v if x > 0]
        print(f" {k:13s} all      ", stats(v), f"| zeroed {sum(x == 0 for x in v)}")
        print(f" {k:13s} pass-only", stats(p))
    q = [float(r["quality_norm_ungated"]) / 100 for r in R if r["quality_norm_ungated"]]
    print(" norm, ungated quality", stats(q))
cnt = collections.Counter()
for r in rows:
    for g in r["gates_norm"].split(";"):
        if g: cnt[g.split(" ")[0]] += 1
print("norm gate firings (pieces):", dict(cnt))
print("raw gate firings (pieces):", dict(collections.Counter(g.split(" ")[0] for r in rows for g in r["gates_raw"].split(";") if g)))
print("blank-line gate fired raw:", sum("blank" in r["gates_raw"] for r in rows), " blank lines in raw xml2abc output (excl. trailing):", sum(int(r["blank_lines_raw"]) for r in rows))
hv = [h["reward"] for h in hk]; print("hacks", stats(hv), "all gates clear:", all(not h["gates"] for h in hk))
real = sorted(float(r["abc_norm"]) for r in rows if float(r["abc_norm"]) > 0)
for h in hk: print("  ", h["file"], h["reward"], "beats %d/%d passing real pieces (norm)" % (sum(x < h["reward"] for x in real), len(real)))
