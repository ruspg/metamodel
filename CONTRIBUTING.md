# Contributing to the Metamodel

This repository contains the **canonical ontology definitions** for the RBank Atlas platform.
Changes here affect all downstream systems (API, MCP, UI, ingestion).

## Happy path: добавить entity kind за 10 минут

```bash
# 1. Клонировать и зайти
git clone <repo-url> && cd metamodel
git checkout -b feat/add-my-kind

# 2. Скопировать шаблон из model/templates/new_entity_kind.yaml
#    и вставить в конец секции entity_kinds в model/metamodel.yaml:

  - id: data_quality_rule
    name: "Data Quality Rule"
    name_ru: "Правило качества данных"
    metamodel_level: solution_details
    category: data
    description: "Правило проверки качества данных при загрузке в граф."

# 3. Проверить
make validate                    # harness: 0 errors?
make diff                        # что изменится в бандле?

# 4. Коммит + PR
git add model/metamodel.yaml
git commit -m "feat: add data_quality_rule entity kind"
git push -u origin feat/add-my-kind
# Создать PR — CI автоматически:
#   - прогонит validate + lint + test
#   - опубликует комментарий с bundle diff
```

Если нужно добавить **связь** — аналогично, но шаблон из
`model/templates/new_relation_kind.yaml`, вставка в `model/relation_catalog.yaml`.

---

## Quick Start

```bash
git clone <repo-url> && cd metamodel

make validate    # Harness: loader + validator + lint + relation catalog
make lint        # Semantic linter
make test        # Unit tests (74 tests)
make diff        # Bundle diff vs baseline
make help        # Все доступные команды
```

## Что где лежит

| Файл | Что редактировать |
|------|-------------------|
| `model/metamodel.yaml` | Entity kinds, атрибуты, словари |
| `model/relation_catalog.yaml` | Relation kinds, квалификаторы |
| `model/templates/` | Шаблоны — копировать и заполнять |

Контракты (что обязательно, что опционально):
- Entity kinds: `docs/architecture/entity_kind_contract_v2.md`
- Relations: `docs/architecture/relation_kind_contract_v2.md`
- Attributes: `docs/architecture/attribute_def_contract_v2.md`
- Qualifiers: `docs/architecture/qualifier_def_contract_v2.md`

## Что происходит после PR

1. CI прогоняет validate + lint + test + determinism
2. CI постит **bundle diff** — комментарий в PR с перечнем добавленных/удалённых kinds и relations + дельта размеров артефактов
3. Metamodel architect ревьюит
4. После мержа: генерация бандла и импорт в rbank-atlas — отдельный ручной шаг

## Roles

| Role | Responsibility |
|---|---|
| **Metamodel Architect** | Approves all structural changes to kinds/relations |
| **Data Owner** | Confirms attribute definitions for their domain |
| **Platform Team** | Maintains tooling, CI, schema validation |

## Rules

- One change per PR (atomic changes only)
- All entity/relation IDs must use `snake_case`
- `name_ru` is required for all entities and relations
- Breaking changes require an ADR in `docs/decisions/`
- Generated bundles in `generated/` are immutable — never edit them

## Need Help?

- Design rationale: see [README.md](README.md#структура-авторинга-обоснование)
- Full contribution rules: `docs/metamodel_contribution_rules.md`
- Naming policy: `docs/architecture/glossary_alias_naming_policy.md`
- Decision log: `docs/decisions/`
