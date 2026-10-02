import re, random, statistics as st
from vc import *
from gen import pool
def setM(abc, new):
    abc=re.sub(r"^M:.*$", "M:"+new, abc, flags=re.M)
    return re.sub(r"\[M:[^\]]*\]", "[M:"+new+"]", abc)
# synthetic: every bar overfull (5 quarters in 4/4), 3 voices
rng=random.Random(1)
def ob(pl): return " ".join(rng.choice(pl)+"2" for _ in range(5))
v=[" | ".join(ob(pl) for _ in range(16))+" |]" for pl in (pool(5,5),pool(4,4),pool(2,3))]
abc="X:1\nT:o\nM:4/4\nL:1/8\nQ:1/4=100\nK:C\n"+"".join(f"V:{i+1}\n{x}\n" for i,x in enumerate(v))
r=rec(abc); print("overfull 4/4: score",S(abc),"bar warnings",r["bar"],"err",r["err"],"ungated",r.get("total"))
r2=rec(setM(abc,"none")); print("overfull M:none: score",S(setM(abc,"none")),"bar",r2["bar"],"err",r2["err"])
# real pieces zeroed only by bar warnings
for pid,t,a,row in pieces(passing_only=False):
    g=row["gates_norm"]
    if g and all(x.startswith("bar_warnings") for x in g.split(";")):
        b=setM(a,"none"); rr=rec(b)
        print(f"{pid} {t[:40]:40s} gate={g:18s} ungated {row['quality_norm_ungated']}  M:none score {S(b):.3f} (bar {rr['bar']} err {rr['err']}) ungated {rr.get('total')}")
