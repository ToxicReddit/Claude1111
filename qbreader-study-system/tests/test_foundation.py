"""Tests for the foundation layer: config, migrations, record storage,
difficulty scope, and text helpers.

All question records here are SYNTHETIC test fixtures shaped like the
documented QBReader API schema. They are not real QBReader data.
"""
import sqlite3

import pytest

from qbstudy import db, records
from qbstudy.config import ConfigError, load_config
from qbstudy.textutil import content_stems, detect_hedges, parse_answerline, split_sentences


@pytest.fixture
def cfg():
    return load_config(local_path=False)


@pytest.fixture
def conn(cfg):
    c = db.connect(":memory:")
    db.migrate(c)
    db.sync_scope(c, cfg)
    records.upsert_set(c, {"_id": "s1", "setName": "2099 Synthetic Set", "difficulty": 8, "standard": True,
                           "year": 2099, "packetsCount": 1, "tossupsCount": 1, "bonusesCount": 1}, "fixture")
    records.upsert_set(c, {"_id": "s2", "setName": "2099 Synthetic Easy", "difficulty": 3, "standard": True,
                           "year": 2099}, "fixture")
    return c


def tossup(**overrides):
    rec = {
        "_id": "t1", "question": "Synthetic clue one. For 10 points, name this.",
        "question_sanitized": "Synthetic clue one. For 10 points, name this.",
        "answer": "Jay Gould", "answer_sanitized": "Jay Gould", "category": "History",
        "subcategory": "American History", "difficulty": 8, "number": 1,
        "packet": {"_id": "p1", "name": "A", "number": 1},
        "set": {"_id": "s1", "name": "2099 Synthetic Set", "year": 2099, "standard": True},
        "updatedAt": "2099-01-01T00:00:00.000Z",
    }
    rec.update(overrides)
    return rec


def bonus():
    return {
        "_id": "b1", "leadin": "L", "leadin_sanitized": "L", "parts": ["a", "b", "c"],
        "parts_sanitized": ["a", "b", "c"], "answers": ["x", "y"], "answers_sanitized": ["x", "y"],
        "category": "Science", "subcategory": "Biology", "difficulty": 8, "number": 1,
        "packet": {"_id": "p1", "name": "A", "number": 1},
        "set": {"_id": "s1", "name": "2099 Synthetic Set", "year": 2099, "standard": True},
    }


def sample_batch():
    easy = tossup(_id="t2", difficulty=3, set={"_id": "s2", "name": "2099 Synthetic Easy"},
                  packet={"_id": "p2", "name": "A", "number": 1})
    conflict = tossup(_id="t3", difficulty=9)        # question says 9, its set says 8
    missing = tossup(_id="t4")
    missing.pop("difficulty")
    return [tossup(), easy, conflict, missing], [bonus()]


# ------------------------------------------------------------------ config
def test_scope_is_difficulty_6_to_10(cfg):
    assert cfg.scope_difficulties == [6, 7, 8, 9, 10]


def test_config_rejects_rate_above_documented_limit(tmp_path):
    bad = tmp_path / "s.toml"
    bad.write_text('[scope]\ndifficulties=[6]\n[qbreader]\nrequests_per_second=25\n'
                   '[paths]\ndatabase="x.db"\n')
    with pytest.raises(ConfigError):
        load_config(settings_path=bad, local_path=False)


def test_config_rejects_invalid_scope(tmp_path):
    bad = tmp_path / "s.toml"
    bad.write_text('[scope]\ndifficulties=[6, 11]\n[qbreader]\nrequests_per_second=2\n')
    with pytest.raises(ConfigError):
        load_config(settings_path=bad, local_path=False)


# -------------------------------------------------------------- migrations
def test_migrations_apply_once(cfg):
    c = db.connect(":memory:")
    assert db.migrate(c) == [1]
    assert db.migrate(c) == []
    assert db.schema_version(c) == 1


def test_migration_checksum_is_enforced(cfg):
    c = db.connect(":memory:")
    db.migrate(c)
    c.execute("UPDATE schema_migrations SET checksum = 'tampered' WHERE version = 1")
    c.commit()
    with pytest.raises(db.MigrationError):
        db.migrate(c)


def test_scope_synced_into_database(conn):
    got = [r["difficulty"] for r in conn.execute("SELECT difficulty FROM scope_difficulties ORDER BY 1")]
    assert got == [6, 7, 8, 9, 10]


# ---------------------------------------------------------- record storage
def test_repeated_import_creates_no_duplicates(conn):
    t, b = sample_batch()
    first = records.store_questions(conn, t, b, "fixture")
    again = records.store_questions(conn, t, b, "fixture")
    assert (first.new, first.changed, first.unchanged) == (5, 0, 0)
    assert (again.new, again.changed, again.unchanged) == (0, 0, 5)
    assert conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0] == 5


def test_edited_record_detected_and_versions_kept(conn):
    records.store_questions(conn, [tossup()], [], "fixture")
    stats = records.store_questions(conn, [tossup(answer_sanitized="Jay Gould [or Jason Gould]")], [], "fixture")
    assert stats.changed == 1
    assert conn.execute("SELECT COUNT(*) FROM raw_records WHERE qb_id = 't1'").fetchone()[0] == 2
    assert conn.execute("SELECT COUNT(*) FROM question_versions WHERE question_id = 't1'").fetchone()[0] == 2


def test_difficulty_statuses_and_eligible_view(conn):
    t, b = sample_batch()
    records.store_questions(conn, t, b, "fixture")
    status = {r["question_id"]: (r["difficulty"], r["difficulty_status"])
              for r in conn.execute("SELECT question_id, difficulty, difficulty_status FROM questions")}
    assert status == {"t1": (8, "valid"), "b1": (8, "valid"), "t2": (3, "valid"),
                      "t3": (9, "conflict"), "t4": (None, "missing")}
    eligible = [r[0] for r in conn.execute("SELECT question_id FROM eligible_questions ORDER BY 1")]
    assert eligible == ["b1", "t1"]


@pytest.mark.parametrize("value,expected", [
    (6, (6, "valid")), (10, (10, "valid")), (None, (None, "missing")), ("6", (None, "invalid")),
    (11, (None, "invalid")), (6.5, (None, "invalid")), (True, (None, "invalid")),
])
def test_difficulty_values_never_guessed(value, expected):
    assert records.classify_difficulty(value) == expected


def test_bonus_part_answer_mismatch_flagged(conn):
    records.store_questions(conn, [], [bonus()], "fixture")
    assert conn.execute("SELECT COUNT(*) FROM bonus_parts WHERE question_id = 'b1'").fetchone()[0] == 3
    assert conn.execute("SELECT parts_answers_mismatch FROM questions WHERE question_id = 'b1'").fetchone()[0] == 1


def test_foreign_keys_clean(conn):
    t, b = sample_batch()
    records.store_questions(conn, t, b, "fixture")
    assert conn.execute("PRAGMA foreign_key_check").fetchall() == []


def test_missing_from_source_flagged_not_deleted(conn):
    records.store_questions(conn, [tossup(), tossup(_id="t5")], [], "fixture")
    gone = records.mark_missing_in_packet(conn, "p1", {"t1"})
    assert gone == 1
    row = conn.execute("SELECT source_status FROM questions WHERE question_id = 't5'").fetchone()
    assert row["source_status"] == "missing_from_source"
    assert "t5" not in [r[0] for r in conn.execute("SELECT question_id FROM eligible_questions")]


def test_invalid_record_rejected_without_crash(conn):
    stats = records.store_questions(conn, [{"_id": "t9"}], [], "fixture")
    assert stats.invalid == 1 and stats.new == 0


def test_extended_json_decoding():
    got = records.ejson_to_plain({"_id": {"$oid": "abc"}, "difficulty": {"$numberInt": "7"},
                                  "updatedAt": {"$date": {"$numberLong": "1700000000000"}}})
    assert got == {"_id": "abc", "difficulty": 7, "updatedAt": "2023-11-14T22:13:20.000Z"}


# ------------------------------------------------------------ text helpers
def test_answerline_parsing():
    a = parse_answerline('Jay Gould [or Jason Gould; prompt on Gould; do not accept "James Fisk"]')
    assert (a.main, a.alternates, a.prompts, a.rejects) == ("Jay Gould", ["Jason Gould"], ["Gould"], ["James Fisk"])
    m = parse_answerline("<b><u>Mercury</u></b> [or <b><u>Hg</u></b>; accept <b><u>quicksilver</u></b>]")
    assert (m.main, m.alternates) == ("Mercury", ["Hg", "quicksilver"])


def test_sentence_split_protects_initials_and_abbreviations():
    s = split_sentences("This man worked with J. P. Morgan and Dr. Smith in the U.S. market. "
                        "He partnered with James Fisk (*) in 1869. For 10 points, name this robber baron.")
    assert len(s) == 3 and s[2].startswith("For 10 points")


def test_content_stems_and_hedges():
    assert content_stems("For 10 points, name this man who controlled the Erie Railroad.") == \
        ["10", "controll", "erie", "railroad"]
    assert detect_hedges("The enzyme may be regulated in vitro, suggesting a role.") == ["in vitro", "may", "suggest"]
