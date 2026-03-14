"""Wave 1 type_catalog artifact generator."""
from __future__ import annotations

from typing import Any, Dict, Mapping

from .projection_model import ProjectionAttribute, ProjectionEntityKind, ProjectionModel

_TYPE_CATALOG_SCHEMA_VERSION = "wave1.type_catalog/v1"


class TypeCatalogGenerationError(ValueError):
    """Raised when projection input cannot produce type catalog output."""


def build_type_catalog(projection: ProjectionModel) -> Mapping[str, Any]:
    """Build a compact, deterministic runtime-facing type catalog payload."""

    _require_non_empty(projection.metadata.model_name, "metadata.model_name")
    _require_non_empty(projection.metadata.version, "metadata.version")
    _require_non_empty(projection.metadata.bank_code, "metadata.bank_code")
    _require_non_empty(projection.metadata.active_profile, "metadata.active_profile")

    kinds = tuple(
        _kind_payload(kind)
        for kind in sorted(projection.entity_kinds, key=lambda value: value.id)
    )
    attribute_count = sum(len(kind["attributes"]) for kind in kinds)

    return {
        "schema_version": _TYPE_CATALOG_SCHEMA_VERSION,
        "model": {
            "model_name": projection.metadata.model_name,
            "model_version": projection.metadata.version,
            "bank_code": projection.metadata.bank_code,
            "profile": projection.metadata.active_profile,
        },
        "counts": {
            "kind_count": len(kinds),
            "attribute_count": attribute_count,
        },
        "kinds": kinds,
    }


def _kind_payload(kind: ProjectionEntityKind) -> Mapping[str, Any]:
    _require_non_empty(kind.id, "entity_kind.id")

    payload: Dict[str, Any] = {
        "id": kind.id,
        "name": kind.name,
        "metamodel_level": kind.metamodel_level,
        "category": kind.category,
        "attributes": tuple(
            _attribute_payload(attribute)
            for attribute in sorted(kind.attributes, key=lambda value: value.id)
        ),
    }

    _copy_if_present(payload, "description", kind.description)
    _copy_if_present(payload, "name_ru", kind.extra.get("name_ru"))
    _copy_if_present(payload, "status", kind.extra.get("status"))
    _copy_if_present(payload, "lifecycle_status", kind.extra.get("lifecycle_status"))
    _copy_if_present(payload, "key_attribute_id", kind.extra.get("key_attribute_id"))
    _copy_if_present(payload, "default_title_attribute_id", kind.extra.get("default_title_attribute_id"))

    return payload


def _attribute_payload(attribute: ProjectionAttribute) -> Mapping[str, Any]:
    _require_non_empty(attribute.id, "attribute.id")

    payload: Dict[str, Any] = {
        "id": attribute.id,
        "name": attribute.name,
        "metamodel_level": attribute.metamodel_level,
    }

    _copy_if_present(payload, "description", attribute.description)

    runtime_meta = _extract_attribute_runtime_meta(attribute.extra)
    payload.update(runtime_meta)
    return payload


def _extract_attribute_runtime_meta(extra: Mapping[str, Any]) -> Mapping[str, Any]:
    payload: Dict[str, Any] = {}

    for key in (
        "data_type",
        "cardinality",
        "required",
        "ref_kind",
        "reference_kind_id",
        "searchable",
        "filterable",
        "display_hint",
        "ui_label",
    ):
        _copy_if_present(payload, key, extra.get(key))

    properties = extra.get("properties")
    if isinstance(properties, Mapping):
        allowed_values = properties.get("allowed_values")
        if isinstance(allowed_values, (list, tuple)):
            payload["enum_values"] = tuple(sorted(str(value) for value in allowed_values))

    return payload


def _copy_if_present(payload: Dict[str, Any], key: str, value: Any) -> None:
    if value is None:
        return
    if isinstance(value, str) and not value.strip():
        return
    payload[key] = value


def _require_non_empty(value: str | None, path: str) -> None:
    if value is None or not str(value).strip():
        raise TypeCatalogGenerationError(f"projection {path} is required")
