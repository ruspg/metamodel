from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from tools.wave1.loader import OntologyLoadError, load_ontology


ROOT = Path(__file__).resolve().parents[1]


def test_loads_legacy_wave1_input_with_relation_catalog() -> None:
    ontology = load_ontology(
        ROOT / "model/metamodel.yaml",
        relation_catalog_path=ROOT / "model/relation_catalog.yaml",
    )

    assert ontology.meta["model_name"] == "bank_metamodel_horizontal"
    assert ontology.entity_kinds
    assert ontology.relation_kinds
    assert ontology.attribute_definitions

    assert ontology.relation_catalog is not None
    assert ontology.relation_catalog.relations
    relation_ids = [relation.id for relation in ontology.relation_catalog.relations]
    assert relation_ids == sorted(relation_ids)


def test_missing_required_sections_fails(tmp_path: Path) -> None:
    invalid_path = tmp_path / "invalid.yaml"
    invalid_path.write_text(yaml.safe_dump({"meta": {"version": 1}}), encoding="utf-8")

    with pytest.raises(OntologyLoadError) as exc_info:
        load_ontology(invalid_path)

    assert "missing required top-level section" in str(exc_info.value)
    assert "entity_kinds" in str(exc_info.value)


def test_normalization_is_deterministic(tmp_path: Path) -> None:
    data = {
        "meta": {"bank_code": "B", "model_name": "x", "version": 1},
        "relation_kinds": [
            {"id": "rel_b", "from_kind": "e2", "to_kind": "e1"},
            {"id": "rel_a", "from_kind": "e1", "to_kind": "e2"},
        ],
        "entity_kinds": [
            {
                "id": "e2",
                "attributes": [
                    {"id": "e2.b", "description": "b"},
                    {"id": "e2.a", "description": "a"},
                ],
            },
            {"id": "e1"},
        ],
    }
    path = tmp_path / "unsorted.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    first = load_ontology(path)
    second = load_ontology(path)

    assert first == second
    assert [item.id for item in first.entity_kinds] == ["e1", "e2"]
    assert [item.id for item in first.relation_kinds] == ["rel_a", "rel_b"]
    assert [item.id for item in first.attribute_definitions] == ["e2.a", "e2.b"]
