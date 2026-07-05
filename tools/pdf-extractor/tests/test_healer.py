#!/usr/bin/env python3
"""
healer.py 회귀·멱등·불변식 테스트
=================================

실행:
  cd .skills/pdf-extractor
  python3 -m unittest discover tests -v

의존성: 표준 라이브러리만 사용 (healer.py 는 re/pathlib 만 의존).
"""

import sys
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

import healer  # noqa: E402


def _count_hangul(s: str) -> int:
    return sum(1 for c in s if '가' <= c <= '힣')


# ─────────────── Pass 단위 골든 테스트 (작은 결정적 입력) ───────────────

class TestPass1(unittest.TestCase):
    def test_drops_standalone_page_number(self):
        self.assertEqual(healer.pass1_page_artifacts("본문\n42\n다음"), "본문\n다음")

    def test_keeps_long_number(self):
        # 4자리 이상은 페이지 번호로 보지 않음 (연도 등 보존)
        self.assertEqual(healer.pass1_page_artifacts("2026"), "2026")

    def test_removes_inline_page_marker(self):
        self.assertEqual(healer.pass1_page_artifacts("앞 12－3 뒤"), "앞  뒤")

    def test_preserves_research_page_marker(self):
        src = "첫 문장.\n\n===== p.2 =====\n\n둘째 문장."
        self.assertIn("===== p.2 =====", healer.pass1_page_artifacts(src))


class TestPass2(unittest.TestCase):
    def test_reclassifies_bibliographic_footnote(self):
        src = "- 12 K. Koch, 서울: 기독교서회, 2020."
        out = healer.pass2_footnote_separation(src)
        self.assertIn("> [각주]", out)

    def test_keeps_normal_korean_sentence(self):
        src = "이것은 평범한 한국어 본문 문장이다."
        self.assertEqual(healer.pass2_footnote_separation(src), src)


class TestPass3(unittest.TestCase):
    def test_removes_spaced_letter_fragment(self):
        # `s i e h t` 같은 자간분리 역전 파편
        out = healer.pass3_garbled_text("계시 s i e h t 그리고")
        self.assertNotIn("s i e h t", out)

    def test_hangul_never_removed(self):
        """불변식: Pass 3 는 한글을 절대 삭제하지 않는다 (학술 본문 보호)."""
        samples = [
            "삼위일체 s i e h t o n o M 페리코레시스",
            '"양태론적 기독론"( i 을 가지고',
            "계시\"i d n i (rSG 로 본다",
        ]
        for s in samples:
            with self.subTest(s=s):
                self.assertEqual(
                    _count_hangul(healer.pass3_garbled_text(s)),
                    _count_hangul(s),
                    "Pass 3 가 한글을 삭제함 — 원어 보호 위반",
                )


class TestPass3Conservatism(unittest.TestCase):
    """P2: 학술 약어·시글라가 깨진 텍스트로 오판되어 삭제되지 않아야 한다."""

    def test_acronyms_not_garbled(self):
        for tok in ("TRE", "RGG", "SBL", "LXX", "KD", "ZAW", "NT"):
            with self.subTest(tok=tok):
                self.assertFalse(
                    healer._is_likely_garbled(tok),
                    f"{tok} 가 깨진 텍스트로 오판됨 (원어 보호 위반)",
                )

    def test_latin_abbrev_not_garbled(self):
        for tok in ("vgl", "cf", "Hrsg", "Bd", "ed", "ff"):
            with self.subTest(tok=tok):
                self.assertFalse(healer._is_likely_garbled(tok))

    def test_real_garble_still_removed(self):
        # 보수화가 실제 잔해까지 살려두면 안 됨 (회귀 방지)
        for tok in ("rSG", "dKh", "DPCa", "VdSudG1"):
            with self.subTest(tok=tok):
                self.assertTrue(healer._is_likely_garbled(tok))

    def test_protected_token_survives_inline(self):
        src = "그는 계시 TRE 항목 을 인용했다"
        self.assertIn("TRE", healer.pass3_garbled_text(src))

    def test_spaced_acronym_preserved(self):
        # 자간 띄운 대문자 시글라는 보존
        src = "약어 T R E S 를 보라"
        self.assertIn("T R E S", healer.pass3_garbled_text(src))

    def test_spaced_garble_still_removed(self):
        src = "계시 s i e h t o n o M 그리고"
        self.assertNotIn("s i e h t", healer.pass3_garbled_text(src))


class TestPass4(unittest.TestCase):
    def test_orphan_paren_before_particle_removed(self):
        # 닫는 괄호 없는 고아 `(` + 한국어 조사
        out = healer.pass4_parenthesis_normalization("신학( 은 학문이다")
        self.assertNotIn("(", out)

    def test_balanced_paren_preserved(self):
        src = "신학(학문)은 중요하다"
        self.assertEqual(healer.pass4_parenthesis_normalization(src), src)


class TestPass5(unittest.TestCase):
    def test_collapses_blank_lines(self):
        self.assertEqual(
            healer.pass5_text_normalization("A\n\n\n\n\nB"), "A\n\n\nB"
        )

    def test_merges_orphan_close_paren(self):
        self.assertEqual(
            healer.pass5_text_normalization("문장\n)\n다음"), "문장)\n다음"
        )


# ─────────────── 감사(Audit) 테스트 ───────────────

class TestAudit(unittest.TestCase):
    def test_disabled_audit_records_nothing(self):
        a = healer.Audit(enabled=False)
        a.record("p", "k", "removed", 1, "ctx")
        self.assertEqual(a.records, [])

    def test_enabled_audit_captures_pass3_deletion(self):
        a = healer.Audit(enabled=True)
        healer.pass3_garbled_text("계시 s i e h t 그리고", a)
        self.assertTrue(a.records)
        self.assertEqual(a.records[0]["pass"], "Pass 3 외래어 잔해")

    def test_clean_input_produces_no_records(self):
        a = healer.Audit(enabled=True)
        text = "이것은 깨끗한 한국어 문장이다."
        for fn in (
            healer.pass1_page_artifacts,
            healer.pass2_footnote_separation,
            healer.pass3_garbled_text,
            healer.pass4_parenthesis_normalization,
            healer.pass5_text_normalization,
        ):
            text = fn(text, a)
        self.assertEqual(a.records, [], "clean 입력에서 변형이 기록됨")


# ─────────────── 실제 샘플 기반 회귀·멱등 ───────────────

SAMPLES = [
    SKILL_ROOT / "output" / "van_Wolde_Amos4_cleaned.md",
    SKILL_ROOT / "output" / "KCI_FI003034827_cleaned.md",
]


def _run_all_passes(text: str) -> str:
    text = healer.pass1_page_artifacts(text)
    text = healer.pass2_footnote_separation(text)
    text = healer.pass3_garbled_text(text)
    text = healer.pass4_parenthesis_normalization(text)
    text = healer.pass5_text_normalization(text)
    return text


class TestRealSamples(unittest.TestCase):
    def test_all_passes_preserve_research_page_marker(self):
        src = "첫 문장.\n\n===== p.2 =====\n\n둘째 문장."
        out = _run_all_passes(src)
        self.assertIn("===== p.2 =====", out)
        self.assertNotIn("===== p.2 ===== 둘째", out)

    def test_idempotent(self):
        """heal(heal(x)) == heal(x) — 재실행 안정성."""
        for sample in SAMPLES:
            if not sample.exists():
                self.skipTest(f"샘플 없음: {sample.name}")
            with self.subTest(sample=sample.name):
                once = _run_all_passes(sample.read_text(encoding="utf-8"))
                twice = _run_all_passes(once)
                self.assertEqual(once, twice, f"{sample.name} 비멱등")

    def test_no_hangul_loss_in_text_passes(self):
        """불변식: Pass 3(외래어 잔해)는 샘플 전체에서 한글을 한 자도 줄이지 않는다."""
        for sample in SAMPLES:
            if not sample.exists():
                self.skipTest(f"샘플 없음: {sample.name}")
            with self.subTest(sample=sample.name):
                src = sample.read_text(encoding="utf-8")
                after = healer.pass3_garbled_text(src)
                self.assertEqual(
                    _count_hangul(src), _count_hangul(after),
                    f"{sample.name}: Pass 3 가 한글을 손실시킴",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
