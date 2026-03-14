"""Wave 1 ontology loading utilities."""

from .loader import OntologyLoadError, load_ontology
from .model import (
    AttributeDefinition,
    EntityKind,
    GlossaryAlias,
    NormalizedOntology,
    QualifierDefinition,
    RelationCatalog,
    RelationCatalogRelation,
    RelationKind,
)

__all__ = [
    "AttributeDefinition",
    "EntityKind",
    "GlossaryAlias",
    "NormalizedOntology",
    "OntologyLoadError",
    "QualifierDefinition",
    "RelationCatalog",
    "RelationCatalogRelation",
    "RelationKind",
    "load_ontology",
]
