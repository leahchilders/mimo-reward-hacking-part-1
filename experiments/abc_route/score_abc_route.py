"""Score 80 random PDMX piano pieces (sample listed in sources.json) through the SAME ABC path used for model outputs.

MusicXML (.mxl) --xml2abc v177 (no flags)--> ABC --> pipeline.compute_score("```abc\\n...```")
(identical to Harbor grade.py: extract_abc -> do -> gates -> total/100), same abc2midi binary.
Variants:
  raw      = xml2abc v177 with no flags
  stripped = raw with whitespace-only lines removed (the blank-line gate)
  norm     = xml2abc -d 16 --nbr (uniform L:1/16, no broken-rhythm '>' spelling) + drop fingering
             decorations !<digits>! + move U: definitions above K:  -- all MIDI-neutral re-spellings
Remaining gate failures under 'norm' are classified as real (source irregularities or abc2midi rejections).
Also scores the hack pieces."""
import os, sys, json, re, csv, glob, subprocess as sp, statistics as st, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common"))
import config  # sets ABC2MIDI_BIN, aliases the upstream scorer as `music_scorer`
from music_scorer.pipeline import compute_score, do, extract_abc, _get_ref
from music_scorer.feats import analyze
from music_scorer.score import score as sc
XML2ABC = config.XML2ABC
OUT = HERE



def grade(abc):
    """compute_score reward + the gate record from do() on the same extracted ABC."""
    text = "```abc\n" + abc + "\n```"
    reward = compute_score("music", text)
    ex = extract_abc(text)
    r = do(dict(key="k", id=0, rep=0, abc=ex, tag=None, lang=None, abc_len=len(ex), nvoice=0, latency=None))
    gates = []
    if r.get("skip"): gates.append("skip:" + str(r["skip"]))
    if r.get("err", 0) > 0: gates.append(f"abc2midi_Error x{r['err']}")
    if r.get("bar", 0) >= 10: gates.append(f"bar_warnings x{r['bar']}")
    if r.get("blank"): gates.append("blank_line")
    if r.get("ch_conflict", 0) > 0: gates.append(f"ch_conflict x{r['ch_conflict']}")
    if "total" not in r and not r.get("skip"): gates.append("no_total")
    return reward, r, gates

def first_errors(abc, n=3):
    with tempfile.TemporaryDirectory() as td:
        ap = td + "/a.abc"; open(ap, "w").write(abc)
        p = sp.run([os.environ["ABC2MIDI_BIN"], ap, "-o", td + "/a.mid"], capture_output=True)
        log = (p.stdout + p.stderr).decode("utf-8", "replace")
    return [l[:120] for l in log.splitlines() if l.startswith("Error")][:n]

def normalize(abc):
    abc = re.sub(r"!\d+!", "", abc)                      # fingerings: typeset-only, abc2midi chokes on '.!1!B'
    lines = abc.split("\n")
    u = [l for l in lines if l.startswith("U:")]
    lines = [l for l in lines if not l.startswith("U:")]
    k = next(i for i, l in enumerate(lines) if l.startswith("K:"))
    return "\n".join(lines[:k] + u + lines[k:])

def source_irregular(mxl):
    """Measures (excluding first/last) whose notated length != time-signature bar length, any staff."""
    from music21 import converter
    sc_ = converter.parse(mxl); n = 0; tot = 0
    for part in sc_.parts:
        ms = list(part.getElementsByClass("Measure"))
        for m in ms[1:-1]:
            ts = m.getContextByClass("TimeSignature")
            if ts is None: continue
            tot += 1
            if abs(float(m.duration.quarterLength) - float(ts.barDuration.quarterLength)) > 1e-6: n += 1
    return n, tot

def strip_blank(abc):
    return "\n".join(l for l in abc.split("\n") if l.strip()) + "\n"

if __name__ == "__main__":
    src = json.load(open(OUT + "/sources.json"))
    os.makedirs(OUT + "/abc", exist_ok=True); os.makedirs(OUT + "/abc_norm", exist_ok=True)
    py = sys.executable
    rows = []
    for i, h in enumerate(src):
        pid = f"{h['sample']}{i % 40:02d}"
        mxl = config.pdmx_mxl(h["mxl_rel"])
        p = sp.run([py, XML2ABC, mxl], capture_output=True, timeout=300)
        abc = p.stdout.decode("utf-8", "replace")
        xlog = p.stderr.decode("utf-8", "replace").strip().splitlines()
        open(f"{OUT}/abc/{pid}.abc", "w").write(abc)
        rw, rr, g = grade(abc)
        abc_s = strip_blank(abc)
        rw_s, rs, g_s = grade(abc_s)
        pn = sp.run([py, XML2ABC, "-d", "16", "--nbr", mxl], capture_output=True, timeout=300)
        abc_n = normalize(pn.stdout.decode("utf-8", "replace"))
        open(f"{OUT}/abc_norm/{pid}.abc", "w").write(abc_n)
        rw_n, rn, g_n = grade(abc_n)
        irr, nmeas = source_irregular(mxl)
        nvoices = len(set(re.findall(r"^V:\s*(\S+)", abc, re.M)))
        blank_lines = sum(1 for l in abc.split("\n")[:-1] if not l.strip())
        row = dict(id=pid, pdmx_path=h["mxl_rel"], title=h["row_title"][:60], composer=h["composer_name"][:40],
                   license=h["license"], license_conflict=h["license_conflict"],
                   abc_raw=round(rw, 3), gates_raw=";".join(g), quality_raw_ungated=rr.get("total"),
                   abc_stripped=round(rw_s, 3), gates_stripped=";".join(g_s), quality_stripped_ungated=rs.get("total"),
                   abc_norm=round(rw_n, 3), gates_norm=";".join(g_n), quality_norm_ungated=rn.get("total"),
                   src_irregular_measures=f"{irr}/{nmeas}",
                   err=rs.get("err"), bar_warn=rs.get("bar"), err_norm=rn.get("err"), bar_warn_norm=rn.get("bar"),
                   ch_conflict=rs.get("ch_conflict"), blank_lines_raw=blank_lines,
                   abc_voices=nvoices, abc_n_chan=rs.get("n_chan"), abc_chars=len(abc),
                   first_errors=" | ".join(first_errors(abc_n)) if rn.get("err") else "",
                   xml2abc_msg=(xlog[-1][-80:] if xlog else ""))
        rows.append(row)
        print(pid, row["abc_raw"], row["abc_stripped"], row["abc_norm"], row["gates_norm"] or "-", row["src_irregular_measures"], row["title"][:40], flush=True)
    with open(OUT + "/per_piece.csv", "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
    # hack pieces
    hk = []
    for fp in sorted(glob.glob(config.EXAMPLES + "/hack_hillclimb*.abc") + glob.glob(OUT + "/hack_pieces/climb_*.abc")):
        abc = open(fp).read(); rw, r, g = grade(abc)
        hk.append(dict(file=os.path.relpath(fp, config.ROOT), reward=round(rw, 3), gates=";".join(g), quality_ungated=r.get("total")))
        print("HACK", hk[-1])
    json.dump(dict(hacks=hk), open(OUT + "/hacks.json", "w"), indent=1)
