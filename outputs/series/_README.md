# 📂 outputs/series/ — 시리즈 사역 자산 트리

> 🚨 **PII 주의 (v2.12)**: `outputs/`는 기본 `.gitignore` 대상입니다 — 산출물에 성도 정보가 담길 수 있으므로 공개 저장소(포크 포함)에 커밋하지 마십시오 (`outputs/sermons/_README.md` 상단 참조).

본 디렉토리는 `Pastor-KR v2.5`의 **시리즈 단위 lineage** 저장소입니다.
강해 시리즈, 절기 시리즈, 주제 시리즈의 기획안과 진행 manifest가 보관됩니다. 시리즈에 속한 개별 주차 본문 자체는 `outputs/sermons/{passage_id}/` 트리에 저장되며, 본 디렉토리는 그것들을 묶는 *상위 인덱스*로 작동합니다.

---

## 1. 디렉토리 구조

```
outputs/series/
├── {series_id}/
│   ├── _manifest.md              # 시리즈 개요 + 주차 진행 표
│   └── plan_{date}.md            # 시리즈 기획안 (sermon-series-planner 결과물)
└── ...
```

---

## 2. `series_id` 명명 규칙

다음 두 형식 중 하나를 선택합니다.

| 형식 | 예시 | 사용 시점 |
|---|---|---|
| `{book-slug}-{year}-{season}` | `ephesians-2026-spring` | 책별 강해 시리즈 |
| `{theme-slug}-{year}-{season}` | `lords-prayer-2026-fall`, `psalms-of-ascent-2027-summer` | 주제 또는 본문군 시리즈 |

`season` 권장값: `spring | summer | fall | winter`. 절기 시리즈(예: 사순절)는 `lent-2026`처럼 절기명만 사용해도 무방.

---

## 3. `_manifest.md` 구조

각 시리즈 폴더 최상단의 manifest. `sermon-series-planner` 실행 시 생성되며, 매 주차 작업이 진행될 때마다 갱신됩니다.

### 3.1 표준 템플릿

```markdown
---
series_id: ephesians-2026-spring
title: "그리스도 안에서: 에베소서 강해"
total: 6
progress: 3
started_on: 2026-04-12
last_updated: 2026-05-10  # 주차 작업이 반영될 때마다 갱신 — weekly-briefing 기간 필터·§5 Archive 정책의 기준 필드
target_end: 2026-05-24
status: in_progress       # in_progress | paused | completed | archived
---

# 🪨 그리스도 안에서: 에베소서 강해

## 시리즈 컨셉
구원의 신학(1-3장) → 윤리적 성숙(4-6장)의 흐름을 6주에 걸쳐 추적.
한국 교회 성도들의 *교리적 무장 빈곤* 문제 의식에서 출발.

## 주차별 본문 및 진행 표

| 주차 | 일자 | 본문 | passage_id | 상태 | 메모 |
|---|---|---|---|---|---|
| 1 | 2026-04-12 | 엡 1:3-14 | `eph-1-3-14` | preached | 영적 축복의 삼위일체적 구조 |
| 2 | 2026-04-19 | 엡 1:15-23 | `eph-1-15-23` | preached | 부르심의 소망 |
| 3 | 2026-05-03 | 엡 2:1-10 | `eph-2-1-10` | preached | 은혜로 받은 구원 |
| 4 | 2026-05-17 | 엡 2:11-22 | `eph-2-11-22` | scheduled | 두 백성이 한 새 사람으로 |
| 5 | 2026-05-24 | 엡 3:1-13 | `eph-3-1-13` | pending |  |
| 6 | 2026-05-31 | 엡 3:14-21 | `eph-3-14-21` | pending |  |

## 핵심 메시지 곡선
1주 (택하심) → 2주 (소망) → 3주 (은혜) → 4주 (화목) → 5주 (계시의 비밀) → 6주 (영광)

## 자료 링크
- 기획안: `plan_2026-04-05.md`
- 주차별 자세한 lineage는 각 `outputs/sermons/{passage_id}/_manifest.md` 참조
```

### 3.2 작성 정책

- 주차별 `상태` 값: `pending | scheduled | drafted | preached | published`
- 주차별 본문이 작업되면 해당 주차 `상태`만 갱신, 다른 행 건드리지 않음.
- `progress`는 `preached` 상태인 주차의 누적 수.
- `status` 자동 전이: 모든 주차가 `preached` 이상이면 `completed`로 갱신.

---

## 4. `pastor_journal.md` 연동

시리즈가 `_manifest.md`에 등록되면 `core/pastor_journal.md`의 `active_series`에도 동시 등록되어야 합니다 (sermon-series-planner의 책임).

- `id == series_id` 일치
- `next_passage` 갱신: 가장 빠른 `pending|scheduled` 주차의 본문 표기
- `progress` 동기화

`status: completed` 또는 `archived` 전이 시 `pastor_journal`의 `active_series`에서 자동 제거 후 archive로 이동.

---

## 5. Archive 정책

- `status: completed` + `last_updated` 6개월 경과 시 아카이브 후보.
- 강제 이동 금지. 사용자 요청 시 `outputs/_archive/series/{year}/`로 폴더째 이동.
