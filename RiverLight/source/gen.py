#!/usr/bin/env python3
"""강빛초중 이음학교 교가 (River Light) -- 플루트 2 + B-flat 클라리넷 + 트롬본 -> MusicXML.

작곡 홍경서 · 작사 임채현/안정민. 학교에서 받은 악보(G장조, 4/4, ♩=128, 33마디)를 옮겨 적은 것.
편곡 구성 (53마디, 약 1분 40초):
  1-4    도입     원곡 29-32마디 (끝 프레이즈)              mf
  5-20   A 1절    원곡 1-16   플루트 1 선율(8va), 플루트 2 3도 아래 화음   mp
  21-36  B 2절    원곡 1-16   클라리넷 선율, 플루트 둘은 긴 음 화음         p
  37-53  C 후렴   원곡 17-33  플루트 1 + 클라리넷 옥타브 선율, 플루트 2 화음  f, 마지막 2마디 rit.
반주(플루트 2 화음, 클라리넷 안쪽 음, 트롬본 베이스)는 아래 박별 코드표에서 자동 생성.

음높이는 모두 콘서트음 (MIDI 번호로 계산). 클라리넷은 기보할 때 장2도 위(A장조)로 적는다.
SONG 의 길이 단위는 8분음표(4/4 한 마디 = 8). 뒤에 "~" 가 붙으면 다음 음과 붙임줄.
"""
import sys
from xml.sax.saxutils import escape

BAR = 16          # 내부 단위: 16분음표 (divisions=4)
TEMPO = 128

# ---------------------------------------------------------------- 원곡 선율 (콘서트, 8분음표 단위)
SONG = [
    "r:1 G4:1 F#4:1 D4:1 G4:2 F#4:1 D4:1~",   # 1  세상을 환히 비
    "D4:1 D4:1~ D4:2 D4:2 C4:1 B3:1~",        # 2  추고 있는
    "B3:4 B3:1 C4:1 D4:1 D4:1~",              # 3  밝은빛처
    "D4:1 C4:1~ C4:6",                        # 4  럼
    "r:1 G4:1 F#4:1 D4:1 G4:2 F#4:1 D4:1~",   # 5  너와나 모두함
    "D4:1 A4:1~ A4:2 A4:1 G4:1 F#4:1 G4:1~",  # 6  께 즐거운
    "G4:4 G4:1 F#4:1 G4:1 G4:1~",             # 7  학교되네
    "G4:6 G4:1 A4:1",                         # 8  우리
    "B4:2 r:2 E4:2 B4:1 A4:1~",               # 9  는 다함께
    "A4:2 r:2 D4:1 D4:1 A4:1 G4:1~",          # 10 한발한발
    "G4:4 G4:1 F#4:1 D4:1 D4:1~",             # 11 성장하는
    "D4:1 C4:2 B3:1~ B3:1 C4:3",              # 12 공동체
    "B4:2 r:2 E4:1 E4:1 B4:1 A4:1~",          # 13 자랑스러운
    "A4:2 r:2 D5:1 C5:1 B4:1 G4:1~",          # 14 강빛인이
    "G4:1 G4:2 A4:1~ A4:1 B4:2 C5:1~",        # 15 되어 가자
    "C5:6 r:2",                               # 16
    "r:2 C5:1 C5:1 C5:1 B4:2 C5:1~",          # 17 서로배려 하
    "C5:1 B4:1 B4:1 A4:1 A4:2 F#4:1 G4:1~",   # 18 고이해해 주는
    "G4:4 G4:1 G4:1 D5:1 D5:1~",              # 19 우리의모
    "D5:1 C5:1~ C5:6",                        # 20 습
    "r:2 C5:1 C5:1 C5:1 B4:2 C5:1~",          # 21 서로존중 하
    "C5:1 B4:1 B4:1 A4:1 A4:2 B4:1 G4:1~",    # 22 고모두소 중한
    "G4:4 G4:1 A4:1 B4:1 C5:1~",              # 23 우리학교
    "C5:6 r:2",                               # 24
    "r:1 D4:1 G4:2 B4:2 B4:1 A4:1",           # 25 언제나 함께
    "r:1 D4:1 F#4:2 A4:2 A4:1 G4:1~",         # 26 최선을 다해
    "G4:2 r:2 G4:1 F#4:1 D4:1 D4:1~",         # 27 다함께도
    "D4:1 C4:2 C4:1 G4:2 A4:2",               # 28 와가면서
    "r:2 B4:2 B4:2 B4:1 A4:1",                # 29 늘언제나
    "r:1 D4:1 F#4:2 A4:2 A4:1 G4:1~",         # 30 빛나는 우리
    "G4:2 r:2 G4:1 F#4:1 D4:1 D4:1~",         # 31 강빛초중
    "D4:3 C4:1 G4:2 A4:2",                    # 32 이음학
    "G4:6 r:2",                               # 33 교
]

# 박마다 코드 하나 (원곡 악보의 코드 기호)
CHORDS = """
G G G G | D D D D | Em Em Em Em | C C C C | G G G G | D D D D | Em Em Em Em | C C C C |
Em Em Em Em | D D D D | C C C C | C C D D | Em Em Em Em | D D D D | C C C C | C C C C |
G G G G | D D D D | Em Em Em Em | C C C C | G G G G | D D D D | Em Em Em Em | C C D D |
G G G G | D D D D | Em Em Em Em | C C C D | G G G G | D D D D | Em Em Em Em | C C D D | G G G G
"""
CHART = [b.split() for b in CHORDS.split("|")]
assert len(CHART) == len(SONG) == 33 and all(len(b) == 4 for b in CHART)

TONES = {"G": (7, 11, 2), "D": (2, 6, 9), "Em": (4, 7, 11), "C": (0, 4, 7)}   # 근음·3음·5음 (pitch class)
ROOT = {"G": 43, "D": 50, "Em": 52, "C": 48}     # 트롬본 근음 G2 D3 E3 C3
FIFTH = {"G": 50, "D": 45, "Em": 47, "C": 43}    # 트롬본 5음 D3 A2 B2 G2
SCALE = (0, 2, 4, 6, 7, 9, 11)                   # G장조
SEMI = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def midi(p):
    step, rest = p[0], p[1:]
    alt = 0
    while rest and rest[0] in "#b":
        alt += 1 if rest[0] == "#" else -1
        rest = rest[1:]
    return 12 * (int(rest) + 1) + SEMI[step] + alt


def parse(s):
    m = []
    for t in s.split():
        p, d = t.split(":")
        tie = d.endswith("~")
        m.append((None if p == "r" else midi(p), int(d.rstrip("~")) * 2, tie))
    assert sum(d for _, d, _ in m) == BAR, (s, sum(d for _, d, _ in m))
    return m


MEL = [parse(s) for s in SONG]

# ---------------------------------------------------------------- 편곡 구성
FORM = [("intro", range(29, 33)), ("v1", range(1, 17)), ("v2", range(1, 17)), ("chorus", range(17, 34))]
BARS = [(sec, n) for sec, rng in FORM for n in rng]          # (구역, 원곡 마디 번호)
assert len(BARS) == 53
REHEARSAL = {5: "A", 21: "B", 37: "C"}
WORDS = {36: "cresc.", 52: "rit."}
RIT = {(52, 0): 120, (52, 4): 112, (52, 8): 104, (52, 12): 96, (53, 0): 88}
LAST = len(BARS)


def chord_at(n, pos):
    return CHART[n - 1][pos // 4]


def groups(n):
    """같은 코드가 이어지는 박을 묶는다 -> [(코드, 길이16)]"""
    out = []
    for c in CHART[n - 1]:
        if out and out[-1][0] == c:
            out[-1][1] += 4
        else:
            out.append([c, 4])
    return [tuple(g) for g in out]


def up(bar, k):
    return [(None if p is None else p + 12 * k, d, t) for p, d, t in bar]


def step_down(p, steps):
    """G장조 음계에서 steps 칸 아래"""
    deg = [i for i, s in enumerate(SCALE) if s == p % 12]
    if not deg:
        return p - 3
    i, octv = deg[0], p // 12
    for _ in range(steps):
        i -= 1
        if i < 0:
            i, octv = 6, octv - 1
    return octv * 12 + SCALE[i]


_prev_h = 74   # 직전 화음 음 (D5)


def harmony(mel_bar, n, low=60):
    """선율 아래 3도/6도 화음 (선율과 같은 리듬)."""
    global _prev_h
    out, pos = [], 0
    for p, d, t in mel_bar:
        if p is None:
            out.append((None, d, False))
        else:
            tones = TONES[chord_at(n, pos)]
            h = None
            if p % 12 in tones:
                # 3도·6도 후보 중 직전 화음 음과 가까운 것 (매끄럽게), 없으면 4도·5도
                for ivs in ((3, 4, 5, 8, 9), (7,)):
                    cands = [p - iv for iv in ivs if (p - iv) % 12 in tones and p - iv >= low]
                    if cands:
                        h = min(cands, key=lambda m: (abs(m - _prev_h), -m))
                        break
            if h is None:
                h = step_down(p, 2)
            out.append((h, d, t))
            _prev_h = h
        pos += d
    # 붙임줄은 같은 음일 때만
    fixed = []
    for i, (h, d, t) in enumerate(out):
        nxt = out[i + 1][0] if i + 1 < len(out) else None
        fixed.append((h, d, t and (nxt is None or nxt == h)))
    return fixed


def pad(n, lo, hi, prev, below=None, avoid_root=False):
    """코드마다 긴 음 하나: lo..hi 안의 코드 구성음 중 직전 음과 가장 가까운 것."""
    out, pos = [], 0
    for c, d in groups(n):
        tones = TONES[c]
        cands = [m for m in range(lo, hi + 1) if m % 12 in tones]
        if avoid_root and len(cands) > 1:
            cands = [m for m in cands if m % 12 != tones[0]] or cands
        if below is not None:
            b = [x for x in below if x[0] <= pos < x[0] + x[1]]
            if b:
                top = b[0][2]
                cands = [m for m in cands if 3 <= top - m <= 9] or cands
        prev = min(cands, key=lambda m: (abs(m - prev), m))
        out.append((prev, d, False))
        pos += d
    return out, prev


def timeline(bar):
    t, out = 0, []
    for p, d, _ in bar:
        out.append((t, d, p))
        t += d
    return out


def bass(n, busy):
    out = []
    if not busy:                     # 2분음표: 근음 - 5음
        for c, d in groups(n):
            if d == 16:
                out += [(ROOT[c], 8, False), (FIFTH[c], 8, False)]
            else:
                out.append((ROOT[c], d, False))
        return out
    prev = None                      # 4분음표: 1·3박 근음, 2·4박 5음 (코드 바뀌면 근음)
    for beat, c in enumerate(CHART[n - 1]):
        p = ROOT[c] if (beat % 2 == 0 or c != prev) else FIFTH[c]
        out.append((p, 4, False))
        prev = c
    return out


def arrange():
    fl1, fl2, cl, tbn = [], [], [], []
    p_cl, p_f1, p_f2 = 55, 79, 72
    for sec, n in BARS:
        mel = MEL[n - 1]
        if sec in ("intro", "v1", "chorus"):
            top = up(mel, 1)
            fl1.append(top)
            fl2.append(harmony(top, n))
        else:  # v2: 플루트 둘은 긴 음 화음
            b1, p_f1 = pad(n, 76, 84, p_f1)
            b2, p_f2 = pad(n, 71, 79, p_f2, below=timeline(b1))
            fl1.append(b1)
            fl2.append(b2)
        if sec in ("intro", "v1"):
            b, p_cl = pad(n, 55, 64, p_cl, avoid_root=True)
            cl.append(b)
        else:
            cl.append(mel)
        tbn.append(bass(n, busy=sec in ("v2", "chorus")))
    # 마지막 마디: 온음표 G장조 화음 + 늘임표
    fl1[-1] = [(79, 16, False)]
    fl2[-1] = [(71, 16, False)]
    cl[-1] = [(67, 16, False)]
    tbn[-1] = [(43, 16, False)]
    return fl1, fl2, cl, tbn


def fix_ties(music):
    """붙임줄은 바로 다음 음이 같은 높이일 때만 남긴다 (마디 경계 포함)."""
    flat = [(i, j) for i, bar in enumerate(music) for j in range(len(bar))]
    out = [list(bar) for bar in music]
    for k, (i, j) in enumerate(flat):
        p, d, t = out[i][j]
        if t:
            nxt = out[flat[k + 1][0]][flat[k + 1][1]][0] if k + 1 < len(flat) else None
            out[i][j] = (p, d, p is not None and nxt == p)
    return out


FL1, FL2, CL, TBN = (fix_ties(x) for x in arrange())

# ---------------------------------------------------------------- 기보
NAMES_G = {0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F", 6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B"}


def spell(m):
    if m is None:
        return None
    name = NAMES_G[m % 12]
    return name[0], (1 if "#" in name else 0), m // 12 - 1


def to_written(music, semis):
    return [[(None if p is None else p + semis, d, t) for p, d, t in bar] for bar in music]


PARTS = {
    "flute_1": dict(name="Flute 1", abbr="Fl. 1", music=FL1, fifths=1, clef=("G", 2),
                    sound="wind.flutes.flute", dyn={1: "mf", 5: "mp", 21: "p", 37: "f"}),
    "flute_2": dict(name="Flute 2", abbr="Fl. 2", music=FL2, fifths=1, clef=("G", 2),
                    sound="wind.flutes.flute", dyn={1: "mf", 5: "p", 21: "p", 37: "mf"}),
    "clarinet": dict(name="Clarinet in B♭", abbr="Cl.", music=to_written(CL, 2), fifths=3, clef=("G", 2),
                     transpose=(-1, -2), sound="wind.reed.clarinet.bflat",
                     dyn={1: "mp", 5: "p", 21: "mf", 37: "f"}),
    "trombone": dict(name="Trombone", abbr="Tbn.", music=TBN, fifths=1, clef=("F", 4),
                     sound="brass.trombone", dyn={1: "mp", 5: "p", 21: "mp", 37: "f"}),
}
ORDER = ["flute_1", "flute_2", "clarinet", "trombone"]

SPELL_A = {0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F", 6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B"}
TYPES = {16: ("whole", 0), 12: ("half", 1), 8: ("half", 0), 6: ("quarter", 1), 4: ("quarter", 0),
         3: ("eighth", 1), 2: ("eighth", 0), 1: ("16th", 0)}


def note_xml(p, d, tie_start=False, tie_stop=False, fermata=False):
    t, dots = TYPES[d]
    if p is None:
        whole = ' measure="yes"' if d == BAR else ""
        return f"<note><rest{whole}/><duration>{d}</duration><voice>1</voice>" + \
               ("" if d == BAR else f"<type>{t}</type>") + "</note>"
    step, alter, octave = spell(p)
    x = f"<note><pitch><step>{step}</step>" + (f"<alter>{alter}</alter>" if alter else "") + \
        f"<octave>{octave}</octave></pitch><duration>{d}</duration>"
    x += '<tie type="stop"/>' * tie_stop + '<tie type="start"/>' * tie_start
    x += f"<voice>1</voice><type>{t}</type>" + "<dot/>" * dots
    nots = '<tied type="stop"/>' * tie_stop + '<tied type="start"/>' * tie_start
    if fermata:
        nots += '<fermata type="upright"/>'
    if nots:
        x += f"<notations>{nots}</notations>"
    return x + "</note>"


def direction(inner, placement="above", sound=""):
    return f'<direction placement="{placement}"><direction-type>{inner}</direction-type>{sound}</direction>'


def part_xml(pid, key, top):
    P = PARTS[key]
    out = [f'<part id="{pid}">']
    tie_open = False
    for i, m in enumerate(P["music"], start=1):
        assert sum(d for _, d, _ in m) == BAR, (key, i)
        out.append(f'<measure number="{i}">')
        if i == 1:
            a = "<attributes><divisions>4</divisions>"
            a += f"<key><fifths>{P['fifths']}</fifths></key><time><beats>4</beats><beat-type>4</beat-type></time>"
            a += f"<clef><sign>{P['clef'][0]}</sign><line>{P['clef'][1]}</line></clef>"
            if "transpose" in P:
                dia, chro = P["transpose"]
                a += f"<transpose><diatonic>{dia}</diatonic><chromatic>{chro}</chromatic></transpose>"
            out.append(a + "</attributes>")
            if top:
                out.append(direction('<words font-weight="bold">Allegretto</words>'))
                out.append(direction(f'<metronome parentheses="no"><beat-unit>quarter</beat-unit>'
                                     f'<per-minute>{TEMPO}</per-minute></metronome>',
                                     sound=f'<sound tempo="{TEMPO}"/>'))
        if top and i in REHEARSAL:
            out.append(direction(f'<rehearsal enclosure="square">{REHEARSAL[i]}</rehearsal>'))
        if top and i in WORDS:
            out.append(direction(f"<words>{WORDS[i]}</words>"))
        if i in P["dyn"]:
            out.append(direction(f'<dynamics><{P["dyn"][i]}/></dynamics>', "below"))
        pos = 0
        for j, (p, d, tie) in enumerate(m):
            if top and (i, pos) in RIT:
                out.append(f'<direction><direction-type><words print-object="no"> </words></direction-type>'
                           f'<offset>0</offset><sound tempo="{RIT[(i, pos)]}"/></direction>')
            last = i == LAST and j == len(m) - 1
            out.append(note_xml(p, d, tie_start=tie, tie_stop=tie_open, fermata=last))
            tie_open = tie
            pos += d
        if i in (4, 20, 36):
            out.append('<barline location="right"><bar-style>light-light</bar-style></barline>')
        if i == LAST:
            out.append('<barline location="right"><bar-style>light-heavy</bar-style></barline>')
        out.append("</measure>")
    out.append("</part>")
    return "\n".join(out)


TITLE, COMPOSER, SUBTITLE = "River Light", "작곡 홍경서", "강빛초중 이음학교 교가"


def score_xml(keys):
    head = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" '
            '"http://www.musicxml.org/dtds/partwise.dtd">',
            '<score-partwise version="4.0">',
            f"<work><work-title>{TITLE}</work-title></work>",
            f"<movement-title>{TITLE}</movement-title>",
            f'<identification><creator type="composer">{COMPOSER}</creator>'
            f'<creator type="lyricist">{SUBTITLE}</creator></identification>',
            "<part-list>"]
    for n, k in enumerate(keys, 1):
        P = PARTS[k]
        head.append(f'<score-part id="P{n}"><part-name>{escape(P["name"])}</part-name>'
                    f'<part-abbreviation>{escape(P["abbr"])}</part-abbreviation>'
                    f'<score-instrument id="P{n}-I1"><instrument-name>{escape(P["name"])}</instrument-name>'
                    f'<instrument-sound>{P["sound"]}</instrument-sound></score-instrument></score-part>')
    head.append("</part-list>")
    body = [part_xml(f"P{n}", k, top=(n == 1)) for n, k in enumerate(keys, 1)]
    return "\n".join(head + body + ["</score-partwise>"])


if __name__ == "__main__":
    outdir = sys.argv[1]
    jobs = {"riverlight_full_score": ORDER}
    for k in ORDER:
        jobs[f"riverlight_{k}"] = [k]
    for name, keys in jobs.items():
        with open(f"{outdir}/{name}.musicxml", "w") as f:
            f.write(score_xml(keys))
        print("wrote", name)
