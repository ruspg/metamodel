"""Wave 1 ontology validator built on top of the normalized model."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Mapping, Optional, Sequence, Tuple

from .model import NormalizedOntology, RelationCatalogRelation


_ALLOWED_DIRECTIONS = {"directed", "undirected"}
_ALLOWED_CARDINALITIES = {"one", "many"}
_ALLOWED_VISIBILITY = {"visible", "collapsed", "hidden"}
_ALLOWED_PATH_PRIORITY = {"primary", "secondary", "tertiary", "excluded"}
_ALLOWED_IMPACT_MODE = {"propagate", "explain_only", "exclude"}
_ALLOWED_STATUS = {"active", "deprecated", "experimental"}
_ALLOWED_VALUE_TYPES = {
    "string",
    "text",
    "integer",
    "number",
    "boolean",
    "enum",
    "id",
    "uri",
}
_ALLOWED_QUALIFIER_CARDINALITY = {"one", "many", "optional"}
_ALLOWED_LIFECYCLE_STATUS = {"active", "deprecated", "experimental", "draft"}


@dataclass(frozen=True)
class ValidationMessage:
    code: str
    message: str
    path: str


@dataclass(frozen=True)
class ValidationResult:
    errors: Tuple[ValidationMessage, ...]
    warnings: Tuple[ValidationMessage, ...]

    @property
    def error_count(self) -> int:
        return len(self.errors)

    @property
    def warning_count(self) -> int:
        return len(self.warnings)

    @property
    def is_valid(self) -> bool:
        return not self.errors


class OntologyValidationError(ValueError):
    """Raised when ontology fails Wave 1 validation checks."""


def validate_ontology(ontology: NormalizedOntology) -> ValidationResult:
    """Validate normalized ontology and return structured Wave 1 findings."""

    errors: List[ValidationMessage] = []
    warnings: List[ValidationMessage] = []

    _validate_core_structure(ontology, errors)
    _validate_entity_kinds(ontology, errors)
    _validate_attribute_definitions(ontology, errors)
    _validate_relation_kinds(ontology, errors)
    _validate_qualifiers(ontology, errors)
    _validate_glossary_aliases(ontology, errors, warnings)
    _validate_relation_catalog(ontology, errors, warnings)
    _validate_profile_applicability(ontology, errors)

    return ValidationResult(errors=tuple(errors), warnings=tuple(warnings))


def ensure_valid_ontology(ontology: NormalizedOntology) -> ValidationResult:
    """Validate ontology and raise a readable fatal error if it is invalid."""

    result = validate_ontology(ontology)
    if result.is_valid:
        return result

    lines = ["Wave 1 ontology validation failed:"]
    for issue in result.errors:
        lines.append(f"- [{issue.code}] {issue.path}: {issue.message}")
    raise OntologyValidationError("\n".join(lines))


def _validate_core_structure(ontology: NormalizedOntology, errors: List[ValidationMessage]) -> None:
    for key in ("model_name", "version", "bank_code"):
        value = ontology.meta.get(key)
        if value is None or (isinstance(value, str) and not value.strip()):
            errors.append(
                ValidationMessage(
                    code="missing_meta",
                    path=f"meta.{key}",
                    message="required metadata field is missing",
                )
            )

    if not ontology.entity_kinds:
        errors.append(ValidationMessage("missing_section", "entity_kinds section is empty", "entity_kinds"))
    if not ontology.relation_kinds:
        errors.append(ValidationMessage("missing_section", "relation_kinds section is empty", "relation_kinds"))


def _validate_entity_kinds(ontology: NormalizedOntology, errors: List[ValidationMessage]) -> None:
    entity_ids = [entity.id for entity in ontology.entity_kinds]
    _append_duplicate_errors(entity_ids, "entity_kinds", errors)

    attribute_ids = {attribute.id for attribute in ontology.attribute_definitions}
    for entity in ontology.entity_kinds:
        if entity.name is not None and not entity.name.strip():
            errors.append(ValidationMessage("invalid_entity", "name cannot be blank", f"entity_kinds.{entity.id}.name"))

        for key in ("key_attribute_id", "default_title_attribute_id"):
            attr_id = entity.extra.get(key)
            if attr_id is None:
                continue
            if not isinstance(attr_id, str) or attr_id not in attribute_ids:
                errors.append(
                    ValidationMessage(
                        code="missing_reference",
                        path=f"entity_kinds.{entity.id}.{key}",
                        message=f"attribute reference '{attr_id}' does not exist",
                    )
                )

        for key in ("status", "lifecycle_status"):
            status_value = entity.extra.get(key)
            if status_value is None:
                continue
            if not isinstance(status_value, str) or status_value not in _ALLOWED_LIFECYCLE_STATUS:
                errors.append(
                    ValidationMessage(
                        code="invalid_enum",
                        path=f"entity_kinds.{entity.id}.{key}",
                        message=f"unsupported lifecycle/status value '{status_value}'",
                    )
                )


def _validate_attribute_definitions(ontology: NormalizedOntology, errors: List[ValidationMessage]) -> None:
    attribute_ids = [attribute.id for attribute in ontology.attribute_definitions]
    _append_duplicate_errors(attribute_ids, "attribute_definitions", errors)

    entity_ids = {entity.id for entity in ontology.entity_kinds}
    for attribute in ontology.attribute_definitions:
        if attribute.owner_kind_id is not None and attribute.owner_kind_id not in entity_ids:
            errors.append(
                ValidationMessage(
                    code="missing_reference",
                    path=f"attribute_definitions.{attribute.id}.owner_kind_id",
                    message=f"owner kind '{attribute.owner_kind_id}' does not exist",
                )
            )

        datatype = _first_present(attribute.extra, "datatype", "data_type", "value_type", "type")
        if datatype is not None and (not isinstance(datatype, str) or datatype not in _ALLOWED_VALUE_TYPES):
            errors.append(
                ValidationMessage(
                    code="invalid_enum",
                    path=f"attribute_definitions.{attribute.id}.datatype",
                    message=f"unsupported datatype '{datatype}'",
                )
            )

        cardinality = _first_present(attribute.extra, "cardinality", "value_cardinality")
        if cardinality is not None and (
            not isinstance(cardinality, str) or cardinality not in _ALLOWED_QUALIFIER_CARDINALITY
        ):
            errors.append(
                ValidationMessage(
                    code="invalid_enum",
                    path=f"attribute_definitions.{attribute.id}.cardinality",
                    message=f"unsupported cardinality '{cardinality}'",
                )
            )

        allowed_values = _first_present(attribute.extra, "allowed_values", "enum_values")
        if allowed_values is not None:
            if not isinstance(allowed_values, list) or not allowed_values:
                errors.append(
                    ValidationMessage(
                        code="invalid_attribute",
                        path=f"attribute_definitions.{attribute.id}.allowed_values",
                        message="enum values must be a non-empty list",
                    )
                )
            elif any(not isinstance(item, str) or not item.strip() for item in allowed_values):
                errors.append(
                    ValidationMessage(
                        code="invalid_attribute",
                        path=f"attribute_definitions.{attribute.id}.allowed_values",
                        message="enum values must be non-empty strings",
                    )
                )

        ref_kind = _first_present(attribute.extra, "ref_kind", "reference_kind_id")
        if ref_kind is not None and (not isinstance(ref_kind, str) or ref_kind not in entity_ids):
            errors.append(
                ValidationMessage(
                    code="missing_reference",
                    path=f"attribute_definitions.{attribute.id}.ref_kind",
                    message=f"reference target kind '{ref_kind}' does not exist",
                )
            )


def _validate_relation_kinds(ontology: NormalizedOntology, errors: List[ValidationMessage]) -> None:
    relation_ids = [relation.id for relation in ontology.relation_kinds]
    _append_duplicate_errors(relation_ids, "relation_kinds", errors)

    entity_ids = {entity.id for entity in ontology.entity_kinds}
    for relation in ontology.relation_kinds:
        if relation.from_kind is None or relation.from_kind not in entity_ids:
            errors.append(
                ValidationMessage(
                    code="missing_reference",
                    path=f"relation_kinds.{relation.id}.from_kind",
                    message=f"from_kind '{relation.from_kind}' does not resolve to an entity kind",
                )
            )
        if relation.to_kind is None or relation.to_kind not in entity_ids:
            errors.append(
                ValidationMessage(
                    code="missing_reference",
                    path=f"relation_kinds.{relation.id}.to_kind",
                    message=f"to_kind '{relation.to_kind}' does not resolve to an entity kind",
                )
            )
        if relation.direction is not None and relation.direction not in _ALLOWED_DIRECTIONS:
            errors.append(
                ValidationMessage(
                    code="invalid_enum",
                    path=f"relation_kinds.{relation.id}.direction",
                    message=f"unsupported direction '{relation.direction}'",
                )
            )


def _validate_qualifiers(ontology: NormalizedOntology, errors: List[ValidationMessage]) -> None:
    qualifier_ids = [qualifier.id for qualifier in ontology.qualifier_definitions]
    if ontology.relation_catalog is not None:
        qualifier_ids.extend(qualifier.id for qualifier in ontology.relation_catalog.qualifier_references)
    _append_duplicate_errors(qualifier_ids, "qualifier_definitions", errors)

    for qualifier in ontology.qualifier_definitions:
        value_type = _first_present(qualifier.extra, "value_type", "allowed_value_type")
        if value_type is not None and (not isinstance(value_type, str) or value_type not in _ALLOWED_VALUE_TYPES):
            errors.append(
                ValidationMessage(
                    code="invalid_enum",
                    path=f"qualifier_definitions.{qualifier.id}.value_type",
                    message=f"unsupported qualifier value_type '{value_type}'",
                )
            )
        cardinality = qualifier.extra.get("cardinality")
        if cardinality is not None and (
            not isinstance(cardinality, str) or cardinality not in _ALLOWED_QUALIFIER_CARDINALITY
        ):
            errors.append(
                ValidationMessage(
                    code="invalid_enum",
                    path=f"qualifier_definitions.{qualifier.id}.cardinality",
                    message=f"unsupported qualifier cardinality '{cardinality}'",
                )
            )


def _validate_glossary_aliases(
    ontology: NormalizedOntology,
    errors: List[ValidationMessage],
    warnings: List[ValidationMessage],
) -> None:
    alias_ids = [alias.id for alias in ontology.glossary_aliases]
    _append_duplicate_errors(alias_ids, "glossary_aliases", errors)

    entity_ids = {entity.id for entity in ontology.entity_kinds}
    seen_aliases = set()
    for alias in ontology.glossary_aliases:
        if alias.alias and alias.alias in entity_ids:
            errors.append(
                ValidationMessage(
                    code="alias_collision",
                    path=f"glossary_aliases.{alias.id}.alias",
                    message=f"alias '{alias.alias}' collides with an entity kind id",
                )
            )
        key = ((alias.language or "").strip().lower(), (alias.alias or "").strip().lower())
        if key in seen_aliases and key[1]:
            warnings.append(
                ValidationMessage(
                    code="duplicate_alias",
                    path=f"glossary_aliases.{alias.id}",
                    message=f"duplicate alias '{alias.alias}' for language '{alias.language}'",
                )
            )
        seen_aliases.add(key)


def _validate_relation_catalog(
    ontology: NormalizedOntology,
    errors: List[ValidationMessage],
    warnings: List[ValidationMessage],
) -> None:
    catalog = ontology.relation_catalog
    if catalog is None:
        return

    _append_duplicate_errors([relation.id for relation in catalog.relations], "relation_catalog.relations", errors)
    entity_ids = {entity.id for entity in ontology.entity_kinds}
    qualifier_ids = {qualifier.id for qualifier in ontology.qualifier_definitions}
    qualifier_ids.update(qualifier.id for qualifier in catalog.qualifier_references)

    relations_by_id = {relation.id: relation for relation in catalog.relations}
    for relation in catalog.relations:
        payload = relation.payload
        _validate_catalog_endpoint_reference(
            relation=relation,
            field_name="from_kind",
            value=relation.from_kind,
            entity_ids=entity_ids,
            warnings=warnings,
        )
        _validate_catalog_endpoint_reference(
            relation=relation,
            field_name="to_kind",
            value=relation.to_kind,
            entity_ids=entity_ids,
            warnings=warnings,
        )

        _validate_enum_field(payload, relation.id, "direction", _ALLOWED_DIRECTIONS, errors)
        _validate_enum_field(payload, relation.id, "source_cardinality", _ALLOWED_CARDINALITIES, errors)
        _validate_enum_field(payload, relation.id, "target_cardinality", _ALLOWED_CARDINALITIES, errors)
        _validate_enum_field(payload, relation.id, "default_visibility", _ALLOWED_VISIBILITY, errors)
        _validate_enum_field(payload, relation.id, "path_priority", _ALLOWED_PATH_PRIORITY, errors)
        _validate_enum_field(payload, relation.id, "impact_mode", _ALLOWED_IMPACT_MODE, errors)
        _validate_enum_field(payload, relation.id, "status", _ALLOWED_STATUS, errors)

        has_inverse = payload.get("has_inverse")
        inverse_relation_id = payload.get("inverse_relation_id")
        if has_inverse is True:
            if not isinstance(inverse_relation_id, str) or inverse_relation_id not in relations_by_id:
                errors.append(
                    ValidationMessage(
                        code="missing_reference",
                        path=f"relation_catalog.relations.{relation.id}.inverse_relation_id",
                        message="has_inverse=true requires existing inverse_relation_id",
                    )
                )
            else:
                inverse_relation = relations_by_id[inverse_relation_id]
                inverse_payload = inverse_relation.payload
                if inverse_payload.get("inverse_relation_id") != relation.id:
                    errors.append(
                        ValidationMessage(
                            code="invalid_inverse",
                            path=f"relation_catalog.relations.{relation.id}.inverse_relation_id",
                            message="inverse relation must point back to source relation",
                        )
                    )
                if relation.from_kind != inverse_relation.to_kind or relation.to_kind != inverse_relation.from_kind:
                    errors.append(
                        ValidationMessage(
                            code="invalid_inverse",
                            path=f"relation_catalog.relations.{relation.id}",
                            message="inverse relation endpoints must be symmetric",
                        )
                    )
        elif inverse_relation_id:
            errors.append(
                ValidationMessage(
                    code="invalid_inverse",
                    path=f"relation_catalog.relations.{relation.id}.inverse_relation_id",
                    message="inverse_relation_id is only allowed when has_inverse=true",
                )
            )

        supports_qualifiers = payload.get("supports_qualifiers")
        allowed_qualifiers = _as_str_list(payload.get("allowed_qualifiers"))
        required_qualifiers = _as_str_list(payload.get("required_qualifiers"))
        if supports_qualifiers is False and (allowed_qualifiers or required_qualifiers):
            errors.append(
                ValidationMessage(
                    code="invalid_qualifier_policy",
                    path=f"relation_catalog.relations.{relation.id}",
                    message="relation with supports_qualifiers=false cannot define allowed/required qualifiers",
                )
            )

        missing_qualifiers = sorted(
            qualifier_id
            for qualifier_id in (*allowed_qualifiers, *required_qualifiers)
            if qualifier_id not in qualifier_ids
        )
        for qualifier_id in missing_qualifiers:
            errors.append(
                ValidationMessage(
                    code="missing_reference",
                    path=f"relation_catalog.relations.{relation.id}.qualifiers",
                    message=f"qualifier '{qualifier_id}' is not declared",
                )
            )

        if set(required_qualifiers) - set(allowed_qualifiers):
            errors.append(
                ValidationMessage(
                    code="invalid_qualifier_policy",
                    path=f"relation_catalog.relations.{relation.id}.required_qualifiers",
                    message="required_qualifiers must be subset of allowed_qualifiers",
                )
            )

        path_priority = payload.get("path_priority")
        allowed_in_paths = payload.get("allowed_in_paths")
        if allowed_in_paths is False and path_priority not in {None, "excluded"}:
            errors.append(
                ValidationMessage(
                    code="invalid_combination",
                    path=f"relation_catalog.relations.{relation.id}",
                    message="allowed_in_paths=false requires path_priority=excluded",
                )
            )

        impact_mode = payload.get("impact_mode")
        allowed_in_impact = payload.get("allowed_in_impact")
        if allowed_in_impact is False and impact_mode not in {None, "exclude"}:
            errors.append(
                ValidationMessage(
                    code="invalid_combination",
                    path=f"relation_catalog.relations.{relation.id}",
                    message="allowed_in_impact=false requires impact_mode=exclude",
                )
            )
        if impact_mode == "propagate" and allowed_in_impact is False:
            errors.append(
                ValidationMessage(
                    code="invalid_combination",
                    path=f"relation_catalog.relations.{relation.id}",
                    message="impact_mode=propagate contradicts allowed_in_impact=false",
                )
            )




def _validate_catalog_endpoint_reference(
    *,
    relation: RelationCatalogRelation,
    field_name: str,
    value: Optional[str],
    entity_ids: set[str],
    warnings: List[ValidationMessage],
) -> None:
    if value is None:
        warnings.append(
            ValidationMessage(
                code="missing_reference",
                path=f"relation_catalog.relations.{relation.id}.{field_name}",
                message=f"{field_name} is empty",
            )
        )
        return
    if value not in entity_ids:
        warnings.append(
            ValidationMessage(
                code="external_reference",
                path=f"relation_catalog.relations.{relation.id}.{field_name}",
                message=f"{field_name} '{value}' is not in current ontology entity_kinds (accepted for profile-scoped catalog inputs)",
            )
        )

def _validate_profile_applicability(ontology: NormalizedOntology, errors: List[ValidationMessage]) -> None:
    declared_profiles = set(ontology.profiles)
    if ontology.relation_catalog is not None:
        declared_profiles.update(ontology.relation_catalog.profiles)

    if ontology.relation_catalog is None:
        return

    for relation in ontology.relation_catalog.relations:
        applies_to_profiles = _as_str_list(relation.payload.get("applies_to_profiles"))
        for profile in applies_to_profiles:
            if profile not in declared_profiles:
                errors.append(
                    ValidationMessage(
                        code="missing_reference",
                        path=f"relation_catalog.relations.{relation.id}.applies_to_profiles",
                        message=f"profile '{profile}' is not declared in ontology/profiles",
                    )
                )

    if any("atlas_mvp" in _as_str_list(r.payload.get("applies_to_profiles")) for r in ontology.relation_catalog.relations):
        if "atlas_mvp" not in declared_profiles:
            errors.append(
                ValidationMessage(
                    code="missing_reference",
                    path="profiles",
                    message="atlas_mvp is referenced but not declared in profiles",
                )
            )


def _append_duplicate_errors(ids: Sequence[str], namespace: str, errors: List[ValidationMessage]) -> None:
    seen = set()
    duplicates = set()
    for item_id in ids:
        if item_id in seen:
            duplicates.add(item_id)
        seen.add(item_id)
    for duplicate in sorted(duplicates):
        errors.append(
            ValidationMessage(
                code="duplicate_id",
                path=namespace,
                message=f"duplicate id '{duplicate}'",
            )
        )


def _validate_enum_field(
    payload: Mapping[str, object],
    relation_id: str,
    field_name: str,
    allowed_values: Iterable[str],
    errors: List[ValidationMessage],
) -> None:
    value = payload.get(field_name)
    if value is None:
        return
    if not isinstance(value, str) or value not in set(allowed_values):
        errors.append(
            ValidationMessage(
                code="invalid_enum",
                path=f"relation_catalog.relations.{relation_id}.{field_name}",
                message=f"unsupported value '{value}'",
            )
        )


def _as_str_list(value: object) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def _first_present(mapping: Mapping[str, object], *keys: str) -> Optional[object]:
    for key in keys:
        value = mapping.get(key)
        if value is not None:
            return value
    properties = mapping.get("properties")
    if isinstance(properties, Mapping):
        for key in keys:
            value = properties.get(key)
            if value is not None:
                return value
    return None
