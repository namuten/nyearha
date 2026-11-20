# source

`assets/`의 악보(PDF/PNG)·음원(MP3)과 `manifest.json`을 만드는 원본입니다.

- `gen.py` — 선율(사용자가 준 클라리넷 악보에서 옮김)·구성 → MusicXML (악보 수정은 여기서)
- `build.sh` — `gen.py` → MuseScore → `out/`에 mscz·pdf·png(150dpi)·mpos·mp3(192k)
- `publish.py` — `out/` → `assets/` 복사, `manifest.json` 생성
- `mpos2json.py` — `.mpos` → 마디 좌표

## 다시 만들기

```bash
brew install --cask musescore   # MuseScore 4 (맥)
bash shampoo/source/build.sh
python3 shampoo/source/publish.py
```

리눅스에서는 `LANG=C.UTF-8 MSCORE=<mscore4 경로> bash shampoo/source/build.sh` (UTF-8 로캘이 아니면 한글 제목이 잘림).
