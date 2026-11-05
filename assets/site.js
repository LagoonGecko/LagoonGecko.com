// Re-orders product cards on category pages when the sort menu changes.
(function () {
  var sel = document.getElementById("sort");
  if (!sel) return;
  sel.addEventListener("change", function () {
    var grid = document.querySelector(".grid");
    var key = sel.value;
    var cards = Array.prototype.slice.call(grid.children);
    cards.sort(function (a, b) {
      var x = parseFloat(a.dataset[key]), y = parseFloat(b.dataset[key]);
      return key === "price" ? x - y : y - x;
    });
    cards.forEach(function (c) { grid.appendChild(c); });
  });
})();

// Header "Explore" dropdown menu
(function () {
  var btn = document.querySelector(".menubtn");
  var panel = document.getElementById("menupanel");
  if (!btn || !panel) return;
  function setOpen(open) {
    panel.hidden = !open;
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  }
  btn.addEventListener("click", function (ev) {
    ev.stopPropagation();
    setOpen(panel.hidden);
  });
  document.addEventListener("click", function (ev) {
    if (!panel.hidden && !panel.contains(ev.target)) setOpen(false);
  });
  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape" && !panel.hidden) { setOpen(false); btn.focus(); }
  });
  panel.addEventListener("click", function (ev) {
    if (ev.target.tagName === "A") setOpen(false);
  });
})();

// Darken the vignette header slightly once the page is scrolled
(function () {
  var top = document.querySelector(".top");
  if (!top) return;
  function onScroll() { top.classList.toggle("scrolled", window.scrollY > 40); }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
})();

// Front-page guide slider: auto-advances every 2 seconds, arrows and dots to click through
(function () {
  var box = document.querySelector(".gslider");
  if (!box) return;
  var slides = box.querySelectorAll(".gs-slide");
  var dots = box.querySelectorAll(".gs-dot");
  if (slides.length < 2) return;
  var i = 0, paused = false, timer;
  function show(n) {
    slides[i].classList.remove("active"); slides[i].tabIndex = -1; slides[i].setAttribute("aria-hidden", "true");
    if (dots[i]) dots[i].classList.remove("active");
    i = (n + slides.length) % slides.length;
    slides[i].classList.add("active"); slides[i].tabIndex = 0; slides[i].setAttribute("aria-hidden", "false");
    if (dots[i]) dots[i].classList.add("active");
  }
  function restart() { clearInterval(timer); timer = setInterval(function () { if (!paused && !document.hidden) show(i + 1); }, 2000); }
  box.querySelector(".gs-next").addEventListener("click", function () { show(i + 1); restart(); });
  box.querySelector(".gs-prev").addEventListener("click", function () { show(i - 1); restart(); });
  dots.forEach(function (d, n) { d.addEventListener("click", function () { show(n); restart(); }); });
  box.addEventListener("mouseenter", function () { paused = true; });
  box.addEventListener("mouseleave", function () { paused = false; });
  box.addEventListener("focusin", function () { paused = true; });
  box.addEventListener("focusout", function () { paused = false; });
  restart();
})();
