# Relation Catalog — Нормативные правила

> Канонический контракт relation kinds, допускаемых в runtime-проекцию.

## 1. Назначение

`relation_catalog` — канонический машиночитаемый контракт relation kinds, которые допускаются в runtime projection.

Он фиксирует **какие relation kinds разрешены и как они должны интерпретироваться в runtime**, включая traversal, impact, UI labels, qualifier policy и evidence policy.

Важные различия:

- **Authoring-level relation kind contract** (`relation_kind_contract_v2.md`): полный upstream-контракт типа связи (богатый, authoring-first).
- **Relation catalog entry** (этот документ + `relation_catalog_v2_spec.yaml`): runtime-oriented, profile-aware нормализованная запись relation kind для конкретной волны.
- **Runtime edge**: фактическое ребро между instance-узлами (`src`, `dst`, `kind`, `edge_attributes`, `sources[]`, timestamps).
- **Qualified edge**: runtime edge, где смысл/объяснимость зависит от edge-level qualifiers, определённых в `qualifier_def`.
- **Future link-entity case**: случаи, где связь уже не должна быть ребром и должна быть повышена до отдельной сущности с lifecycle.

---

## 2. Scope (Wave 1)

Wave 1 relation catalog включает:

1. **Business-layer backbone** из P0 relation matrix.
2. **Минимум P1**, который реально улучшает neighbors/paths/impact/BPMN context.
3. **Минимум cross-layer relations** для полезного process-centric traversal:
   - process/operation -> IT support;
   - operation -> data context;
   - operation -> ownership/responsibility context.
4. Relation kinds, необходимые для:
   - entity card relations tab;
   - neighbors;
   - paths;
   - impact;
   - BPMN activity context через `business_operation`.

В Wave 1 **отложено**:

- полный universe relation kinds по всем слоям;
- rich lineage map beyond MVP-critical edges;
- contract-heavy link-entity conversion;
- risk/control/policy relation families;
- расширенные ranking weights/advanced traversal tuning.

---

## 3. Canonical relation entry model (normative)

Каждая запись relation catalog **должна** содержать поля ниже.

- `id` — стабильный канонический идентификатор relation entry (snake_case, не переиспользуется под другую семантику).
- `name` — canonical display name relation kind.
- `description` — краткое и точное определение семантики.
- `from_kind` — источник связи (`entity_kind.id`).
- `to_kind` — цель связи (`entity_kind.id`).
- `category` — семантическая категория (из согласованного vocab).
- `direction` — `directed | undirected`.
- `source_cardinality` — `one | many` со стороны `from_kind`.
- `target_cardinality` — `one | many` со стороны `to_kind`.
- `has_inverse` — наличие формальной inverse semantics.
- `inverse_relation_id` — ID inverse relation (обязательно при `has_inverse=true`).
- `is_traversable_by_default` — включается ли relation в дефолтный traversal.
- `allowed_in_neighbors` — можно ли показывать в neighbors API/UX.
- `allowed_in_paths` — допускается ли в path explanation.
- `allowed_in_impact` — допускается ли в impact propagation/summaries.
- `default_visibility` — `visible | collapsed | hidden` политика показа relation по умолчанию в стандартных surfaces.
- `path_priority` — `primary | secondary | tertiary | excluded` детерминированный приоритет relation для path ranking.
- `impact_mode` — `propagate | explain_only | exclude` семантика участия relation в impact results.
- `supports_qualifiers` — допускает ли edge-level qualifiers.
- `allowed_qualifiers` — whitelist qualifier IDs (пустой список для non-qualified relation).
- `required_qualifiers` — подмножество `allowed_qualifiers`, обязательное для edge instance.
- `evidence_required` — требуется ли evidence для утверждения edge.
- `ui_label_out` — label из `from_kind` в `to_kind`.
- `ui_label_in` — label с обратной стороны (для entity card/graph hover).
- `ui_group` — контролируемая UI-группа relation.
- `exportable` — включается ли в runtime export/profile snapshot.
- `status` — `active | deprecated | experimental`.
- `introduced_in` — версия модели, где relation зафиксирован.
- `applies_to_profiles` — профили, где relation разрешён (Wave 1: минимум `atlas_mvp`).

---

## 4. Normative rules

### Rule 1 — Relation identity and naming

1. `id` уникален в каталоге.
2. Формат ID: `rel_<source_semantics>_<target_semantics>`.
3. Изменение UI labels/description не меняет identity.
4. Semantic breaking change требует нового `id` и deprecation старого.

### Rule 2 — Endpoint validity

1. `from_kind`/`to_kind` должны ссылаться на валидные `entity_kind.id`.
2. Relation не должен нарушать business-layer anti-patterns (например, `business_process -> business_function` как primary decomposition).
3. Self-relations разрешены только если они явно заданы в каталоге (например, dependency/precedes families).

### Rule 3 — Inverse relation policy

1. Для directed relation в каталоге фиксируется логическая inverse semantics.
2. Если `has_inverse=true`, `inverse_relation_id` обязателен и должен ссылаться на существующую relation entry.
3. Inverse entry должна указывать обратно на canonical entry (двусторонняя связность пары).
4. Runtime может хранить canonical direction, но catalog обязан содержать обе стороны semantics для UI/API.

### Rule 4 — Cardinality policy

1. Кардинальности задаются на уровне relation kind и не должны выводиться ad hoc в runtime.
2. Для backbone relations, где реальная модель допускает множественность, использовать `many -> many`.
3. `one -> many` использовать только там, где это часть доменной нормы (например, stage принадлежит одному stream в canonical модели).

### Rule 5 — Traversal policy

1. Relation с `is_traversable_by_default=true` должен быть low-noise и explainable для MVP.
2. Default traversal для business-centric UX должен отдавать приоритет P0 backbone.
3. High-fanout/reference-only relation не включать в default traversal без необходимости.

### Rule 6 — Path and impact participation

1. `allowed_in_paths=true` только если relation даёт осмысленное объяснение причинно/структурного перехода.
2. `allowed_in_impact=true` только если relation может нести семантику распространения влияния.
3. Ownership/mapping-only relations допускаются в impact только при явной полезности для explainability.

### Rule 6A — Visibility policy

1. `default_visibility` обязателен для каждого relation entry и может быть только `visible | collapsed | hidden`.
2. `visible` означает, что relation показывается по умолчанию в стандартных graph/card relation surfaces.
3. `collapsed` означает, что relation доступен по умолчанию, но в grouped/collapsed состоянии до явного expand.
4. `hidden` означает, что relation не показывается в стандартных surfaces по умолчанию; relation может быть доступен только в advanced/debug/export contexts при отдельном разрешении.
5. `default_visibility` не отменяет capability-флаги:
   - если `allowed_in_neighbors=false`, relation не должен появляться в neighbors независимо от visibility;
   - если `allowed_in_paths=false`, relation не используется в path search/ranking независимо от visibility;
   - если `allowed_in_impact=false`, relation не участвует в impact независимо от visibility/impact_mode;
   - `ui_group` остаётся группирующим измерением и используется совместно с `default_visibility` (например, collapsed по группе).

### Rule 6B — Deterministic path ranking policy

1. `path_priority` обязателен для каждого relation entry и может быть только `primary | secondary | tertiary | excluded`.
2. `primary` — relation приоритетен при ранжировании explanatory/business-critical paths.
3. `secondary` — relation валиден, но должен уступать `primary` при прочих равных.
4. `tertiary` — relation допустим как fallback и не должен доминировать в top paths.
5. `excluded` — relation не должен использоваться path ranking даже если edge физически существует.
6. Для Wave 1 ranking policy:
   - structural/process backbone relations обычно должны outrank contextual/support relations;
   - ownership/context relations не должны доминировать над process/data/technology bridge paths;
   - relations с `path_priority=excluded` всегда исключаются из path ranking.

### Rule 6C — Impact propagation policy

1. `impact_mode` обязателен для каждого relation entry и может быть только `propagate | explain_only | exclude`.
2. `propagate` — relation может расширять blast radius.
3. `explain_only` — relation может отображаться в impact results как контекст, но не распространяет impact дальше.
4. `exclude` — relation не участвует в impact results.
5. `allowed_in_impact` сохраняется как coarse gate для совместимости Wave 1; `impact_mode` является более сильной семантикой интерпретации.
6. Если `allowed_in_impact=false`, runtime обязан трактовать relation как effectively excluded для impact независимо от `impact_mode`.

### Rule 7 — Qualifiers policy

1. `required_qualifiers` всегда подмножество `allowed_qualifiers`.
2. Если `supports_qualifiers=false`, `allowed_qualifiers=[]` и `required_qualifiers=[]`.
3. Qualified edge использовать только там, где edge context materially меняет смысл (operation/entity interaction, flow payload role, dependency type).
4. Qualifier IDs должны соответствовать `qualifier_def` vocabulary.

### Rule 8 — Evidence policy

1. Для qualified relations, которые влияют на impact/path explainability, `evidence_required=true`.
2. Для structural backbone direct relations допускается `evidence_required=false` в MVP (если связь подтверждается source lineage уровня узла/набора).
3. Если relation участвует в governance/ownership claims, evidence policy должна быть явной и строгой.

### Rule 9 — Direct edge vs qualified edge

Использовать **direct edge**, если:
- связь бинарна и устойчива;
- edge-level context не нужен для интерпретации.

Использовать **qualified edge**, если без qualifiers теряется ключевой смысл/проверяемость:
- operation acts on entity (`interaction_type`, `criticality`, `mandatory`);
- information flow carries entity (`payload_role`, `sensitivity`);
- dependency/precedes families (`dependency_type`, `condition`, `order_index`).

### Rule 10 — When relation must be deferred to link-entity

Не моделировать как relation, если:
- связь имеет самостоятельный lifecycle/status/version;
- нужна отдельная discoverable карточка;
- связь сама имеет много собственных relations/ownership/governance.

Такие случаи фиксируются как deferred link-entity pattern (post-Wave 1).

### Rule 11 — Lifecycle and deprecation

1. `status=active` для Wave 1 production catalog.
2. Для замены relation используется soft deprecation: `status=deprecated`, указание replacement relation, сохранение backward compatibility window.
3. Физическое удаление relation ID возможно только после removal window и migration.

---

## 5. Wave 1 modeling policy

1. Начинать от business backbone (P0 matrix) и сохранять его как traversal spine.
2. Предпочитать direct edges.
3. Qualified edges вводить только при материальной добавке к анализу/объяснимости.
4. Каталог держать **minimal-but-strong**: меньше relation kinds, но каждый реально полезен для MVP UX/API.
5. Не расширять каталог «на будущее» без конкретного Wave 1 use case.
6. `business_operation` — обязательный first-class bridge для BPMN activity context и cross-layer navigation.

---

## 6. Controlled relation groups

`ui_group` и связанное `category` используют контролируемый набор:

- `process` — process/operation/function/stage sequencing and decomposition.
- `ownership` — owner/responsible/performer semantics.
- `data` — business_entity, information_flow, data product/object context.
- `technology` — system/component support or implementation context.
- `lineage` — data/flow lineage semantics.
- `governance` — policy/risk/control/compliance relations.
- `structure` — containment/aggregation/composition backbone links.
- `mapping` — cross-model mapping relations.
- `other` — допустимо только как explicit exception.

---

## 7. Downstream projection expectations

Из `relation_catalog_v2_spec.yaml` downstream pipeline должен детерминированно строить:

1. `relation_catalog.json` в atlas bundle (runtime-facing compact contract).
2. Поле relation model в `/v1/meta/model` для UI/API capability discovery.

Минимально проецируемые поля:
`id`, `from_kind`, `to_kind`, `direction`, `inverse_relation_id`, `category`, `source_cardinality`, `target_cardinality`, traversal flags, qualifier policy, evidence policy, UI labels/group, status, profile applicability.

Вне scope этого документа:
- runtime storage internals;
- import implementation details;
- source-specific ingestion pipelines.
