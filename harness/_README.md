# harness/ — 품질 보증 도구 (Quality Assurance)

> **Pastor-KR v2.7 (Audit Gate & Journal Lint)**에서 도입된 디렉토리입니다.

---

## 1. harness/의 존재 이유

v2.5는 사역 자산을 **누적**시킨다. v2.6(Tier 2)은 자산을 **꺼내 쓴다**. v2.7(Tier 3 / 이 디렉토리)은 자산이 **신뢰할 만한가**를 검증한다.

`harness/`는 Pastor-KR에서 **사역 자산의 발행을 차단할 권한을 갖는 유일한 위계**입니다.

---

## 2. skills/와의 책임 경계

| 측면 | `skills/` | `harness/` |
|---|---|---|
| 호출자 | 목회자 (사용자) | Concierge 또는 사용자 직접 요청 |
| 출력 | 목회 결과물 (설교·교안·서신 등) | 검증 리포트 (점수·위반 목록) |
| 빈도 | 주중 수시 | 발행 전 1회 / 주 1회 |
| 페르소나 | 동역자 | 감사관 (감독자) |
| 자산 수정 | 사용자 요청 시 생성/저장 | 사용자 동의 후만 수정 (journal_lint) |

---

## 3. skills/05_meta_tools/와의 책임 경계

`skills/05_meta_tools/`(Tier 1·2)와도 다릅니다.

| 도구 | 출력 성격 | 권한 |
|---|---|---|
| `skills/05_meta_tools/journal-show.md` | 메모리 **현황** 가시화 (대시보드) | 읽기 전용 |
| `harness/journal_lint.md` | 메모리 **위생** 검증 (위반 목록) | 사용자 동의 후 수정 가능 |

- `journal-show`는 "지금 어떻게 생겼는지" 보여준다 — 정상 항목 위주.
- `journal_lint`는 "뭐가 잘못됐는지" 찾는다 — 위반·표류·만료 위주.
- 사용자가 "메모리 점검"이라고만 했을 때는 **lint 우선** (위생 확인이 더 중요).

---

## 4. 운용 정책

### 4.1 sermon_audit

- **발행 직전 1회** 호출이 원칙.
- 80점 이상(PASS)이면 발행 진행, 60–79점(WARN)이면 사용자 동의, 0–59점(FAIL)이면 발행 차단.
- 저장 위치: `outputs/sermons/{passage_id}/audit_v{NN}_{date}.md` (lineage 인접).
- **AI 자가 감사의 한계를 항상 디스클레이머로 명시**합니다. 최종 결정은 목회자에게 있습니다.

### 4.2 journal_lint

- **주 1회** 실행 권장 (월요일 아침).
- 식별만 합니다. 자동 수정은 사용자 명시 동의 후에만 실행.
- PII 위반 보고 시 원문 노출 금지 — 마스킹 표기만 사용합니다.
- 저장 위치: `outputs/{date}/_audit/journal_lint_{date}.md`.

---

## 5. 도구 목록

| 파일 | 역할 |
|---|---|
| `sermon_audit.md` | 발행 전 사역물 5렌즈 포렌식 검수 (80점 fail-fast) |
| `journal_lint.md` | `pastor_journal.md` 스키마·PII·표류 점검 |

---

## 6. 비범위

harness/는 다음을 수행하지 않습니다.

- ❌ 외부 검증기/API (Strong's Concordance, BibleGateway 등) 연동
- ❌ 점수 학습 / RL 피드백 루프
- ❌ `outputs/sermons/` manifest 무결성 점검 (별도 manifest_lint 도구 — 미구현)
- ❌ 자동 git commit / 발행 차단 hook (Claude Code hook 통합) — v3.0 이후 검토
