"""Store QBReader records: raw preservation, normalization, change detection,
and difficulty-scope status. Works for API responses and backup dumps."""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .db import utcnow
from .textutil import canonical_json, sha256_text

# From qbreader/website shared/categories.js (verified 2026-09-27).
QB_CATEGORY_TO_SUBCATEGORIES = {
    "Literature": ["American Literature", "British Literature", "Classical Literature",
                   "European Literature", "World Literature", "Other Literature"],
    "History": ["American History", "Ancient History", "European History", "World History",
                "Other History"],
    "Science": ["Biology", "Chemistry", "Physics", "Other Science"],
    "Fine Arts": ["Visual Fine Arts", "Auditory Fine Arts", "Other Fine Arts"],
    "Religion": ["Religion"],
    "Mythology": ["Mythology"],
    "Philosophy": ["Philosophy"],
    "Social Science": ["Social Science"],
    "Current Events": ["Current Events"],
    "Geography": ["Geography"],
    "Other Academic": ["Other Academic"],
    "Pop Culture": ["Movies", "Music", "Sports", "Television", "Video Games", "Other Pop Culture"],
}
QB_CATEGORY_TO_ALTERNATES = {
    "Literature": ["Drama", "Long Fiction", "Poetry", "Short Fiction", "Misc Literature"],
    "Science": ["Math", "Astronomy", "Computer Science", "Earth Science", "Engineering", "Misc Science"],
    "Fine Arts": ["Architecture", "Dance", "Film", "Jazz", "Musicals", "Opera", "Photography", "Misc Arts"],
    "Social Science": ["Anthropology", "Economics", "Linguistics", "Psychology", "Sociology",
                       "Other Social Science"],
}
QB_DIFFICULTY_LABELS = {
    0: "Pop Culture", 1: "Middle School", 2: "Easy High School", 3: "Regular High School",
    4: "Hard High School", 5: "National High School", 6: "Easy College", 7: "Medium College",
    8: "Regionals College", 9: "Nationals College", 10: "Open",
}


# --------------------------------------------------------- Extended JSON
def _iso_from_millis(ms: int) -> str:
    dt = datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{dt.microsecond // 1000:03d}Z"


def ejson_to_plain(obj: Any) -> Any:
    """Convert MongoDB Extended JSON (as written by bsondump/mongoexport) into
    the plain JSON shapes the QBReader API returns (ObjectId -> hex string,
    dates -> ISO 8601 with milliseconds, numbers -> numbers)."""
    if isinstance(obj, list):
        return [ejson_to_plain(v) for v in obj]
    if not isinstance(obj, dict):
        return obj
    if len(obj) == 1:
        (key, val), = obj.items()
        if key == "$oid":
            return str(val)
        if key in ("$numberInt", "$numberLong"):
            return int(val)
        if key in ("$numberDouble", "$numberDecimal"):
            f = float(val)
            return int(f) if f.is_integer() and key == "$numberDecimal" else f
        if key == "$date":
            if isinstance(val, dict):
                return _iso_from_millis(int(ejson_to_plain(val)))
            if isinstance(val, (int, float)):
                return _iso_from_millis(int(val))
            s = str(val)
            try:
                dt = datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)
                return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{dt.microsecond // 1000:03d}Z"
            except ValueError:
                return s
    return {k: ejson_to_plain(v) for k, v in obj.items()}


# ------------------------------------------------------- difficulty status
def classify_difficulty(value: Any) -> tuple[int | None, str]:
    """Return (difficulty, status) using QBReader's own value only.
    status: valid | missing | invalid. Never guesses (e.g. "6" is invalid,
    because the documented type is an integer)."""
    if value is None:
        return None, "missing"
    if isinstance(value, bool):
        return None, "invalid"
    if isinstance(value, int) and 0 <= value <= 10:
        return value, "valid"
    if isinstance(value, float) and value.is_integer() and 0 <= value <= 10:
        return int(value), "valid"
    return None, "invalid"


def question_difficulty_status(q_value: Any, set_difficulty: int | None,
                               set_status: str | None) -> tuple[int | None, str]:
    diff, status = classify_difficulty(q_value)
    if status == "valid" and set_status == "valid" and set_difficulty is not None \
            and set_difficulty != diff:
        return diff, "conflict"
    return diff, status


def recompute_conflicts(conn: sqlite3.Connection) -> int:
    """Re-derive difficulty_status for all questions from stored raw values
    and current set metadata (run after set metadata changes)."""
    rows = conn.execute(
        "SELECT q.question_id, q.difficulty_raw, q.difficulty_status, s.difficulty AS sd, "
        "s.difficulty_status AS ss FROM questions q LEFT JOIN qb_sets s ON s.set_id = q.set_id").fetchall()
    changed = 0
    for r in rows:
        raw = json.loads(r["difficulty_raw"]) if r["difficulty_raw"] is not None else None
        diff, status = question_difficulty_status(raw, r["sd"], r["ss"])
        if status != r["difficulty_status"]:
            conn.execute("UPDATE questions SET difficulty = ?, difficulty_status = ? WHERE question_id = ?",
                         (diff, status, r["question_id"]))
            changed += 1
    return changed


# ---------------------------------------------------------------- storage
@dataclass
class StoreStats:
    new: int = 0
    changed: int = 0
    unchanged: int = 0
    invalid: int = 0
    errors: list[str] = field(default_factory=list)

    def add(self, other: "StoreStats") -> None:
        self.new += other.new
        self.changed += other.changed
        self.unchanged += other.unchanged
        self.invalid += other.invalid
        self.errors.extend(other.errors)

    def as_dict(self) -> dict:
        return {"new": self.new, "changed": self.changed, "unchanged": self.unchanged,
                "invalid": self.invalid, "errors": self.errors[:50]}


def store_raw(conn: sqlite3.Connection, record_type: str, qb_id: str, plain: dict,
              raw_text: str | None, origin: str, origin_ref: str | None) -> tuple[int, str, bool]:
    """Insert a raw record version if new. Returns (raw_id, raw_hash, was_new)."""
    raw_hash = sha256_text(canonical_json(plain))
    now = utcnow()
    row = conn.execute("SELECT raw_id FROM raw_records WHERE record_type = ? AND qb_id = ? AND raw_hash = ?",
                       (record_type, qb_id, raw_hash)).fetchone()
    if row:
        conn.execute("UPDATE raw_records SET last_seen_at = ? WHERE raw_id = ?", (now, row["raw_id"]))
        return row["raw_id"], raw_hash, False
    cur = conn.execute(
        "INSERT INTO raw_records (record_type, qb_id, raw_hash, raw_json, origin, origin_ref, "
        "first_fetched_at, last_seen_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (record_type, qb_id, raw_hash, raw_text if raw_text is not None else canonical_json(plain),
         origin, origin_ref, now, now))
    return cur.lastrowid, raw_hash, True


def upsert_set(conn: sqlite3.Connection, meta: dict, origin: str, origin_ref: str | None = None,
               raw_text: str | None = None) -> None:
    """meta: a /set-list?expand=true object ({_id, setName, difficulty, standard, year,
    packetsCount?, tossupsCount?, bonusesCount?}) or a backup `sets` document
    ({_id, name, year, difficulty, standard})."""
    set_id = str(meta["_id"])
    name = meta.get("setName") or meta.get("name")
    store_raw(conn, "set", set_id, meta, raw_text, origin, origin_ref)
    diff, status = classify_difficulty(meta.get("difficulty"))
    now = utcnow()
    has_counts = any(k in meta for k in ("packetsCount", "tossupsCount", "bonusesCount"))
    conn.execute(
        "INSERT INTO qb_sets (set_id, name, year, difficulty, difficulty_raw, difficulty_status, standard, "
        " expected_packets, expected_tossups, expected_bonuses, expected_counts_at, origin, "
        " first_seen_at, last_seen_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(set_id) DO UPDATE SET name = excluded.name, year = excluded.year, "
        " difficulty = excluded.difficulty, difficulty_raw = excluded.difficulty_raw, "
        " difficulty_status = excluded.difficulty_status, standard = excluded.standard, "
        " expected_packets = COALESCE(excluded.expected_packets, qb_sets.expected_packets), "
        " expected_tossups = COALESCE(excluded.expected_tossups, qb_sets.expected_tossups), "
        " expected_bonuses = COALESCE(excluded.expected_bonuses, qb_sets.expected_bonuses), "
        " expected_counts_at = COALESCE(excluded.expected_counts_at, qb_sets.expected_counts_at), "
        " last_seen_at = excluded.last_seen_at",
        (set_id, name, meta.get("year"), diff, json.dumps(meta.get("difficulty")), status,
         None if meta.get("standard") is None else int(bool(meta.get("standard"))),
         meta.get("packetsCount"), meta.get("tossupsCount"), meta.get("bonusesCount"),
         now if has_counts else None, origin, now, now))


def upsert_packet(conn: sqlite3.Connection, packet: dict, origin: str, origin_ref: str | None = None,
                  raw_text: str | None = None, set_id: str | None = None) -> str:
    packet_id = str(packet["_id"])
    store_raw(conn, "packet", packet_id, packet, raw_text, origin, origin_ref)
    set_id = set_id or str((packet.get("set") or {}).get("_id"))
    _ensure_set_stub(conn, set_id, (packet.get("set") or {}).get("name"), origin)
    now = utcnow()
    conn.execute(
        "INSERT INTO qb_packets (packet_id, set_id, name, number, origin, first_seen_at, last_seen_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT(packet_id) DO UPDATE SET name = excluded.name, "
        "number = excluded.number, set_id = excluded.set_id, last_seen_at = excluded.last_seen_at",
        (packet_id, set_id, packet.get("name"), packet.get("number"), origin, now, now))
    return packet_id


def _ensure_set_stub(conn: sqlite3.Connection, set_id: str | None, name: str | None, origin: str) -> None:
    if not set_id or set_id == "None":
        return
    if conn.execute("SELECT 1 FROM qb_sets WHERE set_id = ?", (set_id,)).fetchone():
        return
    now = utcnow()
    conn.execute(
        "INSERT INTO qb_sets (set_id, name, difficulty_raw, difficulty_status, origin, first_seen_at, "
        "last_seen_at) VALUES (?, ?, NULL, 'missing', ?, ?, ?)", (set_id, name or "(unknown set)", origin, now, now))


def _ensure_packet_stub(conn: sqlite3.Connection, packet: dict, set_id: str | None, origin: str) -> str | None:
    pid = packet.get("_id")
    if not pid:
        return None
    pid = str(pid)
    if not conn.execute("SELECT 1 FROM qb_packets WHERE packet_id = ?", (pid,)).fetchone() and set_id:
        now = utcnow()
        conn.execute("INSERT INTO qb_packets (packet_id, set_id, name, number, origin, first_seen_at, "
                     "last_seen_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                     (pid, set_id, packet.get("name"), packet.get("number"), origin, now, now))
    return pid


def content_fields(rec: dict, qtype: str) -> dict:
    """Fields whose change means the question itself changed."""
    base = {k: rec.get(k) for k in ("category", "subcategory", "alternate_subcategory", "difficulty")}
    if qtype == "tossup":
        base.update({k: rec.get(k) for k in ("question", "question_sanitized", "answer", "answer_sanitized")})
    else:
        base.update({k: rec.get(k) for k in ("leadin", "leadin_sanitized", "parts", "parts_sanitized",
                                              "answers", "answers_sanitized", "values",
                                              "difficultyModifiers")})
    return base


def validate_question(rec: dict, qtype: str) -> list[str]:
    problems = []
    if not rec.get("_id"):
        problems.append("missing _id")
    if qtype == "tossup":
        if not isinstance(rec.get("question"), str) and not isinstance(rec.get("question_sanitized"), str):
            problems.append("tossup has no question text")
        if rec.get("answer") is None and rec.get("answer_sanitized") is None:
            problems.append("tossup has no answer")
    else:
        if not isinstance(rec.get("parts", rec.get("parts_sanitized")), list):
            problems.append("bonus has no parts list")
    return problems


def upsert_question(conn: sqlite3.Connection, rec: dict, qtype: str, origin: str,
                    origin_ref: str | None = None, raw_text: str | None = None) -> str:
    """Store one tossup or bonus. Returns 'new' | 'changed' | 'unchanged' | 'invalid'."""
    problems = validate_question(rec, qtype)
    if problems:
        raise ValueError("; ".join(problems))
    qid = str(rec["_id"])
    raw_id, raw_hash, _ = store_raw(conn, qtype, qid, rec, raw_text, origin, origin_ref)
    set_obj = rec.get("set") or {}
    packet_obj = rec.get("packet") or {}
    set_id = str(set_obj["_id"]) if set_obj.get("_id") else None
    _ensure_set_stub(conn, set_id, set_obj.get("name"), origin)
    packet_id = _ensure_packet_stub(conn, packet_obj, set_id, origin)
    srow = conn.execute("SELECT difficulty, difficulty_status FROM qb_sets WHERE set_id = ?",
                        (set_id,)).fetchone() if set_id else None
    diff, dstatus = question_difficulty_status(rec.get("difficulty"), srow["difficulty"] if srow else None,
                                               srow["difficulty_status"] if srow else None)
    content_hash = sha256_text(canonical_json(content_fields(rec, qtype)))
    now = utcnow()
    existing = conn.execute("SELECT raw_hash, content_hash FROM questions WHERE question_id = ?",
                            (qid,)).fetchone()
    if existing and existing["raw_hash"] == raw_hash:
        conn.execute("UPDATE questions SET last_seen_at = ?, source_status = 'present' WHERE question_id = ?",
                     (now, qid))
        return "unchanged"

    parts = rec.get("parts") or []
    parts_s = rec.get("parts_sanitized") or []
    answers = rec.get("answers") or []
    answers_s = rec.get("answers_sanitized") or []
    mismatch = int(qtype == "bonus" and len(parts or parts_s) != len(answers or answers_s))
    values = dict(
        question_type=qtype, set_id=set_id, packet_id=packet_id, set_name=set_obj.get("name"),
        set_year=set_obj.get("year"),
        set_standard=None if set_obj.get("standard") is None else int(bool(set_obj.get("standard"))),
        packet_name=packet_obj.get("name"), packet_number=packet_obj.get("number"),
        question_number=rec.get("number"), difficulty=diff,
        difficulty_raw=json.dumps(rec.get("difficulty")), difficulty_status=dstatus,
        qb_category=rec.get("category"), qb_subcategory=rec.get("subcategory"),
        qb_alternate_subcategory=rec.get("alternate_subcategory"),
        question_html=rec.get("question"), question_sanitized=rec.get("question_sanitized"),
        answer_html=rec.get("answer"), answer_sanitized=rec.get("answer_sanitized"),
        leadin_html=rec.get("leadin"), leadin_sanitized=rec.get("leadin_sanitized"),
        parts_answers_mismatch=mismatch, qb_updated_at=rec.get("updatedAt"),
        raw_id=raw_id, raw_hash=raw_hash, content_hash=content_hash, origin=origin,
    )
    if existing:
        sets = ", ".join(f"{k} = :{k}" for k in values)
        conn.execute(f"UPDATE questions SET {sets}, source_status = 'present', last_changed_at = :now, "
                     f"last_seen_at = :now WHERE question_id = :qid", {**values, "now": now, "qid": qid})
        kind = "changed"
    else:
        cols = ", ".join(values)
        conn.execute(f"INSERT INTO questions (question_id, {cols}, first_seen_at, last_changed_at, last_seen_at) "
                     f"VALUES (:qid, {', '.join(':' + k for k in values)}, :now, :now, :now)",
                     {**values, "now": now, "qid": qid})
        kind = "new"
    conn.execute("INSERT OR IGNORE INTO question_versions (question_id, raw_id, content_hash, change_kind, "
                 "recorded_at) VALUES (?, ?, ?, ?, ?)", (qid, raw_id, content_hash, kind, now))
    if qtype == "bonus":
        conn.execute("DELETE FROM bonus_parts WHERE question_id = ?", (qid,))
        vals = rec.get("values") or []
        mods = rec.get("difficultyModifiers") or []
        n = max(len(parts), len(parts_s), len(answers), len(answers_s))
        for i in range(n):
            conn.execute(
                "INSERT INTO bonus_parts (question_id, part_index, part_html, part_sanitized, answer_html, "
                "answer_sanitized, value, difficulty_modifier) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (qid, i, _at(parts, i), _at(parts_s, i), _at(answers, i), _at(answers_s, i),
                 _at(vals, i), _at(mods, i)))
    return kind


def _at(seq: list, i: int):
    return seq[i] if i < len(seq) else None


def store_questions(conn: sqlite3.Connection, tossups: list[dict], bonuses: list[dict], origin: str,
                    origin_ref: str | None = None) -> StoreStats:
    stats = StoreStats()
    for qtype, items in (("tossup", tossups), ("bonus", bonuses)):
        for rec in items:
            try:
                kind = upsert_question(conn, rec, qtype, origin, origin_ref)
            except ValueError as exc:
                stats.invalid += 1
                stats.errors.append(f"{qtype} {rec.get('_id')}: {exc}")
                continue
            setattr(stats, kind, getattr(stats, kind) + 1)
    return stats


def mark_missing_in_packet(conn: sqlite3.Connection, packet_id: str, present_ids: set[str]) -> int:
    """Questions we hold for this packet that QBReader no longer returns are
    kept (never deleted) but flagged missing_from_source."""
    rows = conn.execute("SELECT question_id FROM questions WHERE packet_id = ? AND source_status = 'present'",
                        (packet_id,)).fetchall()
    gone = [r["question_id"] for r in rows if r["question_id"] not in present_ids]
    for qid in gone:
        conn.execute("UPDATE questions SET source_status = 'missing_from_source' WHERE question_id = ?", (qid,))
    return len(gone)
