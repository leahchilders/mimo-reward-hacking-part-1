"""Does the hill-climber's tripled-unison 'chords' ([eee], [EEE], [dee]) matter to the score?"""
import os, sys, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "common"))
from vm_common import compute_score, do
import config
abc = open(os.path.join(config.EXAMPLES, "hack_hillclimb_staccato.abc")).read()
def dedup(m):
    notes = re.findall(r"[A-Ga-g][,']*", m.group(1))
    uniq = list(dict.fromkeys(notes))
    return uniq[0] if len(uniq) == 1 else "[" + "".join(uniq) + "]"
fixed = re.sub(r"\[((?:[A-Ga-g][,']*){2,})\]", dedup, abc)
for name, a in [("original", abc), ("unisons collapsed", fixed)]:
    r = do({"key": "k", "id": 0, "rep": 0, "abc": a})
    print(name, round(compute_score("music", "```abc\n" + a + "\n```"), 3), r.get("groups"))
