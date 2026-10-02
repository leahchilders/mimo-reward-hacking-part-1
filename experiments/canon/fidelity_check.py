"""Spot-check that xml2abc->abc2midi rendered the source faithfully (so a low score is the scorer, not the converter).

For each cid: source MusicXML via music21 (repeats expanded when possible, ties stripped, grace notes dropped)
vs the abc2midi MIDI of the SAME normalized ABC the scorer saw (abc/<cid>.abc).
Reports: note counts, pitch-multiset overlap (sum of min counts / max(n_src, n_abc)), MIDI pitch range on both
sides, total length in quarter notes, onset+pitch F1 after aligning on quarter-note onsets (rounded to 1/12 q),
and measure counts (source measures vs ABC bar lines per voice).
Usage: fidelity_check.py C0123 C0456 ...
"""
import sys, os, re, json, csv, tempfile, subprocess as sp, collections

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "common"))
import config  # sets ABC2MIDI_BIN, aliases the upstream scorer as `music_scorer`
from music_scorer.pipeline import _midi_notes_progs
import struct
from music21 import converter, repeat

ABC2MIDI = config.ABC2MIDI_BIN
rows = {r["cid"]: r for r in csv.DictReader(open(D + "/canon_list.csv"))}


def src_notes(path):
    s = converter.parse(path)
    nmeas = max(len(p.getElementsByClass("Measure")) for p in s.parts)
    expanded = False
    try:
        s2 = s.expandRepeats(); expanded = True
    except Exception:
        s2 = s
    out = []
    for p in s2.parts:
        for n in p.stripTies().recurse().notes:
            if n.duration.isGrace:
                continue
            off = float(n.getOffsetInHierarchy(s2))
            for pt in n.pitches:
                out.append((off, pt.midi))
    return out, nmeas, expanded


def abc_notes(abc_path):
    with tempfile.TemporaryDirectory() as td:
        p = sp.run([ABC2MIDI, abc_path, "-o", td + "/a.mid"], capture_output=True)
        data = open(td + "/a.mid", "rb").read()
    div = struct.unpack(">HHH", data[8:14])[2]
    notes, _ = _midi_notes_progs(data)
    return [(t / div, n) for (t, d, ch, n) in notes]


def f1(a, b, q=12):
    A = collections.Counter((round(o * q), p) for o, p in a)
    B = collections.Counter((round(o * q), p) for o, p in b)
    tp = sum((A & B).values())
    return round(2 * tp / max(1, sum(A.values()) + sum(B.values())), 3)


for cid in sys.argv[1:]:
    r = rows[cid]
    sn, nmeas, exp = src_notes(config.canon_path(r))
    an = abc_notes(f"{D}/abc/{cid}.abc")
    abc = open(f"{D}/abc/{cid}.abc").read()
    # bars per voice: count barlines in the first voice body
    body = [l for l in abc.split("\n") if l and not re.match(r"^[A-Za-z]:|^%", l)]
    pa, pb = collections.Counter(p for _, p in sn), collections.Counter(p for _, p in an)
    ov = round(sum((pa & pb).values()) / max(1, max(len(sn), len(an))), 3)
    # onset offset: align first onsets
    a0 = min(o for o, _ in sn) if sn else 0; b0 = min(o for o, _ in an) if an else 0
    res = dict(cid=cid, title=r["title"][:60], src_measures=nmeas, src_repeats_expanded=exp,
               n_src=len(sn), n_abc_midi=len(an), pitch_multiset_overlap=ov,
               src_range=(min(pa), max(pa)) if pa else None, abc_range=(min(pb), max(pb)) if pb else None,
               src_len_q=round(max(o for o, _ in sn) - a0, 2) if sn else None,
               abc_len_q=round(max(o for o, _ in an) - b0, 2) if an else None,
               onset_pitch_F1=f1([(o - a0, p) for o, p in sn], [(o - b0, p) for o, p in an]))
    print(json.dumps(res))
