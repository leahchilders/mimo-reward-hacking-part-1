"""Score every row of canon_list.csv in parallel (one score_one.py subprocess per piece, per-piece timeout).
Appends to results.jsonl (resumable: already-scored cids are skipped). Saves normalized ABC to abc/<cid>.abc.
Usage: run_all.py [workers] [timeout_s]"""
import os, sys, json, time, subprocess as sp, csv
from concurrent.futures import ThreadPoolExecutor, as_completed

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "common"))
import config  # sets ABC2MIDI_BIN, aliases the upstream scorer as `music_scorer`
PY = sys.executable
WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 14
TIMEOUT = int(sys.argv[2]) if len(sys.argv) > 2 else 900
os.makedirs(D + "/abc", exist_ok=True)
rows = list(csv.DictReader(open(D + "/canon_list.csv")))
done = set()
if os.path.exists(D + "/results.jsonl"):
    done = {json.loads(l)["cid"] for l in open(D + "/results.jsonl")}
todo = [r for r in rows if r["cid"] not in done]
print(f"{len(todo)} to do ({len(done)} done), workers={WORKERS}", flush=True)


def run(r):
    t0 = time.time()
    try:
        p = sp.run([PY, D + "/score_one.py", config.canon_path(r), "--save-abc", f"{D}/abc/{r['cid']}.abc"],
                   capture_output=True, timeout=TIMEOUT)
        out = p.stdout.decode().strip().splitlines()
        res = json.loads(out[-1]) if out else dict(status="no_output", stderr=p.stderr.decode()[-300:])
    except sp.TimeoutExpired:
        res = dict(status="timeout")
    except Exception as e:
        res = dict(status="runner_exception", error=repr(e)[:200])
    res["cid"] = r["cid"]; res["wall"] = round(time.time() - t0, 2)
    return res


t0 = time.time()
with open(D + "/results.jsonl", "a") as fh, ThreadPoolExecutor(WORKERS) as ex:
    futs = [ex.submit(run, r) for r in todo]
    for i, f in enumerate(as_completed(futs), 1):
        res = f.result(); fh.write(json.dumps(res) + "\n"); fh.flush()
        if i % 50 == 0 or i == len(todo):
            el = time.time() - t0
            print(f"{i}/{len(todo)}  {el:.0f}s  {i / el:.2f} pieces/s", flush=True)
print("wall", round(time.time() - t0, 1))
