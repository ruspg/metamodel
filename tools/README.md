# tools

Canonical location for Wave 1 repository tooling.

## Current state
Existing converter tooling is preserved in-place to avoid breaking current workflows:
- `metamodel2owl/` (OWL + Mermaid export CLI)
- `metamodel_to_mermaid/` (focused Mermaid rendering pipeline)

This `tools/` directory is the forward-looking home for future loader/validator/generator/release scripts and wrappers.

## Wave 1 ontology loader
- `tools/wave1/loader.py` provides `load_ontology(...)` for deterministic structural loading/normalization.
- `tools/wave1/model.py` defines the normalized in-memory dataclasses consumed by follow-up validation/generation tasks.

## Wave 1 ontology validator
- `tools/wave1/validator.py` provides `validate_ontology(...)` for structural/contract checks over the normalized model.
- `ensure_valid_ontology(...)` raises a readable fatal error while preserving structured result support for tests/review.

## Wave 1 ontology lint
- `tools/wave1/lint.py` provides `lint_ontology(...)` for semantic quality checks (naming/alias/glossary/relation consistency) after structural validation.

## Wave 1 relation catalog validator
- `tools/wave1/relation_catalog_validator.py` provides `validate_relation_catalog(...)` and `ensure_valid_relation_catalog(...)` for dedicated relation-catalog gates prior to generation tasks.

## Wave 1 validation harness
- `tools/wave1/harness.py` provides `run_wave1_validation_harness(...)` to run load + ontology validation + lint + relation catalog validation in one deterministic flow.
- Local CLI usage: `python -m tools.wave1.harness data/bank_metamodel_horizontal.yaml --relation-catalog-path docs/architecture/relation_catalog_v2_spec.yaml`
