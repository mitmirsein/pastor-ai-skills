#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pastor-KR's evidence adapter for optional Exegete data.

This module deliberately keeps the Pastor-KR boundary small.  It reads local
passage and original-language files, returns a stable evidence JSON document,
and never downloads data or silently changes the requested edition.

The file formats are compatible with the pinned upstream Exegete revision:

* passage files contain one verse per line, for example ``요3:16 본문`` or
  ``Jhn 3:16 text``;
* STEPBible-style original-language files contain a key such as
  ``Jhn.3.16#01=NKO`` followed by tab-separated fields.

The adapter is intentionally independent of optional third-party Python
packages.  The upstream commit is recorded in the evidence and VENDOR.md;
the adapter owns Pastor-KR's edition, provenance, and failure semantics.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


SCHEMA_VERSION = "pastor-exegete-evidence/v1"
ADAPTER_VERSION = "0.1.0"
UPSTREAM_REPOSITORY = "https://github.com/worlyung/exegete"
UPSTREAM_SHA = "6e32717fa6ee012e08d760a066f0f66a723d0bc4"
REPO_ROOT = Path(__file__).resolve().parents[2]

STATUS_OK = "ok"
STATUS_PARTIAL = "partial"
STATUS_UNAVAILABLE = "unavailable"
STATUS_INVALID_REQUEST = "invalid_request"
STATUS_ERROR = "error"
STATUSES = {
    STATUS_OK,
    STATUS_PARTIAL,
    STATUS_UNAVAILABLE,
    STATUS_INVALID_REQUEST,
    STATUS_ERROR,
}
EXIT_CODES = {
    STATUS_OK: 0,
    STATUS_PARTIAL: 1,
    STATUS_INVALID_REQUEST: 2,
    STATUS_UNAVAILABLE: 3,
    STATUS_ERROR: 4,
}


# The names mirror the pinned upstream book map while accepting the Korean
# abbreviations already used throughout Pastor-KR.  Keeping the map here
# avoids making the adapter depend on an untracked data file for references.
BOOKS: Tuple[Dict[str, Any], ...] = (
    {"step": "Gen", "ko": ("창", "창세기"), "en": ("gen", "genesis"), "testament": "OT"},
    {"step": "Exo", "ko": ("출", "출애굽기"), "en": ("exo", "exodus"), "testament": "OT"},
    {"step": "Lev", "ko": ("레", "레위기"), "en": ("lev", "leviticus"), "testament": "OT"},
    {"step": "Num", "ko": ("민", "민수기"), "en": ("num", "numbers"), "testament": "OT"},
    {"step": "Deu", "ko": ("신", "신명기"), "en": ("deu", "deuteronomy"), "testament": "OT"},
    {"step": "Jos", "ko": ("수", "여호수아"), "en": ("jos", "joshua"), "testament": "OT"},
    {"step": "Jdg", "ko": ("삿", "사사기"), "en": ("jdg", "judges"), "testament": "OT"},
    {"step": "Rut", "ko": ("룻", "룻기"), "en": ("rut", "ruth"), "testament": "OT"},
    {"step": "1Sa", "ko": ("삼상", "사무엘상"), "en": ("1sa", "1 samuel"), "testament": "OT"},
    {"step": "2Sa", "ko": ("삼하", "사무엘하"), "en": ("2sa", "2 samuel"), "testament": "OT"},
    {"step": "1Ki", "ko": ("왕상", "열왕기상"), "en": ("1ki", "1 kings"), "testament": "OT"},
    {"step": "2Ki", "ko": ("왕하", "열왕기하"), "en": ("2ki", "2 kings"), "testament": "OT"},
    {"step": "1Ch", "ko": ("대상", "역대상"), "en": ("1ch", "1 chronicles"), "testament": "OT"},
    {"step": "2Ch", "ko": ("대하", "역대하"), "en": ("2ch", "2 chronicles"), "testament": "OT"},
    {"step": "Ezr", "ko": ("스", "에스라"), "en": ("ezr", "ezra"), "testament": "OT"},
    {"step": "Neh", "ko": ("느", "느헤미야"), "en": ("neh", "nehemiah"), "testament": "OT"},
    {"step": "Est", "ko": ("에", "에스더"), "en": ("est", "esther"), "testament": "OT"},
    {"step": "Job", "ko": ("욥", "욥기"), "en": ("job", "job"), "testament": "OT"},
    {"step": "Psa", "ko": ("시", "시편"), "en": ("ps", "psalms"), "testament": "OT"},
    {"step": "Pro", "ko": ("잠", "잠언"), "en": ("pro", "proverbs"), "testament": "OT"},
    {"step": "Ecc", "ko": ("전", "전도서"), "en": ("ecc", "ecclesiastes"), "testament": "OT"},
    {"step": "Sng", "ko": ("아", "아가"), "en": ("sng", "song of songs"), "testament": "OT"},
    {"step": "Isa", "ko": ("사", "이사야"), "en": ("isa", "isaiah"), "testament": "OT"},
    {"step": "Jer", "ko": ("렘", "예레미야"), "en": ("jer", "jeremiah"), "testament": "OT"},
    {"step": "Lam", "ko": ("애", "예레미야애가"), "en": ("lam", "lamentations"), "testament": "OT"},
    {"step": "Ezk", "ko": ("겔", "에스겔"), "en": ("ezk", "ezekiel"), "testament": "OT"},
    {"step": "Dan", "ko": ("단", "다니엘"), "en": ("dan", "daniel"), "testament": "OT"},
    {"step": "Hos", "ko": ("호", "호세아"), "en": ("hos", "hosea"), "testament": "OT"},
    {"step": "Jol", "ko": ("욜", "요엘"), "en": ("jol", "joel"), "testament": "OT"},
    {"step": "Amo", "ko": ("암", "아모스"), "en": ("amo", "amos"), "testament": "OT"},
    {"step": "Oba", "ko": ("옵", "오바댜"), "en": ("oba", "obadiah"), "testament": "OT"},
    {"step": "Jon", "ko": ("욘", "요나"), "en": ("jon", "jonah"), "testament": "OT"},
    {"step": "Mic", "ko": ("미", "미가"), "en": ("mic", "micah"), "testament": "OT"},
    {"step": "Nam", "ko": ("나", "나훔"), "en": ("nah", "nahum"), "testament": "OT"},
    {"step": "Hab", "ko": ("합", "하박국"), "en": ("hab", "habakkuk"), "testament": "OT"},
    {"step": "Zep", "ko": ("습", "스바냐"), "en": ("zep", "zephaniah"), "testament": "OT"},
    {"step": "Hag", "ko": ("학", "학개"), "en": ("hag", "haggai"), "testament": "OT"},
    {"step": "Zec", "ko": ("슥", "스가랴"), "en": ("zec", "zechariah"), "testament": "OT"},
    {"step": "Mal", "ko": ("말", "말라기"), "en": ("mal", "malachi"), "testament": "OT"},
    {"step": "Mat", "ko": ("마", "마태복음"), "en": ("mat", "matthew"), "testament": "NT"},
    {"step": "Mrk", "ko": ("막", "마가복음"), "en": ("mk", "mark"), "testament": "NT"},
    {"step": "Luk", "ko": ("눅", "누가복음"), "en": ("lk", "luke"), "testament": "NT"},
    {"step": "Jhn", "ko": ("요", "요한복음"), "en": ("jn", "john"), "testament": "NT"},
    {"step": "Act", "ko": ("행", "사도행전"), "en": ("act", "acts"), "testament": "NT"},
    {"step": "Rom", "ko": ("롬", "로마서"), "en": ("rom", "romans"), "testament": "NT"},
    {"step": "1Co", "ko": ("고전", "고린도전서"), "en": ("1co", "1 corinthians"), "testament": "NT"},
    {"step": "2Co", "ko": ("고후", "고린도후서"), "en": ("2co", "2 corinthians"), "testament": "NT"},
    {"step": "Gal", "ko": ("갈", "갈라디아서"), "en": ("gal", "galatians"), "testament": "NT"},
    {"step": "Eph", "ko": ("엡", "에베소서"), "en": ("eph", "ephesians"), "testament": "NT"},
    {"step": "Php", "ko": ("빌", "빌립보서"), "en": ("php", "philippians"), "testament": "NT"},
    {"step": "Col", "ko": ("골", "골로새서"), "en": ("col", "colossians"), "testament": "NT"},
    {"step": "1Th", "ko": ("살전", "데살로니가전서"), "en": ("1th", "1 thessalonians"), "testament": "NT"},
    {"step": "2Th", "ko": ("살후", "데살로니가후서"), "en": ("2th", "2 thessalonians"), "testament": "NT"},
    {"step": "1Ti", "ko": ("딤전", "디모데전서"), "en": ("1ti", "1 timothy"), "testament": "NT"},
    {"step": "2Ti", "ko": ("딤후", "디모데후서"), "en": ("2ti", "2 timothy"), "testament": "NT"},
    {"step": "Tit", "ko": ("딛", "디도서"), "en": ("tit", "titus"), "testament": "NT"},
    {"step": "Phm", "ko": ("몬", "빌레몬서"), "en": ("phm", "philemon"), "testament": "NT"},
    {"step": "Heb", "ko": ("히", "히브리서"), "en": ("heb", "hebrews"), "testament": "NT"},
    {"step": "Jas", "ko": ("약", "야고보서"), "en": ("jas", "james"), "testament": "NT"},
    {"step": "1Pe", "ko": ("벧전", "베드로전서"), "en": ("1pe", "1 peter"), "testament": "NT"},
    {"step": "2Pe", "ko": ("벧후", "베드로후서"), "en": ("2pe", "2 peter"), "testament": "NT"},
    {"step": "1Jn", "ko": ("요일", "요한일서"), "en": ("1jn", "1 john"), "testament": "NT"},
    {"step": "2Jn", "ko": ("요이", "요한이서"), "en": ("2jn", "2 john"), "testament": "NT"},
    {"step": "3Jn", "ko": ("요삼", "요한삼서"), "en": ("3jn", "3 john"), "testament": "NT"},
    {"step": "Jud", "ko": ("유", "유다서"), "en": ("jud", "jude"), "testament": "NT"},
    {"step": "Rev", "ko": ("계", "요한계시록"), "en": ("rev", "revelation"), "testament": "NT"},
)

KNOWN_EDITIONS: Tuple[Dict[str, Any], ...] = (
    {
        "edition_id": "krv-user-supplied",
        "name": "개역개정",
        "aliases": ("개역개정", "KRV", "bible_krv.txt"),
        "filename": "bible_krv.txt",
        "license": "사용자 보유 사본의 이용조건",
        "requires_catalog": True,
    },
    {
        "edition_id": "krv-1961",
        "name": "개역한글판 (1961)",
        "aliases": ("개역한글", "개역한글판", "KRV-1961", "bible_korean.txt"),
        "filename": "bible_korean.txt",
        "license": "원배포처·출처 고지 조건 확인 필요",
    },
    {
        "edition_id": "web",
        "name": "World English Bible",
        "aliases": ("WEB", "World English Bible", "web.txt"),
        "filename": "web.txt",
        "license": "원배포처·출처 고지 조건 확인 필요",
    },
)


def _norm(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").strip().lower()
    return re.sub(r"[\s.·_-]+", "", value)


def _book_aliases(book: Dict[str, Any]) -> Iterable[str]:
    yield book["step"]
    yield book["step"].lower()
    yield from book["ko"]
    yield from book["en"]
    if book["step"] == "Psa":
        yield "ps"
        yield "psalm"
        yield "psalms"
    if book["step"] == "Mrk":
        yield "mark"
        yield "mrk"
    if book["step"] == "Luk":
        yield "luke"
        yield "luk"
    if book["step"] == "Jhn":
        yield "john"
        yield "jhn"


BOOK_BY_ALIAS: Dict[str, Dict[str, Any]] = {}
for _book in BOOKS:
    for _alias in _book_aliases(_book):
        BOOK_BY_ALIAS[_norm(_alias)] = _book


def _book(value: str) -> Optional[Dict[str, Any]]:
    return BOOK_BY_ALIAS.get(_norm(value))


def _book_display(book: Dict[str, Any]) -> str:
    return str(book["ko"][1])


def _canonical_ref(book: Dict[str, Any], chapter: int, verse: int) -> str:
    return f"{book['step']} {chapter}:{verse}"


def _parse_reference(ref: str) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """Return ``(book, start, end)`` or a structured parse error."""

    pattern = re.compile(
        r"^(.+?)\s*(\d+)\s*:\s*(\d+)"
        r"(?:\s*-\s*(?:(\d+)\s*:\s*)?(\d+))?$"
    )
    match = pattern.match((ref or "").strip())
    if not match:
        return None, None, {"code": "invalid_reference", "message": "장절 형식을 읽을 수 없습니다. 예: 요3:16 또는 John 3:16"}
    book = _book(match.group(1))
    if book is None:
        return None, None, {"code": "unknown_book", "message": f"알 수 없는 성경 책입니다: {match.group(1).strip()}"}
    start = {"chapter": int(match.group(2)), "verse": int(match.group(3))}
    end_chapter = int(match.group(4)) if match.group(4) else start["chapter"]
    end = {"chapter": end_chapter, "verse": int(match.group(5)) if match.group(5) else start["verse"]}
    if start["chapter"] < 1 or start["verse"] < 1 or end["chapter"] < 1 or end["verse"] < 1:
        return None, None, {"code": "invalid_reference", "message": "장과 절은 1 이상이어야 합니다."}
    if end["chapter"] != start["chapter"]:
        return book, {"start": start, "end": end}, {
            "code": "cross_chapter_unsupported",
            "message": "현재 어댑터는 같은 장 안의 범위만 지원합니다. 장별로 나누어 다시 요청하십시오.",
        }
    if end["verse"] < start["verse"]:
        return None, None, {"code": "invalid_range", "message": "끝 절이 시작 절보다 앞섭니다."}
    return book, {"start": start, "end": end}, None


def _requested_verses(book: Dict[str, Any], span: Dict[str, Any]) -> List[Dict[str, Any]]:
    start, end = span["start"], span["end"]
    return [
        {
            "step": book["step"],
            "book": _book_display(book),
            "testament": book["testament"],
            "chapter": chapter,
            "verse": verse,
            "ref": _canonical_ref(book, chapter, verse),
        }
        for chapter in range(start["chapter"], end["chapter"] + 1)
        for verse in range(
            start["verse"] if chapter == start["chapter"] else 1,
            end["verse"] + 1 if chapter == end["chapter"] else 1,
        )
    ]


def _read_json(path: Path) -> Optional[Dict[str, Any]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _catalog_path(root: Path) -> Optional[Path]:
    for candidate in (root / "_exegete" / "catalog.json", root / "catalog.json"):
        if candidate.is_file():
            return candidate
    return None


def _catalog(root: Path) -> Dict[str, Any]:
    path = _catalog_path(root)
    return _read_json(path) if path else {}


def _frontmatter_value(path: Path, key: str) -> Optional[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    for line in text.splitlines()[1:]:
        if line.strip() == "---":
            break
        match = re.match(rf"^{re.escape(key)}\s*:\s*[\"']?([^#\"']+?)[\"']?\s*$", line)
        if match:
            return match.group(1).strip()
    return None


def _preferred_edition(foundation_path: Optional[Path]) -> str:
    path = foundation_path or REPO_ROOT / "core" / "foundation.md"
    return _frontmatter_value(path, "preferred_bible") or "개역개정"


def _relative_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        try:
            return os.path.relpath(path.resolve(), Path.cwd().resolve()).replace(os.sep, "/")
        except ValueError:
            return path.name


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _warning(code: str, message: str, **extra: Any) -> Dict[str, Any]:
    item = {"code": code, "message": message}
    item.update(extra)
    return item


def _source_record(
    path: Path,
    *,
    kind: str,
    metadata: Optional[Dict[str, Any]] = None,
    record_keys: Optional[Sequence[str]] = None,
) -> Dict[str, Any]:
    metadata = metadata or {}
    record = {
        "kind": kind,
        "provider": metadata.get("provider", "unknown"),
        "source_url": metadata.get("source_url") or metadata.get("url"),
        "dataset_id": metadata.get("dataset_id"),
        "edition_id": metadata.get("edition_id"),
        "revision": metadata.get("revision", "unknown"),
        "license": metadata.get("license", "user-supplied or unspecified"),
        "relative_path": _relative_path(path),
        "sha256": _sha256(path),
    }
    if record_keys:
        record["record_keys"] = list(record_keys)
    return record


def _edition_matches(entry: Dict[str, Any], requested: str) -> bool:
    aliases = [entry.get("edition_id"), entry.get("name")] + list(entry.get("aliases", []))
    wanted = _norm(requested)
    return any(alias and _norm(str(alias)) == wanted for alias in aliases)


def _known_edition(requested: str) -> Optional[Dict[str, Any]]:
    wanted = _norm(requested)
    for entry in KNOWN_EDITIONS:
        if any(_norm(alias) == wanted for alias in entry["aliases"]):
            return dict(entry)
    return None


def _select_passage_file(
    data_root: Path,
    requested_edition: str,
    explicit_file: Optional[Path],
) -> Tuple[Optional[Path], Dict[str, Any], List[Dict[str, Any]]]:
    warnings: List[Dict[str, Any]] = []
    catalog = _catalog(data_root)
    editions = catalog.get("editions", []) if isinstance(catalog.get("editions", []), list) else []

    if explicit_file is not None:
        path = explicit_file.expanduser().resolve()
        if not path.is_file():
            return None, {"requested_edition": requested_edition}, [
                _warning("edition_file_missing", f"지정한 본문 파일이 없습니다: {path}")
            ]
        metadata: Dict[str, Any] = {}
        for entry in editions:
            if not isinstance(entry, dict):
                continue
            candidate = data_root / str(entry.get("file", ""))
            if candidate.resolve() == path:
                metadata = dict(entry)
                break
        metadata.setdefault("edition_id", _norm(requested_edition) or "user-supplied")
        metadata.setdefault("name", requested_edition)
        metadata.setdefault("format", "verse_lines")
        return path, metadata, warnings

    matching = [entry for entry in editions if isinstance(entry, dict) and _edition_matches(entry, requested_edition)]
    if len(matching) > 1:
        return None, {"requested_edition": requested_edition}, [
            _warning("ambiguous_edition", f"역본 식별자가 여러 파일과 일치합니다: {requested_edition}")
        ]
    if matching:
        metadata = dict(matching[0])
        file_value = metadata.get("file")
        if not file_value:
            return None, metadata, [_warning("edition_file_missing", "역본 카탈로그 항목에 file이 없습니다.")]
        path = (data_root / str(file_value)).resolve()
        if not path.is_file():
            return None, metadata, [
                _warning("edition_file_missing", f"카탈로그가 가리키는 본문 파일이 없습니다: {file_value}")
            ]
        return path, metadata, warnings

    known = _known_edition(requested_edition)
    if known:
        path = (data_root / known["filename"]).resolve()
        if path.is_file():
            if known.get("requires_catalog"):
                return None, known, [
                    _warning(
                        "edition_metadata_missing",
                        f"{requested_edition} 파일은 식별자·공급자·revision을 카탈로그에 등록한 뒤 사용하십시오: data/scripture/_exegete/catalog.json",
                    )
                ]
            return path, known, warnings
        return None, known, [
            _warning(
                "edition_unavailable",
                f"요청한 역본이 로컬 슬롯에 없습니다: {requested_edition}. 다른 역본으로 자동 대체하지 않습니다.",
            )
        ]

    return None, {"requested_edition": requested_edition}, [
        _warning(
            "unregistered_edition",
            f"역본 메타데이터가 없습니다: {requested_edition}. data/scripture/_exegete/catalog.json에 등록하십시오.",
        )
    ]


def _parse_passage_line(
    line: str,
    aliases: Dict[str, Dict[str, Any]],
    default_book: Optional[str],
) -> Optional[Tuple[Tuple[str, int, int], Dict[str, Any]]]:
    raw = line.strip()
    if not raw or raw.startswith("#"):
        return None

    short = re.match(r"^(\d+)\s*:\s*(\d+)\s+(.+)$", raw)
    if short:
        book = aliases.get(_norm(default_book or ""))
        if book is None:
            return None
        chapter, verse, body = int(short.group(1)), int(short.group(2)), short.group(3)
        record_key = raw[: short.start(3)].strip()
    else:
        match = re.match(r"^(.+?)\s*(\d+)\s*:\s*(\d+)\s+(.+)$", raw)
        if not match:
            return None
        book = aliases.get(_norm(match.group(1)))
        if book is None:
            return None
        chapter, verse, body = int(match.group(2)), int(match.group(3)), match.group(4)
        record_key = raw[: match.start(4)].strip()

    heading = None
    heading_match = re.match(r"^<([^>]+)>\s*(.*)$", body)
    if heading_match:
        heading, body = heading_match.group(1).strip(), heading_match.group(2).strip()
    return (book["step"], chapter, verse), {
        "step": book["step"],
        "book": _book_display(book),
        "chapter": chapter,
        "verse": verse,
        "ref": _canonical_ref(book, chapter, verse),
        "record_key": record_key,
        "heading": heading,
        "text": body,
    }


def _passage_component(
    requested: List[Dict[str, Any]],
    data_root: Path,
    requested_edition: str,
    explicit_file: Optional[Path],
) -> Dict[str, Any]:
    path, metadata, warnings = _select_passage_file(data_root, requested_edition, explicit_file)
    base: Dict[str, Any] = {
        "status": STATUS_UNAVAILABLE,
        "requested_edition": requested_edition,
        "edition": {
            "edition_id": metadata.get("edition_id"),
            "name": metadata.get("name", requested_edition),
            "provider": metadata.get("provider", "unknown"),
            "revision": metadata.get("revision", "unknown"),
        },
        "requested_verses": requested,
        "resolved_verses": [],
        "missing_verses": list(requested),
        "sources": [],
        "warnings": warnings,
    }
    if path is None:
        return base

    aliases = BOOK_BY_ALIAS
    default_book = metadata.get("book")
    records: Dict[Tuple[str, int, int], Dict[str, Any]] = {}
    duplicate_keys: List[str] = []
    malformed_count = 0
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as error:
        base["warnings"].append(_warning("passage_read_error", f"본문 파일을 읽지 못했습니다: {error}"))
        base["status"] = STATUS_ERROR
        return base

    for line_number, line in enumerate(lines, 1):
        parsed = _parse_passage_line(line, aliases, default_book)
        if parsed is None:
            if line.strip() and not line.lstrip().startswith("#"):
                malformed_count += 1
            continue
        key, record = parsed
        if key in records:
            duplicate_keys.append(record["ref"])
            continue
        records[key] = {**record, "line": line_number, "target": False}

    if malformed_count:
        base["warnings"].append(
            _warning("malformed_passage_lines", f"본문 파일에서 해석하지 못한 행이 {malformed_count}개 있습니다.")
        )
    if duplicate_keys:
        base["warnings"].append(
            _warning("duplicate_verses", "같은 장절이 중복되어 첫 번째 행만 사용했습니다.", refs=duplicate_keys)
        )

    resolved: List[Dict[str, Any]] = []
    missing: List[Dict[str, Any]] = []
    wanted_keys = {(item["step"], item["chapter"], item["verse"]): item for item in requested}
    for key, item in wanted_keys.items():
        if key in records:
            resolved.append({**records[key], "target": True})
        else:
            missing.append(item)
    resolved.sort(key=lambda item: (item["chapter"], item["verse"]))
    base["resolved_verses"] = resolved
    base["missing_verses"] = missing
    base["sources"] = [
        _source_record(
            path,
            kind="passage",
            metadata=metadata,
            record_keys=[item.get("record_key", item["ref"]) for item in resolved],
        )
    ]
    if missing or duplicate_keys:
        base["status"] = STATUS_PARTIAL
        if missing:
            base["warnings"].append(
                _warning("missing_verses", "요청한 절 가운데 본문 파일에서 찾지 못한 절이 있습니다.", refs=[item["ref"] for item in missing])
            )
    else:
        base["status"] = STATUS_OK
    return base


def _source_entries(source_root: Path) -> List[Tuple[Path, Dict[str, Any], str]]:
    catalog = _catalog(source_root)
    datasets = catalog.get("datasets", []) if isinstance(catalog.get("datasets", []), list) else []
    found: List[Tuple[Path, Dict[str, Any], str]] = []
    seen: set = set()

    for dataset in datasets:
        if not isinstance(dataset, dict):
            continue
        root_value = dataset.get("root", "")
        root = (source_root / str(root_value)).resolve() if root_value else source_root.resolve()
        file_values = dataset.get("files")
        paths: Iterable[Path]
        if isinstance(file_values, list) and file_values:
            paths = [(root / str(value)).resolve() for value in file_values]
        else:
            paths = (
                [path for suffix in ("*.txt", "*.tsv") for path in root.rglob(suffix)]
                if root.is_dir()
                else ()
            )
        language = str(dataset.get("language", "")).lower()
        if not language:
            root_name = str(root).lower()
            language = "greek" if "greek" in root_name else "hebrew" if "hebrew" in root_name else ""
        for path in paths:
            if not path.is_file() or path.resolve() in seen:
                continue
            seen.add(path.resolve())
            found.append((path, dict(dataset), language))

    if not found and source_root.is_dir():
        for path in sorted(
            [path for suffix in ("*.txt", "*.tsv") for path in source_root.rglob(suffix)]
        ):
            lowered = "/".join(part.lower() for part in path.parts)
            if "greek" in lowered or "hebrew" in lowered:
                language = "greek" if "greek" in lowered else "hebrew"
                found.append((path, {}, language))
    return found


def _original_line(line: str, language: str) -> Optional[Tuple[str, Dict[str, Any]]]:
    match = re.match(r"^([A-Za-z0-9]+)\.(\d+)\.(\d+)#(\d+)[^\t]*\t(.*)$", line.strip())
    if not match:
        return None
    step, chapter, verse, index = match.group(1), int(match.group(2)), int(match.group(3)), int(match.group(4))
    book = _book(step)
    if book is None:
        return None
    fields = [field.strip() for field in match.group(5).split("\t")]
    record_key = f"{step}.{chapter}.{verse}#{index:02d}"
    if language.startswith("heb"):
        surface = fields[0] if fields else ""
        transliteration = fields[1] if len(fields) > 1 else ""
        gloss = fields[2] if len(fields) > 2 else ""
        strong = fields[3].strip("{}") if len(fields) > 3 else ""
        morphology = fields[4] if len(fields) > 4 else ""
        lemma = ""
        for field in fields[5:]:
            if re.search(r"[GH]\d+", field):
                lemma = field.strip("{}")
                break
        token = {
            "token_id": record_key,
            "record_key": line.strip().split("\t", 1)[0],
            "token_index": index,
            "language": "Hebrew",
            "ref": _canonical_ref(book, chapter, verse),
            "surface": surface,
            "transliteration": transliteration,
            "gloss": gloss,
            "strong": strong,
            "morphology": morphology,
            "raw_morphology": morphology,
            "lemma": lemma,
            "raw_fields": fields,
        }
    else:
        surface = fields[0] if fields else ""
        gloss = fields[1] if len(fields) > 1 else ""
        strong_parse = fields[2] if len(fields) > 2 else ""
        strong, morphology = (strong_parse.split("=", 1) + [""])[:2] if "=" in strong_parse else (strong_parse, "")
        lemma = fields[3] if len(fields) > 3 else ""
        token = {
            "token_id": record_key,
            "record_key": line.strip().split("\t", 1)[0],
            "token_index": index,
            "language": "Greek",
            "ref": _canonical_ref(book, chapter, verse),
            "surface": surface,
            "gloss": gloss,
            "strong": strong,
            "morphology": morphology,
            "raw_morphology": morphology,
            "lemma": lemma,
            "raw_fields": fields,
        }
    return f"{step}.{chapter}.{verse}", token


def _strong_numbers(value: str) -> List[str]:
    return re.findall(r"[GH]\d+[A-Za-z]?", value or "")


def _lexicon_file(source_root: Path, language: str) -> Optional[Path]:
    name = "greek" if language == "Greek" else "hebrew"
    candidates = (
        source_root / "lexicon" / f"{name}_lexicon.json",
        source_root / "_exegete" / "lexicon" / f"{name}_lexicon.json",
        source_root / "original" / "lexicon" / f"{name}_lexicon.json",
    )
    return next((path for path in candidates if path.is_file()), None)


def _annotate_lexicon(token: Dict[str, Any], path: Path) -> None:
    data = _read_json(path)
    if not data:
        return
    entries = data.get("entries", {}) if isinstance(data.get("entries", {}), dict) else {}
    by_base = data.get("by_base", {}) if isinstance(data.get("by_base", {}), dict) else {}
    results = []
    for strong in _strong_numbers(token.get("strong", "")):
        exact = entries.get(strong.upper())
        if exact:
            results.append({"query": strong, "entry": exact, "note": None})
            continue
        base_match = re.match(r"[GH]0*(\d+)", strong)
        candidates = by_base.get(base_match.group(1), []) if base_match else []
        if len(candidates) == 1 and candidates[0] in entries:
            results.append({"query": strong, "entry": entries[candidates[0]], "note": "기본 번호 단일 후보"})
        elif len(candidates) > 1:
            results.append({"query": strong, "entry": None, "note": f"동형이의어 후보 {len(candidates)}개 — 확인 필요"})
        else:
            results.append({"query": strong, "entry": None, "note": "사전에 없음 — 확인 필요"})
    if results:
        token["lexicon"] = results


def _original_component(requested: List[Dict[str, Any]], source_root: Path) -> Dict[str, Any]:
    language = "Greek" if requested and requested[0]["testament"] == "NT" else "Hebrew"
    language_key = language.lower()
    base: Dict[str, Any] = {
        "status": STATUS_UNAVAILABLE,
        "language": language,
        "dataset": None,
        "requested_verses": requested,
        "resolved_verses": [],
        "missing_verses": list(requested),
        "tokens": [],
        "sources": [],
        "warnings": [],
    }
    entries = [item for item in _source_entries(source_root) if item[2].startswith(language_key[:4])]
    if not entries:
        base["warnings"].append(
            _warning(
                "original_data_unavailable",
                f"{language} 원어 데이터가 없습니다. 설치 명령을 자동 실행하지 않습니다.",
            )
        )
        return base

    wanted = {(item["step"], item["chapter"], item["verse"]): item for item in requested}
    verse_tokens: Dict[Tuple[str, int, int], List[Dict[str, Any]]] = {}
    source_keys: Dict[Path, List[str]] = {}
    duplicate_tokens: List[str] = []
    lexicon_paths: Dict[Path, str] = {}
    for path, metadata, language_hint in entries:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError) as error:
            base["warnings"].append(_warning("original_read_error", f"원어 파일을 읽지 못했습니다: {error}"))
            continue
        for line in lines:
            parsed = _original_line(line, language_hint or language_key)
            if parsed is None:
                continue
            verse_key, token = parsed
            step, chapter, verse = verse_key.split(".")
            key = (step, int(chapter), int(verse))
            if key not in wanted:
                continue
            token_id = token["token_id"]
            if any(existing["token_id"] == token_id for existing in verse_tokens.get(key, [])):
                duplicate_tokens.append(token_id)
                continue
            verse_tokens.setdefault(key, []).append(token)
            source_keys.setdefault(path, []).append(token.get("record_key", token_id))
            lexicon = _lexicon_file(source_root, language)
            if lexicon:
                _annotate_lexicon(token, lexicon)
                lexicon_paths[lexicon] = language

    resolved = []
    missing = []
    flat_tokens: List[Dict[str, Any]] = []
    for item in requested:
        key = (item["step"], item["chapter"], item["verse"])
        tokens = sorted(verse_tokens.get(key, []), key=lambda value: value["token_index"])
        if tokens:
            resolved.append({**item, "tokens": tokens})
            flat_tokens.extend(tokens)
        else:
            missing.append(item)
    base["resolved_verses"] = resolved
    base["missing_verses"] = missing
    base["tokens"] = flat_tokens
    if duplicate_tokens:
        base["warnings"].append(
            _warning("duplicate_original_tokens", "원어 데이터에 중복 토큰이 있어 첫 항목만 사용했습니다.", token_ids=duplicate_tokens)
        )
    for path, metadata, _ in entries:
        keys = source_keys.get(path)
        if keys:
            base["sources"].append(_source_record(path, kind="original_language", metadata=metadata, record_keys=keys))
            if base["dataset"] is None:
                base["dataset"] = {
                    "dataset_id": metadata.get("dataset_id", "unknown"),
                    "edition_id": metadata.get("edition_id"),
                    "provider": metadata.get("provider", "unknown"),
                    "revision": metadata.get("revision", "unknown"),
                    "license": metadata.get("license", "user-supplied or unspecified"),
                }
    for path in lexicon_paths:
        base["sources"].append(
            _source_record(
                path,
                kind="lexicon",
                metadata={"provider": "local lexicon", "revision": "user-supplied", "license": "user-supplied or unspecified"},
            )
        )
    if missing:
        base["status"] = STATUS_PARTIAL if resolved else STATUS_UNAVAILABLE
        base["warnings"].append(
            _warning("missing_original_verses", "요청한 절 가운데 원어 토큰을 찾지 못한 절이 있습니다.", refs=[item["ref"] for item in missing])
        )
    else:
        base["status"] = STATUS_OK
    return base


def _capability(available: bool, reason: Optional[str] = None, **extra: Any) -> Dict[str, Any]:
    value: Dict[str, Any] = {"available": available}
    if reason:
        value["reason"] = reason
    value.update(extra)
    return value


def _base_capabilities() -> Dict[str, Any]:
    return {
        "passage": _capability(False, "not_requested"),
        "original_text": _capability(False, "not_requested"),
        "morphology": _capability(False, "not_requested"),
        "lexicon": _capability(False, "not_requested"),
        "louw_nida": _capability(False, "P0 어댑터 범위 밖 — OpenGNT 미연결"),
        "discourse": _capability(False, "P0 어댑터 범위 밖 — OpenGNT 미연결"),
        "lxx": _capability(False, "P0 어댑터 범위 밖 — LXX 미연결"),
    }


def _error_evidence(
    ref: str,
    status: str,
    error: Dict[str, Any],
    *,
    kind: str,
    requested_edition: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "adapter": {"name": "pastor_adapter", "version": ADAPTER_VERSION, "upstream_sha": UPSTREAM_SHA},
        "request_ref": ref,
        "normalized_ref": None,
        "status": status,
        "error": error,
        "kind": kind,
        "requested_edition": requested_edition,
        "requested_verses": [],
        "resolved_verses": [],
        "missing_verses": [],
        "capabilities": _base_capabilities(),
        "sources": [],
        "warnings": [],
    }


def query(
    ref: str,
    *,
    kind: str = "all",
    data_root: Optional[Path] = None,
    source_root: Optional[Path] = None,
    edition: Optional[str] = None,
    bible_file: Optional[Path] = None,
    foundation_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """Return a structured evidence document for ``ref``.

    ``kind`` is ``passage``, ``original``, or ``all``.  No network operation,
    journal update, manifest write, or output-file write occurs here.
    """

    if kind not in {"passage", "original", "all"}:
        return _error_evidence(ref, STATUS_INVALID_REQUEST, {"code": "invalid_kind", "message": "kind은 passage, original, all 중 하나여야 합니다."}, kind=kind)
    book, span, parse_error = _parse_reference(ref)
    requested_edition = edition or _preferred_edition(foundation_path)
    if parse_error:
        return _error_evidence(ref, STATUS_INVALID_REQUEST, parse_error, kind=kind, requested_edition=requested_edition)
    assert book is not None and span is not None
    requested = _requested_verses(book, span)
    normalized = f"{book['step']} {span['start']['chapter']}:{span['start']['verse']}"
    if span["end"] != span["start"]:
        normalized += f"-{span['end']['verse']}"

    data_root = (data_root or REPO_ROOT / "data" / "scripture").expanduser().resolve()
    source_root = (source_root or data_root / "source").expanduser().resolve()
    evidence: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "adapter": {
            "name": "pastor_adapter",
            "version": ADAPTER_VERSION,
            "upstream_repository": UPSTREAM_REPOSITORY,
            "upstream_sha": UPSTREAM_SHA,
        },
        "request_ref": ref,
        "normalized_ref": normalized,
        "kind": kind,
        "status": STATUS_OK,
        "requested_edition": requested_edition,
        "requested_verses": requested,
        "resolved_verses": [],
        "missing_verses": [],
        "request": {
            "step": book["step"],
            "book": _book_display(book),
            "testament": book["testament"],
            "original_language": "Hebrew" if book["testament"] == "OT" else "Greek",
            "requested_verses": requested,
        },
        "capabilities": _base_capabilities(),
        "sources": [],
        "warnings": [],
    }

    passage: Optional[Dict[str, Any]] = None
    original: Optional[Dict[str, Any]] = None
    if kind in {"passage", "all"}:
        passage = _passage_component(requested, data_root, requested_edition, bible_file)
        evidence["passage"] = passage
        evidence["capabilities"]["passage"] = _capability(
            passage["status"] == STATUS_OK,
            None if passage["status"] == STATUS_OK else "본문 전문이 없거나 요청 범위가 부분적으로 누락되었습니다.",
            complete=passage["status"] == STATUS_OK,
            edition_id=passage["edition"].get("edition_id"),
        )
        evidence["sources"].extend(passage.get("sources", []))
        evidence["warnings"].extend(passage.get("warnings", []))

    if kind in {"original", "all"}:
        original = _original_component(requested, source_root)
        evidence["original_language"] = original
        original_ok = original["status"] == STATUS_OK
        evidence["capabilities"]["original_text"] = _capability(
            bool(original.get("tokens")),
            None if original.get("tokens") else "원어 데이터가 없습니다.",
            complete=original_ok,
            language=original.get("language"),
        )
        has_morphology = any(token.get("raw_morphology") for token in original.get("tokens", []))
        evidence["capabilities"]["morphology"] = _capability(
            has_morphology,
            None if has_morphology else "형태소 데이터가 없습니다.",
            complete=has_morphology and original_ok,
            language=original.get("language"),
        )
        has_lexicon = any("lexicon" in token for token in original.get("tokens", []))
        evidence["capabilities"]["lexicon"] = _capability(
            has_lexicon,
            None if has_lexicon else "사전 데이터가 없거나 조회되지 않았습니다.",
            complete=has_lexicon and original_ok,
            language=original.get("language"),
        )
        evidence["sources"].extend(original.get("sources", []))
        evidence["warnings"].extend(original.get("warnings", []))

    if kind == "passage":
        evidence["status"] = passage["status"] if passage else STATUS_ERROR
        if passage:
            evidence["resolved_verses"] = passage["resolved_verses"]
            evidence["missing_verses"] = passage["missing_verses"]
    elif kind == "original":
        evidence["status"] = original["status"] if original else STATUS_ERROR
        if original:
            evidence["resolved_verses"] = original["resolved_verses"]
            evidence["missing_verses"] = original["missing_verses"]
    else:
        # Passage availability is the primary result.  Optional original
        # language data being absent is exposed in its component/capability
        # fields and does not make an otherwise valid text lookup fail.
        evidence["status"] = passage["status"] if passage else STATUS_ERROR
        if passage:
            evidence["resolved_verses"] = passage["resolved_verses"]
            evidence["missing_verses"] = passage["missing_verses"]
        if original and original["status"] == STATUS_PARTIAL and evidence["status"] == STATUS_OK:
            evidence["warnings"].append(_warning("optional_original_partial", "본문은 완전하지만 원어 범위는 부분적으로만 확보되었습니다."))

    evidence["warnings"] = _dedupe_warnings(evidence["warnings"])
    evidence["sources"] = _dedupe_sources(evidence["sources"])
    return evidence


def _dedupe_warnings(warnings: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    seen = set()
    for warning in warnings:
        marker = json.dumps(warning, ensure_ascii=False, sort_keys=True)
        if marker not in seen:
            result.append(warning)
            seen.add(marker)
    return result


def _dedupe_sources(sources: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    seen = set()
    for source in sources:
        marker = (source.get("kind"), source.get("relative_path"), source.get("sha256"))
        if marker not in seen:
            result.append(source)
            seen.add(marker)
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Pastor-KR evidence adapter")
    parser.add_argument("ref", nargs="?", help="장절, 예: 요3:16 또는 Gen 1:1")
    parser.add_argument("--kind", choices=("passage", "original", "all"), default="all")
    parser.add_argument("--edition", help="요청 역본. 생략하면 foundation.md의 preferred_bible")
    parser.add_argument("--bible-file", type=Path, help="사용자가 명시한 본문 파일")
    parser.add_argument("--data-root", type=Path, help="본문 슬롯 루트")
    parser.add_argument("--source-root", type=Path, help="원어 데이터 루트")
    parser.add_argument("--foundation", type=Path, help="preferred_bible을 읽을 foundation.md")
    args = parser.parse_args(argv)

    if not args.ref:
        evidence = _error_evidence(
            "",
            STATUS_INVALID_REQUEST,
            {"code": "missing_reference", "message": "장절을 지정하십시오. 예: 요3:16"},
            kind=args.kind,
            requested_edition=args.edition,
        )
    else:
        try:
            evidence = query(
                args.ref,
                kind=args.kind,
                data_root=args.data_root,
                source_root=args.source_root,
                edition=args.edition,
                bible_file=args.bible_file,
                foundation_path=args.foundation,
            )
        except Exception as error:  # keep stdout a machine-readable contract
            evidence = _error_evidence(
                args.ref,
                STATUS_ERROR,
                {"code": "adapter_error", "message": str(error)},
                kind=args.kind,
                requested_edition=args.edition,
            )
    print(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True))
    return EXIT_CODES.get(evidence.get("status"), EXIT_CODES[STATUS_ERROR])


if __name__ == "__main__":
    raise SystemExit(main())
