"""Opt-in integration checks against pinned local data; no network or writes.

PASTOR_EXEGETE_VALIDATION_ROOT=data/scripture/_validation python3 -B -m unittest
discover -s tools/exegete/tests -v
"""
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pastor_adapter as adapter


@unittest.skipUnless(os.environ.get('PASTOR_EXEGETE_VALIDATION_ROOT'), 'opt-in real data')
class RealData(unittest.TestCase):
    def setUp(self):
        self.root = Path(os.environ['PASTOR_EXEGETE_VALIDATION_ROOT']).resolve()

    def query(self, ref, edition='개역한글'):
        return adapter.query(ref, data_root=self.root, source_root=self.root, edition=edition)

    def test_source_hashes(self):
        for file, digest in (
            ('greek/tagnt.txt', 'ab8eaaeb68e17a1dcfa34e1e9350358f22f03bc2a97244d848750ad81044bc8e'),
            ('hebrew/tahot.txt', 'e9b8546ee48fe0bfc57c3b70f5f40e98d96580e803526d19026224e31753368b'),
            ('bible_korean.txt', '68f4f32d687af20680d128d394a4d72ae0c2e3ae4a58d648f4c1f012ada7ffd3')):
            self.assertEqual(hashlib.sha256((self.root / file).read_bytes()).hexdigest(), digest)

    def test_each_greek_token_against_raw_fields(self):
        evidence = self.query('요3:16')
        self.assertEqual(evidence['status'], 'ok')
        tokens = evidence['original_language']['tokens']
        rows = [line.split('\t') for line in (self.root / 'greek/tagnt.txt').read_text().splitlines() if line.startswith('Jhn.3.16#')]
        self.assertEqual(len(tokens), 26)
        self.assertEqual(len(rows), 26)
        for row, token in zip(rows, tokens):
            self.assertEqual(token['record_key'], row[0])
            self.assertEqual(token['surface'], row[1].split(' (')[0])
            self.assertEqual(token['lemma'], row[4].split('=')[0])
            self.assertEqual(token['strong'], row[3].split('=')[0])
            self.assertEqual(token['raw_morphology'], row[3].split('=')[1])
        self.assertTrue(evidence['capabilities']['original_text']['complete'])

    def test_each_hebrew_token_against_raw_fields(self):
        evidence = self.query('창1:1')
        tokens = evidence['original_language']['tokens']
        rows = [line.split('\t') for line in (self.root / 'hebrew/tahot.txt').read_text().splitlines() if line.startswith('Gen.1.1#')]
        self.assertEqual(len(tokens), 7)
        for row, token in zip(rows, tokens):
            self.assertEqual(token['surface'], row[1])
            self.assertEqual(token['strong'], row[4])
            self.assertEqual(token['raw_morphology'], row[5])
        self.assertEqual(tokens[1]['lemma'], 'בָּרָא')
        self.assertIn('H1254A', adapter._strong_numbers(tokens[1]['strong']))

    def test_passage_range_preserves_text(self):
        evidence = self.query('요3:16-17')
        raw = (self.root / 'bible_korean.txt').read_text().splitlines()
        for verse in evidence['passage']['resolved_verses']:
            row = next(line for line in raw if line.startswith(f"요3:{verse['verse']} "))
            self.assertEqual(verse['text'], row.split(' ', 1)[1])
        self.assertEqual(evidence['status'], 'ok')

    def test_requested_edition_missing_and_offline_cli(self):
        self.assertEqual(self.query('요3:16', '개역개정')['status'], 'unavailable')
        completed = subprocess.run([sys.executable, '-B', str(Path(adapter.__file__)), '요3:16',
            '--kind', 'passage', '--edition', '개역한글', '--data-root', str(self.root)],
            capture_output=True, text=True, timeout=20,
            env={**os.environ, 'http_proxy': 'http://127.0.0.1:1', 'https_proxy': 'http://127.0.0.1:1'})
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_real_dictionary_exact_extended_key(self):
        evidence = self.query('창1:1')
        token = evidence['original_language']['tokens'][1]
        self.assertEqual(token['lexicon'][0]['query'], 'H1254A')
        self.assertEqual(token['lexicon'][0]['entry']['strong'], 'H1254A')
        self.assertNotEqual(token['lexicon'][0]['entry']['strong'], 'H1254B')

    def test_lookup_is_offline_and_preserves_ministry_state(self):
        repo = Path(adapter.__file__).resolve().parents[2]
        def snapshot():
            paths = list((repo / 'core').glob('*.md')) + [p for p in (repo / 'outputs').rglob('*') if p.is_file()]
            return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        before = snapshot()
        with patch('urllib.request.urlopen', side_effect=AssertionError('network forbidden')), patch('socket.create_connection', side_effect=AssertionError('network forbidden')):
            evidence = self.query('요3:16')
        self.assertEqual(evidence['status'], 'ok')
        self.assertEqual(before, snapshot())


if __name__ == '__main__':
    unittest.main()
