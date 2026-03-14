# metamodel

Repository for Wave 1 ontology authoring and release preparation.

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
