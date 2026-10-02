"""Scoring helpers for search.py and climb.py: compute_score (the reward) plus a per-feature view."""
import os, sys, json, subprocess, tempfile, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "common"))
import config  # sets ABC2MIDI_BIN, aliases the upstream scorer as `music_scorer`
from music_scorer.pipeline import do, compute_score, _get_ref
from music_scorer.feats import analyze
from music_scorer.score import score as sc

def score_abc(abc, show=False):
    rec = {"key":"p","id":0,"rep":0,"abc":abc,"tag":None,"lang":None,"abc_len":len(abc),"nvoice":0,"latency":None}
    r = do(rec)
    reward = compute_score("music", "```abc\n"+abc+"\n```")
    # per-feature
    with tempfile.TemporaryDirectory() as td:
        ap=os.path.join(td,"a.abc"); mp=os.path.join(td,"a.mid")
        open(ap,"w").write(abc)
        subprocess.run([os.environ["ABC2MIDI_BIN"],ap,"-o",mp],capture_output=True)
        f = analyze(mp) if os.path.exists(mp) else {"skip":"nomidi"}
    s = sc(f,_get_ref()) if not f.get("skip") else None
    return reward, r, f, s

def score_midi(path):
    f = analyze(path)
    s = sc(f,_get_ref())
    return s["total"]/100, f, s
