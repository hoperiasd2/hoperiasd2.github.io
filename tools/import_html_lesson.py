#!/usr/bin/env python3
"""외부에서 집필된 수업 HTML을 lesson.md 로 되돌린다.

저장소는 lesson.md 하나를 원본으로 두고 index.html 과 slides.pptx 를
만든다. 외부에서 HTML만 받은 경우 그 원본이 없으므로, 다시 빌드할 수도
없고 qa_lesson.py 의 검사도 받지 못한다. 이 스크립트가 그 간격을 메운다.

사용:
    python3 tools/import_html_lesson.py curriculum/M02/W01/L01/index.html
    python3 tools/import_html_lesson.py --glob 'curriculum/M02/W0[1-6]/L0*/index.html'

변환하는 것:
    <h2>학습목표</h2><ol><li>      → @obj
    <h2>선수지식</h2><p>            → @prereq (문장 단위로 나눈다)
    <h3>N. 제목</h3>                → @sec N. 제목
    <p>                             → 문단
    <p class="equation">            → @eq
    <strong class="exam">&gt;&gt;   → >> (시험에서 가려내는 지점)
    <span class="research">~        → ~ (연구 전선)
    <aside class="case">            → > (임상 연계)
    <table>                         → | 구분 표
    <ol class="questions">          → @quiz 의 Q:/A:
    <ol class="references">         → @ref
    <sub>/<sup>                     → _{ } / ^{ }
    <strong>/<em>/<code>            → ** ** / * * / ` `

원본 HTML은 지우지 않는다. 변환 뒤 build_lesson.py 를 돌리면 index.html
이 저장소의 공통 스타일로 다시 만들어진다.
"""
import argparse
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TAG = re.compile(r"<[^>]+>")


def inline(s):
    """인라인 HTML을 lesson.md 의 서식으로 바꾼다."""
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"<sub>(.*?)</sub>", r"_{\1}", s, flags=re.S)
    s = re.sub(r"<sup>(.*?)</sup>", r"^{\1}", s, flags=re.S)
    s = re.sub(r"<(?:strong|b)\b[^>]*>(.*?)</(?:strong|b)>", r"**\1**", s, flags=re.S)
    s = re.sub(r"<(?:em|i|cite)\b[^>]*>(.*?)</(?:em|i|cite)>", r"*\1*", s, flags=re.S)
    s = re.sub(r"<code\b[^>]*>(.*?)</code>", r"`\1`", s, flags=re.S)
    # 수업 사이 링크는 수업 ID만 남긴다. 빌더가 다시 링크로 만든다.
    s = re.sub(r'<a\b[^>]*href="(?:\.\.|#)[^"]*"[^>]*>(.*?)</a>', r"\1", s, flags=re.S)
    # 바깥 주소 링크는 주소를 괄호에 남겨 출처를 잃지 않는다.
    s = re.sub(r'<a\b[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', r"\2 (\1)", s, flags=re.S)
    s = TAG.sub("", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def cells(row):
    out = []
    for m in re.finditer(r"<(th|td)\b[^>]*>(.*?)</\1>", row, flags=re.S):
        out.append(inline(m.group(2)) or " ")
    return out


def table_md(block):
    """<table> 하나를 | 구분 표로 바꾼다. caption 은 표 앞의 굵은 줄로 남긴다."""
    lines = []
    cap = re.search(r"<caption\b[^>]*>(.*?)</caption>", block, flags=re.S)
    if cap and inline(cap.group(1)):
        lines.append(f"**{inline(cap.group(1))}**")
        lines.append("")
    rows = re.findall(r"<tr\b[^>]*>(.*?)</tr>", block, flags=re.S)
    if not rows:
        return []
    head = cells(rows[0])
    lines.append("| " + " | ".join(head) + " |")
    lines.append("|" + "---|" * len(head))
    for r in rows[1:]:
        c = cells(r)
        # 열 수가 어긋나면 빌더가 표를 깨뜨리므로 맞춘다.
        c = (c + [" "] * len(head))[:len(head)]
        lines.append("| " + " | ".join(c) + " |")
    return lines


def sentences(text):
    parts = re.split(r"(?<=[.다])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def convert_body(chunk):
    """한 절의 안쪽 HTML을 lesson.md 줄 목록으로 바꾼다."""
    out = []

    def add(line):
        if line:
            out.append(line)
            out.append("")

    # 블록을 등장 순서대로 집는다.
    pat = re.compile(
        r'(?P<table><div class="table-scroll">.*?</div>)'
        r'|(?P<case><aside class="case">.*?</aside>)'
        r'|(?P<eq><p class="equation">.*?</p>)'
        r'|(?P<ol><ol(?![^>]*class="(?:questions|references)")[^>]*>.*?</ol>)'
        r'|(?P<ul><ul[^>]*>.*?</ul>)'
        r'|(?P<p><p(?![^>]*class="equation")[^>]*>.*?</p>)',
        re.S)

    for m in pat.finditer(chunk):
        if m.group("table"):
            for ln in table_md(m.group("table")):
                out.append(ln)
            out.append("")
        elif m.group("case"):
            h = re.search(r"<h4\b[^>]*>(.*?)</h4>", m.group("case"), flags=re.S)
            body = " ".join(
                inline(x) for x in re.findall(r"<p\b[^>]*>(.*?)</p>", m.group("case"), flags=re.S))
            lead = f"**{inline(h.group(1))}** " if h else ""
            add("> " + lead + body)
        elif m.group("eq"):
            inner = re.sub(r"</?p\b[^>]*>", "", m.group("eq"))
            for part in re.split(r"<br\s*/?>", inner):
                if inline(part):
                    out.append("@eq " + inline(part))
            out.append("")
        elif m.group("ol") or m.group("ul"):
            block = m.group("ol") or m.group("ul")
            num = bool(m.group("ol"))
            items = re.findall(r"<li\b[^>]*>(.*?)</li>", block, flags=re.S)
            for i, it in enumerate(items, 1):
                txt = inline(it)
                if txt:
                    out.append(f"{i}. {txt}" if num else f"- {txt}")
            out.append("")
        elif m.group("p"):
            raw = m.group("p")
            # 시험 상자와 연구 상자는 문단에서 떼어 별도 줄로 만든다.
            # 상자가 문단 중간에 있으면 앞은 문단으로, 상자와 그 뒤는 한 줄로
            # 묶는다. 앞 문단을 상자에 끌어들이면 내용이 어긋난다.
            mk = re.search(r'<strong class="exam">(.*?)</strong>'
                           r'|<span class="research">(.*?)</span>', raw, flags=re.S)
            if not mk:
                add(inline(raw))
                continue
            before = inline(raw[:mk.start()])
            after = inline(raw[mk.end():])
            is_exam = mk.group(1) is not None
            label = ">> " if is_exam else "~ "
            inner = inline(mk.group(1) if is_exam else mk.group(2)).lstrip(">~").strip()
            add(before)
            add(label + inner + (" " + after if after else ""))
    return out


def convert(path):
    src = Path(path)
    t = src.read_text(encoding="utf-8")

    lid = re.search(r'data-lesson-id="([^"]+)"', t)
    lid = lid.group(1) if lid else src.parent.parent.name
    title = re.search(r"<h1>(.*?)</h1>", t, flags=re.S)
    title = inline(title.group(1)) if title else ""
    # 제목 끝의 [N장] 은 교재 장 표시이므로 참고문헌에 남기고 제목에서 뗀다.
    title = re.sub(r"\s*\[[^\]]*장\]\s*$", "", title)

    lines = ["---", f"title: {title}", "status: 초안", "version: v0.1",
             "slides: none", "---", ""]

    obj = re.search(r'id="objectives".*?<ol[^>]*>(.*?)</ol>', t, flags=re.S)
    if obj:
        lines.append("@obj")
        for it in re.findall(r"<li\b[^>]*>(.*?)</li>", obj.group(1), flags=re.S):
            lines.append("- " + inline(it))
        lines.append("")

    pre = re.search(r'id="prerequisites".*?(<p\b.*?</p>)', t, flags=re.S)
    if pre:
        lines.append("@prereq")
        for s in sentences(inline(pre.group(1))):
            lines.append("- " + s)
        lines.append("")

    secs = re.findall(
        r'<section id="s\d+" class="lesson-section">\s*<h3>(.*?)</h3>(.*?)</section>',
        t, flags=re.S)
    if not secs:
        sys.exit(f"{path}: 본문 절을 찾지 못했다")
    for head, chunk in secs:
        lines.append("@sec " + inline(head))
        lines.extend(convert_body(chunk))

    q = re.search(r'<ol class="questions">(.*?)</ol>\s*</section>', t, flags=re.S)
    if q:
        lines.append("@quiz")
        for it in re.findall(r"<li\b[^>]*>(.*?)</li>", q.group(1), flags=re.S):
            qq = re.search(r"<p\b[^>]*>(.*?)</p>", it, flags=re.S)
            aa = re.search(r"<details\b.*?<p\b[^>]*>(.*?)</p>", it, flags=re.S)
            if qq and aa:
                lines.append("Q: " + inline(qq.group(1)))
                lines.append("A: " + inline(aa.group(1)))
                lines.append("")
        lines.append("")

    ref = re.search(r'<ol class="references">(.*?)</ol>', t, flags=re.S)
    if ref:
        lines.append("@ref")
        for it in re.findall(r"<li\b[^>]*>(.*?)</li>", ref.group(1), flags=re.S):
            lines.append("- " + inline(it))
        lines.append("")

    out = src.parent / "lesson.md"
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).rstrip() + "\n"
    out.write_text(text, encoding="utf-8")
    nref = len(re.findall(r"<li\b", ref.group(1))) if ref else 0
    print(f"{lid}  절 {len(secs)}  문항 {text.count('Q: ')}  출처 {nref}  "
          f"수식 {text.count('@eq ')}  {len(text):,}자 → {out}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--glob")
    a = ap.parse_args()
    paths = list(a.paths)
    if a.glob:
        paths += sorted(str(p) for p in ROOT.glob(a.glob))
    if not paths:
        sys.exit("변환할 HTML 경로가 필요하다")
    for p in paths:
        convert(p)


if __name__ == "__main__":
    main()
