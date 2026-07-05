# 🕊️ Pastor-KR (Project Entrypoint)

> **버전 (Version): v2.14 (Deep Lectio — 묵상 전 본문 브리핑 · 남은 긴장 발아 · 주해 이후 재묵상 · 서재 팩)**
> *이전 버전: v2.13 (Exegetical Precision — 주해 스키마 정밀화 · 구조 완결성 사전 게이트)*

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
- **발행 전이 가드 (v2.12):** 파생 발행물(칼럼·블로그·TTS·카드뉴스)은 `preached_on` 확인 전에 본체 설교의 stage를 `published`로 만들지 않습니다(`core/_hooks.md` §3.6). 발행물은 발행 전 `sermon_audit` 권장 — red-team을 거치지 않는 칼럼 상류 경로(qt-to-column) 포함. stage 유효값의 단일 정의는 `pastor_journal.md` §3.1.1.
- **주해 스키마 정밀화 (v2.13):** `sermon-research`의 주해 산출은 명시적 계약을 따릅니다 — 문맥적 위치(Pre/Post-text 논리 유형), Table A/B 표준 컬럼 스키마(상↔어휘상 분리·Louw-Nida·상호본문성/LXX), 목회적 리스크 관리, Big Idea·Action Plan **후보**. 단, 이 후보들은 연구 제안(재료)이며 확정·개요 작성은 목회자와 `sermon-outline-codraft`의 몫입니다(대필 거절 원칙 유지). Table A/B의 원어 표기는 원어 팩 게이트를 따릅니다(정본 없으면 정직 강등).
- **구조 완결성 사전 게이트 (v2.13):** `harness/sermon_audit`은 Claim Ledger·5렌즈 채점에 앞서 **구조 사전 게이트(§4.0)**를 실행합니다 — 절단·거부 시그니처·선언된 섹션 누락이 발견되면 채점하지 않고 `🛑 구조 결함`으로 즉시 반환합니다(5렌즈 산술 불변).
- **묵상 전 본문 브리핑 (v2.14):** `qt-companion`은 큐티 시작에 앞서 본문 오리엔테이션(책 속 위치·앞뒤 문맥·낯선 실재)을 **옵트아웃**으로 건넵니다(0단계). 각 항목은 **출처 태그**(`[본문 팩]`·`[서재 팩: 파일명]`·`[일반 지식 — 검증 불가]`)를 달며, **해석·판정·"핵심 메시지"·적용은 금지**합니다 — 장르·단락 경계도 '판정'하지 않고 본문 팩 표지 인용에 그칩니다(경계 확정은 `sermon-research`의 주해 행위). 초기 묵상은 여전히 불가침이며, 브리핑 섹션(`## 브리핑`)은 발아 합성(`qt-germinate-seed`) 대상이 아닙니다.
- **본문 대질 질문 (v2.14):** `qt-companion` 티키타카는 실제로 던지는 질문 가운데 **최소 1개가 본문 팩의 문구를 인용**하도록 하여 묵상이 본문에서 미끄러지지 않게 합니다. 단 본문 전문이 없으면(부분 팩) 요건을 면제하고 전문 붙여넣기를 1회 안내합니다(기억 인용 금지).
- **남은 긴장 발아 (v2.14):** `qt-germinate-scan`은 본문·주제에 더해 `## 남은 긴장`의 반복(축 3, 내부 노트 한정)을 발아 축으로 봅니다. 아포리아는 본문 발아 후에도 존속하며, `(재소환)` 유래는 자발 등장과 **분리 집계**하여 시스템이 스스로 만든 반복으로 임계를 채우지 않습니다. 긴장 태생 씨앗은 `qt-germinate-seed` 화이트리스트에 `## 남은 긴장`을 포함합니다.
- **주해 이후 재묵상 (v2.14):** `qt-companion` 재묵상 모드는 `sermon-research` 이후 "주해가 초기 묵상을 어디서 확증·전복했나"를 되짚습니다. 산출은 lineage에 저장하되 **YAML `stage: research` 고정**으로 manifest `current_stage` 후퇴를 막고, `qt_kind: secunda`라 발아 코퍼스에 섞이지 않으며, journal은 `notes`에 `[재묵상]`만 남겨 **본체 stage를 전진·후퇴시키지 않습니다**(§3.1.1 파생 작업 원리).
- **서재 팩 (v2.14):** `data/commentary/` 슬롯(2차 문헌)이 있으면 `sermon-research`(Phase 3)·`biblical-dilemma-solver`·`qt-companion` 브리핑이 **파일 출처를 표기하며 인용**하고, `sermon_audit` Claim Ledger 유형 ②·④ 검증이 **실제 대조로 격상**됩니다(원어 팩이 L1을 격상하는 것과 동형). 없으면 현행대로 LLM 지식 + 학파 명시로 정직 폴백합니다. 슬롯 내용물은 `.gitignore` 제외(저작권 자료 커밋 금지), 파일 최소 메타(저자·전통·서지) 의무 — 규약: `data/_README.md` 슬롯 3.

## 3. 워크플로우 (Workflow v2.5)
1. **의무 부트 시퀀스 (Concierge):** 매 세션 첫 발화 시 `core/foundation.md` → `core/pastor_journal.md` → `core/liturgical_calendar.md`를 순차 로드하여 컨텍스트를 복원합니다.
2. **의도 파악 + 메모리 매칭:** 발화를 메모리와 결합하여 "이번 주일 뭐 할까"만으로도 진행 중인 시리즈/심방/절기를 자동 추론합니다.
3. **최적 스킬 라우팅:** 5대 그룹 29개 스킬(+harness·lenses) 중 1개를 매칭하여 복사/붙여넣기용 완성 프롬프트를 제공합니다.
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
    - `03_omni_publisher/`: 재생산 얇은 라우터 및 다매체 변환 (블로그, 칼럼, TTS, 카드뉴스) + 큐티 발아 칼럼(qt-to-column)
    - `04_church_admin/`: 교회 행정, 주보, 목회서신, 이메일, 회의록
    - `05_meta_tools/` *(Tier 1·2)*: 시스템 자기 점검·조회 도구 (foundation-setup, journal-show, recall, weekly-briefing, voice-setup)
- `harness/` *(Tier 3)*: **품질 보증 도구** — skills/와 분리된 감사 전용 위계. 발행 차단 권한을 갖는 유일한 디렉토리.
    - `sermon_audit.md`: 발행 전 사역물 5렌즈 포렌식 검수 (80점 fail-fast + **Claim Ledger 증거표·검증 불가 채점 보류**, v2.8 · **구조 사전 게이트 §4.0**, v2.13)
    - `journal_lint.md`: `pastor_journal.md` 스키마·PII·표류 점검
    - `routing_eval.md` *(v2.10)*: Concierge 라우팅 회귀를 `tests/routing_cases.md` 골든셋으로 자가 평가
    - `_README.md`: harness/ 운용 정책 및 skills/와의 책임 경계
- `data/` *(v2.8 · v2.14)*: **비서의 서재 (Data Shelf)** — 정본 데이터 슬롯. `scripture/`(성경 본문, 사용자 로컬 주입·커밋 금지)·`terms/`(신학 용어 대조표)·`commentary/`(2차 문헌 서재 팩 — 주해·난제·브리핑 인용 격상·감사 대조, v2.14). 규약: `data/_README.md`
- `lenses/` *(v2.10)*: 주제 영역 red-team 렌즈 팩 — 사용자 제작·주입 슬롯 (커밋 금지, `data/`와 동일 원칙). 본문이 `applies_to`와 겹치면 자동 권장. 포맷: `lenses/_README.md`
- `tests/` *(v2.10)*: `routing_cases.md` — 라우팅 골든셋 (스킬 추가 시 케이스 2건 동반 규약)
- `docs/`: 아키텍처 설계, 기획, 리뷰 문서 보관소 (로컬 전용 — `.gitignore` 대상, 공개 배포에는 포함되지 않음)
- `outputs/`:
    - `sermons/{passage_id}/`: 본문 중심 lineage (`_manifest.md` + `v01..vNN`)
    - `series/{series_id}/`: 시리즈 기획·진행 (`_manifest.md` + 기획안)
    - `{date}/{category}/`: 비-본문 작업물 (심방/행정/공지)
    - `devotionals/{topic-slug}/`: 본문 미식별 묵상 폴백
