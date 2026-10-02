import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vc

T = {
    "Goldberg XXIII": "7/11/QmPb7NggGCNXqTZ6GdqkyerQc2YfkeFUrx6ujuqMiW5XTr.mxl",
    "WTC I Prelude XI BWV856": "0/39/QmaQ8oBUiWC9mFSESpizYeNyYJyKHbgbhx6U6HA98N1EYc.mxl",
    "WTC I Fugue X BWV855": "0/36/Qmapor59boKR6tHniSdsQsmN7HkrRebp396Y6MNKwUjJ5T.mxl",
    "Fur Elise C0501": "7/38/QmPqGTx8iM8rNKu75hjZoyvpyNHxL18XwVnsqqLTrpaJAw.mxl",
    "Chopin Op10/1": "5/12/QmfBcXne3RYUgUuZPhqQqE4giJfdumupz4r86NE8ZEgdBz.mxl",
    "Debussy Le vent": "0/15/Qmadte65iwPsoF6r2FA6xhZJxCKv6gRaJii7FeXFHEM65H.mxl",
    "Satie Berceuse": "1/49/QmbVkdMiKVAo54sndFEXNvZ2HApnq4YSRXFkjTiGxHJMjq.mxl",
    # alternates for context
    "Fur Elise C0018": "4/26/QmejNxQRaxmuxkt6khpdU54TKFybehBpATV42wHUNVpfs4.mxl",
}
out = os.path.join(vc.HERE, "work")
os.makedirs(out, exist_ok=True)
res = {}
for name, rel in T.items():
    path = os.path.join(vc.PDMX, rel)
    abc, err = vc.xml2abc(path)
    abc = vc.norm(abc)
    open(os.path.join(out, name.replace(" ", "_").replace("/", "-") + ".abc"), "w").write(abc)
    reward, r = vc.score_abc(abc)
    log, data = vc.abc2midi_run(abc)
    div, mn = vc.midi_notes(data)
    nb, ev, _ = vc.m21_notes(path)
    fid = vc.fidelity(ev, div, mn)
    voices = sorted(set(l.split()[0] for l in abc.split("\n") if l.startswith("V:")))
    row = dict(reward=round(reward, 4), total=r.get("total"), err=r.get("err"), bar=r.get("bar"),
               blank=r.get("blank"), ch_conflict=r.get("ch_conflict"), m21_measures=nb,
               voices=voices, **fid, pit_min=r.get("pit_min"))
    res[name] = row
    print(name, json.dumps(row), flush=True)
json.dump(res, open(os.path.join(out, "t1.json"), "w"), indent=1)
