"""Wave 1 compatibility report artifact generator."""
from __future__ import annotations

from typing import Mapping, Sequence

from .atlas_bundle_model import AtlasBundleArtifactPlan
from .metamodel_snapshot_generator import build_metamodel_snapshot
from .projection_model import ProjectionModel
from .relation_catalog_generator import build_relation_catalog
from .search_aliases_generator import build_search_aliases
from .type_catalog_generator import build_type_catalog

_REQUIRED_ARTIFACT_IDS = (
    "metamodel_snapshot",
    "type_catalog",
    "relation_catalog",
    "search_aliases",
    "compatibility_report",
)


class CompatibilityReportGenerationError(ValueError):
    """Raised when compatibility report cannot be produced."""


def build_compatibility_report(
    projection: ProjectionModel,
    *,
    artifact_inventory: Sequence[AtlasBundleArtifactPlan],
) -> str:
    """Build deterministic human-readable and machine-friendly compatibility report."""

    _validate_inventory(artifact_inventory)
    _require_non_empty(projection.metadata.model_name, "metadata.model_name")
    _require_non_empty(projection.metadata.version, "metadata.version")
    _require_non_empty(projection.metadata.bank_code, "metadata.bank_code")
    _require_non_empty(projection.metadata.active_profile, "metadata.active_profile")

    try:
        snapshot = build_metamodel_snapshot(projection)
        type_catalog = build_type_catalog(projection)
        relation_catalog = build_relation_catalog(projection)
        search_aliases = build_search_aliases(projection)
    except ValueError as exc:
        raise CompatibilityReportGenerationError(str(exc)) from exc

    _require_profile_coherence(
        projection.metadata.active_profile,
        snapshot=snapshot,
        type_catalog=type_catalog,
        relation_catalog=relation_catalog,
        search_aliases=search_aliases,
    )

    checks = _coherence_checks(snapshot, type_catalog, relation_catalog, search_aliases)
    warnings = _warnings(search_aliases)

    lines = [
        "# Wave 1 Compatibility Report",
        "",
        "## Bundle Identity",
        f"- model_name: `{projection.metadata.model_name}`",
        f"- model_version: `{projection.metadata.version}`",
        f"- bank_code: `{projection.metadata.bank_code}`",
        f"- profile: `{projection.metadata.active_profile}`",
        "",
        "## Artifact Inventory",
    ]

    for item in sorted(artifact_inventory, key=lambda value: value.artifact_id):
        status = "placeholder" if item.placeholder else "generated"
        lines.append(
            f"- `{item.artifact_id}` ({status}) → `{item.relative_path}`"
        )

    lines.extend(
        (
            "",
            "## Artifact Summary Counts",
            f"- entity_kinds: `{snapshot['counts']['entity_kind_count']}`",
            f"- attributes: `{type_catalog['counts']['attribute_count']}`",
            f"- relations: `{relation_catalog['counts']['relation_count']}`",
            f"- qualifiers: `{relation_catalog['counts']['qualifier_count']}`",
            f"- aliases: `{search_aliases['counts']['alias_count']}`",
            f"- unresolved_aliases: `{search_aliases['counts']['unresolved_alias_count']}`",
            "",
            "## Validation/Compatibility Status",
        )
    )

    for check_name, passed, detail in checks:
        marker = "PASS" if passed else "FAIL"
        lines.append(f"- {check_name}: **{marker}** ({detail})")

    lines.extend(("", "## Import-Relevant Notes"))
    if warnings:
        for warning in warnings:
            lines.append(f"- WARNING: {warning}")
    else:
        lines.append("- No compatibility warnings detected.")

    return "\n".join(lines) + "\n"


def _validate_inventory(artifact_inventory: Sequence[AtlasBundleArtifactPlan]) -> None:
    by_id = {item.artifact_id for item in artifact_inventory}
    missing = [artifact_id for artifact_id in _REQUIRED_ARTIFACT_IDS if artifact_id not in by_id]
    if missing:
        joined = ", ".join(sorted(missing))
        raise CompatibilityReportGenerationError(
            f"artifact_inventory is missing required artifact(s): {joined}"
        )


def _require_profile_coherence(active_profile: str, **artifacts: Mapping[str, object]) -> None:
    for name, payload in artifacts.items():
        profile = payload.get("model", {}).get("profile")
        if profile != active_profile:
            raise CompatibilityReportGenerationError(
                f"profile mismatch in {name}: expected '{active_profile}', got '{profile}'"
            )


def _coherence_checks(
    snapshot: Mapping[str, object],
    type_catalog: Mapping[str, object],
    relation_catalog: Mapping[str, object],
    search_aliases: Mapping[str, object],
) -> tuple[tuple[str, bool, str], ...]:
    snapshot_kind_count = int(snapshot["counts"]["entity_kind_count"])
    type_kind_count = int(type_catalog["counts"]["kind_count"])
    relation_count = int(relation_catalog["counts"]["relation_count"])
    alias_count = int(search_aliases["counts"]["alias_count"])

    inverse_ok = _inverse_integrity_ok(relation_catalog)

    return (
        (
            "snapshot_type_kind_count_match",
            snapshot_kind_count == type_kind_count,
            f"snapshot={snapshot_kind_count}, type_catalog={type_kind_count}",
        ),
        (
            "relation_catalog_non_empty",
            relation_count > 0,
            f"relation_count={relation_count}",
        ),
        (
            "search_aliases_non_empty",
            alias_count > 0,
            f"alias_count={alias_count}",
        ),
        (
            "relation_inverse_integrity",
            inverse_ok,
            "validated from generated relation_catalog",
        ),
    )


def _inverse_integrity_ok(relation_catalog: Mapping[str, object]) -> bool:
    relations = relation_catalog.get("relations", ())
    by_id = {item.get("id"): item for item in relations}
    for relation in relations:
        has_inverse = bool(relation.get("has_inverse"))
        inverse_id = relation.get("inverse_relation_id")
        if has_inverse:
            if not inverse_id:
                return False
            inverse = by_id.get(inverse_id)
            if inverse is None:
                return False
            if inverse.get("inverse_relation_id") != relation.get("id"):
                return False
            if inverse.get("from_kind") != relation.get("to_kind"):
                return False
            if inverse.get("to_kind") != relation.get("from_kind"):
                return False
    return True


def _warnings(search_aliases: Mapping[str, object]) -> tuple[str, ...]:
    unresolved = int(search_aliases["counts"]["unresolved_alias_count"])
    if unresolved > 0:
        return (f"unresolved_alias_count={unresolved}; unresolved aliases were excluded",)
    return ()


def _require_non_empty(value: str | None, path: str) -> None:
    if value is None or not str(value).strip():
        raise CompatibilityReportGenerationError(f"projection {path} is required")
