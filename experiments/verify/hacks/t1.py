from vc import *
for body in ["C2 .D2 .E .F G4 |]", "C4- C4 | C2 z2 C4 |]", "[CEG]2 .[CEG]2 G/ A/ B c |]"]:
    m, log, f = midi(f"X:1\nM:4/4\nL:1/8\nQ:1/4=100\nK:C\n{body}\n")
    print(body, [(o,d,p) for o,d,c,p,v in m["notes"]])
m, log, f = midi("X:1\nM:4/4\nL:1/8\nQ:1/4=100\nK:C\nV:1\nc2 d2 e2 f2|]\nV:2\nC2 D2 E2 F2|]\n")
print([(o,d,c,p) for o,d,c,p,v in m["notes"]])
