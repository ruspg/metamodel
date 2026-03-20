from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from tools.wave1 import load_ontology
from tools.wave1.atlas_bundle_generator import _ARTIFACT_PLANS
from tools.wave1.compatibility_report_generator import (
    CompatibilityReportGenerationError,
    build_compatibility_report,
)
from tools.wave1.projection_builder import build_projection_model


ROOT = Path(__file__).resolve().parents[1]


def _baseline_projection():
    ontology = load_ontology(
        ROOT / "model/metamodel.yaml",
        relation_catalog_path=ROOT / "model/relation_catalog.yaml",
    )
    return build_projection_model(ontology, profile="atlas_mvp")


def test_compatibility_report_happy_path() -> None:
    projection = _baseline_projection()

    report = build_compatibility_report(projection, artifact_inventory=_ARTIFACT_PLANS)

    assert "# Wave 1 Compatibility Report" in report
    assert "## Artifact Inventory" in report
    assert "snapshot_type_kind_count_match" in report


def test_compatibility_report_is_deterministic() -> None:
    projection = _baseline_projection()

    first = build_compatibility_report(projection, artifact_inventory=_ARTIFACT_PLANS)
    second = build_compatibility_report(projection, artifact_inventory=_ARTIFACT_PLANS)

    assert first == second


def test_compatibility_report_inventory_contains_required_artifacts() -> None:
    projection = _baseline_projection()
    broken_inventory = tuple(item for item in _ARTIFACT_PLANS if item.artifact_id != "type_catalog")

    with pytest.raises(CompatibilityReportGenerationError) as exc_info:
        build_compatibility_report(projection, artifact_inventory=broken_inventory)

    assert "missing required artifact" in str(exc_info.value)


def test_compatibility_report_fails_for_missing_metadata() -> None:
    projection = _baseline_projection()
    broken_projection = replace(
        projection,
        metadata=replace(projection.metadata, model_name=""),
    )

    with pytest.raises(CompatibilityReportGenerationError) as exc_info:
        build_compatibility_report(broken_projection, artifact_inventory=_ARTIFACT_PLANS)

    assert "metadata.model_name" in str(exc_info.value)
