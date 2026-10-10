/* 강의록 페이지에서 직접 고치고, 고친 내용을 내려받아 다시 집필에 넣는다.
   저장은 브라우저 안에서만 일어나고 서버로 가지 않는다. */
(function () {
  "use strict";

  var main = document.querySelector("main.lesson[data-lesson]");
  if (!main) return;

  var LID = main.getAttribute("data-lesson");
  var KEY = "lessonedit:" + LID;
  var SEL = "p, li, figcaption, td, th, summary";
  var SKIP = "nav, .crumb, .pager, .dl, .editbar, .editnote";

  /* ---------------------------------------------------------------- 저장소 */

  function blank() { return { edits: {}, memos: {}, note: "" }; }

  function load() {
    try {
      var raw = localStorage.getItem(KEY);
      var o = raw ? JSON.parse(raw) : blank();
      o.edits = o.edits || {};
      o.memos = o.memos || {};
      o.note = o.note || "";
      return o;
    } catch (e) {
      return blank();
    }
  }

  function save() {
    try {
      localStorage.setItem(KEY, JSON.stringify(store));
    } catch (e) {
      flash("저장 공간이 없어 이번 수정은 기억되지 않는다. 지금 내려받기 바란다.");
    }
  }

  var store = load();

  /* ------------------------------------------------------------- 요소 식별 */

  var items = [];                     // {el, id, ctx, nth, text, html}
  var byId = {};
  var ctxList = [];                   // 본문에 있는 절 제목의 순서

  function indexElements() {
    var ctx = "머리말";
    var nth = {};
    var all = main.querySelectorAll("*");
    for (var i = 0; i < all.length; i++) {
      var el = all[i];
      if (el.closest(SKIP)) continue;
      if (el.tagName === "H2" || el.tagName === "H3") {
        ctx = el.textContent.trim();
        el.setAttribute("data-ctx", ctx);
        if (ctxList.indexOf(ctx) < 0) ctxList.push(ctx);
        continue;
      }
      if (!el.matches(SEL)) continue;
      if (el.querySelector(SEL)) continue;          // 잎 노드만 고친다
      if (!el.textContent.trim()) continue;
      nth[ctx] = (nth[ctx] || 0) + 1;
      var it = {
        el: el, ctx: ctx, nth: nth[ctx], id: ctx + "#" + nth[ctx],
        text: el.textContent.trim(), html: el.innerHTML.trim()
      };
      el.setAttribute("data-eid", it.id);
      items.push(it);
      byId[it.id] = it;
    }
  }

  function headingFor(ctx) {
    return main.querySelector('[data-ctx="' + ctx.replace(/"/g, '\\"') + '"]');
  }

  /* --------------------------------------------------------- 저장분 되살림 */

  var stale = 0;

  function restore() {
    Object.keys(store.edits).forEach(function (id) {
      var rec = store.edits[id];
      var it = byId[id];
      if (!it) { rec.stale = true; stale++; return; }
      if (it.text === rec.to) { it.el.classList.add("is-edited"); return; }
      if (it.text !== rec.from) { rec.stale = true; stale++; return; }
      it.el.innerHTML = rec.toHtml || esc(rec.to);
      it.el.classList.add("is-edited");
    });
    Object.keys(store.memos).forEach(function (ctx) {
      var h = headingFor(ctx);
      if (h) h.classList.add("has-memo");
    });
  }

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function count() {
    return Object.keys(store.edits).length + Object.keys(store.memos).length +
      (store.note.trim() ? 1 : 0);
  }

  /* ------------------------------------------------------------------- UI */

  var bar, editing = false;

  function build() {
    bar = document.createElement("div");
    bar.className = "editbar";
    bar.innerHTML =
      '<button type="button" data-act="toggle" class="editbtn editbtn--main">수정</button>' +
      '<span class="editcount" hidden></span>' +
      '<span class="editgrp" hidden>' +
      '<button type="button" data-act="note" class="editbtn">전체 메모</button>' +
      '<button type="button" data-act="down" class="editbtn">내려받기</button>' +
      '<button type="button" data-act="copy" class="editbtn">복사</button>' +
      '<button type="button" data-act="reset" class="editbtn editbtn--warn">되돌리기</button>' +
      "</span>";
    document.body.appendChild(bar);
    var acts = { toggle: toggle, note: askNote, down: download, copy: copy, reset: reset };
    bar.addEventListener("click", function (ev) {
      var b = ev.target.closest("button[data-act]");
      if (b) acts[b.getAttribute("data-act")]();
    });
    refresh();
  }

  function refresh() {
    var n = count();
    var c = bar.querySelector(".editcount");
    c.hidden = n === 0;
    c.textContent = n
      ? "수정 " + n + "건" + (stale ? " · 본문 개정으로 " + stale + "건 보류" : "")
      : "";
    bar.querySelector(".editgrp").hidden = !(editing || n);
    bar.querySelector('[data-act="toggle"]').textContent = editing ? "편집 끝내기" : "수정";
    bar.classList.toggle("is-on", editing);
  }

  function toggle() {
    editing = !editing;
    document.body.classList.toggle("editing", editing);
    items.forEach(function (it) {
      if (editing) {
        it.el.setAttribute("contenteditable", "true");
        it.el.setAttribute("spellcheck", "false");
      } else {
        it.el.removeAttribute("contenteditable");
      }
    });
    ctxList.forEach(function (ctx) {
      var h = headingFor(ctx);
      if (!h) return;
      var b = h.querySelector(".memobtn");
      if (editing && !b) {
        b = document.createElement("button");
        b.type = "button";
        b.className = "memobtn";
        b.textContent = "메모";
        b.addEventListener("click", function (ev) { ev.preventDefault(); askMemo(ctx); });
        h.appendChild(b);
      } else if (!editing && b) {
        b.remove();
      }
    });
    if (editing) flash("문장을 눌러 그 자리에서 고친다. 절 제목의 '메모'로 지시를 남길 수 있다.");
    refresh();
  }

  function onEdit(ev) {
    if (!editing) return;
    var el = ev.target.closest("[data-eid]");
    if (!el) return;
    var it = byId[el.getAttribute("data-eid")];
    if (!it) return;
    var rec = store.edits[it.id] || { from: it.text, fromHtml: it.html, ctx: it.ctx, nth: it.nth };
    rec.to = el.textContent.trim();
    rec.toHtml = el.innerHTML.trim();
    if (rec.to === rec.from) {
      delete store.edits[it.id];
      el.classList.remove("is-edited");
    } else {
      store.edits[it.id] = rec;
      el.classList.add("is-edited");
    }
    save();
    refresh();
  }

  function askMemo(ctx) {
    ask("'" + ctx + "' 에 남길 메모",
      "고칠 방향, 넣을 그림 주소, 빠진 내용 등을 적는다. 여러 줄도 된다.",
      store.memos[ctx] || "",
      function (v) {
        var h = headingFor(ctx);
        if (v) {
          store.memos[ctx] = v;
          if (h) h.classList.add("has-memo");
        } else {
          delete store.memos[ctx];
          if (h) h.classList.remove("has-memo");
        }
        save();
        refresh();
      });
  }

  function askNote() {
    ask("이 수업 전체에 대한 메모",
      "구성, 분량, 그림의 방향 등 수업 전체에 걸친 지시를 적는다.",
      store.note,
      function (v) { store.note = v; save(); refresh(); });
  }

  /* --------------------------------------------------- 입력 상자 (자체 모달) */

  function ask(title, hint, value, done) {
    var wrap = document.createElement("div");
    wrap.className = "editmodal";
    wrap.innerHTML =
      '<div class="editmodal__box" role="dialog" aria-modal="true" aria-label="' +
      esc(title) + '">' +
      "<h3></h3><p></p><textarea rows=\"6\" spellcheck=\"false\"></textarea>" +
      '<div class="editmodal__row">' +
      '<button type="button" class="editbtn" data-k="cancel">취소</button>' +
      '<button type="button" class="editbtn editbtn--main" data-k="ok">넣기</button>' +
      "</div></div>";
    wrap.querySelector("h3").textContent = title;
    wrap.querySelector("p").textContent = hint;
    var ta = wrap.querySelector("textarea");
    ta.value = value || "";
    document.body.appendChild(wrap);
    ta.focus();

    function close(ok) {
      var v = ta.value.trim();
      wrap.remove();
      if (ok) done(v);
    }
    wrap.addEventListener("click", function (ev) {
      if (ev.target === wrap) return close(false);
      var b = ev.target.closest("button[data-k]");
      if (b) close(b.getAttribute("data-k") === "ok");
    });
    wrap.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape") close(false);
      else if (ev.key === "Enter" && (ev.metaKey || ev.ctrlKey)) close(true);
    });
  }

  function askYes(msg, done) {
    var wrap = document.createElement("div");
    wrap.className = "editmodal";
    wrap.innerHTML =
      '<div class="editmodal__box" role="dialog" aria-modal="true">' +
      "<h3>확인</h3><p></p>" +
      '<div class="editmodal__row">' +
      '<button type="button" class="editbtn" data-k="cancel">취소</button>' +
      '<button type="button" class="editbtn editbtn--warn" data-k="ok">지운다</button>' +
      "</div></div>";
    wrap.querySelector("p").textContent = msg;
    document.body.appendChild(wrap);
    wrap.querySelector('[data-k="cancel"]').focus();
    wrap.addEventListener("click", function (ev) {
      if (ev.target === wrap) return wrap.remove();
      var b = ev.target.closest("button[data-k]");
      if (!b) return;
      var ok = b.getAttribute("data-k") === "ok";
      wrap.remove();
      if (ok) done();
    });
    wrap.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape") wrap.remove();
    });
  }

  /* ------------------------------------------------------------ 내보내기 */

  function oneline(s) { return String(s).replace(/\s+/g, " ").trim(); }

  /* 원문·수정문은 lesson.md 와 같은 표기로 내보낸다. 그래야 집필에서 바로 찾아 고친다. */
  function asMarkdown(html, text) {
    if (!html) return oneline(text || "");
    var d = document.createElement("div");
    d.innerHTML = html;
    d.querySelectorAll("b, strong").forEach(function (e) {
      e.replaceWith("**" + e.textContent + "**");
    });
    d.querySelectorAll("i, em").forEach(function (e) {
      e.replaceWith("*" + e.textContent + "*");
    });
    d.querySelectorAll("code, kbd").forEach(function (e) {
      e.replaceWith("`" + e.textContent + "`");
    });
    d.querySelectorAll("br").forEach(function (e) { e.replaceWith(" "); });
    return oneline(d.textContent);
  }

  function build_md() {
    var today = new Date().toISOString().slice(0, 10);
    var out = ["## " + LID, ""];
    out.push(today + " 강의록 페이지에서 직접 고친 내용이다. 원문을 수정문으로 바꾼다.");
    out.push("");

    if (store.note) out.push("- [수업 전체] " + oneline(store.note));

    Object.keys(store.edits)
      .map(function (id) { return store.edits[id]; })
      .sort(function (a, b) {
        if (a.ctx !== b.ctx) return ctxList.indexOf(a.ctx) - ctxList.indexOf(b.ctx);
        return a.nth - b.nth;
      })
      .forEach(function (r) {
        out.push("- [" + r.ctx + " · " + r.nth + "번째 문장] " +
          (r.stale ? "(본문이 개정되어 위치 확인 필요) " : "") +
          "원문: " + asMarkdown(r.fromHtml, r.from) +
          "  →  수정문: " + asMarkdown(r.toHtml, r.to));
      });

    Object.keys(store.memos)
      .sort(function (a, b) { return ctxList.indexOf(a) - ctxList.indexOf(b); })
      .forEach(function (ctx) {
        out.push("- [" + ctx + " · 메모] " + oneline(store.memos[ctx]));
      });

    out.push("");
    return out.join("\n") + "\n";
  }

  function download() {
    if (!count()) { flash("내려받을 수정이 없다."); return; }
    var a = document.createElement("a");
    a.href = URL.createObjectURL(
      new Blob([build_md()], { type: "text/markdown;charset=utf-8" }));
    a.download = "inbox-" + LID + "-" + new Date().toISOString().slice(0, 10) + ".md";
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
    flash("내려받았다. 저장소의 inbox/ 에 넣고 tools/inbox.py 를 돌리거나 대화창에 올리면 된다.");
  }

  function copy() {
    if (!count()) { flash("복사할 수정이 없다."); return; }
    var md = build_md();
    if (!navigator.clipboard || !window.isSecureContext) { dump(md); return; }

    /* 권한이 막히면 약속이 끝나지 않는 브라우저가 있어 기다리는 시간을 둔다. */
    var settled = false;
    var timer = setTimeout(function () {
      if (!settled) { settled = true; dump(md); }
    }, 1500);
    navigator.clipboard.writeText(md).then(function () {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      flash("클립보드에 복사했다. 그대로 붙여 넣으면 된다.");
    }, function () {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      dump(md);
    });
  }

  function dump(md) {
    var old = document.querySelector(".editdump");
    if (old) old.remove();
    var t = document.createElement("textarea");
    t.value = md;
    t.className = "editdump";
    t.readOnly = true;
    document.body.appendChild(t);
    t.focus();
    t.select();
    flash("복사가 막혀 있어 상자에 띄웠다. 상자의 내용을 직접 복사한다.");
  }

  function reset() {
    if (!count()) { flash("되돌릴 수정이 없다."); return; }
    askYes("이 수업에 해 둔 수정 " + count() + "건을 모두 지운다. 내려받지 않은 것은 사라진다.",
      function () {
        try { localStorage.removeItem(KEY); } catch (e) { /* 무시 */ }
        store = blank();
        location.reload();
      });
  }

  /* ---------------------------------------------------------------- 알림 */

  var noteEl;

  function flash(msg) {
    if (!noteEl) {
      noteEl = document.createElement("div");
      noteEl.className = "editnote";
      noteEl.setAttribute("role", "status");
      document.body.appendChild(noteEl);
    }
    noteEl.textContent = msg;
    noteEl.classList.add("is-on");
    clearTimeout(flash.t);
    flash.t = setTimeout(function () { noteEl.classList.remove("is-on"); }, 6000);
  }

  /* ---------------------------------------------------------------- 시작 */

  indexElements();
  restore();
  build();
  main.addEventListener("input", onEdit);
})();
