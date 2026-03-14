# Wave 1 repository structure note

## Purpose
This note defines the canonical Wave 1 authoring/release structure introduced by task `W1-A-001` and clarifies what remains legacy during phased migration.

## Canonical directories (Wave 1)
- `model/schema/`
- `model/kinds/`
- `model/relations/`
- `model/glossary/`
- `profiles/`
- `tools/`
- `tests/`
- `generated/`

## Legacy-but-preserved areas
To keep the repository coherent and avoid breaking existing workflows, the following are preserved in place in this task:
- `data/` for current monolithic ontology YAML source files.
- `schema/` for current root metamodel schema.
- `metamodel2owl/` and `metamodel_to_mermaid/` for existing conversion/visualization tooling.

## Practical guidance for next tasks
- New loader/validator/generator/release-bundle work should target canonical Wave 1 areas.
- Legacy areas should be treated as compatibility inputs until dedicated migration tasks relocate or split artifacts.
- This task makes no ontology semantic changes.
