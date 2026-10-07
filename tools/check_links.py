#!/usr/bin/env python3
"""생성된 사이트의 내부 링크가 모두 실제 파일을 가리키는지 확인한다."""
import re, sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
HREF = re.compile(r'(?:href|src)="([^"]+)"')
bad, checked = [], 0

for f in ROOT.rglob("*.html"):
    if ".git" in f.parts:
        continue
    for raw in HREF.findall(f.read_text(encoding="utf-8", errors="ignore")):
        u = urlparse(raw)
        if u.scheme or raw.startswith(("#", "mailto:", "//", "data:")) or "${" in raw:
            continue
        target = (f.parent / unquote(u.path)).resolve()
        checked += 1
        if not target.exists():
            bad.append(f"{f.relative_to(ROOT)} → {raw}")

print(f"내부 링크 {checked}개 검사")
if bad:
    print(f"끊어진 링크 {len(bad)}개:")
    for b in bad[:25]:
        print("  " + b)
    sys.exit(1)
print("끊어진 링크 없음")
