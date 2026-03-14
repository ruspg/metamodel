"""Wave 1 ontology loader that normalizes legacy/canonical authoring YAML."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import yaml

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


class OntologyLoadError(ValueError):
    """Raised when ontology input is structurally invalid."""


def load_ontology(
    ontology_path: Path | str,
    *,
    relation_catalog_path: Path | str | None = None,
) -> NormalizedOntology:
    """Load and normalize a Wave 1 ontology YAML file.

    This function performs structural checks and deterministic normalization only.
    Semantic validation and linting are intentionally out of scope.
    """

    data = _load_yaml_mapping(Path(ontology_path), context="ontology")
    _require_sections(data, required=("meta", "entity_kinds", "relation_kinds"))

    entity_kinds = _normalize_entity_kinds(data["entity_kinds"])
    relation_kinds = _normalize_relation_kinds(data["relation_kinds"])

    top_level_attributes = _normalize_attribute_definitions(
        data.get("attribute_definitions", []), owner_kind_id=None
    )
    nested_attributes = tuple(
        attribute
        for entity in entity_kinds
        for attribute in entity.attributes
    )

    relation_catalog = None
    if relation_catalog_path is not None:
        relation_catalog = _load_relation_catalog(Path(relation_catalog_path))

    return NormalizedOntology(
        meta=_sorted_mapping(_expect_mapping(data["meta"], "meta")),
        dictionaries=_normalize_dictionaries(data.get("dictionaries", {})),
        entity_kinds=entity_kinds,
        attribute_definitions=tuple(
            sorted(
                (*top_level_attributes, *nested_attributes),
                key=lambda item: (item.id, item.owner_kind_id or ""),
            )
        ),
        relation_kinds=relation_kinds,
        qualifier_definitions=_normalize_qualifier_definitions(
            data.get("qualifier_definitions", [])
        ),
        glossary_aliases=_normalize_glossary_aliases(data),
        profiles=tuple(sorted(_normalize_profiles(data.get("profiles", [])))),
        relation_catalog=relation_catalog,
    )


def _load_relation_catalog(path: Path) -> RelationCatalog:
    data = _load_yaml_mapping(path, context="relation catalog")

    references = _normalize_qualifier_definitions(data.get("qualifier_references", []))
    relation_catalog_data = data.get("relation_catalog", {})
    relation_catalog_mapping = _expect_mapping(
        relation_catalog_data,
        "relation_catalog",
    )
    relations = relation_catalog_mapping.get("relations", [])

    return RelationCatalog(
        version=_optional_str(data.get("version")),
        status=_optional_str(data.get("status")),
        purpose=_optional_str(data.get("purpose")),
        profiles=tuple(sorted(_normalize_profiles(data.get("profiles", [])))),
        qualifier_references=references,
        relations=_normalize_relation_catalog_relations(relations),
    )


def _normalize_entity_kinds(items: Any) -> Tuple[EntityKind, ...]:
    normalized: List[EntityKind] = []
    for index, raw in enumerate(_expect_sequence(items, "entity_kinds")):
        mapping = _expect_mapping(raw, f"entity_kinds[{index}]")
        entity_id = _required_str(mapping, "id", f"entity_kinds[{index}]")
        attributes = _normalize_attribute_definitions(
            mapping.get("attributes", []), owner_kind_id=entity_id
        )
        normalized.append(
            EntityKind(
                id=entity_id,
                name=_optional_str(mapping.get("name")),
                metamodel_level=_optional_str(mapping.get("metamodel_level")),
                category=_optional_str(mapping.get("category")),
                description=_optional_str(mapping.get("description")),
                rules=_optional_str(mapping.get("rules")),
                attributes=attributes,
                extra=_sorted_mapping(
                    {
                        key: value
                        for key, value in mapping.items()
                        if key
                        not in {
                            "id",
                            "name",
                            "metamodel_level",
                            "category",
                            "description",
                            "rules",
                            "attributes",
                        }
                    }
                ),
            )
        )
    return tuple(sorted(normalized, key=lambda item: item.id))


def _normalize_attribute_definitions(
    items: Any,
    *,
    owner_kind_id: Optional[str],
) -> Tuple[AttributeDefinition, ...]:
    normalized: List[AttributeDefinition] = []
    for index, raw in enumerate(_expect_sequence(items, "attribute definitions")):
        mapping = _expect_mapping(raw, f"attribute_definitions[{index}]")
        normalized.append(
            AttributeDefinition(
                id=_required_str(mapping, "id", f"attribute_definitions[{index}]"),
                owner_kind_id=owner_kind_id,
                name=_optional_str(mapping.get("name")),
                metamodel_level=_optional_str(mapping.get("metamodel_level")),
                description=_optional_str(mapping.get("description")),
                extra=_sorted_mapping(
                    {
                        key: value
                        for key, value in mapping.items()
                        if key not in {"id", "name", "metamodel_level", "description"}
                    }
                ),
            )
        )
    return tuple(sorted(normalized, key=lambda item: (item.id, item.owner_kind_id or "")))


def _normalize_relation_kinds(items: Any) -> Tuple[RelationKind, ...]:
    normalized: List[RelationKind] = []
    for index, raw in enumerate(_expect_sequence(items, "relation_kinds")):
        mapping = _expect_mapping(raw, f"relation_kinds[{index}]")
        normalized.append(
            RelationKind(
                id=_required_str(mapping, "id", f"relation_kinds[{index}]"),
                name=_optional_str(mapping.get("name")),
                from_kind=_optional_str(mapping.get("from_kind")),
                to_kind=_optional_str(mapping.get("to_kind")),
                category=_optional_str(mapping.get("category")),
                direction=_optional_str(mapping.get("direction")),
                metamodel_level=_optional_str(mapping.get("metamodel_level")),
                description=_optional_str(mapping.get("description")),
                extra=_sorted_mapping(
                    {
                        key: value
                        for key, value in mapping.items()
                        if key
                        not in {
                            "id",
                            "name",
                            "from_kind",
                            "to_kind",
                            "category",
                            "direction",
                            "metamodel_level",
                            "description",
                        }
                    }
                ),
            )
        )
    return tuple(sorted(normalized, key=lambda item: item.id))


def _normalize_qualifier_definitions(items: Any) -> Tuple[QualifierDefinition, ...]:
    normalized: List[QualifierDefinition] = []
    for index, raw in enumerate(_expect_sequence(items, "qualifier definitions")):
        mapping = _expect_mapping(raw, f"qualifier_definitions[{index}]")
        normalized.append(
            QualifierDefinition(
                id=_required_str(mapping, "id", f"qualifier_definitions[{index}]"),
                name=_optional_str(mapping.get("name")),
                description=_optional_str(mapping.get("description") or mapping.get("note")),
                extra=_sorted_mapping(
                    {
                        key: value
                        for key, value in mapping.items()
                        if key not in {"id", "name", "description", "note"}
                    }
                ),
            )
        )
    return tuple(sorted(normalized, key=lambda item: item.id))


def _normalize_glossary_aliases(data: Mapping[str, Any]) -> Tuple[GlossaryAlias, ...]:
    aliases_raw = data.get("glossary_aliases")
    if aliases_raw is None:
        aliases_raw = data.get("aliases", [])

    normalized: List[GlossaryAlias] = []
    for index, raw in enumerate(_expect_sequence(aliases_raw, "glossary aliases")):
        mapping = _expect_mapping(raw, f"glossary_aliases[{index}]")
        normalized.append(
            GlossaryAlias(
                id=_required_str(mapping, "id", f"glossary_aliases[{index}]"),
                term=_optional_str(mapping.get("term")),
                alias=_optional_str(mapping.get("alias")),
                language=_optional_str(mapping.get("language") or mapping.get("locale")),
                extra=_sorted_mapping(
                    {
                        key: value
                        for key, value in mapping.items()
                        if key not in {"id", "term", "alias", "language", "locale"}
                    }
                ),
            )
        )
    return tuple(sorted(normalized, key=lambda item: item.id))


def _normalize_profiles(items: Any) -> List[str]:
    result: List[str] = []
    for index, value in enumerate(_expect_sequence(items, "profiles")):
        if not isinstance(value, str):
            raise OntologyLoadError(f"profiles[{index}] must be a string")
        result.append(value)
    return result


def _normalize_relation_catalog_relations(items: Any) -> Tuple[RelationCatalogRelation, ...]:
    normalized: List[RelationCatalogRelation] = []
    for index, raw in enumerate(_expect_sequence(items, "relation_catalog.relations")):
        mapping = _expect_mapping(raw, f"relation_catalog.relations[{index}]")
        relation_id = _required_str(
            mapping,
            "id",
            f"relation_catalog.relations[{index}]",
        )
        normalized.append(
            RelationCatalogRelation(
                id=relation_id,
                from_kind=_optional_str(mapping.get("from_kind")),
                to_kind=_optional_str(mapping.get("to_kind")),
                payload=_sorted_mapping(mapping),
            )
        )
    return tuple(sorted(normalized, key=lambda item: item.id))


def _load_yaml_mapping(path: Path, *, context: str) -> Dict[str, Any]:
    if not path.exists():
        raise OntologyLoadError(f"{context} file does not exist: {path}")

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)

    if not isinstance(data, dict):
        raise OntologyLoadError(f"{context} root must be a mapping: {path}")
    return data


def _require_sections(data: Mapping[str, Any], *, required: Iterable[str]) -> None:
    missing = [section for section in required if section not in data]
    if missing:
        missing_joined = ", ".join(sorted(missing))
        raise OntologyLoadError(f"ontology is missing required top-level section(s): {missing_joined}")


def _expect_mapping(value: Any, field_name: str) -> Dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise OntologyLoadError(f"{field_name} must be a mapping")
    return value


def _expect_sequence(value: Any, field_name: str) -> Sequence[Any]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise OntologyLoadError(f"{field_name} must be a list")
    return value


def _required_str(mapping: Mapping[str, Any], key: str, field_name: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise OntologyLoadError(f"{field_name}.{key} must be a non-empty string")
    return value


def _optional_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        return str(value)
    return value


def _sorted_mapping(value: Mapping[str, Any]) -> Dict[str, Any]:
    sorted_items = sorted(value.items(), key=lambda pair: pair[0])
    normalized: Dict[str, Any] = {}
    for key, raw in sorted_items:
        normalized[key] = _normalize_jsonlike(raw)
    return normalized


def _normalize_dictionaries(value: Any) -> Dict[str, Any]:
    mapping = _expect_mapping(value, "dictionaries")
    normalized: Dict[str, Any] = {}
    for key in sorted(mapping.keys()):
        raw = mapping[key]
        if isinstance(raw, list):
            if all(isinstance(item, dict) and "id" in item for item in raw):
                normalized[key] = [
                    _sorted_mapping(item)
                    for item in sorted(raw, key=lambda item: str(item["id"]))
                ]
            else:
                normalized[key] = [_normalize_jsonlike(item) for item in raw]
        else:
            normalized[key] = _normalize_jsonlike(raw)
    return normalized


def _normalize_jsonlike(value: Any) -> Any:
    if isinstance(value, dict):
        return _sorted_mapping(value)
    if isinstance(value, list):
        return [_normalize_jsonlike(item) for item in value]
    return value
