"""Wave 1 atlas projection bundle manifest/result structures."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class AtlasBundleArtifactPlan:
    artifact_id: str
    relative_path: str
    description: str
    placeholder: bool = True


@dataclass(frozen=True)
class AtlasBundleManifest:
    schema_version: str
    bundle_kind: str
    profile: str
    model_name: str
    model_version: str
    bank_code: str
    generated_at_utc: str
    artifact_count: int
    artifacts: Tuple[AtlasBundleArtifactPlan, ...]


@dataclass(frozen=True)
class AtlasBundleResult:
    bundle_root: str
    manifest_path: str
    artifacts_root: str
    artifact_paths: Tuple[str, ...]
    manifest: AtlasBundleManifest


@dataclass(frozen=True)
class AtlasBundleOptions:
    profile: str = "atlas_mvp"
    bundle_name: Optional[str] = None
    generated_at_utc: str = "1970-01-01T00:00:00Z"
