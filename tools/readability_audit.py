#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""수업 본문에서 이해하기 어려운 지점을 기계적으로 찾는다.

기초부터 쌓아 올라가는 교재가 목표이므로, 용어를 설명 없이 던진 자리와
들어가는 문턱이 높은 편을 찾아 보완 대상을 고르는 데 쓴다. 지표는
가리키는 용도이고 판단은 본문을 읽어서 한다.

지표
  onramp   첫 절의 첫 문단이 정의로 시작하는가. 용어를 먼저 던지면 낮다.
  density  문단당 영문 전문용어 수. 높으면 설명 없이 용어가 쌓인 것이다.
  undef    본문에서 정의 없이 처음 등장하는 영문 용어 수
  long     500자를 넘는 문단 수
  nosum    핵심 정리(=>)가 4절 이상 간격으로 벌어진 구간 수
"""
import re, glob, sys

PAT = sys.argv[1] if len(sys.argv) > 1 else 'curriculum/M0[12]/W*/L*/lesson.md'

DEF_PAT = re.compile(r"(이란|이라 한다|이라고 한다|라 한다|라고 한다|를 뜻한다|을 뜻한다|이다\.|다\. 즉|말한다|부른다|부르며|정의한다)")
TERM = re.compile(r"\b([A-Z][A-Za-z0-9\-]{2,}|[a-z][a-z0-9\-]{3,}(?:\s[a-z]{3,})?)\b")
STOP = set("""the and for with from that this these those are was were been being have has had
not but all any can its it is of in on to as by or at be we you they he she him her his
one two three four five six seven eight nine ten per via vs etc ed eds vol no pp doi
nat cell science nature rev annu biol chem med engl proc natl acad usa genet
et al mol cancer res clin invest curr opin trends front immunol physiol
pdf isbn http https www org com""".split())

def paragraphs(body):
    out=[]
    for blk in re.split(r"\n\s*\n", body):
        s=blk.strip()
        if not s: continue
        if s.startswith(("@","|","- ","=> ",">> ","~ ","> ","Q: ","A: ")): continue
        if re.match(r"^\d{1,2}[.)]\s", s): continue
        out.append(s)
    return out

rows=[]
for f in sorted(glob.glob(PAT)):
    txt=open(f,encoding='utf-8').read()
    if '작성 예정' in txt[:4000]: continue
    lid='-'.join(re.search(r'(M\d\d)/(W\d\d)/(L\d\d)',f).groups())
    body = txt.split('---',2)[2] if txt.startswith('---') else txt
    # 참고문헌 제외
    body = re.split(r'^@ref\s*$', body, flags=re.M)[0]
    secs = re.split(r'^@sec ', body, flags=re.M)[1:]
    paras = paragraphs(body)
    if not paras: continue

    # 1) 온램프: 1절 첫 문단
    first = paragraphs('\n\n'.join(secs[0].split('\n',1)[1:]) ) if secs else []
    onramp = 1 if (first and DEF_PAT.search(first[0][:260])) else 0

    # 2) 용어 밀도와 정의 없는 용어
    seen=set(); undef=[]
    terms_total=0
    for p in paras:
        ts=[m.group(1) for m in TERM.finditer(p)]
        ts=[x for x in ts if x.lower() not in STOP and not x.isdigit()]
        terms_total+=len(ts)
        for x in ts:
            k=x.lower()
            if k in seen: continue
            seen.add(k)
            # 처음 등장한 문장에 정의 표현이 있는가
            for sent in re.split(r'(?<=[.다])\s', p):
                if x in sent:
                    if not DEF_PAT.search(sent): undef.append(x)
                    break
    density = terms_total/len(paras)

    long_p = sum(1 for p in paras if len(p)>500)

    # 3) 핵심 정리 간격
    marks=[i for i,s in enumerate(secs) if re.search(r'^=> ', s, re.M)]
    gaps=0; prev=-1
    for i in marks+[len(secs)]:
        if i-prev>4: gaps+=1
        prev=i

    rows.append((lid, len(secs), len(paras), onramp, round(density,1), len(undef), long_p, gaps, undef[:6]))

rows.sort(key=lambda r:(-r[4], -r[6], r[3]))
print(f"{'lesson':<12}{'절':>3}{'문단':>5}{'온램프':>6}{'밀도':>6}{'미정의':>7}{'장문단':>7}{'정리틈':>7}")
for r in rows:
    print(f"{r[0]:<12}{r[1]:>3}{r[2]:>5}{r[3]:>6}{r[4]:>6}{r[5]:>7}{r[6]:>7}{r[7]:>7}")
print()
print("=== 용어 밀도 상위 10편의 정의 없는 용어 예 ===")
for r in rows[:10]:
    print(r[0], '|', ', '.join(r[8]))
