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
1. **본문 식별**: `passage_id` = `{book-slug}-{ch}-{vstart}-{vend}` (예: 마가 5:25-34 → `mark-5-25-34`). 장 전체를 아우르는 묵상이라 절 범위가 불명확하면 `{book-slug}-{ch}`로 축약할 수 있다(예: `leviticus-4`·`amos-1` — 발아 코퍼스의 장 단위 큐티 관례). 모호하면 사용자에게 확인, 본문이 없으면 `topic-{slug}` 폴백.
2. **버전 번호**: 대상 폴더를 스캔하여 다음 `v{NN}` 결정.
3. **YAML 메타데이터**: `date`, `skill`, `category`, `passage_id`(해당 시), `version`, `topic`, `stage` + 스킬별 `extra` 필드.
   - *(v2.15, 선택)* `seed_refs`: 뿌리 큐티/씨앗의 **레포 상대 경로 리스트** (절대 경로 금지). 기록 주체 — `qt-germinate-seed`(수집한 큐티 전체 자동) · `qt-to-column`(사용한 큐티/씨앗). 이후 lineage 단계(brainstorming·outline 등)는 AGENT 모드에서 같은 lineage 폴더에 씨앗 파일이 있으면 그 `seed_refs`를 상속하고, 붙여넣기만 받은 CHAT 모드에서는 생략한다(모르는 출처를 지어내지 않는다). 소비처 — 씨앗 거울(`sermon-outline-codraft` 4.5단계)·`sermon_audit` Claim Ledger ⑤(일화 대조)·가계도(v2.17 예정).
4. **Manifest 갱신**: `_manifest.md`를 **읽고-병합-쓰기** (없으면 신규 생성). 라인 형식: `- v{NN} {skill} ({date}) — {스킬별 manifest_line}`.
5. **칼럼 인덱스 (v2.17):** 칼럼 스킬(`sermon-to-column`·`qt-to-column`)의 저장 시 `outputs/columns/_index.md`에 한 줄 append — `- {date} · {주제} · {문체} · {지면 또는 "-"} · {파일 경로}` (없으면 생성). 저장 위치 자체는 불변(lineage)이며 인덱스만 추가 — `weekly-briefing`·`recall`(5차·가계도)의 칼럼 축 소스.
6. **설교 인덱스 (v2.18):** `save: sermons-lineage` 저장마다 `outputs/sermons/_index.md`에 한 줄 append — `- {date} · {passage_id} · v{NN} {skill} · {stage} · {키워드 1~2개} · {파일 경로}` (없으면 생성). devotionals `_index.md`(qt-log)·columns `_index.md`(§2.5)와 대칭 — 설교 축만 인덱스가 없어 코퍼스가 커지면 `recall`·`weekly-briefing`이 전 `_manifest.md`를 전수 스캔해야 했던 공백을 메운다. 소비처: `recall`(주제·시기 질의 1차 소스)·`weekly-briefing`(설교 축 집계)·가계도. 새 파일 저장 없이 stage만 바뀐 경우에는 append하지 않는다(라인 = 파일 1개).

## §3. 메모리 갱신 (Journal Update)

`core/pastor_journal.md`를 **읽고-병합-쓰기**로 갱신합니다. 절대 통째로 덮어쓰지 않습니다.

1. 스킬의 `journal` 파라미터에 따라 `active_sermons` / `active_series` / `active_visitations` 항목을 갱신 또는 추가 (`stage`, `next_step`, `notes` 한 줄). 시리즈 항목을 갱신할 때는 `active_series.last_updated`도 함께 갱신합니다 (정체 감지용).
2. `recent_topics`에 핵심 키워드 1~2개 FIFO 추가 (12개 한도, 중복 제거).
3. `last_updated` 갱신.
4. **PII 정책 엄수** (`pastor_journal.md` §2): 실명 → 직분+이니셜 변환, 연락처·병명 상세·재정 기록 금지. 사용자가 실명을 입력해도 변환 후 저장.
5. `journal: 갱신하지 않음`으로 선언된 스킬(읽기 전용 도구)은 이 단계를 건너뜁니다.
5.5 **큐티 리듬 (v2.20):** `save: qt-log` 스킬(`qt-companion`)의 저장 시 frontmatter `last_qt_date`를 오늘 날짜로 갱신합니다 — **이 필드는 qt-companion만 만집니다**(`pastor_journal.md` §3.8). 날짜만 기록하며 묵상 내용은 journal에 남기지 않습니다.
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

1. AGENT 모드: `tools/exegete/pastor_adapter.py`가 있으면 먼저 호출하여 `data/scripture/`의 요청 역본을 조회합니다. 호출 예시는 `python3 tools/exegete/pastor_adapter.py "요3:16" --kind passage --edition "개역개정"`입니다. `--edition`은 `core/foundation.md`의 `preferred_bible`과 일치시킵니다.
2. 어댑터의 `status`와 `capabilities.passage`가 `ok`인 경우에만 그 결과를 본문 팩으로 사용합니다. `partial`, `unavailable`, `invalid_request`, `error`는 성공으로 취급하지 않으며, `warnings`, `missing_verses`, `sources`의 해시·역본·레코드 키를 연구 기록에 남깁니다.
3. **역본 자동 대체 금지:** 요청한 역본이 없을 때 개역개정 → 개역한글 → WEB처럼 조용히 바꾸지 않습니다. 다른 역본은 사용자가 명시적으로 선택했을 때만 조회하고 결과에 실제 역본명과 `edition_id`를 표시합니다.
4. 어댑터가 없거나 본문 팩을 확보하지 못하면 먼저 기존 `data/scripture/`의 책별 슬롯을 직접 확인합니다. 거기에도 요청 역본의 전문이 없으면(또는 CHAT 모드) 사용자에게 **본문 전문 붙여넣기를 요청**하고 기다립니다. 세션 내 동일 본문 재요청은 하지 않습니다. CHAT 모드에서 CLI를 실행했거나 저장했다고 보고하지 않습니다.
5. 🚨 **기억으로부터의 성경 인용 금지:** 확보된 본문 팩이 유일한 인용 원천입니다. 이후 모든 직접 인용·절 번호는 본문 팩과 대조하고, 대조 불가 인용은 "(검증 불가)"를 명시합니다.
6. 확보된 본문은 결과물 머리에 게재하여 독자(목회자)도 같은 정본을 보게 합니다. 어댑터 JSON은 증거 입력이며 `pastor_journal.md`, `_manifest.md`, `stage`를 직접 쓰지 않습니다.

### §6.1 선택적 원어 증거 조회

1. `sermon-research`와 `sermon_audit`은 본문 조회와 별도로 같은 어댑터를 `--kind original` 또는 `--kind all`로 호출할 수 있습니다. 구약 요청은 히브리어, 신약 요청은 헬라어 결과를 받으며 두 언어의 가용성을 섞지 않습니다.
2. `capabilities.original_text`와 `capabilities.morphology`가 `available: true`일 때만 원문·원시 형태소 태그를 관찰 자료로 옮깁니다. `lexicon`, `louw_nida`, `discourse`, `lxx`는 각 capability가 따로 `available`일 때만 사용합니다.
3. 원어 결과에는 데이터셋·판본·revision·license·로컬 상대 경로·SHA-256·레코드 키가 있어야 합니다. 원자료가 부분적이면 해당 절과 토큰을 누락시키지 말고 `partial`과 결손 경고를 표시합니다.
4. 형태소 관찰은 어휘상·상·담화 기능·번역·신학적 해석과 동일하지 않습니다. 어댑터가 제공하지 않는 셀은 "자료 없음/확인 필요"로 두고 기억으로 보완하지 않습니다.
5. 원어 데이터 설치·다운로드는 조회 중 자동 실행하지 않습니다. 설치가 필요하면 `tools/exegete/VENDOR.md`와 `data/_README.md`의 로컬 데이터 절차를 따르고, 사용자 원본과 파생 캐시를 분리합니다.

## §7. 목양 안전 게이트 (Care-Safety Gate) — 목양·서신 스킬 공통

성도의 상황(심방·위로·묵상·서신)을 다루는 스킬은 콘텐츠 생성 **전에** `core/care_safety.md`를 로드하고 위기 신호 스크리닝을 수행합니다. 위기 신호 감지 시 콘텐츠 생성보다 전문 연계 안내가 먼저입니다.

## §8. 입양·원고 등록 (Adopt & Register-Draft) — v2.17

시스템 **밖**에서 태어난 산출물(종이에 쓴 개요, 챗에서 쓴 칼럼, 과거 설교 원고)을 lineage에 소급 편입하는 절차 — 어느 단계든 정문이 됩니다(독립 진행의 양방향 문).

1. **대상·출처 확인:** 무엇이며 언제 만들어졌는지 1회 확인. **내용은 수정하지 않는다** — 입양은 보관이지 개작이 아니다.
2. **passage_id 판정:** §2 규약. 본문 없으면 `topic-{slug}`.
3. **YAML 소급 부여:** `date`(원 작성일 — 모르면 입양일 + `adopted_date_unknown: true`), `skill: adopted`, `stage`(내용에 맞는 값 — 목회자와 확인), `adopted: true`.
4. **버전 번호:** 대상 폴더 스캔 후 다음 `v{NN}`.
5. **Manifest:** `- v{NN} (입양) {설명} ({원 작성일})` — 읽고-병합-쓰기.
6. **Journal:** 선포 여부를 **확인한 후에만** 반영 — 선포됨: `preached_on` 채움 / 미선포: stage만 갱신. 확인 없이 등재하지 않는다. PII 정책 동일 적용.

**register-draft (특수형):** 목회자가 직접 쓴 설교 초안·최종 원고의 등록 — `stage: drafted`(선포된 원고면 `preached`). 이로써 `drafted` 단계가 실체를 갖고, `sermon_audit`·`sermon-retro`·재생산 스킬·주간 세트(심화)가 **실제 원고를 참조**할 수 있게 됩니다. 대필 거절 원칙과 무관합니다 — AI는 원고를 쓰지 않고 보관만 합니다.

## §9. 상류 자동 참조 (Upstream Auto-Reference) — v2.18

lineage 하류 스킬(주해·난제·개요·red-team 등)이 상류 산출물을 매번 "복사해 붙여넣어" 받던 인수인계를 AGENT 모드에서 자동화합니다. 씨앗 거울(`sermon-outline-codraft` 4.5단계)·red-team의 SSOT 로드와 **동형 패턴**의 일반화입니다.

1. **AGENT 모드:** 스킬 실행 시작 시 같은 `outputs/sermons/{passage_id}/` 폴더의 `_manifest.md`를 읽고, 자신의 직전 단계 산출물(해당 skill의 최신 `v{NN}`)을 자동 로드한다. 로드 후 1줄 브리핑: `📎 v{NN} {skill}({date})를 참조합니다.` 목회자가 다른 버전·다른 파일을 지정하면 그것이 우선한다.
2. **씨앗 파일 특례:** `qt-germinate-seed` 산출물을 참조할 때는 `## 접합 블록 (브레인스토밍 입력)` 섹션만 컨텍스트에 올린다 (대화 프로토콜 원문 제외).
3. **폴더에 상류 산출물이 없으면:** 없다고 정직하게 말하고 붙여넣기를 요청한다. 있는 척 진행하거나 기억으로 채우지 않는다.
4. **CHAT 모드:** 현행대로 사용자에게 상류 산출물 붙여넣기를 요청한다.
5. **경계:** 자동 참조는 **읽기**만이다. 상류 파일을 수정하지 않으며, 상류의 `stage`를 되돌리지 않는다(§3.6 원리).

---

## 부록. 본문 기반 스킬 실행 체크리스트 (Hook Conformance Checklist) — v2.20

§가 늘면서 실행자가 절차를 누락하기 쉬워졌다. 본문 기반 스킬(`save: sermons-lineage`/`qt-log`/`devotional-fallback`)을 실행할 때 아래 **실행 순서**대로 점검한다 — 각 행의 조건에 해당할 때만.

| 순서 | 절차 | 조건 (해당 스킬) | 누락 시 증상 |
|---|---|---|---|
| 1 | §1 모드 판별 | 모든 스킬 (1회) | CHAT에서 "자동 저장됨" 거짓 보고 |
| 2 | §9 상류 자동 참조 | lineage 하류 스킬 (AGENT) | 매번 붙여넣기 요구, 맥락 유실 |
| 3 | §6 본문 팩 확보 | 성경 본문을 다루는 스킬 | 기억 인용 → 환각 절 번호 |
| 4 | §7 안전 게이트 | 성도 상황을 다루는 스킬 | 위기 신호 놓침, 금기 언어 |
| 5 | (스킬 본연의 작업) | — | — |
| 6 | §2 저장 + 인덱스 append | 모든 저장 스킬 — `sermons-lineage`는 §2.6, 칼럼은 §2.5, `qt-log`는 devotionals 인덱스 | 인덱스 누락 → recall·briefing 집계 구멍 |
| 7 | §3 journal 갱신 (+§3.6 가드, `qt-log`는 §3 5.5 `last_qt_date`) | `journal: 갱신하지 않음` 제외 전부 | stage 오염·조기 published·리듬 감지 실패 |
| 8 | §4 완료 브리핑 (CHAT이면 §5 폴백) | 모든 스킬 | 저장 경로 미보고 |

읽기 전용 도구(recall·scan·briefing 등)는 1번과 8번만 해당한다. 입양(§8)은 별도 정문 절차다.
