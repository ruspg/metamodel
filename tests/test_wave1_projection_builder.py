from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from tools.wave1 import load_ontology
from tools.wave1.model import GlossaryAlias
from tools.wave1.projection_builder import ProjectionBuildError, build_projection_model


ROOT = Path(__file__).resolve().parents[1]


def _baseline_ontology():
    return load_ontology(
        ROOT / "data/bank_metamodel_horizontal.yaml",
        relation_catalog_path=ROOT / "docs/architecture/relation_catalog_v2_spec.yaml",
    )


def test_projection_builder_happy_path_from_validated_baseline() -> None:
    ontology = _baseline_ontology()

    projected = build_projection_model(ontology, profile="atlas_mvp")

    assert projected.metadata.active_profile == "atlas_mvp"
    assert projected.metadata.model_name == ontology.meta["model_name"]
    assert projected.entity_kinds
    assert projected.relation_kinds
    assert projected.relation_entries
    assert projected.qualifier_references


def test_projection_builder_is_deterministic() -> None:
    ontology = _baseline_ontology()

    first = build_projection_model(ontology, profile="atlas_mvp")
    second = build_projection_model(ontology, profile="atlas_mvp")

    assert first == second
    assert [kind.id for kind in first.entity_kinds] == sorted(kind.id for kind in first.entity_kinds)
    assert [relation.id for relation in first.relation_kinds] == sorted(
        relation.id for relation in first.relation_kinds
    )
    assert [entry.id for entry in first.relation_entries] == sorted(
        entry.id for entry in first.relation_entries
    )


def test_projection_builder_profile_applicability_shaping() -> None:
    ontology = _baseline_ontology()

    relation = ontology.relation_catalog.relations[0]
    patched_relation = replace(
        relation,
        payload={**relation.payload, "applies_to_profiles": ["atlas_mvp"]},
    )
    relation_catalog = replace(
        ontology.relation_catalog,
        relations=(patched_relation, *ontology.relation_catalog.relations[1:]),
    )

    patched_alias = GlossaryAlias(
        id="wave1.test.alias",
        term="business_process",
        alias="proc",
        language="en",
        extra={"applies_to_profiles": ["atlas_mvp"]},
    )

    patched = replace(
        ontology,
        relation_catalog=relation_catalog,
        glossary_aliases=(patched_alias, *ontology.glossary_aliases),
    )

    atlas_projection = build_projection_model(patched, profile="atlas_mvp")
    other_projection = build_projection_model(patched, profile="non_matching_profile")

    atlas_relation_ids = {item.id for item in atlas_projection.relation_entries}
    other_relation_ids = {item.id for item in other_projection.relation_entries}
    assert patched_relation.id in atlas_relation_ids
    assert patched_relation.id not in other_relation_ids

    atlas_alias_ids = {item.id for item in atlas_projection.aliases}
    other_alias_ids = {item.id for item in other_projection.aliases}
    assert patched_alias.id in atlas_alias_ids
    assert patched_alias.id not in other_alias_ids


def test_projection_builder_fails_when_required_structure_missing() -> None:
    ontology = _baseline_ontology()
    broken = replace(ontology, relation_catalog=None)

    with pytest.raises(ProjectionBuildError) as exc_info:
        build_projection_model(broken)

    assert "relation_catalog" in str(exc_info.value)
