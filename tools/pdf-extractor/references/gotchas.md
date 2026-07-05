# 📄 PDF Extractor: Gotchas & Anti-Patterns

신학 논문 PDF 추출 시 에이전트가 반드시 확인해야 할 주의사항입니다.

---

## 1. Hybrid 모드 서버 미기동 오류

Hybrid(Docling) 모드 사용 시 별도 서버가 필요합니다.

```bash
# 터미널 A: 서버 기동
uv run opendataloader-pdf-hybrid

# 터미널 B: 추출 실행
uv run python scripts/extract_pdf.py --input paper.pdf --hybrid
```

`"Hybrid server"` 관련 에러 발생 시 → 서버가 구동되지 않은 것입니다.

---

## 2. Intel Mac (2017 iMac) 호환성

- **문제**: PyTorch 의존성이 Intel Mac 환경에서 충돌할 수 있음
- **해결**: CPU 전용 버전으로 설치하거나, 일반 모드(`--hybrid` 없이)로 실행

---

## 3. 지원 범위 — 텍스트 레이어 / OCR된 PDF만

이 공개본은 **텍스트 레이어가 있는 PDF**(born-digital 또는 **이미 OCR된** PDF)를 대상으로 합니다.

- **텍스트 PDF**: 일반 모드로 충분(Hybrid 불필요).
- **스캔 이미지 PDF**: 먼저 **외부 OCR 도구(ABBYY 등)로 텍스트 레이어를 입힌 뒤** 입력하십시오. **원본 스캔 이미지의 직접 처리는 이 공개 도구의 범위 밖**입니다(스캔 전처리는 사용자 환경의 몫).
- **확인 방법**: Adobe Acrobat·Preview에서 텍스트 선택이 되면 텍스트 레이어가 있는 PDF입니다.

---

## 4. Spalte(단 번호) 누락 문제

독일어 신학 사전(TRE, RGG, RGG4)의 단(Spalte) 번호는 종종 추출 시 노이즈로 처리됩니다.
- `post_cleaner.py`의 Spalte 패턴이 자동 복원하지만, 누락된 경우 수동 확인 필요
- 패턴: `Sp. 123` 형태

---

## 5. 출력 파일명 불일치

`opendataloader-pdf`는 버전에 따라 출력 파일명이 다를 수 있습니다.
- 기대: `{입력파일명}.md`
- 실제 확인: `extract_pdf.py`가 자동으로 출력 디렉토리를 스캔하여 대체 경로를 찾습니다.

---

## 6. 한글 PDF 추출기 선택 (pypdf 자간 분해 함정)

한글 학술 PDF는 추출기에 따라 텍스트 품질이 크게 갈린다.

- **pypdf**: 한글 자간을 공백으로 분해(`오 늘 날`) → 띄어쓰기 소실, 사실상 복구 불가
- **poppler `pdftotext -layout`**: 한글 띄어쓰기를 정상 보존. ★권장
- **opendataloader**: Intel Mac에서 PyTorch 충돌(§2), 미설치도 흔함

`extract_pdf.py`는 opendataloader 부재/실패 시 **자동으로 poppler 폴백**한다(별도 조치 불필요). `preflight.py`가 한글 글자단위 분리를 감지하면 `route_code: CORE` + `extractor_hint: poppler`를 반환하므로, 그때는 poppler 경로로 추출하면 된다.

---
*Created by MS_Dev (2026-04-17)*
