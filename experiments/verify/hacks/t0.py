from vc import *
import statistics as st
ps = pieces()
sc = [S(a) for _,_,a,_ in ps]
print(len(ps), st.median(sc), max(sc), sum(1 for s in sc if s>0))
m, log, f = midi("X:1\nM:4/4\nL:1/8\nQ:1/4=100\nK:C\nC2 D E F G4 |]\n")
print(m["div"], m["notes"])
