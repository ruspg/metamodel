# Glossary, Alias, and Naming Policy

Дата: 2026-03-09
Статус: frozen-for-wave
Сессия: 12 — правила именования, aliases и glossary model

## 1. Цель

Этот документ фиксирует единые правила именования для ontology schema v2, управляемую модель синонимов и glossary model, чтобы:
- исключить терминологический хаос в `metamodel`;
- обеспечить стабильные machine-readable identifiers;
- поддержать поиск, дизамбигуацию и человеко-читаемый UI в `rbank-atlas`;
- разделить canonical ontology terms, display terms и search aliases.

## 2. Область действия

Политика применяется ко всем authoring-объектам онтологии:
- `entity_kind`
- `relation_kind`
- `attribute_def`
- `qualifier_def`
- glossary entries
- profile ids
- enum ids / enum values, если они вводятся как first-class metadata

Политика не применяется напрямую к runtime instance data, кроме тех мест, где runtime использует:
- metamodel snapshot;
- `display_name`/kind labels;
- search alias materialization;
- filter/sort field references.

## 3. Базовый принцип

Для каждого концепта должны различаться четыре уровня имени:
1. **Canonical ID** — стабильный machine-readable идентификатор.
2. **Canonical term** — основное человеко-читаемое понятие в онтологии.
3. **Display label(s)** — UI-представление, допускающее RU/EN локализацию.
4. **Aliases / synonyms / search forms** — дополнительные формы для поиска и дизамбигуации.

Нельзя смешивать эти уровни в одном поле.

## 4. Naming model по типам объектов

### 4.1 Для `entity_kind`
Обязательные поля именования:
- `id`
- `name_en`
- `name_ru`
- `description`
- `aliases[]`
- `short_label` (опционально)

Рекомендации:
- `id` — основной стабильный идентификатор для схемы, bundle generation и runtime type references.
- `name_en` — canonical ontology term на английском.
- `name_ru` — официальный русскоязычный display/canonical term для UI и glossary.
- `aliases[]` — управляемый список search aliases, не заменяющий canonical terms.
- `short_label` — компактная форма для registry chips / UI, если полное имя длинное.

Пример:
- `id`: `business_process`
- `name_en`: `Business Process`
- `name_ru`: `Бизнес-процесс`
- `aliases`: `["process", "process model", "процесс", "бп"]`

### 4.2 Для `relation_kind`
Обязательные поля именования:
- `id`
- `name_en`
- `name_ru`
- `description`
- `inverse_name_en` / `inverse_name_ru` (если нужно)
- `aliases[]`
- `ui_label_out`
- `ui_label_in`

Рекомендации:
- relation name не должен быть двусмысленным вне контекста.
- UI labels могут отличаться от canonical names, если это улучшает читаемость карточек и графа.
- Inverse label должен быть явно задан, если реверсная формулировка не тривиальна.

Пример:
- `id`: `business_process_supported_by_it_system`
- `name_en`: `Business Process Supported by IT System`
- `name_ru`: `Бизнес-процесс поддерживается ИТ-системой`
- `ui_label_out`: `supported by`
- `ui_label_in`: `supports`

### 4.3 Для `attribute_def`
Обязательные поля именования:
- `id`
- `name_en`
- `name_ru`
- `description`
- `aliases[]` (опционально)

Рекомендации:
- ID атрибута должен отражать бизнес-смысл, а не способ хранения.
- Не использовать source-specific naming внутри canonical attribute ids.
- Для common attributes допускается namespace-префикс только при реальной необходимости избежать конфликта.

Примеры:
- `owner_team_id`
- `lifecycle_status`
- `freshness_sla`
- `external_url`

### 4.4 Для `qualifier_def`
Обязательные поля именования:
- `id`
- `name_en`
- `name_ru`
- `description`

Qualifier naming должен делать понятным, что значение относится к **связи**, а не к сущности.

Примеры:
- `interaction_channel`
- `contract_id`
- `evidence_strength`
- `ownership_role`

## 5. Правила для canonical IDs

### 5.1 Общие правила
Canonical IDs должны быть:
- стабильными;
- ASCII-only;
- lowercase;
- в `snake_case`;
- без пробелов, дефисов, camelCase и локализованных символов;
- уникальными в своей namespace-группе.

Разрешённый паттерн:
- `^[a-z][a-z0-9_]*$`

### 5.2 Запрещённые практики
Нельзя:
- использовать пробелы;
- использовать русские буквы в ID;
- кодировать версию в ID;
- использовать слишком общие IDs вроде `process`, `entity`, `link`, `item`;
- использовать source-specific IDs вроде `cmdb_app`, `jira_process`, если речь о canonical ontology concept.

### 5.3 Правила по длине
Рекомендации:
- target length для `kind id`: 8–48 символов;
- target length для `attribute id`: 5–48 символов;
- target length для `relation id`: 16–96 символов;
- избегать чрезмерно длинных цепочек из 5+ смысловых токенов, если можно упростить без потери смысла.

### 5.4 Семантика relation IDs
Relation IDs должны быть:
- ориентированы на смысл, а не на UI wording;
- достаточно явными без внешнего контекста;
- пригодными для inverse/reference semantics.

Предпочтительная форма:
- `<src>_<verb_phrase>_<dst>`

Примеры:
- `business_process_supported_by_it_system`
- `data_product_contains_data_table`
- `component_deployed_on_logical_resource`

## 6. Правила для canonical terms и display labels

### 6.1 Canonical term
Canonical term — это официальное понятие, используемое в glossary и design discussions.

Правила:
- один canonical term на язык;
- термины должны быть предметно точными, а не удобными жаргонными сокращениями;
- canonical term не должен меняться без formal change decision.

### 6.2 Display label
Display label — это UI-форма имени, допускающая упрощение.

Правила:
- допускаются короткие формы для UI;
- display label может отличаться от canonical term только по readability, а не по смыслу;
- display label должен оставаться однозначным в registry/card/filter контексте.

Пример:
- canonical term RU: `Организационная единица`
- display label RU: `Подразделение`

Если возникает смысловая потеря, short label запрещён.

## 7. RU/EN naming strategy

### 7.1 Язык канона
- **Machine-readable canon**: English-based IDs.
- **Human-readable canon**: обязательны обе формы — `name_en` и `name_ru`.
- В спорных случаях source of truth для семантики — ontology definition, а не буквальный перевод термина.

### 7.2 Политика перевода
Правила:
- переводить смысл, а не слово в слово;
- не держать английский термин в `name_ru`, если есть хороший русский эквивалент;
- допускается сохранить английское заимствование в `aliases`, если оно реально используется командами;
- если в русском нет устойчивого эквивалента, canonical RU term должен быть выбран осознанно и закреплён glossary note.

Примеры:
- `business capability` → `Бизнес-способность` неудачно; предпочтительно `Бизнес-возможность` или `Бизнес-способность` только после отдельного semantic decision.
- `value stream` не должен автоматически превращаться в произвольные варианты вроде `поток ценности`, `цепочка ценности`, `value stream` без glossary resolution.

### 7.3 Mixed-language policy
Запрещено:
- смешивать RU и EN в одном canonical display поле;
- использовать случайные транслитерации как canonical labels;
- делать `name_ru` простым дублем `name_en`, если русский термин ожидается в UI.

Допускается:
- держать англоязычные и транслитерированные формы в `aliases`.

## 8. Alias policy

### 8.1 Что такое alias
Alias — это управляемая альтернативная форма referential/search usage.

Alias может быть:
- синонимом;
- сокращением;
- историческим названием;
- распространённым жаргонным названием;
- англоязычной или русскоязычной альтернативой;
- формой для поиска с/без дефиса, аббревиатурой, plural/singular variant.

### 8.2 Что не является alias
Не считать alias:
- source-specific external IDs;
- typo inventory без подтверждённой пользы;
- целые длинные описания;
- значения instance data;
- автоматически сгенерированные морфологические формы без контроля.

### 8.3 Классы aliases
Рекомендуемые типы aliases:
- `synonym`
- `abbreviation`
- `legacy_name`
- `search_form`
- `translation_variant`
- `transliteration_variant`

Рекомендуемая структура alias entry:
- `value`
- `lang` (`ru` / `en` / `neutral`)
- `alias_type`
- `status` (`active` / `deprecated`)
- `notes` (опционально)

### 8.4 Инварианты alias policy
- alias не должен конфликтовать с canonical term другого P0 kind без disambiguation note;
- deprecated alias не удаляется сразу, если он нужен для search compatibility;
- alias должен ссылаться ровно на один canonical concept внутри одного active profile;
- одинаковый alias для нескольких concepts допускается только при явной дизамбигуации search layer.

### 8.5 Alias budget
Чтобы не раздувать словари:
- для P0 kinds: обычно 2–8 aliases;
- для relations: обычно 0–4 aliases + UI labels;
- для attributes: обычно 0–3 aliases.

Если aliases больше, чем canonical design реально требует, нужен review.

## 9. Glossary model

### 9.1 Назначение glossary
Glossary нужен не для красивого словаря, а как:
- semantic source of truth для понятий;
- база для RU/EN alignment;
- база для search/disambiguation hints;
- опора для review новых kinds/relations.

### 9.2 Glossary entry
Каждый glossary entry должен включать:
- `term_id`
- `canonical_name_en`
- `canonical_name_ru`
- `definition`
- `scope_notes`
- `non_examples`
- `aliases[]`
- `related_terms[]`
- `status`
- `introduced_in`
- `deprecated_in` (опционально)

### 9.3 Когда нужен glossary entry
Обязателен для:
- всех P0/P1 entity kinds;
- всех relations бизнес-слоя;
- спорных атрибутов и qualifiers;
- терминов, у которых есть как минимум один semantic overlap risk.

Опционален для:
- простых технических атрибутов (`external_url`, `last_seen_at` и т.п.), если смысл однозначен.

### 9.4 Canonical term vs glossary entry
- `entity_kind.name_*` задаёт официальное имя kind.
- glossary entry даёт определение, границы и различия.
- один kind обычно имеет один glossary entry.
- glossary entry может существовать и для термина, который пока не materialized как kind, если он нужен для semantic guardrails.

## 10. Search normalization rules

### 10.1 Цель
Search normalization должна помогать поиску и дизамбигуации, но не переписывать семантику онтологии.

### 10.2 Нормализация на уровне индекса/search aliases
Разрешено:
- lowercase normalization;
- trim / collapse whitespace;
- hyphen/underscore/space equivalence;
- punctuation stripping для search-only tokenization;
- singular/plural normalization для EN, если реализуется контролируемо;
- базовая нормализация сокращений;
- нормализация распространённых RU/EN вариантов.

### 10.3 Нормализация, которую нельзя использовать как ontology truth
Нельзя делать canonical alias policy зависимой только от search-engine heuristics:
- агрессивный stemming;
- неконтролируемая лемматизация;
- автоматическое объединение омонимов;
- бесконтрольная транслитерация всего словаря.

Эти вещи допустимы только как search-layer feature, не как authoring truth.

### 10.4 Источники search forms
Search layer должен materialize candidate terms из:
- `name_en`
- `name_ru`
- `short_label`
- active `aliases`
- selected relation UI labels
- explicit glossary search forms

### 10.5 Disambiguation hints
Если alias пересекается у нескольких concepts, glossary/search model должен поддерживать:
- `disambiguation_note`
- preferred contexts / layer hints
- entity kind priority hints

Пример:
- `process` может указывать на `business_process`, но не должен автоматически подменять `process model`, `workflow`, `BPMN process` без контекста.

## 11. Anti-patterns

Нельзя:
- делать canonical IDs по названиям source systems;
- использовать один и тот же термин для kind и relation в одинаковой форме;
- смешивать instance names и ontology terms;
- использовать UI short labels как canonical names;
- складывать в aliases всё, что когда-либо кто-то говорил;
- менять canonical name только ради косметики UI;
- скрывать semantic ambiguity через “ну будем искать по всему”.

## 12. Рекомендуемая структура в authoring repo

Рекомендуется завести:
- `model/glossary/*.yaml`
- `model/kinds/*.yaml`
- `model/relations/*.yaml`
- `model/attributes/*.yaml`
- `model/qualifiers/*.yaml`
- `model/dictionaries/aliases.yaml` (только если нужен shared dictionary)

Glossary не должен быть buried inside free-form docs only; он должен быть машиночитаемым.

## 13. Обязательные проверки для будущих валидаторов

Валидаторы должны проверять:
- формат `id`;
- уникальность IDs;
- наличие `name_en` и `name_ru`;
- отсутствие пустых canonical terms;
- отсутствие alias duplication без explicit disambiguation;
- отсутствие `short_label`, который конфликтует с другим active label в том же profile;
- соответствие glossary entry canonical term;
- запрет deprecated alias как единственной активной search form;
- отсутствие source-specific naming leaks в canonical fields.

## 14. Решения по умолчанию

До появления специальных исключений действуют следующие default decisions:
- canonical IDs всегда на английском и в `snake_case`;
- canonical human-readable labels поддерживаются в RU и EN;
- glossary entry обязателен для всех P0 kinds;
- aliases управляются вручную, а не генерируются бесконтрольно;
- transliteration forms допускаются только как aliases;
- display labels могут быть короче canonical terms, но не должны менять смысл;
- search normalization живёт в search-layer/runtime projection, а не в canonical ontology identity.

## 15. Выходы этой сессии

Этот документ должен использоваться как вход для:
- semantic alignment бизнес-слоя;
- ontology authoring structure;
- atlas projection bundle (`search_aliases.json`);
- quality gates / ontology lint rules;
- Codex tasks на validators и generators.

## 16. Критерий завершения

Сессию можно считать завершённой, если:
- каждый `kind`, `relation`, `attribute`, `qualifier` имеет canonical naming model;
- glossary и aliases отделены от display/UI labels;
- RU/EN strategy и search normalization policy определены;
- команда может добавлять новые термины без стихийных naming decisions.
