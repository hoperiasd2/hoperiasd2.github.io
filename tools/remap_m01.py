#!/usr/bin/env python3
"""Cooper 9판 재편성에 따라 집필된 M01 수업을 새 자리로 옮긴다.

내용은 그대로 두고 수업 ID와 경로만 바꾼다. 옮길 자리가 이미 다른 집필본으로
차 있으면 멈춘다. 실행 전 `--dry` 로 계획을 먼저 확인한다.

    python3 tools/remap_m01.py --dry
    python3 tools/remap_m01.py
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAGE = ROOT / ".remap-stage"

# 주제 → 9판 기준 새 수업 ID
PLAN = {
    "세포의 기원": "M01-W05-L01",
    "생체분자와 막": "M01-W05-L02",
    "유전정보의 흐름": "M01-W05-L03",
    "재조합 DNA": "M01-W06-L01",
    "유전자와 유전체의 구성": "M01-W06-L02",
    "DNA 복제·복구와 유전체 재배열": "M01-W07-L01",
    "전사와 RNA polymerase": "M01-W07-L02",
    "RNA 가공": "M01-W07-L02",
    "전사 조절": "M01-W07-L03",
    "Chromatin과 후성유전": "M01-W07-L03",
    "단백질 합성": "M01-W08-L01",
    "번역 후": "M01-W08-L02",
    "유전체·단백체": "M01-W08-L03",
    "핵과 핵-세포질 수송": "M01-W09-L01",
    "단백질 표적화": "M01-W09-L02",
    "생체에너지": "M01-W09-L03",
    "Glycolysis": "M01-W10-L01",
    "산화적 이화": "M01-W10-L01",
    "미토콘드리아": "M01-W10-L02",
    "세포골격": "M01-W10-L03",
    "원형질막": "M01-W11-L01",
    "세포외기질": "M01-W11-L02",
    "세포 신호전달": "M01-W11-L03",
    "세포주기": "M01-W12-L01",
    "세포 재생": "M01-W12-L02",
    "암의 세포생물학": "M01-W12-L03",
}


def path_of(lid):
    m = re.match(r"M01-W(\d{2})-L(\d{2})", lid)
    return ROOT / "curriculum" / "M01" / f"W{m.group(1)}" / f"L{m.group(2)}"


def written(d):
    f = d / "lesson.md"
    return f.exists() and "작성 예정" not in f.read_text(encoding="utf-8")[:4000]


def main():
    dry = "--dry" in sys.argv
    moves = []
    for d in sorted((ROOT / "curriculum" / "M01").glob("W*/L*")):
        if not written(d):
            continue
        txt = (d / "lesson.md").read_text(encoding="utf-8")
        cur = re.search(r"^lesson_id:\s*(\S+)", txt, re.M).group(1)
        title = re.search(r"^title:\s*(.+)$", txt, re.M).group(1)
        dest = next((v for k, v in PLAN.items() if k in title), None)
        if not dest:
            print(f"  대응 없음: {cur}  {title}")
            continue
        if dest != cur:
            moves.append((cur, dest, title))

    if not moves:
        print("옮길 수업이 없습니다.")
        return
    print(f"{len(moves)}건 이동 계획")
    for cur, dest, title in moves:
        occupied = written(path_of(dest)) and dest not in [m[0] for m in moves]
        mark = "  ← 자리 있음(집필본)" if occupied else ""
        print(f"  {cur} → {dest}  {title[:40]}{mark}")
    blocked = [m for m in moves
               if written(path_of(m[1])) and m[1] not in [x[0] for x in moves]]
    if blocked:
        print(f"\n{len(blocked)}건의 목적지가 다른 집필본으로 차 있습니다. 중단합니다.")
        sys.exit(1)
    if dry:
        print("\n--dry 이므로 실행하지 않았습니다.")
        return

    STAGE.mkdir(exist_ok=True)
    for cur, _, _ in moves:
        shutil.move(str(path_of(cur)), str(STAGE / cur))
    for cur, dest, _ in moves:
        dst = path_of(dest)
        if dst.exists():
            shutil.rmtree(dst)
        shutil.move(str(STAGE / cur), str(dst))
        f = dst / "lesson.md"
        f.write_text(re.sub(r"^lesson_id:.*$", f"lesson_id: {dest}", 
                            f.read_text(encoding="utf-8"), count=1, flags=re.M),
                     encoding="utf-8")
        for j in ("sources.json", "figures.json"):
            q = dst / j
            if q.exists():
                q.write_text(q.read_text(encoding="utf-8").replace(cur, dest), encoding="utf-8")
    STAGE.rmdir()
    print(f"\n{len(moves)}건 이동 완료. build_lesson.py --all 과 build_site.py 를 다시 실행하세요.")


if __name__ == "__main__":
    main()
