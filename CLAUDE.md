# nyearha

GitHub Pages로 배포되는 개인 저장소 (https://namuten.github.io/nyearha/).
`main` 브랜치 루트가 자동 배포된다 — PR을 `main`에 머지하면 1~2분 뒤 반영 (브라우저 캐시 최대 10분, 안 보이면 ⌘⇧R).

## 구조 — 3개 영역은 서로 독립

| 영역 | 위치 | 내용 |
|---|---|---|
| 학습자료 | 루트 | 강동고 중간고사 대비: `범위.md`(고정 범위), `규칙.md`(STEP1~3 절차), `step*_*.md`, 대시보드 `index.html` |
| 캐논 | `canon/` | 파헬벨 캐논 관악 앙상블 악보 뷰어 |
| 리포트 | `data-report/` | 데이터 시각화 리포트 |

- 한 영역 작업 시 다른 영역 파일은 건드리지 않는다.
- `canon/` 안의 경로는 모두 폴더 내부 상대경로 (`../` 참조, 루트와 공유하는 CSS/JS 없음).

## Git 작업 방식

- `git commit` / `git push`는 사용자가 직접 실행 — Claude는 스테이징까지 하고 커밋 메시지를 제안한다.
- 작업은 `feature/`, `fix/`, `chore/` 브랜치에서 하고 PR → squash 머지.
- 커밋 메시지: `<type>(<scope>): <subject>` (예: `feat(canon): ...`).

---

## canon/

**Canon in D · 관악 앙상블** — arr. 남연하, Halloween 2026. 콘서트 D장조, 4/4, ♩=66, 24마디, 약 95초.

### 페이지
- `index.html` / `style.css` / `app.js` — 바닐라 JS. 왼쪽 메뉴, 악보 PNG, 오디오 플레이어.
  재생 시 현재 마디 표시, 마디 클릭 시 그 마디부터 재생, 스페이스 재생/정지, `#<id>` 딥링크.
- `manifest.json` — 메뉴 항목 목록. 항목마다 `pdf`, `mp3`, `pages`(PNG), `seconds`,
  `measures`(마디별 `ms` 시작 시간 + 악보 위 위치 `page/l/t/w/h` %).
- 메뉴 순서: 합주(총보) → 합주(트럼펫) → 플루트 · 클라리넷 · 테너 색소폰 · 호른 · 트롬본 → 트럼펫.
  id가 `full_score`로 시작하는 항목이 위쪽 합주 묶음 (구분선은 묶음 뒤에만).
- 첫 쪽 PNG의 원래 제목은 흰 상자로 덮고 안경 로고(`logo.png`) 오른쪽 렌즈 안에 제목을 다시 쓴다 (`.title-cover`, `.title-art`).
- `assets/canon_<id>.pdf|mp3`, `assets/png/canon_<id>-<쪽>.png` (A4, 150dpi = 1240×1754).
- 파트 MP3는 해당 악기 **솔로** 음원, 합주 MP3는 전체.

### 음악 구성
- 트롬본: 반복 베이스 D–A–B–F♯–G–D–G–A (2마디 단위, 처음부터 끝까지)
- 플루트 → 클라리넷 → 테너 색소폰: 2마디 간격 3성부 카논 (진입 5 / 7 / 9마디)
- 호른: 3마디부터 화음 보조. 연습 기호 A(5) B(11) C(19, f 클라이맥스) D(23, rit. · 늘임표)
- **트럼펫(B♭, 2026-11-04 추가)**: 1–4 쉼, 5–18 화음 보조(호른보다 한 단계 여리게 pp→p→mp),
  C(19–22) mf 긴 음 선율 — 사용자 요청: "C에서 멜로디 돋보이되 너무 튀지 않게", D 함께 마무리.
- 기보 조: 클라리넷·테너 색소폰·트럼펫 E장조(♯4), 호른 A장조(♯3), 플루트·트롬본 D장조.

### 악보·음원 원본 — `canon/source/`
- 기존 5중주 원본 `.mscz`(집 PC, MuseScore 4.7.5)는 저장소에 없었다 → 2026-11-04 PDF를 보고 `gen.py`로 다시 입력.
  다시 만든 결과가 기존 PNG와 **픽셀 단위로 동일**, 음원 길이·음량도 일치 (MuseScore 기본 음색).
- `gen.py` — 모든 파트의 음표(기보음)·셈여림·연습 기호·rit. 템포 정의 → MusicXML. **악보 수정은 여기서.**
- `build.sh` — MuseScore 4 + ffmpeg로 `out/`에 mscz·pdf·png·mpos·mp3(192k) 생성 (`out/`은 git 제외).
- `mpos2json.py` — `.mpos` → `manifest.json`의 `measures` (좌표 단위: 150dpi px × 96).
- `mscz/` — MuseScore 원본 8개. MuseScore 앱에서 직접 열어 편집해도 되지만, 그러면 `gen.py`와 내용이 달라지니 한쪽으로 통일할 것.

### 악보를 고치거나 파트를 추가할 때
1. `brew install --cask musescore` (MuseScore 4), ffmpeg 필요.
2. `canon/source/gen.py` 수정 → `bash canon/source/build.sh`.
3. `out/`에서 필요한 파일만 `canon/assets/`(PNG는 `assets/png/`)로 복사. **기존 파일은 요청 없이 덮어쓰지 않는다.**
4. `manifest.json`에 항목 추가 — `measures`는 `mpos2json.measures("out/<이름>.mpos")`로 생성, 기존 항목은 그대로.
5. 로컬 확인: `python3 -m http.server` 후 `/canon/` 열기.

### 집 PC에서 이어 작업 시
- 집 PC에 기존 원본 `.mscz`가 남아 있다면, `canon/source/mscz/canon_full_score.mscz`(재현본)와 내용이 같은지 확인만 하면 된다.
  이제 기준 원본은 `canon/source/`다.
- MuseScore 4.7.x 버전이면 같은 결과가 나온다 (4.7.5와 4.7.6 결과 동일 확인).
