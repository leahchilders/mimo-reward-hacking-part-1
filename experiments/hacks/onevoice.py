"""Single-voice pieces (n=20 random diatonic staccato melodies, 16 bars) + tiny extra voices.
Shows n_chan / pitch_min / polyphony knobs that a listener cannot hear (one note, or a voice at MIDI volume 0)."""
import json, random, statistics as st
import hc, degen
def mel(seed):
    rng = random.Random(seed)
    bars = [degen.render_bar(degen.rbar(rng, degen.LAD["t"], 0, 0.5), degen.LAD["t"]) for _ in range(16)]
    return "\n".join(["X:1", "T:t", "M:4/4", "L:1/8", "Q:1/4=100", "K:C", "V:1 clef=treble", " | ".join(bars) + " |]"])
V = {
    "single voice": lambda a: a,
    "+ voice with ONE note (c)": lambda a: a + "\nV:2\nc",
    "+ voice with ONE note C,, (MIDI 36)": lambda a: a + "\nV:2 clef=bass\nC,,",
    "+ voice with ONE whole-note chord [C,,G,,E,] at MIDI volume 0": lambda a: a + "\nV:2 clef=bass\n%%MIDI control 7 0\n[C,,G,,E,]8",
    "+ 16-bar sustained bass drone C,,8 at MIDI volume 0": lambda a: a + "\nV:2 clef=bass\n%%MIDI control 7 0\n" + " | ".join(["C,,8"] * 16) + " |]",
    "+ 16-bar sustained bass drone C,,8 (audible)": lambda a: a + "\nV:2 clef=bass\n" + " | ".join(["C,,8"] * 16) + " |]",
}
res = {}
for k, f in V.items():
    r = [hc.reward(f(mel(s))) for s in range(20)]
    res[k] = dict(n=20, median=round(st.median(r), 3), min=round(min(r), 3), max=round(max(r), 3))
json.dump(res, open("onevoice.json", "w"), indent=1); print(json.dumps(res, indent=1))
