# Wave 1 atlas candidate bundles

This directory contains versioned, deterministic Wave 1 atlas candidate bundles generated from the canonical ontology/profile inputs.

## Current candidate

- Version: `1`
- Profile: `atlas_mvp`
- Bundle path: `generated/atlas_candidates/bank_metamodel_horizontal__1__atlas_mvp/`

## Generation command

```bash
python - <<'PY'
from pathlib import Path
from tools.wave1.loader import load_ontology
from tools.wave1.projection_builder import build_projection_model
from tools.wave1.atlas_bundle_generator import generate_atlas_bundle

root = Path('.')
ontology = load_ontology(
    root / 'data/bank_metamodel_horizontal.yaml',
    relation_catalog_path=root / 'docs/architecture/relation_catalog_v2_spec.yaml',
)
projection = build_projection_model(ontology, profile='atlas_mvp')
result = generate_atlas_bundle(projection, root / 'generated/atlas_candidates')
print(result.bundle_root)
PY
```
