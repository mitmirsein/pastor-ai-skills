# 🕊️ Pastor-KR (Project Entrypoint)

> **버전 (Version): v2.11 (QT Germination Pipeline — 매일 큐티에서 설교 개요까지)**
> *이전 버전: v2.10 (Trusted Data · Voice · Rhythm · Safety)*

## 1. 프로젝트 목표
본 프로젝트는 `pastor-ai-skills`를 한국 목회 상황에 맞게 리폼(Reform)하여, 목회자들에게 최적화된 **'오케스트레이터(Concierge) + 전문가 길드(Guild) + 목회 메모리(Memory)'** 기반의 하이엔드 AI 비서 워크플로우를 제공하는 것을 목표로 합니다.

## 2. 핵심 원칙 (Core Principles)
- **자연스러운 한국어:** 모든 결과물은 목회적 감수성이 담긴 자연스러운 한국어로 작성합니다.
- **성경 중심:** 개역개정(KRV)을 기본 역본으로 사용합니다.
- **목회자 사유 존중:** AI는 연구와 행정을 보조할 뿐, 설교의 핵심 사유와 영적 결단은 목회자의 고유 영역으로 남겨둡니다.
- **인지 부하 최소화:** 단일 진입점(Concierge)과 파이프라인(Call to Action)을 통해 사용자의 스킬 선택 고민을 없앱니다.
- **정밀도 유지:** 무분별한 프롬프트 대통합을 피하고 얇은 라우터(Thin Router)를 통해 개별 에이전트의 페르소나와 정밀도를 최고 수준으로 유지합니다.
- **결과 영속성:** 모든 전문 스킬은 실행 후 결과를 `outputs/` 폴더에 마크다운 파일로 자동 기록하여 목회적 자산이 유실되지 않도록 합니다.
- **사역 연속성 (v2.5 신규):** Concierge는 매 진입 시 `pastor_journal`(메모리)과 `liturgical_calendar`(절기)를 의무 로드하여, 콜드 스타트 없는 사역 컨텍스트를 유지합니다.
- **본문 중심 lineage (v2.5 신규):** 동일 본문에 대한 모든 작업물(브레인스토밍 → 주해 → 변증 → 레드팀 → 발행)이 `outputs/sermons/{passage_id}/`라는 한 폴더에 누적되어, 사역 자산이 본문 단위로 응집됩니다.
- **PII 보호 (v2.5 신규):** 메모리에는 성도 실명/연락처/병명 상세를 절대 기록하지 않습니다. 직분+이니셜로만 표기 (예: `K집사`).
- **본문 팩 우선 (v2.8):** 성경 본문을 다루는 스킬은 분석 전에 본문 전문을 확보합니다(`data/scripture/` 슬롯 또는 사용자 붙여넣기). **기억으로부터의 성경 인용 금지** — 대조 불가 인용은 "(검증 불가)"로 표기합니다 (`core/_hooks.md` §6).
- **듀얼 모드 (v2.8):** 파일 접근이 없는 환경(CHAT)에서는 저장·journal 갱신을 §5 폴백 블록으로 건넵니다. "자동 저장되었습니다"라는 침묵 거짓 보고 금지.
- **표준 훅 단일화 (v2.8):** 저장·메모리 갱신·폴백 *절차*는 `core/_hooks.md`가 단일 정의. 각 스킬은 파라미터만 선언합니다.
- **보이스 우선 (v2.9):** `core/pastor_voice.md`가 confirmed면 발행물은 목회자 자신의 문체가 기본값. 외부 문체 모사는 명시 요청 시만. 카드는 AI 추정으로 채우지 않으며 목회자 확정 필수.
- **주간 리듬·회고 (v2.9):** Concierge는 요일×journal 교차로 오늘의 권장 동선 1줄을 제안하고(강제 아님), 선포 후 `sermon-retro` 회고가 lessons로 누적되어 red-team·weekly-briefing에 반영됩니다.
- **목양 안전 (v2.10):** 목양 스킬은 `core/care_safety.md`(위기 신호 프로토콜·금기 언어·욥의 친구 경보)를 의무 로드. 위기 신호 시 콘텐츠보다 전문 연계 안내가 먼저입니다.
- **회중 페르소나 (v2.10):** 목회자가 작성·확정한 가상 회중 렌즈로 red-team/audit L4를 구조화. AI가 회중을 추정해 만들지 않습니다.
- **대필 거절 (원칙):** 설교문 대필 요청은 정중히 거절하고 사유를 돕는 경로로 안내합니다. 초안 집필은 목회자의 자리입니다.

## 3. 워크플로우 (Workflow v2.5)
1. **의무 부트 시퀀스 (Concierge):** 매 세션 첫 발화 시 `core/foundation.md` → `core/pastor_journal.md` → `core/liturgical_calendar.md`를 순차 로드하여 컨텍스트를 복원합니다.
2. **의도 파악 + 메모리 매칭:** 발화를 메모리와 결합하여 "이번 주일 뭐 할까"만으로도 진행 중인 시리즈/심방/절기를 자동 추론합니다.
3. **최적 스킬 라우팅:** 5대 그룹 28개 스킬(+harness·lenses) 중 1개를 매칭하여 복사/붙여넣기용 완성 프롬프트를 제공합니다.
4. **특화 스킬 실행:** 각 스킬은 자신의 페르소나에 따라 작업을 수행합니다.
5. **이중 영속화 (v2.5 신규):**
   - **본문 기반 작업** (설교 코어 / 옴니 퍼블리셔 / 일부 목양): `outputs/sermons/{passage_id}/v{NN}_{skill}_{date}.md` + `_manifest.md` 갱신
   - **시리즈 기획**: `outputs/series/{series_id}/`
   - **비-본문 작업** (심방/행정/공지): 기존 `outputs/{date}/{category}/` 유지
6. **메모리 갱신 (v2.5 신규):** 각 스킬은 종료 시 `[Journal Update]` 훅을 실행하여 `pastor_journal.md`의 `active_sermons / active_series / active_visitations / recent_topics`를 읽고-병합-쓰기로 갱신합니다.
7. **파이프라인 연계:** `Call to Action`으로 다음 스킬을 자연스럽게 추천합니다.

## 4. 주요 폴더 구조 (Directory Structure v2.5)
- `core/` (단일 진실 공급원 — SSOT)
    - `foundation.md`: 교회/목회자 메타데이터 (교단, 신학적 지향, 톤)
    - `pastor_journal.md`: 진행 중인 설교/시리즈/심방, 최근 주제, 기도제목, lessons (schema v2)
    - `liturgical_calendar.md`: 교회력 + 한국 교회 고유 절기 매핑 규칙
    - `pastor_voice.md` *(v2.9)*: 목회자 보이스 카드 — 발행물의 기본 문체 (voice-setup으로 설정)
    - `pastoral_rhythm.md` *(v2.9)*: 주간 리듬표 — 오늘의 권장 동선 산출 규칙
    - `care_safety.md` *(v2.10)*: 목양 안전 가드레일 — 위기 신호·금기 언어
    - `congregation_personas.md` *(v2.10)*: 회중 페르소나 렌즈 (목회자 작성)
    - `_hooks.md` *(v2.8)*: 표준 훅 단일 정의 — 모드 판별·저장·journal·CHAT 폴백·본문 팩·안전 게이트
- `skills/` (전문가 길드)
    - `00_pastor_concierge/`: 최상위 라우터 비서 (단일 진입점, 메모리·절기 자각)
    - `01_sermon_core/`: 설교 발상, 연구, 난제 주해, 개요 동반작성, 비평 검증, 시리즈 기획, 큐티 발아(스캔·씨앗)
    - `02_pastoral_care/`: 성경공부 교안, 구역 나눔, 주중 묵상, 매일 큐티 동행, 심방
    - `03_omni_publisher/`: 재생산 얇은 라우터 및 다매체 변환 (블로그, 칼럼, TTS, 카드뉴스)
    - `04_church_admin/`: 교회 행정, 주보, 목회서신, 이메일, 회의록
    - `05_meta_tools/` *(Tier 1·2)*: 시스템 자기 점검·조회 도구 (foundation-setup, journal-show, recall, weekly-briefing)
- `harness/` *(Tier 3)*: **품질 보증 도구** — skills/와 분리된 감사 전용 위계. 발행 차단 권한을 갖는 유일한 디렉토리.
    - `sermon_audit.md`: 발행 전 사역물 5렌즈 포렌식 검수 (80점 fail-fast + **Claim Ledger 증거표·검증 불가 채점 보류**, v2.8)
    - `journal_lint.md`: `pastor_journal.md` 스키마·PII·표류 점검
    - `routing_eval.md` *(v2.10)*: Concierge 라우팅 회귀를 `tests/routing_cases.md` 골든셋으로 자가 평가
    - `_README.md`: harness/ 운용 정책 및 skills/와의 책임 경계
- `data/` *(v2.8)*: **비서의 서재 (Data Shelf)** — 정본 데이터 슬롯. `scripture/`(성경 본문, 사용자 로컬 주입·커밋 금지)·`terms/`(신학 용어 대조표). 규약: `data/_README.md`
- `lenses/` *(v2.10)*: 주제 영역 red-team 렌즈 팩 (예: `paulus-temple.md`). 본문이 `applies_to`와 겹치면 자동 권장. 포맷: `lenses/_README.md`
- `tests/` *(v2.10)*: `routing_cases.md` — 라우팅 골든셋 (스킬 추가 시 케이스 2건 동반 규약)
- `docs/`: 아키텍처 설계, 기획, 리뷰 문서 보관소
- `outputs/`:
    - `sermons/{passage_id}/`: 본문 중심 lineage (`_manifest.md` + `v01..vNN`)
    - `series/{series_id}/`: 시리즈 기획·진행 (`_manifest.md` + 기획안)
    - `{date}/{category}/`: 비-본문 작업물 (심방/행정/공지)
    - `devotionals/{topic-slug}/`: 본문 미식별 묵상 폴백
