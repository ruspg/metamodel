"""Wave 1 atlas projection bundle generator skeleton."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Tuple

from .atlas_bundle_model import (
    AtlasBundleArtifactPlan,
    AtlasBundleManifest,
    AtlasBundleOptions,
    AtlasBundleResult,
)
from .metamodel_snapshot_generator import build_metamodel_snapshot
from .projection_model import ProjectionModel


_MANIFEST_SCHEMA_VERSION = "wave1.atlas.bundle/v1"
_BUNDLE_KIND = "atlas_projection_bundle"
_ARTIFACTS_DIR_NAME = "artifacts"
_MANIFEST_FILE_NAME = "bundle_manifest.json"

_ARTIFACT_PLANS: Tuple[AtlasBundleArtifactPlan, ...] = (
    AtlasBundleArtifactPlan(
        artifact_id="metamodel_snapshot",
        relative_path="artifacts/metamodel_snapshot.json",
        description="Wave 1 atlas metamodel snapshot",
        placeholder=False,
    ),
    AtlasBundleArtifactPlan(
        artifact_id="type_catalog",
        relative_path="artifacts/type_catalog.json",
        description="Wave 1 atlas type catalog placeholder",
    ),
    AtlasBundleArtifactPlan(
        artifact_id="relation_catalog",
        relative_path="artifacts/relation_catalog.json",
        description="Wave 1 atlas relation catalog placeholder",
    ),
    AtlasBundleArtifactPlan(
        artifact_id="search_aliases",
        relative_path="artifacts/search_aliases.json",
        description="Wave 1 atlas search aliases placeholder",
    ),
    AtlasBundleArtifactPlan(
        artifact_id="compatibility_report",
        relative_path="artifacts/compatibility_report.md",
        description="Wave 1 atlas compatibility report placeholder",
    ),
)


class AtlasBundleGenerationError(ValueError):
    """Raised when bundle generation cannot proceed from projection input."""


def generate_atlas_bundle(
    projection: ProjectionModel,
    output_root: Path | str,
    *,
    options: AtlasBundleOptions | None = None,
) -> AtlasBundleResult:
    """Generate Wave 1 atlas bundle skeleton output and deterministic manifest."""

    effective_options = options or AtlasBundleOptions()
    _validate_projection_input(projection)

    root = Path(output_root)
    bundle_name = effective_options.bundle_name or _default_bundle_name(
        projection.metadata.model_name,
        projection.metadata.version,
        effective_options.profile,
    )
    bundle_root = root / bundle_name
    artifacts_root = bundle_root / _ARTIFACTS_DIR_NAME

    artifacts_root.mkdir(parents=True, exist_ok=True)

    artifact_paths = []
    for plan in _ARTIFACT_PLANS:
        artifact_path = bundle_root / plan.relative_path
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        _write_artifact(artifact_path, _build_artifact_payload(projection, plan, effective_options))
        artifact_paths.append(str(artifact_path))

    manifest = AtlasBundleManifest(
        schema_version=_MANIFEST_SCHEMA_VERSION,
        bundle_kind=_BUNDLE_KIND,
        profile=effective_options.profile,
        model_name=projection.metadata.model_name,
        model_version=projection.metadata.version,
        bank_code=projection.metadata.bank_code,
        generated_at_utc=effective_options.generated_at_utc,
        artifact_count=len(_ARTIFACT_PLANS),
        artifacts=_ARTIFACT_PLANS,
    )
    manifest_path = bundle_root / _MANIFEST_FILE_NAME
    _write_json(manifest_path, _manifest_to_json(manifest))

    return AtlasBundleResult(
        bundle_root=str(bundle_root),
        manifest_path=str(manifest_path),
        artifacts_root=str(artifacts_root),
        artifact_paths=tuple(artifact_paths),
        manifest=manifest,
    )


def _validate_projection_input(projection: ProjectionModel) -> None:
    if not projection.metadata.model_name.strip():
        raise AtlasBundleGenerationError("projection metadata.model_name is required")
    if not projection.metadata.version.strip():
        raise AtlasBundleGenerationError("projection metadata.version is required")
    if not projection.metadata.bank_code.strip():
        raise AtlasBundleGenerationError("projection metadata.bank_code is required")


def _default_bundle_name(model_name: str, version: str, profile: str) -> str:
    safe_model = _slugify(model_name)
    safe_version = _slugify(version)
    safe_profile = _slugify(profile)
    return f"{safe_model}__{safe_version}__{safe_profile}"


def _slugify(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")


def _build_artifact_payload(
    projection: ProjectionModel,
    plan: AtlasBundleArtifactPlan,
    options: AtlasBundleOptions,
) -> Any:
    if plan.artifact_id == "metamodel_snapshot":
        return build_metamodel_snapshot(projection)

    if plan.relative_path.endswith(".md"):
        return _build_placeholder_markdown(plan, projection, options)

    return _build_placeholder_payload(projection, plan, options)


def _build_placeholder_payload(
    projection: ProjectionModel,
    plan: AtlasBundleArtifactPlan,
    options: AtlasBundleOptions,
) -> Mapping[str, Any]:
    return {
        "artifact_id": plan.artifact_id,
        "status": "placeholder",
        "description": plan.description,
        "profile": options.profile,
        "model_name": projection.metadata.model_name,
        "model_version": projection.metadata.version,
        "bank_code": projection.metadata.bank_code,
    }


def _build_placeholder_markdown(
    plan: AtlasBundleArtifactPlan,
    projection: ProjectionModel,
    options: AtlasBundleOptions,
) -> str:
    return "\n".join(
        (
            f"# {plan.artifact_id}",
            "",
            "status: placeholder",
            f"profile: {options.profile}",
            f"model_name: {projection.metadata.model_name}",
            f"model_version: {projection.metadata.version}",
            f"bank_code: {projection.metadata.bank_code}",
            f"description: {plan.description}",
            "",
        )
    )


def _manifest_to_json(manifest: AtlasBundleManifest) -> Mapping[str, Any]:
    return {
        "schema_version": manifest.schema_version,
        "bundle_kind": manifest.bundle_kind,
        "profile": manifest.profile,
        "model_name": manifest.model_name,
        "model_version": manifest.model_version,
        "bank_code": manifest.bank_code,
        "generated_at_utc": manifest.generated_at_utc,
        "artifact_count": manifest.artifact_count,
        "artifacts": [
            {
                "artifact_id": artifact.artifact_id,
                "relative_path": artifact.relative_path,
                "description": artifact.description,
                "placeholder": artifact.placeholder,
            }
            for artifact in manifest.artifacts
        ],
    }


def _write_artifact(path: Path, payload: Any) -> None:
    if isinstance(payload, str):
        path.write_text(payload, encoding="utf-8")
        return
    _write_json(path, payload)


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
