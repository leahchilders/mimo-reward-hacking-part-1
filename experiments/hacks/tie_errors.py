"""Collect every abc2midi Error on the gated real pieces (abc_norm) and show the ABC at the
reported line-char position, to classify xml2abc-bad-ABC vs abc2midi-limitation."""
import csv, os, re, collections, json
import hc
rows = list(csv.DictReader(open(os.path.join(os.path.dirname(hc.HERE), "abc_route", "per_piece.csv"))))
cat = collections.Counter(); ex = collections.defaultdict(list); per = {}
for r in rows:
    if float(r["abc_norm"]) > 0: continue
    a = hc.load_norm(r["id"]); d = hc.diag(a)
    ls = a.split("\n")
    errs = [l for l in d["log"].splitlines() if l.startswith("Error")]
    per[r["id"]] = dict(err=d["err"], bar=d["bar"], kinds=collections.Counter(re.sub(r"Error in line-char \S+ : ", "", e)[:60] for e in errs))
    for e in errs:
        m = re.match(r"Error in line-char (\d+)-(\d+) : (.*)", e)
        if not m: cat[e[:60]] += 1; continue
        ln, ch, msg = int(m.group(1)), int(m.group(2)), m.group(3)
        cat[msg[:60]] += 1
        line = ls[ln - 1] if ln - 1 < len(ls) else ""
        ex[msg[:60]].append(f"{r['id']} L{ln}c{ch}: ...{line[max(0,ch-60):ch+15]}...")
out = ["Error kinds across gated real pieces (count of Error lines):"] + [f"  {v:4d}  {k}" for k, v in cat.most_common()]
out.append("\nPer piece:"); out += [f"  {k}: err={v['err']} bar={v['bar']} {dict(v['kinds'])}" for k, v in per.items()]
out.append("\nContexts (first 12 per kind):")
for k, v in ex.items():
    out.append(f"== {k}"); out += ["  " + x for x in v[:12]]
open("tie_errors.txt", "w").write("\n".join(out) + "\n"); print("\n".join(out))
