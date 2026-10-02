import re, sys
from vc import *
P={p[0]:p for p in pieces(False)}
for pid in sys.argv[1:]:
    abc=P[pid][2]; L=abc.split("\n"); m,log,f=midi(abc)
    errs=[l for l in log.splitlines() if l.startswith("Error")]
    print("=====",pid,P[pid][1],len(errs),"errors")
    for e in errs[:4]:
        mm=re.search(r"line-char (\d+)-(\d+)",e); ln,ch=int(mm.group(1)),int(mm.group(2))
        print(e); s=L[ln-1]; print("   ...",s[max(0,ch-70):ch+30].replace("\n"," ")); print("   ",(" "*min(70,ch))+"^")
