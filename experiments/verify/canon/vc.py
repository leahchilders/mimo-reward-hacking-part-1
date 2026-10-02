"""Independent re-derivation helpers for the canon claims.

Pipeline: MusicXML -> xml2abc v177 (-d 16 --nbr) -> norm (strip !N! fingerings,
move U: lines above K:) -> compute_score("music", "```abc\n"+abc+"\n```").
Written from scratch; does not import the canon/ probe scripts.
"""
import os, re, sys, struct, subprocess as sp, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "common"))
import config  # noqa: E402  (sets ABC2MIDI_BIN, aliases the upstream scorer as `mscorer`)
XML2ABC = config.XML2ABC
ABC2MIDI = config.ABC2MIDI_BIN
PDMX = config.pdmx_mxl_dir() if config.PDMX_ROOT or os.environ.get("PDMX_MXL_DIR") else None
import mscorer  # noqa: E402
from mscorer import compute_score  # noqa: E402
from mscorer.pipeline import do  # noqa: E402


def xml2abc(path, timeout=300):
    p = sp.run([sys.executable, XML2ABC, "-d", "16", "--nbr", path],
               capture_output=True, timeout=timeout)
    return p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


_FING = re.compile(r"!\d+!")


def norm(abc):
    abc = _FING.sub("", abc)
    lines = abc.split("\n")
    u = [l for l in lines if l.startswith("U:")]
    rest = [l for l in lines if not l.startswith("U:")]
    if u:
        k = next((i for i, l in enumerate(rest) if l.startswith("K:")), None)
        if k is not None:
            rest = rest[:k] + u + rest[k:]
    return "\n".join(rest)


def score_abc(abc):
    """Returns (reward via compute_score, do() record)."""
    sol = "```abc\n" + abc + "\n```"
    reward = compute_score("music", sol)
    body = mscorer.pipeline.extract_abc(sol)
    r = do(dict(key="v", id=0, rep=0, abc=body))
    return reward, r


def abc2midi_run(abc, keep_dir=None):
    td = keep_dir or tempfile.mkdtemp()
    ap, mp = os.path.join(td, "a.abc"), os.path.join(td, "a.mid")
    open(ap, "w").write(abc)
    p = sp.run([ABC2MIDI, ap, "-o", mp], capture_output=True, timeout=120)
    log = (p.stdout + p.stderr).decode("utf-8", "replace")
    data = open(mp, "rb").read() if os.path.exists(mp) else b""
    return log, data


def midi_notes(data):
    """Own minimal SMF parser -> (div, [(onset, dur, ch, pitch)])."""
    _fmt, ntrk, div = struct.unpack(">HHH", data[8:14])
    i, out = 14, []
    for _ in range(ntrk):
        assert data[i:i + 4] == b"MTrk"
        ln = struct.unpack(">I", data[i + 4:i + 8])[0]
        j, end, t, rs, on = i + 8, i + 8 + ln, 0, None, {}

        def vlq():
            nonlocal j
            v = 0
            while True:
                b = data[j]; j += 1
                v = (v << 7) | (b & 0x7F)
                if not b & 0x80:
                    return v
        while j < end:
            t += vlq()
            st = data[j]
            if st == 0xFF:
                j += 2; L = vlq(); j += L; continue
            if st in (0xF0, 0xF7):
                j += 1; L = vlq(); j += L; continue
            if st & 0x80:
                rs = st; j += 1
            k, ch = rs & 0xF0, rs & 0x0F
            if k in (0xC0, 0xD0):
                j += 1; continue
            a, b = data[j], data[j + 1]; j += 2
            if k == 0x90 and b > 0:
                on.setdefault((ch, a), []).append(t)
            elif k in (0x80, 0x90):
                q = on.get((ch, a))
                if q:
                    t0 = q.pop(0); out.append((t0, t - t0, ch, a))
        i = end
    return div, sorted(out)


def m21_notes(path, expand=True):
    import music21 as m21
    s = m21.converter.parse(path)
    nb = len(s.parts[0].getElementsByClass("Measure")) if s.parts else 0
    if expand:
        try:
            s = s.expandRepeats()
        except Exception:
            pass
    s = s.stripTies()
    ev = []
    for n in s.flatten().notes:
        if n.duration.isGrace:
            continue
        off = float(n.getOffsetInHierarchy(s))
        for p in n.pitches:
            ev.append((off, p.midi))
    return nb, ev, s


def fidelity(src_ev, div, mnotes):
    from collections import Counter
    q = lambda x: round(x * 12) / 12
    A = Counter((q(o), p) for o, p in src_ev)
    B = Counter((q((o + 1) / div), p) for o, d, ch, p in mnotes)  # undo +1 tick
    inter = sum((A & B).values())
    f1 = 2 * inter / (sum(A.values()) + sum(B.values())) if A and B else 0
    PA = Counter(p for _, p in src_ev); PB = Counter(p for *_, p in mnotes)
    pov = sum((PA & PB).values()) / max(sum(PA.values()), sum(PB.values()))
    return dict(n_src=len(src_ev), n_midi=len(mnotes), onset_pitch_f1=round(f1, 3),
                pitch_multiset_overlap=round(pov, 3),
                pitchset_equal=set(PA) == set(PB))
