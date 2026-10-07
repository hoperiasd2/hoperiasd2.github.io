---
lesson_id: M02-W09-L02
title: Cholesterol 항상성과 담즙산·steroid로의 전환
en: Cholesterol Homeostasis and Its Conversion to Bile Acids and Steroids
status: 초안
version: v0.1
---

@obj
- ER 막의 sterol 농도가 SREBP-2를 통해 합성과 흡수를 동시에 조절하는 구조를 설명한다.
- HMG-CoA reductase가 전사·분해·인산화의 세 수준에서 조절되는 방식과 그 임상적 의미를 설명한다.
- Statin과 ezetimibe, PCSK9 억제제가 각각 어느 지점에 작용하며 왜 병용이 추가 효과를 내는지 설명한다.
- Cholesterol이 분해되지 않는 분자이므로 담즙산 전환과 배출이 유일한 제거 경로임을 설명한다.
- Steroid 생성 조직이 LDL에 의존하는 이유와 StAR·CYP11A1 결손의 표현형을 연결한다.
- HDL의 역수송 경로를 설명하고 HDL-C 수치가 치료 표적이 되지 못한 근거를 평가한다.

@prereq
- M02-W09-L01 Eicosanoid와 지질 신호 — isoprenoid 전구체와 지질 신호의 공통 기반
- M02-W07-L01 식이지질의 소화·흡수·운반 — micelle 형성과 chylomicron 경로
- M01-W06-L02 유전정보의 흐름 — 전사인자에 의한 발현 조절의 기본 구조

@sec ER 막의 sterol 농도 하나가 합성과 흡수를 동시에 지시한다
?: 간세포는 cholesterol을 스스로 만들 수도 있고 혈중 LDL에서 받아올 수도 있다. 세포는 둘 중 무엇을 할지 어떻게 정하는가.
!: 세포는 둘 중 하나를 고르지 않는다. ER 막의 cholesterol 농도라는 단일 변수가 SREBP-2를 통해 합성 효소와 흡수 수용체를 같은 방향으로 함께 켜고 끈다.

**SREBP-2**(sterol regulatory element-binding protein 2)는 ER 막에 끼어 있는 전사인자 전구체이며, 막단백 **SCAP**(SREBP cleavage-activating protein)과 복합체를 이룬다. SCAP은 sterol 감지 도메인을 가지고 있어 ER 막의 cholesterol 농도에 따라 입체 구조가 바뀐다.

- ER cholesterol이 충분하면 SCAP이 **Insig**에 결합해 ER에 붙잡힌다. SREBP-2는 전구체 상태로 남고 표적 유전자는 꺼진다.
- ER cholesterol이 떨어지면 SCAP-Insig 결합이 풀린다. 복합체가 COPII 소포를 타고 Golgi로 이동하고, 거기서 **S1P**와 **S2P** 두 단백분해효소가 차례로 자른다. 잘려 나온 N말단 조각(nSREBP-2)이 핵으로 들어가 표적 유전자의 **sterol regulatory element(SRE)**에 결합한다.

핵심은 표적 유전자의 구성이다. SREBP-2는 합성 경로의 **HMG-CoA reductase(HMGCR)**와 흡수 경로의 **LDL receptor(LDLR)**를 함께 유도한다. 세포가 cholesterol이 부족하다고 판단하면 만들기와 가져오기를 동시에 늘리는 것이다. 반대로 sterol이 충분하면 두 경로가 함께 꺼진다.

| 상태 | SCAP-Insig | SREBP-2 | HMGCR | LDLR | PCSK9 |
|---|---|---|---|---|---|
| ER sterol 높음 | 결합, ER 체류 | 전구체로 유지 | ↓ | ↓ | ↓ |
| ER sterol 낮음 | 해리, Golgi 이동 | 절단·핵 이행 | ↑ | ↑ | ↑ |

> 이 모형은 간세포에서 가장 잘 성립한다. 말초 조직은 LDLR 의존도와 합성 능력이 조직마다 달라 같은 비중으로 작동하지 않는다. 또 SREBP-1c는 같은 계열이지만 지방산 합성을 담당하고 insulin과 LXR의 영향을 더 크게 받으므로, SREBP-2의 sterol 되먹임과 구분해야 한다.

=> 이 구조를 알면 뒤이은 모든 약리가 하나의 축으로 설명된다. 간세포의 cholesterol을 어떤 방식으로든 떨어뜨리면 SREBP-2가 켜지고 LDLR이 늘어 혈중 LDL이 제거된다. Statin, ezetimibe, 담즙산 격리제는 출발점이 다를 뿐 모두 이 한 지점으로 수렴한다.

@sec HMG-CoA reductase는 전사·분해·인산화 세 층위에서 조절된다
?: Mevalonate 경로에는 효소가 20개가 넘는데 왜 HMG-CoA reductase 하나만 약물 표적이 되었는가.
!: HMGCR은 비가역적 committed step을 촉매하면서 동시에 세 가지 독립된 조절을 받는 유일한 지점이고, 그 아래 경로가 cholesterol 외의 필수 산물로 갈라지기 때문이다.

HMGCR은 HMG-CoA를 **mevalonate**로 환원하며 NADPH 2분자를 쓴다. 이 반응은 생리적 조건에서 비가역적이고, 경로에서 되돌아갈 수 없는 첫 지점이다. 조절은 세 층위에서 겹친다.

- **전사**: SREBP-2가 SRE를 통해 유도한다. Sterol이 많으면 전사가 줄어든다.
- **단백 분해**: ER 막의 sterol과 lanosterol이 쌓이면 HMGCR의 막 도메인이 Insig과 결합하고, **gp78**과 **TRC8** 같은 E3 ubiquitin ligase가 붙어 분해로 보낸다. 전사 억제보다 빠르게 작동하는 되먹임이다.
- **인산화**: 에너지가 부족해 AMP/ATP 비가 오르면 **AMPK**가 HMGCR을 인산화해 활성을 낮춘다. ATP를 많이 쓰는 합성 경로를 에너지 상태에 맞춰 끄는 장치다.

Mevalonate 아래의 경로는 cholesterol로만 가지 않는다. Farnesyl pyrophosphate에서 갈라져 **ubiquinone(CoQ10)**, **dolichol**, 그리고 Ras·Rho·Rab의 막 고정에 필요한 **prenyl 기**가 만들어진다.

=> Statin이 근육 증상이나 당 대사 변화 같은 cholesterol 저하와 무관해 보이는 효과를 내는 이유의 일부가 여기 있다. 상류를 막으면 하류의 비-sterol 산물도 함께 줄어든다. 다만 CoQ10 보충이 statin 관련 근육 증상을 줄인다는 근거는 무작위 시험에서 일관되지 않으므로, 기전적 설명을 치료 권고로 바로 옮기지 않는다.

@sec Statin의 LDL 저하는 합성 차단이 아니라 수용체 상향의 결과다
?: Statin은 cholesterol 합성을 막는 약인데, 왜 용량을 두 배로 올려도 LDL-C는 6% 정도만 더 떨어지는가.
!: Statin이 LDL-C를 낮추는 실제 경로는 합성 차단 자체가 아니라 그에 따른 SREBP-2 활성화와 LDLR 상향이며, 같은 전사 프로그램이 PCSK9도 함께 올려 LDLR 증가를 스스로 깎아내기 때문이다.

간세포의 cholesterol 합성을 막으면 ER sterol이 떨어지고 SREBP-2가 켜진다. LDLR이 늘어 혈중 LDL 입자의 제거가 빨라지고, 이것이 측정되는 LDL-C 감소의 본체다. 합성이 줄어 혈중 농도가 낮아지는 것이 아니다.

문제는 **PCSK9**도 SREBP-2의 표적이라는 점이다. PCSK9는 분비된 뒤 세포 표면에서 LDLR에 결합하고, LDL과 함께 endosome으로 들어가 LDLR이 재순환하지 못하게 lysosome 분해로 돌린다. Statin은 LDLR 전사를 올리면서 동시에 LDLR 분해 신호도 올린다.

| 단계 | 효과 | 상쇄 요인 |
|---|---|---|
| HMGCR 억제 | ER sterol ↓ | — |
| SREBP-2 활성 | LDLR 전사 ↑ | PCSK9 전사도 ↑ |
| 표면 LDLR 증가 | LDL 제거 ↑ | PCSK9가 LDLR 재순환 차단 |

용량-반응이 평탄해지는 현상을 임상에서는 흔히 **rule of 6**로 부른다. Statin 용량을 두 배로 올릴 때마다 LDL-C가 약 6%씩 추가로 떨어진다는 경험칙이다. 반면 고강도 statin의 시작 용량만으로 이미 50% 안팎의 감소를 얻는다.

> 이 경험칙은 집단 평균이다. 개인의 반응은 유전적 배경, 순응도, 기저 흡수·합성 비중에 따라 크게 다르다. 반응이 기대보다 작을 때 가장 흔한 원인은 약물 저항이 아니라 복약 중단이므로, 용량을 올리기 전에 순응도와 이차성 원인(갑상선기능저하, 신증후군, 폐색성 간담도질환)을 확인한다.

=> PCSK9를 항체로 중화하거나 siRNA로 생산을 줄이면 statin이 만든 LDLR 증가가 깎이지 않는다. 두 약의 병용이 단순한 덧셈이 아니라 서로의 제약을 푸는 조합인 이유가 이것이다.

@sec 식이 cholesterol이 혈중 LDL-C를 생각만큼 올리지 않는 이유
?: 달걀 하나에 cholesterol이 약 200 mg 들어 있는데 왜 섭취량이 혈중 LDL-C로 그대로 이어지지 않는가.
!: 장에서 흡수된 양의 상당 부분이 ABCG5/G8로 장관 내강에 되돌려지고, 흡수된 만큼 간의 합성과 LDLR 발현이 함께 줄어 전체 균형이 보정되기 때문이다.

장 상피세포의 **NPC1L1**이 내강의 미셀에서 cholesterol을 세포 안으로 들인다. 그러나 같은 세포의 정단막에는 **ABCG5/ABCG8** 이종이량체 수송체가 있어 sterol, 특히 식물 sterol을 내강으로 다시 퍼낸다. 결과적으로 식이 cholesterol의 흡수율은 평균 50% 안팎이고 개인차가 20~80%로 넓다.

흡수된 cholesterol이 간에 도달하면 앞 절의 되먹임이 작동한다. ER sterol이 오르면 SREBP-2가 꺼지고 HMGCR과 LDLR이 함께 줄어든다. 내인성 합성이 줄어 섭취 증가를 상쇄하지만, LDLR도 함께 줄기 때문에 혈중 LDL 제거는 느려진다. 두 방향이 겹쳐 순효과가 작아진다.

- **Ezetimibe**는 NPC1L1을 억제해 흡수를 줄인다. 간의 cholesterol이 줄면 SREBP-2가 켜지고 LDLR이 늘어 LDL-C가 추가로 낮아진다. 작용 지점은 장이지만 효과가 나타나는 곳은 간이다.
- **Sitosterolemia**는 *ABCG5* 또는 *ABCG8*의 양쪽 대립유전자 기능 상실로 식물 sterol을 퍼내지 못해 혈중 sitosterol이 수십 배로 오르고 조기 죽상경화와 황색종, 용혈이 나타난다. 이 질환은 ABCG5/G8이 실제로 배출을 담당한다는 사람에서의 증거다.

IMPROVE-IT 시험에서 급성 관동맥증후군 이후 simvastatin에 ezetimibe를 더하자 LDL-C가 69.5에서 53.7 mg/dL로 낮아졌고, 7년 시점 일차 평가변수가 34.7%에서 32.7%로 감소했다(HR 0.936, p=0.016).

> 효과 크기는 크지 않다. 절대 위험 감소 2% 포인트는 고위험군에서 얻은 값이며 저위험군에 그대로 적용되지 않는다. 이 시험의 의미는 효과의 크기보다 "statin 외의 기전으로 LDL을 더 낮춰도 사건이 줄어든다"는 LDL 가설의 검증에 있다.

@sec Cholesterol은 분해되지 않으므로 담즙산으로 바꾸어야만 몸을 떠난다
?: 사람은 cholesterol을 CO₂와 물로 분해할 수 없다. 그렇다면 과잉 cholesterol은 어떻게 제거되는가.
!: 유일한 정량적 제거 경로는 간에서 담즙산으로 전환해 담즙으로 내보내고 장에서 재흡수되지 않은 몫을 대변으로 잃는 것이며, 일부는 담즙 cholesterol 자체로 배출된다.

사람에게는 steroid 고리를 열어 분해하는 효소가 없다. 따라서 제거는 화학적 분해가 아니라 **배출**이다. 두 경로가 있다.

- 간에서 **CYP7A1**(cholesterol 7α-hydroxylase)이 시작하는 고전 경로로 담즙산을 만든다. 이 효소가 담즙산 합성의 율속 단계다.
- 간이 담즙으로 cholesterol을 그대로 내보낸다(ABCG5/G8 경유).

담즙산은 장에서 지방 소화를 돕고 회장 말단에서 **ASBT**를 통해 대부분 재흡수되어 문맥으로 돌아온다. 이 **장간 순환(enterohepatic circulation)** 덕분에 약 3 g의 담즙산 풀이 하루 6~10회 돌며, 대변으로 빠져나가는 양은 하루 약 0.2~0.6 g에 그친다. 간은 잃은 만큼만 새로 합성해 풀을 유지한다.

| 개입 | 즉각 효과 | 간의 반응 | 혈중 LDL-C |
|---|---|---|---|
| 담즙산 격리제(cholestyramine 등) | 장에서 담즙산 결합·배출 | CYP7A1 ↑, 간 cholesterol 소모 | ↓ |
| ASBT 억제제 | 회장 재흡수 차단 | 같은 방향 | ↓ (주 적응증은 담즙정체성 소양증) |
| Ezetimibe | 장 cholesterol 흡수 차단 | SREBP-2 ↑ | ↓ |

=> 담즙산 격리제가 혈중 LDL을 낮추는 기전은 장간 순환을 끊어 간이 담즙산을 새로 만들게 하고, 그 원료로 간의 cholesterol을 소모시켜 결국 LDLR을 올리는 것이다. 약은 흡수되지 않고 장에만 머무는데 효과는 간에서 나타난다.

> 담즙산 격리제는 지용성 비타민과 다른 약물(levothyroxine, warfarin, digoxin 등)의 흡수를 방해하므로 복용 시간을 분리해야 한다. 또 간의 담즙산 합성이 늘면서 triglyceride가 오를 수 있어 고중성지방혈증에서는 적합하지 않다.

@sec 담즙산은 계면활성제이면서 동시에 수용체 리간드다
?: 담즙산의 역할을 지방 유화로만 설명하면 무엇을 놓치는가.
!: 담즙산은 핵수용체 FXR과 막수용체 TGR5의 내인성 리간드로서 자신의 합성량, 간의 지질 대사, 장관 호르몬 분비까지 조절하는 신호분자다.

간세포의 **FXR**(farnesoid X receptor, *NR1H4*)이 담즙산에 결합하면 **SHP**를 유도해 CYP7A1 전사를 억제한다. 담즙산이 자기 합성을 끄는 음성 되먹임이다. 여기에 장 쪽 경로가 더해진다. 회장 상피의 FXR이 활성화되면 **FGF19**(설치류의 FGF15)가 분비되어 문맥을 타고 간에 도달하고, FGFR4-β-Klotho 복합체를 통해 CYP7A1을 억제한다. 간 내부 되먹임과 장-간 내분비 되먹임이 겹쳐 작동한다.

막수용체 **TGR5**(GPBAR1)는 장 내분비세포에서 GLP-1 분비를 자극하고 갈색지방·근육에서 에너지 소비에 관여한다.

- **Obeticholic acid**는 FXR 작용제로 원발성 담즙성 담관염에서 사용되며, 소양증 악화와 진행된 간경변에서의 안전성 문제가 사용 범위를 제한한다.
- 회장 절제나 크론병으로 담즙산 재흡수가 줄면 FGF19 신호가 감소해 CYP7A1 억제가 풀린다. 합성이 늘어난 담즙산이 대장으로 넘어가 분비성 설사를 일으킨다. 이것이 **담즙산 설사**이며, 치료는 지사제가 아니라 담즙산 격리제다.

=> 같은 분자가 소화의 도구이자 신호다. 담즙산을 계면활성제로만 보면 담즙산 설사에서 격리제를 쓰는 이유도, FXR 작용제가 간질환 치료제가 되는 이유도 설명할 수 없다.

@sec Steroid 생성 조직은 왜 LDL에 의존하는가
?: 부신과 생식샘도 cholesterol을 합성할 수 있는데, 왜 이 조직들은 혈중 LDL 흡수에 크게 의존하는가.
!: Steroid 호르몬 생성에 필요한 cholesterol의 양이 자체 합성 능력을 넘기 때문이며, 그래서 율속 단계는 합성이 아니라 미토콘드리아 내막으로의 cholesterol 전달이다.

ACTH나 LH 자극을 받으면 steroid 생성 세포는 짧은 시간에 많은 cholesterol을 써야 한다. 공급원은 LDLR을 통한 LDL 흡수와 SR-B1을 통한 HDL 유래 cholesteryl ester 선택적 섭취이고, 저장형은 세포질 지질방울의 cholesteryl ester다.

율속 단계는 **StAR**(steroidogenic acute regulatory protein)가 cholesterol을 미토콘드리아 외막에서 내막으로 옮기는 과정이다. 내막에 도달한 cholesterol을 **CYP11A1**(P450scc)이 pregnenolone으로 바꾸고, 여기서 모든 steroid 계열이 갈라진다.

| 결손 | 차단 지점 | 표현형 |
|---|---|---|
| *STAR* | 미토콘드리아 내막으로의 전달 | 선천성 지질성 부신과형성. 모든 steroid 결핍, 부신에 지질 축적, 46,XY에서 여성형 외성기 |
| *CYP11A1* | Pregnenolone 생성 | 유사하나 지질 축적은 덜하다 |
| *CYP21A2* | 21-hydroxylation | 선천성 부신과형성의 90~95%. Cortisol·aldosterone 부족, 17-hydroxyprogesterone 축적이 androgen으로 흘러 여아 외성기 남성화 |
| *CYP17A1* | 17α-hydroxylation·17,20-lyase | Cortisol·성호르몬 부족, mineralocorticoid 전구체 축적으로 고혈압·저칼륨 |

=> 21-hydroxylase 결손에서 나타나는 남성화는 androgen 합성 효소의 이상이 아니라, 막힌 경로 위쪽에 쌓인 전구체가 열려 있는 androgen 경로로 흘러간 결과다. 대사 경로의 차단은 결핍만이 아니라 축적과 우회라는 두 번째 결과를 함께 만든다. 신생아 선별에서 17-hydroxyprogesterone을 측정하는 근거도 이 축적에 있다.

@sec HDL은 cholesterol을 간으로 되돌리는데, 왜 HDL-C를 올리는 약은 사건을 줄이지 못했는가
?: 역학에서 HDL-C는 심혈관 위험과 일관되게 역상관한다. 그런데 왜 HDL-C를 올린 약물들은 임상 사건을 줄이지 못했는가.
!: HDL-C 농도는 역수송 경로의 기능을 대신하는 표지일 뿐이며, 농도를 올린다고 cholesterol efflux 기능이 함께 좋아지지는 않기 때문이다.

역수송은 농도가 아니라 흐름이다. 말초 대식세포에서 **ABCA1**이 지질이 거의 없는 apoA-I에, **ABCG1**이 성숙한 HDL 입자에 cholesterol을 넘긴다. **LCAT**이 이를 에스터화해 입자 중심에 가두면 농도 기울기가 유지되어 유출이 계속된다. 이후 **SR-B1**이 간에서 cholesteryl ester를 선택적으로 흡수하거나, **CETP**가 cholesteryl ester를 apoB 함유 입자로 옮겨 LDLR 경로로 간에 도달한다. *ABCA1* 양쪽 대립유전자 결손인 **Tangier disease**에서 HDL이 거의 소실되는 것이 이 경로의 사람 증거다.

| 약물·근거 | HDL-C | 임상 결과 |
|---|---|---|
| Torcetrapib (ILLUMINATE) | 크게 상승 | 사망·사건 증가. 혈압 상승과 aldosterone 증가라는 표적 외 작용 |
| Dalcetrapib (dal-OUTCOMES) | 상승 | 무익성으로 조기 종료 |
| Evacetrapib (ACCELERATE) | 크게 상승 | 사건 감소 없음 |
| Anacetrapib (REVEAL) | 상승 | 주요 관동맥 사건 9% 감소(RR 0.91). 다만 apoB·non-HDL-C 감소로 설명 가능 |
| 멘델 무작위화 (Voight 2012) | *LIPG* Asn396Ser 보유자에서 HDL-C 상승 | 심근경색 위험은 낮아지지 않음(OR 1.0 부근) |

> 멘델 무작위화의 해석에도 한계가 있다. 단일 변이의 효과는 평생 노출이라는 점에서 약물과 다르고, 다면발현을 완전히 배제하기 어렵다. 그럼에도 약물 시험과 유전 역학이 같은 방향을 가리킨다는 점이 결론을 강화한다.

=> HDL-C는 위험 표지이지 인과적 치료 표적이 아니다. 같은 자료로 LDL-C는 정반대의 결론을 얻는다. 멘델 무작위화와 약물 시험이 모두 LDL 저하의 이득을 지지하고, 저하 수단이 무엇이든(statin, ezetimibe, PCSK9 억제) 효과가 유지된다. 연관이 강하다는 사실만으로 표적을 정할 수 없고, 개입으로 결과가 바뀌는지를 물어야 한다. 현재 연구는 농도 대신 **cholesterol efflux capacity**를 측정하려 한다.

@quiz
Q: Statin으로 LDL-C가 충분히 떨어지지 않는 환자에게 statin 용량을 두 배로 올리는 것과 ezetimibe를 추가하는 것 중 어느 쪽이 더 큰 추가 감소를 기대할 수 있는가. 기전으로 설명하라.
A: 일반적으로 ezetimibe 추가가 더 크다. Statin 용량을 두 배로 올려도 추가 감소는 약 6%에 그치는데, 이는 HMGCR 억제가 깊어질수록 SREBP-2가 PCSK9도 함께 올려 LDLR 증가를 상쇄하기 때문이다. Ezetimibe는 NPC1L1을 통한 장 흡수라는 다른 경로를 차단해 간으로 들어오는 cholesterol을 줄이므로, 같은 statin 용량에서 추가로 15~20% 감소를 얻는다. 서로 다른 지점에서 간 cholesterol을 낮춘다는 점이 병용의 근거다.

Q: 회장을 절제한 환자가 수술 후 수양성 설사를 호소한다. 담즙산 설사라면 어떤 기전이며 왜 담즙산 격리제가 치료가 되는가.
A: 회장 말단의 ASBT가 소실되어 담즙산이 재흡수되지 않고 대장으로 넘어간다. 대장에서 담즙산은 전해질과 수분 분비를 자극해 분비성 설사를 일으킨다. 동시에 회장 FXR 활성이 줄어 FGF19 분비가 감소하므로 간의 CYP7A1 억제가 풀려 담즙산 합성이 오히려 늘고 대장으로 넘어가는 양이 더 많아진다. 담즙산 격리제는 대장에 도달한 담즙산을 결합해 분비 자극을 없애므로 원인 치료가 된다. 다만 절제 범위가 넓어 담즙산 풀 자체가 고갈된 경우에는 지방변이 주된 문제가 되며 격리제가 이를 악화시킬 수 있다.

Q: 신생아 선별에서 17-hydroxyprogesterone이 상승했다. 어느 효소 결손을 시사하며 왜 그 대사물이 쌓이는가. 그리고 왜 여아에서 외성기 남성화가 나타나는가.
A: 21-hydroxylase(CYP21A2) 결손을 시사한다. 이 효소는 17-hydroxyprogesterone을 11-deoxycortisol로, progesterone을 deoxycorticosterone으로 바꾸므로, 결손 시 기질인 17-hydroxyprogesterone이 축적된다. Cortisol이 부족해 ACTH 음성 되먹임이 풀리면 부신이 자극을 계속 받아 전구체가 더 쌓인다. 축적된 17-hydroxyprogesterone은 막히지 않은 androgen 합성 경로로 흘러 androstenedione과 testosterone을 만들고, 태아기 노출로 46,XX 여아에서 외성기 남성화가 생긴다. 즉 증상은 결핍과 축적·우회가 함께 만든 결과다.

Q: 어떤 신약이 HDL-C를 40% 올린다는 2상 결과를 보였다. 이 결과만으로 심혈관 사건 감소를 기대해도 되는가. 판단의 근거를 들어 답하라.
A: 기대할 수 없다. CETP 억제제들의 경험이 직접적인 반례다. Torcetrapib은 HDL-C를 크게 올렸으나 사망과 사건이 증가했고, dalcetrapib은 무익성으로 중단되었으며, evacetrapib은 HDL-C를 크게 올리고도 사건을 줄이지 못했다. Anacetrapib만 소폭 이득을 보였는데 그마저 apoB와 non-HDL-C 감소로 설명된다. 멘델 무작위화에서도 HDL-C를 올리는 유전 변이가 심근경색 위험을 낮추지 않았다. HDL-C 농도는 역수송 기능의 표지일 뿐이므로, 농도 변화가 아니라 임상 사건을 평가변수로 한 시험 결과가 필요하다.

Q: 혈중 sitosterol이 현저히 높고 어린 나이에 황색종과 관동맥질환이 있는 환자에서 어떤 진단을 의심하며, 이 환자에게 statin 단독 치료가 왜 충분하지 않은가.
A: Sitosterolemia(*ABCG5* 또는 *ABCG8* 결손)를 의심한다. 이 환자는 식물 sterol을 포함한 sterol의 장 흡수가 과도하고 담즙 배출이 되지 않는 것이 1차 문제이므로, 내인성 합성을 억제하는 statin은 핵심 기전을 교정하지 못한다. 치료는 식물 sterol 섭취 제한과 NPC1L1을 억제해 흡수 자체를 줄이는 ezetimibe가 중심이며, 담즙산 격리제를 병용한다. 가족성 고콜레스테롤혈증과 임상상이 비슷할 수 있어 sterol 분획 측정으로 감별해야 한다.

Q: 간경변 환자에서 혈중 총 cholesterol이 낮게 측정되었다. 이것을 심혈관 위험이 낮다는 뜻으로 읽어도 되는가.
A: 읽을 수 없다. 간은 cholesterol 합성, lipoprotein 조립, LCAT과 apoA-I 생산의 중심이므로 간기능이 떨어지면 생산 자체가 줄어 총 cholesterol과 HDL-C가 함께 낮아진다. 이때 낮은 수치는 위험이 낮다는 신호가 아니라 간 합성능 저하의 지표이며, 실제로 중증 간질환에서 낮은 cholesterol은 예후 불량과 연관된다. 검사값의 의미는 생산과 제거 중 어느 쪽이 변했는지를 따져야 결정된다.

@ref
- Brown MS, Goldstein JL. The SREBP pathway: regulation of cholesterol metabolism by proteolysis of a membrane-bound transcription factor. *Cell* 1997;89:331–340.
- Horton JD, Cohen JC, Hobbs HH. PCSK9: a convertase that coordinates LDL catabolism. *J Lipid Res* 2009;50:S172–S177.
- Cannon CP et al. Ezetimibe added to statin therapy after acute coronary syndromes (IMPROVE-IT). *N Engl J Med* 2015;372:2387–2397.
- Chiang JYL. Bile acid metabolism and signaling. *Compr Physiol* 2013;3:1191–1212.
- Miller WL, Auchus RJ. The molecular biology, biochemistry, and physiology of human steroidogenesis and its disorders. *Endocr Rev* 2011;32:81–151.
- Voight BF et al. Plasma HDL cholesterol and risk of myocardial infarction: a mendelian randomisation study. *Lancet* 2012;380:572–580.
