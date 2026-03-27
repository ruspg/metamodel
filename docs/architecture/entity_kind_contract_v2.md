# Entity Kind Contract

> Контракт определения типа сущности в онтологии.

## 1. Назначение

`entity_kind` — каноническое определение типа сущности в authoring-онтологии `metamodel`.
Его задача — быть одновременно:
- семантическим контрактом для предметной модели;
- машиночитаемым источником для генерации runtime type catalog;
- основой для UI, search, traversal, entity card и import validation.

`entity_kind` существует только в upstream authoring-модели и не является runtime payload сам по себе. В runtime он проецируется в нормализованный `type_catalog` и metamodel snapshot.

## 2. Дизайн-цели

Контракт должен обеспечивать:
- строгую валидацию любого kind;
- однозначную идентификацию kind во всех bundle-артефактах;
- достаточность для runtime projection в `rbank-atlas`;
- поддержку UI/entity card/search без ручных per-kind исключений;
- controlled evolution через lifecycle/deprecation;
- отделение authoring richness от runtime-минимума.

## 3. Нормативная структура `entity_kind`

Ниже — рекомендуемая структура authoring-контракта.

```yaml
id: business_process
name: Business Process
name_ru: Бизнес-процесс
summary: Управляемый поток работ, создающий бизнес-результат.
description: >
  Канонический тип для процессов банка, используемый как якорь навигации,
  BPMN-портала, impact и process-to-system вопросов.
category: process
layer: business
status: active
introduced_in: 2.0.0
deprecated_in: null
replaced_by: null
aliases:
  - process
  - biz_process
  - процесс
canonical_term: business_process
parent_kind: null
abstract: false
instantiable: true
owned_by_profile:
  - atlas_mvp
key_attributes:
  - owner
  - tier
  - domain
  - capability
default_title_attr: display_name
attributes:
  - business_process.owner
  - business_process.tier
  - business_process.domain
  - business_process.capability
  - business_process.lifecycle_status
ui_hints:
  icon: process
  color_token: business.process
  card:
    key_attribute_order:
      - owner
      - tier
      - domain
      - capability
    default_tabs:
      - attributes
      - relations
      - evidence
      - bpmn
search_hints:
  searchable: true
  facetable: true
  filterable_fields:
    - domain
    - tier
    - lifecycle_status
  sortable_fields:
    - display_name
    - last_updated_at
  boost_terms:
    - process
    - процесс
runtime_hints:
  include_in_metamodel_snapshot: true
  include_in_global_search: true
  include_in_registry: true
  rbac_scope: standard
quality_hints:
  requires_owner: true
  requires_evidence: true
  min_required_relations:
    - process_supported_by_system
examples:
  - Открытие расчётного счёта
  - Обработка платежа
notes:
  - BPMN tab показывается только если есть bpmn attachment.
```

## 4. Обязательные поля

### 4.1 Идентичность и человеко-читаемое имя

Обязательные поля:
- `id`
- `name`
- `description`
- `category`
- `layer`
- `status`
- `introduced_in`
- `aliases`
- `attributes`
- `key_attributes`
- `default_title_attr`

Обязательные поля для двуязычного режима:
- `name_ru`

### 4.2 Семантика и эволюция

Обязательные поля:
- `status`
- `introduced_in`

Условно-обязательные:
- `deprecated_in` — обязательно, если `status=deprecated`
- `replaced_by` — обязательно, если kind deprecated и существует прямой successor

### 4.3 Структура и проекция

Обязательные поля:
- `attributes`
- `key_attributes`
- `default_title_attr`
- `ui_hints`
- `search_hints`
- `runtime_hints`

### 4.4 Наследование и инстанцирование

Обязательные поля:
- `abstract`
- `instantiable`

Условно-обязательное:
- `parent_kind` — если kind участвует в inheritance hierarchy

## 5. Семантика полей

### 5.1 `id`
Канонический стабильный идентификатор kind.

Требования:
- lower_snake_case;
- уникален в рамках всей модели;
- не меняется без major-version change;
- используется в relation definitions, runtime catalogs, URN policy, filters и API-ответах metamodel snapshot.

### 5.2 `name` / `name_ru`
Человеко-читаемые названия kind.

Требования:
- `name` — основной display label на EN;
- `name_ru` — основной display label на RU;
- не обязаны быть уникальными как строки, но должны быть семантически различимы в контексте модели;
- не используются как machine ID.

### 5.3 `summary` и `description`
- `summary` — короткая one-line формулировка для registry/list/search hints;
- `description` — нормативное определение сущности.

Требования:
- `description` обязателен;
- definition должна отвечать на вопросы: "что это?", "чем не является?", "какой ролью служит в графе?".

### 5.4 `category`
Укрупнённый семантический класс kind.

Рекомендуемые значения:
- `process`
- `business_object`
- `application`
- `component`
- `resource`
- `data_product`
- `data_object`
- `organization`
- `person_or_role`
- `artifact`
- `link_entity`
- `governance`

Назначение:
- UI grouping;
- registry sections;
- sanity checks на relation patterns;
- search facets.

### 5.5 `layer`
Архитектурный слой сущности.

Рекомендуемые значения:
- `business`
- `data`
- `application`
- `technology`
- `organization`
- `artifact`
- `cross_layer`

Назначение:
- navigation presets;
- faceting;
- impact/use-case slicing;
- minimum slice coverage checks.

### 5.6 `status`
Lifecycle status kind.

Допустимые значения:
- `active`
- `experimental`
- `deprecated`
- `reserved`

Правила:
- `active` — можно использовать в production bundles;
- `experimental` — разрешён только в non-default profile или явно включённом release;
- `deprecated` — допускается в runtime snapshot до removal window;
- `reserved` — ID зарезервирован, но instantiable kind ещё не введён.

### 5.7 `aliases`
Список управляемых синонимов для поиска и миграции терминологии.

Требования:
- aliases не заменяют canonical `id`;
- alias может быть RU/EN;
- alias должен быть нормализуемым для search/disambiguation;
- collision с canonical `id` другого kind запрещён.

### 5.8 `canonical_term`
Явный термин из glossary, если canonical display term отличается от `id`.

Используется для:
- glossary linking;
- semantic disambiguation;
- migration mapping между старой и новой терминологией.

### 5.9 `parent_kind`
Родитель в иерархии kind-ов.

Правила:
- только single inheritance в v2;
- cycles запрещены;
- child наследует базовые structural expectations, но может добавлять свои attributes/hints;
- runtime projection не должен требовать рекурсивного выполнения сложной логики для обычного чтения.

### 5.10 `abstract` и `instantiable`
- `abstract=true` означает, что kind используется для taxonomy/grouping/inheritance и не должен иметь runtime instances;
- `instantiable=true` означает, что ingestion может создавать узлы такого kind.

Правила:
- `abstract=true` и `instantiable=true` одновременно запрещены;
- если `abstract=false`, то `instantiable` должно быть явно задано.

### 5.11 `owned_by_profile`
Список профилей/срезов, в которых kind включён.

Примеры:
- `atlas_mvp`
- `atlas_future`
- `bank_full`

Назначение:
- сборка subset bundles;
- feature gating;
- MVP compatibility checks.

### 5.12 `attributes`
Полный список поддерживаемых attribute IDs для данного kind.

Правила:
- каждый элемент обязан ссылаться на существующий `attribute_def`;
- атрибуты перечисляются через explicit inclusion, не implicit discovery;
- inherited attributes после normalizer могут быть материализованы явно в runtime catalog.

### 5.13 `key_attributes`
Подмножество `attributes`, которое используется как выделенный список для entity card и registry views.

Правила:
- каждый key attribute обязан входить в `attributes`;
- порядок значим;
- число key attributes для MVP желательно держать в диапазоне 3–8;
- отсутствие key attributes допустимо только для крайне технических или link-like kinds.

### 5.14 `default_title_attr`
Атрибут, который является основным полем названия экземпляра kind, если `display_name` не вычисляется отдельно.

Правила:
- должен ссылаться на существующий `attribute_def` этого kind;
- должен быть single-valued и display-safe;
- не должен быть секретным/внутренним identifier-only полем.

### 5.15 `ui_hints`
Набор authoring hints для UI и type catalog.

Рекомендуемые подполя:
- `icon`
- `color_token`
- `card.key_attribute_order`
- `card.default_tabs`
- `registry.default_columns`
- `graph.default_expand_direction`
- `graph.badge_attributes`

Статус:
- это hints, а не hard runtime contract;
- runtime может иметь fallback behavior.

### 5.16 `search_hints`
Набор authoring hints для поиска и registry filtering.

Рекомендуемые подполя:
- `searchable`
- `facetable`
- `filterable_fields`
- `sortable_fields`
- `boost_terms`
- `default_lookup_fields`

Назначение:
- генерация search field metadata;
- disambiguation UX;
- consistency between query semantics and metamodel.

### 5.17 `runtime_hints`
Флаги, влияющие на downstream projection.

Рекомендуемые подполя:
- `include_in_metamodel_snapshot`
- `include_in_global_search`
- `include_in_registry`
- `rbac_scope`
- `exportable_by_default`

### 5.18 `quality_hints`
Authoring-level ожидания качества по kind.

Рекомендуемые подполя:
- `requires_owner`
- `requires_evidence`
- `requires_external_url`
- `min_required_relations`
- `recommended_relations`

Назначение:
- data quality validation;
- demo slice completeness checks;
- golden-question readiness checks.

### 5.19 `examples` и `notes`
Не участвуют в primary runtime contract, но помогают:
- reviewer-ам;
- migration notes;
- glossary quality;
- prompting и documentation.

## 6. Жёсткие инварианты

Любой `entity_kind` должен проходить следующие проверки:

1. `id` уникален глобально.
2. `id` соответствует regex `^[a-z][a-z0-9_]*$`.
3. `name` и `description` непустые.
4. `status` принадлежит допустимому enum.
5. Если `status=deprecated`, то `deprecated_in` обязателен.
6. Если задан `replaced_by`, то такой kind существует.
7. `aliases` не содержат дублей после normalizer.
8. Ни один alias не совпадает с canonical `id` другого kind.
9. `attributes` не содержат дублей.
10. Каждый attribute в `attributes` существует в attribute catalog.
11. Каждый attribute в `key_attributes` входит в `attributes`.
12. `default_title_attr` входит в `attributes`.
13. `default_title_attr` ссылается на single-valued display-safe attribute.
14. Если `abstract=true`, то `instantiable=false`.
15. Если указан `parent_kind`, то родитель существует и не образует cycle.
16. `owned_by_profile` не пуст для instantiable kind, входящих в релиз.
17. `ui_hints.card.default_tabs` не содержит неизвестных tabs.
18. `search_hints.filterable_fields` и `sortable_fields` ссылаются только на существующие attributes.
19. Kind с `include_in_registry=true` обязан иметь хотя бы один title/display strategy.
20. Kind с `requires_owner=true` обязан иметь owner-like attribute или ownership relation в quality rules.

## 7. Рекомендуемые мягкие правила

Это не hard failure, но warning-level lint:
- kind без aliases допустим, но нежелателен для пользовательского домена;
- kind без key attributes ухудшает entity card UX;
- kind без category/layer consistency с relation patterns должен подсвечиваться lint’ом;
- kind без quality/evidence expectations рискован для MVP explainability;
- kind с более чем 25 direct attributes должен рассматриваться как признак скрытого смешения сущностей.

## 8. Что должно попасть в runtime projection

Из authoring `entity_kind` в runtime `type_catalog` и `/v1/meta/model` попадает не всё.

### 8.1 Обязательно в `type_catalog`
- `id`
- `name`
- `name_ru`
- `description`
- `category`
- `layer`
- `status`
- `parent_kind`
- `instantiable`
- `key_attributes`
- `default_title_attr`
- нормализованные `ui_hints`
- нормализованные `search_hints`

### 8.2 Минимально в `/v1/meta/model`
С учётом текущего OpenAPI runtime snapshot может оставаться компактным и содержать:
- `kind`
- `title`
- `description`
- `parent_kind`

При этом downstream type catalog может быть богаче, чем публичный metamodel endpoint.

## 9. Влияние на UI, поиск и traversal

Контракт `entity_kind` обязан обеспечивать:
- выделение key attributes для карточки сущности;
- inline rendering ссылок/URN-полей через attribute metadata следующего шага;
- search facets и sortable fields;
- консистентное поведение фильтра `types` и traversal `allowed_types`;
- корректную работу BPMN tab для `business_process` и будущих process-related kinds.

## 10. Влияние на quality gates и Codex implementation

Из этого контракта должны напрямую следовать:
- JSON Schema / Pydantic model для `entity_kind`;
- lint rules для aliases / inheritance / key attributes;
- generator type catalog;
- warnings для MVP kinds, не готовых к entity card/search/evidence UX;
- compatibility checker для semver.

## 11. Связанные контракты

- [Attribute Definition Contract](attribute_def_contract_v2.md)
- [Qualifier Definition Contract](qualifier_def_contract_v2.md)
- [Glossary и Naming Policy](glossary_alias_naming_policy.md)
- [Relation Kind Contract](relation_kind_contract_v2.md)
