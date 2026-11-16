"""쉬운 악보 규칙 테스트: python3 -m unittest discover -s YouRaiseMeUp/source -v"""
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen  # noqa: E402

ALLOWED = {16, 12, 8, 6, 4, 2}
F_MAJOR_PCS = {5, 7, 9, 10, 0, 2, 4}          # 콘서트 F장조 (F G A Bb C D E)
G_MAJOR_PCS = {7, 9, 11, 0, 2, 4, 6}          # 클라리넷 기보 G장조 (G A B C D E F#)


def notes(music):
    for i, m in enumerate(music, start=1):
        pos = 0
        for j, (p, d, tie) in enumerate(m):
            yield i, j, pos, p, d, tie, m
            pos += d


def sounding(m, pos):
    t = 0
    for p, d, _ in m:
        if t <= pos < t + d:
            return p
        t += d


class Beginner(unittest.TestCase):
    def setUp(self):
        self.fl = gen.flute()
        self.cl = gen.clarinet()
        self.cl_written = gen.written(self.cl)

    def test_shape(self):
        self.assertEqual(len(self.fl), 17)
        self.assertEqual(len(self.cl), 17)
        for m in self.fl + self.cl:
            self.assertEqual(sum(d for _, d, _ in m), 16)

    def test_rhythms(self):
        # 붙임줄 없음; 점4분음표는 박 위에서 시작해 8분음표가 뒤따름;
        # 박 중간에서 시작하는 음은 앞 8분음표(또는 점4분음표) 뒤의 8분음표뿐 -- 박을 가로지르는 당김음 없음
        for music in (self.fl, self.cl):
            for i, j, pos, p, d, tie, m in notes(music):
                self.assertIn(d, ALLOWED, (i, p, d))
                self.assertFalse(tie, (i, p))
                if d == 6:
                    self.assertEqual(pos % 4, 0, (i, pos))
                    self.assertEqual(m[j + 1][1], 2, (i, pos))
                if pos % 4 != 0:
                    self.assertEqual(d, 2, ("off-beat start", i, pos, p, d))
                    self.assertIn(m[j - 1][1], {2, 6}, (i, pos))

    def test_call_and_response_coverage(self):
        # 첫 반마디(도입 코드 패드)를 제외한 모든 반마디(1..31)에서 최소 한 악기는 주선율을 연주하며,
        # 두 악기가 2마디 악구(픽업 포함 4반마디)씩 번갈아 주고받고 마지막 악구(29..31 + 17마디)에서 함께 연주함
        self.assertEqual(gen.FLUTE_LEAD_HALVES | gen.CLARINET_LEAD_HALVES, set(range(1, 32)))
        self.assertGreaterEqual(len(gen.FLUTE_LEAD_HALVES), 14)
        self.assertGreaterEqual(len(gen.CLARINET_LEAD_HALVES), 14)
        self.assertEqual(self.fl[16], [("F5", 16, False)])
        self.assertEqual(self.cl[16], [("F4", 16, False)])

    def test_flute_range(self):
        for i, j, pos, p, d, tie, m in notes(self.fl):
            if p != "r":
                self.assertTrue(gen.midi("E4") <= gen.midi(p) <= gen.midi("G5"), (i, p))

    def test_keys(self):
        for music in (self.fl, self.cl):
            for i, j, pos, p, d, tie, m in notes(music):
                if p != "r":
                    self.assertIn(gen.midi(p) % 12, F_MAJOR_PCS, (i, p))
        for i, j, pos, p, d, tie, m in notes(self.cl_written):
            if p != "r":
                self.assertIn(gen.midi(p) % 12, G_MAJOR_PCS, (i, p))
                self.assertNotIn("b", p[1:], (i, p))

    def test_clarinet_range(self):
        for i, j, pos, p, d, tie, m in notes(self.cl_written):
            if p != "r":
                self.assertTrue(gen.midi("E3") <= gen.midi(p) <= gen.midi("A4"), (i, p))

    def test_clarinet_below_flute_in_concert_pitch(self):
        for i, m in enumerate(self.cl):
            pos = 0
            for p, d, _ in m:
                for t in range(pos, pos + d):
                    f = sounding(self.fl[i], t)
                    if p != "r" and f != "r":
                        self.assertLess(gen.midi(p), gen.midi(f), (i + 1, t, p, f))
                pos += d

    def test_musicxml_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable, "-I", os.path.join(HERE, "gen.py"), tmp], check=True,
                           capture_output=True)
            names = sorted(os.listdir(tmp))
            self.assertEqual(names, ["youraisemeup_clarinet.musicxml", "youraisemeup_flute.musicxml",
                                     "youraisemeup_full_score.musicxml"])
            def read(n):
                with open(os.path.join(tmp, f"youraisemeup_{n}.musicxml")) as f:
                    return f.read()
            full, fl, cl = read("full_score"), read("flute"), read("clarinet")
            self.assertIn('<part id="P2">', full)
            self.assertIn("<fifths>-1</fifths>", fl)
            self.assertIn("<fifths>1</fifths>", cl)
            self.assertIn("<transpose><diatonic>-1</diatonic><chromatic>-2</chromatic>", cl)
            for x in (full, fl, cl):
                self.assertIn("<per-minute>66</per-minute>", x)
                self.assertIn("<fermata", x)
                self.assertIn("<beats>4</beats>", x)


if __name__ == "__main__":
    unittest.main()
