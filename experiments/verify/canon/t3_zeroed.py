import os, sys, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vc
T = {
 "ClairDeLune_C0304": "10/27/QmSJeDjtEuw3PjP17fheDNXGojcQ76HmntyE2T84D5zJYY.mxl",
 "ClairDeLune_C0476": "2/43/QmcS9UechTguCFmdiscHgNk2DwrEBy5hxeR5wP5uoTW95e.mxl",
 "ClairDeLune_C0477": "1/20/QmbFXZxcZDZuVZBMDqRqGwFAf6S5U4ko4Ziky1d5UpWy21.mxl",
 "Op110_C0268": "12/19/QmUf78TMviix8Ru54MRptCuSmteJpmWaaTjT3Fm337Aegr.mxl",
 "Moonlight_C0713": "12/36/QmUpwoWPt5QUso95Nt8icKKmm1VQjYUJdbP1QxWQCSX4mL.mxl",
 "Moonlight_C0022": "9/20/QmRF7ckbdQocrFDobpTZmbR9uoTS3TGfApKtREwoEmXTj3.mxl",
 "Moonlight_C1211": "10/55/QmSY3ReAsvR3M3B7a3raYBw9DM2Y2tXmAVg3NRQ6yyUuxW.mxl",
 "Moonlight_C0719": "10/41/QmSR9dSVAWuyQSJMMEG66At1yXw4jKyfjTB7mp4Ek6gX5w.mxl",
 "K310i_C0094": "16/28/QmYkwGqdPV2gFv7GS3Lv59K6pvwbH7tzEbp2uPFvzBzFzz.mxl",
}
for name, rel in T.items():
    abc = vc.norm(vc.xml2abc(os.path.join(vc.PDMX, rel))[0])
    open(os.path.join(vc.HERE, "work", name + ".abc"), "w").write(abc)
    reward, r = vc.score_abc(abc)
    log, _ = vc.abc2midi_run(abc)
    errs = [l for l in log.splitlines() if l.startswith("Error")]
    kinds = {}
    for e in errs:
        k = re.sub(r"line-char \S+ : ", "", e)
        k = re.sub(r"\d+", "N", k)
        kinds[k] = kinds.get(k, 0) + 1
    print(name, "reward", reward, "total", r.get("total"), "err", r.get("err"), "bar", r.get("bar"), kinds)
    for e in errs[:3]:
        m = re.search(r"line-char (\d+)-(\d+)", e)
        ln, ch = int(m.group(1)), int(m.group(2))
        line = abc.split("\n")[ln - 1]
        print("   ", e, "|| ...", line[max(0, ch - 60):ch + 25])
