"""Check the Sibelius-bound MusicXML carries the same notes (onset, pitch) as the abc2midi MIDI the scorer judged.
abc2midi output can carry a constant lead-in/scale, so onsets are aligned by the first-note offset and a fitted scale."""
import os
import music21
from collections import Counter
EX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "examples")  # *_abc2midi.mid come from make_examples.py
def ev(s):
    return sorted((float(n.getOffsetInHierarchy(s)), p.midi) for n in s.recurse().notes for p in n.pitches)
for name in ["hack_hillclimb_staccato", "hack_hillclimb", "hack_hillclimb_16bar", "hack_wrong_brief_quartet", "twinkle_with_bass", "twinkle_melody_only"]:
    x = ev(music21.converter.parse(os.path.join(EX, f"{name}.musicxml")))
    m = ev(music21.converter.parse(os.path.join(EX, f"{name}_abc2midi.mid"), quantizePost=False))
    x0, m0 = x[0][0], m[0][0]
    scale = (x[-1][0] - x0) / (m[-1][0] - m0) if m[-1][0] != m0 else 1
    xs = Counter((round(o - x0, 2), p) for o, p in x)
    ms = Counter((round((o - m0) * scale, 2), p) for o, p in m)
    same_pitch = Counter(p for _, p in x) == Counter(p for _, p in m)
    print(f"{name:26s} n={len(x)}/{len(m)} pitch-multiset-equal={same_pitch} scale={scale:.3f} lead={m0:.2f} mismatched={sum((xs-ms).values())}")
