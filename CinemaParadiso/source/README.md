# CinemaParadiso/source — 악보·음원 원본

엔니오 & 안드레아 모리꼬네 「Cinema Paradiso - Love Theme (시네마 천국 러브 테마)」 B♭ 클라리넷 솔로 편곡.
기보 다장조/가단조(조표 없음 · 콘서트 B♭장조/G단조), 4/4(브리지 2/4), ♩=66, 21마디, 약 1분 22초.

- `gen.py` — 선율(기보음)·슬러·테누토·셈여림·연습 기호·rit. 템포 → MusicXML. **악보 수정은 여기서.**
- `build.sh` — MuseScore 4 + ffmpeg로 `out/`에 mscz·pdf·png(150dpi)·mpos·mp3(192k) 생성.
- `publish.py` — `out/` → `CinemaParadiso/assets/` 복사 + `CinemaParadiso/manifest.json` 생성.
- `mpos2json.py` — `.mpos` → 마디별 시작 시각(ms)과 PNG 위 좌표(%).

다시 만들기 (저장소 루트에서):

```bash
bash CinemaParadiso/source/build.sh && python3 CinemaParadiso/source/publish.py
```
