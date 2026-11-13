# 손가락 연습 (practice/) — 클라리넷 1차 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 악보를 읽기 힘든 초보자가 MP3를 들으며 클라리넷 운지 그림과 타임라인을 보고 따라 연주하는 선택형 화면 `practice/`를 만든다 (클라리넷 독주 파트 6개).

**Architecture:** `practice/source/extract.py`가 각 곡의 `gen.py` → MusicXML → MuseScore 4(`.spos` 음 시작 ms, `.mpos` 마디 ms)로 파트별 음 이벤트 JSON을 정적으로 생성한다. `practice/` 단일 바닐라 JS 화면이 그 JSON, 운지표 `instruments/clarinet.json`, 정면 그림 `instruments/clarinet.svg`를 읽고, MP3는 각 악보 폴더 `assets/`에서 읽기만 한다. 기존 악보 페이지는 링크 한 줄씩만 추가.

**Tech Stack:** Python 3 (표준 라이브러리, `unittest`), MuseScore 4.7.x CLI, ffprobe, 바닐라 JS (ES module), `node --test` (Node 22), GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-11-13-clarinet-practice-design.md`

## 1차 실행 범위: Blue 클라리넷 시범 (사용자 결정 2026-11-13)

먼저 `blue_clarinet` 한 파트로 Task 1–6을 끝내고 사용자가 로컬에서 직접 써 본 뒤 나머지를 진행한다.
- Task 2: `PIECES`에는 Blue만 넣는다 (`("Blue","blue","그대 안의 블루",["clarinet"])`). 나머지 4곡 행은 시범 확인 후 추가.
- Task 3: 운지표는 Blue 클라리넷이 쓰는 기보음 14개(E3 F3 F♯3 G3 A3 B♭3 B3 C4 C♯4 D4 E4 F4 F♯4 G4)만. 테스트는 생성된 데이터 기준이라 그대로 동작.
- Task 6 브라우저 확인: blue_clarinet 하나로. Review Focus 2(쉼표로 시작)는 canon이 없으므로 시범에서는 첫 음 전(ms 음수 시크)으로 대신 확인.
- Task 7(진입 링크·CLAUDE.md)은 시범 확인 **후**에 한다. 시범 중에는 `http://localhost:8000/practice/#blue_clarinet`으로 연다.

## Global Constraints

- GitHub Pages 정적 배포, 바닐라 JS. 프레임워크·번들러·npm 패키지 추가 없음.
- 기존 악보 폴더(`canon/ Godfather/ YouRaiseMeUp/ Golden/ Blue/`)의 assets·manifest·gen.py는 **읽기만**. 수정 허용은 각 `index.html`에 링크 1줄뿐 (Task 7).
- 운지는 기억/추측으로 쓰지 않는다 — 공개 표 2곳 이상 대조, 항목마다 출처. 불일치 항목은 `"verified": false` + 테스트 실패 + 사용자 결정.
- `pitch`는 기보음(클라리넷 악보에 적힌 음). 계이름도 기보음 기준.
- 색: 지금 누름 = 녹색 채움, 안 누름 = 빈칸, 다음 음에서 바뀔 키 = 파란 테두리.
- 속도 선택지: 0.5 · 0.75 · 1.0x.
- 커밋·푸시는 사용자가 직접 — 각 Task 끝은 `git add` + 커밋 메시지 제안. 브랜치 `feature/practice-clarinet`.
- 커밋 메시지 `<type>(practice): <subject>`, 끝에 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

1. 일시정지 상태에서 시크바를 옮기거나 처음으로 돌아갔을 때 — 현재/다음 운지·타임라인이 즉시 그 위치로 갱신 (Task 5 `noteIndexAt` 테스트 + Task 6 브라우저 확인).
2. 첫 음 전·쉼표 구간 (canon 클라리넷은 쉼표로 시작) — "쉬어요" + 다음 음 운지 미리보기, 빈 화면이나 에러 없음 (Task 5 테스트).
3. 카운트인 중 정지·곡 변경·속도 변경 — 예약된 클릭/재생이 취소되고 두 번 재생되지 않음 (Task 6 브라우저 확인).
4. 구간 반복 끝이 마지막 마디일 때 — 곡 끝(`seconds`)까지 재생 후 시작 마디로 돌아감, `ended`로 멈추지 않음 (Task 5 `loopBounds` 테스트).
5. 휴대폰 세로 폭(375px) — 운지 그림이 화면 폭 대부분을 차지하고 가로 스크롤 없음 (Task 6 브라우저 확인).

---

### Task 1: 음 이벤트 파서 (`extract.py` 순수 함수)

**Files:**
- Create: `practice/source/extract.py`
- Test: `practice/source/test_extract.py`

**Interfaces:**
- Produces (all in `extract.py`):
  - `parse_notes(xml_text: str) -> tuple[list[dict], int]` — 반환 `(onsets, beats)`. onsets는 MusicXML 순서대로 `<chord/>`·`<grace/>`가 아닌 모든 `<note>` (붙임줄 끝 음 포함) 하나당 `{"pitch": "F#3" | None, "rest": bool, "measure": int, "tie_stop": bool}`. pitch 표기: step + (`#`/`b`, alter ±1) + octave. beats = 첫 `<time><beats>`.
  - `parse_spos(text: str) -> list[int]` — `<event elid=… position="ms">` 순서대로 ms.
  - `parse_mpos(text: str) -> list[int]` — 마디 시작 ms (같은 형식).
  - `build_notes(onsets: list[dict], times: list[int], end_ms: int) -> list[dict]` — 길이 다르면 `ValueError`. `tie_stop` 음은 앞 이벤트에 합침. 결과 `{"ms", "end", "pitch", "rest", "measure"}`, `end` = 다음 이벤트 `ms`, 마지막은 `end_ms`.

- [ ] **Step 1: 브랜치 만들기** — `git checkout -b feature/practice-clarinet` (spec·plan 문서도 이 브랜치에서 스테이징).

- [ ] **Step 2: 실패하는 테스트 작성** — 테스트 안에 작은 MusicXML 문자열(4/4, 2마디: 1마디 G3 2분 + 쉼표 2분, 2마디 F#3 2분 → 붙임줄 F#3 4분 + Bb3 4분)과 spos 문자열(5개 이벤트 0, 1000, 2000, 3000, 3500)을 고정값으로 둔다.

```python
def test_parse_notes(self):
    onsets, beats = parse_notes(XML)
    self.assertEqual(beats, 4)
    self.assertEqual([o["pitch"] for o in onsets], ["G3", None, "F#3", "F#3", "Bb3"])
    self.assertEqual([o["tie_stop"] for o in onsets], [False, False, False, True, False])
    self.assertEqual([o["measure"] for o in onsets], [1, 1, 2, 2, 2])

def test_parse_spos(self):
    self.assertEqual(parse_spos(SPOS), [0, 1000, 2000, 3000, 3500])

def test_build_notes_merges_tie_and_sets_end(self):
    notes = build_notes(parse_notes(XML)[0], [0, 1000, 2000, 3000, 3500], 4000)
    self.assertEqual([(n["ms"], n["end"], n["pitch"], n["rest"]) for n in notes],
                     [(0, 1000, "G3", False), (1000, 2000, None, True),
                      (2000, 3500, "F#3", False), (3500, 4000, "Bb3", False)])

def test_build_notes_count_mismatch_raises(self):
    with self.assertRaises(ValueError):
        build_notes(parse_notes(XML)[0], [0, 1000], 4000)
```

- [ ] **Step 3: 실패 확인** — `python3 -m unittest discover -s practice/source -v` → ImportError/FAIL.

- [ ] **Step 4: 구현** — `xml.etree.ElementTree` + `re` (mpos2json.py와 같은 정규식 방식). 외부 라이브러리 없음.

- [ ] **Step 5: 통과 확인** — 같은 명령 → 4 tests OK.

- [ ] **Step 6: 스테이징 + 커밋 메시지 제안** — `git add docs/superpowers/specs/2026-11-13-clarinet-practice-design.md docs/superpowers/plans/2026-11-13-clarinet-practice.md practice/source/` · 제안: `feat(practice): add note-event parser for practice data`

---

### Task 2: 곡 데이터 생성 파이프라인

**Files:**
- Modify: `practice/source/extract.py` (`PIECES`, `extract_part`, `main`)
- Modify: `practice/source/test_extract.py`
- Create (생성물, 커밋): `practice/pieces.json`, `practice/data/<piece>_<part>.json` 6개

**Interfaces:**
- Consumes: Task 1 함수들.
- Produces:
  - `PIECES = [ (folder, prefix, title, [part_id, ...]) ]` =
    `("canon","canon","Canon in D",["clarinet"])`, `("Godfather","godfather","Intermezzo",["clarinet_1","clarinet_2"])`, `("YouRaiseMeUp","youraisemeup","You Raise Me Up",["clarinet"])`, `("Golden","golden","Golden",["clarinet"])`, `("Blue","blue","그대 안의 블루",["clarinet"])`.
  - 데이터 JSON (spec 5.2 형식 + `beats`):
    `{"piece","part","instrument":"clarinet","title","partLabel","mp3":"../<Folder>/assets/<prefix>_<part>.mp3","score":"../<Folder>/#<part>","seconds","beats","measures":[ms...],"notes":[{"ms","end","pitch","rest","measure"}...]}` — `partLabel`·`seconds`는 기존 `<Folder>/manifest.json`의 해당 id 항목에서.
  - `pieces.json`: `[{"id":"<prefix>_<part>","title","partLabel","seconds"}]` (PIECES 순서).
  - 실행: `python3 practice/source/extract.py` (MuseScore 경로는 `MSCORE` 환경변수, 기본 `/Applications/MuseScore 4.app/Contents/MacOS/mscore`).

- [ ] **Step 1: 실패하는 테스트 작성** — 커밋된 생성물을 검사하는 테스트 (생성물이 없으면 실패):

```python
def test_every_part_matches_manifest_measures(self):
    for folder, prefix, title, parts in PIECES:
        man = {p["id"]: p for p in json.load(open(f"{ROOT}/{folder}/manifest.json"))}
        for part in parts:
            d = json.load(open(f"{ROOT}/practice/data/{prefix}_{part}.json"))
            self.assertEqual(d["measures"], [m["ms"] for m in man[part]["measures"]])
            self.assertEqual(d["seconds"], man[part]["seconds"])

def test_notes_monotonic_and_inside_audio(self):
    # 모든 파트: ms 단조 증가, end > ms, 마지막 end <= seconds*1000 + 1000
```

- [ ] **Step 2: 실패 확인** — `python3 -m unittest discover -s practice/source -v` → FileNotFoundError.

- [ ] **Step 3: `extract_part(folder, prefix, part, tmp) -> dict` 와 `main()` 구현** — 곡마다 `python3 -I <folder>/source/gen.py <tmp>` → `mscore -o x.mscz x.musicxml` → `-o x.spos`, `-o x.mpos`. `end_ms` = ffprobe로 잰 `<folder>/assets/<prefix>_<part>.mp3` 길이(ms). mpos 마디 ms가 manifest와 다르면 `SystemExit`로 멈춤 (spec 5.2 시간 일치 검증). 임시 폴더는 `tempfile.TemporaryDirectory`.

- [ ] **Step 4: 생성 실행** — `python3 practice/source/extract.py` → 6줄 출력 (`<id>: <음 개수> notes, <마디> measures`). 기존 악보 폴더에 변경 없음 확인: `git status --short canon Godfather YouRaiseMeUp Golden Blue` → 비어 있음(원래 미추적 원본 3개 제외).

- [ ] **Step 5: 통과 확인** — unittest 전부 OK.

- [ ] **Step 6: 스테이징 + 제안** — `git add practice/` · `feat(practice): generate clarinet note timelines from score sources`

---

### Task 3: 클라리넷 운지표 (`instruments/clarinet.json`) + 정면 그림 (`clarinet.svg`)

**Files:**
- Create: `practice/instruments/clarinet.json`, `practice/instruments/clarinet.svg`
- Modify: `practice/source/test_extract.py`

**Interfaces:**
- Produces `clarinet.json`:
  ```json
  { "instrument": "clarinet", "system": "boehm",
    "sources": [{"id": "wfg", "url": "…"}, {"id": "<2nd>", "url": "…"}],
    "keyList": [{"id": "thumb", "label": "엄지 구멍"}, …],
    "notes": { "E3": {"keys": ["thumb", "L1", …], "alt": [[…]], "src": ["wfg", "<2nd>"], "verified": true }, … } }
  ```
  키 id 규칙: 앞면 링 `L1 L2 L3 R1 R2 R3`, 뒷면 `thumb` `reg`, 왼손 위쪽 `LA`(A키) `LGs`(G♯키), 새끼키는 `LP_` / `RP_` 접두사 (예: `LP_E`, `RP_F`), 오른손 옆키 `RS1…`. 필요한 키가 더 있으면 같은 규칙으로 `keyList`에 추가.
  `clarinet.svg`: `keyList`의 id마다 같은 `id` 속성을 가진 도형. `viewBox`만 쓰고 고정 width/height 없음. 색은 CSS가 칠한다 (SVG 안에 fill 고정 금지 — 클래스 `.on` `.next` 로 바뀜).

- [ ] **Step 1: 실패하는 테스트 작성**

```python
def test_fingering_covers_every_used_pitch(self):
    # practice/data/*.json 의 모든 rest=False pitch 가 clarinet.json notes 에 있음
def test_every_entry_verified_with_two_sources(self):
    # 모든 항목 verified is True 이고 len(src) >= 2 — 실패 시 미확인 음 목록을 메시지에 출력
def test_keys_exist_in_keylist_and_svg(self):
    # notes 의 keys·alt 에 쓰인 id ⊆ keyList id, keyList id 마다 svg 에 id="…" 존재
```

- [ ] **Step 2: 실패 확인** — FileNotFoundError.

- [ ] **Step 3: 출처 수집** — The Woodwind Fingering Guide 클라리넷 표(wfg.woodwind.org)와 공개된 두 번째 표준 운지표를 WebFetch로 읽어, 6개 파트에서 쓰는 기보음(E3–C♯6, 약 30개 — Step 1 테스트가 정확한 목록을 출력) 각각의 기본 운지와 새끼키 대체 운지를 옮긴다. 두 표가 다르면 그 음은 `"verified": false`, 두 운지를 `keys`/`alt`에 모두 남긴다. 기억으로 채우지 않는다.

- [ ] **Step 4: `clarinet.svg` 작성** — 세로로 선 클라리넷 정면(위=마우스피스), 링 6개는 크게(터치 없이 보는 용도, 초보가 한눈에), 뒷면 `thumb`·`reg`는 몸통 왼쪽 옆 작은 원, 새끼키는 아래쪽 좌우 묶음, 각 도형에 `<title>`로 한국어 라벨.

- [ ] **Step 5: 테스트 실행** — `verified` 테스트 외 전부 OK. 미확인 음이 있으면 **멈추고** 목록(음, 두 출처 운지)을 사용자에게 보여 결정받은 뒤 반영 → 전부 OK.

- [ ] **Step 6: 스테이징 + 제안** — `git add practice/instruments practice/source` · `feat(practice): add verified boehm clarinet fingering chart and key diagram`

---

### Task 4: 새끼손가락 대체 운지 규칙 → 이벤트 `fingering`

**Files:**
- Modify: `practice/source/extract.py` (`apply_fingering`, `extract_part`에서 호출)
- Modify: `practice/source/test_extract.py`
- Regenerate: `practice/data/*.json`

**Interfaces:**
- Consumes: Task 3 `clarinet.json` 형식, Task 1 notes.
- Produces: `apply_fingering(notes: list[dict], chart: dict) -> list[dict]` — 쉼표 아닌 이벤트마다 `fingering: list[str]` (키 id), 대체 운지를 쓴 이벤트는 `alt: true`. 데이터 JSON의 notes에 이 두 필드 추가. `main()`은 `alt: true` 이벤트를 `<id> m<마디> <pitch> → alt` 줄로 출력.

규칙 (spec 5.3 그대로): 쉼표를 건너뛴 바로 앞 음의 `fingering`에 새끼키(`LP_`/`RP_`) k1, 현재 음 기본 `keys`에 같은 쪽 접두사의 새끼키 k2이고 k1 ≠ k2 → `alt` 중 그 충돌이 없는 첫 운지를 쓴다. 없으면 기본 유지. 뒤 음은 보지 않는다.

- [ ] **Step 1: 실패하는 테스트 작성** — 테스트 안 가짜 chart(`X`: keys `[L1, LP_E]`, `Y`: keys `[L1, LP_F]`, alt `[[L1, RP_F]]`, `Z`: keys `[L1, LP_F]`, alt 없음):

```python
def test_switches_to_alt_on_same_pinky_conflict(self):
    out = apply_fingering(notes("X", "Y"), CHART)
    self.assertEqual(out[1]["fingering"], ["L1", "RP_F"]); self.assertTrue(out[1]["alt"])
def test_skips_rests_when_looking_back(self):
    out = apply_fingering(notes("X", None, "Y"), CHART)
    self.assertTrue(out[2]["alt"])
def test_keeps_default_without_usable_alt(self):
    out = apply_fingering(notes("X", "Z"), CHART)
    self.assertEqual(out[1]["fingering"], ["L1", "LP_F"]); self.assertFalse(out[1].get("alt", False))
def test_generated_data_has_fingering_on_every_note(self):
    # data/*.json 의 rest=False 이벤트 모두 fingering 존재
```

- [ ] **Step 2: 실패 확인** → ImportError/FAIL.
- [ ] **Step 3: 구현** + `extract_part`에서 호출.
- [ ] **Step 4: 재생성** — `python3 practice/source/extract.py`, 출력된 `alt` 목록을 기록해 두기 (최종 보고에 포함).
- [ ] **Step 5: 통과 확인** — unittest 전부 OK.
- [ ] **Step 6: 스테이징 + 제안** — `feat(practice): pick alternate pinky fingerings to avoid slides`

---

### Task 5: 화면 순수 로직 (`core.js`)

**Files:**
- Create: `practice/core.js` (ES module, DOM 없음)
- Test: `practice/core.test.mjs`

**Interfaces:**
- Produces (named exports):
  - `noteIndexAt(notes, ms) -> number` — `ms` 이하에서 시작한 마지막 이벤트 index, 첫 이벤트 전이면 `-1`.
  - `nextPlayedIndex(notes, i) -> number` — `i` 뒤 첫 `rest:false` index, 없으면 `-1`.
  - `keyChanges(fromKeys, toKeys) -> {press: string[], release: string[]}`.
  - `solfege(pitch) -> string` — `"G3"→"솔"`, `"F#3"→"파♯"`, `"Bb3"→"시♭"`, `"C6"→"도"`.
  - `loopBounds(measures, seconds, start, end) -> {from, to}` (ms, 마디 번호 1부터; `end`가 마지막 마디면 `to = seconds*1000`).
  - `beatMs(measures, seconds, beats, measureNo, rate) -> number` — 그 마디 길이 / beats / rate (마지막 마디는 `seconds*1000`까지).

- [ ] **Step 1: 실패하는 테스트 작성** (`node:test`, `node:assert/strict`)

```js
const N = [{ms:0,end:1000,rest:true},{ms:1000,end:2000,pitch:"G3",rest:false},{ms:2000,end:3000,pitch:"A3",rest:false}];
test("before first / inside / at boundary", () => {
  assert.equal(noteIndexAt(N, -5), -1); assert.equal(noteIndexAt(N, 500), 0);
  assert.equal(noteIndexAt(N, 1000), 1); assert.equal(noteIndexAt(N, 9999), 2); });
test("next played skips rests", () => { assert.equal(nextPlayedIndex(N, 0), 1); assert.equal(nextPlayedIndex(N, 2), -1); });
test("key changes", () => assert.deepEqual(keyChanges(["L1","L2","L3"], ["L1","L2"]), {press: [], release: ["L3"]}));
test("solfege", () => { assert.equal(solfege("F#3"), "파♯"); assert.equal(solfege("Bb3"), "시♭"); assert.equal(solfege("C6"), "도"); });
test("loop to last measure ends at audio end", () =>
  assert.deepEqual(loopBounds([0, 4000, 8000], 14, 2, 3), {from: 4000, to: 14000}));
test("beat ms honours rate", () => assert.equal(beatMs([0, 4000, 8000], 14, 4, 1, 0.5), 2000));
```

- [ ] **Step 2: 실패 확인** — `node --test practice/core.test.mjs` → 모듈 없음 FAIL.
- [ ] **Step 3: 구현** — 각 함수 몇 줄, 이진 탐색 불필요(음 수백 개).
- [ ] **Step 4: 통과 확인** — `node --test practice/core.test.mjs` → 6 pass.
- [ ] **Step 5: 스테이징 + 제안** — `feat(practice): add timing and fingering helpers`

---

### Task 6: 연습 화면 (`index.html` / `style.css` / `app.js`)

**Files:**
- Create: `practice/index.html`, `practice/style.css`, `practice/app.js` (ES module, `core.js` import)

**Interfaces:**
- Consumes: `pieces.json`, `data/<id>.json` (Task 2·4 형식), `instruments/clarinet.json`·`clarinet.svg` (Task 3, SVG는 fetch 후 인라인 삽입해 id로 클래스 토글), `core.js` (Task 5).
- 딥링크 `#<id>` (예 `#blue_clarinet`), 없으면 `pieces.json` 첫 항목.

화면 요소 (spec 5.4 스케치 배치, 기존 악보 페이지의 색·글꼴 톤을 따름):
- 상단: `<a class="home-link" href="../">← 메인</a>`, 곡/파트 선택 `<select>`, "🎼 악보로 보기" (`score` 링크).
- 운지 패널: 인라인 SVG — 현재 음 `fingering` 키에 `.on`, `keyChanges(현재, 다음)`의 press∪release 키에 `.next`. 쉼표·첫 음 전이면 `.on` 없음 + "쉬어요". 옆에 계이름(크게) + pitch(작게) + 현재 음 남은 길이 막대, "다음: 라 A3 · L3 떼기" 문구 (press/release 라벨은 `keyList.label`).
- 타임라인: 가로, 현재선 고정, 앞 4초·뒤 1초 표시, 음 블록 폭 = 길이, 블록 안 계이름, 마디 경계선. 매 프레임 `transform`만 바꿈.
- 플레이어: `<audio>` (`preservesPitch = true`), 재생/정지(스페이스), 시크바, 시간, 속도 버튼 0.5/0.75/1.0, 반복 시작·끝 마디 `<select>` + 켜기/끄기, 카운트인 켜기/끄기 (기본 켜짐).
- 갱신: `requestAnimationFrame`에서 `noteIndexAt(notes, currentTime*1000)`; index가 바뀔 때만 운지·문구 DOM 갱신. `seeked`·일시정지 상태 시크에서도 1회 갱신.
- 카운트인: 재생 시작(처음 또는 반복 시작 마디) 전 `beats`번 Web Audio 짧은 클릭, 간격 `beatMs(...)`, 마지막 클릭 뒤 `audio.play()`. 대기 중 정지/곡 변경/속도 변경 → 예약 전부 취소.
- 반복: `currentTime*1000 >= to` → `currentTime = from/1000` (반복 중엔 카운트인 없이 바로 이어감). `ended`에서도 반복 켜져 있으면 `from`으로.
- 375px 폭: 세로 배치, SVG 폭 최대, 가로 스크롤 없음.

- [ ] **Step 1: 페이지 작성** (위 요소).
- [ ] **Step 2: 로직 테스트 재확인** — `node --test practice/core.test.mjs` → pass, `python3 -m unittest discover -s practice/source` → OK.
- [ ] **Step 3: 브라우저 확인** — `python3 -m http.server` 후 `http://localhost:8000/practice/#youraisemeup_clarinet` (claude-in-chrome 사용 가능). 확인 목록:
  - 6개 파트 각각 재생, 운지·계이름이 소리 나는 음과 맞음, rit.·늘임표 마지막 구간 맞음.
  - 0.5x에서 소리와 화면 일치, 음 높이 그대로.
  - 일시정지 후 시크 → 운지 즉시 갱신 (Review Focus 1). canon 처음 쉼표 구간 "쉬어요" + 다음 음 표시 (2).
  - 카운트인 중 정지·곡 변경·속도 변경 → 재생 안 됨/두 번 재생 없음 (3).
  - 반복 끝 = 마지막 마디 → 처음 마디로 돌아감 (4).
  - 375px 폭 가로 스크롤 없음, 그림 큼 (5). 콘솔 에러 없음.
- [ ] **Step 4: 스테이징 + 제안** — `feat(practice): add clarinet finger practice page`

---

### Task 7: 진입 링크 + 문서

**Files:**
- Modify: 루트 `index.html` — `OTHERS` 배열 맨 앞에 `{ href: 'practice/', icon: '🖐', title: '손가락 연습', sub: '클라리넷 · 악보 없이 따라 하기' }`
- Modify: `canon/index.html`, `Godfather/index.html`, `YouRaiseMeUp/index.html`, `Golden/index.html`, `Blue/index.html` — `.sidebar-foot` 맨 위에 한 줄
  `<a class="home-link" href="../practice/#<prefix>_<part>">🖐 손가락 연습</a>` (Godfather는 `godfather_clarinet_1`). 기존 `.home-link` 스타일 재사용, CSS·app.js 무변경.
- Modify: `CLAUDE.md` — 구조 표에 `practice/` 행, "practice/ 는 악보 폴더 assets의 MP3를 읽기만 하는 유일한 영역 간 참조" 예외, `## practice/` 절(파일 구조, 다시 만들기 `python3 -m unittest discover -s practice/source && node --test practice/core.test.mjs && python3 practice/source/extract.py`, 운지 출처·미확인 규칙, 악기 확장 방법 spec 5.6).

- [ ] **Step 1: 링크·문서 수정.**
- [ ] **Step 2: 회귀 확인** — 브라우저: 메인 칩 → practice 열림; 악보 페이지 5개 각각 링크 → 해당 파트 연습 화면; 각 악보 페이지 재생·마디 사각형·마디 클릭 재생 그대로; 모바일 폭에서 사이드바 링크가 메뉴를 가리지 않음. `git diff --stat` 에서 악보 폴더 변경은 `index.html` 5개 각 1줄뿐.
- [ ] **Step 3: 전체 테스트** — `python3 -m unittest discover -s practice/source && node --test practice/core.test.mjs` → 모두 통과.
- [ ] **Step 4: 스테이징 + 제안** — `feat(practice): link finger practice from hub and score pages` · 사용자에게 보고: 대체 운지 목록(Task 4), 운지 최종 확인 요청, PR 생성 여부 확인.
