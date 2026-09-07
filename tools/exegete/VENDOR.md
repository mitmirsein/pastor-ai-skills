# Exegete integration record

## Upstream pin

- Repository: `https://github.com/worlyung/exegete`
- Reviewed commit: `6e32717fa6ee012e08d760a066f0f66a723d0bc4`
- Reviewed interfaces: `src/lookup.py`, `src/greek_lookup.py`, `src/hebrew_lookup.py`, `src/lexicon.py`, `src/data/book_abbrev.json`, and `setup_data.py`
- Upstream code license: MIT

`pastor_adapter.py` is a Pastor-KR boundary adapter. It does not copy the
upstream scripts into the skill repository and does not treat an upstream
default as a safe translation choice. It implements the stable verse-line and
STEPBible token formats after reviewing the pinned sources, then adds the
Pastor-specific requirements that the upstream command-line tools do not
provide: explicit edition selection, separate component status, source URLs,
source hashes, record keys, and structured failure output.

If an upstream format changes, update the pin and the fixture tests together.
Do not update the pin by changing a URL to a moving branch.

| Pinned interface | Pastor-KR decision |
|---|---|
| `src/lookup.py` and `src/data/book_abbrev.json` | Reference formats and book aliases were reviewed; the adapter keeps its own Korean/English map so the runtime has no untracked import. |
| `src/greek_lookup.py` and `src/hebrew_lookup.py` | STEPBible token fields are parsed by the adapter with separate Greek/Hebrew capability results. |
| `src/lexicon.py` | Lexicon lookup is an optional local JSON index; exact Strong keys are preferred and ambiguous base-number matches remain unresolved. |
| `setup_data.py` | Not copied. `tools/exegete/setup_data.py` requires an explicit manifest and exact SHA-256 values before installation. |
| `export_exegesis_docx.py` | Not adopted in P0. Pastor audit-linked Word output remains the separate P1-E feature. |

The adapter uses Python standard-library modules only. No upstream package,
runtime router, or upstream state file is imported into the Pastor-KR skill
flow.

## Data policy

No Bible, original-language, lexicon, LXX, or OpenGNT data is bundled here.
The ignored slots under `data/scripture/` are user-local inputs. A data source
is accepted only when its catalog records its provider, revision, license, and
the local file hash is emitted by the adapter at query time.

The adapter never downloads data during lookup. Installation and cache
regeneration must be explicit, atomic, and directed at derived files only.
`setup_data.py` accepts a manifest with an exact URL and SHA-256 per file,
stages each download, refuses an existing hash mismatch, and writes an
optional catalog only after the data files verify. User source files are not
replaced by a failed or partial download.

## Compatibility notes

- Pastor-KR's default is read from `core/foundation.md` (`preferred_bible`).
- A missing requested edition is `unavailable`; `개역개정` is never silently
  replaced with `개역한글` or WEB.
- Existing book-specific files (`3:16 본문` with a catalog `book`) and
  upstream-style integrated files (`요3:16 본문`, `Jhn 3:16 text`) are read.
- Same-book, same-chapter ranges are supported. Cross-chapter ranges return a
  structured `invalid_request` result until a split-range contract is added.
- Greek and Hebrew morphology are returned independently. OpenGNT/Louw-Nida,
  discourse data, and LXX remain explicit unavailable capabilities in P0.
- Word/한컴 export is intentionally outside this adapter phase. It remains a
  separate P1-E feature that must recheck the current manuscript and audit
  hashes before producing a document.

## Patch and rollback record

The Pastor adapter is additive. No upstream files, journal records,
lineage manifests, or user data are modified by a lookup. To roll back, stop
calling `pastor_adapter.py`; the existing `data/scripture/` and pasted-text
fallback described in `core/_hooks.md` remain valid.
