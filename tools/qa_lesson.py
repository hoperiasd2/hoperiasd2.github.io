#!/usr/bin/env python3
"""집필된 수업이 PROJECT.md의 기준을 지켰는지 확인한다.

사용:
    python3 tools/qa_lesson.py              집필된 모든 수업
    python3 tools/qa_lesson.py M02-W09-L02
    python3 tools/qa_lesson.py --strict ... 그림 글자 예산 초과도 불통과로 본다

그림 글자 예산은 FIG 에 있다. 새로 그리는 그림은 --strict 로 확인한다.
먼저 쓴 그림은 예산을 넘는 것이 많아 기본값에서는 경고로만 알린다.
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STRICT = "--strict" in sys.argv

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

# 교재로서의 기준. 학부 설명에서 시작해 Step 1 수준의 식별 지점과 연구 전선까지
# 한 수업 안에 모두 들어간다. 분량을 줄여 슬라이드에 맞추지 않는다.
MIN = {"secs": 8, "chars": 22000, "figs": 1, "quiz": 10, "refs": 6,
       "step": 3, "front": 2}
SLIDES = (30, 130)      # 두 편으로 나뉘면 합계로 센다

# 그림은 논문 figure처럼 라벨만 둔다. 설명은 캡션과 SVG 주석으로 옮긴다.
#   one   라벨 한 줄의 길이 한계. 이보다 길면 글자가 그림 밖으로 나가거나 겹친다.
#   chars, nodes 는 권고값이다. 표 형태의 그림은 짧은 칸이 많아 넘을 수 있다.
FIG = {"one": 48, "chars": 380, "nodes": 26}


def is_sentence(t):
    """라벨이 아니라 문장인지 본다. 문장은 캡션과 주석으로 옮겨야 한다."""
    if len(t) > FIG["one"]:
        return True
    if re.search(r"[a-z)\]][.]$", t):          # 마침표로 끝나면 문장이다
        return True
    if re.search(r"[.][ ][A-Z]", t):           # 한 칸 안에 두 문장
        return True
    return False


def fig_text(svg):
    """그림 안에 보이는 글자를 센다. 주석과 aria-label은 설명이므로 빼고 센다."""
    vis = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    vis = re.sub(r"<(desc|title)\b.*?</\1>", "", vis, flags=re.S)
    items = [re.sub(r"<[^>]+>", "", t) for t in
             re.findall(r"<text\b[^>]*>(.*?)</text>", vis, re.S)]
    items = [re.sub(r"\s+", " ", t).strip() for t in items]
    items = [t for t in items if t]
    return items


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
    notes["step"] = len(re.findall(r"^>> ", body, re.M))
    notes["front"] = len(re.findall(r"^~ ", body, re.M))
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

    # 그림 파일과 그림 속 한글, 그리고 그림 안 글자 분량
    fat, hint = [], []
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
            items = fig_text(svg)
            sent = [t for t in items if is_sentence(t)]
            if sent:
                worst = max(sent, key=len)
                fat.append(f"{fid}: 문장 {len(sent)}개 (가장 긴 것 {len(worst)}자) "
                           f"- 캡션과 주석으로 옮긴다")
            total = sum(len(t) for t in items)
            if total > FIG["chars"] or len(items) > FIG["nodes"]:
                hint.append(f"{fid}: 글자 {total}자, text {len(items)}개 "
                            f"(권고 {FIG['chars']}자, {FIG['nodes']}개)")

    # 슬라이드 장수
    pptx = d / "slides.pptx"
    if pptx.exists():
        try:
            from pptx import Presentation
            n = len(Presentation(str(pptx)).slides)
            if (d / "slides-2.pptx").exists():
                n += len(Presentation(str(d / "slides-2.pptx")).slides)
            notes["slides"] = n
            if not (SLIDES[0] <= n <= SLIDES[1]):
                problems.append(f"슬라이드 {n}장 (기준 {SLIDES[0]}~{SLIDES[1]})")
        except Exception as e:
            problems.append(f"슬라이드 열기 실패: {e}")
    else:
        problems.append("슬라이드 없음")

    if fat:
        if STRICT:
            problems += ["그림 안 문장 — " + x for x in fat]
        else:
            notes["fat"] = fat
    if hint:
        notes["hint"] = hint

    return lid, notes, problems


def main():
    with (ROOT / "curriculum.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    args = [a for a in sys.argv[1:] if a != "--strict"]
    want = args[0] if args else None
    results = [r for r in (check(x) for x in rows
                           if not want or x["lesson_id"] == want) if r]
    if not results:
        print("집필된 수업이 없습니다.")
        return
    bad = fatn = 0
    for lid, n, probs in results:
        mark = "OK " if not probs else "NG "
        print(f"{mark}{lid}  절{n['secs']} 그림{n['figs']} 문항{n['quiz']} "
              f"시험{n['step']} 연구{n['front']} 출처{n['refs']} "
              f"{n['chars']:,}자 슬라이드{n.get('slides','-')}")
        for p in probs:
            print(f"      - {p}")
        for x in n.get("fat", []):
            print(f"      ~ 그림 안 문장 {x}")
            fatn += 1
        bad += bool(probs)
    print(f"\n{len(results)}편 중 {len(results)-bad}편 통과, {bad}편 수정 필요")
    if fatn:
        print(f"그림 안에 문장이 남은 그림 {fatn}개. 새로 그릴 때는 라벨만 두고 "
              f"설명을 캡션과 SVG 주석으로 옮긴다. 목록은 tools/fig_audit.py 로 본다.")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
