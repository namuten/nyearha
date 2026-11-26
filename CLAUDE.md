# nyearha

GitHub Pages로 배포되는 개인 저장소 (https://namuten.github.io/nyearha/).
`main` 브랜치 루트가 자동 배포된다 — PR을 `main`에 머지하면 1~2분 뒤 반영 (브라우저 캐시 최대 10분, 안 보이면 ⌘⇧R).

## 구조 — 메인 페이지 + 서로 독립된 영역

| 영역 | 위치 | 내용 |
|---|---|---|
| 메인 | 루트 `index.html` | 각 영역으로 들어가는 시작 페이지 (단일 파일, CSS·JS 인라인) |
| 캐논 | `canon/` | 파헬벨 캐논 관악 앙상블 악보 뷰어 |
| 대부 | `Godfather/` | 마스카니 간주곡(대부 3편) 플루트·클라리넷 3중주 악보 뷰어 — canon과 같은 구조 |
| You Raise Me Up | `YouRaiseMeUp/` | 「You Raise Me Up」 후렴 플루트·클라리넷 2중주 악보 뷰어 — canon과 같은 구조 |
| Golden | `Golden/` | HUNTR/X 「Golden」 플루트·클라리넷 2중주 악보 뷰어 — canon과 같은 구조 |
| 그대 안의 블루 | `Blue/` | 김현철·이소라 「그대 안의 블루」 플루트·클라리넷 2중주 악보 뷰어 — canon과 같은 구조 |
| 교가 | `RiverLight/` | 강빛초중 이음학교 교가 플루트 2·클라리넷·트롬본 4중주 악보 뷰어 — canon과 같은 구조 |
| 샴푸향 | `shampoo/` | 장범준 「흔들리는 꽃들 속에서 네 샴푸향이 느껴진거야」 클라리넷 솔로 악보 뷰어 — canon과 같은 구조 |
| 시네마 천국 | `CinemaParadiso/` | 엔니오 모리꼬네 「Cinema Paradiso - Love Theme」 클라리넷 솔로 악보 뷰어 — canon과 같은 구조 |
| 손가락 연습 | `practice/` | 악보·운지 다이어그램·타임라인 동기화 연습 화면 (현재 `Blue` 플루트·클라리넷, `CinemaParadiso` 클라리넷 적용) |
| 학습자료 | `study/` | 강동고 중간고사 대비: `범위.md`(고정 범위), `규칙.md`(STEP1~3 절차), `step*_*.md`, 대시보드 `index.html` |
| 리포트 | `data-report/` | 데이터 시각화 리포트 |
| (기타) | 루트 `travel_plan.html` | 강원도 가족여행 — 어디에도 링크 안 됨, 주소로만 접근 |

- 한 영역 작업 시 다른 영역 파일은 건드리지 않는다.
- **메인 페이지 구성**: I. Repertoire(악보, 큰 카드, 계속 추가됨) → II. Game(`GAMES` 배열, 악보와 같은 카드) → III. Archive & Notes(학습자료·리포트, 작은 칩).
  새 악보 폴더를 만들면 루트 `index.html`의 `SCORES` 배열에 한 줄 추가한다 (`href`, `icon`, `title`, `sub`, `meta`).
  - Game은 별도 저장소 `namuten/goofyfish`(Astro, 같은 GitHub Pages 계정)로, 절대 URL `https://namuten.github.io/goofyfish/`로 연결한다.
- 각 영역 페이지 맨 위에 메인으로 가는 `<a class="home-link" href="../">← 메인</a>`이 있다 (영역 밖을 가리키는 유일한 `../`).
  새 악보 페이지도 canon처럼 사이드바 `.brand` 맨 위에 넣는다.
- `canon/`, `Godfather/`, `YouRaiseMeUp/`, `Golden/`, `Blue/`, `RiverLight/`, `shampoo/` 안의 경로는 모두 폴더 내부 상대경로 (`../` 참조, 루트와 공유하는 CSS/JS 없음).
  - **예외**: 악보 페이지 왼쪽 메뉴의 연습 링크(`../practice/#<piece>_<part>`)와, `practice/`가 각 악보 폴더의 `assets/`(MP3, 악보 PNG), `logo.png`, `pattern.svg`, `manifest.json`을 **읽기 전용**으로 참조하는 것만 허용한다.

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

---

## Godfather/

**Intermezzo · 플루트·클라리넷 3중주** — P. Mascagni 「Cavalleria rusticana」 간주곡 (대부 3편 마지막 장면 음악).
퍼블릭 도메인. 콘서트 F장조, 3/4, ♩=60, 34마디, 약 1분 51초 (요청: 2분 이내).

- 대부 메인 테마(Nino Rota, "Speak Softly Love")는 저작권이 살아 있어 사용하지 않고, 이 곡으로 대신함 (2026-11-12 사용자 선택).
- 페이지(`index.html`/`style.css`/`app.js`/`logo.png`/`pattern.svg`)는 canon 것을 복사해 제목만 바꿈. 동작 동일.
- 메뉴: 합주(총보) → 플루트 → 클라리넷 1 → 클라리넷 2. 파일 `assets/godfather_<id>.pdf|mp3`, `assets/png/godfather_<id>-<쪽>.png`.

### 음악 구성
- 선율: flutetunes.com(id 401, 퍼블릭 도메인 플루트 악보) MIDI 기준. 2분 안에 맞추려고 원본 1–11 / 20–31 / 32–38·43–46마디만 사용.
  - 1–11 도입 주제 (p) · A(12–23) 찬송가풍 주제 (mp, 22 cresc.) · B(24–34) 클라이맥스 (f) → 33 rit., 34 늘임표
- 플루트: 주선율 전체.
- 클라리넷 1: 1–23 긴 음 안쪽 화음, B(24–)부터 플루트 선율을 한 옥타브 아래로.
- 클라리넷 2: 분산화음 반주 (1–23 4분음표, B부터 8분음표).
- 화음은 `gen.py`의 `CHORDS`(박마다 하나)에서 클라리넷 파트를 자동 생성. 기보 조: 클라리넷 G장조(♯1), 플루트 F장조.

### 악보·음원 원본 — `Godfather/source/`
- `gen.py` — 선율(콘서트음)·화음표·셈여림 → MusicXML. **악보 수정은 여기서.**
- `build.sh` — canon과 같음 (`MSCORE` 환경변수로 MuseScore 경로 변경 가능).
- `publish.py` — `out/` → `assets/` 복사 + `manifest.json` 생성 (마디 좌표 포함).
- `mpos2json.py` — MuseScore 4(1/96 px)·3(1/24 px) `.mpos` 둘 다 처리.
- 현재 assets는 맥 MuseScore 4로 빌드한 결과 (2026-11-12, 약 1분 51초). canon과 음색·글꼴 동일.
  다시 만들기: `bash Godfather/source/build.sh && python3 Godfather/source/publish.py`
  `.title-cover` 위치는 canon과 같은 값 (MuseScore 4 제목 위치 기준).

---

## YouRaiseMeUp/

**You Raise Me Up · 플루트·클라리넷 2중주 (후렴 주고받기·듀엣 편곡)** — Rolf Løvland 작곡 (2002).
콘서트 F장조 (클라리넷 기보 G장조), 4/4, ♩=66, 17마디, 약 1분 11초. 고등학생 연주자용 (쉽게).

- **저작권이 살아 있는 곡** — 공개 사이트 게시 위험을 알고 사용자가 그대로 공개하기로 결정 (2026-11-13).
- 처음엔 24마디 전곡(기억으로 입력한 선율)이었으나 원곡처럼 안 들려서, 사용자가 준 G장조 리드시트(`source/*.gif`, 커밋 안 함)의
  **후렴만** 두 번 반복하는 구성으로 바꿈 (2026-11-13). 이후 두 악기가 `"You raise me..."` 못갖춘마디 픽업부터 2마디 악구 단위로 주선율을 번갈아 주고받고 마지막 악구에서 함께 마무리하도록 **콘서트 F장조(클라리넷 기보 G장조)**로 재편곡 (2026-11-16).
- 페이지는 Godfather 것을 복사해 제목만 바꿈. 제목이 길어 `.title-cover`를 넓히고(left 34.5%, width 31%) 렌즈 안 제목을 두 줄로 씀.
- 메뉴: 합주(총보) → 플루트 → 클라리넷. 파일 `assets/youraisemeup_<id>.pdf|mp3`, `assets/png/youraisemeup_<id>-<쪽>.png`.

### 음악 구성
- **1 도입 + A(2–9) 후렴 1회**(2마디 악구 단위 교대, mf):
  - 1마디 3박(`"You raise me"`)~3마디 2박(`"mountains."`): **클라리넷 주선율**(mf) + 플루트 2분음표 화음 반주(p).
  - 3마디 3박(`"You raise me"`)~5마디 2박(`"seas."`): **플루트 주선율**(mf) + 클라리넷 2분음표 화음 반주(mp).
  - 5마디 4박(`"I am"`)~7마디 2박(`"shoulders."`): **클라리넷 주선율**(mf) + 플루트 2분음표 화음 반주(mp).
  - 7마디 3박(`"You raise me"`)~9마디 2박(`"be."`): **플루트 주선율**(mf) + 클라리넷 2분음표 화음 반주(mp).
- **B(10–17) 후렴 2회 클라이맥스**(교대 후 옥타브 합주, f → 16 rit., 17 늘임표):
  - 9마디 3박~11마디 2박(`"mountains."`): **클라리넷 주선율**(f) + 플루트 4분음표 분산화음 반주(mf).
  - 11마디 3박~13마디 2박(`"seas."`): **플루트 주선율**(f) + 클라리넷 4분음표 분산화음 반주(mf).
  - 13마디 4박~15마디 2박(`"shoulders."`): **클라리넷 주선율**(f) + 플루트 4분음표 분산화음 반주(mf).
  - 15마디 3박~17마디(`"You raise me up, to more than I can be."`): **플루트 + 클라리넷 옥타브 동시 주선율**(f → 16 rit., 17 늘임표).
- 음역 및 규칙: 플루트 콘서트 F장조(♭1) `E4`–`G5`, 클라리넷 기보 G장조(♯1) `E3`–`A4`(브레이크 아래). 붙임줄·16분음표·조표 밖 임시표·박을 가로지르는 당김음 없음. `source/test_gen.py`가 검사한다.

### 악보·음원 원본 — `YouRaiseMeUp/source/`
- 구성은 Godfather와 같음: `gen.py`(악보 수정은 여기서, 후렴은 `CHORUS`) · `build.sh` · `publish.py` · `mpos2json.py` · `test_gen.py`.
- 다시 만들기: `python3 -m unittest discover -s YouRaiseMeUp/source && bash YouRaiseMeUp/source/build.sh && python3 YouRaiseMeUp/source/publish.py`

---

## Golden/

**Golden · 플루트·클라리넷 2중주 (주선율 교대·듀엣 편곡)** — HUNTR/X (케이팝 데몬 헌터스, 2025). EJAE, Mark Sonnenblick, IDO, 24, TEDDY 작곡.
콘서트 F장조 (클라리넷 기보 G장조), 4/4, ♩=120, 44마디, 약 1분 35초. 초급~중급.

- **저작권이 살아 있는 곡** — You Raise Me Up과 같이 공개 게시하기로 함 (2026-11-13).
- 선율 원본: 사용자가 준 G장조 멜로디 악보 `source/HUNTRIX - Golden (원곡).pdf`(81마디, 커밋 안 함).
  두 악기가 주선율을 균형 있게 주고받고 클라이맥스에서 함께 연주하도록 **콘서트 F장조(클라리넷 기보 G장조)**로 편곡 (2026-11-16).
- 페이지는 Godfather 것을 복사해 제목만 바꿈 (`.title-cover`도 Godfather 값).
- 메뉴: 합주(총보) → 플루트 → 클라리넷. 파일 `assets/golden_<id>.pdf|mp3`, `assets/png/golden_<id>-<쪽>.png`.

### 음악 구성
- **1–4 도입**(원본 21–24, 2마디씩 교대): **1–2마디 클라리넷 선율**(mf) ↔ **3–4마디 플루트 선율**(mf, 4마디 후반 `"We're goin'"` 함께 진입하며 cresc.).
- **A(5–20) 후렴 1회**(원본 25–40, 4마디씩 대화형 주고받기):
  - **5–8마디(`"Up, up, up, it's our moment ... golden"`)**: **클라리넷 주선율**(f) + 플루트 반주(mp).
  - **9–12마디(`"Up, up, up with our voices ... golden"`)**: **플루트 주선율**(f) + 클라리넷 반주(mp).
  - **13–16마디(`"I'm done hidin' ... born to be"`)**: **클라리넷 주선율**(f) + 플루트 반주(mp).
  - **17–20마디(`"Our time, no fears, no lies ... We're goin'"`)**: **플루트 주선율**(f) + 클라리넷 반주(mp).
- **B(21–36) 후렴 2회 클라이맥스**(원본 58–73, 교대 후 클라이맥스 합주):
  - **21–24마디**: **플루트 주선율**(f) + 클라리넷 4분음표 분산화음 반주(mf).
  - **25–28마디**: **클라리넷 주선율**(f) + 플루트 4분음표 분산화음 반주(mf).
  - **29–30마디**: **플루트 주선율**(f) ↔ **31–34마디**: **클라리넷 주선율**(f, 31–32마디 플루트 3도/6도 화음) → **35–36마디**: **두 악기 옥타브 동시 주선율**(f).
- **C(37–44) 마무리**(원본 74–81, 1마디 핑퐁 교대 → 피날레 합주, 43 rit., 44 늘임표):
  - **37–40마디**: **클라리넷**(37·39마디)과 **플루트**(38·40마디)가 1마디씩 `"gonna be, gonna be"` 셋잇단 훅을 주고받음.
  - **41–42마디**: **클라리넷**(41마디 `"it's our time, no"`) ↔ **플루트**(42마디 `"fears, no lies, that's"`) 교대.
  - **43–44마디**: 마지막 `"who we're born to be"`를 두 악기가 함께 연주하며 늘임표로 마무리.
- 음역: 클라리넷 기보 G장조(♯1) `E3`–`A4`(브레이크 아래), 플루트 콘서트 F장조(♭1) `D4`–`G5`. 전 구간 성부 교차 없이 플루트가 위쪽 성부 유지.

### 악보·음원 원본 — `Golden/source/`
- 구성은 YouRaiseMeUp과 같음: `gen.py` · `build.sh` · `publish.py` · `mpos2json.py` · `test_gen.py`.
- 다시 만들기: `python3 -m unittest discover -s Golden/source && bash Golden/source/build.sh && python3 Golden/source/publish.py`

---

## Blue/

**그대 안의 블루 · 플루트·클라리넷 2중주 (남녀 보컬 주고받기·듀엣 편곡)** — 김현철 작곡, 이현승 작사, 이소라·김현철 노래 (1992).
4/4, ♩=70 (원곡 악보 Slow Go Go ♩=60), 24마디, 약 1분 32초. 초급~중급, 재즈 분위기.

- **저작권이 살아 있는 곡** — You Raise Me Up·Golden과 같이 공개 게시하기로 함 (2026-11-13).
- 선율 원본: 사용자가 준 리드시트 `source/김현철,이소라-그대안의블루.jpg`(커밋 안 함). 1절+후렴 그대로, 조도 악보대로
  (1–9 F장조, 10부터 B♭장조). 원곡 남녀 보컬(김현철·이소라) 듀엣처럼 클라리넷과 플루트가 소절마다 주선율을 주고받고 마지막 구절에서 옥타브로 함께 부르도록 재편곡 (2026-11-16).
- 페이지는 Golden 것을 복사해 제목만 바꿈 (`.title-cover`도 Golden 값, 렌즈 안 제목은 두 줄).
- 메뉴: 합주(총보) → (구분선) → 플루트 · 클라리넷 → (구분선) → 플루트 연습 · 클라리넷 연습. 파일 `assets/blue_<id>.pdf|mp3`, `assets/png/blue_<id>-<쪽>.png`.

### 음악 구성
- **1–4 전주**(B♭M7–C7): 클라리넷·플루트 재즈 화음 위 **3–4마디 플루트 인트로 선율**(mp) ↔ 4마디 후반 클라리넷 워킹 연결.
- **A(5–9) 1절**(F장조): **5~7마디 3박 클라리넷 주선율**(`"난 난 눈을 감아요, 빛과 그대 모습 사라져"`, mf) ↔ **7마디 4박~9마디 플루트 주선율**(`"이제 어둠이 밀려오네"`, mf).
- **B(10–15) 브리지**(B♭장조): **10–12마디 플루트 주선율**(`"저 파란 어둠 속에서 그대 왜 잠들어 가나"`, mf) ↔ **13~15마디 3박 클라리넷 주선율**(`"세상은 아직 그대 곁에 있는데"`, mf) → 15마디 4박 플루트 후렴 픽업(`"사-"`, f).
- **C(16–24) 후렴 클라이맥스**(f → 23 rit., 24 늘임표):
  - **16–17마디**: **플루트 주선율**(`"사랑은 아니지만 우리의 만남"`) + 클라리넷 4분음표 재즈 워킹.
  - **18~19마디 3박**: **클라리넷 주선율**(`"어둠은 사라지네"`) + 플루트 화음 반주 → 19마디 4박 플루트 픽업(`"오 시간"`).
  - **20–21마디**: **플루트 주선율**(`"시간은 빛으로 물들어 또 다시"`) + 클라리넷 4분음표 재즈 워킹.
  - **22–24마디**: 22마디 1–3박 **클라리넷**(`"흐르네"`) → **22마디 4박~24마디 플루트+클라리넷 옥타브 동시 주선율**(`"내 눈빛 속 그대"`, 23 rit., 24 늘임표).
- 음역: 플루트 콘서트 `D4`–`B♭5`, 클라리넷 기보 `E3`–`G4`(브레이크 아래, G장조→C장조). `practice/`의 검증된 운지표(`clarinet.json`, `flute.json`) 음역 안에서 전 구간 연주된다.

### 악보·음원 원본 — `Blue/source/`
- 구성은 Golden과 같음: `gen.py` · `build.sh` · `publish.py` · `mpos2json.py` · `test_gen.py`. 선율은 콘서트음으로 적음.
- 다시 만들기: `python3 -m unittest discover -s Blue/source && bash Blue/source/build.sh && python3 Blue/source/publish.py`

---

## RiverLight/

**River Light · 강빛초중 이음학교 교가** — 작곡 홍경서, 작사 임채현·안정민. 플루트 2 · B♭ 클라리넷 · 트롬본 4중주.
콘서트 G장조, 4/4, ♩=128, 53마디, 약 1분 46초. 학교 교가라 인터넷 악보가 없어 사용자가 보낸 악보 사진(원곡 33마디, 커밋 안 함)을 옮겨 적음 (2026-11-20).

- 페이지는 Godfather 것을 복사해 제목만 바꿈 (`.title-cover`도 Godfather 값).
- 메뉴: 합주(총보) → 플루트 1 → 플루트 2 → 클라리넷 → 트롬본. 파일 `assets/riverlight_<id>.pdf|mp3`, `assets/png/riverlight_<id>-<쪽>.png`.

### 편곡 구성
- 1–4 도입(원곡 29–32, mf) · A 5–20 1절(원곡 1–16, mp) · B 21–36 2절(원곡 1–16, p → 36 cresc.) · C 37–53 후렴(원곡 17–33, f) → 52 rit., 53 늘임표
- 플루트 1: 도입·1절·후렴 선율을 한 옥타브 위로 (원곡은 B3까지 내려가 플루트로 못 붊). 2절은 긴 음 화음.
- 플루트 2: 선율 아래 3·4·6도 화음(같은 리듬), 2절은 긴 음 화음.
- 클라리넷: 도입·1절 긴 음 안쪽 화음, 2절·후렴은 원곡 높이 선율 (후렴은 플루트 1과 옥타브).
- 트롬본: 근음 베이스 (도입·1절 2분음표 근음–5음, 2절·후렴 4분음표 근음–5음).
- 화음은 `gen.py`의 `CHORDS`(원곡 코드 기호, 박마다 하나)에서 자동 생성. 기보 조: 클라리넷 A장조(♯3), 나머지 G장조.

### 악보·음원 원본 — `RiverLight/source/`
- `gen.py`(원곡 선율 `SONG`·코드표 `CHORDS`·편곡 구성 `FORM`) · `build.sh` · `publish.py` · `mpos2json.py` — Godfather와 같은 구조.
- 다시 만들기: `bash RiverLight/source/build.sh && python3 RiverLight/source/publish.py`
- 현재 assets는 리눅스 MuseScore 4.7.5 AppImage로 빌드 (2026-11-20). 리눅스에서는 **`LANG=C.UTF-8`** 필수 — 아니면 MusicXML의 한글(작곡자·부제)이 일부 잘림.

---

## shampoo/

**흔들리는 꽃들 속에서 네 샴푸향이 느껴진거야 · 클라리넷 솔로 (하이라이트 편곡)** — 장범준 (2019). B♭ 클라리넷 1명.
기보 G장조 (♯1, 콘서트 F장조), 4/4, ♩=94 (Andantino con moto, dolce e espressivo), 26마디, 약 1분 13초.

- **저작권이 살아 있는 곡** — 다른 대중가요 곡들과 같이 공개 게시 (2026-11-20).
- 안의 파일 이름은 `shampoo_` 접두어로 영문.
- 선율 원본: 브런치 전체악보(`https://brunch.co.kr/@mymars/883`, G장조 3쪽). 브런치 악보의 기보 **G장조(♯1, 음역 `D3`–`B4`)**와 당김음 이음줄·Stop-time 브레이크·브리지(`C`, `B7–Em7` 및 `AmM7`)에서 반복 구간을 덜어내고 **가장 임팩트 있는 핵심 훅(타이틀 도입 → 상승 프리코러스 → 메인 후렴 → `AmM7` 브리지 → 피날레)**만 26마디(약 1분 13초)로 압축해 재편곡 (2026-11-20).
- 페이지는 RiverLight 것을 복사해 제목만 바꿈. 제목이 길어 `.title-cover`를 넓히고(left 31.5%, width 37%) 렌즈 안 제목을 두 줄·작은 글씨로 씀.
- 메뉴: 클라리넷 하나. 파일 `assets/shampoo_clarinet.pdf|mp3`, `assets/png/shampoo_clarinet-1.png`.

### 음악 구성 (26마디, 무반복 하이라이트)
- **1–2 전주(Intro, mp)**: 원곡 인트로 코드(`G – D/F# – Em7 | CM7 – D7sus4 – G ① Stop-time`)를 2마디로 압축한 아르페지오 오프닝 & Stop-time 브레이크.
- **A(3–10) 타이틀 훅 + 상승 프리코러스(3–6 mp cantabile → 7–10 mf cresc. & Stop-time)**:
  - **3–6마디**: `"흔들리는 꽃들 속에서 네 샴푸향이 느껴진 거야"` (깊고 따뜻한 샬뤼모 저음역 `A3`–`E4` + `Bm7` 저음 아르페지오 에코).
  - **7–10마디**: 벌스 반복 없이 곧바로 `"한번 연락해 볼까 용기 내 보지만 그냥 내 마음만 아쉬운 거야"`로 고조된 뒤 10마디 `① Stop-time` 및 `"걷다가 보면"` 픽업.
- **B(11–18) 메인 후렴(f espressivo)**: `"항상 이렇게 너를 바라만 보던 너를 기다린다고 말할까 / 지금 집 앞에 계속 이렇게 너를 아쉬워하다 너를 연락했다 할까"`.
- **C(19–26) 감성 브리지 하이라이트 & 피날레 코다(19 mp dolce → 21 mf cresc. → 24 f appassionato → 25 rit. e dim. → 26 mp 늘임표)**:
  - **19–23마디**: `"어떤 계절이 너를(`B7–Em7`) 바라만 보던 너를 기다리면서(`AmM7`, `G#4–A4–B4`) 아무말 못하고 그리워만 할까"` + 23마디 `① Stop-time` `"걷다가 보면"`.
  - **24–26마디**: 마지막 후렴 핵심 훅(`"항상 이렇게 너를 연락했다 할까"`, `rit. e dim.`) 후 26마디 따뜻한 샬뤼모 저음 `G`장조 아르페지오(`D3–G3–B3`) 페르마타 마무리.

### 악보·음원 원본 — `shampoo/source/`
- `gen.py`(선율 `MELODY`) · `build.sh` · `publish.py` · `mpos2json.py` — Godfather와 같은 구조.
- 다시 만들기: `bash shampoo/source/build.sh && python3 shampoo/source/publish.py`
- 현재 assets는 맥 MuseScore 4로 빌드 (2026-11-20).

---

## CinemaParadiso/

**Cinema Paradiso (Love Theme) · 클라리넷 솔로 (고등학생 연주자용 멜로디 편곡)** — Ennio & Andrea Morricone (1988). B♭ 클라리넷 1명.
기보 다장조/가단조 (♯0/♭0, 콘서트 B♭장조/G단조), 4/4(브리지 2/4), ♩=66 (Andante cantabile, dolce), 21마디, 약 1분 22초.

- 선율 원본: 사용자가 준 피아노 악보 `source/시네마천국 - 러브테마 악보.pdf`(콘서트 B♭장조/G단조 3쪽, 40마디, 커밋 안 함).
- 원본 PDF의 벡터 음표 좌표를 추출해 **원곡 주선율을 음정·리듬 변형 없이 100% 그대로** 수록하고, 고등학생 연주자가 쉽게 연주할 수 있도록 전 구간을 **클라리넷 레지스터 브레이크(`B4`) 아래의 편안한 음역(`E3`–`A4`, 기보 다장조/가단조 조표 없음 · 콘서트 B♭장조/G단조 원키 그대로)**으로 배치 (2026-11-20).
- 메뉴: 클라리넷 하나. 파일 `assets/cinema_clarinet.pdf|mp3`, `assets/png/cinema_clarinet-1.png`.

### 음악 구성 (21마디, 브레이크 아래 `E3`–`A4`)
- **1 도입(Intro, mp)**: 원곡 1마디 호흡(`D4:12- r:4`).
- **A(2–10) 전반부 주선율(mp dolce e cantabile → 7 mf → 8 mp)**:
  - `Gm–Cm7 | F–B♭ | 2/4 B♭maj7 | Gm–B♭/F | E♭maj7–Cm7 | Am7♭5–D7♭9 | Gm–Gm7/F | E♭maj7–Edim | D7sus4–D7` 반종지까지 원곡 선율을 그대로 제시.
- **B(11–21) 후반부 주선율(mf espressivo → 16 f appassionato → 20 rit. e dim. → 21 p 늘임표)**:
  - 후반부 주선율을 한 단계 풍부한 셈여림(`mf` → `f`)으로 노래한 뒤 정격종지(`E♭maj7–Edim | B♭/F–F | E♭/B♭–B♭ | B♭maj7`) 페르마타로 마무리.
- 음역 및 난이도: 기보 다장조/가단조(조표 없음) `E3`–`A4` (전 구간 레지스터 브레이크 아래). 임시표는 원곡 선율의 반음 보조음 `G#3`(6·15마디) 1개뿐.

### 악보·음원 원본 — `CinemaParadiso/source/`
- `gen.py`(선율 `MELODY`) · `build.sh` · `publish.py` · `mpos2json.py` — shampoo와 같은 구조.
- 다시 만들기: `bash CinemaParadiso/source/build.sh && python3 CinemaParadiso/source/publish.py`
- 현재 assets는 맥 MuseScore 4로 빌드 (2026-11-20).

---

## practice/ (손가락 연습)

악보 읽기가 어렵거나 운지를 익혀야 하는 연주자를 위해 **악보 진행 + 실시간 악기 운지 다이어그램 + 흘러오는 음 타임라인 + 배속/구간반복/카운트인**을 한 화면에서 제공하는 선택형 연습 영역.
- 설계 명세: `docs/superpowers/specs/2026-11-13-clarinet-practice-design.md`
- 구현 계획 및 진행 기록: `docs/superpowers/plans/2026-11-13-clarinet-practice.md`

### 현재 완료 상태 (2026-11-16, PR #8 `main` 머지 완료)
- **적용 범위**: `Blue` (그대 안의 블루) **플루트 연습(`#blue_flute`)** · **클라리넷 연습(`#blue_clarinet`)**, `CinemaParadiso` **클라리넷 연습(`#cinema_clarinet`)** (2026-11-26).
- **곡 추가 시**: `extract.py`의 `PIECES`, `practice/app.js`의 `PIECE_INFO`(사이드바 제목·부제·곡 정보)와 렌즈 제목(`titleArtHtml`, 긴 제목은 `.wide`/`.wider`), 악보 페이지 메뉴의 연습 링크.
- **박자표 변화**: 데이터의 `measureBeats`(마디별 박 수)로 예비박·박 길이를 계산 (시네마 천국 2/4 마디).
- **확정된 UI·레이아웃 규칙 (사용자 피드백 반영 완료 — 다른 곡 확장 시 그대로 유지할 것)**:
  1. **왼쪽 사이드바 메뉴 통합 (`.sidebar`, 폭 260px)**:
     - 기존 악보 페이지(`Blue/`)와 `practice/` 양쪽 모두 동일한 왼쪽 메뉴 구조를 가진다.
     - 메뉴 순서: `합주 (총보)` → *(구분선 `.menu li.full + li:not(.full)`)* → `플루트` · `클라리넷` → *(구분선 `.menu li:not(.practice) + li.practice`)* → `플루트 연습` · `클라리넷 연습`.
  2. **메인 상단 (`.piece-head` + `.top-deck`)**:
     - `.piece-head`: 기존 악보 뷰어와 동일한 위치·크기로 파트 연습 제목(`클라리넷 연습` / `플루트 연습`), 설명(`B♭ · 화음 반주` / `주선율`), 우측 `↓ 악보 PDF` · `↓ MP3` 다운로드 버튼 배치.
     - `.top-deck`: 상단 고정 전폭 **흘러오는 음 타임라인(`.timeline`)** (과거 1초·미래 4초, 마디선 번호 및 음 길이 블록 표시).
  3. **메인 하단 2단 작업 영역 (`.workspace`)**:
     - **좌측 (`.score-panel`)**: 파트 악보 PNG(`pages`) + 첫 페이지 상단 안경 로고 및 제목 오버레이(`.title-cover`, `.title-art`, 반드시 `position: absolute` 유지) + 현재 마디 박스(`.marker`, 마디 번호 배지) + 마디 내 진행률 채움(`.marker-fill`) 및 세로 진행 커서(`.marker-head`). 줄 변경 시 자동 스크롤, 마디 클릭 시 해당 마디 시작 위치로 즉시 이동.
     - **우측 (`.right-col`)**:
       - 상단 **운지 카드(`.finger-panel`)**: 카드 내부 **왼쪽**에 악기 정면 SVG(`.fingering`, 높이 `min(64vh, 620px)`), **오른쪽**에 지금/다음 계이름·기보음·운지 변경 안내(`.info`).
       - 중단 **플레이어(`.player`)**: 1줄에 재생/정지 버튼·시크바·시간, 2줄(`.opts`)에 속도(`0.5` / `0.75` / `1.0x`)·구간 반복(시작~끝 마디, 켜기/끄기)·카운트인(예비박 켜기/끄기).
       - 하단 **안내 문구(`.hint`)**: 단축키 및 키 색상 설명.

### 파일 구조 및 파이프라인
- `practice/index.html`, `practice/style.css`, `practice/app.js` — 연습 화면 프론트엔드 (바닐라 JS ES module).
- `practice/core.js`, `practice/core.test.mjs` — 순수 로직 (`noteIndexAt`, `nextPlayedIndex`, `keyChanges`, `solfege`, `loopBounds`, `beatMs`, `measureProgress`) 및 단위 테스트.
- `practice/instruments/clarinet.json`, `practice/instruments/clarinet.svg` — B♭ 클라리넷(뵘식, 기보음 기준) 운지표 및 SVG 다이어그램 (`E3`–`A4` 16개 음 검증 완료, `G#3`·`A4`는 2026-11-26 추가).
- `practice/instruments/flute.json`, `practice/instruments/flute.svg` — C 플루트(뵘식, 콘서트음 기준) 운지표 및 SVG 다이어그램 (`D4`–`Bb5` 15개 음 검증 완료).
  - **운지 작성 원칙**: 기억/추측 금지. 공개된 표준 운지표 2곳(`wfg.woodwind.org`, `phys.unsw.edu.au`)을 교차 대조하여 일치하면 `"verified": true`와 `"src": ["wfg", "unsw"]`를 기록한다.
- `practice/source/extract.py`, `practice/source/test_extract.py` — 각 곡의 `<Folder>/source/gen.py` → MusicXML → MuseScore 4 CLI(`.spos`, `.mpos`) + `<Folder>/manifest.json` 대조 → `practice/data/<piece>_<part>.json` 및 `practice/pieces.json` 생성.
  - 재생성 및 테스트 명령어:
    ```bash
    python3 practice/source/extract.py
    python3 -m unittest discover -s practice/source -v
    bun test practice/core.test.mjs   # 또는 node --test practice/core.test.mjs
    ```

### 다음 작업 (나머지 4곡 확장 시 할 일)
1. **운지표 음역 추가 (`instruments/clarinet.json`, `instruments/flute.json`)**:
   - `canon`, `Godfather`(클라 1·2, 플루트), `YouRaiseMeUp`, `Golden`에서 추가로 쓰이는 음(클라리넷 클라리온 음역 `A4`–`C#6`, 플루트 고음역 `B5`–`D6` 등)을 WFG + UNSW 2곳 대조 후 각 JSON에 추가 (`test_extract.py`의 `test_fingering_covers_every_used_pitch`가 누락된 음 목록을 정확히 출력함).
2. **`practice/source/extract.py`의 `PIECES` 확장**:
   - `PIECES` 리스트에 `canon`, `Godfather`, `YouRaiseMeUp`, `Golden`(, `shampoo`)의 플루트·클라리넷 파트 추가 (`canon`은 `canon/source/gen.py` 실행 방식에 맞게 경로 처리) 후 `python3 practice/source/extract.py` 실행.
3. **나머지 4곡 악보 페이지 왼쪽 메뉴 연결**:
   - `Blue/app.js`·`Blue/style.css`와 동일하게 `canon/`, `Godfather/`, `YouRaiseMeUp/`, `Golden/`의 `style.css`에 `.menu li:not(.practice) + li.practice` 구분선 규칙을 넣고 `app.js`의 `#menu` 하단에 `<li class="practice">` 연습 링크 추가.
   - `practice/style.css`의 `.main` 배경 패턴이나 타이틀 아트가 곡별로 맞게 동작하는지 확인 (`youraisemeup`은 `.title-cover.wide` 이미 지원됨).
   - 루트 `index.html`의 `OTHERS` 배열에 `practice/` 진입 칩 추가 여부 확인.
