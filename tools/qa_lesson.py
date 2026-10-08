#!/usr/bin/env python3
"""집필된 수업이 PROJECT.md의 기준을 지켰는지 확인한다.

사용:
    python3 tools/qa_lesson.py            집필된 모든 수업
    python3 tools/qa_lesson.py M02-W09-L02
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 금지 용어 → 대체어
BANNED = {
    "율속": "rate-limiting step", "측쇄": "side chain",
    "수산기": "hydroxyl기", "수산화": "hydroxylation",
    "탈탄산": "decarboxylation", "활면소포체": "smooth ER", "조면소포체": "rough ER",
    "양친매성": "amphipathic", "유화": "emulsification",
    "세포내섭취": "endocytosis", "피막소포": "coated vesicle",
    "사구대": "zona glomerulosa", "속상대": "zona fasciculata", "망상대": "zona reticularis",
    "해당과정": "glycolysis", "당신생": "gluconeogenesis", "당원": "glycogen",
    "구연산 회로": "TCA cycle", "전자전달계": "electron transport chain",
    "상전이 온도": "phase transition temperature", "지질방울": "lipid droplet",
    "담즙정체": "cholestasis",
}

# 금지어가 부분 문자열로 들어가지만 그 자체로는 올바른 용어
EXEMPT = (
    "섬유화", "섬유증", "섬유소", "섬유아세포",   # 유화
)
# 금지 비유
METAPHOR = ["공장", "열쇠와 자물쇠", "택배", "도로처럼", "자물쇠와 열쇠"]
# 내용 없는 강조
FILLER = ["매우 중요하다", "핵심이라고 할 수 있다", "라고 할 수 있다"]

HANGUL = re.compile(r"[가-힣]")

MIN = {"secs": 7, "chars": 10000, "figs": 3, "quiz": 5, "refs": 5}
SLIDES = (38, 52)


def check(row):
    lid = row["lesson_id"]
    d = ROOT / row["path"]
    src = d / ("protocol.md" if row["kind"] == "practicum" else "lesson.md")
    if not src.exists():
        return None
    text = src.read_text(encoding="utf-8")
    if "작성 예정" in text[:4000]:
        return None

    body = text.split("---", 2)[2] if text.startswith("---") else text
    problems, notes = [], {}

    notes["secs"] = len(re.findall(r"^@sec ", body, re.M))
    notes["figs"] = len(re.findall(r"^@fig ", body, re.M))
    notes["quiz"] = len(re.findall(r"^Q: ", body, re.M))
    refs = re.search(r"^@ref\s*$(.*?)(?=^@|\Z)", body, re.M | re.S)
    notes["refs"] = len(re.findall(r"^- ", refs.group(1), re.M)) if refs else 0
    notes["chars"] = len(re.sub(r"\s", "", body))

    for k, lo in MIN.items():
        if notes[k] < lo:
            problems.append(f"{k} {notes[k]} < {lo}")

    # 금지 용어 (정상 용어에 부분 문자열로 포함되는 경우는 제외한다)
    scrub = body
    for w in EXEMPT:
        scrub = scrub.replace(w, "")
    for w, alt in BANNED.items():
        if w in scrub:
            problems.append(f"금지어 '{w}' → {alt}")
    for w in METAPHOR:
        if w in body:
            problems.append(f"비유 '{w}'")
    for w in FILLER:
        if w in body:
            problems.append(f"상투어 '{w}'")

    # 그림 파일과 그림 속 한글
    for fid in re.findall(r"^@fig (\S+)", body, re.M):
        found = None
        for ext in (".svg", ".png", ".jpg", ".jpeg", ".webp"):
            if (d / "assets" / f"{fid}{ext}").exists():
                found = d / "assets" / f"{fid}{ext}"
                break
        if not found:
            problems.append(f"그림 파일 없음: {fid}")
        elif found.suffix == ".svg":
            svg = found.read_text(encoding="utf-8", errors="ignore")
            vis = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
            vis = re.sub(r'aria-label="[^"]*"', "", vis)
            if HANGUL.search(vis):
                problems.append(f"SVG 안에 한글: {fid}")
            if not re.search(r'viewBox="', svg):
                problems.append(f"viewBox 없음: {fid}")

    # 슬라이드 장수
    pptx = d / "slides.pptx"
    if pptx.exists():
        try:
            from pptx import Presentation
            n = len(Presentation(str(pptx)).slides)
            notes["slides"] = n
            if not (SLIDES[0] <= n <= SLIDES[1]):
                problems.append(f"슬라이드 {n}장 (기준 {SLIDES[0]}~{SLIDES[1]})")
        except Exception as e:
            problems.append(f"슬라이드 열기 실패: {e}")
    else:
        problems.append("슬라이드 없음")

    return lid, notes, problems


def main():
    with (ROOT / "curriculum.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    want = sys.argv[1] if len(sys.argv) > 1 else None
    results = [r for r in (check(x) for x in rows
                           if not want or x["lesson_id"] == want) if r]
    if not results:
        print("집필된 수업이 없습니다.")
        return
    bad = 0
    for lid, n, probs in results:
        mark = "OK " if not probs else "NG "
        print(f"{mark}{lid}  절{n['secs']} 그림{n['figs']} 문항{n['quiz']} "
              f"출처{n['refs']} {n['chars']:,}자 슬라이드{n.get('slides','-')}")
        for p in probs:
            print(f"      - {p}")
        bad += bool(probs)
    print(f"\n{len(results)}편 중 {len(results)-bad}편 통과, {bad}편 수정 필요")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
