import re
from vc import *
from gen import pool
from gen2 import piece
T=pool(4,5)+["c'","d'"]; B=pool(2,3)+["C","D"]; M=["G,","A,","B,"]+pool(4,4)+["c","d","e","f"]
base=piece(0,[T,B,M],[0,.3,.5])
simple="X:1\nT:s\nM:4/4\nL:1/8\nQ:1/4=100\nK:C\n"+" | ".join(["CDEF GABc","c2B2 A2G2","FEDC E2G2","c4 G4"]*4)+" |]\n"
def app(abc, bars):  # add 2 bars to voice 1 and rests to other voices
    lines=abc.rstrip("\n").split("\n"); out=[]; first=True
    for ln in lines:
        if ln.endswith("|]") and not ln.startswith(("V:","X:")):
            ext=bars if first else "z8 | z8"
            ln=ln[:-2]+"| "+ext+" |]"; first=False
        out.append(ln)
    return "\n".join(out)+"\n"
cases={
 "control: c4 {d}c4 | c8":"c4 {d}c4 | c8",
 "control: c4- c4 | c8":"c4- c4 | c8",
 "tie+grace c4- {d}c4":"c4- {d}c4 | c8",
 "tie+grace c4-{d}c4":"c4-{d}c4 | c8",
 "stacc tied .c4-c4":".c4-c4 | c8",
 "control: .c4 c4":".c4 c4 | c8",
 "dotted tie c4.-c4":"c4.-c4 | c8",
 "dotted tie no length c.-c (spec example form)":"c.-c c6 | c8",
 "non-pow2 c8/3 (x3 = 8)":"c8/3 c8/3 c8/3 | c8",
 "non-pow2 c4/3":"c4/3 c4/3 c4/3 c4 | c8",
 "control: c8/4 (pow2)":"c8/4 c8/4 c8/4 c8/4 c4 | c8",
}
for nm,b in cases.items():
    row=[]
    for lab,a in (("synth3v",base),("simple1v",simple)):
        x=app(a,b); r=rec(x)
        errs=[l for l in midi(x)[1].splitlines() if l.startswith("Error")][:1]
        row.append(f"{lab}: {S(x):.3f} (err {r['err']}, bar {r['bar']}) {errs[0][-45:] if errs else ''}")
    print(f"{nm:44s} | "+" | ".join(row))
print("base scores", S(base), S(simple))
