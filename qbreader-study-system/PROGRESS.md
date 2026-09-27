# PROGRESS — qbreader-study-system

Last updated: 2026-09-27 (cloud session). Status: **early build, paused on
the user's request.** This is NOT yet a working end-to-end system: there is
no downloader, CLI, launcher, classifier workflow, taxonomy file, or source
ingestion yet. What exists is the foundation listed below, covered by 24
pytest tests (tests/test_foundation.py). See HANDOFF.md for the Windows move.

## Where things are
- Code lives in this folder (`qbreader-study-system/`) on branch
  `claude/new-session-zjgigh` of GitHub repo `ToxicReddit/Claude1111`.
  That repo is **public**. The user first chose a new private repo, but
  the Claude GitHub integration may not create repositories (403). The user
  then asked to save to the connected repo.
- Nothing else in `ToxicReddit/Claude1111` (the chemistry Anki decks) was
  touched.
- The cloud container is temporary: anything not pushed is lost. No
  databases or QBReader data were created except in-memory test runs.

## Completed and verified (cloud, Linux, Python 3.11.15, SQLite 3.45.1)
1. **API research** (from QBReader's official source, `qbreader/website`, commit
   0d0c24c, 2026-09-25, because www.qbreader.org is blocked here):
   - Base URL `https://www.qbreader.org/api`; rate limit 20 req/s per IP
     (`routes/api/index.js`, express-rate-limit).
   - `/set-list?expand=true&includeCounts=true` → `{_id, setName, difficulty,
     standard, year, packetsCount, tossupsCount, bonusesCount}` per set.
   - `/num-packets?setName=` → `{numPackets}` (404 if unknown).
   - `/packet?setName=&packetNumber=` (1-based) → `{tossups, bonuses, packet}`;
     404 when empty.
   - `/query` → `maxReturnLength` ≤ 10000 and pagination capped at
     10000/maxReturnLength, so search cannot enumerate the corpus. An empty
     `q` with `difficulties=N` returns QBReader's own per-difficulty totals
     (`tossups.count`, `bonuses.count`), usable for coverage checks.
   - Official full backups: Google Drive folder linked from
     qbreader.org/db/backups (bsondump JSON: tossups, bonuses, packets, sets).
   - Schemas: tossup `question, question_sanitized, answer, answer_sanitized`;
     bonus `leadin(_sanitized), parts(_sanitized)[], answers(_sanitized)[],
     values?, difficultyModifiers?`; all have `_id, category, subcategory,
     alternate_subcategory?, difficulty (0-10), number, packet{_id,name,number},
     set{_id,name,year,standard}, updatedAt`. Parts/answers lengths can
     differ in a few bonuses (documented).
   - Difficulty: set-level value copied onto each question at upload
     (`tools/upload/upsert-packet.js`); admin update changes set + questions
     together (`database/qbreader/admin/update-set-difficulty.js`); `/query`
     filters on the question-level field. Scale: 6 Easy College, 7 Medium
     College, 8 Regionals, 9 Nationals, 10 Open.
   - Categories/subcategories/alternate subcategories copied from
     `shared/categories.js` into `src/qbstudy/records.py`.
2. **Project scaffolding**: `.gitignore` (private/bulk data excluded),
   `config/settings.toml` (scope 6-10 persisted, throttle 2 req/s, paid API
   disabled), `requirements*.txt`, `pyproject.toml`, `CLAUDE.md`.
3. **Database schema** `src/qbstudy/migrations/0001_initial.sql`: raw
   records, sets/packets/questions/bonus_parts, question version history,
   `eligible_questions` view (scope filter), download checkpoints, coverage
   checks, corpus snapshots, clue units + FTS5, answer keys, taxonomy
   versions, entities/aliases/relations, AI batches, classifications (+
   secondary nodes, tags, clue-level topics), review log, sources,
   passages, claims, comparisons, clue records.
4. **Modules**: `config.py` (TOML load/merge/validate; rejects >20 req/s and
   invalid scope), `db.py` (versioned migrations with checksum enforcement,
   atomic apply, scope sync + history), `textutil.py` (HTML strip,
   normalization, stemming, clue-sentence splitting, answerline parsing,
   hedge detection), `records.py` (raw preservation, Extended JSON decoding
   for backups, change detection, difficulty status incl. conflicts,
   bonus parts, missing-from-source flagging).
5. **Tests**: `tests/test_foundation.py`, 24 passed (Linux cloud only; not yet
   run on Windows). The same checks were first run as a smoke test
   (in-memory DB, SYNTHETIC records, not real data):
   migration applied once and was a no-op on re-run; 5 records stored,
   repeat import → 0 new/5 unchanged; edited answer → 1 changed + 2 raw
   versions kept; difficulty 8 eligible, 3 excluded, question 9 in a
   difficulty-8 set → `conflict`, absent difficulty → `missing`; bonus with
   3 parts/2 answers flagged; `PRAGMA foreign_key_check` clean; Extended
   JSON `$oid/$numberInt/$date` decoded.

## Blocked / external
- **QBReader network access**: this cloud environment's network policy
  returns 403 for www.qbreader.org, so no real QBReader data has been
  downloaded or tested. Fix: environment settings → Network access → allow
  `qbreader.org` and `www.qbreader.org`, or run on the user's Windows PC.
- **Private GitHub repo**: creating repos via the integration → 403.
  User can create `qbreader-study-system` (Private) on github.com and grant
  the Claude GitHub App access; the code can then be moved there.
- **Model API**: no API credential is configured; real AI classification is
  blocked (not attempted). Planned provider uses the official `anthropic`
  SDK, off by default (`allow_paid_api = false`).

## Remaining work (planned design; not implemented)
1. `qbreader_api.py`: urllib client, throttle (≤ config rps), retry with
   exponential backoff + jitter, honor Retry-After/RateLimit-Reset on 429,
   no retry on other 4xx, detect proxy/network block distinctly.
2. `download.py`: set-list → per-set decision (skip sets whose set difficulty
   is valid and outside 6-10; download unknown-difficulty sets to check
   question-level values) → packet items in `download_items` (checkpoint per
   packet, resume skips `done`) → store → mark missing → coverage report.
   Pilot mode (a few packets across difficulties 6-10). Incremental `update`
   (new sets, count changes, explicit/recent rechecks). Report successful /
   skipped / failed / unavailable separately.
3. `backup_import.py`: import official backup JSON (NDJSON or array).
4. `coverage.py`: per-set expected vs local counts; per-difficulty
   `/query` totals vs local eligible counts; never claim completeness
   unless verified.
5. `index.py`: build clue_units/answer_keys (+FTS) for eligible questions
   only, incrementally by content hash; drop rows that leave scope.
6. `taxonomy/taxonomy_v1.json` (versioned, variable depth, definitions,
   examples, QBReader mappings, tag facets) + `taxonomy.py` (load, validate,
   diff, compatibility of saved labels).
7. `classify.py` + `providers.py`: dry-run estimate, reviewed stratified
   pilot gate, batch export/import JSON, validation (IDs, labels, required
   fields, stale input hash), reuse, corrections with provenance; providers
   manual / fixture / anthropic (SDK, gated).
8. `sources.py`, `claims.py`, `compare.py`, `clues.py`, `ladder.py`: text/PDF/
   URL ingestion with page/line locations and OCR detection; deterministic
   quote claims + model claim batches with verbatim-grounding check;
   answer/alias/keyword/category + cross-category fallback retrieval over
   the eligible collection; statuses existing_or_paraphrase /
   deeper_additional_fact / not_found_in_collection / unresolved with saved
   scope, snapshot, closest matches, reasoning; clue records; draft ladder
   labeled as estimated.
9. `search.py`, `export.py`, `report.py`, `cli.py`, launcher `qbstudy.py`
   plus Windows `setup_windows.bat` / `qbstudy.bat`; work-backup
   export/import (the cloud container is not permanent storage).
10. pytest suite for the failure cases in the original spec; public-domain
    demo source (US presidential inaugural addresses via NLTK's corpus on
    raw.githubusercontent.com, reachable here); README, VALIDATION_REPORT.

## Decisions made (and why)
- Python + SQLite + stdlib HTTP: no server, minimal installs, works on Windows.
- Full coverage via set → packet (documented), not `/query` (10k cap).
- 2 req/s default: 10x below the documented limit.
- Difficulty status from the question's own field; set value used only to
  detect conflicts. Strings like "6" count as invalid (schema says number).
- Records missing from a re-downloaded packet are flagged, never deleted.
- Raw hash over canonical plain JSON so API and backup copies of the same
  record deduplicate; original text kept in `raw_json`.

## Exact resume steps (fresh session)
1. `cd qbreader-study-system`
2. `python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt`
   (Windows: `py -3 -m venv .venv` and `.venv\Scripts\pip install -r requirements-dev.txt`)
3. Run the tests (expect 24 passed), read HANDOFF.md and CLAUDE.md, then this
   file's "Remaining work", starting at item 1.
4. Re-check QBReader reachability:
   `curl -sS -o /dev/null -w "%{http_code}\n" https://www.qbreader.org/api/set-list`
5. Re-verify the API against `qbreader/website` if more than a few weeks
   have passed (routes/api/, client/tools/api-docs/).
