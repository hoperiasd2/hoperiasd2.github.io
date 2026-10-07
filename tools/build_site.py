#!/usr/bin/env python3
"""curriculum.csv에서 사이트 위계를 생성한다.

생성 대상:
  index.html                              대문
  curriculum/index.html                   전체 수업 인덱스
  curriculum/MXX/index.html               구성요소 개요
  curriculum/MXX/WXX/index.html           주차 개요
  curriculum/MXX/WXX/LXX/index.html       수업 페이지
  curriculum/MXX/WXX/LXX/lesson.md        설계 원본(강의)
  curriculum/MXX/WXX/LXX/protocol.md      프로토콜 원본(실습)
  curriculum/MXX/WXX/LXX/sources.json
  curriculum/MXX/WXX/LXX/figures.json

이미 집필이 시작된 수업(status가 '설계'가 아님)의 index.html과 본문 파일은
덮어쓰지 않는다. 틀만 다시 만들고 싶으면 --force를 준다.
"""
import argparse
import csv
import html
import json
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "curriculum.csv"

STATUS_CLASS = {
    "설계": "design", "자료조사": "design", "초안": "draft",
    "검수": "review", "승인": "done", "완료": "done",
}

MODULE_EN = {
    "M01": "Human Biology and Cell Biology",
    "M02": "Metabolic Biochemistry",
    "M03": "Molecular Genetics and Systems-Based Medical Biochemistry",
    "M04": "Neuroscience, Neurogenetics and Translational Neuroscience",
    "M05": "Systems-Based Biomedical Science",
    "M06": "Current Issues in Biomedical and Brain Science",
    "M07": "Basic Biomedical Science Laboratory",
}

MODULE_LEDE = {
    "M01": "인체 계통의 구조와 기능을 먼저 훑고, 세포생물학의 실험적 근거와 세포소기관의 작동 원리로 들어간다. 이후 모든 구성요소가 기대는 공통 어휘를 만든다.",
    "M02": "에너지와 물질이 어떤 조건에서 어느 방향으로 흐르는지를 다룬다. 경로의 암기가 아니라 율속 단계와 조절 신호, 그리고 조절이 깨졌을 때 축적되는 것과 고갈되는 것을 추적한다. 경로를 모두 다룬 뒤 마지막 3주는 대사 조절과 중개대사 심화에 쓴다.",
    "M03": "앞 6주는 유전정보의 저장·발현·조작을 질환과 진단의 맥락에서 다룬다. 이후 8주는 심혈관·소화기·신비뇨·면역·소아·노화·종양·신경의 여덟 계통을 각 3회씩 보며, 계통마다 기질 선택과 에너지 흐름, 대사 표지, 대사 표적을 공통 축으로 삼는다.",
    "M04": "앞 7주는 Bear를 기본 교재로 막전위에서 감각·운동·행동까지 올라간다. 뒤 7주는 질환별로 나누어 다루되, 신경면역과 blood-brain barrier, 질환 모델, 유전자·세포 치료, 신경조절처럼 여러 질환에 걸치는 기전과 치료 수단도 독립 수업으로 둔다.",
    "M05": "계통별로 항상성이 유지되는 방식과 그것이 무너지는 지점을 본다. 한 계통의 이상이 다른 계통으로 번지는 경로를 증례로 통합한다.",
    "M06": "최근 원저를 근거로 미해결 질문, 경쟁하는 가설, 결정적 실험을 다룬다. 기초 설명을 반복하지 않고 근거의 수준과 재현성을 평가한다.",
    "M07": "앞선 구성요소에서 다룬 기전을 직접 측정하고 관찰한다. 절차와 그 절차가 성립하는 근거를 함께 다루며, 실패 양상과 판단 기준을 명시한다.",
}

PHASE_NOTE = {
    "M07": "6단계로 나누며 각 단계는 앞 단계의 술기를 전제로 한다. 실제 장비와 동물 사용 승인이 확인되기 전까지는 가상실습과 공개 데이터를 기반으로 한다.",
}


def esc(s):
    return html.escape(str(s), quote=True)


def page(title, body, depth, desc="", extra_head=""):
    """공통 문서 틀. depth는 루트까지의 상대 깊이."""
    up = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="stylesheet" href="{up}assets/site.css">
{extra_head}</head>
<body>

<header class="masthead">
  <div class="wrap">
    <a class="brand" href="{up}index.html">의생명과학 교육과정</a>
    <nav>
      <a href="{up}curriculum/index.html">전체 수업</a>
      <a href="{up}curriculum/M07/index.html">실습</a>
      <a href="{up}archive/lectures/index.html">강의록 아카이브</a>
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

<script src="{up}assets/site.js"></script>
</body>
</html>
"""


def crumb(parts):
    """parts: [(label, href 또는 None)]"""
    out = ['<nav class="crumb" aria-label="이동 경로">']
    for i, (label, href) in enumerate(parts):
        if i:
            out.append('<span aria-hidden="true">›</span>')
        out.append(f'<a href="{href}">{esc(label)}</a>' if href else f"<span>{esc(label)}</span>")
    out.append("</nav>")
    return "".join(out)


def badge(status):
    return f'<span class="badge badge--{STATUS_CLASS.get(status, "design")}">{esc(status)}</span>'


def load():
    with CSV_PATH.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["week"] = int(r["week"])
        r["session"] = int(r["session"])
    mods = OrderedDict()
    for r in rows:
        mods.setdefault(r["module"], []).append(r)
    return rows, mods


def progress(rows):
    done = sum(1 for r in rows if r["status"] in ("승인", "완료"))
    return done, len(rows), (0 if not rows else round(done * 100 / len(rows)))


# --------------------------------------------------------------------------- 대문
def build_root(mods, force):
    cards = []
    for mod, rows in mods.items():
        done, total, pct = progress(rows)
        weeks = max(r["week"] for r in rows)
        per = "주 1회" if mod == "M07" else "주 3회"
        cards.append(f"""      <a class="card" href="curriculum/{mod}/index.html">
        <div class="card__no">{mod}</div>
        <div class="card__title">{esc(rows[0]['module_title'])}</div>
        <div class="card__en">{esc(MODULE_EN[mod])}</div>
        <div class="card__meta">{weeks}주 · {per} · {total}회 &nbsp;·&nbsp; 제작 {done}/{total}</div>
        <div class="bar"><i style="width:{pct}%"></i></div>
      </a>""")

    total = sum(len(v) for v in mods.values())
    body = f"""{crumb([("대문", None)])}

  <section class="hero">
    <p class="eyebrow">Biomedical Science Curriculum · 7 Modules · {total} Sessions</p>
    <h1>의생명과학 교육과정</h1>
    <p class="lede">인체생물학과 세포생물학에서 대사생화학, 오믹스와 임상중개, 신경과학, 계통별 심화,
    최신 연구 쟁점까지 여섯 구성요소로 나누고, 이를 직접 측정하고 분석하는 실습 구성요소를 더해
    모두 {total}회로 편성했다. 각 수업은 독립적으로 읽을 수 있는 HTML 문서와 편집 가능한 슬라이드로 제공된다.</p>
  </section>

  <h2>구성요소</h2>
  <div class="grid grid--modules">
{chr(10).join(cards)}
  </div>

  <h2>자료 찾기</h2>
  <div class="callout">
    <b><a href="curriculum/index.html">전체 수업 인덱스</a></b> — {total}개 수업을 구성요소·주차·키워드로 걸러 찾고
    제작 상태와 슬라이드 내려받기를 한 화면에서 확인한다.
  </div>
  <div class="callout">
    <b><a href="archive/lectures/index.html">강의록 아카이브</a></b> — 이전에 제작한 10묶음 123강.
    현재 교육과정의 수업으로 편입하는 중이며 그동안 읽기 전용으로 유지한다.
  </div>
"""
    out = ROOT / "index.html"
    if out.exists() and not force:
        return False
    out.write_text(page("의생명과학 교육과정", body, 0,
                        "의학생화학·세포생물학·오믹스·신경과학·계통별 기초의학과 실습을 포괄하는 교육과정"),
                   encoding="utf-8")
    return True


# ------------------------------------------------------------------- 전체 인덱스
def build_index(mods):
    filters = "".join(
        f'<button type="button" data-filter="{m}" aria-pressed="false">{m}</button>'
        for m in mods)

    sections = []
    for mod, rows in mods.items():
        lis = []
        for r in rows:
            q = f"{r['lesson_id']} {r['title']} {r['module_title']} {r['group']}"
            grp = f'<span class="lgroup">{esc(r["group"])}</span>' if r["group"] else ""
            lis.append(
                f'      <li data-q="{esc(q)}" data-module="{mod}">'
                f'<a href="{r["path"][len("curriculum/"):]}index.html">'
                f'<span class="lid">{r["lesson_id"]}</span>'
                f'<span class="ltitle">{esc(r["title"])}</span>{grp}{badge(r["status"])}</a></li>')
        sections.append(f"""  <section data-section>
    <h2><a href="{mod}/index.html">{mod} · {esc(rows[0]['module_title'])}</a></h2>
    <ul class="lessons">
{chr(10).join(lis)}
    </ul>
  </section>""")

    total = sum(len(v) for v in mods.values())
    body = f"""{crumb([("대문", "../index.html"), ("전체 수업", None)])}

  <section class="hero">
    <p class="eyebrow">Lesson Index</p>
    <h1>전체 수업 인덱스</h1>
    <p class="lede">{total}개 수업을 한 화면에서 찾는다. 수업 ID, 제목, 구성요소 이름, 실습 단계로 검색된다.</p>
  </section>

  <label class="visually-hidden" for="q">수업 검색</label>
  <input id="q" class="search" type="search" data-search placeholder="수업 검색 (예: urea cycle, M03, 단일세포, 해부)">
  <div class="filters">{filters}</div>
  <p class="count" data-count>{total}개 수업</p>

{chr(10).join(sections)}
"""
    (ROOT / "curriculum").mkdir(exist_ok=True)
    (ROOT / "curriculum/index.html").write_text(
        page("전체 수업 인덱스", body, 1, f"{total}개 수업의 검색 가능한 목록"), encoding="utf-8")


# ----------------------------------------------------------------- 구성요소 개요
def build_module(mod, rows):
    weeks = OrderedDict()
    for r in rows:
        weeks.setdefault(r["week"], []).append(r)

    cards = []
    for wk, wrows in weeks.items():
        titles = "<br>".join(esc(x["title"].split(":")[0]) for x in wrows)
        grp = wrows[0]["group"]
        label = f'<div class="card__en">{esc(grp)}</div>' if grp else ""
        cards.append(f"""      <a class="card" href="W{wk:02d}/index.html">
        <div class="card__no">W{wk:02d}</div>
        <div class="card__title">{wk}주차 · {len(wrows)}회</div>
        {label}<div class="card__meta">{titles}</div>
      </a>""")

    done, total, pct = progress(rows)
    nweeks = max(weeks)
    per = "주 1회" if mod == "M07" else "주 3회"
    note = f'<div class="callout">{esc(PHASE_NOTE[mod])}</div>' if mod in PHASE_NOTE else ""

    body = f"""{crumb([("대문", "../../index.html"), ("전체 수업", "../index.html"), (mod, None)])}

  <section class="hero">
    <p class="eyebrow">{mod} · {nweeks} Weeks · {total} Sessions</p>
    <h1>{esc(rows[0]['module_title'])}</h1>
    <p class="en">{esc(MODULE_EN[mod])}</p>
    <p class="lede">{esc(MODULE_LEDE[mod])}</p>
  </section>

  {note}
  <p class="count">{nweeks}주 · {per} · 전체 {total}회 · 제작 완료 {done}회</p>
  <div class="bar"><i style="width:{pct}%"></i></div>

  <h2>주차</h2>
  <div class="grid grid--weeks">
{chr(10).join(cards)}
  </div>
"""
    d = ROOT / "curriculum" / mod
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(
        page(f"{mod} {rows[0]['module_title']}", body, 2, MODULE_LEDE[mod][:120]), encoding="utf-8")


# --------------------------------------------------------------------- 주차 개요
def build_week(mod, wk, rows, module_title):
    lis = []
    for r in rows:
        grp = f'<span class="lgroup">{esc(r["group"])}</span>' if r["group"] else ""
        lis.append(f'    <li><a href="L{r["session"]:02d}/index.html">'
                   f'<span class="lid">{r["lesson_id"]}</span>'
                   f'<span class="ltitle">{esc(r["title"])}</span>{grp}{badge(r["status"])}</a></li>')

    body = f"""{crumb([("대문", "../../../index.html"), ("전체 수업", "../../index.html"),
                       (mod, "../index.html"), (f"{wk}주차", None)])}

  <section class="hero">
    <p class="eyebrow">{mod} · Week {wk:02d}</p>
    <h1>{wk}주차</h1>
    <p class="lede">{esc(module_title)} · {len(rows)}회</p>
  </section>

  <h2>수업</h2>
  <ul class="lessons">
{chr(10).join(lis)}
  </ul>
"""
    d = ROOT / "curriculum" / mod / f"W{wk:02d}"
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(
        page(f"{mod} {wk}주차", body, 3, f"{module_title} {wk}주차 수업 목록"), encoding="utf-8")


# --------------------------------------------------------------------- 수업 페이지
def build_lesson(r, prev_r, next_r, force):
    d = ROOT / r["path"]
    d.mkdir(parents=True, exist_ok=True)
    practicum = r["kind"] == "practicum"

    pager = []
    if prev_r:
        rel = f'../../../{prev_r["path"][len("curriculum/"):]}index.html'
        pager.append(f'<a href="{rel}">← {prev_r["lesson_id"]} {esc(prev_r["title"].split(":")[0])}</a>')
    else:
        pager.append("<span>처음 수업</span>")
    if next_r:
        rel = f'../../../{next_r["path"][len("curriculum/"):]}index.html'
        pager.append(f'<a href="{rel}">{next_r["lesson_id"]} {esc(next_r["title"].split(":")[0])} →</a>')
    else:
        pager.append("<span>마지막 수업</span>")

    legacy = ""
    if r["legacy_assets"]:
        links = []
        for a in [x.strip() for x in r["legacy_assets"].split(",") if x.strip()]:
            links.append(f'<a href="../../../../{esc(a)}">{esc(a)}</a>')
        legacy = ('<div class="callout callout--warn"><b>편입 대상 자산</b> — '
                  + ", ".join(links)
                  + '. 현행 산출물 규격과 집필 원칙에 맞춰 다시 쓴 뒤 이 경로에 배치한다. '
                    '아래 본문이 채워지기 전까지는 위 링크의 기존 자료를 사용한다.</div>')

    if practicum:
        skeleton = """  <h2>안전·윤리 고지</h2>
  <p>작성 예정. 생물안전등급, 화학물질, 동물, 개인정보 중 해당 항목과 금지 사항을 적는다.</p>

  <h2>선수지식</h2>
  <p>작성 예정. 대응하는 강의 수업 ID를 명시한다.</p>

  <h2>준비물·시약·장비</h2>
  <p>작성 예정.</p>

  <h2>프로토콜</h2>
  <p>작성 예정. 단계·시간·온도·농도와 각 수치의 출처를 적는다.</p>

  <h2>예상 결과와 판독 기준</h2>
  <p>작성 예정.</p>

  <h2>문제해결</h2>
  <p>작성 예정. 흔한 실패 양상, 원인, 재시도 판단 기준을 표로 정리한다.</p>

  <h2>결과 기록 양식</h2>
  <p>작성 예정.</p>

  <h2>토의 질문</h2>
  <p>작성 예정.</p>

  <h2>참고문헌</h2>
  <p>작성 예정.</p>"""
    else:
        skeleton = """  <h2>학습목표</h2>
  <p>작성 예정. 이 수업이 답하는 질문 6~9개를 먼저 확정한 뒤 측정 가능한 학습목표로 옮긴다.</p>

  <h2>선수지식</h2>
  <p>작성 예정.</p>

  <h2>본문</h2>
  <p>작성 예정. 각 절은 하나의 질문에 답하는 단위로 쓰고
  질문 → 답 → 근거 → 조건과 한계 → 귀결의 순서로 전개한다.</p>

  <h2>확인 문항</h2>
  <p>작성 예정. 5개 이상, 절반 이상은 판단을 묻는 문항으로 한다.</p>

  <h2>참고문헌</h2>
  <p>작성 예정.</p>"""

    kindword = "실습" if practicum else "강의"
    body = f"""{crumb([("대문", "../../../../index.html"), ("전체 수업", "../../../index.html"),
                       (r["module"], "../../index.html"), (f'{r["week"]}주차', "../index.html"),
                       (r["lesson_id"], None)])}

  <section class="hero">
    <p class="eyebrow">{r["lesson_id"]} · {esc(r["module_title"])}{" · " + esc(r["group"]) if r["group"] else ""}</p>
    <h1>{esc(r["title"])}</h1>
    <p class="lede">{kindword} 수업 · 상태 {badge(r["status"])}</p>
  </section>

  {legacy}
  <div class="callout">이 수업은 아직 집필 전이다. 제작 기준은
  <a href="../../../../PROJECT.md">PROJECT.md</a>의 집필 원칙과 산출물 규격을 따른다.</div>

{skeleton}

  <nav class="pager">{pager[0]}{pager[1]}</nav>
"""
    f = d / "index.html"
    # 집필이 시작된 수업은 build_lesson.py가 관리하므로 여기서 건드리지 않는다.
    if r["status"] == "설계" and (not f.exists() or force or True):
        f.write_text(page(f'{r["lesson_id"]} {r["title"]}', body, 4, r["title"]), encoding="utf-8")

    # 설계 원본
    src = d / ("protocol.md" if practicum else "lesson.md")
    if not src.exists():
        head = f"# {r['lesson_id']} {r['title']}\n\n- 구성요소: {r['module']} {r['module_title']}\n"
        head += f"- 주차·회차: {r['week']}주 {r['session']}회\n"
        if r["group"]:
            head += f"- 단계: {r['group']}\n"
        if r["legacy_assets"]:
            head += f"- 편입 대상 자산: {r['legacy_assets']}\n"
        head += "- 상태: 설계\n- 버전: v0.1\n\n"
        if practicum:
            head += ("## 안전 등급\n\n작성 예정.\n\n## 선수 수업\n\n작성 예정.\n\n"
                     "## 프로토콜 단계\n\n작성 예정. 각 수치의 출처를 함께 적는다.\n\n"
                     "## 문제해결\n\n작성 예정.\n\n## 제출물\n\n작성 예정.\n")
        else:
            head += ("## 이 수업이 답하는 질문\n\n"
                     "1. 작성 예정\n2. 작성 예정\n3. 작성 예정\n4. 작성 예정\n5. 작성 예정\n6. 작성 예정\n\n"
                     "질문 목록과 각 질문에 대한 한 문장 답을 확정하기 전에 본문을 쓰지 않는다.\n\n"
                     "## 학습목표\n\n작성 예정.\n\n## 절 구성\n\n작성 예정.\n\n"
                     "## 슬라이드 개요\n\n작성 예정.\n\n## 검토 결과\n\n작성 예정.\n")
        src.write_text(head, encoding="utf-8")

    for name, payload in (("sources.json", {"lesson_id": r["lesson_id"], "sources": []}),
                          ("figures.json", {"lesson_id": r["lesson_id"], "figures": []})):
        p = d / name
        if not p.exists():
            p.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if practicum:
        dd = d / "data"
        dd.mkdir(exist_ok=True)
        mf = dd / "MANIFEST.md"
        if not mf.exists():
            mf.write_text(
                f"# {r['lesson_id']} 실습 데이터\n\n"
                "| 파일 | 내용 | 출처 | 크기 | 라이선스·사용 조건 |\n|---|---|---|---|---|\n"
                "| 작성 예정 | | | | |\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="집필이 시작된 수업 페이지도 덮어쓴다")
    args = ap.parse_args()

    rows, mods = load()
    build_index(mods)
    created_root = build_root(mods, args.force)

    for mod, mrows in mods.items():
        build_module(mod, mrows)
        weeks = OrderedDict()
        for r in mrows:
            weeks.setdefault(r["week"], []).append(r)
        for wk, wrows in weeks.items():
            build_week(mod, wk, wrows, mrows[0]["module_title"])

    for i, r in enumerate(rows):
        prev_r = rows[i - 1] if i and rows[i - 1]["module"] == r["module"] else None
        next_r = rows[i + 1] if i + 1 < len(rows) and rows[i + 1]["module"] == r["module"] else None
        build_lesson(r, prev_r, next_r, args.force)

    print(f"{len(rows)}개 수업 · {len(mods)}개 구성요소 생성 완료")
    if not created_root:
        print("루트 index.html은 이미 존재하여 건너뛰었다. 덮어쓰려면 --force")


if __name__ == "__main__":
    main()
