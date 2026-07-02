# 📂 outputs/sermons/ — 본문 중심 사역 자산 트리

본 디렉토리는 `Pastor-KR v2.5`의 **본문 중심 lineage** 저장소입니다.
하나의 성경 본문에 대해 진행된 모든 사역 자산(브레인스토밍 → 주해 → 변증 → 레드팀 → 발행물)이 한 폴더에 누적됩니다.

> 🚨 **PII 주의 (v2.12)**: `outputs/` 산출물(특히 주보·서신·심방 자료)에는 성도 실명이 불가피하게 포함될 수 있습니다. 그래서 `outputs/`는 기본적으로 `.gitignore` 대상입니다 — **공개 저장소(포크 포함)에 커밋하지 마십시오.** 사역 자산을 git으로 백업하려면 반드시 private 저장소에서만 ignore 규칙을 해제하십시오.

---

## 1. 디렉토리 구조

```
outputs/sermons/
├── {passage_id}/
│   ├── _manifest.md              # 본문의 lineage 요약 + 진행 상태
│   ├── v01_sermon-brainstorming_{date}.md
│   ├── v02_sermon-research_{date}.md
│   ├── v03_biblical-dilemma-solver_{date}.md
│   ├── v04_sermon-red-team_{date}.md
│   ├── v05_small-group-guide_{date}.md
│   ├── v06_sermon-to-blog_{date}.md
│   ├── v07_sermon-cardnews-maker_{date}.md
│   └── ...
└── ...
```

---

## 2. `passage_id` 명명 규칙

`{book-slug}-{chapter}-{verse_start}-{verse_end}` (lowercase, hyphen-separated)

| 본문 | passage_id |
|---|---|
| 마가복음 5:25-34 | `mark-5-25-34` |
| 빌립보서 2:5-11 | `philippians-2-5-11` |
| 시편 23편 전체 | `psalms-23` (절 생략 가능) |
| 에베소서 2:11-22 | `eph-2-11-22` 또는 `ephesians-2-11-22` |
| 창세기 1:1-2:3 | `genesis-1-1__2-3` (장 경계 시 더블 언더스코어) |

### 책 약어 권장 표기
- 단일 단어 책: `psalms`, `john`, `revelation` 등 풀네임 lowercase
- 다단어/긴 책: `1-corinthians`, `2-thessalonians`, `1-john` 등 하이픈 결합
- 약어 허용: `eph`, `phil`, `rom`, `gal`, `col`, `mt`, `mk`, `lk`, `jn` (단, 폴더 생성 시 *동일 본문 두 폴더 충돌* 주의 — 사용자가 한 표기로 통일)

> 충돌이 의심되면 Concierge가 사용자에게 한 번 확인합니다.

---

## 3. 버전 번호 규칙

`v{NN}_{skill}_{date}.md` — `NN`은 해당 폴더의 누적 작업 순서.

- 같은 스킬을 두 번 실행해도 새 버전 번호 부여 (덮어쓰기 금지).
- 폴더에 작업이 처음 시작되는 본문은 `v01`부터 시작.
- 날짜는 `YYYY-MM-DD` 형식.

---

## 4. `_manifest.md` 구조

각 본문 폴더 최상단에 위치하는 lineage 요약 파일. 각 스킬 실행 시 읽고-병합-쓰기로 갱신됩니다.

### 4.1 표준 템플릿

```markdown
---
passage_id: mark-5-25-34
title: "혈루증 여인의 손길"
created: 2026-05-06
last_updated: 2026-05-10
current_stage: redteam
preached_on: null
series_id: null
---

# 📜 마가복음 5:25-34 — 혈루증 여인의 손길

## 핵심 요약
- **Big Idea:** 사회적 수치를 뚫고 다가온 개인적 믿음, 그 손길의 거룩함
- **신학 명제:** 예수의 능력은 군중 속에서도 한 사람의 정직한 접촉을 식별한다
- **한국적 적용:** 익명의 군중 속에서도 한 영혼을 호명하시는 목양

## Lineage (자동 누적)
- v01 sermon-brainstorming (2026-05-06) — Big Idea: 사회적 수치 vs 개인적 믿음 긴장
- v02 sermon-research (2026-05-10) — 핵심 강조: αψασθαι(만지다)의 분사적 강세, 12년의 만성성
- v03 biblical-dilemma-solver (2026-05-10) — 난제 해결: 군중 노출 의도(공적 증언 vs 사회적 회복)
- v04 sermon-red-team (2026-05-10) — 핵심 지적: 비-건강자 회중 정서 배려 부족
```

### 4.2 작성 정책

- **Lineage 라인 형식:** `- v{NN} {skill} ({date}) — {1줄 요약}`
- 한 줄 요약은 해당 작업의 *고유한 발견*만 기록 (모든 스킬이 적용한 일반 정보는 생략).
- `current_stage`는 가장 최근 작업의 stage 값으로 갱신.
- `preached_on`은 사용자가 명시적으로 알려줄 때만 채움 (자동 추론 금지).

---

## 5. 시리즈 본문 연동

본문이 시리즈(`active_series`)에 속하는 경우 manifest 프론트매터에 `series_id`를 채웁니다. `outputs/series/{series_id}/_manifest.md`와 양방향 참조됩니다.

```markdown
series_id: ephesians-2026-spring
series_position: 4 of 6
```

---

## 6. Archive 정책

- `preached_on`이 채워지고 `last_updated`로부터 **6개월 경과** 시 아카이브 후보.
- 아카이브는 **삭제가 아니다.** 사용자가 명시적으로 정리를 요청하기 전에는 폴더를 그대로 둡니다.
- 정리 요청 시 `outputs/_archive/sermons/{year}/` 하위로 폴더째 이동.

---

## 7. 백워드 호환성

v2.1 시절 `outputs/{date}/01_sermon_core/...` 구조로 저장된 자료는 그대로 둡니다. 마이그레이션은 사용자가 원할 때만 수동으로 진행하며, AI는 강제로 이동하지 않습니다.
