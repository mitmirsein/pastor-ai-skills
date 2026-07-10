---
last_updated: 2026-07-05
schema_version: 3
active_sermons: []
active_series: []
active_visitations: []
recent_topics: ["대표사상", "영적민감함"]
open_prayer_requests: []
lessons: []
last_qt_date: null
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

### 1.4 심방 기한 기준 — 단일 정의 (SSOT)
모든 도구는 `followup_due`에 대해 아래 세 계층을 따릅니다 (도구별 자의 기준 금지):
- **동선 병기** (오늘 갈 곳): `followup_due ≤ 오늘 + 2일` — `pastoral_rhythm` §2.3
- **임박 경고**: `followup_due ≤ 오늘 + 7일` — Concierge 로드 프로토콜·`journal-show` H3·`weekly-briefing` 우선순위
- **만료** (archive 후보): `followup_due < 오늘 − 14일` — §1.3·`journal_lint` C6·`journal-show` H4·`weekly-briefing` 헬스
- **시리즈/lineage 정체 경고**: 마지막 갱신 **21일** 경과 — `journal-show` H5·H6·`weekly-briefing` 헬스

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
    stage: research              # 유효 값: §3.1.1 stage enum (SSOT) 참조
    next_step: redteam           # 다음 권장 스킬
    started_on: 2026-05-06
    preached_on: null            # 선포일 (강단 후 채움)
    retro_done: false            # (schema v2) 선포 후 회고(sermon-retro) 완료 여부
    series_id: null              # 시리즈에 속할 경우 series.id 참조
    notes: "사회적 수치 vs 개인적 믿음 긴장 강조"
```

#### 3.1.1 stage enum — 단일 정의 (SSOT)

`active_sermons[].stage`의 유효 값은 아래 목록이 **유일한 정의**입니다. `harness/journal_lint.md`(C2 타입 검사)와 `core/pastoral_rhythm.md`(지연 감지의 단계 순서)는 이 목록을 따르며, 다른 파일의 enum 사본과 어긋나면 이 목록이 우선합니다.

- **파이프라인 단계 (순서 있음)** — 값은 "완료된 마지막 단계"를 뜻합니다:
  `devotional → seed → brainstorm → research → dilemma → outline → redteam → drafted → preached → published`
  (`dilemma`는 선택 단계로 건너뛸 수 있습니다. v2.11 발아 파이프라인의 `devotional`(큐티 누적)·`seed`(씨앗 합성)·`outline`(개요 동반작성)을 포함합니다. 단, 큐티 스킬(qt-companion·devotional-generator)은 journal에 **신규 항목을 만들지 않으므로** 발아 항목의 journal 진입은 `seed`부터입니다 — `devotional` 값은 수동·과거 항목 호환용입니다.)
- **예약 단계**: `pending` — `sermon-series-planner`가 다음 주차 본문을 사전 등록할 때만 사용합니다.
- **파생 작업 단계 (순서 없음)**: `study`(성경공부 교안) · `smallgroup`(나눔지) — 파생물 생성 기록이지 본체 진행 단계가 아니므로, 기존 stage가 이보다 늦으면(예: `preached`) **본체 stage를 후퇴시키지 않고 `notes`에만 기록**합니다.
- **발행 세분값 매핑**: 파일 YAML의 `published_blog` / `published_column` / `published_tts` / `published_cardnews`는 lineage 파일 전용 표기이며, journal에는 **발행 전이 가드**(`core/_hooks.md` §3.6)를 거쳐 반영합니다 — `preached_on`이 채워진 항목만 `published`​로 전이하고, 선포 전이면 stage를 바꾸지 않고 `notes`에만 기록합니다. `column_draft`(qt-to-column)·`devotional_draft`(qt-to-devotional, v2.16)는 journal의 stage를 바꾸지 않습니다(`notes`만).

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
    last_updated: 2026-05-10     # 시리즈 관련 작업이 있을 때마다 갱신 (정체 감지용 — journal-show H5·weekly-briefing)
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

### 3.6 `lessons` *(schema v2 — sermon-retro가 기록 · v2.20 — publication-retro도 기록)*
설교 후 회고(그리고 v2.20부터 발행물 회고)에서 나온 "다음에 다르게 할 것". 최근 5건 FIFO 회전(설교·발행 공유). `sermon-red-team`·`weekly-briefing`·*(v2.18)* `sermon-brainstorming`·`sermon-outline-codraft`가 반복 패턴/상기 신호로 참조한다.

```yaml
lessons:
  - passage_id: mark-5-25-34
    date: 2026-05-12
    lesson: "적용이 추상적이었다 — 다음엔 구체적 한 장면으로"
    source: retro               # (v2.20, 선택) retro | publication — 필드 부재 시 retro로 간주 (하위호환)
```

### 3.7 `open_tensions` *(v2.15 — sermon-retro가 기록)*
선포된 설교가 다 담지 못해 남은 신학적 긴장(잔여 아포리아). `lessons`(§3.6, 기술 회고)와 대칭인 신학적 잔여다. `qt-companion` 2단계가 재소환 소스로 읽어 다음 묵상으로 되먹인다(나선 구조). 최근 5건 FIFO 회전. 자동 삭제 없음 — 해소 판단은 목회자의 몫이다.

```yaml
open_tensions:
  - passage_id: leviticus-4
    date: 2026-07-12            # 기록일 (선포 직후 회고일)
    tension: "..."              # 목회자의 표현 그대로 한 문장 (PII 정책 §2 적용)
    source: retro               # retro | manual
```

> 🔄 **에코 루프 차단 (불변식):** `open_tensions`는 `qt-germinate-scan` 축 3의 반복 횟수 집계에 **들어가지 않는다** — 재소환을 거쳐 큐티 노트에 자발적으로 다시 등장한 것만 집계된다. journal 항목 자체는 맥락 병기용이다.

### 3.8 `last_qt_date` *(schema v3 — qt-companion만 기록)*
목회자의 마지막 큐티 기록일. `qt-companion`의 `qt-log` 저장 시에만 갱신되며(`core/_hooks.md` §3), 다른 어떤 스킬도 이 필드를 만지지 않는다. **날짜만 기록한다** — 묵상 내용·본문·횟수는 journal에 남기지 않는다(큐티의 실질은 발아 코퍼스의 몫, 프라이버시 최소 기록).

```yaml
last_qt_date: 2026-07-09       # YYYY-MM-DD | null (한 번도 기록 없음)
```

- **소비처**: Concierge 부트 — 오늘로부터 **3일 이상** 경과 시 헤더 아래 침묵의 초대 1줄(강요·죄책 금지, `null`이면 침묵 — `core/pastoral_rhythm.md` §2.5). `weekly-briefing` 큐티 스냅샷의 보조 신호.
- **v2 → v3 마이그레이션**: 필드가 없는 journal은 정상이다 — 첫 `qt-log` 저장 시 필드가 생기며, `journal_lint` C1이 `schema_version: 2` + 필드 부재를 감지하면 마이그레이션(버전 승격)을 제안만 한다(자동 수정 금지).

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
