# Vendored Tool — pdf-extractor

이 디렉토리는 **벤더링된(복사된) 선택적 개발자 도구**입니다. Pastor-KR의 **29개 목회 스킬(`skills/`)이 아닙니다.**

## 무엇이고, 왜 여기 있나

**서재 팩(`data/commentary/`) 준비용 도구**입니다. 사용권 있는 주석·신학 저작이 대부분 **PDF**이므로, 서재 팩 슬롯에 넣기 전에 **PDF → 마크다운**으로 변환해야 합니다(서재 팩 규약: `data/_README.md` 슬롯 3). 이 도구가 그 변환을 담당합니다 — 구조적 하이브리드 추출 + 비전 OCR + 5단계 교정 파이프라인(신학 논문 최적화).

목회자의 매일 AI 대화에 쓰는 프롬프트 스킬이 아니라, **한 번 돌리는 오프라인 전처리 유틸리티**입니다.

## 출처 (Upstream)

- **정본(canonical)**: MS_Dev 워크스페이스의 전역 스킬 라이브러리 `mitmirsein/skills` (**비공개**) 내 `pdf-extractor` (같은 저자 MS_Dev).
- **벤더링 시점**: 2026-07-05
- **정본 버전**: pdf-extractor v2.2.0

정본이 비공개 레포라 공개 사용자는 정본에 접근할 수 없습니다. 그래서 이 공개 도구가 필요한 사람이 바로 쓸 수 있도록 여기에 **자체 복사본**을 둡니다.

## 복사에서 제외한 것

| 항목 | 이유 |
|---|---|
| `scripts/sync_engine.py` | 정본↔형제 스킬(paper-xray) **미러 동기화 도구** — 비공개 라이브러리 내부 전용이라 공개 벤더에는 불필요·부적합. |
| `__pycache__/`·`output/` | 빌드 산출물·작업 산출물(저작권 원전 텍스트 포함 가능). `output/`은 `.gitignore`로도 제외. |

## 벤더 적응 (정본과의 차이)

**지원 범위를 텍스트 레이어 / OCR된 PDF로 한정**했습니다. 스캔 이미지 PDF의 전처리(로컬 전용 `pdf-phantom-scanner` → OCR 경로 등)는 **비공개 정본에만** 두고, 공개본은 "이미 OCR된(텍스트 레이어) PDF를 입력받아 추출"로 범위를 좁혔습니다. 스캔 원본의 직접 처리는 공개 도구의 범위 밖이며, 스캔 전처리는 사용자 환경의 몫입니다.

정본과의 구체적 차이:
- `SKILL.md`·`references/gotchas.md §3`: 지원 범위를 텍스트 레이어/OCR된 PDF로 명시. Elite(Vision) 모드는 "스캔 OCR"이 아니라 텍스트 레이어 PDF의 추출 품질 폴백으로 명확화.
- 비공개 라이브러리의 형제 스킬 참조 제거(공개 환경에선 죽은 참조): `pdf-phantom-scanner`(§3 — 로컬 정본에만 유지)·`theology-chunker` 연계 절(§6 삭제·번호 재정렬)·`SKILL.md` description의 `paper-xray` 언급.

그 외 엔진 로직·스크립트는 정본과 동일합니다.

## 동기화 정책

벤더링이므로 정본(`mitmirsein/skills/pdf-extractor`)의 개선이 자동 반영되지 않습니다. 추출 엔진에 중요한 업데이트(opendataloader API 변경 대응 등)가 생기면 **유지관리자가 수동으로** 다시 가져오고, 위 "벤더 적응" 차이를 재적용합니다. 이 공개본은 정본이 아니므로, **엔진 수정은 정본에서** 하십시오.

## 사용법

전체 사용법·파이프라인은 `SKILL.md`를 보십시오. 요약:

```bash
# 0) 사전 분류 (Core/Vision 경로 판정)
uv run python scripts/preflight.py <PDF_PATH> --json

# 1) 텍스트 추출 (→ output/*.md)
uv run python scripts/extract_pdf.py --input <PDF_PATH>

# 2) 정제 + 교정 (신학 원전은 --report로 손실 감사)
uv run python scripts/post_cleaner.py output/문서.md
uv run python scripts/healer.py output/문서_cleaned.md --report
```

- **의존성**: `opendataloader-pdf`, `pypdf` (`requirements.txt` — `uv pip install -r requirements.txt`). 나머지는 stdlib.
- **주의**: 이 도구는 Python·uv 실행 환경이 필요합니다. AI에 익숙하지 않은 목회자에게는 진입 장벽이 있으니, 어려우면 md 변환만 기술적 도움을 받아 결과물을 `data/commentary/`에 넣으시면 됩니다. Claude Code 등 일부 환경은 PDF를 직접 읽기도 합니다.
- 변환한 md에는 서재 팩 규약대로 **최소 메타(저자·전통/학파·서지)**를 파일 머리에 붙여 `data/commentary/`에 두십시오(`data/_README.md` 슬롯 3).
