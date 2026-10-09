#!/usr/bin/env python3
"""확인 문항을 골라 남긴다. 임시 파일에 쓴 뒤 교체하므로 중간에 실패해도 원본이 남는다.

사용:
    python3 tools/trim_quiz.py <수업ID>              문항 목록만 보인다
    python3 tools/trim_quiz.py <수업ID> 1 2 4 7      그 번호만 남긴다 (1부터)
"""
import csv
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def lesson_path(lid):
    with (ROOT / "curriculum.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["lesson_id"] == lid:
                return ROOT / r["path"] / "lesson.md"
    sys.exit(f"수업 ID를 찾지 못했다: {lid}")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    p = lesson_path(sys.argv[1])
    s = p.read_text(encoding="utf-8")
    if "@quiz\n" not in s or "@ref\n" not in s:
        sys.exit("@quiz 또는 @ref 구역이 없다.")
    head, rest = s.split("@quiz\n", 1)
    qb, ref = rest.split("@ref\n", 1)
    items = [b for b in re.split(r"\n(?=Q: )", qb.strip()) if b.strip()]

    keep = sys.argv[2:]
    if not keep:
        print(f"{len(items)}문항")
        for i, b in enumerate(items, 1):
            print(f"  {i:>2}  {b.splitlines()[0][3:70]}")
        return

    idx = []
    for k in keep:
        n = int(k)
        if not 1 <= n <= len(items):
            sys.exit(f"{n}번 문항이 없다. 전체 {len(items)}문항")
        idx.append(n - 1)

    out = head + "@quiz\n" + "\n\n".join(items[i] for i in idx) + "\n\n@ref\n" + ref
    tmp = p.with_suffix(".md.tmp")
    tmp.write_text(out, encoding="utf-8")
    os.replace(tmp, p)
    print(f"{len(items)}문항 → {len(idx)}문항")


if __name__ == "__main__":
    main()
