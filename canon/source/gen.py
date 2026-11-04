#!/usr/bin/env python3
"""Canon in D (wind quintet + trumpet) -> MusicXML.

Pitches are WRITTEN pitches (as printed in each part). Durations in 16ths.
Transcribed from canon/assets/png/*.png (original MuseScore 4.7.5 export).
"""
import sys
from xml.sax.saxutils import escape

# ---------------------------------------------------------------- notation
def bars(s):
    """'F#5:4 E5:4 | r:16' -> [[('F#5',4),('E5',4)], [('r',16)]]"""
    out = []
    for bar in s.split("|"):
        toks = bar.split()
        if not toks:
            continue
        m = []
        for t in toks:
            p, d = t.split(":")
            m.append((p, int(d)))
        assert sum(d for _, d in m) == 16, (bar, sum(d for _, d in m))
        out.append(m)
    return out

R = "r:16"
def rep(s, n):
    return " | ".join([s] * n)

FLUTE = bars(" | ".join([
    rep(R, 4),
    "F#5:4 E5:4 D5:4 C#5:4", "B4:4 A4:4 B4:4 C#5:4",
    "D5:4 C#5:4 B4:4 A4:4", "G4:4 F#4:4 G4:4 E4:4",
    "D5:2 F#5:2 A5:2 G5:2 F#5:2 D5:2 F#5:2 E5:2",
    "D5:2 B4:2 D5:2 A5:2 G5:2 B5:2 A5:2 G5:2",
    "F#4:2 D4:2 E4:2 C#5:2 D5:2 F#5:2 A5:2 A4:2",
    "B4:2 G4:2 A4:2 F#4:2 D4:2 D5:2 D5:2 C#5:2",
    "A5:8 F#5:8", "D5:8 B4:4 C#5:4",
    "D5:2 A4:2 C#5:2 E5:2 D5:2 B4:2 C#5:2 A4:2",
    "B4:2 D5:2 A4:2 F#4:2 G4:2 B4:2 A4:2 C#5:2",
    "D5:1 C#5:1 D5:1 D4:1 C#4:1 A4:1 E4:1 F#4:1 D4:1 D5:1 C#5:1 B4:1 C#5:1 F#5:1 A5:1 B5:1",
    "G5:1 F#5:1 E5:1 G5:1 F#5:1 E5:1 D5:1 C#5:1 B4:1 A4:1 G4:1 F#4:1 E4:1 G4:1 F#4:1 E4:1",
    "F#5:2 A5:2 E5:2 A5:2 D5:2 F#5:2 C#5:2 F#5:2",
    "B4:2 D5:2 A4:2 D5:2 B4:2 G5:2 C#5:2 E5:2",
    "A5:4 A5:4 F#5:4 F#5:4", "G5:4 F#5:4 G5:4 A5:4",
    "F#5:4 E5:4 D5:4 C#5:4", "B4:4 C#5:4 D5:8",
]))

# Clarinet / T.Sax: same canon line, written a M2 up (E major), entering 2 / 4 bars later
CANON_E = [
    "G#5:4 F#5:4 E5:4 D#5:4", "C#5:4 B4:4 C#5:4 D#5:4",
    "E5:4 D#5:4 C#5:4 B4:4", "A4:4 G#4:4 A4:4 F#4:4",
    "E5:2 G#5:2 B5:2 A5:2 G#5:2 E5:2 G#5:2 F#5:2",
    "E5:2 C#5:2 E5:2 B5:2 A5:2 C#6:2 B5:2 A5:2",
    "G#4:2 E4:2 F#4:2 D#5:2 E5:2 G#5:2 B5:2 B4:2",
    "C#5:2 A4:2 B4:2 G#4:2 E4:2 E5:2 E5:2 D#5:2",
    "B5:8 G#5:8", "E5:8 C#5:4 D#5:4",
    "E5:2 B4:2 D#5:2 F#5:2 E5:2 C#5:2 D#5:2 B4:2",
    "C#5:2 E5:2 B4:2 G#4:2 A4:2 C#5:2 B4:2 D#5:2",
    "E5:1 D#5:1 E5:1 E4:1 D#4:1 B4:1 F#4:1 G#4:1 E4:1 E5:1 D#5:1 C#5:1 D#5:1 G#5:1 B5:1 C#6:1",
    "A5:1 G#5:1 F#5:1 A5:1 G#5:1 F#5:1 E5:1 D#5:1 C#5:1 B4:1 A4:1 G#4:1 F#4:1 A4:1 G#4:1 F#4:1",
    "G#5:2 B5:2 F#5:2 B5:2 E5:2 G#5:2 D#5:2 G#5:2",
    "C#5:2 E5:2 B4:2 E5:2 C#5:2 A5:2 D#5:2 F#5:2",
]
CLARINET = bars(" | ".join([rep(R, 6)] + CANON_E + ["E5:4 D#5:4 C#5:4 B4:4", "A4:4 F#4:4 G#4:8"]))
TSAX = bars(" | ".join([rep(R, 8)] + CANON_E[:14] + ["B4:4 B4:4 G#4:4 G#4:4", "E5:4 D#5:4 B4:8"]))

HORN = bars(" | ".join(
    [rep(R, 2)]
    + ["E4:8 C#4:8 | A4:8 F#4:4 G#4:4"] * 4
    + ["E4:4 E4:4 C#4:4 C#4:4 | A4:4 A4:4 F#4:4 G#4:4"] * 4
    + ["C#5:4 B4:4 A4:4 G#4:4", "F#4:4 E4:4 F#4:4 G#4:4",
       "A4:4 G#4:4 F#4:4 E4:4", "D4:4 C#4:4 D4:4 B3:4",
       "E4:4 E4:4 F#4:4 E4:4", "F#4:4 G#4:4 A4:8"]))

TROMBONE = bars(" | ".join(
    ["D3:4 A2:4 B2:4 F#2:4 | G2:4 D3:4 G2:4 A2:4"] * 8
    + ["D3:2 D3:2 A2:2 A2:2 B2:2 B2:2 F#2:2 F#2:2 | G2:2 G2:2 D3:2 D3:2 G2:2 G2:2 A2:2 A2:2"] * 3
    + ["D3:4 A2:4 B2:4 F#2:4", "G2:4 A2:4 D3:8"]))

# NEW: Trumpet in Bb (written = concert + M2, E major).
# 1-4 tacet / 5-18 inner harmony, one dynamic step under the horn /
# C (19-22) long-note lyrical melody at mf under the f tutti / D cadence.
TRUMPET = bars(" | ".join(
    [rep(R, 4)]
    + ["G#4:4 F#4:4 G#4:8 | A4:4 G#4:4 A4:4 F#4:4"] * 3          # 5-10  (concert F#4 E4 F#4 | G4 F#4 G4 E4)
    + ["G#4:4 F#4:4 G#4:4 G#4:4 | A4:4 G#4:4 A4:4 F#4:4"] * 4    # 11-18
    + ["B4:8 G#4:8",                 # 19  concert A4 F#4
       "E5:8 C#5:4 D#5:4",           # 20  concert D5 B4 C#5
       "E5:4 D#5:4 C#5:4 B4:4",      # 21  concert D5 C#5 B4 A4
       "C#5:4 B4:4 C#5:4 D#5:4",     # 22  concert B4 A4 B4 C#5
       "B4:8 G#4:8",                 # 23  concert A4 F#4
       "C#5:4 D#5:4 B4:8"]))         # 24  concert B4 C#5 A4

PARTS = {
    "flute": dict(name="Flute", abbr="Fl.", music=FLUTE, fifths=2, clef=("G", 2),
                  sound="wind.flutes.flute", dyn={5: "mp", 13: "p", 15: "mp", 17: "mf", 19: "f", 23: "mf"}),
    "clarinet": dict(name="Clarinet in B♭", abbr="Cl.", music=CLARINET, fifths=4, clef=("G", 2),
                     transpose=(-1, -2, 0), sound="wind.reed.clarinet.bflat",
                     dyn={7: "mp", 15: "p", 17: "mp", 19: "f", 23: "mf"}),
    "tenor_sax": dict(name="Tenor Saxophone", abbr="T. Sax.", music=TSAX, fifths=4, clef=("G", 2),
                      transpose=(-1, -2, -1), sound="wind.reed.saxophone.tenor",
                      dyn={9: "mp", 17: "mp", 19: "f", 23: "mf"}),
    "horn": dict(name="Horn in F", abbr="Hn.", music=HORN, fifths=3, clef=("G", 2),
                 transpose=(-4, -7, 0), sound="brass.french-horn",
                 dyn={3: "p", 11: "mp", 17: "mf", 19: "f", 23: "mf"}),
    "trumpet": dict(name="Trumpet in B♭", abbr="Tpt.", music=TRUMPET, fifths=4, clef=("G", 2),
                    transpose=(-1, -2, 0), sound="brass.trumpet.bflat",
                    dyn={5: "pp", 11: "p", 17: "mp", 19: "mf", 23: "mf"}),
    "trombone": dict(name="Trombone", abbr="Tbn.", music=TROMBONE, fifths=2, clef=("F", 4),
                     sound="brass.trombone", dyn={1: "p", 5: "mp", 11: "mp", 17: "mf", 19: "f", 23: "mf"}),
}
REHEARSAL = {5: "A", 11: "B", 19: "C", 23: "D"}
TYPES = {16: ("whole", 0), 8: ("half", 0), 4: ("quarter", 0), 2: ("eighth", 0), 1: ("16th", 0), 12: ("half", 1)}
# rit. in bar 23-24: per-beat playback tempo, fitted to the original MP3 note onsets
# (bar 23 beats 0.96/0.98/1.02/1.04 s, bar 24 beats 1.18/1.22 s, final fermata half ~6.0 s)
RIT = {(23, 0): 62.5, (23, 4): 61.2, (23, 8): 58.8, (23, 12): 57.7, (24, 0): 50.8, (24, 4): 49.2, (24, 8): 41.7}


def note_xml(p, d, fermata=False):
    t, dots = TYPES[d]
    if p == "r":
        whole = ' measure="yes"' if d == 16 else ""
        return f"<note><rest{whole}/><duration>{d}</duration><voice>1</voice>" + \
               ("" if d == 16 else f"<type>{t}</type>") + "</note>"
    step, rest = p[0], p[1:]
    alter = 0
    while rest and rest[0] in "#b":
        alter += 1 if rest[0] == "#" else -1
        rest = rest[1:]
    x = f"<note><pitch><step>{step}</step>" + (f"<alter>{alter}</alter>" if alter else "") + \
        f"<octave>{rest}</octave></pitch><duration>{d}</duration><voice>1</voice><type>{t}</type>" + \
        "<dot/>" * dots
    if fermata:
        x += '<notations><fermata type="upright"/></notations>'
    return x + "</note>"


def direction(inner, placement="above", sound=""):
    return f'<direction placement="{placement}"><direction-type>{inner}</direction-type>{sound}</direction>'


def part_xml(pid, key, systems, pages, top):
    P = PARTS[key]
    out = [f'<part id="{pid}">']
    for i, m in enumerate(P["music"], start=1):
        out.append(f'<measure number="{i}">')
        if i in pages:
            out.append('<print new-page="yes"/>')
        elif i in systems:
            out.append('<print new-system="yes"/>')
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
                out.append(direction('<metronome parentheses="no"><beat-unit>quarter</beat-unit>'
                                     '<per-minute>66</per-minute></metronome>', sound='<sound tempo="66"/>'))
        if top and i in REHEARSAL:
            out.append(direction(f'<rehearsal enclosure="square">{REHEARSAL[i]}</rehearsal>'))
        if i == 23 and top:
            out.append(direction("<words>rit.</words>"))
        if i in P["dyn"]:
            out.append(direction(f'<dynamics><{P["dyn"][i]}/></dynamics>', "below"))
        pos = 0
        for j, (p, d) in enumerate(m):
            if top and (i, pos) in RIT:
                out.append(f'<direction><direction-type><words print-object="no"> </words></direction-type>'
                           f'<offset>0</offset><sound tempo="{RIT[(i, pos)]}"/></direction>')
            last = i == len(P["music"]) and j == len(m) - 1
            out.append(note_xml(p, d, fermata=last))
            pos += d
        if i == len(P["music"]):
            out.append('<barline location="right"><bar-style>light-heavy</bar-style></barline>')
        out.append("</measure>")
    out.append("</part>")
    return "\n".join(out)


def score_xml(keys, systems, pages):
    head = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" '
            '"http://www.musicxml.org/dtds/partwise.dtd">',
            '<score-partwise version="4.0">',
            "<work><work-title>Canon in D</work-title></work>",
            '<identification><creator type="composer">Johann Pachelbel</creator></identification>',
            '<credit page="1"><credit-type>title</credit-type><credit-words justify="center" valign="top" '
            'default-x="595" default-y="1600" font-size="22">Canon in D</credit-words></credit>',
            '<credit page="1"><credit-type>composer</credit-type><credit-words justify="right" valign="top" '
            'default-x="1100" default-y="1500" font-size="10">Johann Pachelbel</credit-words></credit>',
            "<part-list>"]
    for n, k in enumerate(keys, 1):
        P = PARTS[k]
        head.append(f'<score-part id="P{n}"><part-name>{escape(P["name"])}</part-name>'
                    f'<part-abbreviation>{escape(P["abbr"])}</part-abbreviation>'
                    f'<score-instrument id="P{n}-I1"><instrument-name>{escape(P["name"])}</instrument-name>'
                    f'<instrument-sound>{P["sound"]}</instrument-sound></score-instrument></score-part>')
    head.append("</part-list>")
    body = [part_xml(f"P{n}", k, systems, pages, top=(n == 1)) for n, k in enumerate(keys, 1)]
    return "\n".join(head + body + ["</score-partwise>"])


if __name__ == "__main__":
    outdir = sys.argv[1]
    # original full-score layout: 1-4 / 5-8 / 9-12 || 13-16 / 17-18 / 19-20 || 21-22 / 23-24
    full_sys, full_pages = {5, 9, 17, 19, 23}, {13, 21}
    # original part layout: 1-4 / 5-8 / 9-12 / 13-16 / 17-18 / 19-20 / 21-22 / 23-24
    part_sys = {5, 9, 13, 17, 19, 21, 23}
    quintet = ["flute", "clarinet", "tenor_sax", "horn", "trombone"]
    jobs = {
        # 원본 5중주 총보 재현 (기존 assets/canon_full_score.* 와 같은 결과)
        "canon_full_score": (quintet, full_sys, full_pages),
        # 6중주 (트럼펫 포함) — 줄이 늘어 쪽 나눔은 MuseScore 자동 배치
        "canon_full_score_trumpet": (quintet[:4] + ["trumpet", "trombone"], full_sys, set()),
    }
    for k in quintet + ["trumpet"]:
        jobs[f"canon_{k}"] = ([k], part_sys, set())
    for name, (keys, s, p) in jobs.items():
        with open(f"{outdir}/{name}.musicxml", "w") as f:
            f.write(score_xml(keys, s, p))
        print("wrote", name)
