from __future__ import annotations

from pathlib import Path

from tools.wave1 import load_ontology
from tools.wave1.validator import ensure_valid_ontology, validate_ontology


ROOT = Path(__file__).resolve().parents[1]


def test_validate_happy_path_wave1_inputs() -> None:
    ontology = load_ontology(
        ROOT / "data/bank_metamodel_horizontal.yaml",
        relation_catalog_path=ROOT / "docs/architecture/relation_catalog_v2_spec.yaml",
    )

    result = validate_ontology(ontology)

    assert result.is_valid
    assert result.error_count == 0


def test_validate_missing_reference_case() -> None:
    ontology = load_ontology(
        ROOT / "data/bank_metamodel_horizontal.yaml",
        relation_catalog_path=ROOT / "docs/architecture/relation_catalog_v2_spec.yaml",
    )

    broken_relation = ontology.relation_catalog.relations[0]
    broken_payload = dict(broken_relation.payload)
    broken_payload["supports_qualifiers"] = True
    broken_payload["allowed_qualifiers"] = ["missing_qualifier"]
    broken_catalog = ontology.relation_catalog.__class__(
        version=ontology.relation_catalog.version,
        status=ontology.relation_catalog.status,
        purpose=ontology.relation_catalog.purpose,
        profiles=ontology.relation_catalog.profiles,
        qualifier_references=ontology.relation_catalog.qualifier_references,
        relations=(
            broken_relation.__class__(
                id=broken_relation.id,
                from_kind=broken_relation.from_kind,
                to_kind=broken_relation.to_kind,
                payload=broken_payload,
            ),
            *ontology.relation_catalog.relations[1:],
        ),
    )
    broken_ontology = ontology.__class__(
        meta=ontology.meta,
        dictionaries=ontology.dictionaries,
        entity_kinds=ontology.entity_kinds,
        attribute_definitions=ontology.attribute_definitions,
        relation_kinds=ontology.relation_kinds,
        qualifier_definitions=ontology.qualifier_definitions,
        glossary_aliases=ontology.glossary_aliases,
        profiles=ontology.profiles,
        relation_catalog=broken_catalog,
    )

    result = validate_ontology(broken_ontology)

    assert not result.is_valid
    assert any(error.code == "missing_reference" and "qualifiers" in error.path for error in result.errors)


def test_validate_duplicate_id_case() -> None:
    ontology = load_ontology(
        ROOT / "data/bank_metamodel_horizontal.yaml",
        relation_catalog_path=ROOT / "docs/architecture/relation_catalog_v2_spec.yaml",
    )
    duplicate_entity = ontology.entity_kinds[0]
    broken_ontology = ontology.__class__(
        meta=ontology.meta,
        dictionaries=ontology.dictionaries,
        entity_kinds=(*ontology.entity_kinds, duplicate_entity),
        attribute_definitions=ontology.attribute_definitions,
        relation_kinds=ontology.relation_kinds,
        qualifier_definitions=ontology.qualifier_definitions,
        glossary_aliases=ontology.glossary_aliases,
        profiles=ontology.profiles,
        relation_catalog=ontology.relation_catalog,
    )

    result = validate_ontology(broken_ontology)

    assert not result.is_valid
    assert any(error.code == "duplicate_id" and error.path == "entity_kinds" for error in result.errors)


def test_validate_invalid_inverse_relation_case() -> None:
    ontology = load_ontology(
        ROOT / "data/bank_metamodel_horizontal.yaml",
        relation_catalog_path=ROOT / "docs/architecture/relation_catalog_v2_spec.yaml",
    )
    rel = ontology.relation_catalog.relations[0]
    payload = dict(rel.payload)
    payload["has_inverse"] = True
    payload["inverse_relation_id"] = "rel_missing_inverse"
    broken_catalog = ontology.relation_catalog.__class__(
        version=ontology.relation_catalog.version,
        status=ontology.relation_catalog.status,
        purpose=ontology.relation_catalog.purpose,
        profiles=ontology.relation_catalog.profiles,
        qualifier_references=ontology.relation_catalog.qualifier_references,
        relations=(
            rel.__class__(
                id=rel.id,
                from_kind=rel.from_kind,
                to_kind=rel.to_kind,
                payload=payload,
            ),
            *ontology.relation_catalog.relations[1:],
        ),
    )
    broken_ontology = ontology.__class__(
        meta=ontology.meta,
        dictionaries=ontology.dictionaries,
        entity_kinds=ontology.entity_kinds,
        attribute_definitions=ontology.attribute_definitions,
        relation_kinds=ontology.relation_kinds,
        qualifier_definitions=ontology.qualifier_definitions,
        glossary_aliases=ontology.glossary_aliases,
        profiles=ontology.profiles,
        relation_catalog=broken_catalog,
    )

    result = validate_ontology(broken_ontology)

    assert not result.is_valid
    assert any(error.code == "missing_reference" and "inverse_relation_id" in error.path for error in result.errors)


def test_validate_invalid_enum_value_case() -> None:
    ontology = load_ontology(
        ROOT / "data/bank_metamodel_horizontal.yaml",
        relation_catalog_path=ROOT / "docs/architecture/relation_catalog_v2_spec.yaml",
    )
    rel = ontology.relation_catalog.relations[0]
    payload = dict(rel.payload)
    payload["path_priority"] = "urgent"
    broken_catalog = ontology.relation_catalog.__class__(
        version=ontology.relation_catalog.version,
        status=ontology.relation_catalog.status,
        purpose=ontology.relation_catalog.purpose,
        profiles=ontology.relation_catalog.profiles,
        qualifier_references=ontology.relation_catalog.qualifier_references,
        relations=(
            rel.__class__(
                id=rel.id,
                from_kind=rel.from_kind,
                to_kind=rel.to_kind,
                payload=payload,
            ),
            *ontology.relation_catalog.relations[1:],
        ),
    )
    broken_ontology = ontology.__class__(
        meta=ontology.meta,
        dictionaries=ontology.dictionaries,
        entity_kinds=ontology.entity_kinds,
        attribute_definitions=ontology.attribute_definitions,
        relation_kinds=ontology.relation_kinds,
        qualifier_definitions=ontology.qualifier_definitions,
        glossary_aliases=ontology.glossary_aliases,
        profiles=ontology.profiles,
        relation_catalog=broken_catalog,
    )

    result = validate_ontology(broken_ontology)

    assert not result.is_valid
    assert any(error.code == "invalid_enum" and "path_priority" in error.path for error in result.errors)


def test_ensure_valid_ontology_raises_readable_error() -> None:
    ontology = load_ontology(
        ROOT / "data/bank_metamodel_horizontal.yaml",
        relation_catalog_path=ROOT / "docs/architecture/relation_catalog_v2_spec.yaml",
    )
    rel = ontology.relation_catalog.relations[0]
    payload = dict(rel.payload)
    payload["impact_mode"] = "boom"
    broken_catalog = ontology.relation_catalog.__class__(
        version=ontology.relation_catalog.version,
        status=ontology.relation_catalog.status,
        purpose=ontology.relation_catalog.purpose,
        profiles=ontology.relation_catalog.profiles,
        qualifier_references=ontology.relation_catalog.qualifier_references,
        relations=(
            rel.__class__(
                id=rel.id,
                from_kind=rel.from_kind,
                to_kind=rel.to_kind,
                payload=payload,
            ),
            *ontology.relation_catalog.relations[1:],
        ),
    )
    broken_ontology = ontology.__class__(
        meta=ontology.meta,
        dictionaries=ontology.dictionaries,
        entity_kinds=ontology.entity_kinds,
        attribute_definitions=ontology.attribute_definitions,
        relation_kinds=ontology.relation_kinds,
        qualifier_definitions=ontology.qualifier_definitions,
        glossary_aliases=ontology.glossary_aliases,
        profiles=ontology.profiles,
        relation_catalog=broken_catalog,
    )

    try:
        ensure_valid_ontology(broken_ontology)
    except ValueError as exc:
        message = str(exc)
    else:
        raise AssertionError("ensure_valid_ontology must raise on invalid ontology")

    assert "Wave 1 ontology validation failed" in message
    assert "impact_mode" in message
