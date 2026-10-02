"""Check: are the bar-warning gate failures caused by fermatas? (abc2midi lengthens fermata notes by default,
so a fermata on a full-bar note over-fills that bar -> 'Bar N has X time units' warning, per voice).
Re-grades each zeroed piece with only the '!fermata!' / 'H' decorations removed (MIDI otherwise identical)."""
import os, sys, re, json, csv
sys.argv = sys.argv[:1]
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
import score_one as S  # sets ABC2MIDI_BIN + scorer path
from music_scorer import pipeline
import pandas as pd
pp = pd.read_csv(D + "/per_piece_full.csv", low_memory=False)
z = pp[pp.zeroed & pp.group.isin(["m21_bach_chorales", "pdmx_canon"]) & pp.gates.fillna("").str.contains("bar_warnings")]
out = []
for r in z.itertuples():
    abc = open(f"{D}/abc/{r.cid}.abc").read()
    n_ferm = abc.count("!fermata!")
    abc2 = abc.replace("!fermata!", "")
    rr = pipeline.do(dict(key="k", id=0, rep=0, abc=abc2.strip(), tag=None, lang=None, abc_len=0, nvoice=0, latency=None))
    out.append(dict(cid=r.cid, group=r.group, title=r.title[:60], n_fermata=n_ferm, bar_before=r.bar_warn, err_before=r.err,
                    bar_after=rr.get("bar"), err_after=rr.get("err"), passes_after=int(not rr.get("reject") and "total" in rr),
                    total_after=rr.get("total")))
o = pd.DataFrame(out); o.to_csv(D + "/fermata_check.csv", index=False)
for g, s in o.groupby("group"):
    print(g, "n", len(s), "with fermatas", (s.n_fermata > 0).sum(), "pass after removing fermatas", s.passes_after.sum(),
          "median bar warn before/after", s.bar_before.median(), s.bar_after.median())
