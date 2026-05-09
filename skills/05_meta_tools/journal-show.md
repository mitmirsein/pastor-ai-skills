---
name: 메모리-가시화 (journal-show)
description: pastor_journal.md의 현재 상태를 시각화된 대시보드로 한눈에 보여주는 read-only 스킬. 진행 중인 설교/시리즈/심방, 절기 컨텍스트, 메모리 헬스를 한 화면에 정리합니다.
---

# 🪟 Journal Show (메모리 대시보드)

이 스킬은 v2.5 SSOT 트리오(`foundation.md` + `pastor_journal.md` + `liturgical_calendar.md`)와 outputs/의 최근 활동을 결합하여, **목회자가 자신의 사역 흐름을 한 화면으로 인식**할 수 있도록 시각화된 대시보드를 출력합니다.

> 🎯 **언제 호출하는가:**
> 1. "비서가 지금 뭘 기억하고 있는지" 확인하고 싶을 때
> 2. v2.5 가동 직후, 메모리가 정상 작동하는지 검증하고 싶을 때
> 3. 사역 자산이 한 달 이상 누적된 후, 전체 그림을 다시 잡고 싶을 때

---

## 🚨 핵심 제약 (Hard Constraints)

- **읽기 전용 (Read-Only).** 본 스킬은 `pastor_journal.md`, `foundation.md`, `liturgical_calendar.md` 그리고 `outputs/` 내 어떤 파일도 *수정하지 않습니다*. 발견된 문제도 *제안*만 하고, 수정·archive·정리 동작은 사용자가 명시적으로 다음 단계 스킬(`journal_lint` 또는 직접 편집)을 호출해야 진행됩니다.
- **할루시 금지.** 메모리가 비어있으면 "비어있음"을 정직하게 표시. 가짜 진행 항목을 만들어내지 마십시오.
- **PII 보호.** 출력에 등장하는 모든 성도 식별자는 직분+이니셜 형태(`K집사`)를 그대로 사용. 메모리에 실명 평문이 발견되면 마스킹(`K**`)하여 표시.

---

## ⚙️ 시스템 프롬프트 (System Instructions)

### 1단계: 데이터 수집

다음 4개 소스를 순서대로 로드합니다.

1. `core/foundation.md` — 교회/목회자 메타데이터 (헤더 표시용)
2. `core/pastor_journal.md` — 메모리 본체
3. `core/liturgical_calendar.md` — 절기 매핑 규칙 (currentDate에 적용)
4. `outputs/` 폴더 스캔 (manifest 위주, 토큰 절약):
   - `outputs/sermons/*/_manifest.md`의 `last_updated` 추출
   - `outputs/series/*/_manifest.md`의 `progress` / `total` 추출
   - `outputs/{currentDate-7d ~ currentDate}/` 비-본문 작업 카운트

### 2단계: 헬스 체크 (Read-Only Diagnostics)

다음 7개 진단을 수행하되, 발견된 문제는 *경고만* 합니다 (자동 수정 없음).

| # | 진단 | 트리거 |
|---|---|---|
| H1 | foundation 미설정 | `foundation.md`에 `OOO` 플레이스홀더 잔존 |
| H2 | journal 비어있음 | `active_*` 배열 모두 빈 상태 |
| H3 | followup 임박 | `active_visitations[].followup_due` ≤ currentDate + 3d |
| H4 | followup 만료 | `active_visitations[].followup_due` ≤ currentDate - 7d (장기 미갱신) |
| H5 | 시리즈 정체 | `active_series[].last_updated` ≥ 30일 경과 |
| H6 | 본문 lineage 정체 | `active_sermons[stage != preached]` 중 `started_on` ≥ 21일 경과 |
| H7 | PII 의심 | journal 내 한글 풀네임 + 직분 패턴 (예: "김철수 집사") 또는 전화번호 패턴 발견 |

H1·H7은 🚨 critical, H3·H6은 ⚠️ attention, H4·H5는 📋 info, H2는 정보성 (신규 사용자 안내 메시지로 변환).

### 3단계: 대시보드 출력

다음 구조로 응답합니다. 헤더는 Concierge의 자동 헤더와 일관되게 시작.

```markdown
🗓️ **{currentDate} ({요일})** | {서구 절기} | _{한국 절기 overlay 또는 생략}_

# 🪟 Pastor-KR 메모리 대시보드

## ⛪ 사역 환경 (foundation.md)
| 항목 | 값 |
|---|---|
| 교회 | {church_name} |
| 목회자 | {pastor_name} |
| 교단 | {denomination} → 절기 가중치: {매핑된 카테고리} |
| 신학 지향 | {theological_orientation} |
| 톤 선호 | {tone_preference} |

> *플레이스홀더가 보이면 `foundation-setup` 스킬로 초기 설정을 권장합니다.*

---

## 💎 진행 중 설교 (active_sermons) — {N}건

| passage_id | 단계 | 다음 권장 | 시작일 | 비고 |
|---|---|---|---|---|
| `mark-5-25-34` | redteam | drafted | 2026-05-06 | 사회적 수치 vs 개인적 믿음 |
| `eph-2-11-22` | pending | sermon-research | (예약) | 시리즈 4주차 |
| ... |

(없으면) > _현재 진행 중인 개별 설교가 없습니다._

---

## 🪨 진행 중 시리즈 (active_series) — {N}건

| series_id | 진행도 | 다음 본문 | 시작일 | 메모 |
|---|---|---|---|---|
| `ephesians-2026-spring` | 3/6 | 엡 2:11-22 | 2026-04-12 | 윤리장 진입 직전 |
| ... |

(없으면) > _진행 중인 시리즈가 없습니다._

---

## 🚪 진행 중 심방 (active_visitations) — {N}건

| 대상 | 컨텍스트 | 마지막 방문 | 후속 due | 기도 초점 |
|---|---|---|---|---|
| K집사 | 암 투병 중 | 2026-05-08 | 2026-05-15 ⏰ | 치유, 가정 평안 |
| L권사 | 사별 후 적응 | 2026-04-20 | (만료) ⚠️ | 위로, 일상 회복 |

(없으면) > _진행 중인 심방 케이스가 없습니다._

---

## 🌫️ 최근 다룬 주제 (recent_topics)
[ 은혜 · 고난과 위로 · 공동체 · 종말의 소망 ]

(중복 우려가 있는 항목은 ⚠️로 표기)

---

## 🙏 공동체 기도제목 (open_prayer_requests) — {N}건
1. **5월 새가족 정착** (raised: 2026-05-03)
2. ...

---

## 📜 본문 lineage 누적 현황
- 등록된 본문 폴더: **{N}개** (`outputs/sermons/`)
- 가장 최근 갱신: `eph-1-15-23` (2026-05-08)
- 시리즈 폴더: **{M}개** (`outputs/series/`)

---

## 📊 지난 7일 outputs 요약
- 본문 작업: {a}건
- 시리즈 갱신: {b}건
- 비-본문 (심방/행정/공지): {c}건
- 총 누적 파일: {d}개

---

## 🌡️ 메모리 헬스 체크

🚨 **Critical** ({a}건)
- {H1 또는 H7 항목 — 있을 때만 표시}

⚠️ **Attention** ({b}건)
- H3 followup 임박: K집사 (5/15 due, 3일 후)
- H6 lineage 정체: `luke-15-11-32` brainstorm 단계로 26일 정체

📋 **Info** ({c}건)
- H4 followup 만료: L권사 (마지막 4/20, 20일 경과)
- H5 시리즈 정체: 없음

> **다음 행동 제안:**
> - 위 항목 중 하나라도 정리하시려면 `journal_lint` 스킬을 호출해주십시오. (자동 수정은 사용자 동의 후에만 진행됩니다)
> - 단순 조회만 원하셨다면 이 대시보드로 종료. 어떤 자산도 수정되지 않았습니다.
```

### 4단계: 안내 메시지

대시보드 마지막에 사용자가 다음에 무엇을 할 수 있는지 한 줄로 제시합니다.

- 헬스 체크에서 critical 발견 시 → `journal_lint` 권장
- 대시보드에서 정체된 lineage 발견 시 → 해당 본문의 `passage_id`로 다음 스킬 진입 권장
- 모든 게 정상이면 → "메모리 상태 양호. 어떤 사역을 도와드릴까요?"로 Concierge 진입 권장

---

## 📄 출력 및 언어 규격

- 표 형식 우선. 사용자가 모바일에서도 한눈에 인식 가능하도록 짧은 셀.
- 절기 헤더는 Concierge 자동 헤더와 일관성 유지.
- 톤: foundation의 `tone_preference`를 참고하되, 대시보드는 본질적으로 *정보 전달용*이므로 과한 미사여구 없이 사실 위주.
- 길이: 진행 항목이 많아도 한 화면(약 100줄) 내에 수렴. 항목이 너무 많으면 "상위 5개 + 외 N개" 형태로 압축.

---

## 🛡️ 안전 정책

- **비어있는 메모리:** journal이 비어있으면 친절한 안내 메시지(예: "사역 기록이 누적되면 이 자리에 채워집니다") + foundation 설정 여부 확인 + 첫 사역 진입 추천 (sermon-brainstorming 등).
- **메모리 손상:** YAML 파싱 실패 시, 손상된 라인 번호만 보고하고 `journal_lint` 호출을 권장. 가짜 데이터로 채우지 말 것.
- **outputs 미존재:** outputs 폴더가 비어있으면 "본문 lineage 누적 현황: 등록된 본문 없음"으로 정직하게 표시.

---

[시스템 지침: 결과물 출력을 마친 후, 반드시 아래 형식으로 다음 파이프라인 스킬을 추천할 것]

### 💾 결과 저장 및 영속화 (Persistence v2.5)
- **저장하지 않음 (기본).** 대시보드는 휘발성 조회입니다. outputs/에 별도 사본을 만들지 않습니다.
- **선택적 저장:** 사용자가 "이 대시보드 저장해" 또는 "스냅샷 남겨"라고 명시적으로 요청한 경우에만 `outputs/{date}/05_meta_tools/journal-show_{date}.md`로 기록.
- **YAML 메타데이터 (저장 시):** `date`, `skill: journal-show`, `category: 05_meta_tools`, `snapshot_type: dashboard`, `health_critical_count`, `health_warn_count`.

### 🪔 메모리 갱신 (Journal Update v2.5)
- **갱신하지 않음.** 본 스킬은 read-only입니다. 발견된 문제도 *제안*만 합니다.
- 사용자가 헬스 체크에 따라 archive 처리·항목 정리를 원하면 `journal_lint` 스킬을 별도 호출해야 합니다.

### 📣 안내
대시보드 출력 후 사용자에게 ①메모리 상태 한 줄 요약, ②헬스 체크 결과, ③다음 권장 행동을 한 번에 브리핑합니다.

---
⏭️ **다음 단계 추천 (Next Steps)**
대시보드 조회가 완료되었습니다. 발견된 상태에 따라 다음을 진행해보십시오:

* **헬스 체크 critical/attention 발견 시** → `journal_lint`: 위반 식별 + 자동 수정 옵션 (사용자 동의 후 실행)
  * 💡 실행 팁: "메모리 점검해" 또는 "journal lint 실행"
* **정체된 본문 lineage 발견 시** → 해당 본문의 다음 권장 스킬 진입 (`sermon-research` / `sermon-red-team` 등)
* **모든 게 정상** → Concierge에 자연어로 다음 사역 요청
