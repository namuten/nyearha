# You Raise Me Up 2중주 페이지 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 「You Raise Me Up」 플루트·클라리넷 초보용 2중주 악보 뷰어 `YouRaiseMeUp/`를 만들어 메인 허브에 연결한다.

**Architecture:** `Godfather/`를 그대로 본뜬다. `source/gen.py`(선율 + 반 마디 단위 화음표 → MusicXML) → `build.sh`(MuseScore 4 + ffmpeg → `out/`) → `publish.py`(`out/` → `assets/` + `manifest.json`). 페이지 `index.html`/`style.css`/`app.js`/`logo.png`/`pattern.svg`는 Godfather 것을 복사해 제목만 바꾼다.

**Tech Stack:** Python 3 표준 라이브러리(unittest), MuseScore 4 (`/Applications/MuseScore 4.app`), ffmpeg/ffprobe, 바닐라 HTML/JS.

**Spec:** `docs/superpowers/specs/2026-11-13-youraisemeup-design.md`

## Global Constraints

- 폴더 `YouRaiseMeUp/` (대소문자 그대로 — GitHub Pages는 대소문자 구분). 파일 접두사 `youraisemeup_`.
- 콘서트 B♭장조, 4/4, ♩=66, 24마디, 전조 없음. 목표 길이 약 1분 30초 (85–95초 허용).
- 구성: 1–2 도입(p) · A(3–10) 1절(mp) · B(11–18) 후렴(mf) · C(19–24) 클라이맥스(f) → 23–24 rit., 마지막 음 늘임표.
- 리듬: 온음표·점2분·2분·4분음표, 8분음표는 박 위에서 시작하는 짝으로만. 붙임줄·당김음·16분음표·임시표 없음.
- 음역: 플루트 콘서트 F4–B♭5. 클라리넷 기보 E3–G4 (= 콘서트 D3–F4), 기보 C장조 조표 없음.
- 편성·메뉴: 합주(총보) → 플루트 → 클라리넷. id `full_score`, `flute`, `clarinet`.
- `../`는 `home-link` 하나뿐. 다른 영역 파일은 손대지 않음 (루트 `index.html` `SCORES` 한 줄, `CLAUDE.md` 예외).
- `git commit`/`push`는 사용자가 직접 — 각 Task 끝은 스테이징 + 커밋 메시지 제안.

## Review Focus

1. 첫 쪽 제목 "You Raise Me Up"이 "Intermezzo"보다 길다 → `.title-art span`의 렌즈 안에 한 줄로 들어가야 하고, `.title-cover`가 MuseScore 원래 제목을 다 덮어야 한다. (Task 3 Step 3에서 PNG로 확인)
2. 선율을 기억으로 입력 → 원곡과 다른 음. 사용자가 첫 MP3를 듣고 고칠 수 있게 `gen.py`의 `MELODY`가 마디별 한 줄이어야 한다. (Task 1 구조)
3. 클라리넷 반주가 플루트 선율과 같은 음(유니즌)으로 겹치거나 F4 위로 올라가는 경우 — 테스트로 막는다. (Task 1 `test_clarinet_*`)
4. rit. 때문에 MP3 길이가 목표를 벗어남 → 빌드 후 길이 확인. (Task 2 Step 3)
5. 허브 링크 `YouRaiseMeUp/` 대소문자 오타 → 404. (Task 3 Step 4)

---

### Task 1: `gen.py` — 악보 정의와 MusicXML 생성 (+ 초보 규칙 테스트)

**Files:**
- Create: `YouRaiseMeUp/source/gen.py` (Godfather `gen.py`를 복사해 수정)
- Create: `YouRaiseMeUp/source/test_gen.py`

**Interfaces:**
- Produces: `gen.py`에 `BAR = 16`, `TEMPO = 66`, `melody_bars() -> list[list[(pitch:str, dur:int, tie:bool)]]`, `clarinet() -> 같은 형식(콘서트음)`, `written(music)`, `PARTS = {"flute": ..., "clarinet": ...}`, `midi(p) -> int`, CLI `python3 gen.py <outdir>` → `youraisemeup_full_score.musicxml`, `youraisemeup_flute.musicxml`, `youraisemeup_clarinet.musicxml`.

- [ ] **Step 1: 실패하는 테스트 작성** — `test_gen.py` (unittest, `sys.path`에 자기 폴더 추가 후 `import gen`):

```python
ALLOWED = {16, 12, 8, 4, 2}
BFLAT_MAJOR_PCS = {10, 0, 2, 3, 5, 7, 9}

def test_shape():            # 24마디, 마디마다 합 16
    assert len(gen.melody_bars()) == 24 and len(gen.clarinet()) == 24
def test_rhythms():          # 두 파트 모두 길이 ∈ ALLOWED, tie 없음,
                             # 8분음표(2)는 시작 위치 % 4 == 0 이고 바로 다음도 2
def test_flute_range():      # 쉼표 제외 midi('F4') <= midi(p) <= midi('Bb5')
def test_no_accidentals():   # 플루트·클라리넷 콘서트음 pc ∈ BFLAT_MAJOR_PCS;
                             # written(clarinet())의 모든 음에 '#'/'b' 없음
def test_clarinet_range():   # 쉼표 제외 midi('D3') <= midi(p) <= midi('F4') (콘서트)
def test_clarinet_below_melody():  # 같은 시점 울리는 클라리넷 음 < 플루트 음 (쉼표 제외)
def test_clarinet_rhythm_by_section():  # 1–10마디: 길이 ∈ {16,12,8}; 11–23마디: ∈ {8,4}; 24마디: 16 한 음
def test_musicxml_written(tmp):    # main을 tmpdir로 실행 → 3개 파일 생성, full_score에 <part id="P2">,
                                    # flute에 <fifths>-2</fifths>, clarinet에 <fifths>0</fifths>,
                                    # <transpose><diatonic>-1</diatonic><chromatic>-2</chromatic>,
                                    # <per-minute>66</per-minute>, <fermata, <beats>4</beats>
```

- [ ] **Step 2: 실패 확인** — `python3 -m unittest discover -s YouRaiseMeUp/source -v` → ImportError/FAIL.

- [ ] **Step 3: `gen.py` 구현** — Godfather `gen.py`에서 바꿀 것만:
  - 모듈 docstring: 곡·작곡가(Rolf Løvland, 2002, 저작권 유효 — 사용자 결정으로 공개), B♭ 4/4 ♩=66 24마디, 콘서트음 기준.
  - `BAR = 16`, `TEMPO = 66`, `TYPES`에 `16: ("whole", 0)` 추가, `<beats>4</beats>`.
  - `MELODY`: 24줄(마디당 한 줄, 섹션 주석 `# --- intro/A/B/C`). 원곡 E♭ 선율을 B♭로 옮겨(완전 4도 아래) 플루트 F4–B♭5에 맞추고, 원곡 당김음·붙임줄은 앞 박으로 당긴 4분/2분음표로 단순화. 1–2마디 도입은 후렴 첫 프레이즈 앞부분을 온음표/2분음표로. 24마디는 B♭ 온음표.
  - `CHORDS`: 반 마디에 하나 (마디당 2개, 같은 코드 연속 가능), 쓸 수 있는 코드 `Bb Eb F F7 Gm Cm Dm`. `assert len(CHART)==24 and all(len(b)==2 ...)`.
  - `VOICE` (콘서트, D3–F4 안): `Bb:(D3,F3,Bb3)`, `Eb:(Eb3,G3,Bb3)`, `F:(F3,A3,C4)`, `F7:(F3,A3,Eb4)`, `Gm:(D3,G3,Bb3)`, `Cm:(Eb3,G3,C4)`, `Dm:(D3,F3,A3)`.
  - `clarinet()`: 1–10마디 — 같은 코드가 이어지는 반 마디를 합쳐 온음표/2분음표, 음은 `VOICE`의 bass. 11–23마디 — 반 마디마다 4분음표 `bass, mid`(같은 코드가 마디 전체면 `bass, mid, top, mid`도 가능); 플루트보다 낮지 않으면 한 단계 낮은 음으로. 24마디 — `Bb` bass 온음표.
  - `clarinet1/clarinet2/inner_tone` 삭제. `PARTS`: `flute` (`fifths=-2`, `dyn={1:"p",3:"mp",11:"mf",19:"f"}`), `clarinet` (`name="Clarinet in B♭"`, `abbr="Cl."`, `fifths=0`, `transpose=(-1,-2,0)`, `dyn={1:"p",3:"p",11:"mp",19:"mf"}`).
  - `REHEARSAL = {3:"A", 11:"B", 19:"C"}`, `WORDS = {23:"rit."}`, `RIT = {(23,0):62,(23,8):58,(24,0):52,(24,8):48}`, 템포 문구 `"Moderato"`.
  - `TITLE, COMPOSER = "You Raise Me Up", "Rolf Løvland"`, lyricist 줄은 `arr. 남연하 · 플루트·클라리넷 2중주`로. jobs 접두사 `youraisemeup_`, 키 `["flute","clarinet"]`.

- [ ] **Step 4: 통과 확인** — 같은 명령 → 모든 테스트 OK.

- [ ] **Step 5: 스테이징 + 메시지 제안** — `git add YouRaiseMeUp/source/gen.py YouRaiseMeUp/source/test_gen.py`; 제안: `feat(youraisemeup): add beginner flute–clarinet duet score source`

### Task 2: 빌드·게시 스크립트와 assets 생성

**Files:**
- Create: `YouRaiseMeUp/source/build.sh` (Godfather 복사, 주석의 폴더명만 변경)
- Create: `YouRaiseMeUp/source/mpos2json.py` (그대로 복사)
- Create: `YouRaiseMeUp/source/publish.py` (복사 후 수정)
- Create: `YouRaiseMeUp/source/README.md` (Godfather README에서 폴더명만 변경)
- Create (생성물): `YouRaiseMeUp/assets/youraisemeup_{full_score,flute,clarinet}.{pdf,mp3}`, `YouRaiseMeUp/assets/png/youraisemeup_*-N.png`, `YouRaiseMeUp/manifest.json`
- Modify: `.gitignore`에 `YouRaiseMeUp/source/out/`이 빠져 있으면 추가 (Godfather 줄 확인 후 같은 형식)

**Interfaces:**
- Consumes: Task 1의 `gen.py` CLI.
- Produces: `manifest.json` — 항목 3개, 각 `id,label,desc,pdf,mp3,pages,seconds,measures` (Godfather와 같은 스키마, `app.js`가 읽음).

- [ ] **Step 1: `publish.py` 수정** — 접두사 `youraisemeup_`, `ITEMS`:
  `("full_score","합주 (총보)","2중주 전체 · 지휘자용")`, `("flute","플루트","주선율")`, `("clarinet","클라리넷","B♭ · 화음 반주")`.
  덮어쓰기 전에 대상 폴더가 `YouRaiseMeUp/`인지 확인 (Godfather `G` 계산 방식 그대로면 자동).
- [ ] **Step 2: 빌드** — `bash YouRaiseMeUp/source/build.sh && python3 YouRaiseMeUp/source/publish.py`
  Expected: `built youraisemeup_...` 3줄, publish 출력 3줄, 각 `24 measures`.
- [ ] **Step 3: 결과 검증** —
  `python3 -c "import json;m=json.load(open('YouRaiseMeUp/manifest.json'));print([(x['id'],x['seconds'],len(x['measures']),len(x['pages'])) for x in m])"`
  Expected: id 순서 `full_score, flute, clarinet`, seconds 모두 85–95, measures 모두 24. 벗어나면 `TEMPO`/`RIT` 조정 후 Task 1 테스트 재실행·재빌드.
  플루트·클라리넷 파트 첫 쪽 PNG를 Read로 열어 조표(플루트 ♭2, 클라리넷 없음)·연습기호 A/B/C·rit.·늘임표 확인.
- [ ] **Step 4: 스테이징 + 메시지 제안** — `git add YouRaiseMeUp/source YouRaiseMeUp/assets YouRaiseMeUp/manifest.json .gitignore`; 제안: `feat(youraisemeup): build score pdf, png and audio assets`

### Task 3: 페이지, 허브 연결, 문서

**Files:**
- Create: `YouRaiseMeUp/{index.html,style.css,app.js,logo.png,pattern.svg}` (Godfather에서 복사)
- Modify: `YouRaiseMeUp/index.html`, `YouRaiseMeUp/app.js` ("Intermezzo" 문자열 교체), 필요 시 `YouRaiseMeUp/style.css`의 `.title-cover`/`.title-art span`
- Modify: `index.html:113-116` (`SCORES`)
- Modify: `CLAUDE.md` (구조 표 한 줄 + `## YouRaiseMeUp/` 섹션)

**Interfaces:**
- Consumes: Task 2의 `manifest.json`·assets 경로.

- [ ] **Step 1: 복사·문구 교체** —
  `index.html`: `<title>You Raise Me Up · 플루트·클라리넷 2중주</title>`, description `「You Raise Me Up」 플루트·클라리넷 초보용 2중주 편곡 — 악기별 악보와 연습용 음원`, `<h1>You Raise Me Up</h1>`, `<p>R. Løvland · 플루트·클라리넷 2중주</p>`, meta `콘서트 B♭장조 · 4/4 · ♩=66 · 24마디`, credit `<span>2026</span><span>arr. 남연하</span>`.
  `app.js`: `document.title`과 `.title-art span`의 `Intermezzo` → `You Raise Me Up`.
  확인: `grep -rn "Intermezzo\|godfather\|Mascagni" YouRaiseMeUp --include=*.html --include=*.js --include=*.css` → 출력 없음; `grep -n '\.\./' YouRaiseMeUp/index.html YouRaiseMeUp/app.js YouRaiseMeUp/style.css` → home-link 한 줄만.
- [ ] **Step 2: 허브 연결** — `SCORES`에 추가:
  `{ href: 'YouRaiseMeUp/', icon: '🎶', title: 'You Raise Me Up', sub: '뢰블란 · 플루트·클라리넷 2중주 (초보)', meta: '24마디 · 약 <Task 2 실제 초>' }` (meta는 Godfather처럼 "약 1분 NN초" 형식).
- [ ] **Step 3: 로컬 확인** — `python3 -m http.server 8000` (백그라운드) 후 브라우저 또는 `curl -s localhost:8000/YouRaiseMeUp/manifest.json | head`로 200 확인. 총보 첫 쪽에서 제목이 렌즈 안에 한 줄로 들어가는지, MuseScore 원래 제목이 다 가려지는지 확인 — 넘치면 `.title-art span` font-size(1.9cqw)를 줄이고, 원래 제목이 삐져나오면 `.title-cover` left/width를 넓힌다. 재생 시 마디 표시, 마디 클릭 재생, `#clarinet` 딥링크 동작 확인.
- [ ] **Step 4: 허브 링크 확인** — `curl -s -o /dev/null -w '%{http_code}' localhost:8000/YouRaiseMeUp/` → `200`; 루트 페이지에 카드 3개.
- [ ] **Step 5: CLAUDE.md** — 구조 표에 `| 유레이즈 | YouRaiseMeUp/ | You Raise Me Up 플루트·클라리넷 초보용 2중주 — canon과 같은 구조 |`, 하단에 Godfather 섹션 형식으로: 곡 정보(저작권 유효, 사용자 결정으로 공개 2026-11-13), 편성·초보 규칙(리듬·음역·임시표 없음), 구성(도입/A/B/C), `source/` 사용법과 `test_gen.py` 실행 명령, 선율은 기억 입력이라 원곡과 대조 필요.
- [ ] **Step 6: 스테이징 + 메시지 제안** — `git add YouRaiseMeUp index.html CLAUDE.md docs/superpowers`; 제안: `feat(youraisemeup): add duet score page and link from hub`
