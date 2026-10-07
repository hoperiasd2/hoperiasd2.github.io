---
lesson_id: M02-W09-L02
title: Cholesterol, 담즙산과 steroid 대사
en: Cholesterol, Bile Acid and Steroid Metabolism
status: 초안
version: v0.2
---

@obj
- Cholesterol의 화학 구조와 세포막·전구체로서의 역할을 설명한다.
- Acetyl-CoA에서 cholesterol에 이르는 생합성 경로를 네 단계로 나누어 설명한다.
- HMG-CoA reductase가 율속 효소인 이유와 전사·분해·인산화에 의한 조절을 설명한다.
- LDL receptor를 통한 cholesterol 수송과 세포 내 되먹임 반응을 설명한다.
- 담즙산의 합성·접합·장간 순환과 steroid 호르몬 및 vitamin D 생성 과정을 설명한다.
- 고콜레스테롤혈증의 원인과 주요 약물의 작용 지점을 연결한다.

@prereq
- M02-W07-L01 식이지질의 소화·흡수·운반 — micelle, chylomicron, lipoprotein의 기본 구성
- M02-W08-L03 케톤체 생성·이용과 ketoacidosis — HMG-CoA가 갈라지는 두 경로의 구분
- M02-W06-L03 Pentose phosphate pathway — 환원적 생합성에 쓰이는 NADPH의 공급원

@sec 1. Cholesterol의 구조와 생물학적 역할
Cholesterol은 탄소 27개로 이루어진 **sterol**이다. 기본 골격은 고리 네 개가 붙어 있는 **steroid 핵**(cyclopentanoperhydrophenanthrene)으로, 여섯 탄소 고리 셋(A·B·C)과 다섯 탄소 고리 하나(D)로 구성된다. 여기에 세 가지가 더 붙는다. C3에 **hydroxyl기(-OH)**, C5와 C6 사이에 **이중결합**, C17에 탄소 여덟 개짜리 **곁사슬**이다.

이 구조가 성질을 결정한다. 분자의 대부분은 탄화수소여서 소수성이지만 C3의 -OH 하나가 친수성이므로, cholesterol은 **양친매성(amphipathic)** 분자다. 그래서 인지질 이중층에 끼어들 때 -OH가 막 표면의 인지질 머리 쪽을 향하고 고리와 곁사슬이 지방산 꼬리 사이에 자리 잡는다.

세포에서 cholesterol이 하는 일은 세 가지로 묶인다.

- **막 구성 성분**: 동물 세포막에서 인지질 사이에 끼어 막의 유동성을 조절한다. 상전이 온도보다 높은 온도에서는 지방산 사슬의 운동을 제한해 유동성을 낮추고, 낮은 온도에서는 사슬이 촘촘히 정렬되는 것을 방해해 유동성을 높인다. 즉 온도 변화에 대한 **완충자** 역할을 한다.
- **전구체**: 담즙산, 다섯 계열의 steroid 호르몬, vitamin D가 모두 cholesterol에서 만들어진다. 이 수업의 뒷부분이 그 각각이다.
- **지질 뗏목(lipid raft)의 구성**: sphingolipid와 함께 막의 특정 영역에 모여 신호 단백질이 자리 잡는 발판을 만든다.

저장과 운반에는 **cholesteryl ester** 형태를 쓴다. C3의 -OH에 지방산이 에스터 결합으로 붙은 형태로, -OH가 가려지므로 더 소수성이 되어 지질방울 안쪽이나 lipoprotein 중심부에 빽빽하게 담긴다. 에스터화를 담당하는 효소는 두 곳에서 다르다. 세포 안에서는 **ACAT**(acyl-CoA:cholesterol acyltransferase)이 acyl-CoA의 지방산을 옮기고, 혈장에서는 **LCAT**(lecithin:cholesterol acyltransferase)이 phosphatidylcholine의 지방산을 옮긴다.

| 구분 | 유리 cholesterol | Cholesteryl ester |
|---|---|---|
| C3 위치 | -OH 노출 | 지방산이 에스터 결합 |
| 성질 | 양친매성 | 거의 완전한 소수성 |
| 존재 위치 | 세포막, lipoprotein 표면 | 세포질 지질방울, lipoprotein 중심 |
| 생성 효소 | — | 세포 내 ACAT, 혈장 LCAT |

성인 체내 cholesterol 총량은 약 140 g이며, 공급은 두 경로에서 온다. 식사로 하루 약 300~500 mg을 섭취하고, 체내에서 하루 약 700~900 mg을 새로 만든다. 즉 **대부분은 내인성 합성에서 온다.** 식물에는 cholesterol이 없고 대신 sitosterol 같은 식물 sterol이 있는데, 사람은 이를 거의 흡수하지 못한다.

@sec 2. Cholesterol의 생합성: 경로 개요
Cholesterol의 탄소 27개는 **모두 acetyl-CoA에서 온다.** 합성은 간에서 가장 활발하지만 거의 모든 조직에서 일어나며, 효소들은 세포질과 **활면소포체(smooth ER)** 막에 있다. 환원력으로는 NADPH가 대량으로 필요한데, 주로 pentose phosphate pathway에서 공급된다.

긴 경로이지만 네 단계로 묶으면 구조가 보인다.

| 단계 | 변화 | 주요 효소 | 비고 |
|---|---|---|---|
| 1 | Acetyl-CoA(C2) ×3 → **HMG-CoA**(C6) | Thiolase, HMG-CoA synthase | **세포질**에서 일어난다 |
| 2 | HMG-CoA → **Mevalonate**(C6) | **HMG-CoA reductase** | NADPH 2분자 소비, **율속·비가역** |
| 3 | Mevalonate → **Isoprene 단위**(C5) → farnesyl pyrophosphate(C15) | Kinase 3종, isomerase, prenyltransferase | ATP 3분자 소비, 탈탄산 |
| 4 | Farnesyl-PP ×2 → **Squalene**(C30) → lanosterol(C30) → **Cholesterol**(C27) | Squalene synthase, squalene monooxygenase, cyclase 외 약 19단계 | 탄소 3개가 떨어져 나간다 |

**1단계**에서 주의할 점이 있다. HMG-CoA는 케톤체 합성에도 쓰이는 중간체인데, 두 경로는 **세포 내 위치로 구분된다.** Cholesterol 합성용 HMG-CoA는 세포질의 HMG-CoA synthase가 만들고, 케톤체 합성용은 간 미토콘드리아 기질의 동위효소가 만든다. 같은 분자이지만 서로 다른 구획에 있어 섞이지 않는다.

**2단계**가 경로 전체의 중심이다. HMG-CoA reductase는 소포체 막을 여러 번 관통하는 막단백이며, 활성 부위는 세포질 쪽을 향한다. HMG-CoA의 thioester를 환원해 1차 alcohol인 mevalonate를 만들고 이 과정에서 NADPH 2분자를 쓴다. **생리적 조건에서 비가역이고, 이 지점을 지나면 경로를 되돌릴 수 없다.** 그래서 조절이 여기에 집중된다.

**3단계**에서 C6의 mevalonate가 ATP 세 분자를 써서 인산화된 뒤 탈탄산되어 **C5의 isoprene 단위**가 된다. 이것들이 머리-꼬리로 이어 붙어 C10(geranyl-PP), C15(farnesyl-PP)로 자란다.

**4단계**에서 farnesyl-PP 두 분자가 꼬리-꼬리로 결합해 C30의 squalene이 되고, 산소와 NADPH를 써서 epoxide가 된 뒤 고리화되어 lanosterol이 된다. 여기서 약 19단계를 더 거치며 탄소 세 개가 떨어져 나가 C27의 cholesterol이 완성된다.

핵심은 **3단계에서 갈라지는 가지**다. Farnesyl-PP는 cholesterol로만 가지 않는다. 여기서 **ubiquinone(CoQ10)**, **dolichol**(당단백질 합성에 필요), 그리고 Ras·Rho 같은 단백질을 막에 고정하는 **prenyl기**가 만들어진다. 이 사실은 뒤에 statin의 작용을 이해할 때 다시 쓰인다.

> **임상 연계** Mevalonate 경로의 효소 결손인 **mevalonate kinase deficiency**에서는 mevalonate가 축적되고 하류 isoprenoid 산물이 부족해진다. 환자는 주기적 발열과 염증 발작(hyper-IgD 증후군)을 보이는데, cholesterol 부족이 아니라 **isoprenoid 부족**이 염증 경로를 활성화하기 때문이다. 경로의 가지를 알아야 설명되는 질환이다.

@sec 3. HMG-CoA reductase의 조절
세포가 cholesterol을 얼마나 만들지는 거의 전적으로 HMG-CoA reductase의 양과 활성으로 정해진다. 조절은 세 층위에서 겹쳐 일어나며, 작동 속도가 서로 다르다.

**(1) 전사 조절 — SREBP-2를 통한 되먹임**

소포체 막에는 전사인자 전구체인 **SREBP-2**(sterol regulatory element-binding protein 2)가 끼어 있고, 여기에 sterol 감지 단백 **SCAP**이 붙어 있다.

- 소포체 막의 cholesterol이 **충분하면** SCAP의 구조가 바뀌어 막단백 **Insig**에 결합한다. 복합체가 소포체에 붙잡혀 있으므로 SREBP-2는 전구체 상태로 남는다.
- cholesterol이 **부족하면** SCAP이 Insig에서 떨어진다. 복합체가 소포체를 떠나 Golgi로 이동하고, 거기서 두 단백분해효소(S1P, S2P)가 차례로 자른다. 잘려 나온 조각이 핵으로 들어가 표적 유전자의 **sterol regulatory element(SRE)**에 결합한다.

표적 유전자의 구성이 중요하다. SREBP-2는 합성 효소인 **HMG-CoA reductase**와 흡수 수용체인 **LDL receptor**를 **함께** 유도한다. 세포가 cholesterol이 모자란다고 판단하면 만들기와 가져오기를 동시에 늘리는 것이다.

**(2) 효소 분해 조절**

소포체 막에 sterol이 쌓이면 HMG-CoA reductase 자신의 막 도메인도 Insig에 결합한다. 그러면 ubiquitin이 붙어 분해로 보내진다. 전사를 줄이는 것보다 **빠르게** 효소량을 떨어뜨리는 장치다.

**(3) 공유결합 변형 — 인산화**

세포의 에너지가 부족해 AMP가 늘면 **AMPK**가 활성화되어 HMG-CoA reductase를 인산화하고, 인산화된 효소는 활성이 낮아진다. ATP를 많이 쓰는 합성 경로를 에너지 상태에 맞춰 끄는 조절이다. 반대로 insulin은 탈인산화를 촉진해 활성을 높인다.

| 조절 방식 | 신호 | 방향 | 작동 속도 |
|---|---|---|---|
| 전사(SREBP-2) | 세포 내 sterol 감소 | 효소 합성 ↑ | 수 시간 |
| 분해(Insig-ubiquitin) | 세포 내 sterol 증가 | 효소량 ↓ | 수십 분~시간 |
| 인산화(AMPK) | ATP 부족 | 활성 ↓ | 분 |
| 탈인산화(insulin) | 섭식 상태 | 활성 ↑ | 분 |

Cholesterol 합성에는 **하루 주기 변동**도 있다. 합성은 자정 무렵에 가장 활발하므로, 반감기가 짧은 statin은 저녁에 복용하도록 권한다.

**Statin**은 이 효소를 겨냥한 약물이다. HMG-CoA와 구조가 비슷해 활성 부위에 경쟁적으로 결합하며, 친화도는 본래 기질보다 1,000배 이상 높다. 다만 statin이 혈중 LDL을 낮추는 실제 경로는 합성을 막는 것 자체가 아니다. 간세포의 cholesterol이 줄면 SREBP-2가 켜지고 **LDL receptor가 늘어 혈중 LDL이 더 빨리 제거되는 것**이 본체다. 다음 절에서 그 수용체를 다룬다.

@sec 4. Cholesterol의 수송과 LDL receptor 경로
Cholesterol은 물에 녹지 않으므로 혈액에서는 반드시 **lipoprotein** 입자에 실려 이동한다. 입자는 표면에 인지질·유리 cholesterol·apolipoprotein이 있고 중심에 triacylglycerol과 cholesteryl ester가 들어 있는 구조다.

| 입자 | 주 운반물 | 출발지 | 주요 apolipoprotein |
|---|---|---|---|
| Chylomicron | 식이 triacylglycerol | 장 | apoB-48 |
| VLDL | 내인성 triacylglycerol | 간 | apoB-100 |
| IDL | 중간 단계 | VLDL 분해 산물 | apoB-100, apoE |
| **LDL** | **cholesteryl ester** | IDL에서 생성 | **apoB-100** |
| HDL | 말초에서 회수한 cholesterol | 간·장 | apoA-I |

LDL은 **간에서 말초로** cholesterol을 보내는 입자이고, HDL은 **말초에서 간으로** 되돌리는 입자다.

**LDL receptor를 통한 흡수는 수용체 매개 세포내섭취(receptor-mediated endocytosis)의 교과서적 사례다.** 순서는 다음과 같다.

1. 세포막의 **clathrin coated pit**에 LDL receptor가 모여 있다.
2. 수용체가 LDL 입자의 **apoB-100**을 인식해 결합한다(IDL의 apoE도 인식한다).
3. 피막소포가 떨어져 나와 세포 안으로 들어가고 clathrin이 벗겨진다.
4. **endosome**에서 pH가 낮아지면 수용체와 LDL이 분리된다. 수용체는 세포막으로 **재순환**하고(한 수용체가 수백 회 재사용된다), LDL은 **lysosome**으로 간다.
5. Lysosome에서 apoB-100은 아미노산으로 분해되고, cholesteryl ester는 **lysosomal acid lipase**에 의해 유리 cholesterol과 지방산으로 가수분해된다.

이렇게 세포질로 들어온 유리 cholesterol은 **세 가지 되먹임**을 일으킨다. 이것이 세포 수준의 cholesterol 항상성이다.

- HMG-CoA reductase의 발현과 안정성을 낮춘다 → **합성을 줄인다**
- LDL receptor의 전사를 낮춘다 → **더 들이지 않는다**
- **ACAT**을 활성화한다 → 남는 것을 cholesteryl ester로 바꿔 **저장한다**

여기에 한 가지 조절자가 더 있다. **PCSK9**는 간에서 분비되는 단백분해효소로, 세포 표면에서 LDL receptor에 결합한 뒤 함께 세포 안으로 들어가 수용체가 재순환하지 못하고 lysosome에서 분해되게 만든다. PCSK9가 많으면 수용체 수가 줄어 혈중 LDL이 올라간다.

> **임상 연계** **가족성 고콜레스테롤혈증(familial hypercholesterolemia, FH)**은 LDL receptor 경로의 결함으로 생긴다. 원인 유전자는 *LDLR*(수용체 자체), *APOB*(수용체가 인식하는 리간드), *PCSK9*(기능 획득 변이로 수용체를 과도하게 분해)다. 이형접합은 약 250명 중 1명으로 드물지 않으며, 치료하지 않으면 LDL-C가 190~400 mg/dL에 이르고 30~50대에 관동맥질환이 나타난다. 동형접합은 약 30만 명 중 1명으로 소아기에 황색종과 관동맥질환이 생긴다. 세 유전자가 모두 **같은 경로의 서로 다른 지점**이라는 점이 이 질환이 LDL receptor 경로를 증명한 이유다.

@sec 5. 담즙산의 합성, 접합과 장간 순환
사람은 cholesterol의 고리 구조를 열어 CO₂와 물로 분해하는 효소를 가지고 있지 않다. 따라서 과잉 cholesterol은 **분해되는 것이 아니라 배출된다.** 정량적으로 가장 중요한 배출 경로가 담즙산으로의 전환이다.

**합성** 담즙산은 간에서만 만들어진다. 첫 반응이자 율속 단계는 **CYP7A1**(cholesterol 7α-hydroxylase)이 cholesterol의 C7에 수산기를 붙이는 것이다. 이후 고리의 추가 수산화, 이중결합 환원, 곁사슬 단축을 거쳐 탄소 24개의 **1차 담즙산** 두 가지가 만들어진다.

- **Cholic acid** — 수산기 3개(C3, C7, C12)
- **Chenodeoxycholic acid** — 수산기 2개(C3, C7)

**접합** 만들어진 담즙산은 그대로 쓰이지 않는다. 곁사슬의 carboxyl기에 **glycine** 또는 **taurine**이 아미드 결합으로 붙는다. 접합의 의미는 pKa를 낮추는 데 있다. 접합되지 않은 담즙산의 pKa는 약 6이어서 소장의 pH에서 상당 부분이 비이온형으로 존재하지만, 접합하면 pKa가 1~4로 떨어져 **거의 완전히 이온화된 염(bile salt)** 형태가 된다. 이온화된 분자는 계면활성 능력이 크고 막을 그냥 통과하지 못하므로 장 내강에 머물며 지방을 유화할 수 있다.

**2차 담즙산** 회장과 대장의 세균이 접합을 떼어내고(deconjugation) C7의 수산기를 제거하면(7α-dehydroxylation) **2차 담즙산**이 된다. Cholic acid에서 **deoxycholic acid**가, chenodeoxycholic acid에서 **lithocholic acid**가 생긴다.

**장간 순환(enterohepatic circulation)** 담즙산은 담낭에서 십이지장으로 분비되어 지방 소화를 돕고, 회장 말단에서 수송체 **ASBT**를 통해 능동적으로 재흡수되어 문맥을 거쳐 간으로 돌아온다. 전체 담즙산 풀은 약 3 g이고 하루 6~10회 순환하므로 하루에 장으로 분비되는 총량은 20~30 g에 이르지만, **대변으로 빠져나가는 양은 하루 0.2~0.6 g에 그친다.** 간은 잃은 만큼만 새로 합성해 풀을 유지한다.

합성량 자체도 되먹임으로 조절된다. 담즙산이 간세포로 돌아오면 핵수용체 **FXR**을 활성화하고, FXR은 CYP7A1의 전사를 억제한다. 장에서는 FXR이 **FGF19**를 분비시켜 문맥을 통해 간에 도달한 뒤 역시 CYP7A1을 억제한다.

> **임상 연계** **담즙산 격리제**(cholestyramine 등)는 장에서 담즙산과 결합해 대변으로 내보낸다. 장간 순환이 끊기면 FXR 신호가 줄어 CYP7A1 억제가 풀리고, 간은 담즙산을 새로 만들기 위해 자신의 cholesterol을 소모한다. 간세포 cholesterol이 줄면 SREBP-2가 켜지고 LDL receptor가 늘어 혈중 LDL이 감소한다. **약은 흡수되지 않고 장에만 머무는데 효과는 간에서 나타난다.** 한편 회장을 절제하면 담즙산이 재흡수되지 않아 대장으로 넘어가 수분 분비를 자극하는 **담즙산 설사**가 생기며, 이때의 치료도 담즙산 격리제다.

=> **핵심 정리** Cholesterol은 분해되지 않으므로 담즙산 전환과 담즙 배출이 유일한 제거 경로다. 장간 순환이 이 배출을 최소화하도록 설계되어 있고, 그 순환을 끊는 것이 곧 혈중 LDL을 낮추는 수단이 된다.

@sec 6. Steroid 호르몬의 합성
Cholesterol은 다섯 계열의 steroid 호르몬의 공통 전구체다. 합성은 부신피질, 난소, 정소, 태반에서 일어나며, 이들 조직은 필요한 양이 자체 합성 능력을 넘기 때문에 혈중 **LDL 흡수에 크게 의존한다.**

**율속 단계는 효소 반응이 아니라 운반이다.** Cholesterol을 미토콘드리아 외막에서 내막으로 옮기는 **StAR**(steroidogenic acute regulatory protein)가 그 역할을 한다. ACTH나 LH 자극은 StAR 발현을 빠르게 올려 합성을 개시한다.

내막에 도달한 cholesterol은 **CYP11A1**(측쇄 절단 효소)에 의해 곁사슬이 잘려 탄소 21개의 **pregnenolone**이 된다. **모든 steroid 호르몬은 여기서 갈라진다.**

| 계열 | 탄소 수 | 대표 호르몬 | 생성 조직 |
|---|---|---|---|
| Progestagen | C21 | Progesterone | 난소, 태반 |
| Mineralocorticoid | C21 | Aldosterone | 부신피질 사구대 |
| Glucocorticoid | C21 | Cortisol | 부신피질 속상대 |
| Androgen | C19 | Testosterone | 정소, 부신피질 망상대 |
| Estrogen | C18 | Estradiol | 난소 |

부신피질은 세 층으로 나뉘고 각 층이 서로 다른 효소를 발현해 다른 산물을 만든다. 바깥에서부터 **사구대**(aldosterone), **속상대**(cortisol), **망상대**(androgen 전구체) 순이다.

> **임상 연계** **선천성 부신과형성(congenital adrenal hyperplasia)**의 90~95%는 **21-hydroxylase(CYP21A2)** 결손이다. 이 효소는 cortisol과 aldosterone 합성 경로에 모두 필요하므로 두 호르몬이 부족해진다. Cortisol이 부족하면 ACTH 억제가 풀려 부신이 계속 자극받고, 막힌 지점 위쪽의 전구체인 **17-hydroxyprogesterone**이 크게 축적된다. 축적된 전구체는 막히지 않은 androgen 경로로 흘러 androgen이 과다 생성되고, 그 결과 46,XX 여아에서 외성기 남성화가 나타난다. **즉 증상은 결핍(cortisol·aldosterone)과 축적·우회(androgen)가 함께 만든 결과다.** 신생아 선별검사에서 17-hydroxyprogesterone을 측정하는 근거가 여기에 있다.

@sec 7. Vitamin D의 생성과 활성화
Vitamin D도 cholesterol 대사의 산물이다. 엄밀히 말하면 비타민이라기보다 체내에서 만들어지는 **호르몬**에 가깝다.

출발 물질은 cholesterol 합성 경로의 마지막 직전 중간체인 **7-dehydrocholesterol**이다. 피부에서 이 분자가 **자외선(UVB)**을 받으면 B 고리가 열려 **cholecalciferol(vitamin D₃)**이 된다. 식사로 섭취하는 vitamin D₂(ergocalciferol, 식물·효모 유래)와 D₃도 같은 경로로 합류한다.

활성화는 두 번의 수산화로 완성되며, 두 기관이 나누어 맡는다.

1. **간**에서 C25가 수산화되어 **25-hydroxycholecalciferol(25-OH-D)**이 된다. 혈중 농도가 가장 높고 반감기가 길어 **vitamin D 영양 상태를 평가하는 검사 지표**로 쓰인다.
2. **신장**에서 **1α-hydroxylase(CYP27B1)**가 C1을 수산화해 **1,25-dihydroxycholecalciferol(calcitriol)**을 만든다. 이것이 활성형이다. 이 효소는 **PTH와 저인산혈증에 의해 활성화**되고 FGF23에 의해 억제되므로, 활성형 생성량은 칼슘·인 요구에 따라 조절된다.

Calcitriol은 핵수용체에 결합해 작용한다. 소장에서 칼슘과 인의 흡수를 늘리고, 뼈에서 재형성을 조절하며, 신장에서 칼슘 재흡수를 늘린다.

> **임상 연계** 활성화가 두 기관에서 일어나므로 결핍의 원인도 나뉜다. 햇빛 노출 부족이나 섭취 부족은 25-OH-D를 낮춘다. **만성 신질환**에서는 1α-hydroxylase 활성이 떨어져 25-OH-D가 정상이어도 calcitriol이 부족해지고, 그 결과 저칼슘혈증과 이차성 부갑상선기능항진증이 생긴다. 이때는 일반 vitamin D가 아니라 **활성형 유사체**를 투여해야 한다. 소아에서 결핍은 성장판의 무기질화 장애인 **구루병**으로, 성인에서는 **골연화증**으로 나타난다.

@sec 8. 고콜레스테롤혈증과 약물 치료
혈중 LDL-C가 높을수록 죽상경화와 관동맥질환의 위험이 올라간다. 원인은 일차성과 이차성으로 나뉜다.

- **일차성**: 가족성 고콜레스테롤혈증(앞 절), 다유전자성 고콜레스테롤혈증, 가족성 복합 고지혈증
- **이차성**: 갑상선기능저하증, 신증후군, 폐색성 간담도질환, 당뇨병, 일부 약물(thiazide, 일부 corticosteroid)

이차성 원인은 교정하면 지질이 돌아오므로, **약을 늘리기 전에 먼저 배제**한다.

주요 약물은 앞서 배운 경로의 서로 다른 지점에 작용하며, 결국 **간세포의 cholesterol을 줄여 LDL receptor를 늘린다**는 공통 결과로 수렴한다.

| 약물 | 작용 지점 | 기전 | LDL-C 감소 |
|---|---|---|---|
| **Statin** | HMG-CoA reductase | 경쟁적 억제 → 간 cholesterol ↓ → LDL receptor ↑ | 25~55% |
| **Ezetimibe** | 장 상피의 NPC1L1 | 식이·담즙 cholesterol 흡수 억제 | 15~20% |
| **담즙산 격리제** | 장 내강의 담즙산 | 장간 순환 차단 → 간 cholesterol 소모 | 15~25% |
| **PCSK9 억제제** | 분비된 PCSK9 | LDL receptor 분해 차단 → 수용체 수 유지 | 50~60% |
| Fibrate | PPARα | 주로 triacylglycerol 감소 | 작음 |
| Niacin | 지방 분해 억제 | VLDL 생산 감소 | 중간 |

**병용의 근거**도 경로로 설명된다. Statin은 LDL receptor를 늘리지만 같은 SREBP-2 프로그램이 PCSK9도 함께 올려 수용체 증가를 일부 상쇄한다. 그래서 PCSK9 억제제를 더하면 단순한 덧셈 이상의 효과가 난다. Ezetimibe는 작용 지점이 장이지만 간의 cholesterol을 줄이므로 statin과 다른 경로로 같은 결과를 만든다.

주요 부작용도 기전에서 나온다. Statin의 근육 증상과 간효소 상승은 mevalonate 경로 하류의 isoprenoid(CoQ10 등) 감소와 관련이 있다고 설명되며, 담즙산 격리제는 장에만 머물러 전신 부작용은 적은 대신 지용성 비타민과 다른 약물의 흡수를 방해한다.

=> **핵심 정리** 이 장의 모든 내용은 하나의 축으로 이어진다. Cholesterol은 acetyl-CoA에서 만들어지고, HMG-CoA reductase가 그 속도를 정하며, 세포 내 cholesterol 농도가 SREBP-2를 통해 합성과 흡수를 함께 조절한다. 분해되지 않으므로 담즙산으로 바꾸어 내보내고, 남은 것은 담즙산·steroid 호르몬·vitamin D라는 필수 분자의 재료가 된다. 약물은 이 축의 어느 지점에 작용하든 결국 간의 LDL receptor를 늘리는 쪽으로 수렴한다.

@quiz
Q: Cholesterol 합성 경로에서 HMG-CoA reductase가 율속 효소로 작동하는 이유를 반응의 성질과 조절 방식 두 측면에서 설명하라.
A: 반응의 성질 측면에서, HMG-CoA를 mevalonate로 환원하는 반응은 NADPH 두 분자를 쓰며 생리적 조건에서 비가역적이다. 이 지점을 지나면 되돌아갈 수 없는 committed step이므로 경로 전체의 유입량을 결정한다. 조절 측면에서는 세 가지가 겹친다. 세포 내 sterol이 줄면 SREBP-2가 전사를 늘리고, sterol이 쌓이면 Insig이 효소에 결합해 ubiquitin 매개 분해를 유도하며, ATP가 부족하면 AMPK가 인산화해 활성을 낮춘다. 한 효소에 세 층위의 조절이 모이므로 여기가 경로의 제어점이 된다.

Q: 케톤체 합성과 cholesterol 합성은 둘 다 HMG-CoA를 중간체로 쓴다. 두 경로가 섞이지 않는 이유는 무엇인가.
A: 세포 내 위치가 다르기 때문이다. Cholesterol 합성용 HMG-CoA는 세포질의 HMG-CoA synthase가 만들고 세포질과 소포체에서 처리되며, 케톤체 합성용 HMG-CoA는 간 미토콘드리아 기질의 동위효소가 만들고 거기서 HMG-CoA lyase에 의해 acetoacetate로 분해된다. 같은 화합물이라도 서로 다른 구획에 존재하므로 각 경로의 효소만 접근할 수 있다. 구획화가 대사 경로를 분리하는 대표적인 예다.

Q: 담즙산이 glycine이나 taurine과 접합되는 과정의 생화학적 의미를 설명하라.
A: 접합은 담즙산의 pKa를 낮춘다. 접합되지 않은 담즙산의 pKa는 약 6이어서 소장의 pH에서 상당 부분이 비이온형으로 존재하지만, 접합하면 pKa가 1~4로 떨어져 장 내강에서 거의 완전히 이온화된 염 형태가 된다. 이온화된 분자는 계면활성 능력이 커서 지방을 효과적으로 유화하고, 동시에 막을 수동확산으로 통과하지 못해 장 내강에 머문다. 그 결과 소화 작용을 끝까지 수행한 뒤 회장 말단의 능동수송체를 통해서만 재흡수된다.

Q: 가족성 고콜레스테롤혈증의 원인 유전자가 *LDLR*, *APOB*, *PCSK9* 세 가지인 이유를 LDL receptor 경로로 설명하라.
A: 세 유전자가 모두 같은 경로의 서로 다른 지점에 해당하기 때문이다. *LDLR* 변이는 수용체 자체의 수나 기능을 떨어뜨린다. *APOB* 변이는 LDL 입자 표면에서 수용체가 인식하는 리간드인 apoB-100을 바꾸어 결합을 방해한다. *PCSK9*의 기능 획득 변이는 LDL receptor의 분해를 과도하게 촉진해 세포 표면의 수용체 수를 줄인다. 어느 지점이 망가지든 결과는 같다. 간의 LDL 제거가 느려져 혈중 LDL-C가 올라간다.

Q: 만성 신질환 환자에서 혈중 25-hydroxyvitamin D가 정상인데도 저칼슘혈증이 생길 수 있다. 그 기전과 적절한 치료를 설명하라.
A: Vitamin D의 활성화는 간의 25-수산화와 신장의 1α-수산화 두 단계로 이루어진다. 만성 신질환에서는 신장의 1α-hydroxylase(CYP27B1) 활성이 떨어져 25-OH-D가 정상이어도 활성형인 1,25-dihydroxyvitamin D가 부족해진다. 활성형이 부족하면 소장의 칼슘 흡수가 줄어 저칼슘혈증이 생기고, 이것이 PTH 분비를 자극해 이차성 부갑상선기능항진증으로 이어진다. 따라서 일반 vitamin D 보충으로는 교정되지 않으며 calcitriol 같은 활성형 유사체를 투여해야 한다.

Q: 21-hydroxylase 결손 환자에서 cortisol과 aldosterone이 부족한 것은 효소가 막혔기 때문이다. 그런데 왜 androgen은 오히려 과다해지는가.
A: 막힌 지점 위쪽의 전구체가 쌓이고, 그 전구체가 막히지 않은 다른 경로로 흘러가기 때문이다. 21-hydroxylase가 작동하지 않으면 기질인 17-hydroxyprogesterone이 축적된다. 동시에 cortisol이 부족해 ACTH에 대한 음성 되먹임이 풀리므로 부신이 계속 자극을 받아 전구체가 더 많이 만들어진다. 축적된 17-hydroxyprogesterone은 androgen 합성 경로로 전환되어 androstenedione과 testosterone을 과다 생성하고, 태아기 노출로 46,XX 여아에서 외성기 남성화가 나타난다.

@ref
- Ferrier DR (ed). *Lippincott Illustrated Reviews: Biochemistry*. Chapter 18, Cholesterol, Lipoprotein, and Steroid Metabolism.
- Brown MS, Goldstein JL. The SREBP pathway: regulation of cholesterol metabolism by proteolysis of a membrane-bound transcription factor. *Cell* 1997;89:331–340.
- Goldstein JL, Brown MS. The LDL receptor. *Arterioscler Thromb Vasc Biol* 2009;29:431–438.
- Chiang JYL. Bile acid metabolism and signaling. *Compr Physiol* 2013;3:1191–1212.
- Miller WL, Auchus RJ. The molecular biology, biochemistry, and physiology of human steroidogenesis and its disorders. *Endocr Rev* 2011;32:81–151.
- Nordestgaard BG et al. Familial hypercholesterolaemia is underdiagnosed and undertreated in the general population: EAS consensus statement. *Eur Heart J* 2013;34:3478–3490.
