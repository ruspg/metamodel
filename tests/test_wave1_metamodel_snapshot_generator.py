from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from tools.wave1 import load_ontology
from tools.wave1.metamodel_snapshot_generator import (
    MetamodelSnapshotGenerationError,
    build_metamodel_snapshot,
)
from tools.wave1.projection_builder import build_projection_model


ROOT = Path(__file__).resolve().parents[1]


def _baseline_projection():
    ontology = load_ontology(
        ROOT / "data/bank_metamodel_horizontal.yaml",
        relation_catalog_path=ROOT / "docs/architecture/relation_catalog_v2_spec.yaml",
    )
    return build_projection_model(ontology, profile="atlas_mvp")


def test_metamodel_snapshot_builder_is_deterministic() -> None:
    projection = _baseline_projection()

    first = build_metamodel_snapshot(projection)
    second = build_metamodel_snapshot(projection)

    assert first == second


def test_metamodel_snapshot_builder_fails_for_missing_metadata() -> None:
    projection = _baseline_projection()
    broken = replace(projection, metadata=replace(projection.metadata, version=""))

    with pytest.raises(MetamodelSnapshotGenerationError) as exc_info:
        build_metamodel_snapshot(broken)

    assert "metadata.version" in str(exc_info.value)
