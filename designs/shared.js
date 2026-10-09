// Time-of-day SMPTE timecode at 24fps, like a slate on set.
(function () {
  const els = document.querySelectorAll("[data-tc]");
  if (!els.length) return;
  const pad = (n) => String(n).padStart(2, "0");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  function tick() {
    const d = new Date();
    const ff = Math.floor((d.getMilliseconds() / 1000) * 24);
    const s = `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}:<b>${pad(ff)}</b>`;
    els.forEach((el) => (el.innerHTML = "TOD " + s));
    if (!reduce) requestAnimationFrame(tick);
  }
  tick();
  if (reduce) setInterval(tick, 1000);
})();
