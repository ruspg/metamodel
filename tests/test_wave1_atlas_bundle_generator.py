from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest

from tools.wave1 import load_ontology
from tools.wave1.atlas_bundle_generator import (
    AtlasBundleGenerationError,
    generate_atlas_bundle,
)
from tools.wave1.atlas_bundle_model import AtlasBundleOptions
from tools.wave1.projection_builder import build_projection_model


ROOT = Path(__file__).resolve().parents[1]


def _baseline_projection():
    ontology = load_ontology(
        ROOT / "model/metamodel.yaml",
        relation_catalog_path=ROOT / "model/relation_catalog.yaml",
    )
    return build_projection_model(ontology, profile="atlas_mvp")


def _active_relation_count(projection) -> int:
    kind_ids = {kind.id for kind in projection.entity_kinds}
    return sum(
        1
        for relation in projection.relation_entries
        if relation.from_kind in kind_ids and relation.to_kind in kind_ids
    )


def test_generate_atlas_bundle_happy_path(tmp_path: Path) -> None:
    projection = _baseline_projection()

    result = generate_atlas_bundle(projection, tmp_path)

    assert Path(result.bundle_root).exists()
    assert Path(result.manifest_path).exists()
    assert Path(result.artifacts_root).exists()
    assert result.manifest.artifact_count == 5
    assert len(result.artifact_paths) == 5
    assert all(Path(path).exists() for path in result.artifact_paths)


def test_generate_atlas_bundle_layout_is_deterministic(tmp_path: Path) -> None:
    projection = _baseline_projection()
    options = AtlasBundleOptions(
        profile="atlas_mvp",
        generated_at_utc="2025-01-01T00:00:00Z",
    )

    first = generate_atlas_bundle(projection, tmp_path, options=options)
    second = generate_atlas_bundle(projection, tmp_path, options=options)

    assert first.bundle_root == second.bundle_root
    assert first.manifest_path == second.manifest_path
    assert first.artifact_paths == second.artifact_paths


def test_generate_atlas_bundle_metamodel_snapshot_is_real_artifact(tmp_path: Path) -> None:
    projection = _baseline_projection()

    result = generate_atlas_bundle(projection, tmp_path)
    snapshot_path = Path(result.bundle_root) / "artifacts" / "metamodel_snapshot.json"
    payload = json.loads(snapshot_path.read_text(encoding="utf-8"))

    assert payload["schema_version"] == "wave1.metamodel_snapshot/v1"
    assert payload["model"]["profile"] == "atlas_mvp"
    assert payload["model"]["model_name"] == projection.metadata.model_name
    assert payload["counts"]["entity_kind_count"] == len(projection.entity_kinds)
    assert payload["counts"]["relation_kind_count"] == len(projection.relation_kinds)
    assert [item["id"] for item in payload["entity_kinds"]] == [
        kind.id for kind in projection.entity_kinds
    ]


def test_generate_atlas_bundle_type_catalog_is_real_artifact(tmp_path: Path) -> None:
    projection = _baseline_projection()

    result = generate_atlas_bundle(projection, tmp_path)
    catalog_path = Path(result.bundle_root) / "artifacts" / "type_catalog.json"
    payload = json.loads(catalog_path.read_text(encoding="utf-8"))

    assert payload["schema_version"] == "wave1.type_catalog/v1"
    assert payload["model"]["profile"] == "atlas_mvp"
    assert payload["counts"]["kind_count"] == len(projection.entity_kinds)


def test_generate_atlas_bundle_relation_catalog_is_real_artifact(tmp_path: Path) -> None:
    projection = _baseline_projection()

    result = generate_atlas_bundle(projection, tmp_path)
    catalog_path = Path(result.bundle_root) / "artifacts" / "relation_catalog.json"
    payload = json.loads(catalog_path.read_text(encoding="utf-8"))

    assert payload["schema_version"] == "wave1.relation_catalog/v1"
    assert payload["model"]["profile"] == "atlas_mvp"
    assert payload["counts"]["relation_count"] == _active_relation_count(projection)


def test_generate_atlas_bundle_search_aliases_is_real_artifact(tmp_path: Path) -> None:
    projection = _baseline_projection()

    result = generate_atlas_bundle(projection, tmp_path)
    alias_path = Path(result.bundle_root) / "artifacts" / "search_aliases.json"
    payload = json.loads(alias_path.read_text(encoding="utf-8"))

    assert payload["schema_version"] == "wave1.search_aliases/v1"
    assert payload["model"]["profile"] == "atlas_mvp"
    assert payload["counts"]["alias_count"] > 0


def test_generate_atlas_bundle_compatibility_report_is_real_artifact(tmp_path: Path) -> None:
    projection = _baseline_projection()

    result = generate_atlas_bundle(projection, tmp_path)
    report_path = Path(result.bundle_root) / "artifacts" / "compatibility_report.md"
    payload = report_path.read_text(encoding="utf-8")

    assert "# Wave 1 Compatibility Report" in payload
    assert "## Artifact Inventory" in payload
    assert "## Validation/Compatibility Status" in payload


def test_generate_atlas_bundle_manifest_structure(tmp_path: Path) -> None:
    projection = _baseline_projection()
    options = AtlasBundleOptions(
        profile="atlas_mvp",
        generated_at_utc="2025-01-01T00:00:00Z",
    )

    result = generate_atlas_bundle(projection, tmp_path, options=options)

    manifest_payload = json.loads(Path(result.manifest_path).read_text(encoding="utf-8"))

    assert manifest_payload["schema_version"] == "wave1.atlas.bundle/v1"
    assert manifest_payload["bundle_kind"] == "atlas_projection_bundle"
    assert manifest_payload["artifact_count"] == 5
    assert [item["artifact_id"] for item in manifest_payload["artifacts"]] == [
        "metamodel_snapshot",
        "type_catalog",
        "relation_catalog",
        "search_aliases",
        "compatibility_report",
    ]
    snapshot_manifest_entry = next(
        item for item in manifest_payload["artifacts"] if item["artifact_id"] == "metamodel_snapshot"
    )
    assert snapshot_manifest_entry["placeholder"] is False
    type_catalog_manifest_entry = next(
        item for item in manifest_payload["artifacts"] if item["artifact_id"] == "type_catalog"
    )
    assert type_catalog_manifest_entry["placeholder"] is False
    relation_catalog_manifest_entry = next(
        item for item in manifest_payload["artifacts"] if item["artifact_id"] == "relation_catalog"
    )
    assert relation_catalog_manifest_entry["placeholder"] is False
    search_aliases_manifest_entry = next(
        item for item in manifest_payload["artifacts"] if item["artifact_id"] == "search_aliases"
    )
    assert search_aliases_manifest_entry["placeholder"] is False
    compatibility_report_manifest_entry = next(
        item for item in manifest_payload["artifacts"] if item["artifact_id"] == "compatibility_report"
    )
    assert compatibility_report_manifest_entry["placeholder"] is False


def test_generate_atlas_bundle_fails_for_missing_projection_metadata(tmp_path: Path) -> None:
    projection = _baseline_projection()
    broken = replace(
        projection,
        metadata=replace(projection.metadata, model_name=""),
    )

    with pytest.raises(AtlasBundleGenerationError) as exc_info:
        generate_atlas_bundle(broken, tmp_path)

    assert "model_name" in str(exc_info.value)


def test_generate_atlas_bundle_fails_for_profile_mismatch(tmp_path: Path) -> None:
    projection = _baseline_projection()
    options = AtlasBundleOptions(profile="not_atlas")

    with pytest.raises(AtlasBundleGenerationError) as exc_info:
        generate_atlas_bundle(projection, tmp_path, options=options)

    assert "options.profile" in str(exc_info.value)


def test_generate_atlas_bundle_contains_required_wave1_minimum_slice(tmp_path: Path) -> None:
    projection = _baseline_projection()

    result = generate_atlas_bundle(projection, tmp_path)

    type_catalog = json.loads((Path(result.bundle_root) / "artifacts" / "type_catalog.json").read_text(encoding="utf-8"))
    relation_catalog = json.loads((Path(result.bundle_root) / "artifacts" / "relation_catalog.json").read_text(encoding="utf-8"))

    required_kind_ids = {
        "business_process",
        "business_operation",
        "it_system",
        "component",
        "business_entity",
    }
    required_relation_ids = {
        "rel_process_decomposes_to_operation",
        "rel_operation_supported_by_system",
        "rel_operation_supported_by_component",
        "rel_process_serves_entity",
    }

    assert required_kind_ids.issubset({item["id"] for item in type_catalog["kinds"]})
    assert required_relation_ids.issubset({item["id"] for item in relation_catalog["relations"]})
