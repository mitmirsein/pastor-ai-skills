#!/usr/bin/env python3
"""Safety tests for the explicit Exegete data installer."""

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOL_ROOT))

import setup_data  # noqa: E402


class SetupDataTest(unittest.TestCase):
    def test_verified_local_manifest_installs_and_then_skips(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            payload = root / "payload.txt"
            payload.write_text("verified data\n", encoding="utf-8")
            digest = hashlib.sha256(payload.read_bytes()).hexdigest()
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "files": [
                            {
                                "url": payload.as_uri(),
                                "relative_path": "original/greek/tagnt.txt",
                                "sha256": digest,
                            }
                        ],
                        "catalog": {"datasets": [{"dataset_id": "fixture"}]},
                    }
                ),
                encoding="utf-8",
            )
            destination = root / "source"
            first = setup_data.install_manifest(manifest, destination)
            second = setup_data.install_manifest(manifest, destination)
            self.assertEqual(first["installed"], ["original/greek/tagnt.txt"])
            self.assertEqual(second["skipped"], ["original/greek/tagnt.txt"])
            self.assertEqual(
                json.loads((destination / "_exegete/catalog.json").read_text(encoding="utf-8")),
                {"datasets": [{"dataset_id": "fixture"}]},
            )

    def test_bad_hash_does_not_leave_a_destination_file(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            payload = root / "payload.txt"
            payload.write_text("wrong hash\n", encoding="utf-8")
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "files": [
                            {
                                "url": payload.as_uri(),
                                "relative_path": "original/hebrew/tahot.txt",
                                "sha256": "0" * 64,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            destination = root / "source"
            with self.assertRaisesRegex(setup_data.InstallError, "download_hash_mismatch"):
                setup_data.install_manifest(manifest, destination)
            self.assertFalse((destination / "original/hebrew/tahot.txt").exists())

    def test_existing_mismatch_is_refused_before_download(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            destination = root / "source"
            existing = destination / "original/greek/tagnt.txt"
            existing.parent.mkdir(parents=True)
            existing.write_text("user source\n", encoding="utf-8")
            payload = root / "payload.txt"
            payload.write_text("new source\n", encoding="utf-8")
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "files": [
                            {
                                "url": payload.as_uri(),
                                "relative_path": "original/greek/tagnt.txt",
                                "sha256": hashlib.sha256(payload.read_bytes()).hexdigest(),
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(setup_data.InstallError, "existing_file_hash_mismatch"):
                setup_data.install_manifest(manifest, destination)
            self.assertEqual(existing.read_text(encoding="utf-8"), "user source\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
