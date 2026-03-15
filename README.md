# Metamodel

> Единое рабочее пространство для проектирования, проверки и публикации корпоративной метамодели (Wave 1).

`metamodel` — это репозиторий, в котором собраны:
- **исходные YAML-описания** доменной модели,
- **инструменты контроля качества** (валидация, линтинг, проверки связей),
- **генераторы артефактов** для downstream-систем,
- **конвертеры в OWL и Mermaid** для интеграции и визуализации.

Проект ориентирован на предсказуемую и воспроизводимую подготовку релизов онтологии: от редактирования модели до получения детерминированного bundle.

---

## Что умеет проект

- ✅ Загружать и валидировать метамодель по каноническим правилам Wave 1.
- ✅ Проверять целостность relation catalog и архитектурных ограничений.
- ✅ Строить projection-представления (например, `atlas_mvp`).
- ✅ Генерировать release bundle в `generated/`.
- ✅ Гарантировать **детерминированность** сборки (одинаковый вход → одинаковый результат).
- ✅ Экспортировать модель в:
  - **OWL/Turtle** для семантических сценариев,
  - **Mermaid** для документирования и визуального анализа.

---

## Архитектура репозитория

Каноническая структура Wave 1 разделяет ответственность по зонам:

- `model/` — целевая структура авторинга (схемы, типы, связи, глоссарий).
- `profiles/` — профили проекций и публикации.
- `tools/` — служебные инструменты Wave 1 (harness, генераторы, проверки).
- `tests/` — тесты регрессии и проверок стабильности пайплайна.
- `generated/` — сгенерированные артефакты сборки.

Текущий этап — плавный переход от legacy к канонической структуре:

- рабочие исходники YAML пока сохраняются в `data/`,
- историческая схема остаётся в `schema/`,
- существующие конвертеры доступны в `metamodel2owl/` и `metamodel_to_mermaid/`.

---

## Быстрый старт для разработчика

### 1) Запуск полного validation harness

```bash
python -m tools.wave1.harness \
  data/bank_metamodel_horizontal.yaml \
  --relation-catalog-path docs/architecture/relation_catalog_v2_spec.yaml
```

Этот сценарий запускает канонический набор проверок Wave 1:
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
    root / "data/bank_metamodel_horizontal.yaml",
    relation_catalog_path=root / "docs/architecture/relation_catalog_v2_spec.yaml",
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
    root / "data/bank_metamodel_horizontal.yaml",
    relation_catalog_path=root / "docs/architecture/relation_catalog_v2_spec.yaml",
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
  --input data/bank_metamodel_horizontal.yaml \
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
  --input data/enterprise_metamodel.yaml \
  --output docs/metamodel-all.mmd \
  --view all \
  --diagram-type flow \
  --group-by level \
  --with-notes
```

Пример точечного ER-среза:

```bash
python -m metamodel_to_mermaid \
  --input data/enterprise_metamodel.yaml \
  --output docs/metamodel-data.mmd \
  --view data \
  --diagram-type er
```

---

## Дополнительная документация

- `model/README.md` — правила и статус структуры модели.
- `tools/README.md` — обзор инструментов и сценариев Wave 1.
- `docs/` — форматы, contribution rules и архитектурные спецификации.

Если хотите, следующим шагом можно добавить в README:
- минимальный «happy path» от изменения YAML до готового релизного артефакта,
- раздел «частые ошибки и диагностика»,
- диаграмму пайплайна Wave 1 (в Mermaid).
