# Бандлы-кандидаты Atlas

Эта директория содержит версионированные детерминированные бандлы-кандидаты Atlas, сгенерированные из канонических входных данных онтологии и профиля.

Идентификаторы бандлов иммутабельны: однажды опубликованный путь бандла не должен повторно использоваться для других артефактов.

## Текущий кандидат

- Версия: `2`
- Профиль: `atlas_mvp`
- Путь бандла: `generated/atlas_candidates/bank_metamodel_horizontal__1__atlas_mvp__v2/`
- Предыдущий промотированный кандидат сохранён как иммутабельный исторический артефакт: `generated/atlas_candidates/bank_metamodel_horizontal__1__atlas_mvp/`

## Команда генерации

```bash
python - <<'PY'
from pathlib import Path
from tools.wave1.loader import load_ontology
from tools.wave1.projection_builder import build_projection_model
from tools.wave1.atlas_bundle_generator import generate_atlas_bundle
from tools.wave1.atlas_bundle_model import AtlasBundleOptions

root = Path('.')
ontology = load_ontology(
    root / 'model/metamodel.yaml',
    relation_catalog_path=root / 'model/relation_catalog.yaml',
)
projection = build_projection_model(ontology, profile='atlas_mvp')
result = generate_atlas_bundle(
    projection,
    root / 'generated/atlas_candidates',
    options=AtlasBundleOptions(
        profile='atlas_mvp',
        bundle_name='bank_metamodel_horizontal__1__atlas_mvp__v2',
    ),
)
print(result.bundle_root)
PY
```
