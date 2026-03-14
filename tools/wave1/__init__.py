"""Wave 1 ontology loading utilities."""

from .lint import LintMessage, LintResult, lint_ontology
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
from .relation_catalog_validator import (
    RelationCatalogValidationError,
    ensure_valid_relation_catalog,
    validate_relation_catalog,
)
from .validation_types import ValidationMessage, ValidationResult
from .validator import OntologyValidationError, ensure_valid_ontology, validate_ontology

__all__ = [
    "AttributeDefinition",
    "EntityKind",
    "GlossaryAlias",
    "LintMessage",
    "LintResult",
    "NormalizedOntology",
    "OntologyLoadError",
    "OntologyValidationError",
    "QualifierDefinition",
    "RelationCatalog",
    "RelationCatalogRelation",
    "RelationCatalogValidationError",
    "RelationKind",
    "ValidationMessage",
    "ValidationResult",
    "ensure_valid_ontology",
    "ensure_valid_relation_catalog",
    "lint_ontology",
    "load_ontology",
    "validate_ontology",
    "validate_relation_catalog",
]
