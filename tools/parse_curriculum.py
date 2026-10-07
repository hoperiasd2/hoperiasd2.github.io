#!/usr/bin/env python3
"""PROJECT.md의 수업 표를 읽어 curriculum.csv를 생성한다.

PROJECT.md가 교육과정의 단일 원본이다. 수업을 추가·수정할 때는 PROJECT.md를
고치고 이 스크립트를 다시 실행한다. curriculum.csv를 직접 편집하지 않는다.
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "PROJECT.md"
OUT = ROOT / "curriculum.csv"

LESSON_ID = re.compile(r"^M(\d{2})-W(\d{2})-L(\d{2})$")
PHASE = re.compile(r"^####\s*[^.]+\.\s*(.+?)\s*\(W\d+~W\d+\)\s*$")
MODHEAD = re.compile(r"^###\s")
MODULE_ROW = re.compile(r"^\|\s*(M\d{2})\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*(\d+)\s*\|")


def cells(line):
    """마크다운 표 한 행을 셀 목록으로 자른다."""
    if not line.startswith("|"):
        return None
    return [c.strip() for c in line.strip().strip("|").split("|")]


def main():
    text = SRC.read_text(encoding="utf-8")
    lines = text.split("\n")

    # 1) 머리말 편성표에서 구성요소 제목과 회차를 읽는다.
    modules = {}
    for line in lines:
        m = MODULE_ROW.match(line)
        if m:
            modules[m.group(1)] = {"title": m.group(2), "plan": m.group(3), "count": int(m.group(4))}
    if len(modules) != 7:
        sys.exit(f"구성요소 편성표를 7개로 읽지 못했습니다: {sorted(modules)}")

    # 2) 수업 행을 수집한다. 현재 단계(M07) 헤더를 따라가며 group을 붙인다.
    rows = []
    seen = set()
    group = ""
    for line in lines:
        if MODHEAD.match(line):
            group = ""
            continue
        p = PHASE.match(line)
        if p:
            group = p.group(1)
            continue
        c = cells(line)
        if not c or len(c) < 3:
            continue
        lid = LESSON_ID.match(c[0])
        if not lid:
            continue
        # 두 번째 셀이 정수가 아니면 수업 표가 아니다(원저 후보 표 등).
        if not c[1].isdigit():
            continue
        if c[0] in seen:
            continue
        seen.add(c[0])

        mod = "M" + lid.group(1)
        week = int(lid.group(2))
        sess = int(lid.group(3))
        if mod == "M07":
            title, assets = c[2], (c[3] if len(c) > 3 else "")
        else:
            title, assets = c[3], ""
        assets = "" if assets.strip() in {"—", "-", ""} else assets.replace("`", "")

        rows.append({
            "lesson_id": c[0],
            "module": mod,
            "module_title": modules[mod]["title"],
            "week": week,
            "session": sess,
            "group": group,
            "title": title,
            "legacy_assets": assets,
            "kind": "practicum" if mod == "M07" else "lecture",
            "path": f"curriculum/{mod}/W{week:02d}/L{sess:02d}/",
            "status": "설계",
            "version": "",
            "slides": "",
            "updated": "",
        })

    rows.sort(key=lambda r: (r["module"], r["week"], r["session"]))

    # 3) 구성요소별 회차 수가 편성표와 맞는지 확인한다.
    for mod, meta in sorted(modules.items()):
        got = sum(1 for r in rows if r["module"] == mod)
        if got != meta["count"]:
            sys.exit(f"{mod}: 편성표 {meta['count']}회, 명단 {got}회 — 불일치")

    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"{len(rows)}개 수업 → {OUT.relative_to(ROOT)}")
    for mod, meta in sorted(modules.items()):
        n = sum(1 for r in rows if r["module"] == mod)
        print(f"  {mod} {meta['title'][:28]:30s} {n:3d}회")


if __name__ == "__main__":
    main()
