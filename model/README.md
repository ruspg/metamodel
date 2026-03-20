# Wave 1 canonical model area

This directory is the canonical home for Wave 1 ontology authoring artifacts.

## Layout

- `metamodel.yaml` — entity kinds, attributes, dictionaries, and meta (the core ontology schema).
- `relation_catalog.yaml` — relation kinds, qualifier definitions, and traversal rules.
- `profiles/` — profile projection filters (e.g. `atlas_mvp.yaml`).
- `templates/` — copy-paste starters for contributors adding new kinds or relations.
- `schema/` — JSON Schema validation contracts.
- `glossary/` — glossary terms, aliases, and naming policy artifacts.

See the [design rationale](../README.md#authoring-structure-design-rationale)
in the repository README for why the metamodel uses two source files rather than
file-per-kind.

## Migration status

Wave 1 keeps existing source assets in their current locations for backward legibility:
- current ontology YAML sources stay in `data/`;
- current root schema stays in `schema/`;
- converters stay in `metamodel2owl/` and `metamodel_to_mermaid/`.

Canonical target: `model/metamodel.yaml` + `model/relation_catalog.yaml`.
