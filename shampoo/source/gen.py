#!/usr/bin/env python3
"""흔들리는 꽃들 속에서 네 샴푸향이 느껴진거야 (장범준, 2019) -- B-flat 클라리넷 솔로 하이라이트 -> MusicXML.

브런치 전체악보(https://brunch.co.kr/@mymars/883, G장조 3쪽)에서 반복 구간을 모두 덜어내고
가장 임팩트 있는 핵심 훅(타이틀 도입 -> 상승 프리코러스 -> 메인 후렴 -> AmM7 감성 브리지 -> 피날레)만
약 1분 10초(26마디) 길이로 압축한 클라리넷 솔로 콘서트 하이라이트 편곡.

- 기보 조: G장조(♯1, 콘서트 F장조), 4/4, ♩=94 (Andantino con moto, dolce e espressivo), 26마디.
- 구성 (반복 없이 4~8마디마다 전환되는 하이라이트 아치 구조):
  1) 1–2마디 (Intro): 원곡 코드(G - D/F# - Em7 | CM7 - D7sus4 - G) 압축 아르페지오 오프닝 & Stop-time 브레이크
  2) A (3–10마디, 1절 핵심 4마디 + 프리코러스 4마디):
     - 3–6마디: '흔들리는 꽃들 속에서 네 샴푸향이 느껴진 거야' (따뜻한 샬뤼모 저음 B3–E4 + Bm7 에코)
     - 7–10마디: 반복 없이 곧바로 '한번 연락해 볼까 용기 내 보지만 그냥 내 마음만 아쉬운 거야'로 상승 후 Stop-time & '걷다가 보면'
  3) B (11–18마디, 메인 후렴): '항상 이렇게 너를 바라만 보던 너를 기다린다고 말할까 / 계속 이렇게 너를 아쉬워하다 너를 연락했다 할까'
  4) C (19–26마디, 브리지 하이라이트 & 피날레 코다):
     - 19–23마디: '어떤 계절이 너를(B7-Em7) 바라만 보던 너를 기다리면서(AmM7, G#4) 아무말 못하고 그리워만 할까' + Stop-time
     - 24–26마디: 마지막 후렴 훅('항상 이렇게 너를 연락했다 할까', rit.) + 샬뤼모 저음 G장조 아르페지오 여운 페르마타
"""
import sys

BAR = 16
TEMPO = 94

# 토큰 형식: "음높이:길이[~][flags]"
#   ~ : 다음 음과 붙임줄(tie)
#   ( : 슬러(slur) 시작
#   ) : 슬러(slur) 끝
#   - : 테누토(tenuto)
MELODY = [
    # ── Intro (1–2): 임팩트 있는 2마디 어쿠스틱 훅 & Stop-time ──
    "G3:2( B3:2 D4:2 G4:2 F#4:2 D4:2 E4:2 B3:2)",                    # 1  G - D/F# - Em7
    "C4:2( E4:2 G4:2 A4:2 G4:4-) r:4",                               # 2  CM7 - D7sus4 - G (① Stop-time)

    # ── A (3–10): 타이틀 훅(4마디) + 상승 프리코러스(4마디) 직결 ──
    "r:2 A3:1( B3:1 B3:2 B3:2 B3:2 A3:2 A3:2 B3:2~",                 # 3  G ("흔들리는 꽃들 속에서 -")
    "B3:4-) F#3:2( B3:2 D4:4-) r:2 D4:2(",                           # 4  Bm7 샬뤼모 에코 | "네"
    "D4:2 E4:2 E4:2 E4:2 E4:2 D4:2 B3:2 C4:1 B3:1~",                 # 5  Em7 ("샴푸향이 느껴-진 거야")
    "B3:4-) F#3:2( B3:2 D4:4-) r:2 A3:1( B3:1",                      # 6  Bm7 에코 | "한번"
    "C4:2 C4:2 C4:1 E4:1 D4:2~ D4:4-) r:2 D4:2(",                    # 7  C - D ("연락해볼-까- 용")
    "D4:1 B3:1 B3:2 D4:2 F#4:2 E4:2~ E4:4-) E4:1( F#4:1",            # 8  Bm7 - Em7 ("기-내 보지만-- 그냥")
    "G4:2 G4:2 G4:1 E4:3 E4:2 G4:2 G4:2 A4:2~",                      # 9  Am7 ("내 마음-만 아쉬운 거야")
    "A4:8-) r:2 D4:2( E4:2 G4:2)",                                   # 10 C/D (① Stop-time) | "걷다가보면"

    # ── B (11–18): 메인 후렴 ("항상 이렇게 너를 바라만 보던 너를...") ──
    "B4:4- B4:3( A4:1 A4:2 B4:2 A4:2 G4:2~",                         # 11 G - D/F# - Em7 ("항상 - 이렇게 너 -")
    "G4:2) E4:4- A4:1( B4:1 A4:2 B4:2 A4:2 G4:2~",                   # 12 Em7 - G/D - CM7 ("- 를 바라만 보던 너 -")
    "G4:2) E4:4- B4:2( B4:1 A4:2 G4:1 G4:2 A4:2)",                   # 13 CM7 - D7sus4 - G ("- 를 기다린 다-고 말할까")
    "G4:2( B4:6-) r:2 D4:2( E4:2 G4:2)",                             # 14 G ("할까 - 지금 집앞에")
    "B4:4- B4:3( A4:1 A4:2 B4:2 A4:2 G4:2~",                         # 15 G - D/F# - Em7 ("계속 - 이렇게 너 -")
    "G4:2) E4:4- A4:1( B4:1 A4:2 B4:2 A4:2 G4:2~",                   # 16 Em7 - G/D - CM7 ("- 를 아쉬워 하다 너 -")
    "G4:2) E4:4- B4:2( B4:1 A4:2 G4:1 G4:2 G4:2~",                   # 17 CM7 - D7sus4 - CM7 ("- 를 연락했다 할까 -")
    "G4:4-) C4:2( E4:2 G4:4-) r:2 G4:2(",                            # 18 CM7 에코 | "어떤"

    # ── C (19–26): 감성 브리지 하이라이트(B7-Em7, AmM7) & 피날레 코다 ──
    "F#4:2 B4:2 B4:2 A4:2~ A4:2) G4:4- G4:2(",                       # 19 B7 - Em7 ("계절이 너-를 바라")
    "A4:2 B4:2 A4:2 G4:2~ G4:2) E4:4- A4:2(",                        # 20 Em7/G - Am7 ("만 보던 너-를 기")
    "A4:2 G#4:1 A4:2 B4:1~ B4:6-) r:2 A4:2(",                        # 21 AmM7 ("다리-면서 - 아무")
    "A4:2 E4:1 G4:1~ G4:4-) r:2 G4:2( A4:2 G4:1 E4:1~",              # 22 Am7 ("말 못하-고 그리워 만-")
    "E4:1 G4:1 A4:6-) r:2 D4:2( E4:2 G4:2)",                         # 23 C/D (① Stop-time) | "할-까 - 걷다가보면"
    "B4:4- B4:3( A4:1 A4:2 B4:2 A4:2 G4:2~",                         # 24 G - D/F# - Em7 ("항상 - 이렇게 너 -")
    "G4:2) E4:4- B4:2( B4:1 A4:2 G4:1 G4:2 G4:2~",                   # 25 CM7 - D7sus4 - G ("- 를 연락했다 할까 -", rit.)
    "G4:4-) D3:2( G3:2 B3:8-)",                                      # 26 G 따뜻한 샬뤼모 저음 아르페지오 코다
]


def parse_token(tok):
    p, rest = tok.split(":")
    digits = [ch for ch in rest if ch.isdigit()]
    flags = {ch for ch in rest if not ch.isdigit()}
    d = int("".join(digits))
    return p, d, ("~" in flags), ("(" in flags), (")" in flags), ("-" in flags)


def bars(lines):
    out = []
    for idx, s in enumerate(lines, start=1):
        m = [parse_token(t) for t in s.split()]
        total = sum(item[1] for item in m)
        assert total == BAR, f"Bar {idx}: expected {BAR}, got {total} in {s!r}"
        out.append(m)
    return out


MUSIC = bars(MELODY)
assert len(MUSIC) == 26
LAST = len(MUSIC)

DYN = {
    1: "mp",
    3: "mp",
    7: "mf",
    11: "f",
    19: "mp",
    21: "mf",
    24: "f",
    26: "mp",
}
REHEARSAL = {3: "A", 11: "B", 19: "C"}
WORDS = {
    3: "cantabile, warm low register",
    9: "cresc.",
    11: "espressivo",
    19: "dolce",
    21: "cresc.",
    24: "appassionato",
    25: "rit. e dim.",
}
RIT = {
    (25, 0): 88,
    (25, 4): 84,
    (25, 8): 78,
    (25, 12): 72,
    (26, 0): 66,
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


def note_xml(p, d, tie_start=False, tie_stop=False, slur_start=False, slur_stop=False,
             tenuto=False, fermata=False):
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
    for i, m in enumerate(MUSIC, start=1):
        out.append(f'<measure number="{i}">')
        if i == 1:
            # 기보 G장조(fifths=1), B-flat 클라리넷 이조(콘서트 F장조)
            out.append("<attributes><divisions>4</divisions><key><fifths>1</fifths></key>"
                       "<time><beats>4</beats><beat-type>4</beat-type></time><clef><sign>G</sign><line>2</line></clef>"
                       "<transpose><diatonic>-1</diatonic><chromatic>-2</chromatic></transpose></attributes>")
            out.append(direction('<words font-weight="bold">Andantino con moto, dolce e espressivo</words>'))
            out.append(direction(f'<metronome parentheses="no"><beat-unit>quarter</beat-unit>'
                                 f'<per-minute>{TEMPO}</per-minute></metronome>', sound=f'<sound tempo="{TEMPO}"/>'))
        if i in REHEARSAL:
            out.append(direction(f'<rehearsal enclosure="square">{REHEARSAL[i]}</rehearsal>'))
        if i in WORDS:
            out.append(direction(f'<words font-style="italic">{WORDS[i]}</words>'))
        if i in DYN:
            out.append(direction(f"<dynamics><{DYN[i]}/></dynamics>", "below"))
        pos = 0
        for j, (p, d, tie, sl_start, sl_stop, ten) in enumerate(m):
            if (i, pos) in RIT:
                out.append(f'<direction><direction-type><words print-object="no"> </words></direction-type>'
                           f'<offset>0</offset><sound tempo="{RIT[(i, pos)]}"/></direction>')
            last = i == LAST and j == len(m) - 1
            out.append(note_xml(
                p, d,
                tie_start=tie,
                tie_stop=tie_open,
                slur_start=sl_start,
                slur_stop=sl_stop,
                tenuto=ten,
                fermata=last,
            ))
            tie_open = tie
            pos += d
        if i in (2, 10, 18):
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
