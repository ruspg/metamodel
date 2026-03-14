"""Wave 1 relation_catalog artifact generator."""
from __future__ import annotations

from typing import Any, Dict, Mapping

from .projection_model import ProjectionModel, ProjectionRelationEntry

_RELATION_CATALOG_SCHEMA_VERSION = "wave1.relation_catalog/v1"
_REQUIRED_FIELDS = (
    "direction",
    "category",
    "source_cardinality",
    "target_cardinality",
    "has_inverse",
    "allowed_in_neighbors",
    "allowed_in_paths",
    "allowed_in_impact",
    "default_visibility",
    "path_priority",
    "impact_mode",
    "supports_qualifiers",
    "allowed_qualifiers",
    "required_qualifiers",
    "evidence_required",
    "ui_label_out",
    "ui_label_in",
    "ui_group",
    "status",
)


class RelationCatalogGenerationError(ValueError):
    """Raised when projection input cannot produce relation catalog output."""


def build_relation_catalog(projection: ProjectionModel) -> Mapping[str, Any]:
    """Build compact deterministic runtime-facing relation catalog payload."""

    _require_non_empty(projection.metadata.model_name, "metadata.model_name")
    _require_non_empty(projection.metadata.version, "metadata.version")
    _require_non_empty(projection.metadata.bank_code, "metadata.bank_code")
    _require_non_empty(projection.metadata.active_profile, "metadata.active_profile")

    active_kind_ids = {kind.id for kind in projection.entity_kinds}
    qualifier_ids = {item.id for item in projection.qualifier_references}
    qualifier_ids.update(item.id for item in projection.qualifier_definitions)

    relations = tuple(
        _relation_payload(relation, active_kind_ids=active_kind_ids, qualifier_ids=qualifier_ids)
        for relation in sorted(projection.relation_entries, key=lambda value: value.id)
        if _relation_is_active(relation, active_kind_ids)
    )

    relation_index = {item["id"]: item for item in relations}
    _validate_inverse_links(relation_index)

    return {
        "schema_version": _RELATION_CATALOG_SCHEMA_VERSION,
        "model": {
            "model_name": projection.metadata.model_name,
            "model_version": projection.metadata.version,
            "bank_code": projection.metadata.bank_code,
            "profile": projection.metadata.active_profile,
            "relation_catalog_version": projection.compatibility_hooks.relation_catalog_version,
            "relation_catalog_status": projection.compatibility_hooks.relation_catalog_status,
        },
        "counts": {
            "relation_count": len(relations),
            "qualifier_count": len(qualifier_ids),
        },
        "relations": relations,
    }


def _relation_is_active(relation: ProjectionRelationEntry, active_kind_ids: set[str]) -> bool:
    from_kind = relation.from_kind or ""
    to_kind = relation.to_kind or ""
    return from_kind in active_kind_ids and to_kind in active_kind_ids

def _relation_payload(
    relation: ProjectionRelationEntry,
    *,
    active_kind_ids: set[str],
    qualifier_ids: set[str],
) -> Mapping[str, Any]:
    _require_non_empty(relation.id, "relation.id")
    _require_non_empty(relation.from_kind, f"relations.{relation.id}.from_kind")
    _require_non_empty(relation.to_kind, f"relations.{relation.id}.to_kind")

    payload = relation.payload
    for field in _REQUIRED_FIELDS:
        if field not in payload:
            raise RelationCatalogGenerationError(f"relations.{relation.id}.{field} is required")

    allowed_qualifiers = _normalize_string_list(payload.get("allowed_qualifiers"))
    required_qualifiers = _normalize_string_list(payload.get("required_qualifiers"))

    unknown = sorted((set(allowed_qualifiers) | set(required_qualifiers)) - qualifier_ids)
    if unknown:
        raise RelationCatalogGenerationError(
            f"relations.{relation.id}.qualifiers contain unknown qualifier(s): {', '.join(unknown)}"
        )

    if not set(required_qualifiers).issubset(set(allowed_qualifiers)):
        raise RelationCatalogGenerationError(
            f"relations.{relation.id}.required_qualifiers must be subset of allowed_qualifiers"
        )

    result: Dict[str, Any] = {
        "id": relation.id,
        "from_kind": relation.from_kind,
        "to_kind": relation.to_kind,
    }

    for field in _REQUIRED_FIELDS:
        value = payload.get(field)
        if field in {"allowed_qualifiers", "required_qualifiers"}:
            value = tuple(sorted(_normalize_string_list(value)))
        result[field] = value

    inverse_relation_id = payload.get("inverse_relation_id")
    if inverse_relation_id is not None:
        _require_non_empty(str(inverse_relation_id), f"relations.{relation.id}.inverse_relation_id")
        result["inverse_relation_id"] = str(inverse_relation_id)

    if relation.applies_to_profiles:
        result["applies_to_profiles"] = tuple(sorted(str(item) for item in relation.applies_to_profiles))

    return result


def _validate_inverse_links(relation_index: Mapping[str, Mapping[str, Any]]) -> None:
    for relation_id, relation in relation_index.items():
        has_inverse = bool(relation.get("has_inverse"))
        inverse_id = relation.get("inverse_relation_id")

        if has_inverse and not inverse_id:
            raise RelationCatalogGenerationError(
                f"relations.{relation_id}.inverse_relation_id is required when has_inverse=true"
            )
        if not has_inverse and inverse_id:
            raise RelationCatalogGenerationError(
                f"relations.{relation_id}.inverse_relation_id is only allowed when has_inverse=true"
            )
        if not inverse_id:
            continue

        inverse_relation = relation_index.get(inverse_id)
        if inverse_relation is None:
            raise RelationCatalogGenerationError(
                f"relations.{relation_id}.inverse_relation_id references unknown relation '{inverse_id}'"
            )

        if not bool(inverse_relation.get("has_inverse")):
            raise RelationCatalogGenerationError(
                f"relations.{inverse_id}.has_inverse must be true because it is an inverse target"
            )

        if inverse_relation.get("inverse_relation_id") != relation_id:
            raise RelationCatalogGenerationError(
                f"relations.{inverse_id}.inverse_relation_id must point back to '{relation_id}'"
            )

        if relation.get("from_kind") != inverse_relation.get("to_kind"):
            raise RelationCatalogGenerationError(
                f"relations.{relation_id} inverse endpoint mismatch: from_kind != inverse.to_kind"
            )
        if relation.get("to_kind") != inverse_relation.get("from_kind"):
            raise RelationCatalogGenerationError(
                f"relations.{relation_id} inverse endpoint mismatch: to_kind != inverse.from_kind"
            )


def _normalize_string_list(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, (list, tuple)):
        return tuple(str(item) for item in value)
    raise RelationCatalogGenerationError(f"expected string/list for qualifier field, got {type(value).__name__}")


def _require_non_empty(value: str | None, path: str) -> None:
    if value is None or not str(value).strip():
        raise RelationCatalogGenerationError(f"projection {path} is required")
