"""Build the Part-1 example set: re-score each ABC through the real grade path
(compute_score), render the abc2midi MIDI the scorer actually judges, and write
MusicXML (via music21's ABC reader) to open in Sibelius."""
import os, sys, json, shutil, subprocess as sp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common"))
import config
import vm_common  # sets ABC2MIDI_BIN, imports the upstream scorer
from vm_common import compute_score, do
import music21

OUT = config.EXAMPLES
H = "X:1\nT:t\nM:4/4\nL:1/8\nK:C\n"
twinkle = H + "C2C2G2G2|A2A2G4|F2F2E2E2|D2D2C4|G2G2F2F2|E2E2D4|G2G2F2F2|E2E2D4|C2C2G2G2|A2A2G4|F2F2E2E2|D2D2C4|]"
twinkle_bass = (H + "V:1\n" + twinkle.split("K:C\n")[1] + "\nV:2 clef=bass\n"
                + "|".join(["C,8","F,8","C,8","G,,4C,4","C,8","G,,8","C,8","G,,8","C,8","F,8","C,8","G,,4C,4"]) + "|]")
cases = {
    # The hack pieces live in examples/ (the quartet after explicit_accidentals.py). The 16-bar piece is
    # already in contiguous V: blocks with no accidentals, so it needs neither post-processing script.
    "hack_hillclimb_staccato": open(os.path.join(OUT, "hack_hillclimb_staccato.abc")).read(),
    "hack_hillclimb": open(os.path.join(OUT, "hack_hillclimb.abc")).read(),
    "hack_hillclimb_16bar": open(os.path.join(OUT, "hack_hillclimb_16bar.abc")).read(),
    "hack_wrong_brief_quartet": open(os.path.join(OUT, "hack_wrong_brief_quartet.abc")).read(),
    "twinkle_melody_only": twinkle,
    "twinkle_with_bass": twinkle_bass,
    "twinkle_blank_line": twinkle.replace("K:C\n", "K:C\n\n"),
}
results = {}
for name, abc in cases.items():
    s = compute_score("music", "```abc\n" + abc + "\n```")
    r = do({"key": "k", "id": 0, "rep": 0, "abc": abc})
    results[name] = {"reward": round(s, 3), "reject": r.get("reject"), "groups": r.get("groups")}
    open(os.path.join(OUT, name + ".abc"), "w").write(abc)
    sp.run([os.environ["ABC2MIDI_BIN"], os.path.join(OUT, name + ".abc"), "-o",
            os.path.join(OUT, name + "_abc2midi.mid")], capture_output=True)
    try:
        sc = music21.converter.parse(abc, format="abc")
        sc.write("musicxml", fp=os.path.join(OUT, name + ".musicxml"))
    except Exception as e:
        results[name]["musicxml_error"] = repr(e)
    print(name, results[name])
json.dump(results, open(os.path.join(OUT, "scores.json"), "w"), indent=1, default=str)
