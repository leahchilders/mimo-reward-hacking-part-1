# Greedy own ablation: for each tie-error line, delete single ties (one at a time) and keep deletions that
# reduce the abc2midi tie-error count. Print each kept tie with context for manual classification.
import re, sys
from vc import *
P={p[0]:p for p in pieces(False)}
def mask(s):
    s=re.sub(r'"[^"]*"',lambda m:"#"*len(m.group(0)),s); s=re.sub(r"![^!]*!",lambda m:"#"*len(m.group(0)),s)
    return s.split("%")[0]+"#"*(len(s)-len(s.split("%")[0]))
def ties(line):
    ms=mask(line); return [m.start() for m in re.finditer(r"(?<=[\]A-Ga-gxz,'/0-9])-",ms)]
def nerr(abc):
    r=rec(abc); log=midi(abc)[1]
    return sum(1 for l in log.splitlines() if l.startswith("Error") and "tie" in l.lower()), r["err"]
for pid in sys.argv[1:]:
    abc=P[pid][2]; L=abc.split("\n"); base_tie,base_err=nerr(abc)
    print("=====",pid,P[pid][1],"tie-errors",base_tie,"all errors",base_err,"score",S(abc),"ungated",rec(abc).get("total"))
    log=midi(abc)[1]
    lines=sorted({int(m.group(1)) for m in re.finditer(r"Error in line-char (\d+)-\d+ : (?:Could not find note to be tied|Bad tie|Cannot find note before tie)",log)})
    cand=[]
    for ln in lines:
        for k in (ln-2, ln-1, ln):  # error line (1-based ln-1 index) and previous line
            if 0<=k<len(L) and not re.match(r"^[A-Za-z]:",L[k]): cand+= [(k,c) for c in ties(L[k])]
    cand=sorted(set(cand))
    cur=L[:]; kept=[]
    for k,c in cand:
        trial=cur[:]; trial[k]=trial[k][:c]+" "+trial[k][c+1:]
        t,_=nerr("\n".join(trial))
        if t<base_tie:
            kept.append((k,c,L[k][max(0,c-14):c+16])); cur=trial; base_tie=t
    new="\n".join(cur); t,e=nerr(new)
    print(f"  deleted {len(kept)} ties -> tie-errors {t}, all errors {e}, score {S(new):.3f}")
    for k,c,ctx in kept: print(f"    line {k+1} col {c}: ...{ctx}...")
