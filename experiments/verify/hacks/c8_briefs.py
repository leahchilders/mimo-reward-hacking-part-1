import pyarrow.parquet as pq, json, random
from vc import compute_score, config
from gen import pool
from gen2 import piece
t=pq.read_table(config.MIMO_BRIEFS).to_pylist()
print(len(t), list(t[0].keys()))
T=pool(4,5)+["c'","d'"]; B=pool(2,3)+["C","D"]; M=["G,","A,","B,"]+pool(4,4)+["c","d","e","f"]
abcs=[piece(s,[T,B,M],[0,.3,.5]) for s in (0,1)]
rng=random.Random(0); idx=rng.sample(range(len(t)),25)
for a in abcs:
    sol="```abc\n"+a+"\n```"
    vals=set()
    for i in idx:
        r=t[i]
        gt=r.get("reward_model",{}).get("ground_truth") if isinstance(r.get("reward_model"),dict) else None
        vals.add(compute_score(r.get("data_source","music"), sol, gt, r.get("extra_info")))
        vals.add(compute_score("music", sol, json.dumps(r.get("prompt"),default=str), {"prompt":r.get("prompt")}))
    vals.add(compute_score("music", sol)); vals.add(compute_score("anything", sol, "write a sad waltz in 3/4, F# minor, 1 voice", None))
    print("distinct scores over 25 briefs x2 + none + bogus:", vals)
print(json.dumps(t[idx[0]],default=str)[:600])
