# 🧪 라우팅 골든셋 (Routing Golden Cases) — v2.10 P2-9

> Concierge의 의도 분류 회귀 테스트. 실행 절차는 `harness/routing_eval.md`.
> **유지 규약**: 스킬을 추가·수정하는 변경에는 케이스 2건 이상을 함께 추가한다.
> 표기: `journal:` 접두 케이스는 해당 메모리 상태를 가정한 라우팅이다. `(모호)`는 1~2개 보완 질문 후 기대 스킬로 가야 한다.

| # | 발화 | 기대 스킬 | 비고 |
|---|---|---|---|
| 1 | "이번 주 구역예배 교안 만들어야 해" | small-group-guide | |
| 2 | "성도님 심방 가는데 위로 말씀 추천 좀" | visitation-guide | |
| 3 | "마가복음 5장으로 설교 아이디어 좀 굴려보자" | sermon-brainstorming | |
| 4 | "본문 확정했어. 막 5:25-34 깊이 파줘" | sermon-research | |
| 5 | "가나안 진멸 명령, 청년부가 물어보면 뭐라고 하지?" | biblical-dilemma-solver | |
| 6 | "내일 설교 원고야. 매섭게 까줘" | sermon-red-team | |
| 7 | "사순절에 6주짜리 강해 시리즈 하나 기획하자" | sermon-series-planner | |
| 8 | "주일학교 교사용으로 요한복음 3장 교재 만들어줘" | bible-study-generator | |
| 9 | "성도들 카톡으로 보낼 짧은 묵상 하나" | devotional-generator | |
| 10 | "지난 주일 설교를 블로그에 올리게 다듬어줘" | sermon-to-blog | |
| 11 | "설교를 주보 칼럼으로 바꿔줘" | sermon-to-column | |
| 12 | "설교 요약을 카드뉴스로 만들어서 인스타에 올리고 싶어" | sermon-cardnews-maker | |
| 13 | "설교 오디오북용 3분 대본으로" | sermon-to-tts | |
| 14 | "이번 주 주보 광고 정리해줘" | bulletin-helper | |
| 15 | "강단에서 읽을 광고 멘트로 다듬어줘" | announcement-script | |
| 16 | "성탄절에 전 성도에게 보낼 목회서신" | pastoral-letter | |
| 17 | "외부 강사 섭외 메일 써야 해" | admin-email | |
| 18 | "다음 주 당회 안건 정리하자" | meeting-agenda | |
| 19 | "처음 설치했어. 우리 교회 정보 설정하자" | foundation-setup | |
| 20 | "지금 뭐 진행 중이었지? 메모리 보여줘" | journal-show | |
| 21 | "지난번 마태 5장 어디까지 했지?" | recall | 시간 후행 키워드 |
| 22 | "은혜 다룬 자료 모아줘" | recall | 검색 의도 |
| 23 | "한 주 정리하고 이번 주 뭐 할지 보자" | weekly-briefing | |
| 24 | "발행 전에 이 원고 최종 점검해줘" | sermon_audit | harness |
| 25 | "메모리 위생 검사 한번 돌리자" | journal_lint | harness |
| 26 | "내 설교 문체 등록하고 싶어" | voice-setup | v2.9 |
| 27 | "어제 설교 돌아보자" | sermon-retro | v2.9 |
| 28 | journal: `active_series.next_passage: 엡 2:11-22` + "이번 주일 뭐 하지?" | sermon-brainstorming(또는 research) — 엡 2:11-22 1순위 제시 | 시리즈 > 절기 |
| 29 | journal: `active_sermons[mark-5-25-34].stage: research` + "혈루증 여인 좀 더 가보자" | sermon-red-team (stage 기반 next_step) | 메모리 매칭 |
| 30 | journal: `recent_topics: [은혜]` + "은혜 주제로 묵상 하나" | devotional-generator — 중복 회피 신호와 함께 다른 각도 제안 | |
| 31 | lenses: 고전 3:16-17을 `applies_to`로 갖는 렌즈 설치 가정 + "고전 3장 성전 본문으로 설교하는데 점검 질문 좀" | 해당 렌즈 자동 권장 (렌즈 미설치 환경은 sermon-red-team) | 렌즈 자동 권장 |
| 32 | (모호) "설교 준비 도와줘" | 보완 질문 1회(본문 확정 여부) → 정해짐: qt-germinate-scan 모드 2 / 미정: 모드 1(창 2주) | 즉답 금지 · v2.15 설교 준비 패턴 |
| 33 | (모호) "K집사님 일 때문에 마음이 무겁네" | 보완 질문 → 심방이면 visitation-guide (위기 신호 시 care_safety 우선) | |
| 34 | (복합) "설교 끝났고, 블로그에 올리고 카드뉴스도 만들래" | sermon-republisher (03 SKILL 라우터) | 다중 포맷 |
| 35 | (경계) "설교문 대신 써줘" | 정중히 거절 + sermon-brainstorming/research 안내 | 대필 금지 원칙 |
| 36 | journal: 금요일 + `stage: research` 정체 | (발화 전 헤더) 권장 동선에 red-team 표시 | pastoral_rhythm |
| 37 | "오늘 아모스 1장 묵상했는데, 처음 든 생각 적어봤어. 같이 더 파보자" | qt-companion | v2.11 — 목회자 자신의 매일 묵상 심화(≠성도용 devotional-generator) |
| 38 | "매일 큐티하는 거 질문 좀 던져주면서 도와줘" | qt-companion | v2.11 — 소크라테스 티키타카 |
| 39 | "요즘 큐티한 거 모아서 설교할 만한 본문 있는지 봐줘" | qt-germinate-scan | v2.11 — 누적 큐티 발아(≠recall: 과거 산출물 검색) |
| 40 | "이번 달 묵상 중에 반복해서 돌아온 주제 있나?" | qt-germinate-scan | v2.11 |
| 41 | "아모스 1장 큐티들 시간순으로 모아서 설교 씨앗 만들어줘" | qt-germinate-seed | v2.11 |
| 42 | "발아 스캔 1번, 그걸로 씨앗 합성해줘" | qt-germinate-seed | v2.11 — 스캔 후속 |
| 43 | "Big Idea 나왔고 주해도 했어. 이제 설교 개요 같이 세우자" | sermon-outline-codraft | v2.11 — 동반작성(대필 아님) |
| 44 | "설교 구조 짜는 거 도와줘, 대지 내용은 내가 채울게" | sermon-outline-codraft | v2.11 |
| 45 | (경계) "설교 개요 완성해서 줘" | 대필 거절 + 동반작성(sermon-outline-codraft) 또는 brainstorming/research 안내 | 대필 vs 동반작성 구분 |
| 46 | "이번에 발아한 아모스 1장, 그걸로 주보 칼럼 하나 써줘" | qt-to-column | v2.11 — 큐티/씨앗 상류 칼럼 |
| 47 | "이 묵상을 내 문체로 칼럼 만들어줘" | qt-to-column | v2.11 — 초기 묵상 문체 기반 |
| 48 | (경계) "이 완성된 설교를 주보 칼럼으로 바꿔줘" | sermon-to-column | 완성 설교 하류 전환(≠qt-to-column 큐티 상류) |
| 49 | "이 칼럼 발행 전에 감사해줘" | sermon_audit | harness — 칼럼도 감사 대상 |
| 50 | "이 본문 원어 정밀 분석표(Table A)로 상·어휘상까지 뽑아줘" | sermon-research | v2.13 — 주해 스키마(원어 팩 게이트 준수) |
| 51 | "설교 전에 이 본문 오독 리스크랑 문맥 위치도 같이 짚어줘" | sermon-research | v2.13 — 목회적 리스크·문맥적 위치 |
| 52 | journal: `active_sermons[amos-1-1-15].preached_on: null` (audit 기록 없음) + "이 설교 초안 주보 칼럼으로 바꿔줘" | sermon-to-column + 안내에 "발행 전 sermon_audit 권장" 병기 · journal stage 유지(발행 전이 가드 §3.6) | 발행 직전 권장 + 조기 published 방지 |
| 53 | "레위기 4장 묵상하려는데 본문 배경/개괄 먼저 좀 짚어줘" | qt-companion (0단계 본문 브리핑) | v2.14 A — 묵상 전 컨텍스트(별도 스킬 아님, 큐티 동행 앞단) |
| 54 | "묵상 시작 전에 이 본문 컨텍스트만 마련해줘, 해석은 내가 할게" | qt-companion (브리핑 `pre` — 사실 오리엔테이션만, 해석층 보류) | v2.14 A — 출처 태그·판정 금지 |
| 55 | "큐티하는데 자꾸 내 얘기로만 흘러. 본문 딱 붙잡고 질문 던져줘" | qt-companion (본문 정박 티키타카) | v2.14 B — 본문 팩 문구 인용 질문 |
| 56 | "본문 개괄 말고 성도들 카톡으로 보낼 묵상 하나 만들어줘" | devotional-generator | v2.14 A/B 반례 — 브리핑·정박은 목회자 자신 큐티, 이건 성도용 생성물 |
| 57 | "요즘 큐티에서 자꾸 같은 긴장이 돌아오는데 뭔지 봐줘" | qt-germinate-scan (축 3 남은 긴장) | v2.14 C — 아포리아 발아(자발 등장 집계) |
| 58 | "레위기·시편·로마서 묵상에서 '부지중의 죄' 긴장이 반복되나?" | qt-germinate-scan (축 3) | v2.14 C — 흩어진 본문의 공통 긴장 |
| 59 | "이 주해 보고 나니 처음 묵상이 흔들려. 다시 묵상하게 도와줘" | qt-companion 재묵상 모드 | v2.14 E — 주해 이후 형성 왕복(YAML stage `research` 고정) |
| 60 | (경계) "주해 끝났으니 이제 설교 개요 세워줘" | sermon-outline-codraft | v2.14 E 경계 — 개요 요청은 재묵상 아님(codraft) |
| 61 | "칼뱅 주석에서 이 구절 어떻게 봤는지 서재 팩에서 찾아 인용해줘" | sermon-research (서재 팩 인용 — `data/commentary/` 조회, 출처 표기) | v2.14 D — 슬롯 3 격상 경로 |
| 62 | (경계) `data/commentary/` 비어 있음 + "주석 근거로 이 견해 뒷받침해줘" | sermon-research — 서재 팩 없음 정직 폴백(LLM 지식 + 학파 명시) | v2.14 D — 슬롯 폴백(강등 없음) |
| 63 | "다음 주 본문 로마서 8장인데 관련된 큐티 있었나 봐줘" | qt-germinate-scan (모드 2 본문 정박 수확) | v2.15 — 본문 지정 수확 |
| 64 | journal: `active_series.next_passage: 엡 2:11-22` + "설교 준비 시작하자" | qt-germinate-scan 모드 2 — 엡 2:11-22 정박 제안 | v2.15 — 시리즈 본문 자동 정박 |
| 65 | (경계) "지난번 로마서 8장 설교 어떻게 했었지?" | recall | 과거 산출물 검색 ≠ 정박 수확(과거 묵상) |
| 66 | (경계) "로마서 8장으로 그냥 아이디어부터 굴려보자" | sermon-brainstorming | 큐티 무관 신규 발상 ≠ 수확 |
| 67 | "지난주 레위기 4장 큐티한 거, 성도들 카톡으로 보낼 묵상으로 다듬어줘" | qt-to-devotional | v2.16 — 큐티→성도 묵상(층위 분리) |
| 68 | (경계) "요한복음 15장으로 성도용 묵상 하나 만들어줘" | devotional-generator | 큐티 무관 신규 생성 ≠ qt-to-devotional |
| 69 | (경계) "오늘 큐티 좀 더 깊이 들어가고 싶어" | qt-companion | 목회자 자신 심화 ≠ 성도용 발아 |
| 70 | "지난 주일 설교 본문으로 이번 주 월~토 묵상표 만들어줘" | devotional-generator (주간 세트 — 심화) | v2.16 — 회중 동행 주간 세트 |
| 71 | foundation: `column_venues`에 '주보(600자)' 설정 + "이 씨앗으로 주보에 실을 칼럼 써줘" | qt-to-column — 지면 '주보' 프로파일(600자) 적용 | v2.16 — 지면 프로파일 |
