from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from tools.wave1 import (
    ensure_valid_relation_catalog,
    load_ontology,
    validate_relation_catalog,
)


ROOT = Path(__file__).resolve().parents[1]


def _baseline_ontology():
    return load_ontology(
        ROOT / "data/bank_metamodel_horizontal.yaml",
        relation_catalog_path=ROOT / "docs/architecture/relation_catalog_v2_spec.yaml",
    )


def _replace_relation_payload(ontology, relation_id: str, patch: dict):
    relations = []
    for relation in ontology.relation_catalog.relations:
        if relation.id == relation_id:
            payload = dict(relation.payload)
            payload.update(patch)
            relations.append(replace(relation, payload=payload, from_kind=payload.get("from_kind"), to_kind=payload.get("to_kind")))
        else:
            relations.append(relation)
    catalog = replace(ontology.relation_catalog, relations=tuple(relations))
    return replace(ontology, relation_catalog=catalog)


def _find_inverse_pair(ontology):
    by_id = {relation.id: relation for relation in ontology.relation_catalog.relations}
    for relation in ontology.relation_catalog.relations:
        inverse_id = relation.payload.get("inverse_relation_id")
        if relation.payload.get("has_inverse") is True and isinstance(inverse_id, str) and inverse_id in by_id:
            return relation, by_id[inverse_id]
    raise AssertionError("expected inverse pair in baseline relation catalog")


def test_relation_catalog_happy_path_current_baseline() -> None:
    ontology = _baseline_ontology()

    result = validate_relation_catalog(ontology)

    assert result.error_count == 0


def test_relation_catalog_missing_inverse_reference() -> None:
    ontology = _baseline_ontology()
    relation, _ = _find_inverse_pair(ontology)

    broken = _replace_relation_payload(
        ontology,
        relation.id,
        {"has_inverse": True, "inverse_relation_id": "rel_missing_inverse"},
    )

    result = validate_relation_catalog(broken)

    assert any(item.code == "missing_reference" and "inverse_relation_id" in item.path for item in result.errors)


def test_relation_catalog_inverse_endpoint_mismatch() -> None:
    ontology = _baseline_ontology()
    relation, inverse = _find_inverse_pair(ontology)

    broken = _replace_relation_payload(
        ontology,
        inverse.id,
        {"to_kind": relation.to_kind},
    )

    result = validate_relation_catalog(broken)

    assert any(item.code == "invalid_inverse" and item.path.endswith(inverse.id) for item in result.errors)


def test_relation_catalog_invalid_controlled_enum_values() -> None:
    ontology = _baseline_ontology()
    relation = ontology.relation_catalog.relations[0]

    broken = _replace_relation_payload(
        ontology,
        relation.id,
        {
            "default_visibility": "always_visible",
            "path_priority": "critical",
            "impact_mode": "explode",
        },
    )

    result = validate_relation_catalog(broken)

    assert any("default_visibility" in item.path and item.code == "invalid_enum" for item in result.errors)
    assert any("path_priority" in item.path and item.code == "invalid_enum" for item in result.errors)
    assert any("impact_mode" in item.path and item.code == "invalid_enum" for item in result.errors)


def test_relation_catalog_invalid_qualifier_reference() -> None:
    ontology = _baseline_ontology()
    relation = ontology.relation_catalog.relations[0]

    broken = _replace_relation_payload(
        ontology,
        relation.id,
        {
            "supports_qualifiers": True,
            "allowed_qualifiers": ["missing_qualifier"],
        },
    )

    result = validate_relation_catalog(broken)

    assert any(item.code == "missing_reference" and "qualifiers" in item.path for item in result.errors)


def test_relation_catalog_contradictory_traversal_and_impact_combination() -> None:
    ontology = _baseline_ontology()
    relation = ontology.relation_catalog.relations[0]

    broken = _replace_relation_payload(
        ontology,
        relation.id,
        {
            "allowed_in_paths": False,
            "path_priority": "primary",
            "allowed_in_impact": False,
            "impact_mode": "propagate",
        },
    )

    result = validate_relation_catalog(broken)

    assert any(item.code == "invalid_combination" and "allowed_in_paths" in item.message for item in result.errors)
    assert any(item.code == "invalid_combination" and "allowed_in_impact" in item.message for item in result.errors)


def test_ensure_valid_relation_catalog_raises_readable_error() -> None:
    ontology = _baseline_ontology()
    relation = ontology.relation_catalog.relations[0]
    broken = _replace_relation_payload(ontology, relation.id, {"default_visibility": "broken"})

    try:
        ensure_valid_relation_catalog(broken)
    except ValueError as exc:
        message = str(exc)
    else:
        raise AssertionError("ensure_valid_relation_catalog must raise on invalid relation catalog")

    assert "Wave 1 relation catalog validation failed" in message
    assert "default_visibility" in message
