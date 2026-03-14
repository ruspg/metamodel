"""Wave 1 search_aliases artifact generator."""
from __future__ import annotations

import re
from typing import Any, Dict, Mapping

from .projection_model import ProjectionAlias, ProjectionEntityKind, ProjectionModel

_SEARCH_ALIASES_SCHEMA_VERSION = "wave1.search_aliases/v1"
_WHITESPACE_RE = re.compile(r"\s+")


class SearchAliasesGenerationError(ValueError):
    """Raised when projection input cannot produce search aliases output."""


def build_search_aliases(projection: ProjectionModel) -> Mapping[str, Any]:
    """Build compact deterministic runtime-facing search aliases payload."""

    _require_non_empty(projection.metadata.model_name, "metadata.model_name")
    _require_non_empty(projection.metadata.version, "metadata.version")
    _require_non_empty(projection.metadata.bank_code, "metadata.bank_code")
    _require_non_empty(projection.metadata.active_profile, "metadata.active_profile")

    kind_index = {kind.id: kind for kind in projection.entity_kinds}
    canonical_targets = _build_canonical_target_index(projection.entity_kinds)

    rows: Dict[tuple[str, str], Dict[str, Any]] = {}

    for kind in sorted(projection.entity_kinds, key=lambda value: value.id):
        for raw_alias, source in _kind_alias_candidates(kind):
            normalized = _normalize_alias(raw_alias)
            if not normalized:
                continue
            _register_alias(
                rows,
                alias=normalized,
                target_id=kind.id,
                source=source,
                target_category=kind.category,
            )

    unresolved_count = 0
    for alias in sorted(projection.aliases, key=lambda value: value.id):
        target_id = _resolve_alias_target(alias, canonical_targets)
        if target_id is None or target_id not in kind_index:
            unresolved_count += 1
            continue

        normalized = _normalize_alias(alias.alias)
        if not normalized:
            continue

        _register_alias(
            rows,
            alias=normalized,
            target_id=target_id,
            source="glossary_alias",
            target_category=kind_index[target_id].category,
            language=alias.language,
        )

    aliases = tuple(
        rows[key]
        for key in sorted(rows.keys(), key=lambda item: (item[0], item[1]))
    )

    return {
        "schema_version": _SEARCH_ALIASES_SCHEMA_VERSION,
        "model": {
            "model_name": projection.metadata.model_name,
            "model_version": projection.metadata.version,
            "bank_code": projection.metadata.bank_code,
            "profile": projection.metadata.active_profile,
        },
        "counts": {
            "alias_count": len(aliases),
            "unresolved_alias_count": unresolved_count,
        },
        "aliases": aliases,
    }


def _kind_alias_candidates(kind: ProjectionEntityKind) -> tuple[tuple[str, str], ...]:
    candidates: list[tuple[str, str]] = [(kind.id, "canonical_id")]
    if kind.name:
        candidates.append((kind.name, "canonical_name"))
    name_ru = kind.extra.get("name_ru")
    if isinstance(name_ru, str) and name_ru.strip():
        candidates.append((name_ru, "display_name_ru"))
    return tuple(candidates)


def _build_canonical_target_index(kinds: tuple[ProjectionEntityKind, ...]) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for kind in kinds:
        mapping[_normalize_alias(kind.id)] = kind.id
        if kind.name:
            mapping[_normalize_alias(kind.name)] = kind.id
        name_ru = kind.extra.get("name_ru")
        if isinstance(name_ru, str) and name_ru.strip():
            mapping[_normalize_alias(name_ru)] = kind.id
    return mapping


def _resolve_alias_target(alias: ProjectionAlias, canonical_targets: Mapping[str, str]) -> str | None:
    term = _normalize_alias(alias.term)
    if not term:
        return None
    return canonical_targets.get(term)


def _register_alias(
    rows: Dict[tuple[str, str], Dict[str, Any]],
    *,
    alias: str,
    target_id: str,
    source: str,
    target_category: str | None,
    language: str | None = None,
) -> None:
    key = (alias, target_id)
    existing = rows.get(key)
    if existing is None:
        entry: Dict[str, Any] = {
            "alias": alias,
            "target_id": target_id,
            "target_category": target_category,
            "sources": [source],
        }
        if language and language.strip():
            entry["language"] = language
        rows[key] = entry
        return

    if source not in existing["sources"]:
        existing["sources"] = sorted((*existing["sources"], source))
    if "language" not in existing and language and language.strip():
        existing["language"] = language


def _normalize_alias(value: str | None) -> str:
    if value is None:
        return ""
    normalized = _WHITESPACE_RE.sub(" ", value.strip().lower())
    return normalized


def _require_non_empty(value: str | None, path: str) -> None:
    if value is None or not str(value).strip():
        raise SearchAliasesGenerationError(f"projection {path} is required")
