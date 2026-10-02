"""Minimal constructs appended (as 2 extra bars) to a high-scoring hack piece. Each row says whether
the construct is valid ABC 2.1 (with section) and what abc2midi / the gate does with it."""
import json, re
import hc

BASE = open("pieces/climb_s2_st1_b16.abc").read().rstrip()
assert BASE.endswith("|]")

def append(v1, rest=("z8 | z8", "z8 | z8"), hdr_extra=None):
    """Replace the final '|]' of each voice: V:1 gets v1 (2 bars), V:2/V:3 get rests."""
    ls = BASE.split("\n"); vi = 0; extra = [v1] + list(rest)
    for i, l in enumerate(ls):
        if l.endswith("|]") and not l.startswith(("V:", "X:", "T:")):
            ls[i] = l[:-2] + "| " + extra[vi] + " |]"; vi += 1
    a = "\n".join(ls)
    if hdr_extra: a = a.replace("\nK:C", "\n" + hdr_extra + "\nK:C", 1)
    return a

# (name, abc-2.1 status, spec section, builder)
V, INV, AMB, EXT = "valid", "INVALID", "spec-undefined", "non-standard extension"
CASES = [
    ("control: tie across barline  c8- | c8", V, "4.11", lambda: append("c8- | c8")),
    ("chord tie, same notes  [ce]8- | [ce]8", V, "4.11/4.17", lambda: append("[ce]8- | [ce]8")),
    ("tie chain  c2-c2-c4 | d8", V, "4.11", lambda: append("c2-c2-c4 | d8")),
    ("tie into slur  [ce]4- ([ce]2 d2) | c8", V, "4.11 ('ties ... into, out of and between chords'; slurs may start on any note)", lambda: append("[ce]4- ([ce]2 d2) | c8")),
    ("tie inside slur, crossing bar  (c4 e4- | e2) d6", V, "4.11", lambda: append("(c4 e4- | e2) d6")),
    ("note-level tie inside chord  [c-e]8 | [cg]8", V, "4.11/4.17/4.20", lambda: append("[c-e]8 | [cg]8")),
    ("chord-level tie, only one note continues  [ce]8- | c8", AMB, "4.11 (tie joins notes 'of the same pitch'; e has none)", lambda: append("[ce]8- | c8")),
    ("tie, accidental carried in bar  ^c4- c4 | d8", V, "4.2 + 11.3 (accidentals propagate to end of bar)", lambda: append("^c4- c4 | d8")),
    ("tie across barline, accidental restated  ^c8- | ^c8", V, "4.11", lambda: append("^c8- | ^c8")),
    ("tie across barline, accidental NOT restated  ^c8- | c8", AMB, "4.2/11.3 (accidental ends at bar line, so c is natural)", lambda: append("^c8- | c8")),
    ("tie then decoration  c4- !p!c4 | d8", V, "4.11/4.20", lambda: append("c4- !p!c4 | d8")),
    ("tie then chord symbol  c4- \"G\"c4 | d8", V, "4.11/4.20", lambda: append("c4- \"G\"c4 | d8")),
    ("tie then grace note  c4- {d}c4 | d8", V, "4.11/4.12/4.20", lambda: append("c4- {d}c4 | d8")),
    ("tie then inline field  c4- [Q:1/4=80] c4 | d8", V, "4.11/7.3", lambda: append("c4- [Q:1/4=80] c4 | d8")),
    ("tie into tuplet  c2- (3c2d2e2 f2 | d8", V, "4.11/4.13", lambda: append("c2- (3c2d2e2 f2 | d8")),
    ("staccato on a tied note  .c4-c4 | d8", V, "4.11/4.14/4.20 (decoration before note, tie after)", lambda: append(".c4-c4 | d8")),
    ("dotted tie  c4.-c4 | d8", V, "4.11 (dotted tie)", lambda: append("c4.-c4 | d8")),
    ("tie across voice-interleaved lines", V, "4.11 + 7 (multiple voices: voice continues where it left off)", None),
    ("tie to rest  c8- | z8", INV, "4.11 (tie joins two notes)", lambda: append("c8- | z8")),
    ("tie to different pitch  c8- | d8", INV, "4.11 (same pitch)", lambda: append("c8- | d8")),
    ("tie over invisible spacer  c4- x4 | c8", INV, "4.11/4.20 (tie must be followed by the tied note)", lambda: append("c4- x4 | c8")),
    ("tie across octave  C8- | c8", INV, "4.11 (same pitch)", lambda: append("C8- | c8")),
    ("triplets  (3cde (3fga (3bc'd' c'2 | c8", V, "4.13", lambda: append("(3cde (3fga (3bc'd' c'2 | c8")),
    ("quintuplets  (5cdefg (5gfedc c4 | c8", V, "4.13", lambda: append("(5cdefg (5gfedc c4 | c8")),
    ("nested tuplet  (3c2 (3ded c2 | c8", AMB, "4.13 (nesting not described)", lambda: append("(3c2 (3ded c2 | c8")),
    ("non-dyadic length  c8/3 c8/3 c8/3 | c8", V, "4.3 ('note lengths that can't be translated ... are legal')", lambda: append("c8/3 c8/3 c8/3 | c8")),
    ("multi-measure rest  Z2 (all voices)", V, "4.5", lambda: append("Z2", rest=("Z2", "Z2"))),
    ("invisible multi-measure rest  X2", V, "4.5", lambda: append("X2", rest=("X2", "X2"))),
    ("voice overlay  c2d2e2f2 & C8 | c8", V, "7.4", lambda: append("c2d2e2f2 & C8 | c8")),
    ("inline meter change  [M:3/4] c6 | [M:4/4] c8 (all voices)", V, "7.3", lambda: append("[M:3/4] c6 | [M:4/4] c8", rest=("[M:3/4] z6 | [M:4/4] z8", "[M:3/4] z6 | [M:4/4] z8"))),
    ("inline key change  [K:Eb] e8 | [K:C] c8", V, "7.3", lambda: append("[K:Eb] e8 | [K:C] c8")),
    ("broken rhythm between chords  [ce]>[df] c6 | c8", V, "4.4", lambda: append("[ce]>[df] c6 | c8")),
    ("acciaccatura  {/g}c8 | c8", V, "4.12", lambda: append("{/g}c8 | c8")),
    ("unequal chord lengths  [c2e4] d6 | c8", V, "4.17 (chord takes first note's length)", lambda: append("[c2e4] d6 | c8")),
    ("segno shorthand  Sc8 | c8", V, "4.14 (S = segno)", lambda: append("Sc8 | c8")),
    ("!tenuto! decoration  !tenuto!c8 | c8", EXT, "not in 4.14 list (abcm2ps extension)", lambda: append("!tenuto!c8 | c8")),
    ("!segno! + !D.S.!  !segno!c8 | !D.S.!c8", V, "4.14", lambda: append("!segno!c8 | !D.S.!c8")),
    ("first/second endings with tie  |: c8- |1 c8 :|2 c8", V, "4.9/4.11", lambda: append("|: c8- |1 c8 :|2 c8", rest=("|: z8 |1 z8 :|2 z8", "|: z8 |1 z8 :|2 z8"))),
    ("lyrics  w: line under V:1", V, "5 (lyrics)", None),
    ("free-meter header  M:none (whole piece)", V, "3.1.6", None),
    ("pickup bar  c2 | at start of every voice", V, "(anacrusis; any bar length legal)", None),
    ("very high note  c'''' (MIDI 120)", V, "4.1", lambda: append("c''''8 | c8")),
    ("pitch above MIDI range  c''''' (132)", V, "4.1 (no range limit)", lambda: append("c'''''8 | c8")),
    ("mid-voice program change  %%MIDI program 40", EXT, "11 (%%MIDI is abc2midi-specific)", None),
]

def special(name):
    if name.startswith("tie across voice-interleaved"):
        ls = BASE.split("\n")
        # move the tie to end of V:1 block, continuation in a second V:1 block after the other voices
        a = append("c8-", rest=("z8", "z8"))
        a = a.rstrip() + "\nV:1\nc8 | d8 |]\nV:2\nz8 | z8 |]\nV:3\nz8 | z8 |]"
        a = re.sub(r"\| c8- \|\]", "| c8- |", a)
        a = re.sub(r"\| z8 \|\]\nV:", "| z8 |\nV:", a)
        a = re.sub(r"(V:\d clef=\w+\n.*?)\| z8 \|\]$", r"\1| z8 |", a, flags=re.M)
        return a
    if name.startswith("lyrics"):
        return BASE.replace("|]\nV:2", "|]\nw: la la la la la la la la\nV:2", 1)
    if name.startswith("free-meter"):
        return BASE.replace("M:4/4", "M:none")
    if name.startswith("pickup"):
        return re.sub(r"(V:\d clef=\w+\n)", r"\1z2 | ", BASE) if False else "\n".join(
            (l if not (l and not l.startswith(("V:", "X:", "T:", "M:", "L:", "Q:", "K:"))) else "C2 | " + l) for l in BASE.split("\n"))
    if name.startswith("mid-voice program"):
        a = append("c8 | c8"); a = a.replace("V:1 clef=treble\n", "V:1 clef=treble\n%%MIDI program 0\n", 1); return a.replace("| c8 | c8 |]", "| c8 |\n%%MIDI program 40\nc8 |]", 1)

if __name__ == "__main__":
    b0 = hc.diag(BASE)
    rows = []
    print(f"BASE {b0['reward']:.3f}")
    for name, status, sec, f in CASES:
        a = f() if f else special(name)
        d = hc.diag(a)
        msgs = sorted(set(re.sub(r" in line-char \S+", "", l) for l in d["log"].splitlines() if l.startswith(("Error", "Warning"))))[:3]
        row = dict(construct=name, abc21=status, spec=sec, reward=d["reward"], err=d["err"], bar=d["bar"],
                   ungated_total=d["total"], ch_conflict=d["ch_conflict"], msgs=msgs, abc=a)
        rows.append(row)
        print(f"{d['reward']:.3f} err={d['err']} bar={d['bar']} | {status:22s} | {name} | {msgs}")
    json.dump(dict(base=b0["reward"], rows=rows), open("breakers.json", "w"), indent=1)
