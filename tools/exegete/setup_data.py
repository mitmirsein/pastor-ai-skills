#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Explicit, checksum-verified installation for ignored Exegete data.

The adapter never calls this module.  A user or operator must provide a
manifest containing an exact URL, destination-relative path, and SHA-256 for
every file.  Files are staged and verified before any destination is changed;
existing files with a different hash are refused.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


class InstallError(Exception):
    """A manifest or installation safety check failed."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _safe_relative(value: Any) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise InstallError("manifest_relative_path_missing")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise InstallError(f"unsafe_relative_path:{value}")
    return path


def _load_manifest(path: Path) -> Dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise InstallError(f"manifest_read_error:{error}")
    if not isinstance(value, dict) or not isinstance(value.get("files"), list) or not value["files"]:
        raise InstallError("manifest_files_required")
    return value


def _validate_entries(manifest: Dict[str, Any], destination: Path) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    seen = set()
    for raw in manifest["files"]:
        if not isinstance(raw, dict):
            raise InstallError("manifest_file_entry_invalid")
        relative = _safe_relative(raw.get("relative_path"))
        url = raw.get("url")
        expected = str(raw.get("sha256", "")).lower()
        if not isinstance(url, str) or not url:
            raise InstallError(f"manifest_url_missing:{relative}")
        if len(expected) != 64 or any(char not in "0123456789abcdef" for char in expected):
            raise InstallError(f"manifest_sha256_invalid:{relative}")
        if relative in seen:
            raise InstallError(f"manifest_duplicate_path:{relative}")
        seen.add(relative)
        target = (destination / relative).resolve()
        try:
            target.relative_to(destination.resolve())
        except ValueError:
            raise InstallError(f"unsafe_destination:{relative}")
        entries.append({**raw, "relative": relative, "target": target, "sha256": expected})
    return entries


def _download(url: str, destination: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "Pastor-KR-Exegete-Installer"})
    try:
        with urllib.request.urlopen(request, timeout=180) as response, destination.open("wb") as output:
            shutil.copyfileobj(response, output, length=1024 * 1024)
    except Exception as error:
        raise InstallError(f"download_failed:{url}:{error}")


def _write_json_atomic(path: Path, value: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    temporary = Path(name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as output:
            json.dump(value, output, ensure_ascii=False, indent=2)
            output.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _catalog_plan(manifest: Dict[str, Any], destination: Path) -> Optional[Tuple[Path, Dict[str, Any]]]:
    catalog = manifest.get("catalog")
    if catalog is None:
        return None
    if not isinstance(catalog, dict):
        raise InstallError("manifest_catalog_invalid")
    relative_catalog = _safe_relative(manifest.get("catalog_path", "_exegete/catalog.json"))
    catalog_file = destination / relative_catalog
    if catalog_file.is_file():
        try:
            current = json.loads(catalog_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise InstallError(f"existing_catalog_invalid:{error}")
        if current != catalog:
            raise InstallError(f"existing_catalog_conflict:{relative_catalog}")
    return catalog_file, catalog


def install_manifest(manifest_path: Path, destination: Path) -> Dict[str, Any]:
    """Install a verified manifest without overwriting existing source files."""

    manifest = _load_manifest(manifest_path.resolve())
    destination = destination.expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    entries = _validate_entries(manifest, destination)
    catalog_plan = _catalog_plan(manifest, destination)
    for entry in entries:
        target = entry["target"]
        if target.is_file() and sha256_file(target).lower() != entry["sha256"]:
            raise InstallError(f"existing_file_hash_mismatch:{entry['relative']}")

    installed: List[str] = []
    skipped: List[str] = []
    with tempfile.TemporaryDirectory(prefix=".exegete-staging-", dir=str(destination)) as staging_name:
        staging = Path(staging_name)
        for entry in entries:
            target = entry["target"]
            if target.is_file():
                skipped.append(entry["relative"].as_posix())
                continue
            staged = staging / entry["relative"]
            staged.parent.mkdir(parents=True, exist_ok=True)
            _download(str(entry["url"]), staged)
            if sha256_file(staged).lower() != entry["sha256"]:
                raise InstallError(f"download_hash_mismatch:{entry['relative']}")

        for entry in entries:
            target = entry["target"]
            if target.is_file():
                continue
            staged = staging / entry["relative"]
            target.parent.mkdir(parents=True, exist_ok=True)
            os.replace(staged, target)
            installed.append(entry["relative"].as_posix())

    if catalog_plan is not None:
        catalog_file, catalog = catalog_plan
        if not catalog_file.is_file():
            _write_json_atomic(catalog_file, catalog)

    return {"status": "ok", "installed": installed, "skipped": skipped, "destination": str(destination)}


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Install checksum-verified Exegete data")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--destination", type=Path, required=True, help="예: data/scripture/source")
    args = parser.parse_args(argv)
    try:
        result = install_manifest(args.manifest, args.destination)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except InstallError as error:
        print(json.dumps({"status": "error", "error": str(error)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
