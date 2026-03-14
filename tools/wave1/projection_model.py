"""Generator-oriented projection model for Wave 1 bundle inputs."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, Tuple


JSONMap = Mapping[str, Any]


@dataclass(frozen=True)
class ProjectionMetadata:
    model_name: str
    version: str
    bank_code: str
    source_profiles: Tuple[str, ...]
    active_profile: str
    meta: JSONMap


@dataclass(frozen=True)
class ProjectionAttribute:
    id: str
    owner_kind_id: str
    name: Optional[str]
    metamodel_level: Optional[str]
    description: Optional[str]
    extra: JSONMap


@dataclass(frozen=True)
class ProjectionEntityKind:
    id: str
    name: Optional[str]
    metamodel_level: Optional[str]
    category: Optional[str]
    description: Optional[str]
    rules: Optional[str]
    attributes: Tuple[ProjectionAttribute, ...]
    extra: JSONMap


@dataclass(frozen=True)
class ProjectionRelationKind:
    id: str
    name: Optional[str]
    from_kind: Optional[str]
    to_kind: Optional[str]
    category: Optional[str]
    direction: Optional[str]
    metamodel_level: Optional[str]
    description: Optional[str]
    extra: JSONMap


@dataclass(frozen=True)
class ProjectionRelationEntry:
    id: str
    from_kind: Optional[str]
    to_kind: Optional[str]
    applies_to_profiles: Tuple[str, ...]
    payload: JSONMap


@dataclass(frozen=True)
class ProjectionQualifierRef:
    id: str
    name: Optional[str]
    description: Optional[str]
    extra: JSONMap


@dataclass(frozen=True)
class ProjectionAlias:
    id: str
    term: Optional[str]
    alias: Optional[str]
    language: Optional[str]
    extra: JSONMap


@dataclass(frozen=True)
class ProjectionCompatibilityHooks:
    relation_catalog_version: Optional[str]
    relation_catalog_status: Optional[str]
    relation_catalog_purpose: Optional[str]


@dataclass(frozen=True)
class ProjectionModel:
    metadata: ProjectionMetadata
    entity_kinds: Tuple[ProjectionEntityKind, ...]
    relation_kinds: Tuple[ProjectionRelationKind, ...]
    relation_entries: Tuple[ProjectionRelationEntry, ...]
    qualifier_references: Tuple[ProjectionQualifierRef, ...]
    qualifier_definitions: Tuple[ProjectionQualifierRef, ...]
    aliases: Tuple[ProjectionAlias, ...]
    compatibility_hooks: ProjectionCompatibilityHooks
