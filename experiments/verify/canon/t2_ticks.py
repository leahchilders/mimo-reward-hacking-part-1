import os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vc
# minimal hand-written ABC: two voices, sixteenths/eighths/quarters, a chord
abc = """X:1
T:tick probe
M:4/4
L:1/16
Q:1/4=100
K:C
V:1
cdef gabc' c'4 [ceg]4 | c2d2 e2f2 g8 |]
V:2
C,4 D,4 E,8 | C,16 |]
"""
log, data = vc.abc2midi_run(abc)
div, mn = vc.midi_notes(data)
print("div", div)
for n in mn: print(n)
# Goldberg XXIII
abc = open(os.path.join(vc.HERE, "work", "Goldberg_XXIII.abc")).read()
log, data = vc.abc2midi_run(abc)
div, mn = vc.midi_notes(data)
print("Goldberg div", div, "n", len(mn))
print("onset mod 30 hist", collections.Counter(o % 30 for o, d, c, p in mn).most_common(6))
print("dur hist", collections.Counter(d for o, d, c, p in mn).most_common(8))
step = div // 2
cover = sum(1 for o, d, c, p in mn if any(o <= t < o + d for t in range((o // step) * step, o + d + 1, step)))
print("notes containing an eighth-grid point:", cover, "/", len(mn))
