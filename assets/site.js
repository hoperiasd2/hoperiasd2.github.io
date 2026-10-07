/* 수업 목록 검색과 필터. 스크립트가 없어도 전체 목록은 그대로 읽힌다. */
(function () {
  "use strict";

  var box = document.querySelector("[data-search]");
  var items = Array.prototype.slice.call(document.querySelectorAll("[data-q]"));
  var countEl = document.querySelector("[data-count]");
  var buttons = Array.prototype.slice.call(document.querySelectorAll("[data-filter]"));
  if (!items.length) return;

  var activeFilter = "";

  function apply() {
    var q = box ? box.value.trim().toLowerCase() : "";
    var shown = 0;
    items.forEach(function (el) {
      var hay = (el.getAttribute("data-q") || "").toLowerCase();
      var mod = el.getAttribute("data-module") || "";
      var okText = !q || hay.indexOf(q) !== -1;
      var okFilter = !activeFilter || mod === activeFilter;
      var ok = okText && okFilter;
      el.hidden = !ok;
      if (ok) shown++;
    });
    if (countEl) countEl.textContent = shown + "개 수업";
    // 비어 버린 묶음 제목을 감춘다.
    document.querySelectorAll("[data-section]").forEach(function (sec) {
      var any = sec.querySelector("[data-q]:not([hidden])");
      sec.hidden = !any;
    });
  }

  if (box) {
    box.addEventListener("input", apply);
    box.addEventListener("search", apply);
  }

  buttons.forEach(function (b) {
    b.addEventListener("click", function () {
      var v = b.getAttribute("data-filter");
      activeFilter = activeFilter === v ? "" : v;
      buttons.forEach(function (o) {
        o.setAttribute("aria-pressed", String(o.getAttribute("data-filter") === activeFilter));
      });
      apply();
    });
  });

  apply();
})();
