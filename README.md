# Metamodel

> Единое рабочее пространство для проектирования, проверки и публикации корпоративной метамодели.

`metamodel` — это репозиторий, в котором собраны:
- **исходные YAML-описания** доменной модели,
- **инструменты контроля качества** (валидация, линтинг, проверки связей),
- **генераторы артефактов** для downstream-систем,
- **конвертеры в OWL и Mermaid** для интеграции и визуализации.

Проект ориентирован на предсказуемую и воспроизводимую подготовку релизов онтологии: от редактирования модели до получения детерминированного bundle.

---

## Что умеет проект

- ✅ Загружать и валидировать метамодель по каноническим правилам.
- ✅ Проверять целостность relation catalog и архитектурных ограничений.
- ✅ Строить projection-представления (например, `atlas_mvp`).
- ✅ Генерировать release bundle в `generated/`.
- ✅ Гарантировать **детерминированность** сборки (одинаковый вход → одинаковый результат).
- ✅ Экспортировать модель в:
  - **OWL/Turtle** для семантических сценариев,
  - **Mermaid** для документирования и визуального анализа.

---

## Архитектура репозитория

```
metamodel/
├── model/                        # Авторинг метамодели
│   ├── metamodel.yaml            #   Entity kinds + dictionaries
│   ├── relation_catalog.yaml     #   Relation kinds + qualifiers
│   ├── profiles/                 #   Профили проекций
│   ├── templates/                #   Шаблоны для контрибьюторов
│   └── schema/                   #   Валидационные контракты
├── tools/                        # Инструменты (harness, генераторы)
├── tests/                        # Тесты регрессии и стабильности
├── generated/                    # Иммутабельные release-бандлы
├── docs/                         # Архитектурные контракты и решения
├── metamodel2owl/                # OWL-конвертер
└── metamodel_to_mermaid/         # Mermaid-конвертер
```

Подробнее о том, почему `model/` содержит два файла, а не file-per-kind —
см. [Структура авторинга: обоснование](#структура-авторинга-обоснование).

---

## Быстрый старт для разработчика

### 1) Запуск полного validation harness

```bash
python -m tools.wave1.harness \
  model/metamodel.yaml \
  --relation-catalog-path model/relation_catalog.yaml
```

Этот сценарий запускает канонический набор проверок:
loader + validator + lint + relation catalog checks.

### 2) Генерация Atlas bundle

```bash
python - <<'PY'
from pathlib import Path
from tools.wave1.loader import load_ontology
from tools.wave1.projection_builder import build_projection_model
from tools.wave1.atlas_bundle_generator import generate_atlas_bundle

root = Path(".")
ontology = load_ontology(
    root / "model/metamodel.yaml",
    relation_catalog_path=root / "model/relation_catalog.yaml",
)
projection = build_projection_model(ontology, profile="atlas_mvp")
result = generate_atlas_bundle(projection, root / "generated")
print(result.bundle_root)
PY
```

### 3) Проверка детерминированности bundle

```bash
python - <<'PY'
from pathlib import Path
from tools.wave1.loader import load_ontology
from tools.wave1.projection_builder import build_projection_model
from tools.wave1.bundle_determinism import verify_bundle_determinism

root = Path(".")
ontology = load_ontology(
    root / "model/metamodel.yaml",
    relation_catalog_path=root / "model/relation_catalog.yaml",
)
projection = build_projection_model(ontology, profile="atlas_mvp")
result = verify_bundle_determinism(projection, root / "generated")
print(result.is_deterministic, result.diagnostics)
PY
```

---

## Экспорт и визуализация

### OWL + Mermaid из `metamodel2owl`

```bash
metamodel2owl \
  --input model/metamodel.yaml \
  --output build/bank-metamodel.ttl \
  --mermaid-output build/bank-metamodel.mmd \
  --format turtle \
  --base-iri "https://bank.example.com/metamodel#"
```

`--mermaid-output` создаёт Mermaid-диаграмму (`graph LR`):
- узлы — сущности и их атрибуты,
- рёбра — связи из метамодели.

### Расширенные Mermaid-представления (`metamodel_to_mermaid`)

```bash
python -m metamodel_to_mermaid \
  --input model/metamodel.yaml \
  --output docs/metamodel-all.mmd \
  --view all \
  --diagram-type flow \
  --group-by level \
  --with-notes
```

Пример точечного ER-среза:

```bash
python -m metamodel_to_mermaid \
  --input model/metamodel.yaml \
  --output docs/metamodel-data.mmd \
  --view data \
  --diagram-type er
```

---

## Структура авторинга: обоснование

### Почему не file-per-kind?

Интуитивный подход к inner-source — разбить метамодель на один файл на каждый
entity kind (как one-class-per-file в коде). Мы сознательно **не делаем этого**,
потому что метамодель — это схема, а не кодовая база:

| Фактор | Кодовая база (тысячи файлов) | Метамодель (26 kinds, 39 relations) |
|--------|------------------------------|--------------------------------------|
| Частота изменений | Ежедневно, десятки разработчиков | Раз в квартал, 2-5 архитекторов |
| Связность изменений | Низкая — фичи независимы | Высокая — новый kind = новые relations + qualifiers + profile |
| Стиль ревью | Diff по модулю | Целостный: вписывается ли новый kind в онтологию? |
| Merge-конфликты | Реальная проблема | Не проблема при ~600 строках YAML |
| Навигация | Нужна структура | 600 строк = 2-3 экрана |

### Индустриальные референсы

Крупнейшие онтологические и метамодельные проекты хранят определения типов
в одном или нескольких файлах, даже при значительно большем масштабе:

- **[Schema.org](https://github.com/schemaorg/schemaorg)** — 803 типа,
  1461 свойство в **одном файле** (`data/schema.ttl`). Расширения отдельно
  (`data/ext/*/`), но ядро — монолит.
- **[ArchiMate 3.2](https://pubs.opengroup.org/architecture/archimate3-doc/ch-Generic-Metamodel.html)**
  — ~57 типов элементов, ~11 типов связей. Единая спецификация.
- **[TOGAF Content Metamodel](https://pubs.opengroup.org/architecture/togaf9-doc/arch/chap30.html)**
  — 11 core-сущностей (до ~50 с расширениями). Один документ + extension-модули.
- **[OMG ODM](https://www.omg.org/odm/)** — семейство метамоделей, каждая —
  единая спецификация с модульными профилями.

Паттерн единообразен: **метамодель = один документ на concern**,
расширения — отдельными модулями, когда аудитория или lifecycle расходятся.

### Рекомендуемая структура

**Два исходных файла, а не двадцать шесть.** Разделение — по concern и lifecycle:

| Файл | Что меняется | Кто меняет | Как часто |
|------|-------------|------------|-----------|
| `model/metamodel.yaml` | Entity kinds, атрибуты, словари | Доменные архитекторы | Редко |
| `model/relation_catalog.yaml` | Связи, квалификаторы, traversal | Graph/platform-архитекторы | Иногда |
| `model/profiles/atlas_mvp.yaml` | Какие kinds/relations видны | Продуктовая команда | На каждый релиз |

### Что обеспечивает inner-source (а не структура файлов)

1. **Шаблоны** (`model/templates/`) — контрибьютор копирует готовый блок,
   заполняет 6 полей, вставляет в `metamodel.yaml`.

2. **Мгновенная CI-обратная связь** — harness работает за секунды.
   PR-бот комментирует: "Добавлен kind `data_quality_rule`, 2 новых relation,
   дельта бандла +38 строк, обратная совместимость: OK."

3. **Bundle diff в PR** — ревьюер видит как изменились runtime-артефакты,
   а не сырой YAML.

4. **Единый CODEOWNERS** — одна группа `@metamodel-architects` владеет обоими
   файлами. Дробить ownership по уровням метамодели = фрагментировать решение,
   требующее целостного взгляда.

5. **PR-шаблон с чеклистом** — ведёт контрибьютора через обязательные поля
   и правила именования.

### Когда пересмотреть

Если метамодель вырастет за **~80 entity kinds** или relation catalog за
**~120 relations** — рассмотреть разделение по **домену** (не по metamodel level):
`kinds/payments.yaml`, `kinds/lending.yaml` и т.д.

---

## Дополнительная документация

- `model/README.md` — правила и статус структуры модели.
- `tools/README.md` — обзор инструментов и сценариев.
- `docs/` — форматы, contribution rules и архитектурные спецификации.
