(async function () {
  const $ = (id) => document.getElementById(id);
  const audio = $("audio"), play = $("play"), seek = $("seek"), time = $("time"), pagesEl = $("pages");
  const fmt = (s) => !isFinite(s) ? "0:00" : `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`;

  let pieces, cur = null, curMeasure = -1, curRow = "", raf = 0;
  try {
    pieces = await (await fetch("manifest.json")).json();
  } catch (e) {
    $("title").textContent = "목록을 불러오지 못했어요";
    return;
  }

  $("menu").innerHTML = pieces.map((p) => `
    <li class="${p.id.startsWith("full_score") ? "full" : ""}">
      <a href="#${p.id}" data-id="${p.id}">
        <span class="name">${p.label}</span>
        <span class="sub">${p.desc}${p.seconds ? " · " + fmt(p.seconds) : ""}</span>
      </a>
    </li>`).join("");

  // ---------- 마디 표시 ----------
  const marker = document.createElement("div");
  marker.className = "marker";
  marker.hidden = true;

  function measureAt(ms) {
    const ms_ = cur.measures;
    let i = -1;
    for (let k = 0; k < ms_.length && ms_[k].ms <= ms; k++) i = k;
    return i;
  }

  function placeMarker(i) {
    if (i === curMeasure) return;
    curMeasure = i;
    if (i < 0) { marker.hidden = true; return; }
    const m = cur.measures[i];
    const page = pagesEl.children[m.page];
    if (!page) return;
    if (marker.parentNode !== page) page.appendChild(marker);
    Object.assign(marker.style, {
      left: `${m.l}%`, top: `calc(${m.t}% - 12px)`, width: `${m.w}%`, height: `calc(${m.h}% + 24px)`,
    });
    marker.dataset.bar = i + 1;
    marker.hidden = false;
    // 같은 줄 안에서 오른쪽으로 이동할 때는 그대로 두고, 줄이 바뀔 때만 화면 중앙으로 맞춘다
    const row = `${m.page}:${m.t}`;
    if (row !== curRow) {
      curRow = row;
      centerMarker(page, m);
    }
  }

  // 표시 상자가 움직일 때마다 플레이어 아래 보이는 영역의 세로 중앙에 오도록 스크롤.
  // 상자는 CSS 전환 효과로 움직이므로, 현재 위치가 아닌 도착 위치(마디 좌표)로 계산한다.
  function centerMarker(page, m) {
    const pr = page.getBoundingClientRect();
    const mid = pr.top + pr.height * (m.t + m.h / 2) / 100;
    // 스크롤 후에는 플레이어가 화면 맨 위에 고정되므로, 고정된 상태의 높이를 기준으로 한다
    const top = document.querySelector(".player").offsetHeight;
    const target = top + (window.innerHeight - top) / 2;
    const delta = mid - target;
    if (Math.abs(delta) > 4) window.scrollBy({ top: delta, behavior: "smooth" });
  }

  function tick() {
    placeMarker(measureAt(audio.currentTime * 1000));
    if (audio.duration) seek.value = (audio.currentTime / audio.duration) * 100;
    time.textContent = `${fmt(audio.currentTime)} / ${fmt(audio.duration || cur.seconds)}`;
    if (!audio.paused) raf = requestAnimationFrame(tick);
  }

  // 악보에서 마디를 누르면 그 마디부터 재생
  pagesEl.addEventListener("click", (e) => {
    const page = e.target.closest(".page");
    if (!page) return;
    const pi = [...pagesEl.children].indexOf(page);
    const rect = page.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    const pad = (12 / rect.height) * 100;
    const i = cur.measures.findIndex((m) => m.page === pi &&
      x >= m.l && x <= m.l + m.w && y >= m.t - pad && y <= m.t + m.h + pad);
    if (i < 0) return;
    audio.currentTime = cur.measures[i].ms / 1000;
    curMeasure = -1;
    tick();
    audio.play();
  });

  // ---------- 화면 전환 ----------
  function show(id) {
    const p = pieces.find((x) => x.id === id) || pieces[0];
    cur = p;
    document.querySelectorAll(".menu a").forEach((a) => a.removeAttribute("aria-current"));
    document.querySelector(`.menu a[data-id="${p.id}"]`).setAttribute("aria-current", "page");
    document.title = `${p.label} · You Raise Me Up`;
    $("title").textContent = p.label;
    $("desc").textContent = p.desc;
    $("dl-pdf").href = p.pdf;
    $("dl-mp3").href = p.mp3;

    audio.pause();
    audio.src = p.mp3;
    audio.load();
    seek.value = 0;
    time.textContent = `0:00 / ${fmt(p.seconds)}`;

    pagesEl.innerHTML = p.pages.map((src, i) =>
      `<div class="page"><img src="${src}" alt="${p.label} 악보 ${i + 1}쪽" loading="${i ? "lazy" : "eager"}">` +
      (i === 0 ? `<div class="title-cover"></div><div class="title-art"><img src="logo.png" alt=""><span>You Raise<br>Me Up</span></div>` : "") +
      `</div>`).join("");
    curMeasure = -1; curRow = "";
    marker.hidden = true;
    window.scrollTo({ top: 0 });
  }

  play.addEventListener("click", () => (audio.paused ? audio.play() : audio.pause()));
  audio.addEventListener("play", () => {
    play.classList.add("playing");
    play.setAttribute("aria-label", "일시정지");
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(tick);
  });
  audio.addEventListener("pause", () => {
    play.classList.remove("playing");
    play.setAttribute("aria-label", "재생");
    tick();
  });
  audio.addEventListener("ended", () => { curMeasure = -1; curRow = ""; marker.hidden = true; });
  audio.addEventListener("seeked", tick);
  seek.addEventListener("input", () => {
    if (audio.duration) audio.currentTime = (seek.value / 100) * audio.duration;
  });
  document.addEventListener("keydown", (e) => {
    if (e.code === "Space" && !["INPUT", "BUTTON", "A"].includes(document.activeElement.tagName)) {
      e.preventDefault();
      play.click();
    }
  });

  window.addEventListener("hashchange", () => show(location.hash.slice(1)));
  show(location.hash.slice(1));
})();
