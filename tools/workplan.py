#!/usr/bin/env python3
"""집필 작업을 묶음으로 나누고 진행 상태를 WORKPLAN.md에 남긴다.

중단되어도 이 파일만 보면 어디부터 이어서 할지 알 수 있다.
상태는 curriculum.csv에서 매번 다시 읽으므로 따로 관리할 필요가 없다.

    python3 tools/workplan.py            WORKPLAN.md 갱신
    python3 tools/workplan.py --next     다음에 할 묶음만 출력
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "WORKPLAN.md"

# 묶음 정의: (번호, 이름, 수업 ID 접두 범위)
BATCHES = [
    ("B01", "M01 인체 계통 요약 (1~2주)",
     ["M01-W01-L01", "M01-W01-L02", "M01-W01-L03", "M01-W02-L01", "M01-W02-L02", "M01-W02-L03"]),
    ("B02", "M01 인체 계통 요약 (3~4주)",
     ["M01-W03-L01", "M01-W03-L02", "M01-W03-L03", "M01-W04-L01", "M01-W04-L02", "M01-W04-L03"]),
    ("B03", "M01 Cooper 5~8장",
     ["M01-W06-L03", "M01-W07-L01", "M01-W07-L02", "M01-W07-L03", "M01-W08-L01"]),
    ("B04", "M01 Cooper 10~13장",
     ["M01-W08-L03", "M01-W09-L01", "M01-W10-L01", "M01-W10-L02"]),
    ("B05", "M01 Cooper 14~19장",
     ["M01-W10-L03", "M01-W11-L01", "M01-W11-L02", "M01-W11-L03",
      "M01-W12-L01", "M01-W12-L02", "M01-W12-L03"]),
    ("B06", "M02 기본대사 (1~3주)",
     ["M02-W01-L01", "M02-W01-L02", "M02-W01-L03", "M02-W02-L01", "M02-W02-L02",
      "M02-W02-L03", "M02-W03-L01", "M02-W03-L02", "M02-W03-L03"]),
    ("B07", "M02 당대사 (4~6주)",
     ["M02-W04-L01", "M02-W04-L02", "M02-W04-L03", "M02-W05-L01", "M02-W05-L02",
      "M02-W05-L03", "M02-W06-L01", "M02-W06-L02", "M02-W06-L03"]),
    ("B08", "M02 질소대사와 지질 마무리 (9~11주)",
     ["M02-W09-L01", "M02-W09-L03", "M02-W10-L02", "M02-W10-L03",
      "M02-W11-L01", "M02-W11-L02", "M02-W11-L03"]),
    ("B09", "M02 대사조절과 질환 (12~14주)",
     ["M02-W12-L01", "M02-W12-L02", "M02-W12-L03", "M02-W13-L01", "M02-W13-L02",
      "M02-W13-L03", "M02-W14-L01", "M02-W14-L02", "M02-W14-L03"]),
    ("B10", "M03 분자유전학 (1~2주, 5~6주)",
     ["M03-W01-L01", "M03-W01-L02", "M03-W01-L03", "M03-W02-L01", "M03-W02-L02",
      "M03-W02-L03", "M03-W05-L02", "M03-W05-L03", "M03-W06-L01", "M03-W06-L02",
      "M03-W06-L03"]),
    ("B11", "M03 계통별 의학생화학특론 (7~10주)",
     ["M03-W07-L01", "M03-W07-L02", "M03-W07-L03", "M03-W08-L01", "M03-W08-L02",
      "M03-W08-L03", "M03-W09-L01", "M03-W09-L02", "M03-W09-L03",
      "M03-W10-L01", "M03-W10-L02", "M03-W10-L03"]),
    ("B12", "M03 계통별 의학생화학특론 (11~14주)",
     ["M03-W11-L01", "M03-W11-L02", "M03-W11-L03", "M03-W12-L01", "M03-W12-L02",
      "M03-W12-L03", "M03-W13-L01", "M03-W13-L02", "M03-W13-L03",
      "M03-W14-L01", "M03-W14-L02", "M03-W14-L03"]),
]


def load():
    with (ROOT / "curriculum.csv").open(encoding="utf-8") as f:
        return {r["lesson_id"]: r for r in csv.DictReader(f)}


def main():
    rows = load()
    only_next = "--next" in sys.argv
    out = ["# 집필 작업 계획", "",
           "`curriculum.csv`의 상태에서 매번 다시 계산한다. 중단되어도 이 표를 보고 이어서 하면 된다.",
           "묶음 하나를 작업자 한 명에게 맡긴다. 작업자는 한 편을 그림까지 끝내고 `tools/qa_lesson.py`를",
           "통과시킨 뒤 다음 편으로 넘어간다.", "", "## 묶음", "",
           "| 묶음 | 범위 | 완료 | 전체 | 상태 |", "|---|---|---:|---:|---|"]
    nxt = None
    for code, name, ids in BATCHES:
        done = sum(1 for i in ids if rows.get(i, {}).get("status", "설계") != "설계")
        state = "완료" if done == len(ids) else ("진행" if done else "대기")
        if state != "완료" and nxt is None:
            nxt = (code, name, ids, done)
        out.append(f"| {code} | {name} | {done} | {len(ids)} | {state} |")

    tot = sum(len(i) for _, _, i in BATCHES)
    dn = sum(1 for _, _, ids in BATCHES for i in ids
             if rows.get(i, {}).get("status", "설계") != "설계")
    out += ["", f"합계 {dn} / {tot}편", "", "## 묶음별 수업", ""]
    for code, name, ids in BATCHES:
        out.append(f"### {code} {name}")
        out.append("")
        for i in ids:
            r = rows.get(i, {})
            st = r.get("status", "설계")
            mark = "x" if st != "설계" else " "
            out.append(f"- [{mark}] `{i}` {r.get('title', '')}")
        out.append("")
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")

    if only_next and nxt:
        code, name, ids, done = nxt
        todo = [i for i in ids if rows.get(i, {}).get("status", "설계") == "설계"]
        print(f"다음 묶음: {code} {name}  ({done}/{len(ids)} 완료)")
        print("남은 수업:")
        for i in todo:
            print(f"  {i}  {rows.get(i, {}).get('title', '')}")
    else:
        print(f"WORKPLAN.md 갱신: {dn}/{tot}편 완료")
        if nxt:
            print(f"다음 묶음: {nxt[0]} {nxt[1]}")


if __name__ == "__main__":
    main()
