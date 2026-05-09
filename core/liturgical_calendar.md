---
schema_version: 1
last_updated: 2026-05-10
---

# 🗓️ Liturgical Calendar (절기 자각 레이어)

본 파일은 `Pastor-KR v2.5`의 **절기 자각 레이어**입니다.
`pastor-concierge`는 매 진입 시 `currentDate`를 본 파일의 매핑 규칙에 통과시켜 현재 위치한 교회력 절기와 한국 교회 고유 절기를 자동 식별합니다.

> 🎯 **목적:** "이번 주일 뭐 할까?"라는 모호한 질문에 절기·전통 흐름을 결합하여 본문/주제 후보를 추천한다.

---

## 1. 핵심 원칙 (Principles)

1. **절대일이 아닌 상대 주차로 사고한다.** 부활절·사순절·대림절은 매년 날짜가 바뀌므로, "오늘이 며칠인가"보다 "부활절 기준 몇 주 떨어져 있는가"가 우선 정보다.
2. **절기 톤이 본문 선택을 강요하지 않는다.** 절기는 *제안*이지 *제약*이 아니다. 강해 시리즈 진행 중이라면 시리즈가 우선이며, 절기는 부수 컨텍스트로만 활용한다.
3. **한국 교회 고유 절기를 1급 시민으로 다룬다.** 서구 교회력에 없는 맥추감사·송구영신·어린이주일·어버이주일 등은 한국 목회 현장에서 교회력 절기와 동등한 무게를 갖는다.
4. **교파 차이를 인정한다.** `core/foundation.md`의 `denomination`에 따라 활용 가중치가 달라진다 (장로교 합동/통합은 절기 의식 약함, 감리교/성공회는 강함). Concierge는 이를 참고하여 절기 강조 정도를 조절한다.

---

## 2. 서구 교회력 (Liturgical Year)

### 2.1 대림절 (Advent) — 4주
- **기간:** 성탄 직전 4번의 주일.
- **주제 흐름:** 1주 소망 → 2주 평화 → 3주 기쁨 → 4주 사랑.
- **추천 본문 결:** 이사야 메시아 예언, 누가 1장(수태고지/마리아의 노래), 마태 1장 족보.
- **톤:** 기다림과 갈망. 즉각적 위로보다 종말론적 시선.

### 2.2 성탄절기 (Christmas Season)
- **기간:** 성탄 당일 ~ 주현절 전날 (약 12일).
- **주제 흐름:** 성육신, 임마누엘.
- **추천 본문:** 요한 1:1-18, 누가 2장, 빌립보 2:5-11.
- **톤:** 경배, 신학적 깊이. (감상적 캐롤 톤 지양)

### 2.3 주현절기 (Epiphany) — 1월 6일 ~ 사순절 전
- **주제:** 그리스도의 나타나심(이방에 대한 계시).
- **추천 본문 결:** 동방박사, 세례, 가나 혼인, 변형(transfiguration).
- **톤:** 선교적, 보편적.

### 2.4 사순절 (Lent) — 6주 + 종려주일 + 고난주간
- **시작:** 재의 수요일(Ash Wednesday).
- **주제 흐름:** 회개, 자기부인, 십자가의 길.
- **종려주일(Palm Sunday):** 사순 6번째 주일. 환호와 배신의 긴장.
- **고난주간(Holy Week):** 종려주일 ~ 부활절 전날. 성목요일(세족), 성금요일(십자가) 별도 묵상.
- **추천 본문 결:** 광야 시험, 이사야 53장, 시편 22편, 수난 내러티브.
- **톤:** 절제, 자기 성찰. 화려한 수사 지양.

### 2.5 부활절기 (Easter Season) — 50일
- **기간:** 부활주일 ~ 오순절(Pentecost).
- **주제 흐름:** 부활 증언 → 부활 후 현현 → 승천 → 성령강림.
- **추천 본문:** 부활 내러티브 4복음서, 사도행전 1-2장, 고전 15장.
- **톤:** 기쁨, 새 창조, 증언.

### 2.6 오순절·일반절기 (Pentecost / Ordinary Time)
- **오순절:** 부활 후 50일째 주일. 성령강림.
- **일반절기:** 오순절 다음 주일 ~ 대림절 전. 1년의 절반 가까이 차지.
- **추천 흐름:** 강해 시리즈, 제자도, 교회론.
- **톤:** 일상의 거룩, 성장. (특별 절기 압박 없음 → 강해 시리즈 적기)

---

## 3. 한국 교회 고유 절기 (Korean Church Calendar)

### 3.1 신년주일 (New Year Sunday)
- **시점:** 1월 첫 주일.
- **주제:** 한 해의 비전, 결단, 청지기직.
- **추천 본문:** 빌 3:13-14, 시 90편, 잠 16:1-9.
- **주의:** 새해 야망보다 하나님 주권 강조.

### 3.2 어린이주일 (Children's Sunday)
- **시점:** 5월 첫 주일 (어린이날 5/5 인접).
- **주제:** 다음 세대, 신앙의 계승, 어린이 같은 믿음.
- **추천 본문:** 마 18:1-6, 신 6:4-9, 막 10:13-16.

### 3.3 어버이주일 (Parents' Sunday)
- **시점:** 5월 둘째 주일 (어버이날 5/8 인접).
- **주제:** 효, 가정, 부모 공경의 신학.
- **추천 본문:** 출 20:12, 엡 6:1-4, 신 5:16.
- **주의:** 비혼/사별/관계 단절 가정 배려 필수.

### 3.4 스승의 주일 / 가정의 달 (May Themes)
- **시점:** 5월 셋째 주일까지 가정·교사·청년 주제 흐름.
- **주의:** 이미 어린이/어버이 주일을 지났다면 가족 주제 과잉 지양.

### 3.5 맥추감사주일 (Early Harvest Thanksgiving)
- **시점:** 7월 첫 주일.
- **주제:** 상반기 결산 감사, 보리 추수의 영적 의미, 초실절(레 23:9-14).
- **추천 본문:** 신 26:1-11, 잠 3:9-10.
- **특이사항:** 한국 교회 고유. 성경적 초실절 신학을 한국 농경 절기에 접목.

### 3.6 종교개혁주일 (Reformation Sunday)
- **시점:** 10월 마지막 주일 (10/31 종교개혁기념일 인접).
- **주제:** 오직 성경, 오직 믿음, 오직 은혜.
- **추천 본문:** 롬 1:16-17, 엡 2:8-10, 합 2:4.
- **교파별 무게:** 장로교/개혁주의 → 매우 강조. 감리교/성공회 → 약하거나 생략 가능.

### 3.7 추수감사주일 (Thanksgiving Sunday)
- **시점:** 11월 셋째 주일 (교단별 차이 — 11월 첫 주일 또는 미국식 11월 넷째 목요일 직전 주일).
- **주제:** 한 해의 감사, 청지기직, 나눔.
- **추천 본문:** 신 8:1-10, 시 100편, 빌 4:6-7.

### 3.8 대림절 첫 주일 (한국 적용)
- **시점:** 11월 마지막 ~ 12월 첫 주일 사이.
- **참고:** 한국 보수 교단에서는 절기 인식이 약하므로, 강해 시리즈 종료 시점과 충돌 시 시리즈를 우선.

### 3.9 송구영신 예배 (Watch Night Service)
- **시점:** 12월 31일 밤 ~ 1월 1일 새벽.
- **주제:** 한 해의 회개, 새해의 결단.
- **추천 본문:** 시 90편, 애 3:22-24, 빌 3:12-14.
- **톤:** 회개와 결단의 양극. 한 해 교회 사역의 압축 회고.

### 3.10 임시 국가/사회 절기 (Civic Days)
- **3·1절(3/1), 광복절(8/15)** 등 인접 주일에 민족적 신앙 회고를 전하는 전통이 있음. 강제 아님. 시리즈 진행 중이면 생략 가능.

---

## 4. 매핑 규칙 (Date → Season Resolution)

Concierge가 `currentDate`로부터 절기를 추론할 때 다음 알고리즘을 따른다.

```pseudo
function resolveSeason(currentDate, foundation):
    # 1단계: 부동 절기(movable feast) 계산
    easter = computeEasterSunday(currentDate.year)        # 서방 교회 기준 (Computus)
    ash_wednesday = easter - 46d
    palm_sunday = easter - 7d
    pentecost = easter + 49d
    
    # 2단계: 서구 교회력 위치 결정
    if currentDate in [advent_start(year) .. christmas-1d]:
        season = "Advent (대림 N주차)"
    elif currentDate in [christmas .. epiphany_eve]:
        season = "Christmas (성탄절기)"
    elif currentDate in [ash_wednesday .. palm_sunday-1d]:
        season = "Lent (사순 N주차)"
    elif currentDate in [palm_sunday .. easter-1d]:
        season = "Holy Week (고난주간)"
    elif currentDate in [easter .. pentecost-1d]:
        season = "Easter Season (부활 후 N주)"
    elif currentDate == pentecost:
        season = "Pentecost (오순절)"
    else:
        season = "Ordinary Time (일반절기)"
    
    # 3단계: 한국 교회 고유 절기 오버레이 (서구 절기 위에 부가 라벨)
    overlays = []
    if currentDate is first_sunday_of("January"):
        overlays += "신년주일"
    if currentDate is first_sunday_of("May"):
        overlays += "어린이주일"
    if currentDate is second_sunday_of("May"):
        overlays += "어버이주일"
    if currentDate is first_sunday_of("July"):
        overlays += "맥추감사주일"
    if currentDate is last_sunday_of("October"):
        overlays += "종교개혁주일"
    if currentDate is third_sunday_of("November"):  # 교단별로 첫 주일도 가능
        overlays += "추수감사주일"
    if currentDate.month == 12 and currentDate.day == 31:
        overlays += "송구영신"
    
    # 4단계: 교파 가중치
    if foundation.denomination contains "장로교" or contains "합동" or contains "고신":
        # 종교개혁주일 weight ↑, 사순절 의식 weight ↓
    if foundation.denomination contains "감리교" or contains "성공회":
        # 교회력 전반 weight ↑
    
    return { season, overlays, key_date_offset: { until_easter, until_christmas } }
```

> 📌 **구현 메모:** 본 파일은 *규칙*이지 *코드*가 아니다. Concierge가 LLM 추론으로 위 규칙을 따라가며, 매년 부활절 날짜는 컴퓨투스(Computus) 알고리즘 또는 외부 참조표를 활용한다. 정확도가 중요한 경우 사용자에게 확인을 요청한다.

---

## 5. Concierge 헤더 출력 양식

매 진입 시 다음 헤더를 응답 최상단에 자동 표시한다.

```markdown
🗓️ **2026-05-10 (주일)** | 부활 후 다섯째 주 | _어버이주일 직후_
🪔 진행 중: 에베소서 강해 3/6 · K집사 심방 후속(5/15)
```

(절기 라벨이 없으면 "Ordinary Time"으로 표기. 사역 진행 항목이 없으면 둘째 줄 생략.)

---

## 6. 갱신 정책

- 본 파일의 **규칙(매핑 알고리즘)** 은 거의 변하지 않는다.
- 교파별 가중치, 한국 교회 절기 강조점 등은 사용자 사역 환경에 맞게 수정 가능.
- 매년 1월 초 `last_updated` 갱신, 새해 부활절 날짜 메모(선택).
