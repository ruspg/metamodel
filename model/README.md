# Wave 1 canonical model area

This directory is the canonical home for Wave 1 ontology authoring artifacts.

## Layout
- `schema/` — ontology schema contracts used by authoring/validation workflows.
- `kinds/` — entity/attribute kind definitions (to be incrementally split from monolithic source files).
- `relations/` — relation kind catalogs/rules and related constraints.
- `glossary/` — glossary terms, aliases, and naming policy artifacts.

## Migration status
Wave 1 keeps existing source assets in their current locations for backward legibility:
- current ontology YAML sources stay in `data/`;
- current root schema stays in `schema/`;
- converters stay in `metamodel2owl/` and `metamodel_to_mermaid/`.

New work should target this `model/` tree first, then progressively migrate legacy locations.
