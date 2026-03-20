from __future__ import annotations

from pathlib import Path

from tools.wave1 import load_ontology
from tools.wave1.atlas_bundle_generator import generate_atlas_bundle
from tools.wave1.bundle_determinism import compare_bundle_outputs, verify_bundle_determinism
from tools.wave1.projection_builder import build_projection_model


ROOT = Path(__file__).resolve().parents[1]


def _baseline_projection():
    ontology = load_ontology(
        ROOT / "model/metamodel.yaml",
        relation_catalog_path=ROOT / "model/relation_catalog.yaml",
    )
    return build_projection_model(ontology, profile="atlas_mvp")


def test_verify_bundle_determinism_happy_path(tmp_path: Path) -> None:
    projection = _baseline_projection()

    result = verify_bundle_determinism(projection, tmp_path)

    assert result.is_deterministic
    assert result.diagnostics == ()
    assert "bundle_manifest.json" in result.checked_files


def test_verify_bundle_determinism_checks_expected_ordering(tmp_path: Path) -> None:
    projection = _baseline_projection()

    result = verify_bundle_determinism(projection, tmp_path)

    assert result.is_deterministic
    assert "artifacts/compatibility_report.md" in result.checked_files
    assert "artifacts/relation_catalog.json" in result.checked_files
    assert "artifacts/search_aliases.json" in result.checked_files


def test_compare_bundle_outputs_reports_content_drift(tmp_path: Path) -> None:
    projection = _baseline_projection()
    first = generate_atlas_bundle(projection, tmp_path / "run1")
    second = generate_atlas_bundle(projection, tmp_path / "run2")

    report_path = Path(second.bundle_root) / "artifacts" / "compatibility_report.md"
    report_path.write_text(report_path.read_text(encoding="utf-8") + "\nDRIFT\n", encoding="utf-8")

    result = compare_bundle_outputs(first.bundle_root, second.bundle_root)

    assert not result.is_deterministic
    assert any(item.startswith("content_mismatch:artifacts/compatibility_report.md") for item in result.diagnostics)
