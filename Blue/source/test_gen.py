"""악보 규칙 테스트: python3 -m unittest discover -s Blue/source -v"""
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen  # noqa: E402

ALLOWED = {48, 36, 24, 21, 18, 12, 9, 6, 4, 3}
F_MAJOR_PCS = {5, 7, 9, 10, 0, 2, 4}
BB_MAJOR_PCS = {10, 0, 2, 3, 5, 7, 9}


def notes(music):
    for i, m in enumerate(music, start=1):
        pos = 0
        for p, d, tie in m:
            yield i, pos, p, d, tie
            pos += d


def sounding(m, pos):
    t = 0
    for p, d, _ in m:
        if t <= pos < t + d:
            return p
        t += d


class Score(unittest.TestCase):
    def setUp(self):
        self.fl = gen.melody_bars()
        self.cl = gen.clarinet()

    def test_shape(self):
        self.assertEqual(len(self.fl), 24)
        self.assertEqual(len(self.cl), 24)
        for m in self.fl + self.cl:
            self.assertEqual(sum(d for _, d, _ in m), gen.BAR)

    def test_rhythms(self):
        for music in (self.fl, self.cl):
            for i, pos, p, d, tie in notes(music):
                self.assertIn(d, ALLOWED, (i, p, d))
                if d == 4:  # 셋잇단음표는 한 박 안에서 세 개가 한 묶음
                    self.assertIn(pos % gen.Q, {0, 4, 8}, (i, pos))
        for i, pos, p, d, tie in notes(self.cl):
            self.assertFalse(tie, (i, p))
            self.assertIn(d, {48, 24, 12}, (i, p, d))   # 반주는 온·2분·4분음표만

    def test_ties_join_same_pitch(self):
        flat = [(i, p, tie) for i, pos, p, d, tie in notes(self.fl)]
        for (i, p, tie), (_, q, _) in zip(flat, flat[1:]):
            if tie:
                self.assertEqual(p, q, (i, p, q))

    def test_flute_melody_in_sheet_keys(self):
        for i, pos, p, d, tie in notes(self.fl):
            if p != "r":
                pcs = F_MAJOR_PCS if i < 10 else BB_MAJOR_PCS
                self.assertIn(gen.midi(p) % 12, pcs, (i, p))
                self.assertTrue(gen.midi("D4") <= gen.midi(p) <= gen.midi("Bb5"), (i, p))

    def test_clarinet_chord_tones(self):
        for i, m in enumerate(self.cl, start=1):
            pos = 0
            for p, d, _ in m:
                c = gen.CHART[i - 1][0 if pos < 2 * gen.Q else 1]
                self.assertIn(gen.midi(p) % 12, {gen.midi(n + "4") % 12 for n in gen.SPELL[c]}, (i, p, c))
                pos += d

    def test_clarinet_range_below_break(self):
        for i, pos, p, d, tie in notes(gen.written(self.cl)):
            self.assertTrue(gen.midi("E3") <= gen.midi(p) <= gen.midi("G4"), (i, p))

    def test_clarinet_below_melody(self):
        for i, m in enumerate(self.cl):
            pos = 0
            for p, d, _ in m:
                for t in range(pos, pos + d):
                    f = sounding(self.fl[i], t)
                    if f != "r":
                        self.assertLess(gen.midi(p), gen.midi(f), (i + 1, t, p, f))
                pos += d

    def test_musicxml_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable, "-I", os.path.join(HERE, "gen.py"), tmp], check=True,
                           capture_output=True)
            self.assertEqual(sorted(os.listdir(tmp)), ["blue_clarinet.musicxml", "blue_flute.musicxml",
                                                       "blue_full_score.musicxml"])

            def read(n):
                with open(os.path.join(tmp, f"blue_{n}.musicxml")) as f:
                    return f.read()
            full, fl, cl = read("full_score"), read("flute"), read("clarinet")
            self.assertIn('<part id="P2">', full)
            self.assertIn("<fifths>-1</fifths>", fl)
            self.assertIn("<fifths>-2</fifths>", fl)
            self.assertIn("<fifths>1</fifths>", cl)
            self.assertIn("<fifths>0</fifths>", cl)
            self.assertIn("<transpose><diatonic>-1</diatonic><chromatic>-2</chromatic>", cl)
            for x in (full, fl):
                self.assertIn("<per-minute>70</per-minute>", x)
                self.assertIn('<tuplet type="start"', x)
                self.assertIn("<type>16th</type>", x)
                self.assertIn("<fermata", x)


if __name__ == "__main__":
    unittest.main()
