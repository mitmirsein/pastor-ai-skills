# 🕊️ Pastor-KR (High-Precision Pastoral AI Toolkit)

> **버전 (Version): v2.10 (Trusted Data · Voice · Rhythm · Safety)**
> *이전: v2.7 (Audit Gate & Journal Lint)*

**Agentic pastoral workflow framework with 'Concierge & Guild + Memory + Quality Gate' architecture. High-precision Korean toolkit featuring 24 specialized skills + 3 harness quality-gate tools + domain lens packs, based on '6 Gems' & 'Inferential Ontology', with persistent pastoral memory, liturgical-calendar awareness, passage-centric lineage, and forensic audit gates.**

**"오케스트레이터 + 전문가 길드 + 목회 메모리" 아키텍처 기반의 고성능 한국어 목회 지원 AI 스킬셋.**
단 하나의 진입점(`Pastor-Concierge`)을 통해 복잡한 스킬 선택의 고민 없이 목회 워크플로우를 자동화하며, **매 세션 진입 시 진행 중인 사역(설교/시리즈/심방)과 절기 컨텍스트를 자동 복원**합니다.

![Pastor-KR Hero Image](assets/hero-image.jpg)

**Pastor-KR**은 목회 현장의 고유한 맥락을 깊이 이해하고, 실제적인 사역 결과물을 만들어내는 **고성능 한국어 목회 지원 AI 스킬셋**입니다. 

### 🧥 자신만의 맞춤옷을 만들어 입으십시오
이 도구들은 단순히 정해진 답을 내놓는 자판기가 아닙니다. 각 목회지의 상황과 성도들의 필요는 모두 다릅니다. 제공된 스킬셋을 기반으로 목사님만의 고유한 신학적 철학과 목양의 언어를 덧입혀, **'우리 교회에 가장 잘 어울리는 맞춤옷'**으로 완성해 나가시기를 권장합니다. `core/foundation.md`를 수정하거나 각 스킬의 지침을 조정하는 과정 자체가 곧 목사님의 사역을 AI와 함께 빚어가는 거룩한 동역이 될 것입니다.

---

## 🚀 1분 만에 사역 비서 가동하기 (Quick Start)

가장 간편한 방법입니다. 사용하시는 AI(Antigravity, Cursor, Claude Code, Codex 등)에게 **아래 문구와 저장소 주소를 복사해서 보내기만 하세요.**

> **"아래 깃허브 저장소의 모든 지침을 로드해 줘. 별도의 지시가 없더라도 전용 프로젝트 폴더(`pastor-ai-toolkit`)를 생성하여 툴킷을 구성하고, `USER_GUIDE.md`를 학습하여 나를 돕는 수석 비서 'Pastor-Concierge' 모드로 가동해 줘. 앞으로 내가 자연어로 사역 요청을 하면, 네가 의도를 파악해서 가장 적합한 스킬로 안내해 줘야 해."**
>
> **📍 저장소 주소:** `https://github.com/mitmirsein/pastor-ai-skills-kr.git`

*(URL 인식이 어려운 환경이라면, 파일을 내려받아 직접 업로드하거나 폴더를 공유해 주세요.)*

> **차후 방향:** GitHub·터미널·IDE에 익숙하지 않은 목회자를 위해, v3 후보로 `http://localhost:<port>`에서 여는 로컬 웹 대시보드를 검토합니다. 현재 v2.x는 Markdown 기반 스킬셋이며, v3 구상은 [ROADMAP.md](ROADMAP.md)에 보관합니다.

---

## 🌟 프로젝트의 핵심 가치 (v2.10 업데이트)

1. **인지 부하 최소화 (오케스트레이터):** 24개의 스킬 + 3개의 harness 도구를 외울 필요가 없습니다. `00_pastor_concierge`에게 자연어로 말하면 최적의 스킬을 매칭해 줍니다.
2. **단절 없는 워크플로우 (파이프라인):** 하나의 작업이 끝나면 `Call to Action`을 통해 다음 단계(예: 브레인스토밍 ➔ 주해 ➔ 검증 ➔ 블로그 발행)를 자연스럽게 제안합니다.
3. **정밀도 최극대화 (전문가 길드):** 범용 프롬프트 대통합의 함정을 피하고, 각 목적에 특화된 개별 에이전트들의 페르소나를 완벽히 보존합니다.
4. **추론적 온톨로지(Inferential Ontology):** 별도의 데이터베이스 없이도 AI가 본문의 핵심 개념을 엔티티(Entity)와 관계로 해체하여 분석하는 논리가 탑재되어 있습니다. (적용: `sermon-research`, `biblical-dilemma-solver`, `sermon-brainstorming`, `sermon-red-team`, `devotional-generator`, `small-group-guide`, `sermon-cardnews-maker`)
5. **🪔 목회 메모리 (v2.5 신규):** `core/pastor_journal.md`에 진행 중인 설교/시리즈/심방/기도제목이 자동 누적·갱신됩니다. Concierge는 매 세션 진입 시 이를 의무 로드하여, 콜드 스타트 없이 사역의 흐름을 이어갑니다. (PII 보호: 직분+이니셜만 기록)
6. **🗓️ 절기 자각 (v2.5 신규):** `core/liturgical_calendar.md`가 교회력(대림~일반)과 한국 교회 고유 절기(맥추/추수/송구영신/종교개혁/어린이/어버이)를 매핑합니다. "이번 주일 뭐 할까?"라는 모호한 질문에도 절기 흐름을 결합한 본문 후보가 제시됩니다.
7. **📜 본문 중심 lineage (v2.5 신규):** 동일 본문에 대한 모든 작업물이 `outputs/sermons/{passage_id}/`라는 하나의 폴더에 누적되며, `_manifest.md`가 작업 이력을 한눈에 보여줍니다. "이 본문 어디까지 했지?"가 즉시 보입니다.
8. **🛠️ 메타 도구 (v2.6 Tier 2):** `recall`과 `weekly-briefing`이 v2.5가 쌓은 자산을 **꺼내 쓰는 도구**를 제공합니다. "지난번 마태 5장 어떻게 했지?"(recall) 한마디로 과거 lineage를 인덱싱하고, 월요일 아침 한 장(weekly-briefing)으로 지난 주 사역과 이번 주 우선순위를 파악합니다.
9. **🛑 발행 품질 게이트 (v2.7):** `harness/sermon_audit`이 발행 전 사역물을 5대 렌즈(원어·신학·Foundation·회중·논리)로 검수하여 80점 미만 시 발행을 차단합니다. v2.8부터 채점 전 **Claim Ledger(주장 증거표)** 작성이 의무이며, 검증 불가 항목은 감점이 아니라 **채점 보류**로 정직하게 처리합니다.
10. **📖 본문 팩 우선 (v2.8 신규):** 성경 본문을 다루는 모든 스킬은 분석 전에 본문 전문을 확보합니다 — `data/scripture/` 슬롯(사용자 로컬 주입) 또는 붙여넣기. **기억으로부터의 성경 인용을 금지**하여, 목회자의 비서에게 가장 치명적인 실패(그럴듯한 의역 혼합·존재하지 않는 절 번호)를 구조적으로 차단합니다.
11. **⚙️/📋 듀얼 모드 (v2.8 신규):** 파일 접근이 없는 챗 환경에서도 침묵 실패 없이 동작합니다 — 저장 대신 복사용 블록을 건네고, 그 사실을 정직하게 알립니다 (`core/_hooks.md`).
12. **🎙️ 목회자 보이스 (v2.9 신규):** `voice-setup`이 목사님의 실제 설교문에서 문체 지문을 추출해 `core/pastor_voice.md`에 카드로 보존합니다. 칼럼·블로그 등 발행물은 거장 모사가 아니라 **목사님 자신의 문체**가 기본값이 됩니다.
13. **🗓️ 주간 리듬 + 🔁 회고 루프 (v2.9 신규):** 비서가 먼저 챙깁니다 — 요일과 진행 상태를 교차해 "오늘의 권장 동선"을 제안하고(예: "금요일인데 아직 검증 전입니다"), 선포 후 `sermon-retro` 3분 회고가 lessons로 누적되어 다음 설교 준비에 반영됩니다.
14. **🧯 목양 안전 + 👥 회중 페르소나 (v2.10 신규):** 위기 상황(자해·학대·급성 위기)에서는 콘텐츠보다 전문 연계 안내가 먼저이며, 장례·투병 등 상황별 금기 언어("다 하나님의 뜻")를 차단합니다. 목회자가 정의한 회중 페르소나로 레드팀이 "회중석 시뮬레이션"을 수행합니다.

---

## 📖 스킬 디렉토리 구조 (전문가 길드)

v2.5부터 모든 스킬은 목회자의 실제 워크플로우에 따라 5개의 직관적인 그룹으로 운영되며, 작업 결과가 `outputs/` 폴더에 **본문 중심 lineage** 방식으로 자동 저장됩니다.

### 🛎️ `00_pastor_concierge` (단일 진입점)
- `SKILL.md`: 사용자의 자연어 의도를 분석하여 아래의 5대 그룹(+harness·lenses)으로 라우팅해주는 최상위 수석 비서 (모드 판별·오늘의 동선 포함)

### 💎 `01_sermon_core` (설교 코어)
- `sermon-brainstorming.md`: 소크라테스식 문답을 통한 설교 인사이트 발굴
- `sermon-research.md`: 6 Gems 엔진 기반의 고정밀 주해 리포트 생성
- `biblical-dilemma-solver.md`: 성경 난제에 대한 입체적 변증 가이드
- `sermon-red-team.md`: 설교 원고의 신학적 맹점 및 회중 시선 분석
- `sermon-series-planner.md`: 4-6주 단위의 강해 설교 시리즈 기획
- `sermon-retro.md` *(v2.9)*: 선포 후 3분 회고 — lesson을 누적해 다음 설교에 반영

### 🕊️ `02_pastoral_care` (목양 코어)
- `bible-study-generator.md`: 주해(Core)-교안(Lesson)-워크북(Workbook) 통합 성경공부 설계
- `small-group-guide.md`: 설교 메시지를 성도들의 삶으로 연결하는 나눔지(관찰/적용) 생성
- `devotional-generator.md`: 매일/주중 공유할 수 있는 짧은 QT/묵상 콘텐츠 제작
- `visitation-guide.md`: 상황별 심방 성구 및 목회적 권면 가이드

### 📢 `03_omni_publisher` (재생산 및 다매체 확산)
- `SKILL.md` (Sermon-Republisher): 설교 원고를 1회 입력받아 아래 포맷들로 분기 변환 안내 (Thin Router)
- `sermon-to-column.md`: 설교문을 유진 피터슨/팀 켈러 풍의 고급 칼럼으로 리폼
- `sermon-to-blog.md`: 설교를 웹사이트/블로그 포스팅용 텍스트로 전환
- `sermon-to-tts.md`: 설교문을 3분 분량의 오디오 TTS 대본으로 변환
- `sermon-cardnews-maker.md`: 설교 핵심 내용을 4-5컷의 카드뉴스 기획 및 소셜 캡션 추출

### 📋 `04_church_admin` (행정 보조)
- `bulletin-helper.md`: 주보 광고 및 교회 소식 가독성 있게 정리
- `announcement-script.md`: 자연스럽고 따뜻한 강단 광고 스크립트 작성
- `pastoral-letter.md`: 절기 및 상황별 고품격 공식 목회 서신 작성
- `admin-email.md`: 정중하고 명확한 교회 행정 및 대외 비즈니스 이메일 작성
- `meeting-agenda.md`: 당회 및 제직회 등 각종 회의 안건 구조화

### 🛠️ `05_meta_tools` (메타 도구)
- `foundation-setup.md`: 첫 설치 시 교회·목회자 메타데이터 인터뷰 및 `core/foundation.md` 초기화
- `journal-show.md`: `pastor_journal.md` 현재 상태를 시각화된 대시보드로 표시
- `recall.md`: 자연어 질의로 `outputs/` 내 과거 사역 자산 검색·인덱싱 (읽기 전용)
- `weekly-briefing.md`: 지정 기간 사역 다이제스트 + 다음 주 우선순위 3가지 + 메모리 헬스 체크 + 품질 추이(v2.10)
- `voice-setup.md` *(v2.9)*: 설교문 2~3편으로 보이스 카드 추출·확정 → `core/pastor_voice.md`

### 🛑 `harness/` (품질 보증 — v2.7 신규)
`skills/`와 분리된 **감사 전용 위계**입니다. 사역 *작업* 도구가 아니라 사역 *품질 보증* 도구로, 발행 차단 권한을 갖는 유일한 디렉토리입니다.
- `sermon_audit.md`: 발행 직전 사역물 5렌즈 포렌식 검수 (80점 fail-fast + Claim Ledger 증거표, v2.8)
- `journal_lint.md`: `pastor_journal.md` 스키마·PII·표류·만료 점검 (주 1회 권장)
- `routing_eval.md` *(v2.10)*: Concierge 라우팅 회귀 골든셋 평가 (`tests/routing_cases.md`)
- `_README.md`: harness/ 운용 정책 및 책임 경계 문서

### 📚 `data/` (비서의 서재 — v2.8 신규)
빈 **슬롯**으로 출시됩니다. 사용자가 보유한 성경 본문(`data/scripture/`)·신학 용어표(`data/terms/`)를 넣으면 스킬들이 자동 인지하여 인용 검증 품질이 올라갑니다. 저작권 자료는 커밋 금지(.gitignore) — 규약: `data/_README.md`

### 🔭 `lenses/` (주제 렌즈 팩 — v2.10 신규)
특정 신학 주제의 Claim·Aporia를 red-team 자문 질문으로 변환한 렌즈 모음. 본문이 겹치면 자동 권장됩니다. (현재: `paulus-temple.md`)

---

## 🪔 v2.5 컨텍스트 트리오 (SSOT Trio)
Concierge가 매 세션 진입 시 의무 로드하는 3개 파일이 사역의 단일 진실 공급원(Single Source of Truth)을 구성합니다.

| 파일 | 역할 |
|---|---|
| `core/foundation.md` | 교회·목회자 메타데이터 (교단, 신학적 지향, 톤) |
| `core/pastor_journal.md` | 진행 중인 설교/시리즈/심방, 최근 주제, 기도제목, lessons(v2.9) |
| `core/liturgical_calendar.md` | 교회력 + 한국 교회 고유 절기 매핑 규칙 |
| `core/pastor_voice.md` *(v2.9)* | 목회자 보이스 카드 — 발행물 기본 문체 |
| `core/pastoral_rhythm.md` *(v2.9)* | 주간 리듬표 — 오늘의 권장 동선 |
| `core/care_safety.md` *(v2.10)* | 목양 안전 가드레일 (목양 스킬 의무 로드) |
| `core/congregation_personas.md` *(v2.10)* | 회중 페르소나 렌즈 (목회자 작성) |
| `core/_hooks.md` *(v2.8)* | 표준 훅 단일 정의 — 듀얼 모드·저장·journal·본문 팩 |

> 사역의 흐름을 잃지 않으려면 `core/pastor_journal.md`만 정기적으로 살펴보세요. 자동 갱신되지만, 종결된 시리즈를 archive로 옮기거나 만료된 기도제목을 정리하는 것은 사용자의 몫입니다.

---

## 📂 outputs/ 구조 (v2.5)

```
outputs/
├── sermons/{passage_id}/         # 본문 중심 lineage (설교 코어 / 옴니 퍼블리셔 / 일부 목양)
│   ├── _manifest.md
│   ├── v01_sermon-brainstorming_2026-05-06.md
│   ├── v02_sermon-research_2026-05-10.md
│   └── ...
├── series/{series_id}/           # 시리즈 기획·진행
│   ├── _manifest.md
│   └── plan_2026-04-05.md
├── {date}/{category}/            # 비-본문 작업물 (심방 / 행정 / 공지)
│   └── ...
└── devotionals/{topic-slug}/     # 본문 미식별 묵상 폴백
```

`passage_id` 명명 규칙과 manifest 구조는 `outputs/sermons/_README.md`를 참고하세요.

---

## 🛡️ 할루시네이션(환각) 방지 및 이중 검수 루틴
본 프로젝트는 `core/foundation.md`에 **글로벌 가드레일**이 설치되어 있습니다. 결과물이 의심스럽거나, 원어 분석이 포함된 경우 아래 문구를 복사하여 AI에게 입력하십시오.

> **"방금 네가 내놓은 원어 분석과 주석적 견해를 이 저장소의 `core/foundation.md` 가드레일에 따라 재검토(Re-check)해 줘. 지어낸 부분이나 비약이 있다면 스스로 수정해."**

---

## 🙏 Acknowledgments (감사 인사)
본 프로젝트는 아래의 선행 연구와 오픈 소스 프로젝트에 영감을 받아 제작되었습니다.
- **Original Creator:** 본 툴킷의 모태가 된 [pastor-ai-skills](https://github.com/tkcostello/pastor-ai-skills)의 제작자 **Thomas Costello (@tkcostello)** 님께 깊은 감사를 표합니다. 
- **Support:** 본 툴킷이 한국 교회 목회자분들의 사역에 작은 보탬이 되기를 소망합니다.

---

## ⚖️ 저작권 및 배포
본 프로젝트는 **MIT License**를 따릅니다. 
> **Note:** 본 툴킷은 목회자의 사역을 보조하는 도구입니다. 최종적인 설교의 메시지와 영적 판단은 기도 가운데 목회자 본인이 직접 결정하시기를 권장합니다.
