#!/usr/bin/env python3
"""out/ -> <이 폴더>/assets/ + <이 폴더>/manifest.json  (run after build.sh)

사용: python3 <이 폴더>/source/publish.py
"""
import glob, json, os, shutil, subprocess, sys

S = os.path.dirname(os.path.abspath(__file__))
G = os.path.dirname(S)
OUT = os.path.join(S, "out")
sys.path.insert(0, S)
from mpos2json import measures  # noqa: E402

ITEMS = [  # id, 메뉴 이름, 설명
    ("clarinet", "클라리넷", "B♭ 솔로 · 기보 C장조/A단조(콘서트 B♭장조/G단조)"),
]

os.makedirs(os.path.join(G, "assets", "png"), exist_ok=True)
manifest = []
for pid, label, desc in ITEMS:
    n = f"cinema_{pid}"
    for ext in ("pdf", "mp3"):
        shutil.copy(os.path.join(OUT, f"{n}.{ext}"), os.path.join(G, "assets", f"{n}.{ext}"))
    pages = []
    for p in sorted(glob.glob(os.path.join(OUT, f"{n}-*.png"))):
        shutil.copy(p, os.path.join(G, "assets", "png", os.path.basename(p)))
        pages.append(f"assets/png/{os.path.basename(p)}")
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", os.path.join(OUT, f"{n}.mp3")]))
    manifest.append(dict(id=pid, label=label, desc=desc, pdf=f"assets/{n}.pdf", mp3=f"assets/{n}.mp3",
                         pages=pages, seconds=round(dur), measures=measures(os.path.join(OUT, f"{n}.mpos"))))
    print(f"{n}: {dur:.1f}s, {len(pages)} page(s), {len(manifest[-1]['measures'])} measures")

with open(os.path.join(G, "manifest.json"), "w") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
