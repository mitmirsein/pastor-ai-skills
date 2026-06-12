# 👥 회중 페르소나 렌즈 (Congregation Personas) — v2.10 P2-7

<!-- Concierge 요약 헤더 (부트 시 이 블록만 로드) -->
> **요약**: 목회자가 직접 정의·확정한 가상 회중 3~5인. `status: confirmed`일 때 `sermon-red-team`과 `harness/sermon_audit`(L4)가 "이 설교가 각 자리에 가닿는가"를 구조화 점검한다. 미설정이면 보편 회중으로 폴백한다. 설정은 `foundation-setup` 인터뷰에서 함께.
<!-- /요약 헤더 -->

```yaml
status: unset            # unset | confirmed — 목회자 확정 필수
confirmed_on: null
```

> 🚨 **두 가지 원칙 (고정)**
> 1. **AI가 회중을 추정해 만들지 않는다.** 이 파일이 미설정이면 페르소나 시뮬레이션을 건너뛰고 보편 회중으로 폴백한다 — 상상으로 채우지 않는다.
> 2. **실존 성도를 모델로 쓰지 않는다.** 페르소나는 회중 *유형*을 대표하는 허구의 인물이다 (PII 정책의 연장). 실명·실제 개인사를 옮기지 않는다.
>
> **렌즈의 방향**: 페르소나가 설교를 *채점*하는 것이 아니라, 설교가 페르소나에게 *가닿는지*를 본다. 정죄는 '너희'가 아니라 '우리'로.

---

## 페르소나 정의 (목회자가 작성 — 아래는 작성 양식 예시)

```yaml
personas: []
# 작성 예시 (3~5인 권장):
# personas:
#   - id: tired-worker
#     label: "지친 40대 직장인 집사"
#     seat: "야근 후 겨우 나온 주일 오전, 몸은 앉아 있으나 마음은 분주함"
#     listens_for: "이번 주를 버틸 한 마디"
#     stumbles_on: "또 하나의 '더 해야 한다' 목록"
#   - id: doubting-youth
#     label: "신앙 회의기의 20대 청년"
#     seat: "교회가 답이 되는지 시험 중"
#     listens_for: "정직한 질문을 허용하는 설교"
#     stumbles_on: "증명 없이 단정하는 어조"
#   - id: first-visitor
#     label: "첫 방문 구도자"
#     seat: "용어도 동선도 낯섦"
#     listens_for: "환대, 전제 없는 설명"
#     stumbles_on: "내부자 언어(은혜/교제/구속을 설명 없이)"
```

## 사용 규약 (red-team · sermon_audit L4)

페르소나별로 두 질문만 답한다 (장황한 시뮬레이션 금지):
1. **가닿음**: 이 설교에서 {listens_for}를 받았는가? 어느 대목에서?
2. **걸림**: {stumbles_on}에 해당하는 대목이 있는가? 어디인가?
