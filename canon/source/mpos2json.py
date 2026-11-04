import sys, re, json
# mpos coords are in 1/96 px of the 150-dpi PNG (A4 = 1240 x 1754 px)
W, H = 1240 * 96, 1754 * 96
def measures(path):
    t = open(path).read()
    els = {m[0]: m[1:] for m in re.findall(r'<element id="(\d+)" x="([\d.]+)" y="([\d.]+)" sx="([\d.]+)" sy="([\d.]+)" page="(\d+)"', t)}
    out = []
    for eid, pos in re.findall(r'<event elid="(\d+)" position="(\d+)"', t):
        x, y, sx, sy, pg = els[eid]
        out.append(dict(ms=int(pos), page=int(pg), l=round(float(x) / W * 100, 3), t=round(float(y) / H * 100, 3),
                        w=round(float(sx) / W * 100, 3), h=round(float(sy) / H * 100, 3)))
    return out
if __name__ == "__main__":
    print(json.dumps(measures(sys.argv[1])))
