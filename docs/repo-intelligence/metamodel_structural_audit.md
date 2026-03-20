# Structural Audit — `metamodel` repo

Дата: 2026-03-09

## 1. Цель
Этот артефакт фиксирует текущее состояние репозитория `metamodel` как базы для ontology-as-code и оценивает, что можно переиспользовать для интеграции с `rbank-atlas`, а что потребует переработки.

## 2. Краткий вывод
`metamodel` уже является **полезным seed-репозиторием онтологии**, но в текущем виде это **authoring + visualization/tooling repo**, а не atlas-ready upstream release repo.

Сильные стороны:
- есть живая предметная модель в YAML;
- есть формальная JSON Schema;
- есть CLI-конвертер в OWL;
- есть отдельный Mermaid pipeline;
- есть базовые тесты на преобразование и валидацию.

Критические ограничения:
- онтология хранится в виде **монолитных YAML-файлов**, а не как разложенные versioned contracts;
- схема слишком свободная для runtime-контракта;
- почти отсутствует runtime-ориентированная семантика связей;
- нет release bundle для `rbank-atlas`;
- нет compatibility / semver / deprecation модели;
- нет atlas projection artifacts и import-facing формы.

## 3. Что реально есть в репозитории сейчас

### 3.1 Структура репозитория
На верхнем уровне есть:
- `data/`
- `docs/`
- `metamodel2owl/`
- `metamodel_to_mermaid/`
- `schema/`
- `tests/`
- `README.md`
- `pyproject.toml`
- `setup.cfg`

### 3.2 Authoring data
В `data/` лежат два YAML-файла:
- `enterprise_metamodel.yaml`
- `bank_metamodel_horizontal.yaml`

#### `enterprise_metamodel.yaml`
- meta.model_name: `enterprise_metamodel`
- last_updated: `2025-11-16`
- entity kinds: **66**
- relation kinds: **58**
- attributes total: **239**
- dictionaries: **['metamodel_levels']**
- покрытые уровни: **['business_details', 'component_details', 'data_details', 'infrastructure_details', 'solution_details', 'strategic_view']**

Проверка наличия ключевых atlas/MVP типов:
{
  "value_stream": true,
  "value_stream_stage": true,
  "business_capability": true,
  "business_process": true,
  "business_operation": false,
  "business_function": true,
  "business_entity": true,
  "information_flow": true,
  "data_product": true,
  "data_table": true,
  "topic": true,
  "it_system": true,
  "component": true,
  "logical_resource": true,
  "infrastructure_resource": true,
  "team": true,
  "organizational_unit": true
}

Ключевое наблюдение: нужные P0 типы в целом уже присутствуют, но **`business_operation` отсутствует**.

#### `bank_metamodel_horizontal.yaml`
- meta.model_name: `bank_metamodel_horizontal`
- last_updated: `2025-01-14`
- entity kinds: **25**
- relation kinds: **36**
- attributes total: **1**
- dictionaries: **['metamodel_levels', 'relationship_archetypes']**

Интерпретация:
- `enterprise_metamodel.yaml` уже играет роль основной модели;
- `bank_metamodel_horizontal.yaml` выглядит как более ранний или более узкий горизонтальный срез / сценарный seed.

### 3.3 Формат и схема
Есть JSON Schema `model/schema/metamodel.schema.yaml`.

Обязательные корневые секции:
- `meta`
- `dictionaries`
- `entity_kinds`
- `relation_kinds`

Обязательные поля:
- для `entity_kind`: `['id', 'name', 'metamodel_level', 'category']`
- для `relation_kind`: `['id', 'name', 'from_kind', 'to_kind', 'metamodel_level', 'category', 'direction']`
- для `attribute`: `['id', 'name', 'metamodel_level']`

Важное наблюдение:
- `entity_kind.additionalProperties = True`
- `relation_kind.additionalProperties = True`
- `attribute.properties` допускает произвольный словарь
- schema почти не ограничивает semantics/runtime hints

Это удобно для authoring-гибкости, но недостаточно для контрактного upstream-репозитория.

### 3.4 Документация
Есть два полезных документа:
- `docs/metamodel_yaml_format.md`
- `docs/metamodel_contribution_rules.md`

Они фиксируют:
- целевой YAML-формат;
- шесть уровней Operational Metamodel;
- базовые правила по идентификаторам и review;
- ручные проверки schema/duplicates/reference integrity.

### 3.5 Tooling
Есть два tool-chain слоя:

#### A. OWL converter
Пакет `metamodel2owl`:
- `cli.py`
- вложенная `schema/`
- console entrypoint `metamodel2owl`

Что делает:
- читает YAML;
- валидирует его по JSON Schema;
- конвертирует в OWL/RDF;
- умеет выдавать Mermaid diagram как побочный output;
- маппит primitive datatypes в XSD.

#### B. Mermaid converter
Отдельный пакет `metamodel_to_mermaid`:
- `cli.py`
- `loader.py`
- `model.py`
- `render_er.py`
- `render_flow.py`
- `styles.py`

Что делает:
- строит internal model из YAML;
- фильтрует по `view` (`all`, `strategic`, `business`, `solution`, `data`, `infra`, `horizontal`);
- генерирует Mermaid flow/ER diagrams.

### 3.6 Packaging
Packaging сейчас завязан в основном на `metamodel2owl`:
- package name: `metamodel2owl`
- version: `0.1.0`
- console entrypoint: `metamodel2owl = metamodel2owl.cli:main`

Это важный сигнал: репозиторий сейчас позиционируется скорее как converter package, чем как ontology release product.

### 3.7 Tests
Есть:
- `tests/conftest.py`
- `tests/test_cli.py`
- fixtures: `minimal.yaml`, `invalid_missing_required.yaml`

Судя по тестам, покрыты:
- минимальная успешная конверсия;
- ошибки schema validation;
- datatype/cardinality mapping;
- enums / levels / skos tags;
- deterministic serialization;
- mermaid generation.

Интерпретация:
- tests проверяют **CLI conversion correctness**;
- tests не проверяют ontology governance, semantic conflicts, release compatibility и atlas projection.

## 4. Что можно переиспользовать без большого redesign

### 4.1 Reuse zone A — сама YAML-модель
Это главный актив. Уже есть:
- нормальный набор базовых сущностей;
- описания сущностей;
- метамодельные уровни;
- значимая часть relation seeds;
- достаточное покрытие для старта ontology v2 migration.

### 4.2 Reuse zone B — JSON Schema как стартовая база
Текущая schema годится как основа для:
- backward-compatible reading старых файлов;
- migration validator;
- bootstrap для ontology schema v2.

Но её недостаточно оставлять как конечную target schema.

### 4.3 Reuse zone C — OWL pipeline
`metamodel2owl` полезен как:
- secondary export path;
- research/interop output;
- тест на консистентность ontology authoring.

Но не должен быть центром продукта.

### 4.4 Reuse zone D — Mermaid pipeline
Mermaid tooling полезно оставить для:
- human review;
- docs;
- quick visual checks;
- design reviews.

Это хороший companion tool, но не runtime contract.

### 4.5 Reuse zone E — contribution docs
Rules/docs можно переиспользовать как основу:
- authoring discipline;
- naming conventions;
- PR hygiene;
- schema validation habits.

## 5. Главные пробелы относительно `rbank-atlas`

### 5.1 Нет atlas-ready release bundle
Сейчас отсутствуют:
- `metamodel_snapshot.json`
- `type_catalog.json`
- `relation_catalog.json`
- `search_aliases.json`
- `compatibility_report.md`
- versioned release semantics

### 5.2 Нет нормальной decomposition структуры authoring ontology
Сейчас модель живёт в 1–2 больших YAML.
Для atlas-ready upstream repo нужны:
- `model/schema/`
- `model/kinds/*.yaml`
- `model/relations/*.yaml`
- `model/glossary/*.yaml`
- `profiles/*.yaml`
- `generated/atlas/*`

### 5.3 Схема слишком permissive
Current schema:
- почти не типизирует runtime hints;
- не требует aliases/synonyms;
- не требует lifecycle/deprecation;
- не требует attribute data types как строгого контракта;
- не требует inverse/cardinality/qualifier semantics для relations;
- не различает authoring fields и runtime-projection fields.

### 5.4 Relation catalog слишком слабый
В `enterprise_metamodel.yaml`:
- relation keys фактически ограничены `['category', 'description', 'direction', 'from_kind', 'id', 'metamodel_level', 'name', 'to_kind']`
- descriptions есть только у **5 из 58** relation kinds
- rules / cardinality / inverse / qualifier schema практически отсутствуют

Для atlas это критичный пробел, потому что графовые traversal/path/impact/export/MCP сценарии зависят от качественного relation contract.

### 5.5 Attribute model недоопределён
В `enterprise_metamodel.yaml`:
- attribute keys: `['description', 'id', 'metamodel_level', 'name']`
- у атрибутов фактически есть только id/name/metamodel_level/description
- нет системного `data_type`, `cardinality`, `required`, `enum`, `ref_kind`, `searchable`, `filterable`

Это не годится как runtime-oriented metamodel.

### 5.6 Нет explicit semantic layer для business/process depth
Хотя есть:
- `value_stream`
- `value_stream_stage`
- `business_capability`
- `business_process`
- `business_function`
- `business_entity`

нет `business_operation`, а именно он нужен для более честного BPMN/activity mapping в atlas.

### 5.7 Нет ontology governance уровня release product
Отсутствуют:
- semver/compatibility policy;
- deprecation workflow;
- compatibility tests между версиями;
- release notes discipline;
- pinned import interface для downstream repo.

### 5.8 Нет source-to-ontology alignment
Репозиторий не знает:
- какие source namespaces допустимы;
- какие kinds реально ingested;
- какие relations являются P0/P1/P2;
- как ontology projection соотносится с runtime source mapping atlas.

Это правильно как separation of concerns, но нужен atlas projection contract, чтобы стык между репозиториями стал формальным.

## 6. Technical debt и risk map

### 6.1 Low-risk reuse
- YAML seed content
- docs
- базовая schema
- OWL/Mermaid converters
- CLI tests

### 6.2 Medium redesign
- packaging
- repo layout
- authoring decomposition
- richer validation/linting
- stricter schema evolution

### 6.3 Full redesign required
- release bundle model
- atlas projection
- compatibility/semver policy
- relation catalog v2
- attribute model v2
- import-facing contracts
- ontology quality gates

## 7. Архитектурное решение по репозиторию
Рекомендованная роль `metamodel`:

**Не** “репозиторий с YAML и конвертером в OWL”.

**Да** — upstream ontology release repo, который:
1. хранит conceptual ontology;
2. валидирует её;
3. версионирует изменения;
4. строит normalized ontology;
5. выпускает atlas-ready release bundle;
6. дополнительно умеет экспортировать OWL/Mermaid.

## 8. Практический вывод для следующей волны
После этого аудита следующий правильный шаг — не рефакторить код сразу, а зафиксировать:
1. structural audit `rbank-atlas`;
2. upstream/downstream operating contract;
3. ontology schema v2;
4. relation catalog v2;
5. atlas projection bundle spec.

Только после этого стоит резать Codex backlog на реальную реализацию.

## 9. Вердикт
`metamodel` стоит **эволюционно переработать**, а не выбрасывать.

Правильная стратегия:
- сохранить существующие YAML как migration seed;
- сохранить OWL/Mermaid как secondary outputs;
- перестроить repo вокруг ontology schema v2 + release bundle + validation/release CI;
- сделать `rbank-atlas` потребителем versioned snapshot, а не сырых YAML.
