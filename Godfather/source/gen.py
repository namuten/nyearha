#!/usr/bin/env python3
"""Intermezzo (Cavalleria rusticana, P. Mascagni) -- flute + 2 B-flat clarinets -> MusicXML.

The Godfather Part III closing-scene music. Public domain (Mascagni, d. 1945).
Concert F major, 3/4, quarter = 60, 34 bars, about 1:50.

Melody follows the public-domain flute version (flutetunes.com, id 401), cut to fit under 2 minutes:
  bars  1-11  opening theme          (source bars 1-11)
  bars 12-23  A  hymn theme          (source bars 20-31)
  bars 24-34  B  climax + ending     (source bars 32-38, 43-46)
Accompaniment (clarinets) is generated from the per-beat chord chart below.

All pitches here are CONCERT pitch; clarinet parts are written a major 2nd higher (G major).
Durations are in 16ths (one 3/4 bar = 12). A trailing "~" ties the note into the next one.
"""
import sys
from xml.sax.saxutils import escape

BAR = 12
TEMPO = 60


# ---------------------------------------------------------------- notation
def bars(s):
    """'F5:4 A5:4 C6:4 | C6:6 ...' -> [[('F5',4,False), ...], ...]"""
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


# ---------------------------------------------------------------- melody (flute, concert)
MELODY = [
    # --- opening theme (source 1-11)
    "F5:4 A5:4 C6:4",
    "C6:6 Bb5:2 A5:2 G5:2",
    "D6:2 F5:2 A5:8",
    "G5:4 A5:8~",
    "A5:2 F5:2 E5:2 D5:2 D6:3 B5:1",
    "C6:8 Bb5:3 D5:1",
    "A5:4 G5:4 Bb5:1 C6:1 Bb5:1 F5:1",
    "A5:6 G5:2 F5:2 D6:2~",
    "D6:2 C6:2 B5:2 A5:2 G5:2 F5:2",
    "F5:1 E5:1 G5:1 A4:1 E5:6 D5:2",
    "C5:12",
    # --- A: hymn theme (source 20-31)
    "A5:8 C6:4",
    "F5:8 A5:4",
    "D5:4 D6:2 C6:2 Bb5:2 F5:2",
    "A5:8 G5:4",
    "Bb5:8 D5:4",
    "A5:4 C6:4 F5:4",
    "A5:8 G5:4",
    "F5:12",
    "D6:4 D6:2 C6:2 Bb5:2 F5:2",
    "A5:8 G5:4",
    "Bb5:4 Bb5:2 A5:2 G5:2 D5:2",
    "F5:8 E5:4",
    # --- B: climax + ending (source 32-38, 43-46)
    "F5:4 G5:2 A5:2 Bb5:1 C6:1 D6:1 E6:1",
    "F6:6 F6:2 E6:2 D6:2",
    "A5:4 C6:4 E5:4",
    "F5:6 F6:2 F6:2 F6:2",
    "F6:6 F6:2 F6:2 F6:2",
    "F6:6 F6:2 E6:2 D6:2",
    "A5:4 C6:4 E5:4",
    "F5:6 E5:2 F5:2 G5:2",
    "A5:6 F5:2 A5:2 D6:2",
    "D6:6 Bb5:2 D6:2 F6:2",
    "A6:12",
]

# one chord per beat (3 per bar)
CHORDS = """
F F F | C7 C7 C7 | Dm Dm Dm | F F F | G7 G7 G7 | C7 C7 C7 | F F C7 | Dm Dm Dm | G7 G7 G7 | C C C | C C C |
F F F | Dm Dm Dm | Bb Bb Bb | F F C7 | Gm Gm Gm | F F F | F F C7 | F F F | Bb Bb Bb | F F C7 | Gm Gm Gm | Bb Bb C7 |
F F C7 | F F F | F F C7 | F F F | Bb Bb Bb | Dm Dm Bb | F F C7 | F F F | F F Dm | Bb Bb C7 | F F F
"""
CHART = [b.split() for b in CHORDS.split("|")]
assert len(CHART) == len(MELODY) == 34 and all(len(b) == 3 for b in CHART)

# clarinet 2 voicings (concert): bass, middle, top  -- lowest clarinet concert note is D3
VOICE = {
    "F": ("F3", "C4", "A4"), "Dm": ("D3", "A3", "F4"), "Bb": ("D3", "Bb3", "F4"),
    "Gm": ("G3", "D4", "Bb4"), "C": ("E3", "C4", "G4"), "C7": ("E3", "Bb3", "G4"),
    "G7": ("G3", "B3", "F4"),
}
TONES = {  # chord tones for clarinet 1 inner voice
    "F": "F A C", "Dm": "D F A", "Bb": "Bb D F", "Gm": "G Bb D", "C": "C E G", "C7": "C E G Bb", "G7": "G B D F",
}
SEMI = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def midi(p):
    step, rest = p[0], p[1:]
    alt = 0
    while rest and rest[0] in "#b":
        alt += 1 if rest[0] == "#" else -1
        rest = rest[1:]
    return 12 * (int(rest) + 1) + SEMI[step] + alt


def name_of(pc_name, octave):
    return f"{pc_name}{octave}"


def inner_tone(chord, mel_pitch, prev):
    """Pick a chord tone in F4..C5 for clarinet 1: below the melody, not doubling it, close to prev."""
    cands = []
    for t in TONES[chord].split():
        for o in (3, 4, 5):
            p = name_of(t, o)
            m = midi(p)
            if midi("E4") <= m <= midi("C5") and m < mel_pitch - 2 and m % 12 != mel_pitch % 12:
                cands.append(p)
    if not cands:
        cands = [name_of(TONES[chord].split()[0], 4)]
    return min(cands, key=lambda p: (abs(midi(p) - midi(prev)), midi(p)))


def melody_bars():
    return bars(" | ".join(MELODY))


def clarinet1():
    """Bars 1-23: sustained inner voice. Bars 24-34: the melody an octave lower."""
    mel = melody_bars()
    out, prev = [], "A4"
    for i, (chords, m) in enumerate(zip(CHART, mel), start=1):
        if i >= 24:
            out.append([(f"{p[:-1]}{int(p[-1]) - 1}", d, t) for p, d, t in m])
            continue
        # group equal consecutive chords into one long note
        groups = []
        for c in chords:
            if groups and groups[-1][0] == c:
                groups[-1][1] += 4
            else:
                groups.append([c, 4])
        bar, pos = [], 0
        for c, d in groups:
            mp = sounding_at(m, pos)
            prev = inner_tone(c, mp, prev)
            if bar and bar[-1][0] == prev:  # same tone across a chord change: hold it
                bar[-1] = (prev, bar[-1][1] + d, False)
            else:
                bar.append((prev, d, False))
            pos += d
        out.append(bar)
    # intro colour: bar 1 enters after the downbeat is set by clarinet 2
    out[0] = [("r", 4, False), (out[0][0][0], 8, False)]
    return out


def sounding_at(m, pos):
    t = 0
    for p, d, _ in m:
        if t <= pos < t + d:
            return midi(p)
        t += d
    return midi(m[-1][0])


def clarinet2():
    """Bars 1-23: quarter-note arpeggio (bass-middle-top). Bars 24-33: eighths. Last bar: bass note."""
    out = []
    for i, chords in enumerate(CHART, start=1):
        if i == len(CHART):
            out.append([(VOICE[chords[0]][0], 12, False)])
        elif i < 24:
            out.append([(VOICE[c][k], 4, False) for k, c in enumerate(chords)])
        else:
            b = []
            for k, c in enumerate(chords):
                bass, mid, top = VOICE[c]
                b += [(bass if k == 0 else top, 2, False), (mid, 2, False)]
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
    "flute": dict(name="Flute", abbr="Fl.", music=melody_bars(), fifths=-1, clef=("G", 2),
                  sound="wind.flutes.flute", dyn={1: "p", 12: "mp", 24: "f"}),
    "clarinet_1": dict(name="Clarinet in B♭ 1", abbr="Cl. 1", music=written(clarinet1()), fifths=1,
                       clef=("G", 2), transpose=(-1, -2, 0), sound="wind.reed.clarinet.bflat",
                       dyn={1: "pp", 12: "p", 24: "f"}),
    "clarinet_2": dict(name="Clarinet in B♭ 2", abbr="Cl. 2", music=written(clarinet2()), fifths=1,
                       clef=("G", 2), transpose=(-1, -2, 0), sound="wind.reed.clarinet.bflat",
                       dyn={1: "p", 12: "p", 24: "mf"}),
}
REHEARSAL = {12: "A", 24: "B"}
WORDS = {22: "cresc.", 33: "rit."}
TYPES = {12: ("half", 1), 8: ("half", 0), 6: ("quarter", 1), 4: ("quarter", 0),
         3: ("eighth", 1), 2: ("eighth", 0), 1: ("16th", 0)}
# rit. over the last two bars (per-beat playback tempo), final bar held under a fermata
RIT = {(33, 0): 56, (33, 4): 52, (33, 8): 48, (34, 0): 42}


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
            a += f"<key><fifths>{P['fifths']}</fifths></key><time><beats>3</beats><beat-type>4</beat-type></time>"
            a += f"<clef><sign>{P['clef'][0]}</sign><line>{P['clef'][1]}</line></clef>"
            if "transpose" in P:
                dia, chro, octc = P["transpose"]
                a += f"<transpose><diatonic>{dia}</diatonic><chromatic>{chro}</chromatic>"
                a += (f"<octave-change>{octc}</octave-change>" if octc else "") + "</transpose>"
            out.append(a + "</attributes>")
            if top:
                out.append(direction('<words font-weight="bold">Andante sostenuto</words>'))
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


TITLE, COMPOSER = "Intermezzo", "Pietro Mascagni"


def score_xml(keys):
    head = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" '
            '"http://www.musicxml.org/dtds/partwise.dtd">',
            '<score-partwise version="4.0">',
            f"<work><work-title>{TITLE}</work-title></work>",
            f"<movement-title>{TITLE}</movement-title>",
            f'<identification><creator type="composer">{COMPOSER}</creator>'
            f'<creator type="lyricist">from "Cavalleria rusticana"</creator></identification>',
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
    trio = ["flute", "clarinet_1", "clarinet_2"]
    jobs = {"godfather_full_score": trio}
    for k in trio:
        jobs[f"godfather_{k}"] = [k]
    for name, keys in jobs.items():
        with open(f"{outdir}/{name}.musicxml", "w") as f:
            f.write(score_xml(keys))
        print("wrote", name)
