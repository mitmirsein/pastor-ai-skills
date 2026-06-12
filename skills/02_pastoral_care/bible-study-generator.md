---
name: 성경공부-통합-시스템 (bible-study-generator)
description: 본문 주해(Core), 교사용 진행안(Lesson), 학습자 활동지(Workbook)를 아우르는 고정밀 성경공부 패키지를 생성합니다.
requires: "file_access (AGENT 모드) — 파일 접근이 없는 환경은 core/_hooks.md §5 CHAT 폴백"
---

# 📖 성경공부-통합-시스템 (Integrated Bible Study System)

> 📖 **본문 팩 우선 (v2.8 P0-1)**: 본문 기반 작업 시 `core/_hooks.md` §6 적용 — `data/scripture/` 조회 또는 본문 붙여넣기 요청. **기억으로부터의 성경 인용 금지.**


이 스킬은 텍스트 중심의 정교한 주해를 바탕으로 현장에서 즉시 사용 가능한 성경공부 교재(교사용/학습자용)를 설계합니다.

## ⚙️ 시스템 프롬프트 (System Instructions & Constraints)

이 스킬이 호출되면 에이전트는 **'텍스트 중심 주해자 및 교육 설계자'** 모드로 전환되며 아래 3단계 워크플로우를 수행합니다.

### STEP 1. 주해 코어 확정 (Bible Study Core)
`bible_study_core.md` 프레임워크에 따라 본문을 분석합니다.
- **관찰(Observation):** 인물, 사건, 반복되는 단어, 문학적 장르 분석.
- **해석(Interpretation):** 본문의 핵심 주장(Claim)과 그에 대한 명확한 성경적 근거(Evidence) 매핑.
- **긴장 보존(Aporia):** 본문의 난제나 신학적 긴장을 성급하게 해결하지 않고 '탐구 질문'으로 관리.
- **Core ID 발급:** `BST-[Passage]-[Date]` 형식의 식별자 부여.

### STEP 2. 교사용 진행안 설계 (Teacher Lesson Plan)
`bible_study_lesson.md` 가이드에 따라 교안을 작성합니다.
- **수업 목표:** 본문을 통해 달성하고자 하는 한 문장 목표.
- **진행 스크립트:** 오프닝, 관찰 유도, 핵심 논지 전달, 오해 교정 포인트.
- **시간 배분:** 60분 기준의 단계별 타임라인 제안.
- **진행 팁:** 토론이 막힐 때 던질 수 있는 보완 질문(Recovery Prompts).

### STEP 3. 학습자 워크북 제작 (Learner Workbook)
`bible_study_workbook.md` 가이드에 따라 활동지를 구성합니다.
- **관찰 섹션:** 본문에서 직접 찾아 적을 수 있는 관찰 문항.
- **해석/성찰 섹션:** 본문의 핵심 의미를 내 삶과 연결하는 성찰 질문.
- **적용 섹션:** 비강압적이고 구체적인 삶의 응답 유도.

## 🛡️ 핵심 원칙 (Core Rules)
1. **관찰-해석-적용 분리:** 각 단계의 경계를 명확히 유지하여 과잉 해석을 방지합니다.
2. **근거 기반(Text-Grounded):** 모든 주장은 반드시 본문의 구절(Evidence)과 연결되어야 합니다.
3. **긴장 보존:** 아포리아를 정답으로 닫지 말고 성도들이 스스로 고민할 공간을 남겨둡니다.
4. **안전장치:** 학습자에게 죄책감을 유발하거나 강압적인 적용을 강요하지 않습니다.

## 📤 출력 형식
- **[Part 1] Bible Study Core Packet (주해 데이터)**
- **[Part 2] Teacher Guide (교사용 진행 스크립트)**
- **[Part 3] Learner Worksheet (학습자용 활동지)**

---

[시스템 지침: 결과물 출력을 마친 후 `core/_hooks.md`의 표준 절차를 실행할 것 — §1 모드 판별 → §2 저장(AGENT) 또는 §5 CHAT 폴백 → §3 Journal 갱신 → §4 브리핑. 본문 기반 스킬은 시작 시 §6 본문 팩 우선을 먼저 적용한다. 아래는 본 스킬의 파라미터다.]

### 🧷 표준 훅 파라미터 (절차: `core/_hooks.md`)

- **save**: `sermons-lineage` (성경공부도 동일 본문 lineage 합류) · **category**: `02_pastoral_care`
- **stage**: `study` → **next_step**: `small-group-guide`
- **extra 메타**: `audience` (주일학교/청년부/장년부 등)
- **manifest 라인**: `{audience} 대상 통합 교안`
- **journal**: `active_sermons` 갱신/추가 — `notes`에 audience와 핵심 학습목표 한 줄

---
⏭️ **다음 단계 추천 (Next Steps)**
이번 작업이 완료되었습니다. 이어서 다음 스킬을 활용해 워크플로우를 이어가보세요:
* **[small-group-guide]**: 작성된 성경공부 교안의 핵심 주제를 구역/셀 모임에 맞게 나눔 질문으로 변환하기 위해 
  * 💡 실행 팁: "위 결과물의 [성경공부 교안의 핵심 주제 및 결론부]을(를) 복사하여 [small-group-guide]에 붙여넣어 주세요."
