#!/usr/bin/env python3
"""흔들리는 꽃들 속에서 네 샴푸향이 느껴진거야 (장범준, 2019) -- B-flat 클라리넷 솔로 -> MusicXML.

사용자가 준 클라리넷 멜로디 악보(기보 D♭장조, ♩=100)를 옮겨 적고, 1분 길이 솔로로 다듬었다.
- 기보 조를 반음 내려 C장조로 (조표 없음, 기보 A3–E5). 원래 악보는 D♭장조(♭5).
- 구성 (24마디, 약 1분): 원본 5–27마디 + 마지막 늘임표 마디.
    1–8   1절 앞부분 (원본 5–12, 8마디는 쉼표 대신 짧은 연결구)        mp
    A 9–16  1절 뒷부분 (원본 13–20, 13 cresc. → 15 mf)
    B 17–24 후렴 (원본 21–27) f → 23 rit., 24 늘임표
음높이는 클라리넷 기보음. 길이 단위는 16분음표 (4/4 한 마디 = 16). 뒤에 "~" 가 붙으면 다음 음과 붙임줄.
"""
import sys

BAR = 16
TEMPO = 100

V1 = "r:2 E4:1 E4:1 E4:2 E4:2 E4:2 D4:2 D4:2 E4:1 E4:1~"          # 원본 5, 13
V3 = "G4:2 A4:2 A4:2 A4:2 A4:2 G4:2 E4:2 F4:1 E4:1"               # 원본 7, 15
V4 = "r:12 r:2 E4:1 E4:1"                                           # 원본 8, 16
C1 = "E5:4 E5:3 D5:1 D5:2 E5:2 D5:2 C5:2"                          # 원본 21, 25
C2 = "A4:2 A4:4 E5:1 E5:1 D5:2 E5:2 D5:2 C5:2"                     # 원본 22, 26

MELODY = [
    V1,                                                             # 1  (원본 5)
    "E4:6 r:2 r:6 G4:2",                                            # 2  (6)
    V3,                                                             # 3  (7)
    V4,                                                             # 4  (8)
    "F4:2 F4:2 F4:1 A4:1 G4:1 G4:1~ G4:6 F4:2",                     # 5  (9)
    "E4:2 F4:2 E4:2 D4:1 D4:1~ D4:1 C4:3~ C4:2 C4:1 C4:1",          # 6  (10)
    "r:2 C4:1 C4:1 C4:2 A3:2 A3:2 C4:2 C4:2 D4:1 D4:1",             # 7  (11)
    "r:4 G4:2 F4:2 E4:2 D4:2 C4:4",                                 # 8  (12: 원본은 온쉼표, 연결구로 채움)
    V1,                                                             # 9  (13)
    "E4:6 r:2 r:6 G4:1 G4:1",                                       # 10 (14)
    V3,                                                             # 11 (15)
    V4,                                                             # 12 (16)
    "F4:2 F4:2 F4:1 A4:1 G4:1 G4:1~ G4:6 G4:1 G4:1",                # 13 (17)
    "E4:2 E4:2 G4:2 B4:1 B4:1 A4:6 A4:1 B4:1",                      # 14 (18)
    "C5:2 C5:2 C5:2 A4:2 A4:2 C5:2 C5:2 D5:1 D5:1",                 # 15 (19)
    "r:8 r:2 G4:1 G4:1 G4:1 A4:1 C5:2",                             # 16 (20)
    C1,                                                             # 17 (21)
    C2,                                                             # 18 (22)
    "A4:2 A4:4 E5:1 E5:1 E5:2 D5:2 C5:2 D5:2",                      # 19 (23)
    "C5:2 E5:6 r:2 G4:1 G4:1 G4:1 A4:1 C5:2",                       # 20 (24)
    C1,                                                             # 21 (25)
    C2,                                                             # 22 (26)
    "A4:2 A4:4 E5:1 E5:1 E5:2 D5:2 C5:2 C5:2",                      # 23 (27)
    "C5:16",                                                        # 24 마무리
]

SEMI = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def bars(lines):
    out = []
    for s in lines:
        m = []
        for t in s.split():
            p, d = t.split(":")
            tie = d.endswith("~")
            m.append((p, int(d.rstrip("~")), tie))
        assert sum(d for _, d, _ in m) == BAR, (s, sum(d for _, d, _ in m))
        out.append(m)
    return out


MUSIC = bars(MELODY)
assert len(MUSIC) == 24
LAST = len(MUSIC)
DYN = {1: "mp", 15: "mf", 17: "f"}
REHEARSAL = {9: "A", 17: "B"}
WORDS = {13: "cresc.", 23: "rit."}
RIT = {(23, 0): 94, (23, 4): 88, (23, 8): 82, (23, 12): 76, (24, 0): 70}
TYPES = {16: ("whole", 0), 12: ("half", 1), 8: ("half", 0), 6: ("quarter", 1), 4: ("quarter", 0),
         3: ("eighth", 1), 2: ("eighth", 0), 1: ("16th", 0)}


def note_xml(p, d, tie_start=False, tie_stop=False, fermata=False):
    t, dots = TYPES[d]
    if p == "r":
        whole = ' measure="yes"' if d == BAR else ""
        return f"<note><rest{whole}/><duration>{d}</duration><voice>1</voice>" + \
               ("" if d == BAR else f"<type>{t}</type>" + "<dot/>" * dots) + "</note>"
    step, octave = p[0], p[-1]
    alter = {"#": 1, "b": -1}.get(p[1], 0) if len(p) == 3 else 0
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


def part_xml():
    out = ['<part id="P1">']
    tie_open = False
    for i, m in enumerate(MUSIC, start=1):
        out.append(f'<measure number="{i}">')
        if i == 1:
            out.append("<attributes><divisions>4</divisions><key><fifths>0</fifths></key>"
                       "<time><beats>4</beats><beat-type>4</beat-type></time><clef><sign>G</sign><line>2</line></clef>"
                       "<transpose><diatonic>-1</diatonic><chromatic>-2</chromatic></transpose></attributes>")
            out.append(direction('<words font-weight="bold">Moderato</words>'))
            out.append(direction(f'<metronome parentheses="no"><beat-unit>quarter</beat-unit>'
                                 f'<per-minute>{TEMPO}</per-minute></metronome>', sound=f'<sound tempo="{TEMPO}"/>'))
        if i in REHEARSAL:
            out.append(direction(f'<rehearsal enclosure="square">{REHEARSAL[i]}</rehearsal>'))
        if i in WORDS:
            out.append(direction(f"<words>{WORDS[i]}</words>"))
        if i in DYN:
            out.append(direction(f"<dynamics><{DYN[i]}/></dynamics>", "below"))
        pos = 0
        for j, (p, d, tie) in enumerate(m):
            if (i, pos) in RIT:
                out.append(f'<direction><direction-type><words print-object="no"> </words></direction-type>'
                           f'<offset>0</offset><sound tempo="{RIT[(i, pos)]}"/></direction>')
            last = i == LAST and j == len(m) - 1
            out.append(note_xml(p, d, tie_start=tie, tie_stop=tie_open, fermata=last))
            tie_open = tie
            pos += d
        if i in (8, 16):
            out.append('<barline location="right"><bar-style>light-light</bar-style></barline>')
        if i == LAST:
            out.append('<barline location="right"><bar-style>light-heavy</bar-style></barline>')
        out.append("</measure>")
    out.append("</part>")
    return "\n".join(out)


TITLE, SUBTITLE, COMPOSER = "흔들리는 꽃들 속에서", "네 샴푸향이 느껴진거야", "장범준"


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
    with open(f"{sys.argv[1]}/shampoo_clarinet.musicxml", "w", encoding="utf-8") as f:
        f.write(score_xml())
    print("wrote shampoo_clarinet")
