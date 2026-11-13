import json
import unittest
from pathlib import Path

from extract import PIECES, apply_fingering, build_notes, parse_mpos, parse_notes, parse_spos

ROOT = Path(__file__).resolve().parents[2]

XML = """<?xml version="1.0" encoding="UTF-8"?>
<score-partwise version="3.1"><part-list><score-part id="P1"/></part-list>
<part id="P1">
<measure number="1"><attributes><divisions>2</divisions><time><beats>4</beats><beat-type>4</beat-type></time></attributes>
<note><pitch><step>G</step><octave>3</octave></pitch><duration>4</duration><type>half</type></note>
<note><rest/><duration>4</duration><type>half</type></note>
</measure>
<measure number="2">
<note><pitch><step>F</step><alter>1</alter><octave>3</octave></pitch><duration>4</duration><type>half</type><tie type="start"/></note>
<note><pitch><step>F</step><alter>1</alter><octave>3</octave></pitch><duration>2</duration><type>quarter</type><tie type="stop"/></note>
<note><pitch><step>B</step><alter>-1</alter><octave>3</octave></pitch><duration>2</duration><type>quarter</type></note>
<note><chord/><pitch><step>D</step><octave>4</octave></pitch><duration>2</duration></note>
<note><grace/><pitch><step>C</step><octave>4</octave></pitch></note>
</measure></part></score-partwise>
"""

SPOS = """<score><elements><element id="0" x="30258" y="25673" sx="1944.73" sy="3968.5" page="0">
      </element><element id="1" x="1" y="2" sx="3" sy="4" page="0">
      </element></elements><events>
<event elid="0" position="0"/><event elid="1" position="1000"/><event elid="2" position="2000"/>
<event elid="3" position="3000"/><event elid="4" position="3500"/></events></score>"""

CHART = {"notes": {
    "X": {"keys": ["L1", "LP_E"]},
    "Y": {"keys": ["L1", "LP_F"], "alt": [["L1", "RP_F"]]},
    "Z": {"keys": ["L1", "LP_F"]},
}}


def notes(*pitches):
    return [{"ms": i * 100, "end": i * 100 + 100, "pitch": p, "rest": p is None, "measure": 1}
            for i, p in enumerate(pitches)]


class ExtractTest(unittest.TestCase):
    def test_parse_notes(self):
        onsets, beats = parse_notes(XML)
        self.assertEqual(beats, 4)
        self.assertEqual([o["pitch"] for o in onsets], ["G3", None, "F#3", "F#3", "Bb3"])
        self.assertEqual([o["tie_stop"] for o in onsets], [False, False, False, True, False])
        self.assertEqual([o["measure"] for o in onsets], [1, 1, 2, 2, 2])
        self.assertEqual([o["rest"] for o in onsets], [False, True, False, False, False])

    def test_parse_spos(self):
        self.assertEqual(parse_spos(SPOS), [0, 1000, 2000, 3000, 3500])

    def test_parse_mpos(self):
        self.assertEqual(parse_mpos(SPOS), [0, 1000, 2000, 3000, 3500])

    def test_build_notes_merges_tie_and_sets_end(self):
        notes = build_notes(parse_notes(XML)[0], [0, 1000, 2000, 3000, 3500], 4000)
        self.assertEqual([(n["ms"], n["end"], n["pitch"], n["rest"]) for n in notes],
                         [(0, 1000, "G3", False), (1000, 2000, None, True),
                          (2000, 3500, "F#3", False), (3500, 4000, "Bb3", False)])
        self.assertEqual([n["measure"] for n in notes], [1, 1, 2, 2])

    def test_build_notes_count_mismatch_raises(self):
        with self.assertRaises(ValueError):
            build_notes(parse_notes(XML)[0], [0, 1000], 4000)

    def test_every_part_matches_manifest_measures(self):
        for folder, prefix, title, parts in PIECES:
            man = {p["id"]: p for p in json.load(open(ROOT / folder / "manifest.json", encoding="utf-8"))}
            for part in parts:
                d = json.load(open(ROOT / "practice" / "data" / f"{prefix}_{part}.json", encoding="utf-8"))
                self.assertEqual(d["measures"], [m["ms"] for m in man[part]["measures"]])
                self.assertEqual(d["seconds"], man[part]["seconds"])
                self.assertEqual(d["partLabel"], man[part]["label"])

    def test_notes_monotonic_and_inside_audio(self):
        for folder, prefix, title, parts in PIECES:
            for part in parts:
                d = json.load(open(ROOT / "practice" / "data" / f"{prefix}_{part}.json", encoding="utf-8"))
                notes = d["notes"]
                self.assertTrue(notes)
                for a, b in zip(notes, notes[1:]):
                    self.assertLess(a["ms"], b["ms"])
                for n in notes:
                    self.assertGreater(n["end"], n["ms"])
                self.assertLessEqual(notes[-1]["end"], d["seconds"] * 1000 + 1000)

    def test_pieces_json_lists_all_parts(self):
        got = json.load(open(ROOT / "practice" / "pieces.json", encoding="utf-8"))
        self.assertEqual([g["id"] for g in got],
                         [f"{prefix}_{part}" for _, prefix, _, parts in PIECES for part in parts])

    def _fingering(self):
        return json.load(open(ROOT / "practice" / "instruments" / "clarinet.json", encoding="utf-8"))

    def _used_pitches(self):
        used = set()
        for f in sorted((ROOT / "practice" / "data").glob("*.json")):
            d = json.load(open(f, encoding="utf-8"))
            used |= {n["pitch"] for n in d["notes"] if not n["rest"]}
        return used

    def test_fingering_covers_every_used_pitch(self):
        notes = self._fingering()["notes"]
        missing = sorted(self._used_pitches() - set(notes))
        self.assertEqual(missing, [], f"clarinet.json 에 없는 음: {missing}")

    def test_every_entry_verified_with_two_sources(self):
        fing = self._fingering()
        ids = {s["id"] for s in fing["sources"]}
        bad = sorted(p for p, e in fing["notes"].items()
                     if e.get("verified") is not True or len(set(e["src"]) & ids) < 2)
        self.assertEqual(bad, [], f"미확인 음: {bad}")

    def test_keys_exist_in_keylist_and_svg(self):
        fing = self._fingering()
        key_ids = [k["id"] for k in fing["keyList"]]
        self.assertEqual(len(key_ids), len(set(key_ids)))
        used = set()
        for e in fing["notes"].values():
            used |= set(e["keys"])
            for a in e.get("alt", []):
                used |= set(a)
        self.assertEqual(sorted(used - set(key_ids)), [])
        svg = (ROOT / "practice" / "instruments" / "clarinet.svg").read_text(encoding="utf-8")
        for k in key_ids:
            self.assertIn(f'id="{k}"', svg)
        self.assertIn("viewBox", svg)
        self.assertNotRegex(svg, r"<svg[^>]*\s(width|height)=")
        self.assertNotRegex(svg, r'class="key"[^>]*\sfill=')
        self.assertNotRegex(svg, r'\sfill="[^"]*"[^>]*class="key"')

    def test_switches_to_alt_on_same_pinky_conflict(self):
        out = apply_fingering(notes("X", "Y"), CHART)
        self.assertEqual(out[1]["fingering"], ["L1", "RP_F"])
        self.assertTrue(out[1]["alt"])

    def test_skips_rests_when_looking_back(self):
        out = apply_fingering(notes("X", None, "Y"), CHART)
        self.assertTrue(out[2]["alt"])
        self.assertNotIn("fingering", out[1])

    def test_keeps_default_without_usable_alt(self):
        out = apply_fingering(notes("X", "Z"), CHART)
        self.assertEqual(out[1]["fingering"], ["L1", "LP_F"])
        self.assertFalse(out[1].get("alt", False))

    def test_missing_pitch_raises(self):
        with self.assertRaises(KeyError):
            apply_fingering(notes("Q"), CHART)

    def test_generated_data_has_fingering_on_every_note(self):
        for f in sorted((ROOT / "practice" / "data").glob("*.json")):
            d = json.load(open(f, encoding="utf-8"))
            for n in d["notes"]:
                if not n["rest"]:
                    self.assertIsInstance(n.get("fingering"), list, f"{f.name} m{n['measure']} {n['pitch']}")


if __name__ == "__main__":
    unittest.main()
