# practice/ — 시네마 천국 클라리넷 연습 추가 (짧은 설계)

## 의도
`practice/`를 나머지 곡으로 넓히는 첫 걸음으로, 이번엔 **시네마 천국 클라리넷 솔로 하나만** Blue와 같은 연습 화면(`practice/#cinema_clarinet`)을 붙인다.

## 목표 / 비목표
- 목표: 운지·타임라인·구간 반복·예비박이 시네마 천국에서 정확히 동작. 악보 페이지 메뉴에서 연습으로 들어갈 수 있음.
- 비목표: 다른 곡(canon, Godfather, YouRaiseMeUp, Golden, shampoo) 확장. 연습 화면 UI 변경.
- 반목표: CinemaParadiso의 악보 PNG/MP3가 바뀌는 것.

## 접근 방식
하나뿐 — Blue 파이프라인(`extract.py` `PIECES` → `practice/data/*.json`)을 그대로 따른다. 연습 화면을 곡별로 따로 만드는 방식은 기존 구조와 어긋나서 버림.

## 할 일
1. 운지표 `clarinet.json`에 `G#3`, `A4` 추가 — WFG·UNSW 교차 대조 후 `verified`. SVG에는 `RP_Gs`, `LA` 키가 이미 있음.
2. `CinemaParadiso/source/gen.py`의 MusicXML `&` 미이스케이프 수정 (렌더 결과 동일, assets 재빌드 안 함).
3. 박자표 변화(2/4 마디) 지원: 데이터에 마디별 박 수 `measureBeats` 추가, `beatMs`·예비박이 그 마디의 박 수를 쓰도록. 테스트 추가.
4. `PIECES`에 `("CinemaParadiso", "cinema", "Cinema Paradiso", ["clarinet"])` 추가 후 `extract.py` 실행 (Blue 데이터는 동일해야 함).
5. `practice/app.js` 제목 오버레이: cinema는 CinemaParadiso 페이지 값(`left 31.5%`, `width 37%`)과 두 줄 제목.
6. `CinemaParadiso/app.js`·`style.css`에 연습 메뉴 링크와 구분선 (Blue와 동일 패턴).

## 빌더에게 맡김
- 렌즈 안 제목 줄바꿈 문구, 캐시 버스터 값.
