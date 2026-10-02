"""ABC accidentals carry to the end of the bar (abc2midi honours this; music21's reader does not).
Make carried accidentals explicit in the quartet so the MusicXML shows what the scorer actually heard,
then confirm the reward is unchanged and the notes match the abc2midi MIDI."""
import os, sys, re, subprocess as sp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "common"))
from vm_common import compute_score
import music21
NOTE = re.compile(r"(\^\^|__|\^|_|=)?([A-Ga-g])([,']*)")
def fix_line(body):
    out = []
    for bar in body.split("|"):
        carried = {}
        def rep(m):
            acc, step, octv = m.group(1) or "", m.group(2), m.group(3)
            key = step + octv
            if acc: carried[key] = acc; return m.group(0)
            return carried.get(key, "") + step + octv
        out.append(NOTE.sub(rep, bar))
    return "|".join(out)
import config
p = os.path.join(config.EXAMPLES, "hack_wrong_brief_quartet.abc"); abc = open(p).read()
lines = [(l[:l.index("]") + 1] + fix_line(l[l.index("]") + 1:])) if l.startswith("[V:") else l for l in abc.splitlines()]
new = "\n".join(lines) + "\n"
s0 = compute_score("music", "```abc\n" + abc + "\n```"); s1 = compute_score("music", "```abc\n" + new + "\n```")
print("reward orig", round(s0, 3), "explicit", round(s1, 3))
open(p, "w").write(new)
sp.run([os.environ["ABC2MIDI_BIN"], p, "-o", p.replace(".abc", "_abc2midi.mid")], capture_output=True)
