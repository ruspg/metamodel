from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from tools.wave1 import load_ontology
from tools.wave1.projection_builder import build_projection_model
from tools.wave1.projection_model import ProjectionAlias
from tools.wave1.search_aliases_generator import (
    SearchAliasesGenerationError,
    build_search_aliases,
)


ROOT = Path(__file__).resolve().parents[1]


def _baseline_projection():
    ontology = load_ontology(
        ROOT / "model/metamodel.yaml",
        relation_catalog_path=ROOT / "model/relation_catalog.yaml",
    )
    return build_projection_model(ontology, profile="atlas_mvp")


def test_search_aliases_happy_path() -> None:
    projection = _baseline_projection()

    payload = build_search_aliases(projection)

    assert payload["schema_version"] == "wave1.search_aliases/v1"
    assert payload["model"]["profile"] == "atlas_mvp"
    assert payload["counts"]["alias_count"] > 0


def test_search_aliases_is_deterministic() -> None:
    projection = _baseline_projection()

    first = build_search_aliases(projection)
    second = build_search_aliases(projection)

    assert first == second
    assert [item["alias"] for item in first["aliases"]] == sorted(item["alias"] for item in first["aliases"])


def test_search_aliases_deduplicates_alias_entries() -> None:
    projection = _baseline_projection()
    alias_entries = (
        ProjectionAlias(id="a1", term="api", alias="API", language="en", extra={}),
        ProjectionAlias(id="a2", term="api", alias=" api ", language="en", extra={}),
    )
    patched = replace(projection, aliases=alias_entries)

    payload = build_search_aliases(patched)

    api_aliases = [item for item in payload["aliases"] if item["alias"] == "api" and item["target_id"] == "api"]
    assert len(api_aliases) == 1
    assert "glossary_alias" in api_aliases[0]["sources"]


def test_search_aliases_unresolved_alias_targets_are_counted_and_skipped() -> None:
    projection = _baseline_projection()
    alias_entries = (
        ProjectionAlias(id="x1", term="unknown kind", alias="mystery", language="en", extra={}),
    )
    patched = replace(projection, aliases=alias_entries)

    payload = build_search_aliases(patched)

    assert payload["counts"]["unresolved_alias_count"] == 1
    assert all(item["alias"] != "mystery" for item in payload["aliases"])


def test_search_aliases_fails_for_missing_metadata() -> None:
    projection = _baseline_projection()
    broken = replace(projection, metadata=replace(projection.metadata, model_name=""))

    with pytest.raises(SearchAliasesGenerationError) as exc_info:
        build_search_aliases(broken)

    assert "metadata.model_name" in str(exc_info.value)
