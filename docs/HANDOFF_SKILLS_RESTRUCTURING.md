# Pastor-AI-Skills-KR: 스킬 구조 재편 리포트 (Handoff)

**작성일**: 2026-05-04
**핵심 설계 원칙**: 
1. **Easy for using (사용의 용이성)**: 목회자의 인지적 과부하 최소화
2. **Highest Quality over Quantity (양보다 최상의 품질)**: 다수의 범용 기능보다, 목양에 필수적인 고도화된 최적의 기능에 집중

---

## 1. 현재 구조에 대한 비평적 진단

현재 `core/skills` 하위에 20개의 스킬이 병렬적으로 존재합니다. 현장 목회자의 니즈를 정확히 파악한 훌륭한 라인업이지만, 시스템 설계 관점에서 다음과 같은 문제점이 발생합니다.

### 1) 선택의 역설 (Paradox of Choice) 및 인지적 과부하
* 사용자는 20개의 스킬 목록을 마주했을 때 "지금 상황에 무엇을 써야 할지" 고민하게 됩니다.
* 동일한 '설교 원고 재생산' 작업이 블로그, 칼럼, TTS, 카드뉴스, 소셜 미디어 등 5개 이상의 스킬로 파편화되어 있어 워크플로우가 파편화됩니다.

### 2) 범용 기능과 특화 기능의 혼재
* `admin-email`, `meeting-agenda`, `social-media-post` 등은 LLM이 기본적으로 잘 수행하는 '일반 범용 기능'입니다.
* 이러한 범용 기능들이 목회 특화 스킬(예: `sermon-research`, `biblical-dilemma-solver`)과 같은 계층에 존재하면, 정작 에너지를 쏟아야 할 코어 스킬의 중요도가 희석됩니다.

### 3) 워크플로우의 단절
* 목회자의 일주일(발상 -> 연구 -> 원고 작성 -> 검증 -> 설교 후 재생산 및 적용)이라는 연속적인 라이프사이클을 따라 물 흐르듯 이어지는 마스터 파이프라인이 부재합니다.

---

## 2. 차기 업데이트 제안: 4대 마스터 스킬 대통합

20개의 파편화된 스킬을 **목회자의 실제 업무 흐름에 맞춘 4개의 거대한 마스터 스킬**로 대통합(Consolidation)할 것을 제안합니다. 각 마스터 스킬 내부에서 세부 옵션을 선택(Select)하게 하여 UI/UX 경험을 극대화합니다.

### 마스터 스킬 1: `Sermon-Copilot` (설교 준비 및 주해 파트너)
* **목표:** 강단에 오르기 전까지의 모든 발상, 주해, 맹점 방어를 책임지는 최상위 품질 엔진 (6 Gems 엔진 탑재 등)
* **통합 대상:** 
  - `sermon-research` (주해)
  - `sermon-brainstorming` (발상)
  - `biblical-dilemma-solver` (난제 변증)
  - `sermon-red-team` (원고 검증)
  - `sermon-series-planner` (시리즈 기획)

### 마스터 스킬 2: `Omnichannel-Publisher` (설교 원소스 멀티유즈 배포기)
* **목표:** 하나의 주일 설교 원고를 입력하면, 원하는 모든 매체 포맷으로 원터치 전환
* **통합 대상:**
  - `sermon-to-column` (프리미엄 칼럼)
  - `sermon-to-tts` (오디오/라디오 에세이 대본)
  - `sermon-to-blog` (웹/SEO 최적화)
  - `sermon-cardnews-maker` & `social-media-post` (소셜 미디어용)

### 마스터 스킬 3: `Pastoral-Content` (목양 및 적용 콘텐츠 생성기)
* **목표:** 설교를 성도의 삶으로 연결하는 성경공부 및 적용/위로 메시지 일괄 생성
* **통합 대상:**
  - `bible-study-generator` (통합 성경공부 교안)
  - `small-group-guide` (구역/셀 나눔 질문)
  - `devotional-generator` & `mid-week-meditation` (주중 묵상/QT)
  - `visitation-guide` (상황별 심방 가이드)

### 마스터 스킬 4: `Church-Admin` (교회 행정 및 커뮤니케이션 비서)
* **목표:** 단순 반복되는 교회 행정 업무의 최소화 및 톤앤매너 표준화
* **통합 대상:**
  - `bulletin-helper` & `announcement-script` (주보 및 광고 대본)
  - `pastoral-letter` (목회 서신)
  - `admin-email` & `meeting-agenda` (이메일 및 회의)
* **비고:** 범용성이 높은 기능이므로 프롬프트 다이어트를 통해 최대한 가볍게 유지

---

## 3. Action Items (다음 작업자를 위한 가이드)

1. **Phase 1: 재생산 스킬 통합 시범 적용**
   - 현재 `sermon-to-column`과 `sermon-to-tts`를 분리 유지하고 있으나, 차기 업데이트 시 `Omnichannel-Publisher` 형태의 단일 라우팅 프롬프트로 병합 테스트를 진행할 것.
   - 프롬프트 설계: *"어떤 포맷으로 변환하시겠습니까? [1] 블로그 [2] 카드뉴스 [3] TTS 대본 [4] 칼럼"*

2. **Phase 2: 연구 엔진(Sermon-Copilot) 고도화**
   - 통합 시 가장 공을 들여야 할 부분. 단순한 기능 병합이 아니라, 프롬프트 체이닝(Prompt Chaining)을 통해 "브레인스토밍 -> 주해 -> 레드팀 점검"이 하나의 대화 안에서 매끄럽게 이루어지도록 시스템 프롬프트를 설계해야 함.

3. **Phase 3: 파일 구조 개편 및 문서화**
   - 기존의 단일 `.md` 파일들을 마스터 스킬 단위로 그룹화하는 폴더 구조 재편 고려.
   - 사용자 가이드(README)를 4대 마스터 스킬 중심으로 직관적으로 재작성.
