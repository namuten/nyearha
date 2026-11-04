# canon/source

`canon/assets/`의 악보(PDF/PNG)와 음원(MP3)을 만드는 원본입니다.

- `gen.py` — 모든 파트의 음표·셈여림·연습 기호·rit. 템포를 담은 악보 정의 → MusicXML 생성
- `mscz/` — MuseScore 4 원본 파일 (기존 5중주 재현본 + 트럼펫 6중주 + 각 파트)
- `build.sh` — `gen.py` → MuseScore 4 → `out/`에 mscz·pdf·png(150dpi)·mpos·mp3(192k) 생성
- `mpos2json.py` — MuseScore `.mpos`를 `manifest.json`의 `measures` 좌표로 변환

## 다시 만들기

```bash
brew install --cask musescore   # MuseScore 4
bash canon/source/build.sh      # 결과: canon/source/out/
```

`out/`의 파일을 `canon/assets/`(png는 `assets/png/`)로 복사해 쓰고,
마디 좌표는 `python3 -c "from mpos2json import measures; ..."`로 `manifest.json`에 넣습니다.

## 참고

- 기존 5중주(2026-11-01, 집 PC MuseScore 4.7.5)의 원본 `.mscz`가 없어 PDF를 보고 다시 입력했습니다.
  MuseScore 4.7.6으로 빌드한 결과가 기존 PNG와 픽셀 단위로 같습니다.
- `canon/assets/`의 기존 5중주 파일은 원본 그대로이며, 이 폴더에서 다시 만든 것이 아닙니다.
