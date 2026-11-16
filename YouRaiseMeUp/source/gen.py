#!/usr/bin/env python3
"""You Raise Me Up (Rolf Løvland, 2002) -- chorus call-and-response duet, flute + B-flat clarinet -> MusicXML.

Copyrighted song; published here by the user's decision (2026-11-13, rearranged 2026-11-16).
Melody: the chorus from the G-major lead sheet the user supplied (source/*.gif), placed in concert F major
(clarinet written G major) so flute (concert E4-G5) and clarinet (written F#3-A4, below the break) trade every
2-bar vocal phrase starting on each "You raise me" / "I am" pickup and unite in octaves on the final phrase.
Concert F major, 4/4, quarter = 66, 17 bars, about 1:11.

  bar  1b3 - 3b2   A1 "You raise me up, so I can stand on mountains"      Cl. lead (mf) / Fl. half notes (p)
  bar  3b3 - 5b2   A2 "You raise me up, to walk on stormy seas"           Fl. lead (mf) / Cl. half notes (mp)
  bar  5b4 - 7b2   A3 "I am strong when I am on your shoulders"           Cl. lead (mf) / Fl. half notes (mp)
  bar  7b3 - 9b2   A4 "You raise me up, to more than I can be"            Fl. lead (mf) / Cl. half notes (mp)
  bar  9b3 - 11b2  B1 "You raise me up, so I can stand on mountains"      Cl. lead (f)  / Fl. quarters (mf)
  bar 11b3 - 13b2  B2 "You raise me up, to walk on stormy seas"           Fl. lead (f)  / Cl. quarters (mf)
  bar 13b4 - 15b2  B3 "I am strong when I am on your shoulders"           Cl. lead (f)  / Fl. quarters (mf)
  bar 15b3 - 17    B4 "You raise me up, to more than I can be"            Fl. + Cl. octave duet (f -> 16 rit., fermata)

Easy rules (checked by test_gen.py):
  original rhythm kept (eighths, dotted quarter + eighth, eighth rests) -- no ties, no 16ths, no non-key accidentals.
  flute concert E4-G5 (F major); clarinet written E3-A4 (concert D3-G4, below the break, written G major).

All pitches here are CONCERT pitch; the clarinet part is written a major 2nd higher.
Durations are in 16ths (one 4/4 bar = 16, one half-bar = 8).
"""
import sys
from xml.sax.saxutils import escape

BAR = 16
HALF = 8
TEMPO = 66
LETTERS = "CDEFGAB"
SEMI = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


# ---------------------------------------------------------------- notation & pitch helpers
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
    if p == "r":
        return p
    step, _, octave = split(p)
    li = LETTERS.index(step) + letters
    nstep, octave = LETTERS[li % 7], octave + li // 7
    alt = midi(p) + semis - (12 * (octave + 1) + SEMI[nstep])
    return nstep + ("#" * alt if alt > 0 else "b" * -alt) + str(octave)


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


def split_halves(m):
    """Split a 16-sixteenth bar into two 8-sixteenth half-bars."""
    h1, h2, pos = [], [], 0
    for item in m:
        (h1 if pos < HALF else h2).append(item)
        pos += item[1]
    assert sum(d for _, d, _ in h1) == HALF and sum(d for _, d, _ in h2) == HALF, m
    return h1, h2


# ---------------------------------------------------------------- melody (concert F major, flute register E4-G5)
CHORUS = [
    "F5:6 E5:2 E5:2 D5:2 C5:2 Bb4:2",     # up, so I can stand on
    "C5:2 A4:2 F4:4 r:2 C5:2 G5:2 F5:2",  # mountains. You raise me
    "F5:6 E5:2 E5:2 D5:2 C5:2 Bb4:2",     # up, to walk on stormy
    "C5:8 r:4 C5:2 E5:2",                 # seas. I am
    "F5:6 E5:2 E5:2 D5:2 C5:2 Bb4:2",     # strong when I am on your
    "C5:4 F5:4 r:2 D5:2 C5:2 Bb4:2",      # shoulders. You raise me
    "A4:4 r:2 C5:2 A4:2 G4:2 F4:2 E4:2",  # up, to more than I can
]
MELODY = (
    ["F4:8 r:2 C5:2 D5:2 E5:2"]           # 1 intro -- You raise me
    + CHORUS                              # 2-8  A
    + ["F4:8 r:2 C5:2 D5:2 E5:2"]         # 9    be. You raise me
    + CHORUS                              # 10-16 B
    + ["F5:16"]                           # 17   be.
)

# one chord per half bar (2 per bar), CONCERT F major
CHORUS_CHORDS = "Dm C | F C | Dm Bb | F C | F Bb | F C | F C"
CHORDS = "F C | " + CHORUS_CHORDS + " | F C | " + CHORUS_CHORDS + " | F F"
CHART = [b.split() for b in CHORDS.split("|")]
assert len(CHART) == len(MELODY) == 17 and all(len(b) == 2 for b in CHART)

# Upper accompaniment voicings for flute (concert F major, A4-F5, always > clarinet melody E3-G4)
VOICE_FL = {
    "F":  ("A4", "C5", "F5"),
    "Bb": ("Bb4", "D5", "F5"),
    "C":  ("A4", "C5", "E5"),
    "Dm": ("A4", "D5", "F5"),
}
# Lower accompaniment voicings for clarinet (concert F major, D3-C4 = written E3-D4, always < flute melody E4-G5)
VOICE_CL = {
    "F":  ("F3", "A3", "C4"),
    "Bb": ("D3", "F3", "Bb3"),
    "C":  ("E3", "G3", "C4"),
    "Dm": ("D3", "F3", "A3"),
}

MEL_FL = bars(" | ".join(MELODY))
MEL_CL = [[(transpose(p, -7, -12), d, t) for p, d, t in m] for m in MEL_FL]

# Half-bar indices (0..31 for bars 1..16) where each instrument plays the lead melody:
# Phrase handoffs occur at the pickup rest (half-bar 1, 5, 9, 13, 17, 21, 25, 29); both unite on 29..31 + bar 17.
CLARINET_LEAD_HALVES = {1, 2, 3, 4, 9, 10, 11, 12, 17, 18, 19, 20, 25, 26, 27, 28, 29, 30, 31}
FLUTE_LEAD_HALVES = {5, 6, 7, 8, 13, 14, 15, 16, 21, 22, 23, 24, 29, 30, 31}


def acc_half(voice_map, chord, section_b):
    lo, mid, _ = voice_map[chord]
    return [(lo, 4, False), (mid, 4, False)] if section_b else [(lo, 8, False)]


def flute():
    """Flute in CONCERT F major (E4-G5): trades 2-bar phrases with clarinet and unites in octaves at the end."""
    out = []
    for i, chords in enumerate(CHART, start=1):
        if i == len(CHART):
            out.append(list(MEL_FL[-1]))
            continue
        mh1, mh2 = split_halves(MEL_FL[i - 1])
        h1_idx, h2_idx = 2 * (i - 1), 2 * (i - 1) + 1
        p1 = mh1 if h1_idx in FLUTE_LEAD_HALVES else acc_half(VOICE_FL, chords[0], h1_idx >= 17)
        p2 = mh2 if h2_idx in FLUTE_LEAD_HALVES else acc_half(VOICE_FL, chords[1], h2_idx >= 17)
        out.append(p1 + p2)
    return out


def clarinet():
    """Clarinet in CONCERT F major (D3-G4, written G major E3-A4): trades 2-bar phrases with flute."""
    out = []
    for i, chords in enumerate(CHART, start=1):
        if i == len(CHART):
            out.append(list(MEL_CL[-1]))
            continue
        mh1, mh2 = split_halves(MEL_CL[i - 1])
        h1_idx, h2_idx = 2 * (i - 1), 2 * (i - 1) + 1
        p1 = mh1 if h1_idx in CLARINET_LEAD_HALVES else acc_half(VOICE_CL, chords[0], h1_idx >= 17)
        p2 = mh2 if h2_idx in CLARINET_LEAD_HALVES else acc_half(VOICE_CL, chords[1], h2_idx >= 17)
        out.append(p1 + p2)
    return out


def up_major_second(p):
    """Concert -> written for B-flat clarinet (major 2nd up), spelled diatonically."""
    return transpose(p, 1, 2)


def written(music):
    return [[(up_major_second(p), d, t) for p, d, t in m] for m in music]


DYN_FL = {
    (1, 0): "p", (3, 8): "mf", (5, 8): "mp", (7, 8): "mf",
    (9, 8): "mf", (11, 8): "f", (13, 8): "mf", (15, 8): "f",
}
DYN_CL = {
    (1, 0): "mf", (3, 8): "mp", (5, 8): "mf", (7, 8): "mp",
    (9, 8): "f", (11, 8): "mf", (13, 8): "f",
}
PARTS = {
    "flute": dict(name="Flute", abbr="Fl.", music=flute(), fifths=-1, clef=("G", 2),
                  sound="wind.flutes.flute", dyn=DYN_FL),
    "clarinet": dict(name="Clarinet in B♭", abbr="Cl.", music=written(clarinet()), fifths=1,
                     clef=("G", 2), transpose=(-1, -2, 0), sound="wind.reed.clarinet.bflat",
                     dyn=DYN_CL),
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
        pos = 0
        for j, (p, d, tie) in enumerate(m):
            if (i, pos) in P["dyn"]:
                out.append(direction(f'<dynamics><{P["dyn"][(i, pos)]}/></dynamics>', "below"))
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
