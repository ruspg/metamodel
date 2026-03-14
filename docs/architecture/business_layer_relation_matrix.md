# Сессия 15 — Business-Layer Relation Matrix

## Статус
- Статус: frozen-for-wave
- Волна: Wave 3 — семантика бизнес-слоя и relation model
- Основание: после semantic alignment бизнес-слоя и formal decision по `business_operation`
- Назначение: зафиксировать минимальную опорную сеть бизнес-смысла для MVP и ближайшего расширения без смысловой неоднозначности

---

## 1) Цель

Этот артефакт фиксирует:
- какие связи между бизнес-сущностями **обязательны** для MVP;
- какие связи **допустимы, но не обязательны**;
- какие связи относятся к **P1/P2**;
- какие связи нужно моделировать как **direct edges**;
- где допустимы или желательны **qualified edges**;
- какие связи считаются **недопустимыми** на уровне бизнес-слоя.

Главный принцип: бизнес-слой должен давать **минимальную, но сильную сеть смыслов**, пригодную для поиска, entity card, bounded traversal, impact, BPMN portal и экспорта подграфа.

---

## 2) Business-layer scope

В scope этой матрицы входят следующие kinds:
- `value_stream`
- `value_stream_stage`
- `business_capability`
- `business_process`
- `business_operation`
- `business_function`
- `business_entity`
- `information_flow`

Не входят в эту матрицу, но будут связаны с ней в соседних слоях:
- `it_system`, `functional_subsystem`, `component`
- `data_product`, `data_table`, `topic`
- `team`, `organizational_unit`
- BPMN artifacts / activity artifacts

---

## 3) Нормативная цепочка смыслов

Базовая опорная цепочка бизнес-слоя:

`value_stream -> value_stream_stage -> business_process -> business_operation -> business_function`

Дополнительные опорные связи:
- `business_capability -> business_process`
- `business_process -> business_entity`
- `business_operation -> business_entity`
- `information_flow -> business_entity`
- `business_process -> information_flow`

Смысл этой цепочки:
- **value stream** отвечает на вопрос, какую end-to-end ценность создаём;
- **stage** — в какой стадии жизненного цикла ценности находится работа;
- **process** — какой управляемый поток её реализует;
- **operation** — какой исполняемый шаг выполняется внутри процесса;
- **function** — какая устойчиво определённая бизнес-работа выполняется этим шагом.

---

## 4) Уровни приоритета

### P0
Связи, без которых MVP теряет объяснимость, BPMN-контекст или core traversal usefulness.

### P1
Связи, которые сильно улучшают анализ, impact и governance, но не обязательны для первого демонстрируемого вертикального среза.

### P2
Future-state расширения, полезные для более богатой навигации, lineage business logic и advanced governance.

---

## 5) Relation matrix

| Relation ID | Src | Dst | Priority | MVP Status | Modeling | Recommended qualifiers | Назначение |
|---|---|---:|---:|---|---|---|---|
| `rel_value_stream_contains_stage` | `value_stream` | `value_stream_stage` | P0 | mandatory | direct edge | optional: `order_index` | Разбивка value stream на стадии |
| `rel_stage_realized_by_process` | `value_stream_stage` | `business_process` | P0 | mandatory | direct edge | optional: `role`, `criticality` | Привязка процессов к стадии value stream |
| `rel_capability_aggregates_processes` | `business_capability` | `business_process` | P0 | mandatory | direct edge | optional: `strength`, `scope` | Показывает, какие процессы реализуют capability |
| `rel_process_decomposes_to_operation` | `business_process` | `business_operation` | P0 | mandatory | direct edge | optional: `sequence_group`, `optional_flag` | Основная процессная декомпозиция |
| `rel_operation_executes_function` | `business_operation` | `business_function` | P0 | mandatory | direct edge | optional: `mode`, `automation_level` | Разводит шаг исполнения и устойчивую функцию |
| `rel_process_serves_entity` | `business_process` | `business_entity` | P0 | mandatory | direct edge | optional: `role` (`creates/reads/updates/terminates`) | Какие бизнес-сущности обслуживает процесс |
| `rel_operation_acts_on_entity` | `business_operation` | `business_entity` | P0 | mandatory | qualified edge | `interaction_type`, `criticality`, `mandatory` | На каком объекте выполняется шаг |
| `rel_information_flow_carries_entity` | `information_flow` | `business_entity` | P0 | mandatory | qualified edge | `payload_role`, `sensitivity` | Что именно несёт поток информации |
| `rel_process_uses_information_flow` | `business_process` | `information_flow` | P1 | recommended | direct edge | optional: `role`, `frequency` | Процесс использует/порождает поток информации |
| `rel_operation_uses_information_flow` | `business_operation` | `information_flow` | P1 | recommended | qualified edge | `interaction_type`, `directionality` | Шаг опирается на конкретный инфопоток |
| `rel_stage_supported_by_capability` | `value_stream_stage` | `business_capability` | P1 | optional | direct edge | optional: `strength` | Уточняет capability coverage на уровне стадии |
| `rel_capability_supported_by_function` | `business_capability` | `business_function` | P1 | optional | direct edge | optional: `strength`, `scope` | Соединяет capability и устойчивые функции |
| `rel_process_depends_on_process` | `business_process` | `business_process` | P1 | optional | qualified edge | `dependency_type`, `criticality`, `sla_hint` | Межпроцессные зависимости |
| `rel_operation_precedes_operation` | `business_operation` | `business_operation` | P1 | optional | qualified edge | `condition`, `branch_type`, `order_index` | Локальная последовательность операций |
| `rel_entity_relates_to_entity` | `business_entity` | `business_entity` | P1 | optional | qualified edge | `relation_role`, `cardinality_hint` | Семантические связи между бизнес-объектами |
| `rel_value_stream_supported_by_capability` | `value_stream` | `business_capability` | P2 | optional | direct edge | optional: `strength` | High-level связка stream ↔ capability |
| `rel_value_stream_depends_on_stream` | `value_stream` | `value_stream` | P2 | optional | qualified edge | `dependency_type` | Межпоточные зависимости |
| `rel_function_depends_on_function` | `business_function` | `business_function` | P2 | optional | qualified edge | `dependency_type`, `criticality` | Future-state functional dependency map |
| `rel_entity_lifecycle_precedes_entity` | `business_entity` | `business_entity` | P2 | optional | qualified edge | `lifecycle_role` | Future-state lifecycle/business object transformations |

---

## 6) MVP mandatory relations

Для MVP mandatory должны существовать и быть поддержаны в import/validation как минимум следующие связи:

1. `value_stream -> value_stream_stage`
2. `value_stream_stage -> business_process`
3. `business_capability -> business_process`
4. `business_process -> business_operation`
5. `business_operation -> business_function`
6. `business_process -> business_entity`
7. `business_operation -> business_entity`
8. `information_flow -> business_entity`

Это минимальный business-layer backbone, который позволяет:
- идти от end-to-end value к конкретному process;
- раскрывать process до operation-level;
- объяснять, какая функция выполняется конкретным шагом;
- видеть, над каким бизнес-объектом идёт работа;
- связывать шаги/процессы с information flow.

Без этого backbone система теряет explainability для process-centric navigation и плохо поддерживает BPMN activity context.

---

## 7) Direct edges vs qualified edges

### 7.1 Где нужны direct edges

Direct edges нужны там, где:
- семантика связи устойчива и бинарна;
- тип связи часто участвует в traversal allowlists;
- edge-level контекст не обязателен для MVP;
- наличие связи само по себе уже несёт главный смысл.

К direct edges в бизнес-слое относятся:
- `value_stream -> value_stream_stage`
- `value_stream_stage -> business_process`
- `business_capability -> business_process`
- `business_process -> business_operation`
- `business_operation -> business_function`
- `business_process -> information_flow` (P1)
- `value_stream_stage -> business_capability` (P1)
- `business_capability -> business_function` (P1)

### 7.2 Где нужны qualified edges

Qualified edges нужны там, где сама связь требует контекста и без qualifiers теряет смысл.

В бизнес-слое такими связями считаются:
- `business_operation -> business_entity`
  - нужен как минимум тип воздействия: `creates / reads / updates / approves / closes / validates`
- `information_flow -> business_entity`
  - нужен тип полезной нагрузки или роль сущности в потоке
- `business_operation -> information_flow`
  - нужен directionality / interaction type
- `business_process -> business_process`
  - нужен тип зависимости
- `business_operation -> business_operation`
  - нужен порядок, ветвление или условность
- `business_entity -> business_entity`
  - нужна семантическая роль связи

---

## 8) Недопустимые связи на уровне бизнес-слоя

Следующие связи считаются недопустимыми или anti-pattern по умолчанию:

### 8.1 `business_process -> business_function` как primary decomposition
Недопустимо использовать `business_function` вместо `business_operation` как основной детализирующий слой процесса.

Причина:
- ломается различие между устойчивой функцией и исполняемым шагом;
- BPMN activity mapping начинает попадать в функцию, а не в operation;
- теряется корректный process execution layer.

Допускается только как transitional or derived relation post-MVP, но не как canonical backbone.

### 8.2 `value_stream -> business_operation` как primary relation
Слишком короткое замыкание уровней. Размывает управленческую структуру между stream/stage/process.

### 8.3 `business_capability -> business_operation` как P0 relation
Не запрещено навсегда, но недопустимо как core MVP relation. Capability должно связываться прежде всего с процессами и/или функциями, а не прыгать сразу к operation layer.

### 8.4 `business_entity -> business_function` как canonical mandatory relation
Для MVP это слишком абстрактно и дублирует более точные связи через process/operation. Допустимо только future-state, если появится ясный use case.

### 8.5 `information_flow -> business_process` как единственная точка привязки к data semantics
Недостаточно. Поток должен быть связан не только с процессом, но и с тем, **что именно переносится**, то есть с `business_entity`.

---

## 9) Relation semantics by kind

### 9.1 `value_stream`
Обязательные исходящие:
- к `value_stream_stage`

Допустимые future-state:
- к `business_capability`
- к другому `value_stream`

### 9.2 `value_stream_stage`
Обязательные:
- входящее от `value_stream`
- исходящее к `business_process`

Допустимые:
- исходящее к `business_capability`

### 9.3 `business_capability`
Обязательные:
- исходящее к `business_process`

Допустимые:
- исходящее к `business_function`
- входящее от `value_stream_stage`
- входящее от `value_stream`

### 9.4 `business_process`
Обязательные:
- входящее от `value_stream_stage`
- входящее от `business_capability`
- исходящее к `business_operation`
- исходящее к `business_entity`

Допустимые:
- к `information_flow`
- к другому `business_process`

### 9.5 `business_operation`
Обязательные:
- входящее от `business_process`
- исходящее к `business_function`
- исходящее к `business_entity`

Допустимые:
- к `information_flow`
- к другой `business_operation`

### 9.6 `business_function`
Обязательные:
- входящее от `business_operation`

Допустимые:
- входящее от `business_capability`
- к другой `business_function` (future-state)

### 9.7 `business_entity`
Обязательные:
- входящее от `business_process`
- входящее от `business_operation`
- входящее от `information_flow`

Допустимые:
- к другой `business_entity`

### 9.8 `information_flow`
Обязательные:
- исходящее к `business_entity`

Допустимые:
- входящее от `business_process`
- входящее от `business_operation`

---

## 10) Minimal inverse strategy

На уровне business-layer matrix рекомендуется уже сейчас зафиксировать логические inverse semantics:

- `value_stream contains stage` ↔ `stage belongs to value_stream`
- `stage realized by process` ↔ `process belongs to stage`
- `capability aggregates processes` ↔ `process realizes capability`
- `process decomposes to operation` ↔ `operation belongs to process`
- `operation executes function` ↔ `function executed by operation`
- `process serves entity` ↔ `entity served by process`
- `operation acts on entity` ↔ `entity acted on by operation`
- `information_flow carries entity` ↔ `entity carried by information_flow`

Даже если runtime initially хранит только canonical direction, inverse semantics должны существовать в relation catalog и UI labels.

---

## 11) Traversal guidance for MVP

### Safe defaults for business-centric explore
Для Explore/Neighbors по business-layer:
- `depth=2` по умолчанию;
- stop at `business_entity` и `business_function`, если пользователь не просил deeper analysis;
- allowlists должны предпочитать P0 relation kinds.

### Impact / blast radius
Для impact analysis вокруг `business_process`:
- обязателен выход к `business_operation` и `business_entity`;
- P1-process dependencies можно включать только осознанно через allowed relations.

### Path mode
Для path explanation в business-layer:
- P0 relations должны иметь приоритет как «менее шумные»;
- P1/P2 relations не должны доминировать при ранжировании путей по умолчанию.

---

## 12) Source realism for MVP

С учётом текущего source mapping:
- `csv_excel` уже поставляет `business_process`, `business_capability`, `business_entity` и relation `rel_capability_aggregates_processes`, `rel_process_serves_entity`; это делает backbone частично ingestable уже на MVP.
- `bpmn` сейчас поставляет `business_process`, `business_function`, `information_flow` и relation `rel_process_uses_function`, но после принятого решения по `business_operation` mapping должен быть обновлён в пользу `business_operation`.

Следствие:
- relation matrix должна считаться **нормативной целью**, а не точным отражением уже имеющихся источников;
- ingestability review потом должен отдельно честно отметить, какие P0 relations доступны сразу, а какие потребуют source mapping upgrade.

---

## 13) Автоматические проверки полноты

После появления generators/validators полнота бизнес-модели должна проверяться автоматически.

### 13.1 Kind-level checks
- каждый `business_process` в MVP pilot должен иметь хотя бы одну связь к `business_capability`;
- каждый `business_process` должен иметь хотя бы одну связь к `business_operation`;
- каждый `business_operation` должен иметь хотя бы одну связь к `business_function`;
- каждый `business_operation` должен иметь хотя бы одну связь к `business_entity`;
- каждый `information_flow` должен быть связан хотя бы с одной `business_entity`.

### 13.2 Graph-shape checks
- не должно быть process nodes без decomposition, если процесс помечен как mapped_to_bpmn;
- не должно быть operation nodes без parent process;
- не должно быть function nodes, которые canonically висят только на process without operation layer;
- не должно быть isolated `value_stream_stage` без `value_stream` или `business_process`.

### 13.3 Anti-pattern checks
- запретить `business_process -> business_function` как единственную decomposition relation в canonical model;
- предупреждать о `business_capability -> business_operation` в MVP datasets;
- предупреждать о `value_stream -> business_process` без stage layer, кроме явно помеченных migration cases.

---

## 14) Примеры канонических путей

### Path A — business value to execution step
`value_stream -> value_stream_stage -> business_process -> business_operation -> business_function`

### Path B — process to affected business object
`business_process -> business_operation -> business_entity`

### Path C — process to information semantics
`business_process -> business_operation -> information_flow -> business_entity`

### Path D — capability to concrete execution context
`business_capability -> business_process -> business_operation -> business_entity`

Эти пути должны считаться «хорошими» и low-noise для path ranking и demo scenarios.

---

## 15) Решения, намеренно отложенные

В этой сессии специально **не фиксируются**:
- формальный `relation_catalog v2` как сериализуемый runtime artifact;
- полная policy по `qualified edges vs link entities`;
- evidence policy по relation kinds;
- cross-layer relation matrix (business ↔ IT ↔ data ↔ org).

Они будут зафиксированы следующими сессиями.

---

## 16) Итоговое решение

Для MVP и ближайшей архитектурной траектории бизнес-слой должен опираться на следующий backbone:

- `value_stream -> value_stream_stage`
- `value_stream_stage -> business_process`
- `business_capability -> business_process`
- `business_process -> business_operation`
- `business_operation -> business_function`
- `business_process -> business_entity`
- `business_operation -> business_entity`
- `information_flow -> business_entity`

При этом:
- `business_operation` является обязательным execution-layer kind;
- `business_function` не используется как основной replacement для operation;
- связи к `business_entity` и `information_flow` в operation layer должны поддерживать qualifiers;
- `business_process -> business_function` остаётся недопустимым как canonical primary decomposition.

Этот документ считается нормативной матрицей для:
- следующей сессии по `relation_catalog v2`;
- policy по qualified edges;
- source-to-ontology ingestability review;
- automatic completeness checks на MVP datasets.
