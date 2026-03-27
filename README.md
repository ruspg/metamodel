# Operating Metamodel

> Язык и грамматика моделирования операционной деятельности банка — от стратегии до инфраструктуры.

**Operating Metamodel** задаёт типы сущностей и связей, по которым описывается вся деятельность и архитектура организации: какие сущности существуют (capabilities, процессы, системы, компоненты, данные, инфраструктура), как они связаны между собой и на каких уровнях детализации это описывается.

Метамодель — это не конкретные объекты, а **правила**, по которым объекты создаются: типы сущностей, допустимые связи между ними, атрибуты и ограничения.

---

## Место в архитектуре

```
Operating Metamodel          Язык и грамматика: какие типы сущностей и связей бывают
        │
        ▼
    Онтология                Семантический словарь: конкретные понятия домена (Клиент, Продукт, Риск)
        │
        ▼
Business Architecture       Модели бизнеса: процессы, способности, оргструктура, KPI
        │
        ▼
   Digital Twin              Живой двойник: модели + фактические данные + время + сценарии
```

| Слой | На что отвечает | Изменчивость |
|------|----------------|--------------|
| **Metamodel** | Как вообще можно моделировать? | Редко |
| **Онтология** | Что именно есть в нашем домене? | При смене понимания домена |
| **Business Architecture** | Как устроен и работает бизнес? | При изменениях стратегии |
| **Digital Twin** | Как бизнес реально ведёт себя во времени? | Постоянно |

---

## Ценность

> Полная картина — в [`docs/vision.md`](docs/vision.md): стратегический контекст, индустриальные референсы, целевое видение.

### Composable Enterprise

Запуск нового продукта — это сборка из существующих capabilities, а не переизобретение с нуля. Метамодель показывает какие способности уже есть, какие системы их реализуют, какие данные доступны.

### Снижение структурной сложности

Один способ описывать процессы, события, решения, данные — вместо «зоопарка» форматов в разных командах. Единый словарь, в котором «процесс» означает одно и то же для бизнеса, IT и Data.

### Impact Analysis за секунды

Когда система падает в 2 часа ночи — мгновенно понять какие клиентские сценарии затронуты. Когда регулятор спрашивает — ответить из графа, а не собирать информацию неделю.

### Машиночитаемый каркас для AI

LLM и AI-агенты получают структурированный контекст через MCP-интерфейс: семантический поиск, генерация BPMN, Text2SQL, «что если» анализ. Метамодель — это operating system for knowledge, а не документация.

### Data Contracts и сертификация

Формализация обязательств между производителями и потребителями данных через SLI/SLO/SLA-фреймворк. Уровни сертификации привязаны к типу потребления: регуляторная отчётность, аналитика, операционка.

### Regulatory Readiness by Design

Аудит-готовность встроена в архитектуру: сквозная прослеживаемость от стратегических целей до инфраструктуры, от бизнес-процессов до таблиц данных. Compliance — не разовый проект, а свойство системы.

---

## Уровни метамодели

| Уровень | Смысл | Примеры сущностей |
|---------|-------|-------------------|
| **Strategic View** | Зачем и что в целом: цели, направления, capabilities | Стратегические цели, KPI, ценностные цепочки, capabilities |
| **Business Details** | Как бизнес устроен и работает | Бизнес-функции, процессы, роли, бизнес-сервисы, правила |
| **Data Details** | Какие данные используются и как устроены | Информационные объекты, модели данных, потоки, метаданные |
| **Solution Details** | Какими решениями поддерживается бизнес | Прикладные решения, сервисы, интерфейсы, интеграции |
| **Component Details** | Из чего состоят решения внутри | Компоненты, внутренние контракты, конфигурации |
| **Infrastructure Details** | На чём всё работает | Платформы, ресурсы, среды, сетевые зоны |

---

## Что умеет этот репозиторий

- Загрузка и валидация метамодели по каноническим правилам
- Проверка целостности relation catalog и архитектурных ограничений
- Семантический линтинг (именование, алиасы, консистентность)
- Построение projection-представлений (профили проекций, например `atlas_mvp`)
- Генерация детерминированных release-бандлов (`generated/`)
- Экспорт в OWL/Turtle для семантических сценариев
- Экспорт в Mermaid для визуального анализа и документирования

---

## Быстрый старт

```bash
make validate      # Валидация: loader + validator + lint + relation catalog
make lint          # Семантический линтер
make test          # Pytest-тесты
make bundle        # Генерация бандла → generated/
make diff          # Дельта bundle vs baseline
make determinism   # Проверка воспроизводимости сборки
make all           # validate + lint + test
```

> **Хотите внести изменения?** Читайте [`CONTRIBUTING.md`](CONTRIBUTING.md) — пошаговые инструкции: как добавить сущность, связь, атрибут или квалификатор.

---

## Структура репозитория

```
metamodel/
├── model/                          # Авторинг метамодели
│   ├── metamodel.yaml              #   Entity kinds + атрибуты + словари
│   ├── relation_catalog.yaml       #   Relation kinds + квалификаторы
│   ├── profiles/                   #   Профили проекций (atlas_mvp)
│   ├── templates/                  #   Шаблоны для контрибьюторов
│   ├── schema/                     #   JSON Schema валидационные контракты
│   └── glossary/                   #   Термины, алиасы, политики именования
├── tools/                          # Инструменты (harness, генераторы)
│   └── wave1/                      #   Loader → Validator → Lint → Projection → Bundle
├── tests/                          # Тесты регрессии и стабильности
├── generated/                      # Иммутабельные release-бандлы
│   └── atlas_candidates/           #   Версионированные бандлы
├── docs/                           # Архитектурные контракты и решения
│   ├── architecture/               #   Контракты entity, relation, attribute, qualifier
│   ├── decisions/                  #   ADR (Architecture Decision Records)
│   └── atlas-bundle/               #   Контракт выходных артефактов
├── metamodel2owl/                  # OWL/Turtle-конвертер + CLI
└── metamodel_to_mermaid/           # Mermaid-конвертер (flow, ER, уровни)
```

---

## Пайплайн

```
  YAML-авторинг          Контроль качества         Проекция           Release
┌──────────────┐    ┌──────────────────────┐    ┌────────────┐    ┌────────────┐
│ metamodel    │    │ Harness              │    │ Projection │    │ Bundle     │
│   .yaml      │───▶│  loader              │───▶│ Builder    │───▶│ Generator  │──▶ generated/
│ relation_    │    │  validator           │    │ (profile)  │    │            │
│   catalog    │    │  lint                │    └────────────┘    └────────────┘
│   .yaml      │    │  relation catalog    │
└──────────────┘    │  checks              │
                    └──────────────────────┘
```

Каждый бандл содержит:
- `metamodel_snapshot.json` — компактное runtime-представление
- `type_catalog.json` — типы сущностей и атрибуты
- `relation_catalog.json` — типы связей и правила
- `search_aliases.json` — алиасы для поиска
- `compatibility_report.md` — отчёт совместимости

---

## Экспорт и визуализация

### OWL/Turtle

```bash
metamodel2owl \
  --input model/metamodel.yaml \
  --output build/bank-metamodel.ttl \
  --format turtle \
  --base-iri "https://bank.example.com/metamodel#"
```

### Mermaid-диаграммы

```bash
# Полная диаграмма с группировкой по уровням
python -m metamodel_to_mermaid \
  --input model/metamodel.yaml \
  --output docs/metamodel-all.mmd \
  --view all --diagram-type flow --group-by level --with-notes

# ER-срез по data-слою
python -m metamodel_to_mermaid \
  --input model/metamodel.yaml \
  --output docs/metamodel-data.mmd \
  --view data --diagram-type er
```

Комбинированный экспорт (OWL + Mermaid одной командой):

```bash
metamodel2owl \
  --input model/metamodel.yaml \
  --output build/bank-metamodel.ttl \
  --mermaid-output build/bank-metamodel.mmd \
  --format turtle \
  --base-iri "https://bank.example.com/metamodel#"
```

---

## Философия авторинга

Метамодель хранится в **двух файлах**, а не разбита по файлам на каждый kind. Это осознанное решение: метамодель — это схема с высокой связностью, редкими изменениями и потребностью в целостном ревью.

| Файл | Содержимое | Кто меняет |
|------|-----------|------------|
| `model/metamodel.yaml` | Entity kinds, атрибуты, словари | Доменные архитекторы |
| `model/relation_catalog.yaml` | Связи, квалификаторы, traversal | Graph/platform-архитекторы |
| `model/profiles/atlas_mvp.yaml` | Видимость kinds/relations | Продуктовая команда |

Подробное обоснование с индустриальными референсами (Schema.org, ArchiMate, TOGAF, OMG ODM):
[`docs/architecture/authoring_rationale.md`](docs/architecture/authoring_rationale.md).

---

## RBank Atlas

Atlas — graph-first enterprise registry, один из downstream-потребителей метамодели. Изменения в `model/` проходят валидацию, собираются в профильный бандл (`atlas_mvp`) и синхронизируются с Atlas через версионированные артефакты в `generated/`.

Контракт выходных артефактов: [`docs/atlas-bundle/README.md`](docs/atlas-bundle/README.md).

---

## Документация

### Для контрибьюторов

| Документ | Описание |
|----------|----------|
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Как добавить сущность, связь, атрибут или квалификатор |
| [`docs/metamodel_yaml_format.md`](docs/metamodel_yaml_format.md) | Формат YAML-файла метамодели |
| [`docs/metamodel_contribution_rules.md`](docs/metamodel_contribution_rules.md) | Правила контрибьюшена и проверки |

### Архитектурные контракты

| Документ | Описание |
|----------|----------|
| [`entity_kind_contract_v2.md`](docs/architecture/entity_kind_contract_v2.md) | Контракт типа сущности |
| [`relation_kind_contract_v2.md`](docs/architecture/relation_kind_contract_v2.md) | Контракт типа связи |
| [`attribute_def_contract_v2.md`](docs/architecture/attribute_def_contract_v2.md) | Контракт атрибутов |
| [`qualifier_def_contract_v2.md`](docs/architecture/qualifier_def_contract_v2.md) | Контракт квалификаторов |
| [`glossary_alias_naming_policy.md`](docs/architecture/glossary_alias_naming_policy.md) | Правила именования |
| [`relation_catalog_v2_rules.md`](docs/architecture/relation_catalog_v2_rules.md) | Правила каталога связей |

### Дизайн и решения

| Документ | Описание |
|----------|----------|
| [`ontology_schema_v2_high_level_design.md`](docs/architecture/ontology_schema_v2_high_level_design.md) | Высокоуровневый дизайн схемы онтологии |
| [`authoring_rationale.md`](docs/architecture/authoring_rationale.md) | Обоснование структуры авторинга |
| [`docs/decisions/`](docs/decisions/) | Журнал архитектурных решений (ADR) |

### Внутренние справочники

| Документ | Описание |
|----------|----------|
| [`model/README.md`](model/README.md) | Содержимое и статус директории модели |
| [`tools/README.md`](tools/README.md) | Обзор инструментов и сценариев |
| [`generated/README.md`](generated/README.md) | Сгенерированные артефакты и бандлы |
| [`docs/atlas-bundle/README.md`](docs/atlas-bundle/README.md) | Контракт выходных артефактов Atlas-бандла |
