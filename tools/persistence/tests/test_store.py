import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('store', Path(__file__).parents[1] / 'store.py')
store = importlib.util.module_from_spec(spec)
spec.loader.exec_module(store)


class PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.plan = {'operation_id': 'save-1', 'writes': [
            {'path': 'outputs/sermons/test/v02.md', 'before_sha256': None,
             'kind': 'artifact', 'content': '목회자 원문\n'},
            {'path': 'outputs/sermons/test/_manifest.md', 'before_sha256': None,
             'content': 'current_stage: drafted\n- v02.md\n'},
            {'path': 'outputs/sermons/_index.md', 'before_sha256': None,
             'content': '- outputs/sermons/test/v02.md\n'},
            {'path': 'core/pastor_journal.md', 'before_sha256': None,
             'content': 'stage: drafted\n'}]}

    def test_index_failure_resume_preserves_artifact_and_has_one_row(self):
        with self.assertRaises(OSError):
            store.apply(self.root, self.plan, fail_after=2)
        artifact = self.root / self.plan['writes'][0]['path']
        before = artifact.stat().st_mtime_ns
        receipt = json.loads((self.root / 'outputs/.operations/save-1.json').read_text())
        self.assertEqual(receipt['status'], 'partial')
        self.assertEqual(len(receipt['completed']), 2)
        self.assertFalse((self.root / 'core/pastor_journal.md').exists())
        store.apply(self.root, self.plan)
        store.apply(self.root, self.plan)
        self.assertEqual(before, artifact.stat().st_mtime_ns)
        self.assertEqual(artifact.read_text(), '목회자 원문\n')
        self.assertEqual((self.root / 'outputs/sermons/_index.md').read_text().count('v02.md'), 1)
        self.assertEqual(len(list(artifact.parent.glob('v*.md'))), 1)

    def test_intervening_edit_is_not_overwritten(self):
        with self.assertRaises(OSError):
            store.apply(self.root, self.plan, fail_after=2)
        manifest = self.root / 'outputs/sermons/test/_manifest.md'
        manifest.write_text('다른 편집\n')
        with self.assertRaisesRegex(ValueError, 'concurrent edit'):
            store.apply(self.root, self.plan)
        self.assertEqual(manifest.read_text(), '다른 편집\n')

    def test_operation_id_cannot_change_payload(self):
        store.apply(self.root, self.plan)
        receipt = (self.root / 'outputs/.operations/save-1.json').read_bytes()
        self.plan['writes'][0]['content'] = '다른 원문'
        with self.assertRaisesRegex(ValueError, 'different plan'):
            store.apply(self.root, self.plan)
        self.assertEqual(receipt, (self.root / 'outputs/.operations/save-1.json').read_bytes())

    def test_path_escape_rejected_before_any_writes(self):
        self.plan['writes'][-1]['path'] = '../outside.md'
        with self.assertRaises(ValueError):
            store.apply(self.root, self.plan)
        self.assertFalse((self.root / 'outputs').exists())

    def test_existing_artifact_cannot_be_replaced(self):
        self.plan['writes'][0]['before_sha256'] = store.digest(b'original')
        with self.assertRaisesRegex(ValueError, 'new path'):
            store.apply(self.root, self.plan)

    def test_identical_existing_artifact_is_not_claimed_by_new_operation(self):
        path = self.root / self.plan['writes'][0]['path']
        path.parent.mkdir(parents=True)
        path.write_text('목회자 원문\n')
        for _ in range(2):
            with self.assertRaisesRegex(ValueError, 'already exists'):
                store.apply(self.root, self.plan)
        self.assertFalse((self.root / 'core/pastor_journal.md').exists())

    def test_symlink_outside_root_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            (self.root / 'outputs').symlink_to(outside)
            with self.assertRaises(ValueError):
                store.apply(self.root, self.plan)
            self.assertEqual(list(Path(outside).iterdir()), [])

    def test_invalid_unicode_does_not_leave_lock(self):
        self.plan['writes'][0]['content'] = chr(0xD800)
        with self.assertRaises(UnicodeError):
            store.apply(self.root, self.plan)
        self.assertFalse((self.root / 'outputs/.operations/.lock').exists())

    def test_reviewed_repair_omits_saved_artifact_and_records_predecessor(self):
        with self.assertRaises(OSError):
            store.apply(self.root, self.plan, fail_after=2)
        artifact = self.root / self.plan['writes'][0]['path']
        before = artifact.stat().st_mtime_ns
        manifest = self.root / self.plan['writes'][1]['path']
        manifest.write_text(manifest.read_text() + '다른 편집\n')
        merged = manifest.read_text() + '복구 대조 완료\n'
        repair = {'operation_id': 'repair-1', 'supersedes': 'save-1', 'writes': [
            {'path': self.plan['writes'][1]['path'],
             'before_sha256': store.current_hash(manifest), 'content': merged},
            *self.plan['writes'][2:]]}
        result = store.apply(self.root, repair)
        self.assertEqual(result['status'], 'complete')
        self.assertEqual(result['plan']['supersedes'], 'save-1')
        self.assertEqual(before, artifact.stat().st_mtime_ns)
        self.assertIn('다른 편집', manifest.read_text())
        self.assertEqual((self.root / self.plan['writes'][2]['path']).read_text().count('v02.md'), 1)

    def test_first_write_failure_does_not_claim_saved(self):
        with self.assertRaises(OSError):
            store.apply(self.root, self.plan, fail_after=0)
        receipt = json.loads((self.root / 'outputs/.operations/save-1.json').read_text())
        self.assertEqual(receipt['status'], 'failed')
        self.assertEqual(receipt['completed'], [])


if __name__ == '__main__':
    unittest.main()
