from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from tools.wave1 import load_ontology
from tools.wave1.projection_builder import build_projection_model
from tools.wave1.projection_model import ProjectionRelationEntry
from tools.wave1.relation_catalog_generator import (
    RelationCatalogGenerationError,
    build_relation_catalog,
)


ROOT = Path(__file__).resolve().parents[1]


def _baseline_projection():
    ontology = load_ontology(
        ROOT / "data/bank_metamodel_horizontal.yaml",
        relation_catalog_path=ROOT / "docs/architecture/relation_catalog_v2_spec.yaml",
    )
    return build_projection_model(ontology, profile="atlas_mvp")


def _active_relation_count(projection) -> int:
    kind_ids = {kind.id for kind in projection.entity_kinds}
    return sum(
        1
        for relation in projection.relation_entries
        if (relation.from_kind in kind_ids and relation.to_kind in kind_ids)
    )


def test_relation_catalog_happy_path() -> None:
    projection = _baseline_projection()

    payload = build_relation_catalog(projection)

    assert payload["schema_version"] == "wave1.relation_catalog/v1"
    assert payload["model"]["profile"] == "atlas_mvp"
    assert payload["counts"]["relation_count"] == _active_relation_count(projection)


def test_relation_catalog_is_deterministic() -> None:
    projection = _baseline_projection()

    first = build_relation_catalog(projection)
    second = build_relation_catalog(projection)

    assert first == second
    assert [item["id"] for item in first["relations"]] == sorted(item["id"] for item in first["relations"])


def test_relation_catalog_inverse_integrity_and_qualifiers() -> None:
    projection = _baseline_projection()

    payload = build_relation_catalog(projection)

    relations_by_id = {item["id"]: item for item in payload["relations"]}
    relation_with_inverse = next(item for item in payload["relations"] if item["has_inverse"])
    inverse = relations_by_id[relation_with_inverse["inverse_relation_id"]]

    assert inverse["inverse_relation_id"] == relation_with_inverse["id"]
    assert relation_with_inverse["from_kind"] == inverse["to_kind"]
    assert relation_with_inverse["to_kind"] == inverse["from_kind"]
    assert set(relation_with_inverse["required_qualifiers"]).issubset(
        set(relation_with_inverse["allowed_qualifiers"])
    )


def test_relation_catalog_fails_for_missing_required_relation_field() -> None:
    projection = _baseline_projection()
    relation = projection.relation_entries[0]
    broken_relation = ProjectionRelationEntry(
        id=relation.id,
        from_kind=relation.from_kind,
        to_kind=relation.to_kind,
        applies_to_profiles=relation.applies_to_profiles,
        payload={key: value for key, value in relation.payload.items() if key != "direction"},
    )
    broken = replace(projection, relation_entries=(broken_relation, *projection.relation_entries[1:]))

    with pytest.raises(RelationCatalogGenerationError) as exc_info:
        build_relation_catalog(broken)

    assert ".direction is required" in str(exc_info.value)


def test_relation_catalog_fails_for_unknown_inverse_reference() -> None:
    projection = _baseline_projection()

    kind_ids = {kind.id for kind in projection.entity_kinds}
    relation = next(
        item
        for item in projection.relation_entries
        if item.payload.get("has_inverse") is True
        and item.from_kind in kind_ids
        and item.to_kind in kind_ids
    )
    broken_relation = replace(relation, payload={**relation.payload, "inverse_relation_id": "missing_inverse_id"})
    broken_entries = tuple(
        broken_relation if item.id == relation.id else item
        for item in projection.relation_entries
    )
    broken = replace(projection, relation_entries=broken_entries)

    with pytest.raises(RelationCatalogGenerationError) as exc_info:
        build_relation_catalog(broken)

    assert "references unknown relation" in str(exc_info.value)


def test_relation_catalog_endpoints_within_active_kind_set() -> None:
    projection = _baseline_projection()
    kind_ids = {kind.id for kind in projection.entity_kinds}

    payload = build_relation_catalog(projection)

    for relation in payload["relations"]:
        assert relation["from_kind"] in kind_ids
        assert relation["to_kind"] in kind_ids
