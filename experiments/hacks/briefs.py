"""The same answers scored under all 1,000 briefs (prompt passed as ground_truth/extra_info, exactly as
verl would), plus how badly the top hack violates each brief's requested meter / key / length / instrumentation."""
import json, re, collections, statistics as st
import pandas as pd
import hc
D = pd.read_parquet(hc.config.MIMO_BRIEFS)
answers = {k: open(f"pieces/{k}.abc").read() for k in ("climb_s2_st1_b16", "cell_tiny4_s3", "cell_loop1_s2")}
res = {}
for k, a in answers.items():
    vals = [hc.compute_score(row["data_source"], hc.wrap(a), row["reward_model"]["ground_truth"], dict(row["extra_info"], prompt=row["prompt"][0]["content"]))
            for _, row in D.iterrows()]
    res[k] = dict(n=len(vals), distinct=sorted(set(vals)), reward=vals[0])
# brief requirements vs the hack (C major, 4/4, 16 bars, 3 voices, piano)
ei = pd.DataFrame(list(D["extra_info"]))
txt = [r[0]["content"] for r in D["prompt"]]
meter_ne = int((ei["meter"] != "4/4").sum()); nv_ne = int((ei["nvoice_want"] != 3).sum())
cmaj = sum(1 for t in txt if re.search(r"\bC major\b|C大调", t))
lens = collections.Counter(ei["length"])
bars = [int(m.group(1) or m.group(2)) for t in txt for m in [re.search(r"about (\d+) bars|篇幅[^0-9。]*?(\d+)\s*小节", t)] if m]   # the requested length: "about N bars" / "篇幅N小节"
piano = sum(1 for t in txt if re.search(r"piano|钢琴", t, re.I))
out = {"identical_across_briefs": res, "brief_stats": dict(n=len(D), meter_not_4_4=meter_ne, nvoice_not_3=nv_ne,
       asks_C_major=cmaj, mentions_piano=piano, length_classes=dict(lens),
       requested_bars=dict(n=len(bars), median=st.median(bars), min=min(bars), max=max(bars), n_at_most_16=sum(b <= 16 for b in bars)),
       meters=dict(collections.Counter(ei["meter"]).most_common(8)), langs=dict(collections.Counter(ei["lang"])))}
json.dump(out, open("briefs.json", "w"), indent=1); print(json.dumps(out, indent=1))
