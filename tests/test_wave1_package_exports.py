from __future__ import annotations

from pathlib import Path

from tools.wave1 import (
    format_harness_report,
    load_ontology,
    run_wave1_validation_harness,
    run_wave1_validation_harness_on_model,
)


ROOT = Path(__file__).resolve().parents[1]


def test_wave1_package_exports_include_harness_entrypoints() -> None:
    ontology_path = ROOT / "model/metamodel.yaml"
    relation_catalog_path = ROOT / "model/relation_catalog.yaml"

    by_path = run_wave1_validation_harness(
        ontology_path,
        relation_catalog_path=relation_catalog_path,
    )

    ontology = load_ontology(ontology_path, relation_catalog_path=relation_catalog_path)
    by_model = run_wave1_validation_harness_on_model(ontology)

    assert by_path == by_model
    report = format_harness_report(by_path)
    assert report.startswith("success=true")
    assert "[ontology_validation]" in report
