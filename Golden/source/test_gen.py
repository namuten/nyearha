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
F_MAJOR_PCS = {5, 7, 9, 10, 0, 2, 4}          # 콘서트 F장조 (F G A Bb C D E)
G_MAJOR_PCS = {7, 9, 11, 0, 2, 4, 6}          # 클라리넷 기보 G장조 (G A B C D E F#)


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
        self.fl = gen.flute()
        self.cl_concert = gen.clarinet()
        self.cl_written = gen.written(self.cl_concert)

    def test_shape(self):
        self.assertEqual(len(self.fl), 44)
        self.assertEqual(len(self.cl_concert), 44)
        self.assertEqual(len(self.cl_written), 44)
        for m in self.fl + self.cl_concert + self.cl_written:
            self.assertEqual(sum(d for _, d, _ in m), gen.BAR)

    def test_rhythms(self):
        for music in (self.fl, self.cl_written):
            for i, pos, p, d, tie in notes(music):
                self.assertIn(d, ALLOWED, (i, p, d))
                if d == 4:  # 셋잇단음표는 한 박 안에서 세 개가 한 묶음
                    self.assertIn(pos % gen.Q, {0, 4, 8}, (i, pos))

    def test_call_and_response_coverage(self):
        # 모든 마디에서 최소 한 악기는 주선율을 연주하고, 두 악기가 고르게 주선율을 나눠 가짐
        self.assertEqual(gen.FLUTE_LEAD_BARS | gen.CLARINET_LEAD_BARS, set(range(1, 45)))
        self.assertGreaterEqual(len(gen.FLUTE_LEAD_BARS), 20)
        self.assertGreaterEqual(len(gen.CLARINET_LEAD_BARS), 20)
        for i in range(1, 45):
            if i in gen.FLUTE_LEAD_BARS and i != 38:
                self.assertEqual(self.fl[i - 1], gen.MEL_FL[i - 1], i)
            if i in gen.CLARINET_LEAD_BARS:
                self.assertEqual(self.cl_concert[i - 1], gen.MEL_CL[i - 1], i)

    def test_flute_range(self):
        for i, pos, p, d, tie in notes(self.fl):
            if p != "r":
                self.assertTrue(gen.midi("D4") <= gen.midi(p) <= gen.midi("G5"), (i, p))

    def test_keys(self):
        for music in (self.fl, self.cl_concert):
            for i, pos, p, d, tie in notes(music):
                if p != "r":
                    self.assertIn(gen.midi(p) % 12, F_MAJOR_PCS, (i, p))
        for i, pos, p, d, tie in notes(self.cl_written):
            if p != "r":
                self.assertIn(gen.midi(p) % 12, G_MAJOR_PCS, (i, p))
                self.assertNotIn("b", p[1:], (i, p))

    def test_clarinet_range_below_break(self):
        for i, pos, p, d, tie in notes(self.cl_written):
            if p != "r":
                self.assertTrue(gen.midi("E3") <= gen.midi(p) <= gen.midi("A4"), (i, p))

    def test_clarinet_below_flute_in_concert_pitch(self):
        for i, m in enumerate(self.cl_concert):
            pos = 0
            for p, d, _ in m:
                if p != "r":
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
            self.assertIn("<fifths>-1</fifths>", fl)
            self.assertIn("<fifths>1</fifths>", cl)
            self.assertIn("<transpose><diatonic>-1</diatonic><chromatic>-2</chromatic>", cl)
            for x in (full, fl, cl):
                self.assertIn("<per-minute>120</per-minute>", x)
                self.assertIn('<tuplet type="start"', x)
                self.assertIn("<fermata", x)


if __name__ == "__main__":
    unittest.main()
