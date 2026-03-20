# Инструменты

Каноническое расположение тулинга репозитория.

## Текущее состояние

Существующие конвертеры сохранены на своих местах, чтобы не ломать текущие рабочие процессы:
- `metamodel2owl/` — CLI экспорта в OWL + Mermaid
- `metamodel_to_mermaid/` — пайплайн рендеринга Mermaid-диаграмм

Директория `tools/` — целевое место для загрузчиков, валидаторов, генераторов и скриптов релиза.

## Загрузчик онтологии
- `tools/wave1/loader.py` — `load_ontology(...)` для детерминированной структурной загрузки и нормализации.
- `tools/wave1/model.py` — нормализованные dataclass-модели, используемые последующими задачами валидации и генерации.

## Валидатор онтологии
- `tools/wave1/validator.py` — `validate_ontology(...)` для структурных и контрактных проверок нормализованной модели.
- `ensure_valid_ontology(...)` — выбрасывает читаемую ошибку, сохраняя структурированный результат для тестов и ревью.

## Линтер онтологии
- `tools/wave1/lint.py` — `lint_ontology(...)` для семантических проверок качества (именование, алиасы, глоссарий, консистентность связей) после структурной валидации.

## Валидатор каталога связей
- `tools/wave1/relation_catalog_validator.py` — `validate_relation_catalog(...)` и `ensure_valid_relation_catalog(...)` для выделенных проверок каталога связей перед генерацией.

## Валидационный harness
- `tools/wave1/harness.py` — `run_wave1_validation_harness(...)` запускает загрузку + валидацию онтологии + линт + валидацию каталога связей в одном детерминированном потоке.
- Локальный запуск: `python -m tools.wave1.harness model/metamodel.yaml --relation-catalog-path model/relation_catalog.yaml`

## Построитель проекций
- `tools/wave1/projection_builder.py` — `build_projection_model(...)` для детерминированного профильного формирования валидированных данных онтологии в модель, готовую для генератора.
- `tools/wave1/projection_model.py` — dataclass-модели проекции, используемые как входные данные для генераторов бандлов.

## Генератор Atlas-бандла
- `tools/wave1/atlas_bundle_generator.py` — `generate_atlas_bundle(...)` — каноническая точка входа для оркестрации генерации бандла из проекционной модели.
- `tools/wave1/atlas_bundle_model.py` — dataclass-модели манифеста и результатов бандла, структуры планирования артефактов.
- `tools/wave1/metamodel_snapshot_generator.py` — генерация `metamodel_snapshot.json` — компактного детерминированного runtime-представления метамодели для активного профиля.
- `tools/wave1/type_catalog_generator.py` — генерация `type_catalog.json` — компактного каталога типов и атрибутов для активного профиля.
- `tools/wave1/relation_catalog_generator.py` — генерация `relation_catalog.json` — компактного каталога связей для активного профиля.
- `tools/wave1/search_aliases_generator.py` — генерация `search_aliases.json` — проекции алиасов и дисамбигуации для активного профиля.
- `tools/wave1/compatibility_report_generator.py` — генерация `compatibility_report.md` — отчёта совместимости релиза по сгенерированным артефактам бандла.
- `tools/wave1/bundle_determinism.py` — `verify_bundle_determinism(...)` — повторная генерация бандла и сравнение путей файлов, байтов, порядка манифеста и артефактов с диагностикой дрейфа.
