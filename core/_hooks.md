# 🧷 표준 훅 (Standard Hooks) — 단일 정의

> 모든 전문 스킬의 결과 저장·메모리 갱신·환경 폴백 **절차**는 이 파일이 단일 진실 공급원입니다 (v2.8 P3-10).
> 각 스킬 하단의 `### 🧷 표준 훅` 블록은 *파라미터*만 선언하고, 절차는 본 파일을 따릅니다.
> 절차를 고칠 일이 생기면 **이 파일만** 고치십시오. 스킬마다 복붙된 절차는 표류(drift)합니다.

---

## §1. 모드 판별 (AGENT / CHAT) — 침묵 실패 금지

스킬 실행 시작 시(또는 Concierge 부트 시) 환경을 1회 판별합니다.

- **AGENT 모드**: 파일을 읽고 쓸 수 있는 환경 (Claude Code, Cursor, Antigravity 등). §2~§4를 직접 수행.
- **CHAT 모드**: 파일 접근이 없는 환경 (웹 챗 등). §2~§4 대신 **§5 폴백**을 수행.

판별법: `core/foundation.md`를 읽을 수 있으면 AGENT, 아니면 CHAT.
🚨 **절대 규칙**: CHAT 모드에서 "자동 저장되었습니다"라고 보고하는 것은 거짓 보고입니다. 저장하지 못했으면 못했다고 말하고 §5로 안내합니다.

## §2. 결과 저장 (Persistence)

스킬의 `save` 파라미터에 따라 저장 위치를 결정합니다.

| save | 경로 | 비고 |
|---|---|---|
| `sermons-lineage` | `outputs/sermons/{passage_id}/v{NN}_{skill}_{date}.md` | 본문 중심 lineage |
| `series` | `outputs/series/{series_id}/` | 시리즈 기획 |
| `dated` | `outputs/{date}/{category}/{skill}_{topic}.md` | 비-본문 작업물 |
| `devotional-fallback` | 본문 식별 시 lineage, 아니면 `outputs/devotionals/{topic-slug}/` | 묵상 폴백 |
| `qt-log` | `outputs/devotionals/{passage_id 또는 topic-slug}/v{NN}_{skill}_{date}.md` | 매일 큐티 로그 — 본문이 식별돼도 설교 lineage로 **조기 승격하지 않고** devotionals/에 누적(발아 코퍼스). 설교 lineage로의 승격은 나중에 `qt-germinate-seed`(`sermons-lineage`)가 담당. **인덱스 누적**: 저장 시 `outputs/devotionals/_index.md`에 한 줄 append — `- {date} · {passage_id 또는 topic-slug} · {키워드 1~2개} · {파일 경로}` (없으면 생성; 발아 스캔·주간 브리핑의 1차 스캔 소스 — 코퍼스가 커져도 전수 집계 가능) |

공통 절차:
1. **본문 식별**: `passage_id` = `{book-slug}-{ch}-{vstart}-{vend}` (예: 마가 5:25-34 → `mark-5-25-34`). 모호하면 사용자에게 확인, 본문이 없으면 `topic-{slug}` 폴백.
2. **버전 번호**: 대상 폴더를 스캔하여 다음 `v{NN}` 결정.
3. **YAML 메타데이터**: `date`, `skill`, `category`, `passage_id`(해당 시), `version`, `topic`, `stage` + 스킬별 `extra` 필드.
4. **Manifest 갱신**: `_manifest.md`를 **읽고-병합-쓰기** (없으면 신규 생성). 라인 형식: `- v{NN} {skill} ({date}) — {스킬별 manifest_line}`.

## §3. 메모리 갱신 (Journal Update)

`core/pastor_journal.md`를 **읽고-병합-쓰기**로 갱신합니다. 절대 통째로 덮어쓰지 않습니다.

1. 스킬의 `journal` 파라미터에 따라 `active_sermons` / `active_series` / `active_visitations` 항목을 갱신 또는 추가 (`stage`, `next_step`, `notes` 한 줄). 시리즈 항목을 갱신할 때는 `active_series.last_updated`도 함께 갱신합니다 (정체 감지용).
2. `recent_topics`에 핵심 키워드 1~2개 FIFO 추가 (12개 한도, 중복 제거).
3. `last_updated` 갱신.
4. **PII 정책 엄수** (`pastor_journal.md` §2): 실명 → 직분+이니셜 변환, 연락처·병명 상세·재정 기록 금지. 사용자가 실명을 입력해도 변환 후 저장.
5. `journal: 갱신하지 않음`으로 선언된 스킬(읽기 전용 도구)은 이 단계를 건너뜁니다.
6. **발행 전이 가드 (§3.6) — 파생 발행물 공통**: 재생산 스킬(칼럼·블로그·TTS·카드뉴스)의 journal 갱신은 본체 설교의 진행 단계를 앞당기지 않습니다.
   - 해당 항목의 `preached_on`이 채워져 있을 때만 `stage: published`로 전이합니다.
   - `preached_on`이 비어 있으면(선포 전) **stage를 바꾸지 않고** `notes`에 `[파생 발행: {포맷}] ({date})`만 추가합니다 — 선포 전 재생산(예: 토요일 TTS 낭독 점검, 주중 칼럼 선작성)이 리듬 엔진의 지연 감지를 무력화하지 않게 하기 위함입니다.
   - journal에 없는 본문(외부 원고)이면 선포 여부를 사용자에게 확인한 뒤에만 등재합니다.
   - (근거: `pastor_journal.md` §3.1.1 — 파생 작업은 본체 stage를 후퇴시키지도, 전진시키지도 않는다)

## §4. 완료 브리핑

저장 완료 후 사용자에게 한 번에 보고합니다: ① 저장된 경로 ② manifest 갱신 결과 ③ journal 갱신 항목 ④ (있다면) 다음 단계 추천.

## §5. CHAT 모드 폴백 — "저장 대신 건네드립니다"

파일을 쓸 수 없는 환경에서는 §2~§3 대신:

1. 결과물 머리에 §2의 YAML 메타데이터를 붙인 **저장용 완성 블록**을 코드 블록으로 출력하고, 안내합니다:
   > 📋 이 환경에서는 자동 저장이 불가능합니다. 아래 블록을 복사해 `outputs/{권장 경로}`에 직접 저장하십시오.
2. journal 갱신분은 **"journal에 추가할 항목"** 코드 블록으로 별도 출력합니다 (사용자가 `core/pastor_journal.md`에 붙여넣을 YAML 조각).
3. PII 정책은 동일하게 적용합니다 — 출력 블록에도 실명을 남기지 않습니다.

## §6. 본문 팩 우선 (Passage-Pack First) — 설교·목양 스킬 공통

성경 본문을 다루는 스킬(`save: sermons-lineage` 또는 본문 기반 묵상)은 **분석 시작 전에 본문 전문을 확보**합니다.

1. AGENT 모드: `data/scripture/`에서 해당 본문 조회 (슬롯 규약: `data/_README.md`).
2. 없으면(또는 CHAT 모드): 사용자에게 **본문 전문 붙여넣기를 요청**하고 기다립니다. 세션 내 동일 본문 재요청은 하지 않습니다.
3. 🚨 **기억으로부터의 성경 인용 금지**: 확보된 본문 팩이 유일한 인용 원천입니다. 이후 모든 직접 인용·절 번호는 본문 팩과 대조하고, 대조 불가 인용은 "(검증 불가)"를 명시합니다.
4. 확보된 본문은 결과물 머리에 게재하여 독자(목회자)도 같은 정본을 보게 합니다.

## §7. 목양 안전 게이트 (Care-Safety Gate) — 목양·서신 스킬 공통

성도의 상황(심방·위로·묵상·서신)을 다루는 스킬은 콘텐츠 생성 **전에** `core/care_safety.md`를 로드하고 위기 신호 스크리닝을 수행합니다. 위기 신호 감지 시 콘텐츠 생성보다 전문 연계 안내가 먼저입니다.
