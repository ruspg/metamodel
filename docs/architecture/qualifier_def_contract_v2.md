# Qualifier Definition Contract v2

Status: draft-for-review  
Session: 11  
Wave: 2 — ontology schema v2 и semantic core  
Depends on:
- execution_model.md
- north_star_mvp_boundaries.md
- storage_model_and_source_layers.md
- program_governance_and_artifact_contour.md
- upstream_downstream_contract.md
- master_artifact_register.md
- ontology_schema_v2_high_level_design.md
- entity_kind_contract_v2.md
- attribute_def_contract_v2.md
- relation_kind_contract_v2.md

## 1. Purpose

`qualifier_def` — это first-class authoring-объект upstream-онтологии, который определяет **тип edge-level атрибута** для qualified relations.

`qualifier_def` нужен, чтобы:
- задавать строгую модель `edge_attributes`;
- различать simple edge и qualified edge без импровизации;
- обеспечивать explainability на уровне конкретной связи;
- управлять export semantics для edge-level данных;
- задавать единые правила сериализации qualifiers в runtime;
- удерживать совместимость и предсказуемость relation catalog.

`qualifier_def` описывает **допустимый тип qualifier-поля**, а не конкретное значение на ребре.
Конкретные qualifier values живут в runtime graph store внутри edge representation и попадают в `edge_attributes`, evidence summaries и export outputs.

---

## 2. Design goals

1. Сделать edge-level поля машиночитаемыми и валидируемыми.
2. Поддержать explainable graph model без раздувания числа link entities.
3. Развести relation semantics и context semantics.
4. Сделать qualifiers пригодными для runtime serialization, UI rendering и export.
5. Ограничить хаос ad hoc edge properties.
6. Поддержать deprecation и non-breaking evolution qualifier model.
7. Сделать возможным осознанный выбор между:
   - relation without qualifiers;
   - relation with optional qualifiers;
   - relation with mandatory qualifiers;
   - link entity вместо edge.

---

## 3. Conceptual role of `qualifier_def`

`qualifier_def` отвечает на вопросы:
- какие edge-level поля вообще допустимы;
- какого они типа и кардинальности;
- обязательны ли они для конкретных relation kinds;
- как они влияют на explainability, filters, export и UI chips;
- являются ли они purely descriptive, operational, evidence-related, temporal, contractual или scoring-полями;
- нужно ли их учитывать в traversal explanations и path summaries.

`qualifier_def` **не должен**:
- дублировать semantics самой relation;
- заменять отдельную сущность, если у связи уже есть собственный lifecycle;
- хранить произвольный JSON без схемы;
- подменять evidence source model целиком.

---

## 4. When qualifiers should be used

Qualifiers должны использоваться, когда у связи есть **контекст**, но этот контекст:
- не оправдывает создание отдельной сущности;
- не требует собственного URN и lifecycle;
- нужен для объяснения, фильтрации, экспортов или auditability.

Типовые случаи:
- `channel`, `mode`, `role`, `directionality_hint`;
- `contract_id`, `sla_tier`, `criticality`;
- `confidence`, `match_rule`, `assertion_source`;
- `valid_from`, `valid_to`, `observed_at`, `last_confirmed_at`;
- `flow_type`, `integration_pattern`, `latency_class`;
- `evidence_note`, `manual_override_reason`.

Qualifiers **не должны** использоваться, если контекст связи:
- имеет собственный status/owner/version lifecycle;
- должен жить отдельной карточкой и быть отдельной точкой навигации;
- должен иметь самостоятельные связи с другими сущностями.

В таком случае нужен link entity или полноценный `entity_kind`.

---

## 5. Required fields

### 5.1 Identity and semantics

#### Required
- `id: string`  
  Канонический стабильный идентификатор qualifier definition. Рекомендуемый формат: `snake_case`.
- `name: string`  
  Каноническое display name qualifier.
- `description: string`  
  Точное определение смысла qualifier.
- `category: enum`  
  Семантическая категория qualifier. Базовый набор:
  - `descriptive`
  - `operational`
  - `temporal`
  - `contractual`
  - `governance`
  - `scoring`
  - `evidence`
  - `mapping`
  - `control`
  - `technical`
- `status: enum`  
  `active | deprecated | experimental`
- `introduced_in: string`

#### Optional
- `aliases: string[]`
- `name_ru: string`
- `name_en: string`
- `deprecated_in: string`
- `replaced_by: string`
- `removal_after: string`
- `examples: string[]`
- `anti_examples: string[]`
- `compatibility_notes: string`

### 5.2 Value model

#### Required
- `value_type: enum`  
  Базовый тип значения qualifier. Минимальный набор:
  - `string`
  - `text`
  - `integer`
  - `number`
  - `boolean`
  - `date`
  - `datetime`
  - `enum`
  - `urn_ref`
  - `url`
- `cardinality: enum`  
  `one | many`
- `nullability: enum`  
  `non_null | nullable`
- `serialization_form: enum`  
  `scalar | array | object_ref`

#### Conditional
- Если `value_type=enum`, обязателен один из вариантов:
  - `enum_values: string[]`
  - `enum_ref: string`
- Если `value_type=urn_ref`, обязателен:
  - `ref_kind: string | string[]`
- Если `serialization_form=object_ref`, обязателен:
  - `object_ref_schema: string`

#### Optional
- `default_value: any`
- `unit: string`
- `pattern: string`
- `min_value: number`
- `max_value: number`
- `max_length: integer`
- `precision: integer`
- `scale: integer`
- `allowed_url_schemes: string[]`

### 5.3 Usage scope

#### Required
- `usage_mode: enum`  
  `optional | relation_required | conditionally_required`
- `applicable_relation_kinds: string[] | "*"`  
  Список `relation_kind.id` или `*`, если qualifier является общим.

#### Optional
- `required_for_relation_kinds: string[]`
- `forbidden_for_relation_kinds: string[]`
- `conditional_requirement_rule: string`
- `applies_to_profiles: string[]`
- `edge_direction_scope: enum`  
  `from_to | to_from | both | not_directional`

### 5.4 Runtime and traversal semantics

#### Required
- `visible_in_runtime: boolean`
- `included_in_export_by_default: boolean`
- `included_in_edge_explanations: boolean`

#### Optional
- `affects_neighbors_rendering: boolean`
- `affects_path_ranking: boolean`
- `affects_impact_summarization: boolean`
- `affects_deduplication: boolean`
- `affects_conflict_resolution: boolean`
- `path_weight_modifier_rule: string`
- `impact_modifier_rule: string`
- `filterable: boolean`
- `sortable: boolean`
- `facetable: boolean`

### 5.5 UI and presentation semantics

#### Required
- `ui_label: string`
- `ui_render_mode: enum`  
  `chip | text | badge | date | link | hidden`

#### Optional
- `ui_group: string`
- `ui_priority: integer`
- `ui_short_label: string`
- `ui_hide_when_empty: boolean`
- `ui_show_in_relations_tab: boolean`
- `ui_show_on_graph_hover: boolean`
- `ui_show_in_export_preview: boolean`
- `ui_formatter_hint: enum`  
  `plain | percent | score | datetime | duration | enum_badge | url | urn_ref`

### 5.6 Evidence and provenance semantics

#### Required
- `can_be_source_asserted: boolean`
- `supports_multi_source_values: boolean`

#### Optional
- `requires_evidence_when_present: boolean`
- `provenance_granularity: enum`  
  `edge_level | qualifier_level | mixed`
- `confidence_supported: boolean`
- `manual_override_supported: boolean`
- `source_priority_sensitive: boolean`

---

## 6. Required invariants

1. `id` должен быть глобально уникальным внутри ontology model.
2. `value_type`, `cardinality` и `serialization_form` должны быть совместимы.
3. `enum_values` и `enum_ref` не могут одновременно отсутствовать при `value_type=enum`.
4. `ref_kind` обязателен для `urn_ref`.
5. Если `usage_mode=relation_required`, qualifier должен фигурировать в relation policies как required.
6. `required_for_relation_kinds` должен быть подмножеством `applicable_relation_kinds`, если `applicable_relation_kinds` не равно `*`.
7. Qualifier с `visible_in_runtime=false` не может быть `included_in_export_by_default=true`.
8. Qualifier с `ui_render_mode=hidden` не должен быть единственным объясняющим qualifier для relation kind.
9. Qualifier, влияющий на `path_ranking` или `impact_summarization`, должен иметь формализованное правило или bounded enum.
10. Deprecated qualifier не должен добавляться в новые relations без явного compatibility exception.

---

## 7. Recommended categories of qualifiers

### 7.1 Descriptive qualifiers
Для edge-context без operational последствий.
Примеры:
- `role`
- `channel`
- `interaction_type`

### 7.2 Operational qualifiers
Для runtime контекста связи.
Примеры:
- `sync_mode`
- `latency_class`
- `throughput_tier`

### 7.3 Temporal qualifiers
Для bounded applicability связи.
Примеры:
- `valid_from`
- `valid_to`
- `observed_at`

### 7.4 Contractual qualifiers
Для formal agreement вокруг связи.
Примеры:
- `contract_id`
- `sla_tier`
- `service_level`

### 7.5 Evidence / scoring qualifiers
Для explainability и trust.
Примеры:
- `confidence`
- `match_rule`
- `assertion_source`
- `manual_override_reason`

---

## 8. Relation-level usage patterns

### Pattern A — Optional descriptive qualifiers
Пример: `business_process_supports_business_function` может иметь optional `role`.

### Pattern B — Required operational qualifiers
Пример: `it_system_reads_data_table` должен иметь `access_mode` или `purpose`.

### Pattern C — Temporal validity qualifiers
Пример: ownership relation может иметь `valid_from` и `valid_to`.

### Pattern D — Evidence-sensitive qualifiers
Пример: inferred/matched relation должен иметь `confidence` и `match_rule`.

### Pattern E — Export-only informative qualifiers
Пример: `source_row_id` или `mapping_batch_id`, которые полезны для audit/export, но не для UI.

---

## 9. Runtime serialization contract

В runtime qualified edge должен сериализоваться предсказуемо и без знания authoring internals.

Рекомендуемая форма:

```json
{
  "edge_urn": "urn:edge:...",
  "kind": "system_reads_table",
  "src": "urn:...",
  "dst": "urn:...",
  "edge_attributes": {
    "access_mode": "read_only",
    "confidence": 0.92,
    "match_rule": "cmdb_plus_manual",
    "valid_from": "2026-01-01"
  },
  "sources": [
    {
      "namespace": "cmdb",
      "key": "rel-123",
      "external_url": "..."
    }
  ]
}
```

Требования к runtime serialization:
- ключи `edge_attributes` должны совпадать с `qualifier_def.id`;
- scalar и multi-valued qualifiers сериализуются детерминированно;
- `urn_ref` сериализуется как URN или массив URN;
- deprecated qualifiers могут присутствовать только для backward compatibility;
- отсутствие qualifier не должно путаться с `null`, если для него задан `non_null` semantic.

---

## 10. Explainability rules

Qualifiers должны повышать объяснимость, а не ухудшать её.

Обязательные принципы:
1. В path/impact summaries показываются только qualifiers с высокой explanatory value.
2. В entity relations tab qualifiers рендерятся как chips/badges/text по `ui_render_mode`.
3. Evidence-sensitive qualifiers должны быть связаны с source/provenance model.
4. Export должен уметь явно включать и исключать qualifiers.
5. Qualifier не должен становиться единственным носителем базовой semantics связи.

---

## 11. Distinguishing qualified edge from link entity

Нужен `qualifier_def`, если:
- связь остаётся связью;
- контекст связи можно уместить в bounded set полей;
- у связи нет самостоятельного lifecycle.

Нужен link entity, если:
- контекст связи сам становится предметом управления;
- у него есть собственные owners/status/versioning;
- он должен участвовать в relations как самостоятельный узел;
- для него нужна отдельная карточка/registry/search.

`qualifier_def` сам по себе не решает этот выбор, но задаёт строгую границу допустимого edge context.

---

## 12. Compatibility and evolution rules

Compatible changes:
- добавление нового optional qualifier;
- добавление UI hints;
- добавление enum values без нарушения downstream assumptions, если это явно разрешено policy;
- расширение `applicable_relation_kinds` для experimental qualifiers.

Conditionally compatible:
- изменение formatter/render hints;
- добавление qualifier в default export;
- расширение влияния qualifier на path/impact logic.

Breaking changes:
- переименование `id`;
- изменение `value_type`;
- изменение `cardinality`;
- перевод optional qualifier в required без migration path;
- удаление qualifier без deprecation lifecycle;
- сужение `applicable_relation_kinds`, если qualifier уже встречается в runtime data.

---

## 13. Minimum runtime projection

В `relation_catalog.json` и runtime metamodel qualifier должен попадать как компактная metadata-проекция:
- `id`
- `name`
- `value_type`
- `cardinality`
- `ui_label`
- `ui_render_mode`
- `included_in_export_by_default`
- `included_in_edge_explanations`
- `applicable_relation_kinds`
- `required_for_relation_kinds`
- `status`

Downstream runtime не обязан знать весь authoring richness qualifier definition.

---

## 14. Design examples

### Example 1 — Confidence qualifier
```yaml
id: confidence
name: Confidence
category: scoring
value_type: number
cardinality: one
nullability: non_null
serialization_form: scalar
usage_mode: optional
applicable_relation_kinds: "*"
visible_in_runtime: true
included_in_export_by_default: true
included_in_edge_explanations: true
ui_label: Confidence
ui_render_mode: badge
can_be_source_asserted: true
supports_multi_source_values: false
```

### Example 2 — Contract identifier qualifier
```yaml
id: contract_id
name: Contract ID
category: contractual
value_type: string
cardinality: one
nullability: nullable
serialization_form: scalar
usage_mode: conditionally_required
applicable_relation_kinds:
  - system_serves_business_process
  - data_product_serves_business_process
visible_in_runtime: true
included_in_export_by_default: true
included_in_edge_explanations: true
ui_label: Contract
ui_render_mode: text
can_be_source_asserted: true
supports_multi_source_values: false
```

### Example 3 — Validity interval qualifier pair
```yaml
id: valid_from
name: Valid From
category: temporal
value_type: date
cardinality: one
nullability: nullable
serialization_form: scalar
usage_mode: optional
applicable_relation_kinds:
  - logical_resource_owned_by_team
  - business_process_owned_by_team
visible_in_runtime: true
included_in_export_by_default: true
included_in_edge_explanations: false
ui_label: Valid from
ui_render_mode: date
can_be_source_asserted: true
supports_multi_source_values: false
```

---

## 15. Open questions for later sessions

1. Нужен ли отдельный global qualifier library profile для `atlas_mvp` vs `enterprise_full`.
2. Нужно ли различать qualifiers, разрешённые только для inferred edges.
3. Нужен ли специальный qualifier type для multilingual labels.
4. Нужно ли выносить confidence/evidence model в отдельный reusable contract.
5. Должны ли qualifier values участвовать в search index напрямую.

---

## 16. Acceptance criteria for this session

Сессия считается завершённой, если:
1. Можно строго описать qualifier library без ad hoc edge fields.
2. Можно различать simple edge и qualified edge на уровне authoring contract.
3. Relation kinds могут ссылаться на qualifier definitions детерминированно.
4. Runtime serialization edge attributes не зависит от неявных правил.
5. Export/UI/explainability знают, какие qualifiers выводить и как.
6. Будущие Codex-валидаторы могут автоматически проверять qualifier usage.

