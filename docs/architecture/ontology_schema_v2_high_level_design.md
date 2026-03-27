# Ontology Schema — High-Level Design

> Архитектурный обзор authoring-контракта онтологии: блоки, принципы, границы.

## 1. Назначение

Ontology Schema v2 is the authoring contract of the upstream `metamodel` repository. It is the canonical machine-readable schema for describing:
- model metadata;
- entity kinds;
- relation kinds;
- attribute definitions;
- qualifier definitions;
- aliases and glossary signals;
- lifecycle and compatibility metadata;
- UI/search/runtime hints needed to generate atlas-ready projection artifacts.

Schema v2 is not a runtime contract. Runtime consumers in `rbank-atlas` must consume only release bundle artifacts generated from the authoring model.

## 2. Design goals

1. Make ontology authoring deterministic and machine-readable.
2. Preserve conceptual richness without leaking authoring internals into runtime.
3. Support generation of:
   - `metamodel_snapshot.json`
   - `type_catalog.json`
   - `relation_catalog.json`
   - `search_aliases.json`
   - compatibility and migration reports
4. Be reviewable and evolvable in Git.
5. Support stable IDs, lifecycle controls, aliases, and compatibility classification.
6. Carry enough metadata for API/UI/MCP surfaces without forcing runtime to understand the full authoring format.

## 3. Scope of Schema v2

Schema v2 covers only ontology authoring concerns:
- definitions of kinds and relations;
- field semantics;
- qualifier semantics;
- glossary and alias metadata;
- compatibility metadata;
- authoring-time hints for search/UI/runtime projection.

Schema v2 does **not** contain:
- concrete bank instance data;
- source-specific field mappings;
- merge/conflict policy;
- runtime traversal limits;
- ingestion jobs or schedules;
- operational observability settings.

Those remain in `rbank-atlas` runtime contracts.

## 4. Top-level authoring blocks

Schema v2 consists of these top-level blocks:

### 4.1 `model`
Repository-level metadata for the ontology release lineage.

Responsibilities:
- ontology identity;
- version and status;
- authorship and ownership;
- scope/profile references;
- compatibility anchors;
- glossary language strategy.

### 4.2 `entity_kinds`
Canonical definitions of entity types used by atlas.

Responsibilities:
- semantic definition of a kind;
- category/layer placement;
- lifecycle status;
- inheritance/composition hooks;
- attribute attachment;
- key/display/search/UI hints.

### 4.3 `relation_kinds`
Canonical definitions of graph relations.

Responsibilities:
- relation meaning;
- source and target kind constraints;
- direction and inverse;
- cardinality model;
- traversability/path hints;
- evidence and qualifier expectations.

### 4.4 `attribute_defs`
Reusable definitions of fields that can be attached to kinds.

Responsibilities:
- value typing;
- cardinality;
- validation semantics;
- display/search/filter/sort hints;
- evidence or external-link semantics;
- runtime projection metadata.

### 4.5 `qualifier_defs`
Reusable definitions for edge-level qualifiers.

Responsibilities:
- typed metadata on relations;
- explanation and edge semantics;
- serialization rules for runtime;
- export and traversal influence metadata.

### 4.6 `glossary`
Canonical term system across RU/EN naming and synonyms.

Responsibilities:
- canonical term vs display term;
- aliases/synonyms/forbidden terms;
- search normalization;
- migration support for renamed concepts.

### 4.7 `profiles`
Optional named projections or subsets.

Responsibilities:
- MVP subset;
- domain-specific subsets;
- export scopes;
- consumer-specific slices.

### 4.8 `compatibility`
Authoring-level metadata used by release validation.

Responsibilities:
- schema generation version;
- compatibility policy version;
- deprecation windows;
- change classification hints.

## 5. Core design principles

### 5.1 Stable identifiers first
Every kind, relation, attribute, and qualifier must have a stable canonical ID that is never casually renamed.

### 5.2 Display text is not identity
Human-readable names, labels, and RU/EN display variants may evolve independently from canonical IDs.

### 5.3 Reuse typed definitions
Attributes and qualifiers are first-class reusable definitions, not ad hoc inline text blobs.

### 5.4 Authoring richness, runtime minimalism
The authoring model can be richer than the runtime projection, but every runtime field must have a clear source in the authoring schema.

### 5.5 Explicit lifecycle
Anything that can be deprecated, replaced, or hidden must carry lifecycle metadata.

### 5.6 Explainability by construction
Schema v2 must make it possible to generate runtime surfaces that explain what a type/relation means and how it should be shown.

## 6. High-level contract for `model`

The `model` block should include:
- `id`;
- `name`;
- `description`;
- `version`;
- `status`;
- `owners`;
- `languages` and naming strategy;
- `default_profile`;
- `compatibility_policy_version`;
- `schema_version`;
- `generated_at` or release lineage reference;
- optional references to glossary packs and profiles.

Purpose: allow validation, release generation, and downstream traceability.

## 7. High-level contract for `entity_kind`

Each entity kind should be a first-class object with these semantic groups:

### Identity and semantic definition
- canonical ID;
- canonical name;
- localized display names;
- description;
- aliases;
- category;
- layer.

### Lifecycle and compatibility
- status;
- introduced/deprecated/replaced metadata;
- compatibility notes;
- optional maturity level.

### Structural semantics
- inheritance/composition hooks;
- abstract vs concrete flag;
- allowed profiles/subsets;
- attribute attachment model.

### Runtime projection hints
- default title field;
- key attributes;
- search hints;
- filter/sort hints;
- UI card/list hints;
- registry grouping hints.

### Governance hints
- owning domain/team;
- review class;
- evidence expectations if relevant.

Детальный контракт: [Entity Kind Contract](entity_kind_contract_v2.md).

## 8. High-level contract for `relation_kind`

Each relation kind should be a first-class object with these semantic groups:

### Identity and semantic definition
- canonical ID;
- canonical name;
- localized display names;
- description;
- aliases;
- category.

### Graph semantics
- source kind constraints;
- target kind constraints;
- direction;
- inverse;
- cardinality;
- traversability defaults.

### Qualified-edge semantics
- supported qualifiers;
- required qualifiers;
- evidence policy;
- edge explanation hints.

### Runtime/path hints
- default visibility;
- path weight;
- impact relevance;
- grouping/label hints for UI.

### Lifecycle and compatibility
- status;
- deprecation/replacement metadata;
- breaking-change sensitivity.

Детальный контракт: [Relation Kind Contract](relation_kind_contract_v2.md).

## 9. High-level contract for `attribute_def`

Attributes must move from loose descriptions to reusable typed definitions.

Each `attribute_def` should carry these semantic groups:
- identity and human meaning;
- data type and cardinality;
- required/optional semantics;
- enum or reference semantics where applicable;
- validation hints;
- search/filter/sort/index hints;
- UI display hints;
- external-link or evidence semantics where applicable;
- runtime serialization hints.

Детальный контракт: [Attribute Definition Contract](attribute_def_contract_v2.md).

## 10. High-level contract for `qualifier_def`

Qualifiers are typed edge-level fields.

Each `qualifier_def` should carry these semantic groups:
- identity and meaning;
- data type and cardinality;
- allowed relation scopes;
- required/optional semantics;
- display/explainability semantics;
- export/runtime serialization hints;
- traversal influence flags when needed.

Детальный контракт: [Qualifier Definition Contract](qualifier_def_contract_v2.md).

## 11. Lifecycle and deprecation model

Schema v2 must support explicit lifecycle across all definition types.

Required concepts:
- `status` (`active`, `experimental`, `deprecated`, possibly `internal`/`retired` later);
- `introduced_in`;
- `deprecated_in`;
- `replaced_by`;
- optional `sunset_after`;
- migration notes reference.

Principles:
- deprecation is metadata, not silent removal;
- replacements must point to canonical IDs;
- runtime projections may omit retired internals, but authoring validation must still understand lineage;
- compatibility analysis must classify lifecycle changes automatically.

## 12. Alias, synonym, and glossary model

Schema v2 must treat terminology as managed data, not free text.

Needed concepts:
- canonical term;
- display terms;
- aliases;
- RU/EN naming pairs;
- deprecated aliases;
- forbidden/ambiguous terms;
- search normalization forms.

This enables:
- stable ontology terminology;
- search recall and disambiguation;
- migration from old naming without ID churn.

Детальная политика: [Glossary и Naming Policy](glossary_alias_naming_policy.md).

## 13. UI, search, and runtime hints

Schema v2 should include authoring-level hints that are intentionally projection-friendly.

### UI hints
Examples:
- card sections;
- default summary fields;
- registry columns;
- badges/tags;
- relation grouping labels.

### Search hints
Examples:
- indexed fields;
- query aliases;
- facetable/filterable fields;
- fuzzy matching allowances;
- boost hints.

### Runtime hints
Examples:
- inclusion in metamodel snapshot;
- projection class;
- default export visibility;
- explainability labels.

Rule: these hints are advisory authoring metadata, not hardcoded runtime behavior by themselves.

## 14. Inheritance and composition stance

Schema v2 may support limited inheritance/composition, but only in a controlled form.

Recommended stance:
- allow shallow inheritance for shared metadata patterns;
- avoid deep polymorphic trees;
- prefer explicit composition of attribute sets where possible;
- require flattening to deterministic normalized forms before bundle generation.

Reason: runtime consumers need stable flattened catalogs, not dynamic inheritance interpretation.

## 15. Profiles and subsets

Schema v2 should natively support named profiles/subsets.

Use cases:
- MVP subset;
- domain slices;
- future role-specific or deployment-specific subsets;
- validation of minimum demonstrable slice coverage.

Profiles are authoring metadata and bundle-generation inputs, not independent ontologies.

## 16. Normalization boundary

Before release bundle generation, authoring schema v2 must be normalized into a canonical intermediate form.

Normalization should:
- resolve inherited fields;
- expand reusable attribute/qualifier references;
- validate IDs and references;
- resolve aliases and glossary links;
- materialize lifecycle metadata;
- produce deterministic ordering.

This normalized intermediate model is the direct input for bundle generation.

## 17. Relationship to runtime surfaces

Schema v2 must be designed backward from required runtime consumers:
- `/v1/meta/model` snapshot;
- metamodel registry UI;
- MCP metamodel surface;
- entity card rendering metadata;
- traversal/export/explainability support.

Implication:
- kinds and relations need projection-friendly labels and summaries;
- attributes need runtime field metadata;
- qualifiers need serializable edge metadata;
- aliases/glossary need search-ready outputs.

## 18. Recommended top-level YAML shape

Illustrative high-level shape:

```yaml
model:
  ...

glossary:
  ...

attribute_defs:
  - ...

qualifier_defs:
  - ...

entity_kinds:
  - ...

relation_kinds:
  - ...

profiles:
  - ...

compatibility:
  ...
```

This is a conceptual shape, not the final formal schema.

## 19. What Schema v2 must enable next

На основе этого дизайна реализуются:
1. exact `entity_kind` contract;
2. exact `attribute_def` contract;
3. exact `relation_kind` contract;
4. exact `qualifier_def` contract;
5. glossary/alias policy;
6. ontology authoring directory structure;
7. bundle generator inputs;
8. compatibility and validation rules.

## 20. Ключевые принципы

1. Схема онтологии — **authoring contract**, а не формат runtime API.
2. `metamodel` владеет схемой; `rbank-atlas` потребляет только сгенерированные release-артефакты.
3. Types, relations, attributes и qualifiers — first-class элементы онтологии.
4. Aliases/glossary и lifecycle metadata — обязательные части модели, а не опциональная проза.
5. UI/search/runtime hints хранятся в authoring как projection-friendly metadata.
6. Нормализация обязательна перед генерацией bundle.
7. Profiles/subsets — нативная функция authoring-модели.

## 21. Связанные контракты

- [Entity Kind Contract](entity_kind_contract_v2.md)
- [Attribute Definition Contract](attribute_def_contract_v2.md)
- [Relation Kind Contract](relation_kind_contract_v2.md)
- [Qualifier Definition Contract](qualifier_def_contract_v2.md)
- [Glossary и Naming Policy](glossary_alias_naming_policy.md)
- [Relation Catalog Rules](relation_catalog_v2_rules.md)
