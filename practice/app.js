// 손가락 연습 화면. 순수 로직은 core.js, 여기는 DOM·오디오만.
import { noteIndexAt, nextPlayedIndex, keyChanges, solfege, loopBounds, beatMs, measureProgress, beatsAt } from "./core.js?v=20261126a";

const $ = (id) => document.getElementById(id);
const audio = $("audio");
const playBtn = $("play");
const seek = $("seek");
const timeEl = $("time");
const track = $("track");
const timelineEl = track.parentElement;
const fingeringEl = $("fingering");
const scorePagesEl = $("scorePages");
const nowMeasureEl = $("nowMeasure");
const pieceSelect = $("pieceSelect");
const loopStartSel = $("loopStart");
const loopEndSel = $("loopEnd");
const loopToggle = $("loopToggle");
const countToggle = $("countToggle");
const countInEl = $("countIn");

const marker = document.createElement("div");
marker.className = "marker";
marker.hidden = true;
const markerFill = document.createElement("div");
markerFill.className = "marker-fill";
const markerHead = document.createElement("div");
markerHead.className = "marker-head";
marker.append(markerFill, markerHead);

const PAST_MS = 1000;   // 현재선 왼쪽(지난) 1초
const AHEAD_MS = 4000;  // 현재선 오른쪽(다가올) 4초

audio.preservesPitch = true;
audio.mozPreservesPitch = true;
audio.webkitPreservesPitch = true;

const V = "?v=20261126a";
let pieces = [];
let data = null;            // data/<id>.json
let pendingSeekSec = null;
let labels = {};            // keyId -> 한국어 라벨
let keyEls = {};            // keyId -> SVG 요소
let blocks = [];            // 타임라인 음 블록 (notes와 같은 index)
let pxPerMs = 0;
let lastKey = null;         // 마지막으로 그린 상태 (index + 쉼 여부)
let curMeasure = -2;        // 마지막으로 그린 악보 마디 index
let curRow = "";            // 마지막으로 스크롤 맞춘 악보 줄 (page:t)
let rate = 1;
let loopOn = false;
let countOn = true;
let loadToken = 0;
const instrumentCache = {};

// ---------- 카운트인 (Web Audio) ----------
let actx = null;
const pending = { timers: [], oscs: [], active: false };

// iOS Safari는 탭(사용자 제스처) 안에서 시작한 재생만 허용한다. 카운트인 뒤 setTimeout의 play()는
// 제스처가 끊겨 막힐 수 있으므로, 탭 순간에 음소거로 잠깐 재생→정지해 요소를 "풀어" 둔다.
let unlock = null;          // { token, startSec } — 음소거 재생 중이면 값이 있다
let unlockToken = 0;

function unlockAudio(startSec) {
  const token = ++unlockToken;
  unlock = { token, startSec };
  audio.muted = true;
  let p;
  try { p = audio.play(); } catch { p = Promise.reject(); }
  Promise.resolve(p).then(() => {
    if (!unlock || unlock.token !== token) return;   // 이미 끝났거나 취소됨
    endUnlock();
  }).catch(() => {
    if (unlock && unlock.token === token) endUnlock();
  });
}

/** 음소거 재생을 멈추고 시작 위치·음량을 되돌린다 (소리 안 남, 위치 그대로). */
function endUnlock() {
  if (!unlock) return;
  const { startSec } = unlock;
  unlock = null;
  unlockToken++;
  audio.pause();
  audio.currentTime = startSec;
  audio.muted = false;
}

function playAudio() {
  hidePlayMsg();
  let p;
  try { p = audio.play(); } catch (err) { p = Promise.reject(err); }
  return Promise.resolve(p).catch((err) => {
    syncPlayButton();
    // AbortError = 정지·곡 변경으로 중단된 것이라 정상
    if (!err || err.name !== "AbortError") showPlayMsg("재생이 막혔어요. ▶를 한 번 더 눌러 주세요.");
  });
}

const playMsg = $("playMsg");
function showPlayMsg(text) { playMsg.textContent = text; playMsg.hidden = false; }
function hidePlayMsg() { playMsg.hidden = true; playMsg.textContent = ""; }

function cancelCountIn() {
  endUnlock();
  pending.timers.forEach(clearTimeout);
  pending.oscs.forEach((o) => { try { o.stop(); } catch {} try { o.disconnect(); } catch {} });
  pending.timers = [];
  pending.oscs = [];
  if (pending.active) {
    pending.active = false;
    countInEl.textContent = "";
    syncPlayButton();
  }
}

function click(at, accent) {
  const osc = actx.createOscillator();
  const gain = actx.createGain();
  osc.frequency.value = accent ? 1600 : 1000;
  gain.gain.setValueAtTime(0.0001, at);
  gain.gain.exponentialRampToValueAtTime(0.5, at + 0.004);
  gain.gain.exponentialRampToValueAtTime(0.0001, at + 0.06);
  osc.connect(gain).connect(actx.destination);
  osc.start(at);
  osc.stop(at + 0.08);
  pending.oscs.push(osc);
}

function startWithCountIn() {
  cancelCountIn();
  try {
    actx = actx || new (window.AudioContext || window.webkitAudioContext)();
    if (actx.state === "suspended") actx.resume();
  } catch {
    actx = null;
  }
  if (!actx) { playAudio(); return; }
  const startSec = audio.currentTime;
  const ms = startSec * 1000;
  const measureNo = Math.max(1, noteIndexAt(data.measures.map((m) => ({ ms: m })), ms) + 1);
  const beats = beatsAt(data.measureBeats, data.beats, measureNo);
  const beat = beatMs(data.measures, data.seconds, beats, measureNo, rate);
  const t0 = actx.currentTime + 0.05;
  pending.active = true;
  syncPlayButton();
  unlockAudio(startSec);
  for (let i = 0; i < beats; i++) {
    click(t0 + (i * beat) / 1000, i === 0);
    pending.timers.push(setTimeout(() => { countInEl.textContent = String(i + 1); }, 50 + i * beat));
  }
  pending.timers.push(setTimeout(() => {
    pending.timers = [];
    pending.oscs = [];
    pending.active = false;
    countInEl.textContent = "";
    endUnlock();                 // 늦게 끝나는 음소거 재생이 있으면 정리
    audio.currentTime = startSec;
    audio.muted = false;
    playAudio();
  }, 50 + beats * beat));
}

// ---------- 재생 제어 ----------
function syncPlayButton() {
  playBtn.classList.toggle("playing", !audio.paused || pending.active);
}

function loopRange() {
  return loopBounds(data.measures, data.seconds, +loopStartSel.value, +loopEndSel.value);
}

function togglePlay() {
  if (!data) return;
  if (pending.active) { cancelCountIn(); return; }
  if (!audio.paused) { audio.pause(); return; }
  let ms = audio.currentTime * 1000;
  const dur = (audio.duration || data.seconds) * 1000;
  if (ms >= dur - 50) { audio.currentTime = 0; ms = 0; }
  let atStart = ms < 30;
  if (loopOn) {
    const { from, to } = loopRange();
    if (ms < from || ms >= to - 30) { audio.currentTime = from / 1000; ms = from; }
    atStart = atStart || Math.abs(ms - from) < 30;
  }
  if (countOn && atStart) startWithCountIn();
  else playAudio();
}

playBtn.addEventListener("click", togglePlay);
audio.addEventListener("play", syncPlayButton);
audio.addEventListener("pause", syncPlayButton);
audio.addEventListener("ended", () => {
  if (loopOn && data) {
    audio.currentTime = loopRange().from / 1000;
    playAudio();
  }
  syncPlayButton();
});
audio.addEventListener("seeked", () => render(true));
audio.addEventListener("loadedmetadata", () => {
  if (pendingSeekSec !== null) {
    const sec = pendingSeekSec;
    pendingSeekSec = null;
    audio.currentTime = sec;
  }
  render(true);
});

document.addEventListener("keydown", (e) => {
  if (e.code !== "Space") return;
  const tag = document.activeElement && document.activeElement.tagName;
  if (tag === "SELECT" || tag === "A" || (tag === "INPUT" && document.activeElement.type !== "range")) return;
  e.preventDefault();   // 버튼에 포커스가 있어도 기본 click 대신 한 번만 토글
  togglePlay();
});

let seeking = false;   // 시크바를 끄는 동안엔 값을 덮어쓰지 않는다
seek.addEventListener("pointerdown", () => { seeking = true; });
window.addEventListener("pointerup", () => { seeking = false; });
seek.addEventListener("change", () => { seeking = false; });
seek.addEventListener("input", () => {
  cancelCountIn();
  audio.currentTime = (+seek.value) / 1000;
  render(true);
});

document.querySelectorAll("[data-rate]").forEach((btn) => {
  btn.addEventListener("click", () => {
    cancelCountIn();
    rate = +btn.dataset.rate;
    audio.playbackRate = rate;
    document.querySelectorAll("[data-rate]").forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
  });
});

function setToggle(btn, on) {
  btn.setAttribute("aria-pressed", String(on));
  btn.textContent = on ? "켜기" : "끄기";
}
loopToggle.addEventListener("click", () => {
  loopOn = !loopOn;
  setToggle(loopToggle, loopOn);
  if (loopOn && !audio.paused) {
    const { from, to } = loopRange();
    const ms = audio.currentTime * 1000;
    if (ms < from || ms >= to) audio.currentTime = from / 1000;
  }
});
countToggle.addEventListener("click", () => {
  countOn = !countOn;
  setToggle(countToggle, countOn);
  if (!countOn) cancelCountIn();
});
loopStartSel.addEventListener("change", () => {
  if (+loopEndSel.value < +loopStartSel.value) loopEndSel.value = loopStartSel.value;
});
loopEndSel.addEventListener("change", () => {
  if (+loopEndSel.value < +loopStartSel.value) loopStartSel.value = loopEndSel.value;
});

// ---------- 화면 그리기 ----------
function fmt(sec) {
  const s = Math.max(0, Math.floor(sec));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

function setKeys(onKeys, nextKeys) {
  for (const id in keyEls) {
    keyEls[id].classList.toggle("on", onKeys.includes(id));
    keyEls[id].classList.toggle("next", nextKeys.includes(id));
  }
}

function changeText(press, release) {
  const parts = [];
  release.forEach((k) => parts.push(`${labels[k] || k} 떼기`));
  press.forEach((k) => parts.push(`${labels[k] || k} 누르기`));
  return parts.length ? parts.join(" · ") : "손가락 그대로";
}

function drawState(idx, resting) {
  const notes = data.notes;
  const cur = idx >= 0 && !resting ? notes[idx] : null;
  const curKeys = cur ? cur.fingering : [];
  const nextIdx = nextPlayedIndex(notes, idx);
  const next = nextIdx >= 0 ? notes[nextIdx] : null;
  const { press, release } = next ? keyChanges(curKeys, next.fingering) : { press: [], release: [] };

  setKeys(curKeys, [...press, ...release]);
  document.querySelector(".now").classList.toggle("rest", !cur);
  $("nowSolfege").textContent = cur ? solfege(cur.pitch) : "쉬어요";
  $("nowPitch").textContent = cur ? cur.pitch : "";
  const nt = $("nextText");
  nt.textContent = "";
  if (next) {
    nt.append(`${solfege(next.pitch)} ${next.pitch}`);
    const chg = document.createElement("span");
    chg.className = "chg";
    chg.textContent = "→ " + changeText(press, release);
    nt.append(chg);
  } else {
    nt.textContent = "끝";
  }
  blocks.forEach((b, i) => b.classList.toggle("cur", i === idx && !resting));
}

function centerMarkerInScore(page, m) {
  const sr = scorePagesEl.getBoundingClientRect();
  const pr = page.getBoundingClientRect();
  if (!sr.height || !pr.height) return;
  const mid = pr.top + pr.height * ((m.t + m.h / 2) / 100);
  const target = sr.top + sr.height / 2;
  const delta = mid - target;
  if (Math.abs(delta) > 8) scorePagesEl.scrollBy({ top: delta, behavior: "smooth" });
}

function updateScoreProgress(ms, force) {
  const total = data.measures.length;
  const { index, ratio } = measureProgress(data.measures, data.seconds, ms);
  if (force || index !== curMeasure) {
    curMeasure = index;
    nowMeasureEl.textContent = index >= 0 ? `${index + 1} / ${total} 마디` : `준비 (${total} 마디)`;
    const boxes = data.measureBoxes;
    if (index < 0 || !boxes || !boxes[index]) {
      marker.hidden = true;
    } else {
      const m = boxes[index];
      const page = scorePagesEl.children[m.page];
      if (page) {
        if (marker.parentNode !== page) page.appendChild(marker);
        Object.assign(marker.style, {
          left: `${m.l}%`,
          top: `calc(${m.t}% - 12px)`,
          width: `${m.w}%`,
          height: `calc(${m.h}% + 24px)`,
        });
        marker.dataset.bar = String(index + 1);
        marker.hidden = false;
        const row = `${m.page}:${m.t}`;
        if (row !== curRow) {
          curRow = row;
          centerMarkerInScore(page, m);
        }
      }
    }
  }
  if (!marker.hidden) {
    const pct = `${(ratio * 100).toFixed(2)}%`;
    markerFill.style.width = pct;
    markerHead.style.left = pct;
  }
}

scorePagesEl.addEventListener("click", (e) => {
  if (!data || !data.measureBoxes) return;
  const page = e.target.closest(".page");
  if (!page) return;
  const pi = [...scorePagesEl.children].indexOf(page);
  const rect = page.getBoundingClientRect();
  const x = ((e.clientX - rect.left) / rect.width) * 100;
  const y = ((e.clientY - rect.top) / rect.height) * 100;
  const pad = (12 / rect.height) * 100;
  const i = data.measureBoxes.findIndex((m) =>
    m.page === pi && x >= m.l && x <= m.l + m.w && y >= m.t - pad && y <= m.t + m.h + pad
  );
  if (i < 0) return;
  cancelCountIn();
  const targetSec = data.measures[i] / 1000;
  if (audio.readyState > 0) {
    pendingSeekSec = null;
    audio.currentTime = targetSec;
  } else {
    pendingSeekSec = targetSec;
  }
  render(true);
  if (audio.paused) playAudio();
});

function render(force) {
  if (!data) return;
  const ms = (pendingSeekSec !== null ? pendingSeekSec : audio.currentTime) * 1000;
  const notes = data.notes;
  const idx = noteIndexAt(notes, ms);
  const note = idx >= 0 ? notes[idx] : null;
  const resting = !note || note.rest || ms >= note.end;
  const key = `${idx}${resting ? "r" : ""}`;
  if (force || key !== lastKey) {
    lastKey = key;
    drawState(idx, resting);
  }
  updateScoreProgress(ms, force);
  // 매 프레임: 남은 길이 막대 · 타임라인 위치 · 시간
  const frac = resting ? 0 : Math.min(1, Math.max(0, (note.end - ms) / (note.end - note.ms)));
  $("remainBar").style.transform = `scaleX(${frac})`;
  track.style.transform = `translateX(${(PAST_MS - ms) * pxPerMs}px)`;
  const dur = audio.duration || data.seconds;
  if (!seeking) seek.value = String(Math.round(ms));
  timeEl.textContent = `${fmt(ms / 1000)} / ${fmt(dur)}`;
}

function frame() {
  if (data && loopOn && !audio.paused) {
    const { from, to } = loopRange();
    if (audio.currentTime * 1000 >= to) audio.currentTime = from / 1000;
  }
  render(false);
  requestAnimationFrame(frame);
}

// ---------- 타임라인 ----------
function layoutTimeline() {
  if (!data) return;
  pxPerMs = timelineEl.clientWidth / (PAST_MS + AHEAD_MS);
  data.notes.forEach((n, i) => {
    const b = blocks[i];
    b.style.left = `${n.ms * pxPerMs}px`;
    b.style.width = `${Math.max(2, (n.end - n.ms) * pxPerMs - 2)}px`;
  });
  track.querySelectorAll(".bar").forEach((bar) => {
    bar.style.left = `${+bar.dataset.ms * pxPerMs}px`;
  });
  render(true);
}

function buildTimeline() {
  track.textContent = "";
  blocks = data.notes.map((n) => {
    const b = document.createElement("div");
    b.className = n.rest ? "blk r" : "blk";
    b.textContent = n.rest ? "쉼" : solfege(n.pitch);
    track.append(b);
    return b;
  });
  data.measures.forEach((ms, i) => {
    const bar = document.createElement("div");
    bar.className = "bar";
    bar.dataset.ms = String(ms);
    const s = document.createElement("span");
    s.textContent = String(i + 1);
    bar.append(s);
    track.append(bar);
  });
  layoutTimeline();
}
new ResizeObserver(layoutTimeline).observe(timelineEl);

// ---------- 불러오기 ----------
async function getJSON(url) {
  const sep = url.includes("?") ? "&" : "?";
  const r = await fetch(`${url}${sep}${V.slice(1)}`, { cache: "no-cache" });
  if (!r.ok) throw new Error(`${url}: ${r.status}`);
  return r.json();
}

async function loadInstrument(name) {
  if (!instrumentCache[name]) {
    instrumentCache[name] = Promise.all([
      getJSON(`instruments/${name}.json`),
      fetch(`instruments/${name}.svg`, { cache: "no-cache" }).then((r) => {
        if (!r.ok) throw new Error(`instruments/${name}.svg: ${r.status}`);
        return r.text();
      }),
    ]);
  }
  return instrumentCache[name];
}

function fillMeasureSelect(sel, n, value) {
  sel.textContent = "";
  for (let i = 1; i <= n; i++) sel.append(new Option(String(i), String(i)));
  sel.value = String(value);
}

// 사이드바 제목·부제·곡 정보 — 각 악보 페이지(<Folder>/index.html)의 .brand · .sidebar-foot 문구와 같게
const PIECE_INFO = {
  blue: { title: "그대 안의 블루", sub: "김현철 · 이소라", meta: "콘서트 F→B♭장조 · 4/4 · ♩=70 · 24마디" },
  cinema: { title: "시네마 천국 (Love Theme)", sub: "Ennio & Andrea Morricone · 클라리넷 솔로", meta: "기보 C장조/A단조 · 4/4 · ♩=66 · 21마디" },
};

async function buildSidebarMenu(d, id) {
  const menuEl = $("menu");
  const base = d.score.split("#")[0];
  let scoreItems = [];
  try {
    scoreItems = await getJSON(`${base}manifest.json`);
  } catch {
    scoreItems = [];
  }
  if (menuEl) {
    const samePiecePractice = pieces.filter((p) => p.id.startsWith(`${d.piece}_`));
    menuEl.innerHTML =
      scoreItems.map((p) => `
        <li class="${p.id.startsWith("full_score") ? "full" : ""}">
          <a href="${base}#${p.id}">
            <span class="name">${p.label}</span>
            <span class="sub">${p.desc}${p.seconds ? " · " + fmt(p.seconds) : ""}</span>
          </a>
        </li>`).join("") +
      samePiecePractice.map((p) => `
        <li class="practice">
          <a href="#${p.id}"${p.id === id ? ' aria-current="page"' : ""}>
            <span class="name">${p.partLabel} 연습</span>
            <span class="sub">운지 · 타임라인 · 구간 반복</span>
          </a>
        </li>`).join("");
  }
  return { base, partMeta: scoreItems.find((p) => p.id === d.part) || null };
}

async function load(id) {
  const token = ++loadToken;
  cancelCountIn();
  audio.pause();
  const d = await getJSON(`data/${id}.json`);
  const [inst, svgText] = await loadInstrument(d.instrument);
  if (token !== loadToken) return;   // 그 사이 다른 곡을 골랐다

  data = d;
  labels = Object.fromEntries(inst.keyList.map((k) => [k.id, k.label]));
  fingeringEl.innerHTML = svgText;
  keyEls = {};
  fingeringEl.querySelectorAll(".key[id]").forEach((el) => { keyEls[el.id] = el; });

  const { base, partMeta } = await buildSidebarMenu(d, id);
  if (token !== loadToken) return;

  document.title = `${d.partLabel} 연습 · ${d.title}`;
  const info = PIECE_INFO[d.piece] || { title: d.title, sub: "", meta: "" };
  $("pieceTitle").textContent = info.title;
  $("pieceSub").textContent = info.sub;
  $("sidebarMeta").textContent = info.meta;
  if ($("title")) $("title").textContent = `${d.partLabel} 연습`;
  if ($("desc")) $("desc").textContent = partMeta ? partMeta.desc : `${d.title} · 운지 연습`;
  if ($("dl-pdf") && partMeta) $("dl-pdf").href = `${base}${partMeta.pdf}`;
  if ($("dl-mp3")) $("dl-mp3").href = d.mp3;
  $("scoreLink").href = d.score;
  pieceSelect.value = id;
  const uniqueSongs = new Set(pieces.map((p) => p.id.split("_")[0])).size;
  if ($("pieceSelectWrap")) $("pieceSelectWrap").hidden = uniqueSongs <= 1;
  fillMeasureSelect(loopStartSel, d.measures.length, 1);
  fillMeasureSelect(loopEndSel, d.measures.length, d.measures.length);

  seek.max = String(Math.round(d.seconds * 1000));
  pendingSeekSec = null;
  audio.src = d.mp3 + V;
  audio.playbackRate = rate;
  audio.preservesPitch = true;
  audio.currentTime = 0;
  lastKey = null;
  curMeasure = -2;
  curRow = "";
  marker.hidden = true;
  const titleArtHtml = d.piece === "blue" ? "그대 안의<br>블루"
    : d.piece === "youraisemeup" ? "You Raise<br>Me Up"
    : d.piece === "cinema" ? "Cinema<br>Paradiso"
    : d.title;
  const wideCover = d.piece === "youraisemeup" ? " wide" : d.piece === "cinema" ? " wider" : "";
  scorePagesEl.innerHTML = (d.pages || []).map((src, i) =>
    `<div class="page"><img src="${src}${V}" alt="${d.title} ${d.partLabel} 악보 ${i + 1}쪽" loading="${i ? "lazy" : "eager"}">` +
    (i === 0 ? `<div class="title-cover${wideCover}"></div><div class="title-art${wideCover}"><img src="${base}logo.png" alt=""><span>${titleArtHtml}</span></div>` : "") +
    `</div>`
  ).join("");
  scorePagesEl.scrollTop = 0;
  buildTimeline();
  syncPlayButton();
}

function currentId() {
  const h = decodeURIComponent(location.hash.slice(1));
  return pieces.some((p) => p.id === h) ? h : pieces[0].id;
}

pieceSelect.addEventListener("change", () => { location.hash = pieceSelect.value; });
window.addEventListener("hashchange", () => load(currentId()).catch(showError));
audio.addEventListener("ratechange", () => { audio.preservesPitch = true; });

function showError(err) {
  console.error(err);
  $("nextText").textContent = "불러오기에 실패했어요. 새로고침해 보세요.";
}

(async () => {
  pieces = await getJSON("pieces.json");
  pieces.forEach((p) => pieceSelect.append(new Option(`${p.title} · ${p.partLabel}`, p.id)));
  await load(currentId());
  requestAnimationFrame(frame);
})().catch(showError);
