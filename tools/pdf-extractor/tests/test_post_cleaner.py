#!/usr/bin/env python3
"""
post_cleaner.py P5 회귀 테스트 — 약어 예외 · 디하이프네이션/가운뎃점 가드
"""

import sys
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

import post_cleaner as pc  # noqa: E402


class TestAbbrevTail(unittest.TestCase):
    def test_latin_abbrev_not_sentence_end(self):
        for s in ("siehe vgl.", "so z.B.", "Hrsg.", "et al.", "Bd."):
            with self.subTest(s=s):
                self.assertTrue(pc._is_abbrev_tail(s))

    def test_author_initials_not_sentence_end(self):
        for s in ("herausgegeben von R.", "von R.F.", "J.B."):
            with self.subTest(s=s):
                self.assertTrue(pc._is_abbrev_tail(s))

    def test_real_sentence_end_flushes(self):
        for s in ("이것은 문장이다.", "He wrote a book.", "끝났다."):
            with self.subTest(s=s):
                self.assertFalse(pc._is_abbrev_tail(s))


class TestParagraphMergeAbbrev(unittest.TestCase):
    def test_no_premature_split_on_abbrev(self):
        # clean_markdown 은 파일 IO 기반이므로 임시 파일로 검증
        import tempfile
        import os
        src = "그는 z.B.\n중요한 책을 인용했다."
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t.md")
            Path(p).write_text(src, encoding="utf-8")
            res = pc.clean_markdown(p)
            text = Path(res).read_text(encoding="utf-8")
        # 'z.B.' 뒤에서 줄이 끊겨 별도 문단이 되면 안 됨
        self.assertIn("z.B. 중요한 책을 인용했다", text)

    def test_page_marker_remains_structural(self):
        import tempfile
        import os
        src = "첫 문장.\n\n===== p.2 =====\n\n둘째 문장."
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t.md")
            Path(p).write_text(src, encoding="utf-8")
            text = Path(pc.clean_markdown(p)).read_text(encoding="utf-8")
        self.assertIn("\n===== p.2 =====\n", text)
        self.assertNotIn("===== p.2 ===== 둘째", text)


class TestHyphenationGuard(unittest.TestCase):
    def test_korean_middle_dot_preserved(self):
        """한국어 가운뎃점은 정상 구분자 — 절대 삭제 금지."""
        import tempfile
        import os
        src = "방향은 북·동·서·남 이다. 저자는 김·이·박 이다."
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t.md")
            Path(p).write_text(src, encoding="utf-8")
            text = Path(pc.clean_markdown(p)).read_text(encoding="utf-8")
        self.assertIn("북·동·서·남", text)
        self.assertIn("김·이·박", text)

    def test_latin_linebreak_hyphen_joined(self):
        import tempfile
        import os
        src = "이것은 Heils-\ngeschichte 라는 개념."
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t.md")
            Path(p).write_text(src, encoding="utf-8")
            text = Path(pc.clean_markdown(p)).read_text(encoding="utf-8")
        self.assertIn("Heilsgeschichte", text)

    def test_compound_hyphen_before_capital_preserved(self):
        import tempfile
        import os
        # 다음 줄이 대문자로 시작 → 고유 합성어 하이픈일 수 있어 보존
        src = "용어 Gott-\nMensch 논의."
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "t.md")
            Path(p).write_text(src, encoding="utf-8")
            text = Path(pc.clean_markdown(p)).read_text(encoding="utf-8")
        self.assertNotIn("GottMensch", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
