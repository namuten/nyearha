#!/usr/bin/env python3
"""그대 안의 블루 (김현철 작곡, 이현승 작사, 이소라·김현철 노래, 1992) -- flute + B-flat clarinet duet -> MusicXML.

Copyrighted song; published here by the user's decision (2026-11-13).
Melody: the user's lead sheet (source/*.jpg, not committed), first verse + chorus, keys as on the sheet
(F major, then B-flat major from bar 10). 4/4, quarter = 70, 24 bars, about 1:30.

  bars  1-4   intro  (sheet BbM7 - C, flute pick-up line in bar 3)        mp
  bars  5-9   A  "난 난 눈을 감아요 ... 밀려오네"  (F major)               mp
  bars 10-15  B  "저 파란 어둠 속에서 ... 곁에 있는데"  (B-flat major)      mf
  bars 16-24  C  chorus "사랑은 아니지만 ... 그대"                         f -> 23 rit., fermata

Flute keeps the original rhythm (16ths, triplets, ties), concert D4-Bb5.
Clarinet = jazz-style accompaniment from 7th chords: half notes root -> 7th (guide tone),
quarter-note walking line (R-3-5-7) in the chorus and where the flute rests. Written E3-G4, below the break.

Durations are in 12ths of a quarter (quarter = 12, eighth = 6, 16th = 3, triplet eighth = 4, 4/4 bar = 48).
"""
import sys
from xml.sax.saxutils import escape

Q = 12
BAR = 4 * Q
TEMPO = 70
LETTERS = "CDEFGAB"
SEMI = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


# ---------------------------------------------------------------- pitch helpers
def split(p):
    step, rest = p[0], p[1:]
    alt = 0
    while rest and rest[0] in "#b":
        alt += 1 if rest[0] == "#" else -1
        rest = rest[1:]
    return step, alt, int(rest)


def midi(p):
    step, alt, octave = split(p)
    return 12 * (octave + 1) + SEMI[step] + alt


def transpose(p, letters, semis):
    """Diatonic transposition: move the letter by `letters` steps and the pitch by `semis` semitones."""
    if p == "r":
        return p
    step, _, octave = split(p)
    li = LETTERS.index(step) + letters
    nstep, octave = LETTERS[li % 7], octave + li // 7
    alt = midi(p) + semis - (12 * (octave + 1) + SEMI[nstep])
    return nstep + ("#" * alt if alt > 0 else "b" * -alt) + str(octave)


def bars(lines):
    """['E4:12 G4:12 ...', ...] -> [[('E4',12,False), ...], ...]  ('~' after a duration = tie to next note)"""
    out = []
    for line in lines:
        m = []
        for t in line.split():
            p, d = t.split(":")
            m.append((p, int(d.rstrip("~")), d.endswith("~")))
        assert sum(d for _, d, _ in m) == BAR, (line, sum(d for _, d, _ in m))
        out.append(m)
    return out


# ---------------------------------------------------------------- melody (concert pitch, as on the sheet)
INTRO = [
    "r:48",
    "r:48",
    "r:24 A4:4 Bb4:4 C5:4 A4:3 F4:3 G4:6~",                      # pick-up line
    "G4:24 r:24",
]
VERSE = [  # F major
    "A4:21 A4:3 Bb4:6 A4:3 G4:3~ G4:3 F4:3 G4:6~",               # 난 난 눈을 감아요
    "G4:18 G4:3 G4:3 A4:6 G4:3 F4:3~ F4:6 E4:6",                 # 빛과 그대 모습 사
    "E4:18 F4:3 F4:3~ F4:12 r:6 D4:3 D4:3",                      # 라져 이제
    "D4:6 E4:3 F4:3~ F4:24 r:6 D4:3 A4:3~",                      # 어 둠이 밀려
    "A4:6 Bb4:3 G4:3~ G4:12 r:24",                               # 오네
]
BRIDGE = [  # B-flat major
    "D5:18 D5:3 D5:3 Eb5:6 D5:3 C5:3~ C5:3 Bb4:3 C5:3 C5:3~",    # 저 파란 어둠 속에
    "C5:18 C5:3 C5:3 C5:4 D5:4 Eb5:4 D5:6 C5:3 C5:3~",           # 서 그대 왜 잠들어 가
    "C5:24 Bb4:12 r:12",                                         # 나
    "G4:6 A4:3 Bb4:3~ Bb4:24 r:9 Eb4:3",                         # 세상은 아
    "G4:6 A4:3 Bb4:3~ Bb4:12 D5:6 Eb5:3 C5:3~ C5:6 Bb4:3 Bb4:3~",  # 직 그대 곁에 있는
    "Bb4:36 r:6 Bb4:6",                                          # 데 사
]
CHORUS = [
    "G5:18 Bb4:6 A4:6 Bb4:3 C5:3~ C5:6 G5:6",                    # 랑은 아니지만
    "F5:24 F5:6 F5:3 Eb5:3~ Eb5:6 D5:6",                         # 우리의 만남
    "D5:6 Eb5:3 Eb5:3~ Eb5:12 r:6 C5:3 D5:3~ D5:6 Eb5:3 F5:3~",  # 어둠은 사라지
    "F5:24 G5:6 F5:6 r:6 Bb4:3 Bb4:3",                           # 네 오 시간
    "G5:21 G5:3 A5:6 Bb5:3 A5:3~ A5:6 G5:6",                     # 은 빛으로 물들
    "F5:24 Eb5:9 Eb5:3~ Eb5:6 D5:6",                             # 어 또 다시
    "D5:6 Bb4:3 Bb4:3~ Bb4:24 r:6 G4:3 G4:3",                    # 흐르네 내 눈
    "D5:18 Eb5:3 D5:3 C5:18 D5:3 D5:3~",                         # 빛 속 그대
    "D5:48",                                                     # (fermata)
]
SHEET = INTRO + VERSE + BRIDGE + CHORUS

# one chord per half bar, concert (lead-sheet chords as 7th chords for a jazz colour)
CHORDS = ("BbM7 BbM7 | C7 C7 | BbM7 BbM7 | C7 C7 | "                       # 1-4 intro
          "FM7 FM7 | Edim7 A7 | Dm7 Dm7 | BbM7 Gm7 | C7 C7 | "               # 5-9 A
          "BbM7 BbM7 | Am7b5 D7 | Gm7 Gm7 | EbM7 EbM7 | Cm7 F7 | BbM7 BbM7 | "  # 10-15 B
          "EbM7 F7/Eb | Dm7 G7 | Cm7 F7 | Bb7 Bb7 | EbM7 EbM7 | Dm7 G7 | Cm7 F7 | F7 F7 | BbM7 BbM7")
CHART = [b.split() for b in CHORDS.split("|")]
assert len(CHART) == len(SHEET) == 24 and all(len(b) == 2 for b in CHART)

# spelled chord tones (R, 3, 5, 7) as pitch classes with letters
SPELL = {
    "BbM7": ("Bb", "D", "F", "A"), "C7": ("C", "E", "G", "Bb"), "FM7": ("F", "A", "C", "E"),
    "Edim7": ("E", "G", "Bb", "Db"), "A7": ("A", "C#", "E", "G"), "Dm7": ("D", "F", "A", "C"),
    "Gm7": ("G", "Bb", "D", "F"), "Am7b5": ("A", "C", "Eb", "G"), "D7": ("D", "F#", "A", "C"),
    "EbM7": ("Eb", "G", "Bb", "D"), "Cm7": ("C", "Eb", "G", "Bb"), "F7": ("F", "A", "C", "Eb"),
    "F7/Eb": ("Eb", "A", "C", "F"), "Bb7": ("Bb", "D", "F", "Ab"), "G7": ("G", "B", "D", "F"),
}
LOW, HIGH = midi("D3"), midi("F4")      # concert = written E3-G4 on B-flat clarinet (below the break)


def in_range(name):
    """All octave placements of a pitch class name inside the clarinet range."""
    return [f"{name}{o}" for o in (3, 4) if LOW <= midi(f"{name}{o}") <= HIGH]


def nearest(name, prev):
    return min(in_range(name), key=lambda p: (abs(midi(p) - midi(prev)), midi(p)))


def root(chord):
    return in_range(SPELL[chord][0])[0]


def melody_bars():
    return bars(SHEET)


WALK = {4, 9, 12} | set(range(16, 24))   # quarter-note walking: flute rests (4, 9, 12) and the chorus


def clarinet():
    """concert. Half notes root -> 7th; walking bars R-3-5-7 (two chords: R-3, R-3); last bar whole root."""
    out = []
    for i, (c1, c2) in enumerate(CHART, start=1):
        if i == len(CHART):
            out.append([(root(c1), BAR, False)])
        elif i in WALK:
            seq = []
            for c, tones in ((c1, (0, 1, 2, 3)),) if c1 == c2 else ((c1, (0, 1)), (c2, (0, 1))):
                prev = root(c)
                for k in tones:
                    prev = root(c) if k == 0 else nearest(SPELL[c][k], prev)
                    seq.append((prev, Q, False))
            out.append(seq)
        elif c1 == c2:
            r = root(c1)
            out.append([(r, 2 * Q, False), (nearest(SPELL[c1][3], r), 2 * Q, False)])
        else:
            out.append([(root(c1), 2 * Q, False), (root(c2), 2 * Q, False)])
    return out


def written(music):
    """Concert -> B-flat clarinet (major 2nd up)."""
    return [[(transpose(p, 1, 2), d, t) for p, d, t in m] for m in music]


KEYS = {1: -1, 10: -2}                   # concert key signature changes (fifths)
DYN = {1: "mp", 10: "mf", 16: "f"}
PARTS = {
    "flute": dict(name="Flute", abbr="Fl.", music=melody_bars(), shift=0,
                  sound="wind.flutes.flute", dyn=DYN),
    "clarinet": dict(name="Clarinet in B♭", abbr="Cl.", music=written(clarinet()), shift=2,
                     transpose=(-1, -2), sound="wind.reed.clarinet.bflat", dyn=DYN),
}
REHEARSAL = {5: "A", 10: "B", 16: "C"}
WORDS = {23: "rit."}
TYPES = {48: ("whole", 0), 36: ("half", 1), 24: ("half", 0), 21: ("quarter", 2), 18: ("quarter", 1),
         12: ("quarter", 0), 9: ("eighth", 1), 6: ("eighth", 0), 4: ("eighth", 0), 3: ("16th", 0)}
RIT = {(23, 0): 64, (23, 24): 58, (24, 0): 52}


def note_xml(p, d, pos, tie_start=False, tie_stop=False, fermata=False):
    t, dots = TYPES[d]
    triplet = d == 4
    tm = "<time-modification><actual-notes>3</actual-notes><normal-notes>2</normal-notes></time-modification>" \
        if triplet else ""
    tup = ""
    if triplet and pos % Q == 0:
        tup = '<tuplet type="start" bracket="yes"/>'
    elif triplet and pos % Q == 8:
        tup = '<tuplet type="stop"/>'
    if p == "r":
        whole = ' measure="yes"' if d == BAR else ""
        x = f"<note><rest{whole}/><duration>{d}</duration><voice>1</voice>" + \
            ("" if d == BAR else f"<type>{t}</type>" + "<dot/>" * dots) + tm
        return x + (f"<notations>{tup}</notations>" if tup else "") + "</note>"
    step, alter, octave = split(p)
    x = f"<note><pitch><step>{step}</step>" + (f"<alter>{alter}</alter>" if alter else "") + \
        f"<octave>{octave}</octave></pitch><duration>{d}</duration>"
    x += '<tie type="stop"/>' * tie_stop + '<tie type="start"/>' * tie_start
    x += f"<voice>1</voice><type>{t}</type>" + "<dot/>" * dots + tm
    nots = '<tied type="stop"/>' * tie_stop + '<tied type="start"/>' * tie_start + tup
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
        out.append(f'<measure number="{i}">')
        a = ""
        if i in KEYS:
            a += f"<key><fifths>{KEYS[i] + P['shift']}</fifths></key>"
        if i == 1:
            a = f"<divisions>{Q}</divisions>" + a + "<time><beats>4</beats><beat-type>4</beat-type></time>"
            a += "<clef><sign>G</sign><line>2</line></clef>"
            if "transpose" in P:
                dia, chro = P["transpose"]
                a += f"<transpose><diatonic>{dia}</diatonic><chromatic>{chro}</chromatic></transpose>"
        if a:
            out.append(f"<attributes>{a}</attributes>")
        if i == 1 and top:
            out.append(direction('<words font-weight="bold">Slow, jazzy</words>'))
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
            last = i == len(P["music"]) and j == len(m) - 1
            out.append(note_xml(p, d, pos, tie_start=tie, tie_stop=tie_open, fermata=last))
            tie_open = tie
            pos += d
        if i + 1 in KEYS:
            out.append('<barline location="right"><bar-style>light-light</bar-style></barline>')
        if i == len(P["music"]):
            out.append('<barline location="right"><bar-style>light-heavy</bar-style></barline>')
        out.append("</measure>")
    out.append("</part>")
    return "\n".join(out)


TITLE, COMPOSER = "그대 안의 블루", "김현철 작곡 · 이현승 작사"


def score_xml(keys):
    head = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" '
            '"http://www.musicxml.org/dtds/partwise.dtd">',
            '<score-partwise version="4.0">',
            f"<work><work-title>{TITLE}</work-title></work>",
            f"<movement-title>{TITLE}</movement-title>",
            f'<identification><creator type="composer">{escape(COMPOSER)}</creator>'
            f'<creator type="lyricist">arr. 남연하 · flute &amp; clarinet duet</creator></identification>',
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
    duet = ["flute", "clarinet"]
    jobs = {"blue_full_score": duet}
    for k in duet:
        jobs[f"blue_{k}"] = [k]
    for name, keys in jobs.items():
        with open(f"{outdir}/{name}.musicxml", "w") as f:
            f.write(score_xml(keys))
        print("wrote", name)
