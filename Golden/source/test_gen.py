"""악보 규칙 테스트: python3 -m unittest discover -s Golden/source -v"""
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen  # noqa: E402

ALLOWED = {48, 36, 24, 18, 12, 6, 4}          # 16분음표 없음
C_MAJOR_PCS = {0, 2, 4, 5, 7, 9, 11}
D_MAJOR_PCS = {2, 4, 6, 7, 9, 11, 1}


def notes(music):
    for i, m in enumerate(music, start=1):
        pos = 0
        for j, (p, d, tie) in enumerate(m):
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
        self.assertEqual(len(self.fl), 44)
        self.assertEqual(len(self.cl), 44)
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

    def test_chorus_repeats(self):
        self.assertEqual(self.fl[4:19], self.fl[20:35])

    def test_flute_range(self):
        for i, pos, p, d, tie in notes(self.fl):
            if p != "r":
                self.assertTrue(gen.midi("G4") <= gen.midi(p) <= gen.midi("D6"), (i, p))

    def test_keys(self):
        for music in (self.fl, self.cl):
            for i, pos, p, d, tie in notes(music):
                if p != "r":
                    self.assertIn(gen.midi(p) % 12, C_MAJOR_PCS, (i, p))
        for i, pos, p, d, tie in notes(gen.written(self.cl)):
            self.assertIn(gen.midi(p) % 12, D_MAJOR_PCS, (i, p))
            self.assertNotIn("b", p[1:], (i, p))

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
            self.assertEqual(sorted(os.listdir(tmp)), ["golden_clarinet.musicxml", "golden_flute.musicxml",
                                                       "golden_full_score.musicxml"])
            def read(n):
                with open(os.path.join(tmp, f"golden_{n}.musicxml")) as f:
                    return f.read()
            full, fl, cl = read("full_score"), read("flute"), read("clarinet")
            self.assertIn('<part id="P2">', full)
            self.assertIn("<fifths>0</fifths>", fl)
            self.assertIn("<fifths>2</fifths>", cl)
            self.assertIn("<transpose><diatonic>-1</diatonic><chromatic>-2</chromatic>", cl)
            for x in (full, fl):
                self.assertIn("<per-minute>120</per-minute>", x)
                self.assertIn('<tuplet type="start"', x)
                self.assertIn("<fermata", x)


if __name__ == "__main__":
    unittest.main()
