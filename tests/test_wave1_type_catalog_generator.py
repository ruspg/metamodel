from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from tools.wave1 import load_ontology
from tools.wave1.projection_model import ProjectionEntityKind
from tools.wave1.projection_builder import build_projection_model
from tools.wave1.type_catalog_generator import TypeCatalogGenerationError, build_type_catalog


ROOT = Path(__file__).resolve().parents[1]


def _baseline_projection():
    ontology = load_ontology(
        ROOT / "data/bank_metamodel_horizontal.yaml",
        relation_catalog_path=ROOT / "docs/architecture/relation_catalog_v2_spec.yaml",
    )
    return build_projection_model(ontology, profile="atlas_mvp")


def test_type_catalog_happy_path() -> None:
    projection = _baseline_projection()

    payload = build_type_catalog(projection)

    assert payload["schema_version"] == "wave1.type_catalog/v1"
    assert payload["model"]["profile"] == "atlas_mvp"
    assert payload["counts"]["kind_count"] == len(projection.entity_kinds)
    assert payload["counts"]["attribute_count"] == sum(len(kind.attributes) for kind in projection.entity_kinds)


def test_type_catalog_is_deterministic() -> None:
    projection = _baseline_projection()

    first = build_type_catalog(projection)
    second = build_type_catalog(projection)

    assert first == second
    assert [item["id"] for item in first["kinds"]] == sorted(item["id"] for item in first["kinds"])


def test_type_catalog_attribute_runtime_metadata() -> None:
    projection = _baseline_projection()

    payload = build_type_catalog(projection)

    logical_resource = next(item for item in payload["kinds"] if item["id"] == "logical_resource")
    resource_kind = next(item for item in logical_resource["attributes"] if item["id"] == "logical_resource.resource_kind")

    assert resource_kind["enum_values"] == ("Bucket", "DB", "Namespace", "Queue", "Topic")


def test_type_catalog_fails_for_missing_kind_id() -> None:
    projection = _baseline_projection()
    first_kind = projection.entity_kinds[0]
    broken_first = ProjectionEntityKind(
        id="",
        name=first_kind.name,
        metamodel_level=first_kind.metamodel_level,
        category=first_kind.category,
        description=first_kind.description,
        rules=first_kind.rules,
        attributes=first_kind.attributes,
        extra=first_kind.extra,
    )
    broken = replace(projection, entity_kinds=(broken_first, *projection.entity_kinds[1:]))

    with pytest.raises(TypeCatalogGenerationError) as exc_info:
        build_type_catalog(broken)

    assert "entity_kind.id" in str(exc_info.value)


def test_type_catalog_fails_for_missing_attribute_id() -> None:
    projection = _baseline_projection()
    first_kind_index = next(
        index for index, kind in enumerate(projection.entity_kinds) if kind.attributes
    )
    first_kind = projection.entity_kinds[first_kind_index]

    broken_attribute = replace(first_kind.attributes[0], id="")
    broken_kind = replace(first_kind, attributes=(broken_attribute, *first_kind.attributes[1:]))
    broken_kinds = list(projection.entity_kinds)
    broken_kinds[first_kind_index] = broken_kind
    broken = replace(projection, entity_kinds=tuple(broken_kinds))

    with pytest.raises(TypeCatalogGenerationError) as exc_info:
        build_type_catalog(broken)

    assert "attribute.id" in str(exc_info.value)
