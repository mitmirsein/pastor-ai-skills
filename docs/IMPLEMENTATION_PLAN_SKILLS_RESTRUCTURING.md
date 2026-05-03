# Pastor-AI-Skills-KR: 오케스트레이터 + 전문가 길드 구현 계획서 (Implementation Plan)

## 1. 아키텍처 개요
본 구현 계획은 기존 20개의 파편화된 스킬을 **단일 진입점(Concierge)**과 **명문화된 파이프라인(Workflow Chains)**, 그리고 **특화 스킬(Guild)**의 3계층 구조로 재편하는 작업을 정의합니다.

- **Layer 1: Orchestrator** (`Pastor-Concierge`) - 사용자의 자연어를 해석하여 적절한 스킬로 라우팅
- **Layer 2: Pipeline** - 각 스킬 하단의 `Call to Action`을 통한 자연스러운 작업 흐름 연결
- **Layer 3: Specialized Guild** - 고도의 정밀도를 유지하는 개별 특화 스킬 유지 및 중복 제거

---

## 2. Phase 1: `Pastor-Concierge` 라우터 구현

### 2.1. 핵심 역할
사용자의 일상적인 자연어 입력을 받아, **의도(Intent)를 분류**하고 해당 작업에 필요한 **초기 컨텍스트(Context)를 추출**한 뒤, 가장 적합한 **전문 스킬을 추천**합니다.

### 2.2. 시스템 프롬프트 구조 (초안)
- **Role:** 당신은 목회자의 일정과 사역을 돕는 수석 비서 'Pastor-Concierge'입니다.
- **Task:** 사용자의 자연어 요청을 분석하여 4대 목회 카테고리 중 하나로 분류하고, 최적의 스킬을 매칭합니다.
- **Rules:**
  1. 절대 직접 결과물을 작성하거나 작업을 수행하지 마십시오. (단순 비서 역할에 충실할 것)
  2. 사용자의 발화에서 필수 정보를 추출하고, 누락된 정보가 있다면 한 번 더 질문하여 구체화하십시오.
  3. 매칭된 스킬의 실행 명령어와 함께, 추출한 정보를 그대로 넘겨줄 수 있는 '복사/붙여넣기'용 프롬프트를 제공하십시오.
- **Output Format:**
  - 🎯 **파악된 목적:** (예: 장례 심방 준비)
  - 💡 **추천 스킬:** (예: `/visitation-guide` 스킬 사용 권장)
  - 📋 **초기 컨텍스트:** (상황: 모친상, 대상: 40대 남성 성도, 특징: 갑작스러운 사고)
  - 🚀 **바로 실행하기:** (해당 스킬에 그대로 붙여넣을 수 있도록 정리된 최적화 프롬프트 제공)

---

## 3. Phase 2: 워크플로우 체인 (파이프라인) 명문화

스킬 간의 물리적 결합(Consolidation) 대신, 각 스킬의 결과물 출력 마지막에 **다음 단계를 제안하는 `Call to Action` 블록**을 시스템 프롬프트에 강제 삽입합니다.

### 3.1. 4대 파이프라인 정의
1. **주일 준비 파이프라인:** `sermon-brainstorming` ➔ `sermon-research` ➔ `biblical-dilemma-solver` ➔ `sermon-red-team`
2. **목양 적용 파이프라인:** 설교 연구 결과물 ➔ `bible-study-generator` ➔ `small-group-guide` ➔ `devotional-generator`
3. **설교 확산 파이프라인:** (Phase 3의 `Sermon-Republisher` 참조)
4. **행정 보조 파이프라인:** 독립 실행 형태 위주, 필요시 `pastoral-letter` ➔ `church-social-post` 연결

### 3.2. Call to Action 템플릿 (각 스킬 시스템 프롬프트 하단에 일괄 적용)
```text
[시스템 지침: 결과물 출력을 마친 후, 반드시 아래 형식으로 다음 파이프라인 스킬을 추천할 것]
---
⏭️ **다음 단계 추천 (Next Steps)**
이번 작업이 완료되었습니다. 이어서 다음 스킬을 활용해 워크플로우를 이어가보세요:
* **[추천 스킬명]**: (추천하는 이유 설명) 
  * 💡 실행 팁: "위 결과물의 [핵심 내용]을 복사하여 [추천 스킬]에 붙여넣어 주세요."
```

---

## 4. Phase 3: 얇은 라우터 (Thin Router) 스킬 신설

설교 원고라는 '동일한 입력값'을 가지는 확산/재생산 계열 스킬들을 묶어줄 가벼운 라우터 스킬을 신설합니다.

### 4.1. `Sermon-Republisher` 스킬
- **동작 방식:**
  1. 사용자에게 '주일 설교 원고' 입력을 요청함.
  2. 원고를 분석하여 메인 테마와 핵심 메시지를 파악 (상태 유지).
  3. 사용자에게 변환할 포맷을 선택하도록 요청 (블로그, 칼럼, 카드뉴스, TTS 대본).
  4. 선택에 따라 **기존의 특화 스킬 프롬프트(Sub-prompt)**를 백단에서 호출하여 결과를 생성.
- **장점:** 모든 페르소나를 한 프롬프트에 구겨 넣는 마스터 스킬 대통합과 달리, 사용자가 포맷을 선택할 때만 해당 출력 규격과 페르소나가 작동하므로 **컨텍스트 윈도우 오염 및 정밀도 하락을 완벽히 방지**함.

---

## 5. Phase 4: 스킬 정리 (Pruning & Grouping)

### 5.1. 중복 스킬 병합 (Absorb)
* `church-social-post` ➔ `sermon-cardnews-maker`로 흡수 병합 (카드뉴스 기획 시 텍스트 추출 기능으로 소셜 포스트 커버 가능)
* `mid-week-devotional` ➔ `devotional-generator`로 흡수 병합 (주중/주일 묵상 여부는 단순 파라미터/옵션으로 처리 가능)

### 5.2. 디렉토리/목록 그룹화 (Grouping)
범용 기능과 특화 기능이 섞여 중요도가 희석되는 문제를 해결하기 위해, 디렉토리 구조를 직관적으로 분리합니다.
* `/skills/01_sermon_core/` (💎 설교 코어: 발상, 주해, 변증, 검증)
* `/skills/02_pastoral_care/` (🕊️ 목양 코어: 성경공부, 심방, 구역 나눔)
* `/skills/03_omni_publisher/` (📢 재생산: Republisher 라우터 및 서브 스킬)
* `/skills/04_church_admin/` (📋 행정 보조: 범용 행정, 회의록, 이메일)

---

## 6. 다음 실행 단계 제안 (Next Actions)
1. **`Pastor-Concierge` 스킬 디렉토리 생성 및 `SKILL.md` 시스템 프롬프트 작성 (Phase 1 착수)**
2. 각 코어 스킬(`sermon-research`, `bible-study-generator` 등)의 시스템 프롬프트를 열고 `Call to Action` 블록 강제 주입 (Phase 2 착수)
3. 불필요한 중복 스킬 2개 폴더(`church-social-post`, `mid-week-devotional`) 삭제 및 통합 (Phase 4 착수)
