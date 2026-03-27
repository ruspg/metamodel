# ADR: business_operation как first-class entity kind

> Architectural Decision Record: включение `business_operation` в онтологию.

## 1. Контекст

В бизнес-слое оставался критический semantic gap между:
- `business_process` как end-to-end или регламентным потоком;
- `business_function` как устойчивой функцией/зоной ответственности;
- BPMN `activity/task` как исполняемым шагом процесса.

Без отдельного решения по `business_operation` возникают три системные проблемы:
1. BPMN activity не имеет корректной целевой сущности для маппинга.
2. В process-centric traversal смешиваются «что делаем в процессе» и «за что отвечает функция».
3. Impact analysis либо слишком грубый, либо опирается на ad hoc связи напрямую от процесса к системам и данным.

## 2. Решение

### 2.1 Основное решение

`business_operation` принимается как **first-class entity kind** в ontology schema v2 и в atlas-ready runtime projection.

Это обязательный тип для process-centric модели, а не future-state расширение.

### 2.2 Каноническое определение

`business_operation` — это **исполняемый, предметно осмысленный шаг бизнес-процесса**, который:
- имеет бизнес-цель в рамках конкретного процесса или процессного контекста;
- может быть соотнесён с BPMN activity/task;
- связывает процессный слой с функциями, системами, данными и бизнес-сущностями;
- является достаточно атомарным для impact/path/context analysis, но не обязан быть micro-step уровня UI-click.

Иными словами:
- `business_process` отвечает на вопрос **«какой поток/сценарий выполняется end-to-end?»**
- `business_function` отвечает на вопрос **«какая устойчивая бизнес-функция/область ответственности выполняется?»**
- `business_operation` отвечает на вопрос **«какой конкретный исполняемый шаг совершается внутри процесса?»**

## 3. Что `business_operation` НЕ является

`business_operation` не является:
- синонимом `business_function`;
- полным process instance или execution log событием;
- техническим API-вызовом или системной командой;
- чисто UI-действием пользователя;
- BPMN XML-элементом как таковым.

BPMN activity — это артефактная/нотационная проекция, а `business_operation` — канонический графовый бизнес-узел.

## 4. Почему выбран именно этот вариант

### 4.1 Выбранный вариант

Выбран вариант:
- `business_operation` как first-class kind;
- BPMN activity/task по умолчанию маппится именно на `business_operation`;
- `business_function` сохраняется как отдельный, более устойчивый semantic layer.

### 4.2 Почему не выбран вариант «activity -> business_function»

Вариант отклонён, потому что он:
- смешивает устойчивую функциональную ответственность и исполняемый шаг;
- ухудшает explainability в BPMN portal;
- ведёт к слишком крупнозернистому impact analysis;
- затрудняет точное связывание шага процесса с системами, данными и бизнес-сущностями.

### 4.3 Почему не выбран вариант «без business_operation в MVP»

Вариант отклонён, потому что он:
- оставляет semantic debt в самом центре process layer;
- заставляет кодировать неявную логику в ingestion/UI/API;
- позже делает миграцию дороже, чем принятие решения сейчас.

## 5. Отношение к BPMN

### 5.1 Primary mapping rule

Для MVP и целевого состояния правило такое:

**BPMN activity/task -> `business_operation`**

Если одна activity слишком крупная, допускается:
- временный mapping activity -> 1 `business_operation`,
- а finer-grained decomposition оставляется на P1/P2.

Если activity является чисто технической или orchestration-only и не имеет самостоятельного бизнес-смысла, допускается:
- не создавать отдельный `business_operation`,
- а пометить activity как unmapped / technical / ignored-by-business-layer по policy ingestion.

### 5.2 Secondary mapping rule

`business_operation` может дополнительно связываться с:
- `business_function`, которую операция реализует или в рамках которой выполняется;
- `it_system` / `component`, которые её поддерживают;
- `business_entity`, над которой совершается действие;
- `information_flow` или data-layer сущностями, если операция читает/создаёт/передаёт данные.

### 5.3 BPMN artifact boundary

BPMN XML, diagram metadata и activity ids остаются artifact/evidence layer.
Каноническая семантика шага живёт не в XML, а в `business_operation`.

## 6. Положение `business_operation` в целевой бизнес-цепочке

Нормализованная процессная цепочка для MVP:

`value_stream` -> `value_stream_stage` -> `business_process` -> `business_operation` -> `business_function`

С дополнительными поперечными связями:
- `business_operation` -> `business_entity`
- `business_operation` -> `information_flow`
- `business_operation` -> `it_system`
- `business_operation` -> `component`
- `business_operation` -> `data_product` / `data_table` / `topic` (по необходимости)

## 7. Traversal и impact semantics

### 7.1 Роль в traversal

`business_operation` должен быть **видимым и traversable** в process-centric графе.

Обязательные сценарии traversal:
- process -> operations;
- operation -> function;
- operation -> systems/components;
- operation -> business entities;
- operation -> data artifacts / information flows.

### 7.2 Роль в impact analysis

`business_operation` должен участвовать в impact analysis как промежуточный semantic bridge:
- при impact от процесса вниз к системам и данным;
- при impact от системы вверх к операциям и процессам;
- при BPMN activity context resolution.

### 7.3 UI / graph density rule

В MVP `business_operation` является частью канонического подграфа, но UI может:
- скрывать операции по умолчанию в некоторых high-level обзорах;
- раскрывать их в process/BPMN mode и в focused exploration.

То есть **наличие в модели обязательно**, а **визуальная детализация может быть режимной**.

## 8. Обязательные атрибуты `business_operation` для MVP

Минимально обязательные поля:
- `id`
- `name`
- `name_ru`
- `description`
- `status`
- `aliases[]`
- `process_local_code` или иной стабильный локальный ключ
- `default_title_attr = name`
- `key_attributes`
- `criticality` (enum, optional-but-recommended)
- `automation_level` (manual / assisted / automated, optional-but-recommended)
- `actor_role` (optional)
- `trigger` (optional)
- `outcome` (optional)
- `ui_hints`
- `search_hints`

### 8.1 Что не требуем в MVP как mandatory

Не делаем обязательными на MVP:
- SLA-поля;
- execution frequency;
- control evidence at field level;
- full RACI;
- detailed cost metrics.

Это остаётся P1/P2 enrichment.

## 9. Обязательные связи `business_operation` для MVP

### 9.1 P0 mandatory relations

Для `business_operation` обязательны следующие relation families:
1. `business_process` -> `business_operation`
2. `business_operation` -> `business_function`
3. `business_operation` -> (`it_system` or `component`) — когда операция автоматизирована или поддерживается ИТ

### 9.2 P0 highly recommended relations

Сильно рекомендуемые для MVP:
- `business_operation` -> `business_entity`
- `business_operation` -> `information_flow`
- `business_operation` -> `team` / `organizational_unit` через owner/performer semantics

### 9.3 P1/P2 relations

Можно отложить:
- `business_operation` -> `data_product`
- `business_operation` -> `data_table`
- `business_operation` -> `topic`
- `business_operation` -> `risk/control/policy`-related kinds

## 10. Политика гранулярности

`business_operation` должна быть:
- достаточно конкретной, чтобы соответствовать meaningful process step;
- достаточно устойчивой, чтобы не зависеть от случайной нотации диаграммы;
- не слишком мелкой, чтобы граф не превращался в event log.

Практическое правило MVP:
- одна операция соответствует одному осмысленному business step,
- обычно это 1:1 с BPMN task/activity,
- но допускается controlled many-to-one или one-to-many mapping с явной пометкой в BPMN layer.

## 11. Ingestion и source mapping consequences

Принятое решение требует следующих изменений в downstream preparation:

1. `business_operation` должен появиться в ontology schema v2 и в MVP subset.
2. BPMN source mapping должен ориентироваться на `activity -> business_operation`, а не `activity -> business_function` как дефолт.
3. CSV/Excel bootstrap должен при необходимости уметь поставлять операции для pilot slice.
4. BPMN import layer должен уметь хранить unmapped activities отдельно от канонических operations.
5. Relation matrix бизнес-слоя должна включить process-operation-function chain как обязательную опорную сеть.

## 12. Runtime и API consequences

Это решение влияет на runtime следующим образом:
- `/v1/bpmn/activities/{activity_urn}/context` должен разрешать activity в graph context через связанный `business_operation`;
- entity card для `business_process` и BPMN tab должны уметь показывать mapping activity -> operation;
- paths/impact/export должны уметь включать `business_operation` в подграф без специальной ad hoc логики.

## 13. UI consequences

### 13.1 Entity card

Для `business_operation` должна быть полноценная карточка сущности с:
- ключевыми атрибутами;
- relations tabs;
- evidence tab;
- links на process/function/system/data context.

### 13.2 BPMN UX

В BPMN viewer activity context должен объясняться через mapped operation, а не напрямую через function-only view.
Это делает UX более понятным: пользователь видит не просто «функцию», а конкретный шаг процесса и его downstream context.

## 14. Anti-patterns, которые теперь запрещены

Запрещаются следующие модели:
1. Использовать `business_function` как универсальную замену каждому шагу процесса.
2. Связывать каждый `business_process` напрямую со всеми системами без промежуточного operation layer там, где нужен process context.
3. Считать BPMN activity канонической бизнес-сущностью без graph-level нормализации.
4. Использовать `business_operation` для технических orchestration-only шагов без самостоятельного бизнес-смысла.
5. Делать гранулярность operations настолько мелкой, что они становятся логом, а не моделью.

## 15. Итоговое решение в одной формуле

Для MVP и future-state принимается правило:

**`business_operation` — обязательный first-class узел процессного слоя; BPMN activity/task по умолчанию маппится на `business_operation`; `business_function` остаётся отдельным, более устойчивым semantic layer.**

## 16. Связанные контракты

- [Business Layer Semantic Alignment](../architecture/business_layer_semantic_alignment.md)
- [Business Layer Relation Matrix](../architecture/business_layer_relation_matrix.md)
- [Entity Kind Contract](../architecture/entity_kind_contract_v2.md)
