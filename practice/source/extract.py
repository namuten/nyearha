"""Score sources (MusicXML + MuseScore .spos/.mpos) -> note timelines. Pure functions."""
import json
import os
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MSCORE = os.environ.get("MSCORE", "/Applications/MuseScore 4.app/Contents/MacOS/mscore")

# (folder, prefix, title, [part ids]) -- pilot: Blue only; others are added later
PIECES = [
    ("Blue", "blue", "그대 안의 블루", ["clarinet"]),
]


def parse_notes(xml_text):
    """Return (onsets, beats). One onset per non-chord, non-grace <note>."""
    root = ET.fromstring(xml_text)
    beats = None
    onsets = []
    for measure in root.iter("measure"):
        num = int(measure.get("number"))
        if beats is None:
            b = measure.find("attributes/time/beats")
            if b is not None:
                beats = int(b.text)
        for note in measure.findall("note"):
            if note.find("chord") is not None or note.find("grace") is not None:
                continue
            rest = note.find("rest") is not None
            pitch = None
            if not rest:
                p = note.find("pitch")
                alter = int(float(p.findtext("alter", "0")))
                pitch = p.findtext("step") + ("#" if alter == 1 else "b" if alter == -1 else "") + p.findtext("octave")
            tie_stop = any(t.get("type") == "stop" for t in note.findall("tie"))
            onsets.append({"pitch": pitch, "rest": rest, "measure": num, "tie_stop": tie_stop})
    return onsets, beats


def _parse_events(text):
    return [int(p) for p in re.findall(r'<event elid="\d+" position="(\d+)"', text)]


def parse_spos(text):
    return _parse_events(text)


def parse_mpos(text):
    return _parse_events(text)


def build_notes(onsets, times, end_ms):
    if len(onsets) != len(times):
        raise ValueError(f"onset count {len(onsets)} != event count {len(times)}")
    notes = []
    for o, ms in zip(onsets, times):
        if o["tie_stop"] and notes:
            continue
        notes.append({"ms": ms, "end": end_ms, "pitch": o["pitch"], "rest": o["rest"], "measure": o["measure"]})
    for a, b in zip(notes, notes[1:]):
        a["end"] = b["ms"]
    return notes


def _pinky(keys):
    return {k for k in keys if k.startswith(("LP_", "RP_"))}


def _conflicts(prev, keys):
    """Same-side pinky keys that differ between consecutive notes (a slide)."""
    return any(a[:3] == b[:3] and a != b for a in _pinky(prev) for b in _pinky(keys))


def apply_fingering(notes, chart):
    """Annotate non-rest notes in place with `fingering` (key ids) and `alt: True` when an
    alternate was chosen; returns the same list. `chart` is the whole clarinet.json dict
    (uses chart["notes"]). If the previous played note (rests skipped) used a pinky key and the
    default fingering needs a different key on the same side, use the first conflict-free alt.
    Raises KeyError for a pitch missing from the chart."""
    table = chart["notes"]
    prev = None
    for n in notes:
        if n["rest"]:
            continue
        if n["pitch"] not in table:
            raise KeyError(f"pitch {n['pitch']} not in fingering chart")
        entry = table[n["pitch"]]
        keys = list(entry["keys"])
        if prev is not None and _conflicts(prev, keys):
            for a in entry.get("alt", []):
                if not _conflicts(prev, a):
                    keys = list(a)
                    n["alt"] = True
                    break
        n["fingering"] = keys
        prev = keys
    return notes


def _mscore(*args):
    subprocess.run([MSCORE, *map(str, args)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _mp3_ms(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                   "-of", "csv=p=0", str(path)])
    return round(float(out) * 1000)


def extract_part(folder, prefix, part, tmp):
    tmp = Path(tmp)
    subprocess.run(["python3", "-I", str(ROOT / folder / "source" / "gen.py"), str(tmp)],
                   check=True, stdout=subprocess.DEVNULL)
    xml_path = tmp / f"{prefix}_{part}.musicxml"
    _mscore("-o", tmp / "x.mscz", xml_path)
    _mscore("-o", tmp / "x.spos", tmp / "x.mscz")
    _mscore("-o", tmp / "x.mpos", tmp / "x.mscz")
    onsets, beats = parse_notes(xml_path.read_text(encoding="utf-8"))
    spos = parse_spos((tmp / "x.spos").read_text(encoding="utf-8"))
    mpos = parse_mpos((tmp / "x.mpos").read_text(encoding="utf-8"))
    man = {p["id"]: p for p in json.load(open(ROOT / folder / "manifest.json", encoding="utf-8"))}[part]
    if mpos != [m["ms"] for m in man["measures"]]:
        raise SystemExit(f"{prefix}_{part}: mpos measures differ from {folder}/manifest.json")
    mp3 = ROOT / folder / "assets" / f"{prefix}_{part}.mp3"
    chart = json.load(open(ROOT / "practice" / "instruments" / "clarinet.json", encoding="utf-8"))
    notes = apply_fingering(build_notes(onsets, spos, _mp3_ms(mp3)), chart)
    return {"piece": prefix, "part": part, "instrument": "clarinet", "partLabel": man["label"],
            "mp3": f"../{folder}/assets/{prefix}_{part}.mp3", "score": f"../{folder}/#{part}",
            "seconds": man["seconds"], "beats": beats, "measures": mpos, "notes": notes}


def _dump(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")


def main():
    out_dir = ROOT / "practice" / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    listing = []
    for folder, prefix, title, parts in PIECES:
        for part in parts:
            with tempfile.TemporaryDirectory() as tmp:
                d = extract_part(folder, prefix, part, tmp)
            d = {"piece": d["piece"], "part": d["part"], "instrument": d["instrument"], "title": title,
                 **{k: v for k, v in d.items() if k not in ("piece", "part", "instrument")}}
            _dump(out_dir / f"{prefix}_{part}.json", d)
            listing.append({"id": f"{prefix}_{part}", "title": title, "partLabel": d["partLabel"],
                            "seconds": d["seconds"]})
            print(f"{prefix}_{part}: {len(d['notes'])} notes, {len(d['measures'])} measures")
            for n in d["notes"]:
                if n.get("alt"):
                    print(f"{prefix}_{part} m{n['measure']} {n['pitch']} -> alt")
    _dump(ROOT / "practice" / "pieces.json", listing)


if __name__ == "__main__":
    main()
