---
name: pdf-extractor
description: >
  Extracts text-layer / already-OCR'd PDFs to high-fidelity Markdown using
  structural hybrid engines and a healing pipeline — designed for theological
  papers. Use when the user asks to extract or convert a PDF to Markdown.
  키워드: PDF 추출, 마크다운 변환
version: 2.2.0
author: MS_Dev
triggers:
  - "PDF 추출"
  - "논문 파싱"
  - "비전 추출"
  - "extract pdf"
capabilities:
  - structural_hybrid_extraction
  - elite_vision_ocr
  - intelligent_parenthesis_healing
  - footnote_separation
  - deletion_audit_report
  - original_language_protection
  - preflight_triage_routing
scripts_path: "./scripts"
status: active
---

# 📄 pdf-extractor: 고정밀 신학 논문 추출 스킬

PDF를 신학 연구에 최적화된 마크다운으로 추출하고 교정하는 전문 스킬입니다.

> 📌 **지원 범위(공개본)**: **텍스트 레이어가 있는 PDF**(born-digital 또는 이미 OCR된 PDF)만 대상으로 합니다. 스캔 이미지 PDF는 외부 OCR로 텍스트 레이어를 입힌 뒤 입력하십시오 — 스캔 원본의 직접 처리(전처리)는 이 공개 도구의 범위 밖입니다(`references/gotchas.md §3`).

## 🛠️ 주요 기능

1. **Core Mode (Structural)**: `opendataloader` 하이브리드 엔진을 사용하여 텍스트와 좌표 정보를 고속 추출합니다.
2. **Elite Mode (Vision)**: 텍스트 추출 품질이 낮을 때(독일어 깨짐·괄호 붕괴 등) 렌더된 페이지 이미지를 에이전트가 다시 읽어 보정하는 **품질 폴백**입니다 — 스캔 OCR이 아니라, 텍스트 레이어 PDF의 추출 품질을 끌어올리는 용도입니다.
3. **Healing Pipeline (v2.0)**: 추출 후 발생하는 괄호 노이즈, 각주 혼입, 깨진 외래어를 5단계 로직으로 자동 교정합니다.

---

## 🚀 사용법

### 0단계: 사전 분류 (Pre-flight Triage) — 권장 진입점
무거운 파싱 전에 첫 3페이지를 고속 스캔하여 Core / Vision 경로를 결정합니다.
```bash
# 사람용 판정 리포트
uv run python scripts/preflight.py <PDF_PATH>

# 에이전트 자동 라우팅용 JSON (stdout=순수 JSON, 진단=stderr)
uv run python scripts/preflight.py <PDF_PATH> --json
```
→ `route_code`가 `CORE`면 1단계로, `VISION`이면 3단계로 분기하십시오.

### 1단계: 텍스트 추출 (Core)
```bash
uv run python scripts/extract_pdf.py --input <PDF_PATH> --hybrid
```
> ⚠️ `--hybrid`는 별도 서버가 필요합니다. **먼저 다른 터미널에서**
> `uv run opendataloader-pdf-hybrid`를 기동하십시오 (미기동 시 "Hybrid server" 에러).
> 텍스트 PDF는 `--hybrid` 없이 일반 모드로 충분합니다. (gotchas.md 참조)

연구 인용용 페이지 마커가 필요하면 JSON의 `page number`를 사용해
`===== p.N =====` 마커가 박힌 Markdown을 생성합니다.
```bash
uv run python scripts/extract_pdf.py --input <PDF_PATH> --page-markers
```
출력은 `<파일명>_paged.md`이며, 후속 `post_cleaner.py`는 이 마커를 구조 라인으로 보존합니다.

### 2단계: 구조 정제 및 지능형 교정 (Healing)
```bash
# 기본 정제 (Spalte, Literatur 처리)
uv run python scripts/post_cleaner.py output/논문.md

# 지능형 교정 (문자 단위 괄호 매칭, 각주 분리, 외래어 파편 제거)
uv run python scripts/healer.py output/논문_cleaned.md

# 감사 모드: 삭제·재분류된 모든 span을 _healed.report.md로 기록 (학술 손실 검증 권장)
uv run python scripts/healer.py output/논문_cleaned.md --report
```

> ⚠️ healer는 비가역 삭제를 수행합니다. 신학 원전(원어·인용·각주)이 섞인 문서는
> **`--report`로 감사 로그를 생성하여 손실분을 반드시 확인**하십시오.

### 3단계: 비전 기반 대안 추출 (Elite)
텍스트 추출 품질이 낮을 때(독일어 깨짐, 괄호 붕괴 등) 이미지 디렉토리를 대상으로 실행합니다.
두 스크립트는 OCR을 직접 하지 않고 **에이전트 작성 계약(입력/출력 경로)을 명시**합니다.
```bash
# 마크다운 산출 경로·계약 출력 → 에이전트가 _vision_raw.md 작성
uv run python scripts/vision_extractor.py output/논문_images/

# 시맨틱 JSON 골격 생성 → 에이전트가 _vision.json 채움
uv run python scripts/vision_to_json.py output/논문_images/
```

---

## 🏥 Healer v2.1 파이프라인 (5-Pass)

| Pass | 대상 | 조치 |
| :---: | :--- | :--- |
| 1 | 페이지 잔해 | 단독 숫자(페이지 번호), 반복 헤더 제거 |
| 2 | 각주 분리 | 본문에 섞인 서지 파편을 `> [각주]` 블록으로 격리 |
| 3 | 외래어 잔해 | 역전(`s i e h t o n o M`) 또는 깨진 라틴 자음 파편 제거 |
| 4 | 괄호 정규화 | **문자 단위 스택 매칭**으로 고아 `(`만 정교하게 삭제 |
| 5 | 정규화 | 다중 공백, 연속 빈 줄, 문단 끝 공백 정리 |

---

> ℹ️ 이 디렉토리는 비공개 정본 라이브러리에서 **벤더링된 복사본**입니다(정본·동기화 정책: `VENDOR.md`). 엔진 수정은 정본에서 하십시오.

## 🔧 의존성
- `opendataloader-pdf`, `pypdf` — `uv pip install -r requirements.txt`
- 나머지(healer·post_cleaner·vision_*·tests)는 stdlib만 사용.
- Intel Mac은 PyTorch 충돌 가능 — `gotchas.md §2` 참조.
- `extract_pdf.py`의 `--hybrid`는 API/CLI 기본값이 **False로 일치**(서버 선행 필요).
- Intel Mac은 PyTorch 충돌 가능 — `gotchas.md §2` 참조.
- `extract_pdf.py`의 `--hybrid`는 API/CLI 기본값이 **False로 일치**(서버 선행 필요).

## 📁 디렉토리 구조
- `scripts/preflight.py`: 사전 분류 라우터 (Core/Vision 판정, `--json`)
- `scripts/extract_pdf.py`: 메인 추출 엔진
- `scripts/post_cleaner.py`: 구조 정제기
- `scripts/healer.py`: 지능형 교정기 (v2.1, `--report` 감사)
- `scripts/vision_extractor.py`: 비전 추출 컨트롤러 (마크다운 계약)
- `scripts/vision_to_json.py`: 비전 시맨틱 JSON 골격 생성기
- `tests/test_healer.py`: healer 회귀·멱등·불변식 테스트 (`python3 -m unittest discover tests`)
- `references/gotchas.md`: 함정·안티패턴 가이드
