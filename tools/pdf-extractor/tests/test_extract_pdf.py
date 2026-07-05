#!/usr/bin/env python3
"""extract_pdf.py page marker helpers."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

import extract_pdf  # noqa: E402


class TestPageMarkedMarkdown(unittest.TestCase):
    def test_writes_page_markers_from_json_kids(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            (out / "paper.json").write_text(
                json.dumps(
                    {
                        "number of pages": 2,
                        "kids": [
                            {"page number": 1, "content": "첫 페이지"},
                            {"page number": 2, "content": "둘째 페이지"},
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            marked = extract_pdf._write_page_marked_markdown(str(out), "paper")
            text = Path(marked).read_text(encoding="utf-8")

        self.assertIn("===== p.1 =====", text)
        self.assertIn("첫 페이지", text)
        self.assertIn("===== p.2 =====", text)
        self.assertIn("둘째 페이지", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
