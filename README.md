# 🕊️ Pastor-KR (High-Precision Pastoral AI Toolkit)

> **버전 (Version): v2.1 (Persistence & Layered Orchestrator)**

**Agentic pastoral workflow framework with 'Concierge & Guild' architecture. High-precision Korean toolkit featuring 19 specialized skills based on '6 Gems' & 'Inferential Ontology'.**

**"오케스트레이터 + 전문가 길드" 아키텍처 기반의 고성능 한국어 목회 지원 AI 스킬셋.**
단 하나의 진입점(`Pastor-Concierge`)을 통해 복잡한 스킬 선택의 고민 없이 목회 워크플로우를 자동화합니다.

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

---

## 🌟 프로젝트의 핵심 가치 (v2.1 업데이트)

1. **인지 부하 최소화 (오케스트레이터):** 19개의 스킬 목록을 외울 필요가 없습니다. `00_pastor_concierge`에게 자연어로 말하면 최적의 스킬을 매칭해 줍니다.
2. **단절 없는 워크플로우 (파이프라인):** 하나의 작업이 끝나면 `Call to Action`을 통해 다음 단계(예: 브레인스토밍 ➔ 주해 ➔ 검증 ➔ 블로그 발행)를 자연스럽게 제안합니다.
3. **정밀도 최극대화 (전문가 길드):** 범용 프롬프트 대통합의 함정을 피하고, 각 목적에 특화된 개별 에이전트들의 페르소나를 완벽히 보존합니다.
4. **추론적 온톨로지(Inferential Ontology):** 별도의 데이터베이스 없이도 AI가 본문의 핵심 개념을 엔티티(Entity)와 관계로 해체하여 분석하는 논리가 탑재되어 있습니다. (적용: `sermon-research`, `biblical-dilemma-solver`, `sermon-brainstorming`, `sermon-red-team`, `devotional-generator`, `small-group-guide`, `sermon-cardnews-maker`)

---

## 📖 스킬 디렉토리 구조 (전문가 길드)

v2.1부터 모든 스킬은 목회자의 실제 워크플로우에 따라 5개의 직관적인 그룹으로 재편되었으며, 작업 결과가 `outputs/` 폴더에 자동으로 저장됩니다.

### 🛎️ `00_pastor_concierge` (단일 진입점)
- `SKILL.md`: 사용자의 자연어 의도를 분석하여 아래의 4대 코어 스킬로 라우팅해주는 최상위 수석 비서

### 💎 `01_sermon_core` (설교 코어)
- `sermon-brainstorming.md`: 소크라테스식 문답을 통한 설교 인사이트 발굴
- `sermon-research.md`: 6 Gems 엔진 기반의 고정밀 주해 리포트 생성
- `biblical-dilemma-solver.md`: 성경 난제에 대한 입체적 변증 가이드
- `sermon-red-team.md`: 설교 원고의 신학적 맹점 및 회중 시선 분석
- `sermon-series-planner.md`: 4-6주 단위의 강해 설교 시리즈 기획

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
