-- 0001_initial: core schema for qbreader-study-system.
--
-- Layers (kept separate on purpose):
--   raw_records            exactly what QBReader returned (never edited)
--   qb_sets / qb_packets / questions / bonus_parts
--                          QBReader's original field values, one row per record
--   clue_units / answer_keys (+ FTS)
--                          derived, cleaned search data (rebuildable, eligible only)
--   classifications ...    AI / human labels with provenance
--   sources / claims / comparisons / clues
--                          outside-source research
--   review_log             every human decision

-- ---------------------------------------------------------------- settings
CREATE TABLE project_settings (
    key        TEXT PRIMARY KEY,
    value      TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Mirrors [scope].difficulties from config; re-synced on every run.
CREATE TABLE scope_difficulties (
    difficulty INTEGER PRIMARY KEY CHECK (difficulty BETWEEN 0 AND 10)
);

CREATE TABLE scope_history (
    id         INTEGER PRIMARY KEY,
    changed_at TEXT NOT NULL,
    old_value  TEXT,
    new_value  TEXT NOT NULL
);

-- ---------------------------------------------------------------- raw layer
CREATE TABLE raw_records (
    raw_id           INTEGER PRIMARY KEY,
    record_type      TEXT NOT NULL CHECK (record_type IN ('set', 'packet', 'tossup', 'bonus')),
    qb_id            TEXT NOT NULL,
    raw_hash         TEXT NOT NULL,          -- sha256 of canonical plain JSON
    raw_json         TEXT NOT NULL,          -- original text as received
    origin           TEXT NOT NULL CHECK (origin IN ('api', 'backup', 'fixture')),
    origin_ref       TEXT,                   -- endpoint + params, or backup file
    first_fetched_at TEXT NOT NULL,
    last_seen_at     TEXT NOT NULL,
    UNIQUE (record_type, qb_id, raw_hash)
);
CREATE INDEX idx_raw_records_qb_id ON raw_records (record_type, qb_id);

-- ------------------------------------------------ QBReader records (original)
CREATE TABLE qb_sets (
    set_id              TEXT PRIMARY KEY,
    name                TEXT NOT NULL,
    year                INTEGER,
    difficulty          INTEGER,
    difficulty_raw      TEXT,                -- JSON of the value as given
    difficulty_status   TEXT NOT NULL CHECK (difficulty_status IN ('valid', 'missing', 'invalid')),
    standard            INTEGER,
    expected_packets    INTEGER,             -- from /set-list includeCounts
    expected_tossups    INTEGER,
    expected_bonuses    INTEGER,
    expected_counts_at  TEXT,
    origin              TEXT NOT NULL,
    first_seen_at       TEXT NOT NULL,
    last_seen_at        TEXT NOT NULL
);
CREATE INDEX idx_qb_sets_name ON qb_sets (name);

CREATE TABLE qb_packets (
    packet_id     TEXT PRIMARY KEY,
    set_id        TEXT NOT NULL REFERENCES qb_sets (set_id),
    name          TEXT,
    number        INTEGER,
    origin        TEXT NOT NULL,
    first_seen_at TEXT NOT NULL,
    last_seen_at  TEXT NOT NULL
);
CREATE INDEX idx_qb_packets_set ON qb_packets (set_id, number);

CREATE TABLE questions (
    question_id              TEXT PRIMARY KEY,   -- QBReader _id
    question_type            TEXT NOT NULL CHECK (question_type IN ('tossup', 'bonus')),
    set_id                   TEXT REFERENCES qb_sets (set_id),
    packet_id                TEXT REFERENCES qb_packets (packet_id),
    set_name                 TEXT,
    set_year                 INTEGER,
    set_standard             INTEGER,
    packet_name              TEXT,
    packet_number            INTEGER,
    question_number          INTEGER,
    difficulty               INTEGER,
    difficulty_raw           TEXT,
    difficulty_status        TEXT NOT NULL
        CHECK (difficulty_status IN ('valid', 'missing', 'invalid', 'conflict')),
    qb_category              TEXT,
    qb_subcategory           TEXT,
    qb_alternate_subcategory TEXT,
    question_html            TEXT,               -- tossup body (HTML, original)
    question_sanitized       TEXT,
    answer_html              TEXT,
    answer_sanitized         TEXT,
    leadin_html              TEXT,               -- bonus leadin (original)
    leadin_sanitized         TEXT,
    parts_answers_mismatch   INTEGER NOT NULL DEFAULT 0,
    qb_updated_at            TEXT,
    raw_id                   INTEGER NOT NULL REFERENCES raw_records (raw_id),
    raw_hash                 TEXT NOT NULL,
    content_hash             TEXT NOT NULL,
    source_status            TEXT NOT NULL DEFAULT 'present'
        CHECK (source_status IN ('present', 'missing_from_source')),
    origin                   TEXT NOT NULL,
    first_seen_at            TEXT NOT NULL,
    last_changed_at          TEXT NOT NULL,
    last_seen_at             TEXT NOT NULL
);
CREATE INDEX idx_questions_scope ON questions (difficulty_status, difficulty, source_status);
CREATE INDEX idx_questions_packet ON questions (packet_id);
CREATE INDEX idx_questions_set ON questions (set_id);
CREATE INDEX idx_questions_category ON questions (qb_category, qb_subcategory);

CREATE TABLE bonus_parts (
    question_id         TEXT NOT NULL REFERENCES questions (question_id) ON DELETE CASCADE,
    part_index          INTEGER NOT NULL,        -- 0-based
    part_html           TEXT,
    part_sanitized      TEXT,
    answer_html         TEXT,
    answer_sanitized    TEXT,
    value               INTEGER,
    difficulty_modifier TEXT,
    PRIMARY KEY (question_id, part_index)
);

CREATE TABLE question_versions (
    question_id  TEXT NOT NULL,
    raw_id       INTEGER NOT NULL REFERENCES raw_records (raw_id),
    content_hash TEXT NOT NULL,
    change_kind  TEXT NOT NULL CHECK (change_kind IN ('new', 'changed')),
    recorded_at  TEXT NOT NULL,
    PRIMARY KEY (question_id, raw_id)
);

-- The ONLY question set used for processing (classification, clue
-- extraction, comparison, export). Everything else stays raw-only.
CREATE VIEW eligible_questions AS
SELECT q.*
FROM questions q
WHERE q.difficulty_status = 'valid'
  AND q.source_status = 'present'
  AND q.difficulty IN (SELECT difficulty FROM scope_difficulties);

-- ------------------------------------------------------------ downloads
CREATE TABLE download_runs (
    run_id       INTEGER PRIMARY KEY,
    mode         TEXT NOT NULL,
    started_at   TEXT NOT NULL,
    finished_at  TEXT,
    status       TEXT NOT NULL CHECK (status IN ('running', 'completed', 'interrupted', 'aborted')),
    params_json  TEXT,
    summary_json TEXT
);

CREATE TABLE set_download_state (
    set_id             TEXT PRIMARY KEY REFERENCES qb_sets (set_id),
    decision           TEXT NOT NULL
        CHECK (decision IN ('download', 'skip_out_of_scope', 'skip_unknown_difficulty')),
    reason             TEXT,
    num_packets        INTEGER,
    num_packets_source TEXT,
    updated_at         TEXT NOT NULL
);

CREATE TABLE download_items (
    item_key          TEXT PRIMARY KEY,          -- packet:<set_id>:<number>
    set_id            TEXT NOT NULL REFERENCES qb_sets (set_id),
    set_name          TEXT NOT NULL,
    packet_number     INTEGER NOT NULL,
    status            TEXT NOT NULL
        CHECK (status IN ('pending', 'done', 'failed', 'unavailable')),
    attempts          INTEGER NOT NULL DEFAULT 0,
    http_status       INTEGER,
    last_error        TEXT,
    tossups_received  INTEGER,
    bonuses_received  INTEGER,
    new_records       INTEGER,
    changed_records   INTEGER,
    unchanged_records INTEGER,
    last_run_id       INTEGER REFERENCES download_runs (run_id),
    updated_at        TEXT NOT NULL
);
CREATE INDEX idx_download_items_status ON download_items (status);

CREATE TABLE coverage_checks (
    check_id     INTEGER PRIMARY KEY,
    created_at   TEXT NOT NULL,
    kind         TEXT NOT NULL,
    status       TEXT NOT NULL,
    details_json TEXT NOT NULL
);

CREATE TABLE corpus_snapshots (
    snapshot_id                  INTEGER PRIMARY KEY,
    created_at                   TEXT NOT NULL,
    scope_json                   TEXT NOT NULL,
    eligible_tossups             INTEGER NOT NULL,
    eligible_bonuses             INTEGER NOT NULL,
    eligible_by_difficulty_json  TEXT NOT NULL,
    excluded_json                TEXT NOT NULL,
    latest_record_seen_at        TEXT,
    coverage_status              TEXT NOT NULL,
    notes                        TEXT
);

-- ------------------------------------------ derived search data (eligible)
CREATE TABLE clue_units (
    unit_id      INTEGER PRIMARY KEY,
    question_id  TEXT NOT NULL REFERENCES questions (question_id) ON DELETE CASCADE,
    segment      TEXT NOT NULL CHECK (segment IN ('tossup', 'leadin', 'part')),
    part_index   INTEGER NOT NULL DEFAULT -1,
    unit_index   INTEGER NOT NULL,
    unit_count   INTEGER NOT NULL,
    text         TEXT NOT NULL,
    is_giveaway  INTEGER NOT NULL DEFAULT 0,
    content_hash TEXT NOT NULL,
    UNIQUE (question_id, segment, part_index, unit_index)
);

CREATE VIRTUAL TABLE clue_units_fts USING fts5(
    text, content='clue_units', content_rowid='unit_id',
    tokenize='porter unicode61 remove_diacritics 2'
);
CREATE TRIGGER clue_units_ai AFTER INSERT ON clue_units BEGIN
    INSERT INTO clue_units_fts (rowid, text) VALUES (new.unit_id, new.text);
END;
CREATE TRIGGER clue_units_ad AFTER DELETE ON clue_units BEGIN
    INSERT INTO clue_units_fts (clue_units_fts, rowid, text) VALUES ('delete', old.unit_id, old.text);
END;
CREATE TRIGGER clue_units_au AFTER UPDATE ON clue_units BEGIN
    INSERT INTO clue_units_fts (clue_units_fts, rowid, text) VALUES ('delete', old.unit_id, old.text);
    INSERT INTO clue_units_fts (rowid, text) VALUES (new.unit_id, new.text);
END;

CREATE TABLE answer_keys (
    question_id     TEXT NOT NULL REFERENCES questions (question_id) ON DELETE CASCADE,
    part_index      INTEGER NOT NULL DEFAULT -1,  -- -1 = tossup answer
    answer_main     TEXT NOT NULL,
    answer_norm     TEXT NOT NULL,
    alternates_json TEXT NOT NULL,
    alternates_norm TEXT NOT NULL,                 -- '|alt1|alt2|' for matching
    content_hash    TEXT NOT NULL,
    PRIMARY KEY (question_id, part_index)
);
CREATE INDEX idx_answer_keys_norm ON answer_keys (answer_norm);

CREATE TABLE index_state (
    question_id  TEXT PRIMARY KEY REFERENCES questions (question_id) ON DELETE CASCADE,
    content_hash TEXT NOT NULL,
    indexed_at   TEXT NOT NULL
);

-- ---------------------------------------------------------------- taxonomy
CREATE TABLE taxonomy_versions (
    version     TEXT PRIMARY KEY,
    taxonomy_id TEXT NOT NULL,
    file_sha256 TEXT NOT NULL,
    node_count  INTEGER NOT NULL,
    loaded_at   TEXT NOT NULL
);

CREATE TABLE taxonomy_nodes (
    version                  TEXT NOT NULL REFERENCES taxonomy_versions (version),
    node_id                  TEXT NOT NULL,
    parent_id                TEXT,
    label                    TEXT NOT NULL,
    kind                     TEXT NOT NULL,
    definition               TEXT NOT NULL,
    definition_hash          TEXT NOT NULL,
    qb_category              TEXT,
    qb_subcategory           TEXT,
    qb_alternate_subcategory TEXT,
    PRIMARY KEY (version, node_id)
);

-- ---------------------------------------------------------------- entities
CREATE TABLE entities (
    entity_id      INTEGER PRIMARY KEY,
    canonical_name TEXT NOT NULL,
    disambiguator  TEXT NOT NULL DEFAULT '',
    entity_type    TEXT,
    description    TEXT,
    origin         TEXT NOT NULL,
    created_at     TEXT NOT NULL,
    UNIQUE (canonical_name, disambiguator)
);

CREATE TABLE entity_aliases (
    entity_id  INTEGER NOT NULL REFERENCES entities (entity_id) ON DELETE CASCADE,
    alias      TEXT NOT NULL,
    alias_norm TEXT NOT NULL,
    PRIMARY KEY (entity_id, alias_norm)
);
CREATE INDEX idx_entity_aliases_norm ON entity_aliases (alias_norm);

CREATE TABLE entity_relations (
    relation_id   INTEGER PRIMARY KEY,
    src_entity_id INTEGER NOT NULL REFERENCES entities (entity_id) ON DELETE CASCADE,
    relation      TEXT NOT NULL,
    dst_entity_id INTEGER NOT NULL REFERENCES entities (entity_id) ON DELETE CASCADE,
    provenance    TEXT NOT NULL,
    confidence    REAL,
    created_at    TEXT NOT NULL,
    UNIQUE (src_entity_id, relation, dst_entity_id)
);

-- --------------------------------------------------------------- AI batches
CREATE TABLE ai_batches (
    batch_id         TEXT PRIMARY KEY,
    kind             TEXT NOT NULL CHECK (kind IN ('classification', 'claims', 'comparison')),
    created_at       TEXT NOT NULL,
    prompt_version   TEXT NOT NULL,
    taxonomy_version TEXT,
    is_pilot         INTEGER NOT NULL DEFAULT 0,
    item_count       INTEGER NOT NULL,
    status           TEXT NOT NULL
        CHECK (status IN ('exported', 'partially_imported', 'imported')),
    export_path      TEXT,
    notes            TEXT
);

CREATE TABLE ai_batch_items (
    batch_id   TEXT NOT NULL REFERENCES ai_batches (batch_id) ON DELETE CASCADE,
    item_id    TEXT NOT NULL,
    input_hash TEXT NOT NULL,
    status     TEXT NOT NULL CHECK (status IN ('pending', 'succeeded', 'failed', 'stale')),
    attempts   INTEGER NOT NULL DEFAULT 0,
    last_error TEXT,
    PRIMARY KEY (batch_id, item_id)
);

-- ---------------------------------------------------------- classifications
CREATE TABLE classifications (
    classification_id INTEGER PRIMARY KEY,
    question_id       TEXT NOT NULL REFERENCES questions (question_id),
    input_hash        TEXT NOT NULL,
    taxonomy_version  TEXT NOT NULL,
    primary_node_id   TEXT,
    status            TEXT NOT NULL CHECK (status IN ('classified', 'uncertain', 'unclassifiable')),
    confidence        REAL CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 1)),
    rationale         TEXT,
    origin            TEXT NOT NULL CHECK (origin IN ('model', 'human', 'fixture')),
    provider          TEXT,
    model_name        TEXT,
    prompt_version    TEXT,
    batch_id          TEXT REFERENCES ai_batches (batch_id),
    review_state      TEXT NOT NULL DEFAULT 'unreviewed'
        CHECK (review_state IN ('unreviewed', 'accepted', 'corrected', 'rejected')),
    is_current        INTEGER NOT NULL DEFAULT 1,
    supersedes_id     INTEGER REFERENCES classifications (classification_id),
    flags_json        TEXT NOT NULL DEFAULT '[]',
    created_at        TEXT NOT NULL
);
CREATE INDEX idx_classifications_question ON classifications (question_id, is_current);

CREATE TABLE classification_secondary_nodes (
    classification_id INTEGER NOT NULL REFERENCES classifications (classification_id) ON DELETE CASCADE,
    node_id           TEXT NOT NULL,
    PRIMARY KEY (classification_id, node_id)
);

CREATE TABLE classification_tags (
    classification_id INTEGER NOT NULL REFERENCES classifications (classification_id) ON DELETE CASCADE,
    facet             TEXT NOT NULL,
    value             TEXT NOT NULL,
    PRIMARY KEY (classification_id, facet, value)
);

-- Individual clue topics, separate from the question-level category.
CREATE TABLE clue_topics (
    classification_id INTEGER NOT NULL REFERENCES classifications (classification_id) ON DELETE CASCADE,
    segment           TEXT NOT NULL,
    part_index        INTEGER NOT NULL DEFAULT -1,
    unit_index        INTEGER NOT NULL,
    node_id           TEXT,
    topic             TEXT,
    entities_json     TEXT NOT NULL DEFAULT '[]',
    PRIMARY KEY (classification_id, segment, part_index, unit_index)
);

CREATE TABLE question_entities (
    question_id       TEXT NOT NULL REFERENCES questions (question_id),
    part_index        INTEGER NOT NULL DEFAULT -1,
    entity_id         INTEGER NOT NULL REFERENCES entities (entity_id),
    role              TEXT NOT NULL CHECK (role IN ('answer', 'subject', 'mentioned')),
    classification_id INTEGER REFERENCES classifications (classification_id) ON DELETE CASCADE,
    PRIMARY KEY (question_id, part_index, entity_id, role)
);

CREATE TABLE review_log (
    review_id   INTEGER PRIMARY KEY,
    target_type TEXT NOT NULL,
    target_id   TEXT NOT NULL,
    action      TEXT NOT NULL,
    old_value   TEXT,
    new_value   TEXT,
    note        TEXT,
    reviewer    TEXT,
    created_at  TEXT NOT NULL
);

-- ---------------------------------------------------------- outside sources
CREATE TABLE sources (
    source_id           INTEGER PRIMARY KEY,
    title               TEXT NOT NULL,
    author              TEXT,
    source_type         TEXT NOT NULL
        CHECK (source_type IN ('textbook', 'paper', 'news', 'primary', 'reference', 'other')),
    publication_date    TEXT,
    event_date          TEXT,
    url                 TEXT,
    local_path          TEXT,
    content_sha256      TEXT,
    media_type          TEXT,
    rights_note         TEXT,
    is_private          INTEGER NOT NULL DEFAULT 1,
    verification_status TEXT NOT NULL DEFAULT 'unverified',
    ingest_status       TEXT NOT NULL
        CHECK (ingest_status IN ('ok', 'partial_needs_ocr', 'needs_ocr', 'empty', 'failed', 'access_denied')),
    ingest_notes        TEXT,
    page_count          INTEGER,
    pages_without_text  INTEGER,
    passage_count       INTEGER NOT NULL DEFAULT 0,
    added_at            TEXT NOT NULL,
    UNIQUE (content_sha256)
);

CREATE TABLE source_passages (
    passage_id      INTEGER PRIMARY KEY,
    source_id       INTEGER NOT NULL REFERENCES sources (source_id) ON DELETE CASCADE,
    seq             INTEGER NOT NULL,
    location_label  TEXT NOT NULL,
    page_number     INTEGER,
    section         TEXT,
    paragraph_index INTEGER,
    line_start      INTEGER,
    line_end        INTEGER,
    text            TEXT NOT NULL,
    text_hash       TEXT NOT NULL,
    flags_json      TEXT NOT NULL DEFAULT '[]',
    UNIQUE (source_id, seq)
);

CREATE TABLE claims (
    claim_id              INTEGER PRIMARY KEY,
    source_id             INTEGER NOT NULL REFERENCES sources (source_id),
    passage_id            INTEGER NOT NULL REFERENCES source_passages (passage_id),
    claim_text            TEXT NOT NULL,
    normalized_claim      TEXT NOT NULL,
    evidence_quote        TEXT NOT NULL,
    claim_type            TEXT NOT NULL
        CHECK (claim_type IN ('quotation', 'fact', 'event', 'definition', 'other')),
    answer_entity         TEXT,
    entity_id             INTEGER REFERENCES entities (entity_id),
    aliases_json          TEXT NOT NULL DEFAULT '[]',
    related_entities_json TEXT NOT NULL DEFAULT '[]',
    category_node_id      TEXT,
    assertion_status      TEXT NOT NULL
        CHECK (assertion_status IN ('source_asserts', 'source_hedges', 'source_reports_dispute',
                                    'quotation_of_speaker')),
    qualifiers_json       TEXT NOT NULL DEFAULT '[]',
    event_date            TEXT,
    verification_status   TEXT NOT NULL DEFAULT 'unverified'
        CHECK (verification_status IN ('unverified', 'primary_source_text', 'corroborated', 'contradicted')),
    extraction_method     TEXT NOT NULL
        CHECK (extraction_method IN ('deterministic_quote', 'model', 'manual', 'fixture')),
    provider              TEXT,
    model_name            TEXT,
    prompt_version        TEXT,
    batch_id              TEXT REFERENCES ai_batches (batch_id),
    review_status         TEXT NOT NULL DEFAULT 'candidate'
        CHECK (review_status IN ('candidate', 'accepted', 'rejected', 'needs_revision')),
    flags_json            TEXT NOT NULL DEFAULT '[]',
    created_at            TEXT NOT NULL,
    UNIQUE (passage_id, normalized_claim)
);

CREATE TABLE comparisons (
    comparison_id          INTEGER PRIMARY KEY,
    claim_id               INTEGER NOT NULL REFERENCES claims (claim_id) ON DELETE CASCADE,
    snapshot_id            INTEGER REFERENCES corpus_snapshots (snapshot_id),
    status                 TEXT NOT NULL
        CHECK (status IN ('existing_or_paraphrase', 'deeper_additional_fact',
                          'not_found_in_collection', 'unresolved')),
    method                 TEXT NOT NULL CHECK (method IN ('lexical', 'model', 'human', 'fixture')),
    semantic_check         TEXT NOT NULL,
    reasoning              TEXT NOT NULL,
    search_scope_json      TEXT NOT NULL,
    closest_matches_json   TEXT NOT NULL,
    answer_question_count  INTEGER,
    matched_question_count INTEGER,
    provider               TEXT,
    model_name             TEXT,
    prompt_version         TEXT,
    batch_id               TEXT REFERENCES ai_batches (batch_id),
    is_current             INTEGER NOT NULL DEFAULT 1,
    created_at             TEXT NOT NULL
);
CREATE INDEX idx_comparisons_claim ON comparisons (claim_id, is_current);

CREATE TABLE clues (
    clue_id                 INTEGER PRIMARY KEY,
    claim_id                INTEGER NOT NULL UNIQUE REFERENCES claims (claim_id),
    comparison_id           INTEGER REFERENCES comparisons (comparison_id),
    clue_text               TEXT NOT NULL,
    normalized_claim        TEXT NOT NULL,
    answer                  TEXT,
    entity_id               INTEGER REFERENCES entities (entity_id),
    aliases_json            TEXT NOT NULL DEFAULT '[]',
    category_node_id        TEXT,
    microcategories_json    TEXT NOT NULL DEFAULT '[]',
    related_entities_json   TEXT NOT NULL DEFAULT '[]',
    source_id               INTEGER NOT NULL REFERENCES sources (source_id),
    passage_id              INTEGER NOT NULL REFERENCES source_passages (passage_id),
    citation                TEXT NOT NULL,
    location_label          TEXT NOT NULL,
    publication_date        TEXT,
    event_date              TEXT,
    linked_question_ids_json TEXT NOT NULL DEFAULT '[]',
    frequency_count         INTEGER,
    frequency_method        TEXT,
    novelty_status          TEXT,
    novelty_statement       TEXT,
    closest_matches_json    TEXT NOT NULL DEFAULT '[]',
    estimated_difficulty    REAL,
    difficulty_basis        TEXT,
    confidence              REAL,
    review_status           TEXT NOT NULL DEFAULT 'candidate'
        CHECK (review_status IN ('candidate', 'approved', 'rejected', 'needs_revision')),
    created_at              TEXT NOT NULL,
    updated_at              TEXT NOT NULL
);
