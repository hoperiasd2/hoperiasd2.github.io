#!/usr/bin/env python3
"""그림 안 글자 분량을 조사한다.

그림은 논문 figure처럼 라벨만 두고, 설명은 캡션과 SVG 주석으로 옮긴다.
문장을 그림 안에 넣으면 글자가 겹쳐 그림이 깨지고, 읽는 사람도 그림을 읽지 않는다.

문장으로 보는 기준은 한 줄 48자 초과, 마침표로 끝남, 한 칸에 두 문장이다.
글자 합계와 text 개수는 권고값이다. 표 형태의 그림은 짧은 칸이 많아 넘을 수 있다.

사용:
    python3 tools/fig_audit.py                문장이 남은 그림만, 심한 순서로
    python3 tools/fig_audit.py --all          전부
    python3 tools/fig_audit.py M01-W07-L01    한 수업만
    python3 tools/fig_audit.py --worst 20     가장 심한 20개
    python3 tools/fig_audit.py --lesson       수업별 합계
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUDGET = {"one": 48, "chars": 380, "nodes": 26}


def is_sentence(t):
    return (len(t) > BUDGET["one"]
            or bool(re.search(r"[a-z)\]][.]$", t))
            or bool(re.search(r"[.][ ][A-Z]", t)))


def texts(svg):
    vis = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    vis = re.sub(r"<(desc|title)\b.*?</\1>", "", vis, flags=re.S)
    out = [re.sub(r"<[^>]+>", "", t) for t in
           re.findall(r"<text\b[^>]*>(.*?)</text>", vis, re.S)]
    out = [re.sub(r"\s+", " ", t).strip() for t in out]
    return [t for t in out if t]


def scan(want=None):
    rows = []
    for f in sorted(ROOT.glob("curriculum/*/*/*/assets/fig-*.svg")):
        lid = f"{f.parts[-5]}-{f.parts[-4]}-{f.parts[-3]}"
        if want and lid != want:
            continue
        it = texts(f.read_text(encoding="utf-8", errors="ignore"))
        sent = [t for t in it if is_sentence(t)]
        rows.append({"lid": lid, "name": f.stem,
                     "chars": sum(len(t) for t in it), "nodes": len(it),
                     "one": max((len(t) for t in it), default=0),
                     "sent": len(sent),
                     "worst": max((len(t) for t in sent), default=0)})
    return rows


def line(r):
    flag = lambda v, k: f"{v}{'!' if v > BUDGET[k] else ' '}"
    return (f"  {r['lid']}  {r['name']:<28} "
            f"문장 {r['sent']:3d}개  가장 긴 것 {r['worst']:4d}자  "
            f"글자 {flag(r['chars'], 'chars'):>6} "
            f"text {flag(r['nodes'], 'nodes'):>5}")


def main():
    a = sys.argv[1:]
    want = next((x for x in a if re.fullmatch(r"M\d{2}-W\d{2}-L\d{2}", x)), None)
    rows = scan(want)
    if not rows:
        print("그림이 없다.")
        return

    if "--lesson" in a:
        agg = {}
        for r in rows:
            g = agg.setdefault(r["lid"], [0, 0, 0])
            g[0] += 1
            g[1] += r["chars"]
            g[2] += r["sent"] > 0
        print(f"수업 {len(agg)}개, 그림 {len(rows)}개  "
              f"(그림 하나 예산 {BUDGET['chars']}자)\n")
        for lid in sorted(agg, key=lambda k: -agg[k][1] / agg[k][0]):
            n, c, bad = agg[lid]
            print(f"  {lid}  그림 {n:2d}  평균 {c // n:4d}자  문장 남은 그림 {bad:2d}개")
        return

    show = rows if "--all" in a or want else [r for r in rows if r["sent"]]
    show.sort(key=lambda r: (-r["worst"], -r["sent"]))
    if "--worst" in a:
        i = a.index("--worst")
        show = show[:int(a[i + 1])] if len(a) > i + 1 else show[:20]

    print(f"문장 기준: 한 줄 {BUDGET['one']}자 초과, 마침표로 끝남, 한 칸에 두 문장")
    print(f"권고: 글자 합계 {BUDGET['chars']}자, text {BUDGET['nodes']}개. "
          f"{'!'} 는 권고를 넘은 값이다.\n")
    for r in show:
        print(line(r))
    bad = sum(1 for r in rows if r["sent"])
    print(f"\n그림 {len(rows)}개 중 {bad}개에 문장이 남아 있다 "
          f"({bad * 100 // max(len(rows), 1)}%). 그림 하나 평균 "
          f"{sum(r['chars'] for r in rows) // len(rows)}자.")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:          # head 등으로 끊어 볼 때
        pass
