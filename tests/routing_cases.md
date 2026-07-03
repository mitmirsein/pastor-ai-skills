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
| 32 | (모호) "설교 준비 도와줘" | 보완 질문 1~2개 → 본문/단계 확인 후 라우팅 | 즉답 금지 |
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
