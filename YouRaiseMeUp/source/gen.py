#!/usr/bin/env python3
"""You Raise Me Up (Rolf Løvland, 2002) -- chorus only, flute + B-flat clarinet duet -> MusicXML.

Copyrighted song; published here by the user's decision (2026-11-13).
Melody: the chorus from the G-major lead sheet the user supplied (source/*.gif), moved up a minor 3rd.
Concert B-flat major, 4/4, quarter = 66, 17 bars, about 1:10.

  bar   1     intro (ends with the "You raise me" pickup)   mf
  bars  2-9   A  chorus, first time                        mf
  bars 10-17  B  chorus, second time (climax)              f   -> 16 rit., fermata on the last note

Easy rules (checked by test_gen.py):
  original rhythm kept (eighths, dotted quarter + eighth, eighth rests) -- no ties, no 16ths, no accidentals.
  flute concert A4-C6; clarinet written E3-G4 (concert D3-F4, below the break), written C major.

All pitches here are CONCERT pitch; the clarinet part is written a major 2nd higher.
Durations are in 16ths (one 4/4 bar = 16).
"""
import sys
from xml.sax.saxutils import escape

BAR = 16
TEMPO = 66


# ---------------------------------------------------------------- notation
def bars(s):
    """'D5:4 Eb5:4 F5:8 | ...' -> [[('D5',4,False), ...], ...]"""
    out = []
    for bar in s.split("|"):
        toks = bar.split()
        if not toks:
            continue
        m = []
        for t in toks:
            p, d = t.split(":")
            tie = d.endswith("~")
            m.append((p, int(d.rstrip("~")), tie))
        assert sum(d for _, d, _ in m) == BAR, (bar, sum(d for _, d, _ in m))
        out.append(m)
    return out


# ---------------------------------------------------------------- melody (flute, concert) -- one line per bar
CHORUS = [
    "Bb5:6 A5:2 A5:2 G5:2 F5:2 Eb5:2",    # up, so I can stand on
    "F5:2 D5:2 Bb4:4 r:2 F5:2 C6:2 Bb5:2",  # mountains. You raise me
    "Bb5:6 A5:2 A5:2 G5:2 F5:2 Eb5:2",    # up, to walk on stormy
    "F5:8 r:4 F5:2 A5:2",                 # seas. I am
    "Bb5:6 A5:2 A5:2 G5:2 F5:2 Eb5:2",    # strong when I am on your
    "F5:4 Bb5:4 r:2 G5:2 F5:2 Eb5:2",     # shoulders. You raise me
    "D5:4 r:2 F5:2 D5:2 C5:2 Bb4:2 A4:2", # up, to more than I can
]
MELODY = (
    ["Bb4:8 r:2 F5:2 G5:2 A5:2"]          # 1 intro -- You raise me
    + CHORUS                              # 2-8  A
    + ["Bb4:8 r:2 F5:2 G5:2 A5:2"]        # 9    be. You raise me
    + CHORUS                              # 10-16 B
    + ["Bb4:16"]                          # 17   be.
)

# one chord per half bar (2 per bar)
CHORUS_CHORDS = "Gm F7 | Bb F7 | Gm Eb | Bb F7 | Bb Eb | Bb F7 | Bb F7"
CHORDS = "Bb F7 | " + CHORUS_CHORDS + " | Bb F7 | " + CHORUS_CHORDS + " | Bb Bb"
CHART = [b.split() for b in CHORDS.split("|")]
assert len(CHART) == len(MELODY) == 17 and all(len(b) == 2 for b in CHART)

# clarinet voicings (concert, all within D3-F4): low, middle, high
VOICE = {
    "Bb": ("Bb3", "D4", "F4"), "Eb": ("Eb3", "G3", "Bb3"), "F7": ("F3", "A3", "Eb4"), "Gm": ("G3", "Bb3", "D4"),
}
SEMI = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def midi(p):
    step, rest = p[0], p[1:]
    alt = 0
    while rest and rest[0] in "#b":
        alt += 1 if rest[0] == "#" else -1
        rest = rest[1:]
    return 12 * (int(rest) + 1) + SEMI[step] + alt


def melody_bars():
    return bars(" | ".join(MELODY))


def clarinet():
    """1-9: half notes on the chord's low note. 10-16: quarters (low, middle per half bar). 17: whole B-flat."""
    out = []
    for i, chords in enumerate(CHART, start=1):
        if i == len(CHART):
            out.append([(VOICE[chords[0]][0], 16, False)])
        elif i <= 9:
            out.append([(VOICE[c][0], 8, False) for c in chords])
        else:
            b = []
            for c in chords:
                lo, mid, _ = VOICE[c]
                b += [(lo, 4, False), (mid, 4, False)]
            out.append(b)
    return out


def up_major_second(p):
    """Concert -> written for B-flat clarinet (major 2nd up), spelled diatonically."""
    if p == "r":
        return p
    letters = "CDEFGAB"
    step = p[0]
    li = letters.index(step)
    nstep = letters[(li + 1) % 7]
    target = midi(p) + 2
    octave = int(p.lstrip("CDEFGAB#b")) + (1 if step == "B" else 0)
    alt = target - (12 * (octave + 1) + SEMI[nstep])
    return nstep + ("#" * alt if alt > 0 else "b" * -alt) + str(octave)


def written(music):
    return [[(up_major_second(p), d, t) for p, d, t in m] for m in music]


PARTS = {
    "flute": dict(name="Flute", abbr="Fl.", music=melody_bars(), fifths=-2, clef=("G", 2),
                  sound="wind.flutes.flute", dyn={1: "mf", 10: "f"}),
    "clarinet": dict(name="Clarinet in B♭", abbr="Cl.", music=written(clarinet()), fifths=0,
                     clef=("G", 2), transpose=(-1, -2, 0), sound="wind.reed.clarinet.bflat",
                     dyn={1: "mf", 10: "f"}),
}
REHEARSAL = {2: "A", 10: "B"}
WORDS = {16: "rit."}
TYPES = {16: ("whole", 0), 12: ("half", 1), 8: ("half", 0), 6: ("quarter", 1), 4: ("quarter", 0),
         3: ("eighth", 1), 2: ("eighth", 0), 1: ("16th", 0)}
# rit. over the last two bars (per-half-bar playback tempo), final bar held under a fermata
RIT = {(16, 0): 62, (16, 8): 56, (17, 0): 50}


def note_xml(p, d, tie_start=False, tie_stop=False, fermata=False):
    t, dots = TYPES[d]
    if p == "r":
        whole = ' measure="yes"' if d == BAR else ""
        return f"<note><rest{whole}/><duration>{d}</duration><voice>1</voice>" + \
               ("" if d == BAR else f"<type>{t}</type>") + "</note>"
    step, rest = p[0], p[1:]
    alter = 0
    while rest and rest[0] in "#b":
        alter += 1 if rest[0] == "#" else -1
        rest = rest[1:]
    x = f"<note><pitch><step>{step}</step>" + (f"<alter>{alter}</alter>" if alter else "") + \
        f"<octave>{rest}</octave></pitch><duration>{d}</duration>"
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
        out.append(f'<measure number="{i}">')
        if i == 1:
            a = "<attributes><divisions>4</divisions>"
            a += f"<key><fifths>{P['fifths']}</fifths></key><time><beats>4</beats><beat-type>4</beat-type></time>"
            a += f"<clef><sign>{P['clef'][0]}</sign><line>{P['clef'][1]}</line></clef>"
            if "transpose" in P:
                dia, chro, octc = P["transpose"]
                a += f"<transpose><diatonic>{dia}</diatonic><chromatic>{chro}</chromatic>"
                a += (f"<octave-change>{octc}</octave-change>" if octc else "") + "</transpose>"
            out.append(a + "</attributes>")
            if top:
                out.append(direction('<words font-weight="bold">Moderato</words>'))
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
            out.append(note_xml(p, d, tie_start=tie, tie_stop=tie_open, fermata=last))
            tie_open = tie
            pos += d
        if i == len(P["music"]):
            out.append('<barline location="right"><bar-style>light-heavy</bar-style></barline>')
        out.append("</measure>")
    out.append("</part>")
    return "\n".join(out)


TITLE, COMPOSER = "You Raise Me Up", "Rolf Løvland"


def score_xml(keys):
    head = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" '
            '"http://www.musicxml.org/dtds/partwise.dtd">',
            '<score-partwise version="4.0">',
            f"<work><work-title>{TITLE}</work-title></work>",
            f"<movement-title>{TITLE}</movement-title>",
            f'<identification><creator type="composer">{COMPOSER}</creator>'
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
    jobs = {"youraisemeup_full_score": duet}
    for k in duet:
        jobs[f"youraisemeup_{k}"] = [k]
    for name, keys in jobs.items():
        with open(f"{outdir}/{name}.musicxml", "w") as f:
            f.write(score_xml(keys))
        print("wrote", name)
