# Atlas candidate bundles

This directory contains versioned, deterministic atlas candidate bundles generated from the canonical ontology/profile inputs.

Bundle identifiers are immutable: once published, a bundle path must never be reused for different artifacts.

## Current candidate

- Version: `2`
- Profile: `atlas_mvp`
- Bundle path: `generated/atlas_candidates/bank_metamodel_horizontal__1__atlas_mvp__v2/`
- Prior promoted candidate retained as immutable historical artifact: `generated/atlas_candidates/bank_metamodel_horizontal__1__atlas_mvp/`

## Generation command

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
