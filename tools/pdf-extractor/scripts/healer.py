#!/usr/bin/env python3
"""
healer.py — PDF 추출 마크다운 지능형 교정 엔진 v2.1
====================================================

opendataloader로 추출된 _cleaned.md 파일의 잔류 노이즈를 제거합니다.

5단계 교정 파이프라인:
  Pass 1: [구조] 페이지 잔해 제거 — 잔류 페이지 번호, 헤더 반복 제거
  Pass 2: [구조] 각주 분리 — 본문에 혼입된 각주를 식별하여 블록 인용 처리
  Pass 3: [텍스트] 외래어 잔해 제거 — 역전·파편화된 라틴/독일어 파편 제거
  Pass 4: [텍스트] 괄호 정규화 — 문자 단위 매칭으로 고아 여는 괄호만 제거
  Pass 5: [정규화] 공백·문단 정리 — 다중 공백, 빈 줄 정규화

사용법:
  python healer.py <input_cleaned_md> [output_path]
  python healer.py <input_cleaned_md> --report
  # 출력 미지정 시: 같은 디렉토리에 {이름}_healed.md 생성
  # --report 지정 시: {이름}_healed.report.md 에 삭제 감사 로그 생성

원칙:
  - 한국어 본문은 절대 변경하지 않음 (삭제만, 추가 금지)
  - 복원 불가한 원어는 제거하되 문맥은 보존
  - 멱등성: 두 번 실행해도 동일한 결과
  - 보수적 접근: 의심스러우면 원본 유지
  - 감사 가능성: --report 로 모든 삭제 span을 추적 (학술 텍스트 손실 검증용)
"""

import argparse
import re
import sys
from pathlib import Path


# ─── 한국어 조사/어미 목록 ───
# (빈 괄호 뒤에 이것들이 오면 괄호는 고아 확정)
KOREAN_PARTICLES = (
    '으로서의', '으로써', '으로서', '에서는', '에게서', '로서의',
    '으로는', '에서도', '으로의',
    '으로', '에서', '에게', '라고', '라면', '이며', '이라',
    '이고', '지만', '한다', '했다', '된다', '되다',
    '은', '는', '이', '가', '을', '를', '의', '에',
    '와', '과', '로', '도', '면', '다', '고', '라', '며',
)

# 각주 식별용 서지 마커
BIBLIO_MARKERS = (
    '《', '》', '역,', '역.', ' 역 ', '서울:', '서울,',
    '쇄', '이하', '참조', '출판', '기독교서회', '신학연구소',
    '같은 책', '같은 저자',
)

# ─── Pass 3 원어 보호 화이트리스트 ───
# 신학 논문에서 정상적으로 등장하는 약어·총서·언어 태그. Pass 3 의 깨짐
# 판정(_is_likely_garbled)이 이들을 절대 삭제하지 않도록 보호한다.
# (모음 없는 대문자 약어가 OCR 잔해로 오판되어 삭제되던 문제 차단)
PROTECTED_TOKENS = {
    # 신학 사전·총서·학술지 시글라
    'TRE', 'RGG', 'RGG4', 'EKL', 'LThK', 'HWP', 'HDG', 'TDNT', 'TWNT',
    'TWAT', 'ABD', 'NBL', 'WUNT', 'BZAW', 'BZNW', 'FRLANT', 'SBL',
    'SBLDS', 'JBL', 'JSOT', 'JSNT', 'ZAW', 'ZNW', 'ZThK', 'ZTK',
    'NTS', 'VT', 'CBQ', 'HTR', 'ThLZ', 'ThR', 'EvTh', 'KuD', 'NPNF',
    'PG', 'PL', 'CCSL', 'CSEL', 'GCS', 'SC', 'CChr',
    # 칼 바르트 등 표준 약칭
    'KD', 'CD', 'GA', 'WA', 'LW', 'CO', 'OS', 'CR',
    # 성서 본문·역본
    'LXX', 'MT', 'BHS', 'NA', 'NA28', 'UBS', 'KJV', 'ESV', 'NRSV',
    'NIV', 'RSV', 'NT', 'OT', 'AT',
    # 라틴/독일어 학술 약어
    'cf', 'cf.', 'vgl', 'vgl.', 'ibid', 'ibid.', 'op', 'cit',
    'et', 'al', 'al.', 'ed', 'ed.', 'eds', 'eds.', 'trans', 'tr',
    'Hrsg', 'Hg', 'Bd', 'Bde', 'Sp', 'Aufl', 'Diss', 'Festschrift',
    'ff', 'ff.', 'f.', 'pp', 'pp.', 'vol', 'vols', 'no', 'nr',
    'idem', 'eadem', 'passim', 'sic', 'cap', 'col', 'fol',
    # 언어 태그
    'he', 'gr', 'lat', 'aram', 'heb', 'grc',
}
_PROTECTED_LOWER = {t.lower().rstrip('.') for t in PROTECTED_TOKENS}


def _is_protected(word: str) -> bool:
    """화이트리스트(또는 그 단순 활용형) 토큰이면 True — Pass 3 삭제 면제."""
    if word in PROTECTED_TOKENS:
        return True
    return word.lower().rstrip('.') in _PROTECTED_LOWER


# ────────────────────── 감사 로깅 ──────────────────────

class Audit:
    """삭제·재분류 span을 기록하는 감사 수집기.

    학술 텍스트는 침묵형 손상이 치명적이므로, 모든 비가역 변형을
    원문·위치와 함께 기록하여 사용자가 손실분을 검증할 수 있게 한다.
    enabled=False 면 모든 record 호출이 no-op (성능·기본 동작 보존).
    """

    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.records: list[dict] = []

    def record(self, pass_name: str, kind: str, removed: str,
               line_no=None, context: str = "") -> None:
        if not self.enabled:
            return
        removed = removed if removed is not None else ""
        if removed.strip() == "" and kind != "line-drop":
            return  # 순수 공백 변형은 감사 대상 아님
        self.records.append({
            "pass": pass_name,
            "kind": kind,
            "line_no": line_no,
            "removed": removed,
            "context": context.strip()[:160],
        })

    def to_markdown(self, src_name: str) -> str:
        lines = [
            f"# 🧾 Healer 삭제 감사 리포트",
            "",
            f"- 원본: `{src_name}`",
            f"- 총 변형 건수: **{len(self.records)}**",
            "",
            "> 이 리포트는 healer가 **제거하거나 재분류한 모든 span**을 기록합니다.",
            "> 학술 원문(원어·인용·각주)이 의도치 않게 손실되지 않았는지 검증하십시오.",
            "",
        ]
        if not self.records:
            lines.append("_변형 없음 (clean)._")
            return "\n".join(lines) + "\n"

        by_pass: dict[str, list[dict]] = {}
        for r in self.records:
            by_pass.setdefault(r["pass"], []).append(r)

        for pass_name, recs in by_pass.items():
            lines.append(f"## {pass_name} ({len(recs)}건)")
            lines.append("")
            lines.append("| 줄 | 유형 | 제거/변형된 내용 | 문맥 |")
            lines.append("|---:|:---|:---|:---|")
            for r in recs:
                ln = r["line_no"] if r["line_no"] is not None else "—"
                removed = r["removed"].replace("|", "\\|").replace("\n", "⏎")
                ctx = r["context"].replace("|", "\\|").replace("\n", "⏎")
                if len(removed) > 80:
                    removed = removed[:77] + "…"
                lines.append(f"| {ln} | {r['kind']} | `{removed}` | {ctx} |")
            lines.append("")
        return "\n".join(lines) + "\n"


# ────────────────────── Pass 1 ──────────────────────

def pass1_page_artifacts(text: str, audit: Audit | None = None) -> str:
    """Pass 1: 페이지 잔해 제거

    - 단독 숫자 줄 (페이지 번호)
    - 반복 헤더 (논문 제목 + 페이지 마커)
    - 인라인 페이지 마커 (9－1, 9 - 1 등)
    """
    a = audit or Audit(False)
    lines = text.split('\n')
    cleaned = []
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()

        # 단독 숫자 줄 (1~3자리): 페이지 번호
        if re.match(r'^\d{1,3}$', stripped):
            a.record("Pass 1 페이지 잔해", "line-drop", stripped,
                     line_no=idx, context="단독 숫자(페이지 번호)")
            continue

        # 페이지 상단 헤더 잔류 패턴
        if re.match(r'^.{5,50}\s+\d+\s*[－\-]\s*\d+\s*$', stripped):
            a.record("Pass 1 페이지 잔해", "line-drop", stripped,
                     line_no=idx, context="반복 헤더 패턴")
            continue

        # 인라인 페이지 마커 제거
        new_line = re.sub(r'\d+\s*[－]\s*\d+', '', line)
        if new_line != line and a.enabled:
            for m in re.finditer(r'\d+\s*[－]\s*\d+', line):
                a.record("Pass 1 페이지 잔해", "inline", m.group(0),
                         line_no=idx, context=line)
        line = new_line

        cleaned.append(line)
    return '\n'.join(cleaned)


# ────────────────────── Pass 2 ──────────────────────

def pass2_footnote_separation(text: str, audit: Audit | None = None) -> str:
    """Pass 2: 각주 분리 — 본문에 혼입된 각주를 블록 인용으로 처리

    식별 기준:
    - 줄이 `- N 대문자약어` 또는 `N 대문자약어`로 시작
    - 서지 마커(《》, 역, 서울, 쇄 등) 포함
    - 한국어 문장 종결 어미로 끝나지 않음 (불완전한 서지 파편)
    """
    a = audit or Audit(False)
    lines = text.split('\n')
    result = []

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped:
            result.append(line)
            continue

        is_footnote = False

        # 패턴 1: `- N 대문자` (대시 시작)
        if re.match(r'^-\s*\d+\s+[A-Z]', stripped):
            has_biblio = any(m in stripped for m in BIBLIO_MARKERS)
            # 완전한 한국어 문장이 아니라면 각주로 간주
            ends_with_sentence = bool(re.search(r'[다습까요][\.\s]*$', stripped))
            if has_biblio or not ends_with_sentence:
                is_footnote = True

        # 패턴 2: `N 대문자약어,` (숫자+대문자+구두점)
        elif re.match(r'^\d+\s+[A-Z]{1,4}[\s,《]', stripped):
            has_biblio = any(m in stripped for m in BIBLIO_MARKERS)
            if has_biblio:
                is_footnote = True

        if is_footnote:
            a.record("Pass 2 각주 분리", "reclassify→각주", stripped,
                     line_no=idx, context="본문→ > [각주] 블록으로 재분류")
            result.append(f'\n> [각주] {stripped.lstrip("- ")}')
        else:
            result.append(line)

    return '\n'.join(result)


# ────────────────────── Pass 3 ──────────────────────

def _has_vowels(word: str) -> bool:
    """라틴어/독일어 단어에 모음이 있는지 확인"""
    return bool(re.search(r'[aeiouAEIOU]', word))


def _is_likely_garbled(word: str) -> bool:
    """라틴 문자열이 깨진 텍스트인지 판별

    깨진 텍스트 특징:
    - 모음 없는 자음 연쇄 (예: BL, DPCa, rSG, dKh)
    - 비정상적 대소문자 혼합 (예: VdSudG1)
    - 매우 짧고 의미 없는 약어

    보존 대상:
    - 의미 있는 독일어 (예: Perichorose, innertrinitarische, Filioque)
    - 알려진 학술 약어 (예: TRE, SBL)
    """
    # 너무 짧으면 판단 보류 (다른 pass에서 처리)
    if len(word) <= 1:
        return False

    # 화이트리스트(학술 약어·총서·언어 태그) → 절대 깨짐 아님 (원어 보호)
    if _is_protected(word):
        return False

    # 숫자 포함 → 깨진 텍스트
    if re.search(r'\d', word):
        return True

    # 모음 비율이 극단적으로 낮으면 깨진 텍스트.
    # 단, 전부 대문자인 약어(TRE, RGG, SBL 등)는 정상 시글라로 보존한다
    # — 모음 없는 대문자 약어를 잔해로 오판해 삭제하던 결함 차단.
    vowel_count = sum(1 for c in word if c.lower() in 'aeiou')
    if len(word) >= 3 and vowel_count == 0 and not word.isupper():
        return True

    # 5자 이하인데 대소문자가 비정상적으로 섞임 (예: DPCa, VdSu)
    if len(word) <= 5:
        uppers = sum(1 for c in word if c.isupper())
        lowers = sum(1 for c in word if c.islower())
        if uppers >= 2 and lowers >= 1 and uppers > lowers:
            return True

    return False


def pass3_garbled_text(text: str, audit: Audit | None = None) -> str:
    """Pass 3: 외래어 잔해 제거

    3-a. 공백 분리된 단일 라틴 문자 시퀀스 (역전/파편 텍스트)
    3-b. 괄호 안의 1~3자 라틴 파편 (닫는 괄호 없는 경우)
    3-c. 한국어 사이에 끼인 깨진 라틴 파편
    """
    a = audit or Audit(False)

    def _sub_logged(pattern, repl, s, kind, flags=0):
        if not a.enabled:
            return re.sub(pattern, repl, s, flags=flags)

        def _wrap(m):
            replacement = repl(m) if callable(repl) else m.expand(repl)
            if m.group(0) != replacement:
                # 위치를 줄 번호로 환산
                line_no = s.count('\n', 0, m.start()) + 1
                ctx_start = s.rfind('\n', 0, m.start()) + 1
                ctx_end = s.find('\n', m.end())
                ctx = s[ctx_start:ctx_end if ctx_end != -1 else None]
                a.record("Pass 3 외래어 잔해", kind, m.group(0),
                         line_no=line_no, context=ctx)
            return replacement

        return re.sub(pattern, _wrap, s, flags=flags)

    # 3-a. 공백으로 분리된 단일 라틴 문자 시퀀스 (4자 이상)
    # 예: `s i e h t o n o M`, `i d n i`
    # 가드: 자간 띄운 약어/시글라(전부 대문자: `T R E`)나 정·역방향이
    #       화이트리스트면 정상 표기로 보고 보존한다.
    def _strip_spaced_run(m):
        run = m.group(0)
        letters = run.replace(' ', '')
        if letters.isupper():               # 자간 띄운 대문자 약어/시글라
            return run
        if _is_protected(letters) or _is_protected(letters[::-1]):
            return run
        return ''

    text = _sub_logged(r'(?:[a-zA-Z] ){3,}[a-zA-Z]', _strip_spaced_run, text,
                        "3-a 자간분리 파편")

    # 3-b. 괄호 안의 1~3자 라틴 파편 (뒤에 한국어가 오는 경우)
    # 예: `(i 을`, `(C 을`, `(n 교의학`, `(m 그리고`
    # 가드: `(NT `, `(LXX ` 등 화이트리스트 약어는 정상 인용이므로 보존.
    def _strip_paren_frag(m):
        tok = re.sub(r'^\(\s*|\s+$', '', m.group(0))
        return m.group(0) if _is_protected(tok) else ''

    text = _sub_logged(r'\(\s*[a-zA-Z]{1,3}\s+(?=[가-힣"\'《])',
                        _strip_paren_frag, text, "3-b 괄호내 파편")

    # 3-c. 따옴표 뒤 괄호+파편 제거
    # 예: `"양태론적 기독론"( i 을` → `"양태론적 기독론" 을`
    def _strip_quote_paren_frag(m):
        tok = re.sub(r'^"\s*\(\s*|\s+$', '', m.group(0))
        return m.group(0) if _is_protected(tok) else '" '

    text = _sub_logged(r'"\s*\(\s*[a-zA-Z]{1,3}\s+', _strip_quote_paren_frag,
                        text, "3-c 따옴표뒤 파편")

    # 3-d. 한국어 사이에 끼인 깨진 라틴 파편 제거
    # 예: `...계시"i d n i (rSG 로...` → `...계시" 로...`
    def _replace_inline_garbled(match):
        word = match.group(1)
        if _is_likely_garbled(word):
            return ' '
        return match.group(0)

    # 한국어/구두점 사이의 라틴 파편 (2~8자)
    text = _sub_logged(
        r'(?<=[가-힣"\s])([a-zA-Z]{2,8})(?=[\s,.\)가-힣])',
        _replace_inline_garbled,
        text,
        "3-d 인라인 깨진 파편",
    )

    return text


# ────────────────────── Pass 4 ──────────────────────

def pass4_parenthesis_normalization(text: str, audit: Audit | None = None) -> str:
    """Pass 4: 괄호 정규화 — 문자 단위 매칭으로 고아 괄호만 제거

    알고리즘:
    1. 각 줄에서 여는 괄호 `(`의 위치를 추적
    2. 닫는 괄호 `)`를 만나면 가장 최근 여는 괄호와 매칭
    3. 매칭 안 된 여는 괄호 = 고아 괄호
    4. 고아 괄호 뒤에 오는 내용에 따라 처리:
       - 한국어 조사 → 괄호+공백 제거 (조사를 앞 단어에 붙임)
       - 《 → 괄호 제거
       - 줄 끝 → 괄호 제거
       - 그 외 → 원본 유지 (보수적 처리)
    """
    a = audit or Audit(False)
    lines = text.split('\n')
    result = []

    for idx, line in enumerate(lines, start=1):
        # 여는 괄호 위치 추적
        open_positions = []
        for i, ch in enumerate(line):
            if ch == '(':
                open_positions.append(i)
            elif ch == ')':
                if open_positions:
                    open_positions.pop()  # 매칭됨

        # open_positions에 남은 것들이 고아 여는 괄호
        if not open_positions:
            result.append(line)
            continue

        # 뒤에서부터 처리 (인덱스 안전성)
        chars = list(line)
        for pos in reversed(open_positions):
            after_raw = line[pos + 1:]
            after = after_raw.lstrip()
            space_len = len(after_raw) - len(after)

            handled = False

            # Case A: 한국어 조사가 바로 뒤에 → 괄호+공백 제거
            for p in KOREAN_PARTICLES:
                if after.startswith(p):
                    # `(` + 공백들 제거, 조사는 유지
                    end = pos + 1 + space_len
                    for j in range(pos, end):
                        chars[j] = ''
                    a.record("Pass 4 괄호 정규화", "고아( 제거(조사)",
                             line[pos:end], line_no=idx, context=line)
                    handled = True
                    break

            if handled:
                continue

            # Case B: 《 (책 제목) 앞 → 괄호+공백 제거
            if after.startswith('《'):
                end = pos + 1 + space_len
                for j in range(pos, end):
                    chars[j] = ''
                a.record("Pass 4 괄호 정규화", "고아( 제거(《)",
                         line[pos:end], line_no=idx, context=line)
                continue

            # Case C: 줄 끝의 고아 괄호 → 제거
            if not after or after.isspace():
                chars[pos] = ''
                a.record("Pass 4 괄호 정규화", "고아( 제거(줄끝)",
                         '(', line_no=idx, context=line)
                continue

            # Case D: 한국어 텍스트가 바로 뒤에 (조사 외) → 괄호+공백 제거
            if after and re.match(r'^[가-힣]', after):
                end = pos + 1 + space_len
                for j in range(pos, end):
                    chars[j] = ''
                a.record("Pass 4 괄호 정규화", "고아( 제거(한국어)",
                         line[pos:end], line_no=idx, context=line)
                continue

            # Case E: 그 외 → 보수적으로 원본 유지
            # (의미 있는 괄호일 수 있으므로 건드리지 않음)

        line = ''.join(chars)

        # 빈 괄호 최종 정리
        if a.enabled:
            for m in re.finditer(r'\(\s*\)', line):
                a.record("Pass 4 괄호 정규화", "빈 괄호 제거",
                         m.group(0), line_no=idx, context=line)
        line = re.sub(r'\(\s*\)', '', line)

        result.append(line)

    return '\n'.join(result)


# ────────────────────── Pass 5 ──────────────────────

def pass5_text_normalization(text: str, audit: Audit | None = None) -> str:
    """Pass 5: 공백 및 문단 정규화

    5-a. 다중 공백 정리 (블록 인용 내부 제외)
    5-b. 연속 빈 줄 정리 (최대 2줄)
    5-c. 줄 끝 공백 제거
    5-d. 고아 닫는 괄호를 이전 문맥에 병합

    주: 5-a~5-c 는 순수 공백 정규화(비손실)이므로 감사 대상에서 제외.
        5-d 만 의미론적 변형이므로 기록한다.
    """
    a = audit or Audit(False)
    lines = text.split('\n')
    normalized = []
    for line in lines:
        # 블록 인용 내부는 건드리지 않음
        if not line.startswith('>'):
            line = re.sub(r' {2,}', ' ', line)
        normalized.append(line)
    text = '\n'.join(normalized)

    # 3줄 이상 연속 빈 줄 → 2줄로
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    # 줄 끝 공백 제거
    text = re.sub(r' +\n', '\n', text)

    # 고아 닫는 괄호로 시작하는 줄: 이전 줄에 붙이기
    # 예: `...한다\n)\n` → `...한다)\n`
    if a.enabled:
        for m in re.finditer(r'(?<=\S)\n\s*\)\s*(?=\n)', text):
            line_no = text.count('\n', 0, m.start()) + 1
            a.record("Pass 5 텍스트 정규화", "고아) 이전줄 병합",
                     m.group(0), line_no=line_no, context="줄바꿈 ) → 앞 줄에 병합")
    text = re.sub(r'(?<=\S)\n\s*\)\s*(?=\n)', ')', text)

    return text


# ────────────────────── 파이프라인 ──────────────────────

def heal(input_path: str, output_path: str = None,
         report: bool = False) -> str:
    """메인 교정 파이프라인 실행

    Args:
        input_path: _cleaned.md 파일 경로
        output_path: 출력 경로 (미지정 시 _healed.md)
        report: True 면 {출력}.report.md 에 삭제 감사 로그 생성

    Returns:
        출력 파일 경로
    """
    path = Path(input_path)
    if not path.exists():
        print(f"❌ 파일을 찾을 수 없습니다: {input_path}")
        sys.exit(1)

    if output_path is None:
        stem = path.stem.replace('_cleaned', '')
        output_path = str(path.parent / f"{stem}_healed.md")

    text = path.read_text(encoding='utf-8')
    original_len = len(text)

    audit = Audit(enabled=report)

    print(f"🏥 교정 시작: {path.name}")
    print(f"   원본 크기: {original_len:,} bytes")
    if report:
        print(f"   🧾 감사 모드 활성 (--report)")
    print()

    # Pass 1: 페이지 잔해 제거
    text = pass1_page_artifacts(text, audit)
    d1 = len(text)
    print(f"  ✅ Pass 1 [페이지 잔해 제거] → {d1:,} bytes (Δ {d1 - original_len:+,})")

    # Pass 2: 각주 분리
    text = pass2_footnote_separation(text, audit)
    d2 = len(text)
    print(f"  ✅ Pass 2 [각주 분리]       → {d2:,} bytes (Δ {d2 - d1:+,})")

    # Pass 3: 외래어 잔해 제거
    text = pass3_garbled_text(text, audit)
    d3 = len(text)
    print(f"  ✅ Pass 3 [외래어 잔해 제거] → {d3:,} bytes (Δ {d3 - d2:+,})")

    # Pass 4: 괄호 정규화
    text = pass4_parenthesis_normalization(text, audit)
    d4 = len(text)
    print(f"  ✅ Pass 4 [괄호 정규화]     → {d4:,} bytes (Δ {d4 - d3:+,})")

    # Pass 5: 텍스트 정규화
    text = pass5_text_normalization(text, audit)
    d5 = len(text)
    print(f"  ✅ Pass 5 [텍스트 정규화]   → {d5:,} bytes (Δ {d5 - d4:+,})")

    # 저장
    out = Path(output_path)
    out.write_text(text, encoding='utf-8')

    delta = d5 - original_len
    pct = (delta / original_len) * 100 if original_len else 0
    print()
    print(f"✨ 교정 완료: {out.name}")
    print(f"   최종 크기: {d5:,} bytes (Δ {delta:+,}, {pct:+.1f}%)")
    print(f"   출력 경로: {out}")

    if report:
        report_path = out.with_suffix('').with_suffix('.report.md')
        report_path.write_text(audit.to_markdown(path.name), encoding='utf-8')
        print(f"   🧾 감사 리포트: {report_path} ({len(audit.records)}건 변형)")

    return str(out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="PDF 추출 마크다운 지능형 교정 엔진 (5-Pass)",
        epilog="예시:\n  python healer.py output/논문_cleaned.md\n"
               "  python healer.py output/논문_cleaned.md --report",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", help="입력 _cleaned.md 파일 경로")
    parser.add_argument("output", nargs="?", default=None,
                        help="출력 경로 (미지정 시 _healed.md)")
    parser.add_argument("--report", action="store_true",
                        help="삭제 감사 로그(_healed.report.md) 생성 — 학술 손실 검증용")

    args = parser.parse_args()
    heal(args.input, args.output, report=args.report)
