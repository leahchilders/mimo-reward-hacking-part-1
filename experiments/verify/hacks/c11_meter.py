import re, statistics as st
from vc import *
def setM(abc,new):
    abc=re.sub(r"^M:.*$","M:"+new,abc,flags=re.M); return re.sub(r"\[M:[^\]]*\]","[M:"+new+"]",abc)
def nba(a): return re.sub(r"^(X:.*)$","\\1\n%%MIDI nobeataccents",a,count=1,flags=re.M)
D=[];D2=[];gz=0;same_notes=0;n=0;rows=[]
for pid,t,abc,r in pieces():
    Ms=re.findall(r"^M:(.*)$|\[M:([^\]]*)\]",abc,flags=re.M); Ms={(a or b).strip() for a,b in Ms}
    if Ms<= {"4/4","C"}: continue
    n+=1; b=setM(abc,"4/4")
    r0,r1=rec(abc),rec(b); d=r1["total"]/100-r0["total"]/100; D.append(d)
    d2=rec(nba(b))["total"]/100-rec(nba(abc))["total"]/100; D2.append(d2)
    gz+= S(b)==0
    m0,m1=midi(abc)[0],midi(b)[0]
    same_notes+= [x[:4] for x in m0["notes"]]==[x[:4] for x in m1["notes"]]
    rows.append((pid,sorted(Ms),round(d,4),r1["bar"]))
print("non-4/4 passing pieces:",n)
print("ungated delta: max |d| %.4f; n with d==0: %d; with nobeataccents max |d| %.4f"%(max(abs(x) for x in D),sum(abs(x)<1e-9 for x in D),max(abs(x) for x in D2)))
print("identical (onset,dur,ch,pitch) notes:",same_notes,"/",n,"; zeroed by gate after relabel:",gz)
for r in rows: print(r)
