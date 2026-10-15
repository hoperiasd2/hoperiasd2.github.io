---
title: Hemoglobin·myoglobin과 산소 운반
status: 초안
version: v0.1
slides: none
---

@obj
- Heme과 globin의 역할을 나누고 산소 결합과 iron oxidation을 구별한다.
- Myoglobin과 hemoglobin의 구조·기능 차이를 설명한다.
- Cooperativity와 P_{50}로 산소 결합 곡선을 해석한다.
- 조직의 CO_{2}·H^{+}와 2,3-BPG가 산소 방출을 돕는 이유를 설명한다.
- CO 중독·methemoglobinemia·빈혈에서 서로 다른 운반 장애를 구별한다.
- HbS와 thalassemia의 기전을 아미노산 변화와 사슬 생성량 변화로 나누어 설명한다.
- 산소 분압·포화도·산소 함량을 구별한다.

@prereq
- M02-W01-L01의 전하와 protonation, M02-W01-L02의 여러 사슬 사이 결합을 사용한다.
- Affinity는 주어진 조건에서 산소를 결합하는 성향이다.
- Capacity는 결합할 수 있는 자리의 총량이다.
- 산소 운반에는 폐에서 잘 결합하는 능력과 조직에서 필요한 만큼 방출하는 능력이 모두 필요하다.

@sec 1. 산소는 heme의 iron에 결합하고 globin은 그 환경을 만든다
Hemoglobin의 protein 부분을 globin이라고 하고, 산소가 직접 결합하는 부분은 heme이다. Heme에는 porphyrin ring과 그 중심의 iron이 있다. Globin은 heme을 일정한 위치에 놓고 주변의 화학적 환경을 만든다. 같은 heme을 가진 단백질이라도 주변 protein이 다르면 산소 운반, 전자 전달, peroxide 처리처럼 다른 일을 할 수 있다. [T3, PDF 66–69]

정상적으로 산소를 결합하는 hemoglobin의 heme iron은 Fe^{2+} 상태로 설명한다. 산소가 붙는 oxygenation과 iron이 Fe^{3+}가 되는 oxidation은 같은 사건이 아니다. Fe^{3+}인 methemoglobin의 해당 자리는 정상적으로 산소를 결합하지 못한다. “산소가 붙었다”와 “철이 산화되었다”를 혼동하면 뒤의 질환 설명이 잘못된다.

**결합과 산화 상태를 구별하기**

| 상태 | 분자에서 일어난 일 | 산소 운반 |
|---|---|---|
| Oxyhemoglobin | 정상 heme에 O_{2}가 결합 | 산소를 결합했다가 방출할 수 있다. |
| Methemoglobin | Iron이 Fe^{3+} 상태 | 해당 자리는 정상적으로 산소를 결합하지 못한다. |
| Carboxyhemoglobin | Heme에 CO가 결합 | 산소에 쓸 수 있는 자리가 줄고 방출도 어려워진다. |

Globin의 proximal histidine은 iron에 직접 결합한다. Iron의 위치가 바뀌면 이 연결을 통해 protein의 모양도 영향을 받는다. Distal histidine은 산소가 결합하는 주변 환경을 안정화한다. 두 histidine을 산소 결합 자리 두 개로 세지는 않는다. Heme 하나에는 산소 분자 하나가 결합한다.

@sec 2. Myoglobin은 근육 내부에서, hemoglobin은 혈액에서 일한다
Myoglobin(Mb)은 사슬 하나와 heme 하나를 가지며 근육세포 안에 있다. 낮은 산소 분압에서도 산소를 잘 결합하고, 세포 내부 산소 공급이 더 낮아지면 방출한다. Hemoglobin(Hb)은 red blood cell(RBC), 즉 적혈구 안에서 폐와 조직 사이의 산소 운반을 맡는다. 성인의 주요 HbA는 α-chain 두 개와 β-chain 두 개인 α_{2}β_{2}이고 heme도 네 개다. [T3, PDF 67–73]

**비슷한 globin 구조를 서로 다른 기능에 쓰는 방법**

| 비교 | Myoglobin | HbA |
|---|---|---|
| 사슬·heme 수 | 1·1 | 4·4 |
| 주요 위치 | 근육세포 내부 | 적혈구 내부 |
| 결합 곡선 | Hyperbolic | Sigmoidal |
| 기능에서 필요한 점 | 낮은 세포 내부 산소에서 확보·방출 | 폐에서 결합하고 조직에서 방출 |

산소와 강하게 결합하는 것이 언제나 좋은 운반을 뜻하지는 않는다. 폐에서 잘 받더라도 조직에서 잘 놓지 않으면 공급이 부족해질 수 있다. Mb의 높은 affinity는 근육 내부에서의 역할에 맞고, Hb는 여러 사슬 사이 조절로 결합과 방출의 균형을 맞춘다.

적혈구 자신은 성숙한 상태에서 mitochondria가 없어 주로 glycolysis로 adenosine triphosphate(ATP)를 만든다. 산소를 운반하는 세포라는 사실과 그 세포가 산소를 이용해 주로 ATP를 만드는지 여부는 다른 질문이다. RBC 대사는 아래의 2,3-BPG 생성과도 연결된다.

@sec 3. 한 자리에 산소가 붙으면 다른 자리의 결합도 쉬워진다
Hb의 네 산소 결합 자리는 완전히 독립적이지 않다. 한 heme에 산소가 붙으면 iron과 proximal histidine의 위치가 바뀌고, 이 변화가 사슬 사이의 결합 배치에 전달된다. 그 결과 다른 heme도 산소를 받기 쉬워진다. 이를 positive cooperativity라고 한다. 단순히 자리가 네 개라는 사실과 서로의 결합을 돕는다는 사실은 구별한다. [T3, PDF 70–74]

교재에서는 산소와 덜 결합하는 T(tense) 상태와 더 잘 결합하는 R(relaxed) 상태로 이 관계를 설명한다. T 상태를 안정화하는 결합이 유지되면 affinity가 낮고, 산소 결합으로 R 상태가 유리해지면 affinity가 높아진다. 이 상태들은 많은 Hb 분자의 행동을 이해하기 위한 대표적 설명이다.

**분자 변화에서 결합 결과까지**

| 순서 | 변화 | 다음 결과 |
|---|---|---|
| 1 | Heme에 O_{2}가 붙는다. | Iron과 연결된 부분의 위치가 바뀐다. |
| 2 | Globin과 사슬 사이 배치가 달라진다. | 높은 affinity 상태가 유리해진다. |
| 3 | 나머지 자리의 산소 결합이 쉬워진다. | S-shaped saturation curve가 나타난다. |

Allostery는 한 위치의 변화가 다른 위치의 기능을 바꾸는 관계다. Hb에서는 산소 자체가 이런 조절에 참여하고, H^{+}나 2,3-BPG처럼 산소와 다른 분자도 참여한다.

>> 사슬이 여러 개라고 반드시 cooperative한 것은 아니다. 구조와 실제 결합 곡선을 연결해 판단한다.

@sec 4. P_{50}와 곡선 이동은 산소를 얼마나 쉽게 놓는지 알려 준다
산소 결합 곡선의 가로축은 산소 분압(pO_{2}), 세로축은 결합 자리 중 산소가 붙은 비율인 saturation이다. P_{50}는 절반의 자리가 찰 때의 산소 분압이다. 더 낮은 분압에서도 절반이 차면 affinity가 높은 것이므로 P_{50}가 낮다. 교재의 대표값은 Mb 약 1 mmHg, Hb 약 26 mmHg다. 실제 Hb 값은 pH, 온도, 2,3-BPG 등 조건에 따라 달라진다. [T3, PDF 71–74]

**같은 조직 산소 분압에서 비교하는 방향**

| 곡선 변화 | P_{50} | Affinity | 조직에서의 방출 경향 |
|---|---|---|---|
| Left shift | 감소 | 증가 | 더 유지하여 방출이 줄어든다. |
| Right shift | 증가 | 감소 | 더 쉽게 방출한다. |

Hb의 S-shaped curve는 폐의 높은 분압에서 잘 결합하고 조직의 낮은 분압에서 상당한 양을 방출하게 한다. 그러나 right shift가 전체 산소 공급을 항상 개선하는 것은 아니다. 폐의 분압이 낮으면 산소를 받는 단계도 불리해질 수 있다. 혈류와 Hb의 양도 함께 필요하다.

> **학습용 비교** 같은 Hb 농도에서 폐 98%, 조직을 지난 뒤 75%라면 결합 자리의 23%p에 해당하는 산소를 놓았다. 다른 조건에서 90%→60%면 차이는 30%p다. 차이가 더 크다는 정보와 전체 산소 공급이 더 좋다는 결론은 같지 않다. 혈류와 동맥혈의 실제 산소 함량을 함께 본다.

@sec 5. 일하는 조직의 CO_{2}와 H^{+}는 산소 방출을 돕는다
조직이 산소를 사용하면 CO_{2}가 생긴다. CO_{2}가 bicarbonate 평형에 들어가면 H^{+}와도 연결된다. H^{+}와 CO_{2}가 늘어나는 조건에서 Hb의 낮은 affinity 상태가 유리해져 산소를 더 쉽게 놓는다. pH 감소 또는 CO_{2} 증가가 산소 결합을 낮추는 관계를 Bohr effect라고 한다. [T3, PDF 75–80]

H^{+}는 일부 작용기의 전하와 사슬 사이 결합을 바꾼다. CO_{2}의 대부분은 bicarbonate로 운반되고 일부는 globin의 amino 말단에 carbamate로 붙는다. CO_{2}가 산소와 같은 iron 자리에 붙는다고 설명하면 CO와 혼동한 것이다.

**폐와 조직에서 반대 방향으로 작동하는 이유**

| 장소 | 산소·CO_{2}의 흐름 | Hb 기능 |
|---|---|---|
| 대사 조직 | 산소 소비, CO_{2} 생성 | 산소 방출과 H^{+} 결합에 유리 |
| 폐 | 산소 공급, CO_{2} 배출 | 산소 결합과 H^{+}·CO_{2} 방출에 유리 |

2,3-Bisphosphoglycerate(2,3-BPG)는 적혈구의 glycolysis 중간물에서 만들어진다. HbA의 β-chain 사이 중앙 공간에 결합하여 T 상태를 안정화한다. 그래서 affinity를 낮추고 조직의 산소 방출을 돕는다. Tetramer당 중앙 결합 공간 한 곳을 설명하는 것이며 heme 네 개에 각각 하나씩 붙는 것은 아니다.

Fetal hemoglobin(HbF)은 α_{2}γ_{2}다. γ-chain은 2,3-BPG와 덜 강하게 상호작용하여 같은 생리적 조건에서 HbA보다 산소 affinity가 높다. 이는 태반에서 태아 쪽 혈액이 산소를 받는 데 도움을 준다. [T3, PDF 77–83]

>> HbF의 높은 affinity는 다른 iron이 아니라 globin과 조절 물질의 상호작용 차이로 설명한다.

~ 탐구 질문: 2,3-BPG를 올려 affinity를 낮추면 언제나 좋은가? 조직 방출뿐 아니라 폐에서의 결합과 HbS의 deoxy-state polymerization도 함께 고려해야 한다.

@sec 6. CO 중독과 methemoglobinemia는 정상처럼 보이는 산소 측정을 오도할 수 있다
Carbon monoxide(CO)는 heme iron에 결합하여 carboxyhemoglobin을 만든다. 산소에 사용할 자리가 줄고, 남은 자리는 산소를 더 잘 붙잡아 조직에 놓기 어려워진다. 따라서 운반 가능한 양의 감소와 방출 장애가 함께 생긴다. CO toxicity에는 세포의 산소 이용 장애도 관여할 수 있다. [T3, PDF 80–81]

일반적인 two-wavelength pulse oximeter는 COHb가 있을 때 정확하지 않을 수 있다. 정상에 가까운 SpO_{2}만으로 CO 중독을 배제하지 않는다. 여러 파장에서 Hb 종류를 구별하는 CO-oximetry와 노출·증상을 함께 본다. 혈액의 산소 분압은 주로 녹아 있는 산소를 반영하므로 운반 Hb의 정상 기능을 보장하지 않는다. [C1]

**운반 장애가 생긴 지점의 차이**

| 상태 | 직접 문제 | 운반에 미치는 결과 |
|---|---|---|
| COHb 증가 | CO가 heme 자리를 차지 | 유효 자리 감소·남은 산소의 방출 저하 |
| MetHb 증가 | Iron이 Fe^{3+} 상태 | 정상적으로 산소를 결합할 자리 감소 |
| 빈혈 | 단위 혈액당 Hb 양 감소 | 남은 Hb가 정상이어도 총 운반량 감소 |

Methemoglobin은 Fe^{3+} iron을 가진 Hb다. 정상 적혈구에서는 reduced nicotinamide adenine dinucleotide(NADH)를 사용하는 cytochrome b_{5} reductase 계통이 이를 기능하는 상태로 되돌리는 주된 역할을 한다. Oxidant exposure가 많거나 환원 능력이 부족하면 MetHb가 쌓인다. [T3, PDF 91–92]

Methylene blue는 환원형인 leucomethylene blue를 통해 Hb iron을 Fe^{2+}로 되돌리는 데 도움을 준다. 약물 자체가 iron으로 바뀌는 것은 아니다. 이 과정은 reduced nicotinamide adenine dinucleotide phosphate(NADPH)와 연결된다. Glucose-6-phosphate dehydrogenase(G6PD) deficiency에서는 효과와 hemolysis 문제가 있어 라벨상 금기에 해당한다. [C2] 기전과 상세한 치료 선택·용량은 구별한다.

@sec 7. HbS는 단백질 성질의 변화이고 thalassemia는 사슬 생성의 불균형이다
Hemoglobin S(HbS)는 mature β-chain의 6번 glutamate가 valine으로 바뀐 variant다. 음전하를 띤 곁가지가 nonpolar 곁가지로 바뀌어, 산소가 떨어진 HbS 분자끼리 모이기 쉬워진다. Deoxy HbS polymer가 적혈구 안에 생기면 세포가 잘 변형되지 못하고 membrane 손상과 혈관 막힘에 기여한다. [T3, PDF 85–90]

혈관이 막히면 조직 산소 공급이 줄어 통증과 허혈성 손상이 생길 수 있다. 적혈구가 손상되어 빨리 파괴되면 anemia와 bilirubin 증가가 생길 수 있다. 같은 residue 변화에서 시작해도 혈류 장애와 세포 파괴는 서로 다른 중간 과정이다. 산소가 떨어지는 조건과 적혈구 안 HbS 농도를 높이는 탈수는 polymerization에 불리한 조건이 될 수 있다.

**Globin 장애를 구별하는 기준**

| 예 | 변화 | 주된 분자 문제 |
|---|---|---|
| HbS | Glu→Val | Deoxy-state polymerization |
| Hemoglobin C(HbC) | 같은 자리의 Glu→Lys | 전하가 바뀌지만 HbS와 같은 nonpolar 치환은 아님 |
| β-Thalassemia | β-Chain 생성 감소 | α-chain이 상대적으로 남아 세포 손상에 기여 |
| α-Thalassemia | α-Chain 생성 감소 | 발달 단계에 따라 γ 또는 β-chain이 상대적으로 남음 |

Thalassemia에서는 Hb가 적어질 뿐 아니라 조합할 상대를 잃은 chain이 문제를 만든다. Fetal HbF에는 β 대신 γ-chain이 있으므로 심한 β-chain 부족은 출생 뒤 더 뚜렷해질 수 있다. α-chain은 HbF와 HbA 양쪽에 필요하여 심한 α-chain 부족은 태아기에도 영향을 준다. [T3, PDF 92–96]

α-Chain 부족 때 성인에서 β_{4}인 HbH, 태아에서 γ_{4}인 Hb Bart가 형성될 수 있다. 남은 사슬이 tetramer를 만들었다고 정상 Hb의 운반 기능이 복구된 것은 아니다. 정상 chain 조합과 affinity·stability가 모두 필요하다.

>> HbS의 아미노산 성질 변화와 thalassemia의 생성량 불균형을 같은 기전으로 설명하지 않는다.

@sec 8. 산소 포화도가 정상이어도 운반량은 부족할 수 있다
산소 분압은 녹아 있는 산소의 상태, saturation은 Hb 자리 중 산소가 붙은 비율, oxygen content는 혈액 일정 부피의 산소 총량이다. Hb가 절반으로 줄면 남은 Hb의 saturation이 정상이어도 총량은 크게 줄어든다. 또한 혈액의 content가 충분해도 혈류가 적으면 조직에 도달하는 산소가 적어진다.

@eq C_{a}O_{2}(mL/dL) ≈ 1.34 × Hb(g/dL) × saturation(fraction) + 0.003 × P_{a}O_{2}(mmHg)

첫 항은 Hb에 붙은 산소, 둘째 항은 혈액에 녹은 산소다. 98%라면 fraction은 0.98로 넣는다. 이는 정상적으로 산소를 결합하는 Hb를 전제한 근사식이다. Dyshemoglobin이 많으면 saturation의 측정 방식과 어떤 Hb 종류를 포함한 값인지 확인해야 한다. 계수의 사용 근거는 보충 문헌에 제시한다. [R1]

**학습용 가정: 포화도는 같지만 Hb 양은 다름**

| 가정 | Hb | Saturation·산소 분압 | 계산 산소 함량 |
|---|---|---|---|
| A | 15 g/dL | 0.98·100 mmHg | 약 20.0 mL/dL |
| B | 7.5 g/dL | 0.98·100 mmHg | 약 10.15 mL/dL |

이 값은 진단 기준이나 수혈 기준이 아니라 계산 연습의 가정이다. 결과는 같은 포화도에서도 Hb 양이 운반량을 바꾼다는 뜻이다. 실제 조직 산소 공급에는 혈류, 지역별 분포, 세포의 산소 이용도 관여한다.

~ 탐구 질문: Hb affinity를 바꾼 중재가 좋은지 무엇으로 확인할까? P_{50}뿐 아니라 폐의 결합, 조직의 방출, Hb 농도와 혈류를 함께 본다. HbS에서는 polymerization과 혈관 사건도 별도 결과다. 한 숫자가 좋아졌다는 사실을 모든 임상 결과의 개선으로 확대하지 않는다.

@quiz
Q: **판단.** 산소가 붙은 oxyhemoglobin은 Fe^{3+} hemoglobin인가?
A: 아니다. 정상 산소 결합과 ferric iron을 가진 methemoglobin을 구별한다.

Q: **판단.** P_{50}가 낮아지면 산소를 조직에 더 쉽게 놓는가?
A: 반대다. 더 낮은 분압에서 절반이 차므로 affinity가 높다. 같은 조직 조건에서는 더 유지하는 경향이다.

Q: **판단.** CO 노출 뒤 일반 pulse oximeter가 정상에 가까우면 중독을 배제할 수 있는가?
A: 없다. 일반 측정은 COHb가 있을 때 정확하지 않을 수 있다. 노출과 증상, Hb 종류를 구별하는 측정을 함께 본다.

Q: **판단.** Hb 농도와 혈류를 보지 않고 saturation만으로 조직 산소 공급을 판단해도 되는가?
A: 안 된다. Saturation은 비율이고 content와 delivery는 양과 흐름의 정보다.

Q: **설명.** HbF가 태반에서 산소를 받는 데 유리한 이유는?
A: γ-chain이 2,3-BPG와 덜 강하게 상호작용해 같은 생리적 조건에서 상대적으로 높은 affinity를 가진다.

Q: **설명.** HbS에서 pain과 anemia를 각각 어떤 중간 과정으로 연결하는가?
A: Deoxy HbS polymer는 변형성 저하와 혈관 막힘을 통해 pain·ischemia에, 적혈구 손상·파괴를 통해 anemia에 연결된다.

Q: **계산.** Hb 10 g/dL, saturation 95%, 산소 분압 80 mmHg인 학습용 가정의 산소 함량은?
A: 1.34×10×0.95 + 0.003×80 = 12.97 mL/dL다. %를 fraction으로 바꾸고 단위를 확인한다.

@ref
- Abali EE, Cline SD, Franklin DS, Viselli SM. *Lippincott Illustrated Reviews: Biochemistry*. 8th ed. Wolters Kluwer; 2022. Chapter 3, “Globular Proteins.” 제공 PDF 66–100페이지. Heme·globin structure: II.A–C, 66–71페이지; binding curve·allostery: II.D–E, 71–81페이지; minor Hb·gene organization: II.F–III, 81–85페이지; hemoglobinopathies: IV, 85–96페이지. 페이지는 제공 PDF의 1-based 파일 페이지이며 인쇄 쪽수가 아니다.
- C1. Centers for Disease Control and Prevention. Clinical Guidance for Carbon Monoxide Poisoning Following Disasters and Severe Weather (https://www.cdc.gov/carbon-monoxide/hcp/clinical-guidance/index.html). COHb 측정, 일반 two-wavelength pulse oximetry의 한계, cellular toxicity. 확인일 2026-10-15.
- C2. DailyMed. Methylene blue injection: prescribing information (https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=691a6872-bc2f-d492-11c6-c3eec25aa3d3). XIROMED, LLC. 라벨 개정 2026-05; sections 4, 5.3, 12.1. Redox mechanism·G6PD deficiency. 확인일 2026-10-15.
- R1. Gatterer H, Menz V, Burtscher M. Acute Moderate Hypoxia Reduces One-Legged Cycling Performance Despite Compensatory Increase in Peak Cardiac Output: A Pilot Study (https://www.mdpi.com/1660-4601/18/7/3732). *International Journal of Environmental Research and Public Health*. 2021;18(7):3732. DOI: 10.3390/ijerph18073732. Oxygen-content·delivery 계산식의 사용 근거. 본문 수치 예시는 해당 연구의 결과를 복제한 것이 아니라 명시된 가정으로 새로 계산한 값이다.
