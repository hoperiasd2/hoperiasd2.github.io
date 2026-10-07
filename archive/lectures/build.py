#!/usr/bin/env python3
"""강의록 빌더.

src/bNN.md 원고(간단한 마크업)를 읽어 다음을 생성한다.
  lectures/index.html            전체 목록 (10묶음)
  lectures/bNN/index.html        묶음별 목록
  lectures/bNN/lMM.html          강의록 HTML
  lectures/bNN/ppt/bNN-lMM.pptx  강의록 PPT

실행:  python3 lectures/build.py
원고 문법은 lectures/README.md 참고.
"""
from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

# --------------------------------------------------------------------------
# 원고 파서
# --------------------------------------------------------------------------


@dataclass
class Section:
    title: str
    blocks: list = field(default_factory=list)  # (kind, payload)


@dataclass
class Lecture:
    no: int
    meta: dict
    objectives: list = field(default_factory=list)
    sections: list = field(default_factory=list)
    frontier: list = field(default_factory=list)
    summary: list = field(default_factory=list)
    quiz: list = field(default_factory=list)  # (q, a)
    refs: list = field(default_factory=list)
    bundle: "Bundle" = None

    @property
    def code(self):
        return f"{self.bundle.code}-L{self.no:02d}"

    @property
    def slug(self):
        return f"l{self.no:02d}"

    @property
    def ppt_name(self):
        return f"b{self.bundle.no:02d}-l{self.no:02d}.pptx"


@dataclass
class Bundle:
    no: int
    meta: dict
    lectures: list = field(default_factory=list)

    @property
    def code(self):
        return f"B{self.no:02d}"

    @property
    def slug(self):
        return f"b{self.no:02d}"


def parse_blocks(lines):
    """섹션 본문 줄들을 블록 리스트로 변환."""
    blocks = []
    para = []
    ul = None
    table = None

    def flush():
        nonlocal para, ul, table
        if para:
            blocks.append(("p", " ".join(para)))
            para = []
        if ul is not None:
            blocks.append(("ul", ul))
            ul = None
        if table is not None:
            blocks.append(("table", table))
            table = None

    for raw in lines:
        line = raw.rstrip()
        s = line.strip()
        if not s:
            flush()
            continue
        if s.startswith("|"):
            if table is None:
                flush()
                table = []
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                continue
            table.append(cells)
            continue
        m = re.match(r"^(\s*)- (.*)$", line)
        if m:
            if ul is None:
                flush()
                ul = []
            level = 1 if len(m.group(1)) >= 2 else 0
            ul.append((level, m.group(2).strip()))
            continue
        if s.startswith("!> "):
            flush()
            blocks.append(("key", s[3:].strip()))
            continue
        if s.startswith("> "):
            flush()
            blocks.append(("clin", s[2:].strip()))
            continue
        if ul is not None and raw.startswith("    "):
            # 이전 bullet의 연속 줄
            lvl, txt = ul[-1]
            ul[-1] = (lvl, txt + " " + s)
            continue
        if table is not None:
            flush()
        if ul is not None:
            flush()
        para.append(s)
    flush()
    return blocks


def parse_list(lines):
    out = []
    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        if s.startswith("- "):
            out.append(s[2:].strip())
        elif out:
            out[-1] += " " + s
        else:
            out.append(s)
    return out


def parse_quiz(lines):
    out = []
    q = a = None
    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        if s.startswith("Q:"):
            if q:
                out.append((q, a or ""))
            q, a = s[2:].strip(), None
        elif s.startswith("A:"):
            a = s[2:].strip()
        elif a is not None:
            a += " " + s
        elif q is not None:
            q += " " + s
    if q:
        out.append((q, a or ""))
    return out


def parse_meta(lines):
    meta = {}
    for raw in lines:
        m = re.match(r"^([a-z_]+):\s*(.*)$", raw.strip())
        if m:
            meta[m.group(1)] = m.group(2).strip()
    return meta


def parse_bundle(paths) -> Bundle:
    path = paths[0]
    text = "\n".join(p.read_text(encoding="utf-8") for p in paths)
    parts = re.split(r"^### +L(\d+)\s*$", text, flags=re.M)
    head = parts[0]
    m = re.search(r"^=== +B(\d+)\s*$", head, flags=re.M)
    if not m:
        raise SystemExit(f"{path}: '=== Bnn' 헤더가 없습니다")
    bundle = Bundle(no=int(m.group(1)), meta=parse_meta(head[m.end():].splitlines()))
    for i in range(1, len(parts), 2):
        no = int(parts[i])
        body = parts[i + 1]
        chunks = re.split(r"^@(\w+)[ \t]*(.*)$", body, flags=re.M)
        lec = Lecture(no=no, meta=parse_meta(chunks[0].splitlines()), bundle=bundle)
        for j in range(1, len(chunks), 3):
            tag, arg, content = chunks[j], chunks[j + 1].strip(), chunks[j + 2].splitlines()
            if tag == "obj":
                lec.objectives = parse_list(content)
            elif tag == "sec":
                lec.sections.append(Section(arg, parse_blocks(content)))
            elif tag == "frontier":
                lec.frontier = parse_list(content)
            elif tag == "summary":
                lec.summary = parse_list(content)
            elif tag == "quiz":
                lec.quiz = parse_quiz(content)
            elif tag == "ref":
                lec.refs = parse_list(content)
            else:
                raise SystemExit(f"{path} L{no}: 알 수 없는 태그 @{tag}")
        for req in ("title",):
            if req not in lec.meta:
                raise SystemExit(f"{path} L{no}: {req} 누락")
        bundle.lectures.append(lec)
    bundle.lectures.sort(key=lambda l: l.no)
    return bundle


# --------------------------------------------------------------------------
# HTML
# --------------------------------------------------------------------------

def inline(text: str) -> str:
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    t = re.sub(r"\^\{(.+?)\}", r"<sup>\1</sup>", t)
    t = re.sub(r"_\{(.+?)\}", r"<sub>\1</sub>", t)
    return t


def plain(text: str) -> str:
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\1", t)
    t = re.sub(r"\^\{(.+?)\}", r"\1", t)
    t = re.sub(r"_\{(.+?)\}", r"\1", t)
    return t


def render_ul(items):
    out = ["<ul>"]
    open_sub = False
    for i, (lvl, txt) in enumerate(items):
        if lvl == 0:
            if open_sub:
                out.append("</ul></li>")
                open_sub = False
            elif i > 0:
                out.append("</li>")
            out.append(f"<li>{inline(txt)}")
        else:
            if not open_sub:
                out.append("<ul>")
                open_sub = True
            out.append(f"<li>{inline(txt)}</li>")
    if open_sub:
        out.append("</ul></li>")
    elif items:
        out.append("</li>")
    out.append("</ul>")
    return "".join(out)


def render_blocks(blocks):
    out = []
    for kind, payload in blocks:
        if kind == "p":
            out.append(f"<p>{inline(payload)}</p>")
        elif kind == "ul":
            out.append(render_ul(payload))
        elif kind == "table":
            head, *rows = payload
            t = ['<div class="tbl"><table><thead><tr>']
            t += [f"<th>{inline(c)}</th>" for c in head]
            t.append("</tr></thead><tbody>")
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t))
        elif kind == "clin":
            out.append(f'<aside class="box box--clin"><b>임상 연계</b><p>{inline(payload)}</p></aside>')
        elif kind == "key":
            out.append(f'<aside class="box box--key"><b>핵심</b><p>{inline(payload)}</p></aside>')
    return "\n".join(out)


def page(title, body, depth, desc=""):
    pre = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="stylesheet" href="{pre}assets/lecture.css">
</head>
<body>
<header class="mast">
  <div class="mast__in">
    <a class="mast__home" href="{pre}index.html">의생명 강의록 아카이브</a>
    <a class="mast__site" href="{pre}../index.html">KimjintaeHYU</a>
  </div>
</header>
{body}
<footer class="foot">
  <span>의학생화학 · 의학분자생물학 · 신경과학 강의록</span>
  <a href="{pre}index.html">전체 목록</a>
</footer>
<script src="{pre}assets/lecture.js"></script>
</body>
</html>
"""


def lecture_html(lec: Lecture, prev, nxt):
    b = lec.bundle
    m = lec.meta
    toc = ['<li><a href="#obj">학습 목표</a></li>']
    body = []
    body.append('<section id="obj" class="sec"><h2>학습 목표</h2><ol class="obj">'
                + "".join(f"<li>{inline(o)}</li>" for o in lec.objectives) + "</ol></section>")
    for i, s in enumerate(lec.sections, 1):
        sid = f"s{i}"
        toc.append(f'<li><a href="#{sid}">{i}. {inline(s.title)}</a></li>')
        body.append(f'<section id="{sid}" class="sec"><h2><span class="sec__no">{i}</span>{inline(s.title)}</h2>'
                    f"{render_blocks(s.blocks)}</section>")
    if lec.frontier:
        toc.append('<li><a href="#frontier">연구 최전선</a></li>')
        body.append('<section id="frontier" class="sec sec--frontier"><h2>연구 최전선</h2>'
                    + render_ul([(0, x) for x in lec.frontier]) + "</section>")
    if lec.summary:
        toc.append('<li><a href="#summary">요약</a></li>')
        body.append('<section id="summary" class="sec sec--summary"><h2>요약</h2>'
                    + render_ul([(0, x) for x in lec.summary]) + "</section>")
    if lec.quiz:
        toc.append('<li><a href="#quiz">자가 평가</a></li>')
        qs = "".join(
            f'<li><p class="q">{inline(q)}</p><details><summary>해설 보기</summary><p>{inline(a)}</p></details></li>'
            for q, a in lec.quiz)
        body.append(f'<section id="quiz" class="sec"><h2>자가 평가</h2><ol class="quiz">{qs}</ol></section>')
    if lec.refs:
        toc.append('<li><a href="#ref">참고 문헌</a></li>')
        body.append('<section id="ref" class="sec sec--ref"><h2>참고 문헌</h2><ul>'
                    + "".join(f"<li>{inline(r)}</li>" for r in lec.refs) + "</ul></section>")

    nav = ['<nav class="pn">']
    nav.append(f'<a class="pn__prev" href="{prev.slug}.html"><small>이전</small>{inline(prev.meta["title"])}</a>'
               if prev else "<span></span>")
    nav.append(f'<a class="pn__next" href="{nxt.slug}.html"><small>다음</small>{inline(nxt.meta["title"])}</a>'
               if nxt else "<span></span>")
    nav.append("</nav>")

    group = m.get("group", "")
    html_body = f"""
<main class="lec">
  <div class="crumb"><a href="../index.html">전체</a> / <a href="index.html">{b.code} {html.escape(b.meta['title'])}</a>{' / ' + html.escape(group) if group else ''}</div>
  <header class="hero">
    <div class="hero__code">{lec.code}</div>
    <h1>{inline(m['title'])}</h1>
    <p class="hero__en">{html.escape(m.get('en', ''))}</p>
    <div class="hero__meta">
      {'<span class="chip">' + html.escape(group) + '</span>' if group else ''}
      <span class="chip">본문 {len(lec.sections)}개 절</span>
      <span class="chip">자가평가 {len(lec.quiz)}문항</span>
      <a class="btn" href="ppt/{lec.ppt_name}" download>PPT 내려받기</a>
      <button class="btn btn--ghost" type="button" onclick="window.print()">인쇄 / PDF</button>
    </div>
  </header>
  <div class="lec__grid">
    <aside class="toc"><div class="toc__in"><b>목차</b><ol>{''.join(toc)}</ol></div></aside>
    <article class="doc">
{chr(10).join(body)}
{''.join(nav)}
    </article>
  </div>
</main>"""
    return page(f"{lec.code} {plain(m['title'])}", html_body, 1, m.get("en", ""))


def bundle_html(b: Bundle, prev_b, next_b):
    groups = {}
    for lec in b.lectures:
        groups.setdefault(lec.meta.get("group", ""), []).append(lec)
    out = []
    for g, lecs in groups.items():
        if g:
            out.append(f'<h2 class="grp">{html.escape(g)}</h2>')
        out.append('<ol class="lst">')
        for lec in lecs:
            out.append(
                f'<li class="lst__item"><span class="lst__code">{lec.code}</span>'
                f'<a class="lst__title" href="{lec.slug}.html">{inline(lec.meta["title"])}'
                f'<small>{html.escape(lec.meta.get("en", ""))}</small></a>'
                f'<a class="lst__dl" href="{lec.slug}.html">HTML</a>'
                f'<a class="lst__dl" href="ppt/{lec.ppt_name}" download>PPT</a></li>')
        out.append("</ol>")
    nav = '<nav class="pn">'
    nav += (f'<a class="pn__prev" href="../{prev_b.slug}/index.html"><small>이전 묶음</small>{html.escape(prev_b.meta["title"])}</a>'
            if prev_b else "<span></span>")
    nav += (f'<a class="pn__next" href="../{next_b.slug}/index.html"><small>다음 묶음</small>{html.escape(next_b.meta["title"])}</a>'
            if next_b else "<span></span>")
    nav += "</nav>"
    body = f"""
<main class="bnd">
  <div class="crumb"><a href="../index.html">전체</a> / {b.code}</div>
  <header class="hero">
    <div class="hero__code">{b.code} · 강의 {len(b.lectures)}개</div>
    <h1>{html.escape(b.meta['title'])}</h1>
    <p class="hero__en">{html.escape(b.meta.get('en', ''))}</p>
    <p class="hero__desc">{inline(b.meta.get('desc', ''))}</p>
  </header>
  {''.join(out)}
  {nav}
</main>"""
    return page(f"{b.code} {b.meta['title']}", body, 1, b.meta.get("desc", ""))


def index_html(bundles):
    total = sum(len(b.lectures) for b in bundles)
    cards = []
    for b in bundles:
        items = "".join(
            f'<li data-q="{html.escape((plain(l.meta["title"]) + " " + l.meta.get("en", "") + " " + l.meta.get("group", "")).lower())}">'
            f'<span class="lst__code">{l.code}</span>'
            f'<a href="{b.slug}/{l.slug}.html">{inline(l.meta["title"])}</a>'
            f'<a class="mini" href="{b.slug}/ppt/{l.ppt_name}" download title="PPT 내려받기">PPT</a></li>'
            for l in b.lectures)
        cards.append(f"""
  <details class="card" id="{b.slug}">
    <summary>
      <span class="card__no">{b.no:02d}</span>
      <span class="card__t">{html.escape(b.meta['title'])}<small>{html.escape(b.meta.get('en', ''))}</small></span>
      <span class="card__n">{len(b.lectures)}강</span>
    </summary>
    <p class="card__d">{inline(b.meta.get('desc', ''))} <a href="{b.slug}/index.html">묶음 페이지 →</a></p>
    <ol class="card__l">{items}</ol>
  </details>""")
    body = f"""
<main class="idx">
  <header class="hero hero--idx">
    <div class="hero__code">LECTURE ARCHIVE · {len(bundles)}묶음 · {total}강</div>
    <h1>의학생화학 · 분자생물학 · 신경과학 강의록</h1>
    <p class="hero__desc">학부 의학교육부터 연구자 수준까지, 대사·분자·임상·신경과학을 하나의 흐름으로 묶은 강의록입니다.
    모든 강의는 <b>HTML 강의록</b>(학습목표 · 본문 · 임상연계 · 연구 최전선 · 요약 · 자가평가 · 참고문헌)과
    <b>PPT 강의록</b>(발표자 노트 포함)으로 제공됩니다.</p>
    <input id="q" class="search" type="search" placeholder="강의 검색 (예: 요소회로, TREM2, 교모세포종)" autocomplete="off">
  </header>
  <div class="cards">{''.join(cards)}
  </div>
</main>"""
    return page("의생명 강의록 아카이브", body, 0, "의학생화학·의학분자생물학·신경과학 강의록 10묶음")


# --------------------------------------------------------------------------
# PPTX
# --------------------------------------------------------------------------

NAVY = RGBColor(0x00, 0x3C, 0x71)
NAVY_D = RGBColor(0x00, 0x23, 0x43)
CHROME = RGBColor(0xF2, 0xB7, 0x05)
INK = RGBColor(0x11, 0x20, 0x2B)
MUTED = RGBColor(0x66, 0x78, 0x8A)
PAPER = RGBColor(0xF5, 0xF8, 0xF9)
CLIN = RGBColor(0xE8, 0xF1, 0xFA)
KEY = RGBColor(0xFF, 0xF5, 0xD6)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Malgun Gothic"

W, H = Inches(13.333), Inches(7.5)


def set_font(run, size, bold=False, color=INK, italic=False):
    f = run.font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.color.rgb = color
    f.name = FONT
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = rPr.makeelement(qn(tag), {})
            rPr.append(el)
        el.set("typeface", FONT)


def add_rich(paragraph, text, size, color=INK, bold=False):
    """**굵게** 구문을 run 단위로 반영."""
    parts = re.split(r"(\*\*.+?\*\*)", text)
    for part in parts:
        if not part:
            continue
        b = bold
        if part.startswith("**") and part.endswith("**"):
            part, b = part[2:-2], True
        r = paragraph.add_run()
        r.text = plain(part)
        set_font(r, size, bold=b, color=color)


def rect(slide, x, y, w, h, fill, line=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
    s.shadow.inherit = False
    return s


def textbox(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.1)
    tf.margin_top = tf.margin_bottom = Inches(0.05)
    return tf


class Deck:
    def __init__(self, lec: Lecture):
        self.lec = lec
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = W, H
        self.blank = self.prs.slide_layouts[6]
        self.n = 0

    def _base(self, title, kicker=""):
        s = self.prs.slides.add_slide(self.blank)
        self.n += 1
        rect(s, 0, 0, W, H, PAPER)
        rect(s, 0, 0, W, Inches(1.05), NAVY)
        rect(s, 0, Inches(1.05), W, Inches(0.06), CHROME)
        tf = textbox(s, Inches(0.5), Inches(0.12), Inches(12.3), Inches(0.85), MSO_ANCHOR.MIDDLE)
        p = tf.paragraphs[0]
        if kicker:
            r = p.add_run()
            r.text = kicker + "   "
            set_font(r, 14, bold=True, color=CHROME)
        add_rich(p, title, 26 if len(plain(title)) < 34 else 22, color=WHITE, bold=True)
        ftf = textbox(s, Inches(0.5), Inches(7.05), Inches(12.3), Inches(0.35), MSO_ANCHOR.MIDDLE)
        fp = ftf.paragraphs[0]
        r = fp.add_run()
        r.text = f"{self.lec.code}  ·  {plain(self.lec.meta['title'])}"
        set_font(r, 10, color=MUTED)
        r = fp.add_run()
        r.text = f"     {self.n}"
        set_font(r, 10, bold=True, color=NAVY)
        return s

    def notes(self, slide, text):
        if text:
            slide.notes_slide.notes_text_frame.text = plain(text)

    def title_slide(self):
        s = self.prs.slides.add_slide(self.blank)
        self.n += 1
        rect(s, 0, 0, W, H, NAVY_D)
        rect(s, 0, Inches(4.9), W, Inches(0.08), CHROME)
        b = self.lec.bundle
        tf = textbox(s, Inches(0.8), Inches(1.0), Inches(11.7), Inches(0.6))
        r = tf.paragraphs[0].add_run()
        r.text = f"{b.code} {b.meta['title']}" + (f"  ·  {self.lec.meta['group']}" if self.lec.meta.get("group") else "")
        set_font(r, 18, bold=True, color=CHROME)
        tf = textbox(s, Inches(0.8), Inches(1.8), Inches(11.7), Inches(2.2), MSO_ANCHOR.BOTTOM)
        add_rich(tf.paragraphs[0], self.lec.meta["title"], 40 if len(self.lec.meta["title"]) < 26 else 32, WHITE, True)
        p = tf.add_paragraph()
        r = p.add_run()
        r.text = self.lec.meta.get("en", "")
        set_font(r, 20, color=RGBColor(0xC2, 0xCD, 0xD6))
        tf = textbox(s, Inches(0.8), Inches(5.2), Inches(11.7), Inches(1.2))
        r = tf.paragraphs[0].add_run()
        r.text = self.lec.code
        set_font(r, 16, bold=True, color=WHITE)
        p = tf.add_paragraph()
        r = p.add_run()
        r.text = "의학생화학 · 의학분자생물학 · 신경과학 강의록"
        set_font(r, 14, color=RGBColor(0xC2, 0xCD, 0xD6))

    def bullets(self, title, items, kicker="", note="", numbered=False):
        """items: [(level, text)]  — 분량에 따라 여러 장으로 나눔."""
        chunks, cur, size = [], [], 0
        for it in items:
            ln = len(plain(it[1])) + 25
            if cur and (size + ln > 520 or len(cur) >= 7):
                chunks.append(cur)
                cur, size = [], 0
            cur.append(it)
            size += ln
        if cur:
            chunks.append(cur)
        counter = 0
        for ci, chunk in enumerate(chunks):
            t = title + (f" ({ci + 1}/{len(chunks)})" if len(chunks) > 1 else "")
            s = self._base(t, kicker)
            total = sum(len(plain(x[1])) for x in chunk)
            fs = 22 if total < 230 else 20 if total < 330 else 18 if total < 430 else 16
            tf = textbox(s, Inches(0.7), Inches(1.4), Inches(11.9), Inches(5.5))
            first = True
            for lvl, txt in chunk:
                p = tf.paragraphs[0] if first else tf.add_paragraph()
                first = False
                p.space_after = Pt(8 if lvl == 0 else 4)
                if lvl == 0:
                    counter += 1
                    mark = f"{counter}. " if numbered else "▪ "
                    r = p.add_run()
                    r.text = mark
                    set_font(r, fs, bold=True, color=NAVY)
                    add_rich(p, txt, fs)
                else:
                    p.level = 1
                    r = p.add_run()
                    r.text = "    – "
                    set_font(r, fs - 2, color=MUTED)
                    add_rich(p, txt, fs - 2, color=RGBColor(0x2E, 0x3F, 0x4C))
            self.notes(s, note)

    def table(self, title, rows, kicker=""):
        # 행이 많으면 분할
        head, *body = rows
        per = 8
        parts = [body[i:i + per] for i in range(0, len(body), per)] or [[]]
        for pi, part in enumerate(parts):
            t = title + (f" ({pi + 1}/{len(parts)})" if len(parts) > 1 else "")
            s = self._base(t, kicker)
            data = [head] + part
            ncol = max(len(r) for r in data)
            total_chars = sum(len(plain(c)) for r in data for c in r)
            fs = 15 if total_chars < 400 else 13 if total_chars < 650 else 11
            shp = s.shapes.add_table(len(data), ncol, Inches(0.6), Inches(1.4), Inches(12.1), Inches(0.4) * len(data))
            tbl = shp.table
            for ri, r in enumerate(data):
                for cj in range(ncol):
                    cell = tbl.cell(ri, cj)
                    cell.text = ""
                    txt = r[cj] if cj < len(r) else ""
                    p = cell.text_frame.paragraphs[0]
                    add_rich(p, txt, fs, color=WHITE if ri == 0 else INK, bold=(ri == 0))
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = NAVY if ri == 0 else (WHITE if ri % 2 else RGBColor(0xEC, 0xF1, 0xF5))
                    cell.margin_left = cell.margin_right = Inches(0.08)

    def callouts(self, title, items, kicker=""):
        s = self._base(title, kicker)
        total = sum(len(plain(t)) for _, t in items)
        fs = 20 if total < 250 else 18 if total < 400 else 16 if total < 560 else 14
        y = Inches(1.45)
        avail = Inches(5.45)
        weights = [max(len(plain(t)), 60) for _, t in items]
        per_line = int(11.3 * 72 / fs)  # 한글 1자 ≈ 글자 크기 폭
        for (kind, txt), wgt in zip(items, weights):
            share = Emu(int(avail * wgt / sum(weights))) - Inches(0.15)
            lines = (len(plain(txt)) + 8) // per_line + 1
            need = Pt(lines * fs * 1.45) + Inches(0.5)
            h = min(share, need)
            box = rect(s, Inches(0.7), y, Inches(11.9), h, CLIN if kind == "clin" else KEY,
                       line=NAVY if kind == "clin" else CHROME)
            tf = box.text_frame
            tf.word_wrap = True
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf.margin_left = tf.margin_right = Inches(0.25)
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            r = p.add_run()
            r.text = ("임상 연계  " if kind == "clin" else "핵심  ")
            set_font(r, fs, bold=True, color=NAVY if kind == "clin" else RGBColor(0x9A, 0x6B, 0x00))
            add_rich(p, txt, fs)
            y += h + Inches(0.15)

    def quiz(self):
        for i, (q, a) in enumerate(self.lec.quiz, 1):
            s = self._base(f"자가 평가 {i}", "QUIZ")
            tf = textbox(s, Inches(0.7), Inches(1.5), Inches(11.9), Inches(2.4))
            add_rich(tf.paragraphs[0], q, 22 if len(q) < 160 else 18, bold=True)
            box = rect(s, Inches(0.7), Inches(4.1), Inches(11.9), Inches(2.75), WHITE, line=RGBColor(0xC2, 0xCD, 0xD6))
            tf = box.text_frame
            tf.word_wrap = True
            tf.vertical_anchor = MSO_ANCHOR.TOP
            tf.margin_left = tf.margin_right = Inches(0.25)
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            r = p.add_run()
            r.text = "해설  "
            set_font(r, 16, bold=True, color=NAVY)
            add_rich(p, a, 16 if len(a) < 300 else 14, color=RGBColor(0x2E, 0x3F, 0x4C))
            self.notes(s, "해설: " + a)

    def build(self, out: Path):
        lec = self.lec
        self.title_slide()
        self.bullets("학습 목표", [(0, o) for o in lec.objectives], kicker="GOALS", numbered=True)
        self.bullets("강의 구성", [(0, s.title) for s in lec.sections], kicker="OUTLINE", numbered=True)
        for i, sec in enumerate(lec.sections, 1):
            kicker = f"{i:02d}"
            items, notes, calls = [], [], []
            paras = [p for k, p in sec.blocks if k == "p"]
            for kind, payload in sec.blocks:
                if kind == "ul":
                    items.extend(payload)
                elif kind in ("clin", "key"):
                    calls.append((kind, payload))
            notes = " ".join(paras)
            if not items:
                items = [(0, p) for p in paras]
                notes = ""
            if items:
                self.bullets(sec.title, items, kicker, note=notes)
            for kind, payload in sec.blocks:
                if kind == "table":
                    self.table(sec.title, payload, kicker)
            if calls:
                # 콜아웃이 많으면 2개씩 나눔
                for k in range(0, len(calls), 2):
                    self.callouts(sec.title, calls[k:k + 2], kicker)
        if lec.frontier:
            self.bullets("연구 최전선", [(0, x) for x in lec.frontier], kicker="FRONTIER")
        if lec.summary:
            self.bullets("요약", [(0, x) for x in lec.summary], kicker="SUMMARY", numbered=True)
        if lec.quiz:
            self.quiz()
        if lec.refs:
            self.bullets("참고 문헌", [(0, x) for x in lec.refs], kicker="REFERENCES")
        out.parent.mkdir(parents=True, exist_ok=True)
        self.prs.save(out)


# --------------------------------------------------------------------------

def main():
    only = set(sys.argv[1:])  # 예: build.py b01  (HTML/PPT 일부만 재생성)
    files = {}
    for p in sorted(SRC.glob("b*.md")):  # b01.md, b01_2.md ... 를 한 묶음으로 합침
        files.setdefault(p.name[:3], []).append(p)
    bundles = [parse_bundle(ps) for ps in files.values()]
    bundles.sort(key=lambda b: b.no)
    for bi, b in enumerate(bundles):
        bdir = ROOT / b.slug
        bdir.mkdir(exist_ok=True)
        prev_b = bundles[bi - 1] if bi > 0 else None
        next_b = bundles[bi + 1] if bi + 1 < len(bundles) else None
        (bdir / "index.html").write_text(bundle_html(b, prev_b, next_b), encoding="utf-8")
        for li, lec in enumerate(b.lectures):
            prev = b.lectures[li - 1] if li > 0 else None
            nxt = b.lectures[li + 1] if li + 1 < len(b.lectures) else None
            (bdir / f"{lec.slug}.html").write_text(lecture_html(lec, prev, nxt), encoding="utf-8")
            if not only or b.slug in only:
                Deck(lec).build(bdir / "ppt" / lec.ppt_name)
    (ROOT / "index.html").write_text(index_html(bundles), encoding="utf-8")
    total = sum(len(b.lectures) for b in bundles)
    print(f"{len(bundles)}묶음 · {total}강 생성 완료")


if __name__ == "__main__":
    main()
