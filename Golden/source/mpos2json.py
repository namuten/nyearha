import sys, re, json
# .mpos -> manifest "measures" (page %, for the 150-dpi PNG, A4 = 1240 x 1754 px)
# units: MuseScore 4 = 1/96 px of the 150-dpi PNG, MuseScore 3 = 1/24 px (told apart by page width)
PX_W, PX_H = 1240, 1754


def measures(path):
    t = open(path).read()
    els = {m[0]: m[1:] for m in re.findall(r'<element id="(\d+)" x="([\d.]+)" y="([\d.]+)" sx="([\d.]+)" sy="([\d.]+)" page="(\d+)"', t)}
    right = max(float(e[0]) + float(e[2]) for e in els.values())
    u = 96 if right > PX_W * 30 else 24
    out = []
    for eid, pos in re.findall(r'<event elid="(\d+)" position="(\d+)"', t):
        x, y, sx, sy, pg = els[eid]
        out.append(dict(ms=int(pos), page=int(pg), l=round(float(x) / u / PX_W * 100, 3),
                        t=round(float(y) / u / PX_H * 100, 3), w=round(float(sx) / u / PX_W * 100, 3),
                        h=round(float(sy) / u / PX_H * 100, 3)))
    return out


if __name__ == "__main__":
    print(json.dumps(measures(sys.argv[1])))
