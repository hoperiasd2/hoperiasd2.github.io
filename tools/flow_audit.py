#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""절이 앞 내용과 이어지지 않고 갑자기 시작하는 자리를 찾는다.

교재는 한 편이 하나의 논증으로 읽혀야 한다. 절마다 앞에서 세운 것과
남은 질문을 짚고 들어가지 않으면, 내용이 아무리 좋아도 독자는 매 절에서
다시 길을 찾아야 한다. 이 도구는 그런 절을 세어 보완 대상을 고른다.

사용:
    python3 tools/flow_audit.py                      M01·M02 전체
    python3 tools/flow_audit.py 'curriculum/M01/W06/L*/lesson.md'
"""
import re, glob, sys
PAT = sys.argv[1] if len(sys.argv)>1 else 'curriculum/M0[12]/W*/L*/lesson.md'
# 앞 내용과 잇는 표현
BRIDGE = re.compile(r"(앞 절|앞에서|앞 수업|지금까지|여기까지|여기서|그런데|이제|그렇다면|다음 질문|이 질문|위에서|방금|앞의|이어서|남은 문제|그 다음|이번 절|이 절)")
tot=0; abrupt=0; rows=[]
for f in sorted(glob.glob(PAT)):
    txt=open(f,encoding='utf-8').read()
    if '작성 예정' in txt[:4000]: continue
    lid='-'.join(re.search(r'(M\d\d)/(W\d\d)/(L\d\d)',f).groups())
    body=txt.split('---',2)[2] if txt.startswith('---') else txt
    body=re.split(r'^@ref\s*$',body,flags=re.M)[0]
    parts=re.split(r'^@sec ',body,flags=re.M)[1:]
    bad=[]
    for p in parts:
        head,_,rest=p.partition('\n')
        if '연결' in head or '들어가며' in head: continue
        first=''
        for ln in rest.split('\n'):
            s=ln.strip()
            if not s: continue
            if s.startswith(('@','|','- ','=> ','>> ','~ ','> ')) or re.match(r'^\d{1,2}[.)]',s): continue
            first=s; break
        if not first: continue
        tot+=1
        lead=' '.join(re.split(r'(?<=[.다])\s', first)[:2])[:160]
        if not BRIDGE.search(lead):
            abrupt+=1; bad.append(head.strip()[:38])
    if bad: rows.append((lid,len(parts),len(bad),bad))
rows.sort(key=lambda r:-r[2])
print(f"전체 절 {tot}개 중 앞과 잇는 표현이 없는 절 {abrupt}개 ({abrupt/tot*100:.0f}%)\n")
for lid,n,b,bad in rows[:18]:
    print(f"{lid}  {b}/{n}절  → {' / '.join(bad[:4])}")
