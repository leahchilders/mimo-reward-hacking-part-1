from vc import *
for extra in ["", "%%MIDI chordattack 0\n", "%%MIDI randomchordattack 0\n"]:
    m,log,f=midi(f"X:1\nM:4/4\nL:1/8\nK:C\n{extra}[CEG]2 [CEG]4 C2|]\n")
    print(repr(extra), m["tempo"], [(o,d,p) for o,d,c,p,v in m["notes"]])
