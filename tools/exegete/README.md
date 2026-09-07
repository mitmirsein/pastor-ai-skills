# Pastor-KR Exegete adapter

`pastor_adapter.py` is the optional local evidence bridge for Pastor-KR. It
returns JSON for a requested Bible reference and keeps the primary Korean
passage result separate from optional original-language evidence.

It performs no network access and writes no files.

Data installation is a separate explicit operation. Prepare a manifest with
`url`, `relative_path`, and `sha256` for every file, then run:

```bash
python3 tools/exegete/setup_data.py /secure/path/manifest.json \
  --destination data/scripture/source
```

The installer stages and hashes downloads, refuses to replace an existing
file with a different hash, and can write a catalog supplied in the manifest.
It does not provide a default download list or infer a license.

The manifest may carry the catalog that describes the installed files. The
catalog is written only after every file passes its declared hash:

```json
{
  "files": [
    {
      "url": "https://example.invalid/data.txt",
      "relative_path": "original/greek/tagnt.txt",
      "sha256": "64-character-lowercase-sha256"
    }
  ],
  "catalog": {
    "datasets": [
      {
        "dataset_id": "example-tagnt",
        "language": "Greek",
        "root": "original/greek",
        "provider": "source provider",
        "revision": "fixed revision",
        "license": "license identifier"
      }
    ]
  }
}
```

```bash
python3 tools/exegete/pastor_adapter.py '요3:16' --kind all --edition '개역개정'
python3 tools/exegete/pastor_adapter.py 'Jhn 3:16' --kind original
python3 tools/exegete/pastor_adapter.py '창1:1' --kind passage --edition '개역개정'
```

The command writes one JSON object to standard output. Diagnostics are inside
`warnings`; a shell caller can use the process exit code as follows:

| Status | Exit | Meaning |
|---|---:|---|
| `ok` | 0 | Requested component is complete |
| `partial` | 1 | At least one requested verse or record is missing/duplicated |
| `invalid_request` | 2 | Reference or option cannot be used |
| `unavailable` | 3 | The requested local edition/data is absent |
| `error` | 4 | Local read or adapter failure |

## Data registration

An ignored `data/scripture/_exegete/catalog.json` may register editions:

```json
{
  "editions": [
    {
      "edition_id": "krv-1998",
      "name": "개역개정",
      "aliases": ["개역개정"],
      "file": "bible_krv.txt",
      "provider": "대한성서공회",
      "source_url": "원배포처 URL",
      "revision": "user-supplied",
      "license": "user-held copy"
    }
  ]
}
```

Original-language data can use the same pattern at
`data/scripture/source/_exegete/catalog.json`:

```json
{
  "datasets": [
    {
      "dataset_id": "stepbible-tagnt",
      "language": "Greek",
      "root": "original/greek",
      "provider": "Tyndale House / STEPBible",
      "source_url": "https://github.com/STEPBible/STEPBible-Data",
      "revision": "pinned by VENDOR.md",
      "license": "CC BY 4.0"
    }
  ]
}
```

The adapter preserves the requested edition and reports a missing edition. It
does not select another local file merely because it happens to exist.

## Evidence contract

Every successful or unsuccessful response contains `schema_version`,
`request_ref`, `normalized_ref`, `status`, `capabilities`, `requested_verses`,
`resolved_verses`, `missing_verses`, `sources`, and `warnings` at the top level
and in the relevant component. `sources` contains a provider URL when the
catalog supplies one, a relative path, SHA-256, dataset/edition metadata, and
resolved record keys. A text result is not treated as a
morphology result unless the original-language component reports that
capability separately.

This JSON is evidence for `sermon-research` and `sermon_audit`; it does not
write `pastor_journal.md`, `_manifest.md`, `stage`, or a Word document.
Word/한컴 export is a separate follow-up feature and is not part of this P0
adapter.
