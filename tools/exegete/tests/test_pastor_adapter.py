#!/usr/bin/env python3
"""Contract tests for the local Pastor-KR evidence adapter."""

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOL_ROOT))

import pastor_adapter  # noqa: E402


class AdapterFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.data_root = self.root / "data" / "scripture"
        self.source_root = self.data_root / "source"
        self.data_root.mkdir(parents=True)
        self.source_root.mkdir(parents=True)
        self.foundation = self.root / "core" / "foundation.md"
        self.foundation.parent.mkdir()
        self.foundation.write_text(
            '---\npreferred_bible: "개역개정"\n---\n', encoding="utf-8"
        )

    def tearDown(self):
        self.temp.cleanup()

    def write_catalog(self, value, root):
        catalog = root / "_exegete" / "catalog.json"
        catalog.parent.mkdir(parents=True, exist_ok=True)
        catalog.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    def test_requested_edition_never_falls_back(self):
        (self.data_root / "bible_korean.txt").write_text(
            "요3:16 개역한글 본문\n", encoding="utf-8"
        )

        evidence = pastor_adapter.query(
            "요3:16", kind="passage", data_root=self.data_root, foundation_path=self.foundation
        )

        self.assertEqual(evidence["status"], "unavailable")
        self.assertEqual(evidence["passage"]["resolved_verses"], [])
        self.assertIn("edition_unavailable", {item["code"] for item in evidence["warnings"]})

    def test_catalogued_integrated_and_book_specific_files(self):
        integrated = self.data_root / "fixture.txt"
        integrated.write_text(
            "요3:16 <사랑> 하나님이 세상을 이처럼 사랑하사\n"
            "요3:17 하나님이 그 아들을 보내신 것은\n",
            encoding="utf-8",
        )
        self.write_catalog(
            {
                "editions": [
                    {
                        "edition_id": "fixture-ko",
                        "name": "Fixture Korean",
                        "aliases": ["FIXTURE"],
                        "file": "fixture.txt",
                        "provider": "test",
                        "revision": "fixture-1",
                        "license": "test-only",
                    }
                ]
            },
            self.data_root,
        )
        evidence = pastor_adapter.query(
            "요한복음 3:16-17", kind="passage", data_root=self.data_root, edition="FIXTURE"
        )
        self.assertEqual(evidence["status"], "ok")
        self.assertEqual(
            [verse["text"] for verse in evidence["passage"]["resolved_verses"]],
            ["하나님이 세상을 이처럼 사랑하사", "하나님이 그 아들을 보내신 것은"],
        )
        self.assertEqual(evidence["passage"]["resolved_verses"][0]["heading"], "사랑")
        self.assertEqual(len(evidence["sources"][0]["sha256"]), 64)
        self.assertEqual(evidence["sources"][0]["record_keys"], ["요3:16", "요3:17"])

        book_specific = self.data_root / "john-only.txt"
        book_specific.write_text("3:16 책별 파일 본문\n", encoding="utf-8")
        self.write_catalog(
            {
                "editions": [
                    {
                        "edition_id": "fixture-book",
                        "name": "Fixture Book",
                        "file": "john-only.txt",
                        "book": "요",
                    }
                ]
            },
            self.data_root,
        )
        book_evidence = pastor_adapter.query(
            "John 3:16", kind="passage", data_root=self.data_root, edition="fixture-book"
        )
        self.assertEqual(book_evidence["status"], "ok")
        self.assertEqual(book_evidence["passage"]["resolved_verses"][0]["text"], "책별 파일 본문")

    def test_duplicate_and_missing_verses_are_partial(self):
        path = self.data_root / "fixture.txt"
        path.write_text("요3:16 첫 행\n요3:16 중복 행\n", encoding="utf-8")
        evidence = pastor_adapter.query(
            "요3:16-17", kind="passage", data_root=self.data_root, edition="개역개정", bible_file=path
        )
        self.assertEqual(evidence["status"], "partial")
        codes = {item["code"] for item in evidence["warnings"]}
        self.assertTrue({"duplicate_verses", "missing_verses"}.issubset(codes))
        self.assertEqual(evidence["passage"]["resolved_verses"][0]["text"], "첫 행")

    def test_cross_chapter_range_is_explicitly_rejected(self):
        evidence = pastor_adapter.query("요3:16-4:2", kind="all")
        self.assertEqual(evidence["status"], "invalid_request")
        self.assertEqual(evidence["error"]["code"], "cross_chapter_unsupported")

    def test_greek_and_hebrew_tokens_are_independent(self):
        greek = self.source_root / "original" / "greek" / "tagnt.txt"
        hebrew = self.source_root / "original" / "hebrew" / "tahot.txt"
        greek.parent.mkdir(parents=True)
        hebrew.parent.mkdir(parents=True)
        greek.write_text(
            "Jhn.3.16#01=NKO\tΟὕτως\tthus\tG3779=ADV\tοὕτως=thus\n",
            encoding="utf-8",
        )
        hebrew.write_text(
            "Gen.1.1#01=HVqp3ms\tבְּרֵאשִׁית\tbərēʾšît\tin the beginning\tH7225\tN-fs\t{H7225=beginning}\n",
            encoding="utf-8",
        )
        self.write_catalog(
            {
                "datasets": [
                    {
                        "dataset_id": "fixture-tagnt",
                        "language": "Greek",
                        "root": "original/greek",
                        "provider": "fixture",
                        "revision": "g1",
                        "license": "test-only",
                    },
                    {
                        "dataset_id": "fixture-tahot",
                        "language": "Hebrew",
                        "root": "original/hebrew",
                        "provider": "fixture",
                        "revision": "h1",
                        "license": "test-only",
                    },
                ]
            },
            self.source_root,
        )
        greek_evidence = pastor_adapter.query("요3:16", kind="original", source_root=self.source_root)
        self.assertEqual(greek_evidence["status"], "ok")
        token = greek_evidence["original_language"]["tokens"][0]
        self.assertEqual(token["language"], "Greek")
        self.assertEqual(token["strong"], "G3779")
        self.assertEqual(token["raw_morphology"], "ADV")
        self.assertEqual(greek_evidence["capabilities"]["morphology"]["available"], True)

        hebrew_evidence = pastor_adapter.query("창1:1", kind="original", source_root=self.source_root)
        self.assertEqual(hebrew_evidence["status"], "ok")
        hebrew_token = hebrew_evidence["original_language"]["tokens"][0]
        self.assertEqual(hebrew_token["language"], "Hebrew")
        self.assertEqual(hebrew_token["strong"], "H7225")
        self.assertEqual(hebrew_token["lemma"], "H7225=beginning")
        self.assertEqual(greek_evidence["sources"][0]["record_keys"], ["Jhn.3.16#01=NKO"])

    def test_original_partial_result_and_exact_lexicon_key(self):
        greek = self.source_root / "original" / "greek" / "tagnt.txt"
        greek.parent.mkdir(parents=True)
        greek.write_text(
            "Jhn.3.16#01=NKO\tΟὕτως\tthus\tG3779=ADV\tοὕτως=thus\n"
            "Jhn.3.16#02=NKO\tθεός\tGod\tG2316=N-NSM\tθεός=God\n",
            encoding="utf-8",
        )
        self.write_catalog(
            {
                "datasets": [
                    {
                        "dataset_id": "fixture-tagnt",
                        "language": "Greek",
                        "root": "original/greek",
                    }
                ]
            },
            self.source_root,
        )
        lexicon = self.source_root / "lexicon"
        lexicon.mkdir()
        (lexicon / "greek_lexicon.json").write_text(
            json.dumps(
                {
                    "entries": {"G3779": {"strong": "G3779", "gloss": "thus"}},
                    "by_base": {"3779": ["G3779"]},
                }
            ),
            encoding="utf-8",
        )
        evidence = pastor_adapter.query("요3:16-17", kind="original", source_root=self.source_root)
        self.assertEqual(evidence["status"], "partial")
        self.assertEqual(evidence["original_language"]["tokens"][0]["lexicon"][0]["entry"]["strong"], "G3779")
        self.assertTrue(evidence["original_language"]["missing_verses"])

    def test_original_text_without_morphology_is_not_overstated(self):
        greek = self.source_root / "original" / "greek" / "text-only.txt"
        greek.parent.mkdir(parents=True)
        greek.write_text("Jhn.3.16#01=NKO\tΟὕτως\n", encoding="utf-8")
        self.write_catalog(
            {
                "datasets": [
                    {"dataset_id": "fixture-text-only", "language": "Greek", "root": "original/greek"}
                ]
            },
            self.source_root,
        )
        evidence = pastor_adapter.query("요3:16", kind="original", source_root=self.source_root)
        self.assertEqual(evidence["status"], "ok")
        self.assertTrue(evidence["capabilities"]["original_text"]["available"])
        self.assertFalse(evidence["capabilities"]["morphology"]["available"])

    def test_cli_always_returns_json_for_unavailable_data(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = pastor_adapter.main(
                ["요3:16", "--kind", "passage", "--edition", "개역개정", "--data-root", str(self.data_root)]
            )
        payload = json.loads(output.getvalue())
        self.assertEqual(exit_code, 3)
        self.assertEqual(payload["status"], "unavailable")
        self.assertIn("capabilities", payload)

    def test_foundation_comments_and_quotes(self):
        for scalar in ('"WEB" # chosen', "'WEB' # chosen", 'WEB # chosen'):
            self.foundation.write_text(f'---\npreferred_bible: {scalar}\n---\n', encoding='utf-8')
            self.assertEqual(pastor_adapter._preferred_edition(self.foundation), 'WEB')

    def test_two_books_in_one_edition(self):
        (self.data_root / 'john.txt').write_text('3:16 fixture john\n', encoding='utf-8')
        (self.data_root / 'gen.txt').write_text('1:1 fixture genesis\n', encoding='utf-8')
        self.write_catalog({'editions': [
            {'name': 'fixture', 'book': '요', 'file': 'john.txt'},
            {'name': 'fixture', 'book': '창', 'file': 'gen.txt'}]}, self.data_root)
        for ref, text in [('요3:16', 'fixture john'), ('창1:1', 'fixture genesis')]:
            evidence = pastor_adapter.query(ref, kind='passage', data_root=self.data_root, edition='fixture')
            self.assertEqual(evidence['status'], 'ok')
            self.assertEqual(evidence['resolved_verses'][0]['text'], text)

    def test_original_conflicts_and_empty_dictionary_never_complete(self):
        root = self.source_root / 'greek'
        root.mkdir()
        path = root / 'tokens.tsv'
        path.write_text('Jhn.3.16#01=NKO\tA\tfirst\tG0001=N\tA\n'
                        'Jhn.3.16#02=NKO\tB\n'
                        'Jhn.3.16#01=NKO\tCONFLICT\tother\tG0002=N\tC\n', encoding='utf-8')
        lex = self.source_root / 'lexicon'
        lex.mkdir()
        (lex / 'greek_lexicon.json').write_text('{"entries": {}, "by_base": {}}', encoding='utf-8')
        evidence = pastor_adapter.query('요3:16', kind='original', source_root=self.source_root)
        self.assertEqual(evidence['status'], 'partial')
        for name in ('original_text', 'morphology', 'lexicon'):
            self.assertFalse(evidence['capabilities'][name]['complete'])
        self.assertFalse(evidence['capabilities']['lexicon']['available'])
        self.assertFalse(evidence['original_language']['provenance_complete'])

    def test_coverage_requires_separate_counts(self):
        root = self.source_root / 'greek'
        root.mkdir()
        (root / 'tokens.tsv').write_text('Jhn.3.16#01=NKO\tA\tfirst\tG0001=N\tA\n', encoding='utf-8')
        metadata = dict(dataset_id='fixture', edition_id='fixture', provider='fixture', revision='1',
                        license='fixture', source_url='https://example.invalid', tagset='fixture', language='Greek', root='greek')
        self.write_catalog({'datasets': [metadata]}, self.source_root)
        evidence = pastor_adapter.query('요3:16', kind='original', source_root=self.source_root)
        self.assertFalse(evidence['capabilities']['original_text']['complete'])
        metadata['verse_token_counts'] = {'Jhn 3:16': 1}
        self.write_catalog({'datasets': [metadata]}, self.source_root)
        evidence = pastor_adapter.query('요3:16', kind='original', source_root=self.source_root)
        self.assertTrue(evidence['capabilities']['original_text']['complete'])
        self.assertTrue(evidence['original_language']['provenance_complete'])

    def test_different_datasets_are_not_merged(self):
        datasets = []
        for i in (1, 2):
            root = self.source_root / f'greek{i}'
            root.mkdir()
            (root / 'tokens.tsv').write_text(f'Jhn.3.16#0{i}=NKO\tA\tfirst\tG0001=N\tA\n', encoding='utf-8')
            datasets.append({'dataset_id': str(i), 'language': 'Greek', 'root': root.name})
        self.write_catalog({'datasets': datasets}, self.source_root)
        evidence = pastor_adapter.query('요3:16', kind='original', source_root=self.source_root)
        self.assertEqual(evidence['status'], 'partial')
        self.assertEqual(len(evidence['original_language']['tokens']), 1)
        self.assertIn('dataset_conflict', {w['code'] for w in evidence['warnings']})


if __name__ == "__main__":
    unittest.main(verbosity=2)
