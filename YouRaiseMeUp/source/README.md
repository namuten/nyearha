# YouRaiseMeUp/source

`YouRaiseMeUp/assets/`의 악보(PDF/PNG)·음원(MP3)과 `manifest.json`을 만드는 원본입니다.

- `gen.py` — 선율·화음표·셈여림 → MusicXML (악보 수정은 여기서)
- `build.sh` — `gen.py` → MuseScore → `out/`에 mscz·pdf·png(150dpi)·mpos·mp3(192k)
- `publish.py` — `out/` → `assets/` 복사, `manifest.json` 생성
- `mpos2json.py` — `.mpos` → 마디 좌표

## 다시 만들기

```bash
brew install --cask musescore   # MuseScore 4 (맥)
bash YouRaiseMeUp/source/build.sh
python3 YouRaiseMeUp/source/publish.py
```

리눅스에서는 `MSCORE=/usr/bin/mscore3 QT_QPA_PLATFORM=offscreen bash YouRaiseMeUp/source/build.sh`.
