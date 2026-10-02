"""Post-hoc: best-key gain, renotation on the identical-audio subset, per-piece oracle over iso-sonic notations."""
import json, statistics as st, collections
R1 = json.load(open("knobs_rows.json")); R2 = json.load(open("knobs2_rows.json"))
def tab(rows):
    t = collections.defaultdict(dict)
    for r in rows:
        if "reward" in r: t[(r["kind"], r["pid"])][r["knob"]] = r
    return t
T1, T2 = tab(R1), tab(R2)
out = []
for kind in ("real", "hack"):
    gains, bestk = [], collections.Counter()
    for k, d in T1.items():
        if k[0] != kind: continue
        cand = {0: d["BASE"]["reward"]}
        for s in range(-6, 6):
            if s: cand[s] = d[f"transpose {s:+d}"]["reward"]
        b = max(cand, key=cand.get); bestk[b] += 1; gains.append(cand[b] - cand[0])
    out.append(f"[{kind}] best-of-12-transpositions gain over written key: n={len(gains)} median {st.median(gains):+.3f} mean {st.mean(gains):+.3f} max {max(gains):+.3f}; written key already best in {bestk[0]}/{len(gains)}; best shift counts {dict(bestk)}")
    # renotation, identical-audio subset
    ok = [k for k, d in T2.items() if k[0] == kind and all("dur_sec" in d[n] and abs(d[n]["dur_sec"][0]-d[n]["dur_sec"][1]) <= 0.2 for n in ("renotate x2 (same audio)", "renotate x0.5 (same audio)"))]
    sw = []; orc = []
    for k in ok:
        d = T2[k]; v = [d["renotate x0.5 (same audio)"]["reward"], d["BASE"]["reward"], d["renotate x2 (same audio)"]["reward"]]
        sw.append(max(v) - min(v)); orc.append(max(v) - v[1])
    if ok:
        out.append(f"[{kind}] iso-sonic renotation (x0.5 / x1 / x2), identical-seconds subset n={len(ok)}: max-min swing median {st.median(sw):.3f} max {max(sw):.3f}; best-of-3 gain over as-written median {st.median(orc):+.3f}, max {max(orc):+.3f}, pieces that gain >0.01: {sum(x>0.01 for x in orc)}")
        ex = sorted(ok, key=lambda k: -max(T2[k][n]['reward'] for n in T2[k]) + 0)[:0]
        big = sorted(ok, key=lambda k: -(max(T2[k]['renotate x0.5 (same audio)']['reward'], T2[k]['renotate x2 (same audio)']['reward'], T2[k]['BASE']['reward']) - min(T2[k]['renotate x0.5 (same audio)']['reward'], T2[k]['renotate x2 (same audio)']['reward'], T2[k]['BASE']['reward'])))[:5]
        for k in big:
            d = T2[k]; out.append(f"    {k[1]}: x0.5 {d['renotate x0.5 (same audio)']['reward']:.3f} | as written {d['BASE']['reward']:.3f} | x2 {d['renotate x2 (same audio)']['reward']:.3f}")
open("analyze_knobs.txt", "w").write("\n".join(out) + "\n"); print("\n".join(out))
