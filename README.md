# 🕊️ Pastor-KR (High-Precision Pastoral AI Toolkit)

![Pastor-KR Hero Image](assets/hero-image.jpg)

**Pastor-KR**은 목회 현장의 고유한 맥락을 깊이 이해하고, 실제적인 사역 결과물을 만들어내는 **고성능 한국어 목회 지원 AI 스킬셋**입니다. 

### 🧥 자신만의 맞춤옷을 만들어 입으십시오

이 도구들은 단순히 정해진 답을 내놓는 자판기가 아닙니다. 각 목회지의 상황과 성도들의 필요는 모두 다릅니다. 

제공된 스킬셋을 기반으로 목사님만의 고유한 신학적 철학과 목양의 언어를 덧입혀, **'우리 교회에 가장 잘 어울리는 맞춤옷'**으로 완성해 나가시기를 권장합니다. `core/foundation.md`를 수정하거나 각 스킬의 지침을 조정하는 과정 자체가 곧 목사님의 사역을 AI와 함께 빚어가는 거룩한 동역이 될 것입니다.

---

## 🚀 1분 만에 사역 비서 가동하기 (Quick Start)

가장 간편한 방법입니다. 사용하시는 AI(Cursor, Claude, ChatGPT 등)에게 **아래 문구와 저장소 주소를 복사해서 보내기만 하세요.**

> **"아래 깃허브 저장소에 담긴 사역 지침들을 네 지식으로 로드해서, 나를 돕는 '고성능 목회 비서'로 가동해 줘. 앞으로 내가 요청하는 모든 사역은 이 저장소의 '6 Gems' 원칙과 가드레일에 따라 수행해야 해."**
>
> **📍 저장소 주소:** `https://github.com/mitmirsein/pastor-ai-skills-kr.git`

*(URL 인식이 어려운 환경이라면, 파일을 내려받아 직접 업로드하거나 폴더를 공유해 주세요.)*

---

## 🛡️ 할루시네이션(환각) 방지 및 검수 가이드

본 프로젝트는 RAG(검색 증강) 없이도 높은 신뢰도를 유지하기 위해 `core/foundation.md`에 **글로벌 가드레일**이 설치되어 있습니다. 그럼에도 불구하고 AI의 특성상 발생할 수 있는 환각 현상을 최소화하기 위해 다음의 **'이중 검수 루틴(Double-Pass Routine)'**을 적극 권장합니다.

### 🔍 사용자의 이중 검수 명령 (The Re-check Prompt)
결과물이 조금이라도 의심스럽거나, 특히 원어 분석/학술적 견해가 포함된 경우 아래 문구를 복사하여 AI에게 입력하십시오.

> **"방금 네가 내놓은 원어 분석과 주석적 견해를 이 저장소의 `core/foundation.md` 가드레일에 따라 재검토(Re-check)해 줘. 지어낸 부분이나 비약이 있다면 스스로 수정해."**

### 💡 왜 이 명령이 필요한가요?
AI는 한 번에 답을 낼 때보다, **자신이 낸 답을 다시 한번 검토할 때** 비약적으로 높은 추론 성능을 보입니다. 이 명령을 통해 에이전트는 내부적인 '레드팀' 모드를 가동하여 오류를 스스로 수정하게 됩니다.

---

## 🌟 프로젝트의 핵심 가치

1.  **목회적 감수성:** 번역투가 아닌, 성도들의 마음을 만지는 따뜻하고 권위 있는 한국어 목양 언어를 사용합니다.
2.  **6 Gems 엔진:** 성경 본문을 구조, 문헌, 정경, 상황 등 6가지 깊은 렌즈로 분석합니다.
3.  **추론적 온톨로지(Inferential Ontology):** 별도의 데이터베이스 없이도 AI가 본문의 핵심 개념을 엔티티(Entity)와 관계(Relation) 단위로 해체하여 분석하는 **'최소한의 온톨로지 빌딩'** 로직이 **주요 주해 및 영성 형성 스킬**의 사유 체계를 지탱합니다.
4.  **즉시 실행 가능 (Portable):** 별도의 프로그램 설치 없이 지침 파일만 있으면 어디서든 즉시 가동됩니다.
5.  **개인화된 사역:** `foundation.md` 설정을 통해 우리 교회만의 맞춤형 결과물을 얻습니다.

---

### 📖 주요 스킬 리스트 (총 20종)

현재 **총 20개**의 고정밀 사역 스킬이 탑재되어 있습니다.

### 🔍 주해 및 사역 연구
- `sermon-research.md`: 6 Gems 엔진 기반의 고정밀 주해 리포트 생성
- `bible-study-generator.md`: 주해(Core)-교안(Lesson)-워크북(Workbook) 통합 성경공부 설계
- `sermon-brainstorming.md`: 소크라테스식 문답을 통한 설교 인사이트 발굴
- `sermon-series-planner.md`: 4-6주 단위의 강해 설교 시리즈 기획
- `biblical-dilemma-solver.md`: 성경 난제에 대한 입체적 변증 가이드

### 🖋️ 콘텐츠 전환 및 고급화
- `sermon-to-column.md`: 설교문을 유진 피터슨/팀 켈러 풍의 고급 칼럼으로 리폼
- `sermon-cardnews-maker.md`: 설교 핵심 내용을 4-5컷의 카드뉴스로 기획
- `sermon-to-tts.md`: 설교문을 3분 분량의 오디오 TTS 대본으로 변환
- `sermon-to-blog.md`: 설교를 블로그 포스팅용 텍스트로 전환

### 🛡️ 비평 및 행정 지원
- `sermon-red-team.md`: 설교 원고의 신학적 맹점 및 회중 시선 분석
- `pastoral-letter.md`: 절기 및 상황별 고품격 목양 편지 작성
- `admin-email.md`: 정중하고 명확한 교회 행정 이메일 작성
- `bulletin-helper.md`: 주보 광고 및 교회 소식 가독성 있게 정리
- `announcement-script.md`: 자연스럽고 따뜻한 광고 스크립트 작성
- `meeting-agenda.md`: 당회 및 제직회 회의 안건 구조화

### 🤝 목양 및 소그룹
- `bible-study-generator.md`: 주해(Core)-교안(Lesson)-워크북(Workbook) 통합 성경공부 설계
- `devotional-generator.md`: 개인의 영적 형성을 돕는 고정밀 QT/묵상 가이드 생성
- `small-group-guide.md`: 설교 메시지를 성도들의 삶으로 연결하는 나눔지(관찰/적용) 생성
- `visitation-guide.md`: 상황별 심방 성구 및 목회적 권면 가이드
- `mid-week-meditation.md`: 주중 성도들에게 공유할 짧은 묵상 콘텐츠 제작
- `social-media-post.md`: 인스타그램/페이스북용 짧은 영감 문구 추출

---

## 🙏 Acknowledgments (감사 인사)

본 프로젝트는 아래의 선행 연구와 오픈 소스 프로젝트에 영감을 받아 제작되었습니다.

- **Original Creator:** 본 툴킷의 모태가 된 [pastor-ai-skills](https://github.com/tkcostello/pastor-ai-skills)의 제작자 **Thomas Costello (@tkcostello)** 님께 깊은 감사를 표합니다. 
- **Support:** 본 툴킷이 한국 교회 목회자분들의 사역에 작은 보탬이 되기를 소망합니다.

---

## ⚖️ 저작권 및 배포
본 프로젝트는 **MIT License**를 따릅니다. 

> **Note:** 본 툴킷은 목회자의 사역을 보조하는 도구입니다. 최종적인 설교의 메시지와 영적 판단은 기도 가운데 목회자 본인이 직접 결정하시기를 권장합니다.
