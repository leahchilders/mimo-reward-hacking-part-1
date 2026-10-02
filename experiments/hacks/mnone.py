"""Bar-warning gate bypass: declare free meter (M:none, ABC 2.1 sec 3.1.6) and abc2midi stops checking bar lengths.
Tested on (a) the real pieces zeroed only by bar warnings and (b) a hack piece with every bar deliberately wrong."""
import re, json, csv, os
import hc
def mnone(a):
    return re.sub(r"\[M:[^\]]*\]", "", re.sub(r"^M:\s*\S+", "M:none", a, flags=re.M))
out = {}
for r in csv.DictReader(open(os.path.join(os.path.dirname(hc.HERE), "abc_route", "per_piece.csv"))):
    if float(r["abc_norm"]) == 0 and int(r["err_norm"]) == 0:
        a = hc.load_norm(r["id"]); d0 = hc.diag(a); d1 = hc.diag(mnone(a))
        out[r["id"]] = dict(title=r["title"][:40], bar_before=d0["bar"], reward_before=d0["reward"], bar_after=d1["bar"], reward_after=d1["reward"], ungated_total_before=d0["total"])
h = open("pieces/climb_s2_st1_b16.abc").read()
broken = re.sub(r"\| ", "| c ", h)                     # one extra eighth in every bar of every voice
out["hack_every_bar_overfull"] = dict(bar_before=hc.diag(broken)["bar"], reward_before=hc.reward(broken), reward_after_Mnone=hc.reward(mnone(broken)), bar_after=hc.diag(mnone(broken))["bar"])
json.dump(out, open("mnone.json", "w"), indent=1); print(json.dumps(out, indent=1))
