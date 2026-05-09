---
last_updated: 2026-05-10
schema_version: 1
active_sermons: []
active_series: []
active_visitations: []
recent_topics: []
open_prayer_requests: []
---

# 🪔 Pastor Journal (목회 메모리 레이어)

본 파일은 `Pastor-KR v2.5`의 **목회 메모리 레이어(Memory Layer)** 입니다.
`pastor-concierge`는 매 진입 시 본 파일을 의무적으로 로드하여 사역 컨텍스트를 복원하고, 각 전문 스킬은 작업 종료 시 본 파일을 갱신하여 다음 세션에서도 사역의 연속성이 유지되도록 합니다.

> ⚠️ **단일 진실 공급원(SSOT)** : `core/foundation.md`(교회 메타) + `core/pastor_journal.md`(사역 동향) + `core/liturgical_calendar.md`(절기 자각)
> 이 세 파일이 합쳐져 Concierge의 사고 컨텍스트가 됩니다.

---

## 1. 갱신 정책 (Update Policy)

### 1.1 자동 갱신 (Automatic)
- 모든 스킬은 종료 단계에 `[Journal Update]` 훅을 수행해야 합니다.
- 갱신 대상: 작업한 본문/설교/심방 대상의 진행 상태(stage), `last_updated`, `recent_topics`(중복 제거).
- 갱신 방식: 본 파일을 **읽고-병합-쓰기(Read-Merge-Write)**. 절대 통째로 덮어쓰지 않습니다.

### 1.2 수동 갱신 (Manual)
- 목회자가 직접 편집해도 무방합니다. (예: 종결된 시리즈 archive 처리, 기도제목 정리)
- AI는 사용자가 명시적으로 요청한 경우에만 항목을 **삭제**합니다.

### 1.3 보존 기한 (Retention)
- `active_sermons`: 발행(`preached_on` 채워짐) 후 **4주** 경과 시 archived 로그로 이동.
- `active_visitations`: `followup_due` 경과 후 **2주** 미갱신 시 archived 로그로 이동.
- archived 항목은 본 파일 하단 `## Archive` 섹션에 압축 보관 (한 줄 요약).

---

## 2. PII 정책 (Privacy)

> 🚨 본 파일은 git에 커밋될 수 있는 작업 산출물입니다. **개인정보는 절대 평문으로 기록하지 않습니다.**

| 카테고리 | 허용 표기 | 금지 표기 |
|---|---|---|
| 성도 식별 | "직분 + 이니셜" (예: `K집사`, `L권사`) | 실명, 한글 풀네임, 영문 풀네임 |
| 연락처 | (기록 금지) | 전화번호, 카톡 ID, 이메일, 주소 |
| 가정 상황 | 일반화된 사역 단어 (예: "투병", "사별", "이사") | 구체적 진단명/병원명/사건 상세 |
| 재정 | (기록 금지) | 헌금 액수, 개인 채무, 직장 정보 |

이 규칙은 AI가 본 파일을 **갱신**할 때도 동일하게 적용됩니다. 사용자가 실명을 입력해도 AI는 이니셜로 변환해서 저장합니다.

---

## 3. 스키마 정의 (Schema)

YAML 프론트매터의 각 필드는 다음 의미를 가집니다.

### 3.1 `active_sermons`
진행 중인 개별 설교(아직 강단에서 선포되지 않았거나, 후속 재생산 작업이 남은 설교).

```yaml
active_sermons:
  - id: mark-5-25-34            # passage_id (book-ch-vstart-vend)
    title: "혈루증 여인의 손길"   # 임시 제목
    stage: research_done         # brainstorm | research | dilemma | redteam | drafted | preached | published
    next_step: redteam           # 다음 권장 스킬
    started_on: 2026-05-06
    preached_on: null            # 선포일 (강단 후 채움)
    series_id: null              # 시리즈에 속할 경우 series.id 참조
    notes: "사회적 수치 vs 개인적 믿음 긴장 강조"
```

### 3.2 `active_series`
강해/주제 시리즈의 진행 현황.

```yaml
active_series:
  - id: ephesians-2026-spring
    title: "그리스도 안에서: 에베소서 강해"
    total: 6
    progress: 3                  # 완료 편수
    next_passage: "엡 2:11-22"
    next_passage_id: eph-2-11-22
    started_on: 2026-04-12
    notes: "2장 후반부터 윤리장(章) 진입"
```

### 3.3 `active_visitations`
진행 중인 심방 케이스 (정기/긴급 무관).

```yaml
active_visitations:
  - target: "K집사"               # 직분+이니셜 (PII 정책)
    context: "암 투병 중, 가족 동반 거주"
    last_visit: 2026-05-08
    followup_due: 2026-05-15
    prayer_focus: "치유, 가정 평안"
```

### 3.4 `recent_topics`
최근 4주간 다룬 핵심 주제(중복 회피용). 최대 12개, FIFO로 회전.

```yaml
recent_topics: ["은혜", "고난과 위로", "공동체"]
```

### 3.5 `open_prayer_requests`
공동체 기도제목(특정 성도 식별 정보 없이, 사역 단위로만 기록).

```yaml
open_prayer_requests:
  - id: 2026-05-prayer-01
    item: "5월 새가족 정착"
    raised_on: 2026-05-03
```

---

## 4. Concierge 로드 프로토콜

`pastor-concierge`가 본 파일을 로드할 때 다음 우선순위로 컨텍스트를 추출합니다.

1. `active_series.next_passage` — 다음 주일 설교 후보 (1순위)
2. `active_sermons[stage != preached]` — 미완료 설교 작업
3. `active_visitations[followup_due <= today + 7d]` — 임박한 심방
4. `recent_topics` — 중복 주제 회피
5. `open_prayer_requests` — 목회 서신/광고/심방 기도 시 활용

---

## 5. 초기화 (Bootstrap)

본 파일이 비어있는 상태에서 처음 사용하는 경우, Concierge는 **아무것도 추측하지 않습니다.** 사용자가 첫 사역 요청을 던지면, 그 작업이 끝난 후 처음으로 한 항목을 기록하기 시작합니다. 강제 초기 인터뷰는 수행하지 않습니다.

---

## Archive

(보존 기한 경과 항목이 여기에 한 줄 요약으로 누적됩니다.)
