# metamodel

Repository for Wave 1 ontology authoring and release preparation.

## Wave 1 developer quickstart

Run the canonical Wave 1 validation harness (loader + validator + lint + relation catalog checks):

```bash
python -m tools.wave1.harness \
  data/bank_metamodel_horizontal.yaml \
  --relation-catalog-path docs/architecture/relation_catalog_v2_spec.yaml
```

Generate an atlas bundle from the baseline ontology/profile:

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

Verify deterministic bundle output:

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

## Canonical Wave 1 structure

The canonical authoring/release layout is now scaffolded with these top-level areas:

- `model/schema/`
- `model/kinds/`
- `model/relations/`
- `model/glossary/`
- `profiles/`
- `tools/`
- `tests/`
- `generated/`

See `model/README.md` and `tools/README.md` for migration notes.

## Canonical vs legacy (current phase)

This task establishes the Wave 1 structure without semantic migration:

- Canonical target areas are under `model/`, `profiles/`, `tools/`, and `generated/`.
- Existing source YAML remains in `data/` for backward legibility.
- Existing root schema remains in `schema/`.
- Existing converter tooling remains in `metamodel2owl/` and `metamodel_to_mermaid/`.

## Existing converter usage

### OWL и визуализация Mermaid

```bash
metamodel2owl \
  --input data/bank_metamodel_horizontal.yaml \
  --output build/bank-metamodel.ttl \
  --mermaid-output build/bank-metamodel.mmd \
  --format turtle \
  --base-iri "https://bank.example.com/metamodel#"
```

Флаг `--mermaid-output` создаёт файл с диаграммой Mermaid (`graph LR`), где
узлы соответствуют сущностям и их атрибутам, а рёбра — связям из метамодели.
Такой файл можно вставлять в Markdown или обрабатывать любым Mermaid-рендерером.

### Mermaid CLI with advanced styling

The repository also contains a dedicated converter that produces richer Mermaid
views directly from the YAML metamodel:

```bash
python -m metamodel_to_mermaid \
  --input data/enterprise_metamodel.yaml \
  --output docs/metamodel-all.mmd \
  --view all \
  --diagram-type flow \
  --group-by level \
  --with-notes
```

To focus on a specific slice simply change the flags, for example to get a data ER view:

```bash
python -m metamodel_to_mermaid \
  --input data/enterprise_metamodel.yaml \
  --output docs/metamodel-data.mmd \
  --view data \
  --diagram-type er
```
