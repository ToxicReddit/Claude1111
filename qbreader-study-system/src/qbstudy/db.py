"""SQLite connection, versioned migrations, and scope syncing."""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

from .config import Config

MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"
_MIGRATION_RE = re.compile(r"^(\d{4})_([a-z0-9_]+)\.sql$")


class MigrationError(Exception):
    pass


def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def connect(path: Path | str) -> sqlite3.Connection:
    if str(path) != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 30000")
    if str(path) != ":memory:":
        conn.execute("PRAGMA journal_mode = WAL")
    return conn


@contextmanager
def transaction(conn: sqlite3.Connection) -> Iterator[sqlite3.Connection]:
    """Explicit transaction: commit on success, roll back on any error."""
    conn.execute("BEGIN")
    try:
        yield conn
    except BaseException:
        conn.rollback()
        raise
    else:
        conn.commit()


def available_migrations() -> list[tuple[int, str, Path]]:
    found = []
    for p in sorted(MIGRATIONS_DIR.glob("*.sql")):
        m = _MIGRATION_RE.match(p.name)
        if not m:
            raise MigrationError(f"Badly named migration file: {p.name}")
        found.append((int(m.group(1)), m.group(2), p))
    versions = [v for v, _, _ in found]
    if versions != list(range(1, len(versions) + 1)):
        raise MigrationError(f"Migration versions must be contiguous from 0001: {versions}")
    return found


def migrate(conn: sqlite3.Connection) -> list[int]:
    """Apply pending migrations in order. Returns versions applied now."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS schema_migrations ("
        " version INTEGER PRIMARY KEY, name TEXT NOT NULL,"
        " checksum TEXT NOT NULL, applied_at TEXT NOT NULL)")
    conn.commit()
    applied = {r["version"]: r for r in conn.execute("SELECT * FROM schema_migrations")}
    newly = []
    for version, name, path in available_migrations():
        sql = path.read_text(encoding="utf-8")
        checksum = hashlib.sha256(sql.encode("utf-8")).hexdigest()
        if version in applied:
            if applied[version]["checksum"] != checksum:
                raise MigrationError(
                    f"Migration {path.name} was modified after it was applied. "
                    "Never edit an applied migration; add a new numbered file instead.")
            continue
        try:
            conn.executescript(
                "BEGIN;\n" + sql + "\n"
                f"INSERT INTO schema_migrations (version, name, checksum, applied_at) "
                f"VALUES ({version}, '{name}', '{checksum}', '{utcnow()}');\nCOMMIT;")
        except sqlite3.Error as exc:
            conn.rollback()
            raise MigrationError(f"Migration {path.name} failed and was rolled back: {exc}") from exc
        newly.append(version)
    return newly


def schema_version(conn: sqlite3.Connection) -> int:
    try:
        row = conn.execute("SELECT MAX(version) AS v FROM schema_migrations").fetchone()
    except sqlite3.OperationalError:
        return 0
    return row["v"] or 0


def sync_scope(conn: sqlite3.Connection, cfg: Config) -> bool:
    """Mirror [scope].difficulties into the DB. Returns True if it changed."""
    new = sorted(cfg.scope_difficulties)
    old_row = conn.execute(
        "SELECT value FROM project_settings WHERE key = 'scope.difficulties'").fetchone()
    old = json.loads(old_row["value"]) if old_row else None
    current = sorted(r["difficulty"] for r in conn.execute("SELECT difficulty FROM scope_difficulties"))
    if old == new and current == new:
        return False
    with transaction(conn):
        conn.execute("DELETE FROM scope_difficulties")
        conn.executemany("INSERT INTO scope_difficulties (difficulty) VALUES (?)", [(d,) for d in new])
        conn.execute(
            "INSERT INTO project_settings (key, value, updated_at) VALUES ('scope.difficulties', ?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at",
            (json.dumps(new), utcnow()))
        conn.execute(
            "INSERT INTO project_settings (key, value, updated_at) VALUES ('scope.collection_label', ?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at",
            (cfg.collection_label, utcnow()))
        conn.execute("INSERT INTO scope_history (changed_at, old_value, new_value) VALUES (?, ?, ?)",
                     (utcnow(), json.dumps(old) if old is not None else None, json.dumps(new)))
    return old is not None and old != new


def open_db(cfg: Config) -> sqlite3.Connection:
    """Open the project database, apply migrations, and sync the scope."""
    conn = connect(cfg.db_path)
    migrate(conn)
    sync_scope(conn, cfg)
    return conn
