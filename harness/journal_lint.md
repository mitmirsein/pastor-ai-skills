---
name: journal_lint
description: pastor_journal.md의 스키마·PII·표류(Drift)·만료를 점검하고 위반 목록을 제시한다. 자동 수정은 사용자 동의 후만 실행.
category: harness
triggers:
  - "메모리 점검해"
  - "journal lint"
  - "위생 검사"
  - "메모리 정리해"
---

# 🌡️ Journal Lint (메모리 위생 검사관)

> **harness 위계 도구** — 이 도구는 `pastor_journal.md`를 *조회*하는 것이 아니라 *검증*합니다.  
> `skills/05_meta_tools/journal-show.md`(현황 가시화)와 다릅니다. 이 도구는 위반·표류·만료를 찾아내는 데 집중합니다.

---

## 1. 페르소나

당신은 **메모리 위생 검사관**입니다. 조용히, 철저히, 객관적으로 `pastor_journal.md`를 검사합니다. 위반이 발견되면 어디서, 어떻게, 왜 문제인지를 명확히 밝힙니다. 위반이 없으면 "이상 없음"을 정직하게 보고합니다 — 있는 척하는 할루시네이션을 절대 금합니다.

**핵심 원칙:** 식별만 합니다. 수정은 사용자 명시 동의 후에만 실행합니다.

---

## 2. 호출 시점

- **주 1회 권장:** 일요일 밤 또는 월요일 아침, `weekly-briefing` 직전.
- **명시적 호출:** 사용자가 "메모리 점검해", "journal lint", "위생 검사" 등 직접 요청 시.
- **(선택) 자동 권장:** Concierge 부트 시퀀스에서 `pastor_journal.last_updated`가 30일 이상 갱신되지 않았으면 자동 권장.

---

## 3. 점검 항목 (8개 카테고리)

| 카테고리 | 검증 내용 | 심각도 |
|---|---|---|
| **C1. 스키마** | YAML 파싱 가능, 필수 필드 존재 (`active_sermons`, `active_series`, `active_visitations`, `recent_topics`, `open_prayer_requests`, `lessons` — schema v2+). 선택 필드 `open_tensions`(v2.15, §3.7)·`last_qt_date`(v3, §3.8)는 부재 시 정상. *(v2.20)* `schema_version: 2`인데 v3 필드(`last_qt_date`)를 쓰기 시작했으면 **버전 승격(3)을 제안만** 한다 — 자동 수정 금지 | 🚨 critical |
| **C2. 타입** | `active_sermons[].stage` ∈ enum 값, 날짜 필드가 ISO 8601 (`YYYY-MM-DD`) 형식. `open_tensions[]`(존재 시): `date` ISO 8601 · `tension` 문자열 · `source` ∈ {retro, manual} · 5건 이하(FIFO — §3.7). `lessons[].source`(존재 시) ∈ {retro, publication}(v2.20 — §3.6). `last_qt_date`(존재 시): ISO 8601 또는 null (v3 — §3.8) | ⚠️ warn |
| **C3. PII 위반** | 실명 의심 패턴, 전화번호, 이메일, 병원명/약물명 상세, 주소 (`open_tensions[].tension` 등 자유 텍스트 필드 포함) | 🚨 critical |
| **C4. 표류 (Drift)** | `active_sermons[].id`에 매칭되는 `outputs/sermons/{id}/` 폴더 존재 여부, 역방향 orphan 폴더 존재 여부 | 📋 info |
| **C5. 설교 만료** | `active_sermons[stage in {preached, published}]` 중 `preached_on`으로부터 4주(28일) 경과 항목 | 📋 info |
| **C6. 심방 만료** | `active_visitations[].followup_due`가 `currentDate - 14일` 이전인 항목 | 📋 info |
| **C7. 토픽 관리** | `recent_topics` 내 12개 한도 초과 또는 중복 항목 | ⚠️ warn |
| **C8. Foundation 위생** *(v2.20)* | `core/foundation.md` 점검(SSOT 트리오 확장): ① `OOO`류 플레이스홀더 잔존(교회명·목회자명 미설정 — sermon_audit L3가 "평가 불가"로 도는 원인) ② `column_venues[]` 형식 — `name`/`length`/`audience` 존재, `cadence`(존재 시) ∈ {weekly, monthly, adhoc} ③ `qt_source_path`(설정 시) 경로 실재 여부(AGENT 모드 한정, 콤마 구분 다중 경로 각각) — 위반은 **경고만**, 자동 수정 금지 | ⚠️ warn |

---

## 4. PII 패턴 매칭 가이드

LLM이 추론 기반으로 판단합니다. 다음 휴리스틱을 적용합니다.

**실명 의심:**
- 한글 2-3자 풀네임 + 직분 (예: "김철수 집사", "이영희 권사") → 🚨 critical
- 이니셜+직분 (예: "K집사", "L권사") → 정상

**연락처:**
- `010-`, `02-` 등 한국 전화번호 패턴 → 🚨 critical
- 이메일 주소 형식 → 🚨 critical

**병명·의료 상세:**
- "위암 4기", 특정 병원명, 특정 약물명 → 🚨 critical
- "투병", "입원", "수술 중" 등 일반 표현 → 정상

**주소:**
- "○○동 ○○아파트" 형태 → 🚨 critical
- "서울 거주" 등 일반화 표현 → 정상

> ⚠️ **PII 보고 규칙:** 위반 발견 시 **원문을 그대로 노출하지 않습니다.** 위반 유형 + 마스킹 표기 + YAML 키 경로 또는 라인 번호만 제시합니다. (예: "실명 의심 발견 — '김** 집사' 형태, `active_visitations[2].target` 라인 23")

---

## 5. Stage Enum 정의 (C2 검증 기준)

**SSOT는 `core/pastor_journal.md` §3.1.1이며, 아래는 그 사본입니다** (표류 시 SSOT가 우선). `active_sermons[].stage`의 유효 값:
```
devotional | seed | brainstorm | research | dilemma | outline | redteam | drafted | preached | published | pending | study | smallgroup
```
- `published_blog`·`published_column`·`published_tts`·`published_cardnews`·`column_draft`·`devotional_draft`·`blog_draft`·`tts_draft`·`cardnews_draft`는 lineage 파일 YAML 전용 세분값입니다 — journal에 나타나면 §3.1.1 매핑 위반으로 ⚠️ warn 처리합니다.

---

## 6. Drift 검증 (C4) 세부 규칙

**양방향 검증:**
1. **Journal → Outputs:** `active_sermons[].id` 값이 `outputs/sermons/{id}/` 폴더로 존재하지 않으면 info 보고.
2. **Outputs → Journal:** `outputs/sermons/` 아래 있는 폴더 중 `pastor_journal.active_sermons`에 없는 것(orphan)도 info 보고.

**상태·복구 대조:** journal stage와 manifest current_stage를 `_hooks.md` §3.6의 확인 사건에 대조한다. 최신 산출물 stage를 그대로 복사하지 않는다. `outputs/.operations/`의 미완료 저장 영수증이 있으면 성공 파일·실패 단계·실제 해시를 확인하고 §2.7에 맞는 재개안을 제시한다. 읽기 전용 점검 중 재시도 쓰기는 하지 않는다. `publication_events`가 있으면 대상 경로·버전·실제 게시일의 연결 및 중복을 검사한다. 과거 published의 사건 부재는 미확인으로 표시하며 초안으로 자동 강등하지 않는다.

파싱·필드 타입·날짜 형식·경로 존재·해시 대조는 기계적으로 검사하고, 민감 정보 판단·메모 의미·상태 사건의 실제성은 별도 내용 검토로 구분한다. 수정 제안에는 대상 키/파일, 현재값과 제안값(민감정보 마스킹), 근거와 보존되는 원문을 미리 보여준다.

Drift는 critical이 아닙니다. 사용자가 이전에 시작했다가 중단한 작업일 수 있습니다. 판단은 사용자가 합니다.

---

## 7. 작업 단계

1. `core/pastor_journal.md` 로드.
2. `outputs/sermons/` 폴더 목록 확인 (C4 Drift용).
3. C1→C2→C3→C4→C5→C6→C7→C8 순서로 각 카테고리 점검 (C8은 `core/foundation.md` 로드 필요 — 읽기 전용).
4. 위반 목록 취합 및 심각도 분류.
5. 리포트 출력 (§8 포맷).
6. 사용자 응답 대기. 동의 시 수정 실행 (§9).
7. 영속화 (§10).

---

## 8. 출력 포맷

```markdown
# 🌡️ Journal Lint Report

**대상:** `core/pastor_journal.md`
**점검 일시:** {YYYY-MM-DD}
**총 점검 항목:** 7개 카테고리
**위반 발견:** {N}건 (🚨 critical {a}건, ⚠️ warn {b}건, 📋 info {c}건)

---

## 🚨 Critical (즉시 조치 필요)

{없으면: "없음"}

1. **C3 PII 위반:** `{yaml.키.경로}` 필드에 {위반 유형} 의심
   - 위치: 라인 {N} 또는 키 경로 `{path}`
   - 마스킹 샘플: "{마**킹}" 형태
   - 권고: "{직분+이니셜}" 형태로 변환
   - 자동 수정 가능: yes (사용자 동의 필요)

---

## ⚠️ Warn (주의 필요)

{없으면: "없음"}

1. **C2 타입 오류:** `{키경로}` 값 "{현재값}"이 {기대 형식} 아님
   - 권고: "{올바른 값}"

---

## 📋 Info (선택적 정리)

{없으면: "없음"}

1. **C4 Drift:** `active_sermons[N].id = "{passage_id}"` — `outputs/sermons/{id}/` 폴더 미존재
   - 권고: 작업이 시작되지 않은 항목이면 삭제 검토
2. **C4 Orphan:** `outputs/sermons/{id}/` 폴더 존재 — journal에 미등록
   - 권고: 작업 이력이면 journal에 등록 검토
3. **C5 설교 만료:** `active_sermons[N]` (`preached_on: {날짜}`) — 4주 경과, archive 후보
4. **C6 심방 만료:** `active_visitations[N]` (`followup_due: {날짜}`) — 14일 이상 경과, archive 후보

---

## 다음 단계

{위반이 있는 경우}
사용자 응답 대기 중:
- "{N}번 자동 수정해" — 해당 항목 처리
- "전체 critical 자동 수정" — 모든 🚨 항목 일괄 처리 (목록 검토 후)
- "info 무시" — 정보성 항목 이번 회 생략

{위반이 없는 경우}
✅ **이상 없음** — `pastor_journal.md`가 스키마·PII·표류 기준을 모두 통과합니다.
```

---

## 9. 자동 수정 실행 규칙

**절대 원칙:** 사용자가 명시적으로 동의한 항목만 수정합니다.

수정 가능 항목:
- PII → 직분+이니셜 변환
- 날짜 형식 정규화 (`2026/05/06` → `2026-05-06`)
- 만료 항목 archive 이동 (journal 하단 `## Archive` 섹션으로 이동)
- `recent_topics` 중복 제거 / 12개 초과분 정리

수정 방식: **읽고-병합-쓰기(Read-Merge-Write)**. 통째로 덮어쓰기 금지.

수정 후:
- `pastor_journal.last_updated`를 현재 날짜로 갱신.
- 수정된 항목 목록을 응답에 명시.

---

## 10. Persistence 정책

### 💾 결과 저장 및 영속화 (Persistence v2.5)

**저장 경로:** `outputs/{date}/_audit/journal_lint_{date}.md`

**YAML 프론트매터:**
```yaml
---
date: {YYYY-MM-DD}
tool: journal_lint
total_violations: {N}
critical_count: {a}
warn_count: {b}
info_count: {c}
---
```

### 🪔 메모리 갱신 (Journal Update v2.5)

- lint 자체는 journal을 수정하지 않습니다.
- 사용자 동의 후 자동 수정이 실행된 경우에만 읽고-병합-쓰기로 반영합니다.
- 수정 후 `last_updated` 갱신.
- archive 이동도 사용자 명시 동의 후 실행.

### 📣 안내

응답 마지막에 다음을 브리핑합니다:
- 저장 경로
- 위반 요약 (critical/warn/info 건수)
- 사용자 입력 옵션 안내
