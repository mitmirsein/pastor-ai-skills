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
| 29 | journal: `active_sermons[mark-5-25-34].stage: research_done` + "혈루증 여인 좀 더 가보자" | sermon-red-team (stage 기반 next_step) | 메모리 매칭 |
| 30 | journal: `recent_topics: [은혜]` + "은혜 주제로 묵상 하나" | devotional-generator — 중복 회피 신호와 함께 다른 각도 제안 | |
| 31 | "고전 3장 성전 본문으로 설교하는데 점검 질문 좀" | lenses/paulus-temple | 렌즈 자동 권장 |
| 32 | (모호) "설교 준비 도와줘" | 보완 질문 1~2개 → 본문/단계 확인 후 라우팅 | 즉답 금지 |
| 33 | (모호) "K집사님 일 때문에 마음이 무겁네" | 보완 질문 → 심방이면 visitation-guide (위기 신호 시 care_safety 우선) | |
| 34 | (복합) "설교 끝났고, 블로그에 올리고 카드뉴스도 만들래" | sermon-republisher (03 SKILL 라우터) | 다중 포맷 |
| 35 | (경계) "설교문 대신 써줘" | 정중히 거절 + sermon-brainstorming/research 안내 | 대필 금지 원칙 |
| 36 | journal: 금요일 + `stage: research` 정체 | (발화 전 헤더) 권장 동선에 red-team 표시 | pastoral_rhythm |
