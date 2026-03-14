"""Determinism and reproducibility checks for Wave 1 atlas bundles."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence, Tuple

from .atlas_bundle_generator import generate_atlas_bundle
from .atlas_bundle_model import AtlasBundleOptions
from .projection_model import ProjectionModel


@dataclass(frozen=True)
class BundleDeterminismResult:
    is_deterministic: bool
    first_bundle_root: str
    second_bundle_root: str
    checked_files: Tuple[str, ...]
    diagnostics: Tuple[str, ...]


class BundleDeterminismError(ValueError):
    """Raised when deterministic bundle verification cannot be completed."""


def verify_bundle_determinism(
    projection: ProjectionModel,
    output_root: Path | str,
    *,
    options: AtlasBundleOptions | None = None,
) -> BundleDeterminismResult:
    """Generate two bundles from the same input and verify byte-for-byte reproducibility."""

    root = Path(output_root)
    run_a_root = root / "determinism_run_a"
    run_b_root = root / "determinism_run_b"

    effective_options = options or AtlasBundleOptions(profile=projection.metadata.active_profile)

    first = generate_atlas_bundle(projection, run_a_root, options=effective_options)
    second = generate_atlas_bundle(projection, run_b_root, options=effective_options)

    return compare_bundle_outputs(Path(first.bundle_root), Path(second.bundle_root))


def compare_bundle_outputs(bundle_root_a: Path | str, bundle_root_b: Path | str) -> BundleDeterminismResult:
    """Compare two existing bundles for deterministic path/content/order stability."""

    first_root = Path(bundle_root_a)
    second_root = Path(bundle_root_b)
    if not first_root.exists() or not second_root.exists():
        raise BundleDeterminismError("both bundle roots must exist for determinism comparison")

    files_a = _collect_relative_files(first_root)
    files_b = _collect_relative_files(second_root)

    diagnostics: list[str] = []
    if files_a != files_b:
        missing_in_b = sorted(set(files_a) - set(files_b))
        missing_in_a = sorted(set(files_b) - set(files_a))
        if missing_in_b:
            diagnostics.append(f"missing_in_second={missing_in_b}")
        if missing_in_a:
            diagnostics.append(f"missing_in_first={missing_in_a}")

    checked = tuple(sorted(set(files_a) & set(files_b)))
    for relative in checked:
        bytes_a = (first_root / relative).read_bytes()
        bytes_b = (second_root / relative).read_bytes()
        if bytes_a != bytes_b:
            diagnostics.append(f"content_mismatch:{relative}")

    diagnostics.extend(_ordering_diagnostics(first_root))

    return BundleDeterminismResult(
        is_deterministic=not diagnostics,
        first_bundle_root=str(first_root),
        second_bundle_root=str(second_root),
        checked_files=checked,
        diagnostics=tuple(sorted(diagnostics)),
    )


def _collect_relative_files(bundle_root: Path) -> Tuple[str, ...]:
    return tuple(
        sorted(
            str(path.relative_to(bundle_root))
            for path in bundle_root.rglob("*")
            if path.is_file()
        )
    )


def _ordering_diagnostics(bundle_root: Path) -> Sequence[str]:
    diagnostics: list[str] = []

    manifest = _read_json(bundle_root / "bundle_manifest.json")
    artifact_ids = [item["artifact_id"] for item in manifest["artifacts"]]
    expected_order = [
        "metamodel_snapshot",
        "type_catalog",
        "relation_catalog",
        "search_aliases",
        "compatibility_report",
    ]
    if artifact_ids != expected_order:
        diagnostics.append("manifest_artifact_order_mismatch")

    snapshot = _read_json(bundle_root / "artifacts" / "metamodel_snapshot.json")
    if [item["id"] for item in snapshot["entity_kinds"]] != sorted(
        item["id"] for item in snapshot["entity_kinds"]
    ):
        diagnostics.append("snapshot_entity_kind_order_mismatch")
    if [item["id"] for item in snapshot["relations"]] != sorted(
        item["id"] for item in snapshot["relations"]
    ):
        diagnostics.append("snapshot_relation_order_mismatch")

    type_catalog = _read_json(bundle_root / "artifacts" / "type_catalog.json")
    type_ids = [item["id"] for item in type_catalog["kinds"]]
    if type_ids != sorted(type_ids):
        diagnostics.append("type_catalog_kind_order_mismatch")
    for kind in type_catalog["kinds"]:
        attr_ids = [item["id"] for item in kind["attributes"]]
        if attr_ids != sorted(attr_ids):
            diagnostics.append(f"type_catalog_attribute_order_mismatch:{kind['id']}")

    relation_catalog = _read_json(bundle_root / "artifacts" / "relation_catalog.json")
    relation_ids = [item["id"] for item in relation_catalog["relations"]]
    if relation_ids != sorted(relation_ids):
        diagnostics.append("relation_catalog_relation_order_mismatch")
    for relation in relation_catalog["relations"]:
        allowed = relation.get("allowed_qualifiers", [])
        required = relation.get("required_qualifiers", [])
        if list(allowed) != sorted(allowed):
            diagnostics.append(f"relation_catalog_allowed_qualifier_order_mismatch:{relation['id']}")
        if list(required) != sorted(required):
            diagnostics.append(f"relation_catalog_required_qualifier_order_mismatch:{relation['id']}")

    search_aliases = _read_json(bundle_root / "artifacts" / "search_aliases.json")
    alias_pairs = [(item["alias"], item["target_id"]) for item in search_aliases["aliases"]]
    if alias_pairs != sorted(alias_pairs):
        diagnostics.append("search_aliases_order_mismatch")

    report_lines = (bundle_root / "artifacts" / "compatibility_report.md").read_text(encoding="utf-8").splitlines()
    expected_sections = [
        "# Wave 1 Compatibility Report",
        "## Bundle Identity",
        "## Artifact Inventory",
        "## Artifact Summary Counts",
        "## Validation/Compatibility Status",
        "## Import-Relevant Notes",
    ]
    cursor = 0
    for section in expected_sections:
        try:
            index = report_lines.index(section)
        except ValueError:
            diagnostics.append(f"compatibility_report_missing_section:{section}")
            continue
        if index < cursor:
            diagnostics.append("compatibility_report_section_order_mismatch")
            break
        cursor = index

    return diagnostics


def _read_json(path: Path) -> dict:
    if not path.exists():
        raise BundleDeterminismError(f"required artifact missing for determinism check: {path}")
    return json.loads(path.read_text(encoding="utf-8"))
