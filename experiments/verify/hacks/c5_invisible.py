# Claim 5: fraction of notes that never touch a half-beat sampling tick, real pieces.
from vc import *
import statistics as st
fr=[]; fr_fix=[]
for pid,t,abc,r in pieces():
    m,log,f = midi(abc)
    div=m["div"]; step=max(1,int(div*0.5))
    pit=[n for n in m["notes"] if n[2]!=9]
    def vis(o,d):
        k=-(-o//step)*step  # first grid tick >= o
        return k < o+max(d,1)
    inv=sum(1 for o,d,c,p,v in pit if not vis(o,d))/len(pit)
    # counterfactual: onset 1 tick earlier (nominal), same end
    inv2=sum(1 for o,d,c,p,v in pit if not vis(o-1,d+1))/len(pit)
    fr.append(inv); fr_fix.append(inv2)
print("n",len(fr),"median invisible %.3f min %.3f max %.3f"%(st.median(fr),min(fr),max(fr)))
print("if onsets were nominal: median %.3f min %.3f max %.3f"%(st.median(fr_fix),min(fr_fix),max(fr_fix)))
