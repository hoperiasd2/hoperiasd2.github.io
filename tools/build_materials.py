#!/usr/bin/env python3
"""저장소의 모든 슬라이드와 실습 자료를 모은 내려받기 페이지를 만든다."""
import csv
import html
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "curriculum" / "materials.html"


def esc(s):
    return html.escape(str(s), quote=True)


def mb(p):
    n = p.stat().st_size
    return f"{n/1024/1024:.1f} MB" if n >= 1024 * 1024 else f"{n/1024:.0f} KB"


def tracked(pattern):
    r = subprocess.run(["git", "ls-files", pattern], cwd=ROOT,
                       capture_output=True, text=True)
    return [ROOT / x for x in r.stdout.split("\n") if x.strip()]


def main():
    with (ROOT / "curriculum.csv").open(encoding="utf-8") as f:
        rows = {r["lesson_id"]: r for r in csv.DictReader(f)}

    # 1) 수업 슬라이드
    lesson_rows = []
    for lid, r in rows.items():
        p = ROOT / r["path"] / "slides.pptx"
        if p.exists():
            rel = f'{r["path"][len("curriculum/"):]}slides.pptx'
            lesson_rows.append((r["module"], lid, r["title"], rel, mb(p)))
    lesson_rows.sort()

    by_mod = {}
    for mod, lid, title, rel, size in lesson_rows:
        by_mod.setdefault(mod, []).append((lid, title, rel, size))

    secs = []
    for mod, items in by_mod.items():
        trs = "".join(
            f'<tr><td class="lid">{esc(lid)}</td><td>{esc(t)}</td>'
            f'<td class="sz">{esc(sz)}</td>'
            f'<td><a class="dlbtn dlbtn--sm" href="{esc(rel)}" download>PPTX</a></td></tr>'
            for lid, t, rel, sz in items)
        secs.append(f'<section data-section><h3>{esc(mod)} · {len(items)}개</h3>'
                    f'<table><thead><tr><th>수업</th><th>제목</th><th>용량</th><th></th></tr></thead>'
                    f'<tbody>{trs}</tbody></table></section>')

    # 2) 기존 자료
    legacy = []
    for p in sorted(tracked("*.pptx")):
        if p.parent == ROOT:
            legacy.append((p.name, p.name, mb(p)))
    legacy_tr = "".join(
        f'<tr><td>{esc(n)}</td><td class="sz">{esc(s)}</td>'
        f'<td><a class="dlbtn dlbtn--sm" href="../{esc(h)}" download>PPTX</a></td></tr>'
        for n, h, s in legacy)

    # 3) 아카이브 강의록
    arch = tracked("archive/lectures/*/ppt/*.pptx")
    arch_by_b = {}
    for p in sorted(arch):
        arch_by_b.setdefault(p.parent.parent.name, []).append(p)
    arch_tr = "".join(
        f'<tr><td class="lid">{esc(b.upper())}</td><td>{len(v)}강</td>'
        f'<td class="sz">{sum(x.stat().st_size for x in v)/1024/1024:.0f} MB</td>'
        f'<td><a href="../archive/lectures/{esc(b)}/index.html">묶음 열기</a></td></tr>'
        for b, v in sorted(arch_by_b.items()))

    total = len(lesson_rows) + len(legacy) + len(arch)
    body = f"""  <nav class="crumb" aria-label="이동 경로">
    <a href="../index.html">대문</a><span aria-hidden="true">›</span>
    <a href="index.html">전체 수업</a><span aria-hidden="true">›</span><span>자료 내려받기</span>
  </nav>

  <section class="hero">
    <p class="eyebrow">Downloads · {total} files</p>
    <h1>자료 내려받기</h1>
    <p class="lede">수업 슬라이드와 기존 강의·실습 자료를 한곳에 모았다.
    수업 슬라이드는 집필된 수업만 올라오며, 본문이 갱신되면 같은 원본에서 다시 생성된다.</p>
  </section>

  <h2>수업 슬라이드 · {len(lesson_rows)}개</h2>
  {''.join(secs) if secs else '<p class="count">아직 생성된 슬라이드가 없다.</p>'}

  <h2>기존 강의·실습 자료 · {len(legacy)}개</h2>
  <table><thead><tr><th>파일</th><th>용량</th><th></th></tr></thead><tbody>{legacy_tr}</tbody></table>
  <div class="callout">이 자료는 M07 기초의과학 실습으로 편입 중이다. 편입이 끝나면 해당 수업 폴더로 옮긴다.</div>

  <h2>강의록 아카이브 · {len(arch)}개</h2>
  <table><thead><tr><th>묶음</th><th>강 수</th><th>용량</th><th></th></tr></thead><tbody>{arch_tr}</tbody></table>
"""
    page = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>자료 내려받기</title>
<meta name="description" content="수업 슬라이드와 강의·실습 자료 모음">
<link rel="stylesheet" href="../assets/site.css">
<link rel="stylesheet" href="../assets/lesson.css">
<style>
  .dlbtn--sm {{ padding: 4px 11px; font-size: 12px; }}
  td.lid {{ font-family: var(--mono); font-size: 12px; white-space: nowrap; }}
  td.sz {{ color: var(--ink-3); font-size: 13px; white-space: nowrap; }}
  table {{ font-size: 14.5px; }}
</style>
</head>
<body>

<header class="masthead">
  <div class="wrap">
    <a class="brand" href="../index.html">의생명과학 교육과정</a>
    <nav>
      <a href="index.html">전체 수업</a>
      <a href="materials.html">자료 내려받기</a>
      <a href="../archive/index.html">아카이브</a>
    </nav>
  </div>
</header>

<main class="wrap">
{body}
</main>

<footer class="foot wrap">
  <span>© 2026 Kim Jintae · Hanyang University</span>
  <a href="https://github.com/hoperiasd2/hoperiasd2.github.io">GitHub 저장소</a>
</footer>
</body>
</html>
"""
    OUT.write_text(page, encoding="utf-8")
    print(f"자료 {total}개 → {OUT.relative_to(ROOT)}")
    print(f"  수업 슬라이드 {len(lesson_rows)} · 기존 자료 {len(legacy)} · 아카이브 {len(arch)}")


if __name__ == "__main__":
    main()
