#!/usr/bin/env python3
"""즉석 입력을 수업으로 보내고, 저장된 입력 명령을 관리한다.

사용:
    python3 tools/inbox.py                   INBOX.md와 inbox/ 의 .md 파일을 각 수업으로 보낸다
    python3 tools/inbox.py --show            보낸 뒤 각 수업에 쌓인 입력을 모아 본다
    python3 tools/inbox.py --snippets        저장된 입력 명령 목록
    python3 tools/inbox.py --save 이름       표준입력을 입력 명령으로 저장한다
    python3 tools/inbox.py --dry             보내지 않고 무엇이 어디로 갈지만 보인다

강의록 페이지의 '수정' 단추로 내려받은 파일도 inbox/ 에 넣으면 같이 처리된다.
처리한 파일은 inbox/done/ 으로 옮긴다.

형식:
    ## M03-W05-L02
    @img https://example.org/xist.png | Xist가 X 염색체를 덮는 과정
    > 이 부분은 lncRNA 절 뒤에 넣어라
"""
import csv
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox" / "INBOX.md"
SNIP = ROOT / "tools" / "snippets"

TEMPLATE = """<!-- 즉석 입력 칸.

여기에 적은 것은 `python3 tools/inbox.py` 를 돌리면 각 수업 폴더의 notes.md 로
옮겨지고, 다음 빌드에서 그 수업 페이지의 '보강 입력' 항목으로 나타난다.
옮겨진 뒤 이 파일은 비워진다.

쓰는 방법
  ## M03-W05-L02                     ← 수업 ID로 구역을 연다
  아무 문장이나 적는다                  ← 본문 문단이 된다
  - 불릿도 된다
  @img <주소> | <설명>                ← 외부 이미지를 주소로 가져온다
  > 지시사항                           ← 임상 연계 상자로 표시된다
  @use <이름>                         ← 저장된 입력 명령을 불러온다

저장된 입력 명령은 `python3 tools/inbox.py --snippets` 로 확인한다.
-->

"""


def rows():
    with (ROOT / "curriculum.csv").open(encoding="utf-8") as f:
        return {r["lesson_id"]: r for r in csv.DictReader(f)}


def split_sections(text):
    """'## <수업ID>' 단위로 쪼갠다."""
    out, cur, buf = [], None, []
    for ln in text.split("\n"):
        m = re.match(r"^##\s+([A-Z]\d{2}-W\d{2}-L\d{2})\s*$", ln.strip())
        if m:
            if cur:
                out.append((cur, buf))
            cur, buf = m.group(1), []
            continue
        if cur is not None:
            buf.append(ln)
    if cur:
        out.append((cur, buf))
    return out


def inputs():
    """INBOX.md 와 inbox/ 에 들어온 .md 파일을 모은다."""
    out = []
    if INBOX.exists():
        out.append(INBOX)
    for f in sorted(INBOX.parent.glob("*.md")):
        if f != INBOX and f.name.upper() != "README.MD":
            out.append(f)
    return out


def dispatch(dry=False):
    INBOX.parent.mkdir(parents=True, exist_ok=True)
    if not INBOX.exists():
        INBOX.write_text(TEMPLATE, encoding="utf-8")
        print(f"입력 칸을 만들었다: {INBOX.relative_to(ROOT)}")

    known, n, used = rows(), 0, []
    for src in inputs():
        text = re.sub(r"<!--.*?-->", "", src.read_text(encoding="utf-8"), flags=re.S)
        secs = split_sections(text)
        if not secs:
            continue
        print(f"{src.relative_to(ROOT)}")
        sent = 0
        for lid, body in secs:
            body = "\n".join(body).strip("\n")
            if not body.strip():
                continue
            if lid not in known:
                print(f"  건너뜀 {lid}: curriculum.csv에 없는 수업 ID")
                continue
            d = ROOT / known[lid]["path"]
            print(f"  {lid} → {d.relative_to(ROOT)}/notes.md  ({len(body)}자)")
            if dry:
                continue
            d.mkdir(parents=True, exist_ok=True)
            f = d / "notes.md"
            old = f.read_text(encoding="utf-8") if f.exists() else ""
            f.write_text(f"{old}\n\n{body}\n".lstrip("\n")
                         if old.strip() else f"{body}\n", encoding="utf-8")
            sent += 1
        if sent:
            n += sent
            used.append(src)

    if dry:
        return n
    if not n:
        print("보낼 입력이 없다.")
        return 0

    done = INBOX.parent / "done"
    for src in used:
        if src == INBOX:
            INBOX.write_text(TEMPLATE, encoding="utf-8")
        else:
            done.mkdir(parents=True, exist_ok=True)
            src.replace(done / src.name)
    print(f"\n{n}개 수업으로 보냈다. 입력 칸을 비우고 받은 파일은 inbox/done/ 으로 옮겼다.")
    print("다음: python3 tools/build_lesson.py <수업ID>  (또는 --all)")
    return n


def show():
    known = rows()
    found = False
    for lid, r in known.items():
        f = ROOT / r["path"] / "notes.md"
        if not f.exists():
            continue
        t = re.sub(r"<!--.*?-->", "", f.read_text(encoding="utf-8"), flags=re.S).strip()
        if not t:
            continue
        found = True
        print(f"\n=== {lid}  {r['title']}")
        print(t)
    if not found:
        print("쌓인 보강 입력이 없다.")


def snippets():
    SNIP.mkdir(parents=True, exist_ok=True)
    fs = sorted(SNIP.glob("*.md"))
    if not fs:
        print("저장된 입력 명령이 없다.")
        return
    print("저장된 입력 명령 (lesson.md나 INBOX.md에서 '@use 이름' 으로 부른다)\n")
    for f in fs:
        t = f.read_text(encoding="utf-8")
        desc = ""
        m = re.search(r"^desc:\s*(.+)$", t, re.M)
        if m:
            desc = m.group(1).strip()
        print(f"  @use {f.stem:<16} {desc}")


def save(name):
    SNIP.mkdir(parents=True, exist_ok=True)
    body = sys.stdin.read().rstrip("\n")
    if not body.strip():
        print("표준입력이 비어 있다.")
        return
    f = SNIP / f"{name}.md"
    f.write_text(f"---\nname: {name}\ndesc: \nsaved: {date.today()}\n---\n{body}\n",
                 encoding="utf-8")
    print(f"저장했다: {f.relative_to(ROOT)}  →  @use {name}")


def main():
    a = sys.argv[1:]
    if not a:
        dispatch()
    elif a[0] == "--dry":
        dispatch(dry=True)
    elif a[0] == "--show":
        dispatch()
        show()
    elif a[0] == "--snippets":
        snippets()
    elif a[0] == "--save" and len(a) > 1:
        save(a[1])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
