#!/usr/bin/env python3
"""시네마 천국 (Cinema Paradiso) - Love Theme (Ennio & Andrea Morricone, 1988) -- B-flat 클라리넷 솔로 -> MusicXML.

원본 피아노 악보(source/시네마천국 - 러브테마 악보.pdf, 콘서트 B♭장조/G단조)의 원곡 주선율을
고등학생 연주자가 쉽게 연주할 수 있도록 클라리넷 브레이크(B4) 아래의 따뜻하고 편안한 음역(기보 E3–A4,
기보 다장조/가단조 조표 없음 · 콘서트 B♭장조/G단조 원키 그대로)으로 옮긴 멜로디 중심 편곡.

- 기보 조: 다장조/가단조(♯0/♭0, 콘서트 B♭장조/G단조), 4/4(브리지 2/4 원곡 박자 유지), ♩=66 (Andante cantabile), 21마디.
- 음역 및 난이도 설계 (고등학생 연주자용):
  - 기보 음역: E3–A4 (전 구간 클라리넷 레지스터 브레이크 B4 아래의 샬뤼모·쓰로트 음역 안에서만 연주)
  - 조표 없음(다장조/가단조), 임시표는 원곡 선율의 반음 보조음 G#3(6·15마디) 1개뿐
  - 불필요한 꾸밈음·도약 없이 원본 악보의 순수 주선율(1마디 도입 + A 전반부 반종지 + B 후반부 정격종지)만 그대로 수록.
"""
import sys

TEMPO = 66

# 각 마디: (박자 분자, 토큰 문자열) -- 분모는 항상 4 (4/4 = 16단위, 2/4 = 8단위)
MELODY = [
    # ── Intro (1): 원곡 1마디 도입 ──
    (4, "D4:12- r:4"),                                                     # 1  Intro

    # ── A (2–10): 전반부 주선율 (반종지 D7sus4 - D7) ──
    (4, "C4:6-( E3:2 F3:2 C4:2 B3:2 A3:2)"),                               # 2  Gm - Cm7
    (4, "B3:2( D4:2 G3:3 F3:1 F3:4 E3:4-)"),                               # 3  F - Bb
    (2, "r:2 E3:2( G3:2 B3:2"),                                            # 4  Bbmaj7 (2/4)
    (4, "D4:2 C4:2 B3:2 C4:2 E4:6-) E4:2("),                               # 5  Gm - Bb/F (4/4)
    (4, "A3:2 G#3:2 A3:2 G4:2 F4:8-)"),                                    # 6  Ebmaj7 - Cm7
    (4, "r:2 D4:2( A4:2 G4:2 G4:2 F4:2 E4:2 D4:2)"),                       # 7  Am7(b5) - D7(b9)
    (4, "C4:6-( C4:2 D4:2 C4:2 B3:2 G3:2)"),                               # 8  Gm - Gm7/F
    (4, "A3:12- B3:2( C4:2"),                                              # 9  Ebmaj7 - Edim
    (4, "B3:12-) r:4"),                                                    # 10 D7sus4 - D7

    # ── B (11–21): 후반부 주선율 (정격종지 Bb/F - F | Eb/Bb - Bb | Bbmaj7) ──
    (4, "C4:6-( E3:2 F3:2 C4:2 B3:2 A3:2)"),                               # 11 Gm - Cm7
    (4, "B3:2( D4:2 G3:3 F3:1 F3:4 E3:4-)"),                               # 12 F7 - Bb
    (2, "r:2 E3:2( G3:2 B3:2"),                                            # 13 Bbmaj7/A (2/4)
    (4, "D4:2 C4:2 B3:2 C4:2 E4:6-) E4:2("),                               # 14 Gm - Bb/F (4/4)
    (4, "A3:2 G#3:2 A3:2 G4:2 F4:8-)"),                                    # 15 Ebmaj7 - Cm7
    (4, "r:2 D4:2( A4:2 G4:2 G4:2 F4:2 E4:2 D4:2)"),                       # 16 Am7(b5) - D7(b9)
    (4, "C4:6-( C4:2 D4:2 C4:2 B3:2 G3:2)"),                               # 17 Gm - Gm7/F
    (4, "A3:12- B3:2( C4:2"),                                              # 18 Ebmaj7 - Edim (A/E)
    (4, "G4:12~ G4:2 F4:2)"),                                              # 19 Bb/F - F
    (4, "F4:8-( E4:8-)"),                                                  # 20 Eb/Bb - Bb (rit.)
    (4, "E4:16-"),                                                         # 21 Bbmaj7 (페르마타)
]


def parse_token(tok):
    p, rest = tok.split(":")
    digits = [ch for ch in rest if ch.isdigit()]
    flags = {ch for ch in rest if not ch.isdigit()}
    d = int("".join(digits))
    return p, d, ("~" in flags), ("(" in flags), (")" in flags), ("-" in flags)


def bars(lines):
    out = []
    for idx, (beats, s) in enumerate(lines, start=1):
        expected = beats * 4
        m = [parse_token(t) for t in s.split()]
        total = sum(item[1] for item in m)
        assert total == expected, f"Bar {idx}: expected {expected}, got {total} in {s!r}"
        out.append((beats, m))
    return out


MUSIC = bars(MELODY)
assert len(MUSIC) == 21
LAST = len(MUSIC)

DYN = {
    1: "mp",
    2: "mp",
    7: "mf",
    8: "mp",
    11: "mf",
    16: "f",
    19: "mf",
    20: "mp",
    21: "p",
}
REHEARSAL = {2: "A", 11: "B"}
WORDS = {
    2: "dolce e cantabile",
    11: "espressivo",
    16: "appassionato",
    20: "rit. e dim.",
}
RIT = {
    (20, 0): 62,
    (20, 8): 56,
    (21, 0): 50,
}
TYPES = {
    16: ("whole", 0),
    12: ("half", 1),
    8: ("half", 0),
    6: ("quarter", 1),
    4: ("quarter", 0),
    3: ("eighth", 1),
    2: ("eighth", 0),
    1: ("16th", 0),
}


def note_xml(p, d, bar_len=16, tie_start=False, tie_stop=False, slur_start=False, slur_stop=False,
             tenuto=False, fermata=False):
    t, dots = TYPES[d]
    if p == "r":
        whole = ' measure="yes"' if d == bar_len else ""
        return f"<note><rest{whole}/><duration>{d}</duration><voice>1</voice>" + \
               ("" if d == bar_len else f"<type>{t}</type>" + "<dot/>" * dots) + "</note>"
    step, octave = p[0], p[-1]
    alter = {"#": 1, "b": -1}.get(p[1], 0) if len(p) == 3 else 0
    x = f"<note><pitch><step>{step}</step>" + (f"<alter>{alter}</alter>" if alter else "") + \
        f"<octave>{octave}</octave></pitch><duration>{d}</duration>"
    x += '<tie type="stop"/>' * tie_stop + '<tie type="start"/>' * tie_start
    x += f"<voice>1</voice><type>{t}</type>" + "<dot/>" * dots

    nots = ""
    if tie_stop:
        nots += '<tied type="stop"/>'
    if tie_start:
        nots += '<tied type="start"/>'
    if slur_stop:
        nots += '<slur type="stop" number="1"/>'
    if slur_start:
        nots += '<slur type="start" number="1"/>'
    if tenuto:
        nots += "<articulations><tenuto/></articulations>"
    if fermata:
        nots += '<fermata type="upright"/>'
    if nots:
        x += f"<notations>{nots}</notations>"
    return x + "</note>"


def direction(inner, placement="above", sound=""):
    return f'<direction placement="{placement}"><direction-type>{inner}</direction-type>{sound}</direction>'


def part_xml():
    out = ['<part id="P1">']
    tie_open = False
    prev_beats = None
    for i, (beats, m) in enumerate(MUSIC, start=1):
        out.append(f'<measure number="{i}">')
        if i == 1:
            # 기보 다장조/가단조(fifths=0), B-flat 클라리넷 이조(콘서트 B♭장조/G단조)
            out.append(f"<attributes><divisions>4</divisions><key><fifths>0</fifths></key>"
                       f"<time><beats>{beats}</beats><beat-type>4</beat-type></time>"
                       f"<clef><sign>G</sign><line>2</line></clef>"
                       f"<transpose><diatonic>-1</diatonic><chromatic>-2</chromatic></transpose></attributes>")
            out.append(direction('<words font-weight="bold">Andante cantabile, dolce</words>'))
            out.append(direction(f'<metronome parentheses="no"><beat-unit>quarter</beat-unit>'
                                 f'<per-minute>{TEMPO}</per-minute></metronome>', sound=f'<sound tempo="{TEMPO}"/>'))
        elif beats != prev_beats:
            out.append(f"<attributes><time><beats>{beats}</beats><beat-type>4</beat-type></time></attributes>")
        prev_beats = beats

        if i in REHEARSAL:
            out.append(direction(f'<rehearsal enclosure="square">{REHEARSAL[i]}</rehearsal>'))
        if i in WORDS:
            out.append(direction(f'<words font-style="italic">{WORDS[i]}</words>'))
        if i in DYN:
            out.append(direction(f"<dynamics><{DYN[i]}/></dynamics>", "below"))
        pos = 0
        bar_len = beats * 4
        for j, (p, d, tie, sl_start, sl_stop, ten) in enumerate(m):
            if (i, pos) in RIT:
                out.append(f'<direction><direction-type><words print-object="no"> </words></direction-type>'
                           f'<offset>0</offset><sound tempo="{RIT[(i, pos)]}"/></direction>')
            last = i == LAST and j == len(m) - 1
            out.append(note_xml(
                p, d,
                bar_len=bar_len,
                tie_start=tie,
                tie_stop=tie_open,
                slur_start=sl_start,
                slur_stop=sl_stop,
                tenuto=ten,
                fermata=last,
            ))
            tie_open = tie
            pos += d
        if i in (4, 10, 13):
            out.append('<barline location="right"><bar-style>light-light</bar-style></barline>')
        if i == LAST:
            out.append('<barline location="right"><bar-style>light-heavy</bar-style></barline>')
        out.append("</measure>")
    out.append("</part>")
    return "\n".join(out)


TITLE, SUBTITLE, COMPOSER = "Cinema Paradiso", "Love Theme (시네마 천국)", "Ennio & Andrea Morricone"


def score_xml():
    return "\n".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" '
        '"http://www.musicxml.org/dtds/partwise.dtd">',
        '<score-partwise version="4.0">',
        f"<work><work-title>{TITLE}</work-title></work>",
        f"<movement-title>{TITLE}</movement-title>",
        f'<identification><creator type="composer">{COMPOSER}</creator>'
        f'<creator type="lyricist">{SUBTITLE}</creator></identification>',
        '<part-list><score-part id="P1"><part-name>Clarinet in B♭</part-name><part-abbreviation>Cl.</part-abbreviation>'
        '<score-instrument id="P1-I1"><instrument-name>Clarinet in B♭</instrument-name>'
        '<instrument-sound>wind.reed.clarinet.bflat</instrument-sound></score-instrument></score-part></part-list>',
        part_xml(),
        "</score-partwise>"])


if __name__ == "__main__":
    with open(f"{sys.argv[1]}/cinema_clarinet.musicxml", "w", encoding="utf-8") as f:
        f.write(score_xml())
    print("wrote cinema_clarinet")
