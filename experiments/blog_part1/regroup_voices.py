"""music21's ABC reader mis-handles inline-interleaved voices ("[V:1] ... |" lines):
it puts every voice's bars into every part (192 bars instead of 64). Regroup into
contiguous V: blocks (same music, same abc2midi MIDI), verify the score is unchanged,
then write MusicXML and check bar counts."""
import os, sys, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "common"))
from vm_common import compute_score
import config
import music21

def regroup(abc):
    head, body, order = [], {}, []
    decl = {}
    for line in abc.splitlines():
        m = re.match(r"^\[V:(\S+)\]\s*(.*)$", line)
        if m:
            v = m.group(1); body.setdefault(v, []).append(m.group(2))
            if v not in order: order.append(v)
            continue
        d = re.match(r"^V:(\S+)(.*)$", line)
        if d:
            decl[d.group(1)] = [line]; order.append(d.group(1)) if d.group(1) not in order else None; cur = d.group(1); continue
        if line.startswith("%%MIDI") and decl:
            decl[list(decl)[-1]].append(line); continue
        head.append(line)
    k = [i for i, l in enumerate(head) if l.startswith("K:")][0]
    out = head[:k + 1]
    for v in order:
        out += decl.get(v, [f"V:{v}"]) + body.get(v, [])
    return "\n".join(out) + "\n"

for name in ["hack_hillclimb_staccato", "hack_hillclimb", "hack_wrong_brief_quartet"]:
    p = os.path.join(config.EXAMPLES, f"{name}.abc"); abc = open(p).read()
    g = regroup(abc)
    s0 = compute_score("music", "```abc\n" + abc + "\n```"); s1 = compute_score("music", "```abc\n" + g + "\n```")
    sc = music21.converter.parse(g, format="abc")
    sc.write("musicxml", fp=os.path.join(config.EXAMPLES, f"{name}.musicxml"))
    print(name, "score orig", round(s0, 3), "regrouped", round(s1, 3), "bars/part", [len(pt.getElementsByClass('Measure')) for pt in sc.parts])
