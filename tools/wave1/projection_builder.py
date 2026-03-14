"""Wave 1 projection builder for generator-ready normalized model output."""
from __future__ import annotations

from typing import Any, Mapping, Tuple

from .model import (
    AttributeDefinition,
    EntityKind,
    GlossaryAlias,
    NormalizedOntology,
    QualifierDefinition,
    RelationCatalogRelation,
    RelationKind,
)
from .projection_model import (
    ProjectionAlias,
    ProjectionAttribute,
    ProjectionCompatibilityHooks,
    ProjectionEntityKind,
    ProjectionMetadata,
    ProjectionModel,
    ProjectionQualifierRef,
    ProjectionRelationEntry,
    ProjectionRelationKind,
)


class ProjectionBuildError(ValueError):
    """Raised when a validated ontology is unexpectedly missing required sections."""


def build_projection_model(
    ontology: NormalizedOntology,
    *,
    profile: str = "atlas_mvp",
) -> ProjectionModel:
    """Build deterministic, profile-aware projection model from validated ontology."""

    _require_meta_key(ontology.meta, "model_name")
    _require_meta_key(ontology.meta, "version")
    _require_meta_key(ontology.meta, "bank_code")

    if not ontology.entity_kinds:
        raise ProjectionBuildError("normalized ontology must include at least one entity kind")
    if not ontology.relation_kinds:
        raise ProjectionBuildError("normalized ontology must include at least one relation kind")
    if ontology.relation_catalog is None:
        raise ProjectionBuildError("normalized ontology must include relation_catalog for projection")

    source_profiles = _resolve_source_profiles(ontology, profile)

    projected_entities = tuple(
        _build_entity_kind(entity, profile=profile)
        for entity in ontology.entity_kinds
        if _includes_for_profile(entity.extra, profile)
    )

    projected_relations = tuple(
        _build_relation_kind(relation)
        for relation in ontology.relation_kinds
        if _includes_for_profile(relation.extra, profile)
    )

    projected_relation_entries = tuple(
        _build_relation_entry(relation)
        for relation in ontology.relation_catalog.relations
        if _includes_for_profile(relation.payload, profile)
    )

    projected_aliases = tuple(
        _build_alias(alias)
        for alias in ontology.glossary_aliases
        if _includes_for_profile(alias.extra, profile)
    )

    projected_qualifier_refs = tuple(
        _build_qualifier_ref(qualifier)
        for qualifier in ontology.relation_catalog.qualifier_references
        if _includes_for_profile(qualifier.extra, profile)
    )

    projected_qualifier_defs = tuple(
        _build_qualifier_ref(qualifier)
        for qualifier in ontology.qualifier_definitions
        if _includes_for_profile(qualifier.extra, profile)
    )

    return ProjectionModel(
        metadata=ProjectionMetadata(
            model_name=str(ontology.meta["model_name"]),
            version=str(ontology.meta["version"]),
            bank_code=str(ontology.meta["bank_code"]),
            source_profiles=source_profiles,
            active_profile=profile,
            meta=ontology.meta,
        ),
        entity_kinds=projected_entities,
        relation_kinds=projected_relations,
        relation_entries=projected_relation_entries,
        qualifier_references=projected_qualifier_refs,
        qualifier_definitions=projected_qualifier_defs,
        aliases=projected_aliases,
        compatibility_hooks=ProjectionCompatibilityHooks(
            relation_catalog_version=ontology.relation_catalog.version,
            relation_catalog_status=ontology.relation_catalog.status,
            relation_catalog_purpose=ontology.relation_catalog.purpose,
        ),
    )


def _resolve_source_profiles(ontology: NormalizedOntology, profile: str) -> Tuple[str, ...]:
    merged = set(ontology.profiles)
    if ontology.relation_catalog is not None:
        merged.update(ontology.relation_catalog.profiles)
    if profile not in merged:
        merged.add(profile)
    return tuple(sorted(merged))


def _require_meta_key(meta: Mapping[str, Any], key: str) -> None:
    value = meta.get(key)
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ProjectionBuildError(f"normalized ontology is missing required metadata key: {key}")


def _build_entity_kind(entity: EntityKind, *, profile: str) -> ProjectionEntityKind:
    attributes = tuple(
        _build_attribute(attribute)
        for attribute in entity.attributes
        if _includes_for_profile(attribute.extra, profile)
    )
    return ProjectionEntityKind(
        id=entity.id,
        name=entity.name,
        metamodel_level=entity.metamodel_level,
        category=entity.category,
        description=entity.description,
        rules=entity.rules,
        attributes=attributes,
        extra=entity.extra,
    )


def _build_attribute(attribute: AttributeDefinition) -> ProjectionAttribute:
    if not attribute.owner_kind_id:
        raise ProjectionBuildError(
            f"attribute '{attribute.id}' is missing owner_kind_id in entity projection path"
        )
    return ProjectionAttribute(
        id=attribute.id,
        owner_kind_id=attribute.owner_kind_id,
        name=attribute.name,
        metamodel_level=attribute.metamodel_level,
        description=attribute.description,
        extra=attribute.extra,
    )


def _build_relation_kind(relation: RelationKind) -> ProjectionRelationKind:
    return ProjectionRelationKind(
        id=relation.id,
        name=relation.name,
        from_kind=relation.from_kind,
        to_kind=relation.to_kind,
        category=relation.category,
        direction=relation.direction,
        metamodel_level=relation.metamodel_level,
        description=relation.description,
        extra=relation.extra,
    )


def _build_relation_entry(relation: RelationCatalogRelation) -> ProjectionRelationEntry:
    profiles = _normalize_profiles(relation.payload.get("applies_to_profiles"))
    return ProjectionRelationEntry(
        id=relation.id,
        from_kind=relation.from_kind,
        to_kind=relation.to_kind,
        applies_to_profiles=profiles,
        payload=relation.payload,
    )


def _build_qualifier_ref(qualifier: QualifierDefinition) -> ProjectionQualifierRef:
    return ProjectionQualifierRef(
        id=qualifier.id,
        name=qualifier.name,
        description=qualifier.description,
        extra=qualifier.extra,
    )


def _build_alias(alias: GlossaryAlias) -> ProjectionAlias:
    return ProjectionAlias(
        id=alias.id,
        term=alias.term,
        alias=alias.alias,
        language=alias.language,
        extra=alias.extra,
    )


def _includes_for_profile(payload: Mapping[str, Any], profile: str) -> bool:
    applies = payload.get("applies_to_profiles")
    if applies is None:
        return True
    profiles = _normalize_profiles(applies)
    if not profiles:
        return True
    return profile in profiles


def _normalize_profiles(value: Any) -> Tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, (list, tuple)):
        return tuple(sorted(str(item) for item in value))
    raise ProjectionBuildError(f"applies_to_profiles must be a string or list, got {type(value).__name__}")
