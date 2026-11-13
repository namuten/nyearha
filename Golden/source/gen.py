#!/usr/bin/env python3
"""Golden (HUNTR/X, KPop Demon Hunters, 2025) -- flute + B-flat clarinet duet -> MusicXML.

Copyrighted song; published here by the user's decision (2026-11-13).
Melody: the user's G-major lead sheet (source/*.pdf, not committed), moved up a perfect 4th to concert C major.
Concert C major, 4/4, quarter = 120, 44 bars, about 1:30.

  bars  1-4   intro  (sheet 21-24 "dreamin' hard ... we're goin'")        mp
  bars  5-20  A  chorus, first time  (sheet 25-40)                        mf
  bars 21-36  B  chorus, second time (climax, sheet 58-73)                f
  bars 37-44  C  ending "gonna be, gonna be golden" (sheet 74-81)         f -> 43 rit., fermata

Melody keeps the original rhythm (triplets, eighth anticipations); no 16ths.
Flute concert G4-D6. Clarinet written D major, below the break: chords (A half notes, B quarters).

Melody lines below are written in the SHEET key (G major) and transposed in code.
Durations are in 12ths of a quarter (quarter = 12, eighth = 6, triplet eighth = 4, 4/4 bar = 48).
"""
import sys
from xml.sax.saxutils import escape

Q = 12
BAR = 4 * Q
TEMPO = 120
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


# ---------------------------------------------------------------- melody (sheet key G major)
T3 = "D5:4 D5:4 D5:4 D5:4 C5:4 C5:4"          # "gonna be, gonna be" / "you know together we're"
INTRO = [
    "E4:12 G4:12 C5:12 B4:12",                 # dreamin' hard, we
    "D4:12 G4:12 E5:12 D5:12",                 # came so far, now
    "F#4:12 A4:12 D5:24~",                     # I be-lieve
    "D5:24 B4:6 B4:12 E5:6",                   # We're go-in'
]
CHORUS = [
    "E5:12 E5:12 E5:6 B4:6 B4:6 D5:6",         # up, up, up, it's our
    "D5:12 G4:6 r:6 " + T3,                    # moment. You know together we're
    "C5:6 B4:12 r:6 " + T3,                    # glowing. Gonna be, gonna be
    "C5:6 B4:12 r:6 A4:12 B4:6 G4:6",          # golden. Oh,
    "E5:12 E5:12 G5:6 F#5:6 E5:6 D5:6",        # up, up, up with our
    "D5:12 G4:6 r:6 " + T3,                    # voices ...
    "C5:6 B4:12 r:6 " + T3,                    # ... Gonna be, gonna be
    "C5:6 B4:12 r:6 A4:12 B4:6 G4:6",          # golden. Oh,
    "E4:12 G4:12 C5:12 B4:12",                 # I'm done hidin',
    "D4:12 F#4:12 E5:12 D5:12",                # now I'm shinin'
    "G4:12 B4:12 A5:12 F#5:6 G5:6~",           # like I'm born to be.
    "G5:12 E5:12 r:12 F#4:12",                 # Oh,
    "E4:12 G4:12 C5:12 B4:12",                 # our time, no
    "D4:12 F#4:12 E5:12 D5:12",                # fears, no lies, that's
    "G4:12 B4:12 A5:12 F#5:6 G5:6~",           # who we're born to be.
]
TURN = "G5:12 E5:12 B4:6 B4:12 E5:6"           # (be.) We're go-in'  -> chorus 2
LAST = "G5:12 E5:6 r:6 D5:12 D5:6 A4:6"        # (be.) You know we're
A6 = "A4:4 A4:4 A4:4 A4:4 A4:4 A4:4"
ENDING = [
    A6 + " A4:6 B4:12 G4:6",                   # gonna be, gonna be golden. We're
    A6 + " r:24",                              # gonna be, gonna be
    A6 + " A4:6 B4:12 G4:6",                   # born to be, born to be glowin'
    A6 + " r:6 A4:6 G4:6 F#4:6",               # ... You know that
    "E4:12 G4:12 C5:12 B4:12",                 # it's our time, no
    "D4:12 F#4:12 E5:12 D5:12",                # fears, no lies, that's
    "G4:12 B4:12 A5:12 F#5:6 G5:6~",           # who we're born to
    "G5:36 E5:12",                             # be.
]
SHEET = INTRO + CHORUS + [TURN] + CHORUS + [LAST] + ENDING

# one chord per half bar, CONCERT C major
INTRO_CH = "F F | C C | G G | G Am"
CHORUS_CH = ("F F | G G | C C | Am Am | F F | G G | C C | Am Am | "
             "F F | G G | C C | Am Am | F F | G G | C C")
ENDING_CH = "G C | G G | G C | G G | F F | G G | C C | F F"
CHORDS = f"{INTRO_CH} | {CHORUS_CH} | Am Am | {CHORUS_CH} | Am G | {ENDING_CH}"
CHART = [b.split() for b in CHORDS.split("|")]
assert len(CHART) == len(SHEET) == 44 and all(len(b) == 2 for b in CHART)

# clarinet voicings (concert, D3-F4 = written E3-G4, below the break): low, middle, high
VOICE = {
    "F": ("F3", "A3", "C4"), "C": ("E3", "G3", "C4"), "G": ("G3", "B3", "D4"), "Am": ("A3", "C4", "E4"),
}


def melody_bars():
    """Flute, concert pitch: the sheet melody up a perfect 4th (G major -> C major)."""
    return [[(transpose(p, 3, 5), d, t) for p, d, t in m] for m in bars(SHEET)]


def clarinet():
    """concert. 1-20: half notes (low, middle). 21-36: quarters low-middle-high-middle (two chords: low-middle each).
    37-43: half notes low; 44: whole low under the fermata."""
    out = []
    for i, (c1, c2) in enumerate(CHART, start=1):
        if i == len(CHART):
            out.append([(VOICE[c1][0], BAR, False)])
        elif 21 <= i <= 36:
            if c1 == c2:
                lo, mid, hi = VOICE[c1]
                out.append([(lo, Q, False), (mid, Q, False), (hi, Q, False), (mid, Q, False)])
            else:
                out.append([(VOICE[c][k], Q, False) for c in (c1, c2) for k in (0, 1)])
        elif i <= 20:
            out.append([(VOICE[c1][0], 2 * Q, False), (VOICE[c2][1], 2 * Q, False)])
        else:
            out.append([(VOICE[c][0], 2 * Q, False) for c in (c1, c2)])
    return out


def written(music):
    """Concert -> B-flat clarinet (major 2nd up)."""
    return [[(transpose(p, 1, 2), d, t) for p, d, t in m] for m in music]


DYN = {1: "mp", 5: "mf", 21: "f"}
PARTS = {
    "flute": dict(name="Flute", abbr="Fl.", music=melody_bars(), fifths=0,
                  sound="wind.flutes.flute", dyn=DYN),
    "clarinet": dict(name="Clarinet in B♭", abbr="Cl.", music=written(clarinet()), fifths=2,
                     transpose=(-1, -2), sound="wind.reed.clarinet.bflat", dyn=DYN),
}
REHEARSAL = {5: "A", 21: "B", 37: "C"}
WORDS = {4: "cresc.", 43: "rit."}
# (eighth note = 6, triplet eighth = 4 with time-modification)
TYPES = {48: ("whole", 0), 36: ("half", 1), 24: ("half", 0), 18: ("quarter", 1), 12: ("quarter", 0),
         6: ("eighth", 0), 4: ("eighth", 0)}
RIT = {(43, 0): 112, (43, 24): 100, (44, 0): 88}


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
        if i == 1:
            a = f"<attributes><divisions>{Q}</divisions>"
            a += f"<key><fifths>{P['fifths']}</fifths></key><time><beats>4</beats><beat-type>4</beat-type></time>"
            a += "<clef><sign>G</sign><line>2</line></clef>"
            if "transpose" in P:
                dia, chro = P["transpose"]
                a += f"<transpose><diatonic>{dia}</diatonic><chromatic>{chro}</chromatic></transpose>"
            out.append(a + "</attributes>")
            if top:
                out.append(direction('<words font-weight="bold">Bright pop</words>'))
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
        if i == len(P["music"]):
            out.append('<barline location="right"><bar-style>light-heavy</bar-style></barline>')
        out.append("</measure>")
    out.append("</part>")
    return "\n".join(out)


TITLE, COMPOSER = "Golden", "EJAE, Mark Sonnenblick, IDO, 24, TEDDY"


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
    jobs = {"golden_full_score": duet}
    for k in duet:
        jobs[f"golden_{k}"] = [k]
    for name, keys in jobs.items():
        with open(f"{outdir}/{name}.musicxml", "w") as f:
            f.write(score_xml(keys))
        print("wrote", name)
