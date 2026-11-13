// 연습 화면의 순수 로직 (DOM 없음). 시간 단위는 ms, 마디 번호는 1부터.

/** ms 이하에서 시작한 마지막 이벤트 index, 첫 이벤트 전이면 -1. */
export function noteIndexAt(notes, ms) {
  let found = -1;
  for (let i = 0; i < notes.length; i++) {
    if (notes[i].ms <= ms) found = i;
    else break;
  }
  return found;
}

/** i 뒤 첫 rest:false index, 없으면 -1. */
export function nextPlayedIndex(notes, i) {
  for (let j = i + 1; j < notes.length; j++) {
    if (!notes[j].rest) return j;
  }
  return -1;
}

/** 입력 배열 등장 순서대로 눌러야 할/뗄 키. */
export function keyChanges(fromKeys, toKeys) {
  return {
    press: toKeys.filter((k) => !fromKeys.includes(k)),
    release: fromKeys.filter((k) => !toKeys.includes(k)),
  };
}

const SOLFEGE = { C: "도", D: "레", E: "미", F: "파", G: "솔", A: "라", B: "시" };

/** "F#3" -> "파♯", "Bb3" -> "시♭", "G3" -> "솔". */
export function solfege(pitch) {
  const m = /^([A-G])([#b]?)/.exec(pitch);
  if (!m) return "";
  return SOLFEGE[m[1]] + (m[2] === "#" ? "♯" : m[2] === "b" ? "♭" : "");
}

function measureEnd(measures, seconds, measureNo) {
  return measureNo < measures.length ? measures[measureNo] : seconds * 1000;
}

/** start~end 마디(포함) 구간의 [from, to] ms. */
export function loopBounds(measures, seconds, start, end) {
  return { from: measures[start - 1], to: measureEnd(measures, seconds, end) };
}

/** 한 박의 ms (재생 속도 rate 반영). */
export function beatMs(measures, seconds, beats, measureNo, rate) {
  const len = measureEnd(measures, seconds, measureNo) - measures[measureNo - 1];
  return len / beats / rate;
}
