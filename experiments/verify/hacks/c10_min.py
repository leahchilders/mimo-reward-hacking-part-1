from vc import *
H="X:1\nM:4/4\nL:1/8\nQ:1/4=100\nK:C\n"
cases={"_E- E3 (accidental carries in bar)":"E3_E- E3 z | c8 |]",
 "_E- _E3 explicit":"E3_E- _E3 z | c8 |]",
 "_E- E3 then [DG]- x8 (as in Paragon V:3)":"E3_E- E3[DG]- | x8 | c8 |]",
 "[DG]- x8 alone":"E3E E3[DG]- | x8 | c8 |]",
 "[DG]- [DG]":"E3E E3[DG]- | [DG]8 | c8 |]",
 "chord tie into chord inside slur ([DFcd]-) [DFcd]4-":"([DFcd]F=A[DFcd]-) [DFcd]4- | [DFcd]8 |]",
 "[bd']- [bd']e[gb]2":"z2 [ae'][bd']- [bd']e[gb]2 | c8 |]",
 "partial chord tie [Bg]- B2":"[Bg]- B2 B2 z2 | c8 |]",
 "tie to rest B- z":"A^A2B- z4 | c8 |]",
}
for k,b in cases.items():
    r=rec(H+b+"\n"); log=midi(H+b+"\n")[1]
    print(f"{k:55s} err {r['err']}  {[l[-50:] for l in log.splitlines() if l.startswith('Error')][:2]}")
