#!/usr/bin/env python3
"""Golden (HUNTR/X, KPop Demon Hunters, 2025) -- flute + B-flat clarinet call-and-response duet -> MusicXML.

Copyrighted song; published here by the user's decision (2026-11-13, rearranged 2026-11-16).
Melody: the user's G-major lead sheet (source/*.pdf, not committed), arranged in concert F major (clarinet written
G major) so flute (concert D4-G5) and clarinet (written E3-A4, below the break) trade the lead melody back and forth
like a vocal duet and unite at the climax and finale.

  bars  1-4   intro  (1-2 Cl. lead <-> 3-4 Fl. lead, 4b3-4 together)      mf -> cresc.
  bars  5-20  A  chorus 1 (4-bar trade: 5-8 Cl. <-> 9-12 Fl. <-> 13-16 Cl. <-> 17-20 Fl.)
  bars 21-36  B  chorus 2 climax (21-24 Fl. <-> 25-28 Cl. <-> 29-30 Fl. <-> 31-34 Cl.+Fl. -> 35-36 Duet)
  bars 37-44  C  ending (1-bar ping-pong: 37,39,41 Cl. <-> 38,40,42 Fl. -> 43-44 Duet, rit., fermata)

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
    "G4:12 B4:12 E5:12 D5:12",                 # came so far, now (G-B replaces D-G to stay >= written E3)
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
    "F#4:12 A4:12 E5:12 D5:12",                # now I'm shinin' (F#-A replaces D-F# to stay >= written E3)
    "G4:12 B4:12 A5:12 F#5:6 G5:6~",           # like I'm born to be.
    "G5:12 E5:12 r:12 F#4:12",                 # Oh,
    "E4:12 G4:12 C5:12 B4:12",                 # our time, no
    "F#4:12 A4:12 E5:12 D5:12",                # fears, no lies, that's
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
    "F#4:12 A4:12 E5:12 D5:12",                # fears, no lies, that's
    "G4:12 B4:12 A5:12 F#5:6 G5:6~",           # who we're born to
    "G5:36 E5:12",                             # be.
]
SHEET = INTRO + CHORUS + [TURN] + CHORUS + [LAST] + ENDING

# one chord per half bar, CONCERT F major (clarinet written G major)
INTRO_CH = "Bb Bb | F F | C C | C Dm"
CHORUS_CH = ("Bb Bb | C C | F F | Dm Dm | Bb Bb | C C | F F | Dm Dm | "
             "Bb Bb | C C | F F | Dm Dm | Bb Bb | C C | F F")
ENDING_CH = "C F | C C | C F | C C | Bb Bb | C C | F F | Bb Bb"
CHORDS = f"{INTRO_CH} | {CHORUS_CH} | Dm Dm | {CHORUS_CH} | Dm C | {ENDING_CH}"
CHART = [b.split() for b in CHORDS.split("|")]
assert len(CHART) == len(SHEET) == 44 and all(len(b) == 2 for b in CHART)

# Upper accompaniment voicings for flute (concert F major, G4-F5, always > clarinet melody D3-G4)
VOICE_FL = {
    "Bb": ("Bb4", "D5", "F5"),
    "F":  ("A4", "C5", "F5"),
    "C":  ("G4", "C5", "E5"),
    "Dm": ("A4", "D5", "F5"),
}
# Lower accompaniment voicings for clarinet (concert F major, D3-C4 = written E3-D4, always < flute melody D4-G5)
VOICE_CL = {
    "Bb": ("D3", "F3", "Bb3"),
    "F":  ("F3", "A3", "C4"),
    "C":  ("E3", "G3", "C4"),
    "Dm": ("D3", "F3", "A3"),
}

# Full reference melody in concert pitch: flute register (D4-G5) and clarinet register (D3-G4, 1 octave lower)
MEL_FL = [[(transpose(p, -1, -2), d, t) for p, d, t in m] for m in bars(SHEET)]
MEL_CL = [[(transpose(p, -8, -14), d, t) for p, d, t in m] for m in bars(SHEET)]

# Bars where each instrument takes the main melody (both play together on 35-36 and 43-44)
FLUTE_LEAD_BARS = {3, 4, 9, 10, 11, 12, 17, 18, 19, 20, 21, 22, 23, 24, 29, 30, 35, 36, 38, 40, 42, 43, 44}
CLARINET_LEAD_BARS = {1, 2, 5, 6, 7, 8, 13, 14, 15, 16, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 39, 41, 43, 44}


def flute():
    """Flute in CONCERT F major (D4-G5): alternates lead melody with clarinet and provides upper harmony/fills."""
    out = []
    for i, (c1, c2) in enumerate(CHART, start=1):
        lo1, mid1, hi1 = VOICE_FL[c1]
        lo2, mid2, hi2 = VOICE_FL[c2]
        if i == 38:
            # Ending ping-pong: flute plays the bar-38 triplets then adds a 2-beat answering motif
            out.append(MEL_FL[i - 1][:-1] + [("C5", Q, False), ("A4", Q, False)])
        elif i in FLUTE_LEAD_BARS:
            out.append(list(MEL_FL[i - 1]))
        elif i <= 2:
            # Intro bars 1-2: warm harmonic pad while clarinet opens
            out.append([(lo1, 2 * Q, False), (mid2, 2 * Q, False)])
        elif i in (6, 7):
            # Chorus A (bars 5-8, Cl. lead): quarter pulse on beats 1-2 filling Cl. eighth rest, half note under triplets
            out.append([(lo1, Q, False), (mid1, Q, False), (hi2, 2 * Q, False)])
        elif i == 8:
            out.append([(lo1, 2 * Q, False), (mid2, Q, False), (hi2, Q, False)])
        elif i == 16:
            # Answering obligato fill on beat 3 where clarinet rests
            out.append([(lo1, 2 * Q, False), (hi2, Q, False), (mid2, Q, False)])
        elif i <= 15:
            out.append([(lo1, 2 * Q, False), (mid2, 2 * Q, False)])
        elif i == 25:
            # Climax B (bars 25-28, Cl. lead): upper harmony on "Up, up, up with our"
            out.append([("Bb4", Q, False), ("D5", Q, False), ("G5", Q, False), ("F5", Q, False)])
        elif i == 31:
            # Climax B ("like I'm born to be"): 3rd/6th upper harmony above clarinet lead, tied to bar 32
            out.append([("A4", Q, False), ("C5", Q, False), ("D5", Q, False), ("C5", 6, False), ("A4", 6, True)])
        elif i == 32:
            out.append([("A4", Q, False), ("F4", Q, False), ("D5", Q, False), ("A4", Q, False)])
        elif 26 <= i <= 34:
            # Climax B driving quarter-note arpeggios while clarinet leads
            out.append([(lo1, Q, False), (mid1, Q, False), (hi1, Q, False), (mid1, Q, False)])
        else:
            # Ending C odd bars (37, 39, 41) while clarinet leads
            out.append([(lo1, 2 * Q, False), (mid2, 2 * Q, False)])
    return out


def clarinet():
    """Clarinet in CONCERT pitch (D3-G4, written E3-A4): alternates lead melody with flute and supports underneath."""
    out = []
    for i, (c1, c2) in enumerate(CHART, start=1):
        lo1, mid1, hi1 = VOICE_CL[c1]
        lo2, mid2, hi2 = VOICE_CL[c2]
        if i in CLARINET_LEAD_BARS:
            out.append(list(MEL_CL[i - 1]))
        elif i == 3:
            # Intro bar 3 (Fl. lead): warm low half notes
            out.append([(lo1, 2 * Q, False), (mid2, 2 * Q, False)])
        elif i == 4:
            # Intro bar 4: half note on beats 1-2, then joins flute on "We're goin'" pickup into bar 5
            out.append([(lo1, 2 * Q, False)] + list(MEL_CL[3][1:]))
        elif i in (10, 11):
            # Chorus A (bars 9-12, Fl. lead): quarter pulse on beats 1-2 filling Fl. eighth rest, half note under triplets
            out.append([(lo1, Q, False), (mid1, Q, False), (hi2, 2 * Q, False)])
        elif i in (12, 20):
            out.append([(lo1, 2 * Q, False), (mid2, Q, False), (hi2, Q, False)])
        elif i <= 19:
            out.append([(lo1, 2 * Q, False), (mid2, 2 * Q, False)])
        elif 21 <= i <= 30:
            # Climax B (bars 21-24, 29-30, Fl. lead): driving quarter-note arpeggios
            if c1 == c2:
                out.append([(lo1, Q, False), (mid1, Q, False), (hi1, Q, False), (mid1, Q, False)])
            else:
                out.append([(VOICE_CL[c][k], Q, False) for c in (c1, c2) for k in (0, 1)])
        elif i == 40:
            # Ending bar 40: supports flute triplets on beats 1-2, then joins pickup "You know that" into bar 41
            out.append([(lo1, 2 * Q, False)] + list(MEL_CL[39][6:]))
        else:
            # Ending C even bars (38, 42) while flute leads
            out.append([(lo1, 2 * Q, False), (mid2, 2 * Q, False)])
    return out


def written(music):
    """Concert -> B-flat clarinet (major 2nd up, written G major E3-A4)."""
    return [[(transpose(p, 1, 2), d, t) for p, d, t in m] for m in music]


DYN_FL = {1: "p", 3: "mf", 5: "mp", 9: "f", 13: "mp", 17: "f", 21: "f", 25: "mf", 29: "f", 31: "mf", 35: "f"}
DYN_CL = {1: "mf", 3: "mp", 5: "f", 9: "mp", 13: "f", 17: "mp", 21: "mf", 25: "f", 29: "mf", 31: "f"}
PARTS = {
    "flute": dict(name="Flute", abbr="Fl.", music=flute(), fifths=-1,
                  sound="wind.flutes.flute", dyn=DYN_FL),
    "clarinet": dict(name="Clarinet in B♭", abbr="Cl.", music=written(clarinet()), fifths=1,
                     transpose=(-1, -2), sound="wind.reed.clarinet.bflat", dyn=DYN_CL),
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
