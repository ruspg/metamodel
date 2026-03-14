"""Wave 1 metamodel_snapshot artifact generator."""
from __future__ import annotations

from typing import Any, Dict, Mapping, Tuple

from .projection_model import ProjectionModel

_SNAPSHOT_SCHEMA_VERSION = "wave1.metamodel_snapshot/v1"


class MetamodelSnapshotGenerationError(ValueError):
    """Raised when projection input cannot produce metamodel snapshot output."""


def build_metamodel_snapshot(projection: ProjectionModel) -> Mapping[str, Any]:
    """Build a compact, deterministic runtime-facing metamodel snapshot payload."""

    _require_non_empty(projection.metadata.model_name, "metadata.model_name")
    _require_non_empty(projection.metadata.version, "metadata.version")
    _require_non_empty(projection.metadata.bank_code, "metadata.bank_code")
    _require_non_empty(projection.metadata.active_profile, "metadata.active_profile")

    entity_kinds = tuple(_entity_kind_payload(item) for item in projection.entity_kinds)
    relation_kinds = tuple(_relation_kind_payload(item) for item in projection.relation_kinds)
    relations = tuple(_relation_entry_payload(item) for item in projection.relation_entries)
    qualifier_refs = tuple(_qualifier_payload(item) for item in projection.qualifier_references)

    return {
        "schema_version": _SNAPSHOT_SCHEMA_VERSION,
        "model": {
            "model_name": projection.metadata.model_name,
            "model_version": projection.metadata.version,
            "bank_code": projection.metadata.bank_code,
            "profile": projection.metadata.active_profile,
            "source_profiles": tuple(sorted(projection.metadata.source_profiles)),
        },
        "catalog_metadata": {
            "relation_catalog_version": projection.compatibility_hooks.relation_catalog_version,
            "relation_catalog_status": projection.compatibility_hooks.relation_catalog_status,
        },
        "counts": {
            "entity_kind_count": len(entity_kinds),
            "relation_kind_count": len(relation_kinds),
            "relation_count": len(relations),
            "qualifier_count": len(qualifier_refs),
        },
        "entity_kinds": entity_kinds,
        "relation_kinds": relation_kinds,
        "relations": relations,
        "qualifiers": qualifier_refs,
    }


def _entity_kind_payload(entity: Any) -> Mapping[str, Any]:
    return {
        "id": entity.id,
        "name": entity.name,
        "metamodel_level": entity.metamodel_level,
        "category": entity.category,
        "attributes": tuple(
            {
                "id": attribute.id,
                "name": attribute.name,
                "metamodel_level": attribute.metamodel_level,
            }
            for attribute in entity.attributes
        ),
    }


def _relation_kind_payload(relation_kind: Any) -> Mapping[str, Any]:
    return {
        "id": relation_kind.id,
        "name": relation_kind.name,
        "from_kind": relation_kind.from_kind,
        "to_kind": relation_kind.to_kind,
        "category": relation_kind.category,
        "direction": relation_kind.direction,
    }


def _relation_entry_payload(relation: Any) -> Mapping[str, Any]:
    return {
        "id": relation.id,
        "from_kind": relation.from_kind,
        "to_kind": relation.to_kind,
        "applies_to_profiles": relation.applies_to_profiles,
    }


def _qualifier_payload(qualifier: Any) -> Mapping[str, Any]:
    return {
        "id": qualifier.id,
        "name": qualifier.name,
    }


def _require_non_empty(value: str, path: str) -> None:
    if not value or not value.strip():
        raise MetamodelSnapshotGenerationError(f"projection {path} is required")
