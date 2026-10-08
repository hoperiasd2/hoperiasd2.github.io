#!/usr/bin/env python3
"""refs/decks/ 의 참고 자료 색인을 만든다. Lippincott 장 번호는 수업에 자동 대응시킨다."""
import re
from pathlib import Path

DECKS = Path("/home/user/refs/decks")

# Lippincott 장 → 수업 ID (PROJECT.md의 편성 기준)
CH2LESSON = {
    1: "M02-W01-L01", 2: "M02-W01-L02", 3: "M02-W01-L03", 4: "M02-W02-L01",
    5: "M02-W02-L02 · M02-W02-L03", 6: "M02-W03-L01 · M02-W03-L02",
    7: "M02-W03-L03", 8: "M02-W04-L01 · M02-W04-L02", 9: "M02-W04-L03 · M02-W05-L01",
    10: "M02-W05-L02", 11: "M02-W05-L03 · M02-W06-L01", 12: "M02-W06-L02",
    13: "M02-W06-L03", 14: "M02-W03-L03", 15: "M02-W07-L01",
    16: "M02-W07-L02 · M02-W07-L03 · M02-W08-L01 · M02-W08-L02",
    17: "M02-W08-L03", 18: "M02-W09-L02 · M02-W09-L03",
    19: "M02-W10-L01 · M02-W10-L02", 20: "M02-W10-L03 · M02-W11-L01",
    21: "M02-W11-L02", 22: "M02-W11-L03", 23: "M02-W12-L01",
    24: "M02-W12-L02", 25: "M02-W13-L03", 26: "M02-W14-L01",
    27: "M02 보조 (영양)", 28: "M02 보조 (비타민)", 29: "M02 보조 (무기질)",
    30: "M03-W01-L01 ~ M03-W02-L01", 31: "M03-W02-L02 · M03-W02-L03 · M03-W03-L01",
    32: "M03-W05-L03 ~ M03-W06-L03", 33: "M03-W04-L02 · M03-W04-L03 · M03-W05-L01",
    34: "M03-W05-L03 ~ M03-W06-L03",
}
MANUAL = {
    "ref-01": ("분자생물학의 기초 (Cooper 4장)", "M01-W06-L02"),
    "ref-03": ("대사의 기초 · 미토콘드리아", "M01-W10-L02 · M02-W03"),
    "ref-04": ("세포소기관 2. 세포막", "M01-W11-L01 · M01-W05-L02"),
    "ref-gene-regulation": ("유전자조절의 기초와 원핵생물 유전자조절", "M01-W08-L03 · M03-W04-L02"),
    "gb-01": ("일반생물학 — 내분비계와 신경계에 의한 조절", "M01-W02-L02"),
    "gb-23": ("일반생물학 ch32 — Control by nervous and endocrine systems", "M01-W02-L02"),
    "gb-02": ("일반생물학 ch34 — Reproduction 생식과 발생", "M01-W02-L03 · M01-W03-L01"),
    "gb-03": ("일반생물학 — Kidneys 신장과 배설", "M01-W02-L01"),
    "gb-01b": ("일반생물학 ch37 — Animal Behavior 동물의 행동", "M01-W03-L02"),
}


def first_title(md):
    for ln in md.read_text(encoding="utf-8", errors="ignore").split("\n"):
        m = re.match(r"^## \d+\.\s*(.+)", ln)
        if m and m.group(1).strip():
            return m.group(1).strip()[:70]
    return ""


def main():
    rows_lip, rows_other = [], []
    for md in sorted(DECKS.glob("*.md")):
        if md.name == "INDEX.md":
            continue
        txt = md.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"- 슬라이드 (\d+)장", txt)
        n = m.group(1) if m else "—"
        stem = md.stem
        ch = re.search(r"[Cc]h(?:apter)?\.?(\d{1,2})", stem)
        if ch and "Lippincott" in stem or (ch and stem.startswith("Chapter")):
            c = int(ch.group(1))
            rows_lip.append((c, md.name, first_title(md), n, CH2LESSON.get(c, "미정")))
        elif stem in MANUAL:
            t, target = MANUAL[stem]
            rows_other.append((md.name, t, n, target))
        else:
            rows_other.append((md.name, first_title(md), n, "미정"))

    out = ["# 참고 강의 자료 색인", "",
           "사용자가 실제로 강의한 자료다. `*.md`는 각 파일에서 추출한 텍스트이고 원본은 같은 이름의 `.ppt`·`.pptx`·`.pdf`다.",
           "",
           "**다루는 범위와 깊이, 설명 순서, 사용한 용어를 참고하되 문장을 그대로 옮기지 않는다.** 본문은",
           "`tools/WRITING_GUIDE.md`의 기준에 맞춰 새로 쓴다. 참고 자료에 없는 내용이라도 교재 수준에서",
           "필요하면 넣는다.", "",
           "## Lippincott 장별 슬라이드", "",
           "| 장 | 파일 | 내용 | 장수 | 대응 수업 |", "|---:|---|---|---:|---|"]
    for c, f, t, n, lesson in sorted(rows_lip):
        out.append(f"| {c} | `{f}` | {t} | {n} | {lesson} |")

    out += ["", "## 그 밖의 강의 자료", "",
            "| 파일 | 내용 | 장수 | 대응 수업 |", "|---|---|---:|---|"]
    for f, t, n, lesson in sorted(rows_other):
        out.append(f"| `{f}` | {t} | {n} | {lesson} |")

    out += ["", "## 사용 방법", "",
            "1. 담당 수업에 대응하는 파일이 있으면 먼저 읽는다. 경로는 `/home/user/refs/decks/<파일명>`이다.",
            "2. 범위와 순서, 용어를 참고한다. 교재가 어디까지 다루는지 가늠하는 용도다.",
            "3. 본문은 새로 쓴다. 문장을 복사하지 않는다.",
            "4. 새 자료가 들어오면 `python3 tools/ingest_refs.py` 로 받아들이고 이 스크립트로 색인을 다시 만든다."]
    (DECKS / "INDEX.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"색인 갱신: Lippincott {len(rows_lip)}건 · 그 밖 {len(rows_other)}건")


if __name__ == "__main__":
    main()
