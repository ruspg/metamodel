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
from .validator import (
    OntologyValidationError,
    ValidationMessage,
    ValidationResult,
    ensure_valid_ontology,
    validate_ontology,
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
    "OntologyValidationError",
    "ValidationMessage",
    "ValidationResult",
    "ensure_valid_ontology",
    "load_ontology",
    "validate_ontology",
]
