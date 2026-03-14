"""Wave 1 ontology loading utilities."""

from .atlas_bundle_generator import AtlasBundleGenerationError, generate_atlas_bundle
from .atlas_bundle_model import (
    AtlasBundleArtifactPlan,
    AtlasBundleManifest,
    AtlasBundleOptions,
    AtlasBundleResult,
)
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
from .projection_builder import ProjectionBuildError, build_projection_model
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
    "ProjectionAlias",
    "ProjectionAttribute",
    "ProjectionBuildError",
    "ProjectionCompatibilityHooks",
    "ProjectionEntityKind",
    "ProjectionMetadata",
    "ProjectionModel",
    "ProjectionQualifierRef",
    "ProjectionRelationEntry",
    "ProjectionRelationKind",
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
    "build_projection_model",
    "AtlasBundleArtifactPlan",
    "AtlasBundleGenerationError",
    "AtlasBundleManifest",
    "AtlasBundleOptions",
    "AtlasBundleResult",
    "generate_atlas_bundle",
]
