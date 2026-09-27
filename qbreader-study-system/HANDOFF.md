# HANDOFF — qbreader-study-system (cloud → local Windows)

Prepared 2026-09-27 at the end of a Claude Code cloud session.
Read this first, then `CLAUDE.md` (project rules) and `PROGRESS.md`
(detailed status, API findings, design for the remaining work).

## One-line status
**Foundation only.** Config, database schema, and record-storage code exist
and pass 24 automated tests on synthetic data. There is **no downloader,
command-line interface, launcher, classifier workflow, taxonomy file,
source ingestion, or clue research yet**, and **no real QBReader data has
ever been downloaded**.

## Project scope — keep this
Only QBReader questions with question-level `difficulty` **6, 7, 8, 9, or 10**
are processed (classified, indexed, used for clue extraction and novelty
comparison, exported). This is stored in:
- `config/settings.toml` → `[scope] difficulties = [6, 7, 8, 9, 10]`
- the database table `scope_difficulties` (re-synced from config on open)
  and the SQL view `eligible_questions` that all processing must use
- `CLAUDE.md` (rules Claude Code reads automatically)

Other difficulties are kept only as raw data. Missing, invalid, or
question-vs-set conflicting difficulty values are kept separate and
reported (`difficulty_status`), never guessed. Novelty must be described as
"not found in the QBReader difficulty 6-10 collection".

## What is implemented
| File | What it does |
|---|---|
| `config/settings.toml` | Scope 6-10, QBReader API settings (2 req/s; documented limit is 20), paid model API **off** |
| `src/qbstudy/config.py` | Loads settings + optional `config/settings.local.toml`; rejects invalid scope and >20 req/s |
| `src/qbstudy/migrations/0001_initial.sql` | Full planned schema (raw, QBReader records, scope view, downloads, search index, taxonomy, entities, AI batches, classifications, sources, claims, comparisons, clue records, review log) |
| `src/qbstudy/db.py` | Opens SQLite; applies numbered migrations atomically; refuses edited migrations (checksum); syncs scope with history |
| `src/qbstudy/records.py` | Stores tossups/bonuses/packets/sets: raw JSON preserved, duplicate prevention, change detection with version history, difficulty status incl. conflicts, bonus parts (incl. part/answer count mismatch), missing-from-source flag, MongoDB Extended JSON decoding (for official backups); QBReader category lists |
| `src/qbstudy/textutil.py` | HTML stripping, normalization, stemming, clue-sentence splitting, answerline parsing (main / alternates / prompts / rejects), hedge-word detection |
| `tests/test_foundation.py` | 24 pytest tests (below) |

Category definitions: only QBReader's own category / subcategory /
alternate-subcategory lists exist (copied from QBReader's source into
`records.py`). The versioned starter taxonomy with microcategories
(`taxonomy/taxonomy_v1.json`) is **not written yet**.

## What was actually tested
Environment: Linux cloud container, Python 3.11.15, SQLite 3.45.1,
pytest 9.1.1. Command: `.venv/bin/python -m pytest` → **24 passed**.

Covered (synthetic records shaped like the documented QBReader schema):
- scope is exactly 6-10; config rejects difficulty 11 and 25 req/s
- migrations apply once, re-run is a no-op, tampered migration refused
- repeated import → no duplicates (5 new, then 0 new / 5 unchanged)
- edited record → detected as changed, both raw versions kept
- difficulty 8 eligible; 3 excluded; question 9 in a difficulty-8 set →
  `conflict`; no difficulty → `missing`; `"6"`, 6.5, 11, `true` → `invalid`
- bonus with 3 parts / 2 answers stored and flagged
- foreign-key check clean; missing-from-source flagged, not deleted
- invalid record rejected without crashing; Extended JSON decoded
- answerline parsing, sentence splitting, stemming, hedge detection

**Not tested anywhere:** Windows (nothing has been run on Windows), real
QBReader responses, network behavior, anything not listed above.

## What is blocked (and how to unblock)
1. **QBReader access** — the cloud environment's network policy blocked
   `www.qbreader.org` (proxy 403). On your Windows PC it should work
   normally; verify first (step 4 below).
2. **Private GitHub repo** — the Claude GitHub integration could not create
   repositories (403). Code is currently on the **public** repo
   `ToxicReddit/Claude1111`, branch `claude/new-session-zjgigh`, folder
   `qbreader-study-system/`. To go private: create `qbreader-study-system`
   (Private, no README) at https://github.com/new, then from the unzipped
   folder: `git init`, `git add .`, `git commit -m "Import"`,
   `git remote add origin https://github.com/ToxicReddit/qbreader-study-system.git`,
   `git push -u origin main` (or ask local Claude Code to do it).
3. **AI model API** — no credential configured; real AI classification has
   never been run. The planned provider uses the official `anthropic`
   package and stays off unless you set `allow_paid_api = true` in
   `config/settings.local.toml`. A Claude subscription does not
   automatically include API credits.

## How to continue on Windows
1. Install Python 3.11 or newer from https://www.python.org/downloads/
   (tick **"Add python.exe to PATH"**). Check in PowerShell: `py -3 --version`
2. Unzip this archive, e.g. to `C:\Users\<you>\Projects\qbreader-study-system`.
3. In PowerShell, inside that folder:
   ```powershell
   py -3 -m venv .venv
   .venv\Scripts\python -m pip install -r requirements-dev.txt
   .venv\Scripts\python -m pytest
   ```
   Expect `24 passed`. If anything fails, that is the first Windows issue
   to fix (paths, encodings).
4. Check QBReader is reachable from your PC:
   ```powershell
   curl.exe -s -o NUL -w "%{http_code}`n" "https://www.qbreader.org/api/set-list"
   ```
   `200` means the downloader can be built and piloted for real.
5. Open the folder in Claude Code and say, for example:
   *"Read HANDOFF.md, CLAUDE.md and PROGRESS.md, then continue with
   'Remaining work' item 1 (API client), keeping the difficulty 6-10 scope.
   Run a small real pilot download before anything large."*
6. Keep private material out of Git: your textbooks/PDFs go in
   `local-sources\`, generated data in `local-data\` (both ignored).

## Build order for the remaining work
(Full design in PROGRESS.md → "Remaining work".)
1. API client (throttle, retry/backoff, 429 handling) → 2. downloader with
checkpoints, pilot, update, coverage → 3. backup import → 4. search index
(eligible only) → 5. taxonomy v1 → 6. classification batch export/import +
providers + reviewed pilot → 7. sources/claims/comparison/clue records/
ladder → 8. CLI + Windows launcher (`qbstudy.bat`) + README → 9. tests for
every failure case in the original specification + validation report.

## What this ZIP contains / excludes
Contains: code, config, schema, docs (this file, CLAUDE.md, PROGRESS.md),
tests, dependency lists. Excludes: `.venv/`, `__pycache__/`,
`.pytest_cache/`, credentials (none exist), databases and downloaded data
(none exist). The QBReader source clone used for API research is not
included; re-clone with `git clone --depth 1 https://github.com/qbreader/website`
if needed.
