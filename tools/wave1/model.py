"""Normalized internal model for Wave 1 ontology loading."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, Tuple


JSONMap = Mapping[str, Any]


@dataclass(frozen=True)
class AttributeDefinition:
    id: str
    owner_kind_id: Optional[str]
    name: Optional[str]
    metamodel_level: Optional[str]
    description: Optional[str]
    extra: JSONMap


@dataclass(frozen=True)
class EntityKind:
    id: str
    name: Optional[str]
    metamodel_level: Optional[str]
    category: Optional[str]
    description: Optional[str]
    rules: Optional[str]
    attributes: Tuple[AttributeDefinition, ...]
    extra: JSONMap


@dataclass(frozen=True)
class RelationKind:
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
class QualifierDefinition:
    id: str
    name: Optional[str]
    description: Optional[str]
    extra: JSONMap


@dataclass(frozen=True)
class GlossaryAlias:
    id: str
    term: Optional[str]
    alias: Optional[str]
    language: Optional[str]
    extra: JSONMap


@dataclass(frozen=True)
class RelationCatalogRelation:
    id: str
    from_kind: Optional[str]
    to_kind: Optional[str]
    payload: JSONMap


@dataclass(frozen=True)
class RelationCatalog:
    version: Optional[str]
    status: Optional[str]
    purpose: Optional[str]
    profiles: Tuple[str, ...]
    qualifier_references: Tuple[QualifierDefinition, ...]
    relations: Tuple[RelationCatalogRelation, ...]


@dataclass(frozen=True)
class NormalizedOntology:
    meta: JSONMap
    dictionaries: JSONMap
    entity_kinds: Tuple[EntityKind, ...]
    attribute_definitions: Tuple[AttributeDefinition, ...]
    relation_kinds: Tuple[RelationKind, ...]
    qualifier_definitions: Tuple[QualifierDefinition, ...]
    glossary_aliases: Tuple[GlossaryAlias, ...]
    profiles: Tuple[str, ...]
    relation_catalog: Optional[RelationCatalog]
