"""Load settings from config/settings.toml (+ optional settings.local.toml)."""
from __future__ import annotations

import copy
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SETTINGS = PROJECT_ROOT / "config" / "settings.toml"
LOCAL_SETTINGS = PROJECT_ROOT / "config" / "settings.local.toml"

# QBReader's documented hard limit (https://www.qbreader.org/api-docs).
QBREADER_MAX_RPS = 20.0


class ConfigError(Exception):
    """Raised when settings are missing or invalid."""


def _deep_merge(base: dict, override: dict) -> dict:
    out = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = value
    return out


@dataclass
class Config:
    data: dict
    root: Path

    def get(self, dotted: str, default: Any = None) -> Any:
        node: Any = self.data
        for part in dotted.split("."):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node

    def section(self, name: str) -> dict:
        return dict(self.data.get(name, {}))

    def path(self, dotted: str) -> Path:
        value = self.get(dotted)
        if value is None:
            raise ConfigError(f"Missing path setting: {dotted}")
        p = Path(value)
        return p if p.is_absolute() else self.root / p

    @property
    def scope_difficulties(self) -> list[int]:
        return list(self.data["scope"]["difficulties"])

    @property
    def collection_label(self) -> str:
        return self.data["scope"].get("collection_label", "scoped QBReader collection")

    @property
    def db_path(self) -> Path:
        return self.path("paths.database")

    @property
    def data_dir(self) -> Path:
        return self.path("paths.data_dir")

    @property
    def sources_dir(self) -> Path:
        return self.path("paths.sources_dir")


def validate(cfg: Config) -> None:
    diffs = cfg.get("scope.difficulties")
    if not isinstance(diffs, list) or not diffs:
        raise ConfigError("[scope].difficulties must be a non-empty list of integers 0-10")
    for d in diffs:
        if not isinstance(d, int) or isinstance(d, bool) or not 0 <= d <= 10:
            raise ConfigError(f"[scope].difficulties contains invalid value {d!r} (must be an integer 0-10)")
    if len(set(diffs)) != len(diffs):
        raise ConfigError("[scope].difficulties contains duplicates")
    rps = cfg.get("qbreader.requests_per_second")
    if not isinstance(rps, (int, float)) or rps <= 0:
        raise ConfigError("[qbreader].requests_per_second must be a positive number")
    if rps > QBREADER_MAX_RPS:
        raise ConfigError(
            f"[qbreader].requests_per_second={rps} exceeds QBReader's documented limit of "
            f"{QBREADER_MAX_RPS:g} requests/second")


def load_config(settings_path: Path | None = None, local_path: Path | None = None,
                overrides: dict | None = None, root: Path | None = None) -> Config:
    settings_path = settings_path or DEFAULT_SETTINGS
    local_path = LOCAL_SETTINGS if local_path is None else local_path
    if not settings_path.exists():
        raise ConfigError(f"Settings file not found: {settings_path}")
    with open(settings_path, "rb") as fh:
        data = tomllib.load(fh)
    if local_path and Path(local_path).exists():
        with open(local_path, "rb") as fh:
            data = _deep_merge(data, tomllib.load(fh))
    if overrides:
        data = _deep_merge(data, overrides)
    cfg = Config(data=data, root=root or PROJECT_ROOT)
    validate(cfg)
    return cfg
