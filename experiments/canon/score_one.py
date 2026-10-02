"""Score ONE piece through the MiMo model-output path; print one JSON line.

Path (identical to abc_route 'norm'):
  MusicXML/.mxl --xml2abc v177 -d 16 --nbr--> ABC --normalize (drop !N! fingering, U: above K:)-->
  "```abc\n...\n```" --pipeline.do() [abc2midi + gates + analyze + score]--> reward
reward is computed with exactly compute_score's logic (skip/reject -> 0, else clamp(total/100)); we
call do() once and intercept analyze()/_score_v1() to also keep the per-feature breakdown and the
raw feature values (the 'ungated quality' is r['total'] even when a gate fires).
For music21-corpus kern input, music21 first writes MusicXML (extra step, flagged in output).
Usage: score_one.py <path> [--check-compute-score]
"""
import os, sys, json, re, time, tempfile, subprocess as sp

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "common"))
import config  # sets ABC2MIDI_BIN, aliases the upstream scorer as `music_scorer`
from music_scorer import pipeline
from music_scorer.score import SPEC

XML2ABC = config.XML2ABC
CAP = {}
_orig_analyze, _orig_score = pipeline.analyze, pipeline._score_v1


def _an(p):
    f = _orig_analyze(p); CAP["feat"] = f; return f


def _sc(f, ref):
    s = _orig_score(f, ref); CAP["score"] = s; return s


pipeline.analyze, pipeline._score_v1 = _an, _sc


def normalize(abc):  # same as abc_route/score_abc_route.py
    abc = re.sub(r"!\d+!", "", abc)
    lines = abc.split("\n")
    u = [l for l in lines if l.startswith("U:")]
    lines = [l for l in lines if not l.startswith("U:")]
    k = next(i for i, l in enumerate(lines) if l.startswith("K:"))
    return "\n".join(lines[:k] + u + lines[k:])


def first_errors(abc, n=3):
    with tempfile.TemporaryDirectory() as td:
        ap = td + "/a.abc"; open(ap, "w").write(abc)
        p = sp.run([os.environ["ABC2MIDI_BIN"], ap, "-o", td + "/a.mid"], capture_output=True, timeout=60)
        log = (p.stdout + p.stderr).decode("utf-8", "replace")
    errs = [l[:110] for l in log.splitlines() if l.startswith("Error")]
    bars = [l[:80] for l in log.splitlines() if re.search(r"Bar \d+ has", l)]
    return errs[:n], bars[:2]


def main(path, check=False, save_abc=None):
    t0 = time.time()
    out = dict(path=path)
    src = path
    if path.endswith(".krn"):
        from music21 import converter
        td = tempfile.mkdtemp(); src = td + "/x.musicxml"
        converter.parse(path).write("musicxml", fp=src); out["via_m21_xml"] = True
    p = sp.run([sys.executable, XML2ABC, "-d", "16", "--nbr", src], capture_output=True, timeout=300)
    abc_raw = p.stdout.decode("utf-8", "replace")
    if "K:" not in abc_raw:
        out.update(status="xml2abc_fail", xml2abc_err=p.stderr.decode("utf-8", "replace")[-200:]); return out
    abc = normalize(abc_raw)
    if save_abc:
        open(save_abc, "w").write(abc)
    out["t_xml2abc"] = round(time.time() - t0, 2)
    text = "```abc\n" + abc + "\n```"
    ex = pipeline.extract_abc(text)
    r = pipeline.do(dict(key="k", id=0, rep=0, abc=ex, tag=None, lang=None, abc_len=len(ex), nvoice=0, latency=None))
    # reward exactly as compute_score
    if r.get("skip") or r.get("reject", 0) or "total" not in r:
        reward = 0.0
    else:
        reward = max(0.0, min(1.0, float(r["total"]) / 100.0))
    gates = []
    if r.get("skip"): gates.append("skip:" + str(r["skip"]))
    if r.get("err", 0) > 0: gates.append(f"abc2midi_Error x{r['err']}")
    if r.get("bar", 0) >= 10: gates.append(f"bar_warnings x{r['bar']}")
    if r.get("blank"): gates.append("blank_line")
    if r.get("ch_conflict", 0) > 0: gates.append(f"ch_conflict x{r['ch_conflict']}")
    if "total" not in r and not r.get("skip"): gates.append("no_total:" + str(r.get("scorer_skip", "")))
    out.update(status="ok", reward=round(reward, 4), quality_ungated=r.get("total"), gates=";".join(gates),
               err=r.get("err"), bar_warn=r.get("bar"), ch_conflict=r.get("ch_conflict"), n_chan=r.get("n_chan"),
               abc_chars=len(abc), abc_bars=sum(len(re.findall(r"\|", l)) for l in abc.split("\n")
                                                  if l and not re.match(r"^[A-Za-z]:|^%", l)),
               abc_voices=len(set(re.findall(r"^V:\s*(\S+)", abc, re.M))),
               xml2abc_msg=p.stderr.decode("utf-8", "replace").strip().splitlines()[-1][-100:] if p.stderr.strip() else "")
    if r.get("err") or r.get("bar", 0) >= 10:
        e, b = first_errors(ex); out["first_errors"] = " | ".join(e); out["first_barwarn"] = " | ".join(b)
    s = CAP.get("score"); f = CAP.get("feat") or {}
    if s:
        out["groups"] = s["groups"]; out["dist_score"] = s["dist_score"]; out["per_feature"] = s["per_feature"]
    out["feat"] = {k: f.get(k) for k, _, _ in SPEC}
    for k in ("n_note", "dur_sec", "bpm", "pitch_max", "key_tonic", "key_minor"):
        out["feat"][k] = f.get(k)
    if check:
        from music_scorer.pipeline import compute_score
        out["compute_score_check"] = compute_score("music", text)
    out["t_total"] = round(time.time() - t0, 2)
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    sv = None
    if "--save-abc" in a:
        i = a.index("--save-abc"); sv = a[i + 1]; del a[i:i + 2]
    try:
        res = main(a[0], "--check-compute-score" in a, sv)
    except Exception as e:
        res = dict(path=a[0], status="exception", error=repr(e)[:300])
    print(json.dumps(res))
