"""Scan raw MusicXML (lxml) for tie starts whose matching stop is not the next
note of the same pitch in the same <voice>/<staff> -> dangling / cross-voice ties."""
import os, sys, zipfile, collections
import xml.etree.ElementTree as etree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vc

def load(p):
    z = zipfile.ZipFile(p)
    name = [n for n in z.namelist() if n.endswith(".xml") and not n.startswith("META")][0]
    return etree.fromstring(z.read(name))

def scan(rel):
    root = load(os.path.join(vc.PDMX, rel))
    out = collections.Counter(); ex = []
    for part in root.iter("part"):
        open_ties = {}  # (staff, voice, pitch) -> measure
        for m in part.iter("measure"):
            for n in m.iter("note"):
                if n.find("pitch") is None or n.find("grace") is not None:
                    continue
                pe = n.find("pitch")
                pitch = (pe.findtext("step"), pe.findtext("alter") or "0", pe.findtext("octave"))
                staff, voice = n.findtext("staff") or "1", n.findtext("voice") or "1"
                types = [t.get("type") for t in n.findall("tie")]
                if "stop" in types:
                    k = (staff, voice, pitch)
                    if k in open_ties:
                        open_ties.pop(k)
                    else:
                        other = [kk for kk in open_ties if kk[2] == pitch]
                        if other:
                            out["stop matches start in other voice/staff"] += 1
                            ex.append((m.get("number"), "cross", other[0][:2], (staff, voice), pitch))
                            open_ties.pop(other[0])
                        else:
                            out["stop without start"] += 1
                            ex.append((m.get("number"), "orphan-stop", (staff, voice), pitch))
                if "start" in types:
                    open_ties[(staff, voice, pitch)] = m.get("number")
        for k, mn in open_ties.items():
            out["start never stopped"] += 1
            ex.append((mn, "dangling-start", k))
    return out, ex

for nm, rel in [("Clair C0477", "1/20/QmbFXZxcZDZuVZBMDqRqGwFAf6S5U4ko4Ziky1d5UpWy21.mxl"),
                ("Clair C0304", "10/27/QmSJeDjtEuw3PjP17fheDNXGojcQ76HmntyE2T84D5zJYY.mxl"),
                ("K310 C0094", "16/28/QmYkwGqdPV2gFv7GS3Lv59K6pvwbH7tzEbp2uPFvzBzFzz.mxl"),
                ("Op110 C0268", "12/19/QmUf78TMviix8Ru54MRptCuSmteJpmWaaTjT3Fm337Aegr.mxl")]:
    c, ex = scan(rel)
    print(nm, dict(c)); print("   ", ex[:8])
