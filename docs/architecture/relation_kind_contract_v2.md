# Relation Kind Contract v2

Status: draft-for-review  
Session: 10  
Wave: 2 — ontology schema v2 и semantic core  
Depends on:
- execution_model.md
- north_star_mvp_boundaries.md
- storage_model_and_source_layers.md
- program_governance_and_artifact_contour.md
- metamodel_structural_audit.md
- rbank_atlas_structural_audit.md
- upstream_downstream_contract.md
- master_artifact_register.md
- ontology_schema_v2_high_level_design.md
- entity_kind_contract_v2.md
- attribute_def_contract_v2.md

## 1. Purpose

`relation_kind` — это first-class authoring-объект upstream-онтологии, который определяет допустимый тип связи между двумя `entity_kind` и несёт достаточно метаданных для:
- runtime relation catalog;
- graph traversal (`neighbors`, `paths`, `impact`);
- UI grouping и naming в Relations tab;
- export semantics;
- evidence-aware qualified edges;
- compatibility и deprecation policy.

`relation_kind` описывает **тип связи**, а не конкретное runtime-ребро.
Конкретные связи между экземплярами сущностей живут в runtime graph store как `edges` с `src`, `dst`, `kind`, `edge_attributes`, `sources[]`, timestamps и RBAC filtering.

---

## 2. Design goals

1. Сделать связи машиночитаемыми и валидируемыми.
2. Отделить authoring richness от runtime edge representation.
3. Поддержать deterministic generation `relation_catalog.json`.
4. Задать traversal-safe semantics для graph API.
5. Обеспечить explainability для path/impact и entity card.
6. Поддержать deprecation и non-breaking evolution relation model.
7. Явно различать:
   - simple typed relation;
   - relation with qualifiers;
   - cases, где требуется link-entity вместо relation kind.

---

## 3. Conceptual role of `relation_kind`

`relation_kind` отвечает на вопросы:
- между какими kinds связь допустима;
- как читается направление связи;
- какая у неё кардинальность;
- является ли она обычной, композиционной, ownership, lineage, deployment, realization и т.д.;
- должна ли она участвовать в traversal по умолчанию;
- допустимы ли qualifier-атрибуты на ребре;
- как связь показывается в UI и как влияет на path/impact semantics.

Каждый `relation_kind` должен быть:
- стабильным по `id`;
- однозначным по семантике;
- валидируемым по allowed endpoints;
- пригодным для deterministic runtime projection.

---

## 4. Required fields

### 4.1 Identity and semantics

#### Required
- `id: string`  
  Канонический стабильный идентификатор relation kind. Рекомендуемый формат: `snake_case`.
- `name: string`  
  Каноническое display name relation kind.
- `description: string`  
  Короткое точное определение семантики связи.
- `category: enum`  
  Семантическая категория relation kind. Базовый набор:
  - `association`
  - `aggregation`
  - `composition`
  - `ownership`
  - `responsibility`
  - `support`
  - `realization`
  - `implementation`
  - `deployment`
  - `flow`
  - `lineage`
  - `dependency`
  - `representation`
  - `service`
  - `mastership`
  - `mapping`
  - `reference`
- `status: enum`  
  `active | deprecated | experimental`
- `introduced_in: string`  
  Версия онтологии, где связь появилась.

#### Optional
- `aliases: string[]`
- `name_ru: string`
- `name_en: string`
- `deprecated_in: string`
- `replaced_by: string`
- `removal_after: string`
- `compatibility_notes: string`
- `examples: string[]`
- `anti_examples: string[]`

### 4.2 Endpoint contract

#### Required
- `from_kind: string`  
  `entity_kind.id` источника связи.
- `to_kind: string`  
  `entity_kind.id` приёмника связи.
- `direction: enum`  
  `directed | undirected`
- `source_cardinality: enum`  
  `one | many`
- `target_cardinality: enum`  
  `one | many`

#### Optional
- `applies_to_profiles: string[]`  
  Например: `atlas_mvp`, `enterprise_full`.
- `allow_self_reference: boolean`  
  По умолчанию `false`.
- `symmetric: boolean`  
  Допустимо только для `undirected` или явно симметричных моделей.

### 4.3 Inverse semantics

#### Required
- `has_inverse: boolean`

#### Conditional
- Если `has_inverse=true`, обязателен:
  - `inverse_relation_id: string`

#### Optional
- `inverse_name: string`
- `inverse_name_ru: string`
- `inverse_name_en: string`

### 4.4 Traversal semantics

#### Required
- `is_traversable_by_default: boolean`
- `allowed_in_neighbors: boolean`
- `allowed_in_paths: boolean`
- `allowed_in_impact: boolean`

#### Optional
- `default_direction_for_traversal: enum`  
  `out | in | both`
- `path_weight: number`  
  Относительный вес для top-k paths ranking.
- `impact_weight: number`  
  Относительный вес/приоритет для blast-radius summarization.
- `stop_propagation_by_default: boolean`
- `fanout_risk: enum`  
  `low | medium | high`
- `safe_mode_default: enum`  
  `include | exclude | conditional`
- `transitivity_hint: enum`  
  `none | domain_transitive | runtime_transitive`

### 4.5 Qualified-edge semantics

#### Required
- `supports_qualifiers: boolean`
- `evidence_required: boolean`

#### Conditional
- Если `supports_qualifiers=true`, обязателен:
  - `allowed_qualifiers: string[]`  
    Ссылки на `qualifier_def.id`

#### Optional
- `required_qualifiers: string[]`
- `edge_attribute_order: string[]`
- `edge_evidence_mode: enum`  
  `entity_level | edge_level | mixed`
- `field_level_provenance_supported: boolean`

### 4.6 UI and presentation semantics

#### Required
- `ui_label_out: string`  
  Как связь читается в карточке и графе от `from_kind` к `to_kind`.
- `ui_group: string`  
  Группа для Relations tab / graph legend.

#### Optional
- `ui_label_in: string`
- `ui_short_label: string`
- `ui_short_label_in: string`
- `ui_hide_by_default: boolean`
- `ui_priority: integer`
- `show_qualifiers_as_chips: boolean`
- `show_in_registry_filters: boolean`
- `graph_style_hint: enum`  
  `default | dashed | strong | weak | dependency | ownership | flow`

### 4.7 Export and interoperability semantics

#### Required
- `exportable: boolean`

#### Optional
- `export_label: string`
- `export_include_qualifiers: boolean`
- `export_include_evidence: boolean`
- `api_name_override: string`
- `external_mapping_codes: string[]`

---

## 5. Recommended additional fields

Не обязательны для MVP, но полезны для зрелой модели:
- `business_meaning: string`
- `governance_notes: string`
- `security_notes: string`
- `migration_recipe: string`
- `quality_expectation: enum` (`required_for_mvp | recommended | optional`)
- `expected_source_kinds: string[]` — hint, не runtime source mapping
- `allowed_source_namespaces: string[]` — hint, не policy enforcement
- `analytics_bucket: string`
- `change_risk: enum` (`low | medium | high`)

---

## 6. Invariants

### 6.1 Identity invariants
- `id` должен быть уникален во всей модели.
- `id` relation kind не должен переиспользоваться для другой семантики.
- Переименование display labels не является сменой identity.

### 6.2 Endpoint invariants
- `from_kind` и `to_kind` должны ссылаться на существующие `entity_kind.id`.
- Для MVP relation kind должен ссылаться только на kinds, входящие в активный профиль, либо явно помечаться как вне профиля.
- Если `allow_self_reference=false`, то `from_kind == to_kind` запрещено.

### 6.3 Inverse invariants
- Если `inverse_relation_id` указан, он должен существовать.
- Инверсная связь должна указывать обратно на исходную либо помечаться как canonical-only pair по специальному правилу.
- Для truly symmetric relations либо:
  - используется один `undirected` relation kind,
  - либо пара directed relations с `inverse_relation_id`.

### 6.4 Traversal invariants
- `allowed_in_paths=true` нельзя задавать, если relation не имеет осмысленной направленной семантики для path explanation.
- Relation с `fanout_risk=high` должен иметь либо `safe_mode_default=exclude`, либо документированное justification.
- `allowed_in_impact=true` для ownership/reference-only relations должно использоваться осторожно и явно обосновываться.

### 6.5 Qualifier invariants
- `required_qualifiers` должен быть подмножеством `allowed_qualifiers`.
- Если `supports_qualifiers=false`, `allowed_qualifiers` и `required_qualifiers` запрещены.
- Если relation требует edge-level explainability, `evidence_required=true` должно быть включено.

### 6.6 UI invariants
- `ui_label_out` обязателен даже при наличии `name`.
- `ui_group` должен быть из контролируемого набора групп, согласованного с entity card / graph UI.
- UI labels не должны подменять смысл relation kind; они являются presentation-layer names.

---

## 7. Controlled enums and reference vocabularies

### 7.1 Recommended `ui_group` vocabulary
- `structure`
- `ownership`
- `process`
- `data`
- `technology`
- `deployment`
- `integration`
- `lineage`
- `governance`
- `mapping`
- `other`

### 7.2 Recommended `category` usage rules
- `composition` — когда часть не существует отдельно в рамках моделируемого контекста или смыслово вложена.
- `aggregation` — когда объект входит в состав, но сохраняет отдельную идентичность.
- `ownership` — для владения активом/объектом.
- `responsibility` — для ответственности без ownership.
- `realization` / `implementation` — когда один слой реализует другой.
- `deployment` — размещение на runtime/resource layer.
- `flow` / `lineage` — движение информации/данных.
- `reference` — слабая справочная связь, обычно не path/impact-primary.

---

## 8. Distinguishing relation kind vs link entity

`relation_kind` следует использовать, если:
- связь семантически первична, но не требует самостоятельной карточки сущности;
- qualifiers ограничены и естественны для edge model;
- lifecycle связи привязан к связи между двумя объектами;
- runtime traversal должен идти по ребру без промежуточного узла.

Нужен **link entity**, если:
- связь имеет собственный жизненный цикл;
- у связи много собственных атрибутов и документов;
- связь должна быть discoverable как отдельный объект каталога;
- требуется независимое ownership/governance на саму связь.

`relation_kind` contract должен позволять явно документировать это решение в `compatibility_notes` или `governance_notes`.

---

## 9. Runtime projection expectations

Из `relation_kind` downstream bundle обычно получает runtime-friendly поля:
- `id`
- `from_kind`
- `to_kind`
- `direction`
- `inverse_relation_id`
- `category`
- `source_cardinality`
- `target_cardinality`
- `supports_qualifiers`
- `allowed_qualifiers`
- `is_traversable_by_default`
- `allowed_in_neighbors`
- `allowed_in_paths`
- `allowed_in_impact`
- `ui_label_out`
- `ui_label_in`
- `ui_group`
- `status`

В authoring-only слое остаются:
- длинные examples/anti_examples;
- governance notes;
- migration recipes;
- source hints;
- расширенные compatibility notes.

---

## 10. Validation checklist

Любой `relation_kind` должен проходить следующие проверки:
1. Уникальный `id`.
2. Непустые `name`, `description`, `ui_label_out`.
3. Валидные `from_kind` / `to_kind`.
4. Валидная `category`.
5. Валидный `direction`.
6. Валидные `source_cardinality` / `target_cardinality`.
7. Корректный inverse contract.
8. Корректный qualifier contract.
9. Корректные traversal flags.
10. Отсутствие конфликта между `status`, `deprecated_in`, `replaced_by`.
11. Совместимость с активными profiles.
12. Отсутствие дублирующей relation semantics под другим `id` без justification.

---

## 11. Example skeleton

```yaml
relation_kinds:
  - id: rel_process_supported_by_system
    name: Process supported by system
    description: Connects a business process to an IT system that supports its execution.
    category: support
    status: active
    introduced_in: 2.0.0
    from_kind: business_process
    to_kind: it_system
    direction: directed
    source_cardinality: many
    target_cardinality: many
    has_inverse: true
    inverse_relation_id: rel_it_system_supports_process
    is_traversable_by_default: true
    allowed_in_neighbors: true
    allowed_in_paths: true
    allowed_in_impact: true
    supports_qualifiers: true
    allowed_qualifiers:
      - role
      - channel
      - criticality
    evidence_required: true
    ui_label_out: supported by
    ui_label_in: supports
    ui_group: technology
    exportable: true
```

---

## 12. Open questions for next sessions

Следующей сессии потребуется уточнить:
- полный контракт `qualifier_def`;
- controlled vocabulary для `ui_group` и `graph_style_hint`;
- relation matrix бизнес-слоя;
- policy для producer/consumer-style relations и symmetric flows;
- правила перехода relation → link entity в data lineage и contract-heavy scenarios.

